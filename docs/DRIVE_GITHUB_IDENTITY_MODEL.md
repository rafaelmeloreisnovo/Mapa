# GitHub ↔ Google Drive Cross-Surface Identity Model

**Version**: 1.0  
**Last Updated**: 2026-08-30  
**Status**: REFERENCE (specification document)  
**Scope**: Immutable identity anchors for Mapa, CONVERSATIONS_CHUNKS_PRIVATE, and NOVOexport inventory

---

## Core Invariant

```text
GitHub commit SHA + Drive fileId + provider hashes form IMMUTABLE ANCHOR

Rename ≠ new identity
Move ≠ new identity  
Refactor ≠ new identity

Identity persists across storage surfaces.
Only with RECEIPT does move/rename become traceable.
```

---

## Why Cross-Surface Identity Matters

The RAFAELIA ecosystem operates across two storage surfaces:

1. **GitHub**: Code, documentation, governance state (immutable commits)
2. **Google Drive**: Custody records, operational dashboards, governance receipts (fileIds stable)

A single claim (e.g., "Mapa aggregates 28 repos") requires evidence from both surfaces:

- GitHub: Commit SHA of PRODUCTO_ECOSYSTEM_REGISTRY.v1.json
- Drive: fileId of OMEGA-CYCLE receipt + governance dashboard

Without cross-surface binding, these surfaces are isolated. With binding via DRIVE_CUSTODY_RECEIPT.v1.json, we can ask: "Is the Mapa evidence on GitHub consistent with the custody records on Drive?"

---

## The Three Identity Anchors

### Anchor 1: GitHub Commit SHA

**Immutable, cryptographic, permanent history:**

```json
{
  "repository": "rafaelmeloreisnovo/Mapa",
  "main_sha": "eb9cb679d42f64da6e4e4e09abcb96848aae2a8f",
  "observed_at": "2026-08-30T00:00:00Z"
}
```

- **Immutability**: SHA cannot be faked; cryptographic guarantee
- **Permanence**: SHA points to exact commit history forever
- **Scope**: Governs all files at that commit (including PRODUCTO.json, README, data/control-plane/)

**How it breaks:**

- Force-pushing to rewrite history (extremely rare, requires explicit authorization)
- Deleting a branch (GitHub keeps deleted commits for 90 days)

**Standard practice**: Link all cross-repo claims to observed main SHA at binding time.

### Anchor 2: Google Drive fileId

**Stable unless explicitly moved, but not cryptographic:**

```json
{
  "folder_name": "NOVOexport",
  "folder_id": "1T41msBTBXITyd_NEOEKVfq2miVwqGQ1O",
  "observed_at": "2026-08-25T11:26:56.708Z"
}
```

- **Stability**: fileId does not change if file/folder is NOT moved
- **Non-cryptographic**: No guarantee that fileId content hasn't been modified
- **Authority**: Drive API can read, move, delete (but not hide history if audit is enabled)

**How it breaks:**

- Moving folder without recording receipt (identity chain breaks)
- Overwriting folder contents (fileId stays same, contents change—hard to detect)
- Deleting and recreating (new fileId)

**Standard practice**: Record receipt BEFORE and AFTER any move; verify fileId still resolves.

### Anchor 3: Provider Hash (SHA-256)

**Cryptographic, immutable, byte-level:**

```json
{
  "archive_name": "conversations-019.json",
  "provider_id": "1cDWWp9vmRfOXp3nca6le1feiPkk0-vvW",
  "sha256": "f90bfc11a9088772570c1f81503c1bedcc9bd475c5435ce809d62812ff351436",
  "bytes": 16440670,
  "observed_at": "2026-08-25T11:26:56.708Z"
}
```

- **Immutability**: If bytes change, SHA changes; byte-level guarantee
- **Permanence**: SHA cannot be forged (would require collision attack)
- **Scope**: Covers exact file contents at fetch time

**How it breaks:**

- File overwritten or truncated (SHA changes, detected immediately)
- Hash collision attack (astronomically unlikely for SHA-256)

**Standard practice**: Store all provider hashes in append-only ledger (CONVERSATIONS_CHUNKS_PRIVATE audit trail).

---

## The Cross-Surface Binding: DRIVE_CUSTODY_RECEIPT.v1.json

**Single source of truth for GitHub ↔ Drive linkage:**

```json
{
  "receipt_id": "DRIVE-CUSTODY-RECEIPT-MAPA-20260830",
  "github_anchor": {
    "repository": "rafaelmeloreisnovo/Mapa",
    "main_sha": "eb9cb679d42f64da6e4e4e09abcb96848aae2a8f",
    "refactoring_cycle": "DOCUMENTATION-CODIFICATION-20260830"
  },
  "drive_anchors": [
    {
      "anchor_type": "NOVOEXPORT_ROOT",
      "folder_id": "1T41msBTBXITyd_NEOEKVfq2miVwqGQ1O",
      "object_count": 15439,
      "last_observed": "2026-08-25T11:26:56.708Z"
    },
    {
      "anchor_type": "CONVERSATIONS_CUSTODY",
      "provider_id": "1cDWWp9vmRfOXp3nca6le1feiPkk0-vvW",
      "sha256": "f90bfc11a9088772570c1f81503c1bedcc9bd475c5435ce809d62812ff351436"
    }
  ],
  "immutability_rules": {
    "GitHub_SHA": "Immutable; points to exact commit history",
    "Drive_fileId": "Stable unless explicitly moved with receipt",
    "Provider_hash": "Immutable; identifies exact bytes"
  }
}
```

