# RAFAELIA — Calculation Memory E0 Exact Δ — 2026-08-22

**State:** `E0_PASS_BOUNDED / DIGEST_LEDGER_REVALIDATED / APPEND_ONLY / claim_allowed=false`

## Authority

- revalidation receipt: `data/reconciliation/OMEGA_FORMULA_DIGEST_REVALIDATION_E0_S01_S05_20260822.v1.json`
- Drive calculation-memory spreadsheet: `1HDaHo5IBj42rr-iyxftG1zfaEzzCI9xC4s_0W_-1vR8`
- full correction ledger: `DIGEST_REVALIDATION`
- exact summary/readback: `E0_EXACT`

## Why this delta exists

Before exact cross-shard deduplication, each historical stored digest was required to reproduce from the stored `normalized_expression` under its declared normalization contract:

```text
SHA256(Unicode NFC(trim(normalized_expression)))
```

The gate correctly detected that the historical expression content could remain intact while the stored hash ledger was inconsistent.

## Digest revalidation result

| Shard | Records | Stored hash matches | Mismatches | State |
|---|---:|---:|---:|---|
| S01 | 22 | 22 | 0 | PASS |
| S02 | 38 | 1 | 37 | corrected by append-only ledger |
| S03 | 47 | 0 | 47 | corrected by append-only ledger |
| total | 107 | 23 | 84 | revalidated |

No source expression was modified. The old receipts are retained as historical execution artifacts; the corrected ledger is a new layer.

Example:

```text
normalized_expression = |m|=42
stored S02 sha256      = ddfba245af3b34bd95b52f3f828937b4d75179c0d4cf395bc9a3ae795863c45a
recomputed NFC+trim    = 9be21e29103564ee443072d0ac37b95bf7b338e68812aeb53ed5e7d57f540682
```

## E0 exact bounded result

With S01–S03 re-hashed and S04/S05 using their current NFC+trim identities:

```text
RAW_OCCURRENCES_S01_S05          = 374
E0_EXACT_UNIQUE_SHA256_BOUNDED   = 356
E0_DUPLICATE_EXTRA_OCCURRENCES   = 18
FROZEN_SCAN_REMAINING_PATHS      = 0
```

The exact bounded denominator is therefore **356 textual identities** within the frozen 49-path source scan.

This is not a global formula total:

```text
FORMULA_REGISTRY_GLOBAL_UNIQUE_TOTAL = TOKEN_VAZIO
E1_EXACT_AST                         = TOKEN_VAZIO
E2_ALGEBRAIC_EQUIVALENCE             = TOKEN_VAZIO
SEMANTIC_DEDUP_GLOBAL                = TOKEN_VAZIO
claim_allowed                         = false
```

## Identity ladder boundary

```text
E0 = SHA256(NFC(trim(expression))) identity
E1 = canonical AST identity after safe parsing
E2 = proved algebraic equivalence in compatible typed domain
```

No E0 collision or duplicate implies E1/E2 equivalence beyond exact text. Conversely, mathematically equivalent formulas with different notation remain distinct at E0 by design.

## Route

```text
E0 PASS (356/374)
→ define parser grammar
→ E1 AST + typed parse failures
→ E2 algebraic equivalence only on compatible AST/domain
→ domain / units / assumptions
→ D / Δ / ∇ / J / H
→ antiderivative / inverse / preimage / reverse
→ MCM append
```

## R3

**F_ok:** S01–S03 digest integrity is fully revalidated append-only and E0 exact bounded is now materialized: `374 → 356`, with 18 duplicate extra occurrences.  
**F_gap:** E1 AST, E2 algebraic equivalence, global universe total and complete calculation overlay remain unpromoted.  
**F_next:** implement/execute deterministic E1 parsing with explicit parse failures before any algebraic merge.
