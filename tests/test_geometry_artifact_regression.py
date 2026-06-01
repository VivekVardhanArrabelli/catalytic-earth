from __future__ import annotations

import csv
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
            "coordinate_bundle_not_persisted_results_parseable",
        )
        self.assertEqual(audit["counts"]["total_coordinate_requests"], 299)
        self.assertEqual(audit["counts"]["unique_coordinate_files_expected"], 299)
        self.assertEqual(audit["counts"]["unique_coordinate_files_observed"], 0)
        self.assertEqual(audit["counts"]["unique_coordinate_files_missing"], 299)
        self.assertEqual(audit["counts"]["unique_accessions_expected"], 293)
        self.assertEqual(
            audit["counts"]["unique_accessions_without_any_local_file"],
            293,
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
            "fold_channel_reproduction_manifest_ready_missing_coordinates",
        )
        self.assertEqual(manifest["counts"]["heldout_rows_ok"], 126)
        self.assertEqual(
            manifest["counts"]["priority_cofactor_confounded_oos_rows"],
            6,
        )
        self.assertEqual(manifest["counts"]["total_coordinate_requests"], 299)
        self.assertEqual(manifest["counts"]["unique_coordinate_files_expected"], 299)
        self.assertEqual(manifest["counts"]["unique_coordinate_files_observed"], 0)
        self.assertEqual(manifest["counts"]["unique_coordinate_files_missing"], 299)
        self.assertEqual(manifest["counts"]["unique_accessions_expected"], 293)
        self.assertEqual(
            manifest["counts"]["unique_accessions_without_any_local_file"],
            293,
        )
        self.assertEqual(manifest["counts"]["duplicate_accession_requests"], 6)
        self.assertEqual(manifest["counts"]["foldseek_result_files"], 2)
        self.assertTrue(manifest["counts"]["result_files_parseable"])
        self.assertTrue(manifest["counts"]["foldseek_runtime_available"])
        self.assertFalse(manifest["counts"]["byte_reproduction_ready"])
        self.assertEqual(
            manifest["blocker_classes"],
            ["persistent_afdb_v6_coordinate_bundle_missing"],
        )
        self.assertEqual(
            manifest["scored_channel_contract"]["critical_violation_total"],
            0,
        )
        self.assertFalse(manifest["guardrails"]["coordinate_downloads_performed"])
        self.assertFalse(manifest["guardrails"]["foldseek_or_tmsearch_recomputed"])

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
        self.assertEqual(matrix["counts"]["blocked_rows_tracked"], 7)
        self.assertEqual(matrix["counts"]["decision_classes"], 5)
        self.assertEqual(matrix["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertEqual(
            matrix["recommended_decision_order"][0],
            "human_locator_copy_approval_after_split_safe_pass",
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
            "p0_source_evidence_sidecar_draft_review_required",
        )
        self.assertEqual(sidecar["counts"]["worksheet_rows"], 15)
        self.assertEqual(sidecar["counts"]["sidecar_rows"], 15)
        self.assertEqual(sidecar["counts"]["rows_with_source_spans"], 15)
        self.assertEqual(sidecar["counts"]["rows_with_draft_bond_change_events"], 15)
        self.assertEqual(sidecar["counts"]["rows_with_rhea_equations"], 11)
        self.assertEqual(sidecar["counts"]["rows_missing_rhea_equations"], 4)
        self.assertEqual(sidecar["counts"]["approved_rows"], 0)
        self.assertEqual(sidecar["counts"]["feature_contract_consumable_rows"], 0)
        self.assertEqual(sidecar["counts"]["review_status_counts"], {"draft": 15})
        self.assertFalse(sidecar["guardrails"]["feature_contract_mutated"])
        self.assertFalse(sidecar["guardrails"]["feature_contract_refresh_allowed"])
        self.assertTrue(sidecar["guardrails"]["draft_source_evidence_not_training_input"])

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
            "p0_source_evidence_sidecar_strict_audit_passed_draft_not_consumable",
        )
        self.assertEqual(audit["counts"]["worksheet_rows"], 15)
        self.assertEqual(audit["counts"]["sidecar_rows"], 15)
        self.assertEqual(audit["counts"]["draft_rows"], 15)
        self.assertEqual(audit["counts"]["approved_rows"], 0)
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
                "high_complexity_multi_event_review": 4,
                "rhea_lookup_required_before_approval": 4,
                "standard_draft_event_review": 7,
            },
        )
        self.assertEqual(queue["counts"]["approved_rows"], 0)
        self.assertEqual(queue["counts"]["feature_contract_consumable_rows"], 0)
        self.assertEqual(queue["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            [row["entry_id"] for row in queue["queue_rows"][:4]],
            ["m_csa:124", "m_csa:11", "m_csa:169", "m_csa:5"],
        )
        self.assertTrue(
            all(count == 0 for count in queue["counts"]["critical_counts"].values())
        )
        self.assertFalse(queue["guardrails"]["feature_contract_mutated"])
        self.assertFalse(queue["guardrails"]["feature_contract_refresh_allowed"])

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
        self.assertEqual(manifest["counts"]["rhea_lookup_rows"], 4)
        self.assertEqual(manifest["counts"]["rows_with_ec_targets"], 4)
        self.assertEqual(manifest["counts"]["lookup_target_count"], 4)
        self.assertEqual(manifest["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            [row["entry_id"] for row in manifest["lookup_rows"]],
            ["m_csa:124", "m_csa:11", "m_csa:169", "m_csa:5"],
        )
        self.assertEqual(
            [row["ec_targets"][0] for row in manifest["lookup_rows"]],
            ["ec:1.9.3.1", "ec:3.1.21.2", "ec:3.4.14.5", "ec:3.4.16.6"],
        )
        self.assertTrue(
            all(count == 0 for count in manifest["counts"]["critical_counts"].values())
        )
        self.assertFalse(manifest["guardrails"]["source_fetch_performed"])
        self.assertFalse(manifest["guardrails"]["feature_contract_refresh_allowed"])

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
        self.assertEqual(audit["counts"]["json_artifacts_checked"], 16)
        self.assertEqual(audit["counts"]["json_artifacts_parse_passed"], 16)
        self.assertEqual(audit["counts"]["work_reports_checked"], 16)
        self.assertEqual(audit["counts"]["work_reports_present"], 16)
        self.assertEqual(audit["counts"]["repo_json_artifacts_parse_checked"], 3123)
        self.assertEqual(audit["counts"]["repo_jsonl_artifacts_parse_checked"], 25)
        self.assertEqual(audit["counts"]["repo_json_parse_error_count"], 0)
        self.assertEqual(audit["counts"]["label_registry_mutations"], 0)
        self.assertEqual(audit["counts"]["new_coordinates_fetched"], 0)
        self.assertEqual(audit["counts"]["predicted_geometry_scores_created"], 0)
        self.assertFalse(audit["guardrails"]["labels_registries_ontologies_changed"])
        self.assertFalse(audit["guardrails"]["production_thresholds_changed"])
        self.assertFalse(audit["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(audit["guardrails"]["model_weights_fit_or_refit"])
        self.assertTrue(
            all(count == 0 for count in audit["critical_counts"].values())
        )
        self.assertEqual(len(audit["artifact_rows"]), 16)
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
        self.assertEqual(readout["counts"]["primary_score_complete_rows"], 15)
        self.assertEqual(readout["counts"]["non_abstained_at_research_threshold"], 9)
        self.assertEqual(readout["counts"]["abstained_at_research_threshold"], 6)
        self.assertEqual(readout["counts"]["not_score_complete_for_primary_channel"], 7)
        self.assertEqual(
            [row["entry_id"] for row in readout["review_priority_rows"]],
            [
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
            "family_panel_source_free_predicted_geometry_retrieval",
        )
        self.assertEqual(
            by_entry["secondary_probe::radical_sam_enzyme"][
                "research_gate_status"
            ],
            "non_abstained_at_research_threshold",
        )
        self.assertTrue(readout["guardrails"]["review_only"])
        self.assertFalse(readout["guardrails"]["thresholds_selected_on_family_panel_rows"])

    def test_fold_augmented_family_panel_source_check_queue_current_counts(self) -> None:
        queue = _load_json(
            ROOT
            / "artifacts"
            / "v3_fold_augmented_family_panel_source_check_queue_current702_20260601.json"
        )

        self.assertEqual(queue["status"], "source_check_queue_ready_review_only")
        self.assertEqual(queue["counts"]["source_check_rows"], 9)
        self.assertEqual(queue["counts"]["panels_represented"], 5)
        self.assertEqual(
            queue["counts"]["source_check_rows_by_panel"],
            {
                "cobalamin_and_radical_rearrangement_panel": 2,
                "flavin_monooxygenase_and_flavin_oxygen_transfer": 3,
                "lipoamide_or_sulfur_transfer_redox_boundary": 1,
                "near_orphan_glycoside_or_nucleoside_hydrolase_controls": 2,
                "no_reliable_structure_metal_hydrolase_controls": 1,
            },
        )
        self.assertEqual(
            [row["entry_id"] for row in queue["queue_rows"]],
            [
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
        self.assertEqual(queue["counts"]["missing_primary_channel_rows"], 7)
        self.assertEqual(queue["counts"]["m_csa_rows"], 0)
        self.assertEqual(queue["counts"]["secondary_probe_rows"], 1)
        self.assertEqual(queue["counts"]["external_or_placeholder_rows"], 6)
        self.assertEqual(
            queue["counts"]["score_blocker_counts"],
            {
                "predicted_geometry_top1_score_missing": 7,
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
        self.assertEqual(diagnosis["counts"]["diagnosed_rows"], 7)
        self.assertEqual(
            diagnosis["counts"]["diagnosis_counts"],
            {
                "source_backed_fold_scored_needs_predicted_geometry": 7,
            },
        )
        self.assertEqual(diagnosis["counts"]["rows_with_source_backed_fold_score"], 7)
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
            3,
        )
        self.assertEqual(manifest["counts"]["source_free_geometry_ready_rows"], 3)
        self.assertEqual(manifest["counts"]["source_free_geometry_blocked_rows"], 7)
        self.assertEqual(
            manifest["counts"]["blocker_counts"],
            {
                "approved_source_free_active_site_locator_missing": 7,
                "source_backed_sidecar_lacks_residue_locator": 7,
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
        self.assertEqual(retrieval["counts"]["manifest_ready_to_score_rows"], 3)
        self.assertEqual(retrieval["counts"]["predicted_geometry_ok_rows"], 3)
        self.assertEqual(retrieval["counts"]["runtime_blocked_ready_rows"], 0)
        self.assertEqual(retrieval["counts"]["precondition_blocked_rows_carried"], 7)
        self.assertEqual(retrieval["counts"]["retained_at_fixed_research_threshold"], 3)
        by_entry = {row["entry_id"]: row for row in retrieval["row_scores"]}
        self.assertEqual(
            set(by_entry),
            {"mh_066", "mh_073", "secondary_probe::radical_sam_enzyme"},
        )
        self.assertEqual(
            by_entry["mh_066"]["predicted_geometry_retrieval"]["top1_fingerprint_id"],
            "metal_dependent_hydrolase",
        )
        self.assertEqual(
            by_entry["mh_073"]["predicted_geometry_retrieval"]["top1_fingerprint_id"],
            "ser_his_acid_hydrolase",
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
        self.assertEqual(status["counts"]["blocked_rows_tracked"], 7)
        self.assertEqual(status["counts"]["automation_discovery_completed_rows"], 7)
        self.assertEqual(status["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertEqual(status["counts"]["locator_sidecars_created_or_copied"], 0)
        self.assertEqual(
            status["counts"]["resolution_class_counts"],
            {
                "accession_equivalence_or_matching_coordinate_required": 2,
                "alternate_coordinate_fetch_approval_required": 1,
                "human_locator_copy_approval_after_split_safe_pass": 2,
                "ligand_specificity_validator_or_substrate_coordinate_required": 1,
                "nonlabel_locator_strategy_or_alternate_source_required": 1,
            },
        )
        self.assertFalse(
            status["guardrails"]["approved_locator_sidecars_created_or_copied"]
        )
        self.assertFalse(status["guardrails"]["new_coordinates_fetched"])
        self.assertFalse(status["guardrails"]["predicted_geometry_scored"])

        by_entry = {row["entry_id"]: row for row in status["resolution_rows"]}
        self.assertEqual(by_entry["mh_065"]["resolution_status"], "blocked_accession_mismatch")
        self.assertEqual(
            by_entry["mh_067"]["resolution_status"],
            "split_safe_passed_copy_not_authorized",
        )
        self.assertEqual(
            by_entry["external_glycoside_panel"]["resolution_status"],
            "selected_acetate_locator_rejected",
        )
        self.assertEqual(
            by_entry["secondary_probe::cobalamin_radical_rearrangement"][
                "resolution_status"
            ],
            "blocked_no_ligand_no_alternate_pdb",
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
        self.assertEqual(audit["counts"]["locator_sidecars_present"], 3)
        self.assertEqual(audit["counts"]["locator_sidecars_missing"], 7)
        self.assertEqual(audit["counts"]["ready_for_predicted_geometry_scoring"], 3)
        self.assertEqual(
            audit["counts"]["critical_counts"],
            {"locator_sidecar_missing": 7},
        )
        self.assertFalse(audit["guardrails"]["predicted_geometry_scored"])
        by_entry = {row["entry_id"]: row for row in audit["row_audits"]}
        self.assertEqual(by_entry["mh_066"]["status"], "passed")
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

    def test_family_panel_source_free_active_site_locator_audited_dir_after_approval(
        self,
    ) -> None:
        locator_dir = (
            ROOT
            / "artifacts"
            / "family_panel_source_free_active_site_locators_current702_20260601"
        )

        self.assertEqual(
            sorted(path.name for path in locator_dir.glob("*.json")),
            [
                "mh_066_P52699.json",
                "mh_073_P01112.json",
                "secondary_probe_radical_sam_enzyme_A0A1M6T2I7.json",
            ],
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
