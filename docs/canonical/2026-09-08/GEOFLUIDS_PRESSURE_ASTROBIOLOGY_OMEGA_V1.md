# Mapa — Geofluidos · Pressão · Astrobiologia · Ω — V1

**Data:** 2026-09-08  
**Tipo:** projeção temática / roteamento  
**Estado:** `CANONICAL_DRAFT · claim_allowed=false`

## Autoridade

Registro de memória de pesquisa correspondente:

```text
rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE
memory_bridge/deltas/2026-09-08_geofluids_pressure_astrobiology_omega.md
branch: memory/geofluids-omega-20260908
```

Este arquivo NÃO replica a memória integral. Ele localiza o ramo no Mapa e preserva a separação:

```text
SOURCE != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM
```

## Rota semântica

```text
WATER
 -> POLAR_SOLVENT
 -> HYDROSTATIC_COLUMN
 -> PORE_PRESSURE
 -> EFFECTIVE_STRESS
 -> FRACTURE_PERMEABILITY
 -> REACTIVE_TRANSPORT
 -> WATER_ROCK_REACTION
 -> REDOX
 -> H2 / CH4 / S / Fe / Si / metals
 -> CHEMICAL_DISEQUILIBRIUM
 -> DEEP_BIOSPHERE / ASTROBIOLOGY
```

Forçantes externas e naturais:

```text
ATMOSPHERIC_PRESSURE
ATMOSPHERIC_TIDE
EARTH_TIDE
OCEAN_TIDE_LOADING
TEMPERATURE
```

Observáveis de fusão:

```text
SEISMIC
GRAVITY
MAGNETIC
ELECTROMAGNETIC / CONDUCTIVITY
HEAT_FLOW
PORE_PRESSURE / HYDRAULIC_HEAD
GEOCHEMISTRY
MICROBIOLOGY
```

## Distinções obrigatórias

- `Mariana-MG` != `Mariana Trench`.
- cárstico != piping/sufusão != compactação/consolidação.
- estabilidade != homogeneidade.
- sinal periódico != causalidade.
- regularização de inversão != unicidade física.
- fractal visual != lei de escala.
- “plasticidade do magnetismo das informações” = metáfora de roteamento contextual, peso físico de evidência = 0.

## Operadores

```text
DIRECT      y = F(theta)+epsilon
INVERSE     theta <- y under regularization
REVERSE     adjoint/sensitivity from residual to parameter
RECURSIVE   posterior update with new observations
CONSERVE    local derivatives integrate to global budgets
LOG_LOG     scale slope + log-curvature + explicit null models
```

## Ω gates

```text
Omega0  CONSERVATION
Omega1  PHASE
Omega2  TRANSPORT
Omega3  GEOCHEMISTRY
Omega4  BIOENERGETICS
Omega5  CROSS_TELEMETRY
Omega6  SCALE
Omega7  HOLDOUT
Omega8  FORCING_ID
Omega9  INVERSE_STABILITY
Omega10 CUSTODY
```

`claim_allowed=true` só pode ser considerado para um claim específico quando os gates essenciais daquele claim forem observados como PASS.

## Fontes de ancoragem

- Lyu et al. 2026 — DOI `10.1029/2025GC012742` — porosidade/permeabilidade da crosta oceânica jovem.
- Lu et al. 2025 — DOI `10.1029/2023WR036237` — resposta de aquíferos a marés terrestres/difusão hidráulica.
- Cuthbert, Acworth & Blum 2020 — HESS 24:6033–6046 — separação de respostas a marés terrestres/atmosféricas.
- TEOS-10 — IOC/SCOR/IAPSO — equação termodinâmica oficial da água do mar.
- Shiau et al. 2022 — DOI `10.1061/(ASCE)PS.1949-1204.0000657` — colapso/instabilidade associado a ruptura de adutora.
- Boden et al. 2025 — DOI `10.1111/gbi.70016` — serpentinização/hidrotermalismo em astrobiologia.
- Nisson et al. 2026 — DOI `10.1029/2025JE009395` — H2/habitabilidade em serpentinitos como análogos planetários.

## Estado

```yaml
source_binding: PARTIAL
real_multimodal_dataset: TOKEN_VAZIO
parameter_estimation: TOKEN_VAZIO
fractal_claim: TOKEN_VAZIO
physical_information_magnetism: REJECT_LITERAL
claim_allowed: false
```

**F_ok:** rota temática e limites epistemológicos definidos.  
**F_gap:** faltam dataset sincronizado, unidades/localização/tempo e inversão observada.  
**F_next:** selecionar um sítio com pressão atmosférica + maré + head/pore pressure e ao menos uma modalidade geofísica independente, pré-registrar o holdout e rodar Ω0–Ω10.
