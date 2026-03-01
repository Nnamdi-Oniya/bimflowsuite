from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
import logging

from .models import Project, GeneratedIFC, Site, SpatialStructure, Asset
from .serializers import (
    ProjectSerializer,
    ProjectDetailSerializer,
    GeneratedIFCSerializer,
    SiteSerializer,
    SpatialStructureSerializer,
    AssetSerializer,
    SiteStructureSerializer,
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


class CanEditProject(permissions.BasePermission):
    """Permission check: user must have edit permission"""

    def has_object_permission(self, request, view, obj):
        # obj is a Project
        if not OrganizationMember.objects.filter(
            organization=obj.organization, user=request.user, is_active=True
        ).exists():
            return False

        member = OrganizationMember.objects.get(
            organization=obj.organization, user=request.user
        )
        return member.can_edit_projects


class CanDeleteProject(permissions.BasePermission):
    """Permission check: user must have delete permission"""

    def has_object_permission(self, request, view, obj):
        # obj is a Project
        if not OrganizationMember.objects.filter(
            organization=obj.organization, user=request.user, is_active=True
        ).exists():
            return False

        member = OrganizationMember.objects.get(
            organization=obj.organization, user=request.user
        )
        return member.can_delete_projects


class ProjectViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for BIM projects (organization-based access)"""

    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]
    serializer_class = ProjectSerializer
    filterset_fields = ["phase", "project_type", "organization", "approval_status"]
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

    @action(
        detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def summary(self, request, pk=None):
        """Get project summary: metadata + generated IFC count"""
        project = self.get_object()
        self.check_object_permissions(request, project)

        return Response(
            {
                "id": project.id,
                "name": project.name,
                "project_number": project.project_number,
                "project_type": project.project_type,
                "phase": project.phase,
                "ifc_generation_count": project.generated_ifcs.count(),
                "completed_ifcs": project.generated_ifcs.filter(
                    status="completed"
                ).count(),
                "failed_ifcs": project.generated_ifcs.filter(status="failed").count(),
                "site_count": project.sites.count(),
                "created_at": project.created_at,
                "updated_at": project.updated_at,
            }
        )

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def validate_specs(self, request, pk=None):
        """Validate project specifications before IFC generation"""
        project = self.get_object()
        self.check_object_permissions(request, project)

        errors = []

        # Check required fields for IFC generation
        if not project.name:
            errors.append("Project name is required")
        if not project.project_number:
            errors.append("Project number is required")
        if not project.project_type:
            errors.append("Project type is required")

        sites = project.sites.all()
        if not sites.exists():
            errors.append("At least one site is required")
        elif not sites.filter(
            latitude__isnull=False, longitude__isnull=False
        ).exists():
            errors.append("At least one site with latitude/longitude is required")

        if errors:
            return Response(
                {"valid": False, "errors": errors}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"valid": True, "message": "Project specifications valid"})


class GeneratedIFCViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for generated IFC files"""

    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]
    serializer_class = GeneratedIFCSerializer
    filterset_fields = ["project", "asset_type", "status"]
    ordering_fields = ["created_at", "completed_at"]
    ordering = ["-created_at"]

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
                "download_url": request.build_absolute_uri(ifc.ifc_file.url),
                "filename": ifc.ifc_file.name,
                "file_size": ifc.file_size,
                "asset_type": ifc.get_asset_type_display(),
            }
        )

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def regenerate(self, request, pk=None):
        """Regenerate IFC file with same specs"""
        ifc = self.get_object()
        self.check_object_permissions(request, ifc)

        # Reset IFC to pending status
        ifc.status = "pending"
        ifc.error_message = None
        ifc.ifc_file = None
        ifc.completed_at = None
        ifc.save(update_fields=["status", "error_message", "ifc_file", "completed_at"])

        logger.info(f"IFC regeneration requested: {ifc.id}")

        return Response(
            {
                "message": "IFC regeneration queued",
                "id": ifc.id,
                "status": ifc.status,
            },
            status=status.HTTP_202_ACCEPTED,
        )

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def create_for_project(self, request):
        """Create new GeneratedIFC for a project with specifications"""
        project_id = request.data.get("project_id")
        asset_type = request.data.get("asset_type")
        ifc_schema_version = request.data.get("ifc_schema_version") or "ifc4x3"
        specifications = request.data.get("specifications", {})

        if not project_id or not asset_type:
            return Response(
                {"error": "project_id and asset_type are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        project = get_object_or_404(Project, id=project_id)

        # Check permissions
        try:
            member = OrganizationMember.objects.get(
                organization=project.organization, user=request.user, is_active=True
            )
        except OrganizationMember.DoesNotExist:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not member.can_edit_projects:
            return Response(
                {
                    "error": "You don't have permission to generate IFCs in this organization"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Create IFC record
        ifc = GeneratedIFC.objects.create(
            project=project,
            asset_type=asset_type,
            ifc_schema_version=ifc_schema_version,
            specifications=specifications,
            status="pending",
        )

        logger.info(
            f"New IFC generation queued: {ifc.id} for project {project.id} asset_type {asset_type}"
        )

        serializer = self.get_serializer(ifc)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="generate-model",
        url_name="generate-model",
    )
    def generate(self, request, pk=None):
        """Generate IFC file for a GeneratedIFC record"""
        ifc = self.get_object()
        self.check_object_permissions(request, ifc)

        if ifc.status != "pending":
            return Response(
                {"error": f"Cannot generate IFC with status: {ifc.status}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update status to generating
        ifc.status = "generating"
        ifc.save(update_fields=["status"])

        try:
            # Import all generators
            from .generators import building, road, bridge, tunnel, highrise, generic

            generator_map = {
                # Building types
                "building": building.generate_building_ifc,
                "residential": building.generate_building_ifc,
                "commercial": building.generate_building_ifc,
                "industrial": building.generate_building_ifc,
                "institutional": building.generate_building_ifc,
                # Infrastructure types
                "road": road.generate_road_ifc,
                "highway": road.generate_road_ifc,
                "bridge": bridge.generate_bridge_ifc,
                "tunnel": tunnel.generate_tunnel_ifc,
                "railway": tunnel.generate_tunnel_ifc,  # Similar to tunnel
                "parking": road.generate_road_ifc,  # Similar to road
                # Utilities
                "utility_network": generic.generate_generic_ifc,
                "power_line": generic.generate_generic_ifc,
                "pipeline": generic.generate_generic_ifc,
                "water_system": generic.generate_generic_ifc,
                "drainage": generic.generate_generic_ifc,
                # Site/Landscape
                "site": generic.generate_generic_ifc,
                "landscape": generic.generate_generic_ifc,
                "plaza": generic.generate_generic_ifc,
                "park": generic.generate_generic_ifc,
                # Specialized
                "airport": generic.generate_generic_ifc,
                "seaport": generic.generate_generic_ifc,
                "dam": generic.generate_generic_ifc,
                "solar_farm": generic.generate_generic_ifc,
                "wind_farm": generic.generate_generic_ifc,
                # MEP Systems
                "hvac_system": generic.generate_generic_ifc,
                "electrical_system": generic.generate_generic_ifc,
                "plumbing_system": generic.generate_generic_ifc,
                "fire_safety": generic.generate_generic_ifc,
                # Specialized buildings
                "highrise": highrise.generate_highrise_ifc,
                # Other
                "other": generic.generate_generic_ifc,
            }

            generator = generator_map.get(ifc.asset_type)
            if not generator:
                raise ValueError(f"No generator for asset type: {ifc.asset_type}")

            # Call generator with project and specifications
            ifc_content = generator(ifc.project, ifc.specifications)

            # Save IFC file
            filename = f"{ifc.project.project_number}_{ifc.asset_type}_{ifc.id}.ifc"
            from django.core.files.base import ContentFile

            ifc.ifc_file.save(filename, ContentFile(ifc_content), save=False)
            ifc.file_size = len(
                ifc_content.encode() if isinstance(ifc_content, str) else ifc_content
            )
            ifc.status = "completed"
            ifc.completed_at = timezone.now()
            ifc.error_message = None
            ifc.save()

            logger.info(f"IFC generation completed: {ifc.id}")

            return Response(
                {
                    "message": "IFC generated successfully",
                    "id": ifc.id,
                    "status": ifc.status,
                    "file_size": ifc.file_size,
                    "completed_at": ifc.completed_at,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            ifc.status = "failed"
            ifc.error_message = str(e)
            ifc.save(update_fields=["status", "error_message"])
            logger.error(f"IFC generation failed: {ifc.id} - {str(e)}", exc_info=True)

            return Response(
                {
                    "error": "Generation failed",
                    "message": str(e),
                    "id": ifc.id,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class SiteViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for Sites within projects (organization-based access)"""

    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]
    serializer_class = SiteSerializer
    filterset_fields = ["project", "project_type", "coordinate_reference_system"]
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
        methods=["get", "put"],
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

        elif request.method == "PUT":
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

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def generate_ifc(self, request, pk=None):
        """
        POST: Queue IFC4X3 generation for this site

        Returns:
            {
                "status": "queued",
                "generated_ifc_id": "uuid",
                "task_id": "celery-task-id"
            }
        """
        site = self.get_object()

        # Verify user can access this site
        self.check_object_permissions(request, site)

        # Verify user has edit permission
        member = OrganizationMember.objects.get(
            organization=site.project.organization, user=request.user
        )
        if not member.can_edit_projects:
            raise PermissionDenied(
                "You don't have permission to generate IFC for sites in this organization"
            )

        try:
            # Queue IFC generation task
            task = generate_ifc_for_site.delay(str(site.id))

            logger.info(
                f"IFC generation task queued for site {site.id}: task_id={task.id}"
            )

            return Response(
                {
                    "status": "queued",
                    "site_id": str(site.id),
                    "task_id": task.id,
                    "message": "IFC generation task has been queued. Check the generated_ifcs endpoint for results.",
                },
                status=status.HTTP_202_ACCEPTED,
            )

        except Exception as e:
            logger.error(f"Failed to queue IFC generation for site {site.id}: {str(e)}")
            return Response(
                {"error": f"Failed to queue IFC generation: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

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
        """Create asset linked to a spatial structure"""
        spatial_structure_id = data.get("spatial_structure_id")
        try:
            spatial_structure = SpatialStructure.objects.get(
                id=spatial_structure_id, site=site
            )
        except SpatialStructure.DoesNotExist:
            raise ValueError(
                f"Spatial structure {spatial_structure_id} not found in this site"
            )

        Asset.objects.create(
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


class AssetViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for assets (physical elements)"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssetSerializer
    filterset_fields = ["site", "asset_type", "spatial_structure"]
    search_fields = ["name", "description"]
    ordering = ["spatial_structure", "asset_type"]

    def get_queryset(self):
        """Return assets from sites user can access"""
        if getattr(self, "swagger_fake_view", False):
            return Asset.objects.none()

        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user, is_active=True
        ).values_list("organization", flat=True)

        return Asset.objects.filter(site__project__organization__in=user_organizations)

    def perform_create(self, serializer):
        """Verify user can edit the site and set site context"""
        site = serializer.validated_data["spatial_structure"].site
        member = OrganizationMember.objects.get(
            organization=site.project.organization, user=self.request.user
        )
        if not member.can_edit_projects:
            raise PermissionDenied("You don't have permission to edit this site")

        serializer.context["site"] = site
        serializer.save(site=site)

    def perform_update(self, serializer):
        """Verify user can edit the site"""
        asset = self.get_object()
        member = OrganizationMember.objects.get(
            organization=asset.site.project.organization, user=self.request.user
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
