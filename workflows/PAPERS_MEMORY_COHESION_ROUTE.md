# Papers Memory Cohesion Federated Route

## Estado

`v1 / ACTIVE_PRIVATE / claim_allowed=false`

## Papéis

```text
Vectras-VM-Android
  = autoridade do código observado

papers
  = produtor das unidades de memória científica e dos falsificadores

Mapa
  = control plane de autoridade, coesão, dependências e drift
```

O `Mapa` não copia o código nem eleva o estado científico. Ele fixa o commit produtor,
registra a unidade, aponta o artefato canônico e bloqueia conclusões mais amplas que a
fonte.

## Rota

```text
código fixado no Vectras
→ leitura limitada por arquivo e blob
→ unidade RMU no papers
→ validação fail-closed no papers
→ ponte fixada no Mapa
→ validação de autoridade e drift
→ próxima ação no repositório competente
```

## Unidades iniciais

| Unidade | Assunto | Estado permitido |
|---|---|---|
| `RMU-LAYERSBIT4096-001` | 512 bytes físicos, 4.096 bits internos e fold de 256 bits | implementação documentada; execução e exportação total ainda limitadas |
| `RMU-PRIORITY-ADMISSION-001` | prioridade de polling versus admissão sob saturação | code review; receipt de descarte não localizado |
| `RMU-ERASURE-RECOVERY-001` | recuperação geométrica e perda parcial | hipótese; teste unitário atual remove um nó por vez |

## Contrato de memória

O Mapa trata cada unidade por três eixos independentes:

```text
material_state
semantic_state
operational_state
```

Isso impede compressões incorretas como:

```text
empty = absent = error = blocked
```

## Contrato de erro

Erro pode ser registrado como ameaça, sinal, resíduo, paridade, divergência, rota ou
degradação. O papel informacional não remove o dever de integridade.

O plano de controle deve preservar:

- origem;
- posição;
- relação;
- prioridade;
- admission policy;
- receipt policy;
- evidência;
- falsificadores;
- estado negativo;
- `TOKEN_VAZIO`.

## Drift

A ponte entra em `STALE` quando:

```text
papers.current_ref != registry.producer_ref
```

Ela entra em `CONTRADICTION` quando o produtor registra contradição ou quando o escopo
do Mapa excede o escopo da unidade.

Um digest de conteúdo ainda vazio não impede a indexação quando o blob Git e o commit
estão fixados, mas mantém `claim_allowed=false` e exige preenchimento posterior do
SHA-256.

## Próximas execuções permitidas

1. corrigir o overwrite potencial de `lb_zero` no repositório do código;
2. criar exportação opcional das 16 camadas sem substituir o fold;
3. implementar admission control por prioridade com receipt determinístico;
4. separar consenso total de conflito triplo;
5. criar teste de erasure com máscaras de 0% a 45%;
6. validar reconstrução por digest, não apenas conectividade;
7. registrar desgaste físico por endereço somente quando houver fonte de hardware.

## Limite

Este workflow cria coesão e memória auditável. Ele não modifica o Vectras, não prova
resistência a 45%, não demonstra vida útil de memória e não autoriza claim de
superioridade.