from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.northstar_next_levers import (
    build_family_panel_evidence_packet,
    build_fold_augmented_abstention_gate,
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
