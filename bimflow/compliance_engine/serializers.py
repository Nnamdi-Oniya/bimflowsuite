from rest_framework import serializers
from .models import ComplianceCheck, RulePack
from parametric_generator.models import GeneratedModel  # For nested if needed

class GeneratedModelSerializer(serializers.ModelSerializer):
    """Nested serializer for GeneratedModel (minimal for compliance context)."""
    class Meta:
        model = GeneratedModel
        fields = ['id', 'name', 'status', 'asset_type']  # Key fields for compliance

class RulePackSerializer(serializers.ModelSerializer):
    """Serializer for RulePack model."""
    class Meta:
        model = RulePack
        fields = '__all__'  # Includes name, yaml_content, description, created_at

class ComplianceCheckSerializer(serializers.ModelSerializer):
    """Serializer for ComplianceCheck model."""
    model = GeneratedModelSerializer(read_only=True)  # Nested model details
    rule_pack = serializers.CharField(read_only=True)  # FIXED: Removed source='rule_pack' (redundant)

    class Meta:
        model = ComplianceCheck
        fields = '__all__'  # Includes model, rule_pack, status, results, clash_results, checked_at

    def create(self, validated_data):
        """Override create if needed (views handle creation)."""
        return super().create(validated_data)