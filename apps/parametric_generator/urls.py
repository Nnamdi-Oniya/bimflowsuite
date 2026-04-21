from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from .views import (
    ProjectViewSet,
    GeneratedIFCViewSet,
    SiteViewSet,
    FacilityViewSet,
    SpatialStructureViewSet,
    ElementViewSet,
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
        "projects/<uuid:pk>/",
        ProjectViewSet.as_view(
            {
                "get": "retrieve",
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
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="site-detail",
    ),
    # Generate/IFC endpoints
    path("generate-model/", include(generate_router.urls)),
    # Structure/Hierarchy endpoints (flattened)
    path(
        "spatial-structures/",
        SpatialStructureViewSet.as_view({"get": "list"}),
        name="spatial-structure-list",
    ),
    path(
        "spatial-structures/create/",
        SpatialStructureViewSet.as_view({"post": "create"}),
        name="spatial-structure-create",
    ),
    path(
        "spatial-structures/<uuid:pk>/",
        SpatialStructureViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="spatial-structure-detail",
    ),
    path(
        "facilities/",
        FacilityViewSet.as_view({"get": "list"}),
        name="facility-list",
    ),
    path(
        "facilities/create/",
        FacilityViewSet.as_view({"post": "create"}),
        name="facility-create",
    ),
    path(
        "facilities/<uuid:pk>/",
        FacilityViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="facility-detail",
    ),
    path(
        "facilities/<uuid:pk>/structure/details/",
        FacilityViewSet.as_view({"get": "structure_details"}),
        name="facility-structure-details",
    ),
    path(
        "facilities/<uuid:pk>/structure/create/",
        FacilityViewSet.as_view({"post": "structure_create"}),
        name="facility-structure-create",
    ),
    path(
        "facilities/<uuid:pk>/generate-ifc/",
        FacilityViewSet.as_view({"post": "generate_ifc"}),
        name="facility-generate-ifc",
    ),
    path(
        "elements/",
        ElementViewSet.as_view({"get": "list"}),
        name="element-list",
    ),
    path(
        "elements/create/",
        ElementViewSet.as_view({"post": "create"}),
        name="element-create",
    ),
    path(
        "elements/<uuid:pk>/",
        ElementViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="element-detail",
    ),
]
