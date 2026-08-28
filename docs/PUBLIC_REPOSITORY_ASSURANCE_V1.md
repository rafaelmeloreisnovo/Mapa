# Public Repository Assurance V1

## Purpose

This control-plane artifact prevents public visibility, a README, a hash, a successful local build, or a familiar upstream brand from being promoted into a legal, provenance, security, privacy, runtime, or scientific claim without the evidence required for that claim.

Canonical matrix:

`data/control-plane/PUBLIC_REPOSITORY_ASSURANCE_MATRIX_V1.json`

## Non-negotiable separation

`VISÃO != ARTEFATO != EXECUÇÃO != EVIDÊNCIA != CLAIM`

`TOKEN_VAZIO != PASS`

A public repository can be perfectly usable and still have an open provenance or licensing gate. A fork can be correctly licensed upstream and still have an unclassified authorial delta. A source file can exist and still have no runtime proof. A scientific result can have code and still lack the dataset/version/falsifier needed for reproduction.

## Repository classes

1. **Authorial project with observed root license** — preserve the root license and bind provenance/gates to exact commits.
2. **Authorial project with owner license decision open** — do not invent a grant. Preserve `TOKEN_VAZIO_OWNER_LICENSE_SELECTION` or an explicit all-rights-reserved position until the owner acts.
3. **Mixed-scope authorial repository** — use path/module scope; never silently relicense third-party or separately licensed material.
4. **Upstream derivative** — upstream license/NOTICE/COPYING controls upstream material. Only a proven authorial delta may receive additional notices or a separate compatible license where legally possible.
5. **Large/multi-license upstream tree** — license/provenance is path-aware; a single root label is insufficient.
6. **Research/model repository** — separate code, weights, datasets, citations, hypotheses, empirical results and third-party sources.

## Minimum gate per public repository

A repository cannot move to `PASS` in this matrix unless all applicable dimensions are evidence-bound:

- identity: repository + exact commit/ref;
- authority: who may change which state;
- license: observed governing terms or explicit owner hold;
- provenance: origin of upstream, copied, generated and authorial material;
- third party: SPDX/license/notice retained and compatibility assessed where needed;
- security/privacy: critical blockers fail closed;
- runtime/science: only required when a runtime/scientific claim is made;
- gate: named falsifiable validator with exit criterion;
- rollback: concrete reversal path.

## Priority logic

`P0` means the gap can cause incorrect public permission, provenance, cryptographic/scientific promotion, cross-repository promotion or runtime assertion.

`P1` means the surface is public and reusable but lacks a complete path-aware assurance envelope.

`P2` means the repository is public but currently lower-impact or very large; it remains explicitly unresolved rather than silently treated as safe.

Urgency changes execution order, never truth value.

## Fork rule

For an upstream derivative:

```text
UPSTREAM_BYTES -> upstream LICENSE/NOTICE/COPYING
AUTHORIAL_DELTA -> exact commit/path provenance -> compatible notice/license if applicable
UNKNOWN_DELTA   -> TOKEN_VAZIO_AUTHORIAL_DELTA_BOUNDARY
```

A RAFAELIA notice must never imply ownership of upstream algorithms, source, standards, trademarks, patents, datasets, documentation or other third-party rights.

## Closure

A TOKEN_VAZIO closes only when a successor record points to the exact evidence and named gate that closed it. Historical observations are append-only; a newer pass supersedes rather than rewriting the meaning of an older observation.

The matrix itself has `claim_allowed=false`. It is a routing and assurance artifact, not proof that every listed repository is compliant, secure, original, production-ready or legally cleared.
