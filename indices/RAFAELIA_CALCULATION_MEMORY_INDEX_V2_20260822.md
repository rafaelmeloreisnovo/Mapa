# RAFAELIA — Calculation Memory Index Ω — V2 — 2026-08-22

**State:** `BOUNDED_SOURCE_CLOSED / E0_EXACT_PASS / E1_E2_PENDING / claim_allowed=false`  
**Predecessor:** `indices/RAFAELIA_CALCULATION_MEMORY_INDEX_V1_20260822.md`  
**Evolution rule:** V1 is preserved as the checkpoint where digest revalidation was still blocked; V2 records the resolved append-only state.

## 1. Persistent anchors

### Drive calculation memory
- document ID: `1ELvmzr2cltIayFrJmY1ZHzbWgjl6OJ2AkmBu3UoaivU`
- operational spreadsheet ID: `1HDaHo5IBj42rr-iyxftG1zfaEzzCI9xC4s_0W_-1vR8`
- relevant sheets: `SHARD04_RAW`, `SHARD05_RAW`, `DIGEST_REVALIDATION`, `E0_EXACT`, `SOURCE_COVERAGE`, `GAPS_NEXT`

### GitHub receipts
- `data/reconciliation/OMEGA_FORMULA_EXTRACTION_SHARD04_MATEMATICA_20260822.v1.json`
- `data/reconciliation/OMEGA_FORMULA_EXTRACTION_SHARD05_TEOREMAS_20260822.v1.json`
- `data/reconciliation/OMEGA_FORMULA_DIGEST_REVALIDATION_E0_S01_S05_20260822.v1.json`
- `data/reconciliation/OMEGA_FORMULA_E0_EXACT_DUPLICATE_MAP_20260822.v1.json`

### Index deltas
- `indices/RAFAELIA_CALCULATION_MEMORY_SHARD04_DELTA_20260822.md`
- `indices/RAFAELIA_CALCULATION_MEMORY_SHARD05_DELTA_20260822.md`
- `indices/RAFAELIA_CALCULATION_MEMORY_E0_EXACT_DELTA_20260822.md`

## 2. Bounded source closure

The provider-bound source scan frozen by the prior reconciliation contained 49 candidate paths / 48 unique blobs.

After SHARD04 + SHARD05:

```text
SOURCE_SCAN_CANDIDATE_PATHS                    = 49
REMAINING_CANDIDATE_PATHS_IN_FROZEN_SCAN       = 0
RAW_EXPRESSION_OCCURRENCES_S01_S05             = 374
```

This is a closure statement about the frozen scan denominator only. It is **not** an exhaustive statement about every Drive file or GitHub repository.

## 3. Material ingestion

| Layer | Paths / blobs | Occurrences | Local identity state |
|---|---:|---:|---|
| S01 | historical | 22 | hash ledger revalidated 22/22 |
| S02 | historical | 38 | old hash ledger 1/38 reproducible; corrected append-only |
| S03 | 3 formal sources | 47 | old hash ledger 0/47 reproducible; corrected append-only |
| S04 Matem-tica- | 12 / 11 | 208 | current 208/208 hashes independently reproduced; 201 local exact identities |
| S05 teoremas | 4 / 4 | 59 | current 59/59 hashes independently reproduced; 59 local exact identities |

Guarded source-count rules:

- `Paper2.md` / `Paper3.md` same blob => alias, not independent evidence.
- `350-formulas-mvps.md`: 350 editorial labels, **0** materially written formulas under the extraction rule.
- `domo-rafaelia-402-expressoes.md`: editorial range to 402, **6** materially written general/final forms.
- empty formula placeholders in `biosincronia.md` are not converted into formulas.

## 4. Digest revalidation

Rule:

```text
canonical_e0_digest = SHA256(Unicode_NFC(trim(normalized_expression)))
```

Historical revalidation result:

```text
S01: 22/22 match
S02:  1/38 match ; 37 mismatch
S03:  0/47 match ; 47 mismatch
TOTAL: 23/107 old hashes reproduced ; 84 corrected by append-only ledger
```

No historical receipt and no source expression was overwritten.

