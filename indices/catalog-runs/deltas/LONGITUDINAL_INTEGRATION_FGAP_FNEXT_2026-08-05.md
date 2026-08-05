# Integração longitudinal — F_gap → F_next — 2026-08-05

- **Modo:** `INCREMENTAL_APPEND_ONLY_FAIL_CLOSED`
- **Autoridade:** `rafaelmeloreisnovo/Mapa`
- **Espinha de integração:** PR `#151`
- **Execução catalogada relacionada:** PR `#150`
- **Índice-mestre:** `indices/RAFAELIA_IMPLEMENTACAO_LATENTES_PAPERS_V1.md`
- **Claim permitido:** `false`
- **Privacidade:** `PUBLIC_SANITIZED_POINTERS_ONLY`
- **Event ID:** `sha256:d5dcc113a61cf0c737b98dce76369b5c1c887b41abc56229eba0fc5a99f872a7`

## Decisão de integração

A PR `#151` permanece como espinha da memória longitudinal porque contém a cadeia sanitizada e navegável do `NOVOexport` (`conversations-000 → 001 → 002`).

A PR `#150` entra como **execução catalogada relacionada**, não como fonte de identidade nem como autoridade concorrente. Sua relação é tipada:

```text
NOVOEXPORT_MEMORY_000_002
  --SUPPLIES_SANITIZED_LONGITUDINAL_CONTEXT-->
GAIA_RMR_FGAP_FNEXT
  --CATALOGED_EXECUTION_DELTA-->
RAFAELIA_IMPLEMENTACAO_LATENTES_PAPERS_V1
```

Similaridade semântica não cria identidade. Dois objetos somente podem ser tratados como o mesmo corpo quando houver identidade física demonstrada por revisão e hash de conteúdo.

## F_ok integrado

- `conversations-000` a `conversations-002` estão catalogados como `300` conversas e `20.059` IDs únicos de mensagens;
- sete envelopes privados foram registrados na origem como recuperados e comparados byte a byte;
- o ciclo GAIA/RMR registrou gate local `10/10 PASS`;
- os deltas públicos não expõem IDs do Drive, títulos de conversas, corpos de mensagens, nomes de assets ou URLs privadas;
- `claim_allowed=false`, `automatic_merge=false` e `destructive_actions=false` permanecem invariantes;
- a integração usa ponteiros, estados e relações tipadas, sem copiar corpos privados entre superfícies.

## F_gap consolidado

| ID | Estado | Condição de fechamento |
|---|---|---|
| `G-LONG-001` | `TOKEN_VAZIO_NEXT_CURSOR` | catalogar privadamente `conversations-003.json` |
| `G-LONG-002` | `48_LOTS_PENDING` | fechar os lotes de conversa restantes por deltas incrementais |
| `G-LONG-003` | `21_CODEX_LOTS_PENDING` | inventário e ingestão Codex com custódia separada |
| `G-LONG-004` | `TOKEN_VAZIO_ASSETS` | reconciliar manifest de assets, `img/` e `chat.html` |
| `G-LONG-005` | `TOKEN_VAZIO_CROSS_SURFACE_HASH` | hash byte a byte do mesmo corpo entre superfícies |
| `G-LONG-006` | `TOKEN_VAZIO_OBSERVABLE_CI` | jobs com steps e logs recuperáveis |
| `G-LONG-007` | `TOKEN_VAZIO_PHYSICAL_RUNTIME` | receipts Termux ARMv7/ARM64 e Android físico |
| `G-LONG-008` | `TOKEN_VAZIO_FULL_COVERAGE` | inventário paginado Drive, Library e GitHub |
| `G-LONG-009` | `TOKEN_VAZIO_SECRET_CLOSURE` | rotação de credencial, secret scan e receipt de encerramento |
| `G-LONG-010` | `TOKEN_VAZIO_REPLICATION` | reprodução independente dos hashes, contagens e gates |

## F_next executável

1. Manter a PR `#151` em draft como espinha de integração.
2. Catalogar `conversations-003.json` somente na superfície privada.
3. Gerar os dois índices do lote `003` e testar recuperação integral.
4. Reconciliar `conversations-002 ↔ conversations-003`.
5. Materializar a custódia anonimizada do lote `000` como delta separado.
6. Publicar apenas o agregado sanitizado sucessor.
7. Observar CI; falhas sem steps/logs continuam `TOKEN_VAZIO_RUNNER_OR_STARTUP`, não defeito de código estabelecido.
8. Produzir receipts físicos Termux antes de qualquer promoção de runtime.
9. Mesclar somente após revisão humana e emitir receipt pós-merge ligado ao SHA final da `main`.

## Gate de promoção

```text
promotion = DENIED
while (
  TOKEN_VAZIO bloqueante
  or human_review_required
  or observable_ci != PASS
  or physical_runtime_receipt == TOKEN_VAZIO
)
```

Nenhum merge, presença de arquivo, similaridade de conteúdo ou teste local isolado promove claim científico, técnico ou operacional.

## Registro estruturado

`data/catalog_runs/RAFAELIA_LONGITUDINAL_INTEGRATION_FGAP_FNEXT_2026-08-05.json`

## R₃

- `F_ok`: memória sanitizada, execução GAIA/RMR e índice-mestre conectados por arestas tipadas.
- `F_gap`: cobertura integral, CI observável, runtime físico, hashes cruzados, segredo encerrado e reprodução permanecem abertos.
- `F_next`: avançar pelo cursor `conversations-003`, emitir receipts e preservar a cadeia append-only.
