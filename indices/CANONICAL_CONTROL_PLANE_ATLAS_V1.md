# RAFAELIA — Canonical Control Plane × Atlas V1

**Data:** 2026-08-29  
**Estado:** `VERIFIED_LIMITED_APPEND_ONLY`  
**Claim global:** `claim_allowed=false`

## Função

Este índice aponta para a camada canônica de controle. Ele **não duplica** as fontes de verdade: o `MASTER_INDEX` continua sendo inventário factual, o `Mapa` continua sendo ontologia/roteador, o Drive preserva custódia/memória longitudinal e cada repositório produtor mantém autoridade sobre seu artefato.

## Artefatos canônicos

- Control plane sucessor: `data/control-plane/CANONICAL_CONTROL_PLANE_ATLAS_V1_20260829.json`
- Receipt de bootstrap: `data/receipts/CANONICAL_CONTROL_PLANE_BOOTSTRAP_20260829.v1.json`
- Predecessor federado preservado: `data/control-plane/federated-reference-matrix.v1.json`
- Predecessor ATLAS/NOVO preservado: `data/reconciliation/ATLAS_NOVO_INGEST_CONTINUATION_WAVE2_20260828.v1.json`
- Google Drive MASTER_INDEX: `1-13h93Q_iOyuuGvrMNt5AG4-vYWPLux2UIWbk8khaLk`

## MASTER_INDEX — planos transversais adicionados

`PROVENANCE` · `CUSTODY_CHAIN` · `RECEIPTS` · `CONTRACTS` · `URGENCIES_GATES` · `CLAIMS` · `RISKS` · `ATLAS_ROUTES` · `VALIDATIONS` · `SUPERSESSION` · `CLOSURE_LEDGER`

Os planos anteriores foram preservados; a mudança é aditiva.

## Contratos mínimos

- `C-EVIDENCE-001`: `VISION != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`
- `C-TOKEN-001`: `TOKEN_VAZIO != 0`; ausência não vira valor inferido.
- `C-SEARCH-001`: `SEARCH_MISS != GLOBAL_ABSENCE`.
- `C-RUNTIME-001`: `CODE_PRESENT != RUNTIME_VERIFIED`; `FIXTURE != LIVE`.
- `C-REGRESSION-001`: uma versão nova não pode remover identidade, proveniência, classificação de evidência, gaps conhecidos, incerteza ou rollback sem `SUPERSESSION_RECEIPT`.

## Rotas ATLAS

```text
ATLAS:X  localização + autoridade + rota
NOVO:X   fonte mais recente válida / NOVOexport quando aplicável
L:X      predecessor/sucessor longitudinal
O:X      eixo ortogonal independente
T:X      ponte transversal entre domínios
REL:X    relações estruturais tipadas
SCALE:X  META → macro → micro → token → yocto quando aplicável
EVID:X   evidência / receipt / gate
GAP:X    TOKEN_VAZIO / incerteza / blocker
LEARN:X  aprendizado append-only
```

## Pipeline de ingestão

```text
ENUMERATE
→ IDENTIFY
→ HASH/REVISION
→ PROVENANCE
→ RELATIONS
→ CONTRACTS
→ EVIDENCE
→ GAPS/TOKEN_VAZIO
→ URGENCY
→ VALIDATION
→ RECEIPT
→ ATLAS EDGES
→ LEARN APPEND
→ CLOSURE
```

## Fechamento

`CLOSED_VERIFIED` só é admissível quando identidade, proveniência, relações, contratos, evidência, gaps e receipts satisfazem os gates; P0/P1 precisam estar resolvidos ou formalmente bloqueados; toda fila deve alcançar sua `STOP_CONDITION`.

Um `TOKEN_VAZIO` pode terminar em `RESOLVED_EVIDENCED`, `ACCEPTED_BOUNDARY`, `FALSIFIED`, `SUPERSEDED` ou `DEFERRED_WITH_TRIGGER`. Nunca deve ser fechado por suposição.

## Gaps prioritários preservados

- `TV-RAW-018-CURRENT-LOCATOR-PROVENANCE`
- `TV-MESSAGES-PROJECTION-GENERATOR`
- `TV-TOKEN-OCCURRENCE-GENERATOR-PROVENANCE`
- `TV-PREPOST-SPREADSHEET-DIGEST`

## Exemplo transversal já indexado

`NEON4096` foi ligado a Papers, ChipQuantum e Matemática, com o baseline T7 ARM32 batch4 separado de hipóteses batch8/ARM64/Q15 e com `pointer_traversal` mantido aberto.

## Estado atual

```text
MASTER_INDEX = factual inventory + transversal registries
ATLAS        = routing graph
LEDGER       = append-only evolution
PROVENANCE   = origin/custody chain
RECEIPTS     = transition evidence
CONTRACTS    = invariants
EVIDENCE     = claim support
GAPS         = explicit ignorance
URGENCIES    = rational work ordering
LEARN        = non-destructive learning
CLOSURE      = proof of finalization
```

`R3 = <F_ok: control-plane materialized; F_gap: validators + universe coverage + P0/P1 evidence; F_next: enforce contracts mechanically and continue queue closure>`
