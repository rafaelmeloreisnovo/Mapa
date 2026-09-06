#!/usr/bin/env python3
"""Fail-closed PROFILE_OS CI evidence builder. stdlib only."""
from __future__ import annotations
import argparse, hashlib, json, os, pathlib, shutil, subprocess, sys, time, zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_capture(cmd: list[str], log: pathlib.Path) -> int:
    p = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log.write_text(p.stdout, encoding="utf-8")
    return p.returncode


def git_output(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.strip()


def git_tracked() -> list[str]:
    p = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, stdout=subprocess.PIPE, check=True)
    return sorted(x.decode("utf-8") for x in p.stdout.split(b"\0") if x)


def stage(chain_path: pathlib.Path, stage_id: str, state: str, details: dict) -> None:
    previous = None
    if chain_path.exists() and chain_path.stat().st_size:
        previous = hashlib.sha256(chain_path.read_bytes()).hexdigest()
    record = {
        "stage": stage_id,
        "state": state,
        "timestamp_epoch": int(time.time()),
        "previous_chain_sha256": previous,
        "details": details,
        "claim_allowed": False,
    }
    with chain_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def deterministic_zip(src_root: pathlib.Path, zip_path: pathlib.Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p in sorted(x for x in src_root.rglob("*") if x.is_file() and x != zip_path):
            rel = p.relative_to(src_root).as_posix()
            info = zipfile.ZipInfo(rel, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, p.read_bytes())


def verify_zip(zip_path: pathlib.Path, src_root: pathlib.Path) -> tuple[bool, list[str]]:
    errors = []
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            bad = zf.testzip()
            if bad:
                errors.append(f"crc failure: {bad}")
            members = sorted(i.filename for i in zf.infolist())
            expected = sorted(
                p.relative_to(src_root).as_posix()
                for p in src_root.rglob("*")
                if p.is_file() and p not in {zip_path, zip_path.with_suffix(zip_path.suffix + '.sha256')}
                and p.name not in {"gate-result.json", "token-resolution.jsonl"}
            )
            if members != expected:
                errors.append("zip member set differs from pre-result evidence tree")
            for name in members:
                disk = src_root / name
                if not disk.exists():
                    errors.append(f"zip member has no disk peer: {name}")
                    continue
                if hashlib.sha256(zf.read(name)).hexdigest() != sha256_file(disk):
                    errors.append(f"zip content mismatch: {name}")
    except zipfile.BadZipFile as exc:
        errors.append(f"bad zip: {exc}")
    return not errors, errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", default="data/control-plane/PROFILE_OS_CI_POLICY.v1.json")
    ap.add_argument("--out", default="build/profile-os-evidence")
    args = ap.parse_args()
    out = ROOT / args.out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    source = out / "source"
    source.mkdir()
    chain = out / "STAGE_CHAIN.jsonl"
    policy = json.loads((ROOT / args.policy).read_text(encoding="utf-8"))
    errors: list[str] = []

    checked_out_sha = git_output("rev-parse", "HEAD")
    expected_sha = os.getenv("PROFILE_OS_EXPECTED_SHA", checked_out_sha).strip() or checked_out_sha
    event_sha = os.getenv("GITHUB_SHA", "").strip() or None
    identity_ok = checked_out_sha == expected_sha
    if not identity_ok:
        errors.append(f"source identity mismatch: checked_out={checked_out_sha} expected={expected_sha}")
    stage(chain, "00_SOURCE_IDENTITY", "PASS" if identity_ok else "FAIL", {
        "checked_out_sha": checked_out_sha,
        "expected_sha": expected_sha,
        "event_sha": event_sha,
    })

    tracked = git_tracked()
    tracked_set = set(tracked)
    composition = policy["composition"]
    missing = [p for p in composition if not (ROOT / p).is_file()]
    untracked = [p for p in composition if p not in tracked_set]
    if missing: errors.append("missing composition: " + ", ".join(missing))
    if untracked: errors.append("untracked composition: " + ", ".join(untracked))
    stage(chain, "01_SOURCE_INVENTORY", "PASS" if not (missing or untracked) else "FAIL", {
        "tracked_files": len(tracked), "composition_files": len(composition), "missing": missing, "untracked": untracked
    })

    validator_log = out / "validator.log"
    tests_log = out / "tests.log"
    validator_rc = run_capture([
        sys.executable, "scripts/validate_profile_os_registry.py",
        "--registry", "data/control-plane/PROFILE_OS_REGISTRY.v1.json",
        "--supersession", "data/control-plane/PROFILE_OS_SUPERSESSION.v1.jsonl",
        "--gaps", "data/control-plane/PROFILE_OS_GAPS.v1.jsonl",
        "--ci-policy", args.policy,
    ], validator_log)
    tests_rc = run_capture([sys.executable, "-m", "unittest", "tests/test_profile_os_registry.py", "tests/test_profile_os_ci_gate.py"], tests_log)
    if validator_rc: errors.append(f"validator exit={validator_rc}")
    if tests_rc: errors.append(f"tests exit={tests_rc}")
    stage(chain, "02_VALIDATE_AND_TEST", "PASS" if validator_rc == tests_rc == 0 else "FAIL", {
        "validator_exit": validator_rc, "tests_exit": tests_rc
    })

    repo_rows = []
    for rel in tracked:
        p = ROOT / rel
        if p.is_file():
            repo_rows.append((sha256_file(p), p.stat().st_size, rel))
    (out / "REPOSITORY_TRACKED_SHA256SUMS.txt").write_text(
        "".join(f"{h}  {rel}\n" for h, _, rel in repo_rows), encoding="utf-8")
    tree_json = [{"path": rel, "bytes": size, "sha256": h} for h, size, rel in repo_rows]
    write_json(out / "TREE.json", {"tracked_file_count": len(tree_json), "files": tree_json, "claim_allowed": False})
    (out / "TREE.txt").write_text("".join(f"{i:06d}  {rel}\n" for i, (_, _, rel) in enumerate(repo_rows, 1)), encoding="utf-8")

    composition_rows = []
    for rel in composition:
        src = ROOT / rel
        if not src.is_file():
            continue
        dst = source / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        hs, hd = sha256_file(src), sha256_file(dst)
        if hs != hd:
            errors.append(f"copy hash mismatch: {rel}")
        composition_rows.append((hs, src.stat().st_size, rel))
    (out / "COMPOSITION_SHA256SUMS.txt").write_text(
        "".join(f"{h}  {rel}\n" for h, _, rel in composition_rows), encoding="utf-8")
    stage(chain, "03_HASH_AND_COPY", "PASS" if not any("hash mismatch" in e for e in errors) else "FAIL", {
        "repository_hashed_files": len(repo_rows), "composition_copied_files": len(composition_rows)
    })

    zip_path = out / "PROFILE_OS_EVIDENCE.zip"
    deterministic_zip(out, zip_path)
    zip_digest = sha256_file(zip_path)
    (out / "PROFILE_OS_EVIDENCE.zip.sha256").write_text(f"{zip_digest}  PROFILE_OS_EVIDENCE.zip\n", encoding="utf-8")
    zip_ok, zip_errors = verify_zip(zip_path, out)
    if not zip_ok: errors.extend(zip_errors)
    stage(chain, "04_ZIP_ROUND_TRIP", "PASS" if zip_ok else "FAIL", {"zip_sha256": zip_digest, "errors": zip_errors})

    token_states = [
      {"id":"TV-PROFILE-OS-REMOTE-CI-EXECUTION","from":"TOKEN_VAZIO_PENDING","to":"F_OK_RUNTIME_EVIDENCED" if identity_ok and validator_rc == tests_rc == 0 else "F_FAIL_RUNTIME","evidence":["STAGE_CHAIN.jsonl","validator.log","tests.log"],"claim_allowed":False},
      {"id":"TV-PROFILE-OS-CI-HASH-CUSTODY","from":"TOKEN_VAZIO_PENDING","to":"F_OK_RUNTIME_EVIDENCED" if len(composition_rows) == len(composition) and not missing and not untracked else "F_FAIL_RUNTIME","evidence":["COMPOSITION_SHA256SUMS.txt","REPOSITORY_TRACKED_SHA256SUMS.txt","TREE.json"],"claim_allowed":False},
      {"id":"TV-PROFILE-OS-CI-ZIP-INTEGRITY","from":"TOKEN_VAZIO_PENDING","to":"F_OK_RUNTIME_EVIDENCED" if zip_ok else "F_FAIL_RUNTIME","evidence":["PROFILE_OS_EVIDENCE.zip","PROFILE_OS_EVIDENCE.zip.sha256"],"claim_allowed":False},
      {"id":"TV-PROFILE-OS-CI-ARTIFACT-CUSTODY","from":"TOKEN_VAZIO_POST_RUN","to":"TOKEN_VAZIO_POST_RUN","evidence":[],"reason":"provider artifact ID/digest requires post-upload external readback","claim_allowed":False}
    ]
    with (out / "token-resolution.jsonl").open("w", encoding="utf-8") as f:
        for row in token_states: f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    blocking_bad = [x for x in token_states[:3] if x["to"] != "F_OK_RUNTIME_EVIDENCED"]
    passed = not errors and not blocking_bad
    result = {
        "schema":"RAFAELIA_PROFILE_OS_CI_GATE_RESULT_V1",
        "state":"PASS" if passed else "FAIL",
        "git_sha": checked_out_sha,
        "checked_out_sha": checked_out_sha,
        "expected_sha": expected_sha,
        "event_sha": event_sha,
        "source_identity_match": identity_ok,
        "run_id": os.getenv("GITHUB_RUN_ID", "LOCAL"),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT", "LOCAL"),
        "validator_exit": validator_rc,
        "tests_exit": tests_rc,
        "tracked_file_count": len(repo_rows),
        "composition_file_count": len(composition_rows),
        "zip_sha256": zip_digest,
        "errors": errors,
        "post_run_token":"TV-PROFILE-OS-CI-ARTIFACT-CUSTODY",
        "claim_allowed": False
    }
    write_json(out / "gate-result.json", result)
    stage(chain, "05_GATE_DECISION", result["state"], {"errors": errors, "checked_out_sha": checked_out_sha, "claim_allowed": False})
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if passed else 1

if __name__ == "__main__":
    raise SystemExit(main())
