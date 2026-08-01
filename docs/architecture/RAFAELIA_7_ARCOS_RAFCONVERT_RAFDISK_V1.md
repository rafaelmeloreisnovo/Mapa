# RAFAELIA — 7 Arcos de Fluxo para RafAlign, RafConvert e RafDisk V1

**ID:** `RAF-7ARC-20260801-V1`  
**Estado:** `DESIGN_MATERIALIZED_IMPLEMENTATION_PENDING`  
**Autoridade de ontologia:** `rafaelmeloreisnovo/Mapa`  
**Autoridade editorial:** Google Drive — `RAFAELIA — Implementação Latentes e Papers — Drive GitHub V1`  
**Claim permitido:** `false`  
**Data:** `2026-08-01`

## 0. Escopo e separação semântica

Este documento transforma a intenção recebida em arquitetura verificável, sem
promover metáforas ou fórmulas simbólicas a fatos computacionais.

A separação adotada é:

- **RafAlign**: motor genérico de cálculo de offsets, blocos, páginas, setores,
  preenchimento e restrições de alinhamento;
- **ZipAlign adapter**: adaptador específico para ZIP/APK, inspirado na classe
  de operação do `zipalign`, sem presumir que todo ZIP ou arquivo é APK;
- **RafConvert**: grafo de capacidades que analisa, planeja, transforma e
  verifica conversões entre representações;
- **RafDisk**: modelo de imagem de disco/partição e escritor transacional de
  extents; não grava dispositivo físico sem adapter e autorização explícitos;
- **RAFIR**: representação intermediária estável que impede parsers, layouts,
  codecs e backends ASM de dependerem uns dos outros.

`Zipaling` é preservado como alias textual de origem. O nome técnico adotado é
`RafAlign`, com `ZipAlign` como adapter especializado.

## 1. Invariante de sustentação

```text
bytes de entrada imutáveis
→ probe limitado por tamanho
→ RAFIR normalizado
→ plano de layout sem escrita
→ validação de limites/overflow/capacidades
→ saída em staging
→ verificação estrutural + integridade
→ publicação atômica
→ receipt append-only
```

Uma conversão só é permitida quando há uma aresta declarada no grafo de
capacidades e quando suas perdas são classificadas.

```text
convert_allowed =
    parser_supported
  ∧ writer_supported
  ∧ bounds_valid
  ∧ alignment_satisfiable
  ∧ integrity_policy_satisfied
  ∧ loss_policy_accepted
```

Quando qualquer termo não puder ser provado, o estado é `TOKEN_VAZIO`, nunca
sucesso presumido.

## 2. Os sete arcos distintos

| Arco | Vetor | Módulo | Entrada | Saída | Gate principal |
|---:|---|---|---|---|---|
| 1 | `ψ` intenção/prospecção | `raf_probe` | bytes + limites | candidatos de formato, endian, versão, confiança | assinatura e tamanho coerentes |
| 2 | `χ` observação/decodificação | `raf_decode` | candidato + bytes | RAFIR canônico | offsets e contagens dentro do arquivo |
| 3 | `ρ` ruído/layout | `raf_align` | RAFIR + perfil alvo | mapa de extents, padding e conflitos | nenhum overflow; nenhuma sobreposição indevida |
| 4 | `Δ` transformação | `raf_transform` | plano validado | operações puras e ordenadas | toda operação possui precondição e custo |
| 5 | `Σ` composição | `raf_emit` + `rafdisk` | operações + destino | imagem/arquivo em staging | escrita somente nos extents declarados |
| 6 | `Ω` verificação | `raf_verify` + `rafseal` | entrada, saída, plano | hashes, CRC, round-trip e decisão | equivalência ou perda declarada |
| 7 | `ψ′` roteamento/retro | `raf_route` + receipt | decisão + métricas | artefato publicado, relatório e próximo arco | commit atômico e receipt append-only |

O fluxo é um arco fechado, não uma linha descartável:

```text
ψ probe → χ decode → ρ align → Δ transform → Σ emit → Ω verify → ψ′ route
       ↑_______________________________________________________________|
```

## 3. Agrupamento por resultado da reflexão do modelo

### Grupo A — Descoberta sem mutação

Arcos 1 e 2. Fazem leitura limitada, identificação por assinatura e parsing
estrutural. Extensão de arquivo é apenas pista; nunca autoridade.

### Grupo B — Geometria e transformação

Arcos 3 e 4. Calculam alinhamento, extents, padding, endianness, normalização,
recompressão e canonicalização. Não escrevem destino definitivo.

### Grupo C — Materialização e prova

Arcos 5, 6 e 7. Escrevem em staging, verificam, publicam atomicamente e geram
receipt. Se o verificador não conseguir reler a saída, a publicação falha.

