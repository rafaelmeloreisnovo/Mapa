# RAFAELIA — Prompt Route Index — 2026-08-12

Canonical navigation layer for recent prompt intents.

## Route classes
`URGENT`, `NECESSARY`, `IMPORTANT`, `LATENT`, `IGNORED`, `LEFT_BEHIND`, `SHOULD_HAVE`, `ABORTED`, `CENSORED`, `UNDERESTIMATED`, `OBVIOUS`, `INTELLIGENT`, `INTERESTING`, `DERIVED`, `ANTIDERIVED`, `REVERSE`, `INVERSE`, `RECURSIVE`, `INVERSION`, plus fourteen distant vectors: `CONTRAFACTUAL`, `DUAL`, `ADJOINT`, `ORTHOGONAL`, `BOUNDARY`, `NULL_SPACE`, `RESIDUAL`, `COUNTEREXAMPLE`, `BIFURCATION`, `TRANSITIVE_CLOSURE`, `MINIMAL_WITNESS`, `SENSITIVITY`, `PROVENANCE_DEBT`, `RECONSTRUCTION_INVARIANT`.

## Navigation invariant
Each prompt node should eventually expose:
`prompt_id -> session/time -> theme -> repository/file -> artifact -> execution -> evidence -> claim_gate -> hashes/provenance -> relations -> F_gap -> F_next`.

Current recoverable range: `P001..P043`. Full historical enumeration is not claimed; missing history is `TOKEN_VAZIO` until exports/indexes are scanned.

## Priority
P0: provenance/fail-closed/claim-risk.
P1: receipts, hashes, contracts, tests, missing dependencies.
P2: paper↔math↔code↔Drive↔GitHub crosslinks.
P3: latent/interesting/contrafactual/dual research routes.
P4: TOKEN_VAZIO, never silently filled.

## Reconstruction rule
Preserve enough identity, relation and route information to rebuild context without loading the entire universe. No destructive rewrite: append-only evolution, negative results retained.
