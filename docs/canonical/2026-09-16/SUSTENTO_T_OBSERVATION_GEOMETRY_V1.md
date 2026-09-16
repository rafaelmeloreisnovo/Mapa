# SUSTENTO^T — Gate de evidência, janela 3-4-5 e geometria de observação V1

**ID:** `SUSTENTO-T-OBS345-20260916-V1`  
**Data:** 2026-09-16  
**Estado:** `RESEARCH_FORMALIZATION / IMPLEMENTED_UNTESTED`  
**claim_allowed:** `false`

## 0. Fronteira

Este delta continua a rota `OBS345-SQRT3` e transforma a intuição de "entrada–meio–fim / yin–yang / √3÷2 / vazio" em um contrato matemático testável.

```text
SOURCE != ARTEFATO != EXECUCAO != EVIDENCIA != CLAIM
OBSERVACAO != ESTADO_FISICO_COMPLETO
TOKEN_VAZIO != 0
EMPTY_SET != TOKEN_VAZIO
FRIDA_OBSERVER != MISSION_AUTHORITY
```

O literal `sus_ento^T` é preservado como alias de origem. A forma canônica deste artefato é `SUSTENTO^T`. Partes não semanticamente resolvidas do literal original permanecem `TOKEN_VAZIO_SEMANTIC`; não são completadas por invenção.

## 1. Vetor de sustentação

Defina o vetor:

\[
G=(P,C,E,K,U,R,B)\in[0,1]^7
\]

onde:

- \(P\): proveniência;
- \(C\): contexto;
- \(E\): evidência;
- \(K\): contradição residual;
- \(U\): incerteza;
- \(R\): reprodução;
- \(B\): rollback/reversibilidade.

Os componentes efetivos de suporte são:

\[
G^+=(P,C,E,1-K,1-U,R,B)
\]

e o escore diagnóstico:

\[
S_T=\left(\prod_{i=1}^{7}G_i^+\right)^{1/7}.
\]

**Importante:** \(S_T\) não é probabilidade de verdade. É apenas um agregador diagnóstico condicionado à definição dos sete eixos.

A decisão exige um limiar explicitamente fornecido \(\tau\):

\[
PASS \iff \min(G^+)\ge\tau.
\]

Se qualquer eixo obrigatório estiver ausente, o resultado é `TOKEN_VAZIO_GATE_INPUT`. Nenhum limiar universal é declarado.

A ação condicional é:

\[
A_{cond}=
\begin{cases}
EXECUTE\_AUTHORIZED,& PASS\land authority=true\\
HOLD,& otherwise.
\end{cases}
\]

O hash SHA-256 do receipt canônico funciona como **chave de custódia do portão**, não como chave criptográfica de autorização.

## 2. Janela temporal normalizada

Para \([t_{in},t_{out}]\):

\[
m=(t_{in}+t_{out})/2,\quad T=t_{out}-t_{in},\quad
u=\frac{2(t-m)}{T}.
\]

Stencil 3 pontos:

\[
U_3=\{-1,0,+1\}.
\]

Stencil 4 pontos equidistantes:

\[
U_4=\{-1,-1/3,+1/3,+1\}.
\]

Stencil 5 pontos:

\[
U_5=\{-1,-1/2,0,+1/2,+1\}.
\]

Isso modela entrada/meio/saída ou janelas instrumentais; não implica trajetória clássica predeterminada de partícula.

## 3. Estados e vazio

Fenômeno binário candidato:

\[
X\in\{0,1\}.
\]

Registro epistemológico:

\[
E\in\{0,1,\varnothing_{\text{evid}}\}.
\]

Neste artefato:

- `0` = valor zero/YIN;
- `1` = valor um/YANG;
- `EMPTY_SET` = conjunto matematicamente vazio;
- `TOKEN_VAZIO` = informação necessária ausente/indeterminada;
- `CONTRADICTED` = evidências incompatíveis preservadas.

