# Rafaelia Arco 7: Routing & Retrospection Schema

**Version**: 1.0  
**Date**: 2026-08-18  
**Phase**: psi-prime (ψ')  
**Module**: `raf_route`

---

## Overview

Arco 7 completes the Rafaelia Adaptive Cycle by routing decision outcomes back into prospection for the next cycle. This phase transforms conclusions into actionable signals for future observation.

**Not a return to psi** — psi-prime is retrospective routing, not a restart. It answers: "Given what happened, what should be observed next?"

---

## Core Concepts

### Routing Decision

The decision output from Arco 6 (Omega verification) becomes a **routing signal**:

```json
{
  "source_arco": 6,
  "decision": "VERIFIED_LATEST_FOUR_READ_ONLY",
  "evidence_set": ["hash_chain", "receipt_signatures", "audit_timestamp"],
  "next_cycle_observations": [
    "monitor hash_chain_continuity for break patterns",
    "track claim_allowed promotion attempts",
    "observe epistemic_state advancement gates"
  ],
  "routing_target": "lane_01_intake_sources",
  "priority": "P0"
}
```text

### Retrospection

After routing, the cycle retrospectively documents:

- What was observed? (chi → observation integrity)

- What was transformed? (delta → ethical gates passed)

- What was verified? (omega → decision confidence)

- What gaps remain? (TOKEN_VAZIO markers)

---

## Routing Targets (10 Lanes)

| Target | Purpose | Decision Triggers |
|--------|---------|-------------------|
| **Lane 00** | Governance update | Policy change required, schema version bump |
| **Lane 01** | New source intake | Dependency discovered, external link validated |
| **Lane 02** | Normalization review | Schema collision, ambiguous naming |
| **Lane 03** | Semantic model extension | Ontology gap discovered, new relation type needed |
| **Lane 04** | Validation enhancement | Falsifier gap, new constraint discovered |
| **Lane 05** | Evidence collection | Artifact missing, reproducibility gap |
| **Lane 06** | Integration staging | Module interface mismatch, version conflict |
| **Lane 07** | Security/Compliance review | Risk escalation, threat model update |
| **Lane 08** | Release readiness assessment | Regression candidate, performance degradation |
| **Lane 09** | Archive & retention | Retention policy applied, historical checkpoint |

---

## Retrospection Schema

Each completed cycle produces a retrospection record:

```json
{
  "cycle_id": "RAF-CYCLE-20260817T045531Z-N25",
  "retrospection": {
    "arco_timeline": {
      "psi": {
        "intention": "Observe claim_allowed gate",
        "duration_ms": 250,
        "completeness": "full"
      },
      "chi": {
        "observations_collected": 8,
        "all_8_required_fields_present": true,
        "duplicates_found": 0
      },
      "rho": {
        "noise_factors": ["gh_runner_clock_skew_12ms", "transient_network_delay"],
        "layout_verified": true
      },
      "delta": {
        "ethical_gates_passed": ["claim_allowed=false", "fail_closed=true"],
        "transformations_applied": 0,
        "mutations_rejected": 0
      },
      "sigma": {
        "coherent_memory": "hash_chain_verified_complete_index_and_latest_four",
        "composition_integrity": true
      },
      "omega": {
        "verification_gates": ["signature_valid", "timestamp_monotonic", "dependency_acyclic"],
        "verification_result": "PASSED"
      },
      "psi_prime": {
        "retrospection_complete": true,
        "routing_decision": "VERIFIED_LATEST_FOUR_READ_ONLY"
      }
    },
    "token_vazio_observed": [
      {
        "id": "TOKEN_VAZIO_DEPENDENCY_LICENSE_COMPATIBILITY_NOT_AUDITED",
        "affected_component": "rafaelia-adaptive-cycle v1.0",
        "status": "PRESERVED",
        "next_action": "Lane 07 security/compliance review",
        "priority": "P2"
      }
    ],
    "next_cycle_forecast": {
      "critical_observations": [
        "Monitor for any claim_allowed=true injection attempts",
        "Verify hash_chain discontinuity detection fires",
        "Check receipt timestamp monotonicity across runs"
      ],
      "lane_assignments": {
        "lane_04": "Add falsifier for claim_allowed=true case",
        "lane_05": "Collect run 408-411 artifacts for reproduction",
        "lane_07": "Audit unresolved license compatibility (TOKEN_VAZIO)"
      }
    }
  }
}
```text

---

## Routing Rules (Fail-Closed)

1. **Route only on verified decision** — Omega verification must pass before routing

2. **Preserve decision immutability** — Routing does not re-examine or re-decide

3. **Token Vazio explicit** — Gaps in next-cycle observations must be marked, never elided

4. **Lane ownership** — Each lane must acknowledge its routed work or reject with reason

5. **Append-only record** — Retrospection is immutable; corrections require new cycle

---

## Connection to Arco 1 (psi)

Arco 7 routing creates the input signal for the next cycle's psi (prospection):

```text
Cycle N, Arco 7 (psi-prime):
  Decision: VERIFIED_LATEST_FOUR_READ_ONLY
  Routing: Lane 01 [new source], Lane 04 [validation], Lane 07 [security]
  
Cycle N+1, Arco 1 (psi):
  Intention: "Verify the 3 routed items from Cycle N"
  Observation targets: sources from Lane 01, falsifiers from Lane 04, threats from Lane 07
```text

This closes the loop without returning to psi — it creates a forward arrow.

---

## Example: Run 407 Routing

From WORKFLOW_RECEIPTS_VALIDATION_REPORT.md:

```json
{
  "cycle_id": "RAF-CYCLE-20260817T045531Z-N25",
  "arco_6_decision": "VERIFIED_LATEST_FOUR_READ_ONLY",
  "arco_7_routing": {
    "primary_target": "lane_01_intake_sources",
    "reason": "Next workflow runs 408-411 will generate new receipts",
    "signal": "Continue latest-four window monitoring",
    
    "secondary_targets": [
      {
        "lane": 4,
        "work": "Add negative test: claim_allowed mutation injection attempt",
        "priority": "P0"
      },
      {
        "lane": 5,
        "work": "Store run 407 artifacts for Cycle N+1 reproducibility",
        "priority": "P1"
      },
      {
        "lane": 7,
        "work": "Audit TOKEN_VAZIO_PINNED_ACTION_NODE24_NATIVE_COMPATIBILITY",
        "priority": "P2"
      }
    ],
    
    "token_vazio_preserved": [
      "TOKEN_VAZIO_DEPENDENCY_LICENSE_COMPATIBILITY_NOT_AUDITED",
      "TOKEN_VAZIO_PINNED_ACTION_NODE24_NATIVE_COMPATIBILITY_NOT_VERIFIED"
    ]
  }
}
```text

---

## Implementation Notes

- **raf_route** module does not execute routing — it documents routing decisions

- Actual work is assigned to lane owners (Lane 00-09) via audit trail

- Routing is not optional; every cycle must route or document refusal (fail-closed)

- Each lane maintains its own queue of routed work in `/data/audits/lane-*.queue.jsonl`

---

## References

- `/docs/architecture/RAFAELIA_7_ARCOS_RAFCONVERT_RAFDISK_V1.md` — Full arco definitions

- `/docs/governance/BRANCH_TOPOLOGY_MAIN_NUMBERED_V1.md` — Lane 00-09 responsibilities

- `/data/audits/` — Lane work queues and routing history
