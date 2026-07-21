# Mapa — RAFAELIA Knowledge Organization System

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Domain](https://img.shields.io/badge/Domain-Biblioteconomia%20%7C%20Rastreabilidade-purple)](biblioteconomia/)
[![Research](https://img.shields.io/badge/Research-RAFAELIA%20Ecosystem-orange)](https://github.com/rafaelmeloreisnovo/ChipQuantum)

> Central repository for organization, traceability, mechanism recognition, and visual knowledge mapping of the RAFAELIA ecosystem.

---

## Objective

Transform files, images, conversations, indices, repository identities, mechanisms, and results into a clear work tree: a **living biblioteconomic knowledge system** that classifies, catalogs, cross-references, validates, and visually develops the RAFAELIA corpus.

The repository is deliberately fail-closed:

```text
observed identity = FATO
unread behavior   = TOKEN_VAZIO
```

A repository name never proves how that repository works.

---

## Repository Map

```text
Mapa/
├── arquitetura/       Work structure and living-system architecture
├── biblioteconomia/   KOS: classification, vocabulary, catalog, method
├── protocolos/        Execution, integrity, claim, and gap contracts
├── indices/           Inventories, graphs, generated indices, provenance
├── data/              Federated routes and evidence-bounded mechanism profiles
├── schemas/           Machine-readable data contracts
├── scripts/           Deterministic builders and validators
├── codigo/            Biblioteconomic tools retained from the original layer
├── tests/             Executable invariants and adversarial boundaries
├── resultados/        Audits, validations, and delivery records
├── visual/            Human-readable concept maps and development views
├── workflows/         Operational routes and sweep procedures
├── docs/              Supplementary documentation
└── .github/           GitHub governance and workflows
```

---

## Living System of Mechanisms

The living-system layer represents each inventoried repository through eleven common questions:

`purpose · inputs · transformations · outputs · interfaces · invariants · quality_controls · risks · relations · philosophical_context · visual_model`

Each answer is explicitly marked as `FATO`, `HIPOTESE`, `PARABOLA`, or `TOKEN_VAZIO`. Resolved cells require evidence. Empty cells require a reason, next action, and exit criterion.

Core files:

- [`arquitetura/ARQUITETURA_SISTEMA_VIVO.md`](arquitetura/ARQUITETURA_SISTEMA_VIVO.md)
- [`schemas/repository_mechanism.schema.json`](schemas/repository_mechanism.schema.json)
- [`data/mechanisms/`](data/mechanisms/)
- [`scripts/build_living_system_index.py`](scripts/build_living_system_index.py)
- [`scripts/validate_living_system_index.py`](scripts/validate_living_system_index.py)
- [`visual/SISTEMA_VIVO.md`](visual/SISTEMA_VIVO.md)

```bash
python3 scripts/build_living_system_index.py --write
python3 scripts/build_living_system_index.py --check
python3 scripts/validate_living_system_index.py
python3 -m unittest tests/test_living_system_index.py -v
```

The generated `indices/LIVING_SYSTEM_INDEX.json` is deterministic and integrity-protected with BLAKE2b-256.

---

## Biblioteconomic Layer

This repository implements a library-science classification system for the RAFAELIA ecosystem:

- **cataloging**: repositories classified by identity, domain, maturity, and evidence status;
- **indexing**: `indices/` tracks assets, sources, topology, inventory, and generated knowledge views;
- **navigation**: `biblioteconomia/` and `visual/` provide cross-repository reading paths;
- **mechanism recognition**: `data/mechanisms/` records how a repository works only after evidence review;
- **lacuna preservation**: missing knowledge remains a valid, actionable `TOKEN_VAZIO`;
- **validation**: stdlib-only tools derive metrics, detect conflicts, and fail closed.

---

## Ecosystem

| Repository | Domain |
|---|---|
| [`ChipQuantum`](https://github.com/rafaelmeloreisnovo/ChipQuantum) | T⁷ toroidal cryptographic pipeline |
| [`Cosmos`](https://github.com/rafaelmeloreisnovo/Cosmos) | Cosmological RAFAELIA framework |
| [`papers`](https://github.com/rafaelmeloreisnovo/papers) | Research and publication artifacts |
| [`TeoremasTesesTeorias`](https://github.com/rafaelmeloreisnovo/TeoremasTesesTeorias) | Formal theorems and prior art |
| [`GEOMETRIA_SOLAR_Maia_Inca`](https://github.com/rafaelmeloreisnovo/GEOMETRIA_SOLAR_Maia_Inca) | Solar geometry |
| [`Catalogo-cosmologico`](https://github.com/rafaelmeloreisnovo/Catalogo-cosmologico) | Astronomical catalog |
| [`llamaRafaelia`](https://github.com/rafaelmeloreisnovo/llamaRafaelia) | LLM inference framework |
| [`Vectras-VM-Android`](https://github.com/rafaelmeloreisnovo/Vectras-VM-Android) | Android VM runtime |

The table is navigational, not a substitute for the connector-backed inventory or mechanism evidence.

---

## License

**License:** MIT — see [`LICENSE`](LICENSE).
