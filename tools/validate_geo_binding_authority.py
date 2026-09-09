#!/usr/bin/env python3
import json
import sys
from pathlib import Path

SCHEMA_VERSION = "rafaelia.geo-binding-authority/v1"
BITOMEGA = {
    0: "NEG",
    1: "ZERO",
    2: "POS",
    3: "MIX",
    4: "VOID",
    5: "EDGE",
    6: "FLOW",
    7: "LOCK",
    8: "NOISE",
    9: "META",
}


def fail(msg):
    print(json.dumps({"status": "FAIL", "error": msg, "runtime_binding_allowed": False, "claim_allowed": False}, sort_keys=True))
    raise SystemExit(1)


def validate(doc):
    if not isinstance(doc, dict):
        fail("root must be object")
    if doc.get("schema_version") != SCHEMA_VERSION:
        fail("schema_version mismatch")
    if doc.get("claim_allowed") is not False:
        fail("claim_allowed must remain false")
    if not isinstance(doc.get("authority_id"), str) or not doc["authority_id"]:
        fail("authority_id required")
    if doc.get("status") not in {"TOKEN_VAZIO", "EVIDENCED", "REJECTED"}:
        fail("invalid status")
    refs = doc.get("source_refs")
    if not isinstance(refs, list) or not refs or any(not isinstance(x, str) or not x for x in refs):
        fail("source_refs must be non-empty strings")
    mapping = doc.get("mapping")
    if not isinstance(mapping, list) or len(mapping) > 10:
        fail("mapping must be array of at most 10 rows")

    raf_seen = set()
    omega_seen = set()
    for i, row in enumerate(mapping):
        if not isinstance(row, dict):
            fail(f"mapping[{i}] must be object")
        rs = row.get("rafbit_state")
        oc = row.get("bitomega_code")
        symbol = row.get("bitomega_symbol")
        if not isinstance(rs, int) or not 0 <= rs <= 9:
            fail(f"mapping[{i}].rafbit_state out of range")
        if not isinstance(oc, int) or not 0 <= oc <= 9:
            fail(f"mapping[{i}].bitomega_code out of range")
        if symbol != BITOMEGA[oc]:
            fail(f"mapping[{i}] BitOmega code/symbol mismatch")
        if rs in raf_seen:
            fail(f"duplicate rafbit_state {rs}")
        if oc in omega_seen:
            fail(f"duplicate bitomega_code {oc}")
        raf_seen.add(rs)
        omega_seen.add(oc)
        if not isinstance(row.get("rafbit_label"), str) or not row["rafbit_label"]:
            fail(f"mapping[{i}].rafbit_label required")
        basis = row.get("semantic_basis")
        if not isinstance(basis, str) or not basis or basis == "TOKEN_VAZIO":
            fail(f"mapping[{i}].semantic_basis must be evidenced text")
        erefs = row.get("evidence_refs")
        if not isinstance(erefs, list) or not erefs or any(not isinstance(x, str) or not x for x in erefs):
            fail(f"mapping[{i}].evidence_refs required")

    status = doc["status"]
    exact = doc.get("exact")
    receipt = doc.get("authority_receipt_ref")
    if not isinstance(receipt, str) or not receipt:
        fail("authority_receipt_ref required")

    runtime_allowed = False
    classification = "STRUCTURALLY_VALID_NON_PROMOTABLE"
    if status == "EVIDENCED":
        if exact is not True:
            fail("EVIDENCED authority requires exact=true")
        if len(mapping) != 10 or raf_seen != set(range(10)) or omega_seen != set(range(10)):
            fail("EVIDENCED authority requires exact 10x10 bijection")
        if receipt == "TOKEN_VAZIO":
            fail("EVIDENCED authority requires non-empty receipt reference")
        runtime_allowed = True
        classification = "VALID_EVIDENCED_AUTHORITY_INPUT"
    elif status == "TOKEN_VAZIO":
        if exact is not False:
            fail("TOKEN_VAZIO authority requires exact=false")
        runtime_allowed = False
        classification = "VALID_TOKEN_VAZIO_NO_RUNTIME_BINDING"
    else:
        runtime_allowed = False
        classification = "VALID_REJECTED_NO_RUNTIME_BINDING"

    return {
        "status": "PASS",
        "classification": classification,
        "runtime_binding_allowed": runtime_allowed,
        "mapping_rows": len(mapping),
        "claim_allowed": False,
    }


def main():
    if len(sys.argv) != 2:
        fail("usage: validate_geo_binding_authority.py <input.json>")
    path = Path(sys.argv[1])
    doc = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(validate(doc), sort_keys=True))


if __name__ == "__main__":
    main()
