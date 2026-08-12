# RAFAELIA — Fibonacci Inverse/Reverse Jump Ruler — Cross-Repo Index V1

**Date:** 2026-08-12  
**State:** `GOVERNED_PARTIAL`  
**claim_allowed:** `false`  
**Rule:** index != proof; link != evidence transfer.

## Canonical routing

```text
session concept
→ Matem-tica- formal definition/verifier
→ papers research synthesis/claims
→ Mapa semantic/provenance index
→ future Termux + benchmark + literature receipts
```

## 1. Formal authority

```yaml
repo: rafaelmeloreisnovo/Matem-tica-
pr: 13
branch: audit/fibonacci-inverse-reverse-ruler-20260812
head_at_pr_open: 3ad73932b8ddde36cf54e3131d4ff9ee896404d6
formal_note: docs/formal/FIBONACCI_INVERSE_REVERSE_JUMP_RULER_V1.md
formal_note_blob: d57a14e3a3bf24863f3bddd52a67336d014f2c32
verifier: src/verify_fibonacci_inverse_reverse_ruler.py
verifier_blob: 0c561e882750dcc8ac6e3f13f8560cea819f10e5
reference_execution_sha256: 6685cf5a6baa516df87b62896a46a1a8d7cc96e87b6030e5d75cbab89fb186f7
reference_execution_state: PASS_REFERENCE
physical_termux: TOKEN_VAZIO
```

Formal kernel:

\[
F_{n+1}=F_n+F_{n-1},\qquad F_{n-1}=F_{n+1}-F_n,
\]

\[
F_{-n}=(-1)^{n+1}F_n,
\]

\[
\mathcal F^{-1}(x)=\{n:F_n=x\},
\]

\[
R_n=F_{n+3}-1,\qquad \Delta R_n=F_{n+1},
\]

\[
\mathcal R_{RAF}(n)=(F_n,F_{n+1},F_{n+3}-1).
\]

Toroidal jump/reverse:

\[
p'=(p+J_n d)\bmod N,
\qquad
p=(p'-J_n d)\bmod N.
\]

## 2. Research authority

```yaml
repo: rafaelmeloreisnovo/papers
pr: 48
branch: research/fibonacci-inverse-reverse-ruler-20260812
head_at_pr_open: 36fdb6c4bcd896c30f882324e64e7c1af193b7d8
research_note: docs/matematica_autoral/fibonacci-inverse-reverse-jump-ruler-research-note-2026-08-12.md
claims: data/claims/fibonacci_inverse_reverse_jump_ruler_claims.v1.jsonl
provenance: governance/fibonacci_inverse_reverse_ruler_provenance_2026-08-12.md
```

`papers` may contextualize and propose experiments, but it does not promote mathematical or domain claims by itself.

## 3. Relation to Formula Registry

This cross-repo object is a specialization of the 2026-08-12 session formula inventory on branch `audit/formula-registry-session-20260812` / PR #194.

The existing mother invariant remains:

```text
formula != implementation != execution != evidence != physical claim
```

Historical recurrences using `n-2`/`n-3` remain `CONFLICTING_SUPERSEDED` rather than being erased.

## 4. TOKEN_VAZIO priority queue

### P0 — physical replay

`TOKEN_VAZIO_TERMUX_PHYSICAL_REPLAY`

Required receipt:

```text
repo + commit/blob
Python version
Android/Termux environment
exact command
stdout/stderr
exit code
SHA-256
KAT results
```

### P1 — matrix optimality

`TOKEN_VAZIO_MATRIX_OPTIMALITY`

Required comparison:

```text
Fibonacci/Rafael
vs uniform
vs prime stepping
vs Gray
vs Morton/Z-order
vs Hilbert where applicable
vs seeded random
```

Metrics: coverage, collision/revisit, cycle length, target distance, compute cost, cache locality.

### P1 — literature novelty

`TOKEN_VAZIO_LITERATURE_NOVELTY`

Primary-source search was attempted in this integration but the external web search service returned HTTP 503 twice. No novelty inference is authorized from that failure.

### P2 — domain advantage

`TOKEN_VAZIO_DOMAIN_ADVANTAGE`

Only after the generic benchmark may a domain repository test AI/compression/physics/HPC effects.

## 5. Anti-regression rules

1. Negafibonacci != geometric reverse traversal.
2. Reversibility != optimality.
3. Finite KAT != universal theorem beyond the formally proved identities.
4. Matrix traversal behavior depends on shape, direction, level and mode.
5. A missing metadata field remains `TOKEN_VAZIO`; it is not guessed.
6. `claim_allowed=false` remains global for empirical/domain claims.

## 6. F_next

```text
bind final PR/commit identities
→ replay exact verifier on Termux
→ benchmark frozen shapes/seeds/baselines
→ repeat primary-source literature search
→ append receipts
→ only then consider gate promotion
```
