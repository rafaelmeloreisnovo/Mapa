import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validator", ROOT / "scripts/validate_contextual_semantic_packet.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ContextualSemanticPacketTest(unittest.TestCase):
    def packet(self):
        return json.loads(
            (ROOT / "examples/contextual-semantic-packet.wine-formula.json")
            .read_text(encoding="utf-8")
        )

    def test_valid_packet_is_limited(self):
        report = MODULE.validate_packet(self.packet())
        self.assertEqual("PASS", report["status"])
        self.assertFalse(report["answer_allowed"])
        self.assertFalse(report["claim_allowed"])
        self.assertGreater(report["blocking_gaps"], 0)

    def test_unknown_source_reference_is_rejected(self):
        packet = self.packet()
        packet["memory_claims"][0]["source_refs"] = ["src:missing"]
        with self.assertRaises(MODULE.PacketError):
            MODULE.validate_packet(packet)

    def test_dangling_relation_is_rejected(self):
        packet = self.packet()
        packet["relations"][0]["object"] = "ent:missing"
        with self.assertRaises(MODULE.PacketError):
            MODULE.validate_packet(packet)

    def test_untyped_gap_is_rejected(self):
        packet = self.packet()
        packet["gaps"][0]["gap_class"] = "UNKNOWN"
        with self.assertRaises(MODULE.PacketError):
            MODULE.validate_packet(packet)

    def test_answer_cannot_open_with_blocking_gap(self):
        packet = self.packet()
        packet["answer_gate"]["allowed"] = True
        with self.assertRaises(MODULE.PacketError):
            MODULE.validate_packet(packet)

    def test_answer_cannot_open_with_unobserved_required_source(self):
        packet = self.packet()
        for gap in packet["gaps"]:
            gap["blocking"] = False
        packet["answer_gate"]["allowed"] = True
        with self.assertRaises(MODULE.PacketError):
            MODULE.validate_packet(packet)


if __name__ == "__main__":
    unittest.main()
