import unittest
from pathlib import Path

from tools.resolve_manifold_gap import load_gaps, resolve
from tools.validate_manifold_gap_registry import validate

ROOT = Path(__file__).resolve().parents[1]
GAPS = ROOT / "data/manifold/gaps_omega_v1.jsonl"

class ManifoldGapRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = validate(GAPS)
        cls.by_id = {row["gap_id"]: row for row in cls.rows}

    def test_seed_count_and_unique_ids(self):
        self.assertEqual(len(self.rows), 12)
        self.assertEqual(len(self.by_id), 12)

    def test_gap_of_gap_is_explicit(self):
        self.assertEqual(self.by_id["G0002"]["child_gap_refs"], ["G0011"])
        self.assertEqual(self.by_id["G0011"]["parent_gap_id"], "G0002")
        self.assertEqual(self.by_id["G0011"]["state"], "TOKEN_VAZIO_NESTED")

    def test_known_gap_is_navigable_without_becoming_filled(self):
        out = resolve("G0002", self.rows)
        self.assertEqual(out["status"], "GAP_NAVIGABLE")
        self.assertEqual(out["state"], "TOKEN_VAZIO_NOT_RUN")
        self.assertEqual(out["catalog_reduction"]["before"], "NP_CATALOG")
        self.assertEqual(out["catalog_reduction"]["after"], "P_CATALOG")
        self.assertFalse(out["catalog_reduction"]["complexity_claim"])
        self.assertFalse(out["claim_allowed"])

    def test_nested_gap_depth(self):
        out = resolve("G0011", self.rows)
        self.assertEqual(out["depth"], 1)
        self.assertEqual(out["path_to_root"], ["G0002"])
        self.assertEqual(out["state"], "TOKEN_VAZIO_NESTED")

    def test_unknown_gap_stays_open(self):
        out = resolve("G9999", self.rows)
        self.assertEqual(out["status"], "TOKEN_VAZIO_GAP_NOT_FOUND")
        self.assertEqual(out["catalog_reduction"]["after"], "NP_CATALOG")
        self.assertFalse(out["claim_allowed"])

    def test_symbolic_envelope_is_preserved_not_interpreted(self):
        out = resolve("G0012", self.rows)
        self.assertIn("⟨‡«†{★[ =SER=AO≈DE≠]★}»⟩¡¿?", out["markers"])
        self.assertEqual(out["kind"], "SYMBOLIC_SEMANTICS_UNBOUND")
        self.assertIsNone(out["noise"]["delta_section_noise"])

if __name__ == "__main__":
    unittest.main()
