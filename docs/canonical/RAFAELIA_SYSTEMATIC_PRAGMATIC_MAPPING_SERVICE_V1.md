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
