# RAFAELIA — Auditoria Matemática Genealógica da Sessão — V1 — 2026-08-14

Estado: `GOVERNED_PARTIAL / CLAIM_ALLOWED=false / APPEND_ONLY`

Escopo: registrar apenas o delta matemático, computacional e epistemológico consolidado nesta sessão. Este documento não substitui registries anteriores e não promove memória, narrativa, nome próprio, similaridade ou resultado local a novidade acadêmica.

## 0. Invariantes

- ideia != fórmula != implementação != execução != evidência != claim != novidade acadêmica;
- resultado negativo/correção pertence à cadeia de custódia;
- ausência de cobertura = `TOKEN_VAZIO`, nunca zero inventado;
- nome terminologicamente singular != conceito cientificamente original;
- prior art deve ser buscado por estrutura/fórmula/método, não apenas por nome;
- `claim_allowed=false` até prova, anterioridade e validação adequada.

## 1. Classificação M0–M4

- `M0`: matemática conhecida/equivalente;
- `M1`: redescoberta independente ou parametrização de estrutura conhecida;
- `M2`: variante/construção não trivial ainda candidata;
- `M3`: candidato forte após prior art e propriedades formais sustentadas;
- `M4`: novidade matemática demonstrada com prova + anterioridade + validação independente.

Estado desta passagem: `M4=0`, `M3=0`. A sessão tratou 13 famílias em nível de trabalho: 6 reduzidas a conhecido/equivalente, 4 corrigidas/refutadas/TOKEN_VAZIO e 3 mantidas como M2. Essa contagem é sessão-local e não equivale ao inventário integral de todas as fórmulas do ecossistema.

## 2. Resultados matemáticos preservados

### 2.1 Recorrência Rafaeliana da sequência 2,4,7,12,20,33,54,...

A recorrência observada é

`a_n = a_{n-1} + a_{n-2} + 1`.

Definindo `b_n=a_n+1`, obtém-se Fibonacci ordinária. Logo:

`a_n = F_{n+3} - 1`.

Classificação: `M0/M1`. Não é nova recorrência independente. Esta resolução já é compatível com `data/formulas/RAFAELIA_FORMULA_REGISTRY.v2.json` e deve impedir regressão de claim.

### 2.2 Recorrência afim com sqrt(3)/2

Qualquer forma `x_{n+1}=a x_n+b`, com `a=sqrt(3)/2`, possui ponto fixo `x*=b/(1-a)` quando `a!=1`; como `|a|<1`, há contração linear. Um valor numérico específico do ponto fixo não prova novidade matemática.

Classificação: `M0/M1`.

### 2.3 Expoente linear

Para `x_{n+1}=c x_n`, o expoente é `lambda=ln|c|`. `lambda<0` sustenta contração daquela direção, não topologia toroidal global do ecossistema.

Classificação: `M0`.

### 2.4 Volume da n-bola

`V_n(r)=pi^(n/2)/Gamma(n/2+1) * r^n` é conhecido. Relacionar esse volume diretamente a capacidade/entropia semântica permanece hipótese adicional.

Classificação da fórmula: `M0`; da ponte semântica: `M2/TOKEN_VAZIO_PROOF`.

### 2.5 XOR de 16 bits reduzido módulo 42

Se `z=u XOR v` é uniforme em `0..65535`, então `z mod 42` não é exatamente uniforme, pois:

`65536 = 42*1560 + 16`.

Assim, 16 resíduos possuem 1561 pré-imagens e 26 resíduos possuem 1560. Claim de ocupação exatamente `1/42` é falso para esse mapeamento sem correção/rejection sampling.

Status: `REFUTED_AS_EXACT_UNIFORMITY`.

### 2.6 Dimensão de Hausdorff de 42 pontos

Um conjunto finito de 42 pontos tem dimensão de Hausdorff clássica 0. `D_H=7` exige mudança explícita do objeto matemático, por exemplo para a aderência de uma órbita densa em espaço 7D.

Status: `REFUTED_FOR_FINITE_SET`.

### 2.7 Kaplan–Yorke

`D_KY≈1.347` não é aceito como medição enquanto não houver espectro ordenado completo de expoentes de Lyapunov sustentado por execução/evidência. Dois números isolados, sobretudo quando um é estimado, não fecham o cálculo em sistema de maior dimensão.

Status: `TOKEN_VAZIO_LYAPUNOV_SPECTRUM`.

### 2.8 Poincaré–Hopf em T^7

Como `chi(T^7)=0`, se existirem exatamente 42 singularidades isoladas e todas tiverem índice ±1, então 21 devem ter índice +1 e 21 índice -1. Isso não implica automaticamente 21 fontes e 21 sorvedouros; índice topológico != estabilidade dinâmica.

