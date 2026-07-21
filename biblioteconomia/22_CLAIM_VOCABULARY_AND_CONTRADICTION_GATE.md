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
conformidade.

`CERTIFIED` permanece proibido.

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

## Execução local

```bash
python3 -m py_compile scripts/validate_claim_vocabulary.py
python3 -m py_compile tests/test_claim_vocabulary.py
python3 -m unittest tests/test_claim_vocabulary.py -v
python3 scripts/validate_claim_vocabulary.py \
  --root . \
  --policy indices/CLAIM_VOCABULARY_POLICY.json \
  --write-report claim-vocabulary-validation.json
```

## Estado do gap

```text
G006 control implementation in Mapa = IMPLEMENTED_LOCAL_SCOPE
portfolio-wide scan                 = TOKEN_VAZIO
portfolio exit criteria             = false
claim_allowed                       = false
certification_claim                 = false
```

O P0 não é fechado para os 126 repositórios até que cada autoridade execute o
scanner, trate os candidatos e produza recibos reproduzíveis. O presente passo
materializa o controle e sua cobertura adversarial sem fabricar fechamento.
