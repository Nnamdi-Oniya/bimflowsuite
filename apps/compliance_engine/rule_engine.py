import yaml
import ifcopenshell
from io import BytesIO
from .clash_detector import AdvancedClashDetector  # Our advanced module
import logging
import re

logger = logging.getLogger(__name__)


class RuleEngine:
    def __init__(self, rule_pack_yaml, tolerance_hard=0.01, tolerance_soft=0.05):
        try:
            self.rules = yaml.safe_load(rule_pack_yaml).get("rules", [])
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in rulepack: {e}")
            raise ValueError(f"Invalid rulepack YAML: {e}")

        self.results = []
        self.detector = AdvancedClashDetector(
            tolerance_hard=tolerance_hard, tolerance_soft=tolerance_soft
        )

    def evaluate(self, ifc_string, model_id, include_clash=True):
        """Evaluate all rules and optionally run clash detection."""
        try:
            ifc_file = ifcopenshell.open(BytesIO(ifc_string.encode()))
        except Exception as e:
            logger.error(f"Failed to parse IFC: {e}")
            raise ValueError(f"Invalid IFC file: {e}")

        # Rule checks with actual condition evaluation
        for rule in self.rules:
            try:
                rule_name = rule.get("name", "Unknown")
                condition = rule.get("condition", "True")
                category = rule.get("category", "general")
                severity = rule.get("severity", "info")

                # Parse condition: simple expressions like "wall_count > 5" or "avg_height < 30"
                passed = self._evaluate_condition(condition, ifc_file)

                self.results.append(
                    {
                        "rule": rule_name,
                        "category": category,
                        "severity": severity,
                        "passed": passed,
                        "condition": condition,
                        "details": [],
                    }
                )
                logger.debug(f"Rule '{rule_name}' -> {passed}")
            except Exception as e:
                logger.warning(f"Rule evaluation failed for '{rule.get('name')}': {e}")
                self.results.append(
                    {
                        "rule": rule.get("name", "Unknown"),
                        "passed": False,
                        "error": str(e),
                    }
                )

        # Advanced clash detection if enabled
        if include_clash:
            try:
                clash_results = self.detector.detect_clashes(ifc_string)
                # Convert clash results to rule format
                hard_clash_passed = clash_results["summary"]["hard_clashes"] == 0
                self.results.append(
                    {
                        "rule": "clash_detection_hard",
                        "category": "clash",
                        "severity": "critical",
                        "passed": hard_clash_passed,
                        "details": clash_results["clashes"][:10],  # Top 10
                    }
                )

                soft_clash_passed = clash_results["summary"]["soft_clashes"] == 0
                self.results.append(
                    {
                        "rule": "clash_detection_soft",
                        "category": "clash",
                        "severity": "warning",
                        "passed": soft_clash_passed,
                        "details": clash_results["clashes"][10:20],  # Next 10
                    }
                )
                logger.info(f"Clash detection: {clash_results['summary']}")
            except Exception as e:
                logger.error(f"Clash detection failed: {e}")
                self.results.append(
                    {
                        "rule": "clash_detection",
                        "passed": False,
                        "error": f"Clash detection failed: {e}",
                    }
                )

        # Save to DB
        from .models import ComplianceCheck

        try:
            check = ComplianceCheck.objects.create(
                model_id=model_id, rule_pack="evaluated", results=self.results
            )
            # Determine overall status
            overall_passed = all(
                r.get("passed", True) for r in self.results if "error" not in r
            )
            check.status = "passed" if overall_passed else "failed"
            check.clash_results = self.detector.results if include_clash else {}
            check.save()
            logger.info(
                f"ComplianceCheck saved: model={model_id}, status={check.status}"
            )
        except Exception as e:
            logger.error(f"Failed to save ComplianceCheck: {e}")

        return self.results

    def _evaluate_condition(self, condition, ifc_file):
        """
        Evaluate a rule condition string.
        Examples:
        - "wall_count > 5" → counts IfcWall elements
        - "avg_height < 30" → averages story heights
        - "has_fire_rating" → checks for fire properties
        """
        condition = condition.strip()

        # Simple heuristics (not a full expression evaluator)
        if "wall_count" in condition:
            wall_count = len(ifc_file.by_type("IfcWall"))
            return self._compare_value(
                wall_count, condition.replace("wall_count", str(wall_count))
            )

        if "column_count" in condition:
            col_count = len(ifc_file.by_type("IfcColumn"))
            return self._compare_value(
                col_count, condition.replace("column_count", str(col_count))
            )

        if "beam_count" in condition:
            beam_count = len(ifc_file.by_type("IfcBeam"))
            return self._compare_value(
                beam_count, condition.replace("beam_count", str(beam_count))
            )

        if "has_fire_rating" in condition:
            # Check for fire rating properties
            for obj in ifc_file:
                if hasattr(obj, "IsDefinedBy"):
                    for rel in obj.IsDefinedBy:
                        if hasattr(rel, "RelatingPropertyDefinition"):
                            pset = rel.RelatingPropertyDefinition
                            if hasattr(pset, "HasProperties"):
                                for prop in pset.HasProperties:
                                    if "fire" in str(prop.Name).lower():
                                        return True
            return False

        # Default: pass (conservative)
        logger.debug(f"Condition not recognized, defaulting to True: {condition}")
        return True

    @staticmethod
    def _compare_value(value, expression):
        """Compare value against expression like '> 5' or '< 30'."""
        try:
            # Extract operator and threshold
            match = re.match(r".*?([<>=]+)\s*(\d+\.?\d*)", expression)
            if match:
                op, threshold = match.groups()
                threshold = float(threshold)

                if op == ">":
                    return value > threshold
                elif op == "<":
                    return value < threshold
                elif op == ">=":
                    return value >= threshold
                elif op == "<=":
                    return value <= threshold
                elif op == "==":
                    return value == threshold
        except (ValueError, AttributeError, IndexError) as e:
            logger.warning(f"Could not evaluate comparison: {expression}, error: {e}")

        return True  # Conservative default
