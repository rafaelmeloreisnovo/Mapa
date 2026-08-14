# RAFAELIA — Hypothesis Index V4

Date: 2026-08-14  
Mode: `APPEND_ONLY_BY_REFERENCE`  
State: `GOVERNED_PARTIAL / NONTERMINAL / claim_allowed=false`

Extends: `indices/RAFAELIA_HYPOTHESIS_INDEX_V2.md`

## Frontier after HYP_CKPT_0004

| Layer | Count | Meaning |
|---|---:|---|
| Mathematical families in session-local genealogy | 13 | audited local scope, not global universe |
| Mathematical M2 survivors | 3 | current mathematical novelty candidates |
| Delta 0001 | 6 | normalized cross-domain records |
| Delta 0002 | 10 | normalized cross-domain records |
| Delta 0003 | 8 | ZIPRAF + memory records |
| Delta 0004 | 2 | hardware-signal + RMRCTI association records |
| Represented hypothesis IDs | **29** | provisional ledger frontier |
| Certified global unique hypotheses | `TOKEN_VAZIO` | terminality not reached |
| Mathematical M3 | 0 | current audited scope |
| Mathematical M4 | 0 | current audited scope |

**29 is not the answer to the global-total question.** It is the count of currently represented normalized IDs after four controlled checkpoints.

## New in Delta 0003

- `HYP-COMP-ZIPRAF-SEEDMATRIX-020` — Bitraf64 seed/KDF reproducible matrices — `TOKEN_VAZIO`.
- `HYP-METH-ZIPRAF-TOROSPIRAL-021` — torus+spiral traversal utility — `ACTIVE_UNTESTED`.
- `HYP-COMP-ZIPRAF-SYNDROME-COMP-022` — sparse majority/syndrome compression — `ACTIVE_PARTIAL_EVIDENCE` (reconstruction algebra supported; corpus compression gain unproven).
- `HYP-COMP-ZIPRAF-COMP2X5X-023` — declared 2–5x compression — `ACTIVE_UNTESTED / source DECLARED_UNVERIFIED`.
- `HYP-COMP-ZIPRAF-ETHICA-LT1MS-024` — declared Ethica latency <1 ms — `ACTIVE_UNTESTED / source DECLARED_UNVERIFIED`.
- `HYP-COMP-ZIPRAF-GAIN30_70-025` — declared 30–70% gain — `BLOCKED_BY_DEPENDENCIES` because component/metric/baseline are not frozen.
- `HYP-COMP-ZIPRAF-TAMPER100-026` — 100% tamper detection — `BLOCKED_BY_DEPENDENCIES` pending bounded threat model.
- `HYP-COMP-ERASURE-40_45-027` — exact payload recovery under 40–45% erasure budget — `ACTIVE_UNTESTED`.

## New in Delta 0004

- `HYP-HW-ERROR-SIGNAL-028` — repeatable hardware error/hot-state observations as degradation signal without treating corrupt data as valid payload — `ACTIVE_UNTESTED`.
- `HYP-STAT-RMRCTI-PEAK-STABILITY-029` — peak membership associated with `stable_any` beyond exact fixed-margin independence null — `ACTIVE_UNTESTED`.

## Important alias/dedup decisions

### Four-inks recovery alias

`SV-HYP-001` did **not** create another hypothesis ID. It is an additional source expression for `HYP-COMP-ERASURE-40_45-027`.

Reason: both concern strategic 40–45% loss and reconstruction; the registry statement is the stricter form requiring exact payload/digest equality.

### RMRCTI hierarchy

`HYP-STAT-RMRCTI-PEAK-STABILITY-029` and `HYP-EMP-HETE018-019` remain distinct:

```text
association against exact null
    ↓ stronger requirement
repeatability/stationarity near 0.18
    ↓ stronger requirement
parameter basin + perturbation return
    ↓ stronger requirement
dynamical attractor
```

The repository currently documents formula and falsifier machinery, but real provenance-fixed traces are still required before promotion.

### BITRAF family

Three related objects remain distinct:

1. `HYP-M2-BITRAF64-F2-001` — finite algebraic transformation candidate;
2. `HYP-COMP-ZIPRAF-SEEDMATRIX-020` — deterministic seed-expansion protocol;
3. `HYP-EMP-BITRAF-PHYSRES-008` — empirical physical-residue model.

Same vocabulary is not semantic identity.

### ZIPRAF compression family

- sparse syndrome regime (`022`)
- broad historical 2–5x benchmark (`023`)

remain separate pending an exact benchmark protocol/equivalence proof.

## Evidence edges strengthened

### Semantic Parable Codec — `HYP-METH-PARABLE-CODEC-018`

Implementation observed in ZIPRAF:

- deterministic versioned codebook;
- exact syntactic roundtrip;
- explicit `claim_allowed=false`;
- corruption rejection;
- `TOKEN_VAZIO` preserved;
- no claim of human semantic equivalence.

Tests cover these protocol properties. This is an implementation/test edge, **not** proof of the methodological H1 about human semantic loss.

### RMRCTI / HETE

Canonical source resolved to `rafaelmeloreisnovo/llamaRafaelia/rmrCti`.

Observed layers:

- `Delta P = P(stable_any=1 | peak) - P(stable_any=1 | nonpeak)` is documented;
- cumulative lift implements terminal identity `I_N = Delta P`;
- fixed-margin hypergeometric null is implemented exactly;
- rejecting that null supports association only;
- causality, universal constant, path invariant and dynamical attractor remain `TOKEN_VAZIO`;
- repository contract says L0 is established by inspection; L1+ require generated real-trace reports.

## Custody / operation errata

During branch-only registry work, accidental placeholder paths were introduced and immediately removed from the proposed diff. They are preserved transparently in commit history and explicit errata files:

- `data/evidence/hypotheses/RAFAELIA_HYPOTHESIS_REGISTRY_CKPT_0002_OPERATION_ERRATA.v1.json`
- `data/evidence/hypotheses/RAFAELIA_HYPOTHESIS_REGISTRY_CKPT_0002_OPERATION_ERRATA_ADDENDUM.v1.json`

No merge/release/main mutation is represented by those incidents.

## Checkpoints

- `HYP_CKPT_0001` — initial cross-domain sources and 9-ID frontier.
- `HYP_CKPT_0002` — papers/RLL expansion and 19-ID frontier.
- `HYP_CKPT_0003` — ZIPRAF/memory expansion and 27-ID frontier.
- `HYP_CKPT_0004` — four-inks exact extraction + RMRCTI source resolution and 29-ID frontier.

## F_gap

- `FG-HYP-001` coverage: **IN_PROGRESS**.
- `FG-HYP-002` identity/dedup: **IN_PROGRESS**.
- `FG-HYP-003` classification: **PARTIAL**.
- `FG-HYP-004` evidence linkage: **IN_PROGRESS**.
- `FG-HYP-005` prior art/genealogy: **PARTIAL**.
- `FG-HYP-006` execution/falsification: **IN_PROGRESS**.
- `FG-HYP-007` terminality/global count: **OPEN_TOKEN_VAZIO**.

## Next cursor

`HYP_CKPT_0005_PAPERS_REMAINING_HYPOTHESIS_HITS_ZIPRAF_SECURITY_RECEIPTS_AND_DOMAIN_COVERAGE_MAP`
