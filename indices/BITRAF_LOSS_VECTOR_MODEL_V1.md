# BITRAF — Modelo de Perda, Erasure, Síndrome e Índice Vetorial V1

Status: `CANONICAL_DRAFT`  
Modo: `EXECUÇÃO_NÃO_DESTRUTIVA`  
Claim global: `claim_allowed=false`  
Data: 2026-07-26

## 0. Objetivo

Organizar o problema descrito como “o bit some” em estados tecnicamente distintos, preservar a geometria autoral como camada de indexação e impedir que semelhança vetorial seja confundida com recuperação exata.

```text
observação física/lógica
→ classificação do evento
→ localização na matriz
→ síndrome/paridade
→ recuperação FEC quando matematicamente autorizada
→ índice vetorial auxiliar
→ hipótese causal
→ experimento/falsificador
```

## 1. Fontes inspecionadas

| Repositório | Snapshot | Artefato | Leitura |
|---|---|---|---|
| `rafaelmeloreisnovo/Rafaelia_Private` | `cebabd2178000d063aa147a4fe68521b192254a1` | `core a incluir/raf_crc_ecc_tool.c` | CRC32C/CRC64 e uma paridade XOR por faixa; recupera um shard ausente |
| `rafaelmeloreisnovo/Rafaelia_Private` | mesmo | `new_data/fiber_ecc.c` | esqueleto H1/H2/M; matrizes ainda sem inicialização operacional |
| `rafaelmeloreisnovo/Rafaelia_Private` | mesmo | `core a incluir/fec_src_rs_gf256_Version2.c` | tentativa Reed–Solomon GF(256); requer correções antes de claim de recuperação |
| `rafaelmeloreisnovo/Rafaelia_Private` | mesmo | `scripts/bitraf_crystal_compare.py` | comparação Python/C/golden com registro do primeiro byte divergente |
| `rafaelmeloreisnovo/Rafaelia_Private` | mesmo | `Anews/RAFAELIA_SPIRAL_FIBONACCI_Version2.py` | espirais geométrica/Fibonacci/inversa e embeddings D |
| `rafaelmeloreisnovo/Rafaelia_Private` | mesmo | `vectras_integration/geometry/bitraf_state.py` | estados vetoriais e transformações Σ/Ω/Δ/Φ |
| `rafaelmeloreisnovo/papers` | `cf7b4a697e44f251ab3b9000b00d0bf1d72fcec6` | `docs/matematica_autoral/INVENTARIO_60...md` | Fibonacci-Rafael, espiral hexagonal, BITRAF 42 bits, régua adaptativa e TOKEN_VAZIO tipado |
| `rafaelmeloreisnovo/RafPolimata` | `1e63c6edc07144936102dbda0929b67d4391dc21` | `scripts/contextual_relational_tensor.py` | matriz externa auditável e abstinência por gaps |

## 2. As quatro coisas que não podem ser colapsadas

| Estado | Símbolo | Significado |
|---|---:|---|
| zero observado | `0` | valor binário conhecido |
| um observado | `1` | valor binário conhecido |
| erasure | `?` | coordenada conhecida; valor desconhecido |
| TOKEN_VAZIO | `⊥τ` | evidência insuficiente, origem ausente ou evento não observado |

`null` em JSON não significa bit zero.  
Um `erasure` não é necessariamente um bit flip.  
Um byte ausente do log não prova perda física no semicondutor.

## 3. Classificação mínima do evento

```yaml
MATCH: esperado == observado
FLIP_0_TO_1: esperado=0, observado=1
FLIP_1_TO_0: esperado=1, observado=0
ERASURE: posição conhecida, valor não lido
OMISSION: registro esperado não chegou ao coletor
OVERWRITE: outra escrita substituiu o valor
PERMUTATION: valor mudou de endereço por transformação deliberada
ALIAS: dois endereços apontaram para o mesmo armazenamento
TOKEN_VAZIO_EXPECTED: não existe referência confiável
TOKEN_VAZIO_OBSERVED: coleta ausente sem localização de erasure
```

A causa física permanece separada:

```yaml
THERMAL_OR_RTN: hipótese
LEAKAGE_OR_RETENTION: hipótese
TIMING_MARGIN: hipótese
SUPPLY_DROOP: hipótese
RADIATION_SEU: hipótese
SOFTWARE_OR_DMA: hipótese
MAPPING_OR_ENDIANNESS: hipótese
UNKNOWN: TOKEN_VAZIO
```

