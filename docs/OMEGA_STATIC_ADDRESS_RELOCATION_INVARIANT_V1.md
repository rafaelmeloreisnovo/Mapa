# Ω Static Address, Relocation and ZIPRAF Invariant V1

Status: `CANONICAL_DRAFT / REFERENCE_GATE_PASS`  
Data de observação: `2026-08-01`  
Claim global: `claim_allowed=false`

## 1. Intenção

Este documento federa evidências existentes em PCR Rafaelia, Termux/Rafacodephi, Vectras/RMR, GAIA e ZIPRAF sem confundir três planos:

```text
offset relativo
endereço virtual
posição física
```

A invariante é:

```text
Address(object, epoch) = Base(epoch) + StableOffset(object)
```

Uma tabela de offsets pode ser reutilizada quando o manifesto estrutural permanece idêntico. Ponteiros absolutos só podem ser reutilizados quando base, época e manifesto permanecem iguais.

## 2. O que já existe

### PCR Rafaelia

Há documentação de transformação para allocators próprios, syscalls diretas e redução de dependências. Parte permanece roadmap e não é tratada como execução provada.

### Termux/Rafacodephi

Existem arenas bump, contratos `NoMalloc`, emissores ELF executáveis delimitados e validadores. O contrato APKC declara honestamente que linker geral, símbolos e relocações arbitrárias permanecem `TOKEN_VAZIO`.

### Vectras/RMR

Existem pools estáticos, arena BSS, rollback por marca, ZIPRAF STORE validado, mapeamento por extent/janelas e a implementação de referência `rmr_static_layout` para manifesto imutável, binding de base e resolução por offset.

A implementação foi integrada por squash na PR `Vectras-VM-Android#1074`, commit:

```text
8f54f929460c5f33ed5b1a7856460499b4439eef
```

O gate focal `RMR Static Layout Invariant` passou no head testado `c6af39cda44d838123b785b4d75d7ac0103b7cc5`, run `30697373545`. Falhas de workflows gerais não foram promovidas como evidência desta unidade delimitada.

### GAIA

Existe evidência delimitada de ELF32 ARM estático, sem `PT_INTERP`, sem `PT_DYNAMIC`, sem símbolos externos indefinidos e com zero relocações no artefato observado. Isso é userspace loaderless Linux/Android, não firmware físico.

### Google Drive/ZIPRAF

Há índices, logs e pastas históricas ZIPRAF. Eles são fontes de investigação e proveniência; não promovem automaticamente zero-copy, endereço físico fixo ou validade universal.

## 3. Separação obrigatória

```text
FIXED_OFFSET
  posição relativa imutável dentro do layout

FIXED_VIRTUAL
  endereço virtual imutável dentro do processo/escopo declarado

FIXED_PHYSICAL
  posição física imutável na plataforma declarada
```

Logo:

```text
FIXED_OFFSET != FIXED_VIRTUAL != FIXED_PHYSICAL
```

Em Android/Linux com ASLR, a política padrão segura é:

```text
BASE_RELATIVE + IMMUTABLE_OFFSETS
```

Em firmware bare-metal, `FIXED_PHYSICAL` exige linker script, memory map, plataforma e execução específicos.

## 4. Mobilidade

| Estado | Significado |
|---|---|
| `MOVABLE_BASE` | a base pode mudar, offsets não |
| `FIXED_OFFSET` | região não muda de posição dentro do manifesto |
| `PINNED_RUNTIME` | base não muda enquanto o vínculo está ativo |
| `REMAP_ONLY` | mudança somente por nova época auditável |
| `PHYSICAL_FIXED` | exige prova física específica |
| `TOKEN_VAZIO` | condição não demonstrada |

Atributos `HIDDEN`, `READ_ONLY`, `SYSTEM` e `ARCHIVE` pertencem ao plano de atributos de arquivo. Eles não equivalem a pinning de memória ou cluster.

## 5. Semântica `SCH/sch`

Até que uma definição histórica anterior seja localizada, a sequência `S c h s C H` é preservada como vocabulário RAFAELIA provisório e qualificado.

```text
SCH — estrutura
S = STATIC_OFFSET
C = CONTIGUOUS_REGION
H = HANDLE_RELATIVE

sch — evidência
s = stable layout epoch
c = checked bounds/alignment
h = hashed manifest signature
```

A forma sem domínio nunca deve ser usada como claim técnico externo.

## 6. Reutilização

```text
reuse(offset_table) :=
  manifest_signature_before == manifest_signature_after

reuse(absolute_pointer) :=
  same_manifest
  AND same_base
  AND same_mapping_epoch
```

Trocar somente a base permite conservar todos os offsets:

```text
B0 + Δi  →  B1 + Δi
```

Não é necessário relocar cada objeto quando as referências armazenadas são `region_id + local_offset`.

