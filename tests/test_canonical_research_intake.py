from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("intake", ROOT / "scripts" / "canonical_research_intake.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MOD)


class CanonicalResearchIntakeTests(unittest.TestCase):
    def setUp(self):
        self.config = MOD.load_config(ROOT / "configs" / "00_CANONICAL_RESEARCH_INTAKE.xml")
        self.raw = MOD.load_json_records(ROOT / "tests" / "fixtures" / "research_intake_fixture.json")
        self.reviews = MOD.load_review_ledger(ROOT / "data" / "research_intake" / "review_ledger.v1.jsonl")
        self.id_registry = MOD.load_id_registry(
            ROOT / "data" / "research_intake" / "id_registry.v1.json",
            self.config["prefix"],
            self.config["width"],
        )

    def build(self):
        return MOD.assign_states(
            MOD.deduplicate(self.raw), self.reviews, self.config["prefix"], self.config["width"], self.id_registry
        )

    def test_config_is_fail_closed(self):
        self.assertFalse(self.config["claim_allowed"])
        scholar = next(s for s in self.config["sources"] if s["id"] == "google_scholar")
        self.assertEqual(scholar["mode"], "manual_only")
        self.assertEqual(scholar["enabled"], "false")

    def test_deduplicates_same_doi_across_metadata_sources(self):
        records = MOD.deduplicate(self.raw)
        record = next(r for r in records if r["canonical_key"] == "doi:10.1000/a")
        self.assertEqual(record["metadata_source_count"], 2)
        self.assertTrue(record["metadata_corroboration_only"])

    def test_unknown_is_token_vazio_not_zero(self):
        records = self.build()
        missing = next(r for r in records if r["canonical_key"].startswith("source:manual"))
        self.assertEqual(missing["state"], "TOKEN_VAZIO")
        self.assertNotEqual(missing["metadata_completeness"], 0.0)

    def test_no_automatic_promotion_from_duplicate_count(self):
        records = self.build()
        duplicate = next(r for r in records if r["canonical_key"] == "doi:10.1000/a")
        self.assertEqual(duplicate["state"], "UNREVIEWED")

    def test_review_ledger_controls_state(self):
        records = self.build()
        hypothesis = next(r for r in records if r["canonical_key"] == "doi:10.1000/b")
        self.assertEqual(hypothesis["state"], "HYPOTHESIS_CANDIDATE")
        self.assertIsNotNone(hypothesis["review"])
        self.assertTrue(hypothesis["review"]["falsifier"])
        self.assertTrue(hypothesis["review"]["scope"])

    def test_unlikely_requires_explicit_review(self):
        records = self.build()
        item = next(r for r in records if r["canonical_key"] == "arxiv:2601.00001")
        self.assertEqual(item["state"], "UNLIKELY_UNDER_CURRENT_EVIDENCE")
        self.assertIn("não refutação universal", item["state_reason"])

    def test_public_export_is_allowlisted_and_sanitized(self):
        export = MOD.public_export(self.build(), "2026-07-23T00:00:00Z")
        self.assertEqual(len(export["records"]), 1)
        record = export["records"][0]
        self.assertEqual(record["canonical_key"], "pmid:1")
        self.assertNotIn("source_records", record)
        self.assertNotIn("state_reason", record)
        self.assertTrue(record["falsifier"])
        self.assertFalse(record["claim_allowed"])

    def test_sequence_is_stable_and_monotonic(self):
        first = self.build()
        second = self.build()
        self.assertEqual([r["record_id"] for r in first], [r["record_id"] for r in second])
        self.assertEqual(first[0]["record_id"], "LIT-00000001")

    def test_existing_ids_do_not_shift_when_earlier_key_arrives(self):
        prior = {r["canonical_key"]: r["record_id"] for r in self.build()}
        expanded = self.raw + [{
            "source": "crossref", "source_record_id": "10.0000/aaa",
            "title": "An earlier-sorting canonical key", "year": 2026,
            "authors": ["Z. Test"], "doi": "10.0000/aaa", "domain": "testing",
            "url": "https://doi.org/10.0000/aaa",
        }]
        records = MOD.assign_states(
            MOD.deduplicate(expanded), self.reviews, self.config["prefix"], self.config["width"], self.id_registry
        )
        after = {r["canonical_key"]: r["record_id"] for r in records}
        for key, record_id in prior.items():
            self.assertEqual(after[key], record_id)
        self.assertEqual(after["doi:10.0000/aaa"], "LIT-00000007")

    def test_synthesis_trigger_does_not_allow_claim(self):
        syn = MOD.synthesis(self.build(), self.config, "2026-07-23T00:00:00Z")
        self.assertFalse(syn["claim_allowed"])
        self.assertEqual(syn["trigger_policy"], "HEURISTIC_TRIGGER_NOT_PROMOTION")

    def test_artifacts_and_checksums_are_deterministic(self):
        records = self.build()
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            MOD.emit_artifacts(records, self.config, Path(a), "2026-07-23T00:00:00Z", self.id_registry)
            MOD.emit_artifacts(records, self.config, Path(b), "2026-07-23T00:00:00Z", self.id_registry)
            self.assertEqual((Path(a) / "CHECKSUMS.sha256").read_text(), (Path(b) / "CHECKSUMS.sha256").read_text())
            manifest = json.loads((Path(a) / "00_MANIFEST.json").read_text())
            self.assertFalse(manifest["claim_allowed"])

    def test_invalid_review_state_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bad.jsonl"
            path.write_text('{"canonical_key":"x","state":"PROVADO","reviewed_by":"a","reason":"b"}\n')
            with self.assertRaises(ValueError):
                MOD.load_review_ledger(path)

    def test_review_without_falsifier_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bad-review.jsonl"
            path.write_text(json.dumps({
                "canonical_key": "doi:10.1000/x", "state": "HYPOTHESIS_CANDIDATE",
                "reviewed_by": "reviewer", "reviewed_at": "2026-07-23T00:00:00Z",
                "reason": "reason", "scope": "scope", "evidence_basis": "EXTERNAL_METADATA",
                "public_export_allowed": False
            }) + "\n")
            with self.assertRaises(ValueError):
                MOD.load_review_ledger(path)

    def test_network_errors_become_token_vazio_records(self):
        normalized = MOD.normalize_record({
            "source": "x", "source_record_id": "NETWORK-ERROR", "title": "",
            "authors": [], "domain": "TOKEN_VAZIO"
        })
        self.assertTrue(normalized["canonical_key"].startswith("source:x"))


if __name__ == "__main__":
    unittest.main()
