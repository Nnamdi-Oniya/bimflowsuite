from .base import BaseAnalyser
from .utils import open_ifc, count_products_by_class


class CostEstimateAnalyser(BaseAnalyser):
    def run(self, file_path):
        model = open_ifc(file_path)
        if model is None:
            return self.with_meta({"notice": "ifcopenshell not installed"}, "cost_estimate")

        counts = count_products_by_class(model)
        unit_cost = {
            "IfcWall": 350,
            "IfcSlab": 500,
            "IfcBeam": 420,
            "IfcColumn": 390,
            "IfcDoor": 250,
            "IfcWindow": 220,
        }
        by_class = {}
        total = 0
        for cls, price in unit_cost.items():
            cost = counts.get(cls, 0) * price
            if cost:
                by_class[cls] = cost
                total += cost

        return self.with_meta(
            {
                "estimated_cost": total,
                "currency": "USD",
                "cost_breakdown": by_class,
                "assumptions": "Unit-rate estimate using default class rates.",
            },
            "cost_estimate",
        )
