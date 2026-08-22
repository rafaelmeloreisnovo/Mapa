#!/usr/bin/env python3
"""
Unit tests for Bootstrap & Uncertainty Quantification Engine.

Reference: data/analysis/bootstrap_uq.py
TV-CODE-2 closure: Bootstrap with deterministic seed, error propagation, model comparison
"""

import sys
import unittest
import statistics

# Add parent directory to path for imports
sys.path.insert(0, '/home/user/mapa')

from data.analysis.bootstrap_uq import (
    BootstrapEngine, ConfidenceInterval, ModelComparison, ModelType, UQStatus
)


class TestBootstrapEngine(unittest.TestCase):
    """Test cases for bootstrap engine."""

    def setUp(self):
        """Create bootstrap engine before each test."""
        self.engine = BootstrapEngine(seed=42, preregistered_coverage=0.95)

    def test_engine_initialization(self):
        """Test engine initialization."""
        self.assertEqual(self.engine.seed, 42)
        self.assertEqual(self.engine.preregistered_coverage, 0.95)
        self.assertEqual(self.engine.rng_state, 42)

    def test_deterministic_random(self):
        """Test that RNG is deterministic with fixed seed."""
        engine1 = BootstrapEngine(seed=42)
        engine2 = BootstrapEngine(seed=42)

        # Generate same sequence from both
        seq1 = [engine1._deterministic_random() for _ in range(5)]
        seq2 = [engine2._deterministic_random() for _ in range(5)]

        self.assertEqual(seq1, seq2, "Same seed should produce same sequence")

    def test_different_seeds_different_sequences(self):
        """Test that different seeds produce different sequences."""
        engine1 = BootstrapEngine(seed=42)
        engine2 = BootstrapEngine(seed=43)

        seq1 = [engine1._deterministic_random() for _ in range(5)]
        seq2 = [engine2._deterministic_random() for _ in range(5)]

        self.assertNotEqual(seq1, seq2, "Different seeds should produce different sequences")

    def test_bootstrap_ci_basic(self):
        """Test basic bootstrap CI computation."""
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        ci = self.engine.bootstrap_ci(data, lambda x: statistics.mean(x), n_resamples=1000)

        # CI should bracket the point estimate
        self.assertLess(ci.lower, ci.point_estimate)
        self.assertGreater(ci.upper, ci.point_estimate)

    def test_bootstrap_ci_contains_true_mean(self):
        """Falsifier: CI should contain the true point estimate."""
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        ci = self.engine.bootstrap_ci(data, lambda x: statistics.mean(x), n_resamples=1000)

        true_mean = statistics.mean(data)
        self.assertLessEqual(ci.lower, true_mean, "CI lower bound should be ≤ true mean")
        self.assertGreaterEqual(ci.upper, true_mean, "CI upper bound should be ≥ true mean")

    def test_bootstrap_ci_percentile_method(self):
        """Test percentile method for CI."""
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        ci = self.engine.bootstrap_ci(
            data,
            lambda x: statistics.mean(x),
            n_resamples=1000,
            ci_method="percentile"
        )

        self.assertEqual(ci.method, "percentile")
        self.assertIsNotNone(ci.lower)
        self.assertIsNotNone(ci.upper)

    def test_bootstrap_ci_basic_method(self):
        """Test basic method for CI."""
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        ci = self.engine.bootstrap_ci(
            data,
            lambda x: statistics.mean(x),
            n_resamples=1000,
            ci_method="basic"
        )

        self.assertEqual(ci.method, "basic")
        self.assertLess(ci.lower, ci.upper)

    def test_error_propagation_positive(self):
        """Falsifier: Propagated uncertainty should be positive."""
        data = [9.5, 10.0, 10.5, 10.2, 9.8]
        transformed_val, propagated_unc = self.engine.error_propagation(
            data,
            transform_func=lambda x: x ** 2,
            derivative_func=lambda x: 2 * x,
            n_resamples=1000
        )

        self.assertGreater(propagated_unc, 0, "Propagated uncertainty should be positive")

    def test_error_propagation_zero_derivative(self):
        """Test error propagation with near-zero derivative (uncertainty should diminish)."""
        data = [0.1, 0.05, 0.15, 0.08, 0.12]
        transformed_val, propagated_unc = self.engine.error_propagation(
            data,
            transform_func=lambda x: x ** 3,  # Large uncertainty near x=0
            derivative_func=lambda x: 3 * x ** 2,  # Derivative near zero for small x
            n_resamples=100
        )

        # Uncertainty should exist (test passes if no exception)
        self.assertIsNotNone(propagated_unc)

    def test_error_propagation_large_derivative(self):
        """Test error propagation amplifies with large derivative."""
        data_a = [5.0, 5.1, 4.9, 5.0, 5.05]
        data_b = [5.0, 5.1, 4.9, 5.0, 5.05]

        # Same data, but one uses large derivative
        _, unc_small = self.engine.error_propagation(
            data_a,
            transform_func=lambda x: x ** 2,
            derivative_func=lambda x: 0.1,  # Small derivative
            n_resamples=100
        )

        _, unc_large = self.engine.error_propagation(
            data_b,
            transform_func=lambda x: x ** 2,
            derivative_func=lambda x: 2 * x,  # Large derivative at x~5
            n_resamples=100
        )

        self.assertGreater(unc_large, unc_small, "Large derivative should amplify uncertainty")

    def test_model_comparison_returns_winner(self):
        """Test that model comparison returns a valid winner."""
        y_vals = [2*x + 1 for x in range(1, 11)]
        residuals_a = [0.0] * len(y_vals)  # Perfect fit for model A
        residuals_b = [0.1] * len(y_vals)  # Slightly worse for model B

        comparison = self.engine.compare_models(
            y_vals,
            model_a_func=lambda x: 2*x + 1,
            model_b_func=lambda x: x**1.5,
            residuals_a=residuals_a,
            residuals_b=residuals_b
        )

        self.assertIn(comparison.winner, ["a", "b", "tie"])

    def test_model_comparison_aic_diff_monotonic(self):
        """Falsifier: AIC difference should reflect model fit quality."""
        y_vals = list(range(1, 11))

        # Model A with perfect residuals
        residuals_a = [0.0] * len(y_vals)

        # Model B with poor residuals
        residuals_b = [1.0] * len(y_vals)

        comparison = self.engine.compare_models(
            y_vals,
            model_a_func=lambda x: x,
            model_b_func=lambda x: x + 1,
            residuals_a=residuals_a,
            residuals_b=residuals_b
        )

        # Model A (perfect fit) should win
        self.assertEqual(comparison.winner, "a", "Better model (lower residuals) should win")

    def test_model_comparison_confidence(self):
        """Test that model comparison assigns confidence."""
        y_vals = [1, 2, 3, 4, 5]
        residuals_a = [0.0] * len(y_vals)
        residuals_b = [2.0] * len(y_vals)

        comparison = self.engine.compare_models(
            y_vals,
            model_a_func=lambda x: x,
            model_b_func=lambda x: x + 1,
            residuals_a=residuals_a,
            residuals_b=residuals_b
        )

        self.assertGreater(comparison.confidence, 0)
        self.assertLessEqual(comparison.confidence, 1.0)

    def test_seed_reproducibility_ci(self):
        """Test that same seed produces same CI."""
        data = [1.0, 2.0, 3.0, 4.0, 5.0]

        engine1 = BootstrapEngine(seed=42)
        ci1 = engine1.bootstrap_ci(data, lambda x: statistics.mean(x), n_resamples=500)

        engine2 = BootstrapEngine(seed=42)
        ci2 = engine2.bootstrap_ci(data, lambda x: statistics.mean(x), n_resamples=500)

        self.assertAlmostEqual(ci1.lower, ci2.lower, places=5)
        self.assertAlmostEqual(ci1.upper, ci2.upper, places=5)


