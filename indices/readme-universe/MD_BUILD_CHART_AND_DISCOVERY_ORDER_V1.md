# RAFAELIA — MD Build Chart and Discovery Order V1

**Camada:** 1 — navegação semântica anterior à árvore de arquivos  
**Estado:** CANONICAL_DRAFT  
**Branch:** `main_01_readme-universe-layer1`  
**Regra:** nenhum arquivo produtor é alterado por este índice  
**claim_allowed:** false

## Objetivo

Definir como humanos e IAs descobrem, ordenam e leem arquivos Markdown no ecossistema RAFAELIA. O chart não presume que todo repositório possua todos os tipos; ausência é registrada como `TOKEN_VAZIO_MD_TYPE`, não como defeito automático.

## Endereçamento navegável

```text
ORGANIZATION / REPOSITORY / BRANCH_OR_COMMIT / PATH / BLOB_SHA
      rua        endereço       número          cômodo    identidade
```

Identificador canônico sugerido:

```text
md://<organization>/<repository>@<commit>/<path>#<blob_sha>
```

Exemplo:

```text
md://rafaelmeloreisnovo/RafPolimata@e6699c3/CLAUDE.md#TOKEN_VAZIO_BLOB
```

## Ordem de descoberta por prioridade

| Delta | Classe | Padrões comuns | Pergunta respondida |
|---:|---|---|---|
| Δ00 | identidade | `README.md`, `README.MD`, `README.rst` | O que é este repositório? |
| Δ01 | instrução para agentes | `AGENTS.md`, `AGENTES.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md` | Como uma IA deve operar aqui? |
| Δ02 | navegação | `INDEX.md`, `docs/INDEX.md`, `SUMMARY.md`, `MAP.md`, `CATALOG.md` | Onde estão os corpos documentais? |
| Δ03 | arquitetura | `ARCHITECTURE.md`, `DESIGN.md`, `ADR*.md`, `RFC*.md` | Como o sistema é dividido e por quê? |
| Δ04 | estado e verdade atual | `STATUS.md`, `CURRENT_STATE*.md`, `STATE*.md`, `BASELINE*.md` | O que existe de fato neste corte? |
| Δ05 | build e execução | `BUILD.md`, `INSTALL.md`, `RUNBOOK.md`, `OPERATIONS.md`, `DEPLOYMENT.md` | Como construir, executar e operar? |
| Δ06 | evidência | `EVIDENCE*.md`, `PROOF*.md`, `RECEIPT*.md`, `AUDIT*.md`, `VALIDATION*.md` | Qual execução ou prova foi registrada? |
| Δ07 | mudança temporal | `CHANGELOG.md`, `RELEASE_NOTES.md`, `HISTORY.md`, `MIGRATION*.md`, `UPGRADE*.md` | O que mudou entre versões? |
| Δ08 | governança | `GOVERNANCE.md`, `CONTRIBUTING.md`, `MAINTAINERS.md`, `OWNERS.md`, `CODEOWNERS` | Quem decide, mantém e revisa? |
| Δ09 | segurança e conformidade | `SECURITY.md`, `PRIVACY.md`, `THREAT_MODEL.md`, `COMPLIANCE.md` | Quais riscos e controles existem? |
| Δ10 | limites epistemológicos | `LIMITATIONS.md`, `GAPS.md`, `KNOWN_ISSUES.md`, `ASSUMPTIONS.md` | O que não está provado ou fechado? |
| Δ11 | roadmap | `ROADMAP.md`, `TODO.md`, `BACKLOG.md` | O que é futuro e não deve ser confundido com implementação? |
| Δ12 | domínio e teoria | `MANIFESTO.md`, `THEORY*.md`, `PAPER*.md`, `SPEC*.md`, `ONTOLOGY*.md` | Qual contexto conceitual ou formal orienta o trabalho? |
| Δ13 | subsistemas | `**/README.md`, `docs/**.md`, `research/**.md`, `proofs/**.md` | Como cada cômodo/subsistema se apresenta? |
| Δ14 | arquivo e legado | `archive/**.md`, `legacy/**.md`, `OLD*.md`, `DEPRECATED*.md` | O que é histórico, substituído ou apenas referência? |
| Δ15 | lacuna útil | arquivo esperado ausente ou incompreensível | Qual próximo gate deve ser aberto? |

## Regras de prioridade

1. Arquivo específico do agente não substitui o README; complementa instruções operacionais.
2. Documento de estado atual prevalece sobre roadmap para descrever implementação observada.
3. Receipt/auditoria prevalece sobre linguagem promocional para afirmar execução.
4. Changelog e release notes preservam temporalidade; não devem ser condensados em estado presente sem predecessor.
5. README interno é nó de subsistema, não duplicata automática do README raiz.
6. Instruções conflitantes geram `CONFLICT_INSTRUCTION` e decisão humana.
7. Arquivo sem commit/blob conhecido recebe `TOKEN_VAZIO_REVISION`.

## Delta documental

Cada leitura gera um vetor:

```text
ΔMD = <identity, instructions, navigation, architecture, state,
       build, evidence, temporal, governance, security,
       gaps, roadmap, domain, subsystem, legacy>
```

Valores permitidos por dimensão:

```text
ABSENT | PRESENT_UNREAD | READ | CONTRADICTED | SUPERSEDED | TOKEN_VAZIO
```

## Tipos já observados no lote inicial

- `Mapa/README.md` — Δ00 identidade + Δ02 navegação + Δ08 governança.
- `RafGitTools/README.md` — Δ00 identidade + Δ04 estado + Δ05 build + Δ11 roadmap.
- `RafGitTools/AGENTS.md` — Δ01 instrução para agentes.
- `RafGitTools/Livro/CHANGELOG.md` — Δ07 mudança temporal.
- `RafGitTools/docs/BUILD.md` — Δ05 build.
- `RafPolimata/README.md` — Δ00 identidade + Δ02 navegação + Δ04 estado + Δ06 evidência.
- `RafPolimata/CLAUDE.md` — Δ01 instrução específica de agente.
- `RafPolimata/docs/AGENTES_DECISAO_LOG.md` — Δ01/Δ08 decisões de agentes.

## Entrada de novos artefatos

```text
DISCOVER
→ ADDRESS
→ FETCH
→ HASH/REVISION
→ CLASSIFY ΔMD
→ EXTRACT DECLARED ROLE
→ TYPE RELATIONS
→ RECORD CONFLICTS/GAPS
→ APPEND TO MAP
→ F_next
```

## Fronteira desta camada

Esta camada registra documentos Markdown, seus endereços, papéis e relações declaradas. Não inventaria ainda classes, funções ou todos os arquivos não documentais. A árvore estrutural completa pertence à camada seguinte.

## F_next

1. Enumerar os tipos Δ00–Δ15 em cada repositório acessível.
2. Ler diretamente os arquivos prioritários encontrados.
3. Registrar commit, path e blob SHA quando disponíveis.
4. Criar nós de conflito quando README, AGENTS/CLAUDE e estado técnico divergirem.
5. Manter alterações em arquivos produtores na fila de autorização.
