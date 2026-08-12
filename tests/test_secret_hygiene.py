#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "scan_secret_hygiene.py"
spec = importlib.util.spec_from_file_location("scan_secret_hygiene", TOOL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def run_case(name, content, expected_rule=None, expect_clean=False):
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "sample.txt").write_text(content, encoding="utf-8")
        receipt = mod.scan(root)
        rules = {x["rule"] for x in receipt["findings"]}
        if expect_clean:
            assert receipt["result"] == "PASS", (name, receipt)
            assert not rules
        else:
            assert receipt["result"] == "FAIL", (name, receipt)
            assert expected_rule in rules, (name, expected_rule, rules)
            for finding in receipt["findings"]:
                assert set(finding) == {"rule","path","line","fingerprint_sha256"}
                assert len(finding["fingerprint_sha256"]) == 64
        print("PASS", name)

def main():
    run_case("credential-in-url", "remote=https://user:supersecretvalue@example.invalid/repo.git\n", "CREDENTIAL_IN_URL")
    run_case("github-token-prefix", "token=ghp_1234567890abcdefghijklmnop\n", "GITHUB_TOKEN_PREFIX")
    run_case("hardcoded-jwt-secret", 'JWT_SECRET = "this-is-a-hardcoded-secret"\n', "HARDCODED_JWT_SECRET")
    run_case("private-key-block", "-----BEGIN PRIVATE KEY-----\nREDACTED\n", "PRIVATE_KEY_BLOCK")
    run_case("env-backed-jwt-is-clean", 'JWT_SECRET = os.environ["JWT_SECRET"]\n', expect_clean=True)
    run_case("ordinary-github-url-is-clean", "remote=https://github.com/example/project.git\n", expect_clean=True)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "binary.bin").write_bytes(b"abc\x00def")
        receipt = mod.scan(root)
        assert receipt["result"] == "PASS"
        assert receipt["skipped_binary"] == 1
        print("PASS binary-file-skipped")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        bad = root / "bad"
        bad.mkdir()
        (bad / "x.txt").write_text("ordinary text\n", encoding="utf-8")
        receipt = mod.scan(root)
        assert receipt["files_scanned"] == 1
        print("PASS recursive-clean-scan")
    print("PASS 8/8")

if __name__ == "__main__":
    main()
