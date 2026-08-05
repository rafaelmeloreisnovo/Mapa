# RAFAELIA — P0-01 Promotion Control V1

**Estado:** IMPLEMENTADO_EM_BRANCH / `claim_allowed=false`  
**Modo:** fail-closed, manual-merge-only, append-only por commits  
**Escopo:** pull requests do repositório `Mapa`

## F_ok

O `Integral Gate V1` já valida receipts e nega promoção quando critérios técnicos
não estão em `PASS`. Porém, esse gate não lia diretamente o estado vivo da pull
request, seus reviews ou declarações explícitas de “não mesclar”.

## F_gap fechado neste delta

Foi materializado um controle independente que:

1. nega PR em draft ou com estado ambíguo;
2. nega auto-merge habilitado;
3. nega declarações explícitas como `promotion=DENIED`,
   `READY_FOR_GRAPH=false`, “não mesclar” e “manter PR draft”;
4. exige aprovação humana independente quando o corpo declara
   `human_review_required=true` ou equivalente;
5. ignora aprovação do próprio autor e contas terminadas em `[bot]`;
6. considera apenas o review mais recente de cada ator;
7. falha fechado quando evento, policy ou reviews são ilegíveis;
8. produz resultado JSON estruturado e código de saída distinto para
   `ALLOWED`, `DENIED` e entrada inválida.

## Gates executáveis

```sh
python -m py_compile \
  tools/verify_promotion_control.py \
  tests/test_promotion_control.py

python tests/test_promotion_control.py
```

O workflow `RAFAELIA Promotion Control V1` executa os testes negativos e consulta
os reviews da PR com permissão somente-leitura.

## Limites preservados

- A existência do workflow não prova que o check esteja configurado como
  **required status check** na proteção da branch.
- O controle não atribui causalidade a merges passados.
- O controle não substitui revisão científica, receipt físico ou reprodução.
- `claim_allowed=false` permanece inalterado.
- Nenhuma PR é mesclada automaticamente.

## F_next

1. observar o primeiro run com steps e logs recuperáveis;
2. configurar `promotion-control / enforce` como check obrigatório na branch;
3. executar teste negativo administrativo: tentar promover uma PR draft ou com
   `promotion=DENIED` e preservar o receipt;
4. somente depois classificar `promotion_control=PASS`.
