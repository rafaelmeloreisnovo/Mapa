import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "build_json_identity_commitments.py"
spec = importlib.util.spec_from_file_location("json_identity", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class JsonIdentityCommitmentsV1Tests(unittest.TestCase):
    def run_index(self, root: Path, source_id: str = "TEST-SOURCE") -> dict:
        out = root / "out"
        receipt = mod.run([root / "src"], out, source_id=source_id)
        manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
        return {"receipt": receipt, "manifest": manifest, "out": out}

    def test_deterministic_same_inputs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"
            src.mkdir()
            (src / "a.json").write_text('[{"x":1},{"x":2}]', encoding="utf-8")
            first = self.run_index(root)
            first_records = (first["out"] / "records.index.jsonl").read_bytes()
            first_manifest = first["manifest"]
            (root / "out").rename(root / "out-first")
            second = self.run_index(root)
            self.assertEqual(first_manifest, second["manifest"])
            self.assertEqual(first_records, (second["out"] / "records.index.jsonl").read_bytes())

    def test_same_content_different_occurrence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"
            src.mkdir()
            (src / "a.json").write_text('{"x":1}', encoding="utf-8")
            (src / "b.json").write_text('{"x":1}', encoding="utf-8")
            result = self.run_index(root)
            rows = [json.loads(line) for line in
                    (result["out"] / "records.index.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(rows[0]["record_content_id"], rows[1]["record_content_id"])
            self.assertNotEqual(rows[0]["record_occurrence_id"], rows[1]["record_occurrence_id"])

    def test_reorder_changes_order_commitments(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"
            src.mkdir()
            p = src / "a.json"
            p.write_text('[{"x":1},{"x":2}]', encoding="utf-8")
            first = self.run_index(root)["manifest"]
            (root / "out").rename(root / "out-first")
            p.write_text('[{"x":2},{"x":1}]', encoding="utf-8")
            second = self.run_index(root)["manifest"]
            self.assertNotEqual(first["corpus_merkle_root_sha256"], second["corpus_merkle_root_sha256"])
            self.assertNotEqual(first["corpus_terminal_chain_sha256"], second["corpus_terminal_chain_sha256"])

    def test_exact_bytes_and_canonical_content_are_distinct_identities(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"
            src.mkdir()
            p = src / "a.json"
            p.write_text('{"b":2, "a":1}\n', encoding="utf-8")
            first = self.run_index(root)
            file1 = json.loads((first["out"] / "files.index.jsonl").read_text(encoding="utf-8"))
            rec1 = json.loads((first["out"] / "records.index.jsonl").read_text(encoding="utf-8"))
            (root / "out").rename(root / "out-first")
            p.write_text('{"a":1,"b":2}', encoding="utf-8")
            second = self.run_index(root)
            file2 = json.loads((second["out"] / "files.index.jsonl").read_text(encoding="utf-8"))
            rec2 = json.loads((second["out"] / "records.index.jsonl").read_text(encoding="utf-8"))
            self.assertNotEqual(file1["file_content_id"], file2["file_content_id"])
            self.assertEqual(rec1["record_content_id"], rec2["record_content_id"])

    def test_invalid_json_fails_closed_without_committed_indexes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"
            src.mkdir()
            (src / "bad.json").write_text('{"x":', encoding="utf-8")
            out = root / "out"
            with self.assertRaises(mod.IndexErrorV1):
                mod.run([src], out, source_id="TEST")
            self.assertFalse((out / "records.index.jsonl").exists())
            self.assertFalse((out / "manifest.json").exists())

    def test_non_empty_output_is_refused(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"
            src.mkdir()
            (src / "a.json").write_text('{"x":1}', encoding="utf-8")
            out = root / "out"
            out.mkdir()
            (out / "old.txt").write_text("keep", encoding="utf-8")
            with self.assertRaises(mod.IndexErrorV1):
                mod.run([src], out, source_id="TEST")


if __name__ == "__main__":
    unittest.main()
