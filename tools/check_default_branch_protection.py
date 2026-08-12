#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

def check(doc):
    if not isinstance(doc, dict):
        return 2, "REJECT branch metadata must be an object"
    name = doc.get("name")
    if not isinstance(name, str) or not name.strip():
        return 2, "REJECT missing branch name"
    if doc.get("protected") is not True:
        return 3, f"REJECT branch {name} protected=false"
    protection = doc.get("protection")
    if not isinstance(protection, dict) or protection.get("enabled") is not True:
        return 4, f"REJECT branch {name} protection.enabled!=true"
    checks = protection.get("required_status_checks")
    if not isinstance(checks, dict):
        return 5, f"REJECT branch {name} required_status_checks missing"
    if checks.get("enforcement_level") in (None, "", "off"):
        return 6, f"REJECT branch {name} status-check enforcement off"
    return 0, f"PASS branch {name} protection gate"

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("metadata_json")
    ns = p.parse_args(argv)
    try:
        doc = json.loads(Path(ns.metadata_json).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"REJECT unreadable metadata: {exc}")
        return 2
    code, msg = check(doc)
    print(msg)
    return code

if __name__ == "__main__":
    raise SystemExit(main())
