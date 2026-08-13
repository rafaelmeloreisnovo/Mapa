#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

ALLOWED = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"}
IDENTITY = {"IDENTITY", "SENSOR_IDENTITY"}
SENSITIVE = {"IDENTITY", "SENSOR_IDENTITY", "PERSONAL", "SENSITIVE"}


def validate(doc):
    errors = []
    if not isinstance(doc, dict):
        return ["document must be object"]
    if doc.get("version") != 1:
        errors.append("version must be 1")
    if doc.get("claim_allowed") is not False:
        errors.append("claim_allowed must be false")
    items = doc.get("items")
    if not isinstance(items, list):
        return errors + ["items must be array"]

    seen = set()
    for i, item in enumerate(items):
        p = f"items[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{p} must be object")
            continue
        iid = item.get("id")
        if not isinstance(iid, str) or not iid.strip():
            errors.append(f"{p}.id required")
        elif iid in seen:
            errors.append(f"{p}.id duplicate:{iid}")
        else:
            seen.add(iid)

        cls = item.get("classification")
        if cls not in ALLOWED:
            errors.append(f"{p}.classification invalid")

        contains = item.get("contains")
        if not isinstance(contains, list):
            errors.append(f"{p}.contains must be array")
            contains = []
        kinds = set(contains)

        access = item.get("access_roles")
        if not isinstance(access, list):
            errors.append(f"{p}.access_roles must be array")
            access = []

        public = item.get("public_representation")
        if not isinstance(public, dict) or not isinstance(public.get("redacted"), bool):
            errors.append(f"{p}.public_representation.redacted required")
            public = {"redacted": False}

        if cls == "PUBLIC" and kinds & IDENTITY:
            errors.append(f"{p} PUBLIC cannot contain identity")
        if cls in {"INTERNAL", "CONFIDENTIAL", "RESTRICTED"} and not access:
            errors.append(f"{p} non-public requires access_roles")
        if kinds & SENSITIVE and public.get("redacted") is not True:
            errors.append(f"{p} sensitive public representation must be redacted")
    return errors


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ns = ap.parse_args(argv)
    try:
        doc = json.loads(Path(ns.input).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"REJECT input-error:{exc}")
        return 2
    errors = validate(doc)
    if errors:
        for e in errors:
            print("REJECT", e)
        return 1
    print("PASS privacy-classification-v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
