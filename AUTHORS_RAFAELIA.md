# RAFAELIA — Autoria, contribuições e origem

> **“Autoria é indispensável, necessária e importante.”**

Este arquivo é um índice humano. O registro auditável e versionado está em
`data/authorship/authorship_registry*.jsonl` e segue
`schemas/authorship-provenance-record.schema.json`.

## Autor e autoridade conceitual do projeto

- **Rafael Melo Reis / ∆RafaelVerboΩ**
  - papéis: `PROJECT_CREATOR`, `AUTHOR`, `MAINTAINER` conforme cada artefato;
  - marca declarada: `RAFCODE-Φ-∆RafaelVerboΩ-𓂀ΔΦΩ`;
  - responsabilidade: concepção, requisitos, decisões éticas e aprovação humana.

A presença neste índice não atribui automaticamente a Rafael a autoria de fontes,
obras, teorias, códigos ou resultados produzidos por terceiros. Cada derivação deve
conservar o autor anterior e a relação utilizada.

## Assistência computacional

- **OpenAI ChatGPT**
  - papel: `AI_ASSISTED_TOOL`;
  - contribuição possível: estruturação, redação assistida, análise e implementação
    sob instrução;
  - não é autor humano responsável, não aprova publicação e não substitui revisão.

## Regra para qualquer pessoa ou organização

Toda contribuição deve receber o papel real, sem inflar nem apagar crédito:

```text
AUTHOR | COAUTHOR | SOURCE_AUTHOR | CONTRIBUTOR | SOFTWARE_DEVELOPER
DATA_COLLECTOR | EDITOR | TRANSLATOR | CURATOR | REVIEWER
PROJECT_CREATOR | MAINTAINER | INSTITUTION | AI_ASSISTED_TOOL | UNKNOWN
```

`UNKNOWN` não significa “livre para apropriação”. Significa:

```text
TOKEN_VAZIO_AUTHORSHIP
claim_allowed=false
promotion_allowed=false
```

## Invariante

```text
origem ≠ transmissor ≠ editor ≠ implementador ≠ revisor
```

Uma mesma pessoa pode ocupar mais de um papel, mas cada papel precisa de declaração
de contribuição. Citar não transfere autoria. Implementar não apaga a fonte do
conceito. Traduzir ou adaptar gera contribuição própria sem eliminar a obra anterior.

## Correções

Erros de atribuição são corrigidos por registro append-only que aponta para o registro
anterior. Não se apaga silenciosamente o histórico de autoria.

Consulte: `docs/governance/AUTHORSHIP_PROVENANCE_INVARIANT_V1.md`.
