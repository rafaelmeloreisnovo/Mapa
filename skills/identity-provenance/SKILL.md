---
name: identity-provenance
description: Bind exact identity and provenance before semantic, execution, or governance decisions.
version: 1.0.0
status: DRAFT_FAIL_CLOSED
---

# D1 — Identity & Provenance

## Goal

Answer: `what exactly is this, and where did it come from?`

## Inputs

Prefer: `repo | ref | path | blob/hash | drive revision | provider | timestamp | source relation`.

## Procedure

1. Bind the strongest exact identity available.
2. Separate canonical source, verified replica, cache, derived artifact, and candidate alias.
3. Record staleness and lineage.
4. If identity is only inferred, label `CANDIDATE_IDENTITY`; never silently promote it.
5. A search miss is bounded negative evidence only: `search_miss != absence`.

## Gates

- hash mismatch → `QUARANTINE`;
- provider unknown → `TOKEN_VAZIO_PROVIDER`;
- derived ordinal used as raw identity → `FAIL_ANTI_SUBSTITUTION`;
- two authorities claim same identity without resolution → `HOLD_AUTHORITY_CONFLICT`.

## Output

`identity_state`, `source_class`, `exact_locator_or_opaque_commitment`, `digest_state`, `lineage`, `staleness`, `F_ok/F_gap/F_next`.
