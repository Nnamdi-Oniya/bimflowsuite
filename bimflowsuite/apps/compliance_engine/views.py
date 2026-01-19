from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ComplianceCheck, RulePack
from .rule_engine import RuleEngine
from apps.parametric_generator.models import GeneratedModel

class ComplianceCheckViewSet(viewsets.ModelViewSet):
    queryset = ComplianceCheck.objects.all()

    def get_queryset(self):
        return self.queryset.filter(model__program_spec__intent__user=self.request.user)

    @action(detail=False, methods=['post'])
    def check(self, request):  # Renamed from create
        model_id = request.data.get('model_id')
        rule_pack_name = request.data.get('rule_pack', None)
        include_clash = request.data.get('include_clash', True)

        try:
            model = GeneratedModel.objects.get(id=model_id, program_spec__intent__user=request.user)
        except GeneratedModel.DoesNotExist:
            return Response({'error': 'Model not found'}, status=status.HTTP_404_NOT_FOUND)

        if model.status != 'completed':
            return Response({'error': 'Model must be completed'}, status=status.HTTP_400_BAD_REQUEST)

        ifc_string = model.ifc_content if model.ifc_content else model.ifc_file.read().decode() if model.ifc_file else None
        if not ifc_string:
            return Response({'error': 'IFC not available'}, status=status.HTTP_400_BAD_REQUEST)

        # Use asset_type.code for default
        asset_type_code = model.asset_type.code if model.asset_type else 'building'
        rule_pack = RulePack.get_default_pack(asset_type_code) if not rule_pack_name else RulePack.objects.get(name=rule_pack_name)
        engine = RuleEngine(rule_pack.yaml_content)
        results = engine.evaluate(ifc_string, model.id, include_clash)

        return Response({'results': results, 'clashes': engine.detector.results if include_clash else {}}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def upload_rulepack(self, request):
        yaml_content = request.data.get('yaml_content')
        name = request.data.get('name')
        description = request.data.get('description', '')
        if not yaml_content or not name:
            return Response({'error': 'yaml_content and name required'}, status=status.HTTP_400_BAD_REQUEST)
        pack = RulePack.objects.create(name=name, yaml_content=yaml_content, description=description)
        return Response({'id': pack.id}, status=status.HTTP_201_CREATED)