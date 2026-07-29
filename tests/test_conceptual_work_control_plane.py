import copy
import json
import unittest
from pathlib import Path
from scripts.validate_conceptual_work_control_plane import validate

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads(
    (ROOT / "indices/CONCEPTUAL_WORK_CONTROL_PLANE.json").read_text(encoding="utf-8")
)


class TestConceptualWorkControlPlane(unittest.TestCase):
    def test_canonical_passes(self):
        self.assertEqual(validate(copy.deepcopy(DATA))["status"], "PASS")

    def test_claim_promotion_blocked(self):
        data = copy.deepcopy(DATA)
        data["scope"]["claim_allowed"] = True
        self.assertEqual(validate(data)["status"], "FAIL")

    def test_hash_cannot_be_truth(self):
        data = copy.deepcopy(DATA)
        data["invariants"].remove("hash != truth")
        self.assertEqual(validate(data)["status"], "FAIL")

    def test_missing_layer_fails(self):
        data = copy.deepcopy(DATA)
        data["layers"].pop()
        self.assertEqual(validate(data)["status"], "FAIL")

    def test_duplicate_decision_fails(self):
        data = copy.deepcopy(DATA)
        data["decisions"][-1]["id"] = "D001"
        self.assertEqual(validate(data)["status"], "FAIL")

    def test_non_token_blocker_fails(self):
        data = copy.deepcopy(DATA)
        data["open_blockers"][0]["state"] = "PASS"
        self.assertEqual(validate(data)["status"], "FAIL")

    def test_reference_cannot_claim_compliance(self):
        data = copy.deepcopy(DATA)
        data["references"][0]["claim"] = "COMPLIANT"
        self.assertEqual(validate(data)["status"], "FAIL")

    def test_journal_requires_hash_chain(self):
        data = copy.deepcopy(DATA)
        data["journal_contract"]["required_fields"].remove("previous_event_sha256")
        self.assertEqual(validate(data)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
