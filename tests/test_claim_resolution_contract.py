from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "scripts"))

from validate_claim_resolution_contract import (
    ResolutionContractError,
    canonical_digest,
    load,
    validate,
)

PATH = Path("indices/CLAIM_REVIEW_RESOLUTION_CC028.json")


class ClaimResolutionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = load(PATH)

    def reseal(self, data):
        data["integrity"]["digest"] = canonical_digest(data)

    def test_current_resolution_contract_passes(self):
        result = validate(copy.deepcopy(self.base))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["boundary_count"], 6)
        self.assertTrue(result["all_boundaries_false"])
        self.assertEqual(result["decoded_size_bytes"], 19542)
        self.assertEqual(result["exact_strong_token_count"], 0)
        self.assertEqual(result["current_token_vazio_count"], 0)
        self.assertFalse(result["claim_allowed"])

    def test_each_resolution_boundary_is_fail_closed(self):
        for key in self.base["boundaries"]:
            with self.subTest(boundary=key):
                data = copy.deepcopy(self.base)
                data["boundaries"][key] = True
                self.reseal(data)
                with self.assertRaises(ResolutionContractError):
                    validate(data)

    def test_missing_boundary_rejected(self):
        data = copy.deepcopy(self.base)
        data["boundaries"].pop("remote_runner_pass_inferred")
        self.reseal(data)
        with self.assertRaises(ResolutionContractError):
            validate(data)

    def test_git_blob_sha_drift_rejected(self):
        data = copy.deepcopy(self.base)
        data["materialization"]["git_blob_sha1"] = "0" * 40
        self.reseal(data)
        with self.assertRaises(ResolutionContractError):
            validate(data)

    def test_sha256_drift_rejected(self):
        data = copy.deepcopy(self.base)
        data["materialization"]["sha256"] = "0" * 64
        self.reseal(data)
        with self.assertRaises(ResolutionContractError):
            validate(data)

    def test_base64_range_loss_rejected(self):
        data = copy.deepcopy(self.base)
        data["materialization"]["line_ranges"].pop()
        self.reseal(data)
        with self.assertRaises(ResolutionContractError):
            validate(data)

    def test_exact_token_regression_rejected(self):
        data = copy.deepcopy(self.base)
        data["token_scan"]["strong_token_counts"]["COMPLETE"] = 1
        self.reseal(data)
        with self.assertRaises(ResolutionContractError):
            validate(data)

    def test_false_positive_cause_drift_rejected(self):
        data = copy.deepcopy(self.base)
        data["token_scan"]["false_positive_source"] = "unknown"
        self.reseal(data)
        with self.assertRaises(ResolutionContractError):
            validate(data)

    def test_historical_residual_cannot_be_detached(self):
        data = copy.deepcopy(self.base)
        data["historical_residual"]["state"] = "DISCARDED"
        self.reseal(data)
        with self.assertRaises(ResolutionContractError):
            validate(data)

    def test_current_token_vazio_cannot_reappear(self):
        data = copy.deepcopy(self.base)
        data["derived"]["current_token_vazio_count"] = 1
        self.reseal(data)
        with self.assertRaises(ResolutionContractError):
            validate(data)

    def test_next_gate_cannot_be_skipped(self):
        data = copy.deepcopy(self.base)
        data["derived"]["next_gate"] = "PORTFOLIO_CLOSED"
        self.reseal(data)
        with self.assertRaises(ResolutionContractError):
            validate(data)

    def test_integrity_tampering_rejected(self):
        data = copy.deepcopy(self.base)
        data["materialization"]["repository_count"] = 40
        with self.assertRaises(ResolutionContractError):
            validate(data)


if __name__ == "__main__":
    unittest.main()
