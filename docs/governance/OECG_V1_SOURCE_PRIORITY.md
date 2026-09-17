# OECG V1 source-priority / staleness policy

For current operational state, prefer the narrowest authoritative fresh source:

1. producer repository current revision + execution/readback evidence;
2. provider state/readback for provider-owned controls;
3. Drive receipts/indexes for documentary custody and longitudinal reconstruction;
4. session memory/context only as routing aid, never as replacement for a fresh source when current state matters.

A historical receipt remains true about the state observed then. It must not be silently rewritten to match current provider state.

`HISTORICAL_STATE != CURRENT_STATE`

`MEMORY != SOURCE`
