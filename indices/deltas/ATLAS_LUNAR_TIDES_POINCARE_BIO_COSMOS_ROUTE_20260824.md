# ATLAS — Lua/Marés × Poincaré 1D–7D × Ionosfera/Aurora × Bio/Neuro × Cosmos — 2026-08-24

**Estado:** `INDEXED_RESEARCH_ROUTE | APPEND_ONLY | CLAIM_ALLOWED=false`  
**Objetivo:** materializar uma rota navegável e anti-regressiva entre NOVOexport, Mapa, Matemática, Cosmos, RLL e memória editorial do Drive, sem transferir evidência entre domínios.

## 0. Contrato de leitura

```text
ATLAS:X = procurar e selecionar autoridade/rota
NOVO:X  = começar pelo corpus bruto/índices NOVOexport
L:X     = preservar evolução longitudinal
O:X     = separar eixos independentes
T:X     = tipar pontes transversais
REL:X   = registrar relações estruturais
SCALE:X = navegar de META a escalas físicas/informacionais válidas
EVID:X  = evidência, prova, gate e falsificador
GAP:X   = TOKEN_VAZIO explícito
LEARN:X = incorporar delta append-only sem apagar predecessores
```

Invariante: `VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`.

## 1. Autoridades

- `rafaelmeloreisnovo/Mapa`: ontologia, relações, estado, dependências e roteamento.
- `rafaelmeloreisnovo/Matem-tica-`: definições formais, protocolos, validadores e matemática do programa Ω7.
- `instituto-Rafael/relativity-living-light`: domínio científico falsificável para clima, marés, heliofísica e experimentos/baselines.
- `rafaelmeloreisnovo/Cosmos`: mapa interdisciplinar e análise epistemológica; não herda prova de outros repositórios.
- Google Drive: memória longitudinal/editorial e custódia; não autoriza validade científica.

## 2. NOVO:X — primeiro sinal observado

Fonte editorial recente: `EXPLICIT_THEME_REGISTRY_SEED_V1`, Drive ID `1m0iQ-FeP5Rmz2fvIsJBtepgw7VCLtXbSUbzSeKCq-e4`.

No recorte bruto `conversations-000..007`, aparecem explicitamente:

- Neurociência — 45 conversas / 67 mensagens;
- Computação Quântica — 34 / 49;
- Biotecnologia — 28 / 36;
- Biofotônica — 18 / 22;
- DNA Computing — 15 / 23;
- Redes Neurais Fractais — 13 / 23;
- Neuromórfica — 6 / 10;
- Computação Cósmica — 4 / 11;
- Medicina Regenerativa — 3 / 4;
- ocorrências literais de Biofotônica Regenerativa, Biologia Quântica, Química Subquântica e Teoria do Campo Unificado.

Gate: isto prova **presença temática**, não invariância nem validade científica.

`TOKEN_VAZIO_NOVO_FULL_COVERAGE`: `conversations-008..050` ainda não estavam cobertas pelo seed observado.

## 3. Lua → marés: núcleo físico clássico

O campo gravitacional lunar e a maré não são o mesmo objeto. A maré é principalmente o **gradiente espacial** do campo da Lua através da Terra.

Para uma massa externa `M` a distância `d`, com `r` medindo o ponto terrestre relativo ao centro da Terra e `d_hat` apontando para o corpo perturbador, a aproximação de primeira ordem é:

\[
\mathbf a_{tidal}(\mathbf r) \simeq \frac{GM}{d^3}\left[3(\mathbf r\cdot\hat{\mathbf d})\hat{\mathbf d}-\mathbf r\right].
\]

No eixo Terra–Lua, a escala radial na superfície é aproximadamente:

\[
|a_{tidal}| \sim \frac{2GM_{Lua}R_{Terra}}{d_{TL}^3}.
\]

Consequências de modelagem:

```text
geometria Sol–Lua–Terra
→ gradiente gravitacional
→ maré sólida da Terra
→ maré oceânica + loading
→ residual gravimétrico local
```

