from django.urls import path, include
from .views import (
    LoginView,
    RequestSubmissionView,
    ActivateAccountView,
    OrganizationViewSet,
    OrganizationMemberViewSet,
    ForgotPasswordView,
    ResetPasswordView,
    ChangePasswordView,
    UserProfileView,
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
        "auth/change-password/",
        ChangePasswordView.as_view(),
        name="auth_change_password",
    ),
    path(
        "user/request-submission/",
        RequestSubmissionView.as_view(),
        name="auth_request_submission",
    ),
    path("user/profile/", UserProfileView.as_view(), name="user_profile"),
    # Organizations
    path(
        "organizations/",
        OrganizationViewSet.as_view({"get": "list", "post": "create"}),
        name="organization-list",
    ),
    path(
        "organizations/<uuid:pk>/",
        OrganizationViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="organization-detail",
    ),
    path(
        "organizations/<uuid:pk>/add_member/",
        OrganizationViewSet.as_view({"post": "add_member"}),
        name="organization-add-member",
    ),
    path(
        "organizations/<uuid:pk>/remove_member/",
        OrganizationViewSet.as_view({"post": "remove_member"}),
        name="organization-remove-member",
    ),
    # Organization members
    path(
        "organization-members/",
        OrganizationMemberViewSet.as_view({"get": "list", "post": "create"}),
        name="organization-member-list",
    ),
    path(
        "organization-members/<uuid:pk>/",
        OrganizationMemberViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="organization-member-detail",
    ),
    path(
        "organization-members/<uuid:pk>/change_role/",
        OrganizationMemberViewSet.as_view({"patch": "change_role"}),
        name="organization-member-change-role",
    ),
    path("", include("apps.parametric_generator.urls")),
    path("compliance/", include("apps.compliance_engine.urls")),
    path("analytics/", include("apps.analytics.urls")),
]
