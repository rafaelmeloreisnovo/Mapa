from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/validate_custody_gap_closure_v1.py"
MODEL = ROOT / "data/governance/custody/06_GAPS/CUSTODY_GAP_CLOSURE_MODEL_V1.json"

spec = importlib.util.spec_from_file_location("custody_gap_validator", SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CustodyGapClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(MODEL.read_text(encoding="utf-8"))

    def test_canonical_model_passes(self) -> None:
        self.assertEqual(module.validate(self.data), [])

    def test_external_provider_gap_cannot_be_locally_promoted(self) -> None:
        data = copy.deepcopy(self.data)
        gap = next(g for g in data["gaps"] if g["gap_id"] == "CUST-20260927-003")
        gap["state"] = "PASS"
        errors = module.validate(data)
        self.assertTrue(any("external-authority gap must remain ROUTE_STATE_BLOCKED" in e for e in errors))

    def test_historical_nonexecution_cannot_be_retroactively_promoted(self) -> None:
        data = copy.deepcopy(self.data)
        gap = next(g for g in data["gaps"] if g["gap_id"] == "CUST-20260927-007")
        gap["state"] = "PASS"
        errors = module.validate(data)
        self.assertIn("historical non-execution must remain NOT_RUN", errors)

    def test_dependency_must_resolve_to_known_gap(self) -> None:
        data = copy.deepcopy(self.data)
        gap = next(g for g in data["gaps"] if g["gap_id"] == "CUST-20260927-004")
        gap["depends_on"] = ["UNKNOWN-GAP"]
        errors = module.validate(data)
        self.assertTrue(any("unknown dependency UNKNOWN-GAP" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
