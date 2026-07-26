# C08 — Memory Cohesion Contract

## Estado

```yaml
contract: C08
status: IMPLEMENTED_DOCUMENTARY_AND_VALIDATION_CODE
claim_allowed: false
producer: rafaelmeloreisnovo/papers
control_plane: rafaelmeloreisnovo/Mapa
implementation_authority: rafaelmeloreisnovo/Vectras-VM-Android
physical_execution: TOKEN_VAZIO
```

## Problema fechado

Antes deste contrato, informações sobre bits, vazio, erro, redundância, prioridade,
memória quente e recuperação parcial poderiam circular como observações textuais sem
uma unidade formal comum entre `papers` e `Mapa`.

O C08 introduz:

- unidade científica RMU no produtor;
- schema e registro JSONL;
- falsificadores obrigatórios;
- três planos independentes de estado;
- pointer federado fixado por commit e blob;
- detecção local de divergência entre pins;
- testes fail-closed;
- artifacts de CI com boundary explícito.

## Fonte produtora fixada

```yaml
repository: rafaelmeloreisnovo/papers
ref: a2d23bb0e757900e840ffc95b6296ff1950b5062
path: data/memory/research_memory_units.v1.jsonl
blob_sha: 502b5786cf3a0710b2bcdbb62e3b17e9775860ab
sha256: TOKEN_VAZIO
```

O blob e o commit permitem identidade Git. A ausência de SHA-256 não é convertida em
zero e mantém a promoção bloqueada.

## Registros incorporados

| Registro Mapa | Unidade produtora | Limite |
|---|---|---|
| `MAP-RMU-001` | `RMU-LAYERSBIT4096-001` | 4.096 bits internos; fold de 256 bits; exportação integral não provada |
| `MAP-RMU-002` | `RMU-PRIORITY-ADMISSION-001` | prioridade de polling não equivale a admission control |
| `MAP-RMU-003` | `RMU-ERASURE-RECOVERY-001` | remoção unitária não prova recuperação arbitrária de 40% a 45% |

## Cadeia de autoridade

```text
Vectras source commit
→ papers RMU
→ papers validator and CI receipt
→ Mapa pointer registry
→ Mapa validator and CI receipt
→ implementation or experiment request
```

O Mapa não pode alterar `source_state` para um nível superior ao produtor.

## Artefatos C08

```text
workflows/PAPERS_MEMORY_COHESION_ROUTE.md
schemas/federated_memory_pointer.v1.schema.json
indices/MEMORY_COHESION_REGISTRY.v1.jsonl
scripts/validate_memory_cohesion_registry.py
tests/test_memory_cohesion_registry.py
.github/workflows/memory-cohesion-registry.yml
```

## Gates

### C08-G1 — identidade

- commit produtor válido;
- blob produtor válido;
- caminho explícito;
- pointer único por unidade.

### C08-G2 — autoridade

- código pertence ao repositório de implementação;
- `papers` produz memória científica;
- `Mapa` registra ponte e drift;
- execução exige receipt separado.

### C08-G3 — epistemologia

```text
zero != vazio
vazio != ausente
erro detectado != erro corrigido
redundância != recuperação comprovada
```

### C08-G4 — promoção

`claim_allowed` permanece `false` até haver evidência compatível com o escopo,
falsificadores executados e ausência de contradição bloqueante.

## TOKEN_VAZIO preservado

```yaml
source_sha256: TOKEN_VAZIO
full_4096_layer_export_receipt: TOKEN_VAZIO
priority_saturation_receipt: TOKEN_VAZIO
erasure_0_45_digest_reconstruction: TOKEN_VAZIO
physical_memory_wear_ledger: TOKEN_VAZIO
device_execution: TOKEN_VAZIO
```

## Próximo ciclo permitido

O próximo ciclo técnico pertence ao repositório de implementação e deve tratar, sem
misturar os assuntos:

1. limite exato de `lb_zero` por `sizeof` e assert de compilação;
2. exportação das camadas como API opcional;
3. admission control com receipt;
4. estado explícito de conflito triplo;
5. teste adversarial de erasure com digest final.

## Limite

C08 prova que a estrutura de integração e validação foi escrita. Não prova que os jobs
de CI executaram, que o código do Vectras foi corrigido, que houve execução em Android
ou que a recuperação parcial atingiu o percentual declarado.
