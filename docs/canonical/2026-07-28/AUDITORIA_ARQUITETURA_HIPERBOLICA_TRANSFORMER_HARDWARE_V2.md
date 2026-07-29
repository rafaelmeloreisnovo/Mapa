# Auditoria da Arquitetura Hiperbólica, Transformer e Hardware — V2

**Data:** 2026-07-28  
**Estado:** `CANONICAL_AUDIT`  
**claim_allowed:** `false`  
**Execução runtime nesta etapa:** `NÃO`

Documento longitudinal integral no Google Drive:

- [RAFAELIA — Auditoria Matemática da Arquitetura Hiperbólica, Transformer e Hardware — V2](https://docs.google.com/document/d/128f4oUJ7f8IoHHOFXDgvjFhJRJgFFhrhkQLM3nnpGng)

## 1. Veredito

A formulação auditada contém componentes matemáticos legítimos e um núcleo aplicável, mas ainda não constitui teoria unificada nem solução universal pronta para física, IA e silício.

```text
FRAMEWORK_CONCEITUAL_PROMISSOR
+ NÚCLEO_HIPERBÓLICO_CORRIGÍVEL
+ CLAIMS_NÃO_DEMONSTRADOS
```

A separação obrigatória é:

```text
DEMONSTRAÇÃO ≠ CONVENÇÃO ≠ HIPÓTESE ≠ PARÁBOLA ≠ TOKEN_VAZIO
```

## 2. Núcleo aproveitável

- fatoração matricial `T = ΦΨ`;
- recorrência de Tribonacci;
- grafo de coprimalidade;
- distância geodésica no disco de Poincaré;
- atenção baseada em distância;
- otimização Riemanniana;
- localidade de cache como objetivo mensurável;
- máscaras explícitas para dados ausentes;
- separação entre geometria, computação, hardware e evidência.

## 3. Correções invariantes

### 3.1 Minkowski

Primeiro deve ser extraído um único vetor:

\[
x_0=g_0(T),\qquad
\mathbf{x}=[g_1(T),\ldots,g_7(T)]^T.
\]

Depois se impõe, normaliza ou demonstra:

\[
x_0^2-\|\mathbf{x}\|^2=1,\qquad x_0>0.
\]

A igualdade não nasce automaticamente da multiplicação matricial.

### 3.2 Hiperboloide para Poincaré

A projeção coerente é:

\[
\mathbf{p}=\frac{\mathbf{x}}{x_0+1},
\qquad
\mathbf{p}\in\mathbb{R}^7,
\qquad
\|\mathbf{p}\|<1.
\]

A construção anterior de sete vetores com oito componentes não produz diretamente um ponto em `D⁷`.

### 3.3 Raio não é entropia

`r(t) → r∞ ∈ (0,1)` demonstra no máximo limitação e convergência radial. Não prova organização da entropia, preservação de informação ou coerência semântica.

Devem ser medidos separadamente:

- raio;
- deslocamento geodésico;
- perda da tarefa;
- entropia definida sobre distribuição explícita;
- estabilidade sob perturbações.

### 3.4 Lorentz

O boost precisa atualizar o par temporal-espacial:

\[
\begin{bmatrix}x_0'\\x_1'\end{bmatrix}
=
\begin{bmatrix}\cosh\xi&\sinh\xi\\\sinh\xi&\cosh\xi\end{bmatrix}
\begin{bmatrix}x_0\\x_1\end{bmatrix}.
\]

`ξ` é rapidez adimensional. Os números `3,6,9` podem parametrizar discretização autoral, mas não constituem mecanismo físico de Tesla sem evidência.

### 3.5 Mudança de base

`diag(1,2,…,8)` não representa por si só conversão entre bases 2, 20 e 60. São necessários contratos de largura, ordem dos dígitos, carry, overflow e representação canônica.

```text
B₂→₂₀ = TOKEN_VAZIO_DEFINITION
B₂₀→₆₀ = TOKEN_VAZIO_DEFINITION
```

### 3.6 Grafo

O conjunto fornecido contém compostos e o número `1`; portanto, o nome correto é **grafo de coprimalidade**, não grafo de primos.

## 4. Correção decisiva do TOKEN_VAZIO

No disco de Poincaré, `p = 0` não produz distância infinita:

\[
d_{\mathbb D}(0,q)=2\operatorname{artanh}(\|q\|),
\]

que é finita para `||q|| < 1`.

Logo:

```text
TOKEN_VAZIO ≠ VETOR_ZERO ≠ ZERO_OBSERVADO
```

A máscara deve atuar explicitamente nos logits:

\[
\ell_{ij}=-d_{\mathbb D}(p_i,p_j)/\tau+M_{ij},
\]

com `Mᵢⱼ = 0` para token válido e `Mᵢⱼ = -∞` para posição mascarada.

## 5. Hardware

### Cache

`CMR ≈ 1/√N` não é lei geral. Três matrizes `8×8` de `float32` ocupam aproximadamente 768 bytes, normalmente pequenas para L1 após aquecimento.

```text
CMR_REAL = TOKEN_VAZIO_MEASUREMENT
```

A taxa real depende de layout, alinhamento, linha, associatividade, stride, prefetch, conflitos e concorrência.

### DMB

`DMB` é barreira de ordenação de memória. Não é flush universal, validação numérica ou coerência matemática global.

A modelagem adequada é uma relação de ordem:

\[
W_A \prec_{DMB} W_B.
\]

## 6. Perda e ética

Uma barreira geométrica mais segura que `max(0,r−1)²` é:

\[
L_{geo}=-\mu\log(1-\|p\|^2+\varepsilon).
\]

Os hiperparâmetros não garantem ética.

```text
RESTRIÇÃO_GEOMÉTRICA ≠ GARANTIA_ÉTICA
```

A ética permanece em contrato próprio: finalidade, proveniência, privacidade, abstinência, revisão humana, falsificadores e rollback.

## 7. Verdade e abstinência

Centralidade geométrica não equivale a verdade. A decisão epistemológica deve combinar evidência, contradição, incerteza e extrapolação. Abaixo do limiar definido:

```text
resultado = TOKEN_VAZIO
```

## 8. Lagrangiano original

A expressão original mistura campo físico, atenção, cache, ética e dado empírico sem compatibilidade dimensional.

- `log det(A)` pode não existir;
- cache miss dividido por largura de banda não é densidade de energia;
- `δ(r−0,5)` é uma restrição distributiva, não simples registro de medição;
- `r=0,5` exige receipt, incerteza e ambiente.

Sem receipt:

```text
r_empírico = 0,5 → TOKEN_VAZIO_EVIDENCE
```

## 9. Arquitetura corrigida

\[
\mathfrak{R}=\langle\mathcal{G},\mathcal{A},\mathcal{H},\mathcal{E}\rangle
\]

- `G`: geometria hiperbólica;
- `A`: atenção com máscara explícita;
- `H`: hardware medido em cycles, misses, joules e bytes;
- `E`: fonte, método, teste, falsificador, receipt e estado.

```text
receipt ausente ⇒ claim_allowed=false
```

## 10. Próximo artefato autorizado

```text
T
→ extração (x₀,x)
→ normalização no hiperboloide
→ projeção p∈D⁷
→ distância hiperbólica
→ máscara explícita
→ softmax estável
→ testes de invariantes
→ receipt local
```

Testes mínimos:

1. norma de Minkowski dentro da tolerância;
2. `||p|| < 1−ε`;
3. atenção nula nas posições mascaradas;
4. linhas válidas somam 1;
5. ausência de `NaN/Inf`;
6. round-trip hiperboloide ↔ disco;
7. benchmark separado da correção matemática;
8. `claim_allowed=false` até receipt verificável.

## R₃

- **F_ok:** geometria hiperbólica, atenção por distância e otimização Riemanniana formam um núcleo útil.
- **F_gap:** projeção, máscara, Lorentz, bases, cache, DMB, ética e Lagrangiano estavam misturados.
- **F_next:** materializar o núcleo geométrico mínimo no `RafPolimata`, com testes, hashes e receipt local.

FIAT LUX · Ω = Amor
