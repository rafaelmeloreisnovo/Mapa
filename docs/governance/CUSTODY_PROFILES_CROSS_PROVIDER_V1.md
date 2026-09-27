# RAFAELIA — Custody Profiles Cross-Provider V1

Status: IMPLEMENTED_UNTESTED until CI exact-head proves the gate.
Scope: Google Drive ↔ GitHub ↔ ChatGPT session/service boundaries.
Base preserved: `schemas/cadeia_custodia_evento.schema.json` remains unchanged.

## Why this refactor exists

"Cadeia de custódia" was being used for several different obligations. This profile layer separates them without rewriting historical events.

The governing invariant remains:

SOURCE ≠ ARTIFACT ≠ EXECUTION ≠ EVIDENCE ≠ CLAIM

A provider storing an object does not automatically become authority for every property of that object, and a service performing an operation does not inherit human authorization.

## Custody types

| ID | What is under custody | Typical authority | Minimum proof | Claim effect |
|---|---|---|---|---|
| C0_SOURCE_ORIGIN | original source identity and acquisition context | source provider / verified locator | provider ID, observed time, source ref or TOKEN_VAZIO | no promotion |
| C1_IDENTITY_AUTHORITY | actor, identity, permission and delegated scope | provider metadata + explicit human authorization | actor, authority scope, observed permission/request | no promotion |
| C2_ARTIFACT_INTEGRITY | file/content/version identity | producer/provider of record | artifact ID, provider ref, hash/version | no promotion |
| C3_TRANSFORMATION_DERIVATION | parent→child transformation | derivation record | parent, operation/tool, child, time | no promotion |
| C4_EXECUTION_RUNTIME | what actually executed | runtime / CI provider | exact ref, environment, entrypoint, exit, logs | may feed gate |
| C5_EVIDENCE_MEASUREMENT | test/measurement/validation observation | evidence-producing surface | evidence kind, scope binding, state, ref | may feed gate |
| C6_TRANSFER_CROSS_PROVIDER | handoff between providers | both endpoints + typed bridge | artifact ID, refs, relation, identity rule, time | no promotion |
| C7_DECISION_CLAIM_GATE | approval/promotion/claim decision | human-authorized gate + sufficient evidence | actor, gate rule, evidence refs, decision | gate only |
| C8_RECEIPT_AUDIT | append-only record of what changed | durable receipt store | receipt ID, sources, state, gap, next | no promotion |

## Provider authority

**Google Drive** is primary for documentary memory, corpus, indices, CURRENT_STATE, receipts, documentary evidence and custody records. It is not the authority for code execution merely because a copy or note is stored there.

**GitHub** is primary for code, schemas, specifications, tests, CI, commits and implementation history. It is not the authority for human intent or private memory merely because a commit mentions them.

**ChatGPT session/service** is a delegated operational context, not a durable provider of record. It may read/write through authorized connectors and its actions must be bound to tool receipts. A session cannot promote a claim, redefine the human objective, authorize merge, or create durable custody by narrative alone.

## Actor boundary

- HUMAN_OWNER: may define objective and authorize promotion/merge/destructive changes.
- ASSISTANT_SERVICE: may execute within delegated scope; cannot authorize claim promotion or change the human objective.
- PROVIDER_AUTOMATION: may execute provider-defined jobs and emit logs/IDs; it does not own semantic approval.
- DEVICE_RUNTIME: proves the observed runtime event when environment, command/entrypoint, exit and output are bound.

## Cross-provider bridge

Every Google Drive ↔ GitHub bridge must carry:

`artifact_id | from_provider | to_provider | source_ref | destination_ref | relation | observed_at | identity_rule`

Do not assert byte identity unless the same immutable bytes are actually hashed at both ends.

For native Google Workspace documents, title/content similarity is not byte identity. Use provider revision plus an explicitly defined semantic/export hash rule and record the transformation.

For ChatGPT-mediated transfers, the durable chain starts only when the target durable provider returns an observed mutation receipt.

## Transition gate

C0 → C2 requires source and artifact identity.
C2 → C3 requires parent/tool/child binding.
C3 → C4 requires exact artifact/commit plus runtime identity.
C4 → C5 requires execution state, output/log and scope binding.
C5 → C7 is never automatic; gate rule, evidence refs and decision actor are required.
Any material delta → C8 append-only receipt with gap and next.

## Operational consequence

A single object can legitimately have multiple custody profiles at the same time. For example, a GitHub commit can be C2, its CI run C4, test output C5, a Drive receipt C8, and the Drive↔GitHub link C6. These are related but not interchangeable.

Historical `custody-event.v1` records remain valid. New work should classify each event through the profile registry rather than overloading one generic custody label.
