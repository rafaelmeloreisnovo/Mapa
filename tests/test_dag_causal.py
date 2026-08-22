#!/usr/bin/env python3
"""
Unit tests for DAG Causal Engine.

Reference: data/analysis/dag_causal_engine.py
TV-CODE-1 closure: Engine can distinguish association from intervention
"""

import sys
import unittest

# Add parent directory to path for imports
sys.path.insert(0, '/home/user/mapa')

from data.analysis.dag_causal_engine import (
    CausalDAG, Node, Edge, RelationType, EpistemicState,
    create_example_dag
)


class TestDAGCausal(unittest.TestCase):
    """Test cases for DAG causal engine."""

    def setUp(self):
        """Create test DAG before each test."""
        self.dag = create_example_dag()

    def test_dag_creation(self):
        """Test basic DAG creation."""
        self.assertEqual(self.dag.id, "example-confounded-causal")
        self.assertEqual(len(self.dag.nodes), 3)
        self.assertEqual(len(self.dag.edges), 3)
        self.assertIn("z", self.dag.confounders)

    def test_d_separation_unconditioned(self):
        """Test d-separation without conditioning (should have unblocked path)."""
        # x → y with z as confounder
        # Should find path: x → y (direct edge) and x ← z → y (confounder fork)
        d_sep = self.dag.validate_d_separation("x", "y", set())
        self.assertFalse(d_sep, "Expected unblocked path from x to y")

    def test_d_separation_conditioned(self):
        """Test d-separation with confounder controlled."""
        # When conditioning on z (the confounder), confounder fork is blocked
        # But direct edge x→y remains unblocked
        d_sep = self.dag.validate_d_separation("x", "y", {"z"})
        self.assertFalse(d_sep, "Expected unblocked direct path x→y even after conditioning on z")

    def test_causal_claim_unconditioned(self):
        """Test that causal claim fails without controlling confounders."""
        is_causal, reason = self.dag.can_be_causal("x", "y", set())
        self.assertFalse(is_causal, f"Causal claim should fail without controlling confounders: {reason}")

    def test_causal_claim_conditioned(self):
        """Test that causal claim succeeds when confounders are controlled."""
        is_causal, reason = self.dag.can_be_causal("x", "y", {"z"})
        self.assertTrue(is_causal, f"Causal claim should succeed with confounders controlled: {reason}")

    def test_intervention_removes_incoming_edges(self):
        """Test that intervention removes incoming edges to intervened node."""
        dag_intervened = self.dag.apply_intervention("x", 0.0)

        # After intervention, x should have no incoming edges
        incoming_to_x = [e for e in dag_intervened.edges if e.target == "x"]
        self.assertEqual(len(incoming_to_x), 0, "Intervention should remove all incoming edges")

    def test_intervention_breaks_causal_chain(self):
        """Test that intervention breaks confounding path and validates causal claim."""
        dag_intervened = self.dag.apply_intervention("x", 0.0)

        # After intervention, z→x is removed, so x→y becomes causal (no confounder)
        is_causal, _ = dag_intervened.can_be_causal("x", "y", set())
        self.assertTrue(is_causal, "Causal claim should succeed after intervention breaks confounding path")

    def test_confounder_detection(self):
        """Test that confounders are correctly identified."""
        self.assertIn("z", self.dag.confounders)
        self.assertEqual(len(self.dag.confounders), 1)

    def test_outcome_tracking(self):
        """Test that outcomes are correctly tracked."""
        self.assertIn("y", self.dag.outcomes)

    def test_intervention_tracking(self):
        """Test that interventions are tracked."""
        self.assertIn("x", self.dag.interventions)

    def test_serialization(self):
        """Test DAG serialization to dict."""
        dag_dict = self.dag.to_dict()

        self.assertEqual(dag_dict["id"], self.dag.id)
        self.assertEqual(len(dag_dict["nodes"]), 3)
        self.assertEqual(len(dag_dict["edges"]), 3)
        self.assertEqual(set(dag_dict["confounders"]), {"z"})

    def test_no_edge_between_unconnected_nodes(self):
        """Test that causal claim fails for unconnected nodes."""
        is_causal, reason = self.dag.can_be_causal("lungcancer", "smoking", set())
        self.assertFalse(is_causal, f"Should fail for reverse direction: {reason}")

    def test_edge_relation_type_matters(self):
        """Test that edge relation type (ASSOCIATION vs MECHANISM) affects causality."""
        # Create a new DAG with ASSOCIATION edge only
        nodes = {
            "x": Node(id="x", label="X"),
            "y": Node(id="y", label="Y")
        }
        edges = [
            Edge(
                source="x",
                target="y",
                relation_type=RelationType.ASSOCIATION,  # Not causal
                strength=0.5
            )
        ]
        dag_assoc = CausalDAG(id="assoc-only", nodes=nodes, edges=edges)

        is_causal, _ = dag_assoc.can_be_causal("x", "y", set())
        self.assertFalse(is_causal, "ASSOCIATION edge should not support causal claim")


class TestFalsifiers(unittest.TestCase):
    """Test falsifier scenarios (negative control tests)."""

    def test_falsifier_confounder_blocks_causal_claim(self):
        """
        Falsifier: If an uncontrolled confounder exists, causal claim should fail.
        Negative control: Presence of confounder should break the claim.
        """
        dag = create_example_dag()

        # Without controlling z (the confounder), claim should fail
        is_causal_uncond, _ = dag.can_be_causal("x", "y", set())
        self.assertFalse(is_causal_uncond, "Falsifier violated: uncontrolled confounder did not break claim")

        # With control, claim should pass
        is_causal_cond, _ = dag.can_be_causal("x", "y", {"z"})
        self.assertTrue(is_causal_cond, "Controlled claim should pass")

    def test_falsifier_intervention_removes_causality(self):
        """
        Falsifier: Intervention that removes incoming edges should break confounder path.
        Negative control: Intervening on a node should remove incoming edges.
        """
        dag = create_example_dag()
        dag_int = dag.apply_intervention("x", 0.0)

        # After intervention, z no longer causes x
        is_causal_pre = any(
            e.source == "z" and e.target == "x"
            for e in dag.edges
        )
        is_causal_post = any(
            e.source == "z" and e.target == "x"
            for e in dag_int.edges
        )

        self.assertTrue(is_causal_pre, "Pre-intervention: z should cause x")
        self.assertFalse(is_causal_post, "Post-intervention: z should not cause x")


if __name__ == "__main__":
    unittest.main()
