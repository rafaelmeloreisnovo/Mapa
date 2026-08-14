#!/usr/bin/env python3
"""BITRAF physical execution residue classifier.

Authorized-lab research scaffold. It does not recover secrets and does not
claim a physical causal mechanism. It learns path/state centroids from labeled
calibration traces, after subtracting an idle baseline, and classifies query
traces. Intended evidence class: SIMULATED_ONLY until real instrument capture.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

FEATURES = ("current_a", "voltage_v", "temperature_c")


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            obj["_lineno"] = lineno
            rows.append(obj)
    return rows


def baseline_by_channel(rows):
    acc = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r.get("role") != "baseline":
            continue
        ch = r["channel"]
        for f in FEATURES:
            acc[ch][f].append(float(r[f]))
    return {ch: {f: mean(vals[f]) for f in FEATURES} for ch, vals in acc.items()}


def residual_vector(r, baseline):
    ch = r["channel"]
    if ch not in baseline:
        raise ValueError(f"missing baseline for channel {ch!r}")
    b = baseline[ch]
    di = float(r["current_a"]) - b["current_a"]
    dv = float(r["voltage_v"]) - b["voltage_v"]
    dt = float(r["temperature_c"]) - b["temperature_c"]
    p = float(r["current_a"]) * float(r["voltage_v"])
    p0 = b["current_a"] * b["voltage_v"]
    dp = p - p0
    return (di * 1e3, dv * 1e3, dt, dp * 1e3)


def learn_centroids(rows, baseline):
    by_label = defaultdict(list)
    for r in rows:
        if r.get("role") == "calibration":
            label = r.get("path_label")
            if not label:
                raise ValueError("calibration row missing path_label")
            by_label[label].append(residual_vector(r, baseline))
    if len(by_label) < 2:
        raise ValueError("need at least two calibration labels")
    centroids = {}
    for label, vectors in sorted(by_label.items()):
        dims = list(zip(*vectors))
        centroids[label] = tuple(mean(list(d)) for d in dims)
    return centroids


def sqdist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def classify(rows):
    baseline = baseline_by_channel(rows)
    if not baseline:
        raise ValueError("no baseline rows")
    centroids = learn_centroids(rows, baseline)
    results = []
    for r in rows:
        if r.get("role") != "query":
            continue
        v = residual_vector(r, baseline)
        ranked = sorted((sqdist(v, c), label) for label, c in centroids.items())
        best_d, best_label = ranked[0]
        second_d = ranked[1][0] if len(ranked) > 1 else math.inf
        margin = None if math.isinf(second_d) else max(0.0, second_d - best_d)
        results.append({
            "observation_id": r["observation_id"],
            "candidate_path": best_label,
            "distance2": best_d,
            "separation_margin": margin,
            "residual_vector": {
                "delta_current_mA": v[0],
                "delta_voltage_mV": v[1],
                "delta_temperature_C": v[2],
                "delta_power_mW": v[3]
            },
            "evidence_class": r.get("source_kind", "TOKEN_VAZIO"),
            "claim_allowed": False,
            "causal_mechanism": "TOKEN_VAZIO"
        })
    return {"schema_version": "rafaelia.bitraf-rfe-inference/v1", "results": results}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl", type=Path)
    ap.add_argument("--pretty", action="store_true")
    ns = ap.parse_args()
    print(json.dumps(classify(load_jsonl(ns.jsonl)), indent=2 if ns.pretty else None, sort_keys=True))


if __name__ == "__main__":
    main()
