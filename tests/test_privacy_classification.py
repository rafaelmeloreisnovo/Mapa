#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "validate_privacy_classification.py"
spec = importlib.util.spec_from_file_location("validator", TOOL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def base_item():
    return {
        "id": "item-1",
        "classification": "CONFIDENTIAL",
        "contains": ["PERSONAL"],
        "access_roles": ["privacy-reviewer"],
        "public_representation": {"redacted": True},
    }


def doc(item=None):
    return {"version": 1, "claim_allowed": False, "items": [item or base_item()]}


def expect(name, document, ok):
    errors = mod.validate(document)
    assert (not errors) == ok, (name, errors)
    print("PASS", name)


def main():
    expect("valid-confidential", doc(), True)

    x = doc(); del x["items"][0]["classification"]
    expect("missing-classification", x, False)

    x = doc(); x["items"][0]["classification"] = "SECRET"
    expect("invalid-classification", x, False)

    x = doc(); x["items"][0]["public_representation"]["redacted"] = False
    expect("unredacted-sensitive-public-view", x, False)

    x = doc(); x["items"][0]["access_roles"] = []
    expect("nonpublic-without-access-policy", x, False)

    x = doc(); x["items"][0].update({"classification": "PUBLIC", "contains": ["IDENTITY"], "access_roles": []})
    expect("public-containing-identity", x, False)

    x = doc(); x["items"].append(dict(x["items"][0]))
    expect("duplicate-id", x, False)

    x = doc(); x["claim_allowed"] = True
    expect("claim-allowed-true-rejected", x, False)

    print("PASS 8/8")


if __name__ == "__main__":
    main()
