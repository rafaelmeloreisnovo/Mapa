# Auditoria do Motor Hiperbólico para Deep Learning e Falsificabilidade — V1

## Evento

```text
event_id: AUDIT-MOTOR-HYPERBOLIC-DL-FALSIFIABILITY-V1-20260728
source: sessão Sementeira / síntese executiva e auditoria subsequente
state: CANONICAL_RECLASSIFICATION
claim_allowed: false
append_only: true
merge_automatic: false
```

## Objetivo

Registrar no Mapa a topologia epistemológica do motor experimental de cinco estágios, separando:

```text
especificação
!= implementação
!= teste estrutural
!= evidência empírica
!= robustez certificada
!= prova científica
```

Este evento não substitui a autoridade matemática do `papers #30`. O `Mapa #88` registra estados, relações, dependências e próximos gates.

---

## Nós principais

```text
MHDL-SOURCE
MHDL-SPEC
MHDL-ENCODER
MHDL-GEOMETRY
MHDL-ATTENTION
MHDL-MEMORY
MHDL-LOSS
MHDL-FALSIFIER
MHDL-EVIDENCE
MHDL-REVIEW
MHDL-DECISION
MHDL-MEMORY-EVENT
```

## Cordas tipadas

```text
MHDL-SOURCE       --derived_into-->       MHDL-SPEC
MHDL-SPEC         --defines-->            MHDL-ENCODER
MHDL-SPEC         --defines-->            MHDL-GEOMETRY
MHDL-SPEC         --defines-->            MHDL-ATTENTION
MHDL-SPEC         --defines-->            MHDL-MEMORY
MHDL-SPEC         --defines-->            MHDL-LOSS
MHDL-SPEC         --requires-->           MHDL-FALSIFIER
MHDL-FALSIFIER    --produces_or_refutes--> MHDL-EVIDENCE
MHDL-EVIDENCE     --reviewed_by-->         MHDL-REVIEW
MHDL-REVIEW       --authorizes_or_blocks-->MHDL-DECISION
MHDL-DECISION     --appends-->             MHDL-MEMORY-EVENT
```

Nenhuma corda `defines`, `implemented_by`, `tested_by` ou `supported_by` deve ser interpretada automaticamente como causalidade ou prova.

---

## Estados canônicos

| Objeto | Estado |
|---|---|
| motor de cinco estágios | `FORMAL_SPEC_V0_2` |
| implementação executável | `TOKEN_VAZIO_CODE` |
| injetividade BLENDDIGS | `TOKEN_VAZIO_INJECTIVITY_PROOF` |
| Lambda igual a um | `CONSTRAINT_GEOMETRIC_ONLY` |
| raio menor que um | `DOMAIN_MEMBERSHIP_ONLY` |
| raio 0.5 como atrator | `TOKEN_VAZIO_ATTRACTOR` |
| token vazio como vetor zero | `REFUTED_AS_WRITTEN` |
| log-log como barreira infinita | `REFUTED_AS_BARRIER` |
| Caputo como preservação integral | `TOKEN_VAZIO_INFORMATION_PRESERVATION` |
| Reclusão convergindo a zero | `TOKEN_VAZIO_BOUNDARY_FUNCTIONAL` |
| imunidade adversarial pelo disco | `REFUTED_AS_WRITTEN` |
| certificado Lipschitz local | `CONDITIONAL_MATHEMATICAL_STATEMENT` |
| superioridade hiperbólica | `TOKEN_VAZIO_EMPIRICAL` |
| CI estrutural | `TOKEN_VAZIO_CI` / `STRUCTURAL_TEST_ONLY` |
| revisão independente | `TOKEN_VAZIO_REVIEW` |

---

## Invariantes que não podem ser quebradas

1. `TOKEN_VAZIO` não pode ser convertido em vetor geométrico zero.
2. Pertencimento à bola não pode ser promovido a estabilidade ou verdade.
3. Falsificabilidade científica não pode ser confundida com vulnerabilidade adversarial.
4. Teste estrutural não pode ser promovido a evidência empírica.
5. O conjunto final de teste não pode calibrar pesos, limiares ou escolha de arquitetura.
6. Resultados negativos e ataques bem-sucedidos devem ser preservados como evidência.
7. Cada claim precisa apontar para fonte, método, falsificador, ambiente e receipt.

---

## Gates M0–M10

```text
M0  domínio e contrato da entrada
M1  codificador e máscara explícita
M2  decodificador/roundtrip e colisões
M3  normalização hiperbólica e tolerâncias
M4  atenção finita e ausência de vazamento da máscara
M5  memória Caputo comparada com baseline recorrente
M6  perda, barreira e Reclusão bem tipadas
M7  baseline euclidiana congelada
M8  ataques FGSM, PGD e ataque Riemanniano
M9  avaliação fora da amostra, ablações e receipt
M10 revisão independente e decisão de promoção
```

### Regra de avanço

```text
M(n+1) só abre quando M(n) possui:
origem + contrato + teste + resultado + hash + falsificador
```

O fracasso em qualquer gate não encerra o programa. Ele produz estado tipado e `F_next` verificável.

---

## Falsificadores mínimos

A hipótese de vantagem hiperbólica é rejeitada ou rebaixada quando ocorrer qualquer uma das condições:

- não superar ou não igualar a baseline pelo critério pré-registrado;
- robustez limpa obtida à custa de degradação não declarada;
- ataque Riemanniano encontrar perturbações menores que o raio alegadamente certificado;
- vazamento da máscara de ausência;
- resultados desaparecerem em ablação de curvatura;
- ganho depender de seleção posterior do conjunto de teste;
- custo computacional invalidar a comparação;
- receipt não reproduzir os resultados.

---

## Autoridades

```text
Google Drive                 = memória editorial e origem
Mapa #88                    = estados, topologia, gates e custódia
papers #30                  = formulação matemática e ledger de claims
RafPolimata/implementação   = código e receipts futuros
RLL                         = somente quando existir hipótese científica e protocolo de dados adequado
revisores independentes     = gate de reprodução e promoção
```

O RLL não deve receber este motor como modelo físico antes de existir objeto observável, hipótese nula, dados, unidades e likelihood específicos.

---

## R3

### F_ok

- motor preservado como especificação;
- sobreclaims reclassificados;
- cordas e autoridades declaradas;
- gates M0–M10 definidos;
- falsificadores mínimos registrados;
- `claim_allowed=false` mantido.

### F_gap

- implementação;
- fixtures;
- baselines;
- ataques;
- dados fora da amostra;
- calibração;
- receipts;
- CI hash-bound;
- reprodução independente.

### F_next

Abrir `M0` e `M1`: congelar domínio de entrada, contrato do codificador e máscara explícita antes de implementar a geometria ou executar ataques.
