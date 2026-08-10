#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "materialize_effective_gap_atlas.py"
SEED = ROOT / "data/gap-atlas/RAFAELIA_GAP_ATLAS_V1.json"
APPEND = ROOT / "data/gap-atlas/RAFAELIA_GAP_RECORD_APPEND_V1.jsonl"
OVERRIDES = ROOT / "data/gap-atlas/GAP_STATE_OVERRIDES_V1.json"


class EffectiveAtlasTests(unittest.TestCase):
    def test_current_materialization_has_31_records_and_reduced_meta_gap(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "effective.json"
            proc = subprocess.run(
                [sys.executable, str(TOOL), "--output", str(out)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["counts"]["seed_records"], 26)
            self.assertEqual(data["counts"]["appended_records"], 5)
            self.assertEqual(data["counts"]["effective_records"], 31)
            self.assertFalse(data["claim_allowed"])
            self.assertFalse(data["publication_ready"])
            by_id = {record["gap_id"]: record for record in data["records"]}
            self.assertEqual(by_id["GAP-META-INVENTORY-001"]["base_state"], "TOKEN_VAZIO")
            self.assertEqual(by_id["GAP-META-INVENTORY-001"]["effective_state"], "REDUCED")
            self.assertEqual(by_id["GAP-CONVERSATIONS-018-027-CUSTODY-001"]["effective_state"], "TOKEN_VAZIO")
            self.assertEqual(by_id["GAP-CONVERSATIONS-TOKENIZER-001"]["effective_state"], "TOKEN_VAZIO")
            self.assertEqual(by_id["GAP-CONVERSATIONS-ASSET-JOIN-001"]["effective_state"], "TOKEN_VAZIO")
            self.assertEqual(by_id["GAP-DRIVE-GITHUB-PROVENANCE-001"]["effective_state"], "TOKEN_VAZIO")
            self.assertEqual(by_id["GAP-TRAINING-EVIDENCE-001"]["effective_state"], "NOT_MEASURED")

    def test_duplicate_appended_gap_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            duplicate = Path(td) / "append.jsonl"
            seed_data = json.loads(SEED.read_text(encoding="utf-8"))
            rec = dict(seed_data["records"][0])
            duplicate.write_text(json.dumps({
                "schema":"RAFAELIA_GAP_RECORD_APPEND_V1",
                "append_id":"DUP-1",
                "appended_at":"2026-08-10T00:00:00Z",
                "claim_allowed":False,
                "record":rec,
            }) + "\n", encoding="utf-8")
            out = Path(td) / "effective.json"
            proc = subprocess.run(
                [sys.executable, str(TOOL), "--seed", str(SEED), "--append", str(duplicate), "--overrides", str(OVERRIDES), "--output", str(out)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("duplicate/invalid gap_id", proc.stderr)


if __name__ == "__main__":
    unittest.main()
