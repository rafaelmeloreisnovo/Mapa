#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_multimodal_cave_seed.py"
SEED_PATH = ROOT / "data" / "multimodal" / "MULTIMODAL_CAVE_SEED_20260822.v1.json"
spec = importlib.util.spec_from_file_location("multimodal_cave", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class MultimodalCaveSeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))

    def validate_mutation(self, mutator) -> None:
        payload = copy.deepcopy(self.seed)
        mutator(payload)
        with self.assertRaises(module.ValidationError):
            module.validate_seed(payload, ROOT)

    def test_real_seed_passes_all_bounded_gates(self) -> None:
        result = module.validate_seed(copy.deepcopy(self.seed), ROOT)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["objects"], 10)
        self.assertEqual(result["representations"], 10)
        self.assertEqual(result["tiles"], 28)
        self.assertEqual(result["root_tiles"], 10)
        self.assertEqual(result["extension_mime_mismatches"], 9)
        self.assertEqual(result["codec_vectors"], 1024)
        self.assertFalse(result["claim_allowed"])

    def test_exhaustive_10bit_roundtrip(self) -> None:
        self.assertEqual(module.exhaustive_roundtrip(), 1024)
        for x10 in range(1024):
            q8, r2 = module.encode_10_to_8_plus_residual(x10)
            self.assertEqual(module.decode_8_plus_residual(q8, r2), x10)

    def test_codec_rejects_invalid_types_and_ranges(self) -> None:
        for invalid in (-1, 1024, True, 1.0, "1", None):
            with self.assertRaises(module.ValidationError):
                module.encode_10_to_8_plus_residual(invalid)
        for invalid in (-1, 256, True, 1.0):
            with self.assertRaises(module.ValidationError):
                module.decode_8_plus_residual(invalid, 0)
        for invalid in (-1, 4, True, 1.0):
            with self.assertRaises(module.ValidationError):
                module.decode_8_plus_residual(0, invalid)

    def test_global_claim_promotion_fails_closed(self) -> None:
        self.validate_mutation(lambda payload: payload.__setitem__("claim_allowed", True))

    def test_nested_claim_promotion_fails_closed(self) -> None:
        self.validate_mutation(lambda payload: payload["tiles"][0].__setitem__("claim_allowed", True))

    def test_dangling_relation_fails_closed(self) -> None:
        self.validate_mutation(lambda payload: payload["relations"][0].__setitem__("target_id", "MISSING-NODE"))

    def test_duplicate_identity_fails_closed(self) -> None:
        self.validate_mutation(lambda payload: payload["objects"][1].__setitem__("object_id", "MMO-01"))

    def test_preface_cycle_or_invalid_depth_fails_closed(self) -> None:
        def mutate(payload):
            payload["route_prefaces"][0]["parent_preface_id"] = "PREFACE-CATHEDRAL"
            payload["route_prefaces"][0]["depth"] = 3

        self.validate_mutation(mutate)

    def test_child_tile_outside_parent_fails_closed(self) -> None:
        def mutate(payload):
            tile = next(item for item in payload["tiles"] if item["tile_id"] == "MMTILE-01-FORMULA")
            tile["bounds_normalized"]["x"] = 0.95

        self.validate_mutation(mutate)

    def test_scientific_interpretation_promotion_fails_closed(self) -> None:
        def mutate(payload):
            tile = next(item for item in payload["tiles"] if item["tile_id"] == "MMTILE-03-FRACTAL")
            tile["interpretations"][0]["state"] = "VERIFIED_LIMITED"

        self.validate_mutation(mutate)

    def test_extension_is_not_allowed_to_override_detected_mime(self) -> None:
        self.validate_mutation(lambda payload: payload["objects"][0]["source"].__setitem__("extension_mime_match", True))

    def test_portrait_identity_and_crop_guards_fail_closed(self) -> None:
        def mutate(payload):
            portrait = next(item for item in payload["objects"] if item["object_id"] == "MMO-10")
            portrait["privacy"]["segmentation_export_allowed"] = True

        self.validate_mutation(mutate)

    def test_matrix_anchor_is_exact_not_decorative(self) -> None:
        def mutate(payload):
            anchor = next(item for item in payload["mathematical_anchors"] if item["anchor_id"] == "ANCHOR-MATRIX-M")
            anchor["matrix_A"][0][0] = 0

        self.validate_mutation(mutate)

    def test_distinct_square_root_asts_cannot_collapse(self) -> None:
        def mutate(payload):
            radical = next(item for item in payload["mathematical_anchors"] if item["anchor_id"] == "ANCHOR-SQRT-3-OVER-2-IN-RADICAL")
            quotient = next(item for item in payload["mathematical_anchors"] if item["anchor_id"] == "ANCHOR-SQRT3-OVER-2")
            quotient["normalized_ast"] = radical["normalized_ast"]

        self.validate_mutation(mutate)

    def test_unexecuted_transform_cannot_report_pass(self) -> None:
        def mutate(payload):
            transform = next(item for item in payload["transforms"] if item["transform_id"] == "MMX-ROTATE-90")
            transform["evidence"]["result"] = "PASS"

        self.validate_mutation(mutate)


if __name__ == "__main__":
    unittest.main(verbosity=2)
