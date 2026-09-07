# ATLAS:X — Message Provenance Custody — 2026-09-07

**Route ID:** `ATLAS:X-MESSAGE-PROVENANCE-CUSTODY-20260907`  
**State:** `TERMUX_MERGED_LLAMA_SOURCE_READY_REMOTE_EXECUTION_GATED`  
**Mode:** `APPEND_ONLY / SOURCE_FIRST / FAIL_CLOSED`  
**claim_allowed:** `false`

## Decision

NOVOexport remains data/context, not mission authority. The semantic-custody defect was that retrieved messages retained an original CTI `role`, but the derived ConversationChunk was intentionally wrapped as `role=tool` without carrying that original role through the later context/governance chain. This could make a model-authored message indistinguishable from a user-role message at a later semantic pass.

The successor contract is `MESSAGE_ROLE_BOUND_V1`.

```text
user      -> USER_SOURCE
assistant -> MODEL_OUTPUT
system    -> SYSTEM_SOURCE
tool      -> TOOL_SOURCE
```

These labels are message-container provenance only. They do not prove lexical authorship of every token. A user message may quote external/model text; an assistant message may quote user text. Therefore:

```text
MESSAGE_ROLE_PROVENANCE != LEXICAL_AUTHORSHIP
USER_RETRANSMISSION     = TOKEN_VAZIO_CONTENT_CLASSIFICATION
THIRD_PARTY_CODE        = TOKEN_VAZIO_CONTENT_CLASSIFICATION
MODEL_LABEL             = TOKEN_VAZIO_CONTENT_CLASSIFICATION
```

## ATLAS route

```text
ATLAS:X
 -> NOVO:X       raw JSON/export first, read-only
 -> L:X          preserve predecessor/message lineage
 -> O:X          message role vs lexical authorship vs execution authority remain independent axes
 -> T:X          bind NOVO/CTI -> Chunk -> ContextBundle -> IntentIR -> Governance
 -> REL:X        exact role/provenance relations, no heuristic promotion
 -> SCALE:X      conversation -> message -> chunk -> evidence ref -> token/term when separately evidenced
 -> EVID:X       hashes, CI runs, merge state, provider observations
 -> GAP:X        remote/prestep and content-classification TOKEN_VAZIO
 -> LEARN:X      append-only correction/contradiction/next verifiable step
```

## EVID:X — Termux lane

PR `termux-app-rafacodephi#435` was merged as:

`82e71419d606428e75279d6e6b545f4497de3de7`

Source blobs at that merge:

| Object | git blob SHA-1 |
|---|---|
| `tools/atlas_novo_context_adapter.py` | `a6ad892b170d86d15c8dc426a4ed194b73ba7741` |
| `tools/atlas_llama_governance_bridge.py` | `e107e2c48e851b2c3ee736e5a2557ed31d269104` |
| `docs/contracts/conversation_chunk.schema.json` | `91715df6fddba1d702aeaa17c53278a786388850` |
| `docs/contracts/context_bundle.schema.json` | `b184d03cd01d0bddcf322c85b9be1b7d0662a08d` |
| `docs/contracts/intent_ir.schema.json` | `c4458596d3b1abe34807e8696c70b9a5d1d61483` |

Relevant PR-head workflows:

- Atlas NOVO Context Contract Gate `34109877217` — `SUCCESS`
- atlas-llama-governance-v1 `34109877108` — `SUCCESS`
- Rafaelia Native Safety `34109877177` — `SUCCESS`
- Safety Gates CI `34109877280` — `SUCCESS`
- RAFAELIA Pipeline ψχρΔΣΩ `34109877394` — `SUCCESS`

Provider Protection Gate `34109877071` remained `FAILURE`; it is preserved as an orthogonal external gate and was not bypassed.

## EVID:X / GAP:X — llamaRafaelia provider lane

PR `llamaRafaelia#125` head:

`9dbf2d55555ccae62aa5aa1a53ec4d18a0a95281`

The source implements matching `MESSAGE_ROLE_BOUND_V1` validation and IntentIR evidence propagation, with a mismatch falsifier. It is intentionally **not merged** here because remote execution evidence did not materialize.

Targeted `atlas-intent-provider-v1` run `34109852213`:

- initial `contract` job: `failure`, `steps=[]`;
- log retrieval: `BlobNotFound`;
- targeted job rerun was accepted;
- rerun successor `contract` job again: `failure`, `steps=[]`.

Orthogonal same-head correlation:

- Python Type-Check `34109852181`: `pyright type-check`, `steps=[]`;
- RMRCTI Safety and Determinism `34109852183`: five independent jobs, all `steps=[]`.

Classification:

```text
TV-LLAMA-ACTIONS-PRESTEP-REMOTE-EXECUTION
root_cause = TOKEN_VAZIO
source_regression_proven = false
remote_test_pass_proven  = false
```

Absence of executed steps is not converted into a code failure or a PASS.

## REL:X — structural binding

```text
NOVOexport message
  role=user|assistant|system|tool
       |
       v
RMRCTI hit.role
       |
       v
ConversationChunk
  runtime role=tool
  source_role=<original role>
  provenance_class=<deterministic class>
  tag=LEXICAL_ORIGIN_TOKEN_VAZIO
       |
       v
ContextBundle
  provenance_contract=MESSAGE_ROLE_BOUND_V1
  chunk_ref carries source_role + provenance_class
       |
       v
llama IntentIR evidence_ref
  must preserve exact provenance
       |
       v
Termux Governance
  rejects provenance downgrade/mismatch
```

## Mission boundary

```text
DATASET_INFORMS         != MISSION_AUTHORITY
RETRIEVAL_CONTEXT       != WEIGHT_UPDATE
LEARN_APPEND_ONLY       != ONLINE_SELF_TRAINING
MODEL_PROPOSAL          != EXECUTION_PERMISSION
CONTINUE_APPROVED_SCOPE != AUTONOMOUS_GOAL_CREATION
```

The dataset informs the model about the already-defined mission. It does not create, alter, or authorize the mission and does not update model weights.

## R3

- **F_ok:** Termux message-provenance chain is merged with targeted context/governance CI evidence and exact source blobs.
- **F_gap:** llamaRafaelia provider source is prepared but its remote Actions jobs did not execute steps; lexical/content-level origin classes remain TOKEN_VAZIO.
- **F_next:** obtain a real executed provider test for PR #125 or a separately authorized equivalent evidence path; then create an append-only successor rather than rewriting this record.
