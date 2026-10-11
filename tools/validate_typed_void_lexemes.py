#!/usr/bin/env python3
"""Bounded synthetic lexeme witnesses for the existing RAFAELIA typed-void lattice.

Never infer missing values from glyph similarity. No network, mutable external
state, raw private data, runtime secrets, or unbounded parse input.
"""
from __future__ import annotations
import argparse
import ast
import json
from pathlib import Path
from typing import Any

FIXTURES = Path(__file__).resolve().parents[1] / "data/semantics/typed-void-lexical-fixtures.v1.json"
KINDS = {"PRESENT", "EMPTY_SET", "EMPTY_STRING", "TOKEN_VAZIO",
         "NULL_LITERAL", "NUMERIC_ZERO", "MISSING_FIELD"}


def classify(record: dict[str, Any]) -> dict[str, Any]:
    """Classify only declared syntax/domain, keeping the exact lexeme separate."""
    syntax, domain = record.get("syntax"), record.get("domain")
    present = "raw" in record
    raw = record.get("raw")
    if not present:
        kind = "MISSING_FIELD" if (syntax, domain) == ("object_key", "object") else "TOKEN_VAZIO"
        return dict(kind=kind, observed=False, source_present=False, codepoints=None,
                    parsed_length=None, parsed_value=None,
                    reason="KEY_NOT_PRESENT" if kind == "MISSING_FIELD" else "NO_RAW_WITNESS")
    if not isinstance(raw, str):
        return dict(kind="TOKEN_VAZIO", observed=True, source_present=True, codepoints=None,
                    parsed_length=None, parsed_value=None, reason="NON_STRING_RAW_LEXEME")
    result = dict(kind="TOKEN_VAZIO", observed=True, source_present=True,
                  codepoints=[f"U+{ord(c):04X}" for c in raw], parsed_length=None,
                  parsed_value=None, reason="GRAMMAR_UNRESOLVED")
    if len(raw) > 4096:
        result["reason"] = "RAW_LEXEME_EXCEEDS_BOUND"
        return result
    if (syntax, domain) == ("set_theory", "set") and raw == "∅":
        result.update(kind="EMPTY_SET", parsed_length=0, parsed_value=[],
                      reason="DECLARED_SET_THEORY")
    elif (syntax, domain) == ("observed_string", "text"):
        result.update(kind="EMPTY_STRING" if raw == "" else "PRESENT", parsed_length=len(raw),
                      parsed_value=raw, reason="SOURCE_STRING_VALUE")
    elif (syntax, domain) == ("json_string", "text"):
        try:
            val = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            result["reason"] = "INVALID_JSON_STRING_LITERAL"
        else:
            if isinstance(val, str) and raw.startswith('"') and raw.endswith('"'):
                result.update(kind="EMPTY_STRING" if val == "" else "PRESENT", parsed_length=len(val),
                              parsed_value=val, reason="VALID_JSON_STRING_LITERAL")
            else:
                result["reason"] = "NOT_A_JSON_STRING_LITERAL"
    elif (syntax, domain) == ("python_string", "text"):
        try:
            val = ast.literal_eval(raw)
        except (SyntaxError, ValueError, TypeError, MemoryError, RecursionError):
            result["reason"] = "INVALID_PYTHON_STRING_LITERAL"
        else:
            if isinstance(val, str):
                result.update(kind="EMPTY_STRING" if val == "" else "PRESENT", parsed_length=len(val),
                              parsed_value=val, reason="VALID_PYTHON_STRING_LITERAL")
            else:
                result["reason"] = "NOT_A_PYTHON_STRING_LITERAL"
    elif (syntax, domain) == ("semicolon_fields", "delimited_text"):
        parts = raw.split(";")
        result.update(kind="PRESENT", parsed_length=len(parts), parsed_value=parts,
                      reason="EXPLICIT_DELIMITED_SLOTS_NOT_MISSING_KEYS")
    elif (syntax, domain) == ("json_null", "json") and raw == "null":
        result.update(kind="NULL_LITERAL", parsed_length=len(raw),
                      reason="EXPLICIT_JSON_NULL_SENTINEL")
    elif (syntax, domain) == ("json_number", "number") and raw == "0":
        result.update(kind="NUMERIC_ZERO", parsed_length=1, parsed_value=0,
                      reason="EXACT_DECLARED_NUMERIC_ZERO")
    elif (syntax, domain) == ("symbolic", "symbolic") and raw == "⁰":
        result.update(parsed_length=1, reason="SYMBOLIC_SUPERSCRIPT_ZERO_NOT_NUMERIC")
    elif syntax == "free_text":
        result.update(parsed_length=len(raw), reason="UNBOUND_FREE_TEXT_HAS_NO_DECLARED_TYPE")
    else:
        result.update(parsed_length=len(raw), reason="NO_VALID_PARSE_IN_DECLARED_GRAMMAR")
    return result


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "rafaelia.typed-void-lexical-fixtures/v1" or data.get("claim_allowed") is not False:
        errors.append("INVALID_FIXTURE_SCOPE_OR_CLAIM")
    seen: set[str] = set()
    for n, item in enumerate(data.get("cases", [])):
        if not isinstance(item, dict):
            errors.append(f"CASE_{n}_NOT_OBJECT")
            continue
        case_id = item.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            errors.append(f"CASE_{n}_MISSING_OR_DUPLICATE_ID")
            continue
        seen.add(case_id)
        result = classify(item)
        if result["kind"] not in KINDS or result["kind"] != item.get("expected_kind"):
            errors.append(f"{case_id}_KIND_MISMATCH")
        if item.get("expected_length") != result["parsed_length"]:
            raw = item.get("raw")
            # For unresolved symbols the expected length is the observed lexeme length.
            if not (result["kind"] == "TOKEN_VAZIO" and isinstance(raw, str)
                    and len(raw) == item.get("expected_length")):
                errors.append(f"{case_id}_LENGTH_MISMATCH")
        if "expected_value" in item and (
            type(result["parsed_value"]) is not type(item["expected_value"])
            or result["parsed_value"] != item["expected_value"]
        ):
            errors.append(f"{case_id}_VALUE_MISMATCH")
        if "raw" in item and isinstance(item["raw"], str) and result["codepoints"] != [
            f"U+{ord(c):04X}" for c in item["raw"]
        ]:
            errors.append(f"{case_id}_CODEPOINT_LOSS")
        if result["kind"] == "TOKEN_VAZIO" and not result["reason"]:
            errors.append(f"{case_id}_MISSING_REASON")
        if result["kind"] == "NUMERIC_ZERO" and (
            result["parsed_value"] != 0 or result["parsed_value"] is None
        ):
            errors.append(f"{case_id}_ZERO_DRIFT")
    if len(seen) < 18:
        errors.append("INSUFFICIENT_NEGATIVE_FIXTURES")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=FIXTURES)
    args = parser.parse_args()
    try:
        data = json.loads(args.fixtures.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("expected object")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print("FAIL: unreadable fixture contract:", str(exc))
        return 2
    errors = validate(data)
    for error in errors:
        print("FAIL:", error)
    if errors:
        return 1
    print("PASS: bounded lexical void falsifiers", "cases=" + str(len(data["cases"])))
    print("GLOBAL_CLAIM=false; SOURCE_LEXEME != PARSED_VALUE != EVIDENCE_FOR_MISSING_VALUE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
