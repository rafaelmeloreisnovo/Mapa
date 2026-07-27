#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sementeira_defensive_ranker.py"
SPEC = importlib.util.spec_from_file_location("sementeira_defensive_ranker", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
REGISTRY = Path(__file__).resolve().parents[1] / "data" / "sementeira" / "defensive-strategy-registry.v1.json"


class DefensiveRankerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_registry_passes(self) -> None:
        result = MODULE.evaluate_registry(self.payload)
        self.assertEqual(result["status"], "PASS", result)

    def test_dignity_gate_is_mandatory(self) -> None:
        result = MODULE.evaluate_registry(self.payload)
        states = {item["strategy_id"]: item["state"] for item in result["ranking"]}
        self.assertEqual(states["STRAT-005-DIGNITY-GATE"], "P0_MANDATORY_GUARDRAIL")

    def test_dual_risk_is_mandatory(self) -> None:
        result = MODULE.evaluate_registry(self.payload)
        states = {item["strategy_id"]: item["state"] for item in result["ranking"]}
        self.assertEqual(states["STRAT-004-DUAL-RISK"], "P0_MANDATORY_GUARDRAIL")

    def test_restricted_lab_is_quarantined(self) -> None:
        result = MODULE.evaluate_registry(self.payload)
        states = {item["strategy_id"]: item["state"] for item in result["ranking"]}
        self.assertEqual(states["STRAT-007-RESTRICTED-LAB"], "P3_QUARANTINE")

    def test_high_risk_detail_is_prohibited(self) -> None:
        result = MODULE.evaluate_registry(self.payload)
        states = {item["strategy_id"]: item["state"] for item in result["ranking"]}
        self.assertEqual(states["STRAT-008-PROHIBITED-DETAIL"], "P4_PROHIBITED")

    def test_missing_forbidden_output_fails(self) -> None:
        item = dict(self.payload["strategies"][0])
        item["forbidden_outputs"] = [x for x in item["forbidden_outputs"] if x != "CAT-HR-04"]
        errors = MODULE.validate_strategy(item)
        self.assertTrue(any("forbidden_outputs missing" in error for error in errors))

    def test_claim_promotion_fails(self) -> None:
        item = dict(self.payload["strategies"][0])
        item["claim_allowed"] = True
        errors = MODULE.validate_strategy(item)
        self.assertIn("claim_allowed must remain false", errors)

    def test_authorization_is_mandatory(self) -> None:
        item = dict(self.payload["strategies"][0])
        item["authorization_required"] = False
        errors = MODULE.validate_strategy(item)
        self.assertIn("authorization_required must be true", errors)

    def test_operational_k4_detail_fails(self) -> None:
        item = dict(self.payload["strategies"][-1])
        item["high_risk_detail_present"] = True
        errors = MODULE.validate_strategy(item)
        self.assertIn("K4 entries must not preserve high-risk operational detail", errors)

    def test_order_starts_with_mandatory_guardrails(self) -> None:
        result = MODULE.evaluate_registry(self.payload)
        self.assertEqual(result["ranking"][0]["state"], "P0_MANDATORY_GUARDRAIL")


if __name__ == "__main__":
    unittest.main()
