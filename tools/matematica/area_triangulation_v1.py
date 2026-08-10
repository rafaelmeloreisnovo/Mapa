#!/usr/bin/env python3
"""Reference kernel for reversible signed-area geometry.

Stdlib-only. This module validates identities; it does not claim mathematical novelty.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose, sqrt
from typing import Iterable

EPS = 1e-12


@dataclass(frozen=True)
class SignedArea:
    area: float
    sign: int = 1

    def value(self) -> float:
        if self.sign not in (-1, 1):
            raise ValueError("sign must be -1 or +1")
        if self.area < 0:
            raise ValueError("area magnitude must be non-negative")
        return self.sign * self.area


def total_signed_area(parts: Iterable[SignedArea]) -> float:
    return sum(p.value() for p in parts)


def transfer_area(a1: float, a2: float, delta: float) -> tuple[float, float]:
    """Move delta from region 1 to region 2 while preserving total area."""
    return a1 - delta, a2 + delta


def isosceles_height(equal_side: float, base: float) -> float:
    if equal_side <= 0 or base <= 0:
        raise ValueError("lengths must be positive")
    radicand = equal_side * equal_side - (base * base) / 4.0
    if radicand < -EPS:
        raise ValueError("invalid isosceles geometry")
    return sqrt(max(0.0, radicand))


def isosceles_area(equal_side: float, base: float) -> float:
    return 0.5 * base * isosceles_height(equal_side, base)


def equivalent_square_side(area: float) -> float:
    if area < 0:
        raise ValueError("unsigned square area must be non-negative")
    return sqrt(area)


def s30(length: float) -> float:
    """30° projection / equilateral-height scale: sqrt(3)/2."""
    return length * sqrt(3.0) / 2.0


def s30_inverse(length: float) -> float:
    return length * 2.0 / sqrt(3.0)


def s2(length: float) -> float:
    """Square diagonal scale: sqrt(2)."""
    return length * sqrt(2.0)


def s2_inverse(length: float) -> float:
    return length / sqrt(2.0)


def linear_area_scale(m00: float, m01: float, m10: float, m11: float) -> float:
    """Absolute area scale |det(T)| for a 2x2 linear transform."""
    return abs(m00 * m11 - m01 * m10)


def shear_area_scale(k: float) -> float:
    return linear_area_scale(1.0, k, 0.0, 1.0)


def complete_square_offset(b: float, a: float = 1.0) -> float:
    """Area term added/subtracted when completing ax^2+bx+c after divide by a."""
    if a == 0:
        raise ValueError("a must be non-zero")
    t = b / (2.0 * a)
    return t * t


def quadratic_roots(a: float, b: float, c: float) -> tuple[float, float]:
    if a == 0:
        raise ValueError("a must be non-zero")
    disc = b * b - 4.0 * a * c
    if disc < 0:
        raise ValueError("real-roots reference kernel requires discriminant >= 0")
    r = sqrt(disc)
    return ((-b + r) / (2.0 * a), (-b - r) / (2.0 * a))


def conserved(before: float, after: float, *, eps: float = EPS) -> bool:
    return isclose(before, after, rel_tol=eps, abs_tol=eps)


def self_check() -> dict[str, bool]:
    L = 1.0
    a1, a2 = 7.0, 5.0
    b1, b2 = transfer_area(a1, a2, 1.25)
    side = 1.0
    h = isosceles_height(side, side)  # equilateral is a special isosceles case

    checks = {
        "transfer_conserves_area": conserved(a1 + a2, b1 + b2),
        "s30_inverse": conserved(L, s30_inverse(s30(L))),
        "s2_inverse": conserved(L, s2_inverse(s2(L))),
        "s30_squared_is_3_over_4": conserved(s30(s30(L)), 0.75 * L),
        "equilateral_height": conserved(h, sqrt(3.0) / 2.0),
        "shear_preserves_area": conserved(shear_area_scale(42.0), 1.0),
        "signed_area_cancels": conserved(
            total_signed_area([SignedArea(3.0, +1), SignedArea(1.0, -1)]), 2.0
        ),
    }
    return checks


if __name__ == "__main__":
    checks = self_check()
    for name, ok in checks.items():
        print(f"{name}: {'PASS' if ok else 'FAIL'}")
    raise SystemExit(0 if all(checks.values()) else 1)
