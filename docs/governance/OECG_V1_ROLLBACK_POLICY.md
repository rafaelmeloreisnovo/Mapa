# OECG V1 rollback / supersession policy

Rollback is planned before promotion.

For repository changes:

- preserve base/head SHAs;
- prefer reversible branch/commit deltas;
- do not rewrite default-branch history as a routine rollback mechanism;
- record revert/superseding commit and observed result.

For documentary/semantic records:

- do not erase prior receipts/events;
- append a successor with `parent`/`supersedes`;
- update active pointers while preserving historical navigation.

Rollback readiness is not rollback execution. A tested rollback must have its own evidence.
