from ifcopenshell import file as ifc_file, util
import uuid

def generate_tunnel_ifc(spec_json):
    """
    Example full generator for 'tunnel' (extend similarly for others).
    """
    ifc = ifc_file(schema="IFC4X3")
    
    project = ifc.createIfcProject(ifc.guid.compress(uuid.uuid4()), "Tunnel Project")
    site = ifc.createIfcSite(ifc.guid.compress(uuid.uuid4()), "Tunnel Site")
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [site], project)
    
    tunnel = ifc.createIfcTunnel(ifc.guid.compress(uuid.uuid4()), "Subway Tunnel")  # IFC4.3 infra type
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [tunnel], site)
    
    length = spec_json.get('length', 500)
    # Simple alignment for tunnel
    alignment = ifc.createIfcAlignment(ifc.guid.compress(uuid.uuid4()), "Tunnel Alignment")
    curve = ifc.createIfcPolyline([[ifc.createIfcCartesianPoint(0,0,0)], [ifc.createIfcCartesianPoint(length,0,-10)]])  # Slight grade
    segment = ifc.createIfcAlignmentSegment(ifc.guid.compress(uuid.uuid4()), "Tunnel Segment", curve)
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [segment], alignment)
    
    # Lining wall (example element)
    lining = ifc.createIfcWall(ifc.guid.compress(uuid.uuid4()), "Tunnel Lining")
    profile = ifc.createIfcCircleProfileDef(None, None, spec_json.get('diameter', 5.0))  # Radius
    extrusion = ifc.createIfcExtrudedAreaSolid(profile, ifc.createIfcAxis2Placement2D(), length)
    rep = ifc.createIfcShapeRepresentation(ifc.createIfcGeometricRepresentationContext(), "Body", "SweptSolid", [extrusion])
    lining.Representation = rep
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [lining], tunnel)
    
    # Pset
    pset = ifc.createIfcPropertySet(ifc.guid.compress(uuid.uuid4()), "Pset_TunnelCommon", None)
    mat_prop = ifc.createIfcPropertySingleValue("Material", None, ifc.createIfcLabel(spec_json.get('materials', {}).get('lining', 'reinforced_concrete')), None)
    ifc.createIfcRelDefinesByProperties(None, None, None, [tunnel], pset)
    pset.HasProperties = [mat_prop]

    return ifc.to_string()