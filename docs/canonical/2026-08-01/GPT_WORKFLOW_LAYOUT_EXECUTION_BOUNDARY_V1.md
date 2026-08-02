# Fronteira de Execução — GPT Project Workflow Layout V1

**Corte:** 2026-08-01  
**Estado:** `ACTIVE_CONTEXT_BOUNDARY`  
**Claim:** este ambiente é uma camada de orquestração e contexto; não é automaticamente equivalente a GitHub Actions, Termux físico ou replicação independente.

## 1. Camadas de execução

```text
L0 — GPT Project Workflow Layout
     contexto do projeto, instruções, memória, arquivos, conectores e orquestração

L1 — Connector Execution
     gravações reais em GitHub/Google Drive quando uma ação do conector retorna sucesso

L2 — OpenAI Container
     execução local de código no ambiente isolado do modelo

L3 — GitHub Actions
     execução remota nos runners do GitHub, com run/job/step próprios

L4 — Termux físico / Android
     execução no dispositivo do usuário

L5 — Replicação independente
     execução por terceiro ou ambiente independente com entradas e tolerâncias congeladas
```

## 2. Invariante de proveniência

Todo resultado deve carregar:

```yaml
executor_layer: L0|L1|L2|L3|L4|L5
environment_identity: string
source_commit: string|TOKEN_VAZIO
run_or_receipt_id: string
exit_code: integer|TOKEN_VAZIO
artifacts_hash: map|TOKEN_VAZIO
claim_allowed: false|true
```

Ausência de um campo não é preenchida por inferência. Deve ser registrada como `TOKEN_VAZIO`.

## 3. O que L0 pode fazer

O GPT Project Workflow Layout pode:

- organizar fontes e dependências;
- definir contratos, gates e estados;
- decidir onde um artefato deve residir;
- acionar conectores disponíveis;
- produzir documentação, código e testes;
- comparar receipts e detectar incoerências;
- preservar memória longitudinal.

L0 não prova, por si só:

- execução física no Android;
- sucesso de GitHub Actions;
- equivalência entre runners;
- replicação independente;
- validade científica externa.

## 4. Aplicação ao estado atual

```yaml
project_context_and_orchestration:
  executor_layer: L0
  status: ACTIVE

github_and_drive_writes:
  executor_layer: L1
  status: OBSERVED_SUCCESS_WHERE_CONNECTOR_RETURNED_SUCCESS

local_python_tests:
  executor_layer: L2
  status: PASS_BY_LOCAL_RECEIPTS

github_actions:
  executor_layer: L3
  status: QUEUED_OR_REMOTE_GATE_BLOCKED_DEPENDING_ON_HEAD

termux_android:
  executor_layer: L4
  status: TOKEN_VAZIO

independent_replication:
  executor_layer: L5
  status: TOKEN_VAZIO
```

## 5. Regra contra mistura de camadas

\[
\text{L0 planejamento}
\neq
\text{L2 execução local}
\neq
\text{L3 CI remoto}
\neq
\text{L4 runtime físico}
\neq
\text{L5 replicação independente}.
\]

A passagem de uma camada para outra exige receipt próprio.

## 6. Fechamento

O “workflow layout do GPT” funciona como **plano de controle cognitivo-operacional**. Ele pode coordenar execuções reais, mas cada execução conserva sua autoridade e seu ambiente de origem.

```yaml
F_ok: contexto do projeto e conectores ativos
F_gap: Termux físico e replicação independente
F_next: anexar executor_layer a todos os próximos receipts e PRs
```
