"""Offline tests for the reaction-aware cap wiring in the sourcing runners.

The governor's ``reaction_aware_cap`` and the gate's ``per_reaction_cap`` are the
forward-prevention levers; this module verifies they are wired into the runners'
shared cap guard and admission call without breaking the historical (flag-off)
behavior. No network: the helpers are exercised on synthetic registry-shaped rows,
and runner propagation is checked through the injected-fetcher harness.
"""

from __future__ import annotations

import unittest

from catalytic_earth.coverage_redundancy_audit import DEFAULT_TARGET_FLOOR
from catalytic_earth.novelty_admission_gate import DiversityState, evaluate_batch
from catalytic_earth.stage1_hole_sourcing import (
    _distinct_reactions_by_fingerprint,
    _reaction_aware_cap_guard,
)


def _row(entry_id, fp, *, rhea=("RHEA:1",), label_type="seed_fingerprint", organism="o"):
    return {
        "entry_id": entry_id,
        "label_type": label_type,
        "fingerprint_id": fp,
        "evidence": {
            "source_provenance": {"organism": organism, "sequence_length": 400},
            "mechanism_evidence": {
                "ec_numbers": ["1.1.1.1"],
                "reaction_equations": [{"rhea_id": r} for r in rhea],
            },
        },
    }


class DistinctReactionsByFingerprintTests(unittest.TestCase):
    def test_counts_distinct_concrete_reactions_seed_only(self) -> None:
        rows = [
            _row("a", "fpA", rhea=("RHEA:1", "RHEA:2")),
            _row("b", "fpA", rhea=("RHEA:2",)),  # repeat -> still 2 distinct
            _row("c", "fpB", rhea=("RHEA:9",)),
            _row("d", "fpA", rhea=("RHEA:5",), label_type="out_of_scope"),  # ignored
        ]
        got = _distinct_reactions_by_fingerprint(rows)
        self.assertEqual(got["fpA"], 2)
        self.assertEqual(got["fpB"], 1)

    def test_merges_across_registries(self) -> None:
        frozen = [_row("f1", "fpA", rhea=("RHEA:1",))]
        expansion = [_row("e1", "fpA", rhea=("RHEA:2",))]
        got = _distinct_reactions_by_fingerprint(frozen, expansion)
        self.assertEqual(got["fpA"], 2)


class ReactionAwareCapGuardTests(unittest.TestCase):
    def _admitted(self, fp, n):
        return [_row(f"{fp}_{i}", fp, organism=f"org{i}") for i in range(n)]

    def test_flag_off_is_flat_cap_backcompat(self) -> None:
        # base cap 5, nothing existing -> exactly 5 kept, rest trimmed (historical).
        admitted, trimmed, caps = _reaction_aware_cap_guard(
            self._admitted("fpA", 10),
            combined_counts={},
            base_cap_for=lambda fp: 5,
            reaction_aware_caps=False,
        )
        self.assertEqual(len(admitted), 5)
        self.assertEqual(len(trimmed), 5)
        self.assertEqual(caps["fpA"], 5)

    def test_single_reaction_family_bounded_at_floor(self) -> None:
        # distinct_reactions=1 -> clamp(rate*1, floor, ceiling) = floor (100). With 95
        # already present only 5 more fit before the floor cap bites.
        admitted, trimmed, caps = _reaction_aware_cap_guard(
            self._admitted("fpA", 20),
            combined_counts={"fpA": 95},
            base_cap_for=lambda fp: 250,
            reaction_aware_caps=True,
            reaction_cap_rate=8,
            target_floor=DEFAULT_TARGET_FLOOR,
            distinct_reactions_by_fp={"fpA": 1},
        )
        self.assertEqual(caps["fpA"], 100)
        self.assertEqual(len(admitted), 5)
        self.assertEqual(len(trimmed), 15)

    def test_reaction_rich_family_earns_headroom(self) -> None:
        # distinct_reactions=20 -> clamp(8*20=160, 100, 250) = 160. 150 present -> 10 fit.
        admitted, trimmed, caps = _reaction_aware_cap_guard(
            self._admitted("fpA", 30),
            combined_counts={"fpA": 150},
            base_cap_for=lambda fp: 250,
            reaction_aware_caps=True,
            reaction_cap_rate=8,
            distinct_reactions_by_fp={"fpA": 20},
        )
        self.assertEqual(caps["fpA"], 160)
        self.assertEqual(len(admitted), 10)
        self.assertEqual(len(trimmed), 20)

    def test_per_family_base_ceiling_caps_reaction_aware(self) -> None:
        # base ceiling 150 (confusable) clamps even a reaction-rich family below 160.
        _, _, caps = _reaction_aware_cap_guard(
            self._admitted("fpA", 5),
            combined_counts={},
            base_cap_for=lambda fp: 150,
            reaction_aware_caps=True,
            reaction_cap_rate=8,
            distinct_reactions_by_fp={"fpA": 20},
        )
        self.assertEqual(caps["fpA"], 150)


class EvaluateBatchPerReactionCapTests(unittest.TestCase):
    def _state_one_saturated_reaction(self, fp, n=150):
        s = DiversityState()
        for i in range(n):
            s.absorb(_row(f"s{i}", fp, organism=f"org{i}", rhea=("RHEA:1001",)))
        return s

    def test_batch_default_admits_new_organism_same_reaction(self) -> None:
        state = self._state_one_saturated_reaction("plp_dependent_enzyme")
        batch = [_row("new", "plp_dependent_enzyme", organism="brand_new", rhea=("RHEA:1001",))]
        result = evaluate_batch(batch, state)  # per_reaction_cap default None
        self.assertIn("new", result["admit_entry_ids"])

    def test_batch_per_reaction_cap_throttles_saturated_reaction(self) -> None:
        state = self._state_one_saturated_reaction("plp_dependent_enzyme")
        batch = [_row("new", "plp_dependent_enzyme", organism="brand_new", rhea=("RHEA:1001",))]
        result = evaluate_batch(batch, state, per_reaction_cap=12)
        self.assertNotIn("new", result["admit_entry_ids"])
        self.assertEqual(
            result["reason_counts"].get("reaction_saturated_per_reaction_cap"), 1
        )


if __name__ == "__main__":
    unittest.main()
