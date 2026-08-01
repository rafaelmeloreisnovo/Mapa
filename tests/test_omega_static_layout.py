#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "omega_validator", ROOT / "scripts" / "validate_omega_static_layout.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
ValidationError = MODULE.ValidationError
validate = MODULE.validate


def valid_record() -> dict:
    return json.loads(
        (ROOT / "data" / "control-plane" / "omega-static-address-relocation.v1.json")
        .read_text(encoding="utf-8")
    )


class OmegaStaticLayoutTests(unittest.TestCase):
    def test_canonical_record_passes(self) -> None:
        report = validate(valid_record())
        self.assertEqual(report["status"], "PASS")
        self.assertFalse(report["claim_allowed"])

    def test_overlap_is_rejected(self) -> None:
        record = valid_record()
        record["regions"][1]["offset"] = 256
        with self.assertRaisesRegex(ValidationError, "overlap"):
            validate(record)

    def test_system_attribute_cannot_be_pinning(self) -> None:
        record = valid_record()
        record["semantic_guards"]["system_attribute_is_pinning"] = True
        with self.assertRaisesRegex(ValidationError, "ATTR.SYSTEM"):
            validate(record)

    def test_fixed_offset_cannot_be_physical_claim(self) -> None:
        record = valid_record()
        record["semantic_guards"]["fixed_offset_is_fixed_physical"] = True
        with self.assertRaisesRegex(ValidationError, "FIXED_OFFSET"):
            validate(record)

    def test_physical_fixed_requires_evidence(self) -> None:
        record = valid_record()
        record["regions"][0]["mobility"] = "PHYSICAL_FIXED"
        with self.assertRaisesRegex(ValidationError, "physical_space"):
            validate(record)

    def test_fixed_virtual_requires_android_runtime(self) -> None:
        record = valid_record()
        record["address_model"]["base_policy"] = "FIXED_VIRTUAL"
        with self.assertRaisesRegex(ValidationError, "Android"):
            validate(record)

    def test_empty_region_with_payload_is_rejected(self) -> None:
        record = valid_record()
        record["regions"][2]["size"] = 64
        with self.assertRaisesRegex(ValidationError, "EMPTY exige size=0"):
            validate(record)

    def test_claim_promotion_is_rejected(self) -> None:
        record = valid_record()
        record["claim_allowed"] = True
        with self.assertRaisesRegex(ValidationError, "claim_allowed"):
            validate(record)

    def test_absolute_pointer_rule_cannot_be_weakened(self) -> None:
        record = valid_record()
        record["reuse_contract"]["absolute_pointer"] = "SAME_MANIFEST_SIGNATURE"
        with self.assertRaisesRegex(ValidationError, "ponteiro absoluto"):
            validate(record)

    def test_duplicate_source_is_rejected(self) -> None:
        record = valid_record()
        record["sources"].append(copy.deepcopy(record["sources"][0]))
        with self.assertRaisesRegex(ValidationError, "fonte duplicada"):
            validate(record)


if __name__ == "__main__":
    unittest.main()
