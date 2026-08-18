# WILDCHAR + ΔMAINFOLD — Routing e Falsificação V1

**Estado:** `CANONICAL_DRAFT`  
**Claim gate:** `claim_allowed=false`  
**Autoridade canônica:** `rafaelmeloreisnovo/Mapa`

## 1. Finalidade

Esta camada amplia o espaço de busca sem ampliar artificialmente a certeza.

```text
tokenização + ↑ > N
N := *
* := cardinalidade aberta de candidatos conceituais
```

`*` não significa infinito matemático medido. Significa: **não fixar previamente a quantidade de conceitos, contraexemplos, fronteiras ou parábolas que podem ser gerados**.

O contrato fundamental é:

```text
WILDCHAR gera candidatos
→ ΔMAINFOLD organiza rotas
→ proveniência ancora
→ falsificador ataca
→ evidência compara
→ TOKEN_VAZIO preserva o desconhecido
→ F_NEXT reduz incerteza
→ gate existente decide promoção
```

Portanto:

```text
candidate != claim
analogy != mechanism
parabola != evidence
priority != truth
urgency != necessity
providencia_operacional != providência metafísica nem prova
TOKEN_VAZIO != zero
Ω∞ != certeza infinita
```

## 2. ΔMAINFOLD

`ΔMAINFOLD` é um operador de navegação semântico-operacional, não uma alegação de variedade matemática ou geometria física já demonstrada.

Ele projeta cada rota em sete eixos:

1. conceito;
2. evidência;
3. proveniência;
4. falsificador/estado;
5. lacuna/desconhecido;
6. urgência/necessidade;
7. próximo passo/providência operacional.

A expressão operacional é:

\[
\Delta M =
F_{gap}
\oplus F_{next}
\oplus F_{esquecido}
\oplus (F_{urgencia},F_{necessidade})
\oplus F_{proveniencia}
\oplus F_{providencia\_operacional}
\oplus F_{aprendizado\_nao\_regredir}
\oplus F_{otimizar}
\oplus F_{evolucao}
\oplus F_{so\_sei\_q\_nada\_sei}
\]

Não há pesos numéricos nesta versão. O estado é explicitamente:

```yaml
numeric_weights_state: TOKEN_VAZIO_CALIBRATION
```

Até haver calibração contra dados reais, prioridade usa as classes canônicas `P0_CRITICAL`…`P4_BACKLOG` já definidas no Mapa.

## 3. WILDCHAR

Cada item pode ser expandido por sete lentes:

1. `direct` — consequência direta;
2. `inverse` — hipótese inversa/reversa;
3. `boundary` — limite, domínio de validade, caso extremo;
4. `counterexample` — tentativa explícita de quebra;
5. `analogy_parabola` — transferência didática/simbólica;
6. `adjacent_domain_transfer` — ponte para domínio adjacente;
7. `unknown_unknown` — variável, dependência ou pergunta possivelmente esquecida.

Toda saída com `origin=WILDCHAR` nasce com:

```yaml
claim_allowed: false
```

Parábolas e analogias exigem:

```yaml
literal_claim: false
```

Se delas surgir uma proposição testável, cria-se **nova rota** do tipo `hypothesis`; a parábola original não muda retroativamente de papel.

## 4. Sete perguntas invariantes

Toda rota deve responder:

1. O que exatamente está sendo afirmado ou perguntado?
2. O que falsificaria isso?
3. Qual a cadeia fonte → artefato → claim?
4. Que evidência contrária ou contradição já existe?
5. O que continua desconhecido e deve permanecer `TOKEN_VAZIO`?
6. Qual a urgência e a necessidade, separadamente, e por quê?
7. Qual ação verificável reduz a incerteza agora?

## 5. Fatores

| Fator | Função |
|---|---|
| `F_GAP` | lacuna conhecida, evidência ausente, contrato incompleto |
| `F_NEXT` | menor próximo passo verificável |
| `F_ESQUECIDO` | órfão, stale, rota sem sucessor, variável não revisitada |
| `F_URGENCIA` | risco adicional causado pelo atraso |
| `F_NECESSIDADE` | dependência sem a qual um objetivo/gate não fecha |
| `F_PROVENIENCIA` | cadeia fonte → artefato → observação → claim |
| `F_PROVIDENCIA_OPERACIONAL` | ação de reparo/obtenção de evidência + critério de verificação |
| `F_APRENDIZADO_NAO_REGREDIR` | eventos append-only de criação, falsificação, correção e supersessão |
| `F_OTIMIZAR` | reduzir duplicação/latência sem apagar identidade/proveniência |
| `F_EVOLUCAO` | delta mensurável em cobertura, fechamento de gaps e qualidade de custódia |
| `F_SO_SEI_Q_NADA_SEI` | desconhecido explícito, com motivo e teste seguinte |

`F_PROVIDENCIA_OPERACIONAL` é deliberadamente secular e auditável no contrato: ação, verificação e estado. Não é evidência por si só.

## 6. Aprendizado sem regressão

Nada é apagado para fazer o presente parecer mais correto.

```text
erro
→ evento append-only
→ correção
→ supersedes/superseded
→ teste anti-regressão
→ nova decisão
```

Uma hipótese falsificada pode continuar navegável, mas nunca retorna silenciosamente a `VERIFIED_LIMITED`.

Contagem de rotas também não é métrica de evolução. Evolução exige delta observável, por exemplo:

```text
gaps fechados
+ proveniência completa
+ falsificadores executados
+ contradições registradas
+ duplicações resolvidas sem perda de custódia
```

## 7. Relação com os contratos existentes

Esta camada **não substitui**:

- workflow canônico de excelência operacional;
- invariantes de necessidade/urgência;
- heurísticas dinâmicas e vazios;
- ontologia operacional;
- gates cross-source;
- cadeia de custódia;
- decisão final de `claim_allowed`.

Ela somente cria uma interface comum entre expansão conceitual, roteamento e ataque falsificacionista.

## 8. Artefatos V1

```text
docs/WILDCHAR_DELTA_MANIFOLD_ROUTING_V1.md
schemas/wildchar-delta-manifold-route.v1.schema.json
data/routing/wildchar-delta-manifold.synthetic.v1.json
scripts/validate_wildchar_delta_manifold.py
tests/test_wildchar_delta_manifold.py
.github/workflows/wildchar-delta-manifold-gate.yml
```

A fixture é sintética de propósito. Ela testa o contrato sem fingir que uma rota científica real já possui evidência.

## 9. Gate V1

O gate deve rejeitar, no mínimo:

1. `origin=WILDCHAR` promovido diretamente;
2. parábola/analogia com `literal_claim=true`;
3. `TOKEN_VAZIO` sem motivo e próximo teste;
4. pesos numéricos inventados antes de calibração;
5. rota científica sem proveniência ou falsificador;
6. claim promovido sem evidência;
7. ledger anti-regressão fora de ordem ou com sequência duplicada.

## 10. Próximo vertical real

Depois do gate sintético passar, ingerir **uma única rota real** com:

```text
fonte imutável
→ locator de proveniência
→ claim literal
→ evidência a favor
→ evidência contra
→ falsificador
→ TOKEN_VAZIO residual
→ prioridade categórica
→ F_NEXT
```

Somente após esse vertical devem ser ampliadas novas famílias por WILDCHAR.

## 11. Limite

Esta V1 demonstra contrato, roteamento e falsificabilidade estrutural. Não demonstra completude do universo de dados, descoberta automática de todos os conceitos, superioridade científica do método ou qualquer geometria física subjacente.

**Ω∞ aqui significa horizonte aberto de busca; não certeza infinita.**
