#!/usr/bin/env python3
"""RAFAELIA operational ontology validator and gap mapper (stdlib only)."""
from __future__ import annotations
import argparse, hashlib, json, sys
from collections import Counter, defaultdict, deque
from pathlib import Path

REPORT_SCHEMA = "rafaelia.operational-ontology-report/v1"
SPECIAL = {"ABORTED", "CENSORED", "IGNORED", "POTENTIAL", "SUGGESTED", "WITHHELD"}
UNRESOLVED = {"HIPOTESE", "ESTIMATIVA", "CONJECTURA", "TOKEN_VAZIO", "BOTH", "NEITHER", "SCOPE_SPLIT"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def finding(code, severity, record, message, gap, next_gate):
    raw = "\0".join((code, severity, record, message)).encode()
    return {"id": hashlib.sha256(raw).hexdigest()[:20], "heuristic": code,
            "severity": severity, "record_id": record, "message": message,
            "gap_class": gap, "next_gate": next_gate}


def validate(data):
    errors = []
    sections = ("metadata", "operational_arms", "epistemic_states", "gap_classes", "tokens", "operators",
                "dynamics", "anomaly_classes", "records")
    for name in sections:
        if name not in data:
            errors.append(f"missing section: {name}")
    if data.get("metadata", {}).get("claim_allowed") is not False:
        errors.append("metadata.claim_allowed must be false")
    indexes = {}
    for name in sections[1:]:
        items = data.get(name, [])
        if not isinstance(items, list):
            errors.append(f"{name} must be an array"); continue
        values = [x.get("id") for x in items if isinstance(x, dict)]
        if any(not x for x in values): errors.append(f"{name} has missing id")
        if len(values) != len(set(values)): errors.append(f"{name} has duplicate id")
        indexes[name] = set(values)
    required = ("id", "label", "kind", "status", "epistemic_state", "trajectory", "context",
                "definition", "claim_allowed", "provenance", "evidence", "falsifiers",
                "tags", "next_gate", "relations")
    record_ids = indexes.get("records", set())
    for rec in data.get("records", []):
        rid = rec.get("id", "<missing>")
        for key in required:
            if key not in rec: errors.append(f"record {rid} missing {key}")
        if rec.get("epistemic_state") not in indexes.get("epistemic_states", set()):
            errors.append(f"record {rid} unknown state {rec.get('epistemic_state')}")
        if rec.get("gap_class") and rec["gap_class"] not in indexes.get("gap_classes", set()):
            errors.append(f"record {rid} unknown gap {rec['gap_class']}")
        if rec.get("claim_allowed") and rec.get("epistemic_state") in UNRESOLVED:
            errors.append(f"record {rid} unresolved state cannot allow claim")
        for rel in rec.get("relations", []):
            if rel.get("operator") not in indexes.get("operators", set()):
                errors.append(f"record {rid} unknown operator {rel.get('operator')}")
            if rel.get("target") not in record_ids:
                errors.append(f"record {rid} unknown target {rel.get('target')}")
    return sorted(set(errors))


def heuristics(data):
    out = []
    for rec in data.get("records", []):
        rid, state, status = rec["id"], rec.get("epistemic_state"), rec.get("status")
        def add(code, sev, msg, gap, gate): out.append(finding(code, sev, rid, msg, gap, gate))
        if not rec.get("definition"): add("H-DEF", "BLOCK", "missing operational definition", "TV-DEF", "define term, domain and counterexample")
        if not rec.get("provenance"): add("H-PROVENANCE", "BLOCK", "missing source/path/commit", "TV-PROVENANCE", "register provenance pointer")
        if state in {"PROVADO", "EVIDENCIADO", "SUPPORTED_ONLY"} and not rec.get("evidence"):
            add("H-EVIDENCE", "ERROR", f"{state} without evidence", "TV-DATA", "attach evidence or demote state")
        if state == "TOKEN_VAZIO":
            if not rec.get("gap_class"): add("H-GAP-CLASS", "ERROR", "unclassified TOKEN_VAZIO", "TV-DEF", "assign gap class")
            if not rec.get("reason"): add("H-GAP-REASON", "ERROR", "TOKEN_VAZIO without reason", rec.get("gap_class"), "document why evidence is missing")
            if not rec.get("next_gate"): add("H-DEAD-END", "ERROR", "TOKEN_VAZIO without next gate", rec.get("gap_class"), "assign verifiable next action")
        if status in SPECIAL and (not rec.get("reason") or not rec.get("decision_context")):
            add("H-SPECIAL-STATUS", "BLOCK", f"{status} requires reason and decision context", "TV-PROVENANCE", "record decision source and boundary")
        if status == "CENSORED" and not rec.get("censorship_evidence"):
            add("H-CENSORSHIP", "ERROR", "not-found/withheld cannot be inferred as censorship", "TV-ACCESS", "attach documentary evidence or demote status")
        if rec.get("value") == 0 and rec.get("measurement_status") in {None, "UNKNOWN", "UNMEASURED"}:
            add("H-EMPTY-NOT-ZERO", "ERROR", "unknown encoded as zero", "TV-DATA", "use TOKEN_VAZIO or validity mask")
        if rec.get("relation_mode") == "causal" and not rec.get("falsifiers"):
            add("H-FALSIFIER", "BLOCK", "causal claim without falsifier", "TV-TEST", "define negative control and rejection condition")
        evidence = rec.get("evidence", [])
        lineage = [x.get("lineage_id") for x in evidence if isinstance(x, dict) and x.get("lineage_id")]
        if len(lineage) > 1 and len(lineage) != len(set(lineage)):
            add("H-INDEPENDENCE", "WARN", "sources share lineage", "TV-INDEPENDENCE", "deduplicate and seek independent source")
        for rel in rec.get("relations", []):
            op, target = rel.get("operator"), rel.get("target")
            if not rel.get("scope"): add("H-BOUNDARY", "BLOCK", f"{op}->{target} lacks scope", "TV-BOUNDARY", "declare domain, time, language and scale")
            if op == "REVERSIVE" and not rel.get("reconstruction_metric"): add("H-RECON", "BLOCK", "reversive path lacks reconstruction metric", "TV-RECON", "declare error and tolerance")
            if op == "RECURSIVE" and not rel.get("exit"): add("H-LOOP", "ERROR", "recursive path lacks exit criteria", "TV-LOOP", "declare max depth, repeated-state detector and minimum gain")
            if op == "DERIVATIVE" and not (rel.get("axis") and rel.get("unit")): add("H-DERIVATIVE", "BLOCK", "derivative lacks axis/unit", "TV-BOUNDARY", "declare axis, spacing and unit")
            if op == "ANTIDERIVATIVE" and not rel.get("boundary_condition"): add("H-ANTIDERIVATIVE", "BLOCK", "antiderivative lacks boundary/origin", "TV-BOUNDARY", "declare integration constant or historical boundary")
            if op == "LOG_LOG" and (rel.get("domain") != "positive" or not rel.get("alternative_models")):
                add("H-LOGLOG", "BLOCK", "log-log lacks positive domain or competing models", "TV-TEST", "compare power law, exponential, lognormal and segmented models")
            if op == "NESTED_LOG_LOG" and not rel.get("domain_definition"):
                add("H-NESTED-LOG", "ERROR", "log(log(x)) domain/purpose undefined", "TV-DOMAIN", "define x>1, scale, purpose and falsifier")
    return sorted(out, key=lambda x: (x["severity"], x["heuristic"], x["record_id"]))


def graph(data):
    records = data.get("records", [])
    adj = {r["id"]: set() for r in records}; inbound = Counter()
    for rec in records:
        for rel in rec.get("relations", []):
            if rel.get("target") in adj:
                adj[rec["id"]].add(rel["target"]); inbound[rel["target"]] += 1
    und = {k: set(v) for k, v in adj.items()}
    for a, bs in adj.items():
        for b in bs: und[b].add(a)
    seen, comps = set(), []
    for start in sorted(und):
        if start in seen: continue
        q, comp = deque([start]), []; seen.add(start)
        while q:
            n = q.popleft(); comp.append(n)
            for x in sorted(und[n]):
                if x not in seen: seen.add(x); q.append(x)
        comps.append(sorted(comp))
    return {"nodes": len(adj), "edges": sum(map(len, adj.values())),
            "isolated": sorted(k for k,v in adj.items() if not v and not inbound[k]),
            "dead_ends": sorted(k for k,v in adj.items() if not v and inbound[k]),
            "components": sorted(comps, key=lambda x:(len(x),x))}


def trajectories(data):
    groups, tagmap = defaultdict(list), defaultdict(lambda: defaultdict(list))
    for rec in data.get("records", []):
        groups[rec["trajectory"]].append(rec)
        for tag in rec.get("tags", []): tagmap[tag][rec["trajectory"]].append(rec["id"])
    summary = {k: {"records": len(v), "unresolved": sum(r.get("epistemic_state") in UNRESOLVED or r.get("status") in SPECIAL for r in v),
                   "statuses": sorted({r.get("status") for r in v}),
                   "next_gates": sorted({r.get("next_gate") for r in v if r.get("next_gate")})}
               for k,v in sorted(groups.items())}
    bridges = [{"tag": tag, "trajectories": sorted(by), "records": {k:sorted(v) for k,v in sorted(by.items())},
                "classification": "METHODOLOGICAL_BRIDGE_NOT_PHYSICAL_EQUIVALENCE"}
               for tag,by in sorted(tagmap.items()) if len(by)>1]
    return {"trajectories": summary, "bridges": bridges}


def build_report(data, generated_at):
    errors, finds = validate(data), heuristics(data)
    states = Counter(r.get("epistemic_state") for r in data.get("records", []))
    statuses = Counter(r.get("status") for r in data.get("records", []))
    declared = Counter(r.get("gap_class") for r in data.get("records", []) if r.get("gap_class"))
    return {"schema": REPORT_SCHEMA, "generated_at": generated_at,
            "ontology": {"version": data.get("metadata",{}).get("version"),
                         "sha256": hashlib.sha256(canonical(data).encode()).hexdigest()},
            "validation": {"valid": not errors, "errors": errors},
            "summary": {"records": len(data.get("records",[])), "findings": len(finds),
                        "blocking": sum(x["severity"] in {"ERROR","BLOCK"} for x in finds),
                        "states": dict(sorted(states.items())), "statuses": dict(sorted(statuses.items())),
                        "declared_gaps": dict(sorted(declared.items()))},
            "graph": graph(data), "trajectory_analysis": trajectories(data), "findings": finds,
            "closure": {"F_ok": ["machine-readable ontology", "unknown != zero", "heuristic != proof", "not found != censored"],
                        "F_gap": sorted(declared), "claim_allowed": False}}


def render_md(r):
    s=r["summary"]; lines=["# RAFAELIA Operational Ontology — Audit", "", f"- Validation: **{'PASS' if r['validation']['valid'] else 'FAIL'}**", f"- Records: **{s['records']}**", f"- Findings: **{s['findings']}**", f"- TOKEN_VAZIO: **{s['states'].get('TOKEN_VAZIO',0)}**", f"- Graph: **{r['graph']['nodes']} nodes / {r['graph']['edges']} edges**", "", "## Declared gaps"]
    lines += [f"- `{k}`: {v}" for k,v in s["declared_gaps"].items()]
    lines += ["", "## Trajectories", "", "| Trajectory | Records | Unresolved |", "|---|---:|---:|"]
    lines += [f"| `{k}` | {v['records']} | {v['unresolved']} |" for k,v in r["trajectory_analysis"]["trajectories"].items()]
    lines += ["", "## Bridges"]
    lines += [f"- `{b['tag']}`: {', '.join(b['trajectories'])} — `METHODOLOGICAL_BRIDGE_NOT_PHYSICAL_EQUIVALENCE`" for b in r["trajectory_analysis"]["bridges"]]
    lines += ["", "## Findings"]
    lines += [f"- `{x['severity']}` `{x['heuristic']}` `{x['record_id']}` — {x['message']} → {x['next_gate']}" for x in r["findings"]] or ["- No structural defects detected; declared gaps remain open and useful."]
    lines += ["", "## Ω", "", "```text", "heuristic != proof", "missing != zero", "not found != censored", "claim_allowed=false", "```", ""]
    return "\n".join(lines)


def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--ontology",required=True); p.add_argument("--output-json",required=True); p.add_argument("--output-md",required=True); p.add_argument("--generated-at",required=True); p.add_argument("--strict",action="store_true"); a=p.parse_args(argv)
    try: data=json.loads(Path(a.ontology).read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as e: print(e,file=sys.stderr); return 2
    r=build_report(data,a.generated_at); Path(a.output_json).parent.mkdir(parents=True,exist_ok=True); Path(a.output_md).parent.mkdir(parents=True,exist_ok=True); Path(a.output_json).write_text(json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); Path(a.output_md).write_text(render_md(r),encoding="utf-8"); print(json.dumps(r["summary"],sort_keys=True)); return 1 if (not r["validation"]["valid"] or (a.strict and r["summary"]["blocking"])) else 0

if __name__ == "__main__": raise SystemExit(main())
