from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "data" / "omega7-relational-amplifier.v1.json"
VALIDATOR_PATH = ROOT / "tools" / "validate_omega7_relational_amplifier.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("omega7_validator", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_validator()


class Omega7RelationalAmplifierTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def test_valid_contract_is_fail_closed(self):
        report = VALIDATOR.validate(self.contract)
        self.assertEqual(report["status"], "PASS_LIMITED_SCHEMA_AND_CONTRACT")
        self.assertEqual(report["addressable_cells"], 2401)
        self.assertEqual(report["materialized_cells"], 0)

    def test_axis_duplication_is_rejected(self):
        invalid = copy.deepcopy(self.contract)
        invalid["axes"]["direction"][6] = invalid["axes"]["direction"][0]
        with self.assertRaises(VALIDATOR.ContractError):
            VALIDATOR.validate(invalid)

    def test_claim_promotion_is_rejected(self):
        invalid = copy.deepcopy(self.contract)
        invalid["claim_allowed"] = True
        with self.assertRaises(VALIDATOR.ContractError):
            VALIDATOR.validate(invalid)

    def test_wrong_coordinate_count_is_rejected(self):
        invalid = copy.deepcopy(self.contract)
        invalid["coordinate_space"]["addressable_cells"] = 2400
        with self.assertRaises(VALIDATOR.ContractError):
            VALIDATOR.validate(invalid)

    def test_causality_is_fail_closed(self):
        invalid = copy.deepcopy(self.contract)
        invalid["relation_policy"]["causality"]["default_state"] = "CAUSAL"
        with self.assertRaises(VALIDATOR.ContractError):
            VALIDATOR.validate(invalid)

    def test_unproven_semantic_edge_is_rejected(self):
        invalid = copy.deepcopy(self.contract)
        invalid["relation_policy"]["sparsity"]["semantic_edges_materialized"] = 1
        with self.assertRaises(VALIDATOR.ContractError):
            VALIDATOR.validate(invalid)


if __name__ == "__main__":
    unittest.main()
