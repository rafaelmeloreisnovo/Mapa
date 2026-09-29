# RAFAELIA — Session F_gap/F_next Materialization — 2026-09-29

status: APPEND_ONLY_WORK_QUEUE
claim_allowed: false
predecessors:
- Mapa issue #567
- Mapa PR #377
- Mapa commit 6fb1947c181aba1f3e7e3271535b8d0c6fb1f473

## Invariants
SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM
TOKEN_VAZIO != 0
IMPLEMENTED_UNTESTED != PASS
RETRIEVAL_CONTEXT != WEIGHT_UPDATE

## Session intersections

| id | F_gap observed in session | state | F_next materialized | evidence/gate |
|---|---|---|---|---|
| SG-001 | exact-head focused test for Mapa@6fb1947c not executed | NOT_RUN | execute tests/test_knowledge_campus_gymnasia_federation_v1.py against exact SHA and retain output | PASS only from execution receipt |
| SG-002 | workflow runs for 6fb1947c absent in queried PR-triggered run surface | NOT_RUN | trigger/observe authorized CI for exact head; record run id/job/log refs | empty query != global absence |
| SG-003 | combined commit statuses for 6fb1947c empty | NOT_RUN | bind status/check evidence after exact-head execution | statuses=[] |
| SG-004 | no PR found for atlas/campus-source-rebind-v1-20260928 | OPEN | create draft PR only through authorized provider path after test evidence; human review; no auto-merge | PR search=[] |
| SG-005 | rollback test not executed | NOT_RUN | replay predecessor -> candidate -> rollback in isolated branch/worktree and compare expected refs | rollback evidence required |
| SG-006 | full historical conversation corpus not reindexed in current cycle | OPEN | cursor-first ingest from authoritative corpus source; deduplicate interaction IDs; preserve source refs | current chat context != full corpus |
| SG-007 | some historical IA statements lack execution_ref | OPEN | classify each as SEMANTIC_COORDINATION until execution evidence exists | do not promote narrative to execution |
| SG-008 | reconstruction may be incomplete where source_ref/exact_ref is absent | TOKEN_VAZIO_RECONSTRUCTION | emit typed gap per missing pointer; resolve from authoritative source only | fail-closed |
| SG-009 | Drive-side receipt/index update for this session not yet written | NOT_RUN | append receipt in canonical Drive evidence/receipt surface after Git artifact exists | Drive=corpus/index/receipt authority |
| SG-010 | START HERE topology change not established | NO_CHANGE_REQUIRED | do not modify START HERE unless routing topology changes | short-router invariant |
| SG-011 | standards mapping for this delta has no new control-level evidence | TOKEN_VAZIO | add only official/versioned control refs when applicability is demonstrated | no certification claim |
| SG-012 | child-safety/environmental relevance not evidenced for this technical routing delta | TOKEN_VAZIO | retain fail-closed relevance fields; reassess if human/data scope changes | no invented applicability |

## Execution order
1. SG-001 exact-head focused test.
2. SG-002/003 CI + status evidence.
3. SG-004 draft PR with human gate.
4. SG-005 rollback replay.
5. SG-006/007/008 interaction-corpus reconstruction.
6. SG-009 Drive receipt.
7. Recompute gaps; never close by assertion.

## ROUTE_PIN
route_id: R-SESSION-FGAP-FNEXT-20260929
source_ref: CURRENT_SESSION + issue#567 + PR#377 + Mapa@6fb1947c
target_ref: this append-only work queue
relation_type: SESSION_GAP_TO_EXECUTABLE_SUCCESSOR
owner: human/RAFAELIA
authority: Mapa routing; producer repositories for implementation; Drive for corpus/receipt
predecessor: R-INTERACTION-IA-INTERSECTION-097
supersedes: TOKEN_VAZIO_SESSION_WORK_QUEUE
dependency_edges: SG-001..SG-012
evidence_ref: exact Git refs and current provider queries
receipt_ref: commit produced by this branch
replay_recipe: read predecessors -> verify 6fb1947c -> execute rows in order -> append receipts -> recompute
rollback_ref: branch can be deleted/reverted without touching main
reconstruction_minimum: predecessor refs + this file + exact execution receipts
privacy_class: corpus-by-reference; no corpus duplication
retention_class: APPEND_ONLY
standards_refs: TOKEN_VAZIO until official/versioned applicability mapping
rights_refs: privacy-by-design; human review
human_impact: auditability/navigation
child_safety_relevance: TOKEN_VAZIO
environmental_relevance: TOKEN_VAZIO
claim_allowed: false

## R3 seed
F_ok: session gaps are materialized as typed executable successors.
F_gap: SG-001..SG-012 remain governed by their individual states.
F_next: SG-001.
