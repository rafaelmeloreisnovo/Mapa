# ZIPRAF Content-Page Execution Graph V1

Status: `CANONICAL_DRAFT / REFERENCE_MODEL`  
Data de observação: `2026-08-01`  
Claim global: `claim_allowed=false`

## 1. Entendimento consolidado

O nome ZIPRAF possui duas funções distintas:

```text
ZIP
  envelope de compatibilidade com ferramentas e sistemas atuais

RAF page graph
  organização autoral de blocos, módulos, digests, relações,
  redundância, fases, cores, épocas e evidências
```

Portanto:

```text
ZIPRAF != apenas compressão ZIP
ZIPRAF != execução arbitrária de arquivo comprimido
ZIPRAF = compatibilidade ZIP + grafo autoral delimitado
```

## 2. Fontes e interações anteriores

A análise consolidou:

- `rmr_zipraf_core`: CRC32C, hash BitRafa, assinatura e fluxo triangular;
- `BITRAF_LOSS_VECTOR_MODEL_V1`: separação entre flip, erasure, omission, permutation e `TOKEN_VAZIO`;
- `ECC32_MASKED`: equivalência funcional do cálculo de seis paridades, sem decoder físico demonstrado;
- `OMEGA_STATIC_ADDRESS_RELOCATION_INVARIANT_V1`: `Base(epoch)+StableOffset`;
- ZIPRAF/GAIA/Termux: índices, mmap, arenas, readers e escritores parciais;
- TOF/fault overlay: identidade lógica separada da tradução física e dos bad blocks.

O modelo novo não substitui essas fontes. Ele as conecta.

## 3. Invariante principal

```text
ObjectID
→ ContentDigest
→ ZIP Entry Payload Span
→ Block Local Offset
→ Module Edge
→ Core/Phase Schedule
→ Mapping Epoch
→ Physical/DMA Translation
→ Fault and Evidence Ledger
```

Endereço lógico do objeto:

```text
Address(object, epoch) =
  ArchiveBase(epoch)
  + EntryPayloadOffset
  + BlockLocalOffset(object)
```

Uma troca de base não altera o offset interno. Uma troca de conteúdo altera o digest e exige nova versão do bloco.

## 4. Acesso sem extração

A expressão “não extrair” foi tipada:

| Estado | Condição |
|---|---|
| `DIRECT_MAP_CANDIDATE` | entrada `STORE`, alinhada, imutável e com digest verificado |
| `MATERIALIZE_REQUIRED` | entrada comprimida, criptografada ou sem alinhamento suficiente |
| `EXEC_CANDIDATE` | bloco mapeável que ainda depende do loader/plataforma |
| `DMA_CANDIDATE` | região alinhada que ainda depende do driver/IOMMU |

Dados DEFLATE não são bytes executáveis ou diretamente mapeáveis em sua forma comprimida. Compatibilidade ZIP e acesso direto são propriedades separadas.

## 5. Blocos e composições

Um bloco canônico possui:

```text
block_id
offset e tamanhos
compression method
alignment
digest kind + digest
immutability
direct-map candidate
execution candidate
redundancy profile
```

Dois programas podem apontar para o mesmo bloco imutável:

```text
Program X ─┐
           ├─ digest H → shared block
Program Z ─┘
```

Quando apenas um bloco muda:

```text
H0 H1 H2 H3
      ↓
H0 H1 H2' H3
```

Somente `H2` recebe nova identidade. O manifesto superior muda porque a composição mudou, mas os blocos iguais continuam reutilizáveis.

Isso aproxima ZIPRAF de:

- armazenamento endereçado por conteúdo;
- DAG/Merkle de composição;
- overlays;
- copy-on-write;
- deduplicação de páginas imutáveis;
- scatter/gather;
- módulos carregados sob demanda.

## 6. Multicore, single-core e ciclos

Cada relação módulo-bloco inclui:

```text
core_mask
phase
access
span
```

`core_mask` define cores permitidos. `phase` define precedência lógica. O modelo permite:

- várias leituras do mesmo bloco imutável;
- módulos distintos em cores distintos;
- execução serial no mesmo core;
- simulação com vCPU/hyper-threading;
- rejeição de duas escritas sobrepostas na mesma fase.

Entretanto:

```text
phase lógica != harmônica física comprovada
clock != hash
frequência != identidade do conteúdo
```

Ciclos, cache misses, amplitude térmica e latência devem ser medidos e gravados em receipts separados.

## 7. Cabeçalhos estáticos

Assinaturas como:

```text
MZ
PE\0\0
ELF
PK\x03\x04
```

são invariantes de classificação de formato. Elas não autorizam execução nem demonstram integridade completa.

Fluxo seguro:

```text
magic
→ parser
→ bounds
→ arquitetura
→ seções/imports/relocações
→ digest/assinatura
→ política do loader
→ mapping executable
```

