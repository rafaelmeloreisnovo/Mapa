# RAFAELIA — Delta de Autoria, Origem e Proveniência — 2026-08-03 01:45 BRT

**ID:** `AUTH-PROV-20260803T0145-0300`  
**Modo:** `APPEND_ONLY / FAIL_CLOSED / NON_DESTRUCTIVE`  
**Estado:** `DRAFT_PR / claim_allowed=false`  
**PR:** `rafaelmeloreisnovo/Mapa#139`  
**Branch:** `governance/authorship-provenance-invariant-20260803`

## Diretiva

```text
Autoria é indispensável, necessária e importante.
A origem é constante estrutural do conhecimento.
```

A mensagem-fonte foi selada com:

```text
SHA-256 = 8ae13334f6305ca4de3089c11f630fe9237aba7231290198fe310bd09288e230
bytes = 1454
```

## Invariante

```text
origem ≠ transmissor ≠ editor ≠ implementador ≠ revisor
origem desconhecida = TOKEN_VAZIO_AUTHORSHIP
```

A cadeia mínima é:

```text
ARTIFACT
  → ROLE + CONTRIBUTION
  → ORIGIN_CHAIN@REVISION
  → RIGHTS_STATE
  → REVIEW
  → PROMOTION_OR_TOKEN_VAZIO
```

## GitHub materializado

- `AUTHORS_RAFAELIA.md`;
- `docs/governance/AUTHORSHIP_PROVENANCE_INVARIANT_V1.md`;
- `data/control-plane/authorship-provenance-policy.v1.json`;
- `schemas/authorship-provenance-record.schema.json`;
- `data/authorship/authorship_registry.delta.20260803.jsonl`;
- `data/authorship/authorship_registry.drive.delta.20260803.jsonl`;
- `tools/verify_authorship_provenance.py`;
- `tests/test_authorship_provenance.py`;
- `.github/workflows/authorship-provenance.yml`.

## Google Drive

Documento editorial:

```text
file_id = 1s1W8wpEeDsSwTylgijU-LnybF_ijnf4grFo768JdHig
revision_id = AIroW37DiIf7kWn7w9UCzvzxjf8TT3jJxkPuYFAfUfv0J1tGL0ixFvI_IJ6oqwTexMfCl6AIibOWMiMAgUAUE6LAYn0QNEu9tMQidxhgAyA
export_mime = text/plain
export_bytes = 4214
export_sha256 = db5f860ae2bcd3333eb7e029eb59672216836385ddff92e44501bab05bca342a
```

Duas criações vazias acidentais foram preservadas e rotuladas como
`DUPLICATE_EMPTY_TOKEN_VAZIO`; nenhuma exclusão destrutiva foi executada.

## Papéis

```text
AUTHOR | COAUTHOR | SOURCE_AUTHOR | CONTRIBUTOR | SOFTWARE_DEVELOPER
DATA_COLLECTOR | EDITOR | TRANSLATOR | CURATOR | REVIEWER
PROJECT_CREATOR | MAINTAINER | INSTITUTION | AI_ASSISTED_TOOL | UNKNOWN
```

A ferramenta de IA permanece `AI_ASSISTED_TOOL`, sem responsabilidade de autoria
humana. A fonte `openai/ten-proofs` conserva autoria institucional da OpenAI e não é
absorvida como criação RAFAELIA.

## Gates antiplágio

Bloquear quando houver:

- origem ou autor materialmente desconhecido;
- uso substancial sem âncora;
- autor elegível omitido;
- autor listado sem contribuição;
- adaptação, tradução ou implementação que esconda a fonte;
- direitos ou licença indefinidos;
- similaridade automática promovida como conclusão humana.

A saída segura é:

```text
PLAGIARISM_RISK_BLOCKED
TOKEN_VAZIO_AUTHORSHIP
claim_allowed=false
```

## F_GAP

- cobertura retroativa de todos os arquivos e repositórios;
- reconciliação MIT/CC-BY-SA/RAFCODE-Φ e demais licenças declaradas;
- mapa completo de autores e contribuições anteriores;
- teste de restauração da memória autoral;
- revisão humana independente;
- CI remota e required checks ainda em observação;
- manifesto final de blobs e receipt pós-review.

## F_NEXT

1. observar os workflows da PR #139;
2. selar blob SHA de cada artefato no manifesto append-only;
3. corrigir somente por `previous_record_id`;
4. aplicar o registro às próximas promoções matemáticas e científicas;
5. manter a PR draft enquanto houver bloqueadores.

## R₃

**F_ok:** princípio transformado em política, schema, registros, validador, testes, CI
e espelho Drive.  
**F_gap:** cobertura histórica, licenças e revisão independente incompletas.  
**F_next:** manifestar blobs, observar CI e exigir autoria antes de qualquer promoção.
