# RAFAELIA — Performance Metric Observatory — V1

Date: 2026-08-12
Mode: APPEND_ONLY / EVIDENCE_FIRST / UNIT_AWARE / NO_SILENT_PROMOTION
Global state: VERIFIED_MIXED_EVIDENCE
Global claim_allowed: false

## Purpose

Broaden the Vectras/MVP evidence surface beyond the satirical shorthand `N^N` and beyond a single layer-count sweep. The observable object is any reproducible or potentially reproducible quantitative signal: time, rate, throughput, IOPS, bandwidth, cycles, jitter, cache behavior, energy, size, determinism and scaling.

The core rule is:

`number + unit != measurement receipt`.

Every metric must carry an epistemic class and a provenance pointer.

## Epistemic classes

1. `MEASURED_WITH_RECEIPT` — execution artifact with environment/build/workload identity and result evidence.
2. `HISTORICAL_RUN_OUTPUT` — concrete output preserved in conversation/log material, but missing one or more modern receipt fields.
3. `MEASUREMENT_PATH_IMPLEMENTED` — code exists to measure the metric, but no result value is promoted.
4. `DOCUMENTED_BENCHMARK_UNBOUND` — numeric benchmark table exists, but the raw run/device/build receipt has not been linked in this registry.
5. `ESTIMATE_CODE_ANALYSIS` — value/range explicitly derived from source analysis, expectation or theoretical estimate rather than measured run.
6. `OPERATIONAL_THRESHOLD` — control/gate threshold, not a performance result.
7. `TOKEN_VAZIO` — required evidence or interpretation unresolved.

## Unit ontology

The registry must recognize at least:

- time: `ns`, `ns/op`, `ns/sector`, `us`, `us/op`, `ms`, `s`
- rates: `ops/s`, `MOPS`, `GOPS`, `sectors/s`, `chunks/s`, `files/s`, `transitions/s`, `audits/s`, `IOPS`
- bandwidth: `MB/s`, `MiB/s`, `GB/s`, `Gbps`, `Mbps`
- compute: `GFLOPS`, `GOPS/W`, `cycles`, `cycles/op`, `host cycles/guest instruction`
- quality/stability: `%`, ratio, p50/p95/p99, jitter, coefficient-of-variation-derived scores
- footprint: bytes, KiB, MiB, GiB, text/data/bss size, memory usage
- integrity/reproducibility: sample count, deterministic assertions, CRC/hash/signature identities

## A. Strongest currently observed measured artifacts

### A1 — RAFAELOS/RafCoder Top-56 CI benchmark

Drive source: `benchmark_top56.md`, provider id `13ww5-v9HleRhGZ8JHiHXb253XZR8Q0E5`.
Class: `MEASURED_WITH_RECEIPT` at CI-runner scope.

Observed:
- best: `594.881 ns/sector`
- best throughput: `1,681,007.421 sectors/s`
- worst: `603.280 ns/sector`
- median: `599.707 ns/sector`
- mean: `599.265 ns/sector`
- spread ratio: `1.014119`
- timing stability score: `99.208 / 100`
- samples: `30`
- matrix cases: `6`
- deterministic snapshot assertions: `true` for all six cases
- largest iteration case: `2048`
- large/small time ratio: `2049.168`
- large/small ns/sector ratio: `1.000571`
- binary size: `16,432 bytes`
- binary SHA-256: `e473670485b752db029e39a30bb7f4816b0daae34defc7ab0a1b77b0a412f90a`
- runner: Linux x86_64 / clang / `-O2 -Wall -Wextra -Werror`

Boundary: these are runner-relative regression measurements, not universal hardware claims.

### A2 — EDGE V7 historical ARM32 MVP

Source chain: raw `conversations-047.json` -> `RAFAELIA — MVP N^N Benchmark Lattice — Historical Seeds 046–050 — V1`, Drive provider id `1XFoJOYSCdN7WzgGVvDWHbD-ZhEDT_DjqErnp1RtCV1s`.
Class: `HISTORICAL_RUN_OUTPUT`.

Configuration: ARM32, 256 KiB buffer, 72 rounds, discard low/high = 8/8.
- BASE: `1,477,804 ns`; `338.34 MB/s`
- UNROLL4: `2,052,718 ns`; `243.58 MB/s`; penalty vs base `0.389`
- UNROLL8: `2,132,431 ns`; `234.47 MB/s`; penalty vs base `0.443`
- winner: BASE

