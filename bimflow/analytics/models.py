from django.db import models
from parametric_generator.models import GeneratedModel
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

class AnalyticsRun(models.Model):
    ANALYTICS_TYPES = [
        ('qto', 'Quantity Takeoff'),
        ('cost_estimate', 'Cost Estimation'),
        ('schedule', 'Schedule'),
        ('anomaly_detection', 'Anomaly Detection'),
    ]
    
    model = models.ForeignKey(GeneratedModel, on_delete=models.CASCADE)
    analytics_type = models.CharField(max_length=20, choices=ANALYTICS_TYPES)
    results = models.JSONField(default=dict)
    report_file = models.FileField(upload_to='analytics_reports/%Y/%m/%d/', blank=True, null=True)
    has_anomalies = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.analytics_type} for {self.model}"

    def generate_report(self):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, f"{self.analytics_type.upper()} Report")
        y = 700
        data = self.results
        if self.analytics_type == 'qto':
            for item, qty in data.get('quantities', {}).items():
                c.drawString(100, y, f"{item}: {qty}")
                y -= 20
        c.save()
        buffer.seek(0)
        self.report_file.save(f"{self.id}.pdf", buffer)