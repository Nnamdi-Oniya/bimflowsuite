from ifcopenshell import file as ifc_file, util
import uuid


def generate_highrise_ifc(project, specifications):
    """
    Generate highrise building IFC from project metadata and specifications.
    Args:
        project: Project model instance with metadata
        specifications: Dict with generation specs (total_floors, core_count, facade_type, etc.)
    """
    ifc = ifc_file(schema="IFC4X3")

    project_ifc = ifc.createIfcProject(
        ifc.guid.compress(uuid.uuid4()), project.name or "Highrise Project"
    )
    site = ifc.createIfcSite(
        ifc.guid.compress(uuid.uuid4()), project.location or "Highrise Site"
    )
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [site], project_ifc
    )

    highrise = ifc.createIfcBuilding(
        ifc.guid.compress(uuid.uuid4()), project.name or "Office Highrise"
    )
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [highrise], site
    )

    floors = specifications.get("total_floors", project.stories or 20)
    height_per_floor = 3.5
    for i in range(floors):
        storey = ifc.createIfcBuildingStorey(
            ifc.guid.compress(uuid.uuid4()),
            f"Floor {i + 1}",
            None,
            i * height_per_floor,
        )
        ifc.createIfcRelAggregates(
            ifc.guid.compress(uuid.uuid4()), None, None, None, [storey], highrise
        )

    cores = specifications.get("core_count", 1)
    for c in range(cores):
        core = ifc.createIfcSpace(
            ifc.guid.compress(uuid.uuid4()), f"Core {c + 1}", "CORE"
        )
        ifc.createIfcRelAggregates(
            ifc.guid.compress(uuid.uuid4()), None, None, None, [core], highrise
        )

    facade = ifc.createIfcCurtainWall(ifc.guid.compress(uuid.uuid4()), "Glass Facade")
    # Simple polyline for facade
    poly = ifc.createIfcPolyline(
        [
            ifc.createIfcCartesianPoint(0, 0, 0),
            ifc.createIfcCartesianPoint(0, 0, floors * height_per_floor),
        ]
    )
    rep = ifc.createIfcShapeRepresentation(
        ifc.createIfcGeometricRepresentationContext(), "Axis", "Polyline", [poly]
    )
    facade.Representation = rep
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [facade], highrise
    )

    pset = ifc.createIfcPropertySet(
        ifc.guid.compress(uuid.uuid4()), "Pset_CurtainWallCommon", None
    )
    facade_prop = ifc.createIfcPropertySingleValue(
        "FacadeType",
        None,
        ifc.createIfcLabel(specifications.get("facade_type", "glass")),
        None,
    )
    ifc.createIfcRelDefinesByProperties(None, None, None, [facade], pset)
    pset.HasProperties = [facade_prop]

    return ifc.to_string()
