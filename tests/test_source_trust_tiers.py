"""Offline validation of the source trust-tier / N-of-M corroboration / honest-counter policy."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.source_trust_tiers import (
    CORROBORATOR_AXES,
    HONEST_COUNTER_AXES,
    SOURCE_TRUST_TIERS,
    build_source_trust_tier_policy,
    evaluate_corroboration,
    write_source_trust_tier_policy,
)


class SourceTrustTierTests(unittest.TestCase):
    def test_tier_0_admits_with_one_corroborator(self) -> None:
        verdict = evaluate_corroboration(
            source_tier="source_tier_0",
            present_axes=["cofactor_or_cosubstrate"],
        )
        self.assertTrue(verdict["meets_n_of_m"])
        self.assertEqual(
            verdict["decision"], "admit_bronze_candidate_pending_governor_and_novelty_gate"
        )
        # Trust-tier admission still defers to the mandatory downstream gates.
        self.assertIn("coverage_redundancy_governor", verdict["still_requires"])
        self.assertIn("novelty_admission_gate", verdict["still_requires"])

    def test_tier_2_requires_three_independent_axes(self) -> None:
        two = evaluate_corroboration(
            source_tier="source_tier_2",
            present_axes=["reaction_or_rhea_or_ec_family", "cofactor_or_cosubstrate"],
        )
        self.assertFalse(two["meets_n_of_m"])
        self.assertEqual(two["decision"], "hold_insufficient_independent_corroboration")

        three = evaluate_corroboration(
            source_tier="source_tier_2",
            present_axes=[
                "reaction_or_rhea_or_ec_family",
                "cofactor_or_cosubstrate",
                "active_site_motif_or_residue_role",
            ],
        )
        self.assertTrue(three["meets_n_of_m"])
        self.assertEqual(
            three["decision"], "admit_bronze_candidate_pending_governor_and_novelty_gate"
        )

    def test_duplicate_axes_do_not_count_twice(self) -> None:
        verdict = evaluate_corroboration(
            source_tier="source_tier_2",
            present_axes=[
                "cofactor_or_cosubstrate",
                "cofactor_or_cosubstrate",
                "cofactor_or_cosubstrate",
            ],
        )
        self.assertEqual(verdict["distinct_corroborator_count"], 1)
        self.assertFalse(verdict["meets_n_of_m"])

    def test_tier_3_and_4_are_hypotheses_never_bronze(self) -> None:
        for tier in ("source_tier_3", "source_tier_4"):
            verdict = evaluate_corroboration(
                source_tier=tier,
                present_axes=list(CORROBORATOR_AXES),  # even with EVERY axis
            )
            self.assertFalse(verdict["bronze_eligible_tier"])
            self.assertEqual(verdict["decision"], "hold_hypothesis_not_countable_bronze")

    def test_unknown_axes_ignored(self) -> None:
        verdict = evaluate_corroboration(
            source_tier="source_tier_0",
            present_axes=["not_a_real_axis", "cofactor_or_cosubstrate"],
        )
        self.assertEqual(verdict["unknown_axes_ignored"], ["not_a_real_axis"])
        self.assertEqual(verdict["distinct_corroborator_count"], 1)

    def test_unknown_tier_raises(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_corroboration(source_tier="source_tier_9", present_axes=[])

    def test_only_tiers_0_1_2_are_bronze_eligible(self) -> None:
        eligible = {t for t, v in SOURCE_TRUST_TIERS.items() if v["bronze_eligible"]}
        self.assertEqual(eligible, {"source_tier_0", "source_tier_1", "source_tier_2"})
        # Escalating corroboration requirement away from reviewed Swiss-Prot.
        self.assertEqual(SOURCE_TRUST_TIERS["source_tier_0"]["min_independent_corroborators"], 1)
        self.assertEqual(SOURCE_TRUST_TIERS["source_tier_1"]["min_independent_corroborators"], 2)
        self.assertEqual(SOURCE_TRUST_TIERS["source_tier_2"]["min_independent_corroborators"], 3)

    def test_counter_ledger_keeps_axes_separate(self) -> None:
        frozen = [
            {"label_type": "seed_fingerprint", "tier": "bronze"},
            {"label_type": "out_of_scope", "tier": "bronze"},
        ]
        expansion = [
            {"label_type": "seed_fingerprint", "tier": "bronze"},
            {"label_type": "seed_fingerprint", "tier": "bronze"},
            {"label_type": "out_of_scope", "tier": "bronze"},
        ]
        policy = build_source_trust_tier_policy(
            frozen_benchmark_payload=frozen,
            expansion_payload=expansion,
            created_utc="2026-06-12T00:00:00Z",
        )
        ledger = policy["current_honest_counter_ledger"]
        self.assertEqual(ledger["positive_bronze_count"], 3)
        self.assertEqual(ledger["oos_bronze_count"], 2)
        self.assertEqual(ledger["silver_ready_count"], 0)
        self.assertEqual(ledger["silver_confirmed_count"], 0)
        self.assertEqual(ledger["projected_provisional_count"], 0)
        # The policy declares the counters must never be merged.
        self.assertTrue(policy["honest_counters_must_not_be_merged"])
        for axis in HONEST_COUNTER_AXES:
            self.assertIn(axis, ledger)

    def test_writer_non_destructive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frozen = Path(tmp) / "frozen.json"
            expansion = Path(tmp) / "expansion.json"
            frozen.write_text(json.dumps([{"label_type": "seed_fingerprint", "tier": "bronze"}]))
            expansion.write_text(json.dumps([{"label_type": "out_of_scope", "tier": "bronze"}]))
            frozen_before = frozen.read_bytes()
            out = Path(tmp) / "policy.json"
            policy = write_source_trust_tier_policy(
                out_path=out,
                frozen_benchmark_path=frozen,
                expansion_registry_path=expansion,
            )
            self.assertEqual(frozen.read_bytes(), frozen_before)
            self.assertTrue(out.exists())
            self.assertEqual(policy["current_honest_counter_ledger"]["positive_bronze_count"], 1)
            self.assertEqual(policy["current_honest_counter_ledger"]["oos_bronze_count"], 1)


if __name__ == "__main__":
    unittest.main()
