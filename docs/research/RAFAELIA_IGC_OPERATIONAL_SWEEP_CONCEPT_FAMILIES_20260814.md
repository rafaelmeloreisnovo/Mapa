# RAFAELIA — IGC Operational Sweep across Concept Families — 2026-08-14

State: `CANONICAL_DRAFT / APPEND_ONLY / EVIDENCE_FIRST / claim_allowed=false`

## 0. Custody boundary

This sweep is derived from the already-merged geometric invariant contract and the already-merged concept-anteriority batch. Historical PR #231 was merged before this sweep was materialized; therefore these sweep artifacts are intentionally carried on a new branch based on current `main` and must not be treated as part of PR #231.

Historical post-merge writes on `audit/concept-anteriority-batch-20260813` are preserved as provenance and are not rewritten.

## 1. Purpose

Apply the already-materialized **Invariante Geométrica Coerente / Coesão Real (IGC-CR)** as an operational filter over the concept-anteriority families.

This sweep does **not** promote every family to a geometry. It asks, for each family:

`OBJECT -> REPRESENTATION -> TRANSFORMATION_FAMILY -> PRESERVED_PROPERTY -> TOLERANCE -> TEST/PROOF -> FALSIFIER -> CUSTODY`

Canonical rule:

`IGC(X,T,I,epsilon)=PASS` only over a declared transformation family and declared test/proof surface.

Missing transformation family => `TOKEN_VAZIO_TRANSFORMATION_FAMILY` and `claim_allowed=false`.

Coesão real gate:

`C_real = G_S AND G_D AND G_T AND G_I AND G_E AND G_F AND G_C`

where source/authorship, definition, transformation, invariant compatibility, evidence, falsifier and custody must all be present.

## 2. Operational classes

### A. DIRECT_GEOMETRIC
- HYPERCUBE/HIPERCUBO
- TESSERACT
- HYPERFORMA only after an exact model is declared

Allowed transformation candidates depend on the model: isometry, similarity, affine, projective, homeomorphism, projection. Generic visual similarity is insufficient.

### B. STRUCTURAL_COMBINATORIAL
- ZIPRAF
- ZRF
- ZFR
- BITRAF
- RAFBIT
- XOR compositions

Useful invariants may be byte/combinatorial rather than Euclidean: exact roundtrip bytes, archive compatibility, record cardinality/layout, declared incidence relations, verification behavior. Cryptographic authenticity remains a separate trust layer.

### C. STATE_SPACE_OPERATIONAL
- RAFMEM
- RAFMEN
- RAFSTORE
- RAFSTORAGE
- NETRAF
- RAFNET_CORE
- RAFCODE
- RAFCORE
- RAFAELOS
- `fir via os` / `rafarlos`
- RafQuantumSupercomputer
- EXOCORDEX

No family in this class receives a geometric claim from its name alone. Minimum declaration: `state set + transition operator + equivalence relation + observable invariant`.

### D. EMPIRICAL_BIOPHYSICAL
- BIOSSINTETICO
- BIOPHOTON/BIOFOTON

Graph/topology/state-space models remain hypotheses until dataset, measurement procedure, uncertainty and falsifier are bound.

### E. META_MATHEMATICAL
- CLAYMATH

This is not one geometry. Each problem-specific construction inherits the transformation/invariant language of the specific mathematical problem. Internal derivation is not a solved-problem claim.

## 3. Family sweep

