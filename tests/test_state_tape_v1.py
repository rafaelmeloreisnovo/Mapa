import unittest

from tools.state_tape_v1 import (
    combine_byte_pair,
    compose_streams,
    pair16,
    punched_tape,
    snapshot_delta,
)

class StateTapeV1Tests(unittest.TestCase):
    def test_pair16_is_pairing_not_8x8_assumption(self):
        data = bytes([0x12, 0x34, 0xAB, 0xCD])
        be = pair16(data, "big")
        le = pair16(data, "little")
        self.assertEqual(be[0]["word16"], 0x1234)
        self.assertEqual(be[1]["word16"], 0xABCD)
        self.assertEqual(le[0]["word16"], 0x3412)

    def test_operator_family_is_explicit(self):
        out = combine_byte_pair(0b10100000, 0b00110000)
        self.assertEqual(out["or8"], 0b10110000)
        self.assertEqual(out["and8"], 0b00100000)
        self.assertEqual(out["xor8"], 0b10010000)
        self.assertEqual(out["semantic_operator"], "TOKEN_VAZIO_UNBOUND")

    def test_stream_composition_does_not_choose_semantics(self):
        out = compose_streams(bytes([1, 2]), bytes([3, 4]))
        self.assertEqual(out["length_compared"], 2)
        self.assertEqual(out["operator_choice"], "TOKEN_VAZIO_UNBOUND")
        self.assertFalse(out["claim_allowed"])

    def test_sparse_delta_punched_tape(self):
        before = bytearray(256)
        after = bytearray(before)
        after[3] = 0x01
        after[130] = 0x80
        delta = snapshot_delta(bytes(before), bytes(after), block_size=64, page_size=256)
        self.assertEqual(delta["changed_bytes"], 2)
        self.assertEqual(delta["changed_bits"], 2)
        self.assertEqual(delta["state"], "SPARSE_DELTA_OBSERVED")
        self.assertEqual(punched_tape(delta), "●·●·")
        self.assertTrue(delta["page_activity"][0]["changed"])

    def test_no_delta_is_explicit(self):
        data = bytes(range(64))
        delta = snapshot_delta(data, data)
        self.assertEqual(delta["state"], "NO_DELTA")
        self.assertEqual(delta["changed_bytes"], 0)
        self.assertEqual(punched_tape(delta), "·")

    def test_size_change_is_not_hidden(self):
        delta = snapshot_delta(b"abc", b"abcd", block_size=2, page_size=4)
        self.assertEqual(delta["state"], "SIZE_CHANGED")
        self.assertGreaterEqual(delta["changed_bytes"], 1)

if __name__ == "__main__":
    unittest.main()
