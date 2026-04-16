from .base import BaseAnalyser
from .utils import open_ifc, count_products_by_class


class ScheduleAnalyser(BaseAnalyser):
    def run(self, file_path):
        model = open_ifc(file_path)
        if model is None:
            return self.with_meta({"notice": "ifcopenshell not installed"}, "schedule")

        counts = count_products_by_class(model)
        total_work_items = sum(counts.values())
        productivity_per_day = 12
        duration_days = int((total_work_items / productivity_per_day) + 0.999)
        return self.with_meta(
            {
                "estimated_duration_days": duration_days,
                "total_work_items": total_work_items,
                "productivity_assumption_items_per_day": productivity_per_day,
            },
            "schedule",
        )
