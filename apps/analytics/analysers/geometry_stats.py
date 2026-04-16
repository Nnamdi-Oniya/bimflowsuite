from .base import BaseAnalyser
import os
from .utils import open_ifc


class GeometryStatsAnalyser(BaseAnalyser):
    def run(self, file_path):
        file_size = os.path.getsize(file_path)
        model = open_ifc(file_path)
        if model is None:
            return self.with_meta(
                {
                    "file_size_bytes": file_size,
                    "notice": "ifcopenshell not installed",
                },
                "geometry_stats",
            )

        solids = len(model.by_type("IfcExtrudedAreaSolid"))
        polylines = len(model.by_type("IfcPolyline"))
        mapped_items = len(model.by_type("IfcMappedItem"))
        return self.with_meta(
            {
                "file_size_bytes": file_size,
                "geometry": {
                    "extruded_area_solids": solids,
                    "polylines": polylines,
                    "mapped_items": mapped_items,
                },
            },
            "geometry_stats",
        )
