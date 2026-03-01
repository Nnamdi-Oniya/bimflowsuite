from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
import threading
import logging
import re

User = get_user_model()
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    RequestSubmissionSerializer,
    OrganizationSerializer,
    OrganizationDetailSerializer,
    OrganizationMemberSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    EmailOrUsernameTokenObtainPairSerializer,
    UserProfileSerializer,
)
from .models import Organization, OrganizationMember, PasswordResetToken
from helper.utils import send_request_notifications
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    inline_serializer,
)

logger = logging.getLogger(__name__)
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


@extend_schema_view(
    post=extend_schema(
        tags=["token"],
        description="Obtain JWT tokens using username or email and password.",
    )
)
class EmailOrUsernameTokenObtainPairView(TokenObtainPairView):
    """JWT token endpoint that supports login via username or email."""

    serializer_class = EmailOrUsernameTokenObtainPairSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Login with username or email and password to get JWT tokens.",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="Login successful"),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Invalid credentials"),
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username_or_email = serializer.validated_data["username_or_email"].strip()
            password = serializer.validated_data["password"]
            is_email = bool(EMAIL_PATTERN.match(username_or_email))

            if is_email:
                user = User.objects.filter(email__iexact=username_or_email).first()
            else:
                user = User.objects.filter(username__iexact=username_or_email).first()

            if not user or not user.check_password(password) or not user.is_active:
                user = None

            if user:
                refresh = RefreshToken.for_user(user)
                tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}
                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "date_joined": user.date_joined.isoformat(),
                }
                return Response(
                    {"user": user_data, "tokens": tokens}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Register a new user account.",
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description="User created successfully"),
            400: OpenApiResponse(description="Bad request - validation errors"),
        },
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined.isoformat(),
            }
            return Response(
                {"user": user_data, "tokens": tokens}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestSubmissionView(APIView):
    """Handle request submissions from the frontend."""

    permission_classes = [AllowAny]

    @extend_schema(
        description=(
            "Submit a request (demo, general enquiries, compliance validation, or other)."
        ),
        request=RequestSubmissionSerializer,
        responses={
            201: OpenApiResponse(description="Request submitted successfully"),
            400: OpenApiResponse(description="Bad request - validation errors"),
        },
    )
    def post(self, request):
        """
        Submit a new request with user details and consent information.
        Supports request types: Request a Demo, General Enquiries, Compliance Validation, Other.
        Sends admin notification and user acknowledgement emails asynchronously.
        """
        serializer = RequestSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save()

            # Send admin + user acknowledgement emails asynchronously
            email_thread = threading.Thread(
                target=send_request_notifications, args=(submission,), daemon=True
            )
            email_thread.start()

            return Response(
                {
                    "message": "Request received successfully. We will contact you soon.",
                    "submission": {
                        "id": submission.id,
                        "request_type": submission.get_request_type_display(),
                        "firstname": submission.firstname,
                        "lastname": submission.lastname,
                        "email": submission.email,
                        "company_name": submission.company_name,
                        "created_at": submission.created_at.isoformat(),
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):
    """Activate user account by setting password and marking user as active"""

    permission_classes = [AllowAny]

    @extend_schema(
        description=(
            "Activate user account by verifying email, uid, token and setting password."
        ),
        request=inline_serializer(
            name="ActivateAccountRequest",
            fields={
                "email": serializers.CharField(),
                "uid": serializers.CharField(),
                "token": serializers.CharField(),
                "password": serializers.CharField(),
                "password_confirm": serializers.CharField(),
            },
        ),
        responses={
            200: OpenApiResponse(description="Account activated successfully"),
            400: OpenApiResponse(description="Bad request - validation errors"),
        },
    )
    def post(self, request):
        """
        Activate user account by verifying email, token and setting password.
        This endpoint:
        1. Validates the activation token (must be valid and within 24 hours)
        2. Sets the user's password
        3. Marks the user as active (is_active = True)

        Token must be valid (within 24 hours of generation).
        Frontend handles redirect based on success/error response.
        """
        email_encoded = request.data.get("email")
        uid = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")
        password_confirm = request.data.get("password_confirm")

        # Validate inputs
        if not all([email_encoded, uid, token, password, password_confirm]):
            return Response(
                {
                    "success": False,
                    "error": "Missing required fields: email, uid, token, password, password_confirm",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != password_confirm:
            return Response(
                {"success": False, "error": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(password) < 8:
            return Response(
                {
                    "success": False,
                    "error": "Password must be at least 8 characters long",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Decode user ID and email
            user_id = force_str(urlsafe_base64_decode(uid))
            email = force_str(urlsafe_base64_decode(email_encoded))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, User.DoesNotExist):
            return Response(
                {"success": False, "error": "Invalid activation link"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate email matches
        if user.email != email:
            return Response(
                {"success": False, "error": "Email does not match user account"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Verify token
        if not default_token_generator.check_token(user, token):
            return Response(
                {
                    "success": False,
                    "error": "Activation link has expired or is invalid",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set password and activate user
        user.set_password(password)
        user.is_active = True
        user.save()

        return Response(
            {
                "success": True,
                "message": "Account activated successfully. You can now login.",
            },
            status=status.HTTP_200_OK,
        )


class OrganizationViewSet(viewsets.ModelViewSet):
    """Viewset for managing organizations"""

    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer
    filterset_fields = ["is_active", "country"]
    search_fields = ["name", "slug", "description"]
    ordering_fields = ["created_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Return organizations where user is a member"""
        if getattr(self, "swagger_fake_view", False):
            return Organization.objects.none()
        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user, is_active=True
        ).values_list("organization", flat=True)
        return Organization.objects.filter(id__in=user_organizations)

    def get_serializer_class(self):
        """Use detailed serializer for retrieve"""
        if self.action == "retrieve":
            return OrganizationDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create organization and add creator as owner"""
        organization = serializer.save(owner=self.request.user)
        # Add creator as owner member
        OrganizationMember.objects.create(
            organization=organization, user=self.request.user, role="owner"
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_member(self, request, pk=None):
        """Add a member to the organization"""
        organization = self.get_object()

        # Check if user has manage_team permission
        try:
            member = OrganizationMember.objects.get(
                organization=organization, user=request.user
            )
            if not member.can_manage_team:
                raise PermissionDenied(
                    "You don't have permission to manage team members"
                )
        except OrganizationMember.DoesNotExist:
            raise PermissionDenied("You are not a member of this organization")

        # Get user to add
        username = request.data.get("username")
        role = request.data.get("role", "member")

        if not username:
            return Response(
                {"error": "username is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            new_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if already a member
        if OrganizationMember.objects.filter(
            organization=organization, user=new_user
        ).exists():
            return Response(
                {"error": "User is already a member"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create membership
        org_member = OrganizationMember.objects.create(
            organization=organization,
            user=new_user,
            role=role,
            invited_by=request.user,
        )

        serializer = OrganizationMemberSerializer(org_member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def remove_member(self, request, pk=None):
        """Remove a member from the organization"""
        organization = self.get_object()

        # Check if user has manage_team permission
        try:
            member = OrganizationMember.objects.get(
                organization=organization, user=request.user
            )
            if not member.can_manage_team:
                raise PermissionDenied(
                    "You don't have permission to manage team members"
                )
        except OrganizationMember.DoesNotExist:
            raise PermissionDenied("You are not a member of this organization")

        # Get member to remove
        member_id = request.data.get("member_id")
        if not member_id:
            return Response(
                {"error": "member_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            org_member = OrganizationMember.objects.get(
                id=member_id, organization=organization
            )
        except OrganizationMember.DoesNotExist:
            return Response(
                {"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Can't remove owner
        if org_member.role == "owner":
            return Response(
                {"error": "Cannot remove organization owner"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        org_member.is_active = False
        org_member.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganizationMemberViewSet(viewsets.ModelViewSet):
    """Viewset for managing organization members"""

    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationMemberSerializer
    filterset_fields = ["organization", "role", "is_active"]
    ordering_fields = ["joined_at", "role"]
    ordering = ["joined_at"]

    def get_queryset(self):
        """Return members of organizations the user belongs to"""
        if getattr(self, "swagger_fake_view", False):
            return OrganizationMember.objects.none()
        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user, is_active=True
        ).values_list("organization", flat=True)
        return OrganizationMember.objects.filter(organization__in=user_organizations)

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def change_role(self, request, pk=None):
        """Change member role (requires manage_team permission)"""
        org_member = self.get_object()

        # Check if user has manage_team permission in this organization
        try:
            requester_member = OrganizationMember.objects.get(
                organization=org_member.organization, user=request.user
            )
            if not requester_member.can_manage_team:
                raise PermissionDenied(
                    "You don't have permission to manage team members"
                )
        except OrganizationMember.DoesNotExist:
            raise PermissionDenied("You are not a member of this organization")

        new_role = request.data.get("role")
        if not new_role:
            return Response(
                {"error": "role is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_role not in dict(OrganizationMember.ROLE_CHOICES):
            return Response(
                {
                    "error": f"Invalid role. Must be one of {[r[0] for r in OrganizationMember.ROLE_CHOICES]}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        org_member.role = new_role
        org_member.save()

        serializer = self.get_serializer(org_member)
        return Response(serializer.data)


class ForgotPasswordView(APIView):
    """View for requesting password reset token via email."""

    permission_classes = [AllowAny]

    @extend_schema(
        description=(
            "Request password reset token. If account exists, reset email is sent."
        ),
        request=ForgotPasswordSerializer,
        responses={204: OpenApiResponse(description="No content")},
    )
    def post(self, request):
        """
        Request password reset token for a registered email.
        If email doesn't match any registered account, silently return 204 (security best practice).
        If email exists, sends reset token via email.
        """
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            # Return 204 even if invalid data (silent fail for security)
            return Response(status=status.HTTP_204_NO_CONTENT)

        email = serializer.validated_data["email"]

        # Check if user exists with this email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Create reset token
        reset_token = PasswordResetToken.create_reset_token(user)

        # Send email in background thread
        email_thread = threading.Thread(
            target=self._send_reset_email, args=(user, reset_token), daemon=True
        )
        email_thread.start()

        # Always return 204 for security (don't reveal if user exists)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _send_reset_email(self, user, reset_token):
        """Send password reset email with token."""
        try:
            # Construct reset URL for frontend
            frontend_base_url = settings.BASE_URL
            reset_url = f"{frontend_base_url}/reset-password?token={reset_token.token}"

            subject = "Password Reset Request - BIMFlow Suite"
            message = f"""
Hello {user.first_name or user.username},

We received a request to reset your password for your BIMFlow Suite account.
Click the link below to reset your password:

{reset_url}

This link will expire in 24 hours.

If you did not request a password reset, please ignore this email.

Best regards,
BIMFlow Suite Team
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"Password reset email sent to {user.email}")
        except Exception as e:
            logger.error(
                f"Failed to send password reset email to {user.email}: {str(e)}"
            )


class ResetPasswordView(APIView):
    """View for resetting password with valid token."""

    permission_classes = [AllowAny]

    @extend_schema(
        description="Reset password using valid reset token.",
        request=ResetPasswordSerializer,
        responses={
            200: OpenApiResponse(description="Password reset successful"),
            400: OpenApiResponse(description="Bad request - invalid token or password"),
        },
    )
    def post(self, request):
        """
        Reset password using a valid token.
        Token must be valid (not expired and not previously used).
        """
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_str = serializer.validated_data["token"]
        new_password = serializer.validated_data["password"]

        try:
            reset_token = PasswordResetToken.objects.get(token=token_str)
        except PasswordResetToken.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": "Invalid or expired reset token",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if token is valid
        if not reset_token.is_valid():
            return Response(
                {
                    "success": False,
                    "error": "Reset token has expired or has already been used",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set new password
        user = reset_token.user
        user.set_password(new_password)
        user.save()

        # Mark token as used
        reset_token.is_used = True
        reset_token.save()

        logger.info(f"Password reset successful for user {user.email}")

        return Response(
            {
                "success": True,
                "message": "Password has been reset successfully. You can now login with your new password.",
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(APIView):
    """View for changing password for authenticated users."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Change password for authenticated user by providing current password.",
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description="Password changed successfully"),
            400: OpenApiResponse(description="Bad request - validation errors"),
            401: OpenApiResponse(description="Unauthorized"),
        },
    )
    def post(self, request):
        """Change current user's password."""
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()

        logger.info(f"Password changed successfully for user {request.user.email}")
        return Response(
            {
                "success": True,
                "message": "Password has been changed successfully.",
            },
            status=status.HTTP_200_OK,
        )


class UserProfileView(APIView):
    """Endpoint to get and update current user profile."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Get current user profile with all details.",
        responses={
            200: UserProfileSerializer,
            401: OpenApiResponse(description="Unauthorized"),
        },
    )
    def get(self, request):
        """Get current authenticated user's profile."""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Update current user profile.",
        request=UserProfileSerializer,
        responses={
            200: UserProfileSerializer,
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
    )
    def put(self, request):
        """Update current authenticated user's profile."""
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User profile updated: {request.user.email}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
