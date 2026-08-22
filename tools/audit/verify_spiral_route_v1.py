#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
from pathlib import Path

# Relevant implementation logic reproduced from:
# rafaelmeloreisnovo/GAIA_phi@cccf5f7da96e2f867fbb5cdec07a45da6e380994
# dados/RAFAELIA_TRIG_CORE2.py
TAU = 2.0 * math.pi
SQRT3_OVER_2 = math.sqrt(3.0) / 2.0


def generate_spiral_sqrt3_over_2(n_turns, steps_per_turn, r0=1.0, direction=1):
    if n_turns < 1:
        raise ValueError("n_turns must be >= 1.")
    if steps_per_turn < 1:
        raise ValueError("steps_per_turn must be >= 1.")
    if r0 <= 0.0:
        raise ValueError("r0 must be > 0.0.")
    if direction == 0:
        raise ValueError("direction must be non-zero (use +1 or -1).")
    total_steps = n_turns * steps_per_turn
    sign = 1 if direction > 0 else -1
    points = []
    for k in range(total_steps + 1):
        radius = r0 * (SQRT3_OVER_2 ** k)
        theta = sign * TAU * (k / float(steps_per_turn))
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        points.append((x, y))
    return points


def generate_spiral_yinyang_42(r0=1.0):
    if r0 <= 0.0:
        raise ValueError("r0 must be > 0.0.")
    yin = generate_spiral_sqrt3_over_2(1, 20, r0, 1)
    yang = generate_spiral_sqrt3_over_2(1, 20, r0, -1)
    return yin + yang


def run_receipt():
    pts = generate_spiral_sqrt3_over_2(2, 10, 1.0, 1)
    radii = [math.hypot(x, y) for x, y in pts]
    radial_errors = [
        abs(radii[k + 1] - SQRT3_OVER_2 * radii[k])
        for k in range(len(radii) - 1)
    ]
    closed_form_errors = [
        abs(r - (SQRT3_OVER_2 ** k)) for k, r in enumerate(radii)
    ]
    yy_count = len(generate_spiral_yinyang_42())
    return {
        "schema": "RAFAELIA_SPIRAL_ROUTE_EXECUTION_RECEIPT_V1",
        "claim_allowed": False,
        "source": {
            "repo": "rafaelmeloreisnovo/teoremas",
            "path": "docs/rafaelia/04-spiral-raiz3-sobre-2.md",
            "blob_sha": "eaa831155fcfac79fa72d1cd6fd13f5d5d9aecb8",
            "formula_radial": "r_{n+1}=(sqrt(3)/2)*r_n",
            "formula_angular": "theta[n+1]=theta[n]+pi/phi",
        },
        "implementation": {
            "repo": "rafaelmeloreisnovo/GAIA_phi",
            "path": "dados/RAFAELIA_TRIG_CORE2.py",
            "blob_sha": "cccf5f7da96e2f867fbb5cdec07a45da6e380994",
            "function": "generate_spiral_sqrt3_over_2",
            "radial_form": "r0*(SQRT3_OVER_2**k)",
            "angular_form": "theta(k)=sign*2*pi*k/steps_per_turn",
        },
        "execution": {
            "n_turns": 2,
            "steps_per_turn": 10,
            "r0": 1.0,
            "points": len(pts),
            "yinyang_points": yy_count,
            "kappa": SQRT3_OVER_2,
            "max_radial_recurrence_abs_error": max(radial_errors),
            "max_closed_form_abs_error": max(closed_form_errors),
            "implementation_angular_step_for_steps10": TAU / 10.0,
        },
        "gates": {
            "radial_recurrence_matches_source": (
                "PASS_NUMERIC_LIMITED" if max(radial_errors) < 1e-14 else "FAIL"
            ),
            "closed_form_consistency": (
                "PASS_NUMERIC_LIMITED" if max(closed_form_errors) < 1e-14 else "FAIL"
            ),
            "yinyang_42_count": "PASS" if yy_count == 42 else "FAIL",
            "full_source_pair_equivalence": "TOKEN_VAZIO_NOT_ESTABLISHED",
            "angular_equivalence": "FAIL_NOT_SAME_FORM",
        },
        "boundary": (
            "Execution verifies the radial recurrence implemented by GAIA_phi. "
            "It does not validate broader applications/physical meaning, and the "
            "angular law in the source document is not the same law implemented "
            "by the generator."
        ),
        "F_ok": (
            "source->implementation radial link found and executed; radial recurrence "
            "and 42-point count pass limited deterministic checks"
        ),
        "F_gap": (
            "angular source recurrence pi/phi is not implemented by this generator; "
            "broader source applications remain unverified; full semantic equivalence "
            "is not established"
        ),
        "F_next": (
            "either bind a producer implementation for theta[n+1]=theta[n]+pi/phi "
            "or explicitly split Spiral√3/2 into independent radial and angular variants "
            "before any full-formula claim"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    receipt = run_receipt()
    payload = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.write_text(payload, encoding="utf-8")
    script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    receipt_sha = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    print(
        json.dumps(
            {
                "receipt": receipt,
                "script_sha256": script_sha,
                "receipt_sha256": receipt_sha,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
