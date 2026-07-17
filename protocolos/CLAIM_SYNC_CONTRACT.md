# Contrato de Sincronização de Claims Cross-Repo

## Estado

`v1 / FAIL_CLOSED / claim_allowed=false`

## Problema

Quando uma conclusão é copiada de um repositório produtor para um consumidor, ela pode continuar circulando após o produtor registrar nova evidência, contradição ou resultado negativo. O contrato impede essa divergência silenciosa.

## Papéis

- **Producer**: proprietário canônico do domínio da alegação.
- **Consumer**: repositório que recupera, explica, executa ou traduz a alegação.
- **Control plane**: `Mapa`, que registra autoridade e divergências sem substituir o produtor.

## Envelope mínimo

```json
{
  "claim_id": "C-DOMAIN-001",
  "producer": "owner/repository",
  "source_path": "path/to/artifact.json",
  "source_ref": "commit-or-tag",
  "source_digest": "sha256-or-TOKEN_VAZIO",
  "state": "VERIFIED|VERIFIED_LIMITED|DECLARED_BY_AUTHOR|HYPOTHESIS|TOKEN_VAZIO|CONTRADICTION",
  "scope": "leitura estreita e verificável",
  "not_claimed": ["leituras bloqueadas"],
  "observed_at": "RFC3339",
  "claim_allowed": false
}
```

## Regras bloqueantes

1. `producer`, `source_path`, `source_ref`, `state` e `scope` são obrigatórios.
2. `source_digest=TOKEN_VAZIO` mantém `claim_allowed=false`.
3. Um consumidor não pode elevar o estado recebido.
4. `VERIFIED` é sempre limitado ao escopo declarado; não significa verdade universal.
5. Resultado negativo ou contradição não pode ser apagado por atualização editorial.
6. Se o produtor mudar depois do `source_ref`, o consumidor entra em `STALE_CONSUMER` até nova sincronização.
7. Texto didático, parábola ou explicação gerada deve carregar o mesmo limite do claim de origem.
8. Dados sintéticos não podem alimentar claims rotulados como dados reais.

## Detecção de drift

```text
producer.current_ref != consumer.pinned_ref
  -> STALE_CONSUMER

producer.state == CONTRADICTION and consumer.state in {VERIFIED, DECLARED_BY_AUTHOR}
  -> CONTRADICTION

consumer.scope broader than producer.scope
  -> CLAIM_BLOCKED

missing producer artifact
  -> TOKEN_VAZIO
```

## Política de atualização

```text
fetch producer export
-> validate schema
-> verify ref/path/digest
-> compare state and scope
-> record divergence
-> update consumer pin
-> run consumer tests
-> emit synchronization artifact
```

## Primeira aplicação

A primeira relação a usar este contrato é:

```text
relativity-living-light (producer de claims RLL)
  -> llamaRafaelia (consumer de contexto e explicação)
  -> Mapa (registro de autoridade e drift)
```

## Limite

Este contrato organiza transmissão de evidência; ele não certifica o conteúdo científico, criptográfico, jurídico ou operacional transmitido.
