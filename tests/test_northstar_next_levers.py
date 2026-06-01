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
    build_learned_mechanism_feature_embedding_plan,
    build_mechanism_feature_active_site_role_graph_sidecar,
    build_mechanism_feature_reaction_center_template_sidecar,
    build_mechanism_feature_sidecar_schema_audit,
    build_predicted_atlas_geometry_novelty_variants,
    build_predicted_structure_fold_channel,
    build_predicted_structure_fold_channel_contract_audit,
    build_selected_organic_cofactor_sidecar_schema_audit,
)
from catalytic_earth.predicted_geometry_robustness import _target_manifest_row_selection


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
