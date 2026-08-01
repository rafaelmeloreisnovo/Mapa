from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validator", ROOT / "scripts" / "validate_drive_snapshot_catalog.py"
)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


class DriveSnapshotCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads(
            (ROOT / "indices" / "memoria-longitudinal" / "drive_snapshot_catalog.v1.json")
            .read_text(encoding="utf-8")
        )

    def test_catalog_passes(self) -> None:
        report = validator.validate_catalog(copy.deepcopy(self.catalog))
        self.assertTrue(report["ok"])
        self.assertEqual(report["snapshots"], 7)
        self.assertEqual(report["open_gates"], 3)

    def test_private_body_key_fails(self) -> None:
        data = copy.deepcopy(self.catalog)
        data["snapshots"][0]["body"] = "must never be stored"
        with self.assertRaises(validator.CatalogError):
            validator.validate_catalog(data)

    def test_two_canonical_snapshots_fail(self) -> None:
        data = copy.deepcopy(self.catalog)
        data["snapshots"][1]["status"] = "CANONICAL_RAW"
        with self.assertRaises(validator.CatalogError):
            validator.validate_catalog(data)

    def test_duplicate_candidate_without_group_fails(self) -> None:
        data = copy.deepcopy(self.catalog)
        del data["snapshots"][2]["duplicate_candidate_group"]
        with self.assertRaises(validator.CatalogError):
            validator.validate_catalog(data)

    def test_open_gate_cannot_allow_claim(self) -> None:
        data = copy.deepcopy(self.catalog)
        data["open_gates"][0]["claim_allowed"] = True
        with self.assertRaises(validator.CatalogError):
            validator.validate_catalog(data)


if __name__ == "__main__":
    unittest.main()
