# Public Repository License & README Audit — 2026-09-16

**Scope:** `rafaelmeloreisnovo` public repositories only  
**Observed account inventory:** 86 repositories = 51 public + 35 private  
**Audit layer:** repository-level LICENSE / README / attribution / provenance consistency  
**Not a claim:** this is not a file-by-file legal opinion, patent clearance, trademark clearance, privacy impact assessment, export-control review, or certification of legal compliance.

## Invariants

```text
PUBLIC != PUBLIC_DOMAIN
VISIBLE_SOURCE != OPEN_SOURCE
COPYRIGHT != LICENSE
FORK_MAINTAINER != UPSTREAM_COPYRIGHT_OWNER
HASH != LEGAL_OWNERSHIP
DOI != LICENSE
MANIFESTO != STATUTE
SOURCE != CLAIM != EVIDENCE
THIRD_PARTY_MATERIAL != RELICENSED_BY_INCLUSION
TOKEN_VAZIO > invented permission
```

## Status vocabulary

- **OK_STANDARD** — standard/root license and README are materially consistent.
- **OK_UPSTREAM/MULTI** — upstream, dual, component or file-level licensing is preserved.
- **FIXED** — a concrete LICENSE/README contradiction was corrected during this audit.
- **POLICY_SCOPED** — licensing is intentionally scoped by content/component/policy.
- **TOKEN_VAZIO** — no safe repository-wide license selection can be inferred.
- **RISK_NO_UPSTREAM_LICENSE** — third-party/upstream material is visible but no express upstream license was located.
- **PR_PENDING** — correction prepared but protected-branch merge is still required.

## 51-public-repository matrix

