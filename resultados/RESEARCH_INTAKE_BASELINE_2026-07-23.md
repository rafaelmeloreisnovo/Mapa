# Baseline local — Research Intake v1

```text
config XML                     PASS
XSD well-formed                PASS
Python compilation             PASS
unittest                       14/14 PASS
fixture records input          7
canonical records              6
metadata duplicates merged     1
reviewed records               3
public records exported        1
persistent IDs preserved       PASS
numbered artifacts             00–10 + CHECKSUMS
claim_allowed                  false
automatic public push          false
automatic claim promotion      false
```

O baseline usa fixture controlada. Não demonstra disponibilidade atual das APIs nem executa
coleta online. O modo de rede existe em escopo limitado para Crossref, OpenAlex, Semantic
Scholar e Europe PMC; arXiv e SciELO permanecem declarados, mas sua coleta XML específica é
`TOKEN_VAZIO_CODE` até testes dedicados.

A numeração canônica usa `data/research_intake/id_registry.v1.json`. Novas chaves recebem o
próximo número; nenhuma execução pode renumerar silenciosamente os registros históricos.
`10_ID_REGISTRY_PROPOSAL.json` exige revisão e commit explícito antes de substituir o registro.
