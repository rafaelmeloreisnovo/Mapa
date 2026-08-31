## Summary

<!-- Describe the change, why it is needed, and the consequence it is intended to reduce. -->

## Type

- [ ] New classification / catalog entry
- [ ] New visual map (SVG)
- [ ] Protocol or workflow
- [ ] Index update
- [ ] Documentation
- [ ] Bug fix
- [ ] Security / supply-chain control
- [ ] Privacy / data-governance change
- [ ] Audit / risk / CAPA change

## Affected area

<!-- arquitetura/ | biblioteconomia/ | protocolos/ | indices/ | resultados/ | visual/ | workflows/ | .github/ | governance/ -->

## Risk and consequence

- Threat / failure mode:
- Plausible consequence:
- Existing control:
- Residual risk after this change:
- Rollback / disable path:

## Data and privacy impact

- [ ] No new personal or sensitive data flow
- [ ] Data flow changed and is documented below
- [ ] External service / supplier receives data or metadata
- [ ] Retention / deletion behavior changed
- [ ] Access or permission boundary changed

<!-- If any box other than "No new personal or sensitive data flow" applies, describe source, purpose, destination, minimization, retention and evidence. -->

## Supply-chain and workflow impact

- [ ] No new external GitHub Action / executable dependency
- [ ] Every changed external GitHub Action is pinned to an immutable full commit SHA
- [ ] Permissions follow least privilege
- [ ] Third-party network egress is absent or explicitly reviewed

## Evidence and epistemic state

<!-- Use only states supported by evidence. TOKEN_VAZIO is valid and must not be promoted to PASS. -->

- State: `REFERENCE | DESIGNED | IMPLEMENTED | EVIDENCED | VERIFIED | TOKEN_VAZIO`
- Evidence / receipt:
- Falsifier or negative fixture:
- Independent review required: `yes | no | TOKEN_VAZIO`

## Standards / legal references

<!-- References guide the work; they are not certification claims. Add only references that are actually relevant to this change. -->

- References:
- Applicability gaps:

## Validation

- [ ] Relevant tests / linters / validators run
- [ ] Negative path or failure behavior considered
- [ ] No secrets, credentials, unnecessary personal data, or private evidence added
- [ ] README / index updated when navigation changes
- [ ] CHANGELOG.md updated under [Unreleased] when appropriate
- [ ] No certification or compliance claim is made without independently verifiable scope and authority

## Closure invariant

`REFERENCE != IMPLEMENTED != EVIDENCED != VERIFIED != CERTIFIED`

`TOKEN_VAZIO != PASS`
