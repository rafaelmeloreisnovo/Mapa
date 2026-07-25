from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_operational_workflow import validate_workflow


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data/workflows/rafaelia-operational-workflow.v1.json"


class OperationalWorkflowContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = json.loads(CANONICAL.read_text(encoding="utf-8"))

    def defects(self, document=None, repo_root=None):
        defects, _ = validate_workflow(document or self.document, repo_root)
        return defects

    def stage(self, document, stage_id):
        return next(stage for stage in document["stages"] if stage["id"] == stage_id)

    def assert_has(self, defects, text):
        self.assertTrue(any(text in defect for defect in defects), defects)

    def test_canonical_workflow_passes_semantic_validation(self):
        self.assertEqual([], self.defects())

    def test_duplicate_stage_id_is_rejected(self):
        doc = copy.deepcopy(self.document)
        doc["stages"][1]["id"] = doc["stages"][0]["id"]
        self.assert_has(self.defects(doc), "duplicate stage id")

    def test_unknown_dependency_is_rejected(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "validate_source")["depends_on"] = ["missing_stage"]
        self.assert_has(self.defects(doc), "depends on unknown stage")

    def test_cycle_is_rejected(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "ingest_source")["depends_on"] = ["validate_source"]
        self.assert_has(self.defects(doc), "contains a cycle")

    def test_active_stage_cannot_be_token_vazio(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "validate_source")["epistemic_state"] = "TOKEN_VAZIO"
        self.assert_has(self.defects(doc), "active stage requires FATO or VERIFIED_LIMITED")

    def test_planned_stage_must_preserve_token_vazio(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "interpret_context")["epistemic_state"] = "FATO"
        self.assert_has(self.defects(doc), "planned stage requires epistemic_state=TOKEN_VAZIO")

    def test_planned_stage_cannot_allow_claim(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "interpret_context")["claim_allowed"] = True
        self.assert_has(self.defects(doc), "planned stage requires claim_allowed=false")

    def test_active_stage_requires_implementation_reference(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "validate_source")["implementation_refs"] = []
        self.assert_has(self.defects(doc), "active stage requires implementation_refs")

    def test_active_claim_requires_evidence_requirements(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "validate_source")["evidence_requirements"] = []
        defects = self.defects(doc)
        self.assert_has(defects, "evidence_requirements must not be empty")
        self.assert_has(defects, "claim_allowed=true requires evidence_requirements")

    def test_execute_and_publish_require_human_review(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "execute_operation")["human_review_required"] = False
        self.assert_has(self.defects(doc), "execute stage requires human_review_required=true")

    def test_active_stage_cannot_depend_on_planned_stage(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "epistemic_gate")["depends_on"] = ["interpret_context"]
        self.stage(doc, "epistemic_gate")["inputs"] = ["semantic_hypotheses"]
        self.assert_has(self.defects(doc), "must not depend on non-active stage")

    def test_input_requires_external_or_ancestor_output(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "validate_source")["inputs"] = ["unknown_input"]
        self.assert_has(self.defects(doc), "is not external and is not produced by an ancestor")

    def test_duplicate_output_is_rejected(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "validate_source")["outputs"] = ["intake_manifest"]
        self.assert_has(self.defects(doc), "is produced by both")

    def test_unconsumed_nonterminal_output_is_rejected(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "validate_source")["outputs"].append("orphan_output")
        self.assert_has(self.defects(doc), "is neither consumed nor terminal")

    def test_terminal_output_must_exist(self):
        doc = copy.deepcopy(self.document)
        doc["terminal_outputs"].append("missing_terminal")
        self.assert_has(self.defects(doc), "is not produced by any stage")

    def test_workflow_claim_requires_complete_active_chain(self):
        doc = copy.deepcopy(self.document)
        doc["claim_allowed"] = True
        self.assert_has(self.defects(doc), "requires every stage active")

    def test_unsafe_implementation_path_is_rejected(self):
        doc = copy.deepcopy(self.document)
        self.stage(doc, "validate_source")["implementation_refs"] = ["../escape.py"]
        self.assert_has(self.defects(doc), "contains unsafe path")

    def test_repo_root_verifies_active_implementation_refs(self):
        doc = {
            "schema_version": "rafaelia.operational-workflow/v1",
            "workflow_id": "wf:minimal-valid",
            "title": "Minimal",
            "owner": "tests",
            "objective": "Verify repository references.",
            "claim_allowed": True,
            "external_inputs": ["source"],
            "terminal_outputs": ["result"],
            "policy": {
                "immutable_sources": True,
                "token_vazio_is_valid": True,
                "human_review_for_execute_publish": True,
                "max_active_stage_timeout_seconds": 60
            },
            "stages": [{
                "id": "ingest_minimal",
                "symbolic_stage": None,
                "operational_name": "Minimal ingest",
                "phase": "ingest",
                "state": "active",
                "epistemic_state": "FATO",
                "claim_allowed": True,
                "executor": "script",
                "human_review_required": False,
                "depends_on": [],
                "inputs": ["source"],
                "transformation": "Read source.",
                "outputs": ["result"],
                "success_criteria": ["result exists"],
                "evidence_requirements": ["test"],
                "failure_modes": ["missing result"],
                "rollback": "Discard result.",
                "resource_limits": {"timeout_seconds": 30, "max_memory_mb": 32},
                "implementation_refs": ["scripts/worker.py"],
                "next_verifiable_step": "Run the worker test."
            }],
            "next_verifiable_step": "Run validation."
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "scripts/worker.py").write_text("pass\n", encoding="utf-8")
            self.assertEqual([], self.defects(doc, root))
            (root / "scripts/worker.py").unlink()
            self.assert_has(self.defects(doc, root), "missing active artifact")


if __name__ == "__main__":
    unittest.main()
