from ifcopenshell import file as ifc_file, util
import uuid


def generate_bridge_ifc(project, specifications):
    """
    Generate bridge IFC from project metadata and specifications.
    Args:
        project: Project model instance with metadata
        specifications: Dict with generation specs (span_length, piers, load_class, etc.)
    """
    ifc = ifc_file(schema="IFC4X3")

    project_ifc = ifc.createIfcProject(
        ifc.guid.compress(uuid.uuid4()), project.name or "Bridge Project"
    )
    site = ifc.createIfcSite(
        ifc.guid.compress(uuid.uuid4()), project.location or "Bridge Site"
    )
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [site], project_ifc
    )

    bridge = ifc.createIfcBridge(
        ifc.guid.compress(uuid.uuid4()), project.name or "Highway Bridge"
    )
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [bridge], site
    )

    span_length = specifications.get("span_length", project.span or 50)
    piers = specifications.get("piers", 2)
    for i in range(piers + 1):
        pier = ifc.createIfcColumn(ifc.guid.compress(uuid.uuid4()), f"Pier {i + 1}")
        profile = ifc.createIfcCircleProfileDef(None, None, 1.0)
        extrusion = ifc.createIfcExtrudedAreaSolid(
            profile, ifc.createIfcAxis2Placement2D(), span_length / (piers + 1)
        )
        rep = ifc.createIfcShapeRepresentation(
            ifc.createIfcGeometricRepresentationContext(),
            "Body",
            "SweptSolid",
            [extrusion],
        )
        pier.Representation = rep
        ifc.createIfcRelAggregates(
            ifc.guid.compress(uuid.uuid4()), None, None, None, [pier], bridge
        )

    deck = ifc.createIfcSlab(ifc.guid.compress(uuid.uuid4()), "Bridge Deck", "ROOF")
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [deck], bridge
    )

    pset = ifc.createIfcPropertySet(
        ifc.guid.compress(uuid.uuid4()), "Pset_BridgeCommon", None
    )
    load_prop = ifc.createIfcPropertySingleValue(
        "LoadClass",
        None,
        ifc.createIfcLabel(specifications.get("load_class", "A")),
        None,
    )
    ifc.createIfcRelDefinesByProperties(None, None, None, [bridge], pset)
    pset.HasProperties = [load_prop]

    return ifc.to_string()
