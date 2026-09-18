# RAFAELIA — Systematic Pragmatic Mapping Service V1

**Status:** `IMPLEMENTED_UNTESTED_REMOTE`  
**Mode:** `BOUNDED / FAIL-CLOSED / APPEND-ONLY / CLAIM-GATED`  
**Claim boundary:** `claim_allowed=false`

## 1. Objetivo

Transformar inventário técnico em trabalho executável, sem confundir descoberta com
resolução.

O serviço encadeia:

```text
SCAN → BIND → NIBIGUIRI → PRIORIZE → SERVICE → GATE → RECEIPT
```

Ele reutiliza `tools/repository_gap_mapper.py` como scanner de superfície e
`data/gap-atlas/RAFAELIA_GAP_ATLAS_V1.json` como autoridade de lacunas.

## 2. O que ele entrega

Para cada gap observado:

- origem/root/path e hash quando disponível;
- vínculo com `gap_id` existente;
- prioridade operacional;
- serviço aplicável;
- estado Nibiguiri;
- autoridade necessária;
- evidência necessária;
- próximo gate;
- `effort=TOKEN_VAZIO_UNMEASURED` enquanto não houver medição;
- `claim_allowed=false`.

Um achado sem vínculo no Atlas recebe automaticamente:

```text
NIBIGUIRI:CAUSA_DESCONHECIDA
```

A ausência de binding não prova que algo seja "óbvio", esquecido, censurado ou
filtrado. `NIBIGUIRI:OBVIO_NAO_INDEXADO` fica reservado para relação formal
independentemente demonstrada e explicitamente ausente do índice.

## 3. Serviços pragmáticos

| Gap observado | Serviço |
|---|---|
| `BINARY_PROVENANCE_MISSING` | `PROVENANCE_REPAIR` |
| `ASM_NOT_REFERENCED_BY_BUILD` | `BUILD_INTEGRATION_AUDIT` |
| `HASH_INCOMPLETE` | `CUSTODY_HASH` |
| `UNRESOLVED_MARKERS` | `SEMANTIC_TRIAGE` |
| `DOCUMENT_INCOMPLETE` | `DOCUMENT_COMPLETION` |
| outros | `GAP_TRIAGE` |

Esses rótulos são roteamento de trabalho, não prova de causa ou resolução.

### Regra anti-ruído

`TOKEN_VAZIO` é um estado válido. Se um documento contém somente marcador
`TOKEN_VAZIO`, o serviço preserva a observação no gap map, mas não cria uma ação
pragmática artificial. Se o mesmo documento recebe simultaneamente
`UNRESOLVED_MARKERS` e `DOCUMENT_INCOMPLETE` pela mesma causa, o serviço coalesce
os dois em uma única ação.

Isso mantém:

```text
OBSERVAÇÃO != TRABALHO
TOKEN_VAZIO != BUG
UM FATO GERADOR != DUAS AÇÕES DUPLICADAS
```

## 4. Execução

No repositório Mapa:

```bash
python3 tools/systematic_pragmatic_mapping_service.py \
  --root Mapa=. \
  --exclude generated \
  --exclude artifacts \
  --output-dir artifacts/systematic-pragmatic-map \
  --fail-on none
```

Vários repositórios locais podem ser passados repetindo `--root`:

```bash
python3 tools/systematic_pragmatic_mapping_service.py \
  --root Mapa=/path/Mapa \
  --root RafGitTools=/path/RafGitTools \
  --root RafPolimata=/path/RafPolimata \
  --output-dir artifacts/systematic-pragmatic-map
```

## 5. Saídas

```text
artifacts/systematic-pragmatic-map/
├── repository_gap_map.json
├── repository_gap_map.md
├── pragmatic_action_map.json
├── pragmatic_action_map.md
├── cluster_review_queue.json
└── receipt.json
```

O `receipt.json` liga hash canônico do Atlas, gap map e action map.

## 6. Priorização

A prioridade de um item já indexado herda a prioridade mais forte dos registros do
Atlas vinculados. Itens ainda não indexados usam uma heurística explícita de triagem:

