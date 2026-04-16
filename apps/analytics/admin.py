from django.contrib import admin

from .models import AnalysisResult, AnalysisSession, IFCAnalysisFile


@admin.register(IFCAnalysisFile)
class IFCAnalysisFileAdmin(admin.ModelAdmin):
    list_display = ["id", "owner", "name", "source_type", "generated_ifc", "created_at"]
    list_filter = ["source_type", "created_at"]
    search_fields = ["name", "owner__email", "owner__username"]


@admin.register(AnalysisSession)
class AnalysisSessionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "status", "ifc_source", "owner", "created_at"]
    list_filter = ["status", "created_at", "report_generated_at"]
    search_fields = ["name", "owner__email", "ifc_source__name"]
    readonly_fields = [
        "started_at",
        "completed_at",
        "report_generated_at",
        "report_pdf_path",
        "report_json_path",
        "celery_group_id",
    ]


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "ifc_source",
        "session",
        "analysis_type",
        "status",
        "severity",
        "issue_count",
        "completed_at",
    ]
    list_filter = ["analysis_type", "status", "severity", "completed_at"]
    readonly_fields = ["result_data", "error_detail", "completed_at", "duration_ms"]
