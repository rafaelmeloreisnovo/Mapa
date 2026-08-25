# ATLAS — Tzolk’in × Lua × vento solar × aurora/equinócio × O₃ × Voyager/Juno × Júpiter He³ — 2026-08-25

**Estado:** `INDEXED_RESEARCH_DELTA | APPEND_ONLY | CLAIM_ALLOWED=false`  
**Parent:** `indices/deltas/ATLAS_AURORA_SAA_GEOMETRY_IONIZATION_BIOSPHERE_CORRELATION_20260825.md`  
**Autoridade federada:** `Mapa` roteia; `GEOMETRIA_SOLAR_Maia_Inca` é autoridade calendárica; `Clima` é autoridade de química ionosférica/O₃; fontes NASA/NOAA/Smithsonian são evidência externa.  
**Regra:** `CALENDÁRIO != FORÇANTE FÍSICA != CORRELAÇÃO != CAUSALIDADE`.

## 0. Objetivo

Materializar uma matriz observacional capaz de testar, sem fusão indevida de domínios:

```text
Tzolk'in / Haab / Calendar Round
+ fases e marés lunares
+ vento solar / IMF
+ geometria de equinócio e dipole tilt
+ bordas do oval auroral
+ ionização N/O → NOx/HOx → O3
+ biosfera oceânica/terrestre
+ comparação planetária Voyager/Galileo/Juno em Júpiter
```

## 1. Predecessores internos localizados

### 1.1 GEOMETRIA_SOLAR_Maia_Inca

`data/calendar_cycles_matrix.json` já registra:
- `CAL-MAYA-TZOLKIN-260` como ciclo de `260 day`, `evidence_state=VERIFIED`;
- ciclo Venus 5×8 como `PARTIAL`;
- candidatos lunar/auroral ainda como `TOKEN_VAZIO` quando não havia fonte.

### 1.2 Clima / SAA-Aurora

`Clima/docs/IONOSFERA_QUIMICA_AURORA_ELETRODINAMICA.md` já separa ionização, aurora, O/N, O₂/N₂, O₃ e geometria solar. O pipeline privado `saa_aurora_pipeline` já possui ionização O/N/O₂/N₂, mas o campo SAA ainda tem gap IGRF/tilt explícito.

## 2. Tzolk’in, Haab e o número 51,### / 52 anos

Fonte institucional: Smithsonian/NMAI, *Living Maya Time*.

```text
Tzolk'in = 13 × 20 = 260 dias
Haab     = 365 dias
Calendar Round = lcm(260,365) = 18.980 dias
               = 73 Tzolk'in
               = 52 Haab
```

Usando ano tropical médio `365.2422 d`:

```text
18.980 / 365.2422 = 51.9655177 anos tropicais
52 anos tropicais - 18.980 d = 12.5944 dias
```

Portanto o seu `51,### anos ↔ 52 anos` é matematicamente real: **52 Haab = ~51,9655 anos tropicais**.

**Invariante:** isto não demonstra um ciclo físico de aurora de 52 anos. É um período calendárico que pode ser usado como base de fase em teste estatístico.

## 3. Lua — fases, maré e ionosfera

Eixos independentes:

```text
LUNAR_PHASE       ≈ ciclo sinódico 29.53 d
SPRING_NEAP       ≈ meia lunação ~14.77 d
LUNAR_NODAL       ≈ 18.6 anos
ATM_LUNAR_TIDE    = maré atmosférica lunar semidiurna
```

NASA/ICON + GOLD observaram maré lunar atmosférica acoplando ventos neutros, deriva de plasma `E×B` e airglow O 135.6 nm. Em oceanografia há evidência regional de ciclos lunar/tidal em plâncton; isso não é universal.

Adicionar fases como **relógio físico gravitacional/iluminação**, não como substituto de vento solar.

## 4. Vento solar + equinócio

Variáveis mínimas:

```text
Vsw, Nsw, Pdyn
IMF_Bx, IMF_By, IMF_Bz
IMF_clock_angle
dipole_tilt
Kp, AE, Dst
F10.7 / solar-cycle context
```

A atividade geomagnética possui, em média, variação semi-anual com máximos próximos aos equinócios. O efeito Russell–McPherron depende da geometria relativa entre IMF, eixos solar/terrestre e dipolo geomagnético.

**Correção importante:**

```text
EQUINOX != AURORAL_BOUNDARY_CONTRACTION
```

Em média, maior acoplamento geomagnético perto dos equinócios tende a favorecer **expansão equatorward** do oval quando a forçante é geoe efetiva. A contração poleward ocorre tipicamente em recuperação/baixa atividade ou após IMF tornar-se norte.

## 5. Borda auroral — arquivo histórico 1971→2026

### 5.1 âncoras históricas

