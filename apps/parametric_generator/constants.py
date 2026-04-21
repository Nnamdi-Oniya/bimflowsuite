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

ELEMENT_ASSET_TYPE_CHOICES = [
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

GENERATED_IFC_ASSET_TYPE_CHOICES = [
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
    ("industrial_plant", "Industrial Plant"),
    ("marine", "Marine Facility"),
    ("distribution", "Distribution Network"),
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

# Project choices
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
IFC_SCHEMA_CHOICES = [
    ("ifc2x3", "IFC2x3"),
    ("ifc4", "IFC4"),
    ("ifc4x3", "IFC4x3"),
]
CRS_CHOICES = [
    ("epsg:4326", "WGS 84 (EPSG:4326)"),
    ("epsg:3857", "Web Mercator (EPSG:3857)"),
    ("epsg:3395", "World Mercator (EPSG:3395)"),
    ("local", "Local Coordinate System"),
    ("custom", "Custom CRS"),
]

GENERATED_IFC_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("generating", "Generating"),
    ("completed", "Completed"),
    ("failed", "Failed"),
]

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
