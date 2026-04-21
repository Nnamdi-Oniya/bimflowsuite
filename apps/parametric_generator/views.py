from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
from django.db import transaction
import logging
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from .models import (
    Project,
    GeneratedIFC,
    Site,
    Facility,
    Material,
    SpatialStructure,
    Element,
)
from .serializers import (
    ProjectSerializer,
    ProjectDetailSerializer,
    GeneratedIFCSerializer,
    SiteSerializer,
    FacilitySerializer,
    MaterialSerializer,
    SpatialStructureSerializer,
    ElementSerializer,
    SiteStructureSerializer,
    FacilityStructureCreateSerializer,
)
from .tasks import generate_ifc_for_site
from apps.users.models import OrganizationMember

logger = logging.getLogger(__name__)


class IsOrganizationMember(permissions.BasePermission):
    """Permission check: user must be a member of the organization"""

    @staticmethod
    def _extract_organization(obj):
        """Resolve organization from supported object types."""
        if hasattr(obj, "organization"):
            return obj.organization

        if hasattr(obj, "project"):
            project = obj.project
            if hasattr(project, "organization"):
                return project.organization

        if hasattr(obj, "site"):
            site = obj.site
            if hasattr(site, "project") and hasattr(site.project, "organization"):
                return site.project.organization

        return None

    def has_object_permission(self, request, view, obj):
        organization = self._extract_organization(obj)
        if organization is None:
            return False

        return OrganizationMember.objects.filter(
            organization=organization, user=request.user, is_active=True
        ).exists()


class ProjectViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for BIM projects (organization-based access)"""

    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]
    serializer_class = ProjectSerializer
    filterset_fields = ["phase", "organization", "approval_status"]
    search_fields = ["name", "project_number", "description"]
    ordering_fields = ["created_at", "updated_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Return only projects from organizations the user is a member of"""
        if getattr(self, "swagger_fake_view", False):
            return Project.objects.none()
        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user, is_active=True
        ).values_list("organization", flat=True)
        return Project.objects.filter(organization__in=user_organizations)

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == "retrieve":
            return ProjectDetailSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        """Create new project (auto-injects organization from user's membership)"""

        # Get user's organization (user can only belong to one organization at a time)
        org_member = (
            OrganizationMember.objects.filter(user=request.user, is_active=True)
            .select_related("organization")
            .first()
        )

        if not org_member:
            return Response(
                {"error": "You are not a member of any organization"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not org_member.can_edit_projects:
            return Response(
                {
                    "error": "You don't have permission to create projects in your organization"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Add organization to request data
        data = (
            request.data.copy() if hasattr(request.data, "copy") else dict(request.data)
        )
        data["organization"] = org_member.organization.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        """Set user to current request user when saving"""
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Delete project (requires can_delete_projects permission)"""
        instance = self.get_object()

        # Check delete permission
        member = OrganizationMember.objects.get(
            organization=instance.organization, user=request.user
        )
        if not member.can_delete_projects:
            raise PermissionDenied("You don't have permission to delete projects")

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GeneratedIFCViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only endpoints for generated IFC files"""

    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]
    serializer_class = GeneratedIFCSerializer
    filterset_fields = ["project", "asset_type", "status"]
    ordering_fields = ["created_at", "completed_at"]
    ordering = ["-created_at"]
    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        """Return only IFCs from projects in user's organizations"""
        if getattr(self, "swagger_fake_view", False):
            return GeneratedIFC.objects.none()
        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user, is_active=True
        ).values_list("organization", flat=True)
        return GeneratedIFC.objects.filter(project__organization__in=user_organizations)

    def check_object_permissions(self, request, obj):
        """Check permissions on GeneratedIFC's parent project"""
        super().check_object_permissions(request, obj)
        # Verify user is member of the project's organization
        if not OrganizationMember.objects.filter(
            organization=obj.project.organization, user=request.user, is_active=True
        ).exists():
            self.permission_denied(request)

    @action(
        detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def download(self, request, pk=None):
        """Download IFC file"""
        ifc = self.get_object()
        self.check_object_permissions(request, ifc)

        if not ifc.ifc_file:
            return Response(
                {"error": "IFC file not available"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Log download
        logger.info(
            f"IFC download: {ifc.id} by user {request.user.id} from project {ifc.project.id}"
        )

        return Response(
            {
                "download_url": ifc.ifc_file.url,
                "filename": ifc.ifc_file.name,
                "file_size": ifc.file_size,
                "asset_type": ifc.get_asset_type_display(),
            }
        )


class SiteViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for Sites within projects (organization-based access)"""

    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]
    serializer_class = SiteSerializer
    filterset_fields = ["project", "coordinate_reference_system"]
    search_fields = ["site_name", "address"]
    ordering_fields = ["created_at", "updated_at", "site_name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Return only sites from projects in organizations the user is a member of"""
        if getattr(self, "swagger_fake_view", False):
            return Site.objects.none()
        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user, is_active=True
        ).values_list("organization", flat=True)
        return Site.objects.filter(project__organization__in=user_organizations)

    def create(self, request, *args, **kwargs):
        """Create new site for an existing project"""
        project_id = request.data.get("project")

        if not project_id:
            return Response(
                {"error": "project is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the project and verify user has access
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if user is member of project's organization
        if not OrganizationMember.objects.filter(
            organization=project.organization, user=request.user, is_active=True
        ).exists():
            raise PermissionDenied(
                "You don't have permission to create sites for this project"
            )

        # Check if user has edit_projects permission
        member = OrganizationMember.objects.get(
            organization=project.organization, user=request.user
        )
        if not member.can_edit_projects:
            raise PermissionDenied(
                "You don't have permission to create sites in this organization"
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_update(self, serializer):
        """Update site with permission checks"""
        site = self.get_object()

        # Verify user can edit projects in this organization
        member = OrganizationMember.objects.get(
            organization=site.project.organization, user=self.request.user
        )
        if not member.can_edit_projects:
            raise PermissionDenied(
                "You don't have permission to edit sites in this organization"
            )

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Delete site (requires can_edit_projects or can_delete_projects permission)"""
        site = self.get_object()

        # Check permissions
        member = OrganizationMember.objects.get(
            organization=site.project.organization, user=request.user
        )
        if not member.can_delete_projects and not member.can_edit_projects:
            raise PermissionDenied("You don't have permission to delete sites")

        self.perform_destroy(site)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get", "patch"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def structure(self, request, pk=None):
        """
        GET: Retrieve complete spatial structure and assets for a site
        PUT: Update spatial structure and assets for a site
        """
        site = self.get_object()

        # Verify user can access this site
        self.check_object_permissions(request, site)

        if request.method == "GET":
            serializer = SiteStructureSerializer(site, context={"request": request})
            return Response(serializer.data)

        elif request.method == "PATCH":
            # Verify user has edit permission
            member = OrganizationMember.objects.get(
                organization=site.project.organization, user=request.user
            )
            if not member.can_edit_projects:
                raise PermissionDenied(
                    "You don't have permission to edit sites in this organization"
                )

            data = request.data
            errors = []

            try:
                # Process spatial structures (hierarchical structure)
                spatial_structures_data = data.get("spatial_structures", [])
                site.spatial_structures.all().delete()  # Clear existing

                # Recursively create spatial structures
                for struct_data in spatial_structures_data:
                    self._create_spatial_structure(site, struct_data, parent=None)

                # Process assets
                assets_data = data.get("assets", [])
                site.assets.all().delete()  # Clear existing

                for asset_data in assets_data:
                    self._create_asset(site, asset_data)

                # Return updated structure
                serializer = SiteStructureSerializer(site, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {"error": f"Failed to update structure: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    # legacy site structure action kept for admin use only (no public route)

    def _create_spatial_structure(self, site, data, parent=None):
        """Recursively create spatial structure with children"""
        children_data = data.pop("children", [])

        spatial_struct = SpatialStructure.objects.create(
            site=site,
            parent=parent,
            spatial_type=data.get("spatial_type"),
            name=data.get("name"),
            description=data.get("description", ""),
            order_in_parent=data.get("order_in_parent", 0),
            properties=data.get("properties", {}),
            level=(parent.level + 1) if parent else 0,
        )

        # Recursively create children
        for child_data in children_data:
            self._create_spatial_structure(site, child_data, parent=spatial_struct)

        return spatial_struct

    def _create_asset(self, site, data):
        """Create element linked to a spatial structure"""
        spatial_structure_id = data.get("spatial_structure_id")
        try:
            spatial_structure = SpatialStructure.objects.get(
                id=spatial_structure_id, site=site
            )
        except SpatialStructure.DoesNotExist:
            raise ValueError(
                f"Spatial structure {spatial_structure_id} not found in this site"
            )

        Element.objects.create(
            spatial_structure=spatial_structure,
            site=site,
            asset_type=data.get("asset_type"),
            name=data.get("name"),
            description=data.get("description", ""),
            properties=data.get("properties", {}),
        )


class SpatialStructureViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for spatial structures (hierarchical organization)"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SpatialStructureSerializer
    filterset_fields = ["site", "spatial_type", "parent"]
    search_fields = ["name", "description"]
    ordering = ["level", "order_in_parent"]

    def get_queryset(self):
        """Return spatial structures from sites user can access"""
        if getattr(self, "swagger_fake_view", False):
            return SpatialStructure.objects.none()

        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user, is_active=True
        ).values_list("organization", flat=True)

        return SpatialStructure.objects.filter(
            site__project__organization__in=user_organizations
        )

    def create(self, request, *args, **kwargs):
        """
        Create spatial structure(s).

        Supports:
        - Single-node create (existing behavior)
        - Nested tree create in one request when `children` is provided
        """
        payload = request.data
        if not isinstance(payload, dict):
            raise ValidationError("Invalid payload format")

        # Keep default DRF behavior for legacy single-node requests.
        if "children" not in payload:
            return super().create(request, *args, **kwargs)

        site_id = payload.get("site")
        if not site_id:
            raise ValidationError({"site": "site is required"})

        site = get_object_or_404(Site, id=site_id)
        self._ensure_can_edit_site(site)

        parent = None
        parent_id = payload.get("parent")
        if parent_id:
            parent = get_object_or_404(SpatialStructure, id=parent_id, site=site)

        with transaction.atomic():
            root_structure = self._create_structure_tree(site, payload, parent=parent)

        serializer = self.get_serializer(root_structure, context={"request": request})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """Verify user can edit the site"""
        site = serializer.validated_data["site"]
        self._ensure_can_edit_site(site)
        serializer.save()

    def perform_update(self, serializer):
        """Verify user can edit the site"""
        spatial_structure = self.get_object()
        self._ensure_can_edit_site(spatial_structure.site)
        serializer.save()

    def perform_destroy(self, instance):
        """Verify user can edit the site"""
        try:
            member = OrganizationMember.objects.get(
                organization=instance.site.project.organization,
                user=self.request.user,
                is_active=True,
            )
        except OrganizationMember.DoesNotExist:
            raise PermissionDenied("You don't have permission to delete this site")
        if not member.can_delete_projects:
            raise PermissionDenied(
                "You don't have permission to delete structures from this site"
            )

        instance.delete()

    def _ensure_can_edit_site(self, site):
        """Check organization membership and edit permission for a site."""
        try:
            member = OrganizationMember.objects.get(
                organization=site.project.organization,
                user=self.request.user,
                is_active=True,
            )
        except OrganizationMember.DoesNotExist:
            raise PermissionDenied("You don't have permission to edit this site")

        if not member.can_edit_projects:
            raise PermissionDenied("You don't have permission to edit this site")

    def _create_structure_tree(self, site, node, parent=None):
        """Recursively create spatial structures from a nested payload."""
        if not isinstance(node, dict):
            raise ValidationError({"children": "Each child must be an object"})

        spatial_type = node.get("spatial_type")
        name = node.get("name")
        if not spatial_type:
            raise ValidationError({"spatial_type": "spatial_type is required"})
        if not name:
            raise ValidationError({"name": "name is required"})

        level = parent.level + 1 if parent else 0
        structure = SpatialStructure.objects.create(
            site=site,
            parent=parent,
            spatial_type=spatial_type,
            name=name,
            description=node.get("description", ""),
            level=level,
            order_in_parent=node.get("order_in_parent", 0),
            properties=node.get("properties", {}),
        )

        children = node.get("children", [])
        if children is None:
            children = []
        if not isinstance(children, list):
            raise ValidationError({"children": "children must be a list"})

        for index, child_node in enumerate(children):
            if (
                isinstance(child_node, dict)
                and child_node.get("order_in_parent") is None
                and "order_in_parent" not in child_node
            ):
                child_node = dict(child_node)
                child_node["order_in_parent"] = index
            self._create_structure_tree(site, child_node, parent=structure)

        return structure


class ElementViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for elements (physical components)"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ElementSerializer
    filterset_fields = ["site", "asset_type", "spatial_structure"]
    search_fields = ["name", "description"]
    ordering = ["spatial_structure", "asset_type"]

    def get_queryset(self):
        """Return elements from sites user can access"""
        if getattr(self, "swagger_fake_view", False):
            return Element.objects.none()

        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user, is_active=True
        ).values_list("organization", flat=True)

        return Element.objects.filter(site__project__organization__in=user_organizations)

    def perform_create(self, serializer):
        """Verify user can edit the site and set site context"""
        struct = serializer.validated_data["spatial_structure"]
        site = struct.site
        facility = getattr(struct, "facility", None) or getattr(site, "facilities", None)
        member = OrganizationMember.objects.get(
            organization=site.project.organization, user=self.request.user
        )
        if not member.can_edit_projects:
            raise PermissionDenied("You don't have permission to edit this site")

        serializer.context["site"] = site
        serializer.save(site=site, facility=facility)

    def perform_update(self, serializer):
        """Verify user can edit the site"""
        element = self.get_object()
        member = OrganizationMember.objects.get(
            organization=element.site.project.organization, user=self.request.user
        )
        if not member.can_edit_projects:
            raise PermissionDenied("You don't have permission to edit this site")

        serializer.save()

    def perform_destroy(self, instance):
        """Verify user can edit the site"""
        member = OrganizationMember.objects.get(
            organization=instance.site.project.organization, user=self.request.user
        )
        if not member.can_delete_projects:
            raise PermissionDenied(
                "You don't have permission to delete elements from this site"
            )

        instance.delete()


class FacilityViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for facilities within sites"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FacilitySerializer
    serializer_action_classes = {
        "structure_create": FacilityStructureCreateSerializer,
    }
    filterset_fields = ["project", "site", "facility_type"]
    search_fields = ["name", "description"]
    ordering = ["name"]

    def get_serializer_class(self):
        if hasattr(self, "serializer_action_classes"):
            return self.serializer_action_classes.get(self.action, self.serializer_class)
        return super().get_serializer_class()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Facility.objects.none()

        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user, is_active=True
        ).values_list("organization", flat=True)

        return Facility.objects.filter(project__organization__in=user_organizations)

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        member = OrganizationMember.objects.get(
            organization=project.organization, user=self.request.user
        )
        if not member.can_edit_projects:
            raise PermissionDenied("You don't have permission to add facilities")
        serializer.save()

    def perform_update(self, serializer):
        facility = self.get_object()
        member = OrganizationMember.objects.get(
            organization=facility.project.organization, user=self.request.user
        )
        if not member.can_edit_projects:
            raise PermissionDenied("You don't have permission to edit facilities")
        serializer.save()

    def perform_destroy(self, instance):
        member = OrganizationMember.objects.get(
            organization=instance.project.organization, user=self.request.user
        )
        if not member.can_delete_projects:
            raise PermissionDenied("You don't have permission to delete facilities")
        instance.delete()

    @action(detail=True, methods=["get"], url_path="structure/details")
    def structure_details(self, request, pk=None):
        facility = self.get_object()
        site = facility.site
        spatial_structures = site.spatial_structures.filter(parent__isnull=True).order_by(
            "order_in_parent"
        )
        elements = site.elements.all()
        if facility:
            elements = elements.filter(facility=facility)

        return Response(
            {
                "facility": str(facility.id),
                "site": str(site.id),
                "spatial_structures": SpatialStructureSerializer(
                    spatial_structures, many=True, context={"request": request}
                ).data,
                "elements": ElementSerializer(
                    elements, many=True, context={"request": request}
                ).data,
                "materials": MaterialSerializer(
                    facility.materials.all(), many=True, context={"request": request}
                ).data,
            }
        )

    @extend_schema(
        request=FacilityStructureCreateSerializer,
        responses={201: OpenApiTypes.OBJECT},
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="structure/create",
        serializer_class=FacilityStructureCreateSerializer,
    )
    def structure_create(self, request, pk=None):
        """
        Create spatial structures and elements for this facility/site in one payload.
        Payload shape:
        {
          "materials": [ {id, name, ...} ],
          "spatial_structures": [ {spatial_type, name, properties?, order_in_parent?, children: [...] , client_id?} ],
          "elements": [ {asset_type, spatial_structure (uuid) or spatial_structure_client_id, name?, description?, properties?} ]
        }
        """
        facility = self.get_object()
        site = facility.site

        member = OrganizationMember.objects.get(
            organization=site.project.organization, user=request.user
        )
        if not member.can_edit_projects:
            raise PermissionDenied("You don't have permission to edit this site")

        payload = request.data if isinstance(request.data, dict) else {}
        spatial_data = payload.get("spatial_structures", [])
        elements_data = payload.get("elements", [])
        materials_data = payload.get("materials", [])

        created_structures = {}
        created_elements = []
        created_materials = []

        def create_node(node, parent=None):
            if not isinstance(node, dict):
                raise ValidationError({"spatial_structures": "Each node must be an object"})
            spatial_type = node.get("spatial_type")
            name = node.get("name")
            if not spatial_type:
                raise ValidationError({"spatial_type": "spatial_type is required"})
            if not name:
                raise ValidationError({"name": "name is required"})
            client_id = node.get("client_id") or node.get("id")
            struct = SpatialStructure.objects.create(
                site=site,
                parent=parent,
                spatial_type=spatial_type,
                name=name,
                description=node.get("description", ""),
                order_in_parent=node.get("order_in_parent", 0),
                properties=node.get("properties", {}),
                level=(parent.level + 1) if parent else 0,
            )
            if client_id:
                created_structures[client_id] = struct
            for child in node.get("children", []) or []:
                create_node(child, struct)

        with transaction.atomic():
            for mat in materials_data:
                material = Material.objects.create(
                    facility=facility,
                    name=mat.get("name", ""),
                    code=mat.get("code"),
                    description=mat.get("description", ""),
                    properties=mat.get("properties", {}),
                )
                created_materials.append(material.id)

            for root in spatial_data:
                create_node(root, parent=None)

            for el in elements_data:
                spatial_ref = el.get("spatial_structure") or el.get("spatial_structure_id")
                if not spatial_ref and el.get("spatial_structure_client_id"):
                    spatial_ref = created_structures.get(el["spatial_structure_client_id"])
                struct_obj = None
                if isinstance(spatial_ref, SpatialStructure):
                    struct_obj = spatial_ref
                elif spatial_ref:
                    struct_obj = get_object_or_404(
                        SpatialStructure, id=spatial_ref, site=site
                    )
                else:
                    raise ValidationError(
                        {"spatial_structure": "spatial_structure is required for element"}
                    )

                material_obj = None
                if el.get("material"):
                    material_obj = Material.objects.filter(
                        id=el.get("material"), facility=facility
                    ).first()

                elem = Element.objects.create(
                    site=site,
                    spatial_structure=struct_obj,
                    facility=facility,
                    asset_type=el.get("asset_type"),
                    name=el.get("name", ""),
                    description=el.get("description", ""),
                    properties=el.get("properties", {}),
                    geometry=el.get("geometry", {}),
                    position=el.get("position", {}),
                    material=material_obj,
                )
                created_elements.append(elem.id)

        return Response(
            {
                "facility": str(facility.id),
                "site": str(site.id),
                "created_spatial_structures": [str(s.id) for s in created_structures.values()],
                "created_elements": [str(eid) for eid in created_elements],
                "created_materials": [str(mid) for mid in created_materials],
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], url_path="generate-ifc")
    def generate_ifc(self, request, pk=None):
        """Queue IFC generation for this facility's site and facility context."""
        facility = self.get_object()
        site = facility.site

        # permission: edit projects
        member = OrganizationMember.objects.get(
            organization=facility.project.organization, user=request.user
        )
        if not member.can_edit_projects:
            raise PermissionDenied(
                "You don't have permission to generate IFC in this organization"
            )

        try:
            task = generate_ifc_for_site.delay(str(site.id), str(facility.id))
            return Response(
                {
                    "status": "queued",
                    "facility_id": str(facility.id),
                    "site_id": str(site.id),
                    "task_id": task.id,
                    "message": "IFC generation task has been queued. Check generated_ifcs for results.",
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            logger.error(
                f"Failed to queue IFC generation for facility {facility.id}: {e}"
            )
            return Response(
                {"error": f"Failed to queue IFC generation: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
