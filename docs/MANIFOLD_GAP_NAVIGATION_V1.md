# Manifold Gap Navigation V1

State: `IMPLEMENTED_ON_ISOLATED_BRANCH / FAIL_CLOSED / CI_PENDING`

## Purpose

Make absence navigable without converting absence into content.

The registry introduces stable gap nodes:

```
gap_id -> parent_gap_id -> child_gap_refs -> evidence_needed -> closure_criterion
```

A gap may therefore contain a typed **gap-of-gap**. The child gap records that the decomposition itself is unknown. It does not invent the missing decomposition.

## TOKEN_VAZIO states

- `TOKEN_VAZIO_NAVIGABLE`: the missing object is addressable and its closure condition is known.
- `TOKEN_VAZIO_NOT_RUN`: execution evidence is absent.
- `TOKEN_VAZIO_NESTED`: the missing object is itself a missing decomposition/semantic layer.
- `TOKEN_VAZIO_AMBIGUOUS`: more than one unresolved candidate remains.
- `PARTIAL_BOUNDED`: part is observed but the declared coverage is incomplete.

`TOKEN_VAZIO != 0`, and a navigable gap is still a gap.

## Catalog reduction: NP_catalog -> P_catalog

This notation is **operational catalog notation only**.

```
NP_catalog = unresolved candidate/search space before typed routing
P_catalog  = deterministically addressable route/node under a fixed index and invariants

R_catalog:
NP_catalog --[stable id + type + provenance + constraints]--> P_catalog
```

The reduction means that the **location of the unknown** can become deterministic while the unknown content remains `TOKEN_VAZIO`.

It is not a proof, conjecture, approximation, or claim that the computational complexity classes `P` and `NP` are equal.

```
P_catalog != complexity-class P
NP_catalog != complexity-class NP
NP_catalog -> P_catalog  !=  P = NP
```

## Recursive gaps

Let `G^0(x)` mean a missing value for object `x`.

```
G^(n+1)(x) = missing evidence, decomposition, mapping, grammar or authority
             required to close G^n(x)
```

Every recursive level receives a stable `gap_id`, a parent pointer and a closure criterion. Recursion must terminate operationally by one of:

1. observed closure evidence;
2. explicit bounded scope;
3. `TOKEN_VAZIO_UNDECOMPOSED`;
4. superseding successor.

## Delta channels

The schema reserves three independent delta channels:

- `ΔP_catalog`: change in deterministic routing cost/path after a verified catalog delta.
- `ΔNP_catalog`: change in unresolved candidate-space cardinality.
- `Δ§RUIDO`: residual unclassified change after the current rules have been applied.

All three remain `null` until a unit, baseline and measurement procedure are defined. A delta is not evidence merely because it is non-zero.

## Symbolic envelope

The source marker

```
⟨‡«†{★[ =SER=AO≈DE≠]★}»⟩¡¿?
```

is preserved byte-for-text as a catalog marker in `G0012`. Its operator semantics remain `SYMBOLIC_SEMANTICS_UNBOUND`. Future work may bind a grammar by successor; this version does not retrospectively invent meanings.

## Seed coverage

`G0001..G0010` are derived from already-observed open gaps in `EDGES_OMEGA_V1`.

`G0011` is the first explicit gap-of-gap: decomposition of the full-shard TieGrid `NOT_RUN` gap.

`G0012` preserves the user-supplied symbolic envelope while leaving its formal semantics empty.

## Invariants

```
SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM
TOKEN_VAZIO != 0
NAVIGABLE != FILLED
ROUTE_RESOLVED != CLAIM_VALIDATED
DELTA != EVIDENCE
NP_catalog -> P_catalog != P = NP
```

## Reproduction

```bash
python tools/validate_manifold_gap_registry.py data/manifold/gaps_omega_v1.jsonl
python tools/resolve_manifold_gap.py G0011
python -m unittest discover -s tests -p 'test_manifold*.py'
```

## R3

`F_ok`: recursive typed gaps are schema-bound, addressable and fail-closed.

`F_gap`: no quantitative ΔP/ΔNP/Δ§RUIDO metric is yet defined; exhaustive gap decomposition remains open.

`F_next`: bind gap nodes to manifold edges only after this registry passes CI, then add domain-specific decomposition one verified child at a time.

`claim_allowed=false`