The current correction ledger is the `DIGEST_REVALIDATION` sheet and the GitHub revalidation receipt.

## 5. E0 exact identity — PASS

After the corrected S01–S03 digests and independent S04/S05 digest checks:

```text
RAW_OCCURRENCES_S01_S05             = 374
E0_EXACT_UNIQUE_SHA256_BOUNDED      = 356
E0_DUPLICATE_GROUPS                  = 16
E0_DUPLICATE_EXTRA_OCCURRENCES      = 18
```

Thus the frozen 49-path bounded corpus currently contains **356 E0 identities** under NFC+trim.

The duplicate map is materialized in:

`data/reconciliation/OMEGA_FORMULA_E0_EXACT_DUPLICATE_MAP_20260822.v1.json`

Examples of cross-shard exact identity recovered only after re-hashing include:

- `|m|=42` — S02 ↔ S05;
- `A=u` — S02 ↔ S05;
- `ρ_n=log(F_{n+1}/F_n) mod 2π` — S02 ↔ S05;
- `θ_n=arg(F_n+iF_{n-1}) mod 2π` — S02 ↔ S05;
- `ℛ(X)=sort(σ_1,…,σ_q)` — S01 ↔ S05;
- `ℛ(π·X)=ℛ(X)` — S01 ↔ S05.

## 6. What 356 means — and does not mean

```text
356 = E0 exact textual identities within frozen bounded scan
356 != E1 canonical AST identities
356 != E2 algebraic-equivalence classes
356 != global Drive/GitHub unique formula total
356 != novelty count
```

Canonical boundaries remain:

```text
E1_EXACT_AST                         = TOKEN_VAZIO
E2_ALGEBRAIC_EQUIVALENCE             = TOKEN_VAZIO
FORMULA_REGISTRY_GLOBAL_UNIQUE_TOTAL = TOKEN_VAZIO
SEMANTIC_DEDUP_GLOBAL                = TOKEN_VAZIO
claim_allowed                         = false
```

The reported historical target `593 + 60 = 653` remains an unverified target and is not reconciled into a global total by this bounded pass.

## 7. Identity/equivalence ladder

```text
E0 EXACT_TEXT          = CLOSED_BOUNDED (356)
E1 EXACT_AST           = NEXT_GATE
E2 ALGEBRAIC_EQUIV     = BLOCKED_BY_E1_AND_DOMAIN
E3 CHANGE_OF_VARIABLES = future typed relation
E4 CONJUGACY           = future typed relation
E5 ISOMORPHISM         = future typed relation
E6 NUMERICAL_NEAR      = comparison only
E7 SEMANTIC_ANALOGY    = proof weight zero
```

A useful immediate E1 example is that `q = sqrt(3)/2` and `q=√3/2` are distinct E0 strings but are candidates for the same canonical AST only if the parser safely maps radical notation to `sqrt(3)` without changing meaning.

## 8. Calculation-memory route

```text
E0 identity
→ E1 deterministic parser / canonical AST / typed parse failure
→ E2 algebraic equivalence on compatible typed domains
→ variables + domain + units + assumptions
→ derivative operator applicability
→ D / Δ / ∇ / J / H
→ antiderivative / inverse / preimage / causal reverse
→ implementation link
→ execution receipt
→ evidence / falsifier
→ claim gate
→ MCM append-only
```

No formula is forced into real differential calculus merely because it contains mathematical symbols.

## 9. R3

**F_ok:** the frozen 49-path ingestion denominator is closed; 374 expression occurrences are persisted; S01–S03 hash integrity was revalidated append-only; S04/S05 current digests were independently reproduced; E0 is closed at 356 exact identities with 16 duplicate groups / 18 duplicate extra occurrences.  

**F_gap:** E1 canonical AST, E2 algebraic equivalence, full domain/unit typing, full calculation overlay, formula→implementation→execution→evidence linkage, and global Drive/GitHub exhaustivity remain partial or `TOKEN_VAZIO`.  

**F_next:** execute conservative E1 parsing over the 356 E0 representatives with typed parser failures; only parsed/domain-compatible records may proceed to E2.
