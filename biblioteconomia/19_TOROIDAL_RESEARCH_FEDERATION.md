# Federação do ciclo de pesquisa toroidal — estado 1.1

## Função do Mapa

O `Mapa` registra autoridade, dependência, estado de adaptadores e lacunas de evidência. Ele não executa a ciência, não substitui o runtime e não reescreve a memória.

```text
RafGitTools -> contrato e governança
Mapa        -> autoridade, dependência e maturidade
RLL         -> ciência e falsificadores
RafPolimata -> roteamento e execução formal
Termux      -> runtime Android e recibos de dispositivo
llama       -> memória e consumo delimitado de claims
```

## Estado dos adaptadores

Os seis papéis canônicos possuem artefatos observados e, portanto, estão `ACTIVE` como adaptadores.

```text
ACTIVE adapters        = 6
ADAPTER_PLANNED        = 0
repository TOKEN_VAZIO = 0
open evidence gaps     = 1
claim_allowed          = false
```

`ACTIVE` não significa que toda evidência do domínio esteja completa. Ele significa somente que existe um adaptador identificado, com caminho e localizador de evidência.

## Runtime

O Termux possui o coletor `tools/collect_runtime_receipt_v2.py`, integrado pelo merge `016158c66c1f426aa3b85f23feb456c76c61df3c`.

A prova no aparelho permanece:

```text
device_evidence_state = TOKEN_VAZIO
```

Ela somente fecha com `DEVICE_RECEIPT_COMPLETE`, APK SHA-256, commit produtor, identidade Android, `termux-info`, ABI, kernel e comandos delimitados.

## Memória

O `llamaRafaelia` possui o bundle `data/governance/rll_federated_claim_bundle.v2.json`, integrado pelo merge `68b637fba72d6a8daef65c678615fdfe003ddcae`.

O head do produtor observado pelo conector em 20 de julho de 2026 foi:

```text
8251a7fc71c16ffcc236f981598d4c6684cbdded
```

Ele coincide com o pin imutável do consumidor. Isso permite `SYNCED_BOUNDED`, mas não transfere autoridade científica ao consumidor.

## Invariante

```text
adaptador ativo != prova universal
recibo de CI != prova física
memória sincronizada != ciência confirmada
TOKEN_VAZIO != zero
```
