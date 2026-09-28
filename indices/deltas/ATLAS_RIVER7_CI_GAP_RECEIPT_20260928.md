# ATLAS — RIVER-7 CI Gap Receipt — 2026-09-28

**parent:** \`ATLAS_RIVER7_GAP_CLOSURE_V2_20260928\`  
**supersedes field:** \`RIVER7-CI=PENDING\`  
**new state:** \`RIVER7-CI=REMOTE_FAIL_UNRESOLVED\`  
**claim_allowed:** \`false\`

## Evidence split

### Exact-source local execution

For \`ChipQuantum#86\` head
\`ae5bd3a1ee18f7dd099b433078975fa9957c7fca\`:

\`\`\`text
unittest: 5/5 PASS
exit_code: 0
simulator: SIMULATION_PASS
receipt_sha256: c40a6c42ab9250ba41e3c10cb0198049d99228efa7d553aabe693ebb00e9f769
physical_network_state: NOT_RUN
\`\`\`

Source blobs observed before execution:

\`\`\`text
simulator: 02bace136d0e202804f82069a09019461c6bfdf2
test:      7ae689f7a9e6b5eac65587c7c0d0e8153535bc6c
workflow:  09cbd124f12a2d37804697c35ff0a45d4cb3056f
\`\`\`

### GitHub Actions

Dedicated workflow:

\`RIVER-7 Offline Validation\`

Evidence:

\`\`\`text
run_id: 36376514936
first job: 108783373691 -> failure
rerun job: 108783733869 -> failure
steps via connector: unavailable
logs via connector: unavailable
\`\`\`

Therefore:

\`\`\`text
LOCAL_EXACT_PASS = observed
REMOTE_CI_PASS   = false
REMOTE_CAUSE     = TOKEN_VAZIO
\`\`\`

No inference is allowed from unavailable logs to a specific provider, runner,
billing, checkout or code cause.

## Updated gaps

| Gap | State |
|---|---|
| RIVER7-FEC-743 | CLOSED_FINITE_DOMAIN |
| RIVER7-REORDER | CLOSED_FINITE_DOMAIN |
| RIVER7-LEAKAGE-SYNTHETIC | PARTIAL_CLOSED |
| RIVER7-LOCAL-EXACT | PASS |
| RIVER7-CI | REMOTE_FAIL_UNRESOLVED |
| RIVER7-CI-ROOT-CAUSE | TOKEN_VAZIO |
| RIVER7-FEC-GENERAL | OPEN |
| RIVER7-AUTH-SYMBOL | OPEN |
| RIVER7-LOSS-BURST | OPEN |
| RIVER7-LEAKAGE-PHYSICAL | NOT_RUN |
| RIVER7-PHYSICAL | NOT_RUN |
| RIVER7-WIRE | ROUTE_STATE_BLOCKED |
| RIVER7-PRODUCTION | ROUTE_STATE_BLOCKED |

## F_next

The smallest next verifiable step is no longer another change to the erasure algorithm.

It is to obtain remote execution evidence for the dedicated job. Until a step or log
identifies a code/workflow defect, modifying the algorithm would violate
fail-closed diagnosis.

\[
F_{next}=RESOLVE(CI\_ROOT\_CAUSE)
\]

while preserving:

\[
LOCAL\_PASS\neq CI\_PASS.
\]

## R3

\`F_ok\`: exact source passes offline and finite mathematical boundaries are stable.  
\`F_gap\`: remote CI root cause remains \`TOKEN_VAZIO\`; physical execution remains
\`NOT_RUN\`.  
\`F_next\`: obtain remote job evidence, then apply the smallest evidence-backed
hotfix only if required.
