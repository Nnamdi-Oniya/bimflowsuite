from drf_spectacular.utils import extend_schema
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import FileResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AnalysisSession
from .serializers import (
    AnalysisSessionCreateSerializer,
    AnalysisSessionDetailSerializer,
    AnalysisGeneratedSourceSerializer,
    AnalysisSourceSerializer,
    AnalysisSourceUploadSerializer,
)
from .services import generate_pdf_report, get_report_download_url
from .tasks import run_analysis_session


class AnalysisSourceUploadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AnalysisSourceUploadSerializer, responses=AnalysisSourceSerializer
    )
    def post(self, request):
        serializer = AnalysisSourceUploadSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        source = serializer.save()
        return Response(
            AnalysisSourceSerializer(source).data, status=status.HTTP_201_CREATED
        )


class AnalysisGeneratedSourceView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AnalysisGeneratedSourceSerializer, responses=AnalysisSourceSerializer
    )
    def post(self, request):
        serializer = AnalysisGeneratedSourceSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        source = serializer.save()
        return Response(
            AnalysisSourceSerializer(source).data, status=status.HTTP_201_CREATED
        )


class AnalysisSessionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=AnalysisSessionCreateSerializer)
    def post(self, request, id):
        serializer = AnalysisSessionCreateSerializer(
            data=request.data, context={"request": request, "source_id": id}
        )
        serializer.is_valid(raise_exception=True)
        session = serializer.save(owner=request.user, status="pending")
        run_analysis_session.delay(str(session.id))
        return Response(
            {
                "session_id": str(session.id),
                "status": "pending",
                "analysis_types": session.analysis_types,
            },
            status=status.HTTP_202_ACCEPTED,
        )


class AnalysisSessionDetailView(RetrieveAPIView):
    serializer_class = AnalysisSessionDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    queryset = AnalysisSession.objects.select_related(
        "ifc_source", "owner"
    ).prefetch_related("results")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return self.queryset.none()
        return self.queryset.filter(owner=self.request.user)


class AnalysisSessionPDFReportView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_session(self, request, id):
        try:
            return AnalysisSession.objects.get(id=id, owner=request.user)
        except AnalysisSession.DoesNotExist:
            return None

    @extend_schema(
        parameters=[],
        request=None,
        responses={
            200: {
                "type": "object",
                "properties": {"report_pdf_path": {"type": "string"}},
            },
            422: {
                "type": "object",
                "properties": {"error": {"type": "string"}},
            },
        },
    )
    def post(self, request, id):
        session = self._get_session(request, id)
        if session is None:
            return Response(
                {"error": "Analysis session not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if session.status not in {"done", "partial"}:
            return Response(
                {"error": "Report can only be generated when session status is done or partial."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        try:
            report_path = generate_pdf_report(session)
        except Exception as exc:
            return Response(
                {"error": f"Failed to generate report: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"report_pdf_path": report_path}, status=status.HTTP_200_OK)

    @extend_schema(parameters=[], responses={200: None})
    def get(self, request, id):
        session = self._get_session(request, id)
        if session is None:
            return Response(
                {"error": "Analysis session not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not session.report_pdf_path:
            return Response(
                {"error": "Report not yet generated."},
                status=status.HTTP_404_NOT_FOUND,
            )

        s3_enabled = bool(
            getattr(settings, "S3_ENABLED", getattr(settings, "USE_S3", False))
        )
        if s3_enabled:
            presigned_url = get_report_download_url(session.report_pdf_path, expires_in=3600)
            if not presigned_url:
                return Response(
                    {"error": "Report URL is unavailable."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            return redirect(presigned_url)

        try:
            file_obj = default_storage.open(session.report_pdf_path, "rb")
            response = FileResponse(file_obj, content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="report_{session.id}.pdf"'
            )
            return response
        except Exception as exc:
            return Response(
                {"error": f"Report file not accessible: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
