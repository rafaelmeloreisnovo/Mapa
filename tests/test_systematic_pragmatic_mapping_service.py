#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SERVICE = REPO_ROOT / "tools" / "systematic_pragmatic_mapping_service.py"


class SystematicPragmaticMappingServiceTest(unittest.TestCase):
    def make_fixture(self, root: Path) -> Path:
        (root / "src").mkdir(exist_ok=True)
        (root / "src" / "loose.S").write_text(".text\n", encoding="utf-8")
        (root / "README.md").write_text(
            "TOKEN_VAZIO: runtime evidence\n", encoding="utf-8"
        )
        (root / "NOTES.md").write_text(
            "TODO: bind this operational note\n", encoding="utf-8"
        )
        atlas = {
            "schema": "RAFAELIA_GAP_ATLAS_V1",
            "claim_allowed": False,
            "records": [
                {
                    "gap_id": "GAP-FIXTURE-ASM-001",
                    "artifact_id": "different-id",
                    "priority": "P0",
                    "state": "TOKEN_VAZIO",
                    "authority_required": ["Fixture build authority"],
                    "evidence_required": ["Build descriptor binding"],
                    "next_gate": "Bind loose.S into the declared build graph.",
                    "source_refs": ["fixture: src/loose.S"],
                }
            ],
        }
        atlas_path = root / "atlas.json"
        atlas_path.write_text(json.dumps(atlas), encoding="utf-8")
        return atlas_path

    def run_service(self, root: Path, fail_on: str = "none"):
        atlas = self.make_fixture(root)
        out = root / "out"
        proc = subprocess.run(
            [
                sys.executable,
                str(SERVICE),
                "--root",
                f"fixture={root}",
                "--atlas",
                str(atlas),
                "--output-dir",
                str(out),
                "--exclude",
                "out",
                "--fail-on",
                fail_on,
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        action_map = json.loads(
            (out / "pragmatic_action_map.json").read_text(encoding="utf-8")
        )
        receipt = json.loads((out / "receipt.json").read_text(encoding="utf-8"))
        review = json.loads(
            (out / "cluster_review_queue.json").read_text(encoding="utf-8")
        )
        return proc, action_map, receipt, review

    def test_maps_to_action_queue_and_preserves_claim_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proc, action_map, receipt, review = self.run_service(root)

            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertFalse(action_map["claim_allowed"])
            self.assertFalse(receipt["claim_allowed"])
            self.assertFalse(review["claim_allowed"])
            self.assertGreater(action_map["summary"]["actions"], 0)

            loose = [
                row
                for row in action_map["actions"]
                if row["path"] == "src/loose.S"
                and row["gap"] == "ASM_NOT_REFERENCED_BY_BUILD"
            ]
            self.assertEqual(len(loose), 1)
            self.assertEqual(loose[0]["priority"], "P0")
            self.assertEqual(loose[0]["nibiguiri_state"], "INDEXED")
            self.assertEqual(loose[0]["mapped_gap_ids"], ["GAP-FIXTURE-ASM-001"])
            self.assertEqual(loose[0]["service"], "BUILD_INTEGRATION_AUDIT")
            self.assertEqual(loose[0]["effort"], "TOKEN_VAZIO_UNMEASURED")

            readme = [
                row for row in action_map["actions"] if row["path"] == "README.md"
            ]
            self.assertEqual(readme, [])
            self.assertGreaterEqual(
                action_map["summary"]["preserved_token_vazio_observations"], 1
            )

            notes = [
                row
                for row in action_map["actions"]
                if row["path"] == "NOTES.md"
                and row["gap"] == "UNRESOLVED_MARKERS"
            ]
            self.assertEqual(len(notes), 1)
            self.assertEqual(
                notes[0]["nibiguiri_state"],
                "NIBIGUIRI:CAUSA_DESCONHECIDA",
            )
            self.assertNotEqual(
                notes[0]["nibiguiri_state"],
                "NIBIGUIRI:OBVIO_NAO_INDEXADO",
            )
            self.assertGreaterEqual(action_map["summary"]["clusters"], 1)
            self.assertEqual(
                action_map["summary"]["clusters"],
                len(action_map["clusters"]),
            )
            self.assertTrue(
                all(cluster["claim_allowed"] is False for cluster in action_map["clusters"])
            )
            self.assertEqual(receipt["g3_state"], "REVIEW_REQUIRED")
            self.assertEqual(receipt["g4_state"], "BLOCKED_BY_G3")
            self.assertTrue(receipt["cluster_review_digest_sha256"])
            self.assertTrue(review["policy"]["cluster_is_not_equivalence"])
            self.assertTrue(review["policy"]["authority_binding_requires_g3_evidence"])
            self.assertTrue(
                all(
                    row["g3_semantic_split_gate"]["state"] == "REVIEW_REQUIRED"
                    and row["g4_authority_bind_gate"]["state"] == "BLOCKED_BY_G3"
                    and row["g4_authority_bind_gate"]["auto_create_gap_id"] is False
                    for row in review["clusters"]
                )
            )

    def test_cluster_digest_is_deterministic_for_same_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, action_map_a, receipt_a, review_a = self.run_service(root)
            _, action_map_b, receipt_b, review_b = self.run_service(root)
            self.assertEqual(action_map_a["clusters"], action_map_b["clusters"])
            self.assertEqual(
                receipt_a["cluster_digest_sha256"],
                receipt_b["cluster_digest_sha256"],
            )
            self.assertEqual(review_a, review_b)
            self.assertEqual(
                receipt_a["cluster_review_digest_sha256"],
                receipt_b["cluster_review_digest_sha256"],
            )

    def test_fail_on_unmapped_is_enforceable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proc, action_map, _, _ = self.run_service(root, fail_on="unmapped")
            self.assertGreater(action_map["summary"]["unmapped"], 0)
            self.assertEqual(proc.returncode, 1)


if __name__ == "__main__":
    unittest.main()
