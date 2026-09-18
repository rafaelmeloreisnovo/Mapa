#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "finalize_systematic_pragmatic_routing.py"
spec = importlib.util.spec_from_file_location("spms_finalizer", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


class SystematicPragmaticFinalizerTest(unittest.TestCase):
    def _source(self, root: Path, i: int) -> tuple[str, str]:
        source_gap_id = f"SOURCE-GAP-{i:02d}"
        rel = f"data/routing/operational-gaps/gap-{i:02d}.json"
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "gap_id": source_gap_id,
                    "owner": "rafaelmeloreisnovo/Mapa",
                    "claim_allowed": False,
                    "evidence_for": [f"observed-{i}"],
                    "detector": {"evidence_needed": f"receipt-{i}"},
                    "next_probe": f"probe-{i}",
                }
            ),
            encoding="utf-8",
        )
        return source_gap_id, rel

    def _fixture(self, root: Path):
        candidates = []
        reconciliation_rows = []
        for i in range(35):
            source_gap_id, rel = self._source(root, i)
            gap_id = mod.atlas_gap_id(source_gap_id)
            candidates.append(
                {
                    "source_gap_id": source_gap_id,
                    "source_paths": [rel],
                }
            )
            reconciliation_rows.append(
                {
                    "source_gap_id": source_gap_id,
                    "status": "CANDIDATE_EXACT_MATCH",
                    "candidate_atlas_gap_ids": [gap_id],
                }
            )

        routing = {
            "schema": "rafaelia.systematic-pragmatic-routing-bindings/v1",
            "claim_allowed": False,
            "gap_binding_candidates": candidates,
            "schema_families": [
                {
                    "family_id": f"SF-{i:02d}",
                    "schema_family": f"schema-{i:02d}",
                    "record_count": i + 1,
                }
                for i in range(25)
            ],
        }
        reconciliation = {
            "schema": "rafaelia.systematic-pragmatic-g4-reconciliation/v1",
            "claim_allowed": False,
            "reconciliation": reconciliation_rows,
        }
        append_entries = mod.generated_append_entries(routing, root)
        for row in append_entries:
            row["appended_at"] = "2026-09-18T00:00:00Z"
        policy = {
            "schema": mod.POLICY_SCHEMA,
            "claim_allowed": False,
        }
        return routing, reconciliation, append_entries, policy

    def test_full_fixture_closes_internal_routing_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            routing, reconciliation, append_entries, policy = self._fixture(root)
            out = mod.build(
                routing,
                reconciliation,
                append_entries,
                policy,
                root,
            )
            mod.validate(out)
            self.assertEqual(out["system_state"], "COMPLETE_STRUCTURAL_ROUTING")
            self.assertEqual(out["summary"]["source_gap_bindings"], 35)
            self.assertEqual(
                out["summary"]["schema_families_structurally_resolved"], 25
            )
            self.assertEqual(out["summary"]["remaining_internal_review_required"], 0)
            self.assertEqual(
                out["summary"]["remaining_internal_binding_token_vazio"], 0
            )
            self.assertTrue(out["summary"]["external_subjects_may_remain_open"])
            self.assertTrue(
                all(
                    row["state"] == "BOUND_GOVERNED_SOURCE_RECORD"
                    and row["subject_level_closure"] is False
                    for row in out["source_bindings"]
                )
            )
            self.assertTrue(
                all(
                    row["state"] == "STRUCTURAL_FAMILY_ACCEPTED"
                    and row["semantic_equivalence"] is False
                    for row in out["schema_family_resolutions"]
                )
            )

    def test_committed_record_drift_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            routing, reconciliation, append_entries, policy = self._fixture(root)
            append_entries[0]["record"]["provider"] = "Google Drive"
            with self.assertRaises(ValueError):
                mod.build(
                    routing,
                    reconciliation,
                    append_entries,
                    policy,
                    root,
                )

    def test_ambiguous_reconciliation_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            routing, reconciliation, append_entries, policy = self._fixture(root)
            reconciliation["reconciliation"][0]["status"] = "AMBIGUOUS_EXACT_EVIDENCE"
            with self.assertRaises(ValueError):
                mod.build(
                    routing,
                    reconciliation,
                    append_entries,
                    policy,
                    root,
                )


if __name__ == "__main__":
    unittest.main()
