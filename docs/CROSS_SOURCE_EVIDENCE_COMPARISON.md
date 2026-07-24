# Comparação de Evidências Cross-Source — Termux ↔ GitHub Actions

```yaml
schema: rafaelia.cross-source-evidence-comparison-guide/v4
mode: deterministic_offline_comparison
manifest_required: rafaelia.cross-source-local-gate/v3
floor_required: rafaelia.cross-source-gate-floor/v2
comparison_report: rafaelia.cross-source-evidence-comparison/v4
network_required: false
claim_allowed: false
remote_ci_substituted: false
```

## 1. Finalidade

O protocolo compara dois pacotes produzidos pelo mesmo gate:

1. pacote local, normalmente do Termux;
2. pacote remoto, baixado do GitHub Actions.

A comparação responde:

> Os cinco relatórios possuem os mesmos bytes, são semanticamente coerentes entre si, demonstram execução completa e limpa e estão vinculados ao piso realmente versionado?

Não constitui prova de identidade humana, assinatura digital, segurança absoluta ou certificação externa.

## 2. Pacote obrigatório

```text
cross-source-test-validation.json
cross-source-record-validation.json
cross-source-registry-validation.json
chain-of-custody-validation.json
quality-floor-validation.json
LOCAL_GATE_STATUS.json
CHECKSUMS.sha256
```

Os cinco relatórios são selados e comparados por SHA-256.

## 3. Ordem das verificações

```text
1. carregar o piso real
2. validar checksums internos
3. validar o manifesto
4. validar a semântica de cada relatório
5. cruzar manifesto ↔ relatórios
6. comparar os cinco hashes entre os pacotes
```

A igualdade de hashes é necessária, mas não suficiente.

## 4. Piso real

O comparador recebe ou localiza:

```text
indices/CROSS_SOURCE_GATE_FLOOR.json
```

Cada pacote deve declarar exatamente:

```yaml
manifest.quality_floor.path: indices/CROSS_SOURCE_GATE_FLOOR.json
manifest.quality_floor.schema_version: igual_ao_arquivo_real
manifest.quality_floor.sha256: igual_ao_sha256_do_arquivo_real
manifest.quality_floor.status: PASS
```

Dois pacotes que concordem entre si sobre um SHA inventado continuam inválidos.

## 5. Consistência semântica cruzada

O comparador v4 não aceita apenas `status=PASS`.

### Manifesto ↔ relatório de testes

```yaml
manifest.test_file_count: igual_a test_report.test_file_count
manifest.test_count_discovered: igual_a test_report.tests_discovered
manifest.test_count_observed: igual_a test_report.tests_run
manifest.complete_test_execution: igual_a test_report.complete_execution
manifest.clean_test_outcomes: igual_a test_report.clean_outcomes
```

Além disso:

```yaml
test_report.schema_version: rafaelia.cross-source-test-report/v4
test_file_count: ">= 7"
tests_discovered: ">= 58"
tests_run: ">= 58"
tests_run_equals_tests_discovered: true
complete_execution: true
clean_outcomes: true
failures: 0
errors: 0
skipped: 0
expected_failures: 0
unexpected_successes: 0
claim_allowed: false
remote_ci_substituted: false
```

A lista `test_files` deve ser relativa a `tests/`, ordenada, única e ter o mesmo comprimento de `test_file_count`.

### Records

```yaml
schema_version: rafaelia.cross-source-record/v1
valid_fixture_count: ">= piso"
invalid_fixture_count: ">= piso"
unexpected_failures: 0
unexpected_passes: 0
```

### Registry

```yaml
schema_version: rafaelia.cross-source-registry-report/v1
registry: indices/CROSS_SOURCE_REGISTRY.jsonl
record_count: ">= piso"
provider_counts: ">= piso por provedor"
defect_count: 0
```

### Custódia

```yaml
schema_version: rafaelia.custody-validation-report/v1
event_count: ">= piso"
defect_count: 0
```

### Avaliação do piso

```yaml
schema_version: rafaelia.cross-source-gate-evaluation/v3
floor_schema_version: rafaelia.cross-source-gate-floor/v2
failed_check_count: 0
promotion_state: LOCAL_PASS_REMOTE_TOKEN_VAZIO
all_checks_passed: true
claim_allowed: false
remote_ci_substituted: false
```

