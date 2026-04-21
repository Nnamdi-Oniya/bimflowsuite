from .base import BaseAnalyser
from .utils import open_ifc, count_products_by_class


class QTOAnalyser(BaseAnalyser):
    def run(self, file_path):
        model = open_ifc(file_path)
        if model is None:
            return self.with_meta({"notice": "ifcopenshell not installed"}, "qto")

        counts = count_products_by_class(model)
        tracked = [
            "IfcWall",
            "IfcSlab",
            "IfcBeam",
            "IfcColumn",
            "IfcDoor",
            "IfcWindow",
            "IfcPipeSegment",
            "IfcDuctSegment",
            "IfcRail",
            "IfcSleeper",
        ]
        quantities = {cls: {"count": counts.get(cls, 0)} for cls in tracked}
        return self.with_meta(
            {
                "quantities": quantities,
                "total_tracked_elements": sum(v["count"] for v in quantities.values()),
            },
            "qto",
        )
