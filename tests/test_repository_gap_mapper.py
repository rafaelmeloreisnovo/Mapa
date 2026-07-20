#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MAPPER = REPO_ROOT / "tools" / "repository_gap_mapper.py"


class RepositoryGapMapperTest(unittest.TestCase):
    def run_mapper(self, root: Path, fail_on: str = "none"):
        output_json = root / "out" / "map.json"
        output_md = root / "out" / "map.md"
        proc = subprocess.run(
            [
                sys.executable,
                str(MAPPER),
                "--root", f"fixture={root}",
                "--output-json", str(output_json),
                "--output-md", str(output_md),
                "--exclude", "out",
                "--fail-on", fail_on,
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        payload = json.loads(output_json.read_text(encoding="utf-8"))
        return proc, payload, output_md.read_text(encoding="utf-8")

    def test_maps_asm_elf_dex_apk_and_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "build.gradle").write_text(
                'externalNativeBuild { cmake { path "CMakeLists.txt" } }\n',
                encoding="utf-8",
            )
            (root / "CMakeLists.txt").write_text(
                "add_library(core STATIC src/used.S)\n",
                encoding="utf-8",
            )
            (root / "src" / "used.S").write_text(".text\n", encoding="utf-8")
            (root / "src" / "loose.asm").write_text("; TODO wire me\n", encoding="utf-8")
            (root / "libcore.so").write_bytes(b"\x7fELF" + b"\x00" * 32)
            (root / "classes.dex").write_bytes(b"dex\n035\x00" + b"\x00" * 32)
            (root / "app.apk").write_bytes(b"PK\x03\x04" + b"\x00" * 32)
            (root / "README.md").write_text("TOKEN_VAZIO: runtime evidence\n", encoding="utf-8")

            proc, payload, markdown = self.run_mapper(root)

            self.assertEqual(proc.returncode, 0, proc.stderr)
            by_path = {item["path"]: item for item in payload["artifacts"]}
            self.assertTrue(by_path["src/used.S"]["build_referenced"])
            self.assertIn("ASM_NOT_REFERENCED_BY_BUILD", by_path["src/loose.asm"]["gaps"])
            self.assertIn("UNRESOLVED_MARKERS", by_path["src/loose.asm"]["gaps"])
            self.assertEqual(by_path["libcore.so"]["kind"], "ELF")
            self.assertEqual(by_path["classes.dex"]["kind"], "DEX")
            self.assertEqual(by_path["app.apk"]["kind"], "APK")
            self.assertIn("BINARY_PROVENANCE_MISSING", by_path["app.apk"]["gaps"])
            self.assertIn("DOCUMENT_INCOMPLETE", by_path["README.md"]["gaps"])
            self.assertIn("Deterministic next actions", markdown)

    def test_fail_on_asm_is_enforceable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "loose.S").write_text(".text\n", encoding="utf-8")
            proc, _, _ = self.run_mapper(root, fail_on="asm")
            self.assertEqual(proc.returncode, 1)


if __name__ == "__main__":
    unittest.main()
