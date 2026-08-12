#!/usr/bin/env python3
import importlib.util, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_default_branch_pr_provenance.py"
spec = importlib.util.spec_from_file_location("gate", TOOL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS", name)

def main():
    branch = {"name": "main", "commit": {"sha": "abc"}, "protected": False}
    ok, msg = mod.evaluate(branch, [])
    check("empty PR association rejected", (not ok) and "no-merged-pr-provenance" in msg)
    ok, _ = mod.evaluate(branch, [{"number": 1, "merged_at": None, "base": {"ref": "main"}}])
    check("open PR rejected", not ok)
    ok, _ = mod.evaluate(branch, [{"number": 2, "merged_at": "2026-08-12T00:00:00Z", "base": {"ref": "dev"}}])
    check("merged PR targeting other branch rejected", not ok)
    ok, msg = mod.evaluate(branch, [{"number": 3, "merged_at": "2026-08-12T00:00:00Z", "base": {"ref": "main"}}])
    check("merged PR targeting default branch accepted", ok and "prs=3" in msg)
    ok, _ = mod.evaluate({"name": "main", "commit": {}}, [])
    check("missing commit SHA rejected", not ok)
    ok, _ = mod.evaluate(branch, {"not": "list"})
    check("invalid pulls payload rejected", not ok)
    print("PASS 6/6")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
