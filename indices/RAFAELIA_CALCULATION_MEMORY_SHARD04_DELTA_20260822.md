# RAFAELIA — Calculation Memory SHARD04 Δ — 2026-08-22

**State:** `INGESTED_VERIFIED_LIMITED / APPEND_ONLY / claim_allowed=false`

## Authority

- source repo: `rafaelmeloreisnovo/Matem-tica-`
- frozen tree: `e7a90eb64e02befa2a24708dfd24faa4c2381af5`
- receipt: `data/reconciliation/OMEGA_FORMULA_EXTRACTION_SHARD04_MATEMATICA_20260822.v1.json`
- Drive calculation-memory document: `1ELvmzr2cltIayFrJmY1ZHzbWgjl6OJ2AkmBu3UoaivU`
- Drive operational index: `1HDaHo5IBj42rr-iyxftG1zfaEzzCI9xC4s_0W_-1vR8`
- raw row store: sheet `SHARD04_RAW`

## Material delta

| Metric | Value |
|---|---:|
| provider-bound paths inspected | 12 |
| unique Git blobs | 11 |
| explicit expression occurrences | 208 |
| exact SHA-256 identities after NFC+trim | 201 |
| exact duplicate groups | 6 |
| duplicate extra occurrences | 7 |
| prior raw S01+S02+S03 occurrences | 107 |
| bounded raw S01+S02+S03+S04 occurrences | 315 |

`315` is an occurrence count across bounded extraction shards, **not** a global unique formula count.

```text
FORMULA_REGISTRY_GLOBAL_UNIQUE_TOTAL = TOKEN_VAZIO
SEMANTIC_DEDUP_GLOBAL = TOKEN_VAZIO
```

## Alias rule

`Paper2.md` and `Paper3.md` resolve to the same Git blob:

`976967682b6c242c6ff36745fcbd41c628b86abc`

Expressions are extracted once and the second path is preserved as an alias, not independent evidence.

## Historical-resolution rule

SHARD04 includes both source-era expressions and later mathematical audits. Therefore:

```text
historical occurrence != current accepted resolution
```

Corrections/counterexamples are linked conceptually as `CORRECTS` / `REFUTES` / `SUPERSEDES`; the historical source is not erased.

Examples present in the audited material include distinction of first modular alignment from joint-origin return, failure of the old weighted permutation-invariance claim without explicit conditions, generalized CRT compatibility, and rejection of `28/13` as an approximation to pi.

## Remaining provider-bound source queue

Exactly four source-scan candidates remain at expression level, all in `rafaelmeloreisnovo/teoremas`:

1. `TEORIA_ATRACTOR_42.md`
2. `docs/rafaelia/350-formulas-mvps.md`
3. `docs/rafaelia/biosincronia.md`
4. `docs/rafaelia/domo-rafaelia-402-expressoes.md`

State: `TOKEN_VAZIO_EXPRESSION_LEVEL_PENDING_SHARD05`.

## Route

```text
SHARD05
→ exact cross-shard digest dedup S01..S05
→ E1 AST normalization
→ E2 algebraic equivalence
→ domain/unit typing
→ derivative / discrete-delta / finite-algebra operator selection
→ antiderivative / inverse / preimage / reverse selection
→ MCM append
```

## R3

**F_ok:** SHARD04 closes the prior 12-path Matem-tica- queue with frozen provenance, full Drive row storage and a GitHub receipt.  
**F_gap:** four `teoremas` paths remain; exact cross-shard and semantic/algebraic dedup remain open; global unique count stays `TOKEN_VAZIO`.  
**F_next:** materialize SHARD05 before any global formula-total promotion.
