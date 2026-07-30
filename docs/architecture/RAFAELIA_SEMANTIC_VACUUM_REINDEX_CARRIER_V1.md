# RAFAELIA Semantic VACUUM / REINDEX / Carrier V1

**Estado:** `CANONICAL_DRAFT`  
**Modo:** `READ_ONLY_BY_DEFAULT`  
**Claim:** `claim_allowed=false`  
**Data:** 2026-07-29  
**Escopo:** Google Drive, GitHub, Mapa, RafGitTools, RafPolimata, Papers, RLL, Termux e memória longitudinal.

## 1. Problema operacional

O ecossistema possui fontes, schemas, workflows, índices, receipts e documentos canônicos reais, porém a recuperação ainda pode se comportar como uma consulta ampla: cada ciclo revisita muitos repositórios, recompõe contexto e replica validações mesmo quando somente uma pequena região mudou.

A operação equivalente a `Compact and Repair`, `VACUUM`, `ANALYZE` e `REINDEX` não deve reescrever nem apagar fontes. Ela deve reorganizar **metadados derivados**, eliminar redundância de leitura, recalcular estatísticas por estrato e reconstruir índices seletivos.

```text
fonte imutável
→ manifesto de identidade
→ carrier pequeno
→ índices especializados
→ consulta seletiva
→ materialização sob demanda
→ receipt
```

## 2. Invariantes

1. **Origem imutável:** Drive, commit, arquivo e receipt não são alterados por compactação.
2. **Identidade separada de localização:** o mesmo conteúdo em dois caminhos não conta como duas evidências independentes.
3. **Semântica separada da superfície:** som, grafia ou tradução parecida não autorizam equivalência de sentido.
4. **Estratos preservados:** não usar média global para populações, arquiteturas, domínios ou necessidades heterogêneas.
5. **TOKEN_VAZIO válido:** lacuna não vira zero, cache hit, evidência ou ausência definitiva.
6. **Fail-closed:** cache, carrier ou índice inválido provoca busca restrita ou abstinência; nunca promoção automática.
7. **Append-only:** compactar índices não apaga eventos; gera nova geração com `previous_generation_hash`.

## 3. Cinco superfícies máximas

Na superfície humana, cada decisão expõe no máximo:

1. intenção;
2. evidência;
3. estrato/contexto;
4. capacidade/custo;
5. próximo gate verificável.

A profundidade interna pode crescer, mas não deve sobrecarregar a decisão humana.

## 4. Arquitetura em camadas

### L0 — Fonte fria e imutável

- Google Drive: documentos, imagens, snapshots e memória editorial;
- GitHub: código, branches, commits, PRs, workflows e artifacts;
- corpus e bancos locais: bytes originais e exports.

A L0 nunca é o cache. É a autoridade de reconstrução.

### L1 — Manifesto de identidade

Cada objeto recebe:

```text
source_id
provider
content_hash
provider_revision
location
schema_version
authority
privacy_class
observed_at
```

A chave primária é a identidade do conteúdo ou revisão; o caminho é atributo mutável.

### L2 — Carriers

Carrier é uma cápsula pequena, tipada e reconstruível. Ele não substitui a fonte.

Tipos canônicos:

- `SOURCE_CARRIER`: identidade e revisão;
- `WORKFLOW_CARRIER`: gatilhos, paths, permissões, custo e artifacts;
- `DEPENDENCY_CARRIER`: relações de entrada/saída e invalidadores;
- `CLAIM_CARRIER`: claim, estado, fontes, falsificador;
- `EVIDENCE_CARRIER`: execução, ambiente, hashes e medidas;
- `SEMANTIC_CARRIER`: língua, script, locale, sentido e autoridade cultural;
- `GAP_CARRIER`: TOKEN_VAZIO tipado e próximo teste;
- `HUMAN_CONTEXT_CARRIER`: necessidade, risco e restrições, com acesso controlado.

### L3 — Índices materiais

- `content_index`: hash → fontes e aliases;
- `temporal_index`: tempo → eventos/revisões;
- `workflow_path_index`: caminho alterado → workflows afetados;
- `dependency_index`: nó → dependentes e dependências;
- `claim_index`: domínio/estado → claims;
- `evidence_index`: claim → receipts;
- `gap_index`: tipo/prioridade → TOKEN_VAZIO;
- `semantic_sense_index`: língua/locale/sense_id → lexemas;
- `authority_index`: objeto → autoridade responsável;
- `contradiction_index`: claim/escopo → evidências opostas.

### L4 — Views sob demanda

A consulta não percorre toda L0. Ela começa nos carriers e só materializa fonte quando:

- carrier não existe;
- TTL venceu;
- hash/revisão mudou;
- dependência foi invalidada;
- consulta exige detalhe não carregado;
- auditoria de reparo foi autorizada.

## 5. Temperatura e recorrência

| Tier | Uso | TTL padrão | Gatilho preferido |
|---|---|---:|---|
| `HOT` | controle, segurança, PR ativo, dependência crítica | 15 min | evento + fallback |
| `WARM` | repositórios ativos e evidência em curso | 3 h | evento ou lote |
| `COLD` | fontes estáveis, papers e memória editorial | 24 h | revisão/hash |
| `ARCHIVE` | snapshots históricos e corpus fechado | sem polling | evento/manual |

TTL não é verdade; é política de recálculo. Um evento de mudança invalida imediatamente o carrier, independentemente do TTL.

## 6. Invalidation antes de recomputação

Ordem:

