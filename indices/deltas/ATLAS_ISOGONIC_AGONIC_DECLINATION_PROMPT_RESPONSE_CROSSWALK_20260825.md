# ATLAS — Isogônicas × agônica × declinação × prompt↔resposta — 2026-08-25

**Estado:** `INDEXED_RESEARCH_DELTA | APPEND_ONLY | CLAIM_ALLOWED=false`  
**Parent:** `indices/deltas/ATLAS_SOLAR_LUNAR_TZOLKIN_AURORA_JOVIAN_HE3_20260825.md`  
**Privacidade:** texto bruto de mensagens privadas não é republicado neste repositório.  
**Regra:** `FONTE_PRIVADA != ARTEFATO_PÚBLICO != EVIDÊNCIA_FÍSICA`.

## 0. Objetivo

Reconstruir a linha histórica iniciada por um prompt de 2025 sobre
`noise floor`, declinação magnética e linhas chamadas no prompt de
"antagônicas" e isogônicas; corrigir a terminologia para geomagnetismo
verificável; e cruzar a geometria de declinação com a malha já criada
para SAA, aurora, vento solar, Lua, calendário e biosfera.

A palavra histórica `antagônicas` é preservada como token de proveniência.
Quando o sentido é linha de declinação zero, o termo geomagnético usado
neste delta é **agônica**.

## 1. Cadeia de custódia prompt → resposta

O export longitudinal do Drive possui mensagens JSONL com os campos:

```text
asset_refs
claim_allowed
content_type
conversation_id
create_time
epistemic_state
error_json
kind
message_id
node_id
parent_id
privacy_class
role
source_path
source_pointer
text
text_hash
```

A interação relevante é recuperável por identidade sem publicar o texto
privado integral:

```text
conversation_id = 67edff88-f77c-800d-83e6-2374b28e0f6b
prompt_message_id = bbb21868-fe25-40c0-89e1-65e01103a288
prompt_text_hash = b280c0b3203cbcaac34d2c7cddae1ac69e5795515d1088e8b07e41f99c063666
response_message_id = d94f3e38-a533-4b24-bf95-ed2f3f9d2388
response_parent_id = bbb21868-fe25-40c0-89e1-65e01103a288
response_text_hash = 2d8d6e61dc13be470d5b82f68cb97dc01d7ca5ebcb11035190a10da9f4cf60ac
relation = DIRECT_PARENT_CHILD
privacy_class = PRIVATE_DEFAULT_DENY
```

A estrutura confirma a relação causal conversacional mínima:

```text
prompt node
  └── assistant response node
```

Isto demonstra anterioridade da questão no corpus. Não demonstra que as
interpretações físicas da resposta antiga estejam corretas.

## 2. Auditoria da resposta histórica

### 2.1 Conteúdo tecnicamente aproveitável

- `noise floor` como piso de ruído de um sistema de medição;
- declinação magnética como ângulo entre norte magnético local e norte
  verdadeiro;
- isogônicas como contornos de declinação constante;
- agônica como caso especial `D = 0`;
- possibilidade de usar posição, magnetômetro e modelo global para
  corrigir rumo, desde que calibração e atitude do aparelho sejam tratadas.

### 2.2 Conteúdo rejeitado como física

A resposta histórica também adicionou linguagem de "portais",
"navegação da intenção", "zona de conflito" e outros significados sem
observável geomagnético correspondente.

Estado:

```text
METAPHOR_AS_PHYSICS = REJECT
```

Uma interação posterior do mesmo corpus chamou linhas "sintagônicas" de
estrutura magnética e afirmou sensores em execução sem receipt físico.
No presente atlas:

```text
SINTAGONIC_GEOMAGNETIC_TERM = REJECT_NONSTANDARD
UNVERIFIED_SENSOR_EXECUTION = REJECT_EXECUTION_WITHOUT_EVIDENCE
```

## 3. Geometria física correta

Para componentes horizontais norte e leste do campo principal,
`X` e `Y`:

```text
D = atan2(Y, X)
```

Pela convenção WMM/NCEI, `D > 0` é declinação para leste e `D < 0`
para oeste.

### 3.1 Isogônica

Uma linha isogônica é um conjunto de pontos que satisfaz:

```text
D(lat, lon, h, t) = d0
```

para um valor constante `d0`.

### 3.2 Agônica

A linha agônica é a isogônica especial:

```text
D(lat, lon, h, t) = 0
```

Logo, no modelo principal, o norte magnético horizontal coincide com o
norte verdadeiro naquele ponto e época.

### 3.3 Isopórica

Não confundir com agônica. Uma isopórica conecta lugares de igual
variação secular da declinação:

```text
dD/dt = constante
```

Ela é útil para medir a migração temporal das isogônicas.

### 3.4 Par oposto derivado

