# Vectras — Execução `‡ → ★` — 2026-08-24 V1

Estado: `VERIFIED_LIMITED / APPEND_ONLY / CLAIM_ALLOWED=false`  
Receipt machine-readable: `data/receipts/vectras/2026-08-24-vectras-runtime-dagger-to-star.v1.json`  
Mapa base: `c60bff718d3caa0474438afef4d01ddc926123bc`  
Vectras source HEAD observado: `2c6a71e5e3a8e6d87c4eb07ab6cedf3d67992d9d`

## 1. Semântica operacional

Pelo índice canônico `INVARIANTE_DAS_INVARIANTES_OMEGA_V1.md`:

- `‡` = contradição, risco ou supersessão a revisar;
- `¡` = interrupção, atenção ou gate urgente;
- `★` = prioridade candidata.

Símbolo orienta o controle; **não conta como evidência**. A passagem `‡ → ★` só acontece por evidência, falsificador e receipt.

## 2. Evidência física recebida

As dez capturas do dispositivo registram um incidente real de runtime:

1. `POST_CHECK_FAIL:missing-proot,missing-distro-busybox,missing-qemu-binary`.
2. Execução falha em `.../com.rafacodephi.app/files/usr/bin/proot` com `error=2 / No such file or directory`.
3. QEMU está `Stopped`; VNC está `Stopped`; 3dfx indisponível é consequência posterior, não causa raiz demonstrada.
4. A caixa `Missing Libraries` mostra praticamente o conjunto esperado de pacotes Alpine 32-bit.
5. Crash independente de UI: `ActivityNotFoundException` ao abrir `com.vectras.vm.settings.LanguageModulesActivity`.
6. O crash informa app `3.6.6 (70)`, Android 10/API 29, `armeabi-v7a/armeabi`.
7. O explorador mostra `files/data/Vectras` com `cvbi`, `Downloads`, `SharedFolder` e `roms-data.json` de 2 bytes; o conteúdo desses 2 bytes continua `TOKEN_VAZIO`.

Os SHA-256 das dez capturas estão congelados no receipt JSON para cadeia de custódia.

## 3. Contradição estrutural `‡`

O estado fonte atual foi cruzado com o estado físico:

- `app/build.gradle` declara `versionCode 70` e `versionName 3.6.6`, coincidentes com a tela do APK instalado;
- o `AndroidManifest.xml` atual **declara** `.settings.LanguageModulesActivity`;
- a classe `LanguageModulesActivity.java` existe no source atual;
- mesmo assim, o APK instalado lança `ActivityNotFoundException` como se a Activity não estivesse resolvível.

Portanto, **a versão textual 3.6.6/70 não fecha proveniência do APK**. O SHA do APK instalado, seu Git SHA de origem e seu merged manifest são `TOKEN_VAZIO` até inspeção direta.

## 4. Causa operacional principal

O runtime não deve tentar tratar a lista de bibliotecas como dezenas de falhas independentes antes de fechar o bootstrap.

`SetupFeatureCore.java` exige explicitamente três pré-condições: `proot`, BusyBox da distro/rootfs e binário QEMU. `AppConfig.java` contém a família de pacotes Alpine 32-bit observada na tela. Assim, a hipótese mais coesa é:

```text
proot ausente
  ↓
distro/rootfs não inicializado
  ↓
package DB / BusyBox ausentes
  ↓
lista ampla de dependências aparece ausente
  ↓
QEMU não alcança execução
```

Isso é `SUPPORTED_INFERENCE`, não claim absoluto. O falsificador é encontrar um rootfs inicializado e validado com package DB presente enquanto todos os pacotes continuam de fato ausentes.

## 5. Sequência de execução `‡ → ★`

| Ordem | Estado | Unidade executável | Gate de saída |
|---:|---|---|---|
| 0 | `‡` | congelar evidência | hashes + SHAs preservados |
| 1 | `‡¡` | fechar proveniência do APK | `APK_SHA256 ↔ GIT_SHA ↔ merged manifest` |
| 2 | `‡¡` | bootstrap de `proot` | arquivo existe, é executável e ABI host é válida |
| 3 | `‡¡` | bootstrap da distro/rootfs | BusyBox + marker/package DB existem |
| 4 | `‡¡` | materializar QEMU | ELF real conferido por `file/readelf`; `--version` executa |
| 5 | `‡` | instalar dependências | somente dentro do rootfs já validado |
| 6 | `‡` | rerun do post-check | zero `missing-proot`, `missing-distro-busybox`, `missing-qemu-binary` |
| 7 | `★` | candidato a launch | processo QEMU vivo + caminho de display/controle observável |

