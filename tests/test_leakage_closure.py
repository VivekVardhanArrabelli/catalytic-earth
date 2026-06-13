from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.fingerprints import load_fingerprints

from catalytic_earth.labels import (
    build_epk_5hvk_local_polymer_entity_role_audit,
    build_epk_5hvk_protein_substrate_axis_generalization_audit,
    build_epk_external_protein_substrate_source_scout,
    build_epk_external_source_alternate_cocomplex_review,
    build_epk_external_source_lower_priority_ligand_sourcing_review,
    build_epk_external_source_scout_pass_terminal_decision,
    build_epk_external_source_structure_mapping_review,
    build_epk_ligand_specific_5hvk_control_rerun_queue,
    build_epk_ligand_specific_5hvk_prototype_control_rerun,
    build_epk_ligand_specific_5hvk_source_validity_review,
    build_epk_local_chain_topology_acceptor_replacement_rule,
    build_epk_mek_erk_broad_role_stress_audit,
    build_epk_mek_erk_context_counteraxis_stress_audit,
    build_epk_mek_erk_phosphosite_source_review,
    build_epk_mek_erk_residual_false_hit_source_adjudication,
    build_epk_mek_erk_role_control_rerun,
    build_epk_mek_erk_source_free_topology_ambiguity_counteraxis,
    build_epk_mek_erk_source_free_topology_broader_stress_audit,
    build_epk_mek_erk_substrate_mode_counteraxis_audit,
    build_epk_mek_erk_substrate_mode_existing_scout_gap_audit,
    build_epk_mek_erk_substrate_mode_fresh_stress_audit,
    build_epk_substrate_mode_next_tranche_source_review,
    build_epk_substrate_mode_tranche_recovery_decision,
    build_epk_midlength_protein_role_counteraxis_audit,
    build_epk_protein_substrate_calibration_diagnostic,
    build_epk_protein_substrate_scorer_design_freeze,
    build_epk_heteromeric_candidate_source_validation_review,
    build_epk_heteromeric_chain_topology_signal_audit,
    build_epk_heteromeric_positive_coverage_candidate_scout,
    build_epk_heteromeric_source_valid_candidate_gamma_distance_sample,
    build_epk_heteromeric_source_free_role_rule_probe,
    build_epk_heteromeric_source_valid_control_rerun,
    build_epk_heteromeric_text_free_axis_gap_audit,
    build_epk_heteromeric_acceptor_chain_counteraxis_audit,
    build_epk_heteromeric_broader_counteraxis_control_audit,
    build_epk_heteromeric_ligand_asymmetry_role_audit,
    build_epk_heteromeric_acceptor_identity_gap_audit,
    build_epk_heteromeric_acceptor_identity_rule_probe,
    build_epk_heteromeric_peptide_acceptor_identity_probe,
    build_epk_heteromeric_peptide_broader_stress_audit,
    build_epk_heteromeric_peptide_external_hard_negative_probe,
    build_epk_heteromeric_source_expansion_peptide_role_axis_audit,
    build_epk_substrate_mode_gap_audit,
    build_epk_source_authority_axis_replacement_gap_audit,
    build_epk_source_free_chain_topology_role_audit,
    load_labels,
)
from catalytic_earth.labels import CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION
from catalytic_earth.transfer_scope import (
    EXTERNAL_HARD_NEGATIVE_ABSTAIN_THRESHOLD,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_12FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_14FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_15FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_16FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_17FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_18FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_19FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_20FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_21FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_22FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_23FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_24FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_25FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_26FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_27FP_ARTIFACT,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_28FP_ARTIFACT,
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

    def test_mek_erk_source_validation_fails_closed_for_phosphosite_state(
        self,
    ) -> None:
        scout = {
            "metadata": {
                "method": "epk_heteromeric_positive_coverage_candidate_scout",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
            },
            "rows": [
                {
                    "pdb_id": "9UUR",
                    "candidate_status": (
                        "heteromeric_candidate_source_validation_pending_review_only"
                    ),
                    "heteromeric_candidate_hit_count": 1,
                    "heteromeric_candidate_hits": [
                        {
                            "candidate_chain_name": "B",
                            "candidate_residue_code": "TYR",
                            "candidate_auth_seq_id": "204",
                            "gamma_associated_polymer_chain_name": "A",
                            "nearest_gamma_distance_angstrom": 4.181,
                        }
                    ],
                }
            ],
        }
        cif_text = "\n".join(
            [
                "data_9UUR",
                "loop_",
                "_struct.title",
                "'The complex of human pMEK1 and uERK1 (ANP)'",
                "#",
                "loop_",
                "_entity.id",
                "_entity.pdbx_description",
                "1 'Dual specificity mitogen-activated protein kinase kinase 1'",
                "2 'Mitogen-activated protein kinase 3'",
                "#",
                "loop_",
                "_struct_ref_seq.pdbx_db_accession",
                "_struct_ref_seq.pdbx_strand_id",
                "Q02750 A",
                "P27361 B",
                "#",
            ]
        )

        review = build_epk_heteromeric_candidate_source_validation_review(
            epk_heteromeric_positive_coverage_candidate_scout=scout,
            cif_text_by_pdb={"9UUR": cif_text},
        )
        row = review["rows"][0]
        self.assertEqual(
            row["source_validation_status"],
            "blocked_mek_erk_role_direction_or_phosphosite_state_unresolved_review_only",
        )
        self.assertEqual(row["source_pair_id"], "mek1_erk1")
        self.assertFalse(row["source_validated_positive_like"])
        self.assertIn(
            "acceptor_phosphorylation_state_not_adjudicated",
            row["remaining_blockers"],
        )
        self.assertFalse(review["metadata"]["ready_to_run_epk_scorer"])

    def test_next_tranche_pre_registration_is_frozen_before_selection(self) -> None:
        artifact = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_hard_negative_next_tranche_preregistration_1025.json"
        )
        metadata = artifact["metadata"]
        # This pre-registration was frozen in the 8-fingerprint era. The Stage-2
        # metal_dependent_hydrolase v2 split (2026-06-11) expanded the positive
        # fingerprint universe, so the frozen artifact's universe is now a STRICT
        # SUBSET of the live registry -- it must be re-frozen against the expanded
        # universe before the next OOS hard-negative tranche (Stage-3 work). We pin
        # the frozen 8fp universe here and assert the split only ADDED fingerprints.
        frozen_8fp_universe = sorted(
            [
                "cobalamin_radical_rearrangement",
                "flavin_dehydrogenase_reductase",
                "flavin_monooxygenase",
                "heme_peroxidase_oxidase",
                "metal_dependent_hydrolase",
                "plp_dependent_enzyme",
                "radical_sam_enzyme",
                "ser_his_acid_hydrolase",
            ]
        )
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())

        self.assertEqual(
            metadata["version"],
            EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_VERSION,
        )
        self.assertEqual(
            metadata["registration_status"], "frozen_before_candidate_selection"
        )
        self.assertFalse(metadata["candidate_selection_started"])
        self.assertEqual(sorted(metadata["fingerprint_universe"]), frozen_8fp_universe)
        # Supersession: the frozen 8fp universe is a strict subset of the live 12fp
        # registry (the split only added the four metal sub-families, removed none).
        self.assertTrue(set(frozen_8fp_universe) < set(live_fingerprints))
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

    def test_28fp_pre_registration_is_frozen_for_live_universe(self) -> None:
        # The re-frozen 28fp tranche pre-registration is the current prerequisite: the
        # nucleoside diphosphate kinase setup adds one positive fingerprint (universe 27 -> 28),
        # so the prior 27fp re-freeze is itself superseded. This artifact is frozen before
        # selection against the CURRENT 28-fingerprint universe and records the bumped ontology
        # version.
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_28FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(live_fingerprints), 28)
        self.assertEqual(sorted(metadata["fingerprint_universe"]), live_fingerprints)
        self.assertEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )
        self.assertEqual(
            metadata["registration_status"], "frozen_before_candidate_selection"
        )
        self.assertFalse(metadata["candidate_selection_started"])
        self.assertEqual(
            metadata["version"],
            EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_VERSION,
        )
        self.assertEqual(
            metadata["supersedes"],
            "v3_external_hard_negative_next_tranche_preregistration_27fp_1025.json",
        )

    def test_27fp_pre_registration_now_superseded_by_28fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_27FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 27)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_26fp_pre_registration_now_superseded_by_27fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_26FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 26)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_25fp_pre_registration_now_superseded_by_26fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_25FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 25)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_24fp_pre_registration_now_superseded_by_25fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_24FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 24)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_23fp_pre_registration_now_superseded_by_24fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_23FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 23)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_22fp_pre_registration_now_superseded_by_23fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_22FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 22)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_21fp_pre_registration_now_superseded_by_22fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_21FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 21)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_20fp_pre_registration_now_superseded_by_21fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_20FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 20)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_19fp_pre_registration_now_superseded_by_20fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_19FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 19)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_18fp_pre_registration_now_superseded_by_19fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_18FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 18)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_17fp_pre_registration_now_superseded_by_18fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_17FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 17)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_16fp_pre_registration_now_superseded_by_17fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_16FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 16)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_15fp_pre_registration_now_superseded_by_16fp(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_15FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 15)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_14fp_pre_registration_now_superseded_by_15fp(self) -> None:
        # After the 14 -> 15 -> 16 expansions the 14fp re-freeze is itself stale: its inverse-gate
        # universe (14) is now a strict subset of the live fingerprint registry, and its
        # ontology version no longer matches CURRENT. It is kept on disk only as history.
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_14FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 14)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_12fp_pre_registration_remains_superseded(self) -> None:
        artifact = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_12FP_ARTIFACT)
        metadata = artifact["metadata"]
        live_fingerprints = sorted(fp.id for fp in load_fingerprints())
        self.assertEqual(len(metadata["fingerprint_universe"]), 12)
        self.assertTrue(set(metadata["fingerprint_universe"]) < set(live_fingerprints))
        self.assertNotEqual(
            metadata["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )

    def test_factory_import_gate_accepts_frozen_preregistration(self) -> None:
        # Happy path: the re-frozen 28fp pre-registration (current universe + bumped
        # ontology version) is accepted by the import gate. The stale 8fp/12fp artifacts are
        # blocked (see test_factory_import_gate_blocks_stale_preregistration_after_split).
        prereg = _load_json(ROOT / EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_28FP_ARTIFACT)
        gate = build_external_hard_negative_next_candidate_factory_import_gate(
            terminal_review_decisions=_terminal_review_decisions(),
            label_factory_gate_check=_passed_label_factory_gate(),
            external_transfer_gate=_passed_external_transfer_gate(),
            existing_label_entry_ids=[],
            max_imports=1,
            pre_registration=prereg,
            pre_registration_artifact_path=(
                EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_28FP_ARTIFACT
            ),
            require_pre_registration=True,
        )

        self.assertTrue(gate["metadata"]["ready_for_label_import"])
        self.assertEqual(gate["metadata"]["selected_import_accessions"], ["PTEST"])
        self.assertEqual(
            gate["metadata"]["pre_registration_reference"]["version"],
            EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_VERSION,
        )
        self.assertEqual(
            gate["metadata"]["pre_registration_reference"]["ontology_version_at_decision"],
            CURRENT_POSITIVE_FINGERPRINT_UNIVERSE_VERSION,
        )
        self.assertEqual(gate["rows"][0]["remaining_import_blockers"], [])
        separation = gate["rows"][0]["evidence_separation"]
        self.assertIn("predictive_evidence", separation)
        self.assertIn("import_gate_evidence", separation)
        self.assertIn("review_only_context", separation)
        self.assertIn("excluded_context", separation)

    def test_factory_import_gate_blocks_stale_preregistration_after_split(self) -> None:
        # The on-disk 8fp pre-registration predates the Stage-2 metal_dependent_hydrolase
        # v2 split. Expanding the positive fingerprint universe MUST invalidate it: BOTH the
        # gate's universe-match check AND the bumped ontology-version check fire, proving an
        # OOS hard-negative tranche cannot be imported against a stale (smaller, 8fp)
        # inverse-gate universe. The re-frozen 12fp artifact is the supersessor.
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

        self.assertFalse(gate["metadata"]["ready_for_label_import"])
        blockers = gate["rows"][0]["remaining_import_blockers"]
        self.assertIn(
            "external_hard_negative_pre_registration_fingerprint_mismatch", blockers
        )
        self.assertIn(
            "external_hard_negative_pre_registration_ontology_mismatch", blockers
        )

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
        self.assertEqual(
            set(row["entry_id"] for row in plan["rows"]),
            EXTERNAL_HARD_NEGATIVES,
        )
        for row in plan["rows"]:
            self.assertEqual(row["reaudit_status"], "planned_not_scored")
            self.assertTrue(row["current_label_contract_valid"])
            self.assertTrue(row["evidence_separation_valid"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_chain_ligand_acceptor_disambiguation_stays_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_chain_ligand_acceptor_disambiguation_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_chain_ligand_acceptor_disambiguation_audit",
        )
        self.assertTrue(metadata["feature_passes_current_review_controls"])
        self.assertEqual(metadata["current_positive_feature_hit_count"], 3)
        self.assertEqual(metadata["negative_control_row_count"], 25)
        self.assertEqual(metadata["negative_control_same_chain_block_count"], 11)
        self.assertEqual(
            metadata["negative_control_broader_chain_context_block_count"],
            2,
        )
        self.assertEqual(metadata["negative_control_chain_context_block_count"], 13)
        self.assertEqual(metadata["negative_control_false_hit_count"], 0)
        self.assertEqual(metadata["external_hard_negative_abstention_row_count"], 3)
        self.assertFalse(metadata["feature_admissible_for_production_scoring"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        external_rows = {
            row["entry_id"]
            for row in audit["rows"]
            if row["row_type"] == "imported_external_hard_negative"
        }
        self.assertEqual(external_rows, EXTERNAL_HARD_NEGATIVES)

    def test_epk_chain_ligand_external_feature_screen_is_not_reaudit(
        self,
    ) -> None:
        screen = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_chain_ligand_external_hard_negative_feature_screen_1025.json"
        )
        metadata = screen["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_chain_ligand_external_hard_negative_feature_screen",
        )
        self.assertTrue(metadata["review_only_feature_screen_complete"])
        self.assertTrue(metadata["review_only_feature_screen_passed"])
        self.assertEqual(
            metadata[
                "review_only_external_hard_negative_feature_non_abstention_count"
            ],
            0,
        )
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["clean_heldout_performance_claim_permitted"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(
            {row["entry_id"] for row in screen["rows"]},
            EXTERNAL_HARD_NEGATIVES,
        )
        for row in screen["rows"]:
            self.assertEqual(row["review_only_feature_score"], 0.0)
            self.assertFalse(row["external_hard_negative_reaudit_scored"])

    def test_epk_protein_substrate_acceptor_candidate_fails_closed(self) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_protein_substrate_acceptor_candidate_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_protein_substrate_acceptor_candidate_audit",
        )
        self.assertEqual(
            metadata["candidate_feature_id"],
            "protein_substrate_non_catalytic_chain_acceptor_v0",
        )
        self.assertEqual(
            metadata["candidate_feature_status"],
            "blocked_review_only_positive_coverage_gap",
        )
        self.assertEqual(metadata["current_positive_feature_hit_count"], 2)
        self.assertEqual(metadata["current_positive_feature_miss_count"], 1)
        self.assertEqual(metadata["ligand_analog_only_positive_miss_count"], 1)
        self.assertEqual(
            metadata["ligand_analog_only_positive_miss_entry_ids"],
            ["m_csa:640"],
        )
        self.assertEqual(metadata["negative_control_row_count"], 25)
        self.assertEqual(metadata["negative_control_false_hit_count"], 0)
        self.assertEqual(
            metadata["external_hard_negative_feature_abstention_count"],
            3,
        )
        self.assertFalse(metadata["feature_passes_current_review_controls"])
        self.assertFalse(metadata["feature_admissible_for_production_scoring"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        external_rows = {
            row["entry_id"]
            for row in audit["rows"]
            if row["row_type"] == "imported_external_hard_negative"
        }
        self.assertEqual(external_rows, EXTERNAL_HARD_NEGATIVES)

    def test_epk_ligand_analog_policy_blocker_stays_review_only(self) -> None:
        decision = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_analog_policy_blocker_decision_1025.json"
        )
        metadata = decision["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_ligand_analog_policy_blocker_decision",
        )
        self.assertEqual(metadata["ligand_analog_dependency_count"], 1)
        self.assertEqual(metadata["ligand_analog_dependency_entry_ids"], ["m_csa:640"])
        self.assertEqual(
            metadata["ligand_analog_policy_decision"],
            "do_not_use_ligand_analog_as_production_acceptor_evidence",
        )
        self.assertEqual(metadata["ligand_analog_production_admissible_count"], 0)
        self.assertTrue(metadata["protein_substrate_positive_coverage_gap"])
        self.assertFalse(metadata["feature_admissible_for_production_scoring"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["entry_id"]: row for row in decision["rows"]}
        self.assertEqual(set(rows), {"m_csa:640"})
        self.assertEqual(rows["m_csa:640"]["acceptor_ligand_code"], "B31")
        self.assertFalse(
            rows["m_csa:640"][
                "ligand_analog_evidence_admissible_for_production_scoring"
            ]
        )

    def test_epk_protein_substrate_positive_source_triage_stays_review_only(
        self,
    ) -> None:
        triage = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_protein_substrate_positive_source_triage_1025.json"
        )
        metadata = triage["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_protein_substrate_positive_source_triage",
        )
        self.assertEqual(metadata["candidate_row_count"], 3)
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertEqual(metadata["product_state_repair_candidate_count"], 1)
        self.assertEqual(
            metadata["product_state_repair_candidate_entry_ids"],
            ["m_csa:760"],
        )
        self.assertEqual(metadata["recommended_next_entry_id"], "m_csa:760")
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["entry_id"]: row for row in triage["rows"]}
        self.assertEqual(set(rows), {"m_csa:756", "m_csa:757", "m_csa:760"})
        self.assertEqual(
            rows["m_csa:760"]["triage_decision"],
            "product_state_atp_repair_candidate_review_only",
        )
        self.assertTrue(rows["m_csa:760"]["has_product_state_nucleotide"])
        for row in rows.values():
            self.assertTrue(row["review_only"])
            self.assertFalse(row["measurement_ready"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertTrue(row["review_context_only_used_for_sourcing"])
        expanded = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_protein_substrate_positive_source_triage_expanded_1025.json"
        )
        preview = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_protein_substrate_positive_source_triage_1025_preview.json"
        )
        expanded_metadata = expanded["metadata"]
        self.assertEqual(
            expanded_metadata["method"],
            "epk_protein_substrate_positive_source_triage",
        )
        self.assertEqual(expanded_metadata["candidate_row_count"], 3)
        self.assertEqual(expanded_metadata["measurement_ready_candidate_count"], 0)
        self.assertFalse(
            expanded_metadata["ready_to_expand_positive_fingerprint_universe"]
        )
        expanded_rows = {row["entry_id"]: row for row in expanded["rows"]}
        self.assertEqual(set(expanded_rows), set(rows))
        preview_rows = {row["entry_id"]: row for row in preview["rows"]}
        self.assertEqual(set(preview_rows), set(rows))
        self.assertTrue(
            all(row["review_only"] for row in expanded_rows.values())
        )
        self.assertTrue(
            all(
                not row["countable_label_candidate"]
                for row in expanded_rows.values()
            )
        )

    def test_epk_m_csa760_atp_state_repair_scan_stays_review_only(self) -> None:
        scan = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_m_csa760_atp_state_repair_scan_1025.json"
        )
        metadata = scan["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_m_csa760_atp_state_repair_scan",
        )
        self.assertEqual(metadata["entry_id"], "m_csa:760")
        self.assertEqual(metadata["candidate_pdb_count"], 5)
        self.assertEqual(
            metadata["atp_metal_state_candidate_pdb_ids"],
            ["1TID", "1TIL"],
        )
        self.assertEqual(
            metadata["protein_substrate_acceptor_context_candidate_pdb_ids"],
            ["1TH8", "1THN"],
        )
        self.assertEqual(
            metadata["combined_atp_metal_substrate_context_candidate_count"],
            0,
        )
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertTrue(metadata["split_state_blocker_detected"])
        self.assertEqual(
            metadata["repair_status"],
            "blocked_review_only_split_atp_and_substrate_context",
        )
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["pdb_id"]: row for row in scan["rows"]}
        self.assertEqual(set(rows), {"1L0O", "1TH8", "1THN", "1TID", "1TIL"})
        for pdb_id in ["1TID", "1TIL"]:
            self.assertEqual(
                rows[pdb_id]["repair_scan_decision"],
                "atp_metal_state_without_protein_substrate_acceptor_review_only",
            )
            self.assertFalse(rows[pdb_id]["measurement_ready"])
        for pdb_id in ["1TH8", "1THN"]:
            self.assertEqual(
                rows[pdb_id]["repair_scan_decision"],
                "substrate_acceptor_product_state_no_gamma_review_only",
            )
            self.assertFalse(rows[pdb_id]["measurement_ready"])

    def test_epk_m_csa757_active_state_repair_scan_stays_review_only(
        self,
    ) -> None:
        scan = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_m_csa757_active_state_repair_scan_1025.json"
        )
        metadata = scan["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_m_csa757_active_state_repair_scan",
        )
        self.assertEqual(metadata["entry_id"], "m_csa:757")
        self.assertEqual(metadata["candidate_pdb_count"], 105)
        self.assertEqual(metadata["scanned_candidate_pdb_count"], 25)
        self.assertEqual(
            metadata["active_state_atp_metal_candidate_pdb_ids"],
            ["1CDK", "1Q24"],
        )
        self.assertEqual(
            metadata["conservative_active_state_atp_metal_candidate_pdb_ids"],
            ["1Q24"],
        )
        self.assertEqual(
            metadata["homomeric_mapping_ambiguous_active_state_candidate_pdb_ids"],
            ["1CDK"],
        )
        self.assertEqual(
            metadata["mapped_protein_substrate_acceptor_candidate_count"],
            0,
        )
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertEqual(
            metadata["repair_status"],
            "blocked_review_only_active_state_without_mapped_substrate_acceptor",
        )
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["pdb_id"]: row for row in scan["rows"]}
        self.assertEqual(
            rows["1CDK"]["repair_scan_decision"],
            "homomeric_active_state_mapping_ambiguous_no_substrate_acceptor_review_only",
        )
        self.assertEqual(
            rows["1Q24"]["repair_scan_decision"],
            "active_state_atp_metal_with_structure_phosphoacceptor_not_substrate_mapped_review_only",
        )
        for row in rows.values():
            self.assertTrue(row["review_only"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["measurement_ready"])

    def test_epk_m_csa756_active_state_repair_scan_stays_review_only(
        self,
    ) -> None:
        scan = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_m_csa756_active_state_repair_scan_1025.json"
        )
        metadata = scan["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_m_csa756_active_state_repair_scan",
        )
        self.assertEqual(metadata["entry_id"], "m_csa:756")
        self.assertEqual(metadata["candidate_pdb_count"], 15)
        self.assertEqual(metadata["scanned_candidate_pdb_count"], 15)
        self.assertEqual(metadata["active_state_atp_metal_candidate_count"], 0)
        self.assertEqual(
            metadata["mapped_protein_substrate_acceptor_candidate_count"],
            0,
        )
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertEqual(
            metadata["repair_status"],
            "blocked_review_only_no_active_state_atp_metal_context",
        )
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["pdb_id"]: row for row in scan["rows"]}
        self.assertEqual(
            rows["5LI1"]["repair_scan_decision"],
            "structure_active_state_ligand_mapping_unresolved_review_only",
        )
        for row in rows.values():
            self.assertTrue(row["review_only"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["measurement_ready"])

    def test_epk_protein_substrate_source_repair_terminal_decision_stays_review_only(
        self,
    ) -> None:
        decision = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_protein_substrate_source_repair_terminal_decision_1025.json"
        )
        metadata = decision["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_protein_substrate_source_repair_terminal_decision",
        )
        self.assertEqual(
            metadata["source_candidate_entry_ids"],
            ["m_csa:760", "m_csa:757", "m_csa:756"],
        )
        self.assertTrue(metadata["current_source_candidates_exhausted"])
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertEqual(
            metadata["terminal_decision"],
            "current_source_candidates_exhausted_review_only",
        )
        self.assertEqual(
            metadata["recommended_next_experiment"],
            "pre_register_ligand_analog_or_product_state_policy_or_source_new_epk_positive",
        )
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["entry_id"]: row for row in decision["rows"]}
        self.assertEqual(
            rows["m_csa:760"]["decision"],
            "terminal_split_state_blocked_review_only",
        )
        self.assertEqual(
            rows["m_csa:757"]["decision"],
            "terminal_active_state_without_mapped_acceptor_review_only",
        )
        self.assertEqual(
            rows["m_csa:756"]["decision"],
            "terminal_no_conservative_active_state_context_review_only",
        )
        for row in rows.values():
            self.assertTrue(row["review_only"])
            self.assertFalse(row["countable_label_candidate"])
        expanded = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_protein_substrate_source_repair_terminal_decision_expanded_1025.json"
        )
        expanded_metadata = expanded["metadata"]
        self.assertEqual(
            expanded_metadata["method"],
            "epk_protein_substrate_source_repair_terminal_decision",
        )
        self.assertEqual(
            expanded_metadata["terminal_decision"],
            "current_source_candidates_exhausted_review_only",
        )
        self.assertEqual(expanded_metadata["measurement_ready_candidate_count"], 0)
        self.assertTrue(expanded_metadata["current_source_candidates_exhausted"])
        self.assertFalse(
            expanded_metadata["ready_to_expand_positive_fingerprint_universe"]
        )
        expanded_rows = {row["entry_id"]: row for row in expanded["rows"]}
        self.assertEqual(set(expanded_rows), set(rows))
        self.assertTrue(
            all(row["review_only"] for row in expanded_rows.values())
        )
        self.assertTrue(
            all(
                not row["countable_label_candidate"]
                for row in expanded_rows.values()
            )
        )

    def test_epk_analog_product_state_policy_preregistration_stays_inactive(
        self,
    ) -> None:
        preregistration = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_analog_product_state_policy_preregistration_1025.json"
        )
        metadata = preregistration["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_analog_product_state_policy_preregistration",
        )
        self.assertEqual(
            metadata["policy_status"],
            "draft_preregistered_review_only_not_activated",
        )
        self.assertFalse(metadata["policy_activation_allowed"])
        self.assertFalse(metadata["production_scoring_admissible"])
        self.assertEqual(metadata["failed_activation_requirement_count"], 3)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["criterion_id"]: row for row in preregistration["rows"]}
        self.assertFalse(
            rows["freeze_policy_before_candidate_selection"][
                "production_use_allowed"
            ]
        )
        self.assertFalse(
            rows["require_external_hard_negative_scored_reaudit"]["passed"]
        )
        self.assertTrue(
            rows["reject_product_state_without_gamma_geometry"]["passed"]
        )

    def test_epk_analog_product_state_policy_activation_audit_fails_closed(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_analog_product_state_policy_activation_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_analog_product_state_policy_activation_audit",
        )
        self.assertEqual(metadata["policy_activation_status"], "blocked_review_only")
        self.assertFalse(metadata["policy_activation_allowed"])
        self.assertFalse(metadata["production_scoring_admissible"])
        self.assertEqual(metadata["failed_activation_requirement_count"], 7)
        self.assertEqual(metadata["diagnostic_control_pass_count"], 2)
        self.assertFalse(
            metadata["protein_substrate_positive_coverage_without_ligand_analog"]
        )
        self.assertEqual(metadata["ligand_analog_dependency_entry_ids"], ["m_csa:640"])
        self.assertEqual(metadata["ligand_analog_production_admissible_count"], 0)
        self.assertEqual(
            metadata["source_repair_measurement_ready_candidate_count"], 0
        )
        self.assertTrue(
            metadata["sibling_controls_remain_blocked_under_candidate_feature"]
        )
        self.assertTrue(
            metadata["imported_external_hard_negative_feature_screen_clear"]
        )
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["criterion_id"]: row for row in audit["rows"]}
        self.assertFalse(rows["policy_frozen_before_activation"]["passed"])
        self.assertFalse(rows["ligand_analog_dependency_resolved"]["passed"])
        self.assertFalse(rows["calibrated_epk_score_exists"]["passed"])
        self.assertTrue(
            rows["imported_external_hard_negative_feature_screen_clear"]["passed"]
        )

    def test_epk_analog_product_state_policy_control_reaudit_stays_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_analog_product_state_policy_control_reaudit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_analog_product_state_policy_control_reaudit",
        )
        self.assertEqual(
            metadata["policy_status"], "review_only_reaudit_not_activated"
        )
        self.assertFalse(metadata["policy_activation_allowed"])
        self.assertFalse(metadata["production_scoring_admissible"])
        self.assertEqual(metadata["current_positive_policy_hit_count"], 3)
        self.assertEqual(metadata["ligand_analog_positive_policy_hit_count"], 1)
        self.assertEqual(metadata["sibling_control_policy_false_hit_count"], 0)
        self.assertTrue(metadata["sibling_family_control_reaudit_passed"])
        self.assertEqual(
            metadata["external_hard_negative_feature_non_abstention_count"], 0
        )
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertIn(
            "external_hard_negative_scored_reaudit",
            metadata["failed_activation_requirement_ids"],
        )
        decisions = {row.get("policy_reaudit_decision") for row in audit["rows"]}
        self.assertIn("policy_positive_ligand_analog_hit_review_only", decisions)
        self.assertIn(
            "policy_source_repair_blocked_by_exclusion_or_missing_geometry",
            decisions,
        )

    def test_epk_review_only_external_hard_negative_score_probe_stays_review_only(
        self,
    ) -> None:
        probe = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_review_only_external_hard_negative_score_probe_1025.json"
        )
        metadata = probe["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_review_only_external_hard_negative_score_probe",
        )
        self.assertEqual(metadata["external_hard_negative_score_probe_row_count"], 3)
        self.assertTrue(metadata["review_only_score_probe_complete"])
        self.assertTrue(metadata["review_only_score_probe_passed"])
        self.assertEqual(metadata["review_only_score_probe_non_abstention_count"], 0)
        self.assertEqual(metadata["missing_expected_external_hard_negative_count"], 0)
        self.assertTrue(metadata["not_a_real_scored_reaudit"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["clean_heldout_performance_claim_permitted"])
        self.assertFalse(metadata["policy_activation_allowed"])
        self.assertFalse(metadata["production_scoring_admissible"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["entry_id"]: row for row in probe["rows"]}
        self.assertEqual(
            set(rows),
            {"uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"},
        )
        self.assertTrue(
            all(
                not row["review_only_score_probe_non_abstention"]
                for row in rows.values()
            )
        )
        self.assertTrue(all(row["review_only"] for row in rows.values()))
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in rows.values())
        )

    def test_epk_m_csa756_5li1_residue_evidence_audit_stays_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_m_csa756_5li1_residue_evidence_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_m_csa756_5li1_residue_evidence_audit",
        )
        self.assertEqual(metadata["entry_id"], "m_csa:756")
        self.assertEqual(metadata["pdb_id"], "5LI1")
        self.assertTrue(metadata["active_site_residue_evidence_found"])
        self.assertEqual(metadata["candidate_residue_resolved_count"], 3)
        self.assertEqual(metadata["local_ligand_codes"], ["ANP", "MG"])
        self.assertFalse(metadata["terminal_gamma_atom_detected"])
        self.assertEqual(
            metadata["noncanonical_terminal_atom_names_detected"], ["PB"]
        )
        self.assertFalse(
            metadata["noncanonical_terminal_atom_policy_admissible"]
        )
        self.assertFalse(metadata["explicit_residue_source_authority_sufficient"])
        self.assertEqual(
            metadata["structure_phosphoacceptor_like_context_count"], 3
        )
        self.assertEqual(
            metadata["mapped_protein_substrate_acceptor_candidate_count"], 0
        )
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertEqual(
            metadata["repair_status"],
            "blocked_review_only_residue_evidence_lacks_terminal_gamma_atom_no_mapped_acceptor",
        )
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        residue_rows = [
            row
            for row in audit["rows"]
            if row["row_type"] == "candidate_active_site_residue"
        ]
        self.assertEqual(len(residue_rows), 3)
        self.assertTrue(all(row["review_only"] for row in residue_rows))
        self.assertTrue(all(row["residue_resolved"] for row in residue_rows))

    def test_epk_external_protein_substrate_source_scout_stays_review_only(
        self,
    ) -> None:
        scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_protein_substrate_source_scout_1025.json"
        )
        metadata = scout["metadata"]
        self.assertEqual(
            metadata["method"], "epk_external_protein_substrate_source_scout"
        )
        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["current_source_candidates_exhausted"])
        self.assertEqual(metadata["sourced_candidate_count"], 8)
        self.assertEqual(metadata["entry_feature_record_available_count"], 16)
        self.assertEqual(metadata["query_fetch_failure_count"], 0)
        self.assertEqual(metadata["entry_feature_fetch_failure_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(
            metadata["existing_external_label_entry_ids_checked"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(
            metadata["source_scout_status_counts"],
            {
                "blocked_active_site_source_missing": 1,
                "sourced_pending_structure_mapping_review": 8,
            },
        )
        self.assertIn(
            "external_positive_structure_mapping_required",
            metadata["blocker_not_removed"],
        )
        sourced = [
            row
            for row in scout["rows"]
            if row["sourcing_status"]
            == "sourced_pending_structure_mapping_review"
        ]
        self.assertEqual(len(sourced), 8)
        self.assertTrue(all(not row["countable_label_candidate"] for row in sourced))
        self.assertTrue(
            all(
                row["protein_phosphotransfer_catalytic_activity_count"] > 0
                for row in sourced
            )
        )

    def test_epk_external_source_structure_mapping_review_stays_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_structure_mapping_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"], "epk_external_source_structure_mapping_review"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_candidate_count"], 8)
        self.assertEqual(metadata["structure_row_count"], 16)
        self.assertEqual(metadata["direct_position_mapping_ready_structure_count"], 9)
        self.assertEqual(metadata["active_state_mapping_ready_structure_count"], 5)
        self.assertEqual(metadata["active_state_mapping_ready_accessions"], ["Q8IVT5"])
        self.assertEqual(
            metadata["active_state_mapping_ready_pdb_ids"],
            ["7JUW", "7JUX", "7JUY", "7JV0", "7JV1"],
        )
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            metadata["mapping_review_status_counts"],
            {
                "active_state_mapping_ready_needs_acceptor_source_review_only": 5,
                "blocked_direct_position_mapping_ambiguous_or_missing_review_only": 7,
                "direct_position_mapping_ready_ligand_context_incomplete_review_only": 4,
            },
        )
        ready_rows = [
            row
            for row in review["rows"]
            if row["mapping_review_status"]
            == "active_state_mapping_ready_needs_acceptor_source_review_only"
        ]
        self.assertEqual(
            {row["pdb_id"] for row in ready_rows},
            {"7JUW", "7JUX", "7JUY", "7JV0", "7JV1"},
        )
        self.assertTrue(
            all(row["local_ligand_codes"] == ["ANP", "MG"] for row in ready_rows)
        )
        self.assertTrue(
            all("metal_ion" in row["local_cofactor_families"] for row in ready_rows)
        )
        self.assertTrue(
            all(
                "protein_substrate_acceptor_not_source_mapped"
                in row["remaining_blockers"]
                for row in ready_rows
            )
        )

    def test_epk_external_source_acceptor_gap_audit_stays_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_acceptor_gap_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"], "epk_external_source_acceptor_gap_audit"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["active_state_mapping_ready_input_count"], 5)
        self.assertEqual(metadata["audited_structure_count"], 5)
        self.assertEqual(metadata["source_mapped_acceptor_count"], 0)
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            metadata["acceptor_gap_status_counts"],
            {
                "acceptor_like_geometry_not_source_mapped_review_only": 3,
                "no_acceptor_like_hydroxyl_within_threshold_review_only": 2,
            },
        )
        rows = {row["pdb_id"]: row for row in audit["rows"]}
        self.assertEqual(set(rows), {"7JUW", "7JUX", "7JUY", "7JV0", "7JV1"})
        self.assertEqual(
            {
                pdb_id
                for pdb_id, row in rows.items()
                if row["acceptor_gap_status"]
                == "acceptor_like_geometry_not_source_mapped_review_only"
            },
            {"7JUW", "7JUY", "7JV0"},
        )
        self.assertEqual(
            {
                pdb_id
                for pdb_id, row in rows.items()
                if row["acceptor_gap_status"]
                == "no_acceptor_like_hydroxyl_within_threshold_review_only"
            },
            {"7JUX", "7JV1"},
        )
        self.assertTrue(
            all(
                "protein_substrate_acceptor_not_source_mapped"
                in row["remaining_blockers"]
                for row in rows.values()
            )
        )

    def test_epk_external_source_next_experiment_queue_stays_review_only(
        self,
    ) -> None:
        queue = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_next_experiment_queue_1025.json"
        )
        metadata = queue["metadata"]
        self.assertEqual(
            metadata["method"], "epk_external_source_next_experiment_queue"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["queued_structure_count"], 16)
        self.assertEqual(
            metadata["top_priority_next_experiment"],
            "source_map_nearby_candidate_acceptor",
        )
        self.assertEqual(metadata["top_priority_accession"], "Q8IVT5")
        self.assertEqual(metadata["top_priority_pdb_id"], "7JUW")
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            metadata["queue_status_counts"],
            {
                "active_state_no_acceptor_candidate_review_only": 2,
                "highest_value_acceptor_source_mapping_review_only": 3,
                "mapped_structure_ligand_context_incomplete_review_only": 4,
                "structure_mapping_unresolved_review_only": 7,
            },
        )
        self.assertEqual(queue["rows"][0]["pdb_id"], "7JUW")
        self.assertEqual(
            queue["rows"][0]["queue_status"],
            "highest_value_acceptor_source_mapping_review_only",
        )
        self.assertTrue(all(row["review_only"] for row in queue["rows"]))
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in queue["rows"])
        )

    def test_epk_external_source_acceptor_source_mapping_stays_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_acceptor_source_mapping_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_external_source_acceptor_source_mapping_review",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_acceptor_candidate_count"], 5)
        self.assertEqual(metadata["source_mapped_acceptor_count"], 0)
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            metadata["source_mapping_status_counts"],
            {"terminal_acceptor_candidate_not_source_mapped_review_only": 5},
        )
        rows = {row["pdb_id"]: row for row in review["rows"]}
        self.assertEqual(set(rows), {"7JUW", "7JUX", "7JUY", "7JV0", "7JV1"})
        self.assertEqual(
            {
                pdb_id
                for pdb_id, row in rows.items()
                if row["candidate_within_measurement_threshold"]
            },
            {"7JUW", "7JUY", "7JV0"},
        )
        for row in rows.values():
            self.assertEqual(row["candidate_residue_code"], "SER")
            self.assertEqual(row["candidate_auth_seq_id"], "194")
            self.assertEqual(row["acceptor_chain_accession"], "P29678")
            self.assertEqual(row["acceptor_uniprot_position"], 194)
            self.assertEqual(row["source_phospho_feature_exact_match_count"], 0)
            self.assertFalse(row["measurement_ready"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_external_source_alternate_cocomplex_review_stays_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_q8ivt5_alternate_cocomplex_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"], "epk_external_source_alternate_cocomplex_review"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["target_accession"], "Q8IVT5")
        self.assertEqual(
            metadata["acceptor_accessions_reviewed"], ["P29678", "Q02750"]
        )
        self.assertEqual(metadata["reviewed_pdb_count"], 8)
        self.assertEqual(metadata["active_state_structure_count"], 6)
        self.assertEqual(metadata["target_mapping_unambiguous_structure_count"], 6)
        self.assertEqual(metadata["source_mapped_phosphoacceptor_candidate_count"], 16)
        self.assertEqual(metadata["source_phosphoacceptor_within_threshold_count"], 0)
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            metadata["alternate_cocomplex_status_counts"],
            {
                "inactive_or_incomplete_active_state_review_only": 2,
                "source_phosphoacceptor_geometry_outside_threshold_review_only": 6,
            },
        )
        self.assertGreater(
            metadata["nearest_source_phosphoacceptor_distance_angstrom"], 6.0
        )
        rows = {row["pdb_id"]: row for row in review["rows"]}
        self.assertEqual(
            {
                pdb_id
                for pdb_id, row in rows.items()
                if row["alternate_cocomplex_status"]
                == "source_phosphoacceptor_geometry_outside_threshold_review_only"
            },
            {"7JUW", "7JUX", "7JUY", "7JV0", "7JV1", "9AXH"},
        )
        self.assertTrue(all(row["review_only"] for row in review["rows"]))
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in review["rows"])
        )

    def test_epk_external_source_lower_priority_ligand_review_stays_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_lower_priority_ligand_sourcing_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_external_source_lower_priority_ligand_sourcing_review",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_row_count"], 4)
        self.assertEqual(metadata["active_gamma_metal_current_structure_count"], 0)
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            metadata["ligand_sourcing_status_counts"],
            {
                "gamma_without_metal_needs_alternate_review_only": 1,
                "inactive_analog_metal_only_needs_policy_or_alternate_review_only": 1,
                "metal_without_gamma_needs_alternate_review_only": 1,
                "no_ligand_context_needs_alternate_review_only": 1,
            },
        )
        rows = {row["accession"]: row for row in review["rows"]}
        self.assertEqual(
            rows["Q5TCX8"]["ligand_sourcing_status"],
            "inactive_analog_metal_only_needs_policy_or_alternate_review_only",
        )
        self.assertEqual(
            rows["Q8IVT5"]["ligand_sourcing_status"],
            "gamma_without_metal_needs_alternate_review_only",
        )
        self.assertTrue(all(row["review_only"] for row in review["rows"]))
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in review["rows"])
        )

    def test_epk_external_source_second_pass_scout_stays_review_only(
        self,
    ) -> None:
        scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_protein_substrate_source_scout_second_pass_1025.json"
        )
        metadata = scout["metadata"]
        self.assertEqual(
            metadata["method"], "epk_external_protein_substrate_source_scout"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["sourced_candidate_count"], 8)
        self.assertEqual(metadata["entry_feature_record_available_count"], 24)
        self.assertEqual(metadata["query_fetch_failure_count"], 0)
        self.assertEqual(metadata["entry_feature_fetch_failure_count"], 0)
        self.assertEqual(
            metadata["sourced_candidate_accessions"],
            [
                "O00506",
                "O60307",
                "O94768",
                "Q15772",
                "Q59H18",
                "Q8IXL6",
                "Q8N2I9",
                "Q8WU08",
            ],
        )
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])

    def test_epk_external_source_second_pass_mapping_fails_closed(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_structure_mapping_review_second_pass_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"], "epk_external_source_structure_mapping_review"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_candidate_count"], 8)
        self.assertEqual(metadata["structure_row_count"], 20)
        self.assertEqual(metadata["active_state_mapping_ready_structure_count"], 0)
        self.assertEqual(metadata["direct_position_mapping_ready_structure_count"], 9)
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(
            metadata["mapping_review_status_counts"],
            {
                "blocked_direct_position_mapping_ambiguous_or_missing_review_only": 11,
                "direct_position_mapping_ready_ligand_context_incomplete_review_only": 9,
            },
        )

    def test_epk_external_source_second_pass_ligand_review_stays_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_lower_priority_ligand_sourcing_review_second_pass_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_external_source_lower_priority_ligand_sourcing_review",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_row_count"], 9)
        self.assertEqual(metadata["active_gamma_metal_current_structure_count"], 0)
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(
            metadata["ligand_sourcing_status_counts"],
            {
                "gamma_without_metal_needs_alternate_review_only": 1,
                "metal_without_gamma_needs_alternate_review_only": 1,
                "non_atp_or_remote_ligand_context_needs_alternate_review_only": 7,
            },
        )
        self.assertTrue(all(row["review_only"] for row in review["rows"]))
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in review["rows"])
        )

    def test_epk_external_source_third_pass_stays_review_only(
        self,
    ) -> None:
        scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_protein_substrate_source_scout_third_pass_1025.json"
        )
        mapping = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_structure_mapping_review_third_pass_1025.json"
        )
        ligand = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_lower_priority_ligand_sourcing_review_third_pass_1025.json"
        )
        self.assertEqual(scout["metadata"]["sourced_candidate_count"], 8)
        self.assertEqual(scout["metadata"]["entry_feature_fetch_failure_count"], 0)
        self.assertEqual(mapping["metadata"]["structure_row_count"], 27)
        self.assertEqual(
            mapping["metadata"]["active_state_mapping_ready_structure_count"], 0
        )
        self.assertEqual(
            mapping["metadata"]["direct_position_mapping_ready_structure_count"], 13
        )
        self.assertEqual(ligand["metadata"]["reviewed_row_count"], 13)
        self.assertEqual(
            ligand["metadata"]["active_gamma_metal_current_structure_count"], 0
        )
        self.assertEqual(ligand["metadata"]["measurement_ready_candidate_count"], 0)
        self.assertFalse(ligand["metadata"]["ready_to_run_epk_scorer"])
        self.assertFalse(ligand["metadata"]["external_hard_negative_reaudit_scored"])
        self.assertFalse(ligand["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(ligand["metadata"]["curated_label_registry_edited"])
        self.assertEqual(ligand["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            ligand["metadata"]["ligand_sourcing_status_counts"],
            {
                "metal_without_gamma_needs_alternate_review_only": 1,
                "non_atp_or_remote_ligand_context_needs_alternate_review_only": 12,
            },
        )

    def test_epk_external_source_fourth_pass_scout_stays_review_only(
        self,
    ) -> None:
        scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_protein_substrate_source_scout_fourth_pass_1025.json"
        )
        metadata = scout["metadata"]
        self.assertEqual(
            metadata["method"], "epk_external_protein_substrate_source_scout"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["sourced_candidate_count"], 8)
        self.assertEqual(metadata["entry_feature_record_available_count"], 16)
        self.assertEqual(metadata["query_fetch_failure_count"], 0)
        self.assertEqual(metadata["entry_feature_fetch_failure_count"], 0)
        self.assertEqual(
            metadata["sourced_candidate_accessions"],
            [
                "O14730",
                "O60229",
                "P78368",
                "O43353",
                "P08922",
                "P09769",
                "P0C1S8",
                "P14616",
            ],
        )
        self.assertEqual(
            metadata["source_scout_status_counts"],
            {
                "blocked_uniprot_feature_fetch": 16,
                "sourced_pending_structure_mapping_review": 8,
            },
        )
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        for row in scout["rows"]:
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["measurement_ready"])
            self.assertFalse(row["epk_score_computed"])

    def test_epk_external_source_fourth_pass_terminal_decision_stays_review_only(
        self,
    ) -> None:
        mapping = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_structure_mapping_review_fourth_pass_1025.json"
        )
        ligand = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_lower_priority_ligand_sourcing_review_fourth_pass_1025.json"
        )
        decision = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_four_pass_terminal_decision_1025.json"
        )
        self.assertEqual(mapping["metadata"]["structure_row_count"], 37)
        self.assertEqual(
            mapping["metadata"]["active_state_mapping_ready_structure_count"], 0
        )
        self.assertEqual(
            mapping["metadata"]["direct_position_mapping_ready_structure_count"], 8
        )
        self.assertEqual(mapping["metadata"]["measurement_ready_candidate_count"], 0)
        self.assertEqual(ligand["metadata"]["reviewed_row_count"], 8)
        self.assertEqual(
            ligand["metadata"]["active_gamma_metal_current_structure_count"], 0
        )
        self.assertEqual(ligand["metadata"]["measurement_ready_candidate_count"], 0)
        self.assertEqual(
            ligand["metadata"]["ligand_sourcing_status_counts"],
            {
                "metal_without_gamma_needs_alternate_review_only": 3,
                "non_atp_or_remote_ligand_context_needs_alternate_review_only": 5,
            },
        )
        metadata = decision["metadata"]
        self.assertEqual(
            metadata["method"], "epk_external_source_scout_pass_terminal_decision"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["source_pass_count"], 4)
        self.assertEqual(metadata["unique_sourced_candidate_count"], 32)
        self.assertEqual(metadata["total_structure_row_count"], 100)
        self.assertEqual(
            metadata["total_active_state_mapping_ready_structure_count"], 5
        )
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertEqual(
            metadata["terminal_decision"],
            "current_4_pass_external_source_surface_exhausted_review_only",
        )
        self.assertTrue(metadata["current_source_candidates_exhausted"])
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_midlength_protein_role_counteraxis_stays_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_midlength_protein_role_counteraxis_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"], "epk_midlength_protein_role_counteraxis_audit"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["midlength_counteraxis_status"],
            "blocks_current_midlength_false_hit_but_no_broad_positive_review_only",
        )
        self.assertEqual(metadata["blocked_midlength_false_hit_count"], 1)
        self.assertEqual(metadata["blocked_midlength_false_hit_pdb_ids"], ["7B56"])
        self.assertEqual(metadata["residual_protein_role_false_hit_count"], 0)
        self.assertEqual(metadata["source_valid_protein_role_retained_count"], 0)
        self.assertEqual(metadata["source_valid_measured_candidate_count"], 3)
        self.assertEqual(metadata["source_valid_short_or_peptide_mode_count"], 3)
        self.assertEqual(
            metadata["source_valid_short_or_peptide_mode_pdb_ids"],
            ["6Z3R", "8OXM", "8OXO"],
        )
        self.assertEqual(metadata["source_valid_chain_length_unresolved_count"], 0)
        self.assertFalse(metadata["protein_discriminator_generalization_ready"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["pdb_id"]: row for row in audit["rows"]}
        self.assertTrue(rows["7B56"]["midlength_acceptor_counterevidence_hit"])
        self.assertFalse(rows["7B56"]["repaired_protein_role_rule_hit"])
        self.assertTrue(rows["6Z3R"]["short_or_peptide_mode_acceptor_hit"])
        self.assertFalse(rows["6Z3R"]["broad_protein_mode_acceptor_hit"])
        self.assertTrue(all(row["review_only"] for row in audit["rows"]))
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in audit["rows"])
        )

    def test_epk_ligand_specific_active_query_scout_stays_review_only(
        self,
    ) -> None:
        scouts = [
            _load_json(
                ROOT
                / "artifacts"
                / artifact_name
            )
            for artifact_name in [
                "v3_epk_ligand_specific_active_query_candidate_scout_1025.json",
                "v3_epk_ligand_specific_active_query_candidate_scout_round2_1025.json",
                "v3_epk_ligand_specific_active_query_candidate_scout_round3_1025.json",
                "v3_epk_ligand_specific_active_query_candidate_scout_round4_1025.json",
                "v3_epk_ligand_specific_active_query_candidate_scout_round5_1025.json",
            ]
        ]
        total_reviewed = sum(
            int(scout["metadata"]["reviewed_candidate_count"])
            for scout in scouts
        )
        total_hit_structures = sum(
            int(scout["metadata"]["heteromeric_candidate_structure_count"])
            for scout in scouts
        )
        self.assertEqual(total_reviewed, 100)
        self.assertEqual(total_hit_structures, 4)
        for scout in scouts:
            metadata = scout["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_heteromeric_positive_coverage_candidate_scout",
            )
            self.assertTrue(metadata["review_only"])
            self.assertEqual(metadata["input_candidate_count"], 20)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            self.assertFalse(metadata["fingerprint_registry_edited"])
            self.assertFalse(metadata["curated_label_registry_edited"])
            self.assertEqual(metadata["countable_label_candidate_count"], 0)
            self.assertTrue(all(row["review_only"] for row in scout["rows"]))
            self.assertTrue(
                all(not row["countable_label_candidate"] for row in scout["rows"])
            )
        self.assertEqual(
            scouts[0]["metadata"]["candidate_status_counts"],
            {"no_heteromeric_candidate_hit_review_only": 20},
        )
        self.assertEqual(
            scouts[1]["metadata"]["candidate_status_counts"],
            {"no_heteromeric_candidate_hit_review_only": 20},
        )
        self.assertEqual(
            scouts[2]["metadata"]["heteromeric_candidate_pdb_ids"], ["7ZE5"]
        )
        self.assertEqual(
            scouts[3]["metadata"]["heteromeric_candidate_pdb_ids"], ["1IR3"]
        )
        self.assertEqual(
            scouts[4]["metadata"]["heteromeric_candidate_pdb_ids"],
            ["2JJ2", "4HPU"],
        )
        for artifact_name in [
            "v3_epk_ligand_specific_active_query_source_validation_review_round3_1025.json",
            "v3_epk_ligand_specific_active_query_source_validation_review_round4_1025.json",
            "v3_epk_ligand_specific_active_query_source_validation_review_round5_1025.json",
        ]:
            validation = _load_json(ROOT / "artifacts" / artifact_name)
            metadata = validation["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_heteromeric_candidate_source_validation_review",
            )
            self.assertGreaterEqual(metadata["reviewed_candidate_count"], 1)
            self.assertEqual(metadata["source_validated_new_candidate_count"], 0)
            self.assertEqual(
                set(metadata["source_validation_status_counts"]),
                {"blocked_source_context_insufficient_review_only"},
            )
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_external_source_three_pass_terminal_decision_stays_review_only(
        self,
    ) -> None:
        decision = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_source_three_pass_terminal_decision_1025.json"
        )
        metadata = decision["metadata"]
        self.assertEqual(
            metadata["method"], "epk_external_source_scout_pass_terminal_decision"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["source_pass_count"], 3)
        self.assertEqual(metadata["unique_sourced_candidate_count"], 24)
        self.assertEqual(metadata["total_sourced_candidate_rows"], 24)
        self.assertEqual(metadata["total_structure_row_count"], 63)
        self.assertEqual(metadata["total_active_state_mapping_ready_structure_count"], 5)
        self.assertEqual(
            metadata["alternate_cocomplex_source_phosphoacceptor_within_threshold_count"],
            0,
        )
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertEqual(
            metadata["terminal_decision"],
            "current_three_pass_external_source_surface_exhausted_review_only",
        )
        self.assertTrue(metadata["current_source_candidates_exhausted"])
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(len(decision["rows"]), 3)
        self.assertTrue(all(row["review_only"] for row in decision["rows"]))

    def test_epk_ligand_specific_active_state_source_stays_review_only(
        self,
    ) -> None:
        scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_specific_active_state_source_scout_1025.json"
        )
        mapping = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_specific_active_state_structure_mapping_review_1025.json"
        )
        acceptor = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_specific_active_state_acceptor_gap_audit_1025.json"
        )
        queue = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_specific_active_state_next_experiment_queue_1025.json"
        )
        self.assertEqual(
            scout["metadata"]["method"],
            "epk_ligand_specific_active_state_source_scout",
        )
        self.assertTrue(scout["metadata"]["review_only"])
        self.assertEqual(scout["metadata"]["query_pdb_count"], 30)
        self.assertEqual(scout["metadata"]["sourced_candidate_count"], 11)
        self.assertEqual(scout["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(scout["metadata"]["ready_to_run_epk_scorer"])
        self.assertFalse(scout["metadata"]["fingerprint_registry_edited"])
        self.assertFalse(scout["metadata"]["curated_label_registry_edited"])
        self.assertEqual(
            mapping["metadata"]["active_state_mapping_ready_accessions"], ["P53355"]
        )
        self.assertEqual(mapping["metadata"]["active_state_mapping_ready_pdb_ids"], ["1JKK"])
        self.assertEqual(mapping["metadata"]["active_state_mapping_ready_structure_count"], 1)
        self.assertEqual(mapping["metadata"]["measurement_ready_candidate_count"], 0)
        self.assertFalse(mapping["metadata"]["ready_to_run_epk_scorer"])
        self.assertEqual(
            acceptor["metadata"]["acceptor_gap_status_counts"],
            {"no_acceptor_like_hydroxyl_within_threshold_review_only": 1},
        )
        self.assertEqual(acceptor["metadata"]["measurement_ready_candidate_count"], 0)
        self.assertEqual(
            queue["metadata"]["top_priority_accession"],
            "P53355",
        )
        self.assertEqual(
            queue["metadata"]["top_priority_next_experiment"],
            "source_alternate_active_state_substrate_cocomplex",
        )
        self.assertFalse(queue["metadata"]["ready_to_run_epk_scorer"])
        self.assertEqual(queue["metadata"]["countable_label_candidate_count"], 0)

    def test_epk_ligand_specific_lower_priority_ligand_review_stays_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_specific_active_state_lower_priority_ligand_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_external_source_lower_priority_ligand_sourcing_review",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_row_count"], 4)
        self.assertEqual(metadata["active_gamma_metal_current_structure_count"], 0)
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertEqual(
            metadata["ligand_sourcing_status_counts"],
            {"non_atp_or_remote_ligand_context_needs_alternate_review_only": 4},
        )
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_ligand_specific_p53355_cocomplex_review_stays_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_specific_p53355_substrate_cocomplex_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_ligand_specific_p53355_substrate_cocomplex_review",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["accession"], "P53355")
        self.assertEqual(metadata["pdb_crossref_count"], 78)
        self.assertEqual(metadata["reviewed_pdb_count"], 78)
        self.assertEqual(metadata["active_state_gamma_metal_structure_count"], 5)
        self.assertEqual(metadata["source_phosphoacceptor_mapped_structure_count"], 13)
        self.assertEqual(metadata["source_phosphoacceptor_within_threshold_count"], 0)
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertEqual(
            metadata["cocomplex_review_status_counts"],
            {
                "active_state_without_source_phosphoacceptor_mapping_review_only": 5,
                "gamma_without_metal_no_acceptor_mapping_review_only": 4,
                "no_active_state_or_source_acceptor_context_review_only": 56,
                "source_phosphoacceptor_mapping_without_gamma_review_only": 13,
            },
        )
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertTrue(all(row["review_only"] for row in review["rows"]))
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in review["rows"])
        )

    def test_epk_ligand_specific_terminal_decision_stays_review_only(
        self,
    ) -> None:
        decision = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_specific_active_state_terminal_decision_1025.json"
        )
        metadata = decision["metadata"]
        self.assertEqual(
            metadata["method"], "epk_ligand_specific_active_state_terminal_decision"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["sourced_candidate_count"], 11)
        self.assertEqual(metadata["active_state_mapping_ready_structure_count"], 1)
        self.assertEqual(metadata["p53355_source_phosphoacceptor_within_threshold_count"], 0)
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertEqual(
            metadata["terminal_decision"],
            "ligand_specific_active_state_surface_blocked_no_source_mapped_acceptor_review_only",
        )
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(len(decision["rows"]), 5)
        self.assertTrue(all(row["review_only"] for row in decision["rows"]))

    def test_epk_ligand_specific_substrate_cocomplex_probe_stays_review_only(
        self,
    ) -> None:
        probe = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_specific_substrate_cocomplex_query_probe_1025.json"
        )
        metadata = probe["metadata"]
        self.assertEqual(
            metadata["method"], "epk_ligand_specific_substrate_cocomplex_query_probe"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["query_pdb_count"], 60)
        self.assertEqual(metadata["reviewed_pdb_count"], 60)
        self.assertEqual(metadata["source_ready_structure_count"], 42)
        self.assertEqual(metadata["acceptor_hit_structure_count_within_6_angstrom"], 4)
        self.assertEqual(
            metadata["cross_accession_acceptor_hit_structure_count_within_6_angstrom"],
            1,
        )
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            metadata["probe_status_counts"],
            {
                "no_source_acceptor_pair_review_only": 18,
                "source_ready_cross_accession_acceptor_hit_review_only": 1,
                "source_ready_no_acceptor_hit_review_only": 38,
                "source_ready_same_accession_acceptor_hit_review_only": 3,
            },
        )
        cross_rows = [
            row
            for row in probe["rows"]
            if row["probe_status"]
            == "source_ready_cross_accession_acceptor_hit_review_only"
        ]
        self.assertEqual([row["pdb_id"] for row in cross_rows], ["5HVK"])

    def test_epk_ligand_specific_5hvk_priority_stays_review_only(
        self,
    ) -> None:
        priority = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_specific_5hvk_review_priority_1025.json"
        )
        metadata = priority["metadata"]
        self.assertEqual(metadata["method"], "epk_ligand_specific_5hvk_review_priority")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["priority_pdb_id"], "5HVK")
        self.assertEqual(metadata["source_ready_accessions"], ["P53667"])
        self.assertEqual(metadata["cross_accession_acceptor_hit_count"], 1)
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertEqual(
            metadata["priority_status"],
            "manual_source_review_required_before_measurement_ready",
        )
        self.assertFalse(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(len(priority["rows"]), 2)
        self.assertTrue(all(row["review_only"] for row in priority["rows"]))

    def test_epk_ligand_specific_5hvk_source_validity_stays_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_specific_5hvk_source_validity_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_ligand_specific_5hvk_source_validity_review",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["pdb_id"], "5HVK")
        self.assertEqual(metadata["kinase_accession"], "P53667")
        self.assertEqual(metadata["acceptor_accession"], "P23528")
        self.assertTrue(metadata["source_validated_kinase_substrate_pair"])
        self.assertEqual(
            metadata["source_validity_status"],
            "accepted_source_valid_kinase_substrate_cocomplex_review_only",
        )
        self.assertEqual(metadata["measurement_ready_candidate_count"], 1)
        self.assertTrue(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertTrue(metadata["ready_to_rerun_controls"])
        self.assertEqual(
            metadata["nearest_source_phosphoacceptor_distance_angstrom"], 4.236
        )
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        row = review["rows"][0]
        self.assertTrue(row["review_only"])
        self.assertTrue(row["measurement_ready"])
        self.assertFalse(row["countable_label_candidate"])

    def test_epk_ligand_specific_5hvk_control_rerun_queue_stays_review_only(
        self,
    ) -> None:
        queue = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_specific_5hvk_control_rerun_queue_1025.json"
        )
        metadata = queue["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_ligand_specific_5hvk_control_rerun_queue",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["control_rerun_queue_status"],
            "ready_for_review_only_control_rerun",
        )
        self.assertTrue(metadata["source_validated_kinase_substrate_pair"])
        self.assertEqual(metadata["source_measurement_ready_candidate_count"], 1)
        self.assertEqual(metadata["sibling_control_row_count"], 20)
        self.assertEqual(metadata["imported_external_hard_negative_row_count"], 3)
        self.assertEqual(metadata["review_only_score_probe_non_abstention_count"], 0)
        self.assertTrue(metadata["not_a_real_scored_reaudit"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["task_id"]: row for row in queue["rows"]}
        self.assertEqual(
            rows["add_5hvk_source_valid_candidate_to_review_only_prototype"][
                "queue_status"
            ],
            "ready_review_only",
        )
        self.assertEqual(
            rows["rerun_current_sibling_control_surface"][
                "carried_control_decision_counts"
            ],
            {
                "blocked_by_family_specific_sibling_counteraxis_review_only": 16,
                "blocked_by_phosphohistidine_counteraxis_review_only": 4,
            },
        )
        self.assertTrue(
            rows["rerun_imported_external_hard_negative_controls"][
                "not_a_real_scored_reaudit"
            ]
        )

    def test_epk_ligand_specific_5hvk_prototype_control_rerun_stays_review_only(
        self,
    ) -> None:
        rerun = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_ligand_specific_5hvk_prototype_control_rerun_1025.json"
        )
        metadata = rerun["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_ligand_specific_5hvk_prototype_control_rerun",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["control_rerun_status"],
            "passes_review_only_controls_but_scorer_blocked",
        )
        self.assertTrue(metadata["source_valid_5hvk_candidate_added"])
        self.assertTrue(metadata["source_valid_5hvk_candidate_axis_complete"])
        self.assertEqual(metadata["source_valid_5hvk_distance_angstrom"], 4.236)
        self.assertEqual(metadata["positive_like_review_row_count"], 4)
        self.assertEqual(metadata["sibling_control_row_count"], 20)
        self.assertEqual(metadata["sibling_control_false_hit_count"], 0)
        self.assertEqual(metadata["imported_external_hard_negative_row_count"], 3)
        self.assertEqual(
            metadata["imported_external_hard_negative_non_abstention_count"],
            0,
        )
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {
            row["row_type"]: row
            for row in rerun["rows"]
            if row["row_type"]
            == "ligand_specific_5hvk_source_valid_positive_candidate"
        }
        self.assertEqual(
            rows["ligand_specific_5hvk_source_valid_positive_candidate"][
                "prototype_decision"
            ],
            "source_valid_5hvk_positive_signal_review_only_not_calibrated",
        )

    def test_epk_5hvk_protein_substrate_axis_generalization_stays_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_5hvk_protein_substrate_axis_generalization_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_5hvk_protein_substrate_axis_generalization_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["generalization_status"],
            "passes_review_only_generalization_but_not_scoring_admissible",
        )
        self.assertEqual(
            metadata["current_m_csa_protein_substrate_positive_hit_count"],
            2,
        )
        self.assertEqual(
            metadata["source_valid_5hvk_protein_substrate_positive_count"],
            1,
        )
        self.assertEqual(
            metadata["combined_protein_substrate_positive_like_count"],
            3,
        )
        self.assertFalse(
            metadata["ligand_analog_required_for_minimum_review_set"]
        )
        self.assertEqual(metadata["sibling_control_false_hit_count"], 0)
        self.assertEqual(
            metadata["imported_external_hard_negative_non_abstention_count"],
            0,
        )
        self.assertFalse(metadata["feature_admissible_for_production_scoring"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_protein_substrate_scorer_design_freeze_stays_review_only(
        self,
    ) -> None:
        design = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_protein_substrate_scorer_design_freeze_1025.json"
        )
        metadata = design["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_protein_substrate_scorer_design_freeze",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["design_status"],
            "frozen_review_only_ready_for_diagnostic_calibration",
        )
        self.assertTrue(metadata["ready_for_review_only_calibration_diagnostic"])
        self.assertTrue(metadata["source_authority_axes_present"])
        self.assertFalse(
            metadata["source_authority_axes_valid_for_orphan_discovery_claims"]
        )
        self.assertFalse(metadata["mechanism_text_predictive_use_allowed"])
        self.assertFalse(metadata["production_scoring_admissible"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        axis_ids = {row["axis_id"] for row in design["rows"]}
        self.assertIn("source_validated_protein_substrate_hydroxyl_acceptor", axis_ids)
        self.assertIn("sibling_family_counteraxis", axis_ids)

    def test_epk_protein_substrate_calibration_diagnostic_stays_review_only(
        self,
    ) -> None:
        diagnostic = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_protein_substrate_calibration_diagnostic_1025.json"
        )
        metadata = diagnostic["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_protein_substrate_calibration_diagnostic",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["diagnostic_status"],
            "passes_review_only_calibration_controls_not_real_scorer",
        )
        self.assertTrue(metadata["review_only_diagnostic_score_computed"])
        self.assertEqual(metadata["diagnostic_positive_full_axis_count"], 3)
        self.assertEqual(metadata["ligand_analog_excluded_positive_count"], 1)
        self.assertEqual(metadata["sibling_control_nonzero_score_count"], 0)
        self.assertEqual(
            metadata["imported_external_hard_negative_nonzero_score_count"],
            0,
        )
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["production_scoring_admissible"])
        self.assertFalse(
            metadata["source_authority_axes_valid_for_orphan_discovery_claims"]
        )
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_source_authority_axis_replacement_gap_audit_stays_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_source_authority_axis_replacement_gap_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_source_authority_axis_replacement_gap_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["replacement_status"],
            "blocked_review_only_source_authority_axes_require_local_replacements",
        )
        self.assertTrue(metadata["diagnostic_passed_review_only_controls"])
        self.assertEqual(metadata["source_authority_axis_count"], 2)
        self.assertEqual(metadata["replacement_gap_count"], 2)
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_orphan_discovery_claims"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        gap_ids = {row["gap_id"] for row in audit["rows"]}
        self.assertIn("source_validated_protein_substrate_acceptor_identity", gap_ids)

    def test_epk_local_chain_topology_acceptor_rule_stays_review_only(
        self,
    ) -> None:
        rule = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_local_chain_topology_acceptor_replacement_rule_1025.json"
        )
        metadata = rule["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_local_chain_topology_acceptor_replacement_rule",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["candidate_rule_status"],
            "passes_current_review_controls_source_roles_not_replaced",
        )
        self.assertEqual(metadata["positive_rule_hit_count"], 3)
        self.assertEqual(metadata["ligand_analog_excluded_positive_count"], 1)
        self.assertEqual(metadata["control_false_hit_count"], 0)
        self.assertEqual(
            metadata["imported_external_hard_negative_non_abstention_count"],
            0,
        )
        self.assertTrue(metadata["source_authority_reduced_not_eliminated"])
        self.assertFalse(
            metadata["source_authority_axes_valid_for_orphan_discovery_claims"]
        )
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_5hvk_local_polymer_entity_role_audit_stays_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_5hvk_local_polymer_entity_role_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_5hvk_local_polymer_entity_role_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["audit_status"],
            "partial_local_entity_support_source_roles_still_required",
        )
        self.assertTrue(metadata["local_entity_supports_cocomplex"])
        self.assertTrue(metadata["chain_sets_disjoint"])
        self.assertFalse(metadata["source_authority_eliminated"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_source_free_chain_topology_role_audit_stays_blocked(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_source_free_chain_topology_role_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_source_free_chain_topology_role_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["audit_status"],
            "blocked_review_only_source_free_topology_role_rule_false_hit_risk",
        )
        self.assertTrue(metadata["source_fields_masked_for_candidate_rule"])
        self.assertEqual(metadata["masked_local_candidate_hit_count"], 4)
        self.assertEqual(metadata["source_valid_cross_accession_positive_count"], 1)
        self.assertEqual(metadata["known_same_accession_control_risk_count"], 3)
        self.assertEqual(
            metadata["known_same_accession_control_risk_pdb_ids"],
            ["3Q4Z", "4I94", "5XD6"],
        )
        self.assertFalse(metadata["source_free_role_assignment_safe"])
        self.assertFalse(metadata["source_authority_eliminated"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_heteromeric_chain_topology_signal_audit_stays_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_chain_topology_signal_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_chain_topology_signal_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["audit_status"],
            "passes_current_hit_controls_but_insufficient_positive_coverage_review_only",
        )
        self.assertTrue(metadata["source_fields_masked_for_candidate_rule"])
        self.assertEqual(metadata["evaluated_hit_control_count"], 4)
        self.assertEqual(metadata["heteromeric_signal_positive_like_count"], 1)
        self.assertEqual(
            metadata["heteromeric_signal_positive_like_pdb_ids"],
            ["5HVK"],
        )
        self.assertEqual(
            metadata["same_accession_control_signal_false_hit_count"], 0
        )
        self.assertEqual(
            metadata["same_accession_control_abstention_pdb_ids"],
            ["3Q4Z", "4I94", "5XD6"],
        )
        self.assertTrue(metadata["current_hit_controls_passed"])
        self.assertFalse(metadata["minimum_positive_coverage_met"])
        self.assertTrue(metadata["full_probe_candidate_scout_run"])
        self.assertEqual(metadata["full_probe_candidate_scout_query_pdb_count"], 60)
        self.assertEqual(
            metadata["full_probe_candidate_scout_fetch_failure_count"], 0
        )
        self.assertEqual(
            metadata["full_probe_heteromeric_candidate_structure_count"],
            1,
        )
        self.assertEqual(
            metadata["full_probe_heteromeric_candidate_pdb_ids"],
            ["5HVK"],
        )
        self.assertTrue(metadata["source_free_5hvk_role_direction_supported"])
        self.assertFalse(metadata["source_authority_eliminated"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        scout_rows = [
            row
            for row in audit["rows"]
            if row["row_type"] == "full_probe_heteromeric_candidate_scout"
        ]
        self.assertEqual([row["pdb_id"] for row in scout_rows], ["5HVK"])
        self.assertEqual(scout_rows[0]["heteromeric_candidate_hit_count"], 1)
        self.assertEqual(
            scout_rows[0]["heteromeric_candidate_hits"][0][
                "candidate_chain_name"
            ],
            "D",
        )
        hit_controls = [
            row
            for row in audit["rows"]
            if row["row_type"] == "heteromeric_chain_topology_hit_control"
        ]
        mapping_bases = {
            evaluation["gamma_associated_polymer_entity_mapping_basis"]
            for row in hit_controls
            for evaluation in row["hit_evaluations"]
            if evaluation.get("mapped_acceptor_atom")
        }
        self.assertEqual(mapping_bases, {"atom_site_author_chain_polymer_entity"})

    def test_epk_heteromeric_positive_coverage_candidate_scout_is_review_only(
        self,
    ) -> None:
        scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_positive_coverage_candidate_scout_1025.json"
        )
        metadata = scout["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_positive_coverage_candidate_scout",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["input_candidate_count"], 50)
        self.assertEqual(metadata["reviewed_candidate_count"], 50)
        self.assertEqual(metadata["fetch_failure_count"], 0)
        self.assertEqual(metadata["heteromeric_candidate_structure_count"], 6)
        self.assertEqual(
            metadata["heteromeric_candidate_pdb_ids"],
            ["6Z3R", "7M0T", "7M0W", "8OXM", "8OXO", "8ZN6"],
        )
        self.assertTrue(metadata["source_validation_queue_ready"])
        self.assertEqual(
            metadata["positive_coverage_status"],
            "source_validation_pending_for_broadened_heteromeric_candidates_review_only",
        )
        self.assertFalse(metadata["minimum_positive_coverage_met"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        hit_rows = [
            row
            for row in scout["rows"]
            if row["candidate_status"]
            == "heteromeric_candidate_source_validation_pending_review_only"
        ]
        self.assertEqual(len(hit_rows), 6)
        for row in hit_rows:
            self.assertFalse(row["measurement_ready"])
            self.assertIn(
                "source_validation_pending_for_heteromeric_candidate",
                row["remaining_blockers"],
            )

    def test_epk_heteromeric_candidate_source_validation_review_is_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_candidate_source_validation_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_candidate_source_validation_review",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_candidate_count"], 6)
        self.assertEqual(metadata["fetch_failure_count"], 0)
        self.assertEqual(metadata["source_validated_new_candidate_count"], 3)
        self.assertEqual(
            metadata["source_validated_new_candidate_pdb_ids"],
            ["6Z3R", "8OXM", "8OXO"],
        )
        self.assertEqual(
            metadata["source_validated_unique_pair_ids"],
            ["atm_p53", "smg1_upf1"],
        )
        self.assertEqual(metadata["ambiguous_candidate_count"], 2)
        self.assertEqual(metadata["rejected_candidate_count"], 1)
        self.assertTrue(metadata["minimum_positive_coverage_met_review_only"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        accepted_rows = [
            row for row in review["rows"] if row["source_validated_positive_like"]
        ]
        self.assertEqual({row["pdb_id"] for row in accepted_rows}, {"6Z3R", "8OXM", "8OXO"})
        for row in accepted_rows:
            self.assertFalse(row["measurement_ready"])
            self.assertIn(
                "external_hard_negative_reaudit_not_real_scorer",
                row["remaining_blockers"],
            )

    def test_epk_heteromeric_source_valid_candidate_distance_sample_is_review_only(
        self,
    ) -> None:
        sample = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_valid_candidate_gamma_distance_sample_1025.json"
        )
        metadata = sample["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_source_valid_candidate_gamma_distance_sample",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["source_validated_candidate_count"], 3)
        self.assertEqual(metadata["measured_candidate_count"], 3)
        self.assertEqual(
            metadata["measured_candidate_pdb_ids"],
            ["6Z3R", "8OXM", "8OXO"],
        )
        self.assertEqual(
            metadata["measured_unique_pair_ids"],
            ["atm_p53", "smg1_upf1"],
        )
        self.assertTrue(metadata["all_source_valid_candidates_measured"])
        self.assertTrue(metadata["minimum_positive_coverage_measured_review_only"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(len(sample["rows"]), 3)
        for row in sample["rows"]:
            self.assertEqual(
                row["measurement_status"],
                "source_valid_heteromeric_gamma_distance_measured_review_only",
            )
            self.assertTrue(row["measurement_ready_for_review_controls"])
            self.assertFalse(row["ready_to_run_epk_scorer"])
            self.assertIn(
                "threshold_not_calibrated_against_negative_controls",
                row["remaining_blockers"],
            )

    def test_epk_heteromeric_source_valid_control_rerun_is_review_only(
        self,
    ) -> None:
        rerun = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_valid_control_rerun_1025.json"
        )
        metadata = rerun["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_source_valid_control_rerun",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["control_rerun_status"],
            "passes_review_only_controls_but_scorer_blocked",
        )
        self.assertEqual(metadata["heteromeric_source_valid_candidate_row_count"], 3)
        self.assertEqual(metadata["heteromeric_source_valid_axis_complete_count"], 3)
        self.assertEqual(
            metadata["heteromeric_source_valid_pdb_ids"],
            ["6Z3R", "8OXM", "8OXO"],
        )
        self.assertEqual(
            metadata["heteromeric_source_valid_unique_pair_ids"],
            ["atm_p53", "smg1_upf1"],
        )
        self.assertEqual(metadata["heteromeric_ambiguous_candidate_count"], 2)
        self.assertEqual(metadata["heteromeric_rejected_candidate_count"], 1)
        self.assertTrue(metadata["heteromeric_ambiguous_and_rejected_separated"])
        self.assertEqual(metadata["positive_like_review_row_count"], 7)
        self.assertEqual(metadata["sibling_control_false_hit_count"], 0)
        self.assertEqual(
            metadata["imported_external_hard_negative_non_abstention_count"], 0
        )
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        source_valid_rows = [
            row
            for row in rerun["rows"]
            if row["row_type"] == "heteromeric_source_valid_positive_candidate"
        ]
        self.assertEqual(len(source_valid_rows), 3)
        for row in source_valid_rows:
            self.assertEqual(
                row["prototype_decision"],
                "source_valid_heteromeric_positive_signal_review_only_not_calibrated",
            )
            self.assertFalse(row["text_free_inputs_only"])
            self.assertIn(
                "external_hard_negative_reaudit_not_real_scorer",
                row["remaining_blockers"],
            )
        separated_rows = [
            row
            for row in rerun["rows"]
            if row["row_type"] == "heteromeric_candidate_separated_nonpositive_control"
        ]
        self.assertEqual(len(separated_rows), 3)
        self.assertFalse(any(row["candidate_feature_hit"] for row in separated_rows))

    def test_epk_heteromeric_source_expansion_artifacts_are_review_only(
        self,
    ) -> None:
        atp_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_expansion_candidate_scout_atp_1025.json"
        )
        adp_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_expansion_candidate_scout_adp_1025.json"
        )
        amp_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_expansion_candidate_scout_amp_pnp_1025.json"
        )
        ags_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_expansion_candidate_scout_ags_1025.json"
        )
        broad_peptide_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_expansion_candidate_scout_broad_peptide_atp_1025.json"
        )
        validation = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_expansion_source_validation_review_amp_pnp_1025.json"
        )
        broad_peptide_validation = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_expansion_source_validation_review_broad_peptide_atp_1025.json"
        )
        next_amp_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_candidate_scout_amp_pnp_peptide_1025.json"
        )
        next_protein_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_candidate_scout_protein_substrate_anp_1025.json"
        )
        next_broad_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_candidate_scout_broad_text_atp_1025.json"
        )
        next_amp_validation = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_source_validation_review_amp_pnp_peptide_1025.json"
        )
        next_amp_round2_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_candidate_scout_amp_pnp_peptide_round2_1025.json"
        )
        next_protein_round2_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_candidate_scout_protein_substrate_anp_round2_1025.json"
        )
        next_broad_round2_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_candidate_scout_broad_text_atp_round2_1025.json"
        )
        next_amp_round2_validation = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_source_validation_review_amp_pnp_peptide_round2_1025.json"
        )
        next_broad_round2_validation = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_source_validation_review_broad_text_atp_round2_1025.json"
        )
        next_protein_round3_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_candidate_scout_protein_substrate_anp_round3_1025.json"
        )
        next_broad_round3_scout = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_candidate_scout_broad_text_atp_round3_1025.json"
        )
        next_protein_round3_validation = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_source_validation_review_protein_substrate_anp_round3_1025.json"
        )
        next_broad_round3_validation = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_next_broad_stress_source_validation_review_broad_text_atp_round3_1025.json"
        )
        distance_sample = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_expansion_gamma_distance_sample_amp_pnp_1025.json"
        )
        rerun = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_expansion_control_rerun_amp_pnp_1025.json"
        )
        peptide_role_axis = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_expansion_peptide_role_axis_audit_1025.json"
        )

        self.assertEqual(atp_scout["metadata"]["input_candidate_count"], 25)
        self.assertEqual(atp_scout["metadata"]["heteromeric_candidate_structure_count"], 0)
        self.assertFalse(atp_scout["metadata"]["source_validation_queue_ready"])

        self.assertEqual(adp_scout["metadata"]["input_candidate_count"], 25)
        self.assertEqual(adp_scout["metadata"]["heteromeric_candidate_structure_count"], 0)
        self.assertFalse(adp_scout["metadata"]["source_validation_queue_ready"])

        self.assertEqual(ags_scout["metadata"]["input_candidate_count"], 25)
        self.assertEqual(ags_scout["metadata"]["heteromeric_candidate_structure_count"], 0)
        self.assertFalse(ags_scout["metadata"]["source_validation_queue_ready"])

        self.assertEqual(amp_scout["metadata"]["input_candidate_count"], 11)
        self.assertEqual(amp_scout["metadata"]["heteromeric_candidate_pdb_ids"], ["1O6K", "1O6L"])
        self.assertTrue(amp_scout["metadata"]["source_validation_queue_ready"])

        self.assertEqual(broad_peptide_scout["metadata"]["input_candidate_count"], 25)
        self.assertEqual(
            broad_peptide_scout["metadata"]["heteromeric_candidate_pdb_ids"],
            ["9L3M", "9L3U"],
        )
        self.assertTrue(broad_peptide_scout["metadata"]["source_validation_queue_ready"])

        self.assertEqual(validation["metadata"]["source_validated_new_candidate_count"], 2)
        self.assertEqual(
            validation["metadata"]["source_validated_new_candidate_pdb_ids"],
            ["1O6K", "1O6L"],
        )
        self.assertEqual(validation["metadata"]["source_validated_unique_pair_ids"], ["pkb_gsk3"])
        self.assertEqual(
            validation["metadata"]["source_validation_status_counts"],
            {
                "accepted_source_valid_heteromeric_kinase_substrate_review_only": 2,
            },
        )
        self.assertEqual(
            broad_peptide_validation["metadata"]["source_validated_new_candidate_count"],
            0,
        )
        self.assertEqual(
            broad_peptide_validation["metadata"]["source_validation_status_counts"],
            {"blocked_source_context_insufficient_review_only": 2},
        )

        self.assertEqual(next_amp_scout["metadata"]["input_candidate_count"], 25)
        self.assertEqual(
            next_amp_scout["metadata"]["heteromeric_candidate_pdb_ids"],
            ["7ZE5"],
        )
        self.assertTrue(next_amp_scout["metadata"]["source_validation_queue_ready"])
        self.assertEqual(next_protein_scout["metadata"]["input_candidate_count"], 25)
        self.assertEqual(
            next_protein_scout["metadata"]["heteromeric_candidate_structure_count"],
            0,
        )
        self.assertFalse(next_protein_scout["metadata"]["source_validation_queue_ready"])
        self.assertEqual(next_broad_scout["metadata"]["input_candidate_count"], 25)
        self.assertEqual(
            next_broad_scout["metadata"]["heteromeric_candidate_structure_count"],
            0,
        )
        self.assertFalse(next_broad_scout["metadata"]["source_validation_queue_ready"])
        self.assertEqual(
            next_amp_validation["metadata"]["source_validation_status_counts"],
            {"blocked_source_context_insufficient_review_only": 1},
        )
        self.assertEqual(
            next_amp_validation["metadata"]["source_validated_new_candidate_count"],
            0,
        )
        self.assertIn(
            "ATP-binding/permease protein CydC",
            next_amp_validation["rows"][0]["entity_descriptions"],
        )

        self.assertEqual(next_amp_round2_scout["metadata"]["input_candidate_count"], 13)
        self.assertEqual(
            next_amp_round2_scout["metadata"]["heteromeric_candidate_pdb_ids"],
            ["4HPU"],
        )
        self.assertTrue(
            next_amp_round2_scout["metadata"]["source_validation_queue_ready"]
        )
        self.assertEqual(
            next_protein_round2_scout["metadata"]["input_candidate_count"], 25
        )
        self.assertEqual(
            next_protein_round2_scout["metadata"][
                "heteromeric_candidate_structure_count"
            ],
            0,
        )
        self.assertFalse(
            next_protein_round2_scout["metadata"]["source_validation_queue_ready"]
        )
        self.assertEqual(next_broad_round2_scout["metadata"]["input_candidate_count"], 25)
        self.assertEqual(
            next_broad_round2_scout["metadata"]["heteromeric_candidate_pdb_ids"],
            ["7T55", "7T56", "7T57"],
        )
        self.assertTrue(
            next_broad_round2_scout["metadata"]["source_validation_queue_ready"]
        )
        self.assertEqual(
            next_amp_round2_validation["metadata"][
                "source_validation_status_counts"
            ],
            {"blocked_source_context_insufficient_review_only": 1},
        )
        self.assertEqual(
            next_amp_round2_validation["metadata"][
                "source_validated_new_candidate_count"
            ],
            0,
        )
        self.assertIn(
            "cAMP-dependent protein kinase catalytic subunit alpha",
            next_amp_round2_validation["rows"][0]["entity_descriptions"],
        )
        self.assertEqual(
            next_broad_round2_validation["metadata"][
                "source_validation_status_counts"
            ],
            {"blocked_source_context_insufficient_review_only": 3},
        )
        self.assertEqual(
            next_broad_round2_validation["metadata"][
                "source_validated_new_candidate_count"
            ],
            0,
        )
        self.assertEqual(
            [row["pdb_id"] for row in next_broad_round2_validation["rows"]],
            ["7T55", "7T56", "7T57"],
        )

        self.assertEqual(
            next_protein_round3_scout["metadata"]["input_candidate_count"], 25
        )
        self.assertEqual(
            next_protein_round3_scout["metadata"]["heteromeric_candidate_pdb_ids"],
            ["2JJ2", "7B56"],
        )
        self.assertTrue(
            next_protein_round3_scout["metadata"]["source_validation_queue_ready"]
        )
        self.assertEqual(next_broad_round3_scout["metadata"]["input_candidate_count"], 25)
        self.assertEqual(
            next_broad_round3_scout["metadata"]["heteromeric_candidate_pdb_ids"],
            ["7ZDT", "7ZDU"],
        )
        self.assertTrue(
            next_broad_round3_scout["metadata"]["source_validation_queue_ready"]
        )
        self.assertEqual(
            next_protein_round3_validation["metadata"][
                "source_validation_status_counts"
            ],
            {"blocked_source_context_insufficient_review_only": 2},
        )
        self.assertEqual(
            next_broad_round3_validation["metadata"][
                "source_validation_status_counts"
            ],
            {"blocked_source_context_insufficient_review_only": 2},
        )
        self.assertEqual(
            [row["pdb_id"] for row in next_protein_round3_validation["rows"]],
            ["2JJ2", "7B56"],
        )
        self.assertEqual(
            [row["pdb_id"] for row in next_broad_round3_validation["rows"]],
            ["7ZDT", "7ZDU"],
        )

        self.assertEqual(
            distance_sample["metadata"]["measured_candidate_pdb_ids"],
            ["1O6K", "1O6L"],
        )
        self.assertEqual(distance_sample["metadata"]["measured_unique_pair_ids"], ["pkb_gsk3"])
        self.assertEqual(distance_sample["metadata"]["distance_min_angstrom"], 3.542)
        self.assertEqual(distance_sample["metadata"]["distance_max_angstrom"], 3.566)

        self.assertEqual(
            rerun["metadata"]["control_rerun_status"],
            "blocked_review_only_control_rerun",
        )
        self.assertEqual(rerun["metadata"]["heteromeric_source_valid_candidate_row_count"], 2)
        self.assertEqual(rerun["metadata"]["source_authority_dependent_positive_like_count"], 1)
        self.assertEqual(rerun["metadata"]["heteromeric_source_valid_axis_complete_count"], 0)
        self.assertEqual(rerun["metadata"]["countable_label_candidate_count"], 0)

        self.assertEqual(
            peptide_role_axis["metadata"]["source_expansion_peptide_role_axis_status"],
            "passes_source_expansion_controls_peptide_role_axis_review_only",
        )
        self.assertEqual(
            peptide_role_axis["metadata"]["source_valid_expansion_peptide_role_hit_pdb_ids"],
            ["1O6K", "1O6L"],
        )
        self.assertEqual(
            peptide_role_axis["metadata"]["source_expansion_reviewed_row_count"],
            13,
        )
        self.assertEqual(
            peptide_role_axis["metadata"]["source_expansion_status_counts"],
            {
                "nonpositive_source_expansion_blocked_by_peptide_role_axis": 11,
                "positive_like_source_expansion_peptide_role_hit_review_only": 2,
            },
        )
        self.assertEqual(
            peptide_role_axis["metadata"][
                "source_free_peptide_role_axis_counterevidence_status_counts"
            ],
            {
                "candidate_acceptor_and_gamma_on_same_chain": 5,
                "candidate_acceptor_chain_has_local_nucleotide_or_metal": 9,
                "candidate_acceptor_chain_not_peptide_like": 11,
                "gamma_chain_not_larger_than_acceptor_chain": 5,
            },
        )
        self.assertEqual(
            peptide_role_axis["metadata"][
                "nonpositive_source_expansion_counterevidence_complete_pdb_ids"
            ],
            [
                "2JJ2",
                "4HPU",
                "7B56",
                "7T55",
                "7T56",
                "7T57",
                "7ZDT",
                "7ZDU",
                "7ZE5",
                "9L3M",
                "9L3U",
            ],
        )
        self.assertEqual(
            peptide_role_axis["metadata"]["nonpositive_source_expansion_control_false_hit_count"],
            0,
        )
        self.assertEqual(
            peptide_role_axis["metadata"]["general_substrate_identity_ready_count"],
            0,
        )

        for artifact in [
            atp_scout,
            adp_scout,
            ags_scout,
            amp_scout,
            broad_peptide_scout,
            validation,
            broad_peptide_validation,
            next_amp_scout,
            next_protein_scout,
            next_broad_scout,
            next_amp_validation,
            next_amp_round2_scout,
            next_protein_round2_scout,
            next_broad_round2_scout,
            next_amp_round2_validation,
            next_broad_round2_validation,
            next_protein_round3_scout,
            next_broad_round3_scout,
            next_protein_round3_validation,
            next_broad_round3_validation,
            distance_sample,
            rerun,
            peptide_role_axis,
        ]:
            metadata = artifact["metadata"]
            self.assertTrue(metadata["review_only"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
            self.assertFalse(metadata["ready_for_production_scoring"])
            self.assertFalse(metadata["ready_for_label_import"])
            self.assertFalse(metadata["fingerprint_registry_edited"])
            self.assertFalse(metadata["curated_label_registry_edited"])

    def test_epk_heteromeric_text_free_axis_gap_audit_is_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_text_free_axis_gap_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_text_free_axis_gap_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["gap_audit_status"],
            "blocked_review_only_source_free_role_acceptor_axes_missing",
        )
        self.assertEqual(metadata["source_authority_dependent_positive_like_count"], 4)
        self.assertEqual(metadata["local_geometry_axis_present_count"], 4)
        self.assertEqual(metadata["source_free_role_assignment_ready_count"], 0)
        self.assertEqual(metadata["source_free_acceptor_identity_ready_count"], 0)
        self.assertEqual(metadata["production_admissible_positive_like_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(len(audit["rows"]), 4)
        for row in audit["rows"]:
            self.assertTrue(row["local_geometry_axis_present"])
            self.assertFalse(row["source_free_role_assignment_present"])
            self.assertFalse(row["source_free_acceptor_identity_present"])
            self.assertFalse(row["production_scoring_admissible"])
            self.assertIn(
                "source_free_kinase_substrate_role_assignment_missing",
                row["remaining_blockers"],
            )

    def test_epk_heteromeric_source_free_role_rule_probe_fails_closed(
        self,
    ) -> None:
        probe = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_free_role_rule_probe_1025.json"
        )
        metadata = probe["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_source_free_role_rule_probe",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["source_free_rule_status"],
            "blocked_review_only_source_free_rule_false_hit_risk",
        )
        self.assertEqual(metadata["reviewed_candidate_count"], 6)
        self.assertEqual(metadata["source_free_rule_hit_count"], 6)
        self.assertEqual(metadata["accepted_rule_hit_count"], 3)
        self.assertEqual(metadata["ambiguous_rule_hit_count"], 2)
        self.assertEqual(metadata["rejected_rule_hit_count"], 1)
        self.assertEqual(metadata["nonaccepted_rule_hit_count"], 3)
        self.assertEqual(
            metadata["nonaccepted_rule_hit_pdb_ids"],
            ["7M0T", "7M0W", "8ZN6"],
        )
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        false_hit_rows = [
            row
            for row in probe["rows"]
            if row["source_free_rule_decision"]
            == "source_free_rule_false_hit_risk_review_only"
        ]
        self.assertEqual({row["pdb_id"] for row in false_hit_rows}, {"7M0T", "7M0W", "8ZN6"})
        for row in false_hit_rows:
            self.assertTrue(row["text_free_inputs_only"])
            self.assertFalse(row["production_scoring_admissible"])
            self.assertIn("source_free_rule_false_hit_risk", row["remaining_blockers"])

    def test_epk_heteromeric_acceptor_chain_counteraxis_audit_is_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_acceptor_chain_counteraxis_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_acceptor_chain_counteraxis_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["counteraxis_status"],
            "passes_current_review_controls_not_scoring_admissible",
        )
        self.assertEqual(metadata["reviewed_candidate_count"], 6)
        self.assertEqual(metadata["fetch_failure_count"], 0)
        self.assertEqual(metadata["initial_topology_gamma_rule_hit_count"], 6)
        self.assertEqual(metadata["retained_source_valid_hit_count"], 3)
        self.assertEqual(metadata["blocked_nonaccepted_rule_hit_count"], 3)
        self.assertEqual(
            metadata["blocked_nonaccepted_rule_hit_pdb_ids"],
            ["7M0T", "7M0W", "8ZN6"],
        )
        self.assertEqual(metadata["residual_nonaccepted_rule_hit_count"], 0)
        self.assertEqual(metadata["accepted_lost_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        retained = [
            row
            for row in audit["rows"]
            if row["counteraxis_decision"]
            == "source_free_counteraxis_retains_source_valid_review_positive"
        ]
        blocked = [
            row
            for row in audit["rows"]
            if row["counteraxis_decision"]
            == "source_free_counteraxis_blocks_nonaccepted_rule_hit"
        ]
        self.assertEqual({row["pdb_id"] for row in retained}, {"6Z3R", "8OXM", "8OXO"})
        self.assertEqual({row["pdb_id"] for row in blocked}, {"7M0T", "7M0W", "8ZN6"})
        for row in audit["rows"]:
            self.assertTrue(row["text_free_inputs_only"])
            self.assertFalse(row["production_scoring_admissible"])

    def test_epk_heteromeric_broader_counteraxis_control_audit_is_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_broader_counteraxis_control_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_broader_counteraxis_control_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["broader_counteraxis_status"],
            "passes_broader_review_controls_not_scoring_admissible",
        )
        self.assertEqual(metadata["broader_heteromeric_reviewed_structure_count"], 50)
        self.assertEqual(metadata["broader_heteromeric_initial_hit_count"], 6)
        self.assertEqual(metadata["broader_heteromeric_no_hit_count"], 44)
        self.assertEqual(metadata["retained_source_valid_hit_count"], 3)
        self.assertEqual(metadata["blocked_nonaccepted_rule_hit_count"], 3)
        self.assertEqual(metadata["residual_nonaccepted_rule_hit_count"], 0)
        self.assertEqual(metadata["accepted_lost_count"], 0)
        self.assertEqual(
            metadata["sibling_control_family_ids"],
            ["atp_grasp", "ndk", "pfka", "pfkb"],
        )
        self.assertEqual(metadata["sibling_same_chain_hydroxyl_hit_count"], 11)
        self.assertEqual(metadata["sibling_counteraxis_blocked_hit_count"], 11)
        self.assertEqual(metadata["sibling_residual_false_hit_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        sibling_blocked = [
            row
            for row in audit["rows"]
            if row["counteraxis_decision"]
            == "source_free_counteraxis_blocks_sibling_same_chain_ligand_hit"
        ]
        self.assertEqual(len(sibling_blocked), 11)
        for row in audit["rows"]:
            self.assertTrue(row["text_free_inputs_only"])
            self.assertFalse(row["production_scoring_admissible"])

    def test_epk_heteromeric_ligand_asymmetry_role_audit_is_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_ligand_asymmetry_role_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_ligand_asymmetry_role_audit",
        )
        self.assertEqual(
            metadata["role_axis_status"],
            "passes_current_ligand_asymmetry_role_controls_not_scoring_admissible",
        )
        self.assertEqual(metadata["retained_source_valid_role_hit_count"], 3)
        self.assertEqual(metadata["nonaccepted_role_hit_count"], 0)
        self.assertEqual(metadata["sibling_role_asymmetry_false_hit_count"], 0)
        self.assertEqual(metadata["source_free_role_assignment_ready_count"], 3)
        self.assertEqual(metadata["source_free_acceptor_identity_ready_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        role_hits = [
            row
            for row in audit["rows"]
            if row["role_axis_decision"]
            == "ligand_asymmetry_supports_heteromeric_role_assignment_review_only"
        ]
        self.assertEqual({row["pdb_id"] for row in role_hits}, {"6Z3R", "8OXM", "8OXO"})
        for row in audit["rows"]:
            self.assertTrue(row["text_free_inputs_only"])
            self.assertFalse(row["production_scoring_admissible"])

    def test_epk_heteromeric_acceptor_identity_gap_audit_is_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_acceptor_identity_gap_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_acceptor_identity_gap_audit",
        )
        self.assertEqual(
            metadata["acceptor_identity_gap_status"],
            "blocked_review_only_source_free_acceptor_identity_missing",
        )
        self.assertEqual(metadata["retained_role_hit_count"], 3)
        self.assertEqual(metadata["source_context_only_acceptor_identity_count"], 3)
        self.assertEqual(metadata["source_free_acceptor_identity_ready_count"], 0)
        self.assertEqual(
            metadata["candidate_acceptor_residue_codes_review_context"],
            ["SER"],
        )
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(len(audit["rows"]), 3)
        for row in audit["rows"]:
            self.assertTrue(row["source_free_role_assignment_present"])
            self.assertFalse(row["source_free_acceptor_identity_present"])
            self.assertTrue(row["source_context_acceptor_identity_present"])
            self.assertTrue(row["text_free_inputs_only"])
            self.assertFalse(row["production_scoring_admissible"])

    def test_epk_heteromeric_acceptor_identity_rule_probe_is_review_only(
        self,
    ) -> None:
        probe = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_acceptor_identity_rule_probe_1025.json"
        )
        metadata = probe["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_acceptor_identity_rule_probe",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["identity_rule_status"],
            "passes_current_controls_but_generic_identity_axis_weak_review_only",
        )
        self.assertEqual(metadata["retained_role_hit_count"], 3)
        self.assertEqual(metadata["positive_identity_rule_hit_count"], 3)
        self.assertEqual(metadata["nonaccepted_blocked_before_identity_rule_count"], 3)
        self.assertEqual(metadata["nonaccepted_identity_rule_hit_count"], 0)
        self.assertEqual(
            metadata["sibling_same_chain_blocked_before_identity_rule_count"], 11
        )
        self.assertEqual(metadata["sibling_identity_rule_false_hit_count"], 0)
        self.assertTrue(metadata["generic_identity_axis_weak"])
        self.assertEqual(metadata["source_free_acceptor_identity_ready_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        positive_rows = [
            row
            for row in probe["rows"]
            if row["row_type"] == "heteromeric_acceptor_identity_rule_probe"
        ]
        self.assertEqual({row["pdb_id"] for row in positive_rows}, {"6Z3R", "8OXM", "8OXO"})
        for row in probe["rows"]:
            self.assertTrue(row["text_free_inputs_only"])
            self.assertFalse(row["production_scoring_admissible"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_heteromeric_peptide_acceptor_identity_probe_is_review_only(
        self,
    ) -> None:
        probe = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_peptide_acceptor_identity_probe_1025.json"
        )
        metadata = probe["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_peptide_acceptor_identity_probe",
        )
        self.assertEqual(
            metadata["peptide_identity_axis_status"],
            "passes_current_controls_peptide_like_acceptor_identity_review_only",
        )
        self.assertEqual(metadata["retained_role_hit_count"], 3)
        self.assertEqual(metadata["positive_peptide_identity_hit_count"], 3)
        self.assertEqual(metadata["nonaccepted_peptide_identity_false_hit_count"], 0)
        self.assertEqual(metadata["sibling_peptide_identity_false_hit_count"], 0)
        self.assertEqual(metadata["source_free_acceptor_identity_ready_count"], 3)
        self.assertTrue(metadata["peptide_identity_axis_narrow"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        for row in probe["rows"]:
            self.assertTrue(row["text_free_inputs_only"])
            self.assertFalse(row["production_scoring_admissible"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_heteromeric_peptide_external_hard_negative_probe_is_review_only(
        self,
    ) -> None:
        probe = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_peptide_external_hard_negative_probe_1025.json"
        )
        metadata = probe["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_peptide_external_hard_negative_probe",
        )
        self.assertTrue(metadata["review_only_feature_probe_complete"])
        self.assertTrue(metadata["review_only_feature_probe_passed"])
        self.assertEqual(
            metadata[
                "review_only_external_hard_negative_feature_non_abstention_count"
            ],
            0,
        )
        self.assertEqual(metadata["missing_expected_external_hard_negative_count"], 0)
        self.assertEqual(
            metadata["coordinate_unavailable_external_hard_negative_count"],
            0,
        )
        self.assertFalse(metadata["clean_heldout_performance_claim_permitted"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            {row["entry_id"] for row in probe["rows"]},
            EXTERNAL_HARD_NEGATIVES,
        )
        for row in probe["rows"]:
            self.assertFalse(row["review_only_feature_non_abstention"])
            self.assertEqual(row["review_only_feature_score"], 0.0)
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_heteromeric_peptide_broader_stress_audit_is_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_peptide_broader_stress_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_peptide_broader_stress_audit",
        )
        self.assertEqual(
            metadata["stress_audit_status"],
            "passes_exact_source_query_stress_but_axis_remains_narrow_review_only",
        )
        self.assertTrue(metadata["exact_source_query_exhausted"])
        self.assertEqual(metadata["exact_source_query_pdb_count"], 110)
        self.assertEqual(metadata["unreviewed_exact_query_pdb_count"], 0)
        self.assertEqual(metadata["positive_peptide_identity_hit_count"], 3)
        self.assertEqual(metadata["positive_non_peptide_substrate_chain_hit_count"], 0)
        self.assertEqual(metadata["general_substrate_identity_ready_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        for row in audit["rows"]:
            self.assertTrue(row["review_only"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_heteromeric_source_expansion_peptide_role_axis_is_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_heteromeric_source_expansion_peptide_role_axis_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_source_expansion_peptide_role_axis_audit",
        )
        self.assertEqual(
            metadata["source_expansion_peptide_role_axis_status"],
            "passes_source_expansion_controls_peptide_role_axis_review_only",
        )
        self.assertEqual(
            metadata["source_valid_expansion_peptide_role_hit_pdb_ids"],
            ["1O6K", "1O6L"],
        )
        self.assertEqual(
            metadata["nonpositive_source_expansion_control_false_hit_count"],
            0,
        )
        self.assertEqual(metadata["general_substrate_identity_ready_count"], 0)
        self.assertTrue(metadata["peptide_identity_axis_narrow"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["pdb_id"]: row for row in audit["rows"]}
        self.assertTrue(rows["1O6K"]["source_free_peptide_role_axis_rule_hit"])
        self.assertTrue(rows["1O6L"]["source_free_peptide_role_axis_rule_hit"])
        self.assertFalse(rows["2JJ2"]["source_free_peptide_role_axis_rule_hit"])
        self.assertFalse(rows["4HPU"]["source_free_peptide_role_axis_rule_hit"])
        self.assertFalse(rows["7B56"]["source_free_peptide_role_axis_rule_hit"])
        self.assertFalse(rows["7T55"]["source_free_peptide_role_axis_rule_hit"])
        self.assertFalse(rows["7T56"]["source_free_peptide_role_axis_rule_hit"])
        self.assertFalse(rows["7T57"]["source_free_peptide_role_axis_rule_hit"])
        self.assertFalse(rows["7ZDT"]["source_free_peptide_role_axis_rule_hit"])
        self.assertFalse(rows["7ZDU"]["source_free_peptide_role_axis_rule_hit"])
        self.assertFalse(rows["7ZE5"]["source_free_peptide_role_axis_rule_hit"])
        self.assertFalse(rows["9L3M"]["source_free_peptide_role_axis_rule_hit"])
        self.assertFalse(rows["9L3U"]["source_free_peptide_role_axis_rule_hit"])
        self.assertEqual(
            rows["1O6K"]["source_free_peptide_role_axis_counterevidence_reasons"],
            [],
        )
        self.assertEqual(
            rows["4HPU"]["source_free_peptide_role_axis_counterevidence_reasons"],
            [
                "candidate_acceptor_chain_not_peptide_like",
                "candidate_acceptor_chain_has_local_nucleotide_or_metal",
                "gamma_chain_not_larger_than_acceptor_chain",
            ],
        )
        self.assertEqual(
            rows["7T55"]["source_free_peptide_role_axis_counterevidence_reasons"],
            [
                "candidate_acceptor_chain_not_peptide_like",
                "candidate_acceptor_chain_has_local_nucleotide_or_metal",
                "candidate_acceptor_and_gamma_on_same_chain",
            ],
        )
        for row in audit["rows"]:
            self.assertTrue(row["review_only"])
            self.assertTrue(row["text_free_inputs_only"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_substrate_mode_gap_audit_is_review_only(self) -> None:
        audit = _load_json(
            ROOT / "artifacts" / "v3_epk_substrate_mode_gap_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(metadata["method"], "epk_substrate_mode_gap_audit")
        self.assertEqual(
            metadata["substrate_mode_gap_status"],
            "passes_review_only_modes_but_unified_substrate_identity_missing",
        )
        self.assertEqual(
            metadata["combined_peptide_mode_positive_pdb_ids"],
            ["1O6K", "1O6L", "6Z3R", "8OXM", "8OXO"],
        )
        self.assertEqual(metadata["combined_peptide_mode_false_hit_count"], 0)
        self.assertEqual(metadata["protein_substrate_mode_positive_like_count"], 3)
        self.assertTrue(metadata["peptide_modes_pass_current_controls"])
        self.assertTrue(metadata["protein_mode_passes_current_controls"])
        self.assertFalse(metadata["unified_source_free_substrate_identity_ready"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["row_type"]: row for row in audit["rows"]}
        self.assertEqual(
            rows["substrate_mode_gap_decision"]["blocker"],
            "peptide_and_protein_substrate_modes_lack_unified_source_free_identity",
        )

    def test_epk_external_source_scout_builder_keeps_rows_non_countable(
        self,
    ) -> None:
        scout = build_epk_external_protein_substrate_source_scout(
            epk_protein_substrate_source_repair_terminal_decision={
                "metadata": {
                    "method": "terminal",
                    "current_source_candidates_exhausted": True,
                }
            },
            query_payloads_by_lane={
                "fixture_lane": {
                    "metadata": {"query": "fixture", "record_count": 1},
                    "records": [
                        {
                            "accession": "PTEST",
                            "reviewed": "reviewed",
                            "ec_numbers": ["2.7.11.1"],
                            "pdb_ids": ["1ABC"],
                            "alphafold_ids": [],
                        }
                    ],
                }
            },
            entry_records_by_accession={
                "PTEST": {
                    "active_site_features": [{"begin": 10}],
                    "binding_site_features": [
                        {"begin": 1, "ligand_name": "ATP"},
                    ],
                    "catalytic_activity_comments": [
                        {
                            "reaction": (
                                "L-seryl-[protein] + ATP = "
                                "O-phospho-L-seryl-[protein] + ADP + H(+)"
                            )
                        }
                    ],
                    "cofactor_comments": [],
                }
            },
            existing_label_records=[],
        )
        self.assertEqual(scout["metadata"]["sourced_candidate_count"], 1)
        self.assertEqual(scout["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(scout["metadata"]["ready_for_label_import"])
        self.assertFalse(scout["rows"][0]["countable_label_candidate"])

    def test_epk_external_source_alternate_cocomplex_builder_can_find_review_hit(
        self,
    ) -> None:
        cif_text = """data_1ABC
loop_
_struct_ref_seq.align_id
_struct_ref_seq.ref_id
_struct_ref_seq.pdbx_PDB_id_code
_struct_ref_seq.pdbx_strand_id
_struct_ref_seq.seq_align_beg
_struct_ref_seq.pdbx_auth_seq_align_beg
_struct_ref_seq.seq_align_end
_struct_ref_seq.pdbx_auth_seq_align_end
_struct_ref_seq.pdbx_db_accession
_struct_ref_seq.db_align_beg
_struct_ref_seq.db_align_end
1 1 1ABC A 1 10 11 20 QKIN 10 20
2 2 1ABC B 1 5 5 5 QSUB 5 5
#
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.auth_atom_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_seq_id
ATOM 1 C CA ILE A 10 8.0 0.0 0.0 CA ILE A 10
ATOM 2 C CA ASP A 20 9.0 0.0 0.0 CA ASP A 20
ATOM 3 O OG SER B 5 3.0 0.0 0.0 OG SER B 5
HETATM 4 P PG ATP A 901 0.0 0.0 0.0 PG ATP A 901
HETATM 5 M MG MG A 902 0.0 0.0 1.0 MG MG A 902
#
"""
        review = build_epk_external_source_alternate_cocomplex_review(
            epk_external_protein_substrate_source_scout={
                "metadata": {"method": "fixture"},
                "rows": [
                    {
                        "sourcing_status": (
                            "sourced_pending_structure_mapping_review"
                        ),
                        "accession": "QKIN",
                        "active_site_positions": [20],
                        "atp_binding_positions": [10],
                        "pdb_ids": ["1ABC"],
                    }
                ],
            },
            target_accession="QKIN",
            acceptor_entry_records_by_accession={
                "QSUB": {
                    "modified_residue_features": [
                        {
                            "begin": 5,
                            "description": "Phosphoserine",
                            "evidence": [{"evidence_code": "ECO:0000269"}],
                        }
                    ]
                }
            },
            cif_text_by_pdb={"1ABC": cif_text},
        )
        metadata = review["metadata"]
        self.assertEqual(metadata["measurement_ready_candidate_count"], 1)
        self.assertTrue(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["countable_label_candidate_count"])
        self.assertEqual(
            metadata["alternate_cocomplex_status_counts"],
            {"measurement_ready_review_only": 1},
        )
        row = review["rows"][0]
        self.assertTrue(row["measurement_ready"])
        self.assertEqual(row["source_phosphoacceptor_within_threshold_count"], 1)
        self.assertEqual(
            row["source_phosphoacceptor_distance_candidates"][0][
                "nearest_gamma_distance_angstrom"
            ],
            3.0,
        )

    def test_epk_ligand_specific_5hvk_source_validity_builder_accepts_pair(
        self,
    ) -> None:
        cif_text = """data_5HVK
_struct.entry_id 5HVK
_struct.title 'Crystal structure of LIMK1 mutant D460N in complex with full-length cofilin-1'
#
loop_
_struct_keywords.entry_id
_struct_keywords.pdbx_keywords
_struct_keywords.text
5HVK TRANSFERASE 'kinase substrate'
#
loop_
_entity.id
_entity.type
_entity.src_method
_entity.pdbx_description
_entity.formula_weight
_entity.pdbx_number_of_molecules
_entity.pdbx_ec
_entity.pdbx_mutation
_entity.pdbx_fragment
_entity.details
1 polymer man 'LIM domain kinase 1' 1.0 1 2.7.11.1 ? ? ?
2 polymer man Cofilin-1 1.0 1 ? ? ? ?
#
loop_
_struct_ref_seq.align_id
_struct_ref_seq.ref_id
_struct_ref_seq.pdbx_PDB_id_code
_struct_ref_seq.pdbx_strand_id
_struct_ref_seq.seq_align_beg
_struct_ref_seq.pdbx_auth_seq_align_beg
_struct_ref_seq.seq_align_end
_struct_ref_seq.pdbx_auth_seq_align_end
_struct_ref_seq.pdbx_db_accession
_struct_ref_seq.db_align_beg
_struct_ref_seq.db_align_end
1 1 5HVK C 1 1 10 10 P53667 1 10
2 2 5HVK D 1 1 10 10 P23528 1 10
#
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.auth_atom_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_seq_id
HETATM 1 P PG ANP C 701 0.0 0.0 0.0 PG ANP C 701
ATOM 2 O OG SER D 3 3.0 0.0 0.0 OG SER D 3
#
"""
        review = build_epk_ligand_specific_5hvk_source_validity_review(
            epk_ligand_specific_5hvk_review_priority={
                "metadata": {
                    "method": "epk_ligand_specific_5hvk_review_priority",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [
                    {
                        "pdb_id": "5HVK",
                        "accession": "P53667",
                        "role": "source_ready_kinase_candidate",
                    },
                    {
                        "pdb_id": "5HVK",
                        "accession": "P23528",
                        "role": "cross_accession_phosphoacceptor_hit",
                    },
                ],
            },
            kinase_uniprot_entry={
                "record": {
                    "active_site_features": [{"begin": 460}],
                    "binding_site_features": [
                        {"begin": 345, "ligand_name": "ATP"}
                    ],
                    "catalytic_activity_comments": [
                        {
                            "reaction": (
                                "L-seryl-[protein] + ATP = "
                                "O-phospho-L-seryl-[protein] + ADP + H(+)"
                            )
                        }
                    ],
                }
            },
            acceptor_uniprot_entry={
                "record": {
                    "modified_residue_features": [
                        {
                            "begin": 3,
                            "description": "Phosphoserine; by NRK",
                            "evidence": [{"evidence_code": "ECO:0000269"}],
                        }
                    ]
                }
            },
            cif_text_by_pdb={"5HVK": cif_text},
        )
        metadata = review["metadata"]
        self.assertTrue(metadata["source_validated_kinase_substrate_pair"])
        self.assertEqual(metadata["measurement_ready_candidate_count"], 1)
        self.assertTrue(metadata["ready_to_measure_gamma_acceptor_distance"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["countable_label_candidate_count"])
        row = review["rows"][0]
        self.assertTrue(row["measurement_ready"])
        self.assertEqual(
            row["acceptor_distance_hits"][0]["nearest_gamma_distance_angstrom"],
            3.0,
        )

    def test_epk_ligand_specific_5hvk_control_rerun_queue_builder(
        self,
    ) -> None:
        queue = build_epk_ligand_specific_5hvk_control_rerun_queue(
            epk_ligand_specific_5hvk_source_validity_review={
                "metadata": {
                    "method": "epk_ligand_specific_5hvk_source_validity_review",
                    "target_fingerprint_id": (
                        "epk_atp_gamma_phosphoryl_transfer"
                    ),
                    "pdb_id": "5HVK",
                    "kinase_accession": "P53667",
                    "acceptor_accession": "P23528",
                    "source_validated_kinase_substrate_pair": True,
                    "measurement_ready_candidate_count": 1,
                    "nearest_source_phosphoacceptor_distance_angstrom": 4.236,
                }
            },
            epk_review_only_scoring_prototype={
                "metadata": {"method": "epk_review_only_scoring_prototype"},
                "rows": [
                    {
                        "row_type": "current_epk_positive_prototype",
                        "prototype_decision": (
                            "candidate_positive_signal_review_only_not_calibrated"
                        ),
                    },
                    {
                        "row_type": "sibling_homolog_negative_control",
                        "prototype_decision": (
                            "blocked_by_phosphohistidine_counteraxis_review_only"
                        ),
                    },
                    {
                        "row_type": "imported_external_hard_negative",
                        "prototype_decision": (
                            "external_hard_negative_abstain_missing_epk_axes_review_only"
                        ),
                    },
                ],
            },
            epk_review_only_external_hard_negative_score_probe={
                "metadata": {
                    "method": "epk_review_only_external_hard_negative_score_probe",
                    "review_only_score_probe_non_abstention_count": 0,
                    "not_a_real_scored_reaudit": True,
                }
            },
        )
        metadata = queue["metadata"]
        self.assertEqual(
            metadata["control_rerun_queue_status"],
            "ready_for_review_only_control_rerun",
        )
        self.assertTrue(metadata["ready_for_review_only_control_rerun"])
        self.assertEqual(metadata["sibling_control_row_count"], 1)
        self.assertEqual(metadata["imported_external_hard_negative_row_count"], 1)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_ligand_specific_5hvk_prototype_control_rerun_builder(
        self,
    ) -> None:
        rerun = build_epk_ligand_specific_5hvk_prototype_control_rerun(
            epk_ligand_specific_5hvk_source_validity_review={
                "metadata": {
                    "method": "epk_ligand_specific_5hvk_source_validity_review",
                    "target_fingerprint_id": (
                        "epk_atp_gamma_phosphoryl_transfer"
                    ),
                    "pdb_id": "5HVK",
                    "kinase_accession": "P53667",
                    "acceptor_accession": "P23528",
                    "source_validated_kinase_substrate_pair": True,
                    "measurement_ready_candidate_count": 1,
                    "nearest_source_phosphoacceptor_distance_angstrom": 4.236,
                    "terminal_gamma_atom_count": 1,
                    "entity_descriptions": ["MAGNESIUM ION"],
                    "kinase_has_active_site_feature": True,
                    "source_validity_status": (
                        "accepted_source_valid_kinase_substrate_cocomplex_review_only"
                    ),
                }
            },
            epk_ligand_specific_5hvk_control_rerun_queue={
                "metadata": {
                    "method": "epk_ligand_specific_5hvk_control_rerun_queue",
                    "ready_for_review_only_control_rerun": True,
                }
            },
            epk_review_only_scoring_prototype={
                "metadata": {"method": "epk_review_only_scoring_prototype"},
                "rows": [
                    {
                        "row_type": "current_epk_positive_prototype",
                        "prototype_decision": (
                            "candidate_positive_signal_review_only_not_calibrated"
                        ),
                    },
                    {
                        "row_type": "sibling_homolog_negative_control",
                        "prototype_decision": (
                            "blocked_by_phosphohistidine_counteraxis_review_only"
                        ),
                    },
                    {
                        "row_type": "imported_external_hard_negative",
                        "entry_id": "uniprot:P06744",
                        "prototype_decision": (
                            "external_hard_negative_abstain_missing_epk_axes_review_only"
                        ),
                    },
                ],
            },
            epk_review_only_external_hard_negative_score_probe={
                "metadata": {
                    "method": "epk_review_only_external_hard_negative_score_probe",
                    "review_only_score_probe_non_abstention_count": 0,
                }
            },
        )
        metadata = rerun["metadata"]
        self.assertEqual(
            metadata["control_rerun_status"],
            "passes_review_only_controls_but_scorer_blocked",
        )
        self.assertTrue(metadata["source_valid_5hvk_candidate_added"])
        self.assertEqual(metadata["positive_like_review_row_count"], 2)
        self.assertEqual(metadata["sibling_control_false_hit_count"], 0)
        self.assertEqual(
            metadata["imported_external_hard_negative_non_abstention_count"],
            0,
        )
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_5hvk_protein_substrate_axis_generalization_builder(
        self,
    ) -> None:
        audit = build_epk_5hvk_protein_substrate_axis_generalization_audit(
            epk_protein_substrate_acceptor_candidate_audit={
                "metadata": {
                    "method": "epk_protein_substrate_acceptor_candidate_audit",
                    "target_fingerprint_id": (
                        "epk_atp_gamma_phosphoryl_transfer"
                    ),
                    "current_positive_feature_hit_count": 2,
                    "current_positive_feature_miss_count": 1,
                    "ligand_analog_only_positive_miss_count": 1,
                    "ligand_analog_only_positive_miss_entry_ids": ["m_csa:640"],
                    "negative_control_false_hit_count": 0,
                }
            },
            epk_ligand_specific_5hvk_prototype_control_rerun={
                "metadata": {
                    "method": "epk_ligand_specific_5hvk_prototype_control_rerun",
                    "source_valid_5hvk_candidate_added": True,
                    "source_valid_5hvk_candidate_axis_complete": True,
                    "source_valid_5hvk_distance_angstrom": 4.236,
                    "sibling_control_false_hit_count": 0,
                    "imported_external_hard_negative_non_abstention_count": 0,
                }
            },
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["generalization_status"],
            "passes_review_only_generalization_but_not_scoring_admissible",
        )
        self.assertEqual(
            metadata["combined_protein_substrate_positive_like_count"],
            3,
        )
        self.assertFalse(
            metadata["ligand_analog_required_for_minimum_review_set"]
        )
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_protein_substrate_scorer_design_freeze_builder(
        self,
    ) -> None:
        design = build_epk_protein_substrate_scorer_design_freeze(
            epk_5hvk_protein_substrate_axis_generalization_audit={
                "metadata": {
                    "method": (
                        "epk_5hvk_protein_substrate_axis_generalization_audit"
                    ),
                    "target_fingerprint_id": (
                        "epk_atp_gamma_phosphoryl_transfer"
                    ),
                    "combined_protein_substrate_positive_like_count": 3,
                    "sibling_control_false_hit_count": 0,
                    "imported_external_hard_negative_non_abstention_count": 0,
                }
            }
        )
        metadata = design["metadata"]
        self.assertEqual(
            metadata["design_status"],
            "frozen_review_only_ready_for_diagnostic_calibration",
        )
        self.assertTrue(metadata["ready_for_review_only_calibration_diagnostic"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(
            metadata["source_authority_axes_valid_for_orphan_discovery_claims"]
        )

    def test_epk_protein_substrate_calibration_diagnostic_builder(
        self,
    ) -> None:
        diagnostic = build_epk_protein_substrate_calibration_diagnostic(
            epk_protein_substrate_scorer_design_freeze={
                "metadata": {
                    "method": "epk_protein_substrate_scorer_design_freeze",
                    "design_version": (
                        "epk_protein_substrate_scorer_design_v0_2026_05_19"
                    ),
                    "target_fingerprint_id": (
                        "epk_atp_gamma_phosphoryl_transfer"
                    ),
                    "ready_for_review_only_calibration_diagnostic": True,
                    "source_authority_axes_valid_for_orphan_discovery_claims": False,
                }
            },
            epk_ligand_specific_5hvk_prototype_control_rerun={
                "metadata": {
                    "method": "epk_ligand_specific_5hvk_prototype_control_rerun"
                },
                "rows": [
                    {
                        "row_type": "carried_current_epk_positive_prototype",
                        "entry_id": "m_csa:35",
                    },
                    {
                        "row_type": "carried_current_epk_positive_prototype",
                        "entry_id": "m_csa:640",
                    },
                    {
                        "row_type": (
                            "ligand_specific_5hvk_source_valid_positive_candidate"
                        ),
                        "pdb_id": "5HVK",
                    },
                    {
                        "row_type": "sibling_homolog_negative_control",
                        "pdb_id": "1WKL",
                    },
                    {
                        "row_type": "imported_external_hard_negative",
                        "entry_id": "uniprot:P06744",
                    },
                ],
            },
        )
        metadata = diagnostic["metadata"]
        self.assertEqual(
            metadata["diagnostic_status"],
            "blocked_review_only_calibration_diagnostic",
        )
        self.assertEqual(metadata["diagnostic_positive_full_axis_count"], 2)
        self.assertEqual(metadata["ligand_analog_excluded_positive_count"], 1)
        self.assertFalse(metadata["epk_score_computed"])

    def test_epk_source_authority_axis_replacement_gap_audit_builder(
        self,
    ) -> None:
        audit = build_epk_source_authority_axis_replacement_gap_audit(
            epk_protein_substrate_scorer_design_freeze={
                "metadata": {
                    "method": "epk_protein_substrate_scorer_design_freeze",
                    "target_fingerprint_id": (
                        "epk_atp_gamma_phosphoryl_transfer"
                    ),
                },
                "rows": [
                    {
                        "axis_id": "source_validated_protein_substrate_hydroxyl_acceptor",
                        "axis_type": "source_authority_context",
                    },
                    {
                        "axis_id": "local_metal_context",
                        "axis_type": "local_ligand_context",
                    },
                ],
            },
            epk_protein_substrate_calibration_diagnostic={
                "metadata": {
                    "method": "epk_protein_substrate_calibration_diagnostic",
                    "diagnostic_status": (
                        "passes_review_only_calibration_controls_not_real_scorer"
                    ),
                }
            },
        )
        metadata = audit["metadata"]
        self.assertEqual(metadata["replacement_gap_count"], 1)
        self.assertEqual(
            metadata["replacement_status"],
            "blocked_review_only_source_authority_axes_require_local_replacements",
        )
        self.assertFalse(metadata["ready_for_production_scoring"])

    def test_epk_local_chain_topology_acceptor_rule_builder(self) -> None:
        rule = build_epk_local_chain_topology_acceptor_replacement_rule(
            epk_chain_ligand_acceptor_disambiguation_audit={
                "metadata": {
                    "method": "epk_chain_ligand_acceptor_disambiguation_audit",
                    "target_fingerprint_id": (
                        "epk_atp_gamma_phosphoryl_transfer"
                    ),
                },
                "rows": [
                    {
                        "row_type": "current_epk_positive_prototype",
                        "entry_id": "m_csa:35",
                        "non_catalytic_chain_acceptor": True,
                    },
                    {
                        "row_type": "current_epk_positive_prototype",
                        "entry_id": "m_csa:640",
                        "ligand_analog_acceptor": True,
                    },
                    {
                        "row_type": "sibling_homolog_negative_control",
                        "pdb_id": "1WKL",
                    },
                    {
                        "row_type": "imported_external_hard_negative",
                        "entry_id": "uniprot:P06744",
                    },
                ],
            },
            epk_ligand_specific_5hvk_source_validity_review={
                "metadata": {
                    "method": "epk_ligand_specific_5hvk_source_validity_review",
                    "source_validated_kinase_substrate_pair": True,
                    "measurement_ready_candidate_count": 1,
                    "nearest_source_phosphoacceptor_distance_angstrom": 4.236,
                }
            },
            epk_source_authority_axis_replacement_gap_audit={
                "metadata": {
                    "method": "epk_source_authority_axis_replacement_gap_audit"
                }
            },
        )
        metadata = rule["metadata"]
        self.assertEqual(metadata["positive_rule_hit_count"], 2)
        self.assertEqual(metadata["ligand_analog_excluded_positive_count"], 1)
        self.assertEqual(metadata["control_false_hit_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_5hvk_local_polymer_entity_role_audit_builder(self) -> None:
        audit = build_epk_5hvk_local_polymer_entity_role_audit(
            epk_ligand_specific_5hvk_source_validity_review={
                "metadata": {
                    "method": "epk_ligand_specific_5hvk_source_validity_review",
                    "pdb_id": "5HVK",
                    "entity_descriptions": [
                        "Cofilin-1",
                        "LIM domain kinase 1",
                        "MAGNESIUM ION",
                        "PHOSPHOAMINOPHOSPHONIC ACID-ADENYLATE ESTER",
                    ],
                    "kinase_chain_ids": ["A", "C"],
                    "acceptor_chain_ids": ["B", "D"],
                    "nearest_source_phosphoacceptor_distance_angstrom": 4.236,
                }
            },
            epk_local_chain_topology_acceptor_replacement_rule={
                "metadata": {
                    "method": "epk_local_chain_topology_acceptor_replacement_rule"
                }
            },
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["audit_status"],
            "partial_local_entity_support_source_roles_still_required",
        )
        self.assertTrue(metadata["local_entity_supports_cocomplex"])
        self.assertFalse(metadata["source_authority_eliminated"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_source_free_chain_topology_role_audit_builder_blocks_risk(
        self,
    ) -> None:
        audit = build_epk_source_free_chain_topology_role_audit(
            epk_5hvk_local_polymer_entity_role_audit={
                "metadata": {
                    "method": "epk_5hvk_local_polymer_entity_role_audit",
                    "pdb_id": "5HVK",
                    "local_entity_supports_cocomplex": True,
                    "chain_sets_disjoint": True,
                    "has_adenylate_ligand_entity": True,
                    "has_magnesium_entity": True,
                    "source_authority_eliminated": False,
                }
            },
            epk_ligand_specific_substrate_cocomplex_query_probe={
                "metadata": {
                    "method": "epk_ligand_specific_substrate_cocomplex_query_probe",
                    "reviewed_pdb_count": 2,
                    "query_pdb_count": 2,
                },
                "rows": [
                    {
                        "pdb_id": "5HVK",
                        "probe_status": (
                            "source_ready_cross_accession_acceptor_hit_review_only"
                        ),
                        "acceptor_hits": [
                            {
                                "within_candidate_threshold": True,
                                "nearest_gamma_distance_angstrom": 4.236,
                            }
                        ],
                    },
                    {
                        "pdb_id": "3Q4Z",
                        "probe_status": (
                            "source_ready_same_accession_acceptor_hit_review_only"
                        ),
                        "acceptor_hits": [
                            {
                                "within_candidate_threshold": True,
                                "nearest_gamma_distance_angstrom": 5.802,
                            }
                        ],
                    },
                ],
            },
            epk_local_chain_topology_acceptor_replacement_rule={
                "metadata": {
                    "method": "epk_local_chain_topology_acceptor_replacement_rule",
                }
            },
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["audit_status"],
            "blocked_review_only_source_free_topology_role_rule_false_hit_risk",
        )
        self.assertEqual(metadata["masked_local_candidate_hit_count"], 2)
        self.assertEqual(metadata["source_valid_cross_accession_positive_count"], 1)
        self.assertEqual(metadata["known_same_accession_control_risk_count"], 1)
        self.assertFalse(metadata["source_free_role_assignment_safe"])
        self.assertFalse(metadata["source_authority_eliminated"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_heteromeric_chain_topology_signal_audit_builder_splits_controls(
        self,
    ) -> None:
        heteromeric_cif = """
data_5HVK
loop_
_struct_asym.id
_struct_asym.entity_id
C 1
D 2
#
loop_
_atom_site.group_PDB
_atom_site.label_atom_id
_atom_site.auth_atom_id
_atom_site.label_comp_id
_atom_site.auth_comp_id
_atom_site.label_asym_id
_atom_site.auth_asym_id
_atom_site.label_seq_id
_atom_site.auth_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM OG OG SER SER D D 3 3 0.0 0.0 0.0
HETATM PG PG ANP ANP C C 1 1 0.0 0.0 4.0
#
"""
        same_entity_cif = """
data_3Q4Z
loop_
_struct_asym.id
_struct_asym.entity_id
A 1
B 1
#
loop_
_atom_site.group_PDB
_atom_site.label_atom_id
_atom_site.auth_atom_id
_atom_site.label_comp_id
_atom_site.auth_comp_id
_atom_site.label_asym_id
_atom_site.auth_asym_id
_atom_site.label_seq_id
_atom_site.auth_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM OG1 OG1 THR THR B B 423 423 0.0 0.0 0.0
HETATM PG PG ANP ANP A A 1 1 0.0 0.0 4.0
#
"""
        audit = build_epk_heteromeric_chain_topology_signal_audit(
            epk_source_free_chain_topology_role_audit={
                "metadata": {
                    "method": "epk_source_free_chain_topology_role_audit",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                    "masked_local_candidate_hit_count": 2,
                }
            },
            epk_ligand_specific_substrate_cocomplex_query_probe={
                "metadata": {
                    "method": "epk_ligand_specific_substrate_cocomplex_query_probe",
                    "reviewed_pdb_count": 2,
                    "query_pdb_count": 2,
                },
                "rows": [
                    {
                        "pdb_id": "5HVK",
                        "probe_status": (
                            "source_ready_cross_accession_acceptor_hit_review_only"
                        ),
                        "acceptor_hits": [
                            {
                                "candidate_chain_name": "D",
                                "candidate_auth_seq_id": "3",
                                "candidate_residue_code": "SER",
                                "nearest_gamma_distance_angstrom": 4.0,
                                "same_as_source_accession": False,
                                "within_candidate_threshold": True,
                            }
                        ],
                    },
                    {
                        "pdb_id": "3Q4Z",
                        "probe_status": (
                            "source_ready_same_accession_acceptor_hit_review_only"
                        ),
                        "acceptor_hits": [
                            {
                                "candidate_chain_name": "B",
                                "candidate_auth_seq_id": "423",
                                "candidate_residue_code": "THR",
                                "nearest_gamma_distance_angstrom": 4.0,
                                "same_as_source_accession": True,
                                "within_candidate_threshold": True,
                            }
                        ],
                    },
                ],
            },
            cif_text_by_pdb={
                "5HVK": heteromeric_cif,
                "3Q4Z": same_entity_cif,
            },
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["audit_status"],
            "passes_current_hit_controls_but_insufficient_positive_coverage_review_only",
        )
        self.assertEqual(metadata["evaluated_hit_control_count"], 2)
        self.assertEqual(metadata["heteromeric_signal_positive_like_count"], 1)
        self.assertEqual(
            metadata["same_accession_control_signal_false_hit_count"], 0
        )
        self.assertTrue(metadata["current_hit_controls_passed"])
        self.assertFalse(metadata["minimum_positive_coverage_met"])
        self.assertEqual(
            metadata["full_probe_heteromeric_candidate_pdb_ids"],
            ["5HVK"],
        )
        self.assertTrue(metadata["source_free_5hvk_role_direction_supported"])
        self.assertFalse(metadata["source_authority_eliminated"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_heteromeric_positive_coverage_candidate_scout_builder(
        self,
    ) -> None:
        heteromeric_cif = """
data_1NEW
loop_
_struct_asym.id
_struct_asym.entity_id
A 1
B 2
#
loop_
_atom_site.group_PDB
_atom_site.label_atom_id
_atom_site.auth_atom_id
_atom_site.label_comp_id
_atom_site.auth_comp_id
_atom_site.label_asym_id
_atom_site.auth_asym_id
_atom_site.label_seq_id
_atom_site.auth_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM OG OG SER SER B B 12 12 0.0 0.0 0.0
HETATM PG PG ANP ANP A A 1 1 0.0 0.0 4.0
#
"""
        same_entity_cif = """
data_1SAME
loop_
_struct_asym.id
_struct_asym.entity_id
A 1
B 1
#
loop_
_atom_site.group_PDB
_atom_site.label_atom_id
_atom_site.auth_atom_id
_atom_site.label_comp_id
_atom_site.auth_comp_id
_atom_site.label_asym_id
_atom_site.auth_asym_id
_atom_site.label_seq_id
_atom_site.auth_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM OG OG SER SER B B 12 12 0.0 0.0 0.0
HETATM PG PG ANP ANP A A 1 1 0.0 0.0 4.0
#
"""
        scout = build_epk_heteromeric_positive_coverage_candidate_scout(
            epk_heteromeric_chain_topology_signal_audit={
                "metadata": {
                    "method": "epk_heteromeric_chain_topology_signal_audit",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                    "heteromeric_signal_positive_like_count": 1,
                    "full_probe_heteromeric_candidate_pdb_ids": ["5HVK"],
                }
            },
            candidate_pdb_ids=["1NEW", "1SAME"],
            source_query="fixture next candidates",
            cif_text_by_pdb={
                "1NEW": heteromeric_cif,
                "1SAME": same_entity_cif,
            },
        )
        metadata = scout["metadata"]
        self.assertEqual(
            metadata["positive_coverage_status"],
            "source_validation_pending_for_broadened_heteromeric_candidates_review_only",
        )
        self.assertEqual(metadata["input_candidate_count"], 2)
        self.assertEqual(metadata["heteromeric_candidate_structure_count"], 1)
        self.assertEqual(metadata["heteromeric_candidate_pdb_ids"], ["1NEW"])
        self.assertTrue(metadata["source_validation_queue_ready"])
        self.assertFalse(metadata["minimum_positive_coverage_met"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = {row["pdb_id"]: row for row in scout["rows"]}
        self.assertEqual(
            rows["1NEW"]["candidate_status"],
            "heteromeric_candidate_source_validation_pending_review_only",
        )
        self.assertEqual(
            rows["1SAME"]["candidate_status"],
            "no_heteromeric_candidate_hit_review_only",
        )
        self.assertIn(
            "source_validation_pending_for_heteromeric_candidate",
            rows["1NEW"]["remaining_blockers"],
        )

    def test_epk_heteromeric_candidate_source_validation_review_builder(
        self,
    ) -> None:
        source_valid_cif = """
data_1ATM
_struct.title 'ATM(Q2971A) activated by oxidative stress in complex with Mg AMP-PNP and p53 peptide'
#
"""
        source_valid_keyword_cif = """
data_1ATK
_struct.title
#
_struct_keywords.entry_id 1ATK
_struct_keywords.text 'Kinase, Ataxia-Telangiectasia Mutated, ATM, p53, SIGNALING PROTEIN'
_struct_keywords.pdbx_keywords 'SIGNALING PROTEIN'
#
loop_
_entity.id
_entity.type
_entity.src_method
_entity.pdbx_description
1 polymer man 'Cellular tumor antigen p53'
2 polymer man 'Serine-protein kinase ATM'
#
"""
        ambiguous_cif = """
data_1BME
_struct.title 'Crystal structure of the BRAF:MEK1 kinases in complex with AMPPNP'
#
"""
        pkb_gsk3_cif = """
data_1PKG
_struct.title 'Structure of activated form of PKB kinase domain S474D with GSK3 peptide and AMP-PNP'
#
"""
        pkb_gsk3_raw_cif = """
data_1PGR
_citation.title 'Crystal Structure of an Activated Akt/Protein Kinase B Ternary Complex with Gsk-3 Peptide and AMP-Pnp'
#
"""
        review = build_epk_heteromeric_candidate_source_validation_review(
            epk_heteromeric_positive_coverage_candidate_scout={
                "metadata": {
                    "method": "epk_heteromeric_positive_coverage_candidate_scout",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [
                    {
                        "pdb_id": "1ATM",
                        "candidate_status": "heteromeric_candidate_source_validation_pending_review_only",
                        "heteromeric_candidate_hit_count": 1,
                        "heteromeric_candidate_hits": [
                            {"nearest_gamma_distance_angstrom": 3.5}
                        ],
                    },
                    {
                        "pdb_id": "1BME",
                        "candidate_status": "heteromeric_candidate_source_validation_pending_review_only",
                        "heteromeric_candidate_hit_count": 1,
                        "heteromeric_candidate_hits": [
                            {"nearest_gamma_distance_angstrom": 4.0}
                        ],
                    },
                    {
                        "pdb_id": "1ATK",
                        "candidate_status": "heteromeric_candidate_source_validation_pending_review_only",
                        "heteromeric_candidate_hit_count": 1,
                        "heteromeric_candidate_hits": [
                            {"nearest_gamma_distance_angstrom": 3.7}
                        ],
                    },
                    {
                        "pdb_id": "1PKG",
                        "candidate_status": "heteromeric_candidate_source_validation_pending_review_only",
                        "heteromeric_candidate_hit_count": 1,
                        "heteromeric_candidate_hits": [
                            {"nearest_gamma_distance_angstrom": 3.6}
                        ],
                    },
                    {
                        "pdb_id": "1PGR",
                        "candidate_status": "heteromeric_candidate_source_validation_pending_review_only",
                        "heteromeric_candidate_hit_count": 1,
                        "heteromeric_candidate_hits": [
                            {"nearest_gamma_distance_angstrom": 3.4}
                        ],
                    },
                ],
            },
            cif_text_by_pdb={
                "1ATM": source_valid_cif,
                "1ATK": source_valid_keyword_cif,
                "1BME": ambiguous_cif,
                "1PKG": pkb_gsk3_cif,
                "1PGR": pkb_gsk3_raw_cif,
            },
        )
        metadata = review["metadata"]
        self.assertEqual(metadata["source_validated_new_candidate_count"], 4)
        self.assertEqual(
            metadata["source_validated_unique_pair_ids"],
            ["atm_p53", "pkb_gsk3"],
        )
        self.assertEqual(metadata["ambiguous_candidate_count"], 1)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        rows = {row["pdb_id"]: row for row in review["rows"]}
        self.assertEqual(
            rows["1ATM"]["source_validation_status"],
            "accepted_source_valid_heteromeric_kinase_substrate_review_only",
        )
        self.assertEqual(
            rows["1ATK"]["source_validation_status"],
            "accepted_source_valid_heteromeric_kinase_substrate_review_only",
        )
        self.assertEqual(
            rows["1BME"]["source_validation_status"],
            "blocked_ambiguous_kinase_kinase_role_direction_review_only",
        )
        self.assertEqual(rows["1PKG"]["source_pair_id"], "pkb_gsk3")
        self.assertEqual(rows["1PGR"]["source_pair_id"], "pkb_gsk3")

    def test_epk_heteromeric_source_valid_candidate_distance_sample_builder(
        self,
    ) -> None:
        sample = build_epk_heteromeric_source_valid_candidate_gamma_distance_sample(
            epk_heteromeric_candidate_source_validation_review={
                "metadata": {
                    "method": "epk_heteromeric_candidate_source_validation_review",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [
                    {
                        "pdb_id": "1ATM",
                        "source_pair_id": "atm_p53",
                        "source_validated_positive_like": True,
                        "candidate_hits": [
                            {
                                "candidate_chain_name": "F",
                                "candidate_auth_seq_id": "15",
                                "candidate_residue_code": "SER",
                                "candidate_atom_name": "OG",
                                "acceptor_entity_id": "1",
                                "gamma_associated_polymer_entity_id": "2",
                                "gamma_ligand_code": "ANP",
                                "gamma_atom_name": "PG",
                                "nearest_gamma_distance_angstrom": 3.5,
                            }
                        ],
                    },
                    {
                        "pdb_id": "1BME",
                        "source_pair_id": None,
                        "source_validated_positive_like": False,
                        "candidate_hits": [
                            {"nearest_gamma_distance_angstrom": 4.0}
                        ],
                    },
                ],
            }
        )
        metadata = sample["metadata"]
        self.assertEqual(metadata["source_validated_candidate_count"], 1)
        self.assertEqual(metadata["measured_candidate_count"], 1)
        self.assertEqual(metadata["measured_candidate_pdb_ids"], ["1ATM"])
        self.assertEqual(metadata["measured_unique_pair_ids"], ["atm_p53"])
        self.assertTrue(metadata["all_source_valid_candidates_measured"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(sample["rows"][0]["nearest_gamma_acceptor_distance_angstrom"], 3.5)

    def test_epk_heteromeric_broader_counteraxis_control_builder(
        self,
    ) -> None:
        audit = build_epk_heteromeric_broader_counteraxis_control_audit(
            epk_heteromeric_positive_coverage_candidate_scout={
                "metadata": {
                    "method": "epk_heteromeric_positive_coverage_candidate_scout",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [
                    {
                        "pdb_id": "1POS",
                        "heteromeric_candidate_hits": [
                            {"nearest_gamma_distance_angstrom": 4.0}
                        ],
                    },
                    {
                        "pdb_id": "1NEG",
                        "heteromeric_candidate_hits": [
                            {"nearest_gamma_distance_angstrom": 4.5}
                        ],
                    },
                    {
                        "pdb_id": "1ABS",
                        "heteromeric_candidate_hits": [],
                    },
                ],
            },
            epk_heteromeric_candidate_source_validation_review={
                "metadata": {
                    "method": "epk_heteromeric_candidate_source_validation_review",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [
                    {
                        "pdb_id": "1POS",
                        "source_validated_positive_like": True,
                        "source_validation_status": (
                            "accepted_source_valid_heteromeric_kinase_substrate_review_only"
                        ),
                    },
                    {
                        "pdb_id": "1NEG",
                        "source_validated_positive_like": False,
                        "source_validation_status": (
                            "blocked_ambiguous_kinase_kinase_role_direction_review_only"
                        ),
                    },
                ],
            },
            epk_heteromeric_acceptor_chain_counteraxis_audit={
                "metadata": {
                    "method": "epk_heteromeric_acceptor_chain_counteraxis_audit",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [
                    {
                        "pdb_id": "1POS",
                        "counteraxis_decision": (
                            "source_free_counteraxis_retains_source_valid_review_positive"
                        ),
                        "source_free_counteraxis_hit": True,
                    },
                    {
                        "pdb_id": "1NEG",
                        "counteraxis_decision": (
                            "source_free_counteraxis_blocks_nonaccepted_rule_hit"
                        ),
                        "source_free_counteraxis_hit": False,
                    },
                ],
            },
            epk_sibling_control_artifacts=[
                {
                    "metadata": {
                        "reviewed_sibling_family_id": "ndk",
                        "reviewed_sibling_family_name": (
                            "Nucleoside diphosphate kinases"
                        ),
                    },
                    "rows": [
                        {
                            "pdb_id": "2NDK",
                            "family_id": "ndk",
                            "gamma_to_mapped_histidine_distance_measured": True,
                            "gamma_capable_nucleotide_codes": ["ATP"],
                            "same_chain_hydroxyl_candidate_threshold_hits_angstrom": [
                                6.0
                            ],
                        },
                        {
                            "pdb_id": "2WAIT",
                            "family_id": "ndk",
                            "measurement_status": (
                                "family_specific_homolog_mapping_not_measurement_ready"
                            ),
                        },
                    ],
                }
            ],
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["broader_counteraxis_status"],
            "passes_broader_review_controls_not_scoring_admissible",
        )
        self.assertEqual(metadata["broader_heteromeric_reviewed_structure_count"], 3)
        self.assertEqual(metadata["broader_heteromeric_initial_hit_count"], 2)
        self.assertEqual(metadata["blocked_nonaccepted_rule_hit_count"], 1)
        self.assertEqual(metadata["retained_source_valid_hit_count"], 1)
        self.assertEqual(metadata["sibling_control_row_count"], 2)
        self.assertEqual(metadata["sibling_same_chain_hydroxyl_hit_count"], 1)
        self.assertEqual(metadata["sibling_counteraxis_blocked_hit_count"], 1)
        self.assertEqual(metadata["sibling_residual_false_hit_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_heteromeric_acceptor_identity_rule_probe_builder(
        self,
    ) -> None:
        probe = build_epk_heteromeric_acceptor_identity_rule_probe(
            epk_heteromeric_acceptor_identity_gap_audit={
                "metadata": {
                    "method": "epk_heteromeric_acceptor_identity_gap_audit",
                    "retained_role_hit_count": 1,
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [
                    {
                        "pdb_id": "1POS",
                        "source_pair_id": "kinase_substrate",
                        "candidate_acceptor_residues_review_context": [
                            {"candidate_residue_code": "SER"}
                        ],
                    }
                ],
            },
            epk_heteromeric_broader_counteraxis_control_audit={
                "metadata": {
                    "method": (
                        "epk_heteromeric_broader_counteraxis_control_audit"
                    ),
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [
                    {
                        "row_type": "heteromeric_broader_counteraxis_control",
                        "pdb_id": "1NEG",
                        "initial_topology_gamma_rule_hit": True,
                        "source_free_counteraxis_hit": False,
                    },
                    {
                        "row_type": "sibling_broader_counteraxis_control",
                        "pdb_id": "2NDK",
                        "family_id": "ndk",
                        "same_chain_hydroxyl_threshold_hit": True,
                        "source_free_counteraxis_blocks_hit": True,
                    },
                ],
            },
        )
        metadata = probe["metadata"]
        self.assertEqual(
            metadata["identity_rule_status"],
            "passes_current_controls_but_generic_identity_axis_weak_review_only",
        )
        self.assertEqual(metadata["positive_identity_rule_hit_count"], 1)
        self.assertEqual(metadata["nonaccepted_blocked_before_identity_rule_count"], 1)
        self.assertEqual(metadata["nonaccepted_identity_rule_hit_count"], 0)
        self.assertEqual(
            metadata["sibling_same_chain_blocked_before_identity_rule_count"], 1
        )
        self.assertEqual(metadata["sibling_identity_rule_false_hit_count"], 0)
        self.assertTrue(metadata["generic_identity_axis_weak"])
        self.assertEqual(metadata["source_free_acceptor_identity_ready_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_heteromeric_peptide_acceptor_identity_probe_builder(
        self,
    ) -> None:
        def cif_with_chains(
            pdb_id: str,
            *,
            acceptor_chain: str,
            acceptor_len: int,
            gamma_chain: str,
            gamma_len: int,
            acceptor_ligands: list[str] | None = None,
        ) -> str:
            lines = [
                f"data_{pdb_id}",
                "loop_",
                "_atom_site.group_PDB",
                "_atom_site.auth_comp_id",
                "_atom_site.label_comp_id",
                "_atom_site.auth_atom_id",
                "_atom_site.label_atom_id",
                "_atom_site.auth_asym_id",
                "_atom_site.label_asym_id",
                "_atom_site.auth_seq_id",
                "_atom_site.label_seq_id",
                "_atom_site.Cartn_x",
                "_atom_site.Cartn_y",
                "_atom_site.Cartn_z",
            ]
            for index in range(1, acceptor_len + 1):
                lines.append(
                    f"ATOM SER SER OG OG {acceptor_chain} {acceptor_chain} {index} {index} 0.0 0.0 0.0"
                )
            for index in range(1, gamma_len + 1):
                lines.append(
                    f"ATOM LYS LYS NZ NZ {gamma_chain} {gamma_chain} {index} {index} 10.0 0.0 0.0"
                )
            for ligand in acceptor_ligands or []:
                lines.append(
                    f"HETATM {ligand} {ligand} PG PG {acceptor_chain} {acceptor_chain} 900 900 1.0 0.0 0.0"
                )
            lines.append("#")
            return "\n".join(lines)

        probe = build_epk_heteromeric_peptide_acceptor_identity_probe(
            epk_heteromeric_acceptor_identity_gap_audit={
                "metadata": {
                    "method": "epk_heteromeric_acceptor_identity_gap_audit",
                    "retained_role_hit_count": 1,
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [{"pdb_id": "1POS", "source_pair_id": "kinase_substrate"}],
            },
            epk_heteromeric_candidate_source_validation_review={
                "metadata": {
                    "method": "epk_heteromeric_candidate_source_validation_review",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [
                    {
                        "pdb_id": "1POS",
                        "candidate_hits": [
                            {
                                "candidate_chain_name": "B",
                                "candidate_auth_seq_id": "3",
                                "candidate_residue_code": "SER",
                                "gamma_associated_polymer_chain_name": "A",
                                "nearest_gamma_distance_angstrom": 3.2,
                            }
                        ],
                    },
                    {
                        "pdb_id": "1NEG",
                        "candidate_hits": [
                            {
                                "candidate_chain_name": "A",
                                "candidate_auth_seq_id": "5",
                                "candidate_residue_code": "SER",
                                "gamma_associated_polymer_chain_name": "A",
                                "nearest_gamma_distance_angstrom": 3.1,
                            }
                        ],
                    },
                ],
            },
            epk_heteromeric_broader_counteraxis_control_audit={
                "metadata": {
                    "method": "epk_heteromeric_broader_counteraxis_control_audit",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [
                    {
                        "row_type": "heteromeric_broader_counteraxis_control",
                        "pdb_id": "1NEG",
                        "initial_topology_gamma_rule_hit": True,
                        "source_free_counteraxis_hit": False,
                    }
                ],
            },
            epk_sibling_control_artifacts=[
                {
                    "metadata": {
                        "method": "epk_sibling_control_homolog_gamma_distance_sample",
                    },
                    "rows": [
                        {
                            "pdb_id": "2NDK",
                            "family_id": "ndk",
                            "same_chain_hydroxyl_distance_rows": [
                                {
                                    "hydroxyl_chain_name": "C",
                                    "chain_id": "C",
                                    "hydroxyl_resid": "12",
                                    "hydroxyl_residue_code": "SER",
                                    "distance_angstrom": 3.8,
                                }
                            ],
                        }
                    ],
                }
            ],
            cif_text_by_pdb={
                "1POS": cif_with_chains(
                    "1POS",
                    acceptor_chain="B",
                    acceptor_len=7,
                    gamma_chain="A",
                    gamma_len=60,
                ),
                "1NEG": cif_with_chains(
                    "1NEG",
                    acceptor_chain="A",
                    acceptor_len=80,
                    gamma_chain="A",
                    gamma_len=80,
                    acceptor_ligands=["ANP", "MG"],
                ),
                "2NDK": cif_with_chains(
                    "2NDK",
                    acceptor_chain="C",
                    acceptor_len=80,
                    gamma_chain="C",
                    gamma_len=80,
                ),
            },
        )
        metadata = probe["metadata"]
        self.assertEqual(
            metadata["peptide_identity_axis_status"],
            "passes_current_controls_peptide_like_acceptor_identity_review_only",
        )
        self.assertEqual(metadata["positive_peptide_identity_hit_count"], 1)
        self.assertEqual(metadata["nonaccepted_peptide_identity_false_hit_count"], 0)
        self.assertEqual(metadata["sibling_peptide_identity_false_hit_count"], 0)
        self.assertEqual(metadata["source_free_acceptor_identity_ready_count"], 1)
        self.assertTrue(metadata["peptide_identity_axis_narrow"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_heteromeric_peptide_external_hard_negative_probe_builder(
        self,
    ) -> None:
        def external_cif(
            *,
            gamma_chain_len: int = 0,
            acceptor_chain_len: int = 20,
            include_gamma: bool = False,
        ) -> str:
            lines = [
                "data_ext",
                "loop_",
                "_atom_site.group_PDB",
                "_atom_site.auth_comp_id",
                "_atom_site.label_comp_id",
                "_atom_site.auth_atom_id",
                "_atom_site.label_atom_id",
                "_atom_site.auth_asym_id",
                "_atom_site.label_asym_id",
                "_atom_site.auth_seq_id",
                "_atom_site.label_seq_id",
                "_atom_site.Cartn_x",
                "_atom_site.Cartn_y",
                "_atom_site.Cartn_z",
            ]
            for index in range(1, gamma_chain_len + 1):
                lines.append(
                    f"ATOM LYS LYS NZ NZ A A {index} {index} 10.0 0.0 0.0"
                )
            for index in range(1, acceptor_chain_len + 1):
                lines.append(
                    f"ATOM SER SER OG OG B B {index} {index} 3.0 0.0 0.0"
                )
            if include_gamma:
                lines.append("HETATM ANP ANP PG PG A A 900 900 0.0 0.0 0.0")
            lines.append("#")
            return "\n".join(lines)

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            abstain_path = root / "abstain.cif"
            hit_path = root / "hit.cif"
            abstain_path.write_text(external_cif(), encoding="utf-8")
            hit_path.write_text(
                external_cif(
                    gamma_chain_len=60,
                    acceptor_chain_len=7,
                    include_gamma=True,
                ),
                encoding="utf-8",
            )
            probe = build_epk_heteromeric_peptide_external_hard_negative_probe(
                epk_heteromeric_peptide_acceptor_identity_probe={
                    "metadata": {
                        "method": "epk_heteromeric_peptide_acceptor_identity_probe",
                        "target_fingerprint_id": (
                            "epk_atp_gamma_phosphoryl_transfer"
                        ),
                        "candidate_threshold_angstrom": 6.0,
                        "max_peptide_chain_residue_count": 40,
                        "peptide_identity_axis_status": (
                            "passes_current_controls_peptide_like_acceptor_identity_review_only"
                        ),
                        "source_free_acceptor_identity_ready_count": 3,
                    }
                },
                external_hard_negative_inverse_gate_scores=[
                    {
                        "metadata": {"method": "external_inverse_fixture"},
                        "rows": [
                            {
                                "entry_id": "uniprot:ABSTAIN",
                                "accession": "ABSTAIN",
                                "coordinate_path": str(abstain_path),
                                "out_of_scope_inverse_gate": {
                                    "inverse_gate_status": "passed",
                                    "max_current_fingerprint_score": 0.1,
                                },
                            },
                            {
                                "entry_id": "uniprot:HIT",
                                "accession": "HIT",
                                "coordinate_path": str(hit_path),
                                "out_of_scope_inverse_gate": {
                                    "inverse_gate_status": "passed",
                                    "max_current_fingerprint_score": 0.1,
                                },
                            },
                        ],
                    }
                ],
                imported_external_entry_ids=["uniprot:ABSTAIN", "uniprot:HIT"],
            )
        metadata = probe["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_heteromeric_peptide_external_hard_negative_probe",
        )
        self.assertFalse(metadata["review_only_feature_probe_passed"])
        self.assertEqual(
            metadata[
                "review_only_external_hard_negative_feature_non_abstention_count"
            ],
            1,
        )
        self.assertEqual(
            metadata[
                "review_only_external_hard_negative_feature_non_abstention_entry_ids"
            ],
            ["uniprot:HIT"],
        )
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        rows = {row["entry_id"]: row for row in probe["rows"]}
        self.assertEqual(rows["uniprot:ABSTAIN"]["gamma_atom_count"], 0)
        self.assertFalse(
            rows["uniprot:ABSTAIN"]["review_only_feature_non_abstention"]
        )
        self.assertTrue(rows["uniprot:HIT"]["review_only_feature_non_abstention"])

    def test_epk_heteromeric_peptide_broader_stress_audit_builder(
        self,
    ) -> None:
        audit = build_epk_heteromeric_peptide_broader_stress_audit(
            epk_ligand_specific_substrate_cocomplex_query_probe={
                "metadata": {
                    "method": "epk_ligand_specific_substrate_cocomplex_query_probe",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [{"pdb_id": "1AAA"}, {"pdb_id": "1AAB"}],
            },
            epk_heteromeric_positive_coverage_candidate_scout={
                "metadata": {
                    "method": "epk_heteromeric_positive_coverage_candidate_scout",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                    "heteromeric_candidate_structure_count": 1,
                },
                "rows": [{"pdb_id": "2AAA"}],
            },
            epk_heteromeric_peptide_acceptor_identity_probe={
                "metadata": {
                    "method": "epk_heteromeric_peptide_acceptor_identity_probe",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                    "max_peptide_chain_residue_count": 40,
                },
                "rows": [
                    {
                        "row_type": (
                            "heteromeric_peptide_acceptor_identity_candidate"
                        ),
                        "pdb_id": "2AAA",
                        "source_pair_id": "kinase_substrate",
                        "acceptor_chain_residue_count": 7,
                        "peptide_like_acceptor_identity_rule_hit": True,
                    },
                    {
                        "row_type": (
                            "heteromeric_nonaccepted_peptide_identity_control"
                        ),
                        "pdb_id": "2AAB",
                        "peptide_like_acceptor_identity_rule_hit": False,
                        "peptide_acceptor_identity_rule_status": (
                            "nonaccepted_control_blocked_by_peptide_identity_rule"
                        ),
                    },
                    {
                        "row_type": "sibling_peptide_identity_control",
                        "pdb_id": "3AAA",
                        "peptide_like_acceptor_identity_rule_hit": False,
                    },
                ],
            },
            exact_source_query_pdb_ids=["1AAA", "1AAB", "2AAA"],
            source_query="fixture exact query",
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["stress_audit_status"],
            "passes_exact_source_query_stress_but_axis_remains_narrow_review_only",
        )
        self.assertTrue(metadata["exact_source_query_exhausted"])
        self.assertEqual(metadata["unreviewed_exact_query_pdb_count"], 0)
        self.assertEqual(metadata["positive_peptide_identity_hit_count"], 1)
        self.assertEqual(metadata["positive_non_peptide_substrate_chain_hit_count"], 0)
        self.assertEqual(metadata["general_substrate_identity_ready_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_source_expansion_peptide_role_axis_builder(
        self,
    ) -> None:
        source_free_positive_cif = """
data_1POS
loop_
_atom_site.group_PDB
_atom_site.label_atom_id
_atom_site.auth_atom_id
_atom_site.label_comp_id
_atom_site.auth_comp_id
_atom_site.label_asym_id
_atom_site.auth_asym_id
_atom_site.label_seq_id
_atom_site.auth_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM CA CA ALA ALA A A 1 1 0.0 0.0 0.0
ATOM CA CA ALA ALA A A 2 2 1.0 0.0 0.0
ATOM CA CA ALA ALA A A 3 3 2.0 0.0 0.0
ATOM OG OG SER SER C C 9 9 0.0 0.0 3.5
HETATM PG PG ANP ANP A A 1 1 0.0 0.0 0.0
HETATM MG MG MG MG A A 2 2 0.0 1.0 0.0
#
"""
        nonpositive_same_chain_cif = """
data_1NEG
loop_
_atom_site.group_PDB
_atom_site.label_atom_id
_atom_site.auth_atom_id
_atom_site.label_comp_id
_atom_site.auth_comp_id
_atom_site.label_asym_id
_atom_site.auth_asym_id
_atom_site.label_seq_id
_atom_site.auth_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM CA CA ALA ALA A A 1 1 0.0 0.0 0.0
ATOM CA CA ALA ALA A A 2 2 1.0 0.0 0.0
ATOM OG1 OG1 THR THR A A 3 3 0.0 0.0 3.0
HETATM PG PG ATP ATP A A 1 1 0.0 0.0 0.0
HETATM MG MG MG MG A A 2 2 0.0 1.0 0.0
#
"""
        audit = build_epk_heteromeric_source_expansion_peptide_role_axis_audit(
            epk_heteromeric_peptide_acceptor_identity_probe={
                "metadata": {
                    "method": "epk_heteromeric_peptide_acceptor_identity_probe",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                    "current_controls_passed_review_only": True,
                }
            },
            epk_heteromeric_peptide_external_hard_negative_probe={
                "metadata": {
                    "method": (
                        "epk_heteromeric_peptide_external_hard_negative_probe"
                    ),
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                    "review_only_feature_probe_passed": True,
                    "review_only_external_hard_negative_feature_non_abstention_count": 0,
                }
            },
            epk_heteromeric_source_expansion_source_validation_reviews=[
                {
                    "metadata": {
                        "method": "epk_heteromeric_candidate_source_validation_review"
                    },
                    "rows": [
                        {
                            "pdb_id": "1POS",
                            "source_pair_id": "kinase_peptide",
                            "source_validated_positive_like": True,
                            "source_validation_status": (
                                "accepted_source_valid_heteromeric_kinase_substrate_review_only"
                            ),
                            "candidate_hits": [
                                {
                                    "candidate_chain_name": "C",
                                    "candidate_auth_seq_id": "9",
                                    "candidate_residue_code": "SER",
                                    "gamma_associated_polymer_chain_name": "A",
                                    "nearest_gamma_distance_angstrom": 3.5,
                                }
                            ],
                        },
                        {
                            "pdb_id": "1NEG",
                            "source_validated_positive_like": False,
                            "source_validation_status": (
                                "blocked_source_context_insufficient_review_only"
                            ),
                            "candidate_hits": [
                                {
                                    "candidate_chain_name": "A",
                                    "candidate_auth_seq_id": "3",
                                    "candidate_residue_code": "THR",
                                    "gamma_associated_polymer_chain_name": "A",
                                    "nearest_gamma_distance_angstrom": 3.0,
                                }
                            ],
                        },
                    ],
                }
            ],
            max_peptide_chain_residue_count=2,
            cif_text_by_pdb={
                "1POS": source_free_positive_cif,
                "1NEG": nonpositive_same_chain_cif,
            },
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["source_expansion_peptide_role_axis_status"],
            "passes_source_expansion_controls_peptide_role_axis_review_only",
        )
        self.assertEqual(
            metadata["source_valid_expansion_peptide_role_hit_pdb_ids"],
            ["1POS"],
        )
        self.assertEqual(
            metadata["nonpositive_source_expansion_control_false_hit_count"],
            0,
        )
        self.assertEqual(metadata["general_substrate_identity_ready_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        rows = {row["pdb_id"]: row for row in audit["rows"]}
        self.assertTrue(rows["1POS"]["source_free_peptide_role_axis_rule_hit"])
        self.assertFalse(rows["1NEG"]["source_free_peptide_role_axis_rule_hit"])

    def test_epk_substrate_mode_gap_audit_builder(self) -> None:
        audit = build_epk_substrate_mode_gap_audit(
            epk_heteromeric_peptide_acceptor_identity_probe={
                "metadata": {
                    "method": "epk_heteromeric_peptide_acceptor_identity_probe",
                    "nonaccepted_control_false_hit_count": 0,
                    "sibling_control_false_hit_count": 0,
                },
                "rows": [
                    {
                        "row_type": "heteromeric_peptide_acceptor_identity_candidate",
                        "pdb_id": "6Z3R",
                        "peptide_like_acceptor_identity_rule_hit": True,
                    },
                    {
                        "row_type": "heteromeric_peptide_acceptor_identity_candidate",
                        "pdb_id": "8OXM",
                        "peptide_like_acceptor_identity_rule_hit": True,
                    },
                    {
                        "row_type": "heteromeric_peptide_acceptor_identity_candidate",
                        "pdb_id": "8OXO",
                        "peptide_like_acceptor_identity_rule_hit": True,
                    },
                ],
            },
            epk_heteromeric_source_expansion_peptide_role_axis_audit={
                "metadata": {
                    "method": (
                        "epk_heteromeric_source_expansion_peptide_role_axis_audit"
                    ),
                    "source_valid_expansion_peptide_role_hit_pdb_ids": [
                        "1O6K",
                        "1O6L",
                    ],
                    "nonpositive_source_expansion_control_false_hit_count": 0,
                    "general_substrate_identity_ready_count": 0,
                }
            },
            epk_5hvk_protein_substrate_axis_generalization_audit={
                "metadata": {
                    "method": "epk_5hvk_protein_substrate_axis_generalization_audit",
                    "combined_protein_substrate_positive_like_count": 3,
                    "sibling_control_false_hit_count": 0,
                    "imported_external_hard_negative_non_abstention_count": 0,
                    "feature_admissible_for_production_scoring": False,
                }
            },
            epk_heteromeric_peptide_external_hard_negative_probe={
                "metadata": {
                    "method": "epk_heteromeric_peptide_external_hard_negative_probe",
                    "review_only_external_hard_negative_feature_non_abstention_count": 0,
                }
            },
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["substrate_mode_gap_status"],
            "passes_review_only_modes_but_unified_substrate_identity_missing",
        )
        self.assertEqual(metadata["combined_peptide_mode_positive_count"], 5)
        self.assertTrue(metadata["peptide_modes_pass_current_controls"])
        self.assertTrue(metadata["protein_mode_passes_current_controls"])
        self.assertFalse(metadata["unified_source_free_substrate_identity_ready"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_external_source_lower_priority_ligand_builder_blocks_analog(
        self,
    ) -> None:
        review = build_epk_external_source_lower_priority_ligand_sourcing_review(
            epk_external_source_structure_mapping_review={
                "metadata": {"method": "mapping_fixture"},
                "rows": [
                    {
                        "accession": "QLOW",
                        "entry_id": "uniprot:QLOW",
                        "pdb_id": "1LOW",
                        "mapping_review_status": (
                            "direct_position_mapping_ready_ligand_context_incomplete_review_only"
                        ),
                        "mapped_residue_positions": [{"chain_name": "A"}],
                        "local_ligand_codes": [],
                        "local_cofactor_families": [],
                        "structure_ligand_codes": ["AGS", "MG"],
                        "structure_cofactor_families": ["metal_ion"],
                    }
                ],
            },
            epk_external_protein_substrate_source_scout={
                "metadata": {"method": "scout_fixture"},
                "rows": [
                    {
                        "accession": "QLOW",
                        "pdb_ids": ["1LOW"],
                    }
                ],
            },
        )
        metadata = review["metadata"]
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertEqual(
            metadata["ligand_sourcing_status_counts"],
            {
                "inactive_analog_metal_only_needs_policy_or_alternate_review_only": 1
            },
        )
        row = review["rows"][0]
        self.assertFalse(row["measurement_ready"])
        self.assertIn("analog_policy_not_active", row["remaining_blockers"])

    def test_epk_midlength_protein_role_counteraxis_builder_blocks_false_hit(
        self,
    ) -> None:
        audit = build_epk_midlength_protein_role_counteraxis_audit(
            epk_source_free_protein_substrate_role_discriminator_stress_audit={
                "metadata": {
                    "method": "stress_fixture",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [
                    {
                        "row_type": "source_expansion_protein_role_stress",
                        "pdb_id": "7B56",
                        "source_validated_positive_like": False,
                        "protein_substrate_role_stress_decision": (
                            "nonpositive_source_expansion_protein_role_false_hit"
                        ),
                        "relaxed_folded_protein_role_rule_hit": True,
                        "acceptor_chain_residue_count": 68,
                    },
                    {
                        "row_type": "source_expansion_protein_role_stress",
                        "pdb_id": "1PRO",
                        "source_validated_positive_like": True,
                        "protein_substrate_role_stress_decision": (
                            "source_valid_expansion_protein_role_hit_review_only"
                        ),
                        "relaxed_folded_protein_role_rule_hit": True,
                        "acceptor_chain_residue_count": 180,
                    },
                ],
            },
            epk_heteromeric_source_valid_candidate_gamma_distance_sample={
                "metadata": {
                    "method": (
                        "epk_heteromeric_source_valid_candidate_gamma_distance_sample"
                    ),
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                },
                "rows": [
                    {
                        "pdb_id": "1PEP",
                        "source_pair_id": "kinase_peptide",
                        "source_validated_positive_like": True,
                        "measurement_status": (
                            "source_valid_heteromeric_gamma_distance_measured_review_only"
                        ),
                        "distance_candidates": [
                            {
                                "candidate_chain_name": "B",
                                "gamma_associated_polymer_chain_name": "A",
                                "acceptor_chain_residue_count": 7,
                                "nearest_gamma_distance_angstrom": 3.2,
                            }
                        ],
                    }
                ],
            },
        )
        metadata = audit["metadata"]
        self.assertEqual(metadata["blocked_midlength_false_hit_pdb_ids"], ["7B56"])
        self.assertEqual(metadata["residual_protein_role_false_hit_count"], 0)
        self.assertEqual(metadata["source_valid_protein_role_retained_pdb_ids"], ["1PRO"])
        self.assertEqual(metadata["source_valid_short_or_peptide_mode_pdb_ids"], ["1PEP"])
        self.assertTrue(metadata["protein_discriminator_generalization_ready"])
        rows = {row["pdb_id"]: row for row in audit["rows"]}
        self.assertFalse(rows["7B56"]["repaired_protein_role_rule_hit"])
        self.assertTrue(rows["1PRO"]["repaired_protein_role_rule_hit"])
        self.assertTrue(rows["1PEP"]["short_or_peptide_mode_acceptor_hit"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["epk_score_computed"])

    def test_epk_external_source_terminal_decision_builder_closes_empty_passes(
        self,
    ) -> None:
        decision = build_epk_external_source_scout_pass_terminal_decision(
            epk_external_protein_substrate_source_scouts=[
                {
                    "metadata": {
                        "sourced_candidate_count": 1,
                        "sourced_candidate_accessions": ["QA"],
                    }
                },
                {
                    "metadata": {
                        "sourced_candidate_count": 1,
                        "sourced_candidate_accessions": ["QB"],
                    }
                },
                {
                    "metadata": {
                        "sourced_candidate_count": 1,
                        "sourced_candidate_accessions": ["QC"],
                    }
                },
            ],
            epk_external_source_structure_mapping_reviews=[
                {"metadata": {"structure_row_count": 1}},
                {"metadata": {"structure_row_count": 1}},
                {"metadata": {"structure_row_count": 1}},
            ],
            epk_external_source_ligand_sourcing_reviews=[
                {"metadata": {"measurement_ready_candidate_count": 0}},
                {"metadata": {"measurement_ready_candidate_count": 0}},
                {"metadata": {"measurement_ready_candidate_count": 0}},
            ],
        )
        metadata = decision["metadata"]
        self.assertEqual(
            metadata["terminal_decision"],
            "current_three_pass_external_source_surface_exhausted_review_only",
        )
        self.assertTrue(metadata["current_source_candidates_exhausted"])
        self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_epk_external_source_mapping_uses_struct_ref_seq_auth_residues(
        self,
    ) -> None:
        cif_text = """data_1ABC
loop_
_struct_ref_seq.align_id
_struct_ref_seq.ref_id
_struct_ref_seq.pdbx_PDB_id_code
_struct_ref_seq.pdbx_strand_id
_struct_ref_seq.seq_align_beg
_struct_ref_seq.pdbx_auth_seq_align_beg
_struct_ref_seq.seq_align_end
_struct_ref_seq.pdbx_auth_seq_align_end
_struct_ref_seq.pdbx_db_accession
_struct_ref_seq.db_align_beg
_struct_ref_seq.db_align_end
1 1 1ABC A 1 100 30 129 QTEST 1 30
#
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.auth_atom_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_seq_id
ATOM 1 C CA ALA A 100 0.0 0.0 0.0 CA ALA A 109
ATOM 2 C CA LYS A 109 1.0 0.0 0.0 CA LYS A 100
#
"""
        review = build_epk_external_source_structure_mapping_review(
            epk_external_protein_substrate_source_scout={
                "metadata": {"method": "fixture"},
                "rows": [
                    {
                        "sourcing_status": (
                            "sourced_pending_structure_mapping_review"
                        ),
                        "candidate_priority_rank": 1,
                        "accession": "QTEST",
                        "entry_id": "uniprot:QTEST",
                        "lane_id": "fixture_lane",
                        "active_site_positions": [10],
                        "atp_binding_positions": [],
                        "pdb_ids": ["1ABC"],
                    }
                ],
            },
            max_candidates=1,
            max_pdbs_per_candidate=1,
            cif_text_by_pdb={"1ABC": cif_text},
        )
        row = review["rows"][0]
        self.assertTrue(row["direct_position_mapping_ready"])
        self.assertEqual(
            row["direct_position_mapping_basis"],
            "struct_ref_seq_uniprot_position_mapping",
        )
        self.assertEqual(row["mapped_residue_positions"][0]["resid"], "109")
        self.assertEqual(row["mapped_residue_positions"][0]["code"], "ALA")
        self.assertEqual(
            row["mapping_review_status"],
            "direct_position_mapping_ready_ligand_context_incomplete_review_only",
        )

    def test_epk_family_specific_template_validation_stays_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_family_specific_mapping_template_validation_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_family_specific_mapping_template_validation_review",
        )
        self.assertTrue(metadata["template_validation_ready"])
        self.assertEqual(
            metadata["validated_template_family_ids"],
            ["atp_grasp", "pfka", "pfkb"],
        )
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        for row in review["rows"]:
            self.assertTrue(row["validated_by_downstream_mapping"])
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

    def test_epk_m_csa640_alternate_gamma_review_stays_review_only(self) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_m_csa640_alternate_gamma_geometry_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_m_csa640_alternate_gamma_geometry_review",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_entry_id"], "m_csa:640")
        self.assertEqual(metadata["reviewed_pdb_id"], "3TM0")
        self.assertTrue(metadata["alternate_gamma_geometry_review_complete"])
        self.assertEqual(metadata["alternate_gamma_geometry_reviewed_count"], 1)
        self.assertEqual(
            metadata["alternate_gamma_geometry_supports_positive_axis_count"],
            1,
        )
        self.assertEqual(
            metadata["observed_alternate_gamma_distance_min_angstrom"],
            3.558,
        )
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        row = review["rows"][0]
        self.assertEqual(
            row["review_status"],
            "alternate_gamma_to_acceptor_analog_distance_reviewed_review_only",
        )
        self.assertEqual(row["pdb_id"], "3TM0")
        self.assertEqual(row["acceptor_ligand_code"], "B31")
        self.assertEqual(row["gamma_to_acceptor_distance_angstrom"], 3.558)
        self.assertTrue(
            row["alternate_gamma_geometry_supports_positive_axis_review_only"]
        )
        self.assertFalse(row["production_scoring_admissible"])
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
        self.assertEqual(metadata["alternate_gamma_geometry_reviewed_row_count"], 1)
        self.assertEqual(metadata["gamma_measured_or_reviewed_row_count"], 3)
        self.assertEqual(
            metadata["source_epk_m_csa640_alternate_gamma_geometry_review_method"],
            "epk_m_csa640_alternate_gamma_geometry_review",
        )
        self.assertTrue(metadata["m_csa640_alternate_gamma_geometry_review_complete"])
        self.assertEqual(metadata["m_csa640_alternate_gamma_geometry_support_count"], 1)
        self.assertEqual(metadata["m_csa640_alternate_gamma_distance_min_angstrom"], 3.558)
        self.assertEqual(
            metadata["source_epk_substrate_acceptor_counteraxis_prototype_method"],
            "epk_substrate_acceptor_counteraxis_prototype",
        )
        self.assertTrue(
            metadata["substrate_acceptor_counteraxis_decision_surface_changed"]
        )
        self.assertEqual(metadata["substrate_acceptor_counteraxis_positive_like_count"], 3)
        self.assertEqual(metadata["substrate_acceptor_counteraxis_blocked_count"], 20)
        self.assertIn(
            "source_supported_acceptor_axis_is_review_context_not_predictive",
            metadata["substrate_acceptor_counteraxis_weak_axes"],
        )
        self.assertEqual(
            metadata["source_epk_text_free_acceptor_feature_gap_audit_method"],
            "epk_text_free_acceptor_feature_gap_audit",
        )
        self.assertEqual(
            metadata["text_free_acceptor_candidate_feature_status"],
            "blocked_review_only",
        )
        self.assertEqual(
            metadata["text_free_acceptor_negative_control_false_hit_count"],
            11,
        )
        self.assertEqual(
            metadata["text_free_acceptor_false_hit_family_ids"],
            ["atp_grasp", "ndk", "pfka", "pfkb"],
        )
        self.assertFalse(
            metadata["text_free_acceptor_feature_admissible_for_scoring"]
        )
        self.assertEqual(
            metadata[
                "source_epk_protein_substrate_acceptor_candidate_audit_method"
            ],
            "epk_protein_substrate_acceptor_candidate_audit",
        )
        self.assertEqual(
            metadata["protein_substrate_acceptor_positive_hit_count"],
            2,
        )
        self.assertEqual(
            metadata["protein_substrate_acceptor_positive_miss_count"],
            1,
        )
        self.assertEqual(
            metadata[
                "protein_substrate_acceptor_ligand_analog_only_miss_entry_ids"
            ],
            ["m_csa:640"],
        )
        self.assertEqual(
            metadata[
                "protein_substrate_acceptor_negative_control_false_hit_count"
            ],
            0,
        )
        self.assertFalse(
            metadata[
                "protein_substrate_acceptor_feature_passes_current_review_controls"
            ]
        )
        self.assertEqual(
            metadata["source_epk_ligand_analog_policy_blocker_decision_method"],
            "epk_ligand_analog_policy_blocker_decision",
        )
        self.assertEqual(
            metadata["ligand_analog_policy_decision"],
            "do_not_use_ligand_analog_as_production_acceptor_evidence",
        )
        self.assertEqual(metadata["ligand_analog_dependency_count"], 1)
        self.assertEqual(metadata["ligand_analog_dependency_entry_ids"], ["m_csa:640"])
        self.assertEqual(metadata["ligand_analog_production_admissible_count"], 0)
        self.assertEqual(
            metadata["source_epk_ligand_specific_5hvk_source_validity_review_method"],
            "epk_ligand_specific_5hvk_source_validity_review",
        )
        self.assertEqual(
            metadata["ligand_specific_5hvk_source_validity_status"],
            "accepted_source_valid_kinase_substrate_cocomplex_review_only",
        )
        self.assertTrue(
            metadata["ligand_specific_5hvk_source_validated_kinase_substrate_pair"]
        )
        self.assertEqual(
            metadata["ligand_specific_5hvk_measurement_ready_candidate_count"],
            1,
        )
        self.assertEqual(
            metadata[
                "ligand_specific_5hvk_nearest_source_phosphoacceptor_distance_angstrom"
            ],
            4.236,
        )
        self.assertTrue(metadata["ligand_specific_5hvk_ready_to_rerun_controls"])
        self.assertEqual(
            metadata["source_epk_ligand_specific_5hvk_control_rerun_queue_method"],
            "epk_ligand_specific_5hvk_control_rerun_queue",
        )
        self.assertEqual(
            metadata["ligand_specific_5hvk_control_rerun_queue_status"],
            "ready_for_review_only_control_rerun",
        )
        self.assertTrue(metadata["ligand_specific_5hvk_control_rerun_ready"])
        self.assertEqual(
            metadata["ligand_specific_5hvk_control_rerun_sibling_control_row_count"],
            20,
        )
        self.assertEqual(
            metadata["ligand_specific_5hvk_control_rerun_imported_external_row_count"],
            3,
        )
        self.assertTrue(
            metadata["ligand_specific_5hvk_control_rerun_not_real_scored_reaudit"]
        )
        self.assertEqual(
            metadata[
                "source_epk_ligand_specific_5hvk_prototype_control_rerun_method"
            ],
            "epk_ligand_specific_5hvk_prototype_control_rerun",
        )
        self.assertEqual(
            metadata["ligand_specific_5hvk_prototype_control_rerun_status"],
            "passes_review_only_controls_but_scorer_blocked",
        )
        self.assertTrue(metadata["ligand_specific_5hvk_candidate_added_to_prototype"])
        self.assertEqual(
            metadata[
                "ligand_specific_5hvk_prototype_positive_like_review_row_count"
            ],
            4,
        )
        self.assertEqual(
            metadata[
                "ligand_specific_5hvk_prototype_sibling_control_false_hit_count"
            ],
            0,
        )
        self.assertEqual(
            metadata["ligand_specific_5hvk_prototype_external_non_abstention_count"],
            0,
        )
        self.assertEqual(
            metadata[
                "source_epk_5hvk_protein_substrate_axis_generalization_audit_method"
            ],
            "epk_5hvk_protein_substrate_axis_generalization_audit",
        )
        self.assertEqual(
            metadata[
                "ligand_specific_5hvk_protein_substrate_axis_generalization_status"
            ],
            "passes_review_only_generalization_but_not_scoring_admissible",
        )
        self.assertEqual(
            metadata[
                "ligand_specific_5hvk_combined_protein_substrate_positive_like_count"
            ],
            3,
        )
        self.assertFalse(
            metadata[
                "ligand_specific_5hvk_ligand_analog_required_for_minimum_review_set"
            ]
        )
        self.assertEqual(
            metadata["source_epk_source_free_chain_topology_role_audit_method"],
            "epk_source_free_chain_topology_role_audit",
        )
        self.assertEqual(
            metadata["source_free_chain_topology_audit_status"],
            "blocked_review_only_source_free_topology_role_rule_false_hit_risk",
        )
        self.assertEqual(
            metadata["source_free_chain_topology_masked_local_candidate_hit_count"],
            4,
        )
        self.assertEqual(
            metadata["source_free_chain_topology_same_accession_control_risk_count"],
            3,
        )
        self.assertEqual(
            metadata[
                "source_free_chain_topology_same_accession_control_risk_pdb_ids"
            ],
            ["3Q4Z", "4I94", "5XD6"],
        )
        self.assertFalse(metadata["source_free_chain_topology_role_assignment_safe"])
        self.assertEqual(
            metadata["source_epk_heteromeric_chain_topology_signal_audit_method"],
            "epk_heteromeric_chain_topology_signal_audit",
        )
        self.assertEqual(
            metadata["heteromeric_chain_topology_audit_status"],
            "passes_current_hit_controls_but_insufficient_positive_coverage_review_only",
        )
        self.assertEqual(
            metadata["heteromeric_chain_topology_positive_like_count"],
            1,
        )
        self.assertEqual(
            metadata["heteromeric_chain_topology_positive_like_pdb_ids"],
            ["5HVK"],
        )
        self.assertEqual(
            metadata["heteromeric_chain_topology_same_accession_false_hit_count"],
            0,
        )
        self.assertEqual(
            metadata["heteromeric_chain_topology_same_accession_abstention_pdb_ids"],
            ["3Q4Z", "4I94", "5XD6"],
        )
        self.assertTrue(
            metadata["heteromeric_chain_topology_current_hit_controls_passed"]
        )
        self.assertFalse(
            metadata["heteromeric_chain_topology_minimum_positive_coverage_met"]
        )
        self.assertEqual(
            metadata[
                "heteromeric_chain_topology_full_probe_candidate_structure_count"
            ],
            1,
        )
        self.assertEqual(
            metadata["heteromeric_chain_topology_full_probe_candidate_pdb_ids"],
            ["5HVK"],
        )
        self.assertTrue(
            metadata["heteromeric_chain_topology_5hvk_role_direction_supported"]
        )
        self.assertFalse(
            metadata["heteromeric_chain_topology_source_authority_eliminated"]
        )
        self.assertEqual(
            metadata[
                "source_epk_heteromeric_positive_coverage_candidate_scout_method"
            ],
            "epk_heteromeric_positive_coverage_candidate_scout",
        )
        self.assertEqual(
            metadata["heteromeric_positive_coverage_status"],
            "source_validation_pending_for_broadened_heteromeric_candidates_review_only",
        )
        self.assertEqual(
            metadata["heteromeric_positive_coverage_input_candidate_count"],
            50,
        )
        self.assertEqual(
            metadata["heteromeric_positive_coverage_candidate_structure_count"],
            6,
        )
        self.assertEqual(
            metadata["heteromeric_positive_coverage_candidate_pdb_ids"],
            ["6Z3R", "7M0T", "7M0W", "8OXM", "8OXO", "8ZN6"],
        )
        self.assertTrue(
            metadata["heteromeric_positive_coverage_source_validation_queue_ready"]
        )
        self.assertFalse(
            metadata["heteromeric_positive_coverage_minimum_positive_coverage_met"]
        )
        self.assertEqual(
            metadata[
                "source_epk_heteromeric_candidate_source_validation_review_method"
            ],
            "epk_heteromeric_candidate_source_validation_review",
        )
        self.assertEqual(
            metadata["heteromeric_source_validation_reviewed_candidate_count"],
            6,
        )
        self.assertEqual(
            metadata["heteromeric_source_validation_accepted_candidate_count"],
            3,
        )
        self.assertEqual(
            metadata["heteromeric_source_validation_accepted_candidate_pdb_ids"],
            ["6Z3R", "8OXM", "8OXO"],
        )
        self.assertEqual(
            metadata["heteromeric_source_validation_unique_pair_ids"],
            ["atm_p53", "smg1_upf1"],
        )
        self.assertEqual(
            metadata["heteromeric_source_validation_ambiguous_candidate_count"],
            2,
        )
        self.assertEqual(
            metadata["heteromeric_source_validation_rejected_candidate_count"],
            1,
        )
        self.assertTrue(
            metadata[
                "heteromeric_source_validation_minimum_positive_coverage_met_review_only"
            ]
        )
        self.assertEqual(
            metadata[
                "source_epk_heteromeric_source_valid_candidate_gamma_distance_sample_method"
            ],
            "epk_heteromeric_source_valid_candidate_gamma_distance_sample",
        )
        self.assertEqual(
            metadata["heteromeric_distance_sample_status"],
            "source_valid_heteromeric_candidates_measured_review_only",
        )
        self.assertEqual(
            metadata["heteromeric_distance_source_validated_candidate_count"],
            3,
        )
        self.assertEqual(metadata["heteromeric_distance_measured_candidate_count"], 3)
        self.assertEqual(
            metadata["heteromeric_distance_measured_candidate_pdb_ids"],
            ["6Z3R", "8OXM", "8OXO"],
        )
        self.assertEqual(
            metadata["heteromeric_distance_measured_unique_pair_ids"],
            ["atm_p53", "smg1_upf1"],
        )
        self.assertEqual(metadata["heteromeric_distance_min_angstrom"], 3.482)
        self.assertEqual(metadata["heteromeric_distance_max_angstrom"], 5.607)
        self.assertTrue(
            metadata[
                "heteromeric_distance_minimum_positive_coverage_measured_review_only"
            ]
        )
        self.assertEqual(
            metadata["source_epk_heteromeric_source_valid_control_rerun_method"],
            "epk_heteromeric_source_valid_control_rerun",
        )
        self.assertEqual(
            metadata["heteromeric_control_rerun_status"],
            "passes_review_only_controls_but_scorer_blocked",
        )
        self.assertEqual(
            metadata["heteromeric_control_positive_like_review_row_count"], 7
        )
        self.assertEqual(
            metadata["heteromeric_control_source_valid_candidate_row_count"], 3
        )
        self.assertEqual(
            metadata["heteromeric_control_source_valid_pdb_ids"],
            ["6Z3R", "8OXM", "8OXO"],
        )
        self.assertEqual(
            metadata["heteromeric_control_source_valid_unique_pair_ids"],
            ["atm_p53", "smg1_upf1"],
        )
        self.assertEqual(metadata["heteromeric_control_ambiguous_candidate_count"], 2)
        self.assertEqual(metadata["heteromeric_control_rejected_candidate_count"], 1)
        self.assertEqual(metadata["heteromeric_control_sibling_false_hit_count"], 0)
        self.assertEqual(metadata["heteromeric_control_external_non_abstention_count"], 0)
        self.assertEqual(
            metadata["source_epk_heteromeric_text_free_axis_gap_audit_method"],
            "epk_heteromeric_text_free_axis_gap_audit",
        )
        self.assertEqual(
            metadata["heteromeric_text_free_axis_gap_audit_status"],
            "blocked_review_only_source_free_role_acceptor_axes_missing",
        )
        self.assertEqual(
            metadata[
                "heteromeric_text_free_source_authority_dependent_positive_like_count"
            ],
            4,
        )
        self.assertEqual(
            metadata["heteromeric_text_free_local_geometry_axis_present_count"],
            4,
        )
        self.assertEqual(
            metadata["heteromeric_text_free_role_assignment_ready_count"], 0
        )
        self.assertEqual(
            metadata["heteromeric_text_free_acceptor_identity_ready_count"], 0
        )
        self.assertEqual(
            metadata[
                "heteromeric_text_free_production_admissible_positive_like_count"
            ],
            0,
        )
        self.assertEqual(
            metadata["source_epk_heteromeric_source_free_role_rule_probe_method"],
            "epk_heteromeric_source_free_role_rule_probe",
        )
        self.assertEqual(
            metadata["heteromeric_source_free_rule_status"],
            "blocked_review_only_source_free_rule_false_hit_risk",
        )
        self.assertEqual(metadata["heteromeric_source_free_rule_hit_count"], 6)
        self.assertEqual(metadata["heteromeric_source_free_accepted_rule_hit_count"], 3)
        self.assertEqual(metadata["heteromeric_source_free_ambiguous_rule_hit_count"], 2)
        self.assertEqual(metadata["heteromeric_source_free_rejected_rule_hit_count"], 1)
        self.assertEqual(metadata["heteromeric_source_free_nonaccepted_rule_hit_count"], 3)
        self.assertEqual(
            metadata["heteromeric_source_free_nonaccepted_rule_hit_pdb_ids"],
            ["7M0T", "7M0W", "8ZN6"],
        )
        self.assertEqual(
            metadata[
                "source_epk_heteromeric_acceptor_chain_counteraxis_audit_method"
            ],
            "epk_heteromeric_acceptor_chain_counteraxis_audit",
        )
        self.assertEqual(
            metadata["heteromeric_acceptor_counteraxis_status"],
            "passes_current_review_controls_not_scoring_admissible",
        )
        self.assertEqual(
            metadata["heteromeric_acceptor_counteraxis_initial_hit_count"], 6
        )
        self.assertEqual(
            metadata[
                "heteromeric_acceptor_counteraxis_retained_source_valid_hit_count"
            ],
            3,
        )
        self.assertEqual(
            metadata[
                "heteromeric_acceptor_counteraxis_blocked_nonaccepted_hit_count"
            ],
            3,
        )
        self.assertEqual(
            metadata["heteromeric_acceptor_counteraxis_blocked_nonaccepted_pdb_ids"],
            ["7M0T", "7M0W", "8ZN6"],
        )
        self.assertEqual(
            metadata[
                "heteromeric_acceptor_counteraxis_residual_nonaccepted_hit_count"
            ],
            0,
        )
        self.assertEqual(
            metadata["heteromeric_acceptor_counteraxis_accepted_lost_count"], 0
        )
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
        self.assertIn(
            metadata["negative_control_repair_review_family_id"],
            {"atp_grasp", "ndk", "pfka", "pfkb"},
        )
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
        self.assertTrue(metadata["negative_control_repair_review_unresolved_entry_ids"])
        self.assertLessEqual(
            set(metadata["negative_control_repair_review_unresolved_entry_ids"]),
            set(metadata["negative_control_repair_review_unresolved_entry_ids_all"]),
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
        self.assertEqual(
            metadata[
                "source_epk_sibling_control_homolog_gamma_distance_sample_method"
            ],
            "epk_sibling_control_homolog_gamma_distance_sample",
        )
        self.assertEqual(
            metadata["negative_control_homolog_distance_sample_family_id"], "ndk"
        )
        self.assertEqual(
            metadata["negative_control_homolog_distance_sample_measured_count"], 4
        )
        self.assertEqual(
            metadata["negative_control_homolog_distance_sample_axis"],
            "mapped_phosphohistidine_site_not_hydroxyl_acceptor",
        )
        self.assertEqual(
            metadata["source_epk_family_specific_mapping_template_review_method"],
            "epk_family_specific_mapping_template_review",
        )
        self.assertEqual(
            metadata["source_epk_family_specific_mapping_template_review_methods"],
            ["epk_family_specific_mapping_template_review"],
        )
        self.assertEqual(metadata["negative_control_family_template_family_id"], "pfkb")
        self.assertEqual(
            metadata["negative_control_family_template_family_ids"],
            ["atp_grasp", "pfka", "pfkb"],
        )
        self.assertEqual(
            metadata["negative_control_family_template_seeded_entry_count"],
            2,
        )
        self.assertEqual(
            metadata["negative_control_family_template_seeded_entry_count_total"],
            5,
        )
        self.assertEqual(metadata["negative_control_family_template_residue_count"], 11)
        self.assertEqual(
            metadata["negative_control_family_template_residue_count_total"],
            35,
        )
        self.assertEqual(
            metadata["negative_control_family_template_review_status"],
            "template_seeded_mapping_algorithm_pending_review_only",
        )
        self.assertEqual(
            metadata["negative_control_family_template_review_status_counts"],
            {"template_seeded_mapping_algorithm_pending_review_only": 3},
        )
        self.assertFalse(metadata["negative_control_family_template_mapping_ready"])
        self.assertEqual(metadata["negative_control_family_template_ready_family_ids"], [])
        self.assertEqual(
            metadata[
                "source_epk_family_specific_mapping_template_validation_review_method"
            ],
            "epk_family_specific_mapping_template_validation_review",
        )
        self.assertEqual(
            metadata["negative_control_family_template_validated_family_ids"],
            ["atp_grasp", "pfka", "pfkb"],
        )
        self.assertTrue(metadata["negative_control_family_template_validation_ready"])
        self.assertEqual(
            metadata["source_epk_family_specific_homolog_mapping_review_method"],
            "epk_family_specific_homolog_mapping_review",
        )
        self.assertEqual(
            metadata["negative_control_family_specific_mapping_family_id"], "pfkb"
        )
        self.assertEqual(
            metadata["negative_control_family_specific_mapping_ready_family_ids"],
            ["atp_grasp", "pfka", "pfkb"],
        )
        self.assertEqual(
            metadata["negative_control_family_specific_mapping_status_counts"],
            {
                "family_specific_acid_base_mapping_unresolved": 16,
                "family_specific_homolog_mapping_ready_for_distance_measurement_review_only": 16,
            },
        )
        self.assertEqual(
            metadata[
                "negative_control_family_specific_mapping_ready_structure_count_total"
            ],
            16,
        )
        self.assertEqual(
            metadata[
                "source_epk_family_specific_homolog_gamma_distance_sample_method"
            ],
            "epk_family_specific_homolog_gamma_distance_sample",
        )
        self.assertEqual(
            metadata[
                "negative_control_family_specific_distance_sample_measured_family_ids"
            ],
            ["atp_grasp", "pfka", "pfkb"],
        )
        self.assertEqual(
            metadata[
                "negative_control_family_specific_distance_sample_measured_count_total"
            ],
            16,
        )
        self.assertEqual(
            metadata["negative_control_family_specific_distance_sample_axis"],
            "family_specific_sibling_acid_base_counteraxis_not_epk_label",
        )
        self.assertEqual(
            metadata["source_epk_unified_substrate_identity_rule_probe_method"],
            "epk_unified_substrate_identity_rule_probe",
        )
        self.assertEqual(
            metadata["unified_substrate_identity_rule_status"],
            "passes_current_controls_unified_substrate_identity_review_only",
        )
        self.assertTrue(
            metadata["unified_substrate_identity_passes_current_review_controls"]
        )
        self.assertEqual(metadata["unified_substrate_identity_positive_hit_count"], 8)
        self.assertEqual(metadata["unified_substrate_identity_control_false_hit_count"], 0)
        self.assertEqual(
            metadata[
                "unified_substrate_identity_external_hard_negative_non_abstention_count"
            ],
            0,
        )
        self.assertEqual(
            metadata["source_epk_general_substrate_identity_gap_audit_method"],
            "epk_general_substrate_identity_gap_audit",
        )
        self.assertEqual(
            metadata["general_substrate_identity_relaxed_polymer_status"],
            "fails_closed_relaxed_polymer_rule_has_nonpositive_false_hit",
        )
        self.assertEqual(
            metadata["general_substrate_identity_relaxed_polymer_false_hit_pdb_ids"],
            ["7B56"],
        )
        self.assertEqual(
            metadata[
                "source_epk_length_band_substrate_identity_counteraxis_audit_method"
            ],
            "epk_length_band_substrate_identity_counteraxis_audit",
        )
        self.assertEqual(
            metadata["length_band_substrate_identity_status"],
            "passes_source_expansion_subset_by_blocking_relaxed_false_hits_review_only",
        )
        self.assertEqual(metadata["length_band_substrate_identity_false_hit_count"], 0)
        self.assertEqual(
            metadata[
                "length_band_substrate_identity_blocked_relaxed_false_hit_pdb_ids"
            ],
            ["7B56"],
        )
        self.assertEqual(
            metadata["source_epk_length_band_external_hard_negative_review_method"],
            "epk_length_band_external_hard_negative_review",
        )
        self.assertEqual(
            metadata["length_band_external_hard_negative_review_status"],
            "passes_review_only_length_band_external_hard_negative_abstention",
        )
        self.assertEqual(
            metadata["length_band_external_hard_negative_non_abstention_count"],
            0,
        )
        self.assertTrue(
            metadata["length_band_external_hard_negative_not_real_scored_reaudit"]
        )
        self.assertEqual(
            metadata[
                "source_epk_source_free_protein_substrate_role_discriminator_audit_method"
            ],
            "epk_source_free_protein_substrate_role_discriminator_audit",
        )
        self.assertEqual(
            metadata["protein_substrate_role_discriminator_status"],
            "passes_current_controls_but_review_only_not_production_admissible",
        )
        self.assertEqual(
            metadata["protein_substrate_role_discriminator_hit_pdb_ids"],
            ["1IR3", "2PHK", "5HVK"],
        )
        self.assertEqual(
            metadata["protein_substrate_role_discriminator_control_false_hit_count"],
            0,
        )
        self.assertEqual(
            metadata[
                "protein_substrate_role_discriminator_external_non_abstention_count"
            ],
            0,
        )
        self.assertTrue(
            metadata["protein_substrate_role_discriminator_length_band_not_general"]
        )
        self.assertEqual(
            metadata[
                "source_epk_source_free_protein_substrate_role_discriminator_stress_audit_method"
            ],
            "epk_source_free_protein_substrate_role_discriminator_stress_audit",
        )
        self.assertEqual(
            metadata["protein_substrate_role_stress_status"],
            "fails_closed_review_only_source_expansion_protein_role_false_hit",
        )
        self.assertEqual(metadata["protein_substrate_role_stress_false_hit_count"], 1)
        self.assertEqual(
            metadata["protein_substrate_role_stress_false_hit_pdb_ids"],
            ["7B56"],
        )
        self.assertFalse(
            metadata["protein_substrate_role_stress_generalization_ready"]
        )
        self.assertEqual(
            metadata["midlength_protein_role_counteraxis_status"],
            "blocks_current_midlength_false_hit_but_no_broad_positive_review_only",
        )
        self.assertEqual(
            metadata["midlength_protein_role_blocked_false_hit_pdb_ids"],
            ["7B56"],
        )
        self.assertEqual(
            metadata[
                "midlength_protein_role_source_valid_short_or_peptide_mode_pdb_ids"
            ],
            ["6Z3R", "8OXM", "8OXO"],
        )
        self.assertEqual(
            metadata["midlength_protein_role_source_valid_retained_count"], 0
        )
        self.assertFalse(metadata["midlength_protein_role_generalization_ready"])
        self.assertEqual(
            metadata["source_epk_unified_review_only_scoring_prototype_method"],
            "epk_unified_review_only_scoring_prototype",
        )
        self.assertEqual(
            metadata["unified_review_only_scoring_prototype_status"],
            "fail_closed_review_only",
        )
        self.assertTrue(
            metadata["unified_review_only_scoring_passes_current_controls"]
        )
        self.assertEqual(
            metadata["unified_review_only_scoring_positive_full_score_count"], 8
        )
        self.assertEqual(
            metadata["unified_review_only_scoring_control_false_non_abstention_count"],
            0,
        )
        self.assertEqual(
            metadata[
                "unified_review_only_scoring_external_hard_negative_non_abstention_count"
            ],
            0,
        )
        self.assertTrue(metadata["unified_review_only_score_computed"])
        self.assertEqual(
            metadata["source_epk_unified_prototype_broad_stress_audit_method"],
            "epk_unified_prototype_broad_stress_audit",
        )
        self.assertEqual(
            metadata["unified_prototype_broad_stress_status"],
            "bounded_stress_has_source_validation_counterexamples_review_only",
        )
        self.assertEqual(
            metadata[
                "unified_prototype_broad_stress_outside_query_reviewed_candidate_count"
            ],
            299,
        )
        self.assertEqual(
            metadata["unified_prototype_broad_stress_blocked_or_rejected_pdb_ids"],
            [
                "2JJ2",
                "4HPU",
                "7B56",
                "7T55",
                "7T56",
                "7T57",
                "7ZDT",
                "7ZDU",
                "7ZE5",
                "9L3M",
                "9L3U",
            ],
        )
        self.assertFalse(metadata["unified_prototype_broad_stress_complete"])
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
        self.assertNotIn(
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
        self.assertIn(
            "text_free_acceptor_feature_gap_audit",
            metadata["failing_gate_ids"],
        )
        self.assertIn(
            "protein_substrate_acceptor_candidate_audit",
            metadata["failing_gate_ids"],
        )
        self.assertIn(
            "source_free_chain_topology_role_audit",
            metadata["failing_gate_ids"],
        )
        self.assertNotIn(
            "heteromeric_chain_topology_signal_audit",
            metadata["failing_gate_ids"],
        )
        self.assertNotIn(
            "unified_substrate_identity_rule_probe",
            metadata["failing_gate_ids"],
        )
        self.assertNotIn(
            "unified_review_only_scoring_prototype",
            metadata["failing_gate_ids"],
        )
        self.assertNotIn(
            "unified_prototype_broad_stress_audit",
            metadata["failing_gate_ids"],
        )
        self.assertIn(
            "m_csa760_atp_state_repair_scan",
            metadata["failing_gate_ids"],
        )
        self.assertIn(
            "m_csa757_active_state_repair_scan",
            metadata["failing_gate_ids"],
        )
        self.assertIn(
            "m_csa756_active_state_repair_scan",
            metadata["failing_gate_ids"],
        )
        self.assertEqual(
            metadata["m_csa760_repair_status"],
            "blocked_review_only_split_atp_and_substrate_context",
        )
        self.assertEqual(metadata["m_csa760_atp_metal_state_candidate_count"], 2)
        self.assertEqual(
            metadata[
                "m_csa760_protein_substrate_acceptor_context_candidate_count"
            ],
            2,
        )
        self.assertEqual(
            metadata[
                "m_csa760_combined_atp_metal_substrate_context_candidate_count"
            ],
            0,
        )
        self.assertEqual(metadata["m_csa760_measurement_ready_candidate_count"], 0)
        self.assertTrue(metadata["m_csa760_split_state_blocker_detected"])
        self.assertEqual(
            metadata["m_csa757_repair_status"],
            "blocked_review_only_active_state_without_mapped_substrate_acceptor",
        )
        self.assertEqual(
            metadata["m_csa757_active_state_atp_metal_candidate_count"],
            2,
        )
        self.assertEqual(
            metadata[
                "m_csa757_conservative_active_state_atp_metal_candidate_count"
            ],
            1,
        )
        self.assertEqual(
            metadata[
                "m_csa757_homomeric_mapping_ambiguous_active_state_candidate_count"
            ],
            1,
        )
        self.assertEqual(
            metadata["m_csa757_mapped_protein_substrate_acceptor_candidate_count"],
            0,
        )
        self.assertEqual(metadata["m_csa757_measurement_ready_candidate_count"], 0)
        self.assertEqual(
            metadata["m_csa756_repair_status"],
            "blocked_review_only_no_active_state_atp_metal_context",
        )
        self.assertEqual(
            metadata["m_csa756_active_state_atp_metal_candidate_count"],
            0,
        )
        self.assertEqual(
            metadata["m_csa756_structure_phosphoacceptor_context_candidate_count"],
            13,
        )
        self.assertEqual(
            metadata["m_csa756_mapped_protein_substrate_acceptor_candidate_count"],
            0,
        )
        self.assertEqual(metadata["m_csa756_measurement_ready_candidate_count"], 0)
        self.assertNotIn(
            "family_specific_homolog_mapping_template",
            metadata["failing_gate_ids"],
        )
        self.assertNotIn(
            "family_specific_homolog_mapping_from_template",
            metadata["failing_gate_ids"],
        )
        checks = {check["gate_id"]: check for check in status["gate_checks"]}
        self.assertTrue(checks["local_axis_prototype"]["passed"])
        self.assertTrue(
            checks["gamma_geometry_measured_for_all_prototype_rows"]["passed"]
        )
        self.assertTrue(checks["m_csa640_alternate_gamma_geometry_reviewed"]["passed"])
        self.assertTrue(checks["substrate_acceptor_counteraxis_prototype"]["passed"])
        self.assertFalse(checks["text_free_acceptor_feature_gap_audit"]["passed"])
        self.assertFalse(
            checks["protein_substrate_acceptor_candidate_audit"]["passed"]
        )
        self.assertTrue(checks["ligand_analog_policy_blocker_decision"]["passed"])
        self.assertFalse(checks["m_csa760_atp_state_repair_scan"]["passed"])
        self.assertFalse(checks["m_csa757_active_state_repair_scan"]["passed"])
        self.assertFalse(checks["m_csa756_active_state_repair_scan"]["passed"])
        self.assertTrue(
            checks["ligand_specific_5hvk_source_validity_review"]["passed"]
        )
        self.assertTrue(
            checks["ligand_specific_5hvk_control_rerun_queue"]["passed"]
        )
        self.assertTrue(
            checks["ligand_specific_5hvk_prototype_control_rerun"]["passed"]
        )
        self.assertEqual(
            checks["ligand_specific_5hvk_prototype_control_rerun"]["evidence"][
                "positive_like_review_row_count"
            ],
            4,
        )
        self.assertEqual(
            checks["ligand_specific_5hvk_prototype_control_rerun"]["evidence"][
                "imported_external_hard_negative_non_abstention_count"
            ],
            0,
        )
        self.assertTrue(
            checks[
                "ligand_specific_5hvk_protein_substrate_axis_generalization"
            ]["passed"]
        )
        self.assertFalse(checks["source_free_chain_topology_role_audit"]["passed"])
        self.assertEqual(
            checks["source_free_chain_topology_role_audit"]["evidence"][
                "known_same_accession_control_risk_count"
            ],
            3,
        )
        self.assertTrue(
            checks["heteromeric_chain_topology_signal_audit"]["passed"]
        )
        self.assertEqual(
            checks["heteromeric_chain_topology_signal_audit"]["evidence"][
                "heteromeric_signal_positive_like_count"
            ],
            1,
        )
        self.assertEqual(
            checks["heteromeric_chain_topology_signal_audit"]["evidence"][
                "same_accession_control_signal_false_hit_count"
            ],
            0,
        )
        self.assertFalse(
            checks["heteromeric_chain_topology_signal_audit"]["evidence"][
                "minimum_positive_coverage_met"
            ]
        )
        self.assertEqual(
            checks["heteromeric_chain_topology_signal_audit"]["evidence"][
                "full_probe_heteromeric_candidate_structure_count"
            ],
            1,
        )
        self.assertTrue(
            checks["heteromeric_positive_coverage_candidate_scout"]["passed"]
        )
        self.assertEqual(
            checks["heteromeric_positive_coverage_candidate_scout"]["evidence"][
                "heteromeric_candidate_structure_count"
            ],
            6,
        )
        self.assertFalse(
            checks["heteromeric_positive_coverage_candidate_scout"]["evidence"][
                "minimum_positive_coverage_met"
            ]
        )
        self.assertTrue(
            checks["heteromeric_candidate_source_validation_review"]["passed"]
        )
        self.assertEqual(
            checks["heteromeric_candidate_source_validation_review"]["evidence"][
                "source_validated_new_candidate_count"
            ],
            3,
        )
        self.assertEqual(
            checks["heteromeric_candidate_source_validation_review"]["evidence"][
                "source_validated_new_candidate_pdb_ids"
            ],
            ["6Z3R", "8OXM", "8OXO"],
        )
        self.assertTrue(
            checks["heteromeric_candidate_source_validation_review"]["evidence"][
                "minimum_positive_coverage_met_review_only"
            ]
        )
        self.assertTrue(
            checks[
                "heteromeric_source_valid_candidate_gamma_distance_sample"
            ]["passed"]
        )
        self.assertEqual(
            checks[
                "heteromeric_source_valid_candidate_gamma_distance_sample"
            ]["evidence"]["measured_candidate_count"],
            3,
        )
        self.assertTrue(
            checks[
                "heteromeric_source_valid_candidate_gamma_distance_sample"
            ]["evidence"]["minimum_positive_coverage_measured_review_only"]
        )
        self.assertFalse(
            checks[
                "ligand_specific_5hvk_protein_substrate_axis_generalization"
            ]["evidence"]["ligand_analog_required_for_minimum_review_set"]
        )
        self.assertEqual(
            checks["ligand_specific_5hvk_source_validity_review"]["evidence"][
                "nearest_source_phosphoacceptor_distance_angstrom"
            ],
            4.236,
        )
        self.assertFalse(
            checks["ligand_specific_5hvk_source_validity_review"]["evidence"][
                "ready_to_run_epk_scorer"
            ]
        )
        self.assertEqual(
            checks["text_free_acceptor_feature_gap_audit"]["evidence"][
                "negative_control_false_hit_count"
            ],
            11,
        )
        self.assertEqual(
            checks["text_free_acceptor_feature_gap_audit"]["evidence"][
                "negative_control_false_hit_family_ids"
            ],
            ["atp_grasp", "ndk", "pfka", "pfkb"],
        )
        self.assertTrue(checks["measured_acceptor_identity_reviewed"]["passed"])
        self.assertTrue(checks["nonready_rows_repaired_or_excluded"]["passed"])
        self.assertTrue(checks["gamma_threshold_control_plan"]["passed"])
        self.assertFalse(
            checks["gamma_negative_control_distance_distribution"]["passed"]
        )
        self.assertTrue(checks["family_specific_homolog_mapping_template"]["passed"])
        self.assertEqual(
            checks["family_specific_homolog_mapping_template"]["evidence"][
                "validated_template_family_ids"
            ],
            ["atp_grasp", "pfka", "pfkb"],
        )
        self.assertTrue(
            checks["family_specific_homolog_mapping_from_template"]["passed"]
        )
        self.assertEqual(
            checks["family_specific_homolog_mapping_from_template"]["evidence"][
                "ready_family_ids"
            ],
            ["atp_grasp", "pfka", "pfkb"],
        )
        self.assertEqual(
            checks["family_specific_homolog_mapping_from_template"]["evidence"][
                "distance_measured_homolog_structure_count_total"
            ],
            16,
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
        self.assertTrue(
            checks["heteromeric_source_expansion_peptide_role_axis_audit"][
                "passed"
            ]
        )
        self.assertEqual(
            checks["heteromeric_source_expansion_peptide_role_axis_audit"][
                "evidence"
            ]["source_valid_expansion_peptide_role_hit_pdb_ids"],
            ["1O6K", "1O6L"],
        )
        self.assertEqual(
            checks["heteromeric_source_expansion_peptide_role_axis_audit"][
                "evidence"
            ]["nonpositive_source_expansion_control_false_hit_count"],
            0,
        )
        self.assertTrue(checks["substrate_mode_gap_audit"]["passed"])
        self.assertEqual(
            checks["substrate_mode_gap_audit"]["evidence"][
                "combined_peptide_mode_positive_pdb_ids"
            ],
            ["1O6K", "1O6L", "6Z3R", "8OXM", "8OXO"],
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

    def test_epk_ndk_homolog_gamma_distance_sample_stays_review_only(self) -> None:
        sample = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_sibling_control_homolog_gamma_distance_sample_ndk_1025.json"
        )
        metadata = sample["metadata"]
        self.assertEqual(
            metadata["method"], "epk_sibling_control_homolog_gamma_distance_sample"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_sibling_family_id"], "ndk")
        self.assertEqual(
            metadata["source_epk_sibling_control_homolog_mapping_review_method"],
            "epk_sibling_control_homolog_mapping_review",
        )
        self.assertEqual(metadata["ready_input_homolog_structure_count"], 4)
        self.assertEqual(metadata["measured_homolog_structure_count"], 4)
        self.assertEqual(
            metadata["measurement_status_counts"],
            {"homolog_gamma_to_mapped_histidine_distance_measured_review_only": 4},
        )
        self.assertEqual(
            metadata["homolog_control_axis"],
            "mapped_phosphohistidine_site_not_hydroxyl_acceptor",
        )
        self.assertGreaterEqual(
            metadata["observed_homolog_histidine_distance_min_angstrom"], 2.8
        )
        self.assertLessEqual(
            metadata["observed_homolog_histidine_distance_max_angstrom"], 3.4
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
        statuses = {row["pdb_id"]: row["measurement_status"] for row in sample["rows"]}
        self.assertEqual(
            set(statuses.values()),
            {"homolog_gamma_to_mapped_histidine_distance_measured_review_only"},
        )
        self.assertEqual(set(statuses), {"1WKL", "3Q86", "9OAN", "9PFY"})
        for row in sample["rows"]:
            self.assertTrue(row["gamma_to_mapped_histidine_distance_measured"])
            self.assertFalse(row["negative_control_distance_distribution_ready"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertIn(
                "homolog_control_not_hydroxyl_acceptor_axis",
                row["measurement_blockers"],
            )

    def test_epk_ndk_homolog_terminal_review_stays_review_only(self) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_sibling_control_homolog_terminal_review_ndk_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"], "epk_sibling_control_homolog_terminal_review"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["reviewed_sibling_family_id"], "ndk")
        self.assertEqual(
            metadata["terminal_review_status"],
            "terminal_review_only_all_homologs_measured_histidine_axis_blocks_threshold",
        )
        self.assertEqual(
            metadata["reviewed_homolog_pdb_ids"], ["1WKL", "3Q86", "9OAN", "9PFY"]
        )
        self.assertEqual(metadata["measurement_ready_homolog_structure_count"], 4)
        self.assertEqual(metadata["measured_homolog_structure_count"], 4)
        self.assertEqual(metadata["unresolved_homolog_structure_count"], 0)
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        statuses = {row["pdb_id"]: row["terminal_review_status"] for row in review["rows"]}
        self.assertEqual(
            set(statuses.values()),
            {"terminal_measured_histidine_counteraxis_review_only"},
        )
        for row in review["rows"]:
            self.assertTrue(row["measurement_ready_for_negative_control"])
            self.assertTrue(row["gamma_to_mapped_histidine_distance_measured"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_remaining_homolog_source_plans_stay_review_only(self) -> None:
        expectations = {
            "pfkb": {
                "path": "v3_epk_sibling_control_homolog_source_plan_pfkb_1025.json",
                "source_entry_ids": ["m_csa:663", "m_csa:670"],
                "candidate_pdb_count": 10,
                "gamma_capable_candidate_count": 9,
                "metal_supported_gamma_candidate_count": 9,
                "status_counts": {
                    "candidate_gamma_metal_source_review_only": 9,
                    "candidate_not_gamma_capable_source": 1,
                },
            },
            "pfka": {
                "path": "v3_epk_sibling_control_homolog_source_plan_pfka_1025.json",
                "source_entry_ids": ["m_csa:365"],
                "candidate_pdb_count": 10,
                "gamma_capable_candidate_count": 5,
                "metal_supported_gamma_candidate_count": 5,
                "status_counts": {
                    "candidate_gamma_metal_source_review_only": 5,
                    "candidate_not_gamma_capable_source": 2,
                    "candidate_product_or_partial_source_not_gamma_capable": 3,
                },
            },
            "atp_grasp": {
                "path": (
                    "v3_epk_sibling_control_homolog_source_plan_atp_grasp_1025.json"
                ),
                "source_entry_ids": ["m_csa:310", "m_csa:498"],
                "candidate_pdb_count": 12,
                "gamma_capable_candidate_count": 2,
                "metal_supported_gamma_candidate_count": 2,
                "status_counts": {
                    "candidate_gamma_metal_source_review_only": 2,
                    "candidate_product_or_partial_source_not_gamma_capable": 10,
                },
            },
        }
        for family_id, expected in expectations.items():
            with self.subTest(family_id=family_id):
                plan = _load_json(ROOT / "artifacts" / expected["path"])
                metadata = plan["metadata"]
                self.assertEqual(
                    metadata["method"], "epk_sibling_control_homolog_source_plan"
                )
                self.assertTrue(metadata["review_only"])
                self.assertEqual(metadata["reviewed_sibling_family_id"], family_id)
                self.assertEqual(
                    metadata["source_entry_ids"], expected["source_entry_ids"]
                )
                self.assertEqual(
                    metadata["candidate_pdb_count"],
                    expected["candidate_pdb_count"],
                )
                self.assertEqual(
                    metadata["gamma_capable_candidate_count"],
                    expected["gamma_capable_candidate_count"],
                )
                self.assertEqual(
                    metadata["metal_supported_gamma_candidate_count"],
                    expected["metal_supported_gamma_candidate_count"],
                )
                self.assertEqual(metadata["measurement_ready_homolog_structure_count"], 0)
                self.assertEqual(metadata["catalytic_mapping_verified_count"], 0)
                self.assertFalse(
                    metadata["negative_control_distance_distribution_ready"]
                )
                self.assertFalse(metadata["threshold_calibrated"])
                self.assertFalse(metadata["epk_score_computed"])
                self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
                self.assertFalse(metadata["ready_to_run_epk_scorer"])
                self.assertFalse(
                    metadata["ready_to_expand_positive_fingerprint_universe"]
                )
                self.assertFalse(metadata["fingerprint_registry_edited"])
                self.assertFalse(metadata["curated_label_registry_edited"])
                self.assertEqual(metadata["countable_label_candidate_count"], 0)
                self.assertEqual(
                    metadata["source_candidate_status_counts"],
                    expected["status_counts"],
                )
                for row in plan["rows"]:
                    self.assertFalse(row["measurement_ready_for_negative_control"])
                    self.assertFalse(row["countable_label_candidate"])
                    self.assertEqual(
                        row["catalytic_mapping_status"],
                        "not_mapped_review_pending",
                    )

    def test_epk_remaining_homolog_mapping_reviews_fail_closed(self) -> None:
        expectations = {
            "pfkb": {
                "path": "v3_epk_sibling_control_homolog_mapping_review_pfkb_1025.json",
                "candidate_pdb_count": 10,
                "nucleotide_site_mapped_candidate_count": 4,
            },
            "pfka": {
                "path": "v3_epk_sibling_control_homolog_mapping_review_pfka_1025.json",
                "candidate_pdb_count": 10,
                "nucleotide_site_mapped_candidate_count": 5,
            },
            "atp_grasp": {
                "path": (
                    "v3_epk_sibling_control_homolog_mapping_review_atp_grasp_1025.json"
                ),
                "candidate_pdb_count": 12,
                "nucleotide_site_mapped_candidate_count": 0,
            },
        }
        for family_id, expected in expectations.items():
            with self.subTest(family_id=family_id):
                review = _load_json(ROOT / "artifacts" / expected["path"])
                metadata = review["metadata"]
                self.assertEqual(
                    metadata["method"], "epk_sibling_control_homolog_mapping_review"
                )
                self.assertTrue(metadata["review_only"])
                self.assertEqual(metadata["reviewed_sibling_family_id"], family_id)
                self.assertEqual(
                    metadata["mapping_reviewed_candidate_count"],
                    expected["candidate_pdb_count"],
                )
                self.assertEqual(
                    metadata["homolog_mapping_status_counts"],
                    {
                        "homolog_catalytic_histidine_mapping_unresolved": (
                            expected["candidate_pdb_count"]
                        )
                    },
                )
                self.assertEqual(metadata["catalytic_histidine_mapped_candidate_count"], 0)
                self.assertEqual(
                    metadata["nucleotide_site_mapped_candidate_count"],
                    expected["nucleotide_site_mapped_candidate_count"],
                )
                self.assertEqual(metadata["measurement_ready_homolog_structure_count"], 0)
                self.assertIn(family_id, metadata["next_actions"][0])
                self.assertNotIn("NDK", metadata["next_actions"][0])
                self.assertFalse(metadata["calibration_distance_measured"])
                self.assertFalse(
                    metadata["negative_control_distance_distribution_ready"]
                )
                self.assertFalse(metadata["threshold_calibrated"])
                self.assertFalse(metadata["epk_score_computed"])
                self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
                self.assertFalse(metadata["ready_to_run_epk_scorer"])
                self.assertFalse(
                    metadata["ready_to_expand_positive_fingerprint_universe"]
                )
                self.assertFalse(metadata["fingerprint_registry_edited"])
                self.assertFalse(metadata["curated_label_registry_edited"])
                self.assertEqual(metadata["countable_label_candidate_count"], 0)
                for row in review["rows"]:
                    self.assertEqual(
                        row["homolog_mapping_status"],
                        "homolog_catalytic_histidine_mapping_unresolved",
                    )
                    self.assertFalse(row["measurement_ready_for_negative_control"])
                    self.assertFalse(row["negative_control_distance_distribution_ready"])
                    self.assertFalse(row["countable_label_candidate"])

    def test_epk_family_specific_mapping_template_reviews_stay_review_only(
        self,
    ) -> None:
        expectations = {
            "pfkb": {
                "path": "v3_epk_family_specific_mapping_template_review_pfkb_1025.json",
                "source_entry_ids": ["m_csa:663", "m_csa:670"],
                "seeded_template_entry_count": 2,
                "template_residue_count": 11,
                "mapping_candidate_count": 10,
                "nucleotide_site_mapped_candidate_count": 4,
            },
            "pfka": {
                "path": "v3_epk_family_specific_mapping_template_review_pfka_1025.json",
                "source_entry_ids": ["m_csa:365"],
                "seeded_template_entry_count": 1,
                "template_residue_count": 7,
                "mapping_candidate_count": 10,
                "nucleotide_site_mapped_candidate_count": 5,
            },
            "atp_grasp": {
                "path": (
                    "v3_epk_family_specific_mapping_template_review_atp_grasp_1025.json"
                ),
                "source_entry_ids": ["m_csa:310", "m_csa:498"],
                "seeded_template_entry_count": 2,
                "template_residue_count": 17,
                "mapping_candidate_count": 12,
                "nucleotide_site_mapped_candidate_count": 0,
            },
        }
        for family_id, expected in expectations.items():
            with self.subTest(family_id=family_id):
                review = _load_json(ROOT / "artifacts" / expected["path"])
                metadata = review["metadata"]
                self.assertEqual(
                    metadata["method"], "epk_family_specific_mapping_template_review"
                )
                self.assertTrue(metadata["review_only"])
                self.assertEqual(metadata["reviewed_sibling_family_id"], family_id)
                self.assertEqual(
                    metadata["source_epk_sibling_control_homolog_mapping_review_method"],
                    "epk_sibling_control_homolog_mapping_review",
                )
                self.assertEqual(
                    metadata["source_entry_ids"], expected["source_entry_ids"]
                )
                self.assertEqual(
                    metadata["seeded_template_entry_count"],
                    expected["seeded_template_entry_count"],
                )
                self.assertEqual(
                    metadata["template_residue_count"],
                    expected["template_residue_count"],
                )
                self.assertEqual(
                    metadata["source_mapping_review_status_counts"],
                    {
                        "homolog_catalytic_histidine_mapping_unresolved": (
                            expected["mapping_candidate_count"]
                        )
                    },
                )
                self.assertEqual(
                    metadata["source_mapping_review_histidine_mapped_count"], 0
                )
                self.assertEqual(
                    metadata["source_mapping_review_nucleotide_site_mapped_count"],
                    expected["nucleotide_site_mapped_candidate_count"],
                )
                self.assertEqual(
                    metadata["source_mapping_review_measurement_ready_count"],
                    0,
                )
                self.assertFalse(metadata["family_specific_mapping_ready"])
                self.assertFalse(metadata["negative_control_distance_distribution_ready"])
                self.assertFalse(metadata["threshold_calibrated"])
                self.assertFalse(metadata["epk_score_computed"])
                self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
                self.assertFalse(metadata["ready_to_run_epk_scorer"])
                self.assertFalse(
                    metadata["ready_to_expand_positive_fingerprint_universe"]
                )
                self.assertFalse(metadata["fingerprint_registry_edited"])
                self.assertFalse(metadata["curated_label_registry_edited"])
                self.assertEqual(metadata["countable_label_candidate_count"], 0)
                rows = {row["entry_id"]: row for row in review["rows"]}
                self.assertEqual(set(rows), set(expected["source_entry_ids"]))
                self.assertIn(
                    "acid_base_or_acceptor_seed",
                    {
                        residue["template_role"]
                        for row in review["rows"]
                        for residue in row["template_residues"]
                    },
                )
                for row in review["rows"]:
                    self.assertFalse(row["template_ready_for_automated_mapping"])
                    self.assertFalse(row["template_can_be_used_for_distance_measurement"])
                    self.assertFalse(row["exact_residue_position_transfer_allowed"])
                    self.assertFalse(row["countable_label_candidate"])

    def test_epk_family_specific_homolog_mapping_and_distance_stay_review_only(
        self,
    ) -> None:
        expectations = {
            "pfkb": {"candidate_count": 10, "ready_count": 9, "blocked_count": 1},
            "pfka": {"candidate_count": 10, "ready_count": 5, "blocked_count": 5},
            "atp_grasp": {"candidate_count": 12, "ready_count": 2, "blocked_count": 10},
        }
        for family_id, expected in expectations.items():
            with self.subTest(family_id=family_id):
                mapping = _load_json(
                    ROOT
                    / "artifacts"
                    / f"v3_epk_family_specific_homolog_mapping_review_{family_id}_1025.json"
                )
                metadata = mapping["metadata"]
                self.assertEqual(
                    metadata["method"], "epk_family_specific_homolog_mapping_review"
                )
                self.assertTrue(metadata["review_only"])
                self.assertEqual(metadata["reviewed_sibling_family_id"], family_id)
                self.assertEqual(
                    metadata["mapping_reviewed_candidate_count"],
                    expected["candidate_count"],
                )
                self.assertEqual(
                    metadata["family_specific_homolog_mapping_status_counts"],
                    {
                        "family_specific_acid_base_mapping_unresolved": (
                            expected["blocked_count"]
                        ),
                        "family_specific_homolog_mapping_ready_for_distance_measurement_review_only": (
                            expected["ready_count"]
                        ),
                    },
                )
                self.assertEqual(
                    metadata["measurement_ready_homolog_structure_count"],
                    expected["ready_count"],
                )
                self.assertFalse(metadata["calibration_distance_measured"])
                self.assertFalse(metadata["negative_control_distance_distribution_ready"])
                self.assertFalse(metadata["threshold_calibrated"])
                self.assertFalse(metadata["epk_score_computed"])
                self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
                self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
                self.assertFalse(metadata["fingerprint_registry_edited"])
                self.assertFalse(metadata["curated_label_registry_edited"])
                ready_rows = [
                    row
                    for row in mapping["rows"]
                    if row["measurement_ready_for_negative_control"]
                ]
                self.assertEqual(len(ready_rows), expected["ready_count"])
                for row in mapping["rows"]:
                    self.assertTrue(row["review_only"])
                    self.assertFalse(row["countable_label_candidate"])
                    for chain_mapping in row["chain_mappings"]:
                        self.assertFalse(
                            chain_mapping["exact_residue_position_transfer_used"]
                        )

                sample = _load_json(
                    ROOT
                    / "artifacts"
                    / f"v3_epk_family_specific_homolog_gamma_distance_sample_{family_id}_1025.json"
                )
                sample_meta = sample["metadata"]
                self.assertEqual(
                    sample_meta["method"],
                    "epk_family_specific_homolog_gamma_distance_sample",
                )
                self.assertTrue(sample_meta["review_only"])
                self.assertEqual(sample_meta["reviewed_sibling_family_id"], family_id)
                self.assertEqual(
                    sample_meta["measured_homolog_structure_count"],
                    expected["ready_count"],
                )
                self.assertEqual(
                    sample_meta[
                        "lowest_covering_candidate_family_acid_base_hit_count"
                    ],
                    expected["ready_count"],
                )
                self.assertEqual(
                    sample_meta["homolog_control_axis"],
                    "family_specific_sibling_acid_base_counteraxis_not_epk_label",
                )
                self.assertFalse(
                    sample_meta["negative_control_distance_distribution_ready"]
                )
                self.assertFalse(sample_meta["threshold_calibrated"])
                self.assertFalse(sample_meta["epk_score_computed"])
                self.assertFalse(
                    sample_meta["ready_to_expand_positive_fingerprint_universe"]
                )
                self.assertFalse(sample_meta["fingerprint_registry_edited"])
                self.assertFalse(sample_meta["curated_label_registry_edited"])
                for row in sample["rows"]:
                    self.assertTrue(row["review_only"])
                    self.assertFalse(row["countable_label_candidate"])

    def test_epk_review_only_scoring_prototype_fails_closed(self) -> None:
        prototype = _load_json(
            ROOT / "artifacts" / "v3_epk_review_only_scoring_prototype_1025.json"
        )
        metadata = prototype["metadata"]
        self.assertEqual(metadata["method"], "epk_review_only_scoring_prototype")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["prototype_gate_status"], "fail_closed_review_only")
        self.assertTrue(metadata["prototype_failed_closed"])
        self.assertEqual(metadata["current_positive_prototype_row_count"], 3)
        self.assertEqual(metadata["current_positive_full_axis_count"], 3)
        self.assertEqual(metadata["m_csa640_alternate_gamma_geometry_support_count"], 1)
        self.assertEqual(metadata["sibling_homolog_counteraxis_row_count"], 4)
        self.assertEqual(metadata["sibling_family_specific_counteraxis_row_count"], 16)
        self.assertEqual(metadata["imported_external_hard_negative_row_count"], 3)
        self.assertEqual(metadata["imported_external_hard_negative_nonhit_count"], 3)
        self.assertEqual(
            metadata["prototype_decision_counts"],
            {
                "blocked_by_family_specific_sibling_counteraxis_review_only": 16,
                "blocked_by_phosphohistidine_counteraxis_review_only": 4,
                "candidate_positive_signal_review_only_not_calibrated": 3,
                "external_hard_negative_abstain_missing_epk_axes_review_only": 3,
            },
        )
        m_csa640 = [
            row for row in prototype["rows"] if row.get("entry_id") == "m_csa:640"
        ][0]
        self.assertEqual(m_csa640["pdb_id"], "3TM0")
        self.assertEqual(
            m_csa640["gamma_geometry_scope"],
            "alternate_graph_linked_structure",
        )
        self.assertEqual(
            m_csa640["alternate_gamma_geometry_review_status"],
            "alternate_gamma_to_acceptor_analog_distance_reviewed_review_only",
        )
        self.assertEqual(m_csa640["review_only_prototype_score"], 1.0)
        self.assertFalse(metadata["negative_control_distance_distribution_ready"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        external_rows = [
            row
            for row in prototype["rows"]
            if row["row_type"] == "imported_external_hard_negative"
        ]
        self.assertEqual(
            sorted(row["entry_id"] for row in external_rows),
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        for row in external_rows:
            self.assertEqual(row["review_only_prototype_score"], 0.0)
            self.assertEqual(
                row["prototype_decision"],
                "external_hard_negative_abstain_missing_epk_axes_review_only",
            )

    def test_epk_unified_review_only_scoring_prototype_fails_closed(self) -> None:
        prototype = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_review_only_scoring_prototype_1025.json"
        )
        metadata = prototype["metadata"]
        self.assertEqual(
            metadata["method"], "epk_unified_review_only_scoring_prototype"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["prototype_gate_status"], "fail_closed_review_only")
        self.assertTrue(metadata["prototype_failed_closed"])
        self.assertTrue(metadata["prototype_passes_current_controls"])
        self.assertEqual(metadata["positive_like_full_score_count"], 8)
        self.assertEqual(
            metadata["positive_like_full_score_pdb_ids"],
            ["1IR3", "1O6K", "1O6L", "2PHK", "5HVK", "6Z3R", "8OXM", "8OXO"],
        )
        self.assertEqual(metadata["positive_like_miss_count"], 1)
        self.assertEqual(metadata["positive_like_miss_pdb_ids"], ["3TM0"])
        self.assertEqual(metadata["current_control_false_non_abstention_count"], 0)
        self.assertEqual(
            metadata["imported_external_hard_negative_non_abstention_count"],
            0,
        )
        self.assertEqual(metadata["legacy_sibling_counteraxis_row_count"], 20)
        self.assertTrue(metadata["review_only_score_computed"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = prototype["rows"]
        five_hvk = [row for row in rows if row.get("pdb_id") == "5HVK"][0]
        self.assertEqual(
            five_hvk["review_only_prototype_decision"],
            "unified_positive_signal_review_only_not_calibrated",
        )
        self.assertEqual(
            five_hvk["nearest_gamma_to_acceptor_distance_angstrom"], 4.236
        )
        external_rows = [
            row
            for row in rows
            if row.get("row_type")
            == "unified_identity_imported_external_hard_negative"
        ]
        self.assertEqual(
            sorted(row["entry_id"] for row in external_rows),
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        for row in external_rows:
            self.assertEqual(row["review_only_unified_prototype_score"], 0.0)
            self.assertEqual(
                row["review_only_prototype_decision"],
                "external_hard_negative_abstain_unified_review_only",
            )

    def test_epk_unified_prototype_broad_stress_audit_fails_closed(self) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_prototype_broad_stress_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"], "epk_unified_prototype_broad_stress_audit"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["broad_stress_status"],
            "bounded_stress_has_source_validation_counterexamples_review_only",
        )
        self.assertEqual(metadata["exact_source_query_reviewed_count"], 110)
        self.assertEqual(metadata["exact_source_query_unreviewed_count"], 0)
        self.assertEqual(metadata["outside_query_reviewed_candidate_count"], 299)
        self.assertEqual(metadata["outside_query_fetch_failure_count"], 0)
        self.assertEqual(metadata["outside_query_heteromeric_candidate_hit_count"], 13)
        self.assertEqual(
            metadata["outside_query_heteromeric_candidate_pdb_ids"],
            [
                "1O6K",
                "1O6L",
                "2JJ2",
                "4HPU",
                "7B56",
                "7T55",
                "7T56",
                "7T57",
                "7ZDT",
                "7ZDU",
                "7ZE5",
                "9L3M",
                "9L3U",
            ],
        )
        self.assertEqual(
            metadata["source_validated_positive_like_pdb_ids"], ["1O6K", "1O6L"]
        )
        self.assertEqual(
            metadata["source_validation_blocked_or_rejected_pdb_ids"],
            [
                "2JJ2",
                "4HPU",
                "7B56",
                "7T55",
                "7T56",
                "7T57",
                "7ZDT",
                "7ZDU",
                "7ZE5",
                "9L3M",
                "9L3U",
            ],
        )
        self.assertTrue(metadata["bounded_stress_identifies_counterexamples"])
        self.assertFalse(metadata["broad_stress_complete"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_general_substrate_identity_gap_audit_fails_closed(self) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_general_substrate_identity_gap_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"], "epk_general_substrate_identity_gap_audit"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["relaxed_polymer_identity_status"],
            "fails_closed_relaxed_polymer_rule_has_nonpositive_false_hit",
        )
        self.assertEqual(
            metadata["source_valid_relaxed_polymer_hit_pdb_ids"],
            ["1O6K", "1O6L"],
        )
        self.assertEqual(
            metadata["nonpositive_relaxed_polymer_false_hit_pdb_ids"],
            ["7B56"],
        )
        self.assertEqual(metadata["general_substrate_identity_ready_count"], 0)
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_length_band_substrate_identity_counteraxis_is_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_length_band_substrate_identity_counteraxis_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_length_band_substrate_identity_counteraxis_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["length_band_identity_status"],
            "passes_source_expansion_subset_by_blocking_relaxed_false_hits_review_only",
        )
        self.assertEqual(
            metadata["positive_like_length_band_hit_pdb_ids"],
            ["1O6K", "1O6L"],
        )
        self.assertEqual(metadata["nonpositive_length_band_false_hit_count"], 0)
        self.assertEqual(
            metadata[
                "nonpositive_relaxed_false_hit_blocked_by_length_band_pdb_ids"
            ],
            ["7B56"],
        )
        self.assertEqual(metadata["general_substrate_identity_ready_count"], 0)
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_length_band_external_hard_negative_review_is_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_length_band_external_hard_negative_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"], "epk_length_band_external_hard_negative_review"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["length_band_external_hard_negative_review_status"],
            "passes_review_only_length_band_external_hard_negative_abstention",
        )
        self.assertEqual(
            metadata["expected_external_hard_negative_entry_ids"],
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        self.assertEqual(metadata["external_hard_negative_review_row_count"], 3)
        self.assertEqual(
            metadata["length_band_external_hard_negative_non_abstention_count"],
            0,
        )
        self.assertTrue(metadata["not_a_real_scored_reaudit"])
        self.assertFalse(metadata["clean_heldout_performance_claim_permitted"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        for row in review["rows"]:
            self.assertFalse(row["length_band_feature_non_abstention"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_source_free_protein_substrate_role_discriminator_is_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_source_free_protein_substrate_role_discriminator_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_source_free_protein_substrate_role_discriminator_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["protein_substrate_role_discriminator_status"],
            "passes_current_controls_but_review_only_not_production_admissible",
        )
        self.assertTrue(
            metadata["protein_substrate_role_discriminator_passes_current_controls"]
        )
        self.assertEqual(metadata["current_protein_positive_hit_pdb_ids"], ["1IR3", "2PHK"])
        self.assertEqual(metadata["heteromeric_protein_positive_hit_pdb_ids"], ["5HVK"])
        self.assertEqual(
            metadata["combined_protein_substrate_role_hit_pdb_ids"],
            ["1IR3", "2PHK", "5HVK"],
        )
        self.assertEqual(metadata["protein_substrate_role_miss_count"], 0)
        self.assertEqual(
            metadata["ligand_analog_excluded_positive_entry_ids"],
            ["m_csa:640"],
        )
        self.assertEqual(metadata["protein_role_control_false_hit_count"], 0)
        self.assertEqual(
            metadata[
                "protein_role_external_hard_negative_non_abstention_count"
            ],
            0,
        )
        self.assertTrue(metadata["length_band_not_general_protein_discriminator"])
        self.assertEqual(metadata["general_substrate_identity_ready_count"], 0)
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        for row in audit["rows"]:
            self.assertFalse(row["production_scoring_admissible"])
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["epk_score_computed"])

    def test_epk_source_free_protein_substrate_role_discriminator_stress_fails_closed(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_source_free_protein_substrate_role_discriminator_stress_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_source_free_protein_substrate_role_discriminator_stress_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["source_epk_source_free_protein_substrate_role_discriminator_audit_method"],
            "epk_source_free_protein_substrate_role_discriminator_audit",
        )
        self.assertEqual(
            metadata["protein_role_source_expansion_stress_status"],
            "fails_closed_review_only_source_expansion_protein_role_false_hit",
        )
        self.assertEqual(
            metadata["source_valid_expansion_protein_role_hit_count"],
            0,
        )
        self.assertEqual(
            metadata["source_valid_expansion_peptide_mode_not_protein_pdb_ids"],
            ["1O6K", "1O6L"],
        )
        self.assertEqual(
            metadata[
                "nonpositive_source_expansion_protein_role_false_hit_pdb_ids"
            ],
            ["7B56"],
        )
        self.assertFalse(metadata["protein_discriminator_generalization_ready"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["ready_for_production_scoring"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        for row in audit["rows"]:
            self.assertFalse(row["production_scoring_admissible"])
            self.assertFalse(row["ready_for_label_import"])
            self.assertFalse(row["countable_label_candidate"])
            self.assertFalse(row["epk_score_computed"])

    def test_epk_unified_prototype_next_broad_stress_preregistration_closed(
        self,
    ) -> None:
        preregistration = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_unified_prototype_next_broad_stress_preregistration_1025.json"
        )
        metadata = preregistration["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_unified_prototype_next_broad_stress_preregistration",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["preregistration_status"],
            "active_review_only_next_broad_stress_tranche_preregistered",
        )
        self.assertEqual(
            metadata["known_counterexample_pdb_ids"],
            [
                "2JJ2",
                "4HPU",
                "7B56",
                "7T55",
                "7T56",
                "7T57",
                "7ZDT",
                "7ZDU",
                "7ZE5",
                "9L3M",
                "9L3U",
            ],
        )
        self.assertEqual(
            metadata["source_validated_positive_like_pdb_ids"], ["1O6K", "1O6L"]
        )
        self.assertEqual(metadata["lane_count"], 3)
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            [row["lane_id"] for row in preregistration["rows"]],
            [
                "amp_pnp_mg_reviewed_peptide_kinase_substrate",
                "protein_substrate_cross_accession_anp_mg",
                "broad_text_query_counterexample_guard",
            ],
        )

    def test_epk_unified_review_artifacts_have_no_countable_rows(self) -> None:
        for artifact_name in [
            "v3_epk_unified_review_only_scoring_prototype_1025.json",
            "v3_epk_unified_prototype_broad_stress_audit_1025.json",
            "v3_epk_general_substrate_identity_gap_audit_1025.json",
            "v3_epk_length_band_substrate_identity_counteraxis_audit_1025.json",
            "v3_epk_length_band_external_hard_negative_review_1025.json",
            "v3_epk_source_free_protein_substrate_role_discriminator_audit_1025.json",
            "v3_epk_source_free_protein_substrate_role_discriminator_stress_audit_1025.json",
            "v3_epk_midlength_protein_role_counteraxis_audit_1025.json",
            "v3_epk_unified_prototype_next_broad_stress_preregistration_1025.json",
        ]:
            artifact = _load_json(ROOT / "artifacts" / artifact_name)
            for row in artifact["rows"]:
                self.assertFalse(row.get("countable_label_candidate"))
                self.assertFalse(row.get("epk_score_computed"))

    def test_epk_counteraxis_sufficiency_decision_blocks_threshold(self) -> None:
        decision = _load_json(
            ROOT / "artifacts" / "v3_epk_counteraxis_sufficiency_decision_1025.json"
        )
        metadata = decision["metadata"]
        self.assertEqual(metadata["method"], "epk_counteraxis_sufficiency_decision")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["threshold_selection_decision"], "do_not_select_threshold")
        self.assertEqual(metadata["family_specific_counteraxis_row_count"], 16)
        self.assertEqual(metadata["family_specific_counteraxis_threshold_hit_count"], 16)
        self.assertEqual(metadata["phosphohistidine_counteraxis_row_count"], 4)
        self.assertEqual(metadata["external_hard_negative_row_count"], 3)
        self.assertEqual(metadata["external_hard_negative_nonhit_count"], 3)
        self.assertTrue(
            metadata[
                "chain_ligand_acceptor_feature_passes_current_review_controls"
            ]
        )
        self.assertFalse(
            metadata[
                "chain_ligand_acceptor_feature_admissible_for_production_scoring"
            ]
        )
        self.assertEqual(
            metadata["chain_ligand_acceptor_negative_control_false_hit_count"],
            0,
        )
        self.assertEqual(
            metadata["chain_ligand_external_feature_non_abstention_count"],
            0,
        )
        self.assertTrue(
            metadata[
                "heteromeric_peptide_acceptor_identity_passes_current_review_controls"
            ]
        )
        self.assertTrue(
            metadata["heteromeric_peptide_external_feature_probe_passed"]
        )
        self.assertEqual(
            metadata["heteromeric_peptide_external_feature_non_abstention_count"],
            0,
        )
        self.assertTrue(
            metadata[
                "heteromeric_source_expansion_peptide_role_axis_passes_source_expansion_controls"
            ]
        )
        self.assertEqual(
            metadata["heteromeric_source_expansion_peptide_role_hit_pdb_ids"],
            ["1O6K", "1O6L"],
        )
        self.assertEqual(
            metadata[
                "heteromeric_source_expansion_peptide_role_nonpositive_false_hit_count"
            ],
            0,
        )
        self.assertEqual(
            metadata[
                "heteromeric_source_expansion_peptide_role_general_substrate_ready_count"
            ],
            0,
        )
        self.assertTrue(
            metadata["unified_review_only_scoring_passes_current_controls"]
        )
        self.assertEqual(
            metadata["unified_review_only_scoring_positive_full_score_count"], 8
        )
        self.assertEqual(
            metadata[
                "unified_review_only_scoring_control_false_non_abstention_count"
            ],
            0,
        )
        self.assertEqual(
            metadata[
                "unified_review_only_scoring_external_hard_negative_non_abstention_count"
            ],
            0,
        )
        self.assertEqual(
            metadata["unified_prototype_broad_stress_status"],
            "bounded_stress_has_source_validation_counterexamples_review_only",
        )
        self.assertEqual(
            metadata[
                "unified_prototype_broad_stress_blocked_or_rejected_pdb_ids"
            ],
            [
                "2JJ2",
                "4HPU",
                "7B56",
                "7T55",
                "7T56",
                "7T57",
                "7ZDT",
                "7ZDU",
                "7ZE5",
                "9L3M",
                "9L3U",
            ],
        )
        self.assertFalse(metadata["unified_prototype_broad_stress_complete"])
        self.assertEqual(
            metadata["family_specific_template_validated_family_ids"],
            ["atp_grasp", "pfka", "pfkb"],
        )
        self.assertTrue(
            metadata["counteraxis_sufficient_to_block_distance_only_threshold"]
        )
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        axes = {row["decision_axis"]: row for row in decision["decision_rows"]}
        self.assertEqual(
            axes["family_specific_sibling_counteraxis"]["candidate_threshold_hit_count"],
            16,
        )
        self.assertEqual(
            axes["family_specific_sibling_counteraxis"]["decision"],
            "blocks_distance_only_threshold_selection",
        )
        self.assertEqual(
            axes["imported_external_hard_negatives"]["decision"],
            "abstain_until_real_epk_axes_exist",
        )
        self.assertEqual(
            axes["chain_ligand_acceptor_disambiguation_feature"]["decision"],
            "passes_current_controls_but_not_production_admissible",
        )
        self.assertEqual(
            axes["heteromeric_peptide_acceptor_identity_feature"]["decision"],
            "passes_current_controls_and_external_feature_probe_but_narrow_not_production_admissible",
        )
        self.assertEqual(
            axes["heteromeric_peptide_acceptor_identity_feature"]["blocker"],
            "peptide_acceptor_identity_axis_narrow_not_general_epk_acceptor_identity",
        )
        self.assertEqual(
            axes["heteromeric_source_expansion_peptide_role_axis"]["decision"],
            "passes_source_expansion_controls_but_peptide_axis_narrow_not_production_admissible",
        )
        self.assertEqual(
            axes["heteromeric_source_expansion_peptide_role_axis"]["blocker"],
            "source_expansion_peptide_role_axis_narrow_not_general_epk_substrate_identity",
        )
        self.assertEqual(
            axes["general_substrate_identity_gap_audit"]["decision"],
            "relaxed_polymer_rule_false_hits_keep_general_identity_closed",
        )
        self.assertEqual(
            axes["general_substrate_identity_gap_audit"][
                "nonpositive_relaxed_polymer_false_hit_pdb_ids"
            ],
            ["7B56"],
        )
        self.assertEqual(
            axes["length_band_substrate_identity_counteraxis_audit"]["decision"],
            "blocks_relaxed_false_hit_in_source_expansion_subset_but_not_production_admissible",
        )
        self.assertEqual(
            axes["length_band_substrate_identity_counteraxis_audit"][
                "nonpositive_relaxed_false_hit_blocked_by_length_band_pdb_ids"
            ],
            ["7B56"],
        )
        self.assertEqual(
            axes["midlength_protein_role_counteraxis_audit"]["decision"],
            "blocks_midlength_false_hit_but_broad_positive_missing",
        )
        self.assertEqual(
            axes["midlength_protein_role_counteraxis_audit"][
                "blocked_midlength_false_hit_pdb_ids"
            ],
            ["7B56"],
        )
        self.assertEqual(
            axes["midlength_protein_role_counteraxis_audit"][
                "source_valid_short_or_peptide_mode_pdb_ids"
            ],
            ["6Z3R", "8OXM", "8OXO"],
        )
        self.assertEqual(
            axes["source_free_protein_substrate_role_discriminator"]["decision"],
            "passes_current_controls_but_not_general_or_calibrated",
        )
        self.assertEqual(
            axes["source_free_protein_substrate_role_discriminator"][
                "protein_substrate_role_hit_pdb_ids"
            ],
            ["1IR3", "2PHK", "5HVK"],
        )
        self.assertEqual(
            axes["source_free_protein_substrate_role_discriminator"]["blocker"],
            "protein_substrate_role_discriminator_not_general_substrate_identity_or_calibrated_score",
        )
        self.assertEqual(
            axes[
                "source_free_protein_substrate_role_discriminator_stress"
            ]["decision"],
            "fails_closed_false_hit_keeps_generalization_closed",
        )
        self.assertEqual(
            axes[
                "source_free_protein_substrate_role_discriminator_stress"
            ]["false_hit_pdb_ids"],
            ["7B56"],
        )
        self.assertEqual(
            axes["unified_review_only_scoring_prototype"]["decision"],
            "passes_current_controls_but_review_only_not_calibrated",
        )
        self.assertEqual(
            axes["unified_review_only_scoring_prototype"][
                "external_hard_negative_non_abstention_count"
            ],
            0,
        )
        self.assertEqual(
            axes["unified_prototype_broad_stress_audit"]["decision"],
            "counterexamples_found_keep_threshold_closed",
        )
        self.assertEqual(
            axes["unified_prototype_broad_stress_audit"][
                "source_validation_blocked_or_rejected_pdb_ids"
            ],
            [
                "2JJ2",
                "4HPU",
                "7B56",
                "7T55",
                "7T56",
                "7T57",
                "7ZDT",
                "7ZDU",
                "7ZE5",
                "9L3M",
                "9L3U",
            ],
        )

    def test_epk_substrate_acceptor_counteraxis_prototype_fails_closed(self) -> None:
        prototype = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_substrate_acceptor_counteraxis_prototype_1025.json"
        )
        metadata = prototype["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_substrate_acceptor_counteraxis_prototype",
        )
        self.assertTrue(metadata["review_only"])
        self.assertTrue(metadata["decision_surface_changed"])
        self.assertEqual(metadata["positive_like_acceptor_axis_row_count"], 3)
        self.assertEqual(metadata["blocked_counteraxis_row_count"], 20)
        self.assertEqual(metadata["external_hard_negative_abstention_row_count"], 3)
        self.assertEqual(
            metadata["counteraxis_rule_decision_counts"],
            {
                "blocked_by_non_hydroxyl_phosphohistidine_counteraxis": 4,
                "blocked_by_sibling_family_acceptor_counteraxis": 16,
                "external_hard_negative_abstain_missing_epk_acceptor_axes": 3,
                "positive_like_acceptor_axis_review_only": 3,
            },
        )
        self.assertIn(
            "source_supported_acceptor_axis_is_review_context_not_predictive",
            metadata["weak_axes"],
        )
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows = prototype["rows"]
        m_csa640 = [row for row in rows if row.get("entry_id") == "m_csa:640"][0]
        self.assertEqual(
            m_csa640["counteraxis_rule_decision"],
            "positive_like_acceptor_axis_review_only",
        )
        self.assertEqual(m_csa640["pdb_id"], "3TM0")
        self.assertEqual(
            m_csa640["acceptor_context_type"],
            "acceptor_like_ligand_analog",
        )
        blocked_families = {
            row["family_id"]
            for row in rows
            if row["counteraxis_rule_decision"]
            == "blocked_by_sibling_family_acceptor_counteraxis"
        }
        self.assertEqual(blocked_families, {"atp_grasp", "pfka", "pfkb"})
        for row in rows:
            self.assertTrue(row["review_only"])
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_external_hard_negative_counteraxis_review_stays_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_external_hard_negative_counteraxis_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_external_hard_negative_counteraxis_review",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["row_count"], 3)
        self.assertEqual(
            metadata["review_only_external_hard_negative_abstention_count"],
            3,
        )
        self.assertEqual(
            metadata["review_only_external_hard_negative_non_abstention_count"],
            0,
        )
        self.assertTrue(metadata["review_only_external_hard_negative_check_complete"])
        self.assertFalse(metadata["clean_heldout_performance_claim_permitted"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            sorted(row["entry_id"] for row in review["rows"]),
            ["uniprot:P06744", "uniprot:P78549", "uniprot:Q3LXA3"],
        )
        for row in review["rows"]:
            self.assertEqual(
                row["review_status"],
                "review_only_external_hard_negative_abstention",
            )
            self.assertFalse(row["review_only_counteraxis_non_abstention"])
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_epk_text_free_acceptor_feature_gap_audit_fails_closed(self) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_text_free_acceptor_feature_gap_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_text_free_acceptor_feature_gap_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["row_count"], 23)
        self.assertEqual(metadata["current_positive_feature_hit_count"], 3)
        self.assertEqual(metadata["negative_control_row_count"], 20)
        self.assertEqual(metadata["negative_control_false_hit_count"], 11)
        self.assertEqual(metadata["candidate_feature_status"], "blocked_review_only")
        self.assertEqual(
            metadata["primary_blocker"],
            "nearest_oxygen_feature_false_hits_sibling_controls",
        )
        self.assertEqual(
            metadata["negative_control_false_hit_family_ids"],
            ["atp_grasp", "ndk", "pfka", "pfkb"],
        )
        self.assertEqual(
            metadata["negative_control_false_hit_family_counts"],
            {"atp_grasp": 2, "ndk": 4, "pfka": 4, "pfkb": 1},
        )
        self.assertFalse(metadata["feature_admissible_for_scoring"])
        self.assertFalse(metadata["threshold_calibrated"])
        self.assertFalse(metadata["epk_score_computed"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        decisions = metadata["feature_audit_decision_counts"]
        self.assertEqual(
            decisions["control_false_hit_blocks_text_free_feature"],
            11,
        )
        self.assertEqual(decisions["positive_text_free_nearest_oxygen_hit_review_only"], 3)
        for row in audit["rows"]:
            self.assertTrue(row["review_only"])
            self.assertTrue(row["text_free_inputs_only"])
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_mek_erk_phosphosite_source_review_with_records(self) -> None:
        review = {
            "metadata": {
                "method": "epk_heteromeric_candidate_source_validation_review",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
            },
            "rows": [
                {
                    "pdb_id": "9TST",
                    "source_pair_id": "mek1_erk1",
                    "source_validation_status": (
                        "blocked_mek_erk_role_direction_or_phosphosite_state_unresolved_review_only"
                    ),
                    "structure_title": "MEK1/ERK1 test complex",
                    "chain_accessions": {"A": ["Q02750"], "B": ["P27361"]},
                    "candidate_hits": [
                        {
                            "candidate_chain_name": "B",
                            "candidate_auth_seq_id": "204",
                            "candidate_residue_code": "TYR",
                            "gamma_associated_polymer_chain_name": "A",
                            "nearest_gamma_distance_angstrom": 3.5,
                        }
                    ],
                }
            ],
        }
        cif_text = """
data_9TST
_struct.title 'MEK1 ERK1 test complex'
#
loop_
_struct_ref_seq.align_id
_struct_ref_seq.ref_id
_struct_ref_seq.pdbx_PDB_id_code
_struct_ref_seq.pdbx_strand_id
_struct_ref_seq.seq_align_beg
_struct_ref_seq.pdbx_seq_align_beg_ins_code
_struct_ref_seq.seq_align_end
_struct_ref_seq.pdbx_seq_align_end_ins_code
_struct_ref_seq.pdbx_db_accession
_struct_ref_seq.db_align_beg
_struct_ref_seq.pdbx_db_align_beg_ins_code
_struct_ref_seq.db_align_end
_struct_ref_seq.pdbx_db_align_end_ins_code
_struct_ref_seq.pdbx_auth_seq_align_beg
_struct_ref_seq.pdbx_auth_seq_align_end
1 1 9TST A 1 ? 393 ? Q02750 1 ? 393 ? 1 393
2 2 9TST B 1 ? 379 ? P27361 1 ? 379 ? 1 379
#
loop_
_pdbx_struct_mod_residue.id
_pdbx_struct_mod_residue.label_asym_id
_pdbx_struct_mod_residue.label_comp_id
_pdbx_struct_mod_residue.label_seq_id
_pdbx_struct_mod_residue.auth_asym_id
_pdbx_struct_mod_residue.auth_comp_id
_pdbx_struct_mod_residue.auth_seq_id
_pdbx_struct_mod_residue.PDB_ins_code
_pdbx_struct_mod_residue.parent_comp_id
_pdbx_struct_mod_residue.details
1 B TPO 202 B TPO 202 ? THR 'modified residue'
#
"""
        records = {
            "Q02750": {
                "accession": "Q02750",
                "catalytic_activity_comments": [
                    {
                        "reaction": (
                            "L-tyrosyl-[protein] + ATP = O-phospho-L-tyrosyl-[protein] + ADP"
                        )
                    }
                ],
                "modified_residue_features": [],
            },
            "P27361": {
                "accession": "P27361",
                "catalytic_activity_comments": [],
                "modified_residue_features": [
                    {
                        "feature_type": "Modified residue",
                        "begin": 204,
                        "end": 204,
                        "description": "Phosphotyrosine; by MAP2K1 and MAP2K2",
                        "evidence": [
                            {"evidence_code": "ECO:0000269", "source": "PubMed"}
                        ],
                    }
                ],
            },
        }
        result = build_epk_mek_erk_phosphosite_source_review(
            epk_mek_erk_source_validation_review=review,
            uniprot_records_by_accession=records,
            cif_text_by_pdb={"9TST": cif_text},
        )
        metadata = result["metadata"]
        self.assertEqual(
            metadata["method"], "epk_mek_erk_phosphosite_source_review"
        )
        self.assertEqual(metadata["source_authoritative_measurement_ready_count"], 1)
        self.assertEqual(
            metadata["source_authoritative_measurement_ready_pdb_ids"], ["9TST"]
        )
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        row = result["rows"][0]
        self.assertEqual(row["candidate_uniprot_position"], 204)
        self.assertTrue(row["source_role_direction_supported"])
        self.assertTrue(row["source_authoritative_measurement_ready"])
        self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_mek_erk_role_control_rerun_stays_review_only(self) -> None:
        source_review = {
            "metadata": {
                "method": "epk_mek_erk_phosphosite_source_review",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
            },
            "rows": [
                {
                    "row_type": "mek_erk_phosphosite_source_review_candidate",
                    "pdb_id": "9TST",
                    "source_authoritative_measurement_ready": True,
                    "candidate_same_chain_as_gamma": False,
                    "candidate_uniprot_accession": "P27361",
                    "candidate_uniprot_position": 204,
                    "kinase_uniprot_accession": "Q02750",
                    "source_phosphosite_matched_candidate": True,
                    "nearest_gamma_to_candidate_acceptor_distance_angstrom": 3.5,
                    "phosphosite_source_review_status": (
                        "source_authoritative_mek1_erk1_phosphosite_measurement_ready_review_only"
                    ),
                }
            ],
        }
        protein_role = {
            "metadata": {
                "method": "epk_source_free_protein_substrate_role_discriminator_audit",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                "protein_role_control_false_hit_count": 0,
                "protein_role_external_hard_negative_non_abstention_count": 0,
            }
        }
        midlength = {
            "metadata": {
                "method": "epk_midlength_protein_role_counteraxis_audit",
                "residual_protein_role_false_hit_count": 0,
            }
        }
        result = build_epk_mek_erk_role_control_rerun(
            epk_mek_erk_phosphosite_source_review=source_review,
            epk_source_free_protein_substrate_role_discriminator_audit=protein_role,
            epk_midlength_protein_role_counteraxis_audit=midlength,
        )
        metadata = result["metadata"]
        self.assertEqual(metadata["method"], "epk_mek_erk_role_control_rerun")
        self.assertEqual(
            metadata["role_control_rerun_status"],
            "passes_review_only_with_source_reviewed_broad_rows_but_scoring_closed",
        )
        self.assertEqual(metadata["source_reviewed_broad_protein_role_hit_count"], 1)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_build_epk_mek_erk_broad_role_stress_audit_fails_closed(self) -> None:
        rerun = {
            "metadata": {
                "method": "epk_mek_erk_role_control_rerun",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                "source_reviewed_broad_protein_role_hit_pdb_ids": ["9POS"],
            }
        }
        terminal = {
            "metadata": {
                "method": "epk_ligand_specific_active_query_extension_audit",
                "known_positive_repeat_hit_pdb_ids": ["1POS"],
            },
            "rows": [
                {
                    "pdb_id": "9POS",
                    "topology_hit": True,
                    "known_context": "source_reviewed_mek_erk_positive",
                    "source_validated_positive_like": False,
                    "heteromeric_candidate_hits": [
                        {
                            "candidate_chain_name": "B",
                            "gamma_associated_polymer_chain_name": "A",
                            "candidate_auth_seq_id": "204",
                            "nearest_gamma_distance_angstrom": 4.0,
                        }
                    ],
                },
                {
                    "pdb_id": "7BAD",
                    "topology_hit": True,
                    "known_context": "prior_counterexample_repeat",
                    "source_validated_positive_like": False,
                    "heteromeric_candidate_hits": [
                        {
                            "candidate_chain_name": "D",
                            "gamma_associated_polymer_chain_name": "C",
                            "candidate_auth_seq_id": "12",
                            "nearest_gamma_distance_angstrom": 3.2,
                        }
                    ],
                },
                {
                    "pdb_id": "1POS",
                    "topology_hit": True,
                    "known_context": "known_source_valid_positive_repeat",
                    "source_validated_positive_like": False,
                    "heteromeric_candidate_hits": [
                        {
                            "candidate_chain_name": "F",
                            "gamma_associated_polymer_chain_name": "E",
                            "candidate_auth_seq_id": "3",
                            "nearest_gamma_distance_angstrom": 5.5,
                        }
                    ],
                },
                {
                    "pdb_id": "9SAME",
                    "topology_hit": True,
                    "known_context": "same_chain_artifact",
                    "source_validated_positive_like": False,
                    "heteromeric_candidate_hits": [
                        {
                            "candidate_chain_name": "A",
                            "gamma_associated_polymer_chain_name": "A",
                            "candidate_auth_seq_id": "194",
                            "nearest_gamma_distance_angstrom": 3.5,
                        }
                    ],
                },
            ],
        }
        result = build_epk_mek_erk_broad_role_stress_audit(
            epk_mek_erk_role_control_rerun=rerun,
            epk_multi_query_active_site_terminal_audit=terminal,
        )
        metadata = result["metadata"]
        self.assertEqual(metadata["method"], "epk_mek_erk_broad_role_stress_audit")
        self.assertEqual(
            metadata["broad_role_stress_status"],
            "fails_closed_naive_broad_role_rule_false_hits_terminal_surface",
        )
        self.assertEqual(
            metadata["source_reviewed_mek_erk_positive_retained_pdb_ids"], ["9POS"]
        )
        self.assertEqual(
            metadata["nonpositive_naive_broad_role_false_hit_pdb_ids"], ["7BAD"]
        )
        self.assertEqual(metadata["nonpositive_same_chain_blocked_pdb_ids"], ["9SAME"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_build_epk_mek_erk_context_counteraxis_stress_audit_reduces_false_hits(
        self,
    ) -> None:
        broad = {
            "metadata": {
                "method": "epk_mek_erk_broad_role_stress_audit",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                "candidate_threshold_angstrom": 6.0,
            },
            "rows": [
                {
                    "pdb_id": "9POS",
                    "broad_role_stress_decision": (
                        "source_reviewed_mek_erk_positive_retained_review_only"
                    ),
                    "source_reviewed_mek_erk_positive": True,
                    "known_positive_repeat_or_source_valid": False,
                    "naive_broad_protein_role_rule_hit": True,
                    "candidate_same_chain_as_gamma": False,
                },
                {
                    "pdb_id": "7OLD",
                    "broad_role_stress_decision": (
                        "nonpositive_naive_broad_role_false_hit_review_only"
                    ),
                    "known_context": "prior_counterexample_repeat",
                    "source_reviewed_mek_erk_positive": False,
                    "known_positive_repeat_or_source_valid": False,
                    "naive_broad_protein_role_rule_hit": True,
                    "candidate_same_chain_as_gamma": False,
                },
                {
                    "pdb_id": "7NEW",
                    "broad_role_stress_decision": (
                        "nonpositive_naive_broad_role_false_hit_review_only"
                    ),
                    "known_context": "new_topology_hit_needs_source_adjudication",
                    "source_reviewed_mek_erk_positive": False,
                    "known_positive_repeat_or_source_valid": False,
                    "naive_broad_protein_role_rule_hit": True,
                    "candidate_same_chain_as_gamma": False,
                },
            ],
        }
        result = build_epk_mek_erk_context_counteraxis_stress_audit(
            epk_mek_erk_broad_role_stress_audit=broad
        )
        metadata = result["metadata"]
        self.assertEqual(
            metadata["method"], "epk_mek_erk_context_counteraxis_stress_audit"
        )
        self.assertEqual(
            metadata["context_counteraxis_status"],
            "fails_closed_context_counteraxis_reduces_but_does_not_clear_false_hits",
        )
        self.assertEqual(metadata["prior_counterexample_context_blocked_pdb_ids"], ["7OLD"])
        self.assertEqual(metadata["residual_new_topology_false_hit_pdb_ids"], ["7NEW"])
        self.assertTrue(metadata["decision_surface_changed"])
        self.assertFalse(metadata["source_free_predictive_feature_materialized"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_build_epk_mek_erk_residual_false_hit_source_adjudication_blocks_transporter(
        self,
    ) -> None:
        context = {
            "metadata": {
                "method": "epk_mek_erk_context_counteraxis_stress_audit",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                "residual_new_topology_false_hit_pdb_ids": ["7TRN"],
            },
            "rows": [
                {
                    "pdb_id": "7TRN",
                    "context_counteraxis_decision": (
                        "residual_new_topology_false_hit_review_only"
                    ),
                }
            ],
        }
        source_review = {
            "metadata": {"method": "epk_heteromeric_candidate_source_validation_review"},
            "rows": [
                {
                    "pdb_id": "7TRN",
                    "source_validation_status": (
                        "blocked_source_context_insufficient_review_only"
                    ),
                    "source_validation_evidence": [
                        "no_explicit_kinase_substrate_source_context_detected"
                    ],
                    "entity_descriptions": [
                        "ABC transporter, ATP-binding protein",
                        "MAGNESIUM ION",
                    ],
                    "keywords": ["TRANSPORT PROTEIN"],
                    "chain_accessions": {"A": ["P00001"], "B": ["P00002"]},
                    "candidate_hits": [{"nearest_gamma_distance_angstrom": 3.4}],
                }
            ],
        }
        result = build_epk_mek_erk_residual_false_hit_source_adjudication(
            epk_mek_erk_context_counteraxis_stress_audit=context,
            epk_ligand_specific_active_query_source_validation_reviews=[
                source_review
            ],
        )
        metadata = result["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_mek_erk_residual_false_hit_source_adjudication",
        )
        self.assertEqual(
            metadata["source_adjudication_status"],
            "passes_review_only_residual_false_hits_terminally_blocked_not_source_free",
        )
        self.assertEqual(
            metadata["terminally_blocked_residual_false_hit_pdb_ids"], ["7TRN"]
        )
        self.assertEqual(metadata["unresolved_residual_false_hit_count"], 0)
        self.assertEqual(metadata["transporter_false_hit_pdb_ids"], ["7TRN"])
        self.assertTrue(metadata["source_context_counterevidence_used"])
        self.assertFalse(metadata["source_free_predictive_feature_materialized"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertTrue(
            result["rows"][0]["terminally_blocked_as_broad_role_false_hit"]
        )

    def test_build_epk_mek_erk_source_free_topology_ambiguity_counteraxis_blocks_residuals(
        self,
    ) -> None:
        source_review = {
            "metadata": {
                "method": "epk_mek_erk_phosphosite_source_review",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                "source_authoritative_measurement_ready_pdb_ids": ["9POS"],
            },
            "rows": [
                {
                    "pdb_id": "9POS",
                    "phosphosite_source_review_status": (
                        "source_authoritative_mek1_erk1_phosphosite_measurement_ready_review_only"
                    ),
                    "candidate_hit": {
                        "candidate_chain_name": "B",
                        "candidate_auth_seq_id": "204",
                        "candidate_residue_code": "TYR",
                        "gamma_associated_polymer_chain_name": "A",
                        "nearest_gamma_distance_angstrom": 4.1,
                    },
                }
            ],
        }
        context = {
            "metadata": {
                "method": "epk_mek_erk_context_counteraxis_stress_audit",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                "residual_new_topology_false_hit_pdb_ids": ["7TRN", "8XSW"],
            },
            "rows": [],
        }
        candidate_artifact = {
            "metadata": {"method": "candidate_context_fixture"},
            "rows": [
                {
                    "pdb_id": "7TRN",
                    "candidate_hits": [
                        {
                            "candidate_chain_name": "D",
                            "candidate_auth_seq_id": "140",
                            "candidate_residue_code": "SER",
                            "gamma_associated_polymer_chain_name": "C",
                            "nearest_gamma_distance_angstrom": 4.0,
                        },
                        {
                            "candidate_chain_name": "C",
                            "candidate_auth_seq_id": "48",
                            "candidate_residue_code": "SER",
                            "gamma_associated_polymer_chain_name": "C",
                            "nearest_gamma_distance_angstrom": 4.8,
                        },
                    ],
                },
                {
                    "pdb_id": "8XSW",
                    "candidate_hits": [
                        {
                            "candidate_chain_name": "B",
                            "candidate_auth_seq_id": "147",
                            "candidate_residue_code": "SER",
                            "gamma_associated_polymer_chain_name": "A",
                            "nearest_gamma_distance_angstrom": 3.4,
                        },
                        {
                            "candidate_chain_name": "A",
                            "candidate_auth_seq_id": "145",
                            "candidate_residue_code": "SER",
                            "gamma_associated_polymer_chain_name": "B",
                            "nearest_gamma_distance_angstrom": 3.5,
                        },
                    ],
                },
            ],
        }
        result = build_epk_mek_erk_source_free_topology_ambiguity_counteraxis(
            epk_mek_erk_phosphosite_source_review=source_review,
            epk_mek_erk_context_counteraxis_stress_audit=context,
            candidate_context_artifacts=[candidate_artifact],
        )
        metadata = result["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_mek_erk_source_free_topology_ambiguity_counteraxis",
        )
        self.assertEqual(
            metadata["source_free_counteraxis_status"],
            "passes_bounded_residual_controls_source_free_topology_ambiguity_review_only",
        )
        self.assertEqual(
            metadata["source_reviewed_positive_retained_pdb_ids"], ["9POS"]
        )
        self.assertEqual(metadata["source_reviewed_positive_lost_count"], 0)
        self.assertEqual(
            metadata["residual_false_hit_blocked_pdb_ids"], ["7TRN", "8XSW"]
        )
        self.assertEqual(metadata["residual_false_hit_unblocked_count"], 0)
        self.assertEqual(metadata["missing_local_topology_hit_count"], 0)
        self.assertTrue(metadata["source_free_predictive_feature_materialized"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_build_epk_mek_erk_source_free_topology_broader_stress_audit_fails_closed(
        self,
    ) -> None:
        broad_role = {
            "metadata": {
                "method": "epk_mek_erk_broad_role_stress_audit",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                "candidate_threshold_angstrom": 6.0,
            },
            "rows": [
                {
                    "pdb_id": "9POS",
                    "naive_broad_protein_role_rule_hit": True,
                    "source_reviewed_mek_erk_positive": True,
                    "known_positive_repeat_or_source_valid": False,
                    "broad_role_stress_decision": (
                        "source_reviewed_mek_erk_positive_retained_review_only"
                    ),
                    "candidate_chain_name": "B",
                    "gamma_associated_polymer_chain_name": "A",
                    "nearest_gamma_distance_angstrom": 4.1,
                },
                {
                    "pdb_id": "7TRN",
                    "naive_broad_protein_role_rule_hit": True,
                    "source_reviewed_mek_erk_positive": False,
                    "known_positive_repeat_or_source_valid": False,
                    "broad_role_stress_decision": (
                        "nonpositive_naive_broad_role_false_hit_review_only"
                    ),
                    "candidate_chain_name": "D",
                    "gamma_associated_polymer_chain_name": "C",
                    "nearest_gamma_distance_angstrom": 4.0,
                },
                {
                    "pdb_id": "8OPEN",
                    "naive_broad_protein_role_rule_hit": True,
                    "source_reviewed_mek_erk_positive": False,
                    "known_positive_repeat_or_source_valid": False,
                    "broad_role_stress_decision": (
                        "nonpositive_naive_broad_role_false_hit_review_only"
                    ),
                    "candidate_chain_name": "B",
                    "gamma_associated_polymer_chain_name": "A",
                    "nearest_gamma_distance_angstrom": 3.4,
                },
            ],
        }
        candidate_artifact = {
            "metadata": {"method": "candidate_context_fixture"},
            "rows": [
                {
                    "pdb_id": "7TRN",
                    "candidate_hits": [
                        {
                            "candidate_chain_name": "C",
                            "candidate_auth_seq_id": "48",
                            "candidate_residue_code": "SER",
                            "gamma_associated_polymer_chain_name": "C",
                            "nearest_gamma_distance_angstrom": 4.8,
                        }
                    ],
                }
            ],
        }
        result = build_epk_mek_erk_source_free_topology_broader_stress_audit(
            epk_mek_erk_broad_role_stress_audit=broad_role,
            candidate_context_artifacts=[candidate_artifact],
        )
        metadata = result["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_mek_erk_source_free_topology_broader_stress_audit",
        )
        self.assertEqual(
            metadata["broader_stress_status"],
            "fails_closed_broader_topology_ambiguity_residual_false_hits",
        )
        self.assertEqual(metadata["positive_control_retained_pdb_ids"], ["9POS"])
        self.assertEqual(metadata["false_hit_blocked_pdb_ids"], ["7TRN"])
        self.assertEqual(metadata["residual_false_hit_pdb_ids"], ["8OPEN"])
        self.assertTrue(metadata["source_free_predictive_feature_materialized"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_build_epk_mek_erk_substrate_mode_counteraxis_audit_blocks_residuals(
        self,
    ) -> None:
        stress = {
            "metadata": {
                "method": "epk_mek_erk_source_free_topology_broader_stress_audit",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                "candidate_threshold_angstrom": 6.0,
            },
            "rows": [
                {
                    "pdb_id": "9POS",
                    "known_positive_control": True,
                    "known_false_hit_control": False,
                    "topology_ambiguity_counteraxis_hit": False,
                    "candidate_hits": [
                        {
                            "candidate_residue_code": "TYR",
                            "candidate_auth_seq_id": "204",
                            "candidate_chain_name": "B",
                            "gamma_associated_polymer_chain_name": "A",
                            "nearest_gamma_distance_angstrom": 4.1,
                        }
                    ],
                },
                {
                    "pdb_id": "5PEP",
                    "known_positive_control": True,
                    "known_false_hit_control": False,
                    "topology_ambiguity_counteraxis_hit": False,
                    "candidate_hits": [
                        {
                            "candidate_residue_code": "SER",
                            "candidate_auth_seq_id": "3",
                            "candidate_chain_name": "D",
                            "gamma_associated_polymer_chain_name": "C",
                            "nearest_gamma_distance_angstrom": 4.2,
                        }
                    ],
                },
                {
                    "pdb_id": "7TOPO",
                    "known_positive_control": False,
                    "known_false_hit_control": True,
                    "topology_ambiguity_counteraxis_hit": True,
                    "candidate_hits": [
                        {
                            "candidate_residue_code": "SER",
                            "candidate_auth_seq_id": "140",
                            "candidate_chain_name": "D",
                            "gamma_associated_polymer_chain_name": "C",
                            "nearest_gamma_distance_angstrom": 4.0,
                        }
                    ],
                },
                {
                    "pdb_id": "8BAD",
                    "known_positive_control": False,
                    "known_false_hit_control": True,
                    "topology_ambiguity_counteraxis_hit": False,
                    "candidate_hits": [
                        {
                            "candidate_residue_code": "SER",
                            "candidate_auth_seq_id": "344",
                            "candidate_chain_name": "I",
                            "gamma_associated_polymer_chain_name": "M",
                            "nearest_gamma_distance_angstrom": 5.4,
                        }
                    ],
                },
            ],
        }
        result = build_epk_mek_erk_substrate_mode_counteraxis_audit(
            epk_mek_erk_source_free_topology_broader_stress_audit=stress
        )
        metadata = result["metadata"]
        self.assertEqual(
            metadata["method"], "epk_mek_erk_substrate_mode_counteraxis_audit"
        )
        self.assertEqual(
            metadata["substrate_mode_counteraxis_status"],
            "passes_current_broad_stress_substrate_mode_controls_review_only",
        )
        self.assertEqual(metadata["positive_control_retained_pdb_ids"], ["5PEP", "9POS"])
        self.assertEqual(metadata["positive_control_lost_count"], 0)
        self.assertEqual(metadata["false_hit_blocked_by_topology_pdb_ids"], ["7TOPO"])
        self.assertEqual(
            metadata["false_hit_blocked_by_substrate_mode_pdb_ids"], ["8BAD"]
        )
        self.assertEqual(metadata["residual_false_hit_count"], 0)
        self.assertTrue(metadata["source_free_predictive_feature_materialized"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_build_epk_mek_erk_substrate_mode_fresh_stress_audit_blocks_fresh(
        self,
    ) -> None:
        substrate = {
            "metadata": {
                "method": "epk_mek_erk_substrate_mode_counteraxis_audit",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                "candidate_threshold_angstrom": 6.0,
                "max_n_terminal_acceptor_auth_seq_id": 25,
            },
            "rows": [
                {
                    "pdb_id": "9REP",
                }
            ],
        }
        scout = {
            "metadata": {
                "method": "epk_heteromeric_positive_coverage_candidate_scout"
            },
            "rows": [
                {
                    "pdb_id": "7NEW",
                    "heteromeric_candidate_hits": [
                        {
                            "candidate_residue_code": "SER",
                            "candidate_auth_seq_id": "467",
                            "candidate_chain_name": "A",
                            "gamma_associated_polymer_chain_name": "A",
                            "nearest_gamma_distance_angstrom": 3.9,
                        }
                    ],
                },
                {
                    "pdb_id": "9REP",
                    "heteromeric_candidate_hits": [
                        {
                            "candidate_residue_code": "TYR",
                            "candidate_auth_seq_id": "204",
                            "candidate_chain_name": "B",
                            "gamma_associated_polymer_chain_name": "A",
                            "nearest_gamma_distance_angstrom": 4.1,
                        }
                    ],
                },
            ],
        }
        validation = {
            "metadata": {
                "method": "epk_heteromeric_candidate_source_validation_review"
            },
            "rows": [
                {
                    "pdb_id": "7NEW",
                    "source_validation_status": (
                        "blocked_ambiguous_kinase_kinase_role_direction_review_only"
                    ),
                    "source_pair_id": None,
                }
            ],
        }
        result = build_epk_mek_erk_substrate_mode_fresh_stress_audit(
            epk_mek_erk_substrate_mode_counteraxis_audit=substrate,
            epk_mek_erk_targeted_candidate_scout=scout,
            epk_mek_erk_targeted_source_validation_review=validation,
        )
        metadata = result["metadata"]
        self.assertEqual(
            metadata["method"], "epk_mek_erk_substrate_mode_fresh_stress_audit"
        )
        self.assertEqual(
            metadata["substrate_mode_fresh_stress_status"],
            "passes_fresh_nonrepeat_controls_with_topology_confounding_review_only",
        )
        self.assertEqual(metadata["fresh_nonrepeat_candidate_pdb_ids"], ["7NEW"])
        self.assertEqual(metadata["fresh_nonrepeat_rule_hit_count"], 0)
        self.assertEqual(
            metadata["fresh_nonrepeat_rejected_by_substrate_mode_pdb_ids"],
            ["7NEW"],
        )
        self.assertEqual(
            metadata["repeat_current_surface_rule_hit_pdb_ids"], ["9REP"]
        )
        self.assertTrue(metadata["fresh_stress_topology_confounded"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_build_epk_mek_erk_substrate_mode_existing_scout_gap_audit_blocks_reuse(
        self,
    ) -> None:
        substrate = {
            "metadata": {
                "method": "epk_mek_erk_substrate_mode_counteraxis_audit",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
            },
            "rows": [{"pdb_id": "9OLD"}],
        }
        fresh = {
            "metadata": {
                "method": "epk_mek_erk_substrate_mode_fresh_stress_audit"
            },
            "rows": [{"pdb_id": "7SEEN"}],
        }
        scout = {
            "metadata": {
                "method": "epk_heteromeric_positive_coverage_candidate_scout",
                "source_query": "unit-test",
            },
            "rows": [
                {
                    "pdb_id": "7NEW",
                    "heteromeric_candidate_hits": [
                        {
                            "candidate_residue_code": "SER",
                            "candidate_auth_seq_id": "467",
                            "candidate_chain_name": "A",
                            "gamma_associated_polymer_chain_name": "A",
                            "nearest_gamma_distance_angstrom": 3.9,
                        }
                    ],
                }
            ],
        }
        result = build_epk_mek_erk_substrate_mode_existing_scout_gap_audit(
            epk_mek_erk_substrate_mode_counteraxis_audit=substrate,
            epk_mek_erk_substrate_mode_fresh_stress_audit=fresh,
            candidate_context_artifacts=[scout],
        )
        metadata = result["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_mek_erk_substrate_mode_existing_scout_gap_audit",
        )
        self.assertEqual(
            metadata["existing_scout_gap_status"],
            "blocked_existing_scouts_only_topology_confounded_candidates_review_only",
        )
        self.assertEqual(metadata["materialized_unreviewed_hit_pdb_ids"], ["7NEW"])
        self.assertEqual(metadata["topology_confounded_candidate_pdb_ids"], ["7NEW"])
        self.assertEqual(metadata["non_topology_confounded_candidate_count"], 0)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_build_epk_substrate_mode_next_tranche_source_review_maps_akt_gsk3b(
        self,
    ) -> None:
        substrate = {
            "metadata": {
                "method": "epk_mek_erk_substrate_mode_counteraxis_audit",
                "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                "candidate_threshold_angstrom": 6.0,
                "max_n_terminal_acceptor_auth_seq_id": 25,
            }
        }
        scout = {
            "metadata": {
                "method": "epk_heteromeric_positive_coverage_candidate_scout",
                "source_query": "unit-test AMP-PNP tranche",
            },
            "rows": [
                {
                    "pdb_id": "4EKK",
                    "candidate_status": (
                        "heteromeric_candidate_source_validation_pending_review_only"
                    ),
                    "heteromeric_candidate_hits": [
                        {
                            "candidate_residue_code": "SER",
                            "candidate_auth_seq_id": "7",
                            "candidate_chain_name": "C",
                            "gamma_associated_polymer_chain_name": "A",
                            "nearest_gamma_distance_angstrom": 3.257,
                        }
                    ],
                }
            ],
        }
        source_validation = {
            "metadata": {
                "method": "epk_heteromeric_candidate_source_validation_review"
            },
            "rows": [
                {
                    "pdb_id": "4EKK",
                    "source_validation_status": (
                        "blocked_source_context_insufficient_review_only"
                    ),
                    "chain_accessions": {
                        "A": ["P31749"],
                        "C": ["P49841"],
                    },
                }
            ],
        }
        cif_text = """
data_4EKK
loop_
_struct.entry_id
_struct.title
4EKK 'Akt1 with AMP-PNP'
loop_
_struct_ref_seq.align_id
_struct_ref_seq.ref_id
_struct_ref_seq.pdbx_PDB_id_code
_struct_ref_seq.pdbx_strand_id
_struct_ref_seq.seq_align_beg
_struct_ref_seq.pdbx_seq_align_beg_ins_code
_struct_ref_seq.seq_align_end
_struct_ref_seq.pdbx_seq_align_end_ins_code
_struct_ref_seq.pdbx_db_accession
_struct_ref_seq.db_align_beg
_struct_ref_seq.pdbx_db_align_beg_ins_code
_struct_ref_seq.db_align_end
_struct_ref_seq.pdbx_db_align_end_ins_code
_struct_ref_seq.pdbx_auth_seq_align_beg
_struct_ref_seq.pdbx_auth_seq_align_end
1 1 4EKK A 5 ? 341 ? P31749 144 ? 480 ? 144 480
2 2 4EKK C 1 ? 10 ? P49841 3 ? 12 ? 1 10
"""
        uniprot_records = {
            "P31749": {
                "accession": "P31749",
                "catalytic_activity_comments": [
                    {
                        "reaction": (
                            "ATP + L-seryl-[protein] = ADP + "
                            "O-phospho-L-seryl-[protein]"
                        )
                    }
                ],
            },
            "P49841": {
                "accession": "P49841",
                "modified_residue_features": [
                    {
                        "feature_type": "Modified residue",
                        "begin": "9",
                        "description": "Phosphoserine; by PKB/AKT1",
                        "evidence": [],
                    }
                ],
            },
        }
        result = build_epk_substrate_mode_next_tranche_source_review(
            epk_mek_erk_substrate_mode_counteraxis_audit=substrate,
            epk_next_tranche_candidate_scout=scout,
            epk_next_tranche_source_validation_review=source_validation,
            uniprot_records_by_accession=uniprot_records,
            cif_text_by_pdb={"4EKK": cif_text},
        )
        metadata = result["metadata"]
        self.assertEqual(
            metadata["method"], "epk_substrate_mode_next_tranche_source_review"
        )
        self.assertEqual(
            metadata["next_tranche_source_review_status"],
            "adds_source_mapped_non_topology_substrate_mode_row_review_only",
        )
        self.assertEqual(metadata["non_topology_confounded_candidate_pdb_ids"], ["4EKK"])
        self.assertEqual(metadata["source_mapped_measurement_ready_pdb_ids"], ["4EKK"])
        self.assertEqual(metadata["source_mapped_measurement_ready_count"], 1)
        self.assertTrue(metadata["source_context_used_as_review_evidence_only"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        row = result["rows"][0]
        self.assertEqual(row["candidate_uniprot_position"], 9)
        self.assertTrue(row["akt1_gsk3b_source_mapped"])
        self.assertTrue(row["measurement_ready_for_review_controls"])
        self.assertFalse(row["production_scoring_admissible"])

    def test_build_epk_substrate_mode_next_tranche_source_review_flags_pkb_isoform_blocker(
        self,
    ) -> None:
        substrate = {
            "metadata": {
                "method": "epk_mek_erk_substrate_mode_counteraxis_audit",
                "candidate_threshold_angstrom": 6.0,
                "max_n_terminal_acceptor_auth_seq_id": 25,
            }
        }
        scout = {
            "metadata": {
                "method": "epk_heteromeric_positive_coverage_candidate_scout"
            },
            "rows": [
                {
                    "pdb_id": "1O6K",
                    "candidate_status": (
                        "heteromeric_candidate_source_validation_pending_review_only"
                    ),
                    "heteromeric_candidate_hits": [
                        {
                            "candidate_residue_code": "SER",
                            "candidate_auth_seq_id": "7",
                            "candidate_chain_name": "C",
                            "gamma_associated_polymer_chain_name": "A",
                            "nearest_gamma_distance_angstrom": 3.566,
                        }
                    ],
                }
            ],
        }
        source_validation = {
            "metadata": {
                "method": "epk_heteromeric_candidate_source_validation_review"
            },
            "rows": [
                {
                    "pdb_id": "1O6K",
                    "source_validation_status": (
                        "accepted_source_valid_heteromeric_kinase_substrate_review_only"
                    ),
                    "source_pair_id": "pkb_gsk3",
                    "chain_accessions": {
                        "A": ["P31751"],
                        "C": ["P49841"],
                    },
                }
            ],
        }
        cif_text = """
data_1O6K
loop_
_struct.entry_id
_struct.title
1O6K 'PKB beta with GSK3 peptide'
loop_
_struct_ref_seq.align_id
_struct_ref_seq.ref_id
_struct_ref_seq.pdbx_PDB_id_code
_struct_ref_seq.pdbx_strand_id
_struct_ref_seq.seq_align_beg
_struct_ref_seq.pdbx_seq_align_beg_ins_code
_struct_ref_seq.seq_align_end
_struct_ref_seq.pdbx_seq_align_end_ins_code
_struct_ref_seq.pdbx_db_accession
_struct_ref_seq.db_align_beg
_struct_ref_seq.pdbx_db_align_beg_ins_code
_struct_ref_seq.db_align_end
_struct_ref_seq.pdbx_db_align_end_ins_code
_struct_ref_seq.pdbx_auth_seq_align_beg
_struct_ref_seq.pdbx_auth_seq_align_end
1 1 1O6K A 5 ? 341 ? P31751 144 ? 480 ? 144 480
2 2 1O6K C 1 ? 10 ? P49841 3 ? 12 ? 1 10
"""
        uniprot_records = {
            "P31751": {
                "accession": "P31751",
                "catalytic_activity_comments": [
                    {
                        "reaction": (
                            "ATP + L-seryl-[protein] = ADP + "
                            "O-phospho-L-seryl-[protein]"
                        )
                    }
                ],
            },
            "P49841": {
                "accession": "P49841",
                "modified_residue_features": [
                    {
                        "feature_type": "Modified residue",
                        "begin": "9",
                        "description": "Phosphoserine; by PKB/AKT1",
                        "evidence": [],
                    }
                ],
            },
        }
        result = build_epk_substrate_mode_next_tranche_source_review(
            epk_mek_erk_substrate_mode_counteraxis_audit=substrate,
            epk_next_tranche_candidate_scout=scout,
            epk_next_tranche_source_validation_review=source_validation,
            uniprot_records_by_accession=uniprot_records,
            cif_text_by_pdb={"1O6K": cif_text},
        )
        metadata = result["metadata"]
        self.assertEqual(metadata["source_mapped_measurement_ready_count"], 0)
        self.assertEqual(metadata["source_mapping_unresolved_pdb_ids"], ["1O6K"])
        row = result["rows"][0]
        self.assertTrue(row["pkb_gsk3b_source_context_matched"])
        self.assertTrue(row["pkb_gsk3b_exact_mapping_blocked"])
        self.assertFalse(row["measurement_ready_for_review_controls"])
        self.assertIn(
            "pkb_gsk3b_source_context_detected_but_exact_akt1_or_chain_mapping_unresolved",
            row["remaining_blockers"],
        )

    def test_build_epk_substrate_mode_next_tranche_source_review_reports_rejected_tranche(
        self,
    ) -> None:
        result = build_epk_substrate_mode_next_tranche_source_review(
            epk_mek_erk_substrate_mode_counteraxis_audit={
                "metadata": {
                    "method": "epk_mek_erk_substrate_mode_counteraxis_audit",
                    "candidate_threshold_angstrom": 6.0,
                    "max_n_terminal_acceptor_auth_seq_id": 25,
                }
            },
            epk_next_tranche_candidate_scout={
                "metadata": {
                    "method": "epk_heteromeric_positive_coverage_candidate_scout"
                },
                "rows": [
                    {
                        "pdb_id": "7ZE5",
                        "candidate_status": (
                            "heteromeric_candidate_source_validation_pending_review_only"
                        ),
                        "heteromeric_candidate_hits": [
                            {
                                "candidate_residue_code": "SER",
                                "candidate_auth_seq_id": "487",
                                "candidate_chain_name": "D",
                                "gamma_associated_polymer_chain_name": "C",
                                "nearest_gamma_distance_angstrom": 3.876,
                            }
                        ],
                    }
                ],
            },
            epk_next_tranche_source_validation_review={
                "metadata": {
                    "method": "epk_heteromeric_candidate_source_validation_review"
                },
                "rows": [
                    {
                        "pdb_id": "7ZE5",
                        "source_validation_status": (
                            "blocked_source_context_insufficient_review_only"
                        ),
                        "chain_accessions": {
                            "C": ["P00001"],
                            "D": ["P00002"],
                        },
                    }
                ],
            },
            uniprot_records_by_accession={
                "P00001": {"accession": "P00001"},
                "P00002": {"accession": "P00002"},
            },
            cif_text_by_pdb={
                "7ZE5": """
data_7ZE5
loop_
_struct.entry_id
_struct.title
7ZE5 'ATP transporter'
loop_
_struct_ref_seq.align_id
_struct_ref_seq.ref_id
_struct_ref_seq.pdbx_PDB_id_code
_struct_ref_seq.pdbx_strand_id
_struct_ref_seq.seq_align_beg
_struct_ref_seq.pdbx_seq_align_beg_ins_code
_struct_ref_seq.seq_align_end
_struct_ref_seq.pdbx_seq_align_end_ins_code
_struct_ref_seq.pdbx_db_accession
_struct_ref_seq.db_align_beg
_struct_ref_seq.pdbx_db_align_beg_ins_code
_struct_ref_seq.db_align_end
_struct_ref_seq.pdbx_db_align_end_ins_code
_struct_ref_seq.pdbx_auth_seq_align_beg
_struct_ref_seq.pdbx_auth_seq_align_end
1 1 7ZE5 C 1 ? 600 ? P00001 1 ? 600 ? 1 600
2 2 7ZE5 D 1 ? 600 ? P00002 1 ? 600 ? 1 600
"""
            },
        )
        metadata = result["metadata"]
        self.assertEqual(
            metadata["next_tranche_source_review_status"],
            "fails_closed_non_topology_tranche_rejected_by_substrate_mode",
        )
        self.assertEqual(metadata["substrate_mode_rejected_pdb_ids"], ["7ZE5"])
        self.assertEqual(metadata["source_mapping_unresolved_pdb_ids"], [])
        self.assertEqual(metadata["source_mapped_measurement_ready_count"], 0)

    def test_build_epk_substrate_mode_tranche_recovery_decision_fails_closed(
        self,
    ) -> None:
        ready_review = {
            "metadata": {
                "method": "epk_substrate_mode_next_tranche_source_review",
                "source_query": "unit-test ready tranche",
                "next_tranche_source_review_status": (
                    "adds_source_mapped_non_topology_substrate_mode_row_review_only"
                ),
            },
            "rows": [
                {
                    "pdb_id": "4EKK",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                    "next_tranche_source_review_status": (
                        "source_mapped_non_topology_substrate_mode_measurement_ready_review_only"
                    ),
                    "measurement_ready_for_review_controls": True,
                    "candidate_uniprot_accession": "P49841",
                    "candidate_uniprot_position": 9,
                    "kinase_uniprot_accession": "P31749",
                    "source_phosphosite_matched_candidate": True,
                    "nearest_gamma_to_candidate_acceptor_distance_angstrom": 3.228,
                    "remaining_blockers": [
                        "source_review_evidence_not_source_free_predictive_feature"
                    ],
                }
            ],
        }
        unresolved_review = {
            "metadata": {
                "method": "epk_substrate_mode_next_tranche_source_review",
                "source_query": "unit-test unresolved tranche",
                "next_tranche_source_review_status": (
                    "fails_closed_non_topology_tranche_source_mapping_unresolved"
                ),
            },
            "rows": [
                {
                    "pdb_id": "1O6K",
                    "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
                    "next_tranche_source_review_status": (
                        "non_topology_confounded_source_mapping_unresolved_review_only"
                    ),
                    "measurement_ready_for_review_controls": False,
                    "candidate_uniprot_accession": "P49841",
                    "candidate_uniprot_position": 9,
                    "kinase_uniprot_accession": "P31751",
                    "source_phosphosite_matched_candidate": True,
                    "nearest_gamma_to_candidate_acceptor_distance_angstrom": 3.566,
                    "remaining_blockers": [
                        "source_phosphosite_or_role_direction_not_mapped_to_candidate"
                    ],
                }
            ],
        }
        result = build_epk_substrate_mode_tranche_recovery_decision(
            epk_substrate_mode_next_tranche_source_reviews=[
                ready_review,
                unresolved_review,
            ]
        )
        metadata = result["metadata"]
        self.assertEqual(
            metadata["method"], "epk_substrate_mode_tranche_recovery_decision"
        )
        self.assertEqual(
            metadata["recovery_decision_status"],
            (
                "partial_recovery_with_measurement_ready_row_and_unresolved_mapping_review_only"
            ),
        )
        self.assertEqual(metadata["measurement_ready_pdb_ids"], ["4EKK"])
        self.assertEqual(metadata["source_mapping_unresolved_pdb_ids"], ["1O6K"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertIn("fresh nonconfounded", metadata["next_experiment"])
        rows_by_pdb = {row["pdb_id"]: row for row in result["rows"]}
        self.assertFalse(rows_by_pdb["1O6K"]["measurement_ready_for_review_controls"])
        self.assertFalse(rows_by_pdb["4EKK"]["production_scoring_admissible"])

    def test_epk_mek_erk_phosphosite_source_review_artifact_stays_review_only(
        self,
    ) -> None:
        review = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_mek_erk_phosphosite_source_review_1025.json"
        )
        metadata = review["metadata"]
        self.assertEqual(
            metadata["method"], "epk_mek_erk_phosphosite_source_review"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(metadata["source_authoritative_measurement_ready_count"], 2)
        self.assertEqual(
            metadata["source_authoritative_measurement_ready_pdb_ids"],
            ["9UUR", "9UUX"],
        )
        self.assertEqual(metadata["same_chain_artifact_rejected_pdb_ids"], ["9UW4"])
        self.assertEqual(metadata["gamma_acceptor_distance_measured_count"], 2)
        self.assertFalse(metadata["source_free_predictive_feature_materialized"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        ready_rows = [
            row for row in review["rows"] if row["source_authoritative_measurement_ready"]
        ]
        self.assertEqual(len(ready_rows), 2)
        self.assertTrue(
            all(row["candidate_uniprot_accession"] == "P27361" for row in ready_rows)
        )
        precount = _load_json(
            ROOT / "artifacts" / "v3_epk_precount_gate_status_1025.json"
        )
        self.assertEqual(
            precount["metadata"]["mek_erk_source_authoritative_measurement_ready_count"],
            2,
        )
        self.assertEqual(
            precount["metadata"]["precount_gate_status"], "blocked_review_only"
        )
        counteraxis = _load_json(
            ROOT / "artifacts" / "v3_epk_counteraxis_sufficiency_decision_1025.json"
        )
        self.assertEqual(
            counteraxis["metadata"]["threshold_selection_decision"],
            "do_not_select_threshold",
        )
        mek_rows = [
            row
            for row in counteraxis["decision_rows"]
            if row["decision_axis"] == "mek_erk_phosphosite_source_review"
        ]
        self.assertEqual(len(mek_rows), 1)
        self.assertEqual(mek_rows[0]["source_authoritative_measurement_ready_count"], 2)

    def test_epk_mek_erk_role_control_rerun_artifact_stays_review_only(self) -> None:
        rerun = _load_json(
            ROOT / "artifacts" / "v3_epk_mek_erk_role_control_rerun_1025.json"
        )
        metadata = rerun["metadata"]
        self.assertEqual(metadata["method"], "epk_mek_erk_role_control_rerun")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["role_control_rerun_status"],
            "passes_review_only_with_source_reviewed_broad_rows_but_scoring_closed",
        )
        self.assertEqual(metadata["source_reviewed_broad_protein_role_hit_count"], 2)
        self.assertEqual(
            metadata["source_reviewed_broad_protein_role_hit_pdb_ids"],
            ["9UUR", "9UUX"],
        )
        self.assertEqual(metadata["same_chain_counterexample_blocked_pdb_ids"], ["9UW4"])
        self.assertEqual(metadata["carried_current_control_false_hit_count"], 0)
        self.assertEqual(
            metadata["carried_imported_external_hard_negative_non_abstention_count"],
            0,
        )
        self.assertFalse(metadata["source_free_predictive_feature_materialized"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_mek_erk_broad_role_stress_audit_artifact_fails_closed(self) -> None:
        audit = _load_json(
            ROOT / "artifacts" / "v3_epk_mek_erk_broad_role_stress_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(metadata["method"], "epk_mek_erk_broad_role_stress_audit")
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["broad_role_stress_status"],
            "fails_closed_naive_broad_role_rule_false_hits_terminal_surface",
        )
        self.assertEqual(metadata["reviewed_topology_hit_count"], 27)
        self.assertEqual(
            metadata["source_reviewed_mek_erk_positive_retained_pdb_ids"],
            ["9UUR", "9UUX"],
        )
        self.assertEqual(
            metadata["known_positive_repeat_retained_pdb_ids"],
            ["1IR3", "5HVK", "6Z3R"],
        )
        self.assertEqual(
            metadata["nonpositive_naive_broad_role_false_hit_count"], 8
        )
        self.assertEqual(
            metadata["nonpositive_naive_broad_role_false_hit_pdb_ids"],
            ["2JJ2", "4HPU", "7B56", "7CAG", "7ZDT", "7ZDU", "7ZE5", "8BMS"],
        )
        self.assertEqual(metadata["nonpositive_same_chain_blocked_count"], 14)
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        precount = _load_json(
            ROOT / "artifacts" / "v3_epk_precount_gate_status_1025.json"
        )
        self.assertEqual(
            precount["metadata"]["mek_erk_broad_role_false_hit_count"], 8
        )
        self.assertIn(
            "mek_erk_broad_role_stress_audit",
            precount["metadata"]["failing_gate_ids"],
        )
        counteraxis = _load_json(
            ROOT / "artifacts" / "v3_epk_counteraxis_sufficiency_decision_1025.json"
        )
        stress_rows = [
            row
            for row in counteraxis["decision_rows"]
            if row["decision_axis"] == "mek_erk_broad_role_stress_audit"
        ]
        self.assertEqual(len(stress_rows), 1)
        self.assertEqual(
            stress_rows[0]["decision"],
            "false_hits_keep_broad_role_rule_closed",
        )

    def test_epk_mek_erk_context_counteraxis_stress_artifact_fails_closed(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_mek_erk_context_counteraxis_stress_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"], "epk_mek_erk_context_counteraxis_stress_audit"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["context_counteraxis_status"],
            "fails_closed_context_counteraxis_reduces_but_does_not_clear_false_hits",
        )
        self.assertEqual(
            metadata["source_reviewed_mek_erk_positive_retained_pdb_ids"],
            ["9UUR", "9UUX"],
        )
        self.assertEqual(
            metadata["prior_counterexample_context_blocked_pdb_ids"],
            ["2JJ2", "4HPU", "7B56", "7ZDT", "7ZDU", "7ZE5"],
        )
        self.assertEqual(
            metadata["residual_new_topology_false_hit_pdb_ids"],
            ["7CAG", "8BMS"],
        )
        self.assertTrue(metadata["decision_surface_changed"])
        self.assertFalse(metadata["source_free_predictive_feature_materialized"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        precount = _load_json(
            ROOT / "artifacts" / "v3_epk_precount_gate_status_1025.json"
        )
        self.assertEqual(
            precount["metadata"]["mek_erk_context_residual_false_hit_pdb_ids"],
            ["7CAG", "8BMS"],
        )
        self.assertIn(
            "mek_erk_context_counteraxis_stress_audit",
            precount["metadata"]["failing_gate_ids"],
        )
        counteraxis = _load_json(
            ROOT / "artifacts" / "v3_epk_counteraxis_sufficiency_decision_1025.json"
        )
        context_rows = [
            row
            for row in counteraxis["decision_rows"]
            if row["decision_axis"] == "mek_erk_context_counteraxis_stress_audit"
        ]
        self.assertEqual(len(context_rows), 1)
        self.assertEqual(
            context_rows[0]["decision"],
            "review_context_reduces_but_residual_false_hits_remain",
        )

    def test_epk_mek_erk_residual_false_hit_source_adjudication_artifact_blocks_residuals(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_mek_erk_residual_false_hit_source_adjudication_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_mek_erk_residual_false_hit_source_adjudication",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["source_adjudication_status"],
            "passes_review_only_residual_false_hits_terminally_blocked_not_source_free",
        )
        self.assertEqual(metadata["residual_false_hit_input_pdb_ids"], ["7CAG", "8BMS"])
        self.assertEqual(
            metadata["terminally_blocked_residual_false_hit_pdb_ids"],
            ["7CAG", "8BMS"],
        )
        self.assertEqual(metadata["unresolved_residual_false_hit_count"], 0)
        self.assertEqual(metadata["transporter_false_hit_count"], 2)
        self.assertFalse(metadata["source_free_predictive_feature_materialized"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertTrue(
            all(
                row["terminally_blocked_as_broad_role_false_hit"]
                for row in audit["rows"]
            )
        )
        precount = _load_json(
            ROOT / "artifacts" / "v3_epk_precount_gate_status_1025.json"
        )
        self.assertEqual(
            precount["metadata"][
                "mek_erk_residual_source_adjudication_terminal_pdb_ids"
            ],
            ["7CAG", "8BMS"],
        )
        counteraxis = _load_json(
            ROOT / "artifacts" / "v3_epk_counteraxis_sufficiency_decision_1025.json"
        )
        adjudication_rows = [
            row
            for row in counteraxis["decision_rows"]
            if row["decision_axis"]
            == "mek_erk_residual_false_hit_source_adjudication"
        ]
        self.assertEqual(len(adjudication_rows), 1)
        self.assertEqual(
            adjudication_rows[0]["decision"],
            "source_adjudication_blocks_residual_false_hits_but_not_source_free",
        )

    def test_epk_mek_erk_source_free_topology_ambiguity_artifact_blocks_residuals(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_mek_erk_source_free_topology_ambiguity_counteraxis_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_mek_erk_source_free_topology_ambiguity_counteraxis",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["source_free_counteraxis_status"],
            "passes_bounded_residual_controls_source_free_topology_ambiguity_review_only",
        )
        self.assertEqual(
            metadata["source_reviewed_positive_retained_pdb_ids"],
            ["9UUR", "9UUX"],
        )
        self.assertEqual(metadata["source_reviewed_positive_lost_count"], 0)
        self.assertEqual(
            metadata["residual_false_hit_blocked_pdb_ids"], ["7CAG", "8BMS"]
        )
        self.assertEqual(metadata["residual_false_hit_unblocked_count"], 0)
        self.assertEqual(metadata["missing_local_topology_hit_count"], 0)
        self.assertTrue(metadata["source_free_predictive_feature_materialized"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        rows_by_pdb = {row["pdb_id"]: row for row in audit["rows"]}
        self.assertTrue(rows_by_pdb["7CAG"]["same_chain_companion_hit_detected"])
        self.assertTrue(rows_by_pdb["8BMS"]["reciprocal_cross_chain_hit_detected"])
        precount = _load_json(
            ROOT / "artifacts" / "v3_epk_precount_gate_status_1025.json"
        )
        self.assertEqual(
            precount["metadata"][
                "mek_erk_source_free_topology_residual_blocked_pdb_ids"
            ],
            ["7CAG", "8BMS"],
        )
        counteraxis = _load_json(
            ROOT / "artifacts" / "v3_epk_counteraxis_sufficiency_decision_1025.json"
        )
        topology_rows = [
            row
            for row in counteraxis["decision_rows"]
            if row["decision_axis"]
            == "mek_erk_source_free_topology_ambiguity_counteraxis"
        ]
        self.assertEqual(len(topology_rows), 1)
        self.assertEqual(
            topology_rows[0]["decision"],
            "source_free_topology_ambiguity_blocks_residuals_but_not_calibrated",
        )

    def test_epk_mek_erk_source_free_topology_broader_stress_artifact_fails_closed(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_mek_erk_source_free_topology_broader_stress_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_mek_erk_source_free_topology_broader_stress_audit",
        )
        self.assertEqual(
            metadata["broader_stress_status"],
            "fails_closed_broader_topology_ambiguity_residual_false_hits",
        )
        self.assertEqual(
            metadata["positive_control_retained_pdb_ids"],
            ["1IR3", "5HVK", "6Z3R", "9UUR", "9UUX"],
        )
        self.assertEqual(metadata["positive_control_lost_count"], 0)
        self.assertEqual(
            metadata["false_hit_blocked_pdb_ids"],
            ["7CAG", "7ZDU", "7ZE5", "8BMS"],
        )
        self.assertEqual(
            metadata["residual_false_hit_pdb_ids"],
            ["2JJ2", "4HPU", "7B56", "7ZDT"],
        )
        self.assertTrue(metadata["source_free_predictive_feature_materialized"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_epk_mek_erk_substrate_mode_counteraxis_artifact_stays_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_mek_erk_substrate_mode_counteraxis_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"], "epk_mek_erk_substrate_mode_counteraxis_audit"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["substrate_mode_counteraxis_status"],
            "passes_current_broad_stress_substrate_mode_controls_review_only",
        )
        self.assertEqual(
            metadata["positive_control_retained_pdb_ids"],
            ["1IR3", "5HVK", "6Z3R", "9UUR", "9UUX"],
        )
        self.assertEqual(metadata["positive_control_lost_count"], 0)
        self.assertEqual(
            metadata["false_hit_blocked_by_topology_pdb_ids"],
            ["7CAG", "7ZDU", "7ZE5", "8BMS"],
        )
        self.assertEqual(
            metadata["false_hit_blocked_by_substrate_mode_pdb_ids"],
            ["2JJ2", "4HPU", "7B56", "7ZDT"],
        )
        self.assertEqual(metadata["residual_false_hit_count"], 0)
        self.assertTrue(metadata["source_free_predictive_feature_materialized"])
        self.assertTrue(metadata["substrate_mode_axis_weak_current_stress_only"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        precount = _load_json(
            ROOT / "artifacts" / "v3_epk_precount_gate_status_1025.json"
        )
        self.assertEqual(
            precount["metadata"][
                "mek_erk_substrate_mode_false_hit_blocked_by_substrate_mode_pdb_ids"
            ],
            ["2JJ2", "4HPU", "7B56", "7ZDT"],
        )
        counteraxis = _load_json(
            ROOT / "artifacts" / "v3_epk_counteraxis_sufficiency_decision_1025.json"
        )
        substrate_rows = [
            row
            for row in counteraxis["decision_rows"]
            if row["decision_axis"] == "mek_erk_substrate_mode_counteraxis_audit"
        ]
        self.assertEqual(len(substrate_rows), 1)
        self.assertEqual(
            substrate_rows[0]["decision"],
            "passes_current_stress_but_weak_not_production_admissible",
        )

    def test_epk_mek_erk_substrate_mode_fresh_stress_artifact_stays_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_mek_erk_substrate_mode_fresh_stress_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"], "epk_mek_erk_substrate_mode_fresh_stress_audit"
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["substrate_mode_fresh_stress_status"],
            "passes_fresh_nonrepeat_controls_with_topology_confounding_review_only",
        )
        self.assertEqual(metadata["fresh_nonrepeat_candidate_count"], 3)
        self.assertEqual(
            metadata["fresh_nonrepeat_candidate_pdb_ids"],
            ["7M0T", "7M0W", "9UW4"],
        )
        self.assertEqual(metadata["fresh_nonrepeat_rule_hit_count"], 0)
        self.assertEqual(
            metadata["fresh_nonrepeat_rejected_by_substrate_mode_pdb_ids"],
            ["7M0T", "7M0W", "9UW4"],
        )
        self.assertEqual(
            metadata["fresh_nonrepeat_topology_ambiguous_pdb_ids"],
            ["7M0T", "7M0W", "9UW4"],
        )
        self.assertEqual(
            metadata["repeat_current_surface_rule_hit_pdb_ids"],
            ["9UUR", "9UUX"],
        )
        self.assertTrue(metadata["fresh_stress_topology_confounded"])
        self.assertTrue(metadata["source_free_predictive_feature_materialized"])
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        precount = _load_json(
            ROOT / "artifacts" / "v3_epk_precount_gate_status_1025.json"
        )
        self.assertEqual(
            precount["metadata"][
                "mek_erk_substrate_mode_fresh_nonrepeat_rejected_pdb_ids"
            ],
            ["7M0T", "7M0W", "9UW4"],
        )
        counteraxis = _load_json(
            ROOT / "artifacts" / "v3_epk_counteraxis_sufficiency_decision_1025.json"
        )
        fresh_rows = [
            row
            for row in counteraxis["decision_rows"]
            if row["decision_axis"]
            == "mek_erk_substrate_mode_fresh_stress_audit"
        ]
        self.assertEqual(len(fresh_rows), 1)
        self.assertEqual(
            fresh_rows[0]["decision"],
            (
                "passes_fresh_nonrepeat_controls_but_topology_confounded_not_production_admissible"
            ),
        )

    def test_epk_mek_erk_substrate_mode_existing_scout_gap_artifact_stays_review_only(
        self,
    ) -> None:
        audit = _load_json(
            ROOT
            / "artifacts"
            / "v3_epk_mek_erk_substrate_mode_existing_scout_gap_audit_1025.json"
        )
        metadata = audit["metadata"]
        self.assertEqual(
            metadata["method"],
            "epk_mek_erk_substrate_mode_existing_scout_gap_audit",
        )
        self.assertTrue(metadata["review_only"])
        self.assertEqual(
            metadata["existing_scout_gap_status"],
            "blocked_existing_scouts_only_topology_confounded_candidates_review_only",
        )
        self.assertEqual(metadata["non_topology_confounded_candidate_count"], 0)
        self.assertEqual(
            metadata["topology_confounded_candidate_pdb_ids"],
            [
                "1TFW",
                "2DRA",
                "2Q66",
                "2ZH6",
                "7T55",
                "7T56",
                "7T57",
                "9BJI",
                "9L3M",
                "9L3U",
            ],
        )
        self.assertFalse(metadata["ready_to_run_epk_scorer"])
        self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
        self.assertFalse(metadata["fingerprint_registry_edited"])
        self.assertFalse(metadata["curated_label_registry_edited"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        precount = _load_json(
            ROOT / "artifacts" / "v3_epk_precount_gate_status_1025.json"
        )
        self.assertEqual(
            precount["metadata"][
                "mek_erk_substrate_mode_existing_scout_non_topology_count"
            ],
            0,
        )
        counteraxis = _load_json(
            ROOT / "artifacts" / "v3_epk_counteraxis_sufficiency_decision_1025.json"
        )
        gap_rows = [
            row
            for row in counteraxis["decision_rows"]
            if row["decision_axis"]
            == "mek_erk_substrate_mode_existing_scout_gap_audit"
        ]
        self.assertEqual(len(gap_rows), 1)
        self.assertEqual(
            gap_rows[0]["decision"],
            "existing_scouts_do_not_supply_clean_next_tranche",
        )

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
