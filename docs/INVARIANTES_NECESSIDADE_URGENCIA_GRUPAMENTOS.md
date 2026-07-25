# Invariantes de Necessidade, Urgência, Grupamentos e Mesma Situação

## Finalidade

Esta camada responde, antes da execução:

1. o que é necessário;
2. o que é urgente;
3. o que pertence ao mesmo grupo;
4. quando dois registros representam realmente a mesma situação.

## Invariante global

\[
I_{dados}=identidade\land proveniência\land contexto\land privacidade\land estado\ epistêmico\land dependências\land evidência\land próximo\ passo
\]

Nenhum agrupamento pode apagar qualquer componente desse vetor.

## Necessidade não é urgência

- **necessidade:** requisito sem o qual um objetivo não fecha;
- **urgência:** atraso aumenta dano, bloqueio ou perda;
- **importância:** impacto potencial, ainda que sem pressão temporal;
- **prioridade:** decisão derivada da combinação dessas dimensões.

A fila usa:

\[
P=f(H,S,O,D,R,E,V)
\]

com segurança humana, privacidade, impacto, dependências, risco de atraso, déficit de evidência e reversibilidade. Segurança humana e privacidade precedem throughput.

| Classe | Significado |
|---|---|
| `P0_CRITICAL` | risco humano, privacidade ou integridade com atraso intolerável |
| `P1_URGENT` | bloqueia cadeia relevante ou agrava rapidamente o risco |
| `P2_NECESSARY` | requisito para fechar um vertical ou gate |
| `P3_IMPORTANT` | melhora significativa sem bloqueio imediato |
| `P4_BACKLOG` | útil, mas não interrompe caminhos superiores |

## Grupamento

Itens podem compartilhar grupo por domínio, alvo, assinatura de invariantes, cadeia de dependência, risco ou privacidade.

\[
mesmo\ grupo\not\Rightarrow mesma\ situação
\]

## Mesma situação

`SAME_SITUATION` só é aceito quando coincidem domínio, tipo, alvo, classe de dados, privacidade, estado epistêmico e estados dos invariantes, além de existir evidência explícita.

Quando somente a forma estrutural se parece, usa-se `STRUCTURAL_ANALOG`.

Exemplo: cache RMR sem wiring produtivo e process monitor sem wiring produtivo compartilham a forma “implementado, mas não conectado”, porém têm alvos, riscos e critérios diferentes. São analogia estrutural, não identidade.

## Passos operacionais

```text
OBSERVE
→ CLASSIFY
→ CHECK INVARIANTS
→ BUILD DEPENDENCIES
→ GROUP
→ TEST EQUIVALENCE
→ DERIVE PRIORITY
→ ASSIGN NEXT ACTION
→ EXECUTE
→ VERIFY
→ CLOSE ou TOKEN_VAZIO
```

## Invariantes centrais

1. fonte original imutável;
2. privacidade antes da interpretação;
3. nenhuma reidentificação presumida segura;
4. evidência antes da promoção;
5. causa-raiz não inventada;
6. checkout real antes de claim remoto;
7. artifact e hash antes de `VERIFIED`;
8. modelo sem acesso direto à fonte bruta;
9. abstinência diante de ambiguidade;
10. shadow mode antes de substituição produtiva;
11. equivalência byte a byte antes de reuso;
12. callsite real antes de declarar wiring;
13. fechamento vertical antes de expansão;
14. reconhecimento de formato não equivale a classificação;
15. leitura streaming, limitada e retomável.

## Estado inicial

O registro inicial contém oito itens, quatro grupos e cinco relações. A fila é calculada pelo validador, não ordenada manualmente para favorecer uma narrativa.

Um item somente vira `VERIFIED` ou `CLOSED` quando invariantes aplicáveis, evidências, dependências e risco residual estão registrados. Até lá, `claim_allowed=false`.
