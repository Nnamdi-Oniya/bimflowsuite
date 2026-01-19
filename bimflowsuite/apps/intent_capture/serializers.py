from rest_framework import serializers
from .models import IntentCapture, ProgramSpec
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """Nested user details."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class IntentCaptureSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested user
    class Meta:
        model = IntentCapture
        fields = ['id', 'user', 'intent_text', 'status', 'use_local_ml', 'asset_type_guess', 'created_at', 'error_message']
        read_only_fields = ['user', 'status', 'created_at', 'error_message', 'asset_type_guess']

    intent_text = serializers.CharField(
        required=True,
        help_text="Natural language BIM intent (e.g., '3-story glass building 20x15m')",
        min_length=10,
        style={'base_template': 'textarea.html'}  # FIXED: Swagger editable textarea
    )

    use_local_ml = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Use local ML fallback (slower but offline)"
    )

class ProgramSpecSerializer(serializers.ModelSerializer):
    intent_text = serializers.CharField(source='intent.intent_text', read_only=True)
    user = serializers.CharField(source='intent.user.username', read_only=True)
    
    class Meta:
        model = ProgramSpec
        fields = ['id', 'intent_text', 'user', 'json_spec', 'created_at']
        read_only_fields = ['created_at']

    json_spec = serializers.JSONField(
        required=True,
        help_text="ProgramSpec JSON (auto-generated from intent)",
        style={'base_template': 'textarea.html'}  # FIXED: Swagger editable for JSON
    )