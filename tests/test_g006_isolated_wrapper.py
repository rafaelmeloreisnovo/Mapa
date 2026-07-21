from __future__ import annotations

import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts" / "run_g006_isolated.sh"
COMMIT = "a" * 40


class G006IsolatedWrapperTests(unittest.TestCase):
    def fixture(self, tmp: Path):
        fake_bin = tmp / "bin"
        fake_bin.mkdir()
        fake_repo = tmp / "repo"
        fake_repo.mkdir()
        capture = tmp / "python-argv.txt"

        git_script = fake_bin / "git"
        git_script.write_text(
            "#!/bin/sh\n"
            "if [ \"$1\" = \"rev-parse\" ] && [ \"$2\" = \"--show-toplevel\" ]; then\n"
            f"  printf '%s\\n' '{fake_repo}'\n"
            "  exit 0\n"
            "fi\n"
            "if [ \"$1\" = \"-C\" ] && [ \"$3\" = \"rev-parse\" ] && [ \"$4\" = \"HEAD\" ]; then\n"
            f"  printf '%s\\n' '{COMMIT}'\n"
            "  exit 0\n"
            "fi\n"
            "exit 9\n",
            encoding="utf-8",
        )
        python_script = fake_bin / "python3"
        python_script.write_text(
            "#!/bin/sh\n"
            f"printf '%s\\n' \"$@\" > '{capture}'\n"
            "exit 0\n",
            encoding="utf-8",
        )
        for path in (git_script, python_script):
            path.chmod(path.stat().st_mode | stat.S_IXUSR)

        inherited_path = os.environ.get("PATH", "")
        env = {
            **os.environ,
            "PATH": str(fake_bin) + os.pathsep + inherited_path,
            "TMPDIR": str(tmp / "external-tmp"),
        }
        return fake_repo, capture, env

    def run_wrapper(self, cwd: Path, env: dict[str, str], *args: str):
        return subprocess.run(
            ["sh", str(WRAPPER), *args],
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_routes_output_outside_repository(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            fake_repo, capture, env = self.fixture(tmp)
            proc = self.run_wrapper(fake_repo, env, COMMIT)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            argv = capture.read_text(encoding="utf-8").splitlines()
            output = argv[argv.index("--output-dir") + 1]
            self.assertTrue(output.startswith(str(tmp / "external-tmp")))
            self.assertFalse(output.startswith(str(fake_repo)))
            self.assertEqual(argv[argv.index("--expected-commit") + 1], COMMIT)

    def test_existing_output_is_immutable(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            fake_repo, _, env = self.fixture(tmp)
            output = Path(env["TMPDIR"]) / "mapa-g006-audit" / COMMIT
            output.mkdir(parents=True)
            proc = self.run_wrapper(fake_repo, env, COMMIT)
            self.assertEqual(proc.returncode, 3)
            self.assertIn("output already exists", proc.stderr)

    def test_invalid_commit_is_rejected(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            fake_repo, _, env = self.fixture(tmp)
            proc = self.run_wrapper(fake_repo, env, "main")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("lowercase hexadecimal", proc.stderr)

    def test_short_hex_commit_is_rejected(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            fake_repo, _, env = self.fixture(tmp)
            proc = self.run_wrapper(fake_repo, env, "a" * 39)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("40 characters", proc.stderr)

    def test_tmpdir_inside_repository_is_rejected(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            fake_repo, _, env = self.fixture(tmp)
            env["TMPDIR"] = str(fake_repo / ".evidence")
            proc = self.run_wrapper(fake_repo, env, COMMIT)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("outside the repository root", proc.stderr)

    def test_default_commit_is_observed_from_git(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            fake_repo, capture, env = self.fixture(tmp)
            proc = self.run_wrapper(fake_repo, env)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            argv = capture.read_text(encoding="utf-8").splitlines()
            self.assertEqual(argv[argv.index("--expected-commit") + 1], COMMIT)


if __name__ == "__main__":
    unittest.main()
