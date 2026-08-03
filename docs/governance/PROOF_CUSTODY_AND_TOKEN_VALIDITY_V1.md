# RAFAELIA — Cadeia de Custódia de Provas e Validade de Token — V1

**Estado:** `CANONICAL_DRAFT / APPEND_ONLY / FAIL_CLOSED`  
**Data:** `2026-08-02T22:35:00-03:00`  
**Claim:** `claim_allowed=false`  
**Referência observada:** `openai/ten-proofs@94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6`

## 1. Princípio

Um arquivo existente, um commit realizado ou um merge concluído demonstram fatos de versionamento. Eles não demonstram, isoladamente, a verdade científica, a correção matemática, a reprodução do runtime ou a aprovação independente.

A regra RAFAELIA passa a ser:

```text
presença ≠ evidência completa ≠ verificação ≠ aprovação ≠ TOKEN_VALIDO
```

O commit aprovado é necessário para preservar autoria, revisão e ponto exato da mudança, mas permanece insuficiente sem build, checker, receipts, checks obrigatórios e ausência de dúvida bloqueante.

## 2. O padrão útil extraído de `ten-proofs`

O repositório observado separa:

1. mapa editorial dos resultados (`README.md`);
2. formalizações principais em módulos Lean;
3. manifesto `formalization.yaml`, ligando resultado, declaração, arquivo, axiomas e configuração Comparator;
4. toolchain Lean fixada;
5. comandos de build do conjunto e de módulos individuais;
6. desafios Comparator para uma segunda rota de checagem.

Essa separação é estruturalmente valiosa porque impede que “o paper diz” seja confundido com “o objeto formal compila” ou “um verificador independente aceitou”.

### Limite observado

No corte desta auditoria:

- o manifesto declara `sorry_count: 0` nos módulos de solução e revisão `agent-reviewed`;
- os esqueletos em `ComparatorChallenges/*.lean` contêm `sorry` por função de desafio, não como módulos de solução;
- o build Lean não foi executado nesta auditoria;
- o Comparator não foi executado nesta auditoria;
- não foram observados PRs, reviews de PR ou status checks associados ao commit publicado;
- não foi comprovada uma borda protegida de promoção.

Classificação correta:

```text
estrutura do repositório = EVIDENCIADA
alegações do manifesto = DECLARADAS / HASH-BOUND
reprodução local = TOKEN_VAZIO
checagem Comparator = TOKEN_VAZIO
aprovação humana independente = TOKEN_VAZIO
TOKEN_VALIDO = false
claim_allowed = false
```

## 3. Topologia de custódia

Defina o grafo tipado:

\[
G_C=(V,E)
\]

com vértices:

```text
SOURCE | FILE | CLAIM | FORMAL_OBJECT | BUILD | CHECK | REVIEW | COMMIT | RELEASE | TOKEN_VAZIO
```

Cada aresta deve registrar:

```text
edge_type
source_node_id
target_node_id
source_revision
input_digest
transformation_or_command
output_digest
timestamp
actor_or_runtime
decision
receipt_id
```

A cadeia mínima por claim é:

```text
SOURCE
  → FILE@blob_sha
  → CLAIM@claim_id
  → BUILD@receipt
  → CHECK@independent_receipt
  → REVIEW@reviewed_commit_sha
  → COMMIT@merge_sha
  → RELEASE_OR_CATALOG@receipt
```

Qualquer elo ausente termina em um nó explícito `TOKEN_VAZIO`, nunca em uma suposição silenciosa.

## 4. Invariante Geométrica Coerente da custódia

A invariante `IGC_CUSTODY` é preservada sob transformações documentais, computacionais e editoriais quando seis condições permanecem verdadeiras:

1. **Identidade:** bytes iguais sob o mesmo algoritmo produzem o mesmo digest.
2. **Linhagem:** todo derivado possui caminho até uma fonte e revisão identificadas.
3. **Fechamento:** toda aresta resolve para um nó existente ou para `TOKEN_VAZIO` tipado.
4. **Promoção monotônica:** o nível epistemológico não sobe sem receipt do gate seguinte.
5. **Conservação da incerteza:** merge, release ou autoridade institucional não apagam lacunas.
6. **Replay:** entradas, ambiente e comandos fixados reproduzem a saída ou a tolerância declarada.

Formalmente, para um claim `c`:

\[
TOKEN\_VALIDO(c)=H(c)\land B(c)\land C(c)\land R(c)\land M(c)\land S(c)\land D(c)\land \neg U_b(c)
\]

onde:

