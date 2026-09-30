# NOVOexport SAF executor evidence — 2026-09-30

cycle_id: Ω-H-20260930-SAF-EXECUTOR-106
route_id: R-NOVOEXPORT-SAF-EXECUTOR-106
source_ref: Mapa@bb03dad5cb241107c233e1caaa96e0e71a2be8a9; RafGitTools PR#584 head=65c2323d1c20d6e1b81f71e33e9aebb6c98173e6 merge=862b83547532d47e60eadf7810e0571b12ca8804
target_ref: RafGitTools Android foreground NOVOexport persistent queue executor
relation_type: MANIFEST_ROUTE_TO_IMPLEMENTED_QUEUE_EXECUTOR
owner: human/RAFAELIA
authority: Mapa=routing; RafGitTools=implementation/runtime; Drive=source/provider evidence
predecessor: R-NOVOEXPORT-MERGE-105
supersedes: TOKEN_VAZIO_QUEUE_EXECUTOR_IMPLEMENTATION
dependency_edges: SAF_TREE,PERSISTENT_QUEUE,ONE_ITEM_EXECUTOR,DRIVE_READBACK,GIT_READBACK,COMPLETION_GATE
evidence_ref: RafGitTools workflow run 36567876002 conclusion=success for exact head 65c2323d1c20d6e1b81f71e33e9aebb6c98173e6
receipt_ref: RafGitTools PR#584 + merge 862b83547532d47e60eadf7810e0571b12ca8804
replay_recipe: select authorized SAF tree; inventory; persist queue; process one eligible item; require verified provider readbacks before COMPLETE
rollback_ref: RafGitTools base cc2363c88260681c58c74189b1d2780384437182
reconstruction_minimum: Mapa merge, PR#584, head SHA, merge SHA, workflow run id, queue transition contract
privacy_class: CORPUS_BY_REFERENCE_ONLY
retention_class: APPEND_ONLY
standards_refs: TOKEN_VAZIO_CONTROL_LEVEL
rights_refs: privacy-by-design,data-minimization,human-review
human_impact: auditability
child_safety_relevance: TOKEN_VAZIO_APPLICABILITY
environmental_relevance: TOKEN_VAZIO_APPLICABILITY
claim_allowed: false
hash/ref: 862b83547532d47e60eadf7810e0571b12ca8804

before_state: queue executor implementation was not bound in the Mapa route.
after_state: exact executor implementation and exact-head workflow success are bound; physical Android canary remains NOT_RUN.
exact_ref: RafGitTools@65c2323d1c20d6e1b81f71e33e9aebb6c98173e6
environment_ref: GitHub Actions run 36567876002; physical Android execution=TOKEN_VAZIO
command_or_action: provider readback of PR/head/merge/workflow; no physical SAF action in this cycle
expected_observable: implemented one-item executor with fail-closed COMPLETE gate and CI evidence
actual_observable: PR#584 merged; exact-head orchestrated workflow success; physical-phone canary not claimed
falsifier: later replay contradicts transition/readback contract or exact refs fail to reproduce implementation
rollback_procedure: supersede this route and return routing to predecessor; preserve historical receipt
rollback_test: NOT_RUN
reconstruction_state: PASS_TO_IMPLEMENTATION_AND_CI; TOKEN_VAZIO_PHYSICAL_RUNTIME

BODY_state: IMPLEMENTED_CI_OBSERVED
SOUL_state: AUTHORITY_SPLIT_PRESERVED
SPIRIT_state: FAIL_CLOSED_COMPLETION_GATE
ARCH_PIN: Mapa manifest route -> RafGitTools queue executor -> provider readback receipt
languages_components: Kotlin Android queue/executor
origin_classification: TOKEN_VAZIO_ORIGIN
CORE_FREESTANDING_candidates: TOKEN_VAZIO_NO_DELTA
ADAPTER_PLATFORM_boundaries: Android SAF,filesystem,Drive provider,GitHub provider,UI,process lifecycle
TAIL_delta: dependencies made explicit
SHADOW_delta: executor route now exact-ref bound
FRICTION_delta: physical Android/provider boundary remains necessary

R3: F_ok=executor merged+CI observed; F_gap=physical canary/per-object receipt/rollback test NOT_RUN; F_next=authorized physical one-item canary with verified provider receipt.
