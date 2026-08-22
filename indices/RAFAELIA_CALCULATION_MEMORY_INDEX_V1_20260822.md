# RAFAELIA — Calculation Memory Index Ω — V1 — 2026-08-22

**State:** `GOVERNED_PARTIAL / APPEND_ONLY_POINTER / claim_allowed=false`  
**Role:** federated pointer from `Mapa` to the persistent mathematical/calculation memory materialized in Google Drive.  
**Mother invariant:** `formula != implementation != execution != evidence != claim != novelty`.

## 1. Drive anchors

### Canonical calculation-memory document

- title: `RAFAELIA — Memória Matemática de Cálculo Ω — Fórmulas, Derivadas, Antiderivadas e Heurísticas — V1 — 2026-08-22`
- Drive ID: `1ELvmzr2cltIayFrJmY1ZHzbWgjl6OJ2AkmBu3UoaivU`
- role: memory taxonomy, calculation-memory record `MCM_i`, derivative/antiderivative operators, latent-math heuristics, equivalence/isomorphism ladder, gates, and the initial governed calculation overlay.

### Operational formula/calculation index

- title: `RAFAELIA — Formula & Calculation Memory Index Ω — V1 — 2026-08-22`
- Drive ID: `1HDaHo5IBj42rr-iyxftG1zfaEzzCI9xC4s_0W_-1vR8`
- sheets: `FORMULAS`, `SOURCE_COVERAGE`, `MEMORY_TAXONOMY`, `INDEX_TAXONOMY`, `GAPS_NEXT`, `SHARD04_RAW`
- role: navigation by source expression, type, domain, derivative, antiderivative/accumulator, inverse/reverse, singularities, equivalence, epistemic state, gap, and `F_next`.

## 2. Recovered memory topology

Three complementary memory views are distinguished instead of collapsed into one count:

1. `LONGITUDINAL` — deltas, revisions, evidence evolution, temporal antiderivative;
2. `TRANSVERSAL_CONTEXTUAL` — cross-domain/project/formula/claim/evidence retrieval;
3. `ORTHOGONAL` — independent recovery axes and convergence without treating aliases as independent confirmation.

The permanent-memory architecture remains layered `L0..L8`, and the observed orthogonal checkpoint uses axes `O1..O7`.

## 3. Recovered index topology

High-level reconstruction families:

`IDX-00 CANON` · `IDX-01 FORMULAS` · `IDX-02 GRAPH` · `IDX-03 RECEIPTS` · `IDX-04 SCIENCE` · `IDX-05 RUNTIME` · `IDX-06 CRYPTO` · `IDX-07 IP` · `IDX-08 MEMORY` · `IDX-09 GOVERNANCE`.

Observed concrete memory-checkpoint indices:

`artifact.index` · `sha256.index` · `temporal.index` · `topic.index` · `entity.index` · `repository.index` · `formula.index` · `claim.index` · `gap.index` · `relations.index` · `falsifier.index`.

These are different levels of the architecture and MUST NOT be added together as if they were one homogeneous taxonomy.

## 4. Formula-source coverage observed in this reconstruction

| Layer | Materialized observation | Guard |
|---|---:|---|
| formula registry V1 | 50 governed records | registry-local |
| 2026-08-12 session registry | 122 surfaced relations | not a global unique count |
| bounded source scan | 49 candidate paths / 48 unique blobs | path != formula |
| extraction shard01 | 22 occurrences | 22 exact digests unique in shard |
| extraction shard02 | 38 occurrences | S01+S02 = 60 occurrences / 59 exact unique |
| extraction shard03 formal | 47 occurrences | 44 exact unique inside shard |
| raw observed S01+S02+S03 | 107 occurrences | NOT a global unique total |
| extraction shard04 Matem-tica- | 208 occurrences | 201 exact NFC+trim identities; 6 duplicate groups; 12 paths / 11 blobs |
| raw observed S01+S02+S03+S04 | 315 occurrences | NOT a global unique total; cross-shard dedup pending |
| reported target | 593 + 60 = 653 | `UNVERIFIED_REPORTED_TARGET` |

SHARD04 receipt:

`data/reconciliation/OMEGA_FORMULA_EXTRACTION_SHARD04_MATEMATICA_20260822.v1.json`

SHARD04 index delta:

`indices/RAFAELIA_CALCULATION_MEMORY_SHARD04_DELTA_20260822.md`

Canonical unresolved states:

```text
FORMULA_REGISTRY_GLOBAL_UNIQUE_TOTAL = TOKEN_VAZIO
SEMANTIC_DEDUP_GLOBAL                = TOKEN_VAZIO
```

Numeric titles/ranges such as `350-formulas-mvps` or `402-expressoes` are not promoted to counts of distinct materialized formulas without expression-level extraction.

## 5. Calculation-memory unit

```text
MCM_i = <
  id,
  source_repo,
  source_path,
  source_blob_or_hash,
  source_span,
  source_expression,
  normalized_expression,
  object_type,
  domain,
  variables,
  assumptions,
  dimensions_units,
  derivative_operator,
  derivative_result,
  second_order_or_sensitivity,
  antiderivative_or_accumulator,
  inverse_or_reverse,
  singularities_branches,
  invariants,
  equivalence_family,
  implementation_refs,
  execution_refs,
  evidence_refs,
  epistemic_state,
  claim_allowed,
  falsifier,
  gaps,
  F_next
>
```

