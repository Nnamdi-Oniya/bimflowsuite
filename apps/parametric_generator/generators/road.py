"""
Road Generator

Specializes the base IFC generator for road projects with
pavement layers, surface properties, and linear referencing systems.
Supports IFC2X3, IFC4, and IFC4X3 schema versions.
"""

from .base import BaseIFCGenerator
from ifcopenshell import guid
import logging

logger = logging.getLogger(__name__)


class RoadIFCGenerator(BaseIFCGenerator):
    """Generate IFC for road infrastructure projects."""

    def generate(self):
        """Generate road IFC with specialized properties."""
        ifc_string = super().generate()
        self.customize()
        return ifc_string

    def customize(self):
        """Add road-specific properties."""
        try:
            # Add pavement and surface properties
            for asset_id, ifc_elem in self.element_map.items():
                if not asset_id.startswith("asset_"):
                    continue

                # Add road-specific properties
                self._add_road_properties(ifc_elem)

            logger.info("Road customization complete")

        except Exception as e:
            logger.warning(f"Road customization error: {str(e)}")

    def _add_road_properties(self, ifc_element):
        """Add road-specific pavement and surface properties."""
        try:
            elem_type = ifc_element.is_a()

            if "Pavement" in elem_type:
                pset = self.ifc.createIfcPropertySet(
                    guid.new(),
                    Name="Pset_PavementProperties",
                    HasProperties=[],
                )

                props = [
                    ("PavementType", "Asphalt Concrete"),
                    ("ThicknessMillimeters", "200"),
                    ("BinderType", "AC-20"),
                    ("CompactionDegree", "98"),  # Percent
                ]

                for prop_name, prop_value in props:
                    prop = self.ifc.createIfcPropertySingleValue(
                        Name=prop_name,
                        NominalValue=self.ifc.createIfcLabel(str(prop_value)),
                    )
                    pset.HasProperties = list(pset.HasProperties or []) + [prop]

                if pset.HasProperties:
                    self.ifc.createIfcRelDefinesByProperties(
                        guid.new(),
                        RelatedObjects=[ifc_element],
                        RelatingPropertyDefinition=pset,
                    )

                # Add sub-layer structure
                self._add_road_layers(ifc_element)

            elif "Marking" in elem_type or "Curb" in elem_type:
                pset = self.ifc.createIfcPropertySet(
                    guid.new(),
                    Name="Pset_RoadAccessoryProperties",
                    HasProperties=[],
                )

                props = [
                    ("AccessoryType", elem_type),
                    ("Material", "Concrete"),
                    ("DesignStandard", "EN 124"),
                ]

                for prop_name, prop_value in props:
                    prop = self.ifc.createIfcPropertySingleValue(
                        Name=prop_name,
                        NominalValue=self.ifc.createIfcLabel(str(prop_value)),
                    )
                    pset.HasProperties = list(pset.HasProperties or []) + [prop]

                if pset.HasProperties:
                    self.ifc.createIfcRelDefinesByProperties(
                        guid.new(),
                        RelatedObjects=[ifc_element],
                        RelatingPropertyDefinition=pset,
                    )

        except Exception as e:
            logger.debug(f"Road property error: {str(e)}")

    def _add_road_layers(self, pavement_element):
        """Add pavement layer structure (base course, binder, surface)."""
        try:
            layers = [
                ("Subgrade", "Soil", "250"),
                ("BaseLayer", "Aggregate", "300"),
                ("BinderLayer", "AC-20", "100"),
                ("SurfaceLayer", "AC-10", "50"),
            ]

            for layer_name, material, thickness in layers:
                layer_elem = self.ifc.createIfcBuildingElementProxy(
                    guid.new(),
                    Name=layer_name,
                    Description=f"{material} layer - {thickness}mm",
                    ObjectPlacement=self._create_local_placement(),
                )

                # Add layer properties
                pset = self.ifc.createIfcPropertySet(
                    guid.new(),
                    Name="Pset_LayerProperties",
                    HasProperties=[],
                )

                layer_props = [
                    ("LayerMaterial", material),
                    ("ThicknessMillimeters", thickness),
                    ("Compaction", "95"),
                ]

                for prop_name, prop_value in layer_props:
                    prop = self.ifc.createIfcPropertySingleValue(
                        Name=prop_name,
                        NominalValue=self.ifc.createIfcLabel(str(prop_value)),
                    )
                    pset.HasProperties = list(pset.HasProperties or []) + [prop]

                if pset.HasProperties:
                    self.ifc.createIfcRelDefinesByProperties(
                        guid.new(),
                        RelatedObjects=[layer_elem],
                        RelatingPropertyDefinition=pset,
                    )

        except Exception as e:
            logger.debug(f"Road layer error: {str(e)}")


def generate_road_ifc(project, specifications):
    """
    Backward-compatible function API used by view-layer generator_map.

    Resolves the site from specifications.site_id or falls back to the
    project's first site, then delegates to RoadIFCGenerator.
    """
    site_id = (specifications or {}).get("site_id")
    sites = project.sites.all()
    if site_id:
        sites = sites.filter(id=site_id)
    site = sites.order_by("created_at").first()
    if site is None:
        raise ValueError(
            f"No site found for project {project.id}. "
            "Provide specifications.site_id or create a site first."
        )

    generator = RoadIFCGenerator(site)
    return generator.generate()
