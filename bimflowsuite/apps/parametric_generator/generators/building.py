from ifcopenshell import file as ifc_file, util
import uuid

def generate_building_ifc(spec_json):
    ifc = ifc_file(schema="IFC4X3")
    
    # Project/Site boilerplate
    project = ifc.createIfcProject(ifc.guid.compress(uuid.uuid4()), "Building Project")
    site = ifc.createIfcSite(ifc.guid.compress(uuid.uuid4()), "Site")
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [site], project)
    
    # Building with basic swept solid for walls
    building = ifc.createIfcBuilding(ifc.guid.compress(uuid.uuid4()), "Office Building")
    ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [building], site)
    
    floors = spec_json.get('floors', 1)
    height_per_floor = spec_json.get('height', 15) / floors
    for i in range(floors):
        storey = ifc.createIfcBuildingStorey(ifc.guid.compress(uuid.uuid4()), f"Floor {i+1}", None, i * height_per_floor)
        ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [storey], building)
        
        # Wall with extrusion (simple rect)
        wall = ifc.createIfcWall(ifc.guid.compress(uuid.uuid4()), "Exterior Wall")
        # Add representation: SweptAreaSolid
        profile = ifc.createIfcRectangleProfileDef(None, None, 0.2, 3.0)  # Thickness x height
        extrusion = ifc.createIfcExtrudedAreaSolid(profile, ifc.createIfcAxis2Placement2D(), 10.0)  # Length
        rep = ifc.createIfcShapeRepresentation(ifc.createIfcGeometricRepresentationContext(), "Body", "SweptSolid", [extrusion])
        wall.Representation = rep
        ifc.createIfcRelAggregates(ifc.guid.compress(uuid.uuid4()), None, None, None, [wall], storey)
        
        # Pset
        pset = ifc.createIfcPropertySet(ifc.guid.compress(uuid.uuid4()), "Pset_WallCommon", None)
        mat_prop = ifc.createIfcPropertySingleValue("Material", None, ifc.createIfcLabel(spec_json.get('materials', {}).get('wall', 'concrete')), None)
        ifc.createIfcRelDefinesByProperties(None, None, None, [wall], pset)
        pset.HasProperties = [mat_prop]

    return ifc.to_string()  # Enhanced with geometry for clashes