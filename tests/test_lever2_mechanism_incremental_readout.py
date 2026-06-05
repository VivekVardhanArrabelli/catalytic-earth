from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.lever2_mechanism_incremental_readout import (
    build_lever2_current_extended_oos_mechanism_overlap_readout,
    build_lever2_event_axis_current_extended_frontier_readout,
    build_lever2_event_axis_loo_current_extended_frontier_readout,
    build_lever2_event_axis_primary_controlled_null_readout,
    build_lever2_event_axis_primary_controlled_rescue_readout,
    build_lever2_event_axis_primary_safe_frontier_readout,
    build_lever2_event_axis_signature_exclusion_sensitivity_readout,
    build_lever2_event_axis_signature_excluded_frontier_readout,
    build_lever2_mechanism_feature_incremental_readout,
    build_lever2_source_free_electron_flow_acquisition_ceiling_readout,
    build_lever2_source_free_electron_flow_approval_import_dry_run_readout,
    build_lever2_source_free_electron_flow_approval_import_smoke_review_readout,
    build_lever2_source_free_electron_flow_candidate_train_cal_bundle_readout,
    build_lever2_source_free_electron_flow_combined_direct_feature_sidecar_readout,
    build_lever2_source_free_electron_flow_coordinate_proxy_readout,
    build_lever2_source_free_electron_flow_current_split_smoke_materialization_readout,
    build_lever2_source_free_electron_flow_donor_acceptor_contact_readout,
    build_lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout,
    build_lever2_source_free_electron_flow_iron_sulfur_projection_support_readout,
    build_lever2_source_free_electron_flow_iron_sulfur_support_subset_preflight_readout,
    build_lever2_source_free_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_readout,
    build_lever2_source_free_electron_flow_pqq_current_split_sidecar_readout,
    build_lever2_source_free_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_readout,
    build_lever2_source_free_electron_flow_pqq_donor_acceptor_contact_readout,
    build_lever2_source_free_electron_flow_pqq_primitive_axis_audit,
    build_lever2_source_free_electron_flow_projection_backed_pqq_nad_feature_sidecar_readout,
    build_lever2_source_free_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_readout,
    build_lever2_source_free_electron_flow_split_alignment_readout,
    build_lever2_source_free_electron_flow_smoke_tranche_evidence_scan,
    build_lever2_source_free_electron_flow_train_cal_sidecar_candidate_readout,
    build_lever2_source_free_mechanism_axis_acquisition_ranking_readout,
    build_lever2_source_free_partial_surface_current_split_portability_readout,
)
from catalytic_earth.northstar_next_levers import (
    build_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_train_cal_projection_readout as build_projection_readout,
)


