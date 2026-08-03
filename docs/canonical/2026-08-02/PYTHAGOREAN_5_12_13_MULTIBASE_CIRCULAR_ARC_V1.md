# Descoberta no corpus — 5–12–13, quadrado anterior 144 e arco circular multibase

**ID:** `PYTH-5-12-13-MULTIBASE-ARC-V1`  
**Data:** `2026-08-02`  
**Modo:** `APPEND_ONLY / NON_DESTRUCTIVE / FAIL_CLOSED`  
**Autoridade ontológica:** `rafaelmeloreisnovo/Mapa`  
**Estado:** `MATH_EXACT + MODEL_DELIMITED + DATASET_REPRODUCIBLE`  
**Claim global:** `claim_allowed=false`

## 1. Correção que vira descoberta no corpus

O triângulo retângulo exato é:

\[
5^2+12^2=25+144=169=13^2.
\]

O ponto novo para o corpus não é apenas substituir `15` por `13`. O número
`144` é o quadrado imediatamente anterior a `169`, e o intervalo entre esses
dois quadrados também é um quadrado:

\[
\boxed{13^2-12^2=169-144=25=5^2}.
\]

Classificação epistemológica:

| Registro | Estado |
|---|---|
| `5² + 12² = 13²` | `PROVADO_ARITMETICAMENTE` |
| `144 = 12²` é o quadrado anterior a `169 = 13²` | `PROVADO_ARITMETICAMENTE` |
| o intervalo `169 − 144` é `25 = 5²` | `PROVADO_ARITMETICAMENTE` |
| novidade | `DISCOVERY_IN_CORPUS`; identidade clássica, sem alegação de novidade matemática mundial |

### 1.1 Família geral

Para todo inteiro ímpar positivo `a`, defina:

\[
b=\frac{a^2-1}{2},
\qquad
c=\frac{a^2+1}{2}.
\]

Então `b` e `c` são consecutivos e:

\[
a^2+b^2=c^2,
\qquad
c^2-b^2=a^2.
\]

Com `a=5`:

\[
(a,b,c)=(5,12,13).
\]

Portanto, o padrão `quadrado anterior + quadrado-intervalo = quadrado
seguinte` pertence a uma família infinita de ternas pitagóricas, e o caso
`25 + 144 = 169` é sua instância `a=5`.

## 2. Preservação do 15 sem promovê-lo a hipotenusa

O valor proposto `15` não satisfaz a igualdade euclidiana:

\[
15^2-(5^2+12^2)=225-169=56.
\]

Ele permanece no registro por duas leituras condicionais, que não podem ser
misturadas:

1. **Modelo de incertezas correlacionadas**

   \[
   225=25+144+2\rho(5)(12)
   \quad\Longrightarrow\quad
   \rho=\frac7{15}.
   \]

2. **Modelo de terceira componente ortogonal**

   \[
   u_{oculto}=\sqrt{225-169}=\sqrt{56}\approx7{,}4833147735.
   \]

Ambos são `MODELO_CONDICIONAL`. Sem variável observável, unidade, mecanismo,
dataset e falsificador, qualquer interpretação física permanece
`TOKEN_VAZIO_PHYSICAL_MEANING`.

## 3. Todas as bases coexistem sem alterar o valor

Para base inteira posicional `b >= 2`:

\[
n=\sum_{k=0}^{m}d_kb^k,
\qquad 0\le d_k<b.
\]

A escrita muda; o inteiro não. Por isso a identidade exata sobrevive em toda
base:

\[
\operatorname{eval}_b(5_b)^2+
\operatorname{eval}_b(12_b)^2=
\operatorname{eval}_b(13_b)^2.
\]

O artefato reprodutível materializa as bases inteiras positivas de `1` até
`225`. O gerador é paramétrico para toda base inteira `b >= 2`. O limite `225`
foi escolhido porque é o maior valor acompanhado; acima dele, todos os valores
do conjunto são algarismos únicos, embora suas posições angulares continuem
paramétricas.

| Estado | Tratamento correto |
|---|---|
| `∅` | marcador epistemológico/semântico; não é radix numérico |
| base `0` | não possui representação posicional convencional única |
| base `1` | escrita unária; não posicional; círculo quociente trivial |
| bases `b >= 2` | sistemas posicionais inteiros cobertos pela fórmula e pelo gerador |
| bases negativas, balanceadas, não inteiras ou complexas | `TOKEN_VAZIO_RADIX_SCOPE` nesta versão |

### 3.1 Amostra de representações coexistentes

