# RAFAELIA Gap Atlas — Coverage & Effective State V1

**Date:** 2026-08-10  
**State:** `GOVERNED_DRAFT`  
**claim_allowed:** `false`  

## 1. Effective composition

The historical seed is not rewritten.

```text
RAFAELIA_GAP_ATLAS_V1.json              seed = 26
+ RAFAELIA_GAP_RECORD_APPEND_V1.jsonl   append = 5
+ GAP_STATE_OVERRIDES_V1.json           state reductions
= effective records                     31
```

`tools/materialize_effective_gap_atlas.py` materializes this view while preserving
`base_state`, `effective_state` and state events.

Current controlled transition:

```text
GAP-META-INVENTORY-001
TOKEN_VAZIO -> REDUCED
```

This is a reduction only. It is not a claim that all Drive/GitHub content has been inventoried.

## 2. GitHub bounded coverage

Denominator: repositories declared in `indices/repository_authority_registry.json`.

```text
expected = 14
observed = 14
main     = 12
master   = 2
private  = 9
public   = 5
archived = 0
```

This proves accessible repository metadata for the declared authority registry only.
It does not prove account-wide repository coverage, branch/ref coverage, code quality,
CI or runtime.

## 3. Drive bounded coverage

Denominator: the seven `branch_registry` roots declared by `RAFAELIA — Master Navigation Registry V1`.

Direct level:

```text
scopes observed = 7/7
CONVERSATIONS_LONGITUDINAL direct children = 7
other six roots direct children = 0 each
```

`0` means no direct children were returned at that folder level. It does not mean
that the whole domain is semantically empty or that related files do not exist elsewhere.

### CONVERSATIONS_LONGITUDINAL level 2

The seven direct child folders were listed one level deeper. Each contains one receipt:

```text
RECEIPTS_APPEND_ONLY                  -> conversations-000 receipt
BATCH_001_007_BYTE_VERIFIED           -> 001-007 receipt
BATCH_008_012_BYTE_VERIFIED           -> 008-012 receipt
BATCH_013_017_BYTE_VERIFIED           -> 013-017 receipt
BATCH_028_032_BYTE_VERIFIED           -> 028-032 receipt
BATCH_033_037_BYTE_VERIFIED           -> 033-037 receipt
BATCH_038_040_HASH_CLOSURE            -> 038-040 receipt
```

## 4. Custody gap 018-027 — source chain confirmed

The observed receipt sequence has no routed batch for `018-027`.

The missing range is also explicit inside the receipt chain:

- receipt `013-017` sets `F_next=PROCESS_CONVERSATIONS_018_022` and states that `018..037` remain outside the canonical measurement chain;
- later receipt `038-040` sets `F_next=RESOLVE_SOURCE_PROVIDER_IDS_AND_PROCESS_CONVERSATIONS_018_027`.

Exact Drive searches performed in this cycle returned no matching canonical source/batch for:

```text
BATCH_018_022
BATCH_023_027
CONVERSATIONS-00018
CONVERSATIONS-00027
conversations-018.json..conversations-027.json inside NOVOexport
```

A broad search did locate `MESSAGES-00018.jsonl.txt`. Therefore the correct claim is
**not** "data 018-027 do not exist". The correct open gap is:

```text
GAP-CONVERSATIONS-018-027-CUSTODY-001 = TOKEN_VAZIO
```

Meaning: source-provider/receipt/index custody for 018-027 remains unresolved in the bounded route currently observed.

## 5. Additional longitudinal governance gaps federated

The canonical governance ledger was reconciled against later exact-ID searches. Four unresolved authorities were appended without rewriting the seed:

```text
GAP-CONVERSATIONS-TOKENIZER-001       P0 TOKEN_VAZIO
GAP-CONVERSATIONS-ASSET-JOIN-001      P1 TOKEN_VAZIO
GAP-DRIVE-GITHUB-PROVENANCE-001       P1 TOKEN_VAZIO
GAP-TRAINING-EVIDENCE-001              P1 NOT_MEASURED
```

Boundaries:

- char/4 token estimates are not exact tokenizer counts;
- partial graph/asset artifacts are not promoted as global join closure;
- naming similarity does not establish Drive↔GitHub commit provenance;
- training candidate/simulation is not training execution.

## 6. Specialized source adapters

`tools/rafaelia_specialized_ledger_adapter.py` supports bounded discovery modes:

- `rll-json`: RLL `records[]` style machine-readable ledgers;
- `token-kv`: `TOKEN_VAZIO_KEY=value` ledgers such as OPCORE94;
- `markdown-states`: explicit operational markers in Termux/RafGitTools/RafPolimata docs.

All adapter outputs are candidates only:

```text
ADAPTER_OUTPUT_IS_DISCOVERY_NOT_RESOLUTION
```

The source adapter registry is `data/gap-atlas/SOURCE_ADAPTER_REGISTRY_V1.json`.

## 7. CI boundary

The prior Gap Atlas and Federated Authority Registry runs failed before executable
steps and returned `BlobNotFound` for logs. That remains classified as provider/runner
unavailability, not a validator result.

The expanded workflow validates the expected composition `26 + 5 = 31` and checks that
all five appended gaps preserve non-promoted states. Until the runner executes steps,
these tests are `NOT_EXECUTED_REMOTE`, not PASS.

## 8. F_gap / F_next

```text
F_ok:
  seed 26 + append 5 = effective 31
  authority registry metadata 14/14
  Drive declared roots 7/7 direct
  conversations branch 7/7 level-2 receipts
  receipt chain confirms 018-027 is an explicit carried-forward gap
  specialized discovery adapters implemented
  meta inventory reduced

F_gap:
  conversations 018-027 source-provider/custody
  exact tokenizer/version and recount
  global asset↔conversation join
  Drive↔GitHub immutable provenance map
  training execution evidence
  arbitrary-depth Drive inventory
  all-account GitHub inventory/refs
  adapter execution against pinned cross-repo source snapshots
  provider/runner availability
  external scientific, human and physical-device authorities

F_next:
  resolve 018-027 provider IDs through NOVOexport_INDEX/receipt lineage
  fix tokenizer and recount only after corpus boundary is explicit
  materialize global asset join denominator/unmatched report
  build Drive↔GitHub provider/hash/commit mapping
  locate script+commit+receipt+output training triples
  run specialized adapters against pinned source snapshots
  enumerate broader GitHub installation with explicit pagination
  preserve every new unknown as append-only gap or explicit disposition
```
