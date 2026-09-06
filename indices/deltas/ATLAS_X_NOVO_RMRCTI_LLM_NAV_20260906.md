# ATLAS:X — NOVOexport × RMRCTI × LLM Navigation — 2026-09-06

**Route ID:** `ATLAS:X-NOVO-RMRCTI-LLM-NAV-20260906`  
**Object ID:** `ATLAS-NOVO-RMRCTI-LLM-NAV-20260906`  
**State:** `CONTRACT_MATERIALIZED / RUNTIME_BINDING_PENDING`  
**Mode:** `APPEND_ONLY / SOURCE_FIRST / claim_allowed=false`

## Route decision

The route selects **Termux as orchestration authority**, not Vectras, because `termux-app-rafacodephi` already owns the typed orchestrator surface (`ContextBundle -> IntentIR -> Governance Gate`) while `llamaRafaelia/rmrCti` already owns the local CTI memory/model integration and a Termux execution guide.

Vectras remains an optional execution/VM backend through the existing Termux provider contract.

## Canonical route

```text
ATLAS:X
  -> authority and route selection
NOVO:X
  -> NOVOexport/JSON source first
L:X
  -> predecessor/delta recovery
  -> adapter fanout
     {RMRCTI, Voynich_Private, RLL_Image, GAIA, optional Vectras}
  -> AtlasLLMContextEnvelope
  -> ContextBundle
  -> IntentIR
  -> Governance Gate
  -> local model interaction
LEARN:X
  -> append-only learning delta + receipt
```

## Authorities

| Domain | Authority |
|---|---|
| Atlas route/gates | `rafaelmeloreisnovo/Mapa` |
| Raw dataset | Google Drive `NOVOexport` |
| LLM + long-term CTI memory | `rafaelmeloreisnovo/llamaRafaelia/rmrCti` |
| Orchestrator | `rafaelmeloreisnovo/termux-app-rafacodephi` |
| Voynich protected implementation | `rafaelmeloreisnovo/Rafaelia_Private/native/voynich_impl` |
| GAIA candidate retrieval | `rafaelmeloreisnovo/GAIA_phi` |
| Image rigor/falsification | `instituto-Rafael/relativity-living-light` |
| Optional VM/runtime | `rafaelmeloreisnovo/Vectras-VM-Android` |

## Source observations supporting the route

### Termux

Existing vertical slice defines:

```text
ConversationChunk -> ContextBundle -> IntentIR -> Governance Gate
 -> ExecutionPlan -> ExecutionResult -> Audit Register
```

### llamaRafaelia / rmrCti

Source-observed canonical chain:

```text
raw / zip / conversations.json
 -> rafa_cti_scan.c
 -> bitstack/CSV
 -> triad_cti_couple.py
 -> coupled artifacts
 -> omega_* navigation/curation
 -> llama-server --cti-memory
```

`RAFAELIA_RUN_TERMUX.md` documents the local Termux route. `CTI_MEMORY_INTEGRATION.md` explicitly distinguishes long-term retrieval from KV-cache and from semantic-search claims.

### NOVOexport / Drive

Existing Drive bridge:

- `RAFAELIA — Assistant Bridge RMRCTI NOVOexport — Ledger V1 — 2026-08-10`
- Drive document ID `1F1jZ9r9vT_rC9Yuul49nv4ZYT2NVWKJX5Q5yAz8pgmQ`
- `06_GAIA_RMRCTI_MEMORY_BRIDGE` folder ID `1ytBGvDrFNh9dZT4XNc-41z5lD2QSJmK2`

This route reuses those authorities rather than creating a parallel corpus.

### RMRCTI ΔP

`ΔP ≈ 0.18` is routed only as a measured-association candidate with explicit falsifier/report provenance. Repetition is not promoted to causality, universality or attractor status.

### Voynich

Existing Mapa Three-Pillars route remains authoritative:

```text
P1 SOURCE_PROVENANCE
P2 EXECUTION_REPLAY
P3 INTERPRETATION_CLAIM_BOUNDARY
```

Protected body remains in `Rafaelia_Private`.

### RLL image method

The RLL side contributes image provenance, repeat/replay and falsification boundaries. Visual similarity/classification is not promoted directly to a physical/scientific claim.

### GAIA

`GAIA_phi/gaia_nanogpt.c` exposes the candidate retrieval chain:

```text
semantic_hash_djb2 -> hash_to_vector -> shift_attention -> resolve_memory_content
```

