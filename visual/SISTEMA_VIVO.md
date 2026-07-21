# Sistema Vivo — visão de desenvolvimento

> Visualização é navegação; não é prova.

```mermaid
flowchart TB
    A[Identidade observada pelo GitHub] --> B[Inventário checkpoint + deltas]
    B --> C{Existe perfil evidenciado?}
    C -- não --> D[TOKEN_VAZIO<br/>reason + next_action + exit_criteria]
    C -- sim --> E[Célula epistêmica<br/>FATO | HIPOTESE | PARABOLA]
    D --> F[Índice do Sistema Vivo]
    E --> F
    F --> G[Completude derivada]
    F --> H[Hash BLAKE2b-256]
    F --> I[Mapa visual e rotas]
    G --> J{Gate de promoção}
    H --> J
    I --> J
    J -- evidência insuficiente --> D
    J -- evidência suficiente --> K[Conhecimento navegável]
```

## Matriz de leitura

| Pergunta | Campo | Quando está vazio |
|---|---|---|
| Por que existe? | `purpose` | ler README, manifesto e escopo |
| O que recebe? | `inputs` | localizar APIs, formatos e fontes |
| O que faz? | `transformations` | seguir fluxo real de execução |
| O que produz? | `outputs` | observar artefatos e contratos |
| Como conversa? | `interfaces` | localizar CLI, API, ABI, arquivos e eventos |
| O que nunca deve quebrar? | `invariants` | extrair testes, normas e asserts |
| Como prova qualidade? | `quality_controls` | localizar validação, testes e auditoria |
| Onde pode falhar? | `risks` | registrar hipótese, impacto e evidência |
| De quem depende e quem o consome? | `relations` | construir arestas produtor/consumidor |
| Que visão humana carrega? | `philosophical_context` | marcar parábola separadamente |
| Como pode ser compreendido rapidamente? | `visual_model` | produzir diagrama sem exceder a evidência |

## Ciclo ψ→χ→ρ→Δ→Σ→Ω

```text
ψ intenção      → escolher o repositório e o mecanismo
χ observação    → ler arquivos, commits e contratos
ρ ruído         → registrar conflitos e ambiguidades
Δ transmutação  → classificar FATO/HIPOTESE/PARABOLA/TOKEN_VAZIO
Σ memória       → gerar índice determinístico e hash
Ω completude    → promover somente o que atravessou o gate
```

## Estado inicial desta refatoração

- A identidade dos repositórios continua vindo do inventário existente.
- O primeiro perfil materializado descreve o próprio `rafaelmeloreisnovo/Mapa`.
- Repositórios ainda não lidos recebem onze células `TOKEN_VAZIO` automaticamente.
- A relação semântica profunda entre repositórios não é presumida.

O vazio aqui não interrompe o mapa; ele aponta a próxima leitura.
