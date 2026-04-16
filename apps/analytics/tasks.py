from celery import shared_task

from .models import AnalysisSession
from .services import launch_analysis_session, refresh_session_status, run_single_session_analysis


@shared_task(bind=True)
def run_single_analysis(self, session_id: str, analysis_type: str):
    try:
        session = AnalysisSession.objects.select_related("ifc_source").get(id=session_id)
    except AnalysisSession.DoesNotExist:
        return {"status": "not_found", "session_id": session_id, "analysis_type": analysis_type}

    result = run_single_session_analysis(
        session=session,
        analysis_type=analysis_type,
        task_id=self.request.id or "",
    )
    refresh_session_status(session)
    return {
        "status": result.status,
        "session_id": str(session.id),
        "analysis_type": analysis_type,
        "result_id": str(result.id),
    }


@shared_task(bind=True)
def run_analysis_session(self, session_id: str):
    try:
        session = AnalysisSession.objects.select_related("ifc_source").get(id=session_id)
    except AnalysisSession.DoesNotExist:
        return {"status": "not_found", "session_id": session_id}

    if session.celery_group_id and session.status == "running":
        return {
            "status": session.status,
            "session_id": str(session.id),
            "celery_group_id": session.celery_group_id,
        }

    session = launch_analysis_session(session)
    return {
        "status": session.status,
        "session_id": str(session.id),
        "celery_group_id": session.celery_group_id,
        "analysis_count": len(session.analysis_types),
    }
