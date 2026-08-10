#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "tools" / "rafaelia_specialized_ledger_adapter.py"


class SpecializedLedgerAdapterTests(unittest.TestCase):
    def run_adapter(self, mode: str, content: str, suffix: str = ".txt", extra: list[str] | None = None):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / f"input{suffix}"
            out = Path(td) / "out.json"
            src.write_text(content, encoding="utf-8")
            cmd = [
                sys.executable,
                str(ADAPTER),
                "--mode", mode,
                "--input", str(src),
                "--source", "fixture/source",
                "--output", str(out),
            ]
            if extra:
                cmd.extend(extra)
            proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
            payload = json.loads(out.read_text(encoding="utf-8")) if out.exists() else None
            return proc, payload

    def test_rll_json_emits_open_and_skips_terminal(self):
        content = json.dumps({
            "records": [
                {"id":"A","state":"TOKEN_VAZIO","priority":"P1","domain":"growth","unknowns":["x"],"next_gate":"measure"},
                {"id":"B","state":"RESOLVED","priority":"P2","domain":"done","unknowns":[],"next_gate":"none"}
            ]
        })
        proc, payload = self.run_adapter("rll-json", content, ".json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(payload["candidate_count"], 1)
        self.assertEqual(payload["candidates"][0]["native_id"], "A")
        self.assertFalse(payload["claim_allowed"])

    def test_token_kv_only_extracts_token_void_entries(self):
        content = "TOKEN_VAZIO_ALPHA=missing source\nNORMAL_KEY=ok\nTOKEN_VAZIO_BETA=not measured\n"
        proc, payload = self.run_adapter("token-kv", content)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(payload["candidate_count"], 2)
        self.assertEqual({c["native_id"] for c in payload["candidates"]}, {"TOKEN_VAZIO_ALPHA", "TOKEN_VAZIO_BETA"})

    def test_markdown_states_extracts_explicit_markers(self):
        content = "| component | TOKEN_VAZIO | absent |\nplain text\nrelease = BLOCKED\n"
        proc, payload = self.run_adapter("markdown-states", content)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(payload["candidate_count"], 2)
        markers = {m for c in payload["candidates"] for m in c["source_state_markers"]}
        self.assertIn("TOKEN_VAZIO", markers)
        self.assertIn("BLOCKED", markers)

    def test_fail_on_empty_is_nonzero_but_receipt_exists(self):
        proc, payload = self.run_adapter("markdown-states", "all green text\n", extra=["--fail-on-empty"])
        self.assertEqual(proc.returncode, 1)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["candidate_count"], 0)
        self.assertFalse(payload["claim_allowed"])


if __name__ == "__main__":
    unittest.main()
