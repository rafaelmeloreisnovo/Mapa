# Observer ↔ Observed Ω — Typed Network Intake V1

State: \`CANDIDATE / FAIL_CLOSED / NO_MERGE / claim_allowed=false\`. Authority: **Mapa** for observation intake and graph routing; **RafGitTools** for federation governance; each producer repo for implementation; provider owners for server-side enforcement.

## Entry routes

- Human/AI: START HERE V2.2 → HOTSTATE V4.5 → this intake → exact source → falsifier → canonical approval → μWRITE → R3.
- Existing authorities: [Risk Observation Ledger](../../indices/RAFAELIA_RISK_OBSERVATION_LEDGER_V1.md), [GAP OF GAPS](GAP_OF_GAPS_CURRENT_V1.md), [TOKEN_VAZIO approval](TOKEN_VAZIO_APPROVAL_WORKFLOWS_V1.md).
- Machine-readable projection: \`data/governance/observer_observed_network_v1.json\`, fail-closed validator: \`tools/validate_observer_observed_network_v1.py\`, negative tests: \`tests/test_observer_observed_network_v1.py\`.
- Relational governance predecessor: RafGitTools \`docs/UNCERTAINTY_URGENCY_FRICTION_ETHICS_LICENSE_BY_DESIGN_V3.md\`. This does not duplicate its canonical relation graph.

## Each observation

Identity and actor (observer.kind/ref) are distinct from observed target/ref/revision. Other dimensions: recorded date and optional event time; epistemic state; novelty relative to this intake, **not universal scientific novelty**; area/science track; conduct; semantic flags; typed edges; scope-bound evidence; gaps; falsifier; next gate.

Conduct: ATTENTION, SERVICE, ACTION, UPDATE, REVIEW, REFUSAL, BUG, ERROR, EDIT, REASON, PERMUTE, ANOMALY, DELTA, EMPTY. Semantic flags include POSSIBLE, VERBAL, ATEMPORAL, IGNORED, NONVERBAL, INCONSISTENCY, FORGOTTEN_RECORD, PARADOX, NONLINEAR, MULTI_PATH, NUMERIC_ZERO, NO_EVENT_OBSERVED. These are **classifications**, not physical measurements or cognitive assertions.

\`TOKEN_VAZIO != numeric 0 != no observed event\`. \`OBSERVED != DERIVED != HYPOTHESIS != CLAIM\`. Silence/ignored/not recorded is not evidence of nonexistence. An atemporal concept never removes the timestamp of a recorded event. Graph proximity/co-occurrence/analogy is not causal evidence.

## Priority observations, 2026-10-12

1. P0: Mapa PR #750 \`NÃO PROMOVER\` but merged=true reported. Exact PR SHA, original event time and readback evidence recorded. **Provider policy and review remain typed unknown**; never infer why it was merged.
2. P0: RLL PR #1108 exact-head 22 workflows: 18 success, 4 failed; merged status also observed. Each failure is an individual falsifier, not a proof that a scientific hypothesis is wrong.
3. P1: Physical runtime for Mapa #750 is \`TOKEN_VAZIO_PHYSICAL_RECEIPT_NOT_VERIFIED\` in the bounded review, not a declaration that no tests occurred anywhere.
4. P2: New semantic multi-path hypothesis requires a frozen benchmark; it has \`evidence_effect=NONE\`.

## Contradiction successor

Historical \`docs/OBSERVATIONS_MAPPING_MATRIX.md\` has a Pathway A that mentions **auto-promotion** when all O0–O11 appear green. That sentence is **not current approval authority**: all technical gates green does not grant provider/reviewer/rights authority, and no \`TOKEN_VAZIO\` being counted is not proof that none exist. Apply provider enforcement, rights checks, independent review and an explicit decision, each proven separately.

## Nonregression and rollback

Run \`python3 tools/validate_observer_observed_network_v1.py\` and \`python3 -m unittest discover -s tests -p test_observer_observed_network_v1.py\`. No production code, original ledger, policy, backend, existing dataset or CI workflow is changed. No automatic promotion or merge. Drop the isolated proposed branch/PR or revert its isolated changes; retain historical receipts.

R3: \`F_ok=typed model and negative falsifiers candidate\`; \`F_gap=exact-head CI, independent review, provider protection and physical receipts\`; \`F_next=validate current HEAD, gate promotion via server-side policy and readback\`.