Para preservar a intuição histórica de "antagônicas" sem inventar uma
classe geofísica, pode-se definir apenas como feature matemática:

```text
ISO_PAIR(d) = {D = +d, D = -d}
```

Este par é simétrico em valor em torno de `D = 0`, mas **não** recebe o
status de estrutura geomagnética padrão.

## 4. Modelos e épocas

### WMM2025

Usar WMM2025 para navegação e campo principal no intervalo de validade
2025–2029/2030. O modelo fornece `X, Y, Z, H, F, I, D` e variação
secular.

Para 2026, a rota de dados deve preferir os produtos de declinação do
WMM2025 e, quando resolução espacial adicional for necessária, WMMHR2025.

### IGRF-14

Usar IGRF-14 para comparação científica histórica por época. O IGRF é o
modelo de referência do campo principal e permite reconstruir as épocas
aurorais históricas e a geometria atual sob a mesma família de modelo.

**Invariante:** WMM/IGRF representam o campo principal. Eles não contêm
a totalidade dos campos externos transientes de magnetosfera e ionosfera.

## 5. Decomposição observacional

Uma leitura real de magnetômetro deve ser tratada aproximadamente como:

```text
B_sensor = R_device * (
    B_main
  + dB_external
  + dB_crust_local
) + bias_hard_iron + distortion_soft_iron + noise
```

Depois de calibrar o sensor e resolver a atitude do aparelho:

```text
D_sensor = atan2(Y_corrected, X_corrected)
residual_D = wrap(D_sensor - D_main_model)
```

O residual não deve ser atribuído automaticamente a vento solar. Ele
pode conter erro de atitude, estruturas metálicas, eletrônica do aparelho,
campo crustal, ionosfera, magnetosfera e ruído instrumental.

## 6. Noise floor materializado

`noise floor` deixa de ser metáfora e passa a ser uma variável de
instrumentação.

Registrar, por janela temporal e banda escolhida:

```text
mag_noise_floor_nT_rms
mag_noise_psd
sample_rate_hz
calibration_state
device_attitude_quality
local_interference_flag
```

Sem série calibrada do magnetômetro:

```text
TOKEN_VAZIO_MAG_SENSOR_NOISE_FLOOR
```

## 7. Novos observáveis

Adicionar ao cubo geomagnético:

```text
D_main_deg
I_main_deg
F_main_nT
dDdt_deg_per_year
isogonic_value_deg
dist_to_agonic_km
grad_D_deg_per_km
isoporic_dDdt
D_WMMHR_minus_WMM_deg
D_sensor_deg
D_sensor_residual_deg
mag_noise_floor_nT_rms
model_family
model_generation
model_epoch
```

Uma grandeza derivada útil para a migração da linha agônica é a velocidade
normal local do contorno `D = 0`:

```text
v_agonic_normal ~= -(dD/dt) / ||grad D||
```

quando `grad D` estiver expresso por distância. É uma derivação de
cinemática de contorno, não uma variável fornecida diretamente pela NOAA.

## 8. Cruzamento com SAA

A SAA deve continuar representada principalmente pela intensidade e
geometria do campo:

```text
F_main
|B|
X, Y, Z
grad_F
field_minimum_location
```

A proximidade de uma isogônica ou da agônica pode entrar como covariável
geométrica, mas:

```text
AGONIC_LINE != SAA_BOUNDARY
ISOGONIC_LINE != SAA_CAUSE
```

Para 2026, o eixo SAA deve ser avaliado em conjunto com WMM2025/WMMHR e
IGRF-14, registrando altitude e época.

## 9. Cruzamento com aurora

A borda auroral continua sendo uma resposta de alta latitude em
coordenadas magnéticas apropriadas:

```text
AEB, PAB, oval_width, hemispheric_power
```

O experimento 1972–1977 ↔ 2025–2026 deve registrar a geometria de campo
principal de cada época usando IGRF-14 e depois converter para
AACGM/APEX/MLT ou transformação magnética documentada equivalente.

Declinação geográfica local `D` é contexto, não substituto de MLAT/MLT.

Modelo de controle expandido:

```text
Y_aurora(t) = f(
  IMF_By, IMF_Bz, Vsw, Pdyn,
  Kp, AE, Dst,
  dipole_tilt, MLT,
  D_main, F_main, model_epoch,
  season, solar_cycle_phase
)
```

Somente depois entram Lua e features calendáricas exploratórias.

## 10. Cruzamento com vento solar

Vento solar e IMF pertencem à parcela externa/dinâmica do sistema.
WMM/IGRF não devem ser usados como se previssem tempestades.

Comparar:

```text
residual_D(t)
vs
IMF_By, IMF_Bz, Vsw, Pdyn, Kp, AE, Dst
```

somente após retirar interferência local e erro de sensor.

## 11. Cruzamento com Lua, Tzolk’in e Calendar Round

