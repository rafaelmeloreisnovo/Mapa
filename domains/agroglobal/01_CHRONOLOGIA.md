# Chronology & time provenance

Order:
T0 intent / preregistration (GitHub commit cb6ef2600435fd765d5abc1d696521d3ac174f7d, 2026-10-10T01:59:08Z provider).
T1 source-discovery (Drive canonical V2.2 + CURRENT_STATE + Mapa private repo).
T2 Drive folder NOVOexport/AGROGLOBAL_OMEGA created: 1K1E8Iiqb-DbinyEypXANK4f1Vf1pjiCX (provider createdTime to verify).
T3 alphaXiv scholarly folder created: 01a12389-3b85-7b7b-b6c2-187ba8b0b283.
T4 schema / atlas construction: this additive documentation snapshot; separate provider commit SHA.
T5 raw data ingestion: NOT_RUN.
T6 empirical comparison, audits and independent evidence: NOT_RUN.

For every market record: quote_timestamp_local, quote_utc, timezone, venue, contract_month, publication_timestamp, access_timestamp, source_revision, settlement_or_intraday. Preserve daylight-saving and weekends.
For every crop record: agricultural_year, harvest_season, marketing_year, forecast_vintage, observation_date and publication_date.
For every custody event: actor, provider_reported_created_at, local_recorded_at, previous_hash, source_locator, action, result, digest, rollback_pointer.
Recorded client time is not independent trusted timestamp. Provider timestamp records receipt at that provider, not origin of underlying commodity price.
