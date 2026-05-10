from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class GeometryArtifactRegressionTests(unittest.TestCase):
    def test_label_summary_artifact_matches_curated_registry(self) -> None:
        summary = _load_json(ROOT / "artifacts" / "v3_label_summary.json")

        self.assertEqual(summary["label_count"], 618)
        self.assertEqual(summary["by_type"]["seed_fingerprint"], 151)
        self.assertEqual(summary["by_type"]["out_of_scope"], 467)

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

        self.assertEqual(label_summary["by_tier"], {"bronze": 618})
        self.assertEqual(label_summary["by_review_status"], {"automation_curated": 618})
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

    def test_525_through_650_batch_acceptance_are_gated(self) -> None:
        acceptance = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_525.json")
        acceptance_550 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_550.json")
        acceptance_575 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_575.json")
        acceptance_600 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_600.json")
        acceptance_625 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_625.json")
        acceptance_650 = _load_json(ROOT / "artifacts" / "v3_label_batch_acceptance_check_650.json")
        acceptance_675_preview = _load_json(
            ROOT / "artifacts" / "v3_label_batch_acceptance_check_675_preview.json"
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
        self.assertEqual(preview_summary_675["metadata"]["blocker_count"], 0)
        self.assertTrue(preview_summary_675["metadata"]["all_active_queues_retain_unlabeled_candidates"])
        self.assertEqual(preview_summary_675["metadata"]["scaling_quality_audit_count"], 1)
        self.assertTrue(preview_summary_675["metadata"]["latest_scaling_quality_audit_present"])
        self.assertTrue(preview_summary_675["metadata"]["all_supplied_scaling_quality_audits_ready"])
        self.assertEqual(
            preview_summary_675["metadata"]["latest_scaling_quality_recommendation"],
            "review_before_promoting",
        )
        self.assertIn(
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
            "not_assessed_no_sequence_cluster_artifact",
        )
        self.assertIn(
            "sequence_cluster_artifact_missing_for_near_duplicate_audit",
            scaling_quality_675["review_warnings"],
        )
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
        self.assertEqual(gate_550["blockers"], [])
        self.assertEqual(gate_575["blockers"], [])
        self.assertEqual(gate_600["blockers"], [])
        self.assertEqual(gate_625["blockers"], [])
        self.assertEqual(gate_650["blockers"], [])


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
