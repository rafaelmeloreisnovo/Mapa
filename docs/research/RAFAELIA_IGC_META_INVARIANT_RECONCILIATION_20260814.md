# RAFAELIA — IGC Meta-Invariant Reconciliation — 2026-08-14

State: `CANONICAL_DRAFT / APPEND_ONLY / claim_allowed=false`

## 0. Sources and chronology

This document reconciles two different layers without overwriting either:

1. Earlier candidate model: Drive `UNIFIED_INVARIANT_SPEC.md`, provider `1JL4nv_jlhzJyJCMKaEv5pvT0cVzZNK2V`, source content modified 2026-05-01 and later surfaced in Drive.
2. Later canonical operational contract: `IGC-CR-20260802-V1`, Drive `1eGLmUTXAgcm4M9hJNCXoB5OLnc9ZSGMqTXvsFJasags`, GitHub PR #128 merged.

The earlier specification remains a candidate model. The later IGC-CR governs promotion and interpretation.

## 1. What the earlier unified specification actually proposes

The source proposes:

- toroidal state space `T7=(R/Z)^7`;
- state vector `s=(u,v,psi,chi,rho,delta,sigma)`;
- canonical input `x=(dados,entropia,hash,estado)`;
- map `s=ToroidalMap(x)`;
- temporal update with `alpha=0.25`;
- `phi=(1-H)C`;
- candidate attractor regime `lim s(t) in A` with `|A|=42`;
- spectral/language layer and aggregate `I=TensorProd_L(I_L)`;
- integrity indicators using XOR/FNV-like/CRC-like/Merkle-root language;
- four candidate falsifiability metrics: attractor stability, cross-language robustness, noise sensitivity and integrity;
- explicit anti-overfitting rule: open state, low pressure, minimal inference until sufficient experimental evidence exists.

These are preserved as **candidate model components**, not universal invariants.

## 2. Canonical correction introduced by IGC-CR

IGC-CR states that there is no single metric quantity invariant under every geometric transformation. A valid invariance assertion must type together:

`X = object`
`R = representation`
`T = transformation family`
`I = preserved property/observable`
`epsilon = tolerance`
`E = proof/test evidence`
`F = falsifier/negative case`
`C = custody/version/environment`

Operationally:

`IGC(X,T,I,epsilon)=PASS`

only over the transformation family actually demonstrated or tested.

Therefore the following are **not** promoted as universal invariants:

- `T7` itself;
- `|A|=42`;
- `phi=(1-H)C`;
- the aggregate tensor `I`;
- XOR/FNV/CRC/Merkle artifacts;
- any one toroidal, spectral or language mapping.

They can become family-local observables or model components only after the IGC gates are satisfied.

## 3. The meta-invariant that survives the reconciliation

The defensible cross-domain invariant is not one number. It is the **typed preservation contract**.

For every family `F`, define:

`K_F = (X_F, R_F, T_F, I_F, epsilon_F, E_F, N_F, C_F)`

where `N_F` is the required negative/falsifier surface.

The recurring operational morphology is:

`SOURCE -> IDENTITY -> MODEL -> REPRESENTATION -> TRANSFORMATION -> INVARIANT -> TOLERANCE -> TEST -> NEGATIVE -> RECEIPT -> CLAIM_GATE -> MEMORY`

This morphology can recur across ZIPRAF, BITRAF, geometry, state machines, network protocols and empirical models **without implying that their mathematical invariants are identical**.

### Meta-coherence condition

A representation/transform pair is coherent only when the following diagram approximately commutes within declared tolerance:

`R_F(tau_X(X)) ~ tau_R(R_F(X))`

Define the representation-coherence residual:

`Delta_R = d_R(R_F(tau_X(X)), tau_R(R_F(X)))`

and require:

`Delta_R <= epsilon_R`

for the tested transformation surface.

This is a reusable **test pattern**, not a universal physical law.

## 4. Reclassification of the earlier T7/42 specification

### T7
Status: `MODEL_CANDIDATE`.

