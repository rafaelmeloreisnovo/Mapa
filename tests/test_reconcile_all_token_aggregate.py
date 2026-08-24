#!/usr/bin/env python3

import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

from tools.reconcile_all_token_aggregate import analyze


class AggregateReconciliationTests(unittest.TestCase):
    def _write_fixture(self, root: Path, manifest_total: int, source_b_count: int = 3):
        literal = root / "tokens_literal.tsv.gz"
        with gzip.open(literal, "wt", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
            writer.writerow(["literal", "normalized", "kind", "count_total", "source_mask_hex"])
            writer.writerow(["a", "a", "WORD", 2, "0x3"])
            writer.writerow(["b", "b", "WORD", 3, "0x3"])

        token_source = root / "token_source_counts.tsv.gz"
        with gzip.open(token_source, "wt", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
            writer.writerow(["literal", "source", "count"])
            writer.writerow(["a", "S1", 1])
            writer.writerow(["a", "S2", 1])
            writer.writerow(["b", "S1", source_b_count])

        source_manifest = root / "source_manifest.tsv"
        with source_manifest.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
            writer.writerow(["source", "bytes", "sha256", "lines", "unique_literal_tokens", "token_occurrences"])
            writer.writerow(["S1", 1, "0" * 64, 1, 2, 1 + source_b_count])
            writer.writerow(["S2", 1, "1" * 64, 1, 1, 1])

        manifest = root / "manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "token_occurrences_total_raw": manifest_total,
                    "source_manifest": [
                        {"source": "S1", "token_occurrences": str(1 + source_b_count)},
                        {"source": "S2", "token_occurrences": "1"},
                    ],
                }
            ),
            encoding="utf-8",
        )
        return literal, token_source, source_manifest, manifest

    def test_consistent(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._write_fixture(Path(tmp), manifest_total=5)
            result = analyze(*paths)
            self.assertEqual(result["state"], "CONSISTENT")
            self.assertEqual(result["canonical_detailed_total"], 5)
            self.assertEqual(result["manifest_delta_vs_detailed"], 0)
            self.assertEqual(result["mismatches"]["per_literal"], 0)
            self.assertEqual(result["mismatches"]["per_source"], 0)

    def test_manifest_aggregate_drift_is_localized_without_rewriting_stores(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._write_fixture(Path(tmp), manifest_total=4)
            result = analyze(*paths)
            self.assertEqual(result["state"], "MANIFEST_AGGREGATE_DRIFT")
            self.assertTrue(result["detailed_stores_consistent"])
            self.assertEqual(result["canonical_detailed_total"], 5)
            self.assertEqual(result["manifest_delta_vs_detailed"], -1)
            self.assertEqual(result["generator_root_cause"], "TOKEN_VAZIO_NOT_LOCATED")

    def test_detailed_store_divergence_wins_over_manifest_interpretation(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._write_fixture(Path(tmp), manifest_total=4, source_b_count=2)
            result = analyze(*paths)
            self.assertEqual(result["state"], "STORE_DIVERGENCE")
            self.assertFalse(result["detailed_stores_consistent"])
            self.assertIsNone(result["canonical_detailed_total"])
            self.assertGreater(result["mismatches"]["per_literal"], 0)


if __name__ == "__main__":
    unittest.main()
