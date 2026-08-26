# Política de Higiene — Conteúdo de Uso Ilícito

**Estado:** ACTIVE / FAIL-CLOSED  
**Data:** 2026-08-25  
**Escopo:** federação RAFAELIA / Mapa / ingestão / índices / rotas GitHub

## Regra

Nenhuma rota ativa deve publicar, promover, ensinar, facilitar ou indexar como material operacional conteúdo destinado a:

- uso ou consumo ilícito de substâncias;
- preparo, extração ou fabricação para consumo ilícito;
- dosagem, combinação ou otimização de efeitos para uso recreativo ilícito;
- aquisição, venda, distribuição, ocultação ou cultivo ilícitos.

Termos de triagem incluem LSD, maconha/marijuana/weed/cannabis, DMT, MDMA e outras substâncias controladas. **A presença isolada de uma palavra não é prova de violação.** O gate é semântico.

## Exceções preservadas

Não remover automaticamente:

1. evidência judicial, cadeia de custódia, legislação ou jurisprudência;
2. pesquisa científica, médica, toxicológica, histórica ou de saúde pública em contexto neutro;
3. referências bibliográficas legítimas;
4. símbolos, identificadores ou substrings de software sem relação semântica com drogas;
5. documentação de segurança, prevenção, compliance ou redução de risco sem instrução de uso ilícito.

## Gate obrigatório

Classificação de cada ocorrência:

- `BLOCK_ILLICIT_USE`: remover da rota ativa e impedir ingestão/indexação;
- `ALLOW_LEGAL_EVIDENCE`: preservar como evidência jurídica;
- `ALLOW_SCIENTIFIC_NEUTRAL`: preservar pesquisa neutra;
- `ALLOW_TECH_FALSE_POSITIVE`: preservar símbolo técnico;
- `TOKEN_VAZIO`: contexto insuficiente; não publicar como rota operacional até revisão.

`BLOCK_ILLICIT_USE` tem precedência sobre catálogo, índice, memória, ingestão e roteamento.

## Invariantes

- palavra ≠ intenção;
- evidência jurídica ≠ promoção;
- pesquisa neutra ≠ instrução de consumo;
- substring técnica ≠ substância;
- `TOKEN_VAZIO` ≠ autorização;
- histórico Git ≠ rota ativa.

## Auditoria 2026-08-25

A busca federada encontrou numerosos falsos positivos de siglas em QEMU/dependências e referências científicas/jurídicas legítimas. Um projeto anteriormente catalogado por nome foi revalidado como não acessível e deve permanecer excluído do roteamento ativo por tombstone no índice de governança.

## Próximo gate

Toda nova ingestão de repositório deve aplicar `indices/ROUTE_DENYLIST_ILLICIT_USE.yaml` antes de produzir relações, vetores, resumos ou claims.