| Base | `5` | `12` | `13` | `15` |
|---:|---:|---:|---:|---:|
| 1 | `1×5` | `1×12` | `1×13` | `1×15` |
| 2 | `101₂` | `1100₂` | `1101₂` | `1111₂` |
| 5 | `10₅` | `22₅` | `23₅` | `30₅` |
| 7 | `5₇` | `15₇` | `16₇` | `21₇` |
| 10 | `5₁₀` | `12₁₀` | `13₁₀` | `15₁₀` |
| 12 | `5₁₂` | `10₁₂` | `11₁₂` | `13₁₂` |
| 13 | `5₁₃` | `C₁₃` | `10₁₃` | `12₁₃` |
| 15 | `5₁₅` | `C₁₅` | `D₁₅` | `10₁₅` |
| 20 | `5₂₀` | `C₂₀` | `D₂₀` | `F₂₀` |

| Base | `25 = 5²` | `144 = 12²` | `169 = 13²` | `225 = 15²` |
|---:|---:|---:|---:|---:|
| 2 | `11001₂` | `10010000₂` | `10101001₂` | `11100001₂` |
| 5 | `100₅` | `1034₅` | `1134₅` | `1400₅` |
| 7 | `34₇` | `264₇` | `331₇` | `441₇` |
| 10 | `25₁₀` | `144₁₀` | `169₁₀` | `225₁₀` |
| 12 | `21₁₂` | `100₁₂` | `121₁₂` | `169₁₂` |
| 13 | `1C₁₃` | `B1₁₃` | `100₁₃` | `144₁₃` |
| 15 | `1A₁₅` | `99₁₅` | `B4₁₅` | `100₁₅` |
| 20 | `15₂₀` | `74₂₀` | `89₂₀` | `B5₂₀` |
| 25 | `10₂₅` | `5J₂₅` | `6J₂₅` | `90₂₅` |

Para bases maiores que 36, o dataset usa algarismos numéricos entre colchetes,
evitando inventar um alfabeto. Exemplo:

```text
144₁₀ = [2][24]₆₀
169₁₀ = [2][49]₆₀
225₁₀ = [3][45]₆₀
```

## 4. Posição dentro do arco circular

Há três círculos distintos. Eles são registrados separadamente para impedir
uma coincidência de notação de virar falsa equivalência.

### 4.1 Círculo literal de graus

\[
\theta_{360}(n)=n\bmod360\quad\text{graus}.
\]

Como todos os valores analisados são menores que 360, suas posições são:

| Valor | Posição |
|---:|---:|
| 5 | `5°` |
| 12 | `12°` |
| 13 | `13°` |
| 15 | `15°` |
| 25 | `25°` |
| 144 | `144°` |
| 169 | `169°` |
| 225 | `225°` |

### 4.2 Círculo de 60 posições

Seguindo o anexo do ciclo de 60:

\[
\theta_{60}(n)=6^\circ(n\bmod60).
\]

| Valor | Resíduo em 60 | Posição angular |
|---:|---:|---:|
| 5 | 5 | `30°` |
| 12 | 12 | `72°` |
| 13 | 13 | `78°` |
| 15 | 15 | `90°` |
| 25 | 25 | `150°` |
| 144 | 24 | `144°` |
| 169 | 49 | `294°` |
| 225 | 45 | `270°` |

Aqui aparece uma identidade própria do arco de 60 posições:

\[
\boxed{\theta_{60}(144)=144^\circ}.
\]

No intervalo `0 <= n < 360`, os marcadores inteiros que preservam o próprio
número como ângulo são:

\[
\{0,72,144,216,288\}.
\]

Logo, `144` é um ponto fixo exato dessa transformação discreta; isto é uma
identidade aritmética do modelo circular, não uma frequência física.

### 4.3 Círculo próprio de cada base

Para cada base `b >= 2`, a posição canônica é:

\[
C_b(n)=e^{2\pi i(n\bmod b)/b},
\qquad
\theta_b(n)=360^\circ\frac{n\bmod b}{b}.
\]

Dois valores caem no mesmo ponto exatamente quando:

\[
C_b(x)=C_b(y)
\iff
x\equiv y\pmod b
\iff
b\mid(x-y).
\]

## 5. A descoberta do aliasing circular

A projeção circular preserva resíduos, mas perde voltas inteiras. Por isso ela
pode esconder um erro euclidiano.

O erro quadrático do `15` é:

\[
225-169=56.
\]

Assim, `13²` e `15²` ocupam o mesmo ponto circular exatamente nas bases
inteiras não triviais que dividem `56`:

