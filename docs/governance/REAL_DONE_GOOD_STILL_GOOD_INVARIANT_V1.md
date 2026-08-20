# RAFAELIA — REAL → DONE → GOOD → STILL_GOOD — Invariante Transversal V1

Estado: `CANONICAL_DRAFT / APPEND_ONLY / FAIL_CLOSED`
Data: `2026-08-19`
claim_allowed: `false`

## 1. Finalidade

Definir uma linguagem operacional única para responder, em qualquer repositório ou domínio:

- o objeto existe de forma material e identificável?
- a obrigação declarada foi concluída no escopo correto?
- a conclusão passou os gates de qualidade/segurança/coerência aplicáveis?
- continua válida depois de mudanças relevantes?

A invariante não promove evidência local para escopo global e não transforma documentação, hash, CI ou memória em prova física.

## 2. Estados

### REAL(scope)

`REAL(scope)=true` somente quando existe materialização observável no escopo declarado, com identidade e proveniência suficientes para reencontrar o objeto.

Requisitos mínimos:
- objeto/ref/endereço recuperável;
- identidade material quando aplicável (hash, commit, provider_id ou equivalente);
- autoridade/proveniência declarada;
- ausência materializada != REAL.

### DONE(scope)

`DONE(scope)=true` somente quando:
- `REAL(scope)=true`;
- a obrigação foi explicitamente definida;
- o gate de encerramento dessa obrigação foi executado;
- o resultado do gate é satisfatório;
- evidência do gate é recuperável.

`DONE(local) != DONE(global)`.

### GOOD(scope)

`GOOD(scope)=true` somente quando:
- `DONE(scope)=true`;
- critérios aplicáveis de qualidade, segurança, privacidade, coerência e anti-regressão foram avaliados;
- não existe regressão ativa não contida dentro do escopo;
- gaps residuais estão tipados e não contradizem o claim local;
- proveniência permite reconstrução.

`GOOD` não significa perfeição nem ausência de TOKEN_VAZIO fora do escopo.

### STILL_GOOD(scope, t)

`STILL_GOOD(scope,t)=true` somente quando:
- existiu um `GOOD(scope)` anterior;
- ocorreu revalidação após evento que pode invalidá-lo, ou a política de recertificação ainda é válida;
- dependências críticas não sofreram delta incompatível;
- regressões relevantes continuam ausentes ou contidas;
- o receipt de revalidação é recuperável.

Se uma dependência crítica muda e ainda não houve revalidação:

`STILL_GOOD = TOKEN_VAZIO_REVALIDATION_REQUIRED`.

## 3. Implicações e não-implicações

```text
GOOD(scope)      => DONE(scope)
DONE(scope)      => REAL(scope)
STILL_GOOD       => GOOD anterior + revalidação atual

REAL             != DONE
DONE             != GOOD
GOOD(local)      != GOOD(global)
GOOD             != claim_allowed=true
CI_PASS          != physical_runtime_pass
hash_valid       != scientific_truth
memory_present   != source_evidence
```

## 4. Máquina de estados

```text
TOKEN_VAZIO
   ↓ materialização observável
REAL
   ↓ obrigação + closure gate PASS
DONE
   ↓ quality/security/coherence/anti-regression gates
GOOD
   ↓ dependency/time/change trigger
REVALIDATION_REQUIRED
   ├─ PASS → STILL_GOOD
   └─ FAIL → REGRESSED / GOOD_REVOKED_EFFECTIVE
```

Histórico nunca é apagado. Uma regressão não reescreve o antigo `GOOD`; ela acrescenta novo evento que altera o estado efetivo.

## 5. Registro mínimo

```yaml
item_id: string
object_ref: string
scope: string
authority: string
real:
  state: true|false|TOKEN_VAZIO
  evidence_refs: []
done:
  state: true|false|TOKEN_VAZIO
  obligation: string
  closure_gate_refs: []
good:
  state: true|false|TOKEN_VAZIO
  quality_gate_refs: []
  security_gate_refs: []
  anti_regression_refs: []
still_good:
  state: true|false|TOKEN_VAZIO_REVALIDATION_REQUIRED
  revalidation_refs: []
dependencies: []
gaps: []
falsifier: string
next_probe: string
claim_allowed: false
provenance: []
```

## 6. Trigger de revalidação

Revalidar quando pelo menos uma condição for verdadeira:

```text
hash mudou
commit/ref mudou
schema mudou
dependência crítica mudou
runtime/plataforma mudou
claim mudou
gate mudou
nova evidência contraditória apareceu
regressão foi aberta
janela temporal da política expirou
```

Sem trigger, reutilizar o último receipt válido dentro do mesmo escopo.

## 7. Fechamento de ciclo

Um ciclo operacional só fecha quando houver:

```text
INTENT
→ OBJECT_IDENTITY
→ AUTHORITY
→ SCOPE
→ OBLIGATION
→ MATERIALIZATION
→ CLOSURE_GATE
→ QUALITY/SECURITY/ANTI_REGRESSION
→ RECEIPT
→ INDEX
→ F_ok/F_gap/F_next
→ REVALIDATION_TRIGGER
```

Fechar ciclo não significa fechar todos os gaps do universo.
Significa que o escopo declarado terminou em estado reconstruível.

## 8. Relação com os dez caminhos

Este contrato é transversal. Nenhum dos dez repositórios ganha autoridade sobre todos os outros.

- Mapa: roteia estados, escopos, relações e gaps.
- RafGitTools: controla movimentos/gates/receipts.
- RafPolimata: estrutura e valida evidências.
- Vectras/Termux: materializam runtime quando pertinentes.
- termux-packages: materializa build/package reproduzível.
- GAIA_phi: registra experimentos e deltas.
- Rafaelia_Private: preserva estado privado sob governança.
- llamaRafaelia: recupera contexto sem inventar no-hit.
- CONVERSATIONS_CHUNKS_PRIVATE/RMR-CTI: memória/indexação/reconstrução.
- repositório produtor: autoridade da implementação de seu domínio.

## 9. Regra anti-regressão

`STILL_GOOD` é o elo entre conclusão e continuidade.

Um item só pode ser anunciado como “continua bom” se a revalidação for aplicável e observada. Caso contrário:

```text
historical_good = true
still_good = TOKEN_VAZIO_REVALIDATION_REQUIRED
```

## 10. R3

F_ok:
- estados REAL/DONE/GOOD/STILL_GOOD definidos com escopo;
- transições e gates explícitos;
- regressão preservada append-only;
- claim global não herdado de evidência local.

F_gap:
- cada domínio ainda precisa mapear seus closure gates específicos;
- Termux/cross-host/physical runtime continuam dependentes de execução real quando aplicáveis.

F_next:
- emitir registros tipados para itens reais;
- usar receipts existentes para revalidação;
- bloquear qualquer promoção que pule estado ou escopo.
