from drf_spectacular.utils import extend_schema
from django.http import FileResponse
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


class AnalysisSessionReportDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[],
        responses={200: None},
    )
    def get(self, request, id, report_type):
        """
        Download analysis report (PDF or JSON).

        report_type: "pdf" or "json"
        """
        try:
            session = AnalysisSession.objects.get(id=id, owner=request.user)
        except AnalysisSession.DoesNotExist:
            return Response(
                {"error": "Analysis session not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if report_type == "pdf":
            report_path = session.report_pdf_path
            filename = f"{session.name}_analysis.pdf"
            content_type = "application/pdf"
        elif report_type == "json":
            report_path = session.report_json_path
            filename = f"{session.name}_analysis.json"
            content_type = "application/json"
        else:
            return Response(
                {"error": "Invalid report_type. Use 'pdf' or 'json'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not report_path:
            return Response(
                {"error": "Report not yet generated. Check session status."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            from django.core.files.storage import default_storage

            file_obj = default_storage.open(report_path, "rb")
            response = FileResponse(file_obj, content_type=content_type)
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            return Response(
                {"error": f"Report file not accessible: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
