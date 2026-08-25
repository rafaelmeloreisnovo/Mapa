# RAFAELIA Authorship, Provenance, Licensing & Clean-Room Policy V1

Status: CANONICAL_DRAFT / REVIEW_REQUIRED / claim_allowed=false

## 1. Purpose
This policy governs authorship, provenance, licensing, clean-room reimplementation, third-party attribution, branding, and release readiness across the RAFAELIA ecosystem.

It does not convert third-party material into RAFAELIA authorship by renaming, refactoring, paraphrasing, or recompiling it.

Core invariant:
`ORIGINAL_AUTHORSHIP != LICENSED_DERIVATIVE != CLEAN_ROOM_REIMPLEMENTATION != THIRD_PARTY_COMPONENT`

Also:
`RENAME != NEW_AUTHORSHIP`

## 2. Evidence classes
- A — AUTHORIAL_PROVEN: original RAFAELIA authorship supported by source history/provenance.
- B — THIRD_PARTY_LICENSED: externally authored material retained under its applicable license and notices.
- C — RIGHTS_UNRESOLVED: provenance/license insufficient; distribution blocked.
- D — CLEAN_ROOM_REQUIRED: replacement required before authorial-only distribution.
- E — CLEAN_ROOM_REIMPLEMENTED: independently specified, independently implemented, independently tested, with provenance receipt.

Unknown values remain `TOKEN_VAZIO`; repository ownership alone never proves A/E.

## 3. Clean-room method
1. INVENTORY — identify source path, origin, license, copyright/trademark notices, dependency role.
2. REQUIREMENTS — write functional requirements and acceptance tests without copying expression.
3. IMPLEMENTATION — implement from the independent specification.
4. DISSIMILARITY REVIEW — compare naming, structure, comments, tables, APIs, constants, assets and control flow for accidental derivation.
5. LICENSE REVIEW — ensure new source has explicit license and respects obligations of linked/combined components.
6. TEST — execute independent tests and preserve before/after evidence.
7. RECEIPT — persist source pointers, hashes, reviewers, scope, limitations and `claim_allowed`.

Where a genuine separated clean-room process is unavailable, mark `CLEAN_ROOM_ASSURANCE_LIMITED` rather than asserting legally independent implementation.

## 4. Third-party material
For QEMU, AndroidX, Termux, llama.cpp-derived/related material, Vectras upstream and other third-party components:
- preserve upstream copyright/license notices;
- record exact upstream repository/ref/path when known;
- preserve corresponding-source obligations where applicable;
- never claim upstream code as RAFAELIA-authored;
- document RAFAELIA modifications separately;
- keep trademark/branding permission distinct from copyright/license permission.

## 5. Freestanding kernels
Where technically appropriate, new RAFAELIA kernels may target:
- no libc dependency;
- no malloc/heap/GC;
- no unnecessary runtime dependencies;
- no tail/shadow compatibility layers unless explicitly required and evidenced;
- minimal exported symbols, loops, branches and linkage surface;
- explicit ABI contracts.

These are engineering constraints, not proof of legal independence. Provenance still applies.

## 6. Friction as catalyst
Operational friction is a signal for decomposition, specialization, testing and evidence collection. It never authorizes bypassing licensing, provenance, security or authority gates.

## 7. Naming
Legacy/third-party names are not silently erased. Naming changes require trademark review, provenance-preserving supersession/alias relations, and no implication of upstream endorsement.

For a future independently rebuilt virtualization product, use provisional working identifier `RAFAELIA_VIRTUAL_RUNTIME` until naming/trademark review closes.

## 8. Release gate
No release may be promoted as authorial-clean unless all distributed components have:
- provenance class A, B or E;
- license identified;
- required notices present;
- third-party source/source-offer duties satisfied where applicable;
- no C/D material in the distributable set;
- clean-room receipts for E material;
- current dependency inventory;
- secrets/keystores excluded;
- privacy/data-processing obligations documented where applicable.

`claim_allowed=false` until closure.

## 9. Legal boundary
This is an engineering/compliance control, not legal advice or regulatory certification. Ambiguous redistribution, trademark, patent, linking or privacy questions remain `LEGAL_REVIEW_REQUIRED` / `TOKEN_VAZIO`.
