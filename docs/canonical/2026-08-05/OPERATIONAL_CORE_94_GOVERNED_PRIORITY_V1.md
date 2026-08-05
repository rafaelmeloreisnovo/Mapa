# RAFAELIA — Núcleo Operacional 94: prioridade governada V1

**Evento:** `OPCORE94-20260805T1943-0300`  
**Modo:** append-only, não destrutivo, fail-closed  
**Claim:** `claim_allowed=false`

## Resultado desta etapa

O total **94** é preservado como fronteira reportada pela auditoria anterior. A fonte que individualiza os 94 objetos não está disponível na evidência corrente; portanto, o sistema não fabrica os 78 nomes ausentes.

```text
expected_total   = 94
identified       = 16
unitemized       = 78
unitemized_state = TOKEN_VAZIO_ITEMIZATION_PENDING
```

Os 16 objetos identificáveis foram ligados aos cinco eixos obrigatórios:

```text
fonte
→ teste
→ ambiente
→ receipt
→ função no ecossistema
```

Cada eixo carrega o estado mais forte atualmente sustentado. Ausência de teste ou receipt não foi convertida em reprovação nem aprovação.

## Fila inicial

- **P0:** autoridade longitudinal, ciclo de catálogo e fatia vertical operacional.
- **P1:** seis documentos-âncora do `rmrCti`, com provider ID conhecido e reprodução ainda pendente.
- **P2:** outputs observados e o arquivo vazio `zone53.txt`, ainda sem linhagem completa.
- **TV:** `OC94-017` até `OC94-094`, bloqueados até localização da fonte individualizadora.

## Regra de promoção

Um objeto somente deixa o intervalo `TOKEN_VAZIO_ITEMIZATION_PENDING` quando possuir, no mínimo:

1. identidade de fonte verificável;
2. título não inferido;
3. função delimitada por documento, código ou contexto;
4. estado explícito de teste;
5. ambiente declarado;
6. receipt existente ou lacuna tipada.

## Execução local de referência

```bash
python3 scripts/validate_operational_core_94.py \
  data/core/operational-core-94.v1.json
python3 -m unittest discover -s tests -p 'test_operational_core_94.py' -v
```

O validador bloqueia:

- IDs duplicados;
- contagem que não fecha 94;
- ausência de qualquer um dos cinco eixos;
- promoção de `claim_allowed`;
- intervalo de vazios incoerente.

## Próxima porta

```text
localizar fonte dos 94
→ individualizar sem inferir
→ resolver provider IDs e hashes P2
→ ler integralmente os seis anchors P1
→ reproduzir testes/ambientes
→ emitir receipt sucessor
```

## R3

- **F_ok:** fronteira 94 preservada; 16 objetos conectados; fila P0/P1/P2 materializada; validador fail-closed criado.
- **F_gap:** 78 objetos sem individualização; hashes de bytes e receipts incompletos; Termux físico pendente.
- **F_next:** localizar o artefato-fonte do 94 e fechar primeiro os três P0, sem tocar em duplicatas fora do núcleo.
