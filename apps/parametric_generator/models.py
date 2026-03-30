import uuid
from django.db import models
from django.conf import settings
from apps.users.models import Organization


FACILITY_TYPE_CHOICES = [
    ("IFC_BUILDING", "IFC Building"),
    ("IFC_ROAD", "IFC Road"),
    ("IFC_RAILWAY", "IFC Railway"),
    ("IFC_BRIDGE", "IFC Bridge"),
    ("IFC_TUNNEL", "IFC Tunnel"),
    ("IFC_MARINE", "IFC Marine Facility"),
    ("IFC_FACTORY", "IFC Factory"),
    ("IFC_PROCESS_PLANT", "IFC Process Plant"),
    ("IFC_DISTRIBUTION_SYSTEM", "IFC Distribution System"),
    ("IFC_SITE", "IFC Site"),
    ("IFC_OTHER", "IFC Other"),
]


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

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique project identifier (UUID)",
    )

    # ==================== PROJECT TYPE CHOICES ====================
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
    project_image = models.ImageField(
        upload_to="project_images/",
        blank=True,
        null=True,
        help_text="Optional cover image for the project",
    )
    phase = models.CharField(
        max_length=20,
        choices=PROJECT_PHASE_CHOICES,
        default="concept",
        help_text="Current project design phase",
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
        ]

    def __str__(self):
        return f"{self.name} ({self.project_number})"


class Facility(models.Model):
    """
    Facility - logical facility within a site (e.g., building, bridge, tunnel).
    A site can host multiple facilities; facility type drives IFC generation path.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique facility identifier (UUID)",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="facilities",
        help_text="Project this facility belongs to",
    )
    site = models.ForeignKey(
        "Site",
        on_delete=models.CASCADE,
        related_name="facilities",
        help_text="Site that contains this facility",
    )
    name = models.CharField(max_length=255, help_text="Facility name")
    facility_type = models.CharField(
        max_length=50,
        choices=FACILITY_TYPE_CHOICES,
        help_text="Facility type (Building, Road, Bridge, etc.)",
    )
    description = models.TextField(blank=True, null=True)
    facility_image = models.ImageField(
        upload_to="facility_images/",
        blank=True,
        null=True,
        help_text="Optional image/thumbnail for this facility",
    )
    properties = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["project", "facility_type"]),
            models.Index(fields=["site"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.facility_type})"


class Material(models.Model):
    """Material catalog per facility."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="materials",
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    properties = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Site(models.Model):
    """
    Site Model - Location-specific project information

    Represents a specific construction/development site for a project.
    A project can have multiple sites (e.g., multi-phase development).
    Contains location, geometry, units, materials, and site-specific configuration.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique site identifier (UUID)",
    )

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

    # ==================== METADATA ====================
    type_metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Type-specific site details (if any).",
    )

    # ==================== LOCATION INFORMATION ====================
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Site address",
    )
    site_image = models.ImageField(
        upload_to="site_images/",
        blank=True,
        null=True,
        help_text="Optional image/thumbnail for this site",
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
    """IFC files generated from project specifications with detailed status tracking"""

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
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique IFC record identifier (UUID)",
    )
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
    file_format = models.CharField(
        max_length=20,
        default="ifc",
        help_text="File format/extension (ifc, ifcxml, etc.)",
    )

    # ==================== GENERATION DETAILS ====================
    generation_metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Details about generated IFC: element counts, schema info, etc.",
    )
    # Example structure:
    # {
    #   "total_elements": 1250,
    #   "building_elements": 800,
    #   "spatial_elements": 120,
    #   "property_sets_count": 450,
    #   "schema_version": "IFC4X3",
    #   "generator_version": "1.0.0",
    #   "generation_time_seconds": 2.5
    # }

    generation_warnings = models.JSONField(
        default=list,
        blank=True,
        help_text="Warnings during IFC generation",
    )
    # Example: ["Element 5 has missing property set", "Coordinate precision reduced"]

    # Error Tracking
    error_message = models.TextField(
        blank=True, null=True, help_text="Error message if generation failed"
    )
    error_details = models.JSONField(
        default=dict,
        blank=True,
        help_text="Detailed error information including traceback",
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


class SpatialStructure(models.Model):
    """
    Spatial Structure - Hierarchical spatial organization in IFC structure

    Represents the organizational hierarchy:
    - Building: Site → Building → BuildingStorey → Space
    - Bridge: Site → Bridge → Deck → Segment
    - Road: Site → Road → Segment → Lane

    Fields vary by spatial_type to support different project types flexibly.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique spatial structure identifier (UUID)",
    )

    SPATIAL_TYPE_CHOICES = [
        # Building hierarchy (IFC4X3)
        ("ifc_building", "IfcBuilding"),
        ("ifc_building_storey", "IfcBuildingStorey"),
        ("ifc_space", "IfcSpace"),
        ("ifc_zone", "IfcZone"),
        # Bridge hierarchy (IFC4X3)
        ("ifc_bridge", "IfcBridge"),
        ("ifc_bridge_part", "IfcBridgePart"),
        ("ifc_structural_member", "IfcStructuralMember"),
        # Road hierarchy (IFC4X3)
        ("ifc_road", "IfcRoad"),
        ("ifc_road_part", "IfcRoadPart"),
        ("ifc_alignment", "IfcAlignment"),
        # Site container (IFC4X3)
        ("ifc_site", "IfcSite"),
    ]

    # ==================== HIERARCHY ====================
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="spatial_structures",
        help_text="Site this spatial structure belongs to",
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        help_text="Parent spatial structure in hierarchy",
    )

    # ==================== IDENTIFICATION ====================
    spatial_type = models.CharField(
        max_length=50,
        choices=SPATIAL_TYPE_CHOICES,
        help_text="Type of spatial element (Building, Storey, Bridge, Deck, Road, Segment, etc.)",
    )
    name = models.CharField(
        max_length=255,
        help_text="Name/identifier for this spatial structure (e.g., 'Ground Floor', 'Main Span')",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of this spatial structure",
    )

    # ==================== HIERARCHICAL METADATA ====================
    level = models.PositiveIntegerField(
        default=0,
        help_text="Depth level in hierarchy (0=root, 1=first children, etc.)",
    )
    order_in_parent = models.PositiveIntegerField(
        default=0,
        help_text="Order/sequence within parent structure",
    )

    # ==================== PROPERTIES (Type-specific) ====================
    properties = models.JSONField(
        default=dict,
        blank=True,
        help_text="Type-specific properties (dimensions, materials, specifications)",
    )
    # Examples:
    # Building: {"height": 30.5, "footprint_area": 2500}
    # BuildingStorey: {"elevation": 5.0, "floor_to_floor_height": 3.5}
    # Road: {"length": 2500, "width": 12.0, "surface_type": "asphalt"}
    # RoadSegment: {"start_km": 0, "end_km": 1, "grade": 2.5}

    # ==================== METADATA ====================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["level", "order_in_parent", "created_at"]
        indexes = [
            models.Index(fields=["site", "spatial_type"]),
            models.Index(fields=["parent", "level"]),
        ]
        unique_together = [("site", "name")]

    def __str__(self):
        parent_name = f" in {self.parent.name}" if self.parent else ""
        return f"{self.name} ({self.get_spatial_type_display()}){parent_name}"

    def get_children_by_type(self, spatial_type):
        """Get all direct children of a specific type"""
        return self.children.filter(spatial_type=spatial_type)

    def get_all_descendants(self):
        """Recursively get all descendant spatial structures"""
        descendants = []
        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants


class Element(models.Model):
    """
    Asset - Physical elements/components in the BIM model

    Represents tangible components:
    - Building: Wall, Beam, Slab, Column, Door, Window, Pipe, etc.
    - Bridge: BeamSpan, Pier, Bearing, Railing, etc.
    - Road: Pavement, Curb, Marking, etc.

    Each asset belongs to a spatial element and inherits site context.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique asset identifier (UUID)",
    )

    ASSET_TYPE_CHOICES = [
        # Building components
        ("wall", "Wall"),
        ("beam", "Beam"),
        ("slab", "Slab"),
        ("column", "Column"),
        ("foundation", "Foundation"),
        ("door", "Door"),
        ("window", "Window"),
        ("roof", "Roof"),
        ("stairs", "Stairs"),
        ("ramp", "Ramp"),
        ("shear_wall", "Shear Wall"),
        # MEP/Services
        ("pipe", "Pipe"),
        ("duct", "Duct"),
        ("cable", "Cable"),
        ("fitting", "Fitting"),
        ("equipment", "Equipment"),
        ("sensor", "Sensor"),
        # Bridge components
        ("beam_span", "Beam Span"),
        ("girder", "Girder"),
        ("pier", "Pier"),
        ("abutment", "Abutment"),
        ("bearing", "Bearing"),
        ("expansion_joint", "Expansion Joint"),
        ("bridge_railing", "Bridge Railing"),
        ("bridge_deck", "Bridge Deck Element"),
        # Road components
        ("pavement", "Pavement"),
        ("curb", "Curb"),
        ("marking", "Road Marking"),
        ("sign", "Road Sign"),
        ("light", "Street Light"),
        ("manhole", "Manhole"),
        ("storm_drain", "Storm Drain"),
        ("alignment", "Alignment"),
        ("kerb", "Kerb"),
        ("rail", "Rail"),
        ("sleeper", "Sleeper"),
        # Generic
        ("other", "Other"),
    ]

    # ==================== RELATIONSHIPS ====================
    spatial_structure = models.ForeignKey(
        SpatialStructure,
        on_delete=models.CASCADE,
        related_name="elements",
        help_text="Spatial structure this element belongs to",
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="elements",
        help_text="Site for quick filtering and context",
    )

    # ==================== IDENTIFICATION ====================
    asset_type = models.CharField(
        max_length=50,
        choices=ASSET_TYPE_CHOICES,
        help_text="Type of asset (Wall, Beam, Pipe, etc.)",
    )
    name = models.CharField(
        max_length=255,
        help_text="Name/identifier for this asset (e.g., 'Wall-001', 'Column-A1')",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of this asset",
    )

    # ==================== PROPERTIES (Type-specific) ====================
    material = models.ForeignKey(
        "Material",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="elements",
    )
    geometry = models.JSONField(default=dict, blank=True)
    position = models.JSONField(default=dict, blank=True)
    properties = models.JSONField(
        default=dict,
        blank=True,
        help_text="Type-specific properties (dimensions, specs)",
    )
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="elements",
        null=True,
        blank=True,
        help_text="Facility this element belongs to",
    )

    # ==================== METADATA ====================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["spatial_structure", "asset_type", "created_at"]
        indexes = [
            models.Index(fields=["site", "asset_type"]),
            models.Index(fields=["spatial_structure", "asset_type"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()}) in {self.spatial_structure.name}"
