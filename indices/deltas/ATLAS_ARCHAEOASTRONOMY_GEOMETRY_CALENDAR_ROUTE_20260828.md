# ATLAS — Arqueoastronomia, Geometria e Calendários — rota L/O/T

**ID:** `ATLAS-AGC-20260828`  
**Data:** `2026-08-28`  
**Estado:** `APPEND_ONLY / EVIDENCE_FIRST / CLAIM_GATED`  
**Claim global:** `claim_allowed=false`  
**Contrato:** `OBSERVED_LITERAL != THEME_RECURRENT != INVARIANT != CLAIM`

## 0. Objetivo

Registrar e testar, sem apagar a origem simbólica, relações propostas entre geometria, calendários, arqueoastronomia, toro/Poincaré, redes triangulares/hexagonais e marcos históricos. O documento NÃO afirma transmissão histórica entre civilizações sem evidência documental/arqueológica.

Rota canônica lida antes deste delta:

```text
ATLAS:X → authority → source → literal → theme → L/O/T memory → relations → scale → evidence → gate → delta → index
```

Índices de memória consultados:

- `L:` longitudinal — evolução temporal, versões, decisões, receipts;
- `O:` ortogonal — provenance, integrity, runtime, measurement, symbolic, science claim, governance etc.;
- `T:` transversal — pontes entre domínios, escalas, métodos e aplicações.

## 1. Legenda epistemológica

| Selo | Significado |
|---|---|
| `[F]` | matemática formal/dedutível a partir das definições declaradas |
| `[E]` | evidência histórica/observacional sustentada por fonte identificável |
| `[H]` | hipótese/modelo/analogia testável, ainda não promovida |
| `[TV]` | `TOKEN_VAZIO`: evidência/entidade/operador insuficiente |
| `[R]` | formulação rejeitada/corrigida por conflitar com o modelo ou evidência |

`TOKEN_VAZIO != 0`. Ausência de evidência não é evidência negativa nem valor numérico zero.

## 2. Núcleo geométrico formal já existente

### 2.1 Triângulo / hexágono

`[F]`

```text
h = √3/2 = sin(60°) = cos(30°)
```

Para a base complexa

```text
τ = exp(iπ/3) = 1/2 + i√3/2
Λ = Z + τZ
```

a rede `Λ` é triangular/hexagonal. Com vetores unitários `e1=(1,0)` e `e2=(1/2,√3/2)`, a matriz de Gram é

```text
G = [[1,1/2],[1/2,1]]
det(G)=3/4
sqrt(det(G))=√3/2
```

Logo `√3/2` é também a área da célula fundamental do paralelogramo unitário de 60°.

### 2.2 Toro complexo e toro computacional

`[F]`

```text
T_complex = C / Λ
```

O toro geométrico real já implementado no produtor `ChipQuantum` permanece separado:

```text
X(u,v)=((R+r cos v)cos u,(R+r cos v)sin u,r sin v)
```

com

```text
d_min=R-r
d_med=R
d_max=R+r
```

e mapa de retorno linear declarado

```text
P(v)=v+2π(ω_v/ω_u) mod 2π
```

Referências internas:
- `ChipQuantum/src/geometry/sqrt3_geometry_matrix/RAFAELIA_GEOMETRY_MATRIX.md`
- `ChipQuantum/src/geometry/sqrt3_geometry_matrix/TORUS_SPHERE_POINCARE_MATRIX.md`
- `Mapa/indices/POINCARE_BALL_7D_FEDERATED_MAP.md`

### 2.3 Quadrado + triângulo

`[F]`

```text
45° - 30° = 15°
sin(15°)=(√6-√2)/4
cos(15°)=(√6+√2)/4
```

O campo algébrico natural da composição `√2`/`√3` é `Q(√2,√3)`. Trocas de sinal são conjugações algébricas; não devem ser descritas como “apagar número”.

## 3. Do binário a 4, 8 e 12 sem extrapolação histórica

`[F]`

```text
|{0,1}^1| = 2
|{0,1}^2| = 4
|{0,1}^3| = 8
4×3 = 12
```

`[H]` A decomposição de quatro marcos sazonais em três fases (`início/meio/fim`) gera 12 setores como MODELO DE INDEXAÇÃO contemporâneo.

`[TV]` Não há, neste delta, evidência de que Stonehenge, Gizé, Cusco ou outra civilização tenha derivado seus calendários pelo operador específico `4×3` acima.

