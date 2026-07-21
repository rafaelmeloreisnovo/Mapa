# P0 G006 — baseline máxima do gate de linguagem e contradição

Data: 2026-07-20  
Autoridade: `rafaelmeloreisnovo/Mapa`  
Branch: `governance/p0-g006-claim-vocabulary-v1-20260720`

## Objetivo

Impedir que `COMPLETE`, `COMPLIANT`, `ALIGNED` ou `CERTIFIED` sejam usados
como promoção de estado quando implementação, execução, evidência, escopo ou
autoridade ainda estiverem ausentes.

## Control plane materializado

```text
indices/CLAIM_VOCABULARY_POLICY.json
indices/CLAIM_CONTRADICTION_LEDGER.json
indices/CLAIM_CONTRADICTION_HEAD.json
indices/CLAIM_REVIEW_RESIDUAL.json
indices/claim_review_batches/CLAIM_REVIEW_BATCH_001_2026-07-20.json
indices/claim_review_batches/CLAIM_REVIEW_BATCH_002_2026-07-20.json
schemas/claim-contradiction-ledger.schema.json
scripts/validate_claim_vocabulary.py
scripts/validate_claim_contradiction_ledger.py
scripts/validate_claim_review_chain.py
scripts/validate_claim_review_residual.py
tests/test_claim_vocabulary.py
tests/test_claim_contradiction_ledger.py
tests/test_claim_review_chain.py
tests/test_claim_review_residual.py
.github/workflows/topology-validation.yml
```

## Snapshot delimitado

A busca indexada por `COMPLETE` no commit
`4016c51e024573a3875457fceb6d05926e07a07b` produziu 36 arquivos candidatos.
O ledger declara expressamente que a busca de código pode ser incompleta ou
desatualizada e não equivale a uma varredura byte a byte do repositório.

```text
candidate_count          = 36
base reviewed safe       = 6
batch 001 decisions      = 14
batch 002 decisions      = 15
reviewed safe final      = 35
reviewed blocking final  = 0
TOKEN_VAZIO final        = 1
review completion        = 35/36 = 0.972222222222
claim_allowed            = false
certification_claim      = false
```

## Arquitetura append-only

```text
ledger-base imutável
  ↓
review batch 001 — 14 transições pinadas
  ↓
review batch 002 — 15 transições pinadas
  ↓
HEAD atômico — deriva 35 safe / 0 blocking / 1 TOKEN_VAZIO
  ↓
residual exato — CC028
```

Cada decisão exige caminho, commit, disposição semântica, justificativa,
revisor e `claim_allowed=false`. Um arquivo não lido integralmente não pode ser
marcado como seguro.

## Residual CC028

```text
id        = CC028
path      = indices/REPOSITORY_INVENTORY.json
blob      = b43554096f00c0918997dd9f9b11787cec4d4e52
state     = TOKEN_VAZIO
reason    = CONNECTOR_RESPONSE_TRUNCATED_AT_LINE_BOUNDARY
attempt 1 = GitHub.fetch_file → TRUNCATED_RESPONSE
attempt 2 = GitHub.fetch_blob → TRUNCATED_RESPONSE
```

O início observado mostra `PARTIAL` e `claim_allowed=false`, mas isso não é
suficiente para classificar todas as ocorrências no arquivo completo de uma
linha. A classificação semântica permanece proibida até materialização
byte-idêntica e leitura integral.

## Cobertura adversarial preparada

Os testes versionados cobrem, entre outros:

- promoção de claim e certificação;
- ponteiro `TOKEN_VAZIO` usado como evidência;
- adulteração de digests;
- contagens derivadas falsas;
- repetição de lote ou transição;
- caminho ou commit divergente;
- justificativa insuficiente;
- residual omitido ou trocado;
- falsa alegação de conteúdo integral;
- tentativa de dispensar automaticamente candidato não lido.

## Workflow único

O workflow estrutural existente foi ampliado; nenhum YAML concorrente foi
criado. Quando houver execução observável, ele deverá compilar, testar,
escanear, validar ledger/cadeia/residual, verificar invariantes, produzir
checksums e publicar onze relatórios estruturais.

## Estado de execução

```text
artefatos versionados                  = true
integridades canônicas construídas     = true
workflow integrado                     = IMPLEMENTED_NOT_EXECUTED
execução da suíte no clone integral    = TOKEN_VAZIO
scanner integral observável            = TOKEN_VAZIO
runner remoto observável               = TOKEN_VAZIO
portfolio G006 fechado                 = false
claim_allowed                          = false
certification_claim                    = false
```

Nenhum teste não executado foi convertido em `PASS`. O máximo seguro atingido
neste ambiente é 35/36 candidatos revisados, com o único vazio identificado,
pinado, explicado e protegido por critério de saída executável.

## Próximo gate

```text
MATERIALIZE_FULL_CC028_AND_OBSERVABLE_SCANNER_RECEIPT
```

O fechamento exige materializar o blob completo, verificar sua identidade,
ler todas as ocorrências, anexar novo lote e produzir um recibo observável do
scanner. Mesmo após isso, o fechamento do `Mapa` não fecha automaticamente os
126 repositórios do portfólio.
