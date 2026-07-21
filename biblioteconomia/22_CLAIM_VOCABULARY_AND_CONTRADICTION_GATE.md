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
  = correspondência exata dos TOKEN_VAZIO restantes
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

## Estado delimitado atual

```text
snapshot commit          = 4016c51e024573a3875457fceb6d05926e07a07b
candidate_count          = 36
review batches           = 2
review decisions         = 29
reviewed safe            = 35
reviewed blocking        = 0
TOKEN_VAZIO              = 1
review completion ratio  = 0.972222222222
```

O único residual é `CC028`, correspondente a
`indices/REPOSITORY_INVENTORY.json`. O arquivo é um JSON extenso em uma única
linha; `fetch_file` e `fetch_blob` retornaram conteúdo truncado. Embora o início
observado registre `PARTIAL` e `claim_allowed=false`, a leitura incompleta não
autoriza uma disposição semântica.

## Execução local prevista

```bash
python3 -m py_compile \
  scripts/validate_claim_vocabulary.py \
  scripts/validate_claim_contradiction_ledger.py \
  scripts/validate_claim_review_chain.py \
  scripts/validate_claim_review_residual.py

python3 -m unittest -v \
  tests/test_claim_vocabulary.py \
  tests/test_claim_contradiction_ledger.py \
  tests/test_claim_review_chain.py \
  tests/test_claim_review_residual.py

python3 scripts/validate_claim_vocabulary.py \
  --root . \
  --policy indices/CLAIM_VOCABULARY_POLICY.json \
  --write-report claim-vocabulary-validation.json

python3 scripts/validate_claim_contradiction_ledger.py \
  --write-report claim-contradiction-ledger-validation.json

python3 scripts/validate_claim_review_chain.py \
  --write-report claim-review-chain-validation.json

python3 scripts/validate_claim_review_residual.py \
  --write-report claim-review-residual-validation.json
```

Esses comandos estão versionados no workflow, mas sua execução ainda requer um
clone integral ou runner observável. Código presente não é recibo de execução.

## Estado do gap

```text
G006 control implementation in Mapa = IMPLEMENTED_NOT_EXECUTED
bounded semantic review             = 35/36
remaining residual                  = CC028 / TOKEN_VAZIO
observable full scanner receipt     = TOKEN_VAZIO
portfolio exit criteria             = false
claim_allowed                       = false
certification_claim                 = false
```

## Próximo gate

```text
MATERIALIZE_FULL_CC028_AND_OBSERVABLE_SCANNER_RECEIPT
```

O P0 não é fechado para os 126 repositórios até que cada autoridade execute o
scanner, trate seus candidatos e produza recibos reproduzíveis. O presente
controle maximiza o escopo delimitado do `Mapa` sem transformar ausência em
aprovação.