No derivative, antiderivative, inverse, Jacobian, Hessian, Boolean derivative, modular primitive, or reverse operator is inferred merely from symbol shape. Applicability requires the mathematical object and domain to be typed first.

## 6. Calculation operator families

Derivative side:

`constant` · `d/dx` · partial derivative · gradient · Jacobian · Hessian · discrete difference `Δ` · modular residual · Boolean/GF(2) derivative · parametric sensitivity · graph/state delta.

Reverse/antiderivative side:

continuous primitive · discrete/telescoping sum · recurrence reconstruction · functional inverse · preimage · causal reverse traversal · longitudinal evidence accumulation · finite/modular primitive when defined.

`reverse traversal != inverse function` is a required boundary.

## 7. Equivalence / isomorphism ladder

```text
E0 EXACT_TEXT
E1 EXACT_AST
E2 ALGEBRAIC_EQUIVALENCE
E3 CHANGE_OF_VARIABLES
E4 CONJUGACY
E5 ISOMORPHISM
E6 NUMERICAL_NEAR
E7 SEMANTIC_ANALOGY
```

`E6`/`E7` MUST NOT be silently merged into `E0..E5`. Every occurrence retains source provenance even after a valid equivalence class is found.

## 8. Initial calculation overlay

The Drive memory contains 18 curated seed families plus the provider-bound SHARD04 raw expression layer. Seed families cover:

- `κ=sqrt(3)/2` and `S(d)=κ^d`;
- radial/angular discrete recurrences;
- Rafaeliana/Fibonacci equivalence and discrete derivative;
- affine and filtered updates;
- symbolic multiplicative recurrence with typed-domain guard;
- the six-state semantic cycle as a graph, not forced continuous calculus;
- log/modular and complex phase-scale maps with branch/singularity guards;
- modular residue embedding;
- XOR/GF(2) candidate calculus;
- modular weighted functionals and contraction maps;
- longitudinal discrete derivative/antiderivative;
- typed `TOKEN_VAZIO` gap-load accumulator.

SHARD04 raw expressions are source-bound occurrences; they are not automatically promoted into differentiated `MCM` records until domain/operator gates are applied.

## 9. Source anchors already present in Mapa

- `indices/RAFAELIA_FORMULA_INDEX_V2.md`
- `data/formulas/RAFAELIA_FORMULA_REGISTRY.v3.json`
- `data/reconciliation/OMEGA_FORMULA_SOURCE_SCAN_20260815.v1.json`
- `data/reconciliation/OMEGA_FORMULA_EXTRACTION_SHARD01_20260816.v1.json`
- `data/reconciliation/OMEGA_FORMULA_EXTRACTION_SHARD02_20260816.v1.json`
- `data/reconciliation/OMEGA_FORMULA_EXTRACTION_SHARD03_FORMAL_20260816.v1.json`
- `data/reconciliation/OMEGA_FORMULA_EXTRACTION_SHARD04_MATEMATICA_20260822.v1.json`
- `indices/RAFAELIA_CALCULATION_MEMORY_SHARD04_DELTA_20260822.md`
- `docs/research/RAFAELIA_MULTIDIMENSIONAL_COHERENCE_FORMULA_BRIDGE_20260815.md`

External governed source anchor:

- `rafaelmeloreisnovo/Matem-tica-/papers/2026-07-17_antiderivada_vazio_fluxo_toroidal.md`

## 10. Remaining bounded queue

Four `rafaelmeloreisnovo/teoremas` source-scan candidates remain expression-level pending:

- `TEORIA_ATRACTOR_42.md`
- `docs/rafaelia/350-formulas-mvps.md`
- `docs/rafaelia/biosincronia.md`
- `docs/rafaelia/domo-rafaelia-402-expressoes.md`

State: `TOKEN_VAZIO_EXPRESSION_LEVEL_PENDING_SHARD05`.

## 11. Deterministic route

```text
SOURCE
→ EXTRACT
→ NORMALIZE
→ TYPE
→ DOMAIN
→ DERIVE
→ ANTIDERIVE/INVERT
→ SINGULARITIES
→ EQUIVALENCE
→ DEDUP
→ IMPLEMENTATION
→ EXECUTION
→ EVIDENCE
→ CLAIM_GATE
→ APPEND MEMORY
```

## 12. R3

**F_ok:** Drive calculation memory and operational index were materialized; SHARD04 closes the prior 12-path `Matem-tica-` queue under frozen provenance with 208 raw occurrences and 201 exact NFC+trim identities; the raw row store and GitHub receipt are bound.  
**F_gap:** four `teoremas` paths remain; global unique formula count, exact cross-shard dedup, semantic/algebraic equivalence, complete domain/unit typing, and formula→implementation→execution→evidence linkage remain partial or `TOKEN_VAZIO`.  
**F_next:** SHARD05 → exact digest S01..S05 → E1 AST → E2 algebraic equivalence → typed `MCM` calculation overlay; do not widen scientific or novelty claims before those gates.
