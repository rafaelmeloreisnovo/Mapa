# RAFAELIA — Continuous Draft Execution Ledger V1

**Estado:** ACTIVE_APPEND_ONLY
**Branch:** `main_01_readme-universe-layer1`
**Escopo:** registrar continuamente cada descoberta, leitura, classificação, gap, decisão e próximo gate enquanto a arquitetura é construída.
**claim_allowed:** false

## Regra operacional

Nenhum lote precisa esperar conclusão total para ser materializado. Cada passo verificável gera um rascunho versionado com:

- `event_id`
- timestamp UTC e America/Sao_Paulo
- fonte consultada
- objeto afetado
- estado anterior
- novo estado
- evidência disponível
- risco
- privacidade
- autoridade
- dependências
- `F_ok`
- `F_gap`
- `F_next`

## Estados de rascunho

```text
DISCOVERED
QUEUED
READING
READ_PARTIAL
READ_COMPLETE
CLASSIFIED
CROSSCHECK_PENDING
CONFLICT_FOUND
AUTHORIZATION_REQUIRED
READY_FOR_REVIEW
SUPERSEDED
ARCHIVED_REFERENCE
```

## Política de escrita contínua

1. Descoberta nova entra imediatamente no ledger.
2. Leitura parcial é registrada como parcial; não espera interpretação completa.
3. Correção não apaga evento anterior; cria sucessor.
4. Mudança de autoridade, privacidade, workflow, release ou publicação exige gate específico.
5. Índices derivados podem evoluir por commits pequenos e reversíveis.
6. Arquivos produtores não são alterados silenciosamente.
7. Ausência de acesso vira `TOKEN_VAZIO_ACCESS`, não inexistência.

## Evento inicial

```yaml
event_id: DRAFT-LEDGER-INIT-20260801
source: session_instruction
object: universal_indexing_architecture
previous_state: batch_oriented_materialization
new_state: continuous_draft_materialization
authority: Mapa/control-plane
privacy: no_private_payload
risk: low
F_ok: ledger contínuo criado
F_gap: eventos anteriores ainda precisam ser retroindexados
F_next: registrar cada leitura e alteração futura como evento incremental
claim_allowed: false
```

## Retroindexação necessária

Devem ser convertidos em eventos separados, sem reescrever a história:

- criação da branch `main_01_readme-universe-layer1`;
- criação do PR `Mapa #117`;
- leitura de `Mapa`, `RafGitTools` e `RafPolimata`;
- criação do mapa documental;
- criação do protocolo universal;
- descoberta de `AGENTS.md`, `CLAUDE.md`, `BUILD.md`, `CHANGELOG.md` e demais entradas;
- correção de escopo de “tema Markdown” para indexação universal.

## F_next

Alimentar também `continuous_draft_events.v1.jsonl` a cada passo verificável e espelhar sínteses no documento longitudinal do Drive.
