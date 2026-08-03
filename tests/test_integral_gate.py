#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_integral_gate", ROOT / "tools" / "verify_integral_gate.py"
)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)

POLICY = json.loads((ROOT / "data" / "control-plane" / "integral-gate.v1.json").read_text())
AUDIT = json.loads(
    (ROOT / "data" / "receipts" / "gates" /
     "integral-gate-execution.20260803T1238-0300.json").read_text()
)


def pass_receipt() -> dict:
    value = copy.deepcopy(AUDIT)
    value["source"]["worktree_clean"] = True
    for criterion in value["criteria"].values():
        criterion["status"] = "PASS"
        criterion.pop("next_verifiable_step", None)

    value["criteria"]["authorship_identified"]["authors"] = [{
        "identity": "rafaelmeloreisnovo",
        "role": "author",
        "commit_sha": value["source"]["commit_sha"],
    }]
    value["criteria"]["build_reproducible"]["build"] = {
        "executed": True,
        "exit_code": 0,
        "toolchain": "python-3.12.4",
        "toolchain_digest": "sha256:" + "a" * 64,
        "commands": [["python", "-m", "py_compile", "tools/verify_integral_gate.py"]],
        "output_sha256": "b" * 64,
        "replay_count": 2,
        "outputs_match": True,
        "receipt": "data/receipts/gates/build.json",
    }
    value["criteria"]["tests_executed"]["tests"] = {
        "counts": {"discovered": 5, "executed": 5, "passed": 5, "failed": 0, "skipped": 0},
        "receipt": "data/receipts/gates/tests.json",
    }
    value["criteria"]["source_commit_bound"]["evidence"] = ["clean checkout observed"]
    value["criteria"]["dependency_provenance"]["dependencies"] = [{
        "name": "python",
        "version_or_ref": "3.12.4",
        "digest": "c" * 64,
    }]
    value["criteria"]["falsifiers_exercised"]["falsifiers"] = [{
        "id": "tampered-receipt",
        "status": "EXERCISED",
    }]
    value["criteria"]["privacy_secret_scan"]["scan"] = {
        "executed": True,
        "findings": 0,
        "receipt": "data/receipts/gates/secret-scan.json",
    }
    value["criteria"]["promotion_control"]["control"] = {
        "automatic_merge": False,
        "human_review_required": True,
        "required_checks": ["RAFAELIA Integral Gate V1"],
        "negative_test_executed": True,
    }
    value["criteria"]["physical_runtime_receipt"]["runtime"] = {
        "physical_device": True,
        "device_class": "ANDROID_TERMUX_LOCAL",
        "receipt": "data/receipts/gates/termux.json",
        "receipt_sha256": "d" * 64,
    }
    value["criteria"]["independent_reproduction"]["reproduction"] = {
        "independent_environment": True,
        "outputs_match": True,
        "receipt": "data/receipts/gates/reproduction.json",
    }
    value["decision"]["result"] = "READY_FOR_DOMAIN_REVIEW"
    value["decision"]["blocking_criteria"] = []
    value["decision"]["promotion"] = "NOT_PERFORMED"
    return value


class IntegralGateTests(unittest.TestCase):
    def test_current_audit_is_valid_but_blocked(self) -> None:
        result = gate.validate(copy.deepcopy(AUDIT), POLICY)
        self.assertTrue(result["receipt_valid"], result["errors"])
        self.assertEqual(result["computed_result"], "BLOCKED_FAIL")
        self.assertIn("tests_executed", result["blocking_criteria"])
        self.assertIn("promotion_control", result["blocking_criteria"])

    def test_complete_fixture_reaches_domain_review_only(self) -> None:
        result = gate.validate(pass_receipt(), POLICY)
        self.assertTrue(result["receipt_valid"], result["errors"])
        self.assertEqual(result["computed_result"], "READY_FOR_DOMAIN_REVIEW")
        self.assertFalse(result["claim_allowed"])

    def test_hypothesis_cannot_enable_claim(self) -> None:
        value = pass_receipt()
        value["criteria"]["claim_compatible"]["claim"]["classification"] = "HIPOTESE"
        value["criteria"]["claim_compatible"]["claim"]["claim_allowed"] = True
        result = gate.validate(value, POLICY)
        self.assertFalse(result["receipt_valid"])
        self.assertTrue(any("non-promotable" in error for error in result["errors"]))

    def test_shell_wrapped_build_is_rejected(self) -> None:
        value = pass_receipt()
        value["criteria"]["build_reproducible"]["build"]["commands"] = [
            ["bash", "-lc", "python -m py_compile tools/verify_integral_gate.py"]
        ]
        result = gate.validate(value, POLICY)
        self.assertFalse(result["receipt_valid"])
        self.assertTrue(any("safe argv" in error for error in result["errors"]))

    def test_hash_pass_requires_verified_artifacts(self) -> None:
        value = pass_receipt()
        value["artifacts"][0]["verified"] = False
        result = gate.validate(value, POLICY)
        self.assertFalse(result["receipt_valid"])
        self.assertTrue(any("every artifact" in error for error in result["errors"]))

    def test_declared_decision_cannot_hide_blocker(self) -> None:
        value = copy.deepcopy(AUDIT)
        value["decision"]["result"] = "READY_FOR_DOMAIN_REVIEW"
        value["decision"]["blocking_criteria"] = []
        result = gate.validate(value, POLICY)
        self.assertFalse(result["receipt_valid"])
        self.assertTrue(any("computed result" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