```text
1971-1973  ISIS-II: mapeamento global UV de emissões aurorais
1973-1974  DMSP: fotografias usadas para derivar extensão equatorward da atividade auroral
1981       imagem UV global do oval (12 min, choque interplanetário)
1995       POLAR planning: modelo Holzworth–Meng + IGRF 1995
1996-1997  POLAR/UVI global images
2002-2007  TIMED/GUVI
2004-...   DMSP/SSUSI
2018-2025  GOLD dayside aurora dataset
```

O arquivo DMSP de 1973–1974 é especialmente útil porque 1974→2026 = 52 anos civis, muito próximo de uma janela Calendar Round.

### 5.2 o que pode ser testado

Resposta principal:

```text
AEB(t) = latitude geomagnética da equatorward auroral boundary
PAB(t) = poleward auroral boundary
W(t)   = PAB-AEB / largura do oval
HP(t)  = hemispheric power
Q(t)   = electron energy flux
```

Literatura mostra:
- `IMF Bz southward → expansão equatorward`;
- `IMF Bz northward / quieting → contração poleward`;
- expansão média pode ocorrer em ~45 min e contração em escala de horas (~8 h em estudo clássico), portanto comparar fotos sem estado do IMF/Kp gera falso ciclo.

### 5.3 gate 52 anos

`1973/74 ↔ 2025/26` permite **comparação de duas épocas**, mas não estima periodicidade de 52 anos de modo robusto. Dois pontos separados por um período não formam uma série periódica.

Estado:

`TOKEN_VAZIO_52Y_AURORA_PERIODICITY`.

## 6. O₃ — ponte química real, mas não oceânica automática

Rota física aceita:

```text
EPP / aurora
→ ionização/dissociação N2,O2,O,N
→ NOx + HOx
→ química catalítica de O3
```

A ponte seguinte permanece aberta:

```text
EPP/NOx/O3
→ deposição superficial de N
→ NO3/NO2 oceânico
→ fitoplâncton
```

Estado: `TOKEN_VAZIO_AURORA_TO_SURFACE_N_FLUX`.

## 7. Voyager, Galileo, Juno e He³ em Júpiter

### 7.1 Voyager

Voyager 1/IRIS forneceu estimativas de H₂/He e abundância total de hélio na atmosfera joviana. A estimativa Voyager antiga apontava fração mássica de He em torno de `~0.19–0.21`, com incertezas grandes.

### 7.2 Galileo — correção de autoridade para He³

O isótopo `³He` **não deve ser atribuído a Juno**. A medição direta relevante é da Galileo Probe Mass Spectrometer.

Valor reavaliado publicado:

```text
3He/4He ≈ (1.66 ± 0.05) × 10^-4
```

É um traçador de composição/protosolar e evolução química, não um driver auroral.

### 7.3 Juno

Juno entra em:

```text
JUNOMAG → B Joviano 3D
JADE/JEDI → partículas
UVS → aurora UV
Waves → plasma/ondas
magnetopause compression ← solar wind
```

Júpiter fornece **comparador planetário** para magnetosfera→aurora, não uma prova causal da cadeia terrestre O₃/plâncton.

## 8. Vetor de estado federado V2

```text
X(t) = [
  TZ_260, HAAB_365, CR_18980,
  lunar_phase, lunar_declination, lunar_tide, lunar_node,
  doy, equinox_phase, dipole_tilt,
  Vsw, Nsw, Pdyn, IMF_Bx, IMF_By, IMF_Bz, IMF_clock,
  Kp, AE, Dst, F10_7,
  AEB_N, PAB_N, HP_N, AEB_S, PAB_S, HP_S,
  EPP_e, EPP_p, Ne, NOx, HOx, O3,
  Chl_a, NPP, O2, NO3, NO2,
  JUP_B, JUP_AUR_POWER, JUP_SOLAR_WIND_PROXY,
  JUP_He_total, JUP_3He_4He
]
```

## 9. Features de fase — implementação

Para qualquer período `P`, representar ciclo por seno/cosseno para evitar descontinuidade de borda:

```text
phase_P(t) = 2π * ((t-t0) mod P) / P
feature_P  = [sin(phase_P), cos(phase_P)]
```

Aplicar a:

```text
P = 260 d      Tzolk'in
P = 365 d      Haab
P = 18980 d    Calendar Round
P = 29.53 d    lunar synodic
P ≈ 14.77 d    spring-neap
P ≈ 27 d       solar rotation
P ≈ 13.5 d     half solar rotation
P ≈ 182.62 d   semiannual/equinoctial
P ≈ 365.24 d   annual
```

Calendar Round deve entrar como **feature exploratória** com penalização por baixa identificabilidade.

## 10. Modelo de teste

Resposta principal: `AEB(t)` e `HP(t)`.

