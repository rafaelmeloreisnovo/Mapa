# RAFAELIA Ω177 — R2 Corpus + Custody Entry Receipt v1

Date: 2026-09-09
State: R2_ENTRY_CONTRACT_IMPLEMENTED_TESTED_LOCAL / CORPUS_POPULATION_OPEN / claim_allowed=false

## Predecessor

R1 local contracts G074/G094/G097 are merged in Mapa main through PR #583, merge commit `e19b3214d50d07023092829a2f8e94a68d7383dd`.

## Entry contract

`contracts/omega177/omega177_r2_corpus_custody_entry_v1.json`

Validator:

`tools/validate_omega177_r2_corpus_custody_entry.py`

Corpus-object schema:

`schemas/omega177_corpus_object_v1.schema.json`

Local validation:

`PASS: Ω177 R2 corpus/custody entry contract valid; global root blocked; claim_allowed=false`

## R2 scope

R2 now begins materially with four coupled but non-equivalent obligations:

1. global dedup/hash across X0/home/Drive and related snapshots;
2. canonical authority decisions for multiple snapshots;
3. formal sanitization before reusable template promotion;
4. Template Creator package construction only from sanitized supported references.

## Required per-object custody

Each object is represented by explicit provider/source identity, path/title, observed-byte state, size, SHA-256, BLAKE3, provider commit/Drive ID, object class, canonical authority + reason, duplicate/supersession relations, sensitivity/sanitization, execution/build/runtime proof class, epistemic class and TOKEN_VAZIO reason.

## Promotion rules

- `bytes observed before cryptographic root`
- hashes are not accepted for an object whose bytes were not observed;
- global root is forbidden until `input_scope_complete=true`;
- digest equality is evidence of byte identity, not canonical authority, authorship or truth;
- recency alone never establishes canonical snapshot authority;
- dedup views may collapse duplicates, but source history is not destructively deleted;
- supersession is append-only and explicit;
- template references require `PASS_SANITIZED`;
- raw runtime code remains SOURCE unless transformed into a supported, sanitized template artifact.

## Current bounded states

- `R2_ENTRY_CONTRACT=CLOSED_IMPLEMENTED_TESTED_LOCAL`
- `R2_CORPUS_POPULATION=OPEN`
- `R2_GLOBAL_ROOT=TOKEN_VAZIO_SCOPE_INCOMPLETE`
- `R2_CANONICAL_SNAPSHOTS=OPEN_AUTHORITY_BINDING`
- `R2_SANITIZATION_POPULATION=OPEN`
- `R2_TEMPLATE_PACKAGE=TOKEN_VAZIO_UNTIL_SANITIZED_REFERENCES`
- `claim_allowed=false`

## External gates unchanged

Android/ARM physical, second physical architecture, RafBit↔BitOmega semantic authority, independent external audit, G017/G018/RLL empirical validation and other external providers remain independent open gates.