This is valuable negative evidence: unrolling variants did not improve this workload.

### A3 — CPU / memory hierarchy historical ARM32 MVP

Same historical-seed authority as A2.
Class: `HISTORICAL_RUN_OUTPUT` with supersession preserved.

Observed run family:
- detected threads: `8`
- CPU mean previous: `110.745 MOPS`
- CPU mean corrected run: `111.956 MOPS`
- memory mean previous: `1.615 GB/s`
- memory mean corrected run: `1.522 GB/s`
- prior latency values around `0.51/0.51/0.51/0.60 ns/access` are preserved as `SUPERSEDED_MEASUREMENT_CANDIDATE`
- corrected hierarchy examples: L1-ish 16 KiB `7.01 ns`; L2-ish 256 KiB `130.05 ns`; later hierarchy points around `260/267 ns` are preserved in the historical record.

### A4 — ARMv7 local throughput comparison

Drive catalog authority: `CATALOGO_MESTRE_RMR_LIVROS_ARQUIVOS_AMBIENTES`, provider id `1RQTJ50PcQEn8_u2EIEepZBjN6b5z2wJ2xI7dcfM1RtI`.
Class: `MEASURED_WITH_RECEIPT` according to catalog status `VERIFIED_LOCAL_MEASUREMENT`.

Observed on Moto E7 ARMv7:
- NEON path median: `163.450 MiB/s`
- portable path median: `132.313 MiB/s`
- ratio: `1.235`
- improvement: `+23.53%`
- repeats: `5`
- workload: `512 MiB`
- digest: PASS

Boundary: keep this as an independent throughput/integrity family; do not make it a mandatory dimension of the Vectras MVP lattice.

## B. Current Vectras measurement surface implemented in code

Pinned producer: `rafaelmeloreisnovo/Vectras-VM-Android@21ad17f89ce2bf29cb0d8c184c612d76a99a9b3d`.

### B1 — `VectraBenchmark.java`

Blob SHA: `e86c56e7f6b3680cf37e20a9f3b78ef1bf12b5e5`.
Class: `MEASUREMENT_PATH_IMPLEMENTED`.

`METRIC_COUNT = 79` with explicit categories:
- CPU single-thread metrics `0..19`
- CPU multi-thread `20..29`
- memory `30..44`
- storage `45..59`
- integrity/parity `60..69`
- emulation-specific `70..78`

Notable measurable axes include:
- integer/long/float/double arithmetic
- bitwise AND/OR/XOR/shifts/popcount
- MT throughput/contention/spinlock/CAS/barrier
- sequential/random memory, copy/fill bandwidth, L1/L2/L3/RAM latency, alloc/free, buffer pool, stride
- sequential/random storage, mmap, sync latency, append-only, truncate, seek, 4K/64K/1M I/O
- CRC32C, parity, syndrome, checksum, XOR stripe, Hamming, bit-flip detect, error correct, hash mix
- context switch, syscall overhead, memory-map, buffer copy, event dispatch, timer precision, IRQ latency, state serialization and triad consensus

The result record explicitly supports units such as `ns`, `us`, `ms`, `MB/s`, `GFLOPS`, `IOPS`.

### B2 — `PerformanceMonitor.java`

Blob SHA: `0d851fb37935c1ed003f548b1b61225c12b530c8`.
Class: `MEASUREMENT_PATH_IMPLEMENTED`.

Implemented measurements:
- VM boot duration using `elapsedRealtimeNanos()`
- input latency
- sequential disk read/write MB/s
- random 4K read/write IOPS, fixed seed, 1000 operations
- benchmark total duration
- memory usage tracking

No numeric disk result is promoted here until a raw `DiskBenchmark[...]` execution record is located and bound to device/build identity.

## C. Numeric material that must NOT be silently promoted

### C1 — `VECTRA_VM_BENCHMARKS.md`

Drive provider id: `1nR1qyB9tBbkzdeN922A8Z4kkOqH0Iyfo`.
Class: `DOCUMENTED_BENCHMARK_UNBOUND`.

