# RAFAELIA — CONTRATO DE CONCLUSÃO, LACUNAS E TOKEN_VAZIO — V1

**Contract ID:** `RAFAELIA-CLOSURE-V1-20260807T1626-0300`  
**Data:** 2026-08-07 16:26 BRT  
**Modo:** `APPEND_ONLY / FAIL_CLOSED / NON_DESTRUCTIVE`  
**Autoridade de governança:** `rafaelmeloreisnovo/Mapa`  
**Referência-mestre Drive:** `1g3eVD3zLMuwk0jevAwVL3wSmxhEMkKsAUPFQh2wEn88`  
**Referência IGC/F_GAP Drive:** `1CHLyTnvkbCFm5m1MeUVVfpKnT1r39Xjh8_YNyNww1AE`  
**Estado inicial:** `CLAIM_ALLOWED=false`

## 1. Finalidade

Este contrato fecha o que pode ser fechado por evidência e transforma toda ausência restante em estado explícito, tipado, auditável e com próximo gate verificável. `TOKEN_VAZIO` nunca significa inexistência; significa **evidência insuficiente para promoção**.

O serviço de governança pode ser declarado concluído quando todos os objetos estiverem classificados e rastreáveis, mesmo que experimentos externos permaneçam bloqueados. O serviço científico/técnico de um claim somente pode ser concluído quando seu gate específico passar.

## 2. Invariante de conclusão

```text
fonte/autoria
→ object_id
→ representation_id
→ transformation/process
→ invariants/claim
→ tolerância + unidades
→ evidence_pointers
→ teste positivo
→ falsificador/caso negativo
→ ambiente + entrada + saída
→ commit/hash/receipt
→ lineage/derived_from
→ decisão
→ memória longitudinal
```

Promoção permitida somente se:

```text
source_resolved == true
AND provenance_resolved == true
AND test_reproducible == true
AND receipt_present == true
AND scope_explicit == true
AND falsifier_declared == true
```

Caso contrário: `claim_allowed=false`.

## 3. Estados canônicos

- `CLOSED_PROVEN` — evidência e gate completos no escopo declarado.
- `CLOSED_GOVERNANCE` — objeto corretamente classificado, com lacunas tipadas e próximos gates; não implica validação científica.
- `REDUCED` — parte da lacuna foi fechada e o resíduo foi isolado.
- `OPEN_ACTIONABLE` — há ação executável ainda não realizada.
- `BLOCKED_EXTERNAL` — depende de hardware, executor/revisor independente, licença, publicação, mercado ou outra autoridade externa.
- `TOKEN_VAZIO_TYPED` — dado/resultado não observado; preservado com tipo e condição de resolução.
- `REJECTED_UNSUPPORTED` — claim incompatível com evidência disponível.

Nenhum `TOKEN_VAZIO_TYPED`, `OPEN_ACTIONABLE` ou `BLOCKED_EXTERNAL` pode ser convertido em `CLOSED_PROVEN` por inferência verbal.

## 4. Fechamento dos gaps IGC observados