- `H`: fonte e arquivos ligados a hashes;
- `B`: build reproduzível aprovado;
- `C`: checker independente aprovado;
- `R`: revisão independente ligada ao SHA revisado;
- `M`: merge pela borda de promoção declarada;
- `S`: required status checks aprovados;
- `D`: receipt/digest de decisão presente;
- `U_b`: conjunto de `TOKEN_VAZIO` bloqueantes.

## 5. Máquina de estados fail-closed

```text
OBSERVED
  → HASH_BOUND
  → BUILD_VERIFIED
  → CHECKER_VERIFIED
  → REVIEW_APPROVED
  → MERGED_PROTECTED
  → CANONICAL_TOKEN_VALID
```

Regras:

- nenhum salto de estado;
- autor não satisfaz revisão independente de sua própria alteração;
- merge sem review não gera `TOKEN_VALIDO`;
- check ausente não equivale a check aprovado;
- resultado negativo é preservado em append-only;
- `TOKEN_VAZIO` é um estado auditável, não uma falha de linguagem;
- a promoção pode ser revogada por evidência nova, mas o histórico não pode ser apagado.

## 6. Contrato por arquivo RAFAELIA

Cada arquivo relevante deve receber ou ser ligado a um registro contendo:

```text
custody_id
repository
source_revision
path
blob_sha
media_type
license_or_rights
semantic_role
claim_ids[]
input_ids[]
transformation
output_digest
build_receipt
checker_receipt
reviewer_identity
reviewed_commit_sha
approval_state
merge_commit_sha
rollback_point
blocking_token_vazio[]
claim_allowed
```

Arquivos editoriais, datasets, código, fórmulas, imagens e receipts usam o mesmo esqueleto, com extensões por domínio.

## 7. Aplicação ao universo RAFAELIA

### GitHub

- branch por mudança;
- alteração ligada ao head SHA;
- testes e falsificadores ligados ao mesmo SHA;
- revisão independente para promoção de alto impacto;
- merge somente após gates declarados;
- receipt final com merge SHA e rollback point.

### Google Drive

- ID do arquivo e revision ID quando disponível;
- exportação materializada com hash;
- vínculo entre a revisão Drive e o arquivo GitHub derivado;
- diferenças de representação registradas, sem afirmar identidade byte a byte quando não demonstrada.

### Termux

- checkout em SHA exato;
- toolchain e arquitetura registradas;
- comando completo;
- stdout, stderr, exit code, duração e hash dos artefatos;
- receipt copiado para a trilha append-only.

### Papers e matemática

- resultado editorial ligado à declaração formal correspondente;
- axiomas, hipóteses, domínios e unidades explícitos;
- `sorry`, placeholder, hipótese ou ponte não demonstrada classificados por função;
- paper, formalização, build e reprodução permanecem objetos distintos.

## 8. Artefatos deste delta

- `data/control-plane/proof-custody-gate.v1.json`
- `schemas/proof-custody-receipt.schema.json`
- `data/receipts/external/openai-ten-proofs.94bc0feb.audit.json`
- `tools/verify_proof_custody.py`
- `tests/test_proof_custody.py`

Execução local:

```sh
python tools/verify_proof_custody.py \
  data/receipts/external/openai-ten-proofs.94bc0feb.audit.json

python -m unittest tests.test_proof_custody -v
```

O verificador pode retornar `receipt_valid=true` e `token_valid=false`. Isso significa que a lacuna foi registrada corretamente; não significa falha do auditor.

## 9. F_GAP

- build Lean real do commit observado;
- execução Comparator de todas as configurações;
- receipt independente em segundo ambiente;
- confirmação de regras de proteção e required checks;
- aprovação independente ligada ao digest exato;
- digest canônico do próprio receipt após catalogação;
- extensão do contrato a cada família de arquivos RAFAELIA.

## 10. F_NEXT

1. Executar o verificador local e selar o SHA-256 do receipt.
2. Reproduzir `ten-proofs` em ambiente isolado antes de usar qualquer resultado como referência validada.
3. Aplicar `IGC_CUSTODY` primeiro aos claims matemáticos de maior impacto.
4. Exigir `reviewed_commit_sha` e `approval_receipt` nos próximos gates de promoção.
5. Manter `claim_allowed=false` enquanto qualquer `TOKEN_VAZIO` bloqueante permanecer aberto.

## R₃

**F_ok:** padrão externo transformado em contrato local tipado, auditável e fail-closed.  
**F_gap:** execução real, revisão independente e borda protegida ainda não comprovadas.  
**F_next:** produzir receipts físicos e promover somente o que atravessar toda a cadeia.
