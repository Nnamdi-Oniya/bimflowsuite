from rest_framework import serializers
from .models import GeneratedModel, GenerationTask, AssetType
from intent_capture.models import ProgramSpec  # For ID resolution

class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = ['code', 'name', 'category']

class GeneratedModelSerializer(serializers.ModelSerializer):
    program_spec_id = serializers.IntegerField(write_only=True, required=False)  # Handle in create()
    asset_type_code = serializers.CharField(write_only=True, required=False)  # Input as code
    asset_type = AssetTypeSerializer(read_only=True)  # Output full object
    
    class Meta:
        model = GeneratedModel
        fields = ['id', 'program_spec_id', 'asset_type_code', 'asset_type', 'status', 'ifc_file', 'created_at', 'updated_at', 'error_message']
        read_only_fields = ['status', 'created_at', 'updated_at', 'error_message', 'user']

    def create(self, validated_data):
        program_spec_id = validated_data.pop('program_spec_id', None)
        asset_type_code = validated_data.pop('asset_type_code', None)
        
        if program_spec_id:
            validated_data['program_spec'] = ProgramSpec.objects.get(id=program_spec_id)
            validated_data['user'] = validated_data['program_spec'].intent.user  # Auto-set
        if asset_type_code:
            validated_data['asset_type'] = AssetType.objects.get(code=asset_type_code)
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        program_spec_id = validated_data.pop('program_spec_id', None)
        if program_spec_id:
            validated_data['program_spec'] = ProgramSpec.objects.get(id=program_spec_id)
            validated_data['user'] = validated_data['program_spec'].intent.user
        asset_type_code = validated_data.pop('asset_type_code', None)
        if asset_type_code:
            validated_data['asset_type'] = AssetType.objects.get(code=asset_type_code)
        return super().update(instance, validated_data)