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
    def run_scan(self, out: Path, private_review: Path | None = None):
        command = [
            sys.executable,
            str(SCRIPT),
            str(FIXTURE),
            "--output-dir",
            str(out),
            "--fail-on-parse-error",
        ]
        if private_review is not None:
            command.extend(["--private-review-output", str(private_review)])
        return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)

    def load_jsonl(self, path: Path):
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_pipeline_discovers_known_and_token_vazio_terms_without_raw_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            result = self.run_scan(out)
            self.assertEqual(result.returncode, 0, result.stderr)

            candidates = self.load_jsonl(out / "architecture_candidates.jsonl")
            canonicals = {row["canonical"] for row in candidates if row["canonical"]}
            architecture_ids = {row["architecture_id"] for row in candidates if row["architecture_id"]}
            states = {row["canonical"]: row["state"] for row in candidates if row["canonical"]}

            for expected in {"ARCH-FCEA", "ARCH-ZETA", "ARCH-V79-1", "ARCH-HCPM", "ARCH-MITM-LAYER", "ARCH-NEXUS", "ARCH-EXACORDEX"}:
                self.assertIn(expected, architecture_ids)
            for expected in {"Iara", "Raia", "Infinity", "HiperCognicao", "CMD", "Beta", "Gama", "Teta", "Penta", "Supreme"}:
                self.assertIn(expected, canonicals)
                self.assertTrue(states[expected].startswith("TOKEN_VAZIO"))

            all_outputs = "\n".join(path.read_text(encoding="utf-8") for path in out.iterdir() if path.is_file())
            self.assertNotIn("SENTINEL_PRIVATE_TEXT_7429", all_outputs)
            self.assertNotIn("Nebula", all_outputs)
            self.assertNotIn(str(FIXTURE.resolve()), all_outputs)

    def test_unspoken_structural_context_becomes_token_vazio_orphan(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            result = self.run_scan(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            candidates = self.load_jsonl(out / "architecture_candidates.jsonl")
            orphans = [row for row in candidates if row["rule_id"] == "STRUCTURAL_ORPHAN"]
            self.assertTrue(orphans)
            self.assertTrue(all(row["canonical"] is None for row in orphans))
            self.assertTrue(all(row["state"] == "TOKEN_VAZIO_UNRESOLVED_STRUCTURE" for row in orphans))
            summary = json.loads((out / "architecture_summary.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(summary["structural_orphan_count"], 1)

    def test_ambiguous_version_and_name_tokens_are_disambiguated(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            result = self.run_scan(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            candidates = self.load_jsonl(out / "architecture_candidates.jsonl")
            counts = {}
            for row in candidates:
                if row["canonical"]:
                    counts[row["canonical"]] = counts.get(row["canonical"], 0) + 1
            self.assertEqual(counts.get("V79", 0), 0, "V79.1 must not be downgraded into generic V79")
            self.assertEqual(counts.get("V79-1", 0), 1)
            self.assertEqual(counts.get("RA-IA", 0), 1, "Raia must not be interpreted as RA-IA")
            self.assertGreaterEqual(counts.get("Raia", 0), 1)

    def test_cooccurrence_is_observation_not_causation_at_string_and_record_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            result = self.run_scan(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            relations = self.load_jsonl(out / "architecture_relations.jsonl")
            fcea_hcpm = [row for row in relations if {row["left"], row["right"]} == {"FCEA", "HCPM"}]
            self.assertTrue(fcea_hcpm)
            self.assertEqual({row["scope"] for row in fcea_hcpm}, {"SAME_STRING", "SAME_RECORD"})
            self.assertTrue(all(row["state"] == "OBSERVED_COOCCURRENCE_NOT_CAUSATION" for row in fcea_hcpm))
            self.assertTrue(all(row["dependency_claim"] is False for row in fcea_hcpm))
            self.assertTrue(all(row["claim_allowed"] is False for row in fcea_hcpm))

    def test_private_review_is_explicit_local_only_and_not_in_public_receipt_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            private_review = Path(tmp) / "private-review.jsonl"
            result = self.run_scan(out, private_review)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(private_review.is_file())
            private_text = private_review.read_text(encoding="utf-8")
            self.assertIn("PRIVATE_LOCAL_ONLY_DO_NOT_COMMIT", private_text)
            self.assertIn("Nebula", private_text)
            receipt = json.loads((out / "architecture_receipt.json").read_text(encoding="utf-8"))
            self.assertTrue(receipt["private_review"]["emitted"])
            self.assertFalse(receipt["private_review"]["path_emitted_in_receipt"])
            self.assertNotIn(str(private_review), json.dumps(receipt))

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
