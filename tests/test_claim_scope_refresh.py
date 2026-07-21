from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "scripts"))

from build_claim_scope_refresh import (
    ScopeRefreshError,
    build_refresh,
    canonical_digest,
    stable_candidate_id,
)

CURRENT_COMMIT = "a" * 40


class ClaimScopeRefreshTests(unittest.TestCase):
    def setUp(self):
        entries = [
            {
                "id": f"CC{index:03d}",
                "path": f"docs/baseline-{index:03d}.md",
                "review_state": "TOKEN_VAZIO" if index > 6 else "REVIEWED_SAFE",
            }
            for index in range(1, 37)
        ]
        self.ledger = {
            "schema": "mapa.claim-contradiction-ledger.v1",
            "source_snapshot": {"commit": "4" * 40},
            "entries": entries,
            "integrity": {"digest": "1" * 64},
        }
        self.head = {
            "schema": "mapa.claim-contradiction-head.v1",
            "derived": {
                "reviewed_safe_count": 36,
                "reviewed_blocking_count": 0,
                "token_vazio_count": 0,
                "claim_allowed": False,
            },
            "integrity": {"digest": "2" * 64},
        }
        self.claim_scan = {
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
        self.precision = {
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

    def build(self):
        return build_refresh(
            ledger=copy.deepcopy(self.ledger),
            head=copy.deepcopy(self.head),
            claim_scan=copy.deepcopy(self.claim_scan),
            precision=copy.deepcopy(self.precision),
            current_commit=CURRENT_COMMIT,
        )

    def test_new_paths_become_token_vazio_candidates(self):
        report = self.build()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["derived"]["known_baseline_signal_count"], 1)
        self.assertEqual(report["derived"]["new_candidate_count"], 2)
        self.assertTrue(report["derived"]["review_required"])
        by_path = {item["path"]: item for item in report["new_candidates"]}
        self.assertEqual(by_path["docs/new-control.md"]["state"], "TOKEN_VAZIO")
        self.assertEqual(by_path["docs/new-only.md"]["state"], "TOKEN_VAZIO")
        self.assertFalse(report["boundaries"]["new_control_file_is_automatically_safe"])
        self.assertFalse(report["derived"]["claim_allowed"])

    def test_stable_id_is_deterministic(self):
        first = stable_candidate_id("docs/new-control.md")
        second = stable_candidate_id("docs/new-control.md")
        other = stable_candidate_id("docs/other.md")
        self.assertEqual(first, second)
        self.assertNotEqual(first, other)
        self.assertRegex(first, r"^NCC-[0-9A-F]{12}$")

    def test_missing_current_signal_does_not_mean_resolved(self):
        report = self.build()
        self.assertGreater(report["derived"]["baseline_without_current_signal_count"], 0)
        self.assertFalse(report["boundaries"]["missing_current_signal_means_resolved"])
        self.assertFalse(report["derived"]["filtered_scope_refresh_complete"])
        self.assertFalse(report["derived"]["full_byte_repository_scan_proven"])

    def test_no_new_candidates_selects_full_byte_gate(self):
        precision = copy.deepcopy(self.precision)
        precision["exact_token_files"] = [
            {"path": "docs/baseline-001.md", "tokens": {"COMPLETE": 1}}
        ]
        scan = copy.deepcopy(self.claim_scan)
        scan["warnings"] = [scan["warnings"][0]]
        report = build_refresh(
            ledger=self.ledger,
            head=self.head,
            claim_scan=scan,
            precision=precision,
            current_commit=CURRENT_COMMIT,
        )
        self.assertEqual(report["derived"]["new_candidate_count"], 0)
        self.assertFalse(report["derived"]["review_required"])
        self.assertEqual(
            report["derived"]["next_gate"],
            "PRODUCE_FULL_BYTE_REPOSITORY_RECEIPT",
        )

    def test_truncated_exact_list_rejected(self):
        precision = copy.deepcopy(self.precision)
        precision["exact_token_files_truncated"] = True
        with self.assertRaises(ScopeRefreshError):
            build_refresh(
                ledger=self.ledger,
                head=self.head,
                claim_scan=self.claim_scan,
                precision=precision,
                current_commit=CURRENT_COMMIT,
            )

    def test_truncated_warning_list_rejected(self):
        scan = copy.deepcopy(self.claim_scan)
        scan["warnings_truncated"] = True
        with self.assertRaises(ScopeRefreshError):
            build_refresh(
                ledger=self.ledger,
                head=self.head,
                claim_scan=scan,
                precision=self.precision,
                current_commit=CURRENT_COMMIT,
            )

    def test_explicit_claim_error_blocks_refresh(self):
        scan = copy.deepcopy(self.claim_scan)
        scan["explicit_claim_error_count"] = 1
        with self.assertRaises(ScopeRefreshError):
            build_refresh(
                ledger=self.ledger,
                head=self.head,
                claim_scan=scan,
                precision=self.precision,
                current_commit=CURRENT_COMMIT,
            )

    def test_unreadable_file_blocks_refresh(self):
        precision = copy.deepcopy(self.precision)
        precision["unreadable_file_count"] = 1
        with self.assertRaises(ScopeRefreshError):
            build_refresh(
                ledger=self.ledger,
                head=self.head,
                claim_scan=self.claim_scan,
                precision=precision,
                current_commit=CURRENT_COMMIT,
            )

    def test_duplicate_exact_path_rejected(self):
        precision = copy.deepcopy(self.precision)
        precision["exact_token_files"].append(
            copy.deepcopy(precision["exact_token_files"][0])
        )
        with self.assertRaises(ScopeRefreshError):
            build_refresh(
                ledger=self.ledger,
                head=self.head,
                claim_scan=self.claim_scan,
                precision=precision,
                current_commit=CURRENT_COMMIT,
            )

    def test_invalid_commit_rejected(self):
        with self.assertRaises(ScopeRefreshError):
            build_refresh(
                ledger=self.ledger,
                head=self.head,
                claim_scan=self.claim_scan,
                precision=self.precision,
                current_commit="main",
            )

    def test_digest_is_reproducible(self):
        first = self.build()
        second = self.build()
        self.assertEqual(first, second)
        self.assertEqual(first["integrity"]["digest"], canonical_digest(first))


if __name__ == "__main__":
    unittest.main()
