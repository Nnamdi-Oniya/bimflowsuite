import os
from pathlib import Path

from celery import group
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils import timezone

from .analysers import ANALYSER_REGISTRY
from .constants import ANALYSIS_TYPE_LABELS, ANALYSIS_TYPE_VALUES
from .models import AnalysisResult, AnalysisSession, IFCAnalysisFile

try:
    import ifcopenshell
except Exception:  # pragma: no cover
    ifcopenshell = None

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except Exception:  # pragma: no cover
    Environment = None
    FileSystemLoader = None
    select_autoescape = None

try:
    from weasyprint import HTML
except Exception:  # pragma: no cover
    HTML = None


def resolve_analysis_file_path(analysis_file: IFCAnalysisFile):
    if analysis_file.source_type == "generated" and analysis_file.generated_ifc:
        if analysis_file.generated_ifc.ifc_file:
            return analysis_file.generated_ifc.ifc_file.path
    if analysis_file.source_type == "uploaded" and analysis_file.uploaded_ifc:
        return analysis_file.uploaded_ifc.path
    return None


def sync_analysis_file_metadata(analysis_file: IFCAnalysisFile):
    """Populate denormalized metadata from the selected source."""
    if not analysis_file.file_url:
        analysis_file.file_url = ""

    if analysis_file.source_type == "generated" and analysis_file.generated_ifc:
        src = analysis_file.generated_ifc
        if src.ifc_file:
            try:
                analysis_file.file_url = src.ifc_file.url
            except Exception:
                analysis_file.file_url = src.ifc_file.name
            try:
                analysis_file.file_size_bytes = src.ifc_file.size
            except Exception:
                pass
        analysis_file.ifc_schema = src.ifc_schema_version or ""
        if not analysis_file.name:
            analysis_file.name = src.name or f"Generated IFC {src.id}"

    if analysis_file.source_type == "uploaded" and analysis_file.uploaded_ifc:
        try:
            analysis_file.file_url = analysis_file.uploaded_ifc.url
        except Exception:
            analysis_file.file_url = analysis_file.uploaded_ifc.name
        try:
            analysis_file.file_size_bytes = analysis_file.uploaded_ifc.size
        except Exception:
            pass
        if not analysis_file.name:
            analysis_file.name = os.path.basename(analysis_file.uploaded_ifc.name)

        if not analysis_file.ifc_schema and ifcopenshell:
            try:
                ifc = ifcopenshell.open(analysis_file.uploaded_ifc.path)
                schema = getattr(ifc, "schema", None)
                if schema:
                    analysis_file.ifc_schema = str(schema).lower()
            except Exception:
                pass


def get_session_analysis_types(session: AnalysisSession):
    normalized = []
    seen = set()

    raw_items = session.analysis_types if isinstance(session.analysis_types, list) else []
    for value in raw_items:
        if not isinstance(value, str):
            continue
        key = value.strip()
        if not key or key not in ANALYSIS_TYPE_VALUES or key in seen:
            continue
        seen.add(key)
        normalized.append(key)
    return normalized


def build_default_session_name(ifc_source: IFCAnalysisFile, analysis_types):
    labels = [ANALYSIS_TYPE_LABELS.get(item, item) for item in analysis_types]
    suffix = ", ".join(labels[:2])
    if len(labels) > 2:
        suffix = f"{suffix}, +{len(labels) - 2} more"
    return f"{ifc_source.name} analysis: {suffix or 'run'}"


def format_file_size(file_size_bytes):
    if file_size_bytes in (None, ""):
        return ""

    size = float(file_size_bytes)
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    decimals = 0 if unit_index == 0 else 1
    return f"{size:.{decimals}f} {units[unit_index]}"


def create_pending_results(session: AnalysisSession, analysis_types):
    for analysis_type in analysis_types:
        AnalysisResult.objects.get_or_create(
            session=session,
            analysis_type=analysis_type,
            defaults={
                "ifc_source": session.ifc_source,
                "status": "pending",
            },
        )


