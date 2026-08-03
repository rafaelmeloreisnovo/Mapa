# DIRECTIVE_EVENT Index v1

Status: `METHOD_DEFINED / append-only / claim_allowed=false`

A directive is not a latent, a claim, evidence, a decision result or an authorization without scope. It is an explicit event that changes routing from its effective time forward.

## Minimum distinction

| Object | Function |
|---|---|
| `LAT-GOV` | governance content awaiting consolidation |
| `DIRECTIVE_EVENT` | explicit instruction with scope, effect and authorization |
| claim | assertion whose validity requires evidence and falsifier |
| decision | gate result after evaluating evidence |
| receipt | observed execution record |

## Invariants

- no retroactive rewrite;
- no destructive operation;
- no automatic merge;
- no claim promotion;
- conflict becomes `BLOCKED + CONTRADICTION`;
- source request is linked by SHA-256, not paraphrase alone;
- Google Drive appends editorial memory; GitHub versions schemas, validators and proofs.

## Current event

- `dir:explorar.entrelace.20260803T003524-0300`;
- source SHA-256: `506c65f9c79e64f101a06b29d40c5295001074faad0b677512c468c6f42a4244`;
- effects: `INTERPRET + ROUTE + WRITE`;
- targets: RafGitTools, Mapa and canonical Drive file;
- `retroactive=false`;
- `claim_allowed=false`.

Machine records:

- `schemas/directive-event.schema.json`;
- `data/directives/directive_events.20260803.jsonl`;
- `scripts/validate_directive_events.py`;
- `indices/CROSS_SOURCE_REGISTRY.jsonl`.
