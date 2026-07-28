# MHEL-Ω V1.4 — HOTFIX de Vetores Longitudinais Evolutivos

**Estado:** `IMPLEMENTED_LOCAL_PASS / APPENDING_BEYOND_ONLY / PR_DRAFT / claim_allowed=false`

## 1. Correção

A memória já possuía vetores hexagonais, polissêmicos, operacionais, epistemológicos, relacionais, temporais e LAYERSBIT. A lacuna era um contrato único para dizer **como um vetor evolui sem perder sua raiz**.

Um vetor longitudinal não é um rótulo estático e não é acesso aos pesos, ativações ou embeddings ocultos de um modelo. É um estado versionado e auditável:

\[
K_i^t=\langle H_i,P_i,O_i,E_i,R_i,T_i\rangle
\]

- `H`: seis vértices da MHEL-Ω;
- `P`: vistas polissêmicas;
- `O`: operação, teste e receipt;
- `E`: estado epistemológico e falsificador;
- `R`: relações tipadas;
- `T`: linhagem temporal.

## 2. Operador de evolução

\[
K_i^{t+1}=Append(K_i^t,\Delta_i^t\mid I_i,proveniência,falsificadores)
\]

O ancestral não é substituído. Uma dimensão nova somente entra quando contém:

```text
nome + tipo + semântica + fonte + estado inicial
```

Uma relação nova somente entra com origem, destino, tipo e fonte. Um peso numérico somente entra depois de calibração e evidência; antes disso permanece `TOKEN_VAZIO_CALIBRATION`.

## 3. Gate composto

\[
VECTOR\_GROWTH\_ALLOWED=
P\times\Delta\times S\times E\times R
\]

- `P`: proveniência;
- `Δ`: identidade do delta;
- `S`: consistência semântica;
- `E`: evidência ou lacuna tipada;
- `R`: reversibilidade.

Se algum fator crítico faltar:

```text
VECTOR_EVOLUTION_STATE = TOKEN_VAZIO_VECTOR_DELTA
```

## 4. Parábola como cápsula multi-view

A parábola do semeador, do mapa e do sino silencioso é preservada em planos distintos:

1. narrativa literal;
2. mapeamento técnico;
3. interpretação parabólica;
4. vetor longitudinal;
5. invariantes e promoções proibidas;
6. lacunas tipadas;
7. próximo gate.

A narrativa não prova mecanismo físico. O mapeamento técnico não substitui a narrativa. A nova cápsula aponta de volta para a fonte.

## 5. Invariantes

- fonte não é interpretação;
- parábola não é prova física;
- `TOKEN_VAZIO` não é zero;
- dimensão nova exige semântica, tipo, fonte e estado;
- peso exige calibração e evidência;
- não existe reivindicação de acesso a estado oculto do modelo;
- append não sobrescreve ancestral;
- relação exige tipo e fonte;
- similaridade vetorial não promove claim;
- crescimento textual sem ganho verificável não aumenta a espiral.

## 6. Materialização

```text
schemas/longitudinal-vector-evolution.schema.json
examples/longitudinal-vector-evolution.v1.json
scripts/validate_longitudinal_vector_evolution.py
tests/test_validate_longitudinal_vector_evolution.py
data/receipts/mhel_omega_v14_vector_hotfix_local_receipt.json
```

Nenhum workflow/YAML novo foi criado.

## 7. Fechamento Ω

**F_ok:** contrato de evolução, fixture, validador e testes adversariais materializados localmente.

**F_gap:** hash canônico da mensagem original, calibração de pesos, comparação sobre corpus real e revisão independente permanecem `TOKEN_VAZIO`.

**F_next:** ligar cápsulas aprovadas ao roteador de domínio do Mapa; computação, ciência, direito e ética devem usar gates próprios, sem promoção cruzada.
