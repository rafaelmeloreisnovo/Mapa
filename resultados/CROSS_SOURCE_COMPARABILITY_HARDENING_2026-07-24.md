# Endurecimento de Comparabilidade Cross-Source — 2026-07-24

```yaml
schema: rafaelia.cross-source-comparability-hardening/v2
repository: rafaelmeloreisnovo/Mapa
pull_request: 48
branch: codex/cross-source-schema-fixtures-v1
execution_date: 2026-07-24
claim_allowed: false
merge_ready: false
```

## 1. Riscos prioritários encontrados

```yaml
risks:
  - absolute_checkout_path_changed_report_hash
  - exact_record_counts_blocked_valid_growth
  - declared_test_count_did_not_prove_execution
  - two_missing_reports_could_look_equal
  - two_manifests_could_agree_on_unverified_floor_sha
  - unittest_skips_could_look_green
  - fixed_test_file_tuple_could_omit_new_tests
```

## 2. Controles implantados

### 2.1 Registry independente do host

```text
repo file  → indices/CROSS_SOURCE_REGISTRY.jsonl
external   → external://<basename>
```

Caminhos absolutos e diretórios temporários não entram nos relatórios selados.

### 2.2 Piso evolutivo v2

```yaml
schema_version: rafaelia.cross-source-gate-floor/v2
minimums:
  test_files: 7
  tests_discovered: 58
  tests_run: 58
  valid_fixtures: 2
  invalid_fixtures: 1
  registry_records: 10
  provider_counts:
    github: 2
    google_drive: 8
  custody_events: 13
invariants:
  complete_execution: true
  clean_outcomes: true
  failures: 0
  errors: 0
  skipped: 0
  expected_failures: 0
  unexpected_successes: 0
  claim_allowed: false
  remote_ci_substituted: false
```

O valor 58 é uma exigência a provar. A execução integral ainda é `TOKEN_VAZIO`.

### 2.3 Executor de testes v4

O executor:

- descobre sete arquivos governados por padrões explícitos;
- conta casos antes da execução;
- exige `tests_run == tests_discovered`;
- converte skip, expected failure e unexpected success em FAIL;
- retorna exit code 1 quando o resultado não é limpo.

### 2.4 Avaliador v3

O avaliador bloqueia:

- redução de arquivos ou testes;
- execução incompleta;
- resultados especiais do `unittest`;
- defeitos em registry ou custódia;
- claim ou CI substituída localmente.

### 2.5 Manifesto v3

```yaml
schema_version: rafaelia.cross-source-local-gate/v3
test_file_count: observado
minimum_test_file_count: 7
test_count_discovered: observado
test_count_observed: observado
minimum_test_count: 58
complete_test_execution: true
clean_test_outcomes: true
report_count: 5
quality_floor:
  path: indices/CROSS_SOURCE_GATE_FLOOR.json
  schema_version: rafaelia.cross-source-gate-floor/v2
  sha256: calculado_do_arquivo_real
  status: PASS
claim_allowed: false
remote_ci_substituted: false
```

### 2.6 Comparador v3

O comparador:

- valida `CHECKSUMS.sha256`;
- recompõe hashes dos cinco relatórios;
- rejeita ausência dupla como igualdade;
- valida os manifestos;
- carrega o arquivo real do piso;
- exige que o SHA declarado corresponda ao piso real;
- compara os cinco relatórios byte a byte.

### 2.7 Workflow

O workflow:

- cobre todos os scripts, testes, piso, schema e registries nos filtros;
- executa o mesmo gate do Termux;
- valida o bundle contra o piso do checkout;
- exige execução completa e limpa antes do upload.

## 3. Provas executadas

### 3.1 Comparador exato

```yaml
harness: exact_module_harness
result: PASS_6_OF_6
covers:
  - identical_reports_across_environment_metadata
  - resealed_content_difference
  - equal_absence
  - unsealed_tampering
  - claim_and_completeness_boundaries
  - real_floor_changed_after_seal
```

