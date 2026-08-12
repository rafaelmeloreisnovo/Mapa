# RAFAELIA — Performance Metric Index — V1

Date: 2026-08-12
Mode: APPEND_ONLY

## Canonical route

`raw conversation/log/CI artifact -> metric observation -> epistemic class -> unit normalization -> config/workload/environment join -> comparison lattice -> promotion gate`

## Records

- Observatory: `docs/canonical/2026-08-12/RAFAELIA_PERFORMANCE_METRIC_OBSERVATORY_V1.md`
- Machine registry: `data/benchmarks/RAFAELIA_PERFORMANCE_METRIC_REGISTRY.v1.json`
- MVP lattice: `docs/canonical/2026-08-12/VECTRAS_MVP_NXN_BENCHMARK_LATTICE_V1.md`
- Vectras 8×760 evidence: `docs/canonical/2026-08-12/VECTRAS_8CORE_760_LAYER_EVIDENCE_DELTA_V1.md`

## High-value measured routes

1. CI Top-56: Drive `13ww5-v9HleRhGZ8JHiHXb253XZR8Q0E5`
   - ns/sector, sectors/s, stability, determinism, binary size/hash, scaling.
2. Historical ARM32 MVPs: Drive `1XFoJOYSCdN7WzgGVvDWHbD-ZhEDT_DjqErnp1RtCV1s`
   - MB/s, ns, MOPS, GB/s, negative variants, superseded measurements.
3. ARMv7 local throughput: Drive catalog `1RQTJ50PcQEn8_u2EIEepZBjN6b5z2wJ2xI7dcfM1RtI`
   - MiB/s and repeated local comparison.

## Implemented measurement surfaces

- VectraBenchmark: 79 metrics, pinned source `Vectras-VM-Android@21ad17f89ce2bf29cb0d8c184c612d76a99a9b3d`, blob `e86c56e7f6b3680cf37e20a9f3b78ef1bf12b5e5`.
- PerformanceMonitor: disk MB/s + random 4K IOPS + input latency + boot time + memory, blob `0d851fb37935c1ed003f548b1b61225c12b530c8`.

## Do not promote without rebinding

- `VECTRA_VM_BENCHMARKS.md` -> DOCUMENTED_BENCHMARK_UNBOUND.
- `COMPARACAO_UPSTREAM_VS_OTIMIZADO.md` -> ESTIMATE_CODE_ANALYSIS.
- `vectras_full_metrics.jsx.txt` -> mixed estimate/target discovery map until row-level classification.
- `PERFORMANCE_INTEGRITY.md` device-class values -> EXPECTED_REFERENCE_RANGE.
- `OPERATIONS.md` IOPS thresholds -> OPERATIONAL_THRESHOLD.

## Query aliases

`benchmark`, `metric`, `metrics`, `ns`, `micros`, `us`, `μs`, `ms`, `IOPS`, `ops/s`, `MOPS`, `GOPS`, `GFLOPS`, `MB/s`, `MiB/s`, `GB/s`, `throughput`, `latency`, `jitter`, `p50`, `p95`, `p99`, `cycles`, `cache`, `memory`, `storage`, `IRQ`, `QEMU`, `TCG`, `VirtIO`, `CPU`, `GPU`, `matrix`, `determinism`, `sectors/s`.

## Open tokens

- `TOKEN_VAZIO_RAW_RESULT_VECTRA_79_CURRENT_DEVICE`
- `TOKEN_VAZIO_DISK_BENCHMARK_DEVICE_RECEIPT`
- `TOKEN_VAZIO_DOCUMENTED_VECTRA_BENCH_RAW_BINDING`
- `TOKEN_VAZIO_FULL_METRICS_ROW_CLASSIFICATION`
- `TOKEN_VAZIO_048_050_RAW_METRIC_EXTRACTION`
- `TOKEN_VAZIO_METRIC_DEDUP_SAME_RUN`
- `TOKEN_VAZIO_UNIT_NORMALIZATION_SCHEMA`
- `TOKEN_VAZIO_DEVICE_BUILD_WORKLOAD_JOIN`

## Promotion invariant

`documented number != measured number != reproducible receipt != universal claim`.
