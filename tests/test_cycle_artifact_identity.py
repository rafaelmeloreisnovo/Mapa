#!/usr/bin/env python3
import copy, json, pathlib, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/governance/cycle-artifact-identity.c32-c36.v1.json"
VALIDATOR = ROOT / "tools/validate_cycle_artifact_identity.py"

def run(doc):
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as f:
        json.dump(doc, f)
        p = f.name
    r = subprocess.run([sys.executable, str(VALIDATOR), p], capture_output=True, text=True)
    pathlib.Path(p).unlink(missing_ok=True)
    return r.returncode, r.stdout + r.stderr

base = json.loads(MANIFEST.read_text(encoding="utf-8"))
cases = []
cases.append(("baseline", base, 0))

same = copy.deepcopy(base)
same["records"].append(copy.deepcopy(base["records"][1]))
cases.append(("idempotent_same_provider_alias", same, 0))

distinct = copy.deepcopy(base)
distinct["records"].append({
    "cycle_id":"OMEGA-ANTI-REGRESSION-C33",
    "artifact_role":"ANOTHER_EXPLICIT_ROLE",
    "provider_id":"provider-distinct-role"
})
cases.append(("distinct_role_same_cycle", distinct, 0))

conflict = copy.deepcopy(base)
bad = copy.deepcopy(base["records"][1]); bad["provider_id"] = "CONFLICTING_PROVIDER"
conflict["records"].append(bad)
cases.append(("conflicting_provider_same_cycle_role", conflict, 1))

for missing_key in ("cycle_id","artifact_role","provider_id"):
    bad = copy.deepcopy(base)
    bad["records"].append({"cycle_id":"CXX","artifact_role":"ROLE","provider_id":"P"})
    bad["records"][-1][missing_key] = ""
    cases.append((f"missing_{missing_key}", bad, 1))

failed = 0
for name, doc, expected in cases:
    code, out = run(doc)
    ok = code == expected
    print(("PASS" if ok else "FAIL"), name, f"exit={code}", out.strip().splitlines()[0] if out.strip() else "")
    failed += not ok

print(f"SUMMARY total={len(cases)} failed={failed}")
raise SystemExit(1 if failed else 0)
