# Atlas Router — current pointer

## Current federated router

```text
repository: rafaelmeloreisnovo/Mapa
path: data/control-plane/PRACTICE_ATLAS_V1.json
human route: indices/PRACTICE_ATLAS_V1.md
validator: tools/audit/validate_practice_atlas_v1.py
merged via: PR #694
merge commit: 1d297f22999dcadce08a4adafd15a4a33994b4a6
state: MERGED / claim_allowed=false
```

The Practice ATLAS is the shortest current route for:

```text
INTENT → AUTHORITY → SOURCE_MIN → EXECUTION_TARGET → EVIDENCE_RULE → GAP → NEXT
```

## Prior / complementary pointers

Drive root: `1yqrafV9KvQ2C-wz8nDCrYeVEyQo_TdQZ`  
Historical Mapa router PR: `#377`  
Private memory pointer: `rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE#48`  
Compact command retained for compatibility: `ATLAS:X`

These pointers are not deleted; they are precedent/history or complementary source routes. They no longer
replace the merged Practice ATLAS as the current short federated router.

## Evidence boundary

The merge establishes repository state, not global claim validity. PR #694 had several provider/governance
checks blocked by external/current repository configuration (stale provider snapshot, missing CodeScan
credentials, no active default-branch ruleset observed, and server-side promotion enforcement not observed).
Those conditions remain gaps; they are not converted to PASS by this pointer update.

Status: `MERGED_ROUTER / claim_allowed=false`.
