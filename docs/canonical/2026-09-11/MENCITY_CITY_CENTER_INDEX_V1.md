# MENCity — Centro da Cidade Informacional V1

Status: `DRAFT_AUDITABLE`  
claim_allowed=false

## Purpose

Single navigation hub for the semantic-event work created in the 2026-09-11 session. This file is an index, not evidence.

## Invariants

- SOURCE != ARTIFACT != EXECUTION != EVIDENCE != CLAIM
- TOKEN_VAZIO != 0
- TOKEN_ID != OCCURRENCE_ID != SENSE_VERSION != CLAIM
- correction = append + supersedes
- ordered(A,N) != ordered(N,A) unless an explicit rule proves symmetry/inversion

## City map

| Zone | Function | Canonical surface |
| --- | --- | --- |
| Praça Central | Router | START HERE |
| Cartório | Semantic dictionary | `data/semantics/semantic-dictionary.v1.jsonl` |
| Oficina | μ-event envelope | `schemas/mu-semantic-event.v1.schema.json` |
| Arquivo Vivo | Typed relationships / reconstruction | MANIFOLD Ω |
| Biblioteca | 56 secular intercultural parables | Drive Documento-Mestre |
| Observatório | Ambiguity / contradiction / forks | anomaly classes |
| Porto | schema/test/CI | GitHub PR #606 |
| Memória | documentary hub | Google Drive MENCity |

## Drive routes

- Folder: https://drive.google.com/drive/folders/1-MxPfULH8iSdQ3JZQe6S2RVSt16Own6F
- Documento-Mestre: https://docs.google.com/document/d/1gZ0raDFk2u--En8-Q2MlJrBtV6M1gKAlJD82TEipZsc/edit
- Mapa de Rotas: https://docs.google.com/spreadsheets/d/1IcALrmqohnLt-xOYtOlTnB5DITLXHrYIz2JHsDQ1BkY/edit
- Visão do Coração: https://docs.google.com/presentation/d/1qfzt38piR3NAdtnqlgwQQVBQ5LYxwfr9OW58wUa-gF0/edit

## Current state

`μ[Δ]` is a provisional authorial semantic micro-event.  
`‡`, `ª`, `›`, and `ª>ⁿ` remain `TOKEN_VAZIO_SEMANTIC`.  
`A-N` and `N-A` remain oriented/distinct by default.

## Gate

IMPLEMENTED_DRAFT != PASS.

F_gap:
- deterministic REPLAY not yet executed;
- semantic-support workflow debt remains separate;
- Calendar time is TOKEN_VAZIO_TIME.

F_next:
1. validate schema + JSONL;
2. add USER→AI→correction→fork→REPLAY fixtures;
3. observe successor CI;
4. append only material deltas.
