from __future__ import annotations

import json
import unittest
from pathlib import Path

from catalytic_earth.labels import load_labels
from catalytic_earth.transfer_scope import (
    EXTERNAL_HARD_NEGATIVE_ABSTAIN_THRESHOLD,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_VERSION,
    EXTERNAL_HARD_NEGATIVE_THRESHOLD_POLICY_VERSION,
    build_external_hard_negative_next_candidate_factory_import_gate,
)


ROOT = Path(__file__).resolve().parents[1]
PILOT_REPAIR_CANDIDATES = {
    "O14756",
    "Q6NSJ0",
    "P34949",
    "Q9BXD5",
    "C9JRZ8",
    "P06746",
    "P55263",
    "O60568",
    "O95050",
    "P51580",
}
EXTERNAL_HARD_NEGATIVES = {
    "uniprot:P06744",
    "uniprot:P78549",
    "uniprot:Q3LXA3",
}
FORBIDDEN_PREDICTIVE_CONTEXT = (
    "protein_name",
    "ec_label",
    "uniprot_prose",
    "source_annotation",
    "curated_mechanism_text",
)


class LeakageClosureTests(unittest.TestCase):
    def test_pilot_repair_lanes_are_not_clean_performance_evidence(self) -> None:
        artifact = _load_json(
            ROOT / "artifacts" / "v3_external_pilot_repair_leakage_closure_1025.json"
        )

        self.assertEqual(set(artifact["candidates"]), PILOT_REPAIR_CANDIDATES)
        self.assertEqual(
            artifact["metadata"]["clean_performance_evidence_candidate_count"], 0
        )
        self.assertEqual(
            artifact["decision"]["classification"],
            "development_review_evidence_not_clean_performance_evidence",
        )
        self.assertTrue(
            artifact["metadata"][
                "rules_frozen_before_future_candidate_selection_required"
            ]
        )

    def test_next_tranche_pre_registration_is_frozen_before_selection(self) -> None:
        artifact = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_hard_negative_next_tranche_preregistration_1025.json"
        )
        metadata = artifact["metadata"]
        fingerprints = _load_json(
            ROOT / "data" / "registries" / "mechanism_fingerprints.json"
        )
        expected_fingerprints = sorted(row["id"] for row in fingerprints)

        self.assertEqual(
            metadata["version"],
            EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_VERSION,
        )
        self.assertEqual(
            metadata["registration_status"], "frozen_before_candidate_selection"
        )
        self.assertFalse(metadata["candidate_selection_started"])
        self.assertEqual(
            sorted(metadata["fingerprint_universe"]), expected_fingerprints
        )
        self.assertEqual(
            metadata["ontology_version_at_decision"], "label_factory_v1_8fp"
        )
        self.assertEqual(
            metadata["threshold_policy_version"],
            EXTERNAL_HARD_NEGATIVE_THRESHOLD_POLICY_VERSION,
        )
        self.assertEqual(
            metadata["abstain_threshold"], EXTERNAL_HARD_NEGATIVE_ABSTAIN_THRESHOLD
        )
        self.assertEqual(
            metadata["inverse_gate_rule"], "all_current_fingerprints_below_floor"
        )
        self.assertIn("excluded_context", artifact["frozen_rules"])

    def test_factory_import_gate_blocks_next_tranche_without_preregistration(self) -> None:
        gate = build_external_hard_negative_next_candidate_factory_import_gate(
            terminal_review_decisions=_terminal_review_decisions(),
            label_factory_gate_check=_passed_label_factory_gate(),
            external_transfer_gate=_passed_external_transfer_gate(),
            existing_label_entry_ids=[],
            max_imports=1,
            require_pre_registration=True,
        )

        self.assertFalse(gate["metadata"]["ready_for_label_import"])
        self.assertEqual(gate["metadata"]["selected_import_accessions"], [])
        self.assertIn(
            "external_hard_negative_pre_registration_missing",
            gate["rows"][0]["remaining_import_blockers"],
        )

    def test_factory_import_gate_accepts_frozen_preregistration(self) -> None:
        prereg = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_hard_negative_next_tranche_preregistration_1025.json"
        )
        gate = build_external_hard_negative_next_candidate_factory_import_gate(
            terminal_review_decisions=_terminal_review_decisions(),
            label_factory_gate_check=_passed_label_factory_gate(),
            external_transfer_gate=_passed_external_transfer_gate(),
            existing_label_entry_ids=[],
            max_imports=1,
            pre_registration=prereg,
            pre_registration_artifact_path=(
                "artifacts/v3_external_hard_negative_next_tranche_preregistration_1025.json"
            ),
            require_pre_registration=True,
        )

        self.assertTrue(gate["metadata"]["ready_for_label_import"])
        self.assertEqual(gate["metadata"]["selected_import_accessions"], ["PTEST"])
        self.assertEqual(
            gate["metadata"]["pre_registration_reference"]["version"],
            EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_VERSION,
        )
        self.assertEqual(gate["rows"][0]["remaining_import_blockers"], [])
        separation = gate["rows"][0]["evidence_separation"]
        self.assertIn("predictive_evidence", separation)
        self.assertIn("import_gate_evidence", separation)
        self.assertIn("review_only_context", separation)
        self.assertIn("excluded_context", separation)

    def test_threshold_policy_pins_external_import_floor(self) -> None:
        policy = _load_json(
            ROOT / "artifacts" / "v3_external_hard_negative_threshold_policy_1025.json"
        )
        self.assertEqual(
            policy["metadata"]["version"],
            EXTERNAL_HARD_NEGATIVE_THRESHOLD_POLICY_VERSION,
        )
        self.assertEqual(
            policy["metadata"]["abstain_threshold"],
            EXTERNAL_HARD_NEGATIVE_ABSTAIN_THRESHOLD,
        )
        self.assertFalse(policy["metadata"]["candidate_or_tranche_tuning_permitted"])

        for path in (
            "artifacts/v3_external_hard_negative_next_candidate_factory_import_gate_1025.json",
            "artifacts/v3_external_hard_negative_q3lxa3_single_import_cycle_gate_1025.json",
            "artifacts/v3_external_hard_negative_broader_structural_factory_import_gate_1025.json",
        ):
            artifact = _load_json(ROOT / path)
            for row in artifact["rows"]:
                if row.get("ready_for_label_import"):
                    inverse_gate = row["out_of_scope_inverse_gate"]
                    self.assertEqual(
                        inverse_gate["abstain_threshold"],
                        EXTERNAL_HARD_NEGATIVE_ABSTAIN_THRESHOLD,
                    )
                    self.assertEqual(
                        inverse_gate["ontology_version_at_decision"],
                        "label_factory_v1_8fp",
                    )

    def test_external_label_evidence_separates_review_context(self) -> None:
        labels = {label.entry_id: label for label in load_labels()}
        self.assertEqual(
            set(entry for entry in labels if entry.startswith("uniprot:")),
            EXTERNAL_HARD_NEGATIVES,
        )

        for entry_id in EXTERNAL_HARD_NEGATIVES:
            evidence = labels[entry_id].evidence
            for key in (
                "predictive_evidence",
                "import_gate_evidence",
                "review_only_context",
                "excluded_context",
            ):
                self.assertIsInstance(evidence[key], list)
                self.assertTrue(evidence[key])
            predictive_blob = json.dumps(evidence["predictive_evidence"]).lower()
            for term in FORBIDDEN_PREDICTIVE_CONTEXT:
                self.assertNotIn(term, predictive_blob)

    def test_ontology_reaudit_policy_lists_external_hard_negatives(self) -> None:
        artifact = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_hard_negative_ontology_reaudit_policy_1025.json"
        )
        self.assertTrue(
            artifact["metadata"]["re_audit_required_on_positive_fingerprint_expansion"]
        )
        self.assertEqual(
            {row["entry_id"] for row in artifact["external_labels_requiring_reaudit"]},
            EXTERNAL_HARD_NEGATIVES,
        )
        for trigger in ("epk", "sdr", "akr", "glycoside_hydrolase", "isomerase", "lyase"):
            self.assertIn(trigger, artifact["expansion_triggers"])

    def test_epk_readiness_packet_stays_review_only(self) -> None:
        packet = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_positive_fingerprint_readiness_packet_1025.json"
        )
        metadata = packet["metadata"]
        self.assertEqual(metadata["method"], "epk_positive_fingerprint_readiness_packet")
        self.assertTrue(metadata["evidence_ready_for_draft_fingerprint_spec"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["current_positive_fingerprint_count"], 8)
        self.assertEqual(metadata["epk_boundary_row_count"], 5)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            set(metadata["external_hard_negative_reaudit_entry_ids"]),
            EXTERNAL_HARD_NEGATIVES,
        )
        self.assertEqual(
            {row["entry_id"] for row in packet["rows"]},
            {"m_csa:35", "m_csa:246", "m_csa:282", "m_csa:640", "m_csa:662"},
        )
        for row in packet["rows"]:
            self.assertTrue(row["review_only"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertIn(
                "positive_fingerprint_registry_not_expanded",
                row["readiness_blockers"],
            )

    def test_epk_external_hard_negative_reaudit_plan_is_unscored(self) -> None:
        plan = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_hard_negative_reaudit_plan_1025.json"
        )
        metadata = plan["metadata"]
        self.assertEqual(metadata["method"], "epk_external_hard_negative_reaudit_plan")
        self.assertTrue(metadata["reaudit_plan_ready"])
        self.assertFalse(metadata["ready_to_run_scored_reaudit"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertEqual(metadata["external_label_reaudit_row_count"], 3)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(set(row["entry_id"] for row in plan["rows"]), EXTERNAL_HARD_NEGATIVES)
        for row in plan["rows"]:
            self.assertEqual(row["reaudit_status"], "planned_not_scored")
            self.assertTrue(row["current_label_contract_valid"])
            self.assertTrue(row["evidence_separation_valid"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_draft_fingerprint_spec_stays_review_only(self) -> None:
        spec = _load_json(
            ROOT / "artifacts" / "v3_epk_draft_fingerprint_spec_1025.json"
        )
        metadata = spec["metadata"]
        self.assertEqual(metadata["method"], "epk_draft_fingerprint_spec")
        self.assertTrue(metadata["draft_spec_ready_for_scorer_prototype"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertTrue(metadata["active_fingerprint_universe_unchanged"])
        self.assertEqual(metadata["current_positive_fingerprint_count"], 8)
        self.assertEqual(metadata["boundary_row_count"], 5)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["external_reaudit_row_count"], 3)
        self.assertEqual(
            spec["external_hard_negative_reaudit_summary"]["reaudit_status"],
            "planned_not_scored",
        )
        self.assertEqual(
            set(spec["external_hard_negative_reaudit_summary"]["entry_ids"]),
            EXTERNAL_HARD_NEGATIVES,
        )
        self.assertIn(
            "M-CSA mechanism text",
            spec["draft_fingerprint_spec"]["predictive_evidence_exclusions"],
        )
        for row in spec["boundary_rows"]:
            self.assertTrue(row["review_only"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertEqual(
                row["predictive_use_status"],
                "review_context_only_until_local_scorer_implemented",
            )

    def test_epk_local_evidence_audit_stays_review_only(self) -> None:
        audit = _load_json(
            ROOT / "artifacts" / "v3_epk_local_evidence_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(metadata["method"], "epk_local_evidence_audit")
        self.assertEqual(metadata["boundary_row_count"], 5)
        self.assertEqual(metadata["ready_for_text_free_axis_prototype_count"], 3)
        self.assertEqual(metadata["needs_ligand_or_structure_repair_count"], 2)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["entry_id"]: row for row in audit["rows"]}
        self.assertEqual(
            rows["m_csa:35"]["scorer_input_readiness"],
            "ready_for_text_free_axis_prototype",
        )
        self.assertEqual(
            rows["m_csa:246"]["scorer_input_readiness"],
            "ready_for_text_free_axis_prototype",
        )
        self.assertEqual(
            rows["m_csa:640"]["scorer_input_readiness"],
            "ready_for_text_free_axis_prototype",
        )
        self.assertEqual(
            rows["m_csa:282"]["scorer_input_readiness"],
            "needs_ligand_distance_or_structure_repair",
        )
        self.assertEqual(
            rows["m_csa:662"]["scorer_input_readiness"],
            "needs_ligand_source_or_alternate_structure",
        )
        for row in audit["rows"]:
            self.assertTrue(row["review_only"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertIn("no_epk_score_computed", row["audit_blockers"])

    def test_epk_text_free_local_axis_prototype_stays_review_only(self) -> None:
        prototype = _load_json(
            ROOT / "artifacts" / "v3_epk_text_free_local_axis_prototype_1025.json"
        )
        metadata = prototype["metadata"]
        self.assertEqual(metadata["method"], "epk_text_free_local_axis_prototype")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["prototype_ready_row_count"], 3)
        self.assertEqual(metadata["excluded_row_count"], 2)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        rows = {row["entry_id"]: row for row in prototype["rows"]}
        self.assertEqual(set(rows), {"m_csa:35", "m_csa:246", "m_csa:640"})
        for row in rows.values():
            self.assertTrue(row["review_only"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertEqual(row["axis_presence_count"], 3)
            self.assertFalse(row["epk_score_computed"])
            self.assertIn("epk_threshold_not_calibrated", row["audit_blockers"])
        excluded = {row["entry_id"]: row for row in prototype["excluded_rows"]}
        self.assertEqual(set(excluded), {"m_csa:282", "m_csa:662"})
        self.assertTrue(excluded["m_csa:282"]["excluded_from_axis_prototype"])
        self.assertTrue(excluded["m_csa:662"]["excluded_from_axis_prototype"])

    def test_epk_acceptor_geometry_axis_gap_plan_stays_review_only(self) -> None:
        plan = _load_json(
            ROOT / "artifacts" / "v3_epk_acceptor_geometry_axis_gap_plan_1025.json"
        )
        metadata = plan["metadata"]
        self.assertEqual(metadata["method"], "epk_acceptor_geometry_axis_gap_plan")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["prototype_ready_row_count"], 3)
        self.assertEqual(metadata["excluded_row_count"], 2)
        self.assertEqual(metadata["rows_with_candidate_acceptor_context_count"], 3)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["acceptor_axis_implemented_as_score"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        rows = {row["entry_id"]: row for row in plan["rows"]}
        self.assertEqual(set(rows), {"m_csa:35", "m_csa:246", "m_csa:640"})
        for row in rows.values():
            self.assertTrue(row["review_only"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["epk_score_computed"])
            self.assertGreater(row["hydroxyl_residue_candidate_count"], 0)
            self.assertIn("acceptor_axis_not_thresholded", row["remaining_blockers"])
        self.assertEqual(
            rows["m_csa:640"]["acceptor_axis_status"],
            "hydroxyl_residue_and_acceptor_ligand_context_present_not_scored",
        )
        excluded = {row["entry_id"]: row for row in plan["excluded_rows"]}
        self.assertEqual(set(excluded), {"m_csa:282", "m_csa:662"})

    def test_epk_nonready_ligand_repair_plan_stays_review_only(self) -> None:
        plan = _load_json(
            ROOT / "artifacts" / "v3_epk_nonready_ligand_repair_plan_1025.json"
        )
        metadata = plan["metadata"]
        self.assertEqual(metadata["method"], "epk_nonready_ligand_repair_plan")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["nonready_row_count"], 2)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        rows = {row["entry_id"]: row for row in plan["rows"]}
        self.assertEqual(set(rows), {"m_csa:282", "m_csa:662"})
        self.assertEqual(
            rows["m_csa:282"]["repair_lane"],
            "structure_ligand_signal_not_local_axis",
        )
        self.assertEqual(
            rows["m_csa:662"]["repair_lane"],
            "selected_structure_ligand_axis_missing",
        )
        self.assertTrue(rows["m_csa:282"]["structure_nucleotide_ligand_leads"])
        self.assertFalse(rows["m_csa:662"]["structure_nucleotide_ligand_leads"])
        for row in rows.values():
            self.assertTrue(row["review_only"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertIn(
                "not_ready_for_text_free_axis_prototype",
                row["remaining_blockers"],
            )

    def test_epk_nonready_ligand_alternate_plan_stays_review_only(self) -> None:
        plan = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_nonready_ligand_alternate_structure_plan_1025.json"
        )
        metadata = plan["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_nonready_ligand_alternate_structure_plan",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["row_count"], 2)
        self.assertEqual(metadata["alternate_gamma_structure_count"], 3)
        self.assertEqual(metadata["alternate_gamma_metal_mapped_structure_count"], 0)
        self.assertFalse(metadata["nonready_rows_repaired_or_excluded"])
        self.assertFalse(metadata["ready_to_rerun_local_evidence_audit"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["entry_id"]: row for row in plan["rows"]}
        self.assertEqual(set(rows), {"m_csa:282", "m_csa:662"})
        self.assertEqual(
            rows["m_csa:282"]["repair_evidence_status"],
            "alternate_gamma_structure_found_metal_or_mapping_gap",
        )
        self.assertEqual(rows["m_csa:282"]["alternate_gamma_structure_count"], 1)
        self.assertEqual(rows["m_csa:662"]["alternate_gamma_structure_count"], 2)
        for row in rows.values():
            self.assertFalse(row["ready_to_rerun_local_evidence_audit"])
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_nonready_ligand_exclusion_decision_stays_review_only(self) -> None:
        decision = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_nonready_ligand_exclusion_decision_1025.json"
        )
        metadata = decision["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_nonready_ligand_exclusion_decision",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["row_count"], 2)
        self.assertEqual(metadata["excluded_nonready_row_count"], 2)
        self.assertEqual(
            metadata["excluded_nonready_entry_ids"],
            ["m_csa:282", "m_csa:662"],
        )
        self.assertEqual(metadata["alternate_gamma_structure_count"], 3)
        self.assertEqual(metadata["alternate_gamma_metal_mapped_structure_count"], 0)
        self.assertTrue(metadata["nonready_rows_repaired_or_excluded"])
        self.assertFalse(metadata["ready_to_rerun_local_evidence_audit"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["entry_id"]: row for row in decision["rows"]}
        self.assertEqual(set(rows), {"m_csa:282", "m_csa:662"})
        self.assertEqual(
            rows["m_csa:282"]["exclusion_reason"],
            "selected_structure_signal_is_nonlocal_and_no_alternate_gamma_metal_mapped_structure",
        )
        self.assertEqual(
            rows["m_csa:662"]["exclusion_reason"],
            "alternate_gamma_structures_lack_metal_context_or_complete_catalytic_mapping",
        )
        for row in decision["rows"]:
            self.assertEqual(
                row["exclusion_decision"],
                "exclude_from_current_epk_threshold_calibration",
            )
            self.assertTrue(row["excluded_from_current_epk_threshold_calibration"])
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_acceptor_axis_threshold_design_stays_review_only(self) -> None:
        design = _load_json(
            ROOT / "artifacts" / "v3_epk_acceptor_axis_threshold_design_1025.json"
        )
        metadata = design["metadata"]
        self.assertEqual(metadata["method"], "epk_acceptor_axis_threshold_design")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["candidate_thresholds_angstrom"], [4.0, 6.0, 8.0])
        self.assertEqual(
            metadata[
                "smallest_candidate_hydroxyl_cutoff_covering_current_prototype_rows"
            ],
            6.0,
        )
        self.assertIsNone(metadata["selected_threshold_angstrom"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        threshold_rows = {
            row["candidate_threshold_angstrom"]: row
            for row in design["threshold_rows"]
        }
        self.assertEqual(threshold_rows[4.0]["hydroxyl_residue_hit_count"], 1)
        self.assertEqual(threshold_rows[6.0]["hydroxyl_residue_hit_count"], 3)
        self.assertEqual(threshold_rows[8.0]["combined_candidate_context_hit_count"], 3)

    def test_epk_gamma_geometry_feasibility_plan_stays_review_only(self) -> None:
        plan = _load_json(
            ROOT / "artifacts" / "v3_epk_gamma_geometry_feasibility_plan_1025.json"
        )
        metadata = plan["metadata"]
        self.assertEqual(metadata["method"], "epk_gamma_geometry_feasibility_plan")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["prototype_ready_row_count"], 3)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["gamma_phosphate_geometry_measured"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        rows = {row["entry_id"]: row for row in plan["rows"]}
        self.assertEqual(set(rows), {"m_csa:35", "m_csa:246", "m_csa:640"})
        self.assertEqual(
            rows["m_csa:35"]["gamma_geometry_feasibility_status"],
            "gamma_capable_nucleotide_and_acceptor_context_present_not_measured",
        )
        self.assertEqual(
            rows["m_csa:246"]["gamma_geometry_feasibility_status"],
            "gamma_capable_nucleotide_and_acceptor_context_present_not_measured",
        )
        self.assertEqual(
            rows["m_csa:640"]["gamma_geometry_feasibility_status"],
            "product_state_nucleotide_acceptor_context_present_needs_gamma_source",
        )
        for row in rows.values():
            self.assertFalse(row["gamma_phosphate_geometry_measured"])
            self.assertFalse(row["epk_score_computed"])

    def test_epk_gamma_geometry_measurement_sample_stays_review_only(self) -> None:
        sample = _load_json(
            ROOT / "artifacts" / "v3_epk_gamma_geometry_measurement_sample_1025.json"
        )
        metadata = sample["metadata"]
        self.assertEqual(metadata["method"], "epk_gamma_geometry_measurement_sample")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["row_count"], 3)
        self.assertEqual(metadata["measured_row_count"], 2)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertTrue(metadata["gamma_phosphate_geometry_measured"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        rows = {row["entry_id"]: row for row in sample["rows"]}
        self.assertEqual(set(rows), {"m_csa:35", "m_csa:246", "m_csa:640"})
        self.assertEqual(
            rows["m_csa:35"]["measurement_status"],
            "gamma_to_hydroxyl_distance_measured_review_only",
        )
        self.assertEqual(
            rows["m_csa:246"]["measurement_status"],
            "gamma_to_hydroxyl_distance_measured_review_only",
        )
        self.assertEqual(
            rows["m_csa:640"]["measurement_status"],
            "product_or_missing_gamma_nucleotide_skipped",
        )
        for row in rows.values():
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_acceptor_identity_review_stays_review_only(self) -> None:
        review = _load_json(
            ROOT / "artifacts" / "v3_epk_acceptor_identity_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(metadata["method"], "epk_acceptor_identity_review")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["row_count"], 3)
        self.assertEqual(metadata["measured_row_count"], 2)
        self.assertEqual(
            metadata["measured_acceptor_identity_source_supported_count"],
            2,
        )
        self.assertTrue(metadata["measured_acceptor_identity_review_complete"])
        self.assertTrue(metadata["mechanism_text_used_as_review_context_only"])
        self.assertTrue(metadata["text_free_scoring_preserved"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        rows = {row["entry_id"]: row for row in review["rows"]}
        self.assertEqual(set(rows), {"m_csa:35", "m_csa:246", "m_csa:640"})
        self.assertEqual(
            rows["m_csa:35"]["acceptor_identity_review_status"],
            "measured_acceptor_identity_source_supported_review_only",
        )
        self.assertEqual(
            rows["m_csa:246"]["acceptor_identity_review_status"],
            "measured_acceptor_identity_source_supported_review_only",
        )
        self.assertEqual(
            rows["m_csa:640"]["acceptor_identity_review_status"],
            "source_acceptor_supported_gamma_geometry_missing",
        )
        for row in rows.values():
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertEqual(
                row["predictive_use_status"],
                "review_context_only_not_epk_scoring_input",
            )

    def test_epk_atp_state_evidence_plan_stays_review_only(self) -> None:
        plan = _load_json(
            ROOT / "artifacts" / "v3_epk_atp_state_evidence_plan_1025.json"
        )
        metadata = plan["metadata"]
        self.assertEqual(metadata["method"], "epk_atp_state_evidence_plan")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["row_count"], 1)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["gamma_geometry_measured"])
        self.assertEqual(
            metadata["alternate_gamma_acceptor_geometry_measured_count"],
            1,
        )
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        row = plan["rows"][0]
        self.assertEqual(row["entry_id"], "m_csa:640")
        self.assertEqual(row["gamma_capable_candidate_structure_count"], 2)
        self.assertEqual(row["gamma_capable_acceptor_candidate_structure_count"], 1)
        self.assertEqual(
            row["alternate_gamma_acceptor_geometry_measured_structure_count"],
            1,
        )
        self.assertEqual(metadata["candidate_atp_state_acceptor_row_count"], 1)
        self.assertEqual(
            metadata["gamma_capable_residue_mapped_candidate_structure_count"],
            2,
        )
        self.assertEqual(
            row["atp_state_evidence_status"],
            "candidate_atp_state_acceptor_structure_found_review_only",
        )
        self.assertFalse(row["epk_score_computed"])
        self.assertFalse(row["countable_label_candidate"])

    def test_epk_gamma_threshold_control_plan_stays_review_only(self) -> None:
        plan = _load_json(
            ROOT / "artifacts" / "v3_epk_gamma_threshold_control_plan_1025.json"
        )
        metadata = plan["metadata"]
        self.assertEqual(metadata["method"], "epk_gamma_threshold_control_plan")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["row_count"], 3)
        self.assertEqual(metadata["current_selected_measured_row_count"], 2)
        self.assertEqual(metadata["alternate_structure_measured_row_count"], 1)
        self.assertEqual(
            metadata["lowest_review_geometry_covering_candidate_angstrom"],
            6.0,
        )
        self.assertTrue(metadata["threshold_control_plan_ready"])
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertIsNone(metadata["selected_threshold_angstrom"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["control_requirement_count"], 4)
        scenarios = {
            scenario["threshold_angstrom"]: scenario
            for scenario in metadata["threshold_scenarios"]
        }
        self.assertIn("m_csa:246", scenarios[4.0]["missed_review_geometry_entry_ids"])
        self.assertEqual(scenarios[6.0]["missed_review_geometry_entry_ids"], [])
        rows = {(row["entry_id"], row["pdb_id"]): row for row in plan["rows"]}
        self.assertEqual(
            rows[("m_csa:640", "3TM0")]["geometry_scope"],
            "alternate_graph_linked_structure",
        )
        for row in plan["rows"]:
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_negative_control_distribution_stays_review_only(self) -> None:
        distribution = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_negative_control_gamma_distance_distribution_1025.json"
        )
        metadata = distribution["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_negative_control_gamma_distance_distribution",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["source_control_row_count"], 15)
        self.assertEqual(metadata["measured_control_count"], 2)
        self.assertEqual(
            metadata["measured_control_family_ids"],
            ["dnk", "ghmp"],
        )
        self.assertTrue(metadata["negative_control_distance_distribution_started"])
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertEqual(
            metadata["lowest_covering_candidate_negative_control_hit_count"],
            1,
        )
        self.assertEqual(
            metadata["threshold_selection_status"],
            "blocked_negative_controls_overlap_or_insufficient_distribution",
        )
        self.assertIsNone(metadata["selected_threshold_angstrom"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        collisions = {
            row["threshold_angstrom"]: row
            for row in metadata["threshold_collision_rows"]
        }
        self.assertIn(
            "m_csa:615",
            collisions[6.0]["measured_negative_control_hit_entry_ids"],
        )
        rows = {row["entry_id"]: row for row in distribution["rows"]}
        self.assertEqual(
            rows["m_csa:615"]["measurement_status"],
            "selected_structure_gamma_to_hydroxyl_distance_measured_review_only",
        )
        self.assertEqual(
            rows["m_csa:615"]["nearest_gamma_to_hydroxyl_distance_angstrom"],
            3.232,
        )
        self.assertEqual(
            rows["m_csa:654"]["nearest_gamma_to_hydroxyl_distance_angstrom"],
            6.184,
        )
        for row in distribution["rows"]:
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_sibling_negative_control_alternate_plan_stays_review_only(
        self,
    ) -> None:
        plan = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_sibling_negative_control_alternate_structure_plan_1025.json"
        )
        metadata = plan["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_sibling_negative_control_alternate_structure_plan",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["source_control_row_count"], 15)
        self.assertEqual(metadata["source_unmeasured_control_row_count"], 13)
        self.assertEqual(metadata["row_count"], 13)
        self.assertEqual(metadata["max_structures_per_entry"], 8)
        self.assertEqual(metadata["screened_alternate_pdb_count"], 38)
        self.assertEqual(metadata["alternate_gamma_structure_count"], 7)
        self.assertEqual(metadata["alternate_gamma_metal_mapped_structure_count"], 3)
        self.assertEqual(metadata["ready_for_future_distance_measurement_count"], 3)
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertIsNone(metadata["selected_threshold_angstrom"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["entry_id"]: row for row in plan["rows"]}
        self.assertEqual(
            rows["m_csa:592"]["alternate_control_evidence_status"],
            "alternate_gamma_metal_mapped_candidate_found_review_only",
        )
        self.assertEqual(
            rows["m_csa:696"]["alternate_control_evidence_status"],
            "alternate_gamma_metal_mapped_candidate_found_review_only",
        )
        self.assertEqual(
            rows["m_csa:603"]["alternate_control_evidence_status"],
            "alternate_gamma_metal_mapped_candidate_found_review_only",
        )
        for row in plan["rows"]:
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_sibling_negative_control_alternate_gamma_sample_stays_review_only(
        self,
    ) -> None:
        sample = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_sibling_negative_control_alternate_gamma_distance_sample_1025.json"
        )
        metadata = sample["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_sibling_negative_control_alternate_gamma_distance_sample",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["candidate_structure_count"], 3)
        self.assertEqual(metadata["measured_candidate_structure_count"], 3)
        self.assertEqual(metadata["measured_entry_count"], 3)
        self.assertEqual(
            metadata["measured_entry_ids"],
            ["m_csa:592", "m_csa:603", "m_csa:696"],
        )
        self.assertEqual(metadata["measured_family_ids"], ["askha", "ghkl"])
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertEqual(
            metadata["lowest_covering_candidate_alternate_negative_control_hit_count"],
            1,
        )
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {(row["entry_id"], row["pdb_id"]): row for row in sample["rows"]}
        self.assertEqual(
            rows[("m_csa:592", "3FGU")][
                "nearest_gamma_to_hydroxyl_distance_angstrom"
            ],
            4.175,
        )
        self.assertEqual(
            rows[("m_csa:603", "3CRL")][
                "nearest_gamma_to_hydroxyl_distance_angstrom"
            ],
            7.91,
        )
        self.assertEqual(
            rows[("m_csa:696", "1QHA")][
                "nearest_gamma_to_hydroxyl_distance_angstrom"
            ],
            9.92,
        )
        for row in sample["rows"]:
            self.assertEqual(
                row["measurement_status"],
                "alternate_gamma_to_hydroxyl_distance_measured_review_only",
            )
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_negative_control_calibration_sufficiency_stays_blocked(
        self,
    ) -> None:
        decision = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_negative_control_calibration_sufficiency_decision_1025.json"
        )
        metadata = decision["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_negative_control_calibration_sufficiency_decision",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["selected_structure_measured_control_count"], 2)
        self.assertEqual(metadata["alternate_structure_measured_control_count"], 3)
        self.assertEqual(metadata["combined_measured_control_count"], 5)
        self.assertEqual(metadata["combined_measured_family_count"], 4)
        self.assertEqual(
            metadata["missing_sibling_family_ids"],
            ["atp_grasp", "ndk", "pfka", "pfkb"],
        )
        self.assertEqual(
            metadata["calibration_sufficiency_status"],
            "blocked_review_only",
        )
        self.assertEqual(
            metadata["threshold_calibration_decision"],
            "do_not_select_threshold",
        )
        self.assertEqual(
            metadata["negative_control_calibration_blockers"],
            [
                "sibling_family_coverage_incomplete",
                "candidate_threshold_collides_with_sibling_controls",
            ],
        )
        self.assertEqual(
            metadata["lowest_covering_candidate_negative_control_hit_count"],
            2,
        )
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        collisions = {
            row["threshold_angstrom"]: row
            for row in metadata["threshold_collision_rows"]
        }
        self.assertEqual(
            collisions[6.0]["combined_negative_control_hit_entry_ids"],
            ["m_csa:592", "m_csa:615"],
        )
        self.assertEqual(
            collisions[8.0]["combined_negative_control_hit_entry_ids"],
            ["m_csa:592", "m_csa:603", "m_csa:615", "m_csa:654"],
        )
        for row in decision["rows"]:
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_sibling_control_repair_review_stays_review_only(self) -> None:
        review = _load_json(
            ROOT / "artifacts" / "v3_epk_sibling_control_repair_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(metadata["method"], "epk_sibling_control_repair_review")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_family_id"], "pfkb")
        self.assertEqual(metadata["family_repair_review_status"], "blocked_review_only")
        self.assertEqual(metadata["gamma_capable_structure_count"], 1)
        self.assertEqual(metadata["mapped_gamma_structure_count"], 1)
        self.assertEqual(metadata["metal_supported_gamma_structure_count"], 0)
        self.assertEqual(metadata["measurement_ready_repaired_structure_count"], 0)
        self.assertEqual(metadata["unresolved_entry_ids"], ["m_csa:663", "m_csa:670"])
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["entry_id"]: row for row in review["rows"]}
        self.assertEqual(
            rows["m_csa:663"]["repair_review_status"],
            "mapping_verified_metal_context_unresolved",
        )
        self.assertEqual(rows["m_csa:663"]["measurement_ready_structure_count"], 0)
        self.assertEqual(
            rows["m_csa:663"]["candidate_structure_reviews"][0][
                "repair_assessment_status"
            ],
            "mapping_verified_metal_context_unresolved",
        )
        for row in review["rows"]:
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_ndk_sibling_control_repair_review_stays_review_only(self) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_sibling_control_repair_review_ndk_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(metadata["method"], "epk_sibling_control_repair_review")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_family_id"], "ndk")
        self.assertEqual(metadata["family_repair_review_status"], "blocked_review_only")
        self.assertEqual(metadata["gamma_capable_structure_count"], 0)
        self.assertEqual(metadata["mapped_gamma_structure_count"], 0)
        self.assertEqual(metadata["metal_supported_gamma_structure_count"], 0)
        self.assertEqual(metadata["measurement_ready_repaired_structure_count"], 0)
        self.assertEqual(metadata["unresolved_entry_ids"], ["m_csa:637"])
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["entry_id"]: row for row in review["rows"]}
        self.assertEqual(
            rows["m_csa:637"]["repair_review_status"],
            "source_or_repair_still_required",
        )
        self.assertEqual(rows["m_csa:637"]["measurement_ready_structure_count"], 0)
        structure = rows["m_csa:637"]["candidate_structure_reviews"][0]
        self.assertEqual(
            structure["repair_assessment_status"],
            "product_or_partial_nucleotide_not_gamma_capable",
        )
        self.assertIn("MG", structure["observed_metal_ligand_codes"])
        self.assertFalse(structure["has_gamma_capable_nucleotide"])
        for row in review["rows"]:
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_remaining_sibling_control_repair_reviews_stay_review_only(self) -> None:
        expectations = {
            "atp_grasp": {
                "path": "v3_epk_sibling_control_repair_review_atp_grasp_1025.json",
                "unresolved": ["m_csa:310", "m_csa:498"],
                "row_status_counts": {
                    "no_candidate_structures_to_review": 1,
                    "source_or_repair_still_required": 1,
                },
            },
            "pfka": {
                "path": "v3_epk_sibling_control_repair_review_pfka_1025.json",
                "unresolved": ["m_csa:365"],
                "row_status_counts": {"source_or_repair_still_required": 1},
            },
        }
        for family_id, expected in expectations.items():
            with self.subTest(family_id=family_id):
                review = _load_json(ROOT / "artifacts" / expected["path"])
                metadata = review["metadata"]
                self.assertEqual(
                    metadata["method"], "epk_sibling_control_repair_review"
                )
                self.assertTrue(metadata["review_only"])
                self.assertEqual(metadata["reviewed_family_id"], family_id)
                self.assertEqual(
                    metadata["family_repair_review_status"],
                    "blocked_review_only",
                )
                self.assertEqual(metadata["gamma_capable_structure_count"], 0)
                self.assertEqual(metadata["mapped_gamma_structure_count"], 0)
                self.assertEqual(metadata["metal_supported_gamma_structure_count"], 0)
                self.assertEqual(
                    metadata["measurement_ready_repaired_structure_count"], 0
                )
                self.assertEqual(
                    metadata["unresolved_entry_ids"], expected["unresolved"]
                )
                self.assertEqual(
                    metadata["row_repair_status_counts"],
                    expected["row_status_counts"],
                )
                self.assertFalse(metadata["negative_control_distance_distribution_ready"])
                self.assertFalse(metadata["threshold_calibrated"])
                self.assertFalse(metadata["epk_score_computed"])
                self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
                self.assertFalse(metadata["ready_to_run_epk_scorer"])
                self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
                self.assertFalse(metadata["fingerprint_registry_edited"])
                self.assertFalse(metadata["curated_label_registry_edited"])
                self.assertEqual(metadata["countable_label_candidate_count"], 0)
                for row in review["rows"]:
                    self.assertFalse(row["epk_score_computed"])
                    self.assertFalse(row["countable_label_candidate"])
                    self.assertEqual(row["measurement_ready_structure_count"], 0)

    def test_epk_precount_gate_status_stays_blocked(self) -> None:
        status = _load_json(
            ROOT / "artifacts" / "v3_epk_precount_gate_status_1025.json"
        )
        metadata = status["metadata"]
        self.assertEqual(metadata["method"], "epk_precount_gate_status")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["precount_gate_status"], "blocked_review_only")
        self.assertEqual(metadata["prototype_ready_row_count"], 3)
        self.assertEqual(metadata["gamma_measured_row_count"], 2)
        self.assertEqual(metadata["measured_acceptor_identity_source_supported_count"], 2)
        self.assertEqual(
            metadata["source_epk_acceptor_identity_review_method"],
            "epk_acceptor_identity_review",
        )
        self.assertEqual(
            metadata["source_epk_atp_state_evidence_plan_method"],
            "epk_atp_state_evidence_plan",
        )
        self.assertEqual(
            metadata["source_epk_gamma_threshold_control_plan_method"],
            "epk_gamma_threshold_control_plan",
        )
        self.assertEqual(
            metadata[
                "source_epk_negative_control_gamma_distance_distribution_method"
            ],
            "epk_negative_control_gamma_distance_distribution",
        )
        self.assertEqual(
            metadata["source_epk_nonready_ligand_exclusion_decision_method"],
            "epk_nonready_ligand_exclusion_decision",
        )
        self.assertEqual(
            metadata[
                "source_epk_sibling_negative_control_alternate_structure_plan_method"
            ],
            "epk_sibling_negative_control_alternate_structure_plan",
        )
        self.assertEqual(
            metadata[
                "source_epk_sibling_negative_control_alternate_gamma_distance_sample_method"
            ],
            "epk_sibling_negative_control_alternate_gamma_distance_sample",
        )
        self.assertEqual(
            metadata[
                "source_epk_negative_control_calibration_sufficiency_decision_method"
            ],
            "epk_negative_control_calibration_sufficiency_decision",
        )
        self.assertEqual(
            metadata["source_epk_sibling_control_repair_review_method"],
            "epk_sibling_control_repair_review",
        )
        self.assertTrue(metadata["gamma_threshold_control_plan_ready"])
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertEqual(metadata["negative_control_measured_control_count"], 2)
        self.assertEqual(metadata["negative_control_lowest_candidate_hit_count"], 1)
        self.assertEqual(metadata["negative_control_alternate_ready_for_measurement_count"], 3)
        self.assertEqual(
            metadata["negative_control_alternate_measured_candidate_structure_count"],
            3,
        )
        self.assertEqual(metadata["negative_control_alternate_measured_entry_count"], 3)
        self.assertEqual(
            metadata["negative_control_alternate_lowest_candidate_hit_count"],
            1,
        )
        self.assertEqual(
            metadata["negative_control_calibration_sufficiency_status"],
            "blocked_review_only",
        )
        self.assertEqual(metadata["negative_control_combined_measured_control_count"], 5)
        self.assertEqual(metadata["negative_control_combined_measured_family_count"], 4)
        self.assertEqual(metadata["negative_control_repair_review_family_id"], "pfkb")
        self.assertEqual(
            metadata["negative_control_repair_review_family_ids"],
            ["atp_grasp", "ndk", "pfka", "pfkb"],
        )
        self.assertEqual(
            metadata["negative_control_repair_review_status"],
            "blocked_review_only",
        )
        self.assertEqual(
            metadata["negative_control_repair_review_status_counts"],
            {"blocked_review_only": 4},
        )
        self.assertEqual(metadata["negative_control_repair_review_ready_structure_count"], 0)
        self.assertEqual(
            metadata["negative_control_repair_review_ready_structure_count_total"],
            0,
        )
        self.assertEqual(
            metadata["negative_control_repair_review_unresolved_entry_ids"],
            ["m_csa:663", "m_csa:670"],
        )
        self.assertEqual(
            metadata["negative_control_repair_review_unresolved_entry_ids_all"],
            [
                "m_csa:310",
                "m_csa:365",
                "m_csa:498",
                "m_csa:637",
                "m_csa:663",
                "m_csa:670",
            ],
        )
        self.assertEqual(
            metadata["negative_control_homolog_source_plan_method"],
            "epk_sibling_control_homolog_source_plan",
        )
        self.assertEqual(metadata["negative_control_homolog_source_family_id"], "ndk")
        self.assertEqual(metadata["negative_control_homolog_source_candidate_count"], 4)
        self.assertEqual(
            metadata["negative_control_homolog_source_gamma_metal_candidate_count"],
            4,
        )
        self.assertEqual(
            metadata["negative_control_homolog_source_ready_structure_count"],
            0,
        )
        self.assertEqual(
            metadata["source_epk_sibling_control_homolog_mapping_review_method"],
            "epk_sibling_control_homolog_mapping_review",
        )
        self.assertEqual(metadata["negative_control_homolog_mapping_family_id"], "ndk")
        self.assertEqual(metadata["negative_control_homolog_mapping_candidate_count"], 4)
        self.assertEqual(
            metadata["negative_control_homolog_mapping_histidine_mapped_count"],
            4,
        )
        self.assertEqual(
            metadata["negative_control_homolog_mapping_nucleotide_site_mapped_count"],
            4,
        )
        self.assertEqual(
            metadata["negative_control_homolog_mapping_ready_structure_count"],
            4,
        )
        self.assertEqual(metadata["nonready_ligand_repair_row_count"], 2)
        self.assertEqual(metadata["nonready_ligand_excluded_count"], 2)
        self.assertTrue(metadata["nonready_rows_repaired_or_excluded"])
        self.assertIsNone(metadata["selected_acceptor_threshold_angstrom"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertIn("acceptor_threshold_calibrated", metadata["failing_gate_ids"])
        self.assertIn(
            "gamma_geometry_measured_for_all_prototype_rows",
            metadata["failing_gate_ids"],
        )
        self.assertNotIn(
            "nonready_rows_repaired_or_excluded",
            metadata["failing_gate_ids"],
        )

        self.assertIn(
            "external_hard_negative_scored_reaudit",
            metadata["failing_gate_ids"],
        )
        self.assertIn(
            "gamma_negative_control_distance_distribution",
            metadata["failing_gate_ids"],
        )
        checks = {check["gate_id"]: check for check in status["gate_checks"]}
        self.assertTrue(checks["local_axis_prototype"]["passed"])
        self.assertTrue(checks["measured_acceptor_identity_reviewed"]["passed"])
        self.assertTrue(checks["nonready_rows_repaired_or_excluded"]["passed"])
        self.assertTrue(checks["gamma_threshold_control_plan"]["passed"])
        self.assertFalse(
            checks["gamma_negative_control_distance_distribution"]["passed"]
        )
        self.assertEqual(
            checks["gamma_negative_control_distance_distribution"]["evidence"][
                "alternate_structure_ready_for_measurement_count"
            ],
            3,
        )
        self.assertEqual(
            checks["gamma_negative_control_distance_distribution"]["evidence"][
                "alternate_structure_measured_candidate_structure_count"
            ],
            3,
        )
        self.assertEqual(
            checks["gamma_negative_control_distance_distribution"]["evidence"][
                "alternate_structure_lowest_candidate_hit_count"
            ],
            1,
        )
        self.assertEqual(
            checks["gamma_negative_control_distance_distribution"]["evidence"][
                "calibration_sufficiency_status"
            ],
            "blocked_review_only",
        )
        self.assertEqual(
            checks["gamma_negative_control_distance_distribution"]["evidence"][
                "combined_measured_control_count"
            ],
            5,
        )
        self.assertEqual(
            checks["gamma_negative_control_distance_distribution"]["evidence"][
                "sibling_control_repair_review_status"
            ],
            "blocked_review_only",
        )
        self.assertEqual(
            checks["gamma_negative_control_distance_distribution"]["evidence"][
                "sibling_control_homolog_source_family_id"
            ],
            "ndk",
        )
        self.assertEqual(
            checks["gamma_negative_control_distance_distribution"]["evidence"][
                "sibling_control_homolog_source_gamma_metal_candidate_count"
            ],
            4,
        )
        self.assertEqual(
            checks["gamma_negative_control_distance_distribution"]["evidence"][
                "sibling_control_homolog_mapping_ready_structure_count"
            ],
            4,
        )
        self.assertFalse(checks["registry_and_label_factory_extension"]["passed"])

    def test_epk_post_repair_source_decision_stays_review_only(self) -> None:
        decision = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_missing_sibling_control_post_repair_source_decision_1025.json"
        )
        metadata = decision["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_missing_sibling_control_post_repair_source_decision",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["reviewed_sibling_family_ids"],
            ["atp_grasp", "ndk", "pfka", "pfkb"],
        )
        self.assertEqual(metadata["unreviewed_sibling_family_ids"], [])
        self.assertEqual(
            metadata["post_repair_source_decision_counts"],
            {"external_or_homolog_source_needed": 6},
        )
        self.assertEqual(metadata["source_escalation_required_entry_count"], 6)
        self.assertEqual(metadata["direct_repair_measurement_ready_structure_count"], 0)
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            metadata["source_escalation_required_entry_ids"],
            [
                "m_csa:310",
                "m_csa:365",
                "m_csa:498",
                "m_csa:637",
                "m_csa:663",
                "m_csa:670",
            ],
        )
        for row in decision["rows"]:
            self.assertEqual(
                row["post_repair_source_decision"],
                "external_or_homolog_source_needed",
            )
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_ndk_homolog_source_plan_stays_review_only(self) -> None:
        plan = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_sibling_control_homolog_source_plan_ndk_1025.json"
        )
        metadata = plan["metadata"]
        self.assertEqual(
            metadata["method"], "epk_sibling_control_homolog_source_plan"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_sibling_family_id"], "ndk")
        self.assertEqual(metadata["source_entry_ids"], ["m_csa:637"])
        self.assertEqual(metadata["candidate_pdb_count"], 4)
        self.assertEqual(metadata["metal_supported_gamma_candidate_count"], 4)
        self.assertEqual(metadata["measurement_ready_homolog_structure_count"], 0)
        self.assertEqual(metadata["catalytic_mapping_verified_count"], 0)
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        statuses = {
            row["pdb_id"]: row["source_candidate_status"] for row in plan["rows"]
        }
        self.assertEqual(
            set(statuses.values()), {"candidate_gamma_metal_source_review_only"}
        )
        self.assertEqual(set(statuses), {"1WKL", "3Q86", "9OAN", "9PFY"})
        for row in plan["rows"]:
            self.assertEqual(
                row["catalytic_mapping_status"], "not_mapped_review_pending"
            )
            self.assertFalse(row["measurement_ready_for_negative_control"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_ndk_homolog_mapping_review_stays_review_only(self) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_sibling_control_homolog_mapping_review_ndk_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"], "epk_sibling_control_homolog_mapping_review"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_sibling_family_id"], "ndk")
        self.assertEqual(
            metadata["source_epk_sibling_control_homolog_source_plan_method"],
            "epk_sibling_control_homolog_source_plan",
        )
        self.assertEqual(metadata["mapping_reviewed_candidate_count"], 4)
        self.assertEqual(metadata["catalytic_histidine_mapped_candidate_count"], 4)
        self.assertEqual(metadata["nucleotide_site_mapped_candidate_count"], 4)
        self.assertEqual(metadata["measurement_ready_homolog_structure_count"], 4)
        self.assertFalse(metadata["calibration_distance_measured"])
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        statuses = {
            row["pdb_id"]: row["homolog_mapping_status"] for row in review["rows"]
        }
        self.assertEqual(
            set(statuses.values()),
            {"homolog_mapping_ready_for_distance_measurement_review_only"},
        )
        self.assertEqual(set(statuses), {"1WKL", "3Q86", "9OAN", "9PFY"})
        for row in review["rows"]:
            self.assertTrue(row["measurement_ready_for_negative_control"])
            self.assertFalse(row["negative_control_distance_distribution_ready"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertTrue(row["chain_mappings"])
            self.assertTrue(row["catalytic_histidine_mapping_verified"])
            self.assertTrue(row["nucleotide_site_mapping_verified"])

    def test_mcsa_strict_structural_ood_claim_stays_disabled(self) -> None:
        adjudication = _load_json(
            ROOT / "artifacts" / "v3_mcsa_tm_holdout_feasibility_adjudication_1000.json"
        )
        self.assertFalse(
            adjudication["metadata"]["full_tm_score_holdout_claim_permitted"]
        )
        for path in (
            ROOT / "README.md",
            ROOT / "docs" / "external_source_transfer.md",
            ROOT / "work" / "handoff.md",
            ROOT / "work" / "scope.md",
        ):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("full_tm_score_holdout_claim_permitted=true", text)
            self.assertNotIn("resume M-CSA strict-TM round repair", text)


def _terminal_review_decisions() -> dict:
    return {
        "metadata": {
            "method": "external_hard_negative_next_candidate_terminal_review_decisions"
        },
        "rows": [
            {
                "accession": "PTEST",
                "entry_id": "uniprot:PTEST",
                "lane_id": "test_lane",
                "target_label_type": "out_of_scope",
                "target_fingerprint_id": None,
                "ontology_version_at_decision": "label_factory_v1_8fp",
                "terminal_review_decision_status": (
                    "accepted_out_of_scope_pending_factory_gate"
                ),
                "source_evidence_status": (
                    "explicit_active_site_and_catalytic_activity_source_present"
                ),
                "bounded_duplicate_evidence_status": (
                    "bounded_duplicate_controls_clear_uniref_pending"
                ),
                "uniref_current_reference_screen_status": (
                    "uniref_current_reference_screen_no_current_reference_overlap"
                ),
                "out_of_scope_inverse_gate": {
                    "inverse_gate_status": "passed",
                    "target_label_type": "out_of_scope",
                    "target_fingerprint_id": None,
                    "ontology_version_at_decision": "label_factory_v1_8fp",
                    "threshold_policy_version": (
                        EXTERNAL_HARD_NEGATIVE_THRESHOLD_POLICY_VERSION
                    ),
                    "abstain_threshold": EXTERNAL_HARD_NEGATIVE_ABSTAIN_THRESHOLD,
                    "expected_current_fingerprint_count": 8,
                    "observed_current_fingerprint_count": 8,
                    "all_current_fingerprint_scores_below_threshold": True,
                    "max_current_fingerprint_score": 0.2,
                    "current_fingerprint_scores": {
                        "cobalamin_radical_rearrangement": 0.1,
                        "flavin_dehydrogenase_reductase": 0.1,
                        "flavin_monooxygenase": 0.1,
                        "heme_peroxidase_oxidase": 0.1,
                        "metal_dependent_hydrolase": 0.2,
                        "plp_dependent_enzyme": 0.1,
                        "radical_sam_enzyme": 0.1,
                        "ser_his_acid_hydrolase": 0.1,
                    },
                },
                "top1_fingerprint_id": "metal_dependent_hydrolase",
                "top1_score": 0.2,
                "max_current_fingerprint_score": 0.2,
                "remaining_import_blockers": ["full_label_factory_gate_not_run"],
            }
        ],
    }


def _passed_label_factory_gate() -> dict:
    return {
        "metadata": {
            "method": "label_factory_gate_check",
            "gate_count": 1,
            "passed_gate_count": 1,
        },
        "blockers": [],
    }


def _passed_external_transfer_gate() -> dict:
    return {
        "metadata": {
            "method": "external_source_transfer_gate_check",
            "guardrail_clean": True,
        },
        "blockers": [],
    }


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