O Sol entra pelo mesmo operador `M/d^3`; marés de sizígia/quadratura dependem da geometria relativa, não de rótulos calendáricos.

Autoridade executável existente:
`instituto-Rafael/relativity-living-light/docs/science/RLL_CLIMATE_MULTIPHYSICS_CYCLE_V1.md`.

Variáveis já tipadas nessa rota:
- distância Lua–Terra;
- declinação lunar;
- elongação Sol–Lua;
- maré sólida;
- maré oceânica/loading;
- residual de gravidade local.

Fronteira: `BLUE_MOON` e `BLOOD_MOON` não recebem força gravitacional extra; ~6 h entre alta/baixa é característica aproximada de regime semidiurno, não regra universal.

## 4. Poincaré 1D → 7D: família dimensional única

Âncora auditável:
`instituto-Rafael/relativity-living-light/PapersPub/09_poincare_ball_7d_freestanding/paper.md`.

Para qualquer `n = 1..7`:

\[
B^n=\{p\in\mathbb R^n:\|p\|<1\},
\qquad
H^n=\{(X_0,X_s)\in\mathbb R^{1,n}: X_0>0,\ X_0^2-\|X_s\|^2=1\}.
\]

Métrica da bola:

\[
ds_n^2=\frac{4\sum_{i=1}^{n}dp_i^2}{\left(1-\sum_{i=1}^{n}p_i^2\right)^2}.
\]

Projeção hiperboloide → bola:

\[
p=\frac{X_s}{X_0+1}.
\]

Para vetor timelike bruto `u=(T,V)`:

\[
\Delta=T^2-\|V\|^2>0,
\qquad
p=\frac{V}{T+\sqrt{T^2-\|V\|^2}}.
\]

Lift computacional declarado, válido em qualquer `n`:

\[
q\in\mathbb R^n,
\quad X=(\sqrt{1+\|q\|^2},q),
\quad p=\frac{q}{\sqrt{1+\|q\|^2}+1}.
\]

Distância radial:

\[
d(0,p)=2\operatorname{artanh}(\|p\|).
\]

Especialização dimensional:

| n | coordenadas | domínio |
|---:|---|---|
| 1 | `(p1)` | `B¹` |
| 2 | `(p1,p2)` | `B²` |
| 3 | `(p1,p2,p3)` | `B³` |
| 4 | `(p1..p4)` | `B⁴` |
| 5 | `(p1..p5)` | `B⁵` |
| 6 | `(p1..p6)` | `B⁶` |
| 7 | `(p1..p7)` | `B⁷` |

A fórmula não muda de espécie; muda a dimensão do vetor e da norma.

**Gate:** `Poincare-ball embedding != Poincare return map != Poincare conjecture`.

No caso 7D atual, o material auditado distingue projeção Lorentziana estrita de `canonical lift`. As colunas brutas testadas eram spacelike; a projeção estrita permaneceu `TOKEN_VAZIO_INPUT_NOT_TIMELIKE`, enquanto o lift é somente embedding computacional construído.

Rotas em `Matem-tica-`:
- `data/registries/PG_OMEGA7_OPEN_PROBLEMS_REGISTRY_V1.json`
- `src/validate_pg_omega7_open_problems.py`
- `docs/PG_OMEGA7_MATRIZ_PROBLEMAS_ABERTOS_V1.md`
- `docs/formal/META_INVARIANT_CROSS_DOMAIN_TEST_PROTOCOL_V1.md`
- `papers/2026-08-08_auditoria_crossrepo_matematica_cosmos_teoremas.md`

## 5. O:X — eixos independentes

Os eixos abaixo são independentes para investigação; “ortogonal” aqui é operacional, não afirma ortogonalidade física:

