#!/usr/bin/env python3
"""Offline semantic falsifier: compare typed catalog contract to existing producer KOS.

No network, no private corpus, no normalization of original literals and no PASS
for provider/device gates. A zero exit proves only scoped checks of these files.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/biblioteconomia/federated_biblio_contract.v1.json"
DICTIONARY = ROOT / "data/semantics/semantic-dictionary.v1.jsonl"
ARITHMETIC = re.compile(r"^[0-9]+(?:[+*][0-9]+)*$")
FORBIDDEN_FIELDS = {
    "private_file_id", "private_folder_id", "raw_conversation",
    "raw_message", "conversation_id", "message_id", "oauth_token",
    "refresh_token", "access_token", "private_key", "secret_value",
}


def dictionary_rows(text: str) -> list[dict]:
    rows = []
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError("dictionary row %d not an object" % number)
        rows.append(row)
    return rows


def arithmetic(expression: str) -> int:
    """Evaluate only unsigned integer '+' and '*' with normal precedence."""
    if not ARITHMETIC.fullmatch(expression):
        raise ValueError("not an allowed integer expression")
    return sum(
        _product(piece.split("*"))
        for piece in expression.split("+")
    )


def _product(parts: list[str]) -> int:
    result = 1
    for token in parts:
        result *= int(token)
    return result


def analyze(contract: dict, rows: list[dict]) -> dict:
    errors: list[str] = []
    observations: list[dict] = []
    if not isinstance(contract, dict) or contract.get("claim_allowed") is not False:
        return {"errors": ["CLAIM_OR_CONTRACT_INVALID"], "observations": [], "claim_allowed": False}
    if contract.get("predecessor") != "data/biblioteconomia/novoexport_library_model.v1.json":
        errors.append("PREDECESSOR_IDENTITY_CHANGED")
    if contract.get("promotion", {}).get("auto_merge") is not False:
        errors.append("AUTO_MERGE_UNSAFE")
    if contract.get("publishing_policy", {}).get("raw_conversations") is not False:
        errors.append("RAW_CONVERSATION_PUBLICATION_UNSAFE")

    def walk(obj: object) -> None:
        if isinstance(obj, dict):
            for name, value in obj.items():
                if name.lower() in FORBIDDEN_FIELDS:
                    errors.append("PRIVATE_LOCATOR_OR_SECRET_KEY:%s" % name)
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)
    walk(contract)

    lexemes = contract.get("lexical_types", [])
    if not isinstance(lexemes, list):
        return {"errors": errors + ["LEXEMES_INVALID"], "observations": observations, "claim_allowed": False}
    seen = set()
    for lex in lexemes:
        if not isinstance(lex, dict) or not isinstance(lex.get("literal_utf8"), str):
            errors.append("LITERAL_MISSING")
            continue
        literal = lex["literal_utf8"]
        if literal in seen:
            errors.append("DUPLICATE_LITERAL:%s" % literal)
        seen.add(literal)
        points = lex.get("unicode_codepoints")
        if points is not None and points != ["U+%04X" % ord(char) for char in literal]:
            errors.append("CODEPOINT_MISMATCH:%s" % literal)
    if not {"§", "∆", "∅", "Π", "Ω", "★", "†", "‡", "4bit|4bit"}.issubset(seen):
        errors.append("REQUIRED_SYMBOL_ABSENT")
    math = contract.get("mathematical_checks")
    if not isinstance(math, list):
        errors.append("MATH_CHECKS_INVALID")
        math = []
    for row in math:
        if not isinstance(row, dict):
            errors.append("MATH_ROW_INVALID")
            continue
        literal = row.get("literal", "")
        if not isinstance(literal, str) or "=" not in literal:
            errors.append("MATH_LITERAL_INVALID")
            continue
        lhs, rhs = literal.split("=", 1)
        if lhs == "ceil(log2(1000))":
            actual = (1000 - 1).bit_length()  # exact integer proof
        else:
            try:
                actual = arithmetic(lhs)
            except ValueError:
                errors.append("MATH_UNSUPPORTED_EXPRESSION:%s" % lhs)
                continue
        try:
            declared = int(rhs)
        except ValueError:
            errors.append("MATH_RHS_INVALID")
            continue
        correct = actual == declared
        expect = row.get("expect")
        if correct and expect not in {"TRUE", "TRUE_ARITHMETIC_ONLY"}:
            errors.append("MATH_EXPECT_INCONSISTENT:%s" % literal)
        if not correct and not (
            literal == "70*7=14"
            and actual == 490
            and expect == "CONTRADICTION_490_NOT_14"
            and row.get("do_not_silently_correct") is True
        ):
            errors.append("MATH_FALSE_UNTYPED:%s" % literal)
        observations.append({
            "kind": "MATHEMATICAL_RECOMPUTATION", "literal": literal,
            "computed_lhs": actual, "claimed_rhs": declared,
            "state": "PROVED_ARITHMETIC" if correct else "FALSIFIED_AS_WRITTEN",
        })

    lookup = {row.get("entry_id"): row for row in rows}
    boundaries = contract.get("semantic_scope_collisions", [])
    if not isinstance(boundaries, list):
        boundaries = []
        errors.append("CROSS_SOURCE_COLLISIONS_MISSING")
    scope = {b.get("literal_utf8"): b for b in boundaries if isinstance(b, dict)}
    legacy_empty = lookup.get("SEM-EMPTY-001", {})
    empty = scope.get("∅", {})
    if not (
        legacy_empty.get("surface") == "∅"
        and "TOKEN_VAZIO" in legacy_empty.get("aliases", [])
        and empty.get("legacy_dictionary_id") == "SEM-EMPTY-001"
        and empty.get("state") == "POLYSEMY_TYPED_HOLD"
        and empty.get("do_not_merge_senses") is True
        and empty.get("resolution") == "REQUIRE_CONTEXT_AND_SOURCE"
    ):
        errors.append("EMPTY_SET_EPISTEMIC_COLLISION_UNBOUND")
    else:
        observations.append({
            "kind": "CROSS_SOURCE_POLYSEMY", "literal": "∅",
            "legacy_entry": "SEM-EMPTY-001", "state": "HOLD_TYPED",
            "meaning": "context required; not an equivalence",
        })
    legacy_delta = lookup.get("SEM-DELTA-001", {})
    delta = scope.get("∆", {})
    if not (
        legacy_delta.get("surface") == "Δ"
        and "∆" in legacy_delta.get("aliases", [])
        and delta.get("state") == "DISTINCT_CODEPOINTS_AUTHORIAL_ALIAS"
        and delta.get("do_not_normalize_without_evidence") is True
    ):
        errors.append("DELTA_ALIAS_UNBOUND")
    else:
        observations.append({
            "kind": "UNICODE_ALIAS", "literal": "∆",
            "legacy_entry": "SEM-DELTA-001", "state": "ALIAS_WITH_SCOPE",
            "meaning": "U+2206 and U+0394 preserved distinctly",
        })
    boundaries_state = contract.get("operational_state_boundaries", {})
    if not isinstance(boundaries_state, dict) or boundaries_state.get("claim_allowed") is not False:
        errors.append("STATE_BOUNDARY_UNSAFE")

    return {
        "schema": "rafaelia.biblio.offline-semantic-falsifier/v1",
        "claim_allowed": False,
        "offline_checks": "PASS_SCOPED" if not errors else "FAIL",
        "seven_directions": {
            "identity_provenance": "PASS_SCOPED_MODEL_ONLY" if not errors else "FAIL",
            "semantic_scope": "HOLD_TYPED_CONTEXT_REQUIRED",
            "data_privacy": "PASS_SCOPED_KEY_GUARD_ONLY" if not errors else "FAIL",
            "temporal_freshness": "TOKEN_VAZIO_LIVE_OBSERVATION",
            "academic_falsification": "PASS_SCOPED_INTEGER_AND_UNICODE" if not errors else "FAIL",
            "provider_ci_promotion": "HOLD_EXTERNAL_AUTHORITY",
            "android_arm32": "TOKEN_VAZIO_PHYSICAL_RECEIPT",
        },
        "observations": observations,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=CONTRACT)
    parser.add_argument("--dictionary", type=Path, default=DICTIONARY)
    args = parser.parse_args()
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
        rows = dictionary_rows(args.dictionary.read_text(encoding="utf-8"))
        result = analyze(contract, rows)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        result = {"claim_allowed": False, "offline_checks": "FAIL", "errors": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if result.get("offline_checks") == "PASS_SCOPED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
