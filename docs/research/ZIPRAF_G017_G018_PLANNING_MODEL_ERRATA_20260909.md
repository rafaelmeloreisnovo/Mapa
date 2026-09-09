# ZIPRAF G017/G018 — Planning Model Errata + Evidence Boundary

Date: `2026-09-09`  
Mode: `APPEND_ONLY / SOURCE_FIRST / FAIL_CLOSED`  
Claim gate: `claim_allowed=false`

## Source

Planning document observed in Google Drive:

- title: `_00_ZIPRAF_FULL_STACK_ENTERPRISE.md`
- Drive id: `193_bCxWnMqU6JVRMMMSlyR6nTbtMnsKLUIViLo2Fl28`

This document is a planning source, not an empirical receipt. Its statements are therefore reconstructed and checked as planning algebra only.

## 1. What the worked example actually computes

The planning text writes a simplified recurrence containing a residual term, but its numeric worked example omits that term and repeatedly applies only:

```text
sigma_n = sigma_0 * phi^n
```

with:

```text
sigma_0 = 2.4 = 12/5
phi     = 0.7 = 7/10
strict target: sigma < 0.5
```

Therefore the worked example is a deterministic geometric-decay illustration. It does **not** by itself establish a fitted ARIMA(1,0,1) model, an estimated AR coefficient, or residual dynamics.

## 2. Exact recomputation

Using exact rational arithmetic:

| cycle n | exact sigma_n | decimal | sigma < 0.5 |
|---:|---:|---:|---|
| 0 | 12/5 | 2.4 | no |
| 1 | 42/25 | 1.68 | no |
| 2 | 147/125 | 1.176 | no |
| 3 | 1029/1250 | 0.8232 | no |
| 4 | 7203/12500 | 0.57624 | **no** |
| 5 | 50421/125000 | 0.403368 | **yes** |

So the planning checkmark attached to cycle 4 under a strict `< 0.5` target is inconsistent with the formula. The first cycle satisfying the stated target is cycle 5.

This closes a planning arithmetic gap only. It does not establish that `phi=0.7` was measured.

## 3. The displayed `R²`

The document's displayed number is reproducible from its own algebra:

```text
1 - (sigma_4 / sigma_0)^2
= 1 - (0.7^4)^2
= 1 - 0.7^8
= 0.94235199
```

That arithmetic is internally reproducible. However the expression is not, merely by being bounded in `[0,1]`, ordinary regression `R²`, McFadden pseudo-R², Cox-Snell, Nagelkerke, or a confidence level.

For this planning model it is renamed here as:

```text
CUSTOM_SHRINK_SCORE = 1 - (sigma_n/sigma_0)^2
```

until a statistical estimator/model definition proves another interpretation.

## 4. Confidence boundary

`0.94235199` cannot be interpreted as `94.235199% confidence` from the planning algebra alone. A confidence statement requires an explicit uncertainty model, sampling/resampling procedure or likelihood/estimator construction, plus raw observations and a reproducible calculation.

Therefore:

```text
G017_PLANNING_SYMBOL_AND_ALGEBRA = CLOSED_FORMALIZED
G017_EMPIRICAL_PHI_0_7          = OPEN_TOKEN_VAZIO_EVIDENCE
G018_CUSTOM_SCORE_ARITHMETIC     = CLOSED_RECOMPUTED
G018_STATISTICAL_R2_CONFIDENCE   = OPEN_TOKEN_VAZIO_VALIDATION
```

## 5. Source search result

A source search found other occurrences of `0.7` in RAFAELIA repositories, including unrelated Mandelbrot/PSS3 constants. None of those occurrences is accepted as evidence for the ZIPRAF planning coefficient merely because the numeric token matches.

```text
same_number != same_variable
source_occurrence != empirical_measurement
planning_recompute != statistical_validation
```

## 6. Executable falsifier

Canonical validator:

```text
tools/validate_zipraf_g017_g018_planning_model.py
```

It uses Python `Fraction`, so all gate decisions above use exact rational arithmetic rather than float rounding.

Machine-readable receipt:

```text
data/evidence/zipraf-g017-g018-planning-recompute-20260909.v1.json
```

The validator must fail if cycle 4 is promoted to `<0.5`, if cycle 5 is not the first strict-target crossing, or if the custom shrink-score arithmetic changes without a versioned model change.

## 7. Remaining empirical closure

G017 closes only when a producer supplies a source-bound series/observations, definition of `phi`, estimator, sample/corpus identity/hash, residual treatment and reproducible estimated value/uncertainty.

G018 closes only when the metric family/formula is fixed and the claimed confidence has a valid reproducible uncertainty procedure. Until then both empirical/statistical claims remain typed `TOKEN_VAZIO`.

`SOURCE != PLANNING_MODEL != RECOMPUTATION != EVIDENCE != CLAIM`
