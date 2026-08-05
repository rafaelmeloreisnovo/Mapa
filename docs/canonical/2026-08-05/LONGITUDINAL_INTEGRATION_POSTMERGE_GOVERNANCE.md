# Memória longitudinal — governança pós-merge da PR #151

- **Data observada:** `2026-08-05T13:27:35-03:00`
- **Repositório:** `rafaelmeloreisnovo/Mapa`
- **PR de origem:** `#151`
- **Head mesclado:** `91c836e5a566d34f908f614d46e5cc377dd3b9e2`
- **Merge commit:** `f5fa5e0c8532dbdd36bfaf6918e89c65f6997ba4`
- **Event ID:** `sha256:ce109e5d703a96ef8429bb5fca43e6896927d08d27f2a63e8baf6394c51a47c9`
- **Claim permitido:** `false`

## Estado declarado antes do merge

A PR #151 registrava explicitamente:

```text
draft=true
automatic_merge=false
human_review_required=true
promotion=DENIED_WHILE_BLOCKERS_EXIST
```

Também permaneciam abertos:

- `48` lotes de conversas;
- `21` lotes Codex;
- assets, `img/` e `chat.html`;
- CI com steps/logs observáveis;
- Termux ARMv7/ARM64 e Android físico;
- hashes cross-surface;
- rotação de credencial e secret scan;
- reprodução independente.

## Estado observado

```text
merged=true
draft=false
merged_at=2026-08-05T16:27:35Z
```

Classificação:

```text
GOVERNANCE_DIVERGENCE_MERGED_DESPITE_DECLARED_DRAFT
actor_or_trigger=TOKEN_VAZIO_NOT_ESTABLISHED
```

A ausência de receipt administrativo impede atribuir o merge a pessoa, bot, regra de branch ou automação específica.

## Custódia preservada

Os artefatos de integração foram confirmados na `main` após o merge:

- `indices/catalog-runs/deltas/LONGITUDINAL_INTEGRATION_FGAP_FNEXT_2026-08-05.md`;
- `data/catalog_runs/RAFAELIA_LONGITUDINAL_INTEGRATION_FGAP_FNEXT_2026-08-05.json`;
- `data/catalog_runs/RAFAELIA_LONGITUDINAL_INTEGRATION_CI_OBSERVATION_2026-08-05.json`.

Eventos predecessores:

- integração: `sha256:d5dcc113a61cf0c737b98dce76369b5c1c887b41abc56229eba0fc5a99f872a7`;
- CI: `sha256:56b693cf9e8cab9efbacf8941860c00aa8f0d1c9562f1218c7c93c2b9d310d6b`.

## F_ok

- memória `000 → 002` integrada ao índice-mestre;
- relação com GAIA/RMR tipada sem identidade automática;
- conteúdo privado não foi publicado;
- divergência de governança registrada sem apagar o histórico;
- rollback definido somente por evento compensatório.

## F_gap

- ator ou gatilho do merge: `TOKEN_VAZIO_NOT_ESTABLISHED`;
- teste negativo executável do controle de promoção: `TOKEN_VAZIO`;
- receipt administrativo ligado à decisão de merge: `TOKEN_VAZIO`;
- CI do merge commit com steps/logs observáveis: `TOKEN_VAZIO`;
- todos os blockers técnicos e de cobertura anteriores continuam abertos.

## F_next

1. Manter este delta em PR draft.
2. Observar workflows do merge commit sem correção especulativa.
3. Implementar teste negativo: uma PR com `automatic_merge=false`, `human_review_required=true` ou `TOKEN_VAZIO` bloqueante deve ter promoção negada.
4. Registrar receipt administrativo ou manter causalidade como `TOKEN_VAZIO`.
5. Continuar pelo cursor privado `conversations-003.json` em branch separada.
6. Emitir novo receipt pós-merge somente quando houver revisão humana e SHA final verificados.

## Decisão

O merge prova persistência na `main`; não prova revisão humana, fechamento de gates, validade de claims, runtime físico ou cobertura integral.

```text
claim_allowed=false
promotion=DENIED
retroactive_rewrite=false
rollback=COMPENSATING_EVENT_ONLY
```
