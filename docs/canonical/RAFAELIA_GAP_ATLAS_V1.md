# RAFAELIA Gap Atlas V1 — inventário federado de lacunas

**ID:** `RGA-20260810-V1`  
**Estado:** `GOVERNED_DRAFT`  
**Modo:** `APPEND_ONLY_FEDERATED`  
**Claim boundary:** `claim_allowed=false`  

## 1. Objetivo

Transformar não apenas `TOKEN_VAZIO`, mas também órfãos, duplicatas, estados stale,
limitações aceitas, dependências sem autoridade, contradições, gaps de execução e
**ausências ainda sem nome** em nós auditáveis.

O Atlas não promete eliminar toda incerteza. Ele impõe uma regra mais forte e
verificável:

> nenhuma ausência dentro de um escopo inventariado pode ser silenciosamente tratada
> como sucesso; ela precisa ser ligada a um `gap_id`, explicitamente classificada como
> falso positivo/limitação aceita, ou permanecer como candidato não mapeado.

## 2. Invariante de sete eixos

Todo registro preserva:

```text
IDENTITY
→ PROVENANCE
→ SEMANTICS
→ EXECUTION
→ EVIDENCE
→ GOVERNANCE
→ LINEAGE
```

Uma transformação de estado não pode apagar o predecessor nem fabricar a autoridade
que falta.

```text
FILE_EXISTS != INTEGRATED
INTEGRATED != BUILT
BUILT != EXECUTED
EXECUTED != DEVICE_PROVEN
CI_PASS != PHYSICAL_RUNTIME_PASS
RESOLVED_NEGATIVE != PASS
ACCEPTED_LIMITATION != RESOLVED
TOKEN_VAZIO != ZERO
```

## 3. Camadas

### Parte 1 — descoberta de repositório

O `tools/repository_gap_mapper.py` existente continua sendo o scanner de superfície.
Ele encontra marcadores, ASM não referenciado, binários sem sidecar, hashes
incompletos e documentos incompletos. Sua associação ao build é uma heurística de
triagem, não prova de compilação.

### Parte 2 — federação e identidade do vazio

O `RAFAELIA_GAP_ATLAS_V1.json` recebe gaps com:

- `gap_id` estável;
- artefato/escopo/provider;
- classe e prioridade;
- estado epistêmico/operacional;
- fatos conhecidos e desconhecidos;
- autoridade necessária;
- evidência necessária;
- falsificador/critério de aceitação;
- predecessor/sucessor;
- `next_gate`;
- `source_refs`;
- `resolution_evidence`;
- `claim_allowed=false`.

### Parte 3 — detector do que ainda não entrou no Atlas

`tools/rafaelia_gap_discovery_adapter.py` consome um Repository Gap Map e o Atlas.
Cada instância observada vira:

```text
MAPPED
ou
UNMAPPED_REQUIRES_GAP_ID
```

O adapter **não edita o Atlas automaticamente**. Isso evita transformar heurística de
scanner em autoridade sem revisão.

## 4. Snapshot inicial

O seed V1 registra 26 gaps cobrindo:

- meta-inventário Drive/GitHub;
- FCEA: canonicalidade órfã e segredo exposto;
- RLL: Bayes multi-probe, replicação independente, DESI joint, execução física,
  enforcement GitHub, crescimento `f_sigma8`, OOS e tiers CMB;
- Termux app RAFCODEΦ: matriz ARM32/ARM64 e distribuição;
- RafGitTools: APK/device/adapters e fila offline;
- RafPolimata/ApkC: cadeia ELF→APK→assinatura→NativeActivity;
- Mapa/OPCORE94: origem dos 94, regeneração e revisão independente;
- termux-packages: CI atual e dívida de memória C13;
- RAFCODEΦ delivery D4–D8;
- TORRE: disponibilidade de Actions privados e promoção dos SHA locks;
- drift entre ledgers;
- detector de gap ainda sem nome.

Este número **não é denominador de completude do ecossistema**. O próprio
`GAP-META-INVENTORY-001` permanece P0 até existirem inventários bounded dos providers.

## 5. Reconciliação da autoridade RLL

Durante a materialização foram observados dois repositórios acessíveis:

```text
instituto-Rafael/relativity-living-light
rafaelmeloreisnovo/relativity-living-light
```

