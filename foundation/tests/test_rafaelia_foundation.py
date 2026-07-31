#!/usr/bin/env python3
"""Standard-library contract tests for the Termux Foundation runner."""
from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "rafaelia_foundation.py"
SPEC = importlib.util.spec_from_file_location("rafaelia_foundation", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
FOUNDATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FOUNDATION)
GATE_PATH = ROOT / "scripts" / "gate_computational_v1.py"
GATE_SPEC = importlib.util.spec_from_file_location("gate_computational_v1", GATE_PATH)
assert GATE_SPEC is not None and GATE_SPEC.loader is not None
GATE = importlib.util.module_from_spec(GATE_SPEC)
GATE_SPEC.loader.exec_module(GATE)


class RafaeliaFoundationTests(unittest.TestCase):
    def test_example_manifest_is_valid(self) -> None:
        manifest = json.loads((ROOT / "templates" / "foundation.example.yaml").read_text(encoding="utf-8"))
        FOUNDATION.validate_manifest(manifest)

    def test_test_summary_schema_is_valid_json(self) -> None:
        schema = json.loads((ROOT / "schemas" / "rafaelia-test-summary.v1.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["$id"], "https://rafaelia.local/schemas/rafaelia-test-summary.v1.schema.json")
        self.assertEqual(schema["properties"]["schema"]["const"], "rafaelia.test-summary/v1")

    def test_claim_promotion_is_rejected(self) -> None:
        manifest = json.loads((ROOT / "templates" / "foundation.example.yaml").read_text(encoding="utf-8"))
        manifest["governance"]["claim_allowed"] = True
        with self.assertRaises(FOUNDATION.FoundationError):
            FOUNDATION.validate_manifest(manifest)

    def test_path_escape_is_rejected(self) -> None:
        with self.assertRaises(FOUNDATION.FoundationError):
            FOUNDATION.relative_path("../outside.c", "inputs.source")

    def test_shell_profile_is_rejected(self) -> None:
        manifest = json.loads((ROOT / "templates" / "foundation.example.yaml").read_text(encoding="utf-8"))
        manifest["profiles"]["freestanding-object"]["commands"] = [["sh", "-c", "echo unsafe"]]
        with self.assertRaises(FOUNDATION.FoundationError):
            FOUNDATION.validate_manifest(manifest)

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

    def test_generated_autoexec_routes_to_copied_runner(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "project"
            repo.mkdir()
            (repo / "README.md").write_text("# test\n", encoding="utf-8")
            FOUNDATION.initialize(repo, "autoexec-project", "documentation", None)

            completed = subprocess.run(
                ["bash", str(repo / "termux" / "autoexec-rafaelia.sh"), "run", "documentation"],
                cwd=repo,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("STATUS=PASS_STRUCTURE_ONLY", completed.stdout)

    @unittest.skipUnless(shutil.which("git"), "Git is required to prove commit-bound receipt semantics.")
    def test_computational_gate_requires_bound_complete_test_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "project"
            repo.mkdir()
            (repo / "README.md").write_text("# gate test\n", encoding="utf-8")
            (repo / "emit_summary.py").write_text(
                "from pathlib import Path\n"
                "import json\n"
                "import sys\n"
                "summary = {\n"
                "  'schema': 'rafaelia.test-summary/v1',\n"
                "  'counts': {'discovered': 2, 'executed': 2, 'passed': 2, 'failed': 0, 'skipped': 0},\n"
                "  'tests': [\n"
                "    {'id': 'compile-contract', 'result': 'PASS'},\n"
                "    {'id': 'negative-input', 'result': 'PASS'},\n"
                "  ],\n"
                "  'falsifiers': [\n"
                "    {'id': 'invalid-source', 'condition': 'invalid source must fail', 'status': 'EXERCISED'},\n"
                "  ],\n"
                "}\n"
                "Path(sys.argv[1]).write_text(json.dumps(summary), encoding='utf-8')\n",
                encoding="utf-8",
            )
            FOUNDATION.initialize(repo, "gate-project", "documentation", None)
            manifest_path = repo / ".rafaelia" / "foundation.yaml"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["inputs"]["required_paths"].append("emit_summary.py")
            manifest["profiles"]["local-tests"] = {
                "mode": "COMMANDS",
                "requires_source": False,
                "required_paths": ["README.md", "emit_summary.py"],
                "commands": [["python3", "emit_summary.py", "{{OUT}}/test-summary.json"]],
                "description": "Emit a deterministic test accounting artifact for the gate fixture.",
            }
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            for command in (
                ["git", "init"],
                ["git", "config", "user.email", "foundation@example.invalid"],
                ["git", "config", "user.name", "Foundation Test"],
                ["git", "add", "."],
                ["git", "commit", "-m", "fixture"],
            ):
                completed = subprocess.run(command, cwd=repo, check=False, capture_output=True, text=True)
                self.assertEqual(completed.returncode, 0, completed.stderr)

            run_code = FOUNDATION.run_operation(repo, "run", "local-tests")
            self.assertEqual(run_code, 0)
            receipt_path = next((repo / "COMPILA").glob("*/receipt.json"))
            report = GATE.review(
                repo,
                receipt_path,
                receipt_path.with_name("test-summary.json"),
                "local-tests",
            )
            self.assertEqual(report["COMPUTATIONAL_REVIEW_RESULT"], "READY_FOR_DOMAIN_SPECIFIC_REVIEW")
            self.assertFalse(report["claim_allowed"])

            gate_run = subprocess.run(
                [
                    "python3",
                    str(GATE_PATH),
                    "--repo-root",
                    str(repo),
                    "--receipt",
                    receipt_path.relative_to(repo).as_posix(),
                    "--test-summary",
                    receipt_path.with_name("test-summary.json").relative_to(repo).as_posix(),
                    "--expected-profile",
                    "local-tests",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(gate_run.returncode, 0, gate_run.stderr)
            self.assertIn("COMPUTATIONAL_REVIEW_RESULT=READY_FOR_DOMAIN_SPECIFIC_REVIEW", gate_run.stdout)
            self.assertTrue(list(receipt_path.parent.glob("gate.computational.v1-*.json")))

            summary_path = receipt_path.with_name("test-summary.json")
            summary_path.write_text("{}\n", encoding="utf-8")
            tampered = GATE.review(repo, receipt_path, summary_path, "local-tests")
            self.assertEqual(tampered["COMPUTATIONAL_REVIEW_RESULT"], "FAIL")
            self.assertIn("RECEIPT_ARTIFACT_HASH_MISMATCH", tampered["failures"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
