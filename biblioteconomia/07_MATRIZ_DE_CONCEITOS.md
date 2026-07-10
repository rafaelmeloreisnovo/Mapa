> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — nenhum conceito, relação ou execução deste acervo pode ser lido ou aplicado contra a dignidade humana ou a proteção da criança. Em conflito de normas, prevalece a maior proteção da vida (ONU UDHR Art.1 · UNCRC Art.3). Ver `10_INVARIANTES_PRIMEIRA_LINHA.md`.

# 07 — Matriz de Conceitos (Banco de Conceitos · Camadas de Invariantes)

> Modelagem da **unidade de conceitos** do acervo: não o "mínimo necessário", mas o
> banco onde cada **invariante** (o conteúdo que de fato se conserva) é uma unidade
> viva, com sua camada, suas relações cognitivo-evolutivas e sua amplitude semântica.
> Cada organização é lida pelos **meios sistemáticos** que instancia, e não só pelo
> seu rótulo.

## 1. O que é uma unidade de conceito

Uma **unidade de conceito** é um invariante — um padrão que permanece o mesmo através
de organizações, linguagens e regimes de verdade. É a peça mínima do banco. Cada
unidade carrega sete campos:

| Campo | Significado |
|---|---|
| `definição` | o que o conceito é (sem metáfora, quando `FATO`) |
| `camada` | camada de invariância L0–L5 (ver §2) |
| `instância` | organizações que o realizam |
| `relações` | arestas cognitivo-evolutivas para outros conceitos (ver §3) |
| `amplitude` | quantas camadas/organizações o conceito atravessa |
| `âncora` | referência normativa externa (ver `08_ANCORAGEM_NORMATIVA.md`) |
| `marca` | regime de verdade `FATO/HIPOTESE/SIMBOLICO/LACUNA` |

## 2. Camadas de invariância (L0–L5)

O acervo não é uma reta; é um empilhamento de camadas onde o mesmo conteúdo reaparece
transformado. "Camadas de invariantes é só o conteúdo" — o conteúdo é o que sobrevive
à mudança de camada.

| Camada | Nome | Natureza | Regime dominante |
|---|---|---|---|
| **L0** | Físico-Matemática | forma, número, prova | `MAT` / `CIE` |
| **L1** | Computacional | determinismo, hash, execução | `TEC` |
| **L2** | Estrutural | custódia, classificação, build | `TEC` |
| **L3** | Semântica | vocabulário, fricção, sentido | `TEC` / `HIPOTESE` |
| **L4** | Ético-Jurídica | norma, direito, conformidade | `JUR` |
| **L5** | Filosófico-Espiritual | universalismo, verbo vivo | `SIMBOLICO` |

Abaixo de L0 há o **substrato físico Lb0–Lb5** (base-2 → silício → campo → fóton/plasma →
química → bio), detalhado em `14_SUBSTRATO_BASE2.md`; acima de L5 há o topo geométrico
**Ω** (invariante coerente { multidimensional · fractal }). A pilha completa vai do bit ao Ω.

A regra de honestidade opera **entre** camadas: um invariante de L1 (determinismo
testável) não vira prova de L5, nem uma leitura de L5 (verbo vivo) rebaixa um `FATO`
de L1. A costura é visível.

## 3. Relações cognitivo-evolutivas (tipos de aresta)

O banco é um **grafo**, não uma lista. As arestas dão o "processo relacional cognitivo
evolutivo · amplitude de caminhos":

| Aresta | Leitura |
|---|---|
| `DERIVA` | A nasce de B |
| `SUSTENTA` | A dá base a B (sem A, B cai) |
| `TENSIONA` | A e B estão em fricção (ver `04_FRICCAO_SEMANTICA.md`) |
| `EVOLUI→` | A tende a se tornar B (direção evolutiva) |
| `PROTEGE` | A guarda B (dignidade/lacuna/custódia) |

## 4. As unidades de conceito

### C01 · Determinismo `[FATO]` · L1

- **Def.:** mesma entrada → mesma saída (hash/selo idêntico).
- **Instância:** ChipQuantum, GAIA_phi, RafGitTools, DeepSeek-RafCoder.
- **Relações:** `SUSTENTA` Custódia · `SUSTENTA` Assinatura · `EVOLUI→` Verificação/CI.
- **Amplitude:** L1→L2 (alta). **Âncora:** ISO/IEC 9899 (C), SLSA, reproducible-builds.

