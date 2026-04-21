from .base import BaseAnalyser
from .utils import open_ifc


class StructuralChecksAnalyser(BaseAnalyser):
    def run(self, file_path):
        model = open_ifc(file_path)
        if model is None:
            return self.with_meta({"notice": "ifcopenshell not installed"}, "structural_checks")

        beams = len(model.by_type("IfcBeam"))
        columns = len(model.by_type("IfcColumn"))
        slabs = len(model.by_type("IfcSlab"))
        walls = len(model.by_type("IfcWall"))

        checks = {
            "has_primary_members": (beams + columns + walls) > 0,
            "has_floor_elements": slabs > 0,
            "beam_to_column_ratio": round((beams / columns), 3) if columns else None,
        }

        issues = []
        if not checks["has_primary_members"]:
            issues.append("No primary structural members detected")
        if not checks["has_floor_elements"]:
            issues.append("No slab/floor elements detected")

        return self.with_meta(
            {
                "checks": checks,
                "issues": issues,
                "issue_count": len(issues),
            },
            "structural_checks",
        )
