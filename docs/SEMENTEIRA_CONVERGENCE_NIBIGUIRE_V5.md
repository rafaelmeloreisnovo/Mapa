# SEMENTEIRA — Convergência, NIBIGUIRE e Knee de Desenvolvimento — V5

**Data:** 2026-09-05  
**Estado:** `LOCAL_DETERMINISTIC_CLOSURE / FIXED_POINT_REACHED / EXTERNAL_GAPS_PRESERVED`  
**Autoridade:** Mapa controla contexto, custódia, classificação e próximo gate; não substitui prova física.

## 1. Objetivo

Esta camada responde a um problema recorrente: a cada nova rodada apareciam relações que já eram deriváveis do material existente, mas não estavam explicitamente registradas. Em vez de continuar por acumulação textual, V5 define uma auditoria de completude com critério de parada.

Fluxo:

```text
fonte da Sementeira
→ subgrafo pertinente
→ lacunas candidatas
→ separar NIBIGUIRE de TOKEN_VAZIO
→ fechar somente o determinístico
→ medir ganho por esforço
→ repetir
→ parar no fixed point
```

## 2. NIBIGUIRE

`NIBIGUIRE` é tratado como **termo autoral do usuário**, não como conceito acadêmico externo.

Definição operacional:

> relação estrutural omitida cuja origem, ingredientes e prova já estão presentes no estado consultado e que pode ser fechada sem introduzir fato externo.

Critérios:

1. ingredientes já existem;
2. a relação é derivável/testável;
3. a omissão perde semântica, dinâmica ou contexto;
4. existe artefato/prova mínima para fechamento.

Logo:

```text
NIBIGUIRE != TOKEN_VAZIO
```

Um `TOKEN_VAZIO` exige dado, execução, autorização ou definição que ainda não existe. Se uma suposta NIBIGUIRE não puder ser fechada, ela é roteada para `TOKEN_VAZIO` tipado.

## 3. Matriz fixa de cobertura

A cobertura não é medida pelo tamanho do texto. É medida por:

```text
8 domínios × 7 eixos = 56 células
```

Domínios:

1. escala `77:33 ↔ 7:3`;
2. equilátero/círculo/quadrado do 14;
3. dobra e height-lift mod 7/mod 14;
4. Fibonacci/Rafaeliana e alturas;
5. icosfera e altitude geodésica;
6. namespaces 7/42/70/420/T7;
7. federação do Projeto Sementeira;
8. convergência/NIBIGUIRE.

Eixos:

```text
origem/proveniência
semântica/namespace
fórmula exata
testemunho numérico
implementação executável
teste/evidência
boundary/negative gate
```

## 4. Fechamentos determinísticos V5

Foram catalogados 27 candidatos.

```text
20 = NIBIGUIRE localmente fecháveis
7  = gaps que exigem definição/evidência externa
```

A cadeia fechável inclui:

- preservação de escala de `77:33` versus `7:3`;
- escala dimensional `11, 121, 1331`;
- lado 14, altura `7√3`, triângulo medial lado 7;
- quadrado `7√2` com diagonal 14;
- círculo circunscrito e razões de área;
- operador `H_m,R(x,y) = √3 R sin(π d_m(x,y)/m)`;
- embedding exato `H_14,R(2x,2y)=H_7,R(x,y)`;
- espectro de alturas Fibonacci mod 7;
- isometria relacional de alturas da Rafaeliana;
- altitudes esféricas da icosfera;
- altura cordal `√3 R/(2φ)`;
- escala logarítmica `Δln M_D=D ln s`;
- distinção entre zero numérico, domínio log inválido e TOKEN_VAZIO;
- Project Sementeira como contexto e não evidência;
- matriz de cobertura;
- cálculo marginal de ganho/esforço;
- fixed point de fechamento.

## 5. Curva observada da auditoria

O motor não atribui peso subjetivo a linhas de código. Uma unidade de esforço é uma inspeção de candidato numa rodada; uma unidade de ganho é um fechamento determinístico novo com dependências satisfeitas.

| rodada | candidatos inspecionados | ganho | esforço/ganho |
|---:|---:|---:|---:|
| 1 | 27 | 6 | 4.5 |
| 2 | 21 | 8 | 2.625 |
| 3 | 13 | 3 | 4.3333 |
| 4 | 10 | 2 | 5 |
| 5 | 8 | 1 | 8 |
| 6 | 7 | 0 | ∞ |

A rodada 5 já produz somente **uma nova unidade estrutural para oito inspeções**. Na rodada 6, uma nova passagem completa encontra zero fechamento local:

`ΔG=0`, portanto `ΔE/ΔG → ∞`.

Esse é o ponto de convergência adotado.

## 6. Relação com a analogia SPL

A analogia do usuário é uma **régua de saturação de engenharia**: chegar a uma região em que grande aumento de sistema produz ganho marginal mínimo.

Ela não é usada como identidade acústica. Em acústica ideal:

`+1 dB => P2/P1=10^0.1≈1.258925`,

e duplicar potência corresponde a `10 log10(2)≈3.0103 dB`.

Em competição SPL real, limitações eletromecânicas, térmicas, estruturais e compressão podem tornar ganhos adicionais muito mais caros. V5 usa essa imagem apenas como **critério de saturação**, não como lei de +1 dB.

## 7. Modelo contínuo auxiliar

Uma curva de desenvolvimento saturante pode ser representada por:

`C(E)=C∞(1-e^(-E/τ))`,

com derivada `C'(E)=C∞ e^(-E/τ)/τ` e esforço marginal `dE/dC=τ/(C∞-C)→∞` quando `C→C∞`.

Esta curva é **modelo analítico de forma**, não medição empírica da produtividade do projeto.

## 8. Fixed point

Defina o operador local de fechamento `C(S)=S ∪ {relações determinísticas prováveis a partir de S}`.

V5 encerra quando `C(S*)=S*`.

O motor atingiu esse estado para a lista de candidatos declarada: nenhum `LOCAL_DETERMINISTIC` permanece aberto. Isso é deliberadamente mais forte que “dobrar esforço por +1”: o próximo passe local já produz **zero** ganho.

## 9. Gaps que NÃO foram preenchidos

```text
TOKEN_VAZIO_C7_TO_42_CANONICAL_MAP
TOKEN_VAZIO_T2_TO_T7_PHYSICAL_BRIDGE
TOKEN_VAZIO_FIBONACCI_RAFAEL_REAL_DISCRETIZATION
TOKEN_VAZIO_42_PHYSICAL_ATTRACTORS
TOKEN_VAZIO_PI_PHI_PHYSICAL_CLAIM
TOKEN_VAZIO_PROVIDER_CI_V5
TOKEN_VAZIO_PHYSICAL_RUNTIME_V5
```

Esses itens não são NIBIGUIRE local. Exigem decisão autoral, experimento, CI ou runtime.

## 10. Regra nova para futuras rodadas

```text
novo item já é derivável do estado?
  sim → NIBIGUIRE → fechar e testar
  não → falta definição/evidência?
        sim → TOKEN_VAZIO tipado
        não → nova hipótese claramente marcada
```

O objetivo não é maximizar páginas, arquivos ou commits.

`objetivo = máxima cobertura verificável antes da saturação`

## R3

```text
F_ok:
  20 NIBIGUIRE determinísticas fechadas
  56 células de cobertura endereçadas
  fixed point local alcançado
  curva de esforço/ganho produzida

F_gap:
  7 gaps externos/autorais preservados

F_next:
  somente novo dado, definição, CI, runtime ou evidência
  capaz de mover um dos sete TOKEN_VAZIO restantes
```