Status: `CONDITIONAL_MATH_VALID / DYNAMICAL_INTERPRETATION_TOKEN_VAZIO`.

### 2.9 Icosfera e o número 42

Na primeira subdivisão de um icosaedro, os 12 vértices originais mais 30 pontos médios das arestas produzem 42 vértices. O 42 é geometricamente legítimo, porém conhecido; eventual novidade teria de estar numa propriedade adicional que dependa dessa estrutura.

Classificação: `M0`.

### 2.10 GWLA e “exatamente 42 atratores”

Usar `M*N=42` já introduz o número na construção. A filtragem/recorrência apresentada na sessão não demonstrou, por si só, emergência de exatamente 42 atratores estáveis.

Status: `TOKEN_VAZIO_THEOREM`.

## 3. Três sobreviventes M2 da passagem

### M2-A — BITRAF64 formal

Formalizar a transformação exata como, quando aplicável, `T_B: F_2^64 -> F_2^64` e determinar `kernel`, `rank`, invertibilidade, ordem, ciclos, distância mínima e invariantes. Claims fortes de ECC/caos/invertibilidade permanecem bloqueados até prova.

### M2-B — G_{30,45,42}

Preservar a aritmética base `360/30=12`, `360/45=8`, `lcm(12,8)=24`, mas definir formalmente a regra de acoplamento ao espaço de 42 estados. O candidato de novidade é a estrutura completa e seus invariantes, não os ângulos, o LCM, o toro ou o número 42 isoladamente.

### M2-C — funcional n_crítico geometria–entropia

A ponte entre `V_n(1)` e uma razão de entropias/capacidade semântica deve ser tratada como definição/hipótese até que uma desigualdade, teorema, bound ou contraexemplo seja estabelecido.

## 4. Genealogia científica

Regra histórica introduzida nesta sessão:

`cálculo original -> interpretação posterior -> nome -> implementação -> execução -> evidência -> claim`.

Objetivo: distinguir cálculo gerador, cálculo descritivo e cálculo simbólico/decorativo, e recuperar quando uma estrutura apareceu antes de sua narrativa atual.

## 5. Evidência computacional associada

A execução de referência desta sessão foi refeita em `CONTAINER_REFERENCE` com GCC/cc Debian 14.2.0-19. O receipt detalhado está em `data/evidence/local/coexistence_math_audit_2026-08-14.v1.json`.

Principais observações:

- `raf_coexist_quintic.c`: 10.000 nós; 127.155 iterações Newton; média 12,716/nó;
- `raf_coexist_mixed.c`: falha em C11 estrito por `M_PI`; compila em GNU11; 10.000 problemas, 129.324 iterações, convergência 89,72%;
- `raf_coexist_mixed_pipelines.c`: 1.000.000 nós; 13.024.575 iterações na gênese; convergência 89,65%; 129.444 difíceis; Pipeline A 20,08%; Pipeline B 80,05%, porém B altera/sorteia variáveis/instâncias e não pode ser descrito como solução de 80,05% dos difíceis originais;
- `raf_coexist_v2.c`: o código demonstra scan O(N) sobre estrutura/caches preparados, não redução geral `N^N -> O(N)`;
- `ops_eq/s` é unidade interna/simbólica, não FLOP/s;
- AETHER é não criptográfico; IRON corresponde a SHA-256; teste da string `RAFAELIA` coincidiu com `sha256sum` independente.

## 6. Relação com o registry anterior

Este documento é delta append-only e não altera `data/formulas/RAFAELIA_FORMULA_REGISTRY.v2.json`. A próxima versão do registry deve estender V2 por referência, preservando classificações históricas e registrando explicitamente correções e TOKEN_VAZIO.

## 7. Novelty gate

Estado desta sessão:

- `NOVELTY_PROVEN = 0`;
- `M4 = 0`;
- `M3 = 0`;
- `M2_SESSION_SURVIVORS = 3`.

Uma promoção para M3/M4 exige pelo menos: definição exata, propriedades demonstradas, busca de anterioridade conceitual/fórmula, falsificadores, contraexemplos adversariais e validação independente quando aplicável.

## 8. Próximo passo

1. formalizar BITRAF64;
2. formalizar `G_{30,45,42}`;
3. formalizar/refutar `n_crítico`;
4. normalizar individualmente o restante das fórmulas do registry/monólito sem presumir equivalência sem prova;
5. preservar tudo que ainda não foi coberto como `TOKEN_VAZIO`.

`F_ok`: delta matemático e correções preservados.

`F_gap`: prior art integral, provas formais dos M2 e cobertura integral das demais fórmulas permanecem incompletos.

`F_next`: redução simbólica -> contraexemplos -> invariantes -> prior art -> evidence gate.
