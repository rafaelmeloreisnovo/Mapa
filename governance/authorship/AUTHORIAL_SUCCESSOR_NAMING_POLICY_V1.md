# RAFAELIA Authorial Successor Naming Policy V1

Status: PROVISIONAL / TRADEMARK_REVIEW_REQUIRED

## Goal
Provide neutral, provenance-safe working identifiers for clean-room successor modules without erasing upstream history or implying endorsement.

## Rules
1. Legacy names remain in historical/provenance records.
2. New names apply only to independently specified/reimplemented modules after path-level provenance review.
3. Renaming does not change license obligations or authorship of inherited code.
4. Public product naming requires trademark/domain/package-name review.
5. Transitional mapping uses `supersedes`, `derived_from`, or `clean_room_successor_of` only when evidence supports that relation.

## Working identifiers
- Virtualization runtime successor: `RAFAELIA_VIRTUAL_RUNTIME`
- QEMU-derived integration layer: retain `QEMU` attribution where QEMU code is used; original RAFAELIA-only low-level modules may use `RAFAELIA_RMR` after provenance closure.
- Termux-derived application: retain Termux attribution for inherited code; RAFCODEPHI-specific original modules use `RAFCODEPHI_*` identifiers where provenance supports them.
- llama-related repository: no global rebrand claim until file-level provenance audit closes.

No identifier in this file is a trademark clearance or legal opinion.
