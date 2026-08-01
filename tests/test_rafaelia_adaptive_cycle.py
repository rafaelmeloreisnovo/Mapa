from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_rafaelia_adaptive_cycle.py"
spec = importlib.util.spec_from_file_location("rafaelia_cycle", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class AdaptiveCycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract_path = ROOT / "data" / "control-plane" / "RAFAELIA_ADAPTIVE_CYCLE.v1.json"
        self.registry_path = ROOT / "data" / "formulas" / "RAFAELIA_FORMULA_REGISTRY.v1.json"
        self.contract = module.load_object(self.contract_path)
        self.registry = module.load_object(self.registry_path)

    def test_contract_is_fail_closed(self) -> None:
        module.validate_contract(self.contract)
        self.assertFalse(self.contract["claim_allowed"])
        self.assertFalse(self.contract["automatic_mutation"])
        self.assertFalse(self.contract["automatic_merge"])
        self.assertEqual(self.contract["source_mode"], "READ_ONLY")

    def test_registry_has_exactly_fifty_typed_formulas(self) -> None:
        module.validate_registry(self.registry)
        self.assertEqual([r["id"] for r in self.registry["records"]], list(range(1, 51)))
        self.assertEqual(self.registry["records"][21]["classification"], "CONFLICTING_DEFINITION")
        self.assertEqual(
            [r["id"] for r in self.registry["records"] if r["claim_state"] == "REFUTED_AS_WRITTEN"],
            [16, 33],
        )

    def test_fibonacci_variants_are_both_computed(self) -> None:
        pair = module.fibonacci_pair(self.contract, 7)
        self.assertNotEqual(pair["canonical_plus_sin"], pair["listed_minus_sin"])
        self.assertGreater(pair["absolute_divergence"], 0.0)
        self.assertFalse(pair["silent_selection"])

    def test_toroidal_vector_stays_in_domain(self) -> None:
        metrics = {"files": 42, "bytes": 1234567, "coverage": 1.0, "path_entropy_normalized": 0.5}
        state = module.smooth_state(self.contract, metrics)
        fib = module.fibonacci_pair(self.contract, 3)
        vector = module.toroidal_state(metrics, state, fib, 2)
        self.assertEqual(set(vector), {"u", "v", "psi", "chi", "rho", "delta", "sigma"})
        self.assertTrue(all(0.0 <= value < 1.0 for value in vector.values()))

    def test_execution_produces_hash_bound_read_only_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            for rel in ["README.md", "data/control-plane/x.json", "docs/a.md", "scripts/a.py", "tests/a.py"]:
                path = repo / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(rel + "\n", encoding="utf-8")
            out = Path(tmp) / "out"
            receipt = module.execute(
                repo,
                self.contract_path,
                self.registry_path,
                out,
                module.parse_timestamp("2026-08-01T18:07:00Z"),
            )
            self.assertEqual(receipt["decision"], "EXECUTED_READ_ONLY")
            self.assertFalse(receipt["claim_allowed"])
            self.assertEqual(receipt["repository"]["coverage"], 1.0)
            self.assertEqual(receipt["formula_evaluation"]["formula_count"], 50)
            self.assertTrue((out / "cycle_summary.md").is_file())
            stored = json.loads((out / "cycle_receipt.json").read_text(encoding="utf-8"))
            digest = stored.pop("receipt_sha256")
            self.assertEqual(digest, module.sha256_value(stored))

    def test_missing_formula_is_blocked(self) -> None:
        broken = json.loads(json.dumps(self.registry))
        broken["records"].pop()
        with self.assertRaises(module.CycleError):
            module.validate_registry(broken)

    def test_claim_promotion_is_rejected(self) -> None:
        broken = json.loads(json.dumps(self.contract))
        broken["claim_allowed"] = True
        with self.assertRaises(module.CycleError):
            module.validate_contract(broken)


if __name__ == "__main__":
    unittest.main()