1. `O_GRAV` — gravidade clássica, Lua/Sol, marés, geodesia;
2. `O_PLASMA` — vento solar, magnetosfera, partículas, ionosfera, aurora;
3. `O_GEOMAG` — campo geomagnético, SAA, magnetometria/ambiente de partículas;
4. `O_BIOELEC` — membrana, canais, PIEZO/TRP, Vm, Ca²⁺, fisiologia;
5. `O_BIOPHOTON` — UPE/biofotônica, emissão/detecção óptica e atribuição de fonte;
6. `O_QM` — física quântica/QED/efeitos microscópicos, sem transferência automática ao macro;
7. `O_MATH` — geometria hiperbólica/Poincaré, topologia, invariantes, representação e falsificação.

## 6. T:X + REL:X — pontes tipadas

### 6.1 Ponte heliofísica estabelecida como rota física

```text
vento solar / IMF Bz / densidade de prótons
→ magnetosfera
→ precipitação/energização de partículas
→ ionosfera
→ aurora + química ionosférica/escape
```

A SAA é uma ramificação geomagnética por intensidade de campo local e ambiente de partículas. Não é promovida automaticamente a causa de tempo meteorológico de superfície.

### 6.2 Ponte biofísica mecanística

```text
exposição física declarada
→ dose/geometria/controle
→ sensor/transdução
→ Vm / íons / Ca²⁺
→ fisiologia / sinalização
→ endpoint molecular específico
```

Exemplos tipados no ledger atual: bioeletricidade, PIEZO, thermo-TRP. DNA sequence, dano/aduto, metilação, cromatina e expressão gênica permanecem endpoints distintos.

### 6.3 Biofotônica/UPE

```text
metabolismo/estado biológico
→ emissão óptica ultra-fraca observável
→ detector + background + atenuação + atribuição de fonte
→ possível correlação fisiológica/neural
```

`TOKEN_VAZIO_UPE_BRAIN_CAUSALITY`: emissão biológica mensurável não fecha atribuição cerebral extracraniana nem comunicação neural funcional.

### 6.4 Biomagnetismo

Tratar separadamente:

```text
atividade elétrica/fisiológica
↔ campos magnéticos endógenos mensuráveis
↔ magnetometria (ex.: rota MEG/MCG quando aplicável)
```

`TOKEN_VAZIO_BIOMAGNETISM_CROSSDOMAIN`: no material auditado não foi estabelecida ligação experimental entre biomagnetismo/UPE e Poincaré, wormholes ou uma causalidade aurora→organismo.

### 6.5 Matemática como representação, não causalidade

Poincaré/Hⁿ/Bⁿ pode servir para:
- representação de estados;
- distância/anomalia;
- organização de grafos/embedding;
- comparação com baseline Euclidiano.

Não pode, sozinho, provar:
- que o sistema físico é hiperbólico;
- que existe acoplamento causal entre domínios;
- que uma semelhança geométrica é mecanismo físico.

## 7. Rota multidisciplinar selecionada

```text
NOVOexport bruto
  ↓ presença temática/proveniência
Mapa
  ↓ ontologia + relações + gaps
├─ Matemática → formalização Poincaré/invariantes/testes
├─ RLL → Lua/marés + clima + heliofísica + ionosfera + SAA
├─ Mapa/Papers → neurociência + biofísica + EMF + UPE + bioeletricidade
└─ Cosmos → matemática | cosmologia | quântica | consciência/observação
```

No `Cosmos`, usar preferencialmente:
- `docs/areas/01-mathematics-number-theory.md`
- `docs/areas/02-cosmology-astrophysics.md`
- `docs/areas/03-quantum-physics-energy.md`
- `docs/areas/05-consciousness-observation.md`
- `docs/areas/06-fractal-geometry.md`

A função do Cosmos nesta rota é contextual/epistemológica. Claims antigos mais fortes devem ser confrontados com auditorias modernas antes de promoção.

## 8. SCALE:X

