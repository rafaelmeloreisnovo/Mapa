# RAFAELIA — Foundation Local Termux V1

**Estado:** `IMPLEMENTED_LOCAL_CONTRACT_PENDING_REPOSITORY_RECEIPT`  
**Autoridade de ontologia:** `rafaelmeloreisnovo/Mapa`  
**Autoridade de execução:** repositório-alvo + Termux local  
**Claim permitido:** `false`  
**Rede exigida pelo executor:** `false`

## Finalidade

Foundation V1 fornece uma superfície única para qualquer checkout local:

    init -> plan -> verify -> explicit run -> receipt

Ela não substitui o código do repositório-alvo, o compilador específico, a
cadeia de prova do RafPolimata, o plano de controle do RafGitTools, nem a
autoridade editorial do Drive. Ela torna a passagem para Termux explícita,
reproduzível e auditável.

## Invariantes

1. Cada checkout recebe um arquivo declarativo próprio.
2. A seleção de perfil nunca é inferida por extensão ou nome de arquivo.
3. O executor aceita somente vetores de argumentos; não invoca shell.
4. Cada operação cria um diretório novo em `COMPILA`.
5. O receipt inclui ambiente, inputs com SHA-256, comandos observados e
   estado de decisão.
6. `claim_allowed=false` é requisito de schema, não comentário.
7. GitHub Actions pode checar o contrato do pacote, mas não substitui receipt
   Termux de um checkout nem prova dispositivo/SDK/ELF/APK.

## Fronteira freestanding

O perfil `freestanding-object` produz apenas objeto C ou assembly com flags de
compilação freestanding. Linkar um ELF requer CRT, entrada, linker script, ABI,
syscalls e target explicitamente definidos pelo repositório. Portanto, a
Foundation não chama um objeto compilado de executável e não chama execução
Termux de bare metal.

## Relacionamento federado

| Papel | Destino | Saída da Foundation |
|---|---|---|
| Memória editorial | Drive | Referência e contexto, sem execução automática |
| Ontologia e roteamento | Mapa | Perfil, repositório e receipt revisáveis |
| Plano de controle | RafGitTools | Possível job/dry-run derivado, não execução presumida |
| Evidência determinística | RafPolimata | Receipts e testes específicos de domínio |
| Runtime Android | Termux | Ambiente e saída local observados |
| Ciência falsificável | RLL | Apenas inputs/execuções científicos explicitamente declarados |

## Próximo passo verificável

Inicializar a Foundation em um checkout concreto, executar primeiro `plan` e
`verify`, depois um único profile de baixo risco. O receipt resultante deve ser
revisado contra o commit do checkout antes de entrar em `Mapa/auditoria`.

## R3

`F_ok`: existe um núcleo reutilizável para documento, pré-voo, execução local e
recibo sem API ou CI privada.  
`F_gap`: nenhum repositório-alvo foi promovido por esta documentação; SDK,
compiladores, links freestanding e dispositivos continuam dependentes de
receipts próprios.  
`F_next`: aplicar em um checkout alvo de perfil único e registrar seu primeiro
receipt imutável.
