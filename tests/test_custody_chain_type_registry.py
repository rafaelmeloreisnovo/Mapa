from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_custody_chain_type_registry.py"
REGISTRY = ROOT / "data/control-plane/CUSTODY_CHAIN_TYPE_REGISTRY.v1.json"

spec = importlib.util.spec_from_file_location("custody_type_validator", SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CustodyChainTypeRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_canonical_registry_passes(self) -> None:
        self.assertEqual(module.validate_registry(self.data), [])

    def test_duplicate_profile_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["custody_profiles"].append(copy.deepcopy(data["custody_profiles"][0]))
        errors = module.validate_registry(data)
        self.assertTrue(any("duplicate custody_profiles id" in e for e in errors))

    def test_assistant_cannot_self_authorize_promotion(self) -> None:
        data = copy.deepcopy(self.data)
        for actor in data["actor_classes"]:
            if actor["actor_class"] == "ASSISTANT_ORCHESTRATOR":
                actor["can_self_authorize_promotion"] = True
                break
        errors = module.validate_registry(data)
        self.assertIn("ASSISTANT_ORCHESTRATOR cannot self-authorize promotion", errors)

    def test_unknown_surface_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["custody_profiles"][0]["surface"] = "MAGICAL_SURFACE"
        errors = module.validate_registry(data)
        self.assertTrue(any(".surface is invalid" in e for e in errors))

    def test_agent_action_requires_human_and_provider_anchors(self) -> None:
        data = copy.deepcopy(self.data)
        for profile in data["custody_profiles"]:
            if profile["profile_id"] == "AGENT_ACTION_CUSTODY":
                profile["required_anchors"].remove("provider_result_ref")
                break
        errors = module.validate_registry(data)
        self.assertIn("AGENT_ACTION_CUSTODY missing anchor: provider_result_ref", errors)


if __name__ == "__main__":
    unittest.main()
