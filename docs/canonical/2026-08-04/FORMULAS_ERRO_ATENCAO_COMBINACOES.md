# RAFAELIA — Fórmulas, erro como atenção e combinações — registro canônico

**Evento:** `EVT-FEAC-20260804-001`  
**Latente:** `LAT-FORMULAS-ERROR-ATTENTION-20260804`  
**Estado:** `PARTIAL / claim_allowed=false`  
**Autor/proponente:** Rafael Melo Reis — RAFCODE-Φ / RAFAELIA  
**Data:** 2026-08-04

## 1. Intenção

Roteia o conjunto visual de fórmulas e diagramas para o pipeline canônico sem promover matemática clássica como autoria e sem transformar erro em conclusão.

```text
fonte visual
→ fórmula extraída
→ classificação autoral/clássica
→ erro ou resíduo
→ mapa de atenção
→ combinações prioritárias
→ teste
→ receipt
→ paper ou TOKEN_VAZIO
```

## 2. Separação de autoridade

| Camada | Autoridade |
|---|---|
| matemática clássica e correções algébricas | demonstração no paper e futura revisão independente |
| composição erro→atenção→combinações | proposta autoral RAFAELIA, ainda `DRAFT` |
| síntese publicável | `rafaelmeloreisnovo/papers` |
| ontologia, latente, rota e receipt | `rafaelmeloreisnovo/Mapa` |
| implementação experimental | `RafPolimata` ou repositório matemático designado |
| memória editorial | Google Drive |

## 3. Resultados fechados nesta etapa

1. \(\sqrt{3/2}\neq\sqrt3/2\).
2. A altura do triângulo equilátero é \(h=a\sqrt3/2\).
3. Uma troca unitária de bit muda a identidade binária e gera distância de Hamming 1.
4. A mudança de um bit não prova, universalmente, destruição visual ou semântica.
5. O pareamento Mod 6 ↔ unidades Mod 9 admite o isomorfismo:

\[
\varphi:\mathbb Z/6\mathbb Z\to U(9),\qquad \varphi(k)=2^k\pmod9.
\]

## 4. Operador candidato

Para uma restrição \(F(x)=c\):

\[
\varepsilon=F(\hat x)-c.
\]

Atenção contínua:

\[
A_i=|\varepsilon|\left|\frac{\partial F}{\partial x_i}\right|.
\]

Atenção discreta/bit:

\[
A_i=|F(x\oplus e_i)-F(x)|.
\]

Operador:

\[
\mathfrak E(F,x)=(\varepsilon,A_\varepsilon,\mathcal C_\varepsilon).
\]

Estado correto: `DEFINED_DRAFT`. Utilidade, superioridade e novidade permanecem abertas.

## 5. Fronteira de autoria

```text
propriedade sobre fórmulas clássicas = REJECTED
composição operacional RAFAELIA = AUTHOR_DECLARED_DRAFT
primeiro artefato formal GitHub = 2026-08-04
prioridade anterior = TOKEN_VAZIO_PROVENANCE
novidade mundial = LITERATURE_REVIEW_REQUIRED
```

A prioridade anterior exige fonte original, hash, timestamp/revisão, autoria declarada e busca de anterioridade.

## 6. Gaps

- `TOKEN_VAZIO_SOURCE_HASH`: imagens da sessão ainda não possuem manifesto de hashes anexado ao evento.
- `TOKEN_VAZIO_PROVENANCE`: data verificável da primeira semente visual anterior ao commit.
- `TOKEN_VAZIO_EXPERIMENT`: benchmark do operador contra busca completa e aleatória.
- `TOKEN_VAZIO_FORMAT_MATRIX`: propagação real de bit-flip em PNG, JPEG, SVG e dados crus.
- `TOKEN_VAZIO_NOVELTY`: revisão de anterioridade feature-by-feature.
- `TOKEN_VAZIO_DYNAMICS`: prova de qualquer claim de 42 atratores dinâmicos.

## 7. Destinos criados

### Papers

```text
docs/formulas-error-attention-combinations-research-note.md
docs/formulas-error-attention-combinations-claims.jsonl
```

### Mapa

```text
docs/canonical/2026-08-04/FORMULAS_ERRO_ATENCAO_COMBINACOES.md
data/latents/2026-08-04/formulas_erro_atencao_combinacoes.jsonl
receipts/papers/2026-08-04/FORMULAS_ERRO_ATENCAO_COMBINACOES_RECEIPT.json
```

## 8. Próximo gate

Implementar três experimentos reproduzíveis:

1. verificador simbólico das fórmulas e erros de transcrição;
2. matriz de bit-flip por formato e offset;
3. comparação de busca completa, aleatória e guiada por atenção.

Métricas mínimas:

```text
recall, precision, evaluations, false_negative_rate,
p50, p95, p99, source_hash, toolchain, commit
```

## 9. Retroalimentação

`F_ok`: separação autoral, prova Mod 6 ↔ U(9), fórmula do operador e roteamento para paper.  
`F_gap`: hashes das fontes, anterioridade e benchmarks.  
`F_next`: implementar os verificadores e gerar receipts sem promover claims abertos.