```text
META      : ontologia, hipótese, claim, falsificador
planetário: geometria Sol–Lua–Terra, magnetosfera, ionosfera
regional  : SAA, oceano, atmosfera, clima
organismo : fisiologia, neurociência, bioeletricidade
tecido    : transdução, canais, sinalização
celular   : Vm, Ca²⁺, metabolismo
molecular : DNA/adutos/metilação/proteína/ROS conforme endpoint
quântico  : fótons, estados/energia quando o mecanismo realmente exige QM
informacional: token → mensagem → conversa → tema → relação → índice
```

Escalas subatômicas/yocto só entram quando houver variável física, unidade, instrumento/modelo e necessidade real; não são usadas como decoração semântica.

## 9. L:X — evolução longitudinal preservada

```text
pré-papers/claims históricos
→ auditorias matemáticas fail-closed
→ Poincaré H7/B7 auditável
→ meta-invariant regions R1..R8
→ neurocognitive-biophysical claims/gates
→ NOVOexport explicit-theme seed 2026-08-24
→ este índice relacional
```

Regra: material antigo não é apagado; recebe relação `PREDECESSOR/HISTORICAL_CLAIM` quando uma auditoria posterior reduz o estado de evidência.

## 10. EVID:X — estados atuais

- `PASS/FORMAL`: família matemática padrão Hⁿ/Bⁿ e lift declarado sob suas definições.
- `FORMAL_SPEC`: matriz multiphysics, variáveis tipadas e rota de ingestão/falsificação do RLL.
- `EVIDENCE_FOUND_GATE_OPEN`: vários mecanismos bioelétricos/EMF/epigenéticos no ledger neuro-bio, ainda sem autorização global de claim.
- `TOKEN_VAZIO`: UPE como comunicação cerebral; biomagnetismo como ponte universal; causalidade Poincaré↔bio; aurora/SAA→fisiologia humana específica; ganho preditivo do embedding Poincaré no clima sem benchmark fechado.

## 11. GAP:X — lacunas prioritárias

1. `TOKEN_VAZIO_NOVO_FULL_COVERAGE` — completar `conversations-008..050` e shards posteriores.
2. `TOKEN_VAZIO_FORMULA_CORPUS_RECONCILIATION` — ligar blocos brutos aos IDs formais de fórmula.
3. `TOKEN_VAZIO_CLIMATE_HISTORICAL_BENCHMARK` — evento congelado + baseline Euclidiano/adaptativo + erro/latência/custo.
4. `TOKEN_VAZIO_BIOMAGNETISM_CROSSDOMAIN` — sem mecanismo/dataset/falsificador para ponte ampla.
5. `TOKEN_VAZIO_UPE_BRAIN_CAUSALITY` — falta atribuição independente de fonte e replicação adversarial.
6. `TOKEN_VAZIO_AURORA_BIO_CAUSALITY` — nenhuma transferência automática de evidência de heliofísica para fisiologia.
7. `TOKEN_VAZIO_POINCARE_PHYSICAL_CAUSALITY` — embedding geométrico não é mecanismo físico.

## 12. F_next verificável

1. Expandir extração literal do NOVOexport e produzir relações por `source_shard/conversation/message_id`.
2. Hidratar um evento geomagnético real e um evento de maré/clima no RLL com receipts.
3. Comparar `B^7 distance` com baseline Euclidiano sob orçamento idêntico.
4. Criar ledger específico `geomagnetic_biophysical_bridges` com campos: `driver | dose/exposure | sensor | endpoint | unit | dataset | confounders | falsifier | evidence_state`.
5. Manter biofotônica/UPE e biomagnetismo em trilhas separadas até uma ponte experimental fechar.

## 13. Retroalimentação

`F_ok`: rota NOVO → Mapa → Matemática/RLL/Bio/Cosmos materializada; Poincaré 1D–7D unificado dimensionalmente; relações físicas e representacionais separadas.  
`F_gap`: cobertura NOVO incompleta e principais pontes bio-geomagnéticas permanecem `TOKEN_VAZIO`.  
`F_next`: fechar cobertura literal, datasets/receipts e benchmarks antes de qualquer promoção causal.
