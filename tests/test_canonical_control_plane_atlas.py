#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_canonical_control_plane_atlas.py"
CANONICAL_PATH = ROOT / "data" / "control-plane" / "CANONICAL_CONTROL_PLANE_ATLAS_V1_20260829.json"
NEGATIVE_PATH = ROOT / "fixtures" / "canonical_control_plane_atlas.invalid.token_zero.v1.json"

spec = importlib.util.spec_from_file_location("canonical_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(validator)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class CanonicalControlPlaneTests(unittest.TestCase):
    def test_canonical_control_plane_passes(self) -> None:
        errors = validator.validate(load(CANONICAL_PATH))
        self.assertEqual(errors, [], "canonical control-plane must pass: " + "; ".join(errors))

    def test_token_zero_negative_fixture_fails(self) -> None:
        errors = validator.validate(load(NEGATIVE_PATH))
        self.assertTrue(errors, "negative fixture must fail")
        joined = "\n".join(errors)
        self.assertIn("TOKEN_VAZIO", joined)
        self.assertIn("global claim", joined)
        self.assertIn("CLOSED_VERIFIED", joined)

    def test_required_atlas_planes_are_exactly_represented(self) -> None:
        data = load(CANONICAL_PATH)
        self.assertTrue(validator.EXPECTED_ATLAS_PLANES <= set(data["atlas_planes"]))

    def test_ingestion_order_is_frozen(self) -> None:
        data = load(CANONICAL_PATH)
        self.assertEqual(data["ingestion_order"], validator.EXPECTED_INGESTION_ORDER)

    def test_open_priority_gaps_keep_fail_closed(self) -> None:
        data = load(CANONICAL_PATH)
        self.assertTrue(data["open_priority_gaps"])
        self.assertFalse(data["claim_allowed"])
        self.assertNotEqual(data["state"], "CLOSED_VERIFIED")


if __name__ == "__main__":
    unittest.main()
