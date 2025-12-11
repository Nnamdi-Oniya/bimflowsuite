from django.contrib import admin
from .models import AnalyticsRun
from parametric_generator.models import GeneratedModel

@admin.register(AnalyticsRun)
class AnalyticsRunAdmin(admin.ModelAdmin):
    list_display = ['model', 'analytics_type', 'has_anomalies', 'created_at']
    list_filter = ['analytics_type', 'has_anomalies']
    readonly_fields = ['report_file']