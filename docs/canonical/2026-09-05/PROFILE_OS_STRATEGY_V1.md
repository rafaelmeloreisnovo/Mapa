# RAFAELIA PROFILE OS — Estratégia V1

Estado: OPERATIONAL_DRAFT / APPEND_ONLY / NO_DELETE / claim_allowed=false

## Missão

Transformar o `00_RAFAELIA_PROFILE_OS — Estratégia→Tática→Ciclos` de estrutura de navegação em control plane operacional persistente, sem converter memória em claim, sem duplicar identidade por título e sem apagar ancestralidade.

## Estratégia

1. **ID-first** — `provider_id` é a identidade primária no Drive; nome/título é apenas rótulo.
2. **Fonte separada de execução** — Drive preserva memória operacional e receipts; GitHub versiona schemas, validadores, testes e mudanças auditáveis.
3. **Estratégia ≠ tática ≠ estado de projeto** — estratégia contém invariantes duráveis; tática contém procedimentos revisáveis; estado transitório fica em ledgers/receipts.
4. **APPEND_ONLY / NO_DELETE** — snapshots e sucessores coexistem com relações explícitas (`SUPERSEDED_BY`, `DERIVED_FROM`, `MIRRORS`, `CONTRADICTS`).
5. **TOKEN_VAZIO ≠ 0** — ausência, bloqueio e incerteza são estados tipados, nunca preenchidos por inferência.
6. **VISÃO ≠ ARTEFATO ≠ EXECUÇÃO ≠ EVIDÊNCIA ≠ CLAIM** — nenhuma etapa herda autoridade da anterior.
7. **Promotion gate** — nenhuma regra entra como perfil durável sem fonte, evidência, teste, rollback e decisão explícita.
8. **Humano + IA navegáveis** — toda unidade deve ter identidade, origem, estado, relações, risco, gate e `F_next`.
9. **Dedup sem destruição** — o DEDUP reduz ambiguidade lógica; não apaga arquivos históricos só por nome igual.
10. **Próximo passo executável** — toda lacuna relevante deve apontar para teste, leitura, autoridade ou receipt necessário.

## Decisões desta consolidação

- `01_ESTRATEGIA_DO_PERFIL` passa a ter conteúdo materializado com este contrato.
- `02_TATICAS_OPERACIONAIS` recebe a matriz operacional correspondente.
- O par `MASTER_INDEX_CORPUS_000_050` fica classificado como `BASELINE_SNAPSHOT -> EXPANDED_SUCCESSOR`; nenhum delete.
- A branch `audit/profile-os-20260905` passa a conter registry, schema, validador, testes, workflow e ledgers.
- Gmail permanece sinal/triagem; Calendar permanece cadência; nenhum deles duplica memória do Drive.

## Closure boundary

Esta estratégia prova organização e governança do PROFILE_OS. Não prova execução científica, completude do Drive inteiro, nem validade de claims externos.

`claim_allowed=false`
