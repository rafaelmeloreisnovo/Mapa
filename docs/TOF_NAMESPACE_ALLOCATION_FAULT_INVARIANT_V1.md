# TOF–Namespace–Allocation–Fault Invariant V1

Status: `CANONICAL_DRAFT`  
Data de observação: `2026-08-01`  
Branch de implementação: `codex/tof-fault-invariant-v1`  
Claim global: `claim_allowed=false`

## 1. Intenção

Este documento formaliza a distinção entre:

1. identidade lógica de arquivos e diretórios;
2. metadados e namespace;
3. alocação lógica de conteúdo;
4. tradução para mídia física;
5. mapa esparso de falhas, bad blocks e remapeamentos;
6. vazio semântico, zero numérico, byte zero e estado desconhecido.

A abstração foi motivada pela observação de que um arquivo pode continuar visível, com nome, extensão, índice e tamanho conhecidos, enquanto parte do suporte físico que carregava seu conteúdo se torna ilegível.

A arquitetura canônica é:

```text
namespace
  → object record
  → logical allocation
  → physical translation
  → fault overlay
  → evidence / repair / remap
```

## 2. Invariantes fundamentais

```text
arquivo != bloco físico
nome != conteúdo
índice zero != ausência
tamanho zero != arquivo ausente
byte 0x00 != ausência
bad block != vazio
TOKEN_VAZIO != 0
entrada visível != conteúdo válido
remapeamento físico não deve mudar a identidade lógica
claim_allowed=false enquanto não houver implementação, KAT e evidência de execução
```

Formalmente:

```text
∅ != 0 != 0x00 != BAD != TOKEN_VAZIO
```

E:

```text
ObjectID_antes = ObjectID_depois
PhysicalBlock_antes != PhysicalBlock_depois
```

quando ocorre remapeamento físico coerente.

## 3. Três florestas sobrepostas

### 3.1 Namespace forest

Declara o que aparece ao usuário:

```text
parent directory
  └── directory entry
      ├── object_id
      ├── name bytes
      ├── extension
      ├── type
      └── generation
```

### 3.2 Allocation forest

Declara onde o conteúdo lógico está:

```text
object_id
  → logical offset
  → logical extent
  → translated physical extent
```

### 3.3 Fault forest

Declara quais regiões físicas perderam confiabilidade:

```text
device
  → channel
  → bank
  → block
  → page
  → word
  → lane
  → bit
  → fault event
```

A composição é:

```text
F_sistema = F_namespace ⊕ F_allocation ⊕ F_faults
```

A floresta de faults não reescreve retroativamente a floresta de identidade. Ela acrescenta uma sobreposição temporal e auditável.

## 4. TOF geométrica: base 9 como 6 + 3

O registro lógico mínimo usa três eixos:

```text
I = índice / identidade
N = nome / metadado
B = blocos / payload
```

Cada eixo possui dois estados ativos:

```text
+ = presente, válido ou ligado
- = retirado, inválido, defeituoso ou tombstone
```

Logo:

```text
3 × 2 = 6
```

Acrescentando um estado zero localizado a cada eixo:

```text
I0 = índice não alocado
N0 = nome ausente
B0 = nenhum bloco de dados
```

temos:

```text
3 × 2 + 3 = 9
```

Alfabeto geométrico:

```text
B9G = {I0,I+,I-,N0,N+,N-,B0,B+,B-}
```

Um objeto completo é uma tripla:

```text
F = (I,N,B), com I,N,B em {0,+,-}
```

Assim existem `3³ = 27` configurações compostas possíveis.

## 5. Estados canônicos de objeto

| Tripla | Estado | Interpretação |
|---|---|---|
| `(I+,N+,B+)` | `NORMAL` | identidade, nome e conteúdo presentes |
| `(I+,N+,B0)` | `EMPTY_FILE` | arquivo existente com zero bytes |
| `(I+,N+,B-)` | `PAYLOAD_FAULT` | entrada visível, payload ilegível ou retirado |
| `(I+,N-,B+)` | `NAME_FAULT` | identidade e dados existem, nome inválido |
| `(I0,N+,B+)` | `ORPHANED_OBJECT` | nome/conteúdo sem identidade válida |
| `(I0,N0,B+)` | `RESIDUAL_BLOCKS` | blocos residuais sem vínculo lógico |
| `(I-,N-,B-)` | `TOMBSTONE` | remoção lógica preservada para auditoria |
| `(I0,N0,B0)` | `ABSENT` | nenhum objeto declarado |
| qualquer tripla não demonstrada | `TOKEN_VAZIO` | evidência insuficiente |

Essas combinações são estados epistemológicos e estruturais. Não equivalem automaticamente ao comportamento de um filesystem específico.

## 6. Zero tipado

