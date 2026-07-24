# Cross-Source Gate Status — 2026-07-23/24

```yaml
schema: rafaelia.cross-source-gate-status/v2
repository: rafaelmeloreisnovo/Mapa
branch: codex/cross-source-schema-fixtures-v1
pull_request: 48
base_merge_commit: bf578bca782cdf244f7885864eaa1deadc256af7
observed_head: 517cbb071440dc7b743ef64ec645346e1706a01d
claim_allowed: false
merge_ready: false
remote_gate_state: TOKEN_VAZIO
```

## 1. Escopo implementado

O bloco cross-source materializa a arquitetura GitHub ↔ Google Drive ↔ Termux ↔ sessão em:

- JSON Schema Draft 2020-12 para registros individuais;
- fixtures positivas e negativa;
- validador determinístico com Python standard library;
- registry JSONL com nós observados em GitHub e Google Drive;
- validador do grafo completo;
- ledger append-only de cadeia de custódia;
- testes adversariais;
- executor que mede a quantidade real de testes;
- piso versionado de não regressão;
- avaliador de crescimento append-only;
- gate offline único para Termux e CI;
- workflow read-only com artifact de evidência;
- smoke test de runner sem checkout ou actions externas.

## 2. Correção de maior impacto

O gate anterior continha duas fragilidades:

```yaml
registry_record_count: exatamente_10
test_count: declarado_38
```

Isso congelava a expansão do mapa e confundia valor esperado com observação executada.

O gate v2 usa:

```text
observado >= mínimo versionado
```

Piso atual em `indices/CROSS_SOURCE_GATE_FLOOR.json`:

```yaml
minimums:
  tests_run: 38
  valid_fixtures: 2
  invalid_fixtures: 1
  registry_records: 10
  provider_counts:
    github: 2
    google_drive: 8
  custody_events: 13
comparison: observed_greater_than_or_equal_to_minimum
```

Consequências:

- novos registros, provedores, eventos e testes são aceitos;
- redução silenciosa é bloqueada;
- redução deliberada do piso exige revisão separada;
- `claim_allowed=false` permanece invariável.

## 3. Evidência local executada nesta intervenção

```yaml
evaluator_unit_tests:
  total: 5
  passed: 5
  validates:
    - snapshot_no_piso
    - crescimento_append_only
    - bloqueio_de_reducao_de_registry
    - bloqueio_de_reducao_de_testes
    - bloqueio_de_claim_local
static_contract_and_posix_harness:
  total: 13
  passed: 13
  validates:
    - sintaxe_posix
    - fronteira_offline
    - comandos_proibidos
    - cinco_relatorios
    - piso_de_crescimento
    - redirecionamento_de_pycache
dynamic_test_loader_harness:
  total: 16
  passed: 16
  observed_test_count: 16
  failures: 0
  errors: 0
full_checkout_gate:
  state: TOKEN_VAZIO
  reason: checkout_privado_integral_nao_materializado_e_runner_remoto_sem_steps
```

Os harnesses comprovam os componentes novos. Eles não são apresentados como execução integral do repositório.

## 4. Gate local canônico

```sh
sh scripts/run_cross_source_gate.sh
```

Saídas locais padrão:

```text
.artifacts/cross-source-local/
├── cross-source-test-validation.json
├── cross-source-record-validation.json
├── cross-source-registry-validation.json
├── chain-of-custody-validation.json
├── quality-floor-validation.json
├── LOCAL_GATE_STATUS.json
└── CHECKSUMS.sha256
```

Manifesto esperado:

```yaml
schema_version: rafaelia.cross-source-local-gate/v2
status: PASS
test_count_observed: valor_medido
minimum_test_count: 38
report_count: 5
quality_floor_status: PASS
promotion_state: LOCAL_PASS_REMOTE_TOKEN_VAZIO
claim_allowed: false
remote_ci_substituted: false
```

O manifesto registra também o SHA-256 do piso usado.

## 5. Estado remoto observado

### Workflow dedicado no head atual

```yaml
workflow: Cross-Source Record Validation
run_id: 30119730569
run_number: 27
head_sha: 517cbb071440dc7b743ef64ec645346e1706a01d
status: completed
conclusion: failure
job_id: 89569086477
job_name: Run canonical offline gate
steps: null
logs_url: null
```

