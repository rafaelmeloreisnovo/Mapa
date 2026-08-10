# Geometria de Área Assinada e Triangulação Reversível — V1

Status: `EXPERIMENTAL_GOVERNED`

`claim_allowed=false` para qualquer alegação de novidade matemática, equivalência geral com composição de Gauss, ou invariância além das identidades demonstradas abaixo.

## 1. Núcleo

A construção usa quatro operações:

1. **decompor** uma figura em triângulos;
2. **transportar** parcelas de área sem alterar a soma total;
3. **recompor** as parcelas em retângulos/quadrados equivalentes;
4. **inverter** a transformação quando o operador admite inversa.

O invariante primário é a área orientada total:

\[
A_{total}=\sum_i \sigma_i A_i,\qquad \sigma_i\in\{-1,+1\}.
\]

Uma operação é aceita como conservativa quando:

\[
\Delta A=A_{depois}-A_{antes}=0
\]

dentro de tolerância numérica declarada.

## 2. Isósceles como dobradiça

Para base `b`, lados iguais `l` e altura `h`:

\[
h=\sqrt{l^2-(b/2)^2},\qquad A=bh/2.
\]

A altura divide o isósceles em dois triângulos retângulos congruentes:

\[
(b/2)^2+h^2=l^2.
\]

Isso fornece uma ponte direta entre triangulação e Pitágoras.

## 3. Operadores de escala

Definimos:

\[
S_{30}(L)=\frac{\sqrt 3}{2}L,
\qquad
S_{30}^{-1}(L)=\frac{2}{\sqrt3}L.
\]

Logo:

\[
S_{30}^{-1}(S_{30}(L))=L.
\]

Também:

\[
S_2(L)=\sqrt2L,
\qquad
S_2^{-1}(L)=\frac{L}{\sqrt2}.
\]

Dois passos de `S30` eliminam o radical:

\[
S_{30}^2(L)=\frac34L.
\]

Esse par oferece progressão/regressão geométrica reversível.

## 4. Área emprestada e completar quadrados

O mecanismo geométrico de "emprestar área" é modelado por transferência assinada:

\[
A_1'=A_1-\delta,\qquad A_2'=A_2+\delta,
\]

portanto:

\[
A_1'+A_2'=A_1+A_2.
\]

Para completar o quadrado:

\[
x^2+bx=\left(x+\frac b2\right)^2-\left(\frac b2\right)^2.
\]

A parcela `(b/2)^2` é adicionada para fechar o quadrado e descontada no balanço total.

## 5. Bhaskara como recomposição quadrática

Partindo de:

\[
ax^2+bx+c=0,
\]

com `a != 0`, completar quadrados conduz a:

\[
\left(x+\frac{b}{2a}\right)^2=\frac{b^2-4ac}{4a^2}
\]

e, para discriminante não negativo,

\[
x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}.
\]

O discriminante

\[
\Delta=b^2-4ac
\]

é registrado como invariante algébrico do problema quadrático, sem promover automaticamente equivalência com qualquer teoria de classes de formas quadráticas.

## 6. Transformações de área

Para transformação linear `T` no plano:

\[
A(T(F))=|\det T|A(F).
\]

Portanto, a classe de transformações com

\[
|\det T|=1
\]

preserva área. Um cisalhamento

\[
T=\begin{pmatrix}1&k\\0&1\end{pmatrix}
\]

tem `det(T)=1` e é reversível por

\[
T^{-1}=\begin{pmatrix}1&-k\\0&1\end{pmatrix}.
\]

## 7. Contrato de validação

Cada experimento deve produzir:

- parâmetros de entrada;
- área antes/depois;
- erro absoluto de conservação;
- operador e inversa usada;
- `PASS`, `FAIL` ou `TOKEN_VAZIO`;
- `claim_allowed=false` até evidência independente quando houver alegação nova.

## 8. Hipóteses abertas

`TOKEN_VAZIO`:

- fechamento periódico sob composições mistas de `sqrt(2)`, `sqrt(3)/2`, `pi` e inversas;
- relação não trivial entre essas órbitas geométricas e classes de formas quadráticas;
- existência de invariantes adicionais além de área orientada e determinante.

Esses pontos são perguntas de pesquisa, não resultados estabelecidos.
