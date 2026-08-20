# RAFAELIA — Neurocognitive/Biophysical F_next Index V1

Status: `DRAFT_GOVERNED`
Policy: `APPEND_ONLY | PROVENANCE_FIRST | TOKEN_VAZIO_VALID | claim_allowed=false`

## Regra-mãe

`SOURCE -> EXPOSURE/INTERVENTION -> SENSOR -> TRANSDUCTION -> ENDPOINT -> CAUSALITY -> FALSIFIER -> RECEIPT`

Nunca promover uma aresta por similaridade verbal. Cada ponte entre escalas exige mecanismo ou mediação medível.

## Invariantes

- `DNA_SEQUENCE != DNA_DAMAGE_ADDUCT != DNA_METHYLATION != CHROMATIN != GENE_EXPRESSION`.
- `INTENTION != DIRECT_GENOME_EDITING`.
- `SOCIAL_FIELD_METAPHOR != PHYSICAL_ELECTROMAGNETIC_FIELD`.
- `IONIZING_RADIATION != NON_IONIZING_EMF`.
- `MOLECULAR_POLARITY != MEMBRANE_ELECTRICAL_POLARIZATION != CELL_POLARITY`.
- `EVIDENCE_FOUND != GATE_CLOSED`.
- `TOKEN_VAZIO != ZERO`.

## Fila operacional

| ordem | gap | prioridade | autoridade de fechamento | gate |
|---|---|---|---|---|
| 1 | GAP-NEURO-SEMANTIC-BOUNDARY-001 | P0 | Mapa + Papers | claim grammar tipada |
| 2 | GAP-INTENT-EPIGENETIC-MEDIATION-001 | P0 | evidência científica/experimental | intervenção + mediação + replicação |
| 3 | GAP-DIET-MOLECULAR-ENDPOINTS-001 | P0 | evidência científica/experimental | composto/dose/endpoint separados |
| 4 | GAP-EMF-RADIATION-DOSIMETRY-001 | P0 | evidência científica/experimental | dosimetria + sham + controle térmico |
| 5 | GAP-BIOELECTRIC-MECHANO-THERMO-001 | P1 | evidência científica/experimental | perturbação + bloqueio/resgate |
| 6 | GAP-LANGUAGE-SOCIAL-NEURAL-001 | P1 | Papers + experimento | mediação social/cognitiva explicitada |
| 7 | GAP-UPE-BRAIN-COMMUNICATION-001 | P2-FALSIFY | experimento independente | background + detector + atribuição de fonte |

## Rotas federadas

- **Mapa:** identidade, ontologia, dependências, estados, gaps e receipts.
- **Papers:** síntese, references, claims ledger, limitações e genealogia científica.
- **RafPolimata:** validação determinística do contrato/ledger e testes adversariais computacionais.
- **RafGitTools:** control-plane, preflight, roteamento, gate e envelope de receipt.
- **Drive:** memória longitudinal/editorial, reconstrução e matriz navegável.
- **Laboratório/estudo humano:** única autoridade para fechar gates que dependem de nova medição biológica/humana.

## Critério de parada

Um `F_next` só deixa de ser aberto quando o critério de aceitação específico possui evidência adequada e rastreável. Literatura encontrada pode alterar `TOKEN_VAZIO -> EVIDENCE_FOUND_GATE_OPEN`; não produz `PASS` automaticamente.

## Artefatos locais

- `schemas/neurocognitive-biophysical-claim.schema.json`
- `data/gap-atlas/deltas/RAFAELIA_NEUROCOGNITIVE_BIOPHYSICAL_FNEXT_20260820.v1.json`

## R3

`F_ok`: ontologia, fila e contrato de promoção definidos.

`F_gap`: gates experimentais não executados neste índice.

`F_next`: materializar ledger no Papers, validador no RafPolimata, control-plane no RafGitTools e memória/planilha no Drive; depois anexar receipt federado.
