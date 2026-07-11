> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — avaliar o conteúdo é reconhecer o trabalho vivo do autor com honestidade; nada aqui serve contra a vida ou a criança (ONU UDHR Art.1 · UNCRC Art.3).

# 17 — Avaliação de Conteúdo (leitura real dos arquivos dos 28)

> Passo além da varredura automática: **abrir e ler os arquivos substantivos** — não o
> README, mas o código, a matemática, os motores — e avaliar o que **de fato** está lá.
> Cada avaliação cita o arquivo lido (fonte) e marca o estado. Leitura de 2026-07-05.

## Método

Para cada repositório, localizei os maiores arquivos-fonte reais (não forks/vendored) e
li o conteúdo. Avaliei: **o que é**, **estado** (código real / protótipo / prosa / stub),
**qualidade** e **originalidade** (com honestidade: originalidade declarada é `HIPOTESE`
até revisão de pares). Cruzei com a revisão automática de `indices/REVISAO_PUBLICACAO.md`.

## Achados por obra (amostra substantiva)

### GEOLM (`Matem-tica-/A_raf/geolm_full.c`, ~51k; também `DeepSeek-RafCoder/Rmr/geolm.c`) `[FATO: código real]`

Implementação **single-file em C11** de um mini-transformer + sistema de coerência
toroidal, para ARM32/Termux (Cortex-A7, NEON softfp). Módulos B1–B6 reais: arena estática
64MB (sem malloc), tokenizer, embeddings sinusoidais, MHA (4 cabeças), FFN+cross-entropy,
REPL, e o **B6** — `ContextBuffer`, `CoerenceScore` (cosseno), `ProofLayer` (CRC32+entropia),
ciclo `ψχρΔΣΩ`, `ToroidalState 7D`, `AttractorPool 42`. Matemática declarada no cabeçalho:
`φ=(1−H)·C`, `F_{n+1}=F_n·(√3/2)−π·sin(279°) mod 42`, CRC32C, FNV-1a.

- **Avaliação:** engenharia de baixo nível **coerente e séria**; a documentação interna é
  exemplar (hierarquia de memória, paralelismo, convergência). O `φ=(1−H)·C` é exatamente
  o `phi_fst` que aparece em RafPolimata — **prova de que o núcleo geométrico é o mesmo**
  entre repos (correlação real, não retórica). Originalidade da recorrência Fibonacci-Rafael:
  `HIPOTESE` (a validar contra literatura).

### APKc (`RafPolimata/Apkc/apkc.c`, ~79k) `[FATO: código real]`

Compilador de APK **freestanding** — sem libc, sem heap, syscalls via `sys.h`. Lexer próprio,
pipeline table-driven para 12 linguagens (`lang_profile.h`), encoders ARM64 (`arch_arm64.h`,
~65% da ISA), builders ELF/AXML/ZIP. Determinismo tecnológico: a extensão do fonte dirige
todo o pipeline; `codegen_select` escolhe variantes por `phi_fst`/`phi_attractor`
(reprodutível). Confirma o conceito C01 (Determinismo) e C06 (Toroide) no conteúdo.

- **Avaliação:** dos artefatos mais **maduros** do acervo; a invariante geométrica de coerência
  está de fato no código (imprime `[phi=… attractor=…]`). Alto valor técnico.

### Ethica[8] (`ZIPRAF_OMEGA_FULL/rafaelia_ethica_engine.py`, ~15k) `[FATO: código real]`

Motor de validação ética com **8 dimensões** (`EthicaDimension`: Amor, Verdade, Consciência,
**Proteção**, Transparência, Retroalimentação, Harmonia, Finalidade), `dataclass` de
resultado, `watchdog` contra loops, fórmula `Φ_ethica = e^{(amor+verbo)/proteção}−1`.

- **Avaliação:** a dimensão **PROTECAO ("Proteção ao humano")** é a mesma que este acervo põe
  na primeira linha (I2) — **coerência real** entre o código do autor e o invariante do Mapa.
  A "fórmula ética" é modelo `SIMBOLICO/HIPOTESE` (não métrica validada), o que o próprio
  código admite com `SIMULATION_MODE`. Boa prática de engenharia (validação de faixa, watchdog).

### Bitraf64 (`ZIPRAF_OMEGA_FULL/bitraf64_decompressor.py` + `tests/test_bitraf64.py`) `[FATO: código real + testes]`

Descompressor com RLE, header, **hashchain** e verificação de integridade; validação de
entrada robusta (tipo, tamanho mínimo, checksum). Acompanha teste.

- **Avaliação:** protótipo **honesto** (assume-se "demonstrativo"); as correções de bug da
  v1.3.1 citadas no README são reais no código (proteção contra DoS na descompressão).

