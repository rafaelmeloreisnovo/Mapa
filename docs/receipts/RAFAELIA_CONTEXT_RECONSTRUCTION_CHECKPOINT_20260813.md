# RAFAELIA Context Reconstruction Checkpoint — 2026-08-13

State: VERIFIED_LIMITED
claim_allowed=false
append_only=true

Fresh-base replay of the privacy-preserving context anchor delta.

Base main at replay: `05b27c3d398030470de9b82938408f1d74fb301c`.
Historical first materialization remains preserved in PR #220 / branch `audit/context-anchor-index-20260813` and is not rewritten.

Materialized on this branch:
- `data/memory/context-anchors-20260813.v1.json`
- `indices/RAFAELIA_CONTEXT_ROUTE_INDEX_20260813_V1.md`
- this receipt

Evidence anchors:
- chat export SHA256 `53fbfbc52d110d5815024ca851868555d23c3180cd73bb5433dd5f5bade9d93f`; ZIP PASS; 2573 conversations; 239506 payload messages; no raw private content committed.
- Termux APK SHA256 `e6265a57eb5ca363808488e3b01955958bed93bc0c8a0d281849b363b11027ec`; static ZIP/certificate/ABI inspection PASS; physical runtime TOKEN_VAZIO.
- visual family count 7; state SYMBOLIC_VISUAL_ARTIFACTS; scientific claim false.

F_ok=identity+aggregate index+routes+fresh-main replay.
F_gap=conversation graph, cross-export dedup, custom runtime binding, visual generator provenance, physical receipts.
F_next=open draft PR from this clean branch; keep #220 as historical checkpoint; no force-push/merge until gates are reviewed.
