from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from .views import (
    ProjectViewSet,
    GeneratedIFCViewSet,
    SiteViewSet,
    SpatialStructureViewSet,
    AssetViewSet,
    IsOrganizationMember,
)

generate_router = DefaultRouter()
generate_router.register(r"ifcs", GeneratedIFCViewSet, basename="generated-ifc")

# Routers for new hierarchical structure
structure_router = DefaultRouter()
structure_router.register(
    r"spatial-structures", SpatialStructureViewSet, basename="spatial-structure"
)
structure_router.register(r"assets", AssetViewSet, basename="asset")

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
        "projects/<uuid:pk>/",
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
        "sites/<uuid:pk>/",
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
    # Site structure endpoint (spatial elements + assets hierarchy)
    path(
        "sites/<uuid:pk>/structure/",
        SiteViewSet.as_view(
            {
                "get": "structure",
                "put": "structure",
            }
        ),
        name="site-structure",
    ),
    # Generate/IFC endpoints
    path("generate-model/", include(generate_router.urls)),
    # Structure/Hierarchy endpoints
    path("project-stucture/", include(structure_router.urls)),
]
