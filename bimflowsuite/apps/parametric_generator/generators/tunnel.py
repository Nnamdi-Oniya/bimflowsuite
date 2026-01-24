from ifcopenshell import file as ifc_file, util
import uuid


def generate_tunnel_ifc(project, specifications):
    """
    Generate tunnel IFC from project metadata and specifications.
    Args:
        project: Project model instance with metadata
        specifications: Dict with generation specs (length, diameter, materials, etc.)
    """
    ifc = ifc_file(schema="IFC4X3")

    project_ifc = ifc.createIfcProject(
        ifc.guid.compress(uuid.uuid4()), project.name or "Tunnel Project"
    )
    site = ifc.createIfcSite(
        ifc.guid.compress(uuid.uuid4()), project.location or "Tunnel Site"
    )
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [site], project_ifc
    )

    tunnel = ifc.createIfcTunnel(
        ifc.guid.compress(uuid.uuid4()), project.name or "Subway Tunnel"
    )  # IFC4.3 infra type
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [tunnel], site
    )

    length = specifications.get("length", project.length or 500)
    # Simple alignment for tunnel
    alignment = ifc.createIfcAlignment(
        ifc.guid.compress(uuid.uuid4()), "Tunnel Alignment"
    )
    curve = ifc.createIfcPolyline(
        [
            [ifc.createIfcCartesianPoint(0, 0, 0)],
            [ifc.createIfcCartesianPoint(length, 0, -10)],
        ]
    )  # Slight grade
    segment = ifc.createIfcAlignmentSegment(
        ifc.guid.compress(uuid.uuid4()), "Tunnel Segment", curve
    )
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [segment], alignment
    )

    # Lining wall (example element)
    lining = ifc.createIfcWall(ifc.guid.compress(uuid.uuid4()), "Tunnel Lining")
    profile = ifc.createIfcCircleProfileDef(
        None, None, specifications.get("diameter", 5.0)
    )  # Radius
    extrusion = ifc.createIfcExtrudedAreaSolid(
        profile, ifc.createIfcAxis2Placement2D(), length
    )
    rep = ifc.createIfcShapeRepresentation(
        ifc.createIfcGeometricRepresentationContext(), "Body", "SweptSolid", [extrusion]
    )
    lining.Representation = rep
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [lining], tunnel
    )

    # Pset
    pset = ifc.createIfcPropertySet(
        ifc.guid.compress(uuid.uuid4()), "Pset_TunnelCommon", None
    )
    mat_prop = ifc.createIfcPropertySingleValue(
        "Material",
        None,
        ifc.createIfcLabel(
            specifications.get("materials", {}).get(
                "lining", project.structural_frame or "reinforced_concrete"
            )
        ),
        None,
    )
    ifc.createIfcRelDefinesByProperties(None, None, None, [tunnel], pset)
    pset.HasProperties = [mat_prop]

    return ifc.to_string()
