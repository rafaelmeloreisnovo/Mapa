# RAFAELIA — F_GAP / F_NEXT — Índice Federado de Trânsito V1

**Data:** 2026-08-19  
**Estado:** `CANONICAL_DRAFT / APPEND_ONLY / claim_allowed=false`  
**Autoridade federada:** `rafaelmeloreisnovo/Mapa`  
**Contrato máquina:** `data/control-plane/RAFAELIA_FEDERATED_WORK_SERVICE_CONTRACT.v1.json`

## 0. Regra-mãe

O trabalho não é uma lista solta de pendências. Cada unidade deve ser reconstruível como:

```text
W = <IDENTIDADE, AUTORIDADE, FRONTEIRA, ÍNDICES, ROTA, GAP, EVIDÊNCIA,
     GOVERNANÇA, DADOS, PRIVACIDADE, SEGURANÇA, URGÊNCIA, RISCO,
     DEPENDÊNCIAS, GATE, FALSIFICADOR, EXIT, STOP, RECEIPT, F_NEXT>
```

`TOKEN_VAZIO` é estado válido. Ausência de evidência não vira `false`, `0`, `PASS` ou `RESOLVED`.

## 1. Perguntas obrigatórias de entrada

Antes de executar qualquer mutação ou promover qualquer estado, responder de forma verificável:

1. **Quem sou?** — papel do agente e papel do repositório.
2. **Qual repo/ref/path/hash estou lendo?** — identidade exata do objeto.
3. **Qual minha autoridade?** — local, federada e escopo de escrita.
4. **Qual minha fronteira?** — claims permitidos/proibidos e `claim_allowed`.
5. **Quais índices locais devo abrir?** — conjunto mínimo e justificativa.
6. **Qual rota do Mapa corresponde ao objetivo?** — rota, âncoras e condição de parada.
7. **Que lacunas já existem?** — gaps, `TOKEN_VAZIO`, incertezas e dependências.
8. **Qual evidência é atual?** — commit/artifact/device/protocol/receipt e estado de obsolescência.
9. **Qual gate posso executar?** — gate, falsificador, exit criterion e rollback quando aplicável.
10. **Quando devo parar?** — ausência de ganho marginal, bloqueio, saída observada ou fronteira de autoridade.
11. **Onde registro o delta?** — receipt local, transição no Mapa e memória no Drive quando material.
12. **Quais regras de governança/dados/privacidade/segurança governam a unidade?**

## 2. Trânsito canônico

```text
QUERY / GOAL
  ↓
MINIMUM RECONSTRUCTION
  ↓
IDENTITY BINDING
  ↓
AUTHORITY + BOUNDARY
  ↓
LOCAL INDICES
  ↓
MAPA ROUTE
  ↓
EXISTING F_GAP / TOKEN_VAZIO / UNCERTAINTY
  ↓
GOVERNANCE + DATA + PRIVACY + SECURITY CLASSIFICATION
  ↓
URGENCY + RISK + DEPENDENCY ORDER
  ↓
HIGHEST-UNLOCK VERIFIABLE GATE
  ↓
BASELINE + ROLLBACK
  ↓
BOUNDED EXECUTION
  ↓
LOCAL VERIFICATION
  ↓
CROSS-REPO EDGE VERIFICATION, WHEN CLAIMED
  ↓
RECEIPT
  ↓
APPEND-ONLY TRANSITION
  ↓
DRIVE RECONSTRUCTION DELTA, WHEN MATERIAL
  ↓
RECOMPUTE F_ok / F_gap / F_next
```

## 3. Papéis

```text
MAPA
= autoridade federada + roteamento + estado + relações + gaps + claim boundary

RafGitTools
= executor/control-plane/tool-router + seleção determinística + validadores + ledgers

AGENTS.md
= adaptador de entrada local do produtor; não substitui autoridade/evidência

Google Drive
= memória longitudinal + transversal + ortogonal + reconstrução editorial

repo produtor
= autoridade de implementação/teste/runtime daquele domínio

receipt
= ponte de evidência entre execução, transição, proveniência e reconstrução
```

## 4. Eixos não compensatórios

Cada trabalho deve ser classificado, separadamente, em:

- **Epistêmico:** estado, incerteza, falsificador, evidência e claim gate.
- **Operacional:** urgência, risco, owner, dependências, ação, exit, stop e rollback.
- **Proveniência:** provider, repo, ref, commit, path, hash/receipt e timestamp.
- **Governança:** autoridade, aprovação, mutação, supersessão e decisão.
- **Dados:** categoria, schema/contrato, identidade de entrada/saída, retenção e descarte/supersessão.
- **Privacidade:** classificação, minimização, PII/sensível, papéis de acesso, redação e transferência cross-provider.
- **Segurança:** ameaça/modo de falha, secrets, integridade, autenticidade, fail-closed, incidente/rollback.
- **Reconstrução:** índices, rota Mapa, âncora Drive, relações, predecessor e sucessor/F_next.

