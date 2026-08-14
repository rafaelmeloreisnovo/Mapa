# RAFAELIA — Hypothesis Index V6

Date: 2026-08-14  
Mode: `APPEND_ONLY_BY_REFERENCE`  
State: `GOVERNED_PARTIAL / NONTERMINAL / claim_allowed=false`

Extends: `indices/RAFAELIA_HYPOTHESIS_INDEX_V4.md`

## Frontier after HYP_CKPT_0006

| View | Count | Boundary |
|---|---:|---|
| Session-local mathematical families audited | 13 | local genealogy only |
| Mathematical M2 survivors | 3 | current mathematical novelty candidates |
| Delta 0001 | 6 | normalized records |
| Delta 0002 | 10 | normalized records |
| Delta 0003 | 8 | normalized records |
| Delta 0004 | 2 | normalized records |
| Delta 0005 | 10 | normalized records |
| Delta 0006 | 12 | normalized records |
| Represented substantive hypothesis IDs | **51** | provisional ledger frontier |
| External geophysical comparators | 6 | separate; not project/authorial count |
| Explicit AUTHORIAL_PROPOSITION IDs already classified in migrated sources | at least 2 | lower bound only, not total |
| Certified authorial-only total | `TOKEN_VAZIO` | origin migration incomplete |
| Certified global unique hypotheses | `TOKEN_VAZIO` | coverage/dedup terminality incomplete |
| Mathematical M3 | 0 | current audited scope |
| Mathematical M4 | 0 | current audited scope |

**51 is a ledger frontier, not the certified global answer.**

## Origin policy

Canonical: `data/hypotheses/RAFAELIA_HYPOTHESIS_ORIGIN_POLICY.v1.json`

Required partitions:

- `AUTHORIAL_PROPOSITION`
- `PROJECT_DERIVED_PROPOSITION`
- `EXTERNAL_REFERENCE_HYPOTHESIS`
- `HISTORICAL_INTERNAL_CLAIM`
- `NULL_HYPOTHESIS`
- `BASELINE_MODEL`
- `INFERRED_NORMALIZATION`
- `INTERPRETIVE_SYMBOLIC`

Hard boundary:

```text
ORIGIN != NOVELTY
PROJECT_OWNERSHIP != ACADEMIC_ORIGINALITY
EXTERNAL_REFERENCE != USER_HYPOTHESIS
NULL != SUBSTANTIVE_ALTERNATIVE
BASELINE != CLAIM
```

## Delta 0006

### GAIA

- `HYP-COMP-GAIA-HEX6-040` — structured two-square directions versus random-angle baseline — `ACTIVE_UNTESTED`.
- `HYP-COMP-GAIA-FIBPHI-MSE-041` — Fibonacci/phi modulation versus plain damped-sine synthetic baseline — `ACTIVE_UNTESTED`; synthetic-task scope only.
- `HYP-COMP-GAIA-GRAPHCLUSTER-042` — ring+chords clustering versus ER baseline — `ACTIVE_UNTESTED`.

The implementation defines hypothesis + metric + baseline + hashable log format. A root `logs` directory was not found in the current pass, so execution receipts for these three tracks remain `TOKEN_VAZIO`.

### ChipQuantum — explicit authorial geometry

- `HYP-MATH-CHIP-SQUARE-EQUIL-OVERLAP-043` — square/equilateral overlap model — `AUTHORIAL_PROPOSITION / BLOCKED_BY_DEPENDENCIES`.
- `HYP-MATH-CHIP-TORUS30-15-044` — 30-degree torus projection approximated by composition of two 15-degree layers — `AUTHORIAL_PROPOSITION / BLOCKED_BY_DEPENDENCIES`.

The source itself marks these as authorial model/hypothesis while separating classical identities. That supports **origin**, not M3/M4 novelty.

### ChipQuantum — substantive ledger propositions

- `HYP-MATH-CHIP-T7-INVARIANT-045` — T7 integral invariant conserved along orbits — `PROOF_OBLIGATION`.
- `HYP-APPLIED-CHIP-LASER-TORUS-046` — coupled-laser phases admit a useful toroidal mapping — `BLOCKED_BY_DEPENDENCIES`.
- `HYP-COMP-CHIP-LASER-SYNC200-047` — attractor control synchronizes in <200 iterations — `TOKEN_VAZIO`.
- `HYP-COMP-CHIP-LASER-PID-048` — toroidal/attractor control beats matched PID — `BLOCKED_BY_DEPENDENCIES`.
- `HYP-ML-CHIP-HEX-PARAM-049` — hexagonal NN reduces parameters while maintaining accuracy — `ACTIVE_UNTESTED`.
- `HYP-EMP-CHIP-NEURO-HEX-050` — biological neural-efficiency hypothesis for hexagonal organization — `BLOCKED_BY_DEPENDENCIES`.
- `HYP-COMP-CHIP-BALLTREE-TORUS-051` — toroidal Ball Tree faster than exact naive scan at equivalent intrinsic-distance result — `ACTIVE_UNTESTED`.

## Dedup decisions

- ChipQuantum `P1-C002 exactly 42 attractors` → source edge to existing Ω42 cluster; **no new ID**.
- GAIA geometry `040`, square/equilateral `043`, torus projection `044` → related but **not merged**.
- T7 invariant `045` → pending equivalence check against canonical formula registry.
- AI hex efficiency `049` and biological neural efficiency `050` → **distinct**.
- laser chain `046 → 047 → 048` → hierarchical dependencies, not duplicates.

## External comparator partition

`data/hypotheses/external/RAFAELIA_EXTERNAL_HYPOTHESIS_COMPARATORS.v1.json`

Six Fisica geophysical mechanisms are tracked as external comparators and excluded from authorial/project-substantive counts by default. The 13 literature records behind them are references/evidence records, not 13 additional owned hypotheses.

## Checkpoints

```text
CKPT0001 -> frontier 9
CKPT0002 -> frontier 19
CKPT0003 -> frontier 27
CKPT0004 -> frontier 29
CKPT0005 -> frontier 39 + 6 external comparators separately
CKPT0006 -> frontier 51 + origin-aware partition
```

## F_gap

- `FG-HYP-001 GLOBAL_COVERAGE` — `IN_PROGRESS`.
- `FG-HYP-002 CANONICAL_IDENTITY_AND_DEDUP` — `IN_PROGRESS`.
- `FG-HYP-003 CLASSIFICATION_HARMONIZATION` — `PARTIAL`.
- `FG-HYP-004 EVIDENCE_LINKAGE` — `IN_PROGRESS`.
- `FG-HYP-005 PRIOR_ART_AND_GENEALOGY` — `PARTIAL`.
- `FG-HYP-006 EXECUTION_AND_FALSIFICATION` — `IN_PROGRESS`.
- `FG-HYP-007 TERMINALITY_AND_GLOBAL_COUNT` — `OPEN_TOKEN_VAZIO`.

## Next cursor

`HYP_CKPT_0007_PRIVATE_GAIA_RECEIPTS_CHIPQUANTUM_PAPER6_AND_ORIGIN_MIGRATION`
