# P0 G006 — baseline máxima do gate de linguagem e contradição

Data inicial: 2026-07-20  
Resolução CC028: 2026-07-21  
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
indices/CLAIM_REVIEW_RESOLUTION_CC028.json
indices/claim_review_batches/CLAIM_REVIEW_BATCH_001_2026-07-20.json
indices/claim_review_batches/CLAIM_REVIEW_BATCH_002_2026-07-20.json
indices/claim_review_batches/CLAIM_REVIEW_BATCH_003_2026-07-21.json
schemas/claim-contradiction-ledger.schema.json
scripts/validate_claim_vocabulary.py
scripts/validate_claim_contradiction_ledger.py
scripts/validate_claim_review_chain.py
scripts/validate_claim_review_residual.py
scripts/validate_claim_discovery_precision.py
scripts/validate_g006_auxiliary_receipt.py
scripts/run_g006_local_gate.py
tools/materialize_github_blob.py
tests/test_claim_vocabulary.py
tests/test_claim_contradiction_ledger.py
tests/test_claim_review_chain.py
tests/test_claim_review_residual.py
tests/test_claim_discovery_precision.py
tests/test_github_blob_materializer.py
tests/test_g006_local_gate.py
tests/test_g006_auxiliary_receipt.py
resultados/G006_AUXILIARY_LOCAL_VALIDATION_2026-07-21.json
docs/G006_LOCAL_EXECUTION.md
.github/workflows/topology-validation.yml
```

## Snapshot delimitado

A busca indexada por `COMPLETE` no commit
`4016c51e024573a3875457fceb6d05926e07a07b` produziu 36 arquivos candidatos.
Esse conjunto é uma baseline de descoberta, não uma afirmação de que a busca de
código substitui uma varredura byte a byte atualizada.

```text
candidate_count          = 36
base reviewed safe       = 6
batch 001 decisions      = 14
batch 002 decisions      = 15
batch 003 decisions      = 1
reviewed safe final      = 36
reviewed blocking final  = 0
TOKEN_VAZIO final        = 0
review completion        = 36/36 = 1.0
claim_allowed            = false
certification_claim      = false
```

A revisão integral da baseline indexada não fecha automaticamente o G006 no
portfólio. Ela fecha somente a classificação semântica dos 36 candidatos do
snapshot pinado.

## Arquitetura append-only

```text
ledger-base imutável
  ↓
review batch 001 — 14 transições pinadas
  ↓
review batch 002 — 15 transições pinadas
  ↓
residual histórico CC028 — duas respostas truncadas preservadas
  ↓
resolução byte-idêntica CC028
  ↓
review batch 003 — uma transição pinada
  ↓
