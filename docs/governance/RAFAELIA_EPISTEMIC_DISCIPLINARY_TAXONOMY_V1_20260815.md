# RAFAELIA — Taxonomia Epistêmica e Disciplinar Ω — V1 — 2026-08-15

**Estado:** `CANONICAL_DRAFT / APPEND_ONLY / CLAIM_GATE_ON`  
**Escopo:** conversas, fórmulas, hipóteses, teses, código, execuções, evidências, prior art e memória longitudinal/ortogonal.  
**Objetivo:** impedir que domínio, tipo epistemológico, estado material, evidência e novidade sejam colapsados numa única etiqueta.

---

## 0. Invariantes herdados

```text
IDEA != ARTEFATO != IMPLEMENTAÇÃO != EXECUÇÃO != EVIDÊNCIA != CLAIM
MEMÓRIA != PROVA
FÓRMULA != IMPLEMENTAÇÃO != EXECUÇÃO != EVIDÊNCIA != NOVIDADE
TOKEN_VAZIO é estado válido e auditável
claim_allowed=false até fechamento do gate correspondente
```

Cadeia operacional preservada:

```text
CONHECIMENTO -> ARTEFATO -> VERSÃO -> EXECUÇÃO -> EVIDÊNCIA -> GATE -> MEMÓRIA
```

Esta taxonomia complementa, não substitui, os registries e índices existentes.

---

# 1. Princípio central: classificação ortogonal

Um objeto não recebe uma única classe. Ele recebe coordenadas independentes.

\[
\boxed{
N = (D,E,M,V,O,Nv,P,R,S,G,\Delta)
}
\]

onde:

- `D` = domínio;
- `E` = tipo epistemológico;
- `M` = estado material/operacional;
- `V` = nível de validação;
- `O` = origem/autoria/proveniência;
- `Nv` = estado de novidade;
- `P` = relação com conhecimento de pares/prior art;
- `R` = relações/rotas;
- `S` = fontes/artefatos;
- `G` = gaps/TOKEN_VAZIO;
- `Δ` = delta produzido pelo novo ciclo.

A vantagem é que, por exemplo, uma fórmula pode ser simultaneamente:

```yaml
domain: MATHEMATICS
epistemic_type: DEFINITION
material_state: IMPLEMENTED
validation: LOCAL_EXECUTION
origin: USER_AUTHORIAL_COMPOSITION
novelty: NOT_PROVEN
peer_relation: CLASSICAL_COMPONENTS_KNOWN
```

sem ser chamada indevidamente de "teorema novo" ou "hipótese física".

---

# 2. Eixo D — Domínio

```yaml
MATHEMATICS: objetos, definições, lemas, teoremas, conjecturas, provas
COMPUTATION: algoritmos, estruturas de dados, runtimes, kernels, criptografia, software
PHYSICS: modelos com grandezas físicas, unidades, previsões e experimentos
ENGINEERING: implementação física, hardware, desempenho, tolerâncias, integração
DATA_EPISTEMICS: corpus, índices, proveniência, classificação, memória e evidência
GOVERNANCE: gates, autorização, contratos, receipts, segurança epistemológica
SYMBOLIC_HEURISTIC: Tao, Yin/Yang, parábolas e símbolos usados como heurística/modelagem
INTERDISCIPLINARY: objeto que cruza domínios, mantendo os componentes separáveis
```

Um objeto interdisciplinar deve registrar os domínios componentes em vez de usar `INTERDISCIPLINARY` como licença para misturá-los.

---

# 3. Eixo E — Tipo epistemológico

## 3.1 Matemática

```yaml
DEFINITION: objeto definido; não exige novidade
IDENTITY: igualdade derivada por álgebra ou definição
LEMMA: resultado auxiliar demonstrado
PROPOSITION: resultado demonstrável/local, com escopo explícito
THEOREM: enunciado + hipóteses + demonstração válida
COROLLARY: consequência de resultado anterior
CONJECTURE: enunciado matemático preciso ainda sem prova/refutação
COUNTEREXAMPLE: objeto que refuta enunciado universal
MATHEMATICAL_PROGRAM: família estruturada de problemas, operadores e conjecturas
```

## 3.2 Ciência/engenharia