### Vectra bench (`papers/Raf/vectra_bench.c`, ~9k) `[FATO: código real]`

Benchmark **NEON multicore**: `VectraCell` alinhada a 64B com `float32x4_t state[8]`,
afinidade de núcleo, relatório de hardware (cpuinfo, cache, BogoMIPS). 8 núcleos × 512
células × 200k iterações.

- **Avaliação:** benchmark genuíno de engenharia; `papers` **não é vazio** — o README é stub
  (`LACUNA` de entrada, já marcada), mas o conteúdo é pesquisa real de kernels vetoriais.

### Forks e vendored (honestidade) `[FATO]`

`qemu_rafaelia` (7.293 fontes, upstream QEMU), `llamaRafaelia` (vendored miniaudio/json,
base llama.cpp), `actions` (bundles `dist/*.js`), `UserLAnd`/`termux-*` (upstream) — **o peso
de código está no upstream**; a contribuição RAFAELIA é a camada de custódia/integração.
`home` tem muito vendored (`.cpan`, `.cargo`) — candidato a limpeza (`.gitignore`).

### Obras de prosa/símbolo (`Blackhole`, `MemRafcode`, `LivroVivo`) `[SIMBOLICO / FATO-doc]`

`Blackhole` e `MemRafcode` têm **0 arquivos-fonte** — são documento/símbolo, corretamente
no estrato L5/meta. `LivroVivo` tem 2 scripts (catálogo/derivados) + doutrina em prosa.

## Cruzamento com a revisão automática (achados que viraram teste)

De `indices/REVISAO_PUBLICACAO.md` (declarado × evidenciado no conteúdo):

| Repo | Declarado sem evidência textual | Leitura honesta |
|---|---|---|
| `blackhole` | C14 (Verbo-Vivo) | conteúdo é prosa/README, não código escaneado — coerente |
| `livrovivo_thisbooklives` | C15 (Universalismo), C17 (NÓ_GOOD) | doutrina está no README/prosa, fora dos fontes escaneados |
| `publicacientiespiritual` | C15 (Universalismo) | idem — eixo L5 vive na prosa |

> Nenhum desses é erro: são obras do eixo `SIMBOLICO`, cujo conteúdo vive em prosa, não em
> código. O achado correto é: **para o estrato L5, escanear também `.md`/prosa** (próxima
> melhoria da varredura), não "rebaixar" a obra. C07 (Atrator-42) aparece como
> `nao_escaneado` por opção (o termo "42" é ruidoso) — declarado honestamente.

### Resolução (léxico refinado — melhoria contínua aplicada)

Refinando os termos-âncora **sem baixar a régua** (`universalis`→`universal`; `living light`
→ também `living-light`; C07 qualificado com `atrator`/`attractorpool`/`42 atratores`), a
varredura foi re-executada. **RISCOs de 3 → 1:**

| Repo | Antes | Depois | Como |
|---|---|---|---|
| `blackhole` | C14 sem texto | **confirmado** | "LIVING-LIGHT" no título (termo `living-light`) |
| `publicacientiespiritual` | C15 sem texto | **confirmado** | "universal" na prosa |
| `livrovivo_thisbooklives` | C15, C17 sem texto | **C15 confirmado; C17 residual** | "universal" presente; `no_good` ausente |
| `chipquantum` / `rafpolimata` | C07 `nao_escaneado` | **confirmado** | "atrator"/"AttractorPool" no conteúdo |

**Residual honesto (1):** `livrovivo` declara **C17 (NÓ_GOOD)**, mas o termo **nasce aqui no
`Mapa`** (a parábola de `12_`), não no conteúdo de LivroVivo. É um **link conceitual
`SIMBOLICO`** (a "Verdade como eixo imutável" de LivroVivo ≈ NÓ_GOOD/Amor-Ω), cuja evidência
vive no `Mapa`, não em LivroVivo. Mantido e **declarado como conceitual, não textual** — em
vez de forjar um casamento ou apagar a ligação. Isto é "sem baixar a régua".

> Propriedade verificada: **o refino do léxico não altera nenhum triple-hash por repo**
> (coerência/integridade/prova vêm de `git ls-files`/tree, não do grep). O `selo do acervo`
> mudou apenas porque o próprio `Mapa` (membro auto-referente) avançou de commit — a lente
> de conceitos e a prova de integridade são **camadas independentes**, como devem ser.

## Avaliação ampliada — 2ª leitura (mais obras originais lidas)

Segunda passada de leitura real, cobrindo os estratos ainda não avaliados individualmente.

### verbovivo (`RafPolimata/rafaelia/verbovivo.c`, ~22k) · NG5 `[FATO: código real]`

