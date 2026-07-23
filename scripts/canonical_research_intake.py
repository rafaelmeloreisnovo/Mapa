#!/usr/bin/env python3
"""Canonical, conservative scholarly intake for the private Mapa repository."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from research_intake.artifacts import emit_artifacts, public_export, synthesis
from research_intake.core import (
    VALID_STATES, allocate_record_ids, assign_states, canonical_json, canonical_key,
    deduplicate, load_config, load_id_registry, load_json_records, load_review_ledger,
    normalize_record, normalize_text, sha256_text, title_fingerprint,
)
from research_intake.sources import fetch_json, network_collect


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--input-fixture", type=Path)
    parser.add_argument("--review-ledger", type=Path)
    parser.add_argument("--id-registry", type=Path)
    parser.add_argument("--network-query")
    parser.add_argument("--network-limit", type=int, default=10)
    parser.add_argument("--mailto", default="")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--generated-at", default="")
    args = parser.parse_args()
    if bool(args.input_fixture) == bool(args.network_query):
        raise SystemExit("choose exactly one of --input-fixture or --network-query")
    config = load_config(args.config)
    raw = (load_json_records(args.input_fixture) if args.input_fixture else
           network_collect(config, args.network_query, max(1, min(args.network_limit, 100)), args.mailto))
    reviews = load_review_ledger(args.review_ledger)
    registry = load_id_registry(args.id_registry, config["prefix"], config["width"])
    records = assign_states(deduplicate(raw), reviews, config["prefix"], config["width"], registry)
    generated_at = args.generated_at or datetime.now(timezone.utc).isoformat()
    emit_artifacts(records, config, args.output, generated_at, registry)
    print(f"PASS records={len(records)} output={args.output}")
    print("PASS claim_allowed=false automatic_public_push=false automatic_claim_promotion=false")


if __name__ == "__main__":
    main()
