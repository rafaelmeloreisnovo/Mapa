# RAFAELIA — Forensic Origin Trace V1

**Date:** 2026-09-12  
**State:** IMPLEMENTED_DRAFT  
**claim_allowed:** false

## Purpose

Investigate origin before classification or promotion.

Historical editorial labels such as `POTENTIAL`, `SUGGESTED`, `IGNORED`, `ABORTED` and `WITHHELD` are preserved as provenance. They are not treated as root-cause diagnoses.

```text
EDITORIAL_STATUS != ROOT_CAUSE
FIRST_OBSERVED_BLOCKER != ROOT_CAUSE_PROVEN
NO_PROMOTION_BEFORE_TRACEBACK
```

## Method

The investigation runs through:

```text
READINESS
-> SCENE_SEPARATION
-> TRACEBACK
-> TIMELINE_NORMALIZATION
-> CONFLICT_TREATMENT
-> RECONSTRUCTION
-> CORROBORATION
-> REVIEW
```

The separation step keeps:

```text
SOURCE != ARTEFACT != EXECUTION != EVIDENCE != CLAIM
```

The traceback step asks, for every unresolved record:

1. where was it first recorded?
2. what prerequisite is first missing?
3. is that absence access, data, code, boundary, test, lineage or governance?
4. what evidence would fill the first missing dependency?
5. what discriminating test could show that the apparent blocker is only a symptom?
6. what alternative explanation remains?

## Historical root-origin map

| Record | Historical status | First observed blocker | Root cause state |
|---|---|---|---|
| R-DAG-CAUSAL | SUGGESTED | no executable causal DAG registered | ROOT_CAUSE_NOT_PROVEN |
| R-WEIGHTS-CALIBRATION | POTENTIAL | no blinded benchmark / ground truth | ROOT_CAUSE_NOT_PROVEN |
| R-BOOTSTRAP-UQ | SUGGESTED | no canonical fixed-seed fixture | ROOT_CAUSE_NOT_PROVEN |
| R-ANTIDERIVATIVE-BOUNDARY | IGNORED | no canonical boundary contract | ROOT_CAUSE_NOT_PROVEN |
| R-LOGLOG-COMPETITION | POTENTIAL | no out-of-sample comparison fixture | ROOT_CAUSE_NOT_PROVEN |
| R-SOURCE-INDEPENDENCE | SUGGESTED | incomplete lineage identifiers | ROOT_CAUSE_NOT_PROVEN |
| R-VECTOR-CORPUS | WITHHELD | authorized chunk manifest missing | ROOT_CAUSE_NOT_PROVEN |
| R-SEMANTIC-HUMAN-STUDY | ABORTED | ethics/consent/privacy prerequisites missing | ROOT_CAUSE_NOT_PROVEN |
| R-FRACTAL-DIMENSION | IGNORED | measurement protocol missing | ROOT_CAUSE_NOT_PROVEN |
| R-EXTERNAL-VALIDATION | SUGGESTED | no independent run / third-party evidence | ROOT_CAUSE_NOT_PROVEN |

This table does not claim ten root causes. It identifies ten **historical first blockers** from the canonical ontology. Later evidence must be reconciled by scope before the row is treated as current.

## Scope reconciliation — V1.1

A second traceback found that several ontology gaps were later closed at a
narrow scope and then reused by a stricter successor contract. Reusing the same
broad record ID can make a scope expansion look like regression.

The stable identity is therefore:

```text
GapKey = (record_id, scope_id, contract_version, evidence_cutoff)
```

New invariants:

```text
GAP_ID_WITHOUT_SCOPE != STABLE_STATE_ID
PASS_SCOPE_A != PASS_SCOPE_B
CLOSED_SCOPE_A + EXPANDED_SCOPE_B -> NEW_SCOPED_GAP
LOCKED_WEIGHTS != CALIBRATED_WEIGHTS
FROZEN_FIXTURE != COMPLETE_CORPUS
DETERMINISTIC_BENCHMARK != MODEL_COMPETITION
INTERNAL_FEDERATION_PASS != INDEPENDENT_EXTERNAL_VALIDATION
```

The machine-readable lineage is
`data/contracts/gap-scope-lineage.v1.json`.

| Record | Earlier evidence | Current reconciliation |
|---|---|---|
| R-DAG-CAUSAL | DAG engine + 15 tests reported PASS | original TV-CODE gap resolved at engine/test scope; no domain causal claim promoted |
| R-BOOTSTRAP-UQ | fixed-seed Bootstrap engine + 17 tests reported PASS | engine scope preserved; replay-specific deterministic fixture remains open |
| R-ANTIDERIVATIVE-BOUNDARY | boundary schema/examples reported PASS | schema scope preserved; boundary-sensitive replay execution remains open |
| R-SOURCE-INDEPENDENCE | six-repo lineage/dedup validation reported PASS | six-repo scope preserved; replay widened lineage to all referenced sources |
| R-WEIGHTS-CALIBRATION | fixed 0.3/0.4/0.3 weights serialized, normalized and locked | artifact freeze is closed; blinded calibration remains open |
| R-LOGLOG-COMPETITION | seed-42 log-log determinism/shape/coverage reported PASS | determinism is closed; model-competition execution is not bound by that gate |
| R-FRACTAL-DIMENSION | null fixture frozen | estimator falsifier failed the declared tolerance; failure remains evidence |
| R-VECTOR-CORPUS | federation vector fixture frozen | complete authorized corpus remains access/privacy bounded |
| R-SEMANTIC-HUMAN-STUDY | historical abort preserved | ethics/privacy/consent remains the current prerequisite |
| R-EXTERNAL-VALIDATION | internal six-repo federation validation reported PASS | independent external reproduction remains open |

