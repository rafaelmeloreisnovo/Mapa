from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "scripts"))

from run_g006_local_gate import (
    LocalGateError,
    NEXT_GATE,
    build_command_plan,
    build_receipt,
    canonical_digest,
    sha256_file,
    validate_report_bundle,
)


class G006LocalGateTests(unittest.TestCase):
    def _write(self, root: Path, name: str, payload: dict):
        (root / name).write_text(json.dumps(payload), encoding="utf-8")

    def _valid_reports(self, root: Path):
        self._write(
            root,
            "claim-vocabulary-validation.json",
            {
                "status": "PASS",
                "explicit_claim_error_count": 0,
                "portfolio_exit_criteria_met": False,
                "claim_allowed": False,
            },
        )
        self._write(
            root,
            "claim-contradiction-ledger-validation.json",
            {
                "status": "PASS",
                "candidate_count": 36,
                "reviewed_safe_count": 6,
                "token_vazio_count": 30,
            },
        )
        self._write(
            root,
            "claim-review-chain-validation.json",
            {
                "status": "PASS",
                "review_batch_count": 3,
                "review_decision_count": 30,
                "reviewed_safe_count": 36,
                "reviewed_blocking_count": 0,
                "token_vazio_count": 0,
                "review_completion_ratio": 1.0,
                "exact_absence_resolution_count": 1,
                "next_gate": NEXT_GATE,
                "claim_allowed": False,
            },
        )
        self._write(
            root,
            "claim-review-residual-validation.json",
            {
                "status": "PASS",
                "historical_residual_count": 1,
                "current_residual_count": 0,
                "full_content_observed": True,
                "decoded_size_bytes": 19542,
                "exact_strong_token_count": 0,
                "false_positive_source": "completeness_ratio",
                "claim_allowed": False,
            },
        )
        self._write(
            root,
            "claim-discovery-precision-validation.json",
            {
                "status": "PASS",
                "known_resolution": {
                    "entry_id": "CC028",
                    "substring_complete_count": 1,
                    "exact_complete_count": 0,
                },
                "claim_allowed": False,
            },
        )

    def test_command_plan_is_shell_free_and_complete(self):
        plan = build_command_plan(ROOT, Path("/tmp/g006"))
        self.assertEqual(len(plan), 7)
        self.assertEqual(plan[0]["name"], "py_compile")
        self.assertEqual(plan[1]["name"], "unittest")
        self.assertTrue(all(isinstance(item["argv"], list) for item in plan))
        self.assertTrue(all(item["argv"][0] == sys.executable for item in plan))

    def test_valid_report_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._valid_reports(root)
            result = validate_report_bundle(root)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["reviewed_safe_count"], 36)
            self.assertEqual(result["current_residual_count"], 0)
            self.assertFalse(result["claim_allowed"])

    def test_token_vazio_reappearance_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._valid_reports(root)
            path = root / "claim-review-chain-validation.json"
            data = json.loads(path.read_text())
            data["token_vazio_count"] = 1
            path.write_text(json.dumps(data))
            with self.assertRaises(LocalGateError):
                validate_report_bundle(root)

    def test_exact_token_regression_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._valid_reports(root)
            path = root / "claim-review-residual-validation.json"
            data = json.loads(path.read_text())
            data["exact_strong_token_count"] = 1
            path.write_text(json.dumps(data))
            with self.assertRaises(LocalGateError):
                validate_report_bundle(root)

    def test_receipt_is_fail_closed(self):
        receipt = build_receipt(
            root=ROOT,
            output_dir=Path("/tmp/g006"),
            git={"head_commit": "0" * 40},
            commands=[],
            bundle=None,
            checksums={},
            started_at="2026-07-21T00:00:00+00:00",
            finished_at="2026-07-21T00:00:01+00:00",
            status="FAIL",
            error="test",
        )
        self.assertEqual(receipt["status"], "FAIL")
        self.assertFalse(receipt["boundaries"]["remote_runner_receipt"])
        self.assertFalse(receipt["boundaries"]["portfolio_exit_criteria_met"])
        self.assertFalse(receipt["boundaries"]["claim_allowed"])
        self.assertEqual(receipt["integrity"]["digest"], canonical_digest(receipt))

    def test_sha256_file_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "file"
            path.write_bytes(b"abc")
            self.assertEqual(
                sha256_file(path),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )


if __name__ == "__main__":
    unittest.main()
