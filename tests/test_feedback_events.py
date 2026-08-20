from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_feedback_events import canonical_hash, validate


def reseal(events):
    previous = None
    for index, event in enumerate(events, 1):
        event["sequence"] = index
        event["prev_event_hash"] = previous
        event["event_hash"] = canonical_hash(event)
        previous = event["event_hash"]
    return events


class FeedbackEventTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "ledger.jsonl"
        self.events = [
            {
                "schema": "rafaelia.feedback-event/v1",
                "sequence": 1,
                "event_id": "FEVT-20260820-BASELINE",
                "observed_at": "2026-08-20T11:28:00-03:00",
                "objective": "baseline control-plane observation",
                "source_refs": ["repo:Mapa@abc"],
                "transition_kind": "OBSERVATION",
                "prior_state": "TOKEN_VAZIO",
                "observed_state": "PARTIAL",
                "evidence_refs": ["file:README.md"],
                "gate_id": None,
                "F_ok": ["baseline observed"],
                "F_gap": ["runtime not executed"],
                "F_next": ["execute deterministic validator"],
                "claim_allowed": False,
                "predecessor_event_ids": [],
                "prev_event_hash": None,
                "leverage_class": "SYSTEMIC",
                "leverage_basis": "feeds every later control-plane decision",
                "event_hash": ""
            },
            {
                "schema": "rafaelia.feedback-event/v1",
                "sequence": 2,
                "event_id": "FEVT-20260820-VALIDATOR",
                "observed_at": "2026-08-20T11:29:00-03:00",
                "objective": "baseline control-plane observation",
                "source_refs": ["repo:Mapa@abc"],
                "transition_kind": "EXECUTION",
                "prior_state": "PARTIAL",
                "observed_state": "VERIFIED_LIMITED",
                "evidence_refs": ["run:validator-pass"],
                "gate_id": "GATE-FEVENT-001",
                "F_ok": ["validator executed"],
                "F_gap": ["remote CI not observed"],
                "F_next": ["run CI on branch"],
                "claim_allowed": False,
                "predecessor_event_ids": ["FEVT-20260820-BASELINE"],
                "prev_event_hash": None,
                "leverage_class": "MULTIPLICATIVE",
                "leverage_basis": "one invariant protects multiple future workflows",
                "event_hash": ""
            }
        ]
        self.write(reseal(copy.deepcopy(self.events)))

    def tearDown(self):
        self.temp.cleanup()

    def write(self, events):
        self.path.write_text(
            "\n".join(json.dumps(event, ensure_ascii=False, separators=(",", ":")) for event in events) + "\n",
            encoding="utf-8"
        )

    def test_valid_baseline_passes(self):
        self.assertEqual(validate(self.path)["status"], "PASS")

    def test_duplicate_id_rejected(self):
        events = copy.deepcopy(self.events)
        events[1]["event_id"] = events[0]["event_id"]
        self.write(reseal(events))
        self.assertEqual(validate(self.path)["status"], "FAIL")

    def test_tamper_rejected(self):
        events = reseal(copy.deepcopy(self.events))
        events[0]["F_ok"] = ["tampered"]
        self.write(events)
        self.assertEqual(validate(self.path)["status"], "FAIL")

    def test_future_predecessor_rejected(self):
        events = copy.deepcopy(self.events)
        events[0]["predecessor_event_ids"] = [events[1]["event_id"]]
        self.write(reseal(events))
        self.assertEqual(validate(self.path)["status"], "FAIL")

    def test_silent_downgrade_rejected(self):
        events = copy.deepcopy(self.events)
        third = copy.deepcopy(events[1])
        third["event_id"] = "FEVT-20260820-DOWN"
        third["transition_kind"] = "OBSERVATION"
        third["prior_state"] = "VERIFIED_LIMITED"
        third["observed_state"] = "PARTIAL"
        third["evidence_refs"] = []
        third["predecessor_event_ids"] = [events[1]["event_id"]]
        events.append(third)
        self.write(reseal(events))
        self.assertEqual(validate(self.path)["status"], "FAIL")

    def test_evidence_correction_allows_downgrade(self):
        events = copy.deepcopy(self.events)
        third = copy.deepcopy(events[1])
        third["event_id"] = "FEVT-20260820-CORR"
        third["transition_kind"] = "CORRECTION"
        third["prior_state"] = "VERIFIED_LIMITED"
        third["observed_state"] = "PARTIAL"
        third["evidence_refs"] = ["receipt:new-contrary-evidence"]
        third["predecessor_event_ids"] = [events[1]["event_id"]]
        events.append(third)
        self.write(reseal(events))
        self.assertEqual(validate(self.path)["status"], "PASS")

    def test_claim_without_gate_rejected(self):
        events = copy.deepcopy(self.events)
        events[1]["claim_allowed"] = True
        events[1]["transition_kind"] = "PROMOTION"
        events[1]["observed_state"] = "VERIFIED"
        events[1]["gate_id"] = None
        self.write(reseal(events))
        self.assertEqual(validate(self.path)["status"], "FAIL")

    def test_promotion_with_gate_and_evidence_passes(self):
        events = copy.deepcopy(self.events)
        events[1]["claim_allowed"] = True
        events[1]["transition_kind"] = "PROMOTION"
        events[1]["observed_state"] = "VERIFIED"
        events[1]["gate_id"] = "GATE-FEVENT-001"
        events[1]["evidence_refs"] = ["receipt:gate"]
        self.write(reseal(events))
        self.assertEqual(validate(self.path)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
