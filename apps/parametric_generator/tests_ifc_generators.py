"""
Tests for IFC4X3 Generators

Verifies that generators correctly convert SpatialStructure and Asset models
into valid IFC4X3 files with proper entity hierarchies and property sets.
"""

import pytest
from datetime import datetime
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone

from apps.parametric_generator.models import Project, Site, SpatialStructure, Element
from apps.parametric_generator.generators.building_ifc4 import BuildingIFCGenerator
from apps.parametric_generator.generators.bridge_ifc4 import BridgeIFCGenerator
from apps.parametric_generator.generators.road_ifc4 import RoadIFCGenerator


class BaseGeneratorTestCase(TestCase):
    """Base test case with common setup for all generator tests"""

    @classmethod
    def setUpTestData(cls):
        """Create shared test data"""
        # Create organization and user (can be mocked if needed)
        cls.project = Project.objects.create(
            name="Test Project",
            project_number="TEST-001",
            project_type="BUILDING",
            phase="detailed",
            description="Test project for IFC generation",
        )

    def create_site(self, project_type, site_name="Test Site"):
        """Helper to create a test site"""
        return Site.objects.create(
            project=self.project,
            site_name=site_name,
            project_type=project_type,
            address="123 Main St",
            latitude=Decimal("40.7128"),
            longitude=Decimal("-74.0060"),
            elevation=Decimal("10.5"),
            true_north_angle=Decimal("0"),
            project_north_angle=Decimal("0"),
            length_unit="m",
            area_unit="m2",
            volume_unit="m3",
            angle_unit="degree",
            ifc_schema_version="ifc4x3",
            coordinate_reference_system="epsg:4326",
            precision=Decimal("0.0001"),
        )

    def create_spatial_structure(self, site, spatial_type, name, parent=None, level=0):
        """Helper to create spatial structure"""
        return SpatialStructure.objects.create(
            site=site,
            spatial_type=spatial_type,
            name=name,
            parent=parent,
            level=level,
            properties={},
        )

    def create_asset(self, spatial_structure, asset_type, name, properties=None):
        """Helper to create asset"""
        if properties is None:
            properties = {}
        return Element.objects.create(
            spatial_structure=spatial_structure,
            site=spatial_structure.site,
            asset_type=asset_type,
            name=name,
            properties=properties,
        )


class BuildingGeneratorTests(BaseGeneratorTestCase):
    """Tests for BuildingIFCGenerator"""

    def setUp(self):
        """Set up for each test"""
        self.site = self.create_site("BUILDING")
        self.project.project_type = "BUILDING"
        self.project.save()

    def test_generator_initialization(self):
        """Test that generator initializes correctly"""
        generator = BuildingIFCGenerator(self.site)
        self.assertIsNotNone(generator.site)
        self.assertEqual(generator.site.id, self.site.id)

    def test_empty_site_generation(self):
        """Test IFC generation for site with no structures or assets"""
        generator = BuildingIFCGenerator(self.site)
        ifc_string = generator.generate()

        # Verify output is valid IFC
        self.assertIsInstance(ifc_string, str)
        self.assertIn("ISO-10303-21", ifc_string)
        self.assertIn("IfcProject", ifc_string)
        self.assertIn("IfcSite", ifc_string)

    def test_building_hierarchy_generation(self):
        """Test generation of proper IFC building hierarchy"""
        # Create building hierarchy
        building = self.create_spatial_structure(
            self.site, "ifc_building", "Main Building"
        )
        storey1 = self.create_spatial_structure(
            self.site,
            "ifc_building_storey",
            "Ground Floor",
            parent=building,
            level=1,
        )
        storey2 = self.create_spatial_structure(
            self.site,
            "ifc_building_storey",
            "First Floor",
            parent=building,
            level=1,
        )
        space1 = self.create_spatial_structure(
            self.site,
            "ifc_space",
            "Room 101",
            parent=storey1,
            level=2,
        )

        # Generate IFC
        generator = BuildingIFCGenerator(self.site)
        ifc_string = generator.generate()

        # Verify structure in output
        self.assertIn("IfcBuilding", ifc_string)
        self.assertIn("IfcBuildingStorey", ifc_string)
        self.assertIn("IfcSpace", ifc_string)
        self.assertIn("Main Building", ifc_string)
        self.assertIn("Ground Floor", ifc_string)

    def test_building_elements_generation(self):
        """Test generation of building elements (walls, beams, etc.)"""
        building = self.create_spatial_structure(
            self.site, "ifc_building", "Main Building"
        )

        # Create some building elements
        wall = self.create_asset(
            building,
            "wall",
            "Exterior Wall",
            {"thickness_mm": 300, "material": "concrete"},
        )
        beam = self.create_asset(
            building, "beam", "Main Beam", {"length_m": 20, "section": "IPE400"}
        )
        column = self.create_asset(
            building,
            "column",
            "Support Column",
            {"height_m": 5, "diameter_mm": 400},
        )

        # Generate IFC
        generator = BuildingIFCGenerator(self.site)
        ifc_string = generator.generate()

        # Verify elements in output
        self.assertIn("IfcWall", ifc_string)
        self.assertIn("IfcBeam", ifc_string)
        self.assertIn("IfcColumn", ifc_string)

    def test_structural_properties_added(self):
        """Test that structural analysis properties are added"""
        building = self.create_spatial_structure(
            self.site, "ifc_building", "Main Building"
        )
        beam = self.create_asset(building, "beam", "Steel Beam")
        column = self.create_asset(building, "column", "Steel Column")

        # Generate IFC
        generator = BuildingIFCGenerator(self.site)
        ifc_string = generator.generate()

        # Verify structural properties (PropertySet names)
        self.assertIn("Pset_StructuralAnalysis", ifc_string)

    def test_generation_metadata(self):
        """Test that generation metadata is captured"""
        building = self.create_spatial_structure(
            self.site, "ifc_building", "Main Building"
        )
        self.create_asset(building, "wall", "Wall 1")
        self.create_asset(building, "beam", "Beam 1")

        # Generate IFC
        generator = BuildingIFCGenerator(self.site)
        ifc_string = generator.generate()

        # Verify metadata was captured
        self.assertIsNotNone(generator.generation_metadata)
        self.assertIn("total_elements", generator.generation_metadata)
        self.assertIn("spatial_elements", generator.generation_metadata)
        self.assertGreater(generator.generation_metadata["total_elements"], 0)


