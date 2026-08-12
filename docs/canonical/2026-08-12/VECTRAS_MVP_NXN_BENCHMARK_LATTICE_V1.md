# RAFAELIA — Vectras / MVP N^N Benchmark Lattice — V1

Date: 2026-08-12
Mode: APPEND_ONLY / EVIDENCE_FIRST / NEGATIVE_RESULTS_PRESERVED
Global state: VERIFIED_LIMITED_HISTORICAL
Global claim_allowed: false

## 0. Correction to the earlier narrow gate

The previous controlled layer sweep `{8,64,128,760,1536}` remains useful, but it is now a **sub-test**, not the master benchmark model.

Historical conversation material already contains multiple executed MVP families and configuration comparisons. Therefore the benchmark unit is not only `layer_count`; it is an **MVP configuration vector**.

BLAKE/BLAKE3 is intentionally excluded as a benchmark axis in this lattice. Hashing may still be used for integrity/receipts.

## 1. Configuration-space model

Let an MVP configuration be:

`x = (executor_policy, traversal, transform, memory_mode, access_mode, layer_count, state_model, graph_mode, workload, buffer_size, rounds, compiler_flags, scheduler_policy, integrity_mode, ...)`

For heterogeneous dimensions `X_i` with cardinality `k_i`:

`Omega_raw = X_1 × X_2 × ... × X_m`

`|Omega_raw| = Π_i k_i`

The symmetric special case requested by the design is:

`m = N` and `|X_i| = N` for every dimension, therefore:

`|Omega_raw| = N^N = exp(N ln N)`.

Constraints/invariants prune the raw space:

`Omega_valid = { x ∈ Omega_raw : G(x) = PASS }`

so:

`|Omega_valid| <= |Omega_raw|`.

This is a **configuration-space cardinality**, not a count of physical CPU cores, simultaneous threads, or hardware lanes.

## 2. Target corpus and custody

Requested target: the five final NOVOexport conversation shards `046..050`.

Stage-1 byte authority: Google Drive document `RAFAELIA_METRICS_STAGE1_CONVERSATIONS_043_050`, provider id `1ccOoYooH-STuDvrPQQSihtg4nqpmifd7QQ8w25nIr1w`.

Target aggregate 046–050 under the canonical Stage-1 parser:

- bytes: `149,966,081`
- conversations: `454`
- messages: `25,848`
- user messages: `3,079`
- assistant messages: `22,769`
- characters: `25,628,397`
- textless messages: `16,030`

Raw content read in this evidence pass:

- `conversations-046.json`: raw read; local SHA-256 reproduced as `daef888aee856833c4f26c3c0af804826a2043c775f2d3c543d1135f27ee8e75`, equal to Stage-1.
- `conversations-047.json`: raw read; local SHA-256 reproduced as `dd133d11f02d757036eb3b9228a35e9734dc4b5984b1002f4f40c6b7260598d5`, equal to Stage-1.
- `conversations-048.json`: `TOKEN_VAZIO_RAW_CONTENT_048_CURRENT_ACCESS`; byte count/hash are known from Stage-1 but raw message content was not re-opened in this pass.
- `conversations-049.json`: `TOKEN_VAZIO_RAW_CONTENT_049_CURRENT_ACCESS`; same boundary.
- `conversations-050.json`: `TOKEN_VAZIO_RAW_CONTENT_050_CURRENT_ACCESS`; same boundary.

Therefore the historical MVP seeds below are **directly extracted from byte-matched 046/047 only**, while 048–050 remain in the target corpus but are not silently treated as content-read.

## 3. Historical executed MVP seeds

### MVP-SEED-001 — EDGE V7 adaptive selector: BASE vs UNROLL4 vs UNROLL8

Source: `conversations-047.json`
Conversation: `Diagnóstico Operacional e Tradução`
Conversation id: `6a447820-3ebc-83e9-a282-394148ecd482`
User message id: `bbb21aa7-791f-4dfa-bc49-734eb875faf7`

Observed terminal run:

