from .base import BaseAnalyser
from .utils import open_ifc, count_products_by_class


class CarbonEstimateAnalyser(BaseAnalyser):
    def run(self, file_path):
        model = open_ifc(file_path)
        if model is None:
            return self.with_meta({"notice": "ifcopenshell not installed"}, "carbon_estimate")

        counts = count_products_by_class(model)
        factors = {
            "IfcWall": 120,
            "IfcSlab": 180,
            "IfcBeam": 150,
            "IfcColumn": 140,
            "IfcRoof": 100,
        }
        total = 0
        by_class = {}
        for cls, factor in factors.items():
            value = counts.get(cls, 0) * factor
            if value:
                by_class[cls] = value
                total += value
        return self.with_meta(
            {
                "estimated_embodied_carbon_kgco2e": total,
                "assumptions": "Class-level default factors used; replace with material-level LCA in production.",
                "by_class": by_class,
            },
            "carbon_estimate",
        )
