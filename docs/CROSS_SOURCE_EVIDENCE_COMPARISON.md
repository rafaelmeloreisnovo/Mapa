# Comparação de Evidências Cross-Source — Termux ↔ GitHub Actions

```yaml
schema: rafaelia.cross-source-evidence-comparison-guide/v2
mode: deterministic_offline_comparison
manifest_required: rafaelia.cross-source-local-gate/v3
floor_required: rafaelia.cross-source-gate-floor/v2
network_required: false
claim_allowed: false
remote_ci_substituted: false
```

## 1. Finalidade

Este protocolo compara dois pacotes produzidos pelo mesmo gate canônico:

1. pacote local, normalmente executado no Termux;
2. pacote remoto, produzido pelo GitHub Actions e baixado como artifact.

A pergunta respondida é restrita:

> Os cinco relatórios governados possuem os mesmos bytes, usam o mesmo piso e demonstram execução completa da mesma superfície de testes?

A comparação não afirma identidade humana, certificação externa, segurança absoluta ou autoria criptográfica.

## 2. Normalização entre ambientes

O registry é registrado como:

```text
indices/CROSS_SOURCE_REGISTRY.jsonl
```

Arquivos externos são representados por:

```text
external://<basename>
```

Isso remove a localização física do checkout do conteúdo selado e evita:

- falso negativo entre Termux e Actions;
- vazamento de diretórios locais;
- hashes diferentes causados apenas pelo nome da raiz.

## 3. Pacote obrigatório

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

## 4. Manifesto v3 obrigatório

Metadados ambientais podem variar:

- `generated_at`;
- `python_version`;
- `platform`.

Os campos governados não podem variar semanticamente:

```yaml
schema_version: rafaelia.cross-source-local-gate/v3
status: PASS
test_file_count: ">= minimum_test_file_count"
minimum_test_file_count: 7
test_count_discovered: ">= minimum_test_count"
test_count_observed: ">= minimum_test_count"
minimum_test_count: 58
test_count_observed_equals_discovered: true
complete_test_execution: true
report_count: 5
quality_floor:
  path: indices/CROSS_SOURCE_GATE_FLOOR.json
  schema_version: rafaelia.cross-source-gate-floor/v2
  sha256: sha256_valido
  status: PASS
quality_floor_status: PASS
promotion_state: LOCAL_PASS_REMOTE_TOKEN_VAZIO
claim_allowed: false
remote_ci_substituted: false
checksums: correspondentes_aos_cinco_relatorios
```

Um pacote com 58 testes descobertos e somente 57 executados é inválido, mesmo que os 57 tenham passado.

## 5. Execução

```sh
python3 scripts/compare_cross_source_evidence.py \
  --left .artifacts/cross-source-local \
  --right .artifacts/cross-source-remote \
  --write-report .artifacts/cross-source-comparison.json
```

A execução é offline e usa somente Python standard library.

## 6. Resultado `PASS`

```yaml
schema_version: rafaelia.cross-source-evidence-comparison/v2
status: PASS
left_bundle_status: PASS
right_bundle_status: PASS
report_count: 5
matching_report_count: 5
quality_floor_sha256_match: true
claim_allowed: false
remote_ci_substituted: false
```

Um `PASS` demonstra:

- checksums internos válidos;
- cinco relatórios byte a byte idênticos;
- mesmo SHA-256 do piso v2;
- sete ou mais arquivos governados;
- 58 ou mais testes descobertos;
- todos os testes descobertos executados;
- ausência de promoção local de claim.

## 7. Resultado `FAIL`

O comparador bloqueia:

- relatório ausente;
- ausência simultânea tratada falsamente como igualdade;
- checksum inválido ou desatualizado;
- conteúdo diferente, mesmo depois de reseal;
- manifest anterior à versão v3;
- quantidade de relatórios divergente;
- menos de sete arquivos de teste;
- menos de 58 testes descobertos ou executados;
- contagem executada diferente da contagem descoberta;
- `complete_test_execution=false`;
- `claim_allowed=true`;
- `remote_ci_substituted=true`;
- piso ausente, inválido ou diferente;
- relatório individual com `status != PASS`.

```text
None == None → nunca é evidência de igualdade
```

## 8. Estados epistêmicos

### Sem artifact remoto

```yaml
local_bundle: POSSIVEL_PASS
remote_bundle: TOKEN_VAZIO
comparison: TOKEN_VAZIO
claim_allowed: false
```

### Artifact remoto válido e idêntico

```yaml
local_bundle: PASS
remote_bundle: PASS
comparison: PASS
next_step: append_VALIDATE_custody_event
claim_allowed: false
```

### Pacotes divergentes

```yaml
comparison: FAIL
rewrite_evidence: forbidden
preserve_both_bundles: true
next_step: identify_first_divergent_report
```

## 9. Limites

SHA-256 verifica integridade e identidade de bytes. Isoladamente, não prova:

- quem executou o gate;
- integridade do ambiente;
- vínculo criptográfico entre artifact e executor;
- assinatura digital ou não repúdio;
- conformidade ou certificação externa.

A promoção final exige também:

1. run remoto com steps e logs observáveis;
2. artifact associado ao commit exato;
3. preservação dos dois pacotes;
4. comparação 5/5;
5. evento `VALIDATE` append-only.

## 10. Provas adversariais

```yaml
identical_reports_different_environment_metadata: PASS_expected
resealed_content_difference: FAIL_expected
unsealed_tampering: FAIL_expected
claim_promotion: FAIL_expected
incomplete_test_execution: FAIL_expected
discovered_executed_mismatch: FAIL_expected
test_file_floor_regression: FAIL_expected
quality_floor_mismatch: FAIL_expected
equal_absence: FAIL_expected
```

---

```text
Hash igual = bytes iguais
Descoberto = superfície reconhecida
Executado = superfície percorrida
Descoberto == Executado = completude
Tempo sem artifact = TOKEN_VAZIO útil e auditável
```