## 4. RAFIR — representação intermediária

O RAFIR não é um novo formato de compressão. É um contrato de memória e
serialização para descrever formatos diferentes sem fingir equivalência.

```c
typedef struct {
    raf_u64 src_offset;
    raf_u64 src_length;
    raf_u64 dst_offset;
    raf_u64 dst_length;
    raf_u64 alignment;
    raf_u64 flags;
    raf_u32 codec_id;
    raf_u32 integrity_id;
} raf_extent_v1;

typedef struct {
    raf_u32 abi_version;
    raf_u32 format_id;
    raf_u64 source_size;
    raf_u64 logical_size;
    raf_u64 feature_flags;
    raf_u64 extent_count;
    const raf_extent_v1 *extents;
} raf_ir_v1;
```

Regras:

1. todos os offsets e tamanhos são inteiros sem sinal de 64 bits;
2. toda soma e multiplicação é checada antes de executar;
3. nenhuma estrutura do arquivo é lida por cast de ponteiro não alinhado;
4. endianness é decodificado explicitamente;
5. quantidade máxima de membros/extents é definida pelo perfil;
6. parsing e escrita aceitam cursor limitado, não ponteiro solto;
7. codecs podem ser externos, mas o RAFIR permanece determinístico.

## 5. RafAlign — matriz de alinhamento

O alinhamento efetivo não é um número universal. Ele deriva das restrições do
formato, do objeto e do alvo:

```text
A_effective = LCM(A_format, A_object, A_target)
```

A fórmula só é aplicada quando:

- cada alinhamento é potência de dois ou possui adapter explícito;
- o LCM não excede o limite do perfil;
- `align_up(offset, A_effective)` não transborda;
- o padding é permitido naquele ponto do formato;
- assinatura ou checksum impactados serão regenerados e verificados.

Para potências de dois:

```text
align_up(x, a) = (x + a - 1) & ~(a - 1)
```

com teste obrigatório de `a != 0`, potência de dois e overflow de `x+a-1`.

## 6. Matriz inicial de famílias de formato

| Família | Unidade nativa | Estratégia RafAlign | Conversão direta? | Estado V1 |
|---|---:|---|---|---|
| ZIP/APK | offsets de headers/entradas | padding permitido via campos específicos; adapter preserva central directory | ZIP↔ZIP; APK exige política de assinatura | `DESIGN` |
| ISO 9660 | bloco lógico lido do volume; perfil comum 2048 B | extents por bloco e descritores | ISO↔RAW somente com perfil de filesystem | `DESIGN` |
| TAR/PAX | blocos de 512 B | conteúdo arredondado a 512 B; fim de arquivo validado | TAR↔TAR/PAX | `DESIGN` |
| AR | dialecto e membros | alinhamento do dialecto; nomes e índice tratados separadamente | AR↔AR compatível | `DESIGN` |
| CAB | offsets e blocos internos | respeitar offsets; sem impor página global | CAB↔CAB/repack via codec | `TOKEN_VAZIO_CODEC` |
| 7Z | header e streams codificados | sem alinhamento global inventado; adapter de SDK | 7Z↔7Z/repack via codec | `TOKEN_VAZIO_CODEC` |
| VHD clássico | setores/rodapé/tabelas | geometria e checksums próprios | VHD↔RAW com política explícita | `DESIGN` |
| VHDX | setores lógicos/físicos e blocos | 512/4096 conforme metadata; regiões próprias | VHDX↔RAW com adapter distinto | `DESIGN` |
| RAW/RafDisk | setores e extents declarados | perfil 512/4096 ou valor explícito | RAW↔imagem quando writer existe | `DESIGN` |
| `ARG` | desconhecida | nenhuma suposição | nenhuma | `TOKEN_VAZIO_TERM_UNRESOLVED` |

### Nota sobre `ARG`

O texto de origem pode significar `ar`, uma extensão `.arg` específica ou outro
container. Até existir assinatura, exemplo de arquivo ou especificação, a
entrada permanece `TOKEN_VAZIO_TERM_UNRESOLVED`.

## 7. RafConvert como grafo de capacidades

RafConvert não promete `N×N` conversões. Cada adapter declara arestas:

```text
edge {
  source_format
  target_format
  preserves[]
  loses[]
  requires[]
  verifier
  deterministic
  roundtrip_grade
}
```

Graus de round-trip:

- `R0_EXACT_BYTES`: bytes idênticos;
- `R1_STRUCTURAL`: estrutura e payload equivalentes, metadata pode normalizar;
- `R2_SEMANTIC`: arquivos/payload preservados, layout muda;
- `R3_LOSSY_DECLARED`: perdas aceitas por política explícita;
- `R4_PROHIBITED`: não existe equivalência segura.