Todo zero deve carregar contexto:

| Campo | Zero tipado |
|---|---|
| `object_index=0` | primeira posição ou posição reservada pelo formato |
| `name_length=0` | nome de comprimento zero, se permitido |
| `name_byte=0x00` | byte NUL dentro da codificação declarada |
| `logical_size=0` | objeto existente sem payload |
| `first_extent=null` | nenhuma extensão alocada |
| `block_state=FREE` | bloco disponível para alocação |
| `presence_state=ABSENT` | objeto não declarado |
| `claim_state=TOKEN_VAZIO` | estado ainda não demonstrado |

Nenhum parser pode inferir ausência apenas porque encontrou o valor numérico zero.

## 7. Lastro lógico estável

O lastro mínimo é:

```text
FILE_ANCHOR
├── object_id
├── parent_id
├── generation
├── name_bytes
├── name_encoding
├── logical_size
├── object_type
├── logical_extent_map
├── metadata_integrity
├── content_integrity
├── mapping_epoch
└── object_state
```

A identidade canônica deve ser independente da posição física:

```text
Name → ObjectID → LogicalExtent → PhysicalExtent
```

Nunca:

```text
Name → PhysicalBlock
```

Essa separação permite substituir um bloco defeituoso sem alterar nome, índice ou identidade lógica.

## 8. Mapa esparso de faults

A maioria das regiões não precisa receber um registro explícito `GOOD`. O ledger pode registrar apenas exceções e eventos:

```text
FAULT_KEY = <
  device_id,
  channel,
  bank,
  block,
  page,
  word,
  lane,
  bit,
  epoch
>
```

Estados permitidos:

```text
GOOD_OBSERVED
CORRECTED
SUSPECT
BAD
REMAPPED
POISONED
ABSENT
TOKEN_VAZIO
```

Registro:

```text
FAULT_EVENT
├── event_id
├── fault_key
├── state_before
├── state_after
├── syndrome
├── corrected_count
├── first_seen
├── last_seen
├── replacement_location
├── evidence_refs
├── previous_event_hash
└── event_hash
```

`GOOD_OBSERVED` significa apenas que nenhum erro foi detectado no escopo dos testes registrados.

## 9. Arquivos contêiner

Um arquivo ZIP, banco, imagem de disco ou pacote contém uma segunda camada de indexação:

```text
filesystem namespace
  └── container object
      └── internal directory/index
          └── internal payload
```

Portanto, é possível:

```text
container visível
+ índice interno legível
+ nomes internos recuperáveis
+ payload interno parcialmente corrompido
```

A listagem de nomes não promove o conteúdo para `VALID`.

## 10. Transições

### Criar arquivo vazio

```text
(I0,N0,B0) → (I+,N+,B0)
```

### Escrever o primeiro conteúdo

```text
(I+,N+,B0) → (I+,N+,B+)
```

### Detectar falha física

```text
(I+,N+,B+) → (I+,N+,B-)
```

### Remapear mantendo identidade

```text
logical extent L
physical P_old = BAD
physical P_new = replacement
ObjectID permanece estável
mapping_epoch = mapping_epoch + 1
```

### Excluir sem apagar o histórico

```text
(I+,N+,B+) → (I-,N-,B-) → eventual reciclagem
```

A reciclagem não deve apagar o ledger histórico que já foi promovido como evidência.

## 11. Limites de claim

Este documento prova apenas:

- coerência interna do modelo;
- separação explícita entre identidade, alocação e faults;
- existência de um contrato de dados versionado;
- presença de lacunas registradas.

Ele não prova:

- que uma mídia real foi testada;
- que um filesystem existente implementa exatamente a TOF geométrica;
- que um ECC ou BBT específico foi validado;
- que houve recuperação física de dados;
- que os 27 estados são todos alcançáveis ou desejáveis em uma implementação concreta.

Estado:

```yaml
status: CANONICAL_DRAFT
claim_allowed: false
implementation_state: TOKEN_VAZIO
runtime_evidence: TOKEN_VAZIO
ecc_profile: TOKEN_VAZIO
physical_media_profile: TOKEN_VAZIO
```

## 12. Próximo passo verificável

```text
schema + instância
→ validador determinístico
→ fixtures positivas e adversariais
→ simulador de alocação/remapeamento
→ fault injection
→ KAT de transições
→ relatório com hashes
→ implementação freestanding
→ teste em mídia ou emulador declarado
```

## R3

```text
F_ok   = identidade lógica, zero bytes, alocação e bad blocks separados em três florestas
F_gap  = filesystem-alvo, ECC, política de remapeamento e evidência física permanecem TOKEN_VAZIO
F_next = validar schema e construir simulador determinístico de NamespaceMap + AllocationMap + SparseFaultMap
```
