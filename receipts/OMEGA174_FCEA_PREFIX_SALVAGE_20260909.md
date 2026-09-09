# Ω174 — FCEA truncated snapshot prefix salvage boundary

- cycle: `OMEGA-FED-20260909-174`
- predecessor: Ω173 / Mapa PR #570 (`034effe17347167bb8cfaae1c25c7a26a51206e1`)
- mode: `APPEND_ONLY / FAIL_CLOSED / NO_MERGE`
- claim_allowed: `false`
- COMPLETE: `NO`
- ∅: `NO`

## Source

- Drive `FCEA_CORE/SNAPSHOTS`: `1r6D5lKLhnoCdP5GjyASzyd9i8RW-2VFp`
- `snapshot_20250622011551.tar.gz`: `1nnBPptuTkjz8iP80uEwhD0_ef6v69jDu`
- compressed bytes: `6766592`
- Ω167 already proved this fileId is a third provider reference for the same logical corrupt payload; Ω174 does **not** treat it as independent recovery.
- Ω171 recovered Git HEAD tree: `.github`, `.gitignore`, `README.md`, `antiderivada_hardcore.json`, `pylint_analysis.json`.

## Measured evidence

```text
sha256=292718b82d5440910af9f470a8361cc9f51eec64bb4f41a77ab933321cd98e52
sha512=73509889d5f2e58a31bb154d435253dd9aa7d1f7747e632b565bb9279e86e7370b482665dcb8c80b8e986c9cc660b802674aab55038327ba1a9d2546b988ca7d
gzip_test=FAIL_UNEXPECTED_EOF
gzip_mtime_epoch=0
decompressed_prefix_bytes=22425969
valid_tar_headers=1833
complete_tar_members=1832
partial_tail_members=1
partial_tail_member=./venv/lib/python3.9/site-packages/pydantic_core/_pydantic_core.cpython-39-aarch64-linux-gnu.so
partial_tail_declared_bytes=4449320
partial_tail_available_bytes=48497
backup.bundle_hits=0
backup_supreme.bundle_hits=0
HEAD_tree_nominal_intersection=0/5
```

`gzip_mtime_epoch=0` is non-informative for corruption timing. A miss in the recoverable prefix is not evidence of absence from the original pre-truncation archive.

## Gap successors

### TV-FRIDA-FCEA-ALTERNATE-INTACT-ARCHIVE-174

- state: `CONTRADICTED_ARCHIVE_INTEGRITY | MEASURED_PARTIAL_PREFIX | TOKEN_VAZIO_SUFFIX`
- missing_field: byte-distinct intact archive or independently recoverable suffix/member set
- evidence_needed: candidate fileId + SHA256/SHA512 + gzip/tar PASS, or reproducible member/object reconstruction with provenance
- falsifier: candidate repeats known digest and FAIL_EOF, or reconstructed bytes fail checks
- next_probe: parent-cursor traversal for byte-distinct historical tarball/snapshot
- owner/authority: archive custodian/provider
- urgency: P0
- closure_gate: integrity PASS or complete reproducible reconstruction
- claim_allowed: false

### TV-FRIDA-FCEA-HISTORICAL-BUNDLE-BYTES-174

- state: `TOKEN_VAZIO_PROVIDER_OBJECT | SCOPED_PREFIX_NEGATIVE`
- missing_field: current `backup.bundle` / `backup_supreme.bundle` bytes and cryptographic equality
- evidence_needed: fileId + bytes + SHA256/SHA512 + `git bundle verify/list-heads`
- next_probe: alternate-parent/archive traversal; do not repeat known corrupt snapshot fileIds
- owner/authority: archive custodian/provider
- urgency: P0
- closure_gate: current bundle reproduced and cryptographically bound to historical identity
- claim_allowed: false

### TV-FRIDA-FCEA-CORRUPTION-TIMING-174

- state: `TOKEN_VAZIO_PROVENANCE`
- missing_field: when/how truncation entered custody
- evidence_needed: dated prior digest/integrity state or transfer/log witness
- next_probe: dated predecessor inventory/export/revision/custodian evidence
- owner/authority: archive custodian
- urgency: P1
- closure_gate: dated causal boundary reproduced independently
- claim_allowed: false

### MAPA-OMEGA173-EXACT-HEAD-STATUS-174

- state: `OBSERVED_PENDING | TOKEN_VAZIO_CHECK_RUN_MATRIX`
- source_pointer: PR #570 head `034effe17347167bb8cfaae1c25c7a26a51206e1`
- observed: combined commit status endpoint `pending`, zero classic statuses
- missing_field: complete exact-head CI/check-run disposition
- next_probe: re-read exact-head workflow/check conclusions; do not merge/approve/release
- owner/authority: GitHub provider/reviewer
- urgency: P0
- claim_allowed: false

## Cross-provider pointers

- Drive Ω174 receipt: `1nBhsbiNm2ZAk0o3glTyQ59UEFg_0cQN3V4xnLpni0QM`
- Drive ATLAS Δ174: `1rAk_dU0d0ogdUMIAS6rRv0fDNgtSVoBxJVwzgJSV_sE`
- Mapa predecessor: PR #570 open/draft at observation time

## F state

`F_ok` = member-boundary salvage census + SHA512 + scoped Git-tree intersection + live Ω173 readback.

`F_gap` = intact archive/suffix, historical bundles, corruption timing, exact-head CI matrix, authority/device gates.

`F_next` = alternate-parent archive cursor → byte-distinct candidate → hashes/integrity/full census; otherwise dated custody evidence; re-read Ω173 exact-head checks.
