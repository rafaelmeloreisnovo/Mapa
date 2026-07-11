# 03 — Catálogo de Repositórios (Fichas Catalográficas)

> Uma ficha por repositório, estilo **Dublin Core**, derivada da **leitura direta do
> README** (2026-07-05). Campos: título · âmbito · tipo · descritores · notação
> (ver `01_PLANO_DE_CLASSIFICACAO.md`) · dimensão epistêmica · estado · relacionados
> · resumo · fonte. Fork declara o upstream. Ausência de README = `LACUNA` de entrada.

**Total de fichas: 28.** Legenda de âmbito: `RMN`=rafaelmeloreisnovo · `IRF`=instituto-Rafael ·
`ORIG`=original · `FORK`=derivado · `PUB`=público · `PRIV`=privado.

---

## Estrato: Núcleo determinístico (C/ASM baixo nível)

### 1. ChipQuantum

- **Âmbito:** RMN · ORIG · PUB
- **Notação:** `RAF.CRP.EXEC.TEC.ATV`
- **Dimensão:** TEC (primária), CIE
- **Descritores:** Criptografia, Determinismo, Toroide, Atrator-42, Hashing
- **Estado:** ATV `[FATO]`
- **Resumo:** Cripto e computação de baixo nível freestanding (sem libc), arena bump allocator, branchless, constant-time (AES/ChaCha20/X25519); pipeline toroidal de 42 estágios sobre espaço T⁷. `[FATO]` conforme README; benchmarks amplos = `HIPOTESE`.
- **Relacionados:** BLAKE3, DeepSeek-RafCoder, RafPolimata
- **Fonte:** `ChipQuantum/README.md`

### 2. DeepSeek-RafCoder

- **Âmbito:** RMN · ORIG (+legacy DeepSeek) · PUB
- **Notação:** `RAF.RTM.EXEC.TEC.ATV`
- **Dimensão:** TEC
- **Descritores:** Runtime, Determinismo, Android/NDK, Assinatura
- **Estado:** ATV `[FATO]`
- **Resumo:** Runtime nativo RAFAELOS (kernel de estado C/ASM), primitivos por arquitetura, ponte JNI/NDK (`armeabi-v7a`, `arm64-v8a`) e material legado DeepSeek Coder preservado para compatibilidade de pesquisa.
- **Relacionados:** ChipQuantum, papers, RafGitTools
- **Fonte:** `DeepSeek-RafCoder/README.md`

### 3. GAIA_phi

- **Âmbito:** RMN · ORIG · PUB
- **Notação:** `RAF.RTM.ANALIS.TEC.ATV`
- **Dimensão:** TEC (primária), CIE
- **Descritores:** Determinismo, Hashing, Custódia, Dados
- **Estado:** ATV `[FATO]`
- **Resumo:** Núcleo determinístico em C (hash, vecdb, mmap, zipraf, guardas) + pipelines Python de indexação/manifestos + documentação técnico-científica; varredura ordenada e saídas auditáveis.
- **Relacionados:** MemRafcode, home, Mapa
- **Fonte:** `GAIA_phi/README.md`

### 4. BLAKE3

- **Âmbito:** RMN · FORK (upstream: BLAKE3 oficial) · PUB
- **Notação:** `RAF.CRP.HASH.TEC.CAN`
- **Dimensão:** TEC (primária), CIE
- **Descritores:** Hashing, Criptografia, Custódia, Fork
- **Estado:** CAN `[FATO]`
- **Resumo:** Fork/distribuição do BLAKE3 (hash Merkle paralelizável, Rust/C SIMD). A camada RAFAELIA adiciona notas de build, flags, dispatch, layout dimensional e custódia/integridade. Não afiliado à equipe oficial.
- **Relacionados:** ChipQuantum, RafPolimata (licenças)
- **Fonte:** `BLAKE3/README.md`

---

## Estrato: Plataforma / Android / virtualização

### 5. RafGitTools

