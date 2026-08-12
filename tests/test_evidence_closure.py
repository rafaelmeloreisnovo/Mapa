import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_evidence_closure import _canonical_sha256, validate


AXES = {
    "CODE": "PASS",
    "BUILD": "NOT_APPLICABLE",
    "RUNTIME": "NOT_APPLICABLE",
    "TEST": "PASS",
    "CI": "NOT_APPLICABLE",
    "DEVICE": "NOT_APPLICABLE",
    "SECURITY": "NOT_APPLICABLE",
    "PROVENANCE": "PASS",
    "REPRODUCIBILITY": "NOT_APPLICABLE",
}


def base_record():
    return {
        "schema_version": "evidence-closure-record.v1",
        "closure_id": "TEST-CLOSURE-001",
        "revision": 0,
        "status": "CLOSED_PASS",
        "claim_allowed": True,
        "scope": "STRUCTURAL_TEST",
        "required_axes": ["CODE", "TEST", "PROVENANCE"],
        "evidence_vector": dict(AXES),
        "uncertainty": {"class": "MEASURED", "reasons": []},
        "problem": "Prove the closure contract validator behaves fail closed.",
        "risk": "False promotion would collapse independent evidence axes.",
        "next_probe": "Run the same deterministic unit suite after any contract change.",
        "closure_rule": "All required axes pass and an immutable receipt is present.",
        "falsifier": "Any adversarial fixture accepted by the validator falsifies closure.",
        "provenance": [{
            "kind": "github",
            "locator": "https://github.com/example/repo/commit/0123456789012345678901234567890123456789",
            "authority": "COMMIT_PINNED",
            "commit_sha": "0123456789012345678901234567890123456789",
            "sha256": None,
        }],
        "receipts": [{
            "locator": "tests://evidence-closure",
            "sha256": "a" * 64,
            "producer": "unittest",
            "observed_at": "2026-08-12T08:25:00-03:00",
        }],
        "dependencies": [],
        "contradictions": [],
        "previous_record_sha256": None,
        "transition_reason": "Initial test closure.",
        "observed_at": "2026-08-12T08:25:00-03:00",
        "tags": ["test"],
    }


def run_records(records):
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "ledger.jsonl"
        path.write_text(
            "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in records) + "\n",
            encoding="utf-8",
        )
        return validate(path)


class EvidenceClosureTests(unittest.TestCase):
    def test_valid_closed_pass(self):
        errors, summary = run_records([base_record()])
        self.assertEqual([], errors)
        self.assertEqual("PASS", summary["status"])

    def test_token_vazio_cannot_promote_claim(self):
        record = base_record()
        record["status"] = "TOKEN_VAZIO"
        record["claim_allowed"] = True
        record["evidence_vector"]["TEST"] = "TOKEN_VAZIO"
        record["uncertainty"] = {"class": "TOKEN_VAZIO", "reasons": ["test execution absent"]}
        record["receipts"] = []
        errors, _ = run_records([record])
        self.assertTrue(any("claim_allowed=true requires CLOSED_PASS" in e for e in errors))

    def test_closed_pass_rejects_unresolved_axis(self):
        record = base_record()
        record["evidence_vector"]["TEST"] = "OBSERVED_LIMITED"
        errors, _ = run_records([record])
        self.assertTrue(any("unresolved required axes" in e for e in errors))

    def test_closed_pass_rejects_open_dependency(self):
        record = base_record()
        record["dependencies"] = [{
            "closure_id": "DEP-001",
            "state": "BLOCKED",
            "locator": "github://example/dep",
        }]
        errors, _ = run_records([record])
        self.assertTrue(any("unresolved dependencies" in e for e in errors))

    def test_closed_pass_rejects_open_contradiction(self):
        record = base_record()
        record["contradictions"] = [{
            "id": "C1",
            "lhs": "claim A",
            "rhs": "evidence not-A",
            "state": "OPEN",
            "resolution_evidence": None,
        }]
        errors, _ = run_records([record])
        self.assertTrue(any("open contradictions" in e for e in errors))

    def test_append_only_hash_chain(self):
        first = base_record()
        first["status"] = "EVIDENCED"
        first["claim_allowed"] = False
        first["receipts"] = []
        first["uncertainty"] = {"class": "BOUNDED", "reasons": ["CI intentionally not required"]}
        second = base_record()
        second["revision"] = 1
        second["previous_record_sha256"] = _canonical_sha256(first)
        second["transition_reason"] = "Receipt added after deterministic test execution."
        errors, summary = run_records([first, second])
        self.assertEqual([], errors)
        self.assertEqual(2, summary["records"])

    def test_hash_chain_detects_history_mutation(self):
        first = base_record()
        first["status"] = "EVIDENCED"
        first["claim_allowed"] = False
        first["receipts"] = []
        first["uncertainty"] = {"class": "BOUNDED", "reasons": ["bounded"]}
        second = base_record()
        second["revision"] = 1
        second["previous_record_sha256"] = _canonical_sha256(first)
        second["transition_reason"] = "Advance after evidence."
        first["problem"] = "mutated historical record"
        errors, _ = run_records([first, second])
        self.assertTrue(any("previous_record_sha256 mismatch" in e for e in errors))

    def test_duplicate_json_key_fails(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            path.write_text('{"schema_version":"evidence-closure-record.v1","schema_version":"x"}\n', encoding="utf-8")
            errors, _ = validate(path)
        self.assertTrue(any("duplicate key" in e for e in errors))

    def test_private_drive_url_rejected_from_public_projection(self):
        record = base_record()
        record["provenance"] = [{
            "kind": "drive_private_sanitized",
            "locator": "https://drive.google.com/file/d/private",
            "authority": "OBSERVED",
            "commit_sha": None,
            "sha256": None,
        }]
        errors, _ = run_records([record])
        self.assertTrue(any("private Drive URL" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