- proveniência binária / ASM fora do build / hash incompleto → P1;
- marcadores não resolvidos / documento incompleto → P2;
- tipo desconhecido → P2.

A heurística não substitui decisão de autoridade. `P0` somente é herdado de um
registro governado no Atlas.

## 7. Não-autonomia

O serviço não:

- cria objetivo novo;
- fecha gap automaticamente;
- promove claim;
- estima esforço sem medição;
- transforma correlação em causalidade;
- converte ausência em zero;
- declara censura sem evidência;
- altera o Atlas automaticamente.

## 8. Clusterização determinística

Depois da tipagem, as ações são agrupadas por:

```text
root × domínio de caminho × serviço × marcadores × estado Nibiguiri
```

Cada grupo recebe `cluster_id` derivado por SHA-256, contagem, amostras e
`cluster_digest_sha256` no receipt. O cluster não cria equivalência semântica;
ele é apenas uma unidade de triagem para reduzir trabalho repetitivo.

Regra:

```text
MESMO_CLUSTER != MESMO_SIGNIFICADO
CLUSTER != GAP_RESOLVIDO
```

## 9. Gates

### G3 — Semantic Split Gate

Todo cluster nasce com:

```text
G3=REVIEW_REQUIRED
```

A decisão deve ser uma entre:

```text
DUPLICATE | SAME_FAMILY | DISTINCT_GAP | SPLIT_REQUIRED | FALSE_POSITIVE | ACCEPTED_LIMITATION
```

e exige amostra representativa, comparação de invariantes e razão explícita.
O serviço não escolhe automaticamente.

### G4 — Authority Bind Gate

Todo cluster não resolvido nasce com:

```text
G4=BLOCKED_BY_G3
binding=TOKEN_VAZIO
auto_create_gap_id=false
```

Somente após G3 com evidência pode haver binding a `gap_id` existente ou proposta
governada de novo gap, sempre com autoridade e evidência requeridas.

### Fail modes

`--fail-on`:

- `none`: sempre emite mapa/receipt;
- `p0`: retorna 1 se houver bloqueador P0;
- `unmapped`: retorna 1 se houver Nibiguiri ainda não indexado;
- `any`: retorna 1 se existir qualquer ação.

Isso permite uso tanto exploratório quanto fail-closed em CI.

## 10. Relação com Nibiguiri

```text
SOURCE OBSERVED + NO ATLAS BINDING
→ NIBIGUIRI:CAUSA_DESCONHECIDA
→ DETERMINISTIC CLUSTER
→ TRIAGE
→ EXISTING GAP | NEW TYPED GAP | FALSE POSITIVE | ACCEPTED LIMITATION
→ [OBVIO_NAO_INDEXADO only with formal demonstration]
→ RECEIPT
```

`NIBIGUIRI:CENSURA_EVIDENCIADA` e `NIBIGUIRI:FILTRO_PESO_EVIDENCIADO` não são
inferidos por este serviço.

## 11. R3

```text
F_ok   = scanner + Atlas + Nibiguiri convertidos em fila operacional executável
F_gap  = execução federada e métricas reais de esforço ainda precisam receipt; ruído TOKEN_VAZIO é preservado sem virar fila artificial
F_next = executar teste/CI; depois aplicar o serviço aos repositórios autorizados e triar unmapped
```

## 12. Primeiro G3 executado

O primeiro cluster revisado foi `CL-e005a14253d55a76`, observado no Gap Atlas
run #43. Ele continha 681 ações do domínio `data`, todas com marcador
`TOKEN_VAZIO`, mas distribuídas por 58 subdomínios distintos, incluindo
`routing`, `receipts`, `control-plane`, `catalog_runs`,
`reconciliation`, `evidence`, `governance` e `audits`.

Decisão:

```text
G3 = SPLIT_REQUIRED
G4 = BLOCKED_BY_G3_SPLIT
binding = TOKEN_VAZIO
auto_create_gap_id = false
```

