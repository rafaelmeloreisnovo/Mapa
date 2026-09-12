# RAFAELIA Replay Contract V1

**State:** IMPLEMENTED_DRAFT  
**claim_allowed:** false

## Purpose

This contract turns reconstruction from a vague verb into a typed, fail-closed operation.

```text
RECONSTRUCT(
  base_state,
  event_log,
  provenance,
  boundary,
  operator_versions,
  causal_order,
  reconstruction_metric
)
-> PASS_EXACT | PASS_STRUCTURAL | PASS_SEMANTIC | PASS_PROVENANCE | PARTIAL | FAIL | TOKEN_VAZIO
```

It does not replace the μ-event layer, operational ontology, START HERE, or NOVOexport receipts. It binds them.

## P0 clauses

1. **Boundary / initial condition**
   - replay must name its base state, boundary kind, constants and assumptions;
   - unresolved constants remain `TOKEN_VAZIO`.

2. **Reconstruction metric**
   - exact bytes, structure, semantic equivalence and provenance-only are different levels;
   - `PASS_EXACT` requires equal non-empty hashes.

3. **Unicode identity**
   - raw text is preserved;
   - NFC may be used only as an index;
   - confusables such as `Δ` and `∆` remain distinct unless an evidence-backed alias is declared.

4. **Operator version**
   - each replayed operator has an explicit version and binding state;
   - a historical formulation is not an executable/formal binding.

5. **Partial order / causality**
   - Drive, GitHub, user, assistant and tools may emit parallel deltas;
   - event ancestry is represented as a causal DAG, not inferred from a lone sequence number.

6. **TOKEN_VAZIO coercion**
   - forbidden silent coercions: `0`, `false`, `null`, empty string, missing, default;
   - `SEARCH_MISS != ABSENCE`.

7. **Source independence**
   - aliases or shared ancestry do not count as independent evidence;
   - lineage IDs and deduplication are required before replication counts.

## P1 clauses

- semantic dictionary corrections are `APPEND + SUPERSEDES`;
- semantic conflicts `FORK` until resolved;
- snapshots must point to canonical source + revision + hash and become stale rather than silently canonical;
- append-only loops have explicit stop conditions;
- negative controls/counterexamples are required;
- reconstructibility does not imply retention/publication of raw private content;
- the 56 parables are pedagogical lenses, not official teachings or cultural authority.

## P2 clauses

- weighted paths stay disabled/`TOKEN_VAZIO_CALIBRATION` until calibration;
- human semantic validation remains `ABORTED_UNTIL_ETHICS` until independent ethics/privacy review and consent.

## NOVOexport binding

Observed ingestion receipts preserve these anti-promotion rules:

```text
SEARCH_MISS != ABSENCE
DERIVED_SAMPLE != RAW_SHARD
LOCAL_PARSE_PASS != FAMILY_COMPLETE
UNTESTED != SURVIVED
TOKEN_VAZIO != ZERO
```

The replay contract imports these as invariants. It does not claim complete raw-shard coverage.

## PLECT observation

A historical Drive source defines:

```text
PLECT = Permutation-Linked Correlated Topology
```

with a candidate construction based on topology-defined permutations and weighted aggregation.

Current classification:

```text
source_bound = true
formal_binding = false
binding_state = PROVISIONAL_SOURCE_BOUND
```

Therefore PLECT can be cited as a historical conceptual operator, but cannot yet participate as a formal replay operator until versioned semantics and tests are added.

## Application to existing operational ontology records

| Record | Prior editorial state | Current overlay | Still open because |
|---|---|---|---|
| R-ANTIDERIVATIVE-BOUNDARY | IGNORED | CONTRACT_MATERIALIZED_DRAFT | boundary-sensitive deterministic replay not executed |
| R-SOURCE-INDEPENDENCE | SUGGESTED | CONTRACT_MATERIALIZED_DRAFT | cross-source lineage authority incomplete |
| R-VECTOR-CORPUS | WITHHELD | ACCESS_BOUND_CONTRACT_APPLIED | authorized chunk manifest incomplete |
| R-SEMANTIC-HUMAN-STUDY | ABORTED | ABORTED_PRESERVED | ethics/privacy/consent absent |
| R-WEIGHTS-CALIBRATION | POTENTIAL | WEIGHTS_DISABLED_PENDING_CALIBRATION | no blinded benchmark/ground truth |
| R-BOOTSTRAP-UQ | SUGGESTED | UNCERTAINTY_GATE_DECLARED | no deterministic fixed-seed fixture |
| R-FRACTAL-DIMENSION | IGNORED | FRONTIER_HYPOTHESIS_PRESERVED | estimator/null/scale interval absent |

Nothing above is silently promoted from `TOKEN_VAZIO`.

## Key equations

[
X_n = operatorname{Replay}_{v_{Delta},v_{Sigma}}(X_0,mu_{1:n},B,C)
]

Exact reconstruction:

[
H(operatorname{Replay}(cdot)) = H(X_n)
]

If the required boundary, source, operator version or event is missing:

[
operatorname{Replay} =     exttt{TOKEN\_VAZIO}
]

## Files

- `schemas/replay-contract.v1.schema.json`
- `data/contracts/replay-contract.v1.json`
- `tools/validate_replay_contract.py`
- `tests/test_replay_contract.py`

## Gate

`IMPLEMENTED_DRAFT != PASS`.

The first promotion target is a deterministic fixture that intentionally varies one boundary and proves that incompatible boundaries cannot both be promoted as the same reconstruction.
