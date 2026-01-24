from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import Project, GeneratedIFC


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for BIM projects with comprehensive filtering and actions"""

    list_display = [
        "project_number",
        "name_truncated",
        "status_colored",
        "client_name",
        "building_type",
        "ifc_count",
        "created_at",
        "user",
    ]
    list_filter = ["status", "building_type", "ifc_schema_version", "created_at"]
    search_fields = ["name", "project_number", "client_name", "user__email"]
    readonly_fields = ["created_at", "updated_at", "ifc_count_display"]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "user",
                    "name",
                    "description",
                    "project_number",
                    "status",
                )
            },
        ),
        (
            "Client & Location",
            {
                "fields": (
                    "client_name",
                    "country",
                    "city_address",
                    "latitude",
                    "longitude",
                    "elevation_above_sea",
                    "coordinate_reference_system",
                    "true_north",
                    "project_north_angle",
                )
            },
        ),
        (
            "Building Information",
            {
                "fields": (
                    "building_type",
                    "climate_zone",
                    "design_temperature",
                    "design_target",
                )
            },
        ),
        (
            "Units & Precision",
            {
                "fields": (
                    "length_unit",
                    "area_unit",
                    "volume_unit",
                    "angle_unit",
                    "precision",
                )
            },
        ),
        (
            "IFC Configuration",
            {
                "fields": ("ifc_schema_version",),
            },
        ),
        (
            "Materials & Specifications",
            {
                "fields": ("materials",),
                "classes": ("collapse",),
            },
        ),
        (
            "Authoring & Approval",
            {
                "fields": (
                    "authoring_name",
                    "authoring_company",
                    "approval_status",
                    "revision_id",
                    "change_description",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at", "ifc_count_display"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = [
        "mark_as_concept",
        "mark_as_schematic",
        "mark_as_detailed",
        "mark_as_asbuilt",
    ]

    def get_queryset(self, request):
        """Optimize queryset with annotation"""
        queryset = super().get_queryset(request)
        return queryset.annotate(ifc_count=Count("generated_ifcs"))

    def name_truncated(self, obj):
        """Display project name truncated"""
        return obj.name[:50] + "..." if len(obj.name) > 50 else obj.name

    name_truncated.short_description = "Project Name"

    def status_colored(self, obj):
        """Display status with color coding"""
        colors = {
            "concept": "#FF9800",  # Orange
            "schematic": "#2196F3",  # Blue
            "detailed": "#4CAF50",  # Green
            "as-built": "#9C27B0",  # Purple
        }
        color = colors.get(obj.status, "#999")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_colored.short_description = "Status"

    def ifc_count(self, obj):
        """Display count of generated IFCs"""
        return obj.ifc_count

    ifc_count.short_description = "IFCs Generated"

    def ifc_count_display(self, obj):
        """Display IFC generation summary in detail view"""
        completed = obj.generated_ifcs.filter(status="completed").count()
        failed = obj.generated_ifcs.filter(status="failed").count()
        pending = obj.generated_ifcs.filter(status="pending").count()
        generating = obj.generated_ifcs.filter(status="generating").count()

        return format_html(
            "<div>"
            "<div>Total: <strong>{}</strong></div>"
            "<div>✓ Completed: <strong>{}</strong></div>"
            "<div>⏳ Generating: <strong>{}</strong></div>"
            "<div>⏰ Pending: <strong>{}</strong></div>"
            "<div>✗ Failed: <strong>{}</strong></div>"
            "</div>",
            obj.ifc_count,
            completed,
            generating,
            pending,
            failed,
        )

    ifc_count_display.short_description = "IFC Generation Summary"

    def mark_as_concept(self, request, queryset):
        count = queryset.update(status="concept")
        self.message_user(request, f"{count} projects marked as Concept")

    mark_as_concept.short_description = "Mark selected as Concept"

    def mark_as_schematic(self, request, queryset):
        count = queryset.update(status="schematic")
        self.message_user(request, f"{count} projects marked as Schematic")

    mark_as_schematic.short_description = "Mark selected as Schematic"

    def mark_as_detailed(self, request, queryset):
        count = queryset.update(status="detailed")
        self.message_user(request, f"{count} projects marked as Detailed")

    mark_as_detailed.short_description = "Mark selected as Detailed Design"

    def mark_as_asbuilt(self, request, queryset):
        count = queryset.update(status="as-built")
        self.message_user(request, f"{count} projects marked as As-Built")

    mark_as_asbuilt.short_description = "Mark selected as As-Built"


@admin.register(GeneratedIFC)
class GeneratedIFCAdmin(admin.ModelAdmin):
    """Admin interface for generated IFC files"""

    list_display = [
        "id",
        "project_link",
        "asset_type",
        "status_colored",
        "file_size_display",
        "created_at",
        "completed_at",
    ]
    list_filter = ["status", "asset_type", "created_at"]
    search_fields = ["project__name", "project__project_number"]
    readonly_fields = [
        "project",
        "specifications",
        "status",
        "ifc_file",
        "file_size",
        "error_message",
        "created_at",
        "updated_at",
        "completed_at",
    ]

    fieldsets = (
        (
            "IFC Information",
            {
                "fields": ("project", "asset_type", "status"),
            },
        ),
        (
            "Specifications",
            {
                "fields": ("specifications",),
                "classes": ("collapse",),
            },
        ),
        (
            "File Details",
            {
                "fields": ("ifc_file", "file_size"),
            },
        ),
        (
            "Status & Errors",
            {
                "fields": ("error_message",),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at", "completed_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ["retry_failed"]

    def project_link(self, obj):
        """Link to parent project"""
        url = reverse(
            "admin:parametric_generator_project_change", args=[obj.project.id]
        )
        return format_html('<a href="{}">{}</a>', url, obj.project.name)

    project_link.short_description = "Project"

    def status_colored(self, obj):
        """Display status with color coding"""
        colors = {
            "pending": "#FFC107",  # Amber
            "generating": "#2196F3",  # Blue
            "completed": "#4CAF50",  # Green
            "failed": "#F44336",  # Red
        }
        color = colors.get(obj.status, "#999")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_colored.short_description = "Status"

    def file_size_display(self, obj):
        """Display file size in human-readable format"""
        if obj.file_size == 0:
            return "-"
        size = obj.file_size
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

    file_size_display.short_description = "File Size"

    def retry_failed(self, request, queryset):
        """Reset failed IFCs to pending for retry"""
        count = queryset.filter(status="failed").update(
            status="pending", error_message=""
        )
        self.message_user(request, f"{count} failed IFCs queued for retry")

    retry_failed.short_description = "Retry failed IFC generation"

    def has_add_permission(self, request):
        """Only allow adding IFCs through API/code"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of IFC records (audit trail)"""
        return False