Uma dimensão crítica falha **não** pode ser escondida pela média das outras.

## 5. Prioridade

A prioridade ordena execução, não verdade.

```text
P0 segurança / privacidade / dados / governança / perda / rollback / bloqueio de execução
  ↓
dependência upstream
  ↓
READY_TO_TEST com falsificador observável
  ↓
bloqueio cross-repo com maior raio de impacto
  ↓
dívida local não crítica
```

Pesos numéricos permanecem `TOKEN_VAZIO_PRIORITY_WEIGHT_CALIBRATION` até calibração demonstrável.

## 6. Estado atual — conjunto mínimo reconstruído

### P0 — Mapa / federação HMAC + proveniência

- Autoridade: `Mapa/federated-receipt-broker`.
- Estado: `NEAR_MISS`; impacto externo consumado não observado.
- Gap: assinatura/proveniência podem ser descritas como validadas sem prova terminal HMAC/cross-repo.
- Exit: fixture HMAC errada + proveniência quebrada rejeitadas fail-closed; fixture correta passa com logs/receipt.
- Fonte: `data/routing/operational-gaps/federated-broker-hmac-provenance-gap-20260819.v1.json`.

### P0 — RafGitTools / gap ledger corrente

Fonte canônica operacional: `RafGitTools/data/evidence/github/cross-repo-gap-closure-20260819.v1.json`.

Preserva, entre outros, os seguintes itens ainda não globalmente fechados no snapshot observado:

- snapshot runtime corrente do RafGitTools;
- E2E físico Vectra↔Termux;
- blockers de `missing_reference` do Source Gap Audit;
- contrato estático Provider V3 Termux↔Vectra;
- gaps de handoff `termux-packages`;
- avaliação adversarial ONES V3.

O estado de cada item deve ser relido na fonte corrente antes de executar; este índice não congela o estado temporal do produtor.

### P0/P1 — produtor Android / Vectra

`CI/dispatch/source` não substitui receipt físico. A topologia discovery-v2/execution-v3 é uma evidência de contrato; execução QEMU, exit, guest boot e desempenho são claims separados.

### P1 — package factory

Build receipt, install receipt e runtime receipt são objetos distintos. Handoffs operacionais devem possuir schema, producer/consumer validation, hashes e semântica de erro fail-closed.

### P2 — governed retrieval

Ranking/retrieval/embedding não são verdade semântica. ONES V3 só pode promover claim bounded após gold set, negatives, privacy gate, métricas, falhas e hashes.

## 7. Condições de parada

Pare e emita receipt quando:

- o objetivo já é reconstruível e abrir mais história não altera gate/evidência/contradição/proveniência/autoridade/privacidade/segurança;
- uma dependência obrigatória está ausente;
- falta autoridade para a próxima mutação;
- privacy/security/governance gate falha;
- o exit criterion foi observado;
- a próxima etapa pertence a outro produtor/autoridade.

Parar não significa concluir o universo. Significa fechar a unidade observável e preservar `F_next`.

## 8. Receipt mínimo

```text
event_id
parent_event_id
observed_at
actor_role
repo/ref/commit/path
authority
gap_or_goal_ids
state_before/state_after
urgency/risk
governance_class
data_class
privacy_class
security_class
action
falsifier
exit_criterion
evidence_refs
F_ok
F_gap
F_next
uncertainty_delta
rollback_ref
stop_reason
claim_allowed=false unless independently promoted
```

## 9. Reconstrução

```text
Drive Master Navigation Registry
  → Drive Índice de Reconstrução Ω
  → Mapa / este índice
  → contrato máquina
  → RafGitTools agent-entry + gap ledger
  → AGENTS.md do produtor
  → repo/ref/path/hash
  → receipt/evidência
  → delta append-only
```

## 10. F₃

```text
F_ok   = contrato federado de serviço e trânsito F_gap→F_next materializado como índice + contrato máquina
F_gap  = exaustividade global, reconciliação de todos AGENTS, runtime físico, HMAC/proveniência e classificação dataset-wide permanecem bounded TOKEN_VAZIO/open
F_next = materializar executor/validador no RafGitTools, aplicar o contrato aos adaptadores AGENTS locais e emitir receipt de transição sem reescrever histórico
```