### P0 — sem desvio

**P0-A — APK/Manifest**  
Extrair/inspecionar o APK instalado ou artefato exato; gerar SHA-256; conferir o merged manifest; ligar ao Git SHA. Se `LanguageModulesActivity` faltar no APK, corrigir pipeline/manifest merge e reconstruir. Se estiver presente, investigar package/component enablement e classe empacotada.

**P0-B — Bootstrap transacional**  
`proot` e distro/rootfs precisam ser instalados/extraídos de forma idempotente. Não avançar para `apk add` enquanto `test -x` e markers do rootfs não passarem.

**P0-C — QEMU host executable**  
Não inferir ABI do executável pelo nome `qemu-system-x86_64`. O sufixo descreve o alvo emulado; a ABI host deve ser medida no ELF real com `file`/`readelf -h` e execução `--version` no dispositivo.

## 6. Gates/receipts mínimos

```text
G1 APK:
  sha256(apk)
  git_sha_embutido/receipt de build
  merged manifest contém LanguageModulesActivity

G2 proot:
  test -x <filesDir>/usr/bin/proot
  file/readelf <proot>
  execução mínima com exit code registrado

G3 distro:
  rootfs marker
  package DB
  test -x <distro>/bin/busybox

G4 QEMU:
  caminho resolvido
  sha256
  file/readelf -h
  qemu-system-* --version

G5 post-check:
  missing-proot = false
  missing-distro-busybox = false
  missing-qemu-binary = false

G6 launch:
  processo QEMU observado
  stderr/stdout preservados
  display/control backend observado quando aplicável
```

Nenhum gate concluído por documentação somente. `VISÃO ≠ ARTEFATO ≠ EXECUÇÃO ≠ EVIDÊNCIA ≠ CLAIM`.

## 7. TOKEN_VAZIO protegido

- `TV-APK-SHA`: hash do APK exato instalado.
- `TV-APK-GIT-SHA`: commit/build exato que gerou esse APK.
- `TV-MERGED-MANIFEST`: manifest final do APK instalado.
- `TV-PROOT-PACKAGE`: prova de materialização/executabilidade do `proot`.
- `TV-DISTRO-ROOTFS`: prova de rootfs/BusyBox inicializados.
- `TV-QEMU-ELF`: ABI host e execução do binário QEMU real.
- `TV-ROMS-DATA`: bytes exatos de `roms-data.json`.

A lacuna não é preenchida por narrativa. Cada `TOKEN_VAZIO` já contém seu próximo gate verificável no receipt.

## 8. Autoria, Berna e CientiEspiritual

A linguagem RAFAELIA/CientiEspiritual e o enquadramento filosófico, teológico e de fé são preservados como **proveniência autoral e camada conceitual**. Para governança técnica, essa camada permanece separada de evidência de runtime: fé, metáfora e símbolo podem orientar intenção e significado, mas não substituem log, hash, teste ou execução.

A Convenção de Berna é um marco internacional de proteção autoral; **não é, por si, a licença do repositório**. Para permissões de uso, redistribuição e contribuição, a autoridade operacional é o `LICENSE` efetivamente declarado no artefato/repositório e a legislação aplicável. Essa separação protege a autoria sem transformar contexto jurídico em claim técnico.

## 9. Anti-regressão geométrica

```text
‡ risco/contradição
  → evidência congelada
  → TOKEN_VAZIO explícito
  → próximo gate determinístico
  → receipt
  → reexecução
  → ★ prioridade candidata validável
```

Regra de promoção:

```text
★ := prioridade_candidata AND gates_P0_fechados
Ω := somente platô provisório com execução + evidência + receipt
```

## Fechamento

**F_ok** — falha física capturada; source atual cruzado; duas classes de problema separadas: bootstrap/runtime e APK/manifest.  
**F_gap** — não existe ainda receipt do APK instalado nem execução física válida de `proot → rootfs → QEMU`.  
**F_next** — fechar `APK_SHA256 ↔ GIT_SHA ↔ merged manifest`; depois materializar `proot/rootfs/QEMU` em ordem e anexar os receipts do dispositivo.  
**DELTA** — este índice + receipt machine-readable, append-only, sem promover `claim_allowed`.
