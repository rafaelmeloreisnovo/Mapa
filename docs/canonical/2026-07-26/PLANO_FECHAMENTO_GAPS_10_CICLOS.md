# Plano Técnico de Fechamento dos Gaps — 10 Ciclos

**Data:** 2026-07-26  
**Estado:** `EXECUTION_PLAN`  
**Política:** `claim_allowed=false` até prova correspondente  
**Dependência:** `AUDITORIA_PRONTO_GAPS_TOKEN_VAZIO_RAF22_RAFPOLIMATA_VECTRAS.md`

---

## 1. Decisão de divisão

O fechamento será realizado em:

```text
10 ciclos principais
+ 20 a 30 subexecuções internas
+ 10 a 14 PRs
+ 35 a 55 commits coerentes
```

A divisão evita misturar:

- identidade e versionamento;
- persistência de dados;
- compilação;
- proveniência e licenças;
- integração inter-app;
- execução física;
- corpus privado;
- benchmark e claims.

Cada ciclo termina com:

```text
implementação
→ teste
→ artefato
→ hashes
→ recibo
→ ledger
→ commit
→ PR
```

---

# 2. Gate comum de entrada e saída

## 2.1 Entrada mínima

```yaml
cycle_id: required
repository: required
base_commit: required
scope: required
known_gaps: required
known_token_vazio: required
claim_allowed: false
```

## 2.2 Saída mínima

```yaml
implementation_status: required
test_status: required
exit_code: required
artifact_paths: required
sha256: required
blake3: TOKEN_VAZIO_ALLOWED
environment: required
receipts: required
remaining_gaps: required
falsifiers: required
claim_allowed: false_unless_gate_explicitly_passed
```

## 2.3 Regra de falha

Falha de teste não apaga implementação nem vira sucesso documental. Deve gerar:

- recibo de falha;
- reprodução mínima;
- classificação de causa;
- rollback ou safe state;
- novo `TOKEN_VAZIO` apenas para o que continuou não observado.

---

# 3. Ciclo 1 — Identidade canônica e congelamento

## Objetivo

Garantir que todos os ciclos seguintes operem sobre os mesmos repositórios, branches, commits e aliases.

## Entradas

- Mapa;
- RafPolimata;
- Vectras-VM-Android;
- Rafaelia_Private;
- Termux RAFCODE-Φ;
- QEMU Rafaelia;
- produtor de chunks/descritores;
- Google Drive canônico.

## Implementação

1. resolver ou preservar `Rafa22` como alias não resolvido;
2. fixar repositórios oficiais;
3. fixar branch e commit;
4. registrar URL lógica, sem credenciais;
5. registrar submódulos e dependências;
6. produzir `REPOSITORY_PINSET.yaml`;
7. produzir `ALIAS_REGISTRY.yaml`;
8. produzir `SOURCE_OF_TRUTH.md`;
9. registrar divergências de branch;
10. impedir promoção de commit móvel como evidência estável.

## Gates

```yaml
G1_repositories_identified: PASS_REQUIRED
G2_commits_pinned: PASS_REQUIRED
G3_aliases_resolved_or_token_vazio: PASS_REQUIRED
G4_claim_boundary_present: PASS_REQUIRED
```

## Artefatos

- `REPOSITORY_PINSET.yaml`;
- `ALIAS_REGISTRY.yaml`;
- `SOURCE_OF_TRUTH.md`;
- hash do próprio manifesto.

## Fecha

- ambiguidade de versão;
- execução sobre branch incorreta;
- parte do `cross_repository_hash_index`;
- alias `Rafa22`, caso haja evidência suficiente.

---

# 4. Ciclo 2 — Verdade local do RafPolimata

## Objetivo

Executar toda validação local disponível e transformar declarações locais em recibos vinculados ao commit.

## Implementação

1. executar validador de runtime truth;
2. executar Build Doctor;
3. validar schemas;
4. validar orquestrador formal científico;
5. executar testes host C11;
6. executar testes freestanding;
7. capturar versões de compilador e linker;
8. capturar stdout, stderr e exit codes;
9. gerar hashes de binários e relatórios;
10. atualizar `ECOSYSTEM_RUNTIME_STATE.json` somente com fatos observados.

