# RAFAELIA Anchor Loop — autoridade e indexação transversal

**Data da consolidação:** 2026-07-26  
**Estado:** `MERGED_CODE_AND_HISTORY / TOKEN_VAZIO_RUNTIME_DEVICE`

## Correção de interpretação

A classificação anterior “quatro loops sem controle” descrevia corretamente riscos de implementação, mas comprimia indevidamente a função arquitetural.

A interpretação canônica é:

```text
quatro loops históricos
= quatro órgãos de uma âncora de continuidade
```

Os órgãos eram:

```text
PULSAR
⊕ SENTINEL
⊕ MEMORY_STREAM
⊕ ACTION_ORCHESTRATOR
```

A permanência era intencional. O problema não era o loop infinito; eram a falta de supervisor comum, PID/lock, commit, rollback, retenção e separação entre dado JSON e comando shell.

## Autoridades

| Plano | Autoridade | Estado |
|---|---|---|
| Fonte histórica | Google Drive — `RAFAELIA_MASTER_BOOT.sh` | `OBSERVED_HASHED` |
| Arqueologia e preservação | `rafaelmeloreisnovo/X0` — `fb0410cde68ef33f6a07b486b1a9cf91c36feb59` | `MERGED` |
| Runtime operacional | `rafaelmeloreisnovo/home` — `4006e633c510bdea7e900158cf65ba65ea42d578` | `MERGED` |
| Catálogo, significado e gate | `rafaelmeloreisnovo/Mapa` | `CANONICAL_CONTROL_RECORD` |
| Execução física no Android | Moto E7 Power / Termux | `TOKEN_VAZIO_RUNTIME_DEVICE` |

## Fonte histórica

- nome: `RAFAELIA_MASTER_BOOT.sh`;
- tamanho: 2.782 bytes;
- SHA-256: `856334d57a3ca801a69cc78bc7e4b962ee5f4875c05da5b3203d7a4bc79db8e0`;
- conteúdo observado: geração e disparo de quatro scripts persistentes;
- risco confirmado: `eval` de `.next_action`, processos destacados, ausência de estado transacional comum.

## Contrato atual

```text
LOAD
→ OBSERVE
→ VERIFY
→ SNAPSHOT
→ PLAN
→ COMMIT
→ WAIT
```

Invariantes:

1. `COMMIT`, não tempo transcorrido, autoriza o próximo ciclo;
2. `WAIT` é pacing e não clock de estado;
3. uma única instância é mantida por lock e `runit`;
4. PID e status são observáveis;
5. snapshot ocorre somente por mudança e possui retenção limitada;
6. falha em verificação mantém o ciclo canônico anterior;
7. JSON nunca é executado como shell;
8. `next_action` legado é preservado como evidência, mas não executado;
9. `next_action_id` é apenas plano até existir allowlist versionada;
10. `TOKEN_VAZIO` pode ser commitado como observação válida;
11. a primeira leitura fixa a baseline do estado já existente;
12. assinatura diferente da baseline entra em `pending_review`;
13. promoção exige aprovação do SHA-256 exato e nova verificação;
14. auto-commit é desligado por padrão e exige opt-in explícito.

## Fronteira fechada

O significado de “fechado” é:

```text
entrada pode ser observada
→ mudança fica em quarentena
→ assinatura exata precisa ser aprovada
→ fonte é relida e verificada
→ somente então COMMIT
```

Isso preserva a intenção original de impedir entrada direta “lá em cima”, sem transformar o sistema num processo opaco ou impossível de encerrar.

A aprovação operacional é:

```bash
bash ~/RAFAELIA_ANCHOR_LOOP.sh approve <SHA256_DO_CANDIDATO>
```

A aprovação não executa comando nem altera o estado imediatamente; apenas autoriza o próximo ciclo a verificar a mesma assinatura.

## Relações

```text
X0 / história e cópias
        ↓
home / serviço executável
        ↓
Mapa / autoridade, estado e gate
        ↓
Drive / proveniência e cópia editorial
```

Também se relaciona com:

- `SIGIL_SOCKET/.verbo.sock` como canal IPC local;
- `BUFFER/ULTIMO_COMANDO.txt` como memória curta;
- `AUTOCOGNICAO` e triggers como entrada de eventos;
- Omega Kernel como modelo `VERIFY → COMMIT/ROLLBACK`.

## Evidência disponível

- `bash -n` e `sh -n`: `PASS_LOCAL`;
- teste funcional com HOME temporário: baseline, heartbeat sem novo snapshot, quarentena, aprovação exata, commit posterior e não execução de `next_action`: `PASS_LOCAL`;
- workflow remoto: `TOKEN_VAZIO_RUNNER` — terminou antes de qualquer etapa observável e o log retornou `BlobNotFound`;
- serviço real via Termux/runit: `TOKEN_VAZIO_RUNTIME_DEVICE`;
- consumo energético e estabilidade prolongada: `TOKEN_VAZIO_BENCHMARK`;
- integração real com socket histórico: `TOKEN_VAZIO_PROTOCOL`.

## Próximo gate verificável

No aparelho:

```text
sv up rafaelia-anchor
sv status rafaelia-anchor
bash ~/RAFAELIA_ANCHOR_LOOP.sh status
```

Depois observar:

- um único PID;
- incremento de ciclo apenas após commit;
- ausência de filhos órfãos;
- snapshot novo somente quando FUSION/DECISION mudarem;
- mudança isolada como `pending_review`;
- commit somente após aprovação da assinatura exata;
- rollback se a fonte mudar durante a cópia ou antes do commit;
- memória, bateria e wakeups por período prolongado.
