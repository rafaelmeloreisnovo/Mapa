#!/usr/bin/env python3
"""Deterministic bulk harness for RAFAELIA E1-PARSER-v1.

Input: UTF-8 TSV with header containing at least
Representative Shard, Representative ID, Representative Expression,
Representative SHA256.

The harness verifies the provider-frozen E0 digest for every row before parsing,
requires unique input digests, emits one disposition per identity, and writes a
canonical aggregate receipt. It does not perform E2 equivalence or scientific
claim promotion.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import pathlib
import sys
import unicodedata

EXPECTED_COLUMNS = (
    "Representative Shard",
    "Representative ID",
    "Representative Expression",
    "Representative SHA256",
)
EXPECTED_COUNT_DEFAULT = 356


def sha256_text(s: str) -> str:
    return hashlib.sha256(unicodedata.normalize("NFC", s.strip()).encode("utf-8")).hexdigest()


def canonical(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_parser(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location("omega_math_e1_parser_v1", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("PARSER_LOAD_FAILURE")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_tsv", type=pathlib.Path)
    ap.add_argument("--parser", type=pathlib.Path, default=pathlib.Path(__file__).with_name("omega_math_e1_parser_v1.py"))
    ap.add_argument("--expected-count", type=int, default=EXPECTED_COUNT_DEFAULT)
    ap.add_argument("--output-jsonl", type=pathlib.Path, required=True)
    ap.add_argument("--receipt-json", type=pathlib.Path, required=True)
    args = ap.parse_args()

    parser = load_parser(args.parser)
    rows = []
    with args.input_tsv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        if reader.fieldnames is None or any(c not in reader.fieldnames for c in EXPECTED_COLUMNS):
            raise SystemExit("INPUT_SCHEMA_MISMATCH")
        for row in reader:
            expr = row["Representative Expression"]
            declared = row["Representative SHA256"].lower()
            actual = sha256_text(expr)
            if actual != declared:
                raise SystemExit(f"E0_DIGEST_MISMATCH:{row['Representative ID']}:{declared}:{actual}")
            result = parser.parse_expression(expr)
            if result["input_expression_digest"] != declared:
                raise SystemExit(f"PARSER_INPUT_DIGEST_MISMATCH:{row['Representative ID']}")
            rows.append({
                "shard": row["Representative Shard"],
                "representative_id": row["Representative ID"],
                "representative_sha256": declared,
                "disposition": result["disposition"],
                "ast_digest": result["ast_digest"],
                "typed_failure_code": result["typed_failure_code"],
                "contract_version": result["contract_version"],
                "implementation_version": result["implementation_version"],
            })

    if len(rows) != args.expected_count:
        raise SystemExit(f"CARDINALITY_MISMATCH:{len(rows)}!={args.expected_count}")
    digests = [r["representative_sha256"] for r in rows]
    if len(set(digests)) != len(digests):
        raise SystemExit("DUPLICATE_E0_IDENTITY_IN_INPUT")

    rows.sort(key=lambda r: r["representative_sha256"])
    output_bytes = "".join(canonical(r) + "\n" for r in rows).encode("utf-8")
    args.output_jsonl.write_bytes(output_bytes)

    disposition_counts = {}
    failure_counts = {}
    for r in rows:
        disposition_counts[r["disposition"]] = disposition_counts.get(r["disposition"], 0) + 1
        if r["typed_failure_code"]:
            failure_counts[r["typed_failure_code"]] = failure_counts.get(r["typed_failure_code"], 0) + 1

    receipt = {
        "schema": "RAFAELIA_E1_BULK_RECEIPT_V1",
        "claim_allowed": False,
        "input_count": len(rows),
        "unique_e0_sha256": len(set(digests)),
        "contract_version": parser.CONTRACT_VERSION,
        "implementation_version": parser.IMPLEMENTATION_VERSION,
        "parser_sha256": hashlib.sha256(args.parser.read_bytes()).hexdigest(),
        "input_tsv_sha256": hashlib.sha256(args.input_tsv.read_bytes()).hexdigest(),
        "output_jsonl_sha256": hashlib.sha256(output_bytes).hexdigest(),
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "typed_failure_counts": dict(sorted(failure_counts.items())),
        "closure_gate": "input_count == unique_e0_sha256 == 356 and exactly one deterministic disposition per E0 identity",
        "boundary": "E1 syntax-only reproduction; typed parse failure is an allowed disposition; no E2/domain/scientific promotion",
    }
    args.receipt_json.write_text(canonical(receipt) + "\n", encoding="utf-8")
    print(canonical(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
