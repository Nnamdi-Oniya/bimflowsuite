from .base import BaseAnalyser
from .utils import open_ifc


class ClashDetectionAnalyser(BaseAnalyser):
    def run(self, file_path):
        model = open_ifc(file_path)
        if model is None:
            return self.with_meta({"notice": "ifcopenshell not installed"}, "clash_detection")

        # Lightweight proxy check: duplicated GlobalIds indicate potential data collisions.
        seen = set()
        duplicates = []
        for product in model.by_type("IfcProduct"):
            gid = getattr(product, "GlobalId", None)
            if not gid:
                continue
            if gid in seen:
                duplicates.append(gid)
            seen.add(gid)

        return self.with_meta(
            {
                "potential_clashes": len(duplicates),
                "duplicate_global_ids": duplicates[:200],
                "method": "Duplicate GlobalId heuristic",
            },
            "clash_detection",
        )