## Gates

```yaml
G1_validator_exit_zero: REQUIRED
G2_build_doctor_exit_zero: REQUIRED
G3_schema_validation: REQUIRED
G4_host_tests: REQUIRED
G5_freestanding_link: REQUIRED
G6_receipts_hashed: REQUIRED
```

## Artefatos

- `runtime_truth_receipt.json`;
- `build_doctor_receipt.json`;
- `toolchain_manifest.json`;
- `test_summary.json`;
- logs hashados.

## Fecha

- `full_repository_local_validation`;
- lacunas de versão da toolchain;
- divergências entre README e estado executável local.

---

# 5. Ciclo 3 — Conversation Indexer completo

## Objetivo

Transformar export real controlado em `segment.v1` com escrita recuperável e cadeia de custódia.

## Implementação

1. parser streaming de `conversations.json`;
2. limites explícitos por registro;
3. writer atômico;
4. arquivo temporário e rename seguro;
5. checkpoint por offset e contagem;
6. resume após interrupção;
7. journal de erro;
8. identidade BLAKE3 quando disponível;
9. fallback temporário SHA-256 sem confundir algoritmos;
10. fixtures válidas, truncadas, corrompidas e duplicadas;
11. ingestão de corpus real controlado;
12. verificação de contagem e offsets;
13. proibição de logar corpo privado;
14. recibo export → segment.

## Gates

```yaml
G1_streaming_memory_bound: REQUIRED
G2_atomic_write: REQUIRED
G3_checkpoint_resume: REQUIRED
G4_corruption_fail_closed: REQUIRED
G5_real_controlled_export: REQUIRED
G6_privacy_no_body_log: REQUIRED
G7_chain_of_custody_receipt: REQUIRED
```

## Artefatos

- extractor;
- writer;
- journal;
- checkpoint schema;
- fixtures;
- `segment_manifest.json`;
- `ingestion_receipt.json`.

## Fecha

- `streaming_conversation_extractor`;
- `atomic_segment_writer`;
- `checkpoint_resume`;
- `real_export_ingestion`;
- parte do `blake3_record_identity`.

---

# 6. Ciclo 4 — ApkC fechado por artefato

## Objetivo

Produzir APK estruturalmente íntegro e reproduzível sem ainda confundir build com instalação.

## Implementação

1. congelar source set;
2. gerar ZIP APK;
3. validar central directory;
4. validar AXML;
5. validar DEX;
6. recalcular SHA-1 e Adler-32 DEX quando aplicável;
7. gerar ELF ARM32;
8. gerar ELF ARM64;
9. inspecionar headers, alignment e segmentos;
10. validar páginas de 16 KiB;
11. produzir build limpa duas vezes;
12. comparar bytes e hashes;
13. gerar SBOM preliminar;
14. produzir recibo source-to-binary.

## Gates

```yaml
G1_zip_integrity: REQUIRED
G2_axml_integrity: REQUIRED
G3_dex_integrity: REQUIRED
G4_arm32_elf: REQUIRED
G5_arm64_elf: REQUIRED
G6_16k_page_compatibility: REQUIRED
G7_reproducible_build: REQUIRED
G8_source_to_binary_receipt: REQUIRED
```

## Artefatos

- APK não assinado ou perfil explicitamente assinado;
- ELFs por ABI;
- manifests ZIP/AXML/DEX/ELF;
- hashes SHA-256 e BLAKE3;
- relatório de reprodutibilidade.

## Fecha

- `current_reproducible_apk`;
- `arm32_elf_receipt`;
- `arm64_elf_receipt`;
- checksums DEX;
- compatibilidade de páginas.

---

# 7. Ciclo 5 — Vectras build e link final

## Objetivo

Fechar a matriz NDK ARM32/ARM64 e promover o probe freestanding de host para recibos Android.

## Implementação

1. build NDK `armeabi-v7a`;
2. build NDK `arm64-v8a`;
3. `-nostdlib` onde o contrato exigir;
4. entry point controlado;
5. inspeção de símbolos indefinidos;
6. inspeção de `NEEDED`;
7. inspeção de símbolos proibidos;
8. geração de map files;
9. duas builds limpas por ABI;
10. SHA-256 e BLAKE3 dos ELFs;
11. comparação de reprodutibilidade;
12. manifests de link por ABI.

