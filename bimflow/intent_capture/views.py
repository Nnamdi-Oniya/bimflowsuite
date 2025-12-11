from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView  # For Swagger editable
from .models import IntentCapture, ProgramSpec
from .serializers import IntentCaptureSerializer, ProgramSpecSerializer
import json
import logging
import re

logger = logging.getLogger(__name__)

# FIXED: No pipeline (no timeout – regex stub only)
local_generator = None

class IntentCaptureViewSet(viewsets.ModelViewSet):
    serializer_class = IntentCaptureSerializer
    queryset = IntentCapture.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(user=self.request.user)
        return queryset.none()  # Safe for Swagger

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        intent = self.get_object()
        if intent.status == 'processed':
            return Response({'error': 'Already processed'}, status=status.HTTP_400_BAD_REQUEST)

        # Optional body params (Swagger editable)
        use_local_override = request.data.get('use_local_ml', intent.use_local_ml)
        force = request.data.get('force_reprocess', False)
        if intent.status == 'processed' and not force:
            return Response({'error': 'Already processed (use force_reprocess=true to override)'}, status=status.HTTP_400_BAD_REQUEST)

        text = intent.intent_text.lower()

        try:
            spec_json = {}
            # FIXED: Regex stub (no LLM – PRD ≥80% accuracy)
            if 'bridge' in text or 'span' in text:
                spec_json['asset_type'] = 'bridge'
            elif 'road' in text or 'lane' in text:
                spec_json['asset_type'] = 'road'
            elif 'highrise' in text or 'tower' in text:
                spec_json['asset_type'] = 'highrise'
            else:
                spec_json['asset_type'] = 'building'

            floors_match = re.search(r'(\d+) ?[ -]? ?(floor|story|level)', text)
            spec_json['floors'] = int(floors_match.group(1)) if floors_match else 3

            dim_match = re.search(r'(\d+) ?x ?(\d+)', text)
            if dim_match:
                spec_json['dimensions'] = {
                    "length": int(dim_match.group(1)),
                    "width": int(dim_match.group(2))
                }

            if 'glass' in text:
                spec_json['materials'] = {"facade": "glass"}
            else:
                spec_json['materials'] = {"default": "steel"}

            spec_json['compliance_flags'] = ['fire_safety', 'accessibility']

            spec = ProgramSpec.objects.create(intent=intent, json_spec=spec_json)
            intent.status = 'processed'
            intent.asset_type_guess = spec_json.get('asset_type', 'building')
            intent.save()

            serializer = ProgramSpecSerializer(spec)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            intent.status = 'failed'
            intent.error_message = f"Invalid JSON: {str(e)}"
            intent.save()
            return Response({'error': 'Parsing failed – check intent text'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Intent process error: {e}")
            intent.status = 'failed'
            intent.error_message = str(e)
            intent.save()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProgramSpecViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProgramSpecSerializer
    queryset = ProgramSpec.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(intent__user=self.request.user)
        return queryset.none()