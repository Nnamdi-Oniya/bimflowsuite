import tempfile
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.parametric_generator.models import GeneratedIFC, Project
from apps.users.models import Organization
from apps.users.models import User

from .models import AnalysisSession, IFCAnalysisFile
from .services import sync_analysis_file_metadata


class SuccessfulAnalyser:
    def execute(self, file_path):
        return {"issues": ["alpha", "beta"], "summary": "2 findings detected"}, 12


class PassingAnalyser:
    def execute(self, file_path):
        return {"issue_count": 0, "summary": "All checks passed"}, 5


class FailingAnalyser:
    def execute(self, file_path):
        raise RuntimeError("Deliberate analyser failure")


class AnalyticsSessionAPITests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.settings_override = override_settings(
            USE_S3=False,
            MEDIA_ROOT=self.temp_dir.name,
            STORAGES={
                "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
                "staticfiles": {
                    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
                },
            },
            CELERY_TASK_ALWAYS_EAGER=True,
            CELERY_TASK_EAGER_PROPAGATES=True,
            CELERY_TASK_STORE_EAGER_RESULT=False,
            CELERY_IGNORE_RESULT=True,
            CELERY_BROKER_URL="memory://",
            CELERY_RESULT_BACKEND="cache+memory://",
        )
        self.settings_override.enable()

        self.user = User.objects.create_user(
            username="analytics-user",
            email="analytics@example.com",
            password="secret123",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.organization = Organization.objects.create(
            name="Test Org",
            slug="test-org",
            owner=self.user,
        )
        self.project = Project.objects.create(
            organization=self.organization,
            user=self.user,
            name="Test Project",
            project_number="PRJ-001",
        )
        self.generated_ifc = GeneratedIFC.objects.create(
            project=self.project,
            name="Server IFC",
            asset_type="building",
            ifc_schema_version="ifc4",
            status="completed",
            specifications={},
            ifc_file=SimpleUploadedFile(
                "server.ifc",
                b"ISO-10303-21; ENDSEC; END-ISO-10303-21;",
                content_type="application/octet-stream",
            ),
        )

        self.ifc_source = IFCAnalysisFile.objects.create(
            owner=self.user,
            source_type="uploaded",
            name="Sample IFC",
            uploaded_ifc=SimpleUploadedFile(
                "sample.ifc",
                b"ISO-10303-21; ENDSEC; END-ISO-10303-21;",
                content_type="application/octet-stream",
            ),
        )
        sync_analysis_file_metadata(self.ifc_source)
        self.ifc_source.save(update_fields=["name", "file_url", "file_size_bytes", "ifc_schema"])

    def tearDown(self):
        self.settings_override.disable()
        self.temp_dir.cleanup()

    def test_upload_source_uses_contract_endpoint_and_shape(self):
        response = self.client.post(
            "/api/analysis/sources/upload",
            {
                "source_type": "uploaded",
                "file": SimpleUploadedFile(
                    "house_a.ifc",
                    b"ISO-10303-21; ENDSEC; END-ISO-10303-21;",
                    content_type="application/octet-stream",
                ),
                "name": "House A",
            },
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertIn("source_id", response.data)
        self.assertEqual(response.data["source_type"], "uploaded")
        self.assertEqual(response.data["name"], "House A")
        self.assertIn("file_size_bytes", response.data)

    def test_generated_source_uses_existing_server_file_id(self):
        response = self.client.post(
            "/api/analysis/sources/generated",
            {
                "generated_ifc_id": str(self.generated_ifc.id),
                "name": "Existing Server IFC",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["source_type"], "generated")
        self.assertEqual(response.data["generated_ifc_id"], str(self.generated_ifc.id))
        self.assertEqual(response.data["name"], "Existing Server IFC")
        source = IFCAnalysisFile.objects.get(id=response.data["source_id"])
        self.assertEqual(source.generated_ifc_id, self.generated_ifc.id)
        self.assertEqual(source.owner_id, self.user.id)

    @patch("apps.analytics.views.run_analysis_session.delay")
    def test_create_session_queues_orchestrator_task(self, delay_mock):
        response = self.client.post(
            "/api/analysis/sessions/create/",
            {
                "source_id": str(self.ifc_source.id),
                "name": "Queued run",
                "analysis_types": ["clash_detection", "code_compliance"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 202, response.data)
        session = AnalysisSession.objects.get(id=response.data["session_id"])
        self.assertEqual(session.status, "pending")
        self.assertEqual(session.analysis_types, ["clash_detection", "code_compliance"])
        self.assertFalse(session.results.exists())
        delay_mock.assert_called_once_with(str(session.id))

    @patch(
        "apps.analytics.services.ANALYSER_REGISTRY",
        {
            "clash_detection": SuccessfulAnalyser,
            "code_compliance": PassingAnalyser,
        },
    )
    def test_create_session_runs_requested_analyses_and_generates_reports(self):
        response = self.client.post(
            "/api/analysis/sessions/create/",
            {
                "source_id": str(self.ifc_source.id),
                "name": "Coordination run",
                "analysis_types": ["clash_detection", "code_compliance"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 202, response.data)
        self.assertEqual(response.data["status"], "pending")
        self.assertEqual(response.data["analysis_types"], ["clash_detection", "code_compliance"])

        session = AnalysisSession.objects.prefetch_related("results").get(id=response.data["session_id"])
        self.assertEqual(session.owner_id, self.user.id)
        self.assertEqual(session.ifc_source_id, self.ifc_source.id)
        self.assertEqual(session.status, "done")
        self.assertTrue(session.celery_group_id)
        self.assertTrue(session.report_pdf_path)
        self.assertTrue(session.report_json_path)
        self.assertIsNotNone(session.report_generated_at)

        results = list(session.results.order_by("analysis_type"))
        self.assertEqual(len(results), 2)
        self.assertEqual(
            [result.analysis_type for result in results],
            ["clash_detection", "code_compliance"],
        )
        self.assertTrue(all(result.status == "done" for result in results))
        self.assertEqual(results[0].issue_count, 2)
        self.assertEqual(results[0].severity, "warning")
        self.assertEqual(results[1].issue_count, 0)
        self.assertEqual(results[1].severity, "info")

        detail_response = self.client.get(f"/api/analysis/sessions/{session.id}/")
        self.assertEqual(detail_response.status_code, 200, detail_response.data)
        self.assertEqual(detail_response.data["id"], str(session.id))
        self.assertEqual(detail_response.data["name"], "Coordination run")
        self.assertEqual(detail_response.data["status"], "done")
        self.assertEqual(detail_response.data["source_name"], self.ifc_source.name)
        self.assertEqual(detail_response.data["source_type"], "uploaded")
        self.assertEqual(detail_response.data["total_issues"], 2)
        self.assertEqual(len(detail_response.data["results"]), 2)

    @patch(
        "apps.analytics.services.ANALYSER_REGISTRY",
        {
            "clash_detection": SuccessfulAnalyser,
            "code_compliance": FailingAnalyser,
        },
    )
    def test_create_session_marks_partial_when_some_results_fail(self):
        response = self.client.post(
            "/api/analysis/sessions/create/",
            {
                "source_id": str(self.ifc_source.id),
                "analysis_types": ["clash_detection", "code_compliance"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 202, response.data)

        session = AnalysisSession.objects.prefetch_related("results").get(id=response.data["session_id"])
        self.assertEqual(session.status, "partial")
        self.assertTrue(session.report_pdf_path)
        self.assertTrue(session.report_json_path)

        results = {result.analysis_type: result for result in session.results.all()}
        self.assertEqual(results["clash_detection"].status, "done")
        self.assertEqual(results["code_compliance"].status, "failed")
        self.assertEqual(results["code_compliance"].severity, "error")
        self.assertEqual(
            results["code_compliance"].error_detail,
            {"message": "Deliberate analyser failure"},
        )

    @patch(
        "apps.analytics.services.ANALYSER_REGISTRY",
        {
            "clash_detection": SuccessfulAnalyser,
        },
    )
    def test_create_session_defaults_to_all_configured_analysis_types(self):
        response = self.client.post(
            "/api/analysis/sessions/create/",
            {
                "source_id": str(self.ifc_source.id),
            },
            format="json",
        )

        self.assertEqual(response.status_code, 202, response.data)
        session = AnalysisSession.objects.get(id=response.data["session_id"])
        self.assertEqual(session.analysis_types, response.data["analysis_types"])
        self.assertGreater(len(session.analysis_types), 0)
