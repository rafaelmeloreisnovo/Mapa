# Cross-Source Gate Status — 2026-07-23/24

```yaml
schema: rafaelia.cross-source-gate-status/v1
repository: rafaelmeloreisnovo/Mapa
branch: codex/cross-source-schema-fixtures-v1
pull_request: 46
claim_allowed: false
merge_ready: false
remote_gate_state: TOKEN_VAZIO
```

## 1. Escopo validado

O bloco cross-source materializa a arquitetura GitHub ↔ Google Drive ↔ Termux ↔ sessão em:

- JSON Schema Draft 2020-12 para registros individuais;
- fixtures positivas e negativa;
- validador determinístico com Python standard library;
- registry JSONL com nós observados em GitHub e Google Drive;
- validador do grafo completo;
- testes adversariais;
- gate offline único para Termux e CI;
- workflow read-only com artifact de evidência;
- smoke test de runner sem checkout ou actions externas.

## 2. Evidência local limitada

```yaml
record_tests:
  total: 9
  passed: 9
registry_tests:
  total: 7
  passed: 7
local_gate_contract_tests:
  total: 6
registry_report:
  status: PASS
  record_count: 10
  provider_counts:
    github: 2
    google_drive: 8
  epistemic_state_counts:
    CONVENCAO: 1
    VERIFIED_LIMITED: 8
    TOKEN_VAZIO: 1
  defect_count: 0
  claim_allowed: false
```

A validação local demonstra coerência estrutural no ambiente em que foi reproduzida. Ela não substitui a execução remota do workflow nem promove qualquer claim sobre sincronização automática.

O mesmo gate pode ser executado em Termux ou qualquer ambiente com Python 3:

```sh
sh scripts/run_cross_source_gate.sh
```

Saídas locais padrão:

```text
.artifacts/cross-source-local/
├── cross-source-record-validation.json
├── cross-source-registry-validation.json
├── LOCAL_GATE_STATUS.json
└── CHECKSUMS.sha256
```

O manifesto declara explicitamente:

```yaml
claim_allowed: false
remote_ci_substituted: false
```

## 3. Estado remoto observado

### Workflow dedicado

```yaml
workflow: Cross-Source Record Validation
latest_observed_run: 30095059615
run_number: 12
head_sha: 95871488ebaec2b2db5119afaf99cc50a140ee3e
status: completed
conclusion: failure
```

Ciclos anteriores também retornaram jobs sem passos e sem URL de logs.

### Smoke sem dependências

```yaml
workflow: Actions Runner Smoke
run_id: 30095059623
run_number: 6
job_id: 89487059577
job_name: Zero-dependency runner smoke
status: completed
conclusion: failure
steps_returned: []
logs_url: null
```

O smoke não usa:

- checkout;
- upload de artifact;
- actions externas;
- secrets;
- conteúdo do repositório;
- permissões de escrita.

A primeira instrução seria `echo RUNNER_STARTED=true`, mas nenhum passo observável foi iniciado.

### CI geral

```yaml
workflow: CI
latest_observed_run: 30095059628
run_number: 142
head_sha: 95871488ebaec2b2db5119afaf99cc50a140ee3e
status: completed
conclusion: failure
```

A CI geral já falhava no commit da arquitetura anterior, antes deste bloco:

```yaml
prior_commit: 59d0d6f0fa0d48fe6bd142c5c48c3899dac2bde0
prior_run_id: 29990936700
prior_run_number: 129
prior_conclusion: failure
```

## 4. Fronteira comparativa

Foi realizada uma comparação entre classes de repositório:

```yaml
public_organization_control:
  repository: instituto-Rafael/relativity-living-light
  pr_522_successful_workflows: 9
  pr_576_successful_workflows: 3
personal_private_repositories:
  Mapa: failure_before_observable_steps
  RafGitTools: failure_before_observable_steps
  termux-app-rafacodephi: failure_before_observable_steps
```

A fronteira mais estreita sustentada pela evidência é:

```yaml
owner_class: personal_account
visibility_class: private
failure_phase: before_first_observable_step
```

Detalhes: `resultados/PRIVATE_REPO_ACTIONS_BOUNDARY_2026-07-24.md`.

## 5. Classificação correta da falha

O experimento torna improvável que a causa inicial seja:

- sintaxe Python do gate;
- teste cross-source específico;
- schema ou registry;
- checkout;
- upload-artifact;
- política de actions externas;
- indisponibilidade global do GitHub Actions.

Ainda não há evidência suficiente para distinguir entre:

- minutos incluídos esgotados ou cobrança bloqueada;
- Actions desabilitado para repositórios privados;
- política da conta pessoal;
- entitlement ou provisionamento de runner hospedado;
- bloqueio administrativo específico dos repositórios privados.

Portanto:

```yaml
causa_raiz_exata: TOKEN_VAZIO
fronteira_operacional: personal_private_repository_pre_step_startup
conclusao_negativa_sobre_codigo: false
promocao_do_gate: blocked
```

## 6. Proteções mantidas

1. A PR permanece `DRAFT`.
2. `claim_allowed=false` em fixtures, registry e relatórios.
3. A raiz duplicada do Drive permanece `TOKEN_VAZIO` e `deletion_allowed=false`.
4. Nenhuma sincronização automática foi declarada.
5. Nenhum conteúdo privado do Drive foi copiado; somente IDs, títulos, relações, estados e âncoras autorizadas foram registrados.
6. O gate local não se apresenta como substituto da CI remota.
7. Nenhum merge deve ocorrer enquanto o workflow remoto não produzir passos e evidência inspecionável.

## 7. Próximo passo verificável

Na conta pessoal `rafaelmeloreisnovo`:

1. abrir `Settings → Billing and licensing → Usage`;
2. verificar minutos de Actions e eventual bloqueio de cobrança para repositórios privados;
3. abrir `Mapa → Settings → Actions → General`;
4. confirmar que Actions está habilitado e runners hospedados são permitidos;
5. abrir o run `30095059623` e ler o banner anterior ao job;
6. corrigir a restrição observada;
7. reexecutar primeiro `Actions Runner Smoke`;
8. exigir `RUNNER_STARTED=true` nos logs;
9. reexecutar o workflow cross-source;
10. exigir artifact `cross-source-validation` com relatórios em `PASS`;
11. somente então avaliar `ready for review`.

---

```text
F_ok   = schema + registry + validadores + gate único + testes + smoke comparativo
F_gap  = entitlement/billing/política exata não exposta pela API disponível
F_next = liberar Actions em repositório privado e observar o primeiro step real
```
