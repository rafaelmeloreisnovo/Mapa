# Comparação de Evidências Cross-Source — Termux ↔ GitHub Actions

```yaml
schema: rafaelia.cross-source-evidence-comparison-guide/v3
mode: deterministic_offline_comparison
manifest_required: rafaelia.cross-source-local-gate/v3
floor_required: rafaelia.cross-source-gate-floor/v2
comparison_report: rafaelia.cross-source-evidence-comparison/v3
network_required: false
claim_allowed: false
remote_ci_substituted: false
```

## 1. Finalidade

O protocolo compara dois pacotes produzidos pelo mesmo gate:

1. pacote local, normalmente do Termux;
2. pacote remoto, baixado do GitHub Actions.

Pergunta verificável:

> Os cinco relatórios possuem os mesmos bytes, foram produzidos com execução completa e limpa e estão vinculados ao arquivo real do mesmo piso versionado?

Não é prova de identidade humana, assinatura digital, segurança absoluta ou certificação externa.

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

Os cinco relatórios são comparados byte a byte por SHA-256.

## 3. Piso real, não apenas declarado

O comparador recebe ou localiza:

```text
indices/CROSS_SOURCE_GATE_FLOOR.json
```

Para cada pacote, ele exige:

```yaml
manifest.quality_floor.path: indices/CROSS_SOURCE_GATE_FLOOR.json
manifest.quality_floor.schema_version: igual_ao_arquivo_real
manifest.quality_floor.sha256: igual_ao_sha256_do_arquivo_real
manifest.quality_floor.status: PASS
```

Assim, dois pacotes não podem concordar entre si sobre um SHA inventado e serem aceitos. Ambos precisam concordar com o piso realmente versionado no checkout usado para a comparação.

## 4. Manifesto v3

Metadados ambientais podem variar:

- `generated_at`;
- `python_version`;
- `platform`.

Campos governados:

```yaml
schema_version: rafaelia.cross-source-local-gate/v3
status: PASS
test_file_count: ">= 7"
minimum_test_file_count: 7
test_count_discovered: ">= 58"
test_count_observed: ">= 58"
minimum_test_count: 58
test_count_observed_equals_discovered: true
complete_test_execution: true
clean_test_outcomes: true
report_count: 5
quality_floor_status: PASS
promotion_state: LOCAL_PASS_REMOTE_TOKEN_VAZIO
claim_allowed: false
remote_ci_substituted: false
checksums: correspondentes_aos_cinco_relatorios
```

`clean_test_outcomes=true` significa:

```yaml
skipped: 0
expected_failures: 0
unexpected_successes: 0
```

## 5. Normalização entre ambientes

O registry é registrado como:

```text
indices/CROSS_SOURCE_REGISTRY.jsonl
```

Arquivos externos usam:

```text
external://<basename>
```

A raiz física do checkout não entra no relatório e não altera o hash.

## 6. Execução

```sh
python3 scripts/compare_cross_source_evidence.py \
  --left .artifacts/cross-source-local \
  --right .artifacts/cross-source-remote \
  --floor indices/CROSS_SOURCE_GATE_FLOOR.json \
  --write-report .artifacts/cross-source-comparison.json
```

A opção `--floor` possui o arquivo versionado como padrão, mas é mantida explícita nos procedimentos de auditoria.

## 7. PASS

```yaml
schema_version: rafaelia.cross-source-evidence-comparison/v3
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

- checksums internos válidos;
- cinco relatórios idênticos;
- mesmo piso real;
- sete ou mais arquivos governados;
- 58 ou mais testes descobertos e executados;
- contagens descoberta e executada iguais;
- zero skips e resultados esperados especiais;
- ausência de promoção local de claim.

## 8. FAIL

O comparador bloqueia:

- relatório ausente;
- ausência dupla usada como falsa igualdade;
- checksum inválido;
- conteúdo diferente depois de reseal;
- manifest anterior à v3;
- menos de sete arquivos;
- menos de 58 testes;
- execução parcial;
- `clean_test_outcomes=false`;
- `claim_allowed=true`;
- `remote_ci_substituted=true`;
- piso ausente ou inválido;
- SHA declarado diferente do arquivo real;
- relatório individual diferente de PASS.

```text
None == None → nunca é evidência
```

## 9. Estados epistêmicos

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
next_step: identify_first_divergent_report
```

## 10. Limites

SHA-256 verifica identidade de bytes. Não prova sozinho:

- executor humano ou serviço;
- ambiente não comprometido;
- vínculo criptográfico do artifact;
- não repúdio;
- certificação externa.

Promoção exige também:

1. run com steps e logs observáveis;
2. artifact associado ao commit exato;
3. preservação dos pacotes;
4. comparação 5/5 contra o piso real;
5. evento `VALIDATE` append-only.

## 11. Provas adversariais

```yaml
identical_reports_different_environment: PASS_expected
resealed_content_difference: FAIL_expected
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
Pacotes iguais + piso falso = rejeitado
Pacotes iguais + piso real = comparável
Comparável ≠ executor autenticado
Tempo sem artifact = TOKEN_VAZIO
```
