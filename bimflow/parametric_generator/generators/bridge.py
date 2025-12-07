from ifcopenshell import file as ifc_file, util
import uuid

def generate_bridge_ifc(spec_json):
    ifc = ifc_file(schema="IFC4X3")
    
    project = ifc.createIfcProject(ifc.guid.compress(uuid.uuid4()), "Bridge Project")
    site = ifc.createIfcSite(ifc.guid.compress(uuid.uuid4()), "Bridge Site")
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [site], project)
    
    bridge = ifc.createIfcBridge(ifc.guid.compress(uuid.uuid4()), "Highway Bridge")
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [bridge], site)
    
    span_length = spec_json.get('span_length', 50)
    piers = spec_json.get('piers', 2)
    for i in range(piers + 1):
        pier = ifc.createIfcColumn(ifc.guid.compress(uuid.uuid4()), f"Pier {i+1}")
        profile = ifc.createIfcCircleProfileDef(None, None, 1.0)
        extrusion = ifc.createIfcExtrudedAreaSolid(profile, ifc.createIfcAxis2Placement2D(), span_length / (piers + 1))
        rep = ifc.createIfcShapeRepresentation(ifc.createIfcGeometricRepresentationContext(), "Body", "SweptSolid", [extrusion])
        pier.Representation = rep
        ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [pier], bridge)
    
    deck = ifc.createIfcSlab(ifc.guid.compress(uuid.uuid4()), "Bridge Deck", "ROOF")
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [deck], bridge)
    
    pset = ifc.createIfcPropertySet(ifc.guid.compress(uuid.uuid4()), "Pset_BridgeCommon", None)
    load_prop = ifc.createIfcPropertySingleValue("LoadClass", None, ifc.createIfcLabel(spec_json.get('load_class', 'A')), None)
    ifc.createIfcRelDefinesByProperties(None, None, None, [bridge], pset)
    pset.HasProperties = [load_prop]

    return ifc.to_string()