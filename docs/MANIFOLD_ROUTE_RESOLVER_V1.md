# Manifold Route Resolver V1

State: `IMPLEMENTED_ON_DRAFT_BRANCH / FAIL_CLOSED / REMOTE_CI_TOKEN_VAZIO_UNTIL_OBSERVED`

The resolver maps a query to the stable route registry without promoting any claim.

Rules:
- explicit `ATLAS:`, `NOVO:`, `GAP:`, `EVID:`, `LEARN:` prefixes have deterministic priority;
- trigger matching resolves only when there is one best route;
- no match returns `TOKEN_VAZIO_NO_ROUTE`;
- ties return `TOKEN_VAZIO_AMBIGUOUS_ROUTE`;
- every output carries `claim_allowed=false`;
- resolver chooses a retrieval route, not truth.

Fixture set: 10 positive + 2 adversarial cases.
The ambiguity fixture `math code` must fail closed between R0002 and R0004.
The unknown fixture `banana azul` must produce no route.

Reproduction:
```bash
python tools/resolve_manifold_route.py "ATLAS: geometria e RLL"
python -m unittest tests.test_manifold_route_resolver
```

Rollback: drop the draft branch/PR; Drive canonical routes remain authoritative.
