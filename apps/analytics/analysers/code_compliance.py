from .base import BaseAnalyser
from .utils import open_ifc


class CodeComplianceAnalyser(BaseAnalyser):
    def run(self, file_path):
        model = open_ifc(file_path)
        if model is None:
            return self.with_meta({"notice": "ifcopenshell not installed"}, "code_compliance")

        required_classes = ["IfcProject", "IfcSite", "IfcBuilding"]
        missing = [cls for cls in required_classes if len(model.by_type(cls)) == 0]
        checks = {
            "has_project": len(model.by_type("IfcProject")) > 0,
            "has_site": len(model.by_type("IfcSite")) > 0,
            "has_building": len(model.by_type("IfcBuilding")) > 0,
        }

        return self.with_meta(
            {
                "compliant": len(missing) == 0,
                "missing_required_entities": missing,
                "checks": checks,
            },
            "code_compliance",
        )
