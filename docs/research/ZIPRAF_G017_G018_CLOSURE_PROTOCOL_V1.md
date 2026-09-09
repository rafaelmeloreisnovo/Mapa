# ZIPRAF G017/G018 — falsifiable closure protocol V1

State: `PROTOCOL_MATERIALIZED / EVIDENCE_NOT_YET_ACQUIRED`  
Cycle: `OMEGA-FED-20260909-GEOFS-001`  
Claim gate: `claim_allowed=false`

## Why this exists

`G017` and `G018` are not source-code gaps. They are measurement/validation gaps. This protocol converts them from prose into finite evidence obligations without pretending that a protocol is evidence.

## G017 — ZIPRAF_PLANNING_PHI_0_7_EVIDENCE

Current state: `OPEN_TOKEN_VAZIO`.

Before any run, freeze a manifest with:

- `phi_symbol_definition`: exact operational meaning of the planning φ value;
- `target_value`: `0.7` only if the producer explicitly confirms that this is the target under test;
- `unit_or_dimensionless`: explicit;
- `producer_formula_or_algorithm_sha256`;
- `input_corpus_id + input_corpus_sha256`;
- `baseline_definition`;
- `sample_size`;
- `measurement_function`;
- `acceptance_interval` fixed before observing results;
- environment/toolchain/architecture identifiers.

Fail closed when `phi_symbol_definition` is missing. Presence of `φ=0.7` in planning text is not empirical evidence.

### Required output

Machine-readable rows:

`sample_id, input_hash, observed_phi, target_phi, residual, environment_id, run_id`

plus immutable aggregate receipt containing count, mean/median as applicable, dispersion, outliers policy, exact algorithm version and all hashes.

### Falsifier

G017 must remain open if changing the corpus, algorithm or acceptance interval after observing results is required to obtain agreement.

## G018 — ZIPRAF_R2_CONFIDENCE_VALIDATION

Current state: `OPEN_TOKEN_VAZIO`.

The label `pseudo-R²` is under-specified until its family/formula is named. `McFadden`, `Cox-Snell`, `Nagelkerke`, ordinary `R²`, custom fit score and a correlation coefficient are not interchangeable.

Freeze before execution:

- `metric_name` and exact formula;
- dependent/independent variables;
- model family and fitted parameters;
- training/evaluation split or resampling plan;
- null/baseline model;
- confidence method (`bootstrap`, analytical interval, permutation or other named method);
- confidence level;
- random seed policy;
- corpus/input hashes;
- residual/error definition;
- negative controls and failure thresholds.

If `metric_name/formula` is absent: `TOKEN_VAZIO_METRIC_DEFINITION`.

### Required output

At minimum:

`metric_value, confidence_lower, confidence_upper, n, baseline_metric, residual_summary, corpus_sha256, model_sha256, code_sha256, seed_manifest_sha256`.

### Falsifiers

- confidence interval cannot be reproduced from frozen inputs;
- result disappears under the predeclared negative control;
- data leakage between fit/evaluation is detected;
- metric is renamed/redefined after results;
- pseudo-R² is interpreted as percentage of physical compression/capacity without an explicit model proving that relation.

## Relationship between G017 and G018

They remain independent:

`G017 target agreement != G018 statistical validation`.

A point estimate near 0.7 does not prove model confidence. A statistically stable fit does not prove that φ should equal 0.7.

## Execution route

`definition freeze -> corpus custody -> algorithm hash -> bounded run -> raw rows -> validation -> receipt -> independent reproduction -> Atlas successor`.

The protocol itself closes only the procedural ambiguity: `WHAT_TO_MEASURE` and `HOW_TO_VALIDATE` are now explicit. It does **not** close G017/G018 evidence states.
