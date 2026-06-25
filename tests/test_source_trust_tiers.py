"""Offline validation of the source trust-tier / N-of-M corroboration / honest-counter policy."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.source_trust_tiers import (
    CORROBORATOR_AXES,
    HARD_MECHANISM_AXES,
    HONEST_COUNTER_AXES,
    NON_COUNTED_SCOPE_AXES,
    SOFT_SCOPE_LEANING_AXES,
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

    def test_name_or_family_alone_cannot_carry_a_bronze_label(self) -> None:
        # THE mechanism-not-EC rule: a family/name profile (domain_or_family_profile) is a SOFT
        # axis. Even though it satisfies the tier_0 count of 1, it carries NO hard mechanism
        # evidence, so it is held -- name + EC scope is necessary-context, never sufficient.
        verdict = evaluate_corroboration(
            source_tier="source_tier_0",
            present_axes=["ec_scope_hint", "domain_or_family_profile"],
        )
        self.assertTrue(verdict["meets_n_of_m"])  # count rule alone is satisfied...
        self.assertFalse(verdict["has_hard_mechanism_axis"])  # ...but no real chemistry
        self.assertEqual(verdict["hard_mechanism_axes_present"], [])
        self.assertEqual(
            verdict["decision"],
            "hold_no_hard_mechanism_axis_name_or_family_alone_insufficient",
        )

    def test_name_plus_one_hard_axis_admits(self) -> None:
        # The same name/family profile DOES corroborate once a hard mechanism axis (the actual
        # reaction transformation) is also present.
        verdict = evaluate_corroboration(
            source_tier="source_tier_0",
            present_axes=[
                "ec_scope_hint",
                "domain_or_family_profile",
                "rhea_reaction_or_participant_pattern",
            ],
        )
        self.assertTrue(verdict["has_hard_mechanism_axis"])
        self.assertEqual(
            verdict["hard_mechanism_axes_present"],
            ["rhea_reaction_or_participant_pattern"],
        )
        self.assertEqual(
            verdict["decision"], "admit_bronze_candidate_pending_governor_and_novelty_gate"
        )

    def test_hard_and_soft_axis_partition_is_clean(self) -> None:
        # HARD + SOFT exactly partition the counted axes; EC is in neither (it is scope-only).
        self.assertEqual(set(HARD_MECHANISM_AXES) | set(SOFT_SCOPE_LEANING_AXES), set(CORROBORATOR_AXES))
        self.assertEqual(set(HARD_MECHANISM_AXES) & set(SOFT_SCOPE_LEANING_AXES), set())
        self.assertNotIn("ec_scope_hint", HARD_MECHANISM_AXES)
        self.assertNotIn("ec_scope_hint", SOFT_SCOPE_LEANING_AXES)

    def test_tier_2_requires_three_independent_axes(self) -> None:
        two = evaluate_corroboration(
            source_tier="source_tier_2",
            present_axes=["rhea_reaction_or_participant_pattern", "cofactor_or_cosubstrate"],
        )
        self.assertFalse(two["meets_n_of_m"])
        self.assertEqual(two["decision"], "hold_insufficient_independent_corroboration")

        three = evaluate_corroboration(
            source_tier="source_tier_2",
            present_axes=[
                "rhea_reaction_or_participant_pattern",
                "cofactor_or_cosubstrate",
                "active_site_motif_or_residue_role",
            ],
        )
        self.assertTrue(three["meets_n_of_m"])
        self.assertEqual(
            three["decision"], "admit_bronze_candidate_pending_governor_and_novelty_gate"
        )

    def test_ec_alone_cannot_satisfy_n_of_m_even_at_tier_0(self) -> None:
        # EC is a scope hint, never a counted corroborator. Even at the most permissive
        # bronze-eligible tier (tier_0, required = 1), EC alone cannot admit a label.
        verdict = evaluate_corroboration(
            source_tier="source_tier_0", present_axes=["ec_scope_hint"]
        )
        self.assertEqual(verdict["distinct_corroborator_count"], 0)
        self.assertEqual(verdict["scope_hint_axes_present_not_counted"], ["ec_scope_hint"])
        # EC is recognized -> NOT flagged as unknown.
        self.assertEqual(verdict["unknown_axes_ignored"], [])
        self.assertFalse(verdict["meets_n_of_m"])
        self.assertEqual(verdict["decision"], "hold_insufficient_independent_corroboration")

    def test_ec_does_not_inflate_the_corroborator_count(self) -> None:
        # EC alongside ONE real mechanism corroborator still counts as one -- EC adds nothing.
        with_ec = evaluate_corroboration(
            source_tier="source_tier_0",
            present_axes=["ec_scope_hint", "cofactor_or_cosubstrate"],
        )
        self.assertEqual(with_ec["distinct_corroborator_count"], 1)
        self.assertEqual(with_ec["distinct_corroborator_axes"], ["cofactor_or_cosubstrate"])
        self.assertEqual(with_ec["scope_hint_axes_present_not_counted"], ["ec_scope_hint"])
        # tier_0 needs 1 mechanism corroborator -> the cofactor axis (not EC) satisfies it.
        self.assertTrue(with_ec["meets_n_of_m"])

        # tier_2 needs 3 mechanism axes; EC cannot backfill a missing one.
        ec_plus_two = evaluate_corroboration(
            source_tier="source_tier_2",
            present_axes=[
                "ec_scope_hint",
                "cofactor_or_cosubstrate",
                "active_site_motif_or_residue_role",
            ],
        )
        self.assertEqual(ec_plus_two["distinct_corroborator_count"], 2)
        self.assertFalse(ec_plus_two["meets_n_of_m"])

    def test_ec_family_axis_is_not_a_counted_corroborator(self) -> None:
        # The old lumped axis name is gone; EC is only ever a non-counted scope axis.
        self.assertNotIn("reaction_or_rhea_or_ec_family", CORROBORATOR_AXES)
        self.assertIn("rhea_reaction_or_participant_pattern", CORROBORATOR_AXES)
        self.assertIn("ec_scope_hint", NON_COUNTED_SCOPE_AXES)
        self.assertEqual(set(CORROBORATOR_AXES) & set(NON_COUNTED_SCOPE_AXES), set())

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
