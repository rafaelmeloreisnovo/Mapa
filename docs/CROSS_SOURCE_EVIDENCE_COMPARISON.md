# Comparação de Evidências Cross-Source — Termux ↔ GitHub Actions

```yaml
schema: rafaelia.cross-source-evidence-comparison-guide/v1
mode: deterministic_offline_comparison
network_required: false
claim_allowed: false
remote_ci_substituted: false
```

## Finalidade

Este protocolo compara dois pacotes produzidos pelo mesmo gate canônico:

1. pacote local, normalmente executado no Termux;
2. pacote remoto, produzido pelo GitHub Actions e baixado como artifact.

A comparação responde a uma pergunta restrita e verificável:

> Os cinco relatórios governados possuem exatamente os mesmos bytes e foram selados pelo mesmo piso de qualidade?

Ela não afirma identidade humana, certificação externa, segurança absoluta ou autoria criptográfica.

## Correção de reprodutibilidade

O relatório do registry anteriormente podia registrar o caminho absoluto do checkout. O mesmo conteúdo poderia gerar, por exemplo:

```text
/data/data/com.termux/files/home/Mapa/indices/CROSS_SOURCE_REGISTRY.jsonl
/home/runner/work/Mapa/Mapa/indices/CROSS_SOURCE_REGISTRY.jsonl
```

Esses caminhos eram semanticamente equivalentes, mas produziam hashes diferentes.

A representação canônica agora é:

```text
indices/CROSS_SOURCE_REGISTRY.jsonl
```

Para fixtures externas ao repositório:

```text
external://<basename>
```

Isso evita:

- divergência causada apenas pelo local do checkout;
- vazamento de usuário, diretório pessoal ou raiz temporária;
- falso negativo na comparação Termux ↔ Actions.

## Pacote obrigatório

Cada diretório comparado deve conter:

```text
cross-source-test-validation.json
cross-source-record-validation.json
cross-source-registry-validation.json
chain-of-custody-validation.json
quality-floor-validation.json
LOCAL_GATE_STATUS.json
CHECKSUMS.sha256
```

Os cinco primeiros arquivos são comparados byte a byte por SHA-256.

`LOCAL_GATE_STATUS.json` pode variar somente nos metadados ambientais, como:

- `generated_at`;
- `python_version`;
- `platform`.

Mesmo assim, seus campos governados são validados:

```yaml
status: PASS
report_count: 5
quality_floor_status: PASS
promotion_state: LOCAL_PASS_REMOTE_TOKEN_VAZIO
claim_allowed: false
remote_ci_substituted: false
checksums: correspondentes_aos_cinco_relatorios
```

## Execução

```sh
python3 scripts/compare_cross_source_evidence.py \
  --left .artifacts/cross-source-local \
  --right .artifacts/cross-source-remote \
  --write-report .artifacts/cross-source-comparison.json
```

A execução é offline e usa somente Python standard library.

## Resultado `PASS`

```yaml
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

- integridade interna dos dois pacotes;
- checksums coerentes com os arquivos presentes;
- cinco relatórios byte a byte idênticos;
- mesmo SHA-256 do piso de qualidade;
- ausência de promoção local de claim;
- ausência de substituição artificial da CI remota.

## Resultado `FAIL`

O comparador bloqueia, entre outros casos:

- relatório ausente;
- dois relatórios ausentes no mesmo caminho;
- checksum inválido ou desatualizado;
- conteúdo diferente mesmo após novo selamento;
- quantidade de relatórios divergente;
- `claim_allowed=true`;
- `remote_ci_substituted=true`;
- piso de qualidade ausente ou diferente;
- relatório individual com `status != PASS`.

A ausência simultânea nunca conta como correspondência:

```text
None == None  → proibido como evidência de igualdade
```

## Estados epistêmicos

### Antes de existir artifact remoto

```yaml
local_bundle: POSSIVEL_PASS
remote_bundle: TOKEN_VAZIO
comparison: TOKEN_VAZIO
claim_allowed: false
```

### Depois de artifact remoto válido e idêntico

```yaml
local_bundle: PASS
remote_bundle: PASS
comparison: PASS
next_step: append_VALIDATION_custody_event
claim_allowed: false
```

### Quando os pacotes divergem

```yaml
comparison: FAIL
rewrite_evidence: forbidden
preserve_both_bundles: true
next_step: identify_first_divergent_report
```

## Limites

SHA-256 fornece verificação de integridade e identidade de bytes. Isoladamente, ele não prova:

- quem executou o gate;
- que o ambiente não estava comprometido;
- que o artifact foi produzido pelo runner declarado;
- assinatura digital ou não repúdio;
- conformidade ou certificação externa.

Por isso, a promoção final exige também:

1. artifact remoto associado ao run observável;
2. run com steps e logs reais;
3. referência ao commit exato;
4. preservação dos dois pacotes;
5. evento `VALIDATE` append-only na cadeia de custódia.

## Provas adversariais implementadas

```yaml
identical_reports_different_environment_metadata: PASS_expected
resealed_content_difference: FAIL_expected
unsealed_tampering: FAIL_expected
claim_promotion: FAIL_expected
quality_floor_mismatch: FAIL_expected
equal_absence: FAIL_expected
```

---

```text
Hash igual = bytes iguais
Bytes iguais ≠ executor autenticado
Artifact observável + commit + custódia = evidência ampliada
Tempo sem artifact = TOKEN_VAZIO útil e auditável
```