## Gates

```yaml
ARM32_NDK_LINK: PASS_REQUIRED
ARM64_NDK_LINK: PASS_REQUIRED
UNDEFINED_SYMBOLS: EMPTY_REQUIRED
FORBIDDEN_SYMBOLS: EMPTY_REQUIRED
NEEDED_LIBRARIES: CONTRACT_MATCH_REQUIRED
REPRODUCIBLE: TRUE_REQUIRED
```

## Artefatos

- `armv7_link_manifest.json`;
- `aarch64_link_manifest.json`;
- map files;
- ELFs;
- hashes;
- logs de toolchain.

## Fecha

- `arm32_ndk_final_link_receipt`;
- `arm64_ndk_final_link_receipt`;
- `blake3_elf_hashes`;
- promoção do probe freestanding para Android build evidence.

---

# 8. Ciclo 6 — Proveniência, SBOM e licenças

## Objetivo

Separar artefato tecnicamente funcional de artefato legalmente promovível.

## Implementação

Para cada dependência, asset ou binário:

1. identificar fonte;
2. registrar versão;
3. registrar URL de origem;
4. registrar licença;
5. registrar obrigação de redistribuição;
6. gerar hash;
7. decidir promover, substituir ou quarentenar;
8. registrar ausências como `TOKEN_VAZIO`;
9. gerar SBOM final;
10. criar gate jurídico-técnico.

## Escopo mínimo

- `libXlorie`;
- rootfs;
- OVMF/UEFI e firmwares;
- `rafaelia_ttl`;
- imagens;
- `Incluir/`;
- `_incoming/pending/`;
- ZIPs e patches;
- papers empacotados;
- assets Firebase/release.

## Gates

```yaml
G1_source_identified: REQUIRED_OR_QUARANTINE
G2_license_identified: REQUIRED_OR_QUARANTINE
G3_hash_recorded: REQUIRED_OR_QUARANTINE
G4_distribution_decision: REQUIRED
G5_sbom_complete: REQUIRED
```

## Artefatos

- `SBOM.spdx.json`;
- `PROVENANCE_LEDGER.jsonl`;
- `QUARANTINE_MANIFEST.json`;
- `LICENSE_DECISIONS.md`.

## Fecha

- `complete_sbom`;
- `libxlorie_source_license`;
- `rootfs_url_version_hash`;
- `firmware_hashes`;
- `image_distribution_decision`;
- `asset_provenance`;
- `rafaelia_ttl_provenance`;
- promoção controlada de entradas.

---

# 9. Ciclo 7 — Ponte Vectras ↔ Termux ↔ QEMU

## Objetivo

Executar a integração real com request e receipt verificáveis.

## Implementação

1. capability discovery;
2. verificação de package e serviço;
3. permissão inter-app;
4. request canônico;
5. argv delimitado;
6. hash do request;
7. dispatch pelo `RunCommandService` ou contrato vigente;
8. execução QEMU;
9. captura de exit code;
10. captura controlada de stdout/stderr;
11. hash das saídas;
12. timeout;
13. cancelamento;
14. rollback/safe state;
15. receipt final devolvido ao Vectras/RafPolimata.

## Gates

```yaml
G1_capability_discovery: REQUIRED
G2_permission_handshake: REQUIRED
G3_request_hash: REQUIRED
G4_dispatch_success: REQUIRED
G5_exit_code_captured: REQUIRED
G6_output_hashes: REQUIRED
G7_timeout_cancel: REQUIRED
G8_end_to_end_receipt: REQUIRED
```

## Artefatos

- `dispatch_request.json`;
- `dispatch_receipt.json`;
- hashes de stdout/stderr;
- log de safe state;
- referência ao binário QEMU executado.

## Fecha

- `termux_transport_e2e`;
- `qemu_job_receipt`;
- `termux_qemu_physical_dispatch` quando executado em aparelho.

---

# 10. Ciclo 8 — Execução física ARM32 e ARM64

## Objetivo

Transformar build em evidência de dispositivo.