## 6. Ataque identicamente resealado

Um caso antes insuficientemente bloqueado seria:

```yaml
left_reports_hashes: iguais_aos_right_reports_hashes
matching_report_count: 5
manifest_claim: 58_discovered_58_executed
sealed_test_report: 57_discovered_57_executed
```

Mesmo que ambos os pacotes sejam resealados e produzam hashes 5/5 iguais, o resultado agora é:

```yaml
status: FAIL
reason:
  - test_report_below_floor
  - manifest_test_counts_differ_from_test_report
```

```text
5/5 bytes iguais + semântica falsa = rejeitado
```

## 7. Normalização entre ambientes

O registry é representado por:

```text
indices/CROSS_SOURCE_REGISTRY.jsonl
```

Arquivos externos usam:

```text
external://<basename>
```

A raiz física do checkout não entra no conteúdo selado.

## 8. Execução

```sh
python3 scripts/compare_cross_source_evidence.py \
  --left .artifacts/cross-source-local \
  --right .artifacts/cross-source-remote \
  --floor indices/CROSS_SOURCE_GATE_FLOOR.json \
  --write-report .artifacts/cross-source-comparison.json
```

## 9. PASS

```yaml
schema_version: rafaelia.cross-source-evidence-comparison/v4
status: PASS
left_bundle_status: PASS
right_bundle_status: PASS
report_count: 5
matching_report_count: 5
quality_floor_sha256_match: true
claim_allowed: false
remote_ci_substituted: false
```

Demonstra:

- integridade interna dos pacotes;
- coerência semântica dentro de cada pacote;
- manifesto consistente com os relatórios;
- cinco relatórios byte a byte idênticos;
- vínculo ao mesmo piso real;
- execução completa e limpa acima do piso.

## 10. FAIL

O comparador bloqueia:

- relatório ausente;
- ausência dupla usada como igualdade;
- checksum inválido;
- conteúdo diferente depois de reseal;
- pacote identicamente resealado com semântica falsa;
- schema de relatório incorreto;
- manifesto divergente do relatório de testes;
- lista de testes duplicada, desordenada ou fora de `tests/`;
- registry com caminho não canônico;
- redução de registros, provedores ou custódia;
- avaliação de piso com check falho ou omitido;
- execução parcial ou resultados não limpos;
- claim ou CI remota substituída;
- piso ausente, inválido ou diferente do arquivo real.

```text
None == None → nunca é evidência
Hash igual → não corrige semântica inválida
```

## 11. Estados epistêmicos

### Sem artifact remoto

```yaml
local_bundle: POSSIVEL_PASS
remote_bundle: TOKEN_VAZIO
comparison: TOKEN_VAZIO
claim_allowed: false
```

### Artifact válido e idêntico

```yaml
local_bundle: PASS
remote_bundle: PASS
comparison: PASS
next_step: append_VALIDATE_custody_event
```

### Divergência

```yaml
comparison: FAIL
rewrite_evidence: forbidden
preserve_both_bundles: true
next_step: identify_first_semantic_or_byte_divergence
```

## 12. Limites

SHA-256 e coerência semântica não provam sozinhos:

- identidade do executor;
- ambiente não comprometido;
- vínculo criptográfico do artifact;
- não repúdio;
- certificação externa.

Promoção exige também:

1. run com steps e logs observáveis;
2. artifact associado ao commit exato;
3. preservação dos dois pacotes;
4. comparação semântica e 5/5 contra o piso real;
5. evento `VALIDATE` append-only.

## 13. Provas adversariais

```yaml
identical_reports_different_environment: PASS_expected
resealed_content_difference: FAIL_expected
identically_resealed_semantic_forgery: FAIL_expected
unsealed_tampering: FAIL_expected
claim_promotion: FAIL_expected
incomplete_execution: FAIL_expected
unclean_test_outcomes: FAIL_expected
discovered_executed_mismatch: FAIL_expected
test_file_regression: FAIL_expected
real_floor_changed_after_seal: FAIL_expected
equal_absence: FAIL_expected
```

---

```text
Bytes = integridade
Semântica = coerência
Piso real = referência
Custódia = história
Tempo sem artifact = TOKEN_VAZIO
```