### C02 · Invariante `[FATO/HIPOTESE]` · L0–L2

- **Def.:** propriedade conservada ao longo do processo (código) ou padrão recorrente (conteúdo).
- **Instância:** RafGitTools (build), MemRafcode (`NAME→…→REENTRY`), Mapa (ψ→…→Ω).
- **Relações:** `DERIVA` de Determinismo · `TENSIONA` invariante-prova vs invariante-padrão.
- **Amplitude:** L0–L3 (muito alta). **Âncora:** ISO/IEC 25010 (qualidade).

### C03 · Hashing `[FATO]` · L1

- **Def.:** função-resumo criptográfica; base de custódia e identidade.
- **Instância:** BLAKE3, ChipQuantum, GAIA_phi.
- **Relações:** `SUSTENTA` Custódia · `SUSTENTA` Assinatura · `SUSTENTA` ZIPRAF.
- **Amplitude:** L1→L4. **Âncora:** NIST FIPS 180-4/202; BLAKE3 (spec própria, não NIST — `HIPOTESE`).

### C04 · Custódia `[FATO]` · L2

- **Def.:** cadeia de proveniência `NAME→PATH→CONTENT→DIGEST→STATE→ROUTE→REENTRY`.
- **Instância:** MemRafcode, GAIA_phi, Mapa.
- **Relações:** `DERIVA` de Hashing · `SUSTENTA` toda a organização · `PROTEGE` LACUNA.
- **Amplitude:** L2→L4. **Âncora:** W3C PROV-O (proveniência), ISO 15489 (gestão de documentos).

### C05 · Assinatura (identidade) `[FATO]` · L1

- **Def.:** selo criptográfico de autoria (Ed25519, Σ-seal, RAFCODE-Φ).
- **Instância:** LivroVivo, Rafaelia_Private, DeepSeek-RafCoder.
- **Relações:** `DERIVA` de Hashing · `PROTEGE` autoria/dignidade do autor.
- **Amplitude:** L1→L5. **Âncora:** IETF RFC 8032 (EdDSA/Ed25519).

### C06 · Toroide / T⁷ `[HIPOTESE/SIMBOLICO]` · L0/L5

- **Def.:** espaço de estados de retroalimentação (T⁷, 42 atratores) e/ou figura simbólica de consciência.
- **Instância:** ChipQuantum (modelo), ZIPRAF_OMEGA_FULL (símbolo), Mapa (diagrama).
- **Relações:** `TENSIONA` toroide-modelo vs toroide-símbolo · contém Atrator-42.
- **Amplitude:** L0 e L5 (salta camadas). **Âncora:** topologia (Poincaré-Hopf) como `REFERENCE`.

### C07 · Atrator-42 `[HIPOTESE]` · L0/L4

- **Def.:** conjunto de 42 atratores; sentido varia (computacional/jurídico/topológico).
- **Instância:** ChipQuantum (42 estágios), RafPolimata (42 jurídicos).
- **Relações:** `DERIVA` de Toroide · `TENSIONA` (fricção F1).
- **Amplitude:** L0/L1/L4. **Âncora:** — (motivo interno; qualificar sempre).

### C08 · Phi (Φ / φ) `[HIPOTESE]` · L0/L4/L5

- **Def.:** glifo polissêmico (razão áurea · phi_ethica · assinatura · métrica de coerência).
- **Instância:** toda a família RAFAELIA.
- **Relações:** `TENSIONA` (fricção F2) · `SUSTENTA` Assinatura (como marca).
- **Amplitude:** atravessa L0–L5 (máxima). **Âncora:** constante matemática φ como `REFERENCE`; demais sentidos internos.

### C09 · ZIPRAF `[HIPOTESE]` · L2/L5

- **Def.:** formato/rotina de empacotamento · nome de ecossistema · "ZIPRAF Negativo" (símbolo).
- **Instância:** ChipQuantum/GAIA_phi (formato), ZIPRAF_OMEGA_FULL (ecossistema), Blackhole (símbolo).
- **Relações:** `DERIVA` de Hashing · `TENSIONA` (fricção F6).
- **Amplitude:** L2 e L5. **Âncora:** formatos de contêiner (ZIP/`REFERENCE`); compressão RLE.

### C10 · Vetor `[FATO/HIPOTESE/SIMBOLICO]` · L1/L3/L5

