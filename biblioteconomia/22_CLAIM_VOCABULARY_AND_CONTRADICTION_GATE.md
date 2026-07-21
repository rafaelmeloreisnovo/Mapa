# Vocabulário de claims e gate de contradições — P0 G006

## Propósito

Este controle reduz uma classe específica de sobredeclaração:

```text
texto completo/alinhado
∩ integração pendente
∩ execução ausente
∩ evidência TOKEN_VAZIO
```

O controle pertence ao `Mapa` porque disciplina linguagem, estado epistêmico e
ponteiros de prova. Ele não transforma o repositório em certificador e não
reivindica conformidade com ISO 9001, ISO 8000 ou ISO/IEC 27001.

## Cadeia mínima

```text
DOCUMENTED
  ↓ ponteiro de implementação
IMPLEMENTED
  ↓ ponteiro de execução
EXECUTED
  ↓ ponteiro de evidência preservada
EVIDENCED
  ↓ revisão independente, quando aplicável
INDEPENDENTLY_ASSURED
```

`COMPLETE` só é aceito para um escopo explicitamente delimitado quando os três
ponteiros existem e os estados são `IMPLEMENTED`, `EXECUTED` e `EVIDENCED` ou
`INDEPENDENTLY_ASSURED`.

`COMPLIANT` exige, além da cadeia acima, critérios, escopo e autoridade de
avaliação. Mesmo assim, a baseline atual mantém `claim_allowed=false`.

`ALIGNED` significa apenas que existe um crosswalk delimitado. Não equivale a
conformidade. `CERTIFIED` permanece proibido.

## Modo de adoção

```text
REPORT_PROSE_FAIL_EXPLICIT
```

- linguagem forte e sinais de pendência no mesmo arquivo geram candidatos para
  revisão humana;
- registros explícitos em JSON ou `CLAIM_RECORD` falham imediatamente quando a
  cadeia de prova está incompleta;
- `TOKEN_VAZIO`, `BLOCKED`, `ZERO_STEP_NO_LOGS`, `STUB` e `PLACEHOLDER` nunca
  satisfazem ponteiros de evidência;
- o scanner não promove claims, não corrige arquivos automaticamente e não
  escreve em outros repositórios.

## Registro explícito válido

```json
{
  "claim_state": "COMPLETE",
  "claim_allowed": false,
  "certification_claim": false,
  "implementation_state": "IMPLEMENTED",
  "execution_state": "EXECUTED",
  "evidence_state": "EVIDENCED",
  "implementation_pointer": "src/module.c@<git-sha>",
  "execution_pointer": "runs/local-001.json",
  "evidence_pointer": "evidence/local-001.sha256"
}
```

O exemplo demonstra o formato; não declara que algum módulo atual esteja
completo.

## Plano de controle append-only

```text
CLAIM_CONTRADICTION_LEDGER.json
  = snapshot inicial imutável dos candidatos

claim_review_batches/*.json
  = decisões incrementais pinadas por commit

CLAIM_CONTRADICTION_HEAD.json
  = estado derivado da aplicação ordenada dos lotes

CLAIM_REVIEW_RESIDUAL.json
  = recibo histórico dos TOKEN_VAZIO observados

CLAIM_REVIEW_RESOLUTION_CC028.json
  = resolução byte-idêntica do residual materializado
```

O ledger-base não é reescrito para simular progresso. Cada lote precisa:

- partir de `TOKEN_VAZIO`;
- apontar para o mesmo arquivo e commit do snapshot;
- registrar disposição, justificativa e revisor;
- preservar `claim_allowed=false`;
- declarar as contagens resultantes;
- possuir digest BLAKE2b-256.

O `HEAD` rejeita lote repetido, transição repetida, drift de caminho/commit,
contagem falsa, digest divergente e próximo gate obsoleto.

## Estado delimitado da baseline

```text
snapshot commit          = 4016c51e024573a3875457fceb6d05926e07a07b
candidate_count          = 36
review batches           = 3
review decisions         = 30
reviewed safe            = 36
reviewed blocking        = 0
TOKEN_VAZIO atual        = 0
review completion ratio  = 1.0
```

Isso significa que os 36 candidatos da baseline indexada foram classificados.
Não significa que o branch atual ou os 126 repositórios do portfólio já foram
varridos com recibo observável.

## Residual histórico e resolução CC028

O histórico preserva duas tentativas truncadas sobre:

```text
CC028
indices/REPOSITORY_INVENTORY.json
blob b43554096f00c0918997dd9f9b11787cec4d4e52
```

Depois, o conteúdo Base64 foi recuperado em seis faixas alinhadas e reconstruído
integralmente:

```text
437 linhas Base64
19,542 bytes decodificados
Git blob SHA-1 verificado
SHA-256 registrado
JSON parse PASS
BLAKE2b-256 declarado = calculado
scope.state = PARTIAL
claim_allowed = false
```

A varredura exata encontrou:

```text
COMPLETE  = 0
COMPLIANT = 0
ALIGNED   = 0
CERTIFIED = 0
```

A única ocorrência por substring era `COMPLETE` dentro de
`completeness_ratio`. A disposição final é:

```text
SAFE_EXACT_TOKEN_ABSENCE
```

