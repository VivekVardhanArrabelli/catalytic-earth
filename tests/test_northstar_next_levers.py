from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.northstar_next_levers import (
    _predicted_model_parts,
    build_family_panel_evidence_packet,
    build_fold_augmented_abstention_gate,
    build_fold_augmented_family_panel_m_csa_primary_channel_repair,
    build_fold_augmented_family_panel_missing_primary_channel_diagnosis,
    build_fold_augmented_family_panel_missing_primary_channel_queue,
    build_fold_augmented_family_panel_research_readout,
    build_fold_augmented_family_panel_source_check_queue,
    build_fold_augmented_oos_calibrated_threshold_contract,
    build_fold_augmented_abstention_threshold_contract,
    build_fold_augmented_train_cal_oos_negative_surface_blocker_resolution,
    build_fold_augmented_train_cal_oos_negative_surface_scores,
    build_fold_augmented_train_cal_oos_negative_surface_sufficiency_decision,
    build_fold_only_train_cal_oos_negative_surface,
    build_family_panel_source_free_predicted_geometry_retrieval,
    build_family_panel_source_free_predicted_geometry_source_check_preflight,
    build_learned_mechanism_feature_embedding_plan,
    build_mechanism_feature_active_site_role_graph_sidecar,
    build_mechanism_feature_reaction_center_template_sidecar,
    build_mechanism_feature_sidecar_schema_audit,
    build_predicted_atlas_geometry_novelty_variants,
    build_predicted_structure_fold_augmented_novelty_operating_grid,
    build_predicted_structure_fold_channel,
    build_predicted_structure_fold_channel_contract_audit,
    build_selected_organic_cofactor_sidecar_schema_audit,
    write_family_panel_source_free_active_site_locator_candidate_audit,
    write_family_panel_source_free_active_site_locator_candidate_integrity_audit,
    write_family_panel_source_free_active_site_locator_manual_review_packet,
    write_family_panel_source_free_active_site_locator_review_queue,
    write_family_panel_source_backed_sidecar_materialization,
    write_mechanism_feature_embedding_feature_contract,
)
from catalytic_earth.predicted_geometry_robustness import _target_manifest_row_selection


MINI_AF_CIF = """data_AF-TEST-F1
#
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_alt_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_entity_id
_atom_site.label_seq_id
_atom_site.pdbx_PDB_ins_code
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.occupancy
_atom_site.B_iso_or_equiv
_atom_site.pdbx_formal_charge
_atom_site.auth_seq_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_atom_id
_atom_site.pdbx_PDB_model_num
ATOM 1 N N . ASP A 1 10 ? 0.0 0.0 0.0 1.00 90.0 ? 10 ASP A N 1
ATOM 2 C CA . ASP A 1 10 ? 1.0 0.0 0.0 1.00 90.0 ? 10 ASP A CA 1
ATOM 3 N N . HIS A 1 30 ? 4.0 0.0 0.0 1.00 90.0 ? 30 HIS A N 1
ATOM 4 C CA . HIS A 1 30 ? 5.0 0.0 0.0 1.00 90.0 ? 30 HIS A CA 1
#
"""

MINI_LOCATOR_CIF = """data_TEST
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
1 1 TEST A 1 ? 100 ? PTEST 1 ? 100 ? 1 100
#
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_alt_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_entity_id
_atom_site.label_seq_id
_atom_site.pdbx_PDB_ins_code
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.occupancy
_atom_site.B_iso_or_equiv
_atom_site.pdbx_formal_charge
_atom_site.auth_seq_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_atom_id
_atom_site.pdbx_PDB_model_num
ATOM 1 O OD1 . ASP A 1 10 ? 0.0 0.0 0.0 1.00 90.0 ? 10 ASP A OD1 1
ATOM 2 C CA . ASP A 1 10 ? 0.2 0.0 0.0 1.00 90.0 ? 10 ASP A CA 1
ATOM 3 N NE2 . HIS A 1 30 ? 1.0 0.0 0.0 1.00 90.0 ? 30 HIS A NE2 1
ATOM 4 C CA . HIS A 1 30 ? 1.2 0.0 0.0 1.00 90.0 ? 30 HIS A CA 1
HETATM 5 ZN ZN . ZN B 2 . ? 0.5 0.0 0.0 1.00 40.0 ? 1 ZN B ZN 1
#
"""


