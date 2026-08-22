# RAFAELIA — Semantic Support Matrix Ω V1 — 2026-08-22

**State:** `ACTIVE_BOUNDED / SEMANTIC_FAIL_CLOSED / claim_allowed=false`  
**Applies to:** `interpret_context` and every path that turns source material into a formalization, implementation route, execution request, evidence edge or claim.  
**Mother invariant:**

```text
surface_text != semantic_reading != formalization != implementation != execution != evidence != claim
```

## 1. Why this layer exists

The operational workflow already has source intake, normalization, relation indexing and epistemic gates, but `interpret_context` was still planned. The missing layer was not “more natural-language description”; it was an executable semantic control surface that can distinguish:

- literal source from normalized text;
- symbol from meaning;
- local meaning from cross-repo reuse;
- assertion from condition, procedure, hypothesis and goal;
- ambiguity from equivalence;
- semantic formalization from algebraic equivalence;
- analogy from evidence;
- documentation from implementation;
- implementation from execution;
- execution from evidence;
- evidence from publishable claim.

The semantic layer therefore acts as a **typed impedance matcher** between heterogeneous materials.

## 2. Support arms S0→S12

| Arm | Computational strategy | Persistent artifact | Hard gate |
|---|---|---|---|
| S0 Source identity | content-address provider/ref/path/blob/span; alias-aware identity | source pointer + blob/span | orphan semantics forbidden |
| S1 Surface preservation | lossless literal storage; NFC only in derived field | `surface.text` + normalization mode | derived text never overwrites source |
| S2 Symbol table | local scoping, shadowing, overload detection, unit/domain candidates | scoped symbol records | same glyph is not same object by default |
| S3 Scope/modality | encode condition, negation, temporality, locality, procedural vs asserted state | scope packet | procedure/hypothesis cannot become fact by parsing |
| S4 Ambiguity | maintain alternative readings + discriminating tests | ambiguity lattice | unresolved reading cannot enter E2 equivalence |
| S5 Grounding | source-explicit / reversible lift / derived typed / uninterpreted | canonical-form candidate + witness + gaps | derived grounding requires provenance witness |
| S6 Relation graph | typed edge vocabulary with `evidence_effect` and `promotion_cap` | semantic relation edges | analogy/co-occurrence cannot promote proof |
| S7 Domain engine | route to logic, number theory, recurrence, continuous, modular, GF(2), graph/set or feature engine | route + guards | no universal simplifier across domains |
| S8 Implementation binding | bind repo/ref/path/blob/function; use code symbols/call graph | implementation edge | doc similarity is not implementation |
| S9 Execution evidence | exact runtime, environment, command, exit state, result/stdout digest | execution receipt | code without run remains IMPLEMENTED |
| S10 Falsification | counterexamples, mutation tests, property/metamorphic tests, negative controls | falsifier/negative-control ledger | no falsifier => promotion capped |
| S11 Memory/custody | append-only deltas + longitudinal and orthogonal indices | custody event + indices | corrections append; history not rewritten |
| S12 Claim promotion | evidence matrix + independent review + server-side governance | promotion receipt | `claim_allowed=false` by default |

## 3. Semantic IR

Each semantic packet is a small intermediate representation:

```text
source
→ surface
→ semantic{class,domain,scope,ambiguity}
→ grounding{state,canonical_form,witness,gaps}
→ relations{operator,evidence_effect,promotion_cap}
→ operational{route,implementation,execution,evidence,falsifier,next_gate}
→ epistemic{state,claim_allowed,proof_boundary}
```

This IR is deliberately richer than a formula AST. A formula AST cannot represent that `↔` is undefined, that `+` is feature composition rather than addition, that an “if” may be implicit, or that a pipeline is procedural rather than algebraic.

## 4. Specialized computational engines

### Predicate / logic

Objects: conditions, biconditionals, set predicates, quantifiers.  
Methods: bounded truth tables, witness/counterexample search, explicit predicate signatures.  
Forbidden shortcut: converting linguistic adjacency into implication without a source/producer witness.

### Number theory

Objects: integer sequences, divisibility, primality, congruences.  
Methods: exact integer arithmetic, factorization witnesses, range verifiers plus formal proof.  
Boundary: a finite verifier supports but never replaces a general proof.

### Discrete recurrence

Objects: `x_{n+1}=F(x_n,...)`, deltas and cumulative states.  
Methods: residual identities, index shifts, reverse-roundtrip, antidifferences.  
Boundary: continuous derivative is a secondary analytic extension, not native semantics.

### Real/complex continuous

Objects: typed scalar/vector functions.  
Methods: symbolic differentiation, finite-difference cross-check, branch and singularity probes, Jacobian/Hessian where typed.  
Boundary: domain and branch declaration precede simplification.

### Modular finite

Objects: `Z_m`, residue tuples, finite orbits.  
Methods: exhaustive enumeration when tractable, generalized CRT compatibility, preimage cardinality, minimum-period tests.  
Boundary: inverse modulo a period is not a unique inverse over all integers.

### Boolean/GF(2)/coding

