#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from statistics import median
from typing import Any, Iterable

SCHEMA = "rafaelia.sustento-t-observation.receipt.v1"
BOUNDARY = "SOURCE!=ARTEFACT!=EXECUTION!=EVIDENCE!=CLAIM"
R = math.sqrt(3.0) / 2.0

TV = "TOKEN_VAZIO"
TV_TIE = "TOKEN_VAZIO_TIE"
TV_INSUFFICIENT = "TOKEN_VAZIO_INSUFFICIENT_CONSENSUS"
TV_GATE_INPUT = "TOKEN_VAZIO_GATE_INPUT"


def _bit(v: Any) -> int | None:
    if v in (0, 1):
        return int(v)
    if v is None or (isinstance(v, str) and v.startswith("TOKEN_VAZIO")):
        return None
    raise ValueError(f"invalid epistemic bit: {v!r}")


def majority3(values: Iterable[Any]) -> int | str:
    bits = [_bit(v) for v in values]
    if len(bits) != 3:
        raise ValueError("majority3 requires exactly 3 readings")
    n1 = sum(v == 1 for v in bits)
    n0 = sum(v == 0 for v in bits)
    if n1 >= 2:
        return 1
    if n0 >= 2:
        return 0
    return TV_INSUFFICIENT


def majority4_abstain(values: Iterable[Any]) -> int | str:
    bits = [_bit(v) for v in values]
    if len(bits) != 4:
        raise ValueError("majority4 requires exactly 4 readings")
    n1 = sum(v == 1 for v in bits)
    n0 = sum(v == 0 for v in bits)
    if n1 >= 3:
        return 1
    if n0 >= 3:
        return 0
    if n1 == 2 and n0 == 2:
        return TV_TIE
    return TV_INSUFFICIENT


def gate4of5(values: Iterable[Any]) -> int | str:
    bits = [_bit(v) for v in values]
    if len(bits) != 5:
        raise ValueError("gate4of5 requires exactly 5 readings")
    n1 = sum(v == 1 for v in bits)
    n0 = sum(v == 0 for v in bits)
    if n1 >= 4:
        return 1
    if n0 >= 4:
        return 0
    return TV_INSUFFICIENT


def iid_metrics(p: float) -> dict[str, float]:
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be in [0,1]")
    return {
        "single_error": p,
        "majority3_error": 3 * p**2 - 2 * p**3,
        "u4_wrong_with_tie_abstain": 4 * p**3 - 3 * p**4,
        "u4_tie": 6 * p**2 * (1 - p) ** 2,
        "majority5_error": 10 * p**3 - 15 * p**4 + 6 * p**5,
        "gate4of5_wrong": 5 * p**4 - 4 * p**5,
        "gate4of5_abstain": 10 * p**2 * (1 - p) ** 2,
    }


def normalized_stencil(n: int) -> list[float]:
    if n == 3:
        return [-1.0, 0.0, 1.0]
    if n == 4:
        return [-1.0, -1.0 / 3.0, 1.0 / 3.0, 1.0]
    if n == 5:
        return [-1.0, -0.5, 0.0, 0.5, 1.0]
    raise ValueError("supported stencils are 3, 4, 5")


def contracted_window(t_in: float, t_out: float, level: int) -> dict[str, float]:
    if t_out <= t_in:
        raise ValueError("t_out must be > t_in")
    if level < 0:
        raise ValueError("level must be >= 0")
    m = (t_in + t_out) / 2.0
    width = (t_out - t_in) * (R**level)
    return {
        "level": level,
        "center": m,
        "width": width,
        "left": m - width / 2.0,
        "right": m + width / 2.0,
    }


