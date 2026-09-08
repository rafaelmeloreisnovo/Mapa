# RAFAELIA CASA41 — SYSTEM_MAP V1

Status: `SOURCE_CONTRACT_IMPLEMENTED / PROVIDER_ENFORCEMENT_PARTIAL`

This subtree materializes **41 physical knowledge-house folders**, **7 navigation directions**, virtual drive-letter mappings inspired by Novell NetWare `MAP/RIGHTS`, and a dBASE III `.DBF` route table.

It does **not** claim NetWare wire compatibility or a native dBASE `.MDX` engine.

## Invariants

- `DATASET != MISSION_AUTHORITY`
- `ROUTE != RIGHT`
- `INDEX != EVIDENCE`
- `PHOTO_OBJECT != SHARE_OBJECT`
- `APPEND_ONLY_INTENT != PROVIDER_ENFORCEMENT`
- `TOKEN_VAZIO != 0`
- `SOURCE != ARTEFACT != EXECUTION != EVIDENCE != CLAIM`

## 41 folders

The supplied list had 29 entries but 28 unique names because `Temas` occurred twice. The physical filesystem keeps one `11_temas/` folder and preserves two logical views: `TEMAS_PRIMARY` and `TEMAS_SECONDARY`.

The remaining 13 physical folders close the operational system: `Compartilhado`, `Governança`, `Permissões`, `Índices`, `Rotas`, `Mapas`, `Auditoria`, `Cadeia_de_Custódia`, `Receipts`, `Fotos`, `Serviços`, `Grupos_Timeline`, `Privacidade`.

Physical names are ASCII-safe for Android/Git/legacy portability; UTF-8 display labels remain in `SYSTEM_MAP.json`.

## Seven directions and XYZ/360°

The signed Cartesian directions are:

`X+`, `X-`, `Y+`, `Y-`, `Z+`, `Z-`.

The seventh entry, `OMEGA360`, is a rotation/origin navigation operator:

`Rz(gamma) * Ry(beta) * Rx(alpha)` with each angle modulo 360 degrees.

It is **not** claimed as a fourth independent Euclidean spatial axis. Its purpose is to rotate/navigation-project the X/Y/Z frame through all orientations while preserving the geometry invariants declared in `DIRECTIONS_7.json`.

## NetWare-inspired MAP and RIGHTS layer

`ROUTES.json` defines virtual letter views such as:

- `M:` root house
- `S:` shared governed surface
- `K:` memory
- `D:` dataset
- `P:` programs
- `T:` work
- `R:` routes
- `I:` indexes
- `G:` governance
- `A:` audit
- `C:` custody
- `F:` photos
- `V:` privacy
- `X:/Y:/Z:` axis views
- `O:` OMEGA360

Search routes `S1..S5` provide script/program/route/index lookup semantics.

`SYSTEM_RIGHTS.json` preserves the familiar letters `S/R/W/C/E/M/F/A/N` as a semantic vocabulary, then places new RAFAELIA profiles over them. Provider ACL enforcement remains a separate gate.

## dBASE-inspired route table

- `SYSTEM_MAP.DBF`: dBASE III route table with 41 records.
- `SYSTEM_MAP.IDX`: deterministic textual route index; **not** native dBASE MDX.
- `SYSTEM_MAP.MDX.SPEC.json`: intended production-index tags; native binary MDX remains `TOKEN_VAZIO_NATIVE_MDX_BINARY` until generated and read back by a compatible engine.

## House / doors / service workflow

The workflow is:

`capture reference -> classify privacy -> resolve route -> check rights -> open governed door -> execute service -> verify -> append receipt -> update knowledge -> optional explicit share`.

A photo can therefore act as a **reference that opens a work route** (for example a luxury-car service procedure), but the photo itself does not grant rights and is not automatically published.

## Sharing and privacy

`29_compartilhado/` is the explicit share surface. Sharing is deny-by-default and requires destination, privacy classification, rights check and receipt.

Raw private photos, private memory, datasets, audit and custody material are never auto-shared by this contract.

## Mobile/GitHub boundary

`APP_CONTRACT.json` defines the intended Android-local + GitHub-provider responsibilities. GitHub credentials must never be stored in this repository. Authenticated GitHub writes, Android storage access, photo permissions and provider ACL enforcement remain `TOKEN_VAZIO` until physically bound and tested.

## Commands

```bash
python3 system_map.py folders
python3 system_map.py maps
python3 system_map.py directions
python3 system_map.py resolve S:
python3 system_map.py resolve F38
python3 system_map.py rights APPEND_ONLY_WRITER
python3 validate_casa41.py
```

`SYSTEM_MAP.COM` is only a small valid DOS `.COM` informational shim. It does not mount NetWare volumes and does not modify provider ACLs.
