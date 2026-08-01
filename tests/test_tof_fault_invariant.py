from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_tof_fault_invariant.py"
RECORD = ROOT / "data" / "control-plane" / "tof-namespace-allocation-fault.v1.json"

spec = importlib.util.spec_from_file_location("tof_validator", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TofFaultInvariantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_canonical_empty_file_record_passes(self) -> None:
        report = module.validate(self.record)
        self.assertEqual(report["status"], "PASS")
        self.assertFalse(report["claim_allowed"])
        self.assertEqual(report["logical_extents"], 0)

    def test_empty_file_cannot_have_extent(self) -> None:
        invalid = copy.deepcopy(self.record)
        invalid["allocation"]["logical_extents"] = [
            {
                "logical_offset": 0,
                "length": 1,
                "physical_location": "device0:block1",
                "state": "ALLOCATED",
            }
        ]
        with self.assertRaises(module.ValidationError):
            module.validate(invalid)

    def test_token_vazio_cannot_promote_claim(self) -> None:
        invalid = copy.deepcopy(self.record)
        invalid["claim_allowed"] = True
        with self.assertRaises(module.ValidationError):
            module.validate(invalid)

    def test_absent_is_not_empty_file(self) -> None:
        invalid = copy.deepcopy(self.record)
        invalid["object_state_model"]["semantic_state"] = "ABSENT"
        with self.assertRaises(module.ValidationError):
            module.validate(invalid)

    def test_fault_event_ids_are_unique(self) -> None:
        invalid = copy.deepcopy(self.record)
        invalid["fault_overlay"]["events"].append(
            copy.deepcopy(invalid["fault_overlay"]["events"][0])
        )
        with self.assertRaises(module.ValidationError):
            module.validate(invalid)


if __name__ == "__main__":
    unittest.main()
