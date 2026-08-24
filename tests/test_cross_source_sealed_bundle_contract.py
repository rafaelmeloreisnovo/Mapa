#!/usr/bin/env python3
"""Prevent drift between the sealed-bundle producer, comparator and workflow."""

from __future__ import annotations

import importlib.util
import inspect
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPARATOR_PATH = ROOT / "scripts" / "compare_cross_source_evidence.py"
GATE_PATH = ROOT / "scripts" / "run_cross_source_gate.sh"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "cross-source-record-validation.yml"

SPEC = importlib.util.spec_from_file_location("cross_source_comparator", COMPARATOR_PATH)
assert SPEC and SPEC.loader
comparator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(comparator)


class SealedBundleContractTests(unittest.TestCase):
    def test_comparator_uses_exact_gate_output_names(self) -> None:
        self.assertEqual(
            comparator.REPORT_NAMES,
            [
                "cross-source-test-validation.json",
                "cross-source-record-validation.json",
                "cross-source-registry-validation.json",
                "chain-of-custody-validation.json",
                "quality-floor-validation.json",
            ],
        )
        self.assertEqual(comparator.MANIFEST_NAME, "LOCAL_GATE_STATUS.json")
        self.assertEqual(comparator.CHECKSUMS_NAME, "CHECKSUMS.sha256")

    def test_validate_bundle_accepts_floor_binding_parameter(self) -> None:
        signature = inspect.signature(comparator.validate_bundle)
        self.assertEqual(list(signature.parameters), ["directory", "floor_path"])

    def test_workflow_calls_current_validate_bundle_api(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("comparator.validate_bundle(root, floor_path)", workflow)
        self.assertIn('bundle["status"] == "PASS"', workflow)

    def test_gate_and_comparator_share_manifest_and_report_names(self) -> None:
        gate = GATE_PATH.read_text(encoding="utf-8")
        for name in [comparator.MANIFEST_NAME, comparator.CHECKSUMS_NAME, *comparator.REPORT_NAMES]:
            with self.subTest(name=name):
                self.assertIn(name, gate)


if __name__ == "__main__":
    unittest.main()