O registro federado anterior apontava o segundo como autoridade científica. Porém a
camada atual de reconciliação `docs/governance/RLL_TOKEN_VAZIO_RECONCILIATION_V1.md`
foi observada no repositório `instituto-Rafael` e não foi encontrada no mesmo caminho
do repositório `rafaelmeloreisnovo`.

Por isso `indices/repository_authority_registry.json` foi reconciliado de modo
não destrutivo:

- `instituto-Rafael/relativity-living-light` = autoridade atual declarada para estado
  científico RLL;
- `rafaelmeloreisnovo/relativity-living-light` = candidato paralelo/legado com
  `evidence_state=TOKEN_VAZIO` até a relação entre as árvores ser materialmente
  demonstrada.

Isso não declara que o repositório antigo é obsoleto; apenas impede dupla autoridade
silenciosa.

Também foram registrados no authority registry:

- `RafGitTools`;
- `RafPolimata`;
- `termux-packages`.

## 6. Append-only

O snapshot atual fica em:

```text
data/gap-atlas/RAFAELIA_GAP_ATLAS_V1.json
```

Eventos de materialização/reconciliação ficam em:

```text
data/gap-atlas/RAFAELIA_GAP_EVENTS_V1.jsonl
```

Uma resolução futura deve preservar a história: `RESOLVED`,
`RESOLVED_NEGATIVE` e `REDUCED` exigem predecessor/receipts apropriados. Nenhuma
linha histórica deve ser reescrita para fingir que a lacuna nunca existiu.

## 7. Validação

Validação local:

```bash
python3 tools/validate_rafaelia_gap_atlas.py \
  --write-report artifacts/gap-atlas/validation_report.json

python3 -m unittest -v tests/test_rafaelia_gap_atlas.py
python3 scripts/validate_federated_registry.py
```

Descoberta bounded no próprio Mapa:

```bash
python3 tools/repository_gap_mapper.py \
  --root Mapa=. \
  --exclude generated \
  --exclude artifacts \
  --output-json artifacts/gap-atlas/repository_gap_map.json \
  --output-md artifacts/gap-atlas/repository_gap_map.md \
  --fail-on none

python3 tools/rafaelia_gap_discovery_adapter.py \
  --gap-map artifacts/gap-atlas/repository_gap_map.json \
  --atlas data/gap-atlas/RAFAELIA_GAP_ATLAS_V1.json \
  --output artifacts/gap-atlas/discovery_candidates.json
```

CI: `.github/workflows/rafaelia-gap-atlas.yml`.

Um workflow verde significa somente:

```text
ATLAS_INTERNAL_COHERENCE=PASS
```

Nunca significa:

```text
ALL_GAPS_RESOLVED=true
claim_allowed=true
publication_ready=true
```

## 8. Política de fechamento

Um gap sai do estado aberto somente pela autoridade correspondente.

Exemplos:

- device → receipt de device;
- branch protection → settings autenticados do GitHub;
- dado científico → dataset/likelihood oficial versionado;
- replicação independente → terceiro independente;
- segredo exposto → revogação/rotação/quarentena verificável;
- canonicalidade → identidade/linhagem/hashes;
- gap de inventário → cobertura bounded com denominador declarado.

`TOKEN_VAZIO` nunca é fechado porque outra camada ficou verde.

## 9. Próxima expansão controlada

1. Executar o scanner/adapter em cada repositório registrado no authority registry.
2. Materializar inventários bounded do Drive por provider ID/pasta/tempo.
3. Triar cada `UNMAPPED_REQUIRES_GAP_ID` para gap existente, novo gap ou evento
   explícito de falso positivo/limitação aceita.
4. Adicionar adaptadores de ledgers especializados: RLL, OPCORE94, Termux, RafGitTools,
   RafPolimata e Drive governance.
5. Detectar stale source refs e mudanças de estado sem evento predecessor/sucessor.
6. Manter `claim_allowed=false` enquanto P0 científicos/runtime/governança dependentes
   de autoridade externa ou física estiverem abertos.

## 10. R3

```text
F_ok   = Gap Atlas + schema + validator + tests + discovery adapter + CI + authority reconciliation
F_gap  = provider-wide coverage + source-specific adapters + external/physical authorities
F_next = executar bounded scans e converter todo unmapped observado em nó auditável
```
