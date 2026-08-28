# Google Drive Observation & Invariants ATLAS V1

State: `VERIFIED_LIMITED / APPEND_ONLY / claim_allowed=false`

This ATLAS routes observations from private Google Drive material through the existing **Invariante das Invariantes Ω** instead of creating a competing ontology.

## Core boundary

```text
OBSERVATION
!= INTERPRETATION
!= PATTERN_CANDIDATE
!= INVARIANT_CANDIDATE
!= VALIDATION
!= EXECUTION
!= EVIDENCE
!= CLAIM
```

The controlling gate remains:

```text
I_OMEGA(X) = ID * C * H * P * E * F * Q * G * R * D
```

`TOKEN_VAZIO` preserves a failed or unknown factor and its next gate. It never means numeric zero.

## Surface authority

| Surface | Authority | Cannot prove alone |
|---|---|---|
| Google Drive / NOVOexport | private source, editorial authority, custody | runtime, independent replication, scientific validity |
| `rafaelmeloreisnovo/Mapa` | logical identity, ontology, typed relations, ATLAS/routing | physical execution not observed |
| `instituto-Rafael/RAFAELIA_CORE` | institutional contract, fences, watchdog | producer-domain truth by itself |
| RLL / papers | scientific producer authority under its own gates | promotion without baseline/falsifier/evidence |
| runtime producers | executable behavior with receipts | unexecuted source behavior |

## Macros

- `ATLAS:X` — select route by authority/evidence.
- `NOVO:X` — use provider-bound NOVOexport first when it is the requested corpus.
- `L:X` — compare the same logical identity over revisions.
- `O:X` — test independent axes without collapsing authorities.
- `T:X` — traverse typed cross-relations.
- `REL:X` — preserve type, direction, provenance and falsifier.
- `SCALE:X` — record scale only when the scale mapping exists.
- `EVID:X` — separate observation/execution/evidence/claim.
- `GAP:X` — preserve gaps as `TOKEN_VAZIO` plus next gate.
- `LEARN:X` — append deltas, contradictions, supersessions and receipts.

## O0–O11 route

`O0 intent → O1 provider identity → O2 custody → O3 privacy/license → O4 structure → O5 semantic extraction → O6 longitudinal → O7 orthogonal/transversal → O8 invariant candidacy → O9 falsification → O10 authority routing → O11 receipt`.

No later stage is implied by an earlier stage.

## Possibility classes

| Class | What can be examined | Minimum close condition |
|---|---|---|
| `PI-IDENTITY` | stable logical identity | provider identity + identity falsifier |
| `PI-CUSTODY` | source/hash/lineage | provider-bound locator + hash or explicit gap + lineage |
| `PI-STRUCTURE` | persistent schema/topology | comparable versions + counterexample search |
| `PI-TEMPORAL` | longitudinal relation | same identity + comparable revisions + freshness basis |
| `PI-SEMANTIC` | stable declared meaning | definition + occurrence provenance + semantic falsifier |
| `PI-RELATIONAL` | persistent typed relation | direction/type + independent support |
| `PI-NUMERIC` | formula/constant | semantics + units + representation/quantization + numeric falsifier |
| `PI-BEHAVIORAL` | runtime behavior | executable + environment + input/output receipts + reproduction |
| `PI-SCIENTIFIC` | scientific hypothesis/model | producer baseline + falsifier + declared statistical/test gate + evidence |

A frequent token, formula or relation is a **recurrence**, not automatically an invariant.

## Observation record

Every observation that can affect a route should preserve at minimum:

```text
observation_id
provider_id
logical_id
source_surface
source_family
locator
revision
content_hash
parent_hash
capture_time
privacy_class
authority_role
observation_type
extracted_features
relations
invariant_candidates
falsifiers
contradictions
uncertainty
risk
evidence_state
claim_allowed
rollback_locator
receipt_locator
next_gate
```

## Hard guards

- same filename ≠ same logical identity;
- timestamps alone ≠ freshness;
- frequency ≠ truth;
- source code ≠ execution;
- symbolic formula ≠ physical law;
- same-author rerun ≠ independent replication;
- private Drive body is not copied to public GitHub for convenience;
- absent provider ID/hash/license/unit/semantics remain `TOKEN_VAZIO`;
- conflicting constants are versioned/adjudicated, never silently overwritten;
- Drive observation never authorizes autonomous writes into a producer.

## Continuous observation

```text
new revision / new file / new relationship
-> capture delta
-> identity + custody gate
-> typed relation recomputation
-> invariant candidate update
-> falsifier / counterexample rerun
-> drift + contradiction ledger
-> append-only receipt
```

### External mirrored procedure

Google Drive native document ID: `19PYVBAfaCfTDOOnXmYnTp7MbEU38Crc4hRaW5APgeg4`

CORE machine-readable contract: `instituto-Rafael/RAFAELIA_CORE/governance/google_drive_observation_analysis_protocol.v1.json`
