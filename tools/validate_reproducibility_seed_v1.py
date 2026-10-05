#!/usr/bin/env python3
"""Validate the canonical RAFAELIA reproducibility seed.

This gate is stdlib-only and fail-closed. It binds a numeric seed to an exact
GitHub lockfile observation, but deliberately does not claim that a fixed seed
is a complete PRNG state, cross-library stream identity, or scientific
replication.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/control-plane/omega-assurance/reproducibility-seed.v1.json"

EXPECTED_SEED = 1748365262
EXPECTED_IDENTITY = "RAFAELIA_SEED_1748365262_a6a1f608-b889-4803-8f59-d57ce00dba1b"
EXPECTED_SOURCE = {
    "repository": "rafaelmeloreisnovo/home",
    "path": ".rafaelia/core/id_seed.lock",
    "commit": "d5e32a4c07c5f0c328a8dd85d1b3302e930dae47",
    "blob_sha": "8c04ed93932d00efff94c03d98bc572b8cff9afe",
}
REQUIRED_ANCHORS = {"arXiv:2609.26461", "arXiv:2608.27100"}
REQUIRED_BOUNDARIES = {
    "SEED_IDENTITY != FULL_PRNG_STATE",
    "SEED_EQUALITY != CROSS_LIBRARY_STREAM_IDENTITY",
    "FIXED_SEED != SCIENTIFIC_REPLICATION",
    "DETERMINISTIC_DERIVATION != CRYPTOGRAPHIC_SECRET",
    "GATE_PASS != SCIENTIFIC_VALIDATION",
    "SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM",
}


def load(path: Path = MANIFEST) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be object")
    return value


def derive_u64(seed: int, label: str) -> int:
    """Stable derivation for ordering/receipt identity; not a PRNG claim."""
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("seed must be an integer")
    if not isinstance(label, str) or not label:
        raise ValueError("label must be a non-empty string")
    payload = b"RAFAELIA_SEED_V1\0" + str(seed).encode("ascii") + b"\0" + label.encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if manifest.get("schema_version") != "rafaelia.reproducibility-seed/v1":
        errors.append("schema_version_mismatch")
    if manifest.get("gate_id") != "REPRODUCIBILITY_SEED_V1":
        errors.append("gate_id_mismatch")
    if manifest.get("claim_allowed") is not False:
        errors.append("claim_allowed_must_remain_false")
    if manifest.get("closure_is_automatic") is not False:
        errors.append("automatic_closure_forbidden")

    seed = manifest.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int):
        errors.append("seed_must_be_integer")
    elif seed != EXPECTED_SEED:
        errors.append("canonical_seed_mismatch")

    identity = manifest.get("seed_identity")
    if identity != EXPECTED_IDENTITY:
        errors.append("canonical_seed_identity_mismatch")
    if isinstance(identity, str):
        match = re.fullmatch(r"RAFAELIA_SEED_(\d+)_([0-9a-f-]{36})", identity)
        if not match:
            errors.append("seed_identity_format_invalid")
        elif isinstance(seed, int) and int(match.group(1)) != seed:
            errors.append("seed_identity_numeric_mismatch")
    else:
        errors.append("seed_identity_must_be_string")

    source = manifest.get("source")
    if not isinstance(source, dict):
        errors.append("source_must_be_object")
    else:
        for key, expected in EXPECTED_SOURCE.items():
            if source.get(key) != expected:
                errors.append(f"source_{key}_mismatch")
        if source.get("authority_state") != "OBSERVED_LOCKFILE":
            errors.append("source_authority_state_mismatch")

    derivation = manifest.get("deterministic_derivation")
    if not isinstance(derivation, dict):
        errors.append("deterministic_derivation_must_be_object")
    else:
        if derivation.get("algorithm") != "SHA-256":
            errors.append("derivation_algorithm_mismatch")
        if derivation.get("domain") != "RAFAELIA_SEED_V1":
            errors.append("derivation_domain_mismatch")
        if derivation.get("input_format") != "RAFAELIA_SEED_V1\\0{seed}\\0{label}":
            errors.append("derivation_input_format_mismatch")
        if derivation.get("output") != "first_64_bits_big_endian":
            errors.append("derivation_output_mismatch")

    mutation = manifest.get("mutation_falsifier")
    if not isinstance(mutation, dict):
        errors.append("mutation_falsifier_must_be_object")
    else:
        if mutation.get("operator") != "N_TO_N_PLUS_1":
            errors.append("mutation_operator_mismatch")
        if mutation.get("baseline_seed") != EXPECTED_SEED:
            errors.append("mutation_baseline_seed_mismatch")
        if mutation.get("mutant_seed") != EXPECTED_SEED + 1:
            errors.append("mutation_seed_not_n_plus_1")

    anchors = {
        item.get("ref")
        for item in manifest.get("method_anchors", [])
        if isinstance(item, dict) and isinstance(item.get("ref"), str)
    }
    if not REQUIRED_ANCHORS.issubset(anchors):
        errors.append("required_method_anchors_missing")

    boundaries = set(manifest.get("boundaries", []))
    if not REQUIRED_BOUNDARIES.issubset(boundaries):
        errors.append("required_boundaries_missing")

    return sorted(set(errors))


def run(manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    manifest = manifest if manifest is not None else load()
    errors = validate_manifest(manifest)
    seed = manifest.get("seed")
    probe = None
    if isinstance(seed, int) and not isinstance(seed, bool):
        probe = derive_u64(seed, "TOKEN_VAZIO_CLOSURE_READINESS_V1")
    return {
        "schema_version": "rafaelia.reproducibility-seed-receipt/v1",
        "status": "PASS" if not errors else "FAIL",
        "gate_id": "REPRODUCIBILITY_SEED_V1",
        "canonical_seed": EXPECTED_SEED,
        "derived_probe_u64": probe,
        "source_commit": EXPECTED_SOURCE["commit"],
        "source_blob_sha": EXPECTED_SOURCE["blob_sha"],
        "claim_allowed": False,
        "semantics": "PASS binds the canonical seed and derivation contract only; it is not proof of PRNG portability or scientific replication.",
        "errors": errors,
    }


def main() -> int:
    receipt = run()
    print(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
