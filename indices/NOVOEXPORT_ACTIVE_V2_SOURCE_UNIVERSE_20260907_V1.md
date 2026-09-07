# NOVOexport ACTIVE_V2 — Source Universe — 2026-09-07

State: `ACTIVE_V2_PHYSICAL_UNIVERSE_BOUND_SEMANTIC_INGEST_OPEN`  
`claim_allowed=false`

## ATLAS:X → NOVO:X

The current Google Drive `NOVOexport` corpus is bound by provider identity, not copied into GitHub. Raw JSON/shard content remains source authority. GitHub stores only the evidence envelope, invariants, and deterministic validation needed to route existing ingest pipelines.

## Full physical source boundary

Observed from the complete `export_manifest.json` object (`fileId=13xMqjbn1O5nc1Q3gC3ZjnUdLLW5qneWk`):

- physical export entries: **15,439**
- logical files: **15,369**
- declared bytes: **25,132,295,924**
- `.dat`: **15,358**
- `conversations-000..050.json`: **51/51**, no missing shard number
- `codex-000..020.json`: **21/21**, no missing shard number
- other core JSON: **8**
- `chat.html`: **1**
- source object bytes SHA-256: `38bb97724a432420328a322eb27ff1af9de28201c2857448e62d2b2e3a36df4a`
- canonical sorted `path<TAB>size<LF>` SHA-256: `0c43be312e8ccb0a68ded11ee0e3c7d2454c8a2495241861df36ef4ea51b4f5f`
- Merkle root over `SHA256(path || NUL || size)`: `7f336dd32119afe1c10eb0e816fd72839cad2092e934eb19afd883a761821286`
- Merkle leaves: **15,439**

The Merkle commitment covers every declared physical entry without publishing/copying the private path list into the repository.

## L/O/T/REL/SCALE

- `L:X`: successors are append-only; predecessor indices are not rewritten.
- `O:X`: Mapa/Termux/LLaMA/GAIA/Vectras/RafPolimata/Private/MemRafcode remain independent producer authorities.
- `T:X`: Drive `fileId/source_ref/shard` pointers bridge source to implementation.
- `REL:X`: rapport/context relation has evidence weight zero until separately proved.
- `SCALE:X`: universe → logical file → shard → object → token only when evidence exists.

## EVID:X

Evidence here proves **physical manifest scope and identity envelope only**. It does not prove semantic exhaustivity, runtime behavior, scientific claims, training, or model-weight updates.

## GAP:X

Still open by design:

- `TV-INDEX-INGEST-000-050`
- `TV-MESSAGES-FULL-COVERAGE`

Thus:

`PHYSICAL_UNIVERSE_BOUND != SEMANTIC_EXHAUSTIVITY`

## Route drift

Historical `01_EXPORT_CORE_JSON` provider ID `1ILDwi_A3r_93OyMiQW-BKKOu5hVVeV74` returned `NOT_FOUND` during current readback. Replacement is `TOKEN_VAZIO`; no provider ID is inferred. Existing source files remain reachable by current provider IDs and source lineage.

## LEARN:X

The operational learning promoted by this packet is:

`DEFAULT_BRANCH_PROVIDER > BRANCH_NAME_ASSUMPTION`

and

`NOT_FOUND_ROUTE != DATA_LOSS`

This is append-only routing knowledge, **not online self-training**.
