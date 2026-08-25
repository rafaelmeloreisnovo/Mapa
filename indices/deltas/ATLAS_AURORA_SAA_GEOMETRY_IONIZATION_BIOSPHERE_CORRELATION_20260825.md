# ATLAS — Aurora × SAA × Geometria Terra–Campo × Ionização N/O × Biosfera — Addendum 2026-08-25

**Estado:** `INDEXED_RESEARCH_ADDENDUM | APPEND_ONLY | CLAIM_ALLOWED=false`  
**Parent:** `indices/deltas/ATLAS_PACE_PHYTO_O2_NITROGEN_RHINCODON_FLOW_20260825.md`  
**Drive delta:** `1i6L6HOk13dU9Damh37FcvJycpmik-ewTgbXPve6Wr_Y`  
**Objetivo:** corrigir a omissão de aurora, geometria geomagnética, ionização N/O e séries históricas de decaimento/correlação, sem promover correlação a causalidade.

## 0. Correção de escopo

O delta predecessor tratou SAA apenas como covariável geomagnética independente. Isso ficou incompleto. O sistema correto precisa distinguir:

```text
Sol / vento solar / IMF
→ magnetosfera
→ reconexão + correntes + precipitação de partículas
→ aurora boreal/austral + ionosfera
→ ionização/dissociação de N2, O2, N e O
→ NOx/HOx + química de O3
```

e, separadamente:

```text
geodínamo + dipolo inclinado/descentrado + termos não dipolares
→ geometria do campo interno
→ SAA / intensidade B local / partículas aprisionadas
```

A SAA e a aurora pertencem ao mesmo sistema geomagnético, mas não são o mesmo fenômeno nem podem compartilhar automaticamente a mesma cadeia causal biogeoquímica.

## 1. Três ângulos/geometrias que não podem ser confundidos

### G1 — obliquidade orbital da Terra

`epsilon ≈ 23.44°`: eixo de rotação em relação à normal da eclíptica.

Controla fortemente estação, duração do dia, irradiância e geometria Sol–Terra. Não é a causa direta da SAA.

### G2 — tilt do dipolo geomagnético

Fontes NASA/NTRS de engenharia descrevem o eixo dipolar principal inclinado em aproximadamente `10–11°` em relação ao eixo de rotação e deslocado em aproximadamente `400–500 km` do centro geométrico.

Esse tilt + offset, somados aos termos não dipolares do campo do núcleo, produzem uma assimetria em que o cinturão interno de radiação aproxima-se mais da Terra sobre o Atlântico Sul/América do Sul: a SAA.

Âncoras:
- NASA/NTRS: <https://ntrs.nasa.gov/api/citations/20110015720/downloads/20110015720.pdf>
- NASA: <https://www.nasa.gov/missions/icon/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/>

### G3 — dipole tilt / Sun–Earth coupling

Para aurora e acoplamento magnetosférico, uma variável mais útil que um suposto “ângulo fixo da SAA” é o ângulo instantâneo entre a orientação do dipolo e a geometria Sol–Terra, combinado com IMF `Bz`, velocidade/densidade do vento solar e índices geomagnéticos.

Definir:

```text
psi_dip(t) = dipole tilt angle in solar-magnetospheric coordinates
Bz_IMF(t)
Vsw(t), Nsw(t)
Kp(t), AE(t), Dst(t)
```

A SAA não possui um único ângulo rígido: sua posição/intensidade migram e a região pode se dividir em lóbulos.

## 2. O pipeline privado já contém parte da física — e uma lacuna real

Autoridade de implementação observada:

`rafaelmeloreisnovo/Rafaelia_Private/saa_aurora_pipeline/`

O README declara cálculo de ionização para `O`, `N`, `O2`, `N2`, emissões aurorais e dinâmica dependente de B.

O código `src/saa_aurora_physics.c` observado faz:

```text
B(latitude, altitude)
× penalidade gaussiana SAA(lat,lon)
→ B_local
```

mas não transforma explicitamente coordenadas geográficas para um dipolo inclinado/descentrado nem usa IGRF para resolver a geometria vetorial completa.

Portanto:

`TOKEN_VAZIO_SAA_TILT_IMPLEMENTATION` = a documentação cita física geomagnética, mas o motor atual ainda aproxima a SAA por uma função gaussiana sobre latitude/longitude.

Próximo fix de implementação:

```text
GeoCoord
→ IGRF/WMM epoch field vector
→ geomagnetic coordinates / dipole tilt
→ |B| + inclination + declination + L-shell
→ trapped-particle / auroral operators
```

