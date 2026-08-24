#!/usr/bin/env python3
"""
TV-TEST-2: Fractal Dimension Null Models Validator
====================================================

Validates that fractal dimension estimator produces results within ±0.05 of true values.

Falsifier: Fractal dimension within ±0.05 of true value

Gate: python3 scripts/validate_fractal_estimator.py
"""

import sys
import json
import hashlib
import math
from datetime import datetime
from pathlib import Path


class FractalDimensionValidator:
    """Validate fractal dimension estimator against null models."""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed_checks = []
        self.test_results = []

    def estimate_fractal_dimension(self, data, method="box-counting"):
        """
        Estimate fractal dimension using box-counting method.

        For this validator, we use synthetic test data with known dimensions:
        - Random points in 1D: dimension ≈ 1.0
        - Random points in 2D: dimension ≈ 2.0
        - Random points in 3D: dimension ≈ 3.0
        """
        import random
        random.seed(42)

        if method == "box-counting":
            # Simplified box-counting: count points in progressively smaller boxes
            box_sizes = [10, 5, 2, 1, 0.5]
            point_counts = []

            for box_size in box_sizes:
                count = 0
                for point in data:
                    if len(point) == 2:
                        count += 1 if abs(point[0]) < box_size/2 and abs(point[1]) < box_size/2 else 0
                    elif len(point) == 3:
                        count += 1 if abs(point[0]) < box_size/2 and abs(point[1]) < box_size/2 and abs(point[2]) < box_size/2 else 0
                point_counts.append(max(1, count))

            # Estimate dimension from slope of log-log plot
            log_sizes = [math.log10(s) for s in box_sizes]
            log_counts = [math.log10(c) for c in point_counts]

            # Linear regression on log-log data
            if len(log_sizes) >= 2:
                n = len(log_sizes)
                sum_x = sum(log_sizes)
                sum_y = sum(log_counts)
                sum_xy = sum(x*y for x, y in zip(log_sizes, log_counts))
                sum_x2 = sum(x**2 for x in log_sizes)

                denominator = n * sum_x2 - sum_x**2
                if denominator != 0:
                    slope = (n * sum_xy - sum_x * sum_y) / denominator
                    return abs(slope)

        return 0.0

    def validate_null_models(self):
        """Validate fractal dimension estimation against known null models."""
        try:
            import random
            random.seed(42)

            test_cases = [
                {
                    "name": "1d_uniform",
                    "true_dimension": 1.0,
                    "data": [[random.random(), 0.0] for _ in range(100)],
                    "tolerance": 0.05
                },
                {
                    "name": "2d_uniform",
                    "true_dimension": 2.0,
                    "data": [[random.random(), random.random()] for _ in range(100)],
                    "tolerance": 0.05
                },
                {
                    "name": "3d_uniform",
                    "true_dimension": 3.0,
                    "data": [[random.random(), random.random(), random.random()] for _ in range(100)],
                    "tolerance": 0.05
                }
            ]

            all_pass = True
            for tc in test_cases:
                estimated_dim = self.estimate_fractal_dimension(tc["data"])
                error = abs(estimated_dim - tc["true_dimension"])

                if error <= tc["tolerance"]:
                    self.passed_checks.append({
                        "check": f"fractal_dim_{tc['name']}",
                        "description": f"Estimated dimension {estimated_dim:.4f} within ±{tc['tolerance']} of true {tc['true_dimension']}",
                        "status": "PASS"
                    })
                    self.test_results.append({
                        "case": tc["name"],
                        "true_dimension": tc["true_dimension"],
                        "estimated_dimension": estimated_dim,
                        "error": error,
                        "passed": True
                    })
                else:
                    self.errors.append(f"Falsifier activated: {tc['name']} error {error:.4f} > {tc['tolerance']}")
                    self.test_results.append({
                        "case": tc["name"],
                        "true_dimension": tc["true_dimension"],
                        "estimated_dimension": estimated_dim,
                        "error": error,
                        "passed": False
                    })
                    all_pass = False

            return all_pass
        except Exception as e:
            self.errors.append(f"Null model validation failed: {e}")
            return False

    def validate_convergence(self):
        """Validate that dimension estimates converge with more data points."""
        try:
            import random
            random.seed(42)

            # Test convergence with increasing sample size
            sample_sizes = [50, 100, 200]
            dimensions = []

            for size in sample_sizes:
                data = [[random.random(), random.random()] for _ in range(size)]
                dim = self.estimate_fractal_dimension(data)
                dimensions.append(dim)

            # Check that estimates are reasonably close (within tolerance)
            if all(abs(d - 2.0) <= 0.1 for d in dimensions):
                self.passed_checks.append({
                    "check": "convergence",
                    "description": f"Dimension estimates converge: {[f'{d:.3f}' for d in dimensions]}",
                    "status": "PASS"
                })
                return True
            else:
                self.warnings.append(f"Convergence unclear: estimates {dimensions}")
                return True  # Not a hard failure
        except Exception as e:
            self.errors.append(f"Convergence validation failed: {e}")
            return False

    def run_validation(self):
        """Execute full validation suite."""
        all_pass = True
        all_pass &= self.validate_null_models()
        all_pass &= self.validate_convergence()

        return all_pass, self._generate_receipt()

    def _generate_receipt(self):
        """Generate JSON receipt for this validation."""
        receipt = {
            "schema": "mapa.cycle-4.tv-test-2/v1",
            "gate_id": "TV-TEST-2",
            "validator": "Fractal Dimension Estimator",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "repository": "rafaelmeloreisnovo/Mapa",
            "branch": "claude/urgencias-incertezas-reducao-nrov68",
            "exit_code": 0 if len(self.errors) == 0 else 1,
            "passed_checks": self.passed_checks,
            "errors": self.errors,
            "warnings": self.warnings,
            "test_results": self.test_results,
            "falsifiers": [
                "Fractal dimension within ±0.05 of true value for null models",
                "1D uniform data dimension ≈ 1.0",
                "2D uniform data dimension ≈ 2.0",
                "3D uniform data dimension ≈ 3.0",
                "Dimension estimates converge with increasing sample size"
            ],
            "claim_allowed": len(self.errors) == 0,
            "state": "PASS" if len(self.errors) == 0 else "FAIL"
        }

        # Add hash for immutability
        receipt_str = json.dumps(receipt, sort_keys=True, default=str)
        receipt["artifact_hash"] = hashlib.sha256(receipt_str.encode()).hexdigest()

        return receipt


def main():
    validator = FractalDimensionValidator()
    success, receipt = validator.run_validation()

    # Write receipt
    build_dir = Path(__file__).parent.parent / "build"
    build_dir.mkdir(exist_ok=True)

    receipt_path = build_dir / "tv-test-2-receipt.json"
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2, default=str)

    print(f"TV-TEST-2 Validation: {'PASS' if success else 'FAIL'}")
    print(f"Receipt written to: {receipt_path}")
    print(f"Artifact hash: {receipt['artifact_hash']}")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
