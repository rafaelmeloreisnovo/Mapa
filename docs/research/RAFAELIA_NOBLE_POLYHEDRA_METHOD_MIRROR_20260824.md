# RAFAELIA — Noble Polyhedra Method Mirror — 2026-08-24

State: `EVIDENCE_FIRST / APPEND_ONLY / METHOD_MIRROR_ONLY / claim_allowed=false`

## 0. Scope and non-claim boundary

This record maps a **methodological mirror** between Connor Hill's 2026 computer-assisted classification of noble polyhedra and already-existing RAFAELIA evidence/custody machinery.

It does **not** claim that RAFAELIA classified noble polyhedra, independently discovered Hill's theorem, proves the same mathematics, or that an analogy constitutes prior art. External work is used as a falsifiable methodological reference only.

Hard invariants:

- `VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`
- `METHOD_MIRROR != MATHEMATICAL_EQUIVALENCE`
- `SEARCH_MISS != ABSENCE`
- `INDEX_INCOMPLETE != CORPUS_EMPTY`
- `COMPUTER_ENUMERATION != PROOF_WITHOUT_REDUCTION`
- `TOKEN_VAZIO != ZERO`
- `claim_allowed=false`

## 1. External reference — verified primary-source core

Primary paper: Connor Hill, **The complete set of noble polyhedra**, arXiv:2607.28711, submitted 2026-07-30.

**Provenance correction:** the initial branch materialization mistakenly recorded arXiv `2607.22862`. A primary-source recheck before finalization established `2607.28711` as the correct identifier. The mathematical title/author/date/result description did not change; the incorrect identifier remains visible in Git history and is recorded in the custody receipt rather than hidden.

Primary result summary:

- finite noble polyhedra are treated as polyhedra that are vertex-transitive and facet-transitive;
- existence is reduced to algebraic conditions involving roots of univariate/bivariate cubic polynomials;
- point-group orbits in `R^3` are parametrized;
- a criticality notion and equivalence relation reduce the search to finitely many test cases;
- exhaustive computer search over those finite cases yields exactly **146 isolated noble polyhedra**, in addition to the known infinite families of stephanoids and disphenoids.

Primary URLs:

- https://arxiv.org/abs/2607.28711
- https://www.societyforscience.org/regeneron-sts/2026-student-finalists/connor-hill/

The supplied news article is treated as a secondary pointer; primary sources govern the technical description.

## 2. Existing RAFAELIA lane that genuinely matches at method level

The current Mapa/Drive IGC contract already defines the operational lane:

`SOURCE -> IDENTITY -> MODEL -> TRANSFORMATION -> INVARIANT -> TEST -> NEGATIVE -> RECEIPT -> CLAIM_GATE -> MEMORY`

The existing IGC rule requires the object, representation, transformation family, preserved property, tolerance, test/proof, falsifier and custody to be declared before a PASS can support a claim.

That gives the defensible mirror:

| Hill classification lane | RAFAELIA evidence lane | Relation type |
|---|---|---|
| Infinite-looking candidate universe | Open concept/state universe | `STRUCTURAL_MIRROR` |
| Algebraic restriction | Exact object + transformation contract | `STRUCTURAL_MIRROR` |
| Equivalence relation / finite classes | Canonical identity / quotient candidate classes | `METHOD_BRIDGE` |
| Finite test cases | Enumerated fixtures/candidates | `METHOD_BRIDGE` |
| Exhaustive computer search | Deterministic enumeration | `METHOD_BRIDGE` |
| Mathematical proof around search | Invariant + falsifier + negative test | `METHOD_BRIDGE` |
| Reproducible classification result | Receipt + claim gate | `METHOD_BRIDGE` |

No row above is a claim of mathematical equivalence.

## 3. Source-code evidence from the attached `termux-app-rafacodephi` snapshot

Snapshot SHA-256:

`ac180c75a748c984b5973b1abaa60f251cda17bffe8c9f3dd13c70030c7e7389`

Archive entries observed: `2629`.

### 3.1 Directly relevant source artifacts

1. `app/src/main/cpp/rafaelia_bagua.h`
   - SHA-256: `8859d36ca2cf9f87424ebe52be3ce63e8544e5794641dab7c334f23bb2c861d9`
   - deterministic no-heap machine model;
   - 3-bit trigram rotations;
   - Q15 30-degree rotation;
   - seven modular phases (`T^7`-style discrete state);
   - explicit epistemic boundary: it does **not** claim 42 stable orbits are proved and requires a defined return map, orbit enumeration, Jacobian/spectral tests and reproducible evidence before promotion.

2. `docs/RAFAELIA_GEOMETRIC_ALGEBRA_AUDIT.md`
   - SHA-256: `052fbf72285b2be9d298bb1fd00da1c815b1631aeb4e9758f7768de1978a84e9`
   - records geometric/algebraic audit surfaces including polynomial/root work, Poincaré-Hopf references and dimensional projections.