A decisão está registrada em
`data/triage/systematic-pragmatic-g3-decisions.v1.jsonl` e é validada por
`scripts/validate_systematic_pragmatic_g3_decisions.py`.

## 13. Recursive child materialization

A decisão `SPLIT_REQUIRED` deixa de ser uma anotação terminal. O materializador
`tools/materialize_systematic_pragmatic_children.py` lê o mapa pragmático atual
mais o ledger G3 e produz filhos determinísticos por próximo segmento de caminho.

Regra:

```text
PARENT SPLIT_REQUIRED
→ child candidates
→ each child starts REVIEW_REQUIRED
→ child SPLIT_REQUIRED
→ recursive descendants
→ G4 stays blocked until an evidence-backed non-split G3 decision
```

O identificador de filho é derivado de `parent_cluster_id × segment` por SHA-256.
Nenhum filho recebe `gap_id` automaticamente.

### Segundo G3 executado

O filho determinístico `data/routing` é
`CL-ecc6eb2c44bd5b05`. No artifact do Gap Atlas run #43 ele continha 113 ações
distribuídas por 9 próximos segmentos:

- `cycles`: 74;
- `operational-gaps`: 32;
- sete segmentos adicionais com uma ocorrência cada.

Decisão:

```text
G3(data/routing) = SPLIT_REQUIRED
G4 = BLOCKED_BY_G3_SPLIT
binding = TOKEN_VAZIO
auto_create_gap_id = false
```

O próximo materializador deve, portanto, produzir pelo menos os descendentes
`data/routing/cycles` e `data/routing/operational-gaps`, preservando ambos
como `REVIEW_REQUIRED` até uma decisão G3 própria.

## 14. Routing semantic probe

Antes de decidir G3 para `data/routing/cycles` ou
`data/routing/operational-gaps`, o checkout executa
`tools/probe_systematic_pragmatic_routing.py`.

O probe mede, sem decidir:

- nos ciclos: JSON válido, `claim_allowed=false`, contexto estruturado de lacuna/
  incerteza e presença de closure/next gate;
- nos operational-gaps: `gap_id`, unicidade, owner/authority, estado,
  closure/next gate e duplicidades de `gap_id`.

Fronteiras:

```text
TOKEN_VAZIO_PRESENT != DOCUMENT_DEFECT
OPERATIONAL_GAP_RECORD != GAP_ATLAS_BINDING
PROBE != G3_DECISION
```

O resultado entra no artifact/checksum do Gap Atlas e serve como evidência para o
próximo ledger G3.

## 15. G3 routing decisions from bounded probe

O probe do Gap Atlas run #51 sustenta duas decisões distintas.

### `data/routing/cycles`

Observado: 75 ações, 25 famílias de schema, 69 registros com
`claim_allowed=false`, 71 com contexto estruturado de lacuna/incerteza e 74 com
closure/next gate.

```text
G3 = SPLIT_REQUIRED
split_strategy = SEMANTIC_SCHEMA
G4 = BLOCKED_BY_G3_SPLIT
```

O split por schema produz famílias para revisão; schema comum não implica
`SAME_SITUATION`.

### `data/routing/operational-gaps`

Observado: 36 registros selecionados, todos parseáveis, todos com `gap_id`, 35
identidades únicas, um grupo com dois registros para
`BOOTSTRAP_CROSS_STORE_PARITY_20260819T2044BRT`, 36/36 com
`claim_allowed=false` e 36/36 com closure/next gate.

```text
G3 = DISTINCT_GAP
binding_strategy = PER_EXISTING_GAP_ID
G4 = REQUIRES_PER_ITEM_BINDING
Atlas binding = TOKEN_VAZIO
auto_create_gap_id = false
```

`tools/materialize_systematic_pragmatic_routing_bindings.py` transforma essas
decisões em famílias de schema e candidatos de binding por `source_gap_id`, sem
criar IDs do Atlas.

## 16. G4 exact-evidence source-gap reconciliation

Depois de G3 classificar `data/routing/operational-gaps` como
`DISTINCT_GAP/PER_EXISTING_GAP_ID`, o reconciliador
`tools/reconcile_systematic_pragmatic_source_gaps.py` compara as identidades
de origem com o Atlas efetivo.

