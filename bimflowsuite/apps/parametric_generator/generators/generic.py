from ifcopenshell import file as ifc_file
import uuid


def generate_generic_ifc(project, specifications):
    """
    Fallback generator for unsupported asset types.
    Creates a basic IFC skeleton (project + site + placeholder element).
    Args:
        project: Project model instance with metadata
        specifications: Dict with generation specs (dimensions, asset_type_code, etc.)
    """
    ifc = ifc_file(schema="IFC4X3")

    # Boilerplate: Project & Site
    asset_type_code = specifications.get("asset_type_code", "unknown")
    project_ifc = ifc.createIfcProject(
        ifc.guid.compress(uuid.uuid4()),
        project.name or f"{asset_type_code.capitalize()} Project",
    )
    site = ifc.createIfcSite(
        ifc.guid.compress(uuid.uuid4()),
        project.location or f"{asset_type_code.capitalize()} Site",
    )
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [site], project_ifc
    )

    # Placeholder element
    placeholder = ifc.createIfcBuildingElementProxy(
        ifc.guid.compress(uuid.uuid4()),
        f"{asset_type_code.capitalize()} Placeholder",
        "NOTDEFINED",
    )
    ifc.createIfcRelAggregates(
        ifc.guid.compress(uuid.uuid4()), None, None, None, [placeholder], site
    )

    # Pset with spec hints
    pset = ifc.createIfcPropertySet(
        ifc.guid.compress(uuid.uuid4()),
        f"Pset_{asset_type_code.capitalize()}Common",
        None,
    )
    type_prop = ifc.createIfcPropertySingleValue(
        "AssetType", None, ifc.createIfcLabel(asset_type_code), None
    )
    ifc.createIfcRelDefinesByProperties(None, None, None, [placeholder], pset)
    pset.HasProperties = [type_prop]

    # Add spec dimensions as props
    for key, value in specifications.get("dimensions", {}).items():
        dim_prop = ifc.createIfcPropertySingleValue(
            key.capitalize(), None, ifc.createIfcReal(float(value)), None
        )
        pset.HasProperties.append(dim_prop)

    stub_note = f"Stub generated for {asset_type_code}; extend with custom geometry in generators/{asset_type_code}.py"
    print(stub_note)  # Log in terminal

    return ifc.to_string()
