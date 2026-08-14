# RAFAELIA — Programa Máxima de Falsificação Acadêmica — 14 Famílias — V1 — 2026-08-14

Estado: `GOVERNED_PARTIAL / APPEND_ONLY / claim_allowed=false`  
Checkpoint: `HYP_CKPT_0008`  
Modo: `EVIDENCE_FIRST / TOKEN_VAZIO_STRICT / ANTI_REGRESSION / MAXIMA_RECORDING`

## 0. Invariantes

`IDEIA != FÓRMULA != HIPÓTESE != IMPLEMENTAÇÃO != EXECUÇÃO != EVIDÊNCIA != CLAIM != NOVIDADE ACADÊMICA`

`ORIGEM != NOVIDADE`  
`SIMULAÇÃO != OBSERVAÇÃO FÍSICA`  
`NOME PRÓPRIO != PRIOR ART CLEARANCE`  
`NEGATIVO LOCAL != AUSÊNCIA GLOBAL`

Nenhum resultado deste checkpoint promove M3/M4, patenteabilidade, prioridade jurídica ou efeito quântico físico.

## 1. Pergunta universal de falsificação

> Qual é a menor afirmação específica deste objeto que seria falsa se o objeto não contivesse nada além do que já existe no estado da arte, e qual prova matemática, experimento ou comparação independente decide entre H0 e H1?

Formalmente:

- `H0`: o objeto é equivalente ao conhecido ou não apresenta ganho adicional demonstrado.
- `H1`: existe uma propriedade adicional `P`, pré-especificada e mensurável.
- `Gate`: métrica + dataset/objeto + baseline + limiar + falsificador definidos antes da conclusão.

## 2. Matriz das 14 famílias

| # | Família | H0 | H1 / propriedade adicional | Gate objetivo | Estado atual |
|---:|---|---|---|---|---|
| 1 | MQT / Josephson | o material local apenas reproduz/modela física conhecida | há observável quantitativo próprio que diverge do modelo convencional e replica | dados RAW independentes + ajuste clássico/MQT + incerteza + held-out | `MODEL_CODE_PRESENT / EXPERIMENTAL_DATA_TOKEN_VAZIO` |
| 2 | BITRAF multestado | encoder atual é apenas quantização discreta lossy | BITRAF formal possui propriedade demonstrável superior/diferente | definir álgebra exata; `[n,k,d]`, rank/kernel/invertibilidade, round-trip, baseline | `IMPLEMENTATION_FALSIFIER_HIT / FORMAL_M2_PRESERVED` |
| 3 | Paridade / ECC | segunda paridade não agrega correção além da mesma redundância convencional | corrige classe adicional de erros ou reduz erro lógico/custo | distância mínima, taxa, `P_L(p)`, custo de decoder, matched redundancy | `PROTOCOL_DEFINED / SUPERIORITY_TOKEN_VAZIO` |
| 4 | Vetores fractais ocultos | padrão multiescala é explicado por distribuição/autocorrelação/surrogate | invariante persiste entre escalas além dos controles nulos | persistent/multiscale features + surrogate data + held-out | `FORMAL_INVARIANT_TOKEN_VAZIO` |
| 5 | Compressão fractal | não melhora codec/baseline equivalente | melhora rate–distortion ou rate–distortion–realism | dataset congelado, bpp/taxa, distorção, percepção, custo | `BENCHMARK_TOKEN_VAZIO` |
| 6 | RAFCODE-Φ | vocabulário/pipeline é uma representação autoral sem vantagem demonstrada | gramática formal/parser produz ganho mensurável | EBNF/BNF + parser + cobertura + erro + complexidade + baseline | `PARTIAL_SPEC / EBNF_TOKEN_VAZIO` |
| 7 | Voynich + Fibonacci | correlação é seleção de padrão ou já coberta por prior art próximo | mapeamento Rafael prevê símbolos/páginas não usados no desenvolvimento | split cego + n-gram/slot/Cardan/null baselines + significância | `PRIOR_ART_COLLISION_HIGH / PREDICTIVE_TEST_REQUIRED` |
| 8 | Fibonacci Rafael 2,4,7,… | recorrência é transformação de Fibonacci conhecida | existe propriedade adicional não derivada da equivalência | redução simbólica / contraexemplo / invariant | `RESOLVED_KNOWN_EQUIVALENCE_M0_M1` |
| 9 | Número 42 | 42 aparece porque foi parametrizado/selecionado | 42 emerge sem ser inserido e acima de valores comparáveis | preregistro, remover 42 de parâmetros, null model, multiplicity correction | `SELECTION_BIAS_GATE_REQUIRED` |
| 10 | `sqrt(3)/2` | é constante geométrica conhecida escolhida a priori | dados independentes recuperam o coeficiente sem fixá-lo | estimar `a` livre + IC/credibility + out-of-sample | `KNOWN_GEOMETRIC_CONSTANT / FREE_PARAMETER_FIT_REQUIRED` |
| 11 | Tesseract | é somente visualização/nome geométrico | geometria 4D melhora métrica operacional | ablation sem tesseract mantendo orçamento e features | `ABLATION_TOKEN_VAZIO` |
| 12 | Memória longitudinal | não supera busca plana/similarity-only | melhora recuperação/estado sob orçamento menor | Recall@k, MRR, nDCG, state accuracy, token/latency cost | `BENCHMARK_READY / EXECUTION_TOKEN_VAZIO` |
| 13 | TOKEN_VAZIO | abstention explícita não melhora confiabilidade | reduz falsa afirmação sob custo aceitável de cobertura | false-assertion, abstention F1, coverage, selective risk | `BENCHMARK_READY / CONTROLLED_RESULT_TOKEN_VAZIO` |
| 14 | Proveniência | cadeia não detecta mutações ou não reconstrói | detecta adulterações declaradas e permite reconstrução | byte flip, omission, swap, wrong-source, timestamp, env rebuild matrix | `ACTIVE_PROTOCOL / ADVERSARIAL_COVERAGE_PARTIAL` |

