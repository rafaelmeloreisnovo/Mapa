import copy
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_observer_observed_network_v1 import ContractError, SOURCE, validate

class ObserverObservedNetworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(SOURCE.read_text(encoding="utf-8"))

    def reject(self, change):
        payload = copy.deepcopy(self.base)
        change(payload)
        with self.assertRaises(ContractError):
            validate(payload)

    def test_valid_registry(self):
        self.assertEqual(validate(self.base)["records"], 4)

    def test_cannot_promote(self):
        self.reject(lambda d: d["records"][0].update(claim_allowed=True))

    def test_cannot_automatically_merge(self):
        self.reject(lambda d: d.update(automatic_merge=True))

    def test_unknown_state_rejected(self):
        self.reject(lambda d: d["records"][0].update(epistemic_state="PASS"))

    def test_unidentified_observer_rejected(self):
        self.reject(lambda d: d["records"][0]["observer"].update(ref=""))

    def test_source_revision_required_for_observed(self):
        self.reject(lambda d: d["records"][0]["observed"].update(revision=None))

    def test_no_evidence_for_observed_rejected(self):
        self.reject(lambda d: d["records"][0].update(evidence_refs=[]))

    def test_unknown_cannot_be_zero(self):
        self.reject(lambda d: d["records"][2]["semantic_flags"].append("NUMERIC_ZERO"))

    def test_semantic_link_cannot_be_causal_proof(self):
        self.reject(lambda d: d["records"][3].update(evidence_effect="SUPPORT_SCOPED"))

    def test_untyped_gap_rejected(self):
        self.reject(lambda d: d["records"][2].update(gaps=["unknown"]))

    def test_unknown_category_rejected(self):
        self.reject(lambda d: d["records"][0]["conduct"].append("SILENT_PROMOTION"))

    def test_causal_claim_rejected(self):
        self.reject(lambda d: d["records"][1].update(causal_claim=True))

    def test_duplicate_record_rejected(self):
        self.reject(lambda d: d["records"].append(copy.deepcopy(d["records"][0])))

if __name__ == "__main__":
    unittest.main()
