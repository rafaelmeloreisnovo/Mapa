import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/validate_novoexport_active_v2_source_universe.py"
SPEC = importlib.util.spec_from_file_location("validator", SCRIPT)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MOD)
DATA = ROOT / "data/evidence/novoexport_active_v2_source_universe_20260907.v1.json"

class ActiveV2SourceUniverseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(DATA.read_text(encoding="utf-8"))

    def test_canonical_passes(self):
        self.assertEqual([], MOD.validate(self.payload))

    def test_rejects_semantic_false_promotion(self):
        d = copy.deepcopy(self.payload)
        d["semantic_ingest"]["semantic_exhaustivity_proven"] = True
        self.assertIn("semantic_exhaustivity_proven_must_be_false", MOD.validate(d))

    def test_rejects_missing_physical_entry(self):
        d = copy.deepcopy(self.payload)
        d["physical_universe"]["category_counts"]["dat"] -= 1
        self.assertIn("category_sum", MOD.validate(d))

    def test_not_found_route_cannot_infer_replacement(self):
        d = copy.deepcopy(self.payload)
        d["route_drift"][0]["replacement"] = "invented-provider-id"
        self.assertIn("not_found_replacement_inferred", MOD.validate(d))

if __name__ == "__main__":
    unittest.main()
