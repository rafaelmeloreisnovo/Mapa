#!/usr/bin/env python3
"""Validate MHEL-Ω V1.3 Bagua/manifold receipts without third-party packages."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
TRIGRAMS = {
    "QIAN": "111",
    "DUI": "110",
    "LI": "101",
    "ZHEN": "100",
    "XUN": "011",
    "KAN": "010",
    "GEN": "001",
    "KUN": "000",
}
WINDOW_ROLES = ["ORIGIN_INPUT", "TRANSFORM_MIDDLE", "RECEIPT_OUTPUT"]
MATERIAL_GROUPS = {
    "TEXT_LANGUAGE",
    "MATHEMATICS_GEOMETRY",
    "CODE_BINARY",
    "STORAGE_FORENSICS",
    "SCIENCE_MEASUREMENT",
    "SYMBOL_PARABLE",
    "LEGAL_AUTHORSHIP",
    "TOKEN_VAZIO",
}
DMAIC = {"DEFINE", "MEASURE", "ANALYZE", "IMPROVE", "CONTROL"}
EPISTEMIC = {
    "KNOWS",
    "FELTS",
    "TOKEN_VAZIO",
    "TOKEN_VAZIO_QUANTIFICADO",
    "CONTRADICTED",
    "REFUTED",
    "UNKNOWN_UNKNOWN",
}


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _close(a: float, b: float, *, rel: float = 1e-9, abs_tol: float = 1e-12) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_tol)


def validate(receipt: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    required = {
        "schema_version",
        "receipt_id",
        "source_hash",
        "previous_event_hash",
        "window_thirds",
        "material_group",
        "manifold_coordinates",
        "epistemic_state",
        "dmaic_stage",
        "sample_statistics",
        "token_vazio",
        "next_test",
        "claim_allowed",
    }
    missing = sorted(required - receipt.keys())
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
        return errors

    if receipt["schema_version"] != "mhel-omega-manifold-receipt-v1":
        errors.append("schema_version must be mhel-omega-manifold-receipt-v1")

    if not isinstance(receipt["receipt_id"], str) or not receipt["receipt_id"].strip():
        errors.append("receipt_id must be a non-empty string")

    source_hash = receipt["source_hash"]
    if not isinstance(source_hash, str) or SHA256_RE.fullmatch(source_hash) is None:
        errors.append("source_hash must be a 64-hex SHA-256")

    previous_hash = receipt["previous_event_hash"]
    if previous_hash != "GENESIS" and (
        not isinstance(previous_hash, str) or SHA256_RE.fullmatch(previous_hash) is None
    ):
        errors.append("previous_event_hash must be GENESIS or a 64-hex SHA-256")

    thirds = receipt["window_thirds"]
    if not isinstance(thirds, list) or len(thirds) != 3:
        errors.append("window_thirds must contain exactly 3 entries")
    else:
        roles: list[Any] = []
        for index, third in enumerate(thirds):
            if not isinstance(third, dict):
                errors.append(f"window_thirds[{index}] must be an object")
                continue
            roles.append(third.get("role"))
            for part in ("start", "middle", "end"):
                if part not in third:
                    errors.append(f"window_thirds[{index}] missing {part}")
        if roles != WINDOW_ROLES:
            errors.append(f"window_thirds roles must be ordered as {WINDOW_ROLES}")

    if receipt["material_group"] not in MATERIAL_GROUPS:
        errors.append("material_group is not canonical")

    coordinates = receipt["manifold_coordinates"]
    coordinate_fields = {"source", "syntax", "semantics", "dynamics", "evidence", "uncertainty", "time", "scale"}
    if not isinstance(coordinates, dict):
        errors.append("manifold_coordinates must be an object")
    else:
        absent = sorted(coordinate_fields - coordinates.keys())
        if absent:
            errors.append(f"manifold_coordinates missing: {', '.join(absent)}")
        uncertainty = coordinates.get("uncertainty")
        if not _is_number(uncertainty) or not 0 <= float(uncertainty) <= 1:
            errors.append("manifold uncertainty must be between 0 and 1")

    trigram = receipt.get("trigram_state")
    if trigram is not None:
        if not isinstance(trigram, dict):
            errors.append("trigram_state must be null or an object")
        else:
            trigram_id = trigram.get("id")
            bits = trigram.get("bits")
            if trigram_id not in TRIGRAMS:
                errors.append("trigram_state.id is invalid")
            elif bits != TRIGRAMS[trigram_id]:
                errors.append(f"trigram bits mismatch: {trigram_id} must be {TRIGRAMS[trigram_id]}")

    hexagram = receipt.get("hexagram_state")
    if hexagram is not None:
        if not isinstance(hexagram, dict):
            errors.append("hexagram_state must be null or an object")
        else:
            bits = hexagram.get("bits")
            lower = hexagram.get("lower_trigram")
            upper = hexagram.get("upper_trigram")
            if not isinstance(bits, str) or re.fullmatch(r"[01]{6}", bits) is None:
                errors.append("hexagram bits must contain exactly six binary digits")
            elif lower != bits[:3] or upper != bits[3:]:
                errors.append("hexagram lower/upper trigrams must reconstruct the six bits")

    if receipt["epistemic_state"] not in EPISTEMIC:
        errors.append("epistemic_state is not canonical")
    if receipt["dmaic_stage"] not in DMAIC:
        errors.append("dmaic_stage is not canonical")

    stats = receipt["sample_statistics"]
    if not isinstance(stats, dict):
        errors.append("sample_statistics must be an object")
    else:
        for key in ("n", "n_effective", "design_effect", "margin_of_error", "confidence_level"):
            if key not in stats:
                errors.append(f"sample_statistics missing {key}")
        n = stats.get("n")
        n_eff = stats.get("n_effective")
        deff = stats.get("design_effect")
        if not isinstance(n, int) or isinstance(n, bool) or n < 0:
            errors.append("sample_statistics.n must be a non-negative integer")
        if not _is_number(deff) or float(deff) < 1:
            errors.append("design_effect must be >= 1")
        if _is_number(n_eff) and isinstance(n, int) and _is_number(deff) and float(deff) >= 1:
            expected = n / float(deff)
            if not _close(float(n_eff), expected, rel=1e-7, abs_tol=1e-9):
                errors.append(f"n_effective must equal n/design_effect ({expected})")
        else:
            errors.append("n_effective must be numeric")

        margin = stats.get("margin_of_error")
        if margin is not None and (not _is_number(margin) or float(margin) < 0):
            errors.append("margin_of_error must be null or non-negative")
        confidence = stats.get("confidence_level")
        if confidence is not None and (
            not _is_number(confidence) or not 0 <= float(confidence) <= 1
        ):
            errors.append("confidence_level must be null or between 0 and 1")

    alpha = receipt.get("alpha_k")
    if alpha is not None:
        if not isinstance(alpha, dict):
            errors.append("alpha_k must be null or an object")
        elif alpha.get("state") == "MEASURED":
            r0 = alpha.get("initial_radius")
            delta_d = alpha.get("delta_demand")
            delta_r = alpha.get("delta_radius")
            value = alpha.get("value")
            if not all(_is_number(v) for v in (r0, delta_d, delta_r, value)):
                errors.append("measured alpha_k requires numeric radius, demand, delta and value")
            elif float(r0) <= 0 or float(delta_d) == 0:
                errors.append("alpha_k requires initial_radius > 0 and delta_demand != 0")
            else:
                expected_alpha = float(delta_r) / (float(r0) * float(delta_d))
                if not _close(float(value), expected_alpha, rel=1e-7, abs_tol=1e-9):
                    errors.append(f"alpha_k.value mismatch; expected {expected_alpha}")

    capability = receipt.get("process_capability")
    if capability is not None:
        if not isinstance(capability, dict):
            errors.append("process_capability must be null or an object")
        elif capability.get("stable_process") is not True:
            errors.append("Cp/Cpk/DPMO receipt requires stable_process=true")
        else:
            defects = capability.get("defects")
            units = capability.get("units")
            opportunities = capability.get("opportunities_per_unit")
            if not all(isinstance(v, int) and not isinstance(v, bool) for v in (defects, units, opportunities)):
                errors.append("defects, units and opportunities_per_unit must be integers")
            elif defects < 0 or units <= 0 or opportunities <= 0:
                errors.append("invalid defect/opportunity counts")
            else:
                dpo = defects / (units * opportunities)
                dpmo = 1_000_000 * dpo
                if _is_number(capability.get("dpo")) and not _close(float(capability["dpo"]), dpo, rel=1e-7):
                    errors.append(f"dpo mismatch; expected {dpo}")
                if _is_number(capability.get("dpmo")) and not _close(float(capability["dpmo"]), dpmo, rel=1e-7):
                    errors.append(f"dpmo mismatch; expected {dpmo}")

            mean = capability.get("mean")
            stddev = capability.get("sample_stddev")
            lsl = capability.get("lsl")
            usl = capability.get("usl")
            if all(_is_number(v) for v in (mean, stddev, lsl, usl)) and float(stddev) > 0 and float(usl) > float(lsl):
                cp = (float(usl) - float(lsl)) / (6 * float(stddev))
                cpk = min(
                    (float(usl) - float(mean)) / (3 * float(stddev)),
                    (float(mean) - float(lsl)) / (3 * float(stddev)),
                )
                if _is_number(capability.get("cp")) and not _close(float(capability["cp"]), cp, rel=1e-7):
                    errors.append(f"cp mismatch; expected {cp}")
                if _is_number(capability.get("cpk")) and not _close(float(capability["cpk"]), cpk, rel=1e-7):
                    errors.append(f"cpk mismatch; expected {cpk}")

    token_vazio = receipt["token_vazio"]
    if not isinstance(token_vazio, list):
        errors.append("token_vazio must be an array")
    else:
        for index, token in enumerate(token_vazio):
            if not isinstance(token, dict):
                errors.append(f"token_vazio[{index}] must be an object")
                continue
            for key in ("id", "missing_information", "uncertainty", "required_test"):
                if key not in token:
                    errors.append(f"token_vazio[{index}] missing {key}")
            uncertainty = token.get("uncertainty")
            if not _is_number(uncertainty) or not 0 <= float(uncertainty) <= 1:
                errors.append(f"token_vazio[{index}].uncertainty must be between 0 and 1")

    if not isinstance(receipt["next_test"], str) or not receipt["next_test"].strip():
        errors.append("next_test must be a non-empty string")

    if receipt["claim_allowed"] is not False:
        errors.append("claim_allowed must remain false for this canonical draft")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path, help="JSON receipt to validate")
    args = parser.parse_args()

    try:
        payload = json.loads(args.receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read valid JSON: {exc}", file=sys.stderr)
        return 2

    if not isinstance(payload, dict):
        print("FAIL: receipt root must be an object", file=sys.stderr)
        return 2

    errors = validate(payload)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: MHEL-Ω manifold receipt is internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
