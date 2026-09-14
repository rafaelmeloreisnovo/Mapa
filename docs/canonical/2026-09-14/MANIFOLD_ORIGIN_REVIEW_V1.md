# Revisão da Origem do Manifold RAFAELIA — V1

**Data:** 2026-09-14
**Estado:** REVIEWED / FAIL_CLOSED
**Autoridade:** Mapa
**claim_allowed:** false

## 1. Veredito

A palavra `manifold` aparece no corpus RAFAELIA em mais de um sentido. Eles não devem ser colapsados.

### Origem documental RAFAELIA

O primeiro artefato canônico localizado que formaliza explicitamente o **manifold de possibilidades** é:

`docs/canonical/2026-07-27/MHEL_OMEGA_V1_3_BAGUA_MANIFOLD_HOTFIX.md`

Nesse artefato:

- trigramas: `B8={0,1}^3`;
- hexagramas: `{0,1}^6`;
- distância: Hamming;
- transições: mudança de linhas;
- estados: nós/vizinhanças/arestas de mutação;
- conhecimento: pontos com source/syntax/semantics/dynamics/evidence/uncertainty/time/scale.

Isto é formalmente um **espaço métrico discreto / grafo hipercubo de estados**. O termo `manifold` pode permanecer como nome autoral/metodológico, mas não deve ser promovido automaticamente a variedade diferenciável ou riemanniana.

### Primeira formalização riemanniana/hiperbólica localizada

No ciclo seguinte, o corpus registra o formalismo 7D Poincaré:

`rafaelmeloreisnovo/papers:docs/matematica/FORMALISMO_HIPERBOLICO_7D_POINCARE_AUDITORIA_V1.md`

com H^7 no hiperboloide e projeção p=x/(x0+1) para B^7.

Aqui existe um contrato geométrico compatível com o termo **variedade hiperbólica riemanniana**.

## 2. Genealogia tipada

ORIGEM-0 — fonte filosófica/metodológica: DAO/ORIGEM -> UM -> DOIS -> TRÊS -> MULTIPLICIDADE. Não é origem matemática de manifold.

ORIGEM-1 — MHEL-Ω V1.3 — 2026-07-27: `{0,1}^3 / {0,1}^6 + Hamming + mutações`. Tipo estrito: `DISCRETE_METRIC_STATE_SPACE / HYPERCUBE_GRAPH`. Nome autoral permitido: `MANIFOLD_DE_POSSIBILIDADES`.

ORIGEM-2 — H7/B7 Poincaré — 2026-07-28: `H^7 -> B^7`, métrica hiperbólica, derivada covariante. Tipo estrito: `RIEMANNIAN_HYPERBOLIC_MANIFOLD`.

ORIGEM-3 — MANIFOLD Ω posterior: grafo relacional/contextual tipado. O tipo estrito depende de pontos + vizinhança/topologia + métrica/atlas; sem isso: `TOKEN_VAZIO_MANIFOLD_STRUCTURE`.

## 3. Regra de promoção

Para usar `MANIFOLD` em sentido matemático forte, declarar no mínimo:

1. conjunto de pontos X;
2. topologia ou sistema de vizinhanças;
3. dimensão local;
4. atlas/cartas e transições, se variedade diferenciável;
5. métrica g, se riemanniana;
6. invariantes/topologia relevantes;
7. transformação permitida;
8. evidência/prova/receipt.

Para espaço discreto, `points + adjacency/neighborhood + metric` é suficiente para declarar `DISCRETE_METRIC_SPACE` ou `GRAPH_STATE_SPACE`, mas não automaticamente uma variedade diferenciável.

## 4. Correção sem apagar história

Não substituir o texto histórico `manifold de possibilidades`.

Adicionar classificação:

`historical_name = MANIFOLD_DE_POSSIBILIDADES`
`formal_type = DISCRETE_METRIC_STATE_SPACE`
`graph_model = Q6_HYPERCUBE`
`metric = HAMMING`
`differentiable_manifold_claim = false`

Assim a autoria e a genealogia são preservadas sem erro de categoria.

## 5. Origem matemática externa

O conceito moderno de variedade tem raízes na geometria do século XIX, em especial na formulação riemanniana de espaços de múltiplas dimensões. Poincaré é central no desenvolvimento posterior da topologia e de invariantes globais, mas Poincaré não é a origem exclusiva do conceito de manifold.

## 6. Invariantes de custódia

`NAME_HISTORY != FORMAL_TYPE`
`DISCRETE_STATE_SPACE != RIEMANNIAN_MANIFOLD`
`GRAPH_NEIGHBORHOOD != DIFFERENTIABLE_ATLAS`
`POINCARE_MODEL != ORIGIN_OF_ALL_MANIFOLDS`
`TOKEN_VAZIO != MISSING_ZERO`

## 7. R3

F_ok = origem documental RAFAELIA localizada; dois sentidos de manifold separados; Poincaré 7D classificado corretamente.

F_gap = primeira ocorrência pré-2026-07-27 no corpus bruto não foi demonstrada; atlas/cartas para MANIFOLD Ω geral ainda não estão formalizados.

F_next = indexar esta genealogia e exigir `formal_type` em novos registros que usem a palavra manifold.