Aproximação gaussiana deve continuar apenas como fixture/baseline, não como autoridade física final.

## 3. Aurora: ionização de nitrogênio e oxigênio

Auroras resultam de partículas energéticas precipitantes guiadas pelo campo e colidindo com a atmosfera superior. A rota mínima separa excitação, ionização e dissociação:

```text
e* + N2 → N2+ + 2e
 e* + O2 → O2+ + 2e
 e* + N2 → N + N + e      [dissociação, esquema reduzido]
 e* + O/O2/N/N2 → estados excitados → emissão óptica
```

Em seguida, a química ionosférica liga N e O:

```text
N+ + O2 → NO+ + O
N(2D) + O2 → NO + O
```

A literatura NASA histórica mostra química auroral explícita de `NO+`, `O2+`, `O+`, `N2+`, NO e elétrons, além de produção de NOx por precipitação energética.

Âncoras:
- NASA NTRS, *The auroral ionosphere — comparison of a time-dependent model with composition measurements*: <https://ntrs.nasa.gov/citations/19790064337>
- NASA NTRS, *The chemistry of excited NO+ in an aurora*: <https://ntrs.nasa.gov/citations/19800065021>
- NASA NTRS, EPP overview: <https://ntrs.nasa.gov/citations/20120014295>

## 4. EPP → NOx/HOx → O3 é uma ponte física real

Precipitação de partículas energéticas (`EPP`) pode ionizar/dissociar moléculas e gerar:

```text
N2 dissociation → N → NO / NO2 = NOx
positive-ion chemistry → H / OH / HO2 = HOx
```

NOx possui tempo de vida suficientemente longo para, em certas condições polares de outono/inverno, ser transportado para baixo na mesosfera/estratosfera e participar de ciclos catalíticos de ozônio.

NASA Aura/MLS e revisões NASA tratam esse caminho como observado/modelado.

Âncoras:
- <https://aura.gsfc.nasa.gov/science/feature-20210402.html>
- <https://aura.gsfc.nasa.gov/science/feature-20200701.html>
- <https://ntrs.nasa.gov/citations/20120014295>

### Gate importante

Isto **não** fecha automaticamente:

```text
EPP / aurora
→ NOx mesosférico/estratosférico
→ nitrato/nitrito depositado no oceano
→ fertilização mensurável do fitoplâncton
```

Estado atual:

`TOKEN_VAZIO_AURORA_TO_SURFACE_N_FLUX`.

É preciso medir fluxo descendente/deposição, magnitude contra fontes dominantes de N, latitude, estação e transporte atmosférico.

## 5. Aurora boreal + aurora austral

Para uma análise planetária, usar as duas auroras. A aurora boreal é a manifestação do hemisfério norte; a austral, do sul.

A SAA está no hemisfério sul/Atlântico Sul e não deve ser geometricamente ligada apenas à aurora boreal. O acoplamento correto passa pela magnetosfera global e pelos hemisférios magnéticos.

Adicionar ao vetor de estado:

```text
AUR_N, AUR_S       # hemispheric auroral power / boundary / brightness
EPP_e, EPP_p       # precipitating electron/proton flux
Ne                 # electron density
N2p, O2p, Op, NOp  # ion composition when available
NOx, HOx, O3
psi_dip, Bz_IMF, Kp, AE, Dst
```

## 6. “Decaimento da aurora” — três fenômenos distintos

### D1 — fading/decay de evento

NASA/NTRS registra *auroral fading before breakup*: brilho auroral pode diminuir por ~1–2 min antes do breakup, associado a mudanças em correntes/eco de radar/absorção ionosférica.

Fonte: <https://ntrs.nasa.gov/citations/19780017764>

Um registro NASA de substorm em 13 junho 1983 mostra a aurora avançando por horas e depois declinando em luminosidade/retraindo no final da sequência.

Fonte: <https://pwg.gsfc.nasa.gov/istp/outreach/workshop/bobwhen.html>

### D2 — decaimento radiativo/químico de espécie excitada

No estudo NASA/NTRS de `NO+(a3Σ)`, o decaimento radiativo pode dominar acima de ~150 km, enquanto abaixo disso perdas por troca de carga com N2/O tornam-se importantes.

Fonte: <https://ntrs.nasa.gov/citations/19800065021>

### D3 — tendência histórica de atividade auroral

