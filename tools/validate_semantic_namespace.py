#!/usr/bin/env python3
import json
import sys
from pathlib import Path

CORE = {"ZERO", "NOOP", "VOID", "TOKEN_VAZIO", "EMPTY", "NULL"}


def die(msg):
    print(json.dumps({"status": "FAIL", "error": msg, "claim_allowed": False}, sort_keys=True))
    raise SystemExit(1)


doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
terms = doc.get("terms")
if not isinstance(terms, list):
    die("terms must be array")

tokens = [row.get("token") for row in terms]
if set(tokens) != CORE or len(tokens) != len(CORE):
    die("core namespace must contain each required token exactly once")

for row in terms:
    equivalent = set(row.get("equivalent_to", []))
    forbidden = equivalent & (CORE - {row["token"]})
    if forbidden:
        die(f"forbidden core semantic collapse {row['token']} -> {sorted(forbidden)}")
    if row["token"] == "TOKEN_VAZIO" and "zero" in row.get("meaning", "").lower() and "never" not in row.get("meaning", "").lower():
        die("TOKEN_VAZIO definition may not coerce to zero")

print(json.dumps({"status": "PASS", "tokens": sorted(CORE), "semantic_collapses": 0, "claim_allowed": False}, sort_keys=True))