### Source-supported systemic pattern

The strongest current pattern is:

```text
STALE_ONTOLOGY_SNAPSHOT
+ UNSCOPED_GAP_IDENTIFIER_REUSE
+ CLOSURE_LABEL_SEMANTIC_OVERLOAD
-> APPARENT_REGRESSION
```

This is not yet promoted to a universal root cause. It is a source-supported
mechanism explaining multiple observed contradictions in the current records.

### Important examples

`TV-DATA-2 Calibration` validated deterministic serialization, a locked flag
and normalization of hard-coded weights. Its source explicitly says those
weights would normally come from a calibration run. Therefore the correct
relation is:

```text
WEIGHTS_LOCKED = true
CALIBRATION_EXECUTED = false
```

The log-log gate validates seed determinism, approximate shape and size
coverage. A frozen comparison fixture also exists, but the gate script does not
load that fixture. Therefore:

```text
LOGLOG_DETERMINISM_PASS != MODEL_COMPETITION_PASS
```

The August six-repository lineage authority can also remain valid while the
September replay contract asks for complete lineage across a larger source
population:

```text
SIX_REPO_LINEAGE_PASS != ALL_REFERENCED_SOURCES_LINEAGE_COMPLETE
```

## First higher-order diagnosis

The ten unresolved records collapse into fewer upstream families:

### A. Preparation/fixture deficit

- R-DAG-CAUSAL
- R-BOOTSTRAP-UQ
- R-LOGLOG-COMPETITION

The historical ontology recorded incomplete discrimination machinery. Scope reconciliation now shows that DAG and Bootstrap implementation gaps were later closed at their engine/test scopes, while successor replay/model-competition scopes remain separate.

### B. Calibration target deficit

- R-WEIGHTS-CALIBRATION

Weights cannot be judged before ground truth or blinded benchmark exists.

### C. Boundary/inverse-problem deficit

- R-ANTIDERIVATIVE-BOUNDARY

The boundary schema was later materialized; the remaining current gap is execution of a deterministic boundary-sensitive replay under the successor reconstruction contract.

### D. Lineage/independence deficit

- R-SOURCE-INDEPENDENCE
- R-EXTERNAL-VALIDATION

Six-repository lineage/dedup rules were later validated. The current replay gap is broader source coverage plus genuinely independent external reproduction, not absence of the six-repository schema.

### E. Access/governance prerequisite

- R-VECTOR-CORPUS
- R-SEMANTIC-HUMAN-STUDY

These are not evidence of censorship or scientific failure. One is access/privacy bounded; the other is correctly halted before an ethics-approved human protocol exists.

### F. Measurement-definition deficit

- R-FRACTAL-DIMENSION

A null-model fixture exists, but the estimator falsifier failed its declared tolerance. The current question is estimator accuracy/acceptance policy and replicated measurement, not absence of a null fixture.

## Why this is non-regressive

No historical status is deleted or rewritten. The forensic layer is an overlay.

```text
old state -> preserved
new origin trace -> appended
promotion -> blocked
```

The existing ontology engine remains authoritative for ontology validation. The new tool only reads it.

## "Florence" methodological note

This project uses a methodological analogy to the Enhanced Digital Investigation Process Model by Venansius Baryamureeba and Florence Tushabe (DFRWS USA 2004): separate scenes/context, trace backward, reconstruct and review before drawing conclusions.

No third-party code is copied. The forensic model is cited as methodological inspiration, not as proof for RAFAELIA or for any physical claim.

## Gate

A record may not be promoted from its historical editorial status merely because a first blocker has been identified.

Promotion requires:

```text
first blocker resolved
AND discriminating test executed
AND alternatives recorded
AND provenance complete
AND independent evidence where applicable
```

Until then:

```text
ROOT_CAUSE_NOT_PROVEN
claim_allowed=false
```

## R3

F_ok:

- all 10 unresolved ontology records receive a source-bound origin trace;
- editorial states remain preserved;
- no automatic POTENTIAL/SUGGESTED promotion;
- access is not relabeled censorship;
- first blocker is separated from proven root cause.

F_gap:

- historical gaps have different successor scopes and cannot be treated as one flat state;
- replay-wide lineage, blinded weight calibration, model-competition execution, privacy-safe corpus access, fractal estimator acceptance and external reproduction remain open;
- repository/provider governance gates remain fail-closed and must not be bypassed.

F_next:
run the scoped trace first; preserve closed engine/schema scopes; address only the active successor gaps. Highest-value current work is replay-wide lineage plus deterministic boundary/replay fixture, followed by blinded calibration and model-competition binding.