| # | Repository | Observed legal surface | State | Audit result / next boundary |
|---:|---|---|---|---|
| 1 | actions | MIT upstream | OK_UPSTREAM/MULTI | Preserve Gradle/upstream copyright; do not replace with fork-owner copyright. |
| 2 | androidRom | no root LICENSE/README/NOTICE located; no SPDX/Copyright search hit | TOKEN_VAZIO | Do not invent a blanket license. Inventory provenance/file-level rights first. |
| 3 | androidx_RmR | `LICENSE.txt` Apache-2.0 | OK_UPSTREAM/MULTI | Preserve AndroidX/upstream notices. |
| 4 | android_frameworks_base_rafaelia | `NOTICE` contains Apache-2.0 + third-party notices | OK_UPSTREAM/MULTI | Treat NOTICE/file-level notices as controlling; do not flatten authorship. |
| 5 | arxiv-docs | MIT upstream | OK_UPSTREAM/MULTI | Upstream copyright preserved. |
| 6 | BLAKE3 | `LICENSE_A2` + `LICENSE_CC0` | OK_UPSTREAM/MULTI | Dual upstream licensing preserved. |
| 7 | Catalogo-cosmologico | README said MIT while `LICENSE.md` said CC-BY-SA | FIXED | Scoped: authored code MIT; authored documentation/catalog presentation CC BY-SA 4.0; third-party scientific data not relicensed. |
| 8 | CientiEspiritual | `License.md` policy; provenance/SPDX inventory explicitly open | POLICY_SCOPED | README corrected: public/auditable source != blanket open-source grant; compliance references != certification. |
| 9 | Cosmos | README MIT; former LICENSE was symbolic/restrictive manifesto | FIXED | Root LICENSE restored to canonical MIT; former manifesto archived as non-normative provenance. |
| 10 | CryptoSwift_RmR | upstream CryptoSwift license | OK_UPSTREAM/MULTI | Preserve upstream attribution/license. |
| 11 | DeepSeek-RafCoder | code/model licenses mixed with manifesto | FIXED | Clean MIT `LICENSE-CODE`; model terms remain separate; root is provenance index; manifesto archived. |
| 12 | Espiritual-espirualidade | no repository-wide license located | TOKEN_VAZIO | Public visibility grants no blanket reuse permission; owner decision needed for a standard license. |
| 13 | fcea-originum | no root LICENSE/README located | TOKEN_VAZIO | Determine provenance and intended grant before licensing. |
| 14 | Fisica | authorship/provenance prose, no repository-wide license located | TOKEN_VAZIO | Copyright notice is not a reuse license; choose scope only after third-party review. |
| 15 | florisboard | Apache-2.0 upstream | OK_UPSTREAM/MULTI | Preserve upstream notices. |
| 16 | frida-desktop | `COPYING` wxWindows Library Licence 3.1 | OK_UPSTREAM/MULTI | Alternate conventional license filename is valid; do not overwrite. |
| 17 | GAIA-PDS-PHI | no repository-wide license located | TOKEN_VAZIO | Explicit owner/license decision required before claiming open source. |
| 18 | GEOMETRIA_SOLAR_Maia_Inca | MIT | OK_STANDARD | README/license consistent. |
| 19 | Graditao | GPLv3 | OK_STANDARD | Full GPL text observed. |
| 20 | gradle | Apache-2.0 upstream | OK_UPSTREAM/MULTI | Preserve Gradle upstream ownership/notices. |
| 21 | IaFcea | no standard root license; historical manifesto/legal claims | FIXED + TOKEN_VAZIO | Added legal/no-implied-license notice; historical universal/supranational claims marked non-normative. License selection still owner decision. |
| 22 | IA_nist | GPLv2 surface observed | OK_STANDARD | Keep declared license and third-party/file-level notices controlling. |
| 23 | Judicial- | no root license; legal/investigative working notes | FIXED + TOKEN_VAZIO | Added allegation/privacy/evidence boundary. No blanket reuse license inferred. |
| 24 | linuxkernel | `COPYING`: GPL-2.0 WITH Linux-syscall-note + LICENSES tree | OK_UPSTREAM/MULTI | Correct upstream licensing model; preserve file-level SPDX. |
| 25 | LuaJIT | `COPYRIGHT`: MIT + Lua/dlmalloc notices | OK_UPSTREAM/MULTI | Alternate legal filename is valid; preserve component notices. |
| 26 | Mapa | LICENSE GPLv3 while README badge said MIT | FIXED | README now matches GPLv3 LICENSE. |
| 27 | myCat-iahelpsus | upstream `yumiaura/mycat` referenced; no explicit upstream license located | RISK_NO_UPSTREAM_LICENSE | Added `LEGAL_NOTICE.md` and README warning; do not infer redistribution/commercial rights. |
| 28 | OMEGAGIT | MIT | OK_STANDARD | README correctly separates private GPL source provenance from OMEGAGIT MIT surface. |
| 29 | openssl | `LICENSE.txt` Apache-2.0 | OK_UPSTREAM/MULTI | Preserve OpenSSL NOTICE/license/trademark boundaries. |
| 30 | PCR_Rafaelia_Code_seed | GPLv3 | OK_STANDARD | README evidence boundaries do not contradict GPL. |
| 31 | qemu_rafaelia | QEMU GPLv2 whole + file-specific compatible licenses | OK_UPSTREAM/MULTI | Fork attribution present; keep path/file-level licenses controlling. |
| 32 | rafaelia-core-enterprise | no root license located | TOKEN_VAZIO | No blanket grant inferred. |
| 33 | Rafcodephi_Sdk_ndkJni_c_py_sh_asm_lua_rs_go_swift_perl_yml_ | MIT | OK_STANDARD | License present and consistent. |
| 34 | RafGitTools | GPL notice at root was abbreviated; complete GPL text now available as `COPYING` | FIXED | Preserve project NOTICE/attribution separately; complete GPL text in-repository. |
| 35 | RAFNATIONS_CORE | no root license located | TOKEN_VAZIO | Owner decision required for any reuse grant. |
| 36 | RafPolimata | README explicitly refuses inference of license from visibility | TOKEN_VAZIO | Correct epistemic/legal stance; do not auto-license. |
| 37 | RAIAREIS_FRAMEWORK | no root license located | TOKEN_VAZIO | Owner decision required for any reuse grant. |
| 38 | Recipt | explicit `TOKEN_VAZIO_OWNER_LICENSE_SELECTION` | TOKEN_VAZIO | Intentionally left unresolved; audit must not choose for owner. |
| 39 | relativity-living-light | former RAFCODE custom license conflicted with `data/CITATION.cff: CC-BY-SA-4.0` | FIXED + POLICY_SCOPED | Research/docs CC BY-SA 4.0; software/file-level rights separated; old manifesto archived as non-normative. |
| 40 | ROM-emulator | BSD-2-Clause upstream | OK_UPSTREAM/MULTI | Original Fred Jan Kraan copyright preserved. |
| 41 | Shizuku | Apache-2.0 + README trademark/resource restrictions | OK_UPSTREAM/MULTI | Code license does not erase trademark/resource conditions; preserve NOTICE. |
| 42 | templo-vivo-arcs | historical root LICENSE is manifesto; `LICENSE_POLICY.md`; software decision gate | FIXED + TOKEN_VAZIO | README now exposes policy authority. Software license remains `TOKEN_VAZIO / DECISION_REQUIRED`; no invented SPDX choice. |
| 43 | TeoremasTesesTeorias | README said MIT; LICENSE contained a research paper | FIXED | Research paper preserved under docs; root LICENSE restored to canonical MIT. |
| 44 | termux-api_rafcodephi | GPLv3 fork + `LICENSE.md`; complete `COPYING` now present | FIXED | Upstream Termux attribution preserved; component/file terms still control. |
| 45 | termux-app-rafacodephi | GPLv3 fork + component exceptions; missing complete root GPL copy | PR_PENDING | PR #449 adds complete `COPYING`; protected branch/signature rules correctly prevent direct bypass. |
| 46 | termux-packages | per-package licenses + Apache-2.0 build infrastructure | OK_UPSTREAM/MULTI | README already states not to flatten the tree into a single RAFCODEPHI license. |
| 47 | TinyGPT | MIT upstream | OK_UPSTREAM/MULTI | Preserve keith2018 copyright and dependency licenses. |
| 48 | TRABALHO_ROADMAP_AUDIT_GOV_DATA_ROTA_MAPwithCHAIN_security | no root license located | TOKEN_VAZIO | No blanket reuse grant inferred. |
| 49 | treinarModelos | MIT | OK_STANDARD | License present. |
| 50 | UserLAnd2 | GPLv3 + Apache-2.0 component notice | OK_UPSTREAM/MULTI | Preserve upstream component split. |
| 51 | Vectras-VM-Android | GPLv2 + explicit original/fork attribution | OK_UPSTREAM/MULTI | Original xoureldeen copyright retained; fork modifications separately attributed. |

