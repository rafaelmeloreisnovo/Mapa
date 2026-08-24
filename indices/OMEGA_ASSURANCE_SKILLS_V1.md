# Ω Assurance Skills V1 — Implementation Index

Status: `IMPLEMENTED_UNVERIFIED_BRANCH`
Policy: `claim_allowed=false`
Base: `main@f1a96df83d0969a012358ee321be814d0656f377`

## Objective

Materialize the Omega Assurance Mesh as repository-local procedural skills, subordinate to `AGENTS.md`, producer authority and the canonical bootstrap.

## Composition

There are **9 operational skills plus 1 router**:

1. `omega-assurance-router` — bounded orchestration;
2. `identity-provenance` — D1;
3. `epistemic-discernment` — D2;
4. `execution-evidence` — D3;
5. `resilience-safety` — D4;
6. `privacy-information` — D5;
7. `authority-governance` — D6;
8. `transition-ledger` — D7;
9. `knowledge-attention` — forgotten/stale/ignored/anomalous knowledge;
10. `crossfail-secure-sandbox` — cross-layer negative/fault-injection qualification.

## Serpent–Dove translation

Engineering rule:

`SEE_MORE != CLAIM_MORE`  
`CAN_DO != MAY_DO`

Discern deeply; intervene minimally. Technical capacity cannot manufacture authority.

## Failure semantics

The skills are designed to preserve:

- `TOKEN_VAZIO != PASS`;
- `search_miss != absence`;
- `sandbox_pass != production_pass`;
- `unknown_privacy => PRIVATE_DEFAULT_DENY`;
- `unknown_authority => HOLD_FOR_AUTHORITY`;
- `irreversible_unknown_risk => HOLD`.

## Tests

`tests/test_omega_assurance_skills_v1.py` falsifies the registry by deliberately attempting:

- `claim_allowed=true`;
- unknown dependency;
- dependency cycle;
- removal of `TOKEN_VAZIO != PASS`;
- private Drive-style locator injection.

The validator also requires critical per-skill markers and an acyclic dependency graph.

## Relationship to existing control plane

This Wave does not replace:

- `governance/RAFAELIA_ADAPTIVE_RESILIENCE_WATCHDOG_V1.json`;
- `docs/canonicos/RAFAELIA_CONVERGENCIA_MULTIFILAMENTO_OMEGA_V1.md`;
- `data/control-plane/federated-reference-matrix.v1.json`;
- `AGENTS.md`;
- producer-specific gates/receipts.

Skills are procedural adapters that make those controls discoverable and composable.

## Promotion boundary

A passing skill validator proves only structural/semantic integrity of these skill contracts. It does **not** prove production watchdog operation, runtime failover, legal compliance, or scientific truth.

## F_ok / F_gap / F_next

`F_ok`: skill contracts + registry + fail-closed validator + negative tests + workflow materialized on branch.

`F_gap`: CI not yet observed at index creation; runtime adoption by agents/producers remains unproven; existing governance blockers remain independent.

`F_next`: open draft PR → execute dedicated workflow/general CI → append receipt with exact run IDs → keep `claim_allowed=false` until normal governance gates close.
