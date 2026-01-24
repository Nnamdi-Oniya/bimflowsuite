from rest_framework import serializers
from .models import ComplianceCheck, RulePack
from apps.parametric_generator.serializers import GeneratedIFCSerializer


class RulePackSerializer(serializers.ModelSerializer):
    """Serializer for RulePack model."""

    class Meta:
        model = RulePack
        fields = "__all__"


class ComplianceCheckSerializer(serializers.ModelSerializer):
    """Serializer for ComplianceCheck model."""

    generated_ifc = GeneratedIFCSerializer(read_only=True)
    rule_pack = serializers.CharField(read_only=True)

    class Meta:
        model = ComplianceCheck
        fields = [
            "id",
            "generated_ifc",
            "rule_pack",
            "status",
            "results",
            "clash_results",
            "checked_at",
            "updated_at",
        ]
