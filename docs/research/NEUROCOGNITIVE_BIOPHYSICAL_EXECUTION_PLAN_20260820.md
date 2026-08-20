# Neurocognitive/Biophysical Federated Execution Plan — 2026-08-20

Status: DRAFT / claim_allowed=false

## Objective
Turn the seven mapped gaps into bounded, falsifiable, routed work without converting documentation into biological proof.

## Dependency order
1. typed claim grammar;
2. claim ledger;
3. deterministic contract validator;
4. control-plane gate routing;
5. longitudinal Drive matrix;
6. receipts from actual experiments/replications;
7. promotion only after gate-specific review.

## Anti-regression gates
- schema validation must precede evidence-state promotion;
- endpoint conflation is a hard FAIL;
- missing required fields become TOKEN_VAZIO, never inferred;
- external-lab-required gates cannot be closed by CI, documentation or simulation;
- independent replication is distinct from internal reproduction;
- negative evidence is preserved append-only.

## Promotion state machine
`TOKEN_VAZIO -> DRAFT -> EVIDENCE_FOUND_GATE_OPEN -> REPRODUCED_INTERNAL -> REPLICATED_INDEPENDENT -> PASS`

Any falsifier hit may route to `FAIL` or `BLOCKED`; there is no automatic monotonic promotion.

## R3
F_ok: operational dependency graph defined.
F_gap: cross-repository receipts and Drive IDs are not yet attached to this plan.
F_next: materialize producer/control-plane artifacts and append a federated receipt once their IDs exist.
