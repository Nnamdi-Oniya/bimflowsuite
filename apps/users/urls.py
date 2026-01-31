from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    RegisterView,
    RequestSubmissionView,
    ActivateAccountView,
    OrganizationViewSet,
    OrganizationMemberViewSet,
)

# Create router for viewsets
router = DefaultRouter()
router.register(r"organizations", OrganizationViewSet, basename="organization")
router.register(
    r"organization-members", OrganizationMemberViewSet, basename="organization-member"
)

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="auth_login"),
    path("auth/register/", RegisterView.as_view(), name="auth_register"),
    path("auth/activate/", ActivateAccountView.as_view(), name="auth_activate"),
    path(
        "user/request-submission/",
        RequestSubmissionView.as_view(),
        name="auth_request_submission",
    ),
    path("", include(router.urls)),  # Include viewset routes
    path("generate/", include("apps.parametric_generator.urls")),
    path("compliance/", include("apps.compliance_engine.urls")),
    path("analytics/", include("apps.analytics.urls")),
]
