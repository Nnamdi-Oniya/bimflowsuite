from ifcopenshell import file as ifc_file, util
import uuid

def generate_road_ifc(spec_json):
    ifc = ifc_file(schema="IFC4X3")
    
    project = ifc.createIfcProject(ifc.guid.compress(uuid.uuid4()), "Road Project")
    site = ifc.createIfcSite(ifc.guid.compress(uuid.uuid4()), "Road Site")
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [site], project)
    
    road = ifc.createIfcRoad(ifc.guid.compress(uuid.uuid4()), "Highway Road")
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [road], site)
    
    length = spec_json.get('alignment_length', 1000)
    alignment = ifc.createIfcAlignment(ifc.guid.compress(uuid.uuid4()), "Road Alignment")
    # Add segment curve
    curve = ifc.createIfcCompositeCurve([[ifc.createIfcPolyline([[ifc.createIfcCartesianPoint(0,0,0)], [ifc.createIfcCartesianPoint(length,0,0)]])]])
    segment = ifc.createIfcAlignmentSegment(ifc.guid.compress(uuid.uuid4()), f"Segment 1", curve)
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [segment], alignment)
    
    lanes = spec_json.get('lanes', 2)
    for i in range(lanes):
        lane = ifc.createIfcRoadSegment(ifc.guid.compress(uuid.uuid4()), f"Lane {i+1}")
        ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [lane], road)
    
    pset = ifc.createIfcPropertySet(ifc.guid.compress(uuid.uuid4()), "Pset_RoadCommon", None)
    crossfall_prop = ifc.createIfcPropertySingleValue("Crossfall", None, ifc.createIfcReal(spec_json.get('crossfall', 2.0)), None)
    ifc.createIfcRelDefinesByProperties(None, None, None, [road], pset)
    pset.HasProperties = [crossfall_prop]

    return ifc.to_string()