---
name: resilience-safety
description: Apply bounded fail-safe, rollback, failover, watchdog and minimum-sufficient intervention before risky execution.
version: 1.0.0
status: DRAFT_FAIL_CLOSED
---

# D4 — Resilience & Safety

## Principle

`maximum discernment + minimum sufficient intervention`.

Prefer `contain > destroy`, `isolate > erase`, `degrade_safely > improvise`, `HOLD > fabricated PASS`.

## Risk vector

`R=(authority, security, privacy, governance, integrity, availability, reversibility, uncertainty)`.

Risk is non-compensatory: any P0 dimension forces `HOLD`; unknown dimensions remain `TOKEN_VAZIO`, never zero risk.

## Mitigation ladder

`M0 observe → M1 isolate → M2 degrade safely → M3 failover known-good → M4 hotswap only with interface/state compatibility → M5 sandbox hotfix candidate → M6 bounded canary → M7 promote only after authority/evidence gates`.

## Watchdog

Monitor heartbeat, validator integrity, receipt freshness, hash/ref/clock coherence, rollback target, error/latency drift and storm/loop guards.

Heartbeat loss → `FAIL_CLOSED_HOLD`.

## Rollback

Require known-good ref, state/schema compatibility, reversibility decision and pre-mutation receipt. `rollback_success != prevention_control`.

## Output

`risk_vector`, `severity`, `blast_radius`, `minimum_intervention`, `watchdog_state`, `rollback_target`, `failover_target`, `hold_reason`, `F_ok/F_gap/F_next`.
