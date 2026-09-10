# Third-Party / Copyright Notices Audit V1

Status: ACTIVE_AUDIT / INCOMPLETE / FAIL_CLOSED
Observed at: 2026-09-09T23:10-03:00
Scope: first high-risk upstream/fork/import tranche under `rafaelmeloreisnovo`.

This is an engineering/compliance ledger, not a legal opinion. Repository ownership does not establish copyright ownership of inherited content. Unknown provenance or license terms remain `TOKEN_VAZIO`; `claim_allowed=false` until the relevant gate closes.

## Mandatory mapping

`FROM -> TO -> WHAT -> WHO -> LICENSE -> OBLIGATION -> ACTION`

| from / upstream | to / repository | what | upstream authority | license observed | obligations / caution | status / action |
|---|---|---|---|---|---|---|
| `termux/termux-app` | `rafaelmeloreisnovo/termux-app-rafacodephi` | inherited Termux application tree plus RAFCODEPHI additions | Termux project/developers | GPL-3.0 family observed in repository docs; exact distributed-file matrix pending | preserve upstream copyright/license; GPL distribution obligations apply to covered distributed material; separate RAFCODEPHI-only paths by commit/path proof | `DETACHED_IMPORTED_UPSTREAM`; build inherited-vs-authorial manifest; `claim_allowed=false` for whole-tree authorship |
| `termux/termux-packages` via `termux-play-store/termux-packages` | `rafaelmeloreisnovo/termux-packages` | Termux package build system / package recipes | Termux + individual package upstreams | GitHub `NOASSERTION`; package-level licenses vary | do not assign one license to whole package universe; preserve each package/upstream license and required source/notices | `GITHUB_FORK`; generate per-package license inventory; `claim_allowed=false` for whole-tree authorship |
| `BLAKE3-team/BLAKE3` | `rafaelmeloreisnovo/BLAKE3` | upstream BLAKE3 core plus separate `rmr/` additions | BLAKE3 team for upstream | GitHub detects Apache-2.0; repository also carries `LICENSE_A2`, `LICENSE_A2LLVM`, `LICENSE_CC0` | retain applicable upstream license/notice surfaces; resolve license per path; `rmr/` cannot inherit authorship merely from directory name | `GITHUB_FORK`; `FORK_NOTES.md` says upstream core remains reference and `rmr/` is external. Gap: it references `LICENSE_RMR`, not observed in root listing -> `RIGHTS_UNRESOLVED` for RMR distribution until resolved |
| `openssl/openssl` | `rafaelmeloreisnovo/openssl` | OpenSSL TLS/crypto library fork | OpenSSL project/contributors | Apache-2.0 detected | preserve Apache-2.0 license/copyright notices; preserve applicable NOTICE if present; modifications must not erase upstream provenance | `GITHUB_FORK`; upstream content is third-party; path-level modifications remain to inventory |
| `gradle/gradle` | `rafaelmeloreisnovo/gradle` | Gradle build system fork | Gradle project/contributors | Apache-2.0 detected | preserve license/copyright notices and applicable NOTICE; separate local patches from inherited tree | `GITHUB_FORK`; upstream content is third-party; diff inventory pending |
| `torvalds/linux` | `rafaelmeloreisnovo/linuxkernel` | Linux kernel source fork | Linux kernel copyright holders/contributors | GitHub `NOASSERTION`; per-file SPDX/license surfaces required | never collapse kernel tree to one invented license; inspect root COPYING and per-file SPDX/`LICENSES/`; preserve notices and applicable source obligations | `GITHUB_FORK`; file-level license inventory required before redistribution claims |
| `LuaJIT/LuaJIT` | `rafaelmeloreisnovo/LuaJIT` | LuaJIT mirror/fork | LuaJIT upstream / relevant copyright holders | GitHub `NOASSERTION` | inspect upstream COPYRIGHT/license text; preserve notices; do not infer license from repo name | `GITHUB_FORK`; license text/path audit pending |
| `RikkaApps/Shizuku` | `rafaelmeloreisnovo/Shizuku` | Shizuku Android project fork | RikkaApps/Shizuku contributors | Apache-2.0 detected | preserve Apache-2.0 license/copyright notices and applicable NOTICE; identify local modifications | `GITHUB_FORK`; upstream content is third-party; diff inventory pending |
| QEMU upstream + bundled third parties | `rafaelmeloreisnovo/qemu_rafaelia` | QEMU mirror/import plus RAFAELIA/RMR candidate paths | QEMU project + bundled third-party holders | GitHub `NOASSERTION`; existing governance observes mixed QEMU/third-party license surfaces | preserve all applicable upstream licenses; classify per file/linkage; RAFAELIA naming does not reassign inherited copyright | `DETACHED_IMPORTED_UPSTREAM`; whole-tree authorship prohibited; RMR candidates require path/blob/commit proof |
| Vectras VM upstream + QEMU/Android dependencies | `rafaelmeloreisnovo/Vectras-VM-Android` | legacy Vectras-derived Android VM application with clean-room successor work | Vectras/upstream dependency holders plus separately proven RAFAELIA additions | existing governance records GPL-2.0 surface; exact per-component terms vary | preserve upstream GPL/notices; quarantine unresolved C/D material; clean-room successor requires independent spec/implementation/test receipt | `B_D_MIXED`; no authorial-clean whole-repo claim |

## Non-negotiable release rule

For every distributed repository, APK, binary, source bundle or copied-in component, the release surface must be generated from the actual included paths/dependencies, not from this summary. A row here is a provenance warning and routing record; it does not replace upstream LICENSE/COPYING/NOTICE files.

If `SOURCE`, `COPYRIGHT_HOLDER`, `LICENSE`, `NOTICE`, or path lineage is unknown: set the field to `TOKEN_VAZIO`, block an authorial-clean claim, and resolve before release when the unknown can affect redistribution rights or obligations.

## Next audit tranche

Enumerate every repository owned by `rafaelmeloreisnovo`, classify `GITHUB_FORK`, `DETACHED_IMPORTED_UPSTREAM`, `VENDORED_THIRD_PARTY`, `DEPENDENCY`, `GENERATED_UNVERIFIED`, or `AUTHORIAL_PROVEN`, then descend only into modified/copied-in paths for file-level provenance. Prioritize `Vectras-VM-Android`, `termux-api*`, `UserLAnd*`, `androidx_RmR`, `android_frameworks_base_rafaelia`, `CryptoSwift_RmR`, `florisboard`, `nanoGPT`, `DeepSeek`, `TinyGPT`, and `llamaRafaelia`.

## Evidence anchors

- GitHub repository metadata: fork/parent/source/license fields for the observed forks.
- `BLAKE3/FORK_NOTES.md`: explicit upstream redistribution and isolated `rmr/` statement.
- Existing `governance/authorship/PROVENANCE_MATRIX_V1.md`: QEMU, Termux, Vectras and AndroidX governance baseline.

R3 = <F_ok: first high-risk third-party ledger materialized; F_gap: complete owner inventory + per-file/diff/NOTICE/license scans remain; F_next: enumerate all owned repos and append only newly evidenced rows>.
