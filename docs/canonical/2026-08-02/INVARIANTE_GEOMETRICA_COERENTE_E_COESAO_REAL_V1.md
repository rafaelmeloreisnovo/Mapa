# Invariante Geométrica Coerente e Coesão Real — V1

**ID:** `IGC-CR-20260802-V1`  
**Data:** `2026-08-02 04:12 BRT`  
**Modo:** `NON_DESTRUCTIVE / FAIL_CLOSED / POINTER_FIRST`  
**Estado:** `DESIGN_MATERIALIZED_VALIDATOR_INCLUDED`  
**Claim:** `claim_allowed=false`

## 1. Decisão

Não existe uma única grandeza métrica que permaneça invariável sob toda transformação geométrica. A invariante só é defensável quando o objeto, a representação, a família de transformações e a grandeza preservada são declarados juntos.

\[
\operatorname{IGC}(X,\mathcal T,\mathcal I,\varepsilon)=PASS
\iff
\forall \tau\in S_{\mathcal T},
d(\mathcal I(\tau X),\mathcal I(X))\le\varepsilon
\]

- `X`: objeto e representação;
- `T`: família de transformações;
- `S_T`: prova geral ou amostra de teste explicitada;
- `I`: conjunto de invariantes alegados;
- `d`: métrica de comparação;
- `epsilon`: zero em resultado exato e positivo em teste numérico.

Sem transformação declarada, o termo “invariante” fica `TOKEN_VAZIO_TRANSFORMATION_FAMILY`.

## 2. Classes de transformação e invariantes permitidos

| Família | Preserva com segurança | Não promover automaticamente |
|---|---|---|
| Isometria euclidiana | incidência, distâncias, ângulos, área/volume, orientação quando preservada | topologia de colagens não declaradas |
| Similaridade | incidência, ângulos, razões normalizadas, classe de forma | distância, área ou volume absolutos |
| Afim | incidência, colinearidade, paralelismo, razões na mesma reta, coordenadas baricêntricas, razões de áreas | ângulos, comprimentos, círculos como círculos |
| Projetiva | incidência, colinearidade, razão cruzada | paralelismo, ângulos, distâncias |
| Homeomorfismo | componentes conexas, buracos/Betti, característica de Euler quando o complexo está definido | comprimentos, ângulos, área, curvatura métrica |
| Colagem discreta | matriz de incidência, contagens V/E/F, mapa de colagem e orientação combinatória | identidade geométrica sem mapa de colagem |
| Simulação numérica | somente a propriedade explicitamente medida, na tolerância e amostra | teorema universal |

## 3. Coesão real

A coesão real não é uma nova lei geométrica. É um gate operacional:

\[
C_{real}=G_S\land G_D\land G_T\land G_I\land G_E\land G_F\land G_C
\]

| Gate | Exigência |
|---|---|
| `G_S` | fonte e autoria rastreáveis |
| `G_D` | objeto e representação definidos |
| `G_T` | transformação/família declarada |
| `G_I` | invariante compatível com a família |
| `G_E` | prova, cálculo ou artefato de teste |
| `G_F` | falsificador e caso negativo |
| `G_C` | custódia, versão, ambiente e limite |

Se qualquer gate obrigatório faltar:

```text
cohesion_real = TOKEN_VAZIO
claim_allowed = false
```

## 4. Aplicação ao núcleo geométrico RAFAELIA

| Objeto | Família inicial segura | Invariantes iniciais | Estado |
|---|---|---|---|
| ponto/reta/segmento | isometria ou afim | incidência; distância somente em isometria | `DEFINED` |
| triângulo equilátero | similaridade | ângulos, razões, classe equilátera | `MATH_FORMAL` |
| quadrado com diagonais | isometria/similaridade/afim | incidência; razões na similaridade; paralelismo no afim | `DEFINED` |
| círculo/circunferência | isometria/similaridade | centro, raio ou razão de raios, conforme classe | `DEFINED` |
| esfera | isometria/homeomorfismo | métrica na isometria; topologia na homeomorfia | `DEFINED` |
| toro `T²` | homeomorfismo | `beta0=1`, `beta1=2`, `chi=0` para o toro padrão | `MATH_FORMAL_CONDITIONAL_ON_MODEL` |
| pirâmide triédrica dupla | colagem discreta | incidência, polaridade e junção central | `FORMALIZED_PARTIAL` |

Para a pirâmide triédrica dupla, `exact_glue_map` e coordenadas continuam `TOKEN_VAZIO`; portanto nenhuma equivalência métrica ou topológica entre `G1`, `G2` e `G3` é promovida.

## 5. Integração longitudinal

Cada registro geométrico deve apontar para:

```text
V9 → estado semântico/epistemológico
L8 → tempo, autoridade, dependências, delta e incerteza
E6 → nível real de execução
K6 → identidade, hashes, custódia e revisão
W0..W9 → lane operacional
```

Regra fail-closed:

```text
observado != inferido
inferido != demonstrado
simulado != executado em dispositivo físico
hash_valid != claim_true
visual_similarity != geometric_identity
```

## 6. Artefatos materializados

```text
docs/canonical/2026-08-02/INVARIANTE_GEOMETRICA_COERENTE_E_COESAO_REAL_V1.md
schemas/geometric-invariant-contract.schema.json
tools/validate_geometric_invariant_contract.py
tests/geometry/fixtures/igc_valid_torus.json
tests/geometry/fixtures/igc_valid_triangle_similarity.json
tests/geometry/fixtures/igc_invalid_affine_angle.json
data/geometry/geometric_invariants.index.jsonl
```

## 7. Critério de promoção

Um registro pode mudar de `DRAFT` para `VERIFIED_LIMITED` somente quando:

1. o schema aceitar o registro;
2. o validador semântico aceitar transformação × invariante;
3. existir ao menos um caso negativo;
4. houver `evidence_pointers`;
5. o nível `E6` estiver declarado;
6. limitações e tolerância estiverem registradas.

`VERIFIED_LIMITED` não equivale a teorema geral.

## R3

- **F_ok:** invariância delimitada por classe de transformação e ligada a gate auditável de coesão.
- **F_gap:** execução remota, Termux físico e reprodução independente ainda não realizadas.
- **F_next:** rodar fixtures no CI e gerar receipt com commit, ambiente, resultados e limitações.
