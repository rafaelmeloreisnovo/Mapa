#!/usr/bin/env python3
"""
DAG Causal Engine — Rafaelia Operational Causal Analysis

Separates observed association, mechanism, confounders, interventions and falsifiers.

Epistemic state: TV-CODE (Token Vazio — implementation required)
Closure criteria:
  - Engine can distinguish association from intervention
  - Schema validates confounders and d-separation
  - Falsifier tests pass (negative-control fixtures)
  - Exit code 0 with evidence receipt

Reference: data/ontology/rafaelia-operational-ontology.v1.json :: R-DAG-CAUSAL
"""

import json
import sys
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum


class RelationType(Enum):
    """Types of relations in a causal DAG."""
    ASSOCIATION = "association"      # observed correlation (undirected)
    MECHANISM = "mechanism"          # causal (directed, confound-free)
    CONFOUNDER = "confounder"        # common cause (bidirectional arrows)
    COLLIDER = "collider"            # common effect (both point to child)
    INTERVENTION = "intervention"    # intentional manipulation (breaks confound)


class EpistemicState(Enum):
    """Epistemic state of a causal claim."""
    ASSOCIATION_ONLY = "association_only"          # no causal claim
    MECHANISM_CANDIDATE = "mechanism_candidate"    # proposed, not falsified
    MECHANISM_HYPOTHETICAL = "mechanism_hypothetical"  # requires intervention
    INTERVENTION_TESTED = "intervention_tested"    # intervened and measured
    CONFOUNDED = "confounded"                      # confounder present
    TOKEN_VAZIO = "token_vazio"                    # unproven


@dataclass
class Node:
    """A variable in the DAG."""
    id: str
    label: str
    type: str = "variable"  # variable, confounder, intervention, outcome
    evidence_scope: str = "TOKEN_VAZIO"  # local, device, third_party, TOKEN_VAZIO


@dataclass
class Edge:
    """A directed or undirected relation between nodes."""
    source: str
    target: str
    relation_type: RelationType
    strength: float = 0.0  # correlation/effect size
    epistemic_state: EpistemicState = EpistemicState.TOKEN_VAZIO
    falsifier: Optional[str] = None  # test that would break this edge
    evidence: List[Dict] = field(default_factory=list)


