from __future__ import annotations
import json, unittest
from pathlib import Path
from tools.spectral_geometry_experiment import build, cube, geodesic, icosa, tetra, validate

ROOT=Path(__file__).resolve().parents[2]
BASELINE=ROOT/"data/geometry/spectral_geometry_baseline.v1.json"

class SpectralGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline=json.loads(BASELINE.read_text(encoding="utf-8"))
        cls.fresh=build(cls.baseline["execution_context"])

    def test_topology_counts(self):
        self.assertEqual((len(tetra()[0]),len(tetra()[1])),(4,4))
        self.assertEqual((len(cube()[0]),len(cube()[1])),(8,12))
        ico=icosa()
        self.assertEqual((len(ico[0]),len(ico[1])),(12,20))
        self.assertEqual(tuple(map(len,geodesic(*ico,1))),(42,80))
        self.assertEqual(tuple(map(len,geodesic(*ico,2))),(162,320))

    def test_baseline_reproduces_exactly(self):
        self.assertEqual(self.fresh,self.baseline)

    def test_fail_closed_hash_and_claim_boundary(self):
        validate(self.fresh)
        self.assertIs(self.fresh["claim_allowed"],False)
        self.assertIs(self.fresh["automatic_promotion"],False)

    def test_convergence_is_observed_but_not_promoted(self):
        obs=self.fresh["continuous_discrete_convergence"]["observed"]
        self.assertTrue(all(obs.values()))
        rows=self.fresh["continuous_discrete_convergence"]["rows"]
        self.assertLess(rows[-1]["l2_relative_error"],0.03)
        self.assertLess(rows[-1]["l3_relative_error"],0.06)
        self.assertEqual(self.fresh["hypothesis_assessment"]["H1"],
            "PARTIAL_NUMERICAL_SUPPORT_FOR_CONTINUUM_DISCRETE_CONVERGENCE_ONLY")

    def test_registered_constants_do_not_match(self):
        scan=self.fresh["constant_scan"]
        self.assertIs(scan["any_match"],False)
        self.assertEqual(scan["tolerance_provenance"],
            "SET_IN_EXPERIMENT_V1_BEFORE_REMOTE_REPRODUCTION_NOT_BEFORE_REFERENCE_RUN")
        self.assertIs(scan["statistical_inference_performed"],False)
        self.assertEqual(scan["multiple_comparison_correction"],
            "NOT_APPLICABLE_DESCRIPTIVE_DISTANCE_ONLY")
        self.assertTrue(all(not x["match_within_experiment_v1_tolerance"] for x in scan["results"].values()))
        self.assertEqual(self.fresh["hypothesis_assessment"]["rafaelia_constants_as_spectral_invariants"],
                         "REJECT_CURRENT_PREREGISTERED_SCAN")

    def test_dependency_and_license_friction_reduced(self):
        p=self.fresh["dependency_profile"]
        self.assertEqual(p["third_party_runtime_dependencies"],[])
        self.assertIs(p["python_standard_library_only"],True)
        self.assertIs(p["license_added_by_experiment"],False)
        self.assertIs(p["repository_license_override"],False)

if __name__=="__main__": unittest.main()
