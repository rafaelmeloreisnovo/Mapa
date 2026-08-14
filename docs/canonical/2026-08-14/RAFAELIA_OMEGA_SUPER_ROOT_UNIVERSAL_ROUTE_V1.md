# RAFAELIA Ω — Super Root + Universal Node + Context Route — V1

**Data:** 2026-08-14  
**Estado:** `VERIFIED_LIMITED_NONTERMINAL / APPEND_ONLY / claim_allowed=false`  
**Branch de materialização:** `architecture/omega-super-root-universal-route-v1-20260814`

## 1. Objetivo

Materializar o menor núcleo necessário para que uma sessão/tarefa recupere contexto sem carregar o universo inteiro e sem confundir estado histórico com estado corrente.

```text
CURRENT_TASK
  -> OMEGA_SUPER_ROOT
  -> select CONTEXT_ROUTE
  -> open minimum relevant subgraph
  -> resolve CURRENT_PROVIDER_STATE + provenance
  -> expose TOKEN_VAZIO + next_gate
  -> execute only when an evidence/operation gate requires it
  -> append-only delta
```

## 2. Decisões V1

- `fundamental_unit = typed OMEGA universal node`.
- identidade imutável fica separada de nome de exibição e localização física.
- `SUPER_ROOT` é raiz de roteamento, não alegação de cobertura completa.
- `CONTEXT_ROUTE` é read-only por padrão e abre somente o subgrafo mínimo relevante.
- snapshots históricos permanecem preservados, mas não podem ser reutilizados como estado corrente após observação mais recente do provider.
- `TOKEN_VAZIO` exige tipo, razão e `next_gate`.
- `claim_allowed=false` permanece a condição global desta V1.

## 3. Artefatos

```text
data/knowledge/RAFAELIA_OMEGA_SUPER_ROOT.v1.json
data/knowledge/RAFAELIA_OMEGA_UNIVERSAL_REGISTRY.v1.json
data/knowledge/RAFAELIA_CONTEXT_ROUTES.v1.json
data/governance/RAFAELIA_PR243_STATE_DELTA_20260814.v1.json
scripts/validate_omega_super_root_v1.py
.github/workflows/omega-super-root-v1-gate.yml
```

## 4. Mounts iniciais

A V1 monta somente âncoras de alto valor já observadas:

1. `Mapa@main` como estado GitHub corrente observado no bootstrap desta operação.
2. Drive `Master Navigation Registry V1` como índice documental.
3. `Hypothesis Index V8` como índice governado de hipóteses, explicitamente não terminal.
4. matriz de rastreabilidade Drive como estrutura de gates/procedimentos/semântica dinâmica.
5. `NOVOexport` como `RAW_SOURCE / READ_ONLY`; existência da pasta é observada, inventário recursivo completo permanece `TOKEN_VAZIO_NOVOEXPORT_FULL_INVENTORY`.

Montar não significa copiar, mover, reformatar ou canonizar os bytes da fonte.

## 5. Rotas V1

### OMEGA-ROUTE-BOOTSTRAP

Carrega somente raiz, `Mapa` corrente e Master Navigation; abre rastreabilidade/hipóteses apenas se necessário.

### OMEGA-ROUTE-HYPOTHESIS

Recupera checkpoint, identidade, evidência, falsificador e próximos gaps sem transformar a frontier em contagem global certificada.

### OMEGA-ROUTE-NOVOEXPORT-READONLY

Trata `NOVOexport` como fonte imutável. A primeira operação permitida é catálogo read-only bounded; transformação/parsing só aparece em sucessor quando solicitado e governado.

### OMEGA-ROUTE-STATE-RECONCILIATION

Separa `HISTORICAL_SNAPSHOT` de `CURRENT_PROVIDER_STATE` e preserva a relação `SUPERSEDES_WITHOUT_ERASING`.

## 6. Primeiro caso concreto de reconciliação

O Drive preserva texto histórico no qual `Mapa #243` aparecia como draft/não mesclada. A observação corrente do GitHub feita nesta operação mostra `state=closed`, `merged=true`, `draft=false`, merge commit `a0a0e6c333493d69283d399472eb3321d6fd7ebd`.

A correção não apaga nem reescreve o Drive antigo:

```text
CURRENT_PROVIDER_STATE(PR243)
  SUPERSEDES_WITHOUT_ERASING
HISTORICAL_SNAPSHOT(PR243)
```

## 7. Gate executável

O validador `scripts/validate_omega_super_root_v1.py` verifica de forma dependency-free:

- IDs de nós sem duplicação;
- referências das rotas;
- política read-only/minimum-subgraph;
- mounts resolvendo para nós conhecidos;
- `TOKEN_VAZIO` tipado e com `next_gate`;
- `claim_allowed=false`;
- separação corrente/histórica da PR #243.

A workflow `Omega Super Root V1 Gate` executa esse validador no PR. Resultado de CI só deve ser promovido depois de observado no provider; ausência de run/job/steps permanece `TOKEN_VAZIO_CI`.

## 8. O que esta V1 deliberadamente não faz

- não reorganiza Drive;
- não move `NOVOexport`;
- não modifica `rmrCti`;
- não declara inventário global completo;
- não resolve deduplicação global;
- não executa Termux/aparelho físico;
- não transforma índice/memória em evidência científica;
- não promove M3/M4 ou qualquer claim acadêmico.

## 9. Próxima fronteira

```text
P0 TOKEN_VAZIO_IDENTITY_TABLE_COMPLETE
P0 TOKEN_VAZIO_GLOBAL_TERMINALITY
P1 TOKEN_VAZIO_MOUNT_TABLE_COMPLETE
P1 TOKEN_VAZIO_NOVOEXPORT_FULL_INVENTORY
```

Ordem operacional: preencher identidade/aliases por demanda; observar CI do próprio gate; depois realizar somente inventários read-only que desbloqueiem trabalho concreto. O crescimento do root deve ocorrer por delta, nunca por importação indiscriminada.

## Retroalimentação

**F_ok:** Super Root, universal nodes, quatro rotas, reconciliação histórica/corrente e gate executável materializados em branch isolada.  
**F_gap:** CI ainda precisa ser observado; identidade/mount table não são globais; terminalidade permanece `TOKEN_VAZIO`; inventário recursivo do NOVOexport não foi executado.  
**F_next:** abrir draft PR, observar o gate, criar receipt do provider e registrar a âncora correspondente no Drive/Master Navigation sem apagar registros anteriores.