Somente três classes de evidência são aceitas:

```text
source_gap_id == atlas.gap_id
source_path == explicit Atlas source_ref path
source_gap_id == exact predecessor/successor id
```

Nenhuma similaridade textual, fuzzy match ou aproximação semântica cria
correspondência.

Estados de saída:

```text
CANDIDATE_EXACT_MATCH
NO_EXACT_EVIDENCE
AMBIGUOUS_EXACT_EVIDENCE
```

Mesmo `CANDIDATE_EXACT_MATCH` mantém:

```text
atlas_gap_id = TOKEN_VAZIO
auto_create_gap_id = false
human_or_governed_confirmation_required = true
```

Portanto:

```text
EXACT_EVIDENCE != BINDING
SOURCE_GAP_ID != ATLAS_GAP_ID_BY_ASSUMPTION
NO_MATCH != DOES_NOT_EXIST
```

## 17. Governed G4 append/link proposal queue

Quando a reconciliação exata termina, o serviço
`tools/materialize_systematic_pragmatic_g4_proposals.py` produz somente
propostas de governança.

Estados:

```text
CANDIDATE_EXACT_MATCH + one target
→ PROPOSE_LINK_EXISTING

NO_EXACT_EVIDENCE + bounded source identity complete
→ PROPOSE_APPEND_NEW

AMBIGUOUS or incomplete bounded source evidence
→ NEEDS_MORE_EVIDENCE
```

A completude mínima para `PROPOSE_APPEND_NEW` exige, dentro do conjunto
bounded observado:

- todos os source records com `claim_allowed=false`;
- owner/authority observável;
- closure/next gate em todos os source records.

Mesmo assim:

```text
proposal != binding
proposal != append
proposed_atlas_gap_id = TOKEN_VAZIO
atlas_mutation_allowed = false
auto_create_gap_id = false
```

Campos canônicos ainda não sustentados por evidência, como `gap_class`,
`priority`, `scope` ou novo ID do Atlas, permanecem `TOKEN_VAZIO`.

## 18. Scoped authority resolution + canonical-field completion

A lacuna de autoridade do source gap
`TOKEN_VAZIO_INVALID_CLOSURE_RECEIPT_PROVENANCE_20260819T2207BRT`
é resolvida somente para roteamento governado por um ledger append-only:

`data/triage/systematic-pragmatic-authority-resolutions.v1.jsonl`

Evidência vinculada:

- `indices/repository_authority_registry.json`: `rafaelmeloreisnovo/Mapa`
  é `control_plane`, canônico para `gap_atlas` e `federation_audit`;
- `tools/resolve_token_vazio.py`: Lane 04 coleta/valida, Lane 00 autoriza
  closure/preservation;
- `TOKEN_VAZIO_APPROVAL_WORKFLOWS_V1.md`: Lane 06 integra antes da promoção.

A resolução é escopada:

```text
AUTHORITY_RESOLVED_SCOPED
!= GAP_RESOLVED
!= CLOSURE_VALIDATED
!= ATLAS_BINDING
```

O source record histórico não é reescrito.

### Canonical completion worksheet

`tools/materialize_systematic_pragmatic_canonical_completion.py` transforma
cada `PROPOSE_APPEND_NEW` em um worksheet de campos candidatos:

```text
EXACT_SOURCE_FIELD
SOURCE_ALIAS_CANDIDATE
MULTI_SOURCE_REVIEW
TOKEN_VAZIO
```

Campos avaliados:

`artifact_id, provider, scope, gap_class, priority, known, unknown,
authority_required, evidence_required, next_gate`.

Regras:

```text
alias != equivalence
completion != Atlas record
unsupported field => TOKEN_VAZIO
proposed_atlas_gap_id = TOKEN_VAZIO
atlas_mutation_allowed = false
auto_create_gap_id = false
```

A contagem preserva a linhagem operacional: 34 proposals já elegíveis no gate
anterior + 1 identidade recém-desbloqueada por resolução de autoridade.