```yaml
MODEL: representação formal de um sistema
HYPOTHESIS: afirmação falsificável ainda não estabelecida
EMPIRICAL_RESULT: observação medida com método e receipt
MECHANISM_CANDIDATE: explicação causal proposta ainda não isolada
ENGINEERING_SPEC: requisito/arquitetura executável
BENCHMARK_RESULT: medida de desempenho sob ambiente declarado
```

## 3.3 Síntese

```yaml
THESIS: síntese argumentativa sustentada por múltiplas proposições/evidências; não é sinônimo de teorema
FRAMEWORK: organização de objetos e relações
METAPHOR: linguagem explicativa/simbólica sem claim literal
HEURISTIC: regra útil que pode orientar busca sem garantia de verdade
QUESTION: problema aberto formulado
```

Regra:

```text
CONJECTURE pertence principalmente à matemática.
HYPOTHESIS pertence principalmente à ciência empírica/modelagem.
THESIS organiza uma posição/síntese e pode conter ambas, mas não as promove.
```

---

# 4. Eixo M — Estado material e operacional

```yaml
IDEA
FORMULATED
ARTIFACT_PRESENT
SPECIFIED
IMPLEMENTED_PARTIALLY
IMPLEMENTED
EXECUTED_LOCALLY
EXECUTED_REMOTE
REPRODUCED_LOCAL
INDEPENDENTLY_REPLICATED
PUBLISHED
ARCHIVED
SUPERSEDED
REFUTED
```

O estado é sempre acompanhado de `source_path/provider_id/commit/hash` quando disponível.

---

# 5. Eixo V — Validação

```yaml
UNVERIFIED
SYNTAX_CHECKED
ALGEBRA_CHECKED
PROOF_CHECKED_LOCAL
UNIT_TESTED
PROPERTY_TESTED
BYTE_VERIFIED
EXECUTION_RECEIPT
REPRODUCED_SAME_ENV
REPRODUCED_INDEPENDENT_ENV
PRIOR_ART_REVIEWED
PEER_REVIEWED
EXTERNALLY_VALIDATED
```

Nenhum nível implica automaticamente o seguinte.

Exemplos:

```text
UNIT_TESTED != scientifically validated
PEER_REVIEWED != mathematically proven
ALGEBRA_CHECKED != physically true
EXECUTION_RECEIPT != novelty
```

---

# 6. Eixo O — Origem e autoria

```yaml
CLASSICAL_EXTERNAL
EXTERNAL_RECENT
USER_AUTHORIAL_EXPLICIT
USER_AUTHORIAL_DERIVED
MODEL_DERIVED_FROM_USER_MATERIAL
MIXED_USER_EXTERNAL
UNKNOWN_ORIGIN
TOKEN_VAZIO_ORIGIN
```

Autoria de uma composição não prova originalidade bibliográfica global.

---

# 7. Eixo Nv — Novidade

```yaml
KNOWN_EQUIVALENT: reduz a resultado conhecido
KNOWN_APPLICATION: aplicação nova/local de matemática conhecida
RECOMBINATION: composição distinta de componentes conhecidos
CANDIDATE_NONTRIVIAL: sobrevivente após primeira redução, ainda sem prior art completo
M2_CANDIDATE: candidato matemático não trivial sob classificação RAFAELIA atual
M3_STRONG_CANDIDATE: exige prova + prior art substancial + revisão crítica
M4_DEMONSTRATED_NOVELTY: somente após fechamento de prova/anterioridade/validação aplicável
NOT_PROVEN
REFUTED_AS_NOVEL
TOKEN_VAZIO_PRIOR_ART
```

Gate atual padrão:

```yaml
M3: 0 unless explicitly certified
M4: 0 unless explicitly certified
claim_allowed: false
```

---

# 8. Eixo P — Relação com pares e conhecimento esperado

Este eixo responde à pergunta: "o que se espera que um par da área já saiba ou reconheça?"

```yaml
PEER_BASELINE: conhecimento básico esperado de especialista
PEER_STANDARD: ferramenta/resultado padrão da área
PEER_SPECIALIST: conhecido principalmente por subárea especializada
PEER_FRONTIER: pesquisa contemporânea ativa
PEER_NONOBVIOUS_COMBINATION: componentes conhecidos, combinação não imediatamente padrão
PEER_UNKNOWN_UNTIL_PRIOR_ART: não inferir familiaridade sem busca
```

