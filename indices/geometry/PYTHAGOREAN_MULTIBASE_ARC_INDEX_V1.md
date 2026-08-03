# Índice navegável — 5–12–13 / 144→169 / arco multibase

**ID:** `IDX-PYTH-MULTIBASE-ARC-V1`  
**Data:** `2026-08-02`  
**Regra:** `APPEND_ONLY / POINTER_FIRST / claim_allowed=false`

## Entrada canônica

- `docs/canonical/2026-08-02/PYTHAGOREAN_5_12_13_MULTIBASE_CIRCULAR_ARC_V1.md`

## Grafo mínimo

| Papel | Artefato |
|---|---|
| contrato-mãe | `docs/canonical/2026-08-02/INVARIANTE_GEOMETRICA_COERENTE_E_COESAO_REAL_V1.md` |
| antecedente 60/144 | `rafaelmeloreisnovo/RafPolimata:docs/ANEXO_CICLO_60_BASES_144_0_1HZ.md` |
| documento desta descoberta | `docs/canonical/2026-08-02/PYTHAGOREAN_5_12_13_MULTIBASE_CIRCULAR_ARC_V1.md` |
| gerador determinístico | `tools/generate_pythagorean_multibase_arc.py` |
| teste | `tests/geometry/test_pythagorean_multibase_arc.py` |
| bases 1..225 | `data/geometry/pythagorean_5_12_13_multibase_arc.v1.jsonl` |
| delta geométrico | `data/geometry/geometric_invariants.delta.20260802.pythagorean_multibase_arc.jsonl` |
| índice geométrico global | `data/geometry/geometric_invariants.index.jsonl` |
| delta longitudinal | `data/latents/deltas/latents.20260802.pythagorean_multibase_arc.jsonl` |
| índice longitudinal global | `data/latents/latents.index.jsonl` |
| receipt | `receipts/geometry/PYTHAGOREAN_MULTIBASE_ARC_20260802_RECEIPT_V1.json` |

## Ordem de leitura

1. identidade exata `25 + 144 = 169`;
2. família de ternas com catetos/hipotenusa consecutivos;
3. representação em bases coexistentes;
4. círculos `360`, `60` e `Z/bZ`;
5. aliasing do erro `56` nas bases `2,4,7,8,14,28,56`;
6. limites epistemológicos e receipt.

## Gate

```text
exact_integer_PASS + deterministic_generator_PASS + modular_alias_declared
!= physical_claim
```
