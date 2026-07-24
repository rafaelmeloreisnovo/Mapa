#!/usr/bin/env python3
"""Tests for deterministic discovery of the governed cross-source suite."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "run_cross_source_tests.py"
SPEC = importlib.util.spec_from_file_location("cross_source_test_runner", MODULE_PATH)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class CrossSourceTestRunnerTests(unittest.TestCase):
    def test_discovery_is_sorted_unique_and_nonempty(self) -> None:
        discovered = runner.discover_test_files()
        self.assertTrue(discovered)
        self.assertEqual(discovered, tuple(sorted(set(discovered))))

    def test_discovery_includes_comparator_and_runner_contract(self) -> None:
        discovered = set(runner.discover_test_files())
        self.assertIn("tests/test_compare_cross_source_evidence.py", discovered)
        self.assertIn("tests/test_cross_source_test_runner.py", discovered)
        self.assertIn("tests/test_validate_chain_of_custody.py", discovered)

    def test_discovery_never_escapes_tests_directory(self) -> None:
        for relative_path in runner.discover_test_files():
            path = Path(relative_path)
            self.assertEqual(path.parts[0], "tests")
            self.assertNotIn("..", path.parts)
            self.assertTrue((ROOT / path).is_file())


if __name__ == "__main__":
    unittest.main()