Exemplos de fronteira:

- ZIP→TAR pode preservar payload, mas não toda metadata, compressão ou assinatura;
- ISO→ZIP extrai uma árvore, não preserva imagem de filesystem/boot;
- RAW→VHD encapsula setores quando geometria e tamanho são válidos;
- VHD→ZIP não é conversão direta: exige uma etapa filesystem-aware;
- APK assinado modificado precisa ser realinhado no ponto correto e reassinado;
- arquivo criptografado sem chave fica `TOKEN_VAZIO_KEY_MISSING`.

## 8. RafDisk — arquivo e partição sem confusão

RafDisk é definido em três camadas:

1. **RafDisk Map** — mapa lógico de setores, extents, lacunas e atributos;
2. **RafDisk Image** — arquivo que materializa o mapa;
3. **RafDisk Device Adapter** — acesso opcional a dispositivo real, fora do
   núcleo e bloqueado por padrão.

```text
RafDisk Map ≠ partição física
RafDisk Image = arquivo reproduzível
Device write = adapter explícito + dry-run + autorização + rollback possível
```

O V1 implementará primeiro imagens regulares. Escrita em `/dev/*`, block device,
boot record ou tabela de partição real permanece `PROHIBITED_BY_DEFAULT`.

## 9. Flags bit a bit — espaço de 64 bits

Erros não são flags. `raf_status_t` carrega o primeiro erro causal; flags
carregam capacidades e políticas combináveis.

| Bits | Classe | Exemplos |
|---|---|---|
| 0–7 | traços de formato | compressed, archive, disk-image, filesystem, streamable, random-access, signed, encrypted |
| 8–15 | I/O | read-only, seekable, sparse, in-place-eligible, staged, memory-map, chunked, external-codec |
| 16–23 | alinhamento | 2, 4, 512, 2048, 4096, 16384, 65536, custom |
| 24–31 | transformação | copy, normalize, extract, repack, recompress, canonicalize, zero-fill, deduplicate |
| 32–39 | integridade | CRC32, CRC32C, SHA-256, SHA3, BLAKE3, Merkle, signature, round-trip |
| 40–47 | ISA/backend | portable-C, ARMv7, AArch64, NEON, x86-64, SSE4.2, AVX2, CRC-extension |
| 48–55 | segurança/política | bounded, no-malloc, deterministic, no-shell, no-network, dry-run, atomic, claim-false |
| 56–63 | experimental | reservados; não persistir significado sem versionamento |

O manifesto serializado registra `abi_version`, `flag_schema_version` e nomes
textuais para impedir que um número antigo seja reinterpretado por uma versão
nova.

## 10. C freestanding e ASM inline

### Núcleo portátil obrigatório

- C freestanding sem libc, heap ou shell como requisito de correção;
- tipos com largura verificada em compile-time;
- allocator opcional por callbacks; modo arena/no-malloc padrão;
- cursor de leitura/escrita com limite;
- arithmetic helpers para add/mul/align com overflow;
- nenhum VLA, recursão não limitada ou ponteiro derivado sem range check;
- ordem determinística para membros, extents e manifests;
- writer em duas fases: `measure` e `emit`.

### ASM como backend, não como verdade

ASM inline pode acelerar apenas primitivas com referência C equivalente:

- byte-swap;
- CRC32C quando a ISA oferece instrução;
- popcount/bit scan;
- cópia/alinhamento de blocos medidos;
- hash/compress function quando houver KAT independente.

Regras obrigatórias:

1. backend C é o oráculo funcional;
2. ASM fica em `arch/<isa>/`, nunca dentro do parser de formato;
3. clobbers, constraints, alinhamento e memória são declarados;
4. dispatcher usa capacidade observada, não apenas macro de compilação;
5. teste diferencial compara C e ASM bit a bit;
6. falha do backend retorna ao C sem mudar semântica;
7. benchmark não promove claim de correção.

### Targets iniciais

```text
portable-c  = referência
armv7       = alvo Termux 32-bit / NEON opcional
AArch64     = alvo Android 64-bit
x86_64      = replicação e CI pública quando disponível
```

## 11. Dimensionamento e limites

Todo profile possui limites explícitos:

```text
max_input_bytes
max_output_bytes
max_entries
max_extents
max_name_bytes
max_recursion_depth
max_alignment
max_ratio_expansion
memory_budget_bytes
time_budget_class
```

Defaults conservadores não são especificação de formato. Um arquivo maior que
o perfil retorna `RAF_E_LIMIT`, não é truncado.

Proteções mínimas:

