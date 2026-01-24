from django.db import models
from apps.parametric_generator.models import GeneratedIFC
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


class AnalyticsRun(models.Model):
    ANALYTICS_TYPES = [
        ("qto", "Quantity Takeoff"),
        ("cost_estimate", "Cost Estimation"),
        ("schedule", "Schedule"),
        ("anomaly_detection", "Anomaly Detection"),
    ]

    generated_ifc = models.ForeignKey(
        GeneratedIFC, on_delete=models.CASCADE, related_name="analytics_runs"
    )
    analytics_type = models.CharField(max_length=20, choices=ANALYTICS_TYPES)
    results = models.JSONField(default=dict)
    report_file = models.FileField(
        upload_to="analytics_reports/%Y/%m/%d/", blank=True, null=True
    )
    has_anomalies = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.analytics_type} for {self.generated_ifc}"

    def generate_report(self):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)

    def generate_report(self):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, f"{self.analytics_type.upper()} Report")
        c.drawString(100, 730, f"IFC: {self.generated_ifc.id}")
        c.drawString(100, 710, f"Asset Type: {self.generated_ifc.asset_type}")
        y = 680
        data = self.results
        if self.analytics_type == "qto":
            for item, qty in data.get("quantities", {}).items():
                c.drawString(100, y, f"{item}: {qty}")
                y -= 20
        c.save()
        buffer.seek(0)
        self.report_file.save(f"{self.id}.pdf", buffer)

        if self.analytics_type == "qto":
            for item, qty in data.get("quantities", {}).items():
                c.drawString(100, y, f"{item}: {qty}")
                y -= 20
        c.save()
        buffer.seek(0)
        self.report_file.save(f"{self.id}.pdf", buffer)
