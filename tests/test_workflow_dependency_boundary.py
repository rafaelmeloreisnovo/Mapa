import tempfile
import unittest
from pathlib import Path

from scripts.audit_workflow_dependency_boundary import audit


GOOD_LICENSE = "GNU GENERAL PUBLIC LICENSE\nVersion 3, 29 June 2007\n"
GOOD_WORKFLOW = """name: test
permissions:
  contents: read
jobs:
  test:
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with:
          persist-credentials: false
"""


class WorkflowDependencyBoundaryTests(unittest.TestCase):
    def run_audit(self, workflow: str = GOOD_WORKFLOW, license_text: str = GOOD_LICENSE):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/rafaelia-adaptive-cycle.yml").write_text(workflow, encoding="utf-8")
            (root / "LICENSE").write_text(license_text, encoding="utf-8")
            return audit(root, ".github/workflows/rafaelia-adaptive-cycle.yml", "LICENSE")

    def test_structural_boundary_passes_without_claim_promotion(self):
        result = self.run_audit()
        self.assertEqual(result["decision"], "VERIFIED_BOUNDARY_READ_ONLY")
        self.assertFalse(result["claim_allowed"])
        self.assertFalse(result["automatic_mutation"])
        self.assertFalse(result["automatic_merge"])

    def test_unpinned_external_action_blocks(self):
        workflow = GOOD_WORKFLOW.replace(
            "actions/checkout@11d5960a326750d5838078e36cf38b85af677262",
            "actions/checkout@v4",
        )
        result = self.run_audit(workflow=workflow)
        self.assertEqual(result["decision"], "BLOCKED_POLICY_REGRESSION")
        self.assertIn("all_external_actions_sha_pinned", result["blocking_regressions"])

    def test_write_permission_blocks(self):
        result = self.run_audit(workflow=GOOD_WORKFLOW.replace("contents: read", "contents: write"))
        self.assertEqual(result["decision"], "BLOCKED_POLICY_REGRESSION")
        self.assertIn("contents_permission_read", result["blocking_regressions"])
        self.assertIn("contents_permission_write_absent", result["blocking_regressions"])

    def test_persisted_checkout_credentials_block(self):
        result = self.run_audit(workflow=GOOD_WORKFLOW.replace("persist-credentials: false", "persist-credentials: true"))
        self.assertEqual(result["decision"], "BLOCKED_POLICY_REGRESSION")
        self.assertIn("checkout_persist_credentials_false", result["blocking_regressions"])

    def test_dependency_compatibility_remains_token_vazio(self):
        result = self.run_audit()
        self.assertTrue(result["token_vazio"]["dependency_license_compatibility"].startswith("TOKEN_VAZIO"))
        self.assertTrue(result["token_vazio"]["pinned_action_node24_native_compatibility"].startswith("TOKEN_VAZIO"))
        self.assertFalse(result["runtime_observation"]["warning_is_compatibility_proof"])

    def test_large_workflow_is_scanned_linearly(self):
        noise = "\n".join(f"      # inert-line-{i}" for i in range(20000))
        workflow = GOOD_WORKFLOW + "\n" + noise + "\n"
        result = self.run_audit(workflow=workflow)
        self.assertEqual(result["decision"], "VERIFIED_BOUNDARY_READ_ONLY")
        self.assertEqual(result["complexity_contract"]["workflow_scan"], "O(lines)")
        self.assertFalse(result["complexity_contract"]["catastrophic_regex_backtracking"])

    def test_current_repository_boundary(self):
        root = Path(__file__).resolve().parents[1]
        result = audit(root, ".github/workflows/rafaelia-adaptive-cycle.yml", "LICENSE")
        self.assertEqual(result["decision"], "VERIFIED_BOUNDARY_READ_ONLY")
        self.assertFalse(result["claim_allowed"])


if __name__ == "__main__":
    unittest.main()
