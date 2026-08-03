#!/usr/bin/env python3
"""Generate the deterministic 5-12-13 multibase/circular-arc dataset.

The generator uses only Python's standard library.  It distinguishes value from
representation and Euclidean equality from equality after a modulo projection.
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


ARTIFACT_ID = "PYTH-5-12-13-MULTIBASE-ARC-V1"
SPEC_DATE = "2026-08-02"
MAX_MATERIALIZED_BASE = 225

VALUES: Tuple[Tuple[str, int], ...] = (
    ("leg_a", 5),
    ("leg_b", 12),
    ("hypotenuse_corrected", 13),
    ("hypotenuse_proposed", 15),
    ("leg_a_squared", 25),
    ("previous_square", 144),
    ("corrected_square", 169),
    ("proposed_square", 225),
)

HIGHLIGHTED_BASES: Tuple[int, ...] = (
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    12,
    13,
    15,
    16,
    20,
    25,
    36,
    60,
    64,
    70,
    144,
    169,
    225,
)

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def positional_digits(value: int, base: int) -> List[int]:
    """Return most-significant-first digits for a non-negative integer."""
    if value < 0:
        raise ValueError("value must be non-negative")
    if base < 2:
        raise ValueError("positional base must be at least 2")
    if value == 0:
        return [0]

    digits: List[int] = []
    current = value
    while current:
        current, digit = divmod(current, base)
        digits.append(digit)
    return list(reversed(digits))


def evaluate_digits(digits: Sequence[int], base: int) -> int:
    """Evaluate most-significant-first positional digits."""
    value = 0
    for digit in digits:
        if digit < 0 or digit >= base:
            raise ValueError("digit outside base")
        value = value * base + digit
    return value


def display_digits(digits: Sequence[int], base: int) -> str:
    """Use ordinary symbols through base 36 and bracket digits above it."""
    if base <= len(ALPHABET):
        body = "".join(ALPHABET[digit] for digit in digits)
    else:
        body = "".join("[{}]".format(digit) for digit in digits)
    return "{}_{}".format(body, base)


def fraction_record(value: Fraction) -> Dict[str, object]:
    decimal = "{:.12f}".format(float(value)).rstrip("0").rstrip(".")
    if not decimal:
        decimal = "0"
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": decimal,
    }


def positive_divisors(value: int) -> List[int]:
    if value <= 0:
        raise ValueError("value must be positive")
    return [candidate for candidate in range(1, value + 1) if value % candidate == 0]


def arc_position(value: int, base: int) -> Dict[str, object]:
    residue = value % base
    return {
        "residue": residue,
        "turn_fraction": fraction_record(Fraction(residue, base)),
        "angle_degrees": fraction_record(Fraction(360 * residue, base)),
    }


def value_views() -> List[Dict[str, object]]:
    records: List[Dict[str, object]] = []
    for value_id, value in VALUES:
        records.append(
            {
                "id": value_id,
                "decimal": value,
                "literal_degree_circle": {
                    "residue": value % 360,
                    "angle_degrees": fraction_record(Fraction(value % 360, 1)),
                },
                "clock_60_circle": {
                    "residue": value % 60,
                    "angle_degrees": fraction_record(Fraction(6 * (value % 60), 1)),
                },
            }
        )
    return records


def sentinel_record(symbol: str, reason: str) -> Dict[str, object]:
    return {
        "record_type": "base_sentinel",
        "symbol": symbol,
        "radix_state": "NOT_A_CONVENTIONAL_NUMERIC_RADIX",
        "representation": "TOKEN_VAZIO",
        "arc_position": "TOKEN_VAZIO",
        "reason": reason,
    }


def base_record(base: int) -> Dict[str, object]:
    if base < 1:
        raise ValueError("materialized base must be positive")

    if base == 1:
        digits = [[1] * value for _, value in VALUES]
        residues = [0 for _ in VALUES]
        angles = [[0, 1] for _ in VALUES]
        kind = "UNARY_NON_POSITIONAL"
        corrected_identity = True
        proposed_alias = True
        proposed_residual = 0
    else:
        digits = [positional_digits(value, base) for _, value in VALUES]
        residues = [value % base for _, value in VALUES]
        angles = []
        for residue in residues:
            angle = Fraction(360 * residue, base)
            angles.append([angle.numerator, angle.denominator])
        kind = "POSITIONAL_INTEGER"
        corrected_identity = (25 % base + 144 % base) % base == 169 % base
        proposed_residual = (225 - 25 - 144) % base
        proposed_alias = proposed_residual == 0

    return {
        "record_type": "base",
        "base": base,
        "kind": kind,
        "highlighted": base in HIGHLIGHTED_BASES,
        "digits_msd_first": digits,
        "arc_residues": residues,
        "arc_angle_degrees_rational": angles,
        "checks": {
            "corrected_pythagorean_identity_mod_base": corrected_identity,
            "proposed_15_aliases_corrected_square_mod_base": proposed_alias,
            "proposed_15_residual_mod_base": proposed_residual,
        },
    }


def collision_bases(left: int, right: int, upper: int) -> List[int]:
    difference = abs(left - right)
    if difference == 0:
        return list(range(2, upper + 1))
    return [base for base in positive_divisors(difference) if 2 <= base <= upper]


def header_record() -> Dict[str, object]:
    return {
        "record_type": "manifest",
        "schema": "rafaelia.pythagorean-multibase-arc.v1",
        "artifact_id": ARTIFACT_ID,
        "spec_date": SPEC_DATE,
        "claim_allowed": False,
        "scope": {
            "materialized_positive_integer_bases": [1, MAX_MATERIALIZED_BASE],
            "parametric_positional_scope": "every integer base b >= 2",
            "reason_for_upper_bound": (
                "225 is the largest tracked value; for b > 225 all tracked values "
                "are single digits, while the generator remains parametric"
            ),
            "excluded_radices": {
                "negative": "TOKEN_VAZIO_SCOPE",
                "balanced": "TOKEN_VAZIO_SCOPE",
                "non_integer": "TOKEN_VAZIO_SCOPE",
                "complex": "TOKEN_VAZIO_SCOPE",
            },
        },
        "base_record_columns": {
            "value_order": [value_id for value_id, _ in VALUES],
            "digits_msd_first": "one digit array per value_order entry",
            "arc_residues": "n mod base, in value_order",
            "arc_angle_degrees_rational": "[numerator, denominator] for 360*(n mod base)/base",
        },
        "values": value_views(),
        "identities": [
            {
                "id": "PYTH-EXACT-001",
                "expression": "5^2 + 12^2 = 13^2 = 169",
                "epistemic_state": "PROVADO_ARITMETICAMENTE",
            },
            {
                "id": "CONSECUTIVE-SQUARE-GAP-001",
                "expression": "13^2 - 12^2 = 169 - 144 = 25 = 5^2",
                "epistemic_state": "PROVADO_ARITMETICAMENTE",
            },
            {
                "id": "PROPOSED-15-RESIDUAL-001",
                "expression": "15^2 - 5^2 - 12^2 = 56",
                "epistemic_state": "PROVADO_ARITMETICAMENTE",
            },
            {
                "id": "CORRELATED-UNCERTAINTY-001",
                "expression": "225 = 25 + 144 + 2*rho*5*12 => rho = 7/15",
                "epistemic_state": "MODELO_CONDICIONAL",
            },
            {
                "id": "HIDDEN-ORTHOGONAL-001",
                "expression": "u_hidden = sqrt(225 - 169) = sqrt(56)",
                "epistemic_state": "MODELO_ALTERNATIVO_CONDICIONAL",
            },
        ],
        "circle_conventions": {
            "radix_circle": "theta_b(n) = 360 degrees * (n mod b) / b",
            "literal_degree_circle": "theta_360(n) = n mod 360 degrees",
            "clock_60_circle": "theta_60(n) = 6 degrees * (n mod 60)",
            "warning": "modular coincidence is projection aliasing, not Euclidean equality",
        },
        "highlighted_bases": list(HIGHLIGHTED_BASES),
    }


def summary_record() -> Dict[str, object]:
    proposed_alias_bases = collision_bases(169, 225, MAX_MATERIALIZED_BASE)
    return {
        "record_type": "summary",
        "artifact_id": ARTIFACT_ID,
        "materialized_base_count": MAX_MATERIALIZED_BASE,
        "corrected_identity_failure_bases": [],
        "circular_aliases": [
            {
                "values": [5, 12],
                "difference": 7,
                "bases": collision_bases(5, 12, MAX_MATERIALIZED_BASE),
                "meaning": "the two legs occupy the same radix-circle position",
            },
            {
                "values": [144, 169],
                "difference": 25,
                "bases": collision_bases(144, 169, MAX_MATERIALIZED_BASE),
                "meaning": "the previous and corrected squares alias",
            },
            {
                "values": [169, 225],
                "difference": 56,
                "bases": proposed_alias_bases,
                "meaning": "the corrected and proposed squares alias",
            },
        ],
        "proposed_15_false_positive_modular_bases": proposed_alias_bases,
        "key_observation": (
            "bases dividing 56 cannot distinguish 13^2 from 15^2 after modulo projection"
        ),
    }


def records() -> Iterable[Mapping[str, object]]:
    yield header_record()
    yield sentinel_record(
        "EMPTY_SET",
        "The empty-set marker is an epistemic/semantic state, not a radix.",
    )
    yield sentinel_record(
        "0",
        "Conventional positional base zero has no unique place-value representation.",
    )
    for base in range(1, MAX_MATERIALIZED_BASE + 1):
        yield base_record(base)
    yield summary_record()


def render_jsonl() -> str:
    return "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
        for record in records()
    )


def validate() -> None:
    assert 5 * 5 + 12 * 12 == 13 * 13 == 169
    assert 13 * 13 - 12 * 12 == 5 * 5 == 25
    assert 15 * 15 - 5 * 5 - 12 * 12 == 56
    assert Fraction(225 - 25 - 144, 2 * 5 * 12) == Fraction(7, 15)
    assert positive_divisors(56) == [1, 2, 4, 7, 8, 14, 28, 56]

    for base in range(2, MAX_MATERIALIZED_BASE + 1):
        for _, value in VALUES:
            digits = positional_digits(value, base)
            assert evaluate_digits(digits, base) == value
        assert (25 % base + 144 % base) % base == 169 % base


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        type=Path,
        help="compare generated bytes with an existing JSONL artifact",
    )
    args = parser.parse_args(argv)

    validate()
    generated = render_jsonl()
    if args.check is not None:
        existing = args.check.read_text(encoding="utf-8")
        if existing != generated:
            print("FAIL: dataset differs from deterministic generator", file=sys.stderr)
            return 1
        print("PASS: deterministic dataset matches generator")
        return 0

    sys.stdout.write(generated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