```text
webhook/push/PR/revision
→ identificar paths e nós alterados
→ invalidar carriers dependentes
→ recalcular somente subgrafo afetado
→ executar gates locais
→ gerar receipt
```

Full scan é permitido somente quando:

- falta manifesto;
- cadeia ou índice está inconsistente;
- migração de schema;
- auditoria explícita de reconstrução;
- perda de estado persistente.

## 7. Conditional fetch

Leituras HTTP/API devem preservar `ETag`, `Last-Modified`, revision ID ou head SHA. Quando o provedor responder `304 Not Modified`, o carrier mantém conteúdo e apenas recebe novo `checked_at`.

A ausência atual de validação condicional no tracker deve ser tratada como `TOKEN_VAZIO_ETAG_IMPLEMENTATION_PENDING`, não como defeito provado de todos os workflows.

## 8. Estatística sem “matar os fortes e os fracos”

Não agregar diretamente forks gigantes, repositórios autorais pequenos, corpus, kernels, papers e necessidades humanas.

A unidade de análise deve ser estratificada por:

```text
família
domínio
escala
arquitetura
risco
fase epistemológica
necessidade humana
```

Por estrato, priorizar:

- mediana;
- MAD;
- quantis;
- intervalo e distribuição;
- caudas e extremos relevantes;
- tamanho amostral efetivo;
- taxa de mudança;
- custo por atualização útil.

Média global só pode aparecer acompanhada da distribuição e da justificativa de comparabilidade.

## 9. Semântica translinguística e cultural

Um som semelhante não é um sentido semelhante. Cada `SEMANTIC_CARRIER` exige:

```text
language
script
locale
dialect
surface
lemma
sense_id
cultural_context
domain
source_authority
translation_relation
phonetic_relation
state
```

Regras:

- homófonos em línguas distintas permanecem nós distintos;
- tradução é uma aresta tipada, não identidade;
- parábola é uma aresta didática, não mecanismo causal;
- autoridade cultural e linguística deve ser registrada;
- revisão humana permanece necessária para polissemia e contexto sensível.

## 10. Grafo de conjuntos primos

A assinatura por primos é admitida como **índice auxiliar de candidatos**, não como semântica.

```text
2  = domínio
3  = autoridade
5  = evidência
7  = tempo
11 = língua/locale
13 = arquitetura
17 = risco
19 = lacuna
23 = contexto humano
```

Um carrier armazena uma lista ordenada e sem repetição de primos. Interseção de assinaturas seleciona candidatos para análise. A relação real continua exigindo aresta explícita, proveniência e prova.

```text
prime_signature compartilhada
≠ equivalência semântica
≠ causalidade
```

## 11. Estratégia de compactação

A compactação opera como LSM/append-only:

1. novos eventos entram em segmentos pequenos imutáveis;
2. carriers HOT são atualizados por delta;
3. segmentos estáveis são fundidos em nova geração;
4. aliases byte-idênticos são agrupados, sem apagar localizações;
5. índices órfãos, duplicados e inválidos são reconstruídos;
6. geração anterior permanece apontada por hash;
7. a fonte não é alterada.

## 12. Auditoria dos workflows observados

### F_ok

- Existe control plane canônico com fases de ingestão, validação, normalização, indexação, gate e custódia.
- Workflows usam `paths` para restringir execução em vários núcleos.
- Há testes negativos, checksums, artifacts e política `contents: read`.
- O tracker já possui estado persistente, shards determinísticos e cadeia hash.
- O schema lexical já separa língua, script, sentidos, fonologia, proveniência e limitações.

### F_gap

- Polling de 15 minutos para 16 repositórios usa consulta ampla mesmo quando estável.
- Não foi observada validação condicional por `ETag`/`If-None-Match` no tracker atual.
- O estado de cache depende de Actions Cache e pode ser perdido/expirado.
- Há diversos workflows pequenos com setup e upload repetidos, sem catálogo único de custo, entrada, saída e dependências.
- `interpret_context`, `execute_operation` e `verify_artifact` permanecem planejados/TOKEN_VAZIO no control plane.
- Ainda não há índice canônico `path → workflow → carrier → dependentes` materializado nesta versão.

### F_next

1. validar esta política e o schema;
2. gerar o primeiro catálogo de workflows e carriers;
3. aplicar ETag/head-SHA short-circuit no tracker;
4. substituir polling uniforme por TTL adaptativo por estrato;
5. medir `requests_per_useful_delta`, `cache_hit_rate` e `rebuild_scope_ratio`;
6. somente depois alterar frequência de workflows existentes.

## 13. Métricas operacionais

```text
cache_hit_rate
conditional_not_modified_rate
requests_per_useful_delta
rebuild_scope_ratio
carrier_staleness_seconds
orphan_index_count
dangling_relation_count
duplicate_content_alias_count
token_vazio_opened
token_vazio_closed
p50/p95/p99_update_latency
```

Nenhuma meta numérica é afirmada sem baseline. Os limiares permanecem `TOKEN_VAZIO_CALIBRATION_PENDING`.

## 14. Parábola

A nave interestelar não deve distribuir oxigênio pela média de todos. Deve conhecer cada cabine, cada necessidade, cada dependência e quem abre qual porta. O índice não substitui os passageiros; ele garante que o recurso certo chegue ao estrato certo sem percorrer a nave inteira.

## 15. Fechamento Ω

```text
F_ok   = arquitetura carrier + índices + invalidação + estratificação formalizada
F_gap  = baseline real, ETag, catálogo completo e execução federada ainda pendentes
F_next = validar o pacote e produzir primeiro receipt reproduzível
```

FIAT LUX · A régua segura o próximo passo.