class TestFalsifiers(unittest.TestCase):
    """Falsifier tests (negative controls)."""

    def test_falsifier_ci_brackets_mean(self):
        """
        Falsifier: CI should contain the true mean.
        Negative control: If CI does not bracket true mean, it fails.
        """
        engine = BootstrapEngine(seed=42)
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        ci = engine.bootstrap_ci(data, lambda x: statistics.mean(x), n_resamples=1000)

        true_mean = statistics.mean(data)
        contains_mean = ci.lower <= true_mean <= ci.upper

        self.assertTrue(contains_mean, "Falsifier: CI must bracket true mean")

    def test_falsifier_uncertainty_propagation_positive(self):
        """
        Falsifier: Propagated uncertainty must be positive.
        Negative control: If uncertainty is non-positive, something is wrong.
        """
        engine = BootstrapEngine(seed=42)
        data = [5.0, 5.1, 4.9, 5.2, 4.8]
        _, unc = engine.error_propagation(
            data,
            lambda x: x ** 2,
            lambda x: 2 * x,
            n_resamples=500
        )

        self.assertGreater(unc, 0, "Falsifier: Uncertainty must be positive")

    def test_falsifier_model_comparison_decisive(self):
        """
        Falsifier: Model comparison with different residuals should be decisive.
        Negative control: If models with very different fits are tied, something is wrong.
        """
        engine = BootstrapEngine(seed=42)
        y_vals = list(range(1, 11))

        # Huge difference in residuals
        residuals_a = [0.0] * len(y_vals)  # Perfect
        residuals_b = [10.0] * len(y_vals)  # Terrible

        comparison = engine.compare_models(
            y_vals,
            lambda x: x,
            lambda x: x + 1,
            residuals_a=residuals_a,
            residuals_b=residuals_b
        )

        # Should strongly prefer model A
        self.assertEqual(comparison.winner, "a", "Falsifier: Clear difference should produce clear winner")
        self.assertGreater(comparison.confidence, 0.8, "Falsifier: Confidence should be high for clear win")


if __name__ == "__main__":
    unittest.main()
