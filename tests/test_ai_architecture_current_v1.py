import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "manifold" / "ai_architecture_current_v1.json"
VALIDATOR = ROOT / "tools" / "validate_ai_architecture_current_v1.py"

class AIArchitectureCurrentV1Test(unittest.TestCase):
    def test_manifest_shape(self):
        obj = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(obj["schema"], "rafaelia.ai-architecture-manifold-current.v1")
        self.assertFalse(obj["claim_allowed"])
        self.assertEqual(obj["read_policy"]["roots_max"], 3)
        self.assertEqual(obj["read_policy"]["depth_default"], 1)
        self.assertGreaterEqual(len(obj["atlas_areas"]), 12)
        self.assertGreaterEqual(len(obj["agent_roles"]), 11)
        self.assertGreaterEqual(len(obj["session_packets"]), 8)

    def test_validator(self):
        cp = subprocess.run([sys.executable, str(VALIDATOR)], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertIn("PASS ai_architecture_current_v1", cp.stdout)

if __name__ == "__main__":
    unittest.main()