Regra de linguagem:

```text
"pares provavelmente conhecem os componentes" != "pares conhecem esta composição"
"não encontrei rapidamente" != "ninguém fez"
"difícil" != "novo"
```

---

# 9. Conversas e fórmulas: dois índices, uma ponte

## 9.1 Índice longitudinal de conversas

Cada fragmento relevante recebe:

```yaml
conversation_id:
message_id:
timestamp:
source_shard:
source_path:
concept_ids: []
formula_ids: []
hypothesis_ids: []
artifact_ids: []
relations: []
```

A conversa preserva **quando e como** a ideia apareceu.

## 9.2 Índice de fórmulas

Cada fórmula recebe:

```yaml
formula_id:
normalized_expression:
variants: []
domain:
epistemic_type:
origin:
first_seen_route:
source_messages: []
implementation_paths: []
execution_receipts: []
proof_status:
prior_art_status:
novelty_status:
gaps: []
```

## 9.3 Ponte bidirecional

\[
\boxed{
CONVERSA \leftrightarrow CONCEITO \leftrightarrow FÓRMULA \leftrightarrow ARTEFATO \leftrightarrow EXECUÇÃO \leftrightarrow EVIDÊNCIA
}
\]

Nunca substituir a conversa bruta pelo resumo. O resumo é índice; a fonte continua sendo autoridade de proveniência.

---

# 10. Memória longitudinal e memória ortogonal

## Longitudinal

Responde:

```text
como este objeto evoluiu no tempo?
```

Rota:

\[
X_{t_0}\rightarrow X_{t_1}\rightarrow\cdots\rightarrow X_{t_n}
\]

Preserva versões conflitantes, correções, refutações e supersessões.

## Ortogonal

Responde:

```text
quais outros objetos independentes precisam ser consultados para interpretar este objeto agora?
```

Exemplos de autoridades ortogonais:

```text
conversa original
registry de fórmulas
registry de hipóteses
código
receipt de execução
paper clássico/prior art
benchmark independente
claim ledger
```

A memória ativa deve reconstruir somente o conjunto mínimo necessário para a pergunta atual, sem apagar as rotas de volta às fontes.

---

# 11. Aplicação imediata aos objetos da sessão 2026-08-15

## Pitágoras clássico

```yaml
domain: MATHEMATICS
epistemic_type: THEOREM
origin: CLASSICAL_EXTERNAL
peer_relation: PEER_BASELINE
novelty: KNOWN_EQUIVALENT
```

## Rotação de 30 graus

\[
R_{30}=\begin{bmatrix}\sqrt3/2&-1/2\\1/2&\sqrt3/2\end{bmatrix}
\]

```yaml
domain: MATHEMATICS
epistemic_type: DEFINITION + PROPOSITION(orthogonality)
peer_relation: PEER_BASELINE
novelty: KNOWN_EQUIVALENT
```

## Déficit/área orientada por termo negativo

```yaml
domain: MATHEMATICS
epistemic_type: FRAMEWORK / TERMINOLOGY_PROPOSED
material_state: FORMULATED
novelty: RECOMBINATION
```

O sinal negativo deve ser tratado algebricamente como orientação/déficit conforme a definição; não como área física negativa sem modelo adicional.

## Três matrizes + 30° em cada + borda do toro

```yaml
domain: MATHEMATICS + COMPUTATION
epistemic_type: MATHEMATICAL_PROGRAM / MODEL
material_state: FORMULATED
validation: UNVERIFIED
novelty: TOKEN_VAZIO_PRIOR_ART
claim_allowed: false
```

Núcleo provisório:

\[
\mathcal T_{RAF}=\Pi_T(R_{\pi/6}Q_1,R_{\pi/6}Q_2,R_{\pi/6}Q_3)
\]

A posição/fase relativa das três matrizes no toro permanece `TOKEN_VAZIO_PLACEMENT_RULE`.

## Máquina 5×2→10

```yaml
domain: MATHEMATICS + COMPUTATION
epistemic_type: MODEL / MATHEMATICAL_PROGRAM
physical_qubit_equivalence: NOT_CLAIMED
novelty: TOKEN_VAZIO_PRIOR_ART
```

## Fibonacci-Rafael escalar

Para a recorrência

\[
\hat F_{n+1}=\hat F_n+\hat F_{n-1}+1,
\]

