# Mapa — RAFAELIA Knowledge Organization System

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Domain](https://img.shields.io/badge/Domain-Biblioteconomia%20%7C%20Rastreabilidade-purple)](biblioteconomia/)
[![Research](https://img.shields.io/badge/Research-RAFAELIA%20Ecosystem-orange)](https://github.com/rafaelmeloreisnovo/ChipQuantum)

> Central repository for organization, traceability, and knowledge mapping of the
> RAFAELIA ecosystem — cataloging repositories, claims, evidence and gaps as a living
> biblioteconomic and operational knowledge system.

---

## Objective

Transform files, images, conversations, indices, results, claims and unresolved gaps into a
clear work tree — a **biblioteconomic knowledge organization system (KOS)** that classifies,
catalogs, cross-references and audits the RAFAELIA research corpus.

---

## Repository Map

```text
Mapa/
│
├── arquitetura/       Work structure design and architecture diagrams
├── biblioteconomia/   KOS, controlled vocabulary and authority control
├── protocolos/        Execution rules, gap analysis and operational governance
│   └── HOMEOSTASE_OPERACIONAL_MELHORIA_CONTINUA.md
├── schemas/           Machine-readable contracts
│   └── operational-ontology.schema.json
├── data/ontology/     Canonical operational ontology records
├── scripts/           Custody, validation and ontology engines
├── tools/             Repository and artifact gap mappers
├── tests/             Deterministic positive and negative tests
├── indices/           Asset, source and cross-repository manifests
├── auditoria/         Execution evidence and conservative validation records
├── resultados/        Generated baselines and reviewed outputs
├── workflows/         Operational reading and validation routes
├── visual/            Conceptual maps and architecture images
└── docs/              Architecture, heuristics and supplementary documentation
```

---

## Biblioteconomic Layer

This repository implements a **library science classification system** for the RAFAELIA ecosystem:

- **cataloging**: each object is identified by domain, version, maturity and interconnections;
- **authority control**: `biblioteconomia/` distinguishes preferred terms, aliases and semantic collisions;
- **indexing**: `indices/` tracks assets, origins, hashes, branches and review states;
- **provenance**: claims can be linked to sources, datasets, runs, commits and evidence;
- **operational governance**: `protocolos/` preserves baselines, risks, falsifiers and rollback;
- **gap preservation**: unresolved information remains `TOKEN_VAZIO`, never silently converted to zero;
- **visual navigation**: `visual/` contains SVG concept maps and architecture diagrams.

---

## Operational Ontology

The executable ontology adds a semantic and epistemic layer above the existing physical
repository gap mapper:

| Artifact | Function |
|---|---|
| `data/ontology/rafaelia-operational-ontology.v1.json` | Canonical records for concepts, trajectories, editorial states and useful gaps |
| `schemas/operational-ontology.schema.json` | External structural contract |
| `scripts/operational_ontology_engine.py` | Validation, conservative heuristics, graph and trajectory analysis |
| `tests/test_operational_ontology_engine.py` | Positive and negative invariants |
| `docs/ONTOLOGIA_OPERACIONAL_RAFAELIA.md` | Architecture and limits |
| `docs/HEURISTICAS_DINAMICAS_E_VAZIOS.md` | Heuristics for abandoned, ignored, potential, suggested and withheld themes |
| `indices/ONTOLOGIA_OPERACIONAL_RAFAELIA.md` | Authority and integration map |

Core invariants:

```text
TOKEN_VAZIO != 0
heuristic != proof
not found != censored
methodological bridge != physical equivalence
claim_allowed=false until evidence closes the corresponding gate
```

The existing `tools/repository_gap_mapper.py` remains responsible for files, builds,
binaries and unresolved source markers. The ontology engine maps claims, concepts,
relations, operators, trajectories and epistemic gaps. Neither replaces the other.

---

## Active Governance Artifacts

| Artifact | Function | Status |
|---|---|---|
| `protocolos/HOMEOSTASE_OPERACIONAL_MELHORIA_CONTINUA.md` | Continual improvement across a complex process network | `NORMATIVE_METAMODEL_DRAFT` |
| `indices/NEUROCIENCIA_HOMEOSTASE_OPERACIONAL.md` | GitHub ↔ Drive provenance for neuroscience and governance artifacts | `MERGED_BASELINE` |
| `docs/ONTOLOGIA_OPERACIONAL_RAFAELIA.md` | Executable KOS and epistemic-gap architecture | `DRAFT_AUDITABLE` |

The operational-homeostasis protocol treats standards as controlled baselines rather than
frozen ceilings. A proposed improvement must preserve applicable requirements, state its
delta, measure benefit, control risk, support rollback and maintain traceability.

---

## Cross-repository Research Path

```text
papers / scientific claim
  ↓
Mapa / provenance, ontology and governance
  ↓
Google Drive / editorial review copy
  ↓
review gate
  ↓
merge | correction | TOKEN_VAZIO
```

Merged baselines:

- [`papers` PR #19](https://github.com/rafaelmeloreisnovo/papers/pull/19) — recurrence, myelin, electrophysiology and falsifiability;
- [`Mapa` PR #41](https://github.com/rafaelmeloreisnovo/Mapa/pull/41) — operational homeostasis and continual improvement;
- [Drive provenance folder](https://drive.google.com/drive/folders/1n74otSJEGsmI9I2W7-hg2mYec6d-6Sl5).

A commit proves existence and history of an artifact; it does not by itself prove execution,
scientific validity, causality or operational performance.

---

## Local Validation

```bash
python3 -m unittest -v tests/test_operational_ontology_engine.py

python3 scripts/operational_ontology_engine.py \
  --ontology data/ontology/rafaelia-operational-ontology.v1.json \
  --output-json build/ontology/report.json \
  --output-md build/ontology/report.md \
  --generated-at 2026-07-23T00:00:00Z \
  --strict
```

No automatic workflow is enabled by this package. Remote execution remains a separate,
reviewed decision.

---

## Ecosystem

| Repository | Domain |
|---|---|
| [`ChipQuantum`](https://github.com/rafaelmeloreisnovo/ChipQuantum) | T⁷ toroidal cryptographic pipeline |
| [`Cosmos`](https://github.com/rafaelmeloreisnovo/Cosmos) | Cosmological RAFAELIA framework |
| [`papers`](https://github.com/rafaelmeloreisnovo/papers) | Exacordex, raefaelos and evidence-bounded research notes |
| [`TeoremasTesesTeorias`](https://github.com/rafaelmeloreisnovo/TeoremasTesesTeorias) | Formal theorems and prior art |
| [`GEOMETRIA_SOLAR_Maia_Inca`](https://github.com/rafaelmeloreisnovo/GEOMETRIA_SOLAR_Maia_Inca) | Solar geometry |
| [`Catalogo-cosmologico`](https://github.com/rafaelmeloreisnovo/Catalogo-cosmologico) | Astronomical catalog |
| [`llamaRafaelia`](https://github.com/rafaelmeloreisnovo/llamaRafaelia) | LLM inference framework |
| [`Vectras-VM-Android`](https://github.com/rafaelmeloreisnovo/Vectras-VM-Android) | Android VM runtime |

---

## License

**License:** MIT — see [`LICENSE`](LICENSE).
