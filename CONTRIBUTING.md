# Contributing to Mapa

## Scope

Contributions should relate to the RAFAELIA Knowledge Organization System:

- New library classifications in `biblioteconomia/`
- Protocol definitions in `protocolos/`
- Index updates in `indices/`
- Architecture designs in `arquitetura/`
- Visual maps (SVG) in `visual/`
- Validation workflows in `workflows/`

## File Naming

- Markdown: `SCREAMING_SNAKE_CASE.md` (following established pattern in this repo)
- SVG/images: descriptive names in Portuguese or English, no hash names
- No files with spaces in names (use underscores or hyphens)

## Branch Naming

| Type | Pattern |
|---|---|
| New classification | `feat/biblioteconomia-<topic>` |
| Protocol | `feat/protocol-<name>` |
| Index | `feat/index-<topic>` |
| Visual | `feat/visual-<map-name>` |
| Fix | `fix/<file>` |

## Commit Convention

```text
feat: add RAFAELIA repository index to indices/
docs: update biblioteconomia with Vectras-VM-Android classification
feat: add WORKFLOW_VALIDACAO_CRUZADA.md to workflows/
fix: correct repo count in MAPA_BIBLIOTECONOMICO_RAFAELIA
```

## Pull Request Checklist

- [ ] Content placed in correct directory
- [ ] Filename follows naming convention (no spaces, no hash names)
- [ ] README updated if adding new visual or workflow
- [ ] CHANGELOG.md updated under [Unreleased]
