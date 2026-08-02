# Mapa de Execução Matemática em Sete Direções — V1

**Evento:** `MATH-7D-PORTFOLIO-20260801`  
**Branch:** `research/peer-review-math-portfolio-v1-20260801`  
**Estado:** `DRAFT / claim_allowed=false`

## Autoridades

```text
papers#38       -> manuscrito, escopo e revisão
RafPolimata#195 -> código, testes e validação
Mapa#126        -> dependências, estados e próximos gates
Drive           -> memória longitudinal append-only
```

A referência anterior a `Mapa#94` era incorreta: esse número pertence a uma ata de auditoria de 2026-07-30. A autoridade correta deste portfólio é `Mapa#126`.

## Topologia

\[
\psi_{\rm fato}
\rightarrow
\chi_{\rm lacuna}
\rightarrow
\rho_{\rm invariante}
\rightarrow
\Delta_{\rm variante}
\rightarrow
\Sigma_{\rm prova}
\rightarrow
\Pi_{\rm parábola}
\rightarrow
\Omega_{\rm retroalimentação}.
\]

O arquivo de máquina `data/research/peer_review_math_7d_matrix.v1.json` registra os 12 pacotes e os oito gates editoriais `G0–G7`.

## Governança

- conteúdo público: metadados minimizados;
- corpo de corpus privado: proibido;
- credenciais: proibidas;
- alteração de identidade/escopo: nova versão;
- alteração de estado/evidência: evento append-only;
- ausência de prova: `TOKEN_VAZIO`;
- merge automático: bloqueado;
- claim científico final: bloqueado até revisão e replicação.

## Dependência principal

```text
PRM-02 atlas
   ├── PRM-08 Navier–Stokes discreto
   └── PRM-09 Yang–Mills discreto

PRM-01 evidência
   └── PRM-05 runtime epistêmico
       └── todos os demais pacotes

PRM-03 formalismo H7
   └── PRM-04 resultado negativo
       └── PRM-06 SGHP
```

## Estado numérico

```yaml
canonical_formulations: 60
peer_review_packages: 12
ready_for_scope_review: 5
experiment_required: 5
research_agenda_only: 2
open_problem_solution_claims: 0
publication_ready: false
independent_replication: TOKEN_VAZIO
physical_termux_execution: TOKEN_VAZIO
```

## Próximos gates

1. validar o manifesto 7D no `RafPolimata`;
2. executar o atlas em segundo ambiente;
3. criar MMS mínima para fluxo 2D incompressível;
4. criar U(1) triangular 2D com invariância de gauge;
5. registrar pareceres e respostas sem reescrever a história.
