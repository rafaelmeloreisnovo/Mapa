# Actions Runner Smoke — 2026-07-24

```yaml
schema: rafaelia.actions-runner-diagnostic/v1
repository: rafaelmeloreisnovo/Mapa
pull_request: 46
branch: codex/cross-source-schema-fixtures-v1
head_sha: e0e78ffdea291446b85bb517a3beca421e0b438b
claim_allowed: false
merge_ready: false
```

## 1. Pergunta falsificável

A falha dos workflows nasce no código, no uso de ações externas ou antes da execução do primeiro passo pelo runner?

## 2. Experimento mínimo

Foi criado o workflow:

```text
.github/workflows/actions-runner-smoke.yml
```

Propriedades deliberadas:

- não executa `actions/checkout`;
- não executa `actions/upload-artifact`;
- não usa qualquer action externa ou local;
- não lê arquivos do repositório;
- não usa secrets;
- declara `permissions: {}`;
- contém somente dois passos `run` com Bash e Python já fornecidos pelo runner;
- timeout de dois minutos.

A primeira instrução executável seria:

```text
echo "RUNNER_STARTED=true"
```

## 3. Resultado remoto observado

```yaml
workflow: Actions Runner Smoke
workflow_run_id: 30094789015
run_number: 1
status: completed
conclusion: failure
job:
  id: 89486185805
  name: Zero-dependency runner smoke
  status: completed
  conclusion: failure
  steps_returned: []
  logs_url: null
log_download:
  result: BlobNotFound
artifact_count: 0
```

O mesmo head também produziu:

```yaml
cross_source_validation:
  run_id: 30094788984
  run_number: 7
  conclusion: failure
ci_general:
  run_id: 30094789009
  run_number: 137
  conclusion: failure
```

## 4. Inferência limitada

O smoke test não depende de:

- conteúdo do schema;
- fixtures;
- registry;
- validadores Python do projeto;
- checkout;
- política de actions de terceiros;
- artifact upload.

Como ele encerrou sem qualquer passo observável, a causa inicial encontra-se **antes da execução do conteúdo do job**, dentro do seguinte conjunto ainda não distinguido:

```yaml
candidate_boundary:
  - habilitacao_ou_politica_de_actions
  - disponibilidade_ou_provisionamento_do_runner
  - limite_ou_restricao_da_conta
  - bloqueio_administrativo_do_repositorio_privado
  - falha_de_plataforma_antes_do_step_zero
exact_root_cause: TOKEN_VAZIO
```

Esta evidência reduz a hipótese de defeito inicial no código cross-source, mas não declara que o código remoto passou.

## 5. Decisão operacional

```yaml
cross_source_code_remote_pass: TOKEN_VAZIO
runner_startup_verified: false
external_action_policy_as_root_cause: unlikely_but_not_fully_excluded
merge_allowed: false
ready_for_review: false
claim_allowed: false
```

A PR deve permanecer `DRAFT` até que um job mostre ao menos um passo iniciado e logs legíveis.

## 6. Próximo passo verificável

Na interface do GitHub:

1. abrir o run `30094789015`;
2. ler o banner exibido antes do job;
3. verificar `Settings → Actions → General`;
4. confirmar que Actions está habilitado para o repositório privado;
5. verificar limites de minutos, cobrança e runners hospedados;
6. reexecutar somente o smoke test;
7. exigir `RUNNER_STARTED=true` nos logs;
8. depois reexecutar o workflow cross-source.

---

```text
F_ok   = experimento independente de checkout, actions externas e código do projeto
F_gap  = causa exata anterior ao primeiro passo ainda não exposta pela API
F_next = liberar/provisionar o runner e observar RUNNER_STARTED=true
```
