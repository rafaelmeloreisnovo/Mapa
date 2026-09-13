# RAFAELIA — ΔG-MANIFOLD Bioiônico V1

**Date:** 2026-09-13  
**State:** `GOVERNED_DRAFT / EVIDENCE_FIRST / CLAIM_ALLOWED=false`

## Scope

Formalize a typed bridge between electrochemical gradients, pressure/osmosis, metabolism, excitable membranes, recurrent neural dynamics and sleep-state manifolds without asserting that distinct physical quantities are identical.

```text
gradient -> flux -> reaction -> potential -> oscillation -> recurrent network -> state
```

Canonical boundary:

```text
SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM
TOKEN_VAZIO != 0
P != V != Pi_as_identity
H_Shannon != S_thermo
physiological_mV != ionizing_radiation
```

Note: hydrostatic pressure `P` and osmotic pressure `Pi` share pressure dimensions and may appear in the same transport equation, but they are not the same state variable.

## Established external anchors

- Electrochemical potential: `mu_i_tilde = mu_i^0 + RT ln(a_i) + z_i F psi`.
- Membrane transport: channels permit selective ion flow; pumps maintain gradients by energy coupling.
- Water flux: `J_v = L_p (DeltaP - sigma DeltaPi)`.
- Neural membrane: `C_m dV_m/dt = -sum(I_i) + I_ext`.
- CO2/bicarbonate: `CO2 + H2O <-> H2CO3 <-> H+ + HCO3-`.
- Hemoglobin oxygenation is not identical to Fe2+ -> Fe3+ methemoglobin formation.
- Hypothermic organ preservation reduces metabolic demand while preservation solutions manage edema/osmotic and biochemical injury.
- Microneedle patches are a real transdermal vaccine/drug-delivery platform; this is a different spatial scale and mechanism from molecular ion-channel gating.
- Platelet transfusion is context/guideline driven; systematic liberal platelet loading is not a universal transplant rule.

## Author hypothesis

Let

```text
q(t) = [pO2, pCO2, pH, DeltaG_ATP, V_m, Pi, H_neural]
c_ion(t) = [Na+, K+, Ca2+, Cl-]
z(t) = (q, c_ion, x_neural, sleep_state)
```

and

```text
dz/dt = F(z, u; theta)
x_neural(t) in M_s
s in {wake, NREM, REM, dream}
```

Candidate sleep-state model:

```text
dx/dt = F_s(x,q) + beta_s B u_ext + g_s R(x) + eta
y_motor = gamma_s G(x)
```

with the falsifiable expectation that `gamma_REM << gamma_wake` for normal REM atonia and that sensory/recurrent gains may differ by state.

## Information/thermodynamic boundary

```text
H_Shannon = -sum p_j log p_j
```

is an information metric. Thermodynamic entropy is a physical state quantity. The program may test statistical coupling between metabolic/thermodynamic variables and neural information metrics, but it must never promote the two entropies as identical without a formally defined bridge and units.

## Corrections preserved

- `HFe2O2` / `HFeO2` are not formulas for blood.
- oxygenation != oxidation of heme iron to Fe3+.
- carbonic acid != carboxylic acid.
- lactase != lactate.
- physiological membrane gating != high-energy ionization.
- X-ray != safe generic neuromodulation.

## Privacy/provenance boundary

A user-provided family/identity relation associated with OneSkin is not promoted in this public artifact. Public company material documents Carolina Reis Oliveira, PhD, as a OneSkin cofounder with stem-cell/tissue-engineering and immunology background. Any binding of recalled vaccine-patch or ion-channel work to a specific person remains `TOKEN_VAZIO` until primary provenance is found.

## Gates

1. G0 definition and units.
2. G1 authoritative source.
3. G2 dimensional/model consistency.
4. G3 dataset or experiment.
5. G4 baseline and controls.
6. G5 preregistered analysis.
7. G6 internal reproduction.
8. G7 independent replication.

No integrated biological claim is promoted beyond external-literature support until the applicable gates pass.

## R3

**F_ok:** typed physical boundaries, literature anchors, claims ledger and falsifiers defined.  
**F_gap:** no new wet-lab/human dataset; manifold coupling remains hypothesis; person/work attribution unresolved.  
**F_next:** validate the claims ledger; run a synthetic typed-vs-collapsed model; only then bind a public sleep/respiration/EEG dataset.

