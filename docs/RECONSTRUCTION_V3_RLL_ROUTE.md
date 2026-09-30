# Reconstruction V3: RLL producer route

The user designated RLL and Mapa as the destinations for the JSON reconstruction
implementation. RLL owns the executable kernel and hosted adapters. Mapa owns
this route and its bounded federation record.

- Route: `data/control-plane/RECONSTRUCTION_V3_RLL_ROUTE.v1.json`
- Producer: `instituto-Rafael/relativity-living-light`
- Pinned producer commit: `7f9923ec8f82af2e690e01ffebf052761114d4fa`
- Producer review: https://github.com/instituto-Rafael/relativity-living-light/pull/1022
- Kernel: `native/reconstruction_v3/rv3.c` and `rv3.h`
- Hosted adapters: `tools/reconstruction_v3/scan.c` and `ingest.py`
- Producer receipt: `receipts/reconstruction_v3/20260930-foundation.json`
- Local federation delta: `auditoria/reconstruction_v3/20260930-route-receipt.json`

The native kernel has local fixture evidence: five test methods, C capacity and
depth checks, and no undefined symbols in the freestanding native object.
The Python/SQLite adapter is hosted and uses private local input. No private
source conversations, database or materialized snapshots are included here.

This is a bounded full-document foundation. Streaming, ARM execution, real
corpus inventory, complete semantic graph, language-level code extraction,
formula equivalence, genealogy and source-schema reconciliation remain open.
The quoted historical counts are unverified audit targets. Formula candidates
are AUDIT, references PENDING, observed content completeness UNKNOWN.
Neither a local fixture result nor a topology check closes existing Mapa gaps.
Producer review is unmerged; remote CI is PENDING.

Validate the route without pretending to execute the producer:

```sh
python3 tools/validate_reconstruction_v3_route.py
python3 tools/validate_reconstruction_v3_route.py --producer-root /path/to/rll
python3 scripts/validate_federation_topology.py --repos 6 --check
```

The second command verifies pinned file hashes against available producer bytes;
it does not rerun the producer tests or verify its Git ancestry. Preserve all
original receipts and append successors after new corpus/device evidence.
Rollback: discard this review branch; no existing gap states are changed.
