# Endurecimento de Comparabilidade Cross-Source — 2026-07-24

```yaml
schema: rafaelia.cross-source-comparability-hardening/v1
repository: rafaelmeloreisnovo/Mapa
pull_request: 48
branch: codex/cross-source-schema-fixtures-v1
execution_date: 2026-07-24
claim_allowed: false
merge_ready: false
```

## 1. Questão de maior impacto

O gate produzia relatórios selados, mas o relatório do registry incluía o caminho recebido em `Path.as_posix()`.

Como o caminho padrão era absoluto, Termux e GitHub Actions poderiam produzir SHA-256 diferentes para o mesmo conteúdo validado.

```yaml
risk:
  type: false_cross_environment_mismatch
  consequence: local_and_remote_hashes_not_comparable
  severity: high_for_custody
```

## 2. Correções implementadas

### 2.1 Caminho canônico

`scripts/validate_cross_source_registry.py` agora representa:

```text
arquivo dentro do repositório → caminho relativo à raiz
arquivo externo               → external://<basename>
```

Também remove caminhos absolutos das mensagens de arquivo ausente.

### 2.2 Comparador de pacotes

Criado:

```text
scripts/compare_cross_source_evidence.py
```

O comparador:

- valida os dois `CHECKSUMS.sha256`;
- recompõe os hashes dos cinco relatórios;
- valida os campos governados dos dois manifestos;
- compara os cinco hashes;
- exige o mesmo SHA-256 do piso de qualidade;
- rejeita claim local e substituição artificial da CI;
- não considera dois arquivos ausentes como correspondência.

### 2.3 Descoberta automática de testes

`scripts/run_cross_source_tests.py` deixou de depender de uma tupla fixa de arquivos.

```yaml
patterns:
  - test_cross_source*.py
  - test_compare_cross_source_evidence.py
  - test_validate_chain_of_custody.py
ordering: deterministic
uniqueness: enforced
scope: tests_directory_only
```

### 2.4 Workflow

O workflow agora:

- dispara quando o comparador ou seus testes mudam;
- executa o gate único;
- usa `validate_bundle()` para conferir relatórios, manifesto e checksums;
- exige o caminho canônico `indices/CROSS_SOURCE_REGISTRY.jsonl`;
- preserva `claim_allowed=false`.

## 3. Provas executadas nesta intervenção

```yaml
comparator_harness:
  tests: 5
  passed: 5
  covers:
    - identical_reports_with_different_environment_metadata
    - resealed_content_difference
    - unsealed_tampering
    - claim_promotion
    - quality_floor_mismatch

equal_absence_targeted_check:
  result: PASS
  observed:
    comparison_status: FAIL
    matching_report_count: 4
    missing_report_match: false

automatic_discovery_harness:
  tests: 3
  passed: 3
  covers:
    - sorted_unique_nonempty
    - comparator_and_runner_included
    - no_path_escape

path_normalization_harness:
  tests: 3
  passed: 3
  covers:
    - repository_relative_path
    - identical_external_reports_across_directories
    - no_host_path_leak
```

Esses harnesses são evidência dos componentes alterados. Não são registrados como execução integral do checkout.

## 4. Execução remota observada

No head `e6d145b9651d9a6788b0fab1a672e50fccdfd893`:

```yaml
workflow: Cross-Source Record Validation
run_id: 30120981225
run_number: 39
job_id: 89573293524
status: completed
conclusion: failure
steps: null
logs_url: null
```

Classificação correta:

```yaml
runner_started: false
checkout_executed: false
gate_executed: false
code_failure_observed: false
exact_root_cause: TOKEN_VAZIO
claim_allowed: false
```

## 5. Reconciliação de história

A comparação entre a branch da PR #48 e `main` demonstrou:

```yaml
commit_present_only_in_main: 1
files_changed_in_main_to_branch_direction: 0
safe_history_only_merge: supported
```

Foram tentadas rotas de PR para reconciliar a ancestralidade. O endpoint de criação de PR retornou `502` repetidamente.

Uma branch auxiliar foi criada com sucesso:

```text
reconcile/pr48-main-20260724
```

Nenhum merge, force-push ou alteração no `main` foi realizado.

```yaml
reconciliation: TOKEN_VAZIO
reason: connector_create_pull_request_upstream_502
content_loss: false
main_modified: false
```

## 6. Estado consolidado

```yaml
path_independent_reports: implemented
bundle_comparator: implemented
automatic_test_discovery: implemented
workflow_trigger_coverage: implemented
component_harnesses: PASS
full_checkout_local_gate: TOKEN_VAZIO
remote_runner_started: false
remote_gate_pass: TOKEN_VAZIO
branch_history_reconciled: TOKEN_VAZIO
merge_ready: false
claim_allowed: false
```

## 7. Próximo passo verificável

1. executar `sh scripts/run_cross_source_gate.sh` no checkout integral do Termux;
2. preservar o pacote local completo;
3. restaurar o início do runner remoto;
4. baixar o artifact remoto;
5. executar:

```sh
python3 scripts/compare_cross_source_evidence.py \
  --left .artifacts/cross-source-local \
  --right .artifacts/cross-source-remote \
  --write-report .artifacts/cross-source-comparison.json
```

6. exigir `status=PASS` e `matching_report_count=5`;
7. anexar evento `VALIDATE` à cadeia;
8. reconciliar a história da branch;
9. somente então avaliar `ready for review`.

---

```text
F_ok   = caminhos canônicos + comparação selada + descoberta automática + testes adversariais
F_gap  = checkout integral, artifact remoto e reconciliação ainda sem evidência concluída
F_next = gate Termux → runner real → comparação 5/5 → custódia VALIDATE
```
