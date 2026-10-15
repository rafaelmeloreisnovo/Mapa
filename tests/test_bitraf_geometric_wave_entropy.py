"""Exact source-bound geometrical falsifiers, no binary/device or entropy-gain claim.

This proves ONE 8-vertex tetrahedron-pair construction, not the user's
unresolved historical glue-map. All vertices and squared distances are ints.
"""
import copy
import itertools
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "data/geometry/bitraf_geometric_wave_entropy_route.v1.json"


def vertex(bits):
    """3 bits -> signs on cube corners; roundtrip without lossy parity merging."""
    if len(bits) != 3 or any(x not in (0, 1) for x in bits):
        raise ValueError("three exact binary states required")
    return tuple(1 - 2 * bit for bit in bits)


def decode(point):
    if len(point) != 3 or any(x not in (-1, 1) for x in point):
        raise ValueError("signed cube corner required")
    return tuple((1 - x) // 2 for x in point)


def squared_distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def inspect(contract):
    errors = []
    if contract.get("schema") != "rafaelia.bitraf.geometry-wave-entropy-route/v1":
        errors.append("SCHEMA_INVALID")
    if contract.get("claim_allowed") is not False or contract.get("core_intent", {}).get("is_compression") is not False:
        errors.append("COMPRESSION_OR_CLAIM_FALSE_PROMOTION")
    candidates = contract.get("tetra_pair_candidates", [])
    ids = {x.get("id"): x for x in candidates}
    for key, number in [
        ("OVERLAPPING_REGULAR_TETRA_CUBE8", 8),
        ("TETRA_FACE_GLUE", 5),
        ("TETRA_APEX_GLUE", 7),
        ("SQUARE_PYRAMID_MEDIAN_FOLDS", 5),
    ]:
        if ids.get(key, {}).get("distinct_vertices") != number:
            errors.append("GEOMETRIC_JOIN_CLASS_COLLISION:" + key)
    if ids.get("OVERLAPPING_REGULAR_TETRA_CUBE8", {}).get("state") != "MATHEMATICAL_EXAMPLE_NOT_AUTHOR_CONFIRMED":
        errors.append("UNCERTAIN_AUTHORIAL_GLUE_WAS_PROMOTED")
    if contract.get("binary_cube8_candidate", {}).get("bit_width") != 3:
        errors.append("EIGHT_VERTICES_MUST_NOT_BE_EIGHT_BITS")
    if contract.get("wave_candidate", {}).get("status") != "FORMAL_CANDIDATE_NOT_CODE_EXACT":
        errors.append("SINE_CLAIM_WAS_PROMOTED")
    if contract.get("status", {}).get("authorial_glue_map") != "TOKEN_VAZIO_SELECT_VARIANT":
        errors.append("GLUE_MAP_GAP_WAS_ERASED")
    if contract.get("status", {}).get("entropy_benefit") != "TOKEN_VAZIO_BENCHMARK":
        errors.append("ENTROPY_GAIN_UNPROVED")
    if not any("8 tetrahedron geometric vertices != 8 BitRAF extra registers" in x for x in contract.get("non_equivalence", [])):
        errors.append("GEOMETRY_BITRAF_REGISTER_ALIAS")
    if not any("W20 bridge" in x for x in contract.get("non_equivalence", [])):
        errors.append("W20_ROOT_SCOPE_REGRESSION")
    return sorted(set(errors))


class TestGeometricWaveIntent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(MODEL.read_text(encoding="utf-8"))

    def test_source_bound_types(self):
        self.assertEqual(inspect(self.contract), [])

    def test_all_eight_bit_labels_are_reversible(self):
        codes = list(itertools.product((0, 1), repeat=3))
        points = [vertex(code) for code in codes]
        self.assertEqual(len(set(points)), 8)
        self.assertEqual([decode(point) for point in points], codes)

    def test_two_tetrahedra_have_six_equal_edges_each(self):
        tetra = {0: [], 1: []}
        for code in itertools.product((0, 1), repeat=3):
            tetra[sum(code) % 2].append(vertex(code))
        self.assertEqual([len(tetra[0]), len(tetra[1])], [4, 4])
        self.assertFalse(set(tetra[0]) & set(tetra[1]))
        for vertices in tetra.values():
            distances = [squared_distance(a, b) for a, b in itertools.combinations(vertices, 2)]
            self.assertEqual(distances, [8] * 6)
            faces = list(itertools.combinations(vertices, 3))
            self.assertEqual(len(faces), 4)
            for f in faces:
                self.assertEqual(
                    [squared_distance(a, b) for a, b in itertools.combinations(f, 2)],
                    [8, 8, 8],
                )

    def test_entropy_distribution_invariant_under_bijection(self):
        """Equal exact histograms imply equal joint Shannon entropy for a relabeling."""
        populations = {code: n for code, n in zip(
            itertools.product((0, 1), repeat=3), (12, 1, 5, 0, 3, 7, 2, 9))}
        points = {vertex(code): freq for code, freq in populations.items()}
        self.assertEqual(len(points), 8)
        self.assertEqual(sorted(points.values()), sorted(populations.values()))
        # Parity ONLY is 4-to-1, and cannot replace the original identity.
        self.assertEqual(len({sum(code) % 2 for code in populations}), 2)

    def test_wrongly_claiming_w20_as_root_fails(self):
        d = copy.deepcopy(self.contract)
        d["non_equivalence"] = [x for x in d["non_equivalence"] if "W20 bridge" not in x]
        self.assertIn("W20_ROOT_SCOPE_REGRESSION", inspect(d))

    def test_overstating_eight_bits_fails(self):
        d = copy.deepcopy(self.contract)
        d["binary_cube8_candidate"]["bit_width"] = 8
        self.assertIn("EIGHT_VERTICES_MUST_NOT_BE_EIGHT_BITS", inspect(d))

    def test_geometric_collage_confusion_fails(self):
        d = copy.deepcopy(self.contract)
        next(x for x in d["tetra_pair_candidates"] if x["id"] == "TETRA_FACE_GLUE")["distinct_vertices"] = 8
        self.assertIn("GEOMETRIC_JOIN_CLASS_COLLISION:TETRA_FACE_GLUE", inspect(d))

    def test_unproved_sine_and_entropy_claims_fail(self):
        d = copy.deepcopy(self.contract)
        d["wave_candidate"]["status"] = "PASS_PHYSICAL"
        d["status"]["entropy_benefit"] = "PASS"
        errors = inspect(d)
        self.assertIn("SINE_CLAIM_WAS_PROMOTED", errors)
        self.assertIn("ENTROPY_GAIN_UNPROVED", errors)

    def test_invalid_coordinates_fail_closed(self):
        for bits in ((0, 1), (0, 2, 1), (0, 1, 1, 0)):
            with self.assertRaises(ValueError):
                vertex(bits)
        for signs in ((1, 0, 1), (0, 1), (2, 1, 1)):
            with self.assertRaises(ValueError):
                decode(signs)


if __name__ == "__main__":
    unittest.main()
