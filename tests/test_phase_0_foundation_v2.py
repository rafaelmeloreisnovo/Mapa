#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_phase_0_foundation_v2.py"
SECURITY_PATH = ROOT / "tools" / "phase_0_security_audit_v2.py"
MANIFEST_PATH = ROOT / "data" / "control-plane" / "phase_0_foundation_manifest.v1.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module("phase_0_foundation_validator_v2", VALIDATOR_PATH)
security = load_module("phase_0_security_audit_v2", SECURITY_PATH)


class Phase0FoundationV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_all_strict_checks_pass(self):
        checks = validator.run_checks(ROOT, self.manifest)
        self.assertEqual({result["status"] for result in checks.values()}, {"PASS"}, checks)
        self.assertEqual(
            len(checks["observation_coverage"]["details"]["required"]),
            8,
        )

    def test_empty_manifest_sections_are_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["token_vazio_entries"] = []
        ok, message, _ = validator.check_manifest_contract(ROOT, manifest)
        self.assertFalse(ok)
        self.assertIn("exactly 4", message)

    def test_claim_allowed_true_is_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["claim_allowed"] = True
        ok, message, _ = validator.check_claim_allowed(ROOT, manifest)
        self.assertFalse(ok)
        self.assertIn("claim_allowed", message)

    def test_missing_document_marker_is_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["required_documentation"][0]["markers"].append("MARKER_NOT_PRESENT")
        ok, _, _ = validator.check_documentation(ROOT, manifest)
        self.assertFalse(ok)

    def test_missing_falsifier_is_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["token_vazio_entries"][0]["falsifier"] = ""
        ok, _, _ = validator.check_falsifiers(ROOT, manifest)
        self.assertFalse(ok)

    def test_missing_token_approval_location_is_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["token_vazio_entries"][0]["approval_location"]["marker"] = "MARKER_NOT_PRESENT"
        ok, _, _ = validator.check_token_locations(ROOT, manifest)
        self.assertFalse(ok)

    def test_duplicate_evidence_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "duplicate.json").write_text(
                json.dumps({"a": {"evidence_id": "E-1"}, "b": {"evidence_id": "E-1"}}),
                encoding="utf-8",
            )
            ok, _, details = validator.check_evidence_uniqueness(
                root, {"files": ["duplicate.json"], "key": "evidence_id"}
            )
            self.assertFalse(ok)
            self.assertEqual(details["duplicates"][0].split(":", 1)[0], "E-1")

    def test_cycle_in_lane_graph_is_rejected(self):
        dag = copy.deepcopy(self.manifest["gates"]["lane_dag"])
        dag["dependencies"]["R1"] = ["R3"]
        ok, message, _ = validator.check_lane_dag(dag)
        self.assertFalse(ok)
        self.assertIn("cycle", message)

    def test_missing_observation_row_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            matrix = root / "matrix.md"
            matrix.write_text("| O1 | state | VERIFIED | evidence | next |\n", encoding="utf-8")
            ok, _, _ = validator.check_observation_coverage(
                root, {"path": "matrix.md", "observations": ["O1", "O2"]}
            )
            self.assertFalse(ok)

    def test_audit_logs_are_readable(self):
        ok, _, details = validator.check_audit_logs(ROOT, self.manifest["audit_logs"])
        self.assertTrue(ok, details)
        self.assertEqual(len(details["checked"]), 5)

    def test_security_audit_preserves_open_action_finding(self):
        receipt = security.run_audits(ROOT)
        self.assertFalse(receipt["claim_allowed"])
        self.assertNotEqual(receipt["status"], "FAIL")
        self.assertIn("S1-03", receipt["summary"]["open_findings"])


if __name__ == "__main__":
    unittest.main()
