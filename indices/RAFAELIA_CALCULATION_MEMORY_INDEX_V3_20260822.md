# RAFAELIA — Calculation Memory Index Ω — V3 — 2026-08-22

**State:** `E0_CLOSED_BOUNDED / E1_STRUCTURAL_CLASSIFICATION_CLOSED / E1_AST_PARTIAL / E2_DOMAIN_PARTIAL / claim_allowed=false`  
**Predecessor:** `indices/RAFAELIA_CALCULATION_MEMORY_INDEX_V2_20260822.md`  
**Source main snapshot:** `44cb3cefdb0434b8f3c6f7361cb9c3850dbb7381`

## 1. Persistent anchors

Drive calculation memory:

- document: `1ELvmzr2cltIayFrJmY1ZHzbWgjl6OJ2AkmBu3UoaivU`
- spreadsheet: `1HDaHo5IBj42rr-iyxftG1zfaEzzCI9xC4s_0W_-1vR8`
- structural sheets: `E1_STRUCTURAL_V2_20260822`, `E1_TYPED_CLOSURE_V3_20260822`

Receipts introduced by this successor cycle:

- `data/reconciliation/OMEGA_FORMULA_E1_TYPED_CLOSURE_V3_20260822.v1.json`
- `data/receipts/OMEGA_MCM_SPIRAL_R_003_EXECUTION_20260822.v1.json`

## 2. E0 denominator preserved

```text
E0_REPRESENTATIVES_BOUNDED = 356
RAW_OCCURRENCES_S01_S05    = 374
```

The denominator remains the frozen 49-path provider-bound scan. It is not global Drive/GitHub exhaustivity.

## 3. E1 structural progression

The conservative structural parser in Drive reached:

```text
E1_STRUCTURAL_AST_V2 = 339 / 356 = 95.225%
```

A reversible uninterpreted-symbol lift was then admitted for one record:

```text
source: f(n+1)=n+n+𝒩^n+🆕
map:    🆕 <-> U_NEW
```

No semantics are attached to `U_NEW`; the transformation is only a reversible lexical carrier for AST construction.

Current typed state:

```text
E1_AST_PARSED_V3                 = 340
E1_AST_UNIQUE_V3                 = 332
E1_AST_DUPLICATE_EXTRA           = 8
DERIVED_FORMALIZATION_QUEUE      = 6
TYPED_NON_AST_OBJECTS            = 10
STRUCTURAL_CLASSIFICATION        = 356 / 356 PASS
E1_AST_GLOBAL                    = TOKEN_VAZIO
```

Therefore **classification coverage is closed while AST coverage is not**.

## 4. Why 16 records are not forced into AST

Ten records are now explicitly routed as non-AST objects such as:

- operational pipelines;
- experiment protocols;
- labels/claim candidates;
- mixed route objects;
- transformation pipelines.

Six records remain mathematical/quantitative candidates but require semantic formalization rather than lexical parsing:

1. `if check(A,B,s,P0,P1)=ok`;
2. `R_n is prime iff n in {1,3}`;
3. `C(A,B)={j:test j is well-defined in both A and B}`;
4. the prose-defined piecewise `û={...}` record;
5. `Sincronia 963↔999`;
6. `HRV + condutância dérmica`.

Each derived formalization must preserve the exact source string and carry `formalization_origin=DERIVED_CANDIDATE`.

## 5. E2 boundary

The safe rational/scalar subset currently gives:

```text
E2_RATIONAL_CANDIDATES = 19
E2_RATIONAL_UNIQUE     = 19
E2_NEW_MERGES_BEYOND_E1 = 0
E2_GLOBAL = TOKEN_VAZIO
```

E2 must be partitioned by mathematical domain. Real/continuous algebra, modular arithmetic, Boolean/GF(2), graph relations, recurrences and set predicates MUST NOT share one global simplifier.

## 6. First formula -> implementation -> execution bridge

### Source

`rafaelmeloreisnovo/teoremas/docs/rafaelia/04-spiral-raiz3-sobre-2.md`

```text
r_{n+1}=(sqrt(3)/2) r_n
theta_{n+1}=theta_n+pi/phi
```

### Producer inspected

`rafaelmeloreisnovo/GAIA_phi/dados/RAFAELIA_TRIG_CORE2.py::generate_spiral_sqrt3_over_2`

Radial producer law:

```text
r(k)=r0*(sqrt(3)/2)^k
```

Independent bounded execution over 20 steps:

```text
max radial step residual       = 5.551115123125783e-17
max recurrence/closed residual = 5.551115123125783e-17
RADIAL_GATE = PASS_NUMERIC_LIMITED
```

This is the same radial recurrence up to floating-point roundoff in the tested execution.

### Angular split

The source angular increment is:

```text
pi/phi = 1.9416110387254664
```

The inspected `TRIG_CORE2` default 20-step increment is:

```text
2*pi/20 = 0.3141592653589793
source / implementation = 6.180339887498948
```

A second inspected GAIA_phi bridge uses the golden angle:

```text
2*pi/phi^2 = 2.399963229728653
source / golden-angle implementation = 0.8090169943749475
```

Thus neither inspected angular producer is the same formula as `pi/phi`.

```text
RADIAL_IMPLEMENTATION = BOUND + EXECUTED_LIMITED
ANGULAR_IMPLEMENTATION = GAP_NOT_SAME_FORM
FULL_SPIRAL_SOURCE_PAIR = PARTIAL_ONLY
```

## 7. Calculation-memory route after V3

```text
E0 exact identity
-> structural typing
-> safe E1 AST where syntax permits
-> derived-formalization queue where semantics are needed
-> domain partition
-> E2 within compatible domain only
-> derivative / discrete delta / sensitivity
-> antiderivative / inverse / preimage / reverse
-> implementation binding
-> execution receipt
-> falsifier / evidence
-> claim gate
```

## 8. R3

**F_ok:** all 356 bounded E0 representatives are now structurally classified; 340 have safe structural ASTs; non-formula routes are no longer allowed to pollute the AST denominator; the Spiral sqrt(3)/2 radial recurrence is source-bound, producer-bound and independently re-executed with bounded numeric PASS.  

**F_gap:** six semantic-formalization candidates keep `E1_AST_GLOBAL=TOKEN_VAZIO`; E2 remains domain-partial; the source angular law `pi/phi` has no matching producer among the two inspected GAIA_phi variants; global Drive/GitHub formula exhaustivity remains `TOKEN_VAZIO`.  

**F_next:** formalize the six derived candidates with explicit provenance -> partition E2 by domain -> search/bind or implement the exact `pi/phi` angular producer -> continue MCM formula->implementation->execution bridges family by family.
