# Fronteira de Segurança para Runtimes Legados RAFAELIA

## Estado

`LEGACY_REVIEW / QUARANTINED / NOT_FOR_DEPLOYMENT`

## Origem

O acervo histórico contém módulos denominados Mutante Core, Terminal Ext, Watchdog, Cluster Net, Web Bridge, Bot Bridge, Embedded AI e Local API. Eles preservam ideias úteis de estado, backup, observabilidade, notificação e integração local, mas alguns exemplos não possuem controles mínimos para uso real.

## Componentes aproveitáveis

- persistência simples de estado;
- logs e timestamps;
- backup versionado;
- watchdog com política de reinício limitada;
- detecção de engine local;
- notificação local;
- API de leitura restrita a loopback;
- classificação explícita de fallback e TOKEN_VAZIO.

## Padrões bloqueados

Os seguintes padrões permanecem proibidos fora de laboratório isolado:

```text
HTTP/TCP bind em 0.0.0.0 sem autenticação e TLS
endpoint /run ou bot /run que executa shell arbitrário
os.popen(), eval() ou shell=True com entrada remota
upload usando filename não sanitizado
GET/SEND de arquivo sem normalização de caminho
broadcast UDP como mecanismo de confiança
state.json sobrescrito sem lock, schema, backup atômico ou digest
watchdog infinito sem backoff, limite e circuit breaker
limpeza destrutiva por find -exec rm sem dry-run/allowlist
fallback simulado apresentado como inferência real
OCR/voz em serviço externo descrito como operação offline
segredos, tokens ou webhooks em arquivo, log ou repositório
```

## Classificação inicial

| Módulo histórico | Estado | Motivo | Rota segura |
|---|---|---|---|
| Mutante Core | `RESEARCH_ONLY` | aprendizado alegado sem contrato de modelo/métrica | definir eventos, política e testes determinísticos |
| Fractal Comp | `CLAIM_BLOCKED` | hash reversível, CRC inteligente e compressão exigem especificação e benchmark | separar indexação, integridade e compressão real |
| Terminal Ext | `PARTIAL` | funções úteis, mas limpeza e escrita de estado precisam fail-safe | atomic write, dry-run e retenção configurável |
| Watchdog Autocorr | `PARTIAL` | reinício e correção sem circuit breaker podem criar loop | backoff, max retries, lock e rollback |
| Cluster Net | `QUARANTINED` | transferência sem autenticação, integridade ou path safety | protocolo autenticado, allowlist e digest |
| Web Bridge | `QUARANTINED` | escrita/upload/trigger sem autenticação | loopback, token local, CSRF, limites e schema |
| Bot Bridge | `BLOCKED` | execução remota arbitrária por chat/webhook | remover comando shell; usar catálogo fixo de ações |
| Embedded AI | `EXPERIMENTAL` | caminhos fixos e fallback reverso não são IA | engine registry, modelo verificado e estado TOKEN_VAZIO |
| Local API | `BLOCKED` | `/run` remoto, shell=True e bind público | excluir `/run`; autenticar; executar somente ações tipadas |

## Contrato para reativação

Um módulo só sai de quarentena quando tiver:

```text
threat model
owner
input schema
output schema
authentication/authorization
path normalization
resource limits
timeout
rate limit
atomic state handling
audit log without secrets
negative tests
rollback
runtime evidence
```

## Regra final

Código histórico é evidência de evolução e pode ser preservado. Preservação não significa autorização de implantação. Na dúvida, `TOKEN_VAZIO` e `claim_allowed=false`.
