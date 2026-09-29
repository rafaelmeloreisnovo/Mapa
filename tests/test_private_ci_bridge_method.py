from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METHOD = ROOT / "data" / "routing" / "private_ci_bridge_method_v1.json"


class PrivateCiBridgeMethodTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(METHOD.read_text(encoding="utf-8"))

    def test_authority_is_separated(self):
        authority = self.doc["authority"]
        self.assertEqual(authority["methodology_and_routing"], "rafaelmeloreisnovo/Mapa")
        self.assertEqual(authority["executor"], "rafaelmeloreisnovo/RafGitTools")
        self.assertEqual(authority["source_and_replay_manifest"], "target private repository")

    def test_route_has_secretless_execution_boundary(self):
        stages = {item["stage"]: item for item in self.doc["route"]}
        self.assertTrue(stages["EXACT_SHA_ACCESS"]["secret_access"])
        self.assertFalse(stages["SECRETLESS_REPLAY"]["secret_access"])
        self.assertFalse(stages["SANITIZE"]["secret_access"])

    def test_claim_and_security_gaps_are_not_promoted(self):
        self.assertFalse(self.doc["claim_allowed"])
        self.assertEqual(
            self.doc["privacy"]["hostile_source_network_exfiltration_protection"],
            "TOKEN_VAZIO_NOT_ENFORCED_V1",
        )
        self.assertEqual(
            self.doc["zipraf"]["external_signature_profile"],
            "TOKEN_VAZIO_NOT_IMPLEMENTED",
        )

    def test_core_invariants_exist(self):
        invariants = set(self.doc["invariants"])
        for required in (
            "SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM",
            "TOKEN_VAZIO != PASS",
            "IMPLEMENTED_UNTESTED != PASS",
            "PRIVATE_SOURCE != PUBLIC_ARTIFACT",
            "SECRET_REFERENCE != SECRET_VALUE",
            "ZIPRAF_CONTAINER != ENCRYPTION",
        ):
            self.assertIn(required, invariants)


if __name__ == "__main__":
    unittest.main()