## 19. Identity + semantics enrichment for canonical G4 fields

After canonical completion identifies unresolved fields, the service
`tools/enrich_systematic_pragmatic_identity_semantics.py` performs a bounded
structured-source scan for:

`artifact_id, provider, scope, evidence_required`.

Evidence states:

```text
EXACT_STRUCTURED
NORMALIZED_ENUM_CANDIDATE
ALIAS_CANDIDATE
CONFLICT
TOKEN_VAZIO
```

Rules:

- a matching structured key is evidence, not automatic Atlas promotion;
- provider values may only normalize into the six provider values allowed by
  `rafaelia_gap_atlas.v1.schema.json`;
- repository names remain provenance and are not provider values;
- `evidence_needed` and related producer fields are aliases for review, not
  silent equivalence to `evidence_required`;
- receipt/artifact aliases do not become canonical `artifact_id` without
  governed review;
- conflicting structured values fail closed to `CONFLICT/TOKEN_VAZIO`.

Boundary:

```text
structured evidence != promoted canonical field
normalization != binding
alias != equivalence
enrichment != Atlas record
proposed_atlas_gap_id = TOKEN_VAZIO
atlas_mutation_allowed = false
```

## 20. Final structural routing closure

The systematic/pragmatic service reaches a terminal **internal routing** state when
all bounded source identities are represented by governed Atlas source-record
bindings and all schema families are structurally classified.

The terminal state is:

```text
system_state = COMPLETE_STRUCTURAL_ROUTING
source_gap_bindings = 35/35
schema_families_structurally_resolved = 25/25
remaining_internal_review_required = 0
remaining_internal_binding_token_vazio = 0
canonical_completion_candidates = 0
field_review_work_items = 0
```

This state is produced under
`data/governance/SYSTEMATIC_PRAGMATIC_FINALIZATION_V1.json`.

Each bounded operational-gap source identity is assigned a deterministic
source-artifact identity:

```text
artifact_id = OPG_SOURCE::<source_gap_id>
gap_id      = GAP-G4SRC-<SHA256(source_gap_id)[0:16].upper()>
provider    = GitHub
gap_class   = GOVERNANCE
state       = TOKEN_VAZIO
```

The provider refers to the canonical **source record** stored in
`rafaelmeloreisnovo/Mapa`. It does not assert that the subject described by
the record is a GitHub-hosted phenomenon.

The source paths are preserved as exact `source_refs`. Reconciliation therefore
requires a one-to-one exact path match and never fuzzy name similarity.

Cycle records with the same explicit schema string may be accepted as members of
one **structural representation family**. This is not semantic equivalence:

```text
same_schema => same_structural_family
same_schema != same_event
same_schema != same_cause
same_schema != same_claim
```

The terminal receipt is
`data/receipts/pragmatic-map/RECEIPT_SYSTEMATIC_PRAGMATIC_FINAL_CLOSURE_20260918_PASS.json`.

Observed closure run:

```text
Gap Atlas run #78
effective records = 66
CANDIDATE_EXACT_MATCH = 35
PROPOSE_LINK_EXISTING = 35
PROPOSE_APPEND_NEW = 0
source_gap_bindings = 35
schema_families_structurally_resolved = 25
internal routing debt = 0
```

### Stop condition

`COMPLETE_STRUCTURAL_ROUTING` means that the internal system can be rebuilt from
repository sources without conversation memory and without an unresolved routing,
identity, canonical-field, or schema-family review queue.

It does **not** mean that every represented external condition is resolved.

At terminal structural closure, open external/runtime/scientific records continue
to use their own `state`, `evidence_required`, `next_gate`, and receipts.

The final invariant remains:

```text
SOURCE_RECORD_BINDING != EXTERNAL_CONDITION_CLOSURE
STRUCTURAL_FAMILY != SEMANTIC_EQUIVALENCE
ATLAS_APPEND != SCIENTIFIC_OR_RUNTIME_PROOF
TOKEN_VAZIO != 0
claim_allowed = false
publication_ready = false
```
