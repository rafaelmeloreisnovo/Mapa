# OAM–Skyrmion CI Delta Receipt — 2026-08-12

Status: `CI_REMOTE_FAIL / CONTENT_VERDICT=TOKEN_VAZIO`

Related evidence gate: `docs/canonical/2026-08-12/OAM_SKYRMION_TOPOLOGY_EVIDENCE_GATE_V1.md`

Related structured receipt: `data/evidence/oam_skyrmion_topology_receipt_2026-08-12.v1.json`

PR: `#209` — `audit/oam-skyrmion-topology-20260812` → `main`

Observed head before this receipt: `f72b52c8ee7a2e3ca3977f499cb77b989d3b3223`

## Remote observations

Three GitHub Actions workflows associated with the observed head concluded `FAIL`:

| Workflow class | run_id | job_id | observed steps |
|---|---:|---:|---:|
| CI | 31659124932 | 94320012837 | 0 |
| Branch Topology Gate | 31659124954 | 94320013105 | 0 |
| Promotion Control | 31659124933 | 94320012966 | 0 |

At least one direct log retrieval attempt returned unavailable/`BlobNotFound` rather than an executable-step log.

## Classification

- `CI_REMOTE_STATUS = FAIL`
- `CI_EXECUTED_TEST_STEPS = 0`
- `CI_CONTENT_VERDICT = TOKEN_VAZIO`
- `CI_EXACT_FAILURE_REASON = TOKEN_VAZIO_EXACT_FAILURE_REASON`
- `CI_LOG_PROVENANCE = PARTIAL / log blob unavailable for inspected job`
- `PROMOTION_ALLOWED = false`
- `claim_allowed = false`

The observation of zero executed steps is **consistent with** a failure before workflow test execution (for example startup/runner/provisioning/control-plane class), but this is an inference only. It is not sufficient evidence to assign a definitive root cause.

Therefore this receipt does **not** classify the remote red state as a scientific, mathematical, or source-code test failure. It also does not classify it as definitively an infrastructure failure.

## TOKEN_VAZIO ledger delta

| ID | State | Urgency | Importance | Next verifiable action |
|---|---|---:|---:|---|
| `TV_CI_EXACT_FAILURE_REASON` | `TOKEN_VAZIO_EXACT_FAILURE_REASON` | P0 | high | Recover GitHub runner/job diagnostic or a future run with executable steps; preserve raw logs/IDs. |
| `TV_CI_CONTENT_VERDICT` | `TOKEN_VAZIO` | P0 | high | Obtain a run in which repository checkout/test steps actually execute. |
| `TV_CI_LOG_BLOB` | `TOKEN_VAZIO_UNAVAILABLE` | P1 | medium | Retry only when GitHub exposes the job log; hash/capture it if available. |

## Non-regression rule

The scientific gate remains `VERIFIED_LIMITED / claim_allowed=false` from the local deterministic toy reproduction. CI status is an independent operational axis:

`LOCAL_TOY_EVIDENCE != REMOTE_CI_EXECUTION != PRIMARY_PAPER_EVIDENCE != EXPERIMENTAL_REPLICATION`.

No merge/promotion is authorized by this delta.
