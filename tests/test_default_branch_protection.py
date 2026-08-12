#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("guard", ROOT / "tools" / "check_default_branch_protection.py")
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)

def expect(doc, code, needle):
    got, msg = guard.check(doc)
    assert got == code, (got, msg)
    assert needle in msg, (needle, msg)

def main():
    n = 0
    expect({"name":"main","protected":False,"protection":{"enabled":False,"required_status_checks":{"enforcement_level":"off"}}},3,"protected=false")
    print("PASS 1 current-risk fixture rejected"); n += 1
    expect({"name":"main","protected":True,"protection":{"enabled":False,"required_status_checks":{"enforcement_level":"non_admins"}}},4,"protection.enabled")
    print("PASS 2 inconsistent enabled flag rejected"); n += 1
    expect({"name":"main","protected":True,"protection":{"enabled":True}},5,"required_status_checks missing")
    print("PASS 3 missing status checks rejected"); n += 1
    expect({"name":"main","protected":True,"protection":{"enabled":True,"required_status_checks":{"enforcement_level":"off"}}},6,"enforcement off")
    print("PASS 4 checks-off fixture rejected"); n += 1
    expect({"name":"main","protected":True,"protection":{"enabled":True,"required_status_checks":{"enforcement_level":"non_admins"}}},0,"PASS branch main")
    print("PASS 5 protected fixture accepted"); n += 1
    print(f"PASS total={n}/5")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
