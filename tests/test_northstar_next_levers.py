from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.northstar_next_levers import (
    build_family_panel_evidence_packet,
    build_fold_augmented_abstention_gate,
    build_fold_augmented_oos_calibrated_threshold_contract,
    build_fold_augmented_abstention_threshold_contract,
    build_fold_augmented_train_cal_oos_negative_surface_blocker_resolution,
    build_fold_augmented_train_cal_oos_negative_surface_scores,
    build_fold_only_train_cal_oos_negative_surface,
    build_learned_mechanism_feature_embedding_plan,
    build_mechanism_feature_active_site_role_graph_sidecar,
    build_mechanism_feature_reaction_center_template_sidecar,
    build_predicted_atlas_geometry_novelty_variants,
    build_predicted_structure_fold_channel,
    build_selected_organic_cofactor_sidecar_schema_audit,
)


class NorthstarNextLeversTests(unittest.TestCase):
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

    def test_embedding_plan_reads_feature_sidecar_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            fingerprints = root / "fingerprints.json"
            manifest = root / "manifest.json"
            cofactor = root / "cofactor.json"
            atlas = root / "atlas.json"
            role_sidecar = root / "role.json"
            reaction_sidecar = root / "reaction.json"
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

            audit = build_learned_mechanism_feature_embedding_plan(
                mechanism_fingerprints_path=fingerprints,
                label_manifest_path=manifest,
                selected_organic_cofactor_sidecar_path=cofactor,
                predicted_geometry_atlas_path=atlas,
                active_site_role_graph_sidecar_path=role_sidecar,
                reaction_center_template_sidecar_path=reaction_sidecar,
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

    def test_family_panel_evidence_packet_is_review_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            family_targets = root / "family_targets.json"
            predicted_atlas = root / "predicted_atlas.json"
            fold_signal = root / "fold.json"
            sidecar = root / "cofactor.json"
            variants = root / "variants.json"
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

            audit = build_family_panel_evidence_packet(
                family_targets_path=family_targets,
                predicted_geometry_atlas_path=predicted_atlas,
                fold_level_signal_path=fold_signal,
                selected_organic_cofactor_sidecar_path=sidecar,
                predicted_atlas_variants_path=variants,
            )

        self.assertEqual(audit["status"], "evidence_packet_ready_review_only")
        self.assertTrue(audit["guardrails"]["proposal_only"])
        self.assertEqual(audit["row_evidence"][0]["selected_organic_cofactor_max"], 0.8)
        self.assertEqual(
            audit["row_evidence"][0]["selected_pdb_fold_proxy"]["nearest_primary_foldseek_prob"],
            0.057,
        )

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


if __name__ == "__main__":
    unittest.main()