## 4. Calendário orbital: igual ângulo != igual tempo

`[F]` Para órbita Kepleriana elíptica com excentricidade `e>0`, dividir a elipse em 12 ângulos geométricos iguais NÃO produz, em geral, 12 intervalos de tempo iguais.

No modelo kepleriano:

```text
M = E - e sin(E)
```

onde `M` é anomalia média e cresce uniformemente com o tempo no problema de dois corpos ideal. `E` é anomalia excêntrica. Portanto:

```text
equal_true_angle != equal_time      (e > 0, em geral)
```

Essa distinção é um falsificador obrigatório para qualquer calendário geométrico baseado apenas em setores angulares.

## 5. Solstícios e equinócios

`[F/E]` No calendário astronômico sazonal há dois solstícios e dois equinócios por ano tropical, totalizando quatro marcos sazonais principais.

`[R]` Formulação “quatro solstícios” corrigida para `2 solstícios + 2 equinócios`.

`[H]` Esses quatro marcos podem ser usados como quatro âncoras de um modelo 4×3=12, mas isso é uma parametrização moderna até que uma fonte histórica demonstre o mesmo procedimento para um sítio/cultura específicos.

## 6. Precessão, declinação e Órion

`[F/E]` Declinação é coordenada celeste, não mecanismo de deriva temporal. A mudança secular do céu observado envolve principalmente:

- precessão axial terrestre (~26 kyr na aproximação usual);
- nutação em escalas menores;
- movimento próprio das estrelas;
- para a órbita terrestre, também existe precessão apsidal em outra escala.

Assim, uma configuração como Órion pode reaparecer aproximadamente em ciclos anuais no céu sazonal, mas suas coordenadas relativas a sistemas ligados ao equador/equinócio mudam em escalas históricas por precessão, e estrelas possuem movimento próprio.

Fontes de referência:
- NASA Science, Reference Systems: https://science.nasa.gov/learn/basics-of-space-flight/chapter2-1/
- NASA Science, Milankovitch cycles: https://science.nasa.gov/science-research/earth-science/milankovitch-orbital-cycles-and-their-role-in-earths-climate/

## 7. Ledger arqueoastronômico

### 7.1 Stonehenge

`[E]` English Heritage registra que o eixo principal das pedras se relaciona aos solstícios: nascer do Sol do solstício de verão no eixo NE e pôr do Sol do solstício de inverno no sentido oposto.

`[E/R]` A mesma fonte afirma não haver evidência de que os construtores marcassem os pontos médios de primavera/outono; portanto “Stonehenge prova um calendário de 4 estações/equinócios” NÃO é promovido.

Fonte: https://www.english-heritage.org.uk/visit/places/stonehenge/history-and-stories/understanding-stonehenge/

### 7.2 Grande Pirâmide / Gizé

`[E]` A orientação astronômica das pirâmides do Antigo Império é objeto de literatura científica. Kate Spence propôs alinhamento ao norte por trânsito simultâneo de duas estrelas circumpolares e modelou a precessão para cronologia.

Fonte: Kate Spence, Nature 408, 320–324 (2000), DOI `10.1038/35042510`: https://www.nature.com/articles/35042510

`[H]` A hipótese de correlação entre as três principais pirâmides e o Cinturão de Órion é controversa e não é equivalente ao resultado de orientação cardinal.

`[TV]` Intenção arquitetônica precisa de mapear Órion, época exata do suposto mapa e função cosmológica dos eixos/“tubos” permanecem não demonstradas neste ledger.

### 7.3 Pedra dos Doze Ângulos — Cusco

`[E]` Existe a Pedra dos Doze Ângulos em Cusco/Hatun Rumiyoc, inserida em alvenaria inca/palácio histórico.

`[TV]` Função calendárica, astronômica ou derivação geométrica por 12 setores NÃO foi demonstrada pelas fontes lidas neste delta. O número 12 na geometria da pedra não pode ser promovido a calendário por coincidência numérica.

### 7.4 “Shichokawa”

`[TV:ENTITY_UNRESOLVED]` A grafia/nome fornecida não foi resolvida com confiança para uma entidade arqueológica inequívoca. Preservar literal; não corrigir por adivinhação.

## 8. Einstein / “lençol” gravitacional

`[R/H]` A analogia moderna de uma superfície deformada pode ajudar a intuição sobre curvatura, mas monumentos antigos NÃO constituem evidência de conhecimento de equações de campo de Einstein. Qualquer ponte aqui é `ANALOGOUS_TO`, nunca `IDENTICAL_TO`, salvo nova evidência histórica independente.

