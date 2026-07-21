from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "scripts"))

from validate_claim_discovery_precision import (
    DiscoveryPrecisionError,
    scan_discovery_precision,
    token_counts,
    validate_known_resolution,
)
from validate_claim_vocabulary import load_json

POLICY = Path("indices/CLAIM_VOCABULARY_POLICY.json")


class ClaimDiscoveryPrecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = load_json(POLICY)

    def test_completeness_ratio_is_not_complete_token(self):
        counts = token_counts('{"completeness_ratio":0.5}', "COMPLETE")
        self.assertEqual(counts["substring_count"], 1)
        self.assertEqual(counts["exact_count"], 0)
        self.assertEqual(counts["lexical_false_positive_count"], 1)

    def test_exact_complete_token_is_detected(self):
        counts = token_counts('{"state":"COMPLETE"}', "COMPLETE")
        self.assertEqual(counts["substring_count"], 1)
        self.assertEqual(counts["exact_count"], 1)
        self.assertEqual(counts["lexical_false_positive_count"], 0)

    def test_identifier_suffix_does_not_create_exact_token(self):
        counts = token_counts("COMPLETE_STATE completeness_ratio", "COMPLETE")
        self.assertEqual(counts["substring_count"], 2)
        self.assertEqual(counts["exact_count"], 0)
        self.assertEqual(counts["lexical_false_positive_count"], 2)

    def test_known_cc028_resolution_is_valid(self):
        result = validate_known_resolution(ROOT)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["false_positive_source"], "completeness_ratio")
        self.assertEqual(result["substring_complete_count"], 1)
        self.assertEqual(result["exact_complete_count"], 0)

    def test_fixture_scan_separates_exact_and_substring(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "indices").mkdir()
            (root / "indices" / "CLAIM_REVIEW_RESOLUTION_CC028.json").write_text(
                (ROOT / "indices/CLAIM_REVIEW_RESOLUTION_CC028.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            (root / "ratio.json").write_text(
                '{"completeness_ratio":0.5,"state":"TOKEN_VAZIO"}',
                encoding="utf-8",
            )
            (root / "exact.md").write_text(
                "state COMPLETE while evidence is TOKEN_VAZIO",
                encoding="utf-8",
            )
            policy = copy.deepcopy(self.policy)
            policy["excluded_paths"] = []
            result = scan_discovery_precision(root, policy)
            self.assertEqual(result["status"], "PASS")
            complete = result["token_totals"]["COMPLETE"]
            self.assertGreaterEqual(complete["substring_count"], 2)
            self.assertGreaterEqual(complete["exact_count"], 1)
            self.assertGreaterEqual(complete["lexical_false_positive_count"], 1)
            exact_by_path = {
                row["path"]: row["tokens"] for row in result["exact_token_files"]
            }
            self.assertEqual(exact_by_path["exact.md"]["COMPLETE"], 1)
            self.assertNotIn("ratio.json", exact_by_path)
            self.assertFalse(result["exact_token_files_truncated"])

    def test_multiple_exact_tokens_are_reported_per_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "indices").mkdir()
            (root / "indices" / "CLAIM_REVIEW_RESOLUTION_CC028.json").write_text(
                (ROOT / "indices/CLAIM_REVIEW_RESOLUTION_CC028.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            (root / "claims.md").write_text(
                "COMPLETE COMPLIANT ALIGNED CERTIFIED",
                encoding="utf-8",
            )
            policy = copy.deepcopy(self.policy)
            policy["excluded_paths"] = []
            result = scan_discovery_precision(root, policy)
            row = next(
                item for item in result["exact_token_files"]
                if item["path"] == "claims.md"
            )
            self.assertEqual(
                row["tokens"],
                {"ALIGNED": 1, "CERTIFIED": 1, "COMPLETE": 1, "COMPLIANT": 1},
            )

    def test_missing_resolution_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(Exception):
                validate_known_resolution(Path(tmp))

    def test_resolution_false_positive_source_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "indices" / "CLAIM_REVIEW_RESOLUTION_CC028.json"
            target.parent.mkdir(parents=True)
            data = json.loads(
                (ROOT / "indices/CLAIM_REVIEW_RESOLUTION_CC028.json").read_text(
                    encoding="utf-8"
                )
            )
            data["token_scan"]["false_positive_source"] = "unknown"
            target.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(DiscoveryPrecisionError):
                validate_known_resolution(root)


if __name__ == "__main__":
    unittest.main()