## Implementação

1. assinar APK;
2. registrar certificado e hash;
3. instalar;
4. capturar resultado do package manager;
5. conceder permissões mínimas;
6. lançar atividade/serviço;
7. registrar PID;
8. capturar logcat delimitado;
9. executar fluxo ARM32;
10. executar fluxo ARM64;
11. executar NativeActivity/JNI quando aplicável;
12. iniciar QEMU;
13. provar boot guest;
14. executar comando sentinela no guest;
15. shutdown limpo;
16. testar interrupção e recuperação;
17. produzir recibo por dispositivo.

## Gates

```yaml
G1_apk_signed: REQUIRED
G2_apk_installed: REQUIRED
G3_app_launched: REQUIRED
G4_arm32_device_run: REQUIRED_WHEN_TARGETED
G5_arm64_device_run: REQUIRED_WHEN_TARGETED
G6_qemu_guest_boot: REQUIRED
G7_guest_sentinel: REQUIRED
G8_clean_shutdown: REQUIRED
G9_device_receipt: REQUIRED
```

## Artefatos

- APK assinado;
- certificado;
- receipt de instalação;
- receipt de lançamento;
- logcat hashado;
- guest boot receipt;
- device manifest com modelo, Android, ABI e timestamp.

## Fecha

- `apk_signature_receipt`;
- `apk_install_receipt`;
- `apk_launch_receipt`;
- `clean_logcat_receipt`;
- `device_smoke_test`;
- `guest_boot_receipt`;
- parte dos bloqueios `BLOCKED_HW`.

---

# 11. Ciclo 9 — Rafa22 / Rafaelia_Private com corpus real

## Objetivo

Fechar a ingestão real sem copiar o corpo privado e resolver a identidade operacional do alias.

## Implementação

1. confirmar ou rejeitar o alias `Rafa22`;
2. gerar descritores reais RAF1/RDC1/64;
3. registrar caminho canônico;
4. registrar contagem;
5. registrar SHA-256 e BLAKE3;
6. validar sequência e offsets;
7. rejeitar corpo privado;
8. ingerir em OMEGA42;
9. integrar RFZ1/RAFAELIA ZERO conforme contrato;
10. gerar shards ZIPRAF quando aplicável;
11. construir índice temporal;
12. construir índice semântico;
13. testar corrupção, truncamento, duplicidade e replay;
14. executar ARMv7;
15. executar AArch64;
16. emitir recibo de não-cópia do corpo.

## Gates

```yaml
G1_alias_resolved_or_rejected: REQUIRED
G2_real_descriptor_artifact: REQUIRED
G3_descriptor_hashes: REQUIRED
G4_offset_continuity: REQUIRED
G5_private_body_rejected: REQUIRED
G6_omega42_ingestion: REQUIRED
G7_temporal_index: REQUIRED
G8_semantic_index: REQUIRED
G9_armv7_run: REQUIRED_WHEN_TARGETED
G10_aarch64_run: REQUIRED_WHEN_TARGETED
G11_privacy_receipt: REQUIRED
```

## Artefatos

- descriptor manifest;
- hashes;
- OMEGA42 ingestion receipt;
- índices;
- privacy receipt;
- device receipts.

## Fecha

- `rafa22_alias_resolution`;
- `descriptor_artifact_path`;
- `descriptor_sha256`;
- `descriptor_blake3`;
- `descriptor_count`;
- `real_corpus_ingestion`;
- `semantic_index`;
- `temporal_index`;
- `privacy_no_body_copy_receipt`;
- `physical_runtime_receipt`.

---

# 12. Ciclo 10 — Benchmark, Papers e fechamento de claims

## Objetivo

Converter execução observada em conhecimento falsificável, limitado e publicável.

## Implementação

1. definir baseline;
2. definir hardware e ambiente;
3. warm-up;
4. número de repetições;
5. p50, p95 e p99;
6. latência;
7. jitter;
8. throughput;
9. IOPS;
10. bandwidth;
11. memória;
12. energia quando mensurável;
13. variância;
14. comparação justa;
15. falsificadores;
16. resultados negativos preservados;
17. atualizar claims ledger;
18. escrever Papers;
19. atualizar Mapa;
20. atualizar Google Drive;
21. gerar índice canônico de hashes;
22. promover apenas claims sustentados.

