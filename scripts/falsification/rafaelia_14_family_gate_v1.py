#!/usr/bin/env python3
"""RAFAELIA — deterministic local falsification probes — HYP_CKPT_0008.

Scope is deliberately narrow. The BITRAF probes replicate the algorithm currently
observed in instituto-Rafael/Eletron-efeitos-qu-ntico/scripts/bitraf_simulator.py.
They test that implementation only; they do not refute the broader BITRAF64 formal
candidate. No physical-device or experimental-quantum claim is produced.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

SEED = 20260814
DIMS = (2, 3, 4, 8)
SAMPLES = 10_000


def current_bitraf_encode(amplitudes: np.ndarray) -> list[int]:
    amplitudes = np.asarray(amplitudes, dtype=complex)
    norm = np.linalg.norm(amplitudes)
    if not np.isclose(norm, 1.0):
        amplitudes = amplitudes / norm
    codes: list[int] = []
    for amp in amplitudes:
        magnitude = np.abs(amp)
        phase = np.angle(amp)
        mag_code = int(magnitude * 5) % 5
        phase_code = 5 + int((phase + np.pi) / (2 * np.pi) * 5) % 5
        codes.extend([mag_code, phase_code])
    return codes


def current_bitraf_decode(codes: list[int]) -> np.ndarray:
    amplitudes: list[complex] = []
    for i in range(0, len(codes), 2):
        if i + 1 >= len(codes):
            break
        mag_code = codes[i] % 5
        phase_code = codes[i + 1] % 5
        magnitude = mag_code / 5.0
        phase = (phase_code / 5.0) * 2 * np.pi - np.pi
        amplitudes.append(magnitude * np.exp(1j * phase))
    out = np.asarray(amplitudes, dtype=complex)
    norm = np.linalg.norm(out)
    if norm > 0:
        out = out / norm
    return out


def fidelity(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) != len(b):
        raise ValueError("dimension mismatch")
    return float(np.abs(np.vdot(a, b)) ** 2)


def probe_bitraf_roundtrip() -> dict:
    rng = np.random.default_rng(SEED)
    per_dim = {}
    for d in DIMS:
        fids = []
        for _ in range(SAMPLES):
            z = rng.normal(size=d) + 1j * rng.normal(size=d)
            z = z / np.linalg.norm(z)
            y = current_bitraf_decode(current_bitraf_encode(z))
            fids.append(fidelity(z, y))
        arr = np.asarray(fids)
        per_dim[str(d)] = {
            "mean_fidelity": float(arr.mean()),
            "median_fidelity": float(np.median(arr)),
            "min_fidelity": float(arr.min()),
        }
    return {
        "seed": SEED,
        "samples_per_dimension": SAMPLES,
        "dimensions": per_dim,
        "state": "CURRENT_IMPLEMENTATION_IS_LOSSY_IN_THIS_SAMPLE",
    }


def probe_basis_vectors() -> dict:
    rows = {}
    all_zero = True
    for d in DIMS:
        x = np.zeros(d, dtype=complex)
        x[0] = 1.0 + 0.0j
        codes = current_bitraf_encode(x)
        decoded = current_bitraf_decode(codes)
        norm = float(np.linalg.norm(decoded))
        all_zero = all_zero and norm == 0.0
        rows[str(d)] = {"codes": codes, "decoded_norm": norm}
    return {
        "dimensions": rows,
        "all_tested_basis_vectors_decode_to_zero_norm": all_zero,
        "cause": "mag_code=int(1*5)%5=0",
        "state": "IMPLEMENTATION_DEFECT_CONFIRMED_IN_CURRENT_SIMULATOR" if all_zero else "NOT_CONFIRMED",
    }


def probe_named_hadamard() -> dict:
    rows = {}
    for d in DIMS:
        h = np.ones((d, d), dtype=float) / np.sqrt(d)
        rows[str(d)] = {
            "rank": int(np.linalg.matrix_rank(h)),
            "unitarity_frobenius_error": float(np.linalg.norm(h.T @ h - np.eye(d), ord="fro")),
        }
    return {
        "matrix": "ones(n,n)/sqrt(n)",
        "dimensions": rows,
        "state": "NON_UNITARY_CURRENT_IMPLEMENTATION",
    }


def fibonacci_numbers(n: int) -> list[int]:
    f = [0, 1]
    while len(f) <= n:
        f.append(f[-1] + f[-2])
    return f


def probe_fibonacci_rafael() -> dict:
    seq = [2, 4, 7, 12, 20, 33, 54]
    recurrence_ok = all(seq[i] == seq[i - 1] + seq[i - 2] + 1 for i in range(2, len(seq)))
    f = fibonacci_numbers(len(seq) + 4)
    formula = [f[n + 3] - 1 for n in range(1, len(seq) + 1)]
    return {
        "sequence": seq,
        "recurrence_ok": recurrence_ok,
        "f_n_plus_3_minus_1_1_based": formula,
        "formula_matches": formula == seq,
        "state": "M0_M1_KNOWN_EQUIVALENCE" if recurrence_ok and formula == seq else "UNRESOLVED",
    }


def probe_mod42() -> dict:
    q, r = divmod(2**16, 42)
    return {
        "domain_size": 2**16,
        "modulus": 42,
        "quotient": q,
        "remainder": r,
        "residues_with_q_plus_1_preimages": r,
        "residues_with_q_preimages": 42 - r,
        "state": "EXACT_UNIFORMITY_REFUTED_WITHOUT_CORRECTION" if r else "EXACT_UNIFORMITY_POSSIBLE",
    }


def probe_sqrt3_over_2() -> dict:
    a = math.sqrt(3.0) / 2.0
    return {
        "a": a,
        "lambda_ln_abs_a": math.log(abs(a)),
        "is_linear_contraction": abs(a) < 1.0,
        "state": "LINEAR_CONTRACTION_ONLY_NOT_UNIVERSALITY_PROOF",
    }


def run_all() -> dict:
    return {
        "schema": "RAFAELIA_14_FAMILY_LOCAL_GATE_OUTPUT_V1",
        "checkpoint": "HYP_CKPT_0008",
        "execution_class": "CONTAINER_OR_LOCAL_REFERENCE_ONLY",
        "claim_allowed": False,
        "scope_boundary": "NO_PHYSICAL_QUANTUM_EVIDENCE",
        "probes": {
            "bitraf_roundtrip": probe_bitraf_roundtrip(),
            "bitraf_basis_vectors": probe_basis_vectors(),
            "bitraf_named_hadamard": probe_named_hadamard(),
            "fibonacci_rafael": probe_fibonacci_rafael(),
            "mod42": probe_mod42(),
            "sqrt3_over_2": probe_sqrt3_over_2(),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, help="optional JSON output path")
    args = parser.parse_args()
    result = run_all()
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