## 8. BitRafa e redundância

O BitRafa atual contém paridades e ECC delimitados. Nesta integração:

```text
PARITY2_OBSERVE
ECC32_MASKED_OBSERVE
```

recebem capacidade de detecção/observação, mas:

```text
recovery_claim_ppm = 0
```

Alegações de 35–45% precisam separar:

- erasures conhecidos;
- erros de posição desconhecida;
- omissions de telemetria;
- mudanças de endereço;
- alias;
- falha DMA/software;
- falha física.

Um FEC externo só pode declarar recuperação positiva quando a razão de shards, as posições conhecidas e os KATs autorizarem.

## 9. DMA, IRQ e realocação

O vínculo DMA é temporal:

```text
transaction_id
block_id
owner_core_mask
mapping_epoch
dma_address
length
expires_tick
state
```

A conclusão IRQ só é aceita com:

```text
IN_FLIGHT
AND transaction match
AND epoch match
AND TTL valid
```

A realocação segue:

```text
QUIESCE
→ VERIFY
→ REMAP
→ EPOCH_INCREMENT
→ RESUME
```

Assim, um IRQ antigo não valida uma página nova que reutilizou a posição lógica.

## 10. Hash, último estado e “blockchain”

O digest final identifica conteúdo ou composição. Ele não é a amplitude do clock nem prova causalidade física.

Permitido nesta etapa:

```text
append-only hash chain
manifest Merkle/DAG
receipts encadeados
```

Não promovido:

```text
blockchain distribuído
consenso
imutabilidade absoluta
```

Esses itens permanecem `TOKEN_VAZIO` até existir protocolo de autoridade, validação e replicação.

## 11. Permutações transdisciplinares úteis

| Área | Aplicação no ZIPRAF |
|---|---|
| sistemas de arquivos | extents, allocation epochs e sparse fault maps |
| loaders | páginas, seções, relocação e permissões RX/RW |
| bancos de dados | MVCC, snapshots, WAL e copy-on-write |
| redes | leases, sequence numbers, stale packets e TTL |
| compiladores | módulos, símbolos, IR, code sharing e link-time composition |
| sistemas distribuídos | content addressing, DAGs e receipts |
| HPC | task DAG, affinity, NUMA e work stealing |
| storage resiliente | ECC, erasure coding, scrubbing e remap |
| forense | identidade, provenance, mapping epoch e tombstones |

## 12. Gates materializados

A camada federada rejeita:

1. DEFLATE promovido a direct-map;
2. `MZ` promovido a autorização de execução;
3. hash promovido a medida de clock;
4. ponteiro absoluto reutilizado após nova época;
5. `SYSTEM` promovido a pinning;
6. paridade observacional promovida a recuperação de 45%;
7. escrita concorrente sobre mesma faixa/fase;
8. IRQ sem transaction/epoch/TTL;
9. blockchain promovido sem consenso;
10. `claim_allowed=true` neste estado.

## 13. Implementação produtora

PR produtora:

```text
rafaelmeloreisnovo/Vectras-VM-Android#1076
branch: codex/zipraf-page-graph-v1
```

Artefatos:

```text
engine/rmr/include/rmr_zipraf_page_graph.h
engine/rmr/src/rmr_zipraf_page_graph.c
demo_cli/src/zipraf_page_graph_selftest.c
tools/zipraf/test_zipraf_page_graph.sh
engine/rmr/ZIPRAF_PAGE_GRAPH_EXECUTION_INVARIANT_V1.md
.github/workflows/zipraf-page-graph.yml
```

## 14. Estado epistemológico

```yaml
zip_compatibility: SUPPORTED_BY_DESIGN
content_page_graph: REFERENCE_IMPLEMENTATION
host_local_kat: PASS_12
remote_gate: PENDING
store_direct_map: VERIFIED_AS_CONTRACT_ONLY
compressed_zero_copy: false
android_mmap: TOKEN_VAZIO
pe_elf_execution: TOKEN_VAZIO
dma_iommu_irq_runtime: TOKEN_VAZIO
octa_core_scheduler: TOKEN_VAZIO
bitflip_35_45_recovery: NOT_AUTHORIZED
blockchain_consensus: TOKEN_VAZIO
claim_allowed: false
```

## R3

```text
F_ok:
  compatibilidade ZIP e armazenamento autoral foram separados;
  blocos imutáveis, digests, módulos, fases e leases foram formalizados.

F_gap:
  parser ZIP real ligado ao grafo, mmap Android, loader,
  DMA/IOMMU, benchmark multicore e FEC externo.

F_next:
  ingerir um ZIPRAF real → construir spans a partir do central directory
  → mapear STORE alinhado → medir cópias/page faults/cache/ciclos
  → comparar single-core, multicore e materialização DEFLATE.
```
