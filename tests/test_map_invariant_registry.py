from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audit_map_invariants", ROOT / "scripts" / "audit_map_invariants.py"
)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class InvariantRegistryTests(unittest.TestCase):
    def load_live(self):
        records, errors = MOD.load_jsonl(ROOT / "data/invariants/map_invariant_registry.v1.jsonl")
        self.assertEqual(errors, [])
        edges, errors = MOD.load_jsonl(ROOT / "data/invariants/map_invariant_edges.v1.jsonl")
        self.assertEqual(errors, [])
        return records, edges

    def test_live_registry_is_fail_closed_valid(self):
        receipt = MOD.audit_repository(
            ROOT,
            ROOT / "data/invariants/map_invariant_registry.v1.jsonl",
            ROOT / "data/invariants/map_invariant_edges.v1.jsonl",
            source_sha="0" * 40,
            run_id="UNIT_TEST",
            generated_at="TOKEN_VAZIO_UNIT_TEST_TIME",
        )
        self.assertEqual(receipt["status"], "PASS", receipt["errors"])
        self.assertFalse(receipt["claim_allowed"])
        self.assertEqual(receipt["metrics"]["orphan_count"], 0)
        self.assertEqual(receipt["metrics"]["cycle_count"], 0)
        self.assertGreaterEqual(receipt["metrics"]["invariant_count"], 10)

    def test_source_blob_drift_is_rejected(self):
        records, _ = self.load_live()
        record = copy.deepcopy(records[0])
        record["source"]["blob_sha"] = "0" * 40
        errors, _ = MOD.validate_record(record, ROOT, "fixture")
        self.assertTrue(any("SOURCE_DRIFT" in error for error in errors), errors)

    def test_false_test_promotion_is_rejected(self):
        records, _ = self.load_live()
        record = copy.deepcopy(records[0])
        record["verification_vector"]["T"] = "PASS"
        record["tests"] = []
        errors, _ = MOD.validate_record(record, ROOT, "fixture")
        self.assertTrue(any("FALSE_PROMOTION T=PASS" in error for error in errors), errors)

    def test_claim_promotion_with_token_vazio_is_rejected(self):
        records, _ = self.load_live()
        record = copy.deepcopy(records[0])
        record["claim_allowed"] = True
        errors, _ = MOD.validate_record(record, ROOT, "fixture")
        self.assertTrue(any("claim_allowed=true with TOKEN_VAZIO" in error for error in errors), errors)

    def test_broken_reference_is_rejected(self):
        records, _ = self.load_live()
        record = copy.deepcopy(records[0])
        record["validators"] = ["scripts/DOES_NOT_EXIST.py"]
        errors, _ = MOD.validate_record(record, ROOT, "fixture")
        self.assertTrue(any("broken validators reference" in error for error in errors), errors)

    def test_requires_cycle_is_detected(self):
        ids = {"MAP-INV-AAA-001", "MAP-INV-BBB-001"}
        edges = [
            {"relation": "requires", "from": "MAP-INV-AAA-001", "to": "MAP-INV-BBB-001"},
            {"relation": "requires", "from": "MAP-INV-BBB-001", "to": "MAP-INV-AAA-001"},
        ]
        _, _, cyclic = MOD.requires_topology(ids, edges)
        self.assertEqual(cyclic, sorted(ids))

    def _minimal_record(self, iid: str, statement: str, source: str, blob: str):
        return {
            "schema_version": "map.invariant/v1",
            "invariant_id": iid,
            "version": 1,
            "family": "topology",
            "canonical_statement": statement,
            "scope": ["fixture"],
            "authority": {
                "control_plane": "fixture",
                "implementation": "fixture",
                "evidence": "fixture",
            },
            "source": {
                "path": source,
                "blob_sha": blob,
                "producer_commit_sha": "TOKEN_VAZIO_PRODUCER_COMMIT",
                "observed_at_commit_sha": "1" * 40,
            },
            "validators": [source],
            "tests": [],
            "workflows": [],
            "receipts": [],
            "dependencies": [],
            "falsifiers": ["A deliberately failing fixture falsifier."],
            "verification_vector": {
                "D": "PASS",
                "I": "PASS",
                "T": "TOKEN_VAZIO_TEST",
                "C": "TOKEN_VAZIO_CI",
                "X": "NOT_APPLICABLE",
                "F": "TOKEN_VAZIO_FEDERATION",
            },
            "urgency": "P2_NECESSARY",
            "urgency_reason": "Fixture validates the fail-closed registry topology.",
            "claim_allowed": False,
            "token_vazio_reason": "Fixture intentionally leaves test, CI and federation open.",
            "next_verifiable_step": "Observe the expected fail-closed audit error.",
        }

    def test_orphan_invariant_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data/invariants").mkdir(parents=True)
            source = root / "source.py"
            source.write_text("VALUE = 1\n", encoding="utf-8")
            blob = MOD.git_blob_sha1(source)
            a = self._minimal_record(
                "MAP-INV-AAA-001", "Fixture invariant A remains connected to one implementation artifact.", "source.py", blob
            )
            b = self._minimal_record(
                "MAP-INV-BBB-001", "Fixture invariant B is intentionally orphaned for the falsifier test.", "source.py", blob
            )
            registry = root / "data/invariants/map_invariant_registry.v1.jsonl"
            registry.write_text(json.dumps(a) + "\n" + json.dumps(b) + "\n", encoding="utf-8")
            edge = {
                "schema_version": "map.invariant-edge/v1",
                "edge_id": "MAP-EDGE-0001",
                "relation": "implements",
                "from": "MAP-INV-AAA-001",
                "to": "artifact:source.py",
                "evidence_refs": ["source.py"],
                "claim_allowed": False,
            }
            edges = root / "data/invariants/map_invariant_edges.v1.jsonl"
            edges.write_text(json.dumps(edge) + "\n", encoding="utf-8")
            receipt = MOD.audit_repository(
                root, registry, edges,
                source_sha="2" * 40,
                run_id="ORPHAN_TEST",
                generated_at="TOKEN_VAZIO_UNIT_TEST_TIME",
            )
            self.assertEqual(receipt["status"], "FAIL")
            self.assertTrue(any("ORPHAN_INVARIANT MAP-INV-BBB-001" in e for e in receipt["errors"]), receipt["errors"])

    def test_dependency_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data/invariants").mkdir(parents=True)
            source = root / "source.py"
            source.write_text("VALUE = 1\n", encoding="utf-8")
            blob = MOD.git_blob_sha1(source)
            a = self._minimal_record(
                "MAP-INV-AAA-001", "Fixture root invariant with no declared dependency remains connected.", "source.py", blob
            )
            b = self._minimal_record(
                "MAP-INV-BBB-001", "Fixture child declares a dependency that is intentionally missing from edges.", "source.py", blob
            )
            b["dependencies"] = ["MAP-INV-AAA-001"]
            registry = root / "data/invariants/map_invariant_registry.v1.jsonl"
            registry.write_text(json.dumps(a) + "\n" + json.dumps(b) + "\n", encoding="utf-8")
            edge_rows = [
                {
                    "schema_version": "map.invariant-edge/v1",
                    "edge_id": "MAP-EDGE-0001",
                    "relation": "implements",
                    "from": "MAP-INV-AAA-001",
                    "to": "artifact:source.py",
                    "evidence_refs": ["source.py"],
                    "claim_allowed": False,
                },
                {
                    "schema_version": "map.invariant-edge/v1",
                    "edge_id": "MAP-EDGE-0002",
                    "relation": "implements",
                    "from": "MAP-INV-BBB-001",
                    "to": "artifact:source.py",
                    "evidence_refs": ["source.py"],
                    "claim_allowed": False,
                },
            ]
            edges = root / "data/invariants/map_invariant_edges.v1.jsonl"
            edges.write_text("\n".join(json.dumps(x) for x in edge_rows) + "\n", encoding="utf-8")
            receipt = MOD.audit_repository(
                root, registry, edges,
                source_sha="3" * 40,
                run_id="DRIFT_TEST",
                generated_at="TOKEN_VAZIO_UNIT_TEST_TIME",
            )
            self.assertEqual(receipt["status"], "FAIL")
            self.assertTrue(any("DEPENDENCY_DRIFT MAP-INV-BBB-001" in e for e in receipt["errors"]), receipt["errors"])

    def test_token_vazio_requires_next_step(self):
        records, _ = self.load_live()
        record = copy.deepcopy(records[0])
        record["next_verifiable_step"] = ""
        errors, _ = MOD.validate_record(record, ROOT, "fixture")
        self.assertTrue(any("next_verifiable_step required" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
