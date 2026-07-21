from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "scripts"))

from validate_claim_review_chain import canonical_digest, load_json
from validate_claim_review_residual import (
    ResidualValidationError,
    validate_residual_resolution,
)

RESIDUAL = Path("indices/CLAIM_REVIEW_RESIDUAL.json")
RESOLUTION = Path("indices/CLAIM_REVIEW_RESOLUTION_CC028.json")
HEAD = Path("indices/CLAIM_CONTRADICTION_HEAD.json")


class ClaimReviewResidualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.residual = load_json(RESIDUAL)
        cls.resolution = load_json(RESOLUTION)
        cls.head = load_json(HEAD)

    def test_valid_historical_residual_and_resolution(self):
        result = validate_residual_resolution(
            ROOT,
            copy.deepcopy(self.residual),
            copy.deepcopy(self.resolution),
            copy.deepcopy(self.head),
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["historical_residual_count"], 1)
        self.assertEqual(result["historical_token_vazio_ids"], ["CC028"])
        self.assertEqual(result["historical_attempt_count"], 2)
        self.assertEqual(result["resolved_count"], 1)
        self.assertEqual(result["resolved_ids"], ["CC028"])
        self.assertEqual(result["current_residual_count"], 0)
        self.assertEqual(result["current_token_vazio_ids"], [])
        self.assertTrue(result["full_content_observed"])
        self.assertTrue(result["semantic_disposition_allowed"])
        self.assertEqual(result["decoded_size_bytes"], 19542)
        self.assertEqual(result["exact_strong_token_count"], 0)
        self.assertEqual(result["false_positive_source"], "completeness_ratio")
        self.assertFalse(result["portfolio_exit_criteria_met"])
        self.assertFalse(result["claim_allowed"])

    def _isolated_tree(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        for relative in [
            "indices/CLAIM_CONTRADICTION_LEDGER.json",
            "indices/CLAIM_CONTRADICTION_HEAD.json",
            "indices/CLAIM_REVIEW_RESIDUAL.json",
            "indices/CLAIM_REVIEW_RESOLUTION_CC028.json",
            "indices/claim_review_batches/CLAIM_REVIEW_BATCH_001_2026-07-20.json",
            "indices/claim_review_batches/CLAIM_REVIEW_BATCH_002_2026-07-20.json",
            "indices/claim_review_batches/CLAIM_REVIEW_BATCH_003_2026-07-21.json",
        ]:
            source = ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        return temp, root

    def _reseal(self, data):
        data["integrity"]["digest"] = canonical_digest(data)

    def test_historical_failure_cannot_be_erased(self):
        data = copy.deepcopy(self.residual)
        data["residuals"] = []
        data["derived"]["residual_count"] = 0
        data["derived"]["token_vazio_ids"] = []
        self._reseal(data)
        with self.assertRaises(ResidualValidationError):
            validate_residual_resolution(
                ROOT, data, copy.deepcopy(self.resolution), copy.deepcopy(self.head)
            )

    def test_historical_attempt_result_cannot_be_rewritten(self):
        data = copy.deepcopy(self.residual)
        data["residuals"][0]["attempts"][0]["result"] = "SUCCESS"
        self._reseal(data)
        with self.assertRaises(ResidualValidationError):
            validate_residual_resolution(
                ROOT, data, copy.deepcopy(self.resolution), copy.deepcopy(self.head)
            )

    def test_historical_digest_reference_drift_rejected(self):
        resolution = copy.deepcopy(self.resolution)
        resolution["historical_residual"]["digest_blake2b_256"] = "0" * 64
        self._reseal(resolution)
        with self.assertRaises(ResidualValidationError):
            validate_residual_resolution(
                ROOT, copy.deepcopy(self.residual), resolution, copy.deepcopy(self.head)
            )

    def test_resolution_argument_must_equal_canonical_file(self):
        resolution = copy.deepcopy(self.resolution)
        resolution["token_scan"]["false_positive_source"] = "other"
        self._reseal(resolution)
        with self.assertRaises(ResidualValidationError):
            validate_residual_resolution(
                ROOT, copy.deepcopy(self.residual), resolution, copy.deepcopy(self.head)
            )

    def test_current_head_cannot_restore_token_vazio(self):
        head = copy.deepcopy(self.head)
        head["derived"]["token_vazio_count"] = 1
        head["derived"]["reviewed_safe_count"] = 35
        head["derived"]["review_completion_ratio"] = 0.972222222222
        self._reseal(head)
        with self.assertRaises(ResidualValidationError):
            validate_residual_resolution(
                ROOT,
                copy.deepcopy(self.residual),
                copy.deepcopy(self.resolution),
                head,
            )

    def test_resolution_blob_sha_tampering_rejected(self):
        temp, root = self._isolated_tree()
        try:
            path = root / RESOLUTION
            resolution = json.loads(path.read_text(encoding="utf-8"))
            resolution["materialization"]["git_blob_sha1"] = "0" * 40
            self._reseal(resolution)
            path.write_text(json.dumps(resolution, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            head = load_json(root / HEAD)
            batch_ref = head["review_batches"][2]
            batch_path = root / batch_ref["path"]
            batch = load_json(batch_path)
            batch["materialization_receipt"]["digest_blake2b_256"] = resolution["integrity"]["digest"]
            self._reseal(batch)
            batch_path.write_text(json.dumps(batch, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            batch_ref["digest_blake2b_256"] = batch["integrity"]["digest"]
            self._reseal(head)
            with self.assertRaises(ResidualValidationError):
                validate_residual_resolution(
                    root,
                    load_json(root / RESIDUAL),
                    resolution,
                    head,
                )
        finally:
            temp.cleanup()

    def test_claim_promotion_rejected(self):
        resolution = copy.deepcopy(self.resolution)
        resolution["decision"]["claim_allowed"] = True
        self._reseal(resolution)
        with self.assertRaises(ResidualValidationError):
            validate_residual_resolution(
                ROOT, copy.deepcopy(self.residual), resolution, copy.deepcopy(self.head)
            )

    def test_portfolio_closure_rejected(self):
        resolution = copy.deepcopy(self.resolution)
        resolution["derived"]["portfolio_exit_criteria_met"] = True
        self._reseal(resolution)
        with self.assertRaises(ResidualValidationError):
            validate_residual_resolution(
                ROOT, copy.deepcopy(self.residual), resolution, copy.deepcopy(self.head)
            )

    def test_next_gate_cannot_be_skipped(self):
        head = copy.deepcopy(self.head)
        head["derived"]["next_gate"] = "PORTFOLIO_CLOSED"
        self._reseal(head)
        with self.assertRaises(ResidualValidationError):
            validate_residual_resolution(
                ROOT,
                copy.deepcopy(self.residual),
                copy.deepcopy(self.resolution),
                head,
            )


if __name__ == "__main__":
    unittest.main()
