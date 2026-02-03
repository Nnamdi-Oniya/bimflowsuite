from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.users.models import Organization


class Project(models.Model):
    """Comprehensive BIM Project with detailed metadata"""

    # Project Status Choices
    PROJECT_STATUS_CHOICES = [
        ("concept", "Concept"),
        ("schematic", "Schematic"),
        ("detailed", "Detailed Design"),
        ("as-built", "As-Built"),
    ]

    # Building Type Choices
    BUILDING_TYPE_CHOICES = [
        ("residential", "Residential"),
        ("office", "Office"),
        ("hospital", "Hospital"),
        ("educational", "Educational"),
        ("retail", "Retail"),
        ("industrial", "Industrial"),
        ("mixed-use", "Mixed-Use"),
        ("other", "Other"),
    ]

    # Unit Choices
    LENGTH_UNIT_CHOICES = [("mm", "Millimeters"), ("m", "Meters")]
    AREA_UNIT_CHOICES = [("m2", "Square Meters"), ("mm2", "Square Millimeters")]
    VOLUME_UNIT_CHOICES = [("m3", "Cubic Meters"), ("mm3", "Cubic Millimeters")]
    ANGLE_UNIT_CHOICES = [("degree", "Degrees"), ("radian", "Radians")]

    # IFC Schema Choices
    IFC_SCHEMA_CHOICES = [
        ("ifc2x3", "IFC2x3"),
        ("ifc4", "IFC4"),
        ("ifc4x3", "IFC4x3"),
    ]

    # CRS (Coordinate Reference System) Choices
    CRS_CHOICES = [
        ("epsg:4326", "WGS 84 (EPSG:4326)"),
        ("epsg:3857", "Web Mercator (EPSG:3857)"),
        ("epsg:3395", "World Mercator (EPSG:3395)"),
        ("local", "Local Coordinate System"),
        ("custom", "Custom CRS"),
    ]

    # ==================== BASIC INFORMATION ====================
    # Organization-based access
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="projects",
        help_text="Organization that owns this project",
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_projects",
        help_text="User who created the project",
    )

    name = models.CharField(max_length=255, help_text="Project name")
    description = models.TextField(
        blank=True, null=True, help_text="Project description"
    )
    project_number = models.CharField(
        max_length=100, unique=True, help_text="Project number/ID"
    )
    status = models.CharField(
        max_length=20,
        choices=PROJECT_STATUS_CHOICES,
        default="concept",
        help_text="Project stage",
    )

    # ==================== CLIENT/OWNER ====================
    client_name = models.CharField(
        max_length=255, blank=True, null=True, help_text="Client/Owner name"
    )

    # ==================== LOCATION INFORMATION ====================
    country = models.CharField(max_length=100, blank=True, null=True)
    city_address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    elevation_above_sea = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Elevation in meters",
    )
    coordinate_reference_system = models.CharField(
        max_length=50,
        choices=CRS_CHOICES,
        default="epsg:4326",
        help_text="Coordinate Reference System",
    )
    true_north = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="True north in degrees",
    )
    project_north_angle = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Project north angle in degrees",
    )

    # ==================== BUILDING INFORMATION ====================
    building_type = models.CharField(
        max_length=50,
        choices=BUILDING_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text="Building type/category",
    )

    # ==================== UNITS & PRECISION ====================
    length_unit = models.CharField(
        max_length=10, choices=LENGTH_UNIT_CHOICES, default="m"
    )
    area_unit = models.CharField(max_length=10, choices=AREA_UNIT_CHOICES, default="m2")
    volume_unit = models.CharField(
        max_length=10, choices=VOLUME_UNIT_CHOICES, default="m3"
    )
    angle_unit = models.CharField(
        max_length=20, choices=ANGLE_UNIT_CHOICES, default="degree"
    )
    precision = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=0.0001,
        help_text="Geometric precision tolerance",
    )

    # ==================== IFC CONFIGURATION ====================
    ifc_schema_version = models.CharField(
        max_length=20, choices=IFC_SCHEMA_CHOICES, default="ifc4x3"
    )

    # ==================== ENVIRONMENTAL/DESIGN ====================
    climate_zone = models.CharField(
        max_length=100, blank=True, null=True, help_text="Climate zone classification"
    )
    design_temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Design temperature in Celsius",
    )
    design_target = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Design performance target or goals",
    )

    # ==================== MATERIALS (JSON) ====================
    materials = models.JSONField(
        default=dict,
        blank=True,
        help_text="Material specifications: walls, slabs, layers",
    )
    # Example structure:
    # {
    #   "walls": {
    #     "exterior": {
    #       "layers": [
    #         {"name": "Brick", "thickness": 0.12, "thermal_conductivity": 0.6},
    #         {"name": "Insulation", "thickness": 0.1, "thermal_conductivity": 0.04}
    #       ],
    #       "fire_rating": "A1",
    #       "thermal_properties": {"u_value": 0.25}
    #     }
    #   },
    #   "slabs": {...}
    # }

    # ==================== AUTHORING & APPROVAL ====================
    authoring_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Name of project author/creator",
    )
    authoring_company = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Company that authored the project",
    )
    approval_status = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="e.g., Pending, Approved, Rejected",
    )
    revision_id = models.CharField(
        max_length=50, blank=True, null=True, help_text="Current revision identifier"
    )
    change_description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of changes in this revision",
    )

    # ==================== METADATA ====================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["project_number"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.project_number})"


