# RAFAELIA — Cross-Provider Sidecar Recovery — 2026-08-14

State: `VERIFIED_LIMITED_CROSS_PROVIDER / claim_allowed=false`

## Why this delta exists

Stage1 MB1795–MB1801 had identified four RafGitTools archive `.sha256` sidecars and receipts, but Google Drive searches could not resolve their primary provider objects. The identifiers use the `file_000...` upload/File-Library identity family, so treating them as Google Drive file IDs was a provider-layer mismatch.

The broader workflow routed the same immutable logical identities to the File Library. This recovered the original sidecar text and receipt content without changing the evidence gate.

## Recovered expected archive digests

| Archive | Expected SHA-256 | Status |
|---|---|---|
| `RafGitTools-main-own-lowlevel-sdk-20260731.zip` | `656ff819e68ab43213a72541e71e9670680b2c448fa2b6e3ec64e7ee1e6976c0` | expected digest recovered |
| `RafGitTools-main-lowlevel-android-capsule-20260731.zip` | `41c7f2cbe73f8cfa9d82ffa0231c6103b002d3c22d4819b40298e525a0eab37b` | expected digest recovered |
| `RafGitTools-main-operational-hardening-20260731.zip` | `bef3512d4634181a28fce4888a99b54b2e9c483247ae32ec9ed4148ea1d917e4` | expected digest recovered |
| `RafGitTools-main-owned-elf-indexed-20260731.zip` | `13a39cb62f39d317c417deee6f623beab6a4719b604043aa52f66f446a9d5dfb` | expected digest recovered |

These are **expected digests read from the original sidecars**. They are not promoted to `PRIMARY_ARCHIVE_HASH_VERIFIED` until the corresponding ZIP bytes are independently available and re-hashed.

## Receipt boundary recovered

Four receipt families were recovered:

- `RAFSDK_LOWLEVEL_RECEIPT_2026-07-31.md`
- `LOWLEVEL_ANDROID_CAPSULE_RECEIPT_2026-07-31.md`
- `OPERATIONAL_HARDENING_RECEIPT_2026-07-31.md`
- `RAFSDK_OWNED_ELF_EXECUTION_RECEIPT_2026-07-31.md`

The receipts preserve a consistent boundary: source/host structural gates may be evidenced while Android SDK/NDK builds, APK signing/install, device smoke and remote CI remain independent `TOKEN_VAZIO` where not executed.

## Gap vector

### Closed

- four sidecar hash values previously `TOKEN_VAZIO_HASH_VALUE_NOT_READ`;
- receipt content for the four named receipt families.

### Still open

- current primary ZIP byte location for the four archives;
- recomputed SHA-256 against those primary bytes;
- `hj200225.zip` primary asset bytes/hash;
- raw provider/hash/receipts for `conversations-018..027`;
- snapshot-to-provider total map and provider enumeration terminality;
- producer batching/range rule.

## Anti-regression invariants

```text
expected_digest_recovered != archive_hash_verified
receipt_content != runtime_execution
Drive_search_miss != File_Library_absence
File_Library_search_miss != archive_absence
identity != provider_location
```

## Next cursor

`FILE_LIBRARY_PRIMARY_ARCHIVE_IDENTITY_RECOVERY_4_RAFGITTOOLS_ZIPS_THEN_PAIR00007_FALLBACK`

If the primary ZIP bytes remain inaccessible through the current interface, record `PRIMARY_BYTES_UNAVAILABLE_IN_CURRENT_INTERFACE` and resume the canonical `PAIR_00007` source-path inverted-index fallback rather than looping on exhausted provider-name searches.
