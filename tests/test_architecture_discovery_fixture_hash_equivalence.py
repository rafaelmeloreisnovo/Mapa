import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/discover_architecture_families.py"
FIXTURE = ROOT / "tests/fixtures/architecture_discovery/novoexport_sample.json"
RULES = ROOT / "data/ontology/architectures/ARCHITECTURE_DISCOVERY_RULES_V1.json"

EXPECTED = {
    "architecture_candidates.jsonl": "867e0cd4e0cc5d133c6702b5f171c743ff40086d0923dc0fba1a8365b4ebbf71",
    "architecture_relations.jsonl": "a5d85c0dddc248ede8c585b533f681dd1d33b4c86d15710a1a9017d8e19e2f9c",
    "architecture_summary.json": "3af03376b7decd6f6052b2efc632d87231e4cf69d0e459360ae718f07185b829",
    "architecture_receipt.json": "d922d242eaba3573be05c214b618032093c8b0ee4853ffa8d93e2fbf7458940d",
}


class ArchitectureDiscoveryFixtureHashEquivalence(unittest.TestCase):
    def test_canonical_scanner_matches_bounded_reproduction_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(FIXTURE),
                    "--rules",
                    str(RULES),
                    "--output-dir",
                    str(out),
                    "--fail-on-parse-error",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            for name, expected in EXPECTED.items():
                observed = hashlib.sha256((out / name).read_bytes()).hexdigest()
                self.assertEqual(observed, expected, name)


if __name__ == "__main__":
    unittest.main()
