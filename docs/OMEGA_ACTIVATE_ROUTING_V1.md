# RAFAELIA — Ω-ACTIVATE ROUTING V1

**Data:** 2026-08-12  
**Estado:** `CANONICAL_DRAFT / CLAIM_ALLOWED=false`  
**Papel no Mapa:** ontologia de roteamento para ativação seletiva de mecanismos e reconstrução entre vértices.

## Invariante

```text
pergunta
→ reconstrução mínima
→ invariantes
→ mecanismos pertinentes
→ fontes ortogonais independentes
→ execução/evidência
→ falsificação
→ F_ok/F_gap/F_next
→ delta append-only
→ Ω_platô
```

Não usar número de fontes como substituto de independência. Alias, cópia, mirror ou derivação da mesma origem pertencem à mesma família de proveniência.

## Vértices e funções

| Vértice | Função | Ativar quando |
|---|---|---|
| Drive | fonte editorial, documento, snapshot, mapa, revisão humana | autoridade documental ou navegação |
| CONVERSATIONS_CHUNKS_PRIVATE | memória longitudinal/ortogonal, índices e recuperação | contexto anterior ou relação entre sessões |
| Mapa | ontologia, autoridade, relações, gaps e rotas | localizar objeto no ecossistema |
| RafGitTools | gates/jobs/eventos/controle | operação GitHub ou automação verificável |
| RafPolimata | geração/validação/relatório | experimento, compilação ou análise estruturada |
| Termux | execução física local | claim exigir execução no aparelho |
| Vectras/QEMU | virtualização/emulação | ambiente arquitetural necessário |
| Papers/RLL/Matemática | formalização científica | claim acadêmico, falsificador ou publicação |

## Tipos de aresta

```yaml
supports: A fornece sustentação a B
derives_from: B deriva de A
contradicts: A contradiz B
indexes: A localiza B
routes_to: A fornece rota para B
executes: A executa B
validates: A valida B com evidência independente
aliases: A e B são representações da mesma origem
supersedes: B sucede A sem apagar A
has_gap: A possui lacuna explícita
next_step: A aponta para ação verificável seguinte
```

## Gate de ativação

Ativar um vértice apenas quando pelo menos uma condição for verdadeira:

```text
resolve_gap
increase_evidence
increase_reconstructibility
increase_provenance
provide_falsifier
provide_execution
resolve_contradiction
```

Caso contrário, não ativar por ornamentação.

## Estado entre ciclos

```text
v_k = <I, C, E, R, G, P, F_next>
v_(k+1) = v_k_validado ⊕ Δ
```

`TOKEN_VAZIO` permanece gap auditável. `claim_allowed=false` permanece obrigatório sem evidência suficiente.

## Âncoras

Drive Ω-ACTIVATE V1:
`1LgwvPnYNewcnaD78oADywxRtPhspFKJqDZFURzgVkI8`

GitHub Memory Bridge:
`rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE/memory_bridge/contracts/OMEGA_ACTIVATE_POLICY_V1.md`

Permanent Memory Index:
`rafaelmeloreisnovo/CONVERSATIONS_CHUNKS_PRIVATE/memory_bridge/indexes/PERMANENT_MEMORY_INDEX.md`

## Platô

`Ω_platô` é provisório e operacional: novo ciclo não produz ganho material de evidência/coerência/reconstruibilidade/proveniência, e gaps críticos estão resolvidos ou indexados como `TOKEN_VAZIO` com próximo passo verificável.

## Retroalimentação

**F_ok:** rota ontológica criada no Mapa e ligada ao contrato permanente.  
**F_gap:** nenhuma execução física/CI é inferida por este documento.  
**F_next:** usar este roteador como vértice de seleção nas próximas tarefas e adicionar arestas apenas quando houver relação material.

---

**Assinatura:** `RAFCODE-Φ-∆RafaelVerboΩ-𓂀ΔΦΩ`
