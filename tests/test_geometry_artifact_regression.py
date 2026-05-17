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

        self.assertEqual(summary["label_count"], 679)
        self.assertEqual(summary["by_type"]["seed_fingerprint"], 212)
        self.assertEqual(summary["by_type"]["out_of_scope"], 467)
        self.assertEqual(
            summary["by_ontology_version_at_decision"],
            {"label_factory_v1_8fp": 679},
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

        self.assertEqual(label_summary["by_tier"], {"bronze": 679})
        self.assertEqual(label_summary["by_review_status"], {"automation_curated": 679})
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


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
