# ATLAS — PACE/El Niño × Fitoplâncton × O₂ × NO₃⁻/NO₂⁻ × Fluxo × Rhincodon × Amazônia/SAA — 2026-08-25

**Estado:** `INDEXED_RESEARCH_DELTA | APPEND_ONLY | CLAIM_ALLOWED=false`  
**Parent:** `indices/deltas/ATLAS_LUNAR_TIDES_POINCARE_BIO_COSMOS_ROUTE_20260824.md`  
**Drive delta:** `1i6L6HOk13dU9Damh37FcvJycpmik-ewTgbXPve6Wr_Y`  
**Objetivo:** incorporar a observação PACE/OCI de 2026 ao ciclo longitudinal oxigênio–nitrogênio–plâncton, mantendo `VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`.

## 0. Predecessores localizados

No corpus longitudinal do Drive foi localizado um registro anterior que já encadeava:

```text
manguezal / decomposição
→ nutrientes dissolvidos + deposição atmosférica nitrogenada
→ plâncton
→ produção de O₂ / atmosfera
```

Outra peça registra explicitamente os ciclos de carbono, oxigênio, nitrogênio e nitrito/nitrato como sistema acoplado.

Esses itens entram como `HISTORICAL_CONCEPT_SOURCE`; não recebem promoção automática a evidência experimental.

### Correção científica anti-regressão

Não transportar para frente a formulação histórica `70–80% do O₂ global`. NOAA estima que **aproximadamente metade da produção de oxigênio da Terra ocorre no oceano**, principalmente por organismos planctônicos fotossintéticos, e aproximadamente a mesma ordem é consumida pela própria vida marinha. Produção bruta diária de O₂ não é igual à contribuição líquida ao reservatório atmosférico.

Fonte: <https://oceanservice.noaa.gov/facts/ocean-oxygen.html>

## 1. EVID:X — nova observação PACE 2026

Fonte primária:
- NASA Earth Observatory, *El Niño Alters Marine Life in the Pacific*, 2026-08-10/13: <https://science.nasa.gov/earth/earth-observatory/el-nino-alters-marine-life-in-the-pacific/>

Comparação observacional:

```text
junho/2025: ENSO neutro
junho/2026: El Niño em intensificação
sensor      : PACE / OCI
observável  : clorofila-a superficial por cor do oceano
sinal       : queda substancial de Chl-a no Pacífico equatorial central
```

Mecanismo físico aceito para a rota:

```text
El Niño
→ alísios equatoriais enfraquecidos
→ camada superficial quente mais profunda
→ ressurgência de água fria/rica em nutrientes suprimida
→ menor suprimento de nutrientes à zona eufótica
→ menor Chl-a / fitoplâncton
```

**Invariante:** `PACE_CHL_A != DISSOLVED_O2`. OCI mede cor/clorofila; O₂ precisa de observação/modelo próprio.

## 2. O:X — sete eixos independentes

1. `O_ENSO` — ENSO index, SST, SSH, vento/alísios;
2. `O_FLOW` — `U=(u,v,w)`, ressurgência `w_up`, mistura, MLD, frentes e advecção;
3. `O_NUTRIENT` — NO₃⁻, NO₂⁻, PO₄³⁻, Si, Fe, deposição/entrada fluvial;
4. `O_PRIMARY` — Chl-a PACE/OCI, pigmentos, biomassa fitoplanctônica, NPP;
5. `O_REDOX` — O₂ dissolvido/saturação, respiração, remineralização, nitrificação, denitrificação, anammox;
6. `O_TROPHIC` — zooplâncton, ovos/larvas, peixes, presa e `Rhincodon typus`;
7. `O_GEO_AUX` — pluma amazônica como eixo Atlântico físico-biogeoquímico; SAA como covariável geomagnética independente.

## 3. Vetor de estado

```text
X(t,x,y,z) = [
  ENSO, SST, SSH,
  U, w_up, MLD,
  NO3, NO2, PO4, Si, Fe,
  Chl_a, NPP, O2,
  ZOO, FISH, WSI,
  AMAZON_PLUME, B_geo
]
```

Definições:
- `WSI`: índice observacional de presença/alimentação/agregação de `Rhincodon typus`;
- `AMAZON_PLUME`: salinidade + nutrientes + posição/idade da pluma;
- `B_geo`: intensidade/estado geomagnético local, sem causalidade biológica presumida.

## 4. REL:X — relações tipadas

