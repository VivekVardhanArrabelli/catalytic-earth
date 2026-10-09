import math
import unittest

from tools.research_lanes.protease_retargeting.tev_censoring_identifiability import (
    interaction_interval,
    witness_unbounded_efficiency,
)


class TevCensoringIdentifiabilityTest(unittest.TestCase):
    def test_arbitrarily_large_efficiency_can_remain_nondetected(self):
        for efficiency in (1.0, 1e3, 1e9):
            witness = witness_unbounded_efficiency(
                efficiency, [0.1, 1.0, 100.0], [1e-4, 2e-4, 3e-4]
            )
            self.assertEqual(witness["efficiency"], efficiency)
            self.assertTrue(
                all(rate < bound for rate, bound in zip(witness["rates"], [1e-4, 2e-4, 3e-4]))
            )

    def test_censored_off_diagonals_can_bound_fixed_condition_interaction(self):
        lower, upper = interaction_interval(
            (math.log(8), math.log(12)),
            (math.log(8), math.log(12)),
            (-math.inf, math.log(2)),
            (-math.inf, math.log(2)),
        )
        self.assertAlmostEqual(lower, math.log(16))
        self.assertEqual(upper, math.inf)

    def test_censored_diagonal_cannot_support_positive_interaction(self):
        lower, _ = interaction_interval(
            (-math.inf, math.log(2)),
            (math.log(8), math.log(12)),
            (-math.inf, math.log(2)),
            (-math.inf, math.log(2)),
        )
        self.assertEqual(lower, -math.inf)


if __name__ == "__main__":
    unittest.main()
