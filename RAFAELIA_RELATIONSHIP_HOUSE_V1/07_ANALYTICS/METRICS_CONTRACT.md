# Analytics / QA Metrics Contract V1

No metric value is populated during bootstrap. Values become admissible only after a reproducible source-set exists.

## Association metrics

### Jaccard

`J(A,B) = |A ∩ B| / |A ∪ B|`

Use for set overlap. A record MUST preserve the exact set-definition/version.

### PMI / PPMI

`PMI(A,B) = log(P(A,B)/(P(A)P(B)))`

`PPMI(A,B) = max(PMI(A,B), 0)`

The probability estimator, smoothing policy and corpus/window definition MUST be versioned.

### Support

`support_count` is mandatory beside normalized association scores. A high score with weak support must not be promoted as a strong empirical relationship.

### Temporal relation

Preserve `temporal_lag`, observation window, timestamp policy and directionality separately from association strength.

## Mandatory metric envelope

Every computed metric record MUST include:

```json
{
  "metric_id": "METRIC-*",
  "subject_refs": [],
  "metric": "jaccard|pmi|ppmi|support_count|temporal_lag|directionality|qa:*",
  "value": null,
  "method_version": "...",
  "source_set_sha256": "...",
  "support": 0,
  "computed_at": "...",
  "derivation_ref": "...",
  "status": "TOKEN_VAZIO|COMPUTED|INVALIDATED"
}
```

`value=null` + `status=TOKEN_VAZIO` is valid. Invented defaults are forbidden.

## QA metrics replacing metaphorical sigma values

- `provenance_integrity`
- `explicit_support_ratio`
- `missingness_rate`
- `parse_loss_rate`
- `ambiguity_rate`
- `stale_index_rate`
- `reproducibility_rate`
- `hash_mismatch_rate`

Example definition:

`provenance_integrity = 1 - (hash_mismatch_count / objects_verified)`

The denominator-zero policy MUST be explicit; do not silently coerce undefined results to zero or one.

## Interpretation gates

- association != causation
- visualization distance != semantic/scientific distance
- heuristic != proof
- design example != observation
- provisional taxonomy != confirmed corpus classification
- metric without source-set digest/method version/support = inadmissible
