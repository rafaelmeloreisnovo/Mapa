#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "validate_release_boundary.py"
spec = importlib.util.spec_from_file_location("validator", TOOL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def manifest():
    return {
        "version": 1,
        "claim_allowed": False,
        "default_policy": "DENY",
        "items": [{
            "path": "docs/public/README.md",
            "visibility": "PUBLIC",
            "release_allowed": True,
            "review_receipt": "receipt-public-readme"
        }]
    }

def expect(name, doc, ok):
    errors = mod.validate(doc)
    assert (not errors) == ok, (name, errors)
    print("PASS", name)

def main():
    expect("valid-public-reviewed", manifest(), True)
    x = manifest(); x["default_policy"] = "ALLOW"
    expect("default-allow-rejected", x, False)
    x = manifest(); x["items"][0]["visibility"] = "PRIVATE"
    expect("private-release-rejected", x, False)
    x = manifest(); x["items"][0]["review_receipt"] = ""
    expect("release-without-review-rejected", x, False)
    x = manifest(); x["items"][0]["release_allowed"] = False
    expect("explicit-deny-accepted", x, True)
    x = manifest(); x["claim_allowed"] = True
    expect("claim-allowed-true-rejected", x, False)
    x = manifest(); x["items"].append(dict(x["items"][0]))
    expect("duplicate-path-rejected", x, False)
    print("PASS 7/7")

if __name__ == "__main__":
    main()
