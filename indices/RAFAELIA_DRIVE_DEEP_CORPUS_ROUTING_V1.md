# RAFAELIA — Drive Deep Corpus Routing V1

Date: 2026-08-22  
State: `ROUTING_DRAFT / APPEND_ONLY / claim_allowed=false / COVERAGE_NOT_EXHAUSTIVE`

## Function

This Mapa record routes deep-corpus reconstruction. It does not duplicate Drive contents, invent coverage, or replace producer authority.

```text
legacy inventories
→ discovery
→ identity normalization
→ type-real classification
→ provenance/hash
→ namespace
→ relation
→ coverage_state
→ gap
→ next gate
```

Mother boundary:

```text
DISCOVERY != COVERAGE
filename != identity
extension_nominal != container_type
same_name_and_size != duplicate
log != physical_execution_receipt
```

## Drive anchors

### Deep checkpoint
- title: `RAFAELIA — Catalogação Profunda do Corpus — B-namespaces, Arquivos, Logs e Inventários — CHECKPOINT_DEEP_0001 — 2026-08-22`
- file_id: `1BKeUIyy4jhPHPBuM_pDrdLH-iYKKfIbAkKSw1Cua7do`
- state: `DEEP_SCAN_STARTED / COVERAGE_NOT_EXHAUSTIVE`

### Master Navigation Registry
- file_id: `1x_5x3_NdSaHtPLF9hbu8M1i0kvza_MnhtWeZycav19Y`
- relation: `INDEXES / ROUTES_TO`
- deep checkpoint appended with optimistic revision control.

## Legacy coverage sources to ingest

These are discovery/reconciliation sources, not automatic proof of current existence:

- `RAFAELIA_SCAN_ABSOLUTO.sh`
- `rafaelia_scan_report.txt`
- `listdir.txt`
- `RESULTADOSTREE.TXT`
- `resultadosmap.txt`
- `RAFAELIA_MATRIX_SCAN.md`
- `DRIVE_ANALOG_SOURCE_REGISTRY_2026-07-25`
- `INDEX__CODEX-00001.jsonl.txt`
- `CODEX-00001.jsonl.txt`
- `MESSAGES-*.jsonl.txt`
- `ASSETS-*.jsonl.txt`
- CHUNKS / NORMALIZED / RECEIPT / CHECKPOINT worker artifacts

## B namespaces — never collapse by label alone

### B_NAMESPACE_TECH_BENCH
- observed technical family: `B0–B18` / 19 blocks.
- `enterprise_probe.c`: observed scope `B0–B12`.
- examples already surfaced: B1 arena alloc/align, B4 CRC32C KAT, B8 NEON dot vs scalar, B11 dispatch pipeline, B12 p50/p95/p99 benchmark, B13 SHA-256 KAT, B14 HMAC-SHA256 KAT, B15 AES-128, B16 ChaCha20.
- full B0–B18 definition remains subject to source reconstruction.

### B_NAMESPACE_ACADEMIC_BRANCH
- observed conceptual family `B1–B15` in Drive material such as `ativar.txt`.
- B14 observed in that namespace as `Artes de Linguagens Vivas`.

### B_NAMESPACE_RUNTIME_BRIDGE
- `B7_TO_T2_BRIDGE` remains `TOKEN_VAZIO`.
- no B7 from another namespace may close this gap by label similarity.

Canonical B key:

```text
<namespace, B_id, source_id, source_revision_or_hash>
```

## Artifact/container families

```text
archives/blobs:
  zip, zipraf, tar, tar.gz, tgz, gz, 7z, rar, apk, aab, qcow2, raw, iso

extracted_or_named_trees:
  folders whose names preserve .zip/.tar.gz/etc.

text_and_dumps:
  txt, log, jsonl.txt, md, csv, checksum, manifest

execution_evidence:
  logcat, receipts, checkpoints, normalized, chunks, audit logs

coverage_sources:
  listdir, tree, resultadosmap, scan reports, custody/index dumps
```

A folder named `*.tar.gz` or `*.zip` is `EXTRACTED_TREE_OR_NAMED_FOLDER` until content/type evidence says otherwise. A `*.zip.b64.txt` object is `ENCODED_PAYLOAD` until decoded/verified; it is not a physical ZIP by filename.

## Index routes

- `artifact.index`
- `container.index`
- `hash.index`
- `path.index`
- `b_namespace.index`
- `archive.index`
- `log.index`
- `relation.index`
- `coverage.index`

Coverage states:

```text
DISCOVERED
SCANNED_METADATA
CONTENT_SAMPLED
CONTENT_INDEXED
HASH_VERIFIED
TOKEN_VAZIO
```

## Typed relations

- `INDEXES`
- `ROUTES_TO`
- `DISCOVERED_BY`
- `EXTRACTED_FROM`
- `ENCODES`
- `MEMBER_OF`
- `DUPLICATE_CANDIDATE`
- `RECEIPT_FOR`
- `HAS_GAP`
- `SUPERSEDES_SCOPE_WITHOUT_ERASING`

No decorative relation should be materialized without source identity and a boundary/next gate.

## Open gaps

- `TV-DEEP-001`: integral B-namespace inventory incomplete.
- `TV-DEEP-002`: exact counts by extension and real container type not computed.
- `TV-DEEP-003`: hash reconciliation/dedup of large TXT/JSONL incomplete.
- `TV-DEEP-004`: archive → extracted-tree lineage partial.
- `TV-DEEP-005`: real RAR/7Z coverage insufficient.
- `TV-DEEP-006`: log → execution/device/commit binding partial.
- `TV-DEEP-007`: current Drive × legacy scanner reconciliation incomplete.
- `TV-DEEP-008`: generic-name/hidden-content inventory incomplete.

An empty search result does not close any of these as `ABSENT`.

## Priority route

```text
P0 legacy_inventory_ingest
→ normalize
→ current-Drive reconciliation
→ hash/dedup candidates
→ B namespace reconstruction
→ archive/log lineage
→ uncovered-content probes
→ append-only delta
```

## Anti-regression

1. A filename hit is discovery, not full indexing.
2. A no-hit query is insufficient to assert absence.
3. `MBxxxx` and worker/checkpoint identifiers must not be parsed as `B<n>` without namespace evidence.
4. Same filename/size is `DUPLICATE_CANDIDATE`, not confirmed duplicate.
5. Historical paths from scanners remain historical until current-provider reconciliation.
6. Logs need environment/receipt binding before they prove a runtime execution.
7. All corrections and negative results remain in custody.
8. `claim_allowed=false` remains unchanged by corpus size.

## F-state

`F_ok`: deep-corpus route and B namespace separation materialized in Mapa.

`F_gap`: corpus totals, hash-level dedup, full archive lineage and full B reconstruction are not yet closed.

`F_next`: ingest legacy Drive inventory sources as structured coverage records, then reconcile against current Drive identities before opening uncovered payloads.