O workflow não chegou ao checkout, ao shell ou ao Python. Portanto, não existe execução remota do código a ser interpretada como falha funcional.

### CI geral no mesmo head

```yaml
workflow: CI
run_id: 30119730609
run_number: 157
status: completed
conclusion: failure
```

### Smoke independente anteriormente observado

```yaml
workflow: Actions Runner Smoke
run_id: 30095059623
run_number: 6
job_id: 89487059577
status: completed
conclusion: failure
steps_returned: []
logs_url: null
```

A primeira instrução do smoke seria `echo RUNNER_STARTED=true`, mas nenhum passo observável foi iniciado.

## 6. Fronteira sustentada

```yaml
public_organization_control:
  repository: instituto-Rafael/relativity-living-light
  successful_workflows_observed: true
personal_private_repositories:
  Mapa: failure_before_observable_steps
  RafGitTools: failure_before_observable_steps
  termux-app-rafacodephi: failure_before_observable_steps
supported_boundary:
  owner_class: personal_account
  visibility_class: private
  failure_phase: before_first_observable_step
exact_root_cause: TOKEN_VAZIO
claim_allowed: false
```

Detalhes comparativos: `resultados/PRIVATE_REPO_ACTIONS_BOUNDARY_2026-07-24.md`.

## 7. O que a evidência não autoriza concluir

O experimento torna improvável que a causa inicial seja um erro executado em:

- sintaxe Python do gate;
- schema ou registry;
- checkout;
- upload-artifact;
- política de actions externas.

Porém ainda não distingue entre:

- minutos ou orçamento bloqueado;
- Actions desabilitado para repositórios privados;
- política da conta pessoal;
- entitlement ou provisionamento de runner hospedado;
- bloqueio administrativo específico.

Portanto:

```yaml
causa_raiz_exata: TOKEN_VAZIO
conclusao_negativa_sobre_codigo: false
promocao_do_gate: blocked
```

## 8. História da branch

```yaml
ahead_of_main: 21
behind_main: 1
mergeable: true
behind_commit_meaning: merge_commit_da_PR_46
reconciliation_state: TOKEN_VAZIO
```

A divergência deve ser reconciliada sem reescrever histórico antes da promoção final.

## 9. Proteções mantidas

1. A PR permanece `DRAFT`.
2. `claim_allowed=false` em fixtures, registry, relatórios e avaliador.
3. A raiz duplicada do Drive permanece `TOKEN_VAZIO` e `deletion_allowed=false`.
4. Nenhuma sincronização automática foi declarada.
5. Nenhum conteúdo privado do Drive foi copiado; somente metadados e relações autorizadas foram registrados.
6. O gate local não se apresenta como substituto da CI remota.
7. Redução do piso no mesmo commit que remove evidência é tratada como regressão.
8. Nenhum merge deve ocorrer enquanto o workflow remoto não produzir passos e artifact inspecionável.

## 10. Próximo passo verificável

Na conta pessoal `rafaelmeloreisnovo`:

1. executar o gate completo em um checkout integral no Termux;
2. preservar cinco relatórios, manifesto e checksums;
3. abrir `Settings → Billing and licensing → Usage/Budgets`;
4. verificar minutos, orçamento e bloqueio de cobrança para repositórios privados;
5. abrir `Mapa → Settings → Actions → General`;
6. confirmar que Actions e runners hospedados estão permitidos;
7. reexecutar primeiro `Actions Runner Smoke`;
8. exigir `RUNNER_STARTED=true` em um step real;
9. reexecutar o workflow cross-source;
10. exigir artifact `cross-source-validation` com cinco relatórios;
11. comparar hashes e resultados local/remoto;
12. anexar evento `VALIDATE` à cadeia;
13. reconciliar a branch com o merge de `main`;
14. somente então avaliar `ready for review`.

---

```text
F_ok   = piso versionado + testes medidos + crescimento permitido + regressão bloqueada
F_gap  = gate integral e runner remoto ainda sem evidência executada
F_next = PASS integral no Termux → runner iniciado → artifact remoto comparável
```
