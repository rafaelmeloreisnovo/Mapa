#!/usr/bin/env python3
import fcntl
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOC = ROOT / "tools" / "allocate_cycle_id.py"


def run(registry, cycle, role, provider):
    return subprocess.run(
        [sys.executable, str(ALLOC), str(registry), cycle, role, provider],
        text=True,
        capture_output=True,
        check=False,
    )


def load(registry):
    with open(registry, "r", encoding="utf-8") as f:
        return json.load(f)


def assert_true(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    passed = 0
    with tempfile.TemporaryDirectory() as td:
        registry = Path(td) / "registry.json"

        r1 = run(registry, "C38", "EXECUTIVE_RECEIPT", "provider-A")
        assert_true(r1.returncode == 0 and "allocated" in r1.stdout, (r1.returncode, r1.stdout, r1.stderr))
        print("PASS 1 first allocation")
        passed += 1

        r2 = run(registry, "C38", "EXECUTIVE_RECEIPT", "provider-A")
        assert_true(r2.returncode == 0 and "idempotent" in r2.stdout, (r2.returncode, r2.stdout, r2.stderr))
        print("PASS 2 idempotent replay")
        passed += 1

        r3 = run(registry, "C38", "EXECUTIVE_RECEIPT", "provider-B")
        assert_true(r3.returncode != 0 and "conflicting-provider" in r3.stdout, (r3.returncode, r3.stdout, r3.stderr))
        print("PASS 3 conflicting provider rejected")
        passed += 1

        doc = load(registry)
        assert_true(len(doc["records"]) == 1 and doc["records"][0]["provider_id"] == "provider-A", doc)
        print("PASS 4 registry unchanged after conflict")
        passed += 1

    with tempfile.TemporaryDirectory() as td:
        registry = Path(td) / "race.json"

        def contender(provider):
            return run(registry, "C39", "EXECUTIVE_RECEIPT", provider)

        with ThreadPoolExecutor(max_workers=2) as ex:
            results = list(ex.map(contender, ["provider-X", "provider-Y"]))
        allocated = [r for r in results if r.returncode == 0 and "allocated" in r.stdout]
        rejected_or_serialized = [r for r in results if r.returncode != 0 or "idempotent" in r.stdout]
        assert_true(len(allocated) == 1 and len(rejected_or_serialized) == 1, [(r.returncode, r.stdout, r.stderr) for r in results])
        doc = load(registry)
        assert_true(len(doc["records"]) == 1, doc)
        print("PASS 5 concurrent conflicting providers -> exactly one allocation")
        passed += 1

    with tempfile.TemporaryDirectory() as td:
        registry = Path(td) / "malformed.json"
        registry.write_text('{"records":[{"cycle_id":"C1","artifact_role":"R","provider_id":"A"},{"cycle_id":"C1","artifact_role":"R","provider_id":"B"}]}\n', encoding="utf-8")
        r = run(registry, "C2", "R", "C")
        assert_true(r.returncode != 0 and "existing conflicting provider" in r.stdout, (r.returncode, r.stdout, r.stderr))
        print("PASS 6 pre-existing conflicting registry fails closed")
        passed += 1

    with tempfile.TemporaryDirectory() as td:
        registry = Path(td) / "live.json"
        lock = Path(str(registry) + ".lock")
        with lock.open("a+", encoding="utf-8") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            r = run(registry, "C41", "EXECUTIVE_RECEIPT", "provider-live")
            assert_true(r.returncode == 3 and "lock-busy" in r.stdout, (r.returncode, r.stdout, r.stderr))
        assert_true(not registry.exists(), registry)
        print("PASS 7 live owner is never stolen")
        passed += 1

    with tempfile.TemporaryDirectory() as td:
        registry = Path(td) / "orphan.json"
        lock = Path(str(registry) + ".lock")
        helper = (
            "import fcntl,os,sys; "
            "p=sys.argv[1]; f=open(p,'a+'); "
            "fcntl.flock(f.fileno(),fcntl.LOCK_EX); "
            "f.write('orphan\\n'); f.flush(); os.fsync(f.fileno()); os._exit(0)"
        )
        h = subprocess.run([sys.executable, "-c", helper, str(lock)], capture_output=True, text=True, check=False)
        assert_true(h.returncode == 0 and lock.exists(), (h.returncode, h.stdout, h.stderr))
        r = run(registry, "C41", "EXECUTIVE_RECEIPT", "provider-orphan")
        assert_true(r.returncode == 0 and "allocated" in r.stdout, (r.returncode, r.stdout, r.stderr))
        doc = load(registry)
        assert_true(doc["records"][0]["provider_id"] == "provider-orphan", doc)
        print("PASS 8 orphaned lock file recovers after kernel releases owner lock")
        passed += 1

    with tempfile.TemporaryDirectory() as td:
        registry = Path(td) / "replay.json"
        r1 = run(registry, "C41", "ROOT", "provider-Z")
        r2 = run(registry, "C41", "ROOT", "provider-Z")
        assert_true(r1.returncode == 0 and "allocated" in r1.stdout, (r1.returncode, r1.stdout, r1.stderr))
        assert_true(r2.returncode == 0 and "idempotent" in r2.stdout, (r2.returncode, r2.stdout, r2.stderr))
        print("PASS 9 idempotent replay survives persistent lock-file design")
        passed += 1

    print(f"PASS total={passed}/9")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
