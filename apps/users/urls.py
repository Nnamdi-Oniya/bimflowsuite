from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    RequestSubmissionView,
    ActivateAccountView,
    OrganizationViewSet,
    OrganizationMemberViewSet,
    ForgotPasswordView,
    ResetPasswordView,
    UserProfileView,
)

# Create router for viewsets
router = DefaultRouter()
router.register(r"organizations", OrganizationViewSet, basename="organization")
router.register(
    r"organization-members", OrganizationMemberViewSet, basename="organization-member"
)

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="auth_login"),
    path("auth/activate/", ActivateAccountView.as_view(), name="auth_activate"),
    path(
        "auth/forgot-password/",
        ForgotPasswordView.as_view(),
        name="auth_forgot_password",
    ),
    path(
        "auth/reset-password/", ResetPasswordView.as_view(), name="auth_reset_password"
    ),
    path(
        "user/request-submission/",
        RequestSubmissionView.as_view(),
        name="auth_request_submission",
    ),
    path("user/profile/", UserProfileView.as_view(), name="user_profile"),
    path("", include(router.urls)),
    path("", include("apps.parametric_generator.urls")),
    path("compliance/", include("apps.compliance_engine.urls")),
    path("analytics/", include("apps.analytics.urls")),
]
