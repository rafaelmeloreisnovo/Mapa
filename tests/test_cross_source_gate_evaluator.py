#!/usr/bin/env python3
"""Tests for the growth-safe cross-source gate evaluator."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "evaluate_cross_source_gate.py"
SPEC = importlib.util.spec_from_file_location("cross_source_gate_evaluator", MODULE_PATH)
assert SPEC and SPEC.loader
EVALUATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVALUATOR)


def baseline() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    floor = {
        "schema_version": "rafaelia.cross-source-gate-floor/v1",
        "minimums": {
            "tests_run": 38,
            "valid_fixtures": 2,
            "invalid_fixtures": 1,
            "registry_records": 10,
            "provider_counts": {"github": 2, "google_drive": 8},
            "custody_events": 13,
        },
        "invariants": {
            "unexpected_failures": 0,
            "unexpected_passes": 0,
            "defect_count": 0,
            "claim_allowed": False,
            "remote_ci_substituted": False,
        },
    }
    records = {
        "status": "PASS",
        "valid_fixture_count": 2,
        "invalid_fixture_count": 1,
        "unexpected_failures": 0,
        "unexpected_passes": 0,
        "claim_allowed": False,
    }
    registry = {
        "status": "PASS",
        "record_count": 10,
        "provider_counts": {"github": 2, "google_drive": 8},
        "defect_count": 0,
        "claim_allowed": False,
    }
    custody = {
        "status": "PASS",
        "event_count": 13,
        "defect_count": 0,
        "claim_allowed": False,
    }
    tests = {
        "status": "PASS",
        "tests_run": 38,
        "failures": 0,
        "errors": 0,
        "claim_allowed": False,
        "remote_ci_substituted": False,
    }
    return floor, records, registry, custody, tests


class CrossSourceGateEvaluatorTests(unittest.TestCase):
    def test_floor_snapshot_passes(self) -> None:
        report = EVALUATOR.evaluate(*baseline())
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["failed_check_count"], 0)
        self.assertEqual(report["promotion_state"], "LOCAL_PASS_REMOTE_TOKEN_VAZIO")
        self.assertFalse(report["claim_allowed"])

    def test_append_only_growth_passes_without_editing_floor(self) -> None:
        floor, records, registry, custody, tests = baseline()
        records["valid_fixture_count"] = 5
        registry["record_count"] = 27
        registry["provider_counts"] = {"github": 12, "google_drive": 15}
        custody["event_count"] = 31
        tests["tests_run"] = 52
        report = EVALUATOR.evaluate(floor, records, registry, custody, tests)
        self.assertEqual(report["status"], "PASS")

    def test_registry_shrink_is_blocked(self) -> None:
        floor, records, registry, custody, tests = baseline()
        registry["record_count"] = 9
        report = EVALUATOR.evaluate(floor, records, registry, custody, tests)
        self.assertEqual(report["status"], "FAIL")
        failed_names = {
            check["name"] for check in report["checks"] if not check["passed"]
        }
        self.assertIn("registry.record_count", failed_names)

    def test_test_count_regression_is_blocked(self) -> None:
        floor, records, registry, custody, tests = baseline()
        tests["tests_run"] = 37
        report = EVALUATOR.evaluate(floor, records, registry, custody, tests)
        self.assertEqual(report["status"], "FAIL")

    def test_claim_promotion_inside_local_gate_is_blocked(self) -> None:
        floor, records, registry, custody, tests = baseline()
        registry["claim_allowed"] = True
        report = EVALUATOR.evaluate(floor, records, registry, custody, tests)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["promotion_state"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