- zip bomb / expansion ratio;
- path traversal e nomes absolutos;
- symlink/hardlink policy;
- sparse extent overflow;
- sobreposição de partições/extents;
- integer wraparound;
- checksum/signature stale;
- escrita parcial e crash consistency;
- payload criptografado ou codec ausente.

## 12. CLI planejada

```text
rafconvert probe INPUT
rafconvert plan INPUT --to FORMAT --profile PROFILE
rafconvert verify INPUT [--deep]
rafconvert convert INPUT OUTPUT --to FORMAT --profile PROFILE --dry-run
rafdisk inspect IMAGE
rafdisk plan MANIFEST
rafdisk build MANIFEST OUTPUT --staging DIR
rafdisk verify IMAGE --manifest MANIFEST
rafalign check INPUT --profile PROFILE
```

O executor recebe vetor de argumentos e não invoca shell. A execução destrutiva
não existe no V1.

## 13. Receipts e proveniência

Cada execução registra:

```text
receipt_id
schema_version
source_hashes
source_size
probe_result
selected_adapter
capability_edge
profile_hash
layout_plan_hash
output_hashes
verification_grade
losses_declared
backend_used
backend_equivalence_result
claim_allowed=false
TOKEN_VAZIO[]
```

O receipt é append-only e não substitui o arquivo de entrada.

## 14. Gates de implementação

| Gate | Objetivo | Critério |
|---|---|---|
| `RAF-G0` | headers compilam | 4 targets, warnings como erro, sem libc requerida |
| `RAF-G1` | cursor e overflow | property tests + casos-limite |
| `RAF-G2` | probe | corpus positivo/negativo por formato |
| `RAF-G3` | RAFIR | parse→serialize determinístico |
| `RAF-G4` | RafAlign | extents sem overlap e padding válido |
| `RAF-G5` | writer | measure==bytes emitidos |
| `RAF-G6` | round-trip | graus R0/R1/R2 verificados por adapter |
| `RAF-G7` | ASM | equivalência bit a bit C↔ASM + KAT |
| `RAF-G8` | Termux | receipt observado no commit exato |
| `RAF-G9` | segurança | corpus malformado, fuzz e limites |

## 15. Relação com o Mapa existente

A arquitetura respeita a Foundation local já canonizada:

```text
init → plan → verify → explicit run → receipt
```

Também reutiliza a disciplina do mapa 7D: separar modelo, precondição,
resultado computacional e afirmação física. Aqui, “sete direções” é topologia
de workflow e roteamento; não é por si só prova matemática ou física de um
toro `T^7`.

As fórmulas simbólicas fornecidas ficam classificadas como:

- linguagem de organização/ontologia quando mapeiam `ψχρΔΣΩ`;
- hipótese/modelo quando propõem funções mensuráveis;
- `TOKEN_VAZIO` quando não há unidade, domínio, dataset ou falsificador;
- fora do núcleo binário quando tratam significado espiritual.

## 16. Estrutura proposta de repositórios

```text
Mapa/
  docs/architecture/RAFAELIA_7_ARCOS_RAFCONVERT_RAFDISK_V1.md
  data/contracts/RAF_FORMAT_ALIGNMENT_MATRIX_V1.csv
  foundation/contracts/rafconvert/raf_core_v1.h

RafConvert/                 # implementação futura dedicada
  include/raf/
  src/core/
  src/formats/{zip,iso,tar,ar,cab,7z,vhd,vhdx,raw}/
  src/arch/{portable,armv7,aarch64,x86_64}/
  tests/{fixtures,negative,roundtrip,kats}/

RafDisk/                    # pode iniciar como módulo do RafConvert
  src/map/
  src/image/
  src/partition/
  src/device/               # bloqueado por padrão
```

Até existir repositório dedicado e teste real, `Mapa` preserva o contrato, não
finge conter a implementação completa.

## 17. Decisão V1

```text
architecture_defined=true
seven_arcs_defined=true
flag_schema_defined=true
format_matrix_seeded=true
freestanding_contract_seeded=true
portable_reference_implemented=false
asm_backends_implemented=false
format_adapters_implemented=false
termux_receipt_observed=false
claim_allowed=false
```

## 18. R3

`F_ok`: sete arcos, fronteiras de módulo, RAFIR, flags, alinhamento, política ASM,
matriz de formatos, gates e receipts foram definidos.  
`F_gap`: `ARG` não foi identificado; codecs, parsers, writers, KATs e receipts
Termux ainda não existem neste trabalho.  
`F_next`: implementar primeiro `raf_core_v1.h` + cursor/overflow + `raf_probe`
para ZIP/TAR/RAW, gerar corpus negativo e produzir o primeiro receipt local.