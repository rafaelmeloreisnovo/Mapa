import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.catalog_zip_bytes_v1 import scan_zip
from tools.generate_byte_catalog_v1 import generate, write_jsonl

class ByteCatalogV1Tests(unittest.TestCase):
    def test_byte_catalog_has_exact_256_rows(self):
        rows = generate()
        self.assertEqual(len(rows), 256)
        self.assertEqual([row["byte_dec"] for row in rows], list(range(256)))

    def test_byte_layer_boundaries(self):
        rows = {row["byte_dec"]: row for row in generate()}
        self.assertEqual(rows[0]["ascii_class"], "CONTROL")
        self.assertEqual(rows[65]["ascii_symbol"], "A")
        self.assertEqual(rows[127]["ascii_class"], "DEL")
        self.assertEqual(rows[128]["utf8_role"], "CONTINUATION")
        self.assertEqual(rows[0xC2]["utf8_role"], "LEAD_2")
        self.assertEqual(rows[0xE2]["utf8_role"], "LEAD_3")
        self.assertEqual(rows[0xF0]["utf8_role"], "LEAD_4")
        self.assertEqual(rows[0xF5]["utf8_role"], "INVALID_LEAD")
        self.assertFalse(rows[0x80]["standalone_utf8"])
        self.assertEqual(rows[255]["semantic_state"], "TOKEN_VAZIO_UNBOUND")
        self.assertFalse(rows[255]["claim_allowed"])

    def test_generated_catalog_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bytes.jsonl"
            write_jsonl(path)
            decoded = [
                json.loads(line)
                for line in path.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(len(decoded), 256)
            self.assertEqual(decoded[32]["byte_hex"], "0x20")
            self.assertEqual(decoded[255]["latin1_codepoint"], "U+00FF")

    def test_zip_catalog_redundancy_crc_and_word_views(self):
        payload = bytes(range(64))
        page = bytes(range(256))
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "sample.zip"
            with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("a.bin", payload)
                zf.writestr("b.bin", payload)
                zf.writestr("page.bin", page)
                zf.writestr("../not-extracted.txt", "safe because scanner never extracts")

            out = scan_zip(archive, include_word_views=True)
            self.assertEqual(out["schema"], "rafaelia.zip-byte-catalog.v1")
            self.assertFalse(out["claim_allowed"])
            members = {member["name"]: member for member in out["members"]}
            self.assertTrue(members["a.bin"]["crc_match"])
            self.assertEqual(members["a.bin"]["blocks"][0]["read32_count"], 16)
            self.assertEqual(members["a.bin"]["blocks"][0]["read64_count"], 8)
            self.assertEqual(len(members["a.bin"]["blocks"][0]["word_views"]["u32_le"]), 16)
            self.assertEqual(len(members["a.bin"]["blocks"][0]["word_views"]["u64_le"]), 8)
            self.assertEqual(members["page.bin"]["pages"][0]["read32_count"], 64)
            self.assertEqual(members["page.bin"]["pages"][0]["read64_count"], 32)
            self.assertTrue(members["page.bin"]["pages"][0]["full_page_256"])
            self.assertTrue(members["../not-extracted.txt"]["unsafe_path_flag"])

            a_block = members["a.bin"]["blocks"][0]
            b_block = members["b.bin"]["blocks"][0]
            self.assertEqual(a_block["redundancy_group_id"], b_block["redundancy_group_id"])
            self.assertGreaterEqual(a_block["redundancy_count"], 2)

    def test_size_limit_stays_token_vazio(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "bounded.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("large.bin", b"x" * 65)
            out = scan_zip(archive, max_member_bytes=64)
            self.assertEqual(
                out["members"][0]["state"],
                "TOKEN_VAZIO_MEMBER_SIZE_LIMIT",
            )

if __name__ == "__main__":
    unittest.main()
