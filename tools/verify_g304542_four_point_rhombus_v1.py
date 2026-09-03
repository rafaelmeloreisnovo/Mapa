#!/usr/bin/env python3
"""Deterministic local verifier for the G_{30,45,42} four-point rhombus model.

Scope: a finite mathematical model only.  It does not assert a physical mechanism,
an emergent 42-cycle, or a result beyond the explicitly declared transition rule.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Iterable, Sequence


SCHEMA = "RAFAELIA_G304542_FOUR_POINT_RHOMBUS_RECEIPT_V1"
MODEL_ID = "G304542:FOUR_POINT_RHOMBUS:V1"
EPSILON = 1e-12
ANGLES = (("0", 0.0), ("30", math.pi / 6.0), ("45", math.pi / 4.0))

Point = tuple[float, float]
Permutation = tuple[int, int, int, int]
State = tuple[Permutation, int]


def close(a: float, b: float, epsilon: float = EPSILON) -> bool:
    return abs(a - b) <= epsilon


def base_points() -> tuple[Point, Point, Point, Point]:
    """A unit-side rhombus with edge vectors at 0 and 60 degrees.

    The long diagonal is oriented at 30 degrees.  This gives a precise geometric
    meaning to the 30-degree component without treating it as a universal claim.
    """
    sqrt3 = math.sqrt(3.0)
    return (
        (-3.0 / 4.0, -sqrt3 / 4.0),
        (1.0 / 4.0, -sqrt3 / 4.0),
        (3.0 / 4.0, sqrt3 / 4.0),
        (-1.0 / 4.0, sqrt3 / 4.0),
    )


def distance_sq(a: Point, b: Point) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def distance_spectrum(points: Sequence[Point]) -> list[float]:
    return sorted(distance_sq(points[i], points[j]) for i in range(4) for j in range(i + 1, 4))


def project(point: Point, angle: float) -> float:
    return point[0] * math.cos(angle) + point[1] * math.sin(angle)


def polynomial_from_roots(roots: Iterable[float]) -> list[float]:
    """Return monic coefficients in descending order."""
    coeffs = [1.0]
    for root in roots:
        next_coeffs = [0.0] * (len(coeffs) + 1)
        for index, coeff in enumerate(coeffs):
            next_coeffs[index] += coeff
            next_coeffs[index + 1] -= root * coeff
        coeffs = next_coeffs
    return coeffs


def projection_polynomials(points: Sequence[Point]) -> dict[str, list[float]]:
    return {
        label: polynomial_from_roots(project(point, angle) for point in points)
        for label, angle in ANGLES
    }


def all_close(left: Sequence[float], right: Sequence[float]) -> bool:
    return len(left) == len(right) and all(close(a, b) for a, b in zip(left, right))


def receipt_number(value: float) -> float:
    """Normalize tiny platform-dependent trigonometric residue for the receipt."""
    if abs(value) < EPSILON:
        return 0.0
    return round(value, 15)


def state_step(state: State) -> State:
    """Minimal symbolic coupling.

    The ordered four labels are shifted by one; the observation frame advances
    through 0°, 30°, and 45°.  The angles are observation frames, not a physical
    rotation law.  This deliberately minimal rule is suitable for falsification.
    """
    permutation, frame = state
    return (permutation[1:] + permutation[:1], (frame + 1) % len(ANGLES))


def period(state: State, bound: int = 1000) -> int:
    current = state_step(state)
    for step in range(1, bound + 1):
        if current == state:
            return step
        current = state_step(current)
    raise AssertionError(f"period not found within {bound} steps")


def apply_steps(state: State, count: int) -> State:
    current = state
    for _ in range(count):
        current = state_step(current)
    return current


def component_lengths(states: Sequence[State]) -> list[int]:
    remaining = set(states)
    lengths: list[int] = []
    while remaining:
        start = next(iter(remaining))
        cycle: list[State] = []
        current = start
        while current not in cycle:
            cycle.append(current)
            current = state_step(current)
        if current != start:
            raise AssertionError("unexpected tail in permutation/frame transition")
        lengths.append(len(cycle))
        remaining.difference_update(cycle)
    return sorted(lengths)


def run() -> dict[str, object]:
    points = base_points()
    spectrum = distance_spectrum(points)
    expected_spectrum = [1.0, 1.0, 1.0, 1.0, 1.0, 3.0]
    if not all_close(spectrum, expected_spectrum):
        raise AssertionError(f"distance spectrum mismatch: {spectrum}")

    adjacent = [distance_sq(points[i], points[(i + 1) % 4]) for i in range(4)]
    if not all(close(value, 1.0) for value in adjacent):
        raise AssertionError(f"side-length mismatch: {adjacent}")

    diagonals = {"p0_p2_sq": distance_sq(points[0], points[2]), "p1_p3_sq": distance_sq(points[1], points[3])}
    if not close(diagonals["p0_p2_sq"], 3.0) or not close(diagonals["p1_p3_sq"], 1.0):
        raise AssertionError(f"diagonal mismatch: {diagonals}")

    baseline_projection = projection_polynomials(points)
    permutations = list(itertools.permutations(range(4)))
    for permutation in permutations:
        permuted = [points[index] for index in permutation]
        if not all_close(distance_spectrum(permuted), spectrum):
            raise AssertionError(f"distance invariant failed for {permutation}")
        candidate_projection = projection_polynomials(permuted)
        for label in baseline_projection:
            if not all_close(candidate_projection[label], baseline_projection[label]):
                raise AssertionError(f"projection polynomial invariant failed for {permutation} at {label}")

    states: list[State] = [(permutation, frame) for permutation in permutations for frame in range(len(ANGLES))]
    periods = [period(state) for state in states]
    if set(periods) != {12}:
        raise AssertionError(f"minimal transition has unexpected periods: {sorted(set(periods))}")
    if not all(apply_steps(state, 12) == state for state in states):
        raise AssertionError("T^12 must be identity in the declared finite model")
    if all(apply_steps(state, 42) == state for state in states):
        raise AssertionError("T^42 unexpectedly became identity for every state")
    components = component_lengths(states)
    if components != [12] * 6:
        raise AssertionError(f"component structure mismatch: {components}")

    return {
        "schema": SCHEMA,
        "model_id": MODEL_ID,
        "claim_allowed": False,
        "evidence_class": "SIMULATED_LOCAL_MODEL",
        "formal_objects": {
            "base_edges": ["u=(1,0)", "v=(1/2,sqrt(3)/2)"],
            "long_diagonal_angle_degrees": 30,
            "projection_frames_degrees": [0, 30, 45],
            "projection_polynomials": {
                label: [receipt_number(value) for value in coefficients]
                for label, coefficients in baseline_projection.items()
            },
            "squared_distance_spectrum": [receipt_number(value) for value in spectrum],
            "squared_diagonals": {key: receipt_number(value) for key, value in diagonals.items()},
        },
        "coverage": {
            "labeled_point_permutations": len(permutations),
            "projection_frames": len(ANGLES),
            "finite_states": len(states),
            "permutation_invariance_checks": len(permutations) * (1 + len(ANGLES)),
        },
        "minimal_transition": {
            "definition": "T(permutation, frame)=(left_rotate(permutation), (frame+1) mod 3)",
            "order": 12,
            "component_count": len(components),
            "component_lengths": components,
            "periods_observed": sorted(set(periods)),
            "period_42_observed": False,
        },
        "source_custody": {
            "state": "VERIFIED_LIMITED",
            "parent_hypothesis": {
                "id": "HYP-M2-G304542-002",
                "repository": "rafaelmeloreisnovo/Mapa",
                "path": "data/hypotheses/RAFAELIA_HYPOTHESIS_FGAP_REGISTRY.v1.json",
                "source_commit": "ccdea71aa7fb1cbf676b01351e6d954923c9a23f",
                "state": "DOCUMENTED_REFERENCE",
            },
            "reading_metadata": [
                {"id": "arXiv:2510.12532", "url": "https://arxiv.org/abs/2510.12532"},
                {"id": "arXiv:2502.00506", "url": "https://arxiv.org/abs/2502.00506"},
                {"id": "arXiv:2604.13124", "url": "https://arxiv.org/abs/2604.13124"},
                {"id": "arXiv:2602.22356", "url": "https://arxiv.org/abs/2602.22356"},
                {"id": "arXiv:2510.05863", "url": "https://arxiv.org/abs/2510.05863"},
            ],
            "limit": "URLs and abstract metadata were reviewed; no external-paper byte hash or theorem transfer is claimed.",
        },
        "gaps": [
            "TOKEN_VAZIO_G304542_CANONICAL_COUPLING_BEYOND_MINIMAL_RULE",
            "TOKEN_VAZIO_G304542_ENDOGENOUS_42_CYCLE",
            "TOKEN_VAZIO_G304542_NONTRIVIAL_INVARIANT_BEYOND_LABEL_SYMMETRY",
            "TOKEN_VAZIO_G304542_EQUIVALENCE_AND_PRIOR_ART",
            "TOKEN_VAZIO_G304542_EXACT_SYMBOLIC_PROOF",
            "TOKEN_VAZIO_G304542_CROSS_HOST_REPRODUCTION",
            "TOKEN_VAZIO_SCOPE_RXNORM_NO_CLINICAL_INTEGRATION",
        ],
        "scope_guard": "A 12-step result for this declared model neither proves nor disproves a different G_{30,45,42} rule.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    receipt = run()
    receipt["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"model_id": MODEL_ID, "finite_states": 72, "period": 12, "period_42_observed": False}, sort_keys=True))


if __name__ == "__main__":
    main()
