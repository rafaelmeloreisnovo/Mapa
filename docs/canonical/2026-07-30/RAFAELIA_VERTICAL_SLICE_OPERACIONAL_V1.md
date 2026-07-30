# RAFAELIA — Fatia Vertical Operacional V1

**Evento:** `RAFAELIA-VERTICAL-SLICE-V1-20260730T041200Z`  
**Política:** append-only, não destrutiva, `claim_allowed=false`  
**Invariante:** `Ideia != Implementação != Execução != Evidência != Claim`

## Circuito materializado

```text
SRC -> CLAIM -> RUN -> RECEIPT -> DECISION -> MAPA
```

A fatia foi executada sobre nove fontes presentes na sessão:

- um APK Termux;
- uma exportação ZIP de conversas;
- sete imagens PNG RAFAELIA.

## Evidência delimitada

A execução de referência verificou:

1. SHA-256 dos nove artefatos;
2. presença de `libtermux.so` e `libtermux-bootstrap.so` nas ABIs `arm64-v8a`, `armeabi-v7a`, `x86` e `x86_64`;
3. integridade e conjunto de cinco arquivos-raiz da exportação ZIP;
4. assinatura PNG e dimensões IHDR das sete imagens;
5. geração de um receipt, três decisões limitadas, entidades, relações e métricas.

Resultado do runtime de referência: `PASS`, 9/9 fontes, 3/3 claims estruturais, zero divergências de hash.

## Limites

- runtime executado: `CONTAINER_REFERENCE`, não Android/Termux;
- revisão humana independente: `TOKEN_VAZIO_HUMAN_REVIEW_PENDING`;
- replicação Termux: `TOKEN_VAZIO_RUNTIME_NOT_EXECUTED`;
- publicação científica ou prontidão de produção: bloqueadas;
- o resultado não interpreta semanticamente as imagens e não produz claim cosmológico.

## Maturidade

```text
S0 ideia registrada                 PASS
S1 schema definido                  PASS
S2 implementação mínima             PASS
S3 testes locais                    PASS
S4 receipt reproduzível referência  PASS
S5 revisão independente             TOKEN_VAZIO
S6 integração operacional Termux    TOKEN_VAZIO
S7 release estável                  TOKEN_VAZIO
```

## Autoridades federadas

- Drive: memória longitudinal e custódia editorial;
- Mapa: ontologia, identidade, estado e dependências;
- RafGitTools: controle, preflight, dry-run e autorização;
- RafPolimata: testes, métricas, erratas e receipts;
- RLL: falsificação científica `D x B x M x F x R`;
- papers: síntese, limites, referências e ledger de claims;
- Termux: execução Android local e receipt de ambiente.

## Gates fail-closed

- hash incompatível -> `REFUTADO`;
- fonte ausente -> `TOKEN_VAZIO_SOURCE_UNAVAILABLE`;
- falsificador ausente -> bloqueio;
- receipt ausente -> promoção bloqueada;
- revisão humana pendente -> `claim_allowed=false`;
- CI ausente -> nunca converter em PASS.

## Próximo passo verificável

Executar o mesmo pacote no Termux, vincular o receipt ao commit exato desta branch, obter revisão humana independente e só então avaliar promoção para S5/S6.

## R3

- `F_ok`: autoridade, inventário, schemas, runner, gates, receipt, decisões, grafo e métricas materializados.
- `F_gap`: replicação Android, CI remoto, revisão independente e merge canônico.
- `F_next`: publicar adaptadores mínimos por repositório, registrar o evento no Drive e executar no Termux.
