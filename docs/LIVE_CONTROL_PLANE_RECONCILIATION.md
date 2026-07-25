# Mapa — Reconciliação do Control Plane Vivo

Status: `VERIFIED_LIMITED_LOCAL`  
Data de observação: `2026-07-25`  
Branch de implementação: `codex/live-control-plane-reconciliation-v1`  
Claim global: `claim_allowed=false`

## 1. Problema corrigido

O repositório já possuía contratos, fixtures, workflows, ontologia, cadeia de custódia e triagem. Entretanto, quatro superfícies divergiam:

1. a página inicial ainda descrevia principalmente o KOS biblioteconômico;
2. fixtures de contratos podiam ser confundidas com estado operacional corrente;
3. o ledger de procedimentos ainda preservava a PR #51 como draft, embora #51, #52 e #54 já estivessem mescladas;
4. evidências de outros repositórios apareciam como caminhos soltos, sem repositório, commit imutável e limite explícito.

A correção não reescreve o histórico. Ela adiciona uma camada observacional separada:

```text
contrato/fixture histórico
        ↓
observação datada
        ↓
registro vivo
        ↓
validador
        ↓
relatório
        ↓
próximo evento append-only
```

## 2. Invariantes

```text
fixture != estado vivo
merge != remote gate PASS
caminho local != evidência cross-repository
VERIFIED exige evidência resolvível
TOKEN_VAZIO não pode ser promovido silenciosamente
produto draft não vira capacidade da branch principal
claim_allowed permanece false
```

## 3. Registros vivos

| Arquivo | Responsabilidade |
|---|---|
| `data/control-plane/current_state_snapshot.v1.json` | snapshot datado, métricas e estados globais |
| `data/control-plane/module_registry.v1.json` | módulos observados, commits, capacidades e gaps |
| `data/control-plane/product_graph.v1.json` | produtos, produtores, relações e fronteiras |
| `data/control-plane/evidence_pointer_registry.v1.json` | ponte tipada para arquivos, commits, PRs e comentários |
| `data/control-plane/merge_decisions.v1.json` | decisões limitadas dos merges #51, #52 e #54 |
| `data/control-plane/procedure_state.v1.json` | projeção temporal sem alterar a fixture histórica |

`orquestrador/fixtures/` continua destinado a testes de contrato. Nenhum registro vivo aponta para esse diretório como fonte de estado atual.

## 4. Reconciliação dos merges

As PRs #51, #52 e #54 foram mescladas com evidência local registrada e sem passos remotos observáveis. A decisão é preservada como:

```yaml
observed_state: MERGED_WITH_LIMITED_EVIDENCE
local_validation: PASS_RECORDED
remote_validation: TOKEN_VAZIO_RUNNER
human_override: true
decision_type: HUMAN_OVERRIDE_LIMITED
claim_promotion: false
```

Isso não desfaz os merges e não inventa que a Actions passou. Uma futura execução remota deve gerar nova evidência, sem reescrever estas decisões.

## 5. Evidência cross-repository

Uma referência externa deve declarar no mínimo:

```yaml
provider: github
repository: owner/repository
kind: file | commit | pull_request | issue_comment
ref: immutable_commit_sha
path: required_for_file
state: VERIFIED_LIMITED
limitations:
  - boundary of what the pointer proves
claim_allowed: false
```

Para PRs abertas, o registro também conserva `pr_number` e `pr_state`. Assim, código em draft pode ser reconhecido como implementação observada sem virar capacidade mesclada.

## 6. Estados atuais relevantes

```yaml
control_plane: VERIFIED_LIMITED
universal_doctor: PARTIAL
termux_health_bridge: VERIFIED_LIMITED_DRAFT
semantic_interpretation: TOKEN_VAZIO
remote_private_runner: TOKEN_VAZIO_RUNNER
rafmedia_png_wav_vertical: PARTIAL
```

A ponte `termux.health` possui cliente, servidor e execução local limitada, mas os dois lados continuam em PRs draft. A interpretação semântica continua bloqueada até existir redação determinística, teste de reidentificação, exclusão de fonte bruta e gate de abstinência.

## 7. Validador

Comando:

```bash
python3 scripts/validate_live_control_plane.py \
  --repo-root . \
  --write-report build/live-control-plane/report.json
```

O validador bloqueia:

- IDs duplicados;
- evidência local ausente;
- arquivo externo sem repositório, caminho e SHA imutável;
- módulo ou produto apontando para evidência inexistente;
- produto verificado sem prova;
- produto draft com produtores já promovidos ou sem PR draft;
- merge tratado como remote `PASS` sem evidência;
- `claim_promotion=true` nas decisões limitadas;
- estado vivo apontando para `fixtures`;
- divergência entre métricas do snapshot e registros;
- promoção da interpretação semântica enquanto os gates permanecem abertos.

## 8. Limites

A validação local prova coerência estrutural e semântica do pacote no checkout. Ela não prova:

- execução do GitHub Actions privado;
- disponibilidade dos repositórios externos no futuro;
- Android ARM32 ou ARM64;
- integração produtiva completa;
- validade científica de claims dos repositórios produtores.

## 9. Próximo passo verificável

```text
validar pacote no checkout real
→ anexar report.json + SHA256SUMS
→ executar primeiro Universal Doctor read-only
→ comparar observed_ref com producer HEAD
→ registrar STALE_CONSUMER, CONTRADICTION ou TOKEN_VAZIO
→ somente depois atualizar o snapshot
```

## R3

```text
F_ok   = estado vivo separado de fixture, merges reconciliados, evidência tipada, validador e testes
F_gap  = runner remoto, primeira execução federada do Doctor e gate de privacidade semântico
F_next = produzir o primeiro relatório read-only ligado a commits e ambiente
```
