from django.db import models
from django.conf import settings
from apps.users.models import Organization


class Project(models.Model):
    """
    BIM Project Model - Project-level information

    Stores project metadata including client info, project schedule, and scale.
    Sites contain location-specific information (geometry, units, materials).
    A project can have multiple sites (e.g., multi-phase development, phased construction).

    Structure:
    - Basics: name, description, project_number, phase, project_type
    - Client: client_name, client_type, project_scale, risk_classification
    - Schedule: project_start_date, construction_start_date, expected_completion_date
    - Type Metadata: type_metadata for flexible type-specific details
    """

    # ==================== PROJECT TYPE CHOICES ====================
    PROJECT_TYPE_CHOICES = [
        ("IFC_BUILDING", "Building"),
        ("IFC_ROAD", "Road"),
        ("IFC_RAILWAY", "Railway"),
        ("IFC_BRIDGE", "Bridge"),
        ("IFC_TUNNEL", "Tunnel"),
        ("IFC_MARINE_FACILITY", "Marine Facility"),
        ("IFC_FACTORY", "Factory"),
        ("IFC_PROCESS_PLANT", "Process Plant"),
        ("IFC_DISTRIBUTION_SYSTEM", "Distribution System"),
        ("IFC_SITE", "Site / Land Project"),
        ("OTHER", "Other / Custom"),
    ]

    PROJECT_PHASE_CHOICES = [
        ("concept", "Concept"),
        ("schematic", "Schematic"),
        ("detailed", "Detailed Design"),
        ("as-built", "As-Built"),
    ]

    PROJECT_SCALE_CHOICES = [
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
    ]

    CLIENT_TYPE_CHOICES = [
        ("private", "Private"),
        ("government", "Government"),
        ("ngo", "NGO"),
        ("corporate", "Corporate"),
    ]

    RISK_CLASSIFICATION_CHOICES = [
        ("low", "Low Risk"),
        ("medium", "Medium Risk"),
        ("high", "High Risk"),
        ("critical", "Critical Risk"),
    ]

    # ==================== CORE RELATIONSHIPS ====================
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

    # ==================== PROJECT BASICS ====================
    name = models.CharField(
        max_length=255,
        help_text="Project name",
    )
    project_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique project identifier/number",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed project description",
    )
    phase = models.CharField(
        max_length=20,
        choices=PROJECT_PHASE_CHOICES,
        default="concept",
        help_text="Current project design phase",
    )

    # ==================== PROJECT TYPE ====================
    project_type = models.CharField(
        max_length=50,
        choices=PROJECT_TYPE_CHOICES,
        help_text="Primary project type (Building, Road, Bridge, etc.)",
    )

    # ==================== CLIENT INFORMATION ====================
    client_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Name of project client/owner",
    )
    client_type = models.CharField(
        max_length=50,
        choices=CLIENT_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text="Type of client (Private, Government, NGO, Corporate)",
    )

    # ==================== PROJECT SCALE & RISK ====================
    project_scale = models.CharField(
        max_length=20,
        choices=PROJECT_SCALE_CHOICES,
        blank=True,
        null=True,
        help_text="Scale of project (Small, Medium, Large)",
    )
    risk_classification = models.CharField(
        max_length=20,
        choices=RISK_CLASSIFICATION_CHOICES,
        blank=True,
        null=True,
        help_text="Risk level classification for project",
    )

    project_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Principal project address",
    )

    # ==================== PROJECT SCHEDULE ====================
    project_start_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Project initiation date",
    )
    construction_start_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Planned or actual construction start date",
    )
    expected_completion_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Expected project completion date",
    )

    # ==================== PROJECT GOVERNANCE ====================
    approval_status = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Approval status (e.g., Pending, Approved, Rejected)",
    )

    # ==================== METADATA ====================
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Project creation timestamp",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last modification timestamp",
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["project_number"]),
            models.Index(fields=["phase"]),
            models.Index(fields=["project_type"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.project_number})"


