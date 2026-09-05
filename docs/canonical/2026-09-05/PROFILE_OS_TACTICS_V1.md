# RAFAELIA PROFILE OS — Táticas Operacionais V1

Estado: OPERATIONAL_DRAFT / APPEND_ONLY / NO_DELETE / claim_allowed=false

## T0 — Entrada

Para cada novo objeto:
`SOURCE -> IDENTIFY -> DEDUP_CHECK -> CLASSIFY -> ROUTE -> GATE -> RECEIPT -> INDEX -> MEMORY`

Campos mínimos:
- provider
- provider_id
- title
- object_type
- parent/provider scope
- source_pointer
- epistemic_state
- claim_allowed
- relations
- F_gap
- F_next

## T1 — DEDUP

1. Se houver `provider_id`, ele governa identidade.
2. Sem `provider_id`, usar `content_hash + canonical_path`.
3. Mesmo título + IDs diferentes **não** autoriza fusão.
4. Snapshot e sucessor recebem relação tipada; ambos são preservados.
5. Delete permanece bloqueado por política desta V1.

## T2 — Estratégia versus tática

Promover para estratégia apenas:
- regra transversal;
- baixa volatilidade;
- evidência de uso recorrente;
- rollback explícito;
- baixo risco de conflito.

Manter em tática:
- procedimentos;
- roteamentos;
- checks;
- cadências;
- critérios de revisão.

Manter fora do perfil:
- hashes longos transitórios;
- status de PR;
- logs;
- resultados de execução;
- dados de billing/credenciais;
- estado específico de um único projeto.

## T3 — Drive

- `00_INDEX_E_MAPA`: contratos e mapas.
- `01_ESTRATEGIA_DO_PERFIL`: invariantes duráveis.
- `02_TATICAS_OPERACIONAIS`: procedimentos revisáveis.
- `03_CICLOS_E_RECEIPTS`: receipts append-only.
- `04_BIBLIOTECA_E_BIBLIOTECARIA`: regras de curadoria.
- `05_INVENTARIO_E_MEMORIA_LOTCP`: registry operacional.
- `06_INTEGRACOES_GMAIL_CALENDAR_GITHUB`: ponteiros provider-bound.
- `07_CIRURGIA_INSTRUCOES_PERSONALIZADAS`: mudanças candidatas/testadas.

## T4 — GitHub

Mudanças no control plane:
- branch-first;
- um commit coerente quando o delta é indivisível;
- schema + dados + validador + testes;
- PR draft;
- sem auto-merge;
- CI valida invariantes, não promove claim.

## T5 — Gmail e Calendar

- Gmail: somente sinais explicitamente pertinentes; label-first; nada de bulk indiscriminado.
- Calendar: revisão semanal aponta para o Drive; não replica memória.
- Ausência de mensagens/eventos adicionais não é interpretada como ausência de trabalho.

## T6 — TOKEN_VAZIO / F_GAP / F_NEXT

Todo gap deve registrar:
`id, state, reason, source_pointer, evidence_needed, next_probe, urgency, claim_allowed`

Estados desconhecidos continuam desconhecidos até readback/teste.

## T7 — Não regressão

Falhar fechado se:
- `claim_allowed=true` aparecer no registry V1;
- `delete_policy != NO_DELETE`;
- houver `provider_id` duplicado para objetos distintos;
- supersessão apontar para o próprio objeto;
- TOKEN_VAZIO for convertido em zero;
- relação de dedup apagar ancestral sem receipt.

## Resultado esperado

PROFILE_OS deixa de ser apenas uma árvore e passa a ser um contrato verificável, versionado e reproduzível.

`claim_allowed=false`
