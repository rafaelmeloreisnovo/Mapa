import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_gap_closure_delta_v1.py"
DELTA = ROOT / "data" / "gap-atlas" / "RAFAELIA_GAP_CLOSURE_DELTA_20260812_V1.json"

spec = importlib.util.spec_from_file_location("gap_validator", VALIDATOR)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class GapClosureDeltaTest(unittest.TestCase):
    def load(self):
        return json.loads(DELTA.read_text(encoding="utf-8"))

    def run_tmp(self, data):
        with tempfile.TemporaryDirectory() as td:
            p = pathlib.Path(td) / "delta.json"
            p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            mod.main(p)

    def test_canonical_delta_passes(self):
        mod.main(DELTA)

    def test_duplicate_node_id_fails_closed(self):
        d = self.load()
        d["nodes"][1]["id"] = d["nodes"][0]["id"]
        with self.assertRaises(SystemExit):
            self.run_tmp(d)

    def test_missing_next_gate_fails_closed(self):
        d = self.load()
        d["nodes"][0]["next_gate"] = ""
        with self.assertRaises(SystemExit):
            self.run_tmp(d)

    def test_claim_promotion_fails_closed(self):
        d = self.load()
        d["claim_allowed"] = True
        with self.assertRaises(SystemExit):
            self.run_tmp(d)

    def test_physical_gap_requires_gated_or_partial_state(self):
        d = self.load()
        target = next(n for n in d["nodes"] if n["id"] == "RAFGITTOOLS_CONTROL_PLANE")
        target["state"] = "VERIFIED"
        with self.assertRaises(SystemExit):
            self.run_tmp(d)

if __name__ == "__main__":
    unittest.main()