Its generator is source-observed as demo/simulation and is not promoted to trained model inference.

## Termux producer contract

Producer branch:

`rafaelmeloreisnovo/termux-app-rafacodephi@rafaelia/atlas-novo-llm-navigation-contract-v1`

Producer files:

- `docs/contracts/ATLAS_NOVO_LLM_NAVIGATION_CONTRACT_V1.md`
- `docs/contracts/ATLAS_NOVO_LLM_NAVIGATION_CONTRACT_V1.json`
- `docs/contracts/atlas_llm_context_envelope.schema.json`
- `tools/validate_atlas_llm_navigation_contract.py`
- `tests/fixtures/atlas_llm_context_envelope.min.v1.json`
- additive binding in `internal/orchestrator/vertical_slice.md`

Observed producer head after fixture materialization:

`d679f4d464cd835ff194942a760027565e55c068`

## Data/training boundary

```text
retrieval != training
indexing != training
context_injection != weight_update
```

V1 permits read-only retrieval and append-only derived indexes. Weight training/fine-tuning remains disabled until dataset manifest, privacy/license review, deterministic split, model identity, hyperparameters, device budget and reproducible training receipt are explicit.

## L:X lineage

Predecessors include:

- existing `llamaRafaelia/rmrCti` CTI-memory implementation;
- Drive Assistant Bridge RMRCTI↔NOVOexport;
- GAIA_RMRCTI_MEMORY_BRIDGE;
- Mapa Voynich V1.1 Three-Pillars route;
- Termux Vertical Slice v1.

Successor:

`TOKEN_VAZIO_UNTIL_LIVE_ATLAS_NOVO_LLM_BINDING_RECEIPT`

## LEARN:X delta

Material learning incorporated:

1. existing components form a federated route and should not be recopied into a new corpus;
2. Termux is the correct orchestration owner; Vectras is an optional runtime backend;
3. RMRCTI `ΔP≈0.18` must remain an evidence feature, not a relevance score or attractor claim;
4. Voynich and RLL image routes require explicit provenance/replay/claim boundaries;
5. GAIA can be adapted as read-only retrieval but its NanoGPT demo is not model-inference proof;
6. model output never becomes evidence merely by generation.

## Gates

- `G1_ROUTE_DETERMINISM` — OPEN
- `G2_SOURCE_CUSTODY` — OPEN
- `G3_CTI_CAUSAL_USE` — OPEN
- `G4_DELTA_P_BOUNDARY` — CONTRACTED
- `G5_VOYNICH_PRIVACY_AND_CLAIM` — CONTRACTED
- `G6_RLL_IMAGE_RECURRENCE` — OPEN
- `G7_LEARN_APPEND_ONLY` — OPEN

## TOKEN_VAZIO

- `TV-ATLAS-LLM-NOVO-LIVE-BINDING`
- `TV-NOVO-CURRENT-MANIFEST-EXACT-SCOPE`
- `TV-GAIA-RMRCTI-ADAPTER-RUNTIME`
- `TV-PRIVATE-BOUNDED-ADAPTER-RUNTIME`
- `TV-RLL-IMAGE-ADAPTER-REPLAY`
- `TV-VECTRAS-OPTIONAL-BACKEND-DEVICE-PROOF`
- `TV-EXTERNAL-GPT-PROVIDER-BINDING`
- `TV-TRAINING-DATASET-GOVERNANCE-AND-REPRODUCTION`

## F_ok / F_gap / F_next

`F_ok` = producer contract + machine JSON + schema + validator + fixture materialized in Termux; existing source routes located.

`F_gap` = live federated adapters, exact current NOVOexport manifest scope, CTI causal-use replay, RLL image replay and device/runtime receipts.

`F_next` = implement the read-only live adapter `ATLAS:X -> NOVO:X -> L:X -> RMRCTI -> ContextBundle`, run one rare-fact positive control + one no-hit negative control, then append `LEARN:X` receipt without changing model weights.

## Invariants

```text
ATLAS_ROUTE != SOURCE_BODY
NOVOEXPORT_SOURCE != DERIVED_CTI_INDEX
RETRIEVAL != TRAINING
MODEL_OUTPUT != EVIDENCE
REPETITION != CAUSALITY
MEASURED_DELTA_P != ATTRACTOR
PRIVATE_POINTER != PUBLIC_DISCLOSURE
SOURCE_PRESENT != BUILD_PROVEN != RUNTIME_PROVEN != DEVICE_PROVEN
TOKEN_VAZIO != 0
```
