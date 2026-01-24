from rest_framework import serializers
from .models import Project, GeneratedIFC


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for BIM Project with comprehensive metadata"""

    class Meta:
        model = Project
        fields = [
            "id",
            # Basic info
            "name",
            "description",
            "project_number",
            "status",
            # Client
            "client_name",
            # Location
            "country",
            "city_address",
            "latitude",
            "longitude",
            "elevation_above_sea",
            "coordinate_reference_system",
            "true_north",
            "project_north_angle",
            # Building
            "building_type",
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
            "design_target",
            # Materials
            "materials",
            # Authoring
            "authoring_name",
            "authoring_company",
            "approval_status",
            "revision_id",
            "change_description",
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
    """Extended serializer for project detail view with generated IFCs"""

    generated_ifcs = GeneratedIFCSerializer(many=True, read_only=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ["generated_ifcs"]
