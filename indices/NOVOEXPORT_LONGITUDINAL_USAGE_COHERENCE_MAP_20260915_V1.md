# NOVOexport — Longitudinal Usage Coherence Map V1 — 2026-09-15

State: `EVIDENCE_BOUND / APPEND_ONLY / claim_allowed=false`

## Scope

- Raw shard range observed: `000..050` = **51/51 shards**.
- Root array objects: **5,054**.
- Non-empty conversation objects: **5,052**.
- Empty placeholders: **2**, both in `conversations-035.json`.
- User messages observed: **111,367**.
- Assistant messages observed: **185,427**.
- Time range: **2025-02-12 .. 2026-08-03 UTC**.
- RAW018 byte witness reproduced: **12,115,336 bytes**; SHA-256 `3cf4783727feb5c53868af76d6e2de660e2287c2cb075180a6aad2738b10140c`; JSON parse PASS; 100 root objects; prior PID commitment EXACT_PASS.

## Method

Longitudinal recurrence is measured only on user-role text with fixed lexical families. Monthly density = matching user messages per 1,000 user messages.

Model timeline is read from assistant `metadata.model_slug`; first seen in export is not asserted as public release date.

## Invariants

`USER_INPUT != ASSISTANT_OUTPUT`  
`TEMPORAL_PRECEDENCE != CAUSAL_USE`  
`MODEL_FIRST_SEEN_IN_EXPORT != PUBLIC_RELEASE_DATE`  
`RECURRENCE != TRAINING_EVIDENCE`  
`RAW_SOURCE != DERIVED_INDEX`

## Monthly continuation

| month | user msgs | code/1k | memory/1k | image/1k | AI/models/1k | index/search/1k | vectors/1k | cosmology/1k | hash/1k | governance/evidence/1k |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025-05 | 15,443 | 188.0 | 48.8 | 43.4 | 131.4 | 49.0 | 31.0 | 16.1 | 13.1 | 2.7 |
| 2025-06 | 9,603 | 228.7 | 73.6 | 51.7 | 121.5 | 38.3 | 77.9 | 42.8 | 28.7 | 3.1 |
| 2025-07 | 9,020 | 148.1 | 48.1 | 74.4 | 87.1 | 27.7 | 70.0 | 37.6 | 25.3 | 3.2 |
| 2025-08 | 8,957 | 186.6 | 73.6 | 82.5 | 91.0 | 37.1 | 121.7 | 38.2 | 40.1 | 4.8 |
| 2025-09 | 8,372 | 127.0 | 43.4 | 94.0 | 72.3 | 27.1 | 74.1 | 28.7 | 39.1 | 5.9 |
| 2025-10 | 6,035 | 238.3 | 95.3 | 125.6 | 94.8 | 77.5 | 145.0 | 58.3 | 124.9 | 9.1 |
| 2025-11 | 4,270 | 204.0 | 93.2 | 100.0 | 114.1 | 70.7 | 133.7 | 45.4 | 88.3 | 16.6 |
| 2025-12 | 3,624 | 199.2 | 130.2 | 104.9 | 141.3 | 87.7 | 158.7 | 48.0 | 88.0 | 11.3 |
| 2026-01 | 3,623 | 153.5 | 79.5 | 67.9 | 88.3 | 52.2 | 92.2 | 12.4 | 52.7 | 12.4 |
| 2026-02 | 2,655 | 139.4 | 80.2 | 88.5 | 70.8 | 51.6 | 102.4 | 18.1 | 46.3 | 18.1 |
| 2026-03 | 1,547 | 128.0 | 82.7 | 92.4 | 106.0 | 62.7 | 111.8 | 39.4 | 33.6 | 12.3 |
| 2026-04 | 497 | 287.7 | 203.2 | 126.8 | 221.3 | 138.8 | 249.5 | 70.4 | 150.9 | 32.2 |
| 2026-05 | 1,933 | 287.6 | 155.2 | 120.5 | 157.3 | 151.6 | 181.1 | 67.3 | 115.4 | 65.7 |
| 2026-06 | 1,619 | 279.2 | 95.7 | 109.3 | 133.4 | 66.1 | 77.2 | 38.9 | 63.6 | 43.9 |
| 2026-07 | 2,008 | 314.2 | 124.5 | 102.6 | 164.8 | 127.5 | 154.9 | 59.3 | 100.1 | 76.2 |
| 2026-08* | 189 | 312.2 | 259.3 | 142.9 | 248.7 | 248.7 | 195.8 | 116.4 | 137.6 | 132.3 |

`2026-08*` is partial through 2026-08-03 UTC.

## First observed model slugs in this continuation

- 2025-05-19 — `gpt-4-1-mini`
- 2025-08-09 — `gpt-5`
- 2025-08-12 — `gpt-5-thinking`
- 2025-10-03 — `agent-mode`
- 2025-11-13 — `gpt-5-1` / `gpt-5-1-thinking`
- 2025-12-12 — `gpt-5-2` / `gpt-5-2-thinking`
- 2026-03-05 — `gpt-5-4-thinking`
- 2026-03-06 — `gpt-5-3`
- 2026-04-22 — `gpt-5-3-mini`
- 2026-05-06 — `gpt-5-5`
- 2026-05-18 — `gpt-5-5-thinking`
- 2026-07-10 — `gpt-5-6-thinking`
- 2026-07-25 — `gpt-5.6-sol-wm` / `gpt-5.6-terra-wm`
- 2026-08-02 — `gpt-5.6-luna-wm`

## First observed user-side capability terms after April 2025

- 2025-05-08 — `multimodal`
- 2025-06-30 — `vector_db`
- 2025-12-11 — `RAG`
- 2026-06-09 — `Deep Research`

## Artifact commitments

Drive-side derived artifact hashes:

- `NOVOEXPORT_LONGITUDINAL_USAGE_COHERENCE_MAP_V1.md` — SHA-256 `c706b12ee59082277c7a4faea90f615fba3be50058b4cd43f82eb4804a64ef47`
- `NOVOEXPORT_LONGITUDINAL_USAGE_COHERENCE_MAP_V1.json` — SHA-256 `2c1f4f9fc63dbc0aecef6b59a190d47acce1d0d3a249002cfb3a35b774789fb3`
- `longitudinal_monthly.csv` — SHA-256 `f4255099e870845127db073e3b98d7c34f81834a2db571c6e88130ee376dc879`
- `first_model_seen.csv` — SHA-256 `d84b9e264a3ca2c03f15e8eea8e6b57a41f5036fa0244afd69b69f3a699aafba`
- `first_specific_seen.csv` — SHA-256 `beb48ccac1d265b238d0a19b694d267e475a30e0e8c08fbc6b521f076042ced2`
- `shard_inventory.csv` — SHA-256 `233dcf249601bf81a256b7bc2993c38a4274f76e724dc73b816bf7507643227d`

## Epistemic state

Observed: recurrent user-side themes persist across months and several core families become denser in later periods.

Not proved by this corpus: that recurrent user-side themes were used to train models or caused external model/product releases.

`causal_use=TOKEN_VAZIO_EXTERNAL_CAUSAL_EDGE`