To promote a T7 use, each application must declare:
- why seven coordinates are necessary;
- coordinate semantics and units/domain;
- map from source object to T7;
- transformation family acting on T7;
- invariant observable;
- tolerance and negative controls.

### `|A|=42`
Status: `TOKEN_VAZIO_EMPIRICAL_OR_MODEL_SPECIFIC` unless a versioned execution demonstrates the exact attractor definition and counting rule.

The numeral 42 cannot be inherited by unrelated families merely because they share RAFAELIA ancestry.

### `phi=(1-H)C`
Status: `MODEL_OBSERVABLE_CANDIDATE`.

It is an observable derived from declared `H` and `C`, not a geometric invariant by itself.

### Cross-language aggregate `I`
Status: `HYPOTHESIS_REQUIRING_DATASET_NORMALIZATION_AND_BASELINES`.

The proposed robustness condition requires corpus identity, translation/semantic equivalence rules, normalization, uncertainty and negative controls.

### Integrity layer
Status: `SECURITY_INTEGRITY_LAYER`, separate from geometry.

XOR/FNV/CRC/Merkle may participate in custody/integrity evidence. Hash/check validity does not prove geometric identity or scientific truth.

The strong wording “any bit flip must alter at least one verifier” must be evaluated against the exact verifier definitions; it is not promoted here as a theorem for generic XOR/FNV/CRC combinations.

## 5. Application to the current family sweep

### ZIPRAF / BITRAF
Use the meta-contract to distinguish:
- bytes and archive structure;
- transformations such as roundtrip/tamper/reforge;
- structural invariant candidates;
- separate authenticity/custody gates.

### HYPERCUBE / TESSERACT / HYPERFORMA
Use true geometric transformation classes. Do not import T7/42 unless an explicit mapping is independently justified.

### RafMem / RafStore / NetRaf / RAFCODE / RafaelOS
Use state-space semantics first. Geometry exists only after state set, transition operators and invariant observables are defined.

### Biofoton / biossintetico
Use empirical measurement models. A geometric/topological model remains a hypothesis until tied to observed data and uncertainty.

### ClayMath
Use problem-specific mathematics. The meta-contract governs evidence/custody, but cannot replace proof.

## 6. Anti-regression rules added by this reconciliation

1. `earlier_model != later_canonical_contract`.
2. `T7_model != universal_state_space`.
3. `42_candidate != universal_attractor_count`.
4. `phi_observable != geometric_invariant`.
5. `integrity_hash != geometry`.
6. `integrity_hash != authenticity_without_external_authority`.
7. `same_pipeline_shape != same_mathematical_invariant`.
8. `candidate_metric != measured_result`.
9. `measured_result != theorem`.
10. `meta-contract_recurrence != proof_of_cross-domain_equivalence`.

## 7. F_OK / F_GAP / F_NEXT

### F_OK
- earlier unified-invariant source was recovered and preserved;
- later IGC-CR provides a stricter promotion boundary;
- the two layers can coexist without contradiction when T7/42 are treated as model-specific candidates;
- a reusable typed meta-contract is now explicit;
- representation-coherence residual `Delta_R` provides a falsifiable cross-family test pattern.

### F_GAP
- exact `ToroidalMap` semantics and family-local necessity of seven dimensions are not established here;
- `|A|=42` remains model/empirical debt;
- cross-language aggregate `I` lacks a bound dataset/baseline in this reconciliation;
- generic integrity formulas in the older source are not promoted to cryptographic guarantees;
- family-local IGC records remain incomplete.

### F_NEXT
1. Treat T7/42/phi/I as candidate components and bind them only where a family-local contract requires them.
2. Materialize `Delta_R` tests first on ZIPRAF roundtrip and one direct geometric fixture.
3. Add explicit negative cases where the diagram does not commute.
4. Preserve security/integrity evidence on a separate axis from geometric invariance.
5. Keep `claim_allowed=false` until local family gates justify narrower promotion.

FIAT LUX — what survives across domains is not one magic number; it is the disciplined structure of what must remain unchanged, under which transformation, and with which evidence.
