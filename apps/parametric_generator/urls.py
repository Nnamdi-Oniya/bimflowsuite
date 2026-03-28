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
    # Site structure endpoint (spatial elements + assets hierarchy)
    path(
        "sites/<uuid:pk>/structure/",
        SiteViewSet.as_view(
            {
                "get": "structure",
                "patch": "structure",
            }
        ),
        name="site-structure",
    ),
    path(
        "sites/<uuid:pk>/generate-ifc/",
        SiteViewSet.as_view({"post": "generate_ifc"}),
        name="site-generate-ifc",
    ),
    # Generate/IFC endpoints
    path("generate-model/", include(generate_router.urls)),
    # Structure/Hierarchy endpoints
    path(
        "project-stucture/spatial-structures/",
        SpatialStructureViewSet.as_view({"get": "list"}),
        name="spatial-structure-list",
    ),
    path(
        "project-stucture/spatial-structures/create/",
        SpatialStructureViewSet.as_view({"post": "create"}),
        name="spatial-structure-create",
    ),
    path(
        "project-stucture/spatial-structures/<uuid:pk>/",
        SpatialStructureViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="spatial-structure-detail",
    ),
    path(
        "project-stucture/facilities/",
        FacilityViewSet.as_view({"get": "list"}),
        name="facility-list",
    ),
    path(
        "project-stucture/facilities/create/",
        FacilityViewSet.as_view({"post": "create"}),
        name="facility-create",
    ),
    path(
        "project-stucture/facilities/<uuid:pk>/",
        FacilityViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="facility-detail",
    ),
    path(
        "project-stucture/elements/",
        ElementViewSet.as_view({"get": "list"}),
        name="element-list",
    ),
    path(
        "project-stucture/elements/create/",
        ElementViewSet.as_view({"post": "create"}),
        name="element-create",
    ),
    path(
        "project-stucture/elements/<uuid:pk>/",
        ElementViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="element-detail",
    ),
    path(
        "project-stucture/facilities/",
        FacilityViewSet.as_view({"get": "list"}),
        name="facility-list",
    ),
    path(
        "project-stucture/facilities/create/",
        FacilityViewSet.as_view({"post": "create"}),
        name="facility-create",
    ),
    path(
        "project-stucture/facilities/<uuid:pk>/",
        FacilityViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="facility-detail",
    ),
]
