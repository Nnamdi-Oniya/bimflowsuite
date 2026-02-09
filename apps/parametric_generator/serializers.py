from rest_framework import serializers
from .models import Project, Site, GeneratedIFC
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
            is_valid, errors = validate_type_metadata(project_type, type_metadata)
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
            "project_number",
            "phase",
            # Project Type
            "project_type",
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
            request = self.context.get("request")
            if request is not None:
                return request.build_absolute_uri(obj.ifc_file.url)
            return obj.ifc_file.url
        return None


class ProjectDetailSerializer(ProjectSerializer):
    """Extended serializer for project detail view with generated IFCs and sites"""

    generated_ifcs = GeneratedIFCSerializer(many=True, read_only=True)
    sites = SiteSerializer(many=True, read_only=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ["generated_ifcs", "sites"]