class Site(models.Model):
    """
    Site Model - Location-specific project information

    Represents a specific construction/development site for a project.
    A project can have multiple sites (e.g., multi-phase development).
    Contains location, geometry, units, materials, and site-specific configuration.
    """

    # Unit Choices
    LENGTH_UNIT_CHOICES = [
        ("mm", "Millimeters"),
        ("m", "Meters"),
    ]
    AREA_UNIT_CHOICES = [
        ("m2", "Square Meters"),
        ("mm2", "Square Millimeters"),
    ]
    VOLUME_UNIT_CHOICES = [
        ("m3", "Cubic Meters"),
        ("mm3", "Cubic Millimeters"),
    ]
    ANGLE_UNIT_CHOICES = [
        ("degree", "Degrees"),
        ("radian", "Radians"),
    ]

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

    # ==================== CORE RELATIONSHIPS ====================
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="sites",
        help_text="Project this site belongs to",
    )

    # ==================== SITE BASICS ====================
    site_name = models.CharField(
        max_length=255,
        help_text="Site name or identifier",
    )

    # ==================== PROJECT TYPE & METADATA ====================
    project_type = models.CharField(
        max_length=50,
        choices=Project.PROJECT_TYPE_CHOICES,
        help_text="Primary site/project type (Building, Road, Bridge, etc.)",
    )

    type_metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Type-specific site details. Structure varies by project_type.",
    )

    # ==================== LOCATION INFORMATION ====================
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Site address",
    )

    # ==================== GEOMETRY & COORDINATES ====================
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Site latitude in decimal degrees",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Site longitude in decimal degrees",
    )
    elevation = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Site elevation above sea level (meters)",
    )

    coordinate_reference_system = models.CharField(
        max_length=50,
        choices=CRS_CHOICES,
        default="epsg:4326",
        help_text="Coordinate Reference System (CRS/EPSG code)",
    )

    true_north_angle = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="True north direction in degrees (0-360)",
    )
    project_north_angle = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Project north offset from true north in degrees",
    )

    # ==================== UNITS & PRECISION ====================
    length_unit = models.CharField(
        max_length=10,
        choices=LENGTH_UNIT_CHOICES,
        default="m",
        help_text="Unit for length measurements",
    )
    area_unit = models.CharField(
        max_length=10,
        choices=AREA_UNIT_CHOICES,
        default="m2",
        help_text="Unit for area measurements",
    )
    volume_unit = models.CharField(
        max_length=10,
        choices=VOLUME_UNIT_CHOICES,
        default="m3",
        help_text="Unit for volume measurements",
    )
    angle_unit = models.CharField(
        max_length=20,
        choices=ANGLE_UNIT_CHOICES,
        default="degree",
        help_text="Unit for angle measurements",
    )
    precision = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=0.0001,
        help_text="Geometric precision tolerance",
    )

    # ==================== IFC CONFIGURATION ====================
    ifc_schema_version = models.CharField(
        max_length=20,
        choices=IFC_SCHEMA_CHOICES,
        default="ifc4x3",
        help_text="IFC schema version for generation",
    )

    # ==================== MATERIALS & ENVIRONMENTAL ====================
    climate_zone = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Climate zone classification (e.g., temperate, tropical, arctic)",
    )

    design_temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Design temperature in Celsius",
    )

    material_system = models.JSONField(
        default=dict,
        blank=True,
        help_text="Material system and specifications",
    )
    # Example structure:
    # {
    #   "structural": {"primary": "steel", "secondary": "concrete"},
    #   "exterior": {"envelope": "curtain_wall", "roofing": "metal_deck"},
    #   "interior": {"walls": "drywall", "flooring": "polished_concrete"}
    # }

    # ==================== REPORTING & REGULATORY ====================
    regulatory_requirements = models.JSONField(
        default=dict,
        blank=True,
        help_text="Applicable codes, standards, and regulatory requirements",
    )
    # Example structure:
    # {
    #   "building_codes": ["IBC_2021", "IECC_2021"],
    #   "standards": ["ASHRAE_90_1", "NFPA_101"],
    #   "certifications": ["LEED_v4", "WELL"],
    #   "accessibility": "ADA_2010"
    # }

    # ==================== METADATA ====================
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Site creation timestamp",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last modification timestamp",
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["project", "created_at"]),
            models.Index(fields=["coordinate_reference_system"]),
        ]

    def __str__(self):
        return f"{self.site_name} ({self.project.name})"


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
        choices=Site.IFC_SCHEMA_CHOICES,
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
