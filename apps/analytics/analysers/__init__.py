from .base import BaseAnalyser
from .entity_counts import EntityCountsAnalyser
from .geometry_stats import GeometryStatsAnalyser
from .qto import QTOAnalyser
from .anomaly import AnomalyAnalyser
from .carbon import CarbonEstimateAnalyser
from .cost_estimate import CostEstimateAnalyser
from .schedule import ScheduleAnalyser
from .clash_detection import ClashDetectionAnalyser
from .code_compliance import CodeComplianceAnalyser
from .energy_usage import EnergyUsageAnalyser
from .structural_checks import StructuralChecksAnalyser

ANALYSER_REGISTRY = {
    "entity_counts": EntityCountsAnalyser,
    "geometry_stats": GeometryStatsAnalyser,
    "qto": QTOAnalyser,
    "anomaly_detection": AnomalyAnalyser,
    "cost_estimate": CostEstimateAnalyser,
    "schedule": ScheduleAnalyser,
    "clash_detection": ClashDetectionAnalyser,
    "code_compliance": CodeComplianceAnalyser,
    "energy_usage": EnergyUsageAnalyser,
    "carbon_estimate": CarbonEstimateAnalyser,
    "structural_checks": StructuralChecksAnalyser,
}
