from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.exceptions import PermissionDenied
import threading
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    RequestSubmissionSerializer,
    OrganizationSerializer,
    OrganizationDetailSerializer,
    OrganizationMemberSerializer,
)
from .models import Organization, OrganizationMember
from apps.utils import send_request_notification
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login with username and password to get JWT tokens",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "user": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "username": openapi.Schema(type=openapi.TYPE_STRING),
                                "email": openapi.Schema(type=openapi.TYPE_STRING),
                                "date_joined": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                        "tokens": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "access": openapi.Schema(type=openapi.TYPE_STRING),
                                "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "username": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                        "password": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description="Invalid credentials",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
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

    @swagger_auto_schema(
        operation_description="Register a new user account",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response(
                description="User created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "user": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "username": openapi.Schema(type=openapi.TYPE_STRING),
                                "email": openapi.Schema(type=openapi.TYPE_STRING),
                                "date_joined": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                        "tokens": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "access": openapi.Schema(type=openapi.TYPE_STRING),
                                "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="Bad request - validation errors",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "username": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                        "email": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                        "password": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                    },
                ),
            ),
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

    @swagger_auto_schema(
        operation_description="Submit a request (demo, general enquiries, compliance validation, or other)",
        request_body=RequestSubmissionSerializer,
        responses={
            201: openapi.Response(
                description="Request submitted successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "demo_request": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "request_type": openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                "firstname": openapi.Schema(type=openapi.TYPE_STRING),
                                "lastname": openapi.Schema(type=openapi.TYPE_STRING),
                                "email": openapi.Schema(type=openapi.TYPE_STRING),
                                "company_name": openapi.Schema(
                                    type=openapi.TYPE_STRING
                                ),
                                "created_at": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="Bad request - validation errors",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "firstname": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                        "email": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                    },
                ),
            ),
        },
    )
    def post(self, request):
        """
        Submit a new request with user details and consent information.
        Supports request types: Request a Demo, General Enquiries, Compliance Validation, Other.
        Email notification will be sent to admin asynchronously.
        """
        serializer = RequestSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save()

            # Send email notification to admin asynchronously in a background thread
            email_thread = threading.Thread(
                target=send_request_notification, args=(submission,), daemon=True
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
    """Activate user account and set password"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Activate user account by setting password with activation token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "uid": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User ID (base64 encoded)"
                ),
                "token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Activation token"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="New password"
                ),
                "password_confirm": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Confirm password"
                ),
            },
            required=["uid", "token", "password", "password_confirm"],
        ),
        responses={
            200: openapi.Response(
                description="Account activated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "user": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "username": openapi.Schema(type=openapi.TYPE_STRING),
                                "email": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="Bad request - validation errors",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            404: openapi.Response(
                description="User not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
    def post(self, request):
        """
        Activate user account by verifying token and setting password.
        Token must be valid (within 24 hours of generation).
        """
        uid = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")
        password_confirm = request.data.get("password_confirm")

        # Validate inputs
        if not all([uid, token, password, password_confirm]):
            return Response(
                {
                    "error": "Missing required fields: uid, token, password, password_confirm"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != password_confirm:
            return Response(
                {"error": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(password) < 8:
            return Response(
                {"error": "Password must be at least 8 characters long"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Decode user ID
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, User.DoesNotExist):
            return Response(
                {"error": "Invalid activation link"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Verify token
        if not default_token_generator.check_token(user, token):
            return Response(
                {"error": "Activation link has expired or is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set password and activate user
        user.set_password(password)
        user.is_active = True
        user.save()

        return Response(
            {
                "message": "Account activated successfully. You can now login.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
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
