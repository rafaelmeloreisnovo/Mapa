# OECG V1 privacy / child-safety boundary

Privacy and child-safety are applicability-sensitive but fail closed when applicability itself is unknown and the work unit can plausibly affect people.

Principles:

1. Minimize raw retention; prefer pointer/hash/receipt where reconstructibility permits.
2. Do not publish private source identifiers merely to improve auditability.
3. `minor_related=YES` requires non-public privacy classification and an authorization reference in the v2 checker.
4. `minor_related=TOKEN_VAZIO` is not equivalent to `NO`.
5. Consent/legal basis/authorization are not inferred from authorship, family relation, faith statement, account ownership or technical access.
6. Redaction/sanitization must preserve a private custody pointer when reconstruction is required and authorized.

This file is an operational policy overlay, not legal advice or a declaration of compliance with any jurisdiction.
