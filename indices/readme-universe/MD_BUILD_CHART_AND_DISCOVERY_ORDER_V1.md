# RAFAELIA — MD Discovery Adapter V1

**Camada:** 1 — uma entrada documental dentro da indexação universal  
**Estado:** CANONICAL_DRAFT  
**Branch:** `main_01_readme-universe-layer1`  
**Regra:** Markdown é uma superfície de descoberta, não o tema nem o centro do ecossistema  
**claim_allowed:** false

## Correção de escopo

Este documento não define o universo RAFAELIA por arquivos `.md`. Ele define apenas como documentos Markdown podem ser descobertos e usados como portas de entrada para um processo maior de indexação universal.

O processo completo deve abranger, conforme cada repositório:

```text
repositórios
branches e tags
commits e PRs
releases e changelogs
arquivos e diretórios
dados e schemas
código e builds
workflows, runs e artifacts
receipts e evidências
segurança e privacidade
autoridades e responsáveis
alterações, predecessores e próximos passos
```

## Endereçamento navegável

```text
ORGANIZATION / REPOSITORY / REF / PATH / OBJECT_ID_OR_HASH
```

Markdown recebe um endereço documental, mas o mesmo modelo deve aceitar outros tipos de objeto.

```text
object://<source>/<organization>/<repository>@<ref>/<path>#<identity>
```

## Classes de descoberta Markdown

| Delta | Classe | Padrões comuns | Função operacional |
|---:|---|---|---|
| Δ00 | identidade | `README*` | entrada declarativa |
| Δ01 | instrução de agentes | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Copilot instructions | restrições e método local |
| Δ02 | navegação | `INDEX.md`, `SUMMARY.md`, `MAP.md`, `CATALOG.md` | rotas documentais |
| Δ03 | arquitetura | `ARCHITECTURE.md`, `DESIGN.md`, ADR, RFC | estrutura e decisões |
| Δ04 | estado | `STATUS.md`, `CURRENT_STATE*`, `BASELINE*` | corte material declarado |
| Δ05 | build/operação | `BUILD.md`, `INSTALL.md`, `RUNBOOK.md`, `OPERATIONS.md` | construção e operação |
| Δ06 | evidência | `EVIDENCE*`, `PROOF*`, `RECEIPT*`, `AUDIT*`, `VALIDATION*` | suporte verificável |
| Δ07 | mudança temporal | `CHANGELOG.md`, `RELEASE_NOTES.md`, `HISTORY.md`, `MIGRATION*` | evolução e predecessores |
| Δ08 | governança | `GOVERNANCE.md`, `CONTRIBUTING.md`, `MAINTAINERS.md`, `OWNERS.md` | autoridade e revisão |
| Δ09 | segurança/privacidade | `SECURITY.md`, `PRIVACY.md`, `THREAT_MODEL.md`, `COMPLIANCE.md` | risco, acesso e proteção |
| Δ10 | limites | `LIMITATIONS.md`, `GAPS.md`, `KNOWN_ISSUES.md`, `ASSUMPTIONS.md` | lacunas e fronteiras |
| Δ11 | futuro | `ROADMAP.md`, `TODO.md`, `BACKLOG.md` | intenção ainda não materializada |
| Δ12 | domínio | manifestos, papers, specs, ontologias | contexto e formalização |
| Δ13 | subsistemas | READMEs internos e docs locais | entrada por módulo |
| Δ14 | legado | archive, legacy, old, deprecated | história e supersessão |
| Δ15 | lacuna útil | documento ausente/incompreensível | próximo gate |

## Regras de verdade

```text
README apresenta, mas não prova execução
AGENTS orienta, mas não altera autoridade por si só
STATUS declara estado, mas deve apontar para evidência
BUILD descreve procedimento, mas run prova execução
CHANGELOG registra mudança, mas commit/tag fixa identidade
RELEASE documenta entrega, mas artifact/hash fixa o corpo
SECURITY/PRIVACY delimitam tratamento, acesso e exposição
```

## Relação com a indexação universal

```text
MD_DISCOVERY
→ UNIVERSAL_OBJECT_INDEX
→ VERSION_AND_CHANGE_LEDGER
→ AUTHORITY_INDEX
→ PRIVACY_AND_RISK_GATE
→ EVIDENCE_LEDGER
→ DEPENDENCY_GRAPH
→ F_next
```

## Estados

```text
ABSENT
PRESENT_UNREAD
READ
CONTRADICTED
SUPERSEDED
ACCESS_BLOCKED
TOKEN_VAZIO
```

## Fronteira

Esta camada lê documentos prioritários para compreender o repositório antes da varredura estrutural completa. Ela não limita a indexação a Markdown e não transforma preferência de uma IA em autoridade canônica.

## F_next

1. Usar os documentos Markdown como portas de entrada.
2. Cruzar suas declarações com commits, releases, workflows, artifacts, código e dados.
3. Registrar divergências e temporalidade.
4. Aplicar a política universal de governança sem inserir textos normativos desnecessários nos repositórios produtores.
