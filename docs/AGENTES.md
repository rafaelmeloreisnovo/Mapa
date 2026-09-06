# Protocolo de entrada dos agentes no Mapa

A autoridade local é [`AGENTS.md`](../AGENTS.md). Este arquivo fecha a rota
documental referenciada por esse contrato e por [`CLAUDE.md`](../CLAUDE.md).
As instruções de especialidade de outros produtores permanecem nesses produtores.

## Sequência operacional

1. Identificar repo, branch, commit, caminho e hash dos bytes lidos.
2. Responder Q01–Q12 do contrato raiz, incluindo autoridade, escopo e classificação dos dados.
3. Abrir o [`bootstrap federado`](../bootstrap/RAFAELIA_CHATGPT_BOOTSTRAP_V1.md)
   e a rota pertinente no [`Atlas`](../indices/RAFAELIA_ATLAS_ROUTING_INDEX_V1.md).
4. Conferir a evidência no produtor e executar o gate disponível no escopo declarado.
5. Registrar delta, predecessor, receipt, limitações e próximo gate observável.

O Mapa registra relações e estado federado. Código e runtime permanecem sob a
autoridade dos produtores. Hash, estrutura ou teste local não provam execução física.

## Preservação

Trabalhar em branch de revisão, preservar receipts históricos e manter
`claim_allowed=false` enquanto houver gates de promoção em aberto.
Dados privados são representados por identidades e hashes quando isso basta.
Ausência de fonte ou de execução permanece `TOKEN_VAZIO` com próxima sonda explícita.

O bootstrap da skill Ω menciona três caminhos `memory_bridge/...` não presentes
neste snapshot do Mapa. Sua ausência não é suprida por arquivos fictícios:
as âncoras Drive efetivamente localizadas estão no bootstrap federado, enquanto
a localização canônica daqueles três contratos segue como `TOKEN_VAZIO`.