class GeneratedIFC(models.Model):
    """IFC files generated from project specifications"""

    ASSET_TYPE_CHOICES = [
        # Buildings
        ("building", "Building"),
        ("residential", "Residential Building"),
        ("commercial", "Commercial Building"),
        ("industrial", "Industrial Building"),
        ("institutional", "Institutional Building"),
        # Infrastructure
        ("road", "Road"),
        ("highway", "Highway"),
        ("bridge", "Bridge"),
        ("tunnel", "Tunnel"),
        ("railway", "Railway/Track"),
        ("parking", "Parking Structure"),
        # Utilities & Networks
        ("utility_network", "Utility Network"),
        ("power_line", "Power Line"),
        ("pipeline", "Pipeline"),
        ("water_system", "Water System"),
        ("drainage", "Drainage System"),
        # Site & Landscape
        ("site", "Site/Lot"),
        ("landscape", "Landscape"),
        ("plaza", "Plaza/Court"),
        ("park", "Park"),
        # Specialized
        ("airport", "Airport"),
        ("seaport", "Seaport"),
        ("dam", "Dam"),
        ("solar_farm", "Solar Farm"),
        ("wind_farm", "Wind Farm"),
        # Building Systems (MEP)
        ("hvac_system", "HVAC System"),
        ("electrical_system", "Electrical System"),
        ("plumbing_system", "Plumbing System"),
        ("fire_safety", "Fire Safety System"),
        # Other
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("generating", "Generating"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    # ==================== IDENTIFICATION ====================
    id = models.AutoField(primary_key=True, help_text="Unique IFC record ID")
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Name/label for this generated IFC",
    )

    # ==================== REFERENCES & CONFIGURATION ====================
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="generated_ifcs"
    )
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPE_CHOICES)
    ifc_schema_version = models.CharField(
        max_length=20,
        choices=Project.IFC_SCHEMA_CHOICES,
        help_text="IFC schema version used for generation",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Specifications captured from form input
    specifications = models.JSONField(
        default=dict,
        help_text="User-provided specifications for this asset",
    )

    # File Storage
    ifc_file = models.FileField(
        upload_to="ifc_files/%Y/%m/%d/",
        blank=True,
        null=True,
        help_text="Generated IFC file (supports S3 or local storage)",
    )
    file_size = models.BigIntegerField(default=0, help_text="File size in bytes")

    # Error Tracking
    error_message = models.TextField(
        blank=True, null=True, help_text="Error message if generation failed"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(
        blank=True, null=True, help_text="When generation completed"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["project", "status"]),
            models.Index(fields=["asset_type"]),
        ]

    def __str__(self):
        name = self.name or f"{self.project.name} - {self.get_asset_type_display()}"
        return name
