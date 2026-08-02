# Índice — Invariante Geométrica Coerente e Coesão Real — V1

**ID:** `IDX-IGC-CR-20260802-V1`  
**Estado:** `MATERIALIZED_ON_RESEARCH_BRANCH`  
**Claim:** `claim_allowed=false`

## Autoridades

- Contrato canônico: `docs/canonical/2026-08-02/INVARIANTE_GEOMETRICA_COERENTE_E_COESAO_REAL_V1.md`
- Memória da pirâmide triédrica dupla: `docs/canonical/2026-08-02/MEMORIA_LONGITUDINAL_PG_OMEGA7_PIRAMIDE_TRIEDRICA_DUPLA_V1.md`
- Método Drive ↔ GitHub: `indices/RAFAELIA_IMPLEMENTACAO_LATENTES_PAPERS_V1.md`
- Overlay longitudinal: `docs/canonical/2026-08-02/MEMORIA_LONGITUDINAL_CONTEXTUAL_RECORRENTE_E_INDICE_DE_TRABALHO_V1.md`

## Artefatos

- Schema: `schemas/geometric-invariant-contract.schema.json`
- Validador: `tools/validate_geometric_invariant_contract.py`
- Fixtures: `tests/geometry/fixtures/`
- Ledger: `data/geometry/geometric_invariants.index.jsonl`
- CI: `.github/workflows/geometric-invariant-contract.yml`

## Invariante operacional

```text
objeto + representação + transformação + propriedade + tolerância
→ teste/prova + falsificador + custódia
→ PASS | FAIL | TOKEN_VAZIO
```

A igualdade visual não promove identidade geométrica. Toda alegação de invariância deve declarar a família de transformação.

## Estado no corte

```yaml
contract: MATERIALIZED
schema: MATERIALIZED
validator: MATERIALIZED
positive_fixtures: 2
negative_fixtures: 1
ledger_records: 2
local_sandbox_test: PASS_LIMITED
remote_ci: TOKEN_VAZIO_PENDING_PR_RUN
physical_termux: TOKEN_VAZIO
independent_reproduction: TOKEN_VAZIO
claim_allowed: false
```
