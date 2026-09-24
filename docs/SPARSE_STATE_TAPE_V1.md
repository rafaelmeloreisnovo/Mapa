# SPARSE_STATE_TAPE_V1 — fita perfurada de deltas

State: `IMPLEMENTED_ON_DRAFT_BRANCH / CI_PENDING`

## Correção da metáfora

O núcleo não é "ZIP como compressão". É:

```text
estado base + rotas endereçáveis + redundância estrutural + deltas observados
```

Depois de vários ciclos, se a maior parte dos bytes/blocos permanece igual, a atividade pode ser registrada como uma fita esparsa:

```text
· · ● · · · ● · ...
```

`●` significa apenas "este bloco mudou entre duas observações". Não significa instrução, causa, processo, syscall ou semântica.

## Escalas separadas

A expressão "8 + 8 -> 16" é tratada como `PAIR16`:

```text
BYTE8[a] + BYTE8[b] -> WORD16
```

Isso é diferente de uma matriz 8x8.

- `BYTE8` = 8 bits.
- `PAIR16` = dois bytes adjacentes interpretados como uma palavra de 16 bits sob endian declarado.
- `GRID8x8_BITS` = 64 bits, caso uma matriz de bits seja usada.
- `BLOCK64_BYTES` = 64 bytes, uma janela de scanner separada.

Nenhuma dessas escalas deve ser promovida à outra sem uma regra explícita.

## "Colisão" de dois blocos

A metáfora de colisão é implementada como uma **família de operadores candidatos**, não como uma única operação presumida.

Para bytes `a` e `b`:

```text
OR8(a,b)
AND8(a,b)
XOR8(a,b)
ADD8_MOD256(a,b)
CONCAT16_BE(a,b)
CONCAT16_LE(a,b)
```

A escolha semântica do operador permanece:

```text
TOKEN_VAZIO_UNBOUND
```

Se "acender" significa "o bit fica 1 quando qualquer entrada é 1", isso corresponde a `OR`, não à soma aritmética. Se significa diferença/paridade, `XOR` é outra régua. A implementação não escolhe por metáfora.

## Fita de deltas

Para dois snapshots `S_t` e `S_(t+1)`:

```text
M_t = S_t XOR S_(t+1)
```

`M_t` é uma máscara de diferença, não o próximo estado por si só.

São registrados:

- bytes alterados;
- bits alterados;
- blocos alterados;
- páginas alteradas;
- CRC32 antes/depois de cada janela;
- `xor_mask`;
- fita visual de atividade.

Assim a analogia do piano/fita perfurada vira mensurável.

## Kernel

Este módulo **não afirma** que um kernel real ficará necessariamente esparso. Isso deve ser observado em snapshots reais. O módulo apenas fornece a régua para medir quanto do estado mudou.

Também não afirma que "computador só soma". Hardware real oferece cargas, armazenamentos, operações lógicas, deslocamentos, comparações, branches e muitas outras operações. A arquitetura RAFAELIA pode escolher uma álgebra reduzida para catalogação, mas ela deve ser declarada como modelo.

## SIMD

A referência Python é escalar e determinística.

`PAIR16`, `OR/XOR/AND` e comparações de blocos são operações naturalmente vetorizáveis por backends SIMD futuros. SIMD opera sobre dados carregados em registradores vetoriais através da hierarquia de memória/cache; não equivale a "pular memória".

Um backend futuro pode preservar o mesmo receipt:

```text
scalar_reference == SIMD_backend
```

para os mesmos vetores de teste.

## ZIP como mapa

O container ZIP pode usar entradas armazenadas sem compressão. Seu diretório central funciona como índice dos membros, enquanto headers locais e CRCs fornecem metadados estruturais. O projeto usa essa propriedade como rota de catálogo, sem confundir índice com execução.

## Invariantes

```text
PAIRING != ADDITION
DIFF_MASK != EXECUTION
CHANGED != SEMANTICALLY_RELEVANT
REDUNDANCY != ERROR_CORRECTION
SIMD_BACKEND != REFERENCE_SEMANTICS
ADDRESSABLE != UNDERSTOOD
```

## R3

`F_ok`: pair16, operador explícito, composição de streams e fita esparsa de deltas são formalizados.

`F_gap`: snapshots reais de kernel/processos, backend SIMD físico, álgebra canônica de composição e mapeamento de page tables permanecem TOKEN_VAZIO.

`F_next`: executar esta régua primeiro sobre artefatos controlados; só depois sobre snapshots reais, preservando fonte, ambiente e receipt.

`claim_allowed=false`
