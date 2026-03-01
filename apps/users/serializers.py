from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from apps.users.models import RequestSubmission, PasswordResetToken
from .models import Organization, OrganizationMember
import re

User = get_user_model()
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


class LoginSerializer(serializers.Serializer):
    """Login – accepts either username or email with password."""

    username_or_email = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Username or email address",
    )
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Password",
    )

    def validate(self, attrs):
        username_or_email = attrs.get("username_or_email")
        password = attrs.get("password")
        if username_or_email and password:
            return attrs
        raise serializers.ValidationError(
            "Both username/email and password are required."
        )


class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    """SimpleJWT serializer that accepts either username or email."""

    username_or_email = serializers.CharField(required=True, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop(self.username_field, None)

    def validate(self, attrs):
        username_or_email = (attrs.get("username_or_email") or "").strip()
        password = attrs.get("password")
        is_email = bool(EMAIL_PATTERN.match(username_or_email))

        if is_email:
            user = User.objects.filter(email__iexact=username_or_email).first()
        else:
            user = User.objects.filter(username__iexact=username_or_email).first()

        if not user or not user.check_password(password) or not user.is_active:
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        refresh = self.get_token(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


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


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer for forgot password request - accepts email address."""

    email = serializers.EmailField(required=True, help_text="Email address")

    def validate_email(self, value):
        """Silently accept any email (don't reveal if user exists or not)."""
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for password reset confirmation."""

    token = serializers.CharField(required=True, help_text="Password reset token")
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={"input_type": "password"},
        help_text="New password (min 8 chars)",
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Confirm password",
    )

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for authenticated password change."""

    current_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Current password",
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={"input_type": "password"},
        help_text="New password (min 8 chars)",
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Confirm new password",
    )

    def validate(self, attrs):
        """Validate current password and ensure new passwords match."""
        user = self.context["request"].user
        current_password = attrs["current_password"]
        new_password = attrs["new_password"]
        new_password_confirm = attrs["new_password_confirm"]

        if not user.check_password(current_password):
            raise serializers.ValidationError(
                {"current_password": "Current password is incorrect."}
            )

        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                {"new_password": "New passwords do not match."}
            )

        if current_password == new_password:
            raise serializers.ValidationError(
                {"new_password": "New password must be different from current password."}
            )

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile with all personal details."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "location",
            "company",
            "job_title",
            "profile_picture",
            "date_joined",
            "last_login",
            "is_active",
        ]
        read_only_fields = ["id", "username", "date_joined", "last_login", "is_active"]
