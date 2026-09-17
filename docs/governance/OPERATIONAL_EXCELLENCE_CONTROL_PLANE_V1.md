# Operational Excellence Control Plane V1

> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧

## Status

`IMPLEMENTED_DRAFT` · `claim_allowed=false` · append-only governance overlay.

This document is a routing/control-plane artifact. It does not replace producer repositories, source evidence, execution receipts, privacy review, or legal authority.

## Mission boundary

The program optimizes continuous improvement under human-authorized objectives. It does **not** create autonomous goals and it does **not** treat a dataset, memory, index, model output, or symbolic expression as authority by itself.

Canonical invariant:

`SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM`

`TOKEN_VAZIO != 0`

## First-line gate

No operational mutation may be promoted unless all applicable dimensions below are explicitly evaluated:

1. `DIGNITY` — does the change preserve human dignity?
2. `CHILD_SAFETY` — if children can be affected, is the best-interest / fail-safe path selected?
3. `PRIVACY` — are data minimization, purpose limitation, retention and disclosure boundaries explicit?
4. `AUTHORITY` — are source, authorship/authority boundary and destination authority resolved?
5. `TRUTH_GAP` — are unknowns represented as typed gaps/TOKEN_VAZIO instead of inferred facts?

Any unresolved applicable dimension => `HOLD_FAIL_CLOSED`.

## Seven-guard clinical panel

Every material work unit SHOULD carry this exact panel. Missing applicable values are typed gaps, not defaults.

| Guard | Required question | Evidence class | Fail-closed state |
| --- | --- | --- | --- |
| Provenance | Where did this come from and what revision/hash identifies it? | source/ref/hash | `TOKEN_VAZIO_PROVENANCE` |
| Context | Why is this being acted on, for what objective, scope and environment? | intent/scope/authority | `TOKEN_VAZIO_CONTEXT` |
| Evidence | What observable supports the state? | test/log/artifact/readback | `TOKEN_VAZIO_EVIDENCE` |
| Contradiction | What conflicts with this state and was it preserved? | competing source/result | `TOKEN_VAZIO_CONTRADICTION_SCAN` |
| Uncertainty | What is not known, bounded, calibrated or provider-controlled? | typed uncertainty/gap | `TOKEN_VAZIO_UNCERTAINTY` |
| Reproduction | Can the result be reproduced from pinned inputs/operators? | fixture/version/hash/receipt | `TOKEN_VAZIO_REPRODUCTION` |
| Rollback | How is the change reversed/superseded without erasing history? | branch/revert/supersedes | `TOKEN_VAZIO_ROLLBACK` |

## DMAIC operating loop

### Define

Resolve objective, human authorization, source authority, destination authority, privacy boundary and CTQ. CTQ for this control plane: reconstructibility, provenance, fail-closed behavior, non-regression and bounded next action.

### Measure

Record baseline state, source revisions, current gaps, applicable gates and existing receipts. Do not convert absence of observation into absence of the object.

### Analyze

Classify risk by cause, not by narrative. Preserve contradictions. Separate provider/infrastructure gaps from content/scientific gaps. Nibiguiri is a recovery queue, not evidence that suppression, censorship, hidden weighting or causal intent occurred.

### Improve

Prefer the smallest reversible delta that closes a typed gap or reduces verified risk. One coherent mutation is better than broad unverified rewrites.

### Control

Require readback/test, receipt, source/hash, supersession/rollback route and index pointer. Promotion remains blocked until applicable gates close.

No statistical Six Sigma level is claimed unless defect/opportunity measurements support it.

## Nibiguiri recovery contract

Nibiguiri is restricted to evidence-preserving recovery states:

- `IGNORADO`: observed in source, not selected/promoted; cause may remain unknown.
- `ESQUECIDO_OU_DESINDEXADO`: prior existence is traceable but active pointer/index no longer reaches it.
- `ABORTADO`: processing started and ended before its closing gate with a receipt/state.
- `CENSURA_EVIDENCIADA`: only when an observable policy/action/block binds suppression.
- `FILTRO_PESO_EVIDENCIADO`: only when a visible score/threshold mechanism or receipt supports it.
- `OBVIO_NAO_INDEXADO`: independently demonstrable relation missing from the index.
- `CAUSA_DESCONHECIDA`: recovery candidate with no demonstrated cause.

Rule: `RECOVERY_CANDIDATE != TRUTH != AUTHORSHIP != CLAIM`.

## Tokenization authority boundary

A semantic pipeline must keep these identities separate:

`TOKEN_ID != OCCURRENCE_ID != SENSE_VERSION != CLAIM`

Additionally:

`SOURCE_ACTOR != AUTHORSHIP_AUTHORITY != SENSE_AUTHORITY != CLAIM_AUTHORITY`

- `SOURCE_ACTOR`: who/what produced the observed occurrence (`USER|ASSISTANT|TOOL|SYSTEM|UNKNOWN`).
- `AUTHORSHIP_AUTHORITY`: who has evidence-backed authority over original authorship/rights for that expression or artifact.
- `SENSE_AUTHORITY`: who/what source is authorized to bind the intended meaning in the current namespace.
- `CLAIM_AUTHORITY`: the evidence/gate system that can promote a claim; never inferred from identity alone.

No field may be backfilled from another field without an explicit rule and provenance.

## Promotion matrix

| State | Meaning | Promotion |
| --- | --- | --- |
| `OBSERVED` | source occurrence observed | no |
| `DECLARED_BY_AUTHOR` | authorial declaration observed | no |
| `PROVISIONAL` | candidate interpretation/model | no |
| `VERIFIED_LIMITED` | bounded gate closed | only within exact scope |
| `CONTRADICTED` | conflicting evidence preserved | no |
| `TOKEN_VAZIO` | required information unresolved | no |

## Minimal receipt

Each material delta SHOULD emit:

`receipt_id | timestamp | objective | source_refs | authority | baseline | change | seven_guards | gates | evidence | contradictions | uncertainty | reproduction | rollback | nibiguiri_delta | f_ok | f_gap | f_next | hash/ref`

Correction uses a new receipt with `parent/supersedes`; history is never silently rewritten.

## Exit condition

A work cycle stops when the authorized objective is satisfied or blocked by an explicit external/ethical/privacy/provider gap, and the system has a receipt, index pointer, rollback path and bounded next action.

Continuous improvement means repeated evidence-bound cycles, not endless mutation.

## R3

`F_ok`: first-line invariants, typed TOKEN_VAZIO, semantic event sourcing, provenance-first routing and append-only correction already exist in the project.

`F_gap`: first-line booleans are not sufficient evidence by themselves; semantic authority fields and deterministic replay remain incomplete; some provider governance and independent-approval gates remain external.

`F_next`: materialize a machine-readable gate contract + validator tests; extend semantic-event schema additively or by successor version; execute deterministic fixture; append receipt and update router only after observed results.
