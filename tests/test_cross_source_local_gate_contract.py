#!/usr/bin/env python3
"""Static safety tests for the offline cross-source gate entry point."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_cross_source_gate.sh"
TEST_RUNNER = ROOT / "scripts" / "run_cross_source_tests.py"
COMPARATOR = ROOT / "scripts" / "compare_cross_source_evidence.py"
FLOOR = ROOT / "indices" / "CROSS_SOURCE_GATE_FLOOR.json"


class CrossSourceLocalGateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SCRIPT.read_text(encoding="utf-8")
        cls.runner_text = TEST_RUNNER.read_text(encoding="utf-8")
        cls.comparator_text = COMPARATOR.read_text(encoding="utf-8")
        cls.floor = json.loads(FLOOR.read_text(encoding="utf-8"))

    def test_script_is_explicitly_offline_and_posix(self) -> None:
        self.assertTrue(self.text.startswith("#!/usr/bin/env sh\n"))
        self.assertIn("set -eu", self.text)
        self.assertIn("Offline, dependency-free", self.text)

    def test_script_has_no_network_or_repository_mutation_commands(self) -> None:
        forbidden = (
            "curl ",
            "wget ",
            "git push",
            "git commit",
            "git reset",
            "gh ",
            "rm -rf",
            "sudo ",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, self.text)

    def test_script_runs_validators_measured_tests_and_floor_evaluator(self) -> None:
        required = (
            "scripts/validate_cross_source_records.py",
            "scripts/validate_cross_source_registry.py",
            "scripts/validate_chain_of_custody.py",
            "scripts/run_cross_source_tests.py",
            "scripts/evaluate_cross_source_gate.py",
            "scripts/compare_cross_source_evidence.py",
            "tests/test_cross_source_records.py",
            "tests/test_cross_source_registry.py",
            "tests/test_cross_source_gate_evaluator.py",
            "tests/test_cross_source_test_runner.py",
            "tests/test_compare_cross_source_evidence.py",
            "tests/test_validate_chain_of_custody.py",
        )
        for path in required:
            with self.subTest(path=path):
                self.assertIn(path, self.text)

    def test_test_runner_discovers_future_governed_tests(self) -> None:
        self.assertIn("TEST_PATTERNS", self.runner_text)
        self.assertIn('"test_cross_source*.py"', self.runner_text)
        self.assertIn('"test_compare_cross_source_evidence.py"', self.runner_text)
        self.assertIn("glob(pattern)", self.runner_text)
        self.assertIn('"test_file_count": len(TEST_FILES)', self.runner_text)
        self.assertIn('"tests_discovered": tests_discovered', self.runner_text)
        self.assertIn('"complete_execution": complete_execution', self.runner_text)
        self.assertIn('"clean_outcomes": clean_outcomes', self.runner_text)
        self.assertIn("skipped == 0", self.runner_text)
        self.assertIn("expected_failures == 0", self.runner_text)
        self.assertIn("unexpected_successes == 0", self.runner_text)

    def test_comparator_verifies_reports_checksums_and_floor(self) -> None:
        self.assertIn("REPORT_NAMES", self.comparator_text)
        self.assertIn("CHECKSUMS.sha256", self.comparator_text)
        self.assertIn("checksum mismatch", self.comparator_text)
        self.assertIn("quality floor sha256 differs or is absent", self.comparator_text)
        self.assertIn("manifest observed test count differs", self.comparator_text)
        self.assertIn("manifest quality_floor.sha256 differs from floor file", self.comparator_text)
        self.assertIn('"clean_test_outcomes"', self.comparator_text)
        self.assertIn('"claim_allowed": False', self.comparator_text)
        self.assertIn('"remote_ci_substituted": False', self.comparator_text)

    def test_script_seals_five_reports_with_sha256(self) -> None:
        self.assertIn("hashlib.sha256", self.text)
        self.assertIn("cross-source-test-validation.json", self.text)
        self.assertIn("chain-of-custody-validation.json", self.text)
        self.assertIn("quality-floor-validation.json", self.text)
        self.assertIn("CHECKSUMS.sha256", self.text)
        self.assertIn("LOCAL_GATE_STATUS.json", self.text)

    def test_script_preserves_claim_and_remote_ci_boundaries(self) -> None:
        self.assertIn('"claim_allowed": False', self.text)
        self.assertIn('"remote_ci_substituted": False', self.text)
        self.assertIn("LOCAL_PASS_REMOTE_TOKEN_VAZIO", self.text)
        self.assertIn("compare_cross_source_evidence.py", self.text)

    def test_gate_measures_tests_instead_of_declaring_fixed_count(self) -> None:
        minimums = self.floor["minimums"]
        invariants = self.floor["invariants"]
        self.assertEqual(self.floor["schema_version"], "rafaelia.cross-source-gate-floor/v2")
        self.assertEqual(minimums["test_files"], 7)
        self.assertEqual(minimums["tests_discovered"], 58)
        self.assertEqual(minimums["tests_run"], 58)
        self.assertTrue(invariants["complete_execution"])
        self.assertTrue(invariants["clean_outcomes"])
        self.assertEqual(invariants["skipped"], 0)
        self.assertEqual(invariants["expected_failures"], 0)
        self.assertEqual(invariants["unexpected_successes"], 0)
        self.assertIn('"test_count_discovered": tests["tests_discovered"]', self.text)
        self.assertIn('"test_count_observed": tests["tests_run"]', self.text)
        self.assertIn('"minimum_test_file_count": floor["minimums"]["test_files"]', self.text)
        self.assertIn('"clean_test_outcomes": tests["clean_outcomes"]', self.text)
        self.assertIn('tests["tests_discovered"] >= minimums["tests_discovered"]', self.text)
        self.assertIn('tests["tests_run"] >= minimums["tests_run"]', self.text)
        self.assertIn('tests["tests_run"] == tests["tests_discovered"]', self.text)
        self.assertIn('tests["complete_execution"] is True', self.text)
        self.assertIn('tests["clean_outcomes"] is True', self.text)
        self.assertIn('tests["skipped"] == 0', self.text)
        self.assertNotIn('"test_count_expected": 38', self.text)

    def test_gate_allows_append_only_growth_without_freezing_registry(self) -> None:
        self.assertTrue(FLOOR.is_file())
        self.assertIn('registry["record_count"] >= minimums["registry_records"]', self.text)
        self.assertNotIn('registry["record_count"] == 10', self.text)
        self.assertNotIn(
            'registry["provider_counts"] == {"github": 2, "google_drive": 8}',
            self.text,
        )

    def test_pycache_is_redirected_to_untracked_output(self) -> None:
        self.assertIn("PYTHONPYCACHEPREFIX", self.text)
        self.assertIn('.artifacts/cross-source-local', self.text)


if __name__ == "__main__":
    unittest.main()