3. `reports/rafaelia_claim_execution_matrix.csv`
   - SHA-256: `d8aa3de610b0bf9a748eb7d315a25eee23fecf7a738b57d95d6983ff24b832d7`
   - separates `DOC_ONLY`, `NEEDS_EVIDENCE`, `CODE_BACKED` and `RISK_OPEN`;
   - carries executable checks, falsification and rollback fields.

4. `rmr/RAFAELIA_SEMENTES.txt`
   - SHA-256: `f3cff959ecb841bbc30583ee0192a9461f7dced97d7b6c3da9897f6a8e44b884`
   - explicitly recommends isolating a mathematical object, calculating fixed points/period/dimension/invariant, then comparing with literature;
   - the byte-identical `Arme/rafaelia_sementes_v1.txt` has the same hash and is treated as a duplicate, not independent evidence.

### 3.2 Geometry infrastructure already present as package manifests

- `rafaelia/termux-packages-manifests/cgal.rafpkg`: CGAL `6.1.1`, Computational Geometry Algorithms Library.
- `rafaelia/termux-packages-manifests/draco.rafpkg`: Draco `1.5.7`, 3D mesh and point-cloud compression/decompression.

These manifests evidence **available integration intent/inventory**, not installation, runtime success, authorship of the upstream libraries, or a completed polyhedral classifier.

## 4. Runtime evidence produced in this audit

An independent C harness was compiled against the exact `rafaelia_bagua.h` from the supplied archive.

Harness SHA-256:

`ba1769483cb42fdf829ca1ad46634cc18a201c637c67be6e3248b7d3d96e34e6`

Binary SHA-256:

`83226fd37389d3309c2a6dc0fc7096026932769163917a0e716dec5b7549291c`

Observed results:

- `raf_rotation_selftest()` returned `1`;
- 3-bit rotation/inverse mapping closed over all values `0..7`;
- twelve successive Q15 30-degree rotations of `(32768,0)` returned exactly to `(32768,0)` at step 12 in this build;
- squared-norm quantization alternated between the baseline `1073741824` and baseline + `4516` in the observed sequence.

Scope of this evidence:

`PASS_LOCAL_DISCRETE_ROTATION_SELFTEST`

It is **not** evidence of 42 attractors, noble-polyhedra classification, physical geometry, or novelty.

## 5. Validator evidence and negative results

`python3 scripts/validate_rafaelia_claim_matrix.py`

- 20 checks executed;
- after generating the navigation artifact separately, only `C08` remained FAIL;
- C08 failure traces to missing `app/src/main/cpp/bootstrap-arm.zip` in this snapshot.

State: `FAIL_MISSING_REQUIRED_ARTIFACT`, not mathematical refutation.

`python3 scripts/validate_vectra_invariants.py`

- 14 checks;
- 7 PASS / 7 FAIL;
- failures V01–V07 are expected-pattern misses against the current `AGENTS.md` contract (invariants/gcd/42/period/phi/VOID/attractor-table expectations).

State: `FAIL_DOC_EXPECTATION_DRIFT` pending source-of-truth reconciliation; no scientific claim is promoted or refuted solely from this validator drift.

`tests/test_readme_runtime_claim_boundary.py`

- unittest auto-discovery found zero tests because the file uses function-style tests;
- invoking the three test functions directly produced 3/3 PASS.

State: `PASS_MANUAL_FUNCTION_INVOCATION / TEST_DISCOVERY_GAP`.

A dedicated fail-closed validator was added at `tools/validate_noble_polyhedra_method_mirror.py`. A second sandbox retrieval/execution attempt was blocked by external DNS resolution, so no PASS is fabricated for the new validator in this session.

State: `TOKEN_VAZIO_EXECUTION_ENV`.

## 6. NOVO/raw corpus check

The Drive master index for corpus `000–050` exists with typed projections (`CONCEITOS`, `AREAS`, `FORMULAS`, `PROGRAMAS`, `RELACOES`, `TOKEN_VAZIO`, etc.), but its recorded state is still `MATERIALIZING` / `INGESTION_REQUIRED`.

Therefore a missing indexed term cannot be interpreted as absence.

A direct raw source surface was opened from `MESSAGES-00018.jsonl.txt` (11,565,170 bytes in the Drive inventory). It contains source-observed conversation records and numerous geometry-related matches. No direct `Poincar` match was found in the fetched raw resource during this pass; `geometr` returned multiple matches.

Coverage remains non-exhaustive across all raw shards.

State:

`TOKEN_VAZIO_RAW_CROSS_CORPUS_EXHAUSTIVENESS`

No direct searchable Drive hit for `poliedro` was found in this pass. Correct interpretation:

`TOKEN_VAZIO_INTERNAL_NOBLE_POLYHEDRA_PRIOR_ART`

not `ABSENT`.

## 7. ATLAS / NOVO / L / O / T / REL / SCALE / EVID / GAP / LEARN materialization

### ATLAS:X — selected route