Não foi localizada autoridade NASA que sustente uma **queda secular monotônica universal da aurora boreal**. Frequência, potência e limite do oval variam com ciclo solar, vento solar, IMF e atividade geomagnética.

NASA mantém séries de limite auroral GUVI/SSUSI e registros históricos de expansão/retração do oval.

Fonte: <https://ccmc.gsfc.nasa.gov/ccmc-studies/auroral-oval/>

Logo:

`AURORA_EVENT_DECAY != LONG_TERM_AURORA_DECLINE`.

## 7. Decaimento do fitoplâncton e plantas — evidência NASA separada

### P1 — fitoplâncton / diatomáceas

NASA SVS publicou uma série global mostrando declínio de diatomáceas superior a `1%/ano` entre 1998–2012 no modelo impulsionado por dados de satélite, com perdas importantes no Pacífico Norte e oceanos Índico Norte/Equatorial.

Fonte: <https://svs.gsfc.nasa.gov/4350/>

Esse resultado é diferente do evento PACE/El Niño de 2026.

### P2 — vegetação amazônica

NASA publicou uma série de 13 anos na Amazônia oriental/sudeste: 2000–2012 teve redução de precipitação de até 25% em grande área e declínio de ~0.8% de greenness. O próprio estudo liga a resposta a seca/chuva e observa Amazônia mais marrom em anos El Niño e mais verde em anos La Niña.

Fonte: <https://www.nasa.gov/centers-and-facilities/goddard/nasa-study-shows-13-year-record-of-drying-amazon-caused-vegetation-declines/>

### P3 — ciclo conjunto terra/oceano

NASA também publica o ciclo anual conjunto de vegetação terrestre e clorofila oceânica: ambos seguem fortemente a sazonalidade de luz, temperatura e hemisfério.

Fonte: <https://svs.gsfc.nasa.gov/30709/>

Isto demonstra covariação biosférica sazonal, não causalidade auroral.

## 8. Correlação matemática: o que já pode e o que ainda não pode ser afirmado

Há literatura recente explorando relações com atividade solar/geomagnética, mas os resultados não são universais.

### C1 — fitoplâncton × atividade solar

Estudo de 2025 no Rybinsk Reservoir analisou clorofila-a versus número de manchas solares por ciclos 20–24. No ciclo 24 foi relatado `r_s ≈ 0.83`, forte correlação positiva; porém outros ciclos tiveram correlação negativa, fraca ou ausente.

DOI: `10.1007/s10452-025-10193-y`.

Portanto:

`STRONG_LOCAL_CYCLE_CORRELATION != UNIVERSAL_SOLAR_PHYTOPLANKTON_LAW`.

### C2 — vegetação × atividade geomagnética

Trabalho de 2026 usando fluorescência de clorofila induzida pelo Sol (SIF) por satélite e índice geomagnético relata associação temporal **fraca**, não uma resposta global forte estabelecida.

DOI: `10.3390/biology15161415`.

### C3 — coeficiente forte do material longitudinal interno

O Drive contém o título/registro histórico `Análise Plâncton e Interações`, mas nesta varredura não foi recuperado o trecho bruto contendo um coeficiente numérico interno aurora/plâncton/planta que possa ser auditado.

Estado obrigatório:

`TOKEN_VAZIO_INTERNAL_AURORA_BIOSPHERE_CORR_COEF`.

Não reconstruir o número por memória.

## 9. Modelo estatístico correto para testar a hipótese

A análise precisa impedir correlação espúria produzida por estação, ENSO e luz.

Definir séries normalizadas/anomalias:

```text
A(t) = auroral power / AE / EPP / Kp
S(t) = solar/geomagnetic drivers
P_ocean(t,x) = Chl-a / NPP / diatom abundance
P_land(t,x)  = NDVI / EVI / SIF / NPP
N(t,x,z) = NOx / NO3 deposition / NO2
```

### 9.1 Correlação cruzada com lag

```text
C_AP(tau) = corr(A(t), P(t+tau))
```

Testar lags de horas → dias → semanas → meses, definidos pelo mecanismo físico.

### 9.2 Correlação parcial

```text
r_partial = corr(A, P | ENSO, PAR, SST, precipitation,
                 temperature, season, aerosols, upwelling, nutrients)
```

Se o efeito some após os controles, não existe evidência de ponte independente auroral.

### 9.3 Coerência espectral/wavelet

Testar apenas após remover tendência e sazonalidade:

```text
WCOH_A,P(period,time)
```

Picos em ~27 dias, ~1 ano ou ~11 anos precisam ser confrontados com múltiplos drivers que compartilham essas periodicidades.

