from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # Enforce auth
from .models import GeneratedModel, AssetType
from .serializers import GeneratedModelSerializer
from apps.intent_capture.models import ProgramSpec
import json
import base64
import logging  # For errors
from django.http import HttpResponse
import importlib  # For dynamic generator imports

logger = logging.getLogger(__name__)

class GeneratedModelViewSet(viewsets.ModelViewSet):
    serializer_class = GeneratedModelSerializer
    queryset = GeneratedModel.objects.all()
    permission_classes = [IsAuthenticated]  # PRD security

    def get_queryset(self):
        # User-specific filtering
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Auto-set user on create (for default create too)
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='generate')  # Explicit path for Swagger
    def generate(self, request):
        program_spec_id = request.data.get('program_spec_id')
        scenario_id = request.data.get('scenario_id', None)
        
        if not program_spec_id:
            return Response({'error': 'program_spec_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            program_spec = ProgramSpec.objects.get(id=program_spec_id, intent__user=request.user)
        except ProgramSpec.DoesNotExist:
            return Response({'error': 'ProgramSpec not found or access denied'}, status=status.HTTP_404_NOT_FOUND)

        # Fallback if get_spec_as_dict() missing; assume json_spec or spec_data is JSONField
        spec_json = getattr(program_spec, 'get_spec_as_dict', lambda: program_spec.json_spec)()
        spec_json = spec_json or {}  # Ensure dict
        asset_type_code = spec_json.get('asset_type', 'building')
        if not asset_type_code:
            return Response({'error': 'asset_type required in ProgramSpec'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate AssetType
        try:
            asset_type = AssetType.objects.get(code=asset_type_code)
        except AssetType.DoesNotExist:
            return Response({'error': f'Invalid asset_type: {asset_type_code}'}, status=status.HTTP_400_BAD_REQUEST)

        # Create model (status=pending initially)
        model = GeneratedModel.objects.create(
            program_spec=program_spec,
            asset_type=asset_type,
            user=request.user,
            status='generating'  # Start as generating (Celery would async here)
        )

        try:
            # Dynamic dispatch to generator (try custom, fallback generic)
            ifc_str = None
            try:
                # Try custom import/dispatch for Phase 1 assets
                if asset_type_code == 'bridge':
                    from .generators.bridge import generate_bridge_ifc
                    ifc_str = generate_bridge_ifc(spec_json)
                elif asset_type_code == 'building':
                    from .generators.building import generate_building_ifc
                    ifc_str = generate_building_ifc(spec_json)
                elif asset_type_code == 'road':
                    from .generators.road import generate_road_ifc
                    ifc_str = generate_road_ifc(spec_json)
                elif asset_type_code == 'highrise':
                    from .generators.highrise import generate_highrise_ifc
                    ifc_str = generate_highrise_ifc(spec_json)
                else:
                    # Generic fallback
                    from .generators.generic import generate_generic_ifc
                    ifc_str = generate_generic_ifc(spec_json, asset_type_code)
            except ImportError as ie:
                logger.warning(f"Custom generator missing for {asset_type_code}: {ie}. Using generic.")
                from .generators.generic import generate_generic_ifc
                ifc_str = generate_generic_ifc(spec_json, asset_type_code)
            
            if not ifc_str:
                raise ValueError("Generator returned empty IFC string")
            
            # Encode to base64
            ifc_b64 = base64.b64encode(ifc_str.encode('utf-8')).decode('utf-8')
            model.save_ifc_from_base64(ifc_b64, f"{model.id}.ifc")
            
            # Skip scenario handling for now (add back when core app ready)
            # if scenario_id:
            #     try:
            #         from bimflow.core.scenario_manager.models import ScenarioVersion
            #         scenario_version = ScenarioVersion.objects.get(id=scenario_id, user=request.user)
            #         model.scenario_version = scenario_version
            #         model.save()
            #     except Exception as se:
            #         logger.warning(f"Scenario {scenario_id} failed: {se}")
            
            model.status = 'completed'  # Update after success
            model.save(update_fields=['status'])
            
        except Exception as e:
            model.status = 'failed'
            model.error_message = str(e)
            model.save(update_fields=['status', 'error_message'])
            logger.error(f"IFC generation failed for model {model.id}: {e}")
            return Response({'error': 'Generation failed', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = GeneratedModelSerializer(model)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='download_ifc')
    def download_ifc(self, request, pk=None):
        model = self.get_object()
        if model.status != 'completed':
            return Response({'error': 'Model not ready'}, status=status.HTTP_400_BAD_REQUEST)

        if model.ifc_content:
            ifc_data = base64.b64decode(model.ifc_content)
        elif model.ifc_file:
            with model.ifc_file.open('rb') as f:
                ifc_data = f.read()
        else:
            return Response({'error': 'IFC not available'}, status=status.HTTP_404_NOT_FOUND)

        response = HttpResponse(ifc_data, content_type='application/x-ifc')
        response['Content-Disposition'] = f'attachment; filename="{pk}.ifc"'
        return response