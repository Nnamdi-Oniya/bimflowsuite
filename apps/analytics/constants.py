ANALYSIS_TYPES = [
    ("qto", "Quantity Takeoff"),
    ("cost_estimate", "Cost Estimation"),
    ("schedule", "Schedule"),
    ("anomaly_detection", "Anomaly Detection"),
    ("geometry_stats", "Geometry Stats"),
    ("entity_counts", "Entity Counts"),
    ("clash_detection", "Clash Detection"),
    ("code_compliance", "Code Compliance"),
    ("energy_usage", "Energy Usage"),
    ("carbon_estimate", "Carbon Estimate"),
    ("structural_checks", "Structural Checks"),
]

ANALYSIS_TYPE_VALUES = [value for value, _ in ANALYSIS_TYPES]
ANALYSIS_TYPE_LABELS = dict(ANALYSIS_TYPES)

SESSION_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("running", "Running"),
    ("done", "Done"),
    ("partial", "Partial"),
    ("failed", "Failed"),
]

RESULT_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("running", "Running"),
    ("done", "Done"),
    ("failed", "Failed"),
    ("skipped", "Skipped"),
]

SEVERITY_CHOICES = [
    ("info", "Info"),
    ("warning", "Warning"),
    ("error", "Error"),
    ("critical", "Critical"),
]

SOURCE_CHOICES = [
    ("generated", "Generated on platform"),
    ("uploaded", "Uploaded by user"),
]
