# Cruzamento Tipado V2 — Poincaré × Quadrática × Pitágoras × Modularidade × TOKEN_VAZIO

**Data:** 2026-09-14  
**Estado:** DRAFT_AUDITABLE / FAIL_CLOSED  
**Autoridade:** Mapa / IGC-CR-20260802-V1  
**claim_allowed:** false

## 1. Regra-mãe

```text
valor != representação != geometria != topologia != proveniência != evidência
TOKEN_VAZIO != 0 != classe-resíduo [0]_m != conjunto vazio ∅
```

Este V2 preserva o núcleo fértil do cruzamento, mas remove promoções indevidas por analogia.

## 2. Correções formais obrigatórias

### 2.1 7/3 e 77/33

Como números racionais:

[
\frac73 = \frac{77}{33}.
]

Não existe uma geometria diferente apenas porque a fração foi escrita com fator comum 11. O que pode ser diferente é a **representação com proveniência**:

```text
RatRep(7,3)   = value 7/3, scale=1
RatRep(77,33) = value 7/3, scale=11
```

Logo `77/33 != (7/3)*11`. O fator 11 pertence aos metadados da representação; não ao valor reduzido.

### 2.2 Zero modular

`70 mod 7 = 0` é um resultado determinado. Portanto não é `TOKEN_VAZIO`.

Para preservar história:

[
n = qm+r,qquad 0\le r<m.
]

Guardar `(q,r,m)`, não apenas `r`. Exemplo: `70 = 10*7 + 0`.

### 2.3 Poincaré

No disco unitário padrão com curvatura gaussiana `K=-1`:

[
ds^2=\frac{4(dx^2+dy^2)}{(1-x^2-y^2)^2}.
]

O modelo é **conforme**: preserva ângulos localmente. O desenho euclidiano distorce distâncias/escala, não os ângulos hiperbólicos medidos no modelo.

Geodésicas são diâmetros ou arcos de circunferência ortogonais ao bordo.

A curvatura gaussiana é constante `-1`; ela não fica "mais negativa" perto da borda. O fator métrico diverge e a borda está a distância hiperbólica infinita:

[
d(0,r)=\log\frac{1+r}{1-r}=2\operatorname{artanh}(r).
]

Para triângulo hiperbólico em `K=-1`:

[
A=\pi-(\alpha+\beta+\gamma).
]

A fórmula de Gauss–Bonnet em região com bordo exige os termos de bordo; `∫K dA = 2πχ` sozinho não se aplica a uma região arbitrária com bordo.

### 2.4 Bhaskara / equação quadrática

[
\Delta=b^2-4ac.
]

`Δ<0` implica raízes complexas conjugadas. Isso **não** implica geometria hiperbólica.

O plano complexo usual `ℂ` é euclidiano quando equipado com a métrica `|z_1-z_2|`. Multiplicar por `i` representa rotação de 90° nesse plano.

Pontos `2+3i, 2+6i, 2+9i` são colineares e equiespaçados por 3; isso não cria simetria rotacional 3-fold.

### 2.5 Pitágoras + rotação

Uma isometria euclidiana preserva comprimentos e, portanto:

[
a^2+b^2=c^2.
]

O triângulo `(3,6√2,9)` é válido. O que gira são as coordenadas vetoriais; comprimentos laterais não precisam "trocar de variável" em 90°.

### 2.6 "3-6-9 / Tesla"

`3,6,9` pode ser mantido como **namespace simbólico/projeto** ou como classes aritméticas declaradas.

Não promover automaticamente:
- múltiplo de 3 -> simetria geométrica 3-fold;
- múltiplo de 9 -> propriedade física/frequencial;
- autoria/proveniência Tesla sem fonte primária.

`TESLA_PROVENANCE = TOKEN_VAZIO` enquanto não houver fonte primária pinada.

### 2.7 Triângulo, hexágono e círculo

Número de lados pode parametrizar um polígono regular, mas número não possui geometria intrínseca.

Dois triângulos equiláteros centrados e invertidos formam um **hexagrama**; a interseção contém um hexágono central.

Um hexágono regular de lado `a` possui:

[
A_{hex}=\frac{3\sqrt3}{2}a^2
=6\left(\frac{\sqrt3}{4}a^2\right),
]

isto é, seis vezes a área do triângulo equilátero de mesmo lado, não três vezes.

A interseção genérica de dois hexágonos congruentes com rotação de 45° não é automaticamente um quadrado.

Rotacionar um triângulo retângulo 45-45-90 em torno da hipotenusa não produz um quadrado 2D.

### 2.8 Círculo -> esfera

- circunferência rotacionada em torno de um diâmetro -> superfície esférica;
- disco rotacionado em torno de um diâmetro -> bola sólida.

### 2.9 Toro

O toro padrão de revolução é gerado rotacionando uma **circunferência** de raio menor `r`, cujo centro está a distância maior `R` do eixo:

[
x=(R+r\cos v)\cos u,;
y=(R+r\cos v)\sin u,;
z=r\sin v.
]

Área `4π²Rr`; volume `2π²Rr²` para o toro anelar.

Rotacionar uma coroa circular produz em geral uma casca/volume toroidal distinto, não o mesmo gerador de uma circunferência.

No toro de revolução embutido em `R³`, deslocar `u` é simetria axial contínua. Deslocar `v` não é em geral uma rotação ambiente independente equivalente. Portanto `∞-fold × ∞-fold` precisa de um modelo explícito.

### 2.10 Toro -> esfera geodésica

Subdivisão/refinamento não muda topologia:

[
χ(T^2)=0,qquad χ(S^2)=2.
]

Logo uma malha triangular de toro não converge topologicamente a uma esfera apenas por subdivisão. É necessária uma transformação que mude a colagem/topologia.

### 2.11 Matriz 10x10 em toro discreto

Wraparound define a topologia periódica. O número de vizinhos depende da regra de adjacência:
- von Neumann -> 4;
- Moore -> 8.

"Toroidal" sozinho não implica oito vizinhos.

## 3. Compressão reconstruível

Não usar:

```text
lista -> resíduo modular único
```

porque módulo é many-to-one.

Usar:

```text
value
+ representation/provenance
+ generator/rule
+ quotient/winding/index
+ residual
+ dictionary/version
```

Isso é compressão por estrutura/referência. Não é violação de Shannon.

## 4. Tipos mínimos

```text
Scalar(x)
RatRep(p,q,scale)
Residue(r,m)
Winding(q)
Rotation(theta)
SymmetryOrder(n)
EuclideanShape(X)
HyperbolicShape(X,K)
Quadratic(a,b,c,delta,root_space)
Topology(beta0,beta1,beta2,chi)
Epistemic(KNOWN | TOKEN_VAZIO(reason))
```

Misturar tipos exige operador de ponte explícito.

## 5. Invariantes realmente preserváveis

- rotação euclidiana -> distância, ângulo, área;
- similaridade -> ângulo e razões;
- quociente modular -> classe-resíduo, não identidade original;
- redução racional -> valor racional, não representação original;
- subdivisão de uma mesma superfície -> topologia;
- Poincaré -> curvatura `K=-1`, conformalidade e geodésicas do modelo.

## 6. Falsificadores

1. Se `77/33` for tratado como `(7/3)*11`, teste falha.
2. Se `0 mod 7` virar `TOKEN_VAZIO`, teste falha.
3. Se `Δ<0` promover `HYPERBOLIC`, teste falha.
4. Se o disco `K=-1` omitir o fator 4 sem declarar outra normalização, teste falha.
5. Se subdivisão pura declarar `T² -> S²`, teste falha.
6. Se módulo sozinho alegar preservar histórico, teste falha.

## 7. R3

**F_ok:** igualdade racional, resíduo modular, Poincaré, quadrática, rotação e topologia foram separados por tipo.

**F_gap:** proveniência primária de "Tesla 3-6-9", mapa explícito triângulo/hexágono/círculo como projeções de uma entidade comum e algoritmo de compressão empiricamente medido permanecem `TOKEN_VAZIO`.

**F_next:** executar fixtures determinísticas; depois medir reconstruibilidade/compressão contra baseline explícito.