## Material corrections performed

### License/README contradictions
- `Cosmos`: MIT normalized; former symbolic license archived.
- `Mapa`: MIT badge corrected to GPLv3.
- `Catalogo-cosmologico`: MIT/CC conflict converted into explicit scoped licensing.
- `TeoremasTesesTeorias`: research paper removed from license path and preserved under docs.
- `DeepSeek-RafCoder`: MIT code license cleaned; model license separated; manifesto moved to non-normative history.
- `relativity-living-light`: root licensing aligned with existing `data/CITATION.cff` CC-BY-SA-4.0 declaration; custom supraconstitutional/access-as-acceptance language removed from normative license path.

### Compliance/provenance hardening
- `CientiEspiritual`: README no longer equates public code with a blanket open-source grant or blanket statutory compliance.
- `templo-vivo-arcs`: README now routes to `LICENSE_POLICY.md` and preserves software-license `TOKEN_VAZIO`.
- `IaFcea`: legal notice separates manifesto from enforceable law/license.
- `Judicial-`: legal/privacy/evidence notice distinguishes allegations from adjudicated facts and flags public-data/secrecy risks.
- `myCat-iahelpsus`: upstream no-license risk explicitly documented.
- `RafGitTools` and `termux-api_rafcodephi`: complete GPLv3 text available as `COPYING`.
- `termux-app-rafacodephi`: protected-branch PR #449 proposes the same `COPYING` addition.

## Owner decisions that remain intentionally open

A repository can be lawful while having **no public reuse license**. What must
not happen is calling such a repository “MIT”, “GPL”, “open source”, or
commercially reusable without an express grant.

Owner license selection remains intentionally open for at least these
repository-wide scopes:

`androidRom`, `Espiritual-espirualidade`, `fcea-originum`, `Fisica`,
`GAIA-PDS-PHI`, `IaFcea`, `Judicial-`, `rafaelia-core-enterprise`,
`RAFNATIONS_CORE`, `RafPolimata`, `RAIAREIS_FRAMEWORK`, `Recipt`,
`TRABALHO_ROADMAP_AUDIT_GOV_DATA_ROTA_MAPwithCHAIN_security`, plus the
software scope of `templo-vivo-arcs` and software/file scopes not explicitly
licensed in `relativity-living-light`.

## Standards/legal references used as audit baseline

- Brazil, Lei 9.610/1998 — copyright framework:
  https://www.planalto.gov.br/ccivil_03/leis/l9610.htm
- Brazil, Lei 9.609/1998 — software intellectual-property regime:
  https://www.planalto.gov.br/ccivil_03/leis/l9609.htm
- Berne Convention, Article 5(2) — copyright protection is not conditioned on formalities:
  https://www.wipo.int/wipolex/en/text/283698
- SPDX License List — standardized license identifiers/text references:
  https://spdx.org/licenses/
- Creative Commons FAQ — CC licenses are not recommended for software; use software-specific licenses:
  https://creativecommons.org/faq/

## R3

`F_ok`: all 51 public repositories enumerated at account level; root/alternate
license surfaces and READMEs classified; material contradictions corrected;
third-party attribution preserved rather than overwritten.

`F_gap`: repository-level audit cannot prove file-by-file provenance,
compatibility of every dependency, trademark/patent clearance, privacy
compliance, or jurisdiction-specific enforceability. Several repos correctly
remain `TOKEN_VAZIO` pending owner license choice or provenance inventory.

`F_next`: merge protected PR #449 only after repository rules/checks permit;
then, for each `TOKEN_VAZIO` repository where public reuse is desired, perform
component inventory -> owner license decision -> SPDX/file notices ->
third-party compatibility check -> README alignment -> receipt.

---
Audit receipt: `PUBLIC-LEGAL-README-20260916`  
Mode: append-only correction; no upstream license replacement; no invented rights.
