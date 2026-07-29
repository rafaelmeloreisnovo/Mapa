# Auditoria Ω aceita — Reclassificação e Topologia Lógica do Programa 7D V1

## Estado

```yaml
event_id: AUDIT-OMEGA-ACCEPTED-7D-TOPOLOGY-V1-20260728
state: CANONICAL_RECLASSIFICATION
claim_allowed: false
runtime_executed: false
prior_art_complete: false
patent_status: TOKEN_VAZIO_IP
```

A Auditoria Ω passa a ser a autoridade de correção para os antigos textos de “fechamento” dos Problemas do Milênio e conjecturas clássicas. O estado anterior é preservado historicamente; o novo evento o supera sem apagá-lo.

## Oito reclassificações

| Módulo | Estado corrigido | Lacuna dominante |
|---|---|---|
| `UTM-194` Riemann | `PROGRAMA_CONJECTURAL` | `TOKEN_VAZIO_EQUIVALENCE` |
| `UTM-198/239` BSD | `PROGRAMA_CONJECTURAL` | `TOKEN_VAZIO_ARITHMETIC_BRIDGE` |
| `UTM-199` Navier–Stokes | `REFUTED_AS_SAME_EQUATION` | equação modificada ≠ original |
| `UTM-200` Yang–Mills | `PROGRAMA_CONJECTURAL` | `TOKEN_VAZIO_QFT` |
| `UTM-201` Hodge | `PROGRAMA_CONJECTURAL` | `TOKEN_VAZIO_ALGEBRAICITY` |
| `UTM-203` Goldbach | `PROGRAMA_CONJECTURAL` | `TOKEN_VAZIO_GLOBAL_EXISTENCE` |
| `UTM-PNP` P versus NP | `PROGRAMA_CONJECTURAL` | `TOKEN_VAZIO_COMPLEXITY_PRESERVATION` |
| `UTM-KAM` Sistema Solar | `REFUTED_UNIVERSALITY` | atrator dissipativo altera o sistema |

## Topologia: nós, cordas e memória

A unidade não é uma frase isolada. É um grafo tipado:

```text
SOURCE
→ CLAIM
→ DEFINITION
→ OPERATOR
→ DOMAIN
→ HYPOTHESIS
→ EQUIVALENCE
→ TEST/PROOF
→ EVIDENCE
→ REVIEW
→ DECISION
→ MEMORY_EVENT
```

As “cordas” são relações com tipo e direção. Relação visual ou sem nome não é aceita:

```text
visual_proximity != typed_relation
typed_relation != causality
```

Tipos canônicos incluem `derived_from`, `defines`, `acts_on`,
`conjectures_equivalence_with`, `requires_gate`, `supported_by`,
`contradicted_by`, `falsified_by`, `implemented_by`, `executed_by`,
`reviewed_by`, `supersedes_state`, `next_gate` e `routes_to`.

## Programa Riemann R0–R10

1. `R0` — objeto oficial;
2. `R1` — geometria/quociente;
3. `R2` — operador, domínio e condição de Reclusão;
4. `R3` — autoadjunção;
5. `R4` — natureza espectral;
6. `R5` — zeta espectral e determinante regularizado;
7. `R6` — fórmula de traço aplicável à geometria definida;
8. `R7` — identidade exata `det_reg(H-s(1-s))=C(s)xi(s)`;
9. `R8` — implicações em ambas as direções;
10. `R9` — falsificação numérica, sem chamar ajuste de prova;
11. `R10` — revisão independente.

O disco/bola de Poincaré completo não é declarado compacto. Espectro discreto, fórmula de Selberg e função `C(s)` permanecem lacunas até construção rigorosa.

## Autoridades

- **Drive:** origem editorial e memória longitudinal;
- **Mapa:** ontologia, topologia, estados e gates;
- **papers:** definições, lemas, ledger e revisão;
- **RLL:** modelos científicos, controles e falsificadores;
- **RafPolimata/ChipQuantum:** implementações e receipts;
- **CONVERSATIONS_CHUNKS_PRIVATE:** genealogia bruta.

## Validador fail-closed

```bash
python scripts/validate_research_program_topology.py
python -m unittest -q tests/test_research_program_topology.py
```

O validador bloqueia:

- qualquer `claim_allowed=true`;
- módulo fora das oito reclassificações aceitas;
- estado incorreto;
- aresta sem tipo conhecido;
- endpoint inexistente;
- quebra da cadeia R0–R10;
- ausência de gate obrigatório;
- inflação de patente/originalidade;
- falta de invariantes.

## Limite

Este pacote valida **estrutura, coerência de relações, custódia e gates**. Não demonstra a identidade espectral, a Hipótese de Riemann, patenteabilidade ou universalidade de `r=0.5`/`Lambda=1`.

## R₃

- **F_ok:** reclassificação, grafo tipado, gates e validador materializados.
- **F_gap:** equivalência espectral, prior art, IP, prova e revisão externa.
- **F_next:** materializar o programa editorial em `papers`; RLL só recebe experimento numérico depois de modelo nulo e protocolo.