## 7. Fragmentação

Uma arena/pool predefinida pode eliminar fragmentação externa dentro daquele escopo quando usa bump allocation e reset/rollback por época. Isso não elimina automaticamente:

- padding de alinhamento;
- fragmentação do filesystem;
- tradução de páginas virtuais;
- wear leveling/FTL;
- page faults;
- múltiplos mappings;
- desperdício por superdimensionamento.

Portanto:

```text
FRAGMENTATION_FREE_ARENA != FRAGMENTATION_FREE_SYSTEM
```

## 8. ZIPRAF

Para `STORE` validado:

```text
payload_base = archive_base + local_header_offset + metadata_size
object_address = payload_base + stable_relative_offset
```

O mapa interno pode ser reutilizado se:

1. diretório central e registro local forem coerentes;
2. extent, tamanho e CRC continuarem válidos;
3. assinatura do manifesto interno for idêntica;
4. a política de época permitir o binding.

O runtime Java atual não é promovido a `ZERO_ALLOCATION_RUNTIME`: a verificação CRC aloca buffer e o mapeamento possui limites declarados.

## 9. Relação com TOF e faults

Este contrato compõe o documento TOF existente:

```text
ObjectID
→ RelativeSpan
→ LogicalMappingEpoch
→ PhysicalTranslation
→ SparseFaultOverlay
```

Quando um bloco falha:

```text
StableOffset permanece
MappingEpoch aumenta
PhysicalTarget pode mudar
FaultLedger preserva o destino anterior
```

Uma região `FAULT`, `ABSENT` ou `TOKEN_VAZIO` não pode ser resolvida como payload válido.

## 10. Fontes federadas

| Repositório | Fonte | Estado |
|---|---|---|
| PCR Rafaelia | `BAREMETAL_ARCHITECTURE_ANALYSIS.md` | `DOCUMENTED_ROADMAP` |
| Termux | `bootstrap_rafaelia/raf_arena.h` | `SOURCE_PRESENT` |
| Termux | `app/src/main/cpp/lowlevel/baremetal_nomalloc.h` | `SOURCE_PRESENT` |
| Termux | `docs/APKC_EXECUTABLE_ELF_CONTRACT.md` | `VERIFIED_LIMITED` |
| Vectras | `engine/rmr/include/rmr_vectra_os.h` | `SOURCE_PRESENT` |
| Vectras | `app/.../ZiprafDirectRuntime.kt` | `SOURCE_AND_TESTS_PRESENT` |
| Vectras | `engine/rmr/include/rmr_static_layout.h` | `VERIFIED_LIMITED @ 8f54f929` |
| Vectras | `engine/rmr/src/rmr_static_layout.c` | `VERIFIED_LIMITED @ 8f54f929` |
| GAIA | `native/rafaelia_omega_v32/README.md` | `VERIFIED_LIMITED` |
| Mapa | `TOF_NAMESPACE_ALLOCATION_FAULT_INVARIANT_V1.md` | `CANONICAL_DRAFT` |

## 11. Gates

A camada federada rejeita:

- `FIXED_OFFSET` promovido como endereço físico;
- `SYSTEM` promovido como pinning;
- reutilização de ponteiro absoluto após troca de base/época;
- região sobreposta ou desalinhada;
- claim físico sem plataforma e evidência;
- região `FAULT` exposta como válida;
- `TOKEN_VAZIO` com `claim_allowed=true`.

Evidência desta versão:

```text
Vectras focal run: 30697373545 = success
Mapa focal run inicial: 30697464194 = success
Mapa reconciliation: 30697464230 = success
Mapa CI inicial: 30697464214 = success
```

As atualizações de reconciliação após o merge do Vectras exigem novo gate sobre o head final antes da integração desta PR.

## 12. Limites

```yaml
relative_layout_reference: VERIFIED_LIMITED
host_gate: PASS
android_aslr_fixed_virtual: TOKEN_VAZIO
physical_address_fixed: TOKEN_VAZIO
zipraf_end_to_end_zero_copy: TOKEN_VAZIO
zipraf_zero_allocation_runtime: false_for_current_java_path
independent_reproduction: TOKEN_VAZIO
claim_allowed: false
```

O `PASS` confirma o contrato C delimitado em host. Não confirma pinning físico, estabilidade virtual Android ou ausência global de cópias/alocações.

## R3

```text
F_ok:
  arenas estáticas, ZIPRAF STORE, ELF sem relocações e fault overlay
  foram organizados por uma única invariante de base + offset

F_gap:
  prova física, ASLR, linker geral, ZIPRAF >2GiB e medição independente

F_next:
  integrar manifesto ao ZIPRAF → medir mappings/page faults/cópias
  → executar em Android e QEMU com receipts separados
```
