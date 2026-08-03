# RAFAELIA — Invariante de Autoria, Origem e Proveniência — V1

**Estado:** `CANONICAL_DRAFT / APPEND_ONLY / FAIL_CLOSED`  
**Data:** `2026-08-03T01:45:00-03:00`  
**Princípio:** `AUTHORSHIP_IS_INDISPENSABLE`  
**Claim:** `claim_allowed=false`

## 1. Pedra angular

A origem é uma constante estrutural do conhecimento. Quando a origem é apagada,
um resultado pode continuar circulando, mas perde contexto, responsabilidade,
direito de correção e possibilidade de auditoria.

```text
conhecimento sem origem verificável = informação com custódia incompleta
origem desconhecida ≠ domínio livre
origem desconhecida = TOKEN_VAZIO_AUTHORSHIP
```

A regra vale para Rafael, para colaboradores, instituições, autores históricos,
repositórios externos e ferramentas computacionais. Nenhuma reputação ou posição no
projeto autoriza apropriação de obra alheia.

## 2. Autoria não é um rótulo único

O sistema separa:

- **autor/coautor:** contribuição intelectual substancial, aprovação e responsabilidade;
- **autor da fonte:** criou a obra, teoria, texto, código, figura ou resultado anterior;
- **contribuidor:** realizou parte relevante, mas sem preencher o contrato de autoria;
- **desenvolvedor:** implementou código ou infraestrutura;
- **coletor de dados:** produziu ou reuniu observações;
- **editor:** reorganizou ou aprimorou expressão sem assumir a criação original;
- **tradutor/adaptador:** criou uma transformação identificável;
- **curador:** selecionou, classificou e preservou materiais;
- **revisor:** avaliou, criticou ou aprovou dentro de escopo declarado;
- **mantenedor:** possui responsabilidade operacional sobre o repositório;
- **instituição:** pode ser fonte, titular ou responsável editorial conforme evidência;
- **ferramenta de IA:** assistência declarada, sem responsabilidade autoral humana;
- **desconhecido:** estado auditável, nunca licença para atribuição automática.

A fórmula operacional é:

```text
AUTORIA = contribuição demonstrada + identidade + aprovação + responsabilidade
ATRIBUIÇÃO = origem + relação de uso + localização + revisão + escopo utilizado
```

## 3. Invariante geométrica do conhecimento

Defina o grafo de proveniência:

```text
G_A = (V, E)
```

Vértices:

```text
PERSON | INSTITUTION | SOURCE | ARTIFACT | CONCEPT | DATASET | CODE
TRANSFORMATION | REVIEW | LICENSE | TOKEN_VAZIO
```

Arestas:

```text
CREATED_BY | DERIVED_FROM | CITES | ADAPTS | TRANSLATES | IMPLEMENTS
REVIEWS | CURATES | REPRODUCES | INSPIRED_BY | GENERATED_WITH
SUPERSEDES_WITHOUT_ERASURE
```

A invariante é preservada quando toda transformação mantém um caminho navegável até
cada fonte conhecida:

```text
artifact_final → transformação → fonte@revisão → autor/titular
```

A versão mais recente não substitui a origem. Ela acrescenta uma nova camada.

## 4. Conceito, descoberta, expressão e implementação

É necessário separar quatro objetos:

1. **conceito ou ideia**;
2. **descoberta, dado ou resultado**;
3. **forma específica de expressão** — texto, figura, código, organização;
4. **implementação ou aplicação posterior**.

A legislação brasileira de direitos autorais protege criações expressas em suporte,
incluindo textos científicos, programas, bases de dados criativas e adaptações. A
mesma lei distingue essa proteção das ideias, métodos, sistemas e conceitos
matemáticos como tais. Essa distinção jurídica não elimina o dever acadêmico de citar
a origem intelectual de ideias, processos, resultados ou palavras utilizados.

Consequência RAFAELIA:

```text
não ser objeto de copyright como ideia isolada ≠ poder apagar a origem acadêmica
citação ética ≠ transferência de propriedade
implementação nova ≠ autoria da teoria anterior
```

Ao trabalhar com uma fonte histórica — por exemplo, um resultado associado a Mendel
ou qualquer outro pesquisador — o registro deve separar:

```text
autor/fonte histórica
intérprete moderno
edição consultada
implementador atual
contribuição original do RAFAELIA
```

Quando não for possível identificar qual “César”, “Cesária” ou outra referência foi
mencionada, registra-se `TOKEN_VAZIO_ENTITY_RESOLUTION`; o sistema não inventa a
identidade.

## 5. O que é tratado como risco de plágio

O gate bloqueia promoção quando houver indício de:

- palavras, código, dados, figuras, resultados ou estrutura distintiva usados sem
  âncora adequada;
