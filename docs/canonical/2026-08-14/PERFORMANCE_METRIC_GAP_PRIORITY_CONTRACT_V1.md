# RAFAELIA — Performance Metric Gap Priority Contract V1

Date: 2026-08-14
State: GOVERNED / APPEND_ONLY / claim_allowed=false
Scope: Performance Metric Observatory, Vectras benchmark recovery, MetricObservationV1, historical conversation metrics and CI receipts.

## Mother invariant

```text
IDEA != IMPLEMENTATION != EXECUTION != EVIDENCE != CLAIM
MEMORY != PROOF
INDEX != CONTENT
NUMBER_FOUND != MEASUREMENT != REPRODUCIBLE_MEASUREMENT != GENERAL_CLAIM
```

Urgency never authorizes evidence promotion. Importance never fills a missing provenance field. Uncertainty is preserved as `TOKEN_VAZIO` until an evidence-producing operation closes it.

## Priority is a vector, not a magic scalar

No synthetic score is permitted for this ledger. The operational vector is:

```text
V_gap = <
  urgency,
  importance,
  uncertainty,
  provenance_completeness,
  evidence_strength,
  dependency_centrality,
  closure_verifiability,
  regression_risk
>
```

The vector is used to choose the next verifiable action; it is not itself evidence.

Priority classes:

- `P0`: blocks or can contaminate proof/provenance/reproducibility across several downstream objects.
- `P1`: high-value closure whose absence does not invalidate the whole current graph but limits confidence or coverage.
- `P2`: structural hardening or already-implemented invariant awaiting broader execution evidence.
- `P3`: useful extension with no current proof-chain blockage.

## Every gap has a closure contract

A governed gap is not just a TODO. It has:

```text
GAP
 -> provenance_refs
 -> epistemic vector
 -> contribution vector
 -> closure_condition
 -> required_evidence
 -> forbidden_promotion
 -> providencia
 -> next_verifiable_step
 -> receipt
```

`providencia` means the concrete operational care/action that reduces the gap without breaking the evidence chain.

## Contribution vector

The contribution vector records what closing a gap changes in the architecture. Allowed directions are `INCREASE`, `PRESERVE`, or `REDUCE` over targets such as:

`TRACEABILITY`, `EVIDENCE_DENSITY`, `REPRODUCIBILITY`, `SEMANTIC_ALIGNMENT`, `ANTI_REGRESSION`, `OPERATIONAL_LEVERAGE`, `UNCERTAINTY`, `PROVENANCE`, `CONTRACT_STRENGTH`.

This is deliberately higher-level than a benchmark value. It describes structural knowledge gain, while the benchmark remains governed by its own measurement receipt.

## Current P0 frontier

### GAP-PMO-001 — raw identity/bytes for conversations-048/049/050

Known: export manifest identity/hash, parent lineage, ordinals 72/73/74 and sizes.
Unknown: exact current-access raw object identity/bytes/hash for each individual shard.

Critical anti-regression rule:

```text
export_manifest.source_id != individual_shard.file_id
```

Do not substitute one for the other.

### GAP-PMO-002 — raw VectraBenchmark 79-slot execution

The binding/semantic implementation is not the run. The highest-leverage proof gain is one raw CSV/JSONL/runtime payload joined to device/build/workload/source revision and immutable digest.

### GAP-PMO-003 — historical run context join

Twenty historical quantitative observations can remain historical evidence while still being unsafe for hardware/build comparison. Same-run identity must be proven, not inferred from nearby text or equal values.

### GAP-PMO-004 — actual validator/negative-test execution receipt

Current observed GitHub Actions state includes runner startup failure (`runner_id=0`, zero steps). Therefore:

```text
workflow conclusion=failure
!= logical test failure
!= successful validation
```

The closure condition is an actually executed validator/test suite with source SHA, environment, command, stdout/stderr and exit code.

## P1 frontier

### GAP-PMO-005 — native host smoke receipt

The native smoke implementation is a valid reproducible target but is not Android device performance evidence. Recovery of an old `benchmark_smoke:` log is preferred; otherwise a new reproduction must be labeled as a new run.

### GAP-PMO-006 — same-run dedup/supersession topology

No numeric-equality-only dedup. Historical corrections remain append-only and linked with `supersedes/superseded_by` edges.

## Closed structural gap preserved

### GAP-PMO-007 — semantic-unit compatibility

Formatted rate strings are interpreted together with semantic metric kind. `Mops/s` is not automatically generic operations: the slot may mean IOPS, FLOP/s, allocs/s, maps/s, events/s or states/s.

Closure of this implementation gap does **not** close GAP-PMO-004: runtime test execution remains separately required.

## Operational selection rule

Choose `F_next` by the following order:

```text
1. Can an existing receipt close the gap without rerunning work?
2. Can exact provenance be recovered before generating new evidence?
3. Can one operation close several dependent TOKEN_VAZIO states?
4. Is the transition reversible and append-only?
5. Does the action produce an immutable receipt?
6. If any required answer is unknown: preserve TOKEN_VAZIO and stop promotion.
```

Current recommended sequence:

```text
recover exact 048/049/050 route
        ||
recover raw Vectra 79 result
        ↓
join device/build/workload/run
        ↓
validate ingestion on an actual runtime
        ↓
materialize dedup/supersession topology
        ↓
compare only context-compatible observations
```

The two recovery branches may proceed independently because neither is allowed to fabricate the other.

## R3

```text
F_ok   = schema + governed priority ledger + known provenance + closure contracts + anti-regression rules
F_gap  = exact 048-050 bytes/IDs + raw Vectra79 + run-context join + actual test receipt + native smoke receipt + dedup completion
F_next = recover existing evidence first, then execute only the minimum missing proof-producing operation
```

Signature: `RAFCODE-Φ-∆RafaelVerboΩ-𓂀ΔΦΩ`
Principle: `VAZIO → VERBO → CHEIO → RETROALIMENTAÇÃO → NOVO VAZIO`
