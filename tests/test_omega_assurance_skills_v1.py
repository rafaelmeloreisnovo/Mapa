#!/usr/bin/env python3

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_omega_assurance_skills_v1.py"
spec = importlib.util.spec_from_file_location("omega_validator", VALIDATOR)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


class OmegaAssuranceSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / "skills" / "omega-assurance-skills.v1.json").read_text(encoding="utf-8"))

    def test_real_registry_passes(self):
        self.assertEqual(mod.validate_registry(self.registry, ROOT), [])

    def test_claim_allowed_true_fails(self):
        data = copy.deepcopy(self.registry)
        data["claim_allowed"] = True
        errors = mod.validate_registry(data, ROOT)
        self.assertTrue(any("claim_allowed" in e for e in errors))

    def test_unknown_dependency_fails(self):
        data = copy.deepcopy(self.registry)
        data["skills"][1]["depends_on"] = ["does-not-exist"]
        errors = mod.validate_registry(data, ROOT)
        self.assertTrue(any("unknown dependency" in e for e in errors))

    def test_dependency_cycle_fails(self):
        data = copy.deepcopy(self.registry)
        for skill in data["skills"]:
            if skill["id"] == "identity-provenance":
                skill["depends_on"] = ["epistemic-discernment"]
        errors = mod.validate_registry(data, ROOT)
        self.assertTrue(any("dependency cycle" in e for e in errors))

    def test_missing_fail_closed_invariant_fails(self):
        data = copy.deepcopy(self.registry)
        data["fail_closed_invariants"].remove("TOKEN_VAZIO != PASS")
        errors = mod.validate_registry(data, ROOT)
        self.assertTrue(any("TOKEN_VAZIO != PASS" in e for e in errors))

    def test_private_locator_in_skill_fails(self):
        with tempfile.TemporaryDirectory() as td:
            temp_root = Path(td)
            for skill in self.registry["skills"]:
                src = ROOT / skill["path"]
                dst = temp_root / skill["path"]
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            target = temp_root / "skills" / "privacy-information" / "SKILL.md"
            target.write_text(target.read_text(encoding="utf-8") + "\ndrive:1THISISAPRIVATELOCATOR12345\n", encoding="utf-8")
            errors = mod.validate_registry(self.registry, temp_root)
            self.assertTrue(any("private Drive-style locator" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
