import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_architecture_family_registry.py"
REGISTRY = ROOT / "data/ontology/architectures/ARCHITECTURE_FAMILY_REGISTRY_V1.yaml"
INDEX = ROOT / "indices/semantic/ARCHITECTURE_FAMILY_INDEX_V1.yaml"


class ArchitectureFamilyRegistryTests(unittest.TestCase):
    def test_architecture_family_registry_gate_passes(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS architecture-family-registry-v1", result.stdout)

    def test_registry_preserves_epistemic_boundaries(self):
        text = REGISTRY.read_text(encoding="utf-8")
        self.assertIn("CONCEPT != IMPLEMENTATION != BUILD != EXECUTION != EVIDENCE != CLAIM", text)
        self.assertIn("HISTORICAL_ASSISTANT_ASSERTION != PRIMARY_EVIDENCE", text)
        self.assertIn("TOKEN_VAZIO != ZERO", text)
        self.assertIn("claim_allowed: false", text)

    def test_index_routes_only_known_architecture_ids(self):
        registry = REGISTRY.read_text(encoding="utf-8")
        index = INDEX.read_text(encoding="utf-8")
        for arch_id in (
            "ARCH-FCEA",
            "ARCH-ZETA",
            "ARCH-V79-1",
            "ARCH-MAYA-LINEAGE",
            "ARCH-HCPM",
            "ARCH-NEXUS",
            "ARCH-EXACORDEX",
        ):
            self.assertIn(arch_id, registry)
            self.assertIn(arch_id, index)

    def test_index_exposes_discovery_contract(self):
        index = INDEX.read_text(encoding="utf-8")
        self.assertIn("discovery_pipeline: scripts/discover_architecture_families.py", index)
        self.assertIn("CO_OCCURRENCE != CAUSATION != DEPENDENCY", index)
        self.assertIn("raw_text_emission: false", index)


if __name__ == "__main__":
    unittest.main()
