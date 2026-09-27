# RAFAELIA — Federação dos Tipos de Cadeia de Custódia — V1

**Estado:** SPEC + IMPLEMENTATION PR / `claim_allowed=false`  
**Escopo:** diferenciar custódia por superfície, objeto, ator, execução e promoção sem quebrar os ledgers históricos.

## 1. Problema resolvido

"Cadeia de custódia" estava sendo usada para objetos diferentes. O ecossistema já possuía, entre outros:

- evento append-only genérico: `mapa.custody-event.v1`;
- prova/promoção: `proof-custody-receipt`;
- registro de conectores: `CONNECTOR_CUSTODY_CHAIN.jsonl`;
- identidade Drive ↔ GitHub: `DRIVE_GITHUB_IDENTITY_MODEL.md`;
- envelopes de evidência em repositórios produtores, que permanecem autoridade do próprio produtor.

Esses artefatos não são substituídos. Esta camada os **federará por perfil tipado**.

## 2. Invariante de separação

```text
AUTHORSHIP
!= AUTHORIZATION
!= ORCHESTRATION
!= PROVIDER_EXECUTION
!= RUNTIME_EXECUTION
!= REVIEW
!= CLAIM_PROMOTION
```

E permanece:

```text
SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM
TOKEN_VAZIO != 0
IMPLEMENTED_UNTESTED != PASS
```

## 3. Matriz de autoridade

| Superfície | Autoridade | Âncora forte | Não prova sozinha |
|---|---|---|---|
| GitHub código | repo produtor | commit/ref + blob SHA/digest | execução, correção científica |
| GitHub PR/review | provider + política humana | PR + head SHA + checks + review/merge | aprovação ausente |
| GitHub Actions | runtime do run | run/job + exact head + logs/artefatos | outros ambientes |
| Drive documento | Drive documental | fileId + revision/modified state | bytes imutáveis |
| Drive materializado | source + materialização | fileId/revision + hash dos bytes exportados | identidade com outra representação sem ponte |
| Drive move/rename | metadata + receipt | fileId + before/after parents/name | conteúdo inalterado |
| Cross-surface | relação federada | artifact_id + refs de ambas superfícies | byte-equivalência sem digests |
| Receipt | ledger declarado | receipt_id + parent + hash/revision | promoção do claim por si só |

## 4. Cadeia de ator — humano e assistente

Para ações mediadas por assistente/conector:

```text
HUMAN_AUTHORITY
  -> ASSISTANT_ORCHESTRATOR
  -> CONNECTOR_PROVIDER
  -> PROVIDER_RESULT
  -> optional RUNTIME_EXECUTOR
  -> optional INDEPENDENT_REVIEWER
  -> human/provider promotion decision
```

### Regra crítica

O assistente pode analisar, rotear e solicitar uma ação dentro do escopo autorizado. Ele **não**:

- cria a própria autoridade humana;
- transforma texto em execução observada;
- satisfaz revisão independente;
- promove sozinho um claim;
- inventa principal/provider quando o provider não o expõe.

Campo desconhecido = `TOKEN_VAZIO`, com closure path.

## 5. Perfis canônicos

O registry machine-readable define:

1. `GITHUB_SOURCE_CODE_CUSTODY`
2. `GITHUB_REVIEW_PROMOTION_CUSTODY`
3. `GITHUB_ACTIONS_EXECUTION_CUSTODY`
4. `DRIVE_DOCUMENT_REVISION_CUSTODY`
5. `DRIVE_CONTENT_MATERIALIZATION_CUSTODY`
6. `DRIVE_MOVE_RENAME_CUSTODY`
7. `TRANSFORMATION_LINEAGE_CUSTODY`
8. `EVIDENCE_CUSTODY`
9. `AGENT_ACTION_CUSTODY`
10. `CROSS_SURFACE_BINDING_CUSTODY`
11. `RECEIPT_CHAIN_CUSTODY`

## 6. Compatibilidade

Esta V1 **não altera** `schemas/cadeia_custodia_evento.schema.json` nem `scripts/validate_chain_of_custody.py`.  
O ledger histórico continua válido. Novos receipts podem adicionar `profile_id` em artefato complementar ou índice federado sem reescrever eventos antigos.

## 7. Drive ↔ GitHub

### Drive

Guarda:

- índice/documentação operacional;
- CURRENT_STATE;
- μWRITE/receipts;
- fileId/revision e custódia documental.

### GitHub

Guarda:

- schema do registry;
- registry machine-readable;
- validator;
- testes;
- workflow de CI.

### Ponte

```text
artifact_id | repository | commit/ref | Drive fileId | revision | timestamp | relation | digest_when_needed
```

Se houver alegação de **byte-equivalência**, ambos os lados devem ser materializados de forma comparável e ter digest compatível. Ponteiro sem digest comprova relação, não igualdade de bytes.

## 8. Fontes observadas antes deste delta

- `docs/DRIVE_GITHUB_IDENTITY_MODEL.md` — blob `f4a84013a3256eb61e5ea27b15c9c4fa6b24e533`
- `docs/governance/PROOF_CUSTODY_AND_TOKEN_VALIDITY_V1.md` — blob `2b67f23506a9d45f09f7fe983bde035a4439189e`
- `scripts/validate_chain_of_custody.py` — blob `6a7cd28e63840eab2f728311baa028cc657c9887`
- `tools/verify_proof_custody.py` — blob `177e9d1277fd0553f461c95da61c3286e2c56406`
- Drive `START HERE — RAFAELIA Ω CANONICAL V2.1 DISPATCH`
- Drive `CURRENT_STATE Ω — START HERE DISPATCH V1`
- Drive `41_CUSTODY_CHAIN` — observado vazio antes desta rodada.

## 9. Gate

```text
schema/registry present -> IMPLEMENTED
validator + unit tests defined -> IMPLEMENTED_UNTESTED
exact-head CI PASS -> PASS for this registry implementation
provider/human promotion -> separate decision
claim_allowed remains false for broader ecosystem claims
```

## R3

**F_ok:** taxonomia separa superfície, ator, transformação, execução, evidência, receipt e promoção.  
**F_gap:** até CI do exact-head, implementação permanece `IMPLEMENTED_UNTESTED`; merge continua decisão humana/provider.  
**F_next:** observar CI do PR, registrar ponte no Drive `41_CUSTODY_CHAIN` e μWRITE do delta.