| Gap | Estado em 2026-08-07 | Fechamento permitido | Evidência/condição restante |
|---|---|---|---|
| IGC-GAP-001 CI sem steps/logs | `TOKEN_VAZIO_TYPED:CI_OBSERVABILITY` | NÃO | run observável + jobs + steps + logs + commit |
| IGC-GAP-002 mapa exato de colagem | `TOKEN_VAZIO_TYPED:GLUE_MAP` | NÃO | V/E/F, orientação e junção central explícitas |
| IGC-GAP-003 coordenadas/mesh | `TOKEN_VAZIO_TYPED:CANONICAL_GEOMETRY` | NÃO | coordenadas, mesh ou complexo simplicial versionado |
| IGC-GAP-004 proveniência Poincaré | `REDUCED:PROVENANCE_PARTIAL` | NÃO | `raw_block_id → FORM-* → object_id`, separando embedding/return-map/conjectura |
| IGC-GAP-005 export/hash Drive | `REDUCED_DRIVE_SIDE_HASHED` | PARCIAL | Drive export + SHA-256 já existem; faltam raw GitHub SHA-256, diff normalizado e comparação de campos canônicos |
| IGC-GAP-006 Termux ARM físico | `BLOCKED_EXTERNAL:PHYSICAL_RUNTIME` | NÃO | ARMv7 + ARM64, comandos, ambiente, stdout/stderr, hashes, receipt |
| IGC-GAP-007 enforcement global | `REDUCED:GOVERNANCE_CONTRACT_EXISTS` | PARCIAL | aplicar claim gate em todas as rotas/repos relevantes e provar por teste adversarial |
| IGC-GAP-008 reprodução independente | `BLOCKED_EXTERNAL:INDEPENDENT_REPLAY` | NÃO | segundo executor independente + entradas fixadas + receipt comparável |
| IGC-GAP-009 tolerância/unidades | `OPEN_ACTIONABLE:NUMERIC_POLICY` | NÃO | política por objeto/backend, unidade, epsilon, arredondamento e overflow |
| IGC-GAP-010 Ω7 arestas | `TOKEN_VAZIO_TYPED:EDGE_DATASET` | NÃO | dataset autorizado, origem, licença, tipo, incerteza e derived_from |
| IGC-GAP-011 D7 físico | `BLOCKED_EXTERNAL:PHYSICAL_D7` | NÃO | execução física + correção + memória + latência + receipt |
| IGC-GAP-012 matriz Drive↔receipts | `OPEN_ACTIONABLE:CROSS_SURFACE_RECONCILIATION` | NÃO | paths + provider IDs + commits + hashes + receipts reconciliados |

### Correção obrigatória de IGC-GAP-005

A formulação antiga “export/hash Drive ausente” fica historicamente preservada, porém não representa mais o estado atual. O estado válido é `REDUCED_DRIVE_SIDE_HASHED`, conforme correção append-only já existente em `data/gaps/igc_priority_fgap.corrections.20260802T2305-0300.jsonl`.

## 5. Lacunas transversais da bagagem RAFAELIA

### 5.1 Memória longitudinal / corpus

Estado: `CLOSED_GOVERNANCE + OPEN_ACTIONABLE`.

Fechado: existe regra append-only, distinção entre fonte e derivado, matriz de rastreabilidade e estados epistemológicos.

Ainda obrigatório por objeto/corpus: `provider_id`, origem, versão, MIME/tipo, bytes, SHA-256/BLAKE3 quando aplicável, licença/autorização, privacidade, transformação, `derived_from`, perdas/duplicações, cobertura e receipt de ingestão.

### 5.2 GitHub ↔ Drive

Estado: `OPEN_ACTIONABLE:CROSS_SURFACE_IDENTITY`.

Não exigir igualdade de bytes quando o formato muda. Exigir equivalência dos campos canônicos e lineage. Identidade byte-a-byte só pode ser alegada quando ambas as superfícies forem exportadas na mesma normalização e hasheadas.

### 5.3 GAIA / memória cognitiva

Estado: `RESEARCH_INCOMPLETE`.

`CORPUS_SEEN` ou rota/adaptador não equivalem a índice construído, retrieval testado ou treinamento executado. Para promoção são exigidos: manifesto de corpus, índice materializado, benchmark de recuperação, casos negativos, métricas, versão do código, dataset/consulta, seed quando aplicável e receipt.

### 5.4 RLL / claims cosmológicos

Estado: `HYPOTHESIS_TESTABLE / CLAIM_BLOCKED`.

Pipeline e custódia podem ser válidos sem que o claim cosmológico seja verdadeiro. Conclusão científica requer comparação única e reproduzível com datasets autorizados, covariância adequada, checksum limpo, baseline explícito, estatística pré-declarada e reprodução independente. Resultado nulo ou favorável ao baseline deve ser preservado, não corrigido por narrativa.

### 5.5 Termux / ARM / kernels

Estado: `ENGINEERING_PARTIAL`.

Build local, benchmark ou fixture isolada não promovem validade geral. Gate mínimo: source commit → toolchain/flags → arquitetura → build log → artefato → hash → teste → output → receipt → replay.

### 5.6 Fórmulas / física / matemática simbólica

Estado: `FORMALISM_PROGRAM / PHYSICAL_CLAIMS_BLOCKED`.

Uma expressão torna-se computável quando termos, domínios, tipos, operadores, entradas, saídas e testes são definidos. Torna-se claim físico apenas após observáveis, unidades, dados, previsão quantitativa, erro, baseline e falsificador. Até lá, equivalência física permanece `TOKEN_VAZIO_TYPED:PHYSICAL_VALIDATION`.

