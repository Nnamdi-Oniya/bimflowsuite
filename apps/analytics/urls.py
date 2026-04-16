from django.urls import path
from .views import (
    AnalysisGeneratedSourceView,
    AnalysisSessionCreateView,
    AnalysisSessionDetailView,
    AnalysisSessionReportDownloadView,
    AnalysisSourceUploadView,
)

urlpatterns = [
    path(
        "file-generated",
        AnalysisGeneratedSourceView.as_view(),
        name="analysis-source-generated",
    ),
    path(
        "sources/upload",
        AnalysisSourceUploadView.as_view(),
        name="analysis-source-upload",
    ),
    path(
        "file/<uuid:id>/sessions/create/",
        AnalysisSessionCreateView.as_view(),
        name="analysis-session-create",
    ),
    path(
        "sessions/<uuid:id>/",
        AnalysisSessionDetailView.as_view(),
        name="analysis-session-detail",
    ),
    path(
        "sessions/<uuid:id>/report/<str:report_type>/",
        AnalysisSessionReportDownloadView.as_view(),
        name="analysis-session-report-download",
    ),
]
