# RAFAELIA Shared Data Governance V2 — Authorial Operational Excellence

**State:** `CANONICAL_DRAFT / AUTHORIAL / PRIVATE_BY_DEFAULT / FAIL_CLOSED / APPEND_ONLY`

## Authorial boundary

The operational core does not use third-party names, seals, diagrams, visual taxonomies, certification language, or external representations as product identity or authority.

External material may be studied in a separate research-only zone, but it cannot automatically change gates, claims, release state, or the identity of this system.

`external_reference != operational_authority != implementation != execution != evidence != release`

## Drive authority

Governed root:

- `[C1_INTERNAL] RAFAELIA_DADOS_COMPARTILHADOS_GOVERNADOS_V1`
- folder id: `1U3G5dJwcbGxGWaSPu3WbH1WI1-Jeyi7x`

Shared-data subtree:

- `[C1_INTERNAL] DADOS_COMPARTILHADOS`
- folder id: `1pOQ68FarWfRmY6hiG4_9F2X0UrnG0pI2`

Classification names express eligibility, never automatic sharing permission.

## Authorial process tree

`ORIGIN -> QUALIFICATION -> PREPARATION -> TRANSFORMATION -> CONDUCTION -> EXECUTION -> OBSERVATION -> PARITY -> EVIDENCE -> RELEASE -> FEEDBACK -> NEW_ORIGIN`

Each transition binds precondition, input identity, transformation, risk, stop condition, evidence, rollback and receipt.

## Quality starts before execution

A final artifact cannot inherit quality that its origin does not sustain. When applicable, each candidate object records:

- source identity and authority;
- integrity/hash;
- criticality;
- purpose;
- transformation lineage;
- dependencies;
- context/environment relevant to interpretation;
- uncertainties and `TOKEN_VAZIO`;
- destination;
- known and unknown downstream effects.

## Parallel mirror + parity

Redundancy is not sufficient if two channels can repeat the same error.

```text
CHANNEL_A --\
            +--> PARITY_OR_INDEPENDENT_CRITERION --> DECISION
CHANNEL_B --/
```

Allowed comparison states: `MATCH | DIVERGENCE | TOKEN_VAZIO | BLOCKED`.

A critical divergence or unknown is not silently converted into consensus.

## Criticality

| Level | Meaning | Automated raw handoff |
|---|---|---|
| `C0_PUBLIC` | release-eligible candidate | only after explicit manifest/gate |
| `C1_INTERNAL` | internal metadata, manifests, indexes | bounded objects only |
| `C2_SENSITIVE` | minimization/redaction/risk staging | raw source blocked |
| `C3_RESTRICTED` | personal/sensitive/correlatable context | raw source blocked; human gate |
| `C4_CRITICAL` | secrets, credentials, keys, highly identifying/high-impact material | raw automation prohibited |

## Core invariants

1. private by default;
2. `fragmentation != anonymization`;
3. `hash != authorization`;
4. `small_fragment != small_impact`;
5. `unknown_effect != zero_risk`;
6. inference may locate a source but cannot promote a release;
7. critical unknowns remain `TOKEN_VAZIO` and block release;
8. purpose, recipient, scope, retention and reversibility are explicit;
9. downstream copies, caches, forks, logs and artifacts belong to the impact radius;
10. revocation changes effective state append-only and never rewrites historical receipts.

## Share Impact Envelope

Every governed release binds:

`share_id -> source/revision -> authority -> criticality -> data classes -> purpose -> recipient -> selected fields -> minimization/redaction -> reidentification risk -> semantic reconstruction risk -> cascade map -> TTL -> revocation -> human awareness -> approval -> evidence -> receipt`

For `C2+`, unresolved reidentification or semantic reconstruction risk blocks release.

## Cascade analysis

Before release, record:

- direct impact;
- second-order impact;
- affected dependencies;
- known consumers;
- unknown consumers as `TOKEN_VAZIO`;
- reidentification risk;
- semantic reconstruction risk;
- reversibility;
- TTL;
- revocation route;
- propagation already observed;
- point of no return, when one can exist.

## Human awareness

Sensitive release requires explicit awareness of:

- what leaves the boundary;
- why;
- destination;
- retention;
- what can be reconstructed or inferred;
- what remains unknown;
- how revocation works;
- what may not be recoverable after propagation.

## Authorial continual-improvement cycle

`DEFINE -> MEASURE -> ANALYZE -> IMPROVE -> CONTROL -> REVALIDATE`

- **DEFINE** — objective, scope, material, authority and risk.
- **MEASURE** — real observables; missing baseline stays `TOKEN_VAZIO`.
- **ANALYZE** — separate observed cause, correlation, hypothesis and unknown.
- **IMPROVE** — smallest bounded delta with rollback.
- **CONTROL** — gates, metrics, alerts, receipts and stop rules.
- **REVALIDATE** — source, dependency, threat, recipient or context changes reopen the gate.

## GitHub Actions boundary

`DRIVE_BRIDGE_ENABLED=false` remains the default.

Actions must not broadly enumerate Drive. Real Drive access, if ever enabled, requires a separate cycle with least privilege, bounded object identities, TTL, revocation and explicit human authorization.

C4 raw bytes are never eligible for automated handoff.

## Promotion boundary

`implementation != execution != evidence != release`

`policy_pass != privacy_proven`

`hash_valid != safe_to_share`

`CI_pass != human_authorization`

A release is allowed only when every applicable gate for the declared scope is satisfied. Otherwise the state is `BLOCK | QUARANTINE | TOKEN_VAZIO`.

## Stop rule

Do not release because a fragment looks harmless. Stop when the next required fact is unknown and record `TOKEN_VAZIO + F_next`.

A new cycle is required after material changes in source revision, purpose, recipient, transformation, criticality, TTL, threat model or downstream route.

## Final invariant

`VAZIO -> ORIGIN -> QUALIFICATION -> CONDUCTION -> EXECUTION -> EVIDENCE -> RELEASE -> FEEDBACK -> NEW_VAZIO`
