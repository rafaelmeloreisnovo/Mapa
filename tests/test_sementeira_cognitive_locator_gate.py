import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "sementeira_cognitive_locator_gate.py"
spec = importlib.util.spec_from_file_location("sementeira_cognitive_locator_gate", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def sha(ch: str) -> str:
    return ch * 64


def cognitive_payload():
    return {
        "protocol_version": "SEMENTEIRA-5X7-V1",
        "event_id": "evt-linked",
        "variables": {
            "intention": "Link evidence identities.",
            "evidence": "Three local artifacts.",
            "human_state": "Low cognitive surface.",
            "execution_capacity": "Python stdlib.",
            "next_falsifiable_gate": "Block one-byte mismatch.",
        },
        "directions": {
            "fact": "Artifacts exist.",
            "gap": "Truth remains unproved.",
            "invariant": "Identity is not truth.",
            "variant": "Composite gate.",
            "proof_or_falsifier": "Mutate one byte.",
            "parable": "The seal proves the scroll, not its teaching.",
            "feedback": "Route only matching refs.",
        },
        "evidence": [
            {"id": "src", "kind": "SOURCE", "locator": "docs/source.md", "sha256": sha("a")},
            {"id": "method", "kind": "METHOD", "locator": "scripts/method.py", "sha256": sha("b")},
            {"id": "test", "kind": "TEST_RECEIPT", "locator": "auditoria/test.json", "sha256": sha("c")},
        ],
        "claims": [{
            "id": "claim-1",
            "statement": "All claim evidence identities are linked.",
            "falsifier": "Any ref is missing, mismatched, unresolved or blocked.",
            "evidence_refs": ["src", "method", "test"],
            "requested_state": "EVIDENCED",
            "weight": None,
        }],
        "claim_allowed": False,
    }


def cognitive_receipt(payload):
    core = {
        "protocol_version": "SEMENTEIRA-5X7-V1",
        "input_sha256": module.sha256_json(payload),
        "structural_pass": True,
        "claim_allowed": False,
        "blocking_findings": [],
        "gaps": [],
        "claims": [{
            "id": "claim-1",
            "inferred_state": "LOCAL_EVIDENCE_CANDIDATE",
            "claim_allowed": False,
            "evidence_kinds": ["METHOD", "SOURCE", "TEST_RECEIPT"],
        }],
        "r3": {"F_ok": "ok", "F_gap": "gap", "F_next": "next"},
    }
    core["receipt_sha256"] = module.sha256_json(core)
    return core


def locator_receipt(payload):
    results = []
    for item in payload["evidence"]:
        results.append({
            "evidence_id": item["id"],
            "locator": item["locator"],
            "expected_sha256": item["sha256"],
            "actual_sha256": item["sha256"],
            "status": "HASH_MATCH",
            "referenced_by_claim": True,
            "resolved_relative_path": item["locator"],
            "bytes": 1,
            "reason": None,
        })
    core = {
        "protocol_version": "SEMENTEIRA-LOCATOR-RESOLVER-V1",
        "input_sha256": sha("d"),
        "root_policy": "AUTHORIZED_REPOSITORY_ROOT_READ_ONLY",
        "artifact_identity_gate": "PASS",
        "all_referenced_hashes_match": True,
        "epistemic_promotion_allowed": False,
        "claim_allowed": False,
        "blocking_findings": [],
        "gaps": [],
        "referenced_evidence_ids": [x["id"] for x in payload["evidence"]],
        "results": results,
        "r3": {"F_ok": "ok", "F_gap": "gap", "F_next": "next"},
    }
    core["receipt_sha256"] = module.sha256_json(core)
    return core


def bundle():
    payload = cognitive_payload()
    return {
        "protocol_version": module.PROTOCOL_VERSION,
        "cognitive_payload": payload,
        "cognitive_receipt": cognitive_receipt(payload),
        "locator_receipt": locator_receipt(payload),
        "claim_allowed": False,
    }


def rehash(receipt):
    receipt["receipt_sha256"] = module.sha256_json({k: v for k, v in receipt.items() if k != "receipt_sha256"})


class CompositeGateTests(unittest.TestCase):
    def codes(self, receipt):
        return {item["code"] for item in receipt["blocking_findings"]}

    def test_all_match_routes_to_domain_review_but_never_promotes(self):
        receipt = module.build_receipt(bundle())
        self.assertTrue(receipt["structural_pass"])
        self.assertEqual(receipt["artifact_identity_link_gate"], "PASS")
        self.assertEqual(receipt["claims"][0]["promotion_readiness"], "READY_FOR_DOMAIN_SPECIFIC_REVIEW")
        self.assertFalse(receipt["claim_allowed"])
        self.assertFalse(receipt["epistemic_promotion_allowed"])

    def test_cognitive_input_hash_mismatch_blocks(self):
        data = bundle()
        data["cognitive_payload"]["event_id"] = "mutated"
        receipt = module.build_receipt(data)
        self.assertIn("COGNITIVE_INPUT_HASH_MISMATCH", self.codes(receipt))

    def test_cognitive_receipt_self_hash_invalid_blocks(self):
        data = bundle()
        data["cognitive_receipt"]["receipt_sha256"] = sha("0")
        self.assertIn("COGNITIVE_RECEIPT_HASH_INVALID", self.codes(module.build_receipt(data)))

    def test_locator_receipt_self_hash_invalid_blocks(self):
        data = bundle()
        data["locator_receipt"]["receipt_sha256"] = sha("0")
        self.assertIn("LOCATOR_RECEIPT_HASH_INVALID", self.codes(module.build_receipt(data)))

    def test_hash_mismatch_blocks_claim(self):
        data = bundle()
        result = data["locator_receipt"]["results"][0]
        result["status"] = "HASH_MISMATCH"
        result["actual_sha256"] = sha("f")
        data["locator_receipt"]["all_referenced_hashes_match"] = False
        data["locator_receipt"]["artifact_identity_gate"] = "BLOCKED"
        rehash(data["locator_receipt"])
        receipt = module.build_receipt(data)
        self.assertIn("CLAIM_EVIDENCE_IDENTITY_BLOCKED", self.codes(receipt))
        self.assertEqual(receipt["claims"][0]["promotion_readiness"], "BLOCKED_BY_ARTIFACT_IDENTITY")

    def test_unresolved_blocks_claim(self):
        data = bundle()
        data["locator_receipt"]["results"][1]["status"] = "TOKEN_VAZIO_UNRESOLVED"
        data["locator_receipt"]["all_referenced_hashes_match"] = False
        data["locator_receipt"]["artifact_identity_gate"] = "BLOCKED"
        rehash(data["locator_receipt"])
        self.assertIn("CLAIM_EVIDENCE_IDENTITY_BLOCKED", self.codes(module.build_receipt(data)))

    def test_blocked_locator_blocks_claim(self):
        data = bundle()
        data["locator_receipt"]["results"][2]["status"] = "BLOCKED_LOCATOR"
        data["locator_receipt"]["all_referenced_hashes_match"] = False
        data["locator_receipt"]["artifact_identity_gate"] = "BLOCKED"
        rehash(data["locator_receipt"])
        self.assertIn("CLAIM_EVIDENCE_IDENTITY_BLOCKED", self.codes(module.build_receipt(data)))

    def test_missing_locator_result_blocks(self):
        data = bundle()
        data["locator_receipt"]["results"].pop()
        rehash(data["locator_receipt"])
        self.assertIn("CLAIM_EVIDENCE_NOT_RESOLVED", self.codes(module.build_receipt(data)))

    def test_locator_link_mismatch_blocks(self):
        data = bundle()
        data["locator_receipt"]["results"][0]["locator"] = "docs/other.md"
        rehash(data["locator_receipt"])
        self.assertIn("EVIDENCE_LOCATOR_LINK_MISMATCH", self.codes(module.build_receipt(data)))

    def test_sha_link_mismatch_blocks(self):
        data = bundle()
        data["locator_receipt"]["results"][0]["expected_sha256"] = sha("e")
        data["locator_receipt"]["results"][0]["actual_sha256"] = sha("e")
        rehash(data["locator_receipt"])
        self.assertIn("EVIDENCE_SHA_LINK_MISMATCH", self.codes(module.build_receipt(data)))

    def test_cognitive_structural_failure_blocks(self):
        data = bundle()
        data["cognitive_receipt"]["structural_pass"] = False
        rehash(data["cognitive_receipt"])
        self.assertIn("COGNITIVE_GATE_NOT_PASSED", self.codes(module.build_receipt(data)))

    def test_upstream_claim_allowed_true_blocks(self):
        data = bundle()
        data["cognitive_receipt"]["claim_allowed"] = True
        rehash(data["cognitive_receipt"])
        self.assertIn("COGNITIVE_RECEIPT_PROMOTION_FORBIDDEN", self.codes(module.build_receipt(data)))

    def test_unknown_claim_ref_blocks(self):
        data = bundle()
        data["cognitive_payload"]["claims"][0]["evidence_refs"].append("unknown")
        data["cognitive_receipt"] = cognitive_receipt(data["cognitive_payload"])
        self.assertIn("CLAIM_EVIDENCE_REF_UNKNOWN", self.codes(module.build_receipt(data)))

    def test_missing_cognitive_claim_receipt_blocks(self):
        data = bundle()
        data["cognitive_receipt"]["claims"] = []
        rehash(data["cognitive_receipt"])
        self.assertIn("COGNITIVE_CLAIM_RECEIPT_MISSING", self.codes(module.build_receipt(data)))

    def test_receipt_is_deterministic(self):
        first = module.build_receipt(bundle())
        second = module.build_receipt(bundle())
        self.assertEqual(first["receipt_sha256"], second["receipt_sha256"])
        self.assertEqual(first["input_sha256"], second["input_sha256"])

    def test_even_ready_claim_is_never_allowed(self):
        receipt = module.build_receipt(bundle())
        self.assertTrue(receipt["claims"][0]["identity_supported"])
        self.assertFalse(receipt["claims"][0]["claim_allowed"])


if __name__ == "__main__":
    unittest.main()
