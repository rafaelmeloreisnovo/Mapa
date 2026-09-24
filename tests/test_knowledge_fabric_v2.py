import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("knowledge_fabric_v2", ROOT / "scripts/validate_knowledge_fabric_v2.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MOD)
FIXTURE = ROOT / "tests/fixtures/knowledge_fabric_v2.valid.json"


class KnowledgeFabricV2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_pilot_bundle_passes(self):
        self.assertEqual([], MOD.validate(self.valid))

    def test_receipt_cannot_be_evidence(self):
        data = copy.deepcopy(self.valid)
        data["receipts"][0]["id"] = data["evidence"][0]["id"]
        self.assertIn("receipt_id_missing_duplicate_or_collides_with_evidence", MOD.validate(data))

    def test_receipt_must_reference_evidence(self):
        data = copy.deepcopy(self.valid)
        data["receipts"][0]["evidence_refs"] = ["receipt-1"]
        self.assertTrue(any(x.startswith("receipt_must_reference_evidence") for x in MOD.validate(data)))

    def test_private_publish_without_grant_denies(self):
        data = copy.deepcopy(self.valid)
        data["actions"].append({"id": "private-publish", "actor": "operator", "target_id": "private-file", "operation": "PUBLISH", "expected_decision": "ALLOW"})
        self.assertIn("authority_decision_mismatch:private-publish:expected_ALLOW_got_DENY", MOD.validate(data))

    def test_unknown_token_is_not_readable(self):
        data = copy.deepcopy(self.valid)
        data["actions"].append({"id": "token-read", "actor": "operator", "target_id": "unknown-token", "operation": "READ", "expected_decision": "ALLOW"})
        self.assertIn("authority_decision_mismatch:token-read:expected_ALLOW_got_DENY", MOD.validate(data))

    def test_relation_requires_scope_and_promotion_cap(self):
        data = copy.deepcopy(self.valid)
        del data["relations"][0]["scope"]
        data["relations"][0]["promotion_cap"] = "global_truth"
        defects = MOD.validate(data)
        self.assertIn("relation_field_missing:rel-1:scope", defects)
        self.assertIn("relation_promotion_cap:rel-1", defects)

    def test_relation_endpoints_must_exist(self):
        data = copy.deepcopy(self.valid)
        data["relations"][0]["target_id"] = "missing"
        self.assertIn("relation_endpoint_missing:rel-1:target_id", MOD.validate(data))

    def test_pull_request_requires_observed_lifecycle_event(self):
        data = copy.deepcopy(self.valid)
        data["events"] = []
        self.assertIn("mutable_pull_request_requires_event:pull-request-661", MOD.validate(data))

    def test_event_requires_observation_time(self):
        data = copy.deepcopy(self.valid)
        data["events"][0]["observed_at"] = "unknown"
        self.assertIn("event_observed_at_invalid:event-pr-1", MOD.validate(data))

    def test_hash_requires_scope(self):
        data = copy.deepcopy(self.valid)
        data["identities"][0]["hash"] = "abc"
        data["identities"][0]["hash_scope"] = None
        self.assertIn("hash_scope_required:identity-formula-1", MOD.validate(data))

    def test_duplicate_identity_rejected(self):
        data = copy.deepcopy(self.valid)
        data["objects"][1]["id"] = data["objects"][0]["id"]
        self.assertIn("duplicate_object_id", MOD.validate(data))

    def test_typed_identity_cannot_alias_artifact_and_execution(self):
        data = copy.deepcopy(self.valid)
        data["objects"][7]["id"] = data["objects"][9]["id"]
        self.assertTrue(any(x.startswith("typed_id_collision:artifact-1:") for x in MOD.validate(data)))

    def test_authority_grant_requires_source_pointer(self):
        data = copy.deepcopy(self.valid)
        data["authorities"][0]["source_ref"] = ""
        self.assertIn("authority_source_ref_required:authority-fixture-1", MOD.validate(data))

    def test_object_requires_separate_identity(self):
        data = copy.deepcopy(self.valid)
        data["objects"][0]["identity_ref"] = "missing-identity"
        self.assertIn("object_identity_ref_missing:formula-1", MOD.validate(data))

    def test_context_cannot_weaken_member_access(self):
        data = copy.deepcopy(self.valid)
        data["contexts"][1]["access_class"] = "public"
        self.assertIn("context_access_broader_than_members:context-private", MOD.validate(data))

    def test_delta_is_append_only_and_creates_successor(self):
        data = copy.deepcopy(self.valid)
        data["deltas"][0]["append_only"] = False
        data["deltas"][0]["successor_state_id"] = data["deltas"][0]["parent_state_id"]
        defects = MOD.validate(data)
        self.assertIn("delta_must_be_append_only:delta-pr-state", defects)
        self.assertIn("delta_must_create_successor_state:delta-pr-state", defects)

    def test_gap_requires_exact_next_probe(self):
        data = copy.deepcopy(self.valid)
        data["gaps"][0]["next_probe"] = ""
        self.assertIn("gap_reason_and_next_probe_required:gap-pr-browser", MOD.validate(data))


    def test_claim_requires_evidence_not_execution_artifact(self):
        data = copy.deepcopy(self.valid)
        data["objects"][-1]["evidence_refs"] = ["execution-1"]
        self.assertIn("claim_must_reference_evidence:claim-1", MOD.validate(data))


if __name__ == "__main__":
    unittest.main()