### 3.2 Avaliador exato

```yaml
harness: exact_module_harness
result: PASS_5_OF_5
subtest_regressions:
  - test_file_count
  - tests_discovered
  - tests_run
  - complete_execution
  - clean_outcomes
  - skipped
  - expected_failures
  - unexpected_successes
```

### 3.3 Executor dinâmico

```yaml
clean_scenario:
  files_discovered: 7
  tests_discovered: 7
  tests_run: 7
  clean_outcomes: true
  status: PASS
skip_scenario:
  unittest_display: "OK (skipped=1)"
  process_exit_code: 1
  skipped: 1
  clean_outcomes: false
  gate_status: FAIL
```

### 3.4 Provas anteriores preservadas

```yaml
automatic_discovery_harness: PASS_3_OF_3
path_normalization_harness: PASS_3_OF_3
equal_absence_targeted_check:
  comparison_status: FAIL
  matching_report_count: 4
  missing_report_match: false
```

Essas provas validam os componentes. Não são apresentadas como execução integral do repositório.

## 4. Execução integral local

Foi tentado clone read-only no ambiente local de validação.

```yaml
result: TOKEN_VAZIO
reason: container_without_external_dns
observed_error: "Could not resolve host: github.com"
repository_code_executed: false
claim_allowed: false
```

O impedimento é do ambiente de serviço, não evidência positiva ou negativa sobre o gate.

## 5. Execução remota

O último estado observado antes desta consolidação permaneceu:

```yaml
workflow_recognized: true
job_created: true
steps: null
logs_url: null
runner_started: false
checkout_executed: false
gate_executed: false
code_failure_observed: false
exact_root_cause: TOKEN_VAZIO
```

A execução do novo head deve ser novamente observada, mas qualquer run com `steps: null` permanece pré-código.

## 6. Reconciliação da história

```yaml
commit_present_only_in_main: 1
files_changed_in_main_to_branch_direction: 0
history_only_merge_supported: true
create_pull_request_endpoint: repeated_502
auxiliary_branch: reconcile/pr48-main-20260724
reconciliation: TOKEN_VAZIO
main_modified: false
content_loss: false
```

Nenhum force-push, rebase destrutivo ou alteração no `main` foi realizado.

## 7. Estado consolidado

```yaml
path_independent_reports: implemented
growth_safe_floor_v2: implemented
automatic_test_discovery: implemented
complete_execution_check: implemented
clean_outcomes_check: implemented
real_floor_binding: implemented
bundle_comparator_v3: implemented
workflow_trigger_coverage: implemented
component_harnesses: PASS
full_checkout_local_gate: TOKEN_VAZIO
remote_runner_started: TOKEN_VAZIO
remote_gate_pass: TOKEN_VAZIO
branch_history_reconciled: TOKEN_VAZIO
merge_ready: false
claim_allowed: false
```

## 8. Próximo passo verificável

1. executar `sh scripts/run_cross_source_gate.sh` no checkout integral do Termux;
2. exigir sete arquivos, 58 ou mais testes descobertos e a mesma quantidade executada;
3. exigir zero skips e resultados especiais;
4. preservar o pacote local;
5. restaurar o início do runner remoto;
6. baixar o artifact do commit exato;
7. executar:

```sh
python3 scripts/compare_cross_source_evidence.py \
  --left .artifacts/cross-source-local \
  --right .artifacts/cross-source-remote \
  --floor indices/CROSS_SOURCE_GATE_FLOOR.json \
  --write-report .artifacts/cross-source-comparison.json
```

8. exigir `status=PASS` e `matching_report_count=5`;
9. anexar evento `VALIDATE` à cadeia;
10. reconciliar a história;
11. somente então avaliar `ready for review`.

---

```text
F_ok   = superfície descoberta + execução completa + resultados limpos + piso real + hashes 5/5
F_gap  = checkout integral + artifact remoto + reconciliação
F_next = Termux 58/58 limpo → runner real → comparação → VALIDATE
```
