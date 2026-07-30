#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

SCHEMA = "rafaelia.semantic-carrier-policy.v1"
TIERS = {"HOT", "WARM", "COLD", "ARCHIVE"}
REQUIRED_CARRIERS = {
    "SOURCE_CARRIER",
    "WORKFLOW_CARRIER",
    "DEPENDENCY_CARRIER",
    "CLAIM_CARRIER",
    "EVIDENCE_CARRIER",
    "SEMANTIC_CARRIER",
    "GAP_CARRIER",
}
REQUIRED_INDEXES = {
    "content_index",
    "temporal_index",
    "workflow_path_index",
    "dependency_index",
    "claim_index",
    "evidence_index",
    "gap_index",
    "semantic_sense_index",
}


class PolicyError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise PolicyError("root must be an object")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    limit = math.isqrt(number)
    return all(number % divisor for divisor in range(3, limit + 1, 2))


def require_unique(values: list[Any], name: str) -> None:
    if len(values) != len(set(values)):
        raise PolicyError(f"{name} must be unique")


def validate(policy: dict[str, Any]) -> dict[str, Any]:
    if policy.get("schema") != SCHEMA:
        raise PolicyError("wrong schema")
    if policy.get("claim_allowed") is not False:
        raise PolicyError("claim_allowed must be false")

    authorities = policy.get("authorities")
    if not isinstance(authorities, list) or not authorities:
        raise PolicyError("authorities required")
    authority_names = [item.get("name") for item in authorities if isinstance(item, dict)]
    if len(authority_names) != len(authorities) or any(not isinstance(name, str) or not name for name in authority_names):
        raise PolicyError("invalid authority")
    require_unique(authority_names, "authority names")
    immutable = [item for item in authorities if item.get("mutable") is False]
    if not immutable:
        raise PolicyError("at least one immutable reconstruction authority is required")

    tiers = policy.get("tiers")
    if not isinstance(tiers, list) or {item.get("id") for item in tiers if isinstance(item, dict)} != TIERS:
        raise PolicyError("tiers must contain HOT/WARM/COLD/ARCHIVE exactly")
    ttl = {item["id"]: item.get("ttl_seconds") for item in tiers}
    if not (isinstance(ttl["HOT"], int) and isinstance(ttl["WARM"], int) and isinstance(ttl["COLD"], int)):
        raise PolicyError("HOT/WARM/COLD TTL must be integers")
    if not (0 < ttl["HOT"] < ttl["WARM"] < ttl["COLD"]):
        raise PolicyError("TTL ordering must be HOT < WARM < COLD")
    if ttl["ARCHIVE"] is not None:
        raise PolicyError("ARCHIVE TTL must be null")
    if any(item.get("event_invalidates") is not True for item in tiers):
        raise PolicyError("events must invalidate every tier")
    archive = next(item for item in tiers if item["id"] == "ARCHIVE")
    if archive.get("polling") is not False:
        raise PolicyError("ARCHIVE cannot be polled")

    carriers = policy.get("carrier_types")
    if not isinstance(carriers, list):
        raise PolicyError("carrier_types required")
    require_unique(carriers, "carrier types")
    missing_carriers = REQUIRED_CARRIERS - set(carriers)
    if missing_carriers:
        raise PolicyError(f"missing carrier types: {sorted(missing_carriers)}")

    indexes = policy.get("indexes")
    if not isinstance(indexes, list):
        raise PolicyError("indexes required")
    require_unique(indexes, "indexes")
    missing_indexes = REQUIRED_INDEXES - set(indexes)
    if missing_indexes:
        raise PolicyError(f"missing indexes: {sorted(missing_indexes)}")

    invalidation = policy.get("invalidation")
    if not isinstance(invalidation, dict) or invalidation.get("conditional_fetch") is not True:
        raise PolicyError("conditional fetch is mandatory")
    signals = invalidation.get("signals")
    full_scan = invalidation.get("full_scan_allowed_only_when")
    if not isinstance(signals, list) or len(signals) < 3:
        raise PolicyError("at least three invalidation signals required")
    if not isinstance(full_scan, list) or "explicit_repair_audit" not in full_scan:
        raise PolicyError("full scan must be gated by explicit repair audit")
    require_unique(signals, "signals")
    require_unique(full_scan, "full scan reasons")

    statistics = policy.get("statistics")
    if not isinstance(statistics, dict):
        raise PolicyError("statistics policy required")
    if statistics.get("global_mean_policy") != "FORBIDDEN_WITHOUT_DISTRIBUTION_AND_COMPARABILITY_JUSTIFICATION":
        raise PolicyError("global mean policy is unsafe")
    strata = statistics.get("strata")
    estimators = statistics.get("robust_estimators")
    if not isinstance(strata, list) or "human_need" not in strata or len(strata) < 5:
        raise PolicyError("statistics must preserve human_need and multiple strata")
    if not isinstance(estimators, list) or not {"median", "quantiles"}.issubset(estimators):
        raise PolicyError("robust estimators must include median and quantiles")
    require_unique(strata, "strata")
    require_unique(estimators, "estimators")

    semantic = policy.get("semantic_identity")
    if not isinstance(semantic, dict):
        raise PolicyError("semantic identity policy required")
    fields = semantic.get("required_fields")
    required_fields = {"language", "locale", "sense_id", "cultural_context", "source_authority"}
    if not isinstance(fields, list) or not required_fields.issubset(fields):
        raise PolicyError("semantic fields do not preserve language/culture/sense")
    if semantic.get("homophone_policy") != "DISTINCT_NODES_UNLESS_EXPLICITLY_PROVEN_EQUIVALENT":
        raise PolicyError("homophone policy must preserve distinct nodes")
    if semantic.get("translation_policy") != "TYPED_EDGE_NOT_IDENTITY":
        raise PolicyError("translation cannot be identity")
    if semantic.get("human_review") is not True:
        raise PolicyError("human semantic review is mandatory")

    prime_facets = policy.get("prime_facets")
    if not isinstance(prime_facets, dict) or len(prime_facets) < 5:
        raise PolicyError("prime facet registry required")
    primes = list(prime_facets.values())
    if any(not isinstance(number, int) or not is_prime(number) for number in primes):
        raise PolicyError("prime facets must contain prime integers")
    require_unique(primes, "prime facet values")

    safety = policy.get("safety")
    expected = {
        "source_immutable": True,
        "append_only": True,
        "fail_closed": True,
        "auto_merge": False,
        "auto_delete": False,
        "private_text_in_carrier": False,
    }
    if safety != expected:
        raise PolicyError("safety policy drift")

    digest = hashlib.sha256(canonical_bytes(policy)).hexdigest()
    return {
        "schema": "rafaelia.semantic-carrier-validation-report.v1",
        "status": "PASS",
        "claim_allowed": False,
        "policy_sha256": digest,
        "summary": {
            "authorities": len(authorities),
            "tiers": len(tiers),
            "carrier_types": len(carriers),
            "indexes": len(indexes),
            "invalidation_signals": len(signals),
            "statistical_strata": len(strata),
            "prime_facets": len(prime_facets),
        },
        "token_vazio": [
            "TOKEN_VAZIO_BASELINE_PENDING",
            "TOKEN_VAZIO_ETAG_IMPLEMENTATION_PENDING",
            "TOKEN_VAZIO_THRESHOLDS_CALIBRATION_PENDING",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("policy", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        report = validate(load_json(args.policy))
    except (OSError, json.JSONDecodeError, PolicyError) as error:
        report = {
            "schema": "rafaelia.semantic-carrier-validation-report.v1",
            "status": "FAIL",
            "claim_allowed": False,
            "error": f"{type(error).__name__}: {error}",
        }
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 1
    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
