"""Bounded adversarial graph tests; synthetic only, no user corpus."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_observer_paths_v1 import validate

DATA = json.loads((ROOT / "data/observations/observer-paths-synthetic.v1.json").read_text(encoding="utf-8"))


def mutated(event_index, key, value):
    d = copy.deepcopy(DATA)
    d["events"][event_index][key] = value
    return d


class ObserverPathTests(unittest.TestCase):
    def test_fixture_is_valid(self):
        self.assertEqual(validate(DATA), [])

    def test_no_global_claim_promotion(self):
        d = copy.deepcopy(DATA)
        d["claim_allowed"] = True
        self.assertIn("GLOBAL_CLAIM_MUST_REMAIN_FALSE", validate(d))

    def test_no_gate_bypass(self):
        d = copy.deepcopy(DATA)
        d["gates"]["promotion"] = "PASS"
        self.assertIn("PROMOTION_MUST_REMAIN_HOLD", validate(d))

    def test_sequence_is_append_order(self):
        self.assertIn("event[4]:SEQUENCE_DRIFT", validate(mutated(3, "sequence", 3)))

    def test_duplicate_event_id_rejected(self):
        self.assertIn("event[3]:DUPLICATE_OR_INVALID_ID",
                      validate(mutated(2, "event_id", "OBS-SYN-001")))

    def test_no_real_reviewer_in_synthetic_record(self):
        d = copy.deepcopy(DATA)
        d["events"][0]["observer"]["mode"] = "HUMAN"
        self.assertIn("event[1]:SYNTHETIC_OBSERVER_AUTHORITY_INVALID", validate(d))

    def test_missing_observation_timestamp_rejected(self):
        self.assertIn("event[1]:OBSERVATION_TIME_MISSING",
                      validate(mutated(0, "observed_at", None)))

    def test_unbound_effective_time_requires_atemporal(self):
        d = copy.deepcopy(DATA)
        d["events"][5]["uncertainty_markers"].remove("ATEMPORAL")
        self.assertIn("event[6]:UNKNOWN_EFFECTIVE_TIME_UNTYPED", validate(d))

    def test_no_fake_source_sha(self):
        d = copy.deepcopy(DATA)
        d["events"][0]["source"]["content_sha256_state"] = "0" * 64
        self.assertIn("event[1]:REAL_PROVENANCE_FABRICATION_OR_MISSING_FIXTURE", validate(d))

    def test_no_fake_evidence_receipt(self):
        d = copy.deepcopy(DATA)
        d["events"][0]["evidence_refs"] = ["fake://proof"]
        self.assertIn("event[1]:REAL_EVIDENCE_MUST_NOT_BE_CLAIMED", validate(d))

    def test_missing_reason_blocks_void(self):
        self.assertIn("event[2]:GAP_REASON_MISSING",
                      validate(mutated(1, "gap_reason", "")))

    def test_no_silent_void_coercion(self):
        self.assertIn("event[2]:UNTYPED_EPISTEMIC_VOID",
                      validate(mutated(1, "uncertainty_markers", ["UNKNOWN"])))

    def test_no_dangling_network_path(self):
        d = copy.deepcopy(DATA)
        d["events"][4]["links"].append({"to": "OBS-SYN-999", "type": "BRANCHES_FROM"})
        self.assertIn("event[5]:DANGLING_FORWARD_OR_INVALID_EDGE", validate(d))

    def test_no_future_supersession(self):
        d = copy.deepcopy(DATA)
        d["events"][3]["links"] = [{"to": "OBS-SYN-008", "type": "SUPERSEDES"}]
        self.assertIn("event[4]:DANGLING_FORWARD_OR_INVALID_EDGE", validate(d))

    def test_no_silent_contradiction_resolution(self):
        d = copy.deepcopy(DATA)
        d["events"][2]["epistemic_state"] = "UNVERIFIED"
        self.assertIn("event[3]:CONTRADICTION_NOT_PRESERVED", validate(d))

    def test_only_correction_can_supersede(self):
        d = copy.deepcopy(DATA)
        d["events"][4]["links"].append({"to": "OBS-SYN-002", "type": "SUPERSEDES"})
        self.assertIn("event[5]:SILENT_OR_UNJUSTIFIED_SUPERSESSION", validate(d))

    def test_no_auto_approval_of_refusal(self):
        self.assertIn("event[7]:REFUSAL_CANNOT_AUTO_APPROVE",
                      validate(mutated(6, "epistemic_state", "UNVERIFIED")))

    def test_no_unknown_science_conduct_without_contract(self):
        d = copy.deepcopy(DATA)
        d["events"][0]["conduct_areas"].append("unbounded_quantum_cause")
        self.assertIn("event[1]:CONDUCT_INVALID", validate(d))

    def test_no_unreviewed_new_category_without_fixture(self):
        d = copy.deepcopy(DATA)
        d["approved_uncertainty_markers"].append("NEW_UNTESTED")
        self.assertTrue(any(e.startswith("UNTESTED_UNCERTAINTY_MARKERS") for e in validate(d)))

    def test_no_claim_on_multi_path_causality(self):
        d = copy.deepcopy(DATA)
        d["events"][7]["claim_allowed"] = True
        self.assertIn("event[8]:CAUSAL_PROMOTION_FORBIDDEN", validate(d))
        self.assertIn("event[8]:EVENT_CLAIM_MUST_REMAIN_FALSE", validate(d))


if __name__ == "__main__":
    unittest.main()