class Lever2MechanismIncrementalReadoutTests(unittest.TestCase):
    def test_event_axis_frontier_selects_calibrated_current_overlap_rule(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            mechanism_path = root / "mechanism.json"
            sidecar_path = root / "sidecar.json"
            current_overlap_path = root / "current_overlap.json"
            current_primary_path = root / "current_primary.json"
            partial_path = root / "partial.json"

            mechanism_path.write_text(
                json.dumps(
                    {
                        "scored_rows": {
                            "calibration": [
                                {"entry_id": "p1", "is_primary": True},
                                {"entry_id": "p2", "is_primary": True},
                                {"entry_id": "o1", "is_primary": False},
                                {"entry_id": "o2", "is_primary": False},
                            ],
                            "train": [
                                {"entry_id": "p3", "is_primary": True},
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )

            def features(electron_count: int = 0) -> dict[str, object]:
                return {
                    "has_electron_transfer_event": electron_count > 0,
                    "electron_transfer_count": electron_count,
                    "has_bond_change_event": False,
                    "bond_change_event_count": 0,
                    "bond_broken_count": 0,
                    "bond_formed_count": 0,
                    "bond_order_changed_count": 0,
                    "has_proton_transfer_event": False,
                    "proton_transfer_count": 0,
                    "event_count": 0,
                    "multi_event_mechanism_flag": False,
                    "mapped_active_site_residue_count": 0,
                    "unique_mapped_active_site_residue_count": 0,
                    "high_confidence_event_count": 0,
                    "medium_confidence_event_count": 0,
                    "low_confidence_event_count": 0,
                    "unknown_confidence_event_count": 0,
                }

            sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "p1",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(),
                            },
                            {
                                "entry_id": "p2",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(),
                            },
                            {
                                "entry_id": "o1",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(2),
                            },
                            {
                                "entry_id": "o2",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(),
                            },
                            {
                                "entry_id": "p3",
                                "assigned_embedding_split": "train",
                                "row_specific_event_features": features(),
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            current_overlap_path.write_text(
                json.dumps(
                    {
                        "fixed_operating_points": {
                            "current_surface": {
                                "channel": "combined_mean_geometry_fold",
                                "threshold": 0.5,
                            }
                        },
                        "row_readouts": {
                            "current_extended_oos_overlap_rows": [
                                {
                                    "entry_id": "o1",
                                    "current_surface_score": 0.7,
                                    "current_surface_abstains": False,
                                },
                                {
                                    "entry_id": "o2",
                                    "current_surface_score": 0.4,
                                    "current_surface_abstains": True,
                                },
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            current_primary_path.write_text(
                json.dumps(
                    {
                        "calibration_row_scores": [
                            {"entry_id": "p1"},
                            {"entry_id": "p3"},
                            {"entry_id": "p4"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            partial_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "current_retained_oos_rows": 10,
                            "missing_current_primary_source_free_partial_surface_rows": 3,
                            "missing_current_retained_oos_source_free_partial_surface_rows": 10,
                            "union_current_retained_oos_overlap_rows": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_event_axis_current_extended_frontier_readout(
                mechanism_no_template_rerun_path=mechanism_path,
                train_cal_feature_sidecar_path=sidecar_path,
                current_extended_oos_mechanism_overlap_readout_path=(
                    current_overlap_path
                ),
                current_in_scope_threshold_contract_path=current_primary_path,
                partial_surface_current_split_portability_readout_path=partial_path,
                artifact_id="test_event_axis_frontier",
            )

        self.assertEqual(readout["artifact_id"], "test_event_axis_frontier")
        self.assertEqual(
            readout["status"],
            "lever2_event_axis_current_extended_frontier_readout_"
            "research_only_current_extended_axis_signal",
        )
        self.assertEqual(readout["decision"]["best_axis_id"], "electron_flow")
        self.assertEqual(readout["counts"]["best_axis_current_retained_oos_catches"], 1)
        self.assertEqual(
            readout["counts"]["valid_current_primary_calibration_feature_overlap_rows"],
            1,
        )
        self.assertEqual(
            readout["counts"]["current_primary_rows_excluded_as_mechanism_train_targets"],
            1,
        )
        self.assertFalse(readout["decision"]["deployable_now"])
        self.assertTrue(
            readout["decision"]["local_event_axis_signal_beyond_current_surface"]
        )

    def test_event_axis_loo_frontier_finds_marginal_axis_signal(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            mechanism_path = root / "mechanism.json"
            sidecar_path = root / "sidecar.json"
            current_overlap_path = root / "current_overlap.json"
            current_primary_path = root / "current_primary.json"
            partial_path = root / "partial.json"

            mechanism_path.write_text(
                json.dumps(
                    {
                        "scored_rows": {
                            "calibration": [
                                {"entry_id": "p1", "is_primary": True},
                                {"entry_id": "p2", "is_primary": True},
                                {"entry_id": "o1", "is_primary": False},
                                {"entry_id": "o2", "is_primary": False},
                                {"entry_id": "o3", "is_primary": False},
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )

            def features(
                *,
                projected: int = 0,
                bond: int = 0,
            ) -> dict[str, object]:
                return {
                    "expanded_event_residue_role__event_residue_role_proton_transfer_electrostatic_stabiliser": projected,
                    "expanded_residue_code_count__residue_code_count_his_3": 0,
                    "has_proton_transfer_event": projected > 0,
                    "proton_transfer_count": projected,
                    "has_bond_change_event": bond > 0,
                    "bond_change_event_count": bond,
                    "bond_broken_count": 0,
                    "bond_formed_count": 0,
                    "bond_order_changed_count": 0,
                    "has_electron_transfer_event": False,
                    "electron_transfer_count": 0,
                    "event_count": 0,
                    "multi_event_mechanism_flag": False,
                    "mapped_active_site_residue_count": 0,
                    "unique_mapped_active_site_residue_count": 0,
                    "high_confidence_event_count": 0,
                    "medium_confidence_event_count": 0,
                    "low_confidence_event_count": 0,
                    "unknown_confidence_event_count": 0,
                }

            sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "p1",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(),
                            },
                            {
                                "entry_id": "p2",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(),
                            },
                            {
                                "entry_id": "o1",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(projected=1),
                            },
                            {
                                "entry_id": "o2",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(bond=1),
                            },
                            {
                                "entry_id": "o3",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(bond=1),
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            current_overlap_path.write_text(
                json.dumps(
                    {
                        "fixed_operating_points": {
                            "current_surface": {
                                "channel": "combined_mean_geometry_fold",
                                "threshold": 0.5,
                            }
                        },
                        "row_readouts": {
                            "current_extended_oos_overlap_rows": [
                                {
                                    "entry_id": "o1",
                                    "current_surface_score": 0.8,
                                    "current_surface_abstains": False,
                                },
                                {
                                    "entry_id": "o2",
                                    "current_surface_score": 0.7,
                                    "current_surface_abstains": False,
                                },
                                {
                                    "entry_id": "o3",
                                    "current_surface_score": 0.4,
                                    "current_surface_abstains": True,
                                },
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            current_primary_path.write_text(
                json.dumps(
                    {
                        "calibration_row_scores": [
                            {"entry_id": "p1"},
                            {"entry_id": "p2"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            partial_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "current_retained_oos_rows": 2,
                            "missing_current_primary_source_free_partial_surface_rows": 2,
                            "missing_current_retained_oos_source_free_partial_surface_rows": 2,
                            "union_current_retained_oos_overlap_rows": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_event_axis_loo_current_extended_frontier_readout(
                mechanism_no_template_rerun_path=mechanism_path,
                train_cal_feature_sidecar_path=sidecar_path,
                current_extended_oos_mechanism_overlap_readout_path=(
                    current_overlap_path
                ),
                current_in_scope_threshold_contract_path=current_primary_path,
                partial_surface_current_split_portability_readout_path=partial_path,
                artifact_id="test_event_axis_loo_frontier",
            )

        self.assertEqual(readout["artifact_id"], "test_event_axis_loo_frontier")
        self.assertEqual(
            readout["result_class"], "research_only_loo_marginal_axis_signal"
        )
        self.assertEqual(
            readout["counts"][
                "baseline_projected_subset_current_retained_oos_catches"
            ],
            1,
        )
        self.assertEqual(
            readout["decision"]["best_new_axis_id"],
            "bond_change",
        )
        self.assertEqual(
            readout["counts"][
                "best_projection_plus_axis_current_retained_oos_catches"
            ],
            2,
        )
        self.assertEqual(
            readout["counts"][
                "best_projection_plus_axis_marginal_current_retained_oos_catches"
            ],
            1,
        )
        self.assertEqual(
            readout["counts"]["best_projection_plus_axis_primary_loo_control_rows"],
            2,
        )
        self.assertEqual(
            readout["counts"]["best_projection_plus_axis_primary_loo_retained_rows"],
            2,
        )
        best = readout["measured_readout"]["best_projection_plus_axis"]
        self.assertEqual(
            best["current_extended_overlap"]["marginal_caught_entry_ids"], ["o2"]
        )
        pair_rows = readout["row_readouts"][
            "current_extended_overlap_by_projection_plus_axis_loo"
        ][best["projection_plus_axis_id"]]
        o2 = [row for row in pair_rows if row["entry_id"] == "o2"][0]
        self.assertEqual(o2["loo_selection_oos_rows"], 2)
        self.assertTrue(o2["current_retained_caught_beyond_projected_subset"])
        self.assertTrue(
            readout["decision"]["genuinely_new_axis_adds_beyond_projected_subset"]
        )
        self.assertTrue(
            readout["decision"][
                "best_projection_plus_axis_primary_loo_control_passes"
            ]
        )
        self.assertTrue(
            readout["guardrails"][
                "target_oos_rows_excluded_from_their_own_axis_rule_selection"
            ]
        )

    def test_event_axis_primary_safe_frontier_reports_controlled_signal(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            mechanism_path = root / "mechanism.json"
            sidecar_path = root / "sidecar.json"
            current_overlap_path = root / "current_overlap.json"
            current_primary_path = root / "current_primary.json"
            partial_path = root / "partial.json"

            mechanism_path.write_text(
                json.dumps(
                    {
                        "scored_rows": {
                            "calibration": [
                                {"entry_id": "p1", "is_primary": True},
                                {"entry_id": "p2", "is_primary": True},
                                {"entry_id": "o1", "is_primary": False},
                                {"entry_id": "o2", "is_primary": False},
                                {"entry_id": "o3", "is_primary": False},
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )

            def features(
                *,
                projected: int = 0,
                bond: int = 0,
            ) -> dict[str, object]:
                return {
                    "expanded_event_residue_role__event_residue_role_proton_transfer_electrostatic_stabiliser": projected,
                    "expanded_residue_code_count__residue_code_count_his_3": 0,
                    "has_proton_transfer_event": projected > 0,
                    "proton_transfer_count": projected,
                    "has_bond_change_event": bond > 0,
                    "bond_change_event_count": bond,
                    "bond_broken_count": 0,
                    "bond_formed_count": 0,
                    "bond_order_changed_count": 0,
                    "has_electron_transfer_event": False,
                    "electron_transfer_count": 0,
                    "event_count": 0,
                    "multi_event_mechanism_flag": False,
                    "mapped_active_site_residue_count": 0,
                    "unique_mapped_active_site_residue_count": 0,
                    "high_confidence_event_count": 0,
                    "medium_confidence_event_count": 0,
                    "low_confidence_event_count": 0,
                    "unknown_confidence_event_count": 0,
                }

            sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "p1",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(),
                            },
                            {
                                "entry_id": "p2",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(bond=1),
                            },
                            {
                                "entry_id": "o1",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(projected=1),
                            },
                            {
                                "entry_id": "o2",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(bond=2),
                            },
                            {
                                "entry_id": "o3",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(bond=2),
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            current_overlap_path.write_text(
                json.dumps(
                    {
                        "fixed_operating_points": {
                            "current_surface": {
                                "channel": "combined_mean_geometry_fold",
                                "threshold": 0.5,
                            }
                        },
                        "row_readouts": {
                            "current_extended_oos_overlap_rows": [
                                {
                                    "entry_id": "o1",
                                    "current_surface_score": 0.8,
                                    "current_surface_abstains": False,
                                },
                                {
                                    "entry_id": "o2",
                                    "current_surface_score": 0.7,
                                    "current_surface_abstains": False,
                                },
                                {
                                    "entry_id": "o3",
                                    "current_surface_score": 0.4,
                                    "current_surface_abstains": True,
                                },
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            current_primary_path.write_text(
                json.dumps(
                    {
                        "calibration_row_scores": [
                            {"entry_id": "p1"},
                            {"entry_id": "p2"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            partial_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "current_retained_oos_rows": 2,
                            "missing_current_primary_source_free_partial_surface_rows": 2,
                            "missing_current_retained_oos_source_free_partial_surface_rows": 2,
                            "union_current_retained_oos_overlap_rows": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_event_axis_primary_safe_frontier_readout(
                mechanism_no_template_rerun_path=mechanism_path,
                train_cal_feature_sidecar_path=sidecar_path,
                current_extended_oos_mechanism_overlap_readout_path=(
                    current_overlap_path
                ),
                current_in_scope_threshold_contract_path=current_primary_path,
                partial_surface_current_split_portability_readout_path=partial_path,
                artifact_id="test_event_axis_primary_safe_frontier",
            )

        self.assertEqual(
            readout["result_class"],
            "research_only_primary_safe_marginal_axis_signal",
        )
        self.assertEqual(
            readout["decision"]["best_marginal_axis_id"],
            "source_free_projected_proton_role_subset+bond_change",
        )
        self.assertEqual(
            readout["counts"][
                "best_marginal_axis_marginal_current_retained_oos_catches"
            ],
            1,
        )
        self.assertEqual(
            readout["counts"]["best_marginal_axis_primary_loo_retained_rows"],
            2,
        )
        self.assertEqual(
            readout["counts"][
                "best_primary_safe_axis_marginal_current_retained_oos_catches"
            ],
            1,
        )
        self.assertTrue(
            readout["decision"][
                "genuinely_new_axis_adds_beyond_projected_subset_before_primary_control"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "genuinely_new_axis_adds_beyond_projected_subset_under_primary_safe_control"
            ]
        )
        self.assertEqual(
            [
                row["entry_id"]
                for row in readout["missing_evidence_rows"][
                    "best_marginal_axis_primary_control_abstained_rows"
                ]
            ],
            [],
        )
        self.assertTrue(
            readout["guardrails"][
                "target_oos_and_primary_rows_excluded_from_their_own_axis_rule_selection"
            ]
        )

    def test_event_axis_primary_controlled_rescue_recovers_bond_signal(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            mechanism_path = root / "mechanism.json"
            sidecar_path = root / "sidecar.json"
            current_overlap_path = root / "current_overlap.json"
            current_primary_path = root / "current_primary.json"
            partial_path = root / "partial.json"

            mechanism_path.write_text(
                json.dumps(
                    {
                        "scored_rows": {
                            "calibration": [
                                {"entry_id": "p1", "is_primary": True},
                                {"entry_id": "p2", "is_primary": True},
                                {"entry_id": "o1", "is_primary": False},
                                {"entry_id": "o2", "is_primary": False},
                                {"entry_id": "o3", "is_primary": False},
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )

            def features(
                *,
                projected: int = 0,
                bond: int = 0,
            ) -> dict[str, object]:
                return {
                    "expanded_event_residue_role__event_residue_role_proton_transfer_electrostatic_stabiliser": projected,
                    "expanded_residue_code_count__residue_code_count_his_3": 0,
                    "has_proton_transfer_event": projected > 0,
                    "proton_transfer_count": projected,
                    "has_bond_change_event": bond > 0,
                    "bond_change_event_count": bond,
                    "bond_broken_count": 0,
                    "bond_formed_count": 0,
                    "bond_order_changed_count": 0,
                    "has_electron_transfer_event": False,
                    "electron_transfer_count": 0,
                    "event_count": 0,
                    "multi_event_mechanism_flag": False,
                    "mapped_active_site_residue_count": 0,
                    "unique_mapped_active_site_residue_count": 0,
                    "high_confidence_event_count": 0,
                    "medium_confidence_event_count": 0,
                    "low_confidence_event_count": 0,
                    "unknown_confidence_event_count": 0,
                }

            sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "p1",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(bond=2),
                            },
                            {
                                "entry_id": "p2",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(bond=2),
                            },
                            {
                                "entry_id": "o1",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(
                                    projected=2,
                                    bond=2,
                                ),
                            },
                            {
                                "entry_id": "o2",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(),
                            },
                            {
                                "entry_id": "o3",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(),
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            current_overlap_path.write_text(
                json.dumps(
                    {
                        "fixed_operating_points": {
                            "current_surface": {
                                "channel": "combined_mean_geometry_fold",
                                "threshold": 0.5,
                            }
                        },
                        "row_readouts": {
                            "current_extended_oos_overlap_rows": [
                                {
                                    "entry_id": "o1",
                                    "current_surface_score": 0.8,
                                    "current_surface_abstains": False,
                                },
                                {
                                    "entry_id": "o2",
                                    "current_surface_score": 0.7,
                                    "current_surface_abstains": False,
                                },
                                {
                                    "entry_id": "o3",
                                    "current_surface_score": 0.4,
                                    "current_surface_abstains": True,
                                },
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            current_primary_path.write_text(
                json.dumps(
                    {
                        "calibration_row_scores": [
                            {"entry_id": "p1"},
                            {"entry_id": "p2"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            partial_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "current_retained_oos_rows": 2,
                            "missing_current_primary_source_free_partial_surface_rows": 2,
                            "missing_current_retained_oos_source_free_partial_surface_rows": 2,
                            "union_current_retained_oos_overlap_rows": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_event_axis_primary_controlled_rescue_readout(
                mechanism_no_template_rerun_path=mechanism_path,
                train_cal_feature_sidecar_path=sidecar_path,
                current_extended_oos_mechanism_overlap_readout_path=(
                    current_overlap_path
                ),
                current_in_scope_threshold_contract_path=current_primary_path,
                partial_surface_current_split_portability_readout_path=partial_path,
                artifact_id="test_event_axis_primary_controlled_rescue",
            )
            null_readout = build_lever2_event_axis_primary_controlled_null_readout(
                mechanism_no_template_rerun_path=mechanism_path,
                train_cal_feature_sidecar_path=sidecar_path,
                current_extended_oos_mechanism_overlap_readout_path=(
                    current_overlap_path
                ),
                current_in_scope_threshold_contract_path=current_primary_path,
                partial_surface_current_split_portability_readout_path=partial_path,
                null_permutations=8,
                artifact_id="test_event_axis_primary_controlled_null",
            )

        self.assertEqual(
            readout["result_class"],
            "research_only_primary_controlled_marginal_axis_signal_source_free_gap",
        )
        self.assertEqual(
            readout["decision"]["best_primary_controlled_axis_id"],
            "source_free_projected_proton_role_subset+bond_change",
        )
        self.assertEqual(
            readout["counts"][
                "best_primary_controlled_axis_marginal_current_retained_oos_catches"
            ],
            1,
        )
        self.assertEqual(
            readout["counts"][
                "best_primary_controlled_axis_target_rows_passing_primary_control"
            ],
            3,
        )
        self.assertEqual(
            readout["counts"][
                "best_primary_controlled_axis_mechanism_primary_control_rows"
            ],
            2,
        )
        self.assertEqual(
            readout["counts"][
                "smallest_primary_controlled_rescue_smoke_tranche_rows"
            ],
            3,
        )
        self.assertEqual(
            readout["counts"][
                "smallest_smoke_tranche_existing_source_free_covered_rows"
            ],
            0,
        )
        self.assertEqual(
            readout["counts"][
                "smallest_smoke_tranche_existing_source_free_missing_rows"
            ],
            3,
        )
        marginal_rows = readout["missing_evidence_rows"][
            "best_primary_controlled_axis_marginal_rows"
        ]
        self.assertEqual([row["entry_id"] for row in marginal_rows], ["o2"])
        self.assertEqual(
            marginal_rows[0]["added_axis_selected_rule"]["direction"], "low"
        )
        self.assertEqual(
            marginal_rows[0]["added_axis_selected_rule"]["threshold"], 0.0
        )
        self.assertEqual(
            marginal_rows[0]["primary_control"]["retained_rows"], 2
        )
        control_rows = readout["missing_evidence_rows"][
            "best_primary_controlled_axis_mechanism_primary_control_rows_requiring_source_free_materialization"
        ]
        self.assertEqual([row["entry_id"] for row in control_rows], ["p1", "p2"])
        smoke_rows = readout["missing_evidence_rows"][
            "smallest_primary_controlled_rescue_smoke_tranche_rows"
        ]
        self.assertEqual([row["entry_id"] for row in smoke_rows], ["o2", "p1", "p2"])
        coverage = readout["measured_readout"][
            "smallest_smoke_tranche_existing_source_free_coverage"
        ]
        self.assertTrue(coverage["available"])
        self.assertEqual(coverage["covered_rows"], 0)
        self.assertTrue(
            readout["decision"][
                "genuinely_new_axis_adds_beyond_projected_subset_under_primary_control"
            ]
        )
        self.assertTrue(
            readout["guardrails"][
                "target_oos_rows_excluded_from_their_own_axis_rule_selection"
            ]
        )
        self.assertEqual(
            null_readout["counts"][
                "observed_best_axis_marginal_current_retained_oos_catches"
            ],
            1,
        )
        self.assertEqual(null_readout["counts"]["null_permutations"], 8)
        self.assertGreaterEqual(
            null_readout["counts"]["null_max_marginal_catches_p95"],
            1,
        )
        self.assertFalse(
            null_readout["decision"][
                "null_control_supports_genuinely_new_axis_signal"
            ]
        )
        self.assertTrue(
            null_readout["guardrails"][
                "null_control_randomizes_added_axis_feature_assignments_only"
            ]
        )

    def test_event_axis_signature_excluded_frontier_removes_same_signature_oos(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            mechanism_path = root / "mechanism.json"
            sidecar_path = root / "sidecar.json"
            current_overlap_path = root / "current_overlap.json"
            current_primary_path = root / "current_primary.json"
            partial_path = root / "partial.json"

            mechanism_path.write_text(
                json.dumps(
                    {
                        "scored_rows": {
                            "calibration": [
                                {"entry_id": "p1", "is_primary": True},
                                {"entry_id": "p2", "is_primary": True},
                                {"entry_id": "o1", "is_primary": False},
                                {"entry_id": "o2", "is_primary": False},
                                {"entry_id": "o3", "is_primary": False},
                                {"entry_id": "o4", "is_primary": False},
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )

            def features(
                *,
                projected: int = 0,
                bond: int = 0,
            ) -> dict[str, object]:
                return {
                    "expanded_event_residue_role__event_residue_role_proton_transfer_electrostatic_stabiliser": projected,
                    "expanded_residue_code_count__residue_code_count_his_3": 0,
                    "has_proton_transfer_event": projected > 0,
                    "proton_transfer_count": projected,
                    "has_bond_change_event": bond > 0,
                    "bond_change_event_count": bond,
                    "bond_broken_count": 0,
                    "bond_formed_count": 0,
                    "bond_order_changed_count": 0,
                    "has_electron_transfer_event": False,
                    "electron_transfer_count": 0,
                    "event_count": 0,
                    "multi_event_mechanism_flag": False,
                    "mapped_active_site_residue_count": 0,
                    "unique_mapped_active_site_residue_count": 0,
                    "high_confidence_event_count": 0,
                    "medium_confidence_event_count": 0,
                    "low_confidence_event_count": 0,
                    "unknown_confidence_event_count": 0,
                }

            sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "p1",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(bond=2),
                            },
                            {
                                "entry_id": "p2",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(bond=2),
                            },
                            {
                                "entry_id": "o1",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(
                                    projected=2,
                                    bond=2,
                                ),
                            },
                            {
                                "entry_id": "o2",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(),
                            },
                            {
                                "entry_id": "o3",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(projected=1),
                            },
                            {
                                "entry_id": "o4",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": features(),
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            current_overlap_path.write_text(
                json.dumps(
                    {
                        "fixed_operating_points": {
                            "current_surface": {
                                "channel": "combined_mean_geometry_fold",
                                "threshold": 0.5,
                            }
                        },
                        "row_readouts": {
                            "current_extended_oos_overlap_rows": [
                                {
                                    "entry_id": "o1",
                                    "current_surface_score": 0.8,
                                    "current_surface_abstains": False,
                                },
                                {
                                    "entry_id": "o2",
                                    "current_surface_score": 0.7,
                                    "current_surface_abstains": False,
                                },
                                {
                                    "entry_id": "o3",
                                    "current_surface_score": 0.4,
                                    "current_surface_abstains": True,
                                },
                                {
                                    "entry_id": "o4",
                                    "current_surface_score": 0.6,
                                    "current_surface_abstains": False,
                                },
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            current_primary_path.write_text(
                json.dumps(
                    {
                        "calibration_row_scores": [
                            {"entry_id": "p1"},
                            {"entry_id": "p2"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            partial_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "current_retained_oos_rows": 3,
                            "missing_current_primary_source_free_partial_surface_rows": 2,
                            "missing_current_retained_oos_source_free_partial_surface_rows": 3,
                            "union_current_retained_oos_overlap_rows": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_event_axis_signature_excluded_frontier_readout(
                mechanism_no_template_rerun_path=mechanism_path,
                train_cal_feature_sidecar_path=sidecar_path,
                current_extended_oos_mechanism_overlap_readout_path=(
                    current_overlap_path
                ),
                current_in_scope_threshold_contract_path=current_primary_path,
                partial_surface_current_split_portability_readout_path=partial_path,
                artifact_id="test_event_axis_signature_excluded",
            )
            sensitivity = build_lever2_event_axis_signature_exclusion_sensitivity_readout(
                mechanism_no_template_rerun_path=mechanism_path,
                train_cal_feature_sidecar_path=sidecar_path,
                current_extended_oos_mechanism_overlap_readout_path=(
                    current_overlap_path
                ),
                current_in_scope_threshold_contract_path=current_primary_path,
                partial_surface_current_split_portability_readout_path=partial_path,
                signature_axis_ids=(
                    "source_free_projected_proton_role_subset",
                    "bond_change",
                ),
                artifact_id="test_event_axis_signature_sensitivity",
            )
            with self.assertRaisesRegex(
                ValueError,
                "at least one signature axis is required",
            ):
                build_lever2_event_axis_signature_exclusion_sensitivity_readout(
                    mechanism_no_template_rerun_path=mechanism_path,
                    train_cal_feature_sidecar_path=sidecar_path,
                    current_extended_oos_mechanism_overlap_readout_path=(
                        current_overlap_path
                    ),
                    current_in_scope_threshold_contract_path=current_primary_path,
                    partial_surface_current_split_portability_readout_path=partial_path,
                    signature_axis_ids=(),
                    artifact_id="test_event_axis_empty_sensitivity",
                )

        self.assertEqual(
            readout["result_class"],
            "research_only_signature_excluded_marginal_axis_signal_source_free_gap",
        )
        self.assertEqual(
            readout["decision"]["best_signature_excluded_axis_id"],
            "source_free_projected_proton_role_subset+bond_change",
        )
        self.assertEqual(
            readout["counts"][
                "best_signature_excluded_axis_marginal_current_retained_oos_catches"
            ],
            2,
        )
        self.assertEqual(readout["counts"]["signature_excluded_target_rows"], 2)
        self.assertGreaterEqual(
            readout["counts"][
                "signature_excluded_same_signature_oos_rows_for_best_axis"
            ],
            2,
        )
        marginal_rows = readout["missing_evidence_rows"][
            "best_signature_excluded_axis_marginal_rows"
        ]
        self.assertEqual([row["entry_id"] for row in marginal_rows], ["o2", "o4"])
        o2 = [
            row
            for row in readout["row_readouts"][
                "current_extended_overlap_by_projection_plus_axis_signature_excluded"
            ]["source_free_projected_proton_role_subset+bond_change"]
            if row["entry_id"] == "o2"
        ][0]
        self.assertEqual(
            o2["signature_exclusion"]["same_signature_oos_rows_excluded"],
            ["o4"],
        )
        self.assertTrue(
            readout["decision"][
                "genuinely_new_axis_adds_beyond_projected_subset_after_signature_exclusion"
            ]
        )
        self.assertTrue(
            readout["guardrails"][
                "same_signature_calibration_oos_rows_excluded_from_target_selection"
            ]
        )
        self.assertTrue(
            readout["guardrails"][
                "same_projected_signature_calibration_oos_rows_excluded_from_target_selection"
            ]
        )
        self.assertEqual(
            sensitivity["result_class"],
            "research_only_signature_exclusion_sensitivity_signal_with_axis_caveat",
        )
        self.assertEqual(sensitivity["counts"]["signature_axes_evaluated"], 2)
        self.assertEqual(
            sensitivity["counts"]["projected_signature_bond_change_marginal_catches"],
            2,
        )
        self.assertEqual(
            sensitivity["counts"]["bond_signature_bond_change_marginal_catches"],
            0,
        )
        self.assertTrue(
            sensitivity["decision"][
                "bond_change_signal_collapses_under_own_signature_exclusion"
            ]
        )

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

    def test_electron_flow_acquisition_ceiling_tranches_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            split_path = root / "split.json"
            acquisition_rows = [
                {
                    "entry_id": "m_csa:10",
                    "priority_class": (
                        "current_retained_oos_missing_electron_flow_axis"
                    ),
                    "source_free_candidate_projection_row_available": True,
                },
                {
                    "entry_id": "m_csa:11",
                    "priority_class": (
                        "current_retained_oos_missing_electron_flow_axis"
                    ),
                    "source_free_candidate_projection_row_available": False,
                },
                {
                    "entry_id": "m_csa:12",
                    "priority_class": (
                        "current_retained_oos_missing_electron_flow_axis"
                    ),
                    "source_free_candidate_projection_row_available": False,
                },
                {
                    "entry_id": "m_csa:20",
                    "priority_class": (
                        "current_primary_retention_gate_missing_electron_flow_axis"
                    ),
                    "source_free_candidate_projection_row_available": False,
                },
                {
                    "entry_id": "m_csa:21",
                    "priority_class": (
                        "current_primary_retention_gate_missing_electron_flow_axis"
                    ),
                    "source_free_candidate_projection_row_available": False,
                },
                {
                    "entry_id": "m_csa:30",
                    "priority_class": (
                        "already_abstained_oos_missing_electron_flow_axis"
                    ),
                    "source_free_candidate_projection_row_available": False,
                },
            ]
            split_path.write_text(
                json.dumps(
                    {
                        "status": (
                            "lever2_source_free_electron_flow_"
                            "split_alignment_readout_research_only"
                        ),
                        "decision": {
                            "source_free_electron_flow_axis_has_train_cal_signal": True
                        },
                        "counts": {
                            "missing_current_retained_oos_electron_flow_rows": 3,
                            "missing_current_primary_electron_flow_rows": 2,
                        },
                        "measured_readout": {
                            "train_cal_axis_ceiling": {
                                "current_source_free_projected_subset": {
                                    "oos_abstain_recall": 0.5,
                                    "auc_oos_gt_primary": 0.75,
                                },
                                "current_plus_missing_electron_flow": {
                                    "oos_abstain_recall": 0.75,
                                    "auc_oos_gt_primary": 0.85,
                                    "primary_retain_recall": 1.0,
                                },
                                "electron_flow_oos_abstain_recall_delta_vs_current_projected": 0.25,
                            },
                            "raw_full_sidecar_current_surface_overlap_diagnostic": {
                                "available": True,
                                "counts": {
                                    "valid_current_primary_calibration_feature_overlap_rows": 0,
                                    "current_oos_calibration_feature_overlap_rows": 2,
                                    "current_retained_oos_overlap_rows": 2,
                                    "electron_positive_current_retained_oos_overlap_rows": 1,
                                },
                            },
                            "best_axis_current_extended_oos_overlap_diagnostic": {
                                "available": True,
                                "best_single_axis_new_oos_rows": [
                                    {
                                        "entry_id": "m_csa:11",
                                        "current_retained_oos_caught_by_best_axis": True,
                                    },
                                    {
                                        "entry_id": "m_csa:99",
                                        "current_retained_oos_caught_by_best_axis": True,
                                    },
                                ],
                            },
                        },
                        "acquisition_priority_rows": acquisition_rows,
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_acquisition_ceiling_readout(
                electron_flow_split_alignment_readout_path=split_path,
                tranche_sizes=(1, 2),
                artifact_id="test_electron_flow_acquisition_ceiling",
            )

        self.assertEqual(
            readout["artifact_id"], "test_electron_flow_acquisition_ceiling"
        )
        self.assertEqual(readout["result_class"], "research_only_acquisition_ceiling")
        self.assertEqual(
            readout["counts"]["smallest_smoke_source_free_rows_required"], 3
        )
        self.assertEqual(
            readout["counts"]["full_retained_current_split_source_free_rows_required"],
            5,
        )
        self.assertEqual(
            readout["counts"]["all_oos_plus_primary_source_free_rows_required"],
            6,
        )
        self.assertEqual(
            readout["counts"]["candidate_projection_overlap_retained_oos_rows"], 1
        )
        self.assertEqual(
            readout["counts"]["candidate_projection_overlap_primary_rows"], 0
        )
        self.assertEqual(
            readout["counts"]["best_axis_catches_in_acquisition_priority_rows"], 1
        )
        self.assertFalse(
            readout["decision"]["smallest_smoke_tranche_measurable_now"]
        )
        self.assertFalse(
            readout["decision"]["full_retained_current_split_measurable_now"]
        )
        self.assertIn("top 1", readout["decision"]["smallest_next_experiment"])

    def test_electron_flow_smoke_tranche_scan_requires_direct_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            acquisition_path = root / "acquisition.json"
            candidate_path = root / "candidate.json"
            partial_path = root / "partial.json"
            locator_candidate_dir = root / "locator_candidates"
            locator_candidate_dir.mkdir()
            locator_materialization_path = root / "locator_materialized.json"
            event_axis_path = root / "event_axis.json"
            acquisition_path.write_text(
                json.dumps(
                    {
                        "status": (
                            "lever2_source_free_electron_flow_acquisition_"
                            "ceiling_readout_research_only_acquisition_ceiling"
                        ),
                        "counts": {
                            "train_cal_electron_flow_oos_recall_delta": 0.25
                        },
                        "measured_readout": {
                            "train_cal_axis_signal": {
                                "electron_flow_oos_abstain_recall_delta_vs_current_projected": (
                                    0.25
                                )
                            },
                            "smallest_source_free_smoke_tranche": {
                                "tranche_id": "top_1_retained_oos_plus_all_primary",
                                "retained_oos_entry_ids": ["m_csa:10"],
                                "primary_entry_ids": ["m_csa:20", "m_csa:21"],
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )
            candidate_path.write_text(
                json.dumps(
                    {
                        "counts": {"surface_rows": 2},
                        "candidate_projection_rows": [
                            {
                                "entry_id": "m_csa:20",
                                "direct_existing_source_free_projection_fields": [
                                    "has_electron_transfer_event"
                                ],
                                "candidate_projected_event_features": {
                                    "has_electron_transfer_event": True
                                },
                                "projection_status": "partial_direct_projection",
                                "source_free_pair_features": {"x": True},
                            },
                            {
                                "entry_id": "m_csa:21",
                                "direct_existing_source_free_projection_fields": [
                                    "has_electron_transfer_event",
                                    "electron_transfer_count",
                                ],
                                "candidate_projected_event_features": {
                                    "has_electron_transfer_event": True,
                                    "electron_transfer_count": 1,
                                },
                                "projection_status": "direct_projection",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            partial_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "missing_current_primary_source_free_partial_surface_rows": 1
                        },
                        "missing_evidence_rows": {
                            "current_primary_rows_requiring_source_free_partial_surface": [
                                {"entry_id": "m_csa:20"}
                            ],
                            "current_retained_oos_rows_requiring_source_free_partial_surface": [
                                {"entry_id": "m_csa:10"}
                            ],
                        },
                    }
                ),
                encoding="utf-8",
            )
            (locator_candidate_dir / "candidate.json").write_text(
                json.dumps({"entry_id": "m_csa:20"}),
                encoding="utf-8",
            )
            locator_materialization_path.write_text(
                json.dumps(
                    {
                        "row_decisions": [
                            {
                                "entry_id": "m_csa:21",
                                "approved_locator_sidecar_written": True,
                                "decision": "materialized_to_audited_locator_dir",
                                "critical_violations": [],
                            }
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
                                "entry_id": "m_csa:10",
                                "source_free_event_axis_status": (
                                    "source_free_event_axis_linker_ready"
                                ),
                                "critical_violations": [],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_smoke_tranche_evidence_scan(
                electron_flow_acquisition_ceiling_readout_path=acquisition_path,
                source_free_projection_repair_candidate_surface_path=candidate_path,
                partial_surface_current_split_portability_readout_path=partial_path,
                review_only_locator_candidate_dir_path=locator_candidate_dir,
                source_free_locator_rewrite_materialization_gate_path=(
                    locator_materialization_path
                ),
                source_free_event_axis_linker_materialization_gate_path=(
                    event_axis_path
                ),
                artifact_id="test_electron_flow_smoke_scan",
            )

        self.assertEqual(readout["artifact_id"], "test_electron_flow_smoke_scan")
        self.assertEqual(
            readout["result_class"], "research_only_smoke_tranche_evidence_gap"
        )
        self.assertEqual(readout["counts"]["smoke_tranche_rows"], 3)
        self.assertEqual(
            readout["counts"]["candidate_projection_rows_for_smoke_tranche"], 2
        )
        self.assertEqual(
            readout["counts"]["complete_source_free_electron_flow_rows"], 1
        )
        self.assertEqual(
            readout["counts"]["review_only_locator_candidate_rows_in_smoke_tranche"],
            1,
        )
        self.assertEqual(
            readout["counts"]["materialized_source_free_locator_rows_in_smoke_tranche"],
            1,
        )
        self.assertEqual(
            readout["counts"]["source_free_event_axis_linker_rows_in_smoke_tranche"],
            1,
        )
        self.assertEqual(
            readout["counts"]["rows_missing_required_electron_flow_fields"], 2
        )
        self.assertFalse(readout["decision"]["smoke_tranche_measurable_now"])
        self.assertFalse(readout["decision"]["deployable_now"])

    def test_electron_flow_coordinate_proxy_tracks_pqq_smoke_signal(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            acquisition_path = root / "acquisition.json"
            geometry_path = root / "geometry.json"
            gap_cif_path = root / "gap.cif"
            acquisition_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "train_cal_electron_flow_oos_recall_delta": 0.142857
                        },
                        "measured_readout": {
                            "smallest_source_free_smoke_tranche": {
                                "retained_oos_entry_ids": ["m_csa:10"],
                                "primary_entry_ids": ["m_csa:20", "m_csa:30"],
                            },
                            "full_retained_oos_current_split_tranche": {
                                "retained_oos_entry_ids": ["m_csa:10", "m_csa:40"],
                                "primary_entry_ids": ["m_csa:20", "m_csa:30"],
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )
            geometry_path.write_text(
                json.dumps(
                    {
                        "entries": [
                            {
                                "entry_id": "m_csa:10",
                                "status": "ok",
                                "pdb_id": "1AAA",
                                "ligand_context": {"ligand_codes": ["PQQ"]},
                                "residues": [{"code": "His", "resid": 1}],
                                "pocket_context": {
                                    "nearby_residue_sites": [
                                        {
                                            "code": "TYR",
                                            "chain_name": "A",
                                            "resid": "2",
                                            "min_distance_to_active_site": 3.0,
                                        }
                                    ]
                                },
                            },
                            {
                                "entry_id": "m_csa:20",
                                "status": "ok",
                                "pdb_id": "2BBB",
                                "ligand_context": {"ligand_codes": ["FAD"]},
                                "residues": [{"code": "Tyr", "resid": 3}],
                                "pocket_context": {"nearby_residue_sites": []},
                            },
                            {
                                "entry_id": "m_csa:30",
                                "status": "ok",
                                "pdb_id": "3CCC",
                                "ligand_context": {"ligand_codes": []},
                                "residues": [],
                                "pocket_context": {"nearby_residue_sites": []},
                            },
                            {
                                "entry_id": "m_csa:40",
                                "status": "insufficient_resolved_residues",
                                "pdb_id": "4DDD",
                                "ligand_context": {"ligand_codes": ["PQQ"]},
                                "residues": [{"code": "Cys", "resid": 4}],
                                "pocket_context": {"nearby_residue_sites": []},
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            gap_cif_path.write_text(
                "\n".join(
                    [
                        "data_gap",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.id",
                        "_atom_site.type_symbol",
                        "_atom_site.label_atom_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "_atom_site.auth_atom_id",
                        "_atom_site.auth_comp_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.auth_seq_id",
                        "HETATM 1 C C1 NAD A 1 0 0 0 C1 NAD A 1",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_coordinate_proxy_readout(
                electron_flow_acquisition_ceiling_readout_path=acquisition_path,
                geometry_features_path=geometry_path,
                supplemental_coordinate_cif_paths={"m_csa:40": gap_cif_path},
                artifact_id="test_coordinate_proxy",
            )

        self.assertEqual(readout["artifact_id"], "test_coordinate_proxy")
        self.assertEqual(
            readout["result_class"],
            "research_only_coordinate_proxy_smoke_signal",
        )
        self.assertEqual(readout["counts"]["smoke_tranche_coordinate_rows"], 3)
        self.assertEqual(
            readout["counts"]["smoke_generic_redox_primary_positive_rows"], 1
        )
        self.assertEqual(
            readout["counts"]["smoke_pqq_primary_positive_rows"], 0
        )
        self.assertEqual(
            readout["counts"]["smoke_pqq_retained_oos_positive_rows"], 1
        )
        full = readout["measured_readout"][
            "full_retained_oos_current_split_tranche"
        ]
        self.assertEqual(
            full["counts"]["missing_coordinate_feature_entry_ids"], ["m_csa:40"]
        )
        self.assertEqual(
            full["variant_readouts"]["coordinate_quinone_pqq_redox_binary"][
                "retained_oos_positive_rows"
            ],
            1,
        )
        gap_probe = readout["measured_readout"][
            "full_retained_oos_current_split_gap_cif_probe"
        ]
        self.assertEqual(gap_probe["counts"]["sidecar_available_rows"], 1)
        self.assertEqual(
            gap_probe["counts"]["redox_ligand_inventory_positive_rows"], 1
        )
        self.assertEqual(
            gap_probe["counts"]["quinone_pqq_inventory_positive_rows"], 0
        )
        self.assertTrue(
            readout["decision"][
                "pqq_coordinate_subfield_smoke_adds_incremental_oos_abstention"
            ]
        )
        self.assertFalse(readout["decision"]["deployable_now"])

    def test_electron_flow_pqq_primitive_axis_audit_tracks_atom_contact(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            proxy_path = root / "coordinate_proxy.json"
            geometry_path = root / "geometry.json"
            pqq_cif_path = root / "pqq.cif"
            gap_cif_path = root / "gap.cif"
            proxy_rows = [
                {
                    "entry_id": "m_csa:10",
                    "tranche_role": "current_retained_oos",
                    "coordinate_evidence": {
                        "geometry_status": "ok",
                        "source_free_coordinate_features_available": True,
                        "proximal_quinone_redox_ligand_codes": ["PQQ"],
                    },
                },
                {
                    "entry_id": "m_csa:20",
                    "tranche_role": "current_primary_retention_gate",
                    "coordinate_evidence": {
                        "geometry_status": "ok",
                        "source_free_coordinate_features_available": True,
                        "proximal_quinone_redox_ligand_codes": [],
                    },
                },
                {
                    "entry_id": "m_csa:30",
                    "tranche_role": "current_primary_retention_gate",
                    "coordinate_evidence": {
                        "geometry_status": "missing_geometry_row",
                        "source_free_coordinate_features_available": False,
                        "proximal_quinone_redox_ligand_codes": [],
                    },
                },
            ]
            proxy_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "train_cal_electron_flow_oos_recall_delta": 0.142857,
                            "smallest_source_free_smoke_tranche": {
                                "rows": proxy_rows,
                            },
                            "full_retained_oos_current_split_tranche": {
                                "rows": proxy_rows,
                            },
                            "full_retained_oos_current_split_gap_cif_probe": {
                                "rows": [
                                    {
                                        "entry_id": "m_csa:30",
                                        "tranche_role": (
                                            "current_primary_retention_gate"
                                        ),
                                        "sidecar_available": True,
                                        "sidecar_status": "ok",
                                        "coordinate_path": str(gap_cif_path),
                                        "structure_quinone_redox_ligand_codes": [],
                                    }
                                ]
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            geometry_path.write_text(
                json.dumps(
                    {
                        "entries": [
                            {
                                "entry_id": "m_csa:10",
                                "status": "ok",
                                "pdb_id": "1AAA",
                                "ligand_context": {"ligand_codes": ["PQQ"]},
                                "residues": [
                                    {
                                        "chain_name": "A",
                                        "resid": 10,
                                        "code": "Arg",
                                    }
                                ],
                            },
                            {
                                "entry_id": "m_csa:20",
                                "status": "ok",
                                "pdb_id": "2BBB",
                                "ligand_context": {"ligand_codes": ["FAD"]},
                                "residues": [
                                    {
                                        "chain_name": "A",
                                        "resid": 20,
                                        "code": "His",
                                    }
                                ],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            pqq_cif_path.write_text(
                "\n".join(
                    [
                        "data_pqq",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.id",
                        "_atom_site.type_symbol",
                        "_atom_site.label_atom_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "_atom_site.auth_atom_id",
                        "_atom_site.auth_comp_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.auth_seq_id",
                        "ATOM 1 N NH1 ARG A 10 0 0 0 NH1 ARG A 10",
                        "HETATM 2 O O5 PQQ F 1004 0 0 2.8 O5 PQQ A 1004",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            gap_cif_path.write_text("data_gap\n", encoding="utf-8")

            readout = (
                build_lever2_source_free_electron_flow_pqq_primitive_axis_audit(
                    coordinate_proxy_readout_path=proxy_path,
                    geometry_features_path=geometry_path,
                    coordinate_cif_paths={"m_csa:10": pqq_cif_path},
                    artifact_id="test_pqq_primitive_axis",
                )
            )

        self.assertEqual(readout["artifact_id"], "test_pqq_primitive_axis")
        self.assertEqual(
            readout["result_class"],
            "research_only_pqq_redox_center_candidate_axis_signal",
        )
        self.assertEqual(
            readout["counts"]["smoke_complete_pqq_redox_center_rows"], 3
        )
        self.assertEqual(
            readout["counts"][
                "smoke_pqq_redox_center_retained_oos_positive_rows"
            ],
            1,
        )
        self.assertEqual(
            readout["counts"]["smoke_pqq_redox_center_primary_positive_rows"],
            0,
        )
        self.assertEqual(
            readout["counts"]["full_complete_pqq_redox_center_rows"], 3
        )
        self.assertTrue(
            readout["decision"][
                "source_free_pqq_redox_center_fields_complete_on_full_current_split"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "pqq_redox_center_axis_adds_full_current_split_oos_abstention"
            ]
        )
        self.assertFalse(readout["decision"]["deployable_now"])
        positive_row = readout["measured_readout"][
            "smallest_source_free_smoke_tranche"
        ]["rows"][0]
        self.assertEqual(positive_row["field_status"], "ok")
        self.assertEqual(
            positive_row["min_pqq_redox_center_distance_to_active_site_atom"],
            2.8,
        )

    def test_electron_flow_pqq_current_split_sidecar_readout_maps_direct_fields(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pqq_audit_path = root / "pqq_audit.json"
            projection_path = root / "projection.json"
            rows = [
                {
                    "entry_id": "m_csa:10",
                    "tranche_role": "current_retained_oos",
                    "source_free_pqq_redox_center_field_complete": True,
                    "has_source_free_pqq_redox_center_contact": True,
                    "source_free_pqq_redox_center_contact_count": 1,
                    "field_status": "ok",
                    "geometry_status": "ok",
                    "coordinate_path": "artifacts/pdb_1AAA.cif",
                    "pqq_redox_center_contact_cutoff_angstrom": 4.0,
                    "pqq_redox_center_atom_names": ["C4", "C5", "O4", "O5"],
                },
                {
                    "entry_id": "m_csa:11",
                    "tranche_role": "current_retained_oos",
                    "source_free_pqq_redox_center_field_complete": True,
                    "has_source_free_pqq_redox_center_contact": False,
                    "source_free_pqq_redox_center_contact_count": 0,
                    "field_status": "complete_negative_no_proximal_pqq_coordinate_evidence",
                    "geometry_status": "ok",
                    "pqq_redox_center_contact_cutoff_angstrom": 4.0,
                    "pqq_redox_center_atom_names": ["C4", "C5", "O4", "O5"],
                },
                {
                    "entry_id": "m_csa:20",
                    "tranche_role": "current_primary_retention_gate",
                    "source_free_pqq_redox_center_field_complete": True,
                    "has_source_free_pqq_redox_center_contact": False,
                    "source_free_pqq_redox_center_contact_count": 0,
                    "field_status": "complete_negative_no_proximal_pqq_coordinate_evidence",
                    "geometry_status": "ok",
                    "pqq_redox_center_contact_cutoff_angstrom": 4.0,
                    "pqq_redox_center_atom_names": ["C4", "C5", "O4", "O5"],
                },
                {
                    "entry_id": "m_csa:30",
                    "tranche_role": "current_primary_retention_gate",
                    "source_free_pqq_redox_center_field_complete": True,
                    "has_source_free_pqq_redox_center_contact": False,
                    "source_free_pqq_redox_center_contact_count": 0,
                    "field_status": "complete_negative_from_gap_cif_inventory",
                    "geometry_status": "missing_geometry_row",
                    "pqq_redox_center_contact_cutoff_angstrom": 4.0,
                    "pqq_redox_center_atom_names": ["C4", "C5", "O4", "O5"],
                },
            ]
            pqq_audit_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "smallest_source_free_smoke_tranche": {
                                "rows": [rows[0], rows[2], rows[3]],
                            },
                            "full_retained_oos_current_split_tranche": {
                                "rows": rows,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            projection_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "axis_repair_ceiling_rows": [
                                {
                                    "variant": "current_source_free_projected_subset",
                                    "oos_abstain_recall": 0.5,
                                },
                                {
                                    "variant": "current_plus_missing_electron_flow",
                                    "oos_abstain_recall": 0.75,
                                    "primary_retain_recall": 1.0,
                                },
                            ],
                            "split_alignment_context": {
                                "current_geometry_fold_calibration_oos_rows": 4,
                                "current_geometry_fold_calibration_primary_rows": 2,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )

            readout = (
                build_lever2_source_free_electron_flow_pqq_current_split_sidecar_readout(
                    pqq_primitive_axis_audit_path=pqq_audit_path,
                    projection_readout_path=projection_path,
                    artifact_id="test_pqq_current_split_sidecar",
                )
            )

        self.assertEqual(readout["artifact_id"], "test_pqq_current_split_sidecar")
        self.assertEqual(
            readout["result_class"],
            "research_only_direct_pqq_sidecar_operating_point_signal",
        )
        self.assertEqual(
            readout["counts"]["full_current_split_complete_direct_electron_flow_rows"],
            4,
        )
        self.assertEqual(
            readout["counts"]["full_current_split_primary_positive_rows"], 0
        )
        self.assertEqual(
            readout["counts"]["full_current_split_retained_oos_positive_rows"],
            1,
        )
        self.assertEqual(
            readout["counts"][
                "incremental_oos_abstain_recall_vs_current_geometry_fold"
            ],
            0.25,
        )
        self.assertEqual(
            readout["counts"]["projection_electron_flow_oos_recall_delta"],
            0.25,
        )
        sidecar_row = readout["measured_readout"][
            "full_retained_oos_current_split_tranche"
        ]["sidecar_rows"][0]
        self.assertTrue(
            sidecar_row["row_specific_event_features"][
                "has_electron_transfer_event"
            ]
        )
        self.assertEqual(
            sidecar_row["row_specific_event_features"][
                "electron_transfer_count"
            ],
            1,
        )
        self.assertTrue(
            readout["decision"][
                "direct_source_free_pqq_fields_add_operating_point_value_beyond_current_geometry_fold"
            ]
        )
        self.assertFalse(readout["decision"]["deployable_now"])

    def test_electron_flow_pqq_donor_acceptor_contact_readout_maps_strict_contact(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pqq_audit_path = root / "pqq_audit.json"
            projection_path = root / "projection.json"
            rows = [
                {
                    "entry_id": "m_csa:10",
                    "tranche_role": "current_retained_oos",
                    "source_free_pqq_redox_center_field_complete": True,
                    "has_source_free_pqq_redox_center_contact": True,
                    "source_free_pqq_redox_center_contact_count": 1,
                    "field_status": "ok",
                    "geometry_status": "ok",
                    "coordinate_path": "artifacts/pdb_1AAA.cif",
                    "pqq_redox_center_instances": [
                        {
                            "ligand_code": "PQQ",
                            "ligand_chain": "A",
                            "ligand_resid": "1004",
                            "has_redox_center_contact": True,
                            "closest_contact": {
                                "pqq_atom": "O5",
                                "active_residue_code": "ARG",
                                "active_resid": "228",
                                "active_atom": "NH1",
                                "distance_angstrom": 2.8,
                            },
                        }
                    ],
                },
                {
                    "entry_id": "m_csa:11",
                    "tranche_role": "current_retained_oos",
                    "source_free_pqq_redox_center_field_complete": True,
                    "has_source_free_pqq_redox_center_contact": True,
                    "source_free_pqq_redox_center_contact_count": 1,
                    "field_status": "ok",
                    "geometry_status": "ok",
                    "coordinate_path": "artifacts/pdb_1BBB.cif",
                    "pqq_redox_center_instances": [
                        {
                            "ligand_code": "PQQ",
                            "ligand_chain": "A",
                            "ligand_resid": "1004",
                            "has_redox_center_contact": True,
                            "closest_contact": {
                                "pqq_atom": "C5",
                                "active_residue_code": "ALA",
                                "active_resid": "40",
                                "active_atom": "CB",
                                "distance_angstrom": 3.0,
                            },
                        }
                    ],
                },
                {
                    "entry_id": "m_csa:20",
                    "tranche_role": "current_primary_retention_gate",
                    "source_free_pqq_redox_center_field_complete": True,
                    "has_source_free_pqq_redox_center_contact": True,
                    "source_free_pqq_redox_center_contact_count": 1,
                    "field_status": "ok",
                    "geometry_status": "ok",
                    "coordinate_path": "artifacts/pdb_1CCC.cif",
                    "pqq_redox_center_instances": [
                        {
                            "ligand_code": "PQQ",
                            "ligand_chain": "A",
                            "ligand_resid": "1004",
                            "has_redox_center_contact": True,
                            "closest_contact": {
                                "pqq_atom": "C4",
                                "active_residue_code": "VAL",
                                "active_resid": "60",
                                "active_atom": "CG1",
                                "distance_angstrom": 3.1,
                            },
                        }
                    ],
                },
                {
                    "entry_id": "m_csa:30",
                    "tranche_role": "current_primary_retention_gate",
                    "source_free_pqq_redox_center_field_complete": True,
                    "has_source_free_pqq_redox_center_contact": False,
                    "source_free_pqq_redox_center_contact_count": 0,
                    "field_status": "complete_negative_no_proximal_pqq_coordinate_evidence",
                    "geometry_status": "ok",
                },
            ]
            pqq_audit_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "smallest_source_free_smoke_tranche": {
                                "rows": [rows[0], rows[2], rows[3]],
                            },
                            "full_retained_oos_current_split_tranche": {
                                "rows": rows,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            projection_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "axis_repair_ceiling_rows": [
                                {
                                    "variant": "current_source_free_projected_subset",
                                    "oos_abstain_recall": 0.5,
                                },
                                {
                                    "variant": "current_plus_missing_electron_flow",
                                    "oos_abstain_recall": 0.75,
                                    "primary_retain_recall": 1.0,
                                },
                            ],
                            "split_alignment_context": {
                                "current_geometry_fold_calibration_oos_rows": 4,
                                "current_geometry_fold_calibration_primary_rows": 2,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )

            readout = (
                build_lever2_source_free_electron_flow_pqq_donor_acceptor_contact_readout(
                    pqq_primitive_axis_audit_path=pqq_audit_path,
                    projection_readout_path=projection_path,
                    artifact_id="test_pqq_donor_acceptor",
                )
            )

        self.assertEqual(readout["artifact_id"], "test_pqq_donor_acceptor")
        self.assertEqual(
            readout["result_class"],
            "research_only_pqq_donor_acceptor_contact_operating_point_signal",
        )
        self.assertEqual(
            readout["counts"]["full_current_split_complete_donor_acceptor_rows"],
            4,
        )
        self.assertEqual(
            readout["counts"]["full_current_split_primary_positive_rows"], 0
        )
        self.assertEqual(
            readout["counts"]["full_current_split_retained_oos_positive_rows"],
            1,
        )
        self.assertEqual(
            readout["counts"][
                "incremental_oos_abstain_recall_vs_current_geometry_fold"
            ],
            0.25,
        )
        self.assertEqual(
            readout["counts"][
                "pqq_redox_center_positive_rows_not_donor_acceptor"
            ],
            2,
        )
        comparison = readout["measured_readout"][
            "full_retained_oos_current_split_tranche"
        ]["comparison_to_pqq_redox_center_contact"]
        self.assertEqual(
            comparison["pqq_donor_acceptor_positive_entry_ids"],
            ["m_csa:10"],
        )
        self.assertFalse(comparison["same_positive_ids_as_pqq_redox_center_contact"])
        sidecar_row = readout["measured_readout"][
            "full_retained_oos_current_split_tranche"
        ]["sidecar_rows"][0]
        self.assertTrue(
            sidecar_row["row_specific_event_features"][
                "has_electron_transfer_event"
            ]
        )
        self.assertEqual(
            sidecar_row["pqq_donor_acceptor_evidence"]["contacts"][0][
                "active_atom_prefix"
            ],
            "N",
        )
        self.assertTrue(
            readout["decision"][
                "direct_source_free_donor_acceptor_fields_add_operating_point_value_beyond_current_geometry_fold"
            ]
        )
        self.assertFalse(readout["decision"]["deployable_now"])

    def test_electron_flow_donor_acceptor_contact_readout_controls_broad_redox(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            proxy_path = root / "coordinate_proxy.json"
            geometry_path = root / "geometry.json"
            projection_path = root / "projection.json"
            train_cal_path = root / "train_cal_sidecar.json"
            pqq_cif_path = root / "pqq.cif"
            fad_cif_path = root / "fad.cif"
            gap_cif_path = root / "gap.cif"
            proxy_rows = [
                {
                    "entry_id": "m_csa:10",
                    "tranche_role": "current_retained_oos",
                    "coordinate_evidence": {
                        "geometry_status": "ok",
                        "source_free_coordinate_features_available": True,
                        "proximal_quinone_redox_ligand_codes": ["PQQ"],
                        "proximal_redox_ligand_codes": ["PQQ"],
                    },
                },
                {
                    "entry_id": "m_csa:11",
                    "tranche_role": "current_retained_oos",
                    "coordinate_evidence": {
                        "geometry_status": "ok",
                        "source_free_coordinate_features_available": True,
                        "proximal_quinone_redox_ligand_codes": [],
                        "proximal_redox_ligand_codes": [],
                    },
                },
                {
                    "entry_id": "m_csa:20",
                    "tranche_role": "current_primary_retention_gate",
                    "coordinate_evidence": {
                        "geometry_status": "ok",
                        "source_free_coordinate_features_available": True,
                        "proximal_quinone_redox_ligand_codes": [],
                        "proximal_redox_ligand_codes": ["FAD"],
                    },
                },
                {
                    "entry_id": "m_csa:30",
                    "tranche_role": "current_primary_retention_gate",
                    "coordinate_evidence": {
                        "geometry_status": "missing_geometry_row",
                        "source_free_coordinate_features_available": False,
                        "proximal_quinone_redox_ligand_codes": [],
                        "proximal_redox_ligand_codes": [],
                    },
                },
            ]
            proxy_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "smallest_source_free_smoke_tranche": {
                                "rows": [proxy_rows[0], proxy_rows[2], proxy_rows[3]],
                            },
                            "full_retained_oos_current_split_tranche": {
                                "rows": proxy_rows,
                            },
                            "full_retained_oos_current_split_gap_cif_probe": {
                                "rows": [
                                    {
                                        "entry_id": "m_csa:30",
                                        "tranche_role": (
                                            "current_primary_retention_gate"
                                        ),
                                        "sidecar_available": True,
                                        "sidecar_status": "ok",
                                        "coordinate_path": str(gap_cif_path),
                                        "structure_quinone_redox_ligand_codes": [],
                                        "structure_redox_ligand_codes": [],
                                    }
                                ]
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            geometry_path.write_text(
                json.dumps(
                    {
                        "entries": [
                            {
                                "entry_id": "m_csa:10",
                                "status": "ok",
                                "pdb_id": "1AAA",
                                "ligand_context": {"ligand_codes": ["PQQ"]},
                                "residues": [
                                    {
                                        "chain_name": "A",
                                        "resid": 10,
                                        "code": "Arg",
                                    }
                                ],
                            },
                            {
                                "entry_id": "m_csa:20",
                                "status": "ok",
                                "pdb_id": "2BBB",
                                "ligand_context": {"ligand_codes": ["FAD"]},
                                "residues": [
                                    {
                                        "chain_name": "A",
                                        "resid": 20,
                                        "code": "His",
                                    }
                                ],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            projection_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "axis_repair_ceiling_rows": [
                                {
                                    "variant": "current_source_free_projected_subset",
                                    "oos_abstain_recall": 0.5,
                                },
                                {
                                    "variant": "current_plus_missing_electron_flow",
                                    "oos_abstain_recall": 0.75,
                                },
                            ],
                            "split_alignment_context": {
                                "current_geometry_fold_calibration_oos_rows": 4,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            train_cal_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "m_csa:10",
                                "assigned_embedding_split": "train",
                            },
                            {
                                "entry_id": "m_csa:20",
                                "assigned_embedding_split": "calibration",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            cif_header = [
                "loop_",
                "_atom_site.group_PDB",
                "_atom_site.id",
                "_atom_site.type_symbol",
                "_atom_site.label_atom_id",
                "_atom_site.label_comp_id",
                "_atom_site.label_asym_id",
                "_atom_site.label_seq_id",
                "_atom_site.Cartn_x",
                "_atom_site.Cartn_y",
                "_atom_site.Cartn_z",
                "_atom_site.auth_atom_id",
                "_atom_site.auth_comp_id",
                "_atom_site.auth_asym_id",
                "_atom_site.auth_seq_id",
            ]
            pqq_cif_path.write_text(
                "\n".join(
                    [
                        "data_pqq",
                        *cif_header,
                        "ATOM 1 N NH1 ARG A 10 0 0 0 NH1 ARG A 10",
                        "HETATM 2 O O5 PQQ F 1004 0 0 2.8 O5 PQQ A 1004",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            fad_cif_path.write_text(
                "\n".join(
                    [
                        "data_fad",
                        *cif_header,
                        "ATOM 1 N ND1 HIS A 20 0 0 0 ND1 HIS A 20",
                        "HETATM 2 N N5 FAD F 500 0 0 2.6 N5 FAD A 500",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            gap_cif_path.write_text("data_gap\n", encoding="utf-8")

            readout = (
                build_lever2_source_free_electron_flow_donor_acceptor_contact_readout(
                    coordinate_proxy_readout_path=proxy_path,
                    geometry_features_path=geometry_path,
                    projection_readout_path=projection_path,
                    train_cal_feature_sidecar_path=train_cal_path,
                    coordinate_cif_paths={
                        "m_csa:10": pqq_cif_path,
                        "m_csa:20": fad_cif_path,
                    },
                    artifact_id="test_donor_acceptor",
                )
            )

        self.assertEqual(readout["artifact_id"], "test_donor_acceptor")
        self.assertEqual(
            readout["result_class"],
            "research_only_direct_pqq_donor_acceptor_operating_point_signal",
        )
        self.assertEqual(
            readout["counts"]["full_complete_pqq_donor_acceptor_rows"],
            4,
        )
        self.assertEqual(
            readout["counts"]["full_pqq_donor_acceptor_primary_positive_rows"],
            0,
        )
        self.assertEqual(
            readout["counts"][
                "full_pqq_donor_acceptor_retained_oos_positive_rows"
            ],
            1,
        )
        self.assertEqual(
            readout["counts"]["broad_control_full_primary_positive_rows"],
            1,
        )
        self.assertEqual(
            readout["counts"]["broad_control_full_positive_family_summary"][
                "family_positive_row_counts"
            ],
            {"flavin": 1, "pqq": 1},
        )
        self.assertFalse(
            readout["decision"][
                "broad_redox_center_control_preserves_primary_retention"
            ]
        )
        full = readout["measured_readout"][
            "full_retained_oos_current_split_tranche"
        ]
        self.assertEqual(
            full["fixed_gate_readout"]["retained_oos_positive_entry_ids"],
            ["m_csa:10"],
        )
        broad_gate = full["broad_redox_center_donor_acceptor_control"][
            "fixed_gate_readout"
        ]
        self.assertEqual(broad_gate["primary_positive_entry_ids"], ["m_csa:20"])
        scout = readout["measured_readout"][
            "projection_model_donor_acceptor_row_scout"
        ]
        self.assertEqual(scout["projection_rows"], 2)
        self.assertEqual(scout["pqq_positive_entry_ids"], ["m_csa:10"])
        self.assertEqual(
            scout["broad_positive_entry_ids"], ["m_csa:10", "m_csa:20"]
        )
        self.assertEqual(
            scout["broad_positive_family_summary"][
                "family_positive_row_counts"
            ],
            {"flavin": 1, "pqq": 1},
        )
        cutoff_scout = readout["measured_readout"][
            "pqq_donor_acceptor_cutoff_sensitivity_scout"
        ]
        self.assertEqual(cutoff_scout["finite_distance_rows"], 1)
        self.assertEqual(
            cutoff_scout["closest_retained_oos_distance_angstrom"], 2.8
        )
        self.assertFalse(
            cutoff_scout[
                "any_primary_safe_cutoff_adds_rows_beyond_fixed_3p2"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "pqq_donor_acceptor_fields_add_operating_point_value_beyond_current_geometry_fold"
            ]
        )
        self.assertFalse(readout["decision"]["deployable_now"])

    def test_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_readout(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            donor_acceptor_path = root / "donor_acceptor.json"

            def sidecar_row(
                entry_id: str,
                role: str,
                positive: bool,
            ) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "assigned_embedding_split": "calibration",
                    "current_split_role": role,
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": {
                        "has_electron_transfer_event": positive,
                        "electron_transfer_count": 1 if positive else 0,
                        "has_source_free_pqq_donor_acceptor_contact": positive,
                        "source_free_pqq_donor_acceptor_contact_count": (
                            1 if positive else 0
                        ),
                    },
                    "pqq_donor_acceptor_evidence": {
                        "field_status": "ok",
                        "geometry_status": "ok",
                        "coordinate_path": "artifacts/pdb_1AAA.cif",
                        "pqq_donor_acceptor_atom_names": ["O4", "O5"],
                        "donor_acceptor_active_atom_elements": ["N", "O", "S"],
                        "pqq_donor_acceptor_contact_cutoff_angstrom": 3.2,
                        "min_pqq_donor_acceptor_distance_to_active_site_atom": (
                            2.8 if positive else None
                        ),
                        "missing_source_free_evidence": [],
                    },
                }

            donor_acceptor_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "current_geometry_fold_oos_rows": 4,
                            "full_current_split_rows": 4,
                            "full_complete_pqq_donor_acceptor_rows": 4,
                            "full_pqq_donor_acceptor_primary_positive_rows": 0,
                            "full_pqq_donor_acceptor_retained_oos_positive_rows": 1,
                        },
                        "measured_readout": {
                            "projection_context": {
                                "split_alignment_context": {
                                    "current_geometry_fold_calibration_oos_rows": 4
                                }
                            },
                            "smallest_source_free_smoke_tranche": {
                                "pqq_donor_acceptor_sidecar_rows": [
                                    sidecar_row(
                                        "m_csa:10",
                                        "current_retained_oos",
                                        True,
                                    ),
                                    sidecar_row(
                                        "m_csa:20",
                                        "current_primary_retention_gate",
                                        False,
                                    ),
                                ]
                            },
                            "full_retained_oos_current_split_tranche": {
                                "pqq_donor_acceptor_sidecar_rows": [
                                    sidecar_row(
                                        "m_csa:10",
                                        "current_retained_oos",
                                        True,
                                    ),
                                    sidecar_row(
                                        "m_csa:11",
                                        "current_retained_oos",
                                        False,
                                    ),
                                    sidecar_row(
                                        "m_csa:20",
                                        "current_primary_retention_gate",
                                        False,
                                    ),
                                    sidecar_row(
                                        "m_csa:21",
                                        "current_primary_retention_gate",
                                        False,
                                    ),
                                ]
                            },
                            "projection_model_donor_acceptor_row_scout": {
                                "pqq_positive_rows": 0,
                                "broad_positive_rows": 2,
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_readout(
                donor_acceptor_readout_path=donor_acceptor_path,
                artifact_id="test_pqq_donor_acceptor_current_split_feature_sidecar",
            )

        self.assertEqual(
            readout["artifact_id"],
            "test_pqq_donor_acceptor_current_split_feature_sidecar",
        )
        self.assertEqual(
            readout["result_class"],
            "research_only_materialized_feature_sidecar_operating_point_signal",
        )
        self.assertEqual(readout["counts"]["materialized_feature_rows"], 4)
        self.assertEqual(
            readout["counts"]["source_free_electron_flow_feature_complete_rows"],
            4,
        )
        self.assertEqual(readout["counts"]["current_primary_positive_rows"], 0)
        self.assertEqual(
            readout["counts"]["current_retained_oos_positive_rows"], 1
        )
        self.assertEqual(
            readout["counts"][
                "incremental_oos_abstain_recall_vs_current_geometry_fold"
            ],
            0.25,
        )
        self.assertEqual(readout["counts"]["forbidden_row_feature_key_hits"], 0)
        self.assertEqual(
            readout["counts"]["non_pqq_family_exclusion_candidates_checked"], 7
        )
        self.assertEqual(
            readout["counts"][
                "primary_safe_non_pqq_family_exclusion_candidates_with_retained_oos_signal"
            ],
            0,
        )
        self.assertEqual(
            readout["counts"][
                "relaxed_non_pqq_distance_cutoff_scout_rows_with_primary_safe_retained_oos_signal"
            ],
            0,
        )
        feature_row = readout["feature_rows"][0]
        self.assertEqual(
            sorted(feature_row["row_specific_event_features"]),
            [
                "electron_transfer_count",
                "has_electron_transfer_event",
                "has_source_free_pqq_donor_acceptor_contact",
                "source_free_pqq_donor_acceptor_contact_count",
            ],
        )
        self.assertTrue(
            readout["decision"][
                "standalone_current_split_feature_sidecar_materialized"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "pqq_donor_acceptor_feature_rows_add_operating_point_value_beyond_current_geometry_fold"
            ]
        )
        self.assertFalse(readout["decision"]["deployable_now"])
        self.assertFalse(
            readout["decision"][
                "non_pqq_family_exclusion_scout_adds_primary_safe_retained_oos_signal"
            ]
        )
        self.assertFalse(
            readout["decision"][
                "relaxed_non_pqq_distance_scout_finds_primary_safe_signal"
            ]
        )

    def test_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_readout(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            donor_acceptor_path = root / "donor_acceptor.json"

            def broad_row(
                entry_id: str,
                role: str,
                ligand_code: str,
                distance: float,
            ) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "tranche_role": role,
                    "source_free_broad_redox_center_donor_acceptor_field_complete": True,
                    "field_status": "ok",
                    "geometry_status": "ok",
                    "coordinate_path": "artifacts/pdb_1AAA.cif",
                    "broad_redox_center_contact_cutoff_angstrom": 3.2,
                    "donor_acceptor_active_atom_elements": ["N", "O", "S"],
                    "missing_source_free_evidence": [],
                    "broad_redox_center_donor_acceptor_instances": [
                        {
                            "ligand_code": ligand_code,
                            "ligand_chain": "A",
                            "ligand_resid": "100",
                            "has_donor_acceptor_contact": distance <= 3.2,
                            "min_distance_to_active_site_donor_acceptor_atom": (
                                distance
                            ),
                            "closest_contact": {
                                "distance_angstrom": distance,
                                "ligand_atom": "N1N",
                                "active_atom": "OG",
                            },
                        }
                    ],
                }

            full_rows = [
                broad_row("m_csa:10", "current_retained_oos", "NAD", 5.5),
                broad_row("m_csa:11", "current_retained_oos", "SF4", 9.0),
                broad_row(
                    "m_csa:20",
                    "current_primary_retention_gate",
                    "FAD",
                    2.8,
                ),
                broad_row(
                    "m_csa:21",
                    "current_primary_retention_gate",
                    "HEM",
                    2.2,
                ),
            ]
            donor_acceptor_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "current_geometry_fold_oos_rows": 4,
                        },
                        "measured_readout": {
                            "projection_context": {
                                "split_alignment_context": {
                                    "current_geometry_fold_calibration_oos_rows": 4
                                }
                            },
                            "smallest_source_free_smoke_tranche": {
                                "broad_redox_center_donor_acceptor_control": {
                                    "rows": full_rows
                                }
                            },
                            "full_retained_oos_current_split_tranche": {
                                "broad_redox_center_donor_acceptor_control": {
                                    "rows": full_rows
                                }
                            },
                            "projection_model_relaxed_non_pqq_distance_row_scout": {
                                "available": True,
                                "projection_row_materialization_complete_now": True,
                                "projection_rows": 2,
                                "complete_rows": 2,
                                "incomplete_rows": 0,
                                "positive_rows": 1,
                                "positive_entry_ids": ["m_csa:59"],
                                "train_positive_rows": 0,
                                "calibration_positive_rows": 1,
                                "train_cal_supports_fixed_contract": True,
                                "interpretation": "synthetic projection support",
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_readout(
                donor_acceptor_readout_path=donor_acceptor_path,
                artifact_id="test_relaxed_non_pqq_donor_acceptor_sidecar",
            )

        self.assertEqual(
            readout["artifact_id"], "test_relaxed_non_pqq_donor_acceptor_sidecar"
        )
        self.assertEqual(
            readout["result_class"],
            "research_only_fixed_relaxed_non_pqq_distance_operating_point_signal",
        )
        self.assertEqual(readout["counts"]["materialized_feature_rows"], 4)
        self.assertEqual(
            readout["counts"]["source_free_electron_flow_feature_complete_rows"],
            4,
        )
        self.assertEqual(readout["counts"]["current_primary_positive_rows"], 0)
        self.assertEqual(
            readout["counts"]["current_retained_oos_positive_rows"], 1
        )
        self.assertEqual(
            readout["counts"][
                "incremental_oos_abstain_recall_vs_current_geometry_fold"
            ],
            0.25,
        )
        self.assertEqual(
            readout["counts"]["projection_row_scout_positive_entry_ids"],
            ["m_csa:59"],
        )
        feature_row = readout["feature_rows"][0]
        self.assertEqual(
            sorted(feature_row["row_specific_event_features"]),
            [
                "electron_transfer_count",
                "has_electron_transfer_event",
                "has_source_free_relaxed_non_pqq_donor_acceptor_contact",
                "source_free_relaxed_non_pqq_donor_acceptor_contact_count",
            ],
        )
        self.assertTrue(
            readout["decision"][
                "fixed_relaxed_non_pqq_distance_adds_operating_point_value_beyond_current_geometry_fold"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "projection_rows_have_positive_train_cal_signal_for_fixed_contract"
            ]
        )
        self.assertFalse(readout["decision"]["deployable_now"])

    def test_electron_flow_combined_direct_feature_sidecar_readout(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pqq_path = root / "pqq.json"
            relaxed_path = root / "relaxed.json"

            def pqq_row(entry_id: str, role: str, positive: bool) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "current_split_role": role,
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": {
                        "has_electron_transfer_event": positive,
                        "electron_transfer_count": 1 if positive else 0,
                        "has_source_free_pqq_donor_acceptor_contact": positive,
                        "source_free_pqq_donor_acceptor_contact_count": (
                            1 if positive else 0
                        ),
                    },
                    "pqq_donor_acceptor_evidence": {
                        "coordinate_path": "artifacts/pdb_1AAA.cif"
                    },
                }

            def relaxed_row(
                entry_id: str,
                role: str,
                positive: bool,
            ) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "current_split_role": role,
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": {
                        "has_electron_transfer_event": positive,
                        "electron_transfer_count": 1 if positive else 0,
                        "has_source_free_relaxed_non_pqq_donor_acceptor_contact": (
                            positive
                        ),
                        "source_free_relaxed_non_pqq_donor_acceptor_contact_count": (
                            1 if positive else 0
                        ),
                    },
                    "relaxed_non_pqq_donor_acceptor_evidence": {
                        "coordinate_path": "artifacts/pdb_1BBB.cif",
                        "positive_contact_examples": (
                            [
                                {
                                    "reported_family": "nad",
                                    "ligand_code": "NAD",
                                    "min_distance_to_active_site_donor_acceptor_atom": (
                                        5.5
                                    ),
                                }
                            ]
                            if positive
                            else []
                        ),
                    },
                }

            pqq_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "current_geometry_fold_oos_rows": 4,
                            "current_retained_oos_positive_rows": 1,
                            "projection_row_scout_pqq_positive_rows": 0,
                        },
                        "decision": {
                            "pqq_projection_rows_have_positive_train_cal_signal": False
                        },
                        "measured_readout": {
                            "smallest_source_free_smoke_tranche": {
                                "feature_rows": [
                                    pqq_row(
                                        "m_csa:10",
                                        "current_retained_oos",
                                        True,
                                    ),
                                    pqq_row(
                                        "m_csa:20",
                                        "current_primary_retention_gate",
                                        False,
                                    ),
                                    pqq_row(
                                        "m_csa:21",
                                        "current_primary_retention_gate",
                                        False,
                                    ),
                                ]
                            }
                        },
                        "feature_rows": [
                            pqq_row("m_csa:10", "current_retained_oos", True),
                            pqq_row("m_csa:11", "current_retained_oos", False),
                            pqq_row(
                                "m_csa:20",
                                "current_primary_retention_gate",
                                False,
                            ),
                            pqq_row(
                                "m_csa:21",
                                "current_primary_retention_gate",
                                False,
                            ),
                        ],
                    }
                ),
                encoding="utf-8",
            )
            relaxed_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "current_geometry_fold_oos_rows": 4,
                            "current_retained_oos_positive_rows": 1,
                            "projection_row_scout_positive_rows": 1,
                            "projection_row_scout_positive_entry_ids": [
                                "m_csa:59"
                            ],
                        },
                        "decision": {
                            "projection_rows_have_positive_train_cal_signal_for_fixed_contract": True
                        },
                        "measured_readout": {
                            "smallest_source_free_smoke_tranche": {
                                "feature_rows": [
                                    relaxed_row(
                                        "m_csa:10",
                                        "current_retained_oos",
                                        False,
                                    ),
                                    relaxed_row(
                                        "m_csa:20",
                                        "current_primary_retention_gate",
                                        False,
                                    ),
                                    relaxed_row(
                                        "m_csa:21",
                                        "current_primary_retention_gate",
                                        False,
                                    ),
                                ]
                            }
                        },
                        "feature_rows": [
                            relaxed_row(
                                "m_csa:10",
                                "current_retained_oos",
                                False,
                            ),
                            relaxed_row(
                                "m_csa:11",
                                "current_retained_oos",
                                True,
                            ),
                            relaxed_row(
                                "m_csa:20",
                                "current_primary_retention_gate",
                                False,
                            ),
                            relaxed_row(
                                "m_csa:21",
                                "current_primary_retention_gate",
                                False,
                            ),
                        ],
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_combined_direct_feature_sidecar_readout(
                pqq_donor_acceptor_feature_sidecar_readout_path=pqq_path,
                relaxed_non_pqq_feature_sidecar_readout_path=relaxed_path,
                artifact_id="test_combined_direct_electron_flow_sidecar",
            )

        self.assertEqual(
            readout["artifact_id"], "test_combined_direct_electron_flow_sidecar"
        )
        self.assertEqual(
            readout["result_class"],
            "research_only_combined_direct_electron_flow_operating_point_signal",
        )
        self.assertEqual(readout["counts"]["materialized_feature_rows"], 4)
        self.assertEqual(
            readout["counts"]["source_free_electron_flow_feature_complete_rows"],
            4,
        )
        self.assertEqual(readout["counts"]["current_primary_positive_rows"], 0)
        self.assertEqual(
            readout["counts"]["current_retained_oos_positive_rows"], 2
        )
        self.assertEqual(readout["counts"]["smoke_feature_rows"], 3)
        self.assertEqual(readout["counts"]["smoke_complete_feature_rows"], 3)
        self.assertEqual(readout["counts"]["smoke_primary_positive_rows"], 0)
        self.assertEqual(
            readout["counts"]["smoke_retained_oos_positive_rows"], 1
        )
        self.assertEqual(
            readout["counts"][
                "incremental_oos_abstain_recall_vs_current_geometry_fold"
            ],
            0.5,
        )
        feature_row = readout["feature_rows"][0]
        self.assertEqual(
            sorted(feature_row["row_specific_event_features"]),
            [
                "electron_transfer_count",
                "has_electron_transfer_event",
                "has_source_free_pqq_donor_acceptor_contact",
                "has_source_free_relaxed_non_pqq_donor_acceptor_contact",
                "source_free_pqq_donor_acceptor_contact_count",
                "source_free_relaxed_non_pqq_donor_acceptor_contact_count",
            ],
        )
        self.assertEqual(
            readout["measured_readout"][
                "full_retained_oos_current_split_tranche"
            ]["fixed_gate_readout"]["retained_oos_positive_entry_ids"],
            ["m_csa:10", "m_csa:11"],
        )
        self.assertEqual(
            readout["measured_readout"][
                "smallest_source_free_smoke_tranche"
            ]["fixed_gate_readout"]["retained_oos_positive_entry_ids"],
            ["m_csa:10"],
        )
        self.assertEqual(
            readout["measured_readout"][
                "projection_backed_pqq_plus_nad_family_subunion"
            ]["fixed_gate_readout"]["retained_oos_positive_entry_ids"],
            ["m_csa:10", "m_csa:11"],
        )
        self.assertTrue(
            readout["decision"][
                "combined_direct_electron_flow_adds_operating_point_value_beyond_current_geometry_fold"
            ]
        )
        self.assertTrue(
            readout["decision"]["smoke_tranche_preserves_primary_retention"]
        )
        self.assertTrue(
            readout["decision"]["smoke_tranche_adds_retained_oos_abstention"]
        )
        self.assertTrue(
            readout["decision"][
                "projection_rows_have_positive_train_cal_signal_for_combined_contract"
            ]
        )
        self.assertFalse(readout["decision"]["deployable_now"])

    def test_electron_flow_projection_backed_pqq_nad_feature_sidecar_readout(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            combined_path = root / "combined.json"

            def supported_row(
                entry_id: str,
                role: str,
                *,
                pqq: bool = False,
                nad: bool = False,
            ) -> dict[str, object]:
                count = int(pqq) + int(nad)
                return {
                    "entry_id": entry_id,
                    "current_split_role": role,
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": {
                        "has_electron_transfer_event": bool(count),
                        "electron_transfer_count": count,
                        "has_source_free_pqq_donor_acceptor_contact": pqq,
                        "source_free_pqq_donor_acceptor_contact_count": int(pqq),
                        "has_source_free_nad_family_donor_acceptor_distance": nad,
                        "source_free_nad_family_donor_acceptor_distance_count": int(
                            nad
                        ),
                    },
                    "projection_backed_evidence": {},
                }

            fixed_gate = {
                "adds_incremental_oos_abstention": True,
                "complete_rows": 4,
                "incomplete_rows": 0,
                "incremental_oos_abstain_recall_vs_current_geometry_fold": 0.5,
                "operating_point_measurable_now": True,
                "preserves_primary_retention": True,
                "primary_positive_entry_ids": [],
                "primary_positive_rows": 0,
                "primary_retain_recall_if_abstain_positive": 1.0,
                "primary_rows": 2,
                "retained_oos_abstain_recall_if_abstain_positive": 1.0,
                "retained_oos_positive_entry_ids": ["m_csa:10", "m_csa:11"],
                "retained_oos_positive_rows": 2,
                "retained_oos_rows": 2,
                "rows": 4,
                "union_or_gate_oos_abstain_recall": 0.75,
            }
            combined_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "projection_backed_pqq_plus_nad_family_subunion": {
                                "feature_rows": [
                                    supported_row(
                                        "m_csa:10",
                                        "current_retained_oos",
                                        pqq=True,
                                    ),
                                    supported_row(
                                        "m_csa:11",
                                        "current_retained_oos",
                                        nad=True,
                                    ),
                                    supported_row(
                                        "m_csa:20",
                                        "current_primary_retention_gate",
                                    ),
                                    supported_row(
                                        "m_csa:21",
                                        "current_primary_retention_gate",
                                    ),
                                ],
                                "fixed_gate_readout": fixed_gate,
                                "unsupported_relaxed_non_pqq_positive_rows": [
                                    {
                                        "entry_id": "m_csa:119",
                                        "unsupported_families": [
                                            "iron_sulfur_or_iron"
                                        ],
                                    }
                                ],
                            },
                            "projection_support_summary": {
                                "combined_projection_positive_entry_ids": [
                                    "m_csa:59"
                                ],
                                "pqq_projection_positive_rows": 0,
                                "relaxed_non_pqq_projection_positive_rows": 1,
                                "train_cal_supports_combined_contract": True,
                            },
                        },
                        "source_artifacts": {},
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_projection_backed_pqq_nad_feature_sidecar_readout(
                combined_direct_feature_sidecar_readout_path=combined_path,
                artifact_id="test_projection_backed_pqq_nad",
            )

        self.assertEqual(readout["artifact_id"], "test_projection_backed_pqq_nad")
        self.assertEqual(
            readout["result_class"],
            "research_only_projection_backed_pqq_nad_operating_point_signal",
        )
        self.assertEqual(readout["counts"]["materialized_feature_rows"], 4)
        self.assertEqual(
            readout["counts"]["source_free_electron_flow_feature_complete_rows"],
            4,
        )
        self.assertEqual(readout["counts"]["current_primary_positive_rows"], 0)
        self.assertEqual(
            readout["counts"]["current_retained_oos_positive_rows"], 2
        )
        self.assertEqual(
            readout["counts"]["combined_projection_positive_entry_ids"],
            ["m_csa:59"],
        )
        self.assertEqual(
            readout["counts"]["unsupported_relaxed_non_pqq_positive_rows"], 1
        )
        self.assertEqual(
            readout["measured_readout"]["positive_feature_rows"][0]["entry_id"],
            "m_csa:10",
        )
        self.assertTrue(
            readout["decision"][
                "projection_backed_pqq_nad_adds_operating_point_value_beyond_current_geometry_fold"
            ]
        )
        self.assertTrue(
            readout["decision"]["projection_rows_support_pqq_nad_contract"]
        )
        self.assertTrue(
            readout["decision"]["unsupported_iron_sulfur_positive_excluded"]
        )
        self.assertFalse(readout["decision"]["deployable_now"])

    def test_electron_flow_iron_sulfur_projection_support_readout_names_gap(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            relaxed_path = root / "relaxed.json"
            locus_path = root / "iron_sulfur.json"
            current_gate = {
                "adds_incremental_oos_abstention": True,
                "complete_rows": 3,
                "current_geometry_fold_oos_rows": 4,
                "incomplete_rows": 0,
                "incremental_oos_abstain_recall_vs_current_geometry_fold": 0.25,
                "operating_point_measurable_now": True,
                "preserves_primary_retention": True,
                "primary_positive_entry_ids": [],
                "primary_positive_rows": 0,
                "primary_retain_recall_if_abstain_positive": 1.0,
                "primary_rows": 2,
                "retained_oos_abstain_recall_if_abstain_positive": 1.0,
                "retained_oos_positive_entry_ids": ["m_csa:119"],
                "retained_oos_positive_rows": 1,
                "retained_oos_rows": 1,
                "rows": 3,
                "union_or_gate_oos_abstain_recall": 0.5,
            }
            projection_scout = {
                "available": True,
                "calibration_positive_rows": 0,
                "complete_rows": 2,
                "interpretation": (
                    "The fixed relaxed non-PQQ distance contract has no "
                    "positive train/cal projection rows."
                ),
                "positive_entry_ids": [],
                "positive_rows": 0,
                "projection_rows": 2,
                "train_cal_supports_fixed_contract": False,
                "train_positive_rows": 0,
            }
            relaxed_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {"entry_id": "m_csa:119"},
                            {"entry_id": "m_csa:200"},
                            {"entry_id": "m_csa:201"},
                        ],
                        "measured_readout": {
                            "family_split_fixed_8A_readouts": {
                                "candidate_readouts": [
                                    {
                                        "candidate_id": (
                                            "iron_sulfur_or_iron_only"
                                        ),
                                        "fixed_gate_readout": current_gate,
                                        "projection_scout": projection_scout,
                                    }
                                ]
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            def locus_row(
                entry_id: str,
                *,
                distance: float,
                split: str = "in_distribution",
                predictive: bool = False,
            ) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "nearest_active_site_distance_angstrom": distance,
                    "predictive_use_allowed": predictive,
                    "proximal_iron_sulfur_ligands": [
                        {
                            "code": "SF4",
                            "instance_count": 1,
                            "min_distance_to_active_site": distance,
                        }
                    ],
                    "sidecar_status": "proximal_iron_sulfur_context_available",
                    "source_feature_status": "ok",
                    "split_assignment": split,
                    "supporting_ligand_codes": ["SF4"],
                }

            locus_path.write_text(
                json.dumps(
                    {
                        "rows": [
                            locus_row("m_csa:119", distance=5.3),
                            locus_row("m_csa:443", distance=3.458),
                            locus_row("m_csa:127", distance=3.486),
                            locus_row("m_csa:281", distance=3.664),
                            locus_row(
                                "m_csa:323",
                                distance=3.617,
                                split="heldout",
                            ),
                        ]
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_iron_sulfur_projection_support_readout(
                relaxed_non_pqq_feature_sidecar_readout_path=relaxed_path,
                iron_sulfur_locus_sidecar_path=locus_path,
                artifact_id="test_iron_sulfur_projection_support",
            )

        self.assertEqual(
            readout["artifact_id"], "test_iron_sulfur_projection_support"
        )
        self.assertEqual(
            readout["result_class"],
            "research_only_iron_sulfur_current_split_signal_review_only_support_gap",
        )
        self.assertEqual(readout["counts"]["current_primary_positive_rows"], 0)
        self.assertEqual(
            readout["counts"]["current_retained_oos_positive_rows"], 1
        )
        self.assertEqual(readout["counts"]["projection_positive_rows"], 0)
        self.assertEqual(
            readout["counts"][
                "review_only_nonheldout_proximal_rows_outside_current_split"
            ],
            3,
        )
        self.assertEqual(
            readout["measured_readout"][
                "review_only_iron_sulfur_locus_support_scan"
            ]["smallest_noncurrent_projection_tranche_entry_ids"],
            ["m_csa:443", "m_csa:127", "m_csa:281"],
        )
        self.assertTrue(
            readout["decision"][
                "iron_sulfur_or_iron_adds_operating_point_value_beyond_current_geometry_fold"
            ]
        )
        self.assertFalse(
            readout["decision"][
                "existing_projection_rows_support_iron_sulfur_contract"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "review_only_source_free_iron_sulfur_evidence_exists_outside_current_split"
            ]
        )
        self.assertFalse(
            readout["decision"][
                "review_only_source_free_iron_sulfur_evidence_consumable_now"
            ]
        )
        self.assertFalse(readout["decision"]["train_cal_supported_now"])
        self.assertFalse(readout["decision"]["deployable_now"])

    def test_electron_flow_iron_sulfur_approval_qualified_union_readout(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pqq_nad_path = root / "pqq_nad.json"
            relaxed_path = root / "relaxed.json"
            iron_support_path = root / "iron_support.json"

            def pqq_nad_row(
                entry_id: str,
                role: str,
                *,
                pqq_count: int = 0,
                nad_count: int = 0,
            ) -> dict[str, object]:
                total = pqq_count + nad_count
                return {
                    "entry_id": entry_id,
                    "assigned_embedding_split": "calibration",
                    "current_split_role": role,
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": {
                        "has_electron_transfer_event": total > 0,
                        "electron_transfer_count": total,
                        "has_source_free_pqq_donor_acceptor_contact": (
                            pqq_count > 0
                        ),
                        "source_free_pqq_donor_acceptor_contact_count": (
                            pqq_count
                        ),
                        "has_source_free_nad_family_donor_acceptor_distance": (
                            nad_count > 0
                        ),
                        "source_free_nad_family_donor_acceptor_distance_count": (
                            nad_count
                        ),
                    },
                }

            pqq_nad_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            pqq_nad_row("p1", "current_primary_retention_gate"),
                            pqq_nad_row("p2", "current_primary_retention_gate"),
                            pqq_nad_row(
                                "m_csa:104",
                                "current_retained_oos",
                                pqq_count=1,
                            ),
                            pqq_nad_row("m_csa:119", "current_retained_oos"),
                            pqq_nad_row(
                                "m_csa:464",
                                "current_retained_oos",
                                nad_count=1,
                            ),
                        ]
                    }
                ),
                encoding="utf-8",
            )

            def relaxed_row(
                entry_id: str,
                *,
                iron_count: int = 0,
            ) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": {
                        "has_electron_transfer_event": iron_count > 0,
                        "electron_transfer_count": iron_count,
                        "has_source_free_relaxed_non_pqq_donor_acceptor_contact": (
                            iron_count > 0
                        ),
                        "source_free_relaxed_non_pqq_donor_acceptor_contact_count": (
                            iron_count
                        ),
                    },
                    "relaxed_non_pqq_donor_acceptor_evidence": {
                        "positive_contact_examples": [
                            {
                                "reported_family": "iron_sulfur_or_iron",
                                "min_distance_angstrom": 5.1,
                            }
                            for _ in range(iron_count)
                        ]
                    },
                }

            relaxed_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            relaxed_row("p1"),
                            relaxed_row("p2"),
                            relaxed_row("m_csa:104"),
                            relaxed_row("m_csa:119", iron_count=1),
                            relaxed_row("m_csa:464"),
                        ]
                    }
                ),
                encoding="utf-8",
            )

            iron_support_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "current_split_iron_sulfur_or_iron_family_gate": {
                                "adds_incremental_oos_abstention": True,
                                "complete_rows": 5,
                                "current_geometry_fold_oos_rows": 5,
                                "incremental_oos_abstain_recall_vs_current_geometry_fold": 0.2,
                                "operating_point_measurable_now": True,
                                "preserves_primary_retention": True,
                                "primary_positive_entry_ids": [],
                                "primary_positive_rows": 0,
                                "primary_retain_recall_if_abstain_positive": 1.0,
                                "primary_rows": 2,
                                "retained_oos_positive_entry_ids": [
                                    "m_csa:119"
                                ],
                                "retained_oos_positive_rows": 1,
                                "retained_oos_rows": 3,
                                "rows": 5,
                            },
                            "tiny_iron_sulfur_projection_materialization_attempt": {
                                "candidate_rows": 3,
                                "complete_rows": 3,
                                "positive_rows": 3,
                                "positive_entry_ids": [
                                    "m_csa:127",
                                    "m_csa:281",
                                    "m_csa:443",
                                ],
                            },
                            "expanded_iron_sulfur_projection_materialization_attempt": {
                                "candidate_rows": 3,
                                "complete_rows": 3,
                                "positive_rows": 3,
                            },
                        },
                        "decision": {"train_cal_supported_now": False},
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout(
                projection_backed_pqq_nad_feature_sidecar_readout_path=(
                    pqq_nad_path
                ),
                relaxed_non_pqq_feature_sidecar_readout_path=relaxed_path,
                iron_sulfur_projection_support_readout_path=iron_support_path,
                artifact_id="test_iron_sulfur_approval_qualified_union",
            )

        self.assertEqual(
            readout["artifact_id"], "test_iron_sulfur_approval_qualified_union"
        )
        self.assertEqual(
            readout["result_class"],
            "research_only_approval_qualified_iron_sulfur_adds_incremental_signal_pending_feature_sidecar_approval",
        )
        self.assertEqual(
            readout["counts"]["supported_now_current_retained_oos_positive_rows"],
            2,
        )
        self.assertEqual(
            readout["counts"][
                "approval_qualified_current_retained_oos_positive_rows"
            ],
            3,
        )
        self.assertEqual(
            readout["counts"][
                "approval_qualified_current_retained_oos_positive_entry_ids"
            ],
            ["m_csa:104", "m_csa:119", "m_csa:464"],
        )
        self.assertEqual(
            readout["counts"][
                "iron_sulfur_incremental_current_retained_oos_positive_rows_beyond_pqq_nad"
            ],
            1,
        )
        self.assertEqual(
            readout["counts"][
                "iron_sulfur_incremental_oos_abstain_recall_vs_current_geometry_fold_beyond_pqq_nad"
            ],
            0.2,
        )
        self.assertTrue(
            readout["decision"][
                "approval_qualified_iron_sulfur_adds_incremental_oos_abstention_beyond_pqq_nad"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "m_csa119_can_join_supported_route_after_tiny_tranche_approval"
            ]
        )
        family_ablation = readout["measured_readout"]["family_ablation_fixed_gates"]
        self.assertEqual(
            family_ablation["pqq_donor_acceptor_only"][
                "retained_oos_positive_entry_ids"
            ],
            ["m_csa:104"],
        )
        self.assertEqual(
            family_ablation["nad_family_distance_only"][
                "retained_oos_positive_entry_ids"
            ],
            ["m_csa:464"],
        )
        self.assertEqual(
            family_ablation["iron_sulfur_or_iron_distance_only"][
                "retained_oos_positive_entry_ids"
            ],
            ["m_csa:119"],
        )
        self.assertTrue(
            readout["decision"][
                "family_ablation_components_each_add_distinct_primary_safe_oos_signal"
            ]
        )
        self.assertFalse(readout["decision"]["train_cal_supported_now"])
        self.assertFalse(readout["decision"]["deployable_now"])

    def test_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_readout(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            iron_support_path = root / "iron_support.json"
            approval_path = root / "approval.json"
            locus_path = root / "locus.json"
            manifest_path = root / "manifest.json"
            feature_sidecar_path = root / "sidecar.json"
            role_graph_path = root / "role_graph.json"

            def tiny_feature_row(entry_id: str) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "assigned_embedding_split": "research_only_projection_tranche",
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": {
                        "has_electron_transfer_event": True,
                        "electron_transfer_count": 1,
                        "has_source_free_relaxed_non_pqq_donor_acceptor_contact": True,
                        "source_free_relaxed_non_pqq_donor_acceptor_contact_count": 1,
                    },
                    "relaxed_non_pqq_donor_acceptor_evidence": {
                        "positive_contact_examples": [
                            {"reported_family": "iron_sulfur_or_iron"}
                        ]
                    },
                }

            iron_support_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "review_only_iron_sulfur_locus_support_scan": {
                                "smallest_noncurrent_projection_tranche_entry_ids": [
                                    "m_csa:443",
                                    "m_csa:127",
                                    "m_csa:281",
                                ]
                            },
                            "tiny_iron_sulfur_projection_materialization_attempt": {
                                "candidate_entry_ids": [
                                    "m_csa:443",
                                    "m_csa:127",
                                    "m_csa:281",
                                ],
                                "candidate_rows": 3,
                                "complete_rows": 3,
                                "positive_rows": 3,
                                "feature_rows": [
                                    tiny_feature_row("m_csa:443"),
                                    tiny_feature_row("m_csa:127"),
                                    tiny_feature_row("m_csa:281"),
                                ],
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            approval_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "approval_qualified_current_primary_positive_rows": 0,
                            "approval_qualified_current_primary_retain_recall": 1.0,
                            "approval_qualified_current_retained_oos_positive_entry_ids": [
                                "m_csa:104",
                                "m_csa:119",
                                "m_csa:464",
                            ],
                            "approval_qualified_current_retained_oos_positive_rows": 3,
                            "iron_sulfur_incremental_current_retained_oos_positive_rows_beyond_pqq_nad": 1,
                            "iron_sulfur_incremental_oos_abstain_recall_vs_current_geometry_fold_beyond_pqq_nad": 0.013333,
                            "supported_now_current_retained_oos_positive_entry_ids": [
                                "m_csa:104",
                                "m_csa:464",
                            ],
                            "supported_now_current_retained_oos_positive_rows": 2,
                        },
                        "decision": {
                            "approval_qualified_union_adds_operating_point_value_beyond_current_geometry_fold": True,
                            "approval_qualified_union_preserves_primary_retention": True,
                        },
                    }
                ),
                encoding="utf-8",
            )

            def locus_row(entry_id: str) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "predictive_use_allowed": False,
                    "sidecar_status": "proximal_iron_sulfur_context_available",
                    "source_feature_status": "ok",
                    "split_assignment": "in_distribution",
                }

            locus_path.write_text(
                json.dumps(
                    {
                        "rows": [
                            locus_row("m_csa:443"),
                            locus_row("m_csa:127"),
                            locus_row("m_csa:281"),
                        ]
                    }
                ),
                encoding="utf-8",
            )
            manifest_path.write_text(
                json.dumps(
                    {
                        "row_records": [
                            {
                                "entry_id": "m_csa:443",
                                "minimal_train_cal_feature_bundle_ready": False,
                                "role_graph_status": (
                                    "missing_accession_compatible_sequence_positions"
                                ),
                                "split_assignment": "in_distribution",
                            },
                            {
                                "entry_id": "m_csa:127",
                                "minimal_train_cal_feature_bundle_ready": True,
                                "role_graph_status": "ok",
                                "split_assignment": "in_distribution",
                            },
                            {
                                "entry_id": "m_csa:281",
                                "minimal_train_cal_feature_bundle_ready": True,
                                "role_graph_status": "ok",
                                "split_assignment": "in_distribution",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            feature_sidecar_path.write_text(
                json.dumps({"feature_rows": []}), encoding="utf-8"
            )
            role_graph_path.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:443",
                                "accession": "P13063",
                                "accession_compatible_sequence_positions": False,
                                "residues": [
                                    {
                                        "sequence_positions": [
                                            {"uniprot_id": "P13063"},
                                            {"uniprot_id": "P13065"},
                                        ]
                                    }
                                ],
                            },
                            {
                                "entry_id": "m_csa:127",
                                "accession": "P07598",
                                "accession_compatible_sequence_positions": True,
                            },
                            {
                                "entry_id": "m_csa:281",
                                "accession": "P55931",
                                "accession_compatible_sequence_positions": True,
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_readout(
                iron_sulfur_projection_support_readout_path=iron_support_path,
                approval_qualified_union_readout_path=approval_path,
                iron_sulfur_locus_sidecar_path=locus_path,
                train_cal_input_manifest_path=manifest_path,
                train_cal_feature_sidecar_path=feature_sidecar_path,
                role_graph_sidecar_path=role_graph_path,
                artifact_id="test_tiny_tranche_readiness",
            )

        self.assertEqual(readout["artifact_id"], "test_tiny_tranche_readiness")
        self.assertEqual(
            readout["result_class"],
            "research_only_tiny_tranche_source_free_positive_partial_bundle_ready_pending_predictive_gate",
        )
        self.assertEqual(readout["counts"]["tiny_tranche_candidate_rows"], 3)
        self.assertEqual(
            readout["counts"]["tiny_tranche_source_free_positive_rows"], 3
        )
        self.assertEqual(
            readout["counts"][
                "tiny_tranche_minimal_train_cal_feature_bundle_ready_entry_ids"
            ],
            ["m_csa:127", "m_csa:281"],
        )
        self.assertEqual(
            readout["counts"][
                "tiny_tranche_blocked_by_minimal_feature_bundle_entry_ids"
            ],
            ["m_csa:443"],
        )
        self.assertEqual(
            readout["counts"][
                "tiny_tranche_accession_compatible_sequence_position_rows"
            ],
            2,
        )
        self.assertEqual(
            readout["counts"][
                "tiny_tranche_accession_incompatible_sequence_position_entry_ids"
            ],
            ["m_csa:443"],
        )
        self.assertEqual(
            readout["measured_readout"]["tiny_tranche_candidate_rows"][0][
                "role_graph_sequence_position_accession_counts"
            ],
            {"P13063": 1, "P13065": 1},
        )
        self.assertEqual(
            readout["counts"][
                "tiny_tranche_blocked_only_by_predictive_gate_and_import_entry_ids"
            ],
            ["m_csa:127", "m_csa:281"],
        )
        self.assertEqual(
            readout["counts"][
                "iron_sulfur_incremental_current_retained_oos_positive_rows_beyond_pqq_nad"
            ],
            1,
        )
        self.assertTrue(
            readout["decision"][
                "tiny_tranche_source_free_evidence_complete_and_positive"
            ]
        )
        self.assertFalse(
            readout["decision"][
                "tiny_tranche_all_rows_minimal_train_cal_feature_bundle_ready"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "bundle_ready_source_free_positive_subset_available"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "approval_qualified_union_adds_value_if_fe_s_approved"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "m_csa119_can_join_supported_route_after_bundle_ready_subset_approval"
            ]
        )
        self.assertTrue(
            readout["decision"]["approval_readiness_has_minimal_feature_bundle_gap"]
        )
        self.assertFalse(readout["decision"]["train_cal_supported_now"])
        self.assertFalse(readout["decision"]["deployable_now"])
        self.assertEqual(readout["counts"]["forbidden_row_feature_key_hits"], 0)

    def test_electron_flow_current_split_smoke_materialization_readout(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pqq_nad_path = root / "pqq_nad.json"
            combined_path = root / "combined.json"
            approval_path = root / "approval.json"

            def feature_row(
                entry_id: str,
                role: str,
                electron_count: int,
            ) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "assigned_embedding_split": "calibration",
                    "current_split_role": role,
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": {
                        "has_electron_transfer_event": electron_count > 0,
                        "electron_transfer_count": electron_count,
                        "has_source_free_pqq_donor_acceptor_contact": (
                            electron_count > 0
                        ),
                        "source_free_pqq_donor_acceptor_contact_count": (
                            electron_count
                        ),
                        "has_source_free_nad_family_donor_acceptor_distance": False,
                        "source_free_nad_family_donor_acceptor_distance_count": 0,
                    },
                }

            pqq_nad_path.write_text(
                json.dumps(
                    {
                        "feature_sidecar_contract": {
                            "feature_fields": [
                                "has_electron_transfer_event",
                                "electron_transfer_count",
                                "has_source_free_pqq_donor_acceptor_contact",
                                "source_free_pqq_donor_acceptor_contact_count",
                                "has_source_free_nad_family_donor_acceptor_distance",
                                "source_free_nad_family_donor_acceptor_distance_count",
                            ]
                        },
                        "feature_rows": [
                            feature_row(
                                "m_csa:104", "current_retained_oos", 1
                            ),
                            feature_row(
                                "m_csa:10",
                                "current_primary_retention_gate",
                                0,
                            ),
                            feature_row(
                                "m_csa:20",
                                "current_primary_retention_gate",
                                0,
                            ),
                            feature_row(
                                "m_csa:464", "current_retained_oos", 1
                            ),
                        ],
                        "counts": {"current_geometry_fold_oos_rows": 6},
                    }
                ),
                encoding="utf-8",
            )
            combined_path.write_text(
                json.dumps(
                    {
                        "status": "combined",
                        "result_class": "combined_signal",
                        "measured_readout": {
                            "smallest_source_free_smoke_tranche": {
                                "fixed_gate_readout": {"rows": 3}
                            },
                            "full_retained_oos_current_split_tranche": {
                                "fixed_gate_readout": {"rows": 4}
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )
            approval_path.write_text(
                json.dumps(
                    {
                        "status": "approval",
                        "result_class": "pending_support",
                        "counts": {
                            "approval_qualified_current_retained_oos_positive_rows": 3,
                            "iron_sulfur_incremental_current_retained_oos_positive_rows_beyond_pqq_nad": 1,
                        },
                        "measured_readout": {
                            "approval_qualified_pqq_nad_plus_iron_sulfur_gate": {
                                "retained_oos_positive_entry_ids": [
                                    "m_csa:104",
                                    "m_csa:119",
                                    "m_csa:464",
                                ]
                            }
                        },
                        "decision": {"train_cal_supported_now": False},
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_current_split_smoke_materialization_readout(
                projection_backed_pqq_nad_feature_sidecar_readout_path=pqq_nad_path,
                combined_direct_feature_sidecar_readout_path=combined_path,
                approval_qualified_union_readout_path=approval_path,
                artifact_id="test_smoke_materialization",
            )

        self.assertEqual(readout["artifact_id"], "test_smoke_materialization")
        self.assertEqual(
            readout["result_class"],
            "research_only_source_free_smoke_tranche_measured_expands_to_74row_current_split_pending_contract_approval",
        )
        self.assertEqual(readout["counts"]["smoke_tranche_rows"], 3)
        self.assertEqual(readout["counts"]["smoke_tranche_missing_rows"], 0)
        self.assertEqual(
            readout["counts"]["smoke_complete_source_free_electron_flow_rows"], 3
        )
        self.assertEqual(readout["counts"]["smoke_primary_positive_rows"], 0)
        self.assertEqual(
            readout["counts"]["smoke_retained_oos_positive_entry_ids"],
            ["m_csa:104"],
        )
        self.assertEqual(
            readout["counts"][
                "smoke_incremental_oos_abstain_recall_vs_current_geometry_fold"
            ],
            0.166667,
        )
        self.assertEqual(
            readout["counts"]["smoke_union_or_gate_oos_abstain_recall"],
            0.833333,
        )
        self.assertEqual(readout["counts"]["full_current_split_rows"], 4)
        self.assertEqual(
            readout["counts"][
                "full_current_split_complete_source_free_electron_flow_rows"
            ],
            4,
        )
        self.assertEqual(
            readout["counts"]["full_current_split_retained_oos_positive_entry_ids"],
            ["m_csa:104", "m_csa:464"],
        )
        self.assertEqual(
            readout["counts"]["full_current_split_retained_oos_complete_rows"], 2
        )
        self.assertEqual(
            readout["counts"][
                "approval_qualified_current_retained_oos_positive_entry_ids"
            ],
            ["m_csa:104", "m_csa:119", "m_csa:464"],
        )
        expansion_rows = readout["measured_readout"][
            "full_74row_current_split_expansion"
        ]["retained_oos_expansion_rows"]
        self.assertEqual(
            [row["entry_id"] for row in expansion_rows],
            ["m_csa:104", "m_csa:464"],
        )
        self.assertTrue(
            all(row["projection_backed_pqq_nad_positive"] for row in expansion_rows)
        )
        self.assertEqual(
            readout["counts"][
                "full_current_split_incremental_oos_abstain_recall_vs_current_geometry_fold"
            ],
            0.333333,
        )
        self.assertTrue(
            readout["decision"][
                "source_free_current_split_operating_point_measurable_on_smoke"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "direct_source_free_electron_flow_adds_operating_point_value_beyond_current_geometry_fold"
            ]
        )
        self.assertTrue(
            readout["decision"]["retained_oos_expansion_row_matrix_emitted"]
        )
        self.assertTrue(
            readout["decision"][
                "iron_sulfur_expansion_has_incremental_row_pending_support"
            ]
        )
        self.assertFalse(readout["decision"]["deployable_now"])
        self.assertEqual(readout["counts"]["forbidden_row_feature_key_hits"], 0)

    def test_electron_flow_iron_sulfur_support_subset_preflight_readout(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readiness_path = root / "readiness.json"
            smoke_path = root / "smoke.json"
            approval_path = root / "approval.json"
            pqq_nad_path = root / "pqq_nad.json"
            train_cal_sidecar_path = root / "train_cal_sidecar.json"

            def readiness_row(
                entry_id: str,
                *,
                bundle_ready: bool,
                missing_requirements: list[str],
            ) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "source_free_complete": True,
                    "source_free_positive": True,
                    "split_assignment": "in_distribution",
                    "in_distribution": True,
                    "minimal_train_cal_feature_bundle_ready": bundle_ready,
                    "accession_compatible_sequence_positions": bundle_ready,
                    "predictive_use_allowed_now": False,
                    "present_in_current_train_cal_feature_sidecar": False,
                    "missing_import_requirements": missing_requirements,
                }

            def feature_row(entry_id: str) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": {
                        "has_electron_transfer_event": True,
                        "electron_transfer_count": 1,
                        "has_source_free_iron_sulfur_or_iron_donor_acceptor_distance": True,
                        "source_free_iron_sulfur_or_iron_donor_acceptor_distance_count": 1,
                    },
                }

            readiness_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "tiny_tranche_minimal_train_cal_feature_bundle_ready_entry_ids": [
                                "m_csa:127",
                                "m_csa:281",
                            ],
                            "tiny_tranche_blocked_by_minimal_feature_bundle_entry_ids": [
                                "m_csa:443"
                            ],
                            "expanded_tranche_minimal_train_cal_feature_bundle_ready_entry_ids": [
                                "m_csa:127",
                                "m_csa:281",
                                "m_csa:130",
                            ],
                            "expanded_tranche_blocked_by_minimal_feature_bundle_entry_ids": [
                                "m_csa:443"
                            ],
                        },
                        "decision": {"train_cal_supported_now": False},
                        "candidate_feature_sidecar_rows": [
                            feature_row("m_csa:443"),
                            feature_row("m_csa:127"),
                            feature_row("m_csa:281"),
                        ],
                        "measured_readout": {
                            "tiny_tranche_candidate_rows": [
                                readiness_row(
                                    "m_csa:443",
                                    bundle_ready=False,
                                    missing_requirements=[
                                        "minimal_train_cal_feature_bundle_ready",
                                        "accession_compatible_sequence_positions_true",
                                        "predictive_use_allowed_true",
                                        "approved_train_cal_feature_sidecar_row",
                                    ],
                                ),
                                readiness_row(
                                    "m_csa:127",
                                    bundle_ready=True,
                                    missing_requirements=[
                                        "predictive_use_allowed_true",
                                        "approved_train_cal_feature_sidecar_row",
                                    ],
                                ),
                                readiness_row(
                                    "m_csa:281",
                                    bundle_ready=True,
                                    missing_requirements=[
                                        "predictive_use_allowed_true",
                                        "approved_train_cal_feature_sidecar_row",
                                    ],
                                ),
                            ],
                            "expanded_tranche_candidate_rows": [
                                readiness_row(
                                    "m_csa:443",
                                    bundle_ready=False,
                                    missing_requirements=[
                                        "minimal_train_cal_feature_bundle_ready",
                                        "accession_compatible_sequence_positions_true",
                                        "predictive_use_allowed_true",
                                        "approved_train_cal_feature_sidecar_row",
                                    ],
                                ),
                                readiness_row(
                                    "m_csa:127",
                                    bundle_ready=True,
                                    missing_requirements=[
                                        "predictive_use_allowed_true",
                                        "approved_train_cal_feature_sidecar_row",
                                    ],
                                ),
                                readiness_row(
                                    "m_csa:281",
                                    bundle_ready=True,
                                    missing_requirements=[
                                        "predictive_use_allowed_true",
                                        "approved_train_cal_feature_sidecar_row",
                                    ],
                                ),
                                readiness_row(
                                    "m_csa:130",
                                    bundle_ready=True,
                                    missing_requirements=[
                                        "predictive_use_allowed_true",
                                        "approved_train_cal_feature_sidecar_row",
                                    ],
                                ),
                            ],
                        },
                    }
                ),
                encoding="utf-8",
            )
            smoke_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "full_current_split_rows": 74,
                            "full_current_split_complete_source_free_electron_flow_rows": 74,
                            "full_current_split_incomplete_source_free_electron_flow_rows": 0,
                            "full_current_split_primary_rows": 34,
                            "full_current_split_retained_oos_rows": 40,
                            "full_current_split_retained_oos_positive_entry_ids": [
                                "m_csa:104",
                                "m_csa:464",
                            ],
                            "full_current_split_union_or_gate_oos_abstain_recall": 0.493333,
                        },
                        "decision": {
                            "direct_source_free_electron_flow_adds_operating_point_value_beyond_current_geometry_fold": True,
                            "full_74row_expansion_preserves_primary_retention": True,
                            "projection_backed_pqq_nad_contract_approved": False,
                        },
                    }
                ),
                encoding="utf-8",
            )
            approval_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "supported_now_current_retained_oos_positive_entry_ids": [
                                "m_csa:104",
                                "m_csa:464",
                            ],
                            "approval_qualified_current_primary_positive_rows": 0,
                            "approval_qualified_current_primary_retain_recall": 1.0,
                            "approval_qualified_current_retained_oos_positive_entry_ids": [
                                "m_csa:104",
                                "m_csa:119",
                                "m_csa:464",
                            ],
                            "iron_sulfur_incremental_current_retained_oos_positive_rows_beyond_pqq_nad": 1,
                            "iron_sulfur_incremental_oos_abstain_recall_vs_current_geometry_fold_beyond_pqq_nad": 0.013333,
                            "supported_now_union_or_gate_oos_abstain_recall": 0.493333,
                            "approval_qualified_union_or_gate_oos_abstain_recall": 0.506667,
                        },
                        "decision": {
                            "approval_qualified_union_adds_operating_point_value_beyond_current_geometry_fold": True,
                            "approval_qualified_union_preserves_primary_retention": True,
                        },
                    }
                ),
                encoding="utf-8",
            )
            pqq_nad_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "combined_projection_positive_entry_ids": [
                                "m_csa:59",
                                "m_csa:256",
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )
            train_cal_sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "m_csa:59",
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": True,
                                    "electron_transfer_count": 2,
                                },
                            },
                            {
                                "entry_id": "m_csa:256",
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": True,
                                    "electron_transfer_count": 3,
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_iron_sulfur_support_subset_preflight_readout(
                tiny_tranche_approval_readiness_readout_path=readiness_path,
                current_split_smoke_materialization_readout_path=smoke_path,
                approval_qualified_union_readout_path=approval_path,
                projection_backed_pqq_nad_feature_sidecar_readout_path=pqq_nad_path,
                train_cal_feature_sidecar_path=train_cal_sidecar_path,
                artifact_id="test_fe_s_support_subset_preflight",
            )

        self.assertEqual(readout["artifact_id"], "test_fe_s_support_subset_preflight")
        self.assertEqual(
            readout["result_class"],
            "research_only_fe_s_support_subset_preflight_positive_pending_predictive_import",
        )
        self.assertEqual(
            readout["counts"]["tiny_bundle_ready_support_subset_entry_ids"],
            ["m_csa:127", "m_csa:281"],
        )
        self.assertEqual(
            readout["counts"][
                "tiny_support_subset_blocked_only_by_predictive_gate_and_import_entry_ids"
            ],
            ["m_csa:127", "m_csa:281"],
        )
        self.assertEqual(
            readout["counts"][
                "iron_sulfur_incremental_current_retained_oos_entry_ids"
            ],
            ["m_csa:119"],
        )
        self.assertEqual(
            readout["counts"]["approval_qualified_current_primary_positive_rows"], 0
        )
        self.assertTrue(
            readout["decision"][
                "direct_source_free_electron_flow_adds_operating_point_value_after_selected_support_import"
            ]
        )
        self.assertTrue(readout["decision"]["support_contract_gap_only"])
        self.assertTrue(
            readout["decision"]["base_pqq_nad_contract_approval_still_required"]
        )
        self.assertEqual(
            readout["counts"][
                "approved_train_cal_sidecar_projection_support_entry_ids_present"
            ],
            ["m_csa:59", "m_csa:256"],
        )
        self.assertEqual(
            readout["counts"][
                "approved_train_cal_sidecar_source_free_component_fields_present"
            ],
            [],
        )
        self.assertTrue(
            readout["decision"][
                "approved_train_cal_sidecar_missing_direct_source_free_component_fields"
            ]
        )
        self.assertFalse(readout["decision"]["deployable_now"])
        self.assertEqual(
            readout["counts"][
                "selected_support_feature_forbidden_row_feature_key_hits"
            ],
            0,
        )

    def test_electron_flow_candidate_train_cal_bundle_readout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            approval_path = root / "approval.json"
            support_path = root / "support.json"
            relaxed_path = root / "relaxed.json"
            train_cal_sidecar_path = root / "train_cal_sidecar.json"
            train_cal_manifest_path = root / "train_cal_manifest.json"

            def current_row(
                entry_id: str,
                role: str,
                *,
                pqq: int = 0,
                nad: int = 0,
                fe_s: int = 0,
            ) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "assigned_embedding_split": "calibration",
                    "current_split_role": role,
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": {
                        "has_electron_transfer_event": bool(pqq or nad or fe_s),
                        "electron_transfer_count": pqq + nad + fe_s,
                        "has_source_free_pqq_donor_acceptor_contact": pqq > 0,
                        "source_free_pqq_donor_acceptor_contact_count": pqq,
                        "has_source_free_nad_family_donor_acceptor_distance": nad > 0,
                        "source_free_nad_family_donor_acceptor_distance_count": nad,
                        "has_source_free_iron_sulfur_or_iron_donor_acceptor_distance": fe_s > 0,
                        "source_free_iron_sulfur_or_iron_donor_acceptor_distance_count": fe_s,
                    },
                }

            def relaxed_projection_row(entry_id: str) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "assigned_embedding_split": "calibration",
                    "current_split_role": "projection_calibration",
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": {
                        "has_electron_transfer_event": True,
                        "electron_transfer_count": 1,
                        "has_source_free_relaxed_non_pqq_donor_acceptor_contact": True,
                        "source_free_relaxed_non_pqq_donor_acceptor_contact_count": 1,
                    },
                    "relaxed_non_pqq_donor_acceptor_evidence": {
                        "positive_contact_examples": [
                            {"reported_family": "nad"}
                        ]
                    },
                }

            def fe_s_support_row(entry_id: str) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "assigned_embedding_split": "research_only_projection_tranche",
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": {
                        "has_electron_transfer_event": True,
                        "electron_transfer_count": 1,
                        "has_source_free_iron_sulfur_or_iron_donor_acceptor_distance": True,
                        "source_free_iron_sulfur_or_iron_donor_acceptor_distance_count": 1,
                    },
                    "approval_readiness_evidence": {
                        "split_assignment": "in_distribution",
                        "minimal_train_cal_feature_bundle_ready": True,
                        "accession_compatible_sequence_positions": True,
                        "predictive_use_allowed_now": False,
                        "present_in_current_train_cal_feature_sidecar": False,
                        "missing_import_requirements": [
                            "predictive_use_allowed_true",
                            "approved_train_cal_feature_sidecar_row",
                        ],
                    },
                }

            approval_path.write_text(
                json.dumps(
                    {
                        "counts": {"current_geometry_fold_oos_rows": 5},
                        "feature_rows": [
                            current_row(
                                "p1", "current_primary_retention_gate"
                            ),
                            current_row(
                                "p2", "current_primary_retention_gate"
                            ),
                            current_row("o1", "current_retained_oos", pqq=1),
                            current_row("o2", "current_retained_oos", nad=1),
                            current_row("o3", "current_retained_oos", fe_s=1),
                        ],
                    }
                ),
                encoding="utf-8",
            )
            support_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "approved_train_cal_sidecar_projection_support_entry_ids_present": [
                                "s_nad1",
                                "s_nad2",
                            ],
                            "tiny_bundle_ready_support_subset_entry_ids": [
                                "s_fe1",
                                "s_fe2",
                            ],
                            "tiny_support_subset_blocked_only_by_predictive_gate_and_import_entry_ids": [
                                "s_fe1",
                                "s_fe2",
                            ],
                        },
                        "decision": {
                            "support_contract_gap_only": True,
                            "direct_source_free_electron_flow_adds_operating_point_value_after_selected_support_import": True,
                        },
                        "selected_support_feature_rows": [
                            fe_s_support_row("s_fe1"),
                            fe_s_support_row("s_fe2"),
                        ],
                    }
                ),
                encoding="utf-8",
            )
            relaxed_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "projection_model_relaxed_non_pqq_distance_row_scout": {
                                "positive_entry_ids": ["s_nad1", "s_nad2"],
                                "feature_rows": [
                                    relaxed_projection_row("s_nad1"),
                                    relaxed_projection_row("s_nad2"),
                                ],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            train_cal_sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "s_nad1",
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": True,
                                    "electron_transfer_count": 1,
                                },
                            },
                            {
                                "entry_id": "s_nad2",
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": True,
                                    "electron_transfer_count": 1,
                                },
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            train_cal_manifest_path.write_text(
                json.dumps(
                    {
                        "row_records": [
                            {
                                "entry_id": "s_fe1",
                                "split_assignment": "in_distribution",
                                "role_graph_status": "ok",
                            },
                            {
                                "entry_id": "s_fe2",
                                "split_assignment": "in_distribution",
                                "role_graph_status": "ok",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_candidate_train_cal_bundle_readout(
                approval_qualified_union_readout_path=approval_path,
                support_subset_preflight_readout_path=support_path,
                relaxed_non_pqq_feature_sidecar_readout_path=relaxed_path,
                train_cal_feature_sidecar_path=train_cal_sidecar_path,
                train_cal_input_manifest_path=train_cal_manifest_path,
                artifact_id="test_candidate_train_cal_bundle",
            )

        self.assertEqual(readout["artifact_id"], "test_candidate_train_cal_bundle")
        self.assertEqual(
            readout["result_class"],
            "research_only_candidate_train_cal_bundle_materialized_pending_approval_import",
        )
        self.assertEqual(readout["counts"]["candidate_current_split_rows"], 5)
        self.assertEqual(
            readout["counts"]["candidate_current_primary_positive_rows"], 0
        )
        self.assertEqual(
            readout["counts"]["candidate_current_retained_oos_positive_entry_ids"],
            ["o1", "o2", "o3"],
        )
        self.assertEqual(readout["counts"]["candidate_support_rows"], 4)
        self.assertEqual(readout["counts"]["candidate_expected_support_rows"], 4)
        self.assertEqual(
            readout["counts"]["candidate_support_missing_entry_ids"], []
        )
        self.assertEqual(
            readout["counts"]["candidate_pqq_nad_projection_support_entry_ids"],
            ["s_nad1", "s_nad2"],
        )
        self.assertEqual(
            readout["counts"]["candidate_selected_fe_s_support_entry_ids"],
            ["s_fe1", "s_fe2"],
        )
        self.assertEqual(
            readout["counts"][
                "candidate_selected_fe_s_support_missing_explicit_train_cal_split_entry_ids"
            ],
            ["s_fe1", "s_fe2"],
        )
        self.assertEqual(
            readout["counts"][
                "train_cal_manifest_selected_fe_s_support_entry_ids_present"
            ],
            ["s_fe1", "s_fe2"],
        )
        self.assertTrue(
            readout["decision"][
                "train_cal_manifest_confirms_selected_fe_s_rows_in_distribution"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "train_cal_manifest_confirms_selected_fe_s_role_graph_ok"
            ]
        )
        self.assertEqual(
            readout["counts"]["approved_sidecar_direct_component_fields_present"],
            [],
        )
        self.assertTrue(
            readout["decision"][
                "direct_source_free_electron_flow_adds_operating_point_value_beyond_current_geometry_fold_in_candidate_bundle"
            ]
        )
        self.assertTrue(
            readout["decision"]["candidate_expected_support_rows_materialized"]
        )
        self.assertTrue(readout["decision"]["support_contract_gap_only"])
        self.assertFalse(readout["decision"]["deployable_now"])
        self.assertEqual(
            readout["counts"]["candidate_forbidden_row_feature_key_hits"], 0
        )

    def test_electron_flow_candidate_train_cal_bundle_requires_expected_support_rows(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            approval_path = root / "approval.json"
            support_path = root / "support.json"
            relaxed_path = root / "relaxed.json"
            train_cal_sidecar_path = root / "train_cal_sidecar.json"
            train_cal_manifest_path = root / "train_cal_manifest.json"

            approval_path.write_text(
                json.dumps(
                    {
                        "counts": {"current_geometry_fold_oos_rows": 2},
                        "feature_rows": [
                            {
                                "entry_id": "p1",
                                "assigned_embedding_split": "calibration",
                                "current_split_role": (
                                    "current_primary_retention_gate"
                                ),
                                "source_free_electron_flow_field_complete": True,
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": False,
                                    "electron_transfer_count": 0,
                                },
                            },
                            {
                                "entry_id": "o1",
                                "assigned_embedding_split": "calibration",
                                "current_split_role": "current_retained_oos",
                                "source_free_electron_flow_field_complete": True,
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": True,
                                    "electron_transfer_count": 1,
                                    "has_source_free_iron_sulfur_or_iron_donor_acceptor_distance": True,
                                    "source_free_iron_sulfur_or_iron_donor_acceptor_distance_count": 1,
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            support_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "approved_train_cal_sidecar_projection_support_entry_ids_present": [
                                "missing_nad_support"
                            ],
                            "tiny_bundle_ready_support_subset_entry_ids": [
                                "s_fe1"
                            ],
                            "tiny_support_subset_blocked_only_by_predictive_gate_and_import_entry_ids": [
                                "s_fe1"
                            ],
                        },
                        "decision": {
                            "support_contract_gap_only": True,
                        },
                        "selected_support_feature_rows": [
                            {
                                "entry_id": "s_fe1",
                                "assigned_embedding_split": (
                                    "research_only_projection_tranche"
                                ),
                                "source_free_electron_flow_field_complete": True,
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": True,
                                    "electron_transfer_count": 1,
                                    "has_source_free_iron_sulfur_or_iron_donor_acceptor_distance": True,
                                    "source_free_iron_sulfur_or_iron_donor_acceptor_distance_count": 1,
                                },
                                "approval_readiness_evidence": {
                                    "split_assignment": "in_distribution",
                                    "missing_import_requirements": [
                                        "predictive_use_allowed_true",
                                        "approved_train_cal_feature_sidecar_row",
                                    ],
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            relaxed_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "projection_model_relaxed_non_pqq_distance_row_scout": {
                                "positive_entry_ids": [],
                                "feature_rows": [],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            train_cal_sidecar_path.write_text(
                json.dumps({"feature_rows": []}),
                encoding="utf-8",
            )
            train_cal_manifest_path.write_text(
                json.dumps(
                    {
                        "row_records": [
                            {
                                "entry_id": "s_fe1",
                                "split_assignment": "in_distribution",
                                "role_graph_status": "ok",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_candidate_train_cal_bundle_readout(
                approval_qualified_union_readout_path=approval_path,
                support_subset_preflight_readout_path=support_path,
                relaxed_non_pqq_feature_sidecar_readout_path=relaxed_path,
                train_cal_feature_sidecar_path=train_cal_sidecar_path,
                train_cal_input_manifest_path=train_cal_manifest_path,
                artifact_id="test_candidate_train_cal_bundle_missing_support",
            )

        self.assertEqual(
            readout["result_class"],
            "research_only_candidate_train_cal_bundle_incomplete",
        )
        self.assertEqual(
            readout["counts"]["candidate_support_missing_entry_ids"],
            ["missing_nad_support"],
        )
        self.assertFalse(
            readout["decision"]["candidate_expected_support_rows_materialized"]
        )
        self.assertFalse(
            readout["decision"][
                "direct_source_free_electron_flow_adds_operating_point_value_beyond_current_geometry_fold_in_candidate_bundle"
            ]
        )
        self.assertFalse(readout["decision"]["support_contract_gap_only"])

    def test_electron_flow_train_cal_sidecar_candidate_readout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            candidate_path = root / "candidate.json"
            train_cal_sidecar_path = root / "train_cal_sidecar.json"

            def features(
                *,
                pqq: int = 0,
                nad: int = 0,
                fe_s: int = 0,
            ) -> dict[str, object]:
                return {
                    "has_electron_transfer_event": bool(pqq or nad or fe_s),
                    "electron_transfer_count": pqq + nad + fe_s,
                    "has_source_free_pqq_donor_acceptor_contact": pqq > 0,
                    "source_free_pqq_donor_acceptor_contact_count": pqq,
                    "has_source_free_nad_family_donor_acceptor_distance": nad > 0,
                    "source_free_nad_family_donor_acceptor_distance_count": nad,
                    "has_source_free_iron_sulfur_or_iron_donor_acceptor_distance": fe_s > 0,
                    "source_free_iron_sulfur_or_iron_donor_acceptor_distance_count": fe_s,
                }

            def row(
                entry_id: str,
                role: str,
                bundle_role: str,
                *,
                split: str = "calibration",
                candidate_split: str | None = None,
                pqq: int = 0,
                nad: int = 0,
                fe_s: int = 0,
            ) -> dict[str, object]:
                result = {
                    "entry_id": entry_id,
                    "assigned_embedding_split": split,
                    "current_split_role": role,
                    "candidate_bundle_role": bundle_role,
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": features(
                        pqq=pqq, nad=nad, fe_s=fe_s
                    ),
                }
                if candidate_split is not None:
                    result["candidate_split_assignment"] = candidate_split
                return result

            candidate_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "candidate_bundle_rows": 7,
                            "selected_fe_s_support_blocked_only_by_predictive_gate_and_import_entry_ids": [
                                "s_fe"
                            ],
                        },
                        "decision": {
                            "remaining_gap": "protected import gap",
                            "smallest_next_experiment": "approve/import",
                        },
                        "feature_rows": [
                            row(
                                "p1",
                                "current_primary_retention_gate",
                                "current_split_operating_point_row",
                            ),
                            row(
                                "p2",
                                "current_primary_retention_gate",
                                "current_split_operating_point_row",
                            ),
                            row(
                                "o1",
                                "current_retained_oos",
                                "current_split_operating_point_row",
                                pqq=1,
                            ),
                            row(
                                "o2",
                                "current_retained_oos",
                                "current_split_operating_point_row",
                                nad=1,
                            ),
                            row(
                                "o3",
                                "current_retained_oos",
                                "current_split_operating_point_row",
                                fe_s=1,
                            ),
                            row(
                                "s_nad",
                                "projection_calibration",
                                "projection_backed_pqq_nad_support_row",
                                nad=1,
                            ),
                            row(
                                "s_fe",
                                "candidate_fe_s_support_projection",
                                "selected_fe_s_support_row",
                                split="research_only_projection_tranche",
                                candidate_split="in_distribution",
                                fe_s=1,
                            ),
                        ],
                        "measured_readout": {
                            "candidate_current_split_operating_point": {
                                "fixed_gate_readout": {
                                    "current_geometry_fold_oos_rows": 5
                                }
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            train_cal_sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "s_nad",
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": True,
                                    "electron_transfer_count": 1,
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_train_cal_sidecar_candidate_readout(
                candidate_train_cal_bundle_readout_path=candidate_path,
                train_cal_feature_sidecar_path=train_cal_sidecar_path,
                artifact_id="test_train_cal_sidecar_candidate",
            )

        self.assertEqual(
            readout["artifact_id"], "test_train_cal_sidecar_candidate"
        )
        self.assertEqual(
            readout["result_class"],
            "research_only_train_cal_sidecar_candidate_measured_pending_protected_import",
        )
        self.assertEqual(readout["counts"]["sidecar_candidate_rows"], 7)
        self.assertEqual(
            readout["counts"]["sidecar_candidate_current_split_rows"], 5
        )
        self.assertEqual(
            readout["counts"]["sidecar_candidate_complete_source_free_rows"], 7
        )
        self.assertEqual(
            readout["counts"]["sidecar_candidate_explicit_train_cal_split_rows"],
            6,
        )
        self.assertEqual(
            readout["counts"][
                "sidecar_candidate_manifest_or_explicit_train_cal_contained_rows"
            ],
            7,
        )
        self.assertEqual(
            readout["counts"][
                "sidecar_candidate_selected_fe_s_support_missing_explicit_split_entry_ids"
            ],
            ["s_fe"],
        )
        self.assertEqual(
            readout["counts"]["sidecar_candidate_current_primary_positive_rows"],
            0,
        )
        self.assertEqual(
            readout["counts"][
                "sidecar_candidate_current_retained_oos_positive_entry_ids"
            ],
            ["o1", "o2", "o3"],
        )
        self.assertEqual(
            readout["counts"][
                "sidecar_candidate_incremental_oos_abstain_recall_vs_current_geometry_fold"
            ],
            0.6,
        )
        self.assertEqual(
            readout["counts"]["approved_sidecar_direct_component_fields_present"],
            [],
        )
        self.assertEqual(
            readout["counts"]["approved_sidecar_current_split_rows_present"],
            0,
        )
        self.assertEqual(
            readout["counts"][
                "approved_sidecar_current_split_direct_component_complete_rows"
            ],
            0,
        )
        self.assertTrue(
            readout["decision"][
                "train_cal_disciplined_candidate_readout_available"
            ]
        )
        self.assertFalse(
            readout["decision"][
                "approved_sidecar_only_current_split_direct_electron_flow_measurable_now"
            ]
        )
        self.assertFalse(
            readout["decision"]["sidecar_candidate_has_all_explicit_train_cal_splits"]
        )
        self.assertFalse(readout["decision"]["deployable_now"])
        self.assertEqual(readout["counts"]["critical_violation_total"], 0)

    def test_electron_flow_approval_import_dry_run_readout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            candidate_path = root / "candidate_sidecar.json"
            train_cal_sidecar_path = root / "train_cal_sidecar.json"
            manifest_path = root / "manifest.json"

            def features(
                *,
                pqq: int = 0,
                nad: int = 0,
                fe_s: int = 0,
            ) -> dict[str, object]:
                return {
                    "has_electron_transfer_event": bool(pqq or nad or fe_s),
                    "electron_transfer_count": pqq + nad + fe_s,
                    "has_source_free_pqq_donor_acceptor_contact": pqq > 0,
                    "source_free_pqq_donor_acceptor_contact_count": pqq,
                    "has_source_free_nad_family_donor_acceptor_distance": nad > 0,
                    "source_free_nad_family_donor_acceptor_distance_count": nad,
                    "has_source_free_iron_sulfur_or_iron_donor_acceptor_distance": fe_s > 0,
                    "source_free_iron_sulfur_or_iron_donor_acceptor_distance_count": fe_s,
                }

            def row(
                entry_id: str,
                role: str,
                bundle_role: str,
                *,
                split: str = "calibration",
                candidate_split: str | None = None,
                pqq: int = 0,
                nad: int = 0,
                fe_s: int = 0,
            ) -> dict[str, object]:
                result = {
                    "entry_id": entry_id,
                    "assigned_embedding_split": split,
                    "current_split_role": role,
                    "candidate_bundle_role": bundle_role,
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": features(
                        pqq=pqq, nad=nad, fe_s=fe_s
                    ),
                }
                if candidate_split is not None:
                    result["candidate_split_assignment"] = candidate_split
                return result

            candidate_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "approved_sidecar_current_split_rows_present": 0,
                            "approved_sidecar_current_split_direct_component_complete_rows": 0,
                            "approved_sidecar_direct_component_fields_missing": [
                                "has_source_free_pqq_donor_acceptor_contact",
                                "source_free_pqq_donor_acceptor_contact_count",
                            ],
                        },
                        "decision": {
                            "remaining_gap": "protected import gap",
                            "smallest_next_experiment": "approve/import",
                        },
                        "candidate_feature_sidecar": {
                            "feature_rows": [
                                row(
                                    "p1",
                                    "current_primary_retention_gate",
                                    "current_split_operating_point_row",
                                ),
                                row(
                                    "p2",
                                    "current_primary_retention_gate",
                                    "current_split_operating_point_row",
                                ),
                                row(
                                    "o1",
                                    "current_retained_oos",
                                    "current_split_operating_point_row",
                                    pqq=1,
                                ),
                                row(
                                    "o2",
                                    "current_retained_oos",
                                    "current_split_operating_point_row",
                                    nad=1,
                                ),
                                row(
                                    "o3",
                                    "current_retained_oos",
                                    "current_split_operating_point_row",
                                    fe_s=1,
                                ),
                                row(
                                    "s_nad",
                                    "projection_calibration",
                                    "projection_backed_pqq_nad_support_row",
                                    nad=1,
                                ),
                                row(
                                    "s_fe",
                                    "candidate_fe_s_support_projection",
                                    "selected_fe_s_support_row",
                                    split="research_only_projection_tranche",
                                    candidate_split="in_distribution",
                                    fe_s=1,
                                ),
                            ]
                        },
                        "measured_readout": {
                            "fixed_operating_point": {
                                "current_geometry_fold_oos_rows": 5
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            train_cal_sidecar_path.write_text(
                json.dumps(
                    {
                        "feature_rows": [
                            {
                                "entry_id": "s_nad",
                                "assigned_embedding_split": "calibration",
                                "row_specific_event_features": {
                                    "has_electron_transfer_event": True,
                                    "electron_transfer_count": 1,
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            manifest_path.write_text(
                json.dumps(
                    {
                        "row_records": [
                            {
                                "entry_id": "s_fe",
                                "split_assignment": "in_distribution",
                                "role_graph_status": "ok",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_approval_import_dry_run_readout(
                train_cal_sidecar_candidate_readout_path=candidate_path,
                train_cal_feature_sidecar_path=train_cal_sidecar_path,
                train_cal_input_manifest_path=manifest_path,
                artifact_id="test_approval_import_dry_run",
            )

        self.assertEqual(readout["artifact_id"], "test_approval_import_dry_run")
        self.assertEqual(
            readout["result_class"],
            "research_only_approval_import_dry_run_closes_measurability_gap",
        )
        self.assertEqual(readout["counts"]["dry_run_import_rows"], 7)
        self.assertEqual(readout["counts"]["dry_run_current_split_rows"], 5)
        self.assertEqual(
            readout["counts"][
                "dry_run_current_split_direct_component_complete_rows"
            ],
            5,
        )
        self.assertEqual(
            readout["counts"]["dry_run_explicit_train_cal_split_rows"], 7
        )
        self.assertEqual(
            readout["counts"][
                "dry_run_selected_fe_s_support_proposed_split_assignments"
            ],
            {"s_fe": "calibration"},
        )
        self.assertEqual(
            readout["counts"]["dry_run_current_primary_positive_rows"], 0
        )
        self.assertEqual(
            readout["counts"]["dry_run_current_retained_oos_positive_entry_ids"],
            ["o1", "o2", "o3"],
        )
        self.assertEqual(
            readout["counts"][
                "dry_run_incremental_oos_abstain_recall_vs_current_geometry_fold"
            ],
            0.6,
        )
        self.assertEqual(
            readout["counts"][
                "approved_sidecar_current_split_direct_component_complete_rows_before_dry_run"
            ],
            0,
        )
        self.assertTrue(
            readout["decision"][
                "approval_import_dry_run_closes_approved_sidecar_current_split_direct_component_gap"
            ]
        )
        self.assertTrue(
            readout["decision"]["approval_import_dry_run_closes_explicit_split_gap"]
        )
        self.assertTrue(
            readout["decision"][
                "direct_source_free_electron_flow_adds_operating_point_value_beyond_current_geometry_fold_after_dry_run_import"
            ]
        )
        self.assertEqual(
            readout["counts"][
                "dry_run_selected_fe_s_split_policy_sensitivity_policy_ids"
            ],
            ["all_selected_fe_s_calibration", "all_selected_fe_s_train"],
        )
        self.assertEqual(
            readout["counts"][
                "dry_run_selected_fe_s_split_policies_matching_primary_gate"
            ],
            2,
        )
        self.assertTrue(
            readout["decision"][
                "selected_fe_s_support_split_policy_not_operating_point_sensitive"
            ]
        )
        self.assertEqual(
            readout["counts"]["dry_run_component_ablation_ids"],
            [
                "pqq_only",
                "nad_family_only",
                "iron_sulfur_only",
                "pqq_plus_nad_family",
                "pqq_plus_nad_family_plus_iron_sulfur",
            ],
        )
        self.assertEqual(
            readout["counts"][
                "dry_run_pqq_only_current_retained_oos_positive_entry_ids"
            ],
            ["o1"],
        )
        self.assertEqual(
            readout["counts"][
                "dry_run_nad_family_only_current_retained_oos_positive_entry_ids"
            ],
            ["o2"],
        )
        self.assertEqual(
            readout["counts"][
                "dry_run_iron_sulfur_only_current_retained_oos_positive_entry_ids"
            ],
            ["o3"],
        )
        self.assertEqual(
            readout["counts"][
                "dry_run_pqq_plus_nad_current_retained_oos_positive_entry_ids"
            ],
            ["o1", "o2"],
        )
        self.assertEqual(
            readout["counts"][
                "dry_run_iron_sulfur_incremental_current_retained_oos_positive_entry_ids_beyond_pqq_nad"
            ],
            ["o3"],
        )
        self.assertTrue(
            readout["decision"][
                "iron_sulfur_component_adds_incremental_row_beyond_pqq_nad_after_dry_run"
            ]
        )
        self.assertFalse(readout["decision"]["protected_surfaces_modified"])
        self.assertFalse(readout["decision"]["deployable_now"])
        self.assertEqual(readout["counts"]["critical_violation_total"], 0)

    def test_electron_flow_approval_import_smoke_review_readout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            dry_run_path = root / "dry_run.json"

            def features(
                *,
                pqq: int = 0,
                nad: int = 0,
                fe_s: int = 0,
            ) -> dict[str, object]:
                return {
                    "has_electron_transfer_event": bool(pqq or nad or fe_s),
                    "electron_transfer_count": pqq + nad + fe_s,
                    "has_source_free_pqq_donor_acceptor_contact": pqq > 0,
                    "source_free_pqq_donor_acceptor_contact_count": pqq,
                    "has_source_free_nad_family_donor_acceptor_distance": nad > 0,
                    "source_free_nad_family_donor_acceptor_distance_count": nad,
                    "has_source_free_iron_sulfur_or_iron_donor_acceptor_distance": fe_s > 0,
                    "source_free_iron_sulfur_or_iron_donor_acceptor_distance_count": fe_s,
                }

            def row(
                entry_id: str,
                role: str,
                *,
                existing: bool = False,
                pqq: int = 0,
                nad: int = 0,
                fe_s: int = 0,
            ) -> dict[str, object]:
                return {
                    "entry_id": entry_id,
                    "assigned_embedding_split": "calibration",
                    "candidate_bundle_role": "current_split_operating_point_row",
                    "current_split_role": role,
                    "existing_approved_sidecar_row": existing,
                    "source_free_electron_flow_field_complete": True,
                    "row_specific_event_features": features(
                        pqq=pqq, nad=nad, fe_s=fe_s
                    ),
                }

            dry_run_path.write_text(
                json.dumps(
                    {
                        "status": "dry_run_status",
                        "result_class": "dry_run_positive",
                        "dry_run_feature_sidecar": {
                            "sidecar_id": "dry_run_sidecar",
                            "axis_id": "source_free_electron_flow",
                            "feature_fields": [
                                "has_electron_transfer_event",
                                "electron_transfer_count",
                                "has_source_free_pqq_donor_acceptor_contact",
                                "source_free_pqq_donor_acceptor_contact_count",
                                "has_source_free_nad_family_donor_acceptor_distance",
                                "source_free_nad_family_donor_acceptor_distance_count",
                                "has_source_free_iron_sulfur_or_iron_donor_acceptor_distance",
                                "source_free_iron_sulfur_or_iron_donor_acceptor_distance_count",
                            ],
                            "feature_rows": [
                                row(
                                    "m_csa:1",
                                    "current_primary_retention_gate",
                                ),
                                row(
                                    "m_csa:2",
                                    "current_primary_retention_gate",
                                    existing=True,
                                ),
                                row(
                                    "m_csa:104",
                                    "current_retained_oos",
                                    pqq=1,
                                ),
                                row(
                                    "m_csa:119",
                                    "current_retained_oos",
                                    fe_s=1,
                                ),
                                row(
                                    "m_csa:464",
                                    "current_retained_oos",
                                    nad=1,
                                ),
                            ],
                        },
                        "measured_readout": {
                            "fixed_operating_point_after_dry_run": {
                                "current_geometry_fold_oos_rows": 5
                            },
                            "component_ablation_after_dry_run": [],
                        },
                        "counts": {
                            "dry_run_import_rows": 5,
                            "dry_run_current_split_rows": 5,
                            "dry_run_support_rows": 0,
                            "dry_run_rows_new_to_approved_sidecar": 4,
                            "dry_run_rows_updating_existing_approved_sidecar_rows": 1,
                            "dry_run_current_retained_oos_positive_entry_ids": [
                                "m_csa:104",
                                "m_csa:119",
                                "m_csa:464",
                            ],
                            "dry_run_incremental_oos_abstain_recall_vs_current_geometry_fold": 0.6,
                        },
                        "decision": {
                            "smallest_next_experiment": "approve/import"
                        },
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_electron_flow_approval_import_smoke_review_readout(
                approval_import_dry_run_readout_path=dry_run_path,
                artifact_id="test_smoke_review",
            )

        self.assertEqual(readout["artifact_id"], "test_smoke_review")
        self.assertEqual(
            readout["result_class"],
            (
                "research_only_smoke_review_positive_full_expansion_positive_"
                "pending_protected_import"
            ),
        )
        self.assertEqual(readout["counts"]["smoke_tranche_rows"], 3)
        self.assertEqual(readout["counts"]["smoke_current_primary_rows"], 2)
        self.assertEqual(
            readout["counts"]["smoke_complete_direct_component_rows"], 3
        )
        self.assertEqual(
            readout["counts"]["smoke_current_primary_positive_rows"], 0
        )
        self.assertEqual(
            readout["counts"]["smoke_retained_oos_positive_entry_ids"],
            ["m_csa:104"],
        )
        self.assertEqual(
            readout["counts"][
                "smoke_incremental_oos_abstain_recall_vs_current_geometry_fold"
            ],
            0.2,
        )
        self.assertEqual(readout["counts"]["full_current_split_rows"], 5)
        self.assertEqual(
            readout["counts"]["full_current_retained_oos_positive_entry_ids"],
            ["m_csa:104", "m_csa:119", "m_csa:464"],
        )
        self.assertEqual(
            readout["counts"][
                "full_incremental_oos_abstain_recall_vs_current_geometry_fold"
            ],
            0.6,
        )
        self.assertEqual(readout["counts"]["smoke_rows_new_to_approved_sidecar"], 2)
        self.assertEqual(
            readout["counts"]["smoke_rows_updating_existing_approved_sidecar_rows"],
            1,
        )
        self.assertTrue(
            readout["decision"][
                "smoke_tranche_adds_operating_point_value_beyond_current_geometry_fold"
            ]
        )
        self.assertTrue(
            readout["decision"][
                "full_74row_expansion_adds_operating_point_value_beyond_current_geometry_fold"
            ]
        )
        self.assertFalse(readout["decision"]["protected_surfaces_modified"])
        self.assertFalse(readout["decision"]["deployable_now"])
        self.assertTrue(
            readout["source_artifacts"]["approval_import_dry_run_readout"][
                "exists"
            ]
        )

    def test_source_free_mechanism_axis_acquisition_ranking_prefers_electron_flow(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            projection_path = root / "projection.json"
            candidate_path = root / "candidate.json"
            partial_path = root / "partial.json"
            baseline_fields = ["has_proton_transfer_event"]
            projection_path.write_text(
                json.dumps(
                    {
                        "measured_readout": {
                            "axis_repair_ceiling_rows": [
                                {
                                    "variant": "current_source_free_projected_subset",
                                    "feature_fields": baseline_fields,
                                    "primary_retain_recall": 1.0,
                                    "oos_abstain_recall": 0.5,
                                    "auc_oos_gt_primary": 0.7,
                                    "delta_vs_current_projected_oos_abstain_recall": 0.0,
                                },
                                {
                                    "variant": "current_plus_missing_bond_change",
                                    "feature_fields": [
                                        *baseline_fields,
                                        "has_bond_change_event",
                                        "bond_change_event_count",
                                    ],
                                    "primary_retain_recall": 1.0,
                                    "oos_abstain_recall": 0.6,
                                    "auc_oos_gt_primary": 0.75,
                                    "delta_vs_current_projected_oos_abstain_recall": 0.1,
                                },
                                {
                                    "variant": "current_plus_missing_electron_flow",
                                    "feature_fields": [
                                        *baseline_fields,
                                        "has_electron_transfer_event",
                                        "electron_transfer_count",
                                    ],
                                    "primary_retain_recall": 1.0,
                                    "oos_abstain_recall": 0.75,
                                    "auc_oos_gt_primary": 0.9,
                                    "delta_vs_current_projected_oos_abstain_recall": 0.25,
                                },
                                {
                                    "variant": "current_plus_missing_confidence_metadata",
                                    "feature_fields": [
                                        *baseline_fields,
                                        "medium_confidence_event_count",
                                    ],
                                    "primary_retain_recall": 1.0,
                                    "oos_abstain_recall": 0.8,
                                    "auc_oos_gt_primary": 0.85,
                                    "delta_vs_current_projected_oos_abstain_recall": 0.3,
                                },
                            ],
                            "split_alignment_context": {
                                "current_geometry_fold_calibration_primary_rows": 2,
                                "current_geometry_fold_calibration_oos_rows": 3,
                                "source_free_candidate_projection_overlap_primary_rows": 0,
                                "source_free_candidate_projection_overlap_oos_rows": 0,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            candidate_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "surface_rows": 5,
                            "missing_field_counts": {
                                "has_bond_change_event": 5,
                                "bond_change_event_count": 5,
                                "has_electron_transfer_event": 5,
                                "electron_transfer_count": 5,
                                "medium_confidence_event_count": 5,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            partial_path.write_text(
                json.dumps(
                    {
                        "counts": {
                            "union_current_primary_overlap_rows": 0,
                            "union_current_retained_oos_overlap_rows": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )

            readout = build_lever2_source_free_mechanism_axis_acquisition_ranking_readout(
                projection_readout_path=projection_path,
                source_free_projection_repair_candidate_surface_path=candidate_path,
                partial_surface_current_split_portability_readout_path=partial_path,
                artifact_id="test_axis_ranking",
            )

        self.assertEqual(readout["artifact_id"], "test_axis_ranking")
        self.assertEqual(
            readout["result_class"], "research_only_axis_ranked_evidence_gap"
        )
        self.assertEqual(
            readout["decision"]["best_genuine_mechanism_axis_id"],
            "electron_flow",
        )
        self.assertEqual(
            readout["counts"][
                "best_genuine_axis_delta_vs_current_projected_oos_abstain_recall"
            ],
            0.25,
        )
        self.assertEqual(
            readout["counts"]["source_free_ready_genuine_mechanism_axes_now"], 0
        )
        self.assertFalse(
            readout["decision"]["current_split_axis_readout_measurable_now"]
        )
        axis_ids = [
            row["axis_id"]
            for row in readout["measured_readout"]["genuine_mechanism_axis_rankings"]
        ]
        self.assertEqual(axis_ids, ["electron_flow", "bond_change"])


if __name__ == "__main__":
    unittest.main()
