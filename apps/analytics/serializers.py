from rest_framework import serializers

from apps.parametric_generator.models import GeneratedIFC

from .constants import ANALYSIS_TYPES, ANALYSIS_TYPE_VALUES
from .models import IFCAnalysisFile, AnalysisSession, AnalysisResult
from .services import (
    build_default_session_name,
    format_file_size,
    sync_analysis_file_metadata,
)


class IFCAnalysisFileSerializer(serializers.ModelSerializer):
    generated_ifc = serializers.PrimaryKeyRelatedField(
        queryset=GeneratedIFC.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = IFCAnalysisFile
        fields = [
            "id",
            "owner",
            "source_type",
            "name",
            "file_url",
            "file_size_bytes",
            "ifc_schema",
            "generated_ifc",
            "uploaded_ifc",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "file_size_bytes",
            "ifc_schema",
            "file_url",
            "created_at",
        ]
        extra_kwargs = {
            "name": {"required": False, "allow_blank": True},
        }

    def validate(self, attrs):
        source_type = attrs.get(
            "source_type", getattr(self.instance, "source_type", None)
        )
        generated_ifc = attrs.get(
            "generated_ifc", getattr(self.instance, "generated_ifc", None)
        )
        uploaded_ifc = attrs.get(
            "uploaded_ifc", getattr(self.instance, "uploaded_ifc", None)
        )
        if source_type == "generated" and not generated_ifc:
            raise serializers.ValidationError(
                "generated_ifc is required for source_type=generated"
            )
        if source_type == "uploaded" and not uploaded_ifc:
            raise serializers.ValidationError(
                "uploaded_ifc is required for source_type=uploaded"
            )
        return attrs

    def create(self, validated_data):
        analysis_file = IFCAnalysisFile(**validated_data)
        analysis_file.save()
        sync_analysis_file_metadata(analysis_file)
        analysis_file.save(
            update_fields=["name", "file_url", "file_size_bytes", "ifc_schema"]
        )
        return analysis_file

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        sync_analysis_file_metadata(instance)
        instance.save()
        return instance


class AnalysisSourceSerializer(serializers.ModelSerializer):
    source_id = serializers.UUIDField(source="id", read_only=True)
    generated_ifc_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = IFCAnalysisFile
        fields = [
            "source_id",
            "source_type",
            "name",
            "file_url",
            "file_size_bytes",
            "ifc_schema",
            "generated_ifc_id",
            "created_at",
        ]
        read_only_fields = [
            "source_id",
            "file_url",
            "file_size_bytes",
            "ifc_schema",
            "generated_ifc_id",
            "created_at",
        ]


class AnalysisSourceUploadSerializer(AnalysisSourceSerializer):
    file = serializers.FileField(write_only=True, source="uploaded_ifc")

    class Meta(AnalysisSourceSerializer.Meta):
        fields = (
            AnalysisSourceSerializer.Meta.fields[:4]
            + ["file"]
            + AnalysisSourceSerializer.Meta.fields[4:]
        )
        extra_kwargs = {
            "name": {"required": False, "allow_blank": True},
        }

    def validate_source_type(self, value):
        if value != "uploaded":
            raise serializers.ValidationError(
                "source_type must be 'uploaded' for this endpoint."
            )
        return value

    def create(self, validated_data):
        validated_data.pop("source_type", None)
        analysis_file = IFCAnalysisFile(
            owner=self.context["request"].user,
            source_type="uploaded",
            **validated_data,
        )
        analysis_file.save()
        sync_analysis_file_metadata(analysis_file)
        analysis_file.save(
            update_fields=["name", "file_url", "file_size_bytes", "ifc_schema"]
        )
        return analysis_file


class AnalysisGeneratedSourceSerializer(serializers.Serializer):
    generated_ifc_id = serializers.PrimaryKeyRelatedField(
        queryset=GeneratedIFC.objects.all(),
        source="generated_ifc",
    )
    name = serializers.CharField(required=False, allow_blank=True, max_length=255)

    def validate_generated_ifc(self, value):
        request = self.context["request"]
        if value.project.user_id != request.user.id:
            raise serializers.ValidationError(
                "You do not have access to this generated IFC."
            )
        if not value.ifc_file:
            raise serializers.ValidationError(
                "This generated IFC does not have a stored file."
            )
        return value

    def create(self, validated_data):
        generated_ifc = validated_data["generated_ifc"]
        name = validated_data.get("name", "")
        analysis_file, _ = IFCAnalysisFile.objects.get_or_create(
            owner=self.context["request"].user,
            source_type="generated",
            generated_ifc=generated_ifc,
            defaults={
                "name": name
                or generated_ifc.name
                or f"Generated IFC {generated_ifc.id}",
            },
        )
        if name:
            analysis_file.name = name
        sync_analysis_file_metadata(analysis_file)
        analysis_file.save(
            update_fields=["name", "file_url", "file_size_bytes", "ifc_schema"]
        )
        return analysis_file


class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = [
            "analysis_type",
            "status",
            "severity",
            "summary",
            "issue_count",
            "duration_ms",
            "result_data",
        ]
        read_only_fields = fields


class AnalysisSessionCreateSerializer(serializers.ModelSerializer):
    analysis_types = serializers.ListField(
        child=serializers.ChoiceField(choices=ANALYSIS_TYPES),
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = AnalysisSession
        fields = [
            "name",
            "analysis_types",
        ]
        extra_kwargs = {
            "name": {"required": False, "allow_blank": True},
        }

    def validate(self, attrs):
        source_id = self.context.get("source_id")
        if not source_id:
            raise serializers.ValidationError("source_id is required in the URL path.")
        try:
            ifc_source = IFCAnalysisFile.objects.get(id=source_id)
        except IFCAnalysisFile.DoesNotExist:
            raise serializers.ValidationError("IFC analysis file not found.")

        request = self.context.get("request")
        if request and ifc_source and ifc_source.owner_id != request.user.id:
            raise serializers.ValidationError(
                {"source_id": "You do not have access to this IFC source."}
            )

        normalized = []
        seen = set()

        raw_types = attrs.get("analysis_types")
        if raw_types is None:
            raw_types = list(ANALYSIS_TYPE_VALUES)
        if raw_types:
            for value in raw_types:
                if value not in seen:
                    normalized.append(value)
                    seen.add(value)

        if not normalized:
            raise serializers.ValidationError(
                {"analysis_types": "Provide at least one analysis type."}
            )

        attrs["analysis_types"] = normalized
        attrs["ifc_source"] = ifc_source

        if ifc_source and not attrs.get("name"):
            attrs["name"] = build_default_session_name(ifc_source, normalized)

        return attrs


class AnalysisSessionDetailSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source="ifc_source.name", read_only=True)
    source_type = serializers.CharField(source="ifc_source.source_type", read_only=True)
    file_size = serializers.SerializerMethodField()
    total_issues = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()
    report_pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = AnalysisSession
        fields = [
            "id",
            "name",
            "status",
            "source_name",
            "source_type",
            "file_size",
            "total_issues",
            "started_at",
            "completed_at",
            "report_pdf_url",
            "report_generated_at",
            "results",
        ]
        read_only_fields = fields

    def get_results(self, obj):
        queryset = obj.results.order_by("analysis_type")
        return AnalysisResultSerializer(queryset, many=True).data

    def get_file_size(self, obj):
        return format_file_size(obj.ifc_source.file_size_bytes)

    def get_total_issues(self, obj):
        return sum(result.issue_count or 0 for result in obj.results.all())

    def get_report_pdf_url(self, obj):
        if not obj.report_pdf_path:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(
                f"/api/v1/analysis/sessions/{obj.id}/report/pdf/"
            )
        return f"/api/v1/analysis/sessions/{obj.id}/report/pdf/"