HEAD atômico — 36 safe / 0 blocking / 0 TOKEN_VAZIO
```

A falha histórica não foi apagada. Ela permanece no residual com os dois métodos
tentados, o blob observado e o estado de conhecimento daquele momento.

## Resolução byte-idêntica do CC028

O arquivo `indices/REPOSITORY_INVENTORY.json` é um JSON em uma única linha.
A resposta UTF-8 e a leitura direta do blob foram truncadas. A rota alternativa
usou o conteúdo Base64 do GitHub dividido em seis intervalos alinhados:

```text
1–80
81–160
161–240
241–320
321–400
401–437
```

Resultado da reconstrução:

```text
encoded lines                       = 437
decoded size                        = 19,542 bytes
Git blob SHA-1                      = b43554096f00c0918997dd9f9b11787cec4d4e52
calculated Git blob SHA-1           = b43554096f00c0918997dd9f9b11787cec4d4e52
SHA-256                             = b19d27084e5be35a2597f07346450745abfd7084c0a831b48e0eef4c57058e02
JSON parse                          = PASS
repository records                  = 41
scope.state                         = PARTIAL
scope.claim_allowed                 = false
absence_ledger.state                = TOKEN_VAZIO
declared canonical BLAKE2b-256      = 204b310de7ecbfc0e4df316d126748b03cb4ed624a3e0eff8914a3a1e8018d48
calculated canonical BLAKE2b-256    = 204b310de7ecbfc0e4df316d126748b03cb4ed624a3e0eff8914a3a1e8018d48
canonical digest match              = true
```

## Causa-raiz do falso positivo

A busca de substring encontrou `COMPLETE` dentro da chave:

```text
completeness_ratio
```

A mesma regra de fronteira do scanner foi aplicada ao texto integral:

```text
(?<![A-Z0-9_])TOKEN(?![A-Z0-9_])
```

Resultado:

```text
COMPLETE exact tokens   = 0
COMPLIANT exact tokens  = 0
ALIGNED exact tokens    = 0
CERTIFIED exact tokens  = 0
TOKEN_VAZIO exact       = 1
COMPLETE substrings     = 1
false-positive source   = completeness_ratio
```

Portanto, `CC028` foi classificado como `SAFE_EXACT_TOKEN_ABSENCE`. Isso não é
uma dispensa por nome: é uma resolução ligada a bytes, hashes, parse, digest,
contagem lexical e commit pinado.

## Prevenção de recorrência

Foi adicionado um auditor independente de precisão de descoberta:

```text
scripts/validate_claim_discovery_precision.py
tests/test_claim_discovery_precision.py
```

Ele separa:

```text
substring occurrence
!= exact boundary token
!= explicit machine claim
```

A busca ampla permanece útil para triagem, mas não pode decidir a classificação
semântica. O relatório registra totais de substring, tokens exatos e falsos
positivos lexicais por arquivo.

## Cobertura adversarial preparada

Os testes versionados cobrem, entre outros:

- promoção de claim e certificação;
- ponteiro `TOKEN_VAZIO` usado como evidência;
- adulteração de digests;
- contagens derivadas falsas;
- repetição de lote ou transição;
- caminho ou commit divergente;
- justificativa insuficiente;
- adulteração do SHA Git, SHA-256 ou tamanho materializado;
- alteração das seis faixas Base64;
- falsa alegação de ausência de token;
- reescrita da falha histórica como sucesso;
- reaparecimento silencioso do residual;
- confusão entre `completeness_ratio` e token `COMPLETE`;
- tentativa de promover o portfólio a partir da revisão do snapshot.

## Workflow único

O workflow estrutural existente foi ampliado; nenhum YAML concorrente foi
criado. Quando houver execução observável, ele deverá:

```text
compilar validadores e testes
→ executar suítes positivas e adversariais
→ validar os controles estruturais anteriores
→ executar scanner de claims
→ validar ledger-base e três lotes
→ validar residual histórico e resolução CC028
→ medir precisão lexical
→ verificar invariantes 36/36
→ produzir checksums
→ validar o recibo auxiliar contra hashes dos arquivos
→ publicar 13 relatórios e o manifesto de checksums
```

## Estado de execução

```text
materialização Base64 do CC028          = EXECUTED
identidade Git do CC028                 = VERIFIED
parse e digest canônico do CC028        = VERIFIED
varredura exata do CC028                = EXECUTED
classificação da baseline indexada      = 36/36
auxiliary py_compile                    = 4/4 PASS executado
auxiliary component tests               = 15/15 PASS executado
auxiliary receipt validator tests       = 6/6 PASS executado
auxiliary receipt file hashes           = VERIFIED
artefatos e testes versionados          = true
workflow integrado                      = IMPLEMENTED_NOT_EXECUTED
execução da suíte no clone integral     = TOKEN_VAZIO
scanner integral observável do branch   = TOKEN_VAZIO
runner remoto observável                = TOKEN_VAZIO
scope refresh posterior ao snapshot     = TOKEN_VAZIO
portfolio G006 fechado                  = false
claim_allowed                           = false
certification_claim                     = false
```

A materialização e as verificações do CC028 foram executadas. Também foram
executadas as suítes autocontidas do materializador, runner e validador do
recibo. Essas execuções auxiliares não equivalem à suíte integral do control
plane, não estão pinadas ao commit do branch e não constituem recibo remoto.

A suíte completa do branch e o workflow remoto continuam não executados; nenhum
teste apenas versionado foi convertido em `PASS`.

## Próximo gate

```text
OBSERVABLE_SCANNER_RECEIPT_AND_SCOPE_REFRESH
```

O próximo fechamento delimitado exige:

1. executar a suíte em um clone integral observável;
2. produzir os 13 relatórios e checksums;
3. atualizar a busca para o head vigente e medir drift desde o snapshot pinado;
4. tratar qualquer candidato novo pela mesma cadeia append-only;
5. manter `claim_allowed=false` até decisão separada;
6. não interpretar o fechamento do `Mapa` como fechamento dos 126 repositórios.
