from __future__ import annotations

import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "governance" / "validate_operational_excellence_gate.py"
CONTRACT = ROOT / "data" / "contracts" / "operational-excellence-gate.v1.json"
VALID = ROOT / "tests" / "fixtures" / "operational-excellence.receipt.valid.json"
INVALID = ROOT / "tests" / "fixtures" / "operational-excellence.receipt.invalid-authority.json"


class OperationalExcellenceCliTests(unittest.TestCase):
    def run_validator(self, receipt: pathlib.Path):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--contract", str(CONTRACT), "--receipt", str(receipt)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_receipt_exit_zero(self):
        result = self.run_validator(VALID)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_unresolved_authority_is_nonzero(self):
        result = self.run_validator(INVALID)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("AUTHORITY unresolved", result.stderr)


if __name__ == "__main__":
    unittest.main()
