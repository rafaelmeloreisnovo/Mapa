from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "apply_main_branch_protection.py"
spec = importlib.util.spec_from_file_location("apply_main_branch_protection", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class ProviderMergeProtectionBootstrapTests(unittest.TestCase):
    def test_payload_binds_exact_promotion_context_and_one_approval(self) -> None:
        payload = module.protection_payload("promotion-control / enforce")
        self.assertTrue(payload["enforce_admins"])
        self.assertTrue(payload["required_status_checks"]["strict"])
        self.assertEqual(
            payload["required_status_checks"]["contexts"],
            ["promotion-control / enforce"],
        )
        self.assertEqual(
            payload["required_pull_request_reviews"]["required_approving_review_count"],
            1,
        )
        self.assertTrue(
            payload["required_pull_request_reviews"]["require_last_push_approval"]
        )
        self.assertIsNone(payload["restrictions"])

    def test_verify_accepts_required_context_admins_and_one_approval(self) -> None:
        branch = {"protected": True}
        protection = {
            "required_status_checks": {"contexts": ["promotion-control / enforce"]},
            "enforce_admins": {"enabled": True},
            "required_pull_request_reviews": {"required_approving_review_count": 1},
        }
        self.assertEqual(
            module.verify_observed(branch, protection, "promotion-control / enforce"), []
        )

    def test_verify_fails_closed_on_unprotected_zero_approval_state(self) -> None:
        failures = module.verify_observed(
            {"protected": False},
            {
                "required_status_checks": {"contexts": []},
                "enforce_admins": {"enabled": False},
                "required_pull_request_reviews": {"required_approving_review_count": 0},
            },
            "promotion-control / enforce",
        )
        self.assertIn("BRANCH_NOT_PROTECTED", failures)
        self.assertIn("PROMOTION_CONTROL_CONTEXT_NOT_REQUIRED", failures)
        self.assertIn("ADMINS_NOT_ENFORCED", failures)
        self.assertIn("ZERO_APPROVAL_NOT_PROVIDER_BLOCKED_BY_REVIEW_RULE", failures)

    def test_checks_shape_is_also_accepted(self) -> None:
        protection = {
            "required_status_checks": {
                "checks": [{"context": "promotion-control / enforce", "app_id": 15368}]
            },
            "enforce_admins": {"enabled": True},
            "required_pull_request_reviews": {"required_approving_review_count": 1},
        }
        self.assertEqual(
            module.verify_observed({"protected": True}, protection, "promotion-control / enforce"),
            [],
        )


if __name__ == "__main__":
    unittest.main()