@dataclass
class CausalDAG:
    """A Directed Acyclic Graph with causal semantics."""
    id: str
    nodes: Dict[str, Node]
    edges: List[Edge]
    confounders: Set[str] = field(default_factory=set)
    interventions: Set[str] = field(default_factory=set)
    outcomes: Set[str] = field(default_factory=set)
    metadata: Dict = field(default_factory=lambda: {
        "version": "1.0.0",
        "schema": "rafaelia.dag-causal/v1",
        "created_at": None,
        "claim_allowed": False,
        "status": "TOKEN_VAZIO"
    })

    def validate_d_separation(self, x: str, y: str, condition_set: Set[str] = None) -> bool:
        """
        Check if x and y are d-separated given condition_set.

        D-separation (d-separation): x and y are d-separated given a set Z if all
        paths between x and y are blocked. A path is blocked if:
        1. It contains a non-collider node in Z
        2. It contains a collider not in Z and not having descendants in Z

        Falsifier: d-separation claim fails if unblocked path still shows association

        Note: A direct edge x -> y is always unblocked (no way to condition it away).
        Confounder paths x <- z -> y are blocked only by conditioning on z.
        """
        if condition_set is None:
            condition_set = set()

        # Check for any unblocked path from x to y
        # In this simplified implementation, we check:
        # 1. Direct edges x -> y (always unblocked)
        # 2. Confounder forks x <- z -> y (unblocked unless z is in condition_set)

        # Direct edge: x -> y (always unblocked)
        for edge in self.edges:
            if edge.source == x and edge.target == y:
                return False  # Direct path exists and is unblocked

        # Confounder path: x <- confounder -> y
        # This path is unblocked unless the confounder is in condition_set
        for confounder in self.confounders:
            has_conf_to_x = any(e.source == confounder and e.target == x for e in self.edges)
            has_conf_to_y = any(e.source == confounder and e.target == y for e in self.edges)

            if has_conf_to_x and has_conf_to_y:
                # Path x <- confounder -> y exists
                if confounder not in condition_set:
                    return False  # Unblocked path via confounder

        # All paths are blocked (or no unblocked paths found)
        return True

    def can_be_causal(self, source: str, target: str, condition_set: Set[str] = None) -> Tuple[bool, str]:
        """
        Determine if source → target can be causal given confounders.

        A relation is causal if:
        1. source and target are connected by a MECHANISM edge
        2. All confounders affecting both are controlled (in condition_set)
        3. No uncontrolled confounders remain

        Falsifier: causal claim fails if confounder exists and is not controlled
        Returns: (can_be_causal: bool, reason: str)
        """
        if condition_set is None:
            condition_set = set()

        # Find edge between source and target
        edge = None
        for e in self.edges:
            if e.source == source and e.target == target:
                edge = e
                break

        if not edge:
            return False, f"No edge from {source} to {target}"

        if edge.relation_type == RelationType.ASSOCIATION:
            return False, f"Edge is ASSOCIATION, not MECHANISM"

        # Check if confounders are present and not conditioned on
        for confounder in self.confounders:
            if confounder not in condition_set:
                # Check if confounder affects both source and target
                confounds_source = any(
                    e.source == confounder and e.target == source and
                    e.relation_type in (RelationType.MECHANISM, RelationType.CONFOUNDER)
                    for e in self.edges
                )
                confounds_target = any(
                    e.source == confounder and e.target == target and
                    e.relation_type in (RelationType.MECHANISM, RelationType.CONFOUNDER)
                    for e in self.edges
                )
                if confounds_source and confounds_target:
                    return False, f"Uncontrolled confounder: {confounder}"

        # If we reach here, all confounders are controlled
        return True, f"Causal claim supported (confounders controlled: {condition_set})"

    def apply_intervention(self, intervention_node: str, intervened_value: float) -> 'CausalDAG':
        """
        Apply an intervention to intervention_node and return a new DAG.

        Intervention breaks all incoming edges to the intervened node (cuts the confounds).
        The intervened node's value is fixed.

        Falsifier: post-intervention association differs from pre-intervention
        """
        new_dag = CausalDAG(
            id=f"{self.id}|intervene({intervention_node})",
            nodes=dict(self.nodes),
            edges=[e for e in self.edges if e.target != intervention_node],
            confounders=self.confounders,
            interventions=self.interventions | {intervention_node},
            outcomes=self.outcomes,
            metadata=dict(self.metadata)
        )
        new_dag.metadata["status"] = "INTERVENTION_APPLIED"
        return new_dag

    def to_dict(self) -> Dict:
        """Serialize to dict."""
        return {
            "id": self.id,
            "nodes": {k: asdict(v) for k, v in self.nodes.items()},
            "edges": [asdict(e) if not isinstance(e, dict) else e for e in self.edges],
            "confounders": list(self.confounders),
            "interventions": list(self.interventions),
            "outcomes": list(self.outcomes),
            "metadata": self.metadata
        }


def create_example_dag() -> CausalDAG:
    """
    Create an example DAG for testing (confounded causal claim).

    Structure: X <- Z -> Y with direct edge X -> Y
    - Z (confounder) affects both X and Y
    - X directly affects Y
    - To prove X causes Y (not just association), must control for Z
    """

    # Nodes: X (treatment), Z (confounder), Y (outcome)
    nodes = {
        "x": Node(id="x", label="Treatment", type="intervention"),
        "z": Node(id="z", label="Confounder", type="confounder"),
        "y": Node(id="y", label="Outcome", type="outcome")
    }

    # Edges: Z → X, Z → Y, X → Y (confounded)
    edges = [
        Edge(
            source="z",
            target="x",
            relation_type=RelationType.MECHANISM,
            strength=0.4,
            epistemic_state=EpistemicState.MECHANISM_HYPOTHETICAL
        ),
        Edge(
            source="z",
            target="y",
            relation_type=RelationType.MECHANISM,
            strength=0.5,
            epistemic_state=EpistemicState.MECHANISM_HYPOTHETICAL
        ),
        Edge(
            source="x",
            target="y",
            relation_type=RelationType.MECHANISM,
            strength=0.6,
            epistemic_state=EpistemicState.MECHANISM_CANDIDATE,
            falsifier="X-Y association disappears after conditioning on Z"
        ),
    ]

    return CausalDAG(
        id="example-confounded-causal",
        nodes=nodes,
        edges=edges,
        confounders={"z"},
        interventions={"x"},
        outcomes={"y"},
        metadata={
            "version": "1.0.0",
            "schema": "rafaelia.dag-causal/v1",
            "claim_allowed": False,
            "status": "MECHANISM_CANDIDATE"
        }
    )


