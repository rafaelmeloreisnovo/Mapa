import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"data"/"federation"/"SETUP_GOVERNANCE_WIZARD_V1.json"

class SetupWizardFederationTests(unittest.TestCase):
    def load(self):
        return json.loads(PATH.read_text(encoding="utf-8"))

    def test_authority_and_executor_are_separate(self):
        data=self.load()
        self.assertEqual(data["authority"],"rafaelmeloreisnovo/Mapa")
        self.assertEqual(data["executor"],"rafaelmeloreisnovo/RafGitTools")
        self.assertFalse(data["claim_allowed"])

    def test_unmerged_source_cannot_be_runtime_pass(self):
        data=self.load()
        self.assertEqual(data["executor_source"]["merge_state"],"UNMERGED")
        self.assertEqual(data["state"],"PENDING_BUILD_RUNTIME_EVIDENCE")

    def test_secret_values_are_forbidden(self):
        data=self.load()
        self.assertEqual(data["custody"]["secret_values"],"FORBIDDEN")

    def test_all_decision_states_are_preserved(self):
        self.assertEqual(set(self.load()["decision_states"]),{"AGREE","DISAGREE","LATER"})

if __name__=="__main__":
    unittest.main()
