from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "conversation_indexer", ROOT / "scripts" / "index_conversations_export.py"
)
assert SPEC and SPEC.loader
indexer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = indexer
SPEC.loader.exec_module(indexer)


def fixture() -> list[dict]:
    return [
        {
            "id": "conv-secret-1",
            "title": "TÍTULO ULTRASSECRETO",
            "create_time": 1.0,
            "update_time": 2.0,
            "mapping": {
                "n1": {
                    "id": "n1",
                    "parent": None,
                    "children": ["n2"],
                    "message": {
                        "id": "m1",
                        "author": {"role": "user"},
                        "create_time": 1.1,
                        "content": {
                            "content_type": "text",
                            "parts": ["SEGREDO NÃO PODE SAIR Ω"],
                        },
                    },
                },
                "n2": {
                    "id": "n2",
                    "parent": "n1",
                    "children": [],
                    "message": {
                        "id": "m2",
                        "author": {"role": "assistant"},
                        "create_time": 1.2,
                        "content": {"content_type": "text", "parts": ["resposta"]},
                    },
                },
            },
        },
        {
            "id": "conv-2",
            "title": "segunda",
            "create_time": 3.0,
            "update_time": 4.0,
            "mapping": {},
        },
    ]


class ConversationCustodyTests(unittest.TestCase):
    def test_valid_export_indexes_without_private_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "conversations.json"
            source.write_text(json.dumps(fixture(), ensure_ascii=False), encoding="utf-8")
            out = root / "out"
            receipt = indexer.run([source], out, source_id="TEST")
            self.assertEqual(receipt["state"], "INDEXED_PRIVACY_PRESERVING")
            self.assertEqual(receipt["conversation_count"], 2)
            self.assertEqual(receipt["message_count"], 2)
            corpus = b"".join(path.read_bytes() for path in out.iterdir() if path.is_file())
            self.assertNotIn("TÍTULO ULTRASSECRETO".encode(), corpus)
            self.assertNotIn("SEGREDO NÃO PODE SAIR".encode(), corpus)

    def test_arbitrary_byte_splits_reassemble_including_utf8_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            payload = json.dumps(fixture(), ensure_ascii=False).encode("utf-8")
            omega = payload.index("Ω".encode("utf-8"))
            cuts = [omega + 1, len(payload) // 2]
            cuts = sorted(set(cuts))
            chunks = [payload[: cuts[0]], payload[cuts[0] : cuts[1]], payload[cuts[1] :]]
            parts = []
            for index, chunk in enumerate(chunks, start=1):
                path = root / f"part-{index:02d}.bin"
                path.write_bytes(chunk)
                parts.append(path)
            receipt = indexer.run(parts, root / "out", source_id="SPLIT")
            self.assertEqual(receipt["state"], "INDEXED_PRIVACY_PRESERVING")
            self.assertEqual(receipt["conversation_count"], 2)

    def test_middle_fragment_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "fragment.json"
            source.write_bytes(b'"title":"middle fragment"}')
            out = root / "out"
            receipt = indexer.run([source], out, source_id="FRAGMENT")
            self.assertEqual(receipt["state"], "TOKEN_VAZIO_REASSEMBLY_REQUIRED")
            self.assertFalse((out / "conversations.index.jsonl").exists())
            self.assertFalse((out / "messages.index.jsonl").exists())
            self.assertTrue((out / "source.manifest.json").exists())

    def test_outputs_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "conversations.json"
            source.write_text(json.dumps(fixture(), ensure_ascii=False), encoding="utf-8")
            out_a, out_b = root / "a", root / "b"
            indexer.run([source], out_a, source_id="DETERMINISTIC")
            indexer.run([source], out_b, source_id="DETERMINISTIC")
            names_a = sorted(path.name for path in out_a.iterdir())
            names_b = sorted(path.name for path in out_b.iterdir())
            self.assertEqual(names_a, names_b)
            for name in names_a:
                self.assertEqual((out_a / name).read_bytes(), (out_b / name).read_bytes())

    def test_claim_gate_and_raw_flags_remain_false(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "conversations.json"
            source.write_text(json.dumps(fixture(), ensure_ascii=False), encoding="utf-8")
            out = root / "out"
            indexer.run([source], out, source_id="GATE")
            manifest = json.loads((out / "source.manifest.json").read_text())
            self.assertFalse(manifest["claim_allowed"])
            self.assertFalse(manifest["privacy"]["raw_titles_in_index"])
            self.assertFalse(manifest["privacy"]["raw_message_bodies_in_index"])


if __name__ == "__main__":
    unittest.main()
