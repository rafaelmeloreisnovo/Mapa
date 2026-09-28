# PAT Capability Federation V1

State: **PENDING_EXECUTOR_SOURCE_MERGE**  
Federated authority: `rafaelmeloreisnovo/Mapa`  
PAT-backed executor: `rafaelmeloreisnovo/RafGitTools`  
Claim gate: `claim_allowed=false`

## Canonical identifiers

`PAT_ACTIONS`, `PAT_AGENTS`, `PAT_CODESPACES`, `PAT_DEPENDABOT`, `PAT_ENV`.

Canonical GitHub Environment display: `PAT_ENVIRONMENTS`.

Historical case variants are evidence records, not current naming authority.

## Federation rule

Mapa does **not** execute PAT-backed operations and never stores secret values.

Mapa stores only typed routing:

`capability → executor → source ref → evidence rule → state → gap → next`.

RafGitTools owns the bounded execution lanes. A PAT-backed state may be promoted only by the executor contract plus provider readback.

## Current source

Executor source is RafGitTools PR #556 at `b4d21f79988b60d6d2179caf4e173e61045eb235`.

Because that source is not merged at projection creation, this Mapa projection remains `PENDING_EXECUTOR_SOURCE_MERGE`.

## Boundary

`CAPABILITY != PERMISSION != EXECUTION != EVIDENCE != CLAIM`.

The presence of `PAT_AGENTS`, `PAT_CODESPACES` or `PAT_DEPENDABOT` does not prove their provider scopes. They remain routed to a permission probe in RafGitTools.

`PAT_ACTIONS` is currently bounded to exact-SHA read-only provider work.  
`PAT_ENV` is currently bounded to manual environment/protection operations.

No PAT fallback is allowed.
