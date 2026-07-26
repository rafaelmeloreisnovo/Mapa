# RAFAELIA — SOURCE OF TRUTH — C01/C02

**Data:** 2026-07-26  
**Estado:** `PASS_DOCUMENTARY_WITH_TOKEN_VAZIO`  
**Claim global:** `claim_allowed=false`

## Regra principal

```text
conceito != implementação != compilação != artefato != instalação != execução física != evidência replicada != claim permitido
```

## Hierarquia

| Nível | Fonte | Prova permitida | Limite |
|---|---|---|---|
| S0 | conversa, nota, README | intenção e escopo | não prova código ou execução |
| S1 | código em commit fixado | presença de implementação | não prova build |
| S2 | teste com comando, ambiente e exit code | comportamento local | não prova Android/device |
| S3 | artefato com SHA-256 ligado ao commit | identidade do artefato | não prova instalação |
| S4 | receipt de instalação e lançamento | execução naquele aparelho | não generaliza |
| S5 | repetição independente | replicação limitada | não prova superioridade geral |
| S6 | benchmark com protocolo e falsificadores | resultado medido | não excede o intervalo observado |
| S7 | ledger de claims aprovado | claim limitado e auditável | nunca verdade absoluta |

## Fontes por domínio

- **Mapa:** identidade, dependências, estados e pointers; não substitui logs.
- **RafPolimata:** commit fixado, `ECOSYSTEM_RUNTIME_STATE.json`, validadores, testes `segment.v1`, ApkC e receipts.
- **Rafaelia_Private:** RAFAELIA ZERO, OMEGA42 e contratos RAF1/RDC1/64; Rafa22 permanece alias não resolvido.
- **Vectras:** registro de gaps, manifests NDK, SBOM, proveniência, APK e receipts de dispositivo.
- **Termux/QEMU:** request/receipt de dispatch, hashes, exit code, binário QEMU e guest boot.
- **Google Drive:** preservação documental e de versões; documento não é execução.

## Campos mínimos de receipt

```yaml
gate_id: required
source_repository: required
source_commit: required
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
claim_allowed: false_until_promotion
```

## Promoção

1. `IMPLEMENTED`: código localizado em commit fixado.
2. `TESTED_LOCAL`: comando executado e receipt completo.
3. `ARTIFACT_VERIFIED`: source-to-binary e SHA-256.
4. `VERIFIED_DEVICE`: instalação, lançamento e manifesto do aparelho.
5. `EVIDENCE_LINKED`: claim aponta para receipts e artefatos.
6. `REPLICATED`: repetição independente ou controlada.
7. `CLAIM_ALLOWED`: falsificadores, escopo e ausência de contradição bloqueante.

## Inferências proibidas

- código implica execução;
- merge implica validação;
- cross-compile implica aparelho;
- APK gerado implica instalável;
- instalação implica guest boot;
- sintético implica corpus real;
- documentação implica prova;
- benchmark único implica superioridade;
- alias contextual implica identidade canônica.

## TOKEN_VAZIO

É estado epistemicamente válido. Cada ocorrência deve registrar objeto faltante, gate dependente, fonte provável, procedimento de preenchimento e risco de promoção prematura.

## Estado

```yaml
C01: PASS_DOCUMENTARY_WITH_TOKEN_VAZIO
C02: ACTIVE_BLOCKED_INFRA_NO_JOB_STEPS
claim_allowed: false
```

O C02 poderá promover somente verdade local host após execução concreta com transcript, toolchain, exit codes e hashes. Android, APK, Termux, QEMU e aparelho continuam fora desse gate.