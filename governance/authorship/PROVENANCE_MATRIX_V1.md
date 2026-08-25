# Provenance Matrix V1

| component | repo | upstream authority | current class | legal/provenance state | next gate |
|---|---|---|---|---|---|
| qemu_rafaelia | rafaelmeloreisnovo/qemu_rafaelia | QEMU + bundled third parties | B_MIXED_WITH_A_CANDIDATES | upstream licensing must remain; RAFAELIA RMR may be separable by path-level proof | file-level provenance + license matrix |
| termux-app-rafacodephi | rafaelmeloreisnovo/termux-app-rafacodephi | Termux + Android/AndroidX dependencies | B_DERIVATIVE_WITH_A_CANDIDATES | inherited Termux remains third-party; RAFCODEPHI-only modules require commit/path evidence | authorial module ledger + third-party notices |
| Vectras-VM-Android | rafaelmeloreisnovo/Vectras-VM-Android | Vectras VM + QEMU/Android dependencies | B_D_MIXED | current repo documents GPL-2.0 obligations and a clean-room replacement plan | forensic inventory + quarantine + successor specs |
| llamaRafaelia | rafaelmeloreisnovo/llamaRafaelia | llama.cpp/related | TOKEN_VAZIO | repository existence is not file-level authorship proof | LICENSE/NOTICE + path lineage audit |
| AndroidX | multi-repo dependency | AndroidX | B_THIRD_PARTY_DEPENDENCY | preserve dependency licenses/notices | Gradle dependency/license inventory |

## Evidence already observed
- `qemu_rafaelia` contains QEMU/third-party licensing surfaces including `COPYING.LIB`, Linux header licenses and EDK2 licenses, plus `hw/core/rafaelia-rmr-license.txt` for a RAFAELIA-specific low-level module.
- `Vectras-VM-Android/docs/LEGAL_AND_LICENSES.md` states GPL-2.0 distribution/attribution obligations for the current project.
- `Vectras-VM-Android/AUTHORSHIP_CLEANROOM_PLAN.md` already defines a replacement program with provenance classes, quarantine and clean-room implementation.

## Release invariant
No row is promoted to `AUTHORIAL_CLEAN` from this matrix alone. The per-module receipt and release gate must close.
