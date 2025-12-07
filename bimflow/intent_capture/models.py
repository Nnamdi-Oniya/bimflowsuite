from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class IntentCapture(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    intent_text = models.TextField(help_text="Natural language description of BIM intent")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    use_local_ml = models.BooleanField(default=False, help_text="Fallback to local HuggingFace")
    asset_type_guess = models.CharField(max_length=50, blank=True, null=True, help_text="Auto-inferred asset type (building/bridge/road)")
    created_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),  # PRD Perf: Fast user queries
            models.Index(fields=['created_at']),
        ]

    def clean(self):
        if len(self.intent_text) < 10:
            raise ValidationError("Intent text too short (min 10 chars).")

    def save(self, *args, **kwargs):
        if self.status == 'pending' and not self.asset_type_guess:
            self.guess_asset_type()
        super().save(*args, **kwargs)

    def guess_asset_type(self):
        text = self.intent_text.lower()
        if 'bridge' in text or 'span' in text:
            self.asset_type_guess = 'bridge'
        elif 'road' in text or 'lane' in text:
            self.asset_type_guess = 'road'
        elif 'highrise' in text or 'tower' in text:
            self.asset_type_guess = 'highrise'
        else:
            self.asset_type_guess = 'building'

    def __str__(self):
        return f"Intent: {self.intent_text[:50]}... by {self.user.username}"

class ProgramSpec(models.Model):
    intent = models.OneToOneField(IntentCapture, on_delete=models.CASCADE, related_name='program_spec')
    json_spec = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self): 
        # FIXED: Validation in clean() (no lambda in migrations)
        if not isinstance(self.json_spec, dict) or not self.json_spec.get('asset_type'):
            raise ValidationError("json_spec must be dict with 'asset_type' key (e.g., 'building').")

    def __str__(self):
        return f"Spec for {self.intent.intent_text[:50]}..."

    def get_spec_as_dict(self):
        return self.json_spec