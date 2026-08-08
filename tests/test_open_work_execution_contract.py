from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools/validate_open_work_execution_contract.py"
CONTRACT = ROOT / "data/gaps/open_work_execution_contract.20260808.v1.json"

spec = importlib.util.spec_from_file_location("open_work_validator", VALIDATOR)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class OpenWorkExecutionContractTests(unittest.TestCase):
    def load(self):
        return json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_canonical_contract_passes(self):
        result = module.validate(CONTRACT)
        self.assertEqual(result["state"], "PASS")
        self.assertEqual(result["tokens"], 14)
        self.assertEqual(result["in_flight_pass_draft"], 2)

    def test_no_open_token_is_anonymous(self):
        data = self.load()
        for row in data["items"]:
            self.assertTrue(row["authority_required"].strip())
            self.assertTrue(row["minimal_evidence"].strip())
            self.assertTrue(row["promotion_condition"].strip())
            self.assertTrue(row["falsifier"].strip())
            self.assertTrue(row["next_producer"].strip())

    def test_external_and_human_authorities_are_not_internalized(self):
        data = self.load()
        for row in data["items"]:
            if row["authority_state"] in {"OPEN_EXTERNAL", "OPEN_HUMAN"}:
                self.assertNotEqual(row["execution_state"], "IN_FLIGHT_PASS_DRAFT")

    def test_draft_pass_does_not_mutate_authoritative_open_state(self):
        data = self.load()
        rows = {row["token"]: row for row in data["items"]}
        act = rows["TOKEN_VAZIO_ACT_DR6_CMBONLY_MATERIALIZATION_REPRODUCTION"]
        rd = rows["TOKEN_VAZIO_H0_RD_FULL_BOLTZMANN_REPRODUCTION"]
        self.assertEqual(act["authority_state"], "OPEN_INTERNAL")
        self.assertEqual(act["execution_state"], "IN_FLIGHT_PASS_DRAFT")
        self.assertEqual(rd["authority_state"], "OPEN_MIXED")
        self.assertEqual(rd["execution_state"], "IN_FLIGHT_PASS_DRAFT")

    def test_critical_scientific_dependencies_are_explicit(self):
        data = self.load()
        rows = {row["token"]: row for row in data["items"]}
        impl = rows["TOKEN_VAZIO_RLL_CLASS_CAMB_IMPLEMENTATION"]
        self.assertEqual(impl["dependencies"], ["TOKEN_VAZIO_RLL_PERTURBATION_CLOSURE_RELATIONS"])
        joint = rows["TOKEN_VAZIO_REAL_BAYES_JOINT_MULTI_PROBE"]
        self.assertIn("TOKEN_VAZIO_DESI_DR2_OFFICIAL_JOINT_CROSSBLOCK_REPRODUCTION", joint["dependencies"])
        self.assertIn("TOKEN_VAZIO_DES_Y6_3X2PT_LIKELIHOOD", joint["dependencies"])


if __name__ == "__main__":
    unittest.main()
