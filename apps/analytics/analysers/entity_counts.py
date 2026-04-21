from .base import BaseAnalyser
from .utils import open_ifc, count_products_by_class


class EntityCountsAnalyser(BaseAnalyser):
    def run(self, file_path):
        model = open_ifc(file_path)
        if model is None:
            return self.with_meta({"notice": "ifcopenshell not installed"}, "entity_counts")

        counts = count_products_by_class(model)
        return self.with_meta(
            {
                "entity_counts": counts,
                "total_entities": sum(counts.values()),
                "distinct_entity_types": len(counts),
            },
            "entity_counts",
        )
