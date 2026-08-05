import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/core/operational-core-94.v1.json"
VALIDATOR = ROOT / "scripts/validate_operational_core_94.py"


class OperationalCore94Tests(unittest.TestCase):
    def run_validator(self, path: Path):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(path)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_canonical_registry_passes(self):
        result = self.run_validator(REGISTRY)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["identified_count"], 16)
        self.assertEqual(payload["unitemized_count"], 78)
        self.assertFalse(payload["claim_allowed"])

    def test_duplicate_id_fails_closed(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        data["items"][1]["id"] = data["items"][0]["id"]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_validator(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate item id", result.stdout + result.stderr)

    def test_claim_promotion_fails_closed(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        data["items"][0]["claim_allowed"] = True
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_validator(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("promoted claim", result.stdout + result.stderr)

    def test_count_mismatch_fails_closed(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        data["unitemized_count"] = 77
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_validator(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not close", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
