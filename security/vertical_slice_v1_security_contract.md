# Security contract — Vertical Slice V1

1. Standard-library-only executor; no network access is required.
2. Source files are read-only; the runner writes only a new receipt path.
3. Hash mismatch, absent source, absent falsifier or malformed archive fails closed.
4. The chat export is not semantically parsed in this slice; private message content is not copied to GitHub.
5. No credentials, tokens, signing keys, personal identifiers or raw conversation bodies are committed.
6. Reference and Termux receipts are separate immutable records.
7. No automatic merge, publication, branch deletion, force-push or claim promotion is authorized.
