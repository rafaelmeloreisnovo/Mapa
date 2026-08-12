#!/usr/bin/env python3
import argparse, json

SUCCESS = {"success", "neutral", "skipped"}

def completed_successes(payload):
    out = {}
    for run in payload.get("check_runs", []):
        name = run.get("name")
        status = run.get("status")
        conclusion = run.get("conclusion")
        if not name or status != "completed":
            continue
        out.setdefault(name, []).append(conclusion)
    return {name for name, conclusions in out.items()
            if conclusions and all(c in SUCCESS for c in conclusions)}

def choose(base, head, requested=None):
    shared = sorted(completed_successes(base) & completed_successes(head))
    if requested:
        if requested not in shared:
            raise ValueError(f"context-not-green-on-both:{requested}")
        return requested
    if len(shared) != 1:
        raise ValueError(f"expected-exactly-one-shared-green-context:found={shared}")
    return shared[0]

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-json", required=True)
    ap.add_argument("--head-json", required=True)
    ap.add_argument("--context")
    ns = ap.parse_args(argv)
    try:
        with open(ns.base_json, encoding="utf-8") as f:
            base = json.load(f)
        with open(ns.head_json, encoding="utf-8") as f:
            head = json.load(f)
        context = choose(base, head, ns.context)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(f"REJECT {e}")
        return 1
    print(f"PASS context={context}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
