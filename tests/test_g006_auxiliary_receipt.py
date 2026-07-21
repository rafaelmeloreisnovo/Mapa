from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "scripts"))

from validate_g006_auxiliary_receipt import (
    AuxiliaryReceiptError,
    canonical_digest,
    load,
    validate,
)

RECEIPT = Path("resultados/G006_AUXILIARY_LOCAL_VALIDATION_2026-07-21.json")


class G006AuxiliaryReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = load(RECEIPT)

    def test_current_receipt_and_files_validate(self):
        result = validate(ROOT, copy.deepcopy(self.receipt))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["tests_run"], 15)
        self.assertEqual(result["tests_passed"], 15)
        self.assertTrue(result["file_hashes_match"])
        self.assertFalse(result["full_repository_suite_executed"])
        self.assertFalse(result["claim_allowed"])

    def test_test_count_tampering_rejected(self):
        data = copy.deepcopy(self.receipt)
        data["results"]["tests_run"] = 16
        data["integrity"]["digest"] = canonical_digest(data)
        with self.assertRaises(AuxiliaryReceiptError):
            validate(ROOT, data)

    def test_boundary_promotion_rejected(self):
        data = copy.deepcopy(self.receipt)
        data["boundaries"]["claim_control_plane_suite_executed"] = True
        data["integrity"]["digest"] = canonical_digest(data)
        with self.assertRaises(AuxiliaryReceiptError):
            validate(ROOT, data)

    def test_noise_history_cannot_be_erased(self):
        data = copy.deepcopy(self.receipt)
        data["environment_noise"]["observed"] = False
        data["integrity"]["digest"] = canonical_digest(data)
        with self.assertRaises(AuxiliaryReceiptError):
            validate(ROOT, data)

    def test_file_hash_drift_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative in self.receipt["files_sha256"]:
                source = ROOT / relative
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
            target = root / "tools/materialize_github_blob.py"
            target.write_text(target.read_text() + "\n# drift\n")
            with self.assertRaises(AuxiliaryReceiptError):
                validate(root, copy.deepcopy(self.receipt))

    def test_integrity_tampering_rejected(self):
        data = copy.deepcopy(self.receipt)
        data["results"]["tests_passed"] = 14
        with self.assertRaises(AuxiliaryReceiptError):
            validate(ROOT, data)


if __name__ == "__main__":
    unittest.main()
