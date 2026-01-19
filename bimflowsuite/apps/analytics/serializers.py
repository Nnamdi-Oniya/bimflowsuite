from rest_framework import serializers
from .models import AnalyticsRun

class AnalyticsRunSerializer(serializers.ModelSerializer):
    model_id = serializers.IntegerField(source='model.id', write_only=True)
    
    class Meta:
        model = AnalyticsRun
        fields = ['id', 'model_id', 'analytics_type', 'results', 'has_anomalies', 'created_at']
        read_only_fields = ['created_at', 'has_anomalies']