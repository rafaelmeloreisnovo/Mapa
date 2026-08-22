# RAFAELIA — Calculation Memory Index Ω — V4 — 2026-08-22

**State:** `E0_CLOSED_BOUNDED / E1_OBJECT_ROUTING_CLOSED / E1_FORMULA_STRUCTURAL_CLOSED_TYPED / E2_DOMAIN_ROUTED / CALCULUS_BATCH02_PASS / claim_allowed=false`  
**Predecessor:** `indices/RAFAELIA_CALCULATION_MEMORY_INDEX_V3_20260822.md`  
**Base snapshot at cycle start:** `Mapa/main@44cb3cefdb0434b8f3c6f7361cb9c3850dbb7381`

## 1. Persistent anchors

Drive:

- calculation-memory document: `1ELvmzr2cltIayFrJmY1ZHzbWgjl6OJ2AkmBu3UoaivU`
- operational spreadsheet: `1HDaHo5IBj42rr-iyxftG1zfaEzzCI9xC4s_0W_-1vR8`
- new sheets: `E1_TYPED_CLOSURE_V3_20260822`, `E1B_SEMANTIC_FORMALIZATION_V1`, `E2_DOMAIN_ROUTING_V1`, `MCM_CALCULUS_BATCH02_P1_P7`

GitHub receipts:

- `data/reconciliation/OMEGA_FORMULA_E1_TYPED_CLOSURE_V3_20260822.v1.json`
- `data/reconciliation/OMEGA_FORMULA_E1B_SEMANTIC_FORMALIZATION_20260822.v1.json`
- `data/reconciliation/OMEGA_FORMULA_E2_DOMAIN_ROUTING_20260822.v1.json`
- `data/reconciliation/OMEGA_MCM_CALCULUS_BATCH02_P1_P7_20260822.v1.json`
- `data/receipts/OMEGA_MCM_SPIRAL_R_003_EXECUTION_20260822.v1.json`

## 2. E1 closure is typed, not forced

The bounded denominator remains:

```text
E0 exact identities = 356
```

Structural state after E1A + E1B:

```text
E1A direct/reversible structural AST = 340
E1B provenance-preserving semantic formalizations = 6
formula-like objects with structural representation = 346 / 346
non-formula objects explicitly routed = 10
all E0 objects with a typed route = 356 / 356
```

The ten non-formula objects are operational pipelines, experiment protocols, transformation routes or labels. They are intentionally excluded from formula-AST equivalence.

The six E1B records preserve exact source text and introduce derived representations only with explicit `DERIVED_*` provenance. Uninterpreted predicates/operators remain typed gaps rather than invented semantics.

Examples:

- `R_n is prime iff n in {1,3}` -> `Iff(Prime(R_n),Member(n,{1,3}))`, backed by the formal number-theory source;
- `C(A,B)={j:test j is well-defined in both A and B}` -> typed set-builder with `WellDefined` preserved as a domain-dependent predicate;
- `Sincronia 963↔999` -> `Relation(SYNC_UNDEFINED,963,999)`, not a scientific or algebraic claim;
- `HRV + condutância dérmica` -> feature composition candidate, explicitly **not** numeric addition until units/feature scaling are defined.

## 3. E2 domain routing

A primary next-engine routing candidate was assigned across the bounded E0 denominator, with counts reconciling to 356:

| Route candidate | Count |
|---|---:|
| ALGEBRAIC_GENERIC | 102 |
| REAL_COMPLEX_CONTINUOUS | 40 |
| MODULAR_FINITE | 39 |
| SET_GRAPH_STRUCTURAL | 29 |
| DISCRETE_RECURRENCE | 25 |
| SYMBOLIC_REWRITE | 25 |
| NUMERIC_OR_CLAIM_RELATION | 20 |
| NUMBER_THEORY | 20 |
| BOOLEAN_GF2_CODING | 19 |
| SYMBOLIC_UNTYPED | 13 |
| COMBINATORIAL_DISCRETE | 11 |
| OPERATIONAL_NON_FORMULA | 10 |
| PREDICATE_LOGIC | 1 |
| SET_LOGIC | 1 |
| FEATURE_COMPOSITION | 1 |

This is a **routing classification**, not proof that every object has that mathematical domain.

Invariant:

```text
one global simplifier across all domains = FORBIDDEN
```

For example, real/complex calculus, modular arithmetic, XOR/GF(2), rewrite grammars, graph morphisms and integer factorization require different equivalence engines.

