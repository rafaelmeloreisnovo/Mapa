# OECG V1 source-actor rule

`actor` records who/what emitted an observed occurrence. It is not a rights or truth field.

- `USER`: occurrence emitted by the user in the captured source.
- `ASSISTANT`: occurrence emitted by the assistant/model.
- `TOOL`: occurrence emitted by a connected tool/provider.
- `SYSTEM`: occurrence emitted by system/control context.
- `UNKNOWN`: actor cannot be determined from available evidence.

Authorship, sense and claim authority require their own evidence. Never promote those from `actor` alone.
