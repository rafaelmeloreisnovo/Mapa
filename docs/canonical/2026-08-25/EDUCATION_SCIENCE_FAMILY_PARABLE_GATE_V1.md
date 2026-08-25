# RAFAELIA — Education × Science × Family × Parable Gate V1

**Date:** 2026-08-25  
**State:** `IMPLEMENTED_METHOD / CLAIM_GATED / APPEND_ONLY`  
**claim_allowed:** `false`  
**Public scope:** reproducible method, bibliography, epistemic boundaries.  
**Private scope:** family narratives, personal works, child-specific examples and raw conversation content remain in Google Drive/private corpus.

## 1. Purpose

Provide a navigable pedagogical bridge between early-childhood/primary education, science, mathematics, history, geography, family life, geometry, works/authorship, and Biblical/traditional parables **without converting metaphor, tradition, coherence or similarity into scientific evidence**.

Canonical route:

`source → pedagogical node → parable/storyline → candidate bridge → external anchor → counter-anchor/falsifier → activity/test → evidence → receipt → gate → claim`

## 2. Epistemic legend

- `[E] EVIDENCE` — empirical or documentary support under an explicit method.
- `[M] METAPHOR/PARABLE` — structural analogy; proof weight = 0.
- `[H] HYPOTHESIS` — testable proposition; claim remains open.
- `[T] TRADITION` — historical/religious/cultural meaning; not empirical evidence by itself.
- `[A] ART/WORK` — authored expression, representation or artifact.
- `[C] CURRICULUM` — official curriculum/taxonomy anchor.
- `[Ø] TOKEN_VAZIO` — missing evidence, unresolved mapping or untested edge.

Invariants:

1. `PARABLE != PROOF`.
2. `TRADITION != EMPIRICAL_EVIDENCE`.
3. `SCIENCE != TOTAL_WORLDVIEW`.
4. `COHERENCE != CLAIM_AUTHORITY`.
5. `STORYLINE -> HYPOTHESIS/LEARNING_ROUTE`, never automatic fact.
6. `FAMILY_EXAMPLE -> PRIVATE_CONTEXT`, never population-level evidence.
7. Every promoted cross-domain edge requires `source + relation-specific evidence + limit/falsifier + next gate`.

## 3. Pedagogical board

### Stages

- `EI` — Educação Infantil: observation, language, play, comparison, spatial/temporal experience.
- `EF1` — Ensino Fundamental anos iniciais: explanation, measurement, representation, evidence, local-to-global relations.
- `EF2` — Ensino Fundamental anos finais: models, argumentation, historical/geographical reasoning, quantitative analysis and source criticism.

### Domains

`SCIENCE | MATHEMATICS | HISTORY | GEOGRAPHY | SOCIETY | FAMILY | GEOMETRY | AUTHORSHIP_WORKS | TRADITION_BIBLICAL`

### Learning loop

`OBSERVE → ASK → NARRATE → MEASURE → REPRESENT → COMPARE → TEST → RECORD → EXPLAIN → RETROFEED`

The loop is recursive; a failed test returns to `ASK/REPRESENT`, not to claim promotion.

## 4. Biblical/traditional parables as navigation only

Biblical parables may function as `[T]+[M]` pedagogical storylines. Examples:

- **Sower / Semeador** (Mt 13; Mc 4; Lc 8) → conditions of learning/environment; `proof_weight=0`.
- **House on rock / Casa sobre a rocha** (Mt 7; Lc 6) → analogy for evidence foundations; `proof_weight=0`.
- **Good Samaritan / Bom Samaritano** (Lc 10) → ethics/care/social responsibility; normative discussion, not scientific measurement.
- **Mustard seed / Grão de mostarda** (Mt 13; Mc 4; Lc 13) → scale/growth metaphor; no biological or complexity claim without independent evidence.

