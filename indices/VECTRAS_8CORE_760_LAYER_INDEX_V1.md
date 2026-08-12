# Vectras 8-core × 760+ logical-layer index — V1

Date: 2026-08-12
Mode: APPEND_ONLY
claim_allowed: false

## Route

`NOVOexport 048-050 -> Drive Stage-1 metrics -> Vectras static producer evidence -> Mapa evidence delta -> benchmark gate -> runtime receipt -> claim review`

## Canonical records

- Documentation: `docs/canonical/2026-08-12/VECTRAS_8CORE_760_LAYER_EVIDENCE_DELTA_V1.md`
- Machine-readable evidence: `data/evidence/vectras/vectras-8core-760-layer-evidence-2026-08-12.v1.json`
- Producer repo: `rafaelmeloreisnovo/Vectras-VM-Android`
- Producer pinned commit: `21ad17f89ce2bf29cb0d8c184c612d76a99a9b3d`
- Drive Stage-1 authority: provider id `1ccOoYooH-STuDvrPQQSihtg4nqpmifd7QQ8w25nIr1w`

## Key distinction

`8 executors != 760 physical cores`.

`760+` currently denotes a logical `color_layers` / layer-view space in pinned BITWALK/BITGHOST source. The explicit 8-vCPU path is a separate producer artifact. Their runtime coupling remains gated.

## Priority gaps

P0:
- `TOKEN_VAZIO_RUNTIME_8x760_RECEIPT`
- `TOKEN_VAZIO_DEVICE_RECEIPT_CURRENT`

P1:
- `TOKEN_VAZIO_PERFORMANCE_SCALING`
- `TOKEN_VAZIO_PARALLELISM_SEMANTICS`

P1 provenance:
- `TOKEN_VAZIO_NOVOEXPORT_VERSION_RECONCILIATION`

## Promotion rule

No claim of 760-way physical parallelism, 760-core equivalence, acceleration ratio, or superiority may be promoted until a pinned benchmark receipt closes the corresponding gap.
