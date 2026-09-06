# PBIP-L1-FED-V1 — Índice federado canônico

**Data:** 2026-09-06  
**Estado:** `PBIP_CROSS_IMPLEMENTATION_REPRODUCTION_PROVEN_PROVIDER_PENDING`  
**claim_allowed:** `false`

## 1. Objeto

`PBIP-L1` identifica, sob domínio euclidiano declarado:

```math
q^2=r^2-d_\perp^2,
\qquad
\Delta_B=4(r^2-d_\perp^2)=4q^2.
```

O índice máquina-legível é `data/control-plane/PBIP_L1_FEDERATED_INDEX.v1.json`.

## 2. Autoridades e produtores

| Papel | Autoridade/estado |
|---|---|
| derivação formal | `rafaelmeloreisnovo/Matem-tica-` PR #23 |
| geometria/toro/esfera/Poincaré | `rafaelmeloreisnovo/ChipQuantum` PR #68 |
| síntese acadêmica/claims | `rafaelmeloreisnovo/papers` PR #73 |
| RLL cosmológico | `instituto-Rafael/relativity-living-light` PR #832 — typed reference only |
| produtor A | `rafaelmeloreisnovo/Vectras-VM-Android` PR #1123 — Java/JUnit |
| produtor B | `rafaelmeloreisnovo/Rafaelia_Private` PRs #211/#212 — C11/Clang freestanding |
| custódia/comparação | `rafaelmeloreisnovo/RafPolimata` PRs #329/#330 |
| relações/pins/estado | `rafaelmeloreisnovo/Mapa` |

O Mapa conserva relações tipadas e evidência; não se torna autoridade das equações dos outros repositórios.

## 3. Produtor A — Vectras

```text
repo: rafaelmeloreisnovo/Vectras-VM-Android
commit: 836569a69c69b9b5d194108d0079a4a593b9f5d4
language/toolchain: Java / Gradle-JDK21
implementation_sha256: 1119f44f78f6fe3e2abc3540414522106a92b3570b55cd20808ba147385055a9
test_sha256: 2eb4f2d2ceeb587bcdfc19aec45ddfb220397bfdad5d5bb60864415bf2c8a6af
run: 34025698586
job: 101466152645
receipt_sha256: 2077b4674e263338da12d8d78a312744e01d2f3ba44561cfb61cb848aa551c6b
artifact_id: 9987007149
artifact_zip_sha256: 7c569d05c58bbbfd240d1263b7c40546a57ed58367d5facbeb7409469ef5130b
```

## 4. Produtor B — Rafaelia_Private

Segunda implementação, sem chamar o Java do Vectras:

```text
repo: rafaelmeloreisnovo/Rafaelia_Private
implementation_commit: d9bada8895f03805f3187e48cdadb3d435d5f5da
language/toolchain: C11 / Ubuntu Clang 18.1.3
implementation: src/pbip/pbip_l1_freestanding.c
implementation_sha256: 41f39d3f30b90237ae6f250976a3b5240aa822ba3f4a72052b4d31814ece791d
header_sha256: 7e957dc48ff82d04f962466872adb6c68e0222ae800ed3f5f207a80700e15108
test_sha256: 11b3499acf37ad2b734e1c9ecd1ba731267f57f88c873f496ac20649e78c8d4c
object_sha256: 14b8b5e8580dce137af3af4674c62f0d21a93652752af5455d2204950cd02597
stdout_sha256: 804cc3e8b4b84dde2547eef530fe0bd7d672ce50e7e63bcffccb6aa86d94824f
undefined_external_symbols: 0
run: 34026460668
job: 101468184710
receipt_sha256: e1b562b2ee719b93e2f9d5326c06943a5a052b873a259ce0b685a3fe18a00c2b
artifact_id: 9987206552
artifact_zip_sha256: 0240db4d06925daaee604811d24c87a80ec3dad62f5b70c30cb6f32e09c84e89
```

O núcleo foi compilado com:

```text
-ffreestanding -fno-builtin -fno-stack-protector
```

O gate exigiu `nm -u = ∅` antes de executar o observador C11 hospedado.

## 5. Reprodução cruzada

Os dois produtores calcularam independentemente:

```text
r=5,d=3 -> q²=16,  ΔB=64  -> SECANT
r=5,d=5 -> q²=0,   ΔB=0   -> TANGENT
r=5,d=6 -> q²=-11, ΔB=-44 -> NO_REAL_INTERSECTION
```

