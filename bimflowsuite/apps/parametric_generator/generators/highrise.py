from ifcopenshell import file as ifc_file, util
import uuid

def generate_highrise_ifc(spec_json):
    ifc = ifc_file(schema="IFC4X3")
    
    project = ifc.createIfcProject(ifc.guid.compress(uuid.uuid4()), "Highrise Project")
    site = ifc.createIfcSite(ifc.guid.compress(uuid.uuid4()), "Highrise Site")
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [site], project)
    
    highrise = ifc.createIfcBuilding(ifc.guid.compress(uuid.uuid4()), "Office Highrise")
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [highrise], site)
    
    floors = spec_json.get('total_floors', 20)
    height_per_floor = 3.5
    for i in range(floors):
        storey = ifc.createIfcBuildingStorey(ifc.guid.compress(uuid.uuid4()), f"Floor {i+1}", None, i * height_per_floor)
        ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [storey], highrise)
    
    cores = spec_json.get('core_count', 1)
    for c in range(cores):
        core = ifc.createIfcSpace(ifc.guid.compress(uuid.uuid4()), f"Core {c+1}", "CORE")
        ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [core], highrise)
    
    facade = ifc.createIfcCurtainWall(ifc.guid.compress(uuid.uuid4()), "Glass Facade")
    # Simple polyline for facade
    poly = ifc.createIfcPolyline([ifc.createIfcCartesianPoint(0,0,0), ifc.createIfcCartesianPoint(0,0,floors*height_per_floor)])
    rep = ifc.createIfcShapeRepresentation(ifc.createIfcGeometricRepresentationContext(), "Axis", "Polyline", [poly])
    facade.Representation = rep
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [facade], highrise)
    
    pset = ifc.createIfcPropertySet(ifc.guid.compress(uuid.uuid4()), "Pset_CurtainWallCommon", None)
    facade_prop = ifc.createIfcPropertySingleValue("FacadeType", None, ifc.createIfcLabel(spec_json.get('facade_type', 'glass')), None)
    ifc.createIfcRelDefinesByProperties(None, None, None, [facade], pset)
    pset.HasProperties = [facade_prop]

    return ifc.to_string()