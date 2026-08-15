# RAFAELIA — APK/Histórico — Mapa Operacional de Receipt V1

**Estado:** `VERIFIED_LIMITED_STATIC` (síntese documental)  
**Claim gate:** `claim_allowed=false`  
**Política:** `APPEND_ONLY / FAIL_CLOSED / PRIVATE_DEFAULT_DENY`  
**Escopo:** identidade, custódia, integridade estrutural, execução, índice e próximos gates do bundle APK/histórico.

> Este mapa não recalcula bytes nem executa o APK. Ele consolida receipts imutáveis lidos nesta sessão e preserva explicitamente o que ainda precisa de prova física.

## 1. Invariantes operacionais

```text
IDENTIDADE != PROVENIÊNCIA != BUILD != EXECUÇÃO != EVIDÊNCIA != CLAIM
DERIVED_SHARD_ORDINAL != RAW_SOURCE_ORDINAL
TOKEN_VAZIO é estado válido; nunca é preenchido por inferência.
Correção é sucessor append-only; não reescrita de estado histórico.
```

## 2. Âncoras de autoridade e custódia

| Papel | Âncora imutável |
|---|---|
| Receipt estático APK/ZIP | `rafaelmeloreisnovo/termux-app-rafacodephi` — commit `48056015bcfde4c9e70bdd46b22f00d3493adb66` — `data/evidence/upload_artifact_audit_20260814.v1.json` |
| Nota técnica correlata | Mesmo commit — `docs/audit/2026-08-14/UPLOAD_ARTIFACT_AUDIT.md` |
| Custódia RAW019–027 | `rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE` — commit `b343cac4636f1d100e1ff63d6cc081ffe96411c7` — `auditoria/RAFAELIA_RAW_CONVERSATIONS_019_027_PROVIDER_SHA_CLOSURE_20260814.md` |
| Navegação longitudinal | Protocolo de Catalogação Evolutiva Contínua V1 — checkpoint `0073` e sucessores; `RAW018` permanece separado de `RAW019–027` |

## 3. Artefatos principais registrados como verificados

| Artefato | Bytes | SHA-256 | Limite factual |
|---|---:|---|---|
| `com.termux_1002 (1).apk` | 113880067 | `e6265a57eb5ca363808488e3b01955958bed93bc0c8a0d281849b363b11027ec` | `package=com.termux`, `versionName=0.118.3`, ABIs `arm64-v8a`, `armeabi-v7a`, `x86`, `x86_64`; assinatura JAR/v1 FDroid registrada; inspeção estática, sem instalação/execução. |
| `d6e9db90fbd5ffb1158e68518e6f46005d1c78dbaef56427bb8a934c8f466c0a-2025-10-06-21-49-49-edd15254776a4346b05570a99e6d418f.zip` | 305843744 | `53fbfbc52d110d5815024ca851868555d23c3180cd73bb5433dd5f5bade9d93f` | 5 entradas; 1607970090 bytes descomprimidos; `ZipFile.testzip()=None`; sem ZIP-slip, symlink, criptografia ou nomes duplicados. |

### 3.1 Conteúdo estrutural do ZIP histórico

- Entradas: `user.json`, `conversations.json`, `message_feedback.json`, `shared_conversations.json`, `chat.html`.
- `conversations.json`: 792693581 bytes; `chat.html`: 815263242 bytes; `shared_conversations.json`: 72 registros.
- O prefixo `d6e9db...` do nome do ZIP **não é** o SHA-256 observado: `TV-ZIP-01 / TOKEN_VAZIO_FILENAME_HASH_SEMANTICS`.
- O corpus pessoal não é commitado; somente identidade, contagens e receipts sanitizados.

## 4. Custódia atual RAW019–027

Todos os itens abaixo estão registrados no receipt imutável como provider-bound, byte-bound, SHA-256-bound e JSON `PASS`, com 100 objetos de conversa cada.