class BridgeGeneratorTests(BaseGeneratorTestCase):
    """Tests for BridgeIFCGenerator"""

    def setUp(self):
        """Set up for each test"""
        self.site = self.create_site("INFRA_BRIDGE")
        self.project.project_type = "INFRA_BRIDGE"
        self.project.save()

    def test_generator_initialization(self):
        """Test that generator initializes correctly"""
        generator = BridgeIFCGenerator(self.site)
        self.assertIsNotNone(generator.site)
        self.assertEqual(generator.site.id, self.site.id)

    def test_bridge_hierarchy_generation(self):
        """Test generation of proper IFC bridge hierarchy"""
        # Create bridge hierarchy
        bridge = self.create_spatial_structure(
            self.site, "ifc_bridge", "Highway Bridge"
        )
        deck = self.create_spatial_structure(
            self.site,
            "ifc_bridge_part",
            "Main Deck",
            parent=bridge,
            level=1,
        )
        segment = self.create_spatial_structure(
            self.site,
            "ifc_bridge_part",
            "Segment A",
            parent=deck,
            level=2,
        )

        # Generate IFC
        generator = BridgeIFCGenerator(self.site)
        ifc_string = generator.generate()

        # Verify structure in output
        self.assertIn("IfcBridge", ifc_string)
        self.assertIn("IfcBridgePart", ifc_string)
        self.assertIn("Highway Bridge", ifc_string)

    def test_bridge_elements_generation(self):
        """Test generation of bridge elements (beams, piers, etc.)"""
        bridge = self.create_spatial_structure(
            self.site, "ifc_bridge", "Highway Bridge"
        )

        # Create bridge elements
        beam = self.create_asset(
            bridge, "beam", "Main Girder", {"span_length_m": 40, "material": "steel"}
        )
        pier = self.create_asset(
            bridge,
            "column",
            "Bridge Pier",
            {"height_m": 25, "material": "concrete"},
        )

        # Generate IFC
        generator = BridgeIFCGenerator(self.site)
        ifc_string = generator.generate()

        # Verify elements in output
        self.assertIn("IfcBeam", ifc_string)
        self.assertIn("IfcColumn", ifc_string)

    def test_bridge_specific_properties(self):
        """Test that bridge-specific properties are added"""
        bridge = self.create_spatial_structure(
            self.site, "ifc_bridge", "Highway Bridge"
        )
        beam = self.create_asset(bridge, "beam", "Main Girder")
        pier = self.create_asset(bridge, "column", "Pier")

        # Generate IFC
        generator = BridgeIFCGenerator(self.site)
        ifc_string = generator.generate()

        # Verify bridge properties
        self.assertIn("BridgeType", ifc_string)
        self.assertIn("SpanLength", ifc_string)


