# RAFAELIA Orchestrator Frontline V1

**State:** `CANONICAL_DRAFT`  
**Claim gate:** `claim_allowed=false`  
**Default mode:** read-only, local-first, fail-closed  
**First functional fruit:** Universal Doctor

## Root question

> Which module is authorized to understand, decide, execute, observe, persist and present each state — and which evidence must cross the boundary before the next layer can act?

## Sustaining invariant

```text
I_ORQ = Identity × Contract × Boundary × Event × Evidence × Return
```

A repository is a governance/versioning unit. A module is a capability unit. A product is a usable experience. A fruit is a verifiable result. An artifact is a material output. Evidence supports a bounded claim about that result.

## Canonical planes

| Plane | Primary component | Responsibility | Safe boundary |
|---|---|---|---|
| Intent | LlamaRafaelia / typed interpreter | Produce candidate `IntentIR` from bounded inputs | No shell execution and no raw unbounded ingestion |
| Control | RafGitTools | Authentication, gates, capability resolution, jobs and operator state | Read-only status when transport or evidence is missing |
| Topology | Mapa + Matrix | Registry, dependencies, product graph, questions and decisions | Derived views never replace source evidence |
| Execution | termux-app-rafacodephi | Execute allowlisted jobs and emit results | Diagnostic-only until transport and rollback are proved |
| Evidence | RafPolimata / RafBBS | Canonicalize, verify, hash, manifest and expose gaps | Claims remain read-only when evidence is incomplete |
| Virtualization | Vectras-VM-Android + qemu_rafaelia | Isolated guest/workspace lifecycle | VM stopped and no image mutation on preflight failure |
| Data/Memory | Drive/rclone, GAIA, MemRafcode | Ingest, index, cache, checkpoint and retain provenance | Cache is never source authority without revision/hash |
| Observability | EventBus/Syslog/Ledger/R3 | Correlate events, artifacts, evidence and feedback | Local JSONL spool when transport is unavailable |

## Canonical flow

```text
Human/chat
  -> IntentIR
  -> GovernanceGate
  -> CapabilityResolver
  -> immutable JobEnvelope
  -> authorized executor
  -> EventEnvelope JSONL
  -> ResultEnvelope + EvidenceEnvelope
  -> Ledger / Matrix / Mapa / Drive
  -> operator surface and R3
```

The VM branch is selected only after a `VM_REQUIRED` gate. Git status, Drive inventory, hashing, cataloguing and light local scripts do not require a VM by default.

## Contract files

- `contracts/module_registry.schema.json`
- `contracts/event_envelope.schema.json`
- `contracts/product_graph.schema.json`

Existing contracts that must be reused rather than duplicated:

- RafGitTools `docs/contracts/intent_ir.schema.json`
- RafGitTools `schemas/rafaelia_runtime_job.schema.json`

A later contract phase may add `ResultEnvelope`, `EvidenceEnvelope`, `WorkspaceManifest` and a versioned cache-key schema after the read-only path is proved.

## Fixtures and preflight

Canonical fixtures:

- `fixtures/module_registry.valid.json`
- `fixtures/event_envelope.valid.json`
- `fixtures/product_graph.valid.json`

Run the dependency-free structural preflight:

```sh
python3 scripts/validate_orchestrator_contracts.py
```

The preflight proves JSON parsing, critical identifier rules, unique module/node/edge IDs, graph endpoint integrity, structured `TOKEN_VAZIO` gaps and complete R3 fields. It **does not** claim full JSON Schema draft-2020-12 validation and it does not execute Android, Termux, network, VM or cross-repository runtime.

## First product: Universal Doctor

The first product is intentionally read-only. It answers capability questions before orchestration is allowed to mutate anything.

Minimum report per module:

```text
module_id
repository
branch
observed_ref
health_probe
capabilities_declared
capabilities_observed
host
arch
state
safe_state
evidence_refs
known_gaps
next_action
```

Official result states:

```text
PASS
PASS_LIMITED
FAIL
BLOCKED
TOKEN_VAZIO
```

File presence is never sufficient for `PASS`. A probe must record command or method, environment, exit state, output/artifact references and source commit.

## Gates

| Gate | Meaning |
|---|---|
| O0 | Module registered with source identity and bounded capabilities |
| O1 | Contracts reject malformed and ambiguous fixtures |
| O2 | First read-only trace crosses control -> Termux -> result -> ledger |
| O3 | `trace_id` remains continuous across modules |
| O4 | Restart/replay does not duplicate side effects |
| O5 | Cache invalidates on schema, commit, source revision, policy or TTL change |
| O6 | Secrets and unnecessary personal data are redacted |
| O7 | Result is bound to authorized action, environment, artifacts and hashes |
| O8 | Unknown or missing evidence never becomes implicit `PASS` |
| O9 | Rollback is tested before a mutating capability is enabled |
| O10 | VM starts only after justification, artifact validation and preflight |
| O11 | Ledger and Matrix close the run with `F_ok`, `F_gap`, `F_next` |

## Product graph

The graph preserves this sequence:

```text
repository -> module -> capability -> product -> fruit -> artifact -> evidence -> claim
```

Every edge has an authority state:

- `VERIFIED`
- `DECLARED`
- `PARTIAL`
- `CONTRADICTION`
- `TOKEN_VAZIO`

An edge with `TOKEN_VAZIO` must include the next verifiable step.

## Logical service names

These are contract namespaces, not public DNS requirements:

```text
control.rafaelia.local
intent.rafaelia.local
exec.rafaelia.local
evidence.rafaelia.local
index.rafaelia.local
memory.rafaelia.local
vm.rafaelia.local
qemu.rafaelia.local
syslog.rafaelia.local
chat.rafaelia.local
```

The first cycle needs no exposed network service. Local files and JSONL spool are sufficient.

## Cache invariant

```text
cache_key = hash(
  schema_version
  + module_id
  + module_version
  + operation
  + normalized_inputs
  + source_revision
  + policy_hash
)
```

A cache hit must identify its producer, source revision, policy and validity. When those cannot be demonstrated, the result is a miss or `TOKEN_VAZIO`, never canonical evidence.

## Implementation order

1. Freeze and review contracts in this draft PR.
2. Run the dependency-free preflight.
3. Add full draft-2020-12 validation when the repository dependency policy is decided.
4. Implement Universal Doctor in RafGitTools, read-only.
5. Add a minimal `EventEnvelope` JSONL writer to RafGitTools and Termux.
6. Implement local inbox/active/outbox/quarantine spool with atomic rename.
7. Execute one `inventory_source` job end to end.
8. Adapt RafBBS output to `EvidenceEnvelope` without removing its human log.
9. Add Control Deck read-only views.
10. Introduce `VM_REQUIRED` and `WorkspaceManifest` only after O0-O8 are measured.

## Current R3

**F_ok:** Module, event and product-graph contracts; valid fixtures; dependency-free preflight; topology and gates are materialized on an isolated branch.  
**F_gap:** Full JSON Schema validation and every cross-repository runtime path remain unexecuted; Termux transport, JSONL adapters, Result/Evidence envelopes and VM gates are not complete.  
**F_next:** Review this draft PR, execute the preflight, then implement Universal Doctor as the first read-only product fruit.
