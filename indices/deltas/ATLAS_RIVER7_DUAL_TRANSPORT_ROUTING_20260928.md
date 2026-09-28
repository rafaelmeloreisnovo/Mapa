# ATLAS — RIVER-7 Dual Transport Routing Delta — 2026-09-28

**mode:** `POINTER_ONLY / APPEND_ONLY / SOURCE_FIRST / FAIL_CLOSED`  
**claim_allowed:** `false`  
**authority:** routing/provenance only; technical truth remains in producer repositories.

## Intent

Route the RIVER-7 research line across the three producer authorities without duplicating payloads.

## Producer authorities

### Papers — synthesis / hypotheses / limits

- repository: `rafaelmeloreisnovo/papers`
- PR: `#110`
- branch: `research/river7-dual-transport-20260928`
- commit: `a0a99cce81899efa161d2787bf1519e0a7af3e25`
- artifact: `research_notes/2026-09-28_RIVER7_DUAL_TRANSPORT_RECONSTRUCTION_V1.md`
- state: `DRAFT_DEFENSAVEL`

### Matemática — formal definitions / equations / claim boundary

- repository: `rafaelmeloreisnovo/Matem-tica-`
- PR: `#56`
- branch: `research/river7-dual-transport-20260928`
- commit: `c42f4d4265e088cfa43feec2c16db2ebb0d1d45e`
- artifact: `docs/formal/RIVER7_TCP_UDP_DUALITY_RECONSTRUCTION_V1.md`
- state: `FORMALIZATION_DRAFT`

### ChipQuantum — offline simulator / receipt

- repository: `rafaelmeloreisnovo/ChipQuantum`
- PR: `#85`
- branch: `research/river7-dual-transport-20260928`
- head commit: `66281eeb870e17e53562fa33e77668d74835e522`
- artifacts:
  - `experiments/river7_dual_transport/README.md`
  - `experiments/river7_dual_transport/simulate_erasure_reconstruction.py`
  - `experiments/river7_dual_transport/receipts/RIVER7_ERASURE_SIM_RECEIPT_V1.json`
- execution state: `SIMULATION_PASS`
- physical network state: `NOT_RUN`

## Relations

```text
ART:papers:research_notes/2026-09-28_RIVER7_DUAL_TRANSPORT_RECONSTRUCTION_V1.md
  --FORMALIZED_BY-->
ART:Matem-tica-:docs/formal/RIVER7_TCP_UDP_DUALITY_RECONSTRUCTION_V1.md

ART:Matem-tica-:docs/formal/RIVER7_TCP_UDP_DUALITY_RECONSTRUCTION_V1.md
  --VALIDATED_FINITE_DOMAIN_BY-->
ART:ChipQuantum:experiments/river7_dual_transport/simulate_erasure_reconstruction.py

ART:ChipQuantum:experiments/river7_dual_transport/receipts/RIVER7_ERASURE_SIM_RECEIPT_V1.json
  --EVIDENCES-->
SIMULATION_PASS
```

## Semantic boundary

TCP and UDP are not asserted to be literal opposites.

The local analytical duality is:

```text
TCP-like -> ordered / reliable / stateful / byte-stream
UDP-like -> datagram / minimal transport guarantees / application-managed recovery
```

"Marked noise" is routed as an experimental concept for **explicit authenticated deferred evidence**.

The following are not semantic carriers in the governed production model:

```text
timing
packet loss
retransmission
TTL
fragmentation
RST
flood patterns
```

Those may be observed in controlled research, but are not encoded as hidden messages.

## Evidence

- finite offline XOR-erasure demonstrator: `SIMULATION_PASS`
- no sockets: `PASS_BY_DESIGN`
- packet I/O: `NONE`
- timing covert channel: `DISABLED`
- physical network execution: `NOT_RUN`
- GitHub CI at first observation: `QUEUED`
- scientific/physical claim: `BLOCKED`

## Gaps

- `GAP:RIVER7-FEC-GENERAL` — compare simple XOR parity against a general erasure/FEC construction.
- `GAP:RIVER7-LEAKAGE` — measure correlation / mutual information between semantic content and synthetic timing observables.
- `GAP:RIVER7-PHYSICAL` — no physical-network test authorized or executed.
- `GAP:RIVER7-PROTOCOL-WIRE` — wire format remains unpromoted until privacy/governance gates are closed.

## F_next

Run deterministic offline property tests over loss patterns and verify:

```text
SIMULATION_PASS
!=
PHYSICAL_PASS
!=
PRODUCTION_READY
```

No network deployment is implied by this delta.

## R3

`F_ok`: source/authority/routing/evidence split resolved across Papers, Matemática and ChipQuantum.  
`F_gap`: generalized FEC, leakage measurement, physical validation and production wire format remain open.  
`F_next`: property-based offline validation + CI receipt, then reassess the next reversible delta.
