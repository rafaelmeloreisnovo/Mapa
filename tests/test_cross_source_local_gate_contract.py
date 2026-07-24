#!/usr/bin/env python3
"""Static safety tests for the offline cross-source gate entry point."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_cross_source_gate.sh"


class CrossSourceLocalGateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SCRIPT.read_text(encoding="utf-8")

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

    def test_script_runs_both_semantic_validators(self) -> None:
        self.assertIn("scripts/validate_cross_source_records.py", self.text)
        self.assertIn("scripts/validate_cross_source_registry.py", self.text)
        self.assertIn("tests/test_cross_source_records.py", self.text)
        self.assertIn("tests/test_cross_source_registry.py", self.text)

    def test_script_seals_reports_with_sha256(self) -> None:
        self.assertIn("hashlib.sha256", self.text)
        self.assertIn("CHECKSUMS.sha256", self.text)
        self.assertIn("LOCAL_GATE_STATUS.json", self.text)

    def test_script_preserves_claim_and_remote_ci_boundaries(self) -> None:
        self.assertIn('"claim_allowed": False', self.text)
        self.assertIn('"remote_ci_substituted": False', self.text)
        self.assertIn("Restore GitHub Actions runner startup", self.text)

    def test_default_output_is_untracked_artifact_directory(self) -> None:
        self.assertIn('.artifacts/cross-source-local', self.text)


if __name__ == "__main__":
    unittest.main()
