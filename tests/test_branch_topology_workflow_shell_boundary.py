"""Prevent shell interpretation of pull request branch names in branch topology YAML."""
import os
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github/workflows/branch-topology-gate.yml'


def run_blocks(source):
    lines = source.splitlines()
    for i, line in enumerate(lines):
        match = re.match(r'^(\s*)run:\s*\|\s*$', line)
        if not match:
            continue
        indent = len(match.group(1))
        body = []
        for next_line in lines[i + 1:]:
            if next_line.strip() and len(next_line) - len(next_line.lstrip()) <= indent:
                break
            body.append(next_line)
        yield '\n'.join(body)


class BranchTopologyShellBoundaryTests(unittest.TestCase):
    def test_no_event_output_embedded_in_bash(self):
        source = WORKFLOW.read_text(encoding='utf-8')
        blocks = list(run_blocks(source))
        self.assertGreater(len(blocks), 0)
        for block in blocks:
            self.assertNotRegex(block, r'\$\{\{\s*steps\.event\.outputs\.')
        for key, variable in [('default_branch', 'DEFAULT_BRANCH'),
                              ('base_ref', 'BASE_REF'), ('head_ref', 'HEAD_REF')]:
            self.assertEqual(2, source.count(f'{variable}: ${{{{ steps.event.outputs.{key} }}}}'))
            self.assertIn(f'"${variable}"', source)

    def test_negative_shell_falsifier_and_literal_env_transport(self):
        input_ref = '$(printf RAFAELIA_SHELL_BOUNDARY_PROBE)'
        bad = subprocess.run(
            ['bash', '-c', 'printf "%s\\n" "$(printf RAFAELIA_SHELL_BOUNDARY_PROBE)"'],
            check=True, text=True, capture_output=True, timeout=5,
        ).stdout.strip()
        good = subprocess.run(
            ['bash', '-c', 'printf "%s\\n" "$HEAD_REF"'],
            check=True, text=True, capture_output=True, timeout=5,
            env={**os.environ, 'HEAD_REF': input_ref},
        ).stdout.strip()
        self.assertEqual('RAFAELIA_SHELL_BOUNDARY_PROBE', bad)
        self.assertEqual(input_ref, good)


if __name__ == '__main__':
    unittest.main()