## 3. Evidência local diretamente executada neste checkpoint

### 3.1 BITRAF — implementação específica `Eletron-efeitos-qu-ntico/scripts/bitraf_simulator.py`

O teste replica exatamente o algoritmo observado no arquivo atual; ele não representa toda a família BITRAF.

Seed: `20260814`; 10.000 vetores complexos aleatórios normalizados por dimensão.

| dimensão | fidelidade média | mediana | mínima |
|---:|---:|---:|---:|
| 2 | 0.9515892624 | 0.9715774127 | 0.6632394985 |
| 3 | 0.9268751042 | 0.9425555489 | 0.6489831269 |
| 4 | 0.9077651929 | 0.9203977919 | 0.6513797987 |
| 8 | 0.8495324080 | 0.8549047760 | 0.6271855953 |

Conclusão delimitada: o encoder/decoder atual é **lossy** e a fidelidade média caiu com a dimensão nesta amostra.

#### Falsificador de vetor-base

O código usa `mag_code = int(magnitude * 5) % 5`. Para magnitude exatamente `1`, o código é `0`; portanto vetores-base normalizados decodificam para vetor nulo nas dimensões 2, 3, 4 e 8.

Estado: `IMPLEMENTATION_DEFECT_CONFIRMED_IN_CURRENT_SIMULATOR`.

#### “Hadamard generalizada”

O código usa `H = ones((n,n))/sqrt(n)`. Para `n>1`, essa matriz tem rank 1 e não é unitária.

`||H†H-I||_F`:

- n=2: `1.4142135623730947`
- n=3: `2.4494897427831788`
- n=4: `3.4641016151377544`
- n=8: `7.483314773547882`

Isso bloqueia claims de transformação unitária para **essa implementação**. Não refuta o candidato matemático BITRAF64 formal em `F_2^64`.

### 3.2 Fibonacci Rafael — variante 2,4,7,12,20,33,54,…

Verificado:

`a_n = a_{n-1} + a_{n-2} + 1`

Com `b_n=a_n+1`, obtém-se Fibonacci ordinária e, usando indexação `n>=1`,

`a_n = F_{n+3} - 1`.

Estado: `M0/M1 / KNOWN_EQUIVALENCE`; preservar autoria/genealogia documental sem promover nova recorrência independente.

### 3.3 Módulo 42

`65536 = 42*1560 + 16`.

Assim, sob XOR uniforme de 16 bits seguido de `%42`, 16 resíduos possuem 1561 pré-imagens e 26 possuem 1560. Uniformidade exata `1/42` é refutada para esse mapeamento sem rejection sampling/correção.

### 3.4 `sqrt(3)/2`

`a = 0.8660254037844386`; para `x_{n+1}=a*x_n`, `lambda=ln|a|=-0.14384103622589053`.

