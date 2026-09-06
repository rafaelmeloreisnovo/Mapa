import json, pathlib, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
POL = json.loads((ROOT/"data"/"control-plane"/"PROFILE_OS_CI_POLICY.v1.json").read_text(encoding="utf-8"))
WF = ROOT/".github"/"workflows"/"profile-os-registry.yml"

class ProfileOSCiGateTests(unittest.TestCase):
    def test_composition_unique(self):
        self.assertEqual(len(POL["composition"]), len(set(POL["composition"])))
    def test_all_runtime_tokens_are_typed(self):
        self.assertTrue(all(x["gate_policy"] in {"BLOCKING_RUNTIME","POST_RUN_BLOCKING_FOR_CLAIM"} for x in POL["runtime_tokens"]))
    def test_workflow_actions_are_full_sha_pinned(self):
        text=WF.read_text(encoding="utf-8")
        uses=[line.strip() for line in text.splitlines() if "uses:" in line]
        self.assertGreaterEqual(len(uses),3)
        for line in uses:
            self.assertRegex(line, r"@[0-9a-f]{40}(?:\s|$)")
        self.assertNotIn("@v4", text)
        self.assertNotIn("@v5", text)
        self.assertNotIn("@v7", text)
    def test_workflow_uploads_even_on_failure(self):
        text=WF.read_text(encoding="utf-8")
        self.assertIn("if: always()", text)
        self.assertIn("profile-os-evidence-${{ github.run_id }}", text)
    def test_claim_remains_closed(self):
        self.assertIs(POL["claim_allowed"], False)

if __name__ == "__main__": unittest.main()