def launch_analysis_session(session: AnalysisSession):
    analysis_types = get_session_analysis_types(session)
    if not analysis_types:
        raise ValueError("No valid analysis types selected for this session")

    if not session.name:
        session.name = build_default_session_name(session.ifc_source, analysis_types)

    if session.report_pdf_path:
        try:
            default_storage.delete(session.report_pdf_path)
        except Exception:
            pass
    session.analysis_types = analysis_types
    session.status = "running"
    session.started_at = timezone.now()
    session.completed_at = None
    session.report_pdf_path = ""
    session.report_generated_at = None
    session.celery_group_id = ""
    session.save(
        update_fields=[
            "name",
            "analysis_types",
            "status",
            "started_at",
            "completed_at",
            "report_pdf_path",
            "report_generated_at",
            "celery_group_id",
        ]
    )

    create_pending_results(session, analysis_types)

    from .tasks import run_single_analysis

    signatures = [run_single_analysis.s(str(session.id), analysis_type) for analysis_type in analysis_types]
    async_result = group(signatures).apply_async()
    session.celery_group_id = async_result.id or ""
    session.save(update_fields=["celery_group_id"])
    return session


def _derive_severity(issue_count):
    if issue_count >= 50:
        return "critical"
    if issue_count >= 10:
        return "error"
    if issue_count >= 1:
        return "warning"
    return "info"


def _extract_issue_count(results):
    if not isinstance(results, dict):
        return 0

    explicit = results.get("issue_count")
    if explicit is not None:
        try:
            return max(0, int(explicit))
        except (TypeError, ValueError):
            pass

    keys = [
        "anomalies_count",
        "potential_clashes",
        "missing_count",
        "violations_count",
    ]
    for key in keys:
        value = results.get(key)
        if value is not None:
            try:
                return max(0, int(value))
            except (TypeError, ValueError):
                continue

    list_keys = [
        "issues",
        "duplicate_global_ids",
        "missing_required_entities",
        "anomalous_types",
    ]
    for key in list_keys:
        value = results.get(key)
        if isinstance(value, list):
            return len(value)

    compliant = results.get("compliant")
    if compliant is True:
        return 0
    if compliant is False:
        return 1

    return 0


def _build_result_summary(analysis_type, results, issue_count):
    if isinstance(results, dict):
        summary = results.get("summary")
        if isinstance(summary, str) and summary.strip():
            return summary.strip()

    label = ANALYSIS_TYPE_LABELS.get(analysis_type, analysis_type.replace("_", " ").title())
    if issue_count == 0:
        return f"{label} completed without findings"
    if issue_count == 1:
        return f"{label} completed with 1 finding"
    return f"{label} completed with {issue_count} findings"


def _build_failure_result(result: AnalysisResult, message: str, started_at, status_value="failed"):
    finished_at = timezone.now()
    result.status = status_value
    result.severity = "warning" if status_value == "skipped" else "error"
    result.result_data = None
    result.summary = message
    result.issue_count = 0
    result.duration_ms = int((finished_at - started_at).total_seconds() * 1000)
    result.error_detail = None if status_value == "skipped" else {"message": message}
    result.completed_at = finished_at
    result.save(
        update_fields=[
            "status",
            "severity",
            "result_data",
            "summary",
            "issue_count",
            "duration_ms",
            "error_detail",
            "completed_at",
        ]
    )
    return result


def run_single_session_analysis(session: AnalysisSession, analysis_type: str, task_id: str = ""):
    started_at = timezone.now()
    result, _ = AnalysisResult.objects.get_or_create(
        session=session,
        analysis_type=analysis_type,
        defaults={
            "ifc_source": session.ifc_source,
            "status": "pending",
        },
    )
    result.ifc_source = session.ifc_source
    result.status = "running"
    result.severity = None
    result.error_detail = None
    result.summary = ""
    result.save(update_fields=["ifc_source", "status", "severity", "error_detail", "summary"])

    path = resolve_analysis_file_path(session.ifc_source)
    if not path or not os.path.exists(path):
        return _build_failure_result(result, "IFC source file not found", started_at)

    analyser_cls = ANALYSER_REGISTRY.get(analysis_type)
    if analyser_cls is None:
        return _build_failure_result(
            result,
            f"{analysis_type} is not implemented yet",
            started_at,
            status_value="skipped",
        )

    try:
        analyser = analyser_cls()
        results, duration_ms = analyser.execute(path)
        if isinstance(results, dict):
            results.setdefault("execution", {})
            if isinstance(results["execution"], dict):
                results["execution"].setdefault("celery_group_id", session.celery_group_id)
                results["execution"].setdefault("session_id", str(session.id))
                results["execution"].setdefault("task_id", task_id)
                results["execution"].setdefault("analysis_type", analysis_type)

        issue_count = _extract_issue_count(results)
        result.status = "done"
        result.severity = _derive_severity(issue_count)
        result.result_data = results
        result.summary = _build_result_summary(analysis_type, results, issue_count)
        result.issue_count = issue_count
        result.duration_ms = duration_ms
        result.error_detail = None
        result.completed_at = timezone.now()
        result.save(
            update_fields=[
                "status",
                "severity",
                "result_data",
                "summary",
                "issue_count",
                "duration_ms",
                "error_detail",
                "completed_at",
            ]
        )
    except Exception as exc:
        finished_at = timezone.now()
        result.status = "failed"
        result.severity = "error"
        result.result_data = None
        result.summary = f"{ANALYSIS_TYPE_LABELS.get(analysis_type, analysis_type)} failed"
        result.issue_count = 0
        result.duration_ms = int((finished_at - started_at).total_seconds() * 1000)
        result.error_detail = {"message": str(exc)}
        result.completed_at = finished_at
        result.save(
            update_fields=[
                "status",
                "severity",
                "result_data",
                "summary",
                "issue_count",
                "duration_ms",
                "error_detail",
                "completed_at",
            ]
        )

    return result


