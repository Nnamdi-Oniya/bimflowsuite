from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ComplianceCheck, RulePack
from .serializers import ComplianceCheckSerializer
from .rule_engine import RuleEngine
from apps.parametric_generator.models import GeneratedIFC
from apps.users.models import OrganizationMember
import logging

logger = logging.getLogger(__name__)


class ComplianceCheckViewSet(viewsets.ModelViewSet):
    queryset = ComplianceCheck.objects.all()
    serializer_class = ComplianceCheckSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only compliance checks for projects in user's organizations"""
        if getattr(self, "swagger_fake_view", False):
            return self.queryset.none()
        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user, is_active=True
        ).values_list("organization", flat=True)
        return self.queryset.filter(
            generated_ifc__project__organization__in=user_organizations
        )

    @action(detail=False, methods=["post"])
    def evaluate_ifc(self, request):
        ifc_id = request.data.get("ifc_id")
        rule_pack_name = request.data.get("rule_pack", None)
        include_clash = request.data.get("include_clash", True)
        tolerance_hard = request.data.get("tolerance_hard", 0.01)  # meters
        tolerance_soft = request.data.get("tolerance_soft", 0.05)  # meters

        if not ifc_id:
            return Response(
                {"error": "ifc_id required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verify user has access to this IFC through organization membership
            generated_ifc = GeneratedIFC.objects.get(id=ifc_id)

            # Check organization membership
            if not OrganizationMember.objects.filter(
                user=request.user,
                organization=generated_ifc.project.organization,
                is_active=True,
            ).exists():
                return Response(
                    {"error": "IFC not found or access denied"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except GeneratedIFC.DoesNotExist:
            return Response(
                {"error": "IFC not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if generated_ifc.status != "completed":
            return Response(
                {"error": f"IFC must be completed (current: {generated_ifc.status})"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get IFC content
        if not generated_ifc.ifc_file:
            return Response(
                {"error": "IFC file not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ifc_string = (
            generated_ifc.ifc_file.read().decode()
            if hasattr(generated_ifc.ifc_file, "read")
            else str(generated_ifc.ifc_file)
        )

        try:
            # Use asset_type for default
            asset_type_code = generated_ifc.asset_type

            if rule_pack_name:
                rule_pack = RulePack.objects.get(name=rule_pack_name)
            else:
                rule_pack = RulePack.get_default_pack(asset_type_code)

            if not rule_pack:
                return Response(
                    {"error": f"No rule pack found for {asset_type_code}"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Initialize engine with custom tolerances
            engine = RuleEngine(
                rule_pack.yaml_content,
                tolerance_hard=tolerance_hard,
                tolerance_soft=tolerance_soft,
            )
            results = engine.evaluate(ifc_string, generated_ifc.id, include_clash)

            # Get latest check for response
            check = ComplianceCheck.objects.filter(
                generated_ifc_id=generated_ifc.id
            ).latest("checked_at")

            return Response(
                {
                    "check_id": check.id,
                    "ifc_id": generated_ifc.id,
                    "status": check.status,
                    "results": check.results,
                    "clash_results": check.clash_results if include_clash else {},
                    "tolerances": {"hard": tolerance_hard, "soft": tolerance_soft},
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Compliance check failed: {e}", exc_info=True)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def upload_rulepack(self, request):
        """Upload custom rule pack."""
        yaml_content = request.data.get("yaml_content")
        name = request.data.get("name")
        description = request.data.get("description", "")

        if not yaml_content or not name:
            return Response(
                {"error": "yaml_content and name required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate YAML
        try:
            import yaml

            yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            return Response(
                {"error": f"Invalid YAML: {e}"}, status=status.HTTP_400_BAD_REQUEST
            )

        pack = RulePack.objects.create(
            name=name, yaml_content=yaml_content, description=description
        )
        return Response(
            {"id": pack.id, "name": pack.name}, status=status.HTTP_201_CREATED
        )
