"""Offline validation of the breadth feasibility scout.

No network: the supply-count and EC-sample fetchers are injected with deterministic
payloads keyed on the candidate lane query, so the full recon (supply -> reaction
diversity -> redundancy/floor verdict -> 10k feasibility roll-up) is exercised and the
guardrails asserted.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.breadth_feasibility_scout import (
    CANDIDATE_FAMILIES,
    build_breadth_feasibility_scout,
    evaluate_candidate_family,
    write_breadth_feasibility_scout,
)

# Two synthetic candidate families: one clean+distinct, one that shares an EC lane with an
# existing fingerprint AND declares no separating cofactor (redundant).
_CLEAN = {
    "candidate_family": "synthetic_clean_family",
    "ec_class": "EC 9.9.9 (synthetic)",
    "chemistry": "synthetic distinct chemistry",
    "cofactor_ec_handle": "synthetic-cofactor + EC 9.9.9",
    "count_query": "(ec:9.9.9.*) AND (reviewed:true)",
    "ec_prefixes": ["9.9.9"],
    "chemistry_confusable": False,
    "cofactor_distinct_from_overlap": True,
    "notes": "clean",
}
_REDUNDANT = {
    "candidate_family": "synthetic_redundant_family",
    "ec_class": "EC 1.11.1 (peroxidase, already covered)",
    "chemistry": "heme peroxidase, already a fingerprint",
    "cofactor_ec_handle": "heme + EC 1.11.1",
    "count_query": "(ec:1.11.1.*) AND (reviewed:true)",
    "ec_prefixes": ["1.11.1"],  # overlaps heme_peroxidase_oxidase
    "chemistry_confusable": False,
    "cofactor_distinct_from_overlap": False,  # no separating cofactor -> redundant
    "notes": "redundant",
}
_CONFUSABLE_SUBFLOOR = {
    "candidate_family": "synthetic_confusable_subfloor",
    "ec_class": "EC 8.8.8 (synthetic)",
    "chemistry": "distinct but reaction-poor and low-supply",
    "cofactor_ec_handle": "synthetic-cofactor + EC 8.8.8",
    "count_query": "(ec:8.8.8.*) AND (reviewed:true)",
    "ec_prefixes": ["8.8.8"],
    "chemistry_confusable": True,
    "cofactor_distinct_from_overlap": True,
    "notes": "subfloor",
}

# Supply (header count) + distinct EC per lane query.
_SUPPLY = {
    _CLEAN["count_query"]: 1200,            # huge -> cap-bound at 250
    _REDUNDANT["count_query"]: 800,
    _CONFUSABLE_SUBFLOOR["count_query"]: 40,  # 40*0.5 = 20 < 100 floor
}
_EC_SAMPLE = {
    _CLEAN["count_query"]: [[f"9.9.9.{i}"] for i in range(120)],   # reaction-rich
    _REDUNDANT["count_query"]: [["1.11.1.7"] for _ in range(50)],
    _CONFUSABLE_SUBFLOOR["count_query"]: [["8.8.8.1"] for _ in range(40)],  # 1 distinct
}


def _count_fetcher(query):
    return {"total_results": _SUPPLY.get(query), "metadata": {"query": query}}


def _ec_sample_fetcher(query, size):
    rows = _EC_SAMPLE.get(query, [])[:size]
    return {"ec_per_row": rows, "metadata": {"query": query, "size": size}}


# A tiny registry pair: 3 positives in frozen, 2 in expansion, plus an OOS row to ignore.
_FROZEN = [
    {"entry_id": "a", "label_type": "seed_fingerprint", "fingerprint_id": "x"},
    {"entry_id": "b", "label_type": "seed_fingerprint", "fingerprint_id": "x"},
    {"entry_id": "c", "label_type": "seed_fingerprint", "fingerprint_id": "y"},
]
_EXPANSION = [
    {"entry_id": "d", "label_type": "seed_fingerprint", "fingerprint_id": "x"},
    {"entry_id": "e", "label_type": "seed_fingerprint", "fingerprint_id": "y"},
    {"entry_id": "oos", "label_type": "out_of_scope"},
]


def _build(**kwargs):
    return build_breadth_feasibility_scout(
        frozen_benchmark_payload=_FROZEN,
        expansion_payload=_EXPANSION,
        candidate_families=(_CLEAN, _REDUNDANT, _CONFUSABLE_SUBFLOOR),
        sample_size=200,
        count_fetcher=_count_fetcher,
        ec_sample_fetcher=_ec_sample_fetcher,
        created_utc="2026-06-11T00:00:00Z",
        **kwargs,
    )


class BreadthFeasibilityScoutTests(unittest.TestCase):
    def test_clean_redundant_and_subfloor_classified(self) -> None:
        audit = _build()
        by_family = {p["candidate_family"]: p for p in audit["family_probes"]}

        clean = by_family["synthetic_clean_family"]
        self.assertTrue(clean["clean_family"])
        self.assertTrue(clean["mechanistically_distinct"])
        self.assertFalse(clean["redundant_with_existing"])
        self.assertTrue(clean["floor_reachable"])
        # supply 1200 * 0.5 = 600, capped at 250 (not confusable)
        self.assertEqual(clean["estimated_admissible_diverse_bronze"], 250)

        redundant = by_family["synthetic_redundant_family"]
        self.assertFalse(redundant["clean_family"])
        self.assertTrue(redundant["redundant_with_existing"])
        self.assertIn("heme_peroxidase_oxidase", redundant["ec_overlap_with_existing_fingerprints"])
        # redundant families contribute zero admissible bronze
        self.assertEqual(redundant["estimated_admissible_diverse_bronze"], 0)

        subfloor = by_family["synthetic_confusable_subfloor"]
        self.assertTrue(subfloor["mechanistically_distinct"])
        self.assertFalse(subfloor["floor_reachable"])
        self.assertFalse(subfloor["clean_family"])
        self.assertEqual(subfloor["applied_cap"], 150)  # confusable cap

    def test_rollup_counts_and_verdict(self) -> None:
        audit = _build()
        c = audit["counts"]
        self.assertEqual(c["candidate_families_probed"], 3)
        self.assertEqual(c["clean_families"], 1)
        self.assertEqual(c["redundant_with_existing"], 1)
        self.assertEqual(c["mechanistically_distinct_but_floor_blocked"], 1)
        # baseline = 3 frozen + 2 expansion positives = 5 (OOS row ignored)
        self.assertEqual(c["current_combined_positive_bronze"], 5)
        self.assertEqual(c["estimated_new_clean_diverse_bronze"], 250)
        self.assertEqual(c["projected_positive_bronze_clean_only"], 255)
        self.assertEqual(c["gap_to_10k_positive_bronze"], 10_000 - 255)
        # nowhere near 10k -> not plausible
        self.assertFalse(audit["verdict"]["ten_k_diverse_positive_bronze_plausible"])
        self.assertTrue(
            audit["verdict"]["verdict_code"].startswith("ten_k_diverse_positive_bronze_NOT")
        )

    def test_redundancy_ratio_is_conservative_upper_bound(self) -> None:
        # Reaction-rich clean family: 250 labels / 120 distinct EC ~ 2.08 (<= reaction-poor)
        clean = evaluate_candidate_family(
            _CLEAN,
            count_fetcher=_count_fetcher,  # tolerant .get -> EC-ceiling query yields None
            ec_sample_fetcher=_ec_sample_fetcher,
            sample_size=200,
            target_floor=100,
            cap_ceiling=250,
        )
        self.assertAlmostEqual(
            clean["labels_per_distinct_reaction_upper_bound"], round(250 / 120, 3)
        )
        self.assertFalse(clean["reaction_poor_warning"])

    def test_guardrails_no_registry_or_labels(self) -> None:
        audit = _build()
        g = audit["guardrails"]
        self.assertFalse(g["registry_written"])
        self.assertFalse(g["labels_created"])
        self.assertTrue(g["frozen_current702_benchmark_preserved"])
        self.assertTrue(
            g["ec_cofactor_used_for_supply_and_scope_estimate_only_never_predictive"]
        )
        # The audit carries no label objects at all.
        blob = json.dumps(audit)
        self.assertNotIn('"tier": "bronze"', blob)
        self.assertNotIn("predictive_evidence", blob)

    def test_partial_ec_codes_excluded_from_reaction_diversity(self) -> None:
        # "3.2.1.-" partial codes must not count as distinct reactions.
        spec = {**_CLEAN, "count_query": "partial-test"}
        supply = {"partial-test": 100}
        sample = {"partial-test": [["3.2.1.-"], ["3.2.1.-"], ["3.2.1.23"]]}
        probe = evaluate_candidate_family(
            spec,
            count_fetcher=lambda q: {"total_results": supply.get(q)},
            ec_sample_fetcher=lambda q, s: {"ec_per_row": sample.get(q, [])[:s]},
            sample_size=200,
            target_floor=100,
            cap_ceiling=250,
        )
        self.assertEqual(
            probe["reaction_diversity_sample"]["distinct_full_ec_in_sample"], 1
        )

    def test_weak_cofactor_handle_capture_detected(self) -> None:
        # Cofactor handle reaches only 7 of an 8000-entry EC ceiling -> weak handle, and
        # the floor is not reachable on the handle-reachable supply.
        spec = {**_CLEAN, "count_query": "narrow", "ec_prefixes": ["1.1.1"]}
        counts = {"narrow": 7, "(reviewed:true) AND ((ec:1.1.1.*))": 8000}
        probe = evaluate_candidate_family(
            spec,
            count_fetcher=lambda q: {"total_results": counts.get(q)},
            ec_sample_fetcher=lambda q, s: {"ec_per_row": [["1.1.1.1"]]},
            sample_size=200,
            target_floor=100,
            cap_ceiling=250,
        )
        self.assertEqual(probe["ec_only_supply_ceiling"], 8000)
        self.assertAlmostEqual(probe["cofactor_handle_capture_ratio"], round(7 / 8000, 3))
        self.assertFalse(probe["floor_reachable"])

    def test_writer_is_non_destructive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frozen = Path(tmp) / "frozen.json"
            expansion = Path(tmp) / "expansion.json"
            frozen.write_text(json.dumps(_FROZEN), encoding="utf-8")
            expansion.write_text(json.dumps(_EXPANSION), encoding="utf-8")
            frozen_before = frozen.read_bytes()
            expansion_before = expansion.read_bytes()

            out = Path(tmp) / "scout.json"
            report = Path(tmp) / "scout.md"
            audit = write_breadth_feasibility_scout(
                out_path=out,
                report_path=report,
                candidate_families=(_CLEAN, _REDUNDANT, _CONFUSABLE_SUBFLOOR),
                frozen_benchmark_path=frozen,
                expansion_registry_path=expansion,
                count_fetcher=_count_fetcher,
                ec_sample_fetcher=_ec_sample_fetcher,
            )

            # Registries untouched; only artifact + report written.
            self.assertEqual(frozen.read_bytes(), frozen_before)
            self.assertEqual(expansion.read_bytes(), expansion_before)
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(audit["counts"]["clean_families"], 1)
            self.assertIn("Breadth Feasibility Scout", report.read_text(encoding="utf-8"))

    def test_real_candidate_families_are_well_formed(self) -> None:
        # Every shipped candidate spec carries the fields the engine + report read.
        for spec in CANDIDATE_FAMILIES:
            for key in (
                "candidate_family",
                "ec_class",
                "chemistry",
                "cofactor_ec_handle",
                "count_query",
                "ec_prefixes",
            ):
                self.assertIn(key, spec, f"{spec.get('candidate_family')} missing {key}")
            self.assertTrue(spec["ec_prefixes"])
            self.assertIn("reviewed:true", spec["count_query"])
        # Family ids are unique.
        ids = [s["candidate_family"] for s in CANDIDATE_FAMILIES]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
