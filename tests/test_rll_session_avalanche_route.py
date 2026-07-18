import importlib.util
import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location(
    "route", ROOT / "scripts/validate_rll_session_avalanche_route.py"
)
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
assert SPEC.loader
SPEC.loader.exec_module(module)
ROUTE = json.loads(
    (ROOT / "data/federation/rll-session-avalanche-route-v1.json").read_text()
)


class RllSessionAvalancheRouteTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(module.validate(ROUTE), [])

    def test_roles(self):
        self.assertEqual(
            {node["role"] for node in ROUTE["nodes"]}, module.REQUIRED_ROLES
        )

    def test_external_commits_pinned(self):
        self.assertTrue(
            all(
                node["commit"] == "SELF_AFTER_MERGE"
                or module.SHA40.fullmatch(node["commit"])
                for node in ROUTE["nodes"]
            )
        )

    def test_map_is_pointer_only(self):
        self.assertFalse(ROUTE["invariants"]["map_is_source_authority"])

    def test_claim_gate_closed(self):
        self.assertFalse(ROUTE["invariants"]["claim_allowed"])

    def test_private_payload_not_copied(self):
        self.assertFalse(ROUTE["invariants"]["private_payload_copied"])

    def test_dangling_edge_rejected(self):
        changed = json.loads(json.dumps(ROUTE))
        changed["edges"][0]["to"] = "NOPE"
        self.assertTrue(module.validate(changed))

    def test_branch_name_cannot_replace_commit_pin(self):
        changed = json.loads(json.dumps(ROUTE))
        changed["nodes"][0]["commit"] = "main"
        self.assertTrue(module.validate(changed))

    def test_no_automatic_mutation(self):
        self.assertFalse(ROUTE["invariants"]["automatic_cross_repo_write"])
        self.assertFalse(ROUTE["invariants"]["automatic_merge"])


if __name__ == "__main__":
    unittest.main()