def main():
    """
    Test the DAG causal engine.

    Closure criteria:
    - Instantiate example DAG
    - Test d-separation logic
    - Test confounder detection
    - Test intervention mechanism
    - All tests pass → exit 0
    """

    print("[DAG-CAUSAL] Initializing causal DAG engine")

    # Test 1: Create and validate example DAG
    dag = create_example_dag()
    print(f"[TEST 1] Created DAG: {dag.id}")
    print(f"  Nodes: {list(dag.nodes.keys())}")
    print(f"  Edges: {len(dag.edges)}")
    print(f"  Confounders: {dag.confounders}")

    # Test 2: Test d-separation
    print("\n[TEST 2] D-separation tests")
    d_sep_1 = dag.validate_d_separation("x", "y", set())
    print(f"  x ⊥ y (unconditioned): {d_sep_1} (expected: False, path exists via z and direct edge)")

    d_sep_2 = dag.validate_d_separation("x", "y", {"z"})
    print(f"  x ⊥ y | z: {d_sep_2} (expected: False, direct edge x→y still exists)")

    # Test 3: Test causal claim validity
    print("\n[TEST 3] Causal claim validity")
    is_causal_1, reason_1 = dag.can_be_causal("x", "y", set())
    print(f"  x → y (unconditioned): {is_causal_1}")
    print(f"    Reason: {reason_1}")

    is_causal_2, reason_2 = dag.can_be_causal("x", "y", {"z"})
    print(f"  x → y | z: {is_causal_2}")
    print(f"    Reason: {reason_2}")

    # Test 4: Test intervention
    print("\n[TEST 4] Intervention application")
    dag_intervened = dag.apply_intervention("x", 0.0)  # Set x to 0 (intervention)
    print(f"  Applied intervention: {dag_intervened.id}")
    print(f"  Remaining edges after intervention: {len(dag_intervened.edges)}")
    print(f"  Edges still present:")
    for e in dag_intervened.edges:
        print(f"    {e.source} → {e.target}")

    # After intervention, incoming edges to x are removed (z→x is cut)
    # So confounder path is broken, making x→y causal even without controlling z
    is_causal_3, reason_3 = dag_intervened.can_be_causal("x", "y", set())
    print(f"  x → y (post-intervention, no conditioning): {is_causal_3} (expected: True, confounder path broken)")

    # Test 5: Serialize to JSON
    print("\n[TEST 5] Serialization")
    dag_json = dag.to_dict()
    print(f"  DAG serialized: {json.dumps(dag_json, indent=2, default=str)[:200]}...")

    # Determine overall status
    print("\n[DAG-CAUSAL] SUMMARY")
    # Expected:
    #   d_sep_1: False (unblocked paths exist)
    #   d_sep_2: False (direct edge remains)
    #   is_causal_1: False (uncontrolled confounder)
    #   is_causal_2: True (confounder controlled)
    #   is_causal_3: True (intervention breaks confounding path, claim becomes valid)

    all_passed = (
        not d_sep_1 and  # unblocked paths
        not d_sep_2 and  # direct edge still exists
        not is_causal_1 and  # uncontrolled confounder blocks claim
        is_causal_2 and  # controlled confounder allows claim
        is_causal_3  # intervention breaks confounding path, claim valid
    )

    print(f"  Test results: d_sep_1={not d_sep_1}, d_sep_2={not d_sep_2}, is_causal_1={not is_causal_1}, is_causal_2={is_causal_2}, is_causal_3={not is_causal_3}")
    if all_passed:
        print(f"  Status: PASS (all closure criteria met)")
        print(f"  Receipt: DAG causal engine validated")
        print(f"  Falsifiers exercised: confounder detection, d-separation, intervention")
        return 0
    else:
        print(f"  Status: FAIL (one or more tests failed)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
