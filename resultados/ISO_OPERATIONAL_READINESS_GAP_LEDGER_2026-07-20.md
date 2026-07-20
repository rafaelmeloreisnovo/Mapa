# Ledger de lacunas ISO-operacionais — 2026-07-20

Este relatório é derivado do baseline selado e não constitui certificação.

- P0: 8
- P1: 11
- P2: 5
- P3: 1

| ID | Prioridade | Domínio | Achado | Critério de saída | Horas |
|---|---|---|---|---|---:|
| G001 | P0 | inventory | Repository inventory is only 51/126 materialized. | 126 records reconciled or formally scoped with approved exclusions. | 420–760 |
| G002 | P1 | inventory | Inventory head is a dated snapshot and not continuously reconciled with current repository changes. | Two consecutive refreshes reproduce counts and identify drift without silent mutation. | 120–240 |
| G003 | P1 | quality | No unified QMS scope and end-to-end process map exists for the federation. | Approved process map covers all eight core authorities. | 260–420 |
| G004 | P1 | quality | No cross-repository CAPA ledger with root cause and effectiveness checks is evidenced. | All P0/P1 findings have owner, due state, root cause and effectiveness evidence. | 220–360 |
| G005 | P2 | measurement | No longitudinal quality objective and trend dataset is available. | At least three measured cycles exist for each core objective. | 180–320 |
| G006 | P0 | quality | Some documents use complete/aligned language while implementation notes retain pending integrations. | No COMPLETE or COMPLIANT state exists without implementation, execution and evidence pointers. | 160–280 |
| G007 | P1 | data | ISO 8000 goal-question-indicator-metric stacks are not instantiated portfolio-wide. | Every critical data process has goal, question, indicator, metric and inspection order. | 260–440 |
| G008 | P1 | data | No canonical master data dictionary spans repository, artifact, claim, dataset, device and person-role identifiers. | All core ledgers validate against one versioned dictionary. | 300–520 |
| G009 | P0 | privacy | Retention and deletion rules for private conversations, chunks and model corpora are not unified. | Every private dataset has owner, purpose, retention, deletion test and access class. | 280–520 |
| G010 | P1 | data | Duplicate and near-duplicate control across corpora and repositories is partial. | Duplicate rate is measured and every collapse preserves source lineage. | 300–540 |
| G011 | P0 | security | A single ISMS scope and authoritative asset classification are not evidenced. | All core assets are classified with confidentiality, integrity and availability requirements. | 300–500 |
| G012 | P1 | security | No portfolio Statement of Applicability links risks, controls, exclusions and evidence. | Each selected or excluded control has rationale, owner, implementation state and evidence. | 320–560 |
| G013 | P0 | risk | No unified risk register covers the 126-repository portfolio. | All P0 routes and critical assets map to reviewed risks and treatments. | 360–620 |
| G014 | P0 | ci | Multiple remote jobs report zero steps and no logs. | Two consecutive observable runs execute steps and publish logs/artifacts. | 200–480 |
| G015 | P0 | device | Exact target-device and installed-APK receipt remains TOKEN_VAZIO. | Signed receipt binds device, APK, ABI, command, outputs and hashes. | 240–520 |
| G016 | P1 | supply_chain | Sigstore or equivalent signing and external SLSA provenance remain absent. | One reproducible release has verified provenance and signature chain. | 360–700 |
| G017 | P1 | resilience | Real rollback drills for Android, VM/QEMU and models are not evidenced. | Each platform has a successful restoration receipt and dependency-impact record. | 420–760 |
| G018 | P2 | incident_response | No exercised incident-response scenario is evidenced. | Exercise records detection, containment, recovery, lessons and CAPA. | 160–300 |
| G019 | P1 | continuity | Backup and restore evidence is uneven across code, data, VM and model assets. | Restore tests meet declared RPO/RTO for every critical asset class. | 300–560 |
| G020 | P1 | forks | Large forks lack a uniformly frozen upstream-to-delta audit baseline. | AndroidX, framework, kernel, Gradle and QEMU deltas are reproducible and risk-ranked. | 520–900 |
| G021 | P0 | rights | License, authorship and reuse rights are not uniformly resolved for code, papers and private data. | No release contains NOASSERTION or unresolved private/public-domain ambiguity. | 300–620 |
| G022 | P3 | assurance | Independent reproduction, penetration review and management-system audit are absent. | Independent reviewers reproduce selected results and issue tracked findings. | 600–1200 |
| G023 | P2 | people | Segregation of duties and bus factor are not measured. | Every critical process has primary, backup and independent reviewer. | 120–240 |
| G024 | P2 | competence | No competence and training matrix is evidenced for required specialist levels. | All assigned roles meet or have an approved development plan for required competencies. | 120–260 |
| G025 | P2 | documentation | Documentation debt includes placeholders, duplication and potentially stale claims. | Critical documents have owner, freshness date, no unresolved placeholder and valid links. | 240–460 |

## Limite

`OPEN` e `TOKEN_VAZIO` não podem ser convertidos em PASS por média, volume documental ou intenção.

Selo do baseline: `16bce6c5e09ad76a57d9fe3be05fb472651b3e938bc759b68dfc9d0173eca001`
