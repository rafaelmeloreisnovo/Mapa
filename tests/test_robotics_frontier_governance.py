import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FEDERATION = ROOT / "data" / "governance" / "robotics-user-sovereignty-federation.v1.json"
EVOLUTION = ROOT / "data" / "governance" / "robotics-normative-evolution.v1.json"
GEOMETRY = ROOT / "data" / "governance" / "robotics-dual-anchor-octant-geometry.v1.json"
HANDOFF = ROOT / "data" / "governance" / "robotics-lgpd-handoff-contract.v1.json"
UGC_SCHEMA = ROOT / "schemas" / "user-governance-capsule.v1.schema.json"
FRONTIER_DOC = ROOT / "docs" / "governance" / "CGEN_FRONTIER_RESEARCH_PROGRAM_V1.md"


def load(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class RoboticsFrontierGovernanceTests(unittest.TestCase):
    def test_all_machine_readable_artifacts_parse(self):
        for path in (FEDERATION, EVOLUTION, GEOMETRY, HANDOFF, UGC_SCHEMA):
            self.assertIsInstance(load(path), dict, path)

    def test_ugc_schema_preserves_core_epistemic_boundaries(self):
        schema = load(UGC_SCHEMA)
        required = set(schema["required"])
        for field in {
            "authority",
            "purposes",
            "data",
            "automation",
            "sharing",
            "retention",
            "rights",
            "risk",
            "evidence",
            "unknowns",
            "normative_snapshot",
            "receipt",
        }:
            self.assertIn(field, required)
        self.assertFalse(
            schema["properties"]["rights"]["properties"]["acknowledgement_is_consent"]["const"]
        )
        receipt_states = schema["properties"]["receipt"]["properties"]["state"]["enum"]
        self.assertIn("BLOCKED", receipt_states)
        self.assertIn("TOKEN_VAZIO", receipt_states)

    def test_normative_registry_contains_2026_brazil_and_eu_deltas(self):
        registry = load(EVOLUTION)
        ids = {source["id"] for source in registry["sources"]}
        for source_id in {
            "BR-ANPD-R32-2026",
            "BR-ECA-DIGITAL-15211-2025",
            "BR-LAW-15352-2026",
            "EU-AI-ACT-2024-1689-2026-1744",
            "ISO-IEC-27701-2025",
            "ISO-14001-2026",
        }:
            self.assertIn(source_id, ids)
        eu = next(s for s in registry["sources"] if s["id"] == "EU-AI-ACT-2024-1689-2026-1744")
        self.assertEqual(eu["timeline"]["general_application"], "2026-08-02")
        self.assertEqual(eu["timeline"]["annex_III_high_risk"], "2027-12-02")
        self.assertEqual(eu["timeline"]["annex_I_product_high_risk"], "2028-08-02")
        self.assertEqual(registry["normative_change_protocol"]["default_on_conflict_or_unknown"], "TOKEN_VAZIO_FAIL_CLOSED")

    def test_handoff_binds_exact_producer_and_does_not_fake_enrollment(self):
        handoff = load(HANDOFF)
        self.assertEqual(handoff["producer"]["observed_commit"], "ad0de98b4cd521fa9eefb05d5aac033e95b45a65")
        self.assertEqual(handoff["producer_evidence"]["conclusion"], "success")
        self.assertEqual(handoff["producer"]["formal_enrollment_in_mapa_authority_pyramid"], "TOKEN_VAZIO")
        self.assertIn("CI_success_to_legal_compliance", handoff["forbidden_promotions"])

    def test_dual_anchor_rotation_preserves_distance(self):
        c = (1.25, -0.75)
        v = (2.0, 3.0)
        base_norm = math.hypot(*v)
        for k in range(8):
            theta = k * math.pi / 4.0
            x = math.cos(theta) * v[0] - math.sin(theta) * v[1]
            y = math.sin(theta) * v[0] + math.cos(theta) * v[1]
            p = (c[0] + x, c[1] + y)
            q = (c[0] - x, c[1] - y)
            self.assertAlmostEqual(math.hypot(p[0] - c[0], p[1] - c[1]), base_norm, places=12)
            self.assertAlmostEqual(math.hypot(q[0] - c[0], q[1] - c[1]), base_norm, places=12)
            self.assertAlmostEqual(p[0] + q[0], 2.0 * c[0], places=12)
            self.assertAlmostEqual(p[1] + q[1], 2.0 * c[1], places=12)

    def test_octant_antipodal_quotient_is_four(self):
        points = [complex(math.cos(k * math.pi / 4), math.sin(k * math.pi / 4)) for k in range(8)]
        for k in range(4):
            self.assertAlmostEqual((points[k + 4] + points[k]).real, 0.0, places=12)
            self.assertAlmostEqual((points[k + 4] + points[k]).imag, 0.0, places=12)
        classes = [{k, k + 4} for k in range(4)]
        self.assertEqual(len(classes), 4)

    def test_even_and_odd_octant_vertices_are_two_rotated_squares(self):
        points = [(math.cos(k * math.pi / 4), math.sin(k * math.pi / 4)) for k in range(8)]
        for subset in ([0, 2, 4, 6], [1, 3, 5, 7]):
            side_lengths = []
            for i in range(4):
                a = points[subset[i]]
                b = points[subset[(i + 1) % 4]]
                side_lengths.append(math.hypot(a[0] - b[0], a[1] - b[1]))
            self.assertLess(max(side_lengths) - min(side_lengths), 1e-12)
        self.assertAlmostEqual(math.atan2(points[1][1], points[1][0]), math.pi / 4, places=12)

    def test_cube_center_section_is_regular_hexagon(self):
        a = 2.0
        vertices = [
            (a, -a, 0.0),
            (a, 0.0, -a),
            (0.0, a, -a),
            (-a, a, 0.0),
            (-a, 0.0, a),
            (0.0, -a, a),
        ]
        radii = []
        sides = []
        for i, p in enumerate(vertices):
            self.assertAlmostEqual(sum(p), 0.0, places=12)
            self.assertTrue(all(-a <= coordinate <= a for coordinate in p))
            radii.append(math.sqrt(sum(coordinate * coordinate for coordinate in p)))
            q = vertices[(i + 1) % len(vertices)]
            sides.append(math.sqrt(sum((p[j] - q[j]) ** 2 for j in range(3))))
        expected = math.sqrt(2.0) * a
        self.assertTrue(all(abs(r - expected) < 1e-12 for r in radii))
        self.assertTrue(all(abs(s - expected) < 1e-12 for s in sides))
        area = 3.0 * math.sqrt(3.0) * a * a
        self.assertGreater(area, 0.0)

    def test_geometry_registry_keeps_unproved_claims_open(self):
        geometry = load(GEOMETRY)
        self.assertEqual(geometry["cube_hexagon"]["claim_state"], "THEOREM")
        self.assertEqual(geometry["cube_hexagon"]["mechanical_optimality"], "TOKEN_VAZIO")
        self.assertEqual(geometry["spiral"]["radial"]["state"], "PASS_NUMERIC_LIMITED")
        self.assertEqual(
            geometry["spiral"]["angular_authorial"]["state"],
            "FAIL_NOT_SAME_FORM_AS_OBSERVED_GAIA_IMPLEMENTATION",
        )

    def test_frontier_document_separates_metaphor_from_proof(self):
        text = FRONTIER_DOC.read_text(encoding="utf-8")
        for marker in [
            "METAPHOR != MECHANISM",
            "ANALOGY != PROOF",
            "MECHANICAL_OPTIMALITY = TOKEN_VAZIO_HYPOTHESIS",
            "π/4 != π/φ != 2π/φ²",
        ]:
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
