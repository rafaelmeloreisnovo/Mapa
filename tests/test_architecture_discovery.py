import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/discover_architecture_families.py"
FIXTURE = ROOT / "tests/fixtures/architecture_discovery/novoexport_sample.json"


class ArchitectureDiscoveryTests(unittest.TestCase):
    def run_scan(self, out: Path):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE), "--output-dir", str(out), "--fail-on-parse-error"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def load_jsonl(self, path: Path):
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_pipeline_discovers_known_and_token_vazio_terms_without_raw_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            result = self.run_scan(out)
            self.assertEqual(result.returncode, 0, result.stderr)

            candidates = self.load_jsonl(out / "architecture_candidates.jsonl")
            canonicals = {row["canonical"] for row in candidates}
            architecture_ids = {row["architecture_id"] for row in candidates if row["architecture_id"]}
            states = {row["canonical"]: row["state"] for row in candidates}

            for expected in {"ARCH-FCEA", "ARCH-ZETA", "ARCH-V79-1", "ARCH-HCPM", "ARCH-MITM-LAYER", "ARCH-NEXUS", "ARCH-EXACORDEX"}:
                self.assertIn(expected, architecture_ids)
            for expected in {"Iara", "Raia", "Infinity", "HiperCognicao", "CMD", "Beta", "Gama", "Teta", "Penta", "Supreme"}:
                self.assertIn(expected, canonicals)
                self.assertTrue(states[expected].startswith("TOKEN_VAZIO"))

            all_outputs = "\n".join(path.read_text(encoding="utf-8") for path in out.iterdir() if path.is_file())
            self.assertNotIn("SENTINEL_PRIVATE_TEXT_7429", all_outputs)
            self.assertNotIn(str(FIXTURE.resolve()), all_outputs)

    def test_cooccurrence_is_observation_not_causation(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            result = self.run_scan(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            relations = self.load_jsonl(out / "architecture_relations.jsonl")
            fcea_hcpm = [row for row in relations if {row["left"], row["right"]} == {"FCEA", "HCPM"}]
            self.assertTrue(fcea_hcpm)
            self.assertEqual(fcea_hcpm[0]["state"], "OBSERVED_COOCCURRENCE_NOT_CAUSATION")
            self.assertFalse(fcea_hcpm[0]["claim_allowed"])

    def test_receipt_hashes_outputs_and_run_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            out1 = Path(tmp) / "out1"
            out2 = Path(tmp) / "out2"
            first = self.run_scan(out1)
            second = self.run_scan(out2)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)

            receipt1 = json.loads((out1 / "architecture_receipt.json").read_text(encoding="utf-8"))
            receipt2 = json.loads((out2 / "architecture_receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt1["run_id"], receipt2["run_id"])
            self.assertFalse(receipt1["claim_allowed"])
            self.assertFalse(receipt1["semantic_exhaustiveness_claim"])

            for name, expected_hash in receipt1["outputs"].items():
                observed = hashlib.sha256((out1 / name).read_bytes()).hexdigest()
                self.assertEqual(observed, expected_hash)


if __name__ == "__main__":
    unittest.main()
