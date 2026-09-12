# RAFAELIA — Padrão Obrigatório de Atribuição e Citação V1

**Status:** `DRAFT_COUNSEL_REVIEW_REQUIRED`

## 1. Regra

Quando uma licença RAFAELIA aplicável exigir atribuição, a simples menção a um repositório não satisfaz, por si só, o padrão de atribuição.

A atribuição deve permitir reconstruir:

```text
quem criou
→ qual obra
→ qual versão
→ de onde veio
→ o que foi modificado
→ sob qual licença
```

## 2. Bloco mínimo obrigatório

Para material de Rafael Melo Reis:

```text
Autor: Rafael Melo Reis
Projeto: RAFAELIA (ΣΩΔΦBITRAF)
Obra/Componente: <título ou caminho identificável>
Versão/Commit/Hash: <quando disponível>
Fonte: <URL/repositório/documento>
Licença: RAFAELIA-NC-ATTR-V1, salvo indicação diferente no componente
Modificações: <nenhuma | descrição breve>
```

## 3. Citação bibliográfica recomendada para textos/papers

Formato genérico:

```text
MELO REIS, Rafael. <Título da obra>. RAFAELIA (ΣΩΔΦBITRAF),
versão <versão/commit>, <ano>. Disponível em: <URL>.
Acesso em: <data>. Licença: <identificador>.
```

A citação deverá usar o título real da obra e a versão real; valores ausentes permanecem `TOKEN_VAZIO` até serem conhecidos.

## 4. Software e código

Em distribuição de código ou binário que incorpore Material Original RAFAELIA, a atribuição deve aparecer em pelo menos uma superfície razoavelmente acessível:

- arquivo `NOTICE`;
- `About > Legal / Open Source Notices / Third-Party Notices`;
- documentação distribuída;
- tela legal equivalente, quando houver UI.

Quando a licença de terceiro exigir formato específico, esse formato prevalece para o componente de terceiro.

## 5. Derivados

Toda adaptação deve declarar de forma inequívoca:

- que é modificada;
- quem realizou a modificação;
- data ou versão;
- que o autor original não necessariamente endossa a modificação.

## 6. Proibição de falsa atribuição

É proibido:

- remover o autor original quando a atribuição for juridicamente exigível;
- atribuir ao autor uma modificação de terceiro;
- inserir o nome do autor para sugerir endosso;
- substituir o nome do autor por username, organização ou nome de repositório.

## 7. Base autoral

O padrão é coerente com o direito moral de reivindicar autoria e de ter o nome do autor indicado na utilização da obra, sem pretender ampliar por contrato direitos que a lei não permita ampliar.

