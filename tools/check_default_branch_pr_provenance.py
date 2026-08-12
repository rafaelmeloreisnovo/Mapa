#!/usr/bin/env python3
import argparse, json

def evaluate(branch, pulls):
    commit = ((branch or {}).get("commit") or {}).get("sha")
    if not commit:
        return False, "REJECT missing-default-branch-sha"
    if not isinstance(pulls, list):
        return False, "REJECT invalid-pulls-payload"
    merged = []
    for pr in pulls:
        if not isinstance(pr, dict):
            continue
        if pr.get("merged_at") and ((pr.get("base") or {}).get("ref") == branch.get("name")):
            merged.append(pr)
    if not merged:
        return False, f"REJECT no-merged-pr-provenance commit={commit}"
    nums = ",".join(str(pr.get("number", "?")) for pr in merged)
    return True, f"PASS merged-pr-provenance commit={commit} prs={nums}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--branch-json", required=True)
    ap.add_argument("--pulls-json", required=True)
    a = ap.parse_args()
    try:
        with open(a.branch_json, encoding="utf-8") as f:
            branch = json.load(f)
        with open(a.pulls_json, encoding="utf-8") as f:
            pulls = json.load(f)
    except Exception as exc:
        print(f"REJECT input-error {exc}")
        return 2
    ok, msg = evaluate(branch, pulls)
    print(msg)
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
