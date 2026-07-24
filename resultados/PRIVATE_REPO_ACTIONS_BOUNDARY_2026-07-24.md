# GitHub Actions Boundary — Personal Private Repositories — 2026-07-24

```yaml
schema: rafaelia.actions-boundary-analysis/v1
claim_allowed: false
exact_root_cause: TOKEN_VAZIO
operational_boundary: personal_private_repository_pre_step_startup
```

## 1. Pergunta

A falha anterior ao primeiro passo está limitada ao repositório `Mapa`, afeta toda a plataforma GitHub ou acompanha uma classe específica de repositórios?

## 2. Matriz comparativa observada

| Repositório | Proprietário | Visibilidade | Commit/PR observado | Workflows | Estado dos jobs |
|---|---|---:|---|---:|---|
| `instituto-Rafael/relativity-living-light` | organização | pública | PR #522, `665046c8...` | 9 | todos `success` |
| `instituto-Rafael/relativity-living-light` | organização | pública | PR #576, `5b7fc0ba...` | 3 | todos `success` |
| `rafaelmeloreisnovo/Mapa` | conta pessoal | privada | PR #46, `95871488...` | CI + cross-source + smoke | todos `failure`, sem steps |
| `rafaelmeloreisnovo/RafGitTools` | conta pessoal | privada | PR #267, `e9aa1ecd...` | 11 observados | todos `failure`; job consultado sem steps |
| `rafaelmeloreisnovo/termux-app-rafacodephi` | conta pessoal | privada | PR #289, `37e478b6...` | 13 observados | todos `failure`; job consultado sem steps |

## 3. Evidências específicas

### Controle positivo — RLL público

PR #522:

```yaml
head_sha: 665046c8fe3a1aee7988ed4a42deb51e918eb3f2
successful_workflows: 9
examples:
  - Validate Schema Contracts
  - Python tests
  - YAML Syntax Validation Gate
  - RLL Scientific Validation Pipeline
```

PR #576:

```yaml
head_sha: 5b7fc0bab53c2f98c03047f48cd12c5af17a3e1a
successful_workflows: 3
examples:
  - Convention Consistency Check
  - formulas-artifacts
  - Python tests
```

### Mapa privado

```yaml
runner_smoke_run: 30095059623
runner_smoke_run_number: 6
runner_smoke_job: 89487059577
conclusion: failure
steps_returned: []
logs_url: null
```

O smoke não usa checkout, actions externas, secrets nem arquivos do repositório.

### RafGitTools privado

```yaml
pr: 267
head_sha: e9aa1ecd367f7f2950e79181030130d591f06b61
ci_run: 29653305229
ci_job: 88103209217
conclusion: failure
steps_returned: []
logs_url: null
```

### Termux App privado

```yaml
pr: 289
head_sha: 37e478b638caa1493abe8dcf7a2106cfb0bece45
reference_audit_run: 29737034934
reference_audit_job: 88335476836
conclusion: failure
steps_returned: []
logs_url: null
```

O próprio PR #289 já registrava que os runs falhavam sem steps/logs suficientes para atribuir causa ao conteúdo dos workflows.

## 4. Inferência limitada

A hipótese de indisponibilidade global do GitHub Actions perde força porque repositórios públicos da organização executaram múltiplos workflows com sucesso.

A hipótese de defeito exclusivo do `Mapa` perde força porque dois outros repositórios privados da mesma conta pessoal apresentam o mesmo padrão.

A fronteira operacional mais estreita sustentada pelas observações é:

```yaml
owner_class: personal_account
visibility_class: private
failure_phase: before_first_observable_step
```

Ainda não é possível distinguir, apenas pela API disponível, entre:

```yaml
remaining_candidates:
  - included_minutes_exhausted_or_billing_restriction
  - actions_disabled_for_private_repositories
  - personal_account_actions_policy
  - hosted_runner_entitlement_or_provisioning
  - administrative_or_platform_block_specific_to_private_repos
```

## 5. Decisão

```yaml
code_changes_as_initial_root_cause: unlikely
repository_content_as_initial_root_cause: unlikely
public_github_actions_global_outage: unlikely
personal_private_actions_boundary: supported
exact_cause: TOKEN_VAZIO
merge_ready: false
claim_allowed: false
```

Nenhuma PR privada dependente deve ser promovida com base apenas em validação local enquanto essa fronteira permanecer bloqueada.

## 6. Próximo passo verificável

Na conta pessoal `rafaelmeloreisnovo`:

1. abrir `Settings → Billing and licensing → Usage`;
2. verificar minutos incluídos e eventual bloqueio de cobrança para Actions em repositórios privados;
3. abrir `Mapa → Settings → Actions → General`;
4. confirmar que Actions está habilitado;
5. conferir política de ações permitidas e acesso a runners hospedados;
6. verificar se existe banner de pagamento, spending limit ou runner indisponível no run `30095059623`;
7. corrigir a configuração encontrada;
8. reexecutar primeiro `Actions Runner Smoke`;
9. exigir `RUNNER_STARTED=true`;
10. somente depois reexecutar a CI cross-source.

---

```text
F_ok   = controles positivos públicos + três repositórios privados com padrão comum
F_gap  = API não expõe billing/settings/banner anterior ao step zero
F_next = verificar entitlement, billing e Actions General da conta pessoal privada
```
