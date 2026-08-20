import unittest

from scripts.check_server_merge_enforcement import classify_branch


class ServerMergeEnforcementTests(unittest.TestCase):
    def test_unprotected_branch_fails_closed(self):
        report = classify_branch({
            "name": "main",
            "protected": False,
            "protection": {
                "enabled": False,
                "required_status_checks": {
                    "enforcement_level": "off",
                    "contexts": [],
                    "checks": [],
                },
            },
        })
        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("BRANCH_PROTECTION_DISABLED", report["failure_modes"])
        self.assertIn("REQUIRED_STATUS_CHECKS_NOT_ENFORCED", report["failure_modes"])
        self.assertFalse(report["claim_allowed"])
        self.assertFalse(report["promotion_allowed"])

    def test_protected_without_required_checks_fails_closed(self):
        report = classify_branch({
            "name": "main",
            "protected": True,
            "protection": {
                "enabled": True,
                "required_status_checks": {
                    "enforcement_level": "non_admins",
                    "contexts": [],
                    "checks": [],
                },
            },
        })
        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("NO_REQUIRED_STATUS_CHECKS_OBSERVED", report["failure_modes"])

    def test_protected_with_enforced_check_passes_only_scoped_baseline(self):
        report = classify_branch({
            "name": "main",
            "protected": True,
            "protection": {
                "enabled": True,
                "required_status_checks": {
                    "enforcement_level": "everyone",
                    "contexts": ["Promotion Control / enforce"],
                    "checks": [],
                },
            },
        })
        self.assertEqual(report["status"], "PASS_SCOPED")
        self.assertEqual(report["failure_modes"], [])
        self.assertEqual(
            report["promotion_control_exact_required_context"],
            "TOKEN_VAZIO_NOT_OBSERVED_BY_THIS_ENDPOINT",
        )
        self.assertFalse(report["claim_allowed"])

    def test_missing_protection_payload_fails_closed(self):
        report = classify_branch({"name": "main"})
        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("PROTECTION_NOT_ENABLED", report["failure_modes"])
        self.assertIn("REQUIRED_STATUS_CHECKS_NOT_ENFORCED", report["failure_modes"])


if __name__ == "__main__":
    unittest.main()
