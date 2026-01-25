from django.db import models
from apps.parametric_generator.models import GeneratedIFC
import yaml
from pathlib import Path
from django.conf import settings


class ComplianceCheck(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("passed", "Passed"),
        ("failed", "Failed"),
        ("warning", "Warning"),
    ]

    generated_ifc = models.ForeignKey(
        GeneratedIFC, on_delete=models.CASCADE, related_name="compliance_checks"
    )
    rule_pack = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    results = models.JSONField(default=list)
    clash_results = models.JSONField(default=dict, blank=True)  # Advanced clashes
    checked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-checked_at"]

    def __str__(self):
        return f"Compliance for IFC {self.generated_ifc.id} using {self.rule_pack}"


class RulePack(models.Model):
    name = models.CharField(max_length=255, unique=True)
    yaml_content = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def load_rules(self):
        return yaml.safe_load(self.yaml_content)

    @classmethod
    def get_default_pack(cls, asset_type_code):
        file_path = settings.BIMFLOW_RULEPACKS_DIR / f"default_{asset_type_code}.yaml"
        if file_path.exists():
            with open(file_path, "r") as f:
                yaml_content = f.read()
            pack, _ = cls.objects.get_or_create(
                name=f"default_{asset_type_code}",
                defaults={
                    "yaml_content": yaml_content,
                    "description": f"Default for {asset_type_code}",
                },
            )
            return pack
        return None