Objects: bit-vectors, XOR, parity, syndrome, decoder branches.  
Methods: exhaustive truth tables at bounded widths, single/multiple-error controls, decoder roundtrip.  
Boundary: XOR by a known mask is reversible; a state→mask function need not be invertible.

### Set/graph structural

Objects: set builders, preimages, graph relations, routes.  
Methods: membership checks, dangling-edge checks, reachability, cycle rank/topological invariants.  
Boundary: reverse traversal is not automatically a functional inverse.

### Feature/sensor pipeline

Objects: HRV/GSR/etc. feature compositions and pipelines.  
Methods: schema/unit checks, windowing and normalization freeze, channel permutation, missing-channel and replay controls.  
Boundary: `A+B` in prose is not arithmetic until aligned scalar definitions and units exist.

## 5. Ambiguity is executable state

Ambiguity is not a note. It has:

```text
state
alternatives[]
selected_reading?
discriminator for each alternative
```

A discriminator is a future test or source fact capable of killing at least one interpretation.

Example:

```text
Sincronia 963↔999
```

remains three possible objects:

1. symbolic bidirectional association;
2. coupled-frequency dynamical relation;
3. experimental comparison between frequency conditions.

Until an observable/operator/protocol discriminates them, it remains `TOKEN_VAZIO` for mechanism and scientific claim.

## 6. Proof-cap relation algebra

Edges are not all equal.

```text
EXACT_ALIAS
DEFINITIONAL_EQUIV
FORMAL_REWRITE
CHANGE_OF_VARIABLES
IMPLEMENTS
EXECUTES
EVIDENCES
REFUTES
CORRECTS
SUPERSEDES
DERIVED_FROM
DEPENDS_ON
PRECONDITION
METHOD_SHARED
FORMAL_ANALOGY
CO_OCCURS
```

Rules:

```text
FORMAL_ANALOGY / METHOD_SHARED / CO_OCCURS
    => automatic proof promotion = 0

DEFINITIONAL_EQUIV / FORMAL_REWRITE / CHANGE_OF_VARIABLES
    => require witness

IMPLEMENTS
    => requires code binding

EXECUTES
    => requires runtime receipt

EVIDENCES / REFUTES / CORRECTS / SUPERSEDES
    => requires evidence reference
```

## 7. Cross-support feedback, not one-way pipelines

The strategy is recursive:

```text
ambiguity → symbol table
grounding witness → ambiguity resolution
producer code contradiction → downgrade semantic reading
runtime contradiction → reopen implementation binding
counterexample → REFUTES/CORRECTS edge
provider drift → new longitudinal source event
promotion failure → return to falsifier/evidence layer
```

Nothing is silently overwritten. Every correction is a new edge/event.

## 8. Bounded E1B semantic materialization

Six actual unresolved/derived objects are now represented as semantic packets:

- `F01`: conditional recovery relation; two readings retained.
- `F02`: Rafaeliana primality biconditional; source-resolved formal predicate.
- `F03`: cross-domain shared-test set; formal set-builder with domain-specific `WellDefined`.
- `F06`: piecewise decoder; second-lane predicate remains typed unknown.
- `F08`: `Sincronia 963↔999`; uninterpreted relation with three discriminating readings.
- `F10`: `HRV + condutância dérmica`; source context selects feature-vector composition, not numeric addition.

## 9. Retrieval / memory strategy

Every semantic object is retrievable orthogonally by:

```text
source
blob
span
semantic class
domain
symbol
ambiguity state
grounding state
relation operator
implementation ref
execution ref
evidence ref
falsifier
gap
time
```

and longitudinally by:

```text
source → reading → grounding → relation → implementation → run → evidence → correction/claim
```

The two views are complementary, not additive counts.

## 10. CI gate

`semantic-support-gate-v1.yml`:

1. compiles validator/tests;
2. runs negative and positive fail-closed fixtures;
3. validates all bounded semantic packets;
4. writes a deterministic report;
5. hashes schema, contract, packets, validator, tests and output;
6. uploads the audit artifact.

The validator proves **contract consistency**, not semantic/scientific truth.

## 11. Operational strategy for the next vertical

Highest-value next work:

```text
F01 → locate exact producer `check` semantics → bind control-flow function → fixture
F06 → freeze P0/P1 + second-lane check → exhaustive bounded decoder test
F02 → bind exact verifier commit/runtime → receipt
F03 → instantiate WellDefined in two actual domains → membership negative control
F10 → freeze feature schema/windowing/units/privacy → deterministic fixture
F08 → remain TOKEN_VAZIO until observable + intervention + baseline + falsifier exist
```

This ordering maximizes closure per unit of work while preventing semantic uncertainty from leaking into execution.

## R3

**F_ok:** executable semantic-support contract, schema, six source-bound packets, fail-closed validator/tests and CI gate are materialized.  
**F_gap:** producer bindings for F01/F06/F10, runtime receipt for F02, concrete domain instantiation for F03, and scientific observable/protocol for F08.  
**F_next:** run CI → inspect receipt → bind F01/F06 producer code → exhaustive decoder fixture → semantic relation-index materialization → connect `interpret_context` to packet-in/packet-out instead of free-form text.