The document contains many numeric tables, including:
- VM instruction throughput around `3.2M..98.7M ops/s` depending on instruction/variant
- cache patterns with `18.3..45.6 ns` and `3.2..8.7 GB/s`
- MemDrive examples around `0.48..8.45 ms` and `7.7..130.2 MB/s`
- 1000×1000 matrix results from `0.081` to `1.837 GFLOPS`
- dataset parsing near `29..32 MB/s`
- Fibonacci and phi examples in `us` and cycles

But this registry has not yet linked those tables to their raw benchmark outputs, device identity and build artifact. They remain useful retrieval candidates, not promoted measurements.

### C2 — `COMPARACAO_UPSTREAM_VS_OTIMIZADO.md`

Drive provider id: `1DMyuhCKmNii7EvAwXzxyQATuSd8ChFw9`.
Class: `ESTIMATE_CODE_ANALYSIS`.

The document explicitly declares methodology `source-code analysis + performance estimates`; therefore ranges such as:
- `3..20x`
- nanosecond operation estimates
- `0.3..12 G-ops/s`
- `500..8000 IOPS`
- `80..800 MB/s` storage ranges
must not be presented as executed benchmark results.

### C3 — `vectras_full_metrics.jsx.txt`

Drive provider id: `1-1VcxoaRP-y-_FyRIUMXdeDEevBGdH2Q`.
Class: `ESTIMATE_CODE_ANALYSIS / MIXED_DOC_TARGETS` until individual rows are rebound.

It is a rich metric inventory containing ranges for GOPS, GB/s, ns/us, jitter, TCG/VirtIO, JNI, mutex, CRC, scans, chunks/s, files/s and other paths. Its value is primarily as a discovery map for benchmark dimensions. Each row requires independent provenance classification before promotion.

### C4 — expected device-class IOPS

`PERFORMANCE_INTEGRITY.md`, Drive provider id `1Tacc0AYxA6H4jK1Srla9U080vJlT-5JB`, documents expected classes such as `>10,000 random-read IOPS` for high-end devices.
Class: `EXPECTED_REFERENCE_RANGE`, not a measured result.

## D. Operational thresholds are not benchmarks

`OPERATIONS.md`, Drive provider id `1NUv54bq9y7YDg8tZq-eyltFIujJ3GFsf`:
- `writeIops + readIops >= 4096` -> SATURA
- `abs(writeIops - readIops) <= 192` outside saturation -> RECOLAPSA

Class: `OPERATIONAL_THRESHOLD`.
These numbers parameterize state transitions/troubleshooting and must not be reported as achieved IOPS.

## E. The search space is a metric lattice, not only N^N

Let a configuration be:

`x = (hardware, executor, vcpu, threads, traversal, transform, buffer, memory_mode, storage_mode, access_pattern, layer_count, batch, scheduler, compiler, workload, repetitions, ...)`

and a metric vector be:

`M(x) = (ns/op, ops/s, IOPS, MB/s, GB/s, cycles/op, p50, p95, p99, jitter, cache_hit, energy, bytes, determinism, ...)`.

The raw configuration space may be combinatorial (`product k_i`; `N^N` in the symmetric special case), but the goal is not exhaustive brute force. Historical evidence forms `E0`, and exploration should choose the next configuration from evidence, constraints and novelty.

Negative, corrected and superseded measurements remain first-class evidence.

## Open gaps / TOKEN_VAZIO

- `TOKEN_VAZIO_RAW_RESULT_VECTRA_79_CURRENT_DEVICE`
- `TOKEN_VAZIO_DISK_BENCHMARK_DEVICE_RECEIPT`
- `TOKEN_VAZIO_DOCUMENTED_VECTRA_BENCH_RAW_BINDING`
- `TOKEN_VAZIO_FULL_METRICS_ROW_CLASSIFICATION`
- `TOKEN_VAZIO_048_050_RAW_METRIC_EXTRACTION`
- `TOKEN_VAZIO_METRIC_DEDUP_SAME_RUN`
- `TOKEN_VAZIO_UNIT_NORMALIZATION_SCHEMA`
- `TOKEN_VAZIO_DEVICE_BUILD_WORKLOAD_JOIN`

## Next verifiable action

Build a machine-readable `MetricObservationV1` ingest that accepts historical runs and new runs, requires `epistemic_class`, normalizes units, binds `config_id + workload_id + environment_id + artifact_hash + raw_log_hash`, and rejects promotion of estimates/thresholds into measured results.
