# RAFAELIA — Cross-Tech Evidence Closure Contract V1

## Purpose

This layer closes a structural gap between **urgent-memory** and executable evidence.
The existing urgent queue already requires a `closure_contract` and a receipt, but a
cross-domain closure still needs to preserve the fact that:

```text
source != build != test != CI != runtime != device != security != provenance != reproducibility
```

No PASS is inherited between those axes.

## Core invariant

```text
TOKEN_VAZIO is a typed state, never numeric zero and never implicit PASS.
A gap closes only on its declared required_axes.
```

The evidence vector is:

```text
<CODE, BUILD, RUNTIME, TEST, CI, DEVICE, SECURITY, PROVENANCE, REPRODUCIBILITY>
```

Each axis is independently one of:

```text
PASS | FAIL | BLOCKED | OBSERVED | OBSERVED_LIMITED | TOKEN_VAZIO | NOT_APPLICABLE
```

## Closure states

- `TOKEN_VAZIO`: evidence is absent and the next probe is explicit.
- `BLOCKED`: a named external/internal dependency prevents the next observation.
- `OBSERVED_LIMITED`: useful observation exists but is insufficient for closure.
- `EVIDENCED`: required evidence is substantially present but promotion is not yet complete.
- `CLOSED_PASS`: the declared closure rule is satisfied.
- `CLOSED_FAIL`: the falsifier fired or the closure rule is refuted.
- `ARCHIVED`: historical terminal record, not a truth rewrite.

`claim_allowed=true` is stricter than `CLOSED_PASS`: every required axis must be
`PASS` or `NOT_APPLICABLE`, uncertainty must be bounded/measured, and a receipt
must exist. A structural closure may therefore be `CLOSED_PASS` while keeping
`claim_allowed=false` for broader product/scientific claims.

## Append-only custody

Records are JSONL and revisioned per `closure_id`.

```text
revision 0 -> previous_record_sha256 = null
revision n -> previous_record_sha256 = SHA256(canonical revision n-1)
```

The validator requires contiguous revisions and verifies the hash chain. Historical
mutation breaks the chain. Reopening a `CLOSED_PASS` is allowed only when the new
record explicitly cites new/refuting/contradictory evidence; this preserves
falsifiability instead of freezing a false success.

## Contradictions and dependencies

A `CLOSED_PASS` record cannot contain:

- an unresolved required evidence axis;
- an unresolved dependency;
- an open contradiction;
- unbounded/TOKEN_VAZIO uncertainty;
- a missing receipt.

This makes contradiction preservation part of the data model rather than a note.

## Public/private provenance boundary

Public projection may carry sanitized Drive references, but it must not embed
private Google Drive URLs. Provenance may be commit-pinned, byte-hashed, parsed,
observed, source-reported, or receipt-backed. Missing evidence remains explicit.

## Cross-technique network

The contract is intended to join techniques without collapsing their semantics:

1. **Source/Compiler** — static contracts, ABI, parser and source-gap scans.
2. **Build/Supply Chain** — reproducible build inputs, artifact hashes, SBOM/receipts.
3. **CI/Operations** — executable workflow status and failure semantics.
4. **Runtime/Device** — actual process execution, ABI, Android/Bionic/Termux evidence.
5. **Security** — credential boundaries, tamper detection, threat-specific gates.
6. **Scientific/Falsifiability** — equations, datasets, uncertainty, counterexamples.
7. **Memory/Knowledge Graph** — ordinal/longitudinal/urgent references and provenance.
8. **Metrology/Benchmarking** — clocks, environment, sample design, uncertainty.
9. **Reproducibility** — independent rerun/device/environment agreement.

A record can require only the axes appropriate to its claim, but `PROVENANCE` is
always mandatory.

## Seeded closures

The initial public-safe ledger contains four closures:

- the new Mapa structural evidence-closure contract itself (`CLOSED_PASS` only for
  the structural scope, backed by a reference-container receipt);
- RafGitTools source-gap audit execution (`BLOCKED` until executable target-checkout evidence);
- RAFCODEPHI V1.1 hosted CI execution (`BLOCKED` while the cited job has no executed steps);
- RAFCODEPHI V1.1 physical Android proof (`TOKEN_VAZIO`, explicitly dependent on
  its upstream executable build/CI path and later physical receipts).

These records do not copy private corpus content and do not promote device/scientific claims.

## Deterministic commands

```bash
python3 -m json.tool schemas/evidence-closure-record.v1.schema.json >/dev/null
python3 tools/validate_evidence_closure.py data/governance/evidence-closure.public.v1.jsonl
python3 -m unittest -v tests.test_evidence_closure
```

Expected local/reference result at bootstrap:

```text
ledger validation: PASS
unit tests: 9/9 PASS
claim_allowed_true_latest: 0
```

## Anti-regression rules

1. Existing urgent-memory V1 is not modified or reinterpreted.
2. No TOKEN_VAZIO becomes zero.
3. No CI PASS becomes device PASS.
4. No build PASS becomes runtime PASS.
5. No structural PASS becomes scientific validation.
6. No single execution becomes independent reproducibility.
7. A historical record is never silently overwritten; revision hashes expose mutation.
8. New evidence may refute an earlier PASS, but the reopening reason must be explicit.

## F_ok / F_gap / F_next

**F_ok** — structural cross-tech closure is now executable, append-only, hash-linked,
adversarially tested, and seeded with current typed gaps.

**F_gap** — hosted GitHub CI and physical Android evidence remain independent and
cannot be manufactured from source-state observations.

**F_next** — execute the exact gates on available runners/devices, append new revisions
with receipt hashes, and close only the axes whose evidence was actually observed.