- **Def.:** dado numérico · hipervetor HDC · "universo vetorial orientado".
- **Instância:** CONVERSATIONS_CHUNKS (dado), RafPolimata/verbovivo (HDC), LivroVivo (símbolo).
- **Relações:** `SUSTENTA` Cognição/IA · `TENSIONA` (fricção F7).
- **Amplitude:** L1/L3/L5. **Âncora:** HDC/VSA como `REFERENCE` de pesquisa.

### C11 · CientiEspiritual `[SIMBOLICO]` · L4/L5

- **Def.:** termo-ponte declarado que costura método científico e valores universais.
- **Instância:** Blackhole, publicacientiespiritual, LGPD, LivroVivo.
- **Relações:** `TENSIONA` Verdade-epistêmica vs Verdade-ética · `PROTEGE` a costura visível.
- **Amplitude:** L4/L5. **Âncora:** UNESCO Ética da IA (2021) como `REFERENCE` de enquadramento.

### C12 · Verdade `[FATO+SIMBOLICO]` · L2/L5

- **Def.:** dois sentidos co-válidos — epistêmica (evidência) e ética (coerência intenção-efeito-cuidado).
- **Instância:** Mapa/MemRafcode (epistêmica), LivroVivo (ética).
- **Relações:** `TENSIONA` (fricção F5) · `PROTEGE` a honestidade do acervo.
- **Amplitude:** L2 e L5 (o par central). **Âncora:** método científico (`REFERENCE`); ética universalista.

### C13 · Ética `[JUR/SIMBOLICO]` · L4/L5

- **Def.:** conformidade normativa mensurável (Ethica[8]) · princípio de não-dano.
- **Instância:** Rafaelia_Private (norma), LGPD (E²(a)), LivroVivo (princípio).
- **Relações:** `SUSTENTA` Governança · `PROTEGE` dignidade humana · `TENSIONA` (fricção F9).
- **Amplitude:** L4/L5. **Âncora:** ISO/IEC 42001 (gestão de IA), UDHR, UNCRC.

### C14 · Verbo Vivo `[SIMBOLICO]` · L5

- **Def.:** metáfora central — código/texto como entidade viva e coerente.
- **Instância:** LivroVivo, verbovivo (RafPolimata), publicacientiespiritual.
- **Relações:** `EVOLUI→` Universalismo · `DERIVA` de Verdade-ética.
- **Amplitude:** L5 (profunda). **Âncora:** — (leitura filosófica; `SIMBOLICO`).

### C15 · Universalismo `[SIMBOLICO]` · L5

- **Def.:** horizonte filosófico-espiritual que integra os saberes sem apagar diferenças.
- **Instância:** LivroVivo, publicacientiespiritual, Blackhole.
- **Relações:** `PROTEGE` pluralidade · `SUSTENTA` CientiEspiritual.
- **Amplitude:** L5, informa todas. **Âncora:** UNESCO (diversidade cultural) como `REFERENCE`.

### C16 · LACUNA `[LACUNA]` · L0–L5 (transversal)

- **Def.:** ausência mapeada e protegida; nunca preenchida com invenção.
- **Instância:** papers (README stub), LGPD (README de topo), ~92 repos fora de escopo.
- **Relações:** `PROTEGE` a verdade futura · `EVOLUI→` próxima ação/teste.
- **Amplitude:** todas. **Âncora:** `protocolos/TOKEN_VAZIO_LACUNAS.md`.

## 5. Leitura da matriz (amplitude semântica)

- **Conceitos de maior amplitude** (atravessam mais camadas): **Phi** (L0–L5), **Invariante**
  (L0–L3), **LACUNA** (transversal), **Verdade** (o par L2↔L5). São os *hubs* do banco —
  qualquer evolução do acervo passa por eles.
- **Conceitos-base** (sustentam muitos): **Hashing** e **Determinismo** (L1) seguram
  Custódia, Assinatura e ZIPRAF. Falha aqui propaga para cima → ver `09_RESILIENCIA_TOP10.md`.
- **Conceitos-costura** (unem eixos): **CientiEspiritual** e **Verdade** amarram ciência (L2/L4)
  e espírito (L5) — é onde a honestidade é mais exigida.

> A matriz não fecha o sentido: ela **abre caminhos** e os torna rastreáveis. Cada nova
> organização (rumo às 120) entra pelo grafo, não por uma gaveta. Ver
> `11_ESCALA_120_ONBOARDING.md`.