| Family | Structural object candidate | Transformation family | Candidate invariant | Current IGC status | Main gap |
|---|---|---|---|---|---|
| ZIPRAF | byte archive + manifest + BITRAF relation | encode/decode, roundtrip, controlled tamper/reforge | ZIP compatibility, byte identity where declared, structural verification behavior | `PARTIAL_MATERIAL_EVIDENCE` | bind exact current version/receipt to this sweep |
| ZRF | extension/container/codec family | `TOKEN_VAZIO_EXACT_SEMANTICS` | `TOKEN_VAZIO` | `TOKEN_VAZIO_MODEL` | exact ZRF object/representation/transforms |
| ZFR | unresolved later alias/family | `TOKEN_VAZIO` | `TOKEN_VAZIO` | `TOKEN_VAZIO_ALIAS` | first definition + semantics; do not inherit ZRF date |
| BITRAF | binary structural record/index | serialize/deserialize, mutation, verification | record layout/cardinality + declared structural consistency | `VERIFIED_PROTOTYPE_LINEAGE` | version-specific IGC contract and current exact receipt |
| RAFBIT | contextual state/bit precursor | `TOKEN_VAZIO_EXACT_OPERATOR` | `TOKEN_VAZIO` | `TOKEN_VAZIO_MODEL` | relation to BITRAF must be proven, not inferred |
| XOR | bitwise operation | XOR composition | algebraic result for a declared encoding | `ESTABLISHED_OPERATOR_ONLY` | specific RAFAELIA composition/invariant |
| HYPERCUBE | n-dimensional cube | isometry/similarity/projection/etc. as declared | metric/combinatorial/topological property appropriate to T | `DIRECT_GEOMETRIC_CANDIDATE` | exact RAFAELIA representation and T |
| TESSERACT | 4D hypercube | same, model-dependent | same, model-dependent | `DIRECT_GEOMETRIC_CANDIDATE` | exact representation/projection contract |
| HYPERFORMA | user-defined higher form | `TOKEN_VAZIO_TRANSFORMATION_FAMILY` | `TOKEN_VAZIO` | `TOKEN_VAZIO_MODEL` | vertices/cells/glue/state definition |
| RAFMEM | memory/state object | snapshot/reload/reindex only if specified | state equivalence / content identity if defined | `STATE_SPACE_CANDIDATE` | state schema + transition semantics |
| RAFMEN | unresolved alias | `TOKEN_VAZIO` | `TOKEN_VAZIO` | `TOKEN_VAZIO_ALIAS` | explicit RAFMEN ==/!= RafMem evidence |
| RAFSTORE | storage object | put/get/serialize/restore if specified | content identity, index relations if declared | `STATE_SPACE_CANDIDATE` | executable contract + relation to RafStorage |
| RAFSTORAGE | storage precursor/family | `TOKEN_VAZIO_EXACT_SEMANTICS` | `TOKEN_VAZIO` | `STATE_SPACE_CANDIDATE` | identity/equivalence with RafStore |
| NETRAF | protocol/network state graph | encode/decode, route, reorder only if protocol permits | protocol/state graph properties | `STATE_SPACE_CANDIDATE` | wire format + state machine + negatives |
| RAFNET_CORE | network core family | `TOKEN_VAZIO` | `TOKEN_VAZIO` | `TOKEN_VAZIO_RELATION` | prove relation to NetRaf |
| RAFCODE | code/toolchain object | parse/compile/translate/execute only when semantics specified | semantic/output equivalence under declared transform | `STATE_SPACE_OPERATIONAL_CANDIDATE` | language/IR/ABI contract + golden vectors |
| RAFCORE | core family | `TOKEN_VAZIO` | `TOKEN_VAZIO` | `TOKEN_VAZIO_MODEL` | exact object and dependency graph |
| RAFAELOS | OS/runtime state machine | boot/state transition/restart if formally modeled | state-transition invariants and custody, not visual geometry | `STATE_SPACE_OPERATIONAL_CANDIDATE` | executable state model + receipt |
| FIR VIA OS / RAFARLOS | unresolved spelling | `TOKEN_VAZIO` | `TOKEN_VAZIO` | `TOKEN_VAZIO_ALIAS` | source resolving term/alias |
| BIOPHOTON | measured UPE/photonic observable | calibration/channel/time-window transform as explicitly defined | statistical/measurement stability only | `EMPIRICAL_MODEL_REQUIRED` | dataset + measurement protocol + uncertainty |
| BIOSSINTETICO | biological engineered system | intervention/state transition dependent on model | network/topology/phenotype invariant only if declared | `EMPIRICAL_MODEL_REQUIRED` | concrete biological object + safety/measurement contract |
| CLAYMATH | problem-specific mathematical object | inherited per problem | problem-specific theorem invariant | `META_MATH_BOUNDARY` | proof + independent review; no generic IGC promotion |
| EXOCORDEX | user concept | `TOKEN_VAZIO` | `TOKEN_VAZIO` | `TOKEN_VAZIO_MODEL` | definition -> representation -> transformation |
| RafQuantumSupercomputer | system concept | workload/state transformation if real system exists | deterministic outputs/performance invariants only if measured | `TOKEN_VAZIO_IMPLEMENTATION_LEVEL` | hardware/runtime identity + measured receipts |

## 4. Strongest currently defensible cross-family relations

### REL-IGC-ZIPRAF-BITRAF
`ZIPRAF -> structural layer -> BITRAF` is meaningful when versioned artifacts prove the linkage. It is not evidence that BITRAF itself is Euclidean geometry.

