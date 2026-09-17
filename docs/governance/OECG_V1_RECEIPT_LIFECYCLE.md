# OECG V1 receipt lifecycle

`DRAFT_RECEIPT -> EXECUTION_RECEIPT -> SUCCESSOR/CORRECTION_RECEIPT`

- Draft receipt records intended/baseline state and must label unexecuted checks as pending/TOKEN_VAZIO.
- Execution receipt binds exact revision, commands/workflow, observed statuses, output digests and negative controls.
- A later provider change or correction creates a successor; it does not alter the historical execution receipt.

Receipts are evidence indexes, not substitutes for underlying logs/artifacts/source.