As fases já registradas permanecem eixos independentes. Nenhuma linha
isogônica é derivada de Tzolk’in, Haab ou Calendar Round.

A ordem estatística continua:

1. campo principal e época;
2. vento solar/IMF e índices geomagnéticos;
3. geometria orbital, estação e dipole tilt;
4. Lua/marés;
5. calendários como features exploratórias.

## 12. JSONs efetivamente revisados nesta rota

- `data/research/solar_lunar_aurora_jovian_observables.v1.json`;
- `data/research/aurora_historical_image_manifest_1971_2026.v1.json`;
- `GEOMETRIA_SOLAR_Maia_Inca/data/calendar_cycles_matrix.json`;
- `GEOMETRIA_SOLAR_Maia_Inca/data/calendar_round_lunar_extension_20260825.v1.json`;
- `data/federation/geophysical-transduction-executable-route-v1.json`;
- exports privados `MESSAGES-00005.jsonl.txt` e `MESSAGES-00015.jsonl.txt`
  consultados no Drive somente para proveniência prompt↔resposta.

Não é alegado que todo JSON existente no universo do usuário tenha sido
lido nesta execução. O restante permanece:

```text
TOKEN_VAZIO_FULL_JSON_UNIVERSE_SWEEP
```

## 13. Estrutura de interação a preservar

Aplicar o contrato longitudinal já existente:

```text
prompt_id
-> session/time
-> theme
-> source message/node/parent
-> response child
-> extracted items
-> repository/file
-> artifact
-> execution
-> evidence
-> claim_gate
-> hashes/provenance
-> relations
-> F_gap
-> F_next
```

Isto permite auditar não só "o que foi dito", mas como uma resposta
transformou ou distorceu os itens do prompt.

## 14. Gates

| Gate | Estado |
|---|---|
| `PROMPT_RESPONSE_DIRECT_LINEAGE` | `PASS_SOURCE_OBSERVED` |
| `ISOGONIC_DEFINITION` | `PASS_STANDARD_GEOMAGNETICS` |
| `AGONIC_D_ZERO` | `PASS_STANDARD_GEOMAGNETICS` |
| `ISOPORIC_SECULAR_VARIATION` | `PASS_STANDARD_GEOMAGNETICS` |
| `WMM2025_DATA_ROUTE` | `PASS_DATA_ROUTE` |
| `WMMHR2025_DATA_ROUTE` | `PASS_DATA_ROUTE` |
| `IGRF14_HISTORICAL_ROUTE` | `PASS_DATA_ROUTE` |
| `SINTAGONIC_GEOMAGNETIC_TERM` | `REJECT_NONSTANDARD` |
| `METAPHOR_AS_PHYSICS` | `REJECT` |
| `UNVERIFIED_SENSOR_EXECUTION` | `REJECT_EXECUTION_WITHOUT_EVIDENCE` |
| `MAG_SENSOR_NOISE_FLOOR` | `TOKEN_VAZIO_DATASET` |
| `CROSS_INSTRUMENT_DECLINATION_CUBE` | `TOKEN_VAZIO` |
| `AGONIC_AURORA_CAUSALITY` | `TOKEN_VAZIO` |
| `AGONIC_SAA_CAUSALITY` | `TOKEN_VAZIO` |
| `FULL_JSON_UNIVERSE_SWEEP` | `TOKEN_VAZIO` |

## 15. Próximo experimento verificável

Construir duas camadas co-registradas:

```text
LAYER_MAIN_FIELD(t,lat,lon,h)
= [D,I,F,X,Y,Z,dDdt,grad_D,dist_to_agonic]

LAYER_DYNAMIC(t)
= [IMF_By,IMF_Bz,Vsw,Pdyn,Kp,AE,Dst]
```

Depois anexar:

```text
AURORA = [AEB,PAB,HP,MLT]
SAA = [F_min,grad_F]
DEVICE = [D_sensor,residual_D,noise_floor,calibration]
```

Comparar épocas históricas com **a mesma versão de IGRF** sempre que o
objetivo for detectar mudança física secular; registrar WMM2025/WMMHR
separadamente como produto operacional contemporâneo.

## 16. Retroalimentação

`F_ok`: anterioridade do prompt recuperada; relação prompt→resposta
confirmada por `parent_id`; terminologia física corrigida; WMM/IGRF,
isogônica/agônica/isopórica e integração com SAA/aurora materializadas.

`F_gap`: ainda faltam grade numérica WMM/IGRF co-registrada, série física
do magnetômetro e varredura total de todos os JSONs do universo.

`F_next`: ingerir os grids de declinação por época, gerar distância à
agônica/gradiente/velocidade secular e juntar com DMSP–SSUSI–OMNI.

`DELTA`: append-only; texto privado permanece no Drive; GitHub conserva
somente proveniência segura, sem credenciais e sem conteúdo privado bruto.