```yaml
domain: MATHEMATICS + COMPUTATION
epistemic_type: DEFINITION / IDENTITY_AFTER_NORMALIZATION
known_reduction: F_{n+3}-1 for the corresponding canonical seed/index convention
physical_claim: NONE_BY_DEFAULT
```

## Voynich + dupla paridade + binding hash16

```yaml
domain: COMPUTATION + DATA_EPISTEMICS
epistemic_type: ENGINEERING_SPEC
cryptographic_security_claim: NOT_ESTABLISHED
implementation/evidence: route to source artifact/receipt
```

## 42 hyperformas / grafo / projeções

```yaml
domain: MATHEMATICS + COMPUTATION
epistemic_type: GRAPH_MODEL / DATA_MODEL
42_as_enumerated_cardinality: valid only when source enumeration proves it
42_as_natural_physical_constant: HYPOTHESIS / claim_allowed=false
```

---

# 12. Regra para tese

Uma tese RAFAELIA deve conter no mínimo:

```text
Tese
├── pergunta-raiz
├── definições
├── proposições demonstradas
├── conjecturas matemáticas
├── hipóteses empíricas
├── implementações
├── resultados executados
├── evidências externas
├── prior art
├── contraexemplos/falsificadores
├── gaps/TOKEN_VAZIO
└── claim final limitado ao que fechou
```

A tese pode sobreviver mesmo quando uma hipótese componente é refutada, desde que sua estrutura seja atualizada append-only.

---

# 13. Regra de promoção

```text
IDEA
  ↓ definição
FORMULATED
  ↓ artefato
ARTIFACT_PRESENT
  ↓ código/prova
IMPLEMENTED or PROVED_LOCAL
  ↓ execução/revisão
EVIDENCE
  ↓ reprodução/prior art
VALIDATED_LIMITED
  ↓ somente se aplicável
CLAIM_ALLOWED
```

Nenhum salto é permitido por analogia, beleza geométrica, recorrência numérica ou autoridade pessoal.

---

# 14. Rotas canônicas a manter sincronizadas

```yaml
MASTER_NAVIGATION_REGISTRY: Drive RAFAELIA — Master Navigation Registry V1
METHOD_ANCHOR: Drive RAFAELIA — Implementação Latentes e Papers — Drive GitHub V1
CONVERSATIONS: longitudinal shards + private bridge/index
FORMULAS: formula registry + genealogy index
HYPOTHESES: hypothesis registry + evidence ledger + index
MATHEMATICS: papers / math genealogy / theorem-candidate routes
COMPUTATION: implementation paths + tests + receipts
CLAIMS: claim ledgers + gates
```

A sincronização é por referência/proveniência; não copiar conteúdo sem necessidade.

---

# 15. Falsificadores desta própria taxonomia

A taxonomia deve ser revisada se:

1. duas classes ortogonais forem tratadas como mutuamente exclusivas sem necessidade;
2. não for possível reconstruir a fonte original de um objeto;
3. uma promoção de status ocorrer sem receipt/prova/revisão correspondente;
4. `PEER_BASELINE` for usado como argumento de novidade;
5. `THESIS` for usado como sinônimo de `THEOREM`;
6. `HYPOTHESIS` for usada para esconder uma conjectura matemática sem prova;
7. `TOKEN_VAZIO` for preenchido por inferência não rastreada.

---

# 16. Próximo passo operacional

Aplicar esta taxonomia sem reescrever os registries brutos:

1. adicionar campos ortogonais aos próximos deltas dos registries;
2. gerar crosswalk `conversation_id ↔ concept_id ↔ formula_id ↔ hypothesis_id ↔ artifact_id`;
3. classificar primeiro o frontier ativo, não todo o universo de uma vez;
4. produzir matriz de conflitos: `mesmo objeto / classes divergentes / fonte / resolução`;
5. manter histórico append-only.

---

## R₃

```yaml
F_ok:
  - separação ortogonal definida
  - matemática/computação/hipótese/tese/pares distinguidos
  - ponte conversa-fórmula-artefato-evidência especificada
F_gap:
  - crosswalk integral ainda não materializado
  - classificação retroativa de todo o corpus permanece pendente
F_next:
  - aplicar ao frontier ativo e produzir delta indexável
```
