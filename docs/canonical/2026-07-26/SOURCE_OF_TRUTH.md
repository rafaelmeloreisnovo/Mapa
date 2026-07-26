# RAFAELIA — SOURCE OF TRUTH — CICLO 1

**Data canônica:** 2026-07-26  
**Estado:** `PARTIAL_DOCUMENTARY`  
**Claim global:** `claim_allowed=false`

## 1. Finalidade

Este documento determina qual fonte pode sustentar cada tipo de afirmação durante o fechamento dos gaps de Rafa22/Rafaelia_Private, RafPolimata, Vectras-VM-Android, Termux RAFCODEPhi e QEMU Rafaelia.

A regra principal é:

```text
conceito != implementação != compilação != artefato != instalação != execução física != evidência replicada != claim permitido
```

Nenhuma etapa substitui automaticamente a seguinte.

## 2. Hierarquia de verdade

| Nível | Fonte válida | O que pode provar | O que não pode provar |
|---|---|---|---|
| S0 | conversa, nota, ideia, README narrativo | intenção, escopo, hipótese | implementação ou execução |
| S1 | arquivo de código em commit fixado | presença de implementação | build, instalação ou runtime |
| S2 | teste local com comando, ambiente e exit code | comportamento no ambiente testado | dispositivo Android ou corpus real |
| S3 | artefato com SHA-256 e vínculo ao commit | identidade do binário ou dataset | instalação ou funcionamento físico |
| S4 | recibo de instalação/lançamento em aparelho | execução física naquele dispositivo | generalização para outros dispositivos |
| S5 | execução reproduzida em ambiente independente | replicação limitada | superioridade geral |
| S6 | benchmark com protocolo e falsificadores | resultado medido no protocolo | claim além do intervalo medido |
| S7 | ledger de claims aprovado | claim limitado e auditável | verdade absoluta ou perpétua |

## 3. Fontes canônicas por domínio

### 3.1 Identidade e organização

- `rafaelmeloreisnovo/Mapa`
- `REPOSITORY_PINSET.yaml`
- `ALIAS_REGISTRY.yaml`
- `FECHAMENTO_GAPS_MANIFEST.v1.yaml`

Essas fontes governam identidade, escopo, dependências e estado epistemológico. Elas não substituem logs de execução.

### 3.2 RafPolimata

Fontes primárias:

- commit fixado em `REPOSITORY_PINSET.yaml`;
- `ECOSYSTEM_RUNTIME_STATE.json`;
- schemas e validadores locais;
- testes do `segment.v1`;
- código e provas estruturais do ApkC.

Para promover `full_repository_local_validation`, são obrigatórios comando, toolchain, stdout/stderr, exit code e hashes dos artefatos gerados.

### 3.3 Rafaelia_Private / candidato provisório a Rafa22

Fontes primárias:

- código RAFAELIA ZERO;
- implementação OMEGA42;
- contratos RAF1/RDC1/64;
- recibos de teste sintético local.

O alias `Rafa22` permanece `TOKEN_VAZIO_ALIAS_RESOLUTION`. Nenhum arquivo pode usar Rafa22 como identidade criptográfica, nome de repositório ou origem de commit.

### 3.4 Vectras-VM-Android

Fontes primárias:

- `docs/ALL_GAPS_REGISTRY.md`;
- manifests de build e link;
- probe freestanding;
- SBOM e ledger de proveniência;
- recibos de APK e de dispositivo.

Teste host não prova ARM32/ARM64 Android. Compilação NDK não prova instalação. Instalação não prova guest boot.

### 3.5 Termux RAFCODEPhi e QEMU Rafaelia

Fontes primárias:

- contrato de dispatch;
- request e receipt com hashes;
- comando limitado, exit code e hashes de stdout/stderr;
- manifesto do binário QEMU;
- recibo de boot e shutdown do guest.

Presença de JNI, serviço ou script não prova travessia física Vectras → Termux → QEMU.

### 3.6 Google Drive