- contribuição de terceiro apresentada como criação exclusiva do projeto;
- citação genérica que não permite localizar a parte utilizada;
- tradução, adaptação, compilação ou implementação que oculta a fonte anterior;
- autoria honorária — pessoa listada sem contribuição e responsabilidade;
- autoria fantasma — contribuinte elegível omitido;
- licença ou permissão necessária em estado desconhecido;
- origem desconhecida promovida como original;
- cópia de trabalho próprio anterior sem declarar reutilização, quando isso induzir o
  leitor a acreditar que se trata de conteúdo integralmente novo.

A auditoria não deve declarar “plágio comprovado” apenas por similaridade automática.
Ela registra evidência, escopo, intenção conhecida ou desconhecida, versão e direito de
resposta. Até revisão humana:

```text
PLAGIARISM_RISK_BLOCKED
claim_allowed=false
```

## 6. O que não basta para autoria

Isoladamente, não bastam:

- financiar;
- supervisionar genericamente;
- possuir o repositório;
- fornecer revisão gramatical;
- executar comandos sem contribuição intelectual;
- ser citado;
- ser uma ferramenta de IA;
- publicar primeiro um derivado sem revelar a fonte.

Esses atos podem receber crédito como contribuição, apoio, manutenção ou ferramenta.

## 7. Contrato mínimo por artefato

Todo artefato promotável deve possuir:

```text
record_id
artifact_locator
artifact_revision
content_digest_or_TOKEN_VAZIO
roles[]
contribution_statement por papel
origin_chain[]
originality_state
rights_state
citation_or_source_anchors[]
reviewer
blocking_token_vazio[]
claim_allowed
promotion_allowed
```

Para fontes digitais, usar quando disponível:

```text
repository + commit + path + blob_sha
Drive file_id + revision_id + export digest
paper DOI/versão/página/seção
arquivo local + hash + timestamp + parent receipt
```

## 8. Regra append-only e perpetuidade operacional

“Perpétuo” é implementado como objetivo de retenção e invariantes de não apagamento,
não como promessa física de armazenamento eterno.

- registros anteriores permanecem;
- correção cria novo registro com `previous_record_id`;
- remoção de nome exige justificativa, autoridade e receipt, preservando o evento;
- mudança de licença não reescreve a licença histórica;
- conflitos são marcados como `DISPUTED_AUTHORSHIP`;
- backups sem teste de restauração permanecem `TOKEN_VAZIO`.

## 9. Auditoria contínua

A cada PR ou publicação relevante, verificar:

1. todos os autores e contribuidores estão identificados?
2. cada papel possui declaração de contribuição?
3. as fontes usadas têm localização e revisão?
4. adaptações e traduções estão marcadas?
5. direitos e licença são compatíveis?
6. assistência de IA foi declarada?
7. há autor elegível omitido ou autor sem contribuição?
8. existe `TOKEN_VAZIO` bloqueante?
9. o revisor avaliou o mesmo commit que será promovido?
10. a correção preserva o histórico anterior?

## 10. Fontes normativas e boas práticas consideradas

- Brasil, Lei nº 9.610/1998: obras protegidas, distinção entre expressão e ideias,
  direitos morais e patrimoniais do autor;
- Brasil, Lei nº 9.609/1998: proteção de programas de computador e direito de
  reivindicar paternidade do programa;
- WIPO: distinção entre direitos econômicos e morais, incluindo atribuição e
  integridade;
- ORI: plágio em pesquisa como apropriação sem crédito adequado, distinguindo-o de
  erro honesto e de certas disputas de crédito;
- ICMJE: autoria ligada a contribuição substancial, revisão intelectual, aprovação
  final e responsabilidade; contribuidores que não atendem aos critérios devem ser
  reconhecidos sem autoria indevida.

Essas referências orientam a governança; não substituem análise jurídica ou norma
específica de cada periódico, licença, instituição ou país.

## 11. Artefatos desta implementação

- `AUTHORS_RAFAELIA.md`;
- `data/control-plane/authorship-provenance-policy.v1.json`;
- `schemas/authorship-provenance-record.schema.json`;
- `data/authorship/authorship_registry.delta.20260803.jsonl`;
- `tools/verify_authorship_provenance.py`;
- `tests/test_authorship_provenance.py`;
- `.github/workflows/authorship-provenance.yml`;
- índice append-only do ciclo.

## R₃

**F_ok:** autoria, contribuição, origem, transformação, direitos e assistência de IA
foram separados em papéis auditáveis.  
**F_gap:** cobertura retroativa de todos os repositórios, reconciliação de licenças e
revisão independente permanecem incompletas.  
**F_next:** validar o registro, selar blobs pós-commit e exigir o gate nas próximas
promoções de conhecimento.
