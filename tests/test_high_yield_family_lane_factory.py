from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.high_yield_family_lane_factory import (
    HIGH_YIELD_FAMILY_SPECS,
    build_high_yield_family_lane_factory,
    evaluate_family_lane_spec,
    write_high_yield_family_lane_factory,
)


_NEW_SPEC = {
    "family_id": "new_clean_family",
    "display_name": "New clean family",
    "scope_query": "scope-new",
    "corroborator_query": "corrob-new",
    "required_non_ec_corroborators": ["cofactor handle"],
    "disambiguation_holds": ["off-target rows"],
    "cap_ceiling": 250,
    "chemistry_confusable": False,
    "novelty_keep_factor": 0.5,
    "rationale_template": "new family",
    "existing_fingerprint_id": None,
    "current_runner": None,
    "ambiguity_with_existing": [],
    "oos_preregistration_required": True,
}

_EXISTING_SPEC = {
    **_NEW_SPEC,
    "family_id": "existing_family_lane",
    "display_name": "Existing family lane",
    "scope_query": "scope-existing",
    "corroborator_query": "corrob-existing",
    "existing_fingerprint_id": "existing_family_lane",
    "current_runner": "scripts/source_existing_family.py",
    "oos_preregistration_required": False,
}


def _count_fetcher(query: str) -> dict[str, int]:
    totals = {
        "scope-new": 800,
        "corrob-new": 500,
        "scope-existing": 900,
        "corrob-existing": 600,
    }
    return {"total_results": totals[query]}


class HighYieldFamilyLaneFactoryTests(unittest.TestCase):
    def test_new_high_yield_family_is_blocked_for_preregistration(self) -> None:
        row = evaluate_family_lane_spec(
            _NEW_SPEC,
            registry_counts={},
            count_fetcher=_count_fetcher,
        )

        self.assertEqual(row["projected_clean_admits"], 250)
        self.assertEqual(
            row["batch_gate_status"],
            "blocked_new_fingerprint_oos_prereg_and_rule_required",
        )
        self.assertFalse(row["passes_150_batch_gate_now"])
        self.assertTrue(row["oos_preregistration_required"])
        self.assertEqual(row["non_ec_mechanism_corroboration_rate_estimate"], 0.625)

    def test_existing_lane_with_cap_room_can_be_ready_for_preview(self) -> None:
        row = evaluate_family_lane_spec(
            _EXISTING_SPEC,
            registry_counts={"existing_family_lane": 10},
            count_fetcher=_count_fetcher,
        )

        self.assertEqual(row["cap_room"], 240)
        self.assertEqual(row["projected_clean_admits"], 240)
        self.assertEqual(row["batch_gate_status"], "ready_for_preview_not_apply")
        self.assertTrue(row["passes_150_batch_gate_now"])

    def test_existing_lane_below_150_cap_room_is_blocked(self) -> None:
        row = evaluate_family_lane_spec(
            _EXISTING_SPEC,
            registry_counts={"existing_family_lane": 140},
            count_fetcher=_count_fetcher,
        )

        self.assertEqual(row["cap_room"], 110)
        self.assertEqual(
            row["batch_gate_status"],
            "blocked_existing_cap_room_below_150",
        )

    def test_discovery_compass_lanes_are_first_class_new_fingerprint_specs(self) -> None:
        specs = {spec["family_id"]: spec for spec in HIGH_YIELD_FAMILY_SPECS}

        self.assertIn("metal_independent_phosphodiesterase", specs)
        self.assertIn("n_ribosyl_hydrolase", specs)

        phosphodiesterase_row = evaluate_family_lane_spec(
            specs["metal_independent_phosphodiesterase"],
            registry_counts={},
            count_fetcher=lambda _query: {"total_results": 500},
        )
        self.assertEqual(
            phosphodiesterase_row["batch_gate_status"],
            "blocked_new_fingerprint_oos_prereg_and_runner_required",
        )
        self.assertFalse(phosphodiesterase_row["mechanism_rule_required"])
        self.assertEqual(
            phosphodiesterase_row["source_wall_rule_status"],
            "implemented_preview_only",
        )
        self.assertTrue(phosphodiesterase_row["oos_preregistration_required"])
        self.assertFalse(phosphodiesterase_row["passes_150_batch_gate_now"])

        n_ribosyl_row = evaluate_family_lane_spec(
            specs["n_ribosyl_hydrolase"],
            registry_counts={},
            count_fetcher=lambda _query: {"total_results": 500},
        )
        self.assertEqual(
            n_ribosyl_row["batch_gate_status"],
            "ready_for_preview_not_apply",
        )
        self.assertEqual(
            n_ribosyl_row["existing_fingerprint_id"],
            "n_ribosyl_hydrolase",
        )
        self.assertEqual(
            n_ribosyl_row["current_runner"],
            "scripts/source_n_ribosyl_hydrolase_family.py",
        )
        self.assertFalse(n_ribosyl_row["mechanism_rule_required"])
        self.assertEqual(
            n_ribosyl_row["source_wall_rule_status"],
            "implemented_preview_only",
        )
        self.assertTrue(n_ribosyl_row["oos_preregistration_required"])
        self.assertTrue(n_ribosyl_row["passes_150_batch_gate_now"])

    def test_build_rollup_keeps_honest_counters_separate(self) -> None:
        audit = build_high_yield_family_lane_factory(
            frozen_benchmark_payload=[
                {
                    "entry_id": "cur:1",
                    "label_type": "seed_fingerprint",
                    "fingerprint_id": "existing_family_lane",
                }
            ],
            expansion_payload=[
                {
                    "entry_id": "uniprot:A",
                    "label_type": "seed_fingerprint",
                    "fingerprint_id": "existing_family_lane",
                },
                {"entry_id": "uniprot:OOS", "label_type": "out_of_scope"},
            ],
            specs=(_NEW_SPEC, _EXISTING_SPEC),
            count_fetcher=_count_fetcher,
            created_utc="2026-06-14T00:00:00Z",
        )

        self.assertEqual(audit["counts"]["candidate_families_ranked"], 2)
        self.assertEqual(audit["baseline"]["positive_bronze_count"], 1)
        self.assertEqual(audit["baseline"]["oos_bronze_count"], 1)
        self.assertEqual(audit["baseline"]["silver_ready_count"], 0)
        self.assertEqual(audit["baseline"]["projected_provisional_count"], 0)
        self.assertTrue(audit["guardrails"]["ec_scope_only_never_predictive"])
        self.assertFalse(audit["guardrails"]["labels_created"])

    def test_writer_is_non_destructive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            frozen = root / "curated.json"
            expansion = root / "external.json"
            frozen.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "cur:1",
                            "label_type": "seed_fingerprint",
                            "fingerprint_id": "existing_family_lane",
                        }
                    ]
                ),
                encoding="utf-8",
            )
            expansion.write_text(json.dumps([]), encoding="utf-8")
            frozen_before = frozen.read_bytes()
            expansion_before = expansion.read_bytes()
            out = root / "factory.json"
            report = root / "factory.md"

            audit = write_high_yield_family_lane_factory(
                out_path=out,
                report_path=report,
                frozen_benchmark_path=frozen,
                expansion_registry_path=expansion,
                specs=(_NEW_SPEC, _EXISTING_SPEC),
                count_fetcher=_count_fetcher,
            )

            self.assertEqual(frozen.read_bytes(), frozen_before)
            self.assertEqual(expansion.read_bytes(), expansion_before)
            self.assertEqual(audit["counts"]["candidate_families_ranked"], 2)
            self.assertIn("High-Yield Family Lane Factory", report.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
