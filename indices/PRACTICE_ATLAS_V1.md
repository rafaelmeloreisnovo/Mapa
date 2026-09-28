# Practice ATLAS V1 — humano + IA

**Estado:** `IMPLEMENTED_UNTESTED`  
**claim_allowed:** `false`

## Objetivo

Reduzir o caminho de reconstrução do ecossistema para:

```text
INTENT
→ AUTHORITY
→ SOURCE_MIN (<=3)
→ EXECUTION_TARGET
→ EVIDENCE_RULE
→ GAP
→ NEXT
```

O arquivo de máquina é `data/control-plane/PRACTICE_ATLAS_V1.json`.

## Regra de leitura

Comece com no máximo **3 raízes**, profundidade 1. Expanda apenas por
`missing_source | contradiction | unresolved_authority | missing_evidence | explicit_request`.

Não copie corpus para o ATLAS. O ATLAS contém **ponteiros tipados**.

## Fórmulas e símbolos

- `sqrt(3)/2` é uma razão geométrica; `sqrt(3/2)` é outra quantidade.
- A rota Spiral√3/2 já possui execução limitada para a recorrência radial.
- A lei angular `pi/phi` não deve ser fundida automaticamente com geradores que usam outro passo angular.
- Fibonacci, Tribonacci e Trinity633 permanecem separados até haver contrato formal comum e vetores de referência.
- `φ`, `π`, `633`, `42`, emojis e selos podem ser endereços semânticos; não substituem prova.

## ZIPRAF Ω

O Drive contém `ZIPRAF_OMEGA_FULL_DO_it_ativar.txt`. A leitura observada mostra que ele é um
**manifesto curto de ativação/assinatura**, não a especificação executável do formato.

A ponte técnica observada para ZIPRAF Bit Layer preserva:

```text
RafPolimata = autoridade matemática/spec/ABI
RafGitTools = inspector/debug adapter
Vectras     = raster/framebuffer adapter
Termux      = block/decoder adapter
Mapa        = roteamento federado
```

O ponteiro privado do Drive não é replicado aqui.

## Como contribuir

1. Escolha uma `area.id`.
2. Leia somente `source_min`.
3. Resolva `authority`. Se estiver `TOKEN_VAZIO`, pare antes de mutação.
4. Execute o menor gate que pode falsificar a mudança.
5. Registre evidência vinculada a commit/artefato/ambiente.
6. Atualize `gap` e `next`; não transforme documentação em PASS.

## Comentários em código

Comentários novos devem explicar **fronteiras**, não narrar sintaxe óbvia. Para APIs/rotas públicas,
prefira um bloco curto contendo, quando útil:

```text
ROLE:
AUTHORITY:
INPUT:
OUTPUT:
INVARIANT:
EVIDENCE:
FAIL_CLOSED:
SEE:
```

Não adicionar esse cabeçalho mecanicamente a todo arquivo. Use somente onde reduz ambiguidade para
humano/IA.

## Validação

```bash
python3 tools/audit/validate_practice_atlas_v1.py \
  data/control-plane/PRACTICE_ATLAS_V1.json
```

Até essa execução existir para o commit atual:

```text
atlas_state = IMPLEMENTED_UNTESTED
claim_allowed = false
```

## R3

**F_ok:** ATLAS tipado criado para 12 áreas e ligado às autoridades já observadas.  
**F_gap:** autoridade combinada Fibonacci/Tribonacci e Trinity633 permanece `TOKEN_VAZIO`; validação do commit atual ainda não executada.  
**F_next:** executar o validator e consumir o ATLAS a partir dos adapters locais de RafGitTools/RafPolimata.
