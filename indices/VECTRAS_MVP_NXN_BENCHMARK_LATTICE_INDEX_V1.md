# Vectras / MVP N^N Benchmark Lattice Index — V1

Date: 2026-08-12
Mode: APPEND_ONLY
Global claim_allowed: false

## Trigger terms

`MVP`, `N^N`, `benchmark`, `configuration space`, `BASE`, `UNROLL4`, `UNROLL8`, `raf_latency_benchmark`, `HPC_OMEGA`, `8x8`, `ARM32`, `046`, `047`, `048`, `049`, `050`.

## Reconstruction route

`NOVOexport 046–050 -> Stage-1 byte authority -> raw 046/047 historical terminal outputs -> MVP seed registry -> constrained configuration lattice -> replay receipts -> adaptive frontier -> claim review`

## Canonical records

- Lattice documentation: `docs/canonical/2026-08-12/VECTRAS_MVP_NXN_BENCHMARK_LATTICE_V1.md`
- Historical seed registry: `data/evidence/vectras/vectras-mvp-nxn-historical-seeds-2026-08-12.v1.json`
- Earlier 8×760 evidence: `docs/canonical/2026-08-12/VECTRAS_8CORE_760_LAYER_EVIDENCE_DELTA_V1.md`
- Stage-1 Drive authority: provider id `1ccOoYooH-STuDvrPQQSihtg4nqpmifd7QQ8w25nIr1w`

## Mathematical boundary

For heterogeneous configuration dimensions:

`|Omega_raw| = product_i(k_i)`.

Only in the symmetric case of `N` dimensions with `N` choices each:

`|Omega_raw| = N^N`.

This cardinality is not a physical-core count.

## Evidence boundary

Raw content re-read and SHA-matched in this pass:
- `046`: PASS
- `047`: PASS

Current raw-content access:
- `048`: TOKEN_VAZIO
- `049`: TOKEN_VAZIO
- `050`: TOKEN_VAZIO

Stage-1 byte counts/hashes for all five remain authoritative.

## Seed families already observed

1. ARM32 adaptive selector: BASE vs UNROLL4 vs UNROLL8.
2. CPU/MEM/cache benchmark with a corrected latency series superseding an earlier suspect series.
3. direct memory vs CPU vs indirect access.
4. 8×8 matrix/state evolution timing.
5. complex/toroidal simulation family.
6. HPC_OMEGA spectral/clustering alternatives with a degenerate-null-model statistical gap preserved.

## Explicit exclusion

BLAKE/BLAKE3 is not an MVP benchmark axis here. It may be used only as an integrity/receipt primitive when needed.

## No-regression rule

Negative, slower, corrected, superseded, or invalidated variants remain addressable evidence. They are never deleted merely because another configuration wins.

## F_next

`RAW_048_050_RECOVERY -> MVP_DEDUP -> MVP_CONFIG_V1 -> HISTORICAL_REPLAY -> CONSTRAINED_NXN_FRONTIER`.
