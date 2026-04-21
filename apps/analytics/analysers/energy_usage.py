from .base import BaseAnalyser
from .utils import open_ifc


class EnergyUsageAnalyser(BaseAnalyser):
    def run(self, file_path):
        model = open_ifc(file_path)
        if model is None:
            return self.with_meta({"notice": "ifcopenshell not installed"}, "energy_usage")

        spaces = len(model.by_type("IfcSpace"))
        walls = len(model.by_type("IfcWall"))
        windows = len(model.by_type("IfcWindow"))
        doors = len(model.by_type("IfcDoor"))

        # Simplified proxy metric for early-stage dashboards.
        eui = max(10, (walls * 0.8 + windows * 1.4 + doors * 0.6 + spaces * 3.0))
        return self.with_meta(
            {
                "estimated_eui_kwh_m2_year": round(eui, 2),
                "inputs": {
                    "spaces": spaces,
                    "walls": walls,
                    "windows": windows,
                    "doors": doors,
                },
                "assumptions": "High-level geometry proxy; replace with full energy model integration.",
            },
            "energy_usage",
        )