```text
Y(t) = β0
     + β_cal * calendar_features
     + β_lua * lunar_features
     + β_season * annual/semiannual
     + β_sw * [Vsw,Pdyn,IMF_By,IMF_Bz,clock]
     + β_geo * [dipole_tilt,Kp,AE,Dst]
     + interactions
     + ε
```

### Hierarquia obrigatória

1. baseline físico: vento solar + IMF + atividade geomagnética;
2. geometria: estação/equinócio + dipole tilt + MLT;
3. Lua: fase/maré/nó;
4. calendários: 260/365/18.980 d;
5. somente então biosfera/O₃ como respostas separadas.

### Falsificadores

- feature 260/18.980 não melhora validação fora da amostra;
- sinal desaparece após controlar IMF/Kp/seasonality;
- efeito troca de sinal entre eras/instrumentos;
- alinhamento depende de escolher arbitrariamente `t0`;
- 52 anos só aparece ao comparar 1974 e 2026, sem suporte em épocas intermediárias.

## 11. Dataset binding

Implementar adaptadores read-only para:

```text
NASA OMNI          → vento solar + IMF + índices
DMSP/SSUSI         → auroral EDR / boundary
TIMED/GUVI         → aurora 2002-2007
POLAR/UVI          → arquivo global 1990s
ISIS-II / DMSP     → arquivo histórico 1970s
NASA ICON/GOLD     → lunar tide / O 135.6 nm / aurora dayside
PACE               → Chl-a
Aura/MLS           → NOx/O3
Voyager IRIS       → H2/He histórico de Júpiter
Galileo GPMS       → 3He/4He e composição joviana
Juno MAG/UVS/etc   → B/aurora/partículas jovianas
```

## 12. Gates

| ID | Estado |
|---|---|
| `TZOLKIN_260` | `PASS_CALENDAR_STRUCTURE` |
| `CALENDAR_ROUND_18980` | `PASS_ARITHMETIC` |
| `CR_51_9655_TROPICAL_Y` | `PASS_ARITHMETIC` |
| `LUNAR_TIDE_IONOSPHERE` | `PASS_OBSERVED_ROUTE` |
| `EQUINOX_SEMIANNUAL_GEOMAG` | `PASS_MECHANISM_CONTEXT` |
| `AURORA_BOUNDARY_HIST_1973_74` | `PASS_ARCHIVAL_ROUTE` |
| `AURORA_BOUNDARY_MODERN` | `PASS_DATA_ROUTE` |
| `O3_EPP_NOX` | `PASS_MECHANISM` |
| `JUPITER_VOYAGER_HE` | `PASS_HISTORICAL_MEASUREMENT` |
| `JUPITER_GALILEO_3HE4HE` | `PASS_DIRECT_MEASUREMENT` |
| `JUNO_AURORA_MAG` | `PASS_DATA_ROUTE` |
| `52Y_AURORA_PERIODICITY` | `TOKEN_VAZIO_IDENTIFIABILITY` |
| `TZOLKIN_AURORA_CAUSALITY` | `TOKEN_VAZIO` |
| `AURORA_TO_SURFACE_N_FLUX` | `TOKEN_VAZIO` |
| `JUPITER_HE3_AURORA_DRIVER` | `REJECT_CATEGORY_ERROR` |

## 13. Próximo experimento verificável

### EXP-A — 1973/74 ↔ 2025/26 auroral boundary

Normalizar cada observação para AACGM/MLT e parear somente estados comparáveis de `IMF Bz`, `Vsw`, `Kp/AE`, estação e iluminação. Testar mudança secular da borda; **não** chamar de ciclo 52 anos com apenas duas épocas.

### EXP-B — equinócio

Superposed-epoch em março/setembro, condicionado por polaridade IMF e Russell–McPherron. Testar `AEB`, `HP`, NOx/O₃ e latência.

### EXP-C — multicíclo

Adicionar harmônicos 260 d, 29.53 d, 27 d, 13.5 d, semiannual e annual ao baseline físico. Medir ganho fora da amostra e estabilidade de fase.

### EXP-D — comparador Júpiter

Comparar somente invariantes magnetosféricos dimensionais/normalizados: pressão de vento solar → compressão de magnetopausa → partículas/ondas → aurora. Manter `³He/⁴He` como traçador de composição independente.

## 14. Retroalimentação

- `F_ok`: Tzolk'in/52 Haab reconstruído; Lua, vento solar, equinócio, borda auroral, O₃, Voyager/Galileo/Juno e He³ tipados por autoridade.
- `F_gap`: falta baixar/co-registrar os dados brutos de 1973–74 e 2025–26; 52 anos ainda não é periodicidade demonstrada.
- `F_next`: materializar cubo auroral histórico↔moderno e executar EXP-A/B/C.
- `DELTA`: aditivo; nenhum predecessor foi reescrito; `claim_allowed=false`.