## 4. Estado real dos mecanismos encontrados

### 4.1 CRC + paridade XOR

O `raf_crc_ecc_tool.c`:

- detecta divergência por CRC;
- divide o payload em `k` shards;
- cria uma paridade XOR;
- reconstrói exatamente um shard ausente se todos os demais estiverem presentes.

Não corrige uma superfície arbitrária de 40–45% de bits alterados.

### 4.2 `fiber_ecc.c`

A forma desejada está visível:

\[
b \rightarrow p_1=H_1b \rightarrow p_2=H_2x \rightarrow u=Mv \pmod 2.
\]

Mas `H1`, `H2_idx` e `M` são declaradas estaticamente e o inicializador contém apenas comentário. No snapshot auditado, o mecanismo é `CONCEPTUAL_SKELETON`, não ECC validado.

### 4.3 Reed–Solomon GF(256)

Há código para `k` shards de dados e `m` shards de paridade, porém o snapshot não pode ser promovido:

1. a construção do campo usa acumulador de 8 bits antes da redução pelo polinômio `0x11d`;
2. o codificador usa linhas de Vandermonde apenas para paridade;
3. o recuperador trata também shards de dados como linhas de Vandermonde, sem matriz geradora sistemática consistente;
4. não há fixture demonstrando recuperação para todas as combinações de até `m` erasures.

Status: `BLOCKED_FOR_CORRECTION_AND_TESTS`.

## 5. Limite de 40–45%

A pergunta precisa ser dividida.

### Erasures conhecidos

Para um código de comprimento \(n=k+m\), com \(m\) símbolos de redundância, um código MDS ideal pode recuperar até \(m\) erasures:

\[
|E|\le m.
\]

Para tolerar fração \(p=0{,}45\):

\[
\frac{m}{k+m}\ge 0{,}45
\quad\Longrightarrow\quad
\frac{m}{k}\ge \frac{0{,}45}{0{,}55}\approx0{,}8182.
\]

Ou seja: aproximadamente 82 símbolos de paridade para cada 100 símbolos de dados, antes da margem operacional.

### Erros de posição desconhecida

Para erros desconhecidos, a capacidade cai aproximadamente pela metade em um código MDS:

\[
2t+e\le n-k,
\]

onde \(t\) é o número de erros desconhecidos e \(e\) o número de erasures conhecidos.

Logo, “45% perdido” só é uma meta razoável se a maior parte das posições ausentes for conhecida e a redundância tiver sido projetada para isso.

## 6. Núcleo algébrico coerente com a intuição binária

No campo binário \(\mathrm{GF}(2)\):

\[
1+1=0,\qquad -1=1,
\]

portanto:

\[
a-b=a+b=a\oplus b.
\]

Isso permite formalizar a ideia de “não há subtração separada” **dentro do domínio GF(2)**. Fora desse domínio, a frase não deve ser promovida a afirmação universal sobre física ou matemática.

## 7. Recuperação exata por síndrome

Considere:

\[
x\in\{0,1\}^n,\qquad H\in\{0,1\}^{r\times n},
\qquad Hx^\top=0.
\]

Com vetor recebido \(y\):

\[
s=Hy^\top.
\]

Se o conjunto de erasures \(E\) é conhecido e \(K\) é o conjunto conhecido:

\[
H_E x_E^\top
=
H_K x_K^\top
\pmod2.
\]

A recuperação é autorizada somente quando o sistema possui solução única. Caso contrário:

```text
recovered_bit = TOKEN_VAZIO
reason = underdetermined_or_inconsistent_syndrome
```

## 8. Banco vetorial: papel permitido

O índice vetorial guarda **observações**, não “a verdade do bit”.

Vetor externo proposto:

\[
v_i=[
x,y,z,t,\ell,
f(\ell),
h_x,h_y,
o_x,o_y,
b_e,m_e,b_o,m_o,
T,V,L,
shard,stripe,
density(s),
|P_i|,
onehot(class)
].
\]

Onde:

- \(\ell\): índice linear;
- \(f(\ell)\): índice Fibonacci mais próximo;
- \((h_x,h_y)\): projeção hexagonal de 60°;
- \((o_x,o_y)\): projeção octogonal de 45°;
- \(s\): síndrome;
- \(P_i\): conjuntos de paridade aos quais o bit pertence.