- ARM32
- buffer: `256 KB`
- rounds: `72`
- discard low/high: `8/8`
- BASE trimmed average: `1,477,804 ns`, `338.34 MB/s`
- UNROLL4 trimmed average: `2,052,718 ns`, `243.58 MB/s`
- UNROLL8 trimmed average: `2,132,431 ns`, `234.47 MB/s`
- selector: `winner=BASE`
- documented penalties vs BASE: `0.389` and `0.443`
- `rollback=0`, `stuck=0`, `coherence=1.000`

Classification: `MVP_BENCHMARKED_HISTORICAL`.

Critical lesson: a more transformed/unrolled variant was slower in this configuration. Losers must remain evidence; they are pruning information for the configuration lattice.

### MVP-SEED-002 — ARM32 Benchmark v5: CPU + memory + corrected cache hierarchy

Source: `conversations-046.json`
Conversation: `Benchmark industrial ARM32`
Conversation id: `6a434132-1394-83e9-acfa-55068f9d3450`

Observed historical runs include:

- 8 detected threads, 10 CPU executions.
- one run: CPU mean `110.745 MOPS`, memory mean `1.615 GB/s`.
- an early latency implementation reported approximately `0.51 ns/access` across L1/L2/RAM levels.
- a later corrected run reported CPU mean `111.956 MOPS`, memory mean `1.522 GB/s`, and:
  - L1-ish 16 KB: `7.01 ns/access`
  - L2-ish 256 KB: `130.05 ns/access`
  - RAM-mid 4096 KB: `260.08 ns/access`
  - RAM-heavy 16384 KB: `266.81 ns/access`

Classification:

- earlier `0.51 ns/access`: `SUPERSEDED_MEASUREMENT_CANDIDATE`, not to be averaged into the corrected series.
- later cache-hierarchy run: `MVP_BENCHMARKED_HISTORICAL`.

No-regression lesson: a corrected measurement supersedes interpretation but does not erase the earlier receipt/history.

### MVP-SEED-003 — direct memory vs CPU vs indirect access

Source: `conversations-047.json`
Conversation: `Estrutura ASCII e Grafos`
Conversation id: `6a483fd5-d72c-83e9-9083-7f755876f87d`

Observed runs:

Run A:
- MEMORY mean `5604.63 ns`, median `5615 ns`, min `5538`, max `8385`.
- CPU mean `33403.85 ns`, median `30846 ns`, min `30769`, max `280692`.

Run B:
- MEMORY median `3384 ns`, avg `3418 ns`.
- CPU median `78154 ns`, avg `80636 ns`.
- INDIRECT median `3385 ns`, avg `3469 ns`.

Classification: `MVP_BENCHMARKED_HISTORICAL`.

This supplies at least one real `access_mode` dimension: `{direct-memory, cpu-work, indirect}`.

### MVP-SEED-004 — 8×8 parity/state matrix timing

Source: `conversations-047.json`
Conversation: `Estrutura ASCII e Grafos`
User message id: `bbb21dc8-6272-468c-97f1-177078670198`

Observed terminal output includes an 8×8 state matrix evolution and:

`TOTAL TIME: 1.642 ms`

Classification: `MVP_EXECUTED_HISTORICAL`.

The exact workload semantics and repetition policy are not fully reconstructed here, so performance comparison remains blocked beyond the observed run.

### MVP-SEED-005 — complex-state / toroidal simulation family

Source: `conversations-047.json`
Conversation: `Diagnóstico Operacional e Tradução`

Observed executions:

`rafael_complex`:
- seed `3487639414`
- final-window `Htotal_mean_window=5.915541`
- `Htotal_var_window=0.000015`
- program output classified a low-variance final-window attractor.

`toroidal`:
- initial energy `104.011673`
- final energy `44.801323`
- final conflicts `52`
- final linking `-1.610164`

Classification: `MVP_EXECUTED_SIMULATION_HISTORICAL`.

These are simulation outputs, not hardware-equivalence or physical-science proof.

### MVP-SEED-006 — HPC_OMEGA spectral/clustering alternatives

Source: `conversations-047.json`
Conversation: `Script monolito sh`

