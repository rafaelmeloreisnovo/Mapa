# Índice — Ontologia Operacional RAFAELIA

## Autoridade

| Artefato | Função | Autoridade |
|---|---|---|
| `data/ontology/rafaelia-operational-ontology.v1.json` | registro canônico de conceitos, lacunas e trajetórias | dados estruturados |
| `schemas/operational-ontology.schema.json` | contrato externo JSON Schema | estrutura |
| `scripts/operational_ontology_engine.py` | validação, heurísticas, grafo e relatório | execução local |
| `tests/test_operational_ontology_engine.py` | invariantes positivos e negativos | regressão |
| `docs/ONTOLOGIA_OPERACIONAL_RAFAELIA.md` | leitura arquitetural | documentação |
| `docs/HEURISTICAS_DINAMICAS_E_VAZIOS.md` | regras de descoberta e abstinência | método |

## Relação com estruturas existentes

- `tools/repository_gap_mapper.py` continua responsável por arquivos, builds,
  binários e marcadores de repositório.
- A ontologia nova atua acima dele: claims, conceitos, relações, trajetórias,
  estados editoriais, operadores e lacunas epistemológicas.
- `protocolos/HOMEOSTASE_OPERACIONAL_MELHORIA_CONTINUA.md` permanece como régua
  normativa.
- `biblioteconomia/02_VOCABULARIO_CONTROLADO.md` permanece como controle de
  autoridade terminológica.

## Regra de não duplicação

```text
repository_gap_mapper = inventário físico/documental
operational_ontology_engine = inventário semântico/epistemológico
```

Um não substitui o outro. Seus relatórios podem ser ligados posteriormente por
`artifact_id`, `record_id`, caminho e hash.

## Baseline v1

```text
records = 12
epistemic_state.EVIDENCIADO = 2
epistemic_state.TOKEN_VAZIO = 10
graph.nodes = 12
graph.edges = 13
cross_trajectory_bridges = 4
structural_findings = 0
claim_allowed = false
```

Os vazios declarados cobrem `TV-ACCESS`, `TV-BOUNDARY`, `TV-CODE`, `TV-DATA`,
`TV-INDEPENDENCE` e `TV-TEST`. Eles são itens do inventário, não defeitos
silenciosamente apagados.

## Próximos acoplamentos

1. gerar registros ontológicos a partir do gap mapper sem promover claims;
2. criar `lineage_id` para paper→dataset→laboratório→run→commit;
3. registrar resultados negativos como evidência;
4. implementar DAG causal separado;
5. calibrar prioridades somente em benchmark bloqueado.
