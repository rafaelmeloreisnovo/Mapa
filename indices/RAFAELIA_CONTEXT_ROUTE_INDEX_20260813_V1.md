# RAFAELIA Context Route Index — 2026-08-13

State: VERIFIED_LIMITED / APPEND_ONLY / claim_allowed=false

Invariant: `kernel -> index -> minimal relevant subgraph -> evidence -> append-only delta`.

Routes:
- MEMORY: `ART-CTX-20260813-001 -> IDX-08 -> bounded time/topic filter -> selected conversation -> chunks -> graph`.
- RUNTIME: `ART-RUNTIME-20260813-001 -> IDX-05 -> exact SHA -> static provenance -> custom-build comparison -> physical receipt`.
- VISUAL: `VIS-RAFAELIA-FRACTAL-20260813 -> exact image hash -> generator/parameters -> formula relation after provenance`.

Boundaries:
- private raw conversation content is not copied to this index;
- symbolic visual != scientific evidence;
- static APK != runtime proof;
- duplicate/alias != independent evidence;
- TOKEN_VAZIO remains open until closure evidence.

Anchors:
- chat export: SHA256 `53fbfbc52d110d5815024ca851868555d23c3180cd73bb5433dd5f5bade9d93f`, 2573 conversations, 239506 messages with payload, VERIFIED_AGGREGATES_LOCAL.
- Termux APK: SHA256 `e6265a57eb5ca363808488e3b01955958bed93bc0c8a0d281849b363b11027ec`, com.termux, FDroid certificate observed, four ABIs, VERIFIED_STATIC.
- fractal family: 7 images, SYMBOLIC_VISUAL_ARTIFACTS.

F_gap: conversation remote index; chunk graph; cross-export dedup; custom RAFCODEphi binding; exact APK physical receipt; visual generator/parameter provenance.

F_next: materialize privacy-preserving conversation ID/time/topic index, then selective graph links; resolve runtime and visual provenance separately.
