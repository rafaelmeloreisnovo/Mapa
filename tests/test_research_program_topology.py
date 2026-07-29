from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_research_program_topology.py"
DATA = ROOT / "data" / "sementeira" / "graphs" / "formalismo-7d-research-topology.v1.json"

spec = importlib.util.spec_from_file_location("topology_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class ResearchProgramTopologyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(DATA.read_text(encoding="utf-8"))

    def test_canonical_fixture_passes(self) -> None:
        summary = validator.validate(self.payload)
        self.assertEqual(summary["modules"], 8)
        self.assertEqual(summary["gates"], 11)
        self.assertEqual(summary["nodes"], 35)
        self.assertEqual(summary["edges"], 43)
        self.assertEqual(summary["claim_allowed_true"], 0)

    def test_claim_promotion_fails_closed(self) -> None:
        bad = copy.deepcopy(self.payload)
        bad["modules"][0]["claim_allowed"] = True
        with self.assertRaises(validator.ValidationError):
            validator.validate(bad)

    def test_unknown_edge_type_is_rejected(self) -> None:
        bad = copy.deepcopy(self.payload)
        bad["edges"][0]["type"] = "looks_like"
        with self.assertRaises(validator.ValidationError):
            validator.validate(bad)

    def test_missing_edge_endpoint_is_rejected(self) -> None:
        bad = copy.deepcopy(self.payload)
        bad["edges"][0]["to"] = "MISSING-NODE"
        with self.assertRaises(validator.ValidationError):
            validator.validate(bad)

    def test_reversed_semantic_edge_is_rejected(self) -> None:
        bad = copy.deepcopy(self.payload)
        edge = next(item for item in bad["edges"] if item["id"] == "E014")
        edge["from"], edge["to"] = edge["to"], edge["from"]
        with self.assertRaises(validator.ValidationError):
            validator.validate(bad)

    def test_gate_chain_break_is_rejected(self) -> None:
        bad = copy.deepcopy(self.payload)
        bad["riemann_program"]["gates"][4]["next"] = "R9"
        with self.assertRaises(validator.ValidationError):
            validator.validate(bad)

    def test_wrong_reclassification_is_rejected(self) -> None:
        bad = copy.deepcopy(self.payload)
        bad["modules"][2]["current_state"] = "PROGRAMA_CONJECTURAL"
        with self.assertRaises(validator.ValidationError):
            validator.validate(bad)

    def test_missing_required_gate_edge_is_rejected(self) -> None:
        bad = copy.deepcopy(self.payload)
        bad["edges"] = [
            edge
            for edge in bad["edges"]
            if not (
                edge["from"] == "UTM-194"
                and edge["to"] == "R7"
                and edge["type"] == "requires_gate"
            )
        ]
        with self.assertRaises(validator.ValidationError):
            validator.validate(bad)


if __name__ == "__main__":
    unittest.main()
