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
        self.assertEqual(metadata["nonready_ligand_repair_row_count"], 2)
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
        self.assertIn("nonready_rows_repaired_or_excluded", metadata["failing_gate_ids"])
        self.assertIn(
            "external_hard_negative_scored_reaudit",
            metadata["failing_gate_ids"],
        )
        checks = {check["gate_id"]: check for check in status["gate_checks"]}
        self.assertTrue(checks["local_axis_prototype"]["passed"])
        self.assertFalse(checks["registry_and_label_factory_extension"]["passed"])

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
