from __future__ import annotations

import csv
import hashlib
import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class GeometryArtifactRegressionTests(unittest.TestCase):
    def test_label_summary_artifact_matches_curated_registry(self) -> None:
        summary = _load_json(ROOT / "artifacts" / "v3_label_summary.json")

        self.assertEqual(summary["label_count"], 702)
        self.assertEqual(summary["by_type"]["seed_fingerprint"], 230)
        self.assertEqual(summary["by_type"]["out_of_scope"], 472)
        self.assertEqual(
            summary["by_ontology_version_at_decision"],
            {"label_factory_v1_8fp": 702},
        )

    def test_125_entry_geometry_artifacts_remain_clean(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_125.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_125.json")
        margins = _load_json(ROOT / "artifacts" / "v3_geometry_score_margins_125.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_125.json"
        )

        self.assertEqual(evaluation["metadata"]["top1_accuracy_in_scope_evaluable"], 1.0)
        self.assertEqual(evaluation["metadata"]["top3_accuracy_in_scope_evaluable"], 1.0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 1.0)
        self.assertEqual(
            evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"],
            0,
        )
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertTrue(
            margins["metadata"][
                "strict_threshold_exists_to_retain_all_in_scope_and_abstain_all_out_of_scope"
            ]
        )
        self.assertGreater(margins["metadata"]["score_separation_gap"], 0.0)
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 0)

    def test_regression_slices_have_no_hard_negatives(self) -> None:
        for suffix in ["", "_30", "_40", "_50", "_60", "_75", "_100"]:
            with self.subTest(suffix=suffix or "_20"):
                hard_negatives = _load_json(
                    ROOT / "artifacts" / f"v3_hard_negative_controls{suffix}.json"
                )
                evaluation = _load_json(
                    ROOT / "artifacts" / f"v3_geometry_label_eval{suffix}.json"
                )
                self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
                self.assertEqual(
                    evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"],
                    0,
                )
                self.assertEqual(evaluation["metadata"]["top1_accuracy_in_scope_evaluable"], 1.0)

    def test_150_entry_geometry_artifacts_hold_out_of_scope_line(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_150.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_150.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_150.json"
        )
        cofactor_coverage = _load_json(ROOT / "artifacts" / "v3_cofactor_coverage_150.json")
        cofactor_policy = _load_json(ROOT / "artifacts" / "v3_cofactor_policy_150.json")
        seed_family = _load_json(ROOT / "artifacts" / "v3_seed_family_performance_150.json")
        margins = _load_json(ROOT / "artifacts" / "v3_geometry_score_margins_150.json")

        self.assertEqual(evaluation["metadata"]["in_scope_count"], 43)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 1)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(
            in_scope_failures["metadata"]["evidence_limited_abstention_count"], 1
        )
        self.assertEqual(in_scope_failures["metadata"]["top1_mismatch_count"], 1)
        self.assertEqual(cofactor_coverage["metadata"]["expected_absent_count"], 2)
        self.assertEqual(cofactor_coverage["metadata"]["expected_absent_retained_count"], 1)
        self.assertEqual(cofactor_coverage["metadata"]["expected_absent_abstained_count"], 1)
        self.assertEqual(
            cofactor_coverage["metadata"]["expected_absent_retained_entry_ids"],
            ["m_csa:41"],
        )
        self.assertEqual(
            cofactor_coverage["metadata"]["evidence_limited_retained_entry_ids"],
            ["m_csa:41", "m_csa:108"],
        )
        self.assertEqual(
            cofactor_coverage["metadata"]["evidence_limited_abstained_entry_ids"],
            ["m_csa:132"],
        )
        self.assertEqual(
            cofactor_policy["metadata"]["audit_evidence_limited_retained_positive_entry_ids"],
            ["m_csa:41", "m_csa:108"],
        )
        self.assertEqual(
            cofactor_policy["metadata"]["lossless_decision_changing_policy_count"],
            0,
        )
        self.assertEqual(
            cofactor_policy["metadata"]["minimum_evidence_limited_retained_margin"],
            0.0307,
        )
        self.assertEqual(
            cofactor_policy["metadata"]["recommendation"],
            "audit_only_or_separate_stratum",
        )
        self.assertEqual(seed_family["metadata"]["in_scope_family_count"], 7)
        self.assertEqual(seed_family["metadata"]["out_of_scope_retained_family_count"], 0)
        self.assertEqual(
            seed_family["metadata"]["weakest_retained_in_scope_family"],
            "flavin_monooxygenase",
        )
        self.assertTrue(
            margins["metadata"][
                "strict_threshold_exists_to_retain_all_correct_top1_in_scope_and_abstain_all_out_of_scope"
            ]
        )

    def test_175_entry_geometry_artifacts_expose_stress_slice(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_175.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_175.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_175.json"
        )
        cofactor_policy = _load_json(ROOT / "artifacts" / "v3_cofactor_policy_175.json")
        seed_family = _load_json(ROOT / "artifacts" / "v3_seed_family_performance_175.json")

        self.assertEqual(evaluation["metadata"]["in_scope_count"], 58)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9828)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(
            hard_negatives["metadata"]["near_miss_top1_fingerprint_counts"],
            {},
        )
        self.assertEqual(
            hard_negatives["metadata"]["near_miss_cofactor_evidence_counts"],
            {},
        )
        self.assertIsNone(hard_negatives["metadata"]["closest_near_miss_entry_id"])
        self.assertIsNone(hard_negatives["metadata"]["minimum_near_miss_score_gap_to_floor"])
        self.assertEqual(hard_negatives["near_miss_groups"], [])
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 1)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(
            cofactor_policy["metadata"]["recommendation"],
            "audit_only_or_separate_stratum",
        )
        self.assertEqual(seed_family["metadata"]["largest_in_scope_family"], "metal_dependent_hydrolase")
        self.assertEqual(seed_family["metadata"]["largest_in_scope_family_count"], 27)

    def test_200_entry_geometry_artifacts_clear_new_hard_negatives(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_200.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_200.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_200.json"
        )
        label_candidates = _load_json(
            ROOT / "artifacts" / "v3_label_expansion_candidates_200.json"
        )
        mapping_issues = _load_json(
            ROOT / "artifacts" / "v3_structure_mapping_issues_200.json"
        )

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 475)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 64)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 136)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9844)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(
            hard_negatives["metadata"]["closest_below_floor_entry_id"],
            "m_csa:65",
        )
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 1)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["evidence_limited_abstention_count"], 1)
        self.assertEqual(label_candidates["metadata"]["ready_for_label_review_count"], 0)
        self.assertEqual(mapping_issues["metadata"]["issue_count"], 3)

    def test_225_entry_geometry_artifacts_clear_stress_slice(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_225.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_225.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_225.json"
        )
        label_candidates = _load_json(
            ROOT / "artifacts" / "v3_label_expansion_candidates_225.json"
        )
        cofactor_coverage = _load_json(ROOT / "artifacts" / "v3_cofactor_coverage_225.json")
        retrieval = _load_json(ROOT / "artifacts" / "v3_geometry_retrieval_225.json")

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 475)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 70)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 154)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9857)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(
            hard_negatives["metadata"]["closest_below_floor_entry_id"],
            "m_csa:65",
        )
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 1)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["evidence_limited_abstention_count"], 1)
        self.assertEqual(
            cofactor_coverage["metadata"]["evidence_limited_abstained_entry_ids"],
            ["m_csa:132"],
        )
        alanine_racemase = next(
            row for row in retrieval["results"] if row["entry_id"] == "m_csa:213"
        )
        self.assertIn("plp", alanine_racemase["ligand_context"]["cofactor_families"])
        self.assertEqual(
            alanine_racemase["top_fingerprints"][0]["fingerprint_id"],
            "plp_dependent_enzyme",
        )
        self.assertGreaterEqual(alanine_racemase["top_fingerprints"][0]["score"], 0.4145)
        self.assertEqual(label_candidates["metadata"]["ready_for_label_review_count"], 0)

    def test_250_entry_geometry_artifacts_clear_stress_slice(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_250.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_250.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_250.json"
        )
        cofactor_coverage = _load_json(ROOT / "artifacts" / "v3_cofactor_coverage_250.json")
        retrieval = _load_json(ROOT / "artifacts" / "v3_geometry_retrieval_250.json")

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 475)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 77)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 172)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.987)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(
            hard_negatives["metadata"]["closest_below_floor_entry_id"],
            "m_csa:65",
        )
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 1)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["evidence_limited_abstention_count"], 1)
        self.assertEqual(
            cofactor_coverage["metadata"]["evidence_limited_retained_entry_ids"],
            ["m_csa:41", "m_csa:108", "m_csa:160"],
        )
        oxalate_decarboxylase = next(
            row for row in retrieval["results"] if row["entry_id"] == "m_csa:231"
        )
        self.assertIn(
            "structure_only_manganese_decarboxylase_context",
            oxalate_decarboxylase["top_fingerprints"][0]["counterevidence_reasons"],
        )
        self.assertLess(oxalate_decarboxylase["top_fingerprints"][0]["score"], 0.4145)

    def test_275_entry_geometry_artifacts_clear_text_counterevidence_slice(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_275.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_275.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_275.json"
        )
        cofactor_coverage = _load_json(ROOT / "artifacts" / "v3_cofactor_coverage_275.json")
        retrieval = _load_json(ROOT / "artifacts" / "v3_geometry_retrieval_275.json")

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 475)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 80)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 194)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9875)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 1)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["evidence_limited_abstention_count"], 1)
        self.assertEqual(
            cofactor_coverage["metadata"]["evidence_limited_retained_entry_ids"],
            ["m_csa:41", "m_csa:108", "m_csa:160"],
        )

        prenyltransferase = next(
            row for row in retrieval["results"] if row["entry_id"] == "m_csa:253"
        )
        self.assertEqual(prenyltransferase["entry_name"], "geranyltranstransferase")
        self.assertEqual(prenyltransferase["mechanism_text_count"], 1)
        self.assertIn("diphosphate", prenyltransferase["mechanism_text_snippets"][0])
        self.assertIn(
            "nonhydrolytic_prenyl_carbocation_text_context",
            prenyltransferase["top_fingerprints"][0]["counterevidence_reasons"],
        )
        self.assertLess(prenyltransferase["top_fingerprints"][0]["score"], 0.4145)
        methyltransferase = next(
            row for row in retrieval["results"] if row["entry_id"] == "m_csa:268"
        )
        self.assertIn(
            "methylcobalamin_transfer_not_radical_rearrangement",
            methyltransferase["top_fingerprints"][1]["counterevidence_reasons"],
        )
        self.assertLess(methyltransferase["top_fingerprints"][1]["score"], 0.4145)
        flavin_reductase = next(
            row for row in retrieval["results"] if row["entry_id"] == "m_csa:275"
        )
        self.assertEqual(
            flavin_reductase["top_fingerprints"][0]["fingerprint_id"],
            "flavin_dehydrogenase_reductase",
        )
        self.assertGreaterEqual(flavin_reductase["top_fingerprints"][0]["score"], 0.4145)

    def test_375_entry_geometry_artifacts_clear_expanded_stress_slice(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_375.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_375.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_375.json"
        )
        cofactor_coverage = _load_json(ROOT / "artifacts" / "v3_cofactor_coverage_375.json")
        retrieval = _load_json(ROOT / "artifacts" / "v3_geometry_retrieval_375.json")

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 475)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 97)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 277)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 3)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["evidence_limited_abstention_count"], 3)
        self.assertEqual(
            cofactor_coverage["metadata"]["evidence_limited_abstained_entry_ids"],
            ["m_csa:132", "m_csa:353", "m_csa:372"],
        )
        aldoxime_dehydratase = next(
            row for row in retrieval["results"] if row["entry_id"] == "m_csa:361"
        )
        heme_hit = next(
            item
            for item in aldoxime_dehydratase["top_fingerprints"]
            if item["fingerprint_id"] == "heme_peroxidase_oxidase"
        )
        self.assertIn(
            "heme_dehydratase_not_peroxidase_oxidase",
            heme_hit["counterevidence_reasons"],
        )
        self.assertLess(heme_hit["score"], 0.4145)

    def test_400_entry_geometry_artifacts_clear_curated_queue(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_400.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_400.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_400.json"
        )
        label_candidates = _load_json(
            ROOT / "artifacts" / "v3_label_expansion_candidates_400.json"
        )
        retrieval = _load_json(ROOT / "artifacts" / "v3_geometry_retrieval_400.json")

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 475)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 105)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 294)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9808)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 3)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(label_candidates["metadata"]["candidate_count"], 0)
        self.assertEqual(label_candidates["metadata"]["labeled_entry_count"], 475)

        chymotrypsin = next(row for row in retrieval["results"] if row["entry_id"] == "m_csa:387")
        self.assertEqual(
            chymotrypsin["top_fingerprints"][0]["fingerprint_id"],
            "ser_his_acid_hydrolase",
        )
        self.assertEqual(chymotrypsin["top_fingerprints"][0]["mechanistic_coherence_score"], 1.0)
        self.assertGreaterEqual(chymotrypsin["top_fingerprints"][0]["score"], 0.8)

        trna_ligase = next(row for row in retrieval["results"] if row["entry_id"] == "m_csa:384")
        self.assertIn(
            "aminoacyl_ligase_not_metal_hydrolysis",
            trna_ligase["top_fingerprints"][0]["counterevidence_reasons"],
        )
        self.assertLess(trna_ligase["top_fingerprints"][0]["score"], 0.4145)

    def test_425_entry_geometry_artifacts_clear_plp_and_glycosidase_slice(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_425.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_425.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_425.json"
        )
        label_candidates = _load_json(
            ROOT / "artifacts" / "v3_label_expansion_candidates_425.json"
        )
        cofactor_coverage = _load_json(ROOT / "artifacts" / "v3_cofactor_coverage_425.json")
        retrieval = _load_json(ROOT / "artifacts" / "v3_geometry_retrieval_425.json")

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 475)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 116)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 308)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9826)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 3)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["evidence_limited_abstention_count"], 3)
        self.assertEqual(label_candidates["metadata"]["candidate_count"], 0)
        self.assertEqual(label_candidates["metadata"]["labeled_entry_count"], 475)
        self.assertEqual(
            cofactor_coverage["metadata"]["evidence_limited_abstained_entry_ids"],
            ["m_csa:132", "m_csa:353", "m_csa:372"],
        )

        tryptophanase = next(row for row in retrieval["results"] if row["entry_id"] == "m_csa:410")
        self.assertEqual(tryptophanase["entry_name"], "tryptophanase")
        self.assertEqual(
            tryptophanase["top_fingerprints"][0]["fingerprint_id"],
            "plp_dependent_enzyme",
        )
        self.assertEqual(
            tryptophanase["top_fingerprints"][0]["cofactor_evidence_level"],
            "ligand_supported",
        )
        self.assertGreaterEqual(tryptophanase["top_fingerprints"][0]["score"], 0.4644)

        isoamylase = next(row for row in retrieval["results"] if row["entry_id"] == "m_csa:421")
        self.assertIn(
            "glycosidase_not_metal_hydrolase_seed",
            isoamylase["top_fingerprints"][0]["counterevidence_reasons"],
        )
        self.assertLess(isoamylase["top_fingerprints"][0]["score"], 0.4145)

    def test_450_entry_geometry_artifacts_clear_beta_lyase_slice(self) -> None:
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_450.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_450.json")
        in_scope_failures = _load_json(
            ROOT / "artifacts" / "v3_in_scope_failure_analysis_450.json"
        )
        label_candidates = _load_json(
            ROOT / "artifacts" / "v3_label_expansion_candidates_450.json"
        )
        cofactor_coverage = _load_json(ROOT / "artifacts" / "v3_cofactor_coverage_450.json")
        retrieval = _load_json(ROOT / "artifacts" / "v3_geometry_retrieval_450.json")

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 475)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 123)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 326)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9754)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 4)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["evidence_limited_abstention_count"], 4)
        self.assertEqual(label_candidates["metadata"]["candidate_count"], 0)
        self.assertEqual(label_candidates["metadata"]["labeled_entry_count"], 475)
        self.assertEqual(
            cofactor_coverage["metadata"]["evidence_limited_abstained_entry_ids"],
            ["m_csa:132", "m_csa:353", "m_csa:372", "m_csa:430"],
        )

        cystathionine_lyase = next(
            row for row in retrieval["results"] if row["entry_id"] == "m_csa:449"
        )
        self.assertEqual(cystathionine_lyase["entry_name"], "cystathionine beta-lyase")
        self.assertEqual(
            cystathionine_lyase["top_fingerprints"][0]["fingerprint_id"],
            "plp_dependent_enzyme",
        )
        self.assertEqual(
            cystathionine_lyase["top_fingerprints"][0]["cofactor_evidence_level"],
            "ligand_supported",
        )
        self.assertGreaterEqual(cystathionine_lyase["top_fingerprints"][0]["score"], 0.4551)

        acetylxylan_esterase = next(
            row for row in retrieval["results"] if row["entry_id"] == "m_csa:431"
        )
        self.assertEqual(
            acetylxylan_esterase["top_fingerprints"][0]["fingerprint_id"],
            "ser_his_acid_hydrolase",
        )
        self.assertGreaterEqual(acetylxylan_esterase["top_fingerprints"][0]["score"], 0.7892)

    def test_500_entry_queue_carries_plp_and_prenyl_context(self) -> None:
        candidates = _load_json(ROOT / "artifacts" / "v3_label_expansion_candidates_500.json")
        retrieval = _load_json(ROOT / "artifacts" / "v3_geometry_retrieval_500.json")

        self.assertEqual(candidates["metadata"]["labeled_entry_count"], 499)
        self.assertEqual(candidates["metadata"]["candidate_count"], 1)
        self.assertEqual(candidates["metadata"]["candidate_group_count"], 1)
        self.assertEqual(candidates["metadata"]["ready_for_label_review_count"], 1)

        dialkylglycine_decarboxylase = next(
            row for row in retrieval["results"] if row["entry_id"] == "m_csa:482"
        )
        self.assertIn(
            "plp",
            dialkylglycine_decarboxylase["ligand_context"]["cofactor_families"],
        )
        self.assertEqual(
            dialkylglycine_decarboxylase["top_fingerprints"][0]["fingerprint_id"],
            "plp_dependent_enzyme",
        )
        self.assertGreaterEqual(
            dialkylglycine_decarboxylase["top_fingerprints"][0]["score"],
            0.5,
        )

        farnesyltransferase = next(
            row for row in retrieval["results"] if row["entry_id"] == "m_csa:484"
        )
        self.assertIn(
            "nonhydrolytic_metal_transfer_ligand_context",
            farnesyltransferase["top_fingerprints"][0]["counterevidence_reasons"],
        )
        self.assertIn(
            "nonhydrolytic_prenyl_carbocation_text_context",
            farnesyltransferase["top_fingerprints"][0]["counterevidence_reasons"],
        )
        self.assertLess(farnesyltransferase["top_fingerprints"][0]["score"], 0.4115)

    def test_label_factory_artifacts_gate_500_queue(self) -> None:
        label_summary = _load_json(ROOT / "artifacts" / "v3_label_summary.json")
        audit = _load_json(ROOT / "artifacts" / "v3_label_factory_audit_500.json")
        applied = _load_json(
            ROOT / "artifacts" / "v3_label_factory_applied_labels_500.json"
        )
        adversarial = _load_json(
            ROOT / "artifacts" / "v3_adversarial_negative_controls_500.json"
        )
        queue = _load_json(ROOT / "artifacts" / "v3_active_learning_review_queue_500.json")
        review_export = _load_json(ROOT / "artifacts" / "v3_expert_review_export_500.json")
        guardrails = _load_json(
            ROOT / "artifacts" / "v3_family_propagation_guardrails_500.json"
        )
        gate = _load_json(ROOT / "artifacts" / "v3_label_factory_gate_check_500.json")

        self.assertEqual(label_summary["by_tier"], {"bronze": 685, "silver": 17})
        self.assertEqual(
            label_summary["by_review_status"],
            {"automation_curated": 683, "expert_reviewed": 19},
        )
        self.assertEqual(audit["metadata"]["promote_to_silver_count"], 63)
        self.assertEqual(audit["metadata"]["abstention_or_review_count"], 101)
        self.assertEqual(audit["metadata"]["hard_negative_evidence_entry_count"], 100)
        self.assertEqual(applied["metadata"]["output_summary"]["by_tier"]["silver"], 63)
        self.assertEqual(
            applied["metadata"]["output_summary"]["by_review_status"]["needs_expert_review"],
            101,
        )
        self.assertEqual(adversarial["metadata"]["control_count"], 100)
        self.assertIn("ontology_family_boundary", adversarial["metadata"]["axis_counts"])
        self.assertEqual(queue["metadata"]["unlabeled_count"], 1)
        self.assertEqual(queue["metadata"]["queued_count"], 102)
        self.assertEqual(review_export["metadata"]["exported_count"], 26)
        self.assertEqual(
            sum(1 for item in review_export["review_items"] if item["current_label"] is None),
            1,
        )
        self.assertEqual(
            guardrails["metadata"]["decision_counts"]["block_propagation_pending_review"],
            1,
        )
        self.assertTrue(gate["metadata"]["automation_ready_for_next_label_batch"])
        self.assertEqual(gate["blockers"], [])

    def test_525_through_725_batch_acceptance_are_gated(self) -> None:
        acceptance = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_525.json")
        acceptance_550 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_550.json")
        acceptance_575 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_575.json")
        acceptance_600 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_600.json")
        acceptance_625 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_625.json")
        acceptance_650 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_650.json")
        acceptance_675_preview = _load_json(
            ROOT / "artifacts" / "v3_label_batch_acceptance_check_675_preview.json"
        )
        acceptance_675 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_675.json")
        acceptance_700 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_700.json")
        acceptance_725 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_725.json")
        acceptance_750 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_750.json")
        acceptance_975 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_975.json")
        acceptance_1000 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_1000.json")
        batch_summary = _load_json(
            ROOT / "artifacts" / "v3_label_factory_batch_summary.json"
        )
        preview_summary_675 = _load_json(
            ROOT / "artifacts" / "v3_label_factory_preview_summary_675.json"
        )
        preview_debt_675 = _load_json(
            ROOT / "artifacts" / "v3_review_debt_summary_675_preview.json"
        )
        preview_readiness_675 = _load_json(
            ROOT / "artifacts" / "v3_label_preview_promotion_readiness_675.json"
        )
        scaling_quality_675 = _load_json(
            ROOT / "artifacts" / "v3_label_scaling_quality_audit_675_preview.json"
        )
        scaling_quality_700 = _load_json(
            ROOT / "artifacts" / "v3_label_scaling_quality_audit_700_preview.json"
        )
        scaling_quality_725 = _load_json(
            ROOT / "artifacts" / "v3_label_scaling_quality_audit_725_preview.json"
        )
        remediation_700 = _load_json(
            ROOT / "artifacts" / "v3_review_debt_remediation_700.json"
        )
        remediation_700_all = _load_json(
            ROOT / "artifacts" / "v3_review_debt_remediation_700_all.json"
        )
        alternate_scan_700 = _load_json(
            ROOT / "artifacts" / "v3_review_debt_alternate_structure_scan_700.json"
        )
        alternate_scan_700_all = _load_json(
            ROOT
            / "artifacts"
            / "v3_review_debt_alternate_structure_scan_700_all_bounded.json"
        )
        remap_leads_700_all = _load_json(
            ROOT
            / "artifacts"
            / "v3_review_debt_remap_leads_700_all_bounded.json"
        )
        remap_local_audit_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_review_debt_remap_local_lead_audit_700.json"
        )
        structure_selection_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_review_debt_structure_selection_candidates_700.json"
        )
        reaction_mismatch_700 = _load_json(
            ROOT / "artifacts" / "v3_reaction_substrate_mismatch_audit_700.json"
        )
        reaction_mismatch_export_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_reaction_substrate_mismatch_review_export_700.json"
        )
        reaction_mismatch_decision_batch_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_reaction_substrate_mismatch_decision_batch_700.json"
        )
        expert_label_decision_export_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_expert_label_decision_review_export_700.json"
        )
        expert_label_decision_batch_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_expert_label_decision_decision_batch_700.json"
        )
        expert_label_decision_repair_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_expert_label_decision_repair_candidates_700.json"
        )
        expert_label_decision_repair_all_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_expert_label_decision_repair_candidates_700_all.json"
        )
        expert_label_decision_repair_guardrail_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_expert_label_decision_repair_guardrail_audit_700.json"
        )
        expert_label_decision_local_gap_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_expert_label_decision_local_evidence_gap_audit_700.json"
        )
        expert_label_decision_local_export_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_expert_label_decision_local_evidence_review_export_700.json"
        )
        expert_label_decision_local_batch_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_expert_label_decision_local_evidence_decision_batch_700.json"
        )
        expert_label_decision_local_plan_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_expert_label_decision_local_evidence_repair_plan_700.json"
        )
        expert_label_decision_local_resolution_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_expert_label_decision_local_evidence_repair_resolution_700.json"
        )
        alternate_residue_requests_700 = _load_json(
            ROOT
            / "artifacts"
            / "v3_explicit_alternate_residue_position_requests_700.json"
        )
        review_only_import_safety_700 = _load_json(
            ROOT / "artifacts" / "v3_review_only_import_safety_audit_700.json"
        )
        ontology_gap_audit_700 = _load_json(
            ROOT / "artifacts" / "v3_mechanism_ontology_gap_audit_700.json"
        )
        learned_manifest_700 = _load_json(
            ROOT / "artifacts" / "v3_learned_retrieval_manifest_700.json"
        )
        sequence_failure_sets_700 = _load_json(
            ROOT / "artifacts" / "v3_sequence_similarity_failure_sets_700.json"
        )
        sequence_clusters_675 = _load_json(
            ROOT / "artifacts" / "v3_sequence_cluster_proxy_675.json"
        )
        sequence_clusters_700 = _load_json(
            ROOT / "artifacts" / "v3_sequence_cluster_proxy_700.json"
        )
        sequence_clusters_725 = _load_json(
            ROOT / "artifacts" / "v3_sequence_cluster_proxy_725.json"
        )
        evaluation = _load_json(ROOT / "artifacts" / "v3_geometry_label_eval_650.json")
        hard_negatives = _load_json(ROOT / "artifacts" / "v3_hard_negative_controls_650.json")
        candidates_550 = _load_json(ROOT / "artifacts" / "v3_label_expansion_candidates_550.json")
        candidates_575 = _load_json(ROOT / "artifacts" / "v3_label_expansion_candidates_575.json")
        candidates_600 = _load_json(ROOT / "artifacts" / "v3_label_expansion_candidates_600.json")
        candidates_625 = _load_json(ROOT / "artifacts" / "v3_label_expansion_candidates_625.json")
        candidates_650 = _load_json(ROOT / "artifacts" / "v3_label_expansion_candidates_650.json")
        gate_550 = _load_json(ROOT / "artifacts" / "v3_label_factory_gate_check_550.json")
        gate_575 = _load_json(ROOT / "artifacts" / "v3_label_factory_gate_check_575.json")
        gate_600 = _load_json(ROOT / "artifacts" / "v3_label_factory_gate_check_600.json")
        gate_625 = _load_json(ROOT / "artifacts" / "v3_label_factory_gate_check_625.json")
        gate_650 = _load_json(ROOT / "artifacts" / "v3_label_factory_gate_check_650.json")
        gate_675 = _load_json(ROOT / "artifacts" / "v3_label_factory_gate_check_675.json")
        gate_700 = _load_json(ROOT / "artifacts" / "v3_label_factory_gate_check_700.json")
        gate_725 = _load_json(ROOT / "artifacts" / "v3_label_factory_gate_check_725.json")
        gate_750 = _load_json(ROOT / "artifacts" / "v3_label_factory_gate_check_750.json")
        review_debt_deferral_725 = _load_json(
            ROOT / "artifacts" / "v3_accepted_review_debt_deferral_audit_725.json"
        )
        review_debt_deferral_750 = _load_json(
            ROOT / "artifacts" / "v3_accepted_review_debt_deferral_audit_750.json"
        )
        acceptance_750_preview = _load_json(
            ROOT / "artifacts" / "v3_label_batch_acceptance_check_750_preview.json"
        )
        gate_750_preview = _load_json(
            ROOT / "artifacts" / "v3_label_factory_gate_check_750_preview.json"
        )
        scaling_quality_750 = _load_json(
            ROOT / "artifacts" / "v3_label_scaling_quality_audit_750_preview.json"
        )
        preview_summary_750 = _load_json(
            ROOT / "artifacts" / "v3_label_factory_preview_summary_750.json"
        )
        family_guardrails_700 = _load_json(
            ROOT / "artifacts" / "v3_family_propagation_guardrails_700.json"
        )
        active_queue_700 = _load_json(
            ROOT / "artifacts" / "v3_active_learning_review_queue_700.json"
        )
        expert_export_700 = _load_json(
            ROOT / "artifacts" / "v3_expert_review_export_700_post_batch.json"
        )

        self.assertTrue(acceptance["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance["metadata"]["accepted_new_label_count"], 24)
        self.assertEqual(acceptance["metadata"]["countable_label_count"], 523)
        self.assertTrue(acceptance_550["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance_550["metadata"]["accepted_new_label_count"], 23)
        self.assertEqual(acceptance_550["metadata"]["countable_label_count"], 546)
        self.assertTrue(acceptance_575["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance_575["metadata"]["accepted_new_label_count"], 17)
        self.assertEqual(acceptance_575["metadata"]["countable_label_count"], 563)
        self.assertTrue(acceptance_600["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance_600["metadata"]["accepted_new_label_count"], 16)
        self.assertEqual(acceptance_600["metadata"]["countable_label_count"], 579)
        self.assertTrue(acceptance_625["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance_625["metadata"]["accepted_new_label_count"], 20)
        self.assertEqual(acceptance_625["metadata"]["countable_label_count"], 599)
        self.assertTrue(acceptance_650["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance_650["metadata"]["accepted_new_label_count"], 19)
        self.assertEqual(acceptance_650["metadata"]["countable_label_count"], 618)
        self.assertTrue(acceptance_675_preview["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance_675_preview["metadata"]["accepted_new_label_count"], 1)
        self.assertEqual(acceptance_675_preview["metadata"]["accepted_new_label_entry_ids"], ["m_csa:666"])
        self.assertEqual(acceptance_675_preview["metadata"]["countable_label_count"], 619)
        self.assertEqual(acceptance_675_preview["metadata"]["pending_review_count"], 61)
        self.assertEqual(acceptance_675_preview["metadata"]["accepted_review_gap_count"], 0)
        self.assertEqual(acceptance_675_preview["metadata"]["accepted_review_gap_entry_ids"], [])
        self.assertTrue(acceptance_675["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance_675["metadata"]["accepted_new_label_count"], 1)
        self.assertEqual(acceptance_675["metadata"]["accepted_new_label_entry_ids"], ["m_csa:666"])
        self.assertEqual(acceptance_675["metadata"]["countable_label_count"], 619)
        self.assertEqual(acceptance_675["metadata"]["pending_review_count"], 61)
        self.assertEqual(acceptance_675["metadata"]["accepted_review_gap_count"], 0)
        self.assertEqual(acceptance_675["metadata"]["accepted_review_gap_entry_ids"], [])
        self.assertTrue(acceptance_700["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance_700["metadata"]["accepted_new_label_count"], 5)
        self.assertEqual(
            acceptance_700["metadata"]["accepted_new_label_entry_ids"],
            ["m_csa:686", "m_csa:688", "m_csa:694", "m_csa:697", "m_csa:699"],
        )
        self.assertEqual(acceptance_700["metadata"]["countable_label_count"], 624)
        self.assertEqual(acceptance_700["metadata"]["pending_review_count"], 81)
        self.assertEqual(acceptance_700["metadata"]["accepted_review_gap_count"], 0)
        self.assertEqual(acceptance_700["metadata"]["accepted_review_gap_entry_ids"], [])
        self.assertEqual(
            acceptance_700["metadata"]["accepted_reaction_substrate_mismatch_count"],
            0,
        )
        self.assertEqual(
            acceptance_700["metadata"][
                "accepted_reaction_substrate_mismatch_entry_ids"
            ],
            [],
        )
        self.assertTrue(acceptance_725["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance_725["metadata"]["accepted_new_label_count"], 6)
        self.assertEqual(
            acceptance_725["metadata"]["accepted_new_label_entry_ids"],
            ["m_csa:705", "m_csa:709", "m_csa:714", "m_csa:716", "m_csa:723", "m_csa:727"],
        )
        self.assertEqual(acceptance_725["metadata"]["countable_label_count"], 630)
        self.assertEqual(acceptance_725["metadata"]["pending_review_count"], 100)
        self.assertEqual(acceptance_725["metadata"]["accepted_review_gap_count"], 0)
        self.assertEqual(acceptance_725["metadata"]["accepted_review_gap_entry_ids"], [])
        self.assertEqual(acceptance_725["metadata"]["accepted_reaction_substrate_mismatch_count"], 0)
        self.assertTrue(
            batch_summary["metadata"][
                "latest_reaction_substrate_mismatch_review_export_present"
            ]
        )
        self.assertEqual(
            batch_summary["metadata"][
                "latest_reaction_substrate_mismatch_review_export_missing_count"
            ],
            0,
        )
        self.assertTrue(
            batch_summary["metadata"][
                "latest_expert_label_decision_review_export_present"
            ]
        )
        self.assertEqual(
            batch_summary["metadata"][
                "latest_active_queue_expert_label_decision_count"
            ],
            321,
        )
        self.assertEqual(
            batch_summary["metadata"][
                "latest_expert_label_decision_review_export_missing_count"
            ],
            0,
        )
        self.assertEqual(
            batch_summary["metadata"][
                "latest_expert_label_decision_review_export_countable_label_candidate_count"
            ],
            0,
        )
        self.assertTrue(
            batch_summary["metadata"][
                "latest_expert_label_decision_repair_candidates_present"
            ]
        )
        self.assertEqual(
            batch_summary["metadata"][
                "latest_expert_label_decision_repair_candidates_missing_count"
            ],
            0,
        )
        self.assertEqual(
            batch_summary["metadata"][
                "latest_expert_label_decision_repair_candidates_countable_label_candidate_count"
            ],
            0,
        )
        self.assertTrue(
            batch_summary["metadata"][
                "latest_expert_label_decision_repair_guardrail_audit_present"
            ]
        )
        self.assertEqual(
            batch_summary["metadata"][
                "latest_expert_label_decision_repair_guardrail_priority_repair_row_count"
            ],
            92,
        )
        self.assertEqual(
            batch_summary["metadata"][
                "latest_expert_label_decision_repair_guardrail_countable_label_candidate_count"
            ],
            0,
        )
        latest_batch_summary = batch_summary["rows"][-1]
        batch_700_summary = next(row for row in batch_summary["rows"] if row["batch"] == "700")
        self.assertTrue(acceptance_975["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance_975["metadata"]["accepted_new_label_count"], 2)
        self.assertEqual(
            acceptance_975["metadata"]["accepted_new_label_entry_ids"],
            ["m_csa:956", "m_csa:973"],
        )
        self.assertEqual(acceptance_975["metadata"]["countable_label_count"], 675)
        self.assertEqual(acceptance_975["metadata"]["pending_review_count"], 305)
        self.assertEqual(acceptance_975["metadata"]["accepted_review_gap_count"], 0)
        self.assertEqual(acceptance_975["metadata"]["accepted_review_gap_entry_ids"], [])
        self.assertTrue(acceptance_1000["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance_1000["metadata"]["accepted_new_label_count"], 4)
        self.assertEqual(
            acceptance_1000["metadata"]["accepted_new_label_entry_ids"],
            ["m_csa:978", "m_csa:988", "m_csa:990", "m_csa:994"],
        )
        self.assertEqual(acceptance_1000["metadata"]["countable_label_count"], 679)
        self.assertEqual(acceptance_1000["metadata"]["pending_review_count"], 326)
        self.assertEqual(acceptance_1000["metadata"]["accepted_review_gap_count"], 0)
        self.assertEqual(acceptance_1000["metadata"]["accepted_review_gap_entry_ids"], [])
        self.assertEqual(latest_batch_summary["batch"], "1000")
        self.assertEqual(latest_batch_summary["countable_label_count"], 679)
        self.assertEqual(latest_batch_summary["accepted_new_label_count"], 4)
        self.assertEqual(latest_batch_summary["active_queue_expert_label_decision_count"], 321)
        self.assertEqual(latest_batch_summary["expert_label_decision_repair_guardrail_priority_repair_row_count"], 92)
        self.assertTrue(latest_batch_summary["expert_label_decision_local_evidence_gap_audit_ready"])
        self.assertEqual(
            latest_batch_summary["expert_label_decision_local_evidence_review_export_exported_count"],
            92,
        )
        self.assertFalse(
            latest_batch_summary[
                "expert_label_decision_local_evidence_repair_resolution_present"
            ]
        )
        self.assertTrue(
            latest_batch_summary["explicit_alternate_residue_position_requests_present"]
        )
        self.assertEqual(
            latest_batch_summary["explicit_alternate_residue_position_requests_count"],
            38,
        )
        self.assertTrue(latest_batch_summary["review_only_import_safety_audit_present"])
        self.assertEqual(
            latest_batch_summary[
                "review_only_import_safety_audit_total_new_countable_label_count"
            ],
            0,
        )
        self.assertTrue(
            latest_batch_summary[
                "accepted_review_debt_deferral_audit_present"
            ]
        )
        self.assertTrue(
            latest_batch_summary["accepted_review_debt_deferral_audit_ready"]
        )
        self.assertEqual(
            latest_batch_summary[
                "accepted_review_debt_deferral_audit_deferred_entry_count"
            ],
            326,
        )
        self.assertEqual(
            latest_batch_summary[
                "accepted_review_debt_deferral_audit_countable_label_candidate_count"
            ],
            0,
        )
        self.assertTrue(
            gate_725["metadata"]["accepted_review_debt_deferral_audit_ready"]
        )
        self.assertEqual(gate_725["metadata"]["gate_count"], 21)
        self.assertEqual(gate_725["metadata"]["passed_gate_count"], 21)
        self.assertEqual(
            gate_725["metadata"][
                "accepted_review_debt_deferral_audit_strict_remap_guardrail_entry_ids"
            ],
            ["m_csa:712"],
        )
        self.assertTrue(review_debt_deferral_725["metadata"]["deferral_ready"])
        self.assertEqual(
            review_debt_deferral_725["metadata"]["deferred_entry_count"], 100
        )
        self.assertEqual(
            review_debt_deferral_725["metadata"]["metadata_only_review_debt_entry_count"],
            45,
        )
        self.assertEqual(
            review_debt_deferral_725["metadata"][
                "structure_wide_hit_without_local_support_entry_ids"
            ],
            ["m_csa:718", "m_csa:724"],
        )
        self.assertTrue(acceptance_750_preview["metadata"]["accepted_for_counting"])
        self.assertEqual(
            acceptance_750_preview["metadata"]["accepted_new_label_count"], 7
        )
        self.assertEqual(
            acceptance_750_preview["metadata"]["accepted_new_label_entry_ids"],
            [
                "m_csa:728",
                "m_csa:733",
                "m_csa:735",
                "m_csa:739",
                "m_csa:740",
                "m_csa:742",
                "m_csa:750",
            ],
        )
        self.assertEqual(acceptance_750_preview["metadata"]["countable_label_count"], 637)
        self.assertEqual(acceptance_750_preview["metadata"]["pending_review_count"], 118)
        self.assertEqual(acceptance_750_preview["metadata"]["accepted_review_gap_count"], 0)
        self.assertEqual(gate_750_preview["metadata"]["gate_count"], 19)
        self.assertEqual(gate_750_preview["metadata"]["passed_gate_count"], 19)
        self.assertTrue(
            gate_750_preview["metadata"]["automation_ready_for_next_label_batch"]
        )
        self.assertEqual(
            gate_750_preview["metadata"]["active_queue_expert_label_decision_count"],
            120,
        )
        self.assertEqual(
            scaling_quality_750["metadata"]["new_review_debt_count"], 18
        )
        self.assertEqual(
            scaling_quality_750["metadata"]["unclassified_new_review_debt_entry_ids"],
            [],
        )
        self.assertEqual(
            scaling_quality_750["metadata"]["audit_recommendation"],
            "review_before_promoting",
        )
        self.assertTrue(acceptance_750["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance_750["metadata"]["accepted_new_label_count"], 7)
        self.assertEqual(
            acceptance_750["metadata"]["accepted_new_label_entry_ids"],
            [
                "m_csa:728",
                "m_csa:733",
                "m_csa:735",
                "m_csa:739",
                "m_csa:740",
                "m_csa:742",
                "m_csa:750",
            ],
        )
        self.assertEqual(acceptance_750["metadata"]["countable_label_count"], 637)
        self.assertEqual(acceptance_750["metadata"]["pending_review_count"], 118)
        self.assertEqual(acceptance_750["metadata"]["accepted_review_gap_count"], 0)
        self.assertEqual(
            acceptance_750["metadata"]["accepted_reaction_substrate_mismatch_count"],
            0,
        )
        self.assertEqual(gate_750["metadata"]["gate_count"], 20)
        self.assertEqual(gate_750["metadata"]["passed_gate_count"], 20)
        self.assertTrue(gate_750["metadata"]["automation_ready_for_next_label_batch"])
        self.assertEqual(
            gate_750["metadata"]["active_queue_expert_label_decision_count"],
            113,
        )
        self.assertTrue(review_debt_deferral_750["metadata"]["deferral_ready"])
        self.assertEqual(
            review_debt_deferral_750["metadata"]["deferred_entry_count"], 118
        )
        self.assertEqual(
            review_debt_deferral_750["metadata"]["new_review_debt_count"], 18
        )
        self.assertTrue(
            preview_summary_750["metadata"][
                "all_supplied_scaling_quality_audits_ready"
            ]
        )
        self.assertEqual(
            batch_700_summary[
                "family_guardrail_reaction_substrate_mismatch_count"
            ],
            24,
        )
        self.assertTrue(
            batch_700_summary["reaction_substrate_mismatch_review_export_present"]
        )
        self.assertEqual(
            batch_700_summary[
                "reaction_substrate_mismatch_review_export_missing_count"
            ],
            0,
        )
        self.assertTrue(
            batch_700_summary["expert_label_decision_review_export_present"]
        )
        self.assertEqual(
            batch_700_summary["active_queue_expert_label_decision_count"],
            76,
        )
        self.assertEqual(
            batch_700_summary[
                "expert_label_decision_review_export_missing_count"
            ],
            0,
        )
        self.assertTrue(
            batch_700_summary["expert_label_decision_repair_candidates_present"]
        )
        self.assertEqual(
            batch_700_summary[
                "expert_label_decision_repair_candidates_missing_count"
            ],
            0,
        )
        self.assertTrue(
            batch_700_summary[
                "expert_label_decision_repair_guardrail_audit_present"
            ]
        )
        self.assertTrue(
            batch_700_summary[
                "expert_label_decision_local_evidence_gap_audit_present"
            ]
        )
        self.assertTrue(
            batch_700_summary[
                "expert_label_decision_local_evidence_gap_audit_ready"
            ]
        )
        self.assertEqual(
            batch_700_summary[
                "expert_label_decision_local_evidence_gap_audit_missing_count"
            ],
            0,
        )
        self.assertTrue(
            batch_700_summary[
                "expert_label_decision_local_evidence_review_export_present"
            ]
        )
        self.assertTrue(
            batch_700_summary[
                "expert_label_decision_local_evidence_review_export_ready"
            ]
        )
        self.assertEqual(
            batch_700_summary[
                "expert_label_decision_local_evidence_review_export_exported_count"
            ],
            21,
        )
        self.assertTrue(
            batch_700_summary[
                "expert_label_decision_local_evidence_repair_resolution_present"
            ]
        )
        self.assertTrue(
            batch_700_summary[
                "expert_label_decision_local_evidence_repair_resolution_ready"
            ]
        )
        self.assertEqual(
            batch_700_summary[
                "expert_label_decision_local_evidence_repair_resolution_resolved_entry_count"
            ],
            4,
        )
        self.assertTrue(
            batch_700_summary[
                "explicit_alternate_residue_position_requests_present"
            ]
        )
        self.assertTrue(
            batch_700_summary[
                "explicit_alternate_residue_position_requests_ready"
            ]
        )
        self.assertEqual(
            batch_700_summary[
                "explicit_alternate_residue_position_requests_count"
            ],
            3,
        )
        self.assertTrue(
            batch_700_summary["review_only_import_safety_audit_present"]
        )
        self.assertEqual(
            batch_700_summary[
                "review_only_import_safety_audit_total_new_countable_label_count"
            ],
            0,
        )
        self.assertEqual(preview_summary_675["metadata"]["blocker_count"], 0)
        self.assertTrue(preview_summary_675["metadata"]["all_active_queues_retain_unlabeled_candidates"])
        self.assertEqual(preview_summary_675["metadata"]["scaling_quality_audit_count"], 1)
        self.assertTrue(preview_summary_675["metadata"]["latest_scaling_quality_audit_present"])
        self.assertTrue(preview_summary_675["metadata"]["all_supplied_scaling_quality_audits_ready"])
        self.assertEqual(
            preview_summary_675["metadata"]["latest_scaling_quality_recommendation"],
            "review_before_promoting",
        )
        self.assertNotIn(
            "sequence_cluster_artifact_missing_for_near_duplicate_audit",
            preview_summary_675["metadata"]["latest_scaling_quality_review_warnings"],
        )
        self.assertTrue(preview_summary_675["rows"][0]["scaling_quality_ready"])
        self.assertEqual(preview_debt_675["metadata"]["review_debt_count"], 61)
        self.assertEqual(preview_debt_675["metadata"]["needs_more_evidence_count"], 61)
        self.assertEqual(preview_debt_675["metadata"]["carried_review_debt_count"], 37)
        self.assertEqual(preview_debt_675["metadata"]["new_review_debt_count"], 24)
        self.assertEqual(len(preview_debt_675["metadata"]["carried_review_debt_entry_ids"]), 37)
        self.assertEqual(
            preview_debt_675["metadata"]["new_review_debt_entry_ids"],
            [
                "m_csa:653",
                "m_csa:654",
                "m_csa:655",
                "m_csa:656",
                "m_csa:657",
                "m_csa:658",
                "m_csa:659",
                "m_csa:660",
                "m_csa:661",
                "m_csa:662",
                "m_csa:663",
                "m_csa:664",
                "m_csa:665",
                "m_csa:667",
                "m_csa:668",
                "m_csa:669",
                "m_csa:670",
                "m_csa:671",
                "m_csa:672",
                "m_csa:673",
                "m_csa:674",
                "m_csa:675",
                "m_csa:676",
                "m_csa:677",
            ],
        )
        self.assertEqual(
            preview_debt_675["metadata"]["recommended_next_action_counts_by_debt_status"]["new"],
            {
                "expert_family_boundary_review": 2,
                "expert_review_decision_needed": 3,
                "inspect_alternate_structure_or_cofactor_source": 14,
                "verify_local_cofactor_or_active_site_mapping": 5,
            },
        )
        self.assertTrue(preview_readiness_675["metadata"]["mechanically_ready"])
        self.assertEqual(
            preview_readiness_675["metadata"]["promotion_recommendation"],
            "review_before_promoting",
        )
        self.assertEqual(preview_readiness_675["metadata"]["review_debt_delta"], 8)
        self.assertEqual(preview_readiness_675["metadata"]["preview_new_review_debt_count"], 24)
        self.assertEqual(
            preview_readiness_675["metadata"]["preview_new_review_debt_entry_ids"],
            preview_debt_675["metadata"]["new_review_debt_entry_ids"],
        )
        self.assertEqual(
            preview_readiness_675["metadata"]["preview_new_review_debt_next_action_counts"],
            preview_debt_675["metadata"]["recommended_next_action_counts_by_debt_status"]["new"],
        )
        self.assertEqual(
            scaling_quality_675["metadata"]["audit_recommendation"],
            "review_before_promoting",
        )
        self.assertEqual(scaling_quality_675["metadata"]["new_review_debt_count"], 24)
        self.assertEqual(scaling_quality_675["metadata"]["accepted_new_debt_count"], 0)
        self.assertEqual(
            scaling_quality_675["metadata"]["unclassified_new_review_debt_entry_ids"],
            [],
        )
        self.assertEqual(
            scaling_quality_675["metadata"]["accepted_new_debt_entry_ids"],
            [],
        )
        self.assertEqual(
            scaling_quality_675["metadata"]["accepted_clean_label_entry_ids"],
            ["m_csa:666"],
        )
        self.assertEqual(
            scaling_quality_675["metadata"]["issue_class_counts"]["ontology_scope_pressure"],
            24,
        )
        self.assertEqual(
            scaling_quality_675["metadata"]["near_duplicate_audit_status"],
            "not_observed_in_sequence_cluster_artifact",
        )
        self.assertNotIn(
            "sequence_cluster_artifact_missing_for_near_duplicate_audit",
            scaling_quality_675["review_warnings"],
        )
        self.assertEqual(scaling_quality_675["metadata"]["sequence_cluster_missing_entry_count"], 0)
        self.assertEqual(sequence_clusters_675["metadata"]["entry_count"], 675)
        self.assertEqual(sequence_clusters_675["metadata"]["missing_reference_count"], 0)
        self.assertEqual(sequence_clusters_725["metadata"]["entry_count"], 725)
        self.assertEqual(sequence_clusters_725["metadata"]["missing_reference_count"], 0)
        self.assertEqual(
            scaling_quality_700["metadata"]["near_duplicate_audit_status"],
            "not_observed_in_sequence_cluster_artifact",
        )
        self.assertEqual(scaling_quality_700["metadata"]["sequence_cluster_missing_entry_count"], 0)
        self.assertEqual(scaling_quality_700["metadata"]["accepted_new_debt_count"], 0)
        self.assertEqual(
            scaling_quality_700["metadata"]["accepted_clean_label_entry_ids"],
            ["m_csa:686", "m_csa:688", "m_csa:694", "m_csa:697", "m_csa:699"],
        )
        self.assertTrue(scaling_quality_700["metadata"]["alternate_structure_scan_present"])
        self.assertEqual(
            scaling_quality_700["metadata"][
                "alternate_structure_scan_expected_family_hit_entry_ids"
            ],
            ["m_csa:679", "m_csa:696", "m_csa:698"],
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "alternate_structure_scan_local_expected_family_hit_entry_ids"
            ],
            [],
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "alternate_structure_scan_alternate_pdb_remapped_residue_position_entry_ids"
            ],
            [
                "m_csa:678",
                "m_csa:679",
                "m_csa:682",
                "m_csa:687",
                "m_csa:690",
                "m_csa:691",
                "m_csa:693",
                "m_csa:695",
                "m_csa:696",
                "m_csa:698",
                "m_csa:700",
                "m_csa:702",
            ],
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "alternate_structure_scan_alternate_pdb_remapped_residue_position_structure_count"
            ],
            63,
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "alternate_structure_scan_structure_wide_hit_without_local_support_entry_ids"
            ],
            ["m_csa:679", "m_csa:696", "m_csa:698"],
        )
        self.assertIn(
            "alternate_structure_hits_lack_local_support",
            scaling_quality_700["review_warnings"],
        )
        self.assertTrue(scaling_quality_700["metadata"]["remap_local_lead_audit_present"])
        self.assertEqual(
            scaling_quality_700["metadata"][
                "remap_local_lead_audit_strict_guardrail_entry_ids"
            ],
            ["m_csa:577", "m_csa:592", "m_csa:641"],
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "remap_local_lead_audit_expert_family_boundary_review_entry_ids"
            ],
            ["m_csa:577", "m_csa:641"],
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "remap_local_lead_audit_local_structure_selection_rule_candidate_entry_ids"
            ],
            [],
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "remap_local_lead_audit_expert_reaction_substrate_review_entry_ids"
            ],
            ["m_csa:592"],
        )
        self.assertTrue(
            scaling_quality_700["metadata"][
                "expert_label_decision_local_evidence_repair_resolution_present"
            ]
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "expert_label_decision_local_evidence_repair_resolution_resolved_entry_ids"
            ],
            ["m_csa:592", "m_csa:643", "m_csa:654", "m_csa:662"],
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "explicit_alternate_residue_position_request_entry_ids"
            ],
            ["m_csa:567", "m_csa:578", "m_csa:667"],
        )
        self.assertTrue(
            scaling_quality_700["metadata"][
                "review_only_import_safety_audit_present"
            ]
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "review_only_import_safety_audit_total_new_countable_label_count"
            ],
            0,
        )
        self.assertIn(
            "remap_local_leads_require_strict_guardrail",
            scaling_quality_700["review_warnings"],
        )
        self.assertTrue(
            scaling_quality_700["metadata"][
                "reaction_substrate_mismatch_audit_present"
            ]
        )
        self.assertEqual(
            scaling_quality_700["metadata"]["reaction_substrate_mismatch_audit_count"],
            18,
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "family_guardrail_reaction_substrate_mismatch_count"
            ],
            24,
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "family_guardrail_reaction_substrate_mismatch_label_state_counts"
            ],
            {"labeled": 17, "unlabeled": 7},
        )
        self.assertIn(
            "reaction_substrate_mismatch_audit_hits",
            scaling_quality_700["review_warnings"],
        )
        self.assertEqual(scaling_quality_725["metadata"]["accepted_new_debt_count"], 0)
        self.assertEqual(
            scaling_quality_725["metadata"]["accepted_clean_label_entry_ids"],
            ["m_csa:705", "m_csa:709", "m_csa:714", "m_csa:716", "m_csa:723", "m_csa:727"],
        )
        self.assertEqual(scaling_quality_725["metadata"]["new_review_debt_count"], 24)
        self.assertEqual(
            scaling_quality_725["metadata"]["unclassified_new_review_debt_entry_ids"],
            [],
        )
        self.assertEqual(
            scaling_quality_725["metadata"]["near_duplicate_audit_status"],
            "not_observed_in_sequence_cluster_artifact",
        )
        self.assertEqual(scaling_quality_725["metadata"]["sequence_cluster_missing_entry_count"], 0)
        self.assertEqual(
            scaling_quality_725["metadata"]["expert_label_decision_repair_guardrail_priority_repair_row_count"],
            25,
        )
        self.assertEqual(
            scaling_quality_725["metadata"]["expert_label_decision_local_evidence_gap_audit_audited_entry_count"],
            25,
        )
        self.assertEqual(
            scaling_quality_725["metadata"]["review_only_import_safety_audit_total_new_countable_label_count"],
            0,
        )
        self.assertTrue(scaling_quality_725["metadata"]["alternate_structure_scan_present"])
        self.assertEqual(
            scaling_quality_725["metadata"]["alternate_structure_scan_expected_family_hit_entry_ids"],
            ["m_csa:712", "m_csa:718", "m_csa:724"],
        )
        self.assertEqual(
            scaling_quality_725["metadata"]["alternate_structure_scan_local_expected_family_hit_entry_ids"],
            ["m_csa:712"],
        )
        self.assertEqual(
            scaling_quality_725["metadata"]["remap_local_lead_audit_strict_guardrail_entry_ids"],
            ["m_csa:712"],
        )
        self.assertEqual(
            scaling_quality_725["metadata"]["remap_local_lead_audit_expert_family_boundary_review_entry_ids"],
            ["m_csa:712"],
        )
        self.assertEqual(
            scaling_quality_725["metadata"]["explicit_alternate_residue_position_requests_count"],
            8,
        )
        self.assertEqual(
            scaling_quality_725["metadata"]["explicit_alternate_residue_position_requests_countable_label_candidate_count"],
            0,
        )
        self.assertIn(
            "expert_label_decision_rows_require_external_review",
            scaling_quality_725["review_warnings"],
        )
        self.assertEqual(remediation_700["metadata"]["requested_entry_count"], 20)
        self.assertEqual(remediation_700["metadata"]["emitted_row_count"], 20)
        self.assertTrue(remediation_700["metadata"]["all_requested_entries_have_gap_detail"])
        self.assertEqual(remediation_700_all["metadata"]["requested_entry_count"], 81)
        self.assertEqual(remediation_700_all["metadata"]["emitted_row_count"], 81)
        self.assertTrue(remediation_700_all["metadata"]["all_requested_entries_have_gap_detail"])
        self.assertEqual(remediation_700_all["metadata"]["missing_geometry_entry_ids"], [])
        self.assertEqual(remediation_700["metadata"]["alternate_pdb_position_gap_entry_count"], 16)
        self.assertEqual(remediation_700_all["metadata"]["alternate_pdb_position_gap_entry_count"], 69)
        self.assertEqual(remediation_700_all["metadata"]["selected_pdb_position_gap_entry_count"], 0)
        self.assertEqual(remediation_700["metadata"]["missing_graph_context_entry_ids"], [])
        self.assertEqual(remediation_700["metadata"]["missing_geometry_entry_ids"], [])
        self.assertEqual(
            remediation_700["metadata"]["remediation_bucket_counts"],
            {
                "active_site_mapping_repair": 1,
                "alternate_pdb_ligand_scan": 12,
                "expert_family_boundary_review": 1,
                "expert_label_decision": 2,
                "external_cofactor_source_review": 3,
                "local_mapping_or_structure_selection_review": 1,
            },
        )
        remediation_rows = {row["entry_id"]: row for row in remediation_700["rows"]}
        self.assertEqual(
            remediation_rows["m_csa:687"]["remediation_bucket"],
            "alternate_pdb_ligand_scan",
        )
        self.assertEqual(remediation_rows["m_csa:687"]["alternate_pdb_count"], 20)
        self.assertEqual(
            remediation_rows["m_csa:692"]["remediation_bucket"],
            "active_site_mapping_repair",
        )
        self.assertEqual(
            remediation_rows["m_csa:698"]["remediation_bucket"],
            "local_mapping_or_structure_selection_review",
        )
        self.assertEqual(remediation_rows["m_csa:679"]["selected_pdb_residue_position_count"], 5)
        self.assertEqual(
            remediation_rows["m_csa:679"]["alternate_pdb_with_residue_positions_count"],
            0,
        )
        self.assertEqual(
            remediation_rows["m_csa:696"]["alternate_pdb_with_residue_positions_count"],
            0,
        )
        self.assertEqual(
            remediation_rows["m_csa:698"]["alternate_pdb_with_residue_positions_count"],
            0,
        )
        self.assertEqual(alternate_scan_700["metadata"]["candidate_entry_count"], 13)
        self.assertEqual(alternate_scan_700["metadata"]["scanned_entry_count"], 13)
        self.assertEqual(alternate_scan_700["metadata"]["scanned_structure_count"], 152)
        self.assertEqual(alternate_scan_700["metadata"]["unscanned_structure_count"], 0)
        self.assertTrue(alternate_scan_700["metadata"]["all_candidate_structures_scanned"])
        self.assertEqual(alternate_scan_700["metadata"]["fetch_failure_count"], 0)
        self.assertEqual(
            alternate_scan_700["metadata"]["expected_family_hit_entry_ids"],
            ["m_csa:679", "m_csa:696", "m_csa:698"],
        )
        self.assertEqual(
            alternate_scan_700["metadata"][
                "structure_wide_hit_without_local_support_entry_ids"
            ],
            ["m_csa:679", "m_csa:696", "m_csa:698"],
        )
        self.assertEqual(
            alternate_scan_700["metadata"]["scan_outcome_counts"],
            {
                "alternate_structure_has_expected_cofactor_candidate": 3,
                "no_expected_cofactor_in_scanned_structures": 10,
            },
        )
        self.assertEqual(
            alternate_scan_700["metadata"][
                "alternate_pdb_remapped_residue_position_structure_count"
            ],
            63,
        )
        self.assertEqual(
            alternate_scan_700["metadata"]["residue_position_remap_basis_counts"],
            {
                "same_chain_residue_id": 58,
                "same_residue_id_chain_remap": 3,
                "unique_residue_id_code_remap": 2,
            },
        )
        self.assertEqual(
            alternate_scan_700["metadata"][
                "alternate_pdb_without_usable_residue_position_entry_ids"
            ],
            ["m_csa:680"],
        )
        self.assertEqual(alternate_scan_700_all["metadata"]["candidate_entry_count"], 46)
        self.assertEqual(alternate_scan_700_all["metadata"]["scanned_entry_count"], 46)
        self.assertEqual(alternate_scan_700_all["metadata"]["scanned_structure_count"], 739)
        self.assertEqual(alternate_scan_700_all["metadata"]["unscanned_structure_count"], 0)
        self.assertTrue(alternate_scan_700_all["metadata"]["all_candidate_structures_scanned"])
        self.assertEqual(alternate_scan_700_all["metadata"]["fetch_failure_count"], 0)
        self.assertEqual(
            alternate_scan_700_all["metadata"]["local_expected_family_hit_entry_ids"],
            ["m_csa:577", "m_csa:592", "m_csa:641"],
        )
        self.assertEqual(
            alternate_scan_700_all["metadata"]["scan_outcome_counts"],
            {
                "alternate_structure_has_expected_cofactor_candidate": 18,
                "no_expected_cofactor_in_scanned_structures": 27,
                "selected_structure_has_expected_cofactor_candidate": 1,
            },
        )
        self.assertEqual(
            alternate_scan_700_all["metadata"][
                "local_expected_family_hit_from_remap_entry_ids"
            ],
            ["m_csa:577", "m_csa:592", "m_csa:641"],
        )
        self.assertEqual(
            alternate_scan_700_all["metadata"][
                "alternate_pdb_remapped_residue_position_structure_count"
            ],
            362,
        )
        self.assertEqual(
            alternate_scan_700_all["metadata"][
                "alternate_pdb_without_usable_residue_position_entry_ids"
            ],
            [
                "m_csa:13",
                "m_csa:510",
                "m_csa:529",
                "m_csa:624",
                "m_csa:657",
                "m_csa:673",
                "m_csa:680",
            ],
        )
        self.assertEqual(remap_leads_700_all["metadata"]["lead_count"], 44)
        self.assertEqual(
            remap_leads_700_all["metadata"]["lead_type_counts"],
            {
                "local_expected_family_hit_from_remap": 3,
                "remapped_positions_without_expected_family_hit": 25,
                "structure_wide_hit_without_local_support": 16,
            },
        )
        self.assertEqual(
            remap_leads_700_all["metadata"][
                "local_expected_family_hit_from_remap_entry_ids"
            ],
            ["m_csa:577", "m_csa:592", "m_csa:641"],
        )
        self.assertEqual(
            [row["entry_id"] for row in remap_leads_700_all["rows"][:3]],
            ["m_csa:577", "m_csa:592", "m_csa:641"],
        )
        self.assertTrue(
            all(
                row["countable_label_candidate"] is False
                for row in remap_leads_700_all["rows"]
            )
        )
        self.assertEqual(
            remap_local_audit_700["metadata"]["audited_entry_ids"],
            ["m_csa:577", "m_csa:592", "m_csa:641"],
        )
        self.assertEqual(
            remap_local_audit_700["metadata"]["decision_counts"],
            {
                "expert_family_boundary_review_required": 2,
                "expert_reaction_substrate_review_required": 1,
            },
        )
        self.assertEqual(
            remap_local_audit_700["metadata"][
                "expert_family_boundary_review_entry_ids"
            ],
            ["m_csa:577", "m_csa:641"],
        )
        self.assertEqual(
            remap_local_audit_700["metadata"][
                "local_structure_selection_rule_candidate_entry_ids"
            ],
            [],
        )
        self.assertEqual(
            remap_local_audit_700["metadata"][
                "expert_reaction_substrate_review_entry_ids"
            ],
            ["m_csa:592"],
        )
        self.assertEqual(
            remap_local_audit_700["metadata"]["strict_remap_guardrail_entry_ids"],
            ["m_csa:577", "m_csa:592", "m_csa:641"],
        )
        self.assertTrue(
            all(
                row["countable_label_candidate"] is False
                for row in remap_local_audit_700["rows"]
            )
        )
        self.assertEqual(
            structure_selection_700["metadata"]["candidate_entry_ids"],
            [],
        )
        self.assertEqual(
            structure_selection_700["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(structure_selection_700["rows"], [])
        self.assertEqual(reaction_mismatch_700["metadata"]["mismatch_count"], 18)
        self.assertIn(
            "m_csa:592",
            reaction_mismatch_700["metadata"]["mismatch_entry_ids"],
        )
        self.assertEqual(
            reaction_mismatch_700["metadata"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(sequence_clusters_700["metadata"]["entry_count"], 700)
        self.assertEqual(sequence_clusters_700["metadata"]["missing_reference_count"], 0)
        self.assertEqual(scaling_quality_675["blockers"], [])
        scaling_failure_modes = {
            row["id"]: row for row in scaling_quality_675["failure_modes"]
        }
        self.assertEqual(
            scaling_failure_modes["hard_negatives_concentrated_in_one_family"]["status"],
            "not_observed_zero_hard_negatives",
        )
        self.assertEqual(
            scaling_failure_modes["cofactor_family_ambiguity"]["issue_count"],
            19,
        )
        self.assertEqual(
            scaling_failure_modes["review_queue_collapse_to_one_chemistry"]["status"],
            "observed",
        )
        scaling_failure_modes_700 = {
            row["id"]: row for row in scaling_quality_700["failure_modes"]
        }
        self.assertEqual(
            scaling_failure_modes_700[
                "conservative_remap_local_evidence_without_explicit_alt_positions"
            ]["entry_ids"],
            ["m_csa:577", "m_csa:592", "m_csa:641"],
        )
        self.assertEqual(
            scaling_failure_modes_700[
                "reaction_direction_or_substrate_class_mismatch"
            ]["issue_count"],
            23,
        )
        self.assertEqual(
            scaling_failure_modes_700[
                "expert_label_decision_review_only_debt"
            ]["issue_count"],
            76,
        )
        self.assertEqual(
            scaling_failure_modes_700[
                "expert_label_decision_review_only_debt"
            ]["evidence"]["countable_label_candidate_count"],
            0,
        )
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions"], 0)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(candidates_550["metadata"]["ready_for_label_review_count"], 0)
        self.assertEqual(candidates_575["metadata"]["ready_for_label_review_count"], 0)
        self.assertEqual(candidates_600["metadata"]["ready_for_label_review_count"], 0)
        self.assertEqual(candidates_625["metadata"]["ready_for_label_review_count"], 25)
        self.assertEqual(candidates_650["metadata"]["ready_for_label_review_count"], 31)
        self.assertTrue(gate_550["metadata"]["automation_ready_for_next_label_batch"])
        self.assertTrue(gate_575["metadata"]["automation_ready_for_next_label_batch"])
        self.assertTrue(gate_600["metadata"]["automation_ready_for_next_label_batch"])
        self.assertTrue(gate_625["metadata"]["automation_ready_for_next_label_batch"])
        self.assertTrue(gate_650["metadata"]["automation_ready_for_next_label_batch"])
        self.assertTrue(gate_675["metadata"]["automation_ready_for_next_label_batch"])
        self.assertTrue(gate_700["metadata"]["automation_ready_for_next_label_batch"])
        self.assertEqual(gate_700["metadata"]["gate_count"], 21)
        self.assertEqual(gate_700["metadata"]["passed_gate_count"], 21)
        self.assertTrue(gate_700["gates"]["expert_label_decision_review_export_ready"])
        self.assertTrue(
            gate_700["gates"]["expert_label_decision_repair_candidates_ready"]
        )
        self.assertTrue(
            gate_700["gates"]["expert_label_decision_repair_guardrails_ready"]
        )
        self.assertTrue(
            gate_700["gates"][
                "expert_label_decision_local_evidence_gaps_audited"
            ]
        )
        self.assertTrue(
            gate_700["gates"][
                "expert_label_decision_local_evidence_review_export_ready"
            ]
        )
        self.assertEqual(
            gate_700["metadata"]["active_queue_expert_label_decision_count"],
            76,
        )
        self.assertEqual(
            gate_700["metadata"][
                "expert_label_decision_review_export_missing_entry_ids"
            ],
            [],
        )
        self.assertEqual(
            gate_700["metadata"][
                "expert_label_decision_repair_candidates_missing_entry_ids"
            ],
            [],
        )
        self.assertTrue(
            gate_700["metadata"][
                "expert_label_decision_repair_candidate_entry_id_count_matches"
            ]
        )
        self.assertEqual(
            gate_700["metadata"][
                "expert_label_decision_repair_guardrail_priority_repair_row_count"
            ],
            21,
        )
        self.assertTrue(
            gate_700["metadata"][
                "expert_label_decision_local_evidence_gap_audit_present"
            ]
        )
        self.assertTrue(
            gate_700["metadata"][
                "expert_label_decision_local_evidence_gap_audit_ready"
            ]
        )
        self.assertEqual(
            gate_700["metadata"][
                "expert_label_decision_local_evidence_gap_audit_audited_entry_count"
            ],
            21,
        )
        self.assertTrue(
            gate_700["metadata"][
                "expert_label_decision_local_evidence_review_export_present"
            ]
        )
        self.assertEqual(
            gate_700["metadata"][
                "expert_label_decision_local_evidence_review_export_exported_count"
            ],
            21,
        )
        self.assertTrue(
            gate_700["gates"][
                "expert_label_decision_local_evidence_repair_resolution_ready"
            ]
        )
        self.assertEqual(
            gate_700["metadata"][
                "expert_label_decision_local_evidence_repair_resolution_resolved_entry_ids"
            ],
            ["m_csa:592", "m_csa:643", "m_csa:654", "m_csa:662"],
        )
        self.assertTrue(
            gate_700["gates"]["explicit_alternate_residue_position_requests_ready"]
        )
        self.assertEqual(
            gate_700["metadata"][
                "explicit_alternate_residue_position_request_entry_ids"
            ],
            ["m_csa:567", "m_csa:578", "m_csa:667"],
        )
        self.assertTrue(gate_700["gates"]["review_only_import_safety_audit_ready"])
        self.assertEqual(
            gate_700["metadata"][
                "review_only_import_safety_audit_total_new_countable_label_count"
            ],
            0,
        )
        self.assertTrue(
            gate_700["gates"][
                "atp_phosphoryl_transfer_family_expansion_ready"
            ]
        )
        self.assertEqual(
            gate_700["metadata"][
                "atp_phosphoryl_transfer_family_expansion_mapped_family_ids"
            ],
            ["askha", "atp_grasp", "dnk", "epk", "ghkl", "ghmp", "ndk", "pfka", "pfkb"],
        )
        self.assertIn(
            "reaction_substrate_mismatch_value",
            active_queue_700["metadata"]["ranking_terms"],
        )
        self.assertIn(
            "atp_phosphoryl_family_boundary_value",
            active_queue_700["metadata"]["ranking_terms"],
        )
        self.assertEqual(
            active_queue_700["metadata"][
                "atp_phosphoryl_transfer_family_boundary_count"
            ],
            15,
        )
        self.assertEqual(
            family_guardrails_700["metadata"]["reaction_substrate_mismatch_count"],
            24,
        )
        self.assertEqual(
            family_guardrails_700["metadata"]["priority_added_count"],
            14,
        )
        self.assertEqual(
            family_guardrails_700["metadata"]["blocker_counts"]["reaction_substrate_mismatch"],
            24,
        )
        self.assertEqual(
            family_guardrails_700["metadata"]["blocker_counts"][
                "atp_phosphoryl_transfer_family_boundary"
            ],
            20,
        )
        self.assertEqual(
            family_guardrails_700["metadata"][
                "reaction_substrate_mismatch_label_state_counts"
            ],
            {"labeled": 17, "unlabeled": 7},
        )
        self.assertEqual(active_queue_700["metadata"]["total_unlabeled_candidate_count"], 76)
        self.assertEqual(active_queue_700["metadata"]["score_totals"]["reaction_substrate_mismatch_value"], 23.4)
        self.assertEqual(expert_export_700["metadata"]["exported_count"], 182)
        self.assertEqual(
            expert_label_decision_export_700["metadata"]["method"],
            "expert_label_decision_review_export",
        )
        self.assertEqual(
            expert_label_decision_export_700["metadata"]["exported_count"],
            76,
        )
        self.assertEqual(
            expert_label_decision_export_700["metadata"]["decision_counts"],
            {"no_decision": 76},
        )
        self.assertEqual(
            expert_label_decision_export_700["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertEqual(
            expert_label_decision_export_700["metadata"][
                "missing_reaction_substrate_mismatch_export_entry_ids"
            ],
            [],
        )
        self.assertEqual(
            expert_label_decision_export_700["metadata"][
                "reaction_substrate_mismatch_lane_count"
            ],
            7,
        )
        self.assertEqual(
            expert_label_decision_export_700["metadata"][
                "quality_risk_flag_counts"
            ]["external_expert_decision_required"],
            76,
        )
        self.assertEqual(
            expert_label_decision_export_700["metadata"][
                "quality_risk_flag_counts"
            ]["cofactor_family_ambiguity"],
            50,
        )
        self.assertTrue(
            expert_label_decision_batch_700["metadata"][
                "expert_label_decision_review_only"
            ]
        )
        self.assertEqual(
            expert_label_decision_batch_700["metadata"]["decision_counts"],
            {"mark_needs_more_evidence": 66, "reject_label": 10},
        )
        self.assertEqual(
            expert_label_decision_local_export_700["metadata"]["method"],
            "expert_label_decision_local_evidence_review_export",
        )
        self.assertTrue(
            expert_label_decision_local_export_700["metadata"]["export_ready"]
        )
        self.assertEqual(
            expert_label_decision_local_export_700["metadata"]["exported_count"],
            21,
        )
        self.assertEqual(
            expert_label_decision_local_export_700["metadata"]["decision_counts"],
            {"no_decision": 21},
        )
        self.assertTrue(
            expert_label_decision_local_batch_700["metadata"][
                "local_evidence_gap_review_only"
            ]
        )
        self.assertEqual(
            expert_label_decision_local_batch_700["metadata"]["decision_counts"],
            {"mark_needs_more_evidence": 14, "reject_label": 7},
        )
        self.assertTrue(
            expert_label_decision_local_plan_700["metadata"]["repair_plan_ready"]
        )
        self.assertEqual(
            expert_label_decision_local_plan_700["metadata"]["planned_entry_count"],
            21,
        )
        self.assertEqual(
            expert_label_decision_local_plan_700["metadata"]["repair_lane_counts"][
                "expert_reaction_substrate_review"
            ],
            4,
        )
        self.assertTrue(
            expert_label_decision_local_plan_700["metadata"][
                "all_planned_rows_review_exported"
            ]
        )
        self.assertEqual(
            expert_label_decision_local_plan_700["rows"][0]["entry_id"],
            "m_csa:592",
        )
        self.assertEqual(
            expert_label_decision_local_resolution_700["metadata"]["method"],
            "expert_label_decision_local_evidence_repair_resolution",
        )
        self.assertTrue(
            expert_label_decision_local_resolution_700["metadata"]["resolution_ready"]
        )
        self.assertEqual(
            expert_label_decision_local_resolution_700["metadata"][
                "resolved_entry_ids"
            ],
            ["m_csa:592", "m_csa:643", "m_csa:654", "m_csa:662"],
        )
        self.assertEqual(
            expert_label_decision_local_resolution_700["metadata"][
                "remaining_open_entry_count"
            ],
            17,
        )
        self.assertEqual(
            expert_label_decision_local_resolution_700["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertEqual(
            alternate_residue_requests_700["metadata"]["method"],
            "explicit_alternate_residue_position_sourcing_requests",
        )
        self.assertTrue(
            alternate_residue_requests_700["metadata"]["sourcing_request_ready"]
        )
        self.assertEqual(
            alternate_residue_requests_700["metadata"]["request_entry_ids"],
            ["m_csa:567", "m_csa:578", "m_csa:667"],
        )
        self.assertEqual(
            alternate_residue_requests_700["metadata"][
                "candidate_alternate_structure_count"
            ],
            34,
        )
        self.assertEqual(
            alternate_residue_requests_700["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertTrue(
            review_only_import_safety_700["metadata"]["countable_import_safe"]
        )
        self.assertEqual(
            review_only_import_safety_700["metadata"][
                "total_new_countable_label_count"
            ],
            0,
        )
        self.assertEqual(
            review_only_import_safety_700["metadata"]["review_only_artifact_count"],
            3,
        )
        self.assertEqual(
            expert_label_decision_repair_700["metadata"]["candidate_count"],
            76,
        )
        self.assertEqual(
            expert_label_decision_repair_700["metadata"]["emitted_row_count"],
            30,
        )
        self.assertEqual(
            expert_label_decision_repair_700["metadata"]["omitted_by_max_rows"],
            46,
        )
        self.assertEqual(
            len(expert_label_decision_repair_700["metadata"]["candidate_entry_ids"]),
            76,
        )
        self.assertEqual(
            expert_label_decision_repair_700["metadata"][
                "remediation_context_linked_count"
            ],
            76,
        )
        self.assertEqual(
            expert_label_decision_repair_700["metadata"][
                "alternate_structure_scan_context_linked_count"
            ],
            42,
        )
        self.assertEqual(
            expert_label_decision_repair_all_700["metadata"]["emitted_row_count"],
            76,
        )
        self.assertTrue(
            expert_label_decision_repair_all_700["metadata"][
                "all_candidates_retained"
            ]
        )
        self.assertEqual(
            expert_label_decision_repair_700["metadata"][
                "repair_bucket_counts"
            ]["active_site_mapping_or_structure_gap_repair"],
            14,
        )
        self.assertEqual(
            expert_label_decision_repair_700["metadata"][
                "repair_bucket_counts"
            ]["cofactor_evidence_repair"],
            30,
        )
        self.assertEqual(
            expert_label_decision_repair_guardrail_700["metadata"]["method"],
            "expert_label_decision_repair_guardrail_audit",
        )
        self.assertTrue(
            expert_label_decision_repair_guardrail_700["metadata"]["guardrail_ready"]
        )
        self.assertEqual(
            expert_label_decision_repair_guardrail_700["metadata"][
                "priority_repair_row_count"
            ],
            21,
        )
        self.assertEqual(
            expert_label_decision_repair_guardrail_700["metadata"][
                "active_site_mapping_or_structure_gap_row_count"
            ],
            14,
        )
        self.assertEqual(
            expert_label_decision_repair_guardrail_700["metadata"][
                "text_leakage_or_nonlocal_evidence_risk_row_count"
            ],
            9,
        )
        self.assertEqual(
            expert_label_decision_repair_guardrail_700["metadata"][
                "local_expected_family_evidence_review_only_entry_ids"
            ],
            ["m_csa:577", "m_csa:592", "m_csa:641"],
        )
        self.assertEqual(
            expert_label_decision_repair_guardrail_700["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertEqual(
            expert_label_decision_local_gap_700["metadata"]["method"],
            "expert_label_decision_local_evidence_gap_audit",
        )
        self.assertTrue(expert_label_decision_local_gap_700["metadata"]["audit_ready"])
        self.assertEqual(
            expert_label_decision_local_gap_700["metadata"]["audited_entry_count"],
            21,
        )
        self.assertEqual(
            expert_label_decision_local_gap_700["metadata"][
                "countable_label_candidate_count"
            ],
            0,
        )
        self.assertEqual(
            expert_label_decision_local_gap_700["metadata"][
                "selected_structure_residue_support_shortfall_entry_ids"
            ],
            [
                "m_csa:553",
                "m_csa:567",
                "m_csa:592",
                "m_csa:654",
                "m_csa:659",
                "m_csa:662",
                "m_csa:664",
                "m_csa:667",
                "m_csa:677",
                "m_csa:690",
                "m_csa:691",
                "m_csa:692",
                "m_csa:698",
                "m_csa:701",
            ],
        )
        self.assertEqual(
            expert_label_decision_local_gap_700["metadata"][
                "single_structure_no_alternate_context_entry_ids"
            ],
            ["m_csa:654", "m_csa:659", "m_csa:692", "m_csa:701"],
        )
        self.assertEqual(
            ontology_gap_audit_700["metadata"]["method"],
            "mechanism_ontology_gap_audit",
        )
        self.assertFalse(ontology_gap_audit_700["metadata"]["ontology_update_ready"])
        self.assertEqual(
            ontology_gap_audit_700["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertGreaterEqual(
            ontology_gap_audit_700["metadata"]["scope_signal_counts"][
                "transferase_phosphoryl"
            ],
            30,
        )
        self.assertEqual(
            ontology_gap_audit_700["metadata"][
                "local_evidence_gap_context_entry_count"
            ],
            16,
        )
        self.assertEqual(
            ontology_gap_audit_700["metadata"]["local_evidence_gap_class_counts"][
                "single_structure_no_alternate_context"
            ],
            4,
        )
        self.assertEqual(
            ontology_gap_audit_700["metadata"][
                "priority_local_evidence_gap_added_count"
            ],
            9,
        )
        self.assertIn(
            "hydrolysis",
            ontology_gap_audit_700["metadata"]["existing_ontology_families"],
        )
        self.assertEqual(
            learned_manifest_700["metadata"]["method"],
            "learned_retrieval_manifest",
        )
        self.assertEqual(
            learned_manifest_700["metadata"]["embedding_status"],
            "not_computed_interface_only",
        )
        self.assertEqual(
            learned_manifest_700["metadata"]["labeled_entry_count"],
            623,
        )
        self.assertEqual(
            learned_manifest_700["metadata"]["eligible_entry_count"],
            562,
        )
        self.assertEqual(
            learned_manifest_700["metadata"]["ineligible_entry_count"],
            61,
        )
        self.assertEqual(
            sequence_failure_sets_700["metadata"]["method"],
            "sequence_similarity_failure_set_audit",
        )
        self.assertEqual(
            sequence_failure_sets_700["metadata"]["duplicate_cluster_count"],
            2,
        )
        self.assertEqual(
            sequence_failure_sets_700["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertEqual(
            reaction_mismatch_export_700["metadata"]["method"],
            "reaction_substrate_mismatch_review_export",
        )
        self.assertEqual(reaction_mismatch_export_700["metadata"]["exported_count"], 24)
        self.assertEqual(
            reaction_mismatch_export_700["metadata"]["label_state_counts"],
            {"labeled": 17, "unlabeled": 7},
        )
        self.assertEqual(
            reaction_mismatch_export_700["metadata"]["current_label_type_counts"],
            {"out_of_scope": 17, "unlabeled": 7},
        )
        self.assertEqual(
            reaction_mismatch_export_700["metadata"]["labeled_seed_mismatch_count"],
            0,
        )
        self.assertTrue(
            reaction_mismatch_decision_batch_700["metadata"][
                "reaction_substrate_mismatch_review_only"
            ]
        )
        self.assertEqual(
            reaction_mismatch_decision_batch_700["metadata"]["decision_counts"],
            {"reject_label": 17, "accept_label": 7},
        )
        self.assertTrue(
            reaction_mismatch_export_700["metadata"][
                "all_reaction_audit_mismatches_exported"
            ]
        )
        self.assertTrue(
            reaction_mismatch_export_700["metadata"][
                "all_family_guardrail_mismatches_exported"
            ]
        )
        self.assertEqual(
            reaction_mismatch_export_700["metadata"]["recommended_path"],
            "expert_reaction_substrate_review_before_ontology_split",
        )
        self.assertEqual(
            reaction_mismatch_export_700["metadata"]["countable_label_candidate_count"],
            0,
        )
        self.assertTrue(
            scaling_quality_700["gates"][
                "reaction_substrate_mismatch_review_export_retains_mismatch_lanes"
            ]
        )
        self.assertTrue(
            scaling_quality_700["metadata"][
                "reaction_substrate_mismatch_review_export_present"
            ]
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "reaction_substrate_mismatch_review_export_missing_entry_ids"
            ],
            [],
        )
        self.assertTrue(
            scaling_quality_700["gates"][
                "expert_label_decision_review_export_retains_review_only_lanes"
            ]
        )
        self.assertTrue(
            scaling_quality_700["gates"][
                "expert_label_decision_repair_candidates_cover_review_only_lanes"
            ]
        )
        self.assertTrue(
            scaling_quality_700["metadata"][
                "expert_label_decision_review_export_present"
            ]
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "expert_label_decision_review_export_missing_entry_ids"
            ],
            [],
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "expert_label_decision_review_export_countable_label_candidate_count"
            ],
            0,
        )
        self.assertTrue(
            scaling_quality_700["metadata"][
                "expert_label_decision_repair_candidates_present"
            ]
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "expert_label_decision_repair_candidates_missing_entry_ids"
            ],
            [],
        )
        self.assertTrue(
            scaling_quality_700["metadata"][
                "expert_label_decision_repair_candidate_entry_id_count_matches"
            ]
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "expert_label_decision_repair_candidates_countable_label_candidate_count"
            ],
            0,
        )
        self.assertTrue(
            scaling_quality_700["gates"][
                "expert_label_decision_repair_guardrail_keeps_priority_lanes_non_countable"
            ]
        )
        self.assertTrue(
            scaling_quality_700["metadata"][
                "expert_label_decision_repair_guardrail_audit_present"
            ]
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "expert_label_decision_repair_guardrail_priority_repair_row_count"
            ],
            21,
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "expert_label_decision_repair_guardrail_countable_label_candidate_count"
            ],
            0,
        )
        self.assertTrue(
            scaling_quality_700["gates"][
                "expert_label_decision_local_evidence_gaps_audited"
            ]
        )
        self.assertTrue(
            scaling_quality_700["gates"][
                "expert_label_decision_local_evidence_review_export_ready"
            ]
        )
        self.assertTrue(
            scaling_quality_700["metadata"][
                "expert_label_decision_local_evidence_gap_audit_present"
            ]
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "expert_label_decision_local_evidence_gap_audit_audited_entry_count"
            ],
            21,
        )
        self.assertTrue(
            scaling_quality_700["metadata"][
                "expert_label_decision_local_evidence_review_export_present"
            ]
        )
        self.assertEqual(
            scaling_quality_700["metadata"][
                "expert_label_decision_local_evidence_review_export_exported_count"
            ],
            21,
        )
        self.assertIn(
            "expert_label_decision_rows_require_external_review",
            scaling_quality_700["review_warnings"],
        )
        self.assertIn(
            "expert_label_decision_priority_repair_lanes_review_only",
            scaling_quality_700["review_warnings"],
        )
        self.assertIn(
            "expert_label_decision_local_evidence_gaps_remain_review_only",
            scaling_quality_700["review_warnings"],
        )
        self.assertTrue(
            all(
                item["mismatch_context"]["countable_label_candidate"] is False
                for item in reaction_mismatch_export_700["review_items"]
            )
        )
        self.assertTrue(
            all(
                item["expert_label_decision_context"]["countable_label_candidate"]
                is False
                for item in expert_label_decision_export_700["review_items"]
            )
        )
        self.assertEqual(gate_550["blockers"], [])
        self.assertEqual(gate_575["blockers"], [])
        self.assertEqual(gate_600["blockers"], [])
        self.assertEqual(gate_625["blockers"], [])
        self.assertEqual(gate_650["blockers"], [])
        self.assertEqual(gate_675["blockers"], [])
        self.assertEqual(gate_700["blockers"], [])

    def test_selected_pdb_override_path_is_non_countable_and_guardrail_clean(self) -> None:
        override_plan = _load_json(
            ROOT / "artifacts" / "v3_selected_pdb_override_plan_700.json"
        )
        geometry = _load_json(
            ROOT
            / "artifacts"
            / "v3_geometry_features_1000_selected_pdb_override.json"
        )
        evaluation = _load_json(
            ROOT
            / "artifacts"
            / "v3_geometry_label_eval_1000_selected_pdb_override.json"
        )
        hard_negatives = _load_json(
            ROOT
            / "artifacts"
            / "v3_hard_negative_controls_1000_selected_pdb_override.json"
        )
        in_scope_failures = _load_json(
            ROOT
            / "artifacts"
            / "v3_in_scope_failure_analysis_1000_selected_pdb_override.json"
        )

        self.assertEqual(
            override_plan["metadata"]["blocker_removed"],
            "selected_pdb_single_point_mitigation",
        )
        self.assertEqual(
            override_plan["metadata"]["ready_to_apply_entry_ids"],
            ["m_csa:577", "m_csa:641"],
        )
        self.assertEqual(override_plan["metadata"]["skipped_entry_ids"], ["m_csa:592"])
        self.assertEqual(
            override_plan["metadata"]["countable_label_candidate_count"], 0
        )
        rows = {row["entry_id"]: row for row in override_plan["rows"]}
        self.assertEqual(rows["m_csa:577"]["override_pdb_id"], "1AWB")
        self.assertEqual(rows["m_csa:641"]["override_pdb_id"], "1J7N")
        self.assertEqual(rows["m_csa:592"]["apply_status"], "skipped_by_policy")

        self.assertEqual(
            geometry["metadata"]["selected_pdb_override_applied_count"], 2
        )
        entries = {row["entry_id"]: row for row in geometry["entries"]}
        self.assertEqual(entries["m_csa:577"]["pdb_id"], "1AWB")
        self.assertEqual(entries["m_csa:641"]["pdb_id"], "1J7N")
        self.assertEqual(entries["m_csa:592"]["pdb_id"], "3IDH")
        self.assertIn(
            "metal_ion",
            entries["m_csa:577"]["ligand_context"]["cofactor_families"],
        )
        self.assertIn(
            "metal_ion",
            entries["m_csa:641"]["ligand_context"]["cofactor_families"],
        )
        self.assertEqual(
            evaluation["metadata"]["out_of_scope_false_non_abstentions"], 0
        )
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)

    def test_current_geometry_retrieval_artifacts_are_text_leakage_safe(self) -> None:
        retrieval = _load_json(ROOT / "artifacts" / "v3_geometry_retrieval_1000.json")

        self.assertEqual(
            retrieval["metadata"]["blocker_removed"],
            "text_leakage_mitigation_geometry_retrieval",
        )
        leakage_policy = retrieval["metadata"]["leakage_policy"]
        self.assertFalse(leakage_policy["text_or_label_fields_used_for_score"])
        self.assertIn(
            "mechanism_text_snippets",
            leakage_policy["excluded_predictive_fields"],
        )
        self.assertIn(
            "local_plp_ligand_anchor_context",
            retrieval["metadata"]["predictive_evidence_sources"],
        )
        results = {row["entry_id"]: row for row in retrieval["results"]}
        for entry_id in ("m_csa:410", "m_csa:449"):
            plp_hit = next(
                hit
                for hit in results[entry_id]["top_fingerprints"]
                if hit["fingerprint_id"] == "plp_dependent_enzyme"
            )
            self.assertFalse(plp_hit["text_or_label_fields_used_for_score"])
            self.assertEqual(plp_hit["plp_ligand_anchor_score"], 1.0)
            self.assertIn("counterevidence_reasons_by_category", plp_hit)
            self.assertIn("counterevidence_category_counts", plp_hit)

    def test_mechanism_text_counterevidence_ablation_artifact_marks_review_debt(
        self,
    ) -> None:
        ablation = _load_json(
            ROOT / "artifacts" / "v3_mechanism_text_counterevidence_ablation_1000.json"
        )

        metadata = ablation["metadata"]
        self.assertEqual(metadata["method"], "mechanism_text_counterevidence_ablation")
        self.assertEqual(
            metadata["removed_fields"],
            ["mechanism_text_count", "mechanism_text_snippets"],
        )
        self.assertGreater(metadata["changed_row_count"], 0)
        self.assertGreater(metadata["review_debt_row_count"], 0)
        self.assertEqual(metadata["structure_local_guardrail_loss_row_count"], 0)
        review_debt_rows = [
            row for row in ablation["changed_rows"] if row.get("review_debt")
        ]
        self.assertEqual(len(review_debt_rows), metadata["review_debt_row_count"])
        self.assertTrue(
            all(
                row["orphan_discovery_claim_status"]
                == "review_debt_text_only_not_valid_for_orphan_discovery_claims"
                for row in review_debt_rows
            )
        )
        self.assertTrue(
            any(
                row["lost_mechanism_text_review_context_reasons"]
                for row in review_debt_rows
            )
        )

    def test_fold_augmented_train_cal_oos_surface_current_counts(self) -> None:
        surface = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_train_cal_oos_negative_surface_scores_current702_20260601.json"
        )
        blockers = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_train_cal_oos_negative_surface_blocker_resolution_current702_20260601.json"
        )
        oos_contract = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_abstention_threshold_contract_oos_calibrated_current702_20260601.json"
        )

        self.assertEqual(surface["counts"]["candidate_ids_requested"], 76)
        self.assertEqual(surface["counts"]["candidate_rows_with_full_channel_scores"], 71)
        self.assertEqual(surface["counts"]["candidate_predicted_geometry_ok_rows"], 71)
        self.assertEqual(surface["counts"]["foldseek_rows_with_nearest_train_hits"], 75)
        self.assertEqual(blockers["counts"]["missing_full_score_rows"], 5)
        self.assertNotIn(
            "missing_accession_compatible_sequence_positions",
            blockers["counts"]["blocker_reason_counts"],
        )
        repaired_rows = {
            row["entry_id"]: row
            for row in surface["candidate_row_scores"]
            if row.get("predicted_geometry_accession_repair")
        }
        self.assertEqual(
            {
                "m_csa:57",
                "m_csa:106",
                "m_csa:178",
                "m_csa:284",
                "m_csa:314",
                "m_csa:503",
            },
            set(repaired_rows),
        )
        self.assertEqual(
            repaired_rows["m_csa:284"]["predicted_geometry_accession"],
            "O66188",
        )
        self.assertEqual(
            repaired_rows["m_csa:284"]["predicted_structure_fold_channel"][
                "raw_query_name"
            ],
            "afdb_O66188_v6",
        )
        primary = oos_contract["primary_channel_readout"][
            "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain"
        ]
        self.assertEqual(primary["threshold"], 0.44155)
        self.assertEqual(primary["calibration_oos_abstained"], 28)
        self.assertEqual(primary["calibration_oos_total"], 71)

    def test_train_cal_oos_sufficiency_decision_current_counts(self) -> None:
        decision = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_train_cal_oos_negative_surface_sufficiency_decision_current702_20260601.json"
        )

        self.assertEqual(
            decision["status"],
            "research_contract_sufficient_with_blocker_disclosure",
        )
        self.assertTrue(decision["decision"]["research_surface_sufficient"])
        self.assertFalse(decision["decision"]["production_surface_sufficient"])
        self.assertEqual(decision["counts"]["candidate_ids_requested"], 76)
        self.assertEqual(decision["counts"]["score_complete_rows"], 71)
        self.assertEqual(decision["counts"]["missing_full_score_rows"], 5)
        self.assertEqual(decision["counts"]["fold_only_salvage_rows"], 4)
        self.assertEqual(decision["counts"]["calibration_oos_total_used_by_contract"], 71)
        self.assertEqual(decision["threshold_readout"]["oos_calibrated_threshold"], 0.44155)

    def test_train_cal_oos_remaining_blocker_clearance_attempts_current_counts(self) -> None:
        attempts = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_train_cal_oos_remaining_blocker_clearance_attempts_current702_20260601.json"
        )

        self.assertEqual(
            attempts["status"],
            "clearance_attempts_staged_no_safe_repo_mutation",
        )
        self.assertEqual(attempts["counts"]["remaining_blocker_rows"], 5)
        self.assertEqual(attempts["counts"]["safe_repairs_applied"], 0)
        self.assertEqual(attempts["counts"]["rows_with_fold_only_evidence"], 4)
        self.assertEqual(
            {row["entry_id"] for row in attempts["row_attempts"]},
            {"m_csa:78", "m_csa:204", "m_csa:531", "uniprot:P78549", "uniprot:Q3LXA3"},
        )

    def test_fold_augmented_source_sidecar_clearance_preflight_current_counts(
        self,
    ) -> None:
        preflight = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_source_sidecar_clearance_preflight_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            preflight["status"],
            "fold_augmented_source_sidecar_clearance_preflight_candidates_ready_review_only",
        )
        self.assertEqual(preflight["counts"]["remaining_blocker_rows"], 5)
        self.assertEqual(
            preflight["counts"]["source_feature_sidecar_candidate_rows"], 3
        )
        self.assertEqual(preflight["counts"]["coordinate_policy_blocked_rows"], 1)
        self.assertEqual(
            preflight["counts"]["non_residue_interaction_policy_blocked_rows"], 1
        )
        self.assertEqual(preflight["counts"]["deployment_blockers_cleared_now"], 0)
        self.assertEqual(
            preflight["counts"]["source_feature_candidate_entry_ids"],
            ["m_csa:531", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        rows = {row["entry_id"]: row for row in preflight["preflight_rows"]}
        self.assertEqual(rows["m_csa:531"]["source_feature_count"], 3)
        self.assertEqual(rows["uniprot:P78549"]["source_feature_count"], 6)
        self.assertEqual(rows["uniprot:Q3LXA3"]["source_feature_count"], 9)
        self.assertEqual(
            rows["m_csa:204"]["preflight_status"],
            "blocked_non_residue_interaction_policy_required",
        )
        self.assertFalse(preflight["guardrails"]["source_sidecars_created"])

    def test_fold_augmented_source_feature_active_site_sidecar_candidates_current_counts(
        self,
    ) -> None:
        candidates = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_source_feature_active_site_sidecar_candidates_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            candidates["status"],
            "fold_augmented_source_feature_active_site_sidecar_candidates_ready_review_only",
        )
        self.assertEqual(candidates["counts"]["candidate_sidecar_rows"], 3)
        self.assertEqual(candidates["counts"]["draft_rows"], 3)
        self.assertEqual(candidates["counts"]["approved_rows"], 0)
        self.assertEqual(
            candidates["counts"]["total_source_feature_support_rows"], 18
        )
        self.assertEqual(
            candidates["counts"]["candidate_entry_ids"],
            ["m_csa:531", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        rows = {row["entry_id"]: row for row in candidates["sidecar_rows"]}
        self.assertEqual(rows["m_csa:531"]["review_status"], "draft")
        self.assertFalse(rows["uniprot:P78549"]["allowed_for_combined_channel_now"])
        self.assertFalse(candidates["guardrails"]["approved_sidecars_created"])

    def test_fold_augmented_source_feature_active_site_sidecar_candidate_strict_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_source_feature_active_site_sidecar_candidate_"
                "strict_audit_current702_20260602.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "fold_augmented_source_feature_active_site_sidecar_candidate_strict_audit_passed_review_only",
        )
        self.assertEqual(audit["counts"]["candidate_sidecar_rows"], 3)
        self.assertEqual(audit["counts"]["audit_passed_rows"], 3)
        self.assertEqual(audit["counts"]["audit_blocked_rows"], 0)
        self.assertEqual(audit["counts"]["critical_violation_total"], 0)
        self.assertEqual(audit["counts"]["approved_rows"], 0)
        self.assertEqual(audit["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertFalse(audit["guardrails"]["ready_for_predicted_geometry_scoring"])

    def test_fold_augmented_p23007_alternate_accession_scout_current_counts(
        self,
    ) -> None:
        scout = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_p23007_alternate_accession_scout_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            scout["status"],
            "fold_augmented_p23007_alternate_accession_scout_ready_policy_review_only",
        )
        self.assertEqual(scout["counts"]["candidate_alternate_accessions"], 4)
        self.assertEqual(scout["counts"]["candidates_with_afdb"], 4)
        self.assertEqual(scout["counts"]["pattern_compatible_candidates"], 4)
        self.assertEqual(scout["counts"]["replacement_authorized_now"], 0)
        self.assertEqual(scout["counts"]["deployment_blockers_cleared_now"], 0)
        self.assertEqual(
            scout["p23007_reference"]["source_active_site_positions"],
            [274, 320, 375],
        )
        self.assertEqual(
            scout["candidate_alternate_accessions"][0]["accession"], "O75390"
        )
        self.assertFalse(scout["guardrails"]["alternate_accession_authorized"])

    def test_fold_augmented_source_feature_active_site_sidecar_review_gate_current_counts(
        self,
    ) -> None:
        gate = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_source_feature_active_site_sidecar_review_gate_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            gate["status"],
            "fold_augmented_source_feature_active_site_sidecar_review_gate_ready_review_only",
        )
        self.assertEqual(gate["counts"]["candidate_sidecar_rows"], 3)
        self.assertEqual(
            gate["counts"]["manual_approval_review_ready_rows"], 3
        )
        self.assertEqual(gate["counts"]["manual_approval_decisions_required"], 3)
        self.assertEqual(gate["counts"]["strict_audit_passed_rows"], 3)
        self.assertEqual(gate["counts"]["strict_audit_blocked_rows"], 0)
        self.assertEqual(gate["counts"]["approved_rows"], 0)
        self.assertEqual(gate["counts"]["copy_authorized_now"], 0)
        self.assertEqual(
            gate["counts"]["ready_for_predicted_geometry_scoring_now"], 0
        )
        self.assertEqual(gate["counts"]["deployment_blockers_cleared_now"], 0)
        self.assertEqual(gate["counts"]["non_sidecar_policy_rows"], 2)
        self.assertEqual(gate["counts"]["source_feature_support_rows"], 18)
        self.assertEqual(
            gate["counts"]["review_ready_entry_ids"],
            ["m_csa:531", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        rows = {row["entry_id"]: row for row in gate["review_gate_rows"]}
        self.assertTrue(rows["m_csa:531"]["ready_for_manual_approval_review"])
        self.assertIn(
            "rerun_combined_geometry_fold_channel",
            rows["uniprot:P78549"]["blocked_actions_without_approval"],
        )
        self.assertFalse(gate["decision"]["copy_authorized_now"])
        self.assertFalse(gate["guardrails"]["sidecars_approved_or_copied"])

    def test_fold_augmented_p23007_alternate_accession_policy_gate_current_counts(
        self,
    ) -> None:
        gate = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_p23007_alternate_accession_policy_gate_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            gate["status"],
            "fold_augmented_p23007_alternate_accession_policy_gate_ready_review_only",
        )
        self.assertEqual(gate["counts"]["candidate_alternate_accessions"], 4)
        self.assertEqual(gate["counts"]["policy_review_ready_candidates"], 4)
        self.assertEqual(gate["counts"]["candidates_with_afdb"], 4)
        self.assertEqual(gate["counts"]["pattern_compatible_candidates"], 4)
        self.assertEqual(gate["counts"]["replacement_authorized_now"], 0)
        self.assertEqual(gate["counts"]["coordinate_fetch_authorized_now"], 0)
        self.assertEqual(gate["counts"]["deployment_blockers_cleared_now"], 0)
        self.assertEqual(
            gate["counts"]["policy_review_candidate_accessions"],
            ["O75390", "P00889", "Q8VHF5", "Q9CZU6"],
        )
        self.assertIsNone(gate["decision"]["selected_alternate_accession"])
        self.assertFalse(gate["decision"]["replacement_authorized_now"])
        self.assertFalse(gate["guardrails"]["coordinate_fetch_authorized"])
        rows = {row["candidate_accession"]: row for row in gate["candidate_policy_rows"]}
        self.assertTrue(rows["O75390"]["policy_review_ready"])
        self.assertIn(
            "rerun_fold_channel_with_replacement",
            rows["Q9CZU6"]["blocked_actions_without_policy"],
        )

    def test_fold_augmented_blocker_human_decision_application_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_blocker_human_decision_application_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "fold_augmented_blocker_human_decision_application_ready_materialization_pending",
        )
        self.assertEqual(audit["counts"]["approved_source_feature_sidecars"], 3)
        self.assertEqual(
            audit["counts"]["source_feature_sidecars_authorized_for_materialization"],
            3,
        )
        self.assertEqual(audit["counts"]["p23007_replacement_authorized_now"], 1)
        self.assertEqual(
            audit["counts"]["p23007_coordinate_fetch_authorized_now"], 1
        )
        self.assertEqual(audit["counts"]["p10746_keep_fold_only_policy_rows"], 1)
        self.assertEqual(
            audit["counts"]["p10746_non_residue_sidecar_approved_rows"], 0
        )
        self.assertEqual(
            audit["counts"]["human_or_policy_decision_blockers_remaining"], 0
        )
        rows = {
            row["entry_id"]: row
            for row in audit["source_feature_sidecar_decisions"]
            if row["decision"] == "approve_source_feature_sidecar"
        }
        self.assertEqual(
            sorted(rows),
            ["m_csa:531", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(
            audit["p23007_decision"]["selected_alternate_accession"], "P00889"
        )
        self.assertEqual(
            audit["p10746_decision"]["decision"],
            "keep_fold_only_no_non_residue_sidecar",
        )
        self.assertFalse(audit["guardrails"]["sidecars_materialized_now"])
        self.assertFalse(audit["guardrails"]["foldseek_or_tm_rerun_performed"])

    def test_fold_augmented_approved_source_feature_sidecar_materialization_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_approved_source_feature_active_site_sidecar_"
                "materialization_current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "fold_augmented_approved_source_feature_active_site_sidecar_materialization_ready_rerun_pending",
        )
        self.assertEqual(audit["counts"]["approved_decision_rows"], 3)
        self.assertEqual(audit["counts"]["materialized_sidecar_rows"], 3)
        self.assertEqual(audit["counts"]["blocked_materialization_rows"], 0)
        self.assertEqual(audit["counts"]["source_feature_support_rows"], 18)
        self.assertEqual(audit["counts"]["ready_for_predicted_geometry_scoring"], 3)
        self.assertEqual(audit["counts"]["p23007_coordinate_fetch_authorized_now"], 1)
        self.assertEqual(audit["counts"]["p23007_coordinate_fetched_now"], 0)
        self.assertTrue(audit["guardrails"]["approved_sidecar_surface_written"])
        self.assertFalse(audit["guardrails"]["coordinate_fetched_now"])
        self.assertFalse(audit["guardrails"]["combined_channel_rerun_performed"])
        rows = {row["entry_id"]: row for row in audit["materialized_sidecar_rows"]}
        self.assertEqual(
            sorted(rows),
            ["m_csa:531", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(
            rows["m_csa:531"]["review_status"],
            "approved_for_fixed_threshold_rerun",
        )
        self.assertEqual(rows["uniprot:P78549"]["blockers"], ["combined_channel_not_rerun"])

    def test_fold_augmented_p00889_ortholog_coordinate_fetch_manifest_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_p00889_ortholog_coordinate_fetch_manifest_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "fold_augmented_p00889_ortholog_coordinate_fetch_manifest_ready_rerun_pending",
        )
        self.assertEqual(audit["counts"]["coordinate_files_recorded"], 1)
        self.assertEqual(audit["counts"]["p23007_coordinate_fetch_authorized_now"], 1)
        self.assertEqual(audit["counts"]["p23007_coordinate_fetched_now"], 1)
        self.assertEqual(audit["counts"]["approved_source_feature_sidecar_rows"], 3)
        self.assertEqual(audit["counts"]["blocking_conditions"], 0)
        self.assertEqual(
            audit["coordinate_record"]["sha256"],
            "8e41533a17c8c156b4d30640ee99f4d25e5156a1ddb9e0ab8df4e88a6a737b36",
        )
        self.assertTrue(
            audit["decision"]["ready_for_fixed_threshold_combined_rerun"]
        )
        self.assertFalse(audit["guardrails"]["foldseek_or_tm_rerun_performed"])
        self.assertFalse(audit["guardrails"]["combined_channel_rerun_performed"])

    def test_fold_augmented_fixed_threshold_rerun_readiness_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_fixed_threshold_rerun_readiness_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "fold_augmented_fixed_threshold_rerun_readiness_ready",
        )
        self.assertEqual(audit["fixed_threshold"], 0.44155)
        self.assertEqual(
            audit["counts"]["human_or_policy_decision_blockers_remaining"], 0
        )
        self.assertEqual(audit["counts"]["materialized_sidecar_rows"], 3)
        self.assertEqual(audit["counts"]["source_feature_support_rows"], 18)
        self.assertEqual(audit["counts"]["p00889_coordinate_fetched_now"], 1)
        self.assertEqual(audit["counts"]["remaining_pre_rerun_blockers"], 0)
        self.assertEqual(audit["blockers"], [])
        self.assertTrue(
            audit["decision"]["ready_for_fixed_threshold_combined_rerun"]
        )
        self.assertFalse(audit["decision"]["deployment_closed_now"])
        self.assertFalse(audit["guardrails"]["foldseek_or_tm_rerun_performed"])
        self.assertFalse(audit["guardrails"]["combined_channel_rerun_performed"])

    def test_fold_augmented_fixed_threshold_combined_rerun_readout_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_fixed_threshold_combined_rerun_readout_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "fold_augmented_fixed_threshold_combined_rerun_readout_complete_with_caveat",
        )
        self.assertEqual(audit["fixed_threshold"], 0.44155)
        self.assertEqual(audit["counts"]["approved_source_feature_sidecar_rows"], 3)
        self.assertEqual(audit["counts"]["geometry_rows_ok"], 4)
        self.assertEqual(audit["counts"]["source_feature_geometry_rows_ok"], 3)
        self.assertEqual(audit["counts"]["p00889_surrogate_geometry_rows_ok"], 1)
        self.assertEqual(audit["counts"]["fixed_threshold_combined_readout_rows"], 4)
        self.assertEqual(
            audit["counts"]["combined_rows_abstained_at_fixed_threshold"], 2
        )
        self.assertEqual(
            audit["counts"]["combined_rows_retained_at_fixed_threshold"], 2
        )
        self.assertEqual(audit["counts"]["combined_rows_blocked"], 0)
        self.assertEqual(audit["counts"]["fold_only_caveat_rows"], 1)
        self.assertEqual(audit["counts"]["p00889_foldseek_nearest_hits"], 1)
        self.assertEqual(
            audit["decision"]["abstained_entry_ids"],
            ["m_csa:78", "uniprot:P78549"],
        )
        self.assertEqual(
            audit["decision"]["non_abstained_entry_ids"],
            ["m_csa:531", "uniprot:Q3LXA3"],
        )
        rows = {row["entry_id"]: row for row in audit["readout_rows"]}
        self.assertEqual(
            rows["m_csa:78"]["channel_scores"]["combined_mean_geometry_fold"],
            0.4054,
        )
        self.assertTrue(rows["m_csa:78"]["abstains_at_fixed_threshold"])
        self.assertEqual(
            rows["m_csa:531"]["channel_scores"]["combined_mean_geometry_fold"],
            0.4756,
        )
        self.assertFalse(rows["m_csa:531"]["abstains_at_fixed_threshold"])
        self.assertEqual(
            rows["uniprot:P78549"]["channel_scores"]["combined_mean_geometry_fold"],
            0.42485,
        )
        self.assertTrue(rows["uniprot:P78549"]["abstains_at_fixed_threshold"])
        self.assertEqual(
            rows["uniprot:Q3LXA3"]["channel_scores"]["combined_mean_geometry_fold"],
            0.4483,
        )
        self.assertFalse(rows["uniprot:Q3LXA3"]["abstains_at_fixed_threshold"])
        self.assertEqual(
            audit["fold_only_caveat_rows"][0]["status"],
            "fold_only_policy_caveat_not_combined_scored",
        )
        self.assertTrue(
            audit["guardrails"]["p00889_foldseek_or_tm_rerun_performed"]
        )
        self.assertTrue(audit["guardrails"]["combined_channel_rerun_performed"])
        self.assertFalse(audit["guardrails"]["threshold_selected_or_tuned"])
        self.assertFalse(audit["decision"]["deployment_closed_now"])

    def test_fold_augmented_fixed_threshold_combined_rerun_calibration_impact_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_fixed_threshold_combined_rerun_calibration_"
                "impact_current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "fold_augmented_fixed_threshold_combined_rerun_calibration_impact_ready",
        )
        self.assertEqual(audit["fixed_threshold"], 0.44155)
        self.assertEqual(audit["prior_contract_threshold"], 0.44155)
        self.assertEqual(audit["counts"]["candidate_ids_requested"], 76)
        self.assertEqual(audit["counts"]["prior_full_channel_score_rows"], 71)
        self.assertEqual(audit["counts"]["new_combined_readout_rows"], 4)
        self.assertEqual(audit["counts"]["expanded_full_channel_score_rows"], 75)
        self.assertEqual(
            audit["counts"]["remaining_combined_score_blocker_rows"], 1
        )
        self.assertEqual(
            audit["counts"]["prior_oos_abstained_at_fixed_threshold"], 28
        )
        self.assertEqual(
            audit["counts"]["expanded_oos_abstained_at_fixed_threshold"], 30
        )
        self.assertEqual(
            audit["counts"]["expanded_oos_abstain_recall_at_fixed_threshold"],
            0.4,
        )
        self.assertEqual(audit["counts"]["coverage_after_rerun"], 0.986842)
        self.assertEqual(
            audit["remaining_combined_score_blocker_entry_ids"], ["m_csa:204"]
        )
        self.assertTrue(
            audit["decision"]["calibration_surface_expanded_without_heldout"]
        )
        self.assertFalse(audit["guardrails"]["threshold_selected_or_tuned"])
        self.assertFalse(audit["guardrails"]["heldout_rows_read_now"])
        self.assertFalse(audit["decision"]["deployment_closed_now"])

    def test_fold_augmented_expanded_train_cal_oos_negative_surface_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_expanded_train_cal_oos_negative_"
                "surface_scores_current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "computed_partial_expanded_train_cal_oos_negative_surface_scores",
        )
        self.assertEqual(audit["counts"]["candidate_ids_requested"], 76)
        self.assertEqual(audit["counts"]["prior_full_channel_score_rows"], 71)
        self.assertEqual(audit["counts"]["new_combined_readout_rows"], 4)
        self.assertEqual(audit["counts"]["replaced_candidate_rows"], 4)
        self.assertEqual(audit["counts"]["expanded_full_channel_score_rows"], 75)
        self.assertEqual(
            audit["counts"]["candidate_rows_with_full_channel_scores"], 75
        )
        self.assertEqual(audit["counts"]["candidate_predicted_geometry_ok_rows"], 75)
        self.assertEqual(audit["counts"]["foldseek_rows_with_nearest_train_hits"], 76)
        self.assertEqual(
            audit["counts"]["remaining_combined_score_blocker_rows"], 1
        )
        self.assertEqual(audit["counts"]["coverage_after_rerun"], 0.986842)
        self.assertEqual(
            audit["expanded_surface_summary"]["replaced_entry_ids"],
            ["m_csa:78", "m_csa:531", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(
            audit["remaining_combined_score_blocker_entry_ids"], ["m_csa:204"]
        )
        rows = {row["entry_id"]: row for row in audit["candidate_row_scores"]}
        self.assertEqual(
            rows["m_csa:78"]["channel_scores"]["combined_mean_geometry_fold"],
            0.4054,
        )
        self.assertEqual(rows["m_csa:78"]["scoring_accession"], "P00889")
        self.assertEqual(
            rows["m_csa:78"]["predicted_geometry_accession_repair"][
                "original_accession"
            ],
            "P23007",
        )
        self.assertIsNone(rows["m_csa:204"]["channel_scores"])
        self.assertFalse(audit["guardrails"]["threshold_selected_or_tuned"])
        self.assertFalse(audit["guardrails"]["heldout_rows_read_now"])

    def test_fold_augmented_expanded_oos_calibrated_threshold_contract_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_abstention_threshold_contract_"
                "expanded_oos_calibrated_current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["artifact_id"],
            (
                "v3_fold_augmented_abstention_threshold_contract_"
                "expanded_oos_calibrated_current702_20260603"
            ),
        )
        self.assertEqual(
            audit["status"], "computed_oos_calibrated_threshold_contract"
        )
        self.assertEqual(audit["counts"]["calibration_in_scope_rows"], 34)
        self.assertEqual(audit["counts"]["calibration_oos_negative_rows"], 75)
        self.assertEqual(
            audit["counts"]["calibration_oos_negative_candidates_requested"], 76
        )
        self.assertEqual(audit["blockers"], ["train_cal_oos_negative_surface_is_partial"])
        primary = audit["primary_channel_readout"]
        selected = primary[
            "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain"
        ]
        heldout = primary["heldout_final_eval_at_90pct_oos_calibrated_threshold"]
        self.assertEqual(selected["threshold"], 0.44155)
        self.assertEqual(selected["calibration_oos_total"], 75)
        self.assertEqual(selected["calibration_oos_abstained"], 30)
        self.assertEqual(selected["calibration_oos_abstain_recall"], 0.4)
        self.assertEqual(heldout["heldout_confounded_oos_abstained"], 5)
        self.assertEqual(heldout["heldout_confounded_oos_total"], 6)
        self.assertEqual(heldout["heldout_confounded_oos_abstain_recall"], 0.8333)
        self.assertTrue(audit["guardrails"]["heldout_used_for_final_eval_only"])
        self.assertTrue(audit["guardrails"]["train_cal_oos_negatives_used_for_threshold"])

    def test_fold_augmented_post_rerun_deployment_closure_status_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_post_rerun_deployment_closure_status_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "fold_augmented_post_rerun_deployment_closure_status_blocked_p10746_caveat",
        )
        self.assertEqual(audit["fixed_threshold"], 0.44155)
        self.assertEqual(
            audit["counts"]["prior_remaining_production_blocker_rows"], 5
        )
        self.assertEqual(
            audit["counts"]["remaining_combined_score_blocker_rows"], 1
        )
        self.assertEqual(audit["counts"]["expanded_full_channel_score_rows"], 75)
        self.assertEqual(audit["counts"]["candidate_ids_requested"], 76)
        self.assertEqual(audit["counts"]["heldout_confounded_oos_abstained"], 5)
        self.assertEqual(audit["counts"]["heldout_confounded_oos_total"], 6)
        self.assertEqual(
            audit["remaining_blockers"][0]["entry_id"], "m_csa:204"
        )
        self.assertTrue(
            audit["decision"]["research_confounded_operating_point_still_ready"]
        )
        self.assertFalse(audit["decision"]["deployable_without_production_caveat"])
        self.assertFalse(audit["guardrails"]["heldout_rows_read_now"])
        self.assertFalse(audit["guardrails"]["threshold_selected_or_tuned"])
        disposition = {
            row["entry_id"]: row for row in audit["blocker_disposition"]
        }
        self.assertTrue(disposition["m_csa:78"]["abstains_at_fixed_threshold"])
        self.assertFalse(
            disposition["m_csa:531"]["abstains_at_fixed_threshold"]
        )
        self.assertEqual(
            disposition["m_csa:204"]["status"],
            "fold_only_policy_caveat_not_combined_scored",
        )

    def test_fold_augmented_post_rerun_confounded_deployment_closure_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_post_rerun_confounded_deployment_closure_"
                "audit_current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "post_rerun_confounded_fold_channel_research_ready_p10746_caveat",
        )
        self.assertEqual(audit["operating_point"]["fixed_threshold"], 0.44155)
        self.assertEqual(audit["counts"]["priority_confounded_oos_rows"], 6)
        self.assertEqual(audit["counts"]["priority_nearest_hits"], 6)
        self.assertEqual(audit["counts"]["heldout_confounded_oos_abstained"], 5)
        self.assertEqual(audit["counts"]["heldout_confounded_oos_total"], 6)
        self.assertEqual(audit["counts"]["expanded_full_channel_score_rows"], 75)
        self.assertEqual(audit["counts"]["candidate_ids_requested"], 76)
        self.assertEqual(audit["counts"]["remaining_combined_score_blocker_rows"], 1)
        self.assertEqual(audit["counts"]["critical_violation_total"], 1)
        self.assertEqual(
            audit["post_rerun_closure"]["remaining_blocker_rows"][0]["entry_id"],
            "m_csa:204",
        )
        self.assertTrue(
            audit["decision"]["confounded_subset_target_met_for_research"]
        )
        self.assertFalse(audit["decision"]["deployable_without_production_caveat"])
        self.assertFalse(audit["guardrails"]["heldout_rows_read_now"])
        self.assertFalse(audit["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_confounded_proxy_operating_point_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_operating_point_audit_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_operating_point_audit_"
                "current702_20260603"
            ),
        )
        self.assertEqual(
            audit["status"],
            "fold_augmented_confounded_proxy_operating_point_ready_with_proxy_caveat",
        )
        self.assertEqual(audit["fixed_operating_point"]["threshold"], 0.44155)
        self.assertEqual(audit["counts"]["calibration_oos_rows"], 186)
        self.assertEqual(
            audit["counts"]["high_cofactor_proxy_calibration_oos_rows"], 4
        )
        self.assertEqual(
            audit["counts"]["high_cofactor_proxy_abstained_at_fixed_threshold"],
            0,
        )
        self.assertEqual(
            audit["counts"]["same_family_structural_proxy_calibration_oos_rows"],
            55,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["same_family_structural_proxy_abstained_at_fixed_threshold"],
            10,
        )
        self.assertEqual(
            audit["calibration_proxy_readout"][
                "high_cofactor_proxy_calibration_oos"
            ]["abstain_recall"],
            0.0,
        )
        self.assertEqual(
            audit["calibration_proxy_readout"][
                "same_family_structural_proxy_calibration_oos"
            ]["abstain_recall"],
            0.1818,
        )
        self.assertEqual(audit["counts"]["heldout_confounded_oos_abstained"], 5)
        self.assertEqual(audit["counts"]["heldout_confounded_oos_total"], 6)
        self.assertFalse(
            audit["decision"]["calibration_high_cofactor_proxy_target_met"]
        )
        self.assertFalse(
            audit["decision"]["calibration_same_family_structural_proxy_target_met"]
        )
        self.assertTrue(
            audit["decision"][
                "heldout_confounded_operating_point_met_from_existing_readout"
            ]
        )
        self.assertIn(
            "calibration_high_cofactor_proxy_target_not_met",
            audit["blockers"],
        )
        self.assertIn(
            "calibration_same_family_structural_proxy_target_not_met",
            audit["blockers"],
        )
        self.assertFalse(audit["guardrails"]["threshold_selected_or_tuned"])
        self.assertFalse(
            audit["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )

    def test_fold_augmented_confounded_proxy_gap_targets_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_gap_targets_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["artifact_id"],
            "v3_fold_augmented_confounded_proxy_gap_targets_current702_20260603",
        )
        self.assertEqual(
            audit["status"], "fold_augmented_confounded_proxy_gap_targets_ready"
        )
        self.assertEqual(audit["fixed_operating_point"]["threshold"], 0.44155)
        self.assertEqual(audit["counts"]["retained_proxy_gap_rows"], 48)
        self.assertEqual(
            audit["counts"]["high_cofactor_retained_proxy_gap_rows"], 4
        )
        self.assertEqual(
            audit["counts"]["same_family_structural_retained_proxy_gap_rows"],
            45,
        )
        self.assertEqual(
            audit["counts"]["priority_counts"],
            {
                "priority_1_high_cofactor_retained_proxy_gap": 4,
                "priority_2_hard_retained_structural_proxy_gap": 31,
                "priority_3_near_threshold_retained_structural_proxy_gap": 13,
            },
        )
        rows = {row["entry_id"]: row for row in audit["retained_proxy_gap_rows"]}
        self.assertIn("m_csa:368", rows)
        self.assertEqual(
            rows["m_csa:368"]["priority"],
            "priority_1_high_cofactor_retained_proxy_gap",
        )
        self.assertFalse(audit["decision"]["apply_or_change_threshold_now"])
        self.assertFalse(audit["guardrails"]["heldout_rows_read_now"])
        self.assertFalse(
            audit["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )

    def test_fold_augmented_confounded_proxy_threshold_stress_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_threshold_stress_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["artifact_id"],
            "v3_fold_augmented_confounded_proxy_threshold_stress_current702_20260603",
        )
        self.assertEqual(
            audit["status"],
            "fold_augmented_confounded_proxy_threshold_stress_ready",
        )
        self.assertEqual(audit["counts"]["calibration_in_scope_rows"], 34)
        self.assertEqual(audit["counts"]["high_cofactor_proxy_rows"], 4)
        self.assertEqual(audit["counts"]["same_family_structural_proxy_rows"], 55)
        self.assertEqual(audit["counts"]["all_expanded_calibration_oos_rows"], 75)
        high_80 = audit["threshold_stress"]["high_cofactor_signature_proxy"][
            "counterfactual_targets"
        ]["0.8"]
        structural_80 = audit["threshold_stress"]["same_family_structural_proxy"][
            "counterfactual_targets"
        ]["0.8"]
        all_oos_80 = audit["threshold_stress"]["all_expanded_calibration_oos"][
            "counterfactual_targets"
        ]["0.8"]
        self.assertEqual(high_80["threshold"], 0.6399)
        self.assertEqual(high_80["calibration_in_scope_retain_recall"], 0.3529)
        self.assertEqual(structural_80["threshold"], 0.63105)
        self.assertEqual(
            structural_80["calibration_in_scope_retain_recall"], 0.3824
        )
        self.assertEqual(all_oos_80["threshold"], 0.5365)
        self.assertEqual(all_oos_80["calibration_in_scope_retain_recall"], 0.7353)
        self.assertFalse(
            audit["decision"]["structural_proxy_80pct_abstain_retention_ok"]
        )
        self.assertFalse(
            audit["decision"]["high_cofactor_proxy_80pct_abstain_retention_ok"]
        )
        self.assertFalse(audit["decision"]["apply_or_change_threshold_now"])
        self.assertTrue(
            audit["guardrails"]["counterfactual_thresholds_computed_not_applied"]
        )
        self.assertFalse(audit["guardrails"]["heldout_rows_read_now"])

    def test_fold_augmented_confounded_proxy_evidence_extension_plan_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_evidence_extension_plan_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_evidence_extension_plan_"
                "current702_20260603"
            ),
        )
        self.assertEqual(
            audit["status"],
            "fold_augmented_confounded_proxy_evidence_extension_plan_ready",
        )
        self.assertEqual(audit["fixed_operating_point"]["threshold"], 0.44155)
        self.assertEqual(audit["counts"]["retained_proxy_gap_rows"], 48)
        self.assertEqual(audit["counts"]["evidence_request_rows"], 48)
        self.assertEqual(
            audit["counts"]["high_cofactor_min_new_abstained_rows_for_80pct"],
            16,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["same_family_structural_min_new_abstained_rows_for_80pct"],
            170,
        )
        self.assertEqual(
            audit["counts"]["axis_counts"],
            {
                "hard_same_family_structural_counteraxis": 31,
                "high_cofactor_confounded_proxy_extension": 4,
                "near_threshold_same_family_structural_counteraxis": 13,
            },
        )
        self.assertEqual(
            audit["counts"]["current_surface_train_cal_oos_scored_rows"], 186
        )
        self.assertEqual(
            audit["counts"]["current_surface_unused_high_cofactor_rows"], 0
        )
        self.assertEqual(
            audit["counts"][
                "current_surface_additional_same_family_rows_if_loosened"
            ],
            21,
        )
        self.assertEqual(
            audit["counts"]["current_surface_unscored_candidate_rows"], 6
        )
        self.assertEqual(
            audit["current_surface_unscored_candidate_rows"][0]["entry_id"],
            "m_csa:204",
        )
        self.assertEqual(
            audit["current_surface_unscored_candidate_rows"][0]["accession"],
            "P10746",
        )
        self.assertFalse(
            audit["current_surface_pool"][
                "current_surface_can_satisfy_high_cofactor_80pct_without_new_rows"
            ]
        )
        self.assertFalse(
            audit["current_surface_pool"][
                "current_surface_can_satisfy_structural_80pct_by_loosened_membership"
            ]
        )
        self.assertEqual(
            audit["current_surface_pool"][
                "same_family_abstain_recall_without_component_thresholds"
            ],
            0.3289,
        )
        self.assertFalse(audit["decision"]["apply_or_change_threshold_now"])
        self.assertFalse(
            audit["decision"]["evidence_extension_ready_for_threshold_rerun"]
        )
        self.assertFalse(audit["guardrails"]["heldout_rows_read_now"])
        self.assertFalse(
            audit["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )
        self.assertIn(
            "same_family_structural_proxy_needs_170_more_abstained_train_cal_rows_at_fixed_threshold",
            audit["blockers"],
        )
        self.assertIn(
            "current_train_cal_surface_lacks_high_cofactor_proxy_scale",
            audit["blockers"],
        )
        self.assertIn(
            "current_train_cal_surface_cannot_reach_structural_proxy_80pct_by_loosened_membership",
            audit["blockers"],
        )

    def test_fold_augmented_confounded_proxy_acquisition_queue_current_counts(
        self,
    ) -> None:
        queue = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_acquisition_queue_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            queue["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_acquisition_queue_"
                "current702_20260603"
            ),
        )
        self.assertEqual(
            queue["status"],
            "fold_augmented_confounded_proxy_acquisition_queue_blocked",
        )
        self.assertEqual(queue["fixed_operating_point"]["threshold"], 0.44155)
        self.assertEqual(queue["counts"]["evidence_request_rows"], 48)
        self.assertEqual(
            queue["counts"]["existing_retained_gap_queue_rows"], 48
        )
        self.assertEqual(
            queue["counts"]["loose_same_family_current_surface_rows"], 21
        )
        self.assertEqual(
            queue["counts"]["family_panel_acceptance_scenario_rows"], 6
        )
        self.assertEqual(
            queue["counts"]["family_panel_scenario_high_cofactor_axis_rows"], 5
        )
        self.assertEqual(
            queue["counts"]["family_panel_scenario_structural_axis_rows"], 1
        )
        self.assertEqual(
            queue["counts"]["family_panel_scenario_train_cal_oos_eligible_now"],
            0,
        )
        self.assertEqual(
            queue["counts"]["family_panel_scenario_heldout_confounded_rows"], 4
        )
        self.assertEqual(
            queue["counts"]["family_panel_scenario_train_cal_in_scope_or_seed_rows"],
            1,
        )
        self.assertEqual(
            queue["counts"]["family_panel_scenario_not_on_train_cal_manifest_rows"],
            5,
        )
        self.assertEqual(
            queue["counts"]["high_cofactor_shortfall_after_current_scenario"], 16
        )
        self.assertEqual(
            queue["counts"][
                "same_family_structural_shortfall_after_current_scenario"
            ],
            170,
        )
        self.assertEqual(
            queue["counts"]["current_surface_unscored_candidate_rows"], 6
        )
        by_id = {
            row["entry_id"]: row
            for row in queue["family_panel_scenario_calibration_screen"]
        }
        self.assertFalse(
            by_id["m_csa:973"]["train_cal_oos_calibration_eligible_now"]
        )
        self.assertIn(
            "not_train_cal_oos_calibration_row_label_type",
            by_id["m_csa:973"]["non_eligible_reasons"],
        )
        self.assertTrue(by_id["m_csa:30"]["current_heldout_confounded_oos_row"])
        self.assertIn(
            "current_heldout_confounded_oos_row_not_allowed_for_train_cal_calibration",
            by_id["m_csa:30"]["non_eligible_reasons"],
        )
        self.assertIn(
            "family_panel_acceptance_scenario_rows_do_not_close_train_cal_proxy_calibration",
            queue["blockers"],
        )
        self.assertIn(
            "heldout_confounded_scenario_rows_guardrailed",
            queue["blockers"],
        )
        self.assertFalse(queue["decision"]["apply_or_change_threshold_now"])
        self.assertFalse(
            queue["decision"]["proxy_calibration_rerun_ready_now"]
        )
        self.assertFalse(
            queue["guardrails"]["heldout_confounded_rows_counted_as_calibration"]
        )

    def test_fold_augmented_confounded_proxy_train_cal_candidate_pool_current_counts(
        self,
    ) -> None:
        pool = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_candidate_pool_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            pool["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_train_cal_candidate_pool_"
                "current702_20260603"
            ),
        )
        self.assertEqual(
            pool["status"],
            "fold_augmented_confounded_proxy_train_cal_candidate_pool_ready_for_scoring_plan",
        )
        self.assertEqual(pool["counts"]["ready_train_cal_oos_rows"], 353)
        self.assertEqual(
            pool["counts"]["current_scored_train_cal_oos_rows"], 192
        )
        self.assertEqual(
            pool["counts"]["unscored_ready_train_cal_oos_candidate_rows"],
            170,
        )
        self.assertEqual(
            pool["counts"]["high_organic_cofactor_candidate_rows"], 0
        )
        self.assertEqual(
            pool["counts"]["high_inorganic_cofactor_locus_candidate_rows"], 0
        )
        self.assertEqual(
            pool["counts"]["high_cofactor_axis_candidate_rows"], 0
        )
        self.assertEqual(
            pool["counts"]["structural_locus_candidate_rows"], 0
        )
        self.assertEqual(
            pool["counts"]["metal_structural_locus_candidate_rows"], 0
        )
        self.assertEqual(
            pool["counts"]["unsupported_or_missing_geometry_locus_rows"], 9
        )
        self.assertEqual(
            pool["counts"]["priority_bucket_counts"],
            {"3": 170},
        )
        self.assertEqual(pool["counts"]["priority_candidate_rows_emitted"], 80)
        self.assertFalse(
            pool["decision"]["candidate_pool_meets_high_shortfall_by_count"]
        )
        self.assertFalse(
            pool["decision"][
                "candidate_pool_meets_structural_shortfall_by_count"
            ]
        )
        self.assertFalse(pool["decision"]["apply_or_change_threshold_now"])
        self.assertFalse(pool["decision"]["proxy_calibration_rerun_ready_now"])
        self.assertTrue(pool["decision"]["current_proxy_axes_exhausted"])
        self.assertIn(
            "candidate_pool_not_scored_at_fixed_threshold", pool["blockers"]
        )
        first = pool["priority_candidate_rows"][0]
        self.assertEqual(first["entry_id"], "m_csa:288")
        self.assertEqual(first["organic_cofactor_max_class"], "heme")
        self.assertEqual(first["organic_cofactor_max_score"], 0.407563)
        self.assertFalse(
            pool["guardrails"]["heldout_rows_read_for_training_or_threshold_tuning"]
        )
        self.assertFalse(pool["guardrails"]["candidate_rows_scored_now"])

    def test_fold_augmented_confounded_proxy_train_cal_scoring_tranche_plan_current_counts(
        self,
    ) -> None:
        plan = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_scoring_"
                "tranche_plan_current702_20260603.json"
            )
        )

        self.assertEqual(
            plan["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_train_cal_scoring_"
                "tranche_plan_current702_20260603"
            ),
        )
        self.assertEqual(
            plan["status"],
            "fold_augmented_confounded_proxy_train_cal_scoring_tranche_plan_blocked",
        )
        self.assertEqual(plan["counts"]["priority_candidate_rows_available"], 80)
        self.assertEqual(plan["counts"]["tranche_rows"], 0)
        self.assertEqual(
            plan["counts"]["selected_high_cofactor_axis_rows"], 0
        )
        self.assertEqual(plan["counts"]["selected_structural_axis_rows"], 0)
        self.assertEqual(
            plan["counts"]["high_cofactor_shortfall_from_acquisition_queue"], 16
        )
        self.assertEqual(
            plan["counts"]["structural_shortfall_from_acquisition_queue"], 170
        )
        self.assertFalse(
            plan["counts"]["selected_high_rows_meet_shortfall_by_count"]
        )
        self.assertFalse(
            plan["counts"]["selected_structural_rows_meet_shortfall_by_count"]
        )
        self.assertFalse(plan["decision"]["tranche_ready_for_scoring_plan"])
        self.assertFalse(plan["decision"]["score_tranche_now"])
        self.assertFalse(plan["decision"]["apply_or_change_threshold_now"])
        self.assertFalse(plan["decision"]["proxy_calibration_rerun_ready_now"])
        self.assertIn("scoring_tranche_not_run", plan["blockers"])
        self.assertIn(
            "selected_high_cofactor_rows_below_shortfall", plan["blockers"]
        )
        self.assertIn(
            "selected_structural_rows_below_shortfall", plan["blockers"]
        )
        self.assertEqual(plan["scoring_tranche_rows"], [])
        self.assertFalse(
            plan["guardrails"]["heldout_rows_read_for_training_or_threshold_tuning"]
        )
        self.assertFalse(plan["guardrails"]["candidate_rows_scored_now"])

    def test_fold_augmented_confounded_proxy_train_cal_background_axis_blocker_current_counts(
        self,
    ) -> None:
        blocker = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_background_"
                "axis_blocker_current702_20260603.json"
            )
        )

        self.assertEqual(
            blocker["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_train_cal_background_"
                "axis_blocker_current702_20260603"
            ),
        )
        self.assertEqual(
            blocker["status"],
            (
                "fold_augmented_confounded_proxy_train_cal_background_axis_"
                "blocker_complete"
            ),
        )
        self.assertEqual(
            blocker["counts"]["remaining_unscored_ready_train_cal_oos_rows"],
            170,
        )
        self.assertEqual(blocker["counts"]["background_only_rows"], 170)
        self.assertEqual(
            blocker["counts"]["high_cofactor_axis_candidate_rows"], 0
        )
        self.assertEqual(blocker["counts"]["structural_locus_candidate_rows"], 0)
        self.assertEqual(blocker["counts"]["scoring_tranche_rows"], 0)
        self.assertEqual(
            blocker["classification_counts"]["priority_bucket_counts"],
            {"3": 170},
        )
        self.assertTrue(
            blocker["decision"][
                "all_remaining_rows_background_only_current_axes"
            ]
        )
        self.assertFalse(blocker["decision"]["score_background_only_rows_now"])
        self.assertIn(
            "remaining_train_cal_oos_rows_background_only_current_axes",
            blocker["blockers"],
        )
        self.assertEqual(len(blocker["background_only_rows"]), 170)
        self.assertFalse(blocker["guardrails"]["candidate_rows_scored_now"])
        self.assertFalse(
            blocker["guardrails"]["heldout_rows_read_for_training_or_threshold_tuning"]
        )

    def test_fold_augmented_confounded_proxy_train_cal_background_axis_scout_current_counts(
        self,
    ) -> None:
        scout = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_background_"
                "axis_scout_current702_20260603.json"
            )
        )

        self.assertEqual(
            scout["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_train_cal_background_"
                "axis_scout_current702_20260603"
            ),
        )
        self.assertEqual(
            scout["status"],
            "fold_augmented_confounded_proxy_train_cal_background_axis_scout_blocked",
        )
        self.assertEqual(scout["counts"]["background_only_rows"], 170)
        self.assertEqual(scout["counts"]["candidate_axis_tests"], 3)
        self.assertEqual(scout["counts"]["mechanically_ready_axis_tests"], 0)
        self.assertEqual(
            scout["counts"]["unsupported_geometry_rows"], 9
        )
        self.assertFalse(scout["decision"]["new_proxy_axis_ready_to_score_now"])
        self.assertFalse(scout["guardrails"]["new_proxy_axis_registered"])
        self.assertFalse(scout["guardrails"]["candidate_rows_scored_now"])
        self.assertIn(
            "no_pre_registered_new_proxy_axis_contract", scout["blockers"]
        )

    def test_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_contract_current_counts(
        self,
    ) -> None:
        contract = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_new_"
                "proxy_axis_contract_current702_20260603.json"
            )
        )

        self.assertEqual(
            contract["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_train_cal_new_"
                "proxy_axis_contract_current702_20260603"
            ),
        )
        self.assertEqual(
            contract["status"],
            (
                "fold_augmented_confounded_proxy_train_cal_new_proxy_axis_"
                "contract_ready"
            ),
        )
        self.assertEqual(
            contract["selected_proxy_axis"]["axis_id"],
            "active_site_residue_count_10_plus",
        )
        self.assertEqual(
            contract["selected_proxy_axis"]["membership_rule"],
            "active_site_residue_count >= 10",
        )
        self.assertEqual(contract["counts"]["contracted_scoring_rows"], 6)
        self.assertEqual(contract["counts"]["heldout_like_rows"], 0)
        self.assertEqual(contract["counts"]["blockers"], 0)
        self.assertTrue(contract["decision"]["new_proxy_axis_registered"])
        self.assertTrue(contract["decision"]["scoring_tranche_rows_ready_now"])
        self.assertFalse(contract["decision"]["score_contract_tranche_now"])
        self.assertFalse(contract["decision"]["proxy_calibration_rerun_ready_now"])
        self.assertFalse(contract["decision"]["apply_or_change_threshold_now"])
        self.assertFalse(contract["guardrails"]["candidate_rows_scored_now"])
        self.assertFalse(
            contract["guardrails"][
                "heldout_rows_read_for_training_or_threshold_tuning"
            ]
        )
        self.assertEqual(
            [row["entry_id"] for row in contract["scoring_tranche_rows"]],
            [
                "m_csa:89",
                "m_csa:90",
                "m_csa:143",
                "m_csa:253",
                "m_csa:466",
                "m_csa:501",
            ],
        )
        self.assertEqual(
            contract["scoring_tranche_rows"][0][
                "recommended_proxy_axes_after_scoring"
            ],
            [
                "active_site_residue_count_10_plus_proxy",
                "background_train_cal_oos_structural_pool",
            ],
        )

    def test_fold_augmented_confounded_proxy_train_cal_scoring_input_manifest_current_counts(
        self,
    ) -> None:
        manifest = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_scoring_"
                "input_manifest_current702_20260603.json"
            )
        )

        self.assertEqual(
            manifest["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_train_cal_scoring_"
                "input_manifest_current702_20260603"
            ),
        )
        self.assertEqual(
            manifest["status"],
            "confounded_proxy_train_cal_scoring_input_manifest_staged_missing_coordinates",
        )
        self.assertEqual(manifest["counts"]["scoring_tranche_rows"], 0)
        self.assertEqual(
            manifest["counts"]["sequence_manifest_rows_found"], 0
        )
        self.assertEqual(manifest["counts"]["tranche_rows_with_accession"], 0)
        self.assertEqual(manifest["counts"]["unique_query_accessions"], 0)
        self.assertEqual(manifest["counts"]["query_coordinate_requests"], 0)
        self.assertEqual(manifest["counts"]["query_coordinate_files_observed"], 0)
        self.assertEqual(manifest["counts"]["query_coordinate_files_missing"], 0)
        self.assertEqual(
            manifest["counts"]["train_atlas_target_coordinate_files_missing"],
            0,
        )
        self.assertEqual(manifest["counts"]["foldseek_result_tsv_exists"], 1)
        self.assertEqual(manifest["counts"]["foldseek_result_current_query_hits"], 0)
        self.assertIn(
            "scoring_tranche_plan_empty",
            manifest["blockers"],
        )
        self.assertFalse(
            manifest["decision"]["coordinate_manifest_ready_for_fetch"]
        )
        self.assertFalse(
            manifest["decision"]["foldseek_ready_to_run_after_coordinates"]
        )
        self.assertFalse(manifest["decision"]["score_tranche_now"])
        self.assertFalse(
            manifest["decision"]["proxy_calibration_rerun_ready_now"]
        )
        self.assertEqual(
            len(manifest["missing_query_coordinate_manifest"]), 0
        )
        self.assertFalse(
            manifest["guardrails"][
                "heldout_rows_read_for_training_or_threshold_tuning"
            ]
        )
        self.assertFalse(manifest["guardrails"]["coordinate_downloads_performed"])
        self.assertFalse(manifest["guardrails"]["candidate_rows_scored_now"])

    def test_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scoring_input_manifest_current_counts(
        self,
    ) -> None:
        manifest = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_new_"
                "proxy_axis_scoring_input_manifest_current702_20260603.json"
            )
        )

        self.assertEqual(
            manifest["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_"
                "scoring_input_manifest_current702_20260603"
            ),
        )
        self.assertEqual(
            manifest["status"],
            "confounded_proxy_train_cal_scoring_input_manifest_scored_ready_to_parse",
        )
        self.assertEqual(manifest["counts"]["scoring_tranche_rows"], 6)
        self.assertEqual(manifest["counts"]["unique_query_accessions"], 6)
        self.assertEqual(manifest["counts"]["query_coordinate_files_missing"], 0)
        self.assertEqual(
            manifest["counts"]["train_atlas_target_coordinate_files_missing"],
            0,
        )
        self.assertEqual(
            manifest["counts"]["foldseek_result_current_query_hits"], 6
        )
        self.assertEqual(manifest["counts"]["blockers"], 0)
        self.assertFalse(manifest["decision"]["score_tranche_now"])
        self.assertFalse(manifest["decision"]["apply_or_change_threshold_now"])
        self.assertTrue(
            manifest["decision"]["foldseek_ready_to_run_after_coordinates"]
        )

    def test_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scored_extension_current_counts(
        self,
    ) -> None:
        extension = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_new_"
                "proxy_axis_scored_extension_current702_20260603.json"
            )
        )

        self.assertEqual(
            extension["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_"
                "scored_extension_current702_20260603"
            ),
        )
        self.assertEqual(
            extension["status"],
            "confounded_proxy_train_cal_scored_extension_complete",
        )
        self.assertEqual(extension["counts"]["scoring_tranche_rows"], 6)
        self.assertEqual(
            extension["counts"]["candidate_rows_with_full_channel_scores"], 6
        )
        self.assertEqual(extension["counts"]["foldseek_rows_with_nearest_train_hits"], 6)
        self.assertEqual(extension["missing_full_score_entry_ids"], [])
        self.assertEqual(extension["blockers"], [])
        rows = {row["entry_id"]: row for row in extension["candidate_row_scores"]}
        self.assertEqual(
            rows["m_csa:90"]["channel_scores"]["combined_mean_geometry_fold"],
            0.49735,
        )
        self.assertEqual(
            rows["m_csa:501"]["channel_scores"]["combined_mean_geometry_fold"],
            0.601,
        )
        self.assertEqual(
            rows["m_csa:501"]["predicted_geometry_accession_repair"]["policy"],
            "reference_sequence_positions_without_experimental_structure_positions",
        )
        self.assertFalse(
            extension["guardrails"][
                "heldout_rows_read_for_training_or_threshold_tuning"
            ]
        )

    def test_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_extended_surface_current_counts(
        self,
    ) -> None:
        surface = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_"
                "extended_train_cal_oos_surface_current702_20260603.json"
            )
        )

        self.assertEqual(
            surface["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_"
                "extended_train_cal_oos_surface_current702_20260603"
            ),
        )
        self.assertEqual(
            surface["status"],
            "confounded_proxy_extended_train_cal_oos_surface_partial",
        )
        self.assertEqual(surface["counts"]["extended_candidate_rows"], 198)
        self.assertEqual(
            surface["counts"]["candidate_rows_with_full_channel_scores"], 192
        )
        self.assertEqual(surface["counts"]["appended_full_channel_rows"], 6)
        self.assertEqual(
            surface["counts"]["remaining_combined_score_blocker_rows"], 6
        )
        self.assertIn("scored_extension_has_blockers", surface["blockers"])
        self.assertIn(
            "some_extended_train_cal_oos_rows_missing_full_channel_scores",
            surface["blockers"],
        )
        self.assertIn(
            "clear the remaining full-channel score blockers first",
            surface["interpretation"]["next_action"],
        )

    def test_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_fixed_threshold_readout_current_counts(
        self,
    ) -> None:
        readout = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_"
                "fixed_threshold_readout_current702_20260603.json"
            )
        )

        self.assertEqual(
            readout["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_"
                "fixed_threshold_readout_current702_20260603"
            ),
        )
        self.assertEqual(
            readout["status"],
            (
                "fold_augmented_confounded_proxy_train_cal_new_proxy_axis_"
                "fixed_threshold_readout_ready"
            ),
        )
        self.assertEqual(readout["fixed_threshold"], 0.44155)
        self.assertEqual(readout["counts"]["contracted_scored_rows"], 6)
        self.assertEqual(readout["counts"]["full_channel_rows"], 6)
        self.assertEqual(readout["counts"]["abstained_at_fixed_threshold"], 1)
        self.assertEqual(readout["counts"]["retained_at_fixed_threshold"], 5)
        self.assertEqual(readout["counts"]["blockers"], 0)
        self.assertEqual(readout["abstained_entry_ids"], ["m_csa:466"])
        self.assertEqual(
            readout["retained_entry_ids"],
            ["m_csa:89", "m_csa:90", "m_csa:143", "m_csa:253", "m_csa:501"],
        )
        rows = {row["entry_id"]: row for row in readout["readout"]["rows"]}
        self.assertTrue(rows["m_csa:466"]["abstains_at_fixed_threshold"])
        self.assertEqual(rows["m_csa:466"]["threshold_margin"], -0.056)
        self.assertFalse(
            readout["decision"]["global_operating_point_audit_ready_now"]
        )
        self.assertFalse(readout["decision"]["apply_or_change_threshold_now"])
        self.assertFalse(
            readout["guardrails"][
                "heldout_rows_read_for_training_or_threshold_tuning"
            ]
        )

    def test_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_current_counts(
        self,
    ) -> None:
        contract = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_followup_"
                "proxy_axis_contract_current702_20260603.json"
            )
        )
        manifest = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_followup_"
                "proxy_axis_scoring_input_manifest_current702_20260603.json"
            )
        )
        extension = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_followup_"
                "proxy_axis_scored_extension_current702_20260603.json"
            )
        )
        readout = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_followup_"
                "proxy_axis_fixed_threshold_readout_current702_20260603.json"
            )
        )
        surface = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_followup_"
                "proxy_axis_extended_train_cal_oos_surface_current702_20260603.json"
            )
        )
        blocker = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_post_followup_"
                "background_axis_blocker_current702_20260603.json"
            )
        )
        scout = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_post_followup_"
                "background_axis_scout_current702_20260603.json"
            )
        )
        repair_queue = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_post_followup_"
                "unsupported_geometry_repair_queue_current702_20260603.json"
            )
        )
        coordinate_manifest = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_post_followup_"
                "unsupported_geometry_coordinate_acquisition_manifest_"
                "current702_20260603.json"
            )
        )
        locus_scan = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_post_followup_"
                "unsupported_geometry_coordinate_locus_scan_"
                "current702_20260603.json"
            )
        )
        protein_only_preflight = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_post_followup_"
                "protein_only_proxy_design_preflight_current702_20260603.json"
            )
        )
        protein_only_contract = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_post_followup_"
                "protein_only_fold_topology_residual_contract_current702_"
                "20260603.json"
            )
        )
        protein_only_scoring_input = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_post_followup_"
                "protein_only_fold_topology_residual_scoring_input_manifest_"
                "current702_20260603.json"
            )
        )
        protein_only_scored_readout = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_post_followup_"
                "protein_only_fold_topology_residual_scored_readout_"
                "current702_20260603.json"
            )
        )
        protein_only_extended_surface = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_post_followup_"
                "protein_only_fold_topology_residual_extended_train_cal_oos_"
                "surface_current702_20260603.json"
            )
        )

        self.assertEqual(
            contract["selected_proxy_axis"]["axis_id"],
            "organic_score_0_30_to_below_high_axis_threshold",
        )
        self.assertEqual(contract["counts"]["contracted_scoring_rows"], 4)
        self.assertEqual(
            contract["excluded_previously_scored_entry_ids"], ["m_csa:89"]
        )
        self.assertEqual(
            [row["entry_id"] for row in contract["scoring_tranche_rows"]],
            ["m_csa:60", "m_csa:75", "m_csa:214", "m_csa:288"],
        )
        self.assertEqual(
            manifest["status"],
            "confounded_proxy_train_cal_scoring_input_manifest_scored_ready_to_parse",
        )
        self.assertEqual(manifest["counts"]["scoring_tranche_rows"], 4)
        self.assertEqual(manifest["counts"]["foldseek_result_current_query_hits"], 4)
        self.assertEqual(manifest["counts"]["query_coordinate_files_missing"], 0)
        self.assertEqual(extension["counts"]["candidate_rows_with_full_channel_scores"], 4)
        self.assertEqual(extension["blockers"], [])
        rows = {row["entry_id"]: row for row in extension["candidate_row_scores"]}
        self.assertEqual(
            rows["m_csa:288"]["channel_scores"]["combined_mean_geometry_fold"],
            0.41995,
        )
        self.assertEqual(readout["counts"]["abstained_at_fixed_threshold"], 1)
        self.assertEqual(readout["counts"]["retained_at_fixed_threshold"], 3)
        self.assertEqual(readout["abstained_entry_ids"], ["m_csa:288"])
        self.assertEqual(
            surface["counts"]["candidate_rows_with_full_channel_scores"], 196
        )
        self.assertEqual(surface["counts"]["extended_candidate_rows"], 202)
        self.assertEqual(surface["counts"]["appended_full_channel_rows"], 4)
        self.assertEqual(
            surface["counts"]["remaining_combined_score_blocker_rows"], 6
        )
        self.assertEqual(
            surface["extended_surface_summary"]["appended_extension_entry_ids"],
            ["m_csa:60", "m_csa:75", "m_csa:214", "m_csa:288"],
        )
        self.assertEqual(blocker["counts"]["background_only_rows"], 160)
        self.assertEqual(blocker["counts"]["high_cofactor_axis_candidate_rows"], 0)
        self.assertEqual(blocker["counts"]["structural_locus_candidate_rows"], 0)
        self.assertEqual(scout["counts"]["active_site_residue_count_10_plus_rows"], 0)
        self.assertEqual(
            scout["counts"]["organic_score_0_30_to_below_high_axis_rows"], 0
        )
        self.assertEqual(scout["counts"]["unsupported_geometry_rows"], 8)
        self.assertFalse(scout["decision"]["new_proxy_axis_ready_to_score_now"])
        self.assertEqual(
            repair_queue["counts"]["unsupported_geometry_repair_rows"], 8
        )
        self.assertEqual(repair_queue["counts"]["ready_to_score_now_rows"], 0)
        self.assertEqual(repair_queue["counts"]["rows_with_sequence_accession"], 8)
        self.assertEqual(
            repair_queue["counts"]["local_afdb_v6_coordinate_files_observed"], 8
        )
        self.assertEqual(
            repair_queue["counts"]["local_afdb_v6_coordinate_files_missing"], 0
        )
        self.assertEqual(
            [row["entry_id"] for row in repair_queue["repair_rows"]],
            [
                "m_csa:105",
                "m_csa:137",
                "m_csa:318",
                "m_csa:327",
                "m_csa:360",
                "m_csa:610",
                "m_csa:618",
                "m_csa:649",
            ],
        )
        self.assertFalse(
            repair_queue["decision"]["new_proxy_axis_ready_to_score_now"]
        )
        self.assertEqual(
            coordinate_manifest["status"],
            (
                "fold_augmented_confounded_proxy_train_cal_unsupported_geometry_"
                "coordinate_acquisition_manifest_ready_for_locus_repair_audit"
            ),
        )
        self.assertEqual(coordinate_manifest["counts"]["repair_rows"], 8)
        self.assertEqual(
            coordinate_manifest["counts"]["query_coordinate_files_observed"], 8
        )
        self.assertEqual(
            coordinate_manifest["counts"]["query_coordinate_files_missing"], 0
        )
        self.assertEqual(
            coordinate_manifest["blockers"],
            ["locus_repair_audit_not_rerun_after_coordinate_materialization"],
        )
        self.assertTrue(
            coordinate_manifest["decision"]["ready_for_locus_repair_audit"]
        )
        self.assertFalse(
            coordinate_manifest["decision"]["score_repair_rows_now"]
        )
        self.assertFalse(
            coordinate_manifest["decision"]["new_proxy_axis_ready_to_score_now"]
        )
        self.assertEqual(
            locus_scan["status"],
            (
                "fold_augmented_confounded_proxy_train_cal_unsupported_geometry_"
                "coordinate_locus_scan_protein_only_no_locus_evidence"
            ),
        )
        self.assertEqual(locus_scan["counts"]["coordinate_files_scanned"], 8)
        self.assertEqual(locus_scan["counts"]["coordinate_files_missing"], 0)
        self.assertEqual(
            locus_scan["counts"]["protein_only_afdb_coordinate_files"], 8
        )
        self.assertEqual(locus_scan["counts"]["files_with_hetatm_rows"], 0)
        self.assertEqual(
            locus_scan["counts"][
                "files_with_source_free_inorganic_locus_evidence"
            ],
            0,
        )
        self.assertEqual(
            locus_scan["blockers"],
            [
                "afdb_predicted_coordinates_do_not_carry_ligands_or_metals",
                "inorganic_locus_statuses_still_unsupported",
            ],
        )
        self.assertFalse(
            locus_scan["decision"][
                "background_scout_rerun_can_create_structural_axis_now"
            ]
        )
        self.assertEqual(
            protein_only_preflight["status"],
            (
                "fold_augmented_confounded_proxy_train_cal_protein_only_"
                "proxy_design_preflight_ready_contract_selection"
            ),
        )
        self.assertEqual(
            protein_only_preflight["counts"]["unsupported_geometry_repair_rows"], 8
        )
        self.assertEqual(
            protein_only_preflight["counts"]["protein_only_afdb_coordinate_files"], 8
        )
        self.assertEqual(
            protein_only_preflight["counts"][
                "files_with_source_free_inorganic_locus_evidence"
            ],
            0,
        )
        self.assertEqual(
            protein_only_preflight["counts"]["design_contract_candidate_options"], 2
        )
        self.assertEqual(
            protein_only_preflight["counts"]["ready_to_score_now_rows"], 0
        )
        self.assertTrue(
            protein_only_preflight["decision"][
                "design_preflight_ready_for_contract_selection"
            ]
        )
        self.assertEqual(
            protein_only_preflight["decision"]["preferred_next_axis_id"],
            "protein_only_fold_topology_residual",
        )
        self.assertFalse(protein_only_preflight["decision"]["score_any_rows_now"])
        self.assertFalse(
            protein_only_preflight["decision"]["register_new_proxy_axis_now"]
        )
        self.assertTrue(protein_only_preflight["guardrails"]["design_only"])
        self.assertFalse(protein_only_preflight["guardrails"]["rows_scored_now"])
        self.assertFalse(
            protein_only_preflight["guardrails"]["new_proxy_axis_registered"]
        )
        self.assertEqual(
            protein_only_contract["status"],
            (
                "fold_augmented_confounded_proxy_train_cal_protein_only_"
                "fold_topology_residual_contract_ready"
            ),
        )
        self.assertEqual(
            protein_only_contract["selected_axis"]["axis_id"],
            "protein_only_fold_topology_residual",
        )
        self.assertEqual(protein_only_contract["counts"]["contract_rows"], 8)
        self.assertEqual(
            protein_only_contract["counts"]["query_coordinate_files_observed"], 8
        )
        self.assertEqual(
            protein_only_contract["counts"]["query_coordinate_files_missing"], 0
        )
        self.assertEqual(
            protein_only_contract["counts"][
                "ready_to_build_scoring_input_manifest_rows"
            ],
            8,
        )
        self.assertEqual(
            protein_only_contract["counts"]["ready_to_score_now_rows"], 0
        )
        self.assertEqual(protein_only_contract["blockers"], [])
        self.assertTrue(
            protein_only_contract["decision"]["contract_pre_registered"]
        )
        self.assertTrue(
            protein_only_contract["decision"]["build_scoring_input_manifest_next"]
        )
        self.assertFalse(
            protein_only_contract["decision"]["score_contract_rows_now"]
        )
        self.assertFalse(
            protein_only_contract["decision"]["register_deployable_axis_now"]
        )
        self.assertEqual(
            sorted(row["entry_id"] for row in protein_only_contract["contract_rows"]),
            [
                "m_csa:105",
                "m_csa:137",
                "m_csa:318",
                "m_csa:327",
                "m_csa:360",
                "m_csa:610",
                "m_csa:618",
                "m_csa:649",
            ],
        )
        forbidden_features = set(
            protein_only_contract["feature_contract"]["forbidden_predictive_features"]
        )
        self.assertIn("nearest-hit entry IDs", forbidden_features)
        self.assertIn("nearest-hit target names", forbidden_features)
        self.assertIn("curated labels or family names", forbidden_features)
        self.assertIn("heldout M-CSA rows", forbidden_features)
        self.assertTrue(protein_only_contract["guardrails"]["contract_only"])
        self.assertFalse(protein_only_contract["guardrails"]["rows_scored_now"])
        self.assertFalse(
            protein_only_contract["guardrails"]["deployable_axis_registered"]
        )
        self.assertEqual(
            protein_only_scoring_input["status"],
            "confounded_proxy_train_cal_scoring_input_manifest_scored_ready_to_parse",
        )
        self.assertEqual(
            protein_only_scoring_input["counts"]["scoring_tranche_rows"], 8
        )
        self.assertEqual(
            protein_only_scoring_input["counts"]["query_coordinate_files_missing"],
            0,
        )
        self.assertEqual(
            protein_only_scoring_input["counts"][
                "train_atlas_target_coordinate_files_missing"
            ],
            0,
        )
        self.assertEqual(
            protein_only_scoring_input["counts"][
                "foldseek_result_current_query_hits"
            ],
            8,
        )
        self.assertEqual(protein_only_scoring_input["blockers"], [])
        self.assertEqual(
            protein_only_scoring_input["existing_foldseek_parse_summary"][
                "mapped_pair_count"
            ],
            580,
        )
        self.assertEqual(
            protein_only_scoring_input["existing_foldseek_parse_summary"][
                "min_nearest_atlas_tm_score"
            ],
            0.3715,
        )
        self.assertEqual(
            protein_only_scoring_input["existing_foldseek_parse_summary"][
                "max_nearest_atlas_tm_score"
            ],
            0.7752,
        )
        self.assertFalse(
            protein_only_scoring_input["guardrails"]["heldout_rows_read_for_training_or_threshold_tuning"]
        )
        protein_only_tsv = (
            ROOT
            / "artifacts"
            / "v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results"
            / "protein_only_fold_topology_residual_vs_train_atlas.tsv"
        )
        with protein_only_tsv.open() as handle:
            self.assertEqual(sum(1 for _ in handle), 580)
        self.assertEqual(
            protein_only_scored_readout["status"],
            "confounded_proxy_train_cal_scored_extension_complete",
        )
        self.assertEqual(
            protein_only_scored_readout["counts"]["scoring_tranche_rows"], 8
        )
        self.assertEqual(
            protein_only_scored_readout["counts"][
                "foldseek_rows_with_nearest_train_hits"
            ],
            8,
        )
        self.assertEqual(
            protein_only_scored_readout["counts"][
                "candidate_rows_with_full_channel_scores"
            ],
            8,
        )
        self.assertEqual(
            protein_only_scored_readout["counts"]["missing_full_score_rows"], 0
        )
        self.assertEqual(
            protein_only_scored_readout["blockers"],
            ["some_tranche_rows_missing_predicted_geometry"],
        )
        scored_rows = {
            row["entry_id"]: row
            for row in protein_only_scored_readout["candidate_row_scores"]
        }
        self.assertEqual(
            scored_rows["m_csa:360"][
                "predicted_structure_fold_channel"
            ]["nearest_train_atlas_tm_score"],
            0.7752,
        )
        self.assertEqual(
            scored_rows["m_csa:360"]["channel_scores"][
                "combined_mean_geometry_fold"
            ],
            0.5407,
        )
        self.assertFalse(
            protein_only_scored_readout["guardrails"][
                "heldout_rows_read_for_training_or_threshold_tuning"
            ]
        )
        self.assertFalse(
            protein_only_scored_readout["guardrails"]["threshold_selected_or_tuned"]
        )
        self.assertEqual(
            protein_only_extended_surface["status"],
            "confounded_proxy_extended_train_cal_oos_surface_partial",
        )
        self.assertEqual(
            protein_only_extended_surface["counts"]["appended_full_channel_rows"], 8
        )
        self.assertEqual(
            protein_only_extended_surface["counts"]["candidate_rows_with_full_channel_scores"],
            204,
        )
        self.assertEqual(
            protein_only_extended_surface["counts"]["extended_candidate_rows"], 210
        )
        self.assertEqual(
            protein_only_extended_surface["counts"]["remaining_combined_score_blocker_rows"],
            6,
        )
        self.assertEqual(
            protein_only_extended_surface["blockers"],
            [
                "remaining_fold_only_policy_caveat_not_combined_scored",
                "scored_extension_has_blockers",
                "some_extended_train_cal_oos_rows_missing_full_channel_scores",
            ],
        )
        self.assertFalse(
            protein_only_extended_surface["guardrails"][
                "heldout_rows_read_now"
            ]
        )
        self.assertFalse(
            protein_only_extended_surface["guardrails"][
                "threshold_selected_or_tuned"
            ]
        )

    def test_fold_augmented_confounded_proxy_deployment_validity_blocker_packet_current_counts(
        self,
    ) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_deployment_validity_"
                "blocker_packet_current702_20260604.json"
            )
        )

        self.assertEqual(
            packet["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_deployment_validity_"
                "blocker_packet_current702_20260604"
            ),
        )
        self.assertEqual(
            packet["status"],
            (
                "fold_augmented_confounded_proxy_deployment_validity_"
                "blocker_packet_blocked"
            ),
        )
        self.assertEqual(packet["fixed_operating_point"]["threshold"], 0.44155)
        self.assertEqual(packet["counts"]["retained_proxy_gap_rows"], 48)
        self.assertEqual(packet["counts"]["high_cofactor_proxy_rows"], 4)
        self.assertEqual(
            packet["counts"]["high_cofactor_proxy_abstained_at_fixed_threshold"],
            0,
        )
        self.assertEqual(
            packet["counts"]["high_cofactor_min_new_abstained_rows_for_80pct"],
            16,
        )
        self.assertEqual(packet["counts"]["same_family_structural_proxy_rows"], 55)
        self.assertEqual(
            packet["counts"][
                "same_family_structural_proxy_abstained_at_fixed_threshold"
            ],
            10,
        )
        self.assertEqual(
            packet["counts"][
                "same_family_structural_min_new_abstained_rows_for_80pct"
            ],
            170,
        )
        self.assertEqual(packet["counts"]["family_panel_train_cal_oos_eligible_now"], 0)
        self.assertEqual(
            packet["counts"]["heldout_confounded_scenario_rows_guarded"], 4
        )
        self.assertEqual(packet["counts"]["protein_only_rows_scored"], 8)
        self.assertEqual(
            packet["counts"]["protein_only_rows_abstained_at_fixed_threshold"], 7
        )
        self.assertEqual(
            packet["counts"]["protein_only_rows_retained_at_fixed_threshold"], 1
        )
        self.assertEqual(
            packet["counts"]["protein_only_extended_full_channel_rows"], 204
        )
        self.assertEqual(
            packet["counts"]["protein_only_extended_candidate_rows"], 210
        )
        self.assertEqual(packet["counts"]["remaining_combined_score_blocker_rows"], 6)
        self.assertEqual(
            packet["counts"]["remaining_combined_score_mechanically_clearable_now_rows"],
            0,
        )
        self.assertEqual(packet["counts"]["policy_decision_required_rows"], 1)
        self.assertEqual(packet["counts"]["predicted_structure_unavailable_rows"], 4)
        self.assertEqual(packet["counts"]["approved_geometry_feature_missing_rows"], 1)
        self.assertFalse(packet["decision"]["deployment_closure_valid_now"])
        self.assertFalse(
            packet["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(packet["decision"]["apply_or_change_threshold_now"])
        self.assertFalse(
            packet["decision"][
                "current_evidence_can_solve_confounded_safe_calibration"
            ]
        )
        self.assertTrue(packet["guardrails"]["source_free_evidence_only"])
        self.assertFalse(packet["guardrails"]["threshold_values_changed"])
        self.assertFalse(packet["guardrails"]["fixed_threshold_audit_rerun"])
        self.assertFalse(packet["guardrails"]["candidate_rows_scored_now"])
        self.assertEqual(
            sorted(
                row["entry_id"]
                for row in packet["affected_rows"][
                    "remaining_combined_score_blocker_rows"
                ]
            ),
            [
                "m_csa:204",
                "m_csa:416",
                "m_csa:562",
                "m_csa:586",
                "m_csa:604",
                "m_csa:637",
            ],
        )
        blocker_by_id = {
            row["entry_id"]: row
            for row in packet["affected_rows"][
                "remaining_combined_score_blocker_rows"
            ]
        }
        self.assertEqual(
            blocker_by_id["m_csa:204"]["missing_evidence_type"],
            "explicit deployment caveat decision or approved non-residue sidecar",
        )
        self.assertEqual(
            blocker_by_id["m_csa:416"]["missing_evidence_type"],
            "approved deployment-valid predicted-structure coordinate source",
        )
        experiments = {
            row["experiment_id"]: row for row in packet["smallest_next_experiments"]
        }
        self.assertIn(
            "sixteen_row_high_cofactor_train_cal_oos_probe", experiments
        )
        self.assertFalse(
            experiments["sixteen_row_high_cofactor_train_cal_oos_probe"][
                "sufficient_for_deployment_closure"
            ]
        )
        self.assertFalse(
            experiments[
                "one_hundred_seventy_row_same_family_structural_acquisition"
            ]["sufficient_for_deployment_closure"]
        )
        self.assertIn(
            "threshold_stress_retention_cost_blocks_threshold_raise",
            packet["blockers"],
        )
        self.assertIn(
            "protein_only_extended_surface_still_partial", packet["blockers"]
        )

    def test_fold_augmented_confounded_proxy_current_unavailable_coordinate_reprobe_counts(
        self,
    ) -> None:
        reprobe = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_current_unavailable_"
                "coordinate_reprobe_current702_20260604.json"
            )
        )

        self.assertEqual(
            reprobe["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_current_unavailable_"
                "coordinate_reprobe_current702_20260604"
            ),
        )
        self.assertEqual(
            reprobe["status"],
            (
                "fold_augmented_confounded_proxy_current_unavailable_"
                "coordinate_reprobe_no_rows_cleared"
            ),
        )
        self.assertEqual(reprobe["counts"]["probe_rows"], 4)
        self.assertEqual(reprobe["counts"]["afdb_v6_coordinate_available_rows"], 0)
        self.assertEqual(reprobe["counts"]["afdb_v6_coordinate_unavailable_rows"], 4)
        self.assertEqual(reprobe["counts"]["fixed_threshold_audit_cleared_rows"], 0)
        self.assertEqual(reprobe["counts"]["uniprot_records_with_alphafolddb_xref"], 0)
        self.assertEqual(
            reprobe["counts"]["uniprot_records_with_secondary_accessions"], 3
        )
        self.assertEqual(reprobe["counts"]["secondary_accession_probe_count"], 6)
        self.assertEqual(
            reprobe["counts"]["secondary_accession_afdb_v6_available_rows"], 0
        )
        self.assertFalse(reprobe["decision"]["coordinate_import_authorized_now"])
        self.assertFalse(
            reprobe["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(reprobe["guardrails"]["coordinate_downloads_performed"])
        self.assertFalse(reprobe["guardrails"]["coordinates_imported_or_cached"])
        self.assertFalse(reprobe["guardrails"]["threshold_values_changed"])
        self.assertEqual(
            sorted(row["entry_id"] for row in reprobe["rows"]),
            ["m_csa:416", "m_csa:562", "m_csa:586", "m_csa:637"],
        )
        self.assertEqual(
            {row["http_status"] for row in reprobe["rows"]},
            {404},
        )
        self.assertEqual(
            {
                tuple(row["uniprot_current_record_probe"]["alphafold_db_cross_references"])
                for row in reprobe["rows"]
            },
            {()},
        )
        secondary_statuses = {
            status
            for row in reprobe["rows"]
            for status in row["uniprot_current_record_probe"][
                "secondary_accession_afdb_v6_statuses"
            ].values()
        }
        self.assertEqual(secondary_statuses, {404})
        self.assertIn(
            "four_current_remaining_rows_still_afdb_v6_unavailable",
            reprobe["blockers"],
        )

    def test_fold_augmented_confounded_proxy_high_cofactor_probe_contract_counts(
        self,
    ) -> None:
        contract = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_high_cofactor_probe_"
                "contract_current702_20260604.json"
            )
        )

        self.assertEqual(
            contract["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_high_cofactor_probe_"
                "contract_current702_20260604"
            ),
        )
        self.assertEqual(
            contract["status"],
            (
                "fold_augmented_confounded_proxy_high_cofactor_probe_"
                "contract_ready_for_candidate_acquisition"
            ),
        )
        self.assertEqual(contract["counts"]["fixed_threshold"], 0.44155)
        self.assertEqual(contract["counts"]["probe_target_new_rows"], 16)
        self.assertEqual(contract["counts"]["candidate_rows_registered_now"], 0)
        self.assertEqual(contract["counts"]["current_high_cofactor_proxy_rows"], 4)
        self.assertEqual(
            contract["counts"][
                "current_high_cofactor_proxy_abstained_at_fixed_threshold"
            ],
            0,
        )
        self.assertEqual(
            contract["counts"]["minimum_new_abstained_rows_for_80pct"], 16
        )
        self.assertEqual(
            contract["counts"][
                "structural_proxy_minimum_new_abstained_rows_for_80pct"
            ],
            170,
        )
        self.assertFalse(contract["decision"]["candidate_rows_ready_to_score_now"])
        self.assertFalse(
            contract["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(contract["decision"]["deployable_closure_after_probe_alone"])
        self.assertFalse(contract["decision"]["apply_or_change_threshold_now"])
        self.assertTrue(contract["guardrails"]["train_cal_only"])
        self.assertFalse(contract["guardrails"]["heldout_rows_allowed"])
        self.assertFalse(contract["guardrails"]["threshold_values_changed"])
        self.assertFalse(contract["guardrails"]["candidate_rows_scored_now"])
        self.assertEqual(
            contract["excluded_rows"]["current_high_cofactor_retained_gap_rows"],
            ["m_csa:289", "m_csa:298", "m_csa:361", "m_csa:368"],
        )
        self.assertEqual(
            contract["excluded_rows"][
                "heldout_confounded_or_not_train_cal_rows_not_allowed_for_probe"
            ],
            ["m_csa:30", "m_csa:31", "m_csa:191", "m_csa:448", "m_csa:973"],
        )
        self.assertIn(
            "All 16 newly acquired train/cal high-cofactor proxy rows abstain",
            contract["membership_contract"]["pass_fail_rule"]["pass_condition"],
        )
        self.assertIn(
            "structural_proxy_shortfall_remains_after_this_probe",
            contract["blockers"],
        )

    def test_fold_augmented_confounded_proxy_same_family_structural_acquisition_contract_counts(
        self,
    ) -> None:
        contract = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_same_family_structural_"
                "acquisition_contract_current702_20260604.json"
            )
        )

        self.assertEqual(
            contract["artifact_id"],
            (
                "v3_fold_augmented_confounded_proxy_same_family_structural_"
                "acquisition_contract_current702_20260604"
            ),
        )
        self.assertEqual(
            contract["status"],
            (
                "fold_augmented_confounded_proxy_same_family_structural_"
                "acquisition_contract_ready_for_candidate_acquisition"
            ),
        )
        self.assertEqual(contract["counts"]["fixed_threshold"], 0.44155)
        self.assertEqual(
            contract["counts"]["current_same_family_structural_proxy_rows"], 55
        )
        self.assertEqual(
            contract["counts"][
                "current_same_family_structural_proxy_abstained_at_fixed_threshold"
            ],
            10,
        )
        self.assertEqual(
            contract["counts"]["minimum_new_abstained_rows_for_80pct"], 170
        )
        self.assertEqual(contract["counts"]["probe_target_new_rows"], 170)
        self.assertEqual(
            contract["counts"]["loose_same_family_current_surface_rows"], 21
        )
        self.assertEqual(
            contract["counts"]["loose_same_family_if_included_rows"], 76
        )
        self.assertEqual(
            contract["counts"]["loose_same_family_if_included_abstained_rows"], 25
        )
        self.assertEqual(
            contract["counts"]["high_cofactor_minimum_new_abstained_rows_for_80pct"],
            16,
        )
        self.assertFalse(contract["decision"]["candidate_rows_ready_to_score_now"])
        self.assertFalse(
            contract["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(
            contract["decision"]["deployable_closure_after_contract_alone"]
        )
        self.assertTrue(contract["guardrails"]["train_cal_only"])
        self.assertFalse(contract["guardrails"]["heldout_rows_allowed"])
        self.assertFalse(contract["guardrails"]["threshold_values_changed"])
        self.assertFalse(contract["guardrails"]["candidate_rows_scored_now"])
        self.assertIn(
            "scale_experiment_large_170_row_lower_bound",
            contract["blockers"],
        )
        self.assertIn(
            "high_cofactor_probe_still_separate",
            contract["blockers"],
        )

    def test_fold_augmented_confounded_proxy_scored_extension_surfaces_current_counts(
        self,
    ) -> None:
        first = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_scored_"
                "extension_current702_20260603.json"
            )
        )
        second = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_train_cal_scored_"
                "extension_tranche2_current702_20260603.json"
            )
        )
        after_tranche1 = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_extended_train_cal_oos_"
                "surface_after_tranche1_current702_20260603.json"
            )
        )
        current = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_extended_train_cal_oos_"
                "surface_current702_20260603.json"
            )
        )

        self.assertEqual(first["counts"]["scoring_tranche_rows"], 50)
        self.assertEqual(first["counts"]["candidate_rows_with_full_channel_scores"], 47)
        self.assertEqual(
            first["missing_full_score_entry_ids"],
            ["m_csa:416", "m_csa:562", "m_csa:604"],
        )
        self.assertEqual(second["counts"]["scoring_tranche_rows"], 66)
        self.assertEqual(second["counts"]["candidate_rows_with_full_channel_scores"], 64)
        self.assertEqual(
            second["missing_full_score_entry_ids"], ["m_csa:586", "m_csa:637"]
        )
        self.assertEqual(after_tranche1["counts"]["extended_candidate_rows"], 126)
        self.assertEqual(
            after_tranche1["counts"]["candidate_rows_with_full_channel_scores"], 122
        )
        self.assertEqual(current["counts"]["extended_candidate_rows"], 192)
        self.assertEqual(
            current["counts"]["candidate_rows_with_full_channel_scores"], 186
        )
        self.assertEqual(current["counts"]["scored_extension_appended_rows"], 66)
        self.assertEqual(
            current["remaining_combined_score_blocker_entry_ids"],
            [
                "m_csa:204",
                "m_csa:416",
                "m_csa:562",
                "m_csa:586",
                "m_csa:604",
                "m_csa:637",
            ],
        )
        self.assertFalse(current["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_p10746_source_feature_refresh_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_p10746_source_feature_refresh_audit_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "p10746_source_feature_refresh_no_eligible_features",
        )
        self.assertEqual(audit["source_record"]["http_status"], 200)
        self.assertEqual(audit["feature_audit"]["features_total"], 63)
        self.assertEqual(audit["feature_audit"]["eligible_source_feature_count"], 0)
        self.assertFalse(
            audit["decision"]["p10746_source_features_available_for_sidecar_review"]
        )
        self.assertFalse(audit["decision"]["deployment_caveat_cleared_now"])
        self.assertFalse(audit["guardrails"]["sidecars_created_or_copied"])
        self.assertFalse(audit["guardrails"]["heldout_rows_read_now"])
        self.assertFalse(audit["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_p10746_deployment_caveat_decision_packet_current_counts(
        self,
    ) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_p10746_deployment_caveat_decision_packet_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            packet["status"],
            "p10746_deployment_caveat_decision_packet_ready_review_only",
        )
        self.assertEqual(packet["counts"]["decision_stub_rows"], 1)
        self.assertEqual(packet["counts"]["p10746_post_rerun_blocker_rows"], 1)
        self.assertEqual(packet["counts"]["eligible_source_feature_count"], 0)
        self.assertEqual(packet["counts"]["non_residue_policy_approved_rows"], 0)
        self.assertEqual(packet["counts"]["fold_only_contract_authorized"], 0)
        self.assertEqual(packet["counts"]["blockers"], 0)
        self.assertEqual(packet["counts"]["heldout_confounded_oos_abstained"], 5)
        self.assertEqual(packet["counts"]["heldout_confounded_oos_total"], 6)
        self.assertTrue(packet["decision"]["ready_for_explicit_policy_decision"])
        self.assertFalse(packet["decision"]["p10746_fold_only_caveat_accepted_now"])
        self.assertFalse(packet["decision"]["deployment_closed_now"])
        stub = packet["decision_stubs"][0]
        self.assertEqual(stub["entry_id"], "m_csa:204")
        self.assertEqual(stub["accession"], "P10746")
        self.assertEqual(stub["review_status"], "pending_explicit_decision")
        self.assertEqual(stub["decision_field_to_update"], "decision")
        self.assertEqual(stub["review_status_field_to_update"], "review_status")
        self.assertEqual(
            stub["required_review_status_after_decision"],
            "reviewed_explicit_decision",
        )
        self.assertIn(
            "explicit_accept_p10746_fold_only_deployment_caveat",
            stub["allowed_decisions"],
        )
        self.assertIn(
            "reject_p10746_caveat_require_approved_non_residue_sidecar",
            stub["allowed_decisions"],
        )
        self.assertFalse(packet["guardrails"]["deployment_closed_now"])
        self.assertFalse(packet["guardrails"]["heldout_rows_read_now"])

    def test_fold_augmented_p10746_deployment_caveat_decision_application_current_counts(
        self,
    ) -> None:
        application = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_p10746_deployment_caveat_decision_"
                "application_current702_20260603.json"
            )
        )

        self.assertEqual(
            application["status"],
            "p10746_deployment_caveat_decision_application_blocked_pending_explicit_decision",
        )
        self.assertEqual(application["counts"]["source_decision_stub_rows"], 1)
        self.assertEqual(application["counts"]["decision_rows_checked"], 1)
        self.assertEqual(application["counts"]["reviewed_decision_rows"], 0)
        self.assertEqual(application["counts"]["accepted_p10746_caveat_rows"], 0)
        self.assertEqual(application["counts"]["pending_decision_rows"], 1)
        self.assertEqual(application["counts"]["invalid_decision_rows"], 0)
        self.assertIn(
            "explicit_p10746_caveat_decision_missing",
            application["blockers"],
        )
        self.assertEqual(
            application["application_rows"][0]["entry_id"], "m_csa:204"
        )
        self.assertTrue(
            application["application_rows"][0][
                "decision_context_sha256_matches_source"
            ]
        )
        self.assertFalse(
            application["decision"]["p10746_fold_only_caveat_accepted_now"]
        )
        self.assertFalse(
            application["decision"]["ready_for_deployment_closure_application"]
        )
        self.assertFalse(application["guardrails"]["deployment_closed_now"])
        self.assertFalse(application["guardrails"]["heldout_rows_read_now"])

    def test_fold_augmented_p10746_prior_human_decision_and_impact_counts(
        self,
    ) -> None:
        reviewed = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_p10746_prior_human_decision_"
                "reviewed_stub_current702_20260604.json"
            )
        )
        application = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_p10746_deployment_caveat_decision_"
                "application_prior_human_current702_20260604.json"
            )
        )
        impact = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_p10746_decision_"
                "impact_current702_20260604.json"
            )
        )

        self.assertEqual(
            reviewed["status"], "p10746_prior_human_decision_reviewed_stub_ready"
        )
        self.assertEqual(reviewed["counts"]["reviewed_decision_stub_rows"], 1)
        self.assertEqual(reviewed["counts"]["accepted_p10746_caveat_rows"], 1)
        self.assertEqual(reviewed["counts"]["blockers"], 0)
        self.assertEqual(
            reviewed["reviewed_decision_stubs"][0]["decision"],
            "explicit_accept_p10746_fold_only_deployment_caveat",
        )
        self.assertEqual(
            reviewed["reviewed_decision_stubs"][0]["review_status"],
            "reviewed_explicit_decision",
        )
        self.assertFalse(reviewed["guardrails"]["deployment_closed_now"])
        self.assertFalse(reviewed["guardrails"]["threshold_selected_or_tuned"])

        self.assertEqual(
            application["artifact_id"],
            (
                "v3_fold_augmented_p10746_deployment_caveat_decision_"
                "application_prior_human_current702_20260604"
            ),
        )
        self.assertEqual(
            application["status"],
            "p10746_deployment_caveat_decision_application_accepted_review_only",
        )
        self.assertEqual(application["counts"]["reviewed_decision_rows"], 1)
        self.assertEqual(application["counts"]["accepted_p10746_caveat_rows"], 1)
        self.assertEqual(application["counts"]["pending_decision_rows"], 0)
        self.assertTrue(
            application["decision"]["p10746_fold_only_caveat_accepted_now"]
        )
        self.assertFalse(application["decision"]["deployment_closed_now"])
        self.assertFalse(application["guardrails"]["heldout_rows_read_now"])

        self.assertEqual(
            impact["status"],
            (
                "fold_augmented_confounded_proxy_p10746_decision_impact_"
                "blocked_remaining_evidence"
            ),
        )
        self.assertEqual(
            impact["counts"]["source_remaining_combined_score_blocker_rows"], 6
        )
        self.assertEqual(impact["counts"]["p10746_policy_blocker_rows"], 1)
        self.assertEqual(
            impact["counts"]["p10746_policy_blocker_resolved_rows"], 1
        )
        self.assertEqual(
            impact["counts"]["remaining_full_channel_blocker_rows_after_p10746"],
            5,
        )
        self.assertEqual(
            impact["counts"]["remaining_predicted_structure_unavailable_rows"], 4
        )
        self.assertEqual(
            impact["counts"]["remaining_approved_geometry_feature_missing_rows"], 1
        )
        self.assertEqual(impact["counts"]["remaining_policy_decision_required_rows"], 0)
        self.assertEqual(
            impact["counts"]["high_cofactor_min_new_abstained_rows_for_80pct"], 16
        )
        self.assertEqual(
            impact["counts"][
                "same_family_structural_min_new_abstained_rows_for_80pct"
            ],
            170,
        )
        self.assertFalse(
            impact["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(
            impact["decision"]["current_evidence_can_solve_confounded_safe_calibration"]
        )
        self.assertFalse(impact["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_q43088_geometry_locator_blocker_packet_counts(
        self,
    ) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_q43088_geometry_locator_blocker_packet_"
                "current702_20260604.json"
            )
        )

        self.assertEqual(
            packet["status"],
            (
                "fold_augmented_q43088_geometry_locator_blocker_packet_"
                "blocked_missing_source_free_locator"
            ),
        )
        self.assertEqual(packet["affected_row"]["entry_id"], "m_csa:604")
        self.assertEqual(packet["affected_row"]["accession"], "Q43088")
        self.assertEqual(
            packet["affected_row"]["blocker_class"],
            "approved_geometry_feature_missing",
        )
        self.assertEqual(
            packet["counts"]["local_predicted_coordinate_available_rows"], 1
        )
        self.assertEqual(packet["counts"]["fold_channel_available_rows"], 1)
        self.assertEqual(
            packet["counts"]["approved_source_free_geometry_locator_rows"], 0
        )
        self.assertEqual(packet["counts"]["active_site_residue_count"], 1)
        self.assertEqual(
            packet["counts"]["minimum_locator_positions_required_for_geometry_channel"],
            3,
        )
        self.assertEqual(
            packet["counts"]["additional_approved_locator_positions_needed"], 2
        )
        self.assertEqual(packet["counts"]["high_cofactor_proxy_membership_rows"], 1)
        self.assertEqual(
            packet["counts"]["selected_organic_cofactor_max_score"], 0.605709
        )
        self.assertIn(
            "q43088_missing_approved_source_free_geometry_sidecar",
            packet["blockers"],
        )
        self.assertFalse(
            packet["decision"]["q43088_ready_for_combined_channel_rescore_now"]
        )
        self.assertFalse(
            packet["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(packet["guardrails"]["row_rescored_now"])
        self.assertFalse(packet["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_q43088_source_free_locator_approval_contract_counts(
        self,
    ) -> None:
        contract = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_q43088_source_free_locator_approval_"
                "contract_current702_20260604.json"
            )
        )

        self.assertEqual(
            contract["status"],
            (
                "fold_augmented_q43088_source_free_locator_approval_contract_"
                "ready_for_review"
            ),
        )
        self.assertEqual(contract["affected_row"]["entry_id"], "m_csa:604")
        self.assertEqual(contract["affected_row"]["accession"], "Q43088")
        self.assertEqual(
            contract["affected_row"]["residual_blocker_class"],
            "approved_geometry_feature_missing",
        )
        self.assertTrue(
            contract["affected_row"]["local_predicted_coordinate_available"]
        )
        self.assertEqual(contract["counts"]["affected_rows"], 1)
        self.assertEqual(
            contract["counts"]["local_predicted_coordinate_available_rows"], 1
        )
        self.assertEqual(contract["counts"]["fold_channel_available_rows"], 1)
        self.assertEqual(contract["counts"]["active_site_residue_count"], 1)
        self.assertEqual(
            contract["counts"]["minimum_locator_positions_required_for_geometry_channel"],
            3,
        )
        self.assertEqual(
            contract["counts"]["additional_approved_locator_positions_needed"], 2
        )
        self.assertEqual(contract["counts"]["locator_positions_approved_now"], 0)
        self.assertEqual(contract["counts"]["geometry_sidecars_approved_now"], 0)
        self.assertEqual(
            contract["counts"]["high_cofactor_proxy_membership_rows"], 1
        )
        self.assertEqual(
            contract["counts"]["selected_organic_cofactor_max_score"], 0.605709
        )
        self.assertEqual(
            contract["counts"]["remaining_coordinate_source_blocker_rows"], 4
        )
        self.assertEqual(contract["counts"]["blockers"], 3)
        self.assertIn(
            "q43088_two_additional_source_free_locator_positions_not_approved",
            contract["blockers"],
        )
        self.assertFalse(contract["decision"]["q43088_ready_for_rescore_now"])
        self.assertFalse(
            contract["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(contract["guardrails"]["locator_positions_approved_now"])
        self.assertFalse(contract["guardrails"]["geometry_sidecar_approved_now"])
        self.assertFalse(contract["guardrails"]["row_rescored_now"])
        self.assertFalse(contract["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_q43088_source_free_locator_candidate_scout_counts(
        self,
    ) -> None:
        scout = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_q43088_source_free_locator_candidate_"
                "scout_current702_20260604.json"
            )
        )

        self.assertEqual(
            scout["status"],
            (
                "fold_augmented_q43088_source_free_locator_candidate_scout_"
                "pending_review_no_approval"
            ),
        )
        self.assertEqual(scout["counts"]["affected_rows"], 1)
        self.assertEqual(
            scout["counts"]["local_predicted_coordinate_available_rows"], 1
        )
        self.assertEqual(scout["counts"]["anchor_locator_rows"], 1)
        self.assertEqual(scout["counts"]["candidate_locator_rows"], 12)
        self.assertEqual(scout["counts"]["candidate_locators_approved_now"], 0)
        self.assertEqual(
            scout["counts"]["additional_approved_locator_positions_needed"], 2
        )
        self.assertEqual(scout["counts"]["q43088_ready_for_rescore_now"], 0)
        self.assertEqual(scout["counts"]["blockers"], 3)
        anchor = scout["anchor_locators"][0]
        self.assertEqual(anchor["sequence_position"], 287)
        self.assertEqual(anchor["residue_code"], "TYR")
        self.assertEqual(
            anchor["roles"], ["activator", "proton_acceptor", "proton_donor"]
        )
        candidates = scout["candidate_locator_rows"]
        self.assertEqual(candidates[0]["sequence_position"], 288)
        self.assertEqual(candidates[0]["residue_code"], "ASP")
        self.assertEqual(candidates[0]["approval_status"], "pending_review")
        self.assertFalse(candidates[0]["approved_now"])
        self.assertIn(
            "q43088_candidate_locators_pending_review", scout["blockers"]
        )
        self.assertFalse(scout["decision"]["q43088_ready_for_rescore_now"])
        self.assertFalse(
            scout["decision"]["candidate_scout_clears_locator_contract"]
        )
        self.assertFalse(
            scout["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertTrue(scout["guardrails"]["candidate_locators_generated_now"])
        self.assertFalse(scout["guardrails"]["locator_positions_approved_now"])
        self.assertFalse(scout["guardrails"]["row_rescored_now"])
        self.assertFalse(scout["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_confounded_proxy_residual_queue_after_p10746_q43088_counts(
        self,
    ) -> None:
        queue = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_residual_queue_after_"
                "p10746_q43088_current702_20260604.json"
            )
        )

        self.assertEqual(
            queue["status"],
            (
                "fold_augmented_confounded_proxy_residual_queue_blocked_after_"
                "p10746_q43088"
            ),
        )
        self.assertEqual(queue["counts"]["p10746_policy_blocker_resolved_rows"], 1)
        self.assertEqual(queue["counts"]["residual_full_channel_rows"], 5)
        self.assertEqual(
            queue["counts"]["residual_predicted_structure_unavailable_rows"], 4
        )
        self.assertEqual(
            queue["counts"]["residual_locator_or_geometry_sidecar_rows"], 1
        )
        self.assertEqual(queue["counts"]["residual_policy_decision_required_rows"], 0)
        self.assertEqual(
            queue["counts"]["q43088_additional_approved_locator_positions_needed"],
            2,
        )
        self.assertEqual(queue["counts"]["afdb_unavailable_rows_reprobed_current_run"], 4)
        self.assertEqual(
            queue["counts"]["high_cofactor_min_new_abstained_rows_for_80pct"], 16
        )
        self.assertEqual(
            queue["counts"][
                "same_family_structural_min_new_abstained_rows_for_80pct"
            ],
            170,
        )
        residual = {row["entry_id"]: row for row in queue["residual_full_channel_rows"]}
        self.assertEqual(
            sorted(residual),
            ["m_csa:416", "m_csa:562", "m_csa:586", "m_csa:604", "m_csa:637"],
        )
        self.assertIn(
            "q43088_needs_two_additional_approved_locator_positions_or_geometry_sidecar",
            queue["blockers"],
        )
        self.assertFalse(
            queue["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(queue["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_confounded_proxy_afdb_version_sweep_counts(
        self,
    ) -> None:
        sweep = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_afdb_version_sweep_"
                "current702_20260604.json"
            )
        )

        self.assertEqual(
            sweep["status"],
            "fold_augmented_confounded_proxy_afdb_version_sweep_no_models_available",
        )
        self.assertEqual(sweep["counts"]["probe_rows"], 4)
        self.assertEqual(sweep["counts"]["afdb_versions_checked_per_row"], 6)
        self.assertEqual(sweep["counts"]["afdb_http_200_rows"], 0)
        self.assertEqual(sweep["counts"]["afdb_all_versions_404_rows"], 4)
        self.assertEqual(sweep["counts"]["coordinate_downloads_performed"], 0)
        self.assertEqual(sweep["counts"]["blockers"], 2)
        rows = {row["entry_id"]: row for row in sweep["rows"]}
        self.assertEqual(
            sorted(rows),
            ["m_csa:416", "m_csa:562", "m_csa:586", "m_csa:637"],
        )
        for row in rows.values():
            self.assertFalse(row["any_afdb_model_available"])
            self.assertEqual(
                row["afdb_model_version_statuses"],
                {"1": 404, "2": 404, "3": 404, "4": 404, "5": 404, "6": 404},
            )
        self.assertFalse(
            sweep["decision"]["built_in_afdb_auto_version_fallback_can_clear_rows_now"]
        )
        self.assertFalse(
            sweep["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertIn(
            "approved_non_afdb_predicted_structure_source_missing",
            sweep["blockers"],
        )
        self.assertFalse(sweep["guardrails"]["coordinate_downloads_performed"])
        self.assertFalse(sweep["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_confounded_proxy_alternate_structure_source_contract_counts(
        self,
    ) -> None:
        contract = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_alternate_structure_"
                "source_contract_current702_20260604.json"
            )
        )

        self.assertEqual(
            contract["status"],
            (
                "fold_augmented_confounded_proxy_alternate_structure_source_"
                "contract_ready_for_source_approval"
            ),
        )
        self.assertEqual(
            contract["counts"]["residual_coordinate_source_blocker_rows"], 4
        )
        self.assertEqual(
            contract["counts"]["affected_coordinate_source_blocker_rows"], 4
        )
        self.assertEqual(contract["counts"]["afdb_versions_checked_per_row"], 6)
        self.assertEqual(contract["counts"]["afdb_all_versions_404_rows"], 4)
        self.assertEqual(contract["counts"]["afdb_http_200_rows"], 0)
        self.assertEqual(contract["counts"]["required_alternate_structure_rows"], 4)
        self.assertEqual(
            contract["counts"]["approved_alternate_structure_rows_now"], 0
        )
        self.assertEqual(
            contract["counts"]["remaining_non_coordinate_full_channel_blocker_rows"],
            1,
        )
        self.assertEqual(contract["counts"]["coordinate_downloads_performed"], 0)
        self.assertEqual(contract["counts"]["blockers"], 4)
        rows = {row["entry_id"]: row for row in contract["affected_rows"]}
        self.assertEqual(
            sorted(rows),
            ["m_csa:416", "m_csa:562", "m_csa:586", "m_csa:637"],
        )
        self.assertEqual(
            contract["source_contract"]["required_accessions"],
            ["P07071", "P07658", "P00806", "P04531"],
        )
        for row in rows.values():
            self.assertFalse(row["any_afdb_model_available"])
            self.assertFalse(row["rescore_ready_now"])
            self.assertEqual(
                row["residual_blocker_class"], "predicted_structure_unavailable"
            )
            self.assertEqual(
                row["missing_evidence_type"],
                (
                    "approved non-AFDB deployment-valid predicted-structure "
                    "coordinate source"
                ),
            )
            self.assertEqual(
                row["afdb_model_version_statuses"],
                {"1": 404, "2": 404, "3": 404, "4": 404, "5": 404, "6": 404},
            )
        self.assertIn(
            "alternate_predicted_structure_provider_not_approved",
            contract["blockers"],
        )
        self.assertFalse(
            contract["decision"]["approved_alternate_structure_rows_ready_now"]
        )
        self.assertFalse(
            contract["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(contract["guardrails"]["provider_approved_now"])
        self.assertFalse(contract["guardrails"]["coordinates_downloaded_or_imported"])
        self.assertFalse(contract["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_confounded_proxy_deployment_input_preflight_counts(
        self,
    ) -> None:
        preflight = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_deployment_input_"
                "preflight_current702_20260604.json"
            )
        )

        self.assertEqual(
            preflight["status"],
            (
                "fold_augmented_confounded_proxy_deployment_input_preflight_"
                "blocked_no_approved_predicted_coordinates"
            ),
        )
        self.assertEqual(preflight["counts"]["affected_rows"], 4)
        self.assertEqual(
            preflight["counts"]["approved_predicted_coordinate_hits"], 0
        )
        self.assertEqual(
            preflight["counts"]["rows_with_approved_predicted_hits"], 0
        )
        self.assertEqual(
            preflight["counts"]["disallowed_experimental_coordinate_hits"], 3
        )
        self.assertEqual(
            preflight["counts"]["rows_with_disallowed_experimental_hits"], 3
        )
        self.assertEqual(
            preflight["counts"]["rows_with_no_local_coordinate_hit"], 1
        )
        self.assertEqual(
            preflight["counts"]["deployment_valid_coordinate_rows_ready_now"], 0
        )
        self.assertEqual(
            preflight["counts"]["remaining_coordinate_source_blocker_rows"], 4
        )
        self.assertEqual(preflight["counts"]["blockers"], 4)
        rows = {row["entry_id"]: row for row in preflight["rows"]}
        self.assertEqual(
            sorted(rows),
            ["m_csa:416", "m_csa:562", "m_csa:586", "m_csa:637"],
        )
        self.assertEqual(
            rows["m_csa:416"]["local_status"], "no_local_coordinate_hit_observed"
        )
        self.assertEqual(
            rows["m_csa:562"]["local_status"],
            "experimental_only_disallowed_for_deployment",
        )
        self.assertEqual(
            rows["m_csa:586"]["local_status"],
            "experimental_only_disallowed_for_deployment",
        )
        self.assertEqual(
            rows["m_csa:637"]["local_status"],
            "experimental_only_disallowed_for_deployment",
        )
        self.assertEqual(
            rows["m_csa:562"]["disallowed_experimental_coordinate_hits"][0][
                "path"
            ],
            "artifacts/v3_foldseek_coordinates_1000/pdb_1AA6.cif",
        )
        self.assertEqual(
            rows["m_csa:586"]["disallowed_experimental_coordinate_hits"][0][
                "path"
            ],
            "artifacts/v3_foldseek_coordinates_1000/pdb_1LBA.cif",
        )
        self.assertEqual(
            rows["m_csa:637"]["disallowed_experimental_coordinate_hits"][0][
                "path"
            ],
            "artifacts/v3_foldseek_coordinates_1000/pdb_1DEK.cif",
        )
        self.assertIn(
            "experimental_pdb_coordinate_shortcuts_disallowed_for_deployment",
            preflight["blockers"],
        )
        self.assertFalse(
            preflight["decision"][
                "local_repo_can_clear_coordinate_source_blockers_now"
            ]
        )
        self.assertTrue(
            preflight["decision"]["experimental_coordinate_shortcuts_blocked"]
        )
        self.assertFalse(
            preflight["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(preflight["guardrails"]["downloads_performed"])
        self.assertFalse(
            preflight["guardrails"][
                "experimental_coordinates_used_as_deployment_inputs"
            ]
        )
        self.assertFalse(preflight["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_confounded_proxy_repo_wide_coordinate_sanity_scan_counts(
        self,
    ) -> None:
        scan = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_repo_wide_coordinate_"
                "sanity_scan_current702_20260604.json"
            )
        )

        self.assertEqual(
            scan["status"],
            (
                "fold_augmented_confounded_proxy_repo_wide_coordinate_sanity_scan_"
                "no_additional_approved_predicted_coordinates"
            ),
        )
        self.assertEqual(scan["counts"]["affected_rows"], 4)
        self.assertEqual(scan["counts"]["repo_wide_cif_files_scanned"], 1636)
        self.assertEqual(scan["counts"]["repo_wide_cif_accession_hits"], 3)
        self.assertEqual(scan["counts"]["repo_wide_unclassified_cif_hits"], 0)
        self.assertEqual(scan["counts"]["rows_with_any_repo_wide_cif_hit"], 3)
        self.assertEqual(scan["counts"]["rows_with_no_repo_wide_cif_hit"], 1)
        self.assertEqual(
            scan["counts"]["rows_with_only_disallowed_experimental_hits"], 3
        )
        self.assertEqual(
            scan["counts"]["rows_with_approved_predicted_hits_ready_now"], 0
        )
        self.assertEqual(
            scan["counts"]["deployment_valid_coordinate_rows_ready_now"], 0
        )
        self.assertEqual(
            scan["counts"]["remaining_coordinate_source_blocker_rows"], 4
        )
        rows = {row["entry_id"]: row for row in scan["rows"]}
        self.assertEqual(
            rows["m_csa:416"]["repo_wide_local_status"],
            "no_local_cif_accession_hit_observed",
        )
        self.assertEqual(
            rows["m_csa:562"]["repo_wide_cif_hits"][0]["hit_class"],
            "disallowed_experimental_coordinate_shortcut_recorded_in_preflight",
        )
        self.assertFalse(
            scan["decision"][
                "repo_wide_scan_changes_deployment_input_preflight_blocker"
            ]
        )
        self.assertFalse(
            scan["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(scan["guardrails"]["downloads_performed"])
        self.assertFalse(scan["guardrails"]["coordinates_staged_or_imported"])
        self.assertFalse(scan["guardrails"]["sources_approved_now"])
        self.assertFalse(scan["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_confounded_proxy_swissmodel_coordinate_staging_manifest_counts(
        self,
    ) -> None:
        probe = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_swissmodel_repository_"
                "probe_current702_20260604.json"
            )
        )
        manifest = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_swissmodel_coordinate_"
                "staging_manifest_current702_20260604.json"
            )
        )

        self.assertEqual(
            probe["status"],
            (
                "fold_augmented_confounded_proxy_swissmodel_repository_probe_"
                "partial_3_of_4"
            ),
        )
        self.assertEqual(probe["counts"]["rows_with_swissmodel_predicted_model"], 3)
        self.assertEqual(probe["counts"]["rows_with_pdb_provider_only"], 1)
        self.assertEqual(probe["counts"]["coordinates_staged_for_review_only"], 3)
        self.assertEqual(probe["counts"]["provider_pdb_structures_rejected"], 14)

        self.assertEqual(
            manifest["status"],
            (
                "fold_augmented_confounded_proxy_swissmodel_coordinate_staging_"
                "manifest_partial_3_of_4"
            ),
        )
        self.assertEqual(
            manifest["counts"]["affected_coordinate_source_blocker_rows"], 4
        )
        self.assertEqual(manifest["counts"]["swissmodel_predicted_model_rows"], 3)
        self.assertEqual(manifest["counts"]["staged_predicted_coordinate_rows"], 3)
        self.assertEqual(manifest["counts"]["pdb_provider_only_rows"], 1)
        self.assertEqual(
            manifest["counts"]["remaining_coordinate_source_blocker_rows"], 1
        )
        self.assertEqual(
            manifest["counts"]["coordinate_rows_rescore_input_ready_now"], 3
        )
        self.assertEqual(manifest["counts"]["fixed_threshold"], 0.44155)
        self.assertFalse(
            manifest["decision"]["coordinate_source_surface_fully_clear_now"]
        )
        self.assertEqual(
            manifest["decision"]["partial_coordinate_source_clearance_rows"], 3
        )
        self.assertFalse(
            manifest["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )

        rows = {row["entry_id"]: row for row in manifest["rows"]}
        self.assertEqual(
            sorted(rows),
            ["m_csa:416", "m_csa:562", "m_csa:586", "m_csa:637"],
        )
        for entry_id, accession, template in [
            ("m_csa:416", "P07071", "9d3x.1.A"),
            ("m_csa:586", "P00806", "1lba.1.A"),
            ("m_csa:637", "P04531", "1del.1.A"),
        ]:
            row = rows[entry_id]
            selected = row["selected_swissmodel_model"]
            self.assertEqual(row["accession"], accession)
            self.assertEqual(
                row["local_status"],
                "swissmodel_predicted_coordinate_staged_review_only",
            )
            self.assertEqual(selected["provider"], "SWISSMODEL")
            self.assertEqual(selected["method"], "HOMOLOGY MODELLING")
            self.assertEqual(selected["template"], template)
            self.assertTrue(selected["staged_coordinate_exists"])
            coordinate_path = ROOT / selected["staged_coordinate_path"]
            self.assertTrue(coordinate_path.exists())
            digest = hashlib.sha256(coordinate_path.read_bytes()).hexdigest()
            self.assertEqual(selected["staged_coordinate_sha256"], digest)
            self.assertEqual(
                row["provider_model_version_path_checksum_provenance"][
                    "checksum_sha256"
                ],
                digest,
            )
            self.assertTrue(row["coordinate_rescore_input_ready"])

        p07658 = rows["m_csa:562"]
        self.assertEqual(p07658["accession"], "P07658")
        self.assertEqual(
            p07658["local_status"], "swissmodel_repository_pdb_only_disallowed"
        )
        self.assertEqual(p07658["selected_swissmodel_model"], None)
        self.assertFalse(p07658["coordinate_rescore_input_ready"])
        self.assertIn(
            "swissmodel_repository_only_experimental_pdb_mappings",
            p07658["row_blockers"],
        )
        self.assertFalse(
            manifest["guardrails"]["experimental_pdb_repository_mappings_used_as_inputs"]
        )
        self.assertFalse(manifest["guardrails"]["candidate_rows_scored_now"])
        self.assertFalse(manifest["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_p07658_secondary_accession_predicted_coordinate_reprobe_counts(
        self,
    ) -> None:
        reprobe = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_p07658_secondary_accession_predicted_"
                "coordinate_reprobe_current702_20260604.json"
            )
        )

        self.assertEqual(
            reprobe["status"],
            (
                "fold_augmented_p07658_secondary_accession_reprobe_blocked_"
                "no_predicted_model"
            ),
        )
        self.assertEqual(reprobe["affected_row"]["entry_id"], "m_csa:562")
        self.assertEqual(reprobe["affected_row"]["accession"], "P07658")
        self.assertEqual(reprobe["secondary_accessions_checked"], ["P78137", "Q2M6M5"])
        self.assertEqual(reprobe["counts"]["secondary_accessions_checked"], 2)
        self.assertEqual(
            reprobe["counts"]["secondary_accessions_resolving_to_primary"], 2
        )
        self.assertEqual(reprobe["counts"]["swissmodel_predicted_model_rows"], 0)
        self.assertEqual(reprobe["counts"]["swissmodel_pdb_provider_rows"], 10)
        self.assertEqual(reprobe["counts"]["afdb_v6_http_404_rows"], 2)
        self.assertEqual(
            reprobe["counts"]["deployment_valid_predicted_coordinate_rows_ready_now"],
            0,
        )
        self.assertEqual(
            reprobe["counts"]["remaining_coordinate_source_blocker_rows"], 1
        )
        rows = {row["query_accession"]: row for row in reprobe["rows"]}
        for accession in ["P78137", "Q2M6M5"]:
            row = rows[accession]
            self.assertEqual(row["resolved_primary_accession"], "P07658")
            self.assertEqual(row["swissmodel_predicted_model_rows"], 0)
            self.assertEqual(row["swissmodel_pdb_provider_rows"], 5)
            self.assertEqual(row["afdb_v6_http_status"], 404)
            self.assertFalse(row["deployment_valid_predicted_coordinate_available"])
        self.assertFalse(
            reprobe["decision"][
                "p07658_secondary_accessions_clear_coordinate_blocker_now"
            ]
        )
        self.assertFalse(
            reprobe["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(
            reprobe["guardrails"]["experimental_pdb_mappings_used_as_deployment_inputs"]
        )
        self.assertFalse(reprobe["guardrails"]["candidate_rows_scored_now"])
        self.assertFalse(reprobe["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_p07658_esmfold_api_preflight_counts(self) -> None:
        preflight = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_p07658_esmfold_api_preflight_current702_20260604.json"
        )

        self.assertEqual(
            preflight["status"],
            "fold_augmented_p07658_esmfold_api_preflight_blocked_sequence_too_long",
        )
        self.assertEqual(preflight["affected_row"]["entry_id"], "m_csa:562")
        self.assertEqual(preflight["affected_row"]["accession"], "P07658")
        self.assertEqual(preflight["counts"]["sequence_length"], 715)
        self.assertEqual(preflight["counts"]["public_esmfold_endpoint_limit"], 400)
        self.assertEqual(preflight["counts"]["noncanonical_residue_count"], 1)
        self.assertEqual(preflight["counts"]["coordinates_returned"], 0)
        self.assertEqual(
            preflight["counts"]["remaining_coordinate_source_blocker_rows"], 1
        )
        self.assertEqual(preflight["endpoint_probe"]["http_status"], 413)
        self.assertEqual(
            preflight["endpoint_probe"]["response_body"],
            "Sequence is longer than 400.",
        )
        self.assertFalse(
            preflight["decision"]["public_esmfold_can_clear_p07658_now"]
        )
        self.assertFalse(
            preflight["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(preflight["guardrails"]["sequence_modified_or_truncated"])
        self.assertFalse(preflight["guardrails"]["coordinates_downloaded_or_staged"])
        self.assertFalse(preflight["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_p07658_full_length_predictor_provider_probe_counts(
        self,
    ) -> None:
        probe = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_p07658_full_length_predictor_provider_"
                "probe_current702_20260604.json"
            )
        )

        self.assertEqual(
            probe["status"],
            (
                "fold_augmented_p07658_full_length_predictor_provider_probe_"
                "blocked_auth_or_access"
            ),
        )
        self.assertEqual(probe["affected_row"]["entry_id"], "m_csa:562")
        self.assertEqual(probe["counts"]["providers_probed"], 2)
        self.assertEqual(probe["counts"]["credentialed_or_denied_providers"], 2)
        self.assertEqual(probe["counts"]["coordinates_returned"], 0)
        self.assertEqual(
            probe["counts"]["remaining_coordinate_source_blocker_rows"], 1
        )
        providers = {row["provider"]: row for row in probe["provider_probes"]}
        self.assertEqual(providers["BioLM ESMFold"]["http_status"], 401)
        self.assertEqual(providers["OpenProtein ESMFold"]["http_status"], 403)
        self.assertFalse(
            probe["decision"][
                "credential_free_full_length_provider_clears_p07658_now"
            ]
        )
        self.assertFalse(
            probe["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(probe["guardrails"]["credentials_or_tokens_used"])
        self.assertFalse(probe["guardrails"]["coordinates_downloaded_or_staged"])
        self.assertFalse(probe["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_p07658_local_predictor_runtime_scan_counts(
        self,
    ) -> None:
        scan = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_p07658_local_predictor_runtime_scan_"
                "current702_20260604.json"
            )
        )

        self.assertEqual(
            scan["status"],
            (
                "fold_augmented_p07658_local_predictor_runtime_scan_blocked_"
                "no_runtime"
            ),
        )
        self.assertEqual(scan["affected_row"]["entry_id"], "m_csa:562")
        self.assertEqual(scan["affected_row"]["accession"], "P07658")
        self.assertEqual(scan["affected_row"]["sequence_length"], 715)
        self.assertEqual(scan["affected_row"]["noncanonical_residue_count"], 1)
        self.assertEqual(scan["counts"]["path_commands_checked"], 5)
        self.assertEqual(scan["counts"]["path_commands_available"], 0)
        self.assertEqual(scan["counts"]["conda_envs_checked"], 3)
        self.assertEqual(scan["counts"]["python_modules_checked_per_env"], 6)
        self.assertEqual(scan["counts"]["python_module_hits"], 0)
        self.assertEqual(scan["counts"]["conda_env_tree_hits"], 0)
        self.assertEqual(scan["counts"]["private_tmp_runtime_or_coordinate_hits"], 0)
        self.assertEqual(scan["counts"]["coordinates_returned"], 0)
        self.assertEqual(scan["counts"]["coordinates_staged"], 0)
        self.assertEqual(
            scan["counts"]["remaining_coordinate_source_blocker_rows"], 1
        )
        self.assertFalse(scan["decision"]["local_runtime_clears_p07658_now"])
        self.assertFalse(scan["decision"]["fixed_threshold_audit_ready_to_rerun_now"])
        self.assertFalse(scan["guardrails"]["coordinates_downloaded_or_staged"])
        self.assertFalse(scan["guardrails"]["sequence_modified_or_truncated"])
        self.assertFalse(scan["guardrails"]["credentials_or_tokens_used"])
        self.assertFalse(scan["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_p07658_3dbeacons_predicted_structure_probe_counts(
        self,
    ) -> None:
        probe = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_p07658_3dbeacons_predicted_structure_"
                "probe_current702_20260604.json"
            )
        )

        self.assertEqual(
            probe["status"],
            "fold_augmented_p07658_3dbeacons_probe_blocked_experimental_only",
        )
        self.assertEqual(probe["affected_row"]["entry_id"], "m_csa:562")
        self.assertEqual(probe["affected_row"]["accession"], "P07658")
        self.assertEqual(probe["affected_row"]["sequence_length"], 715)
        self.assertEqual(probe["endpoint_probe"]["http_status"], 200)
        self.assertEqual(probe["counts"]["structures_returned"], 5)
        self.assertEqual(probe["counts"]["predicted_model_rows"], 0)
        self.assertEqual(probe["counts"]["experimental_model_rows"], 5)
        self.assertEqual(probe["counts"]["provider_counts"], {"PDBe": 5})
        self.assertEqual(
            probe["counts"][
                "deployment_valid_predicted_coordinate_rows_ready_now"
            ],
            0,
        )
        self.assertEqual(
            {row["model_category"] for row in probe["rows"]},
            {"EXPERIMENTALLY DETERMINED"},
        )
        self.assertFalse(probe["decision"]["three_d_beacons_clears_p07658_now"])
        self.assertFalse(
            probe["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(
            probe["guardrails"]["experimental_coordinates_used_as_deployment_inputs"]
        )
        self.assertFalse(probe["guardrails"]["coordinates_downloaded_or_staged"])
        self.assertFalse(probe["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_confounded_proxy_current_evidence_after_swissmodel_staging_counts(
        self,
    ) -> None:
        blocker = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_current_evidence_after_"
                "swissmodel_staging_current702_20260604.json"
            )
        )

        self.assertEqual(
            blocker["status"],
            (
                "fold_augmented_confounded_proxy_current_evidence_after_"
                "swissmodel_staging_blocked_partial_surface"
            ),
        )
        self.assertEqual(blocker["counts"]["staged_predicted_coordinate_rows"], 3)
        self.assertEqual(blocker["counts"]["surface_completeness_blocker_rows"], 2)
        self.assertEqual(blocker["counts"]["coordinate_source_blocker_rows"], 1)
        self.assertEqual(
            blocker["counts"]["locator_or_geometry_sidecar_blocker_rows"], 1
        )
        self.assertEqual(
            blocker["counts"]["coordinate_rows_rescore_input_ready_now"], 3
        )
        self.assertEqual(
            blocker["counts"]["fixed_threshold_score_rows_ready_to_rerun_now"], 0
        )
        self.assertEqual(
            blocker["counts"]["high_cofactor_min_new_abstained_rows_for_80pct"],
            16,
        )
        self.assertEqual(
            blocker["counts"][
                "same_family_structural_min_new_abstained_rows_for_80pct"
            ],
            170,
        )
        staged = {row["entry_id"]: row for row in blocker["staged_coordinate_rows"]}
        self.assertEqual(sorted(staged), ["m_csa:416", "m_csa:586", "m_csa:637"])
        coordinate_rows = {
            row["entry_id"]: row
            for row in blocker["surface_completeness_blocker_rows"][
                "coordinate_source_rows"
            ]
        }
        locator_rows = {
            row["entry_id"]: row
            for row in blocker["surface_completeness_blocker_rows"][
                "locator_or_geometry_sidecar_rows"
            ]
        }
        self.assertEqual(sorted(coordinate_rows), ["m_csa:562"])
        self.assertEqual(coordinate_rows["m_csa:562"]["accession"], "P07658")
        self.assertIn(
            "local PATH, conda env, and shallow filesystem runtime scan found no "
            "full-length predictor",
            coordinate_rows["m_csa:562"]["failed_rescue_paths"],
        )
        self.assertIn(
            "3D-Beacons summary returns only experimentally determined PDBe rows",
            coordinate_rows["m_csa:562"]["failed_rescue_paths"],
        )
        self.assertEqual(sorted(locator_rows), ["m_csa:604"])
        self.assertEqual(
            locator_rows["m_csa:604"]["additional_approved_locator_positions_needed"],
            2,
        )
        self.assertIn(
            "p07658_local_predictor_runtime_scan",
            blocker["source_artifacts"],
        )
        self.assertIn(
            "p07658_3dbeacons_predicted_structure_probe",
            blocker["source_artifacts"],
        )
        self.assertFalse(
            blocker["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(blocker["guardrails"]["candidate_rows_scored_now"])
        self.assertFalse(blocker["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_q43088_locator_review_priority_packet_counts(
        self,
    ) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_q43088_locator_review_priority_packet_current702_20260604.json"
        )

        self.assertEqual(
            packet["status"],
            "fold_augmented_q43088_locator_review_priority_packet_ready_no_approvals",
        )
        self.assertEqual(packet["affected_row"]["entry_id"], "m_csa:604")
        self.assertEqual(packet["affected_row"]["accession"], "Q43088")
        self.assertEqual(packet["counts"]["anchor_locator_rows"], 1)
        self.assertEqual(packet["counts"]["candidate_locator_rows"], 12)
        self.assertEqual(packet["counts"]["priority_candidate_rows"], 4)
        self.assertEqual(
            packet["counts"]["minimum_additional_locator_positions_needed"], 2
        )
        self.assertEqual(packet["counts"]["locator_positions_approved_now"], 0)
        self.assertEqual(packet["counts"]["q43088_ready_for_rescore_now"], 0)
        self.assertEqual(
            [row["sequence_position"] for row in packet["priority_candidate_rows"]],
            [288, 286, 243, 250],
        )
        self.assertFalse(packet["decision"]["q43088_ready_for_rescore_now"])
        self.assertFalse(packet["decision"]["priority_packet_clears_locator_contract"])
        self.assertFalse(
            packet["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(packet["guardrails"]["locator_positions_approved_now"])
        self.assertFalse(packet["guardrails"]["geometry_sidecar_approved_now"])
        self.assertFalse(packet["guardrails"]["row_rescored_now"])
        self.assertFalse(packet["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_confounded_proxy_current_evidence_blocker_after_input_preflight_counts(
        self,
    ) -> None:
        blocker = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_proxy_current_evidence_"
                "blocker_after_input_preflight_current702_20260604.json"
            )
        )

        self.assertEqual(
            blocker["status"],
            (
                "fold_augmented_confounded_proxy_current_evidence_blocker_"
                "blocked_after_input_preflight"
            ),
        )
        self.assertEqual(
            blocker["counts"]["surface_completeness_blocker_rows"], 5
        )
        self.assertEqual(blocker["counts"]["coordinate_source_blocker_rows"], 4)
        self.assertEqual(blocker["counts"]["coordinate_rows_ready_now"], 0)
        self.assertEqual(
            blocker["counts"]["disallowed_experimental_shortcut_rows"], 3
        )
        self.assertEqual(blocker["counts"]["rows_with_no_local_coordinate_hit"], 1)
        self.assertEqual(
            blocker["counts"]["locator_or_geometry_sidecar_blocker_rows"], 1
        )
        self.assertEqual(
            blocker["counts"][
                "q43088_additional_approved_locator_positions_needed"
            ],
            2,
        )
        self.assertEqual(
            blocker["counts"]["high_cofactor_min_new_abstained_rows_for_80pct"],
            16,
        )
        self.assertEqual(
            blocker["counts"][
                "same_family_structural_min_new_abstained_rows_for_80pct"
            ],
            170,
        )
        self.assertEqual(blocker["counts"]["blockers"], 6)
        coordinate_rows = {
            row["entry_id"]: row
            for row in blocker["surface_completeness_blocker_rows"][
                "coordinate_source_rows"
            ]
        }
        self.assertEqual(
            sorted(coordinate_rows),
            ["m_csa:416", "m_csa:562", "m_csa:586", "m_csa:637"],
        )
        locator_rows = blocker["surface_completeness_blocker_rows"][
            "locator_or_geometry_sidecar_rows"
        ]
        self.assertEqual(locator_rows[0]["entry_id"], "m_csa:604")
        self.assertEqual(
            locator_rows[0]["additional_approved_locator_positions_needed"], 2
        )
        self.assertIn(
            "current_local_evidence_cannot_clear_surface_completeness",
            blocker["blockers"],
        )
        self.assertFalse(
            blocker["decision"]["current_evidence_can_solve_surface_completeness"]
        )
        self.assertFalse(
            blocker["decision"][
                "current_evidence_can_solve_confounded_safe_calibration"
            ]
        )
        self.assertFalse(
            blocker["decision"]["fixed_threshold_audit_ready_to_rerun_now"]
        )
        self.assertFalse(blocker["guardrails"]["downloads_performed"])
        self.assertFalse(blocker["guardrails"]["coordinates_staged_or_imported"])
        self.assertFalse(blocker["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_augmented_post_decision_deployment_closure_status_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_post_decision_deployment_closure_status_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "fold_augmented_post_decision_deployment_closure_blocked_pending_p10746_decision",
        )
        self.assertEqual(audit["counts"]["heldout_confounded_oos_abstained"], 5)
        self.assertEqual(audit["counts"]["heldout_confounded_oos_total"], 6)
        self.assertEqual(audit["counts"]["expanded_full_channel_score_rows"], 75)
        self.assertEqual(audit["counts"]["candidate_ids_requested"], 76)
        self.assertEqual(audit["counts"]["remaining_combined_score_blocker_rows"], 1)
        self.assertEqual(audit["counts"]["p10746_caveat_accepted_rows"], 0)
        self.assertEqual(audit["counts"]["p10746_pending_decision_rows"], 1)
        self.assertIn("p10746_fold_only_caveat_not_accepted", audit["blockers"])
        self.assertTrue(
            audit["decision"]["confounded_subset_target_met_for_research"]
        )
        self.assertTrue(
            audit["decision"]["in_scope_retention_ok_at_operating_point"]
        )
        self.assertFalse(audit["decision"]["deployment_closed_now"])
        self.assertFalse(
            audit["decision"]["deployment_closed_with_p10746_caveat"]
        )
        self.assertFalse(audit["guardrails"]["heldout_rows_read_now"])
        self.assertFalse(
            audit["guardrails"]["deployment_closed_without_explicit_p10746_decision"]
        )

    def test_fold_augmented_remaining_blocker_decision_matrix_current_counts(
        self,
    ) -> None:
        matrix = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_remaining_blocker_decision_matrix_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            matrix["status"],
            "fold_augmented_remaining_blocker_decision_matrix_ready_review_only",
        )
        self.assertEqual(matrix["counts"]["decision_rows"], 5)
        self.assertEqual(matrix["counts"]["source_feature_sidecar_review_rows"], 3)
        self.assertEqual(matrix["counts"]["alternate_accession_policy_rows"], 1)
        self.assertEqual(matrix["counts"]["non_residue_interaction_policy_rows"], 1)
        self.assertEqual(matrix["counts"]["authorized_now"], 0)
        self.assertEqual(matrix["counts"]["ready_for_scoring_now"], 0)
        rows = {row["entry_id"]: row for row in matrix["decision_rows"]}
        self.assertEqual(
            rows["m_csa:531"]["decision_class"],
            "manual_source_feature_sidecar_review",
        )
        self.assertIn(
            "authorize_alternate:O75390",
            rows["m_csa:78"]["decision_options"],
        )
        self.assertEqual(
            rows["m_csa:204"]["decision_class"],
            "non_residue_interaction_sidecar_policy_design",
        )
        self.assertFalse(matrix["guardrails"]["alternate_accession_authorized"])

    def test_fold_augmented_non_residue_interaction_sidecar_policy_preflight_current_counts(
        self,
    ) -> None:
        preflight = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_non_residue_interaction_sidecar_policy_preflight_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            preflight["status"],
            "fold_augmented_non_residue_interaction_sidecar_policy_preflight_blocked_no_approved_policy",
        )
        self.assertEqual(preflight["counts"]["policy_rows"], 1)
        self.assertEqual(preflight["counts"]["coordinate_available_rows"], 1)
        self.assertEqual(preflight["counts"]["source_feature_rows"], 0)
        self.assertEqual(preflight["counts"]["graph_residue_nodes"], 0)
        self.assertEqual(preflight["counts"]["local_graph_residue_nodes"], 0)
        self.assertEqual(preflight["counts"]["mechanism_text_nodes_present"], 1)
        self.assertEqual(
            preflight["counts"][
                "mechanism_text_nodes_eligible_for_predictive_features"
            ],
            0,
        )
        self.assertEqual(preflight["counts"]["approved_policy_rows"], 0)
        self.assertEqual(preflight["counts"]["sidecars_created_now"], 0)
        self.assertEqual(preflight["counts"]["copy_authorized_now"], 0)
        self.assertEqual(preflight["counts"]["deployment_blockers_cleared_now"], 0)
        row = preflight["policy_preflight_rows"][0]
        self.assertEqual(row["entry_id"], "m_csa:204")
        self.assertFalse(row["non_residue_interaction_sidecar_policy_defined"])
        self.assertFalse(row["mechanism_text_eligible_for_predictive_features"])
        self.assertFalse(
            preflight["guardrails"]["mechanism_text_used_as_predictive_feature"]
        )

    def test_fold_augmented_fold_only_deployment_contract_decision_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_fold_only_deployment_contract_decision_"
                "current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "fold_only_deployment_contract_no_go_fixed_threshold_insufficient",
        )
        self.assertFalse(
            audit["decision"]["fold_only_deployment_contract_authorized"]
        )
        self.assertFalse(audit["decision"]["fold_only_85pct_rescue_contract_authorized"])
        self.assertEqual(audit["counts"]["fold_only_blocker_rows"], 4)
        self.assertEqual(
            audit["counts"]["fold_only_rows_abstained_at_90pct_threshold"], 0
        )
        self.assertEqual(
            audit["counts"]["fold_only_rows_abstained_at_85pct_threshold"], 1
        )
        self.assertEqual(
            audit["counts"]["heldout_confounded_oos_abstain_recall_at_90pct_threshold"],
            0.3333,
        )
        self.assertEqual(audit["counts"]["critical_violation_total"], 5)
        self.assertFalse(audit["guardrails"]["threshold_selected_or_tuned"])

    def test_predicted_structure_fold_confounded_operating_point_readiness_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_predicted_structure_fold_confounded_operating_point_readiness_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "predicted_structure_fold_confounded_operating_point_research_ready_deployment_blocked",
        )
        self.assertTrue(
            audit["decision"]["research_confounded_operating_point_ready"]
        )
        self.assertFalse(audit["decision"]["deployment_closed"])
        self.assertEqual(audit["counts"]["priority_confounded_oos_rows"], 6)
        self.assertEqual(audit["counts"]["priority_confounded_nearest_hits"], 6)
        self.assertTrue(audit["counts"]["deployment_input_contract_passed"])
        self.assertEqual(
            audit["counts"]["deployment_input_coordinate_request_rows"], 299
        )
        self.assertEqual(audit["counts"]["deployment_input_row_score_rows"], 126)
        self.assertEqual(
            audit["counts"]["deployment_input_critical_violation_total"], 0
        )
        self.assertEqual(
            audit["operating_point_summary"]["fixed_operating_threshold"], 0.44155
        )
        self.assertEqual(
            audit["counts"][
                "source_feature_review_gate_manual_approval_decisions_required"
            ],
            3,
        )
        self.assertEqual(
            audit["counts"]["source_feature_review_gate_copy_authorized_now"], 0
        )
        self.assertEqual(
            audit["counts"]["p23007_policy_gate_review_ready_candidates"], 4
        )
        self.assertEqual(
            audit["counts"]["p23007_policy_gate_replacement_authorized_now"], 0
        )
        self.assertEqual(
            audit["counts"]["p10746_non_residue_policy_approved_rows"], 0
        )
        self.assertEqual(
            audit["counts"]["p10746_non_residue_policy_sidecars_created_now"], 0
        )
        self.assertIn(
            "P23007 alternate-accession policy",
            audit["decision"]["next_gate"],
        )
        self.assertEqual(
            audit["operating_point_summary"][
                "heldout_confounded_oos_abstain_recall"
            ],
            0.8333,
        )
        gate_statuses = {
            row["gate"]: row["status"] for row in audit["deployment_closure_gate"]
        }
        self.assertEqual(
            gate_statuses["predicted_structure_vs_atlas_input_contract"],
            "passed",
        )
        self.assertEqual(
            gate_statuses["fixed_oos_calibrated_operating_threshold"],
            "fixed_no_change",
        )
        self.assertEqual(gate_statuses["production_blocker_rows"], "blocked")
        self.assertEqual(
            gate_statuses["persistent_afdb_coordinate_bundle"], "passed"
        )
        self.assertEqual(gate_statuses["fold_only_escape_hatch"], "rejected")
        self.assertEqual(audit["counts"]["heldout_confounded_oos_abstained"], 5)
        self.assertEqual(audit["counts"]["heldout_confounded_oos_total"], 6)
        self.assertEqual(audit["counts"]["remaining_production_blocker_rows"], 5)
        self.assertEqual(audit["counts"]["fold_only_blocker_rows"], 4)
        self.assertEqual(
            audit["counts"]["fold_only_rows_abstained_at_90pct_threshold"], 0
        )
        self.assertEqual(audit["counts"]["unique_coordinate_files_missing"], 0)
        self.assertEqual(
            audit["counts"]["remaining_blocker_coordinate_reprobe_rows_cleared"], 0
        )
        self.assertEqual(
            audit["counts"]["remaining_blocker_coordinate_reprobe_unavailable_rows"], 1
        )
        self.assertEqual(
            audit[
                "counts"
            ][
                "remaining_blocker_coordinate_reprobe_source_geometry_blocked_rows"
            ],
            4,
        )
        self.assertEqual(audit["counts"]["source_sidecar_preflight_candidate_rows"], 3)
        self.assertEqual(
            audit["counts"]["source_sidecar_preflight_coordinate_policy_blocked_rows"],
            1,
        )
        self.assertEqual(
            audit["counts"][
                "source_sidecar_preflight_non_residue_policy_blocked_rows"
            ],
            1,
        )
        self.assertEqual(
            [row["entry_id"] for row in audit["remaining_production_blocker_rows"]],
            ["m_csa:78", "m_csa:204", "m_csa:531", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertFalse(
            audit["remaining_production_blocker_rows"][0]["coordinate_reprobe"][
                "coordinate_available_now"
            ]
        )
        self.assertEqual(
            audit["remaining_production_blocker_rows"][1]["coordinate_reprobe"][
                "remaining_blocker"
            ],
            "source active-site geometry evidence missing",
        )
        self.assertTrue(
            audit["remaining_production_blocker_rows"][2][
                "source_sidecar_preflight"
            ]["source_feature_sidecar_candidate"]
        )
        self.assertFalse(
            audit["guardrails"]["experimental_pdb_metadata_used_as_channel_input"]
        )
        self.assertFalse(audit["decision"]["apply_or_change_threshold_now"])

    def test_fold_augmented_remaining_blocker_coordinate_reprobe_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_remaining_blocker_coordinate_reprobe_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "fold_augmented_remaining_blocker_coordinate_reprobe_no_rows_cleared",
        )
        self.assertEqual(audit["counts"]["remaining_blocker_rows"], 5)
        self.assertEqual(audit["counts"]["coordinate_unavailable_rows"], 1)
        self.assertEqual(audit["counts"]["coordinate_available_rows"], 4)
        self.assertEqual(audit["counts"]["rows_cleared_by_reprobe"], 0)
        rows = {row["entry_id"]: row for row in audit["rows"]}
        self.assertEqual(rows["m_csa:78"]["afdb_model_version_statuses"]["v7"], 404)
        self.assertEqual(
            rows["m_csa:78"]["uniprot_current_record_probe"][
                "alphafold_db_cross_references"
            ],
            [],
        )
        self.assertEqual(rows["m_csa:204"]["afdb_model_version_statuses"]["v6"], 200)
        self.assertFalse(audit["guardrails"]["coordinates_imported_or_cached"])

    def test_fold_augmented_confounded_deployment_closure_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_confounded_deployment_closure_audit_"
                "current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "confounded_fold_channel_research_ready_production_blocked",
        )
        self.assertEqual(audit["operating_point"]["fixed_threshold"], 0.44155)
        self.assertEqual(audit["counts"]["priority_confounded_oos_rows"], 6)
        self.assertEqual(audit["counts"]["priority_nearest_hits"], 6)
        self.assertEqual(audit["counts"]["heldout_confounded_oos_abstained"], 5)
        self.assertEqual(audit["counts"]["heldout_confounded_oos_total"], 6)
        self.assertEqual(audit["counts"]["remaining_production_blocker_rows"], 5)
        self.assertEqual(audit["counts"]["critical_violation_total"], 5)
        self.assertTrue(
            audit["decision"]["confounded_subset_target_met_for_research"]
        )
        self.assertFalse(audit["decision"]["deployable_without_production_caveat"])
        self.assertFalse(audit["guardrails"]["threshold_values_changed"])
        self.assertFalse(
            audit["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )

    def test_predicted_structure_fold_channel_contract_audit_current_counts(self) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_predicted_structure_fold_channel_contract_audit_current702_20260601.json"
        )

        self.assertEqual(audit["status"], "fold_channel_contract_passed_current702")
        self.assertEqual(audit["counts"]["heldout_rows_ok"], 126)
        self.assertEqual(audit["counts"]["all_heldout_nearest_hits"], 126)
        self.assertEqual(audit["counts"]["priority_cofactor_confounded_oos_rows"], 6)
        self.assertEqual(audit["counts"]["priority_nearest_hits"], 6)
        self.assertTrue(
            all(
                count == 0
                for count in audit["counts"]["critical_counts"].values()
            )
        )
        self.assertEqual(
            audit["foldseek_result_files"]["all_heldout_vs_atlas"][
                "query_entry_count_with_hits"
            ],
            126,
        )
        self.assertEqual(
            audit["foldseek_result_files"]["priority_cofactor_confounded_oos_vs_atlas"][
                "query_entry_count_with_hits"
            ],
            6,
        )

    def test_predicted_structure_fold_channel_deployment_input_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_predicted_structure_fold_channel_deployment_input_audit_current702_20260602.json"
        )

        self.assertEqual(
            audit["status"],
            "predicted_structure_fold_channel_deployment_inputs_predicted_only",
        )
        self.assertTrue(
            audit["decision"]["deployment_input_contract_passed"]
        )
        self.assertTrue(
            audit["deployment_validity"]["predicted_structure_vs_atlas_only"]
        )
        self.assertEqual(audit["counts"]["coordinate_request_rows"], 299)
        self.assertEqual(audit["counts"]["afdb_url_requests"], 299)
        self.assertEqual(audit["counts"]["afdb_local_path_requests"], 299)
        self.assertEqual(audit["counts"]["row_score_rows"], 126)
        self.assertEqual(
            audit["counts"]["row_scores_with_nearest_atlas_tm_score"], 126
        )
        self.assertEqual(audit["counts"]["critical_violation_total"], 0)
        self.assertTrue(
            all(
                count == 0
                for count in audit["counts"]["critical_counts"].values()
            )
        )
        self.assertFalse(
            audit["guardrails"]["foldseek_or_tm_rerun_performed"]
        )
        self.assertFalse(
            audit["guardrails"]["experimental_pdb_metadata_used_as_channel_input"]
        )

    def test_predicted_structure_fold_channel_coordinate_provenance_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_predicted_structure_fold_channel_coordinate_provenance_audit_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "coordinate_provenance_complete",
        )
        self.assertEqual(audit["counts"]["total_coordinate_requests"], 299)
        self.assertEqual(audit["counts"]["unique_coordinate_files_expected"], 299)
        self.assertEqual(audit["counts"]["unique_coordinate_files_observed"], 299)
        self.assertEqual(audit["counts"]["unique_coordinate_files_missing"], 0)
        self.assertEqual(audit["counts"]["unique_accessions_expected"], 293)
        self.assertEqual(
            audit["counts"]["unique_accessions_without_any_local_file"],
            0,
        )
        self.assertEqual(audit["counts"]["duplicate_accession_requests"], 6)
        self.assertTrue(audit["counts"]["result_files_parseable"])
        self.assertEqual(audit["contract_audit"]["critical_violation_total"], 0)

    def test_predicted_structure_fold_channel_reproduction_manifest_current_counts(
        self,
    ) -> None:
        manifest = _load_json(
            ROOT
            / "artifacts"
            / "v3_predicted_structure_fold_channel_reproduction_manifest_current702_20260601.json"
        )

        self.assertEqual(
            manifest["status"],
            "fold_channel_byte_reproduction_ready",
        )
        self.assertEqual(manifest["counts"]["heldout_rows_ok"], 126)
        self.assertEqual(
            manifest["counts"]["priority_cofactor_confounded_oos_rows"],
            6,
        )
        self.assertEqual(manifest["counts"]["total_coordinate_requests"], 299)
        self.assertEqual(manifest["counts"]["unique_coordinate_files_expected"], 299)
        self.assertEqual(manifest["counts"]["unique_coordinate_files_observed"], 299)
        self.assertEqual(manifest["counts"]["unique_coordinate_files_missing"], 0)
        self.assertEqual(manifest["counts"]["unique_accessions_expected"], 293)
        self.assertEqual(
            manifest["counts"]["unique_accessions_without_any_local_file"],
            0,
        )
        self.assertEqual(manifest["counts"]["duplicate_accession_requests"], 6)
        self.assertEqual(manifest["counts"]["foldseek_result_files"], 2)
        self.assertTrue(manifest["counts"]["result_files_parseable"])
        self.assertTrue(manifest["counts"]["foldseek_runtime_available"])
        self.assertTrue(manifest["counts"]["byte_reproduction_ready"])
        self.assertEqual(manifest["blocker_classes"], [])
        self.assertEqual(
            manifest["scored_channel_contract"]["critical_violation_total"],
            0,
        )
        self.assertFalse(manifest["guardrails"]["coordinate_downloads_performed"])
        self.assertFalse(manifest["guardrails"]["foldseek_or_tmsearch_recomputed"])

    def test_predicted_structure_fold_channel_carryover_resolution_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_predicted_structure_fold_channel_carryover_resolution_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "fold_channel_carryover_resolved_no_rerun_needed",
        )
        resolution = audit["requested_carryover_resolution"]
        self.assertTrue(resolution["requested_outputs_present"])
        self.assertTrue(resolution["scored_scope_complete"])
        self.assertFalse(resolution["foldseek_rerun_required"])
        self.assertFalse(resolution["coordinate_provenance_blocker_is_score_blocker"])
        self.assertEqual(audit["counts"]["heldout_rows_ok"], 126)
        self.assertEqual(audit["counts"]["all_heldout_nearest_hits"], 126)
        self.assertEqual(audit["counts"]["priority_cofactor_confounded_oos_rows"], 6)
        self.assertEqual(audit["counts"]["priority_nearest_hits"], 6)
        self.assertEqual(audit["counts"]["contract_critical_violation_total"], 0)
        self.assertEqual(audit["counts"]["unique_coordinate_files_missing"], 0)
        self.assertTrue(resolution["byte_level_reproduction_ready"])
        self.assertEqual(resolution["remaining_blocker_classes"], [])

    def test_predicted_atlas_geometry_novelty_variants_current_counts(self) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_predicted_atlas_geometry_novelty_variants_current702_20260601.json"
        )

        self.assertEqual(audit["status"], "computed_predicted_atlas_geometry_variants")
        self.assertEqual(audit["counts"]["atlas_rows"], 168)
        self.assertEqual(audit["counts"]["heldout_rows"], 126)
        self.assertEqual(audit["counts"]["inscope"], 47)
        self.assertEqual(audit["counts"]["oos"], 79)
        self.assertEqual(audit["counts"]["confounded_predicted_geometry_oos"], 6)
        self.assertEqual(
            audit["best_signal"]["name"],
            "negative_nearest_class_centroid_robust_distance",
        )
        self.assertEqual(audit["best_signal"]["auc_in_gt_oos_all"], 0.776461)
        self.assertTrue(
            audit["guardrails"]["atlas_statistics_only_for_normalization"]
        )

    def test_predicted_atlas_geometry_novelty_operating_grid_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_predicted_atlas_geometry_novelty_operating_grid_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "predicted_atlas_geometry_novelty_operating_grid_ready_review_only",
        )
        self.assertEqual(audit["counts"]["row_scores"], 126)
        self.assertEqual(audit["counts"]["signals"], 10)
        self.assertEqual(audit["counts"]["retention_targets"], 4)
        self.assertEqual(audit["counts"]["grid_rows"], 40)
        self.assertTrue(audit["guardrails"]["uses_existing_variant_artifact_only"])
        self.assertFalse(audit["guardrails"]["production_thresholds_changed"])
        best = audit["best_signal_from_variant_artifact"]
        self.assertEqual(
            best["name"],
            "negative_nearest_class_centroid_robust_distance",
        )
        self.assertEqual(
            best["best_at_90pct_inscope_retention"]["oos_abstain_recall"],
            0.2278,
        )
        self.assertEqual(
            best["best_at_85pct_inscope_retention"]["oos_abstain_recall"],
            0.5949,
        )
        self.assertEqual(
            audit["best_by_retention_target"]["0.90"]["signal"],
            "negative_nearest_class_centroid_robust_distance",
        )
        confounded_rows = best["confounded_rows"]
        self.assertEqual(
            [row["entry_id"] for row in confounded_rows],
            ["m_csa:30", "m_csa:31", "m_csa:80", "m_csa:191", "m_csa:267", "m_csa:448"],
        )
        self.assertEqual(
            sum(1 for row in confounded_rows if row["abstained_at_best_signal_90pct"]),
            2,
        )
        self.assertEqual(
            sum(1 for row in confounded_rows if row["abstained_at_best_signal_85pct"]),
            4,
        )

    def test_predicted_structure_fold_augmented_novelty_variants_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_predicted_structure_fold_augmented_novelty_variants_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "computed_from_existing_predicted_geometry_and_predicted_fold_channels_review_only",
        )
        self.assertEqual(audit["counts"]["overlap_rows"], 126)
        self.assertEqual(audit["counts"]["inscope"], 47)
        self.assertEqual(audit["counts"]["oos"], 79)
        self.assertEqual(audit["counts"]["confounded_predicted_geometry_oos"], 6)
        self.assertEqual(audit["counts"]["signals"], 11)
        self.assertEqual(audit["best_signal"]["name"], "mean_top1_raw_and_tm")
        self.assertEqual(audit["best_signal"]["auc_in_gt_oos_all"], 0.907622)
        self.assertEqual(audit["best_signal"]["auc_in_gt_confounded_oos"], 0.911348)
        self.assertFalse(audit["guardrails"]["foldseek_or_tmsearch_recomputed"])
        self.assertFalse(audit["guardrails"]["production_thresholds_changed"])
        self.assertEqual(
            audit["comparisons"]["geometry_best_from_prior_artifact"]["name"],
            "negative_nearest_class_centroid_robust_distance",
        )
        self.assertEqual(
            audit["comparisons"]["fold_only_from_predicted_structure_channel"][
                "auc_in_gt_oos_all"
            ],
            0.814301,
        )

    def test_predicted_structure_fold_augmented_novelty_operating_grid_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_predicted_structure_fold_augmented_novelty_operating_grid_"
                "current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "predicted_structure_fold_augmented_novelty_operating_grid_ready_review_only",
        )
        self.assertEqual(audit["counts"]["row_scores"], 126)
        self.assertEqual(audit["counts"]["signals"], 11)
        self.assertEqual(audit["counts"]["retention_targets"], 4)
        self.assertEqual(audit["counts"]["grid_rows"], 44)
        self.assertTrue(audit["guardrails"]["uses_existing_variant_artifact_only"])
        self.assertFalse(audit["guardrails"]["foldseek_or_tmsearch_recomputed"])
        self.assertFalse(audit["guardrails"]["production_thresholds_changed"])
        best = audit["best_signal_from_variant_artifact"]
        self.assertEqual(best["name"], "mean_top1_raw_and_tm")
        self.assertEqual(
            best["best_at_90pct_inscope_retention"]["oos_abstain_recall"],
            0.7215,
        )
        self.assertEqual(
            best["best_at_85pct_inscope_retention"]["oos_abstain_recall"],
            0.7722,
        )
        self.assertEqual(
            audit["best_by_retention_target"]["0.90"]["signal"],
            "mean_top1_atlas_percentile_and_tm",
        )
        self.assertEqual(
            audit["best_by_retention_target"]["0.85"]["signal"],
            "harmonic_top1_raw_and_tm",
        )
        confounded_rows = best["confounded_rows"]
        self.assertEqual(
            [row["entry_id"] for row in confounded_rows],
            ["m_csa:30", "m_csa:31", "m_csa:80", "m_csa:191", "m_csa:267", "m_csa:448"],
        )
        self.assertEqual(
            sum(1 for row in confounded_rows if row["abstained_at_best_signal_90pct"]),
            5,
        )

    def test_predicted_atlas_vs_fold_novelty_delta_current_counts(self) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_predicted_atlas_vs_fold_novelty_operating_grid_delta_"
                "current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "predicted_atlas_vs_fold_novelty_delta_ready_review_only",
        )
        self.assertEqual(audit["counts"]["shared_retention_targets"], 4)
        self.assertEqual(audit["counts"]["targets_with_oos_abstain_lift"], 4)
        self.assertEqual(audit["counts"]["targets_with_confounded_abstain_lift"], 4)
        self.assertEqual(audit["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            audit["target_90_summary"]["oos_abstain_recall_delta"],
            0.5444,
        )
        self.assertEqual(
            audit["target_90_summary"]["confounded_abstain_recall_delta"],
            0.5,
        )
        self.assertFalse(audit["guardrails"]["production_thresholds_changed"])

    def test_mechanism_feature_sidecar_schema_audit_current_counts(self) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_sidecar_schema_audit_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "mechanism_feature_sidecar_schema_passed_current702",
        )
        self.assertEqual(audit["counts"]["manifest_rows"], 702)
        self.assertEqual(audit["counts"]["active_site_rows"], 702)
        self.assertEqual(audit["counts"]["reaction_center_rows"], 702)
        self.assertEqual(audit["counts"]["active_site_status_counts"]["ok"], 656)
        self.assertEqual(
            audit["counts"]["reaction_center_status_counts"]["template_available"],
            232,
        )
        self.assertTrue(
            all(
                count == 0
                for count in audit["counts"]["critical_counts"].values()
            )
        )

    def test_mechanism_feature_row_specific_bond_change_schema_current_counts(
        self,
    ) -> None:
        schema = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_row_specific_bond_change_schema_current702_20260601.json"
        )

        self.assertEqual(
            schema["status"],
            "row_specific_bond_change_schema_staged_no_fit",
        )
        self.assertEqual(schema["counts"]["manifest_rows"], 702)
        self.assertEqual(schema["counts"]["reaction_template_rows"], 702)
        self.assertEqual(
            schema["counts"]["rows_requiring_row_specific_bond_change_evidence"],
            232,
        )
        self.assertEqual(
            schema["counts"]["row_status_counts"][
                "not_applicable_no_mechanism_fingerprint_oos_or_unlabeled"
            ],
            470,
        )
        self.assertIn(
            "electron_transfer",
            schema["schema_contract"]["allowed_event_types"],
        )
        self.assertFalse(schema["guardrails"]["model_weights_fit_or_refit"])

    def test_family_panel_high_value_glycyl_radical_readiness_packet(self) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_high_value_glycyl_radical_readiness_packet_current702_20260601.json"
        )

        self.assertEqual(
            packet["status"],
            "glycyl_radical_panel_ready_as_oos_boundary_review_only",
        )
        self.assertEqual(packet["counts"]["panel_rows"], 2)
        self.assertEqual(packet["counts"]["score_complete_rows"], 2)
        self.assertEqual(packet["counts"]["abstained_at_research_threshold"], 2)
        self.assertEqual(packet["counts"]["non_abstained_at_research_threshold"], 0)
        self.assertFalse(packet["panel_decision"]["promotion_or_import_ready"])
        self.assertEqual(
            {row["entry_id"] for row in packet["row_readiness"]},
            {"m_csa:30", "m_csa:31"},
        )
        self.assertTrue(packet["guardrails"]["review_only"])

    def test_source_free_locator_human_decision_matrix_current_counts(self) -> None:
        matrix = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_source_free_locator_human_decision_matrix_current702_20260601.json"
        )

        self.assertEqual(
            matrix["status"],
            "source_free_locator_human_decision_matrix_ready_review_only",
        )
        self.assertEqual(matrix["counts"]["blocked_rows_tracked"], 5)
        self.assertEqual(matrix["counts"]["decision_classes"], 4)
        self.assertEqual(matrix["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertEqual(
            matrix["recommended_decision_order"][0],
            "accession_equivalence_or_matching_coordinate_required",
        )
        first_class = matrix["decision_classes"][0]
        self.assertEqual(
            first_class["supporting_gate"]["matching_coordinate_scout_status"],
            "source_free_locator_matching_coordinate_scout_blocked_no_replacement_matches_review_only",
        )
        self.assertEqual(
            first_class["supporting_gate"]["matching_replacement_coordinates"],
            0,
        )
        self.assertFalse(
            first_class["supporting_gate"]["matching_coordinate_gate_cleared"]
        )
        second_class = matrix["decision_classes"][1]
        self.assertEqual(
            second_class["supporting_gate"][
                "glycoside_substrate_coordinate_scout_status"
            ],
            "source_free_locator_glycoside_substrate_coordinate_scout_blocked_no_substrate_like_local_coordinate_review_only",
        )
        self.assertEqual(
            second_class["supporting_gate"]["substrate_like_coordinate_candidates"],
            0,
        )
        self.assertFalse(
            second_class["supporting_gate"]["substrate_coordinate_gate_cleared"]
        )
        self.assertFalse(matrix["guardrails"]["locator_sidecars_created_or_copied"])
        self.assertFalse(matrix["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(matrix["guardrails"]["predicted_geometry_scores_created"])

    def test_row_specific_bond_change_feature_contract_gap_audit(self) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_row_specific_bond_change_feature_contract_gap_audit_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "row_specific_bond_change_gap_not_consumed_by_feature_contract",
        )
        self.assertEqual(audit["counts"]["feature_contract_rows"], 524)
        self.assertEqual(
            audit["counts"]["rows_requiring_row_specific_bond_change_evidence"],
            232,
        )
        self.assertEqual(audit["counts"]["unexpected_bond_change_feature_rows"], 0)
        self.assertEqual(audit["counts"]["heldout_feature_rows"], 0)
        self.assertEqual(audit["counts"]["strict_audit_critical_violation_total"], 0)
        self.assertFalse(audit["guardrails"]["model_weights_fit_or_refit"])

    def test_row_specific_bond_change_materialization_priority_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_row_specific_bond_change_materialization_priority_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "row_specific_bond_change_materialization_priority_ready_no_fit",
        )
        self.assertEqual(
            audit["counts"]["rows_requiring_row_specific_bond_change_evidence"],
            232,
        )
        self.assertEqual(
            audit["counts"]["priority_tier_counts"],
            {
                "P0_train_cal_feature_contract_gap": 171,
                "P1_in_distribution_not_feature_contract_ready": 13,
                "P2_heldout_final_only_evidence_gap": 48,
            },
        )
        self.assertEqual(audit["counts"]["train_cal_feature_contract_gap_rows"], 171)
        self.assertEqual(
            audit["counts"]["in_distribution_not_feature_contract_ready_rows"],
            13,
        )
        self.assertEqual(audit["counts"]["heldout_final_only_gap_rows"], 48)
        self.assertEqual(audit["counts"]["balanced_pilot_seed_rows"], 15)
        self.assertEqual(
            audit["counts"]["embedding_split_counts"],
            {"calibration": 35, "not_in_split_manifest": 61, "train": 136},
        )
        self.assertTrue(
            all(count == 0 for count in audit["counts"]["critical_counts"].values())
        )
        self.assertFalse(audit["guardrails"]["row_specific_source_evidence_materialized"])
        self.assertFalse(audit["guardrails"]["feature_contract_mutated"])
        self.assertFalse(audit["guardrails"]["model_weights_fit_or_refit"])
        self.assertEqual(
            {
                row["fingerprint_id"]
                for row in audit["balanced_pilot_seed_queue"]
            },
            {
                "flavin_dehydrogenase_reductase",
                "heme_peroxidase_oxidase",
                "metal_dependent_hydrolase",
                "plp_dependent_enzyme",
                "ser_his_acid_hydrolase",
            },
        )

    def test_row_specific_bond_change_p0_source_graph_readiness_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_row_specific_bond_change_p0_source_graph_readiness_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "p0_source_graph_context_ready_bond_events_not_structured",
        )
        self.assertEqual(audit["counts"]["balanced_p0_seed_rows"], 15)
        self.assertEqual(audit["counts"]["m_csa_entry_nodes_present"], 15)
        self.assertEqual(audit["counts"]["mechanism_text_present_rows"], 15)
        self.assertEqual(audit["counts"]["catalytic_residue_edges_present_rows"], 15)
        self.assertEqual(audit["counts"]["ec_mapping_present_rows"], 15)
        self.assertEqual(audit["counts"]["rhea_mapping_present_rows"], 11)
        self.assertEqual(audit["counts"]["structured_bond_change_ready_rows"], 0)
        self.assertEqual(audit["counts"]["manual_extraction_required_rows"], 15)
        self.assertEqual(
            audit["counts"]["blocker_counts"],
            {
                "rhea_reaction_mapping_missing": 4,
                "structured_bond_change_events_missing": 15,
            },
        )
        self.assertEqual(
            audit["counts"]["status_counts"],
            {"source_context_present_structured_bond_events_missing": 15},
        )
        self.assertFalse(audit["guardrails"]["row_specific_source_evidence_materialized"])
        self.assertFalse(audit["guardrails"]["feature_contract_mutated"])
        self.assertFalse(audit["guardrails"]["model_weights_fit_or_refit"])

    def test_row_specific_bond_change_p0_extraction_package_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_row_specific_bond_change_p0_extraction_work_package_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "p0_row_specific_bond_change_extraction_work_package_ready_manual_only",
        )
        self.assertEqual(audit["counts"]["p0_seed_rows"], 15)
        self.assertEqual(audit["counts"]["manual_extraction_rows"], 15)
        self.assertEqual(audit["counts"]["rows_with_rhea_targets"], 11)
        self.assertEqual(audit["counts"]["rows_requiring_rhea_lookup"], 4)
        self.assertEqual(audit["counts"]["rows_with_structured_bond_change_events_now"], 0)
        self.assertEqual(audit["counts"]["required_field_count"], 9)
        self.assertEqual(
            audit["counts"]["fingerprint_counts"],
            {
                "flavin_dehydrogenase_reductase": 3,
                "heme_peroxidase_oxidase": 3,
                "metal_dependent_hydrolase": 3,
                "plp_dependent_enzyme": 3,
                "ser_his_acid_hydrolase": 3,
            },
        )
        self.assertTrue(
            all(count == 0 for count in audit["counts"]["critical_counts"].values())
        )
        self.assertFalse(audit["guardrails"]["row_specific_source_evidence_materialized"])
        self.assertFalse(audit["guardrails"]["feature_contract_mutated"])
        self.assertTrue(audit["guardrails"]["manual_extraction_templates_only"])

    def test_row_specific_bond_change_p0_extraction_strict_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_row_specific_bond_change_p0_extraction_package_strict_audit_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "p0_extraction_work_package_strict_audit_passed",
        )
        self.assertEqual(audit["counts"]["extraction_rows"], 15)
        self.assertEqual(audit["counts"]["passed_template_only_rows"], 15)
        self.assertEqual(audit["counts"]["rows_with_non_null_template_values"], 0)
        self.assertEqual(audit["counts"]["required_field_count"], 9)
        self.assertEqual(audit["counts"]["violation_counts"], {})
        self.assertEqual(audit["counts"]["strict_audit_critical_violation_total"], 0)
        self.assertTrue(
            all(count == 0 for count in audit["counts"]["critical_counts"].values())
        )
        self.assertFalse(audit["guardrails"]["row_specific_source_evidence_materialized"])
        self.assertFalse(audit["guardrails"]["feature_contract_mutated"])
        self.assertTrue(audit["guardrails"]["strict_audit_only"])

    def test_row_specific_bond_change_p0_extraction_worksheet_current_counts(
        self,
    ) -> None:
        worksheet_path = (
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_row_specific_bond_change_p0_extraction_worksheet_current702_20260601.tsv"
        )
        with worksheet_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))

        self.assertEqual(len(rows), 15)
        self.assertEqual(rows[0]["entry_id"], "m_csa:5")
        self.assertEqual(rows[-1]["entry_id"], "m_csa:186")
        self.assertEqual(
            {row["fingerprint_id"] for row in rows},
            {
                "flavin_dehydrogenase_reductase",
                "heme_peroxidase_oxidase",
                "metal_dependent_hydrolase",
                "plp_dependent_enzyme",
                "ser_his_acid_hydrolase",
            },
        )
        self.assertEqual(
            sum(1 for row in rows if row["rhea_lookup_required"] == "true"),
            4,
        )
        self.assertTrue(all(row["source_record_id"] == "" for row in rows))
        self.assertTrue(
            all(row["row_specific_bond_change_events"] == "" for row in rows)
        )
        self.assertTrue(all(row["review_status"] == "" for row in rows))

    def test_row_specific_bond_change_p0_source_evidence_schema_current_counts(
        self,
    ) -> None:
        schema = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_schema_current702_20260601.json"
        )

        self.assertEqual(schema["status"], "p0_source_evidence_sidecar_schema_staged_no_fit")
        self.assertEqual(schema["counts"]["p0_worksheet_rows"], 15)
        self.assertEqual(schema["counts"]["required_row_field_count"], 12)
        self.assertEqual(schema["counts"]["required_event_field_count"], 6)
        self.assertEqual(schema["counts"]["required_mapping_field_count"], 4)
        self.assertEqual(schema["counts"]["source_values_materialized_now"], 0)
        self.assertTrue(
            all(count == 0 for count in schema["counts"]["critical_counts"].values())
        )
        self.assertFalse(
            schema["guardrails"]["row_specific_source_evidence_materialized"]
        )
        self.assertFalse(schema["guardrails"]["feature_contract_mutated"])
        self.assertIn(
            "geometry_score",
            schema["sidecar_schema"]["forbidden_predictive_fields"],
        )

    def test_row_specific_bond_change_p0_source_evidence_sidecar_current_counts(
        self,
    ) -> None:
        sidecar = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_current702_20260601.json"
        )

        self.assertEqual(
            sidecar["status"],
            "p0_source_evidence_sidecar_all_train_cal_p0_rows_approved",
        )
        self.assertEqual(sidecar["counts"]["worksheet_rows"], 15)
        self.assertEqual(sidecar["counts"]["sidecar_rows"], 15)
        self.assertEqual(sidecar["counts"]["rows_with_source_spans"], 15)
        self.assertEqual(sidecar["counts"]["rows_with_draft_bond_change_events"], 15)
        self.assertEqual(sidecar["counts"]["rows_with_rhea_equations"], 12)
        self.assertEqual(sidecar["counts"]["rows_missing_rhea_equations"], 3)
        self.assertEqual(sidecar["counts"]["approved_rows"], 15)
        self.assertEqual(sidecar["counts"]["m_csa_only_reviewer_approved_rows"], 3)
        self.assertEqual(sidecar["counts"]["rhea_backed_reviewer_approved_rows"], 12)
        self.assertEqual(sidecar["counts"]["feature_contract_consumable_rows"], 15)
        self.assertEqual(
            sidecar["counts"]["review_status_counts"],
            {"approved": 15},
        )
        self.assertFalse(sidecar["guardrails"]["feature_contract_mutated"])
        self.assertFalse(sidecar["guardrails"]["feature_contract_refresh_allowed"])
        self.assertTrue(sidecar["guardrails"]["draft_source_evidence_not_training_input"])
        self.assertTrue(
            sidecar["guardrails"][
                "m_csa_source_evidence_train_cal_only_requires_split_filter"
            ]
        )
        self.assertTrue(
            sidecar["guardrails"]["heldout_m_csa_rows_excluded_from_training_required"]
        )

    def test_row_specific_bond_change_p0_source_evidence_sidecar_strict_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_strict_audit_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "p0_source_evidence_sidecar_strict_audit_passed_reviewed_consumable",
        )
        self.assertEqual(audit["counts"]["worksheet_rows"], 15)
        self.assertEqual(audit["counts"]["sidecar_rows"], 15)
        self.assertEqual(audit["counts"]["draft_rows"], 0)
        self.assertEqual(audit["counts"]["approved_rows"], 15)
        self.assertEqual(audit["counts"]["feature_contract_consumable_rows"], 15)
        self.assertEqual(audit["counts"]["model_training_allowed_rows"], 0)
        self.assertEqual(audit["counts"]["rows_with_events"], 15)
        self.assertEqual(audit["counts"]["rows_with_source_spans"], 15)
        self.assertEqual(audit["counts"]["strict_audit_critical_violation_total"], 0)
        self.assertEqual(audit["counts"]["violation_counts"], {})
        self.assertFalse(audit["counts"]["feature_contract_refresh_allowed"])
        self.assertTrue(
            all(count == 0 for count in audit["counts"]["critical_counts"].values())
        )
        self.assertFalse(audit["guardrails"]["feature_contract_mutated"])
        self.assertFalse(audit["guardrails"]["feature_contract_refresh_allowed"])

    def test_row_specific_bond_change_p0_source_evidence_review_queue_current_counts(
        self,
    ) -> None:
        queue = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_review_queue_current702_20260601.json"
        )

        self.assertEqual(
            queue["status"],
            "p0_source_evidence_review_queue_ready_manual_only",
        )
        self.assertEqual(queue["counts"]["sidecar_rows"], 15)
        self.assertEqual(queue["counts"]["queue_rows"], 15)
        self.assertEqual(
            queue["counts"]["category_counts"],
            {
                "approved_m_csa_only_source_evidence": 3,
                "approved_rhea_backed_source_evidence": 12,
            },
        )
        self.assertEqual(queue["counts"]["approved_rows"], 15)
        self.assertEqual(queue["counts"]["feature_contract_consumable_rows"], 15)
        self.assertEqual(queue["counts"]["approved_feature_contract_consumable_rows"], 15)
        self.assertEqual(queue["counts"]["unreviewed_feature_contract_consumable_rows"], 0)
        self.assertEqual(queue["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            [row["entry_id"] for row in queue["queue_rows"][:3]],
            ["m_csa:102", "m_csa:124", "m_csa:133"],
        )
        approved_queue_rows = [
            row
            for row in queue["queue_rows"]
            if row["review_category"] == "approved_m_csa_only_source_evidence"
        ]
        self.assertEqual(
            {row["entry_id"] for row in approved_queue_rows},
            {"m_csa:5", "m_csa:11", "m_csa:169"},
        )
        self.assertTrue(
            all(count == 0 for count in queue["counts"]["critical_counts"].values())
        )
        self.assertFalse(queue["guardrails"]["feature_contract_mutated"])
        self.assertFalse(queue["guardrails"]["feature_contract_refresh_allowed"])

    def test_row_specific_bond_change_p0_rhea_lookup_resolution_current_counts(
        self,
    ) -> None:
        resolution = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_rhea_lookup_resolution_current702_20260601.json"
            )
        )

        self.assertEqual(
            resolution["status"],
            "p0_rhea_lookup_resolution_unresolved_review_only",
        )
        self.assertEqual(resolution["counts"]["lookup_rows"], 0)
        self.assertEqual(resolution["counts"]["resolved_rows"], 0)
        self.assertEqual(resolution["counts"]["resolved_by_accession_rows"], 0)
        self.assertEqual(resolution["counts"]["resolved_by_exact_ec_rows"], 0)
        self.assertEqual(resolution["counts"]["unresolved_rows"], 0)
        self.assertEqual(resolution["row_resolutions"], [])
        self.assertTrue(resolution["guardrails"]["source_fetch_performed"])
        self.assertFalse(resolution["guardrails"]["feature_contract_refresh_allowed"])

    def test_row_specific_bond_change_p0_rhea_lookup_manifest_current_counts(
        self,
    ) -> None:
        manifest = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_row_specific_bond_change_p0_rhea_lookup_manifest_current702_20260601.json"
        )

        self.assertEqual(
            manifest["status"],
            "p0_rhea_lookup_manifest_ready_manual_only",
        )
        self.assertEqual(manifest["counts"]["review_queue_rows"], 15)
        self.assertEqual(manifest["counts"]["rhea_lookup_rows"], 0)
        self.assertEqual(manifest["counts"]["rows_with_ec_targets"], 0)
        self.assertEqual(manifest["counts"]["lookup_target_count"], 0)
        self.assertEqual(manifest["counts"]["critical_violation_total"], 0)
        self.assertEqual(manifest["lookup_rows"], [])
        self.assertTrue(
            all(count == 0 for count in manifest["counts"]["critical_counts"].values())
        )
        self.assertFalse(manifest["guardrails"]["source_fetch_performed"])
        self.assertFalse(manifest["guardrails"]["feature_contract_refresh_allowed"])

    def test_row_specific_bond_change_p0_rhea_resolution_consumption_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_rhea_resolution_consumption_audit_current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "p0_rhea_resolution_consumption_audit_passed_review_only",
        )
        self.assertEqual(audit["counts"]["resolution_rows"], 0)
        self.assertEqual(audit["counts"]["resolved_rows"], 0)
        self.assertEqual(audit["counts"]["unresolved_rows"], 0)
        self.assertEqual(audit["counts"]["reviewer_approved_m_csa_only_rows"], 0)
        self.assertEqual(audit["counts"]["remaining_lookup_manifest_rows"], 0)
        self.assertEqual(audit["counts"]["feature_contract_consumable_rows"], 0)
        self.assertEqual(audit["counts"]["model_training_allowed_rows"], 0)
        self.assertEqual(audit["counts"]["critical_violation_total"], 0)
        self.assertEqual(audit["row_audits"], [])
        self.assertFalse(audit["guardrails"]["feature_contract_refresh_allowed"])

    def test_row_specific_bond_change_p0_rhea_unresolved_official_source_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_rhea_unresolved_official_source_audit_current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "p0_rhea_unresolved_official_source_audit_ready_review_only",
        )
        self.assertEqual(audit["counts"]["manifest_rows_audited"], 0)
        self.assertEqual(audit["counts"]["rhea_query_attempts"], 0)
        self.assertEqual(audit["counts"]["rows_with_official_rhea_evidence_found"], 0)
        self.assertEqual(audit["counts"]["rows_with_uniprot_matching_ec_activity"], 0)
        self.assertEqual(audit["counts"]["unresolved_after_official_source_check"], 0)
        self.assertEqual(audit["counts"]["reviewer_decision_required_rows"], 0)
        self.assertEqual(audit["counts"]["feature_contract_consumable_rows"], 0)
        self.assertEqual(audit["row_audits"], [])
        self.assertFalse(audit["guardrails"]["feature_contract_refresh_allowed"])

    def test_row_specific_bond_change_p0_reviewer_decision_matrix_current_counts(
        self,
    ) -> None:
        matrix = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_reviewer_decision_matrix_current702_20260601.json"
            )
        )

        self.assertEqual(
            matrix["status"],
            "p0_reviewer_decision_matrix_ready_review_only",
        )
        self.assertEqual(matrix["counts"]["decision_rows"], 0)
        self.assertEqual(matrix["counts"]["decision_options_per_row"], 3)
        self.assertEqual(matrix["counts"]["rows_with_uniprot_matching_ec_activity"], 0)
        self.assertEqual(matrix["counts"]["rows_with_existing_reviewer_id"], 0)
        self.assertEqual(matrix["counts"]["copy_ready_approved_decisions"], 0)
        self.assertEqual(matrix["counts"]["feature_contract_consumable_rows"], 0)
        self.assertEqual(matrix["decision_rows"], [])
        self.assertFalse(matrix["guardrails"]["feature_contract_refresh_allowed"])
        self.assertFalse(
            matrix["guardrails"]["reviewer_decision_recorded_by_this_artifact"]
        )
        self.assertFalse(matrix["guardrails"]["reviewer_decision_recorded_by_sidecar"])

    def test_row_specific_bond_change_p0_feature_readiness_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_feature_readiness_audit_current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "p0_feature_readiness_audit_ready_for_feature_contract_refresh",
        )
        self.assertEqual(audit["counts"]["sidecar_rows"], 15)
        self.assertEqual(audit["counts"]["structurally_ready_draft_rows"], 15)
        self.assertEqual(audit["counts"]["approved_consumable_rows"], 15)
        self.assertEqual(
            audit["counts"]["approved_event_type_counts"],
            {
                "bond_broken": 8,
                "bond_formed": 8,
                "bond_order_changed": 9,
                "electron_transfer": 10,
                "proton_transfer": 16,
            },
        )
        self.assertEqual(audit["counts"]["rows_with_bond_change_event"], 13)
        self.assertEqual(audit["counts"]["rows_with_proton_transfer_event"], 9)
        self.assertEqual(audit["counts"]["rows_with_electron_transfer_event"], 7)
        self.assertEqual(
            audit["counts"]["draft_event_type_counts"],
            {
                "bond_broken": 8,
                "bond_formed": 8,
                "bond_order_changed": 9,
                "electron_transfer": 10,
                "proton_transfer": 16,
            },
        )
        self.assertEqual(audit["counts"]["critical_violation_total"], 0)
        self.assertTrue(audit["counts"]["feature_contract_refresh_allowed"])
        self.assertFalse(audit["guardrails"]["feature_contract_mutated"])

    def test_row_specific_bond_change_p0_refresh_blocker_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_refresh_blocker_audit_current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "p0_no_template_feature_refresh_allowed_after_review_gate",
        )
        self.assertTrue(
            audit["decision"]["automation_feature_contract_refresh_allowed"]
        )
        self.assertTrue(
            audit["decision"]["partial_train_cal_feature_materialization_allowed"]
        )
        self.assertEqual(audit["counts"]["sidecar_rows"], 15)
        self.assertEqual(audit["counts"]["structurally_ready_draft_rows"], 15)
        self.assertEqual(audit["counts"]["approved_consumable_rows"], 15)
        self.assertEqual(audit["counts"]["reviewer_decision_required_rows"], 0)
        self.assertEqual(audit["counts"]["remaining_reviewer_decision_required_rows"], 0)
        self.assertEqual(audit["counts"]["reviewer_decision_rows"], 0)
        self.assertEqual(audit["counts"]["copy_ready_approved_decisions"], 0)
        self.assertEqual(audit["counts"]["rows_with_existing_reviewer_id"], 0)
        self.assertEqual(audit["counts"]["rhea_unresolved_rows"], 0)
        self.assertEqual(
            audit["unresolved_decision_rows"],
            [],
        )
        self.assertFalse(audit["guardrails"]["feature_contract_mutated"])

    def test_row_specific_bond_change_p0_train_cal_feature_sidecar_current_counts(
        self,
    ) -> None:
        sidecar = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_train_cal_feature_sidecar_current702_20260601.json"
            )
        )

        self.assertEqual(
            sidecar["status"],
            "p0_train_cal_row_specific_feature_sidecar_ready_partial_no_fit",
        )
        self.assertEqual(sidecar["counts"]["source_sidecar_rows"], 15)
        self.assertEqual(sidecar["counts"]["approved_source_rows"], 15)
        self.assertEqual(sidecar["counts"]["approved_consumable_rows"], 15)
        self.assertEqual(sidecar["counts"]["materialized_feature_rows"], 15)
        self.assertEqual(sidecar["counts"]["train_rows"], 11)
        self.assertEqual(sidecar["counts"]["calibration_rows"], 4)
        self.assertEqual(sidecar["counts"]["draft_rows_excluded"], 0)
        self.assertEqual(sidecar["counts"]["heldout_approved_rows_excluded"], 0)
        self.assertEqual(
            sidecar["counts"]["materialized_event_type_counts"],
            {
                "bond_broken": 8,
                "bond_formed": 8,
                "bond_order_changed": 9,
                "electron_transfer": 10,
                "proton_transfer": 16,
            },
        )
        self.assertEqual(sidecar["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            [row["entry_id"] for row in sidecar["feature_rows"]],
            [
                "m_csa:5",
                "m_csa:6",
                "m_csa:11",
                "m_csa:15",
                "m_csa:16",
                "m_csa:37",
                "m_csa:66",
                "m_csa:68",
                "m_csa:94",
                "m_csa:102",
                "m_csa:124",
                "m_csa:133",
                "m_csa:147",
                "m_csa:169",
                "m_csa:186",
            ],
        )
        self.assertTrue(
            sidecar["decision"]["partial_train_cal_feature_materialization_ready"]
        )
        self.assertTrue(
            sidecar["decision"][
                "full_no_template_centroid_or_residual_rerun_ready"
            ]
        )
        feature_rows_text = json.dumps(sidecar["feature_rows"])
        self.assertNotIn("span_text", feature_rows_text)
        self.assertNotIn("reviewer_id", feature_rows_text)
        self.assertFalse(sidecar["guardrails"]["model_weights_fit_or_refit"])
        self.assertFalse(
            sidecar["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )

    def test_row_specific_bond_change_p0_train_cal_feature_guardrail_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_train_cal_feature_guardrail_audit_current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "p0_train_cal_feature_guardrail_audit_passed_partial_no_fit",
        )
        self.assertEqual(audit["counts"]["feature_rows"], 15)
        self.assertEqual(audit["counts"]["train_rows"], 11)
        self.assertEqual(audit["counts"]["calibration_rows"], 4)
        self.assertEqual(
            audit["counts"]["feature_value_type_counts"],
            {"bool": 60, "int": 195},
        )
        self.assertEqual(audit["counts"]["critical_violation_total"], 0)
        self.assertTrue(
            audit["decision"]["partial_feature_surface_guardrail_passed"]
        )
        self.assertTrue(
            audit["decision"]["safe_to_use_as_partial_train_feature_surface"]
        )
        self.assertTrue(audit["decision"]["safe_to_run_no_template_methods_now"])
        self.assertTrue(
            audit["decision"]["full_no_template_rerun_ready_from_sidecar"]
        )
        self.assertFalse(audit["guardrails"]["model_weights_fit_or_refit"])
        self.assertFalse(
            audit["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )

    def test_row_specific_bond_change_p0_train_cal_coverage_gap_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_train_cal_coverage_gap_current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "p0_train_cal_feature_coverage_gap_ready_review_queue",
        )
        self.assertEqual(audit["counts"]["materialized_feature_rows"], 15)
        self.assertEqual(audit["counts"]["materialized_train_rows"], 11)
        self.assertEqual(audit["counts"]["materialized_calibration_rows"], 4)
        self.assertEqual(audit["counts"]["draft_train_cal_review_rows"], 0)
        self.assertEqual(audit["counts"]["draft_train_rows"], 0)
        self.assertEqual(audit["counts"]["draft_calibration_rows"], 0)
        self.assertEqual(audit["counts"]["excluded_draft_rows"], 0)
        self.assertEqual(
            audit["counts"]["priority_class_counts"],
            {},
        )
        self.assertEqual(audit["counts"]["missing_materialized_event_type_counts"], {})
        self.assertEqual(audit["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            audit["decision"]["next_review_gate_entry_ids"],
            [],
        )
        self.assertFalse(audit["decision"]["rerun_blocked_by_calibration_coverage"])
        self.assertTrue(audit["decision"]["full_no_template_rerun_ready"])
        self.assertEqual(audit["review_priority_rows"], [])
        self.assertFalse(audit["guardrails"]["model_weights_fit_or_refit"])
        self.assertFalse(
            audit["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )

    def test_row_specific_bond_change_p0_calibration_review_packet_current_counts(
        self,
    ) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_calibration_review_packet_current702_20260601.json"
            )
        )

        self.assertEqual(
            packet["status"],
            "p0_calibration_review_packet_ready_manual_only",
        )
        self.assertEqual(packet["counts"]["packet_rows"], 0)
        self.assertEqual(packet["counts"]["calibration_rows"], 0)
        self.assertEqual(packet["counts"]["rows_with_unmaterialized_event_type"], 0)
        self.assertEqual(packet["counts"]["event_rows"], 0)
        self.assertEqual(packet["counts"]["critical_violation_total"], 0)
        self.assertEqual(packet["packet_rows"], [])
        self.assertFalse(packet["guardrails"]["model_weights_fit_or_refit"])
        self.assertFalse(
            packet["guardrails"]["reviewer_decisions_recorded_by_this_artifact"]
        )

    def test_row_specific_bond_change_p0_pending_rewrite_blocker_current_counts(
        self,
    ) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_pending_rewrite_blocker_current702_20260601.json"
            )
        )

        self.assertEqual(
            packet["status"],
            "p0_pending_rewrite_blocker_cleared_ready_for_no_template_rerun",
        )
        self.assertEqual(packet["counts"]["pending_rewrite_rows"], 0)
        self.assertEqual(packet["counts"]["event_rows"], 0)
        self.assertEqual(packet["counts"]["blocked_event_rows"], 0)
        self.assertEqual(packet["counts"]["blocked_event_type_counts"], {})
        self.assertEqual(packet["counts"]["blocker_counts"], {})
        self.assertEqual(packet["decision"]["next_gate_entry_ids"], [])
        self.assertTrue(packet["decision"]["full_no_template_rerun_ready"])
        self.assertIsNone(packet["decision"]["reason_not_ready"])
        self.assertEqual(packet["counts"]["approved_materialized_feature_rows"], 15)
        self.assertEqual(packet["counts"]["approved_materialized_train_rows"], 11)
        self.assertEqual(packet["counts"]["approved_materialized_calibration_rows"], 4)
        self.assertEqual(packet["counts"]["critical_violation_total"], 0)
        self.assertFalse(packet["guardrails"]["model_weights_fit_or_refit"])

    def test_row_specific_bond_change_p0_no_template_rerun_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_no_template_rerun_current702_20260602.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "p0_row_specific_no_template_train_cal_scored_oos_blocked",
        )
        self.assertEqual(audit["counts"]["feature_rows"], 15)
        self.assertEqual(audit["counts"]["train_rows"], 11)
        self.assertEqual(audit["counts"]["calibration_rows"], 4)
        self.assertEqual(audit["counts"]["calibration_primary_rows"], 4)
        self.assertEqual(audit["counts"]["calibration_oos_rows"], 0)
        self.assertEqual(audit["counts"]["feature_dimensions"], 17)
        self.assertEqual(audit["counts"]["primary_centroid_labels"], 5)
        self.assertTrue(audit["decision"]["centroid_train_cal_scored"])
        self.assertTrue(audit["decision"]["residual_train_cal_scored"])
        self.assertFalse(
            audit["decision"]["known_vs_novel_operating_point_evaluable"]
        )
        self.assertFalse(audit["decision"]["heldout_read_once_performed"])
        self.assertEqual(
            audit["centroid_variant"]["calibration_summary"]["primary_rows"],
            4,
        )
        self.assertIsNone(
            audit["centroid_variant"]["calibration_summary"]["auc_primary_vs_oos"]
        )
        self.assertIsNone(
            audit["residual_variant"]["calibration_summary"]["auc_oos_gt_primary"]
        )
        self.assertFalse(
            audit["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )
        self.assertTrue(audit["guardrails"]["m_csa_row_specific_features_train_cal_only"])

    def test_row_specific_bond_change_p0_oos_calibration_gap_current_counts(
        self,
    ) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_calibration_gap_current702_20260602.json"
            )
        )

        self.assertEqual(
            packet["status"], "p0_oos_calibration_gap_ready_review_packet"
        )
        self.assertEqual(packet["counts"]["candidate_rows"], 353)
        self.assertEqual(packet["counts"]["candidate_calibration_rows"], 71)
        self.assertEqual(packet["counts"]["candidate_train_rows"], 282)
        self.assertEqual(packet["counts"]["packet_rows"], 30)
        self.assertEqual(packet["counts"]["packet_calibration_rows"], 30)
        self.assertEqual(packet["counts"]["packet_train_rows"], 0)
        self.assertEqual(packet["counts"]["approved_p0_rows_excluded"], 15)
        self.assertEqual(packet["packet_rows"][0]["entry_id"], "m_csa:2")
        self.assertEqual(
            packet["packet_rows"][0]["assigned_embedding_split"], "calibration"
        )
        self.assertFalse(packet["decision"]["feature_consumption_allowed_now"])
        self.assertTrue(
            packet["decision"]["fills_no_template_oos_operating_point_if_approved"]
        )
        self.assertFalse(packet["guardrails"]["heldout_rows_in_packet"])
        self.assertFalse(
            packet["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )

    def test_row_specific_bond_change_p0_oos_calibration_extraction_work_package_current_counts(
        self,
    ) -> None:
        package = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_calibration_extraction_work_package_current702_20260602.json"
            )
        )

        self.assertEqual(
            package["status"],
            "p0_oos_calibration_extraction_work_package_ready_manual_only",
        )
        self.assertEqual(package["counts"]["gap_packet_rows"], 30)
        self.assertEqual(package["counts"]["manual_extraction_rows"], 30)
        self.assertEqual(package["counts"]["calibration_rows"], 30)
        self.assertEqual(package["counts"]["train_rows"], 0)
        self.assertEqual(package["counts"]["rows_with_accession"], 30)
        self.assertEqual(
            package["counts"]["rows_with_active_site_role_template"], 30
        )
        self.assertEqual(package["counts"]["required_field_count"], 9)
        self.assertEqual(package["counts"]["critical_violation_total"], 0)
        self.assertEqual(package["counts"]["critical_counts"], {})
        self.assertEqual(package["extraction_rows"][0]["entry_id"], "m_csa:2")
        self.assertEqual(
            package["extraction_rows"][0]["assigned_embedding_split"],
            "calibration",
        )
        self.assertIn(
            "source_record_id",
            package["extraction_rows"][0]["manual_extraction_template"],
        )
        self.assertFalse(
            package["guardrails"]["feature_contract_consumption_allowed_now"]
        )
        self.assertFalse(
            package["guardrails"]["row_specific_source_evidence_materialized"]
        )

    def test_row_specific_bond_change_p0_oos_calibration_extraction_work_package_strict_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_calibration_extraction_work_package_strict_audit_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "p0_oos_calibration_extraction_work_package_strict_audit_passed",
        )
        self.assertEqual(audit["counts"]["manual_extraction_rows"], 30)
        self.assertEqual(audit["counts"]["required_field_count"], 9)
        self.assertEqual(audit["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            audit["counts"]["critical_counts"],
            {
                "heldout_rows": 0,
                "missing_manual_template_fields": 0,
                "non_oos_rows": 0,
                "rows_allowed_for_feature_contract_consumption_now": 0,
                "rows_allowed_for_model_training_now": 0,
                "rows_not_train_or_calibration": 0,
                "rows_with_materialized_source_evidence_status": 0,
            },
        )
        self.assertTrue(audit["decision"]["manual_extraction_package_passed"])
        self.assertFalse(audit["decision"]["feature_consumption_allowed_now"])
        self.assertTrue(audit["guardrails"]["validation_only"])
        self.assertFalse(audit["guardrails"]["feature_contract_mutated"])

    def test_row_specific_bond_change_p0_oos_approved_sidecar_current_counts(
        self,
    ) -> None:
        sidecar = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_calibration_approved_source_evidence_sidecar_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            sidecar["status"],
            "p0_oos_calibration_approved_source_evidence_sidecar_ready",
        )
        self.assertEqual(sidecar["counts"]["selected_oos_rows"], 28)
        self.assertEqual(sidecar["counts"]["approved_rows"], 28)
        self.assertEqual(sidecar["counts"]["calibration_rows"], 28)
        self.assertEqual(sidecar["counts"]["rows_with_rhea_equations"], 28)
        self.assertEqual(sidecar["counts"]["skipped_candidate_rows"], 2)
        self.assertEqual(sidecar["counts"]["model_training_allowed_rows"], 0)
        self.assertEqual(
            [row["entry_id"] for row in sidecar["sidecar_rows"]],
            [
                "m_csa:2",
                "m_csa:17",
                "m_csa:23",
                "m_csa:25",
                "m_csa:40",
                "m_csa:49",
                "m_csa:59",
                "m_csa:70",
                "m_csa:78",
                "m_csa:85",
                "m_csa:101",
                "m_csa:149",
                "m_csa:154",
                "m_csa:194",
                "m_csa:221",
                "m_csa:222",
                "m_csa:224",
                "m_csa:241",
                "m_csa:246",
                "m_csa:253",
                "m_csa:256",
                "m_csa:263",
                "m_csa:273",
                "m_csa:287",
                "m_csa:292",
                "m_csa:312",
                "m_csa:317",
                "m_csa:318",
            ],
        )
        self.assertEqual(
            [row["entry_id"] for row in sidecar["skipped_rows"]],
            ["m_csa:76", "m_csa:202"],
        )
        self.assertTrue(
            all(
                row["allowed_for_feature_contract_consumption_now"]
                for row in sidecar["sidecar_rows"]
            )
        )

    def test_row_specific_bond_change_p0_oos_approved_sidecar_strict_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_calibration_approved_source_evidence_sidecar_strict_audit_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "p0_oos_calibration_approved_source_evidence_sidecar_strict_audit_passed",
        )
        self.assertEqual(audit["counts"]["sidecar_rows"], 28)
        self.assertEqual(audit["counts"]["approved_rows"], 28)
        self.assertEqual(
            audit["counts"]["strict_audit_critical_violation_total"], 0
        )
        self.assertEqual(audit["counts"]["violation_counts"], {})
        self.assertTrue(
            all(row["status"] == "passed" for row in audit["row_audits"])
        )

    def test_row_specific_bond_change_p0_oos_augmented_no_template_current_counts(
        self,
    ) -> None:
        feature_sidecar = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_train_cal_feature_sidecar_current702_20260602.json"
            )
        )
        guardrail = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_train_cal_feature_guardrail_audit_"
                "current702_20260602.json"
            )
        )
        rerun = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_no_template_rerun_current702_20260602.json"
            )
        )

        self.assertEqual(
            feature_sidecar["status"],
            "p0_oos_augmented_train_cal_row_specific_feature_sidecar_ready_no_fit",
        )
        self.assertEqual(feature_sidecar["counts"]["materialized_feature_rows"], 43)
        self.assertEqual(feature_sidecar["counts"]["train_rows"], 11)
        self.assertEqual(feature_sidecar["counts"]["calibration_rows"], 32)
        self.assertEqual(
            feature_sidecar["counts"]["materialized_label_type_counts"],
            {"out_of_scope": 28, "seed_fingerprint": 15},
        )
        self.assertEqual(
            guardrail["status"],
            "p0_oos_augmented_train_cal_feature_guardrail_audit_passed",
        )
        self.assertEqual(guardrail["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            rerun["status"],
            "p0_row_specific_no_template_train_cal_operating_point_ready",
        )
        self.assertTrue(
            rerun["decision"]["known_vs_novel_operating_point_evaluable"]
        )
        self.assertEqual(rerun["counts"]["calibration_primary_rows"], 4)
        self.assertEqual(rerun["counts"]["calibration_oos_rows"], 28)
        self.assertEqual(
            rerun["centroid_variant"]["calibration_selected_similarity_threshold"][
                "oos_abstain_recall"
            ],
            0.5,
        )
        self.assertEqual(
            rerun["residual_variant"]["calibration_selected_residual_threshold"][
                "oos_abstain_recall"
            ],
            0.5,
        )

    def test_row_specific_bond_change_p0_oos_augmented_operating_point_contract_current_counts(
        self,
    ) -> None:
        contract = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_operating_point_contract_current702_20260602.json"
            )
        )

        self.assertEqual(
            contract["status"],
            "p0_oos_augmented_operating_point_contract_ready_calibration_only",
        )
        self.assertTrue(
            contract["decision"]["known_vs_novel_operating_point_evaluable"]
        )
        self.assertTrue(
            contract["decision"]["residual_calibration_contract_ready"]
        )
        self.assertFalse(contract["decision"]["heldout_read_once_performed"])
        self.assertEqual(contract["counts"]["calibration_oos_rows"], 28)
        self.assertEqual(contract["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            contract["calibration_contract"]["residual_distance"]["threshold"],
            3.21469422,
        )
        self.assertEqual(
            contract["calibration_contract"]["residual_distance"][
                "primary_retain_recall"
            ],
            1.0,
        )
        self.assertEqual(
            contract["calibration_contract"]["residual_distance"][
                "oos_abstain_recall"
            ],
            0.5,
        )
        self.assertFalse(
            contract["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )

    def test_row_specific_bond_change_p0_oos_augmented_calibration_error_analysis_current_counts(
        self,
    ) -> None:
        analysis = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_calibration_error_analysis_current702_20260602.json"
            )
        )

        self.assertEqual(
            analysis["status"],
            "p0_oos_augmented_calibration_error_analysis_ready",
        )
        self.assertEqual(analysis["counts"]["calibration_oos_rows"], 28)
        self.assertEqual(analysis["counts"]["calibration_primary_rows"], 4)
        self.assertEqual(
            analysis["counts"]["outcome_counts"],
            {
                "oos_abstained": 14,
                "oos_non_abstained": 14,
                "primary_retained": 4,
            },
        )
        self.assertEqual(analysis["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            analysis["oos_non_abstained_rows"][0]["entry_id"], "m_csa:101"
        )
        self.assertEqual(
            analysis["oos_abstained_rows"][0]["entry_id"], "m_csa:292"
        )
        self.assertEqual(
            analysis["counts"]["retained_oos_nearest_primary_counts"],
            {
                "flavin_dehydrogenase_reductase": 1,
                "heme_peroxidase_oxidase": 4,
                "metal_dependent_hydrolase": 4,
                "ser_his_acid_hydrolase": 5,
            },
        )
        self.assertEqual(len(analysis["retained_oos_failure_set"]), 14)
        self.assertEqual(
            analysis["counts"]["retained_oos_priority_counts"],
            {
                "borderline_contract_miss": 2,
                "near_contract_miss": 3,
                "strong_primary_alias": 9,
            },
        )
        self.assertEqual(
            analysis["retained_oos_failure_set"][0],
            {
                "entry_id": "m_csa:273",
                "event_profile": "events=4;bond=1;proton=3;electron=0",
                "nearest_primary_label": "metal_dependent_hydrolase",
                "priority": "borderline_contract_miss",
                "residual_margin_below_threshold": 0.04711835,
            },
        )
        self.assertFalse(analysis["guardrails"]["heldout_rows_evaluated"])

    def test_row_specific_bond_change_p0_oos_augmented_retained_oos_feature_target_current_counts(
        self,
    ) -> None:
        target = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_retained_oos_feature_target_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            target["status"],
            "p0_oos_augmented_retained_oos_feature_target_ready",
        )
        self.assertEqual(target["counts"]["retained_oos_failure_rows"], 14)
        self.assertEqual(
            target["counts"]["priority_retained_oos_failure_rows"], 5
        )
        self.assertEqual(target["counts"]["feature_families_scanned"], 14)
        self.assertEqual(target["counts"]["candidate_feature_tokens_scanned"], 426)
        self.assertEqual(target["counts"]["ready_candidate_feature_families"], 8)
        self.assertEqual(target["counts"]["critical_violation_total"], 0)
        self.assertTrue(
            target["decision"]["feature_family_ready_for_expanded_sidecar"]
        )
        self.assertEqual(
            target["decision"]["ready_candidate_feature_families"][:4],
            [
                "event_residue_code",
                "event_residue_code_count",
                "event_residue_role_count",
                "residue_role_count",
            ],
        )
        self.assertFalse(target["guardrails"]["heldout_rows_evaluated"])

    def test_row_specific_bond_change_p0_oos_augmented_expanded_surface_current_counts(
        self,
    ) -> None:
        sidecar = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_expanded_train_cal_feature_sidecar_"
                "current702_20260602.json"
            )
        )
        guardrail = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_expanded_train_cal_feature_guardrail_audit_"
                "current702_20260602.json"
            )
        )
        rerun = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_expanded_no_template_rerun_"
                "current702_20260602.json"
            )
        )
        comparison = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_expanded_calibration_comparison_"
                "current702_20260602.json"
            )
        )
        ablation = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_expanded_family_ablation_"
                "current702_20260602.json"
            )
        )
        token_ablation = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_expanded_token_ablation_"
                "current702_20260602.json"
            )
        )
        best_sidecar = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_train_cal_feature_sidecar_"
                "current702_20260602.json"
            )
        )
        best_guardrail = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_train_cal_feature_guardrail_audit_"
                "current702_20260602.json"
            )
        )
        best_rerun = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_no_template_rerun_"
                "current702_20260602.json"
            )
        )
        best_contract = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_operating_point_contract_"
                "current702_20260602.json"
            )
        )
        best_error = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_calibration_error_analysis_"
                "current702_20260602.json"
            )
        )
        preflight = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_heldout_safe_application_preflight_"
                "current702_20260602.json"
            )
        )
        followup_ablation = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_token_ablation_"
                "current702_20260602.json"
            )
        )
        pair_sidecar = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_train_cal_feature_sidecar_"
                "current702_20260602.json"
            )
        )
        pair_guardrail = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_train_cal_feature_guardrail_audit_"
                "current702_20260602.json"
            )
        )
        pair_rerun = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_no_template_rerun_"
                "current702_20260602.json"
            )
        )
        pair_contract = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_operating_point_contract_"
                "current702_20260602.json"
            )
        )
        pair_error = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_calibration_error_analysis_"
                "current702_20260602.json"
            )
        )
        pair_surface_plan = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_heldout_safe_surface_plan_"
                "current702_20260602.json"
            )
        )
        pair_source_free_surface = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_application_surface_"
                "current702_20260602.json"
            )
        )
        pair_event_linker = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_event_linker_"
                "blocker_audit_current702_20260602.json"
            )
        )
        pair_residue_fallback = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_residue_count_"
                "fallback_contract_current702_20260602.json"
            )
        )
        pair_event_axis_schema = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_event_axis_"
                "linker_schema_current702_20260602.json"
            )
        )
        pair_event_axis_review_packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_event_axis_"
                "linker_review_packet_current702_20260603.json"
            )
        )
        pair_event_axis_gate = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_event_axis_"
                "linker_materialization_gate_current702_20260603.json"
            )
        )
        pair_event_axis_signoff_finalization = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_event_axis_"
                "linker_signoff_finalization_current702_20260603.json"
            )
        )
        pair_locator_queue = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_locator_action_queue_"
                "current702_20260602.json"
            )
        )
        pair_locator_input = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_locator_input_audit_"
                "current702_20260602.json"
            )
        )
        pair_coordinate_anchor = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_"
                "anchor_candidate_audit_current702_20260602.json"
            )
        )
        pair_coordinate_anchor_candidate_strict_audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_"
                "anchor_candidate_strict_audit_current702_20260602.json"
            )
        )
        pair_coordinate_anchor_review_queue = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_"
                "anchor_review_queue_current702_20260602.json"
            )
        )
        pair_coordinate_anchor_manual_review_packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_"
                "anchor_manual_review_packet_current702_20260602.json"
            )
        )
        pair_coordinate_anchor_priority1_review_worksheet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_"
                "anchor_priority1_review_worksheet_current702_20260602.json"
            )
        )
        pair_coordinate_anchor_priority1_rewrite_preflight = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_"
                "anchor_priority1_rewrite_preflight_current702_20260602.json"
            )
        )
        pair_locator_rewrite_approval_packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_locator_"
                "rewrite_approval_packet_current702_20260603.json"
            )
        )
        pair_locator_rewrite_gate = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_locator_"
                "rewrite_materialization_gate_current702_20260603.json"
            )
        )
        pair_pre_threshold_readiness = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_"
                "readiness_current702_20260603.json"
            )
        )
        pair_partial_surface_policy = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_partial_"
                "surface_policy_gate_current702_20260604.json"
            )
        )
        pair_partial_surface_contract_preflight = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_partial_"
                "surface_operating_contract_preflight_current702_20260604.json"
            )
        )
        pair_source_free_readout = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_heldout_"
                "threshold_readout_current702_20260604.json"
            )
        )
        pair_source_free_post_readout_queue = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_post_"
                "readout_recovery_queue_current702_20260604.json"
            )
        )
        pair_source_free_feature_repair_preflight = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_train_cal_"
                "safe_feature_repair_preflight_current702_20260604.json"
            )
        )
        pair_source_free_projection_repair_candidate_surface = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_projection_"
                "repair_candidate_surface_current702_20260604.json"
            )
        )
        pair_source_free_projection_repair_axis_packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_row_specific_bond_change_"
                "p0_oos_augmented_best_token_followup_pair_source_free_projection_"
                "repair_axis_review_packet_current702_20260604.json"
            )
        )

        self.assertEqual(
            sidecar["status"],
            "p0_oos_augmented_expanded_train_cal_row_specific_feature_sidecar_ready_no_fit",
        )
        self.assertEqual(sidecar["counts"]["materialized_feature_rows"], 43)
        self.assertEqual(sidecar["counts"]["base_feature_dimensions"], 17)
        self.assertEqual(sidecar["counts"]["expanded_feature_dimensions"], 543)
        self.assertEqual(sidecar["counts"]["total_feature_dimensions"], 560)
        self.assertEqual(sidecar["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            guardrail["status"],
            "p0_oos_augmented_expanded_train_cal_feature_guardrail_audit_passed",
        )
        self.assertEqual(guardrail["counts"]["critical_violation_total"], 0)
        self.assertTrue(guardrail["decision"]["safe_to_run_no_template_methods_now"])
        self.assertEqual(
            rerun["status"],
            "p0_row_specific_no_template_train_cal_operating_point_ready",
        )
        self.assertEqual(rerun["counts"]["feature_dimensions"], 560)
        self.assertEqual(
            rerun["residual_variant"]["calibration_selected_residual_threshold"][
                "oos_abstain_recall"
            ],
            0.035714,
        )
        self.assertEqual(
            comparison["status"],
            "p0_oos_augmented_expanded_calibration_comparison_ready",
        )
        self.assertFalse(
            comparison["decision"][
                "expanded_surface_replaces_frozen_residual_contract"
            ]
        )
        self.assertEqual(
            comparison["decision"]["recommended_operating_point_surface"],
            "coarse_oos_augmented_residual_contract",
        )
        self.assertEqual(
            comparison["deltas_expanded_minus_coarse"][
                "residual_oos_abstain_recall"
            ],
            -0.464286,
        )
        self.assertTrue(comparison["decision"]["keep_existing_residual_threshold"])
        self.assertEqual(
            ablation["status"],
            "p0_oos_augmented_expanded_family_ablation_ready",
        )
        self.assertEqual(ablation["counts"]["ablation_family_rows"], 8)
        self.assertEqual(
            ablation["counts"]["families_beating_coarse_residual_contract"], 0
        )
        self.assertEqual(
            ablation["decision"]["best_family_by_residual_oos_abstain_recall"],
            "event_type_sequence",
        )
        self.assertEqual(
            ablation["family_ablation_rows"][0]["residual_oos_abstain_recall"],
            0.285714,
        )
        self.assertTrue(ablation["decision"]["keep_existing_residual_threshold"])
        self.assertEqual(
            token_ablation["status"],
            "p0_oos_augmented_expanded_token_ablation_ready",
        )
        self.assertEqual(token_ablation["counts"]["candidate_tokens_scored"], 80)
        self.assertEqual(
            token_ablation["counts"]["tokens_beating_coarse_residual_contract"],
            33,
        )
        self.assertTrue(
            token_ablation["decision"][
                "single_token_expansion_replaces_frozen_residual_contract"
            ]
        )
        self.assertEqual(
            token_ablation["decision"]["best_token"],
            "event_residue_role:proton_transfer|electrostatic_stabiliser",
        )
        self.assertEqual(
            token_ablation["decision"]["best_token_residual_oos_abstain_recall"],
            0.714286,
        )
        self.assertEqual(
            token_ablation["decision"]["best_token_residual_auc_oos_gt_primary"],
            0.776786,
        )
        self.assertFalse(token_ablation["decision"]["keep_existing_residual_threshold"])
        self.assertEqual(
            best_sidecar["status"],
            "p0_oos_augmented_best_token_train_cal_feature_sidecar_ready_no_fit",
        )
        self.assertEqual(best_sidecar["counts"]["materialized_feature_rows"], 43)
        self.assertEqual(best_sidecar["counts"]["expanded_feature_dimensions"], 1)
        self.assertEqual(best_sidecar["counts"]["total_feature_dimensions"], 18)
        self.assertEqual(best_sidecar["counts"]["token_hit_rows"], 13)
        self.assertEqual(
            best_sidecar["decision"]["selected_feature_token"],
            "event_residue_role:proton_transfer|electrostatic_stabiliser",
        )
        self.assertEqual(
            best_guardrail["status"],
            "p0_oos_augmented_best_token_train_cal_feature_guardrail_audit_passed",
        )
        self.assertEqual(best_guardrail["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            best_rerun["status"],
            "p0_row_specific_no_template_train_cal_operating_point_ready",
        )
        self.assertEqual(best_rerun["counts"]["feature_dimensions"], 18)
        self.assertEqual(
            best_contract["status"],
            "p0_oos_augmented_best_token_operating_point_contract_ready_calibration_only",
        )
        self.assertEqual(
            best_contract["calibration_contract"]["residual_distance"][
                "threshold"
            ],
            3.21469422,
        )
        self.assertEqual(
            best_contract["calibration_contract"]["residual_distance"][
                "oos_abstain_recall"
            ],
            0.714286,
        )
        self.assertEqual(
            best_contract["calibration_contract"]["residual_distance"][
                "calibration_auc_oos_gt_primary"
            ],
            0.776786,
        )
        self.assertEqual(
            best_error["status"],
            "p0_oos_augmented_best_token_calibration_error_analysis_ready",
        )
        self.assertEqual(
            best_error["counts"]["outcome_counts"],
            {
                "oos_abstained": 20,
                "oos_non_abstained": 8,
                "primary_retained": 4,
            },
        )
        self.assertEqual(best_error["counts"]["critical_violation_total"], 0)
        self.assertEqual(len(best_error["retained_oos_failure_set"]), 8)
        self.assertEqual(best_error["retained_oos_failure_set"][0]["entry_id"], "m_csa:273")
        self.assertEqual(
            preflight["status"],
            "p0_oos_augmented_best_token_heldout_safe_application_preflight_blocked",
        )
        self.assertFalse(
            preflight["decision"]["heldout_safe_application_surface_available"]
        )
        self.assertFalse(
            preflight["decision"]["frozen_residual_threshold_applied_once"]
        )
        self.assertEqual(preflight["counts"]["heldout_rows_in_manifest"], 140)
        self.assertEqual(
            preflight["counts"]["heldout_rows_in_best_token_feature_sidecar"], 0
        )
        self.assertIn(
            "source_free_event_residue_role_surface_missing",
            preflight["blockers"],
        )
        self.assertEqual(
            followup_ablation["status"],
            "p0_oos_augmented_best_token_followup_token_ablation_ready",
        )
        self.assertEqual(
            followup_ablation["counts"]["remaining_retained_oos_failure_rows"], 8
        )
        self.assertEqual(
            followup_ablation["counts"]["candidate_tokens_scored"], 309
        )
        self.assertEqual(len(followup_ablation["candidate_feature_tokens"]), 309)
        self.assertEqual(
            followup_ablation["counts"][
                "tokens_beating_best_token_residual_contract"
            ],
            54,
        )
        self.assertEqual(
            followup_ablation["decision"]["best_followup_token"],
            "residue_code_count:his=3",
        )
        self.assertEqual(
            followup_ablation["decision"][
                "best_followup_residual_oos_abstain_recall"
            ],
            0.857143,
        )
        self.assertEqual(
            followup_ablation["decision"]["best_followup_residual_auc_oos_gt_primary"],
            0.875,
        )
        self.assertEqual(
            pair_sidecar["status"],
            "p0_oos_augmented_best_token_followup_pair_train_cal_feature_sidecar_ready_no_fit",
        )
        self.assertEqual(pair_sidecar["counts"]["materialized_feature_rows"], 43)
        self.assertEqual(pair_sidecar["counts"]["base_feature_dimensions"], 18)
        self.assertEqual(pair_sidecar["counts"]["expanded_feature_dimensions"], 1)
        self.assertEqual(pair_sidecar["counts"]["total_feature_dimensions"], 19)
        self.assertEqual(pair_sidecar["counts"]["token_hit_rows"], 6)
        self.assertEqual(
            pair_sidecar["decision"]["selected_followup_feature_token"],
            "residue_code_count:his=3",
        )
        self.assertEqual(
            pair_guardrail["status"],
            "p0_oos_augmented_best_token_followup_pair_train_cal_feature_guardrail_audit_passed",
        )
        self.assertEqual(pair_guardrail["counts"]["critical_violation_total"], 0)
        self.assertTrue(
            pair_guardrail["decision"]["safe_to_run_no_template_methods_now"]
        )
        self.assertEqual(
            pair_rerun["status"],
            "p0_row_specific_no_template_train_cal_operating_point_ready",
        )
        self.assertEqual(pair_rerun["counts"]["feature_dimensions"], 19)
        self.assertEqual(
            pair_contract["status"],
            "p0_oos_augmented_best_token_followup_pair_operating_point_contract_ready_calibration_only",
        )
        self.assertEqual(
            pair_contract["calibration_contract"]["residual_distance"][
                "threshold"
            ],
            3.21469422,
        )
        self.assertEqual(
            pair_contract["calibration_contract"]["residual_distance"][
                "oos_abstain_recall"
            ],
            0.857143,
        )
        self.assertEqual(
            pair_contract["calibration_contract"]["residual_distance"][
                "calibration_auc_oos_gt_primary"
            ],
            0.875,
        )
        self.assertEqual(
            pair_error["status"],
            "p0_oos_augmented_best_token_followup_pair_calibration_error_analysis_ready",
        )
        self.assertEqual(
            pair_error["counts"]["outcome_counts"],
            {
                "oos_abstained": 24,
                "oos_non_abstained": 4,
                "primary_retained": 4,
            },
        )
        self.assertEqual(len(pair_error["retained_oos_failure_set"]), 4)
        self.assertFalse(pair_error["guardrails"]["heldout_rows_evaluated"])
        self.assertEqual(
            pair_surface_plan["status"],
            "p0_oos_augmented_best_token_followup_pair_heldout_safe_surface_plan_ready_surface_blocked",
        )
        self.assertFalse(
            pair_surface_plan["decision"][
                "heldout_safe_pair_application_surface_ready"
            ]
        )
        self.assertEqual(
            pair_surface_plan["counts"]["heldout_rows_in_manifest"], 140
        )
        self.assertEqual(
            pair_surface_plan["counts"]["pair_calibration_oos_abstain_recall"],
            0.857143,
        )
        self.assertEqual(
            pair_surface_plan["counts"]["pair_calibration_retained_oos_rows"], 4
        )
        self.assertEqual(pair_surface_plan["counts"]["required_extractors"], 2)
        self.assertEqual(pair_surface_plan["counts"]["blockers"], 3)
        self.assertEqual(
            pair_surface_plan["counts"]["source_free_locator_priority1_candidates"],
            126,
        )
        self.assertEqual(
            pair_surface_plan["counts"][
                "source_free_locator_input_priority1_rows_without_anchor"
            ],
            24,
        )
        self.assertEqual(
            pair_surface_plan["counts"][
                "source_free_locator_input_priority1_rows_with_coordinate_anchor_candidate"
            ],
            102,
        )
        self.assertEqual(
            pair_surface_plan["counts"][
                "source_free_locator_input_priority1_preflight_passed_pending_explicit_approval"
            ],
            55,
        )
        self.assertEqual(
            pair_surface_plan["counts"][
                "source_free_locator_input_priority1_preflight_rows_with_warnings"
            ],
            6,
        )
        self.assertEqual(
            pair_surface_plan["counts"][
                "source_free_locator_input_priority1_preflight_approved_rewrites"
            ],
            0,
        )
        self.assertEqual(
            pair_surface_plan["counts"][
                "source_free_locator_input_auto_create_allowed_rows"
            ],
            0,
        )
        self.assertEqual(
            pair_surface_plan["counts"][
                "source_free_locator_schema_required_residue_locator_minimum"
            ],
            2,
        )
        self.assertEqual(
            pair_surface_plan["counts"][
                "source_free_application_surface_current702_heldout_locator_sidecars"
            ],
            53,
        )
        self.assertEqual(
            pair_surface_plan["counts"][
                "source_free_application_surface_residue_count_rows"
            ],
            53,
        )
        self.assertEqual(
            pair_surface_plan["counts"][
                "source_free_application_surface_event_residue_role_rows"
            ],
            14,
        )
        self.assertEqual(
            [
                row["status"]
                for row in pair_surface_plan["required_extractors"]
                if row["extractor"] == "source_free_event_residue_role_linker"
            ],
            ["ready_from_approved_source_free_event_axis_linkers"],
        )
        self.assertEqual(
            [
                row["status"]
                for row in pair_surface_plan["required_extractors"]
                if row["extractor"] == "source_free_active_site_residue_identity_counter"
            ],
            ["partial_source_free_residue_count_surface_materialized"],
        )
        self.assertIn(
            "source_free_current702_heldout_locator_coverage_incomplete",
            pair_surface_plan["blockers"],
        )
        self.assertNotIn(
            "source_free_event_residue_role_extractor_missing",
            pair_surface_plan["blockers"],
        )
        self.assertNotIn(
            "source_free_current702_heldout_locator_surface_missing",
            pair_surface_plan["blockers"],
        )
        self.assertFalse(pair_surface_plan["guardrails"]["heldout_rows_evaluated"])
        self.assertEqual(
            pair_source_free_surface["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_application_surface_blocked",
        )
        self.assertEqual(
            pair_source_free_surface["counts"]["heldout_rows_in_manifest"], 140
        )
        self.assertEqual(
            pair_source_free_surface["counts"]["source_free_locator_sidecars_total"],
            58,
        )
        self.assertEqual(
            pair_source_free_surface["counts"][
                "current702_heldout_locator_sidecars"
            ],
            53,
        )
        self.assertEqual(
            pair_source_free_surface["counts"][
                "source_free_residue_count_feature_rows"
            ],
            53,
        )
        self.assertEqual(
            pair_source_free_surface["counts"][
                "source_free_event_residue_role_feature_rows"
            ],
            14,
        )
        self.assertEqual(
            pair_source_free_surface["counts"][
                "source_free_event_axis_materialized_rows"
            ],
            14,
        )
        self.assertTrue(
            pair_source_free_surface["decision"][
                "source_free_event_residue_role_surface_ready"
            ]
        )
        self.assertIn(
            "event_axis_linker_materialization_gate",
            pair_source_free_surface["source_artifacts"],
        )
        self.assertFalse(
            pair_source_free_surface["decision"][
                "heldout_safe_pair_application_surface_ready"
            ]
        )
        self.assertFalse(
            pair_source_free_surface["guardrails"]["heldout_rows_evaluated"]
        )
        self.assertEqual(
            pair_partial_surface_policy["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_partial_surface_policy_gate_ready_no_threshold_read",
        )
        self.assertTrue(
            pair_partial_surface_policy["decision"][
                "heldout_safe_partial_surface_policy_ready"
            ]
        )
        self.assertTrue(
            pair_partial_surface_policy["decision"][
                "partial_surface_policy_accepted_for_frozen_threshold_read"
            ]
        )
        self.assertEqual(
            pair_partial_surface_policy["counts"]["source_free_pair_feature_rows"],
            53,
        )
        self.assertEqual(
            pair_partial_surface_policy["counts"][
                "missing_source_free_locator_policy_abstain_rows"
            ],
            87,
        )
        self.assertEqual(pair_partial_surface_policy["blockers"], [])
        self.assertFalse(
            pair_partial_surface_policy["guardrails"]["heldout_rows_evaluated"]
        )
        self.assertEqual(
            pair_partial_surface_contract_preflight["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_partial_surface_operating_contract_preflight_ready",
        )
        self.assertFalse(
            pair_partial_surface_contract_preflight["decision"][
                "explicit_policy_decision_required"
            ]
        )
        self.assertTrue(
            pair_partial_surface_contract_preflight["decision"][
                "ready_to_apply_frozen_residual_threshold_once"
            ]
        )
        self.assertEqual(
            pair_partial_surface_contract_preflight["counts"][
                "source_free_pair_feature_rows"
            ],
            53,
        )
        self.assertEqual(
            pair_partial_surface_contract_preflight["counts"][
                "missing_source_free_locator_policy_abstain_rows"
            ],
            87,
        )
        self.assertEqual(pair_partial_surface_contract_preflight["blockers"], [])
        self.assertEqual(
            pair_partial_surface_contract_preflight["decision_packet"][
                "decision_class"
            ],
            "source_free_partial_surface_operating_contract",
        )
        self.assertEqual(
            len(
                pair_partial_surface_contract_preflight["decision_packet"][
                    "decision_context_sha256"
                ]
            ),
            64,
        )
        self.assertFalse(
            pair_partial_surface_contract_preflight["guardrails"][
                "heldout_rows_evaluated"
            ]
        )
        self.assertEqual(
            pair_event_linker["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_event_linker_blocker_audit_ready_blocked",
        )
        self.assertEqual(
            pair_event_linker["counts"]["heldout_rows_in_manifest"], 140
        )
        self.assertEqual(
            pair_event_linker["counts"]["current702_heldout_locator_sidecars"],
            53,
        )
        self.assertEqual(
            pair_event_linker["counts"]["m_csa_curated_heldout_role_graph_ok_rows"],
            132,
        )
        self.assertEqual(
            pair_event_linker["calibration_contract_comparison"][
                "pair_residual_oos_abstain_recall"
            ],
            0.857143,
        )
        self.assertEqual(
            pair_event_linker["calibration_contract_comparison"][
                "residue_code_only_oos_abstain_recall"
            ],
            0.642857,
        )
        self.assertIn(
            "m_csa_curated_active_site_role_graph_forbidden_as_deployment_input",
            pair_event_linker["blockers"],
        )
        self.assertIn(
            "source_free_current702_heldout_locator_coverage_incomplete",
            pair_event_linker["blockers"],
        )
        self.assertNotIn(
            "source_free_current702_heldout_locator_surface_missing",
            pair_event_linker["blockers"],
        )
        self.assertIn(
            "source_free_residue_code_only_fallback_underperforms_pair_contract",
            pair_event_linker["blockers"],
        )
        self.assertFalse(
            pair_event_linker["decision"]["source_free_event_linker_ready"]
        )
        self.assertFalse(
            pair_event_linker["decision"][
                "curated_active_site_role_graph_allowed_for_deployment"
            ]
        )
        self.assertFalse(pair_event_linker["guardrails"]["heldout_rows_evaluated"])
        self.assertEqual(
            pair_residue_fallback["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_residue_count_fallback_contract_ready_calibration_only_surface_blocked",
        )
        self.assertEqual(
            pair_residue_fallback["fallback_feature"]["feature_token"],
            "residue_code_count:his=3",
        )
        self.assertFalse(
            pair_residue_fallback["fallback_feature"]["event_axis_required"]
        )
        self.assertEqual(
            pair_residue_fallback["calibration_contract"][
                "residual_distance_threshold"
            ],
            3.21469422,
        )
        self.assertEqual(
            pair_residue_fallback["calibration_contract"][
                "calibration_oos_abstain_recall"
            ],
            0.642857,
        )
        self.assertEqual(
            pair_residue_fallback["calibration_contract"]["recall_delta_vs_pair"],
            0.214286,
        )
        self.assertEqual(
            pair_residue_fallback["counts"][
                "source_free_locator_input_priority1_preflight_passed_pending_explicit_approval"
            ],
            55,
        )
        self.assertEqual(
            pair_residue_fallback["counts"][
                "source_free_locator_input_priority1_preflight_rows_with_warnings"
            ],
            6,
        )
        self.assertEqual(
            pair_residue_fallback["counts"][
                "source_free_locator_input_priority1_approved_rewrites"
            ],
            0,
        )
        self.assertEqual(
            pair_residue_fallback["counts"]["current702_heldout_locator_sidecars"],
            53,
        )
        self.assertEqual(
            pair_residue_fallback["counts"][
                "source_free_residue_count_feature_rows"
            ],
            53,
        )
        self.assertTrue(
            pair_residue_fallback["decision"][
                "fallback_contract_calibrated_train_cal_only"
            ]
        )
        self.assertFalse(
            pair_residue_fallback["decision"][
                "fallback_accepted_as_deployable_replacement"
            ]
        )
        self.assertTrue(
            pair_residue_fallback["decision"][
                "explicit_acceptance_required_before_heldout_read"
            ]
        )
        self.assertIn(
            "source_free_residue_count_fallback_lower_recall_requires_explicit_acceptance",
            pair_residue_fallback["blockers"],
        )
        self.assertIn(
            "source_free_current702_heldout_locator_coverage_incomplete",
            pair_residue_fallback["blockers"],
        )
        self.assertIn(
            "source_free_residue_count_surface_incomplete",
            pair_residue_fallback["blockers"],
        )
        self.assertNotIn(
            "source_free_current702_heldout_locator_surface_missing",
            pair_residue_fallback["blockers"],
        )
        self.assertNotIn(
            "source_free_locator_rewrite_explicit_approval_pending",
            pair_residue_fallback["blockers"],
        )
        self.assertFalse(
            pair_residue_fallback["guardrails"]["heldout_rows_evaluated"]
        )
        self.assertEqual(
            pair_event_axis_schema["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_schema_ready_no_linkers_materialized",
        )
        self.assertEqual(
            pair_event_axis_schema["target_feature"]["event_residue_role_token"],
            "event_residue_role:proton_transfer|electrostatic_stabiliser",
        )
        self.assertEqual(
            pair_event_axis_schema["row_schema"]["allowed_event_types"],
            ["proton_transfer"],
        )
        self.assertEqual(
            pair_event_axis_schema["row_schema"]["allowed_residue_roles"],
            ["electrostatic_stabiliser"],
        )
        self.assertEqual(
            pair_event_axis_schema["counts"]["materialized_linker_rows"],
            0,
        )
        self.assertEqual(
            pair_event_axis_schema["counts"]["blockers_to_clear"],
            3,
        )
        self.assertTrue(
            pair_event_axis_schema["decision"]["event_axis_linker_schema_ready"]
        )
        self.assertFalse(
            pair_event_axis_schema["decision"]["event_axis_linkers_materialized"]
        )
        self.assertFalse(
            pair_event_axis_schema["guardrails"]["heldout_rows_evaluated"]
        )
        self.assertEqual(
            pair_event_axis_review_packet["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_review_packet_ready_review_only",
        )
        self.assertEqual(
            pair_event_axis_review_packet["counts"]["event_axis_review_stub_rows"],
            55,
        )
        self.assertEqual(
            pair_event_axis_review_packet["counts"]["pending_reviewer_decisions"],
            53,
        )
        self.assertEqual(
            pair_event_axis_review_packet["counts"][
                "locator_dependency_approved_rows"
            ],
            53,
        )
        self.assertEqual(
            pair_event_axis_review_packet["counts"][
                "locator_dependency_pending_rows"
            ],
            0,
        )
        self.assertEqual(
            pair_event_axis_review_packet["counts"][
                "locator_dependency_rejected_rows"
            ],
            2,
        )
        self.assertEqual(
            pair_event_axis_review_packet["blocker_counts"][
                "explicit_event_axis_linker_review_required"
            ],
            53,
        )
        self.assertEqual(
            pair_event_axis_review_packet["blocker_counts"][
                "source_free_locator_dependency_rejected"
            ],
            2,
        )
        self.assertNotIn(
            "approved_source_free_locator_surface_missing",
            pair_event_axis_review_packet["blockers"],
        )
        self.assertFalse(
            pair_event_axis_review_packet["guardrails"]["heldout_rows_evaluated"]
        )
        self.assertEqual(
            pair_event_axis_gate["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_materialization_gate_ready",
        )
        self.assertEqual(
            pair_event_axis_gate["counts"]["submitted_linker_rows"], 14
        )
        self.assertEqual(
            pair_event_axis_gate["counts"]["materialized_linker_rows"], 14
        )
        self.assertIn(
            "event_axis_linker_signoff_finalization_current702_20260603.json",
            pair_event_axis_gate["source_artifacts"]["linker_rows"]["path"],
        )
        self.assertNotIn(
            "source_free_event_axis_linker_rows_missing",
            pair_event_axis_gate["blockers"],
        )
        self.assertNotIn(
            "approved_source_free_locator_surface_still_required",
            pair_event_axis_gate["blockers"],
        )
        self.assertTrue(
            pair_event_axis_gate["decision"]["event_axis_linkers_materialized"]
        )
        self.assertFalse(
            pair_event_axis_gate["decision"]["apply_frozen_pair_threshold_now"]
        )
        self.assertFalse(
            pair_event_axis_gate["guardrails"]["heldout_rows_evaluated"]
        )
        self.assertEqual(
            pair_event_axis_signoff_finalization["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_signoff_finalization_ready",
        )
        self.assertEqual(
            pair_event_axis_signoff_finalization["counts"]["draft_signoff_rows"],
            53,
        )
        self.assertEqual(
            pair_event_axis_signoff_finalization["counts"]["rows_with_both_roles"],
            14,
        )
        self.assertEqual(
            pair_event_axis_signoff_finalization["counts"][
                "priority_1_both_roles_moderate_evidence_review_rows"
            ],
            3,
        )
        self.assertEqual(
            pair_event_axis_signoff_finalization["counts"][
                "priority_2_both_roles_weak_evidence_review_rows"
            ],
            11,
        )
        self.assertEqual(
            pair_event_axis_signoff_finalization["counts"][
                "priority_review_rows"
            ],
            14,
        )
        self.assertEqual(
            len(pair_event_axis_signoff_finalization["priority_review_rows"]),
            14,
        )
        self.assertEqual(
            [
                row["entry_id"]
                for row in pair_event_axis_signoff_finalization[
                    "priority_review_rows"
                ][:3]
            ],
            ["m_csa:418", "m_csa:545", "m_csa:750"],
        )
        self.assertEqual(
            pair_event_axis_signoff_finalization["counts"][
                "insufficient_event_axis_evidence_rewrite_or_reject_rows"
            ],
            33,
        )
        self.assertEqual(
            pair_event_axis_signoff_finalization["counts"][
                "pending_reviewer_signoff_rows"
            ],
            0,
        )
        self.assertEqual(
            pair_event_axis_signoff_finalization["counts"][
                "explicit_approved_rows"
            ],
            14,
        )
        self.assertEqual(
            pair_event_axis_signoff_finalization["counts"][
                "explicit_rejected_rows"
            ],
            39,
        )
        self.assertEqual(
            pair_event_axis_signoff_finalization["counts"][
                "gate_consumable_event_axis_linker_rows"
            ],
            14,
        )
        self.assertNotIn(
            "event_axis_signoff_decisions_pending",
            pair_event_axis_signoff_finalization["blockers"],
        )
        self.assertTrue(
            pair_event_axis_signoff_finalization["decision"][
                "event_axis_linker_rows_ready_for_materialization_gate"
            ]
        )
        self.assertFalse(
            pair_event_axis_signoff_finalization["guardrails"][
                "heldout_rows_evaluated"
            ]
        )
        self.assertEqual(
            pair_locator_queue["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_locator_action_queue_ready",
        )
        self.assertEqual(
            pair_locator_queue["counts"]["heldout_rows_in_manifest"], 140
        )
        self.assertEqual(
            pair_locator_queue["counts"][
                "approved_current702_source_free_locator_sidecars"
            ],
            0,
        )
        self.assertEqual(
            pair_locator_queue["counts"][
                "priority_1_coordinate_ready_locator_candidates"
            ],
            126,
        )
        self.assertEqual(
            pair_locator_queue["counts"][
                "priority_2_active_site_position_ready_predicted_geometry_missing"
            ],
            4,
        )
        self.assertEqual(
            pair_locator_queue["counts"][
                "priority_3_predicted_structure_fetch_failed"
            ],
            2,
        )
        self.assertEqual(
            pair_locator_queue["counts"][
                "blocker_accession_compatible_sequence_positions_missing"
            ],
            8,
        )
        self.assertFalse(pair_locator_queue["guardrails"]["heldout_rows_evaluated"])
        self.assertFalse(
            pair_locator_queue["decision"]["apply_frozen_pair_threshold_now"]
        )
        self.assertEqual(
            pair_locator_input["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_locator_input_audit_blocked",
        )
        self.assertEqual(
            pair_locator_input["counts"]["priority1_locator_queue_rows"], 126
        )
        self.assertEqual(
            pair_locator_input["counts"][
                "priority1_rows_with_source_free_ligand_or_cofactor_anchor"
            ],
            0,
        )
        self.assertEqual(
            pair_locator_input["counts"][
                "priority1_rows_with_source_free_coordinate_local_anchor_candidate"
            ],
            102,
        )
        self.assertEqual(
            pair_locator_input["counts"][
                "priority1_rows_without_source_free_anchor"
            ],
            24,
        )
        self.assertEqual(
            pair_locator_input["counts"][
                "priority1_coordinate_anchor_preflight_passed_pending_explicit_approval"
            ],
            55,
        )
        self.assertEqual(
            pair_locator_input["counts"][
                "priority1_coordinate_anchor_preflight_rows_with_warnings"
            ],
            6,
        )
        self.assertEqual(
            pair_locator_input["counts"][
                "priority1_coordinate_anchor_preflight_approved_rewrites"
            ],
            0,
        )
        self.assertIn(
            "source_free_coordinate_anchor_preflight_passed_requires_explicit_approval",
            pair_locator_input["blockers"],
        )
        self.assertEqual(
            pair_locator_input["counts"]["source_free_locator_schema_available"],
            1,
        )
        self.assertEqual(
            pair_locator_input["counts"][
                "source_free_locator_schema_required_residue_locator_minimum"
            ],
            2,
        )
        self.assertEqual(
            pair_locator_input["source_free_locator_schema_summary"][
                "allowed_locator_evidence_classes"
            ],
            4,
        )
        self.assertFalse(
            pair_locator_input["decision"]["auto_create_locator_sidecars_now"]
        )
        self.assertFalse(pair_locator_input["guardrails"]["heldout_rows_evaluated"])
        self.assertEqual(
            pair_locator_rewrite_approval_packet["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_approval_packet_ready_review_only",
        )
        self.assertEqual(
            pair_locator_rewrite_approval_packet["counts"]["decision_stub_rows"],
            55,
        )
        self.assertEqual(
            pair_locator_rewrite_approval_packet["counts"][
                "pending_reviewer_decisions"
            ],
            55,
        )
        self.assertEqual(
            pair_locator_rewrite_approval_packet["counts"][
                "materialization_gate_ready_if_approved_rows"
            ],
            55,
        )
        self.assertEqual(
            pair_locator_rewrite_approval_packet["counts"]["warning_review_rows"],
            6,
        )
        self.assertIn(
            "reviewer_decisions_not_recorded",
            pair_locator_rewrite_approval_packet["blockers"],
        )
        self.assertFalse(
            pair_locator_rewrite_approval_packet["decision"][
                "approved_locator_rewrites_available"
            ]
        )
        self.assertFalse(
            pair_locator_rewrite_approval_packet["guardrails"][
                "locator_sidecars_created_or_copied"
            ]
        )
        first_locator_stub = pair_locator_rewrite_approval_packet[
            "locator_rewrite_decision_stubs"
        ][0]
        self.assertEqual(
            first_locator_stub["decision_field_to_update"], "reviewer_decision"
        )
        self.assertEqual(
            first_locator_stub["approved_boolean_field_to_update"], "approved"
        )
        self.assertTrue(
            first_locator_stub["required_approved_value_if_approving"]
        )
        self.assertEqual(
            pair_locator_rewrite_gate["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate_materialized",
        )
        self.assertEqual(pair_locator_rewrite_gate["counts"]["preflight_rows"], 55)
        self.assertEqual(
            pair_locator_rewrite_gate["counts"]["approval_records_total"], 55
        )
        self.assertEqual(
            pair_locator_rewrite_gate["counts"]["approved_decision_records"], 53
        )
        self.assertEqual(
            pair_locator_rewrite_gate["counts"]["invalid_approval_records"], 0
        )
        self.assertEqual(
            pair_locator_rewrite_gate["counts"]["approved_locator_sidecars_written"],
            53,
        )
        self.assertEqual(
            pair_locator_rewrite_gate["counts"]["rows_without_explicit_approval"],
            2,
        )
        self.assertEqual(pair_locator_rewrite_gate["blockers"], [])
        self.assertFalse(
            pair_locator_rewrite_gate["decision"][
                "apply_frozen_pair_threshold_now"
            ]
        )
        self.assertTrue(
            pair_locator_rewrite_gate["decision"][
                "approved_source_free_locator_surface_ready"
            ]
        )
        self.assertTrue(
            pair_locator_rewrite_gate["guardrails"]["locator_sidecars_created_or_copied"]
        )
        self.assertFalse(
            pair_locator_rewrite_gate["guardrails"]["heldout_rows_evaluated"]
        )
        self.assertEqual(
            pair_pre_threshold_readiness["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_readiness_ready",
        )
        self.assertTrue(
            pair_pre_threshold_readiness["readiness_inputs"][
                "pair_operating_point_contract_ready"
            ]
        )
        self.assertTrue(
            pair_pre_threshold_readiness["readiness_inputs"][
                "source_free_event_axis_linkers_materialized"
            ]
        )
        self.assertTrue(
            pair_pre_threshold_readiness["readiness_inputs"][
                "approved_source_free_locator_surface_ready"
            ]
        )
        self.assertFalse(
            pair_pre_threshold_readiness["readiness_inputs"][
                "heldout_safe_pair_application_surface_ready"
            ]
        )
        self.assertTrue(
            pair_pre_threshold_readiness["readiness_inputs"][
                "heldout_safe_partial_surface_policy_ready"
            ]
        )
        self.assertTrue(
            pair_pre_threshold_readiness["readiness_inputs"][
                "partial_surface_policy_accepted_for_frozen_threshold_read"
            ]
        )
        self.assertTrue(
            pair_pre_threshold_readiness["readiness_inputs"][
                "partial_surface_policy_effective_application_surface_ready"
            ]
        )
        self.assertEqual(
            pair_pre_threshold_readiness["frozen_contract"][
                "residual_distance_threshold"
            ],
            3.21469422,
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"]["locator_preflight_rows"], 55
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"]["locator_approval_records"], 55
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"][
                "locator_pending_reviewer_decisions"
            ],
            0,
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"]["locator_review_warning_rows"],
            6,
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"]["locator_sidecars_written"], 53
        )
        self.assertEqual(pair_pre_threshold_readiness["counts"]["blockers"], 0)
        self.assertEqual(
            pair_pre_threshold_readiness["counts"][
                "source_free_event_residue_role_feature_rows"
            ],
            14,
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"][
                "event_axis_materialized_linker_rows"
            ],
            14,
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"][
                "partial_surface_policy_pair_feature_rows"
            ],
            53,
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"][
                "partial_surface_policy_missing_locator_abstain_rows"
            ],
            87,
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"]["event_axis_signoff_draft_rows"],
            53,
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"][
                "event_axis_signoff_rows_with_both_roles"
            ],
            14,
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"][
                "event_axis_pending_reviewer_signoff_rows"
            ],
            0,
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"][
                "event_axis_gate_consumable_signoff_rows"
            ],
            14,
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"][
                "event_axis_priority_1_both_roles_moderate_evidence_review_rows"
            ],
            3,
        )
        self.assertEqual(
            pair_pre_threshold_readiness["counts"][
                "event_axis_priority_2_both_roles_weak_evidence_review_rows"
            ],
            11,
        )
        self.assertNotIn(
            "approved_source_free_locator_surface_missing",
            pair_pre_threshold_readiness["blockers"],
        )
        self.assertNotIn(
            "source_free_event_axis_linkers_missing",
            pair_pre_threshold_readiness["blockers"],
        )
        self.assertNotIn(
            "source_free_event_axis_linker_rows_missing",
            pair_pre_threshold_readiness["blockers"],
        )
        self.assertNotIn(
            "event_axis_signoff_decisions_pending",
            pair_pre_threshold_readiness["blockers"],
        )
        self.assertNotIn(
            "source_free_event_residue_role_extractor_missing",
            pair_pre_threshold_readiness["blockers"],
        )
        self.assertNotIn(
            "source_free_proton_transfer_event_axis_missing",
            pair_pre_threshold_readiness["blockers"],
        )
        self.assertEqual(pair_pre_threshold_readiness["blockers"], [])
        self.assertTrue(
            pair_pre_threshold_readiness["source_artifacts"][
                "event_axis_linker_signoff_finalization"
            ]["exists"]
        )
        self.assertTrue(
            pair_pre_threshold_readiness["source_artifacts"][
                "event_axis_linker_materialization_gate"
            ]["exists"]
        )
        self.assertTrue(
            pair_pre_threshold_readiness["source_artifacts"][
                "partial_surface_policy_gate"
            ]["exists"]
        )
        self.assertTrue(
            pair_pre_threshold_readiness["decision"][
                "ready_to_apply_frozen_residual_threshold_once"
            ]
        )
        self.assertFalse(
            pair_pre_threshold_readiness["decision"][
                "apply_frozen_pair_threshold_now"
            ]
        )
        self.assertFalse(
            pair_pre_threshold_readiness["guardrails"]["heldout_rows_evaluated"]
        )
        self.assertEqual(
            pair_source_free_readout["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_heldout_threshold_readout_applied_once",
        )
        self.assertEqual(
            pair_source_free_readout["counts"]["heldout_rows_total"], 140
        )
        self.assertEqual(
            pair_source_free_readout["counts"]["heldout_feature_complete_rows"], 53
        )
        self.assertEqual(
            pair_source_free_readout["counts"][
                "heldout_missing_locator_deterministic_abstain_rows"
            ],
            87,
        )
        self.assertEqual(
            pair_source_free_readout["counts"]["overall_oos_abstain_recall"], 1.0
        )
        self.assertEqual(
            pair_source_free_readout["counts"]["overall_primary_retain_recall"], 0.0
        )
        self.assertTrue(
            pair_source_free_readout["guardrails"]["heldout_rows_evaluated_once"]
        )
        self.assertFalse(
            pair_source_free_readout["guardrails"][
                "heldout_rows_used_for_training_or_threshold_tuning"
            ]
        )
        self.assertFalse(
            pair_source_free_readout["guardrails"][
                "missing_locator_rows_scored_by_residual_threshold"
            ]
        )
        self.assertEqual(
            pair_source_free_post_readout_queue["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_post_readout_recovery_queue_ready_deployment_blocked",
        )
        self.assertEqual(
            pair_source_free_post_readout_queue["counts"]["queue_rows"], 119
        )
        self.assertEqual(
            pair_source_free_post_readout_queue["counts"][
                "feature_complete_primary_abstained_by_residual_rows"
            ],
            32,
        )
        self.assertEqual(
            pair_source_free_post_readout_queue["counts"][
                "primary_missing_source_free_locator_rows"
            ],
            16,
        )
        self.assertEqual(
            pair_source_free_post_readout_queue["counts"][
                "oos_missing_source_free_locator_rows"
            ],
            71,
        )
        self.assertEqual(
            pair_source_free_post_readout_queue["counts"][
                "feature_complete_oos_retained_by_residual_rows"
            ],
            0,
        )
        self.assertTrue(
            pair_source_free_post_readout_queue["decision"][
                "deployable_claim_blocked"
            ]
        )
        self.assertFalse(
            pair_source_free_post_readout_queue["decision"][
                "coverage_repair_alone_sufficient_for_deployment"
            ]
        )
        self.assertFalse(
            pair_source_free_post_readout_queue["decision"][
                "rerun_or_retune_heldout_authorized"
            ]
        )
        self.assertFalse(
            pair_source_free_post_readout_queue["guardrails"][
                "heldout_rows_rescored"
            ]
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_train_cal_safe_feature_repair_preflight_ready_deployment_blocked",
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["counts"][
                "feature_complete_readout_rows"
            ],
            53,
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["counts"][
                "feature_complete_primary_abstentions"
            ],
            32,
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["counts"][
                "feature_complete_primary_abstentions_with_projection_gap"
            ],
            32,
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["counts"][
                "frozen_feature_fields"
            ],
            19,
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["counts"][
                "source_free_projected_feature_fields"
            ],
            2,
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["counts"][
                "frozen_feature_fields_missing_from_source_free_projection"
            ],
            17,
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["counts"][
                "priority_repair_feature_fields"
            ],
            11,
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["counts"][
                "priority_repair_fields_with_direct_existing_source_free_axis"
            ],
            2,
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["counts"][
                "priority_repair_fields_requiring_new_source_free_axis"
            ],
            9,
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["counts"][
                "priority_repair_category_counts"
            ],
            {
                "bond_change": 5,
                "electron_flow": 2,
                "event_topology": 2,
                "proton_transfer": 2,
            },
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["counts"][
                "source_free_event_axis_materialized_rows"
            ],
            14,
        )
        self.assertEqual(
            pair_source_free_feature_repair_preflight["counts"][
                "source_free_event_axis_type_counts"
            ],
            {"proton_transfer": 14},
        )
        self.assertTrue(
            pair_source_free_feature_repair_preflight["decision"][
                "train_cal_safe_feature_repair_required"
            ]
        )
        self.assertFalse(
            pair_source_free_feature_repair_preflight["decision"][
                "coverage_repair_alone_sufficient_for_deployment"
            ]
        )
        self.assertFalse(
            pair_source_free_feature_repair_preflight["decision"][
                "rerun_or_retune_heldout_authorized"
            ]
        )
        self.assertFalse(
            pair_source_free_feature_repair_preflight["guardrails"][
                "heldout_rows_rescored"
            ]
        )
        self.assertEqual(
            pair_source_free_projection_repair_candidate_surface["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_projection_repair_candidate_surface_partial_not_scoreable",
        )
        self.assertEqual(
            pair_source_free_projection_repair_candidate_surface["counts"][
                "candidate_projection_rows"
            ],
            53,
        )
        self.assertEqual(
            pair_source_free_projection_repair_candidate_surface["counts"][
                "rows_with_direct_proton_transfer_projection"
            ],
            14,
        )
        self.assertEqual(
            pair_source_free_projection_repair_candidate_surface["counts"][
                "rows_pair_only_no_direct_projection"
            ],
            39,
        )
        self.assertEqual(
            pair_source_free_projection_repair_candidate_surface["counts"][
                "full_frozen_projection_ready_rows"
            ],
            0,
        )
        self.assertEqual(
            pair_source_free_projection_repair_candidate_surface["counts"][
                "threshold_scoring_ready_rows"
            ],
            0,
        )
        self.assertEqual(
            pair_source_free_projection_repair_candidate_surface["counts"][
                "new_source_free_axis_required_fields"
            ],
            9,
        )
        self.assertFalse(
            pair_source_free_projection_repair_candidate_surface["decision"][
                "candidate_surface_ready_for_threshold_scoring"
            ]
        )
        self.assertFalse(
            pair_source_free_projection_repair_candidate_surface["decision"][
                "rerun_or_retune_heldout_authorized"
            ]
        )
        self.assertFalse(
            pair_source_free_projection_repair_candidate_surface["guardrails"][
                "heldout_rows_rescored"
            ]
        )
        self.assertEqual(
            pair_source_free_projection_repair_axis_packet["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_projection_repair_axis_review_packet_ready_review_only",
        )
        self.assertEqual(
            pair_source_free_projection_repair_axis_packet["counts"][
                "review_items"
            ],
            3,
        )
        self.assertEqual(
            pair_source_free_projection_repair_axis_packet["counts"][
                "pending_review_items"
            ],
            3,
        )
        self.assertEqual(
            pair_source_free_projection_repair_axis_packet["counts"][
                "covered_priority_fields"
            ],
            9,
        )
        self.assertEqual(
            pair_source_free_projection_repair_axis_packet["counts"][
                "materialization_gate_ready_items"
            ],
            0,
        )
        self.assertFalse(
            pair_source_free_projection_repair_axis_packet["decision"][
                "materialization_gate_ready_now"
            ]
        )
        self.assertFalse(
            pair_source_free_projection_repair_axis_packet["decision"][
                "rerun_or_retune_heldout_authorized"
            ]
        )
        self.assertEqual(
            [
                item["axis_id"]
                for item in pair_source_free_projection_repair_axis_packet[
                    "review_items"
                ]
            ],
            [
                "source_free_bond_change_axis",
                "source_free_electron_flow_axis",
                "source_free_event_topology_axis",
            ],
        )
        self.assertEqual(
            pair_coordinate_anchor["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_anchor_candidate_audit_ready_review_only",
        )
        self.assertEqual(
            pair_coordinate_anchor["counts"]["priority1_locator_queue_rows"], 126
        )
        self.assertEqual(
            pair_coordinate_anchor["counts"]["selected_pdb_coordinate_files_found"],
            126,
        )
        self.assertEqual(
            pair_coordinate_anchor["counts"][
                "rows_with_minimum_coordinate_anchor_locators"
            ],
            102,
        )
        self.assertEqual(
            pair_coordinate_anchor["counts"][
                "rows_with_all_candidate_sequence_positions_validated"
            ],
            93,
        )
        self.assertEqual(
            pair_coordinate_anchor["counts"]["candidate_sidecars_staged"], 126
        )
        self.assertEqual(
            pair_coordinate_anchor["counts"][
                "auto_create_locator_sidecar_allowed_rows"
            ],
            0,
        )
        self.assertFalse(
            pair_coordinate_anchor["decision"]["auto_create_locator_sidecars_now"]
        )
        self.assertFalse(
            pair_coordinate_anchor["guardrails"]["heldout_rows_evaluated"]
        )
        self.assertFalse(
            pair_coordinate_anchor["candidate_sidecars"][0][
                "ready_for_predicted_geometry_scoring"
            ]
        )
        self.assertEqual(
            pair_coordinate_anchor_candidate_strict_audit["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_anchor_candidate_strict_audit_passed_review_only",
        )
        self.assertEqual(
            pair_coordinate_anchor_candidate_strict_audit["counts"][
                "candidate_sidecars_checked"
            ],
            126,
        )
        self.assertEqual(
            pair_coordinate_anchor_candidate_strict_audit["counts"][
                "candidate_only_sidecars"
            ],
            126,
        )
        self.assertEqual(
            pair_coordinate_anchor_candidate_strict_audit["counts"][
                "sidecars_with_forbidden_feature_flags"
            ],
            0,
        )
        self.assertEqual(
            pair_coordinate_anchor_candidate_strict_audit["counts"][
                "ready_for_predicted_geometry_scoring"
            ],
            0,
        )
        self.assertEqual(
            pair_coordinate_anchor_candidate_strict_audit["counts"][
                "critical_violation_total"
            ],
            0,
        )
        self.assertFalse(
            pair_coordinate_anchor_candidate_strict_audit["decision"][
                "copy_to_audited_locator_dir_allowed_now"
            ]
        )
        self.assertEqual(
            pair_coordinate_anchor_review_queue["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_anchor_review_queue_ready_review_only",
        )
        self.assertEqual(
            pair_coordinate_anchor_review_queue["counts"]["review_queue_rows"],
            126,
        )
        self.assertEqual(
            pair_coordinate_anchor_review_queue["counts"][
                "ready_for_manual_forbidden_feature_review"
            ],
            55,
        )
        self.assertEqual(
            pair_coordinate_anchor_review_queue["counts"][
                "needs_ligand_specificity_review"
            ],
            40,
        )
        self.assertEqual(
            pair_coordinate_anchor_review_queue["counts"][
                "needs_uniprot_position_validation"
            ],
            7,
        )
        self.assertEqual(
            pair_coordinate_anchor_review_queue["counts"][
                "blocked_minimum_or_no_ligand_anchor"
            ],
            24,
        )
        self.assertFalse(
            pair_coordinate_anchor_review_queue["decision"][
                "copy_to_audited_locator_dir_allowed_now"
            ]
        )
        self.assertFalse(
            pair_coordinate_anchor_review_queue["guardrails"][
                "heldout_rows_evaluated"
            ]
        )
        self.assertEqual(
            pair_coordinate_anchor_manual_review_packet["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_anchor_manual_review_packet_ready_review_only",
        )
        self.assertEqual(
            pair_coordinate_anchor_manual_review_packet["counts"]["review_rows"],
            126,
        )
        self.assertEqual(
            pair_coordinate_anchor_manual_review_packet["counts"][
                "candidate_sidecar_files_present"
            ],
            126,
        )
        self.assertEqual(
            pair_coordinate_anchor_manual_review_packet["counts"][
                "priority1_manual_forbidden_feature_review_rows"
            ],
            55,
        )
        self.assertFalse(
            pair_coordinate_anchor_manual_review_packet["decision"][
                "copy_to_audited_locator_dir_allowed_now"
            ]
        )
        self.assertFalse(
            pair_coordinate_anchor_manual_review_packet["guardrails"][
                "heldout_rows_evaluated"
            ]
        )
        self.assertIsNotNone(
            pair_coordinate_anchor_manual_review_packet["review_rows"][0][
                "candidate_sha256"
            ]
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_review_worksheet["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_anchor_priority1_review_worksheet_ready_review_only",
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_review_worksheet["counts"][
                "priority1_review_rows"
            ],
            55,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_review_worksheet["counts"][
                "candidate_sidecar_files_present"
            ],
            55,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_review_worksheet["counts"][
                "expanded_residue_locators"
            ],
            303,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_review_worksheet["role_hint_counts"][
                "metal_ligand_or_water_activator_candidate"
            ],
            76,
        )
        self.assertFalse(
            pair_coordinate_anchor_priority1_review_worksheet["decision"][
                "copy_to_audited_locator_dir_allowed_now"
            ]
        )
        self.assertFalse(
            pair_coordinate_anchor_priority1_review_worksheet["guardrails"][
                "heldout_rows_evaluated"
            ]
        )
        self.assertFalse(
            pair_coordinate_anchor_priority1_review_worksheet["worksheet_rows"][0][
                "ready_for_predicted_geometry_scoring"
            ]
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["status"],
            "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_anchor_priority1_rewrite_preflight_passed_pending_explicit_approval",
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "priority1_review_rows"
            ],
            55,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "preflight_passed_pending_explicit_approval"
            ],
            55,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "schema_dry_run_passed_rows"
            ],
            55,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "guardrail_preflight_passed_rows"
            ],
            55,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "coordinate_contact_supported_rows"
            ],
            55,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "rows_with_preflight_warnings"
            ],
            6,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "preflight_clean_pending_explicit_approval"
            ],
            49,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "preflight_warning_pending_explicit_approval"
            ],
            6,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "preflight_blocked_before_approval"
            ],
            0,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "explicit_approval_queue_rows"
            ],
            55,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "explicit_approval_queue_clean_rows"
            ],
            49,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "explicit_approval_queue_warning_rows"
            ],
            6,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight[
                "explicit_approval_queue"
            ][0]["approval_review_class"],
            "candidate_clean_pending_explicit_approval",
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight[
                "explicit_approval_queue"
            ][48]["approval_review_class"],
            "candidate_clean_pending_explicit_approval",
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight[
                "explicit_approval_queue"
            ][49]["approval_review_class"],
            "candidate_minimum_locator_warning_pending_explicit_approval",
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "critical_violation_total"
            ],
            0,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "copy_to_audited_locator_dir_allowed_now"
            ],
            0,
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["counts"][
                "explicitly_approved_locator_rewrites"
            ],
            0,
        )
        self.assertFalse(
            pair_coordinate_anchor_priority1_rewrite_preflight["decision"][
                "copy_to_audited_locator_dir_allowed_now"
            ]
        )
        self.assertFalse(
            pair_coordinate_anchor_priority1_rewrite_preflight["guardrails"][
                "heldout_rows_evaluated"
            ]
        )
        self.assertFalse(
            pair_coordinate_anchor_priority1_rewrite_preflight["guardrails"][
                "locator_sidecars_created_or_copied"
            ]
        )
        self.assertEqual(
            pair_coordinate_anchor_priority1_rewrite_preflight["preflight_rows"][0][
                "preflight_status"
            ],
            "preflight_passed_pending_explicit_approval",
        )

    def test_high_value_glycyl_radical_no_template_guardrail_current_counts(
        self,
    ) -> None:
        guardrail = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_high_value_glycyl_radical_"
                "no_template_feature_guardrail_current702_20260601.json"
            )
        )

        self.assertEqual(
            guardrail["status"],
            "glycyl_radical_panel_no_template_feature_guardrail_ready_review_only",
        )
        self.assertEqual(guardrail["counts"]["panel_rows"], 2)
        self.assertEqual(guardrail["counts"]["heldout_final_only_rows"], 2)
        self.assertEqual(guardrail["counts"]["score_complete_rows"], 2)
        self.assertEqual(guardrail["counts"]["abstained_at_research_threshold"], 2)
        self.assertEqual(guardrail["counts"]["rows_present_in_p0_train_cal_readiness"], 0)
        self.assertEqual(guardrail["counts"]["rows_present_in_train_cal_feature_contract"], 0)
        self.assertEqual(
            guardrail["counts"]["rows_allowed_for_no_template_feature_contract_refresh"],
            0,
        )
        self.assertEqual(
            [row["entry_id"] for row in guardrail["row_guardrails"]],
            ["m_csa:30", "m_csa:31"],
        )
        self.assertFalse(guardrail["guardrails"]["feature_contract_mutated"])
        self.assertFalse(
            guardrail["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )

    def test_mechanism_feature_inorganic_cofactor_locus_schema_current_counts(
        self,
    ) -> None:
        schema = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_inorganic_cofactor_locus_schema_current702_20260601.json"
        )

        self.assertEqual(
            schema["status"],
            "inorganic_cofactor_locus_schema_ready_review_only",
        )
        self.assertEqual(schema["counts"]["current702_manifest_rows"], 702)
        self.assertEqual(schema["counts"]["geometry_feature_rows_in_current702"], 698)
        self.assertEqual(schema["counts"]["organic_cofactor_row_class_records"], 2106)
        self.assertEqual(schema["counts"]["active_site_role_graph_ok_rows"], 656)
        self.assertEqual(
            schema["counts"]["proximal_context_counts"],
            {
                "cobalamin": 4,
                "fe_s_cluster": 17,
                "metal_ion": 176,
                "sam": 8,
            },
        )
        self.assertEqual(
            schema["counts"]["structure_wide_context_counts"],
            {
                "cobalamin": 4,
                "fe_s_cluster": 29,
                "metal_ion": 264,
                "sam": 11,
            },
        )
        by_class = {row["class_id"]: row for row in schema["schema_classes"]}
        self.assertEqual(set(by_class), {
            "metal_ion_locus",
            "cobalamin_locus",
            "radical_sam_locus",
            "iron_sulfur_locus",
        })
        self.assertIn(
            "structure_wide_only_flag",
            by_class["cobalamin_locus"]["required_fields"],
        )
        self.assertFalse(schema["guardrails"]["new_coordinates_or_models_downloaded"])
        self.assertTrue(schema["guardrails"]["review_only"])

    def test_mechanism_feature_inorganic_cofactor_locus_completion_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_inorganic_cofactor_locus_completion_audit_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "inorganic_cofactor_locus_completion_audit_passed_review_only",
        )
        self.assertEqual(audit["counts"]["schema_classes"], 4)
        self.assertEqual(audit["counts"]["materialized_sidecar_classes"], 4)
        self.assertEqual(audit["counts"]["schema_audit_passed_classes"], 4)
        self.assertEqual(audit["counts"]["critical_violation_total"], 0)
        self.assertEqual(audit["counts"]["predictive_use_allowed_rows"], 0)
        self.assertEqual(audit["counts"]["ready_for_label_import_rows"], 0)
        self.assertEqual(
            audit["counts"]["sidecar_rows_per_class"],
            {
                "cobalamin_locus": 702,
                "iron_sulfur_locus": 702,
                "metal_ion_locus": 702,
                "radical_sam_locus": 702,
            },
        )
        self.assertEqual(
            {row["class_id"] for row in audit["class_rows"]},
            {
                "cobalamin_locus",
                "iron_sulfur_locus",
                "metal_ion_locus",
                "radical_sam_locus",
            },
        )
        self.assertFalse(audit["guardrails"]["new_coordinates_or_models_downloaded"])
        self.assertTrue(audit["guardrails"]["review_only"])

    def test_mechanism_feature_metal_ion_locus_sidecar_current_counts(self) -> None:
        sidecar = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_metal_ion_locus_sidecar_current702_20260601.json"
        )

        self.assertEqual(
            sidecar["status"],
            "metal_ion_locus_sidecar_ready_review_only",
        )
        self.assertEqual(sidecar["counts"]["rows"], 702)
        self.assertEqual(
            sidecar["counts"]["status_counts"],
            {
                "no_metal_context_detected": 422,
                "proximal_metal_context_available": 175,
                "structure_wide_metal_context_only": 85,
                "unsupported_or_missing_geometry": 20,
            },
        )
        self.assertEqual(sidecar["counts"]["proximal_context_rows"], 175)
        self.assertEqual(sidecar["counts"]["structure_wide_only_rows"], 85)
        self.assertEqual(sidecar["counts"]["ready_for_label_import_rows"], 0)
        self.assertEqual(sidecar["counts"]["predictive_use_allowed_rows"], 0)
        self.assertEqual(
            sidecar["counts"]["top_proximal_metal_codes"]["MG"],
            65,
        )
        self.assertEqual(
            sidecar["counts"]["top_proximal_metal_codes"]["ZN"],
            61,
        )
        by_entry = {row["entry_id"]: row for row in sidecar["rows"]}
        self.assertEqual(
            by_entry["m_csa:4"]["sidecar_status"],
            "proximal_metal_context_available",
        )
        self.assertIn("CU", by_entry["m_csa:4"]["supporting_ligand_codes"])
        self.assertFalse(sidecar["guardrails"]["new_coordinates_or_models_downloaded"])
        self.assertTrue(sidecar["guardrails"]["review_only"])

    def test_mechanism_feature_metal_ion_locus_sidecar_schema_audit_current(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_metal_ion_locus_sidecar_schema_audit_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "metal_ion_locus_sidecar_schema_passed_current702",
        )
        self.assertEqual(audit["counts"]["manifest_rows"], 702)
        self.assertEqual(audit["counts"]["sidecar_rows"], 702)
        self.assertEqual(
            audit["counts"]["status_counts"],
            {
                "no_metal_context_detected": 422,
                "proximal_metal_context_available": 175,
                "structure_wide_metal_context_only": 85,
                "unsupported_or_missing_geometry": 20,
            },
        )
        self.assertTrue(
            all(
                count == 0
                for count in audit["counts"]["critical_counts"].values()
            )
        )
        self.assertFalse(audit["guardrails"]["new_coordinates_or_models_downloaded"])
        self.assertTrue(audit["guardrails"]["review_only"])

    def test_mechanism_feature_cobalamin_locus_sidecar_current_counts(self) -> None:
        sidecar = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_cobalamin_locus_sidecar_current702_20260601.json"
        )

        self.assertEqual(
            sidecar["status"],
            "cobalamin_locus_sidecar_ready_review_only",
        )
        self.assertEqual(sidecar["counts"]["rows"], 702)
        self.assertEqual(
            sidecar["counts"]["status_counts"],
            {
                "no_cobalamin_context_detected": 678,
                "proximal_cobalamin_context_available": 4,
                "unsupported_or_missing_geometry": 20,
            },
        )
        self.assertEqual(sidecar["counts"]["top_proximal_cobalamin_codes"]["B12"], 2)
        self.assertEqual(sidecar["counts"]["top_proximal_cobalamin_codes"]["COB"], 2)
        self.assertEqual(sidecar["counts"]["ready_for_label_import_rows"], 0)
        by_entry = {row["entry_id"]: row for row in sidecar["rows"]}
        self.assertEqual(
            by_entry["m_csa:62"]["sidecar_status"],
            "proximal_cobalamin_context_available",
        )
        self.assertIn("B12", by_entry["m_csa:62"]["supporting_ligand_codes"])

    def test_mechanism_feature_cobalamin_locus_sidecar_schema_audit_current(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_cobalamin_locus_sidecar_schema_audit_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "cobalamin_locus_sidecar_schema_passed_current702",
        )
        self.assertEqual(audit["counts"]["manifest_rows"], 702)
        self.assertEqual(audit["counts"]["sidecar_rows"], 702)
        self.assertTrue(
            all(
                count == 0
                for count in audit["counts"]["critical_counts"].values()
            )
        )
        self.assertTrue(audit["guardrails"]["review_only"])

    def test_mechanism_feature_radical_sam_and_iron_sulfur_locus_sidecars(
        self,
    ) -> None:
        expected = {
            "radical_sam": {
                "status": "radical_sam_locus_sidecar_ready_review_only",
                "status_counts": {
                    "no_radical_sam_context_detected": 672,
                    "proximal_radical_sam_context_available": 8,
                    "structure_wide_radical_sam_context_only": 2,
                    "unsupported_or_missing_geometry": 20,
                },
                "proximal_context_rows": 8,
                "structure_wide_only_rows": 2,
                "example_entry": "m_csa:358",
                "example_code": "SAM",
            },
            "iron_sulfur": {
                "status": "iron_sulfur_locus_sidecar_ready_review_only",
                "status_counts": {
                    "no_iron_sulfur_context_detected": 654,
                    "proximal_iron_sulfur_context_available": 17,
                    "structure_wide_iron_sulfur_context_only": 11,
                    "unsupported_or_missing_geometry": 20,
                },
                "proximal_context_rows": 17,
                "structure_wide_only_rows": 11,
                "example_entry": "m_csa:358",
                "example_code": "SF4",
            },
        }
        for kind, spec in expected.items():
            sidecar = _load_json(
                ROOT
                / "artifacts"
                / f"v3_mechanism_feature_{kind}_locus_sidecar_current702_20260601.json"
            )
            self.assertEqual(sidecar["status"], spec["status"])
            self.assertEqual(sidecar["counts"]["rows"], 702)
            self.assertEqual(
                sidecar["counts"]["status_counts"],
                spec["status_counts"],
            )
            self.assertEqual(
                sidecar["counts"]["proximal_context_rows"],
                spec["proximal_context_rows"],
            )
            self.assertEqual(
                sidecar["counts"]["structure_wide_only_rows"],
                spec["structure_wide_only_rows"],
            )
            self.assertEqual(sidecar["counts"]["ready_for_label_import_rows"], 0)
            self.assertEqual(sidecar["counts"]["predictive_use_allowed_rows"], 0)
            by_entry = {row["entry_id"]: row for row in sidecar["rows"]}
            self.assertEqual(
                by_entry[spec["example_entry"]]["sam_fe_s_copresence_status"],
                "proximal_sam_and_fe_s_context",
            )
            self.assertIn(
                spec["example_code"],
                by_entry[spec["example_entry"]]["supporting_ligand_codes"],
            )
            self.assertFalse(sidecar["guardrails"]["new_coordinates_or_models_downloaded"])
            self.assertTrue(sidecar["guardrails"]["review_only"])

    def test_mechanism_feature_radical_sam_and_iron_sulfur_schema_audits(
        self,
    ) -> None:
        for kind in ("radical_sam", "iron_sulfur"):
            audit = _load_json(
                ROOT
                / "artifacts"
                / f"v3_mechanism_feature_{kind}_locus_sidecar_schema_audit_current702_20260601.json"
            )
            self.assertEqual(
                audit["status"],
                f"{kind}_locus_sidecar_schema_passed_current702",
            )
            self.assertEqual(audit["counts"]["manifest_rows"], 702)
            self.assertEqual(audit["counts"]["sidecar_rows"], 702)
            self.assertTrue(
                all(
                    count == 0
                    for count in audit["counts"]["critical_counts"].values()
                )
            )

    def test_embedding_plan_consumes_mechanism_feature_sidecar_schema_audit(self) -> None:
        plan = _load_json(
            ROOT
            / "artifacts"
            / "v3_learned_mechanism_feature_embedding_plan_current702_20260601.json"
        )

        schema = plan["current_data_readiness"][
            "mechanism_feature_sidecar_schema_audit"
        ]
        self.assertEqual(
            schema["status"],
            "mechanism_feature_sidecar_schema_passed_current702",
        )
        self.assertTrue(schema["schema_safe_for_train_cal_pilot"])
        self.assertEqual(
            plan["source_artifacts"]["mechanism_feature_sidecar_schema_audit"][
                "path"
            ],
            "artifacts/v3_mechanism_feature_sidecar_schema_audit_current702_20260601.json",
        )

    def test_mechanism_feature_embedding_train_cal_input_manifest_current_counts(
        self,
    ) -> None:
        manifest = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_embedding_train_cal_input_manifest_current702_20260601.json"
        )

        self.assertEqual(
            manifest["status"],
            "train_cal_input_manifest_ready_no_model_fit",
        )
        self.assertEqual(manifest["counts"]["manifest_rows"], 702)
        self.assertEqual(manifest["counts"]["train_cal_candidate_rows"], 562)
        self.assertEqual(manifest["counts"]["heldout_excluded_rows"], 140)
        self.assertEqual(manifest["counts"]["minimal_feature_bundle_ready_rows"], 524)
        self.assertEqual(
            manifest["counts"]["role_graph_status_counts_train_cal"]["ok"],
            524,
        )
        self.assertEqual(
            manifest["counts"]["reaction_template_status_counts_train_cal"][
                "template_available"
            ],
            184,
        )
        self.assertEqual(
            manifest["counts"]["inorganic_completion_critical_violation_total"],
            0,
        )
        self.assertFalse(manifest["guardrails"]["model_weights_fit_or_refit"])
        self.assertFalse(
            manifest["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )
        self.assertEqual(len(manifest["row_records"]), 562)
        self.assertTrue(manifest["row_records"][0]["minimal_train_cal_feature_bundle_ready"])
        self.assertIn("metal_ion_locus", manifest["locus_status_counts_train_cal"])

    def test_mechanism_feature_embedding_train_cal_split_manifest_current_counts(
        self,
    ) -> None:
        manifest = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.json"
        )

        self.assertEqual(
            manifest["status"],
            "mechanism_feature_embedding_train_cal_split_ready_no_model_fit",
        )
        self.assertEqual(manifest["counts"]["minimal_feature_bundle_ready_rows"], 524)
        self.assertEqual(manifest["counts"]["split_rows"], 524)
        self.assertEqual(manifest["counts"]["train_rows"], 418)
        self.assertEqual(manifest["counts"]["calibration_rows"], 106)
        self.assertEqual(manifest["counts"]["heldout_excluded_rows"], 140)
        self.assertEqual(manifest["counts"]["not_ready_rows"], 38)
        self.assertEqual(manifest["counts"]["strata"], 6)
        self.assertFalse(manifest["guardrails"]["model_weights_fit_or_refit"])
        self.assertFalse(manifest["guardrails"]["threshold_selected_or_tuned"])
        self.assertFalse(
            manifest["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )
        self.assertEqual(
            manifest["stratum_counts"]["fingerprint:metal_dependent_hydrolase"],
            {"calibration": 13, "total": 64, "train": 51},
        )
        self.assertEqual(
            manifest["stratum_counts"]["label_type:out_of_scope"],
            {"calibration": 71, "total": 353, "train": 282},
        )
        self.assertEqual(
            manifest["counts"]["not_ready_reason_counts"],
            {
                "role_graph:missing_accession_compatible_sequence_positions": 34,
                "role_graph:missing_catalytic_residue_nodes": 1,
                "role_graph:not_m_csa_no_curated_active_site_roles": 3,
            },
        )
        split_counts = Counter(
            row["assigned_embedding_split"] for row in manifest["split_records"]
        )
        self.assertEqual(dict(split_counts), {"train": 418, "calibration": 106})
        self.assertEqual(manifest["split_records"][0]["entry_id"], "m_csa:1")
        self.assertEqual(
            manifest["split_records"][1]["assigned_embedding_split"],
            "calibration",
        )

    def test_mechanism_feature_embedding_feature_contract_current_counts(
        self,
    ) -> None:
        contract = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_embedding_feature_contract_current702_20260601.json"
        )

        self.assertEqual(
            contract["status"],
            "mechanism_feature_embedding_feature_contract_ready_no_model_fit",
        )
        self.assertEqual(contract["counts"]["feature_rows"], 524)
        self.assertEqual(contract["counts"]["train_rows"], 418)
        self.assertEqual(contract["counts"]["calibration_rows"], 106)
        self.assertEqual(contract["counts"]["heldout_excluded_rows"], 140)
        self.assertEqual(contract["counts"]["missing_input_records"], 0)
        self.assertFalse(contract["guardrails"]["model_weights_fit_or_refit"])
        self.assertTrue(contract["guardrails"]["label_fields_excluded_from_feature_rows"])
        self.assertFalse(contract["guardrails"]["heldout_rows_present_in_feature_rows"])
        self.assertIn("fingerprint_id", contract["excluded_fields_as_features"])
        self.assertIn("label_type", contract["excluded_fields_as_features"])
        self.assertEqual(
            [group["name"] for group in contract["feature_groups"]],
            [
                "active_site_role_graph",
                "reaction_center_template",
                "organic_cofactor_scores",
                "inorganic_cofactor_loci",
            ],
        )
        first = contract["feature_rows"][0]
        self.assertNotIn("fingerprint_id", first)
        self.assertNotIn("label_type", first)
        self.assertIn("active_site_role_graph", first)

    def test_mechanism_feature_embedding_feature_contract_strict_audit_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_embedding_feature_contract_"
                "strict_audit_current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "mechanism_feature_embedding_feature_contract_strict_audit_passed_no_model_fit",
        )
        self.assertEqual(audit["counts"]["feature_rows"], 524)
        self.assertEqual(audit["counts"]["split_manifest_rows"], 524)
        self.assertEqual(audit["counts"]["row_audits_passed"], 524)
        self.assertEqual(audit["counts"]["row_audits_blocked"], 0)
        self.assertEqual(audit["counts"]["train_rows"], 418)
        self.assertEqual(audit["counts"]["calibration_rows"], 106)
        self.assertEqual(audit["counts"]["heldout_excluded_rows"], 140)
        self.assertEqual(audit["counts"]["critical_violation_total"], 0)
        self.assertEqual(audit["counts"]["critical_counts"], {})
        self.assertFalse(audit["guardrails"]["model_weights_fit_or_refit"])
        self.assertFalse(audit["guardrails"]["threshold_selected_or_tuned"])
        self.assertFalse(
            audit["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )
        self.assertEqual(audit["row_audits"][0]["entry_id"], "m_csa:1")
        self.assertEqual(audit["row_audits"][0]["critical_violations"], [])

    def test_mechanism_feature_embedding_pilot_current_counts(self) -> None:
        pilot = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_embedding_pilot_current702_20260601.json"
        )

        self.assertEqual(
            pilot["status"],
            "mechanism_feature_embedding_pilot_fit_train_cal_ready",
        )
        self.assertEqual(pilot["counts"]["feature_rows"], 524)
        self.assertEqual(pilot["counts"]["train_rows"], 418)
        self.assertEqual(pilot["counts"]["calibration_rows"], 106)
        self.assertEqual(pilot["counts"]["heldout_excluded_rows"], 140)
        self.assertEqual(pilot["counts"]["variants"], 2)
        self.assertEqual(pilot["counts"]["missing_label_rows"], 0)
        self.assertEqual(
            pilot["counts"]["missing_three_organic_cofactor_score_rows"], 0
        )
        self.assertEqual(
            pilot["best_calibration_variant"],
            "full_contract_with_reaction_template",
        )
        by_variant = {
            variant["variant_name"]: variant
            for variant in pilot["pilot_variants"]
        }
        self.assertAlmostEqual(
            by_variant["full_contract_with_reaction_template"][
                "calibration_summary"
            ]["auc_primary_vs_oos"],
            0.948491,
        )
        self.assertAlmostEqual(
            by_variant["full_contract_with_reaction_template"][
                "calibration_selected_threshold"
            ]["oos_abstain_recall"],
            1.0,
        )
        self.assertAlmostEqual(
            by_variant["no_reaction_template_ablation"][
                "calibration_summary"
            ]["auc_primary_vs_oos"],
            0.549698,
        )
        self.assertTrue(pilot["guardrails"]["model_weights_fit_or_refit"])
        self.assertEqual(pilot["guardrails"]["model_fit_rows"], "train_only")
        self.assertEqual(
            pilot["guardrails"]["threshold_selection_rows"],
            "calibration_only",
        )
        self.assertFalse(
            pilot["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )
        self.assertFalse(pilot["guardrails"]["heldout_rows_evaluated"])

    def test_mechanism_feature_embedding_heldout_readout_current_counts(self) -> None:
        readout = _load_json(
            ROOT
            / "artifacts"
            / "v3_mechanism_feature_embedding_heldout_readout_current702_20260601.json"
        )

        self.assertEqual(
            readout["status"],
            "mechanism_feature_embedding_heldout_readout_applied_once",
        )
        self.assertEqual(readout["counts"]["heldout_rows_total"], 140)
        self.assertEqual(readout["counts"]["heldout_feature_rows"], 132)
        self.assertEqual(readout["counts"]["heldout_feature_missing_rows"], 8)
        self.assertEqual(
            readout["counts"]["blocker_counts"],
            {"role_graph:missing_accession_compatible_sequence_positions": 8},
        )
        by_variant = {
            variant["variant_name"]: variant
            for variant in readout["variant_readouts"]
        }
        self.assertAlmostEqual(
            by_variant["full_contract_with_reaction_template"][
                "heldout_summary"
            ]["auc_primary_vs_oos"],
            0.8812,
        )
        self.assertAlmostEqual(
            by_variant["full_contract_with_reaction_template"][
                "heldout_threshold_readout"
            ]["primary_retain_recall"],
            0.75,
        )
        self.assertAlmostEqual(
            by_variant["full_contract_with_reaction_template"][
                "heldout_threshold_readout"
            ]["oos_abstain_recall"],
            1.0,
        )
        self.assertAlmostEqual(
            by_variant["no_reaction_template_ablation"][
                "heldout_summary"
            ]["auc_primary_vs_oos"],
            0.488591,
        )
        self.assertFalse(readout["guardrails"]["model_weights_fit_or_refit"])
        self.assertFalse(readout["guardrails"]["threshold_selected_or_tuned"])
        self.assertTrue(readout["guardrails"]["heldout_rows_evaluated_once"])
        self.assertFalse(
            readout["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )

    def test_mechanism_feature_embedding_train_cal_guardrail_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_mechanism_feature_embedding_train_cal_guardrail_audit_"
                "current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "mechanism_feature_embedding_train_cal_guardrail_audit_passed_review_only",
        )
        self.assertEqual(audit["counts"]["input_manifest_rows"], 562)
        self.assertEqual(audit["counts"]["input_heldout_excluded_rows"], 140)
        self.assertEqual(audit["counts"]["split_rows"], 524)
        self.assertEqual(audit["counts"]["feature_rows"], 524)
        self.assertEqual(audit["counts"]["train_rows"], 418)
        self.assertEqual(audit["counts"]["calibration_rows"], 106)
        self.assertEqual(audit["counts"]["split_minus_input_rows"], 0)
        self.assertEqual(audit["counts"]["feature_minus_split_rows"], 0)
        self.assertEqual(audit["counts"]["split_minus_feature_rows"], 0)
        self.assertEqual(audit["counts"]["feature_rows_marked_heldout"], 0)
        self.assertEqual(audit["counts"]["feature_rows_with_fingerprint_id_feature_leak"], 0)
        self.assertEqual(audit["counts"]["feature_rows_with_label_type_feature_leak"], 0)
        self.assertEqual(audit["counts"]["feature_rows_with_stratum_feature_leak"], 0)
        self.assertEqual(
            audit["not_ready_reason_counts"],
            {
                "role_graph:missing_accession_compatible_sequence_positions": 34,
                "role_graph:missing_catalytic_residue_nodes": 1,
                "role_graph:not_m_csa_no_curated_active_site_roles": 3,
            },
        )
        self.assertFalse(audit["guardrails"]["heldout_rows_present_in_feature_rows"])
        self.assertFalse(audit["guardrails"]["model_weights_fit_or_refit"])
        self.assertFalse(audit["guardrails"]["threshold_selected_or_tuned"])

    def test_current_run_artifact_integrity_audit_current_counts(self) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_current_run_artifact_integrity_audit_current702_20260601.json"
        )

        self.assertEqual(audit["status"], "current_run_artifact_integrity_audit_passed")
        self.assertEqual(audit["schema_version"], "current_run_artifact_integrity.v2")
        self.assertEqual(audit["counts"]["json_artifacts_checked"], 30)
        self.assertEqual(audit["counts"]["json_artifacts_parse_passed"], 30)
        self.assertEqual(audit["counts"]["work_reports_checked"], 30)
        self.assertEqual(audit["counts"]["work_reports_present"], 30)
        self.assertEqual(audit["counts"]["repo_json_artifacts_parse_checked"], 3142)
        self.assertEqual(audit["counts"]["repo_jsonl_artifacts_parse_checked"], 26)
        self.assertEqual(audit["counts"]["repo_json_parse_error_count"], 0)
        self.assertEqual(audit["counts"]["label_registry_mutations"], 0)
        self.assertEqual(audit["counts"]["new_coordinates_fetched"], 0)
        self.assertEqual(audit["counts"]["predicted_geometry_scores_created"], 0)
        self.assertEqual(
            audit["counts"]["fold_channel_carryover_resolution_artifacts"],
            1,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["fold_augmented_confounded_deployment_closure_audit_artifacts"],
            1,
        )
        self.assertEqual(
            audit["counts"]["mechanism_feature_p0_refresh_blocker_audit_artifacts"],
            1,
        )
        self.assertEqual(
            audit["counts"]["mechanism_feature_p0_feature_readiness_audit_artifacts"],
            1,
        )
        self.assertEqual(
            audit["counts"]["mechanism_feature_p0_train_cal_feature_sidecar_artifacts"],
            1,
        )
        self.assertEqual(
            audit[
                "counts"
            ][
                "mechanism_feature_p0_train_cal_feature_guardrail_audit_artifacts"
            ],
            1,
        )
        self.assertEqual(
            audit["counts"]["mechanism_feature_p0_train_cal_coverage_gap_artifacts"],
            1,
        )
        self.assertEqual(
            audit["counts"]["mechanism_feature_p0_calibration_review_packet_artifacts"],
            1,
        )
        self.assertEqual(
            audit["counts"]["predicted_atlas_vs_fold_novelty_delta_artifacts"],
            1,
        )
        self.assertEqual(
            audit["counts"]["mechanism_feature_p0_rhea_lookup_resolution_artifacts"],
            1,
        )
        self.assertEqual(
            audit[
                "counts"
            ][
                "mechanism_feature_p0_rhea_resolution_consumption_audit_artifacts"
            ],
            1,
        )
        self.assertEqual(
            audit[
                "counts"
            ][
                "mechanism_feature_p0_rhea_unresolved_official_source_audit_artifacts"
            ],
            1,
        )
        self.assertEqual(
            audit["counts"]["mechanism_feature_p0_reviewer_decision_matrix_artifacts"],
            1,
        )
        self.assertEqual(
            audit["counts"]["family_panel_no_template_feature_guardrail_artifacts"],
            1,
        )
        self.assertFalse(audit["guardrails"]["labels_registries_ontologies_changed"])
        self.assertFalse(audit["guardrails"]["production_thresholds_changed"])
        self.assertFalse(audit["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(audit["guardrails"]["model_weights_fit_or_refit"])
        self.assertTrue(
            all(count == 0 for count in audit["critical_counts"].values())
        )
        self.assertEqual(len(audit["artifact_rows"]), 30)
        self.assertEqual(
            audit["artifact_rows"][-1]["category"],
            "docs_reference_check",
        )

    def test_thiol_disulfide_family_panel_packet_current_counts(self) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_evidence_packet_thiol_disulfide_oxidoreductase_isomerase_boundary_current702_20260601.json"
        )

        self.assertEqual(packet["status"], "evidence_packet_ready_review_only")
        self.assertEqual(packet["panel"]["candidate_family"], "thiol_disulfide_oxidoreductase_isomerase_boundary")
        self.assertEqual(packet["counts"]["candidate_rows"], 1)
        self.assertEqual(packet["counts"]["predicted_geometry_ok_rows"], 1)
        self.assertEqual(packet["counts"]["rows_with_predicted_structure_fold_hits"], 1)
        self.assertEqual(packet["row_evidence"][0]["entry_id"], "m_csa:191")
        self.assertEqual(
            packet["row_evidence"][0]["predicted_structure_fold_channel"][
                "nearest_atlas_tm_score"
            ],
            0.3863,
        )

    def test_flavin_monooxygenase_family_panel_packet_current_counts(self) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_evidence_packet_flavin_monooxygenase_and_flavin_oxygen_transfer_current702_20260601.json"
        )

        self.assertEqual(packet["status"], "evidence_packet_ready_review_only")
        self.assertEqual(packet["panel"]["candidate_family"], "flavin_monooxygenase_and_flavin_oxygen_transfer")
        self.assertEqual(packet["counts"]["candidate_rows"], 4)
        self.assertEqual(packet["counts"]["predicted_geometry_ok_rows"], 4)
        self.assertEqual(packet["counts"]["rows_with_predicted_structure_fold_hits"], 3)
        self.assertEqual(packet["counts"]["missing_geometry_entry_ids"], [])
        by_entry = {row["entry_id"]: row for row in packet["row_evidence"]}
        self.assertEqual(
            by_entry["m_csa:131"]["predicted_structure_fold_channel"][
                "nearest_atlas_tm_score"
            ],
            0.751,
        )
        self.assertEqual(
            by_entry["m_csa:551"]["predicted_structure_fold_channel"][
                "nearest_atlas_tm_score"
            ],
            0.7309,
        )
        self.assertEqual(
            by_entry["m_csa:132"]["predicted_structure_fold_channel"][
                "score_source"
            ],
            "m_csa_primary_channel_repair",
        )

    def test_remaining_family_panel_packets_current_counts(self) -> None:
        expected = {
            "v3_family_panel_evidence_packet_cobalamin_and_radical_rearrangement_panel_current702_20260601.json": {
                "candidate_rows": 3,
                "predicted_geometry_ok_rows": 2,
                "rows_with_predicted_structure_fold_hits": 3,
            },
            "v3_family_panel_evidence_packet_no_reliable_structure_metal_hydrolase_controls_current702_20260601.json": {
                "candidate_rows": 6,
                "predicted_geometry_ok_rows": 1,
                "rows_with_predicted_structure_fold_hits": 6,
            },
            "v3_family_panel_evidence_packet_near_orphan_glycoside_or_nucleoside_hydrolase_controls_current702_20260601.json": {
                "candidate_rows": 4,
                "predicted_geometry_ok_rows": 3,
                "rows_with_predicted_structure_fold_hits": 4,
            },
        }
        for filename, counts in expected.items():
            packet = _load_json(ROOT / "artifacts" / filename)
            self.assertEqual(packet["status"], "evidence_packet_ready_with_geometry_gaps")
            for key, value in counts.items():
                self.assertEqual(packet["counts"][key], value)
        no_reliable = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_evidence_packet_no_reliable_structure_metal_hydrolase_controls_current702_20260601.json"
        )
        by_entry = {row["entry_id"]: row for row in no_reliable["row_evidence"]}
        self.assertEqual(
            by_entry["mh_066"]["predicted_geometry_score_source"],
            "family_panel_source_free_predicted_geometry_retrieval",
        )
        near_orphan = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_evidence_packet_near_orphan_glycoside_or_nucleoside_hydrolase_controls_current702_20260601.json"
        )
        by_entry = {row["entry_id"]: row for row in near_orphan["row_evidence"]}
        self.assertEqual(
            by_entry["mh_073"]["predicted_geometry_score_source"],
            "family_panel_source_free_predicted_geometry_retrieval",
        )

    def test_fold_augmented_family_panel_research_readout_current_counts(self) -> None:
        readout = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_family_panel_research_readout_current702_20260601.json"
        )

        self.assertEqual(
            readout["status"],
            "family_panel_research_readout_ready_review_only",
        )
        self.assertEqual(readout["threshold_source"]["threshold"], 0.44155)
        self.assertEqual(readout["counts"]["panel_packets"], 7)
        self.assertEqual(readout["counts"]["candidate_rows"], 22)
        self.assertEqual(readout["counts"]["primary_score_complete_rows"], 17)
        self.assertEqual(readout["counts"]["non_abstained_at_research_threshold"], 11)
        self.assertEqual(readout["counts"]["abstained_at_research_threshold"], 6)
        self.assertEqual(readout["counts"]["not_score_complete_for_primary_channel"], 5)
        self.assertEqual(
            [row["entry_id"] for row in readout["review_priority_rows"]],
            [
                "mh_068",
                "mh_067",
                "mh_066",
                "m_csa:267",
                "m_csa:131",
                "m_csa:750",
                "m_csa:551",
                "m_csa:132",
                "mh_073",
                "secondary_probe::radical_sam_enzyme",
                "m_csa:116",
            ],
        )
        by_entry = {row["entry_id"]: row for row in readout["row_scores"]}
        self.assertEqual(
            by_entry["m_csa:973"]["predicted_structure_fold_score_source"],
            "fold_augmented_train_cal_threshold_contract_calibration_row",
        )
        self.assertEqual(
            by_entry["m_csa:973"]["research_gate_status"],
            "abstained_at_research_threshold",
        )
        self.assertEqual(
            by_entry["mh_066"]["predicted_geometry_score_source"],
            "family_panel_packet_predicted_geometry_top1",
        )
        self.assertEqual(
            by_entry["mh_067"]["predicted_geometry_score_source"],
            "family_panel_source_free_predicted_geometry_retrieval",
        )
        self.assertEqual(
            by_entry["mh_068"]["research_gate_status"],
            "non_abstained_at_research_threshold",
        )
        self.assertEqual(
            by_entry["secondary_probe::radical_sam_enzyme"][
                "research_gate_status"
            ],
            "non_abstained_at_research_threshold",
        )
        self.assertTrue(readout["guardrails"]["review_only"])
        self.assertFalse(readout["guardrails"]["thresholds_selected_on_family_panel_rows"])

    def test_fold_augmented_family_panel_countability_gate_preflight_current_counts(
        self,
    ) -> None:
        preflight = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_family_panel_countability_gate_preflight_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            preflight["status"],
            "family_panel_countability_gate_preflight_ready_no_countable_rows",
        )
        self.assertEqual(preflight["counts"]["coverage_candidate_rows"], 22)
        self.assertEqual(preflight["counts"]["readout_candidate_rows"], 22)
        self.assertEqual(preflight["counts"]["primary_score_complete_rows"], 17)
        self.assertEqual(preflight["counts"]["non_abstained_review_rows"], 11)
        self.assertEqual(preflight["counts"]["abstained_review_rows"], 6)
        self.assertEqual(preflight["counts"]["missing_primary_channel_rows"], 5)
        self.assertEqual(preflight["counts"]["source_check_queue_rows_joined"], 11)
        self.assertEqual(
            preflight["counts"]["source_check_completed_rows_joined"], 11
        )
        self.assertEqual(
            preflight["counts"]["source_check_pending_rows_joined"], 0
        )
        self.assertEqual(
            preflight["counts"][
                "source_check_completed_no_family_promotion_rows"
            ],
            11,
        )
        self.assertEqual(
            preflight["counts"]["locator_human_or_policy_blocked_rows_joined"],
            5,
        )
        self.assertEqual(preflight["counts"]["import_preview_ready_rows"], 0)
        self.assertEqual(preflight["counts"]["label_factory_gate_ready_rows"], 0)
        self.assertEqual(
            preflight["counts"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(
            preflight["counts"]["blocker_counts"],
            {
                "completed_source_check_not_family_promotion_ready": 11,
                "countable_import_preview_missing": 22,
                "label_factory_gate_not_run_for_family_panel_row": 22,
                "primary_channel_score_missing": 5,
                "review_packet_not_expert_import_decision": 22,
                "source_free_locator_human_or_policy_decision_required": 5,
            },
        )
        self.assertFalse(preflight["decision"]["new_countable_labels_authorized"])
        self.assertFalse(preflight["decision"]["countable_label_import_ready"])
        self.assertFalse(preflight["decision"]["label_factory_gate_ready"])
        self.assertTrue(preflight["decision"]["source_checks_fully_reconciled"])
        self.assertEqual(
            preflight["decision"]["countable_label_candidate_entry_ids"], []
        )
        panel_by_id = {
            row["panel_id"]: row for row in preflight["panel_gate_summaries"]
        }
        self.assertEqual(
            panel_by_id["no_reliable_structure_metal_hydrolase_controls"][
                "geometry_or_locator_blocked_rows"
            ],
            3,
        )
        by_entry = {
            row["entry_id"]: row for row in preflight["row_gate_status"]
        }
        self.assertIn(
            "completed_source_check_not_family_promotion_ready",
            by_entry["mh_066"]["gate_blockers"],
        )
        self.assertIn(
            "source_free_locator_human_or_policy_decision_required",
            by_entry["mh_064"]["gate_blockers"],
        )
        self.assertFalse(
            any(row["countable_label_candidate"] for row in preflight["row_gate_status"])
        )
        self.assertTrue(preflight["guardrails"]["review_only"])
        self.assertFalse(
            preflight["guardrails"]["labels_registries_ontologies_changed"]
        )

    def test_fold_augmented_family_panel_import_preview_blocker_gate_current_counts(
        self,
    ) -> None:
        gate = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_family_panel_import_preview_blocker_gate_"
                "current702_20260602.json"
            )
        )

        self.assertEqual(
            gate["status"],
            "family_panel_import_preview_blocker_gate_ready_blocked",
        )
        self.assertEqual(gate["counts"]["review_rows_evaluated"], 22)
        self.assertEqual(gate["counts"]["panels_represented"], 7)
        self.assertEqual(
            gate["counts"]["rows_blocked_before_import_preview"], 22
        )
        self.assertEqual(gate["counts"]["import_preview_ready_rows"], 0)
        self.assertEqual(gate["counts"]["label_factory_gate_ready_rows"], 0)
        self.assertEqual(gate["counts"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            gate["counts"]["rows_blocked_by_expert_import_decision"], 22
        )
        self.assertEqual(
            gate["counts"]["rows_blocked_by_locator_or_primary_channel"], 5
        )
        self.assertEqual(
            gate["counts"]["rows_with_completed_review_only_source_check"], 11
        )
        self.assertEqual(
            gate["counts"][
                "rows_blocked_by_completed_source_check_no_promotion"
            ],
            11,
        )
        self.assertEqual(
            gate["counts"]["primary_blocker_class_counts"],
            {
                "completed_source_check_review_only_no_promotion": 11,
                "expert_family_admission_decision_required": 6,
                "source_free_locator_or_primary_channel_missing": 5,
            },
        )
        self.assertEqual(
            gate["counts"]["priority_rows_with_locator_decision_class"], 5
        )
        self.assertEqual(
            gate["counts"][
                "priority_rows_requiring_human_or_policy_decision"
            ],
            5,
        )
        self.assertEqual(
            gate["counts"]["priority_rows_mechanically_clearable_now"], 0
        )
        self.assertTrue(gate["decision"]["source_checks_fully_reconciled"])
        self.assertFalse(gate["decision"]["import_preview_can_run"])
        self.assertFalse(gate["decision"]["new_countable_labels_authorized"])
        self.assertTrue(
            gate["decision"]["all_priority_rows_human_or_policy_blocked"]
        )
        self.assertEqual(
            gate["decision"]["priority_next_entry_ids"],
            [
                "secondary_probe::cobalamin_radical_rearrangement",
                "external_glycoside_panel",
                "mh_064",
                "mh_065",
                "mh_072",
            ],
        )
        self.assertEqual(
            gate["decision"]["priority_next_decision_class_order"],
            [
                "accession_equivalence_or_matching_coordinate_required",
                "ligand_specificity_validator_or_substrate_coordinate_required",
                "alternate_coordinate_fetch_approval_required",
                "nonlabel_locator_strategy_or_alternate_source_required",
            ],
        )
        self.assertIn(
            "No matching non-AFDB replacement coordinate is cached",
            gate["interpretation"]["next_action"],
        )
        by_entry = {row["entry_id"]: row for row in gate["row_blockers"]}
        self.assertEqual(
            by_entry["m_csa:131"]["primary_blocker_class"],
            "completed_source_check_review_only_no_promotion",
        )
        self.assertEqual(
            by_entry["m_csa:30"]["primary_blocker_class"],
            "expert_family_admission_decision_required",
        )
        self.assertEqual(
            by_entry["mh_064"]["primary_blocker_class"],
            "source_free_locator_or_primary_channel_missing",
        )
        self.assertEqual(
            by_entry["mh_067"]["primary_blocker_class"],
            "completed_source_check_review_only_no_promotion",
        )
        self.assertEqual(
            by_entry["secondary_probe::cobalamin_radical_rearrangement"][
                "locator_decision_class"
            ],
            "nonlabel_locator_strategy_or_alternate_source_required",
        )
        self.assertTrue(gate["guardrails"]["review_only"])
        self.assertFalse(gate["guardrails"]["imports_or_promotions_performed"])

    def test_fold_augmented_family_panel_expert_import_decision_packet_current_counts(
        self,
    ) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_family_panel_expert_import_decision_packet_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            packet["status"],
            "family_panel_expert_import_decision_packet_ready_review_only",
        )
        self.assertEqual(packet["counts"]["decision_stub_rows"], 22)
        self.assertEqual(packet["counts"]["panels_represented"], 7)
        self.assertEqual(
            packet["counts"]["pending_expert_import_decisions"], 22
        )
        self.assertEqual(packet["counts"]["accepted_decision_records"], 0)
        self.assertEqual(packet["counts"]["rejected_decision_records"], 0)
        self.assertEqual(
            packet["counts"]["import_preview_candidate_if_accepted_rows"], 6
        )
        self.assertEqual(
            packet["counts"]["family_promotion_override_needed_rows"], 11
        )
        self.assertEqual(
            packet["counts"]["locator_or_primary_channel_blocked_rows"], 5
        )
        self.assertEqual(
            packet["counts"]["primary_blocker_class_counts"],
            {
                "completed_source_check_review_only_no_promotion": 11,
                "expert_family_admission_decision_required": 6,
                "source_free_locator_or_primary_channel_missing": 5,
            },
        )
        self.assertIn(
            "expert_import_decisions_not_recorded", packet["blockers"]
        )
        self.assertIn(
            "family_promotion_override_decisions_missing", packet["blockers"]
        )
        self.assertIn(
            "locator_or_primary_channel_blockers_remain", packet["blockers"]
        )
        self.assertFalse(packet["decision"]["import_preview_can_run_now"])
        self.assertFalse(packet["decision"]["new_countable_labels_authorized"])
        by_entry = {
            row["entry_id"]: row
            for row in packet["expert_import_decision_stubs"]
        }
        self.assertTrue(
            by_entry["m_csa:30"]["import_preview_candidate_if_accepted_now"]
        )
        self.assertEqual(
            by_entry["m_csa:30"]["decision_field_to_update"], "decision"
        )
        self.assertEqual(
            by_entry["m_csa:30"]["review_status_field_to_update"],
            "review_status",
        )
        self.assertEqual(
            by_entry["m_csa:30"]["recommended_review_status_after_decision"],
            "reviewed_expert_import_decision",
        )
        self.assertFalse(
            by_entry["mh_064"]["import_preview_candidate_if_accepted_now"]
        )
        self.assertEqual(
            len(by_entry["m_csa:30"]["decision_context_sha256"]), 64
        )
        self.assertTrue(packet["guardrails"]["review_only"])
        self.assertFalse(packet["guardrails"]["imports_or_promotions_performed"])
        self.assertFalse(
            packet["guardrails"]["labels_registries_ontologies_changed"]
        )

    def test_fold_augmented_family_panel_acceptance_scenario_plan_current_counts(
        self,
    ) -> None:
        plan = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_family_panel_acceptance_scenario_plan_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            plan["status"],
            "family_panel_acceptance_scenario_plan_ready_review_only",
        )
        self.assertEqual(plan["counts"]["decision_stub_rows"], 22)
        self.assertEqual(plan["counts"]["acceptance_scenario_rows"], 6)
        self.assertEqual(plan["counts"]["non_preview_rows_if_accepted"], 16)
        self.assertEqual(plan["counts"]["panels_represented"], 5)
        self.assertEqual(
            plan["counts"][
                "label_factory_gate_candidate_rows_if_all_scenario_rows_accepted"
            ],
            6,
        )
        self.assertEqual(plan["counts"]["countable_label_candidate_count_now"], 0)
        self.assertEqual(
            plan["counts"]["scenario_rows_by_panel"],
            {
                "flavin_monooxygenase_and_flavin_oxygen_transfer": 1,
                "glycyl_radical_or_thiamine_radical_lyase_boundary": 2,
                "lipoamide_or_sulfur_transfer_redox_boundary": 1,
                "near_orphan_glycoside_or_nucleoside_hydrolase_controls": 1,
                "thiol_disulfide_oxidoreductase_isomerase_boundary": 1,
            },
        )
        self.assertEqual(
            plan["counts"]["non_preview_rows_by_primary_blocker"],
            {
                "completed_source_check_review_only_no_promotion": 11,
                "source_free_locator_or_primary_channel_missing": 5,
            },
        )
        self.assertIn("expert_import_decisions_not_recorded", plan["blockers"])
        self.assertFalse(plan["decision"]["apply_expert_decisions_now"])
        self.assertFalse(plan["decision"]["write_import_preview_now"])
        self.assertFalse(plan["decision"]["run_label_factory_gate_now"])
        scenario_entries = {
            row["entry_id"] for row in plan["acceptance_scenario_rows"]
        }
        self.assertEqual(
            scenario_entries,
            {"m_csa:10", "m_csa:30", "m_csa:31", "m_csa:191", "m_csa:448", "m_csa:973"},
        )
        self.assertTrue(plan["guardrails"]["review_only"])
        self.assertFalse(plan["guardrails"]["imports_or_promotions_performed"])
        self.assertFalse(
            plan["guardrails"]["labels_registries_ontologies_changed"]
        )

    def test_fold_augmented_family_panel_expert_import_decision_application_current_counts(
        self,
    ) -> None:
        application = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_family_panel_expert_import_decision_"
                "application_current702_20260603.json"
            )
        )

        self.assertEqual(
            application["status"],
            "family_panel_expert_import_decision_application_blocked",
        )
        self.assertEqual(application["counts"]["packet_stub_rows"], 22)
        self.assertEqual(application["counts"]["decision_records_total"], 22)
        self.assertEqual(application["counts"]["explicit_decision_records"], 0)
        self.assertEqual(application["counts"]["reviewed_decision_records"], 0)
        self.assertEqual(application["counts"]["pending_decision_rows"], 22)
        self.assertEqual(
            application["counts"]["accepted_import_preview_candidate_rows"], 0
        )
        self.assertEqual(
            application["counts"]["accepted_but_still_blocked_rows"], 0
        )
        self.assertEqual(application["counts"]["rejected_rows"], 0)
        self.assertEqual(application["counts"]["review_only_rows"], 0)
        self.assertEqual(application["counts"]["critical_violation_total"], 0)
        self.assertIn(
            "explicit_expert_import_decisions_missing",
            application["blockers"],
        )
        self.assertIn(
            "accepted_import_preview_candidate_rows_missing",
            application["blockers"],
        )
        self.assertFalse(application["decision"]["import_preview_can_run_now"])
        self.assertFalse(application["decision"]["new_countable_labels_authorized"])
        by_entry = {
            row["entry_id"]: row for row in application["row_decisions"]
        }
        self.assertEqual(by_entry["m_csa:30"]["decision"], "pending_review")
        self.assertFalse(
            by_entry["m_csa:30"]["accepted_import_preview_candidate"]
        )
        self.assertTrue(application["guardrails"]["review_only"])
        self.assertFalse(
            application["guardrails"]["imports_or_promotions_performed"]
        )
        self.assertFalse(
            application["guardrails"]["labels_registries_ontologies_changed"]
        )

    def test_fold_augmented_family_panel_accepted_import_preview_current_counts(
        self,
    ) -> None:
        preview = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_family_panel_accepted_import_preview_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            preview["status"],
            "family_panel_accepted_import_preview_blocked",
        )
        self.assertEqual(preview["counts"]["application_row_decisions"], 22)
        self.assertEqual(
            preview["counts"]["accepted_import_preview_candidate_rows"], 0
        )
        self.assertEqual(preview["counts"]["preview_rows"], 0)
        self.assertEqual(preview["counts"]["panels_represented"], 0)
        self.assertEqual(
            preview["counts"]["label_factory_gate_candidate_rows"], 0
        )
        self.assertEqual(preview["counts"]["countable_label_candidate_count"], 0)
        self.assertIn(
            "expert_import_decision_application_not_ready",
            preview["blockers"],
        )
        self.assertIn(
            "accepted_import_preview_candidate_rows_missing",
            preview["blockers"],
        )
        self.assertFalse(
            preview["decision"]["accepted_import_preview_ready"]
        )
        self.assertFalse(
            preview["decision"][
                "label_factory_gate_can_run_after_preview_review"
            ]
        )
        self.assertFalse(preview["decision"]["new_countable_labels_authorized"])
        self.assertEqual(preview["accepted_import_preview_rows"], [])
        self.assertTrue(preview["guardrails"]["review_only"])
        self.assertFalse(
            preview["guardrails"]["import_preview_artifact_written"]
        )
        self.assertFalse(preview["guardrails"]["imports_or_promotions_performed"])
        self.assertFalse(
            preview["guardrails"]["labels_registries_ontologies_changed"]
        )

    def test_fold_augmented_family_panel_label_factory_gate_readiness_current_counts(
        self,
    ) -> None:
        readiness = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_family_panel_label_factory_gate_readiness_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            readiness["status"],
            "family_panel_label_factory_gate_readiness_blocked",
        )
        self.assertEqual(readiness["counts"]["accepted_import_preview_rows"], 0)
        self.assertEqual(
            readiness["counts"]["label_factory_gate_input_rows"], 0
        )
        self.assertEqual(readiness["counts"]["panels_represented"], 0)
        self.assertEqual(
            readiness["counts"]["countable_label_candidate_count"], 0
        )
        self.assertIn(
            "accepted_import_preview_not_ready", readiness["blockers"]
        )
        self.assertIn(
            "label_factory_gate_input_rows_missing", readiness["blockers"]
        )
        self.assertFalse(
            readiness["decision"]["accepted_import_preview_ready"]
        )
        self.assertFalse(
            readiness["decision"]["label_factory_gate_inputs_ready"]
        )
        self.assertFalse(readiness["decision"]["label_factory_gate_run"])
        self.assertFalse(readiness["decision"]["new_countable_labels_authorized"])
        self.assertEqual(readiness["label_factory_gate_input_rows"], [])
        self.assertTrue(readiness["guardrails"]["review_only"])
        self.assertFalse(readiness["guardrails"]["label_factory_gate_run"])
        self.assertFalse(
            readiness["guardrails"]["imports_or_promotions_performed"]
        )
        self.assertFalse(
            readiness["guardrails"]["labels_registries_ontologies_changed"]
        )

    def test_active_lever_reviewer_decision_queue_current_counts(self) -> None:
        queue = _load_json(
            ROOT
            / "artifacts"
            / "v3_active_lever_reviewer_decision_queue_current702_20260603.json"
        )

        self.assertEqual(
            queue["status"],
            "active_lever_reviewer_decision_queue_ready_review_only",
        )
        self.assertEqual(queue["counts"]["decision_items"], 131)
        self.assertEqual(queue["counts"]["pending_decision_items"], 23)
        self.assertEqual(queue["counts"]["reviewed_decision_items"], 108)
        self.assertEqual(
            queue["counts"]["lever_counts"],
            {"Lever 2": 108, "Lever 3": 1, "Lever 4": 22},
        )
        self.assertEqual(
            queue["counts"]["decision_class_counts"],
            {
                "family_panel_expert_import_decision": 22,
                "p10746_fold_only_deployment_caveat": 1,
                "source_free_event_axis_linker_signoff": 53,
                "source_free_locator_rewrite_approval": 55,
            },
        )
        self.assertEqual(queue["counts"]["p10746_policy_decision_items"], 1)
        self.assertEqual(queue["counts"]["lever2_locator_rewrite_items"], 55)
        self.assertEqual(queue["counts"]["lever2_pending_locator_rewrite_items"], 0)
        self.assertEqual(queue["counts"]["lever2_reviewed_locator_rewrite_items"], 55)
        self.assertEqual(
            queue["counts"]["lever2_clean_locator_rewrite_items"], 49
        )
        self.assertEqual(queue["counts"]["lever2_event_axis_signoff_items"], 53)
        self.assertEqual(
            queue["counts"]["lever2_pending_event_axis_signoff_items"], 0
        )
        self.assertEqual(
            queue["counts"]["lever2_event_axis_priority1_signoff_items"], 3
        )
        self.assertEqual(
            queue["counts"]["lever2_event_axis_priority2_signoff_items"], 11
        )
        self.assertEqual(queue["counts"]["lever4_expert_import_items"], 22)
        self.assertEqual(
            queue["counts"]["lever4_accepted_import_preview_rows"], 0
        )
        self.assertEqual(
            queue["counts"]["lever4_label_factory_gate_input_rows"], 0
        )
        self.assertEqual(
            queue["counts"][
                "lever4_import_preview_candidate_if_accepted_items"
            ],
            6,
        )
        self.assertEqual(
            queue["counts"]["automation_action_allowed_now_items"], 0
        )
        self.assertEqual(queue["blockers"], [])
        self.assertTrue(queue["decision"]["queue_ready_for_review"])
        self.assertFalse(queue["decision"]["apply_decisions_now"])
        self.assertFalse(
            queue["decision"]["lever4_label_factory_gate_inputs_ready"]
        )
        self.assertEqual(
            queue["decision_queue"][0]["decision_class"],
            "p10746_fold_only_deployment_caveat",
        )
        self.assertEqual(queue["decision_queue"][0]["entry_id"], "m_csa:204")
        self.assertEqual(
            queue["decision_queue"][0]["decision_field_to_update"], "decision"
        )
        self.assertEqual(
            queue["decision_queue"][0]["review_status_field_to_update"],
            "review_status",
        )
        self.assertEqual(
            queue["decision_queue"][0]["required_review_status_after_decision"],
            "reviewed_explicit_decision",
        )
        priority2_rows = [
            row
            for row in queue["decision_queue"]
            if row["priority"] == 2
        ]
        self.assertEqual(len(priority2_rows), 6)
        self.assertEqual(priority2_rows[0]["decision_field_to_update"], "decision")
        priority3_rows = [
            row
            for row in queue["decision_queue"]
            if row["priority"] == 3
        ]
        self.assertEqual(len(priority3_rows), 52)
        self.assertEqual(
            priority3_rows[0]["decision_field_to_update"], "reviewer_decision"
        )
        self.assertEqual(
            priority3_rows[0]["approved_boolean_field_to_update"], "approved"
        )
        self.assertTrue(
            any(
                row["decision_class"] == "source_free_event_axis_linker_signoff"
                for row in priority3_rows
            )
        )
        self.assertTrue(queue["guardrails"]["review_only"])
        self.assertFalse(queue["guardrails"]["imports_or_promotions_performed"])
        self.assertFalse(
            queue["guardrails"]["labels_registries_ontologies_changed"]
        )

    def test_active_lever_mechanical_actionability_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_active_lever_mechanical_actionability_audit_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "active_lever_mechanical_actionability_blocked_external_decisions",
        )
        self.assertEqual(audit["counts"]["decision_items"], 131)
        self.assertEqual(
            audit["counts"]["external_decision_required_items"], 23
        )
        self.assertEqual(
            audit["counts"]["automation_action_allowed_now_items"], 0
        )
        self.assertEqual(audit["counts"]["mechanical_gates_ready_now"], 1)
        self.assertEqual(audit["counts"]["blockers"], 10)
        self.assertEqual(
            audit["counts"]["source_decision_intake_pending_rows"], 23
        )
        self.assertEqual(
            audit["counts"]["source_decision_intake_invalid_rows"], 0
        )
        self.assertEqual(
            audit["counts"]["source_decision_follow_on_gate_ready_rows"], 0
        )
        self.assertEqual(audit["counts"]["p10746_pending_policy_decisions"], 1)
        self.assertEqual(
            audit["counts"]["lever3_confounded_structural_proxy_rows"], 55
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_structural_proxy_abstained"], 10
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_retained_gap_rows"], 48
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_threshold_stress_blockers"], 2
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_evidence_request_rows"], 48
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_high_cofactor_min_new_abstained_rows_for_80pct"],
            16,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_structural_min_new_abstained_rows_for_80pct"],
            170,
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_evidence_extension_blockers"],
            6,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_acquisition_family_panel_eligible_rows"],
            0,
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_acquisition_high_shortfall"],
            16,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_acquisition_structural_shortfall"],
            170,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_acquisition_heldout_guardrail_rows"],
            4,
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_acquisition_blockers"],
            6,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_candidate_pool_unscored_rows"],
            170,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_candidate_pool_high_axis_rows"],
            0,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_candidate_pool_structural_axis_rows"],
            0,
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_scoring_tranche_rows"], 0
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_scoring_tranche_high_rows"],
            0,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_scoring_tranche_structural_rows"],
            0,
        )
        self.assertFalse(
            audit[
                "counts"
            ]["lever3_confounded_proxy_scoring_tranche_ready_for_plan"]
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_scoring_tranche_blockers"],
            3,
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_background_only_rows"], 170
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_background_axis_blockers"], 4
        )
        self.assertTrue(
            audit["counts"]["lever3_confounded_proxy_background_axis_exhausted"]
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_background_axis_scout_axes"],
            3,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_background_axis_scout_ready_axes"],
            0,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_unsupported_geometry_repair_rows"],
            8,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_unsupported_geometry_coordinate_files_observed"],
            8,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_unsupported_geometry_coordinate_files_missing"],
            0,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_unsupported_geometry_locus_files_scanned"],
            8,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_unsupported_geometry_locus_evidence_files"],
            0,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_unsupported_geometry_locus_protein_only_files"],
            8,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_unsupported_geometry_locus_ready_to_score_rows"],
            0,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_unsupported_geometry_locus_blockers"],
            2,
        )
        self.assertTrue(
            audit["counts"]["lever3_confounded_proxy_new_axis_registered"]
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_new_axis_contracted_rows"],
            6,
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_new_axis_contract_blockers"],
            0,
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_new_axis_full_channel_rows"],
            6,
        )
        self.assertEqual(
            audit["counts"]["lever3_confounded_proxy_new_axis_missing_full_score_rows"],
            0,
        )
        self.assertEqual(
            audit[
                "counts"
            ]["lever3_confounded_proxy_new_axis_scored_extension_blockers"],
            0,
        )
        self.assertEqual(
            audit["counts"]["lever4_pending_expert_import_decisions"], 22
        )
        self.assertEqual(audit["counts"]["lever4_acceptance_scenario_rows"], 6)
        self.assertEqual(audit["counts"]["lever4_acceptance_scenario_panels"], 5)
        self.assertEqual(
            audit[
                "counts"
            ]["lever4_label_factory_candidates_if_all_scenario_rows_accepted"],
            6,
        )
        self.assertEqual(
            audit["counts"]["lever2_pending_locator_approvals"], 0
        )
        self.assertEqual(
            audit["counts"]["lever2_pending_event_axis_signoffs"], 0
        )
        self.assertEqual(
            audit["counts"]["lever2_locator_sidecars_written"], 53
        )
        self.assertEqual(
            audit["counts"]["lever2_event_axis_materialized_linker_rows"], 14
        )
        self.assertEqual(
            audit["counts"]["lever2_event_axis_signoff_draft_rows"], 53
        )
        self.assertEqual(
            audit["counts"]["lever2_event_axis_signoff_rows_with_both_roles"], 14
        )
        self.assertEqual(
            audit["counts"]["lever2_event_axis_pending_reviewer_signoff_rows"], 0
        )
        self.assertEqual(
            audit["counts"]["lever2_event_axis_explicit_approved_rows"], 14
        )
        self.assertEqual(
            audit["counts"]["lever2_event_axis_gate_consumable_signoff_rows"], 14
        )
        self.assertEqual(
            audit["counts"]["lever2_event_axis_priority1_signoff_rows"], 3
        )
        self.assertEqual(
            audit["counts"]["lever2_event_axis_priority2_signoff_rows"], 11
        )
        self.assertEqual(
            audit["counts"]["lever2_event_axis_insufficient_signoff_rows"], 33
        )
        self.assertTrue(
            audit["counts"]["lever2_partial_surface_policy_ready"]
        )
        self.assertTrue(
            audit["counts"]["lever2_partial_surface_policy_threshold_read_accepted"]
        )
        self.assertEqual(
            audit["counts"]["lever2_partial_surface_policy_pair_feature_rows"], 53
        )
        self.assertEqual(
            audit["counts"][
                "lever2_partial_surface_policy_missing_locator_abstain_rows"
            ],
            87,
        )
        self.assertFalse(
            audit["counts"][
                "lever2_partial_surface_operating_contract_decision_required"
            ]
        )
        self.assertEqual(
            audit["counts"]["lever2_partial_surface_operating_contract_blockers"],
            0,
        )
        self.assertTrue(
            audit["counts"]["lever2_heldout_threshold_read_once_performed"]
        )
        self.assertEqual(
            audit["counts"]["lever2_heldout_threshold_overall_oos_abstain_recall"],
            1.0,
        )
        self.assertEqual(
            audit["counts"][
                "lever2_heldout_threshold_overall_primary_retain_recall"
            ],
            0.0,
        )
        self.assertEqual(
            audit["counts"]["lever2_post_readout_recovery_queue_rows"], 119
        )
        self.assertEqual(
            audit["counts"][
                "lever2_post_readout_feature_complete_primary_abstentions"
            ],
            32,
        )
        self.assertEqual(
            audit["counts"][
                "lever2_post_readout_primary_missing_locator_abstentions"
            ],
            16,
        )
        self.assertEqual(
            audit["counts"][
                "lever2_post_readout_oos_missing_locator_abstentions"
            ],
            71,
        )
        self.assertFalse(
            audit["counts"][
                "lever2_post_readout_coverage_repair_alone_sufficient"
            ]
        )
        self.assertIn(
            "post-readout recovery queue blocks deployment",
            audit["decision"]["next_gate"],
        )
        self.assertEqual(
            audit["counts"]["lever4_label_factory_gate_input_rows"], 0
        )
        self.assertNotIn("no_active_lever_mechanical_gate_ready", audit["blockers"])
        self.assertIn(
            "lever3_confounded_structural_proxy_calibration_gap",
            audit["blockers"],
        )
        self.assertIn(
            "lever3_confounded_proxy_threshold_stress_retention_cost",
            audit["blockers"],
        )
        self.assertIn(
            "lever3_confounded_proxy_evidence_extension_scale_gap",
            audit["blockers"],
        )
        self.assertIn(
            "lever3_confounded_proxy_acquisition_shortfall", audit["blockers"]
        )
        self.assertIn(
            "lever3_confounded_proxy_train_cal_scoring_tranche_not_run",
            audit["blockers"],
        )
        self.assertIn(
            "lever3_confounded_proxy_background_axis_exhausted",
            audit["blockers"],
        )
        self.assertIn(
            "lever3_confounded_proxy_unsupported_geometry_locus_scan_no_axis",
            audit["blockers"],
        )
        self.assertNotIn(
            "lever3_confounded_proxy_new_axis_contract_missing",
            audit["blockers"],
        )
        self.assertNotIn(
            "lever3_confounded_proxy_new_axis_contract_tranche_not_scored",
            audit["blockers"],
        )
        self.assertNotIn(
            "lever3_confounded_proxy_new_axis_contract_tranche_partial_scores",
            audit["blockers"],
        )
        gates = {row["gate"]: row for row in audit["gate_checks"]}
        self.assertEqual(
            gates["confounded_proxy_train_cal_background_axis_scout"][
                "blocking_reason"
            ],
            "current_scout_axis_scored_no_ready_followup_axis",
        )
        self.assertEqual(
            gates["confounded_proxy_train_cal_unsupported_geometry_locus_scan"][
                "blocking_reason"
            ],
            "unsupported_geometry_afdb_coordinates_protein_only_no_locus_evidence",
        )
        self.assertFalse(
            gates["confounded_proxy_train_cal_unsupported_geometry_locus_scan"][
                "ready_now"
            ]
        )
        self.assertEqual(
            gates["confounded_proxy_train_cal_new_proxy_axis_contract"][
                "blocking_reason"
            ],
            "contracted_proxy_axis_fully_scored_surface_still_blocked",
        )
        self.assertNotIn(
            "source_decision_intake_preflight_not_ready", audit["blockers"]
        )
        self.assertIn("p10746_policy_decision_missing", audit["blockers"])
        self.assertIn(
            "family_panel_expert_import_decisions_missing", audit["blockers"]
        )
        self.assertNotIn(
            "lever2_partial_surface_operating_contract_decision_required",
            audit["blockers"],
        )
        self.assertNotIn(
            "source_free_locator_rewrite_approvals_missing", audit["blockers"]
        )
        self.assertIn(
            "Lever 2 locator approvals and event-axis signoffs are cleared",
            audit["interpretation"]["result"],
        )
        self.assertIn("event-axis signoffs are cleared", audit["interpretation"]["result"])
        self.assertNotIn(
            "Lever 2 is blocked by locator approvals plus",
            audit["interpretation"]["result"],
        )
        self.assertNotIn(
            "source_free_event_axis_linker_gate_blocked", audit["blockers"]
        )
        self.assertNotIn(
            "source_free_event_axis_linkers_missing", audit["blockers"]
        )
        self.assertFalse(audit["decision"]["apply_any_decision_gate_now"])
        self.assertFalse(audit["decision"]["copy_locator_sidecars_now"])
        self.assertFalse(
            audit["decision"]["apply_frozen_residual_threshold_now"]
        )
        self.assertFalse(audit["decision"]["run_label_factory_gate_now"])
        self.assertTrue(audit["guardrails"]["review_only"])
        self.assertFalse(
            audit["guardrails"]["labels_registries_ontologies_changed"]
        )
        self.assertEqual(
            audit["gate_checks"][0]["gate"], "source_decision_intake_preflight"
        )
        self.assertFalse(audit["gate_checks"][0]["ready_now"])
        self.assertEqual(
            audit["gate_checks"][0]["blocking_reason"],
            "source_decision_follow_on_rows_already_consumed",
        )
        self.assertEqual(
            audit["next_review_items"][0]["decision_field_to_update"],
            "decision",
        )
        next_review_classes = {
            item["decision_class"] for item in audit["next_review_items"]
        }
        self.assertIn(
            "family_panel_expert_import_decision", next_review_classes
        )
        self.assertNotIn(
            "source_free_partial_surface_operating_contract", next_review_classes
        )
        self.assertNotIn(
            "source_free_locator_rewrite_approval", next_review_classes
        )
        self.assertFalse(
            any(
                item["entry_id"] == "current702_partial_surface"
                for item in audit["next_review_items"]
            )
        )
        self.assertNotIn(
            "remaining Lever 2 event-axis signoffs",
            audit["interpretation"]["next_action"],
        )
        self.assertNotIn(
            "Lever 2 partial-surface operating-contract decision",
            audit["interpretation"]["next_action"],
        )
        self.assertEqual(
            gates["source_free_partial_surface_operating_contract"][
                "blocking_reason"
            ],
            "partial_surface_operating_contract_accepted",
        )
        self.assertFalse(
            gates["source_free_partial_surface_operating_contract"]["ready_now"]
        )
        self.assertEqual(
            gates["source_free_locator_materialization_and_pre_threshold_readiness"][
                "blocking_reason"
            ],
            "source_free_heldout_threshold_readout_applied_once",
        )
        self.assertEqual(
            audit["next_review_items"][7]["entry_id"], "m_csa:116"
        )
        self.assertEqual(
            audit["next_review_items"][7]["decision_field_to_update"],
            "decision",
        )

    def test_active_lever_priority_decision_templates_current_counts(
        self,
    ) -> None:
        templates = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_active_lever_priority_decision_templates_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            templates["status"],
            "active_lever_priority_decision_templates_ready_review_only",
        )
        self.assertEqual(templates["counts"]["template_rows"], 78)
        self.assertEqual(
            templates["counts"]["p10746_policy_decision_templates"], 1
        )
        self.assertEqual(
            templates["counts"][
                "family_panel_import_preview_candidate_templates"
            ],
            6,
        )
        self.assertEqual(
            templates["counts"]["other_family_panel_expert_decision_templates"],
            16,
        )
        self.assertEqual(
            templates["counts"]["clean_locator_rewrite_approval_templates"], 49
        )
        self.assertEqual(
            templates["counts"]["warning_locator_rewrite_approval_templates"], 6
        )
        self.assertEqual(
            templates["counts"]["source_locations_matched_by_hash"], 78
        )
        self.assertEqual(templates["counts"]["source_locations_unresolved"], 0)
        source_location_statuses = {
            row["source_location_status"]
            for rows in templates["template_groups"].values()
            for row in rows
        }
        self.assertEqual(
            source_location_statuses, {"matched_by_entry_id_and_hash"}
        )
        self.assertEqual(
            templates["template_groups"]["p10746_policy_decisions"][0][
                "source_json_pointer"
            ],
            "/decision_stubs/0",
        )
        self.assertEqual(
            templates["template_groups"]["p10746_policy_decisions"][0][
                "review_status_field_to_update"
            ],
            "review_status",
        )
        self.assertEqual(
            templates["template_groups"]["p10746_policy_decisions"][0][
                "required_review_status_after_decision"
            ],
            "reviewed_explicit_decision",
        )
        self.assertEqual(
            templates["template_groups"]["family_panel_import_preview_candidates"][
                0
            ]["source_json_pointer"],
            "/expert_import_decision_stubs/12",
        )
        self.assertEqual(
            templates["template_groups"]["clean_locator_rewrite_approvals"][0][
                "decision_field_to_update"
            ],
            "reviewer_decision",
        )
        self.assertEqual(
            templates["template_groups"]["clean_locator_rewrite_approvals"][0][
                "source_json_pointer"
            ],
            "/locator_rewrite_decision_stubs/0",
        )
        self.assertTrue(templates["decision"]["templates_ready_for_review"])
        self.assertFalse(templates["decision"]["apply_templates_now"])
        self.assertFalse(templates["guardrails"]["decisions_applied"])
        self.assertFalse(
            templates["guardrails"]["labels_registries_ontologies_changed"]
        )

    def test_active_lever_source_decision_intake_preflight_current_counts(
        self,
    ) -> None:
        preflight = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_active_lever_source_decision_intake_preflight_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            preflight["status"],
            "active_lever_source_decision_intake_preflight_ready",
        )
        self.assertEqual(preflight["counts"]["template_rows"], 78)
        self.assertEqual(
            preflight["counts"]["decision_class_counts"],
            {
                "family_panel_expert_import_decision": 22,
                "p10746_fold_only_deployment_caveat": 1,
                "source_free_locator_rewrite_approval": 55,
            },
        )
        self.assertEqual(
            preflight["counts"]["intake_status_counts"],
            {
                "pending_external_decision": 23,
                "ready_for_locator_materialization_gate": 53,
                "reviewed_locator_rejection_no_materialization": 2,
            },
        )
        self.assertEqual(preflight["counts"]["explicit_decision_rows"], 55)
        self.assertEqual(preflight["counts"]["pending_decision_rows"], 23)
        self.assertEqual(preflight["counts"]["invalid_decision_rows"], 0)
        self.assertEqual(
            preflight["counts"]["source_edit_contract_violation_rows"], 0
        )
        self.assertEqual(preflight["counts"]["follow_on_gate_ready_rows"], 53)
        self.assertEqual(
            preflight["counts"]["p10746_application_ready_rows"], 0
        )
        self.assertEqual(
            preflight["counts"]["family_panel_application_ready_rows"], 0
        )
        self.assertEqual(
            preflight["counts"][
                "family_panel_import_preview_candidate_accept_rows"
            ],
            0,
        )
        self.assertEqual(
            preflight["counts"]["locator_materialization_ready_approval_rows"],
            53,
        )
        self.assertEqual(preflight["counts"]["locator_rejection_rows"], 2)
        self.assertIn(
            "explicit_source_decisions_missing", preflight["blockers"]
        )
        self.assertNotIn(
            "no_hash_valid_decision_rows_ready_for_gate",
            preflight["blockers"],
        )
        self.assertTrue(preflight["decision"]["run_any_matching_gate_now"])
        self.assertTrue(preflight["decision"]["locator_materialization_gate_ready"])
        self.assertFalse(preflight["decision"]["copy_locator_sidecars_now"])
        self.assertFalse(preflight["decision"]["run_label_factory_gate_now"])
        self.assertFalse(
            preflight["decision"]["apply_frozen_residual_threshold_now"]
        )
        self.assertEqual(preflight["intake_rows"][0]["entry_id"], "m_csa:204")
        self.assertEqual(
            preflight["intake_rows"][0]["decision_class"],
            "p10746_fold_only_deployment_caveat",
        )
        self.assertEqual(
            preflight["intake_rows"][0]["source_json_pointer"],
            "/decision_stubs/0",
        )
        self.assertEqual(
            preflight["intake_rows"][0]["decision_field_to_update"],
            "decision",
        )
        self.assertEqual(
            preflight["intake_rows"][0]["review_status_field_to_update"],
            "review_status",
        )
        self.assertEqual(
            preflight["intake_rows"][0]["review_status"],
            "pending_explicit_decision",
        )
        self.assertEqual(
            [row["entry_id"] for row in preflight["intake_rows"][1:7]],
            [
                "m_csa:10",
                "m_csa:30",
                "m_csa:31",
                "m_csa:191",
                "m_csa:448",
                "m_csa:973",
            ],
        )
        locator_rows = [
            row
            for row in preflight["intake_rows"]
            if row["decision_class"] == "source_free_locator_rewrite_approval"
        ]
        self.assertEqual(
            locator_rows[0]["decision_field_to_update"], "reviewer_decision"
        )
        self.assertEqual(
            locator_rows[0]["approved_boolean_field_to_update"], "approved"
        )
        self.assertTrue(locator_rows[0]["approved"])
        self.assertEqual(
            locator_rows[0]["intake_status"],
            "ready_for_locator_materialization_gate",
        )
        self.assertTrue(preflight["guardrails"]["review_only"])
        self.assertFalse(preflight["guardrails"]["decisions_applied"])
        self.assertFalse(
            preflight["guardrails"]["labels_registries_ontologies_changed"]
        )

    def test_active_lever_decision_application_contract_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_active_lever_decision_application_contract_audit_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "active_lever_decision_application_contract_audit_passed_pending_source_decisions",
        )
        self.assertEqual(audit["counts"]["contract_violations"], 0)
        self.assertEqual(audit["counts"]["source_intake_template_rows"], 78)
        self.assertEqual(audit["counts"]["source_intake_pending_rows"], 78)
        self.assertEqual(audit["counts"]["source_intake_follow_on_ready_rows"], 0)
        self.assertEqual(audit["counts"]["p10746_reviewed_decision_rows"], 0)
        self.assertEqual(audit["counts"]["family_reviewed_decision_records"], 0)
        self.assertEqual(audit["counts"]["locator_approved_decision_records"], 0)
        self.assertEqual(audit["counts"]["locator_invalid_approval_records"], 0)
        self.assertFalse(audit["decision"]["run_any_matching_gate_now"])
        self.assertTrue(audit["decision"]["application_contracts_aligned"])
        self.assertFalse(audit["guardrails"]["decisions_applied"])

    def test_fold_augmented_family_panel_source_check_queue_current_counts(self) -> None:
        queue = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_family_panel_source_check_queue_current702_20260601.json"
        )

        self.assertEqual(queue["status"], "source_check_queue_ready_review_only")
        self.assertEqual(queue["counts"]["source_check_rows"], 11)
        self.assertEqual(queue["counts"]["panels_represented"], 5)
        self.assertEqual(
            queue["counts"]["source_check_rows_by_panel"],
            {
                "cobalamin_and_radical_rearrangement_panel": 2,
                "flavin_monooxygenase_and_flavin_oxygen_transfer": 3,
                "lipoamide_or_sulfur_transfer_redox_boundary": 1,
                "near_orphan_glycoside_or_nucleoside_hydrolase_controls": 2,
                "no_reliable_structure_metal_hydrolase_controls": 3,
            },
        )
        self.assertEqual(
            [row["entry_id"] for row in queue["queue_rows"]],
            [
                "mh_068",
                "mh_067",
                "mh_066",
                "m_csa:267",
                "m_csa:131",
                "m_csa:750",
                "m_csa:551",
                "m_csa:132",
                "mh_073",
                "secondary_probe::radical_sam_enzyme",
                "m_csa:116",
            ],
        )
        self.assertTrue(queue["guardrails"]["review_only"])
        self.assertFalse(queue["guardrails"]["new_source_data_fetched"])

    def test_fold_augmented_family_panel_source_check_completion_reconciliation_current_counts(
        self,
    ) -> None:
        reconciliation = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_fold_augmented_family_panel_source_check_completion_"
                "reconciliation_current702_20260602.json"
            )
        )

        self.assertEqual(
            reconciliation["status"],
            "family_panel_source_check_completion_reconciliation_ready_complete",
        )
        self.assertEqual(reconciliation["counts"]["source_check_queue_rows"], 11)
        self.assertEqual(
            reconciliation["counts"]["source_check_artifact_paths_supplied"],
            11,
        )
        self.assertEqual(
            reconciliation["counts"]["source_check_artifacts_found"], 11
        )
        self.assertEqual(
            reconciliation["counts"][
                "completed_review_only_no_label_change_rows"
            ],
            11,
        )
        self.assertEqual(reconciliation["counts"]["pending_source_check_rows"], 0)
        self.assertEqual(
            reconciliation["counts"]["family_promotion_ready_rows"], 0
        )
        self.assertEqual(
            reconciliation["counts"]["countable_label_candidate_count"], 0
        )
        self.assertEqual(
            reconciliation["decision"]["pending_source_check_entry_ids"],
            [],
        )
        self.assertEqual(
            reconciliation["decision"]["completed_source_check_entry_ids"],
            [
                "mh_068",
                "mh_067",
                "mh_066",
                "m_csa:267",
                "m_csa:131",
                "m_csa:750",
                "m_csa:551",
                "m_csa:132",
                "mh_073",
                "secondary_probe::radical_sam_enzyme",
                "m_csa:116",
            ],
        )
        self.assertTrue(
            reconciliation["decision"]["source_check_queue_fully_reconciled"]
        )
        self.assertFalse(reconciliation["decision"]["new_countable_labels_authorized"])
        by_entry = {
            row["entry_id"]: row
            for row in reconciliation["reconciliation_rows"]
        }
        self.assertEqual(
            by_entry["mh_066"]["completion_status"],
            "completed_review_only_no_label_change",
        )
        self.assertEqual(
            by_entry["mh_067"]["completion_status"],
            "completed_review_only_no_label_change",
        )
        self.assertEqual(
            by_entry["mh_068"]["completion_status"],
            "completed_review_only_no_label_change",
        )
        self.assertEqual(
            by_entry["mh_066"]["source_check_result"],
            "hold_as_review_only_metal_hydrolase_expansion_candidate",
        )
        self.assertEqual(
            by_entry["m_csa:267"]["source_check_result"],
            "keep_as_review_only_oos_boundary_control",
        )
        self.assertFalse(
            any(
                row["countable_label_candidate"]
                for row in reconciliation["reconciliation_rows"]
            )
        )
        self.assertTrue(reconciliation["guardrails"]["review_only"])
        self.assertFalse(
            reconciliation["guardrails"]["labels_registries_ontologies_changed"]
        )

    def test_family_panel_source_free_predicted_geometry_mh067_mh068_source_checks(
        self,
    ) -> None:
        checks = {
            "mh_067": (
                "v3_family_panel_source_free_predicted_geometry_source_check_"
                "mh_067_current702_20260602.json",
                "hold_as_review_only_carbonic_anhydrase_boundary_same_accession_anchor",
            ),
            "mh_068": (
                "v3_family_panel_source_free_predicted_geometry_source_check_"
                "mh_068_current702_20260602.json",
                "hold_as_review_only_sulfatase_fgly_boundary_same_accession_anchor",
            ),
        }
        for entry_id, (filename, result) in checks.items():
            check = _load_json(ROOT / "artifacts" / filename)
            self.assertEqual(
                check["status"],
                "source_check_completed_review_only_no_label_change",
            )
            self.assertEqual(check["row"]["entry_id"], entry_id)
            self.assertEqual(
                check["source_check_decision"]["source_check_result"],
                result,
            )
            self.assertFalse(
                check["source_check_decision"]["family_promotion_ready"]
            )
            self.assertFalse(check["source_check_decision"]["label_import_ready"])
            self.assertTrue(
                check["duplicate_and_leakage_screen"][
                    "source_accession_in_current702_manifest"
                ]
            )
            self.assertTrue(
                check["local_source_evidence"]["mechanism_locus_assessment"][
                    "same_accession_current702_anchor_present"
                ]
            )
            self.assertTrue(check["guardrails"]["review_only"])
            self.assertFalse(check["guardrails"]["new_source_data_fetched"])

    def test_family_panel_m_csa_primary_channel_repair_current_scores(self) -> None:
        repair = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_family_panel_m_csa_primary_channel_repair_current702_20260601.json"
        )

        self.assertEqual(
            repair["status"],
            "m_csa_primary_channel_repair_scored_review_only",
        )
        self.assertEqual(repair["counts"]["primary_channel_score_complete_rows"], 2)
        self.assertEqual(
            repair["counts"]["repair_policy_counts"],
            {
                "best_real_sequence_accession_by_active_site_coverage": 1,
                "manifest_accession_compatible_residue_subset": 1,
            },
        )
        by_entry = {row["entry_id"]: row for row in repair["row_scores"]}
        self.assertEqual(by_entry["m_csa:132"]["predicted_geometry_accession"], "P07740")
        self.assertEqual(by_entry["m_csa:132"]["nearest_atlas_tm_score"], 0.6879)
        self.assertEqual(by_entry["m_csa:116"]["predicted_geometry_accession"], "Q2RSB2")
        self.assertEqual(by_entry["m_csa:116"]["nearest_atlas_tm_score"], 0.5417)
        self.assertFalse(repair["blockers"])
        self.assertTrue(repair["guardrails"]["review_only"])

    def test_fold_augmented_family_panel_m_csa267_source_check_current_result(self) -> None:
        check = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_family_panel_source_check_m_csa267_current702_20260601.json"
        )

        self.assertEqual(
            check["status"],
            "source_check_completed_review_only_no_label_change",
        )
        self.assertEqual(check["row"]["entry_id"], "m_csa:267")
        self.assertEqual(check["row"]["label_type"], "out_of_scope")
        self.assertIsNone(check["row"]["fingerprint_id"])
        self.assertEqual(
            check["source_check_decision"]["source_check_result"],
            "keep_as_review_only_oos_boundary_control",
        )
        self.assertFalse(check["source_check_decision"]["family_promotion_ready"])
        self.assertEqual(check["local_source_evidence"]["catalytic_residue_count"], 6)
        self.assertTrue(check["guardrails"]["review_only"])
        self.assertFalse(check["guardrails"]["new_source_data_fetched"])

    def test_fold_augmented_family_panel_m_csa131_source_check_current_result(self) -> None:
        check = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_family_panel_source_check_m_csa131_current702_20260601.json"
        )

        self.assertEqual(
            check["status"],
            "source_check_completed_review_only_no_label_change",
        )
        self.assertEqual(check["row"]["entry_id"], "m_csa:131")
        self.assertEqual(check["row"]["benchmark_role"], "secondary_ood_probe::flavin_monooxygenase")
        self.assertEqual(check["row"]["label_type"], "seed_fingerprint")
        self.assertEqual(check["row"]["fingerprint_id"], "flavin_monooxygenase")
        self.assertEqual(
            check["source_check_decision"]["source_check_result"],
            "confirm_secondary_fmo_probe_support_no_primary_promotion",
        )
        self.assertFalse(check["source_check_decision"]["family_promotion_ready"])
        self.assertEqual(check["local_source_evidence"]["catalytic_residue_count"], 5)
        self.assertTrue(check["guardrails"]["review_only"])
        self.assertFalse(check["guardrails"]["new_source_data_fetched"])

    def test_fold_augmented_family_panel_repaired_m_csa_source_checks_current_results(
        self,
    ) -> None:
        check_132 = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_family_panel_source_check_m_csa132_current702_20260601.json"
        )
        check_116 = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_family_panel_source_check_m_csa116_current702_20260601.json"
        )

        self.assertEqual(
            check_132["status"],
            "source_check_completed_review_only_no_label_change",
        )
        self.assertEqual(
            check_132["source_check_decision"]["source_check_result"],
            "confirm_secondary_fmo_support_after_geometry_repair_no_primary_promotion",
        )
        self.assertFalse(check_132["source_check_decision"]["family_promotion_ready"])
        self.assertEqual(
            check_132["repair_evidence"]["predicted_geometry_accession_repair"]["policy"],
            "best_real_sequence_accession_by_active_site_coverage",
        )
        self.assertEqual(
            check_116["source_check_decision"]["source_check_result"],
            "keep_as_review_only_oos_transhydrogenase_control",
        )
        self.assertFalse(check_116["source_check_decision"]["family_promotion_ready"])
        self.assertEqual(
            check_116["repair_evidence"]["predicted_geometry_accession_repair"]["policy"],
            "manifest_accession_compatible_residue_subset",
        )
        self.assertTrue(check_132["guardrails"]["review_only"])
        self.assertTrue(check_116["guardrails"]["review_only"])

    def test_fold_augmented_family_panel_m_csa750_source_check_current_result(self) -> None:
        check = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_family_panel_source_check_m_csa750_current702_20260601.json"
        )

        self.assertEqual(
            check["status"],
            "source_check_completed_review_only_no_label_change",
        )
        self.assertEqual(check["row"]["entry_id"], "m_csa:750")
        self.assertEqual(check["row"]["current_label_type"], "out_of_scope")
        self.assertIsNone(check["row"]["current_fingerprint_id"])
        self.assertEqual(
            check["local_source_evidence"]["label_revision_decision"],
            "relabel_out_of_scope",
        )
        self.assertEqual(
            check["local_source_evidence"]["label_revision_mechanism_class"],
            "radical_flavin_fe_s_dehydratase",
        )
        self.assertEqual(
            check["source_check_decision"]["source_check_result"],
            "keep_as_oos_boundary_and_future_radical_flavin_fe_s_candidate",
        )
        self.assertFalse(check["source_check_decision"]["family_promotion_ready"])
        self.assertTrue(check["guardrails"]["review_only"])
        self.assertFalse(check["guardrails"]["new_source_data_fetched"])

    def test_fold_augmented_family_panel_m_csa551_source_check_current_result(self) -> None:
        check = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_family_panel_source_check_m_csa551_current702_20260601.json"
        )

        self.assertEqual(
            check["status"],
            "source_check_completed_review_only_no_label_change",
        )
        self.assertEqual(check["row"]["entry_id"], "m_csa:551")
        self.assertEqual(check["row"]["current_label_type"], "seed_fingerprint")
        self.assertEqual(
            check["row"]["current_fingerprint_id"],
            "flavin_dehydrogenase_reductase",
        )
        self.assertEqual(
            check["local_source_evidence"]["adjudication_mechanism_decision"],
            "mechanism_clean_fmo_support",
        )
        self.assertFalse(check["local_source_evidence"]["import_ready"])
        self.assertFalse(check["local_source_evidence"]["registry_edit_allowed"])
        self.assertEqual(
            check["source_check_decision"]["source_check_result"],
            "confirm_future_fmo_support_no_registry_change",
        )
        self.assertFalse(check["source_check_decision"]["family_promotion_ready"])
        self.assertTrue(check["guardrails"]["review_only"])
        self.assertFalse(check["guardrails"]["new_source_data_fetched"])

    def test_fold_augmented_family_panel_missing_primary_channel_queue_current_counts(self) -> None:
        queue = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_family_panel_missing_primary_channel_queue_current702_20260601.json"
        )

        self.assertEqual(
            queue["status"],
            "missing_primary_channel_queue_ready_review_only",
        )
        self.assertEqual(queue["counts"]["missing_primary_channel_rows"], 5)
        self.assertEqual(queue["counts"]["m_csa_rows"], 0)
        self.assertEqual(queue["counts"]["secondary_probe_rows"], 1)
        self.assertEqual(queue["counts"]["external_or_placeholder_rows"], 4)
        self.assertEqual(
            queue["counts"]["score_blocker_counts"],
            {
                "predicted_geometry_top1_score_missing": 5,
            },
        )
        self.assertNotIn("m_csa:973", {row["entry_id"] for row in queue["queue_rows"]})
        self.assertNotIn("m_csa:132", {row["entry_id"] for row in queue["queue_rows"]})
        self.assertNotIn("m_csa:116", {row["entry_id"] for row in queue["queue_rows"]})
        self.assertTrue(queue["guardrails"]["review_only"])
        self.assertFalse(queue["guardrails"]["new_source_data_fetched"])

    def test_fold_augmented_family_panel_missing_primary_channel_diagnosis_current_counts(
        self,
    ) -> None:
        diagnosis = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_family_panel_missing_primary_channel_diagnosis_current702_20260601.json"
        )

        self.assertEqual(
            diagnosis["status"],
            "missing_primary_channel_diagnosis_ready_review_only",
        )
        self.assertEqual(diagnosis["counts"]["diagnosed_rows"], 5)
        self.assertEqual(
            diagnosis["counts"]["diagnosis_counts"],
            {
                "source_backed_fold_scored_needs_predicted_geometry": 5,
            },
        )
        self.assertEqual(diagnosis["counts"]["rows_with_source_backed_fold_score"], 5)
        self.assertEqual(
            diagnosis["counts"]["rows_with_train_calibration_fold_score"],
            0,
        )
        by_entry = {row["entry_id"]: row for row in diagnosis["diagnosed_rows"]}
        self.assertNotIn("m_csa:973", by_entry)
        self.assertNotIn("m_csa:132", by_entry)
        self.assertNotIn("m_csa:116", by_entry)
        self.assertIn("m_csa:973 is no longer in the missing primary-channel queue", diagnosis["interpretation"]["m_csa_973_result"])
        self.assertFalse(diagnosis["guardrails"]["foldseek_or_tmsearch_recomputed"])

    def test_family_panel_source_backed_sidecar_materialization_plan_current_counts(
        self,
    ) -> None:
        plan = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_source_backed_sidecar_materialization_plan_current702_20260601.json"
        )

        self.assertEqual(
            plan["status"],
            "source_backed_sidecar_materialization_plan_ready_review_only",
        )
        self.assertEqual(plan["counts"]["planned_rows"], 10)
        self.assertEqual(plan["counts"]["source_backed_representatives_selected"], 10)
        self.assertEqual(plan["counts"]["secondary_probe_representatives"], 2)
        self.assertEqual(plan["counts"]["glycoside_representatives"], 1)
        self.assertEqual(plan["counts"]["prior_identifier_resolution_rows"], 7)
        self.assertEqual(plan["counts"]["labels_or_imports_changed"], 0)

        expected = {
            "secondary_probe::cobalamin_radical_rearrangement": (
                "uniprot:Q59490",
                "1L1L",
            ),
            "secondary_probe::radical_sam_enzyme": (
                "uniprot:A0A1M6T2I7",
                "8VPO",
            ),
            "external_glycoside_panel": ("uniprot:Q6NSJ0", "7QQF"),
            "mh_073": ("uniprot:P01112", "121P"),
            "mh_064": ("uniprot:C7C422", "3PG4"),
            "mh_065": ("uniprot:Q79MP6", "1DDK"),
            "mh_066": ("uniprot:P52699", "1DD6"),
            "mh_067": ("uniprot:P00918", "12CA"),
            "mh_068": ("uniprot:P15289", "1AUK"),
            "mh_072": ("uniprot:P0A6P9", "1E9I"),
        }
        by_entry = {row["entry_id"]: row for row in plan["row_plan"]}
        self.assertEqual(set(by_entry), set(expected))
        for entry_id, (accession, structure) in expected.items():
            self.assertEqual(
                by_entry[entry_id]["identifier_resolution"]["source_accession"],
                accession,
            )
            self.assertEqual(
                by_entry[entry_id]["coordinate_materialization_manifest"][
                    "preferred_coordinate_id"
                ],
                structure,
            )
            self.assertEqual(
                by_entry[entry_id]["coordinate_materialization_manifest"][
                    "materialization_status"
                ],
                "not_run_manifest_only",
            )

        self.assertIn(
            "no labels, registries, ontologies, imports, splits, thresholds",
            " ".join(plan["guardrails"]),
        )
        self.assertIn("foldseek easy-search", "\n".join(plan["commands_to_run_next"]))

    def test_family_panel_source_backed_sidecar_materialization_current_scores(
        self,
    ) -> None:
        materialization = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_source_backed_sidecar_materialization_current702_20260601.json"
        )

        self.assertEqual(
            materialization["status"],
            "source_backed_sidecars_fold_scored_review_only",
        )
        self.assertEqual(materialization["counts"]["targeted_rows"], 10)
        self.assertEqual(
            materialization["counts"]["foldseek_query_entries_with_hits"],
            10,
        )
        self.assertEqual(
            materialization["counts"]["remaining_predicted_fold_blockers"],
            0,
        )
        self.assertEqual(
            materialization["counts"]["remaining_predicted_geometry_blockers"],
            10,
        )
        self.assertFalse(materialization["blockers"])
        by_entry = {row["entry_id"]: row for row in materialization["row_scores"]}
        expected_tm = {
            "secondary_probe::cobalamin_radical_rearrangement": 0.4655,
            "secondary_probe::radical_sam_enzyme": 0.7039,
            "external_glycoside_panel": 0.6259,
            "mh_073": 0.8022,
            "mh_064": 0.9222,
            "mh_065": 0.9411,
            "mh_066": 0.9445,
            "mh_067": 1.004,
            "mh_068": 1.002,
            "mh_072": 0.5936,
        }
        self.assertEqual(set(by_entry), set(expected_tm))
        for entry_id, tm_score in expected_tm.items():
            row = by_entry[entry_id]
            self.assertEqual(
                row["predicted_structure_fold_channel"]["nearest_atlas_tm_score"],
                tm_score,
            )
            self.assertEqual(
                row["predicted_structure_fold_channel"]["score_source"],
                "family_panel_source_backed_afdb_vs_predicted_atlas",
            )
            self.assertEqual(
                row["remaining_primary_channel_blockers"],
                ["predicted_geometry_top1_score_missing"],
            )
            for record in row["coordinate_records"]:
                self.assertTrue(record["exists"])
                self.assertRegex(record["sha256"], r"^[0-9a-f]{64}$")
            sidecar = _load_json(ROOT / row["sidecar_path"])
            self.assertFalse(sidecar["predictive_use_allowed"])
            self.assertFalse(sidecar["ready_for_label_import"])

    def test_family_panel_source_free_predicted_geometry_sidecar_manifest_current_counts(
        self,
    ) -> None:
        manifest = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_source_free_predicted_geometry_sidecar_manifest_current702_20260601.json"
        )

        self.assertEqual(
            manifest["status"],
            "source_free_predicted_geometry_manifest_partially_ready_to_score_review_only",
        )
        self.assertEqual(manifest["counts"]["targeted_rows"], 10)
        self.assertEqual(manifest["counts"]["rows_with_afdb_predicted_cif"], 10)
        self.assertEqual(manifest["counts"]["rows_with_source_backed_fold_score"], 10)
        self.assertEqual(
            manifest["counts"]["rows_with_approved_source_free_active_site_locator"],
            5,
        )
        self.assertEqual(manifest["counts"]["source_free_geometry_ready_rows"], 5)
        self.assertEqual(manifest["counts"]["source_free_geometry_blocked_rows"], 5)
        self.assertEqual(
            manifest["counts"]["blocker_counts"],
            {
                "approved_source_free_active_site_locator_missing": 5,
                "source_backed_sidecar_lacks_residue_locator": 5,
            },
        )
        self.assertEqual(
            len(manifest["blocker_clearing_attempts"]),
            4,
        )
        self.assertEqual(
            [row["entry_id"] for row in manifest["row_manifests"][:3]],
            [
                "secondary_probe::cobalamin_radical_rearrangement",
                "secondary_probe::radical_sam_enzyme",
                "external_glycoside_panel",
            ],
        )
        by_entry = {row["entry_id"]: row for row in manifest["row_manifests"]}
        for entry_id in (
            "mh_066",
            "mh_067",
            "mh_068",
            "mh_073",
            "secondary_probe::radical_sam_enzyme",
        ):
            self.assertEqual(
                by_entry[entry_id]["source_free_predicted_geometry_status"],
                "ready_to_score_source_free_predicted_geometry",
            )
            self.assertEqual(by_entry[entry_id]["blockers"], [])
            self.assertTrue(
                by_entry[entry_id]["approved_source_free_active_site_locator"][
                    "ready_for_predicted_geometry_scoring"
                ]
            )
        for row in manifest["row_manifests"]:
            self.assertTrue(row["alphafolddb_predicted_cif"]["exists"])
            self.assertIn(
                row["source_free_predicted_geometry_status"],
                {
                    "blocked_source_free_geometry_preconditions",
                    "ready_to_score_source_free_predicted_geometry",
                },
            )
            self.assertEqual(
                row["source_free_predicted_geometry_retrieval"]["status"],
                "missing_pending_scoring",
            )
            self.assertFalse(row["source_backed_sidecar"]["predictive_use_allowed"])
            self.assertIsNone(row["existing_source_free_geometry_row"])
        self.assertFalse(
            manifest["guardrails"]["source_prose_used_as_predictive_geometry_feature"]
        )
        self.assertIn(
            "build-family-panel-source-free-predicted-geometry-sidecar-manifest",
            manifest["commands"]["reproduce_this_manifest"],
        )

    def test_family_panel_source_free_predicted_geometry_retrieval_current_counts(
        self,
    ) -> None:
        retrieval = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_source_free_predicted_geometry_retrieval_current702_20260601.json"
        )

        self.assertEqual(
            retrieval["status"],
            "source_free_predicted_geometry_retrieval_scored_review_only",
        )
        self.assertEqual(retrieval["counts"]["manifest_target_rows"], 10)
        self.assertEqual(retrieval["counts"]["manifest_ready_to_score_rows"], 5)
        self.assertEqual(retrieval["counts"]["predicted_geometry_ok_rows"], 5)
        self.assertEqual(retrieval["counts"]["runtime_blocked_ready_rows"], 0)
        self.assertEqual(retrieval["counts"]["precondition_blocked_rows_carried"], 5)
        self.assertEqual(retrieval["counts"]["retained_at_fixed_research_threshold"], 5)
        by_entry = {row["entry_id"]: row for row in retrieval["row_scores"]}
        self.assertEqual(
            set(by_entry),
            {
                "mh_066",
                "mh_067",
                "mh_068",
                "mh_073",
                "secondary_probe::radical_sam_enzyme",
            },
        )
        self.assertEqual(
            by_entry["mh_066"]["predicted_geometry_retrieval"]["top1_fingerprint_id"],
            "metal_dependent_hydrolase",
        )
        self.assertEqual(
            by_entry["mh_073"]["predicted_geometry_retrieval"]["top1_fingerprint_id"],
            "ser_his_acid_hydrolase",
        )
        self.assertEqual(
            by_entry["mh_067"]["predicted_geometry_status"],
            "ok",
        )
        self.assertEqual(by_entry["mh_067"]["resolved_residue_count"], 3)
        self.assertEqual(
            by_entry["mh_068"]["predicted_geometry_retrieval"]["top1_fingerprint_id"],
            "metal_dependent_hydrolase",
        )
        self.assertTrue(
            by_entry["secondary_probe::radical_sam_enzyme"][
                "fold_augmented_projection"
            ]["retained_at_fixed_research_threshold"]
        )
        self.assertFalse(retrieval["guardrails"]["source_text_used_for_score"])
        self.assertFalse(retrieval["guardrails"]["panel_ids_used_for_score"])

    def test_family_panel_source_free_predicted_geometry_mh066_source_check_current_result(
        self,
    ) -> None:
        check = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_predicted_geometry_source_check_"
                "mh_066_current702_20260601.json"
            )
        )

        self.assertEqual(
            check["status"],
            "source_check_completed_review_only_no_label_change",
        )
        self.assertEqual(check["row"]["entry_id"], "mh_066")
        self.assertEqual(
            check["row"]["current_v1_state"],
            "external_no_decision_review_only",
        )
        self.assertEqual(
            check["fold_augmented_readout"]["predicted_geometry_top1_fingerprint_id"],
            "metal_dependent_hydrolase",
        )
        self.assertEqual(
            check["fold_augmented_readout"]["nearest_atlas_true_fingerprint_id"],
            "metal_dependent_hydrolase",
        )
        self.assertTrue(check["fold_augmented_readout"]["geometry_fold_agreement"])
        self.assertEqual(
            check["duplicate_and_leakage_screen"]["exact_source_accession_matches"],
            [],
        )
        self.assertEqual(
            check["duplicate_and_leakage_screen"]["nearest_atlas_entry_id"],
            "m_csa:15",
        )
        self.assertEqual(
            check["source_check_decision"]["source_check_result"],
            "hold_as_review_only_metal_hydrolase_expansion_candidate",
        )
        self.assertFalse(check["source_check_decision"]["family_promotion_ready"])
        self.assertFalse(check["source_check_decision"]["label_import_ready"])
        self.assertTrue(check["guardrails"]["review_only"])
        self.assertFalse(check["guardrails"]["new_source_data_fetched"])

    def test_family_panel_source_free_predicted_geometry_mh073_source_check_current_result(
        self,
    ) -> None:
        check = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_predicted_geometry_source_check_"
                "mh_073_current702_20260601.json"
            )
        )

        self.assertEqual(
            check["status"],
            "source_check_completed_review_only_no_label_change",
        )
        self.assertEqual(check["row"]["entry_id"], "mh_073")
        self.assertEqual(
            check["row"]["candidate_role"],
            "external_hard_negative",
        )
        self.assertEqual(
            check["fold_augmented_readout"]["predicted_geometry_top1_fingerprint_id"],
            "ser_his_acid_hydrolase",
        )
        self.assertEqual(
            check["fold_augmented_readout"]["nearest_atlas_true_fingerprint_id"],
            "metal_dependent_hydrolase",
        )
        self.assertFalse(check["fold_augmented_readout"]["geometry_fold_agreement"])
        self.assertEqual(
            check["duplicate_and_leakage_screen"]["nearest_atlas_entry_id"],
            "m_csa:535",
        )
        self.assertEqual(
            check["source_check_decision"]["source_check_result"],
            "keep_as_review_only_gtpase_boundary_hard_negative",
        )
        self.assertFalse(check["source_check_decision"]["family_promotion_ready"])
        self.assertFalse(check["source_check_decision"]["label_import_ready"])
        self.assertTrue(check["guardrails"]["review_only"])
        self.assertFalse(check["guardrails"]["new_source_data_fetched"])

    def test_family_panel_source_free_predicted_geometry_radical_sam_source_check_current_result(
        self,
    ) -> None:
        check = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_predicted_geometry_source_check_"
                "secondary_probe_radical_sam_enzyme_current702_20260601.json"
            )
        )

        self.assertEqual(
            check["status"],
            "source_check_completed_review_only_no_label_change",
        )
        self.assertEqual(
            check["row"]["entry_id"],
            "secondary_probe::radical_sam_enzyme",
        )
        self.assertEqual(
            check["row"]["current_v1_state"],
            "secondary_probe_review_only_not_import_ready",
        )
        self.assertEqual(
            check["fold_augmented_readout"]["predicted_geometry_top1_fingerprint_id"],
            "metal_dependent_hydrolase",
        )
        self.assertEqual(
            check["fold_augmented_readout"]["nearest_atlas_true_fingerprint_id"],
            "plp_dependent_enzyme",
        )
        self.assertFalse(check["fold_augmented_readout"]["geometry_fold_agreement"])
        self.assertEqual(
            check["duplicate_and_leakage_screen"]["nearest_atlas_entry_id"],
            "m_csa:358",
        )
        self.assertEqual(
            check["source_check_decision"]["source_check_result"],
            "confirm_radical_sam_locus_review_only_no_family_promotion",
        )
        self.assertFalse(check["source_check_decision"]["family_promotion_ready"])
        self.assertFalse(check["source_check_decision"]["label_import_ready"])
        self.assertTrue(check["guardrails"]["review_only"])
        self.assertFalse(check["guardrails"]["new_source_data_fetched"])

    def test_family_panel_source_free_locator_remaining_blocker_action_queue_current_counts(
        self,
    ) -> None:
        queue = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_remaining_blocker_"
                "action_queue_current702_20260601.json"
            )
        )

        self.assertEqual(
            queue["status"],
            "source_free_locator_remaining_blocker_action_queue_ready_review_only",
        )
        self.assertEqual(queue["counts"]["blocked_rows"], 7)
        self.assertEqual(queue["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertEqual(
            queue["counts"]["action_class_counts"],
            {
                "alternate_coordinate_fetch_requires_manual_approval": 1,
                "ligand_specificity_review_required": 1,
                "new_nonlabel_locator_strategy_required": 1,
                "split_safe_template_check_required": 2,
                "uniprot_position_validation_required": 2,
            },
        )
        by_entry = {row["entry_id"]: row for row in queue["action_rows"]}
        self.assertEqual(
            by_entry["mh_065"]["action_class"],
            "uniprot_position_validation_required",
        )
        self.assertEqual(
            by_entry["mh_072"]["action_class"],
            "uniprot_position_validation_required",
        )
        self.assertEqual(
            by_entry["mh_064"]["alternate_pdb_ids"],
            ["3RKJ", "3RKK", "3SBL", "3SFP", "3SPU"],
        )
        self.assertFalse(queue["guardrails"]["locator_sidecars_created_or_copied"])
        self.assertFalse(queue["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(queue["guardrails"]["predicted_geometry_scored"])

    def test_family_panel_source_free_locator_uniprot_position_validation_mh065_mh072(
        self,
    ) -> None:
        validation = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_uniprot_position_"
                "validation_mh065_mh072_current702_20260601.json"
            )
        )

        self.assertEqual(
            validation["status"],
            "source_free_locator_uniprot_position_validation_blocked_review_only",
        )
        self.assertEqual(validation["counts"]["target_rows"], 2)
        self.assertEqual(validation["counts"]["validation_passed_rows"], 0)
        self.assertEqual(validation["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertEqual(
            validation["counts"]["rows_with_selected_pdb_struct_ref_accession_mismatch"],
            2,
        )
        self.assertFalse(
            validation["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(validation["guardrails"]["new_source_data_fetched"])
        self.assertFalse(validation["guardrails"]["predicted_geometry_scored"])

        by_entry = {row["entry_id"]: row for row in validation["validation_rows"]}
        self.assertEqual(
            by_entry["mh_065"]["accession_validation"]["result"],
            "blocked_accession_mismatch",
        )
        self.assertEqual(
            by_entry["mh_065"]["accession_validation"][
                "selected_pdb_struct_ref_accessions"
            ],
            ["Q932P5"],
        )
        self.assertEqual(
            by_entry["mh_072"]["accession_validation"]["result"],
            "blocked_accession_mismatch",
        )
        self.assertEqual(
            by_entry["mh_072"]["accession_validation"][
                "selected_pdb_struct_ref_accessions"
            ],
            ["P08324"],
        )
        for row in validation["validation_rows"]:
            self.assertEqual(
                row["validation_decision"]["sequence_position_validated_locator_count"],
                0,
            )
            self.assertFalse(row["validation_decision"]["approved_locator_copy_allowed"])

    def test_family_panel_source_free_locator_accession_equivalence_position_audit_mh065_mh072(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_accession_equivalence_"
                "position_audit_mh065_mh072_current702_20260602.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "source_free_locator_accession_equivalence_position_audit_blocked_review_only",
        )
        self.assertEqual(audit["counts"]["target_rows"], 2)
        self.assertEqual(
            audit["counts"]["selected_pdb_struct_ref_accession_mismatch_rows"],
            2,
        )
        self.assertEqual(
            audit["counts"]["candidate_locator_positions_checked"],
            6,
        )
        self.assertEqual(
            audit["counts"]["requested_afdb_expected_code_matches"],
            0,
        )
        self.assertEqual(
            audit["counts"]["rows_with_all_requested_afdb_position_mismatches"],
            2,
        )
        self.assertFalse(
            audit["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(audit["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(audit["guardrails"]["predicted_geometry_scored"])
        self.assertFalse(audit["decision"]["raw_selected_pdb_locator_copy_safe"])
        self.assertFalse(audit["decision"]["representative_equivalence_alone_sufficient"])

        by_entry = {row["entry_id"]: row for row in audit["audit_rows"]}
        self.assertEqual(
            by_entry["mh_065"]["selected_pdb_struct_ref_accessions"],
            ["Q932P5"],
        )
        self.assertEqual(
            by_entry["mh_072"]["selected_pdb_struct_ref_accessions"],
            ["P08324"],
        )
        self.assertEqual(
            by_entry["mh_065"]["requested_afdb_expected_code_match_count"],
            0,
        )
        self.assertEqual(
            by_entry["mh_072"]["requested_afdb_expected_code_match_count"],
            0,
        )

    def test_family_panel_source_free_locator_matching_coordinate_scout_mh065_mh072(
        self,
    ) -> None:
        scout = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_matching_coordinate_"
                "scout_mh065_mh072_current702_20260602.json"
            )
        )

        self.assertEqual(
            scout["status"],
            "source_free_locator_matching_coordinate_scout_blocked_no_replacement_matches_review_only",
        )
        self.assertEqual(scout["counts"]["target_rows"], 2)
        self.assertEqual(scout["counts"]["matching_replacement_coordinates"], 0)
        self.assertEqual(scout["counts"]["same_accession_struct_ref_coordinates"], 2)
        self.assertEqual(
            scout["counts"]["rows_with_same_accession_afdb_coordinate_only"],
            2,
        )
        self.assertFalse(scout["decision"]["matching_coordinate_gate_cleared"])
        self.assertFalse(scout["decision"]["raw_representative_coordinate_copy_allowed"])
        self.assertFalse(scout["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(
            scout["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )

        by_entry = {row["entry_id"]: row for row in scout["row_scouts"]}
        self.assertEqual(
            by_entry["mh_065"]["decision_status"],
            "only_requested_afdb_coordinate_present_prior_residue_mismatch",
        )
        self.assertEqual(
            by_entry["mh_065"]["matching_replacement_coordinate_count"],
            0,
        )
        self.assertEqual(
            by_entry["mh_072"]["same_accession_afdb_coordinate_count"],
            1,
        )

    def test_family_panel_source_free_locator_split_safe_template_check_mh067_mh068(
        self,
    ) -> None:
        check = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_split_safe_template_"
                "check_mh067_mh068_current702_20260601.json"
            )
        )

        self.assertEqual(
            check["status"],
            "source_free_locator_split_safe_template_check_passed_review_only_copy_not_authorized",
        )
        self.assertEqual(check["counts"]["target_rows"], 2)
        self.assertEqual(check["counts"]["rows_with_heldout_same_accession_matches"], 0)
        self.assertEqual(
            check["counts"]["split_safe_template_check_passed_rows"],
            2,
        )
        self.assertEqual(check["counts"]["approved_locator_copy_authorized_rows"], 0)
        self.assertEqual(check["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertFalse(
            check["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(check["guardrails"]["heldout_rows_used_as_templates"])
        self.assertFalse(check["guardrails"]["predicted_geometry_scored"])

        by_entry = {row["entry_id"]: row for row in check["split_check_rows"]}
        self.assertEqual(
            by_entry["mh_067"]["same_accession_current702_matches"][0]["entry_id"],
            "m_csa:216",
        )
        self.assertEqual(
            by_entry["mh_068"]["same_accession_current702_matches"][0]["entry_id"],
            "m_csa:158",
        )
        for row in check["split_check_rows"]:
            self.assertEqual(row["heldout_same_accession_matches"], [])
            self.assertEqual(
                row["split_safety_decision"]["split_safe_template_check_result"],
                "passed_no_heldout_same_accession_template",
            )
            self.assertTrue(
                row["split_safety_decision"]["manual_copy_approval_still_required"]
            )
            self.assertFalse(
                row["split_safety_decision"]["approved_locator_copy_allowed_now"]
            )

    def test_family_panel_source_free_locator_ligand_specificity_external_glycoside(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_ligand_specificity_review_"
                "external_glycoside_panel_current702_20260601.json"
            )
        )

        self.assertEqual(
            review["status"],
            "source_free_locator_ligand_specificity_review_rejected_selected_acetate_review_only",
        )
        self.assertEqual(review["counts"]["target_rows"], 1)
        self.assertEqual(review["counts"]["selected_ligand_specificity_passed_rows"], 0)
        self.assertEqual(review["counts"]["selected_ligand_specificity_rejected_rows"], 1)
        self.assertEqual(review["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertFalse(
            review["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(review["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(review["guardrails"]["predicted_geometry_scored"])

        row = review["review_rows"][0]
        self.assertEqual(row["entry_id"], "external_glycoside_panel")
        self.assertEqual(row["selected_ligand_site"]["comp_id"], "ACT")
        self.assertEqual(
            row["selected_ligand_review"]["review_result"],
            "rejected_selected_ligand_not_biologically_specific_for_glycoside_hydrolase_active_site",
        )
        self.assertFalse(
            row["selected_ligand_review"]["acceptable_for_audited_locator_copy"]
        )
        self.assertEqual(
            row["alternate_ligand_candidates_observed"][0]["comp_id"],
            "NAG",
        )
        self.assertFalse(
            row["alternate_ligand_candidates_observed"][0]["automatic_retarget_allowed"]
        )
        self.assertFalse(row["validation_decision"]["approved_locator_copy_allowed_now"])

    def test_family_panel_source_free_locator_glycoside_nag_validator_external_glycoside(
        self,
    ) -> None:
        validator = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_glycoside_nag_validator_"
                "external_glycoside_panel_current702_20260602.json"
            )
        )

        self.assertEqual(
            validator["status"],
            "source_free_locator_glycoside_nag_validator_rejected_nag_glycan_review_only",
        )
        self.assertEqual(validator["counts"]["target_rows"], 1)
        self.assertEqual(validator["counts"]["nag_candidate_sites"], 4)
        self.assertEqual(
            validator["counts"]["nag_sites_with_near_covalent_c1_asn_contact"],
            4,
        )
        self.assertEqual(
            validator["counts"]["approved_locator_copy_authorized_rows"], 0
        )
        self.assertEqual(
            validator["counts"]["ready_for_predicted_geometry_scoring"], 0
        )
        self.assertFalse(
            validator["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(validator["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(validator["guardrails"]["predicted_geometry_scored"])

        row = validator["validation_rows"][0]
        self.assertEqual(row["entry_id"], "external_glycoside_panel")
        self.assertEqual(row["alternate_ligand_comp_id"], "NAG")
        self.assertTrue(
            all(
                site["validator_result"]
                == "rejected_nag_glycan_or_n_linked_glycosylation_context"
                for site in row["nag_site_validations"]
            )
        )
        self.assertTrue(
            all(
                not site["automatic_locator_copy_allowed"]
                for site in row["nag_site_validations"]
            )
        )

    def test_family_panel_source_free_locator_glycoside_substrate_coordinate_scout(
        self,
    ) -> None:
        scout = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_glycoside_substrate_"
                "coordinate_scout_external_glycoside_panel_current702_20260602.json"
            )
        )

        self.assertEqual(
            scout["status"],
            "source_free_locator_glycoside_substrate_coordinate_scout_blocked_no_substrate_like_local_coordinate_review_only",
        )
        self.assertEqual(scout["counts"]["target_rows"], 1)
        self.assertEqual(scout["counts"]["same_accession_coordinate_records"], 4)
        self.assertEqual(
            scout["counts"]["same_accession_records_with_rejected_glycan_or_buffer_ligands"],
            1,
        )
        self.assertEqual(scout["counts"]["substrate_like_coordinate_candidates"], 0)
        self.assertFalse(scout["decision"]["substrate_coordinate_gate_cleared"])
        self.assertFalse(scout["decision"]["raw_acetate_or_nag_locator_copy_allowed"])
        self.assertFalse(
            scout["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(scout["guardrails"]["new_coordinates_fetched"])

        pdb_records = [
            row
            for row in scout["coordinate_records"]
            if row["coordinate_kind"] == "pdb_mmcif"
        ]
        self.assertEqual(len(pdb_records), 1)
        self.assertEqual(
            pdb_records[0]["rejected_glycan_or_buffer_ligand_counts"]["NAG"],
            434,
        )
        self.assertEqual(pdb_records[0]["substrate_like_ligand_counts"], {})

    def test_family_panel_source_free_locator_external_glycoside_block_decision(
        self,
    ) -> None:
        decision = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_external_glycoside_"
                "block_decision_current702_20260603.json"
            )
        )

        self.assertEqual(
            decision["status"],
            "source_free_locator_external_glycoside_block_decision_rejected_review_only",
        )
        self.assertEqual(decision["counts"]["target_rows"], 1)
        self.assertEqual(decision["counts"]["same_accession_coordinate_records"], 4)
        self.assertEqual(
            decision["counts"]["substrate_like_coordinate_candidates"], 0
        )
        self.assertTrue(
            decision["decision"]["external_glycoside_panel_left_blocked"]
        )
        self.assertFalse(decision["decision"]["copy_7qqf_acetate_or_nag_locator"])
        self.assertFalse(decision["decision"]["predicted_geometry_scoring_authorized"])
        self.assertFalse(
            decision["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(decision["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(decision["guardrails"]["predicted_geometry_scored"])

    def test_family_panel_source_free_locator_policy_blockers_mh064_q59490(
        self,
    ) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_policy_blockers_"
                "mh064_q59490_current702_20260601.json"
            )
        )

        self.assertEqual(
            packet["status"],
            "source_free_locator_policy_blockers_ready_for_human_decision_review_only",
        )
        self.assertEqual(packet["counts"]["target_rows"], 2)
        self.assertEqual(packet["counts"]["rows_with_candidate_residue_locators"], 0)
        self.assertEqual(
            packet["counts"]["rows_requiring_alternate_coordinate_fetch_approval"],
            1,
        )
        self.assertEqual(
            packet["counts"]["rows_requiring_new_nonlabel_locator_strategy"],
            1,
        )
        self.assertEqual(packet["counts"]["alternate_coordinate_fetch_commands_manifested"], 5)
        self.assertEqual(packet["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertFalse(
            packet["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(packet["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(packet["guardrails"]["predicted_geometry_scored"])

        by_entry = {row["entry_id"]: row for row in packet["policy_rows"]}
        self.assertEqual(len(by_entry["mh_064"]["alternate_pdb_ids"]), 5)
        self.assertEqual(
            by_entry["mh_064"]["policy_decision_required"],
            "approve_or_reject_fetch_of_frozen_alternate_coordinates",
        )
        self.assertEqual(
            by_entry["secondary_probe::cobalamin_radical_rearrangement"][
                "policy_decision_required"
            ],
            "design_nonlabel_locator_strategy_or_authorize_alternate_source_row",
        )
        self.assertEqual(
            by_entry["secondary_probe::cobalamin_radical_rearrangement"][
                "alternate_coordinate_fetch_commands"
            ],
            [],
        )

    def test_family_panel_source_free_locator_q59490_block_decision(self) -> None:
        decision = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_q59490_block_decision_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            decision["status"],
            "source_free_locator_q59490_block_decision_rejected_review_only",
        )
        self.assertEqual(decision["counts"]["target_rows"], 1)
        self.assertEqual(decision["counts"]["primary_q59490_local_coordinate_paths"], 3)
        self.assertEqual(decision["counts"]["alternate_eligible_source_rows"], 0)
        self.assertEqual(decision["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertTrue(decision["decision"]["q59490_left_blocked"])
        self.assertFalse(decision["decision"]["alternate_source_substitution_authorized"])
        self.assertFalse(decision["decision"]["nonlabel_locator_strategy_authorized"])
        self.assertFalse(decision["decision"]["predicted_geometry_scoring_authorized"])
        self.assertFalse(
            decision["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(decision["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(decision["guardrails"]["predicted_geometry_scored"])

    def test_family_panel_source_free_locator_mh064_alternate_coordinate_local_cache_preflight(
        self,
    ) -> None:
        preflight = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_mh064_alternate_coordinate_"
                "local_cache_preflight_current702_20260602.json"
            )
        )

        self.assertEqual(
            preflight["status"],
            "source_free_locator_mh064_alternate_coordinate_local_cache_preflight_blocked_no_cached_alternates_review_only",
        )
        self.assertEqual(preflight["counts"]["alternate_pdb_ids_checked"], 5)
        self.assertEqual(preflight["counts"]["alternate_coordinate_files_cached"], 0)
        self.assertEqual(preflight["counts"]["alternate_coordinate_files_missing"], 5)
        self.assertEqual(preflight["counts"]["new_coordinates_fetched"], 0)
        self.assertFalse(preflight["guardrails"]["network_fetch_attempted"])
        self.assertFalse(preflight["guardrails"]["new_coordinates_fetched"])
        self.assertTrue(preflight["decision"]["fetch_policy_decision_still_required"])
        self.assertFalse(
            preflight["decision"][
                "alternate_coordinate_fetch_already_satisfied_by_local_cache"
            ]
        )
        self.assertEqual(
            [row["pdb_id"] for row in preflight["alternate_coordinate_rows"]],
            ["3RKJ", "3RKK", "3SBL", "3SFP", "3SPU"],
        )

    def test_family_panel_source_free_locator_mh064_block_decision(self) -> None:
        decision = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_mh064_block_decision_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            decision["status"],
            "source_free_locator_mh064_block_decision_rejected_review_only",
        )
        self.assertEqual(decision["counts"]["alternate_pdb_ids_checked"], 5)
        self.assertEqual(decision["counts"]["alternate_coordinate_files_cached"], 0)
        self.assertEqual(decision["counts"]["alternate_coordinate_files_missing"], 5)
        self.assertEqual(decision["counts"]["new_coordinates_fetched"], 0)
        self.assertTrue(decision["decision"]["mh064_left_blocked"])
        self.assertFalse(decision["decision"]["alternate_coordinate_fetch_authorized"])
        self.assertFalse(decision["decision"]["predicted_geometry_scoring_authorized"])
        self.assertFalse(decision["guardrails"]["network_fetch_attempted"])
        self.assertFalse(decision["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(
            decision["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )

    def test_family_panel_source_free_locator_policy_closure_status(self) -> None:
        closure = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_policy_closure_status_"
                "current702_20260603.json"
            )
        )

        self.assertEqual(
            closure["status"],
            "source_free_locator_policy_closure_status_closed_for_automation_blocked_review_only",
        )
        self.assertEqual(closure["counts"]["block_decision_artifacts"], 4)
        self.assertEqual(closure["counts"]["blocked_locator_rows"], 5)
        self.assertEqual(
            closure["counts"]["priority_rows_mechanically_clearable_now"], 0
        )
        self.assertEqual(
            closure["counts"]["locator_policy_rows_approved_for_copy_or_scoring"], 0
        )
        self.assertEqual(closure["counts"]["import_preview_ready_rows"], 0)
        self.assertEqual(closure["counts"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            closure["decision"]["automation_clearable_locator_decisions_remaining"],
            0,
        )
        self.assertFalse(closure["decision"]["family_panel_import_preview_unblocked_now"])
        self.assertFalse(closure["decision"]["predicted_geometry_scoring_authorized"])
        self.assertFalse(
            closure["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(closure["guardrails"]["coordinates_fetched"])
        self.assertFalse(closure["guardrails"]["predicted_geometry_scored"])

    def test_family_panel_source_free_locator_q59490_nonlabel_locator_feasibility_audit(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_q59490_nonlabel_locator_"
                "feasibility_audit_current702_20260602.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "source_free_locator_q59490_nonlabel_locator_feasibility_blocked_no_coordinate_anchor_review_only",
        )
        self.assertEqual(audit["counts"]["target_rows"], 1)
        self.assertEqual(audit["counts"]["candidate_residue_locators"], 0)
        self.assertEqual(audit["counts"]["coordinate_files_checked"], 2)
        self.assertEqual(
            audit["counts"]["coordinate_files_with_nonwater_hetatm_or_metal_anchor"],
            0,
        )
        self.assertEqual(audit["counts"]["nonwater_hetatm_atoms_detected"], 0)
        self.assertEqual(audit["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertFalse(
            audit["guardrails"]["source_text_or_label_fields_used_as_predictive_features"]
        )
        self.assertFalse(audit["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(audit["guardrails"]["predicted_geometry_scored"])
        self.assertFalse(
            audit["decision"]["coordinate_only_nonlabel_locator_strategy_available_now"]
        )
        self.assertTrue(
            audit["decision"]["manual_nonlabel_strategy_or_alternate_source_required"]
        )

    def test_family_panel_source_free_locator_blocker_resolution_status_current(
        self,
    ) -> None:
        status = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_blocker_resolution_status_"
                "current702_20260601.json"
            )
        )

        self.assertEqual(
            status["status"],
            "source_free_locator_blocker_resolution_status_ready_review_only",
        )
        self.assertEqual(status["counts"]["blocked_rows_tracked"], 5)
        self.assertEqual(status["counts"]["automation_discovery_completed_rows"], 7)
        self.assertEqual(status["counts"]["ready_for_predicted_geometry_scoring"], 2)
        self.assertEqual(status["counts"]["locator_sidecars_created_or_copied"], 2)
        self.assertEqual(
            status["counts"]["resolution_class_counts"],
            {
                "accession_equivalence_or_matching_coordinate_required": 2,
                "alternate_coordinate_fetch_approval_required": 1,
                "ligand_specificity_validator_or_substrate_coordinate_required": 1,
                "nonlabel_locator_strategy_or_alternate_source_required": 1,
            },
        )
        self.assertTrue(
            status["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(status["guardrails"]["new_coordinates_fetched"])
        self.assertTrue(status["guardrails"]["predicted_geometry_scored"])

        by_entry = {row["entry_id"]: row for row in status["resolution_rows"]}
        self.assertEqual(
            by_entry["mh_065"]["resolution_status"],
            "blocked_accession_mismatch_requested_afdb_position_mismatch",
        )
        self.assertEqual(
            by_entry["mh_072"]["resolution_status"],
            "blocked_accession_mismatch_requested_afdb_position_mismatch",
        )
        self.assertIn(
            "accession_equivalence_position_audit_path",
            by_entry["mh_065"],
        )
        self.assertNotIn("mh_067", by_entry)
        self.assertNotIn("mh_068", by_entry)
        resolved = {row["entry_id"]: row for row in status["resolved_rows"]}
        self.assertEqual(
            resolved["mh_067"]["resolution_status"],
            "approved_locator_copied_schema_passed_scored_source_checked_review_only",
        )
        self.assertEqual(
            by_entry["external_glycoside_panel"]["resolution_status"],
            "selected_acetate_and_nag_glycan_validator_rejected",
        )
        self.assertIn(
            "glycoside_nag_validator_path",
            by_entry["external_glycoside_panel"],
        )
        self.assertEqual(
            by_entry["secondary_probe::cobalamin_radical_rearrangement"][
                "resolution_status"
            ],
            "blocked_no_coordinate_anchor_nonlabel_strategy_required",
        )
        self.assertIn(
            "nonlabel_locator_feasibility_audit_path",
            by_entry["secondary_probe::cobalamin_radical_rearrangement"],
        )
        self.assertEqual(
            by_entry["mh_064"]["resolution_status"],
            "blocked_pending_fetch_policy_no_local_alternates_cached",
        )
        self.assertIn(
            "alternate_coordinate_local_cache_preflight_path",
            by_entry["mh_064"],
        )

    def test_family_panel_source_free_active_site_locator_schema_current_counts(
        self,
    ) -> None:
        schema = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_source_free_active_site_locator_schema_current702_20260601.json"
        )

        self.assertEqual(
            schema["status"],
            "source_free_active_site_locator_schema_ready_review_only",
        )
        self.assertEqual(schema["counts"]["target_rows"], 10)
        self.assertEqual(schema["counts"]["required_residue_locator_minimum"], 2)
        self.assertEqual(schema["counts"]["allowed_locator_evidence_classes"], 4)
        self.assertFalse(
            schema["guardrails"][
                "source_text_or_label_fields_allowed_as_predictive_features"
            ]
        )
        self.assertIn(
            "source_prose",
            schema["forbidden_predictive_fields"],
        )
        self.assertIn(
            "residue_locators",
            schema["sidecar_required_top_level_fields"],
        )
        self.assertIn(
            "sequence_position",
            schema["residue_locator_required_fields"],
        )
        self.assertEqual(
            [row["entry_id"] for row in schema["target_rows"][:3]],
            [
                "secondary_probe::cobalamin_radical_rearrangement",
                "secondary_probe::radical_sam_enzyme",
                "external_glycoside_panel",
            ],
        )
        self.assertIn(
            "build-fold-augmented-family-panel-research-readout",
            "\n".join(schema["next_commands_after_sidecars_exist"]),
        )

    def test_family_panel_source_free_active_site_locator_schema_audit_current_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_source_free_active_site_locator_schema_audit_current702_20260601.json"
        )

        self.assertEqual(
            audit["status"],
            "source_free_active_site_locator_schema_audit_blocked_missing_sidecars",
        )
        self.assertEqual(audit["counts"]["target_rows"], 10)
        self.assertEqual(audit["counts"]["locator_sidecars_present"], 5)
        self.assertEqual(audit["counts"]["locator_sidecars_missing"], 5)
        self.assertEqual(audit["counts"]["ready_for_predicted_geometry_scoring"], 5)
        self.assertEqual(
            audit["counts"]["critical_counts"],
            {"locator_sidecar_missing": 5},
        )
        self.assertFalse(audit["guardrails"]["predicted_geometry_scored"])
        by_entry = {row["entry_id"]: row for row in audit["row_audits"]}
        self.assertEqual(by_entry["mh_066"]["status"], "passed")
        self.assertEqual(by_entry["mh_067"]["status"], "passed")
        self.assertEqual(by_entry["mh_068"]["status"], "passed")
        self.assertEqual(by_entry["mh_073"]["status"], "passed")
        self.assertEqual(
            by_entry["secondary_probe::radical_sam_enzyme"]["status"],
            "passed",
        )
        self.assertEqual(
            by_entry["secondary_probe::radical_sam_enzyme"]["residue_locator_count"],
            4,
        )
        self.assertIn(
            "secondary_probe_cobalamin_radical_rearrangement_Q59490.json",
            audit["row_audits"][0]["path"],
        )

    def test_family_panel_source_free_locator_copy_decision_mh067_mh068(
        self,
    ) -> None:
        decision = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_copy_decision_"
                "mh067_mh068_current702_20260602.json"
            )
        )

        self.assertEqual(
            decision["status"],
            "source_free_locator_copy_decision_mh067_mh068_approved_review_only",
        )
        self.assertEqual(decision["operator_decision"], "approve")
        self.assertEqual(decision["counts"]["target_rows"], 2)
        self.assertEqual(decision["counts"]["approved_locator_copy_rows"], 2)
        self.assertEqual(decision["counts"]["blocked_preflight_rows"], 0)
        self.assertEqual(
            decision["counts"]["predicted_model_sequence_position_repairs"],
            3,
        )
        self.assertTrue(
            decision["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(
            decision["guardrails"][
                "source_text_or_label_fields_used_as_predictive_features"
            ]
        )
        by_entry = {row["entry_id"]: row for row in decision["row_decisions"]}
        self.assertEqual(
            by_entry["mh_067"]["decision"],
            "approved_for_audited_locator_copy_review_only",
        )
        self.assertEqual(
            by_entry["mh_067"]["predicted_model_sequence_position_repair_count"],
            3,
        )
        self.assertEqual(
            [
                repair["resolved_sequence_position"]
                for repair in by_entry["mh_067"][
                    "predicted_model_sequence_position_repairs"
                ]
            ],
            [96, 119, 94],
        )
        self.assertEqual(
            by_entry["mh_068"]["predicted_model_sequence_position_repair_count"],
            0,
        )

    def test_family_panel_source_free_active_site_locator_audited_dir_after_approval(
        self,
    ) -> None:
        locator_dir = (
            ROOT
            / "artifacts"
            / "family_panel_source_free_active_site_locators_current702_20260601"
        )

        # After the 2026-06-03 Lever 2 reviewer decision (approve 53, reject
        # m_csa:723 and m_csa:599), the audited dir holds the 5 family-panel
        # locators plus the 53 approved priority-1 source-free locators.
        self.assertEqual(
            sorted(path.name for path in locator_dir.glob("*.json")),
            [
                "m_csa_109_Q02127.json",
                "m_csa_115_Q9T0N8.json",
                "m_csa_121_P07850.json",
                "m_csa_131_P20586.json",
                "m_csa_159_P0A434.json",
                "m_csa_163_P0A7Y4.json",
                "m_csa_171_P00730.json",
                "m_csa_180_P35505.json",
                "m_csa_188_P09147.json",
                "m_csa_199_P04425.json",
                "m_csa_211_P38489.json",
                "m_csa_220_P20906.json",
                "m_csa_239_P00433.json",
                "m_csa_242_Q8I914.json",
                "m_csa_250_P04963.json",
                "m_csa_311_P00924.json",
                "m_csa_321_P09155.json",
                "m_csa_323_P05314.json",
                "m_csa_32_Q04760.json",
                "m_csa_333_Q9RUB5.json",
                "m_csa_352_P00949.json",
                "m_csa_356_P14769.json",
                "m_csa_370_O75164.json",
                "m_csa_384_P23395.json",
                "m_csa_392_P07801.json",
                "m_csa_397_P04063.json",
                "m_csa_3_P15559.json",
                "m_csa_403_P07584.json",
                "m_csa_418_P37821.json",
                "m_csa_419_O52552.json",
                "m_csa_43_P80366.json",
                "m_csa_44_P00634.json",
                "m_csa_45_P43379.json",
                "m_csa_46_P14385.json",
                "m_csa_480_P26214.json",
                "m_csa_497_Q9FDN7.json",
                "m_csa_517_P61517.json",
                "m_csa_526_P11708.json",
                "m_csa_541_P75430.json",
                "m_csa_545_Q7M523.json",
                "m_csa_551_P15245.json",
                "m_csa_56_Q9WZW0.json",
                "m_csa_709_P00431.json",
                "m_csa_710_P25524.json",
                "m_csa_714_P0ABI8.json",
                "m_csa_750_P55792.json",
                "m_csa_853_P31570.json",
                "m_csa_854_P80147.json",
                "m_csa_916_P9WI55.json",
                "m_csa_97_P0ABF6.json",
                "m_csa_990_Q8GS60.json",
                "m_csa_994_Q9Y3Z3.json",
                "m_csa_9_P31153.json",
                "mh_066_P52699.json",
                "mh_067_P00918.json",
                "mh_068_P15289.json",
                "mh_073_P01112.json",
                "secondary_probe_radical_sam_enzyme_A0A1M6T2I7.json",
            ],
        )
        # The two rejected in-scope serine-hydrolase rows must not be materialized.
        self.assertFalse((locator_dir / "m_csa_723_P00782.json").exists())
        self.assertFalse((locator_dir / "m_csa_599_P36936.json").exists())
        # A materialized Lever 2 sidecar carries the explicit reviewer signature
        # and stays split-protected (review-only, not for training/threshold/import).
        m_csa_3 = _load_json(locator_dir / "m_csa_3_P15559.json")
        self.assertEqual(
            m_csa_3["manual_review_approval"]["approved_by"], "VivekVardhanArrabelli"
        )
        self.assertEqual(
            m_csa_3["manual_review_approval"]["approval_source"],
            "explicit_locator_rewrite_decision_artifact",
        )
        self.assertTrue(m_csa_3["ready_for_predicted_geometry_scoring"])
        self.assertTrue(m_csa_3["split_protection"]["review_only"])
        self.assertFalse(m_csa_3["split_protection"]["allowed_for_training"])
        self.assertFalse(m_csa_3["split_protection"]["allowed_for_threshold_selection"])
        self.assertFalse(m_csa_3["split_protection"]["ready_for_label_import"])
        self.assertTrue(
            all(value is False for value in m_csa_3["forbidden_feature_audit"].values())
        )
        mh_067 = _load_json(locator_dir / "mh_067_P00918.json")
        self.assertEqual(
            [locator["sequence_position"] for locator in mh_067["residue_locators"]],
            [96, 119, 94],
        )
        self.assertEqual(
            mh_067["manual_review_approval"]["approval_source"],
            "automation_exact_next_action_2026-06-02_after_split_safe_pass",
        )
        radical_sam = _load_json(
            locator_dir / "secondary_probe_radical_sam_enzyme_A0A1M6T2I7.json"
        )
        self.assertNotIn("panel_id", radical_sam)
        self.assertNotIn("rank", radical_sam)
        self.assertEqual(len(radical_sam["residue_locators"]), 4)
        self.assertTrue(
            all(
                locator["role_hint"] == "iron_sulfur_cluster_contact_candidate"
                for locator in radical_sam["residue_locators"]
            )
        )

    def test_family_panel_source_free_active_site_locator_materialization_plan_counts(
        self,
    ) -> None:
        plan = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_source_free_active_site_locator_materialization_plan_current702_20260601.json"
        )

        self.assertEqual(
            plan["status"],
            "source_free_active_site_locator_materialization_plan_ready_review_only",
        )
        self.assertEqual(plan["counts"]["planned_rows"], 10)
        self.assertEqual(plan["counts"]["locator_sidecars_present_before_plan"], 3)
        self.assertEqual(plan["counts"]["locator_sidecars_ready_before_plan"], 3)
        self.assertEqual(
            plan["counts"]["suggested_locator_policy_counts"],
            {
                "structure_local_ligand_geometry_without_source_text_candidate_requires_validator": 8,
                "train_cal_template_alignment_without_heldout_rows_candidate_requires_split_check": 2,
            },
        )
        self.assertFalse(plan["guardrails"]["locator_sidecars_created"])
        self.assertFalse(plan["guardrails"]["predicted_geometry_scored"])
        self.assertEqual(
            [row["entry_id"] for row in plan["row_plans"][:3]],
            [
                "secondary_probe::cobalamin_radical_rearrangement",
                "secondary_probe::radical_sam_enzyme",
                "external_glycoside_panel",
            ],
        )
        by_entry = {row["entry_id"]: row for row in plan["row_plans"]}
        self.assertEqual(
            by_entry["mh_067"]["suggested_locator_policy"],
            "train_cal_template_alignment_without_heldout_rows_candidate_requires_split_check",
        )
        self.assertIn(
            "audit-family-panel-source-free-active-site-locator-schema",
            plan["commands"]["rerun_schema_audit"],
        )

    def test_family_panel_source_free_active_site_locator_template_bundle_counts(
        self,
    ) -> None:
        bundle = _load_json(
            ROOT
            / "artifacts"
            / "v3_family_panel_source_free_active_site_locator_template_bundle_current702_20260601.json"
        )

        self.assertEqual(
            bundle["status"],
            "source_free_active_site_locator_templates_ready_review_only",
        )
        self.assertEqual(bundle["counts"]["templates"], 10)
        self.assertEqual(bundle["counts"]["templates_ready_for_scoring"], 0)
        self.assertTrue(bundle["guardrails"]["template_only"])
        self.assertFalse(
            bundle["guardrails"]["locator_sidecars_created_in_audited_dir"]
        )
        self.assertFalse(bundle["guardrails"]["predicted_geometry_scored"])
        template_dir = ROOT / bundle["template_dir"]
        self.assertEqual(len(list(template_dir.glob("*.json"))), 10)
        first_template_path = ROOT / bundle["templates"][0]["template_path"]
        self.assertIn(
            "secondary_probe_cobalamin_radical_rearrangement_Q59490.json",
            str(first_template_path),
        )
        self.assertTrue(first_template_path.exists())
        first_template = _load_json(first_template_path)
        self.assertEqual(first_template["status"], "template_only_not_ready_for_scoring")
        self.assertFalse(first_template["ready_for_predicted_geometry_scoring"])
        self.assertEqual(first_template["residue_locators"], [])
        self.assertTrue(
            first_template["template_guardrails"][
                "do_not_place_in_audited_locator_dir_until_filled_and_reviewed"
            ]
        )
        self.assertFalse(
            first_template["template_guardrails"][
                "source_text_or_label_fields_allowed_as_predictive_features"
            ]
        )
        self.assertFalse(first_template["split_protection"]["ready_for_label_import"])

    def test_family_panel_source_free_active_site_locator_candidate_audit_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_active_site_locator_candidate_audit_"
                "current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "source_free_active_site_locator_candidates_staged_review_only",
        )
        self.assertEqual(audit["counts"]["target_rows"], 10)
        self.assertEqual(audit["counts"]["candidate_sidecars_staged"], 10)
        self.assertEqual(
            audit["counts"]["rows_with_minimum_candidate_residue_locators"],
            8,
        )
        self.assertEqual(audit["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertEqual(audit["counts"]["rows_requiring_split_safe_template_check"], 2)
        self.assertEqual(
            audit["counts"]["rows_with_all_candidate_sequence_positions_validated"],
            6,
        )
        self.assertFalse(
            audit["guardrails"]["locator_sidecars_created_in_audited_dir"]
        )
        self.assertFalse(audit["guardrails"]["predicted_geometry_scored"])
        candidate_dir = ROOT / audit["candidate_dir"]
        self.assertEqual(len(list(candidate_dir.glob("*.json"))), 10)
        first = audit["row_audits"][0]
        self.assertEqual(
            first["entry_id"],
            "secondary_probe::cobalamin_radical_rearrangement",
        )
        self.assertEqual(first["candidate_residue_locator_count"], 0)
        second = audit["row_audits"][1]
        self.assertEqual(second["selected_ligand_site"]["comp_id"], "SF4")
        self.assertEqual(second["candidate_residue_locator_count"], 8)
        self.assertEqual(second["sequence_position_validated_locator_count"], 8)
        second_sidecar = _load_json(ROOT / second["candidate_path"])
        self.assertFalse(second_sidecar["ready_for_predicted_geometry_scoring"])
        self.assertTrue(
            second_sidecar["candidate_guardrails"][
                "written_outside_audited_locator_dir"
            ]
        )

    def test_family_panel_source_free_active_site_locator_candidate_integrity_audit_counts(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_active_site_locator_"
                "candidate_integrity_audit_current702_20260601.json"
            )
        )

        self.assertEqual(
            audit["status"],
            "source_free_active_site_locator_candidate_integrity_passed_review_only",
        )
        self.assertEqual(audit["counts"]["candidate_sidecars_expected"], 10)
        self.assertEqual(audit["counts"]["candidate_sidecar_files_present"], 10)
        self.assertEqual(audit["counts"]["integrity_passed_sidecars"], 10)
        self.assertEqual(audit["counts"]["integrity_blocked_sidecars"], 0)
        self.assertEqual(audit["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertEqual(audit["counts"]["critical_counts"], {})
        self.assertFalse(audit["guardrails"]["locator_sidecars_created_in_audited_dir"])
        self.assertFalse(audit["guardrails"]["predicted_geometry_scored"])
        by_entry = {row["entry_id"]: row for row in audit["row_audits"]}
        self.assertTrue(
            by_entry["secondary_probe::radical_sam_enzyme"][
                "payload_matches_candidate_audit"
            ]
        )
        self.assertFalse(
            by_entry["secondary_probe::radical_sam_enzyme"][
                "inside_audited_locator_dir"
            ]
        )

    def test_family_panel_source_free_active_site_locator_manual_review_packet_counts(
        self,
    ) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_active_site_locator_"
                "manual_review_packet_current702_20260601.json"
            )
        )

        self.assertEqual(
            packet["status"],
            "source_free_active_site_locator_manual_review_packet_ready_review_only",
        )
        self.assertEqual(packet["counts"]["review_rows"], 10)
        self.assertEqual(packet["counts"]["integrity_passed_rows"], 10)
        self.assertEqual(
            packet["counts"]["priority_1_manual_forbidden_feature_review_rows"],
            3,
        )
        self.assertEqual(packet["counts"]["copy_to_audited_locator_dir_allowed_now"], 0)
        self.assertEqual(packet["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertFalse(packet["guardrails"]["locator_sidecars_created_in_audited_dir"])
        self.assertFalse(packet["guardrails"]["predicted_geometry_scored"])
        self.assertEqual(packet["review_rows"][0]["entry_id"], "mh_066")
        self.assertEqual(packet["review_rows"][0]["integrity_status"], "passed")
        self.assertFalse(
            packet["review_rows"][0]["copy_to_audited_locator_dir_allowed_now"]
        )

    def test_family_panel_source_free_active_site_locator_review_queue_counts(
        self,
    ) -> None:
        queue = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_active_site_locator_review_queue_"
                "current702_20260601.json"
            )
        )

        self.assertEqual(
            queue["status"],
            "source_free_active_site_locator_review_queue_ready_review_only",
        )
        self.assertEqual(queue["counts"]["queue_rows"], 10)
        self.assertEqual(queue["counts"]["ready_for_manual_forbidden_feature_review"], 3)
        self.assertEqual(queue["counts"]["needs_ligand_specificity_review"], 1)
        self.assertEqual(queue["counts"]["needs_split_safe_template_check"], 2)
        self.assertEqual(queue["counts"]["needs_uniprot_position_validation"], 2)
        self.assertEqual(
            queue["counts"]["blocked_needs_new_coordinate_or_nonlabel_locator"],
            2,
        )
        self.assertFalse(queue["guardrails"]["locator_sidecars_created_in_audited_dir"])
        self.assertFalse(queue["guardrails"]["predicted_geometry_scored"])
        self.assertEqual(
            [row["entry_id"] for row in queue["queue_rows"][:3]],
            ["mh_066", "mh_073", "secondary_probe::radical_sam_enzyme"],
        )
        self.assertEqual(
            queue["queue_rows"][0]["review_class"],
            "ready_for_manual_forbidden_feature_review",
        )

    def test_family_panel_source_free_active_site_locator_priority1_review_preflight_counts(
        self,
    ) -> None:
        preflight = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_active_site_locator_"
                "priority1_review_preflight_current702_20260601.json"
            )
        )

        self.assertEqual(
            preflight["status"],
            "source_free_active_site_locator_priority1_preflight_passed_pending_human_approval",
        )
        self.assertEqual(preflight["counts"]["priority_1_rows"], 3)
        self.assertEqual(
            preflight["counts"]["preflight_passed_pending_human_approval"], 3
        )
        self.assertEqual(preflight["counts"]["schema_dry_run_passed_rows"], 3)
        self.assertEqual(preflight["counts"]["guardrail_preflight_passed_rows"], 3)
        self.assertEqual(
            preflight["counts"]["scientific_preflight_supported_rows"], 3
        )
        self.assertEqual(preflight["counts"]["copy_to_audited_locator_dir_allowed_now"], 0)
        self.assertEqual(preflight["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertFalse(preflight["guardrails"]["locator_sidecars_created_in_audited_dir"])
        self.assertFalse(preflight["guardrails"]["predicted_geometry_scored"])
        self.assertTrue(preflight["guardrails"]["human_approval_required_before_copy"])
        self.assertEqual(
            [row["entry_id"] for row in preflight["preflight_rows"]],
            ["mh_066", "mh_073", "secondary_probe::radical_sam_enzyme"],
        )
        self.assertTrue(
            all(row["schema_dry_run_passed"] for row in preflight["preflight_rows"])
        )
        self.assertTrue(
            all(row["guardrail_preflight_passed"] for row in preflight["preflight_rows"])
        )
        self.assertEqual(
            preflight["preflight_rows"][1]["scientific_preflight"]["warnings"],
            ["minimum_two_locator_floor_only"],
        )

    def test_family_panel_source_free_locator_blocked_row_rescue_manifest_counts(
        self,
    ) -> None:
        manifest = _load_json(
            ROOT
            / "artifacts"
            / (
                "v3_family_panel_source_free_locator_blocked_row_"
                "rescue_manifest_current702_20260601.json"
            )
        )

        self.assertEqual(
            manifest["status"],
            "source_free_locator_blocked_row_rescue_manifest_ready_review_only",
        )
        self.assertEqual(manifest["counts"]["blocked_rows"], 2)
        self.assertEqual(
            manifest["counts"]["rows_with_selected_coordinate_only_water_hetatms"],
            2,
        )
        self.assertEqual(manifest["counts"]["rows_with_alternate_source_pdb_ids"], 1)
        self.assertEqual(manifest["counts"]["alternate_pdb_ids_total"], 5)
        self.assertEqual(manifest["counts"]["alternate_fetch_commands"], 5)
        self.assertEqual(manifest["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertFalse(manifest["guardrails"]["coordinates_fetched"])
        self.assertFalse(manifest["guardrails"]["locator_sidecars_created_in_audited_dir"])
        by_entry = {row["entry_id"]: row for row in manifest["row_plans"]}
        self.assertEqual(
            by_entry["mh_064"]["alternate_pdb_ids"],
            ["3RKJ", "3RKK", "3SBL", "3SFP", "3SPU"],
        )
        self.assertEqual(
            by_entry["secondary_probe::cobalamin_radical_rearrangement"][
                "alternate_pdb_ids"
            ],
            [],
        )
        self.assertEqual(
            by_entry["secondary_probe::cobalamin_radical_rearrangement"][
                "rescue_status"
            ],
            "no_frozen_source_alternate_pdb_ids_found",
        )

    def test_fmo_subtype_hard_negative_packet_current_counts(self) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / "v3_fmo_subtype_hard_negative_packet_current702_20260601.json"
        )

        self.assertEqual(
            packet["status"],
            "fmo_subtype_hard_negative_packet_ready_review_only",
        )
        self.assertEqual(packet["counts"]["rows"], 5)
        self.assertEqual(packet["counts"]["current_primary_fmo_rows"], 0)
        self.assertEqual(packet["counts"]["secondary_or_future_support_rows"], 4)
        self.assertEqual(packet["counts"]["hard_negative_or_boundary_rows"], 1)
        self.assertEqual(packet["counts"]["geometry_or_coordinate_blocked_rows"], 1)
        self.assertEqual(packet["counts"]["import_ready_rows"], 0)
        self.assertEqual(packet["counts"]["registry_edit_allowed_rows"], 0)
        by_entry = {row["entry_id"]: row for row in packet["panel_rows"]}
        self.assertEqual(
            by_entry["m_csa:973"]["fold_augmented_readout"]["research_gate_status"],
            "abstained_at_research_threshold",
        )
        self.assertEqual(
            by_entry["m_csa:132"]["decision"],
            "keep_as_secondary_fmo_support_after_geometry_repair_no_primary_promotion",
        )
        self.assertEqual(
            by_entry["m_csa:750"]["hard_negative_role"],
            "radical_flavin_fe_s_boundary",
        )
        self.assertTrue(packet["guardrails"]["review_only"])
        self.assertFalse(packet["guardrails"]["imports_or_promotions_performed"])


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