## 9. Kähler / 7D — fronteira dimensional

`[F]` Uma variedade Kähler ordinária tem dimensão real par. Portanto “7D Kähler” diretamente é inválido no sentido ordinário.

`[H]` Rota testável possível:

```text
M^7 Sasakian → cone C(M)^8 Kähler
M^7 3-Sasakian → cone C(M)^8 hyper-Kähler
```

Aplicar isso à geometria RAFAELIA exige métricas, formas diferenciais e condições de integrabilidade explícitas; até lá, `TOKEN_VAZIO_SPECIFIC_MODEL`.

## 10. Matriz 7×7 de auditoria — governança, não teorema

Esta grade é um operador de cobertura operacional.

| Direção \ Gate | Evidência | Fórmula | Contraexemplo | Falsificador | Gap | Rota | Próximo gate |
|---|---|---|---|---|---|---|---|
| Geometria | fonte/derivação | equações | forma rival | erro geométrico | TV | F/O | teste numérico |
| Astronomia | efeméride | coordenadas | época rival | residual angular | TV | O/T | simulação epoch-aware |
| Calendário | registro | periodicidade | calendário rival | erro temporal | TV | L/O | reconstrução |
| Arqueologia | contexto | medidas | sítio rival | proveniência | TV | L/O | fonte primária |
| Computação | receipt | algoritmo | implementação rival | bit/error gate | TV | T | reprodução |
| Epistemologia | classe | regra | claim rival | contradição | TV | O | revisão |
| Proveniência | source_id | hash/id | fonte independente | custody break | TV | L/T | receipt |

## 11. Rotas L/O/T materializadas

### L: `L:AGC-20260828`

```text
source literals
→ formalização geométrica pré-existente
→ pesquisa histórica/astronômica 2026-08-28
→ correções de terminologia
→ ledger de claims
→ próximos gates
```

Não apagar as formulações anteriores; registrar correção por delta.

### O: `O:AGC-20260828`

Eixos independentes obrigatórios:

```text
O1 provenance          = source/DOI/instituição
O2 identity_integrity  = path/hash/arquivo
O4 measurement         = azimute/ângulo/epoch/erro
O5 semantic_symbolic   = metáfora separada de evidência
O6 science_claim       = hipótese + falsificador
O7 governance          = ATLAS/gaps/next gate
```

### T: `T:AGC-20260828`

Pontes permitidas:

```text
geometry ↔ astronomy      via angular/metric models
astronomy ↔ calendar      via time/epoch/season definitions
archaeology ↔ astronomy   via measured site orientation + dated context
geometry ↔ computation    via tested operators/fixtures
history ↔ computation     via reconstruction, never automatic causality
```

Ponte sem evidência nos dois lados permanece `[H]/[TV]`.

## 12. Genesis Seal como identidade, não segredo

Artefato público:

`Mapa/file_000000002e20820ebc7eb4567c469138.png`

Pode atuar como `public identity anchor/domain separator`. Não deve atuar como chave secreta por estar publicamente acessível.

## 13. Gates seguintes

1. `AGC-G1`: resolver ou preservar definitivamente `Shichokawa` como entidade não resolvida.
2. `AGC-G2`: levantar coordenadas/azimutes/horizonte de cada sítio com fonte arqueológica.
3. `AGC-G3`: reconstruir céu por época com precessão/nutação/movimento próprio e registrar modelo/epoch.
4. `AGC-G4`: comparar `equal-angle` versus `equal-time` em órbita elíptica e quantificar erro por 12 setores.
5. `AGC-G5`: separar alinhamento observado de intenção cultural documentada.
6. `AGC-G6`: criar fixtures negativos para coincidência numérica `12`, `4×3`, `8`, `√3/2`.
7. `AGC-G7`: somente promover ponte histórico-matemática se houver evidência independente em ambos os domínios.

## 14. Retroalimentação

`F_ok`: relações geométricas e astronômicas formais foram separadas de evidência histórica; Stonehenge solsticial e orientação astronômica de pirâmides têm fontes identificadas.  
`F_gap`: intenção de Órion, função calendárica da Pedra dos Doze Ângulos e entidade “Shichokawa” permanecem abertas.  
`F_next`: efemérides epoch-aware + medidas de sítio + fontes arqueológicas primárias + fixtures de falsificação.