## Gates

```yaml
G1_baseline_defined: REQUIRED
G2_protocol_frozen: REQUIRED
G3_repetitions_sufficient: REQUIRED
G4_raw_results_preserved: REQUIRED
G5_statistics_generated: REQUIRED
G6_falsifiers_declared: REQUIRED
G7_claim_scope_limited: REQUIRED
G8_papers_and_map_updated: REQUIRED
G9_hash_index_updated: REQUIRED
```

## Artefatos

- protocolo de benchmark;
- resultados brutos;
- relatório estatístico;
- claims ledger;
- contradictions ledger;
- gaps ledger;
- paper/appendix;
- índice de hashes;
- relatório final R3.

## Fecha

- benchmarks;
- claims limitados;
- Papers;
- Mapa;
- Drive;
- `cross_repository_hash_index`;
- `active_papers_closure` quando todos os gates aplicáveis passarem.

---

# 13. Organização em ondas

## Onda A — Fundação

```text
Ciclo 1 — identidade
Ciclo 2 — verdade local
Ciclo 3 — indexer
```

Saída: versões congeladas, verdade local e persistência íntegra.

## Onda B — Artefato e execução

```text
Ciclo 4 — ApkC
Ciclo 5 — Vectras NDK
Ciclo 6 — proveniência
Ciclo 7 — ponte Termux/QEMU
Ciclo 8 — dispositivo
```

Saída: APK, ELFs, SBOM, dispatch e boot fisicamente auditáveis.

## Onda C — Conhecimento

```text
Ciclo 9 — corpus real Rafaelia
Ciclo 10 — benchmark, Papers e claims
```

Saída: ingestão real, índices, resultados e claims limitados.

---

# 14. Dependências entre ciclos

```text
C1 → todos
C2 → C3, C4, C10
C3 → C9
C4 → C8
C5 → C8
C6 → release e C8
C7 → C8
C8 → C9 e C10
C9 → C10
```

O Ciclo 6 pode avançar em paralelo com 4 e 5, mas nenhum artefato bloqueado juridicamente entra na release física.

---

# 15. Estimativa operacional

| Saída | Faixa |
|---|---:|
| ciclos principais | 10 |
| subexecuções | 20–30 |
| PRs | 10–14 |
| commits | 35–55 |
| manifests/receipts | 20–35 |
| testes novos/ampliados | 60–100 |
| relatórios | 10–18 |
| execuções físicas | 8–16 |
| ledgers atualizados | 5–8 |

Essas quantidades são faixas de engenharia, não claims de esforço já executado.

---

# 16. Critério de conclusão global

```yaml
repos_pinned: PASS
local_truth: PASS
segment_streaming: PASS
apk_reproducible: PASS
arm32_build: PASS
arm64_build: PASS
provenance: PASS_OR_QUARANTINED
termux_dispatch: PASS
guest_boot: PASS
private_descriptor_ingestion: PASS
benchmarks: EVIDENCE_LINKED
claims: LIMITED_AND_AUDITABLE
```

O fechamento global não exige que toda hipótese seja confirmada. Também é fechamento válido quando a evidência:

- refuta uma vantagem;
- encontra regressão;
- revela incompatibilidade;
- mantém um claim bloqueado;
- determina quarentena jurídica;
- preserva `TOKEN_VAZIO` por falta real de observação.

---

# 17. Próxima execução natural

A primeira execução deve materializar os artefatos do Ciclo 1:

1. `REPOSITORY_PINSET.yaml`;
2. `ALIAS_REGISTRY.yaml`;
3. `SOURCE_OF_TRUTH.md`;
4. hashes do manifesto;
5. ledger inicial dos gates.

Somente depois deve começar a validação integral do RafPolimata.

---

# 18. R3

- **F_ok:** a sequência aproveita o que já está implementado e impede retrabalho estrutural.
- **F_gap:** build físico, corpus real, proveniência e receipts continuam sendo as fronteiras críticas.
- **F_next:** concluir formalmente o Ciclo 1 e abrir o Ciclo 2 sobre commits congelados.