class RoadGeneratorTests(BaseGeneratorTestCase):
    """Tests for RoadIFCGenerator"""

    def setUp(self):
        """Set up for each test"""
        self.site = self.create_site("INFRA_ROAD")
        self.project.project_type = "INFRA_ROAD"
        self.project.save()

    def test_generator_initialization(self):
        """Test that generator initializes correctly"""
        generator = RoadIFCGenerator(self.site)
        self.assertIsNotNone(generator.site)
        self.assertEqual(generator.site.id, self.site.id)

    def test_road_hierarchy_generation(self):
        """Test generation of proper IFC road hierarchy"""
        # Create road hierarchy
        road = self.create_spatial_structure(self.site, "ifc_road", "Main Road")
        segment = self.create_spatial_structure(
            self.site, "ifc_road_part", "Segment 1A", parent=road, level=1
        )

        # Generate IFC
        generator = RoadIFCGenerator(self.site)
        ifc_string = generator.generate()

        # Verify structure in output
        self.assertIn("IfcRoad", ifc_string)
        self.assertIn("IfcRoadPart", ifc_string)
        self.assertIn("Main Road", ifc_string)

    def test_pavement_generation(self):
        """Test generation of pavement assets"""
        road = self.create_spatial_structure(self.site, "ifc_road", "Main Road")

        # Create pavement elements
        pavement = self.create_asset(
            road,
            "pavement",
            "Asphalt Surface",
            {"thickness_mm": 200, "material": "AC-20", "compaction": "98"},
        )
        curb = self.create_asset(
            road, "curb", "Concrete Curb", {"height_mm": 150, "material": "concrete"}
        )

        # Generate IFC
        generator = RoadIFCGenerator(self.site)
        ifc_string = generator.generate()

        # Verify elements in output
        self.assertIn("IfcBuildingElementProxy", ifc_string)

    def test_road_specific_properties(self):
        """Test that road-specific properties are added"""
        road = self.create_spatial_structure(self.site, "ifc_road", "Main Road")
        pavement = self.create_asset(road, "pavement", "Asphalt Surface")

        # Generate IFC
        generator = RoadIFCGenerator(self.site)
        ifc_string = generator.generate()

        # Verify road properties
        self.assertIn("PavementType", ifc_string)
        self.assertIn("Asphalt", ifc_string)

    def test_pavement_layers(self):
        """Test that pavement layers are created"""
        road = self.create_spatial_structure(self.site, "ifc_road", "Main Road")
        pavement = self.create_asset(road, "pavement", "Multi-layer Pavement")

        # Generate IFC
        generator = RoadIFCGenerator(self.site)
        ifc_string = generator.generate()

        # Verify layer structure is created
        self.assertIn("BaseLayer", ifc_string)
        self.assertIn("BinderLayer", ifc_string)
        self.assertIn("SurfaceLayer", ifc_string)


class GeneratorIntegrationTests(BaseGeneratorTestCase):
    """Integration tests combining multiple generators and features"""

    def test_large_structure_generation(self):
        """Test generation with larger structures"""
        site = self.create_site("BUILDING", "Large Building")

        # Create complex building hierarchy
        building = self.create_spatial_structure(site, "ifc_building", "Office Tower")

        # Create multiple floors with spaces
        for floor_num in range(1, 4):
            storey = self.create_spatial_structure(
                site,
                "ifc_building_storey",
                f"Floor {floor_num}",
                parent=building,
                level=1,
            )

            # Add spaces to each floor
            for room_num in range(1, 6):
                space = self.create_spatial_structure(
                    site,
                    "ifc_space",
                    f"Room {floor_num}{room_num:02d}",
                    parent=storey,
                    level=2,
                )

                # Add elements to spaces
                self.create_asset(space, "wall", f"Wall {floor_num}{room_num:02d}")

        # Test all generators (site is BUILDING type)
        generator = BuildingIFCGenerator(site)
        ifc_string = generator.generate()

        # Verify output size (should be significant)
        self.assertGreater(len(ifc_string), 1000)
        self.assertIn("IfcProject", ifc_string)

    def test_ifc_string_validity(self):
        """Test that generated IFC strings have valid ISO-10303 format"""
        site = self.create_site("BUILDING")
        building = self.create_spatial_structure(site, "ifc_building", "Test Building")

        generator = BuildingIFCGenerator(site)
        ifc_string = generator.generate()

        # Check basic IFC format markers
        self.assertIn("ISO-10303-21", ifc_string)
        self.assertTrue(
            ifc_string.startswith("ISO-10303-21;"),
            "IFC should start with ISO-10303-21;",
        )

    def test_generator_error_handling(self):
        """Test that generators handle invalid data gracefully"""
        site = self.create_site("BUILDING")

        # Create spatial structure with invalid properties
        building = self.create_spatial_structure(
            site,
            "ifc_building",
            "Test",
            properties={"invalid_key": "some_value"},
        )

        # Should generate without raising exception
        generator = BuildingIFCGenerator(site)
        try:
            ifc_string = generator.generate()
            self.assertIsInstance(ifc_string, str)
        except Exception as e:
            self.fail(f"Generator should handle invalid properties gracefully: {e}")
