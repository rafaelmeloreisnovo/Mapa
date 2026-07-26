#!/usr/bin/env python3
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_square_median_x3264_pointer as validator


class SquareMedianPointerTests(unittest.TestCase):
    def test_packet_is_valid_and_fail_closed(self):
        report = validator.validate(ROOT)
        self.assertTrue(report["pass"], report)
        self.assertEqual(report["state"], "PASS_POINTER_BOUNDARY")
        self.assertEqual(report["pointer_count"], 4)
        self.assertFalse(report["claim_allowed"])
        self.assertEqual(report["errors"], [])

    def test_runtime_and_consumer_gates_remain_open(self):
        import json
        packet = json.loads(
            (ROOT / "data/control-plane/evidence_pointer_square_median_x3264.v1.json")
            .read_text(encoding="utf-8")
        )
        gates = packet["gates"]
        self.assertEqual(gates["source_built_qemu_i386"], "TOKEN_VAZIO_PENDING_WORKFLOW")
        self.assertEqual(gates["source_built_qemu_x86_64"], "TOKEN_VAZIO_PENDING_WORKFLOW")
        self.assertEqual(gates["vectras_linux_user_profile"], "TOKEN_VAZIO_NOT_IMPLEMENTED")
        self.assertEqual(gates["android_dispatch"], "TOKEN_VAZIO")
        self.assertEqual(gates["full_system_guest_boot"], "NOT_IN_SCOPE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
