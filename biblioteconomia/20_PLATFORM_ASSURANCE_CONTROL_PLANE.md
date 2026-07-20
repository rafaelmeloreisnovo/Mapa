# Ponteiro do Platform Assurance Control Plane

## Autoridade

O `Mapa` registra localização, versão, maturidade e drift. A lógica de decisão
permanece canônica no `RafGitTools`.

```text
RafGitTools → contrato, work items e gate
Mapa        → ponteiro, dependências e estado observado
```

## Pin atual

```text
producer = rafaelmeloreisnovo/RafGitTools
PR       = #280
merge    = 356c11749fa423bcb458ca399ff39f0155557aa5
index    = configs/platform-assurance/index.json
digest   = e2da04fec6a7334b698a87676c095aba62596a7bdd7777a66f211cccd9621b31
```

O estado materializado é:

```text
6 autoridades
12 work items
5 P0 · 5 P1 · 2 P2
9 bloqueadores abertos
0 promoções prontas
claim_allowed=false
```

## Regra de drift

O ponteiro é imutável para o merge observado. Quando o head produtor divergir,
o consumidor deve retornar `STALE_POINTER`; ele não atualiza automaticamente o
SHA, o digest ou as contagens.

A atualização exige:

1. novo commit imutável do produtor;
2. novo digest do índice;
3. revalidação das contagens;
4. novo selo de integridade do `Mapa`.

## P0

- correção estrutural de Actions no Termux já mesclada, mas limitada;
- loader APK bloqueado até endurecimento de segurança;
- RLL FASE29 bloqueado até correção semântica e de direitos;
- recibo físico do aparelho permanece `TOKEN_VAZIO`;
- execução de CI sem steps/logs permanece bloqueadora.

## Limite

O `Mapa` não copia o algoritmo do control plane, não eleva estados e não
transforma documentação em autorização. Repositório público não é domínio
público; `ZERO_STEP_NO_LOGS` não é PASS nem falha comprovada do código.
