# RAFAELIA — C02 — RAFPOLIMATA LOCAL TRUTH RUNBOOK

**Data:** 2026-07-26  
**Estado:** `ACTIVE_BLOCKED_INFRA_NO_JOB_STEPS`  
**Base:** `rafaelmeloreisnovo/RafPolimata@b230f79b4519f398d6a0f32c2235527966f14a36`  
**Claim:** `claim_allowed=false`

## Objetivo

Executar e preservar a verdade local integral do RafPolimata sem confundir inspeção estática, compilação host, cross-compile, APK ou runtime físico.

## Gate existente

```sh
bash scripts/validate_runtime_truth_local.sh
```

O gate executa nove blocos:

1. build estrito do compilador host;
2. testes e auditoria do `segment.v1`;
3. contrato de saída nativa;
4. parsing de output-base opcional;
5. rejeição de extensão desconhecida e fonte oversized;
6. invariantes de honestidade no código;
7. validação do estado do ecossistema;
8. roteador de pesquisa toroidal;
9. testes e self-audit do Build Doctor.

## Lacuna corrigida no PR RafPolimata #167

O gate usa diretório temporário e descartava relatórios ao final. Foram adicionados:

- `scripts/run_runtime_truth_receipt.sh`;
- `.github/workflows/runtime-truth-receipt.yml`;
- `docs/C02_RUNTIME_TRUTH_RECEIPT.md`.

O wrapper preserva logs, executa o Build Doctor com saídas persistentes, registra commit e toolchain, calcula SHA-256 e usa BLAKE3 quando `b3sum` estiver disponível.

## Execução permitida

```sh
bash scripts/run_runtime_truth_receipt.sh artifacts/runtime-truth
```

Não instala pacotes, não baixa dependências, não modifica Git e não acessa corpus privado.

## Saídas

```text
artifacts/runtime-truth/
├── runtime-truth.stdout.log
├── runtime-truth.stderr.log
├── build-doctor.stdout.log
├── build-doctor.stderr.log
├── build-doctor.json
├── build-doctor.md
├── toolchain_manifest.json
└── runtime_truth_receipt.json
```

## Observação atual

O workflow run `30192393839` foi criado, mas o job `89767890981` apresentou zero steps e nenhum log. O CI geral do mesmo commit também apresentou zero steps. Logo:

```yaml
workflow_registered: true
runner_started_commands: false
code_execution_observed: false
code_result: TOKEN_VAZIO_EXECUTION_NOT_OBSERVED
infrastructure_state: BLOCKED_INFRA_NO_JOB_STEPS
```

## Promoção permitida após execução positiva

```yaml
repository_local_truth: VERIFIED_BY_EXECUTION
build_doctor: VERIFIED_BY_EXECUTION
host_toolchain: EVIDENCE_LINKED
android_build: TOKEN_VAZIO
apk_install: TOKEN_VAZIO
physical_runtime: TOKEN_VAZIO
claim_allowed: false
```

## Falsificadores

- exit code diferente de zero;
- commit ausente ou divergente;
- logs ou hashes ausentes;
- relatório do Build Doctor ausente;
- artifact upload ausente;
- host PASS promovido a Android/device;
- workflow zero-step interpretado como falha de código.

## Fechamento

O C02 fecha somente após observar `runtime_truth_receipt.json`, `build-doctor.json` e `toolchain_manifest.json` produzidos por execução concreta. Até lá, permanece `ACTIVE_BLOCKED_INFRA_NO_JOB_STEPS`.