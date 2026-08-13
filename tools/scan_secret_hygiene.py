#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, re, sys
from pathlib import Path

MAX_FILE_BYTES = 2 * 1024 * 1024
SNIFF_BYTES = 4096
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}
RULES = [
    ("GITHUB_TOKEN_PREFIX", re.compile(r"\b(?:ghp|github_pat|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{16,}\b")),
    ("CREDENTIAL_IN_URL", re.compile(r"https?://[^\s/:@]+:[^\s/@]+@[A-Za-z0-9.-]+")),
    ("HARDCODED_JWT_SECRET", re.compile(r"""\b(?:JWT_SECRET|JWT_SIGNING_KEY|JWT_KEY)\b\s*(?:=|:)\s*["'][^"'{}\n$]{8,}["']""", re.IGNORECASE)),
    ("PRIVATE_KEY_BLOCK", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
]
def fingerprint(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8", "surrogatepass")).hexdigest()

def iter_files(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        base = Path(current)
        for name in files:
            yield base / name

def scan_text(path: Path, text: str, root: Path):
    findings = []
    rel = path.relative_to(root).as_posix()
    for line_no, line in enumerate(text.splitlines(), 1):
        for rule, rx in RULES:
            for match in rx.finditer(line):
                findings.append({"rule":rule,"path":rel,"line":line_no,"fingerprint_sha256":fingerprint(match.group(0))})
    return findings

def _looks_binary(path: Path) -> bool:
    with path.open("rb") as f:
        return b"\x00" in f.read(SNIFF_BYTES)

def scan(root: Path):
    findings=[]; skipped_binary=0; skipped_oversize_text=0; unreadable=0; files_scanned=0
    for path in iter_files(root):
        try:
            size = path.stat().st_size
            if size > MAX_FILE_BYTES:
                if _looks_binary(path):
                    skipped_binary += 1
                else:
                    skipped_oversize_text += 1
                continue
            raw = path.read_bytes()
        except OSError:
            unreadable += 1
            continue
        if b"\x00" in raw[:SNIFF_BYTES]:
            skipped_binary += 1
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            skipped_binary += 1
            continue
        files_scanned += 1
        findings.extend(scan_text(path, text, root))
    coverage_complete = unreadable == 0 and skipped_oversize_text == 0
    return {"schema":"RAFAELIA_SECRET_SCAN_RECEIPT_V1","claim_allowed":False,"root":str(root),"files_scanned":files_scanned,"skipped_binary":skipped_binary,"skipped_oversize_text":skipped_oversize_text,"unreadable":unreadable,"coverage_complete":coverage_complete,"findings_count":len(findings),"findings":findings,"result":"FAIL" if findings or not coverage_complete else "PASS"}

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("root", nargs="?", default="."); ap.add_argument("--json-out"); ns=ap.parse_args(argv)
    root=Path(ns.root).resolve()
    if not root.is_dir():
        print("REJECT root-not-directory", file=sys.stderr); return 2
    receipt=scan(root); payload=json.dumps(receipt, indent=2, sort_keys=True)+"\n"
    if ns.json_out: Path(ns.json_out).write_text(payload, encoding="utf-8")
    sys.stdout.write(payload); return 0 if receipt["result"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
