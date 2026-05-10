from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class GeometryArtifactRegressionTests(unittest.TestCase):
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

        self.assertEqual(evaluation["metadata"]["in_scope_count"], 44)
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

        self.assertEqual(evaluation["metadata"]["in_scope_count"], 59)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9831)
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
        self.assertEqual(seed_family["metadata"]["largest_in_scope_family_count"], 28)

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

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 450)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 65)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 135)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9846)
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

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 450)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 71)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 153)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9859)
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

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 450)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 78)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 171)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9872)
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

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 450)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 81)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 193)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9877)
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

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 450)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 98)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 276)
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

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 450)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 106)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 293)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.981)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 3)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(label_candidates["metadata"]["candidate_count"], 0)
        self.assertEqual(label_candidates["metadata"]["labeled_entry_count"], 450)

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

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 450)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 117)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 307)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9828)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 3)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["evidence_limited_abstention_count"], 3)
        self.assertEqual(label_candidates["metadata"]["candidate_count"], 0)
        self.assertEqual(label_candidates["metadata"]["labeled_entry_count"], 450)
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

        self.assertEqual(evaluation["metadata"]["label_summary"]["label_count"], 450)
        self.assertEqual(evaluation["metadata"]["in_scope_count"], 124)
        self.assertEqual(evaluation["metadata"]["out_of_scope_count"], 325)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions_evaluable"], 0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate_evaluable"], 0.9756)
        self.assertEqual(hard_negatives["metadata"]["hard_negative_count"], 0)
        self.assertEqual(hard_negatives["metadata"]["near_miss_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["failure_count"], 4)
        self.assertEqual(in_scope_failures["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(in_scope_failures["metadata"]["evidence_limited_abstention_count"], 4)
        self.assertEqual(label_candidates["metadata"]["candidate_count"], 0)
        self.assertEqual(label_candidates["metadata"]["labeled_entry_count"], 450)
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


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
