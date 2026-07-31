#!/usr/bin/env python3
"""Standard-library contract tests for the Termux Foundation runner."""
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "rafaelia_foundation.py"
SPEC = importlib.util.spec_from_file_location("rafaelia_foundation", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
FOUNDATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FOUNDATION)


class RafaeliaFoundationTests(unittest.TestCase):
    def test_example_manifest_is_valid(self) -> None:
        manifest = json.loads((ROOT / "templates" / "foundation.example.yaml").read_text(encoding="utf-8"))
        FOUNDATION.validate_manifest(manifest)

    def test_claim_promotion_is_rejected(self) -> None:
        manifest = json.loads((ROOT / "templates" / "foundation.example.yaml").read_text(encoding="utf-8"))
        manifest["governance"]["claim_allowed"] = True
        with self.assertRaises(FOUNDATION.FoundationError):
            FOUNDATION.validate_manifest(manifest)

    def test_path_escape_is_rejected(self) -> None:
        with self.assertRaises(FOUNDATION.FoundationError):
            FOUNDATION.relative_path("../outside.c", "inputs.source")

    def test_init_verify_and_run_python_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "project"
            repo.mkdir()
            (repo / "README.md").write_text("# test\n", encoding="utf-8")
            (repo / "sample.py").write_text("value = 42\n", encoding="utf-8")

            FOUNDATION.initialize(repo, "sample-project", "python", "sample.py")

            verify_code = FOUNDATION.run_operation(repo, "verify", "python")
            self.assertEqual(verify_code, 0)
            run_code = FOUNDATION.run_operation(repo, "run", "python")
            self.assertEqual(run_code, 0)

            receipts = sorted((repo / "COMPILA").glob("*/receipt.json"))
            self.assertGreaterEqual(len(receipts), 2)
            latest = json.loads(receipts[-1].read_text(encoding="utf-8"))
            self.assertEqual(latest["status"], "PASS_LOCAL_EXECUTION")
            self.assertFalse(latest["claim_allowed"])
            self.assertEqual(latest["commands_executed"], 1)
            self.assertTrue((receipts[-1].parent / "source.pyc").is_file())

    def test_init_is_non_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "project"
            repo.mkdir()
            (repo / "README.md").write_text("# test\n", encoding="utf-8")
            FOUNDATION.initialize(repo, "docs-project", "documentation", None)
            with self.assertRaises(FOUNDATION.FoundationError):
                FOUNDATION.initialize(repo, "docs-project", "documentation", None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
