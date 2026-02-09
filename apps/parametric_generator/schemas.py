"""
Type Metadata Schemas for BIM Project Types

Defines the structure and requirements for type_metadata JSONField for each project type.
Frontend should implement forms based on these schemas.

Usage:
    from apps.parametric_generator.schemas import PROJECT_TYPE_SCHEMAS, validate_type_metadata

    # Validate type_metadata during project creation
    validate_type_metadata("IFC_BUILDING", {"building_use": "residential", "num_stories": 5, ...})
"""

PROJECT_TYPE_SCHEMAS = {
    "IFC_BUILDING": {
        "description": "Building project metadata",
        "usage": "Residential, commercial, institutional, or mixed-use buildings",
        "fields": {
            "building_use": {
                "type": "string",
                "required": True,
                "enum": [
                    "residential",
                    "commercial",
                    "industrial",
                    "institutional",
                    "mixed_use",
                    "other",
                ],
                "description": "Primary use of the building (residential/office/retail/hospital/school/etc.)",
            },
            "num_stories": {
                "type": "integer",
                "required": True,
                "min": 1,
                "max": 300,
                "description": "Total number of floors/stories (including basement levels)",
            },
            "occupancy_type": {
                "type": "string",
                "required": True,
                "description": "Occupancy classification for code compliance (e.g., A-1, B, E, F-1, etc.)",
            },
            "total_area": {
                "type": "number",
                "required": True,
                "min": 0,
                "unit": "m²",
                "description": "Total building area",
            },
            "is_residential": {
                "type": "boolean",
                "required": False,
                "description": "Whether building contains residential units",
            },
            "ground_floor_use": {
                "type": "string",
                "required": False,
                "description": "Specific use of ground floor (e.g., parking, retail, lobby)",
            },
        },
    },
    "IFC_ROAD": {
        "description": "Road infrastructure metadata",
        "usage": "Highways, arterials, collectors, local streets, service roads",
        "fields": {
            "road_class": {
                "type": "string",
                "required": True,
                "enum": [
                    "highway",
                    "arterial",
                    "collector",
                    "local",
                    "service",
                    "private",
                ],
                "description": "Road classification by functional type",
            },
            "road_usage": {
                "type": "string",
                "required": True,
                "enum": ["urban", "suburban", "rural", "mixed"],
                "description": "Road context/environment where it operates",
            },
            "num_lanes": {
                "type": "integer",
                "required": True,
                "min": 1,
                "max": 20,
                "description": "Total number of traffic lanes (does not include shoulder/turn lanes)",
            },
            "pavement_type": {
                "type": "string",
                "required": True,
                "enum": ["asphalt", "concrete", "gravel", "brick_paver", "permeable"],
                "description": "Surface material",
            },
            "length": {
                "type": "number",
                "required": True,
                "min": 0,
                "unit": "km",
                "description": "Total road length",
            },
            "design_speed": {
                "type": "integer",
                "required": False,
                "unit": "km/h",
                "description": "Designed speed limit for the road",
            },
            "shoulder_width": {
                "type": "number",
                "required": False,
                "unit": "m",
                "description": "Width of shoulder/verge on each side",
            },
            "median_type": {
                "type": "string",
                "required": False,
                "enum": ["none", "painted", "barrier", "landscaped"],
                "description": "Median separation type (if divided highway)",
            },
        },
    },
    "IFC_BRIDGE": {
        "description": "Bridge infrastructure metadata",
        "usage": "Vehicular bridges, pedestrian bridges, railway bridges, combined-use structures",
        "fields": {
            "bridge_type": {
                "type": "string",
                "required": True,
                "enum": [
                    "suspension",
                    "cable_stay",
                    "arch",
                    "beam",
                    "truss",
                    "composite",
                ],
                "description": "Structural type of bridge",
            },
            "bridge_usage": {
                "type": "string",
                "required": True,
                "enum": ["vehicular", "pedestrian", "railway", "pipeline", "combined"],
                "description": "Primary use/traffic type",
            },
            "span_length": {
                "type": "number",
                "required": True,
                "min": 0,
                "unit": "m",
                "description": "Main span length",
            },
            "total_length": {
                "type": "number",
                "required": False,
                "unit": "m",
                "description": "Total bridge length including approaches",
            },
            "material_system": {
                "type": "string",
                "required": True,
                "enum": ["steel", "concrete", "hybrid", "timber", "composite"],
                "description": "Primary structural material",
            },
            "clearance": {
                "type": "number",
                "required": True,
                "unit": "m",
                "description": "Vertical clearance above water/road below",
            },
            "num_lanes": {
                "type": "integer",
                "required": False,
                "description": "Number of traffic lanes (for vehicular bridges)",
            },
            "pedestrian_walkway": {
                "type": "boolean",
                "required": False,
                "description": "Whether bridge includes pedestrian facilities",
            },
        },
    },
    "IFC_RAILWAY": {
        "description": "Railway infrastructure metadata",
        "usage": "High-speed rail, commuter rail, freight lines, urban transit, heritage railways",
        "fields": {
            "rail_type": {
                "type": "string",
                "required": True,
                "enum": ["standard_gauge", "narrow_gauge", "broad_gauge"],
                "description": "Track gauge specification",
            },
            "rail_usage": {
                "type": "string",
                "required": True,
                "enum": [
                    "high_speed",
                    "commuter",
                    "freight",
                    "light_rail",
                    "heritage",
                    "metro",
                ],
                "description": "Service type/purpose",
            },
            "track_type": {
                "type": "string",
                "required": True,
                "enum": ["ballasted", "slab", "viaduct", "elevated", "underground"],
                "description": "Track structure type",
            },
            "electrification": {
                "type": "boolean",
                "required": True,
                "description": "Whether track is electrified for electric trains",
            },
            "max_speed": {
                "type": "integer",
                "required": True,
                "unit": "km/h",
                "description": "Maximum design speed for trains",
            },
            "num_tracks": {
                "type": "integer",
                "required": True,
                "min": 1,
                "description": "Number of parallel tracks",
            },
            "line_length": {
                "type": "number",
                "required": False,
                "unit": "km",
                "description": "Total line length",
            },
        },
    },
    "IFC_TUNNEL": {
        "description": "Tunnel infrastructure metadata",
        "usage": "Road tunnels, rail tunnels, utility tunnels, pedestrian tunnels, metro tunnels",
        "fields": {
            "tunnel_type": {
                "type": "string",
                "required": True,
                "enum": ["road", "rail", "utility", "pedestrian", "metro", "mining"],
                "description": "Primary purpose of tunnel",
            },
            "tunnel_usage": {
                "type": "string",
                "required": False,
                "description": "Specific application (e.g., water transport, cable conduit, evacuation)",
            },
            "length": {
                "type": "number",
                "required": True,
                "min": 0,
                "unit": "m",
                "description": "Tunnel length",
            },
            "cross_section_type": {
                "type": "string",
                "required": True,
                "enum": ["circular", "horseshoe", "rectangular", "obround"],
                "description": "Cross-sectional shape",
            },
            "diameter": {
                "type": "number",
                "required": False,
                "unit": "m",
                "description": "Internal diameter (for circular tunnels)",
            },
            "width": {
                "type": "number",
                "required": False,
                "unit": "m",
                "description": "Internal width (for non-circular tunnels)",
            },
            "height": {
                "type": "number",
                "required": False,
                "unit": "m",
                "description": "Internal height (for non-circular tunnels)",
            },
            "num_lanes": {
                "type": "integer",
                "required": False,
                "description": "Number of traffic lanes (for road tunnels)",
            },
            "construction_method": {
                "type": "string",
                "required": False,
                "enum": ["drill_blast", "tbm", "cut_cover", "immersed", "open_cut"],
                "description": "Construction method used",
            },
        },
    },
    "IFC_MARINE_FACILITY": {
        "description": "Marine and port infrastructure metadata",
        "usage": "Container ports, bulk terminals, marinas, breakwaters, piers, harbors, offshore structures",
        "fields": {
            "facility_type": {
                "type": "string",
                "required": True,
                "enum": [
                    "port",
                    "pier",
                    "dock",
                    "marina",
                    "breakwater",
                    "wharf",
                    "jetty",
                    "offshore",
                ],
                "description": "Type of marine facility",
            },
            "facility_usage": {
                "type": "string",
                "required": True,
                "enum": [
                    "container",
                    "bulk_cargo",
                    "passenger",
                    "fishing",
                    "recreation",
                    "naval",
                ],
                "description": "Primary cargo/vessel type handled",
            },
            "water_depth": {
                "type": "number",
                "required": True,
                "min": 0,
                "unit": "m",
                "description": "Average water depth at facility",
            },
            "berth_count": {
                "type": "integer",
                "required": False,
                "min": 0,
                "description": "Number of vessel berths/mooring locations",
            },
            "design_vessel_size": {
                "type": "string",
                "required": False,
                "description": "Max vessel dimensions (e.g., 'Panamax', 'New Panamax', 'Post-Panamax')",
            },
            "tidal_range": {
                "type": "number",
                "required": False,
                "unit": "m",
                "description": "Difference between high and low tide",
            },
            "breakwater_length": {
                "type": "number",
                "required": False,
                "unit": "m",
                "description": "Length of protective breakwater (if applicable)",
            },
        },
    },
    "IFC_FACTORY": {
        "description": "Factory/Manufacturing facility metadata",
        "usage": "Automotive plants, electronics manufacturing, food processing, textile mills, assembly plants",
        "fields": {
            "manufacturing_type": {
                "type": "string",
                "required": True,
                "enum": [
                    "automotive",
                    "electronics",
                    "food_beverage",
                    "textiles",
                    "chemicals",
                    "machinery",
                    "pharmaceuticals",
                    "other",
                ],
                "description": "Industry sector",
            },
            "facility_usage": {
                "type": "string",
                "required": True,
                "enum": [
                    "assembly",
                    "component_production",
                    "heavy_processing",
                    "light_assembly",
                    "mixed",
                ],
                "description": "Type of manufacturing operations",
            },
            "production_capacity": {
                "type": "number",
                "required": True,
                "min": 0,
                "unit": "units/day or tonnes/day",
                "description": "Daily production output capacity",
            },
            "num_production_lines": {
                "type": "integer",
                "required": False,
                "min": 1,
                "description": "Number of parallel production lines",
            },
            "shift_schedule": {
                "type": "string",
                "required": False,
                "enum": ["single_shift", "double_shift", "triple_shift", "24_7"],
                "description": "Operating schedule",
            },
            "workforce_count": {
                "type": "integer",
                "required": False,
                "description": "Typical number of employees",
            },
            "automation_level": {
                "type": "string",
                "required": False,
                "enum": ["manual", "semi_automated", "automated", "fully_automated"],
                "description": "Degree of automation",
            },
        },
    },
    "IFC_PROCESS_PLANT": {
        "description": "Process plant infrastructure metadata",
        "usage": "Petrochemical refineries, power plants, water treatment, mining processing, chemical plants",
        "fields": {
            "process_type": {
                "type": "string",
                "required": True,
                "enum": [
                    "petrochemical",
                    "refinery",
                    "power_generation",
                    "water_treatment",
                    "mineral_processing",
                    "chemical",
                    "pharmaceutical",
                ],
                "description": "Type of industrial process",
            },
            "facility_usage": {
                "type": "string",
                "required": True,
                "description": "Specific process purpose (e.g., 'crude oil refining', 'wastewater treatment', 'coal combustion')",
            },
            "throughput": {
                "type": "number",
                "required": True,
                "min": 0,
                "unit": "bbl/day, MW, m³/day, tonnes/day",
                "description": "Daily processing capacity",
            },
            "major_equipment": {
                "type": "array",
                "required": False,
                "description": "Key process equipment (e.g., 'furnaces', 'compressors', 'reactors', 'distillation_columns')",
            },
            "hazmat_classification": {
                "type": "string",
                "required": False,
                "description": "Hazardous material classification (e.g., 'Class 1 - Explosives', 'Class 3 - Flammable')",
            },
            "environmental_controls": {
                "type": "array",
                "required": False,
                "description": "Environmental compliance systems (e.g., 'baghouses', 'scrubbers', 'cooling_towers')",
            },
        },
    },
    "IFC_DISTRIBUTION_SYSTEM": {
        "description": "Utility distribution network metadata",
        "usage": "Electrical grids, water mains, gas pipelines, district heating, sewer systems, telecommunication networks",
        "fields": {
            "system_type": {
                "type": "string",
                "required": True,
                "enum": [
                    "electrical",
                    "water",
                    "gas",
                    "sewer",
                    "stormwater",
                    "district_heating",
                    "telecom",
                    "fuel_pipeline",
                ],
                "description": "Type of utility distributed",
            },
            "system_usage": {
                "type": "string",
                "required": True,
                "description": "Distribution purpose (e.g., 'municipal water supply', 'power transmission', 'natural gas distribution')",
            },
            "network_length": {
                "type": "number",
                "required": True,
                "min": 0,
                "unit": "km",
                "description": "Total length of distribution network",
            },
            "design_capacity": {
                "type": "number",
                "required": True,
                "min": 0,
                "unit": "MW, m³/day, kW, etc.",
                "description": "Maximum design capacity",
            },
            "service_area_population": {
                "type": "integer",
                "required": False,
                "description": "Population served by this network",
            },
            "num_substations": {
                "type": "integer",
                "required": False,
                "description": "Number of distribution points (substations, pump stations, pressure regulators, etc.)",
            },
            "redundancy_type": {
                "type": "string",
                "required": False,
                "enum": ["single_line", "dual_line", "mesh", "ring"],
                "description": "Network topology for fault tolerance",
            },
        },
    },
    "IFC_SITE": {
        "description": "Site/Land development project metadata",
        "usage": "Land parcels, development sites, parks, plazas, landscaped areas, site preparation",
        "fields": {
            "site_area": {
                "type": "number",
                "required": True,
                "min": 0,
                "unit": "m²",
                "description": "Total site area",
            },
            "land_use": {
                "type": "string",
                "required": True,
                "enum": [
                    "commercial",
                    "residential",
                    "industrial",
                    "agricultural",
                    "recreational",
                    "mixed_use",
                    "public_space",
                ],
                "description": "Primary land use classification",
            },
            "site_usage": {
                "type": "string",
                "required": True,
                "description": "Specific usage (e.g., 'shopping center', 'residential development', 'public park', 'industrial zone')",
            },
            "zoning": {
                "type": "string",
                "required": False,
                "description": "Local zoning designation/code",
            },
            "site_slope": {
                "type": "string",
                "required": False,
                "enum": ["flat", "gentle", "moderate", "steep"],
                "description": "Terrain gradient",
            },
            "existing_structures": {
                "type": "boolean",
                "required": False,
                "description": "Whether site has existing buildings (greenfield vs brownfield)",
            },
            "parking_spaces": {
                "type": "integer",
                "required": False,
                "description": "Designed number of parking spaces",
            },
        },
    },
    "OTHER": {
        "description": "Custom project type metadata",
        "usage": "Non-standard project types not covered by predefined categories",
        "fields": {
            "project_category": {
                "type": "string",
                "required": True,
                "description": "Custom category name (free text)",
            },
            "custom_fields": {
                "type": "object",
                "required": False,
                "description": "Any custom key-value pairs relevant to project",
            },
        },
    },
}


