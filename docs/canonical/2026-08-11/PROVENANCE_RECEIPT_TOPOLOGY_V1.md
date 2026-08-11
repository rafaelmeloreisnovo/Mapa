# RAFAELIA — Provenance → Receipt Topology V1

Date: 2026-08-11  
State: `GOVERNED_PARTIAL`  
Claim gate: `claim_allowed=false`  
Targets: `FG-006` (single chain of custody), `FG-033` (navigable semantic index), and the anti-regression part of `FG-036`.

## 1. Mother invariant

The canonical path is:

`source → identity → claim → evidence → execution → receipt → gate`

Time is **independent** of that path. A document may describe a future run, but a future timestamp/plan does not become execution merely because the file exists.

This extends—not replaces—the existing operational record and F_GAP ledger. Existing receipts remain receipts; this topology is the navigation and reconciliation layer.

## 2. Tree inside the vector matrix

Each node carries an 8-axis vector:

| Axis | Question |
|---|---|
| `source` | Does the source exist and was it observed? |
| `identity` | Are exact bytes/version/provider bound? |
| `claim` | What is being asserted, and is it bounded? |
| `evidence` | Is evidence absent, documented, executed or reproduced? |
| `execution` | Was anything actually run? |
| `receipt` | Is there an inspectable receipt? |
| `gate` | Is the node `F_OK`, `F_GAP`, or still empty? |
| `time` | Is this observed, historical, future-planned, or unknown? |

The graph (`edges`) supplies the tree/topology. The vector supplies the local state. Together they prevent a semantic relation from silently becoming evidence.

## 3. ΣΩΔΦ sigil

`sigil = ΣΩΔΦ::<NODE_ID>` is only a **stable symbolic label** for human navigation. It is not a cryptographic signature and must never substitute for `content_sha256`, Git commit/blob identity, provider ID, or receipt hashes.

This separation is intentional:

`symbolic identity ≠ cryptographic identity`

## 4. Fail-closed promotion

A node can be `F_OK` only when:

1. `identity=BOUND`;
2. evidence is `EXECUTED` or `REPRODUCED`;
3. execution is `EXECUTED` (or genuinely `NOT_APPLICABLE`);
4. receipt is `PRESENT` (or genuinely `NOT_APPLICABLE`);
5. no vector axis is `TOKEN_VAZIO`;
6. time is observed/past-recorded, never future-planned.

`CLOSED` additionally requires `gate=F_OK`.

The validator enforces these rules mechanically.

## 5. Current proof-of-concept map

The initial graph anchors:

- the Drive canonical method “Implementação Latentes e Papers — Drive GitHub V1”;
- the F_GAP ledger schema;
- the operational-record schema;
- the existing vertical-slice reference receipt;
- FG-006 and FG-033;
- Fase 2 and Fase 3 documents as **future-planned nodes**, not execution evidence.

The vertical-slice receipt is intentionally `EVIDENCED_LIMITED`: it contains command, hashes, exit code and limitations, but its own `commit` field is still `TOKEN_VAZIO_GIT_COMMIT_NOT_BOUND_AT_REFERENCE_RUN`, and the runtime is a reference container rather than Android Termux.

## 6. Natural next traversal

For every important concept:

`concept`
→ `source node`
→ `artifact identity`
→ `claim node`
→ `run`
→ `receipt`
→ `decision`
→ `gap/next test`

No edge authorizes promotion by itself. Promotion depends on the node vector and receipt identity.

## 7. What this closes—and what it does not

This commit **does not close FG-006 or FG-033**. It materializes the missing topology contract and a seed graph.

Remaining `F_gap`:

- immutable byte hashes for Drive sources;
- exact Git commit binding for all GitHub anchors;
- ingestion of the full concept inventory;
- deterministic query coverage over the graph;
- execution/replay receipts for scheduled future phases;
- independent/physical-runtime reproduction where required.

Only after those are observed should a later append-only decision consider promotion.

## 8. Validation and navigation

Validate:

```bash
python3 scripts/validate_provenance_topology.py
```

Expected initial result:

```text
PASS: data/governance/provenance_topology.v1.json nodes=8 edges=7 F_OK=0 TOKEN_VAZIO=5 future_planned=2 claim_allowed=false
```

`F_OK=0` is deliberate. The first version organizes provenance without inventing completion.

Query all unresolved nodes:

```bash
python3 scripts/query_provenance_topology.py --token-vazio
```

Traverse dependencies from FG-006:

```bash
python3 scripts/query_provenance_topology.py --id FG006_CHAIN_CUSTODY --traverse out --depth 4
```

Inspect future plans without conflating them with execution:

```bash
python3 scripts/query_provenance_topology.py --time FUTURE_PLANNED
```

## 9. Repository placement invariant

- `Mapa`: canonical cross-repository semantic/provenance graph, schemas, decisions and index.
- implementation repositories: runtime-specific code, build/test receipts and exact commit identities.
- Google Drive: source/editorial memory, provider IDs, frozen exports and human-review snapshots.
- receipts: immutable evidence of an observed execution, never a forecast.

A repository-specific fact should be linked into `Mapa`; it should not be copied as if `Mapa` were the execution origin.

## R3

`F_ok`: topology contract + validator + query CLI + anchored seed graph.  
`F_gap`: exact bytes/commit/replay/full inventory.  
`F_next`: bind identities → append runs → append receipts → traverse graph → only then promote gates.
