import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"data"/"federation"/"PAT_CAPABILITY_FEDERATION_V1.json"

class PatCapabilityFederationTests(unittest.TestCase):
    def load(self):
        return json.loads(PATH.read_text(encoding="utf-8"))

    def test_authority_split(self):
        data=self.load()
        self.assertEqual(data["authority"],"rafaelmeloreisnovo/Mapa")
        self.assertEqual(data["executor"],"rafaelmeloreisnovo/RafGitTools")
        self.assertFalse(data["claim_allowed"])

    def test_secret_ids_are_uppercase_and_exact(self):
        data=self.load()
        expected={"PAT_ACTIONS","PAT_AGENTS","PAT_CODESPACES","PAT_DEPENDABOT","PAT_ENV"}
        self.assertEqual(set(data["canonical_secret_ids"]),expected)
        self.assertTrue(all(x==x.upper() for x in data["canonical_secret_ids"]))
        self.assertEqual(data["canonical_environment_display"],"PAT_ENVIRONMENTS")

    def test_no_secret_values(self):
        data=self.load()
        self.assertEqual(data["secret_values"],"FORBIDDEN")
        raw=PATH.read_text(encoding="utf-8")
        self.assertNotIn("ghp_",raw)
        self.assertNotIn("github_pat_",raw)

    def test_unmerged_executor_cannot_be_active(self):
        data=self.load()
        self.assertEqual(data["executor_source"]["merge_state"],"UNMERGED_AT_PROJECTION_CREATION")
        self.assertEqual(data["state"],"PENDING_EXECUTOR_SOURCE_MERGE")

if __name__=="__main__":
    unittest.main()