### R1 — ENSO → fluxo → nutrientes → fitoplâncton

`ESTABLISHED_ROUTE`

```text
ENSO → circulação/upwelling → nutrientes → Chl-a/NPP
```

### R2 — fitoplâncton ↔ O₂

`MECHANISTIC_BUT_MULTIFACTORIAL`

Fitoplâncton fotossintético produz O₂, mas o O₂ dissolvido observado resulta também de temperatura, solubilidade, ventilação, mistura, troca ar-mar, respiração e remineralização.

Portanto:

```text
ΔChl_a < 0  !=  ΔO2 < 0 automaticamente
```

### R3 — NO₃⁻ / NO₂⁻ / O₂

`BIOGEOCHEMICAL_COUPLING`

NO₃⁻ é fonte central de N fixado para produção primária. NO₂⁻ é intermediário de nitrificação e vias anaeróbias. Em zonas de mínimo O₂, a produção e o consumo de NO₂⁻ podem desacoplar e gerar acúmulo; o nitrito precisa ser variável diagnóstica própria.

Âncoras:
- <https://www.nature.com/articles/s41396-020-00852-3>
- <https://www.nature.com/articles/s41561-025-01849-3>

### R4 — rede trófica / Rhincodon

`REGIONAL_EVIDENCE_ROUTE`

```text
fitoplâncton/NPP
→ zooplâncton + ovos/larvas + presa
→ peixes / grandes filtradores-planktívoros
```

`Rhincodon typus` entra como **sentinela móvel da paisagem de presas e do campo oceanográfico**, não como causa do ciclo de O₂.

Evidência útil:
- Apego, Kudela & Yñiguez (2024), Donsol: estação de tubarão-baleia associada a temperatura, silicato, chuva e mudança da assembleia fitoplanctônica/diatomáceas. DOI `10.1016/j.rsma.2024.103898`.
- Guzman et al./rota de movimento-habitat no Pacífico Tropical Oriental usa SST, clorofila-a, produtividade primária, correntes e ventos como covariáveis: <https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2022.793248/full>.
- Agregações também podem seguir presas concentradas, inclusive ovos de peixe; Chl-a não deve ser tratada como alimento direto universal de Rhincodon.

### R5 — fluxo como operador, não decoração

Todos os escalares biogeoquímicos são transportados:

```text
∂C/∂t + ∇·(U C) = fontes - sumidouros + mistura/difusão
```

Comparações espaciais sem advecção, mistura e lag temporal podem gerar correlação espúria.

### R6 — Amazônia / pluma amazônica

`ESTABLISHED_ATLANTIC_ROUTE`

NASA documenta que a pluma amazônica fornece nutrientes que sustentam fitoplâncton e a rede de peixes no Atlântico e que a pluma é advectada pela North Brazil Current e pela North Equatorial Countercurrent.

- <https://science.nasa.gov/earth/earth-observatory/amazon-river-in-the-atlantic-ocean-7021/>
- ANACONDAS/SeaBASS estudou ciclos C/N na pluma e inclui oxigênio entre os parâmetros: <https://seabass.gsfc.nasa.gov/experiment/ANACONDAS>

**Fronteira:** `AMAZON_PLUME -> PACIFIC_PACE_2026` permanece sem mecanismo direto estabelecido.

### R7 — SAA / Anomalia do Atlântico Sul

`GEOMAGNETIC_AXIS | CAUSAL_BRIDGE_OPEN`

NASA descreve a SAA como região de campo geomagnético enfraquecido sobre América do Sul/Atlântico Sul, relevante ao ambiente de partículas e operação de satélites. NASA também registra ausência de impactos visíveis estabelecidos na vida cotidiana à superfície.

- <https://www.nasa.gov/missions/icon/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/>

Não existe, neste gate, evidência suficiente para promover:

```text
SAA → NOx/nitrato/nitrito → fitoplâncton → O₂ → peixes/Rhincodon
```

Estado obrigatório: `TOKEN_VAZIO_SAA_BIOGEOCHEM_CAUSALITY`.

## 5. Modelo dinâmico mínimo

Sem fixar coeficientes antes de calibração:

```text
dP/dt   = growth(T,I,NO3,PO4,Si,Fe)*P
          - grazing - mortality - div(U*P) + mixing

dO2/dt  = photosynthetic_production(P)
          - respiration - remineralization
          + air_sea_exchange - div(U*O2) + mixing

dNO3/dt = inputs + nitrification
          - assimilation - nitrate_reduction
          - div(U*NO3) + mixing

dNO2/dt = nitrification_production + nitrate_reduction
          - nitrite_oxidation - denitrification_anammox
          - div(U*NO2) + mixing
```

