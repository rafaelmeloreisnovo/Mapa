# PBIP-L1-FED-V1 — Índice federado canônico

**Data:** 2026-09-06  
**Estado:** `WIRED_DOCUMENTALLY_EVIDENCE_PENDING`  
**claim_allowed:** `false`

## 1. Objeto

`PBIP-L1` identifica a ponte formal, sob domínio euclidiano declarado:

```math
q^2=r^2-d_\perp^2,
\qquad
\Delta_B=4(r^2-d_\perp^2)=4q^2.
```

O índice máquina-legível é `data/control-plane/PBIP_L1_FEDERATED_INDEX.v1.json`.

## 2. Autoridades

| Papel | Autoridade |
|---|---|
| derivação formal | `rafaelmeloreisnovo/Matem-tica-` PR #23 |
| geometria/toro/esfera/Poincaré | `rafaelmeloreisnovo/ChipQuantum` PR #68 |
| síntese acadêmica/claims | `rafaelmeloreisnovo/papers` PR #73 |
| RLL cosmológico | `instituto-Rafael/relativity-living-light` |
| consumidor Android | `rafaelmeloreisnovo/Vectras-VM-Android` |
| consumidor kernel privado | `rafaelmeloreisnovo/Rafaelia_Private` |
| rota de evidência | `rafaelmeloreisnovo/RafPolimata` |
| relações/pins/estado | `rafaelmeloreisnovo/Mapa` |

O Mapa **não** se torna autoridade das equações dos outros repositórios; ele conserva relações tipadas e refs imutáveis.

## 3. Cadeia

```text
FORMAL_MATH
  -> GEOMETRY_REFERENCE
  -> CONSUMER_BINDINGS
  -> EVIDENCE_ROUTE
  -> ACADEMIC_LEDGER
```

RLL entra lateralmente como `TYPED_REFERENCE_ONLY`; nenhuma seta permite inferir automaticamente dinâmica cosmológica ou vorticidade física.

## 4. Gate estrutural

```bash
python3 scripts/validate_pbip_l1_federated_index.py
```

O validador testa estrutura, pins, invariantes e bloqueio epistemológico. `PASS` nesse script prova apenas consistência do índice — não build/runtime/device/reprodução dos consumidores.

## 5. Gates preservados

```text
TOKEN_VAZIO_CI_BINDING_PBIP_L1
TOKEN_VAZIO_POLY3_CANONICAL
TOKEN_VAZIO_PHYSICAL_VORTEX_MODEL
TOKEN_VAZIO_RLL_PBIP_PHYSICAL_BINDING
TOKEN_VAZIO_PRIVATE_PBIP_IMPLEMENTATION
TOKEN_VAZIO_PRIVATE_PBIP_RECEIPT
```

## 6. Não-regressão semântica

```text
TOKEN_VAZIO != 0
FORMULA != IMPLEMENTATION
IMPLEMENTATION != BUILD_PROVEN
BUILD_PROVEN != RUNTIME_PROVEN
RUNTIME_PROVEN != DEVICE_PROVEN
EVIDENCE != CLAIM
Poincare_return_map != Poincare_conjecture
H_RADIAL_30 != H_MAX_EQUILATERAL_MERIDIAN
```

## R3

- **F_ok:** fórmula, autoridades, consumidores, evidência e ledger foram federados por ID e commit.
- **F_gap:** implementação PBIP consumível e receipt de execução continuam abertos.
- **F_next:** executar o gate estrutural em CI e depois preencher um receipt real do primeiro consumidor.
