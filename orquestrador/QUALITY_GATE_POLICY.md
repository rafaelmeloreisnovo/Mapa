> ⟦PRIMEIRA-LINHA · DIGNIDADE-HUMANA · PROTEÇÃO-INFANTIL⟧ — nenhuma automação promove conteúdo acima da evidência disponível; a proteção da vida e da criança precede desempenho, publicação e integração.

# Política do Gate de Qualidade da Topologia

## 1. Propósito

Este contrato governa a passagem entre **mapa documental**, **índices derivados**, **orquestração** e **injeção de contexto em IA**. O gate impede que uma declaração estrutural seja promovida como executável quando ainda existe como `LACUNA`.

A fonte canônica é:

```text
indices/GRAFO_DEPENDENCIAS_MAPA.yaml
```

O arquivo usa JSON canônico compatível com YAML 1.2 para permitir validação apenas com a biblioteca padrão do Python.

## 2. Invariantes bloqueantes

O gate retorna falha quando qualquer condição abaixo ocorre:

1. referência a nó inexistente;
2. auto-dependência ou ciclo;
3. nó órfão fora de `I_00`;
4. arquivo obrigatório ausente;
5. `state=active` sem `epistemic_mark=FATO`;
6. `state=planned` sem `epistemic_mark=LACUNA`;
7. métricas declaradas diferentes das métricas derivadas;
8. hash BLAKE2b-256 diferente do conteúdo canônico;
9. ausência do selo de Primeira Linha na primeira linha física.

## 3. Relação normativa corrigida

A especificação de varredura e sua implementação possuem direção única:

```text
QUAL_16  ──especifica──▶  F_03  ──gera──▶  IND_MANIFESTO
```

`QUAL_16` **não depende** de `F_03`. Essa separação elimina o ciclo anteriormente presente e preserva o princípio:

\[
\text{norma} \rightarrow \text{implementação} \rightarrow \text{evidência}
\]

## 4. Estados epistêmicos

| Estado | Marca obrigatória | Significado operacional |
|---|---|---|
| `active` | `FATO` | artefato presente e utilizável dentro do escopo declarado |
| `planned` | `LACUNA` | caminho reservado, sem promoção indevida de implementação |

A presença posterior de um arquivo planejado gera aviso e exige revisão explícita antes de sua promoção para `active`.

## 5. Ordem de execução

A ordem não é escrita manualmente. Ela é derivada por ordenação topológica:

```text
I_00
  → classificação e substrato
  → vocabulário e catálogo
  → normas e ferramentas
  → índices e evidências
  → avaliação e roadmap
  → orquestrador
  → consulta
  → injeção de contexto
  → gate final
```

Os campos reversos `dependentes` foram removidos da fonte canônica. Eles são calculados pelo validador, evitando duas verdades concorrentes.

## 6. Comandos oficiais

```bash
python3 scripts/validate_mapa_topology.py
python3 -m unittest tests/test_topology.py -v
python3 scripts/validate_mapa_topology.py \
  --write-report topology-validation.json
```

## 7. Regra de promoção

Um nó planejado somente pode ser promovido quando:

- o arquivo existe;
- há teste correspondente;
- suas dependências estão ativas ou explicitamente aceitas como entrada planejada;
- a marca muda de `LACUNA` para `FATO`;
- o hash e as métricas são recalculados;
- o workflow de topologia conclui com sucesso.

Até isso ocorrer:

```text
claim_allowed = false
```

## 8. Artefato de auditoria

A GitHub Action produz:

- `topology-validation.json`;
- `TOPOLOGY_CHECKSUMS.sha256`.

Esses artefatos registram resultado, ordem topológica, métricas, nós críticos, lacunas e prova de integridade sem modificar automaticamente o repositório.
