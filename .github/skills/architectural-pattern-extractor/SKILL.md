---
name: architectural-pattern-extractor
description: Extract reusable operational patterns from languages, databases, runtimes, legacy systems, or prior architectures and adapt them to the current repository without importing their incidental syntax or violating local authority. Use when asked to learn from an architecture, transplant a mechanism, derive a reusable behavior, or reconstruct a solution from a prior technical pattern.
---

# Architectural Pattern Extractor

This skill turns a concrete technology or historical architecture into a bounded reusable operational pattern.

It is a procedural adapter, not authority, evidence, novelty proof, or permission to weaken repository rules.

## Core seed

```text
source architecture
-> extract mechanism
-> separate invariant from incidental implementation
-> normalize state/trigger/guard/action/evidence/failure/rollback
-> map to the local repository role
-> apply the smallest compatible leaf
-> execute the narrowest available falsifier
-> record F_ok / F_gap / F_next
```

## Mandatory preflight

1. Read repository `AGENTS.md` and any nearer scoped instructions.
2. Bind repository, ref/commit, target path and current authority boundary.
3. Classify the source pattern as reference/inspiration unless stronger evidence exists.
4. Identify local invariants that cannot be weakened.
5. Keep missing evidence as `TOKEN_VAZIO`; do not infer PASS from similarity.

## Normalize the source

Represent the useful mechanism as:

```yaml
pattern:
  source_family: REFERENCE
  trigger: TOKEN_VAZIO
  state: TOKEN_VAZIO
  inputs: []
  guards: []
  action: TOKEN_VAZIO
  outputs: []
  integrity_rules: []
  evidence_required: []
  failure_mode: TOKEN_VAZIO
  rollback: TOKEN_VAZIO
  claim_allowed: false
```

Do not preserve syntax merely because it existed in the source technology. Preserve behavior only when it improves the current system and survives local gates.

## Reference examples

### Pascal-like variable discipline

Possible transferable mechanisms include explicit type boundaries, initialization discipline, numeric-range checks, deterministic state transitions and explicit error handling.

Do not copy Pascal syntax into another subsystem unless Pascal itself is the target language.

### InterBase-like trigger discipline

Possible transferable mechanisms include event-conditioned activation, transactional guards, integrity checks, durable logging and deterministic post-event actions.

Do not turn every event into an implicit trigger. The local subsystem must own the event, state transition and rollback semantics.

## Reusable geometry families

Historical machine and database architectures may carry useful geometry beyond their original syntax. Normalize them into the following families before adapting them.

### Event and persistence geometry

```text
request/event
-> validate
-> append or stage
-> durable commit
-> sequence/hash identity
-> index
-> derived current view
```

Treat create/add, update, delete and commit as distinct transitions. An update or delete may be represented as a successor event instead of destructive mutation when the local contract is append-only.

The important questions are where identity is created, when state becomes durable, what can be rolled back, and which artifact proves the transition.

### Allocation and identifier geometry

Extract rules for:

- identifier generation point and ownership;
- explicit integer width/range and conversion policy;
- auto-number or sequence allocation;
- logical key layout versus physical placement;
- collision, overflow, wrap and reuse behavior;
- per-user/per-domain partitioning only when local authority requires it.

Do not confuse a convenient physical layout with identity semantics.

### Storage locality geometry

Normalize old disk/page/block reasoning as a cost model:

```text
logical record
-> page/block
-> allocation unit
-> physical medium locality
-> access latency / transfer cost
-> fragmentation / compaction state
```

Sector, track, head, page, erase block, cache line and extent are technology-specific instances of a broader locality/allocation model.

Historical latency values, media classes or controller timings are measurement inputs, not universal constants. Re-measure on the current target before using them for optimization claims.

### Memory and bus geometry

Translate conventional/high-memory maps, banked windows, DMA/IRQ, ISA-like buses, north/south bridge separation, MMIO and address ranges into:

- address-space ownership;
- capability/resource discovery;
- alignment and width constraints;
- interrupt/event routing;
- transfer ownership;
- voltage/electrical constraints only at the hardware boundary.

Never copy a historical address, interrupt or voltage into a modern target without an owning hardware contract.

### Protocol-stack geometry

Keep layers distinct:

```text
physical medium
!= link framing
!= network protocol
!= transport/session
!= application command
```

A cable/termination rule, a network protocol, and a modem command set are separate pattern families even if they were used in the same historical installation.

Transfer state machines, framing, capability negotiation, retry, timeout and integrity behavior only at the layer that owns them.

### Binary and OS-layout geometry

Executable headers, partition tables, filesystem metadata, registry/config trees, service state, file alignment and loader-visible flags can be normalized as:

```text
header/schema
-> validated offsets/lengths
-> mapped objects
-> activation/load order
-> visible state
-> recovery/failure path
```

A historical binary or OS structure is a reference model; exact offsets and magic values require current-source evidence before reuse.

### Device-control geometry

Serial, parallel, GPIO-like signaling, relays, sensors and discrete components reduce to a boundary model:

```text
command
-> encoded signal
-> electrical interface
-> device transition
-> observed feedback
```

Software state never proves the electrical transition. Hardware voltage/current/noise constraints require a hardware-specific falsifier and safety boundary.

## Leaf adaptation

Before applying a pattern, answer:

- What local problem does this mechanism solve?
- Which local invariant does it preserve or strengthen?
- What is the minimum implementation delta?
- What observable condition falsifies the adaptation?
- What evidence would justify promotion beyond `IMPLEMENTED`?

If the source pattern conflicts with local architecture, authority, privacy, security or evidence rules, stop and record `TOKEN_VAZIO/HOLD` rather than forcing the transplant.

## Public/private boundary

A public repository may receive the abstract reusable mechanism, but not private source prompts, raw conversation text, private corpus records, private locators, credentials, personal data or hidden provenance payload.

When a pattern was derived from private material, publish only the sanitized abstraction needed for the local task. Keep the private derivation and source pointers in their private authority domain.

## Non-negotiable distinctions

```text
pattern similarity != proof of origin
pattern extraction != implementation
implementation != execution
execution != evidence
skill != authority
skill != evidence
TOKEN_VAZIO != 0 != false != PASS
```

## Completion record

End each use with:

```text
source_pattern = what mechanism was extracted
local_leaf     = where/how it was adapted
falsifier      = what could prove the adaptation wrong
F_ok           = what was actually changed or demonstrated
F_gap          = what remains unknown/unexecuted
F_next         = smallest reproducible next action
claim_allowed  = false unless a separate bounded gate promotes it
```
