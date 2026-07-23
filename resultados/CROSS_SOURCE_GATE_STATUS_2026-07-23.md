# Cross-Source Gate Status — 2026-07-23

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
- workflow read-only com artifact de evidência.

## 2. Evidência local limitada

```yaml
record_tests:
  total: 9
  passed: 9
registry_tests:
  total: 7
  passed: 7
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

## 3. Estado remoto observado

### Workflow dedicado

```yaml
workflow: Cross-Source Record Validation
run_id: 30054385237
run_number: 5
head_sha: b157a7ca2d18e42c3c440106546277b6cc79c523
status: completed
conclusion: failure
job_id: 89362955648
job_name: validate
steps_returned: []
logs_url: null
```

### CI geral

```yaml
workflow: CI
run_id: 30054385205
run_number: 135
head_sha: b157a7ca2d18e42c3c440106546277b6cc79c523
status: completed
conclusion: failure
```

Também foi observado que a CI geral já falhava no commit da arquitetura anterior, antes deste bloco:

```yaml
prior_commit: 59d0d6f0fa0d48fe6bd142c5c48c3899dac2bde0
prior_run_id: 29990936700
prior_run_number: 129
prior_conclusion: failure
```

## 4. Classificação correta da falha

Não há evidência suficiente para atribuir a falha remota a:

- sintaxe Python;
- teste específico;
- schema;
- runner indisponível;
- configuração de cobrança;
- política da conta;
- permissão de Actions;
- indisponibilidade transitória da plataforma.

O conector retornou o job sem passos e sem URL de logs. Tentativas de obter os logs retornaram `BlobNotFound`. Portanto:

```yaml
causa_raiz: TOKEN_VAZIO
conclusao_negativa_sobre_codigo: false
promocao_do_gate: blocked
```

## 5. Proteções mantidas

1. A PR permanece `DRAFT`.
2. `claim_allowed=false` em fixtures, registry e relatórios.
3. A raiz duplicada do Drive permanece `TOKEN_VAZIO` e `deletion_allowed=false`.
4. Nenhuma sincronização automática foi declarada.
5. Nenhum conteúdo privado do Drive foi copiado; somente IDs, títulos, relações, estados e âncoras autorizadas foram registrados.
6. Nenhum merge deve ocorrer enquanto o workflow remoto não produzir passos e evidência inspecionável.

## 6. Próximo passo verificável

1. Abrir o run `30054385237` na interface do GitHub Actions.
2. Verificar mensagem de inicialização do job, política de Actions, disponibilidade de runner e limites da conta.
3. Reexecutar o workflow somente após identificar ou remover o bloqueio.
4. Exigir artifact `cross-source-validation` com os dois relatórios em `PASS`.
5. Somente então avaliar `ready for review`; manter `claim_allowed=false` até cadeia de custódia append-only.

---

```text
F_ok   = schema + fixtures + registry + validadores + 16 testes locais
F_gap  = execução remota sem passos e sem logs úteis
F_next = diagnosticar inicialização do GitHub Actions e exigir artifact verificável
```
