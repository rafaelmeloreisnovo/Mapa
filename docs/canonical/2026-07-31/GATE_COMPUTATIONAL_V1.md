# RAFAELIA — `gate.computational.v1`

**Estado:** `IMPLEMENTED_LOCAL_GATE_PENDING_TERMUX_RECEIPT`  
**Autoridade do contrato:** `rafaelmeloreisnovo/Mapa`  
**Autoridade da execução:** checkout alvo + Termux local  
**Resultado máximo:** `READY_FOR_DOMAIN_SPECIFIC_REVIEW`  
**Promoção de claim:** `false`

## O que o gate prova — e o que não prova

O gate não decide ciência, conformidade, segurança, autoria jurídica, execução
em aparelho, nem comportamento de APK/ELF. Ele só decide se um **receipt de
execução local** está suficientemente amarrado para revisão específica de
domínio.

```text
receipt local
  -> checkout Git limpo + HEAD exato
  -> inputs SHA-256 ainda iguais
  -> ambiente e executáveis observados
  -> comandos completos, todos exit 0
  -> testes descobertos = executados = passados
  -> falhas = skips = 0
  -> falsificadores explicitamente exercitados
  -> COMPUTATIONAL_REVIEW_RESULT
```

O estado positivo é deliberadamente limitado a:

```text
READY_FOR_DOMAIN_SPECIFIC_REVIEW
```

Ele preserva `claim_allowed=false` e `decision=NOT_PROMOTED`.

## Entradas exigidas

1. `COMPILA/<run-id>/receipt.json` com `PASS_LOCAL_EXECUTION` e `exit_code=0`.
2. `receipt.sha256` que corresponda aos bytes do receipt.
3. `repository_identity.state=BOUND`, `head_sha` e worktree limpo.
4. `environment.json`, `input_manifest.json`, `commands.jsonl`, `stdout.log` e
   `stderr.log`, todos hasheados no receipt.
5. `test-summary.json`, produzido pelo profile de execução e também hasheado
   no receipt.

O resumo de testes usa o schema local
[`rafaelia-test-summary.v1.schema.json`](../../../foundation/schemas/rafaelia-test-summary.v1.schema.json):

```json
{
  "schema": "rafaelia.test-summary/v1",
  "counts": {
    "discovered": 2,
    "executed": 2,
    "passed": 2,
    "failed": 0,
    "skipped": 0
  },
  "tests": [
    {"id": "build", "result": "PASS"},
    {"id": "negative-input", "result": "PASS"}
  ],
  "falsifiers": [
    {
      "id": "invalid-input",
      "condition": "invalid input must fail",
      "status": "EXERCISED"
    }
  ]
}
```

O gate rejeita inventário duplicado, contagens inconsistentes, falha, skip,
teste não executado, resumo fora do receipt, alterações posteriores nos inputs
ou checkout diferente.

## Execução local

Após um profile que produza `test-summary.json`:

```sh
bash termux/autoexec-rafaelia.sh gate \
  --receipt COMPILA/<run-id>/receipt.json \
  --test-summary COMPILA/<run-id>/test-summary.json \
  --expected-profile <profile-explícito>
```

O gate cria um novo artefato append-only no mesmo diretório de execução:

```text
gate.computational.v1-<UTC>.json
gate.computational.v1-<UTC>.json.sha256
```

Os retornos são:

| Código | Resultado | Significado |
|---:|---|---|
| `0` | `READY_FOR_DOMAIN_SPECIFIC_REVIEW` | Evidência computacional íntegra e limitada a revisão de domínio |
| `2` | `TOKEN_VAZIO` | Falta evidência observável; não há promoção |
| `1` | `FAIL` | Bytes, receipt, checkout ou contagem são inconsistentes |

## Falsificadores operacionais

- mudar um arquivo listado em `input_manifest.json` após o run → `FAIL`;
- alterar um artefato hasheado após o run → `FAIL`;
- checkout em outro `HEAD` ou worktree sujo → `FAIL`/`TOKEN_VAZIO`;
- omitir ou não hashear `test-summary.json` → `TOKEN_VAZIO`;
- `executed != discovered`, `failed > 0` ou `skipped > 0` → `FAIL`;
- usar um receipt sem `PASS_LOCAL_EXECUTION` → `FAIL`.

## R3

`F_ok`: arquivo, ambiente, comandos, testes e falsificadores passam a ter
contrato verificável numa mesma decisão computacional.  
`F_gap`: não existe ainda receipt Android/Termux do commit exato de um alvo.  
`F_next`: aplicar ao primeiro profile de compilação do RafPolimata e registrar
o receipt físico antes de qualquer promoção de runtime, APK, ELF ou ciência.
