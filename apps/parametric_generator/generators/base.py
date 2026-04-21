"""
Base Generator Class for IFC4X3 Generation

This module provides the foundation for generating IFC4X3 files from
SpatialStructure and Asset models. All project-type generators inherit
from this class.
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from ifcopenshell import file as ifc_file
from ifcopenshell import guid
import json
import math

logger = logging.getLogger(__name__)


class BaseIFCGenerator(ABC):
    """
    Base class for IFC4X3 generation from hierarchical BIM structure.

    Handles:
    - Site/Project/Building hierarchy creation
    - Asset/Element placement and properties
    - Material and Property Set creation
    - Coordinate system setup
    """

    def __init__(self, site, facility=None):
        """
        Initialize generator with a Site instance.

        Args:
            site: Site model instance containing project context
        """
        self.site = site
        self.facility = facility
        self.project = site.project
        self.ifc = None
        self.model_context = None
        self.body_context = None
        self.element_map = {}  # Maps model IDs to IFC elements
        self.metadata = {
            "total_elements": 0,
            "spatial_elements": 0,
            "building_elements": 0,
            "property_sets": 0,
            "schema_version": self._get_ifc_schema_name(site.ifc_schema_version),
            "generator_version": "1.0.0",
            "generation_timestamp": datetime.now().isoformat(),
        }

    def generate(self):
        """
        Main generation workflow. Returns IFC string.
        """
        try:
            # Initialize IFC file
            self._create_ifc_file()

            # Create project/site hierarchy
            self._create_project_context()

            # Create spatial structures (Buildings, Storeys, etc.)
            self._create_spatial_structures()

            # Create assets (Walls, Beams, columns, etc.)
            self._create_assets()

            # Set metadata
            self._set_generation_metadata()

            logger.info(
                f"IFC generation complete: {self.metadata['total_elements']} elements"
            )
            return self.ifc.to_string()

        except Exception as e:
            logger.error(f"IFC generation failed: {str(e)}", exc_info=True)
            raise

    def _create_ifc_file(self):
        """Initialize IFC file with schema version from site configuration."""
      
        schema_version = self._get_ifc_schema_name(self.site.ifc_schema_version)
        self.ifc = ifc_file(schema=schema_version)
        logger.info(f"Created IFC file with schema version: {schema_version}")

    def _get_ifc_schema_name(self, site_version):
        """
        Convert site's ifc_schema_version to ifcopenshell format.

        Mappings:
            ifc2x3 → IFC2X3
            ifc4 → IFC4
            ifc4x3 → IFC4X3
        """
        versions = {
            "ifc2x3": "IFC2X3",
            "ifc4": "IFC4",
            "ifc4x3": "IFC4X3",
        }
        return versions.get(site_version, "IFC4X3")
    
    def _create_project_context(self):
        """
        Create base project, site, and building containers.
        Subclasses override for specific hierarchy.
        """
        # Project
        project_ifc = self.ifc.createIfcProject(
            guid.new(),
            Name=self.project.name,
            LongName=self.project.description or "",
        )

        # Geometric context
        context_3d = self.ifc.createIfcGeometricRepresentationContext(
            ContextType="Model",
            ContextIdentifier="3D",
            CoordinateSpaceDimension=3,
            Precision=float(self.site.precision),
            WorldCoordinateSystem=self._create_local_placement(),
        )
        self.model_context = context_3d

        # Body sub-context reused for all products
        self.body_context = self.ifc.createIfcGeometricRepresentationSubContext(
            ContextIdentifier="Body",
            ContextType="Model",
            ParentContext=context_3d,
            TargetView="MODEL_VIEW",
            CoordinateSpaceDimension=3,
            Precision=float(self.site.precision),
        )

        # Attach context to project
        project_ifc.RepresentationContexts = [context_3d]

        # Site
        site_ifc = self.ifc.createIfcSite(
            guid.new(),
            Name=self.site.site_name,
            Description=self.site.address or "",
            ObjectPlacement=self._create_local_placement(),
        )

        # Relate site to project
        self.ifc.createIfcRelAggregates(
            guid.new(),
            RelatedObjects=[site_ifc],
            RelatingObject=project_ifc,
        )

        self.element_map["project"] = project_ifc
        self.element_map["site"] = site_ifc

    def _create_local_placement(self):
        """Create 3D placement at origin."""
        axis2placement = self.ifc.createIfcAxis2Placement3D(
            Location=self.ifc.createIfcCartesianPoint([0.0, 0.0, 0.0])
        )
        return self.ifc.createIfcLocalPlacement(
            PlacementRelTo=None, RelativePlacement=axis2placement
        )

    def _create_spatial_structures(self):
        """
        Create spatial hierarchy from SpatialStructure model instances.
        """
        root_structures = self.site.spatial_structures.filter(parent=None).order_by(
            "order_in_parent"
        )

        for root_struct in root_structures:
            ifc_element = self._spatial_structure_to_ifc(root_struct)
            self.element_map[f"spatial_{root_struct.id}"] = ifc_element
            self.metadata["spatial_elements"] += 1

            # Recursively create children
            self._create_child_spatial_structures(root_struct, ifc_element)

    def _create_child_spatial_structures(self, parent_struct, parent_ifc_element):
        """Recursively create child spatial structures."""
        for child_struct in parent_struct.children.all().order_by("order_in_parent"):
            ifc_element = self._spatial_structure_to_ifc(
                child_struct, parent_ifc_element
            )
            self.element_map[f"spatial_{child_struct.id}"] = ifc_element
            self.metadata["spatial_elements"] += 1

            # Continue recursion
            self._create_child_spatial_structures(child_struct, ifc_element)

    def _spatial_structure_to_ifc(self, spatial_struct, parent=None):
        """
        Convert SpatialStructure model to IFC entity.

        Maps spatial types to IFC entity types:
        - ifc_building → IfcBuilding
        - ifc_building_storey → IfcBuildingStorey
        - ifc_space → IfcSpace
        """
        spatial_type = spatial_struct.spatial_type

        # Normalize properties (JSONField may be stored as string)
        properties = self._normalize_properties(spatial_struct.properties)

        # Get elevation if available
        # Use spatial elevation if provided; otherwise fall back to site elevation
        elevation = properties.get("elevation")
        if elevation is None and hasattr(self.site, "elevation"):
            elevation = self.site.elevation or 0
        elevation = elevation or 0

        # Create IFC element based on spatial type
        ifc_element = None
        if spatial_type == "ifc_building":
            ifc_element = self.ifc.createIfcBuilding(
                guid.new(),
                Name=spatial_struct.name,
                Description=spatial_struct.description or "",
                ObjectPlacement=self._create_local_placement(),
            )
        elif spatial_type == "ifc_building_storey":
            ifc_element = self.ifc.createIfcBuildingStorey(
                guid.new(),
                Name=spatial_struct.name,
                Description=spatial_struct.description or "",
                Elevation=float(elevation),
                ObjectPlacement=self._create_local_placement(),
            )
        elif spatial_type == "ifc_space":
            ifc_element = self.ifc.createIfcSpace(
                guid.new(),
                Name=spatial_struct.name,
                Description=spatial_struct.description or "",
                ObjectPlacement=self._create_local_placement(),
            )
        elif spatial_type == "ifc_bridge":
            ifc_element = self.ifc.createIfcBridge(
                guid.new(),
                Name=spatial_struct.name,
                Description=spatial_struct.description or "",
                ObjectPlacement=self._create_local_placement(),
            )
        elif spatial_type == "ifc_road":
            ifc_element = self.ifc.createIfcRoad(
                guid.new(),
                Name=spatial_struct.name,
                Description=spatial_struct.description or "",
                ObjectPlacement=self._create_local_placement(),
            )
        else:
            # Fallback to generic container
            ifc_element = self.ifc.createIfcBuildingElementProxy(
                guid.new(),
                Name=spatial_struct.name,
                Description=spatial_struct.description or "",
                ObjectPlacement=self._create_local_placement(),
            )

        # Aggregate to parent
        if parent is not None:
            self.ifc.createIfcRelAggregates(
                guid.new(),
                RelatedObjects=[ifc_element],
                RelatingObject=parent,
            )
        else:
            # Root structure aggregates to site
            self.ifc.createIfcRelAggregates(
                guid.new(),
                RelatedObjects=[ifc_element],
                RelatingObject=self.element_map.get("site"),
            )

        # Add properties from JSON
        self._add_spatial_properties(ifc_element, properties)

        return ifc_element

    def _create_assets(self):
        """
        Create building/bridge/road elements from Asset model instances.
        """
        assets = self.site.elements.all().select_related("spatial_structure")
        if self.facility:
            assets = assets.filter(facility=self.facility)

        for asset in assets:
            try:
                ifc_element = self._asset_to_ifc(asset)
                if ifc_element:
                    self.element_map[f"asset_{asset.id}"] = ifc_element
                    self.metadata["building_elements"] += 1
                    self.metadata["total_elements"] += 1
            except Exception as e:
                logger.warning(f"Failed to create asset {asset.id}: {str(e)}")

    def _asset_to_ifc(self, asset):
        """
        Convert Asset model to IFC element.

        Maps asset types to IFC classes:
        - wall → IfcWall
        - beam → IfcBeam
        - slab → IfcSlab
        - column → IfcColumn
        - pipe → IfcPipeSegment
        - etc.
        """
        asset_type = asset.asset_type
        props = asset.properties

        # Create IFC element based on asset type
        ifc_element = None
        if asset_type == "wall":
            ifc_element = self.ifc.createIfcWall(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "beam":
            ifc_element = self.ifc.createIfcBeam(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "slab":
            ifc_element = self.ifc.createIfcSlab(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "column":
            ifc_element = self.ifc.createIfcColumn(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "foundation":
            ifc_element = self.ifc.createIfcFooting(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "door":
            ifc_element = self.ifc.createIfcDoor(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "window":
            ifc_element = self.ifc.createIfcWindow(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "roof":
            ifc_element = self.ifc.createIfcRoof(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "stairs":
            ifc_element = self.ifc.createIfcStair(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "pipe":
            ifc_element = self.ifc.createIfcPipeSegment(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "duct":
            ifc_element = self.ifc.createIfcDuctSegment(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "alignment":
            ifc_element = self.ifc.createIfcAlignment(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type in ("kerb", "curb"):
            ifc_element = self.ifc.createIfcKerb(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "pavement":
            ifc_element = self.ifc.createIfcPavement(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "rail":
            ifc_element = self.ifc.createIfcRail(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        elif asset_type == "sleeper":
            ifc_element = self.ifc.createIfcSleeper(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
            )
        else:
            # Fallback to generic building element proxy
            ifc_element = self.ifc.createIfcBuildingElementProxy(
                guid.new(),
                Name=asset.name,
                Description=asset.description or "",
                ObjectPlacement=self._create_local_placement(),
            )

        if ifc_element:
            # Place element in spatial structure
            spatial_struct = asset.spatial_structure
            parent_ifc = self.element_map.get(f"spatial_{spatial_struct.id}")

            if parent_ifc:
                placement = self._create_local_placement()
                pos = self._normalize_properties(asset.position or {})
                if pos and all(k in pos for k in ("x", "y", "z")):
                    placement.RelativePlacement.Location = self.ifc.createIfcCartesianPoint(
                        [float(pos["x"]), float(pos["y"]), float(pos["z"])]
                    )
                ifc_element.ObjectPlacement = placement
                self.ifc.createIfcRelContainedInSpatialStructure(
                    guid.new(),
                    RelatedElements=[ifc_element],
                    RelatingStructure=parent_ifc,
                )

            # Add properties
            self._add_asset_properties(ifc_element, asset)
            # Apply geometry as solid/shape if provided
            self._apply_geometry(ifc_element, asset)

        return ifc_element

    def _add_spatial_properties(self, ifc_element, properties):
        """Add PropertySets to spatial element."""
        if not properties:
            return

        pset = self.ifc.createIfcPropertySet(
            guid.new(),
            Name="Pset_SpatialStructureCommon",
            HasProperties=[],
        )

        for key, value in properties.items():
            if isinstance(value, (int, float)):
                prop = self.ifc.createIfcPropertySingleValue(
                    Name=key,
                    NominalValue=self.ifc.createIfcReal(value)
                    if isinstance(value, float)
                    else self.ifc.createIfcInteger(value),
                )
            else:
                prop = self.ifc.createIfcPropertySingleValue(
                    Name=key,
                    NominalValue=self.ifc.createIfcLabel(str(value)),
                )
            pset.HasProperties = list(pset.HasProperties or []) + [prop]

        if pset.HasProperties:
            self.ifc.createIfcRelDefinesByProperties(
                guid.new(),
                RelatedObjects=[ifc_element],
                RelatingPropertyDefinition=pset,
            )
            self.metadata["property_sets"] += 1

    def _add_asset_properties(self, ifc_element, asset):
        """Add PropertySets and material to asset element."""
        properties = self._normalize_properties(asset.properties)

        if asset.material:
            ifc_mat = self.ifc.createIfcMaterial(asset.material.name)
            self.ifc.createIfcRelAssociatesMaterial(
                guid.new(),
                RelatedObjects=[ifc_element],
                RelatingMaterial=ifc_mat,
            )

        if not properties:
            return

        # Attach raw geometry as a label property if present on asset
        geom = self._normalize_properties(asset.geometry or {})
        if geom:
            geom_prop = self.ifc.createIfcPropertySingleValue(
                Name="geometry",
                NominalValue=self.ifc.createIfcLabel(json.dumps(geom)),
            )
        else:
            geom_prop = None

        pset = self.ifc.createIfcPropertySet(
            guid.new(),
            Name="Pset_ElementCommon",
            HasProperties=[],
        )

        for key, value in properties.items():
            if isinstance(value, (int, float)):
                prop = self.ifc.createIfcPropertySingleValue(
                    Name=key,
                    NominalValue=self.ifc.createIfcReal(value)
                    if isinstance(value, float)
                    else self.ifc.createIfcInteger(value),
                )
            else:
                prop = self.ifc.createIfcPropertySingleValue(
                    Name=key,
                    NominalValue=self.ifc.createIfcLabel(str(value)),
                )
            pset.HasProperties = list(pset.HasProperties or []) + [prop]

        if geom_prop:
            pset.HasProperties = list(pset.HasProperties or []) + [geom_prop]

        if pset.HasProperties:
            self.ifc.createIfcRelDefinesByProperties(
                guid.new(),
                RelatedObjects=[ifc_element],
                RelatingPropertyDefinition=pset,
            )
            self.metadata["property_sets"] += 1

    def _apply_geometry(self, ifc_element, asset):
        """Create simple shape representations from stored geometry."""
        geom = self._normalize_properties(asset.geometry or {})
        if not geom or "type" not in geom:
            return

        gtype = geom.get("type")
        rep_items = []

        if gtype == "extruded_wall":
            start = geom.get("start", [0, 0, 0])
            end = geom.get("end", [0, 0, 0])
            height = float(geom.get("height", 3.0))
            thickness = float(geom.get("thickness", 0.2))
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            length = math.hypot(dx, dy) or 0.001
            dir_x = dx / length
            dir_y = dy / length
            # rectangle profile thickness x length, extrude height
            rect = self.ifc.createIfcRectangleProfileDef(
                ProfileType="AREA",
                ProfileName=None,
                XDim=thickness,
                YDim=length,
                Position=self.ifc.createIfcAxis2Placement2D(
                    Location=self.ifc.createIfcCartesianPoint([0.0, 0.0]),
                    RefDirection=self.ifc.createIfcDirection([1.0, 0.0]),
                ),
            )
            solid = self.ifc.createIfcExtrudedAreaSolid(
                SweptArea=rect,
                Position=self.ifc.createIfcAxis2Placement3D(
                    Location=self.ifc.createIfcCartesianPoint(list(start)),
                    RefDirection=self.ifc.createIfcDirection([dir_x, dir_y, 0.0]),
                    Axis=self.ifc.createIfcDirection([0.0, 0.0, 1.0]),
                ),
                ExtrudedDirection=self.ifc.createIfcDirection([0.0, 0.0, 1.0]),
                Depth=height,
            )
            rep_items.append(solid)

        elif gtype == "rectangular_slab":
            length = float(geom.get("length", 1.0))
            width = float(geom.get("width", 1.0))
            thickness = float(geom.get("thickness", 0.2))
            rect = self.ifc.createIfcRectangleProfileDef(
                ProfileType="AREA",
                ProfileName=None,
                XDim=width,
                YDim=length,
                Position=self.ifc.createIfcAxis2Placement2D(
                    Location=self.ifc.createIfcCartesianPoint([0.0, 0.0]),
                    RefDirection=self.ifc.createIfcDirection([1.0, 0.0]),
                ),
            )
            solid = self.ifc.createIfcExtrudedAreaSolid(
                SweptArea=rect,
                Position=self.ifc.createIfcAxis2Placement3D(
                    Location=self.ifc.createIfcCartesianPoint([0.0, 0.0, 0.0])
                ),
                ExtrudedDirection=self.ifc.createIfcDirection([0.0, 0.0, 1.0]),
                Depth=thickness,
            )
            rep_items.append(solid)

        elif gtype == "alignment" or asset.asset_type == "alignment":
            pts = geom.get("points", [])
            if len(pts) >= 2:
                poly = self.ifc.createIfcPolyline(
                    [self.ifc.createIfcCartesianPoint(list(p)) for p in pts]
                )
                rep_items.append(poly)
        elif gtype == "circular_column":
            diameter = float(geom.get("diameter", 0.5))
            height = float(geom.get("height", 3.0))
            circle = self.ifc.createIfcCircleProfileDef(
                ProfileType="AREA",
                ProfileName=None,
                Radius=diameter / 2.0,
                Position=self.ifc.createIfcAxis2Placement2D(
                    Location=self.ifc.createIfcCartesianPoint([0.0, 0.0])
                ),
            )
            solid = self.ifc.createIfcExtrudedAreaSolid(
                SweptArea=circle,
                Position=self.ifc.createIfcAxis2Placement3D(
                    Location=self.ifc.createIfcCartesianPoint([0.0, 0.0, 0.0])
                ),
                ExtrudedDirection=self.ifc.createIfcDirection([0.0, 0.0, 1.0]),
                Depth=height,
            )
            rep_items.append(solid)
        elif gtype == "i_beam":
            length = float(geom.get("length", 1.0))
            height = float(geom.get("height", 0.3))
            flange_width = float(geom.get("flange_width", 0.15))
            web_thickness = float(geom.get("web_thickness", flange_width / 5))
            flange_thickness = float(geom.get("flange_thickness", height / 10))
            # Approximate I-profile using IfcIShapeProfileDef
            iprof = self.ifc.createIfcIShapeProfileDef(
                ProfileType="AREA",
                ProfileName=None,
                OverallWidth=flange_width,
                OverallDepth=height,
                WebThickness=web_thickness,
                FlangeThickness=flange_thickness,
                FilletRadius=None,
            )
            solid = self.ifc.createIfcExtrudedAreaSolid(
                SweptArea=iprof,
                Position=self.ifc.createIfcAxis2Placement3D(
                    Location=self.ifc.createIfcCartesianPoint([0.0, 0.0, 0.0])
                ),
                ExtrudedDirection=self.ifc.createIfcDirection([1.0, 0.0, 0.0]),
                Depth=length,
            )
            rep_items.append(solid)
        elif gtype in ("railway_alignment", "rail_alignment"):
            pts = geom.get("points", [])
            if len(pts) >= 2:
                poly = self.ifc.createIfcPolyline(
                    [self.ifc.createIfcCartesianPoint(list(p)) for p in pts]
                )
                rep_items.append(poly)
        elif gtype in ("continuous_rail",):
            length = float(geom.get("length", 1.0))
            solid = self.ifc.createIfcExtrudedAreaSolid(
                SweptArea=self.ifc.createIfcRectangleProfileDef(
                    ProfileType="AREA",
                    ProfileName=None,
                    XDim=float(geom.get("profile_width", 0.07)),
                    YDim=float(geom.get("profile_height", 0.16)),
                    Position=self.ifc.createIfcAxis2Placement2D(
                        Location=self.ifc.createIfcCartesianPoint([0.0, 0.0])
                    ),
                ),
                Position=self.ifc.createIfcAxis2Placement3D(
                    Location=self.ifc.createIfcCartesianPoint([0.0, 0.0, 0.0])
                ),
                ExtrudedDirection=self.ifc.createIfcDirection([1.0, 0.0, 0.0]),
                Depth=length,
            )
            rep_items.append(solid)
        elif gtype in ("sleeper_array",):
            count = int(geom.get("count", 1))
            spacing = float(geom.get("spacing", 0.6))
            length = float(geom.get("length", 2.5))
            width = float(geom.get("width", 0.25))
            thickness = float(geom.get("thickness", 0.2))
            sleeper_profile = self.ifc.createIfcRectangleProfileDef(
                ProfileType="AREA",
                ProfileName=None,
                XDim=width,
                YDim=length,
                Position=self.ifc.createIfcAxis2Placement2D(
                    Location=self.ifc.createIfcCartesianPoint([0.0, 0.0])
                ),
            )
            for i in range(max(count, 1)):
                solid = self.ifc.createIfcExtrudedAreaSolid(
                    SweptArea=sleeper_profile,
                    Position=self.ifc.createIfcAxis2Placement3D(
                        Location=self.ifc.createIfcCartesianPoint(
                            [float(i) * spacing, 0.0, 0.0]
                        )
                    ),
                    ExtrudedDirection=self.ifc.createIfcDirection([0.0, 0.0, 1.0]),
                    Depth=thickness,
                )
                rep_items.append(solid)

        if rep_items:
            shape = self.ifc.createIfcShapeRepresentation(
                ContextOfItems=self.body_context or self.model_context,
                RepresentationIdentifier="Body",
                RepresentationType="SweptSolid" if any(hasattr(i, "Depth") for i in rep_items) else "Curve3D",
                Items=rep_items,
            )
            if ifc_element.Representation:
                ifc_element.Representation.Representations.append(shape)
            else:
                ifc_element.Representation = self.ifc.createIfcProductDefinitionShape(
                    Representations=[shape]
                )

    def _normalize_properties(self, raw):
        """
        Ensure properties are a dict.
        Accepts dict, JSON string, or returns empty dict otherwise.
        """
        if isinstance(raw, dict):
            return raw
        if isinstance(raw, str):
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                return {}
        return {}

    def _set_generation_metadata(self):
        """Set metadata and mark generation complete."""
        self.metadata["total_elements"] = (
            self.metadata["spatial_elements"] + self.metadata["building_elements"]
        )

    @abstractmethod
    def customize(self):
        """
        Override in subclasses for project-type-specific customization.
        E.g., add structural analysis sets for buildings, pavement layers for roads.
        """
        pass
