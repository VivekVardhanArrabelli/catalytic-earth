from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Scaling1025ArtifactTests(unittest.TestCase):
    def test_1025_preview_is_clean_but_not_promotable(self) -> None:
        gate = _load_json(ROOT / "artifacts" / "v3_label_factory_gate_check_1025_preview.json")
        acceptance = _load_json(
            ROOT / "artifacts" / "v3_label_batch_acceptance_check_1025_preview.json"
        )
        scaling_quality = _load_json(
            ROOT / "artifacts" / "v3_label_scaling_quality_audit_1025_preview.json"
        )
        review_debt = _load_json(
            ROOT / "artifacts" / "v3_review_debt_summary_1025_preview.json"
        )
        deferral = _load_json(
            ROOT
            / "artifacts"
            / "v3_accepted_review_debt_deferral_audit_1025_preview.json"
        )

        self.assertTrue(gate["metadata"]["automation_ready_for_next_label_batch"])
        self.assertEqual(gate["blockers"], [])
        self.assertFalse(acceptance["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance["metadata"]["accepted_new_label_count"], 0)
        self.assertEqual(acceptance["metadata"]["countable_label_count"], 679)
        self.assertEqual(acceptance["metadata"]["pending_review_count"], 329)
        self.assertEqual(acceptance["metadata"]["hard_negative_count"], 0)
        self.assertEqual(acceptance["metadata"]["near_miss_count"], 0)
        self.assertEqual(
            acceptance["metadata"]["out_of_scope_false_non_abstentions"], 0
        )
        self.assertEqual(
            acceptance["metadata"]["actionable_in_scope_failure_count"], 0
        )
        self.assertEqual(acceptance["metadata"]["accepted_review_gap_count"], 0)
        self.assertEqual(acceptance["blockers"], ["accepted_labels_added"])
        self.assertEqual(
            scaling_quality["metadata"]["audit_recommendation"], "do_not_promote"
        )
        self.assertEqual(scaling_quality["blockers"], [])
        self.assertEqual(review_debt["metadata"]["new_review_debt_count"], 3)
        self.assertEqual(
            review_debt["metadata"]["new_review_debt_entry_ids"],
            ["m_csa:1003", "m_csa:1004", "m_csa:1005"],
        )
        self.assertEqual(deferral["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(deferral["metadata"]["accepted_review_debt_overlap_count"], 0)

    def test_source_limit_and_transfer_manifests_block_m_csa_only_scaling(self) -> None:
        source_limit = _load_json(
            ROOT / "artifacts" / "v3_source_scale_limit_audit_1025.json"
        )
        transfer = _load_json(
            ROOT / "artifacts" / "v3_external_source_transfer_manifest_1025.json"
        )
        queries = _load_json(
            ROOT / "artifacts" / "v3_external_source_query_manifest_1025.json"
        )
        ood_plan = _load_json(
            ROOT / "artifacts" / "v3_external_ood_calibration_plan_1025.json"
        )
        sample = _load_json(
            ROOT / "artifacts" / "v3_external_source_candidate_sample_1025.json"
        )
        sample_audit = _load_json(
            ROOT / "artifacts" / "v3_external_source_candidate_sample_audit_1025.json"
        )

        self.assertTrue(source_limit["metadata"]["source_limit_reached"])
        self.assertEqual(source_limit["metadata"]["observed_source_entries"], 1003)
        self.assertEqual(source_limit["metadata"]["source_entry_gap"], 22)
        self.assertEqual(source_limit["metadata"]["countable_label_count"], 679)
        self.assertEqual(
            source_limit["metadata"]["recommendation"],
            "stop_m_csa_only_tranche_growth_and_scope_external_source_transfer",
        )
        self.assertFalse(transfer["metadata"]["ready_for_label_import"])
        self.assertEqual(transfer["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            transfer["metadata"]["manifest_recommendation"],
            "prototype_external_source_transfer_before_next_count_growth",
        )
        self.assertFalse(queries["metadata"]["ready_for_label_import"])
        self.assertEqual(queries["metadata"]["countable_label_candidate_count"], 0)
        self.assertGreaterEqual(queries["metadata"]["lane_count"], 5)
        self.assertFalse(ood_plan["metadata"]["ready_for_label_import"])
        self.assertEqual(ood_plan["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            ood_plan["metadata"]["lane_count"], queries["metadata"]["lane_count"]
        )
        self.assertFalse(sample["metadata"]["ready_for_label_import"])
        self.assertEqual(sample["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(sample["metadata"]["fetch_failure_count"], 0)
        self.assertGreater(sample["metadata"]["candidate_count"], 0)
        self.assertTrue(sample_audit["metadata"]["guardrail_clean"])
        self.assertEqual(sample_audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(sample_audit["blockers"], [])


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
