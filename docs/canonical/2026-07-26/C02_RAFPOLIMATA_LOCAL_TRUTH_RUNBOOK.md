# RAFAELIA — CICLO 2 — RAFPOLIMATA LOCAL TRUTH RUNBOOK

**Data:** 2026-07-26  
**Estado:** `ACTIVE`  
**Base congelada:** `rafaelmeloreisnovo/RafPolimata@b230f79b4519f398d6a0f32c2235527966f14a36`  
**Claim:** `claim_allowed=false`

## Objetivo

Executar e preservar a verdade local integral do RafPolimata sem confundir inspeção estática, compilação host, cross-compile, artefato Android ou runtime físico.

## Gate já existente

```sh
bash scripts/validate_runtime_truth_local.sh
```

O gate possui nove etapas:

1. build estrito do compilador host;
2. testes e auditoria do `segment.v1`;
3. contrato de saída nativa;
4. parsing de output-base opcional;
5. rejeição de extensão desconhecida e fonte oversized;
6. invariantes de honestidade no código-fonte;
7. validação do estado de evidência do ecossistema;
8. validação do roteador de pesquisa toroidal;
9. testes e self-audit do Ecosystem Build Doctor.

## Lacuna encontrada

O script usa diretório temporário removido ao final. O relatório do Build Doctor e os binários temporários não são preservados. O workflow `ecosystem-build-doctor.yml` executa somente o doctor, não o gate integral. Portanto, a existência dos nove passos não equivale a um receipt persistente do C02.

## Implementação de fechamento

Criar no RafPolimata:

- `scripts/run_runtime_truth_receipt.sh`;
- `.github/workflows/runtime-truth-receipt.yml`;
- `docs/C02_RUNTIME_TRUTH_RECEIPT.md`.

O wrapper deve:

- executar o gate integral sem esconder exit code;
- preservar stdout e stderr separadamente;
- executar novamente o Build Doctor para manter JSON/Markdown persistentes;
- registrar commit executado e commit-base congelado;
- registrar versões de OS, Python, CC, Clang, Make e Git;
- calcular SHA-256 dos logs, relatórios e scripts;
- calcular BLAKE3 quando `b3sum` estiver disponível;
- marcar BLAKE3 ausente como `TOKEN_VAZIO_B3SUM_ABSENT`;
- produzir `runtime_truth_receipt.json` e `toolchain_manifest.json`;
- manter build Android, instalação e runtime como `TOKEN_VAZIO`;
- retornar falha quando o gate integral ou o doctor falhar.

## Artefatos esperados

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

## Promoção permitida

Após uma execução positiva com artefatos preservados:

```yaml
full_repository_local_validation: VERIFIED_BY_EXECUTION
build_doctor: VERIFIED_BY_EXECUTION
host_toolchain: EVIDENCE_LINKED
android_build: TOKEN_VAZIO
apk_install: TOKEN_VAZIO
physical_runtime: TOKEN_VAZIO
claim_allowed: false
```

## Falsificadores

- qualquer exit code diferente de zero impede promoção;
- ausência do commit exato invalida o receipt;
- ausência de logs ou hashes mantém o gate incompleto;
- workflow não iniciado não significa falha do código;
- workflow concluído sem upload de artefato não fecha cadeia de custódia;
- host PASS não prova ARM32/ARM64 em aparelho.

## Saída do C02

O C02 só fecha quando `runtime_truth_receipt.json`, `build-doctor.json` e `toolchain_manifest.json` forem observados em uma execução concreta. Até isso ocorrer, o estado é `ACTIVE / EXECUTION_PENDING`.