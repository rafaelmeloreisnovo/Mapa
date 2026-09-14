# RAFCODE-Φ — Vector, Memory Routing, Index/Atlas Integration — V1

Status: `DRAFT_EVIDENCE_ROUTING`
Date: `2026-09-13`
Author context: `∆RafaelVerboΩ`
Policy: `APPEND_ONLY | PROVENANCE_FIRST | TOKEN_VAZIO_VALID`
Global claim: `claim_allowed=false`

## 0. Objective

Consolidate the current-session findings around `RAFCODE-Φ / RAFCODEphi / RAFCODE_PHI`, vector semantics, memory/index routing, and the path toward benchmark correlation without converting structural indices into unsupported physical performance claims.

Canonical resolution chain:

`objective → authority → route → evidence → gate → delta → index`

Separation rule:

`VISION ≠ ARTIFACT ≠ EXECUTION ≠ EVIDENCE ≠ CLAIM`

## 1. Search aliases

Two search methods are canonical for this family:

### A. Symbolic search

- `RAFCODE-Φ`
- `Φ`

### B. ASCII/normalized search

- `RAFCODE PHI`
- `RAFCODE_PHI`
- `rafcode_phi`
- `RAFCODEphi`

Do not merge `Φ` with `π` or `θ` semantically. They may be visually confusable in informal notation, but remain distinct symbols.

## 2. Evidence located

### 2.1 Vectras bridge

Source:

`rafaelmeloreisnovo/Vectras-VM-Android/docs/active/VECTRA_RAFCODE_PHI_BRIDGE.md`

Documented pipeline:

`mnemonic → C parser → opcode_hex → emit_word_abi → ASM store → stats/CRC → VecBit/Hamming/hash-chain`

Documented structure:

`tools/baremetal/rafcode_phi/`

- `include/rafcode_phi_abi.h`
- `c/rafcode_phi_front_shell.c`
- `c/rafcode_phi_vecbit.c`
- `asm/rafcode_phi_emit_word.S`

Documented roles:

- C shell: validation, preparation, token→hex, local CRC32C.
- ASM core: materializes the 32-bit word into the buffer.
- VecBit: measures neighborhood by Hamming distance and FNV-1a hash-chain.
- Binary/header layer: architecture, word count, CRC32C, flags.

### 2.2 Private low-level implementation

Located paths:

- `Rafaelia_Private/Low-level/rafcode_phi_impl.c`
- `Rafaelia_Private/Low-level/rafcode_phi_core.h`

These establish that `RAFCODE-Φ` is not only a symbolic label; code artifacts exist.

### 2.3 Drive continuity

Drive contains copies/references such as:

- `RAFCODE_PHI_COMPILER_HEADER.md`
- `README_append_RAFCODE-PHI*.md`
- `GaiaPhiRafcode/`
- longitudinal/registry material that references RAFCODE families.

## 3. Vector semantics

The current defensible vector link is `VecBit`.

For words `a,b`:

`d_H(a,b) = popcount(a XOR b)`

Allowed use:

- compare neighboring emitted words;
- measure structural change along a chain;
- feed route/walk heuristics;
- compare transforms without pretending the result is FLOPS/IOPS;
- anchor later benchmark correlation.

Not allowed:

- infer physical throughput from Hamming distance alone;
- infer causality from vector proximity;
- replace ECC/FEC recovery by vector similarity;
- fill unknown state as zero.

## 4. Structural benchmark model

Legacy absolute figures from conceptual discussions must not be treated as measured physical performance unless backed by a reproducible benchmark receipt.

Use two layers:

### Physical benchmark

`B_HW = {throughput, latency_p50, latency_p95, latency_p99, bandwidth, energy, power, error_rate}`

### Structural benchmark

`B_STRUCT = {vector_width, state_density, locality, hamming_transition, redundancy, reconstruction_rate, utilization, parallelism}`

A structural gain index may be defined only as a model variable, for example:

`G_struct = useful_work_variant / useful_work_baseline`

It is not FLOPS until a FLOPS benchmark closes that gate.

## 5. Voltage/state programming note

`voltage-state programming ≠ overclock`

Overclock concerns clock-frequency increase beyond a nominal regime. Voltage can participate in state representation, DVFS, signaling margins, and multi-level encoding, but requires measured margins/noise/error rates before performance or reliability claims.

For `M` distinguishable states, ideal information capacity per symbol is:

`b = log2(M)`

This is an information-theoretic capacity expression, not a hardware throughput claim.

## 6. Base/state sequences

Current session expressions around `2 → 20 → 40 → 60` remain split into three possible meanings:

1. radix/base notation;
2. number of distinguishable states;
3. structural scale/index.

Only the arithmetic identities are immediately established:

- `2 × 10 = 20`
- `2 × 20 = 40`
- `20 × 3 = 60`

No canonical operator for the full transformation chain is closed yet.

State: `TOKEN_VAZIO_OPERATOR`.

## 7. Memory/index organization target

This document is a producer/reference artifact. Canonical routing should connect it to:

- START HERE / bootstrap entry;
- Master Navigation Registry;
- longitudinal/orthogonal memory indexes;
- atlas/gap routes;
- RAFCODE/VecBit/Vectras producer authority;
- later benchmark evidence from export material.

The terms `LTO`, `CPD`, and `U` require exact source resolution before hard-coding their ontology. Until their current canonical definitions are retrieved:

- `LTO = TOKEN_VAZIO_CANONICAL_EXPANSION`
- `CPD = TOKEN_VAZIO_CANONICAL_EXPANSION`
- `U = TOKEN_VAZIO_CANONICAL_EXPANSION`

Do not infer expansions from abbreviation alone.

## 8. Benchmark route

Next evidence path:

`RAFCODE-Φ code → VecBit/ABI/ASM properties → reproducible local test → export benchmark records → normalization → comparison → claim gate`

Required benchmark fields where available:

- source/export identifier;
- timestamp;
- device/runtime;
- build/commit;
- workload;
- input size;
- repetitions;
- latency distribution;
- throughput;
- memory/bandwidth;
- energy/power if observed;
- error/reconstruction counters;
- confidence/variance;
- receipt/hash.

## 9. Heuristic layer

Use heuristics only as candidate generators:

1. provenance;
2. recurrence;
3. baseline/null comparison;
4. compression/minimum-description;
5. invariance;
6. symmetry;
7. modular relation;
8. parity;
9. reversibility;
10. orthogonal confirmation;
11. graph centrality;
12. multi-scale recurrence;
13. conservation;
14. contradiction/falsifier;
15. minimum assumption cost;
16. reproduction;
17. structural locality;
18. evidence gate.

`heuristic_result ≠ proof`.

## 10. Current evidence state

`F_ok`

- `RAFCODE-Φ` naming family located by symbolic and ASCII-normalized search.
- Concrete C/ASM/HEX implementation paths located.
- `VecBit` documented as Hamming + FNV-chain neighborhood measure.
- CRC32C/header/32-bit word pipeline documented.
- Structural-vs-physical benchmark separation formalized.

`F_gap`

- exact canonical meaning of `LTO`, `CPD`, and `U` still unresolved in this write;
- exact artifact named `half code` not located as canonical component;
- export benchmark correlation not yet executed;
- physical performance claims remain closed.

`F_next`

1. Resolve `LTO`, `CPD`, `U` from current canonical memory/index sources.
2. Update Master Navigation Registry/START HERE routing with exact meanings and this artifact.
3. Inspect `rafcode_phi_vecbit.c`, ABI, and ASM quantitatively.
4. Correlate against benchmark records in the designated export corpus.

`claim_allowed=false`
