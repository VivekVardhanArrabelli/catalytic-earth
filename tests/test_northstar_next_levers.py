from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.northstar_next_levers import (
    _predicted_model_parts,
    build_family_panel_evidence_packet,
    build_family_panel_high_value_glycyl_radical_readiness_packet,
    build_fold_augmented_abstention_gate,
    build_fold_augmented_confounded_deployment_closure_audit,
    build_fold_augmented_fold_only_deployment_contract_decision,
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
    build_family_panel_source_free_locator_human_decision_matrix,
    build_family_panel_source_free_predicted_geometry_retrieval,
    build_family_panel_source_free_predicted_geometry_source_check_preflight,
    build_learned_mechanism_feature_embedding_plan,
    build_mechanism_feature_active_site_role_graph_sidecar,
    build_mechanism_feature_reaction_center_template_sidecar,
    build_mechanism_feature_row_specific_bond_change_feature_contract_gap_audit,
    build_mechanism_feature_row_specific_bond_change_materialization_priority,
    build_mechanism_feature_row_specific_bond_change_p0_calibration_review_packet,
    build_mechanism_feature_row_specific_bond_change_p0_extraction_package_strict_audit,
    build_mechanism_feature_row_specific_bond_change_p0_extraction_work_package,
    build_mechanism_feature_row_specific_bond_change_p0_no_template_rerun,
    build_mechanism_feature_row_specific_bond_change_p0_oos_augmented_calibration_error_analysis,
    build_mechanism_feature_row_specific_bond_change_p0_oos_augmented_expanded_calibration_comparison,
    build_mechanism_feature_row_specific_bond_change_p0_oos_augmented_expanded_train_cal_feature_sidecar,
    build_mechanism_feature_row_specific_bond_change_p0_oos_augmented_retained_oos_feature_target,
    build_mechanism_feature_row_specific_bond_change_p0_oos_calibration_approved_source_evidence_sidecar,
    build_mechanism_feature_row_specific_bond_change_p0_oos_calibration_extraction_work_package,
    build_mechanism_feature_row_specific_bond_change_p0_oos_calibration_extraction_work_package_strict_audit,
    build_mechanism_feature_row_specific_bond_change_p0_oos_calibration_gap,
    build_mechanism_feature_row_specific_bond_change_p0_pending_rewrite_blocker,
    build_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar,
    build_mechanism_feature_row_specific_bond_change_p0_source_evidence_review_queue,
    build_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_strict_audit,
    build_mechanism_feature_row_specific_bond_change_p0_feature_readiness_audit,
    build_mechanism_feature_row_specific_bond_change_p0_source_graph_readiness,
    build_mechanism_feature_row_specific_bond_change_p0_rhea_lookup_manifest,
    build_mechanism_feature_row_specific_bond_change_p0_rhea_lookup_resolution,
    build_mechanism_feature_row_specific_bond_change_p0_rhea_resolution_consumption_audit,
    build_mechanism_feature_row_specific_bond_change_p0_rhea_unresolved_official_source_audit,
    build_mechanism_feature_row_specific_bond_change_p0_refresh_blocker_audit,
    build_mechanism_feature_row_specific_bond_change_p0_reviewer_decision_matrix,
    build_mechanism_feature_row_specific_bond_change_p0_train_cal_coverage_gap,
    build_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_guardrail_audit,
    build_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_sidecar,
    build_mechanism_feature_row_specific_bond_change_schema,
    build_mechanism_feature_embedding_pilot,
    build_mechanism_feature_sidecar_schema_audit,
    build_predicted_atlas_geometry_novelty_variants,
    build_predicted_atlas_vs_fold_novelty_operating_grid_delta,
    build_predicted_structure_fold_augmented_novelty_operating_grid,
    build_predicted_structure_fold_channel,
    build_predicted_structure_fold_channel_carryover_resolution,
    build_predicted_structure_fold_channel_contract_audit,
    build_predicted_structure_fold_channel_coordinate_provenance_audit,
    build_predicted_structure_fold_channel_reproduction_manifest,
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
    def test_predicted_structure_fold_reproduction_manifest_tracks_missing_bundle(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            tsv = root / "all_heldout_vs_atlas.tsv"
            fold_channel_path = root / "fold_channel.json"
            contract_path = root / "contract.json"
            provenance_path = root / "provenance.json"
            tsv.write_text(
                "afdb_Q1_v6\tafdb_A1_v6\t0.4\t0.5\t0.45\t0.9\t100\n",
                encoding="utf-8",
            )
            fold_channel_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "heldout_rows_ok": 1,
                            "priority_cofactor_confounded_oos_rows": 1,
                        },
                        "commands": {
                            "materialize_coordinate_bundle": "python fetch.py",
                            "run_priority_cofactor_confounded_oos_vs_atlas": (
                                "foldseek easy-search priority atlas out tmp "
                                "--exact-tmscore 1"
                            ),
                            "run_all_heldout_vs_atlas_when_cheap": (
                                "foldseek easy-search heldout atlas out tmp "
                                "--exact-tmscore 1"
                            ),
                        },
                        "foldseek_input_manifest": {
                            "coordinate_request_groups": {
                                "atlas_in_distribution": [
                                    {
                                        "accession": "A1",
                                        "entry_ids": ["m_csa:1"],
                                        "expected_local_path": str(root / "afdb_A1.cif"),
                                        "url": "https://example.invalid/AF-A1.cif",
                                        "download_command": "curl A1",
                                    }
                                ],
                                "queries_all_heldout": [
                                    {
                                        "accession": "Q1",
                                        "entry_ids": ["m_csa:2"],
                                        "expected_local_path": str(root / "afdb_Q1.cif"),
                                        "url": "https://example.invalid/AF-Q1.cif",
                                        "download_command": "curl Q1",
                                    }
                                ],
                            }
                        },
                        "parsed_foldseek_results": {
                            "all_heldout_vs_atlas": {
                                "path": str(tsv),
                                "status": "parsed",
                                "summary": {
                                    "mapped_pair_count": 1,
                                    "query_entry_count_with_hits": 1,
                                },
                            }
                        },
                        "runtime": {
                            "foldseek": {
                                "available": True,
                                "requested": "/bin/foldseek",
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            contract_path.write_text(
                json.dumps(
                    {
                        "status": "fold_channel_contract_passed_current702",
                        "counts": {"critical_counts": {"missing_result_files": 0}},
                    }
                ),
                encoding="utf-8",
            )
            provenance_path.write_text(
                json.dumps(
                    {
                        "status": "coordinate_bundle_not_persisted_results_parseable",
                        "counts": {
                            "unique_coordinate_files_expected": 2,
                            "unique_coordinate_files_missing": 2,
                            "unique_accessions_without_any_local_file": 2,
                            "result_files_parseable": True,
                        },
                    }
                ),
                encoding="utf-8",
            )

            manifest = build_predicted_structure_fold_channel_reproduction_manifest(
                predicted_structure_fold_channel_path=fold_channel_path,
                contract_audit_path=contract_path,
                coordinate_provenance_audit_path=provenance_path,
            )

        self.assertEqual(
            manifest["status"],
            "fold_channel_reproduction_manifest_ready_missing_coordinates",
        )
        self.assertEqual(manifest["counts"]["unique_coordinate_files_expected"], 2)
        self.assertEqual(manifest["counts"]["unique_coordinate_files_missing"], 2)
        self.assertTrue(manifest["counts"]["result_files_parseable"])
        self.assertFalse(manifest["counts"]["byte_reproduction_ready"])
        self.assertIn(
            "persistent_afdb_v6_coordinate_bundle_missing",
            manifest["blocker_classes"],
        )
        self.assertEqual(
            manifest["scored_channel_contract"]["critical_violation_total"],
            0,
        )

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

    def test_source_free_locator_human_decision_matrix_orders_classes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            status = root / "status.json"
            queue = root / "queue.json"
            status.write_text(
                json.dumps(
                    {
                        "status": "source_free_locator_blocker_resolution_status_ready_review_only",
                        "resolution_rows": [
                            {
                                "entry_id": "mh_067",
                                "source_accession": "uniprot:P00918",
                                "resolution_class": (
                                    "human_locator_copy_approval_after_split_safe_pass"
                                ),
                                "next_action": "approve or reject copy",
                            },
                            {
                                "entry_id": "mh_064",
                                "source_accession": "uniprot:C7C422",
                                "resolution_class": (
                                    "alternate_coordinate_fetch_approval_required"
                                ),
                                "next_action": "approve fetches",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps(
                    {
                        "status": "source_free_locator_remaining_blocker_action_queue_ready_review_only"
                    }
                ),
                encoding="utf-8",
            )

            matrix = build_family_panel_source_free_locator_human_decision_matrix(
                blocker_resolution_status_path=status,
                remaining_blocker_action_queue_path=queue,
            )

        self.assertEqual(
            matrix["status"],
            "source_free_locator_human_decision_matrix_ready_review_only",
        )
        self.assertEqual(matrix["counts"]["blocked_rows_tracked"], 2)
        self.assertEqual(matrix["counts"]["decision_classes"], 2)
        self.assertEqual(
            matrix["recommended_decision_order"][0],
            "human_locator_copy_approval_after_split_safe_pass",
        )
        self.assertFalse(
            matrix["decision_classes"][0]["automation_can_continue_without_decision"]
        )
        self.assertFalse(matrix["guardrails"]["new_coordinates_fetched"])

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

    def test_confounded_deployment_closure_blocks_production_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            fold_channel = root / "fold_channel.json"
            contract = root / "contract.json"
            threshold = root / "threshold.json"
            sufficiency = root / "sufficiency.json"
            clearance = root / "clearance.json"
            fold_channel.write_text(
                json.dumps(
                    {
                        "status": "computed_all_heldout_foldseek_scores",
                        "parsed_foldseek_results": {
                            "priority_cofactor_confounded_oos_vs_atlas": {
                                "nearest_atlas_hits": [
                                    {
                                        "query_entry_id": "m_csa:31",
                                        "nearest_atlas_entry_id": "m_csa:900",
                                        "nearest_atlas_true_fingerprint_id": (
                                            "ser_his_acid_hydrolase"
                                        ),
                                        "tm_score": 0.38,
                                    },
                                    {
                                        "query_entry_id": "m_csa:30",
                                        "nearest_atlas_entry_id": "m_csa:11",
                                        "nearest_atlas_true_fingerprint_id": (
                                            "metal_dependent_hydrolase"
                                        ),
                                        "tm_score": 0.5,
                                    },
                                ]
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            contract.write_text(
                json.dumps(
                    {
                        "status": "fold_channel_contract_passed_current702",
                        "counts": {
                            "heldout_rows_ok": 20,
                            "all_heldout_nearest_hits": 20,
                            "priority_cofactor_confounded_oos_rows": 2,
                            "priority_nearest_hits": 2,
                            "critical_counts": {"missing_priority_hit_ids": 0},
                        },
                    }
                ),
                encoding="utf-8",
            )
            threshold.write_text(
                json.dumps(
                    {
                        "counts": {"heldout_confounded_oos": 2},
                        "primary_channel_readout": {
                            "channel": "combined_mean_geometry_fold",
                            "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain": {
                                "threshold": 0.44,
                                "calibration_oos_total": 9,
                                "calibration_oos_abstained": 4,
                                "calibration_oos_abstain_recall": 0.4444,
                            },
                            "heldout_final_eval_at_90pct_oos_calibrated_threshold": {
                                "heldout_in_scope_retain_recall": 0.95,
                                "heldout_oos_abstain_recall": 0.55,
                                "heldout_confounded_oos_abstain_recall": 1.0,
                                "heldout_confounded_oos_abstained": 2,
                                "heldout_confounded_oos_total": 2,
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )
            sufficiency.write_text(
                json.dumps(
                    {
                        "counts": {
                            "candidate_ids_requested": 10,
                            "score_complete_rows": 9,
                        },
                        "decision": {
                            "research_surface_sufficient": True,
                            "production_surface_sufficient": False,
                        },
                    }
                ),
                encoding="utf-8",
            )
            clearance.write_text(
                json.dumps(
                    {
                        "counts": {
                            "remaining_blocker_rows": 1,
                            "rows_with_fold_only_evidence": 1,
                        },
                        "row_attempts": [
                            {
                                "entry_id": "m_csa:78",
                                "current_blocker": "alphafold_db_coordinate_unavailable",
                                "fold_only_evidence_available": True,
                                "clearance_result": "blocked",
                                "next_action": "source an alternate accession",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_fold_augmented_confounded_deployment_closure_audit(
                predicted_structure_fold_channel_path=fold_channel,
                contract_audit_path=contract,
                oos_calibrated_threshold_contract_path=threshold,
                sufficiency_decision_path=sufficiency,
                remaining_blocker_clearance_path=clearance,
            )

        self.assertEqual(
            audit["status"],
            "confounded_fold_channel_research_ready_production_blocked",
        )
        self.assertTrue(
            audit["decision"]["confounded_subset_target_met_for_research"]
        )
        self.assertFalse(audit["decision"]["deployable_without_production_caveat"])
        self.assertEqual(audit["counts"]["critical_violation_total"], 1)
        self.assertEqual(
            audit["counts"]["remaining_production_blocker_rows"],
            1,
        )
        self.assertEqual(
            audit["predicted_structure_vs_atlas_contract"]["confounded_entry_ids"],
            ["m_csa:30", "m_csa:31"],
        )
        self.assertFalse(audit["guardrails"]["threshold_selected_or_tuned"])

    def test_fold_only_deployment_contract_rejects_fixed_threshold_escape_hatch(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            threshold = root / "threshold.json"
            fold_only = root / "fold_only.json"
            closure = root / "closure.json"
            threshold.write_text(
                json.dumps(
                    {
                        "threshold_contract": {
                            "fold_nearest_atlas_tm_score": {
                                "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain": {
                                    "threshold": 0.4
                                },
                                "selected_at_85pct_calibration_in_scope_retention_max_oos_abstain": {
                                    "threshold": 0.45
                                },
                                "heldout_final_eval_at_90pct_oos_calibrated_threshold": {
                                    "heldout_in_scope_retain_recall": 0.95,
                                    "heldout_confounded_oos_abstain_recall": 0.3333,
                                },
                                "heldout_final_eval_at_85pct_oos_calibrated_threshold": {
                                    "heldout_in_scope_retain_recall": 0.9,
                                    "heldout_confounded_oos_abstain_recall": 0.3333,
                                },
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            fold_only.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:204",
                                "accession": "P10746",
                                "nearest_train_atlas_entry_id": "m_csa:337",
                                "nearest_train_atlas_tm_score": 0.5,
                                "predicted_geometry_status": "missing",
                            },
                            {
                                "entry_id": "uniprot:P78549",
                                "accession": "P78549",
                                "nearest_train_atlas_entry_id": "m_csa:83",
                                "nearest_train_atlas_tm_score": 0.3,
                                "predicted_geometry_status": "missing",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            closure.write_text(
                json.dumps({"counts": {"remaining_production_blocker_rows": 2}}),
                encoding="utf-8",
            )

            audit = build_fold_augmented_fold_only_deployment_contract_decision(
                oos_calibrated_threshold_contract_path=threshold,
                fold_only_surface_path=fold_only,
                confounded_deployment_closure_path=closure,
            )

        self.assertEqual(
            audit["status"],
            "fold_only_deployment_contract_no_go_fixed_threshold_insufficient",
        )
        self.assertFalse(
            audit["decision"]["fold_only_deployment_contract_authorized"]
        )
        self.assertEqual(
            audit["counts"]["fold_only_rows_abstained_at_90pct_threshold"],
            1,
        )
        self.assertEqual(audit["counts"]["critical_violation_total"], 2)
        self.assertFalse(audit["guardrails"]["threshold_selected_or_tuned"])

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

    def test_row_specific_bond_change_schema_stages_required_queue(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest = root / "manifest.json"
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
                                "entry_id": "m_csa:2",
                                "accession": "P22222",
                                "fingerprint_id": None,
                                "split_assignment": "heldout",
                            },
                            {
                                "entry_id": "m_csa:3",
                                "accession": "P33333",
                                "fingerprint_id": "missing",
                                "split_assignment": "in_distribution",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            reaction_sidecar.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "status": "template_available",
                                "reaction_center_template": {
                                    "chemical_operation_normalized": "hydrolysis",
                                    "bond_changes_normalized": ["bond_broken"],
                                },
                            },
                            {
                                "entry_id": "m_csa:2",
                                "status": "no_mechanism_fingerprint_oos_or_unlabeled",
                                "reaction_center_template": {},
                            },
                            {
                                "entry_id": "m_csa:3",
                                "status": "fingerprint_template_missing",
                                "reaction_center_template": {},
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_schema(
                label_manifest_path=manifest,
                reaction_center_template_sidecar_path=reaction_sidecar,
            )

        self.assertEqual(
            audit["status"],
            "row_specific_bond_change_schema_staged_no_fit",
        )
        self.assertEqual(
            audit["counts"]["rows_requiring_row_specific_bond_change_evidence"],
            1,
        )
        self.assertIn(
            "proton_transfer",
            audit["schema_contract"]["allowed_event_types"],
        )
        required_row = audit["row_materialization_queue"][0]
        self.assertEqual(required_row["entry_id"], "m_csa:1")
        self.assertFalse(required_row["ready_for_embedding_pilot"])
        self.assertIn(
            "row_specific_reaction_participant_mapping",
            required_row["required_next_evidence"],
        )

    def test_row_specific_bond_change_gap_audit_excludes_contract_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            schema = root / "schema.json"
            contract = root / "contract.json"
            strict = root / "strict.json"
            schema.write_text(
                json.dumps(
                    {
                        "counts": {
                            "manifest_rows": 3,
                            "rows_requiring_row_specific_bond_change_evidence": 1,
                        }
                    }
                ),
                encoding="utf-8",
            )
            contract.write_text(
                json.dumps(
                    {
                        "feature_groups": [{"name": "reaction_center_template"}],
                        "feature_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "assigned_embedding_split": "train",
                                "feature_guardrails": {"heldout_row": False},
                                "reaction_center_template": {"status": "template_available"},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            strict.write_text(
                json.dumps({"counts": {"critical_violation_total": 0}}),
                encoding="utf-8",
            )

            audit = (
                build_mechanism_feature_row_specific_bond_change_feature_contract_gap_audit(
                    row_specific_bond_change_schema_path=schema,
                    feature_contract_path=contract,
                    feature_contract_strict_audit_path=strict,
                )
            )

        self.assertEqual(
            audit["status"],
            "row_specific_bond_change_gap_not_consumed_by_feature_contract",
        )
        self.assertEqual(audit["counts"]["feature_contract_rows"], 1)
        self.assertEqual(audit["counts"]["unexpected_bond_change_feature_rows"], 0)
        self.assertEqual(audit["counts"]["heldout_feature_rows"], 0)
        self.assertEqual(audit["counts"]["strict_audit_critical_violation_total"], 0)

    def test_row_specific_bond_change_materialization_priority_splits_p0_p1_p2(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            schema = root / "schema.json"
            contract = root / "contract.json"
            split = root / "split.json"
            schema.write_text(
                json.dumps(
                    {
                        "schema_contract": {
                            "forbidden_predictive_fields": ["label_type"]
                        },
                        "row_materialization_queue": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "split_assignment": "in_distribution",
                                "fingerprint_id": "fp_a",
                                "row_specific_bond_change_status": (
                                    "row_specific_bond_change_evidence_required"
                                ),
                                "template_chemical_operation_normalized": "hydrolysis",
                                "required_next_evidence": ["source_record_id"],
                            },
                            {
                                "entry_id": "m_csa:2",
                                "accession": "P22222",
                                "split_assignment": "in_distribution",
                                "fingerprint_id": "fp_b",
                                "row_specific_bond_change_status": (
                                    "row_specific_bond_change_evidence_required"
                                ),
                                "template_chemical_operation_normalized": "redox",
                                "required_next_evidence": ["source_record_id"],
                            },
                            {
                                "entry_id": "m_csa:3",
                                "accession": "P33333",
                                "split_assignment": "heldout",
                                "fingerprint_id": "fp_c",
                                "row_specific_bond_change_status": (
                                    "row_specific_bond_change_evidence_required"
                                ),
                                "template_chemical_operation_normalized": "radical",
                                "required_next_evidence": ["source_record_id"],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            contract.write_text(
                json.dumps({"feature_rows": [{"entry_id": "m_csa:1"}]}),
                encoding="utf-8",
            )
            split.write_text(
                json.dumps(
                    {
                        "split_records": [
                            {
                                "entry_id": "m_csa:1",
                                "assigned_embedding_split": "train",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_materialization_priority(
                row_specific_bond_change_schema_path=schema,
                feature_contract_path=contract,
                split_manifest_path=split,
            )

        self.assertEqual(
            audit["status"],
            "row_specific_bond_change_materialization_priority_ready_no_fit",
        )
        self.assertEqual(audit["counts"]["train_cal_feature_contract_gap_rows"], 1)
        self.assertEqual(
            audit["counts"]["in_distribution_not_feature_contract_ready_rows"],
            1,
        )
        self.assertEqual(audit["counts"]["heldout_final_only_gap_rows"], 1)
        self.assertEqual(audit["counts"]["balanced_pilot_seed_rows"], 1)
        self.assertFalse(audit["guardrails"]["row_specific_source_evidence_materialized"])
        self.assertFalse(
            audit["priority_rows"][0]["allowed_for_feature_contract_consumption_now"]
        )

    def test_row_specific_bond_change_p0_source_graph_readiness_blocks_unstructured_events(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            priority = root / "priority.json"
            graph = root / "graph.json"
            priority.write_text(
                json.dumps(
                    {
                        "balanced_pilot_seed_queue": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "fingerprint_id": "fp_a",
                                "assigned_embedding_split": "train",
                                "template_chemical_operation_normalized": "hydrolysis",
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
                            {"id": "m_csa:1", "type": "m_csa_entry", "name": "test"},
                            {"id": "ec:1.1.1.1", "type": "ec"},
                            {"id": "rhea:RHEA:1", "type": "rhea_reaction"},
                        ],
                        "edges": [
                            {
                                "source": "m_csa:1",
                                "target": "m_csa:1:residue:1",
                                "predicate": "has_catalytic_residue",
                            },
                            {
                                "source": "m_csa:1",
                                "target": "m_csa:1:mechanism:1",
                                "predicate": "has_mechanism_text",
                            },
                            {
                                "source": "m_csa:1",
                                "target": "ec:1.1.1.1",
                                "predicate": "has_ec",
                            },
                            {
                                "source": "ec:1.1.1.1",
                                "target": "rhea:RHEA:1",
                                "predicate": "maps_to_reaction",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_source_graph_readiness(
                materialization_priority_path=priority,
                graph_path=graph,
            )

        self.assertEqual(
            audit["status"],
            "p0_source_graph_context_ready_bond_events_not_structured",
        )
        self.assertEqual(audit["counts"]["balanced_p0_seed_rows"], 1)
        self.assertEqual(audit["counts"]["structured_bond_change_ready_rows"], 0)
        self.assertEqual(audit["counts"]["rhea_mapping_present_rows"], 1)
        self.assertIn(
            "structured_bond_change_events_missing",
            audit["row_readiness"][0]["blockers"],
        )
        self.assertFalse(audit["guardrails"]["row_specific_source_evidence_materialized"])

    def test_row_specific_bond_change_p0_extraction_package_templates_only(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readiness = root / "readiness.json"
            readiness.write_text(
                json.dumps(
                    {
                        "row_readiness": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "fingerprint_id": "fp_a",
                                "assigned_embedding_split": "train",
                                "template_chemical_operation_normalized": "hydrolysis",
                                "status": (
                                    "source_context_present_structured_"
                                    "bond_events_missing"
                                ),
                                "blockers": [
                                    "structured_bond_change_events_missing"
                                ],
                                "source_graph_evidence": {
                                    "m_csa_entry_name": "test",
                                    "ec_targets": ["ec:1.1.1.1"],
                                    "rhea_targets": ["rhea:RHEA:1"],
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_extraction_work_package(
                source_graph_readiness_path=readiness,
            )

        self.assertEqual(
            audit["status"],
            "p0_row_specific_bond_change_extraction_work_package_ready_manual_only",
        )
        self.assertEqual(audit["counts"]["p0_seed_rows"], 1)
        self.assertEqual(audit["counts"]["manual_extraction_rows"], 1)
        self.assertEqual(audit["counts"]["rows_with_rhea_targets"], 1)
        self.assertEqual(audit["counts"]["rows_requiring_rhea_lookup"], 0)
        self.assertFalse(audit["guardrails"]["row_specific_source_evidence_materialized"])
        self.assertFalse(
            audit["extraction_rows"][0]["allowed_for_feature_contract_consumption_now"]
        )
        self.assertIsNone(
            audit["extraction_rows"][0]["manual_extraction_template"][
                "row_specific_bond_change_events"
            ]
        )

    def test_row_specific_bond_change_p0_extraction_strict_audit_rejects_values(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            package = root / "package.json"
            template = {
                "source_record_id": None,
                "source_database": None,
                "source_record_version_or_date": None,
                "row_specific_reaction_participant_mapping": None,
                "row_specific_bond_change_events": [{"event_type": "bond_broken"}],
                "active_site_residue_role_support": None,
                "source_text_or_database_evidence_span": None,
                "extractor_id": None,
                "review_status": None,
            }
            package.write_text(
                json.dumps(
                    {
                        "required_fields": list(template),
                        "guardrails": {
                            "row_specific_source_evidence_materialized": False,
                            "feature_contract_mutated": False,
                            "manual_extraction_templates_only": True,
                        },
                        "extraction_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "manual_extraction_template": template,
                                "acceptance_criteria": [
                                    "a",
                                    "b",
                                    "c",
                                    "d",
                                    "e",
                                ],
                                "allowed_for_feature_contract_consumption_now": False,
                                "allowed_for_model_training_now": False,
                                "extraction_status": "manual_extraction_not_started",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_extraction_package_strict_audit(
                extraction_work_package_path=package,
            )

        self.assertEqual(
            audit["status"],
            "p0_extraction_work_package_strict_audit_failed",
        )
        self.assertEqual(
            audit["counts"]["violation_counts"],
            {"template_contains_materialized_values": 1},
        )
        self.assertEqual(audit["counts"]["critical_counts"]["row_template_violation_rows"], 1)
        self.assertFalse(audit["guardrails"]["row_specific_source_evidence_materialized"])

    def test_row_specific_bond_change_p0_source_evidence_sidecar_is_draft_only(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            worksheet = root / "worksheet.tsv"
            schema = root / "schema.json"
            graph = root / "graph.json"
            worksheet.write_text(
                "\t".join(
                    [
                        "entry_id",
                        "accession",
                    ]
                )
                + "\n"
                + "\t".join(["m_csa:1", "P11111"])
                + "\n",
                encoding="utf-8",
            )
            schema.write_text(
                json.dumps(
                    {
                        "sidecar_schema": {
                            "allowed_event_types": [
                                "bond_formed",
                                "bond_broken",
                                "bond_order_changed",
                                "proton_transfer",
                                "electron_transfer",
                            ],
                            "allowed_participant_roles": [
                                "substrate",
                                "product",
                                "cofactor",
                                "catalytic_residue",
                                "water",
                                "metal",
                                "other",
                            ],
                            "allowed_review_statuses": [
                                "draft",
                                "needs_more_evidence",
                                "approved",
                                "rejected",
                            ],
                            "forbidden_predictive_fields": [
                                "geometry_score",
                                "fold_score",
                            ],
                            "required_event_fields": [
                                "event_type",
                                "participants_before",
                                "participants_after",
                                "mapped_active_site_residues",
                                "source_evidence_span",
                                "confidence",
                            ],
                            "required_mapping_fields": [
                                "participant_id",
                                "role",
                                "source_identifier",
                                "mapped_atom_or_group",
                            ],
                            "required_row_fields": [
                                "entry_id",
                                "accession",
                                "source_record_id",
                                "source_database",
                                "source_record_version_or_date",
                                "row_specific_reaction_participant_mapping",
                                "row_specific_bond_change_events",
                                "active_site_residue_role_support",
                                "source_text_or_database_evidence_span",
                                "extractor_id",
                                "review_status",
                                "reviewer_id",
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"generated_at": "2026-06-01T00:00:00Z"},
                        "nodes": [
                            {"id": "m_csa:1", "type": "m_csa_entry"},
                            {
                                "id": "m_csa:1:mechanism:1",
                                "type": "mechanism_text",
                                "text": (
                                    "Serine attacks the scissile peptide bond. "
                                    "Histidine transfers a proton to the leaving group."
                                ),
                            },
                            {
                                "id": "m_csa:1:residue:1",
                                "type": "catalytic_residue",
                                "roles": ["nucleophile", "proton donor"],
                                "sequence_positions": [
                                    {
                                        "code": "Ser",
                                        "resid": 42,
                                        "uniprot_id": "P11111",
                                    }
                                ],
                            },
                            {
                                "id": "ec:3.4.1.1",
                                "type": "ec_number",
                            },
                            {
                                "id": "rhea:RHEA:1",
                                "type": "rhea_reaction",
                                "equation": "peptide + H2O = hydrolyzed peptide",
                            },
                        ],
                        "edges": [
                            {
                                "source": "m_csa:1",
                                "target": "m_csa:1:mechanism:1",
                                "predicate": "has_mechanism_text",
                            },
                            {
                                "source": "m_csa:1",
                                "target": "m_csa:1:residue:1",
                                "predicate": "has_catalytic_residue",
                            },
                            {
                                "source": "m_csa:1",
                                "target": "ec:3.4.1.1",
                                "predicate": "has_ec",
                            },
                            {
                                "source": "ec:3.4.1.1",
                                "target": "rhea:RHEA:1",
                                "predicate": "maps_to_reaction",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            sidecar = build_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar(
                worksheet_path=worksheet,
                source_evidence_schema_path=schema,
                graph_path=graph,
            )

        self.assertEqual(
            sidecar["status"],
            "p0_source_evidence_sidecar_draft_review_required",
        )
        self.assertEqual(sidecar["counts"]["sidecar_rows"], 1)
        self.assertEqual(sidecar["counts"]["rows_with_draft_bond_change_events"], 1)
        self.assertEqual(sidecar["counts"]["approved_rows"], 0)
        self.assertFalse(sidecar["guardrails"]["feature_contract_refresh_allowed"])
        row = sidecar["sidecar_rows"][0]
        self.assertEqual(row["review_status"], "draft")
        self.assertFalse(row["allowed_for_feature_contract_consumption_now"])
        self.assertIn(
            "bond_broken",
            {event["event_type"] for event in row["row_specific_bond_change_events"]},
        )

    def test_row_specific_bond_change_p0_source_evidence_strict_audit_blocks_consumption(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            worksheet = root / "worksheet.tsv"
            schema = root / "schema.json"
            sidecar = root / "sidecar.json"
            worksheet.write_text(
                "entry_id\taccession\nm_csa:1\tP11111\n",
                encoding="utf-8",
            )
            schema.write_text(
                json.dumps(
                    {
                        "sidecar_schema": {
                            "allowed_event_types": ["bond_formed"],
                            "allowed_participant_roles": [
                                "substrate",
                                "product",
                                "catalytic_residue",
                            ],
                            "allowed_review_statuses": [
                                "draft",
                                "approved",
                            ],
                            "forbidden_predictive_fields": ["geometry_score"],
                            "required_event_fields": [
                                "event_type",
                                "participants_before",
                                "participants_after",
                                "mapped_active_site_residues",
                                "source_evidence_span",
                                "confidence",
                            ],
                            "required_mapping_fields": [
                                "participant_id",
                                "role",
                                "source_identifier",
                                "mapped_atom_or_group",
                            ],
                            "required_row_fields": [
                                "entry_id",
                                "accession",
                                "source_record_id",
                                "source_database",
                                "source_record_version_or_date",
                                "row_specific_reaction_participant_mapping",
                                "row_specific_bond_change_events",
                                "active_site_residue_role_support",
                                "source_text_or_database_evidence_span",
                                "extractor_id",
                                "review_status",
                                "reviewer_id",
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )
            sidecar.write_text(
                json.dumps(
                    {
                        "guardrails": {"feature_contract_mutated": False},
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "source_record_id": "m_csa:1",
                                "source_database": "m_csa_local_graph",
                                "source_record_version_or_date": "2026-06-01",
                                "row_specific_reaction_participant_mapping": [
                                    {
                                        "participant_id": "substrate_1",
                                        "role": "substrate",
                                        "source_identifier": "rhea:RHEA:1",
                                        "mapped_atom_or_group": "peptide",
                                    }
                                ],
                                "row_specific_bond_change_events": [
                                    {
                                        "event_type": "bond_formed",
                                        "participants_before": ["peptide"],
                                        "participants_after": ["acyl-enzyme"],
                                        "mapped_active_site_residues": [
                                            "m_csa:1:residue:1"
                                        ],
                                        "source_evidence_span": {
                                            "source_record_id": "m_csa:1:mechanism:1",
                                            "span_text": "Serine attacks.",
                                        },
                                        "confidence": "medium",
                                    }
                                ],
                                "active_site_residue_role_support": [],
                                "source_text_or_database_evidence_span": [
                                    {
                                        "source_record_id": "m_csa:1:mechanism:1",
                                        "source_database": "m_csa_local_graph",
                                        "span_text": "Serine attacks.",
                                    }
                                ],
                                "extractor_id": "test",
                                "review_status": "draft",
                                "reviewer_id": None,
                                "allowed_for_feature_contract_consumption_now": False,
                                "allowed_for_model_training_now": False,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_strict_audit(
                sidecar_path=sidecar,
                source_evidence_schema_path=schema,
                worksheet_path=worksheet,
            )

        self.assertEqual(
            audit["status"],
            "p0_source_evidence_sidecar_strict_audit_passed_draft_not_consumable",
        )
        self.assertEqual(audit["counts"]["sidecar_rows"], 1)
        self.assertEqual(audit["counts"]["draft_rows"], 1)
        self.assertEqual(audit["counts"]["approved_rows"], 0)
        self.assertEqual(audit["counts"]["strict_audit_critical_violation_total"], 0)
        self.assertFalse(audit["counts"]["feature_contract_refresh_allowed"])

    def test_row_specific_bond_change_p0_source_evidence_strict_audit_requires_reviewer_for_approved_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            worksheet = root / "worksheet.tsv"
            schema = root / "schema.json"
            sidecar = root / "sidecar.json"
            worksheet.write_text(
                "entry_id\taccession\nm_csa:1\tP11111\n",
                encoding="utf-8",
            )
            schema.write_text(
                json.dumps(
                    {
                        "sidecar_schema": {
                            "allowed_event_types": ["bond_formed"],
                            "allowed_participant_roles": ["substrate"],
                            "allowed_review_statuses": ["draft", "approved"],
                            "forbidden_predictive_fields": [],
                            "required_event_fields": [
                                "event_type",
                                "participants_before",
                                "participants_after",
                                "mapped_active_site_residues",
                                "source_evidence_span",
                                "confidence",
                            ],
                            "required_mapping_fields": [
                                "participant_id",
                                "role",
                                "source_identifier",
                                "mapped_atom_or_group",
                            ],
                            "required_row_fields": [
                                "entry_id",
                                "accession",
                                "source_record_id",
                                "source_database",
                                "source_record_version_or_date",
                                "row_specific_reaction_participant_mapping",
                                "row_specific_bond_change_events",
                                "active_site_residue_role_support",
                                "source_text_or_database_evidence_span",
                                "extractor_id",
                                "review_status",
                                "reviewer_id",
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )
            sidecar.write_text(
                json.dumps(
                    {
                        "guardrails": {"feature_contract_mutated": False},
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "source_record_id": "m_csa:1",
                                "source_database": "m_csa_local_graph",
                                "source_record_version_or_date": "2026-06-01",
                                "row_specific_reaction_participant_mapping": [
                                    {
                                        "participant_id": "substrate_1",
                                        "role": "substrate",
                                        "source_identifier": "rhea:RHEA:1",
                                        "mapped_atom_or_group": "peptide",
                                    }
                                ],
                                "row_specific_bond_change_events": [
                                    {
                                        "event_type": "bond_formed",
                                        "participants_before": ["peptide"],
                                        "participants_after": ["product"],
                                        "mapped_active_site_residues": [
                                            "m_csa:1:residue:1"
                                        ],
                                        "source_evidence_span": {
                                            "source_record_id": "m_csa:1:mechanism:1",
                                            "span_text": "Serine attacks.",
                                        },
                                        "confidence": "medium",
                                    }
                                ],
                                "active_site_residue_role_support": [],
                                "source_text_or_database_evidence_span": [
                                    {
                                        "source_record_id": "m_csa:1:mechanism:1",
                                        "source_database": "m_csa_local_graph",
                                        "span_text": "Serine attacks.",
                                    }
                                ],
                                "extractor_id": "test",
                                "review_status": "approved",
                                "reviewer_id": None,
                                "allowed_for_feature_contract_consumption_now": False,
                                "allowed_for_model_training_now": False,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_strict_audit(
                sidecar_path=sidecar,
                source_evidence_schema_path=schema,
                worksheet_path=worksheet,
            )

        self.assertEqual(
            audit["status"],
            "p0_source_evidence_sidecar_strict_audit_failed",
        )
        self.assertEqual(
            audit["counts"]["critical_counts"]["approved_row_evidence_violation_rows"],
            1,
        )
        self.assertIn(
            "approved_row_reviewer_id_missing",
            audit["row_audits"][0]["violations"],
        )

    def test_row_specific_bond_change_p0_source_evidence_review_queue_prioritizes_blockers(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sidecar = root / "sidecar.json"
            strict = root / "strict.json"
            event = {
                "event_type": "bond_formed",
                "participants_before": ["substrate"],
                "participants_after": ["product"],
                "mapped_active_site_residues": ["m_csa:1:residue:1"],
                "source_evidence_span": {
                    "source_record_id": "m_csa:1:mechanism:1",
                    "span_text": "Serine attacks.",
                },
                "confidence": "medium",
            }
            sidecar.write_text(
                json.dumps(
                    {
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:2",
                                "accession": "P22222",
                                "review_status": "draft",
                                "row_specific_bond_change_events": [event] * 4,
                                "source_text_or_database_evidence_span": [
                                    {
                                        "source_database": "m_csa_local_graph",
                                        "span_text": "multi event",
                                    },
                                    {
                                        "source_database": "rhea_local_graph",
                                        "span_text": "reaction",
                                    },
                                ],
                                "allowed_for_feature_contract_consumption_now": False,
                                "allowed_for_model_training_now": False,
                            },
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "review_status": "draft",
                                "row_specific_bond_change_events": [event],
                                "source_text_or_database_evidence_span": [
                                    {
                                        "source_database": "m_csa_local_graph",
                                        "span_text": "single event",
                                    }
                                ],
                                "allowed_for_feature_contract_consumption_now": False,
                                "allowed_for_model_training_now": False,
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            strict.write_text(
                json.dumps(
                    {
                        "status": (
                            "p0_source_evidence_sidecar_strict_audit_"
                            "passed_draft_not_consumable"
                        )
                    }
                ),
                encoding="utf-8",
            )

            queue = build_mechanism_feature_row_specific_bond_change_p0_source_evidence_review_queue(
                sidecar_path=sidecar,
                strict_audit_path=strict,
            )

        self.assertEqual(
            queue["status"],
            "p0_source_evidence_review_queue_ready_manual_only",
        )
        self.assertEqual(queue["counts"]["queue_rows"], 2)
        self.assertEqual(
            queue["counts"]["category_counts"],
            {
                "high_complexity_multi_event_review": 1,
                "rhea_lookup_required_before_approval": 1,
            },
        )
        self.assertEqual(queue["queue_rows"][0]["entry_id"], "m_csa:1")
        self.assertEqual(
            queue["queue_rows"][0]["review_category"],
            "rhea_lookup_required_before_approval",
        )
        self.assertEqual(queue["counts"]["critical_violation_total"], 0)
        self.assertFalse(queue["guardrails"]["feature_contract_refresh_allowed"])

    def test_row_specific_bond_change_p0_source_evidence_review_queue_accepts_rhea_backed_approved_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sidecar = root / "sidecar.json"
            strict = root / "strict.json"
            event = {
                "event_type": "bond_order_changed",
                "participants_before": ["substrate"],
                "participants_after": ["product"],
                "mapped_active_site_residues": ["m_csa:147:residue:2"],
                "source_evidence_span": {
                    "source_record_id": "m_csa:147:mechanism:1",
                    "span_text": "The aldimine rearranges.",
                },
                "confidence": "medium",
            }
            sidecar.write_text(
                json.dumps(
                    {
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:147",
                                "accession": "P07511",
                                "review_status": "approved",
                                "reviewer_id": "reviewer",
                                "reviewer_decision": {
                                    "decision": "approve_rhea_backed_source_evidence",
                                },
                                "row_specific_bond_change_events": [event] * 4,
                                "source_text_or_database_evidence_span": [
                                    {
                                        "source_database": "m_csa_local_graph",
                                        "span_text": "multi-event mechanism",
                                    },
                                    {
                                        "source_database": "rhea_local_graph",
                                        "span_text": "reaction equation",
                                    },
                                ],
                                "allowed_for_feature_contract_consumption_now": True,
                                "allowed_for_model_training_now": False,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            strict.write_text(
                json.dumps(
                    {
                        "status": (
                            "p0_source_evidence_sidecar_strict_audit_"
                            "passed_reviewed_consumable"
                        )
                    }
                ),
                encoding="utf-8",
            )

            queue = build_mechanism_feature_row_specific_bond_change_p0_source_evidence_review_queue(
                sidecar_path=sidecar,
                strict_audit_path=strict,
            )

        self.assertEqual(
            queue["status"],
            "p0_source_evidence_review_queue_ready_manual_only",
        )
        self.assertEqual(queue["counts"]["critical_violation_total"], 0)
        self.assertEqual(queue["counts"]["approved_feature_contract_consumable_rows"], 1)
        self.assertEqual(queue["counts"]["unreviewed_feature_contract_consumable_rows"], 0)
        self.assertEqual(
            queue["queue_rows"][0]["review_category"],
            "approved_rhea_backed_source_evidence",
        )
        self.assertEqual(queue["queue_rows"][0]["blockers"], [])

    def test_row_specific_bond_change_p0_rhea_lookup_manifest_stages_missing_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            queue = root / "queue.json"
            readiness = root / "readiness.json"
            queue.write_text(
                json.dumps(
                    {
                        "status": "p0_source_evidence_review_queue_ready_manual_only",
                        "queue_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "review_category": (
                                    "rhea_lookup_required_before_approval"
                                ),
                                "priority_rank": 1,
                                "event_count": 3,
                                "allowed_for_feature_contract_consumption_now": False,
                            },
                            {
                                "entry_id": "m_csa:2",
                                "accession": "P22222",
                                "review_category": "standard_draft_event_review",
                                "priority_rank": 3,
                                "event_count": 1,
                                "allowed_for_feature_contract_consumption_now": False,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            readiness.write_text(
                json.dumps(
                    {
                        "row_readiness": [
                            {
                                "entry_id": "m_csa:1",
                                "source_graph_evidence": {
                                    "m_csa_entry_name": "test enzyme",
                                    "ec_targets": ["ec:1.2.3.4"],
                                    "rhea_targets": [],
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            manifest = build_mechanism_feature_row_specific_bond_change_p0_rhea_lookup_manifest(
                review_queue_path=queue,
                source_graph_readiness_path=readiness,
            )

        self.assertEqual(
            manifest["status"],
            "p0_rhea_lookup_manifest_ready_manual_only",
        )
        self.assertEqual(manifest["counts"]["rhea_lookup_rows"], 1)
        self.assertEqual(manifest["counts"]["rows_with_ec_targets"], 1)
        self.assertEqual(manifest["counts"]["lookup_target_count"], 1)
        self.assertEqual(manifest["lookup_rows"][0]["entry_id"], "m_csa:1")
        self.assertEqual(
            manifest["lookup_rows"][0]["lookup_targets"][0]["rhea_query_url"],
            "https://www.rhea-db.org/rhea?query=1.2.3.4",
        )
        self.assertEqual(manifest["counts"]["critical_violation_total"], 0)
        self.assertFalse(manifest["guardrails"]["source_fetch_performed"])

    def test_row_specific_bond_change_p0_rhea_lookup_resolution_feeds_sidecar(
        self,
    ) -> None:
        def fake_fetch(query: str) -> str:
            header = "Reaction identifier\tEquation\tEC number\tEnzymes\n"
            if query == "uniprot:P00396":
                return (
                    header
                    + "RHEA:11436\t4 Fe(II)-[cytochrome c] + O2 + "
                    "8 H(+)(in) = 4 Fe(III)-[cytochrome c] + 2 H2O + "
                    "4 H(+)(out)\tEC:7.1.1.9\t1870579\n"
                )
            return header

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest = root / "manifest.json"
            resolution_path = root / "resolution.json"
            worksheet = root / "worksheet.tsv"
            schema = root / "schema.json"
            graph = root / "graph.json"
            manifest.write_text(
                json.dumps(
                    {
                        "lookup_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P00396",
                                "m_csa_entry_name": "cytochrome oxidase",
                                "draft_event_count": 2,
                                "lookup_blockers": ["rhea_equation_missing"],
                                "ec_targets": ["ec:1.9.3.1"],
                            },
                            {
                                "entry_id": "m_csa:2",
                                "accession": "P0A6C1",
                                "m_csa_entry_name": "nuclease",
                                "draft_event_count": 1,
                                "lookup_blockers": ["rhea_equation_missing"],
                                "ec_targets": ["ec:3.1.21.2"],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            resolution = build_mechanism_feature_row_specific_bond_change_p0_rhea_lookup_resolution(
                rhea_lookup_manifest_path=manifest,
                fetcher=fake_fetch,
            )
            resolution_path.write_text(json.dumps(resolution), encoding="utf-8")
            worksheet.write_text(
                "entry_id\taccession\nm_csa:1\tP00396\n",
                encoding="utf-8",
            )
            schema.write_text(
                json.dumps(
                    {
                        "sidecar_schema": {
                            "allowed_event_types": [
                                "bond_formed",
                                "bond_broken",
                                "bond_order_changed",
                                "proton_transfer",
                                "electron_transfer",
                            ],
                            "allowed_participant_roles": [
                                "substrate",
                                "product",
                                "cofactor",
                                "catalytic_residue",
                                "water",
                                "metal",
                                "other",
                            ],
                            "allowed_review_statuses": ["draft"],
                            "forbidden_predictive_fields": [],
                            "required_event_fields": [
                                "event_type",
                                "participants_before",
                                "participants_after",
                                "mapped_active_site_residues",
                                "source_evidence_span",
                                "confidence",
                            ],
                            "required_mapping_fields": [
                                "participant_id",
                                "role",
                                "source_identifier",
                                "mapped_atom_or_group",
                            ],
                            "required_row_fields": [
                                "entry_id",
                                "accession",
                                "source_record_id",
                                "source_database",
                                "source_record_version_or_date",
                                "row_specific_reaction_participant_mapping",
                                "row_specific_bond_change_events",
                                "active_site_residue_role_support",
                                "source_text_or_database_evidence_span",
                                "extractor_id",
                                "review_status",
                                "reviewer_id",
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"generated_at": "2026-06-01T00:00:00Z"},
                        "nodes": [
                            {"id": "m_csa:1", "type": "m_csa_entry"},
                            {
                                "id": "m_csa:1:mechanism:1",
                                "type": "mechanism_text",
                                "text": "Cytochrome oxidase transfers electrons and pumps protons.",
                            },
                        ],
                        "edges": [
                            {
                                "source": "m_csa:1",
                                "target": "m_csa:1:mechanism:1",
                                "predicate": "has_mechanism_text",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            sidecar = build_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar(
                worksheet_path=worksheet,
                source_evidence_schema_path=schema,
                graph_path=graph,
                rhea_lookup_resolution_path=resolution_path,
            )

        self.assertEqual(
            resolution["status"],
            "p0_rhea_lookup_resolution_partial_review_only",
        )
        self.assertEqual(resolution["counts"]["resolved_rows"], 1)
        self.assertEqual(resolution["counts"]["resolved_by_accession_rows"], 1)
        self.assertEqual(resolution["counts"]["unresolved_rows"], 1)
        self.assertEqual(sidecar["counts"]["rows_with_rhea_equations"], 1)
        self.assertEqual(sidecar["counts"]["rows_missing_rhea_equations"], 0)
        span_databases = {
            span["source_database"]
            for span in sidecar["sidecar_rows"][0]["source_text_or_database_evidence_span"]
        }
        self.assertIn("rhea_official_lookup", span_databases)

    def test_row_specific_bond_change_p0_rhea_resolution_consumption_audit_passes(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            resolution = root / "resolution.json"
            sidecar = root / "sidecar.json"
            queue = root / "queue.json"
            manifest = root / "manifest.json"
            readiness = root / "readiness.json"
            resolution.write_text(
                json.dumps(
                    {
                        "row_resolutions": [
                            {
                                "entry_id": "m_csa:1",
                                "accepted_resolution": {
                                    "status": "resolved_accession_query",
                                    "rhea_id": "RHEA:1",
                                },
                            },
                            {
                                "entry_id": "m_csa:2",
                                "accepted_resolution": {
                                    "status": (
                                        "unresolved_no_rhea_record_for_ec_or_accession"
                                    ),
                                    "rhea_id": None,
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            sidecar.write_text(
                json.dumps(
                    {
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "review_status": "draft",
                                "source_text_or_database_evidence_span": [
                                    {
                                        "source_database": "rhea_official_lookup",
                                        "source_record_id": "rhea:RHEA:1",
                                    }
                                ],
                                "allowed_for_feature_contract_consumption_now": False,
                                "allowed_for_model_training_now": False,
                            },
                            {
                                "entry_id": "m_csa:2",
                                "review_status": "draft",
                                "source_text_or_database_evidence_span": [],
                                "allowed_for_feature_contract_consumption_now": False,
                                "allowed_for_model_training_now": False,
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps(
                    {
                        "queue_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "review_category": "high_complexity_multi_event_review",
                            },
                            {
                                "entry_id": "m_csa:2",
                                "review_category": "rhea_lookup_required_before_approval",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            manifest.write_text(
                json.dumps({"lookup_rows": [{"entry_id": "m_csa:2"}]}),
                encoding="utf-8",
            )
            readiness.write_text(
                json.dumps(
                    {
                        "row_readiness": [
                            {"entry_id": "m_csa:1", "blockers": []},
                            {
                                "entry_id": "m_csa:2",
                                "blockers": ["rhea_lookup_unresolved"],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_rhea_resolution_consumption_audit(
                rhea_lookup_resolution_path=resolution,
                sidecar_path=sidecar,
                review_queue_path=queue,
                rhea_lookup_manifest_path=manifest,
                feature_readiness_path=readiness,
            )

        self.assertEqual(
            audit["status"],
            "p0_rhea_resolution_consumption_audit_passed_review_only",
        )
        self.assertEqual(audit["counts"]["resolved_rows"], 1)
        self.assertEqual(audit["counts"]["unresolved_rows"], 1)
        self.assertEqual(audit["counts"]["critical_violation_total"], 0)
        self.assertFalse(audit["guardrails"]["feature_contract_refresh_allowed"])

    def test_row_specific_bond_change_p0_rhea_unresolved_official_source_audit_blocks_without_rhea(
        self,
    ) -> None:
        def fake_rhea_fetch(query: str) -> str:
            return "Reaction identifier\tEquation\tEC number\tEnzymes\n"

        def fake_uniprot_fetch(accession: str) -> dict[str, object]:
            return {
                "primaryAccession": accession,
                "uniProtkbId": "TEST_HUMAN",
                "entryAudit": {"lastAnnotationUpdateDate": "2026-01-28"},
                "proteinDescription": {
                    "recommendedName": {
                        "fullName": {"value": "Test peptidase"},
                        "ecNumbers": [{"value": "3.4.14.5"}],
                    }
                },
                "comments": [
                    {
                        "commentType": "CATALYTIC ACTIVITY",
                        "reaction": {
                            "name": "Release of an N-terminal dipeptide.",
                            "ecNumber": "3.4.14.5",
                        },
                    }
                ],
            }

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest = root / "manifest.json"
            resolution = root / "resolution.json"
            manifest.write_text(
                json.dumps(
                    {
                        "lookup_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P27487",
                                "m_csa_entry_name": "dipeptidyl peptidase",
                                "ec_targets": ["ec:3.4.14.5"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            resolution.write_text(
                json.dumps(
                    {
                        "row_resolutions": [
                            {
                                "entry_id": "m_csa:1",
                                "accepted_resolution": {
                                    "status": (
                                        "unresolved_no_rhea_record_for_ec_or_accession"
                                    ),
                                    "rhea_id": None,
                                },
                            },
                            {
                                "entry_id": "m_csa:2",
                                "accepted_resolution": {
                                    "status": "resolved_accession_query",
                                    "rhea_id": "RHEA:1",
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_rhea_unresolved_official_source_audit(
                rhea_lookup_manifest_path=manifest,
                rhea_lookup_resolution_path=resolution,
                rhea_fetcher=fake_rhea_fetch,
                uniprot_fetcher=fake_uniprot_fetch,
            )

        self.assertEqual(
            audit["status"],
            "p0_rhea_unresolved_official_source_audit_ready_review_only",
        )
        self.assertEqual(audit["counts"]["manifest_rows_audited"], 1)
        self.assertEqual(audit["counts"]["rhea_query_attempts"], 3)
        self.assertEqual(audit["counts"]["rows_with_official_rhea_evidence_found"], 0)
        self.assertEqual(audit["counts"]["rows_with_uniprot_matching_ec_activity"], 1)
        self.assertEqual(audit["counts"]["unresolved_after_official_source_check"], 1)
        self.assertEqual(audit["counts"]["feature_contract_consumable_rows"], 0)
        self.assertEqual(
            audit["row_audits"][0]["status"],
            "official_ec_activity_present_without_rhea_cross_reference",
        )
        self.assertTrue(audit["row_audits"][0]["reviewer_decision_required"])
        self.assertFalse(audit["guardrails"]["feature_contract_refresh_allowed"])

    def test_row_specific_bond_change_p0_reviewer_decision_matrix_stages_options(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            official = root / "official.json"
            sidecar = root / "sidecar.json"
            readiness = root / "readiness.json"
            official.write_text(
                json.dumps(
                    {
                        "row_audits": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P27487",
                                "m_csa_entry_name": "dipeptidyl peptidase",
                                "status": (
                                    "official_ec_activity_present_without_rhea_cross_reference"
                                ),
                                "ec_targets": ["ec:3.4.14.5"],
                                "official_rhea_evidence_found": False,
                                "uniprot_query": {
                                    "matching_ec_catalytic_activities": [
                                        {"ec_number": "3.4.14.5"}
                                    ]
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
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "review_status": "draft",
                                "reviewer_id": None,
                                "row_specific_bond_change_events": [
                                    {
                                        "event_type": "bond_broken",
                                        "confidence": "medium",
                                        "mapped_active_site_residues": [
                                            "m_csa:1:residue:1"
                                        ],
                                        "source_evidence_span": {
                                            "source_record_id": "m_csa:1:mechanism:1"
                                        },
                                    }
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            readiness.write_text(
                json.dumps(
                    {
                        "row_readiness": [
                            {
                                "entry_id": "m_csa:1",
                                "blockers": [
                                    "reviewer_id_missing",
                                    "rhea_lookup_unresolved",
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            matrix = build_mechanism_feature_row_specific_bond_change_p0_reviewer_decision_matrix(
                unresolved_official_source_audit_path=official,
                sidecar_path=sidecar,
                feature_readiness_path=readiness,
            )

        self.assertEqual(
            matrix["status"],
            "p0_reviewer_decision_matrix_ready_review_only",
        )
        self.assertEqual(matrix["counts"]["decision_rows"], 1)
        self.assertEqual(matrix["counts"]["decision_options_per_row"], 3)
        self.assertEqual(matrix["counts"]["feature_contract_consumable_rows"], 0)
        self.assertEqual(matrix["decision_rows"][0]["event_count"], 1)
        self.assertIn(
            "rhea_lookup_unresolved",
            matrix["decision_rows"][0]["readiness_blockers"],
        )
        self.assertFalse(
            matrix["decision_rows"][0]["copy_ready_approved_decision_present"]
        )
        self.assertFalse(matrix["guardrails"]["reviewer_decision_recorded_by_this_artifact"])

    def test_row_specific_bond_change_p0_feature_readiness_blocks_draft_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sidecar = root / "sidecar.json"
            strict = root / "strict.json"
            queue = root / "queue.json"
            rhea = root / "rhea.json"
            contract = root / "contract.json"
            sidecar.write_text(
                json.dumps(
                    {
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "review_status": "draft",
                                "reviewer_id": None,
                                "row_specific_reaction_participant_mapping": [
                                    {"participant_id": "substrate_1"}
                                ],
                                "row_specific_bond_change_events": [
                                    {"event_type": "bond_formed"},
                                    {"event_type": "proton_transfer"},
                                    {"event_type": "electron_transfer"},
                                ],
                                "source_text_or_database_evidence_span": [
                                    {"source_database": "m_csa_local_graph"}
                                ],
                                "allowed_for_feature_contract_consumption_now": False,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            strict.write_text(
                json.dumps(
                    {
                        "status": (
                            "p0_source_evidence_sidecar_strict_audit_"
                            "passed_draft_not_consumable"
                        )
                    }
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps(
                    {
                        "status": "p0_source_evidence_review_queue_ready_manual_only",
                        "queue_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "blockers": ["review_status_not_approved"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            rhea.write_text(
                json.dumps(
                    {
                        "status": "p0_rhea_lookup_manifest_ready_manual_only",
                        "lookup_rows": [],
                    }
                ),
                encoding="utf-8",
            )
            contract.write_text(json.dumps({"feature_rows": []}), encoding="utf-8")

            audit = build_mechanism_feature_row_specific_bond_change_p0_feature_readiness_audit(
                sidecar_path=sidecar,
                strict_audit_path=strict,
                review_queue_path=queue,
                rhea_lookup_manifest_path=rhea,
                feature_contract_path=contract,
            )

        self.assertEqual(
            audit["status"],
            "p0_feature_readiness_audit_blocked_review_required",
        )
        self.assertEqual(audit["counts"]["sidecar_rows"], 1)
        self.assertEqual(audit["counts"]["structurally_ready_draft_rows"], 1)
        self.assertEqual(audit["counts"]["approved_consumable_rows"], 0)
        self.assertEqual(audit["counts"]["rows_with_bond_change_event"], 1)
        self.assertEqual(audit["counts"]["rows_with_proton_transfer_event"], 1)
        self.assertEqual(audit["counts"]["rows_with_electron_transfer_event"], 1)
        self.assertFalse(audit["counts"]["feature_contract_refresh_allowed"])
        self.assertFalse(audit["guardrails"]["feature_contract_mutated"])
        self.assertIn("reviewer_id_missing", audit["row_readiness"][0]["blockers"])

    def test_row_specific_bond_change_p0_refresh_blocker_blocks_drafts(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            strict = root / "strict.json"
            readiness = root / "readiness.json"
            rhea_consumption = root / "rhea_consumption.json"
            unresolved = root / "unresolved.json"
            matrix = root / "matrix.json"
            gap = root / "gap.json"
            strict.write_text(
                json.dumps(
                    {
                        "status": (
                            "p0_source_evidence_sidecar_strict_audit_"
                            "passed_draft_not_consumable"
                        ),
                        "counts": {"strict_audit_critical_violation_total": 0},
                    }
                ),
                encoding="utf-8",
            )
            readiness.write_text(
                json.dumps(
                    {
                        "status": "p0_feature_readiness_audit_blocked_review_required",
                        "counts": {
                            "sidecar_rows": 1,
                            "structurally_ready_draft_rows": 1,
                            "approved_consumable_rows": 0,
                            "feature_contract_refresh_allowed": False,
                            "critical_violation_total": 0,
                            "blocker_counts": {
                                "reviewer_id_missing": 1,
                                "rhea_lookup_unresolved": 1,
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )
            rhea_consumption.write_text(
                json.dumps(
                    {
                        "status": "p0_rhea_resolution_consumption_audit_passed_review_only",
                        "counts": {
                            "critical_violation_total": 0,
                            "unresolved_rows": 1,
                        },
                    }
                ),
                encoding="utf-8",
            )
            unresolved.write_text(
                json.dumps(
                    {
                        "status": "p0_rhea_unresolved_official_source_audit_ready_review_only",
                        "counts": {"reviewer_decision_required_rows": 1},
                    }
                ),
                encoding="utf-8",
            )
            matrix.write_text(
                json.dumps(
                    {
                        "status": "p0_reviewer_decision_matrix_ready_review_only",
                        "counts": {
                            "decision_rows": 1,
                            "copy_ready_approved_decisions": 0,
                            "rows_with_existing_reviewer_id": 0,
                            "feature_contract_consumable_rows": 0,
                        },
                        "decision_rows": [
                            {
                                "entry_id": "m_csa:11",
                                "accession": "P0A6C1",
                                "review_status": "draft",
                                "reviewer_id": None,
                                "official_source_status": (
                                    "official_ec_activity_present_without_rhea_cross_reference"
                                ),
                                "copy_ready_approved_decision_present": False,
                                "readiness_blockers": [
                                    "reviewer_id_missing",
                                    "rhea_lookup_unresolved",
                                ],
                                "decision_options": [
                                    {"decision": "approve_m_csa_only_source_evidence"}
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            gap.write_text(
                json.dumps(
                    {
                        "status": (
                            "row_specific_bond_change_gap_not_consumed_by_feature_contract"
                        ),
                        "counts": {
                            "strict_audit_critical_violation_total": 0,
                            "unexpected_bond_change_feature_rows": 0,
                        },
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_refresh_blocker_audit(
                strict_audit_path=strict,
                feature_readiness_path=readiness,
                rhea_resolution_consumption_audit_path=rhea_consumption,
                unresolved_official_source_audit_path=unresolved,
                reviewer_decision_matrix_path=matrix,
                feature_contract_gap_audit_path=gap,
            )

        self.assertEqual(
            audit["status"],
            "p0_no_template_feature_refresh_blocked_review_required",
        )
        self.assertFalse(
            audit["decision"]["automation_feature_contract_refresh_allowed"]
        )
        self.assertEqual(audit["counts"]["approved_consumable_rows"], 0)
        self.assertEqual(audit["counts"]["reviewer_decision_required_rows"], 1)
        self.assertEqual(audit["counts"]["copy_ready_approved_decisions"], 0)
        self.assertEqual(audit["unresolved_decision_rows"][0]["entry_id"], "m_csa:11")
        self.assertIn(
            "build-mechanism-feature-embedding-pilot from draft sidecar rows",
            audit["decision"]["do_not_run"],
        )

    def test_row_specific_bond_change_p0_train_cal_feature_sidecar_filters_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sidecar_path = root / "sidecar.json"
            readiness_path = root / "readiness.json"
            split_path = root / "split.json"
            contract_path = root / "contract.json"
            label_manifest_path = root / "label_manifest.json"

            event = {
                "event_type": "bond_broken",
                "confidence": "medium",
                "mapped_active_site_residues": ["m_csa:5:residue:1"],
                "source_evidence_span": {
                    "source_record_id": "m_csa:5:mechanism:1",
                    "span_text": "mechanism text should not travel",
                },
            }
            proton_event = {
                "event_type": "proton_transfer",
                "confidence": "low",
                "mapped_active_site_residues": ["m_csa:5:residue:2"],
                "source_evidence_span": {
                    "source_record_id": "m_csa:5:mechanism:1",
                    "span_text": "proton source text should not travel",
                },
            }
            sidecar_path.write_text(
                json.dumps(
                    {
                        "status": (
                            "p0_source_evidence_sidecar_partially_approved_review_required"
                        ),
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:5",
                                "review_status": "approved",
                                "reviewer_id": "reviewer",
                                "allowed_for_feature_contract_consumption_now": True,
                                "row_specific_bond_change_events": [
                                    event,
                                    proton_event,
                                ],
                            },
                            {
                                "entry_id": "m_csa:6",
                                "review_status": "draft",
                                "reviewer_id": None,
                                "allowed_for_feature_contract_consumption_now": False,
                                "row_specific_bond_change_events": [event],
                            },
                            {
                                "entry_id": "m_csa:999",
                                "review_status": "approved",
                                "reviewer_id": "reviewer",
                                "allowed_for_feature_contract_consumption_now": True,
                                "row_specific_bond_change_events": [event],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            readiness_path.write_text(
                json.dumps(
                    {
                        "status": "p0_feature_readiness_audit_blocked_review_required",
                        "row_readiness": [
                            {
                                "entry_id": "m_csa:5",
                                "approved_and_consumable": True,
                            },
                            {
                                "entry_id": "m_csa:999",
                                "approved_and_consumable": True,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            split_path.write_text(
                json.dumps(
                    {
                        "status": (
                            "mechanism_feature_embedding_train_cal_split_ready_no_model_fit"
                        ),
                        "split_records": [
                            {
                                "entry_id": "m_csa:5",
                                "assigned_embedding_split": "train",
                            },
                            {
                                "entry_id": "m_csa:999",
                                "assigned_embedding_split": "train",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            contract_path.write_text(
                json.dumps(
                    {
                        "status": (
                            "mechanism_feature_embedding_feature_contract_ready_no_model_fit"
                        ),
                        "feature_rows": [
                            {
                                "entry_id": "m_csa:5",
                                "feature_guardrails": {"heldout_row": False},
                            },
                            {
                                "entry_id": "m_csa:999",
                                "feature_guardrails": {"heldout_row": False},
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            label_manifest_path.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:5",
                                "split_assignment": "in_distribution",
                            },
                            {
                                "entry_id": "m_csa:6",
                                "split_assignment": "in_distribution",
                            },
                            {
                                "entry_id": "m_csa:999",
                                "split_assignment": "heldout",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            sidecar = build_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_sidecar(
                source_sidecar_path=sidecar_path,
                feature_readiness_path=readiness_path,
                train_cal_split_manifest_path=split_path,
                feature_contract_path=contract_path,
                label_manifest_path=label_manifest_path,
            )

        self.assertEqual(
            sidecar["status"],
            "p0_train_cal_row_specific_feature_sidecar_ready_partial_no_fit",
        )
        self.assertEqual(sidecar["counts"]["materialized_feature_rows"], 1)
        self.assertEqual(sidecar["counts"]["draft_rows_excluded"], 1)
        self.assertEqual(sidecar["counts"]["heldout_approved_rows_excluded"], 1)
        self.assertEqual(
            sidecar["counts"]["materialized_event_type_counts"],
            {"bond_broken": 1, "proton_transfer": 1},
        )
        self.assertEqual(sidecar["feature_rows"][0]["entry_id"], "m_csa:5")
        features = sidecar["feature_rows"][0]["row_specific_event_features"]
        self.assertEqual(features["bond_change_event_count"], 1)
        self.assertEqual(features["proton_transfer_count"], 1)
        self.assertEqual(features["unique_mapped_active_site_residue_count"], 2)
        feature_rows_text = json.dumps(sidecar["feature_rows"])
        self.assertNotIn("mechanism text should not travel", feature_rows_text)
        self.assertNotIn("source_record_id", feature_rows_text)
        self.assertFalse(sidecar["guardrails"]["model_weights_fit_or_refit"])
        self.assertFalse(
            sidecar["decision"][
                "full_no_template_centroid_or_residual_rerun_ready"
            ]
        )

    def test_row_specific_bond_change_p0_train_cal_coverage_gap_prioritizes_calibration(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            feature_sidecar_path = root / "feature_sidecar.json"
            source_sidecar_path = root / "source_sidecar.json"
            review_queue_path = root / "review_queue.json"
            split_path = root / "split.json"
            label_manifest_path = root / "label_manifest.json"
            feature_sidecar_path.write_text(
                json.dumps(
                    {
                        "decision": {
                            "full_no_template_centroid_or_residual_rerun_ready": False
                        },
                        "counts": {
                            "materialized_feature_rows": 1,
                            "train_rows": 1,
                            "calibration_rows": 0,
                            "materialized_event_type_counts": {
                                "bond_broken": 1,
                            },
                            "critical_violation_total": 0,
                            "critical_counts": {
                                "materialized_heldout_rows": 0,
                                "materialized_draft_rows": 0,
                            },
                        },
                        "feature_rows": [
                            {
                                "entry_id": "m_csa:5",
                                "assigned_embedding_split": "train",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            source_sidecar_path.write_text(
                json.dumps(
                    {
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:5",
                                "review_status": "approved",
                                "row_specific_bond_change_events": [
                                    {"event_type": "bond_broken"}
                                ],
                            },
                            {
                                "entry_id": "m_csa:6",
                                "review_status": "draft",
                                "row_specific_bond_change_events": [
                                    {"event_type": "proton_transfer"},
                                    {"event_type": "bond_order_changed"},
                                ],
                            },
                            {
                                "entry_id": "m_csa:7",
                                "review_status": "draft",
                                "row_specific_bond_change_events": [
                                    {"event_type": "electron_transfer"}
                                ],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            review_queue_path.write_text(
                json.dumps(
                    {
                        "queue_rows": [
                            {
                                "entry_id": "m_csa:6",
                                "review_category": "standard_draft_event_review",
                                "blockers": ["review_status_not_approved"],
                            },
                            {
                                "entry_id": "m_csa:7",
                                "review_category": "standard_draft_event_review",
                                "blockers": ["review_status_not_approved"],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            split_path.write_text(
                json.dumps(
                    {
                        "split_records": [
                            {
                                "entry_id": "m_csa:6",
                                "assigned_embedding_split": "calibration",
                            },
                            {
                                "entry_id": "m_csa:7",
                                "assigned_embedding_split": "train",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            label_manifest_path.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:6",
                                "split_assignment": "in_distribution",
                            },
                            {
                                "entry_id": "m_csa:7",
                                "split_assignment": "in_distribution",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_train_cal_coverage_gap(
                train_cal_feature_sidecar_path=feature_sidecar_path,
                source_sidecar_path=source_sidecar_path,
                review_queue_path=review_queue_path,
                train_cal_split_manifest_path=split_path,
                label_manifest_path=label_manifest_path,
            )

        self.assertEqual(
            audit["status"],
            "p0_train_cal_feature_coverage_gap_ready_review_queue",
        )
        self.assertTrue(audit["decision"]["rerun_blocked_by_calibration_coverage"])
        self.assertEqual(audit["decision"]["next_review_gate_entry_ids"], ["m_csa:6"])
        self.assertEqual(audit["counts"]["draft_calibration_rows"], 1)
        self.assertEqual(audit["counts"]["draft_train_rows"], 1)
        self.assertEqual(
            audit["counts"]["missing_materialized_event_type_counts"],
            {
                "bond_order_changed": 1,
                "electron_transfer": 1,
                "proton_transfer": 1,
            },
        )
        self.assertEqual(
            audit["review_priority_rows"][0]["priority_class"],
            "P0.1_calibration_coverage_unblocker",
        )
        self.assertFalse(audit["guardrails"]["model_weights_fit_or_refit"])

    def test_row_specific_bond_change_p0_train_cal_feature_guardrail_audit_passes_clean_payload(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            feature_sidecar_path = root / "feature_sidecar.json"
            source_sidecar_path = root / "source_sidecar.json"
            label_manifest_path = root / "label_manifest.json"
            feature_sidecar_path.write_text(
                json.dumps(
                    {
                        "decision": {
                            "full_no_template_centroid_or_residual_rerun_ready": False,
                            "reason_not_ready_for_rerun": (
                                "calibration coverage absent"
                            ),
                        },
                        "feature_rows": [
                            {
                                "entry_id": "m_csa:5",
                                "assigned_embedding_split": "train",
                                "row_specific_event_features": {
                                    "event_count": 2,
                                    "bond_change_event_count": 1,
                                    "has_bond_change_event": True,
                                },
                                "feature_guardrails": {
                                    "heldout_row": False,
                                    "source_text_excluded_from_features": True,
                                    "source_ids_excluded_from_features": True,
                                    "reviewer_metadata_excluded_from_features": True,
                                    "accession_excluded_from_features": True,
                                    "labels_and_fingerprint_excluded_from_features": True,
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            source_sidecar_path.write_text(
                json.dumps(
                    {
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:5",
                                "review_status": "approved",
                                "allowed_for_feature_contract_consumption_now": True,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            label_manifest_path.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:5",
                                "split_assignment": "in_distribution",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_guardrail_audit(
                train_cal_feature_sidecar_path=feature_sidecar_path,
                source_sidecar_path=source_sidecar_path,
                label_manifest_path=label_manifest_path,
            )

        self.assertEqual(
            audit["status"],
            "p0_train_cal_feature_guardrail_audit_passed_partial_no_fit",
        )
        self.assertEqual(audit["counts"]["critical_violation_total"], 0)
        self.assertEqual(audit["counts"]["feature_value_type_counts"], {"bool": 1, "int": 2})
        self.assertTrue(
            audit["decision"]["safe_to_use_as_partial_train_feature_surface"]
        )
        self.assertFalse(audit["decision"]["safe_to_run_no_template_methods_now"])
        self.assertIn(
            "calibration coverage absent",
            audit["decision"]["reason_not_ready_for_rerun"],
        )

    def test_row_specific_bond_change_p0_train_cal_feature_guardrail_audit_blocks_leaks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            feature_sidecar_path = root / "feature_sidecar.json"
            source_sidecar_path = root / "source_sidecar.json"
            label_manifest_path = root / "label_manifest.json"
            feature_sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "m_csa:6",
                                "assigned_embedding_split": "train",
                                "row_specific_event_features": {
                                    "source_span_text": "leaky source text",
                                    "event_count": 1,
                                },
                                "feature_guardrails": {
                                    "heldout_row": False,
                                    "source_text_excluded_from_features": True,
                                    "source_ids_excluded_from_features": True,
                                    "reviewer_metadata_excluded_from_features": True,
                                    "accession_excluded_from_features": True,
                                    "labels_and_fingerprint_excluded_from_features": True,
                                },
                            },
                            {
                                "entry_id": "m_csa:999",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": {
                                    "event_count": 1,
                                },
                                "feature_guardrails": {
                                    "heldout_row": True,
                                    "source_text_excluded_from_features": True,
                                    "source_ids_excluded_from_features": True,
                                    "reviewer_metadata_excluded_from_features": True,
                                    "accession_excluded_from_features": True,
                                    "labels_and_fingerprint_excluded_from_features": True,
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            source_sidecar_path.write_text(
                json.dumps(
                    {
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:6",
                                "review_status": "draft",
                                "allowed_for_feature_contract_consumption_now": False,
                            },
                            {
                                "entry_id": "m_csa:999",
                                "review_status": "approved",
                                "allowed_for_feature_contract_consumption_now": True,
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            label_manifest_path.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:6",
                                "split_assignment": "in_distribution",
                            },
                            {
                                "entry_id": "m_csa:999",
                                "split_assignment": "heldout",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_guardrail_audit(
                train_cal_feature_sidecar_path=feature_sidecar_path,
                source_sidecar_path=source_sidecar_path,
                label_manifest_path=label_manifest_path,
            )

        self.assertEqual(
            audit["status"],
            "p0_train_cal_feature_guardrail_audit_blocked",
        )
        critical_counts = audit["counts"]["critical_counts"]
        self.assertEqual(critical_counts["feature_rows_source_not_approved"], 1)
        self.assertEqual(critical_counts["feature_rows_source_not_consumable"], 1)
        self.assertEqual(critical_counts["feature_rows_label_manifest_heldout"], 1)
        self.assertEqual(critical_counts["feature_rows_marked_heldout"], 1)
        self.assertEqual(critical_counts["feature_payload_forbidden_keys"], 1)
        self.assertEqual(
            critical_counts["feature_payload_non_scalar_or_string_values"], 1
        )
        self.assertFalse(
            audit["decision"]["safe_to_use_as_partial_train_feature_surface"]
        )

    def test_row_specific_bond_change_p0_calibration_review_packet_uses_next_gate_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            coverage_path = root / "coverage.json"
            source_path = root / "source.json"
            coverage_path.write_text(
                json.dumps(
                    {
                        "counts": {"critical_violation_total": 0},
                        "decision": {
                            "next_review_gate_entry_ids": ["m_csa:6"],
                        },
                        "review_priority_rows": [
                            {
                                "entry_id": "m_csa:6",
                                "assigned_embedding_split": "calibration",
                                "priority_class": (
                                    "P0.1_calibration_coverage_unblocker"
                                ),
                                "priority_reasons": [
                                    "calibration_coverage_absent"
                                ],
                                "review_category": "standard_draft_event_review",
                                "review_blockers": [
                                    "review_status_not_approved"
                                ],
                                "event_types": ["proton_transfer"],
                                "missing_from_materialized_event_types": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            source_path.write_text(
                json.dumps(
                    {
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:6",
                                "source_text_or_database_evidence_span": [
                                    {
                                        "source_record_id": "m_csa:6:mechanism:1",
                                        "span_text": "review-only source text",
                                    }
                                ],
                                "row_specific_bond_change_events": [
                                    {
                                        "event_type": "proton_transfer",
                                        "confidence": "medium",
                                        "mapped_active_site_residues": [
                                            "m_csa:6:residue:1",
                                            "m_csa:6:residue:2",
                                        ],
                                        "source_evidence_span": {
                                            "source_record_id": (
                                                "m_csa:6:mechanism:1"
                                            ),
                                            "span_text": (
                                                "review-only event source text"
                                            ),
                                        },
                                    }
                                ],
                            },
                            {
                                "entry_id": "m_csa:7",
                                "source_text_or_database_evidence_span": [],
                                "row_specific_bond_change_events": [],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            packet = build_mechanism_feature_row_specific_bond_change_p0_calibration_review_packet(
                train_cal_coverage_gap_path=coverage_path,
                source_sidecar_path=source_path,
            )

        self.assertEqual(
            packet["status"],
            "p0_calibration_review_packet_ready_manual_only",
        )
        self.assertEqual(packet["counts"]["packet_rows"], 1)
        self.assertEqual(packet["packet_rows"][0]["entry_id"], "m_csa:6")
        self.assertEqual(packet["packet_rows"][0]["event_review_rows"][0]["event_type"], "proton_transfer")
        self.assertEqual(
            packet["packet_rows"][0]["copy_if_approved"],
            {
                "review_status": "approved",
                "allowed_for_feature_contract_consumption_now": True,
                "allowed_for_model_training_now": False,
                "reviewer_id_required": True,
            },
        )
        self.assertFalse(packet["guardrails"]["model_weights_fit_or_refit"])
        self.assertFalse(
            packet["guardrails"]["reviewer_decisions_recorded_by_this_artifact"]
        )

    def test_row_specific_bond_change_p0_pending_rewrite_blocker_summarizes_reviewed_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_path = root / "source.json"
            feature_sidecar_path = root / "feature_sidecar.json"
            split_path = root / "split.json"
            source_path.write_text(
                json.dumps(
                    {
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:6",
                                "accession": "P00390",
                                "review_status": "needs_more_evidence",
                                "reviewer_id": "reviewer",
                                "reviewer_decision": {
                                    "decision": (
                                        "rewrite_events_and_keep_review_pending"
                                    ),
                                    "decision_rationale": (
                                        "low-confidence electron transfer"
                                    ),
                                    "blocked_event_indices": [0],
                                    "accepted_event_indices_for_future_rewrite_context": [
                                        1
                                    ],
                                },
                                "allowed_for_feature_contract_consumption_now": False,
                                "allowed_for_model_training_now": False,
                                "row_specific_bond_change_events": [
                                    {
                                        "event_type": "electron_transfer",
                                        "confidence": "low",
                                        "mapped_active_site_residues": [],
                                        "source_evidence_span": {
                                            "source_record_id": (
                                                "m_csa:6:mechanism:1"
                                            ),
                                            "span_text": "electron transfer text",
                                        },
                                    },
                                    {
                                        "event_type": "proton_transfer",
                                        "confidence": "medium",
                                        "mapped_active_site_residues": [
                                            "m_csa:6:residue:1"
                                        ],
                                        "source_evidence_span": {
                                            "source_record_id": (
                                                "m_csa:6:mechanism:1"
                                            ),
                                            "span_text": "proton transfer text",
                                        },
                                    },
                                ],
                            },
                            {
                                "entry_id": "m_csa:147",
                                "review_status": "approved",
                                "allowed_for_feature_contract_consumption_now": True,
                                "allowed_for_model_training_now": False,
                                "row_specific_bond_change_events": [],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            feature_sidecar_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "materialized_feature_rows": 1,
                            "train_rows": 0,
                            "calibration_rows": 1,
                            "critical_violation_total": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            split_path.write_text(
                json.dumps(
                    {
                        "split_records": [
                            {
                                "entry_id": "m_csa:6",
                                "assigned_embedding_split": "train",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            packet = build_mechanism_feature_row_specific_bond_change_p0_pending_rewrite_blocker(
                source_sidecar_path=source_path,
                train_cal_feature_sidecar_path=feature_sidecar_path,
                train_cal_split_manifest_path=split_path,
            )

        self.assertEqual(
            packet["status"],
            "p0_pending_rewrite_blocker_ready_manual_only",
        )
        self.assertEqual(packet["counts"]["pending_rewrite_rows"], 1)
        self.assertEqual(packet["counts"]["blocked_event_rows"], 1)
        self.assertEqual(
            packet["counts"]["blocked_event_type_counts"],
            {"electron_transfer": 1},
        )
        self.assertEqual(
            packet["counts"]["blocker_counts"],
            {
                "low_confidence_event_review": 1,
                "unmapped_event_review": 1,
            },
        )
        row = packet["pending_rewrite_rows"][0]
        self.assertEqual(row["entry_id"], "m_csa:6")
        self.assertEqual(row["assigned_embedding_split"], "train")
        self.assertEqual(row["blocked_event_indices"], [0])
        self.assertEqual(
            row["accepted_event_indices_for_future_rewrite_context"], [1]
        )
        self.assertTrue(row["event_rows"][0]["blocked_by_reviewer"])
        self.assertFalse(row["event_rows"][1]["blocked_by_reviewer"])
        self.assertFalse(packet["guardrails"]["model_weights_fit_or_refit"])

    def test_row_specific_bond_change_p0_pending_rewrite_blocker_clears_when_full_surface_materialized(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_path = root / "source.json"
            feature_sidecar_path = root / "feature_sidecar.json"
            split_path = root / "split.json"
            source_path.write_text(
                json.dumps(
                    {
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:6",
                                "review_status": "approved",
                                "allowed_for_feature_contract_consumption_now": True,
                                "allowed_for_model_training_now": False,
                                "row_specific_bond_change_events": [],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            feature_sidecar_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "materialized_feature_rows": 1,
                            "train_rows": 1,
                            "calibration_rows": 1,
                            "critical_violation_total": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            split_path.write_text(
                json.dumps(
                    {
                        "split_records": [
                            {
                                "entry_id": "m_csa:6",
                                "assigned_embedding_split": "train",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            packet = build_mechanism_feature_row_specific_bond_change_p0_pending_rewrite_blocker(
                source_sidecar_path=source_path,
                train_cal_feature_sidecar_path=feature_sidecar_path,
                train_cal_split_manifest_path=split_path,
            )

        self.assertEqual(
            packet["status"],
            "p0_pending_rewrite_blocker_cleared_ready_for_no_template_rerun",
        )
        self.assertTrue(packet["decision"]["full_no_template_rerun_ready"])
        self.assertIsNone(packet["decision"]["reason_not_ready"])
        self.assertEqual(packet["counts"]["pending_rewrite_rows"], 0)

    def test_row_specific_bond_change_p0_no_template_rerun_scores_train_cal_but_blocks_without_oos(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sidecar = root / "feature.json"
            guardrail = root / "guardrail.json"
            manifest = root / "manifest.json"
            feature_payloads = [
                ("m_csa:1", "train", "alpha", 1, 0),
                ("m_csa:2", "train", "alpha", 2, 0),
                ("m_csa:3", "train", "beta", 0, 2),
                ("m_csa:4", "calibration", "alpha", 1, 1),
            ]
            sidecar.write_text(
                json.dumps(
                    {
                        "counts": {
                            "critical_violation_total": 0,
                            "materialized_feature_rows": 4,
                        },
                        "feature_rows": [
                            {
                                "entry_id": entry_id,
                                "assigned_embedding_split": split,
                                "row_specific_event_features": {
                                    "bond_change_event_count": bond_count,
                                    "electron_transfer_count": electron_count,
                                    "has_bond_change_event": bool(bond_count),
                                },
                            }
                            for entry_id, split, _label, bond_count, electron_count in feature_payloads
                        ],
                    }
                ),
                encoding="utf-8",
            )
            guardrail.write_text(
                json.dumps(
                    {
                        "counts": {"critical_violation_total": 0},
                        "decision": {"safe_to_run_no_template_methods_now": True},
                    }
                ),
                encoding="utf-8",
            )
            manifest.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": entry_id,
                                "fingerprint_id": label,
                                "label_type": "seed_fingerprint",
                            }
                            for entry_id, _split, label, _bond_count, _electron_count in feature_payloads
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_no_template_rerun(
                train_cal_feature_sidecar_path=sidecar,
                train_cal_feature_guardrail_path=guardrail,
                label_manifest_path=manifest,
            )

        self.assertEqual(
            audit["status"],
            "p0_row_specific_no_template_train_cal_scored_oos_blocked",
        )
        self.assertTrue(audit["decision"]["centroid_train_cal_scored"])
        self.assertTrue(audit["decision"]["residual_train_cal_scored"])
        self.assertFalse(
            audit["decision"]["known_vs_novel_operating_point_evaluable"]
        )
        self.assertEqual(audit["counts"]["calibration_oos_rows"], 0)
        self.assertFalse(
            audit["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )

    def test_row_specific_bond_change_p0_oos_calibration_gap_prioritizes_calibration_oos(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sidecar = root / "sidecar.json"
            contract = root / "contract.json"
            split = root / "split.json"
            manifest = root / "manifest.json"
            sidecar.write_text(
                json.dumps(
                    {
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:5",
                                "review_status": "approved",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            contract_rows = [
                ("m_csa:1", "train"),
                ("m_csa:2", "calibration"),
                ("m_csa:3", "calibration"),
                ("m_csa:4", "calibration"),
                ("m_csa:5", "calibration"),
                ("m_csa:6", "train"),
            ]
            contract.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": entry_id,
                                "assigned_embedding_split": assigned_split,
                                "active_site_role_graph": {
                                    "active_site_residue_count": 4,
                                    "status": "ok",
                                },
                                "reaction_center_template": {
                                    "status": "no_mechanism_fingerprint_oos_or_unlabeled"
                                },
                            }
                            for entry_id, assigned_split in contract_rows
                        ]
                    }
                ),
                encoding="utf-8",
            )
            split.write_text(
                json.dumps(
                    {
                        "split_records": [
                            {
                                "entry_id": entry_id,
                                "assigned_embedding_split": assigned_split,
                                "stratum": "label_type:out_of_scope",
                            }
                            for entry_id, assigned_split in contract_rows
                        ]
                    }
                ),
                encoding="utf-8",
            )
            manifest.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "label_type": "out_of_scope",
                                "split_assignment": "in_distribution",
                            },
                            {
                                "entry_id": "m_csa:2",
                                "label_type": "out_of_scope",
                                "split_assignment": "in_distribution",
                            },
                            {
                                "entry_id": "m_csa:3",
                                "label_type": "seed_fingerprint",
                                "split_assignment": "in_distribution",
                            },
                            {
                                "entry_id": "m_csa:4",
                                "label_type": "out_of_scope",
                                "split_assignment": "heldout",
                            },
                            {
                                "entry_id": "m_csa:5",
                                "label_type": "out_of_scope",
                                "split_assignment": "in_distribution",
                            },
                            {
                                "entry_id": "m_csa:6",
                                "label_type": "out_of_scope",
                                "split_assignment": "in_distribution",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            packet = build_mechanism_feature_row_specific_bond_change_p0_oos_calibration_gap(
                source_sidecar_path=sidecar,
                feature_contract_path=contract,
                train_cal_split_manifest_path=split,
                label_manifest_path=manifest,
                max_packet_rows=2,
            )

        self.assertEqual(
            packet["status"], "p0_oos_calibration_gap_ready_review_packet"
        )
        self.assertEqual(packet["counts"]["candidate_rows"], 3)
        self.assertEqual(packet["counts"]["candidate_calibration_rows"], 1)
        self.assertEqual(packet["counts"]["candidate_train_rows"], 2)
        self.assertEqual(packet["counts"]["packet_rows"], 2)
        self.assertEqual(packet["counts"]["packet_calibration_rows"], 1)
        self.assertEqual(
            [row["entry_id"] for row in packet["packet_rows"]],
            ["m_csa:2", "m_csa:1"],
        )
        self.assertFalse(packet["decision"]["feature_consumption_allowed_now"])
        self.assertTrue(
            packet["decision"]["fills_no_template_oos_operating_point_if_approved"]
        )
        self.assertFalse(packet["guardrails"]["heldout_rows_in_packet"])
        self.assertFalse(
            packet["guardrails"]["heldout_rows_used_for_training_or_threshold_tuning"]
        )

    def test_row_specific_bond_change_p0_no_template_rerun_ready_with_calibration_oos(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sidecar = root / "feature.json"
            guardrail = root / "guardrail.json"
            manifest = root / "manifest.json"
            feature_payloads = [
                ("m_csa:1", "train", "seed_fingerprint", "alpha", 1, 0),
                ("m_csa:2", "train", "seed_fingerprint", "alpha", 2, 0),
                ("m_csa:3", "train", "seed_fingerprint", "beta", 0, 2),
                ("m_csa:4", "calibration", "seed_fingerprint", "alpha", 1, 1),
                ("m_csa:5", "calibration", "out_of_scope", None, 4, 4),
            ]
            sidecar.write_text(
                json.dumps(
                    {
                        "counts": {"critical_violation_total": 0},
                        "feature_rows": [
                            {
                                "entry_id": entry_id,
                                "assigned_embedding_split": split,
                                "row_specific_event_features": {
                                    "bond_change_event_count": bond_count,
                                    "electron_transfer_count": electron_count,
                                },
                            }
                            for entry_id, split, _label_type, _label, bond_count, electron_count in feature_payloads
                        ],
                    }
                ),
                encoding="utf-8",
            )
            guardrail.write_text(
                json.dumps(
                    {
                        "counts": {"critical_violation_total": 0},
                        "decision": {"safe_to_run_no_template_methods_now": True},
                    }
                ),
                encoding="utf-8",
            )
            manifest.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": entry_id,
                                "label_type": label_type,
                                "fingerprint_id": label,
                            }
                            for entry_id, _split, label_type, label, _bond_count, _electron_count in feature_payloads
                        ]
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_no_template_rerun(
                train_cal_feature_sidecar_path=sidecar,
                train_cal_feature_guardrail_path=guardrail,
                label_manifest_path=manifest,
            )

        self.assertEqual(
            audit["status"],
            "p0_row_specific_no_template_train_cal_operating_point_ready",
        )
        self.assertTrue(
            audit["decision"]["known_vs_novel_operating_point_evaluable"]
        )
        self.assertEqual(audit["counts"]["calibration_primary_rows"], 1)
        self.assertEqual(audit["counts"]["calibration_oos_rows"], 1)
        self.assertIsNotNone(
            audit["centroid_variant"]["calibration_selected_similarity_threshold"][
                "threshold"
            ]
        )
        self.assertIsNotNone(
            audit["residual_variant"]["calibration_selected_residual_threshold"][
                "threshold"
            ]
        )

    def test_row_specific_bond_change_p0_oos_calibration_extraction_package_is_manual_only(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            gap = root / "gap.json"
            manifest = root / "manifest.json"
            role_graph = root / "roles.json"
            gap.write_text(
                json.dumps(
                    {
                        "packet_rows": [
                            {
                                "entry_id": "m_csa:2",
                                "assigned_embedding_split": "calibration",
                                "label_manifest_type": "out_of_scope",
                                "label_manifest_split": "in_distribution",
                                "active_site_residue_count": 2,
                                "role_graph_status": "ok",
                                "reaction_template_status": "no_mechanism_fingerprint_oos_or_unlabeled",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            manifest.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:2",
                                "accession": "P12345",
                                "label_type": "out_of_scope",
                                "split_assignment": "in_distribution",
                                "oos_tier": "near_oos",
                                "benchmark_role": "oos_tier::near_oos",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            role_graph.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:2",
                                "residues": [
                                    {
                                        "residue_node_id": "m_csa:2:residue:1",
                                        "roles": ["proton_acceptor"],
                                        "sequence_positions": [
                                            {"code": "Asp", "resid": 10}
                                        ],
                                        "structure_positions": [],
                                    }
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            package = build_mechanism_feature_row_specific_bond_change_p0_oos_calibration_extraction_work_package(
                oos_calibration_gap_path=gap,
                label_manifest_path=manifest,
                active_site_role_graph_sidecar_path=role_graph,
            )

        self.assertEqual(
            package["status"],
            "p0_oos_calibration_extraction_work_package_ready_manual_only",
        )
        self.assertEqual(package["counts"]["manual_extraction_rows"], 1)
        self.assertEqual(package["counts"]["calibration_rows"], 1)
        self.assertEqual(package["counts"]["critical_violation_total"], 0)
        self.assertFalse(
            package["guardrails"]["feature_contract_consumption_allowed_now"]
        )
        self.assertFalse(package["guardrails"]["row_specific_source_evidence_materialized"])
        row = package["extraction_rows"][0]
        self.assertEqual(row["accession"], "P12345")
        self.assertIn("source_record_id", row["manual_extraction_template"])
        self.assertEqual(len(row["active_site_residue_role_template"]), 1)
        self.assertFalse(row["allowed_for_feature_contract_consumption_now"])
        self.assertFalse(row["allowed_for_model_training_now"])

    def test_row_specific_bond_change_p0_oos_approved_sidecar_skips_rhea_missing_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            package_path = root / "package.json"
            graph_path = root / "graph.json"
            package_rows = [
                {
                    "entry_id": "m_csa:1",
                    "accession": "P11111",
                    "assigned_embedding_split": "calibration",
                    "label_manifest_type": "out_of_scope",
                    "label_manifest_split": "in_distribution",
                    "oos_tier": "boundary_oos",
                },
                {
                    "entry_id": "m_csa:2",
                    "accession": "P22222",
                    "assigned_embedding_split": "calibration",
                    "label_manifest_type": "out_of_scope",
                    "label_manifest_split": "in_distribution",
                    "oos_tier": "unknown_oos",
                },
            ]
            package_path.write_text(
                json.dumps({"extraction_rows": package_rows}),
                encoding="utf-8",
            )
            graph_path.write_text(
                json.dumps(
                    {
                        "metadata": {"generated_at": "2026-06-02T00:00:00Z"},
                        "nodes": [
                            {"id": "m_csa:1"},
                            {"id": "m_csa:2"},
                            {
                                "id": "m_csa:1:mechanism:1",
                                "text": "A serine residue attacks the substrate carbonyl.",
                            },
                            {
                                "id": "m_csa:2:mechanism:1",
                                "text": "A cysteine residue attacks the substrate carbonyl.",
                            },
                            {
                                "id": "m_csa:1:residue:1",
                                "roles": ["nucleophile"],
                                "sequence_positions": [
                                    {
                                        "code": "Ser",
                                        "resid": 10,
                                        "uniprot_id": "P11111",
                                    }
                                ],
                            },
                            {
                                "id": "m_csa:2:residue:1",
                                "roles": ["nucleophile"],
                                "sequence_positions": [
                                    {
                                        "code": "Cys",
                                        "resid": 20,
                                        "uniprot_id": "P22222",
                                    }
                                ],
                            },
                            {"id": "ec:1.1.1.1"},
                            {"id": "ec:2.2.2.2"},
                            {
                                "id": "rhea:RHEA:1",
                                "equation": "substrate + H2O = product",
                            },
                        ],
                        "edges": [
                            {
                                "source": "m_csa:1",
                                "target": "m_csa:1:mechanism:1",
                                "predicate": "has_mechanism_text",
                            },
                            {
                                "source": "m_csa:2",
                                "target": "m_csa:2:mechanism:1",
                                "predicate": "has_mechanism_text",
                            },
                            {
                                "source": "m_csa:1",
                                "target": "m_csa:1:residue:1",
                                "predicate": "has_catalytic_residue",
                            },
                            {
                                "source": "m_csa:2",
                                "target": "m_csa:2:residue:1",
                                "predicate": "has_catalytic_residue",
                            },
                            {
                                "source": "m_csa:1",
                                "target": "ec:1.1.1.1",
                                "predicate": "has_ec",
                            },
                            {
                                "source": "m_csa:2",
                                "target": "ec:2.2.2.2",
                                "predicate": "has_ec",
                            },
                            {
                                "source": "ec:1.1.1.1",
                                "target": "rhea:RHEA:1",
                                "predicate": "maps_to_reaction",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            sidecar = build_mechanism_feature_row_specific_bond_change_p0_oos_calibration_approved_source_evidence_sidecar(
                extraction_work_package_path=package_path,
                graph_path=graph_path,
                max_rows=2,
            )

        self.assertEqual(sidecar["counts"]["approved_rows"], 1)
        self.assertEqual(sidecar["counts"]["skipped_candidate_rows"], 1)
        self.assertEqual(sidecar["sidecar_rows"][0]["entry_id"], "m_csa:1")
        self.assertEqual(sidecar["skipped_rows"][0]["entry_id"], "m_csa:2")
        self.assertIn(
            "rhea_equation_missing", sidecar["skipped_rows"][0]["blockers"]
        )
        self.assertTrue(
            sidecar["sidecar_rows"][0][
                "allowed_for_feature_contract_consumption_now"
            ]
        )

    def test_row_specific_bond_change_p0_oos_calibration_extraction_strict_audit_blocks_unsafe_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            package_path = root / "package.json"
            package_path.write_text(
                json.dumps(
                    {
                        "required_fields": [
                            "source_record_id",
                            "source_database",
                        ],
                        "extraction_rows": [
                            {
                                "entry_id": "m_csa:2",
                                "assigned_embedding_split": "heldout",
                                "label_manifest_split": "heldout",
                                "label_manifest_type": "seed_fingerprint",
                                "manual_extraction_template": {
                                    "source_record_id": None
                                },
                                "allowed_for_feature_contract_consumption_now": True,
                                "allowed_for_model_training_now": False,
                                "extraction_status": "approved",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_row_specific_bond_change_p0_oos_calibration_extraction_work_package_strict_audit(
                extraction_work_package_path=package_path,
            )

        self.assertEqual(
            audit["status"],
            "p0_oos_calibration_extraction_work_package_strict_audit_failed",
        )
        self.assertFalse(audit["decision"]["manual_extraction_package_passed"])
        self.assertGreater(audit["counts"]["critical_violation_total"], 0)
        self.assertEqual(
            audit["counts"]["critical_counts"][
                "rows_allowed_for_feature_contract_consumption_now"
            ],
            1,
        )
        self.assertEqual(audit["counts"]["critical_counts"]["heldout_rows"], 1)
        self.assertEqual(audit["counts"]["critical_counts"]["non_oos_rows"], 1)
        self.assertEqual(
            audit["counts"]["critical_counts"]["missing_manual_template_fields"],
            1,
        )
        self.assertFalse(audit["decision"]["feature_consumption_allowed_now"])

    def test_row_specific_bond_change_p0_oos_augmented_error_analysis_names_retained_failure_set(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            rerun_path = root / "rerun.json"
            contract_path = root / "contract.json"
            feature_sidecar_path = root / "features.json"
            rerun_path.write_text(
                json.dumps(
                    {
                        "scored_rows": {
                            "calibration": [
                                {
                                    "entry_id": "m_csa:1",
                                    "is_primary": False,
                                    "true_label": "none_of_above",
                                    "nearest_primary_label": "ser_his_acid_hydrolase",
                                    "nearest_primary_similarity": 0.3,
                                    "out_of_atlas_span_residual": 2.95,
                                },
                                {
                                    "entry_id": "m_csa:2",
                                    "is_primary": False,
                                    "true_label": "none_of_above",
                                    "nearest_primary_label": "metal_dependent_hydrolase",
                                    "nearest_primary_similarity": 0.1,
                                    "out_of_atlas_span_residual": 3.4,
                                },
                                {
                                    "entry_id": "m_csa:3",
                                    "is_primary": True,
                                    "true_label": "ser_his_acid_hydrolase",
                                    "nearest_primary_label": "ser_his_acid_hydrolase",
                                    "nearest_primary_similarity": 0.5,
                                    "out_of_atlas_span_residual": 1.0,
                                },
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )
            contract_path.write_text(
                json.dumps(
                    {
                        "status": (
                            "p0_oos_augmented_operating_point_contract_ready_calibration_only"
                        ),
                        "calibration_contract": {
                            "residual_distance": {"threshold": 3.0},
                            "centroid_similarity": {"threshold": 0.2},
                        },
                    }
                ),
                encoding="utf-8",
            )
            feature_sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "row_specific_event_features": {
                                    "event_count": 3,
                                    "bond_change_event_count": 1,
                                    "proton_transfer_count": 1,
                                    "electron_transfer_count": 1,
                                },
                            },
                            {
                                "entry_id": "m_csa:2",
                                "row_specific_event_features": {
                                    "event_count": 4,
                                    "bond_change_event_count": 2,
                                    "proton_transfer_count": 0,
                                    "electron_transfer_count": 2,
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            analysis = build_mechanism_feature_row_specific_bond_change_p0_oos_augmented_calibration_error_analysis(
                no_template_rerun_path=rerun_path,
                operating_point_contract_path=contract_path,
                train_cal_feature_sidecar_path=feature_sidecar_path,
            )

        self.assertEqual(
            analysis["status"], "p0_oos_augmented_calibration_error_analysis_ready"
        )
        self.assertEqual(
            analysis["counts"]["outcome_counts"],
            {"oos_abstained": 1, "oos_non_abstained": 1, "primary_retained": 1},
        )
        self.assertEqual(
            analysis["counts"]["retained_oos_nearest_primary_counts"],
            {"ser_his_acid_hydrolase": 1},
        )
        self.assertEqual(
            analysis["counts"]["retained_oos_event_profile_counts"],
            {"events=3;bond=1;proton=1;electron=1": 1},
        )
        self.assertEqual(
            analysis["counts"]["retained_oos_priority_counts"],
            {"borderline_contract_miss": 1},
        )
        self.assertEqual(
            analysis["retained_oos_failure_set"][0],
            {
                "entry_id": "m_csa:1",
                "event_profile": "events=3;bond=1;proton=1;electron=1",
                "nearest_primary_label": "ser_his_acid_hydrolase",
                "priority": "borderline_contract_miss",
                "residual_margin_below_threshold": 0.05,
            },
        )

    def test_oos_augmented_retained_oos_feature_target_finds_contrast_tokens(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_sidecar_path = root / "source.json"
            error_analysis_path = root / "error.json"
            rerun_path = root / "rerun.json"
            source_sidecar_path.write_text(
                json.dumps(
                    {
                        "status": "p0_oos_augmented_source_evidence_sidecar_ready",
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "review_status": "approved",
                                "allowed_for_feature_contract_consumption_now": True,
                                "active_site_residue_role_support": [
                                    {
                                        "residue_node_id": "m_csa:1:residue:1",
                                        "code": "Ser",
                                        "roles": ["nucleophile"],
                                    }
                                ],
                                "row_specific_bond_change_events": [
                                    {
                                        "event_type": "bond_formed",
                                        "participants_before": ["substrate"],
                                        "participants_after": ["product"],
                                        "mapped_active_site_residues": [
                                            "m_csa:1:residue:1"
                                        ],
                                    }
                                ],
                                "row_specific_reaction_participant_mapping": [
                                    {"role": "substrate"},
                                    {"role": "product"},
                                    {"role": "catalytic_residue"},
                                ],
                            },
                            {
                                "entry_id": "m_csa:2",
                                "review_status": "approved",
                                "allowed_for_feature_contract_consumption_now": True,
                                "active_site_residue_role_support": [
                                    {
                                        "residue_node_id": "m_csa:2:residue:1",
                                        "code": "His",
                                        "roles": ["metal ligand"],
                                    },
                                    {
                                        "residue_node_id": "m_csa:2:residue:2",
                                        "code": "Tyr",
                                        "roles": ["proton donor"],
                                    },
                                ],
                                "row_specific_bond_change_events": [
                                    {
                                        "event_type": "electron_transfer",
                                        "participants_before": [
                                            "substrate",
                                            "cofactor",
                                        ],
                                        "participants_after": [
                                            "product",
                                            "reduced cofactor",
                                        ],
                                        "mapped_active_site_residues": [
                                            "m_csa:2:residue:1",
                                            "m_csa:2:residue:2",
                                        ],
                                    }
                                ],
                                "row_specific_reaction_participant_mapping": [
                                    {"role": "substrate"},
                                    {"role": "product"},
                                    {"role": "cofactor"},
                                    {"role": "catalytic_residue"},
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            error_analysis_path.write_text(
                json.dumps(
                    {
                        "status": "p0_oos_augmented_calibration_error_analysis_ready",
                        "retained_oos_failure_set": [
                            {
                                "entry_id": "m_csa:2",
                                "priority": "borderline_contract_miss",
                                "nearest_primary_label": "ser_his_acid_hydrolase",
                            }
                        ],
                        "all_calibration_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "operating_point_outcome": "primary_retained",
                            },
                            {
                                "entry_id": "m_csa:2",
                                "operating_point_outcome": "oos_non_abstained",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            rerun_path.write_text(
                json.dumps(
                    {
                        "status": (
                            "p0_row_specific_no_template_train_cal_operating_point_ready"
                        ),
                        "scored_rows": {
                            "train": [
                                {
                                    "entry_id": "m_csa:1",
                                    "is_primary": True,
                                    "true_label": "ser_his_acid_hydrolase",
                                }
                            ],
                            "calibration": [
                                {
                                    "entry_id": "m_csa:2",
                                    "is_primary": False,
                                    "true_label": "none_of_above",
                                }
                            ],
                        },
                    }
                ),
                encoding="utf-8",
            )

            target = build_mechanism_feature_row_specific_bond_change_p0_oos_augmented_retained_oos_feature_target(
                source_sidecar_path=source_sidecar_path,
                calibration_error_analysis_path=error_analysis_path,
                no_template_rerun_path=rerun_path,
            )

        self.assertEqual(
            target["status"], "p0_oos_augmented_retained_oos_feature_target_ready"
        )
        self.assertTrue(
            target["decision"]["feature_family_ready_for_expanded_sidecar"]
        )
        self.assertIn(
            "event_type_present",
            target["decision"]["ready_candidate_feature_families"],
        )
        self.assertEqual(target["counts"]["critical_violation_total"], 0)
        self.assertEqual(target["counts"]["priority_retained_oos_failure_rows"], 1)
        self.assertEqual(
            target["retained_row_feature_contrasts"][0]["entry_id"], "m_csa:2"
        )

    def test_oos_augmented_expanded_feature_sidecar_materializes_target_family(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_sidecar_path = root / "source.json"
            target_path = root / "target.json"
            split_path = root / "split.json"
            contract_path = root / "contract.json"
            label_manifest_path = root / "labels.json"
            source_sidecar_path.write_text(
                json.dumps(
                    {
                        "sidecar_rows": [
                            {
                                "entry_id": "m_csa:1",
                                "review_status": "approved",
                                "allowed_for_feature_contract_consumption_now": True,
                                "active_site_residue_role_support": [
                                    {
                                        "residue_node_id": "m_csa:1:residue:1",
                                        "code": "Ser",
                                        "roles": ["nucleophile"],
                                    }
                                ],
                                "row_specific_bond_change_events": [
                                    {
                                        "event_type": "bond_formed",
                                        "mapped_active_site_residues": [
                                            "m_csa:1:residue:1"
                                        ],
                                    }
                                ],
                            },
                            {
                                "entry_id": "m_csa:2",
                                "review_status": "approved",
                                "allowed_for_feature_contract_consumption_now": True,
                                "active_site_residue_role_support": [
                                    {
                                        "residue_node_id": "m_csa:2:residue:1",
                                        "code": "His",
                                        "roles": ["metal ligand"],
                                    }
                                ],
                                "row_specific_bond_change_events": [
                                    {
                                        "event_type": "electron_transfer",
                                        "mapped_active_site_residues": [
                                            "m_csa:2:residue:1"
                                        ],
                                    }
                                ],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            target_path.write_text(
                json.dumps(
                    {
                        "status": (
                            "p0_oos_augmented_retained_oos_feature_target_ready"
                        ),
                        "decision": {
                            "ready_candidate_feature_families": [
                                "event_type_present"
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            split_path.write_text(
                json.dumps(
                    {
                        "split_records": [
                            {
                                "entry_id": "m_csa:1",
                                "assigned_embedding_split": "train",
                            },
                            {
                                "entry_id": "m_csa:2",
                                "assigned_embedding_split": "calibration",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            contract_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {"entry_id": "m_csa:1"},
                            {"entry_id": "m_csa:2"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            label_manifest_path.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "split_assignment": "in_distribution",
                                "label_type": "primary",
                            },
                            {
                                "entry_id": "m_csa:2",
                                "split_assignment": "in_distribution",
                                "label_type": "out_of_scope",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            sidecar = build_mechanism_feature_row_specific_bond_change_p0_oos_augmented_expanded_train_cal_feature_sidecar(
                source_sidecar_path=source_sidecar_path,
                retained_oos_feature_target_path=target_path,
                train_cal_split_manifest_path=split_path,
                feature_contract_path=contract_path,
                label_manifest_path=label_manifest_path,
            )

        self.assertEqual(
            sidecar["status"],
            "p0_oos_augmented_expanded_train_cal_row_specific_feature_sidecar_ready_no_fit",
        )
        self.assertEqual(sidecar["counts"]["materialized_feature_rows"], 2)
        self.assertEqual(sidecar["counts"]["expanded_feature_dimensions"], 2)
        self.assertTrue(
            any(
                key.startswith("expanded_event_type_present__")
                for key in sidecar["feature_rows"][0][
                    "row_specific_event_features"
                ]
            )
        )

    def test_oos_augmented_expanded_calibration_comparison_keeps_coarse_contract(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            coarse_path = root / "coarse.json"
            expanded_path = root / "expanded.json"
            base_payload = {
                "status": "p0_row_specific_no_template_train_cal_operating_point_ready",
                "counts": {
                    "feature_dimensions": 17,
                    "calibration_rows": 32,
                    "calibration_primary_rows": 4,
                    "calibration_oos_rows": 28,
                },
                "residual_variant": {
                    "calibration_summary": {
                        "auc_oos_gt_primary": 0.67,
                        "mean_primary_residual": 2.6,
                        "mean_oos_residual": 3.1,
                    },
                    "calibration_selected_residual_threshold": {
                        "threshold": 3.2,
                        "primary_retain_recall": 1.0,
                        "oos_abstain_recall": 0.5,
                    },
                },
                "centroid_variant": {
                    "calibration_summary": {"auc_primary_vs_oos": 0.67},
                    "calibration_selected_similarity_threshold": {
                        "threshold": 0.23,
                        "oos_abstain_recall": 0.5,
                    },
                },
            }
            expanded_payload = json.loads(json.dumps(base_payload))
            expanded_payload["counts"]["feature_dimensions"] = 560
            expanded_payload["residual_variant"]["calibration_summary"][
                "auc_oos_gt_primary"
            ] = 0.28
            expanded_payload["residual_variant"][
                "calibration_selected_residual_threshold"
            ]["threshold"] = 19.3
            expanded_payload["residual_variant"][
                "calibration_selected_residual_threshold"
            ]["oos_abstain_recall"] = 0.04
            coarse_path.write_text(json.dumps(base_payload), encoding="utf-8")
            expanded_path.write_text(
                json.dumps(expanded_payload), encoding="utf-8"
            )

            comparison = build_mechanism_feature_row_specific_bond_change_p0_oos_augmented_expanded_calibration_comparison(
                coarse_no_template_rerun_path=coarse_path,
                expanded_no_template_rerun_path=expanded_path,
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
            -0.46,
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

    def test_mechanism_feature_embedding_pilot_fits_train_cal_centroids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            feature_contract = root / "contract.json"
            strict_audit = root / "strict.json"
            label_manifest = root / "labels.json"
            cofactor_sidecar = root / "cofactor.json"

            def feature_row(
                entry_id: str,
                split: str,
                residue_count: int,
                operation: str | None,
                metal_status: str,
            ) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "assigned_embedding_split": split,
                    "active_site_role_graph": {
                        "status": "ok",
                        "active_site_residue_count": residue_count,
                    },
                    "reaction_center_template": {
                        "status": (
                            "template_available"
                            if operation
                            else "no_mechanism_fingerprint_oos_or_unlabeled"
                        ),
                        "reaction_chemical_operation": operation,
                    },
                    "organic_cofactor_scores": {
                        "available_classes": ["flavin", "heme", "plp"],
                        "score_values_materialized_in_source_sidecar": True,
                    },
                    "inorganic_cofactor_loci": {
                        "metal_ion_locus": metal_status,
                    },
                    "feature_guardrails": {
                        "fingerprint_id_excluded_from_features": True,
                        "label_type_excluded_from_features": True,
                        "stratum_excluded_from_features": True,
                        "heldout_row": False,
                    },
                }

            rows = [
                feature_row("m_csa:1", "train", 2, "op_a", "no_metal_context_detected"),
                feature_row("m_csa:2", "train", 3, "op_a", "no_metal_context_detected"),
                feature_row("m_csa:3", "train", 8, "op_b", "proximal_metal_context_available"),
                feature_row("m_csa:4", "train", 18, None, "no_metal_context_detected"),
                feature_row("m_csa:5", "calibration", 2, "op_a", "no_metal_context_detected"),
                feature_row("m_csa:6", "calibration", 8, "op_b", "proximal_metal_context_available"),
                feature_row("m_csa:7", "calibration", 18, None, "no_metal_context_detected"),
                feature_row("m_csa:8", "calibration", 20, None, "no_metal_context_detected"),
            ]
            feature_contract.write_text(
                json.dumps(
                    {
                        "feature_rows": rows,
                        "counts": {"heldout_excluded_rows": 2},
                    }
                ),
                encoding="utf-8",
            )
            strict_audit.write_text(
                json.dumps(
                    {
                        "status": (
                            "mechanism_feature_embedding_feature_contract_"
                            "strict_audit_passed_no_model_fit"
                        ),
                        "counts": {"critical_violation_total": 0},
                    }
                ),
                encoding="utf-8",
            )
            label_manifest.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "label_type": "seed_fingerprint",
                                "fingerprint_id": "fp_a",
                            },
                            {
                                "entry_id": "m_csa:2",
                                "label_type": "seed_fingerprint",
                                "fingerprint_id": "fp_a",
                            },
                            {
                                "entry_id": "m_csa:3",
                                "label_type": "seed_fingerprint",
                                "fingerprint_id": "fp_b",
                            },
                            {
                                "entry_id": "m_csa:4",
                                "label_type": "out_of_scope",
                                "fingerprint_id": None,
                            },
                            {
                                "entry_id": "m_csa:5",
                                "label_type": "seed_fingerprint",
                                "fingerprint_id": "fp_a",
                            },
                            {
                                "entry_id": "m_csa:6",
                                "label_type": "seed_fingerprint",
                                "fingerprint_id": "fp_b",
                            },
                            {
                                "entry_id": "m_csa:7",
                                "label_type": "out_of_scope",
                                "fingerprint_id": None,
                            },
                            {
                                "entry_id": "m_csa:8",
                                "label_type": "out_of_scope",
                                "fingerprint_id": None,
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            cofactor_records = []
            for row in rows:
                for cofactor_class, score in (
                    ("flavin", 0.1),
                    ("heme", 0.2),
                    ("plp", 0.3),
                ):
                    cofactor_records.append(
                        {
                            "entry_id": row["entry_id"],
                            "cofactor_class": cofactor_class,
                            "selected_score": score,
                        }
                    )
            cofactor_sidecar.write_text(
                json.dumps({"row_class_records": cofactor_records}),
                encoding="utf-8",
            )

            audit = build_mechanism_feature_embedding_pilot(
                feature_contract_path=feature_contract,
                feature_contract_strict_audit_path=strict_audit,
                label_manifest_path=label_manifest,
                selected_organic_cofactor_sidecar_path=cofactor_sidecar,
            )

        self.assertEqual(
            audit["status"],
            "mechanism_feature_embedding_pilot_fit_train_cal_ready",
        )
        self.assertEqual(audit["counts"]["variants"], 2)
        self.assertEqual(audit["counts"]["train_rows"], 4)
        self.assertEqual(audit["counts"]["calibration_rows"], 4)
        self.assertTrue(audit["guardrails"]["model_weights_fit_or_refit"])
        self.assertEqual(audit["guardrails"]["model_fit_rows"], "train_only")
        self.assertFalse(audit["guardrails"]["heldout_rows_evaluated"])
        self.assertEqual(
            {
                variant["variant_name"]
                for variant in audit["pilot_variants"]
            },
            {
                "full_contract_with_reaction_template",
                "no_reaction_template_ablation",
            },
        )
        self.assertTrue(
            all(
                variant["calibration_selected_threshold"]["threshold"] is not None
                for variant in audit["pilot_variants"]
            )
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

    def test_family_panel_high_value_glycyl_readiness_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            packet = root / "packet.json"
            readout = root / "readout.json"
            bond_schema = root / "bond_schema.json"
            fold_provenance = root / "fold_provenance.json"
            packet.write_text(
                json.dumps(
                    {
                        "row_evidence": [
                            {
                                "entry_id": "m_csa:30",
                                "split_assignment": "heldout",
                                "benchmark_role": "oos_tier::unknown_oos",
                                "evidence_role": "cofactor-confounded OOS control",
                                "predicted_geometry_status": "ok",
                                "predicted_geometry_top1": {
                                    "fingerprint_id": "metal_dependent_hydrolase",
                                    "score": 0.2616,
                                },
                                "selected_organic_cofactor_max": 0.589255,
                                "predicted_structure_fold_channel": {
                                    "nearest_atlas_entry_id": "m_csa:11",
                                    "nearest_atlas_true_fingerprint_id": "metal_dependent_hydrolase",
                                    "nearest_atlas_tm_score": 0.4988,
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            readout.write_text(
                json.dumps(
                    {
                        "row_scores": [
                            {
                                "entry_id": "m_csa:30",
                                "research_gate_status": "abstained_at_research_threshold",
                                "primary_threshold": 0.44155,
                                "primary_threshold_margin": -0.06135,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            bond_schema.write_text(
                json.dumps(
                    {
                        "row_materialization_queue": [
                            {
                                "entry_id": "m_csa:30",
                                "row_specific_bond_change_status": (
                                    "not_applicable_no_mechanism_fingerprint_oos_or_unlabeled"
                                ),
                                "ready_for_embedding_pilot": False,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            fold_provenance.write_text(
                json.dumps(
                    {
                        "counts": {
                            "unique_coordinate_files_missing": 299,
                            "result_files_parseable": True,
                        }
                    }
                ),
                encoding="utf-8",
            )

            audit = build_family_panel_high_value_glycyl_radical_readiness_packet(
                evidence_packet_path=packet,
                fold_augmented_readout_path=readout,
                row_specific_bond_change_schema_path=bond_schema,
                fold_coordinate_provenance_audit_path=fold_provenance,
            )

        self.assertEqual(
            audit["status"],
            "glycyl_radical_panel_ready_as_oos_boundary_review_only",
        )
        self.assertEqual(audit["counts"]["panel_rows"], 1)
        self.assertEqual(audit["counts"]["score_complete_rows"], 1)
        self.assertEqual(audit["counts"]["abstained_at_research_threshold"], 1)
        self.assertFalse(audit["panel_decision"]["promotion_or_import_ready"])
        self.assertEqual(
            audit["row_readiness"][0]["promotion_readiness"],
            "not_ready_review_only_oos_boundary_control",
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

    def test_predicted_atlas_vs_fold_operating_grid_delta_compares_targets(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            geometry = root / "geometry_grid.json"
            fold = root / "fold_grid.json"
            geometry.write_text(
                json.dumps(
                    {
                        "status": (
                            "predicted_atlas_geometry_novelty_operating_grid_"
                            "ready_review_only"
                        ),
                        "best_by_retention_target": {
                            "0.90": {
                                "signal": "geometry_signal",
                                "threshold": 0.1,
                                "inscope_retain_recall": 0.91,
                                "oos_abstain_recall": 0.2,
                                "confounded_abstain_recall": 0.3,
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            fold.write_text(
                json.dumps(
                    {
                        "status": (
                            "predicted_structure_fold_augmented_novelty_"
                            "operating_grid_ready_review_only"
                        ),
                        "best_by_retention_target": {
                            "0.90": {
                                "signal": "fold_signal",
                                "threshold": 0.4,
                                "inscope_retain_recall": 0.91,
                                "oos_abstain_recall": 0.8,
                                "confounded_abstain_recall": 0.9,
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            audit = build_predicted_atlas_vs_fold_novelty_operating_grid_delta(
                geometry_operating_grid_path=geometry,
                fold_operating_grid_path=fold,
            )

        self.assertEqual(
            audit["status"],
            "predicted_atlas_vs_fold_novelty_delta_ready_review_only",
        )
        self.assertEqual(audit["counts"]["shared_retention_targets"], 1)
        self.assertEqual(audit["counts"]["targets_with_oos_abstain_lift"], 1)
        self.assertEqual(audit["target_90_summary"]["oos_abstain_recall_delta"], 0.6)
        self.assertFalse(audit["guardrails"]["production_thresholds_changed"])

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

    def test_predicted_structure_fold_channel_coordinate_provenance_audit(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            fold_channel = root / "fold_channel.json"
            contract_audit = root / "contract_audit.json"
            all_tsv = root / "all.tsv"
            priority_tsv = root / "priority.tsv"
            existing_cif = root / "coords" / "atlas" / "afdb_P11111_v6.cif"
            missing_priority = root / "coords" / "queries" / "afdb_P22222_v6.cif"
            missing_atlas = root / "coords" / "atlas" / "afdb_P33333_v6.cif"
            existing_cif.parent.mkdir(parents=True)
            existing_cif.write_text("data_AF-P11111-F1-model_v6\n", encoding="utf-8")
            all_tsv.write_text("q\tt\t0.1\t0.2\t0.7\t0.6\t40\n", encoding="utf-8")
            priority_tsv.write_text(
                "q\tt\t0.1\t0.2\t0.7\t0.6\t40\n",
                encoding="utf-8",
            )
            fold_channel.write_text(
                json.dumps(
                    {
                        "foldseek_input_manifest": {
                            "coordinate_request_groups": {
                                "all_heldout_queries_when_cheap": [
                                    {
                                        "accession": "P11111",
                                        "predicted_pdb_id": "AF-P11111-F1-model_v6",
                                        "entry_ids": ["m_csa:1"],
                                        "role": "atlas_in_distribution_target",
                                        "expected_local_path": str(existing_cif),
                                        "url": "https://example.test/P11111.cif",
                                        "download_command": "curl P11111",
                                        "local_file_exists": False,
                                    },
                                    {
                                        "accession": "P22222",
                                        "predicted_pdb_id": "AF-P22222-F1-model_v6",
                                        "entry_ids": ["m_csa:30"],
                                        "role": "all_heldout_query_when_cheap",
                                        "expected_local_path": str(missing_priority),
                                        "url": "https://example.test/P22222.cif",
                                        "download_command": "curl P22222",
                                        "local_file_exists": False,
                                    },
                                ],
                                "atlas_in_distribution": [
                                    {
                                        "accession": "P33333",
                                        "predicted_pdb_id": "AF-P33333-F1-model_v6",
                                        "entry_ids": ["m_csa:2"],
                                        "role": "atlas_in_distribution_target",
                                        "expected_local_path": str(missing_atlas),
                                        "url": "https://example.test/P33333.cif",
                                        "download_command": "curl P33333",
                                        "local_file_exists": False,
                                    }
                                ],
                                "priority_cofactor_confounded_oos_queries": [
                                    {
                                        "accession": "P22222",
                                        "predicted_pdb_id": "AF-P22222-F1-model_v6",
                                        "entry_ids": ["m_csa:30"],
                                        "role": "priority_query_cofactor_confounded_oos",
                                        "expected_local_path": str(missing_priority),
                                        "url": "https://example.test/P22222.cif",
                                        "download_command": "curl P22222",
                                        "local_file_exists": False,
                                    }
                                ],
                            }
                        },
                        "parsed_foldseek_results": {
                            "all_heldout_vs_atlas": {
                                "status": "parsed",
                                "path": str(all_tsv),
                                "summary": {
                                    "mapped_pair_count": 1,
                                    "query_entry_count_with_hits": 1,
                                },
                            },
                            "priority_cofactor_confounded_oos_vs_atlas": {
                                "status": "parsed",
                                "path": str(priority_tsv),
                                "summary": {
                                    "mapped_pair_count": 1,
                                    "query_entry_count_with_hits": 1,
                                },
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )
            contract_audit.write_text(
                json.dumps(
                    {
                        "status": "fold_channel_contract_passed_current702",
                        "counts": {
                            "critical_counts": {
                                "status_violations": 0,
                                "count_mismatches": 0,
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            audit = (
                build_predicted_structure_fold_channel_coordinate_provenance_audit(
                    predicted_structure_fold_channel_path=fold_channel,
                    contract_audit_path=contract_audit,
                )
            )

        self.assertEqual(
            audit["status"],
            "coordinate_bundle_not_persisted_results_parseable",
        )
        self.assertEqual(audit["counts"]["total_coordinate_requests"], 4)
        self.assertEqual(audit["counts"]["unique_coordinate_files_expected"], 3)
        self.assertEqual(audit["counts"]["unique_coordinate_files_observed"], 1)
        self.assertEqual(audit["counts"]["unique_coordinate_files_missing"], 2)
        self.assertEqual(audit["counts"]["unique_accessions_expected"], 3)
        self.assertEqual(
            audit["counts"]["unique_accessions_without_any_local_file"],
            2,
        )
        self.assertEqual(audit["counts"]["duplicate_coordinate_request_paths"], 1)
        self.assertEqual(audit["counts"]["duplicate_accession_requests"], 1)
        self.assertTrue(audit["counts"]["result_files_parseable"])
        self.assertEqual(audit["contract_audit"]["critical_violation_total"], 0)
        self.assertEqual(
            len(
                audit["violations"][
                    "reported_observed_local_file_exists_mismatches"
                ]
            ),
            1,
        )

    def test_predicted_structure_fold_channel_carryover_resolution_skips_rerun(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            predicted_atlas = root / "predicted_atlas.json"
            fold_signal = root / "fold_signal.json"
            fold_channel = root / "fold_channel.json"
            fold_report = root / "fold_channel.md"
            contract_audit = root / "contract_audit.json"
            coordinate_provenance = root / "coordinate_provenance.json"
            reproduction_manifest = root / "reproduction_manifest.json"

            predicted_atlas.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "entry_id": "m_csa:1",
                                "accession": "P11111",
                                "split_assignment": "in_distribution",
                                "predicted_geometry_status": "ok",
                            },
                            {
                                "entry_id": "m_csa:30",
                                "accession": "P22222",
                                "split_assignment": "heldout",
                                "predicted_geometry_status": "ok",
                            },
                            {
                                "entry_id": "m_csa:40",
                                "accession": "P33333",
                                "split_assignment": "heldout",
                                "predicted_geometry_status": "ok",
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
            fold_channel.write_text(
                json.dumps(
                    {
                        "status": "computed_all_heldout_foldseek_scores",
                        "parsed_foldseek_results": {
                            "all_heldout_vs_atlas": {
                                "status": "parsed",
                                "summary": {"query_entry_count_with_hits": 2},
                            },
                            "priority_cofactor_confounded_oos_vs_atlas": {
                                "status": "parsed",
                                "summary": {"query_entry_count_with_hits": 1},
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )
            fold_report.write_text("# fold report\n", encoding="utf-8")
            contract_audit.write_text(
                json.dumps(
                    {
                        "status": "fold_channel_contract_passed_current702",
                        "counts": {
                            "critical_counts": {
                                "status_violations": 0,
                                "count_mismatches": 0,
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            coordinate_provenance.write_text(
                json.dumps(
                    {
                        "status": "coordinate_bundle_not_persisted_results_parseable",
                        "counts": {
                            "result_files_parseable": True,
                            "unique_coordinate_files_expected": 3,
                            "unique_coordinate_files_missing": 3,
                            "unique_accessions_without_any_local_file": 3,
                        },
                    }
                ),
                encoding="utf-8",
            )
            reproduction_manifest.write_text(
                json.dumps(
                    {
                        "status": "fold_channel_reproduction_manifest_ready_missing_coordinates",
                        "counts": {
                            "result_files_parseable": True,
                        },
                    }
                ),
                encoding="utf-8",
            )

            audit = build_predicted_structure_fold_channel_carryover_resolution(
                predicted_geometry_atlas_path=predicted_atlas,
                fold_level_signal_path=fold_signal,
                predicted_structure_fold_channel_path=fold_channel,
                contract_audit_path=contract_audit,
                coordinate_provenance_audit_path=coordinate_provenance,
                reproduction_manifest_path=reproduction_manifest,
                predicted_structure_fold_channel_report_path=fold_report,
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
        self.assertIn(
            "persistent_afdb_v6_coordinate_bundle_missing",
            resolution["remaining_blocker_classes"],
        )
        self.assertEqual(audit["counts"]["heldout_rows_ok"], 2)
        self.assertEqual(audit["counts"]["priority_cofactor_confounded_oos_rows"], 1)
        self.assertEqual(audit["counts"]["contract_critical_violation_total"], 0)


if __name__ == "__main__":
    unittest.main()
