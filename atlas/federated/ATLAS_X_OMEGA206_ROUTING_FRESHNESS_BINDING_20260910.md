# ATLAS:X Ω206 — Routing freshness/source binding

- predecessor: `OMEGA-FED-20260910-205`
- gap: `G205-01=OBSERVED+TOKEN_VAZIO_ROUTING_INDEX_FRESHNESS`
- source main: `91d2d5a40fd5f8f06b1aacc2ddf64ff64f5ddd1d`
- provider branch state: `protected=false`, status-check enforcement `off`
- provider ruleset: `21909304`, `enforcement=disabled`, updated `2026-09-03T00:47:00.917-03:00`
- predecessor queue: `data/control-plane/TOKEN_VAZIO_PRIORITY_QUEUE.v3.json`
- successor queue: `data/control-plane/TOKEN_VAZIO_PRIORITY_QUEUE.v4.json`
- validator: `tools/validate_temporal_priority_queue.py`

## Delta

The successor preserves predecessor history while binding current routing to an explicit provider snapshot. The validator now fails closed when the snapshot SHA does not equal `source_main_sha`, timestamps disagree, ruleset rows are malformed/duplicated, or provider evidence exceeds the declared bounded freshness window.

This does **not** prove historical merge enforcement and does **not** activate the disabled ruleset. `claim_allowed=false` remains.

## Closure gate

`G205-01` may close only if provider CI validates the successor queue and the stale predecessor remains preserved. Until that run is observed: `IMPLEMENTED_UNTESTED`.
