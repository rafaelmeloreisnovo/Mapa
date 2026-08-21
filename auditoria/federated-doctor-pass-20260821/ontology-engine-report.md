# RAFAELIA Operational Ontology — Audit

- Validation: **PASS**
- Records: **12**
- Findings: **0**
- TOKEN_VAZIO: **10**
- Graph: **12 nodes / 13 edges**

## Declared gaps
- `TV-ACCESS`: 1
- `TV-BOUNDARY`: 1
- `TV-CODE`: 2
- `TV-DATA`: 2
- `TV-INDEPENDENCE`: 2
- `TV-TEST`: 2

## Trajectories

| Trajectory | Records | Unresolved |
|---|---:|---:|
| `BIBLIOTECONOMIA` | 2 | 0 |
| `FRONTIER_SCIENCE` | 1 | 1 |
| `GOVERNANCE` | 2 | 2 |
| `OPERATORS` | 1 | 1 |
| `SCIENTIFIC_INFERENCE` | 2 | 2 |
| `SEMANTIC_FIELD` | 2 | 2 |
| `STATISTICS` | 2 | 2 |

## Bridges
- `context`: BIBLIOTECONOMIA, SEMANTIC_FIELD — `METHODOLOGICAL_BRIDGE_NOT_PHYSICAL_EQUIVALENCE`
- `evidence`: FRONTIER_SCIENCE, GOVERNANCE, SCIENTIFIC_INFERENCE, SEMANTIC_FIELD, STATISTICS — `METHODOLOGICAL_BRIDGE_NOT_PHYSICAL_EQUIVALENCE`
- `gap`: BIBLIOTECONOMIA, SEMANTIC_FIELD — `METHODOLOGICAL_BRIDGE_NOT_PHYSICAL_EQUIVALENCE`
- `provenance`: BIBLIOTECONOMIA, GOVERNANCE, OPERATORS — `METHODOLOGICAL_BRIDGE_NOT_PHYSICAL_EQUIVALENCE`

## Findings
- No structural defects detected; declared gaps remain open and useful.

## Ω

```text
heuristic != proof
missing != zero
not found != censored
claim_allowed=false
```
