from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import RequestSubmission
from .models import Organization, OrganizationMember

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """Login – Swagger shows editable username/password fields."""

    username = serializers.CharField(
        max_length=150, required=True, help_text="Username (e.g., admin)"
    )
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Password",
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        if username and password:
            return attrs
        raise serializers.ValidationError("Both username and password are required.")


class RegisterSerializer(serializers.ModelSerializer):
    """Register – Swagger editable fields."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Password (min 8 chars)",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"email": {"required": True}, "username": {"required": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class RequestSubmissionSerializer(serializers.ModelSerializer):
    """Request submission serializer for frontend form submission."""

    class Meta:
        model = RequestSubmission
        fields = [
            "request_type",
            "firstname",
            "lastname",
            "email",
            "company_name",
            "company_address",
            "country",
            "sector",
            "job_title",
            "company_position",
            "phone_number",
            "additional_details",
            "consent_marketing",
            "consent_privacy",
            "project_params",
        ]
        extra_kwargs = {
            "request_type": {"required": True},
            "firstname": {"required": True},
            "lastname": {"required": True},
            "email": {"required": True},
            "company_name": {"required": True},
            "company_address": {"required": True},
            "country": {"required": True},
            "sector": {"required": True},
            "job_title": {"required": True},
            "phone_number": {"required": True},
            "additional_details": {"required": False, "allow_blank": True},
            "consent_marketing": {"required": True},
            "consent_privacy": {"required": True},
            "project_params": {"required": False, "allow_null": True},
        }


class UserSerializer(serializers.ModelSerializer):
    """User + tokens output."""

    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined", "access", "refresh"]
        read_only_fields = ["id", "date_joined", "access", "refresh"]

    def get_access(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def get_refresh(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh)


class OrganizationMemberSerializer(serializers.ModelSerializer):
    """Serializer for organization members with user details."""

    user_email = serializers.CharField(source="user.email", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = OrganizationMember
        fields = [
            "id",
            "user",
            "user_email",
            "user_username",
            "organization",
            "role",
            "can_edit_projects",
            "can_delete_projects",
            "can_manage_team",
            "can_manage_settings",
            "joined_at",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "user_email",
            "user_username",
            "joined_at",
            "can_edit_projects",
            "can_delete_projects",
            "can_manage_team",
            "can_manage_settings",
        ]


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for organizations with member count."""

    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "owner",
            "contact_email",
            "contact_phone",
            "website",
            "country",
            "state",
            "city",
            "address",
            "postal_code",
            "is_active",
            "created_at",
            "updated_at",
            "members_count",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "members_count"]

    def get_members_count(self, obj):
        """Return count of active members."""
        return obj.organization_members.filter(is_active=True).count()


class OrganizationDetailSerializer(OrganizationSerializer):
    """Detailed serializer for organizations including members list."""

    members = OrganizationMemberSerializer(
        source="organization_members", many=True, read_only=True
    )

    class Meta(OrganizationSerializer.Meta):
        fields = OrganizationSerializer.Meta.fields + ["members"]
