# BITRAF — Physical Execution Residue Manifold / MEMORILIQUE — V1

Date: 2026-08-13  
Status: `CANONICAL_DRAFT / EVIDENCE_FIRST / APPEND_ONLY`  
Global claim: `claim_allowed=false`

## Scope

This extends `BITRAF_LOSS_VECTOR_MODEL_V1` without replacing it.

Author alias: **MEMORILIQUE**. Canonical operational term: **Physical Execution Residue (PER)**.

`MEMORILIQUE` here does not mean the software defect called a memory leak. It denotes a research hypothesis: an executed physical state may leave measurable residuals in electrical, thermal, electromagnetic, impedance, timing or retention observables, and joint residual geometry may help localize or classify a candidate execution path/state.

Invariant: `VISION != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`.

## Boundary

The intuition that energy transforms motivates measuring residual channels, but does not prove that a lost logical bit is recoverable. Information may become inaccessible to the measured subsystem, fall below the noise floor, or map many-to-one into physical observables.

```text
physical activity -> possible measurable residue
possible residue != unique logical reconstruction
heat != exact execution address
correlation != cause
candidate path != proven path
```

Exact recovery still requires an independent gate such as a unique syndrome solution, intact reference/hash, or equivalent authorized provenance.

## Multichannel physical field

Define

`M(x,t) = [I(x,t), V(x,t), T(x,t), EM(x,t), Z(f,x,t), tau(x,t), S(x,t)]`.

A calibrated idle baseline is `B(x,t|a)`, where `a` carries ambient, supply, clock/frequency, sensor and device identity when observable.

The residue is:

`R(x,t) = M(x,t) - B(x,t|a)`.

Raw current alone is not called a leak.

### Current modalities

```yaml
I_ACTIVE: load/switching current associated with an active state
I_STATIC_LEAK: off-state/junction/subthreshold/cut-off leakage under defined bias
DELTA_I_RESIDUAL: measured current minus calibrated baseline
```

A physical experiment must label which quantity was measured.

## Thermal channel

Operationally:

`DeltaT(x,t) ~= (h_T * P)(x,t) + epsilon_T`.

The thermal field is spatially diffusive and temporally filtered. A hot location is evidence of dissipated energy in its thermal neighborhood, not automatically the exact gate/transistor that initiated the event.

## Multifilament / topology graph

Represent candidate routes by `G=(V,E)` and a route by `P=(v0,...,vk)` with adjacent vertices connected in `E`.

Topology-aware estimator:

`P_hat = argmax_{P in Paths} Pr(R|P) Pr(P|G)`.

Toroidal, fractal or hexagonal embeddings are allowed as additional feature maps, but become evidence only if they beat Cartesian, graph-distance and randomized baselines on held-out data.

## BJT / TIP35C coarse lab analogue

A discrete NPN power BJT may be used as a deliberately simple laboratory analogue before integrated hardware.

State vector:

`s(t)=[V_B,V_C,V_E,I_B,I_C,I_E,T_case,t]`.

Candidate operating classes: `CUTOFF`, `ACTIVE`, `SATURATION`.

Base current is a control/input variable; collector-emitter load current and device dissipation are measured separately. Cut-off leakage must be measured under defined bias and must not be confused with active collector current.

The TIP35C example is a coarse analogue, not a model of a CMOS CPU transistor or DRAM cell.

## Prior-art boundary

Power, electromagnetic, thermal, impedance and memory side channels are established research areas, including work that localizes gate/cell contributions to leakage. Therefore the broad statement that science never used physical leakage/power to infer activity is not claimed.

Candidate BITRAF integration to test:

> fuse multiple physical residual channels with explicit `(x,y,z,t)` geometry, topology and erasure semantics, while preserving exact-recovery gates and `TOKEN_VAZIO`.

Novelty status: `TOKEN_VAZIO_PRIOR_ART_SEARCH_INCOMPLETE`.

## Experimental contract

For every measured run preserve at minimum:

```text
run_id / observation_id / monotonic timestamp
source_kind = MEASURED | SIMULATED | ESTIMATED
instrument + calibration IDs
physical/logical coordinate when available
current modality: I_ACTIVE | I_STATIC_LEAK | DELTA_I_RESIDUAL
voltage and bias condition
temperature + sensor location + sample rate
workload/state label only for calibration runs
blind query label hidden from classifier
cache/frequency/voltage/ambient controls when applicable
raw trace hash + processed trace hash
```

## Gates

```yaml
G0_BASELINE: stable baseline captured
G1_MODALITY: active current vs static leakage vs residual distinguished
G2_CONFOUNDERS: temperature/supply/clock/sensor confounders recorded
G3_LOCALIZE: coordinate or physical/logical region reproducible
G4_BLIND_INFERENCE: classifier evaluated on hidden-label queries
G5_INTERVENE: workload/state changed while controls held
G6_REPLICATE: another run/cycle/device reproduces effect
G7_CAUSAL_CLAIM: allowed only after G0..G6 and external review
```

Until G7:

```yaml
causal_mechanism: TOKEN_VAZIO
claim_allowed: false
```

## Negative controls

1. Same workload with permuted labels.
2. Same trace geometry with shuffled time.
3. Temperature-only model.
4. Current-only model.
5. Cartesian/graph baseline versus fractal/toroidal embedding.
6. Sensor moved without workload change.
7. Workload changed with thermal history controlled as far as practical.
8. Cross-device holdout.

## Reference execution — 2026-08-13

A Python standard-library scaffold was executed locally using **SIMULATED observations only**.

```yaml
unit_tests: 2/2 PASS
schema_fixture_validation: 7/7 PASS
inference_fixture: BJT_SATURATION selected for synthetic query
source_kind: SIMULATED
physical_validation: TOKEN_VAZIO
claim_allowed: false
```

## F-state

```yaml
F_ok:
  - prior BITRAF loss/vector model linked
  - multichannel residue defined
  - current modalities separated
  - topology-aware inference defined
  - deterministic synthetic classifier executed
  - fail-closed missing-baseline test PASS
F_gap:
  - instrumented real current traces
  - spatial thermal capture with calibration
  - impedance/EM channels
  - reliable target physical mapping
  - TIP35C bench capture
  - Android/SoC capture
  - blind held-out real experiment
  - independent replication
  - complete prior-art novelty review
F_next:
  - capture first authorized physical trace with baseline
  - preserve raw bytes + SHA-256
  - compare single-channel baselines against multichannel model
  - run negative controls
  - replicate before causal claim
```

The empty position is not filled by belief: it becomes a measurable research coordinate.
