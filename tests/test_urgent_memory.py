#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_urgent_memory import validate


DATA = Path("data/memory/urgent-memory.public.v1.jsonl")


class UrgentMemoryTests(unittest.TestCase):
    def test_public_queue_passes(self) -> None:
        errors, summary = validate(DATA)
        self.assertEqual([], errors)
        self.assertEqual("PASS", summary["status"])
        self.assertGreaterEqual(summary["nodes"], 1)

    def test_unresolved_claim_true_fails_closed(self) -> None:
        rows = DATA.read_text(encoding="utf-8").splitlines()
        node = json.loads(rows[0])
        node["claim_allowed"] = True
        node["state"] = "OPEN"
        rows[0] = json.dumps(node, ensure_ascii=False)

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bad.jsonl"
            path.write_text("\n".join(rows) + "\n", encoding="utf-8")
            errors, summary = validate(path)

        self.assertEqual("FAIL", summary["status"])
        self.assertTrue(any("claim_allowed=true" in e for e in errors))

    def test_private_drive_url_is_rejected(self) -> None:
        rows = DATA.read_text(encoding="utf-8").splitlines()
        node = json.loads(rows[1])
        node["provenance"][0]["locator"] = "https://docs.google.com/document/d/private-id"
        rows[1] = json.dumps(node, ensure_ascii=False)

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bad.jsonl"
            path.write_text("\n".join(rows) + "\n", encoding="utf-8")
            errors, summary = validate(path)

        self.assertEqual("FAIL", summary["status"])
        self.assertTrue(any("private Drive URLs" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
