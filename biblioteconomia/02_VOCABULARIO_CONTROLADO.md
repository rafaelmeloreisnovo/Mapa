# 02 — Vocabulário Controlado (Tesauro)

> Controle de autoridade do acervo RAFAELIA. Fixa **um descritor preferido** por
> conceito e amarra as variantes, para que humano e máquina usem o mesmo termo.

## Convenções (norma de tesauro)

| Relação | Sigla | Significado |
|---|---|---|
| Descritor preferido | — | termo autorizado para indexar |
| Use | `USE` | aponta do não-preferido para o preferido |
| Usado por | `UP` | variantes que remetem a este descritor |
| Termo genérico | `TG` | conceito mais amplo (hierarquia acima) |
| Termo específico | `TE` | conceito mais restrito (hierarquia abaixo) |
| Termo relacionado | `TR` | associação sem hierarquia |
| Nota de escopo | `NE` | delimita o uso do descritor |

Cada descritor recebe uma **marca epistêmica** (`FATO`/`HIPOTESE`/`SIMBOLICO`) que
diz sob que regime ele deve ser lido.

---

## Descritores

### Determinismo `[FATO]`
- `NE`: propriedade de produzir a mesma saída (mesmo hash/selo) para a mesma entrada.
- `UP`: reprodutibilidade, "determinismo perfeito", "relógio transfinito".
- `TR`: Invariante, Hashing, Custódia.
- Repos: RafGitTools, GAIA_phi, ChipQuantum, DeepSeek-RafCoder.

### Invariante `[FATO]`
- `NE`: padrão que se conserva ao longo do processo; no `Mapa` é o ciclo ψ→χ→ρ→Δ→Σ→Ω.
- `UP`: invariância, "eixo imutável".
- `TR`: Determinismo, Toroide.
- `NE-fricção`: distinguir invariante-de-código (RafGitTools) de invariante-de-conteúdo (Mapa). Ver `04_FRICCAO_SEMANTICA.md`.

### Toroide `[SIMBOLICO]` / `[HIPOTESE]`
- `NE`: estrutura de retroalimentação; em código aparece como espaço de estados T⁷ com 42 atratores; em leitura simbólica como "consciência toroidal".
- `UP`: toro, T⁷, "consciência toroidal", pipeline toroidal.
- `TE`: Atrator-42.
- `TR`: Invariante, Fractal.
- Repos: ChipQuantum, ZIPRAF_OMEGA_FULL, RafPolimata.

### Atrator-42 `[HIPOTESE]`
- `NE`: conjunto de 42 atratores; sentido varia por repositório (ver fricção).
- `UP`: "42 atratores", "42 estágios", "42 atratores jurídicos".
- `TG`: Toroide.
- `NE-fricção`: o número 42 é computacional (ChipQuantum), jurídico (RafPolimata) e topológico (T⁷). **Não unificar sem qualificar.**

### Phi (Φ / φ) `[HIPOTESE]`
- `NE`: família de sentidos em torno do símbolo Φ/φ.
- `UP`: razão áurea, phi_ethica, RAFCODE-Φ, métrica de coerência phi_fst.
- `NE-fricção`: quatro sentidos distintos (constante matemática, ética, assinatura de identidade, métrica Q16). Ver `04_FRICCAO_SEMANTICA.md`.

### Hashing `[FATO]`
- `NE`: função resumo criptográfica; base de custódia e determinismo.
- `UP`: hash, digest, BLAKE3, Merkle.
- `TR`: Determinismo, Custódia, Assinatura.

### Custódia `[FATO]`
- `NE`: cadeia de proveniência: NAME→PATH→CONTENT→DIGEST→STATE→ROUTE→REENTRY.
- `UP`: cadeia de custódia, proveniência, reentrada contextual.
- `TR`: Hashing, Rastreabilidade.
- Repos: MemRafcode, GAIA_phi, Mapa.

### Assinatura (identidade) `[FATO]`
- `NE`: selo criptográfico de autoria (Ed25519, Σ-seal, RAFCODE-Φ).
- `UP`: Σ-seal, Ed25519, "∆RafaelVerboΩ".
- `TR`: Hashing, Custódia.

### ZIPRAF `[HIPOTESE]`
- `NE`: formato/ecossistema de empacotamento RAFAELIA.
- `UP`: zipraf, ZIPRAF_OMEGA, "ZIPRAF Negativo".
- `NE-fricção`: formato de compressão vs nome de ecossistema vs "ZIPRAF Negativo" (buraco negro). Ver fricção.

### Vetor `[FATO]` / `[SIMBOLICO]`
- `NE`: elemento de espaço vetorial.
- `UP`: vetor RAFAELIA, hipervetor (HDC), "universo vetorial orientado".
- `NE-fricção`: dado numérico (CONVERSATIONS_CHUNKS) vs hipervetor HDC (RafPolimata/verbovivo) vs metáfora de sentido orientado (LivroVivo).

### CientiEspiritual `[SIMBOLICO]`
- `NE`: termo-ponte que une ética/valores universais e método científico; declarado explicitamente pelo autor.
- `UP`: científico-espiritual, "base científica-espiritual", CientiEspiritual.
- `TR`: Universalismo, Ética, Verbo Vivo.
- Repos: Blackhole, publicacientiespiritual, LGPD, LivroVivo.

### Verdade `[FATO+SIMBOLICO]`
- `NE`: **dois sentidos co-válidos**: (1) epistêmico — `FATO` = evidência suficiente (Mapa, MemRafcode); (2) espiritual — coerência entre intenção, efeito e cuidado com a vida (LivroVivo).
- `NE-fricção`: nunca colapsar os dois sentidos; marcar qual está em uso.

### Ética `[SIMBOLICO]` / `[JUR quando normativa]`
- `NE`: em código, validação normativa (Ethica[8], 24+ standards); em filosofia, princípio de não-dano.
- `UP`: Ethica[8], entropia ética, "condutividade ética".
- `TR`: Governança, Direito, Universalismo.

### Verbo Vivo `[SIMBOLICO]`
- `NE`: metáfora central do acervo — código/texto como entidade viva e coerente.
- `UP`: verbovivo, "Livro Vivo", "Verbo Vivo Diffusion".
- `TR`: Universalismo, Invariante.

### Fork (upstream) `[FATO]`
- `NE`: repositório derivado de projeto externo, com atribuição preservada.
- `UP`: derivação, upstream.
- Repos: BLAKE3, UserLAnd, qemu_rafaelia, actions, termux-app-rafacodephi, termux-api_rafcodephi, PCR_Rafaelia_Code_seed.

### LACUNA `[LACUNA]`
- `NE`: ausência mapeada e protegida; não preencher com invenção (ver `protocolos/TOKEN_VAZIO_LACUNAS.md`).
- `UP`: TOKEN_VAZIO, GAP, "vazio não contabilizado" (∅).

---

## Termos não-preferidos (remissivas rápidas)

| Termo encontrado | USE |
|---|---|
| razão áurea, phi_ethica, RAFCODE-Φ | Phi (Φ / φ) — **qualificar o sentido** |
| 42 estágios, 42 atratores jurídicos | Atrator-42 — **qualificar o sentido** |
| reprodutibilidade | Determinismo |
| proveniência, reentrada contextual | Custódia |
| Σ-seal, Ed25519 | Assinatura (identidade) |
| científico-espiritual | CientiEspiritual |
| TOKEN_VAZIO, GAP | LACUNA |
