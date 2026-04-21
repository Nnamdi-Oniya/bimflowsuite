from .base import BaseAnalyser
from .utils import open_ifc, count_products_by_class


class AnomalyAnalyser(BaseAnalyser):
    def run(self, file_path):
        model = open_ifc(file_path)
        if model is None:
            return self.with_meta({"notice": "ifcopenshell not installed"}, "anomaly_detection")

        counts = count_products_by_class(model)
        values = [v for v in counts.values() if v > 0]
        if not values:
            return self.with_meta({"anomalies_count": 0, "anomalous_types": []}, "anomaly_detection")

        avg = sum(values) / len(values)
        threshold = avg * 3
        anomalous = [cls for cls, val in counts.items() if val > threshold]
        return self.with_meta(
            {
                "anomalies_count": len(anomalous),
                "anomalous_types": anomalous,
                "threshold": threshold,
            },
            "anomaly_detection",
        )
