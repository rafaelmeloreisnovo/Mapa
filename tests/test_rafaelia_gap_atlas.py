#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_rafaelia_gap_atlas.py"
ATLAS = ROOT / "data" / "gap-atlas" / "RAFAELIA_GAP_ATLAS_V1.json"


class GapAtlasTests(unittest.TestCase):
    def run_validator(self, payload: dict) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "atlas.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), "--atlas", str(path)],
                text=True,
                capture_output=True,
                check=False,
            )

    @classmethod
    def base(cls) -> dict:
        return json.loads(ATLAS.read_text(encoding="utf-8"))

    def test_current_atlas_passes(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(proc.stdout)
        self.assertEqual(report["status"], "PASS")
        self.assertFalse(report["claim_allowed"])
        self.assertFalse(report["publication_ready"])
        self.assertGreater(report["p0_open"], 0)

    def test_duplicate_gap_id_fails(self) -> None:
        data = self.base()
        data["records"].append(copy.deepcopy(data["records"][0]))
        proc = self.run_validator(data)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("duplicate gap IDs", proc.stderr)

    def test_claim_promotion_fails(self) -> None:
        data = self.base()
        data["records"][0]["claim_allowed"] = True
        proc = self.run_validator(data)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("claim_allowed", proc.stderr)

    def test_terminal_without_evidence_fails(self) -> None:
        data = self.base()
        data["records"][0]["state"] = "RESOLVED"
        data["records"][0]["resolution_evidence"] = []
        proc = self.run_validator(data)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("terminal resolution requires evidence", proc.stderr)

    def test_missing_internal_successor_fails(self) -> None:
        data = self.base()
        data["records"][0]["successors"] = ["GAP-DOES-NOT-EXIST"]
        proc = self.run_validator(data)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("missing internal successor", proc.stderr)

    def test_empty_authority_fails(self) -> None:
        data = self.base()
        data["records"][0]["authority_required"] = []
        proc = self.run_validator(data)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("authority_required", proc.stderr)


if __name__ == "__main__":
    unittest.main()
