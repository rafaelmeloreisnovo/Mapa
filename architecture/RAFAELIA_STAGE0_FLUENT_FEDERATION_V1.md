# RAFAELIA Stage0 + Fluent Federation V1

State: `MATERIALIZED_FOR_REVIEW / FAIL_CLOSED`
Observed: `2026-08-25`

## Objective

Create a cross-repository route that removes unnecessary compile-time translation layers on ARM32 while preserving explicit authority boundaries.

## Federation roles

### RafPolimata — compiler producer authority

Owns:

- RAFIR/Stage0 compiler core;
- ARM32/ARM64 instruction encoders;
- direct ELF writers;
- freestanding syscall layer;
- canonical `RAFAELIA_FLUENT_EVENT/v1` MessagePack/Forward event codec;
- producer build/test receipts.

### RafGitTools — executor/orchestrator + projection consumer

Owns:

- compile request orchestration;
- event validation/ingest;
- append-only receipt custody on its execution plane;
- optional Room/SQLite read-model projection;
- projection replay and query/UI state.

It does not own a competing compiler backend.

### termux-app-rafacodephi — packaging/runtime authority

Owns:

- Android/Termux packaging of validated compiler artifacts;
- ABI-specific embedded binary path;
- on-device invocation;
- physical runtime receipts;
- packaged-file/hash evidence.

It does not claim that Android app/JNI/Gradle integration is freestanding merely because the Stage0 core is freestanding.

### Mapa — routing/governance authority

Owns:

- cross-repository identity and predecessor links;
- gates;
- TOKEN_VAZIO preservation;
- promotion decisions;
- evidence receipt index.

## Canonical planes

### Compile artifact plane

`SOURCE -> RAFIR -> TARGET ENCODER -> ARTIFACT`

Target examples:

- ARM32 -> A32 -> ELF32
- ARM64 -> A64 -> ELF64
- Android VM -> DEX
- Android package -> AXML + ZIP/APK

### Event/receipt plane

`STATE TRANSITION -> RAFAELIA_FLUENT_EVENT/v1 -> append-only bytes -> optional Fluent-compatible receiver`

### Query projection plane

`canonical events -> optional Room/SQLite/JSONL/index projection`

Invariant:

`ARTIFACT != EVENT != PROJECTION`

and:

`SQL_PROJECTION != AUTHORITY`

## Why Fluent-compatible rather than SQL-first

Compiler/runtime evidence is event-shaped and append-only. SQL-first forces a schema/storage projection into the critical path and then requires export/translation for other systems.

The federation therefore standardizes the event envelope before any database projection.

This does not make Fluent Forward a compiler IR. It is only the event transport/receipt ABI.

## Cross-system invariant

Changing the artifact target must not require changing the evidence envelope:

`TARGET_FORMAT_CHANGE => ARTIFACT_BACKEND_CHANGE`

not:

`TARGET_FORMAT_CHANGE => EVENT_SCHEMA_TRANSLATION`

## Roadmap to closure

### F0 — materialized now

- RafPolimata direct Forward/MessagePack codec V1.
- RafPolimata smoke test source.
- RafPolimata Stage0/event architecture spec.
- RafGitTools SQL/Room projection boundary spec.
- RAFCODEPHI Stage0 packaging/runtime spec.
- Mapa federation contract.

### F1 — codec verification

Compile/run codec smoke test on host and ARM32-capable environment; produce hash + stdout/stderr/exit receipt.

Gate: malformed/capacity overflow must fail closed.

### F2 — direct Stage0 artifact route

Implement bounded RAFIR/ASM -> A32 -> ELF32 using internal encoder/writer without external assembler/linker in the normal supported path.

Gate:

- ELF32/EM_ARM;
- no PT_INTERP;
- no unexpected DT_NEEDED;
- fixed/caller-owned storage;
- deterministic fixture output.

### F3 — eliminate Python from Stage0 subset

Move the bounded parser/lowering needed by Stage0 into freestanding C.

Gate: Stage0 supported subset compiles without Python.

### F4 — bootstrap closure

Build Stage1 from Stage0 and converge toward Stage2 self-host reproducibility where the supported language subset permits it.

Gate: reproducibility equality is recorded separately from authorship/license claims.

### F5 — RafGitTools ingest

Implement append-first canonical event ingest, then optional Room projection and replay.

Gate: deleting/rebuilding the projection must not destroy canonical receipts.

### F6 — RAFCODEPHI ARM32 runtime

Bind a validated Stage0 ARM32 binary into a non-release/internal packaging track, execute on physical ARM32, record source/binary/APK/runtime hashes.

Gate: no release promotion with TOKEN_VAZIO in producer identity/build/runtime evidence.

### F7 — multi-artifact expansion

Reuse the same event ABI for ELF64, DEX and APK/ZIP build transitions.

Gate: no target-specific evidence schema fork unless a versioned extension is required.

### F8 — distribution/provenance convergence

Join Stage0 receipts with PR #410-style provenance tracks:

`ORIGIN -> LICENSE -> AUTHORSHIP -> BUILD -> RUNTIME -> DISTRIBUTION`

No successful freestanding build automatically promotes authorship/license/release state.

## Current truth

- ARM32 compilation is technically supported by existing RafPolimata encoder/tooling surfaces.
- Current strict native build still uses external build-plane tools for part of the route.
- Direct Forward/MessagePack event codec has been materialized but is not yet execution-evidenced.
- Room/SQLite remains useful but is a reconstructible projection, not canonical event authority.
- A validated Stage0 ARM32 binary has not yet been embedded in RAFCODEPHI.

## R3

- `F_ok`: authority split and no-SQL-critical-path architecture are materialized across producer/executor/runtime/governance repos.
- `F_gap`: executable Stage0 closure, codec execution receipt, physical ARM32 runtime, projection implementation.
- `F_next`: verify the codec, then implement the smallest RAFIR/ASM -> A32 -> ELF32 Stage0 path entirely inside RafPolimata before touching broader language support.
