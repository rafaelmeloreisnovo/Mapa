# Receipt — Casa de Conhecimento e Trabalho V1 — 2026-09-13

state: VERIFIED_LIMITED_LOCAL  
claim_allowed: false  
remote_ci: TOKEN_VAZIO_NOT_EXECUTED

## Source
- Drive START HERE — A-A auditar — RAFAELIA
- Drive RAFAELIA — Implementação Latentes e Papers — Drive GitHub V1
- Mapa README / authority registry / control-plane rules

## Delta
Materializado um serviço fail-closed com oito guardiões:
reconstruibilidade, proveniência, contexto, evidência, contradição, incerteza, reprodução e rollback.

## Local test
Python unittest:
- 5 tests
- 5 PASS
- 0 FAIL

Cobertura adversarial:
- contradição OPEN bloqueia promoção;
- TOKEN_VAZIO bloqueia claim_allowed;
- reprodução ausente bloqueia REPRODUCED;
- reconstruibilidade incompleta bloqueia CLOSED;
- unidade completa passa.

## Boundary
O teste foi executado em sandbox local desta sessão, não por GitHub Actions nem por dispositivo físico.
Portanto:
LOCAL_VALIDATOR = VERIFIED_LIMITED_LOCAL
REMOTE_CI = TOKEN_VAZIO_NOT_EXECUTED
SERVICE_PRODUCTION = TOKEN_VAZIO
claim_allowed = false

## R3
F_ok: contrato, schema, manifesto, validador e testes materializados; 5/5 testes locais PASS.
F_gap: CI/provider, integração UI e uso em unidade real ainda não reproduzidos.
F_next: executar CI existente ou revisão do PR; depois aplicar a uma unidade real com receipt e rollback verificável.
