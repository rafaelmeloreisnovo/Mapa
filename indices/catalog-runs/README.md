# RAFAELIA — Índice de ciclos de catálogo

Este diretório contém checkpoints incrementais e não destrutivos da indexação Drive ↔ GitHub.

## Regras

- Cada ciclo possui timestamp BRT e receipt machine-readable em `data/catalog_runs/`.
- Novos latentes e claims são gravados em arquivos delta append-only sob `data/latents/deltas/` e `data/claims/deltas/`.
- O ledger histórico não é reescrito durante a captura do delta.
- Promoções para índices consolidados exigem validação de schema, deduplicação por ID e revisão do estado epistemológico.
- Ausência de evidência permanece `TOKEN_VAZIO`; execução operacional não promove claim científico.

## Ciclos

| ciclo | relatório | receipt | latentes | claims | estado |
|---|---|---|---|---|---|
| `2026-07-31T23:44-03:00` | [`RAFAELIA_CATALOG_CYCLE_2026-07-31T2344-0300.md`](RAFAELIA_CATALOG_CYCLE_2026-07-31T2344-0300.md) | [`data/catalog_runs/RAFAELIA_CATALOG_CYCLE_2026-07-31T2344-0300.json`](../../data/catalog_runs/RAFAELIA_CATALOG_CYCLE_2026-07-31T2344-0300.json) | [`latents.2026-07-31T2344-0300.jsonl`](../../data/latents/deltas/latents.2026-07-31T2344-0300.jsonl) | [`paper_claims.2026-07-31T2344-0300.jsonl`](../../data/claims/deltas/paper_claims.2026-07-31T2344-0300.jsonl) | `EXECUTED / REVIEW_REQUIRED` |

## Consolidação

```text
baseline canonical
  + deltas ordered by timestamp
  + schema validation
  + unique ID gate
  + source/receipt verification
  = consolidated navigable catalog
```

`claim_allowed=false` permanece o default fail-closed.
