import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class ManifoldHumanEntryTests(unittest.TestCase):
    def test_human_entry_bridges_to_canonical_boot(self):
        manifest = json.loads((ROOT/"data"/"manifold"/"human_entry_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["entry_id"], "HUMAN_ENTRY_V1")
        self.assertEqual(manifest["route_id"], "R0011")
        self.assertFalse(manifest["claim_allowed"])
        self.assertIn("HUMAN_ENTRY!=BOOTSTRAP", manifest["invariants"])
        self.assertEqual(manifest["path"][:3], ["HUMAN_ENTRY","CANONICAL_BOOT_V2","CURRENT_STATE"])

        routes = [
            json.loads(line)
            for line in (ROOT/"data"/"manifold"/"routes_omega_v1.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        route = next((r for r in routes if r.get("route_id") == "R0011"), None)
        self.assertIsNotNone(route)
        self.assertEqual(route["path"][:3], ["HUMAN_ENTRY","CANONICAL_BOOT_V2","CURRENT_STATE"])
        self.assertIn("METAPHOR != CLAIM", route["evidence_gate"])
        self.assertIn("SIMPLIFICATION != EVIDENCE", route["evidence_gate"])

if __name__ == "__main__":
    unittest.main()
