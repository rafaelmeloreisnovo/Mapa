# OECG V1 gate-state model

Applicable gate states:

- `PASS`: exact gate closed by evidence within declared scope.
- `FAIL`: exact gate falsified/violated within declared scope.
- `TOKEN_VAZIO_*`: required state unresolved; blocks promotion.
- `NOT_APPLICABLE`: justified as outside the declared work-unit scope.

Forbidden coercions:

- `TOKEN_VAZIO -> PASS`
- `TOKEN_VAZIO -> FAIL`
- `TOKEN_VAZIO -> NOT_APPLICABLE`
- `search miss -> absence`
- `actor -> authorship`
- `authorship -> semantic truth`
- `semantic coherence -> claim`
- `CI PASS -> compliance`

A `NOT_APPLICABLE` state must be explicitly scoped; it is not a shortcut for unknown.
