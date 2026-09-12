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

## Current root-origin map

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

This table does not claim ten root causes. It identifies ten **first observed blockers** from the canonical ontology.

## First higher-order diagnosis

The ten unresolved records collapse into fewer upstream families:

### A. Preparation/fixture deficit

- R-DAG-CAUSAL
- R-BOOTSTRAP-UQ
- R-LOGLOG-COMPETITION

The current problem is not yet a failed scientific hypothesis. The executable discrimination machinery is incomplete.

### B. Calibration target deficit

- R-WEIGHTS-CALIBRATION

Weights cannot be judged before ground truth or blinded benchmark exists.

### C. Boundary/inverse-problem deficit

- R-ANTIDERIVATIVE-BOUNDARY

The inverse reconstruction is underdetermined until boundary/origin assumptions are explicit.

### D. Lineage/independence deficit

- R-SOURCE-INDEPENDENCE
- R-EXTERNAL-VALIDATION

Replication strength cannot be computed safely until shared ancestry and independent execution are separated.

### E. Access/governance prerequisite

- R-VECTOR-CORPUS
- R-SEMANTIC-HUMAN-STUDY

These are not evidence of censorship or scientific failure. One is access/privacy bounded; the other is correctly halted before an ethics-approved human protocol exists.

### F. Measurement-definition deficit

- R-FRACTAL-DIMENSION

The term cannot become empirical until estimator, null, scale interval and replicated measurement exist.

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

- no discriminating test has yet been executed for the ten blockers;
- causal ancestry across repositories remains incomplete;
- several gaps require new evidence, not more labeling.

F_next:
resolve the earliest dependency with the highest downstream fan-out: lineage authority and boundary/replay prerequisites, then rerun the forensic trace before calibrating weights or interpreting frontier-science patterns.
