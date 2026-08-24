---
name: crossfail-secure-sandbox
description: Qualify mitigations with cross-layer fault injection and do-not-overreact tests using only owned, bounded fixtures/sandboxes.
version: 1.0.0
status: DRAFT_FAIL_CLOSED
---

# Cross — CrossFail Secure Sandbox

## Boundary

Allowed only on owned test fixtures/sandboxes. Never attack third-party systems, harvest credentials, bypass authorization, or run destructive production tests.

## Cross-layer matrix

Test both containment and honesty:

```text
D1 fails → D2 must not invent identity/meaning
D2 fails → D6 must block promotion
D3 fails → D4 must hold/degrade/rollback safely
D4 fails → D5 must preserve privacy boundary
D5 fails → D6 must freeze disclosure/write
D6 fails → D7 must record denied attempt without mutation
D7 fails → previous state must remain reconstructible
```

## Required test families

1. `TEST_FAIL_CLOSED` — real fault causes HOLD/containment.
2. `TEST_DO_NOT_OVERREACT` — ambiguous signal does not manufacture incident/PASS/absence.
3. `TEST_ROLLBACK_REHEARSAL` — known-good state is recoverable.
4. `TEST_FAILOVER_BOUNDARY` — failover does not claim root-cause resolution.
5. `TEST_PRIVACY_DEFAULT_DENY` — unknown sensitivity blocks disclosure.
6. `TEST_AUTHORITY_DENY` — capability without authority cannot mutate/promote.
7. `TEST_WATCHDOG_FAILURE` — heartbeat loss produces bounded HOLD, not creative failover.

## Falsifiers

A single case where unknown identity/evidence/authority/privacy/reversibility becomes PASS without the named gate fails the skill qualification.

## Outputs

For every case: `fixture_id`, `fault`, `expected_failure`, `observed_failure`, `expected_mitigation`, `observed_mitigation`, `falsifier`, `blast_radius`, `rollback_result`, `receipt`.
