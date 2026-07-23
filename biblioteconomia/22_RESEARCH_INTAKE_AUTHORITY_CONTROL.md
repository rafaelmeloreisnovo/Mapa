# Controle de autoridade — ingestão científica

## Autoridades separadas

| Autoridade | Responsabilidade |
|---|---|
| Fonte externa | metadado e identificador publicados |
| Mapa privado | acervo, revisão, classificação e cadeia de custódia |
| RLL público | testes locais, resultados, falsificadores e navegação liberada |
| Revisor humano | promoção ou rebaixamento epistemológico |

## Sinônimos e colisões

- `Cielo` é tratado provisoriamente como possível referência a `SciELO`; o alias precisa ser
  confirmado no contexto de cada consulta.
- Google Scholar é ferramenta de descoberta, mas não é adaptador automatizado v1.
- Duplicatas por DOI, PMID ou arXiv são fundidas como um mesmo objeto bibliográfico.
- Homônimos de autores não são fundidos sem identificador persistente.

## Independência

Crossref, OpenAlex e Semantic Scholar podem repetir o mesmo paper. Isso aumenta a confiança
na identificação do registro, mas não aumenta automaticamente a evidência científica do claim.

```text
metadata_corroboration != experimental_replication
```