def _severity_rank(severity_value):
    order = {
        "critical": 0,
        "error": 1,
        "warning": 2,
        "info": 3,
        None: 4,
        "": 4,
    }
    return order.get(severity_value, 5)


def _build_report_scorecard(results):
    total_issues = sum((result.issue_count or 0) for result in results)
    status_counts = {"done": 0, "failed": 0, "skipped": 0}
    severity_counts = {"critical": 0, "error": 0, "warning": 0, "info": 0}

    for result in results:
        if result.status in status_counts:
            status_counts[result.status] += 1
        if result.severity in severity_counts:
            severity_counts[result.severity] += 1

    return {
        "analyses_total": len(results),
        "issues_total": total_issues,
        "status_counts": status_counts,
        "severity_counts": severity_counts,
    }


def generate_pdf_report(session: AnalysisSession):
    if HTML is None or Environment is None:
        raise RuntimeError(
            "PDF generation requires WeasyPrint and Jinja2. Install dependencies first."
        )

    generated_at = timezone.now()
    results = list(
        session.results.select_related("ifc_source").all()
    )
    results.sort(key=lambda item: (_severity_rank(item.severity), item.analysis_type))
    scorecard = _build_report_scorecard(results)

    template_dir = Path(settings.BASE_DIR) / "templates" / "analytics"
    template_env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = template_env.get_template("analysis_report.html.j2")
    html_string = template.render(
        session=session,
        results=results,
        generated_at=generated_at,
        scorecard=scorecard,
        analysis_type_labels=ANALYSIS_TYPE_LABELS,
    )
    pdf_bytes = HTML(string=html_string, base_url=str(settings.BASE_DIR)).write_pdf()

    filename = f"reports/report_{session.id}.pdf"
    if session.report_pdf_path:
        try:
            default_storage.delete(session.report_pdf_path)
        except Exception:
            pass

    saved_path = default_storage.save(filename, ContentFile(pdf_bytes))
    session.report_pdf_path = saved_path
    session.report_generated_at = generated_at
    session.save(update_fields=["report_pdf_path", "report_generated_at"])
    return saved_path


def get_report_download_url(path_value, expires_in=3600):
    if not path_value:
        return ""
    # Force signed URL generation for S3 storage even when public URL mode is enabled.
    original_querystring_auth = getattr(default_storage, "querystring_auth", None)
    try:
        if original_querystring_auth is False:
            default_storage.querystring_auth = True
        return default_storage.url(path_value, expire=expires_in)
    except TypeError:
        return default_storage.url(path_value)
    except Exception:
        return path_value
    finally:
        if original_querystring_auth is False:
            default_storage.querystring_auth = original_querystring_auth


def refresh_session_status(session: AnalysisSession):
    terminal_statuses = ["done", "failed", "skipped"]
    session = AnalysisSession.objects.prefetch_related("results").get(id=session.id)
    results = list(session.results.all())
    if not results:
        return session

    if any(result.status not in terminal_statuses for result in results):
        return session

    status_values = {result.status for result in results}
    if status_values == {"done"}:
        session.status = "done"
    elif status_values == {"failed"}:
        session.status = "failed"
    elif status_values == {"skipped"}:
        session.status = "partial"
    elif "done" in status_values and status_values.issubset({"done", "skipped"}):
        session.status = "done"
    elif "done" in status_values or "skipped" in status_values:
        session.status = "partial"
    else:
        session.status = "failed"

    session.completed_at = timezone.now()
    session.save(update_fields=["status", "completed_at"])
    return session
