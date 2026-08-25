#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_json_totality_invariants.py"
spec = importlib.util.spec_from_file_location("json_totality", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class JsonTotalityInvariantTests(unittest.TestCase):
    def test_passing_message_fixture(self):
        path = ROOT / "tests" / "fixtures" / "json_totality" / "messages-pass.jsonl"
        findings = [mod.audit_record(obj, path, idx) for idx, obj in mod.iter_records(path)]
        report = mod.summarize(findings, [path])
        self.assertEqual(report["state"], "PASS")
        self.assertEqual(report["conservation_rate"], 1.0)
        self.assertEqual(report["governed_gap"], 0)
        for dimension in report["dimension_coverage"].values():
            self.assertEqual(dimension["coverage"], 1.0)

    def test_gap_fixture_fails_closed(self):
        path = ROOT / "tests" / "fixtures" / "json_totality" / "messages-gap.jsonl"
        findings = [mod.audit_record(obj, path, idx) for idx, obj in mod.iter_records(path)]
        report = mod.summarize(findings, [path])
        self.assertEqual(report["state"], "GAP")
        self.assertEqual(report["conservation_rate"], 0.0)
        gaps = {g for f in findings for g in f.gaps}
        self.assertIn("TOKEN_VAZIO_MESSAGE_SOURCE_POINTER_ABSENT", gaps)
        self.assertIn("TOKEN_VAZIO_MESSAGE_TEXT_HASH_ABSENT", gaps)

    def test_longitudinal_contract_matches_existing_mandatory_invariants(self):
        expected = {
            "source_is_not_interpretation",
            "parable_is_not_physical_proof",
            "token_vazio_is_not_zero",
            "new_dimension_requires_semantics_type_source_and_state",
            "weights_require_calibration_and_evidence",
            "no_hidden_model_state_claim",
            "append_never_silently_overwrites_ancestor",
            "relation_requires_type_and_source",
        }
        self.assertEqual(mod.LONGITUDINAL_INVARIANTS, expected)


if __name__ == "__main__":
    unittest.main()
