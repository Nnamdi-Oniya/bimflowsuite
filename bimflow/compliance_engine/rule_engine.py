import yaml
import ifcopenshell
from io import BytesIO
from .clash_detector import AdvancedClashDetector  # Our advanced module
import logging

logger = logging.getLogger(__name__)

class RuleEngine:
    def __init__(self, rule_pack_yaml):
        self.rules = yaml.safe_load(rule_pack_yaml)['rules']
        self.results = []
        self.detector = AdvancedClashDetector(tolerance_hard=0.01, tolerance_soft=0.05)

    def evaluate(self, ifc_string, model_id, include_clash=True):
        ifc_file = ifcopenshell.open(BytesIO(ifc_string.encode()))
        
        # Rule checks (as before, vectorized)
        for rule in self.rules:
            # ... (previous logic for conditions)
            passed = True  # Simplified
            self.results.append({'rule': rule['name'], 'passed': passed, 'details': []})

        # Advanced clash if enabled
        if include_clash:
            clash_results = self.detector.detect_clashes(ifc_string)
            self.results.extend([{'rule': 'clash_hard', 'passed': len(clash_results['summary']['hard_clashes']) == 0, 'details': clash_results['clashes'][:5]}])  # Top 5

        # Save
        from .models import ComplianceCheck
        check = ComplianceCheck.objects.create(model_id=model_id, rule_pack='default', results=self.results)
        check.status = 'passed' if all(r.get('passed', True) for r in self.results) else 'failed'
        check.clash_results = clash_results if include_clash else {}
        check.save()

        return self.results