| Raw source | Provider ID | Bytes | SHA-256 |
|---|---|---:|---|
| `conversations-019.json` | `1cDWWp9vmRfOXp3nca6le1feiPkk0-vvW` | 16440670 | `f90bfc11a9088772570c1f81503c1bedcc9bd475c5435ce809d62812ff351436` |
| `conversations-020.json` | `17hlRdf8JtH6An3gIDDVdfTlpRRPTLGDq` | 13424077 | `32ad3e5f02f06353280fb41fbb6a320b3cb9e42c841105b95674a6a386d8b6c3` |
| `conversations-021.json` | `122bngAutdV8Ru_UnXl-LdYVTbq5QoDP3` | 21426196 | `3fbbba45decd84af923884a1a2cc27d1dfecb884938624b73da73d6dfbe41aff` |
| `conversations-022.json` | `17DVZDmc85ZhnoAP-a7_MOJfH14EbaToP` | 20765905 | `16e55d060d15adde35759ab5ae073a90a7627334c44cdb9c5ee4e2ca19ca9c8c` |
| `conversations-023.json` | `1ElCvaZs25h7UyyPdorUiJwuaBLUx_uXn` | 22099004 | `71700f23655850dca7523054f832406bee3645f73c4885a90b8915cd5e47d236` |
| `conversations-024.json` | `11W_TWthT0He-4SkzVWi0AiJQ_Uffjk7b` | 17872078 | `18d4a8e3931f6820e8a635748c02ce1677d23f90903278d2e60e5b20548c24d8` |
| `conversations-025.json` | `1QF2kAxgcgGP39uHOkB0KleMMgFC13ZTt` | 16086399 | `bb9256b040a16be081d4a601a2ab6e185fa99a404615761c5995d1f0177cbbac` |
| `conversations-026.json` | `1nWS0zUfFgXRfrjg37FrREh_mPJcUL-BW` | 12815159 | `2daafaa7652a12269cb3a10816eeec78b5e9843b1caee4736b40c68e8648335d` |
| `conversations-027.json` | `1i02ona4EPpUszTWXAHnfoUqFGSUJgsPV` | 4098254 | `32ecf289497a30799358ac53a794c2d198e8449592a28a19bb9bbab6ff254211` |

**Agregado fechado:** 145027742 bytes; 900 objetos; `JSON_PARSE=9/9 PASS`.

## 5. Quarentena: lote parcial que não pode substituir o bundle íntegro

`01-com.termux_1002-1-.apk` (103628800 bytes) e `02-...zip` (305266688 bytes) pertencem ao lote unificado parcial, sem central directory/EOCD. O primeiro truncou em `lib/x86_64/libtermux-bootstrap.so`; o segundo em `chat.html`, com ao menos 576722 bytes de payload ausentes.

Há divergência interna entre `artifacts[].sha256` e `partial_container_forensics.sha256` nesse manifesto:

| Objeto parcial | Hash de inventário | Hash forense | Estado correto |
|---|---|---|---|
| APK parcial | `cb439fdd205d138df1bd4ad205c05cc801206b1598e24f69ab1bd2736a1baf76` | `cb439fdd9362c42b70c5afcdfec6636095164f60d2c95e80f795952b3a0baf76` | `TOKEN_VAZIO_UNIFIED_BATCH_HASH_FIELD_RECONCILIATION` |
| ZIP parcial | `ec8f86a8992104ee9432129aa8b65eca2cc6891621b197b7a6fa4ee2c0ded047` | `ec8f86a8e7daf4d1c83b2f94402619882147da15e8be1cb921246df0dded047` | `TOKEN_VAZIO_UNIFIED_BATCH_HASH_FIELD_RECONCILIATION` |

**Regra:** não usar qualquer um desses valores como substituto dos hashes do bundle íntegro; reexportar e recalcular do byte físico antes de nova associação.

## 6. Topologia operacional em camadas e janelas

| Camada | Nó / material | Estado | Relação permitida | Próxima prova |
|---|---|---|---|---|
| L1 — Custódia | APK baseline | Documentado + estático | hash ↔ bytes ↔ manifest | hash de cópia histórica e commit produtor |
| L2 — Integridade | ZIP histórico | CRC/decompressão PASS | ZIP ↔ entradas ↔ escopo temporal | semântica do prefixo do nome |
| L3 — Raw atual | RAW019–027 | 9/9 fechado | provider ↔ bytes ↔ SHA ↔ JSON | join ao output de V2 |
| L4 — Lacuna crítica | RAW018 | tamanho histórico apenas | não inferir de ordinal/derivado | provider atual + bytes + SHA + JSON |
| L5 — Runtime | execução V2 / Android | não provada | build ≠ execução | runner, argv, logs, outputs |
| L6 — Derivação | RAW → MESSAGES/NODES | não vinculada | raw ≠ derived sem receipt | source_pointer + transform receipt |
| L7 — Governança | Drive ↔ Mapa ↔ GitHub | append-only | índice ↔ receipt ↔ sucessor | readback, predecessor e hash |

## 7. Mapa de urgência e gates Six Sigma

### P0 — não promover sem fechar

1. `TV-APK-01 historical_sha256`: localizar o APK histórico de 2025 e comparar SHA-256 com o baseline atual.
2. `TV-APK-02 exact_source_commit`: fixar commit, recipe de build, Gradle/NDK/JDK, signer e hashes de bootstrap.
3. `TV-APK-03 v2_v3_signing_verification`: executar `apksigner verify --verbose --print-certs`; registrar cobertura v1/v2/v3/v4.
4. `TV-APK-04 physical_runtime_behavior`: instalar e executar em Android isolado, com aparelho/ABI/Android, comando, exit code, stdout/stderr e logs.
5. `RAW018_CURRENT_PROVIDER`, `RAW018_CURRENT_BYTES`, `RAW018_SHA256`, `RAW018_JSON_VALIDITY`: recuperar o objeto bruto por path/container/provider histórico, nunca pelo ordinal derivado.
6. `OFFICIAL_V2_EXECUTION_RECEIPT`: executar contra manifesto de entrada hash-bound e capturar receipt completo.

