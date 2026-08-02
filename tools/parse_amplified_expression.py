#!/usr/bin/env python3
"""Deterministic parser for the RAFAELIA amplified-expression mini-language."""

from __future__ import annotations
import json
import re
import sys
from typing import Any

REQUIRED_KEYS = {
    "D", "N", "DELTA_ROLE", "DELTA_VALUE", "OMEGA_NUM", "OMEGA_EPI",
    "PI_ROLE", "PHI_ROLE", "EQUIV", "FUNCTION"
}
ENUMS = {
    "DELTA_ROLE": {"ARITY", "SHIFT", "DIFFERENCE", "GRADIENT", "MUTATION"},
    "OMEGA_NUM": {"GEOMETRIC_MEAN", "PRODUCT", "DISABLED"},
    "OMEGA_EPI": {"TERNARY_FAIL_CLOSED"},
    "PI_ROLE": {"CIRCULAR_CONSTANT", "PHASE", "SYMBOLIC"},
    "PHI_ROLE": {"GOLDEN_RATIO", "WEIGHT", "SYMBOLIC"},
    "EQUIV": {"SYNTACTIC_IDENTITY", "NUMERIC_EQUAL", "APPROX_EQUAL", "RELATIONAL_EQUIVALENCE"},
    "FUNCTION": {"F_TRANSITION"},
}
PAIR_RE = re.compile(r"^([A-Z_]+)=(.+)$")

class ParseError(ValueError):
    pass

def parse_number(raw: str) -> int | float:
    if re.fullmatch(r"-?[0-9]+", raw):
        return int(raw)
    if re.fullmatch(r"-?(?:[0-9]+\.[0-9]*|\.[0-9]+)", raw):
        return float(raw)
    raise ParseError(f"invalid number: {raw}")

def parse_expression(text: str) -> dict[str, Any]:
    if not text.startswith("AMP{") or not text.endswith("}"):
        raise ParseError("expression must use AMP{...}")
    body = text[4:-1].strip()
    if not body:
        raise ParseError("empty expression")
    values: dict[str, str] = {}
    for part in body.split(";"):
        part = part.strip()
        match = PAIR_RE.fullmatch(part)
        if not match:
            raise ParseError(f"invalid field: {part}")
        key, value = match.groups()
        if key in values:
            raise ParseError(f"duplicate key: {key}")
        values[key] = value.strip()

    missing = REQUIRED_KEYS - values.keys()
    extra = values.keys() - REQUIRED_KEYS
    if missing:
        raise ParseError("missing keys: " + ",".join(sorted(missing)))
    if extra:
        raise ParseError("unknown keys: " + ",".join(sorted(extra)))

    for key, allowed in ENUMS.items():
        if values[key] not in allowed:
            raise ParseError(f"invalid {key}: {values[key]}")

    arity = parse_number(values["D"])
    iteration = parse_number(values["N"])
    delta_value = parse_number(values["DELTA_VALUE"])
    if not isinstance(arity, int) or not 1 <= arity <= 7:
        raise ParseError("D must be integer in [1,7]")
    if not isinstance(iteration, int) or not 0 <= iteration <= 1_000_000:
        raise ParseError("N must be integer in [0,1000000]")

    return {
        "schema": "rafaelia.amplified-expression.v1",
        "arity": arity,
        "iteration": iteration,
        "delta": {"role": values["DELTA_ROLE"], "value": delta_value},
        "omega": {"numeric": values["OMEGA_NUM"], "epistemic": values["OMEGA_EPI"]},
        "pi_role": values["PI_ROLE"],
        "phi_role": values["PHI_ROLE"],
        "equivalence": values["EQUIV"],
        "function": {
            "name": values["FUNCTION"],
            "signature": "F(input_state,parameters,evidence_context)->transition_result",
        },
        "claim_allowed": False,
    }

def canonical_json(ast: dict[str, Any]) -> str:
    return json.dumps(ast, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: parse_amplified_expression.py 'AMP{...}'", file=sys.stderr)
        return 2
    try:
        ast = parse_expression(argv[1])
    except ParseError as exc:
        print(f"PARSE_ERROR: {exc}", file=sys.stderr)
        return 1
    print(canonical_json(ast))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
