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
schemas/claim-review-resolution.schema.json
scripts/validate_claim_vocabulary.py
scripts/validate_claim_contradiction_ledger.py
scripts/validate_claim_review_chain.py
scripts/validate_claim_review_residual.py
scripts/validate_claim_discovery_precision.py
scripts/validate_claim_resolution_contract.py
scripts/build_claim_scope_refresh.py
scripts/validate_claim_scope_refresh.py
scripts/validate_g006_auxiliary_receipt.py
scripts/run_g006_local_gate.py
tools/materialize_github_blob.py
tests/test_claim_vocabulary.py
tests/test_claim_contradiction_ledger.py
tests/test_claim_review_chain.py
tests/test_claim_review_residual.py
tests/test_claim_discovery_precision.py
tests/test_claim_resolution_contract.py
tests/test_claim_scope_refresh.py
tests/test_claim_scope_refresh_validation.py
tests/test_github_blob_materializer.py
tests/test_g006_local_gate.py
tests/test_g006_auxiliary_receipt.py
resultados/G006_AUXILIARY_LOCAL_VALIDATION_2026-07-21.json
resultados/G006_RESOLUTION_CONTRACT_LOCAL_VALIDATION_2026-07-21.json
docs/G006_LOCAL_EXECUTION.md
.github/workflows/topology-validation.yml
```

## Baseline indexada delimitada

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

A revisão integral da baseline indexada fecha somente a classificação semântica
dos 36 candidatos do snapshot pinado. Não fecha o scan do branch atual nem o
portfólio de 126 repositórios.

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
usou conteúdo Base64 do GitHub dividido em seis intervalos alinhados:

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

Portanto, `CC028` foi classificado como `SAFE_EXACT_TOKEN_ABSENCE`. A resolução
está ligada a bytes, hashes, parse, digest, contagem lexical e commit pinado.

## Contrato independente da resolução

O arquivo `scripts/validate_claim_resolution_contract.py` verifica de forma
independente:

```text
seis fronteiras obrigatórias = false
identidade Git exata
SHA-256 exato
seis faixas Base64
437 linhas codificadas
19,542 bytes decodificados
digests canônicos coincidentes
zero tokens fortes exatos
histórico residual preservado
TOKEN_VAZIO atual = 0
```

O schema `schemas/claim-review-resolution.schema.json` é descritivo. Ele não
substitui a validação executável nem prova identidade criptográfica por si só.

## Precisão de descoberta

```text
substring occurrence
!= exact boundary token
!= explicit machine claim
```

O auditor `validate_claim_discovery_precision.py` registra:

- totais de substring;
- totais de tokens exatos;
- falsos positivos lexicais;
- caminhos de todos os arquivos com token exato;
- truncamento ou ausência de cobertura;
- resolução conhecida do `CC028`.

A busca ampla permanece triagem; o token com fronteira é a unidade que alimenta
o refresh de escopo.

## Refresh fail-closed do escopo atual

O construtor `scripts/build_claim_scope_refresh.py` consome a baseline, o `HEAD`,
os relatórios do scanner e o commit atual. Ele deriva:

```text
sinais atuais já conhecidos na baseline
candidatos novos após o snapshot
entradas antigas sem sinal no scan filtrado
```

Qualquer caminho novo recebe ID estável `NCC-<12HEX>` e nasce como:

```text
state = TOKEN_VAZIO
owner_role = R12
claim_allowed = false
```

Não existe allowlist automática para novos arquivos de governança, scripts,
testes ou documentação. A ausência de sinal atual também não transforma uma
entrada histórica em resolvida.

O refresh declara sempre:

```text
filtered_scope_refresh_complete = false
full_byte_repository_scan_proven = false
portfolio_exit_criteria_met = false
claim_allowed = false
certification_claim = false
```

Seu `status=PASS` comprova construção coerente do delta; não comprova zero
candidatos novos.

## Validação independente do refresh

O arquivo `scripts/validate_claim_scope_refresh.py` recalcula:

- ID determinístico de cada candidato novo;
- unicidade e disjunção de caminhos;
- cobertura dos 36 IDs históricos;
- aritmética `conhecidos + ausentes = 36`;
- aritmética `conhecidos + novos = candidatos atuais`;
- estado `TOKEN_VAZIO` de toda novidade;
- necessidade de revisão;
- próximo gate condicionado à existência de novidades;
- sete fronteiras obrigatoriamente falsas;
- digest BLAKE2b-256 do relatório.

Assim, o construtor não é a única autoridade sobre a validade da própria saída.

## Evidência auxiliar realmente executada

No ambiente de preparação foram executados:

```text
py_compile de materializador/runner e testes = 4/4 PASS
suítes dos componentes auxiliares            = 15/15 PASS
suíte do validador do recibo auxiliar        = 6/6 PASS
contrato independente — py_compile           = PASS
contrato independente — validação canônica   = PASS
contrato independente — mutações rejeitadas  = 10/10
```

Houve ruído de inicialização do runtime de planilhas do ambiente. O ruído foi
preservado nos recibos; os processos retornaram `0` e os resultados acima não
foram afetados.

Essas execuções são autocontidas e não equivalem à suíte integral do branch, não
são recibo pinado ao commit do clone e não constituem execução remota.

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
- fronteira ausente ou promovida na resolução;
- lista de tokens exatos ou contradições truncada;
- arquivo ilegível durante refresh;
- candidato novo dispensado automaticamente;
- ID de candidato não determinístico;
- sobreposição entre conhecidos, novos e ausentes;
- ausência de sinal antigo tratada como resolução;
- próximo gate incompatível com candidatos novos;
- tentativa de promover o portfólio a partir do snapshot.

## Workflow único

O workflow estrutural existente foi ampliado; nenhum YAML concorrente foi
criado. Quando houver execução observável, ele deverá:

```text
compilar validadores e testes
→ executar suítes positivas e adversariais
→ validar controles estruturais anteriores
→ executar scanner de claims
→ validar ledger-base e três lotes
→ validar residual histórico e resolução CC028
→ medir precisão lexical
→ validar contrato independente da resolução
→ construir refresh do escopo atual
→ validar independentemente o refresh
→ verificar invariantes fail-closed
→ validar recibo auxiliar contra hashes dos arquivos
→ produzir checksums
→ publicar 16 relatórios e o manifesto de checksums
```

O gate aceita candidatos novos somente quando eles estiverem explicitamente
enumerados como `TOKEN_VAZIO`; não exige uma falsa contagem zero.

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
resolution contract targeted checks     = 10/10 rejeitados
artefatos e testes versionados          = true
workflow integrado                      = IMPLEMENTED_NOT_EXECUTED
scope refresh builder                   = IMPLEMENTED_NOT_EXECUTED
scope refresh independent validator     = IMPLEMENTED_NOT_EXECUTED
execução da suíte no clone integral     = TOKEN_VAZIO
scanner integral observável do branch   = TOKEN_VAZIO
refresh do commit atual                 = TOKEN_VAZIO
runner remoto observável                = TOKEN_VAZIO
full-byte repository receipt            = TOKEN_VAZIO
portfolio G006 fechado                  = false
claim_allowed                           = false
certification_claim                     = false
```

Nenhum teste apenas versionado foi convertido em `PASS`. Nenhum refresh ainda
não executado foi interpretado como ausência de candidatos novos.

## Próximo gate

```text
EXECUTE_OBSERVABLE_SCANNER_AND_SCOPE_REFRESH
```

O próximo fechamento delimitado exige:

1. executar a suíte em um clone integral e limpo, pinado ao commit;
2. produzir os 16 relatórios e checksums;
3. observar o número real de candidatos novos no refresh;
4. validar independentemente o relatório de refresh;
5. revisar cada candidato novo por lote append-only;
6. produzir recibo byte a byte do escopo não coberto pelo filtro;
7. manter `claim_allowed=false` até decisão separada;
8. não interpretar o fechamento do `Mapa` como fechamento dos 126 repositórios.