class NorthstarNextLeversTests(unittest.TestCase):
    def test_source_free_locator_candidate_audit_stages_non_scoring_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            cif = root / "pdb_TEST.cif"
            source_backed_sidecar = root / "source_backed.json"
            manifest = root / "manifest.json"
            schema = root / "schema.json"
            out = root / "candidate_audit.json"
            report = root / "candidate_audit.md"
            candidate_dir = root / "candidates"
            cif.write_text(MINI_LOCATOR_CIF, encoding="utf-8")
            source_backed_sidecar.write_text(
                json.dumps(
                    {
                        "coordinate_records": [
                            {
                                "coordinate_role": "selected_pdb_cif",
                                "exists": True,
                                "path": str(cif),
                                "sha256": hashlib.sha256(cif.read_bytes()).hexdigest(),
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            manifest.write_text(
                json.dumps(
                    {
                        "row_manifests": [
                            {
                                "rank": 1,
                                "entry_id": "mh_test",
                                "panel_id": "review_panel",
                                "source_accession": "uniprot:PTEST",
                                "selected_structure_id": "TEST",
                                "same_accession_current702_geometry_rows": [],
                                "source_backed_sidecar": {
                                    "exists": True,
                                    "path": str(source_backed_sidecar),
                                },
                                "alphafolddb_predicted_cif": {
                                    "exists": True,
                                    "path": str(root / "AF-PTEST-F1-model_v6.cif"),
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            schema.write_text(
                json.dumps(
                    {
                        "counts": {"required_residue_locator_minimum": 2},
                        "forbidden_predictive_fields": [
                            "entry_name",
                            "source_prose",
                            "label_type",
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = write_family_panel_source_free_active_site_locator_candidate_audit(
                source_free_geometry_manifest_path=manifest,
                locator_schema_path=schema,
                candidate_dir=candidate_dir,
                out_path=out,
                report_path=report,
            )
            row = audit["row_audits"][0]
            candidate_path_exists = Path(row["candidate_path"]).exists()
            candidate = json.loads(
                Path(row["candidate_path"]).read_text(encoding="utf-8")
            )

        self.assertEqual(
            audit["status"],
            "source_free_active_site_locator_candidates_staged_review_only",
        )
        self.assertEqual(audit["counts"]["candidate_sidecars_staged"], 1)
        self.assertEqual(audit["counts"]["rows_with_minimum_candidate_residue_locators"], 1)
        self.assertEqual(audit["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertEqual(row["selected_ligand_site"]["comp_id"], "ZN")
        self.assertEqual(row["candidate_residue_locator_count"], 2)
        self.assertEqual(row["sequence_position_validated_locator_count"], 2)
        self.assertTrue(candidate_path_exists)
        self.assertFalse(candidate["ready_for_predicted_geometry_scoring"])
        self.assertEqual(
            [locator["sequence_position"] for locator in candidate["residue_locators"]],
            [10, 30],
        )
        self.assertTrue(
            candidate["residue_locators"][0]["coordinate_independent_provenance"][
                "sequence_position_uniprot_validated"
            ]
        )
        self.assertFalse(candidate["forbidden_feature_audit"]["source_prose"])

    def test_source_free_locator_candidate_integrity_audit_passes_staged_sidecar(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            cif = root / "pdb_TEST.cif"
            source_backed_sidecar = root / "source_backed.json"
            manifest = root / "manifest.json"
            schema = root / "schema.json"
            candidate_audit_path = root / "candidate_audit.json"
            candidate_dir = root / "candidates"
            audited_locator_dir = root / "audited_locators"
            out = root / "candidate_integrity.json"
            cif.write_text(MINI_LOCATOR_CIF, encoding="utf-8")
            source_backed_sidecar.write_text(
                json.dumps(
                    {
                        "coordinate_records": [
                            {
                                "coordinate_role": "selected_pdb_cif",
                                "exists": True,
                                "path": str(cif),
                                "sha256": hashlib.sha256(cif.read_bytes()).hexdigest(),
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            manifest.write_text(
                json.dumps(
                    {
                        "row_manifests": [
                            {
                                "rank": 1,
                                "entry_id": "mh_test",
                                "panel_id": "review_panel",
                                "source_accession": "uniprot:PTEST",
                                "selected_structure_id": "TEST",
                                "same_accession_current702_geometry_rows": [],
                                "source_backed_sidecar": {
                                    "exists": True,
                                    "path": str(source_backed_sidecar),
                                },
                                "alphafolddb_predicted_cif": {
                                    "exists": True,
                                    "path": str(root / "AF-PTEST-F1-model_v6.cif"),
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            schema.write_text(
                json.dumps(
                    {
                        "counts": {"required_residue_locator_minimum": 2},
                        "forbidden_predictive_fields": [
                            "entry_name",
                            "source_prose",
                            "label_type",
                        ],
                    }
                ),
                encoding="utf-8",
            )
            write_family_panel_source_free_active_site_locator_candidate_audit(
                source_free_geometry_manifest_path=manifest,
                locator_schema_path=schema,
                candidate_dir=candidate_dir,
                out_path=candidate_audit_path,
            )

            audit = write_family_panel_source_free_active_site_locator_candidate_integrity_audit(
                candidate_audit_path=candidate_audit_path,
                candidate_dir=candidate_dir,
                audited_locator_dir=audited_locator_dir,
                out_path=out,
            )

        self.assertEqual(
            audit["status"],
            "source_free_active_site_locator_candidate_integrity_passed_review_only",
        )
        self.assertEqual(audit["counts"]["candidate_sidecars_expected"], 1)
        self.assertEqual(audit["counts"]["candidate_sidecar_files_present"], 1)
        self.assertEqual(audit["counts"]["integrity_passed_sidecars"], 1)
        self.assertEqual(audit["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertEqual(audit["counts"]["critical_counts"], {})
        self.assertTrue(audit["row_audits"][0]["payload_matches_candidate_audit"])
        self.assertFalse(audit["row_audits"][0]["inside_audited_locator_dir"])

    def test_source_free_predicted_geometry_retrieval_scores_approved_locator(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            af_cif = root / "AF-PTEST-F1-model_v6.cif"
            manifest = root / "manifest.json"
            materialization = root / "materialization.json"
            schema_audit = root / "schema_audit.json"
            threshold_contract = root / "threshold.json"
            locator_dir = root / "locators"
            locator_dir.mkdir()
            locator_sidecar = locator_dir / "mh_test_PTEST.json"
            af_cif.write_text(MINI_AF_CIF, encoding="utf-8")
            manifest.write_text(
                json.dumps(
                    {
                        "row_manifests": [
                            {
                                "rank": 1,
                                "entry_id": "mh_test",
                                "panel_id": "review_panel",
                                "source_accession": "uniprot:PTEST",
                                "source_free_predicted_geometry_status": (
                                    "ready_to_score_source_free_predicted_geometry"
                                ),
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            materialization.write_text(
                json.dumps(
                    {
                        "row_scores": [
                            {
                                "entry_id": "mh_test",
                                "source_accession": "uniprot:PTEST",
                                "selected_structure_id": "TEST",
                                "coordinate_records": [
                                    {
                                        "coordinate_role": "alphafolddb_predicted_cif",
                                        "exists": True,
                                        "path": str(af_cif),
                                        "sha256": hashlib.sha256(
                                            af_cif.read_bytes()
                                        ).hexdigest(),
                                        "size_bytes": af_cif.stat().st_size,
                                    }
                                ],
                                "predicted_structure_fold_channel": {
                                    "nearest_atlas_entry_id": "m_csa:1",
                                    "nearest_atlas_tm_score": 0.7,
                                    "nearest_atlas_true_fingerprint_id": (
                                        "metal_dependent_hydrolase"
                                    ),
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            schema_audit.write_text(
                json.dumps(
                    {
                        "row_audits": [
                            {
                                "entry_id": "mh_test",
                                "ready_for_predicted_geometry_scoring": True,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            threshold_contract.write_text(
                json.dumps(
                    {
                        "threshold_contract": {
                            "combined_mean_geometry_fold": {
                                "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain": {
                                    "threshold": 0.1
                                }
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            locator_sidecar.write_text(
                json.dumps(
                    {
                        "entry_id": "mh_test",
                        "source_accession": "uniprot:PTEST",
                        "locator_evidence_class": (
                            "structure_local_ligand_geometry_without_source_text"
                        ),
                        "locator_policy": "human_approved",
                        "ready_for_predicted_geometry_scoring": True,
                        "manual_review_approval": {
                            "approval_scope": "source_free_active_site_locator_only"
                        },
                        "residue_locators": [
                            {
                                "sequence_position": 10,
                                "residue_code": "ASP",
                                "role_hint": "metal_ligand_contact_candidate",
                                "locator_evidence_class": (
                                    "structure_local_ligand_geometry_without_source_text"
                                ),
                                "locator_confidence": 0.25,
                            },
                            {
                                "sequence_position": 30,
                                "residue_code": "HIS",
                                "role_hint": "metal_ligand_contact_candidate",
                                "locator_evidence_class": (
                                    "structure_local_ligand_geometry_without_source_text"
                                ),
                                "locator_confidence": 0.25,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_family_panel_source_free_predicted_geometry_retrieval(
                source_free_geometry_manifest_path=manifest,
                source_backed_materialization_path=materialization,
                locator_schema_audit_path=schema_audit,
                locator_dir=locator_dir,
                threshold_contract_path=threshold_contract,
            )

        self.assertEqual(
            audit["status"],
            "source_free_predicted_geometry_retrieval_scored_review_only",
        )
        self.assertEqual(audit["counts"]["predicted_geometry_ok_rows"], 1)
        self.assertEqual(audit["counts"]["retained_at_fixed_research_threshold"], 1)
        self.assertFalse(audit["guardrails"]["source_text_used_for_score"])
        row = audit["row_scores"][0]
        self.assertEqual(row["predicted_geometry_status"], "ok")
        self.assertEqual(row["resolved_residue_count"], 2)
        self.assertIsNotNone(
            row["predicted_geometry_retrieval"]["top1_fingerprint_id"]
        )
        self.assertIsNotNone(
            row["fold_augmented_projection"]["combined_mean_geometry_fold"]
        )
        self.assertTrue(
            row["fold_augmented_projection"][
                "retained_at_fixed_research_threshold"
            ]
        )
        feature_entry = audit["predicted_geometry_features"]["entries"][0]
        self.assertFalse(feature_entry["coordinate_swap"]["source_text_used"])
        self.assertEqual(feature_entry["mechanism_text_snippets"], [])

    def test_source_free_predicted_geometry_source_check_preflight_holds_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            queue = root / "queue.json"
            retrieval = root / "retrieval.json"
            materialization = root / "materialization.json"
            source_sidecar = root / "source_sidecar.json"
            external_panel = root / "external_panel.json"
            queue.write_text(
                json.dumps(
                    {
                        "queue_rows": [
                            {
                                "rank": 1,
                                "entry_id": "mh_test",
                                "panel_id": "review_panel",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            retrieval.write_text(
                json.dumps(
                    {
                        "row_scores": [
                            {
                                "entry_id": "mh_test",
                                "panel_id": "review_panel",
                                "source_accession": "uniprot:PTEST",
                                "predicted_geometry_retrieval": {
                                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                                    "top1_score": 0.5,
                                },
                                "predicted_structure_fold_channel": {
                                    "nearest_atlas_true_fingerprint_id": (
                                        "metal_dependent_hydrolase"
                                    ),
                                    "nearest_atlas_tm_score": 0.8,
                                },
                                "fold_augmented_projection": {
                                    "combined_mean_geometry_fold": 0.65,
                                    "fixed_research_threshold": 0.44155,
                                    "retained_at_fixed_research_threshold": True,
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            source_sidecar.write_text(
                json.dumps(
                    {
                        "display_name": "Test hydrolase",
                        "predictive_use_allowed": False,
                        "catalytic_or_binding_site_evidence": {
                            "status": "source_backed_review_context_only"
                        },
                        "source_urls": {"uniprot": "https://example.test/PTEST"},
                    }
                ),
                encoding="utf-8",
            )
            materialization.write_text(
                json.dumps(
                    {
                        "row_scores": [
                            {
                                "entry_id": "mh_test",
                                "source_accession": "uniprot:PTEST",
                                "sidecar_path": str(source_sidecar),
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            external_panel.write_text(
                json.dumps(
                    {
                        "candidate_rows": [
                            {
                                "row_id": "mh_test",
                                "accession": "uniprot:PTEST",
                                "name": "External test hydrolase",
                                "candidate_role": "external_positive_lead",
                                "current_v1_state": "external_no_decision_review_only",
                                "countable_label_candidate": False,
                                "evidence_summary": "frozen local evidence",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_family_panel_source_free_predicted_geometry_source_check_preflight(
                source_check_queue_path=queue,
                source_free_predicted_geometry_retrieval_path=retrieval,
                source_backed_materialization_path=materialization,
                external_metal_hydrolase_panel_path=external_panel,
            )

        self.assertEqual(
            audit["status"],
            "source_free_predicted_geometry_source_check_preflight_ready_review_only",
        )
        self.assertEqual(audit["counts"]["preflight_rows"], 1)
        self.assertEqual(audit["counts"]["geometry_fold_agreement_rows"], 1)
        row = audit["preflight_rows"][0]
        self.assertEqual(
            row["preflight_decision"],
            "hold_review_only_pending_source_check",
        )
        self.assertIn("label_import_not_authorized", row["risk_flags"])
        self.assertIn("external_panel_row_not_countable", row["risk_flags"])
        self.assertTrue(audit["guardrails"]["review_only"])
        self.assertFalse(audit["guardrails"]["new_source_data_fetched"])

    def test_source_free_locator_manual_review_packet_combines_review_inputs(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            candidate_audit = root / "candidate_audit.json"
            candidate_integrity = root / "candidate_integrity.json"
            review_queue = root / "review_queue.json"
            out = root / "manual_review_packet.json"
            candidate_audit.write_text(
                json.dumps(
                    {
                        "row_audits": [
                            {
                                "entry_id": "ready",
                                "source_accession": "uniprot:P1",
                                "candidate_path": "ready.json",
                                "status": "candidate_locators_staged_review_only",
                                "candidate_residue_locator_count": 2,
                                "sequence_position_validated_locator_count": 2,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            candidate_integrity.write_text(
                json.dumps(
                    {
                        "row_audits": [
                            {
                                "entry_id": "ready",
                                "source_accession": "uniprot:P1",
                                "candidate_path": "ready.json",
                                "sha256": "abc123",
                                "status": "passed",
                                "critical_violations": [],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            review_queue.write_text(
                json.dumps(
                    {
                        "queue_rows": [
                            {
                                "priority": 1,
                                "entry_id": "ready",
                                "source_accession": "uniprot:P1",
                                "candidate_path": "ready.json",
                                "review_class": "ready_for_manual_forbidden_feature_review",
                                "candidate_residue_locator_count": 2,
                                "sequence_position_validated_locator_count": 2,
                                "candidate_blockers": [],
                                "next_action": "review row",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            packet = write_family_panel_source_free_active_site_locator_manual_review_packet(
                candidate_audit_path=candidate_audit,
                candidate_integrity_audit_path=candidate_integrity,
                review_queue_path=review_queue,
                out_path=out,
            )

        self.assertEqual(
            packet["status"],
            "source_free_active_site_locator_manual_review_packet_ready_review_only",
        )
        self.assertEqual(packet["counts"]["review_rows"], 1)
        self.assertEqual(packet["counts"]["integrity_passed_rows"], 1)
        self.assertEqual(
            packet["counts"]["priority_1_manual_forbidden_feature_review_rows"],
            1,
        )
        self.assertEqual(packet["counts"]["ready_for_predicted_geometry_scoring"], 0)
        self.assertEqual(packet["review_rows"][0]["candidate_sha256"], "abc123")
        self.assertFalse(
            packet["review_rows"][0]["copy_to_audited_locator_dir_allowed_now"]
        )

    def test_source_free_locator_review_queue_ranks_manual_review_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            candidate_audit = root / "candidate_audit.json"
            out = root / "queue.json"
            candidate_audit.write_text(
                json.dumps(
                    {
                        "row_audits": [
                            {
                                "entry_id": "ready",
                                "source_accession": "uniprot:P1",
                                "candidate_path": "ready.json",
                                "candidate_residue_locator_count": 2,
                                "sequence_position_validated_locator_count": 2,
                                "candidate_blockers": [
                                    "candidate_sidecar_not_in_audited_locator_dir",
                                    "manual_review_required_before_copy_to_audited_dir",
                                ],
                            },
                            {
                                "entry_id": "blocked",
                                "source_accession": "uniprot:P2",
                                "candidate_path": "blocked.json",
                                "candidate_residue_locator_count": 0,
                                "sequence_position_validated_locator_count": 0,
                                "candidate_blockers": [
                                    "insufficient_candidate_residue_locators",
                                ],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            queue = write_family_panel_source_free_active_site_locator_review_queue(
                candidate_audit_path=candidate_audit,
                out_path=out,
            )

        self.assertEqual(
            queue["status"],
            "source_free_active_site_locator_review_queue_ready_review_only",
        )
        self.assertEqual(
            queue["counts"]["ready_for_manual_forbidden_feature_review"],
            1,
        )
        self.assertEqual(queue["queue_rows"][0]["entry_id"], "ready")
        self.assertEqual(
            queue["queue_rows"][0]["review_class"],
            "ready_for_manual_forbidden_feature_review",
        )
        self.assertEqual(queue["queue_rows"][-1]["priority"], 5)

    def test_fold_augmented_gate_combines_fold_geometry_and_cofactor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            fold = root / "fold.json"
            geom = root / "geom.json"
            cof = root / "cof.json"
            fold.write_text(
                json.dumps(
                    {
                        "fold_channel_signal": {
                            "nearest_atlas_tm_score": {
                                "row_scores": [
                                    {
                                        "entry_id": "m_csa:1",
                                        "true_fingerprint_id": "metal_dependent_hydrolase",
                                        "is_confounded_predicted_geometry_oos": False,
                                        "fold_signals": {"nearest_atlas_tm_score": 0.8},
                                    },
                                    {
                                        "entry_id": "m_csa:30",
                                        "true_fingerprint_id": None,
                                        "is_confounded_predicted_geometry_oos": True,
                                        "fold_signals": {"nearest_atlas_tm_score": 0.2},
                                    },
                                ]
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            geom.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "entry_id": "m_csa:1",
                                "top_fingerprints": [{"score": 0.9}],
                            },
                            {
                                "entry_id": "m_csa:30",
                                "top_fingerprints": [{"score": 0.3}],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            cof.write_text(
                json.dumps(
                    {
                        "row_class_records": [
                            {"entry_id": "m_csa:1", "class": "flavin", "selected_score": 0.2},
                            {"entry_id": "m_csa:1", "class": "heme", "selected_score": 0.1},
                            {"entry_id": "m_csa:1", "class": "plp", "selected_score": 0.1},
                            {"entry_id": "m_csa:30", "class": "flavin", "selected_score": 0.8},
                            {"entry_id": "m_csa:30", "class": "heme", "selected_score": 0.1},
                            {"entry_id": "m_csa:30", "class": "plp", "selected_score": 0.1},
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_augmented_abstention_gate(
                predicted_structure_fold_channel_path=fold,
                predicted_geometry_atlas_path=geom,
                selected_organic_cofactor_sidecar_path=cof,
            )

        self.assertEqual(audit["status"], "computed_no_fit_no_threshold_change")
        self.assertEqual(audit["counts"]["heldout_rows_scored"], 2)
        self.assertEqual(
            audit["channels"]["combined_mean_geometry_fold"]["auc_in_gt_oos_all"],
            1.0,
        )

    def test_fold_augmented_threshold_contract_uses_calibration_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            fold_gate = root / "fold_gate.json"
            fold_channel = root / "fold_channel.json"
            predicted_atlas = root / "predicted_atlas.json"
            sidecar = root / "cofactor.json"
            train_cal_tsv = root / "train_cal.tsv"
            fold_gate.write_text(
                json.dumps(
                    {
                        "row_scores": [
                            {
                                "entry_id": "m_csa:101",
                                "is_inscope": True,
                                "is_oos": False,
                                "is_confounded_predicted_geometry_oos": False,
                                "channel_scores": {
                                    "geometry_top1_score": 0.8,
                                    "cofactor_max_score": 0.1,
                                    "fold_nearest_atlas_tm_score": 0.8,
                                    "combined_mean_geometry_cofactor_fold": 0.566667,
                                    "combined_mean_geometry_fold": 0.8,
                                    "combined_min_geometry_fold": 0.8,
                                },
                            },
                            {
                                "entry_id": "m_csa:102",
                                "is_inscope": False,
                                "is_oos": True,
                                "is_confounded_predicted_geometry_oos": True,
                                "channel_scores": {
                                    "geometry_top1_score": 0.2,
                                    "cofactor_max_score": 0.9,
                                    "fold_nearest_atlas_tm_score": 0.2,
                                    "combined_mean_geometry_cofactor_fold": 0.433333,
                                    "combined_mean_geometry_fold": 0.2,
                                    "combined_min_geometry_fold": 0.2,
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            fold_channel.write_text(
                json.dumps(
                    {
                        "foldseek_input_manifest": {
                            "coordinate_root": str(root / "coords"),
                            "atlas_database_dir": str(root / "coords" / "atlas_in_distribution"),
                        }
                    }
                ),
                encoding="utf-8",
            )
            predicted_atlas.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "split_assignment": "in_distribution",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P11111-F1-model_v6",
                                "true_fingerprint_id": "metal_dependent_hydrolase",
                                "top_fingerprints": [{"score": 0.8}],
                            },
                            {
                                "entry_id": "m_csa:2",
                                "accession": "P22222",
                                "split_assignment": "in_distribution",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P22222-F1-model_v6",
                                "true_fingerprint_id": "metal_dependent_hydrolase",
                                "top_fingerprints": [{"score": 0.7}],
                            },
                            {
                                "entry_id": "m_csa:3",
                                "accession": "P33333",
                                "split_assignment": "in_distribution",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P33333-F1-model_v6",
                                "true_fingerprint_id": "ser_his_acid_hydrolase",
                                "top_fingerprints": [{"score": 0.6}],
                            },
                            {
                                "entry_id": "m_csa:4",
                                "accession": "P44444",
                                "split_assignment": "in_distribution",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P44444-F1-model_v6",
                                "true_fingerprint_id": "ser_his_acid_hydrolase",
                                "top_fingerprints": [{"score": 0.5}],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            sidecar.write_text(
                json.dumps(
                    {
                        "row_class_records": [
                            {
                                "entry_id": entry_id,
                                "class": cls,
                                "selected_score": score,
                            }
                            for entry_id, score in [
                                ("m_csa:1", 0.1),
                                ("m_csa:2", 0.2),
                                ("m_csa:3", 0.3),
                                ("m_csa:4", 0.4),
                            ]
                            for cls in ("flavin", "heme", "plp")
                        ]
                    }
                ),
                encoding="utf-8",
            )
            train_cal_tsv.write_text(
                "\n".join(
                    [
                        "afdb_P11111_v6\tafdb_P22222_v6\t0.1\t0.2\t0.9\t0.8\t40",
                        "afdb_P22222_v6\tafdb_P11111_v6\t0.1\t0.2\t0.7\t0.8\t40",
                        "afdb_P33333_v6\tafdb_P44444_v6\t0.1\t0.2\t0.6\t0.8\t40",
                        "afdb_P44444_v6\tafdb_P33333_v6\t0.1\t0.2\t0.5\t0.8\t40",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            audit = build_fold_augmented_abstention_threshold_contract(
                fold_augmented_gate_path=fold_gate,
                predicted_structure_fold_channel_path=fold_channel,
                predicted_geometry_atlas_path=predicted_atlas,
                selected_organic_cofactor_sidecar_path=sidecar,
                train_cal_foldseek_tsv=train_cal_tsv,
                foldseek_binary=str(root / "missing-foldseek"),
            )

        self.assertEqual(audit["status"], "computed_train_cal_threshold_contract")
        self.assertTrue(audit["guardrails"]["heldout_used_for_final_eval_only"])
        self.assertGreater(audit["counts"]["calibration_rows_scored"], 0)
        primary = audit["primary_channel_readout"]
        self.assertIsNotNone(
            primary["selected_at_90pct_calibration_in_scope_retention"]
        )
        self.assertEqual(
            primary["heldout_final_eval_at_90pct_threshold"][
                "heldout_confounded_oos_abstain_recall"
            ],
            1.0,
        )

    def test_fold_augmented_threshold_contract_blocks_without_train_cal_tsv(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            fold_gate = root / "fold_gate.json"
            fold_channel = root / "fold_channel.json"
            predicted_atlas = root / "predicted_atlas.json"
            sidecar = root / "cofactor.json"
            fold_gate.write_text(
                json.dumps(
                    {
                        "row_scores": [
                            {
                                "entry_id": "m_csa:101",
                                "is_inscope": True,
                                "is_oos": False,
                                "is_confounded_predicted_geometry_oos": False,
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.8,
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            fold_channel.write_text(
                json.dumps(
                    {
                        "foldseek_input_manifest": {
                            "coordinate_root": str(root / "coords"),
                            "atlas_database_dir": str(root / "coords" / "atlas_in_distribution"),
                        }
                    }
                ),
                encoding="utf-8",
            )
            predicted_atlas.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "split_assignment": "in_distribution",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P11111-F1-model_v6",
                                "true_fingerprint_id": "metal_dependent_hydrolase",
                                "top_fingerprints": [{"score": 0.8}],
                            },
                            {
                                "entry_id": "m_csa:2",
                                "accession": "P22222",
                                "split_assignment": "in_distribution",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P22222-F1-model_v6",
                                "true_fingerprint_id": "metal_dependent_hydrolase",
                                "top_fingerprints": [{"score": 0.7}],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            sidecar.write_text(
                json.dumps(
                    {
                        "row_class_records": [
                            {"entry_id": "m_csa:1", "class": "flavin", "selected_score": 0.1},
                            {"entry_id": "m_csa:1", "class": "heme", "selected_score": 0.1},
                            {"entry_id": "m_csa:1", "class": "plp", "selected_score": 0.1},
                            {"entry_id": "m_csa:2", "class": "flavin", "selected_score": 0.1},
                            {"entry_id": "m_csa:2", "class": "heme", "selected_score": 0.1},
                            {"entry_id": "m_csa:2", "class": "plp", "selected_score": 0.1},
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_augmented_abstention_threshold_contract(
                fold_augmented_gate_path=fold_gate,
                predicted_structure_fold_channel_path=fold_channel,
                predicted_geometry_atlas_path=predicted_atlas,
                selected_organic_cofactor_sidecar_path=sidecar,
                train_cal_foldseek_tsv=root / "missing.tsv",
            )

        self.assertEqual(audit["status"], "blocked_missing_train_cal_fold_scores")
        self.assertIn("train_cal_foldseek_tsv_missing_or_unparsed", audit["blockers"])
        self.assertIsNone(
            audit["primary_channel_readout"][
                "selected_at_90pct_calibration_in_scope_retention"
            ]
        )

    def test_train_cal_oos_negative_surface_stages_missing_scores(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest = root / "negative_surface.json"
            labels = root / "labels.json"
            graph = root / "graph.json"
            geometry = root / "geometry.json"
            contract = root / "contract.json"
            predicted_atlas = root / "predicted_atlas.json"
            sidecar = root / "cofactor.json"
            manifest.write_text(
                json.dumps(
                    {
                        "candidate_entry_ids": {
                            "calibration_oos_candidates_hash20pct": ["uniprot:P12345"]
                        },
                        "selection_policy": {
                            "calibration_negative_selector": "test selector",
                            "candidate_definition": "split_assignment == in_distribution and no fingerprint",
                            "train_target_policy": "test train targets",
                        },
                    }
                ),
                encoding="utf-8",
            )
            labels.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "uniprot:P12345",
                                "accession": "P12345",
                                "sequence_id": "P12345",
                                "split_assignment": "in_distribution",
                                "benchmark_role": "oos_tier::unknown_oos",
                                "label_type": "out_of_scope",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(json.dumps({"nodes": []}), encoding="utf-8")
            geometry.write_text(json.dumps({"entries": []}), encoding="utf-8")
            contract.write_text(
                json.dumps({"train_cal_partition": {"train_entry_ids": ["m_csa:1"]}}),
                encoding="utf-8",
            )
            predicted_atlas.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "Q11111",
                                "split_assignment": "in_distribution",
                                "true_fingerprint_id": "metal_dependent_hydrolase",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-Q11111-F1-model_v6",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            sidecar.write_text(
                json.dumps(
                    {
                        "row_class_records": [
                            {
                                "entry_id": "uniprot:P12345",
                                "class": "flavin",
                                "selected_score": 0.1,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_augmented_train_cal_oos_negative_surface_scores(
                negative_surface_manifest_path=manifest,
                label_manifest_path=labels,
                graph_path=graph,
                experimental_geometry_features_path=geometry,
                threshold_contract_path=contract,
                predicted_geometry_atlas_path=predicted_atlas,
                selected_organic_cofactor_sidecar_path=sidecar,
                coordinate_root=root / "coords",
                train_cal_oos_foldseek_tsv=root / "missing.tsv",
                out_path=root / "scores.json",
            )

        self.assertEqual(
            audit["status"],
            "manifest_staged_train_cal_oos_negative_surface_scoring",
        )
        self.assertTrue(audit["guardrails"]["frozen_current702_inputs_only"])
        self.assertEqual(audit["counts"]["candidate_ids_requested"], 1)
        self.assertEqual(audit["counts"]["candidate_geometry_target_rows"], 0)
        self.assertIn(
            "train_cal_oos_foldseek_tsv_missing_or_unparsed",
            audit["blockers"],
        )

    def test_oos_calibrated_threshold_contract_uses_negative_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            threshold_contract = root / "threshold_contract.json"
            oos_surface = root / "oos_surface.json"
            fold_gate = root / "fold_gate.json"
            threshold_contract.write_text(
                json.dumps(
                    {
                        "threshold_contract": {
                            "combined_mean_geometry_fold": {
                                "selected_at_90pct_calibration_in_scope_retention": {
                                    "threshold": 0.5
                                }
                            }
                        },
                        "calibration_row_scores": [
                            {
                                "entry_id": "m_csa:1",
                                "channel_scores": {"combined_mean_geometry_fold": 0.8},
                            },
                            {
                                "entry_id": "m_csa:2",
                                "channel_scores": {"combined_mean_geometry_fold": 0.6},
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            oos_surface.write_text(
                json.dumps(
                    {
                        "status": "computed_train_cal_oos_negative_surface_scores",
                        "counts": {"candidate_ids_requested": 2},
                        "candidate_row_scores": [
                            {
                                "entry_id": "m_csa:3",
                                "channel_scores": {"combined_mean_geometry_fold": 0.4},
                            },
                            {
                                "entry_id": "m_csa:4",
                                "channel_scores": {"combined_mean_geometry_fold": 0.7},
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            fold_gate.write_text(
                json.dumps(
                    {
                        "row_scores": [
                            {
                                "entry_id": "m_csa:10",
                                "is_inscope": True,
                                "is_oos": False,
                                "is_confounded_predicted_geometry_oos": False,
                                "channel_scores": {"combined_mean_geometry_fold": 0.65},
                            },
                            {
                                "entry_id": "m_csa:11",
                                "is_inscope": False,
                                "is_oos": True,
                                "is_confounded_predicted_geometry_oos": True,
                                "channel_scores": {"combined_mean_geometry_fold": 0.5},
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_augmented_oos_calibrated_threshold_contract(
                threshold_contract_path=threshold_contract,
                train_cal_oos_surface_path=oos_surface,
                fold_augmented_gate_path=fold_gate,
            )

        self.assertEqual(audit["status"], "computed_oos_calibrated_threshold_contract")
        self.assertTrue(audit["guardrails"]["train_cal_oos_negatives_used_for_threshold"])
        primary = audit["primary_channel_readout"]
        selected = primary[
            "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain"
        ]
        self.assertEqual(selected["threshold"], 0.6)
        self.assertEqual(selected["calibration_oos_abstain_recall"], 0.5)
        self.assertEqual(
            primary["heldout_final_eval_at_90pct_oos_calibrated_threshold"][
                "heldout_confounded_oos_abstain_recall"
            ],
            1.0,
        )

    def test_fold_only_negative_surface_keeps_fold_scored_geometry_gaps(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            surface = root / "surface.json"
            surface.write_text(
                json.dumps(
                    {
                        "candidate_row_scores": [
                            {
                                "entry_id": "m_csa:57",
                                "accession": "P13448",
                                "benchmark_role": "oos_tier::unknown_oos",
                                "predicted_geometry_status": "missing",
                                "channel_scores": None,
                                "predicted_structure_fold_channel": {
                                    "nearest_train_atlas_entry_id": "m_csa:1",
                                    "nearest_train_atlas_true_fingerprint_id": "metal_dependent_hydrolase",
                                    "nearest_train_atlas_tm_score": 0.42,
                                },
                            },
                            {
                                "entry_id": "m_csa:4",
                                "channel_scores": {"combined_mean_geometry_fold": 0.5},
                                "predicted_structure_fold_channel": {
                                    "nearest_train_atlas_tm_score": 0.4,
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_only_train_cal_oos_negative_surface(
                train_cal_oos_surface_path=surface,
            )

        self.assertEqual(audit["status"], "fold_only_negative_surface_ready")
        self.assertEqual(audit["counts"]["fold_only_rows"], 1)
        self.assertEqual(audit["rows"][0]["entry_id"], "m_csa:57")

    def test_train_cal_oos_blocker_resolution_groups_missing_scores(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            surface = root / "surface.json"
            surface.write_text(
                json.dumps(
                    {
                        "counts": {
                            "candidate_ids_requested": 1,
                            "candidate_rows_with_full_channel_scores": 0,
                        },
                        "excluded_candidate_geometry_rows": [
                            {
                                "entry_id": "m_csa:57",
                                "reason": "missing_accession_compatible_sequence_positions",
                            }
                        ],
                        "candidate_row_scores": [
                            {
                                "entry_id": "m_csa:57",
                                "accession": "P13448",
                                "predicted_geometry_status": "missing",
                                "channel_scores": None,
                                "predicted_structure_fold_channel": {
                                    "nearest_train_atlas_tm_score": 0.42,
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_augmented_train_cal_oos_negative_surface_blocker_resolution(
                train_cal_oos_surface_path=surface,
            )

        self.assertEqual(audit["status"], "blocker_resolution_packet_ready")
        self.assertEqual(audit["counts"]["missing_full_score_rows"], 1)
        self.assertEqual(
            audit["blocker_rows"][0]["blocker_reason"],
            "missing_accession_compatible_sequence_positions",
        )

    def test_train_cal_oos_sufficiency_decision_allows_research_partial_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            surface = root / "surface.json"
            blockers = root / "blockers.json"
            contract = root / "contract.json"
            fold_only = root / "fold_only.json"
            surface.write_text(
                json.dumps(
                    {
                        "counts": {
                            "candidate_ids_requested": 10,
                            "candidate_rows_with_full_channel_scores": 9,
                        }
                    }
                ),
                encoding="utf-8",
            )
            blockers.write_text(
                json.dumps(
                    {
                        "counts": {
                            "missing_full_score_rows": 1,
                            "blocker_reason_counts": {
                                "alphafold_db_coordinate_unavailable": 1
                            },
                        },
                        "blocker_rows": [
                            {
                                "entry_id": "m_csa:78",
                                "blocker_reason": "alphafold_db_coordinate_unavailable",
                                "fold_tm_available": False,
                                "recommended_action": "source alternate coordinate",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            contract.write_text(
                json.dumps(
                    {
                        "primary_channel_readout": {
                            "channel": "combined_mean_geometry_fold",
                            "prior_in_scope_only_selected_at_90pct": {
                                "threshold": 0.44
                            },
                            "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain": {
                                "threshold": 0.44,
                                "calibration_oos_total": 9,
                                "calibration_oos_abstained": 4,
                                "calibration_oos_abstain_recall": 0.4444,
                            },
                            "heldout_final_eval_at_90pct_oos_calibrated_threshold": {
                                "heldout_in_scope_retain_recall": 0.95,
                                "heldout_oos_abstain_recall": 0.55,
                                "heldout_confounded_oos_abstain_recall": 0.83,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            fold_only.write_text(
                json.dumps({"counts": {"fold_only_rows": 1}}),
                encoding="utf-8",
            )

            audit = build_fold_augmented_train_cal_oos_negative_surface_sufficiency_decision(
                train_cal_oos_surface_path=surface,
                blocker_resolution_path=blockers,
                oos_calibrated_threshold_contract_path=contract,
                fold_only_surface_path=fold_only,
            )

        self.assertEqual(
            audit["status"],
            "research_contract_sufficient_with_blocker_disclosure",
        )
        self.assertTrue(audit["decision"]["research_surface_sufficient"])
        self.assertFalse(audit["decision"]["production_surface_sufficient"])
        self.assertEqual(audit["counts"]["score_complete_fraction"], 0.9)

    def test_fold_augmented_family_panel_readout_applies_research_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            contract = root / "contract.json"
            sufficiency = root / "sufficiency.json"
            coverage = root / "coverage.json"
            packet = root / "packet.json"
            contract.write_text(
                json.dumps(
                    {
                        "status": "computed_oos_calibrated_threshold_contract",
                        "primary_channel_readout": {
                            "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain": {
                                "threshold": 0.5
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            sufficiency.write_text(
                json.dumps(
                    {
                        "status": "research_contract_sufficient_with_blocker_disclosure"
                    }
                ),
                encoding="utf-8",
            )
            coverage.write_text(
                json.dumps(
                    {
                        "panel_summaries": [
                            {"panel_id": "panel_a", "artifact": str(packet)}
                        ]
                    }
                ),
                encoding="utf-8",
            )
            packet.write_text(
                json.dumps(
                    {
                        "status": "evidence_packet_ready_review_only",
                        "panel": {"candidate_family": "panel_a"},
                        "row_evidence": [
                            {
                                "entry_id": "m_csa:1",
                                "predicted_geometry_status": "ok",
                                "predicted_geometry_top1": {
                                    "fingerprint_id": "metal_dependent_hydrolase",
                                    "score": 0.7,
                                },
                                "predicted_structure_fold_channel": {
                                    "nearest_atlas_entry_id": "m_csa:2",
                                    "nearest_atlas_true_fingerprint_id": "metal_dependent_hydrolase",
                                    "nearest_atlas_tm_score": 0.6,
                                },
                                "selected_organic_cofactor_max": 0.2,
                            },
                            {
                                "entry_id": "m_csa:3",
                                "predicted_geometry_status": "ok",
                                "predicted_geometry_top1": {
                                    "fingerprint_id": "ser_his_acid_hydrolase",
                                    "score": 0.3,
                                },
                                "predicted_structure_fold_channel": {
                                    "nearest_atlas_entry_id": "m_csa:4",
                                    "nearest_atlas_true_fingerprint_id": "ser_his_acid_hydrolase",
                                    "nearest_atlas_tm_score": 0.4,
                                },
                                "selected_organic_cofactor_max": 0.1,
                            },
                            {
                                "entry_id": "m_csa:5",
                                "predicted_geometry_status": "missing",
                                "predicted_geometry_top1": {"score": None},
                                "predicted_structure_fold_channel": {
                                    "nearest_atlas_tm_score": None
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_augmented_family_panel_research_readout(
                oos_calibrated_threshold_contract_path=contract,
                sufficiency_decision_path=sufficiency,
                family_panel_coverage_audit_path=coverage,
            )

        self.assertEqual(
            audit["status"],
            "family_panel_research_readout_ready_review_only",
        )
        self.assertEqual(audit["threshold_source"]["threshold"], 0.5)
        self.assertEqual(audit["counts"]["primary_score_complete_rows"], 2)
        self.assertEqual(audit["counts"]["non_abstained_at_research_threshold"], 1)
        self.assertEqual(audit["counts"]["abstained_at_research_threshold"], 1)
        self.assertEqual(audit["counts"]["not_score_complete_for_primary_channel"], 1)
        self.assertEqual(audit["review_priority_rows"][0]["entry_id"], "m_csa:1")
        self.assertEqual(
            audit["panel_summaries"][0]["research_readout_status"],
            "has_non_abstained_review_rows",
        )

    def test_fold_augmented_family_panel_readout_reuses_train_cal_fold_scores(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            contract = root / "contract.json"
            sufficiency = root / "sufficiency.json"
            coverage = root / "coverage.json"
            packet = root / "packet.json"
            train_cal = root / "train_cal.json"
            contract.write_text(
                json.dumps(
                    {
                        "status": "computed_oos_calibrated_threshold_contract",
                        "primary_channel_readout": {
                            "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain": {
                                "threshold": 0.5
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            sufficiency.write_text(
                json.dumps(
                    {
                        "status": "research_contract_sufficient_with_blocker_disclosure"
                    }
                ),
                encoding="utf-8",
            )
            coverage.write_text(
                json.dumps(
                    {
                        "panel_summaries": [
                            {"panel_id": "panel_a", "artifact": str(packet)}
                        ]
                    }
                ),
                encoding="utf-8",
            )
            packet.write_text(
                json.dumps(
                    {
                        "status": "evidence_packet_ready_review_only",
                        "panel": {"candidate_family": "panel_a"},
                        "row_evidence": [
                            {
                                "entry_id": "m_csa:973",
                                "predicted_geometry_status": "ok",
                                "predicted_geometry_top1": {
                                    "fingerprint_id": "metal_dependent_hydrolase",
                                    "score": 0.7,
                                },
                                "predicted_structure_fold_channel": {},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            train_cal.write_text(
                json.dumps(
                    {
                        "calibration_row_scores": [
                            {
                                "entry_id": "m_csa:973",
                                "partition": "calibration",
                                "nearest_train_atlas_entry_id": "m_csa:795",
                                "nearest_train_atlas_true_fingerprint_id": "heme_peroxidase_oxidase",
                                "channel_scores": {
                                    "fold_nearest_atlas_tm_score": 0.4575,
                                    "geometry_top1_score": 0.3625,
                                    "combined_mean_geometry_fold": 0.41,
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_augmented_family_panel_research_readout(
                oos_calibrated_threshold_contract_path=contract,
                sufficiency_decision_path=sufficiency,
                family_panel_coverage_audit_path=coverage,
                train_cal_threshold_contract_path=train_cal,
            )

        row = audit["row_scores"][0]
        self.assertEqual(audit["counts"]["primary_score_complete_rows"], 1)
        self.assertEqual(row["research_gate_status"], "non_abstained_at_research_threshold")
        self.assertEqual(
            row["predicted_structure_fold_score_source"],
            "fold_augmented_train_cal_threshold_contract_calibration_row",
        )
        self.assertEqual(
            row["channel_scores"]["fold_nearest_atlas_tm_score"],
            0.4575,
        )

    def test_fold_augmented_family_panel_source_check_queue_uses_priority_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readout = root / "readout.json"
            readout.write_text(
                json.dumps(
                    {
                        "status": "family_panel_research_readout_ready_review_only",
                        "review_priority_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "panel_id": "panel_a",
                                "combined_mean_geometry_fold": 0.6,
                                "threshold_margin": 0.1,
                                "predicted_geometry_top1_fingerprint_id": "metal_dependent_hydrolase",
                                "nearest_atlas_true_fingerprint_id": "flavin_dehydrogenase_reductase",
                                "selected_organic_cofactor_max": 0.9,
                            }
                        ],
                        "row_scores": [
                            {
                                "entry_id": "m_csa:1",
                                "panel_id": "panel_a",
                                "split_assignment": "heldout",
                                "benchmark_role": "oos_tier::unknown_oos",
                                "predicted_geometry_top1_fingerprint_id": "metal_dependent_hydrolase",
                                "predicted_structure_nearest_atlas_true_fingerprint_id": "flavin_dehydrogenase_reductase",
                                "selected_organic_cofactor_max": 0.9,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_augmented_family_panel_source_check_queue(
                family_panel_research_readout_path=readout,
            )

        self.assertEqual(audit["status"], "source_check_queue_ready_review_only")
        self.assertEqual(audit["counts"]["source_check_rows"], 1)
        self.assertEqual(audit["queue_rows"][0]["entry_id"], "m_csa:1")
        self.assertIn(
            "geometry_fold_fingerprint_disagreement",
            audit["queue_rows"][0]["source_check_focus"],
        )
        self.assertFalse(audit["guardrails"]["new_source_data_fetched"])

    def test_fold_augmented_family_panel_missing_primary_channel_queue_uses_readout_blockers(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readout = root / "readout.json"
            readout.write_text(
                json.dumps(
                    {
                        "status": "family_panel_research_readout_ready_review_only",
                        "row_scores": [
                            {
                                "entry_id": "m_csa:132",
                                "panel_id": "fmo",
                                "research_gate_status": "not_score_complete_for_primary_channel",
                                "score_blockers": [
                                    "predicted_geometry_top1_score_missing",
                                    "predicted_structure_fold_tm_missing",
                                ],
                            },
                            {
                                "entry_id": "m_csa:973",
                                "panel_id": "fmo",
                                "research_gate_status": "abstained_at_research_threshold",
                                "score_blockers": [],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_augmented_family_panel_missing_primary_channel_queue(
                family_panel_research_readout_path=readout,
            )

        self.assertEqual(
            audit["status"],
            "missing_primary_channel_queue_ready_review_only",
        )
        self.assertEqual(audit["counts"]["missing_primary_channel_rows"], 1)
        self.assertEqual(audit["counts"]["m_csa_rows"], 1)
        self.assertEqual(audit["queue_rows"][0]["entry_id"], "m_csa:132")
        self.assertIn(
            "repair or materialize predicted active-site geometry",
            audit["queue_rows"][0]["recommended_next_action"],
        )

    def test_fold_augmented_family_panel_missing_primary_channel_diagnosis_reuses_train_cal_fold_score(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            queue = root / "queue.json"
            train_cal = root / "train_cal.json"
            fold_channel = root / "fold_channel.json"
            predicted_geometry = root / "predicted_geometry.json"
            adjudication = root / "adjudication.json"
            queue.write_text(
                json.dumps(
                    {
                        "status": "missing_primary_channel_queue_ready_review_only",
                        "queue_rows": [
                            {
                                "rank": 1,
                                "entry_id": "m_csa:973",
                                "panel_id": "fmo",
                                "split_assignment": "in_distribution",
                                "benchmark_role": "primary_supervised_metric::flavin_dehydrogenase_reductase",
                                "score_blockers": [
                                    "predicted_structure_fold_tm_missing"
                                ],
                            },
                            {
                                "rank": 2,
                                "entry_id": "external_panel_row",
                                "panel_id": "external",
                                "score_blockers": [
                                    "predicted_geometry_top1_score_missing",
                                    "predicted_structure_fold_tm_missing",
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            train_cal.write_text(
                json.dumps(
                    {
                        "calibration_row_scores": [
                            {
                                "entry_id": "m_csa:973",
                                "partition": "calibration",
                                "true_fingerprint_id": "flavin_dehydrogenase_reductase",
                                "nearest_train_atlas_entry_id": "m_csa:795",
                                "nearest_train_atlas_true_fingerprint_id": "heme_peroxidase_oxidase",
                                "channel_scores": {
                                    "geometry_top1_score": 0.3625,
                                    "fold_nearest_atlas_tm_score": 0.4575,
                                    "combined_mean_geometry_fold": 0.41,
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            fold_channel.write_text(
                json.dumps({"fold_channel_signal": {}}),
                encoding="utf-8",
            )
            predicted_geometry.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "entry_id": "m_csa:973",
                                "status": "ok",
                                "split_assignment": "in_distribution",
                                "accession": "A0A0C6DRW4",
                                "predicted_pdb_id": "AF-A0A0C6DRW4-F1-model_v6",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "top1_score": 0.3625,
                                "true_fingerprint_id": "flavin_dehydrogenase_reductase",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            adjudication.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:973",
                                "mechanism_clean": True,
                                "coordinate_clean": False,
                                "accepted_for_clean_support_readiness": True,
                                "import_ready": False,
                                "registry_edit_allowed": False,
                                "mechanism_decision": "mechanism_clean_two_component_FMNH2_sulfur_monooxygenase_support",
                                "coordinate_decision": "structure_resolved_source_text_typo_pending_external_source_check",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_augmented_family_panel_missing_primary_channel_diagnosis(
                missing_primary_channel_queue_path=queue,
                train_cal_threshold_contract_path=train_cal,
                predicted_structure_fold_channel_path=fold_channel,
                predicted_geometry_atlas_retrieval_path=predicted_geometry,
                local_candidate_adjudication_path=adjudication,
            )

        self.assertEqual(
            audit["status"],
            "missing_primary_channel_diagnosis_ready_review_only",
        )
        self.assertEqual(audit["counts"]["diagnosed_rows"], 2)
        self.assertEqual(audit["counts"]["rows_with_train_calibration_fold_score"], 1)
        by_entry = {row["entry_id"]: row for row in audit["diagnosed_rows"]}
        self.assertEqual(
            by_entry["m_csa:973"]["diagnosis"],
            "family_panel_lookup_scope_gap",
        )
        self.assertEqual(
            by_entry["m_csa:973"]["fold_score_evidence"][
                "nearest_atlas_tm_score"
            ],
            0.4575,
        )
        self.assertFalse(
            by_entry["m_csa:973"]["local_review_evidence"]["registry_edit_allowed"]
        )
        self.assertEqual(
            by_entry["external_panel_row"]["diagnosis"],
            "needs_source_backed_row_sidecar_and_coordinate_materialization",
        )
        self.assertFalse(audit["guardrails"]["foldseek_or_tmsearch_recomputed"])

    def test_fold_augmented_family_panel_missing_primary_channel_diagnosis_reuses_source_backed_fold_score(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            queue = root / "queue.json"
            train_cal = root / "train_cal.json"
            fold_channel = root / "fold_channel.json"
            predicted_geometry = root / "predicted_geometry.json"
            source_backed = root / "source_backed.json"
            queue.write_text(
                json.dumps(
                    {
                        "status": "missing_primary_channel_queue_ready_review_only",
                        "queue_rows": [
                            {
                                "rank": 1,
                                "entry_id": "external_panel_row",
                                "panel_id": "external",
                                "score_blockers": [
                                    "predicted_geometry_top1_score_missing"
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            train_cal.write_text(json.dumps({"calibration_row_scores": []}), encoding="utf-8")
            fold_channel.write_text(json.dumps({"row_scores": []}), encoding="utf-8")
            predicted_geometry.write_text(json.dumps({"results": []}), encoding="utf-8")
            source_backed.write_text(
                json.dumps(
                    {
                        "row_scores": [
                            {
                                "entry_id": "external_panel_row",
                                "selected_structure_id": "7QQF",
                                "sidecar_path": "sidecars/external.json",
                                "predicted_structure_fold_channel": {
                                    "nearest_atlas_entry_id": "m_csa:697",
                                    "nearest_atlas_true_fingerprint_id": "flavin_dehydrogenase_reductase",
                                    "nearest_atlas_tm_score": 0.6259,
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_augmented_family_panel_missing_primary_channel_diagnosis(
                missing_primary_channel_queue_path=queue,
                train_cal_threshold_contract_path=train_cal,
                predicted_structure_fold_channel_path=fold_channel,
                predicted_geometry_atlas_retrieval_path=predicted_geometry,
                source_backed_materialization_path=source_backed,
            )

        row = audit["diagnosed_rows"][0]
        self.assertEqual(
            row["diagnosis"],
            "source_backed_fold_scored_needs_predicted_geometry",
        )
        self.assertEqual(audit["counts"]["rows_with_source_backed_fold_score"], 1)
        self.assertEqual(
            row["fold_score_evidence"]["source"],
            "family_panel_source_backed_afdb_vs_predicted_atlas",
        )
        self.assertEqual(row["fold_score_evidence"]["nearest_atlas_tm_score"], 0.6259)
        self.assertIn(
            "remaining primary-channel blocker is source-free predicted active-site geometry",
            audit["interpretation"]["headline"],
        )
        self.assertFalse(audit["guardrails"]["foldseek_or_tmsearch_recomputed"])

    def test_fold_augmented_family_panel_m_csa_repair_scores_repaired_row(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            diagnosis = root / "diagnosis.json"
            manifest = root / "manifest.json"
            graph = root / "graph.json"
            experimental = root / "experimental.json"
            fold_channel = root / "fold_channel.json"
            threshold = root / "threshold.json"
            tsv = root / "repair.tsv"
            diagnosis.write_text(
                json.dumps(
                    {
                        "status": "missing_primary_channel_diagnosis_ready_review_only",
                        "diagnosed_rows": [
                            {
                                "entry_id": "m_csa:132",
                                "diagnosis": "needs_predicted_geometry_materialization",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            manifest.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:132",
                                "accession": "P0",
                                "sequence_id": "P0",
                                "real_sequence_accessions": ["P0", "ALT"],
                                "split_assignment": "in_distribution",
                                "benchmark_role": "secondary_ood_probe::flavin_monooxygenase",
                                "fingerprint_id": "flavin_monooxygenase",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "nodes": [
                            {
                                "id": "m_csa:132:residue:1",
                                "type": "catalytic_residue",
                                "roles": ["proton acceptor"],
                                "sequence_positions": [
                                    {
                                        "is_reference": True,
                                        "resid": 10,
                                        "code": "Asp",
                                        "uniprot_id": "ALT",
                                    }
                                ],
                            },
                            {
                                "id": "m_csa:132:residue:2",
                                "type": "catalytic_residue",
                                "roles": ["proton donor"],
                                "sequence_positions": [
                                    {
                                        "is_reference": True,
                                        "resid": 30,
                                        "code": "His",
                                        "uniprot_id": "ALT",
                                    }
                                ],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            experimental.write_text(
                json.dumps({"entries": [{"entry_id": "m_csa:132", "status": "ok"}]}),
                encoding="utf-8",
            )
            fold_channel.write_text(
                json.dumps(
                    {
                        "foldseek_input_manifest": {
                            "coordinate_request_groups": {
                                "atlas_in_distribution": [
                                    {
                                        "accession": "ATLAS",
                                        "alphafold_version": 6,
                                        "predicted_pdb_id": "AF-ATLAS-F1-model_v6",
                                        "expected_local_path": str(
                                            root / "atlas" / "afdb_ATLAS_v6.cif"
                                        ),
                                        "entry_ids": ["m_csa:1"],
                                        "rows": [
                                            {
                                                "entry_id": "m_csa:1",
                                                "true_fingerprint_id": "metal_dependent_hydrolase",
                                            }
                                        ],
                                    }
                                ]
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            threshold.write_text(
                json.dumps(
                    {
                        "threshold_contract": {
                            "combined_mean_geometry_fold": {
                                "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain": {
                                    "threshold": 0.44155
                                }
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            tsv.write_text(
                "afdb_ALT_v6\tafdb_ATLAS_v6\t0.6\t0.55\t0.5\t0.9\t100\n",
                encoding="utf-8",
            )

            def fake_fetcher(accession: str, version: str = "auto") -> tuple[str, dict]:
                return MINI_AF_CIF, {
                    "backend": "alphafold_db",
                    "accession": accession,
                    "alphafold_version": 6,
                    "url": f"memory://{accession}",
                }

            audit = build_fold_augmented_family_panel_m_csa_primary_channel_repair(
                missing_primary_channel_diagnosis_path=diagnosis,
                label_manifest_path=manifest,
                graph_path=graph,
                experimental_geometry_features_path=experimental,
                predicted_structure_fold_channel_path=fold_channel,
                oos_calibrated_threshold_contract_path=threshold,
                coordinate_root=root / "coordinates",
                target_atlas_dir=root / "atlas",
                foldseek_result_tsv=tsv,
                foldseek_binary="/bin/echo",
                fetcher=fake_fetcher,
            )

        self.assertEqual(
            audit["status"],
            "m_csa_primary_channel_repair_scored_review_only",
        )
        self.assertEqual(audit["counts"]["primary_channel_score_complete_rows"], 1)
        row = audit["row_scores"][0]
        self.assertEqual(row["entry_id"], "m_csa:132")
        self.assertEqual(row["predicted_geometry_accession"], "ALT")
        self.assertEqual(
            row["predicted_geometry_accession_repair"]["policy"],
            "best_real_sequence_accession_by_active_site_coverage",
        )
        self.assertEqual(row["nearest_atlas_entry_id"], "m_csa:1")
        self.assertEqual(row["nearest_atlas_tm_score"], 0.6)
        self.assertIsNotNone(row["combined_mean_geometry_fold"])
        self.assertTrue(audit["guardrails"]["review_only"])

    def test_train_cal_oos_geometry_selection_allows_accession_subset(self) -> None:
        label_manifest = {
            "rows": [
                {
                    "entry_id": "m_csa:57",
                    "accession": "P13448",
                    "sequence_id": "P13448",
                    "split_assignment": "in_distribution",
                }
            ]
        }
        graph = {
            "nodes": [
                {
                    "id": "m_csa:57:residue:1",
                    "type": "catalytic_residue",
                    "sequence_positions": [
                        {
                            "is_reference": True,
                            "resid": 110,
                            "code": "Cys",
                            "uniprot_id": "P13448",
                        }
                    ],
                },
                {
                    "id": "m_csa:57:residue:2",
                    "type": "catalytic_residue",
                    "sequence_positions": [
                        {
                            "is_reference": True,
                            "resid": 114,
                            "code": "Ser",
                            "uniprot_id": "P13448",
                        }
                    ],
                },
                {
                    "id": "m_csa:57:residue:3",
                    "type": "catalytic_residue",
                    "sequence_positions": [
                        {
                            "is_reference": True,
                            "resid": 72,
                            "code": "Tyr",
                            "uniprot_id": "P13449",
                        }
                    ],
                },
            ]
        }
        experimental = {"entries": [{"entry_id": "m_csa:57", "status": "ok"}]}

        strict_rows, strict_excluded = _target_manifest_row_selection(
            label_manifest=label_manifest,
            graph=graph,
            experimental_geometry_features=experimental,
            split_assignment=None,
            max_rows=0,
        )
        repaired_rows, repaired_excluded = _target_manifest_row_selection(
            label_manifest=label_manifest,
            graph=graph,
            experimental_geometry_features=experimental,
            split_assignment=None,
            max_rows=0,
            allow_accession_compatible_residue_subset=True,
        )

        self.assertEqual(strict_rows, [])
        self.assertEqual(
            strict_excluded[0]["reason"],
            "missing_accession_compatible_sequence_positions",
        )
        self.assertEqual(repaired_excluded, [])
        self.assertEqual(repaired_rows[0]["accession"], "P13448")
        self.assertEqual(
            repaired_rows[0]["predicted_geometry_accession_repair"]["policy"],
            "manifest_accession_compatible_residue_subset",
        )

    def test_train_cal_oos_geometry_selection_can_use_best_real_accession(self) -> None:
        label_manifest = {
            "rows": [
                {
                    "entry_id": "m_csa:284",
                    "accession": "O66186",
                    "sequence_id": "O66186",
                    "real_sequence_accessions": ["O66186", "O66188"],
                    "split_assignment": "in_distribution",
                }
            ]
        }
        graph = {
            "nodes": [
                {
                    "id": "m_csa:284:residue:1",
                    "type": "catalytic_residue",
                    "sequence_positions": [
                        {
                            "is_reference": True,
                            "resid": 108,
                            "code": "Tyr",
                            "uniprot_id": "O66186",
                        }
                    ],
                },
                {
                    "id": "m_csa:284:residue:2",
                    "type": "catalytic_residue",
                    "sequence_positions": [
                        {
                            "is_reference": True,
                            "resid": 128,
                            "code": "Cys",
                            "uniprot_id": "O66188",
                        }
                    ],
                },
                {
                    "id": "m_csa:284:residue:3",
                    "type": "catalytic_residue",
                    "sequence_positions": [
                        {
                            "is_reference": True,
                            "resid": 132,
                            "code": "Ser",
                            "uniprot_id": "O66188",
                        }
                    ],
                },
            ]
        }
        experimental = {"entries": [{"entry_id": "m_csa:284", "status": "ok"}]}

        rows, excluded = _target_manifest_row_selection(
            label_manifest=label_manifest,
            graph=graph,
            experimental_geometry_features=experimental,
            split_assignment=None,
            max_rows=0,
            allow_accession_compatible_residue_subset=True,
            allow_best_real_sequence_accession=True,
        )

        self.assertEqual(excluded, [])
        self.assertEqual(rows[0]["original_accession"], "O66186")
        self.assertEqual(rows[0]["accession"], "O66188")
        self.assertEqual(rows[0]["sequence_id"], "O66188")
        self.assertEqual(
            rows[0]["predicted_geometry_accession_repair"]["policy"],
            "best_real_sequence_accession_by_active_site_coverage",
        )

    def test_predicted_model_parts_uses_predicted_pdb_accession(self) -> None:
        accession, version, pdb_id = _predicted_model_parts(
            {
                "entry_id": "m_csa:284",
                "accession": "O66186",
                "predicted_pdb_id": "AF-O66188-F1-model_v6",
            }
        )

        self.assertEqual(accession, "O66188")
        self.assertEqual(version, 6)
        self.assertEqual(pdb_id, "AF-O66188-F1-model_v6")

    def test_active_site_role_graph_sidecar_normalizes_roles(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest = root / "manifest.json"
            graph = root / "graph.json"
            manifest.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "split_assignment": "in_distribution",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "nodes": [
                            {
                                "id": "m_csa:1:residue:1",
                                "type": "catalytic_residue",
                                "roles": ["Proton donor", "Metal ligand"],
                                "sequence_positions": [
                                    {
                                        "resid": 10,
                                        "code": "His",
                                        "uniprot_id": "P11111",
                                        "is_reference": True,
                                    }
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_active_site_role_graph_sidecar(
                label_manifest_path=manifest,
                graph_path=graph,
            )

        self.assertEqual(audit["status"], "active_site_role_graph_sidecar_ready")
        self.assertEqual(audit["counts"]["rows_with_ok_role_graph"], 1)
        self.assertEqual(
            audit["rows"][0]["role_counts"],
            {"metal_ligand": 1, "proton_donor": 1},
        )

    def test_reaction_center_template_sidecar_row_aligns_fingerprints(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest = root / "manifest.json"
            fingerprints = root / "fingerprints.json"
            manifest.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "fingerprint_id": "fp1",
                                "split_assignment": "in_distribution",
                            },
                            {
                                "entry_id": "m_csa:2",
                                "fingerprint_id": None,
                                "split_assignment": "in_distribution",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            fingerprints.write_text(
                json.dumps(
                    [
                        {
                            "id": "fp1",
                            "active_site_signature": [{"role": "nucleophile"}],
                            "cofactors": ["PLP"],
                            "reaction_center": {
                                "chemical_operation": "C-C bond cleavage",
                                "bond_changes": ["C-C bond broken"],
                            },
                        }
                    ]
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_reaction_center_template_sidecar(
                label_manifest_path=manifest,
                mechanism_fingerprints_path=fingerprints,
            )

        self.assertEqual(audit["status"], "reaction_center_template_sidecar_ready")
        self.assertEqual(audit["counts"]["rows_with_template"], 1)
        self.assertEqual(
            audit["rows"][0]["reaction_center_template"]["chemical_operation_normalized"],
            "c_c_bond_cleavage",
        )

    def test_mechanism_feature_sidecar_schema_audit_passes_aligned_sidecars(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest = root / "manifest.json"
            graph = root / "graph.json"
            fingerprints = root / "fingerprints.json"
            active_sidecar = root / "active.json"
            reaction_sidecar = root / "reaction.json"
            manifest.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "fingerprint_id": "fp1",
                                "split_assignment": "in_distribution",
                            },
                            {
                                "entry_id": "uniprot:Q11111",
                                "accession": "Q11111",
                                "fingerprint_id": None,
                                "split_assignment": "heldout",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "nodes": [
                            {
                                "id": "m_csa:1:residue:1",
                                "type": "catalytic_residue",
                                "roles": ["Proton donor"],
                                "sequence_positions": [
                                    {
                                        "resid": 10,
                                        "code": "His",
                                        "uniprot_id": "P11111",
                                        "is_reference": True,
                                    }
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            fingerprints.write_text(
                json.dumps(
                    [
                        {
                            "id": "fp1",
                            "active_site_signature": [{"role": "proton donor"}],
                            "cofactors": [],
                            "reaction_center": {
                                "chemical_operation": "hydrolysis",
                                "bond_changes": ["bond broken"],
                            },
                        }
                    ]
                ),
                encoding="utf-8",
            )
            active_sidecar.write_text(
                json.dumps(
                    build_mechanism_feature_active_site_role_graph_sidecar(
                        label_manifest_path=manifest,
                        graph_path=graph,
                    )
                ),
                encoding="utf-8",
            )
            reaction_sidecar.write_text(
                json.dumps(
                    build_mechanism_feature_reaction_center_template_sidecar(
                        label_manifest_path=manifest,
                        mechanism_fingerprints_path=fingerprints,
                    )
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_sidecar_schema_audit(
                label_manifest_path=manifest,
                mechanism_fingerprints_path=fingerprints,
                active_site_role_graph_sidecar_path=active_sidecar,
                reaction_center_template_sidecar_path=reaction_sidecar,
            )

        self.assertEqual(
            audit["status"],
            "mechanism_feature_sidecar_schema_passed_current702",
        )
        self.assertEqual(audit["counts"]["manifest_rows"], 2)
        self.assertTrue(
            all(count == 0 for count in audit["counts"]["critical_counts"].values())
        )

    def test_embedding_plan_reads_feature_sidecar_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            fingerprints = root / "fingerprints.json"
            manifest = root / "manifest.json"
            cofactor = root / "cofactor.json"
            atlas = root / "atlas.json"
            role_sidecar = root / "role.json"
            reaction_sidecar = root / "reaction.json"
            schema_audit = root / "schema_audit.json"
            fingerprints.write_text(
                json.dumps(
                    [
                        {
                            "id": "fp1",
                            "active_site_signature": [{"role": "nucleophile"}],
                            "cofactors": [],
                            "reaction_center": {
                                "chemical_operation": "hydrolysis",
                                "bond_changes": ["bond broken"],
                            },
                        }
                    ]
                ),
                encoding="utf-8",
            )
            manifest.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "fingerprint_id": "fp1",
                                "split_assignment": "in_distribution",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            cofactor.write_text(json.dumps({"row_class_records": []}), encoding="utf-8")
            atlas.write_text(json.dumps({"status": "complete", "counts": {}}), encoding="utf-8")
            role_sidecar.write_text(
                json.dumps(
                    {
                        "status": "active_site_role_graph_sidecar_ready",
                        "counts": {
                            "rows_with_ok_role_graph": 1,
                            "unique_roles": 1,
                            "unique_role_edges": 0,
                        },
                    }
                ),
                encoding="utf-8",
            )
            reaction_sidecar.write_text(
                json.dumps(
                    {
                        "status": "reaction_center_template_sidecar_ready",
                        "counts": {
                            "rows_with_template": 1,
                            "unique_chemical_operations": 1,
                            "unique_bond_change_templates": 1,
                        },
                    }
                ),
                encoding="utf-8",
            )
            schema_audit.write_text(
                json.dumps(
                    {
                        "status": "mechanism_feature_sidecar_schema_passed_current702",
                        "counts": {"critical_counts": {"alignment_violations": 0}},
                    }
                ),
                encoding="utf-8",
            )

            audit = build_learned_mechanism_feature_embedding_plan(
                mechanism_fingerprints_path=fingerprints,
                label_manifest_path=manifest,
                selected_organic_cofactor_sidecar_path=cofactor,
                predicted_geometry_atlas_path=atlas,
                active_site_role_graph_sidecar_path=role_sidecar,
                reaction_center_template_sidecar_path=reaction_sidecar,
                mechanism_feature_sidecar_schema_audit_path=schema_audit,
            )

        readiness = audit["current_data_readiness"]
        self.assertEqual(
            readiness["active_site_role_graph_sidecar"]["rows_with_ok_role_graph"],
            1,
        )
        self.assertEqual(
            readiness["reaction_center_template_sidecar"]["rows_with_template"],
            1,
        )
        self.assertTrue(
            readiness["mechanism_feature_sidecar_schema_audit"][
                "schema_safe_for_train_cal_pilot"
            ]
        )

    def test_mechanism_feature_embedding_feature_contract_strips_labels(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            input_manifest = root / "input.json"
            split_manifest = root / "split.json"
            out = root / "contract.json"
            report = root / "contract.md"
            input_manifest.write_text(
                json.dumps(
                    {
                        "row_records": [
                            {
                                "entry_id": "m_csa:1",
                                "organic_cofactor_classes_available": [
                                    "flavin",
                                    "heme",
                                    "plp",
                                ],
                                "reaction_chemical_operation": "hydrolysis",
                            }
                        ],
                        "counts": {"heldout_excluded_rows": 1},
                    }
                ),
                encoding="utf-8",
            )
            split_manifest.write_text(
                json.dumps(
                    {
                        "split_records": [
                            {
                                "entry_id": "m_csa:1",
                                "assigned_embedding_split": "train",
                                "stratum": "fingerprint:test",
                                "fingerprint_id": "test_fingerprint",
                                "label_type": "primary",
                                "active_site_residue_count": 3,
                                "reaction_template_status": "template_available",
                                "role_graph_status": "ok",
                                "inorganic_locus_statuses": {
                                    "metal_ion_locus": "proximal_metal_context_available",
                                },
                            }
                        ],
                        "counts": {"heldout_excluded_rows": 1},
                    }
                ),
                encoding="utf-8",
            )

            audit = write_mechanism_feature_embedding_feature_contract(
                train_cal_input_manifest_path=input_manifest,
                train_cal_split_manifest_path=split_manifest,
                out_path=out,
                report_path=report,
            )

        self.assertEqual(
            audit["status"],
            "mechanism_feature_embedding_feature_contract_ready_no_model_fit",
        )
        self.assertEqual(audit["counts"]["feature_rows"], 1)
        self.assertEqual(audit["counts"]["heldout_excluded_rows"], 1)
        self.assertTrue(audit["guardrails"]["label_fields_excluded_from_feature_rows"])
        feature_row = audit["feature_rows"][0]
        self.assertNotIn("fingerprint_id", feature_row)
        self.assertNotIn("label_type", feature_row)
        self.assertEqual(
            feature_row["active_site_role_graph"]["active_site_residue_count"],
            3,
        )
        self.assertIn("fingerprint_id", audit["excluded_fields_as_features"])
        self.assertIn(
            "explicit_authorization_required_before_model_weights_are_fit",
            audit["blockers_before_model_fit"],
        )

    def test_family_panel_evidence_packet_is_review_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            family_targets = root / "family_targets.json"
            predicted_atlas = root / "predicted_atlas.json"
            fold_signal = root / "fold.json"
            sidecar = root / "cofactor.json"
            variants = root / "variants.json"
            predicted_fold = root / "predicted_fold.json"
            family_targets.write_text(
                json.dumps(
                    {
                        "candidate_families": [
                            {
                                "candidate_family": "glycyl_radical_or_thiamine_radical_lyase_boundary",
                                "priority_bins": ["cofactor_confounded_oos"],
                                "candidate_rows": ["m_csa:30"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            predicted_atlas.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "entry_id": "m_csa:30",
                                "split_assignment": "heldout",
                                "benchmark_role": "oos_tier::unknown",
                                "predicted_geometry_status": "ok",
                                "top_fingerprints": [
                                    {
                                        "fingerprint_id": "heme_peroxidase_oxidase",
                                        "score": 0.3,
                                        "role_match_fraction": 0.1,
                                        "cofactor_context_score": 0.5,
                                    }
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            fold_signal.write_text(
                json.dumps(
                    {
                        "confounded_row_details": [
                            {
                                "entry_id": "m_csa:30",
                                "nearest_train_label_group": "heme_peroxidase_oxidase",
                                "nearest_train_fingerprint_id": "heme_peroxidase_oxidase",
                                "fold_signals": {
                                    "nearest_primary_foldseek_prob": 0.057,
                                    "top3_primary_foldseek_prob": 0.057,
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            sidecar.write_text(
                json.dumps(
                    {
                        "row_class_records": [
                            {"entry_id": "m_csa:30", "class": "flavin", "selected_score": 0.1},
                            {"entry_id": "m_csa:30", "class": "heme", "selected_score": 0.8},
                            {"entry_id": "m_csa:30", "class": "plp", "selected_score": 0.2},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            variants.write_text(
                json.dumps(
                    {
                        "row_scores": [
                            {
                                "entry_id": "m_csa:30",
                                "variant_scores": {
                                    "top1_score_raw": 0.3,
                                    "negative_nearest_class_centroid_robust_distance": -2.0,
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            predicted_fold.write_text(
                json.dumps(
                    {
                        "status": "computed_all_heldout_foldseek_scores",
                        "parsed_foldseek_results": {
                            "all_heldout_vs_atlas": {
                                "nearest_atlas_hits": [
                                    {
                                        "query_entry_id": "m_csa:30",
                                        "nearest_atlas_entry_id": "m_csa:1",
                                        "nearest_atlas_true_fingerprint_id": "heme_peroxidase_oxidase",
                                        "tm_score": 0.42,
                                    }
                                ]
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            audit = build_family_panel_evidence_packet(
                family_targets_path=family_targets,
                predicted_geometry_atlas_path=predicted_atlas,
                fold_level_signal_path=fold_signal,
                selected_organic_cofactor_sidecar_path=sidecar,
                predicted_atlas_variants_path=variants,
                predicted_structure_fold_channel_path=predicted_fold,
            )

        self.assertEqual(audit["status"], "evidence_packet_ready_review_only")
        self.assertTrue(audit["guardrails"]["proposal_only"])
        self.assertEqual(audit["row_evidence"][0]["selected_organic_cofactor_max"], 0.8)
        self.assertEqual(
            audit["row_evidence"][0]["selected_pdb_fold_proxy"]["nearest_primary_foldseek_prob"],
            0.057,
        )
        self.assertEqual(
            audit["row_evidence"][0]["predicted_structure_fold_channel"][
                "nearest_atlas_tm_score"
            ],
            0.42,
        )

    def test_family_panel_evidence_packet_consumes_m_csa_repair_scores(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            family_targets = root / "family_targets.json"
            empty = root / "empty.json"
            repair = root / "repair.json"
            family_targets.write_text(
                json.dumps(
                    {
                        "candidate_families": [
                            {
                                "candidate_family": "flavin_panel",
                                "candidate_rows": ["m_csa:132"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            empty.write_text(
                json.dumps({"results": [], "confounded_row_details": [], "row_class_records": [], "row_scores": []}),
                encoding="utf-8",
            )
            repair.write_text(
                json.dumps(
                    {
                        "status": "m_csa_primary_channel_repair_scored_review_only",
                        "row_scores": [
                            {
                                "entry_id": "m_csa:132",
                                "split_assignment": "in_distribution",
                                "benchmark_role": "secondary_ood_probe::flavin_monooxygenase",
                                "predicted_geometry_status": "ok",
                                "geometry_top1_fingerprint_id": "ser_his_acid_hydrolase",
                                "geometry_top1_score": 0.3894,
                                "nearest_atlas_entry_id": "m_csa:120",
                                "nearest_atlas_true_fingerprint_id": "flavin_dehydrogenase_reductase",
                                "nearest_atlas_tm_score": 0.6879,
                                "predicted_geometry_accession_repair": {
                                    "policy": "best_real_sequence_accession_by_active_site_coverage"
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_family_panel_evidence_packet(
                family_targets_path=family_targets,
                predicted_geometry_atlas_path=empty,
                fold_level_signal_path=empty,
                selected_organic_cofactor_sidecar_path=empty,
                predicted_atlas_variants_path=empty,
                m_csa_primary_channel_repair_path=repair,
                panel_id="flavin_panel",
            )

        row = audit["row_evidence"][0]
        self.assertEqual(audit["status"], "evidence_packet_ready_review_only")
        self.assertEqual(row["predicted_geometry_status"], "ok")
        self.assertEqual(row["predicted_geometry_top1"]["score"], 0.3894)
        self.assertEqual(
            row["predicted_structure_fold_channel"]["nearest_atlas_tm_score"],
            0.6879,
        )
        self.assertEqual(
            row["predicted_structure_fold_channel"]["score_source"],
            "m_csa_primary_channel_repair",
        )
        self.assertEqual(audit["counts"]["missing_geometry_entry_ids"], [])

    def test_family_panel_evidence_packet_consumes_source_backed_fold_scores(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            family_targets = root / "family_targets.json"
            empty = root / "empty.json"
            source_backed = root / "source_backed.json"
            family_targets.write_text(
                json.dumps(
                    {
                        "candidate_families": [
                            {
                                "candidate_family": "external_panel",
                                "candidate_rows": ["external_panel_row"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            empty.write_text(
                json.dumps({"results": [], "confounded_row_details": [], "row_class_records": [], "row_scores": []}),
                encoding="utf-8",
            )
            source_backed.write_text(
                json.dumps(
                    {
                        "row_scores": [
                            {
                                "entry_id": "external_panel_row",
                                "predicted_structure_fold_channel": {
                                    "nearest_atlas_entry_id": "m_csa:697",
                                    "nearest_atlas_true_fingerprint_id": "flavin_dehydrogenase_reductase",
                                    "nearest_atlas_tm_score": 0.6259,
                                    "score_source": "family_panel_source_backed_afdb_vs_predicted_atlas",
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_family_panel_evidence_packet(
                family_targets_path=family_targets,
                predicted_geometry_atlas_path=empty,
                fold_level_signal_path=empty,
                selected_organic_cofactor_sidecar_path=empty,
                predicted_atlas_variants_path=empty,
                source_backed_materialization_path=source_backed,
                panel_id="external_panel",
            )

        row = audit["row_evidence"][0]
        self.assertEqual(audit["status"], "evidence_packet_ready_with_geometry_gaps")
        self.assertEqual(audit["counts"]["rows_with_predicted_structure_fold_hits"], 1)
        self.assertEqual(
            audit["counts"]["missing_geometry_entry_ids"],
            ["external_panel_row"],
        )
        self.assertEqual(
            row["predicted_structure_fold_channel"]["nearest_atlas_tm_score"],
            0.6259,
        )
        self.assertEqual(
            row["predicted_structure_fold_channel"]["score_source"],
            "family_panel_source_backed_afdb_vs_predicted_atlas",
        )

    def test_family_panel_source_backed_materialization_writes_sidecars(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            coordinate_dir = root / "coordinates"
            sidecar_dir = root / "sidecars"
            query_dir = root / "queries"
            target_dir = root / "targets"
            coordinate_dir.mkdir()
            query_dir.mkdir()
            target_dir.mkdir()
            pdb_path = coordinate_dir / "pdb_1ABC.cif"
            afdb_path = coordinate_dir / "AF-P11111-F1-model_v6.cif"
            pdb_path.write_text("data_1ABC\n", encoding="utf-8")
            afdb_path.write_text("data_AF\n", encoding="utf-8")
            plan = root / "plan.json"
            fold_channel = root / "fold_channel.json"
            tsv = root / "foldseek.tsv"
            out = root / "materialization.json"
            report = root / "materialization.md"
            plan.write_text(
                json.dumps(
                    {
                        "row_plan": [
                            {
                                "rank": 1,
                                "entry_id": "external_panel_row",
                                "panel_id": "external",
                                "priority": "P0",
                                "identifier_resolution": {
                                    "uniprot_id": "P11111",
                                    "source_accession": "uniprot:P11111",
                                    "source_urls": {},
                                },
                                "representative_selection": {
                                    "selected_source_row_id": "uniprot:P11111",
                                    "selection_policy": "unit_test",
                                    "display_name": "Unit test row",
                                },
                                "coordinate_materialization_manifest": {
                                    "preferred_coordinate_id": "1ABC",
                                    "pdb_cif_path": str(pdb_path),
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            fold_channel.write_text(
                json.dumps(
                    {
                        "foldseek_input_manifest": {
                            "coordinate_request_groups": {
                                "atlas_in_distribution": [
                                    {
                                        "accession": "T22222",
                                        "predicted_pdb_id": "AF-T22222-F1-model_v6",
                                        "rows": [
                                            {
                                                "entry_id": "m_csa:1",
                                                "true_fingerprint_id": "metal_dependent_hydrolase",
                                            }
                                        ],
                                    }
                                ]
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            tsv.write_text(
                "AF-P11111-F1-model_v6\tAF-T22222-F1-model_v6\t0.5\t0.6\t0.55\t0.9\t100\n",
                encoding="utf-8",
            )

            audit = write_family_panel_source_backed_sidecar_materialization(
                materialization_plan_path=plan,
                predicted_structure_fold_channel_path=fold_channel,
                coordinate_dir=coordinate_dir,
                sidecar_dir=sidecar_dir,
                foldseek_result_tsv=tsv,
                query_dir=query_dir,
                target_atlas_dir=target_dir,
                foldseek_binary="/missing/foldseek",
                target_priorities=["P0"],
                out_path=out,
                report_path=report,
            )
            row = audit["row_scores"][0]
            sidecar_written = Path(row["sidecar_path"]).is_file()
            sidecar = json.loads(Path(row["sidecar_path"]).read_text(encoding="utf-8"))
            out_written = out.is_file()
            report_written = report.is_file()

        self.assertEqual(audit["status"], "source_backed_sidecars_fold_scored_review_only")
        self.assertEqual(audit["counts"]["targeted_rows"], 1)
        self.assertEqual(audit["counts"]["foldseek_query_entries_with_hits"], 1)
        self.assertEqual(
            row["predicted_structure_fold_channel"]["nearest_atlas_tm_score"],
            0.6,
        )
        self.assertEqual(row["remaining_primary_channel_blockers"], ["predicted_geometry_top1_score_missing"])
        self.assertTrue(sidecar_written)
        self.assertFalse(sidecar["predictive_use_allowed"])
        self.assertFalse(sidecar["ready_for_label_import"])
        self.assertTrue(out_written)
        self.assertTrue(report_written)

    def test_family_panel_evidence_packet_uses_nondefault_panel_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            family_targets = root / "family_targets.json"
            empty = root / "empty.json"
            family_targets.write_text(
                json.dumps(
                    {
                        "candidate_families": [
                            {
                                "candidate_family": "lipoamide_or_sulfur_transfer_redox_boundary",
                                "priority_bins": ["cofactor_confounded_oos"],
                                "candidate_rows": ["m_csa:267"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            empty.write_text(json.dumps({"results": [], "row_class_records": []}), encoding="utf-8")

            audit = build_family_panel_evidence_packet(
                family_targets_path=family_targets,
                predicted_geometry_atlas_path=empty,
                fold_level_signal_path=empty,
                selected_organic_cofactor_sidecar_path=empty,
                predicted_atlas_variants_path=empty,
                panel_id="lipoamide_or_sulfur_transfer_redox_boundary",
            )

        self.assertEqual(
            audit["artifact_id"],
            "v3_family_panel_evidence_packet_lipoamide_or_sulfur_transfer_redox_boundary_current702_20260601",
        )
        self.assertEqual(
            audit["panel"]["candidate_family"],
            "lipoamide_or_sulfur_transfer_redox_boundary",
        )

    def test_selected_organic_cofactor_sidecar_schema_audit_passes_complete_grid(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sidecar_path = root / "sidecar.json"
            manifest_path = root / "manifest.json"
            source = root / "source.json"
            source.write_text("{}", encoding="utf-8")
            manifest_path.write_text(
                json.dumps(
                    {
                        "rows": [
                            {"entry_id": "m_csa:1", "split_assignment": "in_distribution"},
                            {"entry_id": "m_csa:2", "split_assignment": "heldout"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            records = []
            for entry_id, split in [
                ("m_csa:1", "in_distribution"),
                ("m_csa:2", "heldout"),
            ]:
                for cls in ("flavin", "heme", "plp"):
                    records.append(
                        {
                            "entry_id": entry_id,
                            "class": cls,
                            "cofactor_class": cls,
                            "selected_score": 0.1,
                            "selected_source": "trained:esm2_t6_8m",
                            "selected_source_status": "strict_original_selected_t6_t12_source_scored_all_current702",
                            "split_assignment": split,
                            "threshold_or_bin": {
                                "fixed_threshold": 0.5,
                                "threshold_policy": "fixed_0_5_not_tuned_on_heldout",
                            },
                            "source_artifact": str(source),
                            "source_channel_artifact": str(source),
                            "source_summary_artifact": str(source),
                            "provenance_hashes": {"label_manifest_sha256": "abc"},
                        }
                    )
            sidecar_path.write_text(
                json.dumps({"row_class_records": records}),
                encoding="utf-8",
            )

            audit = build_selected_organic_cofactor_sidecar_schema_audit(
                selected_organic_cofactor_sidecar_path=sidecar_path,
                label_manifest_path=manifest_path,
            )

        self.assertEqual(audit["status"], "schema_passed_strict_current702")
        self.assertEqual(audit["counts"]["row_class_records"], 6)
        self.assertTrue(all(v == 0 for v in audit["counts"]["critical_counts"].values()))

    def test_predicted_atlas_geometry_variants_use_atlas_only_stats(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            predicted_atlas = root / "predicted_atlas.json"
            fold_signal = root / "fold_signal.json"
            predicted_atlas.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "entry_id": "m_csa:1",
                                "split_assignment": "in_distribution",
                                "predicted_geometry_status": "ok",
                                "true_fingerprint_id": "metal_dependent_hydrolase",
                                "top_fingerprints": [
                                    {
                                        "fingerprint_id": "metal_dependent_hydrolase",
                                        "score": 0.8,
                                        "role_match_fraction": 0.8,
                                        "residue_match_fraction": 1.0,
                                        "mechanistic_coherence_score": 1.0,
                                        "substrate_pocket_score": 0.7,
                                        "compactness_score": 0.7,
                                        "cofactor_context_score": 0.2,
                                        "counterevidence_penalty": 1.0,
                                        "plp_ligand_anchor_score": 0.0,
                                    }
                                ],
                            },
                            {
                                "entry_id": "m_csa:2",
                                "split_assignment": "in_distribution",
                                "predicted_geometry_status": "ok",
                                "true_fingerprint_id": "ser_his_acid_hydrolase",
                                "top_fingerprints": [
                                    {
                                        "fingerprint_id": "ser_his_acid_hydrolase",
                                        "score": 0.7,
                                        "role_match_fraction": 0.7,
                                        "residue_match_fraction": 1.0,
                                        "mechanistic_coherence_score": 1.0,
                                        "substrate_pocket_score": 0.6,
                                        "compactness_score": 0.6,
                                        "cofactor_context_score": 0.2,
                                        "counterevidence_penalty": 1.0,
                                        "plp_ligand_anchor_score": 0.0,
                                    }
                                ],
                            },
                            {
                                "entry_id": "m_csa:3",
                                "split_assignment": "heldout",
                                "predicted_geometry_status": "ok",
                                "true_fingerprint_id": "metal_dependent_hydrolase",
                                "top_fingerprints": [
                                    {
                                        "fingerprint_id": "metal_dependent_hydrolase",
                                        "score": 0.75,
                                        "role_match_fraction": 0.8,
                                        "residue_match_fraction": 1.0,
                                        "mechanistic_coherence_score": 1.0,
                                        "substrate_pocket_score": 0.7,
                                        "compactness_score": 0.7,
                                        "cofactor_context_score": 0.2,
                                        "counterevidence_penalty": 1.0,
                                        "plp_ligand_anchor_score": 0.0,
                                    }
                                ],
                            },
                            {
                                "entry_id": "m_csa:30",
                                "split_assignment": "heldout",
                                "predicted_geometry_status": "ok",
                                "true_fingerprint_id": None,
                                "top_fingerprints": [
                                    {
                                        "fingerprint_id": "metal_dependent_hydrolase",
                                        "score": 0.2,
                                        "role_match_fraction": 0.1,
                                        "residue_match_fraction": 0.3,
                                        "mechanistic_coherence_score": 0.5,
                                        "substrate_pocket_score": 0.2,
                                        "compactness_score": 0.2,
                                        "cofactor_context_score": 0.0,
                                        "counterevidence_penalty": 0.6,
                                        "plp_ligand_anchor_score": 0.0,
                                    }
                                ],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            fold_signal.write_text(
                json.dumps(
                    {
                        "confounded_entry_ids": {
                            "predicted_geometry_overlap_current_gate": ["m_csa:30"]
                        }
                    }
                ),
                encoding="utf-8",
            )

            audit = build_predicted_atlas_geometry_novelty_variants(
                predicted_geometry_atlas_path=predicted_atlas,
                fold_level_signal_path=fold_signal,
            )

        self.assertEqual(audit["status"], "computed_predicted_atlas_geometry_variants")
        self.assertEqual(audit["counts"]["atlas_rows"], 2)
        self.assertEqual(audit["counts"]["heldout_rows"], 2)
        self.assertTrue(audit["guardrails"]["atlas_statistics_only_for_normalization"])
        self.assertEqual(
            audit["signals"]["top1_score_raw"]["auc_in_gt_oos_all"],
            1.0,
        )
        self.assertEqual(
            audit["row_scores"][0]["variant_scores"]["top1_score_x_role_raw"],
            0.6,
        )

    def test_predicted_structure_fold_augmented_operating_grid_reuses_variant_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            variants = root / "fold_augmented_variants.json"
            variants.write_text(
                json.dumps(
                    {
                        "best_signal": {"name": "mean_top1_raw_and_tm"},
                        "row_scores": [
                            {
                                "entry_id": "m_csa:1",
                                "is_inscope": True,
                                "is_oos": False,
                                "is_confounded_predicted_geometry_oos": False,
                                "variant_scores": {
                                    "mean_top1_raw_and_tm": 0.9,
                                    "nearest_atlas_tm_score": 0.8,
                                },
                            },
                            {
                                "entry_id": "m_csa:2",
                                "is_inscope": True,
                                "is_oos": False,
                                "is_confounded_predicted_geometry_oos": False,
                                "variant_scores": {
                                    "mean_top1_raw_and_tm": 0.8,
                                    "nearest_atlas_tm_score": 0.7,
                                },
                            },
                            {
                                "entry_id": "m_csa:30",
                                "is_inscope": False,
                                "is_oos": True,
                                "is_confounded_predicted_geometry_oos": True,
                                "variant_scores": {
                                    "mean_top1_raw_and_tm": 0.2,
                                    "nearest_atlas_tm_score": 0.2,
                                },
                            },
                            {
                                "entry_id": "m_csa:31",
                                "is_inscope": False,
                                "is_oos": True,
                                "is_confounded_predicted_geometry_oos": False,
                                "variant_scores": {
                                    "mean_top1_raw_and_tm": 0.3,
                                    "nearest_atlas_tm_score": 0.3,
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_predicted_structure_fold_augmented_novelty_operating_grid(
                fold_augmented_variants_path=variants,
            )

        self.assertEqual(
            audit["status"],
            "predicted_structure_fold_augmented_novelty_operating_grid_ready_review_only",
        )
        self.assertEqual(audit["counts"]["row_scores"], 4)
        self.assertEqual(audit["counts"]["grid_rows"], 8)
        self.assertTrue(audit["guardrails"]["uses_existing_variant_artifact_only"])
        self.assertFalse(audit["guardrails"]["foldseek_or_tmsearch_recomputed"])
        best = audit["best_signal_from_variant_artifact"]
        self.assertEqual(best["name"], "mean_top1_raw_and_tm")
        self.assertEqual(
            best["best_at_90pct_inscope_retention"]["oos_abstain_recall"],
            1.0,
        )
        self.assertEqual(
            [row["entry_id"] for row in best["confounded_rows"]],
            ["m_csa:30"],
        )

    def test_predicted_structure_fold_channel_stages_bounded_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            predicted_atlas = root / "predicted_atlas.json"
            fold_signal = root / "fold_signal.json"
            predicted_atlas.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "split_assignment": "in_distribution",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P11111-F1-model_v6",
                                "true_fingerprint_id": "metal_dependent_hydrolase",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                            },
                            {
                                "entry_id": "m_csa:30",
                                "accession": "P22222",
                                "split_assignment": "heldout",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P22222-F1-model_v6",
                                "true_fingerprint_id": None,
                                "top1_fingerprint_id": "heme_peroxidase_oxidase",
                            },
                            {
                                "entry_id": "m_csa:40",
                                "accession": "P33333",
                                "split_assignment": "heldout",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P33333-F1-model_v6",
                                "true_fingerprint_id": "ser_his_acid_hydrolase",
                                "top1_fingerprint_id": "ser_his_acid_hydrolase",
                            },
                            {
                                "entry_id": "m_csa:41",
                                "accession": "P44444",
                                "split_assignment": "heldout",
                                "predicted_geometry_status": "predicted_structure_fetch_failed",
                                "predicted_pdb_id": "AF-P44444-F1-model_v6",
                                "true_fingerprint_id": None,
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            fold_signal.write_text(
                json.dumps(
                    {
                        "confounded_entry_ids": {
                            "predicted_geometry_overlap_current_gate": [
                                "m_csa:30",
                                "m_csa:549",
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )

            audit = build_predicted_structure_fold_channel(
                predicted_geometry_atlas_path=predicted_atlas,
                fold_level_signal_path=fold_signal,
                coordinate_root=root / "coords",
                foldseek_binary=str(root / "missing-foldseek"),
                threads=2,
            )

        self.assertEqual(
            audit["artifact_id"],
            "v3_predicted_structure_fold_channel_current702_20260601",
        )
        self.assertEqual(audit["status"], "manifest_staged_missing_predicted_coordinate_bundle")
        self.assertFalse(audit["runtime"]["foldseek"]["available"])
        self.assertEqual(audit["counts"]["atlas_in_distribution_rows_ok"], 1)
        self.assertEqual(audit["counts"]["heldout_rows_ok"], 2)
        self.assertEqual(audit["counts"]["priority_cofactor_confounded_oos_rows"], 1)
        self.assertEqual(
            audit["target_rows"]["priority_cofactor_confounded_oos_missing_ids"],
            ["m_csa:549"],
        )
        self.assertIn("foldseek_runtime_unavailable", audit["blockers"])
        self.assertIn(
            "predicted_coordinate_files_missing_for_priority_scope",
            audit["blockers"],
        )
        priority_requests = audit["foldseek_input_manifest"]["coordinate_request_groups"][
            "priority_cofactor_confounded_oos_queries"
        ]
        self.assertEqual(priority_requests[0]["url"], "https://alphafold.ebi.ac.uk/files/AF-P22222-F1-model_v6.cif")
        self.assertIn("--exact-tmscore", audit["commands"]["run_priority_cofactor_confounded_oos_vs_atlas"])
        self.assertIn("query,target,qtmscore", audit["commands"]["run_priority_cofactor_confounded_oos_vs_atlas"])

    def test_predicted_structure_fold_channel_parses_priority_foldseek_tsv(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            predicted_atlas = root / "predicted_atlas.json"
            fold_signal = root / "fold_signal.json"
            result_tsv = root / "priority.tsv"
            predicted_atlas.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "split_assignment": "in_distribution",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P11111-F1-model_v6",
                                "true_fingerprint_id": "metal_dependent_hydrolase",
                            },
                            {
                                "entry_id": "m_csa:30",
                                "accession": "P22222",
                                "split_assignment": "heldout",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P22222-F1-model_v6",
                                "true_fingerprint_id": None,
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            fold_signal.write_text(
                json.dumps(
                    {
                        "confounded_entry_ids": {
                            "predicted_geometry_overlap_current_gate": ["m_csa:30"]
                        }
                    }
                ),
                encoding="utf-8",
            )
            result_tsv.write_text(
                "afdb_P22222_v6\tafdb_P11111_v6\t0.21\t0.35\t0.88\t0.7\t42\n",
                encoding="utf-8",
            )

            audit = build_predicted_structure_fold_channel(
                predicted_geometry_atlas_path=predicted_atlas,
                fold_level_signal_path=fold_signal,
                coordinate_root=root / "coords",
                foldseek_binary=str(root / "missing-foldseek"),
                priority_result_tsv=result_tsv,
            )

        parsed = audit["parsed_foldseek_results"][
            "priority_cofactor_confounded_oos_vs_atlas"
        ]
        self.assertEqual(audit["status"], "computed_priority_foldseek_scores")
        self.assertEqual(parsed["status"], "parsed")
        self.assertEqual(parsed["nearest_atlas_hits"][0]["query_entry_id"], "m_csa:30")
        self.assertEqual(parsed["nearest_atlas_hits"][0]["nearest_atlas_entry_id"], "m_csa:1")
        self.assertEqual(parsed["nearest_atlas_hits"][0]["tm_score"], 0.88)

    def test_predicted_structure_fold_channel_contract_audit_passes_scored_channel(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            predicted_atlas = root / "predicted_atlas.json"
            fold_signal = root / "fold_signal.json"
            fold_channel = root / "fold_channel.json"
            all_tsv = root / "all.tsv"
            priority_tsv = root / "priority.tsv"
            predicted_atlas.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "split_assignment": "in_distribution",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P11111-F1-model_v6",
                                "true_fingerprint_id": "metal_dependent_hydrolase",
                            },
                            {
                                "entry_id": "m_csa:30",
                                "accession": "P22222",
                                "split_assignment": "heldout",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P22222-F1-model_v6",
                                "true_fingerprint_id": None,
                            },
                            {
                                "entry_id": "m_csa:40",
                                "accession": "P33333",
                                "split_assignment": "heldout",
                                "predicted_geometry_status": "ok",
                                "predicted_pdb_id": "AF-P33333-F1-model_v6",
                                "true_fingerprint_id": "ser_his_acid_hydrolase",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            fold_signal.write_text(
                json.dumps(
                    {
                        "confounded_entry_ids": {
                            "predicted_geometry_overlap_current_gate": ["m_csa:30"]
                        }
                    }
                ),
                encoding="utf-8",
            )
            all_tsv.write_text(
                "afdb_P22222_v6\tafdb_P11111_v6\t0.1\t0.2\t0.7\t0.6\t40\n"
                "afdb_P33333_v6\tafdb_P11111_v6\t0.2\t0.3\t0.8\t0.7\t50\n",
                encoding="utf-8",
            )
            priority_tsv.write_text(
                "afdb_P22222_v6\tafdb_P11111_v6\t0.1\t0.2\t0.7\t0.6\t40\n",
                encoding="utf-8",
            )

            def digest(path: Path) -> str:
                return hashlib.sha256(path.read_bytes()).hexdigest()

            fold_channel.write_text(
                json.dumps(
                    {
                        "artifact_id": "v3_predicted_structure_fold_channel_current702_20260601",
                        "status": "computed_all_heldout_foldseek_scores",
                        "counts": {
                            "combined_predicted_retrieval_rows": 3,
                            "atlas_in_distribution_rows_ok": 1,
                            "heldout_rows_ok": 2,
                            "priority_cofactor_confounded_oos_rows": 1,
                            "priority_cofactor_confounded_oos_missing_ids": 0,
                        },
                        "guardrails": {
                            "labels_registries_ontologies_changed": False,
                            "imports_or_promotions_performed": False,
                            "production_thresholds_changed": False,
                            "heldout_threshold_tuning_for_deployment": False,
                            "large_model_downloads_performed": False,
                            "frozen_current702_inputs_only": True,
                            "score_fabrication": False,
                        },
                        "blockers": [
                            "predicted_coordinate_files_missing_for_priority_scope"
                        ],
                        "commands": {
                            "run_priority_cofactor_confounded_oos_vs_atlas": (
                                "foldseek easy-search q t out tmp --format-output "
                                "query,target,qtmscore,ttmscore,alntmscore,prob,bits "
                                "--exhaustive-search 1 --exact-tmscore 1"
                            ),
                            "run_all_heldout_vs_atlas_when_cheap": (
                                "foldseek easy-search q t out tmp --format-output "
                                "query,target,qtmscore,ttmscore,alntmscore,prob,bits "
                                "--exhaustive-search 1 --exact-tmscore 1"
                            ),
                        },
                        "parsed_foldseek_results": {
                            "all_heldout_vs_atlas": {
                                "status": "parsed",
                                "path": str(all_tsv),
                                "summary": {
                                    "mapped_pair_count": 2,
                                    "query_entry_count_with_hits": 2,
                                },
                                "nearest_atlas_hits": [
                                    {
                                        "query_entry_id": "m_csa:30",
                                        "tm_score": 0.7,
                                    },
                                    {
                                        "query_entry_id": "m_csa:40",
                                        "tm_score": 0.8,
                                    },
                                ],
                            },
                            "priority_cofactor_confounded_oos_vs_atlas": {
                                "status": "parsed",
                                "path": str(priority_tsv),
                                "summary": {
                                    "mapped_pair_count": 1,
                                    "query_entry_count_with_hits": 1,
                                },
                                "nearest_atlas_hits": [
                                    {
                                        "query_entry_id": "m_csa:30",
                                        "tm_score": 0.7,
                                    }
                                ],
                            },
                        },
                        "fold_channel_signal": {
                            "nearest_atlas_tm_score": {
                                "row_scores": [
                                    {
                                        "entry_id": "m_csa:30",
                                        "fold_signals": {
                                            "nearest_atlas_tm_score": 0.7
                                        },
                                    },
                                    {
                                        "entry_id": "m_csa:40",
                                        "fold_signals": {
                                            "nearest_atlas_tm_score": 0.8
                                        },
                                    },
                                ]
                            }
                        },
                        "source_artifacts": {
                            "predicted_geometry_atlas": {
                                "path": str(predicted_atlas),
                                "sha256": digest(predicted_atlas),
                            },
                            "fold_level_signal": {
                                "path": str(fold_signal),
                                "sha256": digest(fold_signal),
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )

            audit = build_predicted_structure_fold_channel_contract_audit(
                predicted_structure_fold_channel_path=fold_channel,
                predicted_geometry_atlas_path=predicted_atlas,
                fold_level_signal_path=fold_signal,
            )

        self.assertEqual(
            audit["status"],
            "fold_channel_contract_passed_current702",
        )
        self.assertEqual(audit["counts"]["all_heldout_nearest_hits"], 2)
        self.assertEqual(audit["counts"]["priority_nearest_hits"], 1)
        self.assertTrue(audit["foldseek_result_files"]["all_heldout_vs_atlas"]["exists"])
        self.assertTrue(
            all(count == 0 for count in audit["counts"]["critical_counts"].values())
        )


if __name__ == "__main__":
    unittest.main()
