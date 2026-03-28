from rest_framework import serializers
from .models import Project, Site, Facility, GeneratedIFC, SpatialStructure, Element
from .schemas import validate_type_metadata


class SiteSerializer(serializers.ModelSerializer):
    """Serializer for Site model - location-specific project information"""

    class Meta:
        model = Site
        fields = [
            "id",
            "project",
            "site_name",
            # Type & Metadata
            "project_type",
            "type_metadata",
            # Location
            "address",
            "site_image",
            # Geometry
            "latitude",
            "longitude",
            "elevation",
            "coordinate_reference_system",
            "true_north_angle",
            "project_north_angle",
            # Units & Precision
            "length_unit",
            "area_unit",
            "volume_unit",
            "angle_unit",
            "precision",
            # IFC
            "ifc_schema_version",
            # Environmental
            "climate_zone",
            "design_temperature",
            # Materials & Regulatory
            "material_system",
            "regulatory_requirements",
            # Metadata
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        """Validate type_metadata against project_type schema"""
        project_type = data.get("project_type")
        type_metadata = data.get("type_metadata", {})

        if project_type and type_metadata:
            try:
                is_valid, errors = validate_type_metadata(project_type, type_metadata)
            except ValueError as exc:
                raise serializers.ValidationError({"project_type": str(exc)})
            if not is_valid:
                raise serializers.ValidationError(
                    {
                        "type_metadata": f"Invalid metadata for {project_type}: {'; '.join(errors)}"
                    }
                )

        return data


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for BIM Project with comprehensive metadata"""

    class Meta:
        model = Project
        fields = [
            "id",
            "organization",
            # Basic info
            "name",
            "description",
            "project_image",
            "project_number",
            "phase",
            # Client
            "client_name",
            "client_type",
            # Project Scale & Risk
            "project_scale",
            "risk_classification",
            "project_address",
            # Schedule
            "project_start_date",
            "construction_start_date",
            "expected_completion_date",
            # Governance
            "approval_status",
            # Metadata
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        """Associate project with current user"""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = [
            "id",
            "project",
            "site",
            "name",
            "facility_type",
            "description",
            "facility_image",
            "properties",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class GeneratedIFCSerializer(serializers.ModelSerializer):
    """Serializer for generated IFC files"""

    project_name = serializers.CharField(
        source="project.name", read_only=True, help_text="Name of parent project"
    )
    download_url = serializers.SerializerMethodField(
        help_text="URL to download the IFC file"
    )

    class Meta:
        model = GeneratedIFC
        fields = [
            "id",
            "project",
            "project_name",
            "asset_type",
            "status",
            "specifications",
            "ifc_file",
            "download_url",
            "file_size",
            "error_message",
            "created_at",
            "updated_at",
            "completed_at",
        ]
        read_only_fields = [
            "id",
            "ifc_file",
            "file_size",
            "error_message",
            "created_at",
            "updated_at",
            "completed_at",
        ]

    def get_download_url(self, obj):
        """Return download URL for IFC file"""
        if obj.ifc_file:
            return obj.ifc_file.url
        return None


class ProjectDetailSerializer(ProjectSerializer):
    """Extended serializer for project detail view with generated IFCs and sites"""

    generated_ifcs = GeneratedIFCSerializer(many=True, read_only=True)
    sites = SiteSerializer(many=True, read_only=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ["generated_ifcs", "sites"]


class ElementSimpleSerializer(serializers.ModelSerializer):
    """Simple element serializer for nested representation"""

    asset_type_display = serializers.CharField(
        source="get_asset_type_display", read_only=True
    )

    class Meta:
        model = Element
        fields = [
            "id",
            "asset_type",
            "asset_type_display",
            "name",
            "description",
            "properties",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class SpatialStructureSerializer(serializers.ModelSerializer):
    """Serializer for SpatialStructure with nested children and assets"""

    spatial_type_display = serializers.CharField(
        source="get_spatial_type_display", read_only=True
    )
    children = serializers.SerializerMethodField(read_only=True)
    assets = ElementSimpleSerializer(many=True, read_only=True)
    parent_name = serializers.CharField(source="parent.name", read_only=True)

    class Meta:
        model = SpatialStructure
        fields = [
            "id",
            "site",
            "parent",
            "parent_name",
            "spatial_type",
            "spatial_type_display",
            "name",
            "description",
            "level",
            "order_in_parent",
            "properties",
            "children",
            "assets",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "level", "children", "created_at", "updated_at"]

    def get_children(self, obj):
        """Get nested children recursively"""
        children = obj.children.all()
        if children.exists():
            return SpatialStructureSerializer(
                children, many=True, context=self.context
            ).data
        return []


class SiteStructureSerializer(serializers.ModelSerializer):
    """Serializer for Site with complete spatial structure (structures + assets)"""

    spatial_structures = serializers.SerializerMethodField()
    asset_summary = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = [
            "id",
            "project",
            "site_name",
            "project_type",
            "latitude",
            "longitude",
            "elevation",
            "coordinate_reference_system",
            "ifc_schema_version",
            "length_unit",
            "area_unit",
            "volume_unit",
            "spatial_structures",
            "asset_summary",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_spatial_structures(self, obj):
        """Get root spatial structures (those without parents)"""
        root_structures = obj.spatial_structures.filter(parent__isnull=True).order_by(
            "order_in_parent"
        )
        return SpatialStructureSerializer(
            root_structures, many=True, context=self.context
        ).data

    def get_asset_summary(self, obj):
        """Get summary of assets by type"""
        assets = obj.assets.all()
        summary = {}
        for asset_type, display_name in Element.ASSET_TYPE_CHOICES:
            count = assets.filter(asset_type=asset_type).count()
            if count > 0:
                summary[asset_type] = count
        return summary


class ElementSerializer(serializers.ModelSerializer):
    """Full serializer for Element with relationships"""

    asset_type_display = serializers.CharField(
        source="get_asset_type_display", read_only=True
    )
    spatial_structure_name = serializers.CharField(
        source="spatial_structure.name", read_only=True
    )
    site_name = serializers.CharField(source="site.site_name", read_only=True)

    class Meta:
        model = Element
        fields = [
            "id",
            "spatial_structure",
            "spatial_structure_name",
            "site",
            "site_name",
            "asset_type",
            "asset_type_display",
            "name",
            "description",
            "properties",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "site", "created_at", "updated_at"]

    def validate(self, data):
        """Ensure asset's spatial_structure belongs to the same site"""
        spatial_structure = data.get("spatial_structure")
        site = self.context.get("site")  # Site should be passed via context

        if spatial_structure and site and spatial_structure.site != site:
            raise serializers.ValidationError(
                "Spatial structure must belong to the same site"
            )

        return data
