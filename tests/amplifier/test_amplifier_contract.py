import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


PARSER = load_module("amp_parser", ROOT / "tools" / "parse_amplified_expression.py")
BUILDER = load_module("amp_builder", ROOT / "tools" / "build_amplifier_fixture.py")

VALID = (
    "AMP{D=3;N=0;DELTA_ROLE=SHIFT;DELTA_VALUE=1;"
    "OMEGA_NUM=GEOMETRIC_MEAN;OMEGA_EPI=TERNARY_FAIL_CLOSED;"
    "PI_ROLE=CIRCULAR_CONSTANT;PHI_ROLE=GOLDEN_RATIO;"
    "EQUIV=NUMERIC_EQUAL;FUNCTION=F_TRANSITION}"
)


class AmplifierContractTests(unittest.TestCase):
    def test_parser_builds_typed_ast(self):
        ast = PARSER.parse_expression(VALID)
        self.assertEqual(ast["arity"], 3)
        self.assertEqual(ast["delta"]["role"], "SHIFT")
        self.assertEqual(ast["omega"]["epistemic"], "TERNARY_FAIL_CLOSED")
        self.assertFalse(ast["claim_allowed"])

    def test_untyped_delta_is_rejected(self):
        with self.assertRaises(PARSER.ParseError):
            PARSER.parse_expression(VALID.replace("DELTA_ROLE=SHIFT;", ""))

    def test_ambiguous_equivalence_is_rejected(self):
        with self.assertRaises(PARSER.ParseError):
            PARSER.parse_expression(VALID.replace("EQUIV=NUMERIC_EQUAL", "EQUIV==="))

    def test_fixture_generates_81_cells_and_sparse_edges(self):
        config = json.loads((ROOT / "data/fixtures/amplifier_d3.v1.json").read_text())
        fixture = BUILDER.build_fixture(config)
        self.assertEqual(config["expected_cell_count"], 81)
        self.assertEqual(fixture["cell_count"], 81)
        self.assertEqual(len(fixture["nodes"]), 81)
        self.assertEqual(len(fixture["edges"]), 81 * 4)

    def test_barycentric_coordinates_close(self):
        config = json.loads((ROOT / "data/fixtures/amplifier_d3.v1.json").read_text())
        fixture = BUILDER.build_fixture(config)
        for node in fixture["nodes"]:
            b = node["barycentric"]
            self.assertAlmostEqual(b["x"] + b["y"] + b["z"], 1.0)
            self.assertGreaterEqual(b["z"], 0.0)

    def test_edges_have_no_self_loops_and_bounded_rank(self):
        config = json.loads((ROOT / "data/fixtures/amplifier_d3.v1.json").read_text())
        fixture = BUILDER.build_fixture(config)
        for edge in fixture["edges"]:
            self.assertNotEqual(edge["source"], edge["target"])
            self.assertGreaterEqual(edge["score"], -1.0)
            self.assertLessEqual(edge["score"], 1.0)
            self.assertIn(edge["rank"], range(1, 5))

    def test_sparse_neighbor_order_matches_contract(self):
        self.assertEqual(
            BUILDER.nearest_neighbors((0, 0, 0, 0), 3, 4),
            [(1, "C-0001"), (1, "C-0003"), (1, "C-0009"), (1, "C-0027")],
        )

    def test_graph_policy_k_is_fail_closed(self):
        config = json.loads((ROOT / "data/fixtures/amplifier_d3.v1.json").read_text())
        for invalid_k in (-1, 17, True, "4", 4.0):
            bad = json.loads(json.dumps(config))
            bad["graph_policy"]["k"] = invalid_k
            with self.subTest(k=invalid_k):
                with self.assertRaises(ValueError):
                    BUILDER.build_fixture(bad)

    def test_d7_k16_stays_within_rapport_rank_contract(self):
        config = json.loads((ROOT / "data/fixtures/amplifier_d3.v1.json").read_text())
        config["fixture_id"] = "AMP-D7-ANTIREGRESSION"
        config["arity"] = 7
        config["graph_policy"]["k"] = 16
        fixture = BUILDER.build_fixture(config)
        self.assertEqual(fixture["cell_count"], 7 ** 4)
        self.assertEqual(len(fixture["edges"]), (7 ** 4) * 16)
        self.assertEqual(max(edge["rank"] for edge in fixture["edges"]), 16)


if __name__ == "__main__":
    unittest.main()
