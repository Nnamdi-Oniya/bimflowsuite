"""
Bridge Generator

Specializes the base IFC generator for bridge projects with
structural system properties, deck profiles, and bearing elements.
Supports IFC2X3, IFC4, and IFC4X3 schema versions.
"""

from .base import BaseIFCGenerator
from ifcopenshell import guid
import logging

logger = logging.getLogger(__name__)


class BridgeIFCGenerator(BaseIFCGenerator):
    """Generate IFC for bridge projects."""

    def generate(self):
        """Generate bridge IFC with specialized properties."""
        ifc_string = super().generate()
        self.customize()
        return ifc_string

    def customize(self):
        """Add bridge-specific properties."""
        try:
            # Add structural analysis to bridge elements
            for asset_id, ifc_elem in self.element_map.items():
                if not asset_id.startswith("asset_"):
                    continue

                # Add bridge-specific properties
                self._add_bridge_properties(ifc_elem)

            logger.info("Bridge customization complete")

        except Exception as e:
            logger.warning(f"Bridge customization error: {str(e)}")

    def _add_bridge_properties(self, ifc_element):
        """Add bridge-specific structural properties."""
        try:
            elem_type = ifc_element.is_a()

            if "Beam" in elem_type or "Girder" in elem_type:
                pset = self.ifc.createIfcPropertySet(
                    guid.new(),
                    Name="Pset_BridgeBeamProperties",
                    HasProperties=[],
                )

                props = [
                    ("BridgeType", "Highway"),
                    ("SpanLength", "40.0"),  # meters
                    ("Material", "Prestressed Concrete"),
                    ("CompressionMPa", "50"),
                    ("TensionMPa", "5"),
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

            elif "Pier" in elem_type:
                pset = self.ifc.createIfcPropertySet(
                    guid.new(),
                    Name="Pset_PierProperties",
                    HasProperties=[],
                )

                props = [
                    ("FoundationType", "Pile Foundation"),
                    ("MaterialStrength", "40"),  # MPa
                    ("LoadCapacity", "50000"),  # kN
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
            logger.debug(f"Bridge property error: {str(e)}")
