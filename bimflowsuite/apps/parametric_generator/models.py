from django.db import models
from django.utils import timezone
from apps.intent_capture.models import ProgramSpec  # Safe import (no circular)
from django.contrib.auth.models import User  # For ownership
from django.core.files.base import ContentFile
import base64

class AssetType(models.Model):
    """
    Modern and scalable asset type registry.
    Stores all BIM assets dynamically.
    """
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Asset Type"
        verbose_name_plural = "Asset Types"

    def __str__(self):
        return self.name

    @staticmethod
    def load_default_assets():
        ASSET_TYPES = [
            ('building', 'Building'),
            ('bridge', 'Bridge'),
            ('road', 'Road'),
            ('highrise', 'Highrise'),
            ('tunnel', 'Tunnel'),
            ('railway', 'Railway'),
            ('metro_station', 'Metro Station'),
            ('airport_terminal', 'Airport Terminal'),
            ('solar_farm', 'Solar Farm'),
            ('wind_turbine', 'Wind Turbine'),
            ('data_center', 'Data Center'),
            ('smart_home', 'Smart Home'),
            ('industrial_plant', 'Industrial Plant'),
            ('hospital', 'Hospital'),
            ('school', 'School / University'),
            ('stadium', 'Stadium / Arena'),
            ('water_treatment', 'Water Treatment Plant'),
            ('dam', 'Dam'),
            ('harbor', 'Harbor / Port Facility'),
            ('urban_park', 'Urban Park / Landscape'),
            ('charging_station', 'EV Charging Station'),
            ('smart_tower', 'Smart Communication Tower'),
        ]

        for code, name in ASSET_TYPES:
            AssetType.objects.get_or_create(code=code, defaults={'name': name})


class GeneratedModel(models.Model):
    """
    Represents a generated IFC model linked to a ProgramSpec (from Intent Capture).
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    program_spec = models.ForeignKey(ProgramSpec, on_delete=models.CASCADE, related_name='generated_models')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_models')  # Ownership for PRD security
    asset_type = models.ForeignKey(
        AssetType, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )

    ifc_file = models.FileField(upload_to='ifc_models/%Y/%m/%d/', blank=True, null=True)
    ifc_content = models.TextField(blank=True, null=True)  # Base64 fallback

    # REMOVED scenario_version FK (future—no table error)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Generated Model"
        verbose_name_plural = "Generated Models"
        ordering = ['-created_at']

    def __str__(self):
        asset_name = self.asset_type.name if self.asset_type else "Unknown"
        intent_text = (
            self.program_spec.intent.intent_text[:30]
            if hasattr(self.program_spec, 'intent')
            else "No Intent"
        )
        return f"{asset_name} model from {intent_text} (User: {self.user.username})"

    def save_ifc_from_base64(self, base64_data: str, filename: str = "model.ifc"):
        try:
            decoded_file = base64.b64decode(base64_data)
            self.ifc_file.save(filename, ContentFile(decoded_file), save=True)
            self.ifc_content = base64_data
            self.status = 'completed'
            self.save()
        except Exception as e:
            self.status = 'failed'
            self.error_message = str(e)
            self.save()


class GenerationTask(models.Model):
    model = models.ForeignKey(GeneratedModel, on_delete=models.CASCADE, related_name='tasks')
    task_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, default='pending')
    result = models.JSONField(default=dict, blank=True, null=True)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Generation Task"
        verbose_name_plural = "Generation Tasks"
        ordering = ['-started_at']

    def __str__(self):
        return f"Task {self.task_id} for model {self.model.id}"

    def mark_completed(self, result_data=None):
        self.status = 'completed'
        self.result = result_data or {}
        self.completed_at = timezone.now()
        self.save()

    def mark_failed(self, error_message):
        self.status = 'failed'
        self.result = {'error': error_message}
        self.completed_at = timezone.now()
        self.save()