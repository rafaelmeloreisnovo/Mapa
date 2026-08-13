#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

ALLOWED_VISIBILITY = {"PUBLIC", "PRIVATE"}

def validate(doc):
    errors = []
    if not isinstance(doc, dict):
        return ["document must be object"]
    if doc.get("version") != 1:
        errors.append("version must be 1")
    if doc.get("claim_allowed") is not False:
        errors.append("claim_allowed must be false")
    if doc.get("default_policy") != "DENY":
        errors.append("default_policy must be DENY")
    items = doc.get("items")
    if not isinstance(items, list):
        return errors + ["items must be array"]
    seen = set()
    for i, item in enumerate(items):
        p = f"items[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{p} must be object")
            continue
        path = item.get("path")
        if not isinstance(path, str) or not path.strip():
            errors.append(f"{p}.path required")
        elif path in seen:
            errors.append(f"{p}.path duplicate:{path}")
        else:
            seen.add(path)
        visibility = item.get("visibility")
        if visibility not in ALLOWED_VISIBILITY:
            errors.append(f"{p}.visibility invalid")
        release_allowed = item.get("release_allowed")
        if not isinstance(release_allowed, bool):
            errors.append(f"{p}.release_allowed must be boolean")
            release_allowed = False
        review = item.get("review_receipt")
        if release_allowed and visibility != "PUBLIC":
            errors.append(f"{p} release_allowed requires PUBLIC visibility")
        if release_allowed and (not isinstance(review, str) or not review.strip()):
            errors.append(f"{p} release_allowed requires review_receipt")
    return errors

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ns = ap.parse_args(argv)
    try:
        doc = json.loads(Path(ns.manifest).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"REJECT input-error:{exc}")
        return 2
    errors = validate(doc)
    if errors:
        for e in errors:
            print("REJECT", e)
        return 1
    print("PASS release-boundary-v1")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
