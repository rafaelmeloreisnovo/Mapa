# ATLAS — La3Ni2O7 magnetism source route — 2026-10-04

**mode:** `POINTER_ONLY / APPEND_ONLY / SOURCE_FIRST / FAIL_CLOSED`  
**claim_allowed:** `false`  
**authority:** routing/provenance only; scientific synthesis remains in `papers`.

## Intent

Route the new La3Ni2O7 magnetic-order/spin-dynamics source into the RAFAELIA
research graph without copying the paper, promoting a pairing mechanism, or
creating a cross-domain physical claim.

## Producer authority

### Papers — academic synthesis and claim boundary

- repository: `rafaelmeloreisnovo/papers`
- draft PR: `#125`
- branch: `research/la3ni2o7-magnetism-bridge-20261004`
- observed head: `3d7074b3d2878a6d202667c6b65c62b0a0ef1592`
- human artifact:
  `research_notes/2026-10-04_LA3NI2O7_SINGLE_STRIPE_BILAYER_SPIN_DYNAMICS_V1.md`
- machine artifact:
  `data/registries/LA3NI2O7_MAGNETISM_SOURCE_GATE_V1.json`
- state: `DRAFT_SOURCE_ANCHORED / claim_allowed=false`

## External primary source

- DOI: `10.1038/s41563-026-02768-3`
- journal: `Nature Materials`
- version of record: `2026-10-02`
- primary observation family: elastic/inelastic neutron scattering
- publisher source data: Figs. 1-5 available

alphaXiv resolved the study preprint as:

- arXiv: `2605.03448v1`
- title: *Nature of magnetism in bilayer nickelate La3Ni2O7 single crystals*

A second recent alphaXiv record, arXiv `2610.01757v1`, is routed only as a
regime constraint for superconducting thin films. It is not the same
experimental system as the ambient-pressure bulk single-crystal neutron work.

## Typed relations

```text
SRC:DOI:10.1038/s41563-026-02768-3
  --EVIDENCES-->
OBS:LA3NI2O7_SINGLE_STRIPE_AND_BILAYER_SPIN_DYNAMICS

SRC:ARXIV:2605.03448V1
  --SAME_STUDY_MATCHED-->
SRC:DOI:10.1038/s41563-026-02768-3

ART:papers:2026-10-04_LA3NI2O7_SINGLE_STRIPE_BILAYER_SPIN_DYNAMICS_V1
  --SYNTHESIZES_WITH_BOUNDARY-->
SRC:DOI:10.1038/s41563-026-02768-3

ART:papers:LA3NI2O7_MAGNETISM_SOURCE_GATE_V1
  --GATES-->
CLAIM:UNIQUE_SUPERCONDUCTING_PAIRING_MECHANISM
```

`SAME_STUDY_MATCHED` means metadata/content correspondence observed in the
research pass. It is not a cryptographic identity relation.

## Evidence classes

```text
MEASURED:
  single-stripe magnetic order
  finite spin gap
  anisotropic in-plane excitations
  bilayer modulation

MODEL_CONSTRAINED:
  strong antiferromagnetic interlayer coupling
  competing in-plane couplings
  fitted bilayer Heisenberg-type parameters

INTERPRETIVE:
  relevance of intense mid-energy spin fluctuations to superconductivity

TOKEN_VAZIO_CAUSAL:
  unique microscopic pairing mechanism
```

## Anti-expansion boundary

The following edges are forbidden by this routing delta:

```text
La3Ni2O7 magnetism --PROVES--> RLL cosmology
spin fluctuations --EQUALS--> superconducting glue
bulk parent state --EQUALS--> superconducting thin-film state
bilayer Heisenberg fit --EQUALS--> unique microscopic Hamiltonian
```

No RLL source, equation, cosmological fit or claim is modified by this route.

## Gaps

- `GAP:NI-SOURCE-DATA-FREEZE` — publisher XLSX bytes not frozen locally.
- `GAP:NI-FIG3-REFIT` — spin-wave parameter fit not independently reproduced.
- `GAP:NI-FIG5-ABSOLUTE` — absolute susceptibility not independently reproduced.
- `GAP:NI-PAIRING-CAUSALITY` — unique pairing mechanism remains open.
- `GAP:NI-INDEPENDENT-REPRODUCTION` — no local/third-party reanalysis receipt.

## Highest-leverage next gate

```text
publisher Fig. 3 / Fig. 5 source data
  -> immutable byte capture
  -> SHA-256
  -> schema-preserving parse
  -> reproduce one quoted observable
  -> tolerance/residual receipt
  -> exact-source evidence gate
```

This gate has priority over creating a new RAFAELIA physical theory because it
converts a source pointer into locally reproducible evidence with less scope
and lower inference risk.

## Human / AI route

```text
ATLAS:LA3NI2O7-MAGNETISM-20261004
  -> this pointer
  -> papers PR #125
  -> papers research note
  -> papers machine source gate
  -> DOI version of record
  -> arXiv:2605.03448
  -> publisher source data
```

Expand to arXiv `2610.01757` only for film/bulk regime comparison.

## R3

`F_ok`: primary source, preprint, producer authority and claim boundary routed.  
`F_gap`: source-data freeze, refit, absolute-response reproduction and pairing causality remain open.  
`F_next`: exact-source reproduction before any additional physical bridge.
