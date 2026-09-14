"""Typed mathematical crosswalk for RAFAELIA geometry claims.

This module deliberately separates numeric value, representation provenance,
modular residue, winding history, hyperbolic metric facts, and epistemic gaps.

SOURCE != REPRESENTATION != TRANSFORMATION != EVIDENCE != CLAIM
TOKEN_VAZIO != 0 != residue-class zero
"""
from __future__ import annotations

from fractions import Fraction
from math import log
from typing import Any


def rational_with_provenance(numerator: int, denominator: int) -> dict[str, Any]:
    """Reduce a rational while preserving the common representation scale."""
    if denominator == 0:
        raise ZeroDivisionError("denominator must be non-zero")
    value = Fraction(numerator, denominator)
    scale = denominator // value.denominator
    assert numerator == scale * value.numerator
    assert denominator == scale * value.denominator
    return {
        "original": [numerator, denominator],
        "reduced": [value.numerator, value.denominator],
        "representation_scale": scale,
        "value": value,
    }


def modular_state(integer: int, modulus: int) -> dict[str, int]:
    """Return quotient + residue so modulo does not erase winding/history."""
    if modulus <= 0:
        raise ValueError("modulus must be a positive integer")
    quotient, residue = divmod(integer, modulus)
    return {
        "integer": integer,
        "modulus": modulus,
        "quotient": quotient,
        "residue": residue,
        "reconstructed": quotient * modulus + residue,
    }


def poincare_metric_scale_k_minus_1(euclidean_radius: float) -> float:
    """Conformal line-element scale for the unit disk with Gaussian K=-1.

    ds^2 = 4 (dx^2 + dy^2) / (1-r^2)^2
    """
    r = float(euclidean_radius)
    if not 0.0 <= r < 1.0:
        raise ValueError("euclidean_radius must satisfy 0 <= r < 1")
    return 2.0 / (1.0 - r * r)


def poincare_radial_distance_k_minus_1(euclidean_radius: float) -> float:
    """Hyperbolic distance from 0 to Euclidean radius r in the unit disk."""
    r = float(euclidean_radius)
    if not 0.0 <= r < 1.0:
        raise ValueError("euclidean_radius must satisfy 0 <= r < 1")
    return log((1.0 + r) / (1.0 - r))


def quadratic_root_class(a: float, b: float, c: float) -> dict[str, Any]:
    """Classify quadratic roots by discriminant without inventing geometry."""
    if a == 0:
        raise ValueError("a must be non-zero for a quadratic")
    delta = b * b - 4 * a * c
    if delta > 0:
        root_space = "REAL_TWO"
    elif delta == 0:
        root_space = "REAL_DOUBLE"
    else:
        root_space = "COMPLEX_CONJUGATE"
    return {"discriminant": delta, "root_space": root_space}


def angular_cover_state(angle_degrees: int, multiplier: int, cover: int = 7) -> dict[str, Any]:
    """Preserve 360-degree winding count and a declared cover-space remainder."""
    if cover <= 0:
        raise ValueError("cover must be positive")
    total = Fraction(angle_degrees) * Fraction(multiplier)
    winding, angle_remainder = divmod(total, 360)
    cover_period = 360 * cover
    cover_winding, cover_remainder = divmod(total, cover_period)
    return {
        "total_degrees": total,
        "winding_360": int(winding),
        "angle_remainder_360": angle_remainder,
        "cover": cover,
        "cover_winding": int(cover_winding),
        "cover_remainder_degrees": cover_remainder,
    }


TOPOLOGY = {
    "sphere_S2": {"betti_0": 1, "betti_1": 0, "betti_2": 1, "chi": 2},
    "torus_T2": {"betti_0": 1, "betti_1": 2, "betti_2": 1, "chi": 0},
}


def subdivision_can_preserve_target_topology(source: str, target: str) -> bool:
    """Pure subdivision preserves the topology of the same surface."""
    if source not in TOPOLOGY or target not in TOPOLOGY:
        raise KeyError("unknown topology signature")
    return TOPOLOGY[source] == TOPOLOGY[target]
