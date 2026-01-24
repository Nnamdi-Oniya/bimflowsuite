from ifcopenshell import file as ifc_file, util
import uuid


def generate_road_ifc(project, specifications):
    """
    Generate road IFC from project metadata and specifications.
    Args:
        project: Project model instance with metadata
        specifications: Dict with generation specs (alignment_length, lanes, crossfall, etc.)
    """
    ifc = ifc_file(schema="IFC4X3")

    project_ifc = ifc.createIfcProject(
        ifc.guid.compress(uuid.uuid4()), project.name or "Road Project"
    )
    site = ifc.createIfcSite(
        ifc.guid.compress(uuid.uuid4()), project.location or "Road Site"
    )
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [site], project_ifc
    )

    road = ifc.createIfcRoad(
        ifc.guid.compress(uuid.uuid4()), project.name or "Highway Road"
    )
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [road], site
    )

    length = specifications.get("alignment_length", project.length or 1000)
    alignment = ifc.createIfcAlignment(
        ifc.guid.compress(uuid.uuid4()), "Road Alignment"
    )
    # Add segment curve
    curve = ifc.createIfcCompositeCurve(
        [
            [
                ifc.createIfcPolyline(
                    [
                        [ifc.createIfcCartesianPoint(0, 0, 0)],
                        [ifc.createIfcCartesianPoint(length, 0, 0)],
                    ]
                )
            ]
        ]
    )
    segment = ifc.createIfcAlignmentSegment(
        ifc.guid.compress(uuid.uuid4()), f"Segment 1", curve
    )
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [segment], alignment
    )

    lanes = specifications.get("lanes", project.lanes or 2)
    for i in range(lanes):
        lane = ifc.createIfcRoadSegment(
            ifc.guid.compress(uuid.uuid4()), f"Lane {i + 1}"
        )
        ifc.createIfcRelAggregates(
            ifc.guid.compress(uuid.uuid4()), None, None, None, [lane], road
        )

    pset = ifc.createIfcPropertySet(
        ifc.guid.compress(uuid.uuid4()), "Pset_RoadCommon", None
    )
    crossfall_prop = ifc.createIfcPropertySingleValue(
        "Crossfall", None, ifc.createIfcReal(specifications.get("crossfall", 2.0)), None
    )
    ifc.createIfcRelDefinesByProperties(None, None, None, [road], pset)
    pset.HasProperties = [crossfall_prop]

    return ifc.to_string()
