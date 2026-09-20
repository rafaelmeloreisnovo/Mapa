# RAFAELIA — Rollback Canônico de Escopo Autoral / Berna — V2

**Status:** `CANONICAL_ROLLBACK_ACTIVE / LEGAL_REVIEW_REQUIRED / claim_allowed=false`  
**Data:** 2026-09-20  
**Autor/curadoria:** Rafael Melo Reis / RAFAELIA  
**Parent:** `docs/legal/INTERNATIONAL_AUTHORSHIP_TREATY_DOCTRINE_V1.md`  
**Supersedes (governance priority only):** `docs/legal/HUMANITY_PROTECTION_AND_ACCESS_COVENANT_V1.md`

## 0. Intenção do rollback

Restaurar a doutrina de Berna/autoria/proveniência como **rota canônica primária** para o corpus RAFAELIA de autoria ou titularidade demonstrável de Rafael Melo Reis.

Este rollback:
- não apaga o histórico de 2026-09-19;
- não revoga permissões que já tenham sido validamente concedidas por GPL, MIT, CC ou outro instrumento;
- não transforma Berna em licença privada;
- não reivindica direitos de terceiros;
- não converte ideias, métodos, sistemas, fatos ou conceitos matemáticos abstratos em objeto de copyright.

## 1. Regra-mãe restaurada

```text
SOURCE != AUTHORSHIP != COPYRIGHT != LICENSE != PATENT != TRADEMARK != TREATY != EVIDENCE
BERNE_PROTECTION != LICENSE_GRANT
PUBLIC_REPOSITORY != PUBLIC_DOMAIN
PROVENANCE != OWNERSHIP_JUDGMENT
TOKEN_VAZIO != CLEARED
```

A Convenção de Berna é a camada internacional de proteção autoral aplicável às obras protegidas, articulada com a legislação brasileira e com a licença concreta de cada artefato.

## 2. Escopo de "todos os conhecimentos"

Para governança RAFAELIA, "todos os conhecimentos" significa **reintegrar ao mapa de proveniência** todas as classes de produção do corpus, quando existirem fontes verificáveis:

- textos, livros, manifestos e documentação;
- código-fonte e software original;
- diagramas, figuras e composições autorais;
- papers, drafts, hipóteses e cadernos de pesquisa;
- prompts, taxonomias, ontologias e estruturas de organização;
- datasets e compilações autorais, nos limites dos direitos sobre seleção/organização e dos direitos incidentes sobre os dados;
- fórmulas, teoremas, métodos, descobertas, observações e modelos como **objetos de proveniência e pesquisa**, sem afirmar copyright sobre o conteúdo abstrato quando a lei não o protege;
- receipts, hashes, commits, timestamps e cadeias de custódia como evidência de integridade/proveniência, não como sentença automática de titularidade.

```text
KNOWLEDGE_IN_CORPUS -> PROVENANCE_MAP
COPYRIGHTABLE_EXPRESSION -> COPYRIGHT_ROUTE
ABSTRACT_IDEA_METHOD_FACT_MATH -> PROVENANCE_ONLY + OTHER_RIGHTS_IF_APPLICABLE
THIRD_PARTY_OR_MIXED -> UPSTREAM_RIGHTS_CONTROL
```

## 3. Efeito sobre o Humanity Covenant V1

O `HUMANITY_PROTECTION_AND_ACCESS_COVENANT_V1.md` permanece histórico e útil para:
- preservação da autoria de terceiros;
- não apagamento de NOTICE/SPDX/licenças upstream;
- regras de privacidade, segurança e dignidade;
- acesso quando existir licença explícita e autoridade para concedê-la.

Ele deixa de ser a camada de prioridade para decidir abertura do material RAFAELIA-original.

Nova precedência:

```text
MANDATORY_LAW
-> VALID_TREATY / BRAZILIAN_LAW
-> FILE_OR_COMPONENT_UPSTREAM_LICENSE
-> EXISTING_VALID_LICENSE_OR_CONTRACT
-> BERNE_AUTHORIAL_SCOPE_ROLLBACK_V2
-> HUMANITY_ACCESS_COVENANT_V1 (subordinate, rights-cleared only)
-> SYMBOLIC_OR_PARABOLIC_LANGUAGE
```

