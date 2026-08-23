# Receipt — RAFAELIA Activation Registry V1 — 2026-08-23

**Receipt ID:** `EVD:RECEIPT:ACTIVATION_REGISTRY_V1:20260823`  
**Repository:** `rafaelmeloreisnovo/Mapa`  
**Base:** `main@398c3955a60425cd9f6ba031b5a104152eeeac41`  
**Head branch:** `rafaelia/activation-registry-v1-20260823`  
**State:** `IMPLEMENTED_PROPOSED`  
**Claim ceiling:** `REFERENCE` until applicable CI/schema/gate evidence is observed.

## Objective

Materialize one subordinate, machine-readable activation registry that preserves the existing Mapa/Drive authority split and makes activation edges auditable as:

`component → condition → input → gate → output → TOKEN_VAZIO fallback`.

## Sources read before mutation

- `bootstrap/RAFAELIA_CHATGPT_BOOTSTRAP_V1.md`
- `governance/AUTHORITY_MATRIX_V1.yaml`
- `docs/OMEGA_ACTIVATE_ROUTING_V1.md`
- `navigation/INDEX.md`
- `navigation/RAFAELIA_MASTER_REGISTRY.v1.json`
- `SRC:DRIVE:1LgwvPnYNewcnaD78oADywxRtPhspFKJqDZFURzgVkI8` — Ω-ACTIVATE longitudinal plan
- `SRC:DRIVE:1x_5x3_NdSaHtPLF9hbu8M1i0kvza_MnhtWeZycav19Y` — Master Navigation Registry V1
- `SRC:DRIVE:1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88` — Implementação Latentes e Papers — Drive GitHub V1

## Delta

Commits observed before this receipt:

- `c9db6439853a547327df5148b3816e685c12e659` — add `governance/ACTIVATION_REGISTRY_V1.json`
- `fd3ae3f96f6f1a4ecf05ff5bba318d5057676774` — add `docs/ACTIVATION_REGISTRY_V1.md`
- `66ee5fa6a38a4dd04e0830a9e168747ed5e067c3` — bind Activation Registry into `navigation/INDEX.md`
- `dc88e0a31f420c54a28a604ae18f3e18384f0b09` — bind Activation Registry into `navigation/RAFAELIA_MASTER_REGISTRY.v1.json`

Pre-receipt compare result:

- ahead by: `4`
- behind by: `0`
- files changed: `4`
- `docs/ACTIVATION_REGISTRY_V1.md`: added
- `governance/ACTIVATION_REGISTRY_V1.json`: added
- `navigation/INDEX.md`: modified
- `navigation/RAFAELIA_MASTER_REGISTRY.v1.json`: modified

## Evidence / checks

- The machine registry was fetched successfully from the head branch after creation.
- The updated master machine registry was fetched successfully from the head branch after mutation.
- The raw GitHub URL for `governance/ACTIVATION_REGISTRY_V1.json` resolved successfully.
- No CI/schema run is claimed by this receipt.
- No merge to `main` is claimed by this receipt.

## Invariants preserved

- `MASCOTE != AGENTE != AUTORIDADE != EXECUTOR`
- `VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`
- `TOKEN_VAZIO != PASS`
- Drive remains longitudinal navigation authority.
- Mapa remains federated control/navigation plane.
- The new registry is subordinate and does not create a competing master registry.

## TOKEN_VAZIO / open gap

### `GAP:ACTIVATION_MASTER_NAV_POINTER_DRIFT`

Observed: Drive Master Navigation Registry references `Mapa/docs/RAFAELIA_MASTER_NAV_REGISTRY_V1.md`, but that path was not found on observed `main`. Current GitHub navigation artifacts are under `navigation/`.

**State:** `ABERTO`  
**Priority:** `P1`  
**Action:** reconcile the Drive pointer only through explicit append-only provenance.  
**Exit criterion:** the Drive pointer resolves to the current canonical GitHub navigation artifact and the reconciliation has its own receipt.

## R3

- `F_ok`: Activation Registry exists in machine + human form and is indexed in the branch.
- `F_gap`: CI/schema validation, merge promotion, runtime enforcement, and Drive pointer reconciliation are not yet evidenced.
- `F_next`: open PR; observe checks; promote only according to gate; then perform append-only Drive pointer reconciliation.
