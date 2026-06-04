from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.lever2_mechanism_incremental_readout import (
    build_lever2_current_extended_oos_mechanism_overlap_readout,
    build_lever2_mechanism_feature_incremental_readout,
    build_lever2_source_free_electron_flow_split_alignment_readout,
    build_lever2_source_free_partial_surface_current_split_portability_readout,
)
from catalytic_earth.northstar_next_levers import (
    build_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_train_cal_projection_readout as build_projection_readout,
)


class Lever2MechanismIncrementalReadoutTests(unittest.TestCase):
    def test_partial_surface_current_split_portability_measures_union_overlap(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            current_measured_path = root / "current_measured.json"
            current_surface_path = root / "current_surface.json"
            current_primary_path = root / "current_primary.json"
            candidate_surface_path = root / "candidate_surface.json"
            event_axis_path = root / "event_axis.json"
            locator_path = root / "locator.json"

            current_measured_path.write_text(
                json.dumps(
                    {
                        "fixed_operating_point": {
                            "channel": "combined_mean_geometry_fold",
                            "threshold": 0.5,
                        }
                    }
                ),
                encoding="utf-8",
            )
            current_primary_path.write_text(
                json.dumps(
                    {
                        "calibration_row_scores": [
                            {
                                "entry_id": "m_csa:1",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.8
                                },
                            },
                            {
                                "entry_id": "m_csa:2",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.7
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            current_surface_path.write_text(
                json.dumps(
                    {
                        "candidate_row_scores": [
                            {
                                "entry_id": "m_csa:10",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.9
                                },
                            },
                            {
                                "entry_id": "m_csa:11",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.4
                                },
                            },
                            {"entry_id": "m_csa:12", "channel_scores": {}},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            candidate_surface_path.write_text(
                json.dumps(
                    {
                        "candidate_projection_rows": [
                            {"entry_id": "m_csa:1"},
                            {"entry_id": "m_csa:10"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            event_axis_path.write_text(
                json.dumps(
                    {
                        "materialization_rows": [
                            {
                                "entry_id": "m_csa:11",
                                "critical_violations": [],
                                "source_free_event_axis_status": (
                                    "source_free_event_axis_linker_ready"
                                ),
                            },
                            {
                                "entry_id": "m_csa:12",
                                "critical_violations": [],
                                "source_free_event_axis_status": (
                                    "source_free_event_axis_linker_ready"
                                ),
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            locator_path.write_text(
                json.dumps(
                    {
                        "row_decisions": [
                            {
                                "entry_id": "m_csa:2",
                                "approved_locator_sidecar_written": True,
                                "decision": "materialized_to_audited_locator_dir",
                                "critical_violations": [],
                            },
                            {
                                "entry_id": "m_csa:99",
                                "approved_locator_sidecar_written": False,
                                "decision": "held_for_review",
                                "critical_violations": [],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            readout = (
                build_lever2_source_free_partial_surface_current_split_portability_readout(
                    current_measured_readout_path=current_measured_path,
                    current_extended_oos_surface_path=current_surface_path,
                    current_in_scope_threshold_contract_path=current_primary_path,
                    source_free_projection_repair_candidate_surface_path=(
                        candidate_surface_path
                    ),
                    source_free_event_axis_linker_materialization_gate_path=(
                        event_axis_path
                    ),
                    source_free_locator_rewrite_materialization_gate_path=(
                        locator_path
                    ),
                    artifact_id="test_partial_surface_portability",
                )
            )

        self.assertEqual(
            readout["status"],
            "lever2_source_free_partial_surface_current_split_portability_"
            "readout_research_only_overlap_available",
        )
        self.assertEqual(readout["result_class"], "research_only")
        self.assertEqual(readout["counts"]["current_primary_rows"], 2)
        self.assertEqual(readout["counts"]["current_extended_scored_oos_rows"], 2)
        self.assertEqual(readout["counts"]["current_extended_unscored_oos_rows"], 1)
        self.assertEqual(
            readout["counts"]["source_free_partial_surface_union_rows"], 5
        )
        self.assertEqual(readout["counts"]["union_current_primary_overlap_rows"], 2)
        self.assertEqual(
            readout["counts"]["union_current_retained_oos_overlap_rows"], 1
        )
        self.assertEqual(
            readout["counts"]["union_current_abstained_oos_overlap_rows"], 1
        )
        self.assertFalse(
            readout["decision"]["route_negative_for_existing_partial_surface_reuse"]
        )
        missing = readout["missing_evidence_rows"]
        self.assertEqual(
            missing["current_primary_rows_requiring_source_free_partial_surface"], []
        )

    def test_current_extended_oos_overlap_measures_signal_without_primary_gate(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            current_measured_path = root / "current_measured.json"
            current_surface_path = root / "current_surface.json"
            mechanism_path = root / "mechanism.json"
            mechanism_contract_path = root / "mechanism_contract.json"
            current_primary_path = root / "current_primary.json"
            sidecar_path = root / "sidecar.json"

            current_measured_path.write_text(
                json.dumps(
                    {
                        "fixed_operating_point": {
                            "channel": "combined_mean_geometry_fold",
                            "threshold": 0.5,
                        },
                        "measured_readout": {
                            "train_cal_oos_current_scored_surface": {
                                "row_count": 4,
                                "abstained": 1,
                                "retained": 3,
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            current_surface_path.write_text(
                json.dumps(
                    {
                        "candidate_row_scores": [
                            {
                                "entry_id": "m_csa:10",
                                "accession": "P00010",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.4
                                },
                            },
                            {
                                "entry_id": "m_csa:11",
                                "accession": "P00011",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.7
                                },
                            },
                            {
                                "entry_id": "m_csa:12",
                                "accession": "P00012",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.8
                                },
                            },
                            {
                                "entry_id": "m_csa:99",
                                "accession": "P00099",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.9
                                },
                            },
                            {
                                "entry_id": "m_csa:100",
                                "accession": "P00100",
                                "channel_scores": {},
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            mechanism_path.write_text(
                json.dumps(
                    {
                        "residual_variant": {
                            "calibration_selected_residual_threshold": {
                                "threshold": 3.0
                            }
                        },
                        "scored_rows": {
                            "calibration": [
                                {
                                    "entry_id": "m_csa:1",
                                    "is_primary": True,
                                    "out_of_atlas_span_residual": 1.0,
                                },
                                {
                                    "entry_id": "m_csa:10",
                                    "is_primary": False,
                                    "out_of_atlas_span_residual": 4.0,
                                },
                                {
                                    "entry_id": "m_csa:11",
                                    "is_primary": False,
                                    "out_of_atlas_span_residual": 4.5,
                                },
                                {
                                    "entry_id": "m_csa:12",
                                    "is_primary": False,
                                    "out_of_atlas_span_residual": 2.0,
                                },
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            mechanism_contract_path.write_text(
                json.dumps(
                    {"calibration_contract": {"residual_distance": {"threshold": 3.0}}}
                ),
                encoding="utf-8",
            )
            current_primary_path.write_text(
                json.dumps(
                    {
                        "calibration_row_scores": [
                            {
                                "entry_id": "m_csa:20",
                                "accession": "P00020",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.8
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "m_csa:10",
                                "row_specific_event_features": {
                                    "has_bond_change_event": True,
                                    "has_proton_transfer_event": False,
                                    "has_electron_transfer_event": False,
                                    "bond_change_event_count": 1,
                                    "proton_transfer_count": 0,
                                    "electron_transfer_count": 0,
                                    "event_count": 1,
                                },
                            },
                            {
                                "entry_id": "m_csa:11",
                                "row_specific_event_features": {
                                    "has_bond_change_event": True,
                                    "has_proton_transfer_event": True,
                                    "has_electron_transfer_event": True,
                                    "bond_change_event_count": 2,
                                    "proton_transfer_count": 1,
                                    "electron_transfer_count": 1,
                                    "event_count": 3,
                                },
                            },
                            {
                                "entry_id": "m_csa:12",
                                "row_specific_event_features": {
                                    "has_bond_change_event": False,
                                    "has_proton_transfer_event": True,
                                    "has_electron_transfer_event": False,
                                    "bond_change_event_count": 0,
                                    "proton_transfer_count": 1,
                                    "electron_transfer_count": 0,
                                    "event_count": 1,
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_current_extended_oos_mechanism_overlap_readout(
                current_measured_readout_path=current_measured_path,
                current_extended_oos_surface_path=current_surface_path,
                mechanism_no_template_rerun_path=mechanism_path,
                mechanism_operating_point_contract_path=mechanism_contract_path,
                current_in_scope_threshold_contract_path=current_primary_path,
                train_cal_feature_sidecar_path=sidecar_path,
                artifact_id="test_current_extended_oos_overlap",
            )

        self.assertEqual(readout["result_class"], "research_only")
        self.assertEqual(
            readout["status"],
            "lever2_current_extended_oos_mechanism_overlap_readout_research_only",
        )
        self.assertEqual(readout["counts"]["current_extended_scored_oos_rows"], 4)
        self.assertEqual(readout["counts"]["current_extended_unscored_oos_rows"], 1)
        self.assertEqual(readout["counts"]["current_extended_oos_overlap_rows"], 3)
        self.assertEqual(
            readout["counts"]["current_retained_oos_caught_by_mechanism"], 1
        )
        self.assertEqual(readout["counts"]["valid_primary_overlap_rows"], 0)
        self.assertEqual(
            readout["counts"][
                "missing_current_extended_retained_oos_mechanism_feature_rows"
            ],
            1,
        )
        overlap = readout["measured_readout"]["current_extended_oos_overlap_rows"]
        self.assertEqual(overlap["current_surface_abstained"], 1)
        self.assertEqual(overlap["mechanism_surface_abstained"], 2)
        self.assertEqual(overlap["union_or_gate_abstained"], 2)
        self.assertEqual(overlap["current_retained_oos_caught_by_mechanism"], 1)
        event_summary = readout["measured_readout"]["event_feature_overlap_summary"]
        self.assertEqual(
            event_summary["current_retained_overlap_rows"][
                "with_electron_transfer_event"
            ],
            1,
        )
        self.assertFalse(
            readout["decision"]["valid_integrated_operating_point_measurable"]
        )
        self.assertFalse(
            readout["decision"]["adds_operating_point_value_beyond_current_surface"]
        )

    def test_measures_oos_lift_but_blocks_without_valid_primary_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            mechanism_path = root / "mechanism.json"
            current_primary_path = root / "current_primary.json"
            expanded_path = root / "expanded.json"
            mechanism_contract_path = root / "mechanism_contract.json"

            mechanism_path.write_text(
                json.dumps(
                    {
                        "residual_variant": {
                            "calibration_selected_residual_threshold": {
                                "threshold": 3.0,
                                "primary_rows": 2,
                                "primary_retain_recall": 1.0,
                                "oos_rows": 3,
                                "oos_abstain_recall": 0.666667,
                            }
                        },
                        "scored_rows": {
                            "calibration": [
                                {
                                    "entry_id": "m_csa:1",
                                    "is_primary": True,
                                    "out_of_atlas_span_residual": 1.0,
                                },
                                {
                                    "entry_id": "m_csa:2",
                                    "is_primary": True,
                                    "out_of_atlas_span_residual": 1.2,
                                },
                                {
                                    "entry_id": "m_csa:10",
                                    "is_primary": False,
                                    "out_of_atlas_span_residual": 4.0,
                                },
                                {
                                    "entry_id": "m_csa:11",
                                    "is_primary": False,
                                    "out_of_atlas_span_residual": 4.5,
                                },
                                {
                                    "entry_id": "m_csa:12",
                                    "is_primary": False,
                                    "out_of_atlas_span_residual": 2.0,
                                },
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            mechanism_contract_path.write_text(
                json.dumps(
                    {"calibration_contract": {"residual_distance": {"threshold": 3.0}}}
                ),
                encoding="utf-8",
            )
            current_primary_path.write_text(
                json.dumps(
                    {
                        "calibration_row_scores": [
                            {
                                "entry_id": "m_csa:20",
                                "accession": "P00020",
                                "channel_scores": {"combined_mean_geometry_fold": 0.8},
                            }
                        ],
                        "train_cal_partition": {
                            "train_entry_ids": ["m_csa:1", "m_csa:2"],
                            "calibration_entry_ids": ["m_csa:20"],
                        },
                    }
                ),
                encoding="utf-8",
            )
            expanded_path.write_text(
                json.dumps(
                    {
                        "primary_channel_readout": {
                            "channel": "combined_mean_geometry_fold",
                            "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain": {
                                "threshold": 0.5,
                                "calibration_in_scope_retain_recall": 1.0,
                                "calibration_in_scope_retained": 1,
                                "calibration_in_scope_total": 1,
                                "calibration_oos_abstain_recall": 0.5,
                                "calibration_oos_abstained": 1,
                                "calibration_oos_total": 2,
                            },
                        },
                        "calibration_oos_negative_row_scores": [
                            {
                                "entry_id": "m_csa:10",
                                "channel_scores": {"combined_mean_geometry_fold": 0.4},
                            },
                            {
                                "entry_id": "m_csa:11",
                                "channel_scores": {"combined_mean_geometry_fold": 0.6},
                            },
                            {
                                "entry_id": "m_csa:99",
                                "accession": "P00099",
                                "channel_scores": {"combined_mean_geometry_fold": 0.7},
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_mechanism_feature_incremental_readout(
                mechanism_no_template_rerun_path=mechanism_path,
                mechanism_operating_point_contract_path=mechanism_contract_path,
                current_in_scope_threshold_contract_path=current_primary_path,
                expanded_oos_calibrated_threshold_contract_path=expanded_path,
                artifact_id="test_lever2_incremental",
            )

        self.assertEqual(readout["artifact_id"], "test_lever2_incremental")
        self.assertEqual(
            readout["status"],
            "lever2_mechanism_feature_incremental_readout_research_only_overlap_blocked",
        )
        self.assertEqual(readout["result_class"], "research_only")
        self.assertEqual(readout["counts"]["oos_overlap_rows"], 2)
        self.assertEqual(readout["counts"]["valid_primary_overlap_rows"], 0)
        self.assertEqual(
            readout["counts"]["missing_current_calibration_primary_mechanism_feature_rows"],
            1,
        )
        self.assertEqual(
            readout["counts"]["missing_current_calibration_oos_mechanism_feature_rows"],
            1,
        )
        self.assertEqual(
            readout["counts"][
                "mechanism_primary_rows_excluded_as_current_surface_train_targets"
            ],
            2,
        )
        overlap = readout["measured_readout"]["overlap_oos_rows"]
        self.assertEqual(overlap["current_surface_abstained"], 1)
        self.assertEqual(overlap["mechanism_surface_abstained"], 2)
        self.assertEqual(overlap["union_or_gate_abstained"], 2)
        self.assertEqual(overlap["current_retained_oos_caught_by_mechanism"], 1)
        missing_rows = readout["missing_evidence_rows"]
        missing_primary = missing_rows[
            "current_calibration_primary_rows_requiring_source_free_mechanism_features"
        ]
        missing_oos = missing_rows[
            "current_calibration_oos_rows_requiring_source_free_mechanism_features"
        ]
        self.assertEqual([row["entry_id"] for row in missing_primary], ["m_csa:20"])
        self.assertEqual(missing_primary[0]["accession"], "P00020")
        self.assertEqual(missing_primary[0]["current_surface_score"], 0.8)
        self.assertIn("calibration_primary", missing_primary[0]["reason"])
        self.assertEqual([row["entry_id"] for row in missing_oos], ["m_csa:99"])
        self.assertEqual(missing_oos[0]["accession"], "P00099")
        self.assertEqual(missing_oos[0]["current_surface_score"], 0.7)
        self.assertFalse(missing_oos[0]["current_surface_abstains"])
        self.assertIn("calibration_oos", missing_oos[0]["reason"])
        self.assertFalse(
            readout["decision"]["valid_integrated_operating_point_measurable"]
        )
        self.assertFalse(
            readout["decision"]["adds_operating_point_value_beyond_current_surface"]
        )

    def test_source_free_projection_readout_marks_incomplete_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sidecar_path = root / "sidecar.json"
            guardrail_path = root / "guardrail.json"
            labels_path = root / "labels.json"
            candidate_path = root / "candidate.json"
            full_rerun_path = root / "full.json"
            current_primary_path = root / "current_primary.json"
            expanded_oos_path = root / "expanded_oos.json"

            feature_rows = [
                {
                    "entry_id": "m_csa:1",
                    "assigned_embedding_split": "train",
                    "row_specific_event_features": {"f_projected": 0, "f_missing": 1},
                },
                {
                    "entry_id": "m_csa:2",
                    "assigned_embedding_split": "train",
                    "row_specific_event_features": {"f_projected": 1, "f_missing": 0},
                },
                {
                    "entry_id": "m_csa:3",
                    "assigned_embedding_split": "calibration",
                    "row_specific_event_features": {"f_projected": 0, "f_missing": 1},
                },
                {
                    "entry_id": "m_csa:4",
                    "assigned_embedding_split": "calibration",
                    "row_specific_event_features": {"f_projected": 1, "f_missing": 0},
                },
            ]
            sidecar_path.write_text(
                json.dumps({"feature_rows": feature_rows}), encoding="utf-8"
            )
            guardrail_path.write_text(
                json.dumps(
                    {
                        "decision": {"safe_to_run_no_template_methods_now": True},
                        "counts": {"critical_violation_total": 0},
                    }
                ),
                encoding="utf-8",
            )
            labels_path.write_text(
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
                                "fingerprint_id": "fp_b",
                            },
                            {
                                "entry_id": "m_csa:3",
                                "label_type": "seed_fingerprint",
                                "fingerprint_id": "fp_a",
                            },
                            {
                                "entry_id": "m_csa:4",
                                "label_type": "out_of_scope",
                                "fingerprint_id": None,
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            candidate_path.write_text(
                json.dumps(
                    {
                        "status": "candidate_surface_partial",
                        "candidate_projection_rows": [
                            {
                                "entry_id": "m_csa:3",
                                "candidate_projected_event_features": {
                                    "f_projected": 0
                                },
                            },
                            {
                                "entry_id": "m_csa:4",
                                "candidate_projected_event_features": {
                                    "f_projected": 1
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            current_primary_path.write_text(
                json.dumps(
                    {
                        "calibration_row_scores": [
                            {"entry_id": "m_csa:3"},
                            {"entry_id": "m_csa:30"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            expanded_oos_path.write_text(
                json.dumps(
                    {
                        "calibration_oos_negative_row_scores": [
                            {"entry_id": "m_csa:4"},
                            {"entry_id": "m_csa:40"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            full_rerun_path.write_text(
                json.dumps(
                    {
                        "feature_fields": ["f_projected", "f_missing"],
                        "centroid_variant": {"calibration_summary": {}},
                        "residual_variant": {
                            "calibration_selected_residual_threshold": {
                                "oos_abstain_recall": 0.8,
                                "primary_retain_recall": 1.0,
                            },
                            "calibration_summary": {
                                "auc_oos_gt_primary": 0.8,
                                "oos_rows": 1,
                                "primary_rows": 1,
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )

            readout = build_projection_readout(
                train_cal_feature_sidecar_path=sidecar_path,
                train_cal_feature_guardrail_path=guardrail_path,
                label_manifest_path=labels_path,
                source_free_projection_repair_candidate_surface_path=candidate_path,
                full_no_template_rerun_path=full_rerun_path,
                current_in_scope_threshold_contract_path=current_primary_path,
                expanded_oos_calibrated_threshold_contract_path=expanded_oos_path,
            )

        self.assertEqual(
            readout["counts"]["source_free_projected_train_cal_feature_fields"],
            1,
        )
        self.assertEqual(readout["counts"]["frozen_full_surface_feature_fields"], 2)
        self.assertEqual(readout["counts"]["missing_frozen_feature_fields"], 1)
        self.assertEqual(
            readout["counts"][
                "source_free_candidate_projection_overlap_primary_rows"
            ],
            1,
        )
        self.assertEqual(
            readout["counts"]["source_free_candidate_projection_overlap_oos_rows"],
            1,
        )
        split_context = readout["measured_readout"]["split_alignment_context"]
        self.assertEqual(
            split_context["full_row_specific_feature_overlap_primary_entry_ids"],
            ["m_csa:3"],
        )
        self.assertEqual(
            split_context[
                "source_free_candidate_projection_overlap_oos_entry_ids"
            ],
            ["m_csa:4"],
        )
        self.assertTrue(readout["decision"]["measured_readout_available"])
        self.assertFalse(
            readout["decision"]["source_free_projection_complete_for_frozen_contract"]
        )
        self.assertTrue(
            readout["decision"]["result_classification"].endswith(
                "current_projection_incomplete"
            )
        )

    def test_electron_flow_split_alignment_prioritizes_missing_current_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            projection_path = root / "projection.json"
            incremental_path = root / "incremental.json"
            candidate_path = root / "candidate.json"
            sidecar_path = root / "sidecar.json"
            current_primary_path = root / "current_primary.json"
            expanded_oos_path = root / "expanded_oos.json"

            projection_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "axis_repair_ceiling_rows": [
                                {
                                    "variant": "current_source_free_projected_subset",
                                    "feature_field_count": 4,
                                    "primary_retain_recall": 1.0,
                                    "oos_abstain_recall": 0.5,
                                    "auc_oos_gt_primary": 0.7,
                                    "threshold": 0.1,
                                },
                                {
                                    "variant": "current_plus_missing_electron_flow",
                                    "feature_field_count": 6,
                                    "primary_retain_recall": 1.0,
                                    "oos_abstain_recall": 0.75,
                                    "auc_oos_gt_primary": 0.8,
                                    "threshold": 0.2,
                                },
                                {
                                    "variant": "full_frozen_row_specific_surface",
                                    "feature_field_count": 19,
                                    "primary_retain_recall": 1.0,
                                    "oos_abstain_recall": 0.8,
                                    "auc_oos_gt_primary": 0.82,
                                    "threshold": 0.3,
                                },
                            ],
                            "best_single_axis_repair_ceiling": {
                                "variant": "current_plus_missing_electron_flow"
                            },
                            "best_single_axis_new_oos_rows": [
                                {
                                    "entry_id": "m_csa:10",
                                    "in_current_geometry_fold_calibration_oos": False,
                                },
                                {
                                    "entry_id": "m_csa:11",
                                    "in_current_geometry_fold_calibration_oos": True,
                                },
                            ],
                            "split_alignment_context": {
                                "current_geometry_fold_calibration_primary_rows": 2,
                                "current_geometry_fold_calibration_oos_rows": 3,
                                "source_free_candidate_projection_overlap_primary_rows": 0,
                                "source_free_candidate_projection_overlap_oos_rows": 0,
                            },
                        },
                        "decision": {
                            (
                                "split_aligned_current_surface_incremental_readout_"
                                "measurable"
                            ): False
                        },
                    }
                ),
                encoding="utf-8",
            )
            incremental_path.write_text(
                json.dumps(
                    {
                        "missing_evidence_rows": {
                            (
                                "current_calibration_primary_rows_requiring_"
                                "source_free_mechanism_features"
                            ): [
                                {
                                    "entry_id": "m_csa:20",
                                    "accession": "P00020",
                                    "current_surface_score": 0.4,
                                },
                                {
                                    "entry_id": "m_csa:21",
                                    "accession": "P00021",
                                    "current_surface_score": 0.8,
                                },
                            ],
                            (
                                "current_calibration_oos_rows_requiring_"
                                "source_free_mechanism_features"
                            ): [
                                {
                                    "entry_id": "m_csa:10",
                                    "accession": "P00010",
                                    "current_surface_score": 0.9,
                                    "current_surface_abstains": False,
                                },
                                {
                                    "entry_id": "m_csa:11",
                                    "accession": "P00011",
                                    "current_surface_score": 0.2,
                                    "current_surface_abstains": True,
                                },
                                {
                                    "entry_id": "m_csa:12",
                                    "accession": "P00012",
                                    "current_surface_score": 0.7,
                                    "current_surface_abstains": False,
                                },
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )
            candidate_path.write_text(
                json.dumps(
                    {
                        "candidate_projection_rows": [
                            {"entry_id": "m_csa:10"},
                            {"entry_id": "m_csa:21"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "m_csa:10",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": True,
                                    "electron_transfer_count": 1,
                                },
                            },
                            {
                                "entry_id": "m_csa:11",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": False,
                                    "electron_transfer_count": 0,
                                },
                            },
                            {
                                "entry_id": "m_csa:12",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": False,
                                    "electron_transfer_count": 0,
                                },
                            },
                            {
                                "entry_id": "m_csa:20",
                                "assigned_embedding_split": "train",
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": True,
                                    "electron_transfer_count": 1,
                                },
                            },
                            {
                                "entry_id": "m_csa:21",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": False,
                                    "electron_transfer_count": 0,
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            current_primary_path.write_text(
                json.dumps(
                    {
                        "calibration_row_scores": [
                            {
                                "entry_id": "m_csa:20",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.4
                                },
                            },
                            {
                                "entry_id": "m_csa:21",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.8
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            expanded_oos_path.write_text(
                json.dumps(
                    {
                        "primary_channel_readout": {
                            "channel": "combined_mean_geometry_fold",
                            "selected_at_90pct_calibration_in_scope_retention_max_oos_abstain": {
                                "threshold": 0.5
                            },
                        },
                        "calibration_oos_negative_row_scores": [
                            {
                                "entry_id": "m_csa:10",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.9
                                },
                            },
                            {
                                "entry_id": "m_csa:11",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.2
                                },
                            },
                            {
                                "entry_id": "m_csa:12",
                                "channel_scores": {
                                    "combined_mean_geometry_fold": 0.7
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_split_alignment_readout(
                projection_readout_path=projection_path,
                incremental_readout_path=incremental_path,
                source_free_projection_repair_candidate_surface_path=candidate_path,
                train_cal_feature_sidecar_path=sidecar_path,
                current_in_scope_threshold_contract_path=current_primary_path,
                expanded_oos_calibrated_threshold_contract_path=expanded_oos_path,
                artifact_id="test_electron_flow_split",
            )

        self.assertEqual(readout["artifact_id"], "test_electron_flow_split")
        self.assertEqual(readout["result_class"], "research_only")
        self.assertEqual(
            readout["status"],
            "lever2_source_free_electron_flow_split_alignment_readout_research_only",
        )
        self.assertEqual(
            readout["measured_readout"]["train_cal_axis_ceiling"][
                "electron_flow_oos_abstain_recall_delta_vs_current_projected"
            ],
            0.25,
        )
        self.assertTrue(
            readout["decision"][
                "source_free_electron_flow_axis_has_train_cal_signal"
            ]
        )
        self.assertFalse(
            readout["decision"][
                "split_aligned_current_surface_incremental_readout_measurable"
            ]
        )
        self.assertEqual(
            readout["counts"]["missing_current_retained_oos_electron_flow_rows"],
            2,
        )
        self.assertEqual(
            readout["counts"]["candidate_surface_overlap_missing_retained_oos_rows"],
            1,
        )
        self.assertEqual(
            [row["entry_id"] for row in readout["acquisition_priority_rows"]],
            ["m_csa:10", "m_csa:12", "m_csa:20", "m_csa:21", "m_csa:11"],
        )
        self.assertEqual(
            readout["acquisition_priority_rows"][0]["priority_class"],
            "current_retained_oos_missing_electron_flow_axis",
        )
        raw = readout["measured_readout"][
            "raw_full_sidecar_current_surface_overlap_diagnostic"
        ]
        self.assertTrue(raw["available"])
        self.assertEqual(
            raw["counts"]["valid_current_primary_calibration_feature_overlap_rows"],
            1,
        )
        self.assertEqual(
            raw["counts"][
                "current_primary_rows_excluded_as_mechanism_train_targets"
            ],
            1,
        )
        self.assertEqual(
            raw["counts"]["current_oos_calibration_feature_overlap_rows"],
            3,
        )
        self.assertEqual(
            raw["counts"]["electron_positive_current_retained_oos_overlap_rows"],
            1,
        )


if __name__ == "__main__":
    unittest.main()