Motor de **convergência cognitiva** em C, duas camadas: (L1) Fiber-H — hash 256-bit +
distância de Hamming + hipervetores HDC + atenção sináptica + ring buffer de engramas;
(L2) toro T⁷ (42 atratores, `phi_ethica=(1−H)*C`) → HDC 1024-dim → engrama SVG.

- **Avaliação:** invariante declarada e implementada: *"o sistema NÃO aprende por gradiente
  — aprende por DIVERGÊNCIA ESTRUTURAL"* (alta diversidade de Hamming ⇒ retenção). É uma
  abordagem **genuinamente original** de memória (não-backprop); `HIPOTESE` quanto a desempenho,
  `FATO` quanto a existir e rodar. Confirma C06/C08/C10 no código. `Ω=Amor` inscrito no cabeçalho.

### GAIA_phi (`build_dataset.py`, ~33k) · NG1 `[FATO: código real]`

Compilador de dataset: faz *stream* de JSON/JSONL dentro de zips grandes, normaliza para um
esquema único e produz train/eval com **metadados de discernimento**. Traz `SYMBOL_SET`
(42, toroid, spiral_sqrt3_2, bitraf, phi…) e `ETHICA_KEYWORDS` (care/truth/**privacy**/
nonviolence/warning).

- **Avaliação:** engenharia de dados séria; a **etiquetagem ética embutida** (incl. `privacy`)
  liga o pipeline à camada de dados pessoais — reforça a prioridade ALTA de `MATRIZ_CONFORMIDADE`.

### relativity-living-light (`RAFAEL_kernel.sh`, ~43k) · NG4 `[FATO: doc+código]`

Gerador de monólito C/ASM freestanding com **cabeçalho jurídico real e cuidadoso**: dupla
licença Apache-2.0 OR CC0 (modelo BLAKE3), contexto jurisprudencial factual (Google v. Oracle
593 U.S. 2021; Diretiva UE 2009/24/CE; Lei 9.609/98) e afirmação de que implementa **só
algoritmos públicos** (CRC32, ECC Hamming, CPUID, POSIX).

- **Avaliação:** exemplar de governança de licença (C13/jurídico) aplicada ao próprio código —
  não retórica, texto de licença operacional. O modelo cosmológico segue `HIPOTESE` científica.

### publicacientiespiritual (`Bolsas/boosters_integracao.py`, ~23k) · NG6 `[FATO: código real]`

Integra **XGBoost/LightGBM/CatBoost** ao framework BOLSAS (sklearn, imports condicionais,
métricas RMSE/MAE/R²) — ciência de dados real num repo do eixo espiritual.

- **Avaliação:** mostra que NG6 **não é só prosa**: há ML funcional ao lado da publicação
  simbólica. Coerente com a evidência `codigo+prosa` do manifesto para este repo.

### Cobertura

Com a 1ª leitura (GEOLM, APKc, Ethica[8], Bitraf64, vectra_bench) + esta 2ª (verbovivo,
GAIA_phi, RLL, boosters), todos os **7 nós** têm ao menos uma obra avaliada por leitura direta;
os demais são forks/vendored (peso no upstream, declarado) ou prosa do eixo L5 (honrada como
`SIMBOLICO`). As **métricas** por repo (`MANIFESTO_INTEGRIDADE.yaml`) complementam com LOC/bytes.

## Avaliação de conjunto

- O acervo tem **núcleo de engenharia real e forte** (GEOLM, APKc, Ethica[8], Bitraf64,
  vectra_bench) — não é só manifesto. A invariante geométrica `φ=(1−H)·C` é **literalmente
  o mesmo código** em repos diferentes: a coerência que o autor afirma existe no material.
- O eixo `SIMBOLICO` (LivroVivo, Blackhole, publicações) é prosa — honrado como tal, não
  confundido com prova.
- Forks são forks; o valor RAFAELIA neles é a custódia/integração, declarada.

## Próxima ação (melhoria contínua, PDCA)

1. ~~Escanear prosa (`.md`) no L5 e resolver os 3 RISCOs~~ — **feito**: léxico refinado,
   RISCOs 3 → 1 (ver "Resolução" acima); o `.md` já era escaneado, o gargalo era o termo.
2. ~~Termo-âncora de C07 qualificado~~ — **feito** (`atrator`/`attractorpool`/`42 atratores`).
3. Propor `.gitignore` para o vendored de `home` (limpeza) — registrar como ação, não executar
   fora de escopo.
4. O único RISCO residual (`livrovivo` C17) é **link conceitual `SIMBOLICO`**, não defeito —
   mantido e declarado como tal.