Parâmetros: `TOKEN_VAZIO_PARAM` até ajuste contra dados.

## 6. Hipótese Rhincodon falsificável

```text
H_WS:
anomalias persistentes Chl-a/NPP + fluxo + prey_field
antecedem mudanças em presença/agregação/alimentação de Rhincodon,
com sinal regional e sazonal.
```

Falsificadores:
- nenhum ganho preditivo sobre baseline `SST + seasonality + prey`;
- efeito desaparece em validação fora do local/período;
- sinal muda de direção sem mecanismo ecológico pré-registrado.

## 7. EVID:X / GAP:X

| ID | Estado | Conteúdo |
|---|---|---|
| `PACE_CHL_2026` | `PASS_OBSERVED` | queda de Chl-a no Pacífico equatorial central em jun/2026 |
| `ENSO_UPWELLING` | `PASS_MECHANISM` | El Niño suprime ressurgência/nutrientes |
| `OCEAN_O2_GROSS` | `PASS_CONTEXT` | ~metade da produção global de O₂ é oceânica; bruto ≠ líquido |
| `AMAZON_PHYTO` | `PASS_ROUTE` | pluma/nutrientes influenciam fitoplâncton no Atlântico |
| `RHINCODON_ENV` | `EVIDENCE_ROUTE` | Chl-a/NPP/SST/correntes/presas são covariáveis plausíveis/testadas |
| `O2_DIRECT_PACE` | `TOKEN_VAZIO` | OCI não mede O₂ diretamente |
| `NO2_DATASET` | `TOKEN_VAZIO` | série NO₂ ainda não sincronizada |
| `O2_DATASET` | `TOKEN_VAZIO` | série O₂ ainda não sincronizada |
| `WS_DATASET` | `TOKEN_VAZIO` | telemetria/avistamentos ainda não ligados |
| `AMAZON_TO_PACIFIC` | `TOKEN_VAZIO` | sem ponte causal direta estabelecida |
| `SAA_BIOGEOCHEM` | `TOKEN_VAZIO` | sem cadeia causal geomagnetismo→N→plâncton/O₂ |
| `PARAM` | `TOKEN_VAZIO` | coeficientes não calibrados |

## 8. Próximo experimento verificável

Construir cubo espaço-temporal co-registrado:

```text
PACE Chl-a
+ SST/SSH
+ vento
+ U / w_up / MLD
+ NO3 / NO2
+ O2
+ NPP
```

Dois domínios independentes:

### A — Pacífico equatorial 2025–2027

```text
ENSO → fluxo → nutrientes → Chl-a/NPP → O2/redox → rede trófica
```

### B — Atlântico tropical / pluma amazônica

```text
pluma + fluxo → nutrientes → Chl-a/NPP → O2 → peixe/Rhincodon
```

Para SAA, executar somente **controle/covariável negativa** no primeiro ciclo. Promoção causal exige mecanismo pré-registrado, lag plausível, efeito replicável e ganho preditivo fora da amostra.

## 9. Cadeia de custódia

```text
A Crítica 2026-08-17 (fonte secundária recebida)
→ NASA Earth Observatory/PACE 2026-08-10/13 (fonte primária verificada)
→ Drive predecessor oxygen/nitrogen/plankton (historical source)
→ Drive delta 2026-08-25: 1i6L6HOk13dU9Damh37FcvJycpmik-ewTgbXPve6Wr_Y
→ este Mapa delta
```

Fonte secundária recebida:
<https://acritica.net/meio-ambiente/imagens-da-nasa-mostram-queda-de-fitoplancton-no-pacifico-durante-el-nino/>

## 10. Retroalimentação

- `F_ok`: predecessor localizado; PACE/Chl-a integrado; O₂ e N separados; fluxo explicitado; Rhincodon tipado como sentinela; Amazônia e SAA separados por domínio.
- `F_gap`: datasets co-registrados de O₂, NO₂ e Rhincodon ainda ausentes; parâmetros não calibrados.
- `F_next`: materializar cubo observacional e testar lags/ganho preditivo por domínio.
- `DELTA`: aditivo e rastreável; nenhum predecessor foi reescrito.
