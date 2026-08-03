import copy
import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "tools" / "validate_igc_priority_delta.py"


def load_module():
    spec = importlib.util.spec_from_file_location("igc_priority_validator", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


V = load_module()


class IgcPriorityDeltaTests(unittest.TestCase):
    def setUp(self):
        self.paths = dict(V.DEFAULT_PATHS)

    def test_current_delta_passes(self):
        result = V.validate(self.paths)
        self.assertEqual(result["state"], "PASS")
        self.assertFalse(result["claim_allowed"])
        self.assertEqual(result["gaps"]["count"], 12)
        self.assertEqual(result["geometry"]["count"], 4)
        self.assertEqual(result["questions"]["count"], 15)
        self.assertEqual(result["memory"]["count"], 6)

    def _write_mutated_jsonl(self, source, mutate):
        records = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
        mutate(records)
        temp_dir = tempfile.TemporaryDirectory()
        target = pathlib.Path(temp_dir.name) / source.name
        target.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
        return temp_dir, target

    def test_claim_true_is_rejected(self):
        temp_dir, mutated = self._write_mutated_jsonl(
            self.paths["geometry"], lambda records: records[0].__setitem__("claim_allowed", True)
        )
        self.addCleanup(temp_dir.cleanup)
        paths = copy.copy(self.paths)
        paths["geometry"] = mutated
        with self.assertRaisesRegex(V.ValidationError, "claim_allowed must be false"):
            V.validate(paths)

    def test_missing_transformation_is_rejected(self):
        def mutate(records):
            records[0]["transformation_family"] = ""

        temp_dir, mutated = self._write_mutated_jsonl(self.paths["geometry"], mutate)
        self.addCleanup(temp_dir.cleanup)
        paths = copy.copy(self.paths)
        paths["geometry"] = mutated
        with self.assertRaisesRegex(V.ValidationError, "transformation_family is required"):
            V.validate(paths)

    def test_unknown_dependency_is_rejected(self):
        def mutate(records):
            records[0]["dependencies"] = ["IGC-GAP-999"]

        temp_dir, mutated = self._write_mutated_jsonl(self.paths["gaps"], mutate)
        self.addCleanup(temp_dir.cleanup)
        paths = copy.copy(self.paths)
        paths["gaps"] = mutated
        with self.assertRaisesRegex(V.ValidationError, "unknown dependency"):
            V.validate(paths)

    def test_p0_question_without_failure_state_is_rejected(self):
        def mutate(records):
            records[0]["failure_state"] = "UNKNOWN"

        temp_dir, mutated = self._write_mutated_jsonl(self.paths["questions"], mutate)
        self.addCleanup(temp_dir.cleanup)
        paths = copy.copy(self.paths)
        paths["questions"] = mutated
        with self.assertRaisesRegex(V.ValidationError, "failure_state must be"):
            V.validate(paths)


if __name__ == "__main__":
    unittest.main()
