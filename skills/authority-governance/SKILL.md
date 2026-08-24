---
name: authority-governance
description: Resolve who may read, write, mutate, promote, publish or delete, preserving producer authority and human authorization.
version: 1.0.0
status: DRAFT_FAIL_CLOSED
---

# D6 — Authority & Governance

## Principle

`capability != authority` and `knowledge != permission`.

## Procedure

1. Resolve owner/authority for the domain and exact operation.
2. Distinguish read, write, mutate, promote, publish and delete permissions.
3. Preserve producer authority: Mapa routes/reconciles; producer repos own implementation evidence in their domain.
4. Require explicit human authorization where repository policy or risk class demands it.
5. Unknown authority → `HOLD_FOR_AUTHORITY`.

## Write gate

Before material mutation require:

`destination + operation + authority_owner + branch/revision + privacy class + rollback decision + receipt destination`.

A technical PASS never overrides a governance DENY.

## Promotion gate

Promotion requires the specific evidence gate, allowed authority, non-blocking privacy/security state, and required independent review. Missing one remains `claim_allowed=false`.

## Output

`authority_owner`, `operation`, `write_authority`, `promotion_authority`, `human_review_required`, `blocking_reasons`, `F_ok/F_gap/F_next`.
