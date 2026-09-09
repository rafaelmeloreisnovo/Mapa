# Ω175 — FCEA three-root Git topology + Ω174 exact-head CI

- cycle: `OMEGA-FED-20260909-175`
- predecessor: `Ω174 / PR #571 @ 11faf36cc7760239dcb8eb39c1a1510e19334e49`
- mode: `APPEND_ONLY / BULK_FIRST / CURSOR_FIRST / FAIL_CLOSED / NO_MERGE`
- claim_allowed: `false`
- COMPLETE: `NO`
- ∅: `NO`

## Drive custody

- Ω175 receipt: `18AlPPryg0JN_Yka6wFyxfztSNb3CObDe3pvMQVkhkQU`
- ATLAS Δ175: `1BO85PvlsmZ2v4s5HcdbDSalb1Aiqq7v9Uhz-sEtMadY`

Three provider-resolved same-name roots remain distinct occurrences:

| root | FCEA_REPO | .git | objects |
|---|---|---|---|
| A | `1BtjJ9YPFL-wymQj_7wl0GqINAczGbpT2` | `1-t1sWDu2SNyMFyIi-Zm-BZ3KgkfTEXzD` | `1RZmunPJSAE4vCISDbQIC3Ul0sWxD6r-v` |
| B | `1Ur04MJSznzv13n4IYWkVz17VF7LtR3Lz` | `1DQZ_6eGHXQsb5zhXYAtodA6_ybnANR_y` | `1JOlm4mJU4cUeUsMTk0dK3p1h1j7NUt_e` |
| C | `1dRW-lvJicxD-8AMBooFal9XcObr2yMHh` | `1qq1Y7m32dRHqIdEjbd2oGM1UmnHgyZPP` | `1r94VAey-LmxUYqHVkbXVn3_WCMgzvqtX` |

Each `.git` direct traversal exposed `objects`, `refs`, `logs`, `info`, and `hooks` provider folders. Bounded object-root listings are positively non-identical: B exposes observed prefixes including `db` and `b8`; C exposes observed prefixes including `e9,e5,e2,e0,de,db`; A's returned bounded sequence begins `d3,d1,d0,ca,c1,c0,bf,bc,b7,b1,...`.

This supports only:

`NAME_EQUALITY != OBSERVED_TOPOLOGY_EQUALITY`

It does **not** establish disjoint histories or full graph non-equivalence. Provider listings are bounded; an omitted prefix is not an absence claim.

## Ω174 exact-head CI readback

Head: `11faf36cc7760239dcb8eb39c1a1510e19334e49`.

Observed workflow state:

- Provider Protection Gate: `failure`
- main-hardening-gate: `success`
- Branch Topology Gate: `success`
- Human Dignity Ethics Gate V1: `success`
- Server Merge Enforcement Assurance: `failure`
- RAFAELIA Promotion Control V1: `failure`
- CodeScan: `failure`
- SecurityCodeScan: `success`
- CI: `failure`
- CodeQL Advanced: `success`

CI detail: changed-Markdown blocking regression gate passed; `Historical Markdown debt — blocking no-increase ratchet` failed and downstream steps were skipped. Promotion-control negative fixtures and 15 invariants passed; `claim_allowed=false` validation passed; manual promotion decision failed. PR #571 had zero observed submitted reviews.

Therefore the prior `TOKEN_VAZIO_CHECK_RUN_MATRIX` is narrowed to `OBSERVED_MIXED_FAIL_CLOSED`. This is an observation closure only, never promotion authorization.

## Gap delta

### TV-FRIDA-FCEA-THREE-ROOT-GIT-EQUIVALENCE-175

- state: `OBSERVED_TOPOLOGY_DIVERGENCE | TOKEN_VAZIO_OBJECT_IDENTITY`
- source_pointer: Drive A/B/C `.git/objects` IDs above
- missing_field: complete object-ID sets, HEAD/refs/packed-refs, pack identities and graph relation
- blocking_dependency: provider traversal of `refs/heads`, `packed-refs`, `objects/pack`, then nested loose-object leaves where needed
- evidence_needed: per-root ref commit IDs + pack/idx digests/object census + set intersections + reproducible Git verification when bytes are recoverable
- falsifier: full ref/object identities demonstrate equivalence despite bounded directory-topology divergence, or observed folders are proven unrelated to the relevant Git occurrence
- next_probe: A/B/C `refs/heads|packed-refs` → A/B/C `objects/pack` → object/ref set relation → compare against Ω171 recovered commit
- owner/authority: Drive archive custodian/provider
- urgency: `P0`
- closure_gate: classify relation as `EQUIVALENT|SUPERSET|SUBSET|PARTIAL_OVERLAP|DISJOINT` with reproducible object/ref witnesses
- claim_allowed: `false`
- lineage: `Ω174→Ω175`

### MAPA-OMEGA174-EXACT-HEAD-STATUS-175

- state: `OBSERVED_MIXED_FAIL_CLOSED`
- source_pointer: Mapa PR #571 exact head
- scoped closure: exact-head workflow-state observation
- still separate: independent review, provider enforcement and promotion authority
- next_probe: no merge; preserve matrix and address execution debt separately from external authority gates
- claim_allowed: `false`

### Preserved P0 archive gaps

- `TV-FRIDA-FCEA-HISTORICAL-BUNDLE-BYTES-175 = TOKEN_VAZIO_PROVIDER_OBJECT`
- `TV-FRIDA-FCEA-ALTERNATE-INTACT-ARCHIVE-175 = CONTRADICTED_ARCHIVE_INTEGRITY | MEASURED_PARTIAL_PREFIX | TOKEN_VAZIO_SUFFIX`
- corruption timing remains `TOKEN_VAZIO_PROVENANCE`

## R3

**F_ok:** 3/3 FCEA roots were routed through `.git→objects`; positive bounded topology divergence was observed; Ω174 exact-head CI matrix was read back and retyped without false promotion; Drive receipt/Atlas/index pointers exist.

**F_gap:** complete A/B/C Git graph relation, historical bundle bytes, intact archive/suffix, corruption timing, provider enforcement/review, signer/device/runtime.

**F_next:** `refs/heads + packed-refs → objects/pack + hashes/census → graph intersections vs Ω171 → alternate bundle/archive cursor → successor receipt only on new evidence`.
