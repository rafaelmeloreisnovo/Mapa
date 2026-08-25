# OMEGA Assurance Mesh V1 — Machine-Readable Contract Index

Status: `MATERIALIZED_LOCAL_VALIDATED_BRANCH`  
Policy: `APPEND_ONLY | FAIL_CLOSED | TOKEN_VAZIO_VALID | claim_allowed=false`  
Base: `main@1da6932b7a90215dda5fd8c2e2b1d27b114e6538`

## Outcome

This Wave adds the machine-readable layer that was still missing after the procedural Omega Assurance Skills V1 merge. It does not replace the existing watchdog, multifilament canon, authority pyramid, custody ledger, operational ontology, producer authority or repository rules.

The implementation is an identity with seven orthogonal projections, not seven copies:

| Axis | Contract |
|---|---|
| D1 | identity and provenance |
| D2 | epistemic class, uncertainty and falsifier |
| D3 | specification/build/test/runtime/physical evidence ladder |
| D4 | failure, blast radius, rollback and failover |
| D5 | privacy classification, disclosure and minimization |
| D6 | owner, write authority, promotion authority and review |
| D7 | append-only state transition, reason and next review |

Transverse bridges cover attention, evidence aging, risk, relations, scale, Serpent–Dove conduct and cross-layer failure tests. Longitudinal evolution is represented by new transitions and hash-linked ledger events.

## Materialized contracts

- `schemas/omega-assurance/omega7-node.schema.json`
- `schemas/omega-assurance/omega-transition.schema.json`
- `schemas/omega-assurance/watchdog-event.schema.json`
- `data/control-plane/omega-assurance/epistemic-state-registry.json`
- `data/control-plane/omega-assurance/attention-state-registry.json`
- `data/control-plane/omega-assurance/risk-vector.v1.json`
- `data/control-plane/omega-assurance/cross-layer-failure-matrix.json`
- `data/control-plane/omega-assurance/authorization-write-matrix.json`
- `data/control-plane/omega-assurance/rollback-failover-registry.json`
- `data/control-plane/omega-assurance/structural-relation-registry.v1.json`
- `data/control-plane/omega-assurance/scale-lattice.v1.json`
- `data/ledgers/omega-assurance/anomaly-paradox-ledger.v1.jsonl`

The entry registry is `data/control-plane/omega-assurance/omega-assurance-mesh.v1.json`.

## Routed technical domains

The cross-layer and epistemic registries include bounded gates for:

- lock-free structures: ownership, linearization, memory order, reclamation and progress argument;
- profiling: exact binary/environment, raw samples, baseline and p50/p95/p99;
- smart guard: policy scope, review, minimization and fail-safe behavior;
- phase integration: tier ownership, source of truth, invalidation, restart and partial failure;
- network protocol: framing, version, sizes, integrity/authentication and adverse transport cases;
- query system: grammar, precedence, null/collation/ordering semantics and resource bounds;
- RLL/cosmology: code, data, likelihood, covariance, LambdaCDM baseline, priors, convergence and falsifier.

No result in those domains is claimed by this Wave. Their execution and measurement states remain `TOKEN_VAZIO` until the named producer gate yields evidence.

## Falsification suite

The validator and ten unit tests reject, among other cases:

- `TOKEN_VAZIO` promoted as a claim;
- mutation or promotion with unknown authority/privacy;
- irreversible material action with unknown rollback;
- a P0 compensated by favorable dimensions;
- a watchdog acting on ambiguous evidence;
- stale, failed or unknown watchdog heartbeat acting instead of holding;
- private locator injection into the public contract bundle.

The dedicated workflow also re-runs the prior skill registry, adaptive watchdog and authority-pyramid gates to detect integration drift.

## Evidence boundary

A PASS proves only that these files form the tested structural fail-closed contract at the exact ref. It does not prove:

- production watchdog activation;
- agent or producer adoption;
- lock-free or wait-free progress;
- performance, capacity or latency;
- network interoperability or protocol security;
- physical rollback, hotswap or failover;
- RLL or cosmological evidence;
- legal compliance or certification.

## F_ok / F_gap / F_next

`F_ok`: machine-readable schemas, registries, typed relations/scales, cross-fail matrix, ledger, validator, fixtures and workflow are materialized on an isolated branch.

`F_gap`: remote gates are unobserved at index creation; independent review and main-branch enforcement remain unresolved; producer/runtime/performance/failover evidence remains `TOKEN_VAZIO`.

`F_next`: open a draft PR, observe the exact CI head, append a qualification receipt, and retain `claim_allowed=false` until ordinary governance gates close.