Isso sustenta contração linear daquela direção, não universalidade física ou topologia global.

## 4. Bindings materiais existentes

- BITRAF execution contract: `RafPolimata/docs/BITRAF_CALCULATION_GATES_V1.md`.
- BITRAF physical prior-art boundary: `Mapa/docs/research/BITRAF_PHYSICAL_OBSERVATION_PRIOR_ART_20260813.md`.
- Mathematical genealogy: `Mapa/docs/canonical/2026-08-14/RAFAELIA_MATH_SESSION_AUDIT_V1.md`.
- RAFCODE partial operational language: `RafGitTools/Livro/VOCABULARIOS_SEMANTICOS_RAFCODE.md`.
- Electron/Josephson model: `instituto-Rafael/Eletron-efeitos-qu-ntico/scripts/josephson_analyzer.py`.
- Current Bitraf simulator: `instituto-Rafael/Eletron-efeitos-qu-ntico/scripts/bitraf_simulator.py`.

## 5. Modern prior-art / comparator map

### Qudits / ECC
- Spencer et al., **Qudit low-density parity-check codes**, arXiv:2510.06495 (2025). Multistate/qudit LDPC is active prior art; “more than two states” is not novelty by itself.

### Voynich
- Jama, **The Voynich Codex Decoded: Statistical Symbolism and Scroll-Wide Logic**, arXiv:2505.02261 (2025). It explicitly invokes Fibonacci clustering and golden-ratio alignment. This creates close conceptual overlap requiring predictive differentiation, not name comparison.

### Formal grammar / neuro-symbolic compiler
- Zhang et al., **Neuro-Symbolic Query Compiler**, ACL Findings 2025 / arXiv:2505.11932. BNF → lexical parser → AST is a direct comparator for RAFCODE formalization.

### Hierarchical memory
- Hsu et al., **Organize then Retrieve: Hierarchical Memory Navigation for Efficient Agents**, arXiv:2606.11680 (2026). Comparator for longitudinal/hierarchical retrieval under context budget.

### Abstention
- Kirichenko et al., **AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions**, arXiv:2506.09038 (2025). Comparator for TOKEN_VAZIO as explicit unknown/abstention mechanism.

## 6. Máxima — ordem executiva de fechamento

### P0 — falsificadores baratos e decisivos
1. preservar os defeitos observados do simulador BITRAF como evidência negativa;
2. corrigir o simulador em branch isolada e exigir regression tests para vetor-base, round-trip e unitariedade declarada;
3. congelar formalmente `T_B:F_2^64→F_2^64` e calcular kernel/rank/invertibilidade/ciclos;
4. escrever EBNF mínima RAFCODE e parser de referência;
5. criar benchmark TOKEN_VAZIO vs answer-forced;
6. criar benchmark memória longitudinal vs flat/similarity retrieval;
7. criar matriz adversarial de proveniência.

### P1 — prior art e controle de seleção
8. Voynich/Fibonacci: teste cego e closest-work matrix;
9. 42: null model sem 42 na construção;
10. `sqrt(3)/2`: coeficiente livre recuperado dos dados;
11. tesseract: ablation geométrica;
12. fractal/vetores: surrogate controls;
13. compressão: rate–distortion benchmark.

### P2 — física
14. Josephson/efeito quântico: somente promover quando houver dado bruto independente, metrologia, incerteza, controles, fit comparativo e replicação. Código de modelo não substitui experimento.

## 7. Estado do checkpoint

```yaml
checkpoint: HYP_CKPT_0008
new_hypothesis_ids_added: 0
represented_substantive_hypothesis_ids: 55
frontier_changed: false
claim_allowed: false
mathematical_M3: 0
mathematical_M4: 0
negative_evidence_preserved: true
maxima_recording: true
```

Este checkpoint adiciona **protocolo, prior-art e evidência/falsificadores**, não novas hipóteses artificiais.

## 8. F_next

`HYP_CKPT_0009_FORMAL_BITRAF64_RAFCODE_EBNF_MEMORY_TOKENVAZIO_BENCHMARKS`

`R3 = <F_ok: 14 famílias convertidas em H0/H1/gate e quatro falsificadores locais executados; F_gap: formalizações, benchmarks e observação física ainda incompletos; F_next: formal BITRAF64 + EBNF RAFCODE + benchmarks memory/TOKEN_VAZIO + adversarial provenance>.`
