from __future__ import annotations

import pathlib
import re
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "governance" / "check_semantic_event_v2.py"
FIXTURE = ROOT / "tests" / "fixtures" / "mu-semantic-event.v2.valid.json"


class SemanticEventV2CliTests(unittest.TestCase):
    def run_once(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_cli_passes_and_hash_repeats(self):
        a = self.run_once()
        b = self.run_once()
        self.assertEqual(0, a.returncode, a.stderr)
        self.assertEqual(0, b.returncode, b.stderr)
        ha = re.search(r"sha256=([0-9a-f]{64})", a.stdout)
        hb = re.search(r"sha256=([0-9a-f]{64})", b.stdout)
        self.assertIsNotNone(ha)
        self.assertIsNotNone(hb)
        self.assertEqual(ha.group(1), hb.group(1))


if __name__ == "__main__":
    unittest.main()