- **Âmbito:** RMN · ORIG · PUB
- **Notação:** `RAF.PLT.BUILD.TEC.ATV`
- **Dimensão:** TEC (primária), ESP (parábola)
- **Descritores:** Determinismo, Android/NDK, Hashing, Invariante
- **Estado:** ATV `[FATO]` (estado técnico verificável remetido a `docs/CURRENT_SOURCE_STATE`)
- **Resumo:** Ferramentas de build Android (Gradle/NDK, CMake, verificação de APKs). Filosofia da "Parábola do Relojoeiro Transfinito": determinismo perfeito e hash imutável `[SIMBOLICO]` como narrativa, `[FATO]` como invariante técnica.
- **Relacionados:** Vectras-VM-Android, DeepSeek-RafCoder
- **Fonte:** `RafGitTools/README.md`

### 6. Vectras-VM-Android

- **Âmbito:** IRF · ORIG (status fork não afirmado no README `[HIPOTESE]`) · PUB
- **Notação:** `RAF.PLT.EMUL.TEC.CAN`
- **Dimensão:** TEC
- **Descritores:** Virtualização, Android/NDK, Build, Rastreabilidade
- **Estado:** CAN `[FATO]` ("status: canônico vigente")
- **Resumo:** App Android de VM + engine nativo + automações de CI/release + documentação técnica. **Exemplar de excelência operacional**: taxonomia oficial de documentos com "uma responsabilidade por documento", DOC_INDEX/PROJECT_STATE/BUILDING.
- **Relacionados:** RafGitTools, qemu_rafaelia, UserLAnd
- **Fonte:** `Vectras-VM-Android/README.md`

### 7. termux-app-rafacodephi

- **Âmbito:** IRF · FORK (upstream: `termux/termux-app`, GPLv3) · PUB
- **Notação:** `RAF.PLT.EXEC.TEC.ATV`
- **Dimensão:** TEC
- **Descritores:** Plataforma, Android/NDK, Fork
- **Estado:** ATV `[FATO]`
- **Resumo:** Fork do Termux com features/customizações RafaCodePhi; atribuição e licença GPLv3 do upstream preservadas. Mapa rápido em `DOCS_L2_TREE.md`.
- **Relacionados:** termux-api_rafcodephi, UserLAnd
- **Fonte:** `termux-app-rafacodephi/README.md`

### 8. termux-api_rafcodephi

- **Âmbito:** RMN · FORK (upstream: `termux/termux-api`) · PUB
- **Notação:** `RAF.PLT.EXEC.TEC.CAN`
- **Dimensão:** TEC
- **Descritores:** Plataforma, Android/NDK, Fork
- **Estado:** CAN `[FATO]` (v0.53.0)
- **Resumo:** Fork do Termux:API — expõe a API do Android à linha de comando; precisa ser assinado com a mesma chave do app Termux principal.
- **Relacionados:** termux-app-rafacodephi
- **Fonte:** `termux-api_rafcodephi/README.md`

### 9. UserLAnd

