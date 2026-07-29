# Mapa federado — Projeção hiperbólica 7D \(H^7\rightarrow B^7\)

**ID:** `GEOM-PB7-20260728`  
**Estado:** `FEDERATED_DRAFT`  
**Claim global:** `claim_allowed=false`

## 1. Origem

A sessão forneceu uma matriz `C[8][8]`, uma tentativa de interpretar a linha 0 como tempo e as linhas 1–7 como espaço, e um código AArch64 freestanding para projetar o estado em um disco unitário.

A integração foi conectada ao contrato Drive ↔ GitHub registrado no documento:

```text
RAFAELIA — Implementação Latentes e Papers — Drive GitHub V1
Drive ID: 1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88
```

## 2. Delta técnico

A fórmula recebida não podia ser promovida sem correção porque:

1. as sete linhas espaciais contêm `7×8=56` valores, não sete;
2. a projeção do hiperboloide exige norma Lorentziana;
3. o denominador estrito contém `sqrt(T²-||V||²)`, não `sqrt(T²+||V||²)`;
4. as oito colunas atuais possuem delta Lorentziano negativo;
5. `raio<1` prova pertencimento ao modelo escolhido, não estabilidade física.

## 3. Invariante adotada

```text
C[8][8]
→ 8 colunas
→ 8 candidatos em R^(1,7)
→ teste delta = T² - ||V||²
→ modo T: projeção estrita, quando delta>0
→ modo L: lift canônico declarado, quando a entrada bruta não é timelike
→ ponto em B^7
```

## 4. Distribuição por responsabilidade

| Papel | Repositório | PR | Entrega |
|---|---|---:|---|
| Produtor low-level | `rafaelmeloreisnovo/ChipQuantum` | #46 | C AArch64 freestanding, `fsqrt`, syscalls, gate ELF |
| Balança científica | `instituto-Rafael/relativity-living-light` | #606 | paper, validador, resultados, claims e falsificadores |
| Síntese publicável | `rafaelmeloreisnovo/papers` | #29 | manuscrito, ledger, referências e custódia |
| Controle federado | `rafaelmeloreisnovo/Mapa` | esta branch | registro, estados, relações e próximos gates |

## 5. Estado factual

| Objeto | Estado |
|---|---|
| Multiplicação `C=A×B` | `PASS` |
| Interpretação por coluna `1+7` | `PASS` |
| Matriz bruta no hiperboloide | `FAIL_PRECONDITION_SPACELIKE` |
| Saída de projeção estrita | `TOKEN_VAZIO_INPUT_NOT_TIMELIKE` |
| Lift canônico | `PASS_COMPUTATIONAL_EMBEDDING` |
| Oito raios `<1` | `PASS` |
| Cross-build ELF AArch64 | `PASS` |
| Execução Termux AArch64 | `TOKEN_VAZIO` |
| Estabilidade física | `TOKEN_VAZIO` |
| Cosmologia | `PROHIBITED_BY_SCOPE` |

## 6. Evidência numérica

```text
checks: 8/8 PASS
scale: 3472
strict_timelike_columns: 0
canonical_lift_columns: 8
radius_min: 0.14217227697372437
radius_max: 0.5960178971290588
```

## 7. Relações semânticas

```text
Poincare_ball
  is_model_of → hyperbolic_geometry
  is_not → Poincare_return_map
  is_not → Poincare_recurrence
  is_not → Poincare_conjecture

canonical_lift
  produces → valid_H7_point
  does_not_prove → raw_matrix_lorentzian

radius_less_than_one
  proves → ball_membership
  does_not_prove → physical_stability
```

## 8. Próximo gate verificável

```text
PB7-G1
executar tools/build_poincare_7d_aarch64.sh no Termux AArch64
preservar:
  receipt.json
  output.txt
  source_sha256
  binary_sha256
  ABI/dispositivo
```

Depois:

```text
PB7-G2 = comparação bit a bit com o validador independente
PB7-G3 = fixture realmente timelike para ativar modo T
PB7-G4 = boost de Lorentz + distância hiperbólica
```

Para rotações gerais 7D, o mapa recomenda planos de Givens ou estruturas `SO(7)`/`Spin(7)`. Quaterniões isolados ficam restritos a subespaços apropriados e não cobrem todo o grupo de rotações sete-dimensional.

## 9. Retroalimentação

`F_ok`: conceito transformado em código, prova matemática, resultado negativo, paper e registro federado.  
`F_gap`: execução nativa Android e fixtures timelike permanecem abertas.  
`F_next`: produzir receipt Termux e comparar os oito registros IEEE-754.