### 9.4 Falsificadores

A hipótese `H_AUR_BIO` falha se:
- correlação desaparece após controle de ENSO/PAR/SST/chuva;
- o lag observado é incompatível com transporte químico;
- não há fluxo de N suficiente para alterar o balanço de nutrientes;
- resultado não replica em outra região/período;
- ganho preditivo fora da amostra é nulo.

## 10. Vetor ampliado

```text
X_aurbio(t,x,y,z) = [
  epsilon_orb,
  psi_dip,
  B_geo, Bz_IMF, Vsw, Nsw,
  Kp, AE, Dst,
  AUR_N, AUR_S, EPP_e, EPP_p,
  Ne, N2p, O2p, Op, NOp,
  NOx_atm, HOx_atm, O3_atm,
  N_dep_surface,
  ENSO, SST, SSH, U, w_up, MLD,
  NO3_ocean, NO2_ocean, PO4, Si, Fe,
  Chl_a, NPP_ocean, O2_ocean,
  NDVI, SIF, NPP_land,
  ZOO, FISH, WSI,
  AMAZON_PLUME
]
```

## 11. Gates atualizados

| ID | Estado | Conteúdo |
|---|---|---|
| `GEOMAG_TILT_OFFSET` | `PASS_CONTEXT` | dipolo ~10–11° + offset ~400–500 km |
| `SAA_EVOLUTION` | `PASS_OBSERVED` | SAA enfraquece/migra/divide-se; não é geometria fixa |
| `AURORA_N_O_IONIZATION` | `PASS_MECHANISM` | precipitação ioniza/excita N/O/N2/O2 |
| `EPP_NOX` | `PASS_MECHANISM` | EPP produz NOx/HOx e pode alterar O3 polar |
| `AURORA_EVENT_DECAY` | `PASS_HISTORICAL` | fading/retração observados em eventos |
| `DIATOM_DECLINE_1998_2012` | `PASS_NASA_SERIES` | >1%/ano no estudo/modelo NASA |
| `AMAZON_VEG_DECLINE_2000_2012` | `PASS_NASA_SERIES` | declínio de greenness associado à seca |
| `SOLAR_CHL_RS_0_83` | `EVIDENCE_LOCAL` | forte correlação no ciclo 24 em um reservatório; não universal |
| `SAA_TILT_IMPLEMENTATION` | `TOKEN_VAZIO` | pipeline privado ainda não usa tilt/offset/IGRF completo |
| `AURORA_TO_SURFACE_N_FLUX` | `TOKEN_VAZIO` | falta fechar magnitude de deposição até oceano/solo |
| `GLOBAL_AURORA_BIOSPHERE_CAUSALITY` | `TOKEN_VAZIO` | sem causalidade global estabelecida |
| `INTERNAL_AURORA_BIOSPHERE_CORR_COEF` | `TOKEN_VAZIO` | coeficiente interno bruto ainda não recuperado |

## 12. Próxima execução verificável

1. Extrair séries NASA/NOAA/geomagnéticas na mesma grade temporal: `AE/Kp/Dst/EPP/auroral power`.
2. Extrair PACE/MODIS/SeaWiFS: `Chl-a/NPP`; MODIS/OCO/SIF para terra.
3. Adicionar `ENSO/PAR/SST/precipitação/vento/upwelling` como controles obrigatórios.
4. Obter NOx mesosférico/estratosférico e, separadamente, deposição de nitrato na superfície.
5. Rodar `cross-correlation + partial correlation + wavelet coherence + out-of-sample test`.
6. Recuperar do NOVOexport a conversa `Análise Plâncton e Interações` e materializar o coeficiente histórico interno com source pointer/hash.
7. Abrir fix de implementação no `saa_aurora_pipeline`: `Gaussian SAA baseline → IGRF/dipole geometry`.

## 13. Retroalimentação

- `F_ok`: aurora, geometria magnética, ionização N/O, NOx/HOx, decaimentos históricos e séries de plantas/plâncton agora estão explicitamente conectados por relações tipadas.
- `F_gap`: ainda não existe evidência suficiente de fluxo auroral de N até fertilização de superfície; coeficiente interno forte não foi recuperado nesta varredura; pipeline SAA não implementa o tilt/offset explicitamente.
- `F_next`: recuperar coeficiente longitudinal + construir teste multivariado com controles e lags + corrigir geometria do pipeline.
- `DELTA`: addendum append-only; predecessor preservado sem reescrita.
