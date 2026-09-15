# SEED Ω EVOLUTION V1 — índice canônico

**Data:** 2026-09-15
**Estado:** `CANONICAL_DRAFT`
**claim_allowed:** `false`

## Objetivo

Registrar um modelo de seeds evolutivas como grafo genealógico append-only, com cultivos computacionais isolados, operadores tipados, recombinação explícita e seleção multidimensional.

## Antecedentes preservados

- `schemas/multimodal-cave-seed.v1.schema.json`: infraestrutura de seed já existente.
- `data/formulas/SESSION_FORMULA_REGISTRY_53_V1.json`: F01 fixa `q=sqrt(3)/2`; F43 estado evolutivo; F45 evolução append-only; F47 tensor relacional; F51 parada por invariante; F53 limites epistemológicos.
- `papers/research_notes/2026-08-31_ATLAS_X_SQRT3_PI_PHI_F4.md`: contração Euclidiana por `sqrt(3)/2` não implica geodésica hiperbólica.

## Invariantes

1. `sqrt(3/2) != sqrt(3)/2`.
2. `ANTIDERIVATIVE != UNIQUE_INVERSE`.
3. `REVERSE != INVERSE`.
4. `EUCLIDEAN_SCALE != HYPERBOLIC_GEODESIC` sem métrica/manifold explícitos.
5. `POSSIBILITY != EVIDENCE`.
6. `GENOTYPE_ANALOGY != BIOLOGICAL_DNA`.
7. `PLASTICITY_ANALOGY != WATER_IDENTITY`.
8. `ANCESTOR_PRESERVED=true`.
9. `CLAIM_ALLOWED=false` até execução e evidência.

## Operadores

`DIRECT | INVERSE | REVERSE | ANTIDERIVATIVE | RECLUSIVE_CLOSURE | LOG | ITERATED_LOG | TANGENTIAL | ORTHOGONAL | TRANSVERSAL | LATERAL | RECURSIVE | RECOMBINE | PERMUTE | GEODESIC_STEP`

## Escala

`q = sqrt(3)/2`

`a_n = a_0 q^n`

`h_n = a_0 q^(n+1)` para triângulo equilátero quando `a_n` é o lado.

A razão é um operador de escala geométrica. O passo `GEODESIC_STEP` exige manifold, métrica e mapa exponencial definidos.

## Seleção

Não existe vencedor universal. O estado recomendado é uma fronteira de Pareto sobre:

`coherence, novelty, reconstruction, evidence, robustness, cost`.

## Rotas

- Mapa: schema, ontologia, lineage e índice.
- papers: síntese metodológica e claims.
- RLL: contrato científico/modelo falsificável.
- RafPolimata: produtor futuro do simulador e receipts; não implementado neste delta.

## R3

**F_ok:** contrato canônico de seed evolutiva definido e ligado aos antecedentes.
**F_gap:** operador algébrico fechado, simulador, benchmark e reprodução independente = `TOKEN_VAZIO`.
**F_next:** implementar produtor finito determinístico no RafPolimata e validar cada geração por replay.


## Refinamento — in vitro como banco quiescente e retrocruza

A linhagem não é modelada como sequência linear. A topologia canônica é:

`TEMPORAL_TYPED_HYPERGRAPH`

com hiperarcos multi-pais para recombinação e retrocruza.

Cada "tubo" é uma seed/linhagem em estado de atividade reduzida:

`QUIESCENT != DELETED`

`HIDDEN_IN_PROJECTION != ABSENT_FROM_GRAPH`

O banco preserva conexões, integrações, relações, interconexões, anomalias, paradoxos, formulações, contradições, evidências e heurísticas.

Exemplo de relação derivável latente:

`equilateral side a -> altitude h=(sqrt(3)/2)*a`.

A altura pode não estar explícita na visualização inicial, mas é recuperável pela estrutura geométrica.

### Retrocruza / backcross

Se uma linhagem atual perdeu uma característica útil preservada no ancestral `A_k`:

`S_(n+1)=B(S_n,A_k;trait_mask)`.

A operação é multi-parent e cria um novo descendente. O ancestral não é sobrescrito e a característica não é "ressuscitada por memória vaga": o `trait_mask`, os pais e a transformação devem ficar registrados.

### Ruído prática ↔ teoria

Defina apenas o residual:

`Delta_PT=d(practice_observation,theory_prediction)`.

Inicialmente:

`owner(Delta_PT)=TOKEN_VAZIO_RESIDUAL_OWNER`.

Não se decide a priori que a prática é ruído nem que a teoria é ruído. O residual pode depois ser classificado como erro de medição, misspecification, discretização, estrutura não modelada, gap de implementação, anomalia, contradição ou efeito ainda não explicado.

### Operadores acrescentados

`INDIRECT | DERIVATIVE | BACKCROSS | QUIESCE | REACTIVATE | LATENT_RELATION_PROBE | NOISE_RECLASSIFY`.

