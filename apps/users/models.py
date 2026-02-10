from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import secrets


class User(AbstractUser):
    """Custom User model with unique email constraint."""

    email = models.EmailField(
        unique=True, help_text="Email address - must be unique across all users"
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email or self.username


class PasswordResetToken(models.Model):
    """Model for storing password reset tokens with expiry."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
        help_text="User requesting password reset",
    )
    token = models.CharField(
        max_length=255,
        unique=True,
        help_text="Unique reset token",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Token creation timestamp",
    )
    expires_at = models.DateTimeField(
        help_text="Token expiry timestamp",
    )
    is_used = models.BooleanField(
        default=False,
        help_text="Whether token has been used for password reset",
    )

    class Meta:
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["user", "is_used"]),
            models.Index(fields=["expires_at"]),
        ]

    def is_valid(self):
        """Check if token is valid (not expired and not used)."""
        return not self.is_used and timezone.now() < self.expires_at

    @classmethod
    def create_reset_token(cls, user):
        """Create a new reset token for a user (valid for 30 minutes)."""
        # Invalidate any existing tokens for this user
        cls.objects.filter(user=user, is_used=False).update(is_used=True)

        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(minutes=30)

        return cls.objects.create(
            user=user,
            token=token,
            expires_at=expires_at,
        )

    def __str__(self):
        return f"Reset token for {self.user.email}"


class RequestSubmission(models.Model):
    """Model for request submissions from the frontend."""

    REQUEST_TYPE_CHOICES = [
        ("request_demo", "Demo Request"),
        ("general_enquiries", "General Enquiries"),
        ("run_model_analysis", "Run Model Analysis"),
        ("compliance_validation", "Compliance Validation"),
        ("other", "Other"),
    ]

    request_type = models.CharField(
        max_length=25, choices=REQUEST_TYPE_CHOICES, help_text="Type of request"
    )
    firstname = models.CharField(max_length=100, help_text="First name")
    lastname = models.CharField(max_length=100, help_text="Last name")
    email = models.EmailField(unique=True, help_text="Email address")
    company_name = models.CharField(max_length=200, help_text="Company name")
    company_address = models.TextField(help_text="Company address")
    country = models.CharField(max_length=100, help_text="Country")
    sector = models.CharField(max_length=100, help_text="Industry sector")
    job_title = models.CharField(max_length=150, help_text="Job title")
    company_position = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Position/role in the company (e.g., Manager, Director, Executive)",
    )
    phone_number = models.CharField(max_length=20, help_text="Phone number")
    additional_details = models.TextField(
        blank=True, null=True, help_text="Additional details or message"
    )
    consent_marketing = models.BooleanField(
        default=False, help_text="Consent to receive marketing communications"
    )
    consent_privacy = models.BooleanField(
        default=False, help_text="Consent to privacy policy"
    )
    email_sent = models.BooleanField(
        default=False,
        help_text="Flag indicating if notification email was sent successfully",
    )
    admin_response = models.TextField(
        blank=True, null=True, help_text="Admin's response message to the user"
    )
    admin_response_sent = models.BooleanField(
        default=False, help_text="Flag indicating if admin response was sent to user"
    )
    onboarded_user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User account created from this request",
    )
    onboarding_email_sent = models.BooleanField(
        default=False, help_text="Flag indicating if onboarding email was sent to user"
    )
    project_params = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="IFC generation parameters (project spec) submitted via GenerateModelPage",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["request_type", "created_at"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.get_request_type_display()} - {self.firstname} {self.lastname} ({self.email})"


class Organization(models.Model):
    """Represents a company, team, or organization grouping."""

    name = models.CharField(max_length=255, help_text="Organization name")
    slug = models.SlugField(unique=True, help_text="URL-friendly identifier")
    domain = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="Organization domain (e.g., example.com) - must be unique",
    )
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_organizations",
        help_text="Organization owner",
    )
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["owner", "is_active"], name="auth_org_owner_active_idx"
            ),
            models.Index(fields=["slug"], name="auth_org_slug_idx"),
        ]

    def __str__(self):
        return self.name


class OrganizationMember(models.Model):
    """Manages user membership and roles within an organization."""

    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Administrator"),
        ("manager", "Manager"),
        ("member", "Member"),
        ("viewer", "Viewer"),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="organization_members",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="organization_memberships",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    can_edit_projects = models.BooleanField(default=False)
    can_delete_projects = models.BooleanField(default=False)
    can_manage_team = models.BooleanField(default=False)
    can_manage_settings = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invitations_sent",
    )

    class Meta:
        unique_together = [["organization", "user"]]
        indexes = [
            models.Index(
                fields=["organization", "user", "is_active"],
                name="auth_org_user_active_idx",
            ),
        ]

    def save(self, *args, **kwargs):
        """Auto-calculate permissions based on role."""
        if self.role == "owner":
            self.can_edit_projects = True
            self.can_delete_projects = True
            self.can_manage_team = True
            self.can_manage_settings = True
        elif self.role == "admin":
            self.can_edit_projects = True
            self.can_delete_projects = True
            self.can_manage_team = True
            self.can_manage_settings = True
        elif self.role == "manager":
            self.can_edit_projects = True
            self.can_delete_projects = False
            self.can_manage_team = True
            self.can_manage_settings = False
        elif self.role == "member":
            self.can_edit_projects = True
            self.can_delete_projects = False
            self.can_manage_team = False
            self.can_manage_settings = False
        elif self.role == "viewer":
            self.can_edit_projects = False
            self.can_delete_projects = False
            self.can_manage_team = False
            self.can_manage_settings = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.organization.name} ({self.role})"
