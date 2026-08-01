import json
import unittest
from pathlib import Path

from scripts.validate_branch_topology import validate_event, validate_manifest

ROOT = Path(__file__).resolve().parents[1]


class BranchTopologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / "data/governance/branch_topology_main_numbered_v1.json"
        cls.data = json.loads(path.read_text(encoding="utf-8"))

    def test_manifest(self):
        self.assertEqual([], validate_manifest(self.data))

    def test_default_branch_must_be_main(self):
        errors = validate_event(
            self.data,
            repository_default_branch="other",
            base_ref="main",
            head_ref="feature/example",
            pr_body="",
        )
        self.assertNotEqual([], errors)

    def test_unknown_numbered_branch(self):
        errors = validate_event(
            self.data,
            repository_default_branch="main",
            base_ref="main",
            head_ref="main_10_unknown",
            pr_body="",
        )
        self.assertNotEqual([], errors)

    def test_complete_promotion(self):
        body = "\n".join([
            "source: fixture",
            "claim_state: TOKEN_VAZIO",
            "evidence: fixture",
            "falsifier: fixture",
            "rollback: fixture",
            "decision: review",
        ])
        errors = validate_event(
            self.data,
            repository_default_branch="main",
            base_ref="main",
            head_ref="main_05_evidencias",
            pr_body=body,
        )
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
