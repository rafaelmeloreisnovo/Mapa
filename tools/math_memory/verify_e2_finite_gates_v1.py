#!/usr/bin/env python3
"""Deterministic finite verifier for governed RAFAELIA E2 math-memory gates.

No third-party dependencies. This verifier intentionally covers only finite/exact
claims that can be checked with Python integers and finite enumeration:
- Fibonacci and Rafael +1 reversible recurrences;
- Rafaeliana shift R_n = F_{n+3} - 1 on a bounded exact range;
- XOR involution for known masks;
- cardinality falsifier for a 10-bit state -> mod-20 mask injectivity claim;
- multi-base residue embedding Pi(n) over moduli 7/10/12/20, including
  exact period 420, generalized-CRT compatibility and inverse modulo 420.

It does NOT prove cryptographic security, scientific claims, novelty, or global
formula-corpus completeness.
"""

from __future__ import annotations

import itertools
import json
import math
from typing import Dict, List, Sequence, Tuple

MODULI: Tuple[int, ...] = (7, 10, 12, 20)
PERIOD = math.lcm(*MODULI)


def pi_tuple(n: int) -> Tuple[int, int, int, int]:
    return tuple(n % m for m in MODULI)  # type: ignore[return-value]


def crt_compatible(residues: Sequence[int]) -> bool:
    if len(residues) != len(MODULI):
        return False
    for i, mi in enumerate(MODULI):
        if not 0 <= residues[i] < mi:
            return False
        for j in range(i + 1, len(MODULI)):
            mj = MODULI[j]
            if (residues[i] - residues[j]) % math.gcd(mi, mj) != 0:
                return False
    return True


def build_inverse_mod420() -> Dict[Tuple[int, int, int, int], int]:
    inverse: Dict[Tuple[int, int, int, int], int] = {}
    for n in range(PERIOD):
        key = pi_tuple(n)
        if key in inverse:
            raise AssertionError(f"non-injective modulo {PERIOD}: {key}")
        inverse[key] = n
    return inverse


def verify_modular() -> dict:
    inverse = build_inverse_mod420()
    image = set(inverse)
    assert len(image) == PERIOD == 420

    assert all(pi_tuple(n + PERIOD) == pi_tuple(n) for n in range(PERIOD))
    smaller_periods = [
        p
        for p in range(1, PERIOD)
        if all(pi_tuple(n + p) == pi_tuple(n) for n in range(PERIOD))
    ]
    assert smaller_periods == []

    compatible = {
        tuple(r)
        for r in itertools.product(*(range(m) for m in MODULI))
        if crt_compatible(r)
    }
    assert len(compatible) == PERIOD
    assert compatible == image

    for residues, n0 in inverse.items():
        assert pi_tuple(n0) == residues
        assert pi_tuple(n0 + PERIOD) == residues
        assert pi_tuple(n0 - PERIOD) == residues

    return {
        "moduli": list(MODULI),
        "period": PERIOD,
        "minimum_period": PERIOD,
        "unique_image_states": len(image),
        "raw_product_states": math.prod(MODULI),
        "generalized_crt_compatible_states": len(compatible),
        "image_equals_compatible_set": True,
        "inverse_mod420_roundtrips": len(inverse),
        "global_integer_inverse_unique": False,
        "global_preimage_form": "n0 + 420*Z",
        "example_42": {
            "residues": list(pi_tuple(42)),
            "inverse_mod420": inverse[pi_tuple(42)],
        },
    }


def verify_xor() -> dict:
    truth_cases = []
    for a in (0, 1):
        for m in (0, 1):
            ok = ((a ^ m) ^ m) == a
            truth_cases.append(ok)
            assert ok

    finite_checks = 0
    for a in range(32):
        for mask in range(20):
            assert ((a ^ mask) ^ mask) == a
            finite_checks += 1

    state_domain = 1 << 10
    mask_codomain = 20
    assert state_domain > mask_codomain
    pigeonhole_min_max_preimage = math.ceil(state_domain / mask_codomain)
    assert pigeonhole_min_max_preimage == 52

    return {
        "xor_involution_truth_cases": sum(truth_cases),
        "xor_involution_truth_total": len(truth_cases),
        "xor_finite_roundtrips": finite_checks,
        "known_mask_involution": True,
        "state_domain_10bit": state_domain,
        "mask_codomain_mod20": mask_codomain,
        "state_to_mask_injective_possible": False,
        "pigeonhole_minimum_max_preimage": pigeonhole_min_max_preimage,
    }


def fibonacci(count: int) -> List[int]:
    if count < 2:
        raise ValueError("count must be >= 2")
    out = [0, 1]
    for _ in range(2, count):
        out.append(out[-1] + out[-2])
    return out


def rafaeliana(max_n: int) -> List[int | None]:
    if max_n < 2:
        raise ValueError("max_n must be >= 2")
    r: List[int | None] = [None, 2, 4]
    for n in range(2, max_n):
        assert r[n] is not None and r[n - 1] is not None
        r.append(int(r[n]) + int(r[n - 1]) + 1)
    return r


def verify_recurrences() -> dict:
    f = fibonacci(205)
    r = rafaeliana(101)

    fib_reverse_checked = 0
    for n in range(1, 100):
        assert f[n - 1] == f[n + 1] - f[n]
        fib_reverse_checked += 1

    rafael_reverse_checked = 0
    for n in range(2, 100):
        assert r[n - 1] == int(r[n + 1]) - int(r[n]) - 1
        rafael_reverse_checked += 1

    shift_checked = 0
    for n in range(1, 101):
        assert r[n] == f[n + 3] - 1
        shift_checked += 1

    fib_forward = (-1, -1, 1)
    fib_reverse = (1, 1, -1)
    assert fib_reverse == tuple(-x for x in fib_forward)

    rafael_forward = (-1, -1, 1, -1)
    rafael_reverse = (1, 1, -1, 1)
    assert rafael_reverse == tuple(-x for x in rafael_forward)

    return {
        "fibonacci_reverse_checks": fib_reverse_checked,
        "rafael_reverse_checks": rafael_reverse_checked,
        "rafael_fibonacci_shift_checks": shift_checked,
        "fibonacci_residual_negation": True,
        "rafael_residual_negation": True,
        "rafael_initial_terms": [int(r[n]) for n in range(1, 8)],
    }


def main() -> int:
    result = {
        "schema": "RAFAELIA_E2_FINITE_GATES_RUNTIME_V1",
        "claim_allowed": False,
        "scope": "bounded exact finite verifier",
        "recurrence": verify_recurrences(),
        "gf2": verify_xor(),
        "modular": verify_modular(),
        "not_proved": [
            "cryptographic security",
            "scientific or physical mechanism",
            "novelty",
            "global formula-corpus exhaustivity",
        ],
        "overall": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