When science and religious education meet, the board labels the edge `SCIENCE_RELIGION_ENCOUNTER` and requires explicit domain boundaries: what is empirical, what is historical/textual, what is philosophical/theological, and what remains unanswered.

## 5. Board card contract

Each card uses:

`CARD_ID | STAGE | DOMAIN | QUESTION | PHENOMENON | LIFE_CONTEXT | FAMILY_CONTEXT_PRIVATE | GEOMETRY/SPATIAL | PARABLE/TRADITION_OPTIONAL | ACTIVITY | MEASURE/OBSERVATION | SOURCE | EXTERNAL_ANCHOR | COUNTER_ANCHOR/LIMIT | EPISTEMIC_STATE | CLAIM_ALLOWED | NEXT_GATE | WORK_OUTPUT`

No child/family identifying data are permitted in the public GitHub artifact.

## 6. Initial cross-domain routes

1. `SCIENCE ↔ STORYLINE`: phenomena and storylines can organize inquiry, but narrative coherence is not evidence.
2. `SCIENCE ↔ FAMILY`: home routines and informal STEM can support learning; family experience is contextual evidence only.
3. `MATHEMATICS ↔ GEOMETRY/SPATIAL`: spatial reasoning has a documented relationship with mathematical performance; effect depends on domain and age.
4. `MATHEMATICS ↔ GEOGRAPHY`: integrated teaching can use measurement, scale, coordinates, data and spatial representation around real-world questions.
5. `GEOGRAPHY ↔ SOCIETY`: geographical thinking connects space, systems, relations, scale and human-environment questions.
6. `HISTORY ↔ EVIDENCE`: historical thinking requires analysis and interpretation of sources; narrative is reconstructed from evidence, not merely remembered.
7. `PRIMARY_ED ↔ CRITICAL_THINKING`: textual, dialogic, digital and practical approaches are candidate routes, with fewer studies in grades 1–2.
8. `SCIENCE ↔ RELIGIOUS_EDUCATION`: dialogue is allowed; epistemic trespass and category mistakes are explicit failure modes.
9. `AUTHORSHIP_WORKS ↔ LEARNING`: learner/family works are artifacts for reflection and assessment, not independent scientific validation.

## 7. External anchors — academic / official

### Curriculum / Brazil

- BRASIL. Ministério da Educação. **Base Nacional Comum Curricular (BNCC)**. Brasília: MEC, 2017/2018. Official curriculum anchor for Educação Infantil and Ensino Fundamental, including Matemática, Ciências da Natureza, Geografia and História.

### Early-years and inquiry science

- Adopting scientific literacy in early years from empirical studies on formal education: a systematic review. **International Journal of STEM Education**, 2025, 12:26. DOI: `10.1186/s40594-025-00547-1`.
- WILSON, S. E.; THERRIEN, W. J.; GERSIB, J. et al. Inquiry-Based Science Instruction for Students With Disabilities: A Systematic and Meta-Analytic Review. **Science Education**, 2026, 110:639–653. DOI: `10.1002/sce.70029`.
- SASSE, H.; WEBER, A. M.; REUTER, T. et al. Teacher Guidance and On-the-Fly Scaffolding in Primary School Students' Inquiry Learning. **Science Education**, 2025, 109(2):579–604. DOI: `10.1002/sce.21921`.

### Storylines / narrative learning

- WALKER, K. I.; NOURI, N. Phenomenon-based learning and storylines in K-12 science education: a systematic review of current research, implementation, and future directions. **Frontiers in Education**, 2025, 10:1648234. DOI: `10.3389/feduc.2025.1648234`.
- Telling tales: the use of narratives in informal STEM settings. **International Journal of Science Education, Part B**, 2025. DOI: `10.1080/02635143.2025.2469065`.

### Family / informal STEM

- BAY, V. T. et al. Informal STEM experiences, parental influence, and learning outcomes in primary school: A systematic review. **Journal of Turkish Science Education**, 2026. DOI: `10.36681/tused.2026.017`.

