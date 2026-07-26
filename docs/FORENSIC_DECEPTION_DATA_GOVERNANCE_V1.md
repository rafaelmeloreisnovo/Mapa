# RAFAELIA — Arquitetura de Governança, Decepção e Custódia Forense de Dados V1

Estado: `CANONICAL_DRAFT`  
Autoridade: `Mapa` como plano de controle e ontologia; execução permanece nos repositórios produtores.  
Claim boundary: `claim_allowed=false` até experimentos, revisão jurídica e gates reproduzíveis.

## 1. Problema

Uma arquitetura de dados de alta governança precisa responder simultaneamente:

1. qual é o dado empresarial verdadeiro;
2. quem pode visualizar, alterar, aprovar ou exportar cada elemento;
3. de qual estação, usuário, época e distribuição veio uma cópia;
4. se o material encontrado foi alterado, recortado, reordenado ou combinado;
5. como reduzir o valor de um vazamento sem contaminar a operação legítima;
6. como preservar prova, rollback e falsificabilidade.

O sistema não trata um banco como um arquivo isolado. Ele trata o conjunto como um grafo temporal:

```text
registros + relações + políticas + estação + usuário + época + execução + evidência
```

## 2. Separação obrigatória dos cinco planos

A arquitetura é composta por cinco matrizes lógicas:

```text
M_C — CANONICAL: verdade operacional e jurídica
M_D — DECEPTION: dados sintéticos, honeyrecords e rotas instrumentadas
M_F — FINGERPRINT: projeções, codewords, blocos e marcas por destinatário
M_R — RUNTIME: memória efêmera, criptografia, buffers e reconstrução mínima
M_A — AUDIT: eventos, manifestos, hashes, recibos e cadeia de custódia
```

Invariante de isolamento:

```text
M_D não produz efeitos em M_C.
```

Dados de decepção não podem:

- emitir documento fiscal;
- alterar estoque, saldo ou contabilidade;
- conceder autorização;
- alimentar decisão empresarial real;
- representar pessoa real sem base jurídica explícita;
- aparecer silenciosamente para um usuário legítimo como se fossem verdade.

O acesso negado continua sendo negado. A decepção ocorre somente em superfícies deliberadamente instrumentadas.

## 3. Grafo canônico e projeção por estação

O banco canônico é modelado por:

```text
G0 = (V, E, A)
```

- `V`: registros, usuários, estações, documentos e eventos;
- `E`: chaves, dependências, autoria, derivação e sincronização;
- `A`: valores, políticas, versões e estados.

Para cada contexto de distribuição:

```text
R = (tenant, estação, escopo de usuário, schema, época)
```

é criada uma projeção:

```text
GR = F(K, R, G0)
```

A projeção pode coordenar, dentro de limites demonstrados:

- identificadores locais não jurídicos;
- ranking lógico derivado de CEP, nome e identificador canônico normalizados;
- divisão em blocos;
- cadência de autoenumeração;
- índices auxiliares;
- aliases e metadados visuais;
- codeword redundante por estação/época.

### Invariante semântica

Toda consulta empresarial canônica deve preservar o resultado:

```text
BusinessQuery(G0) == BusinessQuery(GR sem decoys)
```

Qualquer divergência é `FAIL`.

### Identidade dupla

```text
CID — identidade canônica, estável e interoperável
FID — identidade projetada, local e forense
```

A identidade fiscal, jurídica ou de integração nunca depende exclusivamente de `FID`.

## 4. CEP, nomes e ordenações

CEP, nome, data ou outro atributo não são automaticamente o identificador. Podem ser coordenadas de uma ordenação canônica ou de uma função keyed:

```text
rank = ORDER_BY(HMAC(KR, normalize(CEP) || normalize(nome) || CID))
```

A ordem física de páginas ou linhas não é prova. Dumps, restores e otimizadores podem alterá-la. A recuperação deve depender de ordem lógica reproduzível, relações e manifestos.

## 5. Fingerprint vetorizado e redundância

A identidade do contexto é reduzida a um fingerprint:

```text
F_R = H(tenant || estação || usuário || schema || época)
C_R = ECC(F_R)
```

Os símbolos de `C_R` podem ser distribuídos entre canais independentes:

```text
IDs projetados
cadência entre IDs
blocos lógicos
relações pai/filho
índices auxiliares
metadados de interface
marcas de exportação
decoys instrumentados
```

Nenhum canal isolado deve ser tratado como atribuição conclusiva. A recuperação combina símbolos sobreviventes e calcula confiança, colisão e falso positivo.

O laboratório V1 usa código de repetição apenas como demonstrador. Códigos robustos, resistência a conluio e ECC de produção permanecem `TOKEN_VAZIO`.

## 6. Plano de decepção

Um decoy válido precisa satisfazer:

```text
plausibilidade + coerência relacional + inutilidade operacional + rastreabilidade
```

Tipos permitidos no laboratório:

- `HONEY_RECORD`: registro sintético atrativo;
- `HONEY_TABLE`: tabela sem dependência produtiva;
- `CANARY_IDENTIFIER`: identificador sem autoridade externa;
- `DECOY_EXPORT`: pacote sintético marcado;
- `DECOY_ROUTE`: consulta instrumentada e isolada.

Regras:

