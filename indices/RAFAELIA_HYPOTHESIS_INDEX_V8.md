# RAFAELIA — Hypothesis Index V8

Date: 2026-08-14  
Mode: `APPEND_ONLY_BY_REFERENCE / MAXIMA_RECORDING`  
State: `GOVERNED_PARTIAL / NONTERMINAL / claim_allowed=false`

Extends: `indices/RAFAELIA_HYPOTHESIS_INDEX_V7.md`

## HYP_CKPT_0008 — 14-family falsification pass

This checkpoint adds **no new hypothesis IDs**. It converts the 14 priority families into explicit `H0/H1/metric/falsifier` structures, records modern comparators, and preserves direct negative evidence from narrow implementation tests.

| View | Count / state |
|---|---:|
| Represented substantive hypothesis IDs | **55** |
| New hypothesis IDs in CKPT0008 | **0** |
| External geophysical comparators | 6 — separate |
| Explicit authorial-origin lower bound | 4 — unchanged |
| Certified authorial-only total | `TOKEN_VAZIO` |
| Certified global unique hypotheses | `TOKEN_VAZIO` |
| Mathematical M3 | 0 |
| Mathematical M4 | 0 |
| claim_allowed | `false` |

`frontier 55` remains provisional and is not a certified global total.

## 1. Canonical falsification artifact

`docs/research/RAFAELIA_FALSIFICATION_PROGRAM_14_FAMILIES_20260814_V1.md`

Evidence ledger:

`data/hypotheses/evidence/RAFAELIA_FALSIFICATION_EVIDENCE_CKPT_0008_20260814.v1.json`

Deterministic local/reference probe:

`scripts/falsification/rafaelia_14_family_gate_v1.py`

## 2. Four direct mathematical/computational closures or falsifiers

### 2.1 Current Bitraf simulator — lossy implementation

Source-bound implementation:

`instituto-Rafael/Eletron-efeitos-qu-ntico/scripts/bitraf_simulator.py` blob `871bd78987934a5983d1320697a8c69dcb76a6bc`.

A deterministic Monte Carlo pass with seed `20260814` and 10,000 normalized complex samples per dimension produced mean round-trip fidelities:

- d=2: `0.9515892624319764`
- d=3: `0.9268751042479932`
- d=4: `0.9077651929364267`
- d=8: `0.8495324080408687`

This establishes `CURRENT_IMPLEMENTATION_IS_LOSSY_IN_THIS_SAMPLE`.

### 2.2 Current Bitraf simulator — basis-vector defect

The current rule `mag_code=int(magnitude*5)%5` maps magnitude exactly `1` to code `0`. Basis vectors in tested dimensions 2,3,4,8 therefore decode to zero-norm vectors.

State: `IMPLEMENTATION_DEFECT_CONFIRMED_IN_CURRENT_SIMULATOR`.

Boundary: this does **not** refute the broader M2 candidate `BITRAF64 formal in F_2^64`.

### 2.3 Current “generalized Hadamard” label

The implementation uses `H=ones((n,n))/sqrt(n)`. For n>1 it has rank 1 and is not unitary. Therefore a claim that this exact operation is a unitary generalized Hadamard is blocked.

### 2.4 Fibonacci Rafael / 42 / sqrt(3)/2

Preserved from the mathematical audit and independently rechecked:

- `2,4,7,12,20,33,54,...`: `a_n=a_(n-1)+a_(n-2)+1`, equivalently `a_n=F_(n+3)-1` for 1-based n — `M0/M1`.
- `uint16 XOR -> mod42`: exact uniformity false because `65536=42*1560+16`.
- `sqrt(3)/2≈0.8660254037844386`; `ln|a|≈-0.14384103622589053`, proving only linear contraction for `x_(n+1)=a*x_n`.

## 3. Josephson/electron repository boundary

`instituto-Rafael/Eletron-efeitos-qu-ntico` is a public repository whose observed scripts include a Josephson model/analyzer and Bitraf simulator. The Josephson script computes known model quantities (`E_J`, plasma frequency, barrier, TA/MQT rates) using chosen example parameters.

State for physical proof in this pass:

`MODEL_CODE_PRESENT / RAW_EXPERIMENTAL_DATA_TOKEN_VAZIO / CURRENT_PASS_ONLY_NOT_GLOBAL_ABSENCE`.

Simulation/model code is not promoted to observation of a quantum effect.

## 4. Modern comparator/prior-art delta

- qudit/QEC: arXiv:2510.06495 — multistate/qudit LDPC makes “>2 states” non-novel by itself;
- Voynich: arXiv:2505.02261 — Fibonacci clustering and golden-ratio alignment create close conceptual overlap requiring blinded predictive differentiation;
- formal grammar: ACL Findings 2025 / arXiv:2505.11932 — BNF→parser→AST is a direct methodological comparator for RAFCODE;
- hierarchical memory: arXiv:2606.11680 — comparator for structured navigation/retrieval under token budget;
- abstention: arXiv:2506.09038 — comparator for TOKEN_VAZIO/unknown handling.

Prior-art note remains a boundary, not a patentability conclusion.

## 5. 14 families and next gates

1. Josephson/MQT → raw data + metrology + model comparison + replication.
2. BITRAF → formal map, rank/kernel/invertibility/distance + fixed implementation tests.
3. parity/ECC → matched-redundancy benchmark.
4. hidden fractal vectors → multiscale invariant + surrogate nulls.
5. fractal compression → rate–distortion(-realism) benchmark.
6. RAFCODE → EBNF + parser + held-out baseline.
7. Voynich/Fibonacci → blind predictive benchmark against close baselines.
8. Fibonacci Rafael → known-equivalence preserved; search only for additional non-derived properties.
9. 42 → preregister null without 42 inserted.
10. sqrt(3)/2 → estimate coefficient as a free parameter.
11. tesseract → ablation.
12. longitudinal memory → Recall@k/MRR/nDCG/state accuracy/cost benchmark.
13. TOKEN_VAZIO → false-assertion/abstention/coverage/selective-risk benchmark.
14. provenance → adversarial mutation and reconstruction matrix.

## 6. F_gap after CKPT0008

- `FG-HYP-001 GLOBAL_COVERAGE` — `IN_PROGRESS`.
- `FG-HYP-002 CANONICAL_IDENTITY_AND_DEDUP` — `IN_PROGRESS`.
- `FG-HYP-003 CLASSIFICATION_HARMONIZATION` — `PARTIAL`.
- `FG-HYP-004 EVIDENCE_LINKAGE` — `IN_PROGRESS_ADVANCED_BY_CKPT0008`.
- `FG-HYP-005 PRIOR_ART_AND_GENEALOGY` — `PARTIAL_ADVANCED_BY_CKPT0008`.
- `FG-HYP-006 EXECUTION_AND_FALSIFICATION` — `IN_PROGRESS_ADVANCED_BY_CKPT0008`.
- `FG-HYP-007 TERMINALITY_AND_GLOBAL_COUNT` — `OPEN_TOKEN_VAZIO`.

## 7. Next cursor

`HYP_CKPT_0009_FORMAL_BITRAF64_RAFCODE_EBNF_MEMORY_TOKENVAZIO_BENCHMARKS`

`R3 = <F_ok: 14-family falsification matrix + modern comparator delta + bounded local falsifiers; F_gap: formal proofs, benchmark executions, physical data, independent replication; F_next: CKPT0009>.`
