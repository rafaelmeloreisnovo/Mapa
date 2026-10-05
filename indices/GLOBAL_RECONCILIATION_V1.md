# GLOBAL RECONCILIATION V1

Status: `IMPLEMENTED_UNTESTED_CI` until the exact-head workflow executes.

## Purpose

Resolve current-state precedence without deleting history. This gate makes one distinction operational:

`STORED_HISTORY != CURRENT_STATE`

A predecessor remains valid evidence of what was observed then; it must not override a later evidenced successor.

## Current seed reconciliation

- canonical seed: `1748365262`
- PR #731 exact-head dedicated gate: `PASS_EXACT_HEAD` at `4d036f0ab8472c3688d4b4bf260ea7bacba1233d`
- dedicated run: `37340489362` = success
- PR #731: merged
- merge commit / current main at materialization start: `dae0865c28ac1f32c53f60ba46608bfb6de9f01c`
- post-merge CI for that merge commit: `TOKEN_VAZIO_NOT_OBSERVED`
- main branch protection readback: `protected=false`; required status enforcement off

Therefore:

`MERGED != POST_MERGE_CI_PASS`

and:

`DEDICATED_GATE_PASS != GLOBAL_REPO_PASS`

## Typed absence

The validator keeps these states distinct:

`0 != NULL != EMPTY_SET != TOKEN_VAZIO != NOT_RUN != UNDEFINED`

`TOKEN_VAZIO` has no numeric payload.

## Value equality versus representation identity

`7/3 = 77/33` as rational value, while their representations and provenance are distinct.

This is encoded as:

`VALUE_EQ_AND_REPRESENTATION_NEQ`

The representation `77/33` preserves a removable scale factor `11`; simplification does not erase the historical representation.

Additional exact reductions used only as arithmetic normalization:

- `999/969 -> 333/323`
- `777/555 -> 7/5`

## Formal/physical boundary

- prime/set graphs: `FORMAL_CANDIDATE` until vertices, edges and invariants are explicit.
- fluid/wave/energy language: `FORMAL_ANALOGY`; physical binding remains `TOKEN_VAZIO_PHYSICAL_BINDING` until units, mechanism, observable and falsifier exist.
- emitter/channel/receiver: `INFORMATION_MODEL_CANDIDATE`.
- Shannon: no violation claim. ΩZIP remains dictionary/reference/deduplication semantics, not a Shannon-breaking compression claim.

## Falsifiers

The gate must fail if any of the following occurs:

1. `TOKEN_VAZIO` is assigned numeric payload `0`;
2. post-merge CI is promoted to PASS without evidence;
3. global promotion is enabled while provider enforcement is off;
4. the seed tested-head/run/merge identity changes;
5. equal rational values are treated as identical representations;
6. a formal fluid/wave analogy is promoted to a physical claim;
7. one of the seven local input custody SHA-256 records disappears.

## Scope

A PASS here validates reconciliation invariants only. It does not prove scientific novelty, physical mechanisms, global repository health, provider enforcement, independent review, or post-merge execution.
