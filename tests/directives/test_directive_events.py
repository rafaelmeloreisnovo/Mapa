#!/usr/bin/env python3
from __future__ import annotations
import copy, importlib.util, json, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts/validate_directive_events.py"
SPEC = importlib.util.spec_from_file_location("directive_validator", MODULE)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)
EVENTS = ROOT / "data/directives/directive_events.20260803.jsonl"

def load_event() -> dict:
    return json.loads(EVENTS.read_text(encoding="utf-8").splitlines()[0])

class DirectiveEventTests(unittest.TestCase):
    def test_current_event_passes(self) -> None:
        self.assertEqual(validator.validate_event(load_event()), [])

    def test_promotion_effect_is_rejected(self) -> None:
        broken = load_event()
        broken["effects"].append("PROMOTE")
        self.assertTrue(any("PROMOTE is forbidden" in x for x in validator.validate_event(broken)))

    def test_retroactive_effect_is_rejected(self) -> None:
        broken = load_event()
        broken["retroactive"] = True
        self.assertTrue(any("retroactive" in x for x in validator.validate_event(broken)))

    def test_write_requires_authorization(self) -> None:
        broken = load_event()
        broken["authorization"]["github_write"] = False
        broken["authorization"]["drive_write"] = False
        self.assertTrue(any("WRITE effect requires" in x for x in validator.validate_event(broken)))

    def test_destructive_target_operation_is_rejected(self) -> None:
        broken = load_event()
        broken["target_surfaces"][0]["operation"] = "DELETE"
        self.assertTrue(any("invalid or destructive" in x for x in validator.validate_event(broken)))

    def test_claim_promotion_is_rejected(self) -> None:
        broken = load_event()
        broken["authorization"]["claim_promotion"] = True
        broken["classification"]["claim_allowed"] = True
        errors = validator.validate_event(broken)
        self.assertTrue(any("claim_promotion" in x for x in errors))
        self.assertTrue(any("claim_allowed" in x for x in errors))

    def test_source_hash_shape_is_enforced(self) -> None:
        broken = load_event()
        broken["source"]["content_sha256"] = "abc"
        self.assertTrue(any("64 lowercase hex" in x for x in validator.validate_event(broken)))

    def test_report_is_deterministic(self) -> None:
        self.assertEqual(validator.build_report(EVENTS), validator.build_report(EVENTS))
        self.assertEqual(validator.build_report(EVENTS)["status"], "PASS")

    def test_duplicate_id_is_rejected(self) -> None:
        raw = EVENTS.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            path.write_text(raw + raw, encoding="utf-8")
            report = validator.build_report(path)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("duplicate directive_id" in x for x in report["defects"]))

if __name__ == "__main__":
    unittest.main()