O Drive é cânone documental e de preservação de versões. Um documento no Drive prova que o registro foi preservado, mas não prova que código foi compilado ou executado.

Documentos associados:

- `RAFAELIA — Implementação Latentes e Papers — Drive GitHub V1`;
- `RAFAELIA — Auditoria Pronto, Gaps e TOKEN_VAZIO — 2026-07-26`;
- `RAFAELIA — Plano Técnico de Fechamento dos Gaps — 10 Ciclos — 2026-07-26`.

## 4. Campos mínimos de um recibo

```yaml
gate_id: required
source_repository: required
source_commit: required
branch_or_ref: required
command_or_procedure: required
environment: required
toolchain: required
started_at: required
finished_at: required
exit_code: required
artifact_path: required_when_generated
sha256: required_when_artifact_exists
blake3: TOKEN_VAZIO_ALLOWED_UNTIL_AVAILABLE
stdout_sha256: required_when_stdout_exists
stderr_sha256: required_when_stderr_exists
device_manifest: required_for_physical_runtime
falsifier: required
claim_allowed: false_until_gate_promotion
```

## 5. Regras de promoção

1. `IMPLEMENTED` exige código localizado em commit fixado.
2. `TESTED_LOCAL` exige teste executado e recibo completo.
3. `ARTIFACT_VERIFIED` exige vínculo source-to-binary e SHA-256.
4. `VERIFIED_DEVICE` exige instalação, lançamento e manifesto do aparelho.
5. `EVIDENCE_LINKED` exige ponteiro do claim para recibos e artefatos.
6. `REPLICATED` exige execução independente ou repetição controlada.
7. `CLAIM_ALLOWED` exige falsificadores, escopo e ausência de contradição bloqueante.

## 6. Inferências proibidas

- presença de código implica execução;
- merge implica validação;
- compilação cruzada implica funcionamento no aparelho;
- APK gerado implica APK instalável;
- instalação implica guest boot;
- dado sintético implica corpus real;
- documentação implica prova;
- benchmark único implica superioridade geral;
- ausência de erro implica correção total;
- alias contextual implica identidade canônica.

## 7. TOKEN_VAZIO como estado válido

`TOKEN_VAZIO` significa que a evidência necessária ainda não foi observada ou não existe no recorte atual. Ele não significa falha automática, falsidade ou descarte.

Cada `TOKEN_VAZIO` deve conter:

- objeto faltante;
- gate que depende dele;
- fonte provável;
- procedimento verificável para preenchimento;
- risco de promoção prematura.

## 8. Situação do Ciclo 1

### Fechado documentalmente

- repositórios centrais identificados;
- branches e commits congelados;
- papéis canônicos registrados;
- aliases exatos e contextuais separados;
- regras de promoção e falsificabilidade registradas;
- fontes de verdade por domínio definidas.

### Ainda vazio

- identidade exata de Rafa22;
- identidade canônica do produtor `CONVERSATIONS_CHUNKS_PRIVATE`;
- hashes dos artefatos ainda não materializados;
- receipts físicos;
- resultado da validação local integral do RafPolimata.

## 9. Gate de saída

O Ciclo 1 pode ser marcado `PASS_DOCUMENTARY_WITH_TOKEN_VAZIO` quando os três artefatos existirem e o manifesto apontar explicitamente as identidades ainda vazias. Isso permite iniciar o Ciclo 2, sem declarar encerramento das lacunas físicas.

```yaml
C01:
  repository_pinset: PASS_DOCUMENTARY
  alias_registry: PASS_DOCUMENTARY_WITH_TOKEN_VAZIO
  source_of_truth: PASS_DOCUMENTARY
  claim_allowed: false
  next_cycle: C02_RAFPOLIMATA_LOCAL_TRUTH
```

## R3

- **F_ok:** identidade, ordem de prova e limites de promoção agora possuem contrato canônico.
- **F_gap:** aliases privados, artefatos atuais, dispositivo e corpus real continuam sem prova direta.
- **F_next:** executar e registrar a validação local integral do RafPolimata sobre o commit congelado.