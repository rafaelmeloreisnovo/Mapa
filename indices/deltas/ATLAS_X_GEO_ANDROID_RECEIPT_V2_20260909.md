# ATLAS:X — Geo Android ARM Receipt V2 — 2026-09-09

Object ID: `ATLAS-X-GEO-ANDROID-RECEIPT-V2-20260909`  
Mode: `APPEND_ONLY / DEVICE_EVIDENCE_ROUTE / claim_allowed=false`

## Producer

`ZIPRAF_CORE#11` — Android ARM physical-receipt V2 harness.

## Predecessors

- `ZIPRAF_CORE#10` merged: GeoWord + structural binding mechanism;
- `Mapa#575/#576` merged: round2 + semantic-authority input contract;
- `MemRafcode#16` merged: authority-input longitudinal successor;
- `Mapa#578` / `MemRafcode#17`: RafBit contextual-hypergraph axis, independent from physical runtime.

## Route

```text
SOURCE_HEAD
  -> native Android/ARM compile
  -> final loaderless ELF audit
  -> repeated native execution
  -> Android runtime identity observation
  -> optional explicit operator physical attestation
  -> receipt verifier
  -> GF008 bounded gate
  -> independent replication remains separate G015
```

## Closed bounded gaps

```text
GF008_ANDROID_ARM_RUNTIME_HARNESS  = CLOSED_IMPLEMENTED
GF008_ANDROID_ARM_RECEIPT_VERIFIER = CLOSED_IMPLEMENTED_TESTED_LOCAL
```

## Open observation gates

```text
GF008_ANDROID_ARM_RUNTIME = TOKEN_VAZIO_DEVICE_UNTIL_RECEIPT
GF008_PHYSICAL_ARM_RUNTIME = TOKEN_VAZIO_OPERATOR_ATTESTATION_UNTIL_RECEIPT
G015_INDEPENDENT_SECOND_PHYSICAL_ARCHITECTURE = TOKEN_VAZIO_EXTERNAL_GATE
```

## Receipt requirements

The V2 runtime receipt must bind:

- source HEAD;
- native ARM/AArch64 architecture;
- Android fingerprint and ABI;
- compiler identity;
- final ELF SHA-256;
- `.text/data/bss`;
- undefined symbols;
- runtime relocations;
- dynamic dependencies;
- at least 3 repeated native return codes;
- explicit operator physical-attestation state;
- independent-witness reference kept separate.

A runtime-only observation cannot self-promote to physical-device proof.

## Semantic separation

The structural binding fixture exercised by the full smoke is not semantic authority:

```text
semantic_authority=TOKEN_VAZIO_SEMANTIC_AUTHORITY
structural_binding_fixture_is_authority=false
```

## Invariants

```text
ANDROID_RUNTIME_OBSERVED != PHYSICAL_DEVICE_PROVED
OPERATOR_ATTESTED != INDEPENDENTLY_WITNESSED
STRUCTURAL_BINDING_FIXTURE != SEMANTIC_AUTHORITY
CROSS_LINK != NATIVE_EXECUTION
```

## Single next observable

Run the V2 harness natively in Termux/Android. If the operator is on a physical device, supply the exact explicit attestation token. Persist the produced receipt unchanged and validate it before any promotion.
