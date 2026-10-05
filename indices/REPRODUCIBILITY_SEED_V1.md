# REPRODUCIBILITY_SEED_V1

## Intent

Bind the existing RAFAELIA seed to a reproducible, auditable experiment identity without claiming that a fixed integer seed is a complete PRNG state or a proof of scientific replication.

## Canonical source

Observed GitHub lockfile:

```text
repository: rafaelmeloreisnovo/home
path: .rafaelia/core/id_seed.lock
commit: d5e32a4c07c5f0c328a8dd85d1b3302e930dae47
blob_sha: 8c04ed93932d00efff94c03d98bc572b8cff9afe
identity: RAFAELIA_SEED_1748365262_a6a1f608-b889-4803-8f59-d57ce00dba1b
seed: 1748365262
```

The numeric seed is therefore **source-bound**, not invented by the gate.

## Deterministic derivation

The gate does not depend on Python `random`, NumPy, PyTorch, TensorFlow or another library PRNG for its own case ordering/receipt identity.

```text
payload = UTF8("RAFAELIA_SEED_V1") || NUL || ASCII(seed) || NUL || UTF8(label)
digest  = SHA-256(payload)
derived = first 64 bits, big-endian
```

This produces a stable deterministic mapping for labels. It is **not** a claim of statistical randomness or a cryptographic secret.

## Mandatory falsifier

A controlled mutation is part of the contract:

```text
N = 1748365262
mutant = 1748365263
operator = N -> N + 1
```

The repository test must kill this mutation. If the seed changes and the gate remains green, the safeguard has failed.

This follows the reproducibility-testing principle that experimentally important configuration should be observable by validation rather than merely allowing software to complete successfully.

## Scientific boundary

Method anchors stored in the machine-readable manifest:

- arXiv:2609.26461 — *Reproducible AI Requires Reproducible Randomness*. Operational use: a seed alone can be insufficient for cross-library identical random streams; implementation fidelity and complete generator state can matter.
- arXiv:2608.27100 — *Mutation Testing for Reproducibility Safeguards in Machine Learning Research Software: An Empirical Study*. Operational use: controlled random-seed mutation is a reproducibility-relevant perturbation and validation workflows can be tested for sensitivity to it.

Therefore:

```text
SEED_IDENTITY != FULL_PRNG_STATE
SEED_EQUALITY != CROSS_LIBRARY_STREAM_IDENTITY
FIXED_SEED != SCIENTIFIC_REPLICATION
DETERMINISTIC_DERIVATION != CRYPTOGRAPHIC_SECRET
GATE_PASS != SCIENTIFIC_VALIDATION
SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM
```

## Files

- `data/control-plane/omega-assurance/reproducibility-seed.v1.json`
- `tools/validate_reproducibility_seed_v1.py`
- `tests/test_reproducibility_seed_v1.py`
- `indices/REPRODUCIBILITY_SEED_V1.md`
- `.github/workflows/serpent-dove-gap-metabolism-v1.yml`

## Local validation

```bash
python3 -m py_compile tools/validate_reproducibility_seed_v1.py
python3 -m py_compile tests/test_reproducibility_seed_v1.py
python3 -m unittest tests/test_reproducibility_seed_v1.py
python3 tools/validate_reproducibility_seed_v1.py
```

`PASS` means the seed identity, source provenance, deterministic derivation contract and mutation safeguard are internally consistent. It does **not** close a scientific claim or prove PRNG portability.

## Relation to TOKEN_VAZIO

The seed can now be used when a gate needs a stable deterministic experiment/case identity. It does not fill unrelated `TOKEN_VAZIO` fields. Unknown source, authority, execution target or evidence still remains `TOKEN_VAZIO`.

R3=<F_ok: canonical seed source-bound + deterministic derivation + N->N+1 mutation falsifier; F_gap: exact-head CI and independent review; F_next: run CI on the implementation head and preserve HOLD on any unrelated TOKEN_VAZIO>
