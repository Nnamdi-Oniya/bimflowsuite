"""
Building Generator

Specializes the base IFC generator for building projects with
structural analysis properties, building systems, and MEP networks.
Supports IFC2X3, IFC4, and IFC4X3 schema versions.
"""

from .base import BaseIFCGenerator
from ifcopenshell import guid
import logging

logger = logging.getLogger(__name__)


class BuildingIFCGenerator(BaseIFCGenerator):
    """Generate IFC for building projects."""

    def generate(self):
        """Generate building IFC with specialized properties."""
        ifc_string = super().generate()
        self.customize()
        return ifc_string

    def customize(self):
        """Add building-specific properties."""
        try:
            # Add structural analysis properties to beams/columns
            for asset_id, ifc_elem in self.element_map.items():
                if not asset_id.startswith("asset_"):
                    continue

                # Add structural properties
                self._add_structural_properties(ifc_elem)

            logger.info("Building customization complete")

        except Exception as e:
            logger.warning(f"Building customization error: {str(e)}")

    def _add_structural_properties(self, ifc_element):
        """Add AISC/EC structural analysis properties."""
        try:
            # Check element type
            elem_type = ifc_element.is_a()

            if "Beam" in elem_type or "Column" in elem_type:
                # Create structural pset
                pset = self.ifc.createIfcPropertySet(
                    guid.new(),
                    Name="Pset_StructuralAnalysisProperties",
                    HasProperties=[],
                )

                # Add standard structural properties
                props = [
                    ("Material", "Steel"),
                    ("YieldStrength", "250"),  # MPa
                    ("ElasticModulus", "210000"),  # MPa
                    ("Density", "7850"),  # kg/m3
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
            logger.debug(f"Structural property error: {str(e)}")
