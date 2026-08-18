#!/usr/bin/env python3
"""Stdlib-only semantic validator for RAFAELIA evidence receipts.

A receipt records what was observed/verified and what remains unknown. It does
not authorize a scientific claim. TOKEN_VAZIO must remain explicit whenever a
local digest has not been recomputed.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "rafaelia.evidence-receipt/v1"
RECEIPT_ID = re.compile(r"^evidence:[a-z0-9][a-z0-9._:-]{4,191}$")
HEX32 = re.compile(r"^[0-9a-fA-F]{32}$")
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(doc: Any) -> tuple[list[str], dict[str, Any]]:
    defects: list[str] = []
    if not isinstance(doc, dict):
        return ["document must be an object"], {}

    if doc.get("schema_version") != SCHEMA_VERSION:
        defects.append(f"schema_version must equal {SCHEMA_VERSION}")
    rid = doc.get("receipt_id")
    if not (_text(rid) and RECEIPT_ID.fullmatch(rid)):
        defects.append("receipt_id is invalid")
    if not _text(doc.get("observed_at")):
        defects.append("observed_at must be non-empty")
    if doc.get("claim_allowed") is not False:
        defects.append("evidence receipt must keep claim_allowed=false")

    chain = doc.get("source_chain")
    if not isinstance(chain, list) or not chain:
        defects.append("source_chain must contain at least one provenance hop")
        chain = []
    for i, hop in enumerate(chain):
        if not isinstance(hop, dict) or not all(_text(hop.get(k)) for k in ("role", "locator", "statement")):
            defects.append(f"source_chain[{i}] requires role, locator and statement")

    artifact = doc.get("artifact")
    if not isinstance(artifact, dict):
        defects.append("artifact must be an object")
        artifact = {}
    if not _text(artifact.get("name")):
        defects.append("artifact.name must be non-empty")

    published = artifact.get("publisher_checksum")
    if not isinstance(published, dict):
        defects.append("artifact.publisher_checksum must be an object")
        published = {}
    alg = published.get("algorithm")
    value = published.get("value")
    if not all(_text(published.get(k)) for k in ("algorithm", "value", "authority")):
        defects.append("publisher_checksum requires algorithm, value and authority")
    elif str(alg).lower() == "md5" and not HEX32.fullmatch(str(value)):
        defects.append("publisher MD5 must contain exactly 32 hexadecimal characters")
    elif str(alg).lower() in {"sha256", "sha-256"} and not HEX64.fullmatch(str(value)):
        defects.append("publisher SHA-256 must contain exactly 64 hexadecimal characters")

    local = artifact.get("local_sha256")
    if not isinstance(local, dict):
        defects.append("artifact.local_sha256 must be an object")
        local = {}
    local_state = local.get("state")
    local_value = local.get("value")
    if local_state == "TOKEN_VAZIO":
        if local_value is not None:
            defects.append("TOKEN_VAZIO local_sha256 requires value=null")
        if not _text(local.get("reason")) or not _text(local.get("next_test")):
            defects.append("TOKEN_VAZIO local_sha256 requires reason and next_test")
    elif local_state == "VERIFIED":
        if not (_text(local_value) and HEX64.fullmatch(str(local_value))):
            defects.append("VERIFIED local_sha256 requires a 64-hex digest")
        byte_length = local.get("byte_length")
        if byte_length is not None and (not isinstance(byte_length, int) or isinstance(byte_length, bool) or byte_length < 0):
            defects.append("local_sha256.byte_length must be a non-negative integer")
    else:
        defects.append("local_sha256.state must be TOKEN_VAZIO or VERIFIED")

    verification = doc.get("verification")
    if not isinstance(verification, dict) or not verification:
        defects.append("verification must be a non-empty object of booleans")
        verification = {}
    for key, flag in verification.items():
        if not isinstance(flag, bool):
            defects.append(f"verification.{key} must be boolean")

    downloaded = verification.get("binary_downloaded_locally")
    md5_local = verification.get("publisher_md5_recomputed_locally")
    sha_local = verification.get("sha256_computed_locally")
    if md5_local is True and downloaded is not True:
        defects.append("publisher_md5_recomputed_locally=true requires binary_downloaded_locally=true")
    if sha_local is True and downloaded is not True:
        defects.append("sha256_computed_locally=true requires binary_downloaded_locally=true")
    if sha_local is True and local_state != "VERIFIED":
        defects.append("sha256_computed_locally=true requires local_sha256.state=VERIFIED")
    if sha_local is False and local_state != "TOKEN_VAZIO":
        defects.append("sha256_computed_locally=false requires local_sha256.state=TOKEN_VAZIO")
    if local_state == "VERIFIED" and sha_local is not True:
        defects.append("local_sha256.state=VERIFIED requires sha256_computed_locally=true")

    for field in ("F_ok", "F_gap", "F_next", "F_esquecido"):
        items = doc.get(field)
        if not isinstance(items, list):
            defects.append(f"{field} must be an array")
            continue
        if field == "F_next" and not items:
            defects.append("F_next must contain at least one verifiable next step")
        for i, item in enumerate(items):
            if not _text(item):
                defects.append(f"{field}[{i}] must be non-empty text")

    anti = doc.get("anti_regression")
    if not isinstance(anti, dict):
        defects.append("anti_regression must be an object")
        anti = {}
    if anti.get("append_only") is not True:
        defects.append("anti_regression.append_only must be true")
    if not isinstance(anti.get("supersedes"), list):
        defects.append("anti_regression.supersedes must be an array")
    if not _text(anti.get("rule")):
        defects.append("anti_regression.rule must be non-empty")

    report = {
        "schema_version": SCHEMA_VERSION,
        "receipt_id": rid,
        "status": "PASS" if not defects else "FAIL",
        "source_hops": len(chain),
        "local_sha256_state": local_state,
        "claim_allowed": False,
        "defects": defects,
        "next_verifiable_step": (
            doc.get("F_next", [None])[0]
            if not defects and isinstance(doc.get("F_next"), list) and doc.get("F_next")
            else "Correct every defect before relying on this receipt."
        ),
    }
    return defects, report


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("receipt", type=Path)
    p.add_argument("--write-report", type=Path)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    doc = json.loads(args.receipt.read_text(encoding="utf-8"))
    defects, report = validate(doc)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if defects else 0


if __name__ == "__main__":
    raise SystemExit(main())
