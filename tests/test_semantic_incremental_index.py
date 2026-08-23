import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "semantic_incremental_index.py"
spec = importlib.util.spec_from_file_location("semantic_incremental_index", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)


class IncrementalIndexerTests(unittest.TestCase):
    def write_node(self, root: Path, inc_id: str, subject: str = "x") -> None:
        (root / f"{inc_id}.yaml").write_text(
            f'id: {inc_id}\nsubject: "{subject}"\nsemantic_type: TEST\nstate: DRAFT\ncreated_at: "2026-08-22T00:00:00-03:00"\n',
            encoding="utf-8",
        )

    def test_single_seed_yields_next_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_node(root, "INC-000001")
            index = mod.build_index(root)
            self.assertEqual(index["sequence"]["sequence_state"], "PASS")
            self.assertEqual(index["sequence"]["next_candidate"], "INC-000002")

    def test_gap_returns_token_vazio_and_no_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_node(root, "INC-000001")
            self.write_node(root, "INC-000003")
            index = mod.build_index(root)
            self.assertEqual(index["sequence"]["sequence_state"], "TOKEN_VAZIO_INCREMENTAL_SEQUENCE")
            self.assertIsNone(index["sequence"]["next_candidate"])
            self.assertEqual(index["sequence"]["missing"], ["INC-000002"])

    def test_filename_id_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "INC-000001.yaml").write_text("id: INC-000002\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "filename/id mismatch"):
                mod.build_index(root)


if __name__ == "__main__":
    unittest.main()
