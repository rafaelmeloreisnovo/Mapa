# Ponte Livro Vivo — Mapas, Navegação e Invariantes Visuais

> Modo: ponte operacional entre `Mapa` e o Livro Vivo RAFAELIA  
> Status inicial: `FORMALIZACAO_READY` + `RISCO_DE_CONFUSAO`  
> Regra: mapa sem legenda é desenho; mapa com escala vira navegação

## Parábola da bússola sem norte

O discípulo desenhou um mapa enorme.

Montanhas, rios, pontes e cidades apareciam com beleza.

O mestre perguntou:

— Onde fica o norte?

O discípulo não sabia.

— Qual é a escala?

Também não sabia.

Então o mestre disse:

— Sem norte e sem escala, o mapa encanta, mas não guia.

## Invariante

```text
sinal visual → legenda → escala → relação → caminho navegável
```

Forma compacta:

```math
Inv(Mapa)=Visual\rightarrow Legenda\rightarrow Escala\rightarrow Grafo\rightarrow Navegação
```

## Risco principal

| Risco | Correção |
|---|---|
| mapa bonito sem função | declarar uso e legenda |
| grafo sem nós/arestas definidos | criar schema mínimo |
| direção sem referência | declarar norte/origem/eixo |
| imagem privada sem classificação | aplicar público/privado |
| mapa sem vínculo | linkar capítulo, hipótese ou artefato |

## Próximos passos

1. Criar `MAPA_VISUAL_INDEX.md`.
2. Definir legenda, escala, eixo e domínio por mapa.
3. Separar mapa conceitual, mapa visual, mapa de repositórios e mapa de dados.
4. Criar schema simples para nós e arestas.
5. Linkar mapas ao Livro Vivo e aos artefatos.

## Ficha Livro Vivo

```yaml
repo: rafaelmeloreisnovo/Mapa
familia: Visual/Mapa
invariante: "sinal visual → legenda → escala → relação → caminho navegável"
selo: FORMALIZACAO_READY
risco: "mapa sem escala, legenda, eixo ou vínculo com artefato"
proximo_passo: "criar MAPA_VISUAL_INDEX.md e schema mínimo de nós/arestas"
```

## Retroalimentar[3]

- **F_ok:** o repo Mapa recebe ponte para transformar visual em navegação auditável.
- **F_gap:** falta inventário real dos mapas e separação por tipo.
- **F_next:** criar `MAPA_VISUAL_INDEX.md`.
