import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_novoexport_full_recount_successor",
    ROOT / "tools" / "validate_novoexport_full_recount_successor.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
DATA = json.loads(
    (ROOT / "data/evidence/novoexport_full_recount_successor_20260907.v1.json").read_text(
        encoding="utf-8"
    )
)


class NovoexportFullRecountSuccessorTests(unittest.TestCase):
    def test_canonical_successor_passes(self):
        self.assertEqual([], MODULE.validate(copy.deepcopy(DATA)))

    def test_dataset_cannot_become_mission_authority(self):
        data = copy.deepcopy(DATA)
        data["authority"]["dataset_is_mission_authority"] = True
        self.assertIn("authority_boundary", MODULE.validate(data))

    def test_training_or_weight_update_cannot_be_promoted(self):
        for key in ("training_executed", "weight_update_executed"):
            data = copy.deepcopy(DATA)
            data["authority"][key] = True
            self.assertIn("authority_boundary", MODULE.validate(data))

    def test_structural_cardinality_cannot_promote_semantic_exhaustivity(self):
        data = copy.deepcopy(DATA)
        data["semantic_ingest"]["semantic_exhaustivity_proven"] = True
        self.assertIn("semantic_exhaustivity_proven_must_be_false", MODULE.validate(data))

    def test_provider_origin_must_remain_token_vazio_without_direct_evidence(self):
        data = copy.deepcopy(DATA)
        data["structural_reuse"]["provider_origin_state"] = "BRANCHING"
        self.assertIn("provider_origin_must_remain_token_vazio", MODULE.validate(data))

    def test_pending_rafgittools_binding_cannot_invent_merge_commit(self):
        data = copy.deepcopy(DATA)
        data["rafgittools_binding"]["merge_commit"] = "a" * 40
        self.assertIn("pending_binding_must_not_have_merge_commit", MODULE.validate(data))

    def test_merged_binding_requires_exact_commit(self):
        data = copy.deepcopy(DATA)
        data["rafgittools_binding"]["state"] = "MERGED_VALIDATED"
        data["rafgittools_binding"]["merge_commit"] = "TOKEN_VAZIO"
        self.assertIn("merged_binding_requires_merge_commit", MODULE.validate(data))

    def test_duplicate_metric_regression_is_rejected(self):
        data = copy.deepcopy(DATA)
        data["source_scope"]["distinct_duplicated_effective_message_ids"] = 5197
        self.assertIn(
            "source_scope.distinct_duplicated_effective_message_ids",
            MODULE.validate(data),
        )

    def test_semantic_gaps_cannot_disappear(self):
        data = copy.deepcopy(DATA)
        data["semantic_ingest"]["open_gaps"] = []
        self.assertIn("semantic_open_gaps", MODULE.validate(data))


if __name__ == "__main__":
    unittest.main()