### REL-IGC-HYPERCUBE-TESSERACT
`TESSERACT` is a specific 4D hypercube model. Any RAFAELIA-specific contribution must attach to encoding/projection/state/algorithm rather than existence of the mathematical object.

### REL-IGC-STATE-LAYERS
`RafMem/RafStore/NetRaf/RAFCODE/RafaelOS` can share an abstract state-space method only after each publishes its own state set and transition operators. Shared ecosystem membership is not shared geometry.

### REL-IGC-BIO
Biofoton/biossintetico may be represented as dynamical or network systems, but geometric/topological language stays `MODEL_HYPOTHESIS` until measurement and falsification are attached.

## 5. Anti-regression falsifiers

Fail closed if any of the following occurs:

1. `visual_similarity => geometric_identity`.
2. `same_alias => same_object`.
3. `same_name_family => same_transformation_family`.
4. `hash_match => scientific_claim_true`.
5. `simulation => physical_measurement`.
6. `state_graph_analogy => topology_proven`.
7. `ZFR => inherits ZRF historical date` without source evidence.
8. `RAFMEN => RafMem` without explicit evidence.
9. `hypercube/tesseract exists => RAFAELIA novelty`.
10. `Clay-related derivation => Millennium Problem solved`.

## 6. Operational excellence lane

For every family F:

`SOURCE_F -> IDENTITY_F -> MODEL_F -> T_F -> I_F -> TEST_F -> NEGATIVE_F -> RECEIPT_F -> CLAIM_GATE_F -> MEMORY_F`

Promotion rule:

- no model: `TOKEN_VAZIO_MODEL`
- model but no T: `TOKEN_VAZIO_TRANSFORMATION_FAMILY`
- T but incompatible/undefined I: `TOKEN_VAZIO_INVARIANT`
- I but no negative case: `TOKEN_VAZIO_FALSIFIER`
- execution without custody: `TOKEN_VAZIO_RECEIPT`
- all local gates passing: at most `VERIFIED_LIMITED`
- no automatic scientific/general promotion

## 7. Source anchors

- Drive canonical IGC: `1eGLmUTXAgcm4M9hJNCXoB5OLnc9ZSGMqTXvsFJasags`
- Mapa IGC origin: PR #128, merged; merge commit `6c60b1df49760f5867d173f24da44ef524b9435b`
- Local reproduction receipt: `receipts/geometry/IGC_CR_20260802_RECEIPT_V2_LOCAL_REPRO.json`
- Concept anteriority registry Drive: `1wn5bQnMzN8Y7_EbLqlOld2CCKNpnx8xZxRs2mMxKWRg`
- Historical anteriority PR: #231, merged at `b50a87ad0e8507bb62bfe7394f47cc0196bd52f4`
- Clean sweep base: `main@54bbcdddc7f82b543fa05fd7ef233e2c3eda75ca`
- Current sweep branch: `audit/igc-family-sweep-20260814`
- Drive sweep: `1ZK4nfS8LupSFHGRUSPJBWtdECUMUhvcLWdOaXe_aBlk`

## 8. F_OK / F_GAP / F_NEXT

### F_OK
- IGC-CR is already materialized and merged.
- Positive and negative local geometry fixtures were reproduced in the prior receipt.
- Concept-family anteriority registry is already materialized on main.
- This sweep separates direct geometry, combinatorial structure, state-space models, empirical models and meta-mathematics.
- Promotion regression from the already-merged PR #231 was detected and contained by clean-branch rematerialization.

### F_GAP
- Most non-geometric families lack exact `OBJECT/REPRESENTATION/T/I` contracts.
- ZFR, RAFMEN, `fir via os/rafarlos` remain alias/identity gaps.
- ZRF exact present semantics are not yet bound here.
- physical Termux execution and independent IGC reproduction remain open from the canonical receipt.
- cross-family equivalence claims remain unpromoted.

### F_NEXT
1. Generate one machine-readable IGC candidate record per family.
2. Materialize negatives first for every proposed equivalence/alias.
3. Bind versioned artifacts and receipts for ZIPRAF/BITRAF before expanding to weaker families.
4. Resolve state schemas for RafMem/RafStore/NetRaf/RAFCODE/RafaelOS.
5. Keep empirical bio families behind measurement gates.
6. Preserve `claim_allowed=false` globally until family-local evidence allows narrower promotion.

FIAT LUX — geometry is not the name of the object; it is the declared relation that survives a declared transformation under a declared test.