`external primary source -> NOVO raw -> attached source snapshot -> canonical IGC contract -> runtime probe -> negative validation -> append-only mirror`

### NOVO:X

Raw source was checked before promoting corpus-level conclusions. Master index incompleteness is explicitly preserved.

### L:X — longitudinal

The evidence line connects earlier symbolic/conceptual geometry, later governed IGC contracts, current source code, current runtime probe and current external methodological reference without rewriting historical states.

### O:X — orthogonal axes

1. identity/provenance
2. mathematical object
3. transformation/equivalence
4. executable enumeration
5. falsifier/negative test
6. runtime evidence
7. claim authority/custody

### T:X — transverse bridges

- geometry <-> computation
- source code <-> formal claim
- raw corpus <-> indexed memory
- external research <-> internal method contract
- enumeration <-> proof gate

### REL:X — explicit relations

Only `STRUCTURAL_MIRROR`, `METHOD_BRIDGE`, `EVIDENCE_SUPPORTS`, `FALSIFIER_OF`, `DUPLICATE_OF`, `GAP_BLOCKS` are permitted in this record. No `PROVES_EQUIVALENT_TO` relation is asserted.

### SCALE:X

`META (classification discipline) -> FAMILY (geometry/state spaces) -> MODEL -> transformation -> candidate class -> orbit/state -> token/field -> executable check -> receipt`.

### EVID:X

Only primary external sources, connected Drive/GitHub sources, exact archive paths/hashes and locally observed executions are evidence-bearing.

### GAP:X

See Section 8.

### LEARN:X

This document and its companion JSON/receipt are append-only in Git history. Corrections are explicit commits/receipts; earlier states are not erased from history.

## 8. Gap ledger / TOKEN_VAZIO

| Gap | State | Promotion effect | Next falsifiable action |
|---|---|---|---|
| Complete raw 000–050 geometry extraction | `TOKEN_VAZIO` | blocks corpus-complete claim | scan every raw shard with exact keyword + semantic family registry |
| Internal noble-polyhedra prior art | `TOKEN_VAZIO` | blocks originality/priority statements | search all raw shards, repos and historical archives for polyhedron-specific algorithms |
| Exact RAFAELIA return map for claimed orbit counts | `TOKEN_VAZIO` | blocks orbit-count claim | formalize map and state space, enumerate canonical orbits |
| Jacobian/spectral stability evidence | `TOKEN_VAZIO` | blocks stable-attractor claim | produce spectra + tolerances + independent rerun receipt |
| `bootstrap-arm.zip` required by C08 | `MISSING_ARTIFACT` | C08 remains FAIL | restore from authoritative custody or change contract with evidence |
| Vectra invariant validator/doc contract drift | `OPEN_DRIFT` | blocks validator PASS | identify authoritative invariant spec and reconcile without weakening checks |
| Automated discovery of function-style runtime boundary tests | `OPEN_TEST_HARNESS` | limits CI evidence | register with pytest or explicit runner |
| New mirror validator runtime in this session | `TOKEN_VAZIO_EXECUTION_ENV` | blocks validator PASS claim | execute in CI/resolvable environment and seal output |
| Noble-polyhedra engine implementation | `NOT_IMPLEMENTED` | blocks any algorithm claim | only after complete paper/code study, implement independently with test corpus |

## 9. Serpent–Dove operational layer

Applied here as:

- **Serpent / discernment:** search primary sources, raw source, source code, hashes, negative tests, validator failures and possible prior art.
- **Dove / minimum sufficient intervention:** no rewriting history, no claiming equivalence, no publishing private raw content, no automatic promotion, no destructive edits.
- **Reversibility:** all new domain records live on a dedicated branch/PR; `claim_allowed=false`.

`SEE_MORE != CLAIM_MORE`

`CAN_COMPUTE != HAVE_PROVED`

`SEARCH_MISS != ABSENCE`

## 10. Next executable research object

The next useful artifact is **not** a copied noble-polyhedra solver. It is a generic, domain-neutral **Finite Classification Contract V1**:

1. define exact object universe `U`;
2. define representation `R(x)`;
3. define admissible transformation group/family `G`;
4. define equivalence `~` and canonical representative `canon(x)`;
5. prove or bound why `U/~` is finite for the scoped problem;
6. enumerate every canonical candidate deterministically;
7. test invariants and explicit falsifiers;
8. emit negative cases and counterexamples;
9. seal inputs/toolchain/output hashes;
10. promote only the scoped result supported by the proof + enumeration chain.

Candidate execution authority for a future mathematical engine: `RafPolimata` or a dedicated research repository. `Mapa` remains the ontology/evidence/gate authority.

## 11. Final state

`METHOD_MIRROR = VERIFIED_LIMITED`

`LOCAL_SOURCE_RUNTIME_EVIDENCE = VERIFIED_LIMITED`

`NOBLE_POLYHEDRA_EQUIVALENCE_CLAIM = BLOCKED`

`RAFAELIA_NOVELTY_CLAIM = BLOCKED`

`claim_allowed=false`
