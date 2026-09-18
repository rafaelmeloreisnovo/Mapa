#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_systematic_pragmatic_g3_decisions.py"

spec = importlib.util.spec_from_file_location("g3_validator", VALIDATOR)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def base_row():
    return {
        "schema": "rafaelia.systematic-pragmatic-g3-decision/v1",
        "decision_id": "G3-CL-test-20260918",
        "cluster_id": "CL-0123456789abcdef",
        "source": {
            "workflow_run_id": 1,
            "workflow_run_number": 1,
            "artifact_id": 2,
            "artifact_digest": "sha256:" + "a" * 64,
            "tested_head": "b" * 40,
        },
        "observed": {
            "action_count": 3,
            "domain": "data",
            "service": "SEMANTIC_TRIAGE",
            "markers": ["TOKEN_VAZIO"],
            "nibiguiri_state": "NIBIGUIRI:CAUSA_DESCONHECIDA",
            "distinct_subdomains": 2,
            "subdomain_counts": {"routing": 2, "receipts": 1},
            "sample_paths": ["data/routing/a.json", "data/receipts/b.json"],
        },
        "decision": "SPLIT_REQUIRED",
        "reason": "Two distinct subdomains require independent review.",
        "invariants": ["SAME_CLUSTER != SAME_MEANING"],
        "g4_authority_bind_gate": {
            "state": "BLOCKED_BY_G3_SPLIT",
            "binding": "TOKEN_VAZIO",
            "auto_create_gap_id": False,
        },
        "next_gate": "Split and review children.",
        "claim_allowed": False,
    }


class G3DecisionValidationTest(unittest.TestCase):
    def test_valid_split_required_passes(self):
        report = mod.validate([base_row()])
        self.assertEqual(report["status"], "PASS")
        self.assertFalse(report["claim_allowed"])
        self.assertEqual(report["by_decision"], {"SPLIT_REQUIRED": 1})

    def test_split_required_cannot_bind_or_autocreate(self):
        row = base_row()
        row["g4_authority_bind_gate"]["auto_create_gap_id"] = True
        row["g4_authority_bind_gate"]["binding"] = "GAP-AUTO-001"
        report = mod.validate([row])
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("auto_create_gap_id" in e for e in report["errors"]))
        self.assertTrue(any("binding must remain TOKEN_VAZIO" in e for e in report["errors"]))

    def test_same_family_requires_evidence(self):
        row = base_row()
        row["decision"] = "SAME_FAMILY"
        row["g4_authority_bind_gate"]["state"] = "BLOCKED_BY_G3"
        report = mod.validate([row])
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("SAME_FAMILY requires evidence_refs" in e for e in report["errors"]))

    def test_subdomain_count_must_reconcile(self):
        row = base_row()
        row["observed"]["action_count"] = 4
        report = mod.validate([row])
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("subdomain_counts sum" in e for e in report["errors"]))


if __name__ == "__main__":
    unittest.main()