### P1 — fecha coerência transversal

1. `RAW019_027_TO_OFFICIAL_V2_OUTPUT_RECEIPT`: ligar entradas, execução e outputs por hashes.
2. `RAW_TO_DERIVED_TRANSFORM_RECEIPT`: materializar relações `source_pointer` e transformação para MESSAGES/NODES.
3. `CROSS_EXPORT_IDENTITY_JOIN`: não rebinding silencioso entre o ZIP histórico e RAW000–050; usar interseção exata de IDs pseudonimizados somente quando a fonte atual estiver disponível.
4. `TV-CI-01 runner_startup_cause`: sete workflows com zero steps não são falha de conteúdo; registrar causa de startup ou um rerun observável.

### P2 — melhora rastreabilidade sem bloquear a identidade estática

1. `TV-ZIP-01 filename_hash_semantics`.
2. `TV-IMG-01 exact_generator_parameters` e `TV-IMG-02 historical_png_byte_lineage` para imagens, sem transformar similaridade visual em evidência de geração.
3. Materialização/reconciliação do lote parcial somente após reexport dos bytes e validação do container completo.

### Ciclo DMAIC mínimo

```text
Define  -> objeto, claim e falsificador.
Measure -> bytes, SHA-256, tamanho, ambiente e saída.
Analyze -> contradição, dependência e TOKEN_VAZIO.
Improve -> uma mudança mínima, reversível e vinculada ao recibo.
Control -> readback, índice append-only, predecessor e gate anti-regressão.
Learn   -> F_ok/F_gap/F_next como entrada do próximo checkpoint.
```

## 8. Contrato mínimo para o Receipt V2

Um receipt só pode mudar de preparação para execução observada quando incluir, conjuntamente:

1. `INPUT_MANIFEST_ID`: RAW019–027, provider, bytes, SHA-256 e parse.
2. `IMPLEMENTATION_ID`: repositório, commit/blob, caminho executável/script e lock de dependências.
3. `INVOCATION_ID`: argv, cwd, variáveis não secretas, seed/config, locale/timezone quando relevante e timestamps.
4. `ENVIRONMENT_ID`: dispositivo/runner, SO, ABI, toolchain e versão relevante.
5. `OBSERVED_RUN`: steps observáveis, exit status, stdout/stderr e classificação da camada de falha.
6. `OUTPUT_MANIFEST_ID`: cada output com bytes, SHA-256, papel semântico e predecessor.
7. `RECEIPT_V2`: join dos seis itens acima, consistente e verificável independentemente.

Ausência de qualquer campo mantém `claim_allowed=false`.

## 9. Lente didática: Parábola da Invariante Ω

**Camada factual:** há pontos firmes de identidade e custódia; há lacunas explícitas de build, assinatura moderna, execução física, RAW018 e transformação.  
**Camada parabólica:** a forja não recebe metal ausente como se fosse lâmina pronta. O vazio mapeado é a cavidade que permite encaixar a peça correta; cada nova prova toca a ponte somente quando sua extremidade, peso e material são medidos.  
**Limite:** a parábola tem peso de evidência zero; não altera hashes, receipts ou gates.  
**Retorno operacional:** executar o próximo P0 em que fonte, bytes, SHA-256, ambiente e output possam ser ligados no mesmo recibo.

## 10. R3 e continuação reconstruível

**F_ok**

- dois artefatos principais têm nomes, bytes e SHA-256 ancorados;
- ZIP histórico passa CRC/decompressão integral;
- RAW019–027 possui custódia criptográfica por arquivo;
- a contradição do lote parcial foi separada e não contaminou o bundle íntegro.

**F_gap**

- identidade histórica byte-a-byte do APK;
- commit/recipe de build, v2/v3/v4, execução Android e CI observável;
- RAW018 atual, execução V2 e cadeia RAW→derivado;
- reconciliação do hash contraditório nos dois containers parciais.

**F_next**

1. Rehash físico do APK e ZIP íntegros; salvar saída e ambiente.
2. Executar `apksigner` e ancorar resultado.
3. Recuperar RAW018 por identidade de fonte.
4. Executar o V2 com os nove inputs fechados e emitir `RECEIPT_V2`.
5. Anexar apenas o novo delta e atualizar o índice, sem reescrever recibos predecessores.

