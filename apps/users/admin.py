from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import RequestSubmission, Organization, OrganizationMember, User
from helper.utils import (
    send_admin_notification,
    create_onboarding_user,
    send_onboarding_email,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Register the custom User model with Django admin"""

    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "date_joined",
        "last_login",
    ]
    list_filter = ["is_active", "is_staff", "is_superuser", "date_joined"]
    search_fields = ["username", "email", "first_name", "last_name"]


@admin.register(RequestSubmission)
class RequestSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        "request_type_display",
        "name",
        "email",
        "email_status",
        "response_status",
        "onboarding_status",
        "action_buttons",
        "created_at",
    ]
    list_filter = [
        "request_type",
        "email_sent",
        "admin_response_sent",
        "onboarding_email_sent",
        "created_at",
    ]
    search_fields = ["firstname", "lastname", "email", "company_name"]
    readonly_fields = [
        "email_sent",
        "created_at",
        "submission_details",
        "admin_response_sent",
        "onboarded_user",
        "onboarding_email_sent",
        "project_params",
    ]
    date_hierarchy = "created_at"
    actions = ["send_notification_email"]
    change_form_template = "admin/users/requestsubmission/change_form.html"

    fieldsets = (
        (
            "Request Information",
            {"fields": ("request_type", "email_sent", "admin_response_sent")},
        ),
        (
            "Personal Information",
            {"fields": ("firstname", "lastname", "email", "phone_number", "job_title")},
        ),
        (
            "Company Information",
            {"fields": ("company_name", "company_address", "country", "sector")},
        ),
        (
            "Additional Information",
            {"fields": ("additional_details", "consent_marketing", "consent_privacy")},
        ),
        (
            "Model Parameters",
            {
                "fields": ("project_params",),
                "description": "IFC generation parameters submitted from GenerateModelPage (if provided)",
            },
        ),
        ("Admin Response", {"fields": ("admin_response",)}),
        ("Onboarding", {"fields": ("onboarded_user", "onboarding_email_sent")}),
        ("Metadata", {"fields": ("created_at", "submission_details")}),
    )

    def name(self, obj):
        return f"{obj.firstname} {obj.lastname}"

    name.short_description = "Name"

    def request_type_display(self, obj):
        return obj.get_request_type_display()

    request_type_display.short_description = "Request Type"

    def email_status(self, obj):
        """Display if admin received notification"""
        if obj.email_sent:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Received</span>'
            )
        else:
            return format_html(
                '<span style="color: orange; font-weight: bold;">⚠ Not Received</span>'
            )

    email_status.short_description = "Admin Notification"

    def response_status(self, obj):
        """Display response status"""
        if obj.admin_response_sent:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Replied</span>'
            )
        elif obj.admin_response:
            return format_html(
                '<span style="color: blue; font-weight: bold;">✎ Draft</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ No Reply</span>'
            )

    response_status.short_description = "Response Status"

    def onboarding_status(self, obj):
        """Display onboarding status"""
        if obj.onboarded_user:
            if obj.onboarding_email_sent:
                return format_html(
                    '<span style="color: green; font-weight: bold;">✓ Onboarded</span>'
                )
            else:
                return format_html(
                    '<span style="color: orange; font-weight: bold;">⚠ User Created (Email Failed)</span>'
                )
        else:
            return format_html(
                '<span style="color: gray; font-weight: bold;">- Not Onboarded</span>'
            )

    onboarding_status.short_description = "Onboarding Status"

    def action_buttons(self, obj):
        """Display quick action buttons in list view"""
        buttons = []

        if not obj.admin_response_sent:
            buttons.append(
                f'<a class="button" href="{obj.id}/send-response/" '
                'style="background-color: #417690; color: white; padding: 5px 10px; '
                'border-radius: 3px; text-decoration: none; font-size: 11px; margin-right: 5px;">'
                "Reply</a>"
            )

        # Show onboard button only if response has been sent AND user hasn't been onboarded yet
        if obj.admin_response_sent and not obj.onboarded_user:
            buttons.append(
                f'<a class="button" href="{obj.id}/onboard-user/" '
                'style="background-color: #28a745; color: white; padding: 5px 10px; '
                'border-radius: 3px; text-decoration: none; font-size: 11px;">'
                "Onboard</a>"
            )

        if buttons:
            return format_html(" ".join(buttons))
        return "—"

    action_buttons.short_description = "Actions"

    def send_notification_email(self, request, queryset):
        """Action to send notification emails"""
        count = 0
        for submission in queryset.filter(email_sent=False):
            # Send admin notification email
            from bimflowsuite.apps.common.utils import format_submission_email

            data = {
                "firstname": submission.firstname,
                "lastname": submission.lastname,
                "request_type_display": submission.get_request_type_display(),
                "email": submission.email,
                "phone_number": submission.phone_number,
                "job_title": submission.job_title,
                "company_name": submission.company_name,
                "company_address": submission.company_address,
                "country": submission.country,
                "sector": submission.sector,
                "additional_details": submission.additional_details,
                "consent_marketing": submission.consent_marketing,
                "consent_privacy": submission.consent_privacy,
                "created_at": submission.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            subject, body = format_submission_email(data)
            email_sent = send_admin_notification(subject, body)

            if email_sent:
                submission.email_sent = True
                submission.save(update_fields=["email_sent"])
                count += 1

        self.message_user(request, f"Successfully sent {count} notification email(s).")

    send_notification_email.short_description = (
        "Send notification emails to selected requests"
    )

    def get_urls(self):
        """Add custom URLs for admin actions"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:submission_id>/send-response/",
                self.admin_site.admin_view(self.send_user_response),
                name="send_user_response",
            ),
            path(
                "<int:submission_id>/onboard-user/",
                self.admin_site.admin_view(self.onboard_user_view),
                name="onboard_user",
            ),
        ]
        return custom_urls + urls

    def send_user_response(self, request, submission_id):
        """Handle sending response email to user"""
        try:
            submission = RequestSubmission.objects.get(pk=submission_id)
        except RequestSubmission.DoesNotExist:
            self.message_user(request, "Request not found.", level="error")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/admin/"))

        if request.method == "POST":
            response_text = request.POST.get("admin_response", "").strip()
            if response_text:
                # Send email to user
                subject = (
                    f"Re: Your {submission.get_request_type_display()} - BIMFlow Suite"
                )
                body = f"""Dear {submission.firstname} {submission.lastname},

Thank you for your {submission.get_request_type_display().lower()} submission.

{response_text}

Best regards,
BIMFlow Suite Team
                """
                email_sent = send_admin_notification(
                    subject, body, recipient_email=submission.email
                )

                if email_sent:
                    submission.admin_response = response_text
                    submission.admin_response_sent = True
                    submission.save(
                        update_fields=["admin_response", "admin_response_sent"]
                    )
                    self.message_user(
                        request, f"Response sent successfully to {submission.email}"
                    )
                else:
                    self.message_user(
                        request, "Failed to send response email.", level="error"
                    )
            else:
                self.message_user(request, "Response cannot be empty.", level="error")

            return HttpResponseRedirect(
                reverse(
                    "admin:users_requestsubmission_change",
                    args=[submission_id],
                )
            )

        # GET request - show form
        context = {
            "title": f"Send Response to {submission.firstname} {submission.lastname}",
            "submission": submission,
            "opts": self.model._meta,
            "has_change_permission": self.has_change_permission(request, submission),
            "cancel_url": reverse(
                "admin:users_requestsubmission_change",
                args=[submission_id],
            ),
        }
        return render(request, "admin/send_response_form.html", context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Add action buttons to detail view"""
        extra_context = extra_context or {}
        try:
            obj = self.get_object(request, object_id)
            extra_context["show_send_response_button"] = not obj.admin_response_sent
            extra_context["send_response_url"] = f"{object_id}/send-response/"
            extra_context["show_onboard_button"] = not obj.onboarded_user
            extra_context["onboard_url"] = f"{object_id}/onboard-user/"
        except:
            pass
        return super().change_view(request, object_id, form_url, extra_context)

    def onboard_user_view(self, request, submission_id):
        """Handle user onboarding"""
        try:
            submission = RequestSubmission.objects.get(pk=submission_id)
        except RequestSubmission.DoesNotExist:
            self.message_user(request, "Request not found.", level="error")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/admin/"))

        if submission.onboarded_user:
            self.message_user(request, "User already onboarded.", level="warning")
            return HttpResponseRedirect(
                reverse(
                    "admin:users_requestsubmission_change",
                    args=[submission_id],
                )
            )

        if request.method == "POST":
            # Create user and send onboarding email (also creates project if params exist)
            user, email_sent, project = create_onboarding_user(submission)

            if user:
                project_msg = ""
                if project:
                    project_msg = f" with project '{project.name}'"
                if email_sent:
                    self.message_user(
                        request,
                        f"User account created{project_msg} and onboarding email sent to {submission.email}",
                    )
                else:
                    self.message_user(
                        request,
                        f"User account created{project_msg} but failed to send onboarding email.",
                        level="warning",
                    )
            else:
                self.message_user(
                    request, "Failed to create user account.", level="error"
                )

            return HttpResponseRedirect(
                reverse(
                    "admin:users_requestsubmission_change",
                    args=[submission_id],
                )
            )

        # GET request - show confirmation
        context = {
            "title": f"Onboard User - {submission.firstname} {submission.lastname}",
            "submission": submission,
            "opts": self.model._meta,
            "has_change_permission": self.has_change_permission(request, submission),
            "cancel_url": reverse(
                "admin:users_requestsubmission_change",
                args=[submission_id],
            ),
        }
        return render(request, "admin/onboard_user_form.html", context)

    def submission_details(self, obj):
        details = f"""
        <strong>Request Type:</strong> {obj.get_request_type_display()}<br>
        <strong>Full Name:</strong> {obj.firstname} {obj.lastname}<br>
        <strong>Email:</strong> {obj.email}<br>
        <strong>Phone:</strong> {obj.phone_number}<br>
        <strong>Job Title:</strong> {obj.job_title}<br>
        <strong>Company:</strong> {obj.company_name}<br>
        <strong>Address:</strong> {obj.company_address}<br>
        <strong>Country:</strong> {obj.country}<br>
        <strong>Sector:</strong> {obj.sector}<br>
        <strong>Admin Notified:</strong> {"✓ Yes" if obj.email_sent else "✗ No"}<br>
        <strong>Admin Replied:</strong> {"✓ Yes" if obj.admin_response_sent else "✗ No"}<br>
        <strong>Onboarded:</strong> {"✓ Yes" if obj.onboarded_user else "✗ No"}<br>
        <strong>Submitted:</strong> {obj.created_at.strftime("%Y-%m-%d %H:%M:%S")}<br>
        """
        if obj.additional_details:
            details += (
                f"<strong>Additional Details:</strong> {obj.additional_details}<br>"
            )
        return format_html(details)

    submission_details.short_description = "Submission Details"


class OrganizationMemberInline(admin.TabularInline):
    """Inline admin for managing organization members"""

    model = OrganizationMember
    extra = 1
    fields = ["user", "role", "is_active", "joined_at", "invited_by"]
    readonly_fields = ["joined_at", "invited_by"]
    raw_id_fields = ["user", "invited_by"]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin interface for organizations"""

    list_display = [
        "name",
        "slug",
        "domain",
        "owner",
        "member_count",
        "country",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "country", "created_at"]
    search_fields = ["name", "slug", "owner__username", "contact_email"]
    readonly_fields = ["slug", "created_at", "updated_at", "member_count"]

    fieldsets = (
        (
            "Organization Information",
            {"fields": ("name", "slug", "owner", "description")},
        ),
        (
            "Contact Details",
            {"fields": ("contact_email", "contact_phone", "website")},
        ),
        (
            "Address",
            {"fields": ("address", "city", "state", "country", "postal_code")},
        ),
        (
            "Settings",
            {"fields": ("is_active", "member_count")},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at")},
        ),
    )

    inlines = [OrganizationMemberInline]

    def member_count(self, obj):
        """Display count of active members"""
        count = obj.organization_members.filter(is_active=True).count()
        return format_html(f"<strong>{count}</strong> members")

    member_count.short_description = "Active Members"

    def save_model(self, request, obj, form, change):
        """Auto-set owner if creating new organization"""
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    """Admin interface for organization members"""

    list_display = [
        "user",
        "organization",
        "role",
        "permission_summary",
        "is_active",
        "joined_at",
    ]
    list_filter = ["role", "is_active", "organization", "joined_at"]
    search_fields = ["user__username", "user__email", "organization__name"]
    readonly_fields = [
        "joined_at",
        "invited_by",
        "can_edit_projects_display",
        "can_delete_projects_display",
        "can_manage_team_display",
        "can_manage_settings_display",
    ]
    raw_id_fields = ["user", "organization", "invited_by"]

    fieldsets = (
        (
            "Membership",
            {"fields": ("user", "organization", "role", "is_active")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "can_edit_projects_display",
                    "can_delete_projects_display",
                    "can_manage_team_display",
                    "can_manage_settings_display",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Audit Information",
            {"fields": ("joined_at", "invited_by")},
        ),
    )

    def permission_summary(self, obj):
        """Display permission summary"""
        perms = []
        if obj.can_edit_projects:
            perms.append("📝 Edit")
        if obj.can_delete_projects:
            perms.append("🗑️ Delete")
        if obj.can_manage_team:
            perms.append("👥 Team")
        if obj.can_manage_settings:
            perms.append("⚙️ Settings")
        return format_html(" ".join(perms)) if perms else "No permissions"

    permission_summary.short_description = "Permissions"

    def can_edit_projects_display(self, obj):
        return obj.can_edit_projects

    can_edit_projects_display.boolean = True
    can_edit_projects_display.short_description = "Can Edit Projects"

    def can_delete_projects_display(self, obj):
        return obj.can_delete_projects

    can_delete_projects_display.boolean = True
    can_delete_projects_display.short_description = "Can Delete Projects"

    def can_manage_team_display(self, obj):
        return obj.can_manage_team

    can_manage_team_display.boolean = True
    can_manage_team_display.short_description = "Can Manage Team"

    def can_manage_settings_display(self, obj):
        return obj.can_manage_settings

    can_manage_settings_display.boolean = True
    can_manage_settings_display.short_description = "Can Manage Settings"
