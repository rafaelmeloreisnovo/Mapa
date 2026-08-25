#!/usr/bin/env python3

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_omega_assurance_mesh_v1.py"
SPEC = importlib.util.spec_from_file_location("omega_mesh_validator", VALIDATOR)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MOD)


class OmegaAssuranceMeshV1Tests(unittest.TestCase):
    def load(self, name):
        path = ROOT / "data" / "fixtures" / "omega-assurance" / name
        return json.loads(path.read_text(encoding="utf-8"))

    def test_real_bundle_passes(self):
        self.assertEqual(MOD.validate_bundle(ROOT), [])

    def test_positive_node_passes(self):
        self.assertEqual(MOD.validate_node(self.load("valid-node.v1.json")), [])

    def test_positive_transition_passes(self):
        self.assertEqual(MOD.validate_transition(self.load("valid-transition.v1.json")), [])

    def test_positive_watchdog_event_passes(self):
        self.assertEqual(MOD.validate_watchdog_event(self.load("valid-watchdog-event.v1.json")), [])

    def test_token_vazio_promotion_is_rejected(self):
        errors = MOD.validate_node(self.load("invalid-token-vazio-promotion.v1.json"))
        self.assertTrue(any("cannot allow claim" in error for error in errors))

    def test_unknown_authority_transition_is_rejected(self):
        errors = MOD.validate_transition(self.load("invalid-authority-transition.v1.json"))
        self.assertTrue(any("authority" in error or "privacy" in error for error in errors))

    def test_watchdog_overreaction_is_rejected(self):
        errors = MOD.validate_watchdog_event(self.load("invalid-watchdog-overreaction.v1.json"))
        self.assertTrue(any("ACT_BOUNDED" in error or "heartbeat" in error for error in errors))

    def test_p0_cannot_be_compensated(self):
        event = self.load("valid-transition.v1.json")
        event["risk_after"]["p0_dimensions"] = ["privacy"]
        event["watchdog_state"] = "ACT_BOUNDED"
        errors = MOD.validate_transition(event)
        self.assertTrue(any("P0" in error for error in errors))

    def test_unknown_rollback_on_promotion_holds(self):
        event = self.load("valid-transition.v1.json")
        event["authority"]["operation"] = "PROMOTE"
        event["rollback"]["state"] = "TOKEN_VAZIO"
        event["watchdog_state"] = "ACT_BOUNDED"
        errors = MOD.validate_transition(event)
        self.assertTrue(any("unknown risk" in error for error in errors))

    def test_private_locator_detector(self):
        self.assertTrue(MOD.contains_private_locator("https://drive.google.com/file/d/example"))
        self.assertFalse(MOD.contains_private_locator("governance/public-contract.json"))


if __name__ == "__main__":
    unittest.main()
