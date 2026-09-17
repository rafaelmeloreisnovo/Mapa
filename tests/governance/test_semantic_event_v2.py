from __future__ import annotations

import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "governance" / "check_semantic_event_v2.py"
FIXTURE = ROOT / "tests" / "fixtures" / "mu-semantic-event.v2.valid.json"

spec = importlib.util.spec_from_file_location("sev2", SCRIPT)
sev2 = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(sev2)


class SemanticEventV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.event = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def clone(self):
        return json.loads(json.dumps(self.event))

    def test_fixture_valid(self):
        self.assertEqual([], sev2.validate_event(self.event))

    def test_canonical_hash_is_deterministic(self):
        self.assertEqual(sev2.canonical_sha256(self.event), sev2.canonical_sha256(self.clone()))

    def test_actor_does_not_prove_authorship(self):
        event = self.clone()
        event["authority"]["authorship_authority"]["state"] = "VERIFIED_LIMITED"
        event["authority"]["authorship_authority"]["evidence_refs"] = []
        errors = sev2.validate_event(event)
        self.assertTrue(any("does not prove VERIFIED_LIMITED authorship" in e for e in errors))

    def test_minor_related_privacy_fails_closed(self):
        event = self.clone()
        event["authority"]["minor_related"] = "YES"
        event["authority"]["privacy_class"] = "PUBLIC"
        errors = sev2.validate_event(event)
        self.assertTrue(any("minor-related event must fail closed" in e for e in errors))

    def test_claim_authority_requires_gate_and_evidence(self):
        event = self.clone()
        ca = event["authority"]["claim_authority"]
        ca["state"] = "VERIFIED_LIMITED"
        ca["gate_refs"] = []
        ca["evidence_refs"] = []
        errors = sev2.validate_event(event)
        self.assertTrue(any("requires gate_refs" in e for e in errors))
        self.assertTrue(any("requires evidence_refs" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
