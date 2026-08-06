# Invariante dos Operadores Cognitivos 15–70 — V1

**Estado:** `CANONICAL_DRAFT`  
**Claim gate:** `claim_allowed=false`  
**Autoridade canônica:** `rafaelmeloreisnovo/Mapa`  
**Produtor de evidência:** `rafaelmeloreisnovo/RafPolimata`  
**Destino editorial:** `rafaelmeloreisnovo/papers`

## 1. Veredito

O corpus recebido contém 56 expressões numeradas de 15 a 70. Ele não pode ser promovido como “70 derivadas operacionais” porque mistura:

- derivadas e diferenças finitas reais;
- integrais e operadores fracionários;
- métricas, distâncias, divergências e transformadas;
- equações diferenciais e fluxos geométricos;
- invariantes topológicos;
- relações de comutação e objetos de teoria de gauge;
- analogias físicas ainda sem representação cognitiva concreta.

A invariante adequada não é o nome simbólico. É o contrato:

```text
nome submetido
→ classe matemática normalizada
→ domínio
→ hipóteses
→ correção ou limite
→ falsificador
→ testes
→ estado de execução
→ próximo gate
```

## 2. Invariantes de verdade

```text
operator_name != mathematical_definition
analogy != mechanism
formal_expression != executable_model
TOKEN_VAZIO != 0
IMPLEMENTABLE != PASS
physical_label != physical_evidence
claim_allowed=false until domain, implementation, tests and evidence gates close
```

`IMPLEMENTABLE` significa apenas que há definição suficiente para construir uma implementação limitada e testável. Não significa que o código existe, executou ou passou.

`TOKEN_VAZIO` significa que a expressão foi preservada, mas faltam definições, unidades, representação, convenção ou evidência. O registro exige motivo e próximo gate.

## 3. Resultado da triagem

| Classe operacional | Quantidade | Efeito |
|---|---:|---|
| Implementável sob contrato | 33 | encaminhar por famílias para `RafPolimata` |
| `TOKEN_VAZIO` útil | 23 | permanecer no `Mapa` até fechar o gate |
| Ponte física somente semântica | 11 | proibida de virar mecanismo automaticamente |
| Total recebido | 56 | ordinais 15–70 preservados |

Estados formais observados:

| Estado | Quantidade |
|---|---:|
| `VALID` | 8 |
| `VALID_WITH_ASSUMPTIONS` | 20 |
| `VALID_WITH_CONVENTION` | 2 |
| `MISNAMED` | 10 |
| `MISCLASSIFIED` | 4 |
| `INCOMPLETE` | 7 |
| Demais estados de lacuna | 5 |

## 4. Correções estruturais mais importantes

1. **Operadores 15–17:** segunda derivada, diferença regressiva e log iterado são executáveis, mas os nomes “inversa”, “reversa” e “derivada recursiva” não descrevem precisamente o objeto.
2. **Operador 28:** a fórmula dada é direcional/Gâteaux; Fréchet exige um mapa linear limitado e resto `o(||h||)`.
3. **Operador 32:** Radon–Nikodym não é, em geral, a razão de derivadas temporais.
4. **Operador 33:** complemento de Schur exige matriz em blocos e pivô invertível.
5. **Operador 38:** a fórmula apresentada estima dimensão box-counting, não Hausdorff em geral.
6. **Operadores 40, 44, 46, 47, 51, 55, 57 e 63:** são relações, invariantes, divergências, distâncias, transformadas, funcionais ou potenciais; não derivadas.
7. **Operador 58:** corrente conservada isoladamente não implica teorema de Goldstone.
8. **Operadores 64–70:** a matemática física pode ser válida no domínio original, mas a transferência para memória/atenção permanece sem mecanismo e sem evidência.

## 5. Arquitetura no GitHub

```text
Mapa
├── data/ontology/cognitive-operators.v1.json
├── data/ontology/cognitive-operators/
│   ├── segment-015-030.v1.json
│   ├── segment-031-050.v1.json
│   └── segment-051-070.v1.json
├── scripts/validate_cognitive_operators.py
├── tests/test_cognitive_operators.py
├── docs/COGNITIVE_OPERATOR_INVARIANT_V1.md
└── .github/workflows/cognitive-operator-gate.yml
```

Responsabilidades:

- **Mapa:** definição, classificação, custódia, fronteira de claim e roteamento.
- **RafPolimata:** implementações de referência, testes analíticos, convergência e receipts.
- **papers:** síntese revisada; nunca fonte primária de execução.

## 6. Ordem de implementação no RafPolimata

A implementação deve avançar por famílias, sem tentar codificar as 56 expressões simultaneamente:

1. **Cálculo discreto e diferencial:** 15, 16, 18, 19, 24, 29, 30, 34.
2. **Geometria diferencial:** 20, 22, 27, 35, 36, 53, 54, 60, 61.
3. **Fracionário e espectral:** 23, 38, 39.
4. **Probabilidade e informação:** 41, 45–51.
5. **Gauge/topologia apenas após modelo concreto:** 40, 52, 55–59, 62, 64–70.

Cada família deverá gerar:

```text
implementation
+ analytic fixtures
+ adversarial tests
+ convergence/error metric
+ environment receipt
+ immutable commit
+ claim_allowed decision
```

## 7. Execução local

```bash
python3 -m unittest -v tests/test_cognitive_operators.py

python3 scripts/validate_cognitive_operators.py \
  --manifest data/ontology/cognitive-operators.v1.json \
  --output build/cognitive-operators/audit.json
```

O validador usa somente Python stdlib.

## 8. Limite científico

Este registro demonstra organização, tipagem e coerência estrutural. Ele não demonstra que há uma nova teoria matemática, uma arquitetura cognitiva superior, um mecanismo quântico de memória ou evidência física. Esses claims permanecem fechados.

## 9. Retroalimentação

- **F_ok:** 56 expressões preservadas e transformadas em objetos auditáveis.
- **F_gap:** 23 definições permanecem `TOKEN_VAZIO`; 33 implementações ainda precisam de código e execução.
- **F_next:** implementar a primeira família no `RafPolimata`, começando por 15, 16, 18, 19 e 24, com testes analíticos e diferenças finitas.

`ΣΩΔΦ`: o nome inspira; o contrato decide; a evidência promove.
