#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "zipraf_v2_validator",
    ROOT / "scripts" / "validate_zipraf_static_layout_runtime_v2.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
ValidationError = MODULE.ValidationError
validate = MODULE.validate


def valid_record() -> dict:
    return json.loads(
        (ROOT / "data" / "evidence" / "zipraf-static-layout-runtime.v2.json")
        .read_text(encoding="utf-8")
    )


class ZiprafStaticLayoutRuntimeV2Tests(unittest.TestCase):
    def test_canonical_receipt_passes(self) -> None:
        report = validate(valid_record())
        self.assertEqual(report["status"], "PASS")
        self.assertFalse(report["claim_allowed"])

    def test_claim_promotion_is_rejected(self) -> None:
        record = valid_record()
        record["claim_allowed"] = True
        with self.assertRaisesRegex(ValidationError, "claim_allowed"):
            validate(record)

    def test_physical_promotion_is_rejected(self) -> None:
        record = valid_record()
        record["claims"]["fixed_physical"] = "VERIFIED_LIMITED"
        with self.assertRaisesRegex(ValidationError, "FIXED_PHYSICAL"):
            validate(record)

    def test_android_device_promotion_is_rejected(self) -> None:
        record = valid_record()
        record["claims"]["android_device"] = "VERIFIED_LIMITED"
        with self.assertRaisesRegex(ValidationError, "Android device"):
            validate(record)

    def test_android_blocker_must_be_identified(self) -> None:
        record = valid_record()
        record["gates"]["android"]["blocker"] = "unknown"
        with self.assertRaisesRegex(ValidationError, "bloqueio externo"):
            validate(record)

    def test_c_kotlin_signature_drift_is_rejected(self) -> None:
        record = valid_record()
        record["manifest_identity"]["value_hex"] = "0000000000000000"
        with self.assertRaisesRegex(ValidationError, "vetor C/Kotlin"):
            validate(record)

    def test_fnv_cannot_be_called_cryptographic(self) -> None:
        record = valid_record()
        record["manifest_identity"]["cryptographic"] = True
        with self.assertRaisesRegex(ValidationError, "criptográfico"):
            validate(record)

    def test_whole_payload_mapping_regression_is_rejected(self) -> None:
        record = valid_record()
        record["runtime_changes"]["whole_payload_map_on_open"] = True
        with self.assertRaisesRegex(ValidationError, "mmap integral"):
            validate(record)

    def test_host_gate_regression_is_rejected(self) -> None:
        record = valid_record()
        record["gates"]["host"]["conclusion"] = "failure"
        with self.assertRaisesRegex(ValidationError, "gate host"):
            validate(record)


if __name__ == "__main__":
    unittest.main()
