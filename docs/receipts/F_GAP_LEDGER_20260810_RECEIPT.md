# Receipt — F_GAP Cohesion Ledger — 2026-08-10

Repository: `rafaelmeloreisnovo/Mapa`
Branch: `audit/f-gap-cohesion-20260810`
PR: `#181` (draft)
Claim gate: `claim_allowed=false`

## Written artifacts

1. `docs/governance/F_GAP_LEDGER_20260810.md`
2. `data/governance/f_gap_ledger.v1.json`
3. `schema/f_gap_ledger.v1.schema.json`
4. `scripts/validate_f_gap_ledger.py`
5. `.github/workflows/f-gap-ledger-gate.yml`

## Commit chain observed during creation

- ledger markdown: `89a7f7bc251d5d47e624c8e49916ad8f4d16b04e`
- machine ledger: `95a638ce8e6f32732a754bfd09691d5f11e29069`
- schema: `b444971855530e04799d02f8bb40085be5470d5a`
- validator: `b02f49bc34576581a08b5bd47c3ed1ed517dcfaa`
- workflow gate: `c6f562d0cbc9ea47c207d29014951bb49c94b997`

## Remote gate observation

For head `c6f562d0cbc9ea47c207d29014951bb49c94b997`:

- `F_GAP Ledger Gate`, run `31425518346`: `completed/failure`.
- job `validate`, id `93576164188`: `completed/failure`.
- GitHub returned `steps=[]`.
- decoded job log fetch returned `BlobNotFound`; no usable step/log evidence was available at observation time.
- existing `RAFAELIA Promotion Control V1`, run `31425518347`: `completed/failure`; `negative-tests` failed before exposed step summaries and `enforce` was skipped.
- `Branch Topology Gate` and generic `CI` were queued at the same observation point.

## Interpretation

`CI_FAILURE_CAUSE = TOKEN_VAZIO`.

The absence of step/log evidence does **not** authorize attributing the failure to ledger content, validator logic, runner infrastructure, permissions, branch policy, or GitHub service state. The cause remains unclassified until provider evidence exists.

## Longitudinal Drive

An append-only audit event was written to the canonical Drive document `RAFAELIA — Implementação Latentes e Papers — Drive GitHub V1.txt`, recording 36 gaps and the fail-closed invariant.

## Invariant

No gap may transition to `CLOSED` without evidence + provenance + reproducibility + acceptance test + receipt. Remote CI failure does not relax this rule.
