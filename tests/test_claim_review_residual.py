from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "scripts"))

from validate_claim_review_residual import (
    ResidualValidationError,
    canonical_digest,
    validate_residual,
)
from validate_claim_review_chain import load_json


class ClaimReviewResidualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.residual = load_json(Path("indices/CLAIM_REVIEW_RESIDUAL.json"))
        cls.head = load_json(Path("indices/CLAIM_CONTRADICTION_HEAD.json"))

    def test_valid_residual(self):
        result = validate_residual(
            ROOT,
            copy.deepcopy(self.residual),
            copy.deepcopy(self.head),
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["residual_count"], 1)
        self.assertEqual(result["token_vazio_ids"], ["CC028"])
        self.assertEqual(result["materialization_attempt_count"], 2)
        self.assertFalse(result["full_content_observed"])
        self.assertFalse(result["semantic_disposition_allowed"])

    def test_missing_residual_rejected(self):
        data = copy.deepcopy(self.residual)
        data["residuals"] = []
        data["derived"]["residual_count"] = 0
        data["derived"]["token_vazio_ids"] = []
        data["integrity"]["digest"] = canonical_digest(data)
        with self.assertRaises(ResidualValidationError):
            validate_residual(ROOT, data, copy.deepcopy(self.head))

    def test_wrong_residual_id_rejected(self):
        data = copy.deepcopy(self.residual)
        data["residuals"][0]["id"] = "CC027"
        data["derived"]["token_vazio_ids"] = ["CC027"]
        data["integrity"]["digest"] = canonical_digest(data)
        with self.assertRaises(ResidualValidationError):
            validate_residual(ROOT, data, copy.deepcopy(self.head))

    def test_fake_full_content_observation_rejected(self):
        data = copy.deepcopy(self.residual)
        data["residuals"][0]["observed_boundary"]["full_content_observed"] = True
        data["integrity"]["digest"] = canonical_digest(data)
        with self.assertRaises(ResidualValidationError):
            validate_residual(ROOT, data, copy.deepcopy(self.head))

    def test_semantic_promotion_rejected(self):
        data = copy.deepcopy(self.residual)
        data["residuals"][0]["observed_boundary"]["semantic_disposition_allowed"] = True
        data["integrity"]["digest"] = canonical_digest(data)
        with self.assertRaises(ResidualValidationError):
            validate_residual(ROOT, data, copy.deepcopy(self.head))

    def test_single_materialization_attempt_rejected(self):
        data = copy.deepcopy(self.residual)
        data["residuals"][0]["attempts"].pop()
        data["integrity"]["digest"] = canonical_digest(data)
        with self.assertRaises(ResidualValidationError):
            validate_residual(ROOT, data, copy.deepcopy(self.head))

    def test_blob_identity_drift_rejected(self):
        data = copy.deepcopy(self.residual)
        data["residuals"][0]["attempts"][1]["blob_sha"] = "0" * 40
        data["integrity"]["digest"] = canonical_digest(data)
        with self.assertRaises(ResidualValidationError):
            validate_residual(ROOT, data, copy.deepcopy(self.head))

    def test_attempt_success_without_full_observation_rejected(self):
        data = copy.deepcopy(self.residual)
        data["residuals"][0]["attempts"][0]["result"] = "SUCCESS"
        data["integrity"]["digest"] = canonical_digest(data)
        with self.assertRaises(ResidualValidationError):
            validate_residual(ROOT, data, copy.deepcopy(self.head))

    def test_exit_criteria_weakening_rejected(self):
        data = copy.deepcopy(self.residual)
        data["residuals"][0]["exit_criteria"] = ["read file"]
        data["integrity"]["digest"] = canonical_digest(data)
        with self.assertRaises(ResidualValidationError):
            validate_residual(ROOT, data, copy.deepcopy(self.head))

    def test_claim_promotion_rejected(self):
        data = copy.deepcopy(self.residual)
        data["claim_allowed"] = True
        data["integrity"]["digest"] = canonical_digest(data)
        with self.assertRaises(ResidualValidationError):
            validate_residual(ROOT, data, copy.deepcopy(self.head))

    def test_integrity_tampering_rejected(self):
        data = copy.deepcopy(self.residual)
        data["derived"]["next_gate"] = "SILENT_PROMOTION"
        with self.assertRaises(ResidualValidationError):
            validate_residual(ROOT, data, copy.deepcopy(self.head))


if __name__ == "__main__":
    unittest.main()