Observed run:
- spectral values include `lambda1=1.301484`, `lambda2=1.205818`, gap `0.095666`.
- Fiedler-sign modularity `Q=-0.0536`.
- K-means 1D modularity `Q=-0.0001`.
- reported best modularity: K-means `-0.0001`.

The same output contains a null model with `mu=0`, `sigma=0` and an enormous derived Z value. That Z is classified here as `SUSPECT_METRIC_NULL_MODEL_DEGENERATE / claim_allowed=false`, because division/normalization around zero variance requires separate validation.

Classification of the executable comparison itself: `MVP_EXECUTED_HISTORICAL`; statistical-strength claim remains blocked.

## 4. Evidence-state ladder

Each lattice point must independently move through:

`MVP_DESIGN -> MVP_COMPILED -> MVP_EXECUTED -> MVP_BENCHMARKED -> MVP_REPRODUCED -> MVP_PROMOTED`

A point may also be:

`MVP_NEGATIVE_RESULT`, `MVP_SUPERSEDED_MEASUREMENT`, `MVP_INVALIDATED`, or `TOKEN_VAZIO`.

No state transition is implied merely because a neighboring configuration passed.

## 5. Search/coverage strategy

Do not brute-force `N^N` by default.

The historical executed MVP set is a seed set `E0` inside the larger configuration space. The next engine should:

1. ingest/replay historical seed points first;
2. normalize their configuration vectors and evidence states;
3. infer only observed dimensions, leaving missing dimensions as `TOKEN_VAZIO`;
4. generate a constrained coverage frontier using pairwise/factorial/adaptive subsets where appropriate;
5. prioritize configurations that maximize uncertainty reduction or falsify a current hypothesis;
6. preserve negative results and superseded measurements as pruning evidence;
7. expand the frontier only after receipts are materialized.

Conceptually:

`E_0 -> normalize -> constraints -> coverage frontier -> execute -> receipt -> selector -> feedback -> E_1`

## 6. Relation to the 8 × 760 finding

`layer_count` is only one coordinate in `x`.

The earlier `{8,64,128,760,1536}` layer sweep remains useful as a controlled slice:

`x | all coordinates fixed except layer_count`.

It must not be confused with the full MVP configuration space.

`8 executors != 760 physical cores` remains invariant.

## 7. Open tokens

P0:
- `TOKEN_VAZIO_RAW_CONTENT_048_CURRENT_ACCESS`
- `TOKEN_VAZIO_RAW_CONTENT_049_CURRENT_ACCESS`
- `TOKEN_VAZIO_RAW_CONTENT_050_CURRENT_ACCESS`
- `TOKEN_VAZIO_MVP_CONFIG_SCHEMA_COMPLETE`
- `TOKEN_VAZIO_HISTORICAL_RAW_LOG_HASHES_PER_MVP`

P1:
- `TOKEN_VAZIO_MVP_DEDUP_ACROSS_CONVERSATIONS`
- `TOKEN_VAZIO_MVP_ARTIFACT_SOURCE_HASH_BINDING`
- `TOKEN_VAZIO_MVP_REPLAY_CURRENT_DEVICE`
- `TOKEN_VAZIO_VALID_SPACE_CARDINALITY`
- `TOKEN_VAZIO_DIMENSION_DEPENDENCY_GRAPH`

## 8. Next verifiable gate

`HISTORICAL_MVP_REPLAY_AND_LATTICE_V1`

Minimum closure condition:

- enumerate historical executed MVPs from 046–050 when raw access is available;
- bind each MVP to conversation/message provenance;
- normalize a configuration vector;
- preserve corrected/superseded/negative results;
- replay a representative seed subset on a pinned current device/build;
- then select new lattice points rather than assuming a fixed layer sweep is sufficient.

## R3

- F_ok: raw 046/047 already prove multiple executed benchmark/MVP families and alternative selectors; N-dimensional configuration space is therefore materially better than a one-dimensional layer sweep.
- F_gap: raw 048–050 content is not re-opened in this evidence pass; full dimension inventory and valid-space cardinality remain unknown.
- F_next: complete 048–050 raw recovery, deduplicate historical MVPs, materialize `MVP_CONFIG_V1`, then replay seed points and expand the constrained N^N frontier.
