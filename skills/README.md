# RAFAELIA Ω Assurance Skills V1

Status: `DRAFT_FAIL_CLOSED`
Policy: `APPEND_ONLY | TOKEN_VAZIO_VALID | CLAIM_GATE_REQUIRED`

Repository-local skills are procedural adapters. They do **not** replace `AGENTS.md`, producer authority, evidence, or promotion gates.

## Entry

Use `omega-assurance-router` first for a non-trivial task. It routes to one or more bounded skills:

| Skill | Axis | Purpose |
|---|---|---|
| `identity-provenance` | D1 | bind exact identity, source, ref, revision and digest |
| `epistemic-discernment` | D2 | classify fact/hypothesis/model/theorem/anomaly/parabola/TOKEN_VAZIO |
| `execution-evidence` | D3 | separate artifact/build/runtime/physical execution |
| `resilience-safety` | D4 | fail-safe, rollback, failover, watchdog and blast-radius |
| `privacy-information` | D5 | classify disclosure/custody and default-deny unknown sensitivity |
| `authority-governance` | D6 | resolve who may read/write/promote and where |
| `transition-ledger` | D7 | record before→after, reason, falsifier, receipt and review trigger |
| `knowledge-attention` | cross | track ignored/deferred/aborted/orphaned/stale/contradicted knowledge |
| `crossfail-secure-sandbox` | cross | fault-injection and do-not-overreact tests inside owned fixtures |

## Global invariants

```text
VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM
TOKEN_VAZIO != 0
prediction != evidence
capability != authority
sandbox_pass != production_pass
failover_success != root_cause_resolved
rollback_success != prevention_control
search_miss != absence
```

Every skill must return, directly or through the router:

```text
F_ok
F_gap
F_next
claim_allowed
write_authority
receipt_required
```

Unknown material fields are explicit `TOKEN_VAZIO + reason + next verifiable gate`.
