from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_live_control_plane import validate


SOURCE = Path(__file__).resolve().parents[1]


class LiveControlPlaneTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(SOURCE / "data", self.root / "data")
        (self.root / "auditoria").mkdir()
        for name in (
            "OPERATIONAL_WORKFLOW_CONTRACT_LOCAL_EVIDENCE_2026-07-24.json",
            "OPERATIONAL_TRIAGE_LOCAL_EVIDENCE_2026-07-25.json",
        ):
            (self.root / "auditoria" / name).write_text("{}\n", encoding="utf-8")
        (self.root / "orquestrador/fixtures").mkdir(parents=True)
        (self.root / "orquestrador/fixtures/procedure_ledger.valid.json").write_text("{}\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def read(self, name):
        path = self.root / f"data/control-plane/{name}"
        return path, json.loads(path.read_text(encoding="utf-8"))

    def write(self, path, data):
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_valid_baseline_passes(self):
        self.assertEqual(validate(self.root)["status"], "PASS")

    def test_unknown_evidence_is_rejected(self):
        path, data = self.read("module_registry.v1.json")
        data["modules"][0]["evidence_ids"].append("EVID-UNKNOWN")
        self.write(path, data)
        report = validate(self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("unknown evidence" in e for e in report["errors"]))

    def test_local_evidence_missing_is_blocking(self):
        (self.root / "auditoria/OPERATIONAL_TRIAGE_LOCAL_EVIDENCE_2026-07-25.json").unlink()
        report = validate(self.root)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("local evidence path missing" in e for e in report["errors"]))

    def test_cross_repo_file_requires_immutable_ref(self):
        path, data = self.read("evidence_pointer_registry.v1.json")
        item = next(x for x in data["pointers"] if x["evidence_id"] == "EVID-RAFMEDIA-CANONICAL")
        item["ref"] = "main"
        self.write(path, data)
        self.assertEqual(validate(self.root)["status"], "FAIL")

    def test_merge_remote_pass_is_rejected(self):
        path, data = self.read("merge_decisions.v1.json")
        data["decisions"][0]["remote_validation"] = "PASS"
        self.write(path, data)
        self.assertEqual(validate(self.root)["status"], "FAIL")

    def test_merge_claim_promotion_is_rejected(self):
        path, data = self.read("merge_decisions.v1.json")
        data["decisions"][1]["claim_promotion"] = True
        self.write(path, data)
        self.assertEqual(validate(self.root)["status"], "FAIL")

    def test_duplicate_module_is_rejected(self):
        path, data = self.read("module_registry.v1.json")
        data["modules"].append(copy.deepcopy(data["modules"][0]))
        self.write(path, data)
        self.assertEqual(validate(self.root)["status"], "FAIL")

    def test_unknown_product_producer_is_rejected(self):
        path, data = self.read("product_graph.v1.json")
        data["products"][0]["producer_modules"] = ["MOD-UNKNOWN"]
        self.write(path, data)
        self.assertEqual(validate(self.root)["status"], "FAIL")

    def test_verified_product_without_evidence_is_rejected(self):
        path, data = self.read("product_graph.v1.json")
        data["products"][0]["evidence_ids"] = []
        self.write(path, data)
        self.assertEqual(validate(self.root)["status"], "FAIL")

    def test_draft_product_requires_draft_producers(self):
        path, data = self.read("module_registry.v1.json")
        data["modules"][1]["state"] = "VERIFIED_LIMITED"
        self.write(path, data)
        self.assertEqual(validate(self.root)["status"], "FAIL")

    def test_live_registry_cannot_point_to_fixture(self):
        path, data = self.read("current_state_snapshot.v1.json")
        data["registries"]["modules"] = "orquestrador/fixtures/module_registry.valid.json"
        self.write(path, data)
        self.assertEqual(validate(self.root)["status"], "FAIL")

    def test_snapshot_count_drift_is_rejected(self):
        path, data = self.read("current_state_snapshot.v1.json")
        data["derived"]["module_count"] = 999
        self.write(path, data)
        self.assertEqual(validate(self.root)["status"], "FAIL")

    def test_semantic_interpretation_cannot_be_promoted(self):
        path, data = self.read("current_state_snapshot.v1.json")
        data["derived"]["semantic_interpretation_state"] = "VERIFIED"
        self.write(path, data)
        self.assertEqual(validate(self.root)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
