#!/usr/bin/env python3
import json, sys

REQUIRED = ("cycle_id", "artifact_role", "provider_id")

def validate(doc):
    errors = []
    seen = {}
    records = doc.get("records")
    if not isinstance(records, list):
        return ["records must be a list"]
    for i, rec in enumerate(records):
        if not isinstance(rec, dict):
            errors.append(f"records[{i}] must be object")
            continue
        missing = [k for k in REQUIRED if not isinstance(rec.get(k), str) or not rec.get(k).strip()]
        if missing:
            errors.append(f"records[{i}] missing/empty: {','.join(missing)}")
            continue
        key = (rec["cycle_id"], rec["artifact_role"])
        provider = rec["provider_id"]
        prior = seen.get(key)
        if prior is None:
            seen[key] = provider
        elif prior != provider:
            errors.append(
                f"conflicting provider for cycle_id={key[0]} artifact_role={key[1]}: {prior} != {provider}"
            )
    return errors

def main(path):
    with open(path, "r", encoding="utf-8") as f:
        doc = json.load(f)
    errors = validate(doc)
    if errors:
        for e in errors:
            print("REJECT", e)
        return 1
    print(f"PASS records={len(doc['records'])} unique_identity_keys={len({(r['cycle_id'],r['artifact_role']) for r in doc['records']})}")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_cycle_artifact_identity.py <json>", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
