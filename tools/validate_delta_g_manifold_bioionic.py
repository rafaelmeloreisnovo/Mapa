#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ALLOWED_STATUS = {"PASS_EXTERNAL", "CORRECTED", "HYPOTHESIS", "TOKEN_VAZIO", "BLOCKED"}
NONPROMOTABLE = {"CORRECTED", "HYPOTHESIS", "TOKEN_VAZIO", "BLOCKED"}
REQUIRED = {"id", "statement", "status", "claim_allowed", "source_class", "falsifier", "quantity_types"}

def load_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def validate_rows(rows):
    errors = []
    seen = set()
    for idx, row in enumerate(rows, 1):
        missing = REQUIRED - row.keys()
        if missing:
            errors.append(f"row {idx}: missing {sorted(missing)}")
            continue
        rid = row["id"]
        if rid in seen:
            errors.append(f"{rid}: duplicate id")
        seen.add(rid)
        if row["status"] not in ALLOWED_STATUS:
            errors.append(f"{rid}: invalid status {row['status']}")
        if row["status"] in NONPROMOTABLE and row["claim_allowed"]:
            errors.append(f"{rid}: {row['status']} cannot be claim_allowed")
        if not isinstance(row["quantity_types"], list):
            errors.append(f"{rid}: quantity_types must be a list")
        if row.get("identity_collapse", False):
            errors.append(f"{rid}: identity_collapse=true is forbidden")
        if row.get("shannon_equals_thermo", False):
            errors.append(f"{rid}: Shannon entropy cannot be asserted identical to thermodynamic entropy")
        if row.get("physiologic_mv_equals_ionizing", False):
            errors.append(f"{rid}: physiological mV cannot be asserted equivalent to ionizing radiation")
        if not row["falsifier"]:
            errors.append(f"{rid}: falsifier is required")
    return errors

def main(argv=None):
    argv = argv or sys.argv[1:]
    path = Path(argv[0] if argv else "data/claims/delta_g_manifold_bioionic_v1.jsonl")
    rows = load_jsonl(path)
    errors = validate_rows(rows)
    if errors:
        for error in errors:
            print("FAIL", error)
        return 1
    print(f"PASS {path} rows={len(rows)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