## 4. Proteção automática e Brasil

A proteção de Berna não depende de formalidade como condição de proteção. No Brasil, a Convenção de Berna (revisão de Paris de 1971) foi promulgada pelo Decreto nº 75.699/1975. A Lei nº 9.610/1998 protege obras e certas compilações, mas exclui ideias, sistemas, métodos, projetos e conceitos matemáticos como tais; em ciência, a proteção autoral recai sobre a forma de expressão, não sobre o conteúdo técnico/científico em si. Software possui regime próprio pela Lei nº 9.609/1998 e sua proteção independe de registro.

## 5. Rollback operacional

A partir deste sucessor:

1. todo índice novo de autoria deve apontar primeiro para este V2;
2. todo conhecimento RAFAELIA recuperado deve receber provenance/source antes de qualquer claim;
3. nenhuma abertura/licença nova é inferida pelo Humanity Covenant;
4. licenças já existentes continuam regendo o material ao qual se aplicam;
5. material original sem licença explícita não deve ser tratado como domínio público apenas por estar em repositório público;
6. material misto é auditado por arquivo/diretório;
7. terceiro/upstream nunca é absorvido como autoria RAFAELIA;
8. `TOKEN_VAZIO` bloqueia apenas o claim/relicenciamento afetado e permanece visível.

## 6. Inventário lógico restaurado

```text
RAFAELIA_ORIGINAL_EXPRESSION = RESTORE_AUTHORIAL_ROUTE
RAFAELIA_PROVENANCE_GRAPH = RESTORE_ALL_KNOWN_NODES
FORMULAS_DISCOVERIES_MODELS = RESTORE_PROVENANCE, NOT ABSTRACT_COPYRIGHT_CLAIM
CODE_ORIGINAL = SOFTWARE_COPYRIGHT_ROUTE
PAPERS_TEXT_FIGURES = COPYRIGHT_ROUTE + PUBLISHER/LICENSE_BOUNDARY
DATASETS = COMPILATION/DATABASE/PRIVACY/CONTRACT_BOUNDARY
UPSTREAM = PRESERVE_UPSTREAM_LICENSE_AND_AUTHORSHIP
UNKNOWN = TOKEN_VAZIO
```

## 7. Fontes oficiais

- WIPO — Berne Convention summary: tratamento nacional, proteção automática e independência da proteção.
- Brasil — Decreto nº 75.699/1975: promulga a Convenção de Berna revista em Paris em 1971.
- Brasil — Lei nº 9.610/1998: direitos autorais e limites para ideias/métodos/fatos/conteúdo científico.
- Brasil — Lei nº 9.609/1998: proteção de programa de computador e independência de registro.

## 8. Não retroatividade fictícia

Este documento restaura a **governança autoral canônica** do projeto. Ele não pode, sozinho, desfazer licenças ou contratos válidos já concedidos a terceiros. Onde houver licença pública prévia, o rollback é de política interna/proveniência para versões e materiais futuros ou não licenciados, respeitando os grants anteriores.

## R3

**F_ok:** Berna/autoria/proveniência voltam a ser a rota canônica primária; todas as classes de conhecimento são reintegradas ao mapa de proveniência.  
**F_gap:** titularidade/licença precisa continua arquivo-específica; revogação de grants anteriores não é presumida; patente, segredo, marca e contratos exigem trilhas próprias.  
**F_next:** federar este V2 para RafGitTools, RafPolimata, papers, CientiEspiritual, ZIPRAF_CORE, Cosmos, ChipQuantum, TeoremasTesesTeorias e CreFeBerna; registrar Drive receipt.

`μID=MU-BERNE-ROLLBACK-V2-20260920 | ts=2026-09-20T02:19:00-03:00 | parent=INTERNATIONAL_AUTHORSHIP_TREATY_DOCTRINE_V1 | kind=LEGAL_GOVERNANCE_ROLLBACK | state=CANONICAL_ROLLBACK_ACTIVE | claim_allowed=false`