Usos permitidos:

- encontrar superfícies de erro semelhantes;
- localizar regiões recorrentes;
- comparar temperatura/tensão/latência;
- priorizar testes;
- sugerir candidato histórico com rótulo `HEURISTIC_ONLY`.

Uso proibido:

- substituir ECC;
- declarar causa térmica pela proximidade vetorial;
- preencher `TOKEN_VAZIO` como 0;
- afirmar reconstrução exata sem síndrome, hash ou referência íntegra.

## 9. Geometria de salto

### Espiral hexagonal

\[
z_n=r_0q^ne^{i(\theta_0+n\pi/3)},
\qquad q=\frac{\sqrt3}{2}.
\]

### Projeção octogonal

\[
o_n=(\cos(n\pi/4),\sin(n\pi/4)).
\]

### Caminho admissível

Não se afirma que só exista um caminho geométrico. Define-se o caminho operacional escolhido:

\[
P^\star=
\arg\min_{P\in\mathcal P}
\left[
\alpha\,C_{compute}(P)+
\beta\,C_{redundancy}(P)+
\gamma\,C_{uncertainty}(P)
\right]
\]

sujeito a:

\[
H x^\top=0,\quad
hash(x)=hash_{ref},\quad
provenance(P)=1.
\]

A unicidade só existe se o argmin for único e os gates forem satisfeitos.

## 10. Protocolo experimental

Cada ensaio deve gravar:

```text
device_id_pseudonymous
build_id / kernel / firmware
matrix_id / pattern_id / seed
address logical + physical when available
expected / observed / erasure mask
temperature sensor + sensor path
voltage/frequency state when observable
timestamp monotônico
CPU/GPU/DMA owner
cache state / flush policy
ECC syndrome / corrected / uncorrected counter
repeat number
hash before / hash after
```

Experimentos mínimos:

1. padrões `00`, `FF`, `AA`, `55`, walking-1 e walking-0;
2. leitura repetida sem escrita;
3. varredura de temperatura controlada;
4. varredura de frequência/tensão apenas em ambiente autorizado;
5. mesma matriz com cache quente/frio;
6. CPU versus GPU/DMA;
7. ordem física aleatória versus sequencial;
8. repetição suficiente para intervalo de confiança.

## 11. Gates de causalidade

```yaml
G0_CAPTURE: observação reproduzível
G1_LOCALIZE: endereço/coordenada rastreável
G2_CLASSIFY: flip/erasure/omission separados
G3_CORRELATE: associação com temperatura ou outro fator
G4_INTERVENE: fator alterado de forma controlada
G5_REPLICATE: repetição em outro ciclo/dispositivo
G6_CAUSAL_CLAIM: permitido somente após G0..G5
```

Até G4:

```text
thermal_cause = TOKEN_VAZIO
```

## 12. Artefatos deste bloco

```text
Mapa:
  indices/BITRAF_LOSS_VECTOR_MODEL_V1.md
  schemas/bitraf-loss-observation.schema.json
  data/claims/bitraf_loss_vector_claims.v1.jsonl

RafPolimata:
  docs/BITRAF_LOSS_VECTOR_MODEL_V1.md
  scripts/bitraf_loss_vector_index.py
  tests/test_bitraf_loss_vector_index.py
  tests/fixtures/bitraf_loss_observations.v1.jsonl
  tests/fixtures/bitraf_loss_query.v1.json

Papers:
  docs/bitraf-bit-loss-recovery-research-note.md

Clay-Maths:
  docs/analysis/mathematical_foundations/bitraf_erasure_geometry_v1.md
```

## 13. Estado

```yaml
F_ok:
  - fontes principais localizadas
  - XOR parity delimitada
  - skeleton H1/H2/M identificado
  - RS bloqueado por inconsistências
  - modelo de observação e vetor formalizado
  - protótipo stdlib testável preparado
F_gap:
  - dump real de erros
  - acesso a síndrome de hardware no Android
  - tensão por domínio
  - endereço físico confiável
  - experimentos térmicos controlados
  - ECC/FEC corrigido e validado
F_next:
  - ingerir primeira captura real sem atribuir causa
  - corrigir FEC em PR separado
  - medir taxa por classe e superfície espacial
```

FIAT LUX — o vazio não vira zero; vira coordenada de pesquisa.
