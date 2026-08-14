# RAFAELIA — Hypothesis Index V2

Date: 2026-08-14  
Mode: `APPEND_ONLY_BY_REFERENCE`  
State: `GOVERNED_PARTIAL / NONTERMINAL / claim_allowed=false`

Extends: `indices/RAFAELIA_HYPOTHESIS_INDEX_V1.md`

## Current ledger frontier

- 13 mathematical families were audited in the session-local mathematical audit.
- 3 mathematical survivors remain M2 candidates.
- Delta 0001 added 6 normalized cross-domain hypothesis-like records.
- Delta 0002 added 10 normalized records.
- **19 stable/provisional hypothesis IDs are now represented in the cross-domain ledger.**
- **19 is not the certified global number of hypotheses.** Global uniqueness/terminality remains `TOKEN_VAZIO`.

## Type system

`data/hypotheses/RAFAELIA_HYPOTHESIS_TYPE_SYSTEM.v1.json`

Types currently used:

- `MATH_NOVELTY_CANDIDATE`
- `MATH_OPEN_PROPOSITION`
- `EMPIRICAL_HYPOTHESIS`
- `COMPUTATIONAL_HYPOTHESIS`
- `STATISTICAL_MODEL_HYPOTHESIS`
- `METHODOLOGICAL_HYPOTHESIS`
- `INTERPRETIVE_SYMBOLIC` (excluded from scientific count by default)

## Delta 0002 — new IDs

| ID | Domain | State |
|---|---|---|
| HYP-SCI-FEAC-BITVIS-010 | one-bit visual coherence | REFUTED_IN_DECLARED_SCOPE |
| HYP-METH-FEAC-SEARCHRECALL-011 | error-attention search/recall | TOKEN_VAZIO |
| HYP-SCI-SQRT3-UNIVERSAL-012 | cross-domain sqrt(3)/2 invariant | BLOCKED_BY_DEPENDENCIES |
| HYP-COMP-OMEGA42-DYNATTR-013 | exactly 42 dynamic attractors | TOKEN_VAZIO |
| HYP-MATH-ERASURE-MINDEG3-014 | erasure reconstruction / min degree 3 | PROOF_OBLIGATION |
| HYP-COMP-VOID-FSM-015 | void-to-discrete finite-state model | ACTIVE_UNTESTED |
| HYP-METH-SEVEN-DIR-TAXONOMY-016 | seven-direction routing taxonomy | ACTIVE_UNTESTED |
| HYP-EMP-SPECTRAL-HISTORY-017 | light-history → illuminant priors | ACTIVE_UNTESTED |
| HYP-METH-PARABLE-CODEC-018 | shared codebook/context reduces semantic loss | ACTIVE_UNTESTED |
| HYP-EMP-HETE018-019 | stationary/recovering DeltaP near 0.18 | ACTIVE_PARTIAL_EVIDENCE |

## RLL update

Drive full-document read completed for `RAFAELIA — Papers × ChipQuantum × RLL — Auditoria de Fórmulas — 2026-08-04`.

Observed document-level facts:

- nested null limit: `Omega_s0=Omega_B0=Omega_P0=0` recovers exactly LambdaCDM;
- FASE20: `Omega_s0 95% UL = 0.0017772301590821408`;
- FASE20: `ln(B10) = -6.190210762419383 ± 0.6906527421175422`;
- the referenced result favors LambdaCDM;
- covariance unification, prior sensitivity, chain length and independent reproduction remain open.

Therefore `HYP-STAT-RLL-EXTENSION-009` remains in the ledger but is `DISFAVORED_BY_CURRENT_EVIDENCE` in that declared analysis rather than deleted.

## Dedup topology

### DEDUP-OMEGA42-DYNAMIC-ATTRACTORS

- `HYP-MATH-ATTR42-FIB-005`
- `HYP-COMP-OMEGA42-DYNATTR-013`

State: `NOT_MERGED_YET`.

Reason: the first is tied to a Fibonacci torus-map statement; the second to the broader Ω-CUBE-42/visual-runtime architecture. Equal use of “42 attractors” is not enough to establish semantic identity.

### DEDUP-BITRAF-FORMAL-VS-PHYSICAL

- `HYP-M2-BITRAF64-F2-001`
- `HYP-EMP-BITRAF-PHYSRES-008`

State: `DISTINCT`.

Reason: finite algebraic transformation versus empirical side-channel/physical-residue model.

## Source coverage checkpoints

- `HYP_CKPT_0001`: 8 source anchors registered; initial 6-record delta.
- `HYP_CKPT_0002`: RLL upgraded to full document read plus seven additional GitHub source reads; 10-record delta; dedup clusters started.

Files:

- `data/hypotheses/checkpoints/RAFAELIA_HYPOTHESIS_COVERAGE_CKPT_0001_20260814.json`
- `data/hypotheses/checkpoints/RAFAELIA_HYPOTHESIS_COVERAGE_CKPT_0002_20260814.json`
- `data/hypotheses/deltas/RAFAELIA_HYPOTHESIS_DELTA_0001.jsonl`
- `data/hypotheses/deltas/RAFAELIA_HYPOTHESIS_DELTA_0002.jsonl`

## Next cursor

`HYP_CKPT_0003_PAPERS_HYPOTHESIS_SEARCH_HITS_PLUS_ZIPRAF_RMRCTI_CLAIM_LEDGERS`

The next count must remain a **ledger frontier**, never a declared global total, until `FG-HYP-007` terminality is physically evidenced.