**Properties of this receipt:**

- **Append-only**: Never delete or rewrite; only add new binding records
- **Timestamped**: Each anchor includes `observed_at` (when binding was recorded)
- **Verified**: Cross-surface binding is verified during CI (GitHub SHA exists, Drive fileId resolves)
- **Immutable**: Receipt itself is committed to GitHub (SHA-protected)

---

## Reading Cross-Surface Identity

### Example: Verify Mapa PRODUCTO.json is coherent

```bash
# Read GitHub anchor
jq .github_anchor data/control-plane/DRIVE_CUSTODY_RECEIPT.v1.json
# {
#   "repository": "rafaelmeloreisnovo/Mapa",
#   "main_sha": "eb9cb679d42f64da6e4e4e09abcb96848aae2a8f",
#   ...
# }

# Verify this SHA exists on GitHub
git rev-parse eb9cb679d42f64da6e4e4e09abcb96848aae2a8f
# Output: eb9cb679d42f64da6e4e4e09abcb96848aae2a8f (matches)

# Read what files that SHA contained
git ls-tree -r eb9cb679d42f64da6e4e4e09abcb96848aae2a8f | grep PRODUCTO
# Shows PRODUCTO.json at that exact commit
```

### Example: Verify CONVERSATIONS_CHUNKS_PRIVATE custody chain

```bash
# Read provider hash from receipt
jq .conversations_chunks_integration.custody_records[0].sha256 \
  data/control-plane/DRIVE_CUSTODY_RECEIPT.v1.json
# "f90bfc11a9088772570c1f81503c1bedcc9bd475c5435ce809d62812ff351436"

# Fetch the file from Drive and verify hash
# (This requires Drive API access; done during CI)
curl -s "https://www.googleapis.com/drive/v3/files/{fileId}?alt=media" | sha256sum
# f90bfc11a9088772570c1f81503c1bedcc9bd475c5435ce809d62812ff351436  -
# (matches receipt)
```

### Example: Detect if a file was moved or renamed

```bash
# Before: receipt shows fileId=1cDWWp9vmRfOXp3nca6le1feiPkk0-vvW
# After refactoring: try to resolve fileId
# If it fails → file was deleted or moved to a new folder
# If it succeeds but contents changed (SHA differs) → file was overwritten
# If it succeeds and SHA matches → no change (safe)
```

---

## Refactoring Safely Across Surfaces

When refactoring across GitHub and Drive simultaneously (e.g., moving files, restructuring):

### Step 1: Record BEFORE State

```json
{
  "action": "PLANNED_MOVE",
  "before": {
    "github_sha": "old_sha_here",
    "drive_fileIds": ["fileId1", "fileId2"],
    "provider_hashes": ["sha256_1", "sha256_2"]
  },
  "timestamp": "2026-08-30T12:00:00Z"
}
```

### Step 2: Execute Refactoring

- Refactor GitHub branch (new README, new PRODUCTO.json, etc.)
- Move Drive files via API (preserves fileId, records move)

### Step 3: Record AFTER State

```json
{
  "action": "MOVE_COMPLETED",
  "after": {
    "github_sha": "new_sha_here",
    "drive_fileIds": ["fileId1", "fileId2"],  # same fileIds!
    "provider_hashes": ["sha256_1", "sha256_2"],  # same hashes!
    "moves_recorded": [
      {
        "fileId": "fileId1",
        "old_parent": "1T41ms...",
        "new_parent": "1T41ms...",
        "reason": "restructure NOVOexport inventory"
      }
    ]
  },
  "timestamp": "2026-08-30T13:00:00Z"
}
```

### Step 4: Verify Consistency

- GitHub SHA resolves ✓
- Drive fileIds resolve ✓
- Provider hashes match ✓
- Move receipt in custody trail ✓

---

## Failure Modes and Detection

| Failure | Symptom | Detection | Recovery |
|---------|---------|-----------|----------|
| GitHub SHA rewritten | Commit history changes | `git rev-parse` fails or returns different tree | Restore from backup; contact repo owner |
| Drive fileId lost | Folder/file deleted | `curl` to Drive API returns 404 | Restore from backup; recreate with new fileId, record successor |
| Provider hash mismatch | File overwritten | Computed SHA ≠ recorded SHA | Determine correct version; record delta; append new hash to receipt |
| Drive move not recorded | fileId stable but parent changed | `git log` shows move receipt is missing | Record receipt retroactively; link to drive API change history |

---

## Best Practices

1. **Always verify before and after**: Don't assume fileIds survive moves
2. **Record receipts immediately**: Append-only ledger is the source of truth
3. **Use immutable hashes for custody**: Provider SHA-256 is the byte-level guarantee
4. **Link GitHub commits to Drive events**: Cross-surface binding must be explicit
5. **Never silently break a link**: If a move fails or fileId dies, record TOKEN_VAZIO
6. **Default to fail-closed**: If cross-surface binding is broken, claim_allowed=false

---

## See Also

- [PRODUCTO_CODIFICATION_GUIDE.md](PRODUCTO_CODIFICATION_GUIDE.md) — How to read PRODUCTO.json
- [TOKEN_VAZIO_CATALOG.md](TOKEN_VAZIO_CATALOG.md) — Gap definitions and closure paths
- [DRIVE_CUSTODY_RECEIPT.v1.json](../data/control-plane/DRIVE_CUSTODY_RECEIPT.v1.json) — Actual bindings (Mapa ↔ Drive)
- [CONVERSATIONS_CHUNKS_PRIVATE](https://github.com/rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE) — Custody bridge repo (GitHub)
