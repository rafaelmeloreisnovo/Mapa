# RAFAELIA — AI Architecture Manifold Current V1

Status: `STRUCTURAL_PASS_MERGED`  
Claim gate: `false`

## Function

Bounded architecture inventory for humans and AIs. It answers where to enter, which source is authoritative, what is current versus stale, which plane routes or executes, which AI role owns a packet, what remains `TOKEN_VAZIO`, and what comes next.

Machine-readable authority: `data/manifold/ai_architecture_current_v1.json`.

## Current three-root view

1. **Drive / START HERE Ω V2.1** — documentary bootstrap, HOTSTATE and receipts.
2. **Mapa @ `56dca415e7a6a460b70fda4f59a320fe1b5198ba`** — pinned merged architecture authority; later moving-main commits are separate state.
3. **RafGitTools @ `a81f0d9ddaae532cf26e4ba23651c4704abd8fc4`** — executor/control-plane/tool-router.

Drive HOTSTATE reported Mapa `959a64d497c87bc84b35b70dc6918fe036f79147` and RafGitTools `ad4966029bd71a330a3d58fee3c642e2de56c983`. Current GitHub readback differs, so HOTSTATE is `STALE_BOUNDED_SUCCESSOR_REQUIRED`.

## Architecture

```text
Drive START HERE
    |
    v
Drive HOTSTATE ---- documentary memory / indices / receipts
    |
    v
Mapa ---------------- federated routing / authority / manifold / gaps
 |  \
 |   +----> producer repositories ----> producer-local gates
 |
 +-------> RafGitTools -------------> deterministic local execution / CI / receipts
 |
 +-------> Agent Dispatch ----------> 11 typed AI roles / 8 bounded packets
 |
 +-------> Rafaelia_Private --------> private custody / approved opaque pointers

producer + executor evidence
    |
    v
receipt / rollback / exact refs
    |
    +----> Mapa reconciliation
    +----> Drive μWRITE / HOTSTATE successor when material
```

## AI entry rule

```text
START HERE Ω V2.1
→ CURRENT_STATE Ω
→ ai_architecture_current_v1.json
→ one Practice ATLAS area
→ nearest AGENTS.md
→ <=3 source_min files
→ exact ref/path/hash
→ smallest named gate
→ evidence + rollback + receipt
→ R3
```

Do not crawl the whole corpus. Stop if SOURCE, AUTHORITY, EXECUTION_TARGET or EVIDENCE_RULE is unresolved; preserve `TOKEN_VAZIO`.

## Inventory

- Practice ATLAS areas: **12**
- Typed AI roles: **11**
- Session packets: **8**
- Architecture nodes: **9**
- Claim promotion from this document: **not allowed**

## Boundary

This snapshot is navigation and state reconciliation. It is not runtime proof, scientific validation, release proof, privacy certification, legal opinion, or independent reproduction.

## R3

**F_ok** — Drive ↔ Mapa ↔ RafGitTools architecture, ATLAS areas, agent roles and work packets are inventoried in one typed graph.

**F_gap** — Provider/server enforcement, CodeScan credentials, physical/runtime/source-specific gaps and downstream packets remain independently evidence-bound.

**F_next** — Enter through HOTSTATE V3, then route to the owning authority and smallest named gate; preserve TOKEN_VAZIO when closure evidence is absent.
