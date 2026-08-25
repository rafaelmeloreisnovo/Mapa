# RAFAELIA Authorship / Provenance / Clean-Room Governance

This directory is the canonical control surface for authorship, licensing, provenance, clean-room replacement and legal-release readiness.

## Files
- `RAFAELIA_AUTHORSHIP_PROVENANCE_CLEANROOM_V1.md` — policy and method.
- `AUTHORSHIP_PROVENANCE_REGISTRY.v1.json` — current component-level classification.
- `AUTHORSHIP_RECEIPT_TEMPLATE.v1.json` — per-module receipt schema.
- `LEGAL_RELEASE_GATE_V1.md` — release checklist and fail-closed gate.

## Invariants
- `RENAME != NEW_AUTHORSHIP`
- `REFACTOR != CLEAN_ROOM`
- `REPOSITORY_OWNERSHIP != COPYRIGHT_OWNERSHIP_OF_ALL_CONTENT`
- `LICENSE_PERMISSION != TRADEMARK_PERMISSION`
- `TOKEN_VAZIO != CLEARED`
- `claim_allowed=false` until the applicable provenance/license/release gate is closed.

## Scope
Initial audit surface: `qemu_rafaelia`, `termux-app-rafacodephi`, `Vectras-VM-Android`, `llamaRafaelia`, AndroidX/Gradle dependencies and later-discovered third-party components.

The working successor label for an independently rebuilt virtualization runtime is `RAFAELIA_VIRTUAL_RUNTIME`. This label is provisional and does not erase upstream Vectras/QEMU/Android/Termux provenance or obligations.
