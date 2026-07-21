from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "scripts"))

from build_claim_scope_refresh import build_refresh, canonical_digest as build_digest
from validate_claim_scope_refresh import (
    ScopeRefreshValidationError,
    canonical_digest,
    validate,
)

CURRENT_COMMIT = "a" * 40


class ClaimScopeRefreshValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        entries = [
            {
                "id": f"CC{index:03d}",
                "path": f"docs/baseline-{index:03d}.md",
                "review_state": "TOKEN_VAZIO" if index > 6 else "REVIEWED_SAFE",
            }
            for index in range(1, 37)
        ]
        ledger = {
            "schema": "mapa.claim-contradiction-ledger.v1",
            "source_snapshot": {"commit": "4" * 40},
            "entries": entries,
            "integrity": {"digest": "1" * 64},
        }
        head = {
            "schema": "mapa.claim-contradiction-head.v1",
            "derived": {
                "reviewed_safe_count": 36,
                "reviewed_blocking_count": 0,
                "token_vazio_count": 0,
                "claim_allowed": False,
            },
            "integrity": {"digest": "2" * 64},
        }
        claim_scan = {
            "schema": "mapa.claim-vocabulary-scan.v1",
            "status": "PASS",
            "claim_allowed": False,
            "explicit_claim_error_count": 0,
            "warnings_truncated": False,
            "warnings": [
                {
                    "path": "docs/baseline-001.md",
                    "class": "POTENTIAL_PROSE_CONTRADICTION",
                    "strong_tokens": ["COMPLETE"],
                    "pending_tokens": ["TOKEN_VAZIO"],
                },
                {
                    "path": "docs/new-control.md",
                    "class": "POTENTIAL_PROSE_CONTRADICTION",
                    "strong_tokens": ["ALIGNED"],
                    "pending_tokens": ["PENDING"],
                },
            ],
        }
        precision = {
            "schema": "mapa.claim-discovery-precision.v1",
            "status": "PASS",
            "claim_allowed": False,
            "files_scanned": 10,
            "files_skipped_by_size": 0,
            "unreadable_file_count": 0,
            "exact_token_files_truncated": False,
            "exact_token_files": [
                {"path": "docs/baseline-001.md", "tokens": {"COMPLETE": 1}},
                {"path": "docs/new-control.md", "tokens": {"ALIGNED": 1}},
                {"path": "docs/new-only.md", "tokens": {"CERTIFIED": 1}},
            ],
        }
        cls.base = build_refresh(
            ledger=ledger,
            head=head,
            claim_scan=claim_scan,
            precision=precision,
            current_commit=CURRENT_COMMIT,
        )

    def reseal(self, report):
        report["integrity"]["digest"] = canonical_digest(report)

    def test_current_fixture_validates(self):
        result = validate(copy.deepcopy(self.base))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["baseline_candidate_count"], 36)
        self.assertEqual(result["new_candidate_count"], 2)
        self.assertTrue(result["all_new_candidates_token_vazio"])
        self.assertTrue(result["review_required"])
        self.assertFalse(result["claim_allowed"])
        self.assertEqual(self.base["integrity"]["digest"], build_digest(self.base))

    def test_nondeterministic_candidate_id_rejected(self):
        report = copy.deepcopy(self.base)
        report["new_candidates"][0]["id"] = "NCC-000000000000"
        self.reseal(report)
        with self.assertRaises(ScopeRefreshValidationError):
            validate(report)

    def test_new_candidate_promotion_rejected(self):
        report = copy.deepcopy(self.base)
        report["new_candidates"][0]["state"] = "REVIEWED_SAFE"
        self.reseal(report)
        with self.assertRaises(ScopeRefreshValidationError):
            validate(report)

    def test_new_candidate_claim_promotion_rejected(self):
        report = copy.deepcopy(self.base)
        report["new_candidates"][0]["claim_allowed"] = True
        self.reseal(report)
        with self.assertRaises(ScopeRefreshValidationError):
            validate(report)

    def test_path_overlap_rejected(self):
        report = copy.deepcopy(self.base)
        report["baseline_without_current_signal"][0]["path"] = report["known_baseline_signals"][0]["path"]
        self.reseal(report)
        with self.assertRaises(ScopeRefreshValidationError):
            validate(report)

    def test_count_tampering_rejected(self):
        report = copy.deepcopy(self.base)
        report["derived"]["new_candidate_count"] += 1
        self.reseal(report)
        with self.assertRaises(ScopeRefreshValidationError):
            validate(report)

    def test_candidate_path_arithmetic_rejected(self):
        report = copy.deepcopy(self.base)
        report["current_scan"]["candidate_path_count"] += 1
        self.reseal(report)
        with self.assertRaises(ScopeRefreshValidationError):
            validate(report)

    def test_review_required_cannot_be_suppressed(self):
        report = copy.deepcopy(self.base)
        report["derived"]["review_required"] = False
        self.reseal(report)
        with self.assertRaises(ScopeRefreshValidationError):
            validate(report)

    def test_next_gate_cannot_skip_review(self):
        report = copy.deepcopy(self.base)
        report["derived"]["next_gate"] = "PRODUCE_FULL_BYTE_REPOSITORY_RECEIPT"
        self.reseal(report)
        with self.assertRaises(ScopeRefreshValidationError):
            validate(report)

    def test_each_boundary_is_fail_closed(self):
        for key in self.base["boundaries"]:
            with self.subTest(boundary=key):
                report = copy.deepcopy(self.base)
                report["boundaries"][key] = True
                self.reseal(report)
                with self.assertRaises(ScopeRefreshValidationError):
                    validate(report)

    def test_integrity_tampering_rejected(self):
        report = copy.deepcopy(self.base)
        report["current_scan"]["files_scanned"] += 1
        with self.assertRaises(ScopeRefreshValidationError):
            validate(report)


if __name__ == "__main__":
    unittest.main()
