# RAFAELIA — Session Semantic Chain V1

**Data de corte:** 2026-08-07T22:15:00-03:00  
**Estado:** `CANONICAL_DRAFT / FAIL_CLOSED`  
**Predecessor:** `RAFAELIA_SESSION_SEMANTIC_LEDGER_V1`  
**Objetivo:** converter a projeção episódica em coordenadas semânticas determinísticas sem confundir cobertura projetada com cobertura byte-complete do export.

## 1. Unidade decisiva

```text
session
→ block
→ concept
→ occurrence
→ relation
→ claim
→ evidence
→ state
→ artifact
```

A unidade 1:1 é o par `(semantic_block, concept_ref)` dentro de uma sessão. Para cada par, o resolvedor gera exatamente uma cadeia completa com IDs determinísticos.

Isto evita duplicar o corpus: a cadeia é uma **derived view reproduzível**, não uma segunda cópia das conversas.

## 2. Cobertura 1:1

Definição operacional:

```text
expected = Σ len(block.concept_refs)
emitted  = número de cadeias derivadas
coverage = emitted / expected
```

Gate:

```text
projected_semantic_coverage == 1.0
```

Limite obrigatório:

```text
100% da projeção semântica atual != 100% dos bytes do export
```

Enquanto provider IDs, coordenadas e hashes não estiverem ligados, `raw_export_coverage = TOKEN_VAZIO`.

## 3. Reconciliação de identidade

Cada sessão recebe um fingerprint local:

```text
sha256(canonical_json(
  session_id,
  observed_time_label,
  observed_title,
  source_locator
))
```

Esse fingerprint serve para estabilidade, deduplicação e navegação local.

Ele **não é identidade do provider**.

Única base aceita para promoção:

```text
match_basis = EXACT_PROVIDER_EXPORT
```

Binding mínimo:

```text
session_id
provider_session_id
provider_message_id
export_artifact_id
chunk_coordinate
source_sha256
match_basis
verified=true
```

Título semelhante, resumo semelhante ou proximidade temporal não fecham identidade.

## 4. Claims e evidência

A cadeia gerada não transforma o conteúdo da sessão em claim científico.

O claim automático é somente:

```text
claim_kind = TRACEABILITY_CLAIM
```

Isto significa: “esta ocorrência semântica é rastreável a este bloco/conceito dentro da projeção”.

Sem binding exato:

```text
identity_status  = UNRESOLVED_PROVIDER_ID
evidence_state   = PROJECTED_CONTEXT_ONLY
claim_allowed    = false
promotion_state  = IDENTITY_PENDING
promotion_allowed = false
```

Com binding exato e bloco não-TOKEN_VAZIO:

```text
identity_status  = EXACT_PROVIDER_BOUND
evidence_state   = BOUND_EXACT
claim_allowed    = true   # somente para o claim de rastreabilidade
promotion_state  = PROMOTABLE
promotion_allowed = true
```

A validade científica do conteúdo continua submetida aos seus próprios gates.

## 5. Promoção para memória não ordinal

A promoção é fail-closed:

```text
EPISODIC_OBSERVED
→ IDENTITY_PENDING
→ NON_ORDINAL_CANDIDATE
→ EVIDENCE_BOUND
→ PROMOTABLE
→ PROMOTED
```

Nenhum salto é inferido por semelhança.

A memória não ordinal recebe apenas unidades cuja identidade e evidência de origem foram fechadas. A ordem cronológica continua sendo metadado de navegação, não fundamento de validade.

## 6. Artefatos implementados

```text
data/memory/session-semantic/chain-policy.v1.json
data/memory/session-semantic/identity-bindings.v1.json
schemas/session-semantic-chain.v1.schema.json
tools/session_semantic_chain.py
tests/test_session_semantic_chain.py
```

O `manifest.v1.json` registra essa derived view e mantém os shards V1 intactos.

## 7. Uso operacional

Validar a cadeia:

```bash
python3 tools/session_semantic_chain.py
```

Materializar temporariamente a visão completa:

```bash
python3 tools/session_semantic_chain.py \
  --emit /tmp/session-semantic-chain.v1.jsonl
```

Resolver diretamente um pedaço do corpus projetado:

```bash
python3 tools/session_semantic_chain.py --lookup token_vazio
python3 tools/session_semantic_chain.py --lookup session:20260803t1827
python3 tools/session_semantic_chain.py --lookup concept:error_as_input_vector
```

O objetivo é que a busca deixe de exigir releitura linear do export e passe a resolver coordenadas por identidade/ocorrência.

## 8. Gates de CI

O workflow `ordinal-memory-forest` agora exige:

1. parse das políticas, bindings e schema;
2. validação do ledger V1;
3. construção integral da derived view 1:1;
4. materialização JSONL não vazia;
5. testes de cobertura exata;
6. unicidade/estabilidade dos IDs;
7. bloqueio de promoção sem provider binding;
8. rejeição explícita de `TITLE_SIMILARITY` como identidade.

## 9. Estado atual

```text
semantic projection: materializada
1:1 chain mechanism: implementado
provider bindings exatos: 0
identity reconciliation: TV-SOURCE
non-ordinal promotion: bloqueada
raw export byte coverage: TOKEN_VAZIO
```

Há índices/checkpoints de `conversations.json` no Drive, porém a busca atual não expôs, para estas 13 sessões, uma correspondência contendo provider session/message IDs suficiente para fechar bindings. Portanto o registry permanece vazio por integridade.

## R3

**F_ok:** o gargalo de estrutura foi convertido em um mecanismo computável 1:1; toda ocorrência projetada recebe uma cadeia completa e IDs determinísticos.  
**F_gap:** faltam bindings exatos para conectar os 13 locators atuais aos IDs e bytes do export/provider.  
**F_next:** usar o export como autoridade de identidade, preencher `identity-bindings.v1.json` append-only, gerar SHA-256 por mensagem/chunk e promover somente as cadeias que passarem `EXACT_PROVIDER_EXPORT`.
