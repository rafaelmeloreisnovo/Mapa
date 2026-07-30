from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validator", ROOT / "scripts" / "validate_semantic_carrier_policy.py"
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class SemanticCarrierPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = json.loads(
            (ROOT / "data" / "indexes" / "semantic-carrier-policy.v1.json").read_text(encoding="utf-8")
        )

    def test_valid_policy_passes(self) -> None:
        report = validator.validate(self.policy)
        self.assertEqual(report["status"], "PASS")
        self.assertFalse(report["claim_allowed"])

    def test_claim_promotion_fails(self) -> None:
        broken = copy.deepcopy(self.policy)
        broken["claim_allowed"] = True
        with self.assertRaises(validator.PolicyError):
            validator.validate(broken)

    def test_global_mean_without_distribution_fails(self) -> None:
        broken = copy.deepcopy(self.policy)
        broken["statistics"]["global_mean_policy"] = "ALLOWED"
        with self.assertRaises(validator.PolicyError):
            validator.validate(broken)

    def test_homophones_are_not_merged(self) -> None:
        broken = copy.deepcopy(self.policy)
        broken["semantic_identity"]["homophone_policy"] = "MERGE_BY_SOUND"
        with self.assertRaises(validator.PolicyError):
            validator.validate(broken)

    def test_archive_polling_fails(self) -> None:
        broken = copy.deepcopy(self.policy)
        next(item for item in broken["tiers"] if item["id"] == "ARCHIVE")["polling"] = True
        with self.assertRaises(validator.PolicyError):
            validator.validate(broken)

    def test_non_prime_signature_fails(self) -> None:
        broken = copy.deepcopy(self.policy)
        broken["prime_facets"]["risk"] = 21
        with self.assertRaises(validator.PolicyError):
            validator.validate(broken)

    def test_auto_delete_fails(self) -> None:
        broken = copy.deepcopy(self.policy)
        broken["safety"]["auto_delete"] = True
        with self.assertRaises(validator.PolicyError):
            validator.validate(broken)


if __name__ == "__main__":
    unittest.main()
