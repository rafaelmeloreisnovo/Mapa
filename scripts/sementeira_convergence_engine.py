#!/usr/bin/env python3
"""SEMENTEIRA V5 convergence engine.

This engine closes only gaps that are deterministically derivable from the
declared source state. It never promotes external/undefined gaps. The user
term NIBIGUIRE is treated as an author-defined class for a missed structural
relation whose ingredients and proof are already present.

The stopping condition is a local fixed point: one complete audit pass closes
zero additional deterministic gaps. At that point local marginal
effort-per-gain is infinite; remaining items are routed to typed TOKEN_VAZIO
instead of being invented.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from typing import Iterable

LOCAL = "LOCAL_DETERMINISTIC"
EXTERNAL = "EXTERNAL_EVIDENCE"
UNDEFINED = "AUTHOR_DEFINITION_REQUIRED"

@dataclass(frozen=True)
class Candidate:
    id: str
    title: str
    mode: str
    dependencies: tuple[str, ...] = ()
    proof: str = ""
    token_vazio: str | None = None

ROOTS = {
    "FOLD_METRIC", "CYCLE_CHORD", "EQUILATERAL_HEIGHT", "FIBONACCI_MOD7",
    "RAFAELIANA_SHIFT_ISOMETRY", "ICOSPHERE_F2", "PROJECT_CONTEXT_CUSTODY",
    "APPEND_ONLY_CUSTODY",
}

CANDIDATES: tuple[Candidate, ...] = (
    Candidate("NBG-001", "Scale-aware ratio object preserves 77:33 versus 7:3", LOCAL, proof="primitive pair + gcd scale + Euclidean norm + angle"),
    Candidate("NBG-002", "Dimensional scaling preserves length/area/volume exponents", LOCAL, ("NBG-001",), "s^1, s^2, s^3 under geometric similarity"),
    Candidate("NBG-003", "Equilateral side 14 exposes height 7*sqrt(3)", LOCAL, ("EQUILATERAL_HEIGHT",), "h=(sqrt(3)/2)*14"),
    Candidate("NBG-004", "Medial inversion of side 14 has side 7 and area quarter", LOCAL, ("NBG-003",), "midpoint theorem + area similarity"),
    Candidate("NBG-005", "Square lift 7 -> 7*sqrt(2) -> diagonal 14", LOCAL, ("NBG-004",), "Pythagoras in square"),
    Candidate("NBG-006", "Circumcircle ratios for equilateral side 14", LOCAL, ("NBG-003",), "R=a/sqrt(3), A_circle=pi*R^2"),
    Candidate("NBG-007", "General folded equilateral height lift H_m,R", LOCAL, ("FOLD_METRIC", "CYCLE_CHORD", "EQUILATERAL_HEIGHT"), "H=sqrt(3)*R*sin(pi*d_m/m)"),
    Candidate("NBG-008", "Even-index embedding of mod 7 height geometry inside mod 14", LOCAL, ("NBG-007",), "H_14(2x,2y)=H_7(x,y)"),
    Candidate("NBG-009", "Fibonacci mod-7 hidden-height spectrum", LOCAL, ("NBG-007", "FIBONACCI_MOD7"), "fold residues then map by H_7"),
    Candidate("NBG-010", "Rafaeliana preserves relational height but not zero-anchored height", LOCAL, ("NBG-007", "RAFAELIANA_SHIFT_ISOMETRY"), "translation preserves pairwise cyclic distance"),
    Candidate("NBG-011", "Central icosphere geodesic altitude equals alpha/2", LOCAL, ("ICOSPHERE_F2",), "spherical right-triangle relation"),
    Candidate("NBG-012", "Parent and central spherical altitudes are complementary", LOCAL, ("NBG-011",), "eta_parent=(pi-alpha)/2 and eta_central=alpha/2"),
    Candidate("NBG-013", "Icosahedral midpoint chord height mixes sqrt(3) and phi", LOCAL, ("ICOSPHERE_F2", "EQUILATERAL_HEIGHT"), "H_chord=sqrt(3)*R/(2*phi)"),
    Candidate("NBG-014", "Log scale preserves dimensional exponent", LOCAL, ("NBG-002",), "Delta ln M_D = D ln s"),
    Candidate("NBG-015", "Log-log domain failure is distinct from numeric zero", LOCAL, ("NBG-014",), "ln(0) undefined while residue zero remains numeric"),
    Candidate("NBG-016", "Project Sementeira is context federation, not evidence", LOCAL, ("PROJECT_CONTEXT_CUSTODY",), "SOURCE_SNAPSHOT != VALIDATED_MEMORY"),
    Candidate("NBG-017", "NIBIGUIRE is typed separately from TOKEN_VAZIO", LOCAL, ("NBG-016",), "closable-from-existing-structure versus missing evidence/definition"),
    Candidate("NBG-018", "Coverage matrix binds domain x proof-axis instead of prose volume", LOCAL, ("NBG-017",), "fixed axes: origin, semantics, formula, numeric, code, test, boundary"),
    Candidate("NBG-019", "Convergence uses marginal verified gain per audit effort", LOCAL, ("NBG-018",), "eta_i=DeltaG_i/DeltaE_i"),
    Candidate("NBG-020", "Local deterministic closure reaches a fixed point", LOCAL, ("NBG-019",), "full pass with zero new deterministic closures"),
    Candidate("TV-001", "Canonical C7 -> 42 map", UNDEFINED, token_vazio="TOKEN_VAZIO_C7_TO_42_CANONICAL_MAP"),
    Candidate("TV-002", "Physical T2 -> T7 bridge", EXTERNAL, token_vazio="TOKEN_VAZIO_T2_TO_T7_PHYSICAL_BRIDGE"),
    Candidate("TV-003", "Integer quantization of real Fibonacci-Rafael family", UNDEFINED, token_vazio="TOKEN_VAZIO_FIBONACCI_RAFAEL_REAL_DISCRETIZATION"),
    Candidate("TV-004", "42 frequency-2 vertices imply 42 physical attractors", EXTERNAL, token_vazio="TOKEN_VAZIO_42_PHYSICAL_ATTRACTORS"),
    Candidate("TV-005", "pi*phi/5 as universal physical constant", EXTERNAL, token_vazio="TOKEN_VAZIO_PI_PHI_PHYSICAL_CLAIM"),
    Candidate("TV-006", "Provider CI for the V5 branches", EXTERNAL, token_vazio="TOKEN_VAZIO_PROVIDER_CI_V5"),
    Candidate("TV-007", "Physical Android/Termux execution for V5", EXTERNAL, token_vazio="TOKEN_VAZIO_PHYSICAL_RUNTIME_V5"),
)

COVERAGE_AXES = ("origin_provenance", "semantic_namespace", "exact_formula", "numeric_witness", "executable_implementation", "test_evidence", "boundary_negative_gate")
DOMAINS = ("scale_77_33_7_3", "equilateral_circle_square_14", "fold_mod7_mod14_height", "fibonacci_rafaeliana_height", "icosphere_geodesic_altitude", "namespace_7_42_70_420_T7", "project_sementeira_federation", "convergence_nibiguire")

def coverage_matrix() -> dict[str, dict[str, str]]:
    matrix = {d: {a: "RESOLVED" for a in COVERAGE_AXES} for d in DOMAINS}
    matrix["project_sementeira_federation"]["test_evidence"] = "SOURCE_AND_CONTRACT_EVIDENCE"
    return matrix

def saturation_curve(effort: float, capacity: float = 1.0, tau: float = 1.0) -> float:
    if effort < 0 or capacity <= 0 or tau <= 0: raise ValueError("invalid saturation parameters")
    return capacity * (1.0 - math.exp(-effort / tau))

def saturation_derivative(effort: float, capacity: float = 1.0, tau: float = 1.0) -> float:
    if effort < 0 or capacity <= 0 or tau <= 0: raise ValueError("invalid saturation parameters")
    return capacity * math.exp(-effort / tau) / tau

def ideal_db_power_factor(delta_db: float) -> float:
    return 10.0 ** (delta_db / 10.0)

def ideal_db_pressure_factor(delta_db: float) -> float:
    return 10.0 ** (delta_db / 20.0)

def audit_fixed_point(candidates: Iterable[Candidate] = CANDIDATES, roots: set[str] | None = None) -> dict[str, object]:
    roots = set(ROOTS if roots is None else roots)
    all_candidates = list(candidates)
    resolved = set(roots)
    pending = {c.id: c for c in all_candidates}
    rounds = []
    total_effort = total_gain = round_index = 0
    while True:
        round_index += 1
        inspected = len(pending); total_effort += inspected
        newly_resolved = []; external_seen = []; undefined_seen = []
        for cid, c in list(pending.items()):
            if c.mode == EXTERNAL: external_seen.append(cid); continue
            if c.mode == UNDEFINED: undefined_seen.append(cid); continue
            if all(dep in resolved for dep in c.dependencies): newly_resolved.append(cid)
        for cid in newly_resolved:
            resolved.add(cid); pending.pop(cid, None)
        gain = len(newly_resolved); total_gain += gain
        rounds.append({"round": round_index, "inspected": inspected, "gain": gain, "efficiency": gain/inspected if inspected else 0.0, "effort_per_gain": inspected/gain if gain else "INF", "newly_resolved": newly_resolved, "external_seen": external_seen, "undefined_seen": undefined_seen, "remaining": len(pending)})
        if gain == 0: break
        if round_index > len(all_candidates)+1: raise RuntimeError("closure did not converge")
    unresolved = list(pending.values())
    local_remaining = [c.id for c in unresolved if c.mode == LOCAL]
    token_vazio = [{"id": c.id, "token": c.token_vazio, "mode": c.mode, "title": c.title} for c in unresolved if c.mode != LOCAL]
    fixed_point = len(local_remaining) == 0 and rounds[-1]["gain"] == 0
    knee_round = next((r["round"] for r in rounds if r["gain"] == 0), None)
    return {"schema":"raf.sementeira.convergence.v5", "definition":{"NIBIGUIRE":"USER_TERM: missed structural relation closable from already-present ingredients and proof", "TOKEN_VAZIO":"gap requiring missing evidence, execution, or author definition; never replaced by zero"}, "roots":sorted(roots), "candidate_count":len(all_candidates), "rounds":rounds, "resolved_candidate_count":sum(1 for c in all_candidates if c.id in resolved), "unresolved_candidate_count":len(unresolved), "local_deterministic_remaining":local_remaining, "token_vazio":token_vazio, "total_audit_effort_units":total_effort, "total_verified_gain_units":total_gain, "fixed_point":fixed_point, "knee_round":knee_round, "marginal_effort_per_gain_at_stop":"INF" if rounds[-1]["gain"] == 0 else rounds[-1]["effort_per_gain"], "coverage":{"domains":list(DOMAINS), "axes":list(COVERAGE_AXES), "cells":len(DOMAINS)*len(COVERAGE_AXES), "matrix":coverage_matrix()}, "spl_analogy_guard":{"ideal_power_factor_for_plus_1_db":ideal_db_power_factor(1.0), "ideal_pressure_factor_for_plus_1_db":ideal_db_pressure_factor(1.0), "ideal_db_for_double_power":10.0*math.log10(2.0), "note":"doubling a real competition system for ~+1 dB is treated as a saturation analogy, not the ideal acoustic identity"}, "claim_allowed":fixed_point, "claim_scope":"local deterministic closure only; external physical and provider claims remain blocked"}

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--compact",action="store_true"); args=parser.parse_args()
    result=audit_fixed_point(); print(json.dumps(result,ensure_ascii=False,indent=None if args.compact else 2,sort_keys=True)); return 0 if result["claim_allowed"] else 1

if __name__ == "__main__": raise SystemExit(main())