def robust_summary(values: Iterable[float]) -> dict[str, float] | str:
    xs = list(values)
    if not xs:
        return "TOKEN_VAZIO_UNOBSERVED"
    ys = sorted(float(v) for v in xs)
    n = len(ys)

    def q(frac: float) -> float:
        if n == 1:
            return ys[0]
        pos = frac * (n - 1)
        lo = int(math.floor(pos))
        hi = int(math.ceil(pos))
        if lo == hi:
            return ys[lo]
        w = pos - lo
        return ys[lo] * (1.0 - w) + ys[hi] * w

    return {
        "min": ys[0],
        "median": float(median(ys)),
        "max": ys[-1],
        "q05": q(0.05),
        "q50": q(0.50),
        "q95": q(0.95),
    }


def sustento_gate(dimensions: dict[str, Any], tau: float) -> dict[str, Any]:
    if not 0.0 <= tau <= 1.0:
        raise ValueError("tau must be in [0,1]")
    required = (
        "provenance",
        "context",
        "evidence",
        "contradiction",
        "uncertainty",
        "reproduction",
        "rollback",
    )
    if any(dimensions.get(k) is None for k in required):
        return {
            "state": TV_GATE_INPUT,
            "score": None,
            "tau": tau,
            "effective": None,
            "pass": False,
        }
    vals = {k: float(dimensions[k]) for k in required}
    if any(not 0.0 <= v <= 1.0 for v in vals.values()):
        raise ValueError("all gate dimensions must be in [0,1]")
    effective = {
        "provenance": vals["provenance"],
        "context": vals["context"],
        "evidence": vals["evidence"],
        "contradiction_control": 1.0 - vals["contradiction"],
        "uncertainty_control": 1.0 - vals["uncertainty"],
        "reproduction": vals["reproduction"],
        "rollback": vals["rollback"],
    }
    product = math.prod(effective.values())
    score = product ** (1.0 / 7.0)
    passed = min(effective.values()) >= tau
    return {
        "state": "PASS" if passed else "HOLD",
        "score": score,
        "tau": tau,
        "effective": effective,
        "pass": passed,
    }


def geometry_reference() -> dict[str, Any]:
    return {
        "sqrt3_over_2": R,
        "r2": R**2,
        "r6": R**6,
        "one_minus_r6": 1.0 - R**6,
        "difference_complement_minus_r6": (1.0 - R**6) - R**6,
        "exact": {
            "r2": "3/4",
            "r6": "27/64",
            "one_minus_r6": "37/64",
            "difference": "5/32",
        },
    }


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def build_receipt(config: dict[str, Any]) -> dict[str, Any]:
    ps = [float(p) for p in config["noise_p"]]
    tau = float(config["tau"])
    gate = sustento_gate(config["gate_dimensions"], tau)
    core = {
        "schema": SCHEMA,
        "state": "EXECUTED_DETERMINISTIC_REFERENCE",
        "claim_allowed": False,
        "promotion_allowed": False,
        "boundary": BOUNDARY,
        "model": {
            "stencils": {
                "U3": normalized_stencil(3),
                "U4": normalized_stencil(4),
                "U5": normalized_stencil(5),
            },
            "void_semantics": "TOKEN_VAZIO!=0; EMPTY_SET!=TOKEN_VAZIO",
            "iid_assumption": True,
        },
        "gate": gate,
        "noise_sweep": [{"p": p, **iid_metrics(p)} for p in ps],
        "geometry": geometry_reference(),
        "examples": {
            "majority3_011": majority3([0, 1, 1]),
            "u4_0011": majority4_abstain([0, 0, 1, 1]),
            "gate45_11110": gate4of5([1, 1, 1, 1, 0]),
            "empty_summary": robust_summary([]),
        },
        "physical_detector": "TOKEN_VAZIO",
        "quantum_causal_binding": "TOKEN_VAZIO",
        "frida_physical_runtime": "TOKEN_VAZIO",
    }
    core["receipt_sha256"] = hashlib.sha256(canonical_bytes(core)).hexdigest()
    return core


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vectors", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    config = json.loads(Path(args.vectors).read_text(encoding="utf-8"))
    receipt = build_receipt(config)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
