from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from .views import (
    ProjectViewSet,
    GeneratedIFCViewSet,
    SiteViewSet,
    IsOrganizationMember,
)

generate_router = DefaultRouter()
generate_router.register(r"ifcs", GeneratedIFCViewSet, basename="generated-ifc")

app_name = "bim_projects"

urlpatterns = [
    # Project endpoints
    path(
        "projects/create/",
        ProjectViewSet.as_view(
            {"post": "create"},
            permission_classes=[permissions.IsAuthenticated, IsOrganizationMember],
        ),
        name="project-create",
    ),
    path("projects/", ProjectViewSet.as_view({"get": "list"}), name="project-list"),
    path(
        "projects/<int:pk>/",
        ProjectViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="project-detail",
    ),
    # Site endpoints
    path(
        "sites/create/",
        SiteViewSet.as_view(
            {"post": "create"},
            permission_classes=[permissions.IsAuthenticated, IsOrganizationMember],
        ),
        name="site-create",
    ),
    path("sites/", SiteViewSet.as_view({"get": "list"}), name="site-list"),
    path(
        "sites/<int:pk>/",
        SiteViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="site-detail",
    ),
    # Generate/IFC endpoints
    path("generate/", include(generate_router.urls)),
]
