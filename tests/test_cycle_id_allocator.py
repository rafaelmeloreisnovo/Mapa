#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

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
        winners = [r for r in results if r.returncode == 0 and "allocated" in r.stdout]
        rejected = [r for r in results if r.returncode != 0]
        assert_true(len(winners) == 1 and len(rejected) == 1, [(r.returncode, r.stdout, r.stderr) for r in results])
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

    print(f"PASS total={passed}/6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
