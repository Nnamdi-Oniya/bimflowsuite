import uuid

from django.conf import settings
from django.db import models

from apps.parametric_generator.models import GeneratedIFC

from .constants import (
    ANALYSIS_TYPES,
    RESULT_STATUS_CHOICES,
    SESSION_STATUS_CHOICES,
    SEVERITY_CHOICES,
    SOURCE_CHOICES,
)


class IFCAnalysisFile(models.Model):
    """An IFC source to analyze (platform-generated or user-uploaded)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ifc_analysis_files",
    )
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    name = models.CharField(max_length=255)
    generated_ifc = models.ForeignKey(
        GeneratedIFC,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="analysis_files",
    )
    uploaded_ifc = models.FileField(
        upload_to="analytics_uploads/%Y/%m/%d/",
        null=True,
        blank=True,
    )
    file_url = models.URLField(blank=True)
    file_size_bytes = models.BigIntegerField(null=True, blank=True)
    ifc_schema = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "source_type"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.source_type})"


class AnalysisSession(models.Model):
    """One analysis run for a single IFC source."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ifc_source = models.ForeignKey(
        IFCAnalysisFile,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="analysis_sessions",
    )
    name = models.CharField(max_length=255)
    analysis_types = models.JSONField(default=list, blank=True)
    status = models.CharField(
        max_length=20,
        choices=SESSION_STATUS_CHOICES,
        default="pending",
    )
    celery_group_id = models.CharField(max_length=255, blank=True, default="")
    report_pdf_path = models.TextField(blank=True, default="")
    report_generated_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "status", "created_at"]),
            models.Index(fields=["ifc_source", "created_at"]),
            models.Index(fields=["celery_group_id"]),
        ]

    def __str__(self):
        return self.name


class AnalysisResult(models.Model):
    """One analysis result per analysis type per session."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        AnalysisSession,
        on_delete=models.CASCADE,
        related_name="results",
    )
    ifc_source = models.ForeignKey(
        IFCAnalysisFile,
        on_delete=models.CASCADE,
        related_name="results",
    )
    analysis_type = models.CharField(max_length=50, choices=ANALYSIS_TYPES)
    status = models.CharField(
        max_length=20,
        choices=RESULT_STATUS_CHOICES,
        default="pending",
    )
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        null=True,
        blank=True,
    )
    result_data = models.JSONField(blank=True, null=True)
    summary = models.TextField(blank=True)
    issue_count = models.IntegerField(default=0)
    duration_ms = models.IntegerField(blank=True, null=True)
    error_detail = models.JSONField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["analysis_type", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["session", "analysis_type"],
                name="analytics_result_session_type_unique",
            )
        ]
        indexes = [
            models.Index(fields=["ifc_source", "analysis_type", "completed_at"]),
            models.Index(fields=["session", "status"]),
        ]

    def __str__(self):
        return f"{self.analysis_type} for {self.session_id}"
