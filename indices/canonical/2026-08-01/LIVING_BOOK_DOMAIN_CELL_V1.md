# Mapa Canônico — Célula de Domínio do Livro Vivo V1

## Objeto observado

O repositório produtor `instituto-Rafael/LivroVivo_ThisBookLives` abriu o PR draft **#9** com a primeira célula de domínio operacional: `LBC-MUSIC-0001`.

A célula não obriga o participante musical a aprender programação ou matemática. Esses conhecimentos entram como módulos paralelos de apoio e devem traduzir suas saídas novamente para a linguagem da música.

```text
semente humana
→ music.core
├── support.math
├── support.code
├── support.ai
└── support.security
→ explicação musical
→ decisão humana
```

## Denominador comum

O denominador não é “todo mundo saber tudo”. É todo módulo declarar o mesmo contrato mínimo:

```text
origem
intenção
domínio
autoridade
entrada
transformação
saída
evidência
limite
privacidade
aprovação
receipt
retorno
```

Assim, músico, agricultor, advogado, programador ou pesquisador podem usar interfaces próprias enquanto a infraestrutura preserva governança e prova.

## Espelhos humano e IA

```text
espelho humano
= sentido + consentimento + correção + autoridade final

espelho IA
= organização + relação + tradução + proposta + marcação de lacuna
```

A IA não pode aprovar a própria saída, publicar, promover claim, revelar conteúdo privado ou executar entrada não confiável.

## Autoridades federadas

| Superfície | Autoridade |
|---|---|
| Domínio, semente e narrativa | `LivroVivo_ThisBookLives` |
| Índice, relações e fronteira de claim | `Mapa` |
| Compilação de procedimento e validação | `RafPolimata` |
| Transporte, bundles, diff e receipts | `RafGitTools` |
| Menu Android e execução Termux limitada | `termux-app-rafacodephi` |
| Fontes privadas e memória longitudinal | Google Drive RAFAELIA |

Nenhum repositório deve copiar o núcleo dos outros. Cada um mantém um adaptador pequeno e um ponteiro para a autoridade correta.

## Gates observados

| Gate | Estado |
|---|---|
| Estrutura local | `PASS` — validador e 8/8 testes |
| Revisão do produtor | `TOKEN_VAZIO_HUMAN_REVIEW` |
| Rota no Mapa | materializada nesta branch |
| Adaptador RafPolimata | `TOKEN_VAZIO_NOT_IMPLEMENTED` |
| Adaptador RafGitTools | `TOKEN_VAZIO_NOT_IMPLEMENTED` |
| Menu/receipt Termux | `TOKEN_VAZIO_RUNTIME_NOT_EXECUTED` |
| Revisão independente de privacidade | `TOKEN_VAZIO_INDEPENDENT_REVIEW` |

## Perguntas obrigatórias de auditoria

1. Quem possui autoridade final sobre o sentido do domínio?
2. A fonte privada foi resumida sem publicação do texto bruto?
3. A pessoa consegue operar sem linguagem técnica auxiliar?
4. O módulo auxiliar devolveu a saída na linguagem do domínio?
5. A aprovação humana aponta para o digest exato?
6. A ação possui ambiente, procedimento, testes, saída, rollback e receipt?
7. Qual `TOKEN_VAZIO` continua aberto e qual gate pode fechá-lo?

## Digest do objeto musical

```text
SHA-256      c2dba442fb9efedb33b4ecc40b38d2f594b7bd0e343051be93087c26724fc9c7
SHA3-256     cfbc142cafba40b9e31bdcd4b0f4dbdd2ea3258ea3014c59e02ff8ab35a25b05
BLAKE2b-256  bbe51280f4a16110ef081bc155ee7c9b3bff5a1cb7d6772af8060262a7abf224
```

Os hashes demonstram identidade do payload canônico; não demonstram verdade musical, execução Android nem eficácia da IA.

## Próximo passo com menor risco

O próximo adaptador coerente pertence ao `RafPolimata`, mas só deve compilar um **procedimento limitado**, sem transportar fontes privadas e sem executar nada. A saída esperada é uma IR de trabalho contendo:

```text
intent_id
cell_id
module_id
action
inputs por digest
capabilities requeridas
policy gates
human approval requirement
expected receipt
rollback
```

Depois disso, o `RafGitTools` poderá transportar o bundle e o Termux poderá materializá-lo apenas após autorização vinculada ao hash.

## Estado

```text
claim_allowed=false
automatic_execution=false
automatic_merge=false
raw_private_text_present=false
state=ROUTED_NOT_PROMOTED
```

### R₃

- **F_ok:** célula produtora e matriz de autoridade possuem artefatos concretos.
- **F_gap:** compilador, transporte, runtime físico e revisão independente.
- **F_next:** um adaptador RafPolimata limitado, somente após revisão do PR produtor.
