# RAFAELIA — Workflow Orthogonal Gap-Fill — conversations-018..027 — 2026-08-14

State: `VERIFIED_LIMITED_SNAPSHOT / CLAIM_ALLOWED=false`

## Purpose

Materialize the delta obtained after moving retrieval from a linear-only descent to an orthogonal, bounded workflow. The workflow/layout changes **method selection**, not evidence status.

Canonical lane:

`source -> identity -> manifest -> physical listing -> derived source_pointer -> custody -> producer -> receipt -> claim gate -> append-only memory`

Knowledge Hypervisor retrieval topology used as control strategy:

`ROOT Ω -> Mount Table -> Identity Table -> Semantic Graph -> Skill Graph -> Evidence Graph -> Active Working Set -> Append-only Δ`

## Source authority

MB1763 parsed manifest source:

- `source_id`: `13xMqjbn1O5nc1Q3gC3ZjnUdLLW5qneWk`
- `source_name`: `export_manifest.json`
- `source_sha256`: `38bb97724a432420328a322eb27ff1af9de28201c2857448e62d2b2e3a36df4a`
- `source_bytes`: `3812404`
- `stage1_microbatch`: `MB1763`
- `parent_id`: `1P7hJq5R4fgYGEQIVNgRvllAad2lGxWEv`

The normalized manifest reports `conversations.json` as 51 shards (`conversations-000.json..conversations-050.json`), with zero broken references and zero shard-count mismatches in that manifest snapshot. This does not by itself prove independent physical-provider identity for each shard.

## Exact export records recovered

| shard | ordinal | span pointer | size_bytes |
|---|---:|---|---:|
| conversations-018.json | 42 | `$.export_files[42]` | 12115336 |
| conversations-019.json | 43 | `$.export_files[43]` | 16440670 |
| conversations-020.json | 44 | `$.export_files[44]` | 13424077 |
| conversations-021.json | 45 | `$.export_files[45]` | 21426196 |
| conversations-022.json | 46 | `$.export_files[46]` | 20765905 |
| conversations-023.json | 47 | `$.export_files[47]` | 22099004 |
| conversations-024.json | 48 | `$.export_files[48]` | 17872078 |
| conversations-025.json | 49 | `$.export_files[49]` | 16086399 |
| conversations-026.json | 50 | `$.export_files[50]` | 12815159 |
| conversations-027.json | 51 | `$.export_files[51]` | 4098254 |

A separate filesystem listing artifact, `temp.locate.txt` (`Drive provider 18Hv8UOPL70HFMXHviW7vHFxPhOoSz7bM`), exposes the same ten names and sizes. This is classified as `CORROBORATIVE_SAME_SNAPSHOT`, not independent replication.

## Derived pair-00008 probe

Canonical providers observed:

- `MESSAGES-00008.jsonl.txt`: `1RjabBaCrdT91oagJ-ujsDzXzEJgXpSuw`
- `NODES-00008.jsonl.txt`: `1IFm0viIS3Pt0WWDjkYNQOQa65xgitStW`

Readable bounded records expose `source_path=conversations-006.json` with explicit `source_pointer`. No positive `source_path=conversations-018.json` was observed in this bounded pair probe. This is not a whole-file or global absence claim. Output suffix `00008` is not treated as source-shard identity.

## Custody anchor

`conversations_chunk_01.json`:

- Drive ID: `1IS-XFlcorZsDag9HtXO4tZyA4DquvYOc`
- bytes: `94371840`
- SHA-256: `72886416eb73cb4bb8fb5beabe828f9e0582995296e1111393043cc6fa19ada3`
- state: `TOKEN_VAZIO_REASSEMBLY_REQUIRED`

This is a custody anchor only; no alias equivalence with `conversations-018..027` is asserted.

## Gate delta

- `MANIFEST_LOGICAL_EXISTENCE_018_027 = SUPPORTED_LIMITED_SNAPSHOT`
- `PATH_ORDINAL_SPAN_018_027 = SUPPORTED`
- `EXPECTED_SIZE_018_027 = SUPPORTED_LIMITED_SNAPSHOT`
- `SIZE_CROSS_REPRESENTATION_COHERENCE = PASS_LIMITED_SAME_SNAPSHOT`
- `PER_SHARD_PROVIDER_ID = TOKEN_VAZIO`
- `PER_SHARD_SHA256 = TOKEN_VAZIO`
- `PER_SHARD_CANONICAL_RECEIPT = TOKEN_VAZIO`
- `PRODUCER_TO_DERIVED_MESSAGES_nodes_BINDING = TOKEN_VAZIO`
- `claim_allowed=false`

## Anti-regression invariants

- manifest membership != physical provider identity
- same path and size != same bytes
- same snapshot corroboration != independent reproduction
- output partition suffix != source shard identity
- negative provider-name search != global absence
- workflow/layout capability != evidence
- memory/index/symbol != proof

## F_ok / F_gap / F_next

**F_ok:** ten target shards now have exact manifest ordinal, JSON span pointer and expected size; filesystem listing corroborates path/size; pair-00008 provenance was bounded without false exclusivity.

**F_gap:** per-shard Drive provider ID, per-shard SHA-256, canonical receipt and producer binding remain unresolved.

**F_next:** query Stage1 custody/checkpoints and object maps using the exact tuple `(path, size, ordinal, span_pointer)`. Stop on the first authoritative record carrying `provider_id` or per-shard SHA-256, then backtrace `provider -> bytes -> SHA-256 -> producer -> receipt -> derived MESSAGES/NODES`. Only if this route remains negative, resume pair-00007..00001 source-path descent.

`CLAIM_ALLOWED=false`
