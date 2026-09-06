# PBIP-L1-FED-V1 — Índice federado canônico

**Data:** 2026-09-06  
**Estado:** `PBIP_UNIT_EVIDENCE_OBSERVED_RUNTIME_PENDING`  
**claim_allowed:** `false`

## 1. Objeto

`PBIP-L1` identifica a ponte formal, sob domínio euclidiano declarado:

```math
q^2=r^2-d_\perp^2,
\qquad
\Delta_B=4(r^2-d_\perp^2)=4q^2.
```

O índice máquina-legível é `data/control-plane/PBIP_L1_FEDERATED_INDEX.v1.json`.

## 2. Autoridades e execução

| Papel | Autoridade/estado |
|---|---|
| derivação formal | `rafaelmeloreisnovo/Matem-tica-` PR #23 |
| geometria/toro/esfera/Poincaré | `rafaelmeloreisnovo/ChipQuantum` PR #68 |
| síntese acadêmica/claims | `rafaelmeloreisnovo/papers` PR #73 |
| RLL cosmológico | `instituto-Rafael/relativity-living-light` PR #832 — typed reference only |
| consumidor Android | `rafaelmeloreisnovo/Vectras-VM-Android` PR #1123 — PBIP unit consumer executed |
| consumidor kernel privado | `rafaelmeloreisnovo/Rafaelia_Private` PR #211 — implementation pending |
| custódia/evidência | `rafaelmeloreisnovo/RafPolimata` PR #329 — first receipt observed |
| relações/pins/estado | `rafaelmeloreisnovo/Mapa` PR #529 |

O Mapa **não** se torna autoridade das equações dos outros repositórios; ele conserva relações tipadas, refs imutáveis e estados de evidência.

## 3. Primeiro receipt executado

Consumidor observado:

```text
repo: rafaelmeloreisnovo/Vectras-VM-Android
commit: 836569a69c69b9b5d194108d0079a4a593b9f5d4
implementation: app/src/main/java/com/vectras/vm/core/PbipL1.java
implementation_sha256: 1119f44f78f6fe3e2abc3540414522106a92b3570b55cd20808ba147385055a9
test: app/src/test/java/com/vectras/vm/core/PbipL1Test.java
test_sha256: 2eb4f2d2ceeb587bcdfc19aec45ddfb220397bfdad5d5bb60864415bf2c8a6af
workflow: PBIP-L1 Evidence
run: 34025698586
job: 101466152645
conclusion: success
```

O gate dedicado executou os três vetores:

```text
r=5,d=3 -> q²=16,  ΔB=64  -> SECANT
r=5,d=5 -> q²=0,   ΔB=0   -> TANGENT
r=5,d=6 -> q²=-11, ΔB=-44 -> NO_REAL_INTERSECTION
```

Receipt/custódia:

```text
RafPolimata: evidence/pbip/PBIP_L1_CI_RECEIPT_20260906_RUN34025698586.v1.json
receipt_sha256: 2077b4674e263338da12d8d78a312744e01d2f3ba44561cfb61cb848aa551c6b
artifact_id: 9987007149
artifact_zip_sha256: 7c569d05c58bbbfd240d1263b7c40546a57ed58367d5facbeb7409469ef5130b
```

A primeira tentativa do gate falhou antes dos testes por ausência de CMake 3.22.1 e não emitiu receipt; a tentativa seguinte provisionou o componente canônico e fechou verde. Essa sequência é mantida como evidência fail-closed.

## 4. Cadeia atual

```text
FORMAL_MATH
  -> VECTRAS_IMPLEMENTATION
  -> PBIP_UNIT_TEST_EXECUTION
  -> PROVIDER_RECEIPT
  -> RAFPOLIMATA_CUSTODY
  -> MAPA_STATE
  -> ACADEMIC_LEDGER (sem promoção automática)
```

RLL continua lateralmente como `TYPED_REFERENCE_ONLY`; nenhuma seta permite inferir automaticamente dinâmica cosmológica, vorticidade física ou Conjectura de Poincaré.

## 5. Estado epistemológico

```text
SOURCE_OBSERVED=true
WIRED_DOCUMENTALLY=true
IMPLEMENTED_PBIP_CONSUMER=true
PBIP_UNIT_BUILD_PROVEN=true
UNIT_TEST_EXECUTION_PROVEN=true
PROVIDER_RECEIPT_OBSERVED=true
ARTIFACT_HASH_OBSERVED=true
BUILD_PROVEN=false
RUNTIME_PROVEN=false
DEVICE_PROVEN=false
REPRODUCED=false
CLAIM_ALLOWED=false
```

`PBIP_UNIT_BUILD_PROVEN` é deliberadamente mais estreito que `BUILD_PROVEN`/`ANDROID_RUNTIME_PROVEN`. Um JUnit verde não prova execução Android física.

## 6. Gate estrutural

```bash
python3 scripts/validate_pbip_l1_federated_index.py
```

O validador testa estrutura, pins, invariantes e bloqueio epistemológico. `PASS` nesse script prova apenas consistência do índice.

## 7. Gates ainda abertos

```text
TOKEN_VAZIO_POLY3_CANONICAL
TOKEN_VAZIO_PHYSICAL_VORTEX_MODEL
TOKEN_VAZIO_RLL_PBIP_PHYSICAL_BINDING
TOKEN_VAZIO_PRIVATE_PBIP_IMPLEMENTATION
TOKEN_VAZIO_PRIVATE_PBIP_RECEIPT
TOKEN_VAZIO_PBIP_INDEPENDENT_REPRODUCTION
TOKEN_VAZIO_PBIP_ANDROID_RUNTIME
TOKEN_VAZIO_PBIP_DEVICE_PROOF
```

O antigo `TOKEN_VAZIO_CI_BINDING_PBIP_L1` foi fechado pelo run `34025698586` e pelo receipt hash acima.

## 8. Não-regressão semântica

```text
TOKEN_VAZIO != 0
FORMULA != IMPLEMENTATION
IMPLEMENTATION != BUILD_PROVEN
PBIP_UNIT_BUILD_PROVEN != ANDROID_RUNTIME_PROVEN
BUILD_PROVEN != RUNTIME_PROVEN
RUNTIME_PROVEN != DEVICE_PROVEN
EVIDENCE != CLAIM
Poincare_return_map != Poincare_conjecture
H_RADIAL_30 != H_MAX_EQUILATERAL_MERIDIAN
```

## R3

- **F_ok:** implementação, teste dedicado, receipt provider, hashes e custódia RafPolimata foram observados e repinados.
- **F_gap:** reprodução independente, Android runtime, device proof, kernel privado, POLY3 e modelo físico de vórtice continuam abertos.
- **F_next:** reproduzir PBIP-L1 por implementação/provedor independente antes de ampliar claims; runtime Android/device é uma cadeia separada.