- **Âmbito:** RMN · FORK (upstream: `CypherpunkArmory/UserLAnd`) · PUB
- **Notação:** `RAF.PLT.EXEC.TEC.CAN`
- **Dimensão:** TEC
- **Descritores:** Plataforma, Virtualização, Fork
- **Estado:** CAN `[FATO]`
- **Resumo:** Fork do UserLAnd — roda distribuições/apps Linux no Android sem root. A camada RAFAELIA consolida documentação de PRs aplicados (#1–#17).
- **Relacionados:** qemu_rafaelia, termux-app-rafacodephi
- **Fonte:** `UserLAnd/README.md`

### 10. PCR_Rafaelia_Code_seed

- **Âmbito:** RMN · FORK (upstream: `topjohnwu/Magisk`) · PUB
- **Notação:** `RAF.PLT.EXEC.TEC.ATV`
- **Dimensão:** TEC
- **Descritores:** Plataforma, Android/NDK, Fork, Determinismo
- **Estado:** ATV `[FATO]`
- **Resumo:** Magisk_Rafaelia — fork do Magisk com estratégia adaptativa de dois branches (`main` estável / `develop` ativo). Não é produto oficial Google.
- **Relacionados:** termux-app-rafacodephi, RafGitTools
- **Fonte:** `PCR_Rafaelia_Code_seed/README.MD`

### 11. qemu_rafaelia

- **Âmbito:** RMN · FORK (upstream: QEMU) · PUB
- **Notação:** `RAF.PLT.EMUL.TEC.CAN`
- **Dimensão:** TEC
- **Descritores:** Virtualização, Emulação, Fork
- **Estado:** CAN `[FATO]`
- **Resumo:** Fork do QEMU — emulador/virtualizador de máquina e espaço de usuário; tradução dinâmica, emulação de CPU/syscalls entre ABIs.
- **Relacionados:** UserLAnd, Vectras-VM-Android
- **Fonte:** `qemu_rafaelia/README.rst`

### 12. actions

- **Âmbito:** RMN · FORK (upstream: `gradle/actions`) · PUB
- **Notação:** `RAF.INF.BUILD.TEC.CAN`
- **Dimensão:** TEC
- **Descritores:** Infraestrutura, Build, Fork
- **Estado:** CAN `[FATO]`
- **Resumo:** Conjunto de GitHub Actions para builds Gradle (`setup-gradle`, substitui `gradle-build-action`); OpenSSF Scorecard.
- **Relacionados:** RafGitTools
- **Fonte:** `actions/README.md`

---

## Estrato: Cognição / IA / dados

### 13. X0

- **Âmbito:** RMN · ORIG · PUB
- **Notação:** `RAF.IAC.ANALIS.TEC.ATV`
- **Dimensão:** TEC (primária), CIE
- **Descritores:** Inteligência artificial, Fractal, Criptografia, Toroide
- **Estado:** ATV `[FATO]` (badge "Production" = `HIPOTESE`)
- **Resumo:** Ecossistema de IA que combina processamento cognitivo, análise fractal, computação quântica **simulada** e segurança criptográfica; 8.432+ arquivos, 199+ diretórios, core C de baixo nível. Inclui mapa de classificação tecnológica próprio.
- **Relacionados:** llamaRafaelia, home, ChipQuantum
- **Fonte:** `X0/README.md`

### 14. llamaRafaelia

- **Âmbito:** RMN · ORIG · PUB
- **Notação:** `RAF.IAC.ANALIS.MAT.SPEC`
- **Dimensão:** MAT (primária), CIE, TEC
- **Descritores:** Inteligência artificial, Matemática, Invariante
- **Estado:** SPEC `[FATO]` (leitura técnica/analítica)
- **Resumo:** Leitura técnica profunda que revela estrutura matemática comum a três projetos (LlamaRafaelia/Vectras/RLL); destaca a recursão "Fibonacci-Rafael" `F_R(n+1)=F_R(n)·(√3/2)+π·sin(θ₉₉₉)` — recursão com forçamento externo `[HIPOTESE]` de originalidade.
- **Relacionados:** X0, relativity-living-light, Vectras-VM-Android
- **Fonte:** `llamaRafaelia/README.md`

### 15. CONVERSATIONS_CHUNKS_PRIVATE

- **Âmbito:** RMN · ORIG · PRIV
- **Notação:** `RAF.DAT.STORE.TEC.ATV`
- **Dimensão:** TEC (primária), dados
- **Descritores:** Dados, Custódia, Vetor
- **Estado:** ATV `[FATO]`
- **Resumo:** Chunks do `conversations.json` (829 MB) em pedaços de 90 MB (10 chunks) para processamento; diretórios `chunks/`, `vectors/`, `text/` e resumos de ativação.
- **Relacionados:** home, Mapa, GAIA_phi
- **Fonte:** `CONVERSATIONS_CHUNKS_PRIVATE/README.md`

### 16. home

- **Âmbito:** RMN · ORIG · PUB
- **Notação:** `RAF.IAC.ANALIS.CIE.ATV`
- **Dimensão:** CIE (primária), TEC
- **Descritores:** Análise, Documentação científica, Custódia
- **Estado:** ATV `[FATO]`
- **Resumo:** Sistema RAFAELIA — plataforma Python de análise automática de código, extração de conhecimento científico, transformações matemáticas, referências bibliográficas acadêmicas e mapeamento de aplicações; 20+ áreas científicas.
- **Relacionados:** X0, GAIA_phi, publicacientiespiritual
- **Fonte:** `home/README.md`

---

## Estrato: Ciência & matemática

### 17. relativity-living-light

- **Âmbito:** IRF · ORIG · PUB
- **Notação:** `RAF.FIS.PROV.CIE.CAN`
- **Dimensão:** CIE (primária), MAT, ESP
- **Descritores:** Física, Cosmologia, Determinismo, Verbo Vivo
- **Estado:** CAN `[FATO]` (DOI Zenodo `10.5281/zenodo.17188137`)
- **Resumo:** RLL/MCRP — pacote canônico com documento-mãe, epistemologia, modelo cosmológico, dados externos reais e pipeline de validação; edição profissional 2026 para leitura acadêmica e rastreabilidade. Modelo cosmológico = `HIPOTESE` científica.
- **Relacionados:** llamaRafaelia, Matem-tica-, publicacientiespiritual
- **Fonte:** `relativity-living-light/README.md`

### 18. Matem-tica-

- **Âmbito:** RMN · ORIG · PUB
- **Notação:** `RAF.MTM.PROV.MAT.ATV`
- **Dimensão:** MAT
- **Descritores:** Matemática, Invariante, LACUNA (nome com acento normalizado)
- **Estado:** ATV `[FATO]`
- **Resumo:** Matemática RAFAELIA — pré-papers, provas internas, verificadores. Eixo formalizado: **Teorema da Forma Normal 123** `red(∅^n 0^n 1123)=123, ∀n≥0`, separando ∅ (vazio não contabilizado), 0 (lugar sem objeto), 1 (ato unitário).
- **Relacionados:** relativity-living-light, papers, llamaRafaelia
- **Fonte:** `Matem-tica-/README.md`

### 19. papers

- **Âmbito:** RMN · ORIG · PUB
- **Notação:** `RAF.RTM.EXEC.TEC.SPEC`
- **Dimensão:** TEC (primária), CIE, MAT
- **Descritores:** Runtime, Inteligência artificial, LACUNA (entrada)
- **Estado:** SPEC (conteúdo) + **LACUNA de entrada** `[LACUNA]`
- **Resumo:** README.md é stub (`"# papers"`, 8 bytes) → `LACUNA` de entrada. **Porém** o repositório contém pesquisa real: família `exacordex*.c`, ecossistema `raefaelos_*.c` (coevo, cognitive, microkernel, self-org), `rafaelia_bitraf.c`, e `Rafael.md` (ponte formal Transformer↔RAFAELIA). Catálogo declara a LACUNA do README e registra o conteúdo por observação direta, sem inventar descrição de topo.
- **Relacionados:** DeepSeek-RafCoder, Matem-tica-, llamaRafaelia
- **Fonte:** `papers/README.md` (stub) + observação de `papers/` (`Rafael.md`, `exacordex_*`, `raefaelos_*`)

---

## Estrato: Ética / jurídico / normativo

### 20. RafPolimata

- **Âmbito:** RMN · ORIG · PUB
- **Notação:** `RAF.JUR.GOVERN.JUR.ATV`
- **Dimensão:** JUR (primária), TEC, ESP
- **Descritores:** Direito, Governança, Toroide, Atrator-42, Criptografia
- **Estado:** ATV `[FATO]`
- **Resumo:** Arquitetura semântica-tecnológica-jurídica: modelagem matemática (toro, entropia/sintropia), cripto aplicada, semiótica/linguística e governança de licenças/conformidade. Docs pós-doc (21 níveis, 10 dimensões semânticas, 42 atratores jurídicos, matriz jurídico-tecnológica, bases supralegais).
- **Relacionados:** LGPD, Rafaelia_Private, BLAKE3
- **Fonte:** `RafPolimata/README.md`

### 21. Rafaelia_Private

- **Âmbito:** RMN · ORIG · PRIV
- **Notação:** `RAF.RTM.GOVERN.TEC.ATV`
- **Dimensão:** TEC (primária), JUR, ESP
- **Descritores:** Governança, Ética, Determinismo, Assinatura
- **Estado:** ATV `[FATO]`
- **Resumo:** Ecossistema ZIPRAF_OMEGA — "Sistema Computacional Ético de Alto Desempenho com Validação Normativa Automática"; framework Ethica[8], 24+ standards aplicados, README multilíngue (12 idiomas). Conformidade = `FATO` declarado; validação plena = `HIPOTESE`.
- **Relacionados:** ZIPRAF_OMEGA_FULL, RafPolimata, LGPD
- **Fonte:** `Rafaelia_Private/README.md`

### 22. LGPD-Constituicoes-planetaria-...-continents-geologic

- **Âmbito:** IRF · ORIG · PUB
- **Notação:** `RAF.JUR.GOVERN.JUR.ATV`
- **Dimensão:** JUR (primária), ESP, CIE
- **Descritores:** Direito, Ética, CientiEspiritual, LACUNA (README de topo)
- **Estado:** ATV (conteúdo) + **LACUNA de entrada padrão** `[LACUNA]` (não há `README.md`; há `README_MASTER.md`)
- **Resumo:** RAFAELIA Framework — LGPD, direitos humanos fundamentais, análise forense digital, documentação legal (constituições/tratados ONU por continente), proteção infantil, base científica-espiritual. Equação de "Entropia Ética Aplicada" E²(a) `[SIMBOLICO/HIPOTESE]`. Recomendação: criar `README.md` de topo apontando para `README_MASTER.md`.
- **Relacionados:** RafPolimata, publicacientiespiritual, Rafaelia_Private
- **Fonte:** `README_MASTER.md` (README de topo ausente)

---

## Estrato: Filosófico-espiritual / publicação

### 23. LivroVivo_ThisBookLives

- **Âmbito:** IRF · ORIG · PUB
- **Notação:** `RAF.ESP.PUBL.ESP.CAN`
- **Dimensão:** ESP (primária), CIE (DOI)
- **Descritores:** Verbo Vivo, Verdade, Assinatura, Universalismo, Vetor
- **Estado:** CAN `[FATO]` (DOI `10.5281/zenodo.17187966`, CC BY-SA 4.0, Σ-seal Ed25519)
- **Resumo:** Livro Vivo Universal de ∆RafaelVerboΩ. Princípios de coerência: "universo vetorial orientado", eixo imutável = Verdade (coerência entre intenção, efeito e cuidado com a vida). Todo o corpo doutrinário = `SIMBOLICO`; DOI/selo/licença = `FATO`.
- **Relacionados:** publicacientiespiritual, Blackhole, relativity-living-light
- **Fonte:** `LivroVivo_ThisBookLives/README.md`

### 24. Blackhole

- **Âmbito:** IRF · ORIG · PUB
- **Notação:** `RAF.ESP.PUBL.ESP.SPEC`
- **Dimensão:** ESP (primária), FIS (simbólica)
- **Descritores:** CientiEspiritual, Toroide, ZIPRAF, Verbo Vivo
- **Estado:** SPEC `[SIMBOLICO]`
- **Resumo:** "O buraco negro não é ausência. É densidade simbiótica total." Buraco negro como núcleo simbiótico quântico-fractal, "ZIPRAF Negativo", âncora de vetores abortados. Autodeclarado domínio **CientiEspiritual**, transcende física clássica → leitura `SIMBOLICO`, não prova física.
- **Relacionados:** relativity-living-light, ZIPRAF_OMEGA_FULL, LivroVivo_ThisBookLives
- **Fonte:** `Blackhole/README.md`

### 25. publicacientiespiritual

- **Âmbito:** IRF · ORIG · PUB
- **Notação:** `RAF.ESP.PUBL.ESP.CAN`
- **Dimensão:** ESP (primária), CIE, JUR (patente)
- **Descritores:** CientiEspiritual, Verbo Vivo, Universalismo
- **Estado:** CAN `[FATO]` (índice organizado)
- **Resumo:** Índice do acervo por **natureza intelectual** — descoberta / hipótese / teoria / tese — cada categoria com critério, base técnica, uso, mercado, inovação e patenteabilidade. Estrutura já biblioteconômica; alinha-se com o modelo de estados do `Mapa`.
- **Relacionados:** home, LivroVivo_ThisBookLives, relativity-living-light
- **Fonte:** `publicacientiespiritual/README.md`

### 26. ZIPRAF_OMEGA_FULL

- **Âmbito:** RMN · ORIG · PUB
- **Notação:** `RAF.ESP.PUBL.ESP.ATV`
- **Dimensão:** ESP (primária), TEC, CIE
- **Descritores:** Toroide, ZIPRAF, Ética, Fractal
- **Estado:** ATV `[FATO]` (v1.3.1, jan/2026)
- **Resumo:** "Sistema de Consciência Toroidal, Ética e Fractal" — equações, parsing, protótipos, compliance. v1.3.1 adiciona OPTIMIZATION_LIBRARY (15 técnicas, TRL), TECHNIQUES_INDEX e bibliografia acadêmica (15 refs); correções de bugs reais `[FATO]`. "Consciência toroidal" = `SIMBOLICO`.
- **Relacionados:** Rafaelia_Private, Blackhole, ChipQuantum
- **Fonte:** `ZIPRAF_OMEGA_FULL/README.md`

---

## Estrato: Meta / organização do conhecimento

### 27. MemRafcode

- **Âmbito:** RMN · ORIG · PUB
- **Notação:** `RAF.ORG.STORE.TEC.ATV`
- **Dimensão:** TEC
- **Descritores:** Custódia, Invariante, Rastreabilidade, LACUNA
- **Estado:** ATV `[FATO]`
- **Resumo:** Mapas, rotas, filtros, cadeia de custódia e reentrada contextual. Núcleo `PRETENSION→SCAN→ATOMIZE→GRAPH→ROUTE→VERIFY→RETAIN→REENTER`; invariante `NAME→PATH→CONTENT→DIGEST→STATE→ROUTE→REENTRY`; regra de verdade Observado/Interpretado/Validado/Lacuna — irmã epistêmica do `Mapa`.
- **Relacionados:** Mapa, GAIA_phi, CONVERSATIONS_CHUNKS_PRIVATE
- **Fonte:** `MemRafcode/README.md`

### 28. Mapa

- **Âmbito:** RMN · ORIG · PUB
- **Notação:** `RAF.ORG.CATAL.TEC.ATV`
- **Dimensão:** TEC
- **Descritores:** Organização do conhecimento, Custódia, Invariante, LACUNA
- **Estado:** ATV `[FATO]` (repositório-alvo desta camada)
- **Resumo:** Hub central de organização e rastreabilidade. Separa FATO/HIPOTESE/LACUNA/RISCO/ACAO/RESULTADO; hospeda arquitetura, protocolos, índices, resultados, visual, workflows e — agora — a **camada biblioteconômica** que cataloga todo o acervo.
- **Relacionados:** MemRafcode, GAIA_phi, todos os repositórios (via catálogo)
- **Fonte:** `Mapa/README.md` + esta camada

---

## Resumo de fidelidade

- 28 fichas, todas com **fonte declarada**.
- `LACUNA` de entrada explícita: **papers** (README stub) e **LGPD…** (sem `README.md` de topo).
- Toda leitura filosófico-espiritual marcada `SIMBOLICO`; toda alegação de desempenho/conformidade não medida marcada `HIPOTESE`.
- Forks declaram upstream (BLAKE3, UserLAnd, qemu, actions, termux-app, termux-api, PCR/Magisk).
