#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_mhel_omega_bagua_manifold.py"
SPEC = importlib.util.spec_from_file_location("mhel_validator", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def valid_receipt() -> dict:
    return {
        "schema_version": "mhel-omega-manifold-receipt-v1",
        "receipt_id": "MHEL-OMEGA-V13-TEST-001",
        "source_hash": "a" * 64,
        "previous_event_hash": "GENESIS",
        "window_thirds": [
            {"role": "ORIGIN_INPUT", "start": 0, "middle": 1, "end": 2, "comprehension_state": "COMPREHENSIBLE"},
            {"role": "TRANSFORM_MIDDLE", "start": 3, "middle": 4, "end": 5, "comprehension_state": "PARTIAL"},
            {"role": "RECEIPT_OUTPUT", "start": 6, "middle": 7, "end": 8, "comprehension_state": "COMPREHENSIBLE"},
        ],
        "material_group": "MATHEMATICS_GEOMETRY",
        "trigram_state": {"id": "LI", "bits": "101"},
        "hexagram_state": {"bits": "101010", "lower_trigram": "101", "upper_trigram": "010"},
        "manifold_coordinates": {
            "source": "fixture",
            "syntax": "binary-lines",
            "semantics": "test-only",
            "dynamics": "one-line-change",
            "evidence": "unit-test",
            "uncertainty": 0.2,
            "time": "t0",
            "scale": 1,
        },
        "yin_yang_pair": {
            "pole_a": 0,
            "pole_b": 1,
            "center": 0.5,
            "mode": "EXACT_EQUIDISTANCE",
            "epsilon": 0,
        },
        "five_phase_transition": {"from": "WOOD", "to": "FIRE", "reason": "fixture"},
        "alpha_k": {
            "initial_radius": 2.0,
            "delta_demand": 4.0,
            "delta_radius": 2.0,
            "value": 0.25,
            "state": "MEASURED",
        },
        "epistemic_state": "TOKEN_VAZIO_QUANTIFICADO",
        "dmaic_stage": "MEASURE",
        "sample_statistics": {
            "n": 120,
            "n_effective": 80.0,
            "design_effect": 1.5,
            "margin_of_error": 0.03,
            "confidence_level": 0.95,
            "ground_truth_available": False,
            "limitations": ["fixture only"],
        },
        "process_capability": {
            "stable_process": True,
            "defects": 1,
            "units": 100,
            "opportunities_per_unit": 10,
            "dpo": 0.001,
            "dpmo": 1000.0,
            "mean": 5.0,
            "sample_stddev": 1.0,
            "lsl": 0.0,
            "usl": 10.0,
            "cp": 10.0 / 6.0,
            "cpk": 5.0 / 3.0,
        },
        "token_vazio": [
            {
                "id": "TV-BASELINE-001",
                "missing_information": "real baseline",
                "uncertainty": 0.8,
                "validation_probability": None,
                "closure_cost": None,
                "required_test": "execute measured pilot",
            }
        ],
        "next_test": "execute measured pilot",
        "forbidden_promotions": ["BAGUA_TO_PHYSICAL_PROOF"],
        "claim_allowed": False,
    }


class ValidatorTests(unittest.TestCase):
    def test_valid_receipt_passes(self) -> None:
        self.assertEqual(MODULE.validate(valid_receipt()), [])

    def test_trigram_mismatch_fails(self) -> None:
        receipt = valid_receipt()
        receipt["trigram_state"]["bits"] = "111"
        errors = MODULE.validate(receipt)
        self.assertTrue(any("trigram bits mismatch" in error for error in errors))

    def test_same_n_effective_contract_is_enforced(self) -> None:
        receipt = valid_receipt()
        receipt["sample_statistics"]["n_effective"] = 120.0
        errors = MODULE.validate(receipt)
        self.assertTrue(any("n_effective must equal" in error for error in errors))

    def test_alpha_k_is_recomputed(self) -> None:
        receipt = valid_receipt()
        receipt["alpha_k"]["value"] = 9.0
        errors = MODULE.validate(receipt)
        self.assertTrue(any("alpha_k.value mismatch" in error for error in errors))

    def test_claim_cannot_be_promoted(self) -> None:
        receipt = valid_receipt()
        receipt["claim_allowed"] = True
        errors = MODULE.validate(receipt)
        self.assertTrue(any("claim_allowed must remain false" in error for error in errors))

    def test_capability_requires_stability(self) -> None:
        receipt = valid_receipt()
        receipt["process_capability"]["stable_process"] = False
        errors = MODULE.validate(receipt)
        self.assertTrue(any("stable_process=true" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
