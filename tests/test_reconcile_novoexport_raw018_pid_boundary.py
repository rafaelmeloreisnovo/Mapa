#!/usr/bin/env python3
import csv
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "reconcile_novoexport_raw018_pid_boundary.py"
spec = importlib.util.spec_from_file_location("raw018_wave3", TOOL)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def pid(value: str) -> str:
    return mod.pid_hash(value)


class Raw018Wave3Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        self.raw17 = self.d / "017.json"
        self.raw19 = self.d / "019.json"
        self.current = self.d / "current.csv"
        self.locator = self.d / "locator.csv"
        self.archive = self.d / "witness.zip"

        self.raw17.write_text(json.dumps([
            {"id": "a0", "create_time": 1.0},
            {"id": "a1", "create_time": 10.0},
        ]), encoding="utf-8")
        self.raw19.write_text(json.dumps([
            {"id": "c0", "create_time": 20.0009},
            {"id": "c1", "create_time": 30.0},
        ]), encoding="utf-8")

        current_rows = [
            ["017", pid("a0")],
            ["017", pid("a1")],
            ["019", pid("c0")],
            ["019", pid("c1")],
        ]
        with self.current.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["raw_shard", "conversation_pid_sha256"])
            w.writerows(current_rows)

        self.locator_rows = [
            ["0", pid("a0"), "1970-01-01T00:00:01.000Z"],
            ["1", pid("a1"), "1970-01-01T00:00:10.000Z"],
            ["2", pid("b0"), "1970-01-01T00:00:11.123Z"],
            ["3", pid("b1"), "1970-01-01T00:00:19.999Z"],
            ["4", pid("c0"), "1970-01-01T00:00:20.000Z"],
            ["5", pid("c1"), "1970-01-01T00:00:30.000Z"],
        ]
        self.write_locator(self.locator_rows)
        self.write_archive(include_b1=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write_locator(self, rows):
        with self.locator.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["Source Index", "Conversation PID (SHA-256)", "Created UTC"])
            w.writerows(rows)

    def write_archive(self, include_b1=True):
        objects = [
            {"id": "a0", "create_time": 1.0},
            {"id": "a1", "create_time": 10.0},
            {"id": "b0", "create_time": 11.1234},
        ]
        if include_b1:
            objects.append({"id": "b1", "create_time": 19.9994})
        objects += [
            {"id": "c0", "create_time": 20.0009},
            {"id": "c1", "create_time": 30.0},
        ]
        with zipfile.ZipFile(self.archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("conversations.json", json.dumps(objects))

    def run_ok(self):
        return mod.reconcile(
            locator_csv=self.locator,
            current_pid_csv=self.current,
            raw017_path=self.raw17,
            raw019_path=self.raw19,
            expected_candidates=2,
            archive_zip=self.archive,
            timestamp_tolerance_seconds=0.0011,
        )

    def test_exact_reconciliation_and_archive_witness(self):
        result = self.run_ok()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["counts"]["reconciled_candidate_pids"], 2)
        self.assertEqual(result["archive_witness"]["candidate_pids_found"], 2)
        self.assertEqual(result["archive_witness"]["candidate_pids_missing"], 0)
        self.assertFalse(result["claim_allowed"])

    def test_boundary_rounding_does_not_create_candidate(self):
        result = self.run_ok()
        self.assertEqual(result["counts"]["reconciled_candidate_pids"], 2)
        self.assertNotEqual(result["commitments"]["candidate_set_sha256"], "")

    def test_candidate_outside_boundary_fails_closed(self):
        rows = [list(row) for row in self.locator_rows]
        for row in rows:
            if row[1] == pid("b0"):
                row[2] = "1970-01-01T00:00:09.999Z"
        self.write_locator(rows)
        with self.assertRaises(mod.ReconciliationError):
            self.run_ok()

    def test_archive_missing_candidate_fails_closed(self):
        self.write_archive(include_b1=False)
        with self.assertRaises(mod.ReconciliationError):
            self.run_ok()


if __name__ == "__main__":
    unittest.main()