def validate_type_metadata(project_type, type_metadata):
    """
    Validate type_metadata against the schema for a given project_type.

    Args:
        project_type (str): Project type code (e.g., 'IFC_BUILDING')
        type_metadata (dict): The metadata to validate

    Returns:
        tuple: (is_valid, errors_list)
        - is_valid (bool): True if valid, False otherwise
        - errors_list (list): List of error messages if invalid

    Raises:
        ValueError: If project_type is not recognized
    """
    if project_type not in PROJECT_TYPE_SCHEMAS:
        raise ValueError(f"Unknown project type: {project_type}")

    schema = PROJECT_TYPE_SCHEMAS[project_type]
    errors = []

    # Check required fields
    for field_name, field_spec in schema["fields"].items():
        if field_spec.get("required", False) and field_name not in type_metadata:
            errors.append(f"Missing required field: {field_name}")

        # Validate field type if present
        if field_name in type_metadata:
            value = type_metadata[field_name]
            field_type = field_spec.get("type")

            # Type validation
            if field_type == "string" and not isinstance(value, str):
                errors.append(
                    f"Field '{field_name}' must be a string, got {type(value).__name__}"
                )

            elif field_type == "integer" and not isinstance(value, int):
                errors.append(
                    f"Field '{field_name}' must be an integer, got {type(value).__name__}"
                )

            elif field_type == "number" and not isinstance(value, (int, float)):
                errors.append(
                    f"Field '{field_name}' must be a number, got {type(value).__name__}"
                )

            elif field_type == "boolean" and not isinstance(value, bool):
                errors.append(
                    f"Field '{field_name}' must be a boolean, got {type(value).__name__}"
                )

            elif field_type == "array" and not isinstance(value, list):
                errors.append(
                    f"Field '{field_name}' must be an array, got {type(value).__name__}"
                )

            # Enum validation
            if "enum" in field_spec and value not in field_spec["enum"]:
                errors.append(
                    f"Field '{field_name}' value '{value}' not in allowed values: {field_spec['enum']}"
                )

            # Min/max validation for numbers
            if field_type in ("integer", "number"):
                if "min" in field_spec and value < field_spec["min"]:
                    errors.append(
                        f"Field '{field_name}' must be >= {field_spec['min']}, got {value}"
                    )
                if "max" in field_spec and value > field_spec["max"]:
                    errors.append(
                        f"Field '{field_name}' must be <= {field_spec['max']}, got {value}"
                    )

    return len(errors) == 0, errors


def get_project_type_schema(project_type):
    """
    Get the schema definition for a specific project type.

    Args:
        project_type (str): Project type code

    Returns:
        dict: Schema definition or None if not found
    """
    return PROJECT_TYPE_SCHEMAS.get(project_type)
