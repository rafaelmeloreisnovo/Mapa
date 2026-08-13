#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path
import tempfile
ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT/"tools"/"scan_secret_hygiene.py"
spec=importlib.util.spec_from_file_location("scan_secret_hygiene",TOOL)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
def run_case(name,content,expected_rule=None,expect_clean=False):
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); (root/"sample.txt").write_text(content,encoding="utf-8"); receipt=mod.scan(root); rules={x["rule"] for x in receipt["findings"]}
        if expect_clean:
            assert receipt["result"]=="PASS" and receipt["coverage_complete"] is True and not rules
        else:
            assert receipt["result"]=="FAIL" and expected_rule in rules
            for finding in receipt["findings"]:
                assert set(finding)=={"rule","path","line","fingerprint_sha256"} and len(finding["fingerprint_sha256"])==64
        print("PASS",name)
def main():
    run_case("credential-in-url","remote=https://user:supersecretvalue@example.invalid/repo.git\n","CREDENTIAL_IN_URL")
    run_case("github-token-prefix","token=ghp_1234567890abcdefghijklmnop\n","GITHUB_TOKEN_PREFIX")
    run_case("hardcoded-jwt-secret",'JWT_SECRET = "this-is-a-hardcoded-secret"\n',"HARDCODED_JWT_SECRET")
    run_case("private-key-block","-----BEGIN PRIVATE KEY-----\nREDACTED\n","PRIVATE_KEY_BLOCK")
    run_case("env-backed-jwt-is-clean",'JWT_SECRET = os.environ["JWT_SECRET"]\n',expect_clean=True)
    run_case("ordinary-github-url-is-clean","remote=https://github.com/example/project.git\n",expect_clean=True)
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); (root/"binary.bin").write_bytes(b"abc\x00def"); r=mod.scan(root); assert r["result"]=="PASS" and r["coverage_complete"] is True and r["skipped_binary"]==1; print("PASS binary-file-skipped")
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); bad=root/"bad"; bad.mkdir(); (bad/"x.txt").write_text("ordinary text\n",encoding="utf-8"); r=mod.scan(root); assert r["files_scanned"]==1 and r["coverage_complete"] is True; print("PASS recursive-clean-scan")
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); (root/"large.txt").write_bytes(b"A"*(mod.MAX_FILE_BYTES+1)); r=mod.scan(root); assert r["result"]=="FAIL" and r["coverage_complete"] is False and r["skipped_oversize_text"]==1 and r["findings_count"]==0; print("PASS oversize-text-fails-closed")
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); (root/"large.bin").write_bytes(b"\x00"+b"A"*mod.MAX_FILE_BYTES); r=mod.scan(root); assert r["result"]=="PASS" and r["coverage_complete"] is True and r["skipped_binary"]==1 and r["skipped_oversize_text"]==0; print("PASS oversize-binary-preserves-binary-contract")
    print("PASS 10/10")
if __name__=="__main__": main()
