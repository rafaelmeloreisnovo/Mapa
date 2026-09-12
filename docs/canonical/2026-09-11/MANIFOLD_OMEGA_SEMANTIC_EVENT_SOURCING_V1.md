# RAFAELIA — MANIFOLD Ω · Semantic Event Sourcing v1

Status: DRAFT_AUDITABLE
claim_allowed=false

## Intenção
Preservar a evolução da redação, identidade e sentido de tokens ao longo de prompts, respostas de IAs, ferramentas e fontes, sem reescrever o passado.

## Núcleo
Uma identidade lexical não é o mesmo que um sentido.

`TOKEN_ID ≠ OCCURRENCE_ID ≠ SENSE_VERSION ≠ CLAIM`

Cada ocorrência nasce em um contexto. Mudanças de sentido são novos eventos append-only; correções apontam para `supersedes_event_id`; ambiguidades criam fork em vez de sobrescrita.

## μ—EVENT
O `μ—EVENT` é a menor transição semântica que merece registro. Ele referencia o conteúdo original por locator+hash, registra o ator/turno, os lexemas observados, o contexto L9 pertinente, a transição semântica e o estado de reconstrução.

O conteúdo bruto não precisa ser duplicado no ledger. Reconstrução depende de fonte acessível + cadeia ordenada de eventos + hashes.

## Álgebra mínima
- `OBSERVE(x,c)`: registra ocorrência de x no contexto c.
- `BIND(o,s_v)`: liga uma ocorrência a uma versão de sentido.
- `Δ(s_v,s_v+1)`: cria nova versão sem apagar s_v.
- `FORK(s_v,{a,b,...})`: preserva ambiguidade real.
- `SUPERSEDE(e_old,e_new)`: corrige por novo evento.
- `REPLAY(base, μ_1..μ_n)`: tenta reconstrução; resultado PASS/FAIL/TOKEN_VAZIO.
- `R(A,N)` e `R(N,A)` permanecem distintos até evidência/regra de simetria ou inversão.

## Paradoxos/anomalias
`UTOPIC_PARADOX_TAG` é somente classe editorial para uma contradição fértil/hipótese idealizada; não é prova nem classe científica por si só. Conflitos de sentido permanecem como ramos tipados: `AMBIGUITY`, `CONTRADICTION`, `ORDER_REVERSAL`, `SEMANTIC_DRIFT`.

## Expressão atual
Raw: `‡ de {'[[CADA] "›ª" 'μ[∆]]'} onde ª>ⁿ e A-N com N-A`

A sintaxe deve ser preservada exatamente no evento. `‡`, `ª`, `›` e `ª>ⁿ` permanecem `TOKEN_VAZIO_SEMANTIC`. `A-N` e `N-A` são preservados como relações orientadas candidatas, não comutativas por padrão. `μ[Δ]` é registrado como declaração autoral provisória de microevento de delta.

## Integração com contratos existentes
O envelope deve referenciar, não substituir:
- `schemas/operational-ontology.schema.json`
- `schemas/ordinal-memory-node.schema.json`
- `schemas/directive-event.schema.json`
- `schemas/feedback-event.schema.json`
- `schemas/semantic-tile.v1.schema.json`
- `Rafaelia_Private/docs/CONTEXT_RECONSTRUCTION_CONTRACT_V1.md`
- `Rafaelia_Private/results/tau_omega_registry.v1.jsonl`

## Invariantes
`SOURCE ≠ ARTEFATO ≠ EXECUÇÃO ≠ EVIDÊNCIA ≠ CLAIM`
`TOKEN_VAZIO ≠ 0`
`ordered(A,N) ≠ ordered(N,A)` salvo regra explícita.
`CORRECTION = APPEND + SUPERSEDES`, nunca apagamento.

## R3
F_ok: schema μ-event + seed dictionary especificados sobre contratos existentes.
F_gap: significado canônico de ‡, ª, › e ª>ⁿ permanece TOKEN_VAZIO_SEMANTIC; round-trip executável ainda não testado.
F_next: validar JSON Schema + JSONL, adicionar fixtures de prompt/resposta e teste de REPLAY determinístico.