### Mathematics / geometry / spatial reasoning

- How is spatial reasoning associated with mathematical ability? Evidence based on a meta-analysis. **Learning and Individual Differences**, 2025. DOI: `10.1016/j.lindif.2025.102838`.
- Integrated Teaching in Geography and Mathematics Education: A Systematic Review. **Sustainability**, 2025, 17(16):7276. DOI: `10.3390/su17167276`.

### Geography

- BENDL, T.; KRAJŇÁKOVÁ, L.; MARADA, M.; ŘEZNÍČKOVÁ, D. Geographical thinking in geography education: a systematic review. **International Research in Geographical and Environmental Education**, 2025, 34(4):326–352. DOI: `10.1080/10382046.2024.2354097`.
- SEMINAR, Y.; LAISKHANOV, S.; ISSAKOV, Y.; GAJIĆ, T. A systematic review of geographical education of students through STEM. **Frontiers in Education**, 2026, 11:1737076. DOI: `10.3389/feduc.2026.1737076`.

### History / critical thinking

- GIBSON, L.; PECK, C. L.; MILES, J.; DUQUETTE, C. Historical thinking: Trends, critiques, and future directions. **Current Opinion in Psychology**, 2025, 65:102088. DOI: `10.1016/j.copsyc.2025.102088`.
- JEGSTAD, K. M. et al. Approaches to critical thinking in primary education classrooms: A systematic review. **Educational Research Review**, 2025, 48:100711. DOI: `10.1016/j.edurev.2025.100711`.

### Science × religion boundary

- ALEXANDER, H. A.; BERGMAN, M.; PEAR, R. S. A. et al. Dialogue Between Science and Religious Education: Philosophical Reflections on Evolution Instruction Using Pedagogy of Difference. **Science & Education**, 2025. DOI: `10.1007/s11191-025-00710-8`.
- REVELL, L.; BOWIE, B.; WOOLLEY, M. et al. Teachers’ use of questions and the science/religion encounter: Basil Bernstein and the impossibility of the unthinkable. **Journal of Religious Education**, 2024, 72:295–309. DOI: `10.1007/s40839-024-00245-0`.

## 8. Promotion gate

A cross-domain claim may move from `CANDIDATE` to `SUPPORTED_SCOPED` only if:

1. corpus/source identity is known;
2. relation type is explicit;
3. at least one relevant external anchor is bound;
4. a counter-anchor, limitation or falsifier is recorded;
5. age/stage and domain scope are stated;
6. activity/test or observation procedure is defined where applicable;
7. privacy boundary is satisfied;
8. result is written to evidence/receipt layer;
9. `claim_allowed` is evaluated independently from narrative coherence.

## 9. Known gaps

- `GAP:EDU:BNCC_SKILL_CODE_BINDING` — individual card→BNCC skill codes not yet mapped.
- `GAP:EDU:50_FORMULA_PEDAGOGICAL_CROSSWALK` — 50 formula corpus not yet classified formula-by-formula for age/domain suitability.
- `GAP:EDU:FAMILY_PRIVATE_CARD_SET` — private family examples must be materialized only in Drive.
- `GAP:EDU:ASSESSMENT_RUBRIC` — evidence rubric for learner outputs remains to be validated.
- `GAP:EDU:ACCESSIBILITY` — differentiated scaffolds and accessibility profiles require explicit design/review.
- `GAP:EDU:SCIENCE_RELIGION_CASE_MATRIX` — case-by-case boundary matrix remains partial.

## R3

- `F_ok`: reproducible public method, domains, epistemic legend, academic bibliography and promotion gate materialized.
- `F_gap`: card-level BNCC mapping, private family board, 50-formula pedagogical crosswalk, assessment/accessibility validation.
- `F_next`: bind Drive pedagogical board and Master Index; append machine-readable source registry; test a first batch of cards and preserve failures/ambiguities as `TOKEN_VAZIO`.