`E2_GLOBAL` therefore remains `TOKEN_VAZIO` while family-specific E2 gates are executed.

## 4. Calculus Batch02 — source-bound P1..P7

Source:

`rafaelmeloreisnovo/Matem-tica-/papers/2026-05-23_adendo_sete_possibilidades_0001123.md`

with

```text
q = sqrt(3)/2
P1(n)=q^n
P2(n)=n q^n
P3(n)=n^2 q^n
P4(n)=log(n+1) q^n
P5(n)=log(log(n+e)) q^n
P6(n)=q^n/(n+1)
P7(n)=phi^n q^n
```

Because the source parameter is discrete, `Delta` is the native derivative operator. The continuous `n -> x` versions are secondary analytic extensions only.

### Native finite differences

```text
Delta P1 = (q-1)q^n
Delta P2 = q^n[(q-1)n+q]
Delta P3 = q^n[(q-1)n^2+2qn+q]
Delta P4 = q^n[q log(n+2)-log(n+1)]
Delta P5 = q^n[q log(log(n+1+e))-log(log(n+e))]
Delta P6 = q^n[q/(n+2)-1/(n+1)]
Delta P7 = (phi q-1)(phi q)^n
```

### Closed antidifferences proved by symbolic `Delta Q=P`

```text
Q1 = q^n/(q-1) + C
Q2 = q^n[n/(q-1)-q/(q-1)^2] + C
Q3 = q^n[n^2/(q-1)-2qn/(q-1)^2+q(q+1)/(q-1)^3] + C
Q7 = (phi q)^n/(phi q-1) + C
```

Verification harness SHA-256:

`df8cd950f826df1e51061db97eacebe9e858c87cfcfbf2ad6cd8ce248e9028d8`

P4/P5/P6 retain exact finite-sum antidifferences. They are **not** given fabricated elementary discrete primitives.

### Continuous analytic extension

All seven received derived continuous derivative forms with domain guards. This does not change the source-native discrete status.

For P7:

```text
phi*q = 1.4012585384440734 > 1
```

so the family is exponentially expansive without normalization, matching the source warning.

## 5. Formula -> implementation -> execution state

The earlier source pair

```text
r_{n+1}=(sqrt(3)/2)r_n
theta_{n+1}=theta_n+pi/phi
```

has a bounded radial implementation/execution bridge to `GAIA_phi/dados/RAFAELIA_TRIG_CORE2.py` with residual approximately `5.55e-17`.

However the inspected angular producer uses `2*pi/steps_per_turn`, and another inspected bridge uses `2*pi/phi^2`. Neither is the same source law as `pi/phi`.

Therefore:

```text
RADIAL_IMPLEMENTATION = EXECUTED_LIMITED_PASS
ANGULAR_IMPLEMENTATION = GAP_NOT_SAME_FORM
FULL_SPIRAL_SOURCE_PAIR = PARTIAL_ONLY
```

A producer search for explicit P1..P7 naming found the `P7(n)` family in the mathematics source but no explicit matching P7 implementation in the inspected producer repository set. This is **not** a global absence claim; implementation linkage for P2..P7 remains `TOKEN_VAZIO_IMPLEMENTATION` until a producer path is bound.

## 6. Current route

```text
E0 exact identity
-> E1A safe structural AST
-> E1B provenance-preserving derived formalization
-> typed non-formula routing where appropriate
-> E2 domain router
-> family-specific equivalence engine
-> native derivative/difference
-> native antidifference/primitive/inverse/preimage
-> implementation binding
-> execution receipt
-> evidence/falsifier
-> claim gate
-> append-only memory
```

## 7. R3

**F_ok:** bounded E0 remains 356; all 356 objects have typed structural routes; all 346 formula-like objects now have E1A/E1B structural representations; E2 has a reconciled 356-object next-engine routing; Calculus Batch02 closes native finite differences for P1..P7 and symbolically verifies closed antidifferences for P1/P2/P3/P7; the radial Spiral√3/2 implementation has bounded execution evidence.  

**F_gap:** E2 mathematical equivalence remains family-partial; route classification is not domain proof; P2..P7 implementation bindings are not established in the inspected producer set; the source `pi/phi` angular law still lacks a matching inspected producer; global Drive/GitHub formula exhaustivity remains `TOKEN_VAZIO`.  

**F_next:** run E2 on high-confidence families (number theory, recurrence, modular/GF2 separately) -> bind P1..P7 producers -> execute those producers -> Calculus Batch03 on the next source-bound families -> continue formula->implementation->execution->evidence memory.