A resolução não apaga o residual: falha histórica e conhecimento atual coexistem
como eventos distintos da cadeia.

## Contrato independente da resolução

```text
scripts/validate_claim_resolution_contract.py
schemas/claim-review-resolution.schema.json
tests/test_claim_resolution_contract.py
```

O validador executável exige:

- as seis fronteiras da resolução presentes e iguais a `false`;
- SHA Git, SHA-256, tamanho e faixas Base64 exatos;
- parse e digest canônico coerentes;
- zero tokens fortes exatos;
- falso positivo ligado a `completeness_ratio`;
- histórico residual preservado;
- residual atual igual a zero;
- próximo gate não promovido.

O schema é descritivo e não substitui o validador nem prova identidade de bytes.

## Precisão de descoberta

```text
substring occurrence
!= exact boundary token
!= explicit machine claim
```

O auditor `validate_claim_discovery_precision.py` mede separadamente:

- quantidade de substrings;
- quantidade de tokens exatos;
- falsos positivos lexicais;
- todos os caminhos com token exato;
- truncamento da lista;
- arquivos ilegíveis ou ignorados por tamanho;
- resolução conhecida do `CC028`.

A busca ampla é triagem. A fronteira semântica é o token exato:

```text
(?<![A-Z0-9_])TOKEN(?![A-Z0-9_])
```

## Refresh do escopo atual

```text
scripts/build_claim_scope_refresh.py
tests/test_claim_scope_refresh.py
```

O construtor recebe a baseline, o `HEAD`, o scanner, o relatório de precisão e o
commit atual. Ele separa:

```text
sinais atuais já conhecidos
candidatos novos após o snapshot
entradas históricas sem sinal no scan filtrado
```

Caminhos novos recebem ID determinístico:

```text
NCC-<12HEX>
```

E são preservados como:

```text
state = TOKEN_VAZIO
owner_role = R12
claim_allowed = false
```

Nenhum arquivo novo é considerado seguro por pertencer a `scripts/`, `tests/`,
`docs/`, `indices/` ou `.github/`. Ausência de sinal no scan filtrado também não
significa resolução ou autorização de remoção.

O refresh nunca declara que o scan filtrado é varredura byte a byte. Seu
`status=PASS` significa apenas que o delta foi construído sem perda silenciosa.

## Execução local

A rota completa e segura para Termux/Linux está em:

```text
docs/G006_LOCAL_EXECUTION.md
```

Ela oferece:

- materialização GitHub Base64 com verificação de objeto Git;
- token por variável de ambiente, sem eco em argumentos ou recibos;
- escrita atômica em modo `0600`;
- runner pinado ao commit e árvore limpa;
- logs separados por comando;
- checksums dos controles;
- contrato independente da resolução;
- refresh posterior explícito;
- recibo agregado fail-closed.

## Evidência auxiliar executada

```text
py_compile de materializador/runner e testes = 4/4 PASS
suítes dos componentes auxiliares            = 15/15 PASS
suíte do validador do recibo auxiliar        = 6/6 PASS
contrato da resolução — py_compile           = PASS
contrato da resolução — validação canônica   = PASS
contrato da resolução — mutações rejeitadas  = 10/10
```

O ruído externo de aquecimento do runtime de planilhas foi preservado nos
recibos; os processos retornaram `0` e o ruído não alterou os resultados.

Essas execuções são delimitadas. Elas não constituem a suíte integral do branch,
recibo pinado ao commit do clone ou execução remota.

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
→ validar contrato independente da resolução
→ construir refresh do escopo atual
→ verificar as fronteiras fail-closed
→ validar recibo auxiliar contra hashes
→ produzir checksums
→ publicar 15 relatórios e o manifesto de checksums
```

O workflow não exige zero candidatos novos. Ele exige que qualquer candidato
novo esteja explicitamente enumerado como `TOKEN_VAZIO`.

## Estado do gap

```text
G006 control implementation in Mapa = IMPLEMENTED_NOT_EXECUTED
bounded indexed semantic review     = 36/36
current indexed residual            = 0
historical residual preserved       = CC028
CC028 materialization               = VERIFIED
auxiliary component tests           = 15/15 PASS
auxiliary receipt-validator tests   = 6/6 PASS
resolution contract targeted checks = 10/10 rejected
observable full scanner receipt     = TOKEN_VAZIO
current-commit scope refresh         = TOKEN_VAZIO
full-byte repository receipt        = TOKEN_VAZIO
portfolio exit criteria             = false
claim_allowed                       = false
certification_claim                 = false
```

## Próximo gate

```text
EXECUTE_OBSERVABLE_SCANNER_AND_SCOPE_REFRESH
```

O próximo passo é executar o controle em clone integral e limpo, produzir os 15
relatórios e checksums, observar os candidatos novos reais e revisar cada um por
lote append-only. Depois ainda será necessário produzir evidência byte a byte do
escopo não coberto pelo filtro.

O P0 não é fechado para os 126 repositórios até que cada autoridade execute o
scanner, trate seus candidatos e produza recibos reproduzíveis. O presente
controle maximiza o escopo delimitado do `Mapa` sem transformar ausência em
aprovação.
