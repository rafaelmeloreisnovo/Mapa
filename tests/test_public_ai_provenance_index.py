#!/usr/bin/env python3
import copy
import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_public_ai_provenance_index.py"
spec = importlib.util.spec_from_file_location("prov", MODULE_PATH)
prov = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(prov)


class PublicAIProvenanceInvariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = prov.load(prov.REGISTRY)
        cls.manifest = prov.load(prov.MANIFEST)

    def test_current_registry_and_manifest_pass(self):
        self.assertEqual([], prov.check_registry(self.registry))
        self.assertEqual([], prov.check_manifest(self.manifest))

    def test_text_style_cannot_be_provider_proof(self):
        bad = copy.deepcopy(self.registry)
        bad["forbidden_promotions"].remove("TEXT_STYLE_TO_PROVIDER_PROOF")
        self.assertTrue(prov.check_registry(bad))

    def test_resolution_cannot_be_provider_proof(self):
        bad = copy.deepcopy(self.registry)
        bad["forbidden_promotions"].remove("IMAGE_RESOLUTION_TO_PROVIDER_PROOF")
        self.assertTrue(prov.check_registry(bad))

    def test_negative_signal_cannot_prove_non_origin(self):
        bad = copy.deepcopy(self.registry)
        bad["forbidden_promotions"].remove("NO_SIGNAL_TO_NON_ORIGIN_PROOF")
        self.assertTrue(prov.check_registry(bad))

    def test_private_raw_content_flag_fails(self):
        bad = copy.deepcopy(self.manifest)
        bad["raw_content_included"] = True
        self.assertTrue(prov.check_manifest(bad))

    def test_navigation_root_detects_reordering(self):
        bad = copy.deepcopy(self.manifest)
        bad["chunks"][0], bad["chunks"][1] = bad["chunks"][1], bad["chunks"][0]
        self.assertTrue(prov.check_manifest(bad))

    def test_indices_are_plural_and_ordered(self):
        bad = copy.deepcopy(self.manifest)
        bad["index_invariants"] = ["IDX-IDENTITY"]
        self.assertTrue(prov.check_manifest(bad))


if __name__ == "__main__":
    unittest.main()
