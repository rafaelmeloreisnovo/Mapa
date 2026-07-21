# Cadeia de Custódia e Governança de Dados — Mapa

## 1. Finalidade

Esta camada transforma cada entrada, classificação, alteração, validação e
publicação do ecossistema RAFAELIA em um evento rastreável, verificável e
reexecutável.

Ela complementa, sem substituir:

- `protocolos/PROTOCOLO_EXECUCAO_EXCELENCIA.md`;
- `protocolos/TOKEN_VAZIO_LACUNAS.md`;
- `biblioteconomia/README.md`;
- `orquestrador/SCHEMA_ORQUESTRADOR_MAPA.md`.

O objetivo não é produzir burocracia. É reduzir perda de contexto, falso
positivo, duplicidade, ambiguidade semântica e alteração sem prova.

## 2. Invariante operacional

Toda mudança material deve responder, de forma auditável:

1. **qual objeto** foi recebido ou alterado;
2. **qual origem** e referência foram usadas;
3. **quem ou qual serviço** executou a operação;
4. **qual método** foi aplicado;
5. **qual evidência** sustenta o resultado;
6. **qual estado epistêmico** foi atribuído;
7. **qual risco ou defeito** foi observado;
8. **qual próximo passo** é verificável.

Quando a evidência ainda não for suficiente:

```text
estado = TOKEN_VAZIO
claim_allowed = false
contexto = preservado
proximo_passo = verificavel
```

`TOKEN_VAZIO` não é erro, descarte ou conclusão negativa. É um estado útil de
integridade epistêmica.

## 3. Unidade mínima: evento de custódia

O contrato canônico está em:

- `schemas/cadeia_custodia_evento.schema.json`;
- `indices/CADEIA_CUSTODIA_EVENTOS.jsonl`;
- `scripts/validate_chain_of_custody.py`.

Cada linha do ledger JSONL representa um evento imutável. Correções não apagam
o evento anterior: produzem novo evento `CORRECT`, ligado por
`previous_event_id`.

### Campos essenciais

| Campo | Função |
|---|---|
| `event_id` | identidade única e ordenável do evento |
| `timestamp_utc` | tempo normalizado em UTC |
| `repository` / `branch` | localização operacional |
| `actor` | responsável humano, serviço ou automação |
| `operation` | ação realizada |
| `object` | caminho, tipo, tamanho e hashes disponíveis |
| `epistemic_state` | `FATO`, `HIPOTESE`, `SIMBOLICO` ou `TOKEN_VAZIO` |
| `claim_allowed` | trava explícita contra afirmação sem evidência |
| `evidence` | commits, arquivos, hashes, logs, medições ou revisão |
| `controls` | integridade, rastreabilidade e reprodutibilidade |
| `sigma` | fase DMAIC e definição mensurável de defeito |
| `next_verifiable_step` | continuidade objetiva |

## 4. Fluxo operacional

```text
ENTRADA
  ↓ identificação + classificação biblioteconômica
EVENTO INGEST/CLASSIFY
  ↓ ação mínima verificável
TRANSFORM/VALIDATE
  ↓ prova + hash + revisão
PUBLISH/TRANSFER
  ↓ controle e medição
CONTROL
```

Qualquer quebra de evidência desvia o fluxo para `TOKEN_VAZIO`, sem eliminar a
informação parcial.

## 5. Controles de governança

### 5.1 Integridade

- SHA-256 pode ser usado como verificação mínima interoperável.
- BLAKE3 pode ser registrado como hash adicional de alto desempenho.
- Hash ausente deve ser `null`, nunca inventado.
- `event_hash_sha256`, quando presente, cobre o JSON canônico do evento sem o
  próprio campo de hash.

### 5.2 Rastreabilidade

- toda referência deve apontar para commit, arquivo, log, medição ou fonte;
- caminhos devem ser relativos ao repositório e não podem conter `..`;
- um evento que depende de outro deve usar `previous_event_id`;
- exclusões lógicas usam `RETIRE`; o histórico permanece preservado.

### 5.3 Reprodutibilidade

- registrar método, entrada, versão e ambiente quando relevantes;
- preferir validadores determinísticos e dependências mínimas;
- diferenciar validação estrutural de validação científica;
- não declarar conformidade, certificação ou desempenho sem teste reproduzível.

### 5.4 Confidencialidade e minimização

- não registrar segredos, tokens, chaves privadas ou dados pessoais
  desnecessários no ledger;
- usar apenas referências ou identificadores minimizados quando o dado for
  restrito;
- o ledger prova o percurso, não precisa duplicar todo o conteúdo sensível.

## 6. Biblioteconomia aplicada

A cadeia de custódia não substitui catalogação. Ela registra o percurso da obra.
A camada biblioteconômica registra sua identidade, classe, vocabulário e posição
no acervo.

| Biblioteconomia | Cadeia de custódia |
|---|---|
| descrição da obra | evento sobre a obra |
| autoridade de termo | origem e evidência da classificação |
| classificação facetada | contexto operacional |
| remissiva semântica | correção sem apagar histórico |
| catálogo | índice append-only de eventos |

## 7. Six Sigma sem falsa certificação

Neste repositório, “6Sigma” significa uso disciplinado de **DMAIC**, definição de
defeito, linha de base, alvo e controle. Não significa certificação externa nem
afirmação automática de nível sigma.

### Defeitos mensuráveis iniciais

- evento sem origem;
- afirmação liberada sem evidência;
- hash declarado inválido;
- caminho inseguro;
- `TOKEN_VAZIO` sem próximo passo;
- quebra de encadeamento;
- objeto sem classificação ou dono operacional.

### Métricas

```text
completude = campos_validos / campos_obrigatorios
rastreabilidade = eventos_com_evidencia / eventos_totais
integridade = hashes_verificados / hashes_declarados
resolucao_vazio = TOKEN_VAZIO_resolvidos / TOKEN_VAZIO_totais
DPMO = defeitos / oportunidades × 1_000_000
```

O nível sigma só pode ser calculado quando oportunidades, universo, janela e
critério de defeito estiverem definidos e medidos. Antes disso, registrar
`TOKEN_VAZIO`.

## 8. Responsabilidades mínimas

| Papel | Responsabilidade |
|---|---|
| Custodiante do dado | preservar origem, acesso e integridade |
| Curador biblioteconômico | classificar e controlar vocabulário |
| Executor | realizar ação mínima verificável |
| Revisor | verificar evidência, risco e reprodutibilidade |
| Dono do processo | aceitar alvo, risco residual e prioridade |

Uma mesma pessoa pode acumular papéis, mas o evento deve declarar a função
executada e a evidência correspondente.

## 9. Política de adoção

1. começar pelos artefatos P0 e pelos fluxos entre repositórios;
2. registrar eventos novos sem reescrever retroativamente a história;
3. importar legado apenas quando houver origem verificável;
4. medir defeitos antes de otimizar;
5. automatizar somente regras estáveis;
6. manter revisão humana para semântica, risco e autorização de claim.

## 10. Estado de tecnologias futuras

Merkle DAG, assinatura digital, transparência verificável e armazenamento
content-addressed são caminhos coerentes, mas permanecem `TOKEN_VAZIO` até que o
modelo de ameaça, o formato de chave, a rotação, a recuperação e o custo
operacional sejam definidos e testados.

Não usar blockchain apenas como rótulo. A solução deve ser proporcional ao risco
e demonstrar benefício verificável sobre Git, hashes e assinaturas já existentes.
