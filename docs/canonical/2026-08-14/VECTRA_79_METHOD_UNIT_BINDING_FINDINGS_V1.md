# Vectras 79 Metrics — Method/Unit Binding Findings V1

Date: 2026-08-14
State: EVIDENCED_STATIC_METHOD_LEVEL
claim_allowed: false

## Scope
Pinned producer: `rafaelmeloreisnovo/Vectras-VM-Android@21ad17f89ce2bf29cb0d8c184c612d76a99a9b3d`
Source: `app/src/main/java/com/vectras/vm/benchmark/VectraBenchmark.java`
Blob: `e86c56e7f6b3680cf37e20a9f3b78ef1bf12b5e5`

All 79 metric slots now have a statically observed producer method, formatter and declared unit label in `data/benchmarks/vectra-79-metric-binding.v2.json`. Runtime values remain `TOKEN_VAZIO`.

## High-priority findings

1. **Raw/format/unit are distinct layers.** `rawValue` is elapsed nanoseconds; `formattedValue` applies dynamic SI prefixes; `unit` is a separately hardcoded label. Ingestion must preserve all three and detect disagreement.
2. **Generic formatter vs semantic IOPS.** Storage IOPS slots use `formatOpsPerSec`, which can emit `Kops/s`, `Mops/s` or `Gops/s`, while the declared semantic label is `IOPS`. IOPS must not be flattened to generic ops/s.
3. **Proxy/reused producers exist.** Several named metrics reuse methods for another operation. Examples include integer modulo via division; long add/mul/div via integer methods; float mul/div via float-add; double add/div via double-mul; multiple MT slots via the same integer/CAS producers.
4. **Storage labels can describe simulations/proxies.** `StorageSim` is memory-backed; `STORAGE_SYNC_LATENCY` uses timer precision rather than a measured fsync; append-only uses memory sequential write; truncate uses timer precision. `STORAGE_MMAP_*` names are backed by `RandomAccessFile` sequential I/O in the observed source, not mmap.
5. **Emulation proxies are explicit.** `EMU_IRQ_LATENCY` uses `Thread.yield()` context-switch timing; `EMU_MEMORY_MAP` uses allocation; `EMU_EVENT_DISPATCH` uses CAS; these are proxy/simulation measurements and must not be promoted as direct hardware IRQ/mmap/event measurements.
6. **XOR stripe byte-basis mismatch candidate.** `benchIntegrityXorStripe` loops over `M4` (`1024 x 4096` bytes) for `n0` iterations. `runAllBenchmarks()` calls it with `n0=1000` but formats bandwidth with `4 * 1024 * 1000` bytes. If each inner-loop byte touch is the intended byte basis, the formatter basis is smaller by factor 1024. This is a static mismatch candidate pending runtime/code-author review, not a promoted performance correction.
7. **64K labels vs producer block size.** Storage 64K read/write slots reuse sequential real-storage producers that operate with a 1 MiB buffer over a 128 MiB fixture in the observed implementation.

## No-regression rules

- metric name != producer mechanism
- declared unit label != formatted unit != raw elapsed-time unit
- proxy benchmark != direct hardware measurement
- static formula mismatch candidate != corrected benchmark until verified
- all current device values remain `TOKEN_VAZIO_VECTRA_79_CURRENT_RAW_RESULTS`

## Ingestion path

`VectraBenchmark audit JSONL/CSV -> tools/ingest_vectra_benchmark_v1.py -> vectra-79-metric-binding.v2.json -> MetricObservationV1 -> validator -> receipt -> promotion review`

The ingester never sets `claim_allowed=true`.

## F_NEXT

1. Obtain one raw VectraBenchmark JSONL/CSV run.
2. Ingest all 79 rows through the binding map.
3. Review unit conflicts and proxy flags.
4. Verify/fix XOR stripe byte basis and proxy metric naming/implementation in the producer repo.
5. Produce device/build/workload/log hashes and a runtime receipt.