1. somente dados sintéticos;
2. nenhum segredo ou credencial funcional;
3. nenhum callback ofensivo ou hack-back;
4. toque no decoy gera evento de auditoria, não acusação automática;
5. resposta automática limita-se a negar, registrar, revogar sessão conforme política aprovada ou elevar inspeção;
6. identidade humana só pode ser atribuída com evidências independentes e cadeia de custódia.

## 7. ABAC e responsabilidade por campo

A decisão de acesso é função de atributos:

```text
Decision = f(sujeito, objeto, ação, ambiente, finalidade, época)
```

Exemplos de ações:

```text
view | edit | approve | export | reposition | decrypt
```

A interface orienta; o banco e o plano de política garantem. Ocultar um campo no Delphi/Android não substitui autorização server-side.

## 8. Proveniência

O modelo segue a separação:

```text
Entity  — registro, arquivo, relatório, manifesto ou resultado
Activity — criar, transformar, consultar, exportar, sincronizar ou reindexar
Agent — usuário, estação, serviço ou organização
```

Cada evento relevante registra, quando aplicável:

```text
event_id
agent_id
activity_type
entity_id
station_id
session_id
epoch_id
policy_version
input_root
output_root
previous_event_hash
timestamp
result
```

## 9. Reindexação como rotação de época

Reindexação física não redefine a verdade. Uma rotação controlada cria nova época:

```text
E_n --signed checkpoint--> E_n+1
```

O checkpoint anterior preserva:

- raiz canônica;
- raiz da projeção;
- hash do inventário de decoys;
- codeword commitment;
- versão do schema e da política;
- última sequência;
- timestamp;
- assinatura ou autenticação aprovada.

O mapa de transformação antigo permanece read-only durante o prazo de custódia.

## 10. Proteção de runtime

A arquitetura distingue:

- criptografia em trânsito;
- criptografia em repouso;
- criptografia de campo/client-side;
- representação fragmentada ou mascarada;
- memória confidencial suportada por hardware;
- minimização do tempo de plaintext.

Software comum não elimina toda representação semanticamente recuperável durante o processamento. A alegação de segredo absoluto em runtime permanece bloqueada.

Princípios:

```text
modelo sugere
política autoriza
kernel determinístico verifica
```

## 11. Concorrência e multitarefa

Anéis de execução:

```text
R0 integridade: validar -> transacionar -> recibo/hash
R1 interação: UI, consulta, edição e navegação
R2 inteligência: vetores, grafos e classificação
R3 manutenção: sync, backup, reindexação e relatórios
```

`R0` não pode ser interrompido ou reordenado por política adaptativa. Ajustes de fila, batch, cache e prioridade ficam dentro de envelope seguro, com métricas e rollback.

## 12. Responsabilidade federada

| Repositório | Autoridade |
|---|---|
| `Mapa` | ontologia, estados, contratos, dependências e limites |
| `papers` | revisão científica, claims, referências, falsificadores e limitações |
| `RafPolimata` | laboratório sintético, validadores, relatórios e evidence runs |
| `RafGitTools` | plano de controle, jobs, gates, aprovação e rollback |
| banco/runtime produtor | implementação real, transações e métricas locais |
| `Vectra`/memória | recuperação vetorial e candidatos; não decisão final |

## 13. Gates mínimos

```text
G0 schema válido
G1 isolamento CANONICAL/DECEPTION
G2 preservação de consultas empresariais
G3 unicidade e integridade das projeções
G4 manifesto autenticado
G5 recuperação sob subset/reorder/strip
G6 taxa de falso positivo medida
G7 resistência a correlação e conluio
G8 overhead p50/p95/p99 medido
G9 revisão jurídica e privacidade
G10 rollback e custódia verificados
```

Nenhum commit isolado fecha esses gates.

## 14. Falsificadores

A proposta falha, total ou parcialmente, se:

- decoys contaminarem resultados canônicos;
- uma projeção quebrar FK ou integração;
- duas estações apresentarem colisão acima do limite aceito;
- o detector atribuir fonte incorreta em amostra adversarial;
- reindexação impedir reconstrução de época anterior;
- a marca puder ser removida sem custo e sem perda observável;
- o overhead inviabilizar o workload;
- usuários legítimos forem enganados fora das superfícies aprovadas;
- a cadeia de custódia puder ser fabricada retroativamente.

## 15. Estado epistemológico

| Claim | Estado |
|---|---|
| separação dos cinco planos | `REFERENCE` |
| simulador sintético V1 | `IMPLEMENTED` no produtor, execução local limitada |
| atribuição forense de produção | `TOKEN_VAZIO` |
| ECC robusto e resistência a conluio | `TOKEN_VAZIO` |
| proteção integral de memória | `TOKEN_VAZIO` |
| equivalência com plataforma empresarial global | `NOT_CLAIMED` |
| conformidade jurídica | `LEGAL_REVIEW_REQUIRED` |

## 16. Próximo passo verificável

Executar o laboratório sintético no `RafPolimata`, registrar ambiente, comando, stdout/stderr e hashes; depois ampliar o teste para ataques de subset, correlação, união de cópias e rotação de época.

---

`F_ok`: arquitetura separada por verdade, decepção, fingerprint, runtime e auditoria.  
`F_gap`: robustez, atribuição, custo e conformidade ainda não demonstrados.  
`F_next`: evidence run sintético reproduzível e claims ledger atualizado.
