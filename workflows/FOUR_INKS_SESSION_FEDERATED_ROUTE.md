# FOUR_INKS_SESSION_FEDERATED_ROUTE

```yaml
schema: four_inks_session_federated_route.v1
state: ACTIVE_PRIVATE
claim_allowed: false
producer: rafaelmeloreisnovo/papers
control_plane: rafaelmeloreisnovo/Mapa
source_ref: e481bc0b6d86ef7781acb8d61bf9b6ae759e88b1
source_path: data/memory/session_vectors_four_inks.v1.jsonl
source_blob_sha: fa6b91847870482c2e01122a0729b515f7d60e42
source_digest: TOKEN_VAZIO
```

## Fluxo

```text
READ SESSION SOURCE
→ PRESERVE AUTHORIAL TEXT
→ LOAD VECTOR LEDGER
→ VALIDATE FOUR INKS
→ VALIDATE TYPE BEFORE OPERATION
→ VALIDATE FALSIFIERS AND FORBIDDEN PROMOTIONS
→ VALIDATE RELATION TARGETS
→ GROUP BY INK
→ REGISTER FIVE MAP POINTERS
→ CHECK PRODUCER REF/BLOB DRIFT
→ APPLY DMAIC STRUCTURAL METRICS
→ EMIT RECEIPT OR TOKEN_VAZIO
```

## Gates

| Gate | Aceitação | Falha |
|---|---|---|
| `G1_SOURCE` | source packet e owner presentes | `TOKEN_VAZIO` |
| `G2_INK` | tinta e estado compatíveis | `CLAIM_BLOCKED` |
| `G3_TYPE` | `type_before_operation=true` | `CLAIM_BLOCKED` |
| `G4_EVIDENCE` | demonstração com refs fixadas | `TOKEN_VAZIO` |
| `G5_FALSIFIER` | hipótese e todos os vetores com falsificador | `CLAIM_BLOCKED` |
| `G6_PARABLE` | parábola sem evidência técnica e com proibições | `CLAIM_BLOCKED` |
| `G7_VOID` | vazio com objeto, gate, fonte, artefato e risco | `TOKEN_VAZIO` |
| `G8_RELATIONS` | alvos existentes e sem self-loop | `CONTRADICTION` |
| `G9_POINTER` | producer ref/path/blob iguais nos cinco seletores | `STALE_CONSUMER` |
| `G10_RECEIPT` | steps/logs/artifact observáveis | `BLOCKED_BEFORE_STEPS` |

## Cinco seletores

```text
MAP-SV-PARABLE
MAP-SV-CONVENTION
MAP-SV-DEMONSTRATION
MAP-SV-HYPOTHESIS
MAP-SV-TOKEN-VAZIO
```

O seletor não copia conteúdo. Ele fixa:

- produtor;
- ref;
- caminho;
- blob;
- regime;
- quantidade esperada;
- escopo;
- proibições;
- próxima ação;
- política de drift.

## Política de promoção

```text
PARABLE       nunca promove diretamente a fato
CONVENTION    promove somente como contrato adotado
HYPOTHESIS    promove após experimento e falsificadores
DEMONSTRATION vale somente no alcance da evidência
TOKEN_VAZIO   promove somente após artefato e evento de resolução
```

## Política de drift

```text
papers.current_ref != pointer.source_ref
→ STALE_CONSUMER

papers.current_blob != pointer.source_blob_sha
→ STALE_CONSUMER

producer ink count != pointer expected_count
→ CONTRADICTION

consumer broadens producer scope
→ CLAIM_BLOCKED
```

## Receipt mínimo

```yaml
route_id: FOUR_INKS_SESSION_FEDERATED_ROUTE
producer_ref: required
producer_blob_sha: required
validator_exit_code: required
steps_executed: required
report_sha256: required_when_report_exists
source_sha256: TOKEN_VAZIO_ALLOWED_UNTIL_CHECKOUT
job_id: required_when_ci
run_id: required_when_ci
claim_allowed: false
```

## Rollback

Nenhuma atualização apaga pointer anterior. Corrigir por novo commit/evento e manter o
estado anterior como `SUPERSEDED` ou `CONTRADICTION` com razão explícita.