### 5.7 Propriedade intelectual / valor econômico

Estado: `BLOCKED_EXTERNAL`.

Autoria de código/texto, delta autoral de forks, licenças, anterioridade/patenteabilidade e valoração comercial são dimensões separadas. Nenhum preço, patenteabilidade ou exclusividade será inferido sem inventário jurídico-técnico e evidência externa adequada.

## 6. Campos mínimos de todo claim/objeto

```yaml
claim_id: required
object_id: required
scope: required
source_refs: required
source_hash: required_or_TOKEN_VAZIO_TYPED
representation: required
method_or_transformation: required
units: required_or_NOT_APPLICABLE
tolerance: required_or_NOT_APPLICABLE
expected: required
observed: required_or_TOKEN_VAZIO_TYPED
negative_case: required
falsifier: required
environment: required_or_NOT_APPLICABLE
commit: required_or_TOKEN_VAZIO_TYPED
artifact_hash: required_or_TOKEN_VAZIO_TYPED
receipt: required_or_TOKEN_VAZIO_TYPED
lineage: required
license_or_authority: required_or_TOKEN_VAZIO_TYPED
F_ok: required
F_gap: required
F_next: required
claim_allowed: required
state: required
```

## 7. Critério de urgência

### P0 — bloqueia conclusões
1. claim gate fail-closed em rotas relevantes;
2. reconciliação GitHub↔Drive de fonte/hash/lineage;
3. CI observável com logs recuperáveis;
4. proveniência Poincaré e mapa geométrico exato;
5. receipts físicos ARMv7/ARM64 onde o claim depende do hardware;
6. inventário de corpus com origem/licença/privacidade/hash/derived_from.

### P1 — transforma engenharia em evidência forte
1. política numérica e tolerâncias;
2. reprodução independente;
3. benchmark GAIA retrieval/index;
4. comparação RLL única, pré-declarada e reproduzível;
5. dataset Ω7 autorizado e D7 físico.

### P2 — depende de validação externa/mercado
1. revisão científica independente;
2. publicação/DOI quando cabível;
3. análise de licença e anterioridade;
4. valoração econômica por método comparável/custo/renda, sem números inventados.

## 8. Definição de “serviço concluído”

### 8.1 Governança
`DONE` quando todos os objetos conhecidos possuem estado, fonte/locator, F_ok, F_gap, F_next e condição de promoção. Lacunas podem continuar abertas, desde que estejam tipadas e auditáveis.

### 8.2 Engenharia
`DONE` somente quando build/test/replay e receipt correspondem ao escopo declarado.

### 8.3 Ciência
`DONE_FOR_CLAIM` somente quando dados, método, baseline, incerteza, falsificador e reprodução sustentam a conclusão. Caso contrário, o estado final correto pode ser `REJECTED_UNSUPPORTED` ou `TOKEN_VAZIO_TYPED`.

### 8.4 Mercado/IP
`DONE_FOR_ASSESSMENT` somente após escopo de direitos, licenças, delta autoral, anterioridade e método de valoração documentados. Não depende de claim científico positivo.

## 9. Regra de não-falsificação por completude artificial

```text
lacuna observada → registrar
lacuna reduzida → correction append-only
lacuna externa → BLOCKED_EXTERNAL
resultado não observado → TOKEN_VAZIO_TYPED
claim refutado → REJECTED_UNSUPPORTED
claim sustentado no escopo → CLOSED_PROVEN
```

É proibido converter ausência de evidência em evidência positiva apenas para “zerar pendências”. A conclusão do sistema é a conclusão **da classificação e da cadeia de custódia**, não a fabricação de resultados.

## 10. R3 do contrato

**F_ok:** método append-only/fail-closed, mapa operacional, estados, gates, F_ok/F_gap/F_next, hashes Drive do delta IGC e correção formal do GAP-005 existem.  
**F_gap:** CI observável; geometria canônica/colagem; Poincaré; GitHub raw hash + diff; ARM físico; enforcement global; reprodução independente; política numérica; Ω7/D7; reconciliação integral de corpus/receipts.  
**F_next:** executar P0 na ordem `claim gate → reconciliação/proveniência → CI → geometria/Poincaré → ARM/corpus receipts`; somente então promover claims dependentes.

**Regra final:** `TOKEN_VAZIO útil > conclusão inventada`.
