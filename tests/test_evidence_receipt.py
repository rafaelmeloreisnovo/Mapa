#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_evidence_receipt import validate

RECEIPT = Path("data/routing/evidence/quantum-echoes-zenodo-release-2025.v1.json")


class EvidenceReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads(RECEIPT.read_text(encoding="utf-8"))

    def test_quantum_echoes_receipt_passes(self) -> None:
        defects, report = validate(copy.deepcopy(self.base))
        self.assertEqual([], defects)
        self.assertEqual("PASS", report["status"])
        self.assertEqual("TOKEN_VAZIO", report["local_sha256_state"])
        self.assertFalse(report["claim_allowed"])

    def test_receipt_cannot_authorize_claim(self) -> None:
        doc = copy.deepcopy(self.base)
        doc["claim_allowed"] = True
        defects, _ = validate(doc)
        self.assertTrue(any("claim_allowed=false" in d for d in defects))

    def test_publisher_checksum_is_not_local_verification(self) -> None:
        doc = copy.deepcopy(self.base)
        doc["verification"]["publisher_md5_recomputed_locally"] = True
        defects, _ = validate(doc)
        self.assertTrue(any("requires binary_downloaded_locally=true" in d for d in defects))

    def test_sha256_computed_requires_verified_digest(self) -> None:
        doc = copy.deepcopy(self.base)
        doc["verification"]["binary_downloaded_locally"] = True
        doc["verification"]["sha256_computed_locally"] = True
        defects, _ = validate(doc)
        self.assertTrue(any("requires local_sha256.state=VERIFIED" in d for d in defects))

    def test_token_vazio_requires_reason_and_next_test(self) -> None:
        doc = copy.deepcopy(self.base)
        del doc["artifact"]["local_sha256"]["next_test"]
        defects, _ = validate(doc)
        self.assertTrue(any("requires reason and next_test" in d for d in defects))

    def test_verified_sha256_requires_local_computation(self) -> None:
        doc = copy.deepcopy(self.base)
        doc["artifact"]["local_sha256"] = {
            "state": "VERIFIED",
            "value": "a" * 64,
            "byte_length": 123
        }
        defects, _ = validate(doc)
        self.assertTrue(any("VERIFIED requires sha256_computed_locally=true" in d for d in defects))

    def test_append_only_is_mandatory(self) -> None:
        doc = copy.deepcopy(self.base)
        doc["anti_regression"]["append_only"] = False
        defects, _ = validate(doc)
        self.assertTrue(any("append_only must be true" in d for d in defects))


if __name__ == "__main__":
    unittest.main()
