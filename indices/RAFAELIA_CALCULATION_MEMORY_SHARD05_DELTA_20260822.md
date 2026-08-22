# RAFAELIA — Calculation Memory SHARD05 Δ — 2026-08-22

**State:** `INGESTED_VERIFIED_LIMITED / BOUNDED_SOURCE_QUEUE_CLOSED / APPEND_ONLY / claim_allowed=false`

## Authority

- source repo: `rafaelmeloreisnovo/teoremas`
- frozen tree: `f497f9bc914bdc54dad7788fd74653bbe5a681d3`
- receipt: `data/reconciliation/OMEGA_FORMULA_EXTRACTION_SHARD05_TEOREMAS_20260822.v1.json`
- Drive calculation-memory document: `1ELvmzr2cltIayFrJmY1ZHzbWgjl6OJ2AkmBu3UoaivU`
- Drive operational index: `1HDaHo5IBj42rr-iyxftG1zfaEzzCI9xC4s_0W_-1vR8`
- raw row store: sheet `SHARD05_RAW`

## Material delta

| Metric | Value |
|---|---:|
| provider-bound paths inspected | 4 |
| unique Git blobs | 4 |
| explicit/typed latent expression occurrences | 59 |
| exact SHA-256 identities inside SHARD05 | 59 |
| exact duplicate groups inside SHARD05 | 0 |
| prior bounded raw S01..S04 occurrences | 315 |
| bounded raw S01..S05 occurrences | 374 |
| remaining paths in frozen 49-path scan | 0 |

`374` is a bounded occurrence count, **not** a global unique-formula count.

```text
FORMULA_REGISTRY_GLOBAL_UNIQUE_TOTAL = TOKEN_VAZIO
SEMANTIC_DEDUP_GLOBAL                = TOKEN_VAZIO
claim_allowed                        = false
```

## Numeric-range inflation blocked

### `350-formulas-mvps.md`

The file enumerates `001..350`, but each item is a generic repeated MVP placeholder and does not materialize a mathematical expression. Therefore:

```text
source_label_count = 350
materialized_expression_count = 0
```

### `domo-rafaelia-402-expressoes.md`

The document declares editorial ranges through `402`, but materializes only block-level general forms and a final symbolic identity. This shard records 6 expressions; it does **not** infer 402 distinct formulas.

## Biosincronia boundary

`biosincronia.md` includes empty formula slots alongside concrete quantitative statements and experimental pipelines. Empty slots were excluded. Fourteen concrete relations/pipelines were stored as typed candidates, generally `HYPOTHESIS_UNVALIDATED` or `EXPERIMENTAL_PIPELINE_CANDIDATE`; no biomedical or physical claim was promoted.

## Historical-resolution boundary

`TEORIA_ATRACTOR_42.md` is retained as source history. Expressions later conditioned or refuted are stored with states such as:

- `HISTORICAL_CLAIM_LATER_CONDITIONED`
- `HISTORICAL_CLAIM_PROOF_OBLIGATION`
- `HISTORICAL_CLAIM_ECC_PROOF_BLOCKED`
- `REFUTED_BY_LATER_AUDIT`

The source occurrence remains append-only; later resolution does not rewrite it.

## Digest-integrity gate discovered during E0 start

Before running global exact cross-shard dedup, the stored SHA-256 must reproduce from the stored normalized expression under the declared rule.

A historical SHARD02 sample fails that check:

```text
normalized_expression = |m|=42
recomputed SHA256(NFC(trim(expr))) = 9be21e29103564ee443072d0ac37b95bf7b338e68812aeb53ed5e7d57f540682
stored SHARD02 sha256              = ddfba245af3b34bd95b52f3f828937b4d75179c0d4cf395bc9a3ae795863c45a
```

Therefore:

```text
DIGEST_INTEGRITY_S01_S03       = BLOCKED_REVALIDATION_REQUIRED
EXACT_CROSS_SHARD_DEDUP_S01_S05 = NOT_PROMOTED
```

This is a fail-closed result, not a regression of source content.

## Route

```text
HASH_REVALIDATION_S01_S03
→ E0 exact cross-shard S01..S05
→ E1 AST
→ E2 algebraic equivalence
→ domain/unit typing
→ D/Δ/∇/J/H operator selection
→ antiderivative / inverse / preimage / reverse selection
→ MCM append
```

## R3

**F_ok:** SHARD05 closes the four remaining provider-bound paths in the frozen 49-path scan and persists 59 rows in Drive with source/blob/span/type/state.  
**F_gap:** historical S01..S03 digest integrity requires revalidation; exact global dedup, E1/E2 and global unique total remain blocked/`TOKEN_VAZIO`.  
**F_next:** re-hash S01..S03 deterministically, then run E0 cross-shard dedup before any unique-total promotion.