RafPolimata registra a comparação em:

```text
evidence/pbip/PBIP_L1_CROSS_IMPLEMENTATION_REPRODUCTION_20260906.v1.json
```

A comparação fechou:

```text
INDEPENDENT_REPOSITORY=true
INDEPENDENT_IMPLEMENTATION=true
INDEPENDENT_LANGUAGE=true
INDEPENDENT_TOOLCHAIN=true
CROSS_IMPLEMENTATION_REPRODUCTION_PROVEN=true
```

Mas **não** fechou independência de provedor, porque ambos os runs ocorreram em GitHub Actions:

```text
INDEPENDENT_CI_PROVIDER=false
PROVIDER_INDEPENDENT_REPRODUCTION_PROVEN=false
ANDROID_RUNTIME_PROVEN=false
DEVICE_PROVEN=false
```

Assim:

```text
CROSS_IMPLEMENTATION_REPRODUCTION != PROVIDER_INDEPENDENT_REPRODUCTION
INDEPENDENT_TOOLCHAIN != INDEPENDENT_CI_PROVIDER
```

## 6. Cadeia atual

```text
FORMAL_MATH
  -> VECTRAS/JAVA EXECUTION + RECEIPT
  -> PRIVATE/C11 FREESTANDING EXECUTION + RECEIPT
  -> RAFPOLIMATA CROSS-COMPARISON
  -> MAPA FEDERATED STATE
  -> ACADEMIC_LEDGER (sem promoção automática)
```

RLL permanece `TYPED_REFERENCE_ONLY`; nada nessa cadeia prova vorticidade física, dinâmica cosmológica ou a Conjectura de Poincaré.

## 7. Estado epistemológico

```text
SOURCE_OBSERVED=true
WIRED_DOCUMENTALLY=true
IMPLEMENTED_PBIP_CONSUMER=true
PBIP_UNIT_BUILD_PROVEN=true
UNIT_TEST_EXECUTION_PROVEN=true
PROVIDER_RECEIPT_OBSERVED=true
PRIVATE_FREESTANDING_CORE_PROVEN=true
PRIVATE_UNIT_EXECUTION_PROVEN=true
CROSS_IMPLEMENTATION_REPRODUCTION_PROVEN=true
INDEPENDENT_REPOSITORY=true
INDEPENDENT_IMPLEMENTATION=true
INDEPENDENT_LANGUAGE=true
INDEPENDENT_TOOLCHAIN=true
INDEPENDENT_CI_PROVIDER=false
BUILD_PROVEN=false
RUNTIME_PROVEN=false
DEVICE_PROVEN=false
REPRODUCED=false
CLAIM_ALLOWED=false
```

`REPRODUCED=false` continua reservado ao gate mais forte de reprodução por provedor/ambiente realmente independente; a reprodução cruzada de implementação tem campo próprio.

## 8. Gate estrutural

```bash
python3 scripts/validate_pbip_l1_federated_index.py
```

O validador exige pins SHA-40, hashes SHA-256, execução/receipt dos dois produtores, objeto Private sem símbolos externos e a permanência do gate de provedor independente. `PASS` prova consistência/custódia do índice, não runtime Android físico.

## 9. Gates ainda abertos

```text
TOKEN_VAZIO_POLY3_CANONICAL
TOKEN_VAZIO_PHYSICAL_VORTEX_MODEL
TOKEN_VAZIO_RLL_PBIP_PHYSICAL_BINDING
TOKEN_VAZIO_PBIP_PROVIDER_INDEPENDENT_REPRODUCTION
TOKEN_VAZIO_PBIP_ANDROID_RUNTIME
TOKEN_VAZIO_PBIP_DEVICE_PROOF
```

Fechados por evidência: `TOKEN_VAZIO_CI_BINDING_PBIP_L1`, `TOKEN_VAZIO_PRIVATE_PBIP_IMPLEMENTATION`, `TOKEN_VAZIO_PRIVATE_PBIP_RECEIPT` e o antigo gate genérico de reprodução de implementação.

## R3

- **F_ok:** dois repositórios, duas implementações, duas linguagens/toolchains e dois receipts reproduzem os mesmos três vetores; RafPolimata validou a comparação.
- **F_gap:** provedor independente, Android runtime, device proof, POLY3 e modelo físico continuam abertos.
- **F_next:** executar o mesmo contrato em um provedor realmente separado — idealmente Termux/dispositivo — e ingerir receipt/hashes sem reutilizar GitHub Actions como executor.