Nunca converter `TOKEN_VAZIO` silenciosamente em 0.

## 4. Decisão 3-4-5

Maioria 2-de-3:

\[
M_3=1\iff N_1\ge2,\quad M_3=0\iff N_0\ge2.
\]

Com quatro leituras, empate 2-2 é:

\[
M_4=\varnothing_{TIE}.
\]

Gate forte 4-de-5:

\[
G_{4/5}=1\iff N_1\ge4,\quad
G_{4/5}=0\iff N_0\ge4,
\]

senão `TOKEN_VAZIO_INSUFFICIENT_CONSENSUS`.

Sob erro IID por leitura \(p\):

\[
P_{err}(M_3)=3p^2-2p^3,
\]

\[
P_{err}(M_5)=10p^3-15p^4+6p^5,
\]

\[
P_{wrong}(U_4,\ abstain\ on\ tie)=4p^3-3p^4,
\]

\[
P_{tie}(U_4)=6p^2(1-p)^2,
\]

\[
P_{wrong}(G_{4/5})=5p^4-4p^5,
\]

\[
P_{abstain}(G_{4/5})=10p^2(1-p)^2.
\]

Estas identidades são condicionais a independência e mesmo \(p\); não são probabilidades físicas universais.

## 5. Spiral √3/2 como refino

\[
r=\frac{\sqrt3}{2},\quad r^2=\frac34.
\]

Janelas concêntricas:

\[
W_n=[m-\frac{T}{2}r^n,\ m+\frac{T}{2}r^n].
\]

Logo \(\operatorname{width}(W_n)=Tr^n\) e \(W_{n+1}\subset W_n\) para \(T>0\).

Identidade determinística já preservada:

\[
r^6=\frac{27}{64},\qquad
1-r^6=\frac{37}{64},\qquad
(1-r^6)-r^6=\frac5{32}.
\]

Isto é matemática da regra de escala; interpretação física continua `TOKEN_VAZIO`.

## 6. Triângulo, estrela de seis pontas e base curva

Triângulo equilátero de lado \(a\):

\[
h=\frac{\sqrt3}{2}a,\qquad
A=\frac{\sqrt3}{4}a^2.
\]

Medianas, alturas, bissetrizes e mediatrizes coincidem no equilátero.

Para triângulo geral, mediana relativa ao lado \(a\):

\[
m_a=\frac12\sqrt{2b^2+2c^2-a^2}.
\]

Isósceles com lados iguais \(l\) e base \(b\):

\[
h=\sqrt{l^2-(b/2)^2}.
\]

Uma estrela de seis pontas é modelável como sobreposição de dois triângulos equiláteros opostos. Isso é uma construção geométrica, não identidade com Ba Gua.

Para substituir uma base reta de corda \(c\) por arco circular de raio \(\rho\):

\[
\theta=2\arcsin\frac{c}{2\rho},\quad
s=\rho-\sqrt{\rho^2-(c/2)^2}.
\]

A altura ao arco pode ser registrada explicitamente como \(h_{eff}=h\pm s\), conforme a concavidade declarada. Sem orientação do arco, o sinal é `TOKEN_VAZIO_ORIENTATION`.

## 7. Hexágono, octógono e multibase

Polígono regular de \(b\ge3\), circunraio \(R\):

\[
\theta_b=\frac{2\pi}{b},\quad
c_b=2R\sin\frac{\pi}{b},\quad
a_b=R\cos\frac{\pi}{b}.
\]

No hexágono regular:

\[
c_6=R,\quad a_6=\frac{\sqrt3}{2}R.
\]

No octógono:

\[
c_8=2R\sin(\pi/8),\quad a_8=R\cos(\pi/8).
\]

Conjunto literal solicitado, preservando ordem e repetição em fonte:

\[
[7,14,9,6,3,20,13,12,20,18,2,1,5,140,10,0,\varnothing].
\]

Conjunto deduplicado de bases poligonais válidas:

\[
B=\{3,5,6,7,9,10,12,13,14,18,20,140\}.
\]

\(2,1,0,\varnothing\) recebem tratamento degenerado/epistemológico, não são promovidos a polígonos regulares usuais.

## 8. Formas 2D/3D

Coroa circular:

\[
A=\pi(R^2-r^2).
\]

Cilindro:

\[
V=\pi r^2h.
\]

Cone:

\[
V=\frac13\pi r^2h.
\]

Esfera:

\[
A=4\pi r^2,\quad V=\frac43\pi r^3.
\]

Toro \(R>r\):

\[
A=4\pi^2Rr,\quad V=2\pi^2Rr^2.
\]

Esfera geodésica icosaédrica por frequência \(f\), antes de relaxação:

\[
V_{tx}=10f^2+2,\quad E=30f^2,\quad F=20f^2.
\]

Distância geodésica em esfera de raio \(R\):

\[
d=R\arccos\left(\frac{x\cdot y}{R^2}\right).
\]

## 9. Vórtice e Venturi — domínio separado

Vórtice potencial idealizado:

\[
v_\theta(r)=\frac{\Gamma}{2\pi r}
\]

fora do núcleo e dentro das hipóteses do modelo.

Venturi ideal incompressível:

\[
A_1v_1=A_2v_2.
\]

Bernoulli só entra com suas hipóteses de escoamento. Sem ponte dimensional e observável, não misturar Venturi, vórtice, quântica e √3/2.

## 10. Álgebra, potências e trigonometria

\(x^2,\sqrt{x},x^3,\sqrt[3]{x}\) são operadores algébricos; só recebem significado geométrico/físico após domínio e unidade definidos.

Aproximação polinomial local:

\[
z(t)\approx\sum_{k=0}^{d}a_k(t-m)^k.
\]

Componente periódica:

\[
z(t)=a_0+\sum_k[a_k\cos(k\omega t)+b_k\sin(k\omega t)].
\]

Escolha de modelo deve ser feita por erro, resíduo, validação e falsificador.

## 11. Fronteira física

- Elétron ligado em átomo não é, em geral, uma esfera em órbita clássica; usa-se estado quântico e distribuição de resultados.
- O gato de Schrödinger é experimento mental sobre superposição/medição; consciência humana não é requisito matemático do modelo.
- Min/mediana/max e \(Q05,Q50,Q95\) são estatísticas de dados observados, não "trajetória escondida" garantida.
- Entrada/meio/saída em detector são janelas instrumentais definidas pelo experimento.

## 12. Frida / ATLAS

Frida permanece observador/consumidor limitado abaixo de `AuthorizedAction`.

```text
ATLAS:X
  -> EVID:X
  -> AuthorizedAction
  -> SUSTENTO^T producer receipt
  -> Frida bounded observer
  -> ProvenanceReceipt
  -> LEARN:X
```

O observador não promove claim, não infere dispositivo físico e não converte ausência em zero.

## 13. Gaps

```text
TOKEN_VAZIO_PHYSICAL_DETECTOR_DATASET
TOKEN_VAZIO_UNITS_AND_CALIBRATION
TOKEN_VAZIO_NOISE_INDEPENDENCE
TOKEN_VAZIO_QUANTUM_CAUSAL_BINDING
TOKEN_VAZIO_CURVED_STAR_ORIENTATION
TOKEN_VAZIO_BASE_SELECTION_CRITERION
TOKEN_VAZIO_FRIDA_PHYSICAL_RUNTIME
```

## R3

`F_ok`: formalização 3-4-5, score/gate 7D, refino √3/2, geometria multibase, vazio tipado e fronteira Frida/ATLAS integrados.  
`F_gap`: dados físicos, calibração, independência do ruído e causalidade física continuam abertos.  
`F_next`: executar fixtures determinísticas e noise sweep em CI; depois criar receipt Frida apenas como observador bounded, sem promoção física.
