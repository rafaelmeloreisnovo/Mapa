# RAFAELIA Hypothesis Index — Crocodylia delta — 2026-09-02

State: `INCREMENTAL / UNMERGED / claim_allowed=false`

## New provisional IDs

| ID | Domain | State |
|---|---|---|
| HYP-EMP-CROC-ORAL-MULTIPHYSICS-068 | oral/cranial thermal physiology | ACTIVE_UNTESTED |
| HYP-COMP-CROC-OPTICAL-CAVITY-069 | biological cavity optics | TOKEN_VAZIO_MODEL_AND_MEASUREMENT |
| HYP-EMP-CROC-CARDIAC-COUPLING-070 | cardiovascular thermoregulation | TOKEN_VAZIO_CAUSAL_BRIDGE |
| HYP-EMP-CROC-DENTAL-SYSTEMIC-071 | dental microbiome/systemic health | TOKEN_VAZIO_DENTAL_TO_SYSTEMIC_CHAIN |

## Authority edges

- Producer: `rafaelmeloreisnovo/papers@rafaelia/crocodylia-thermo-optic-vascular-20260902`.
- State/index: this Mapa branch.
- Longitudinal memory: Google Drive document created for the 2026-09-02 session.
- Evidence: external literature pointers only; no local execution or measurement receipt.

## Semantic edges

`PARABLE → FORMALIZATION → HYPOTHESIS → TEST → EVIDENCE`

- toucan thermal window — `FUNCTIONAL_COMPARATOR` → oral multiphysics;
- gape thermoregulation — `DOCUMENTED_EXTERNAL_SUPPORT` → oral multiphysics;
- thermal cardiac hysteresis — `DOCUMENTED_EXTERNAL_SUPPORT` → cardiac coupling;
- oral geometry — `PROPOSED_CAUSAL_EDGE` → optical cavity;
- optical/thermal field — `PROPOSED_CAUSAL_EDGE` → cardiac coupling;
- tooth renewal and oral microbiome — `BACKGROUND_SUPPORT` → dental/systemic;
- dental infection — `TOKEN_VAZIO_EDGE` → myocardial infection.

## Anti-promotion invariants

`parable != evidence`  
`external literature != local execution`  
`functional analogy != homology`  
`redistribution != energy amplification`  
`independent endpoints != demonstrated causal bridge`  
`TOKEN_VAZIO != PASS`

## Next gate

Verify producer PR commit hashes, complete bibliographic metadata, run global ID/dedup validation, then replace branch pointers with immutable merge SHAs. Until then all four IDs remain provisional and `claim_allowed=false`.