\[
\boxed{b\in\{2,4,7,8,14,28,56\}}.
\]

Nessas bases:

\[
25+144\equiv169\equiv225\pmod b.
\]

Portanto, um teste apenas modular produziria um falso positivo para `15`.
Esse resultado é classificado como `PROJECTION_ALIASING_PROVED`, e não como
validação da terna `5–12–15`.

### 5.1 O colapso triplo da base 7

Em base 7:

\[
5\equiv12\pmod7,
\]

\[
25\equiv144\equiv4\pmod7,
\]

\[
169\equiv225\equiv1\pmod7.
\]

A base 7 faz coexistirem três apagamentos:

- os dois catetos ocupam o mesmo ponto;
- seus quadrados ocupam o mesmo ponto;
- o quadrado correto `169` e o quadrado proposto `225` ocupam o mesmo ponto.

Isto formaliza o ruído do observador/receptor: uma projeção de baixa resolução
pode preservar a coerência interna do arco e, ao mesmo tempo, destruir a
capacidade de distinguir os valores originais.

### 5.2 Bases 5, 12, 13 e 25

| Base | Estrutura observada no arco |
|---:|---|
| 5 | `144` e `169` coincidem no resíduo `4`; `25` está na origem |
| 12 | `144` está na origem; `25` e `169` coincidem no resíduo `1` |
| 13 | `25 ≡ −1`, `144 ≡ +1` e `169 ≡ 0`; o somatório fecha na origem |
| 25 | `25` está na origem; `144` e `169` coincidem no resíduo `19` |

Essas simetrias são propriedades dos quocientes `Z/bZ`. Elas não substituem a
igualdade em `Z` nem a geometria euclidiana.

## 6. Regra de interpretação

```text
valor inteiro != numeral escrito
igualdade exata != coincidência modular
posição no arco != distância euclidiana
aliasing != validação
modelo de incerteza != mecanismo físico demonstrado
```

O gate correto é duplo:

\[
\text{PASS}=
\text{igualdade exata em }\mathbb Z
\land
\text{comportamento projetado declarado em }\mathbb Z/b\mathbb Z.
\]

Se somente a segunda parte passar, o estado é `MODULAR_ALIAS_ONLY`.

## 7. Artefatos reprodutíveis

```text
docs/canonical/2026-08-02/PYTHAGOREAN_5_12_13_MULTIBASE_CIRCULAR_ARC_V1.md
tools/generate_pythagorean_multibase_arc.py
tests/geometry/test_pythagorean_multibase_arc.py
data/geometry/pythagorean_5_12_13_multibase_arc.v1.jsonl
data/geometry/geometric_invariants.delta.20260802.pythagorean_multibase_arc.jsonl
data/geometry/geometric_invariants.index.jsonl (registro anexado)
data/latents/deltas/latents.20260802.pythagorean_multibase_arc.jsonl
data/latents/latents.index.jsonl (registro anexado)
receipts/geometry/PYTHAGOREAN_MULTIBASE_ARC_20260802_RECEIPT_V1.json
```

O JSONL contém:

- manifesto e distinção `∅ / 0 / 1 / b>=2`;
- valores `5, 12, 13, 15, 25, 144, 169, 225`;
- dígitos, resíduos e ângulos racionais em cada base de `1` a `225`;
- prova computacional da identidade correta em todas as bases materializadas;
- bases nas quais o erro `56` desaparece por aliasing modular.

## 8. Proveniência

- Extende `IGC-CR-20260802-V1`, sem alterar seu contrato fail-closed.
- Cruza o anexo `RafPolimata/docs/ANEXO_CICLO_60_BASES_144_0_1HZ.md`.
- Origem de sessão: correção `5–12–15 -> 5–12–13`, triângulos do emissor e
  receptor, incerteza conjunta, distância entre centros e retroalimentação.
- `144` é preservado explicitamente como `previous_square`.

## R3

- **F_ok:** a correção foi elevada a identidade geral, representação multibase,
  posições circulares e teste determinístico; o aliasing de `15` foi localizado.
- **F_gap:** bases negativas/não inteiras, dados perceptivos reais e significado
  físico permanecem `TOKEN_VAZIO`.
- **F_next:** executar o mesmo gerador no Termux físico, anexar receipt de ABI e
  cruzar o mapa circular com um dataset real de emissor–canal–receptor.

\[
\boxed{
144\xrightarrow{+25}169,
\quad
25=5^2,
\quad
\text{arco preserva posição, mas pode ocultar identidade}
}
\]

🌀 Ruído entendido virou aliasing mensurável; correção preservada virou descoberta auditável.
