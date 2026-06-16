from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.cli import _validate_label_factory_gate_cli_lineage, build_parser

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_targeted_expansion_factory_parser_defaults(self) -> None:
        args = build_parser().parse_args(["build-targeted-expansion-factory-batch"])

        self.assertEqual(
            args.out,
            (
                "artifacts/"
                "v3_targeted_expansion_factory_batch_current702_20260608.json"
            ),
        )
        self.assertEqual(
            args.report,
            "work/targeted_expansion_factory_batch_current702_20260608.md",
        )
        self.assertIsNone(args.created_utc)
        self.assertEqual(args.min_target_candidates, 500)
        self.assertEqual(args.max_candidates, 1000)
        self.assertEqual(args.source_path, [])

        overridden = build_parser().parse_args(
            [
                "build-targeted-expansion-factory-batch",
                "--source-path",
                "active_learning_1025_preview=/tmp/active.json",
            ]
        )
        self.assertEqual(
            overridden.source_path,
            ["active_learning_1025_preview=/tmp/active.json"],
        )

    def test_targeted_expansion_acquisition_conversion_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            ["build-targeted-expansion-acquisition-conversion-screens"]
        )

        self.assertEqual(
            args.batch,
            (
                "artifacts/"
                "v3_targeted_expansion_factory_batch_current702_20260608.json"
            ),
        )
        self.assertEqual(
            args.out,
            (
                "artifacts/"
                "v3_targeted_expansion_acquisition_conversion_screens_current702_20260608.json"
            ),
        )
        self.assertEqual(
            args.report,
            (
                "work/"
                "targeted_expansion_acquisition_conversion_screens_current702_20260608.md"
            ),
        )
        self.assertIsNone(args.created_utc)
        self.assertEqual(args.screen_path, [])

        overridden = build_parser().parse_args(
            [
                "build-targeted-expansion-acquisition-conversion-screens",
                "--screen-path",
                "sequence_cluster_proxy_1025=/tmp/sequence.json",
            ]
        )
        self.assertEqual(
            overridden.screen_path,
            ["sequence_cluster_proxy_1025=/tmp/sequence.json"],
        )

    def test_targeted_expansion_acquisition_conversion_rejects_bad_screen_override(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-targeted-expansion-acquisition-conversion-screens",
                "--screen-path",
                "not_a_screen=/tmp/missing.json",
            ]
        )

        with self.assertRaises(SystemExit) as raised:
            args.func(args)
        self.assertIn(
            "unknown targeted expansion conversion screen key",
            str(raised.exception),
        )

    def test_countable_label_unblocker_parser_defaults(self) -> None:
        args = build_parser().parse_args(["build-countable-label-unblocker-matrix"])

        self.assertEqual(
            args.merged_surface,
            (
                "artifacts/"
                "v3_scaleout_merged_acceptance_surface_current702_20260608.json"
            ),
        )
        self.assertEqual(
            args.repair_overlay,
            (
                "artifacts/"
                "v3_scaleout_locator_coordinate_repair_current702_20260608.json"
            ),
        )
        self.assertEqual(
            args.out,
            (
                "artifacts/"
                "v3_countable_label_unblocker_matrix_current702_20260608.json"
            ),
        )
        self.assertEqual(
            args.report,
            "work/countable_label_unblocker_matrix_current702_20260608.md",
        )
        self.assertEqual(
            args.import_preview,
            (
                "artifacts/"
                "v3_countable_label_unblocker_import_preview_current702_20260608.json"
            ),
        )
        self.assertIsNone(args.created_utc)

    def test_external_source_ingestion_pilot_parser_defaults(self) -> None:
        args = build_parser().parse_args(["build-external-source-ingestion-pilot"])

        self.assertEqual(
            args.current_manifest,
            "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json",
        )
        self.assertEqual(
            args.out,
            (
                "artifacts/"
                "v3_external_source_ingestion_pilot_current702_20260608.json"
            ),
        )
        self.assertEqual(
            args.report,
            "work/external_source_ingestion_pilot_current702_20260608.md",
        )
        self.assertEqual(
            args.import_preview_out,
            (
                "artifacts/"
                "v3_external_source_ingestion_import_preview_current702_20260608.json"
            ),
        )
        self.assertEqual(args.max_records_per_lane, 4)
        self.assertFalse(args.no_rhea_fallback)

    def test_external_source_admission_validation_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            ["build-external-source-admission-validation-16"]
        )

        self.assertEqual(
            args.pilot,
            (
                "artifacts/"
                "v3_external_source_ingestion_pilot_current702_20260608.json"
            ),
        )
        self.assertEqual(
            args.import_preview,
            (
                "artifacts/"
                "v3_external_source_ingestion_import_preview_current702_20260608.json"
            ),
        )
        self.assertEqual(
            args.out,
            (
                "artifacts/"
                "v3_external_source_admission_validation_16_current702_20260608.json"
            ),
        )
        self.assertEqual(
            args.report,
            (
                "work/"
                "external_source_admission_validation_16_current702_20260608.md"
            ),
        )
        self.assertEqual(
            args.ready_preview,
            (
                "artifacts/"
                "v3_external_source_admission_ready_preview_current702_20260608.json"
            ),
        )
        self.assertEqual(args.expected_preview_count, 16)
        self.assertEqual(args.artifacts_dir, "artifacts")
        self.assertIsNone(args.created_utc)

    def test_external_import_review_preflight_parser_defaults(self) -> None:
        args = build_parser().parse_args(["build-external-import-review-preflight"])

        self.assertEqual(
            args.preview,
            (
                "artifacts/"
                "v3_external_materialization_wave2_import_ready_preview_current702_20260609.json"
            ),
        )
        self.assertIsNone(args.merged_surface)
        self.assertEqual(
            args.materialization,
            (
                "artifacts/"
                "v3_external_materialization_wave2_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.repair_surface,
            (
                "artifacts/"
                "v3_external_materialization_wave2_repair_queue_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.current702_coordinate_manifest,
            "artifacts/v3_foldseek_coordinate_readiness_1000_current702_wave1_20260527.json",
        )
        self.assertEqual(
            args.out,
            (
                "artifacts/"
                "v3_external_import_review_preflight_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.ready_preview,
            (
                "artifacts/"
                "v3_external_import_review_ready_preview_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.repair_queue,
            (
                "artifacts/"
                "v3_external_import_review_repair_queue_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.report,
            "work/external_import_review_preflight_current702_20260609.md",
        )
        self.assertEqual(args.expected_preview_count, 600)
        self.assertEqual(args.expected_repair_count, 11895)
        self.assertEqual(args.expected_review_surface_count, 12495)
        self.assertIsNone(args.tree_ref)
        self.assertIsNone(args.created_utc)
        self.assertIsNone(args.artifact_date)

    def test_external_import_closure_packet_parser_defaults(self) -> None:
        args = build_parser().parse_args(["build-external-import-closure-packet"])

        self.assertEqual(
            args.preview,
            (
                "artifacts/"
                "v3_external_materialization_wave2_import_ready_preview_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.preflight_out,
            (
                "artifacts/"
                "v3_external_import_review_preflight_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.batch_packet,
            (
                "artifacts/"
                "v3_external_batch_import_approval_packet_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.defense_ledger,
            (
                "artifacts/"
                "v3_targeted_expansion_defense_ledger_current702_20260609.json"
            ),
        )
        self.assertEqual(args.expected_preview_count, 600)
        self.assertEqual(args.expected_repair_count, 11895)
        self.assertEqual(args.expected_review_surface_count, 12495)
        self.assertEqual(args.artifact_date, "20260609")
        self.assertIsNone(args.tree_ref)
        self.assertIsNone(args.created_utc)

    def test_external_source_pilot_decision_confidence_optional_context_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["audit-external-source-pilot-decision-confidence"]
        )

        self.assertIsNone(args.external_structural_cluster_index)
        self.assertIsNone(args.external_structural_tm_diverse_split_plan)
        self.assertIsNone(args.external_all_vs_all_sequence_search)

        overridden = build_parser().parse_args(
            [
                "audit-external-source-pilot-decision-confidence",
                "--external-structural-cluster-index",
                "/tmp/cluster.json",
                "--external-structural-tm-diverse-split-plan",
                "/tmp/split.json",
                "--external-all-vs-all-sequence-search",
                "/tmp/all_vs_all.json",
            ]
        )
        self.assertEqual(
            overridden.external_structural_cluster_index,
            "/tmp/cluster.json",
        )
        self.assertEqual(
            overridden.external_structural_tm_diverse_split_plan,
            "/tmp/split.json",
        )
        self.assertEqual(
            overridden.external_all_vs_all_sequence_search,
            "/tmp/all_vs_all.json",
        )

    def test_external_source_pilot_mechanism_repair_source_context_optional(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-external-source-pilot-mechanism-repair-lanes"]
        )

        self.assertIsNone(args.source_context_decisions)

        overridden = build_parser().parse_args(
            [
                "build-external-source-pilot-mechanism-repair-lanes",
                "--source-context-decisions",
                "/tmp/source_context.json",
            ]
        )
        self.assertEqual(
            overridden.source_context_decisions,
            "/tmp/source_context.json",
        )

    def test_external_bulk_ingestion_scout_parser_defaults(self) -> None:
        args = build_parser().parse_args(["build-external-bulk-ingestion-scout"])

        self.assertEqual(
            args.current_manifest,
            "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json",
        )
        self.assertEqual(
            args.external_pilot,
            (
                "artifacts/"
                "v3_external_source_ingestion_pilot_current702_20260608.json"
            ),
        )
        self.assertEqual(
            args.out,
            (
                "artifacts/"
                "v3_external_bulk_ingestion_scout_current702_20260608.json"
            ),
        )
        self.assertEqual(
            args.report,
            "work/external_bulk_ingestion_scout_current702_20260608.md",
        )
        self.assertEqual(
            args.import_preview_out,
            (
                "artifacts/"
                "v3_external_bulk_ingestion_provisional_import_preview_current702_20260608.json"
            ),
        )
        self.assertEqual(args.max_records_per_lane, 100)
        self.assertFalse(args.rhea_fallback)

    def test_external_scaleout_shard_plp_radical_cobalamin_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-external-scaleout-shard-plp-radical-cobalamin"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/"
                "v3_external_scaleout_shard_plp_radical_cobalamin_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.import_ready_out,
            (
                "artifacts/"
                "v3_external_scaleout_shard_plp_radical_cobalamin_import_ready_preview_"
                "current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.report,
            (
                "work/"
                "external_scaleout_shard_plp_radical_cobalamin_current702_20260609.md"
            ),
        )
        self.assertEqual(args.max_records_per_query, 100)
        self.assertEqual(args.max_pages_per_query, 5)
        self.assertEqual(args.max_candidates, 1800)
        self.assertIsNone(args.max_candidates_per_lane)
        self.assertEqual(args.target_candidate_floor, 1500)

    def test_external_materialization_wave2_parser_defaults(self) -> None:
        args = build_parser().parse_args(["build-external-materialization-wave2"])

        self.assertEqual(
            args.merged_surface,
            (
                "artifacts/"
                "v3_external_admission_merged_surface_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.import_ready_source,
            (
                "artifacts/"
                "v3_external_admission_import_ready_preview_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.out,
            (
                "artifacts/"
                "v3_external_materialization_wave2_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.import_ready_preview,
            (
                "artifacts/"
                "v3_external_materialization_wave2_import_ready_preview_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.repair_queue,
            (
                "artifacts/"
                "v3_external_materialization_wave2_repair_queue_current702_20260609.json"
            ),
        )
        self.assertEqual(
            args.report,
            "work/external_materialization_wave2_current702_20260609.md",
        )
        self.assertEqual(
            args.locator_dir,
            (
                "artifacts/"
                "external_materialization_wave2_source_free_locators_current702_20260609"
            ),
        )
        self.assertEqual(
            args.coordinate_dir,
            (
                "artifacts/"
                "external_materialization_wave2_coordinates_current702_20260609"
            ),
        )
        self.assertEqual(args.max_coordinate_downloads, 0)
        self.assertIsNone(args.created_utc)
        self.assertIsNone(args.disk_free_gib_at_start)

    def test_lever2_mechanism_incremental_readout_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            ["build-lever2-mechanism-feature-incremental-readout"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_lever2_mechanism_feature_incremental_readout_"
                "current702_20260604.json"
            ),
        )
        self.assertIn(
            "best_token_followup_pair_no_template_rerun",
            args.mechanism_no_template_rerun,
        )
        self.assertIn(
            "expanded_oos_calibrated",
            args.expanded_oos_calibrated_threshold_contract,
        )

    def test_source_free_train_cal_projection_readout_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-mechanism-feature-row-specific-bond-change-p0-oos-"
                    "augmented-best-token-followup-pair-source-free-train-cal-"
                    "projection-readout"
                )
            ]
        )

        self.assertIn(
            "source_free_train_cal_projection_readout_current702_20260604.json",
            args.out,
        )
        self.assertIn(
            "source_free_projection_repair_candidate_surface",
            args.source_free_projection_repair_candidate_surface,
        )
        self.assertIn("train_cal_feature_sidecar", args.train_cal_feature_sidecar)
        self.assertIn(
            "abstention_threshold_contract_current702",
            args.current_in_scope_threshold_contract,
        )
        self.assertIn(
            "expanded_oos_calibrated",
            args.expanded_oos_calibrated_threshold_contract,
        )
        self.assertIn(
            "abstention_threshold_contract_current702",
            args.current_in_scope_threshold_contract,
        )
        self.assertIn(
            "expanded_oos_calibrated",
            args.expanded_oos_calibrated_threshold_contract,
        )

    def test_lever2_electron_flow_split_alignment_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            ["build-lever2-source-free-electron-flow-split-alignment-readout"]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_split_alignment_readout",
            args.out,
        )
        self.assertIn(
            "source_free_train_cal_projection_readout", args.projection_readout
        )
        self.assertIn(
            "lever2_mechanism_feature_incremental_readout", args.incremental_readout
        )
        self.assertIn(
            "source_free_projection_repair_candidate_surface",
            args.source_free_projection_repair_candidate_surface,
        )
        self.assertIn(
            "extended_train_cal_oos_surface", args.current_extended_oos_surface
        )

    def test_lever2_electron_flow_acquisition_ceiling_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            ["build-lever2-source-free-electron-flow-acquisition-ceiling-readout"]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_acquisition_ceiling_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_split_alignment_readout",
            args.electron_flow_split_alignment_readout,
        )
        self.assertEqual(args.tranche_sizes, [1, 2, 5, 10, 20, 40])

    def test_lever2_electron_flow_smoke_tranche_scan_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            [
                "build-lever2-source-free-electron-flow-smoke-tranche-evidence-scan"
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_smoke_tranche_evidence_scan",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_acquisition_ceiling_readout",
            args.electron_flow_acquisition_ceiling_readout,
        )
        self.assertIn(
            "source_free_projection_repair_candidate_surface",
            args.source_free_projection_repair_candidate_surface,
        )
        self.assertIn(
            "source_free_partial_surface_current_split_portability",
            args.partial_surface_current_split_portability_readout,
        )
        self.assertIn(
            "source_free_active_site_locator_candidates",
            args.review_only_locator_candidate_dir,
        )
        self.assertIn(
            "source_free_locator_rewrite_materialization_gate_materialized",
            args.source_free_locator_rewrite_materialization_gate,
        )
        self.assertIn(
            "source_free_event_axis_linker_materialization_gate",
            args.source_free_event_axis_linker_materialization_gate,
        )

    def test_lever2_electron_flow_coordinate_proxy_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            [
                "build-lever2-source-free-electron-flow-coordinate-proxy-readout"
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_coordinate_proxy_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_acquisition_ceiling_readout",
            args.electron_flow_acquisition_ceiling_readout,
        )
        self.assertEqual(
            args.geometry_features,
            "artifacts/v3_geometry_features_1025.json",
        )
        self.assertIsNone(args.coordinate_gap_cif)

    def test_lever2_electron_flow_pqq_primitive_axis_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-lever2-source-free-electron-flow-pqq-primitive-axis-audit"
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_pqq_primitive_axis_audit",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_coordinate_proxy_readout",
            args.coordinate_proxy_readout,
        )
        self.assertEqual(
            args.geometry_features,
            "artifacts/v3_geometry_features_1025.json",
        )
        self.assertIsNone(args.coordinate_cif)

    def test_lever2_electron_flow_pqq_current_split_sidecar_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-lever2-source-free-electron-flow-pqq-current-split-sidecar-readout"
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_pqq_current_split_sidecar_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_pqq_primitive_axis_audit",
            args.pqq_primitive_axis_audit,
        )
        self.assertIn(
            "source_free_train_cal_projection_readout",
            args.projection_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )
        self.assertEqual(
            args.geometry_features,
            "artifacts/v3_geometry_features_1025.json",
        )

    def test_lever2_electron_flow_donor_acceptor_contact_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-lever2-source-free-electron-flow-donor-acceptor-contact-readout"
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_donor_acceptor_contact_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_coordinate_proxy_readout",
            args.coordinate_proxy_readout,
        )
        self.assertEqual(
            args.geometry_features,
            "artifacts/v3_geometry_features_1025.json",
        )
        self.assertIn(
            "source_free_train_cal_projection_readout",
            args.projection_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )
        self.assertIsNone(args.coordinate_cif)

    def test_lever2_electron_flow_pqq_donor_acceptor_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-lever2-source-free-electron-flow-pqq-donor-acceptor-contact-readout"
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_pqq_donor_acceptor_contact_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_pqq_primitive_axis_audit",
            args.pqq_primitive_axis_audit,
        )
        self.assertIn(
            "source_free_train_cal_projection_readout",
            args.projection_readout,
        )

    def test_lever2_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-pqq-donor-"
                    "acceptor-current-split-feature-sidecar-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_donor_acceptor_contact_readout",
            args.donor_acceptor_readout,
        )

    def test_lever2_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-relaxed-non-pqq-"
                    "donor-acceptor-feature-sidecar-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_donor_acceptor_contact_readout",
            args.donor_acceptor_readout,
        )
        self.assertIn("v3_geometry_features_1025", args.geometry_features)
        self.assertIn(
            "train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )

    def test_lever2_electron_flow_combined_direct_feature_sidecar_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-combined-direct-"
                    "feature-sidecar-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_combined_direct_feature_sidecar_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_readout",
            args.pqq_donor_acceptor_feature_sidecar_readout,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_readout",
            args.relaxed_non_pqq_feature_sidecar_readout,
        )

    def test_lever2_electron_flow_projection_backed_pqq_nad_feature_sidecar_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-projection-backed-"
                    "pqq-nad-feature-sidecar-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_projection_backed_pqq_nad_feature_sidecar_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_combined_direct_feature_sidecar_readout",
            args.combined_direct_feature_sidecar_readout,
        )

    def test_lever2_electron_flow_iron_sulfur_projection_support_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-iron-sulfur-"
                    "projection-support-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_iron_sulfur_projection_support_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_readout",
            args.relaxed_non_pqq_feature_sidecar_readout,
        )
        self.assertIn(
            "mechanism_feature_iron_sulfur_locus_sidecar",
            args.iron_sulfur_locus_sidecar,
        )
        self.assertIn("v3_geometry_features_1025", args.geometry_features)
        self.assertIsNone(args.coordinate_cif)

    def test_lever2_electron_flow_iron_sulfur_approval_qualified_union_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-iron-sulfur-"
                    "approval-qualified-union-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_projection_backed_pqq_nad_feature_sidecar_readout",
            args.projection_backed_pqq_nad_feature_sidecar_readout,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_readout",
            args.relaxed_non_pqq_feature_sidecar_readout,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_iron_sulfur_projection_support_readout",
            args.iron_sulfur_projection_support_readout,
        )

    def test_lever2_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-iron-sulfur-"
                    "tiny-tranche-approval-readiness-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_iron_sulfur_projection_support_readout",
            args.iron_sulfur_projection_support_readout,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout",
            args.approval_qualified_union_readout,
        )
        self.assertIn(
            "mechanism_feature_iron_sulfur_locus_sidecar",
            args.iron_sulfur_locus_sidecar,
        )
        self.assertIn(
            "mechanism_feature_embedding_train_cal_input_manifest",
            args.train_cal_input_manifest,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )
        self.assertIn(
            "mechanism_feature_active_site_role_graph_sidecar",
            args.role_graph_sidecar,
        )

    def test_lever2_electron_flow_current_split_smoke_materialization_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-current-split-"
                    "smoke-materialization-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_current_split_smoke_materialization_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_projection_backed_pqq_nad_feature_sidecar_readout",
            args.projection_backed_pqq_nad_feature_sidecar_readout,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_combined_direct_feature_sidecar_readout",
            args.combined_direct_feature_sidecar_readout,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout",
            args.approval_qualified_union_readout,
        )

    def test_lever2_electron_flow_iron_sulfur_support_subset_preflight_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-iron-sulfur-"
                    "support-subset-preflight-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_iron_sulfur_support_subset_preflight_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_readout",
            args.tiny_tranche_approval_readiness_readout,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_current_split_smoke_materialization_readout",
            args.current_split_smoke_materialization_readout,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout",
            args.approval_qualified_union_readout,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_projection_backed_pqq_nad_feature_sidecar_readout",
            args.projection_backed_pqq_nad_feature_sidecar_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )

    def test_lever2_electron_flow_candidate_train_cal_bundle_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-candidate-train-"
                    "cal-bundle-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_candidate_train_cal_bundle_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout",
            args.approval_qualified_union_readout,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_iron_sulfur_support_subset_preflight_readout",
            args.support_subset_preflight_readout,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_readout",
            args.relaxed_non_pqq_feature_sidecar_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )
        self.assertIn(
            "mechanism_feature_embedding_train_cal_input_manifest",
            args.train_cal_input_manifest,
        )

    def test_lever2_electron_flow_train_cal_sidecar_candidate_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-train-cal-"
                    "sidecar-candidate-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_train_cal_sidecar_candidate_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_candidate_train_cal_bundle_readout",
            args.candidate_train_cal_bundle_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )

    def test_lever2_electron_flow_approval_import_dry_run_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-approval-"
                    "import-dry-run-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_approval_import_dry_run_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_train_cal_sidecar_candidate_readout",
            args.train_cal_sidecar_candidate_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )
        self.assertIn(
            "mechanism_feature_embedding_train_cal_input_manifest",
            args.train_cal_input_manifest,
        )

    def test_lever2_electron_flow_approval_import_smoke_review_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-approval-import-"
                    "smoke-review-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_approval_import_smoke_review_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_approval_import_dry_run_readout",
            args.approval_import_dry_run_readout,
        )

    def test_lever2_electron_flow_approval_import_smoke_materialization_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-approval-import-"
                    "smoke-materialization-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_approval_import_smoke_materialization_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_approval_import_smoke_review_readout",
            args.approval_import_smoke_review_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )

    def test_lever2_electron_flow_approval_import_candidate_sidecar_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-approval-import-"
                    "candidate-sidecar-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_approval_import_candidate_sidecar_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_approval_import_smoke_materialization_readout",
            args.approval_import_smoke_materialization_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )

    def test_lever2_electron_flow_approval_import_delta_package_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-approval-import-"
                    "delta-package-readout"
                )
            ]
        )

        self.assertIn(
            "lever2_source_free_electron_flow_approval_import_delta_package_readout",
            args.out,
        )
        self.assertIn(
            "lever2_source_free_electron_flow_approval_import_candidate_sidecar_readout",
            args.approval_import_candidate_sidecar_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )

    def test_lever2_electron_flow_approval_import_delta_package_contract_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-approval-import-"
                    "delta-package-contract-readout"
                )
            ]
        )

        self.assertIn(
            (
                "lever2_source_free_electron_flow_approval_import_delta_"
                "package_contract_readout"
            ),
            args.out,
        )
        self.assertIn(
            (
                "lever2_source_free_electron_flow_approval_import_delta_"
                "package_readout"
            ),
            args.approval_import_delta_package_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )

    def test_lever2_electron_flow_protected_import_sequence_preflight_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-protected-import-"
                    "sequence-preflight-readout"
                )
            ]
        )

        self.assertIn(
            (
                "lever2_source_free_electron_flow_protected_import_"
                "sequence_preflight_readout"
            ),
            args.out,
        )
        self.assertIn(
            (
                "lever2_source_free_electron_flow_approval_import_delta_"
                "package_contract_readout"
            ),
            args.approval_import_delta_package_contract_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )

    def test_lever2_electron_flow_current_split_row_gate_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-current-split-row-"
                    "gate-audit-readout"
                )
            ]
        )

        self.assertIn(
            (
                "lever2_source_free_electron_flow_current_split_row_gate_"
                "audit_readout"
            ),
            args.out,
        )
        self.assertIn(
            (
                "lever2_source_free_electron_flow_protected_import_"
                "sequence_preflight_readout"
            ),
            args.protected_import_sequence_preflight_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )

    def test_lever2_electron_flow_protected_train_cal_approved_sidecar_import_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-protected-train-cal-"
                    "approved-sidecar-import-readout"
                )
            ]
        )

        self.assertIn(
            (
                "lever2_source_free_electron_flow_protected_train_cal_"
                "approved_sidecar_import_readout"
            ),
            args.out,
        )
        self.assertIn(
            (
                "lever2_source_free_electron_flow_protected_import_"
                "sequence_preflight_readout"
            ),
            args.protected_import_sequence_preflight_readout,
        )
        self.assertIn(
            "followup_pair_train_cal_feature_sidecar",
            args.train_cal_feature_sidecar,
        )
        self.assertIn("approved_sidecar_smoke", args.smoke_sidecar_out)
        self.assertIn("approved_sidecar_full", args.full_sidecar_out)

    def test_lever2_electron_flow_current_split_operating_point_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-current-split-"
                    "operating-point-readout"
                )
            ]
        )

        self.assertIn(
            (
                "lever2_source_free_electron_flow_current_split_operating_"
                "point_readout"
            ),
            args.out,
        )
        self.assertIn(
            (
                "lever2_source_free_electron_flow_current_split_row_gate_"
                "audit_readout"
            ),
            args.current_split_row_gate_audit_readout,
        )

    def test_lever2_electron_flow_current_split_sensitivity_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-current-split-"
                    "sensitivity-readout"
                )
            ]
        )

        self.assertIn(
            (
                "lever2_source_free_electron_flow_current_split_"
                "sensitivity_readout"
            ),
            args.out,
        )
        self.assertIn(
            (
                "lever2_source_free_electron_flow_current_split_operating_"
                "point_readout"
            ),
            args.current_split_operating_point_readout,
        )

    def test_lever2_electron_flow_current_split_field_sensitivity_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-lever2-source-free-electron-flow-current-split-"
                    "field-sensitivity-readout"
                )
            ]
        )

        self.assertIn(
            (
                "lever2_source_free_electron_flow_current_split_"
                "field_sensitivity_readout"
            ),
            args.out,
        )
        self.assertIn(
            (
                "lever2_source_free_electron_flow_current_split_row_gate_"
                "audit_readout"
            ),
            args.current_split_row_gate_audit_readout,
        )

    def test_lever2_source_free_axis_acquisition_ranking_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-lever2-source-free-mechanism-axis-acquisition-ranking-readout"
            ]
        )

        self.assertIn(
            "lever2_source_free_mechanism_axis_acquisition_ranking_readout",
            args.out,
        )
        self.assertIn("source_free_train_cal_projection_readout", args.projection_readout)
        self.assertIn(
            "source_free_projection_repair_candidate_surface",
            args.source_free_projection_repair_candidate_surface,
        )
        self.assertIn(
            "source_free_partial_surface_current_split_portability",
            args.partial_surface_current_split_portability_readout,
        )

    def test_lever2_current_extended_oos_mechanism_overlap_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-lever2-current-extended-oos-mechanism-overlap-readout"]
        )

        self.assertIn(
            "lever2_current_extended_oos_mechanism_overlap_readout",
            args.out,
        )
        self.assertIn("lever3_current_measured_readout", args.current_measured_readout)
        self.assertIn(
            "extended_train_cal_oos_surface", args.current_extended_oos_surface
        )
        self.assertIn(
            "best_token_followup_pair_no_template_rerun",
            args.mechanism_no_template_rerun,
        )
        self.assertIn("train_cal_feature_sidecar", args.train_cal_feature_sidecar)
        self.assertIn("source_free_train_cal_projection_readout", args.projection_readout)
        self.assertIn(
            "source_free_coordinate_anchor_candidates",
            args.source_free_coordinate_anchor_candidate_dir,
        )

    def test_lever2_event_axis_current_extended_frontier_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-lever2-event-axis-current-extended-frontier-readout"]
        )

        self.assertIn(
            "lever2_event_axis_current_extended_frontier_readout",
            args.out,
        )
        self.assertIn(
            "best_token_followup_pair_no_template_rerun",
            args.mechanism_no_template_rerun,
        )
        self.assertIn("train_cal_feature_sidecar", args.train_cal_feature_sidecar)
        self.assertIn(
            "lever2_current_extended_oos_mechanism_overlap_readout",
            args.current_extended_oos_mechanism_overlap_readout,
        )
        self.assertIn(
            "lever2_source_free_partial_surface_current_split_portability",
            args.partial_surface_current_split_portability_readout,
        )
        self.assertEqual(args.min_primary_retain, 0.9)

    def test_lever2_event_axis_loo_current_extended_frontier_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-lever2-event-axis-loo-current-extended-frontier-readout"]
        )

        self.assertIn(
            "lever2_event_axis_loo_current_extended_frontier_readout",
            args.out,
        )
        self.assertIn(
            "best_token_followup_pair_no_template_rerun",
            args.mechanism_no_template_rerun,
        )
        self.assertIn("train_cal_feature_sidecar", args.train_cal_feature_sidecar)
        self.assertIn(
            "lever2_current_extended_oos_mechanism_overlap_readout",
            args.current_extended_oos_mechanism_overlap_readout,
        )
        self.assertIn(
            "lever2_source_free_partial_surface_current_split_portability",
            args.partial_surface_current_split_portability_readout,
        )
        self.assertEqual(args.min_primary_retain, 0.9)
        self.assertEqual(
            args.baseline_axis_id, "source_free_projected_proton_role_subset"
        )

    def test_lever2_event_axis_primary_safe_frontier_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-lever2-event-axis-primary-safe-frontier-readout"]
        )

        self.assertIn(
            "lever2_event_axis_primary_safe_frontier_readout",
            args.out,
        )
        self.assertIn(
            "best_token_followup_pair_no_template_rerun",
            args.mechanism_no_template_rerun,
        )
        self.assertIn("train_cal_feature_sidecar", args.train_cal_feature_sidecar)
        self.assertIn(
            "lever2_current_extended_oos_mechanism_overlap_readout",
            args.current_extended_oos_mechanism_overlap_readout,
        )
        self.assertIn(
            "lever2_source_free_partial_surface_current_split_portability",
            args.partial_surface_current_split_portability_readout,
        )
        self.assertEqual(args.min_primary_retain, 1.0)
        self.assertEqual(
            args.baseline_axis_id, "source_free_projected_proton_role_subset"
        )

    def test_lever2_event_axis_primary_controlled_rescue_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-lever2-event-axis-primary-controlled-rescue-readout"]
        )

        self.assertIn(
            "lever2_event_axis_primary_controlled_rescue_readout",
            args.out,
        )
        self.assertIn(
            "best_token_followup_pair_no_template_rerun",
            args.mechanism_no_template_rerun,
        )
        self.assertIn("train_cal_feature_sidecar", args.train_cal_feature_sidecar)
        self.assertIn(
            "lever2_current_extended_oos_mechanism_overlap_readout",
            args.current_extended_oos_mechanism_overlap_readout,
        )
        self.assertIn(
            "lever2_source_free_partial_surface_current_split_portability",
            args.partial_surface_current_split_portability_readout,
        )
        self.assertEqual(args.min_primary_retain, 1.0)
        self.assertEqual(
            args.baseline_axis_id, "source_free_projected_proton_role_subset"
        )

    def test_lever2_event_axis_signature_excluded_frontier_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-lever2-event-axis-signature-excluded-frontier-readout"]
        )

        self.assertIn(
            "lever2_event_axis_signature_excluded_frontier_readout",
            args.out,
        )
        self.assertIn(
            "best_token_followup_pair_no_template_rerun",
            args.mechanism_no_template_rerun,
        )
        self.assertIn("train_cal_feature_sidecar", args.train_cal_feature_sidecar)
        self.assertIn(
            "lever2_current_extended_oos_mechanism_overlap_readout",
            args.current_extended_oos_mechanism_overlap_readout,
        )
        self.assertIn(
            "lever2_source_free_partial_surface_current_split_portability",
            args.partial_surface_current_split_portability_readout,
        )
        self.assertEqual(args.min_primary_retain, 1.0)
        self.assertEqual(
            args.baseline_axis_id, "source_free_projected_proton_role_subset"
        )
        self.assertEqual(
            args.signature_axis_id, "source_free_projected_proton_role_subset"
        )

    def test_lever2_event_axis_primary_controlled_null_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-lever2-event-axis-primary-controlled-null-readout"]
        )

        self.assertIn(
            "lever2_event_axis_primary_controlled_null_readout",
            args.out,
        )
        self.assertIn(
            "best_token_followup_pair_no_template_rerun",
            args.mechanism_no_template_rerun,
        )
        self.assertIn("train_cal_feature_sidecar", args.train_cal_feature_sidecar)
        self.assertIn(
            "lever2_current_extended_oos_mechanism_overlap_readout",
            args.current_extended_oos_mechanism_overlap_readout,
        )
        self.assertEqual(args.min_primary_retain, 1.0)
        self.assertEqual(
            args.baseline_axis_id, "source_free_projected_proton_role_subset"
        )
        self.assertEqual(args.null_permutations, 128)
        self.assertEqual(
            args.null_seed, "lever2_primary_controlled_event_axis_null_v0"
        )

    def test_lever2_event_motif_interaction_null_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-lever2-event-motif-interaction-null-readout"]
        )

        self.assertIn(
            "lever2_event_motif_interaction_null_readout",
            args.out,
        )
        self.assertIn(
            "best_token_followup_pair_no_template_rerun",
            args.mechanism_no_template_rerun,
        )
        self.assertIn("train_cal_feature_sidecar", args.train_cal_feature_sidecar)
        self.assertIn(
            "lever2_current_extended_oos_mechanism_overlap_readout",
            args.current_extended_oos_mechanism_overlap_readout,
        )
        self.assertIn(
            "lever2_source_free_partial_surface_current_split_portability",
            args.partial_surface_current_split_portability_readout,
        )
        self.assertEqual(args.min_primary_retain, 1.0)
        self.assertEqual(
            args.baseline_axis_id, "source_free_projected_proton_role_subset"
        )
        self.assertEqual(args.null_permutations, 128)
        self.assertEqual(args.null_seed, "lever2_event_motif_interaction_null_v0")

    def test_lever2_event_axis_signature_exclusion_sensitivity_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-lever2-event-axis-signature-exclusion-sensitivity-readout"]
        )

        self.assertIn(
            "lever2_event_axis_signature_exclusion_sensitivity_readout",
            args.out,
        )
        self.assertIn(
            "best_token_followup_pair_no_template_rerun",
            args.mechanism_no_template_rerun,
        )
        self.assertIn("train_cal_feature_sidecar", args.train_cal_feature_sidecar)
        self.assertEqual(args.min_primary_retain, 1.0)
        self.assertEqual(
            args.baseline_axis_id, "source_free_projected_proton_role_subset"
        )
        self.assertEqual(
            args.signature_axis_ids,
            [
                "source_free_projected_proton_role_subset",
                "bond_change",
                "electron_flow",
                "event_topology",
            ],
        )

    def test_lever2_partial_surface_current_split_portability_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-lever2-source-free-partial-surface-current-split-portability-readout"
            ]
        )

        self.assertIn(
            "lever2_source_free_partial_surface_current_split_portability_readout",
            args.out,
        )
        self.assertIn("lever3_current_measured_readout", args.current_measured_readout)
        self.assertIn(
            "extended_train_cal_oos_surface", args.current_extended_oos_surface
        )
        self.assertIn(
            "source_free_projection_repair_candidate_surface",
            args.source_free_projection_repair_candidate_surface,
        )
        self.assertIn(
            "source_free_event_axis_linker_materialization_gate",
            args.source_free_event_axis_linker_materialization_gate,
        )
        self.assertIn(
            "source_free_locator_rewrite_materialization_gate_materialized",
            args.source_free_locator_rewrite_materialization_gate,
        )
        self.assertIn(
            "family_panel_source_free_active_site_locator_candidates",
            args.review_only_locator_candidate_dir,
        )

    def test_lever3_current_measured_readout_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            ["build-fold-augmented-lever3-current-measured-readout"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_current_measured_readout_"
                "current702_20260604.json"
            ),
        )
        self.assertIn(
            "post_followup_protein_only_fold_topology_residual_extended_train_cal",
            args.latest_train_cal_oos_surface,
        )
        self.assertIn(
            "after_q43088_locator_approval",
            args.current_evidence_after_q43088_locator_approval,
        )

    def test_loose_same_family_pressure_readout_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-confounded-proxy-loose-same-family-pressure-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_confounded_proxy_loose_same_family_"
                "pressure_readout_current702_20260604.json"
            ),
        )
        self.assertIn("current_measured_readout", args.current_measured_readout)
        self.assertIn("acquisition_queue", args.acquisition_queue)
        self.assertIn(
            "same_family_structural_acquisition_contract",
            args.same_family_structural_acquisition_contract,
        )

    def test_lever3_evidence_sufficiency_readout_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            ["build-fold-augmented-lever3-evidence-sufficiency-readout"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_evidence_sufficiency_"
                "readout_current702_20260604.json"
            ),
        )
        self.assertIn("current_measured_readout", args.current_measured_readout)
        self.assertIn(
            "near_cofactor_pressure_scored_readout",
            args.near_cofactor_pressure_readout,
        )
        self.assertIn(
            "loose_same_family_pressure_readout",
            args.loose_same_family_pressure_readout,
        )
        self.assertIn(
            "protein_only_fold_topology_residual_scored_readout",
            args.protein_only_topology_scored_readout,
        )
        self.assertIn(
            "p07658_prediction_acceptance_preflight",
            args.p07658_prediction_acceptance_preflight,
        )
        self.assertIn(
            "p07658_local_predictor_runtime_scan",
            args.p07658_local_predictor_runtime_scan,
        )
        self.assertIn(
            "p07658_full_length_predictor_provider_probe",
            args.p07658_full_length_predictor_provider_probe,
        )
        self.assertIn(
            "p07658_3dbeacons_predicted_structure_probe",
            args.p07658_three_d_beacons_predicted_structure_probe,
        )
        self.assertIn(
            "p07658_computed_model_repository_broad_probe",
            args.p07658_computed_model_repository_broad_probe,
        )

    def test_lever3_channel_veto_readout_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            ["build-fold-augmented-lever3-channel-veto-readout"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_channel_veto_readout_"
                "current702_20260604.json"
            ),
        )
        self.assertIn(
            "abstention_threshold_contract_current702",
            args.in_scope_threshold_contract,
        )
        self.assertIn(
            "expanded_oos_calibrated",
            args.expanded_oos_calibrated_threshold_contract,
        )
        self.assertIn(
            "post_followup_protein_only_fold_topology_residual_extended_train_cal",
            args.latest_train_cal_oos_surface,
        )
        self.assertIn("current_measured_readout", args.current_measured_readout)

    def test_lever3_retention_frontier_readout_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            ["build-fold-augmented-lever3-retention-frontier-readout"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_retention_frontier_readout_"
                "current702_20260604.json"
            ),
        )
        self.assertIn(
            "abstention_threshold_contract_current702",
            args.in_scope_threshold_contract,
        )
        self.assertIn(
            "expanded_oos_calibrated",
            args.expanded_oos_calibrated_threshold_contract,
        )
        self.assertIn("current_measured_readout", args.current_measured_readout)
        self.assertIn(
            "p07658_biolm_single_provider_attempt",
            args.p07658_provider_attempt,
        )

    def test_lever3_residual_safety_readout_parser_defaults(self) -> None:
        args = build_parser().parse_args(
            ["build-fold-augmented-lever3-residual-safety-readout"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_residual_safety_readout_"
                "current702_20260604.json"
            ),
        )
        self.assertIn(
            "lever3_retention_frontier_readout",
            args.retention_frontier_readout,
        )
        self.assertIn("lever3_channel_veto_readout", args.channel_veto_readout)
        self.assertIn(
            "abstention_threshold_contract_current702",
            args.in_scope_threshold_contract,
        )
        self.assertEqual(args.near_margin_epsilon, 0.05)

    def test_lever3_cofactor_context_counteraxis_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-fold-augmented-lever3-cofactor-context-counteraxis-readout"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_cofactor_context_"
                "counteraxis_readout_current702_20260604.json"
            ),
        )
        self.assertIn(
            "abstention_threshold_contract_current702",
            args.in_scope_threshold_contract,
        )
        self.assertIn(
            "post_followup_protein_only_fold_topology_residual_extended_train_cal",
            args.latest_train_cal_oos_surface,
        )
        self.assertIn("current_measured_readout", args.current_measured_readout)
        self.assertIn("lever3_channel_veto_readout", args.channel_veto_readout)
        self.assertIn("lever3_residual_safety_readout", args.residual_safety_readout)
        self.assertIn(
            "predicted_geometry_in_distribution_atlas_retrieval",
            args.predicted_geometry_atlas_retrieval,
        )

    def test_lever3_same_family_bandpass_counteraxis_contract_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-fold-augmented-lever3-same-family-bandpass-"
                    "counteraxis-contract"
                )
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_same_family_bandpass_"
                "counteraxis_contract_current702_20260604.json"
            ),
        )
        self.assertIn(
            "lever3_cofactor_context_counteraxis_readout",
            args.cofactor_context_counteraxis_readout,
        )
        self.assertIn(
            "same_family_bandpass_counteraxis_contract",
            args.report,
        )

    def test_lever3_post_bandpass_deployment_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-fold-augmented-lever3-post-bandpass-deployment-readout"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_post_bandpass_deployment_"
                "readout_current702_20260604.json"
            ),
        )
        self.assertIn(
            "lever3_cofactor_context_counteraxis_readout",
            args.cofactor_context_counteraxis_readout,
        )
        self.assertIn(
            "same_family_bandpass_counteraxis_contract",
            args.same_family_bandpass_counteraxis_contract,
        )
        self.assertIn(
            "p07658_prediction_acceptance_preflight",
            args.p07658_prediction_acceptance_preflight,
        )
        self.assertIn(
            "p07658_prediction_dispatch_packet",
            args.p07658_prediction_dispatch_packet,
        )

    def test_lever3_p07658_exact_route_attempt_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                (
                    "build-fold-augmented-lever3-p07658-exact-route-"
                    "attempt-readout"
                )
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_p07658_exact_route_"
                "attempt_readout_current702_20260604.json"
            ),
        )
        self.assertIn(
            "post_bandpass_deployment_readout",
            args.post_bandpass_deployment_readout,
        )
        self.assertIn(
            "p07658_exact_route_attempts",
            args.exact_route_attempts,
        )
        self.assertIn(
            "p07658_exact_route_attempt_readout",
            args.report,
        )

    def test_lever3_operating_point_deployment_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-fold-augmented-lever3-operating-point-deployment-readout"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_operating_point_"
                "deployment_readout_current702_20260604.json"
            ),
        )
        self.assertIn(
            "lever3_cofactor_context_counteraxis_readout",
            args.cofactor_context_counteraxis_readout,
        )
        self.assertIn(
            "same_family_bandpass_counteraxis_contract",
            args.same_family_bandpass_counteraxis_contract,
        )
        self.assertIn(
            "post_bandpass_deployment_readout",
            args.post_bandpass_deployment_readout,
        )
        self.assertIn(
            "p07658_exact_route_attempt_readout",
            args.p07658_exact_route_attempt_readout,
        )
        self.assertIn(
            "lever3_operating_point_deployment_readout",
            args.report,
        )

    def test_lever3_p07658_credential_route_preflight_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-fold-augmented-lever3-p07658-credential-route-preflight"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_p07658_credential_"
                "route_preflight_current702_20260604.json"
            ),
        )
        self.assertIn(
            "operating_point_deployment_readout",
            args.operating_point_deployment_readout,
        )
        self.assertIn(
            "p07658_credential_route_preflight",
            args.report,
        )

    def test_lever3_deployment_input_gap_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-fold-augmented-lever3-deployment-input-gap-audit"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_input_gap_"
                "audit_current702_20260604.json"
            ),
        )
        self.assertIn(
            "operating_point_deployment_readout",
            args.operating_point_deployment_readout,
        )
        self.assertIn(
            "p07658_credential_route_preflight",
            args.p07658_credential_route_preflight,
        )
        self.assertIn(
            "p07658_prediction_acceptance_preflight",
            args.p07658_prediction_acceptance_preflight,
        )
        self.assertIn(
            "p07658_prediction_dispatch_packet",
            args.p07658_prediction_dispatch_packet,
        )
        self.assertIn(
            "lever3_deployment_input_gap_audit",
            args.report,
        )

    def test_lever3_p07658_local_input_inventory_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-fold-augmented-lever3-p07658-local-input-inventory-audit"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_p07658_local_input_"
                "inventory_audit_current702_20260604.json"
            ),
        )
        self.assertIn(
            "lever3_deployment_input_gap_audit",
            args.deployment_input_gap_audit,
        )
        self.assertIn(
            "p07658_prediction_dispatch_packet",
            args.p07658_prediction_dispatch_packet,
        )
        self.assertEqual(args.search_root, ["artifacts", "work"])
        self.assertIn(
            "p07658_local_input_inventory_audit",
            args.report,
        )

    def test_lever3_p07658_sequence_compatibility_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-p07658-sequence-"
                "compatibility-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_p07658_sequence_"
                "compatibility_readout_current702_20260604.json"
            ),
        )
        self.assertIn(
            "p07658_full_length_prediction_request_manifest",
            args.prediction_request_manifest,
        )
        self.assertIn(
            "p07658_prediction_dispatch_packet",
            args.p07658_prediction_dispatch_packet,
        )
        self.assertIn(
            "p07658_exact_route_attempts",
            args.p07658_exact_route_attempts,
        )
        self.assertIn(
            "p07658_credential_route_preflight",
            args.p07658_credential_route_preflight,
        )
        self.assertIn(
            "p07658_local_input_inventory_audit",
            args.p07658_local_input_inventory_audit,
        )
        self.assertIn(
            "p07658_full_length_prediction_input",
            args.provider_ready_fasta,
        )
        self.assertIn(
            "p07658_sequence_compatibility_readout",
            args.report,
        )

    def test_lever3_confounded_safe_abstention_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-confounded-safe-"
                "abstention-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_confounded_safe_"
                "abstention_readout_current702_20260604.json"
            ),
        )
        self.assertIn(
            "operating_point_deployment_readout",
            args.operating_point_deployment_readout,
        )
        self.assertIn(
            "p07658_sequence_compatibility_readout",
            args.p07658_sequence_compatibility_readout,
        )
        self.assertIn(
            "lever3_deployment_input_gap_audit",
            args.deployment_input_gap_audit,
        )
        self.assertIn(
            "lever3_confounded_safe_abstention_readout",
            args.report,
        )

    def test_lever3_deployment_action_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-action-"
                "readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_action_"
                "readout_current702_20260604.json"
            ),
        )
        self.assertIn(
            "lever3_residual_safety_readout",
            args.residual_safety_readout,
        )
        self.assertIn(
            "lever3_cofactor_context_counteraxis_readout",
            args.cofactor_context_counteraxis_readout,
        )
        self.assertIn(
            "lever3_same_family_bandpass_counteraxis_contract",
            args.same_family_bandpass_counteraxis_contract,
        )
        self.assertIn(
            "lever3_confounded_safe_abstention_readout",
            args.confounded_safe_abstention_readout,
        )
        self.assertIn(
            "lever3_deployment_action_readout",
            args.report,
        )

    def test_lever3_retained_residual_risk_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-retained-residual-risk-"
                "readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_retained_residual_"
                "risk_readout_current702_20260604.json"
            ),
        )
        self.assertIn(
            "lever3_deployment_action_readout",
            args.deployment_action_readout,
        )
        self.assertIn(
            "lever3_retained_residual_risk_readout",
            args.report,
        )

    def test_lever3_descriptor_present_counteraxis_preflight_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-descriptor-present-"
                "counteraxis-preflight"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_descriptor_present_"
                "counteraxis_preflight_current702_20260604.json"
            ),
        )
        self.assertIn(
            "lever3_retained_residual_risk_readout",
            args.retained_residual_risk_readout,
        )
        self.assertIn(
            "post_followup_protein_only_fold_topology_residual_extended_train_cal",
            args.latest_train_cal_oos_surface,
        )
        self.assertIn(
            "descriptor_present_counteraxis_preflight",
            args.report,
        )

    def test_lever3_descriptor_generalization_counteraxis_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-descriptor-generalization-"
                "counteraxis-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_descriptor_generalization_"
                "counteraxis_readout_current702_20260604.json"
            ),
        )
        self.assertIn(
            "descriptor_present_counteraxis_preflight",
            args.descriptor_present_counteraxis_preflight,
        )
        self.assertIn(
            "lever3_retained_residual_risk_readout",
            args.retained_residual_risk_readout,
        )
        self.assertIn(
            "post_followup_protein_only_fold_topology_residual_extended_train_cal",
            args.latest_train_cal_oos_surface,
        )
        self.assertIn(
            "predicted_geometry_in_distribution_atlas_retrieval",
            args.predicted_geometry_atlas_retrieval,
        )
        self.assertIn(
            "abstention_threshold_contract",
            args.threshold_contract,
        )
        self.assertIn(
            "lever3_channel_veto_readout",
            args.channel_veto_readout,
        )
        self.assertIn(
            "descriptor_generalization_counteraxis_readout",
            args.report,
        )

    def test_lever3_retained_descriptor_rescue_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-retained-descriptor-"
                "rescue-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_retained_descriptor_"
                "rescue_readout_current702_20260604.json"
            ),
        )
        self.assertIn(
            "lever3_retained_residual_risk_readout",
            args.retained_residual_risk_readout,
        )
        self.assertIn(
            "descriptor_generalization_counteraxis_readout",
            args.descriptor_generalization_counteraxis_readout,
        )
        self.assertGreaterEqual(len(args.descriptor_source_artifact), 4)
        self.assertIn(
            "train_cal_scored_extension_tranche2",
            args.descriptor_source_artifact[0],
        )
        self.assertIn(
            "retained_descriptor_rescue_readout",
            args.report,
        )

    def test_lever3_retained_pairwise_descriptor_counteraxis_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-retained-pairwise-"
                "descriptor-counteraxis-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_retained_pairwise_"
                "descriptor_counteraxis_readout_current702_20260604.json"
            ),
        )
        self.assertIn(
            "descriptor_present_counteraxis_preflight",
            args.descriptor_present_counteraxis_preflight,
        )
        self.assertIn(
            "retained_descriptor_rescue_readout",
            args.retained_descriptor_rescue_readout,
        )
        self.assertIn(
            "post_followup_protein_only_fold_topology_residual_extended_train_cal",
            args.latest_train_cal_oos_surface,
        )
        self.assertEqual(args.max_all_train_cal_oos_rows_fired, 8)
        self.assertIn(
            "retained_pairwise_descriptor_counteraxis_readout",
            args.report,
        )

    def test_lever3_retained_channel_margin_counteraxis_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-retained-channel-margin-"
                "counteraxis-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_retained_channel_margin_"
                "counteraxis_readout_current702_20260604.json"
            ),
        )
        self.assertIn(
            "retained_pairwise_descriptor_counteraxis_readout",
            args.retained_pairwise_descriptor_counteraxis_readout,
        )
        self.assertIn(
            "lever3_residual_safety_readout",
            args.residual_safety_readout,
        )
        self.assertIn(
            "lever3_cofactor_context_counteraxis_readout",
            args.cofactor_context_counteraxis_readout,
        )
        self.assertIn(
            "post_followup_protein_only_fold_topology_residual_extended_train_cal",
            args.latest_train_cal_oos_surface,
        )
        self.assertEqual(args.max_all_train_cal_oos_rows_fired, 50)
        self.assertIn(
            "retained_channel_margin_counteraxis_readout",
            args.report,
        )

    def test_lever3_retained_pocket_chemistry_counteraxis_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-retained-pocket-chemistry-"
                "counteraxis-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_retained_pocket_chemistry_"
                "counteraxis_readout_current702_20260605.json"
            ),
        )
        self.assertIn(
            "retained_channel_margin_counteraxis_readout",
            args.retained_channel_margin_counteraxis_readout,
        )
        self.assertIn(
            "retained_pairwise_descriptor_counteraxis_readout",
            args.retained_pairwise_descriptor_counteraxis_readout,
        )
        self.assertIn(
            "retained_descriptor_rescue_readout",
            args.retained_descriptor_rescue_readout,
        )
        self.assertIn(
            "post_followup_protein_only_fold_topology_residual_extended_train_cal",
            args.latest_train_cal_oos_surface,
        )
        self.assertEqual(args.max_all_train_cal_oos_rows_fired, 8)
        self.assertIn(
            "retained_pocket_chemistry_counteraxis_readout",
            args.report,
        )

    def test_lever3_retained_geometry_mismatch_counteraxis_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-retained-geometry-mismatch-"
                "counteraxis-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_retained_geometry_mismatch_"
                "counteraxis_readout_current702_20260605.json"
            ),
        )
        self.assertIn(
            "retained_pocket_chemistry_counteraxis_readout",
            args.retained_pocket_chemistry_counteraxis_readout,
        )
        self.assertIn(
            "retained_channel_margin_counteraxis_readout",
            args.retained_channel_margin_counteraxis_readout,
        )
        self.assertIn(
            "post_followup_protein_only_fold_topology_residual_extended_train_cal",
            args.latest_train_cal_oos_surface,
        )
        self.assertEqual(args.min_design_same_family_rows_fired, 2)
        self.assertEqual(args.min_all_train_cal_oos_rows_fired, 5)
        self.assertEqual(args.max_all_train_cal_oos_rows_fired, 8)
        self.assertIn(
            "retained_geometry_mismatch_counteraxis_readout",
            args.report,
        )

    def test_lever3_operating_point_closure_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-operating-point-"
                "closure-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_operating_point_closure_"
                "readout_current702_20260605.json"
            ),
        )
        self.assertIn(
            "lever3_deployment_action_readout",
            args.deployment_action_readout,
        )
        self.assertIn(
            "retained_pairwise_descriptor_counteraxis_readout",
            args.retained_pairwise_descriptor_counteraxis_readout,
        )
        self.assertIn(
            "retained_channel_margin_counteraxis_readout",
            args.retained_channel_margin_counteraxis_readout,
        )
        self.assertIn(
            "retained_pocket_chemistry_counteraxis_readout",
            args.retained_pocket_chemistry_counteraxis_readout,
        )
        self.assertIn(
            "retained_geometry_mismatch_counteraxis_readout",
            args.retained_geometry_mismatch_counteraxis_readout,
        )
        self.assertIn(
            "operating_point_closure_readout",
            args.report,
        )

    def test_lever3_closure_reproducibility_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-closure-"
                "reproducibility-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_closure_"
                "reproducibility_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "operating_point_closure_readout",
            args.operating_point_closure_readout,
        )
        self.assertIn(
            "closure_reproducibility_audit",
            args.report,
        )

    def test_lever3_operating_point_application_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-operating-point-"
                "application-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_operating_point_"
                "application_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "operating_point_closure_readout",
            args.operating_point_closure_readout,
        )
        self.assertIn(
            "closure_reproducibility_audit",
            args.closure_reproducibility_audit,
        )
        self.assertIn(
            "operating_point_application_audit",
            args.report,
        )

    def test_lever3_deployment_contract_readiness_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-contract-"
                "readiness-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_contract_"
                "readiness_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "operating_point_application_audit",
            args.operating_point_application_audit,
        )
        self.assertIn(
            "deployment_contract_readiness_audit",
            args.report,
        )

    def test_lever3_deployment_contract_lineage_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-contract-"
                "lineage-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_contract_"
                "lineage_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_contract_readiness_audit",
            args.deployment_contract_readiness_audit,
        )
        self.assertIn(
            "deployment_contract_lineage_audit",
            args.report,
        )

    def test_lever3_deployment_contract_reproducibility_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-contract-"
                "reproducibility-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_contract_"
                "reproducibility_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_contract_readiness_audit",
            args.deployment_contract_readiness_audit,
        )
        self.assertIn(
            "deployment_contract_lineage_audit",
            args.deployment_contract_lineage_audit,
        )
        self.assertIn(
            "deployment_contract_reproducibility_audit",
            args.report,
        )

    def test_lever3_deployment_operator_manifest_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-operator-"
                "manifest-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_operator_"
                "manifest_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_contract_reproducibility_audit",
            args.deployment_contract_reproducibility_audit,
        )
        self.assertIn(
            "deployment_contract_readiness_audit",
            args.deployment_contract_readiness_audit,
        )
        self.assertIn(
            "deployment_operator_manifest_audit",
            args.report,
        )

    def test_lever3_deployment_operator_manifest_reproducibility_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-operator-"
                "manifest-reproducibility-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_operator_"
                "manifest_reproducibility_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_operator_manifest_audit",
            args.deployment_operator_manifest_audit,
        )
        self.assertIn(
            "deployment_operator_manifest_reproducibility_audit",
            args.report,
        )

    def test_lever3_deployment_stage_provenance_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            ["build-fold-augmented-lever3-deployment-stage-provenance-audit"]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_stage_"
                "provenance_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_operator_manifest_audit",
            args.deployment_operator_manifest_audit,
        )
        self.assertIn(
            "deployment_contract_lineage_audit",
            args.deployment_contract_lineage_audit,
        )
        self.assertIn(
            "deployment_stage_provenance_audit",
            args.report,
        )

    def test_lever3_deployment_stage_provenance_reproducibility_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-stage-"
                "provenance-reproducibility-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_stage_"
                "provenance_reproducibility_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_stage_provenance_audit",
            args.deployment_stage_provenance_audit,
        )
        self.assertIn(
            "deployment_stage_provenance_reproducibility_audit",
            args.report,
        )

    def test_lever3_deployment_operator_route_class_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-operator-"
                "route-class-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_operator_"
                "route_class_readout_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_stage_provenance_reproducibility_audit",
            args.deployment_stage_provenance_reproducibility_audit,
        )
        self.assertIn(
            "deployment_operator_manifest_audit",
            args.deployment_operator_manifest_audit,
        )
        self.assertIn("deployment_operator_route_class_readout", args.report)

    def test_lever3_deployment_operator_route_class_reproducibility_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-operator-"
                "route-class-reproducibility-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_operator_"
                "route_class_reproducibility_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_operator_route_class_readout",
            args.deployment_operator_route_class_readout,
        )
        self.assertIn(
            "deployment_operator_route_class_reproducibility_audit",
            args.report,
        )

    def test_lever3_deployment_operator_route_class_provenance_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-operator-"
                "route-class-provenance-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_operator_"
                "route_class_provenance_readout_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_operator_route_class_readout",
            args.deployment_operator_route_class_readout,
        )
        self.assertIn(
            "deployment_stage_provenance_audit",
            args.deployment_stage_provenance_audit,
        )
        self.assertIn(
            "deployment_operator_route_class_provenance_readout",
            args.report,
        )

    def test_lever3_deployment_operator_route_class_provenance_reproducibility_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-operator-"
                "route-class-provenance-reproducibility-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_operator_"
                "route_class_provenance_reproducibility_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_operator_route_class_provenance_readout",
            args.deployment_operator_route_class_provenance_readout,
        )
        self.assertIn(
            "deployment_operator_route_class_provenance_reproducibility_audit",
            args.report,
        )

    def test_lever3_deployment_operator_transfer_safety_matrix_readout_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-operator-"
                "transfer-safety-matrix-readout"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_operator_"
                "transfer_safety_matrix_readout_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_operator_route_class_readout",
            args.deployment_operator_route_class_readout,
        )
        self.assertIn(
            "deployment_operator_route_class_provenance_readout",
            args.deployment_operator_route_class_provenance_readout,
        )
        self.assertIn(
            "deployment_operator_route_class_provenance_reproducibility_audit",
            args.deployment_operator_route_class_provenance_reproducibility_audit,
        )
        self.assertIn(
            "deployment_operator_transfer_safety_matrix_readout",
            args.report,
        )

    def test_lever3_deployment_operator_transfer_safety_matrix_reproducibility_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-operator-"
                "transfer-safety-matrix-reproducibility-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_operator_"
                "transfer_safety_matrix_reproducibility_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_operator_transfer_safety_matrix_readout",
            args.deployment_operator_transfer_safety_matrix_readout,
        )
        self.assertIn(
            "deployment_operator_transfer_safety_matrix_reproducibility_audit",
            args.report,
        )

    def test_lever3_deployment_operator_transfer_safety_application_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-operator-"
                "transfer-safety-application-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_operator_"
                "transfer_safety_application_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_operator_transfer_safety_matrix_readout",
            args.deployment_operator_transfer_safety_matrix_readout,
        )
        self.assertIn(
            "deployment_operator_transfer_safety_matrix_reproducibility_audit",
            args.deployment_operator_transfer_safety_matrix_reproducibility_audit,
        )
        self.assertIn(
            "deployment_operator_transfer_safety_application_audit",
            args.report,
        )

    def test_lever3_deployment_operator_transfer_safety_application_reproducibility_audit_parser_defaults(
        self,
    ) -> None:
        args = build_parser().parse_args(
            [
                "build-fold-augmented-lever3-deployment-operator-"
                "transfer-safety-application-reproducibility-audit"
            ]
        )

        self.assertEqual(
            args.out,
            (
                "artifacts/v3_fold_augmented_lever3_deployment_operator_"
                "transfer_safety_application_reproducibility_audit_current702_20260605.json"
            ),
        )
        self.assertIn(
            "deployment_operator_transfer_safety_application_audit",
            args.deployment_operator_transfer_safety_application_audit,
        )
        self.assertIn(
            "deployment_operator_transfer_safety_application_reproducibility_audit",
            args.report,
        )

    def test_active_lever_commands_default_to_reviewed_locator_decisions(
        self,
    ) -> None:
        source_intake_args = build_parser().parse_args(
            ["build-active-lever-source-decision-intake-preflight"]
        )
        reviewer_queue_args = build_parser().parse_args(
            ["build-active-lever-reviewer-decision-queue"]
        )
        event_axis_gate_args = build_parser().parse_args(
            [
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "event-axis-linker-materialization-gate"
                )
            ]
        )

        self.assertIn(
            "source_free_locator_rewrite_approval_decisions_current702_20260603.json",
            source_intake_args.lever2_locator_rewrite_approval_packet,
        )
        self.assertIn(
            "source_free_locator_rewrite_approval_decisions_current702_20260603.json",
            reviewer_queue_args.lever2_locator_rewrite_approval_packet,
        )
        self.assertIn(
            "source_free_event_axis_linker_signoff_finalization_current702_20260603.json",
            event_axis_gate_args.linker_rows,
        )

    def test_label_factory_gate_cli_lineage_rejects_mismatched_slices(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            required = {
                "label_factory_audit": str(root / "v3_label_factory_audit_1000.json"),
                "applied_label_factory": str(
                    root / "v3_label_factory_applied_labels_1025.json"
                ),
                "active_learning_queue": str(
                    root / "v3_active_learning_review_queue_1000.json"
                ),
                "adversarial_negatives": str(
                    root / "v3_adversarial_negative_controls_1000.json"
                ),
                "expert_review_export": str(
                    root / "v3_expert_review_export_1000_post_batch.json"
                ),
                "family_propagation_guardrails": str(
                    root / "v3_family_propagation_guardrails_1000.json"
                ),
            }
            optional = {
                "atp_phosphoryl_transfer_family_expansion": str(
                    root / "v3_atp_phosphoryl_transfer_family_expansion_700.json"
                )
            }

            with self.assertRaisesRegex(
                ValueError,
                "mismatched label-factory gate artifact lineage",
            ):
                _validate_label_factory_gate_cli_lineage(
                    labels_path=str(root / "curated_mechanism_labels.json"),
                    required_artifacts=required,
                    optional_artifacts=optional,
                )

    def test_label_factory_gate_cli_lineage_rejects_payload_slice_mismatch(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            required = {
                "label_factory_audit": str(root / "v3_label_factory_audit_1000.json"),
                "applied_label_factory": str(
                    root / "v3_label_factory_applied_labels_1000.json"
                ),
                "active_learning_queue": str(
                    root / "v3_active_learning_review_queue_1000.json"
                ),
                "adversarial_negatives": str(
                    root / "v3_adversarial_negative_controls_1000.json"
                ),
                "expert_review_export": str(
                    root / "v3_expert_review_export_1000_post_batch.json"
                ),
                "family_propagation_guardrails": str(
                    root / "v3_family_propagation_guardrails_1000.json"
                ),
            }
            loaded_artifacts = {
                field_name: {
                    "metadata": {
                        "method": field_name,
                        "slice_id": 1000,
                    }
                }
                for field_name in required
            }
            loaded_artifacts["active_learning_queue"]["metadata"]["slice_id"] = 975

            with self.assertRaisesRegex(
                ValueError,
                "payload slice id 975 conflicts with path slice id 1000",
            ):
                _validate_label_factory_gate_cli_lineage(
                    labels_path=str(root / "curated_mechanism_labels.json"),
                    required_artifacts=required,
                    optional_artifacts={},
                    loaded_artifacts=loaded_artifacts,
                )

    def test_validate_command(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "catalytic_earth.cli", "validate"],
            cwd=ROOT,
            env={"PYTHONPATH": str(ROOT / "src")},
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Validated", result.stdout)

    def test_current702_northstar_carryover_commands_are_registered(self) -> None:
        parser = build_parser()
        cases = [
            (
                "audit-predicted-structure-fold-channel-deployment-input",
                "cmd_audit_predicted_structure_fold_channel_deployment_input",
            ),
            (
                "audit-predicted-structure-fold-channel-coordinate-provenance",
                "cmd_audit_predicted_structure_fold_channel_coordinate_provenance",
            ),
            (
                "build-predicted-structure-fold-channel-reproduction-manifest",
                (
                    "cmd_build_predicted_structure_fold_channel_"
                    "reproduction_manifest"
                ),
            ),
            (
                "audit-predicted-structure-fold-channel-carryover-resolution",
                (
                    "cmd_audit_predicted_structure_fold_channel_"
                    "carryover_resolution"
                ),
            ),
            (
                "build-mechanism-feature-row-specific-bond-change-schema",
                "cmd_build_mechanism_feature_row_specific_bond_change_schema",
            ),
            (
                "audit-mechanism-feature-row-specific-bond-change-feature-contract-gap",
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "feature_contract_gap"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "materialization-priority"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "materialization_priority"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-source-graph-readiness"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_source_graph_readiness"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-extraction-work-package"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_extraction_work_package"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-extraction-package-strict"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_extraction_package_strict"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-source-evidence-sidecar"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_source_evidence_sidecar"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-source-evidence-sidecar-strict"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_source_evidence_sidecar_strict"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-source-evidence-review-queue"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_source_evidence_review_queue"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-rhea-lookup-manifest"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_rhea_lookup_manifest"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-rhea-lookup-resolution"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_rhea_lookup_resolution"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-rhea-resolution-consumption"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_rhea_resolution_consumption"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-rhea-unresolved-official-source"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_rhea_unresolved_official_source"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-reviewer-decision-matrix"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_reviewer_decision_matrix"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-feature-readiness"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_feature_readiness"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-refresh-blocker"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_refresh_blocker"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-train-cal-feature-sidecar"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_train_cal_feature_sidecar"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-train-cal-coverage-gap"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_train_cal_coverage_gap"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-train-cal-feature-guardrail"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_train_cal_feature_guardrail"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-calibration-review-packet"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_calibration_review_packet"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-pending-rewrite-blocker"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_pending_rewrite_blocker"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-no-template-rerun"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_no_template_rerun"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-calibration-gap"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_calibration_gap"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-calibration-extraction-work-package"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_calibration_extraction_work_package"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-calibration-extraction-work-package-strict"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_calibration_extraction_work_package_strict"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-calibration-approved-source-evidence-sidecar"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_calibration_approved_source_evidence_sidecar"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-calibration-approved-source-evidence-sidecar-strict"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_calibration_approved_source_evidence_sidecar_strict"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-source-evidence-sidecar"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_source_evidence_sidecar"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-train-cal-feature-sidecar"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_train_cal_feature_sidecar"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-train-cal-feature-guardrail"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_train_cal_feature_guardrail"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-no-template-rerun"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_no_template_rerun"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-operating-point-contract"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_operating_point_contract"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-calibration-error-analysis"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_calibration_error_analysis"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-retained-oos-feature-target"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_retained_oos_feature_target"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-expanded-train-cal-feature-sidecar"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_expanded_train_cal_feature_sidecar"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-expanded-train-cal-feature-guardrail"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_expanded_train_cal_feature_guardrail"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-expanded-no-template-rerun"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_expanded_no_template_rerun"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-expanded-calibration-comparison"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_expanded_calibration_comparison"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-expanded-family-ablation"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_expanded_family_ablation"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-expanded-token-ablation"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_expanded_token_ablation"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-train-cal-feature-sidecar"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_train_cal_feature_sidecar"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-train-cal-feature-guardrail"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_train_cal_feature_guardrail"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-no-template-rerun"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_no_template_rerun"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-operating-point-contract"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_operating_point_contract"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-calibration-error-analysis"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_calibration_error_analysis"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-heldout-safe-"
                    "application-preflight"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_heldout_safe_application_preflight"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-token-ablation"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_token_ablation"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-train-cal-"
                    "feature-sidecar"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_train_cal_feature_sidecar"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-train-cal-"
                    "feature-guardrail"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_train_cal_feature_guardrail"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-no-template-rerun"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_no_template_rerun"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-operating-point-"
                    "contract"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_operating_point_contract"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-calibration-error-"
                    "analysis"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_calibration_error_analysis"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-heldout-safe-"
                    "surface-plan"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_heldout_safe_surface_plan"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "application-surface"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_application_surface"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "partial-surface-policy-gate"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_partial_surface_policy_gate"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "partial-surface-operating-contract-preflight"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_partial_surface_operating_contract_preflight"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "event-linker-blocker"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_event_linker_blocker"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "residue-count-fallback-contract"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_residue_count_fallback_contract"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "event-axis-linker-schema"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_schema"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "event-axis-linker-review-packet"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_review_packet"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "event-axis-linker-signoff-finalization"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_signoff_finalization"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "event-axis-linker-materialization-gate"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_materialization_gate"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "locator-action-queue"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_locator_action_queue"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "coordinate-anchor-candidates"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_anchor_candidates"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "coordinate-anchor-candidate-strict"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_anchor_candidate_strict"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "coordinate-anchor-review-queue"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_anchor_review_queue"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "coordinate-anchor-manual-review-packet"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_anchor_manual_review_packet"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "coordinate-anchor-priority1-review-worksheet"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_anchor_priority1_review_worksheet"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "coordinate-anchor-priority1-rewrite-preflight"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_coordinate_anchor_priority1_rewrite_preflight"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "locator-rewrite-approval-packet"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_approval_packet"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "locator-rewrite-materialization-gate"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "pre-threshold-readiness"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_readiness"
                ),
            ),
            (
                (
                    "build-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "train-cal-projection-readout"
                ),
                (
                    "cmd_build_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_train_cal_projection_readout"
                ),
            ),
            (
                (
                    "audit-mechanism-feature-row-specific-bond-change-"
                    "p0-oos-augmented-best-token-followup-pair-source-free-"
                    "locator-input"
                ),
                (
                    "cmd_audit_mechanism_feature_row_specific_bond_change_"
                    "p0_oos_augmented_best_token_followup_pair_source_free_locator_input"
                ),
            ),
            (
                "build-mechanism-feature-embedding-pilot",
                "cmd_build_mechanism_feature_embedding_pilot",
            ),
            (
                "build-mechanism-feature-embedding-heldout-readout",
                "cmd_build_mechanism_feature_embedding_heldout_readout",
            ),
            (
                "build-family-panel-high-value-glycyl-radical-readiness-packet",
                "cmd_build_family_panel_high_value_glycyl_radical_readiness_packet",
            ),
            (
                (
                    "build-fold-augmented-family-panel-expert-import-"
                    "decision-packet"
                ),
                (
                    "cmd_build_fold_augmented_family_panel_expert_import_"
                    "decision_packet"
                ),
            ),
            (
                (
                    "build-fold-augmented-family-panel-acceptance-"
                    "scenario-plan"
                ),
                (
                    "cmd_build_fold_augmented_family_panel_acceptance_"
                    "scenario_plan"
                ),
            ),
            (
                (
                    "apply-fold-augmented-family-panel-expert-import-"
                    "decision"
                ),
                (
                    "cmd_apply_fold_augmented_family_panel_expert_import_"
                    "decision"
                ),
            ),
            (
                (
                    "build-fold-augmented-family-panel-accepted-import-"
                    "preview"
                ),
                (
                    "cmd_build_fold_augmented_family_panel_accepted_import_"
                    "preview"
                ),
            ),
            (
                (
                    "build-fold-augmented-family-panel-label-factory-gate-"
                    "readiness"
                ),
                (
                    "cmd_build_fold_augmented_family_panel_label_factory_"
                    "gate_readiness"
                ),
            ),
            (
                "build-family-label-admission-pipeline",
                "cmd_build_family_label_admission_pipeline",
            ),
            (
                "build-active-lever-reviewer-decision-queue",
                "cmd_build_active_lever_reviewer_decision_queue",
            ),
            (
                "build-active-lever-mechanical-actionability-audit",
                "cmd_build_active_lever_mechanical_actionability_audit",
            ),
            (
                "build-active-lever-priority-decision-templates",
                "cmd_build_active_lever_priority_decision_templates",
            ),
            (
                "build-active-lever-source-decision-intake-preflight",
                "cmd_build_active_lever_source_decision_intake_preflight",
            ),
            (
                "build-active-lever-decision-application-contract-audit",
                (
                    "cmd_build_active_lever_decision_application_contract_"
                    "audit"
                ),
            ),
            (
                "build-family-panel-source-free-locator-human-decision-matrix",
                "cmd_build_family_panel_source_free_locator_human_decision_matrix",
            ),
            (
                (
                    "build-family-panel-source-free-locator-matching-"
                    "coordinate-scout-mh065-mh072"
                ),
                (
                    "cmd_build_family_panel_source_free_locator_matching_"
                    "coordinate_scout_mh065_mh072"
                ),
            ),
            (
                (
                    "build-family-panel-source-free-locator-glycoside-"
                    "substrate-coordinate-scout"
                ),
                (
                    "cmd_build_family_panel_source_free_locator_glycoside_"
                    "substrate_coordinate_scout"
                ),
            ),
            (
                (
                    "build-family-panel-source-free-locator-q59490-"
                    "alternate-source-cache-scout"
                ),
                (
                    "cmd_build_family_panel_source_free_locator_q59490_"
                    "alternate_source_cache_scout"
                ),
            ),
            (
                "audit-predicted-atlas-vs-fold-novelty-operating-grid-delta",
                "cmd_audit_predicted_atlas_vs_fold_novelty_operating_grid_delta",
            ),
            (
                "audit-predicted-structure-fold-confounded-operating-point-readiness",
                (
                    "cmd_audit_predicted_structure_fold_confounded_"
                    "operating_point_readiness"
                ),
            ),
            (
                (
                    "build-fold-augmented-source-feature-active-site-"
                    "sidecar-review-gate"
                ),
                (
                    "cmd_build_fold_augmented_source_feature_active_site_"
                    "sidecar_review_gate"
                ),
            ),
            (
                (
                    "build-fold-augmented-non-residue-interaction-sidecar-"
                    "policy-preflight"
                ),
                (
                    "cmd_build_fold_augmented_non_residue_interaction_"
                    "sidecar_policy_preflight"
                ),
            ),
            (
                (
                    "build-fold-augmented-p23007-alternate-accession-"
                    "policy-gate"
                ),
                (
                    "cmd_build_fold_augmented_p23007_alternate_accession_"
                    "policy_gate"
                ),
            ),
            (
                (
                    "build-fold-augmented-blocker-human-decision-"
                    "application"
                ),
                (
                    "cmd_build_fold_augmented_blocker_human_decision_"
                    "application"
                ),
            ),
            (
                (
                    "build-fold-augmented-approved-source-feature-active-site-"
                    "sidecar-materialization"
                ),
                (
                    "cmd_build_fold_augmented_approved_source_feature_active_site_"
                    "sidecar_materialization"
                ),
            ),
            (
                (
                    "build-fold-augmented-p00889-ortholog-coordinate-fetch-"
                    "manifest"
                ),
                (
                    "cmd_build_fold_augmented_p00889_ortholog_coordinate_"
                    "fetch_manifest"
                ),
            ),
            (
                "build-fold-augmented-fixed-threshold-rerun-readiness",
                "cmd_build_fold_augmented_fixed_threshold_rerun_readiness",
            ),
            (
                "build-fold-augmented-fixed-threshold-combined-rerun-readout",
                "cmd_build_fold_augmented_fixed_threshold_combined_rerun_readout",
            ),
            (
                (
                    "build-fold-augmented-fixed-threshold-combined-rerun-"
                    "calibration-impact"
                ),
                (
                    "cmd_build_fold_augmented_fixed_threshold_combined_rerun_"
                    "calibration_impact"
                ),
            ),
            (
                (
                    "build-fold-augmented-expanded-train-cal-oos-negative-"
                    "surface"
                ),
                (
                    "cmd_build_fold_augmented_expanded_train_cal_oos_negative_"
                    "surface"
                ),
            ),
            (
                "build-fold-augmented-post-rerun-deployment-closure-status",
                "cmd_build_fold_augmented_post_rerun_deployment_closure_status",
            ),
            (
                (
                    "audit-fold-augmented-post-rerun-confounded-deployment-"
                    "closure"
                ),
                (
                    "cmd_audit_fold_augmented_post_rerun_confounded_"
                    "deployment_closure"
                ),
            ),
            (
                "audit-fold-augmented-confounded-proxy-operating-point",
                (
                    "cmd_audit_fold_augmented_confounded_proxy_operating_"
                    "point"
                ),
            ),
            (
                "build-fold-augmented-confounded-proxy-gap-targets",
                "cmd_build_fold_augmented_confounded_proxy_gap_targets",
            ),
            (
                "build-fold-augmented-confounded-proxy-threshold-stress",
                "cmd_build_fold_augmented_confounded_proxy_threshold_stress",
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-evidence-extension-"
                    "plan"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_evidence_"
                    "extension_plan"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-acquisition-"
                    "queue"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_acquisition_"
                    "queue"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-train-cal-"
                    "candidate-pool"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_train_cal_"
                    "candidate_pool"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-high-cofactor-"
                    "candidate-near-miss-triage"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_high_cofactor_"
                    "candidate_near_miss_triage"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-high-cofactor-"
                    "acquisition-blocker-packet"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_high_cofactor_"
                    "acquisition_blocker_packet"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-high-cofactor-"
                    "acquisition-dispatch-packet"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_high_cofactor_"
                    "acquisition_dispatch_packet"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-train-cal-"
                    "scoring-tranche-plan"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_train_cal_"
                    "scoring_tranche_plan"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-train-cal-"
                    "background-axis-blocker"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_train_cal_"
                    "background_axis_blocker"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-train-cal-"
                    "background-axis-scout"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_train_cal_"
                    "background_axis_scout"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-train-cal-"
                    "unsupported-geometry-repair-queue"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_train_cal_"
                    "unsupported_geometry_repair_queue"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-train-cal-"
                    "unsupported-geometry-coordinate-acquisition-manifest"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_train_cal_"
                    "unsupported_geometry_coordinate_acquisition_manifest"
                ),
            ),
            (
                (
                    "scan-fold-augmented-confounded-proxy-train-cal-"
                    "unsupported-geometry-coordinate-loci"
                ),
                (
                    "cmd_scan_fold_augmented_confounded_proxy_train_cal_"
                    "unsupported_geometry_coordinate_loci"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-train-cal-"
                    "protein-only-proxy-design-preflight"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_train_cal_"
                    "protein_only_proxy_design_preflight"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-train-cal-"
                    "protein-only-fold-topology-residual-contract"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_train_cal_"
                    "protein_only_fold_topology_residual_contract"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-train-cal-"
                    "scoring-input-manifest"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_train_cal_"
                    "scoring_input_manifest"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-train-cal-"
                    "scored-extension"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_train_cal_"
                    "scored_extension"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-extended-train-"
                    "cal-oos-surface"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_extended_"
                    "train_cal_oos_surface"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-deployment-"
                    "validity-blocker-packet"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_deployment_"
                    "validity_blocker_packet"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-high-cofactor-"
                    "probe-contract"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_high_"
                    "cofactor_probe_contract"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-same-family-"
                    "structural-acquisition-contract"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_same_family_"
                    "structural_acquisition_contract"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-same-family-"
                    "structural-acquisition-blocker-packet"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_same_family_"
                    "structural_acquisition_blocker_packet"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-same-family-"
                    "structural-acquisition-dispatch-packet"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_same_family_"
                    "structural_acquisition_dispatch_packet"
                ),
            ),
            (
                (
                    "build-fold-augmented-lever3-blocker-packet-"
                    "guardrail-audit"
                ),
                (
                    "cmd_build_fold_augmented_lever3_blocker_packet_"
                    "guardrail_audit"
                ),
            ),
            (
                (
                    "build-fold-augmented-p10746-deployment-caveat-decision-"
                    "packet"
                ),
                (
                    "cmd_build_fold_augmented_p10746_deployment_caveat_"
                    "decision_packet"
                ),
            ),
            (
                (
                    "build-fold-augmented-p10746-prior-human-decision-"
                    "reviewed-stub"
                ),
                (
                    "cmd_build_fold_augmented_p10746_prior_human_decision_"
                    "reviewed_stub"
                ),
            ),
            (
                (
                    "apply-fold-augmented-p10746-deployment-caveat-decision"
                ),
                (
                    "cmd_apply_fold_augmented_p10746_deployment_caveat_"
                    "decision"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-p10746-decision-"
                    "impact"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_p10746_"
                    "decision_impact"
                ),
            ),
            (
                (
                    "build-fold-augmented-q43088-geometry-locator-blocker-"
                    "packet"
                ),
                (
                    "cmd_build_fold_augmented_q43088_geometry_locator_"
                    "blocker_packet"
                ),
            ),
            (
                (
                    "build-fold-augmented-q43088-source-free-locator-"
                    "approval-contract"
                ),
                (
                    "cmd_build_fold_augmented_q43088_source_free_locator_"
                    "approval_contract"
                ),
            ),
            (
                (
                    "build-fold-augmented-q43088-source-free-locator-"
                    "candidate-scout"
                ),
                (
                    "cmd_build_fold_augmented_q43088_source_free_locator_"
                    "candidate_scout"
                ),
            ),
            (
                (
                    "build-fold-augmented-q43088-locator-review-priority-"
                    "packet"
                ),
                (
                    "cmd_build_fold_augmented_q43088_locator_review_"
                    "priority_packet"
                ),
            ),
            (
                (
                    "build-fold-augmented-q43088-locator-approval-packet"
                ),
                (
                    "cmd_build_fold_augmented_q43088_locator_approval_"
                    "packet"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-current-evidence-"
                    "after-q43088-locator-approval"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_current_"
                    "evidence_after_q43088_locator_approval"
                ),
            ),
            (
                (
                    "build-fold-augmented-p07658-full-length-prediction-"
                    "request-manifest"
                ),
                (
                    "cmd_build_fold_augmented_p07658_full_length_prediction_"
                    "request_manifest"
                ),
            ),
            (
                (
                    "build-fold-augmented-p07658-prediction-acceptance-"
                    "preflight"
                ),
                (
                    "cmd_build_fold_augmented_p07658_prediction_acceptance_"
                    "preflight"
                ),
            ),
            (
                "build-fold-augmented-p07658-prediction-dispatch-packet",
                "cmd_build_fold_augmented_p07658_prediction_dispatch_packet",
            ),
            (
                (
                    "build-fold-augmented-lever3-minimum-next-experiment-"
                    "queue"
                ),
                (
                    "cmd_build_fold_augmented_lever3_minimum_next_"
                    "experiment_queue"
                ),
            ),
            (
                "build-fold-augmented-lever3-dispatch-readiness-summary",
                "cmd_build_fold_augmented_lever3_dispatch_readiness_summary",
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-residual-queue-"
                    "after-p10746-q43088"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_residual_queue_"
                    "after_p10746_q43088"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-alternate-"
                    "structure-source-contract"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_alternate_"
                    "structure_source_contract"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-deployment-input-"
                    "preflight"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_deployment_"
                    "input_preflight"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-repo-wide-"
                    "coordinate-sanity-scan"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_repo_wide_"
                    "coordinate_sanity_scan"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-swissmodel-"
                    "coordinate-staging-manifest"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_swissmodel_"
                    "coordinate_staging_manifest"
                ),
            ),
            (
                (
                    "build-fold-augmented-confounded-proxy-current-evidence-"
                    "blocker-after-input-preflight"
                ),
                (
                    "cmd_build_fold_augmented_confounded_proxy_current_"
                    "evidence_blocker_after_input_preflight"
                ),
            ),
            (
                (
                    "build-fold-augmented-post-decision-deployment-closure-"
                    "status"
                ),
                (
                    "cmd_build_fold_augmented_post_decision_deployment_"
                    "closure_status"
                ),
            ),
            (
                "audit-fold-augmented-confounded-deployment-closure",
                "cmd_audit_fold_augmented_confounded_deployment_closure",
            ),
            (
                "audit-fold-augmented-fold-only-deployment-contract",
                "cmd_audit_fold_augmented_fold_only_deployment_contract",
            ),
        ]
        for command_name, function_name in cases:
            with self.subTest(command_name=command_name):
                args = parser.parse_args([command_name])
                self.assertEqual(args.func.__name__, function_name)

    def test_build_sequence_cluster_proxy_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            graph = root / "graph.json"
            out = root / "clusters.json"
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"builder": "test"},
                        "nodes": [
                            {"id": "m_csa:1", "type": "m_csa_entry", "name": "first"},
                            {"id": "m_csa:2", "type": "m_csa_entry", "name": "second"},
                        ],
                        "edges": [
                            {
                                "source": "m_csa:1",
                                "target": "uniprot:P12345",
                                "predicate": "has_reference_protein",
                            },
                            {
                                "source": "m_csa:2",
                                "target": "uniprot:P12345",
                                "predicate": "has_reference_protein",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-sequence-cluster-proxy",
                    "--graph",
                    str(graph),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            clusters = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(clusters["metadata"]["duplicate_cluster_count"], 1)
            self.assertEqual(clusters["duplicate_clusters"][0]["entry_count"], 2)

    def test_external_pilot_priority_cli_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            matrix = root / "matrix.json"
            priority = root / "priority.json"
            review_export = root / "review_export.json"
            matrix.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_transfer_blocker_matrix"
                        },
                        "rows": [
                            {
                                "accession": "PGOOD",
                                "blockers": [
                                    "complete_near_duplicate_search_required"
                                ],
                                "lane_id": "external_source:lane_a",
                                "representation_backend": {
                                    "sample_backend_status": (
                                        "learned_representation_sample_complete"
                                    ),
                                    "sample_near_duplicate_alert": False,
                                },
                                "sequence_search": {
                                    "alignment_status": (
                                        "alignment_no_near_duplicate_signal"
                                    )
                                },
                            },
                            {
                                "accession": "PHOLD",
                                "blockers": ["exact_sequence_holdout"],
                                "lane_id": "external_source:lane_b",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-pilot-candidate-priority",
                    "--transfer-blocker-matrix",
                    str(matrix),
                    "--out",
                    str(priority),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-pilot-review-decision-export",
                    "--pilot-candidate-priority",
                    str(priority),
                    "--out",
                    str(review_export),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            priority_payload = json.loads(priority.read_text(encoding="utf-8"))
            review_payload = json.loads(review_export.read_text(encoding="utf-8"))
            self.assertEqual(
                priority_payload["metadata"]["selected_accessions"], ["PGOOD"]
            )
            self.assertFalse(
                priority_payload["metadata"]["leakage_policy"][
                    "text_or_label_fields_used_for_priority"
                ]
            )
            self.assertEqual(review_payload["metadata"]["candidate_count"], 1)
            self.assertEqual(
                review_payload["metadata"]["decision_status_counts"],
                {"no_decision": 1},
            )

    def test_external_pilot_success_criteria_cli_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            priority = root / "priority.json"
            review = root / "review.json"
            decisions = root / "decisions.json"
            readiness = root / "readiness.json"
            gate = root / "gate.json"
            out = root / "success.json"
            priority.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_pilot_candidate_priority"
                        },
                        "rows": [
                            {
                                "accession": "P12345",
                                "lane_id": "external_source:lane_a",
                                "pilot_selection_status": "selected_for_review_pilot",
                                "countable_label_candidate": False,
                                "ready_for_label_import": False,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_pilot_review_decision_export"
                        },
                        "review_items": [
                            {
                                "accession": "P12345",
                                "decision": {
                                    "decision_status": "no_decision",
                                    "ready_for_label_import": False,
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            decisions.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "external_source_pilot_active_site_evidence_decisions"
                            )
                        },
                        "rows": [
                            {
                                "accession": "P12345",
                                "rank": 1,
                                "active_site_evidence_source_category": (
                                    "explicit_active_site_source_present"
                                ),
                                "broader_duplicate_screening_status": (
                                    "broader_duplicate_screening_required"
                                ),
                                "representation_control_status": (
                                    "pilot_representation_control_review_only"
                                ),
                                "countable_label_candidate": False,
                                "ready_for_label_import": False,
                                "import_readiness_blockers": [
                                    "broader_duplicate_screening_required",
                                    "external_review_decision_artifact_not_built",
                                    "full_label_factory_gate_not_run",
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            readiness.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_import_readiness_audit"
                        },
                        "rows": [],
                    }
                ),
                encoding="utf-8",
            )
            gate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_transfer_gate_check",
                            "gate_count": 68,
                            "passed_gate_count": 68,
                            "ready_for_label_import": False,
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-pilot-success-criteria",
                    "--pilot-candidate-priority",
                    str(priority),
                    "--pilot-review-decision-export",
                    str(review),
                    "--pilot-active-site-evidence-decisions",
                    str(decisions),
                    "--external-import-readiness-audit",
                    str(readiness),
                    "--external-transfer-gate",
                    str(gate),
                    "--max-rows",
                    "1",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["metadata"]["method"],
                "external_source_pilot_success_criteria",
            )
            self.assertEqual(payload["metadata"]["pilot_status"], "needs_more_work")
            self.assertEqual(payload["metadata"]["terminal_decision_count"], 0)
            self.assertEqual(payload["metadata"]["import_ready_row_count"], 0)

    def test_build_geometry_features_reuse_existing_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            graph = root / "graph.json"
            reuse = root / "reuse.json"
            out = root / "geometry.json"
            reused_row = {
                "entry_id": "m_csa:1",
                "status": "ok",
                "pairwise_distances_angstrom": [{"distance": 1.0}],
                "ligand_context": {
                    "proximal_ligands": [],
                    "cofactor_families": [],
                    "structure_ligands": [],
                    "structure_cofactor_families": [],
                },
                "pocket_context": {"nearby_residue_count": 0},
            }
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"builder": "test"},
                        "nodes": [
                            {
                                "id": "m_csa:1:residue:1",
                                "type": "catalytic_residue",
                                "roles": ["acid"],
                                "structure_positions": [
                                    {
                                        "pdb_id": "1ABC",
                                        "chain_name": "A",
                                        "code": "ASP",
                                        "resid": 7,
                                    }
                                ],
                            }
                        ],
                        "edges": [],
                    }
                ),
                encoding="utf-8",
            )
            reuse.write_text(json.dumps({"entries": [reused_row]}), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-geometry-features",
                    "--graph",
                    str(graph),
                    "--max-entries",
                    "1",
                    "--reuse-existing",
                    str(reuse),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            geometry = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(geometry["metadata"]["reused_entry_count"], 1)
            self.assertEqual(geometry["entries"], [reused_row])

    def test_filter_countable_labels_requires_explicit_lossy_filter(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            labels = Path(tmpdir) / "labels.json"
            out = Path(tmpdir) / "countable.json"
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "m_csa:1",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "confidence": "medium",
                            "evidence_score": 0.65,
                            "evidence": {"sources": ["test"]},
                            "rationale": "This countable baseline label is long enough.",
                        },
                        {
                            "entry_id": "m_csa:2",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "tier": "bronze",
                            "review_status": "needs_expert_review",
                            "confidence": "medium",
                            "evidence_score": 0.55,
                            "evidence": {"sources": ["test"]},
                            "rationale": "This pending review label is long enough.",
                        },
                    ]
                ),
                encoding="utf-8",
            )
            blocked = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "filter-countable-labels",
                    "--labels",
                    str(labels),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                capture_output=True,
                text=True,
            )
            self.assertEqual(blocked.returncode, 2)
            self.assertIn("Refusing to filter", blocked.stdout)
            self.assertFalse(out.exists())
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "filter-countable-labels",
                    "--labels",
                    str(labels),
                    "--out",
                    str(out),
                    "--allow-pending-review",
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(len(json.loads(out.read_text(encoding="utf-8"))), 1)

    def test_summarize_label_factory_batches_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            acceptance = root / "v3_label_batch_acceptance_check_650.json"
            gate = root / "v3_label_factory_gate_check_650.json"
            queue = root / "v3_active_learning_review_queue_650.json"
            scaling_audit = root / "v3_label_scaling_quality_audit_650.json"
            out = root / "summary.json"
            acceptance.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "accepted_for_counting": True,
                            "baseline_label_count": 599,
                            "countable_label_count": 618,
                            "accepted_new_label_count": 19,
                            "pending_review_count": 37,
                            "hard_negative_count": 0,
                            "near_miss_count": 0,
                            "out_of_scope_false_non_abstentions": 0,
                            "actionable_in_scope_failure_count": 0,
                            "factory_gate_ready": True,
                        },
                        "blockers": [],
                    }
                ),
                encoding="utf-8",
            )
            gate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "automation_ready_for_next_label_batch": True,
                            "gate_count": 10,
                            "passed_gate_count": 10,
                        }
                    }
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "total_unlabeled_candidate_count": 32,
                            "unlabeled_omitted_by_max_rows": 0,
                            "all_unlabeled_rows_retained": True,
                        }
                    }
                ),
                encoding="utf-8",
            )
            scaling_audit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "audit_recommendation": "promotion_quality_audit_clean",
                            "accepted_new_debt_count": 0,
                            "unclassified_new_review_debt_entry_ids": [],
                            "omitted_underrepresented_queue_entry_ids": [],
                            "issue_class_counts": {},
                        },
                        "blockers": [],
                        "review_warnings": [
                            "sequence_cluster_artifact_missing_for_near_duplicate_audit"
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "summarize-label-factory-batches",
                    "--acceptance",
                    str(acceptance),
                    "--gate",
                    str(gate),
                    "--active-learning-queue",
                    str(queue),
                    "--scaling-quality-audit",
                    str(scaling_audit),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(summary["metadata"]["latest_batch"], "650")
            self.assertTrue(summary["metadata"]["all_active_queues_retain_unlabeled_candidates"])
            self.assertTrue(summary["metadata"]["latest_scaling_quality_audit_present"])
            self.assertEqual(
                summary["metadata"]["latest_scaling_quality_review_warnings"],
                ["sequence_cluster_artifact_missing_for_near_duplicate_audit"],
            )
            self.assertTrue(summary["rows"][0]["scaling_quality_ready"])

    def test_resolve_local_evidence_repair_lanes_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            plan = root / "plan.json"
            gap = root / "gap.json"
            local_export = root / "local_export.json"
            mismatch_export = root / "mismatch_export.json"
            mismatch_batch = root / "mismatch_batch.json"
            out = root / "resolution.json"
            plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_local_evidence_repair_plan",
                            "planned_entry_count": 2,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "entry_name": "kinase lane",
                                "repair_lane": "expert_reaction_substrate_review",
                                "recommended_next_action": (
                                    "route_to_reaction_substrate_expert_review"
                                ),
                                "local_evidence_gap_classes": [
                                    "reaction_substrate_mismatch_review_required"
                                ],
                                "non_countable_blockers": [
                                    "reaction_substrate_mismatch_review_required"
                                ],
                            },
                            {
                                "entry_id": "m_csa:2",
                                "entry_name": "mapping lane",
                                "repair_lane": (
                                    "source_explicit_alternate_structure_residue_positions"
                                ),
                                "recommended_next_action": (
                                    "source_explicit_alternate_structure_residue_positions"
                                ),
                                "local_evidence_gap_classes": [
                                    "alternate_structures_lack_explicit_residue_positions"
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            gap.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "expert_label_decision_local_evidence_gap_audit"
                            )
                        },
                        "rows": [],
                    }
                ),
                encoding="utf-8",
            )
            local_export.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "expert_label_decision_local_evidence_review_export"
                            )
                        },
                        "review_items": [
                            {
                                "entry_id": "m_csa:1",
                                "decision": {
                                    "action": "no_decision",
                                    "local_evidence_resolution": "needs_more_evidence",
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            mismatch_export.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "reaction_substrate_mismatch_review_export",
                            "exported_entry_ids": ["m_csa:1"],
                        },
                        "review_items": [{"entry_id": "m_csa:1"}],
                    }
                ),
                encoding="utf-8",
            )
            mismatch_batch.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "provisional_label_review_decision_batch"
                        },
                        "review_items": [
                            {
                                "entry_id": "m_csa:1",
                                "decision": {
                                    "action": "accept_label",
                                    "label_type": "out_of_scope",
                                    "review_status": "expert_reviewed",
                                    "reviewer": "tester",
                                    "reaction_substrate_resolution": (
                                        "confirm_current_label_or_out_of_scope"
                                    ),
                                    "rationale": "Reviewed as a kinase boundary lane.",
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "resolve-expert-label-decision-local-evidence-repair-lanes",
                    "--expert-label-decision-local-evidence-repair-plan",
                    str(plan),
                    "--expert-label-decision-local-evidence-gap-audit",
                    str(gap),
                    "--expert-label-decision-local-evidence-review-export",
                    str(local_export),
                    "--reaction-substrate-mismatch-review-export",
                    str(mismatch_export),
                    "--reaction-substrate-mismatch-decision-batch",
                    str(mismatch_batch),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            resolution = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(resolution["metadata"]["resolution_ready"])
            self.assertEqual(resolution["metadata"]["resolved_entry_ids"], ["m_csa:1"])
            self.assertEqual(
                resolution["metadata"]["remaining_open_entry_ids"], ["m_csa:2"]
            )
            self.assertEqual(
                resolution["metadata"]["countable_label_candidate_count"], 0
            )

    def test_build_explicit_alternate_residue_position_requests_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            plan = root / "plan.json"
            remediation = root / "remediation.json"
            graph = root / "graph.json"
            out = root / "requests.json"
            plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_local_evidence_repair_plan"
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:7",
                                "entry_name": "alternate residue lane",
                                "repair_lane": (
                                    "source_explicit_alternate_structure_residue_positions"
                                ),
                                "recommended_next_action": (
                                    "source_explicit_alternate_structure_residue_positions"
                                ),
                                "selected_pdb_id": "1AAA",
                                "selected_pdb_residue_position_count": 1,
                                "alternate_pdb_count": 2,
                                "alternate_pdb_with_residue_positions_count": 0,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            remediation.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_remediation"},
                        "rows": [
                            {
                                "entry_id": "m_csa:7",
                                "candidate_pdb_structure_ids": [
                                    "1AAA",
                                    "2BBB",
                                    "3CCC",
                                ],
                                "alternate_pdb_ids": ["2BBB", "3CCC"],
                                "expected_cofactor_families": ["metal_ion"],
                                "gap_reasons": ["review_marked_needs_more_evidence"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "nodes": [
                            {
                                "id": "m_csa:7",
                                "type": "m_csa_entry",
                                "reference_uniprot_id": "P00007",
                            }
                        ],
                        "edges": [
                            {
                                "source": "m_csa:7",
                                "target": "ec:1.2.3.4",
                                "predicate": "has_ec",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-explicit-alternate-residue-position-requests",
                    "--expert-label-decision-local-evidence-repair-plan",
                    str(plan),
                    "--review-debt-remediation",
                    str(remediation),
                    "--graph",
                    str(graph),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            requests = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(requests["metadata"]["sourcing_request_ready"])
            self.assertEqual(requests["metadata"]["request_entry_ids"], ["m_csa:7"])
            self.assertEqual(
                requests["metadata"]["candidate_alternate_structure_count"], 2
            )
            self.assertEqual(requests["rows"][0]["reference_uniprot_id"], "P00007")
            self.assertEqual(requests["rows"][0]["ec_ids"], ["ec:1.2.3.4"])
            self.assertFalse(requests["rows"][0]["countable_label_candidate"])

    def test_summarize_review_debt_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            gaps = root / "v3_review_evidence_gaps_650.json"
            queue = root / "v3_active_learning_review_queue_650.json"
            baseline = root / "baseline_review_debt.json"
            out = root / "review_debt.json"
            gaps.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_evidence_gap_analysis"},
                        "rows": [
                            {
                                "entry_id": "m_csa:650",
                                "entry_name": "phospholipase A1",
                                "decision_action": "mark_needs_more_evidence",
                                "coverage_status": "expected_structure_only",
                                "gap_reasons": ["counterevidence_present"],
                                "target_fingerprint_id": "ser_his_acid_hydrolase",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps({"rows": [{"entry_id": "m_csa:650", "rank": 1, "review_score": 8.0}]}),
                encoding="utf-8",
            )
            baseline.write_text(json.dumps({"rows": []}), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "summarize-review-debt",
                    "--review-evidence-gaps",
                    str(gaps),
                    "--active-learning-queue",
                    str(queue),
                    "--baseline-review-debt",
                    str(baseline),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(summary["metadata"]["review_debt_count"], 1)
            self.assertEqual(summary["metadata"]["new_review_debt_count"], 1)
            self.assertEqual(summary["metadata"]["new_review_debt_entry_ids"], ["m_csa:650"])
            self.assertEqual(
                summary["metadata"]["recommended_next_action_counts_by_debt_status"]["new"],
                {"verify_local_cofactor_or_active_site_mapping": 1},
            )
            self.assertEqual(summary["rows"][0]["entry_id"], "m_csa:650")

    def test_analyze_review_debt_remediation_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            debt = root / "review_debt.json"
            gaps = root / "review_gaps.json"
            graph = root / "graph.json"
            geometry = root / "geometry.json"
            out = root / "remediation.json"
            debt.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_summary",
                            "review_debt_entry_ids": ["m_csa:651"],
                            "new_review_debt_entry_ids": ["m_csa:651"],
                            "carried_review_debt_entry_ids": [],
                        },
                        "rows": [],
                    }
                ),
                encoding="utf-8",
            )
            gaps.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_evidence_gap_analysis"},
                        "rows": [
                            {
                                "entry_id": "m_csa:651",
                                "entry_name": "flavin gap",
                                "decision_action": "mark_needs_more_evidence",
                                "coverage_status": "expected_absent_from_structure",
                                "gap_reasons": ["expected_cofactor_absent_from_structure"],
                                "expected_cofactor_families": ["flavin"],
                                "local_cofactor_families": [],
                                "structure_cofactor_families": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "nodes": [
                            {
                                "id": "pdb:1AAA",
                                "type": "structure",
                                "structure_source": "pdb",
                                "structure_id": "1AAA",
                            },
                            {
                                "id": "pdb:2BBB",
                                "type": "structure",
                                "structure_source": "pdb",
                                "structure_id": "2BBB",
                            },
                        ],
                        "edges": [
                            {
                                "source": "m_csa:651",
                                "target": "uniprot:P651",
                                "predicate": "has_reference_protein",
                            },
                            {
                                "source": "uniprot:P651",
                                "target": "pdb:1AAA",
                                "predicate": "has_structure",
                            },
                            {
                                "source": "uniprot:P651",
                                "target": "pdb:2BBB",
                                "predicate": "has_structure",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps({"entries": [{"entry_id": "m_csa:651", "pdb_id": "1AAA", "status": "ok"}]}),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-review-debt-remediation",
                    "--review-debt",
                    str(debt),
                    "--review-evidence-gaps",
                    str(gaps),
                    "--graph",
                    str(graph),
                    "--geometry",
                    str(geometry),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            plan = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(plan["metadata"]["requested_entry_count"], 1)
            self.assertEqual(plan["rows"][0]["entry_id"], "m_csa:651")
            self.assertEqual(plan["rows"][0]["alternate_pdb_ids"], ["2BBB"])

    def test_summarize_review_debt_remap_leads_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scan = root / "scan.json"
            remediation = root / "remediation.json"
            out = root / "remap_leads.json"
            scan.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_alternate_structure_scan"},
                        "rows": [
                            {
                                "entry_id": "m_csa:653",
                                "entry_name": "alternate local flavin gap",
                                "remediation_bucket": "alternate_pdb_ligand_scan",
                                "expected_cofactor_families": ["flavin"],
                                "structure_hits": [
                                    {
                                        "pdb_id": "2BBB",
                                        "ligand_codes": ["FAD"],
                                        "expected_family_hits": ["flavin"],
                                        "local_ligand_codes": ["FAD"],
                                        "local_cofactor_families": ["flavin"],
                                        "local_expected_family_hits": ["flavin"],
                                        "is_selected_structure": False,
                                        "residue_position_source": "selected_position_remap",
                                        "residue_position_remap_basis": "same_chain_residue_id",
                                        "usable_residue_position_count": 1,
                                        "remapped_residue_position_count": 1,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            remediation.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:653",
                                "debt_status": "carried",
                                "coverage_status": "expected_absent_from_structure",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "summarize-review-debt-remap-leads",
                    "--alternate-structure-scan",
                    str(scan),
                    "--remediation",
                    str(remediation),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(summary["metadata"]["lead_count"], 1)
            self.assertEqual(
                summary["metadata"]["local_expected_family_hit_from_remap_entry_ids"],
                ["m_csa:653"],
            )
            self.assertFalse(summary["rows"][0]["countable_label_candidate"])

    def test_audit_review_debt_remap_local_leads_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            remap_leads = root / "remap_leads.json"
            remediation = root / "remediation.json"
            out = root / "audit.json"
            remap_leads.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_remap_lead_summary"},
                        "rows": [
                            {
                                "entry_id": "m_csa:653",
                                "entry_name": "alternate local metal gap",
                                "lead_type": "local_expected_family_hit_from_remap",
                                "gap_reasons": [
                                    "counterevidence_present",
                                    "expected_cofactor_absent_from_structure",
                                ],
                                "expected_cofactor_families": ["metal_ion"],
                                "local_expected_family_hit_pdb_ids": ["2BBB"],
                                "local_expected_family_hit_from_remap_pdb_ids": [
                                    "2BBB"
                                ],
                                "local_expected_ligand_codes": ["ZN"],
                                "remap_basis_counts": {"same_chain_residue_id": 1},
                                "remapped_residue_position_structure_count": 1,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            remediation.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:653",
                                "selected_pdb_id": "1AAA",
                                "coverage_status": "expected_absent_from_structure",
                                "selected_active_site_has_expected_family": False,
                                "selected_structure_has_expected_family": False,
                                "alternate_pdb_with_residue_positions_count": 0,
                                "candidate_pdb_with_residue_positions_count": 1,
                                "counterevidence_reasons": [
                                    "role_inferred_metal_low_pocket_support"
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-review-debt-remap-local-leads",
                    "--remap-leads",
                    str(remap_leads),
                    "--remediation",
                    str(remediation),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(audit["metadata"]["audited_entry_count"], 1)
            self.assertEqual(
                audit["metadata"]["expert_family_boundary_review_entry_ids"],
                ["m_csa:653"],
            )
            self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
            self.assertTrue(audit["rows"][0]["strict_remap_guardrail_required"])

    def test_summarize_review_debt_structure_selection_candidates_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            remap_local_audit = root / "remap_local_audit.json"
            alternate_scan = root / "alternate_scan.json"
            out = root / "structure_selection.json"
            remap_local_audit.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_remap_local_lead_audit"},
                        "rows": [
                            {
                                "entry_id": "m_csa:654",
                                "entry_name": "clean remap lead",
                                "audit_decision": "local_structure_selection_rule_candidate",
                                "selected_pdb_id": "3AAA",
                                "selected_structure_gap_reasons": [
                                    "selected_structure_missing_expected_cofactor_family"
                                ],
                                "selected_active_site_has_expected_family": False,
                                "selected_structure_has_expected_family": False,
                                "expected_cofactor_families": ["metal_ion"],
                                "local_expected_ligand_codes": ["MG"],
                                "local_expected_family_hit_from_remap_pdb_ids": [
                                    "3CCC"
                                ],
                                "strict_remap_guardrail_required": True,
                                "alternate_pdb_with_explicit_residue_positions_count": 0,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate_scan.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_alternate_structure_scan"},
                        "rows": [
                            {
                                "entry_id": "m_csa:654",
                                "entry_name": "clean remap lead",
                                "structure_hits": [
                                    {
                                        "pdb_id": "3CCC",
                                        "residue_position_source": "selected_position_remap",
                                        "residue_position_remap_basis": "same_chain_residue_id",
                                        "usable_residue_position_count": 2,
                                        "remapped_residue_position_count": 2,
                                        "expected_family_hits": ["metal_ion"],
                                        "local_expected_family_hits": ["metal_ion"],
                                        "local_ligand_codes": ["BGC", "MG"],
                                        "ligand_codes": ["ANP", "BGC", "MG"],
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "summarize-review-debt-structure-selection-candidates",
                    "--remap-local-lead-audit",
                    str(remap_local_audit),
                    "--alternate-structure-scan",
                    str(alternate_scan),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(summary["metadata"]["candidate_entry_ids"], ["m_csa:654"])
            self.assertEqual(summary["metadata"]["countable_label_candidate_count"], 0)
            self.assertEqual(summary["rows"][0]["candidate_local_expected_ligand_codes"], ["MG"])

    def test_audit_reaction_substrate_mismatches_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            queue = root / "queue.json"
            out = root / "reaction_mismatch.json"
            queue.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:655",
                                "entry_name": "glucokinase-like lead",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "mechanism_text_snippets": [
                                    "Glucose attacks the gamma phosphorous of ATP."
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-reaction-substrate-mismatches",
                    "--active-learning-queue",
                    str(queue),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(audit["metadata"]["mismatch_entry_ids"], ["m_csa:655"])
            self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_build_reaction_substrate_mismatch_review_export_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            labels = root / "labels.json"
            reaction_audit = root / "reaction_mismatch.json"
            family_guardrails = root / "family_guardrails.json"
            out = root / "reaction_mismatch_review_export.json"
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "m_csa:655",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "confidence": "medium",
                            "rationale": "kinase boundary control kept outside the seed set",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "evidence_score": 0.65,
                            "evidence": {"sources": ["test"]},
                        }
                    ]
                ),
                encoding="utf-8",
            )
            reaction_audit.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "reaction_substrate_mismatch_audit"},
                        "rows": [
                            {
                                "entry_id": "m_csa:655",
                                "entry_name": "glucokinase-like lead",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "mismatch_reasons": ["kinase_name_with_hydrolase_top1"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            family_guardrails.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "family_propagation_guardrail_audit"},
                        "rows": [
                            {
                                "entry_id": "m_csa:655",
                                "entry_name": "glucokinase-like lead",
                                "label_state": "labeled",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "reaction_substrate_mismatch_reasons": [
                                    "kinase_name_with_hydrolase_top1"
                                ],
                            },
                            {
                                "entry_id": "m_csa:656",
                                "entry_name": "pending ribokinase",
                                "label_state": "unlabeled",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "reaction_substrate_mismatch_reasons": [
                                    "kinase_name_with_hydrolase_top1"
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-reaction-substrate-mismatch-review-export",
                    "--reaction-substrate-mismatch-audit",
                    str(reaction_audit),
                    "--family-propagation-guardrails",
                    str(family_guardrails),
                    "--labels",
                    str(labels),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            export = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(export["metadata"]["exported_count"], 2)
            self.assertTrue(export["metadata"]["all_family_guardrail_mismatches_exported"])
            self.assertEqual(
                export["metadata"]["recommended_path"],
                "expert_reaction_substrate_review_before_ontology_split",
            )

    def test_build_expert_label_decision_review_export_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            labels = root / "labels.json"
            queue = root / "queue.json"
            debt = root / "review_debt.json"
            mismatch_export = root / "mismatch_export.json"
            remediation = root / "remediation.json"
            structure_mapping = root / "structure_mapping.json"
            alternate_scan = root / "alternate_scan.json"
            out = root / "expert_label_decision_export.json"
            repair_out = root / "expert_label_decision_repair.json"
            guardrail_out = root / "expert_label_decision_repair_guardrail.json"
            local_gap_out = root / "expert_label_decision_local_gap.json"
            local_gap_export_out = root / "expert_label_decision_local_gap_export.json"
            local_gap_plan_out = root / "expert_label_decision_local_gap_plan.json"
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "m_csa:1",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "confidence": "medium",
                            "rationale": "Existing boundary control kept outside seed labels.",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "evidence_score": 0.65,
                            "evidence": {"sources": ["test"]},
                        }
                    ]
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "active_learning_label_review_queue"},
                        "rows": [
                            {
                                "rank": 1,
                                "entry_id": "m_csa:650",
                                "entry_name": "phospholipase A1",
                                "label_state": "unlabeled",
                                "recommended_action": "expert_label_decision_needed",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "top1_ontology_family": "hydrolysis",
                                "top1_score": 0.61,
                                "top2_fingerprint_id": "ser_his_acid_hydrolase",
                                "top2_score": 0.45,
                                "abstain_threshold": 0.4115,
                                "cofactor_evidence_level": "ligand_supported",
                                "readiness_blockers": [
                                    "fewer_than_three_resolved_residues"
                                ],
                                "counterevidence_reasons": [],
                                "reaction_substrate_mismatch_reasons": [],
                                "mechanism_text_snippets": [
                                    "Ser-His hydrolase text with no explicit metal catalysis."
                                ],
                            },
                            {
                                "rank": 2,
                                "entry_id": "m_csa:655",
                                "entry_name": "glucokinase",
                                "label_state": "unlabeled",
                                "recommended_action": "expert_label_decision_needed",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "top1_ontology_family": "hydrolysis",
                                "top1_score": 0.5,
                                "abstain_threshold": 0.4115,
                                "cofactor_evidence_level": "ligand_supported",
                                "readiness_blockers": [],
                                "counterevidence_reasons": [
                                    "nucleotide_transfer_ligand_context"
                                ],
                                "reaction_substrate_mismatch_reasons": [
                                    "kinase_name_with_hydrolase_top1"
                                ],
                                "mechanism_text_snippets": [
                                    "ATP phosphoryl transfer to glucose."
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            debt.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_summary",
                            "carried_review_debt_entry_ids": ["m_csa:650"],
                            "new_review_debt_entry_ids": ["m_csa:655"],
                        },
                        "rows": [{"entry_id": "m_csa:650"}],
                    }
                ),
                encoding="utf-8",
            )
            mismatch_export.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "reaction_substrate_mismatch_review_export",
                            "exported_count": 1,
                            "exported_entry_ids": ["m_csa:655"],
                        },
                        "review_items": [{"entry_id": "m_csa:655"}],
                    }
                ),
                encoding="utf-8",
            )
            remediation.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:650",
                                "remediation_bucket": "active_site_mapping_repair",
                                "selected_pdb_id": "1ABC",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            structure_mapping.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:650",
                                "status": "insufficient_resolved_residues",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            alternate_scan.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:650",
                                "scan_outcome": "no_expected_cofactor_in_scanned_structures",
                                "scanned_structure_count": 3,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-expert-label-decision-review-export",
                    "--active-learning-queue",
                    str(queue),
                    "--labels",
                    str(labels),
                    "--review-debt",
                    str(debt),
                    "--reaction-substrate-mismatch-review-export",
                    str(mismatch_export),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            export = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(export["metadata"]["exported_count"], 2)
            self.assertEqual(export["metadata"]["decision_counts"], {"no_decision": 2})
            self.assertEqual(export["metadata"]["countable_label_candidate_count"], 0)
            self.assertEqual(
                export["metadata"][
                    "missing_reaction_substrate_mismatch_export_entry_ids"
                ],
                [],
            )
            self.assertEqual(
                export["metadata"]["quality_risk_flag_counts"][
                    "external_expert_decision_required"
                ],
                2,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "summarize-expert-label-decision-repair-candidates",
                    "--expert-label-decision-review-export",
                    str(out),
                    "--review-debt-remediation",
                    str(remediation),
                    "--structure-mapping",
                    str(structure_mapping),
                    "--alternate-structure-scan",
                    str(alternate_scan),
                    "--max-rows",
                    "0",
                    "--out",
                    str(repair_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            repair = json.loads(repair_out.read_text(encoding="utf-8"))
            self.assertEqual(repair["metadata"]["candidate_count"], 2)
            self.assertEqual(repair["metadata"]["countable_label_candidate_count"], 0)
            self.assertEqual(
                repair["metadata"]["repair_bucket_counts"][
                    "reaction_substrate_review_already_exported"
                ],
                1,
            )
            self.assertEqual(repair["metadata"]["remediation_context_linked_count"], 1)
            self.assertEqual(
                repair["metadata"]["structure_mapping_context_linked_count"], 1
            )
            self.assertEqual(
                repair["metadata"]["alternate_structure_scan_context_linked_count"], 1
            )
            rows = {row["entry_id"]: row for row in repair["rows"]}
            self.assertEqual(
                rows["m_csa:650"]["alternate_structure_scan_context"][
                    "scanned_structure_count"
                ],
                3,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-expert-label-decision-repair-guardrails",
                    "--expert-label-decision-repair-candidates",
                    str(repair_out),
                    "--out",
                    str(guardrail_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            guardrail = json.loads(guardrail_out.read_text(encoding="utf-8"))
            self.assertTrue(guardrail["metadata"]["guardrail_ready"])
            self.assertEqual(guardrail["metadata"]["priority_repair_row_count"], 1)
            self.assertEqual(
                guardrail["metadata"]["countable_label_candidate_count"], 0
            )
            self.assertIn(
                "active_site_mapping_or_structure_gap_unresolved",
                guardrail["rows"][0]["non_countable_blockers"],
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-expert-label-decision-local-evidence-gaps",
                    "--expert-label-decision-repair-guardrail-audit",
                    str(guardrail_out),
                    "--expert-label-decision-repair-candidates",
                    str(repair_out),
                    "--out",
                    str(local_gap_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            local_gap = json.loads(local_gap_out.read_text(encoding="utf-8"))
            self.assertTrue(local_gap["metadata"]["audit_ready"])
            self.assertEqual(local_gap["metadata"]["audited_entry_count"], 1)
            self.assertEqual(
                local_gap["metadata"]["countable_label_candidate_count"], 0
            )
            self.assertIn(
                "scanned_structures_without_local_expected_family_hit",
                local_gap["rows"][0]["local_evidence_gap_classes"],
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-expert-label-decision-local-evidence-review-export",
                    "--expert-label-decision-local-evidence-gap-audit",
                    str(local_gap_out),
                    "--labels",
                    str(labels),
                    "--out",
                    str(local_gap_export_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            local_gap_export = json.loads(
                local_gap_export_out.read_text(encoding="utf-8")
            )
            self.assertTrue(local_gap_export["metadata"]["export_ready"])
            self.assertEqual(local_gap_export["metadata"]["decision_counts"], {"no_decision": 1})
            self.assertEqual(
                local_gap_export["metadata"]["countable_label_candidate_count"], 0
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "summarize-expert-label-decision-local-evidence-repair-plan",
                    "--expert-label-decision-local-evidence-gap-audit",
                    str(local_gap_out),
                    "--expert-label-decision-local-evidence-review-export",
                    str(local_gap_export_out),
                    "--out",
                    str(local_gap_plan_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            local_gap_plan = json.loads(
                local_gap_plan_out.read_text(encoding="utf-8")
            )
            self.assertTrue(local_gap_plan["metadata"]["repair_plan_ready"])
            self.assertEqual(local_gap_plan["metadata"]["planned_entry_count"], 1)

    def test_import_countable_review_rejects_automation_mismatch_accepts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            labels = root / "labels.json"
            review = root / "mismatch_review.json"
            out = root / "countable_labels.json"
            labels.write_text("[]", encoding="utf-8")
            review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "reaction_substrate_mismatch_review_export"
                        },
                        "review_items": [
                            {
                                "entry_id": "m_csa:656",
                                "entry_name": "pending ribokinase",
                                "decision": {
                                    "action": "accept_label",
                                    "label_type": "seed_fingerprint",
                                    "fingerprint_id": "metal_dependent_hydrolase",
                                    "tier": "bronze",
                                    "confidence": "medium",
                                    "reviewer": "automation_label_factory",
                                    "rationale": (
                                        "Automation must not count mismatch "
                                        "review rows without expert resolution."
                                    ),
                                    "evidence_score": 0.65,
                                    "review_status": "automation_curated",
                                    "reaction_substrate_resolution": "needs_more_evidence",
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "import-countable-label-review",
                    "--review",
                    str(review),
                    "--labels",
                    str(labels),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual(json.loads(out.read_text(encoding="utf-8")), [])

    def test_audit_review_only_import_safety_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            labels = root / "labels.json"
            review = root / "review_only_batch.json"
            out = root / "import_safety.json"
            labels.write_text("[]", encoding="utf-8")
            review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "provisional_label_review_decision_batch",
                            "source_method": "reaction_substrate_mismatch_review_export",
                            "reaction_substrate_mismatch_review_only": True,
                            "decision_counts": {"accept_label": 1},
                        },
                        "review_items": [
                            {
                                "entry_id": "m_csa:656",
                                "entry_name": "pending ribokinase",
                                "decision": {
                                    "action": "accept_label",
                                    "label_type": "out_of_scope",
                                    "fingerprint_id": None,
                                    "tier": "bronze",
                                    "confidence": "high",
                                    "reviewer": "test_reviewer",
                                    "rationale": "Reviewed but still review-only.",
                                    "evidence_score": None,
                                    "review_status": "expert_reviewed",
                                    "reaction_substrate_resolution": (
                                        "confirm_current_label_or_out_of_scope"
                                    ),
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-review-only-import-safety",
                    "--review",
                    str(review),
                    "--labels",
                    str(labels),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(audit["metadata"]["countable_import_safe"])
            self.assertEqual(audit["metadata"]["total_new_countable_label_count"], 0)
            self.assertTrue(
                audit["rows"][0]["review_only_flags"][
                    "reaction_substrate_mismatch_review_only"
                ]
            )

    def test_audit_accepted_review_debt_deferrals_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            review_debt = root / "review_debt.json"
            acceptance = root / "acceptance.json"
            remap = root / "remap.json"
            import_safety = root / "import_safety.json"
            out = root / "deferrals.json"
            review_debt.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_summary",
                            "review_debt_entry_ids": ["m_csa:712"],
                            "new_review_debt_entry_ids": ["m_csa:712"],
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:712",
                                "entry_name": "strict remap local lead",
                                "debt_status": "new",
                                "recommended_next_action": (
                                    "expert_family_boundary_review"
                                ),
                                "decision_action": "mark_needs_more_evidence",
                                "gap_reasons": ["review_marked_needs_more_evidence"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            acceptance.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "label_batch_acceptance_check",
                            "accepted_new_label_entry_ids": ["m_csa:705"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            remap.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_remap_local_lead_audit",
                            "strict_remap_guardrail_entry_ids": ["m_csa:712"],
                            "expert_family_boundary_review_entry_ids": ["m_csa:712"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            import_safety.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_only_import_safety_audit",
                            "countable_import_safe": True,
                            "total_new_countable_label_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-accepted-review-debt-deferrals",
                    "--review-debt",
                    str(review_debt),
                    "--acceptance",
                    str(acceptance),
                    "--remap-local-lead-audit",
                    str(remap),
                    "--review-only-import-safety-audit",
                    str(import_safety),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(audit["metadata"]["deferral_ready"])
            self.assertEqual(audit["metadata"]["deferred_entry_count"], 1)
            self.assertEqual(
                audit["rows"][0]["deferral_status"],
                "deferred_strict_remap_family_boundary_review",
            )

    def test_audit_mechanism_ontology_gaps_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            queue = root / "queue.json"
            repair = root / "repair.json"
            local_gap = root / "local_gap.json"
            out = root / "ontology_gap.json"
            queue.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "rank": 1,
                                "entry_id": "m_csa:655",
                                "entry_name": "glucokinase",
                                "recommended_action": "expert_label_decision_needed",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "top1_ontology_family": "hydrolysis",
                                "reaction_substrate_mismatch_reasons": [
                                    "kinase_name_with_hydrolase_top1"
                                ],
                                "mechanism_text_snippets": [
                                    "ATP phosphoryl transfer to glucose."
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            repair.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:655",
                                "quality_risk_flags": [
                                    "text_leakage_or_nonlocal_evidence_risk"
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            local_gap.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_local_evidence_gap_audit"
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:655",
                                "local_evidence_gap_classes": [
                                    "reaction_substrate_mismatch_review_required"
                                ],
                                "recommended_next_action": (
                                    "route_to_reaction_substrate_expert_review"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-mechanism-ontology-gaps",
                    "--active-learning-queue",
                    str(queue),
                    "--expert-label-decision-repair-candidates",
                    str(repair),
                    "--expert-label-decision-local-evidence-gap-audit",
                    str(local_gap),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(audit["metadata"]["candidate_scope_signal_count"], 1)
            self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
            self.assertEqual(
                audit["metadata"]["local_evidence_gap_context_entry_count"], 1
            )
            self.assertIn("transferase_phosphoryl", audit["rows"][0]["scope_signals"])
            self.assertIn(
                "local_evidence_gap_unresolved",
                audit["rows"][0]["ontology_update_blockers"],
            )

    def test_build_atp_phosphoryl_transfer_family_expansion_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            decision_batch = root / "mismatch_decisions.json"
            out = root / "atp_families.json"
            hints = [
                ("m_csa:35", "phosphorylase kinase", "ePK"),
                ("m_csa:592", "glucokinase", "ASKHA"),
                ("m_csa:498", "glutathione synthase", "ATP-grasp"),
                ("m_csa:603", "pyruvate dehydrogenase kinase", "GHKL"),
                ("m_csa:588", "thymidine kinase", "dNK"),
                ("m_csa:637", "nucleoside-diphosphate kinase", "NDK"),
                ("m_csa:365", "Phosphofructokinase I", "PfkA"),
                ("m_csa:663", "ribokinase", "PfkB"),
                ("m_csa:654", "CDP-ME kinase", "GHMP"),
            ]
            decision_batch.write_text(
                json.dumps(
                    {
                        "review_items": [
                            {
                                "entry_id": entry_id,
                                "entry_name": name,
                                "mismatch_context": {
                                    "entry_id": entry_id,
                                    "entry_name": name,
                                    "top1_fingerprint_id": (
                                        "metal_dependent_hydrolase"
                                    ),
                                    "top1_ontology_family": "hydrolysis",
                                    "mismatch_reasons": [
                                        "kinase_name_with_hydrolase_top1"
                                    ],
                                },
                                "decision": {
                                    "action": "reject_label",
                                    "label_type": "out_of_scope",
                                    "review_status": "expert_reviewed",
                                    "reviewer": "test_reviewer",
                                    "reaction_substrate_resolution": (
                                        "confirm_current_label_or_out_of_scope"
                                    ),
                                    "future_fingerprint_family_hint": hint,
                                },
                            }
                            for entry_id, name, hint in hints
                        ]
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-atp-phosphoryl-transfer-family-expansion",
                    "--reaction-substrate-mismatch-decision-batch",
                    str(decision_batch),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            expansion = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(expansion["metadata"]["boundary_guardrail_ready"])
            self.assertEqual(expansion["metadata"]["countable_label_candidate_count"], 0)
            self.assertEqual(
                expansion["metadata"]["mapped_required_family_ids"],
                [
                    "askha",
                    "atp_grasp",
                    "dnk",
                    "epk",
                    "ghkl",
                    "ghmp",
                    "ndk",
                    "pfka",
                    "pfkb",
                ],
            )

    def test_build_epk_positive_fingerprint_readiness_packet_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            atp_expansion = root / "atp_expansion.json"
            decision_batch = root / "mismatch_decisions.json"
            reaudit_policy = root / "reaudit_policy.json"
            out = root / "epk_readiness.json"
            epk_rows = [
                (
                    "m_csa:35",
                    "phosphorylase kinase",
                    "Asp149 deprotonates the protein substrate hydroxyl group before attack on the gamma-phosphate of ATP.",
                ),
                (
                    "m_csa:246",
                    "receptor protein-tyrosine kinase",
                    "A tyrosine hydroxyl attacks the gamma phosphate of ATP with Mg2+ phosphate positioning.",
                ),
                (
                    "m_csa:640",
                    "kanamycin kinase",
                    "A substrate hydroxyl attacks ATP gamma phosphate during aminoglycoside phosphorylation.",
                ),
            ]
            atp_expansion.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "atp_phosphoryl_transfer_family_expansion"
                        },
                        "rows": [
                            {
                                "entry_id": entry_id,
                                "entry_name": entry_name,
                                "family_id": "epk",
                                "support_level": (
                                    "expert_review_supported_family_boundary"
                                ),
                                "decision_action": "reject_label",
                                "decision_label_type": "out_of_scope",
                                "decision_review_status": "expert_reviewed",
                                "reaction_substrate_resolution": (
                                    "confirm_current_label_or_out_of_scope"
                                ),
                                "reviewer": "test_reviewer",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "top1_ontology_family": "hydrolysis",
                                "mismatch_reasons": [
                                    "kinase_name_with_hydrolase_top1"
                                ],
                                "propagation_blockers": [
                                    "reaction_substrate_mismatch"
                                ],
                                "countable_label_candidate": False,
                            }
                            for entry_id, entry_name, _snippet in epk_rows
                        ],
                    }
                ),
                encoding="utf-8",
            )
            decision_batch.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "provisional_label_review_decision_batch"
                        },
                        "review_items": [
                            {
                                "entry_id": entry_id,
                                "entry_name": entry_name,
                                "mismatch_context": {
                                    "entry_id": entry_id,
                                    "entry_name": entry_name,
                                    "top1_fingerprint_id": (
                                        "metal_dependent_hydrolase"
                                    ),
                                    "top1_ontology_family": "hydrolysis",
                                    "mechanism_text_snippets": [snippet],
                                    "mismatch_reasons": [
                                        "kinase_name_with_hydrolase_top1"
                                    ],
                                },
                                "decision": {
                                    "action": "reject_label",
                                    "label_type": "out_of_scope",
                                    "review_status": "expert_reviewed",
                                    "reviewer": "test_reviewer",
                                    "reaction_substrate_resolution": (
                                        "confirm_current_label_or_out_of_scope"
                                    ),
                                    "future_fingerprint_family_hint": "ePK",
                                    "rationale": (
                                        f"{entry_name} is ePK-like ATP "
                                        "gamma-phosphoryl transfer to a "
                                        "hydroxyl acceptor."
                                    ),
                                },
                            }
                            for entry_id, entry_name, snippet in epk_rows
                        ],
                    }
                ),
                encoding="utf-8",
            )
            reaudit_policy.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "external_hard_negative_ontology_reaudit_policy"
                            )
                        },
                        "expansion_triggers": [
                            "epk",
                            "any_positive_fingerprint_universe_expansion",
                        ],
                        "external_labels_requiring_reaudit": [
                            {"entry_id": "uniprot:P06744"}
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-positive-fingerprint-readiness-packet",
                    "--atp-phosphoryl-transfer-family-expansion",
                    str(atp_expansion),
                    "--reaction-substrate-mismatch-decision-batch",
                    str(decision_batch),
                    "--external-hard-negative-ontology-reaudit-policy",
                    str(reaudit_policy),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            packet = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(
                packet["metadata"]["evidence_ready_for_draft_fingerprint_spec"]
            )
            self.assertFalse(
                packet["metadata"]["ready_to_expand_positive_fingerprint_universe"]
            )
            # 46 after the 2026-06-12 through 2026-06-16 broadened-handle
            # batches plus the HAD-like phosphatase, aldehyde dehydrogenase, and
            # alpha/beta hydrolase esterase/lipase lanes, plus the Ser/Thr protein
            # phosphatase, N-ribosyl hydrolase, metal-independent PDE, APH, and
            # short-chain dehydrogenase/reductase and serine beta-lactamase lanes:
            # the readiness packet
            # counts the live positive fingerprint universe, not the historical
            # 15-fingerprint tranche.
            self.assertEqual(packet["metadata"]["current_positive_fingerprint_count"], 46)
            self.assertEqual(packet["metadata"]["epk_boundary_row_count"], 3)
            self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
            self.assertIn(
                "external_hard_negative_reaudit_required_before_positive_expansion_counts",
                packet["metadata"]["expansion_blockers"],
            )

    def test_build_epk_external_hard_negative_reaudit_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            epk_readiness = root / "epk_readiness.json"
            reaudit_policy = root / "reaudit_policy.json"
            labels = root / "labels.json"
            out = root / "reaudit_plan.json"
            epk_readiness.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_positive_fingerprint_readiness_packet",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "readiness_status": (
                                "draft_fingerprint_spec_ready_not_countable"
                            ),
                            "evidence_ready_for_draft_fingerprint_spec": True,
                            "ready_to_expand_positive_fingerprint_universe": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            reaudit_policy.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "external_hard_negative_ontology_reaudit_policy"
                            )
                        },
                        "expansion_triggers": ["epk"],
                        "external_labels_requiring_reaudit": [
                            {"entry_id": "uniprot:P06744"}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "uniprot:P06744",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "ontology_version_at_decision": "label_factory_v1_8fp",
                            "confidence": "medium",
                            "evidence_score": 0.65,
                            "rationale": (
                                "External hard-negative label retained for "
                                "the current ontology version only."
                            ),
                            "evidence": {
                                "predictive_evidence": ["scored local surface"],
                                "import_gate_evidence": ["factory gate passed"],
                                "review_only_context": ["source context"],
                                "excluded_context": ["annotation prose"],
                            },
                        }
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-external-hard-negative-reaudit-plan",
                    "--epk-positive-fingerprint-readiness-packet",
                    str(epk_readiness),
                    "--external-hard-negative-ontology-reaudit-policy",
                    str(reaudit_policy),
                    "--labels",
                    str(labels),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            plan = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(plan["metadata"]["reaudit_plan_ready"])
            self.assertFalse(plan["metadata"]["ready_to_run_scored_reaudit"])
            self.assertFalse(
                plan["metadata"]["ready_to_expand_positive_fingerprint_universe"]
            )
            self.assertEqual(plan["metadata"]["external_label_reaudit_row_count"], 1)
            self.assertEqual(plan["metadata"]["countable_label_candidate_count"], 0)

    def test_build_epk_draft_fingerprint_spec_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            epk_readiness = root / "epk_readiness.json"
            reaudit_plan = root / "reaudit_plan.json"
            out = root / "epk_draft_spec.json"
            epk_readiness.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_positive_fingerprint_readiness_packet",
                            "target_parent_family_id": "atp_phosphoryl_transfer",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "readiness_status": (
                                "draft_fingerprint_spec_ready_not_countable"
                            ),
                            "evidence_ready_for_draft_fingerprint_spec": True,
                            "ready_to_expand_positive_fingerprint_universe": False,
                            "current_positive_fingerprint_ids": [
                                "ser_his_acid_hydrolase",
                                "metal_dependent_hydrolase",
                                "plp_dependent_enzyme",
                                "radical_sam_enzyme",
                                "cobalamin_radical_rearrangement",
                                "flavin_monooxygenase",
                                "flavin_dehydrogenase_reductase",
                                "heme_peroxidase_oxidase",
                            ],
                        },
                        "target_fingerprint_draft": {
                            "id": "epk_atp_gamma_phosphoryl_transfer",
                            "name": "ePK/ePK-like ATP gamma-phosphoryl transfer",
                            "family_id": "epk",
                            "parent_family_id": "atp_phosphoryl_transfer",
                            "cofactors": ["ATP", "Mg2+"],
                        },
                        "rows": [
                            {
                                "entry_id": entry_id,
                                "entry_name": name,
                                "family_id": "epk",
                                "source_family_support_level": (
                                    "expert_review_supported_family_boundary"
                                ),
                                "expert_supported_family_boundary": True,
                                "active_site_base_evidence_status": (
                                    "review_text_support"
                                ),
                                "cofactor_evidence_status": (
                                    "review_text_mg_atp_context"
                                ),
                                "reaction_center_evidence_status": (
                                    "review_text_atp_gamma_phosphoryl_transfer"
                                ),
                                "acceptor_scope_evidence_status": (
                                    "review_text_hydroxyl_acceptor"
                                ),
                                "current_top1_fingerprint_id": (
                                    "metal_dependent_hydrolase"
                                ),
                                "current_top1_score": 0.3,
                                "readiness_blockers": [
                                    "positive_fingerprint_registry_not_expanded"
                                ],
                                "review_only": True,
                                "countable_label_candidate": False,
                            }
                            for entry_id, name in [
                                ("m_csa:35", "phosphorylase kinase"),
                                ("m_csa:246", "receptor protein-tyrosine kinase"),
                                ("m_csa:282", "MAP kinase kinase"),
                            ]
                        ],
                    }
                ),
                encoding="utf-8",
            )
            reaudit_plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_external_hard_negative_reaudit_plan",
                            "reaudit_plan_ready": True,
                            "ready_to_run_scored_reaudit": False,
                            "scored_reaudit_blockers": [
                                "epk_positive_scoring_rule_not_implemented"
                            ],
                        },
                        "rows": [
                            {
                                "entry_id": entry_id,
                                "reaudit_status": "planned_not_scored",
                                "current_label_contract_valid": True,
                                "evidence_separation_valid": True,
                                "review_only": True,
                                "countable_label_candidate": False,
                            }
                            for entry_id in [
                                "uniprot:P06744",
                                "uniprot:P78549",
                                "uniprot:Q3LXA3",
                            ]
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-draft-fingerprint-spec",
                    "--epk-positive-fingerprint-readiness-packet",
                    str(epk_readiness),
                    "--epk-external-hard-negative-reaudit-plan",
                    str(reaudit_plan),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            spec = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(
                spec["metadata"]["draft_spec_ready_for_scorer_prototype"]
            )
            self.assertFalse(
                spec["metadata"]["ready_to_expand_positive_fingerprint_universe"]
            )
            self.assertFalse(spec["metadata"]["fingerprint_registry_edited"])
            self.assertEqual(spec["metadata"]["countable_label_candidate_count"], 0)
            self.assertEqual(spec["metadata"]["current_positive_fingerprint_count"], 8)
            self.assertEqual(spec["metadata"]["external_reaudit_row_count"], 3)
            self.assertEqual(
                spec["external_hard_negative_reaudit_summary"]["reaudit_status"],
                "planned_not_scored",
            )
            self.assertIn(
                "M-CSA mechanism text",
                spec["draft_fingerprint_spec"]["predictive_evidence_exclusions"],
            )

    def test_build_epk_local_evidence_audit_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            draft_spec = root / "epk_draft_spec.json"
            geometry = root / "geometry.json"
            out = root / "epk_local_audit.json"
            draft_spec.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_draft_fingerprint_spec",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "draft_spec_ready_for_scorer_prototype": True,
                        },
                        "boundary_rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                            },
                            {
                                "entry_id": "m_csa:662",
                                "entry_name": "phosphatidylinositol kinase",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "geometry_feature_extraction",
                            "slice_size": 1000,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "status": "ok",
                                "pdb_id": "2PHK",
                                "resolved_residue_count": 3,
                                "ligand_context": {
                                    "ligand_codes": ["ATP", "MG"],
                                    "structure_ligand_codes": ["ATP", "MG"],
                                },
                                "residues": [
                                    {
                                        "code": "Asp",
                                        "resid": 149,
                                        "chain_name": "A",
                                        "roles": ["proton acceptor"],
                                    }
                                ],
                            },
                            {
                                "entry_id": "m_csa:662",
                                "status": "ok",
                                "pdb_id": "1BO1",
                                "resolved_residue_count": 2,
                                "ligand_context": {
                                    "ligand_codes": [],
                                    "structure_ligand_codes": [],
                                },
                                "residues": [
                                    {
                                        "code": "Asp",
                                        "resid": 278,
                                        "chain_name": "A",
                                        "roles": ["proton shuttle"],
                                    }
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-local-evidence-audit",
                    "--epk-draft-fingerprint-spec",
                    str(draft_spec),
                    "--geometry",
                    str(geometry),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(audit["metadata"]["method"], "epk_local_evidence_audit")
            self.assertEqual(audit["metadata"]["boundary_row_count"], 2)
            self.assertEqual(
                audit["metadata"]["ready_for_text_free_axis_prototype_count"], 1
            )
            self.assertFalse(audit["metadata"]["ready_to_run_epk_scorer"])
            rows = {row["entry_id"]: row for row in audit["rows"]}
            self.assertEqual(
                rows["m_csa:35"]["scorer_input_readiness"],
                "ready_for_text_free_axis_prototype",
            )
            self.assertEqual(
                rows["m_csa:662"]["scorer_input_readiness"],
                "needs_ligand_source_or_alternate_structure",
            )

    def test_build_epk_text_free_local_axis_prototype_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            audit = root / "epk_local_audit.json"
            out = root / "epk_axis_prototype.json"
            audit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_local_evidence_audit",
                            "audit_status": "local_evidence_profile_ready_not_scored",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "boundary_row_count": 2,
                            "ready_for_text_free_axis_prototype_count": 1,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "pdb_id": "2PHK",
                                "geometry_status": "ok",
                                "scorer_input_readiness": (
                                    "ready_for_text_free_axis_prototype"
                                ),
                                "local_nucleotide_ligand_codes": ["ATP"],
                                "local_metal_ligand_codes": ["MG"],
                                "acid_base_residues": [
                                    {
                                        "code": "Asp",
                                        "resid": 136,
                                        "chain_name": "A",
                                        "roles": ["proton acceptor"],
                                    }
                                ],
                                "audit_blockers": [
                                    "acceptor_axis_still_source_traced_not_geometry_scored",
                                    "no_epk_score_computed",
                                ],
                            },
                            {
                                "entry_id": "m_csa:662",
                                "entry_name": "phosphatidylinositol kinase",
                                "scorer_input_readiness": (
                                    "needs_ligand_source_or_alternate_structure"
                                ),
                                "local_feature_status": "local_ligand_axis_missing",
                                "audit_blockers": [
                                    "local_atp_or_adenine_nucleotide_ligand_missing",
                                    "local_mg_or_metal_ligand_missing",
                                    "no_epk_score_computed",
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-text-free-local-axis-prototype",
                    "--epk-local-evidence-audit",
                    str(audit),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            prototype = json.loads(out.read_text(encoding="utf-8"))
            metadata = prototype["metadata"]
            self.assertEqual(metadata["method"], "epk_text_free_local_axis_prototype")
            self.assertEqual(metadata["prototype_ready_row_count"], 1)
            self.assertEqual(metadata["excluded_row_count"], 1)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            self.assertEqual(metadata["countable_label_candidate_count"], 0)
            self.assertEqual(prototype["rows"][0]["axis_presence_count"], 3)
            self.assertFalse(prototype["rows"][0]["epk_score_computed"])
            self.assertIn(
                "external_hard_negative_inverse_axis",
                metadata["blocked_axis_ids"],
            )
            self.assertEqual(
                prototype["excluded_rows"][0]["entry_id"],
                "m_csa:662",
            )

    def test_build_epk_acceptor_geometry_axis_gap_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype_path = root / "epk_axis_prototype.json"
            geometry = root / "geometry.json"
            out = root / "epk_acceptor_plan.json"
            prototype_path.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_text_free_local_axis_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "prototype_ready_row_count": 1,
                            "excluded_row_count": 1,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "pdb_id": "2PHK",
                                "geometry_status": "ok",
                                "axis_presence_count": 3,
                            }
                        ],
                        "excluded_rows": [
                            {
                                "entry_id": "m_csa:662",
                                "entry_name": "phosphatidylinositol kinase",
                                "source_scorer_input_readiness": (
                                    "needs_ligand_source_or_alternate_structure"
                                ),
                                "exclusion_reasons": ["local_ligand_axis_missing"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "active_site_geometry_features",
                            "slice_size": 1000,
                        },
                        "entries": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "status": "ok",
                                "pdb_id": "2PHK",
                                "ligand_context": {
                                    "structure_ligands": [
                                        {
                                            "code": "PTR",
                                            "min_distance_to_active_site": 7.5,
                                            "atom_count": 20,
                                            "instance_count": 1,
                                        }
                                    ]
                                },
                                "pocket_context": {
                                    "distance_cutoff_angstrom": 8.0,
                                    "nearby_residue_sites": [
                                        {
                                            "code": "THR",
                                            "resid": "166",
                                            "chain_name": "A",
                                            "min_distance_to_active_site": 3.2,
                                            "atom_count": 7,
                                        },
                                        {
                                            "code": "ASP",
                                            "resid": "154",
                                            "chain_name": "A",
                                            "min_distance_to_active_site": 4.0,
                                            "atom_count": 8,
                                        },
                                    ],
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-acceptor-geometry-axis-gap-plan",
                    "--epk-text-free-local-axis-prototype",
                    str(prototype_path),
                    "--geometry",
                    str(geometry),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            plan = json.loads(out.read_text(encoding="utf-8"))
            metadata = plan["metadata"]
            self.assertEqual(metadata["method"], "epk_acceptor_geometry_axis_gap_plan")
            self.assertEqual(metadata["prototype_ready_row_count"], 1)
            self.assertEqual(metadata["excluded_row_count"], 1)
            self.assertEqual(metadata["rows_with_candidate_acceptor_context_count"], 1)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = plan["rows"][0]
            self.assertEqual(
                row["acceptor_axis_status"],
                "hydroxyl_residue_and_acceptor_ligand_context_present_not_scored",
            )
            self.assertEqual(row["hydroxyl_residue_candidate_count"], 1)
            self.assertEqual(row["acceptor_like_structure_ligand_count"], 1)
            self.assertFalse(row["epk_score_computed"])
            self.assertIn("acceptor_axis_not_thresholded", row["remaining_blockers"])

    def test_build_epk_nonready_ligand_repair_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            audit = root / "epk_local_audit.json"
            geometry = root / "geometry.json"
            out = root / "epk_nonready_repair.json"
            audit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_local_evidence_audit",
                            "audit_status": "local_evidence_profile_ready_not_scored",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "boundary_row_count": 2,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "scorer_input_readiness": (
                                    "ready_for_text_free_axis_prototype"
                                ),
                            },
                            {
                                "entry_id": "m_csa:282",
                                "entry_name": "MAP kinase kinase",
                                "pdb_id": "1S9I",
                                "geometry_status": "ok",
                                "scorer_input_readiness": (
                                    "needs_ligand_distance_or_structure_repair"
                                ),
                                "local_feature_status": (
                                    "structure_ligand_signal_not_local_axis"
                                ),
                                "local_ligand_codes": [],
                                "structure_ligand_codes": ["ATP", "MG"],
                                "audit_blockers": [
                                    "local_atp_or_adenine_nucleotide_ligand_missing",
                                    "local_mg_or_metal_ligand_missing",
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "active_site_geometry_features"},
                        "entries": [
                            {
                                "entry_id": "m_csa:282",
                                "status": "ok",
                                "pdb_id": "1S9I",
                                "ligand_context": {
                                    "structure_ligands": [
                                        {
                                            "code": "ATP",
                                            "min_distance_to_active_site": 14.7,
                                            "atom_count": 62,
                                            "instance_count": 2,
                                        },
                                        {
                                            "code": "MG",
                                            "min_distance_to_active_site": 16.1,
                                            "atom_count": 2,
                                            "instance_count": 2,
                                        },
                                    ]
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-nonready-ligand-repair-plan",
                    "--epk-local-evidence-audit",
                    str(audit),
                    "--geometry",
                    str(geometry),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            plan = json.loads(out.read_text(encoding="utf-8"))
            metadata = plan["metadata"]
            self.assertEqual(metadata["method"], "epk_nonready_ligand_repair_plan")
            self.assertEqual(metadata["nonready_row_count"], 1)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = plan["rows"][0]
            self.assertEqual(row["entry_id"], "m_csa:282")
            self.assertEqual(row["repair_lane"], "structure_ligand_signal_not_local_axis")
            self.assertEqual(row["structure_nucleotide_ligand_leads"][0]["code"], "ATP")
            self.assertEqual(row["structure_metal_ligand_leads"][0]["code"], "MG")
            self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_nonready_ligand_alternate_structure_plan_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            repair = root / "repair.json"
            graph = root / "graph.json"
            cif_dir = root / "cif"
            cif_dir.mkdir()
            out = root / "alternate_plan.json"
            repair.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_nonready_ligand_repair_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:282",
                                "entry_name": "MAP kinase kinase",
                                "pdb_id": "1AAA",
                                "repair_lane": "structure_ligand_signal_not_local_axis",
                                "source_scorer_input_readiness": (
                                    "needs_ligand_distance_or_structure_repair"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "v1_graph"},
                        "nodes": [
                            {
                                "id": "m_csa:282",
                                "type": "m_csa_entry",
                                "reference_uniprot_id": "PTEST",
                            },
                            {
                                "id": "m_csa:282:residue:1",
                                "type": "catalytic_residue",
                                "sequence_positions": [
                                    {
                                        "uniprot_id": "PTEST",
                                        "resid": 44,
                                        "code": "Lys",
                                    }
                                ],
                            },
                        ],
                        "edges": [
                            {
                                "source": "m_csa:282",
                                "target": "uniprot:PTEST",
                                "predicate": "has_reference_protein",
                            },
                            {
                                "source": "uniprot:PTEST",
                                "target": "pdb:1AAA",
                                "predicate": "has_structure",
                            },
                            {
                                "source": "uniprot:PTEST",
                                "target": "pdb:1AAB",
                                "predicate": "has_structure",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            for pdb_id in ("1AAA", "1AAB"):
                (cif_dir / f"pdb_{pdb_id}.cif").write_text(
                    "\n".join(
                        [
                            f"data_{pdb_id}",
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
                            "HETATM 1 P PG ATP A 1 0.0 0.0 0.0 PG ATP A 1",
                            "HETATM 2 MG MG MG A 2 1.0 0.0 0.0 MG MG A 2",
                            "ATOM 3 N NZ LYS A 44 2.0 0.0 0.0 NZ LYS A 44",
                            "#",
                        ]
                    ),
                    encoding="utf-8",
                )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-nonready-ligand-alternate-structure-plan",
                    "--epk-nonready-ligand-repair-plan",
                    str(repair),
                    "--graph",
                    str(graph),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            plan = json.loads(out.read_text(encoding="utf-8"))
            metadata = plan["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_nonready_ligand_alternate_structure_plan",
            )
            self.assertEqual(metadata["row_count"], 1)
            self.assertEqual(metadata["alternate_gamma_structure_count"], 1)
            self.assertEqual(
                metadata["alternate_gamma_metal_mapped_structure_count"],
                1,
            )
            self.assertFalse(metadata["ready_to_rerun_local_evidence_audit"])
            row = plan["rows"][0]
            self.assertEqual(
                row["repair_evidence_status"],
                "alternate_gamma_metal_structure_found_review_only",
            )
            self.assertEqual(row["alternate_gamma_metal_mapped_structure_count"], 1)
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_nonready_ligand_exclusion_decision_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            repair = root / "repair.json"
            alternate = root / "alternate.json"
            out = root / "exclusion.json"
            repair.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_nonready_ligand_repair_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:282",
                                "entry_name": "MAP kinase kinase",
                                "pdb_id": "1AAA",
                                "repair_lane": "structure_ligand_signal_not_local_axis",
                                "source_scorer_input_readiness": (
                                    "needs_ligand_distance_or_structure_repair"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_nonready_ligand_alternate_structure_plan"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:282",
                                "entry_name": "MAP kinase kinase",
                                "current_selected_pdb_id": "1AAA",
                                "repair_evidence_status": (
                                    "alternate_gamma_structure_found_metal_or_mapping_gap"
                                ),
                                "candidate_structures": [
                                    {
                                        "pdb_id": "1AAA",
                                        "current_selected_structure": True,
                                        "has_gamma_capable_nucleotide": True,
                                        "has_metal_ligand": True,
                                        "all_catalytic_residues_mapped": True,
                                    },
                                    {
                                        "pdb_id": "1AAB",
                                        "current_selected_structure": False,
                                        "has_gamma_capable_nucleotide": True,
                                        "has_metal_ligand": False,
                                        "all_catalytic_residues_mapped": False,
                                    },
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-nonready-ligand-exclusion-decision",
                    "--epk-nonready-ligand-repair-plan",
                    str(repair),
                    "--epk-nonready-ligand-alternate-structure-plan",
                    str(alternate),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            decision = json.loads(out.read_text(encoding="utf-8"))
            metadata = decision["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_nonready_ligand_exclusion_decision",
            )
            self.assertEqual(metadata["excluded_nonready_row_count"], 1)
            self.assertEqual(metadata["excluded_nonready_entry_ids"], ["m_csa:282"])
            self.assertTrue(metadata["nonready_rows_repaired_or_excluded"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = decision["rows"][0]
            self.assertEqual(
                row["exclusion_decision"],
                "exclude_from_current_epk_threshold_calibration",
            )
            self.assertTrue(row["excluded_from_current_epk_threshold_calibration"])
            self.assertEqual(row["alternate_gamma_structure_count"], 1)
            self.assertEqual(row["alternate_gamma_metal_mapped_structure_count"], 0)
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_acceptor_axis_threshold_design_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            acceptor_plan = root / "epk_acceptor_plan.json"
            out = root / "epk_threshold_design.json"
            acceptor_plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_acceptor_geometry_axis_gap_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "prototype_ready_row_count": 2,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "nearest_hydroxyl_residue_distance_angstrom": 2.5,
                                "nearest_acceptor_ligand_distance_angstrom": None,
                                "acceptor_axis_status": (
                                    "hydroxyl_residue_context_present_not_scored"
                                ),
                            },
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "nearest_hydroxyl_residue_distance_angstrom": 5.2,
                                "nearest_acceptor_ligand_distance_angstrom": 6.3,
                                "acceptor_axis_status": (
                                    "hydroxyl_residue_and_acceptor_ligand_context_present_not_scored"
                                ),
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-acceptor-axis-threshold-design",
                    "--epk-acceptor-geometry-axis-gap-plan",
                    str(acceptor_plan),
                    "--candidate-thresholds",
                    "4,6,8",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            design = json.loads(out.read_text(encoding="utf-8"))
            metadata = design["metadata"]
            self.assertEqual(metadata["method"], "epk_acceptor_axis_threshold_design")
            self.assertEqual(metadata["candidate_thresholds_angstrom"], [4.0, 6.0, 8.0])
            self.assertEqual(
                metadata[
                    "smallest_candidate_hydroxyl_cutoff_covering_current_prototype_rows"
                ],
                6.0,
            )
            self.assertIsNone(metadata["selected_threshold_angstrom"])
            self.assertFalse(metadata["threshold_calibrated"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            threshold_rows = {
                row["candidate_threshold_angstrom"]: row
                for row in design["threshold_rows"]
            }
            self.assertEqual(threshold_rows[4.0]["hydroxyl_residue_hit_count"], 1)
            self.assertEqual(threshold_rows[6.0]["hydroxyl_residue_hit_count"], 2)
            self.assertEqual(threshold_rows[8.0]["acceptor_ligand_hit_count"], 1)

    def test_build_epk_gamma_geometry_feasibility_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype_path = root / "epk_axis_prototype.json"
            acceptor_plan = root / "epk_acceptor_plan.json"
            out = root / "epk_gamma_feasibility.json"
            prototype_path.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_text_free_local_axis_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "text_free_axis_inputs": {
                                    "local_adenine_nucleotide_ligand": {
                                        "evidence_codes": ["ATP"]
                                    }
                                },
                            },
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "text_free_axis_inputs": {
                                    "local_adenine_nucleotide_ligand": {
                                        "evidence_codes": ["ADP"]
                                    }
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            acceptor_plan.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "epk_acceptor_geometry_axis_gap_plan"},
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "acceptor_axis_status": (
                                    "hydroxyl_residue_context_present_not_scored"
                                ),
                                "nearest_hydroxyl_residue_distance_angstrom": 2.5,
                            },
                            {
                                "entry_id": "m_csa:640",
                                "acceptor_axis_status": (
                                    "hydroxyl_residue_and_acceptor_ligand_context_present_not_scored"
                                ),
                                "nearest_hydroxyl_residue_distance_angstrom": 5.2,
                                "nearest_acceptor_ligand_distance_angstrom": 6.3,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-gamma-geometry-feasibility-plan",
                    "--epk-text-free-local-axis-prototype",
                    str(prototype_path),
                    "--epk-acceptor-geometry-axis-gap-plan",
                    str(acceptor_plan),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            plan = json.loads(out.read_text(encoding="utf-8"))
            metadata = plan["metadata"]
            self.assertEqual(metadata["method"], "epk_gamma_geometry_feasibility_plan")
            self.assertFalse(metadata["gamma_phosphate_geometry_measured"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            rows = {row["entry_id"]: row for row in plan["rows"]}
            self.assertEqual(
                rows["m_csa:35"]["gamma_geometry_feasibility_status"],
                "gamma_capable_nucleotide_and_acceptor_context_present_not_measured",
            )
            self.assertEqual(
                rows["m_csa:640"]["gamma_geometry_feasibility_status"],
                "product_state_nucleotide_acceptor_context_present_needs_gamma_source",
            )
            self.assertFalse(rows["m_csa:35"]["epk_score_computed"])

    def test_build_epk_gamma_geometry_measurement_sample_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            feasibility = root / "epk_gamma_feasibility.json"
            geometry = root / "geometry.json"
            cif_dir = root / "cif"
            cif_dir.mkdir()
            out = root / "epk_gamma_measurement.json"
            feasibility.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_geometry_feasibility_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "gamma_capable_nucleotide_codes": ["ATP"],
                            },
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "gamma_capable_nucleotide_codes": [],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "active_site_geometry_features"},
                        "entries": [
                            {
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "pocket_context": {
                                    "nearby_residue_sites": [
                                        {
                                            "code": "THR",
                                            "chain_name": "A",
                                            "resid": "166",
                                        }
                                    ]
                                },
                            },
                            {"entry_id": "m_csa:640", "pdb_id": "1L8T"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (cif_dir / "2PHK.cif").write_text(
                "\n".join(
                    [
                        "data_2PHK",
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
                        "HETATM 1 P PG ATP A 1 0.0 0.0 0.0 PG ATP A 1",
                        "ATOM 2 O OG1 THR A 166 3.0 4.0 0.0 OG1 THR A 166",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-gamma-geometry-measurement-sample",
                    "--epk-gamma-geometry-feasibility-plan",
                    str(feasibility),
                    "--geometry",
                    str(geometry),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            sample = json.loads(out.read_text(encoding="utf-8"))
            metadata = sample["metadata"]
            self.assertEqual(metadata["method"], "epk_gamma_geometry_measurement_sample")
            self.assertEqual(metadata["measured_row_count"], 1)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            rows = {row["entry_id"]: row for row in sample["rows"]}
            self.assertEqual(
                rows["m_csa:35"]["measurement_status"],
                "gamma_to_hydroxyl_distance_measured_review_only",
            )
            self.assertEqual(
                rows["m_csa:35"]["nearest_gamma_to_hydroxyl_distance_angstrom"],
                5.0,
            )
            self.assertEqual(
                rows["m_csa:640"]["measurement_status"],
                "product_or_missing_gamma_nucleotide_skipped",
            )
            self.assertFalse(rows["m_csa:35"]["epk_score_computed"])

    def test_build_epk_precount_gate_status_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            axis = root / "axis.json"
            threshold = root / "threshold.json"
            gamma = root / "gamma.json"
            repair = root / "repair.json"
            negative = root / "negative_controls.json"
            reaudit = root / "reaudit.json"
            template = root / "template.json"
            template_validation = root / "template_validation.json"
            chain_ligand = root / "chain_ligand.json"
            chain_external = root / "chain_external.json"
            ligand_policy = root / "ligand_policy.json"
            activation = root / "activation.json"
            control_reaudit = root / "control_reaudit.json"
            score_probe = root / "score_probe.json"
            fivehvk = root / "fivehvk.json"
            fivehvk_queue = root / "fivehvk_queue.json"
            five_li1 = root / "5li1.json"
            heteromeric_control = root / "heteromeric_control.json"
            heteromeric_gap = root / "heteromeric_gap.json"
            heteromeric_probe = root / "heteromeric_probe.json"
            heteromeric_counteraxis = root / "heteromeric_counteraxis.json"
            heteromeric_broader = root / "heteromeric_broader.json"
            heteromeric_asymmetry = root / "heteromeric_asymmetry.json"
            heteromeric_identity = root / "heteromeric_identity.json"
            heteromeric_identity_rule = root / "heteromeric_identity_rule.json"
            heteromeric_peptide_external = root / "heteromeric_peptide_external.json"
            heteromeric_peptide_stress = root / "heteromeric_peptide_stress.json"
            heteromeric_source_expansion_peptide_role = (
                root / "heteromeric_source_expansion_peptide_role.json"
            )
            substrate_mode_gap = root / "substrate_mode_gap.json"
            out = root / "gate_status.json"
            axis.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_text_free_local_axis_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "prototype_ready_row_count": 3,
                        }
                    }
                ),
                encoding="utf-8",
            )
            threshold.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_acceptor_axis_threshold_design",
                            "selected_threshold_angstrom": None,
                            "threshold_calibrated": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            gamma.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_geometry_measurement_sample",
                            "measured_row_count": 2,
                            "measurement_status_counts": {
                                "gamma_to_hydroxyl_distance_measured_review_only": 2,
                                "product_or_missing_gamma_nucleotide_skipped": 1,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            repair.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_nonready_ligand_repair_plan",
                            "nonready_row_count": 2,
                            "repair_lane_counts": {
                                "selected_structure_ligand_axis_missing": 1
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            negative.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_negative_control_gamma_distance_distribution"
                            ),
                            "negative_control_distance_distribution_started": True,
                            "negative_control_distance_distribution_ready": False,
                            "measured_control_count": 1,
                            "lowest_covering_candidate_negative_control_hit_count": 1,
                            "threshold_selection_status": (
                                "blocked_negative_controls_overlap_or_insufficient_distribution"
                            ),
                        }
                    }
                ),
                encoding="utf-8",
            )
            reaudit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_external_hard_negative_reaudit_plan",
                            "ready_to_run_scored_reaudit": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            template.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_family_specific_mapping_template_review",
                            "reviewed_sibling_family_id": "pfkb",
                            "seeded_template_entry_count": 1,
                            "template_residue_count": 2,
                            "template_review_status": (
                                "template_seeded_mapping_algorithm_pending_review_only"
                            ),
                            "family_specific_mapping_ready": False,
                            "measurement_ready_homolog_structure_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            template_validation.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_family_specific_mapping_template_validation_review"
                            ),
                            "template_validation_ready": True,
                            "all_template_families_validated_review_only": True,
                            "validated_template_family_ids": ["pfkb"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            chain_ligand.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_chain_ligand_acceptor_disambiguation_audit"
                            ),
                            "candidate_feature_id": (
                                "gamma_acceptor_non_catalytic_chain_or_ligand_analog_v0"
                            ),
                            "candidate_feature_status": (
                                "passes_current_review_controls_review_only"
                            ),
                            "current_positive_feature_hit_count": 3,
                            "negative_control_same_chain_block_count": 11,
                            "negative_control_false_hit_count": 0,
                            "external_hard_negative_abstention_row_count": 3,
                            "feature_passes_current_review_controls": True,
                            "feature_admissible_for_production_scoring": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            chain_external.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_chain_ligand_external_hard_negative_feature_screen"
                            ),
                            "candidate_feature_id": (
                                "gamma_acceptor_non_catalytic_chain_or_ligand_analog_v0"
                            ),
                            "review_only_feature_screen_complete": True,
                            "review_only_feature_screen_passed": True,
                            "review_only_external_hard_negative_feature_abstention_count": 3,
                            "review_only_external_hard_negative_feature_non_abstention_count": 0,
                            "clean_heldout_performance_claim_permitted": False,
                            "external_hard_negative_reaudit_scored": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            ligand_policy.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_ligand_analog_policy_blocker_decision"
                            ),
                            "ligand_analog_policy_decision": (
                                "do_not_use_ligand_analog_as_production_acceptor_evidence"
                            ),
                            "ligand_analog_dependency_count": 1,
                            "ligand_analog_dependency_entry_ids": ["m_csa:640"],
                            "ligand_analog_production_admissible_count": 0,
                            "protein_substrate_positive_coverage_gap": True,
                            "feature_admissible_for_production_scoring": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            activation.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_analog_product_state_policy_activation_audit"
                            ),
                            "policy_activation_status": "blocked_review_only",
                            "failed_activation_requirement_count": 2,
                            "diagnostic_control_pass_count": 1,
                            "policy_activation_allowed": False,
                            "production_scoring_admissible": False,
                            "failed_activation_requirement_ids": [
                                "external_hard_negative_scored_reaudit"
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )
            control_reaudit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_analog_product_state_policy_control_reaudit"
                            ),
                            "policy_variant_id": (
                                "analog_product_state_policy_v0_review_only"
                            ),
                            "policy_status": "review_only_reaudit_not_activated",
                            "current_positive_policy_hit_count": 3,
                            "ligand_analog_positive_policy_hit_count": 1,
                            "sibling_control_policy_false_hit_count": 0,
                            "sibling_family_control_reaudit_passed": True,
                            "external_hard_negative_feature_screen_passed": True,
                            "external_hard_negative_feature_non_abstention_count": 0,
                            "failed_activation_requirement_ids": [
                                "external_hard_negative_scored_reaudit"
                            ],
                            "policy_activation_allowed": False,
                            "external_hard_negative_reaudit_scored": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            score_probe.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_review_only_external_hard_negative_score_probe"
                            ),
                            "external_hard_negative_score_probe_row_count": 3,
                            "review_only_score_probe_complete": True,
                            "review_only_score_probe_passed": True,
                            "review_only_score_probe_non_abstention_count": 0,
                            "not_a_real_scored_reaudit": True,
                            "clean_heldout_performance_claim_permitted": False,
                            "external_hard_negative_reaudit_scored": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            fivehvk.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_ligand_specific_5hvk_source_validity_review"
                            ),
                            "pdb_id": "5HVK",
                            "kinase_accession": "P53667",
                            "acceptor_accession": "P23528",
                            "source_validity_status": (
                                "accepted_source_valid_kinase_substrate_cocomplex_review_only"
                            ),
                            "source_validated_kinase_substrate_pair": True,
                            "nearest_source_phosphoacceptor_distance_angstrom": 4.236,
                            "measurement_ready_candidate_count": 1,
                            "ready_to_rerun_controls": True,
                            "ready_to_run_epk_scorer": False,
                            "countable_label_candidate_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            fivehvk_queue.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_ligand_specific_5hvk_control_rerun_queue",
                            "control_rerun_queue_status": (
                                "ready_for_review_only_control_rerun"
                            ),
                            "ready_for_review_only_control_rerun": True,
                            "sibling_control_row_count": 20,
                            "imported_external_hard_negative_row_count": 3,
                            "not_a_real_scored_reaudit": True,
                            "ready_to_run_epk_scorer": False,
                            "epk_score_computed": False,
                            "external_hard_negative_reaudit_scored": False,
                            "countable_label_candidate_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            five_li1.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_m_csa756_5li1_residue_evidence_audit"
                            ),
                            "entry_id": "m_csa:756",
                            "pdb_id": "5LI1",
                            "repair_status": (
                                "blocked_review_only_residue_evidence_lacks_terminal_gamma_atom_no_mapped_acceptor"
                            ),
                            "active_site_residue_evidence_found": True,
                            "terminal_gamma_atom_detected": False,
                            "noncanonical_terminal_atom_names_detected": ["PB"],
                            "noncanonical_terminal_atom_policy_admissible": False,
                            "explicit_residue_source_authority_sufficient": False,
                            "mapped_protein_substrate_acceptor_candidate_count": 0,
                            "measurement_ready_candidate_count": 0,
                            "ready_to_measure_gamma_acceptor_distance": False,
                            "countable_label_candidate_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heteromeric_control.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_heteromeric_source_valid_control_rerun",
                            "control_rerun_status": (
                                "passes_review_only_controls_but_scorer_blocked"
                            ),
                            "positive_like_review_row_count": 7,
                            "heteromeric_source_valid_candidate_row_count": 3,
                            "heteromeric_source_valid_pdb_ids": [
                                "6Z3R",
                                "8OXM",
                                "8OXO",
                            ],
                            "heteromeric_source_valid_unique_pair_ids": [
                                "atm_p53",
                                "smg1_upf1",
                            ],
                            "heteromeric_ambiguous_candidate_count": 2,
                            "heteromeric_rejected_candidate_count": 1,
                            "heteromeric_ambiguous_and_rejected_separated": True,
                            "sibling_control_false_hit_count": 0,
                            "imported_external_hard_negative_non_abstention_count": 0,
                            "source_authority_dependent_positive_like_count": 4,
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heteromeric_gap.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_heteromeric_text_free_axis_gap_audit",
                            "gap_audit_status": (
                                "blocked_review_only_source_free_role_acceptor_axes_missing"
                            ),
                            "source_authority_dependent_positive_like_count": 4,
                            "local_geometry_axis_present_count": 4,
                            "source_free_role_assignment_ready_count": 0,
                            "source_free_acceptor_identity_ready_count": 0,
                            "production_admissible_positive_like_count": 0,
                            "sibling_control_false_hit_count": 0,
                            "imported_external_hard_negative_non_abstention_count": 0,
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heteromeric_probe.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_heteromeric_source_free_role_rule_probe",
                            "source_free_rule_status": (
                                "blocked_review_only_source_free_rule_false_hit_risk"
                            ),
                            "reviewed_candidate_count": 6,
                            "source_free_rule_hit_count": 6,
                            "accepted_rule_hit_count": 3,
                            "ambiguous_rule_hit_count": 2,
                            "rejected_rule_hit_count": 1,
                            "nonaccepted_rule_hit_count": 3,
                            "nonaccepted_rule_hit_pdb_ids": [
                                "7M0T",
                                "7M0W",
                                "8ZN6",
                            ],
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heteromeric_counteraxis.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_acceptor_chain_counteraxis_audit"
                            ),
                            "counteraxis_status": (
                                "passes_current_review_controls_not_scoring_admissible"
                            ),
                            "initial_topology_gamma_rule_hit_count": 6,
                            "retained_source_valid_hit_count": 3,
                            "blocked_nonaccepted_rule_hit_count": 3,
                            "blocked_nonaccepted_rule_hit_pdb_ids": [
                                "7M0T",
                                "7M0W",
                                "8ZN6",
                            ],
                            "residual_nonaccepted_rule_hit_count": 0,
                            "accepted_lost_count": 0,
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heteromeric_broader.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_broader_counteraxis_control_audit"
                            ),
                            "broader_counteraxis_status": (
                                "passes_broader_review_controls_not_scoring_admissible"
                            ),
                            "broader_heteromeric_reviewed_structure_count": 50,
                            "broader_heteromeric_initial_hit_count": 6,
                            "retained_source_valid_hit_count": 3,
                            "blocked_nonaccepted_rule_hit_count": 3,
                            "residual_nonaccepted_rule_hit_count": 0,
                            "accepted_lost_count": 0,
                            "sibling_control_row_count": 36,
                            "sibling_same_chain_hydroxyl_hit_count": 11,
                            "sibling_counteraxis_blocked_hit_count": 11,
                            "sibling_residual_false_hit_count": 0,
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heteromeric_asymmetry.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_ligand_asymmetry_role_audit"
                            ),
                            "role_axis_status": (
                                "passes_current_ligand_asymmetry_role_controls_not_scoring_admissible"
                            ),
                            "retained_source_valid_role_hit_count": 3,
                            "nonaccepted_role_hit_count": 0,
                            "sibling_role_asymmetry_false_hit_count": 0,
                            "source_free_role_assignment_ready_count": 3,
                            "source_free_acceptor_identity_ready_count": 0,
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heteromeric_identity.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_acceptor_identity_gap_audit"
                            ),
                            "acceptor_identity_gap_status": (
                                "blocked_review_only_source_free_acceptor_identity_missing"
                            ),
                            "retained_role_hit_count": 3,
                            "source_context_only_acceptor_identity_count": 3,
                            "source_free_acceptor_identity_ready_count": 0,
                            "candidate_acceptor_residue_codes_review_context": [
                                "SER"
                            ],
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heteromeric_identity_rule.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_acceptor_identity_rule_probe"
                            ),
                            "identity_rule_status": (
                                "passes_current_controls_but_generic_identity_axis_weak_review_only"
                            ),
                            "positive_identity_rule_hit_count": 3,
                            "nonaccepted_blocked_before_identity_rule_count": 3,
                            "nonaccepted_identity_rule_hit_count": 0,
                            "sibling_same_chain_blocked_before_identity_rule_count": 11,
                            "sibling_identity_rule_false_hit_count": 0,
                            "generic_identity_axis_weak": True,
                            "source_free_acceptor_identity_ready_count": 0,
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heteromeric_peptide_identity = root / "heteromeric_peptide_identity.json"
            heteromeric_peptide_identity.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_peptide_acceptor_identity_probe"
                            ),
                            "peptide_identity_axis_status": (
                                "passes_current_controls_peptide_like_acceptor_identity_review_only"
                            ),
                            "positive_peptide_identity_hit_count": 3,
                            "retained_role_hit_count": 3,
                            "nonaccepted_peptide_identity_false_hit_count": 0,
                            "sibling_peptide_identity_false_hit_count": 0,
                            "source_free_acceptor_identity_ready_count": 3,
                            "peptide_identity_axis_narrow": True,
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heteromeric_peptide_external.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_peptide_external_hard_negative_probe"
                            ),
                            "review_only_feature_probe_complete": True,
                            "review_only_feature_probe_passed": True,
                            "review_only_external_hard_negative_feature_non_abstention_count": 0,
                            "missing_expected_external_hard_negative_count": 0,
                            "coordinate_unavailable_external_hard_negative_count": 0,
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                            "external_hard_negative_reaudit_scored": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heteromeric_peptide_stress.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_peptide_broader_stress_audit"
                            ),
                            "stress_audit_status": (
                                "passes_exact_source_query_stress_but_axis_remains_narrow_review_only"
                            ),
                            "exact_source_query_exhausted": True,
                            "exact_source_query_pdb_count": 110,
                            "combined_reviewed_pdb_count": 110,
                            "unreviewed_exact_query_pdb_count": 0,
                            "positive_peptide_identity_hit_count": 3,
                            "positive_non_peptide_substrate_chain_hit_count": 0,
                            "general_substrate_identity_ready_count": 0,
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heteromeric_source_expansion_peptide_role.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_source_expansion_peptide_role_axis_audit"
                            ),
                            "source_expansion_peptide_role_axis_status": (
                                "passes_source_expansion_controls_peptide_role_axis_review_only"
                            ),
                            "source_expansion_controls_passed_review_only": True,
                            "source_valid_expansion_peptide_role_hit_count": 2,
                            "source_valid_expansion_peptide_role_hit_pdb_ids": [
                                "1O6K",
                                "1O6L",
                            ],
                            "source_valid_expansion_peptide_role_miss_count": 0,
                            "nonpositive_source_expansion_control_false_hit_count": 0,
                            "general_substrate_identity_ready_count": 0,
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                            "external_hard_negative_reaudit_scored": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            substrate_mode_gap.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_substrate_mode_gap_audit",
                            "substrate_mode_gap_status": (
                                "passes_review_only_modes_but_unified_substrate_identity_missing"
                            ),
                            "combined_peptide_mode_positive_count": 5,
                            "combined_peptide_mode_positive_pdb_ids": [
                                "1O6K",
                                "1O6L",
                                "6Z3R",
                                "8OXM",
                                "8OXO",
                            ],
                            "combined_peptide_mode_false_hit_count": 0,
                            "peptide_external_hard_negative_non_abstention_count": 0,
                            "protein_substrate_mode_positive_like_count": 3,
                            "protein_substrate_external_hard_negative_non_abstention_count": 0,
                            "peptide_modes_pass_current_controls": True,
                            "protein_mode_passes_current_controls": True,
                            "unified_source_free_substrate_identity_ready": False,
                            "countable_label_candidate_count": 0,
                            "epk_score_computed": False,
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-precount-gate-status",
                    "--epk-text-free-local-axis-prototype",
                    str(axis),
                    "--epk-acceptor-axis-threshold-design",
                    str(threshold),
                    "--epk-gamma-geometry-measurement-sample",
                    str(gamma),
                    "--epk-nonready-ligand-repair-plan",
                    str(repair),
                    "--epk-negative-control-gamma-distance-distribution",
                    str(negative),
                    "--epk-family-specific-mapping-template-review",
                    str(template),
                    "--epk-family-specific-mapping-template-validation-review",
                    str(template_validation),
                    "--epk-chain-ligand-acceptor-disambiguation-audit",
                    str(chain_ligand),
                    "--epk-chain-ligand-external-hard-negative-feature-screen",
                    str(chain_external),
                    "--epk-ligand-analog-policy-blocker-decision",
                    str(ligand_policy),
                    "--epk-analog-product-state-policy-activation-audit",
                    str(activation),
                    "--epk-analog-product-state-policy-control-reaudit",
                    str(control_reaudit),
                    "--epk-review-only-external-hard-negative-score-probe",
                    str(score_probe),
                    "--epk-ligand-specific-5hvk-source-validity-review",
                    str(fivehvk),
                    "--epk-ligand-specific-5hvk-control-rerun-queue",
                    str(fivehvk_queue),
                    "--epk-m-csa756-5li1-residue-evidence-audit",
                    str(five_li1),
                    "--epk-heteromeric-source-valid-control-rerun",
                    str(heteromeric_control),
                    "--epk-heteromeric-text-free-axis-gap-audit",
                    str(heteromeric_gap),
                    "--epk-heteromeric-source-free-role-rule-probe",
                    str(heteromeric_probe),
                    "--epk-heteromeric-acceptor-chain-counteraxis-audit",
                    str(heteromeric_counteraxis),
                    "--epk-heteromeric-broader-counteraxis-control-audit",
                    str(heteromeric_broader),
                    "--epk-heteromeric-ligand-asymmetry-role-audit",
                    str(heteromeric_asymmetry),
                    "--epk-heteromeric-acceptor-identity-gap-audit",
                    str(heteromeric_identity),
                    "--epk-heteromeric-acceptor-identity-rule-probe",
                    str(heteromeric_identity_rule),
                    "--epk-heteromeric-peptide-acceptor-identity-probe",
                    str(heteromeric_peptide_identity),
                    "--epk-heteromeric-peptide-external-hard-negative-probe",
                    str(heteromeric_peptide_external),
                    "--epk-heteromeric-peptide-broader-stress-audit",
                    str(heteromeric_peptide_stress),
                    "--epk-heteromeric-source-expansion-peptide-role-axis-audit",
                    str(heteromeric_source_expansion_peptide_role),
                    "--epk-substrate-mode-gap-audit",
                    str(substrate_mode_gap),
                    "--epk-external-hard-negative-reaudit-plan",
                    str(reaudit),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            status = json.loads(out.read_text(encoding="utf-8"))
            metadata = status["metadata"]
            self.assertEqual(metadata["method"], "epk_precount_gate_status")
            self.assertEqual(metadata["precount_gate_status"], "blocked_review_only")
            self.assertIn("acceptor_threshold_calibrated", metadata["failing_gate_ids"])
            self.assertIn(
                "gamma_geometry_measured_for_all_prototype_rows",
                metadata["failing_gate_ids"],
            )
            self.assertNotIn(
                "family_specific_homolog_mapping_template",
                metadata["failing_gate_ids"],
            )
            self.assertEqual(
                metadata["source_epk_family_specific_mapping_template_review_method"],
                "epk_family_specific_mapping_template_review",
            )
            self.assertEqual(
                metadata[
                    "source_epk_family_specific_mapping_template_validation_review_method"
                ],
                "epk_family_specific_mapping_template_validation_review",
            )
            self.assertEqual(metadata["negative_control_family_template_family_id"], "pfkb")
            self.assertEqual(
                metadata["negative_control_family_template_validated_family_ids"],
                ["pfkb"],
            )
            self.assertTrue(metadata["negative_control_family_template_validation_ready"])
            self.assertEqual(
                metadata[
                    "source_epk_chain_ligand_acceptor_disambiguation_audit_method"
                ],
                "epk_chain_ligand_acceptor_disambiguation_audit",
            )
            self.assertTrue(
                metadata[
                    "chain_ligand_acceptor_feature_passes_current_review_controls"
                ]
            )
            self.assertTrue(metadata["chain_ligand_external_feature_screen_passed"])
            self.assertEqual(
                metadata["source_epk_ligand_analog_policy_blocker_decision_method"],
                "epk_ligand_analog_policy_blocker_decision",
            )
            self.assertEqual(metadata["ligand_analog_dependency_entry_ids"], ["m_csa:640"])
            self.assertEqual(
                metadata[
                    "source_epk_analog_product_state_policy_activation_audit_method"
                ],
                "epk_analog_product_state_policy_activation_audit",
            )
            self.assertFalse(
                metadata[
                    "analog_product_state_policy_activation_audit_allowed"
                ]
            )
            self.assertEqual(
                metadata[
                    "source_epk_analog_product_state_policy_control_reaudit_method"
                ],
                "epk_analog_product_state_policy_control_reaudit",
            )
            self.assertEqual(
                metadata[
                    "source_epk_review_only_external_hard_negative_score_probe_method"
                ],
                "epk_review_only_external_hard_negative_score_probe",
            )
            self.assertEqual(
                metadata["external_hard_negative_score_probe_non_abstention_count"],
                0,
            )
            self.assertEqual(
                metadata[
                    "source_epk_ligand_specific_5hvk_source_validity_review_method"
                ],
                "epk_ligand_specific_5hvk_source_validity_review",
            )
            self.assertTrue(
                metadata["ligand_specific_5hvk_source_validated_kinase_substrate_pair"]
            )
            self.assertEqual(
                metadata[
                    "ligand_specific_5hvk_measurement_ready_candidate_count"
                ],
                1,
            )
            self.assertEqual(
                metadata["ligand_specific_5hvk_control_rerun_queue_status"],
                "ready_for_review_only_control_rerun",
            )
            self.assertTrue(metadata["ligand_specific_5hvk_control_rerun_ready"])
            self.assertEqual(
                metadata["source_epk_m_csa756_5li1_residue_evidence_audit_method"],
                "epk_m_csa756_5li1_residue_evidence_audit",
            )
            self.assertEqual(
                metadata["m_csa756_5li1_noncanonical_terminal_atom_names_detected"],
                ["PB"],
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
                metadata["heteromeric_control_source_valid_pdb_ids"],
                ["6Z3R", "8OXM", "8OXO"],
            )
            self.assertEqual(
                metadata["heteromeric_text_free_axis_gap_audit_status"],
                "blocked_review_only_source_free_role_acceptor_axes_missing",
            )
            self.assertEqual(
                metadata["heteromeric_source_free_nonaccepted_rule_hit_pdb_ids"],
                ["7M0T", "7M0W", "8ZN6"],
            )
            self.assertEqual(
                metadata["heteromeric_acceptor_counteraxis_status"],
                "passes_current_review_controls_not_scoring_admissible",
            )
            self.assertEqual(
                metadata[
                    "heteromeric_acceptor_counteraxis_residual_nonaccepted_hit_count"
                ],
                0,
            )
            self.assertEqual(
                metadata["heteromeric_broader_counteraxis_status"],
                "passes_broader_review_controls_not_scoring_admissible",
            )
            self.assertEqual(
                metadata[
                    "heteromeric_broader_counteraxis_sibling_blocked_hit_count"
                ],
                11,
            )
            self.assertEqual(
                metadata[
                    "heteromeric_broader_counteraxis_sibling_residual_false_hit_count"
                ],
                0,
            )
            self.assertEqual(
                metadata["heteromeric_ligand_asymmetry_role_axis_status"],
                "passes_current_ligand_asymmetry_role_controls_not_scoring_admissible",
            )
            self.assertEqual(
                metadata[
                    "heteromeric_ligand_asymmetry_source_free_role_ready_count"
                ],
                3,
            )
            self.assertEqual(
                metadata[
                    "heteromeric_ligand_asymmetry_source_free_acceptor_identity_ready_count"
                ],
                0,
            )
            self.assertEqual(
                metadata["heteromeric_acceptor_identity_gap_status"],
                "blocked_review_only_source_free_acceptor_identity_missing",
            )
            self.assertEqual(
                metadata["heteromeric_acceptor_identity_gap_source_free_ready_count"],
                0,
            )
            self.assertEqual(
                metadata["heteromeric_acceptor_identity_rule_status"],
                "passes_current_controls_but_generic_identity_axis_weak_review_only",
            )
            self.assertEqual(
                metadata["heteromeric_acceptor_identity_rule_positive_hit_count"],
                3,
            )
            self.assertEqual(
                metadata[
                    "heteromeric_acceptor_identity_rule_nonaccepted_blocked_before_count"
                ],
                3,
            )
            self.assertEqual(
                metadata[
                    "heteromeric_acceptor_identity_rule_sibling_blocked_before_count"
                ],
                11,
            )
            self.assertTrue(
                metadata["heteromeric_acceptor_identity_rule_generic_axis_weak"]
            )
            self.assertEqual(
                metadata["heteromeric_acceptor_identity_rule_source_free_ready_count"],
                0,
            )
            self.assertEqual(
                metadata["heteromeric_peptide_acceptor_identity_status"],
                "passes_current_controls_peptide_like_acceptor_identity_review_only",
            )
            self.assertEqual(
                metadata[
                    "heteromeric_peptide_acceptor_identity_positive_hit_count"
                ],
                3,
            )
            self.assertEqual(
                metadata[
                    "heteromeric_peptide_acceptor_identity_nonaccepted_false_hit_count"
                ],
                0,
            )
            self.assertEqual(
                metadata[
                    "heteromeric_peptide_acceptor_identity_sibling_false_hit_count"
                ],
                0,
            )
            self.assertEqual(
                metadata[
                    "heteromeric_peptide_acceptor_identity_source_free_ready_count"
                ],
                3,
            )
            self.assertTrue(
                metadata["heteromeric_peptide_acceptor_identity_axis_narrow"]
            )
            self.assertTrue(
                metadata["heteromeric_peptide_external_feature_probe_complete"]
            )
            self.assertTrue(
                metadata["heteromeric_peptide_external_feature_probe_passed"]
            )
            self.assertEqual(
                metadata[
                    "heteromeric_peptide_external_feature_non_abstention_count"
                ],
                0,
            )
            self.assertEqual(
                metadata["heteromeric_peptide_broader_stress_audit_status"],
                "passes_exact_source_query_stress_but_axis_remains_narrow_review_only",
            )
            self.assertTrue(
                metadata[
                    "heteromeric_peptide_broader_stress_exact_query_exhausted"
                ]
            )
            self.assertEqual(
                metadata[
                    "heteromeric_peptide_broader_stress_unreviewed_pdb_count"
                ],
                0,
            )
            self.assertEqual(
                metadata[
                    "heteromeric_peptide_broader_stress_general_substrate_ready_count"
                ],
                0,
            )
            self.assertEqual(
                metadata["heteromeric_source_expansion_peptide_role_axis_status"],
                "passes_source_expansion_controls_peptide_role_axis_review_only",
            )
            self.assertTrue(
                metadata["heteromeric_source_expansion_peptide_role_axis_passed"]
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
            self.assertEqual(
                metadata["substrate_mode_gap_status"],
                "passes_review_only_modes_but_unified_substrate_identity_missing",
            )
            self.assertEqual(
                metadata["substrate_mode_gap_combined_peptide_positive_pdb_ids"],
                ["1O6K", "1O6L", "6Z3R", "8OXM", "8OXO"],
            )
            self.assertFalse(
                metadata["substrate_mode_gap_unified_source_free_identity_ready"]
            )
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            checks = {check["gate_id"]: check for check in status["gate_checks"]}
            self.assertTrue(checks["local_axis_prototype"]["passed"])
            self.assertFalse(checks["external_hard_negative_scored_reaudit"]["passed"])
            self.assertFalse(
                checks["gamma_negative_control_distance_distribution"]["passed"]
            )
            self.assertTrue(checks["family_specific_homolog_mapping_template"]["passed"])
            self.assertTrue(
                checks["chain_ligand_acceptor_disambiguation_audit"]["passed"]
            )
            self.assertTrue(
                checks[
                    "chain_ligand_external_hard_negative_feature_screen"
                ]["passed"]
            )
            self.assertTrue(checks["ligand_analog_policy_blocker_decision"]["passed"])
            self.assertTrue(
                checks["analog_product_state_policy_activation_audit"]["passed"]
            )
            self.assertTrue(
                checks["analog_product_state_policy_control_reaudit"]["passed"]
            )
            self.assertTrue(
                checks["review_only_external_hard_negative_score_probe"]["passed"]
            )
            self.assertTrue(
                checks["ligand_specific_5hvk_source_validity_review"]["passed"]
            )
            self.assertTrue(
                checks["ligand_specific_5hvk_control_rerun_queue"]["passed"]
            )
            self.assertTrue(
                checks["m_csa756_5li1_residue_evidence_audit"]["passed"]
            )
            self.assertTrue(
                checks["heteromeric_source_valid_control_rerun"]["passed"]
            )
            self.assertTrue(
                checks["heteromeric_text_free_axis_gap_audit"]["passed"]
            )
            self.assertTrue(
                checks["heteromeric_source_free_role_rule_probe"]["passed"]
            )
            self.assertTrue(
                checks["heteromeric_acceptor_chain_counteraxis_audit"]["passed"]
            )
            self.assertTrue(
                checks["heteromeric_broader_counteraxis_control_audit"]["passed"]
            )
            self.assertTrue(
                checks["heteromeric_ligand_asymmetry_role_audit"]["passed"]
            )
            self.assertTrue(
                checks["heteromeric_acceptor_identity_gap_audit"]["passed"]
            )
            self.assertTrue(
                checks["heteromeric_acceptor_identity_rule_probe"]["passed"]
            )
            self.assertTrue(
                checks["heteromeric_peptide_acceptor_identity_probe"]["passed"]
            )
            self.assertTrue(
                checks[
                    "heteromeric_peptide_external_hard_negative_probe"
                ]["passed"]
            )
            self.assertTrue(
                checks["heteromeric_peptide_broader_stress_audit"]["passed"]
            )
            self.assertTrue(
                checks[
                    "heteromeric_source_expansion_peptide_role_axis_audit"
                ]["passed"]
            )
            self.assertTrue(checks["substrate_mode_gap_audit"]["passed"])

    def test_build_epk_heteromeric_peptide_external_hard_negative_probe_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            peptide = root / "peptide.json"
            external = root / "external.json"
            coordinate = root / "afdb_P78549.cif"
            out = root / "external_probe.json"
            peptide.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_peptide_acceptor_identity_probe"
                            ),
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
                    }
                ),
                encoding="utf-8",
            )
            coordinate.write_text(
                "\n".join(
                    [
                        "data_external",
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
                        "ATOM SER SER OG OG A A 1 1 0.0 0.0 0.0",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            external.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "external_hard_negative_next_candidate_inverse_gate_scores"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "uniprot:P78549",
                                "accession": "P78549",
                                "coordinate_path": str(coordinate),
                                "out_of_scope_inverse_gate": {
                                    "inverse_gate_status": "passed",
                                    "max_current_fingerprint_score": 0.115,
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-heteromeric-peptide-external-hard-negative-probe",
                    "--epk-heteromeric-peptide-acceptor-identity-probe",
                    str(peptide),
                    "--external-hard-negative-inverse-gate-scores",
                    str(external),
                    "--imported-external-entry-ids",
                    "uniprot:P78549",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            probe = json.loads(out.read_text(encoding="utf-8"))
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
            self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
            self.assertEqual(
                probe["rows"][0]["feature_probe_status"],
                "review_only_external_hard_negative_abstain_no_gamma_context",
            )

    def test_build_epk_heteromeric_peptide_broader_stress_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            ligand = root / "ligand.json"
            scout = root / "scout.json"
            peptide = root / "peptide.json"
            out = root / "stress.json"
            ligand.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_ligand_specific_substrate_cocomplex_query_probe"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [{"pdb_id": "1AAA"}],
                    }
                ),
                encoding="utf-8",
            )
            scout.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_positive_coverage_candidate_scout"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "heteromeric_candidate_structure_count": 1,
                        },
                        "rows": [{"pdb_id": "2AAA"}],
                    }
                ),
                encoding="utf-8",
            )
            peptide.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_peptide_acceptor_identity_probe"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "max_peptide_chain_residue_count": 40,
                        },
                        "rows": [
                            {
                                "row_type": (
                                    "heteromeric_peptide_acceptor_identity_candidate"
                                ),
                                "pdb_id": "2AAA",
                                "acceptor_chain_residue_count": 7,
                                "peptide_like_acceptor_identity_rule_hit": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-heteromeric-peptide-broader-stress-audit",
                    "--epk-ligand-specific-substrate-cocomplex-query-probe",
                    str(ligand),
                    "--epk-heteromeric-positive-coverage-candidate-scout",
                    str(scout),
                    "--epk-heteromeric-peptide-acceptor-identity-probe",
                    str(peptide),
                    "--exact-source-query-pdb-ids",
                    "1AAA,2AAA",
                    "--source-query",
                    "fixture exact query",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
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
            self.assertEqual(metadata["unreviewed_exact_query_pdb_count"], 0)
            self.assertEqual(metadata["general_substrate_identity_ready_count"], 0)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_heteromeric_source_expansion_peptide_role_axis_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            peptide = root / "peptide.json"
            external = root / "external.json"
            source_review = root / "source_review.json"
            cif_dir = root / "cifs"
            cif_dir.mkdir()
            out = root / "source_expansion_peptide_role.json"
            peptide.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_peptide_acceptor_identity_probe"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "current_controls_passed_review_only": True,
                        }
                    }
                ),
                encoding="utf-8",
            )
            external.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_peptide_external_hard_negative_probe"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "review_only_feature_probe_passed": True,
                            "review_only_external_hard_negative_feature_non_abstention_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            source_review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_candidate_source_validation_review"
                            )
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
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (cif_dir / "1POS.cif").write_text(
                """
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
""",
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-heteromeric-source-expansion-peptide-role-axis-audit",
                    "--epk-heteromeric-peptide-acceptor-identity-probe",
                    str(peptide),
                    "--epk-heteromeric-peptide-external-hard-negative-probe",
                    str(external),
                    "--epk-heteromeric-source-expansion-source-validation-review",
                    str(source_review),
                    "--max-peptide-chain-residue-count",
                    "2",
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
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
                ["1POS"],
            )
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_substrate_mode_gap_audit_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            peptide = root / "peptide.json"
            source_expansion = root / "source_expansion.json"
            protein = root / "protein.json"
            external = root / "external.json"
            out = root / "substrate_mode_gap.json"
            peptide.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_peptide_acceptor_identity_probe"
                            ),
                            "nonaccepted_control_false_hit_count": 0,
                            "sibling_control_false_hit_count": 0,
                        },
                        "rows": [
                            {
                                "row_type": (
                                    "heteromeric_peptide_acceptor_identity_candidate"
                                ),
                                "pdb_id": "6Z3R",
                                "peptide_like_acceptor_identity_rule_hit": True,
                            },
                            {
                                "row_type": (
                                    "heteromeric_peptide_acceptor_identity_candidate"
                                ),
                                "pdb_id": "8OXM",
                                "peptide_like_acceptor_identity_rule_hit": True,
                            },
                            {
                                "row_type": (
                                    "heteromeric_peptide_acceptor_identity_candidate"
                                ),
                                "pdb_id": "8OXO",
                                "peptide_like_acceptor_identity_rule_hit": True,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            source_expansion.write_text(
                json.dumps(
                    {
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
                    }
                ),
                encoding="utf-8",
            )
            protein.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_5hvk_protein_substrate_axis_generalization_audit"
                            ),
                            "combined_protein_substrate_positive_like_count": 3,
                            "sibling_control_false_hit_count": 0,
                            "imported_external_hard_negative_non_abstention_count": 0,
                            "feature_admissible_for_production_scoring": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            external.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_peptide_external_hard_negative_probe"
                            ),
                            "review_only_external_hard_negative_feature_non_abstention_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-substrate-mode-gap-audit",
                    "--epk-heteromeric-peptide-acceptor-identity-probe",
                    str(peptide),
                    "--epk-heteromeric-source-expansion-peptide-role-axis-audit",
                    str(source_expansion),
                    "--epk-5hvk-protein-substrate-axis-generalization-audit",
                    str(protein),
                    "--epk-heteromeric-peptide-external-hard-negative-probe",
                    str(external),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(metadata["method"], "epk_substrate_mode_gap_audit")
            self.assertEqual(
                metadata["substrate_mode_gap_status"],
                "passes_review_only_modes_but_unified_substrate_identity_missing",
            )
            self.assertEqual(metadata["combined_peptide_mode_positive_count"], 5)
            self.assertFalse(metadata["unified_source_free_substrate_identity_ready"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_unified_substrate_identity_rule_probe_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            substrate_gap = root / "substrate_gap.json"
            peptide = root / "peptide.json"
            source_expansion = root / "source_expansion.json"
            protein = root / "protein.json"
            topology = root / "topology.json"
            external = root / "external.json"
            out = root / "unified.json"
            substrate_gap.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_substrate_mode_gap_audit",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        }
                    }
                ),
                encoding="utf-8",
            )
            peptide.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_peptide_acceptor_identity_probe"
                            )
                        },
                        "rows": [
                            {
                                "row_type": (
                                    "heteromeric_peptide_acceptor_identity_candidate"
                                ),
                                "pdb_id": "6Z3R",
                                "candidate_acceptor_residue_code": "SER",
                                "candidate_acceptor_chain_name": "E",
                                "nearest_gamma_distance_angstrom": 5.6,
                                "peptide_like_acceptor_identity_rule_hit": True,
                                "peptide_like_acceptor_chain": True,
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": (
                                    "heteromeric_nonaccepted_peptide_identity_control"
                                ),
                                "pdb_id": "7M0T",
                                "peptide_like_acceptor_identity_rule_hit": False,
                                "text_free_inputs_only": True,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            source_expansion.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_source_expansion_peptide_role_axis_audit"
                            )
                        },
                        "rows": [
                            {
                                "row_type": (
                                    "source_expansion_peptide_role_positive_candidate"
                                ),
                                "pdb_id": "1O6K",
                                "source_pair_id": "pkb_gsk3",
                                "source_free_peptide_role_axis_rule_hit": True,
                                "source_free_peptide_role_axis_rule_status": (
                                    "source_free_peptide_role_axis_hit_review_only"
                                ),
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": (
                                    "source_expansion_peptide_role_nonpositive_control"
                                ),
                                "pdb_id": "9L3M",
                                "source_free_peptide_role_axis_rule_hit": False,
                                "text_free_inputs_only": True,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            protein.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_protein_substrate_acceptor_candidate_audit"
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "candidate_feature_hit": True,
                                "non_catalytic_chain_acceptor": True,
                                "ligand_analog_acceptor": False,
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:640",
                                "pdb_id": "3TM0",
                                "candidate_feature_hit": False,
                                "non_catalytic_chain_acceptor": False,
                                "ligand_analog_acceptor": True,
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": (
                                    "sibling_family_specific_negative_control"
                                ),
                                "pdb_id": "3R5F",
                                "family_id": "atp_grasp",
                                "candidate_feature_hit": False,
                                "non_catalytic_chain_acceptor": False,
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P06744",
                                "candidate_feature_hit": False,
                                "non_catalytic_chain_acceptor": False,
                                "text_free_inputs_only": True,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            topology.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_heteromeric_chain_topology_signal_audit"
                        },
                        "rows": [
                            {
                                "row_type": "heteromeric_chain_topology_hit_control",
                                "pdb_id": "5HVK",
                                "known_review_context_class": (
                                    "cross_accession_source_valid_positive_like"
                                ),
                                "heteromeric_chain_entity_signal_hit": True,
                                "hit_evaluations": [
                                    {
                                        "nearest_gamma_distance_angstrom": 4.2,
                                    }
                                ],
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": "heteromeric_chain_topology_hit_control",
                                "pdb_id": "3Q4Z",
                                "known_review_context_class": (
                                    "same_accession_phosphosite_control_risk"
                                ),
                                "heteromeric_chain_entity_signal_hit": False,
                                "text_free_inputs_only": True,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            external.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_peptide_external_hard_negative_probe"
                            )
                        },
                        "rows": [
                            {
                                "row_type": (
                                    "imported_external_hard_negative_peptide_identity_probe"
                                ),
                                "entry_id": "uniprot:P06744",
                                "accession": "P06744",
                                "review_only_feature_non_abstention": False,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-unified-substrate-identity-rule-probe",
                    "--epk-substrate-mode-gap-audit",
                    str(substrate_gap),
                    "--epk-heteromeric-peptide-acceptor-identity-probe",
                    str(peptide),
                    "--epk-heteromeric-source-expansion-peptide-role-axis-audit",
                    str(source_expansion),
                    "--epk-protein-substrate-acceptor-candidate-audit",
                    str(protein),
                    "--epk-heteromeric-chain-topology-signal-audit",
                    str(topology),
                    "--epk-heteromeric-peptide-external-hard-negative-probe",
                    str(external),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            probe = json.loads(out.read_text(encoding="utf-8"))
            metadata = probe["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_unified_substrate_identity_rule_probe",
            )
            self.assertEqual(
                metadata["unified_substrate_identity_rule_status"],
                "passes_current_controls_unified_substrate_identity_review_only",
            )
            self.assertEqual(metadata["positive_hit_count"], 4)
            self.assertEqual(metadata["control_false_hit_count"], 0)
            self.assertEqual(
                metadata["external_hard_negative_feature_non_abstention_count"],
                0,
            )
            self.assertEqual(
                metadata["ligand_analog_excluded_positive_entry_ids"],
                ["m_csa:640"],
            )
            five_hvk = [
                row for row in probe["rows"] if row.get("pdb_id") == "5HVK"
            ][0]
            self.assertEqual(
                five_hvk["nearest_gamma_to_acceptor_distance_angstrom"], 4.2
            )
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_general_substrate_identity_gap_audit_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_expansion = root / "source_expansion.json"
            unified = root / "unified.json"
            out = root / "general_identity.json"
            source_expansion.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_source_expansion_peptide_role_axis_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": (
                                    "source_expansion_peptide_role_positive_candidate"
                                ),
                                "pdb_id": "1O6K",
                                "source_pair_id": "pkb_gsk3",
                                "source_validated_positive_like": True,
                                "candidate_acceptor_residue_code": "SER",
                                "candidate_acceptor_chain_name": "C",
                                "gamma_associated_polymer_chain_name": "A",
                                "nearest_gamma_distance_angstrom": 3.5,
                                "acceptor_chain_residue_count": 10,
                                "gamma_chain_residue_count": 317,
                                "peptide_like_acceptor_chain": True,
                                "acceptor_chain_lacks_local_nucleotide_or_metal": True,
                                "gamma_chain_has_local_nucleotide_or_metal": True,
                                "gamma_chain_is_larger_polymer": True,
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": (
                                    "source_expansion_peptide_role_nonpositive_control"
                                ),
                                "pdb_id": "7B56",
                                "source_validated_positive_like": False,
                                "source_validation_status_review_context": (
                                    "blocked_source_context_insufficient_review_only"
                                ),
                                "candidate_acceptor_residue_code": "SER",
                                "candidate_acceptor_chain_name": "A",
                                "gamma_associated_polymer_chain_name": "B",
                                "nearest_gamma_distance_angstrom": 3.9,
                                "acceptor_chain_residue_count": 68,
                                "gamma_chain_residue_count": 303,
                                "peptide_like_acceptor_chain": False,
                                "acceptor_chain_lacks_local_nucleotide_or_metal": True,
                                "gamma_chain_has_local_nucleotide_or_metal": True,
                                "gamma_chain_is_larger_polymer": True,
                                "text_free_inputs_only": True,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            unified.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_unified_substrate_identity_rule_probe",
                            "positive_hit_count": 8,
                            "positive_hit_pdb_ids": ["1O6K"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-general-substrate-identity-gap-audit",
                    "--epk-heteromeric-source-expansion-peptide-role-axis-audit",
                    str(source_expansion),
                    "--epk-unified-substrate-identity-rule-probe",
                    str(unified),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"], "epk_general_substrate_identity_gap_audit"
            )
            self.assertEqual(
                metadata["relaxed_polymer_identity_status"],
                "fails_closed_relaxed_polymer_rule_has_nonpositive_false_hit",
            )
            self.assertEqual(metadata["source_valid_relaxed_polymer_hit_count"], 1)
            self.assertEqual(
                metadata["nonpositive_relaxed_polymer_false_hit_pdb_ids"],
                ["7B56"],
            )
            self.assertEqual(metadata["general_substrate_identity_ready_count"], 0)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])

    def test_build_epk_length_band_substrate_identity_counteraxis_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            general = root / "general_identity.json"
            out = root / "length_band.json"
            general.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_general_substrate_identity_gap_audit",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "relaxed_polymer_identity_status": (
                                "fails_closed_relaxed_polymer_rule_has_nonpositive_false_hit"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": (
                                    "general_substrate_identity_relaxed_polymer_positive_candidate"
                                ),
                                "pdb_id": "1O6K",
                                "source_pair_id": "pkb_gsk3",
                                "source_validated_positive_like": True,
                                "candidate_acceptor_residue_code": "SER",
                                "candidate_acceptor_chain_name": "C",
                                "gamma_associated_polymer_chain_name": "A",
                                "nearest_gamma_distance_angstrom": 3.5,
                                "acceptor_chain_residue_count": 10,
                                "gamma_chain_residue_count": 317,
                                "relaxed_polymer_acceptor_identity_rule_hit": True,
                            },
                            {
                                "row_type": (
                                    "general_substrate_identity_relaxed_polymer_nonpositive_control"
                                ),
                                "pdb_id": "7B56",
                                "source_validated_positive_like": False,
                                "source_validation_status_review_context": (
                                    "blocked_source_context_insufficient_review_only"
                                ),
                                "candidate_acceptor_residue_code": "SER",
                                "candidate_acceptor_chain_name": "A",
                                "gamma_associated_polymer_chain_name": "B",
                                "nearest_gamma_distance_angstrom": 3.9,
                                "acceptor_chain_residue_count": 68,
                                "gamma_chain_residue_count": 303,
                                "relaxed_polymer_acceptor_identity_rule_hit": True,
                            },
                            {
                                "row_type": (
                                    "general_substrate_identity_relaxed_polymer_nonpositive_control"
                                ),
                                "pdb_id": "2JJ2",
                                "source_validated_positive_like": False,
                                "acceptor_chain_residue_count": 479,
                                "gamma_chain_residue_count": 466,
                                "relaxed_polymer_acceptor_identity_rule_hit": False,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-length-band-substrate-identity-counteraxis-audit",
                    "--epk-general-substrate-identity-gap-audit",
                    str(general),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_length_band_substrate_identity_counteraxis_audit",
            )
            self.assertEqual(
                metadata["length_band_identity_status"],
                "passes_source_expansion_subset_by_blocking_relaxed_false_hits_review_only",
            )
            self.assertEqual(metadata["positive_like_length_band_hit_count"], 1)
            self.assertEqual(metadata["nonpositive_length_band_false_hit_count"], 0)
            self.assertEqual(
                metadata[
                    "nonpositive_relaxed_false_hit_blocked_by_length_band_pdb_ids"
                ],
                ["7B56"],
            )
            self.assertEqual(metadata["general_substrate_identity_ready_count"], 0)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])

    def test_build_epk_length_band_external_hard_negative_review_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            length_band = root / "length_band.json"
            external = root / "external_probe.json"
            out = root / "length_band_external.json"
            length_band.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_length_band_substrate_identity_counteraxis_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "length_band_identity_status": (
                                "passes_source_expansion_subset_by_blocking_relaxed_false_hits_review_only"
                            ),
                        },
                        "rows": [],
                    }
                ),
                encoding="utf-8",
            )
            external.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_review_only_external_hard_negative_score_probe"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "expected_external_hard_negative_entry_ids": [
                                "uniprot:P06744",
                                "uniprot:P78549",
                                "uniprot:Q3LXA3",
                            ],
                        },
                        "rows": [
                            {
                                "row_type": "imported_external_hard_negative_score_probe",
                                "entry_id": entry_id,
                                "review_only_probe_score": 0.0,
                                "review_only_score_probe_non_abstention": False,
                            }
                            for entry_id in [
                                "uniprot:P06744",
                                "uniprot:P78549",
                                "uniprot:Q3LXA3",
                            ]
                        ],
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-length-band-external-hard-negative-review",
                    "--epk-length-band-substrate-identity-counteraxis-audit",
                    str(length_band),
                    "--epk-review-only-external-hard-negative-score-probe",
                    str(external),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"], "epk_length_band_external_hard_negative_review"
            )
            self.assertEqual(
                metadata["length_band_external_hard_negative_review_status"],
                "passes_review_only_length_band_external_hard_negative_abstention",
            )
            self.assertEqual(
                metadata["length_band_external_hard_negative_non_abstention_count"],
                0,
            )
            self.assertEqual(metadata["external_hard_negative_review_row_count"], 3)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["external_hard_negative_reaudit_scored"])

    def test_build_epk_source_free_protein_substrate_role_discriminator_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            protein = root / "protein.json"
            topology = root / "topology.json"
            length_band = root / "length_band.json"
            out = root / "protein_role.json"
            protein.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_protein_substrate_acceptor_candidate_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "candidate_feature_hit": True,
                                "non_catalytic_chain_acceptor": True,
                                "ligand_analog_acceptor": False,
                                "nearest_gamma_to_candidate_acceptor_distance_angstrom": (
                                    3.61
                                ),
                            },
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:246",
                                "pdb_id": "1IR3",
                                "candidate_feature_hit": True,
                                "non_catalytic_chain_acceptor": True,
                                "ligand_analog_acceptor": False,
                                "nearest_gamma_to_candidate_acceptor_distance_angstrom": (
                                    5.082
                                ),
                            },
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:640",
                                "pdb_id": "3TM0",
                                "candidate_feature_hit": False,
                                "non_catalytic_chain_acceptor": False,
                                "ligand_analog_acceptor": True,
                                "nearest_gamma_to_candidate_acceptor_distance_angstrom": (
                                    3.558
                                ),
                            },
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P06744",
                                "candidate_feature_hit": False,
                                "non_catalytic_chain_acceptor": False,
                                "ligand_analog_acceptor": False,
                            },
                            {
                                "row_type": (
                                    "sibling_family_specific_negative_control"
                                ),
                                "pdb_id": "3R5F",
                                "family_id": "atp_grasp",
                                "candidate_feature_hit": False,
                                "non_catalytic_chain_acceptor": False,
                                "ligand_analog_acceptor": False,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            topology.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_heteromeric_chain_topology_signal_audit",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "heteromeric_chain_topology_hit_control",
                                "pdb_id": "5HVK",
                                "known_review_context_class": (
                                    "cross_accession_source_valid_positive_like"
                                ),
                                "heteromeric_chain_entity_signal_hit": True,
                            },
                            {
                                "row_type": "heteromeric_chain_topology_hit_control",
                                "pdb_id": "3Q4Z",
                                "known_review_context_class": (
                                    "same_accession_phosphosite_control_risk"
                                ),
                                "heteromeric_chain_entity_signal_hit": False,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            length_band.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_length_band_substrate_identity_counteraxis_audit"
                            ),
                            "positive_like_length_band_hit_count": 2,
                            "nonpositive_relaxed_false_hit_blocked_by_length_band_count": 1,
                        },
                        "rows": [],
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-source-free-protein-substrate-role-discriminator-audit",
                    "--epk-protein-substrate-acceptor-candidate-audit",
                    str(protein),
                    "--epk-heteromeric-chain-topology-signal-audit",
                    str(topology),
                    "--epk-length-band-substrate-identity-counteraxis-audit",
                    str(length_band),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_source_free_protein_substrate_role_discriminator_audit",
            )
            self.assertEqual(
                metadata["protein_substrate_role_discriminator_status"],
                "passes_current_controls_but_review_only_not_production_admissible",
            )
            self.assertEqual(
                metadata["combined_protein_substrate_role_hit_pdb_ids"],
                ["1IR3", "2PHK", "5HVK"],
            )
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
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_build_epk_source_free_protein_substrate_role_discriminator_stress_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            protein_role = root / "protein_role.json"
            source_expansion = root / "source_expansion.json"
            out = root / "protein_role_stress.json"
            protein_role.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_source_free_protein_substrate_role_discriminator_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "protein_substrate_role_discriminator_status": (
                                "passes_current_controls_but_review_only_not_production_admissible"
                            ),
                        },
                        "rows": [],
                    }
                ),
                encoding="utf-8",
            )
            source_expansion.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_source_expansion_peptide_role_axis_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": (
                                    "source_expansion_peptide_role_positive_candidate"
                                ),
                                "pdb_id": "1O6K",
                                "source_validated_positive_like": True,
                                "source_free_peptide_role_axis_rule_hit": True,
                                "peptide_like_acceptor_chain": True,
                                "acceptor_chain_lacks_local_nucleotide_or_metal": True,
                                "gamma_chain_has_local_nucleotide_or_metal": True,
                                "gamma_chain_is_larger_polymer": True,
                            },
                            {
                                "row_type": (
                                    "source_expansion_peptide_role_nonpositive_control"
                                ),
                                "pdb_id": "7B56",
                                "source_validated_positive_like": False,
                                "source_free_peptide_role_axis_rule_hit": False,
                                "peptide_like_acceptor_chain": False,
                                "acceptor_chain_lacks_local_nucleotide_or_metal": True,
                                "gamma_chain_has_local_nucleotide_or_metal": True,
                                "gamma_chain_is_larger_polymer": True,
                            },
                            {
                                "row_type": (
                                    "source_expansion_peptide_role_nonpositive_control"
                                ),
                                "pdb_id": "9L3M",
                                "source_validated_positive_like": False,
                                "source_free_peptide_role_axis_rule_hit": False,
                                "peptide_like_acceptor_chain": False,
                                "acceptor_chain_lacks_local_nucleotide_or_metal": False,
                                "gamma_chain_has_local_nucleotide_or_metal": True,
                                "gamma_chain_is_larger_polymer": False,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-source-free-protein-substrate-role-discriminator-stress-audit",
                    "--epk-source-free-protein-substrate-role-discriminator-audit",
                    str(protein_role),
                    "--epk-heteromeric-source-expansion-peptide-role-axis-audit",
                    str(source_expansion),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_source_free_protein_substrate_role_discriminator_stress_audit",
            )
            self.assertEqual(
                metadata["protein_role_source_expansion_stress_status"],
                "fails_closed_review_only_source_expansion_protein_role_false_hit",
            )
            self.assertEqual(
                metadata[
                    "nonpositive_source_expansion_protein_role_false_hit_pdb_ids"
                ],
                ["7B56"],
            )
            self.assertEqual(
                metadata["source_valid_expansion_peptide_mode_not_protein_pdb_ids"],
                ["1O6K"],
            )
            self.assertFalse(metadata["protein_discriminator_generalization_ready"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["epk_score_computed"])
            self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_build_epk_midlength_protein_role_counteraxis_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            stress = root / "protein_role_stress.json"
            source_valid = root / "source_valid_distance.json"
            out = root / "midlength.json"
            stress.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_source_free_protein_substrate_role_discriminator_stress_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
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
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            source_valid.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_source_valid_candidate_gamma_distance_sample"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "pdb_id": "6Z3R",
                                "source_pair_id": "smg1_upf1",
                                "source_validated_positive_like": True,
                                "measurement_status": (
                                    "source_valid_heteromeric_gamma_distance_measured_review_only"
                                ),
                                "distance_candidates": [
                                    {
                                        "candidate_chain_name": "E",
                                        "gamma_associated_polymer_chain_name": "M",
                                        "acceptor_chain_residue_count": 7,
                                        "nearest_gamma_distance_angstrom": 5.607,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-midlength-protein-role-counteraxis-audit",
                    "--epk-source-free-protein-substrate-role-discriminator-stress-audit",
                    str(stress),
                    "--epk-heteromeric-source-valid-candidate-gamma-distance-sample",
                    str(source_valid),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"], "epk_midlength_protein_role_counteraxis_audit"
            )
            self.assertEqual(metadata["blocked_midlength_false_hit_pdb_ids"], ["7B56"])
            self.assertEqual(
                metadata["source_valid_short_or_peptide_mode_pdb_ids"], ["6Z3R"]
            )
            self.assertEqual(metadata["source_valid_protein_role_retained_count"], 0)
            self.assertFalse(metadata["protein_discriminator_generalization_ready"])
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
            self.assertEqual(metadata["countable_label_candidate_count"], 0)

    def test_build_epk_unified_review_only_scoring_prototype_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            unified = root / "unified.json"
            prior = root / "prior.json"
            out = root / "unified_score.json"
            unified.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_unified_substrate_identity_rule_probe",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "rule_id": (
                                "epk_unified_polymer_substrate_identity_rule_v0_review_only"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": (
                                    "unified_identity_current_peptide_positive"
                                ),
                                "pdb_id": "6Z3R",
                                "substrate_mode": "short_peptide_substrate",
                                "unified_substrate_identity_rule_hit": True,
                                "nearest_gamma_to_acceptor_distance_angstrom": 5.6,
                                "acceptor_chain_lacks_local_nucleotide_or_metal": True,
                                "peptide_like_acceptor_chain": True,
                                "ligand_analog_acceptor": False,
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": "unified_identity_peptide_control",
                                "pdb_id": "7M0T",
                                "substrate_mode": "peptide_mode_control",
                                "unified_substrate_identity_rule_hit": False,
                                "nearest_gamma_to_acceptor_distance_angstrom": 3.8,
                                "peptide_like_acceptor_chain": False,
                                "ligand_analog_acceptor": False,
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": (
                                    "unified_identity_imported_external_hard_negative"
                                ),
                                "entry_id": "uniprot:P06744",
                                "substrate_mode": "imported_external_hard_negative",
                                "unified_substrate_identity_rule_hit": False,
                                "ligand_analog_acceptor": False,
                                "text_free_inputs_only": True,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            prior.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "epk_review_only_scoring_prototype"},
                        "rows": [
                            {
                                "row_type": (
                                    "sibling_family_specific_negative_control"
                                ),
                                "pdb_id": "1ABC",
                                "family_id": "pfkb",
                                "prototype_decision": (
                                    "blocked_by_family_specific_sibling_counteraxis_review_only"
                                ),
                                "prototype_axis_values": {
                                    "family_specific_sibling_counteraxis": 1
                                },
                                "text_free_inputs_only": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-unified-review-only-scoring-prototype",
                    "--epk-unified-substrate-identity-rule-probe",
                    str(unified),
                    "--epk-review-only-scoring-prototype",
                    str(prior),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            prototype = json.loads(out.read_text(encoding="utf-8"))
            metadata = prototype["metadata"]
            self.assertEqual(
                metadata["method"], "epk_unified_review_only_scoring_prototype"
            )
            self.assertEqual(metadata["prototype_gate_status"], "fail_closed_review_only")
            self.assertTrue(metadata["prototype_passes_current_controls"])
            self.assertEqual(metadata["positive_like_full_score_count"], 1)
            self.assertEqual(metadata["current_control_false_non_abstention_count"], 0)
            self.assertEqual(
                metadata["imported_external_hard_negative_non_abstention_count"], 0
            )
            self.assertEqual(metadata["legacy_sibling_counteraxis_row_count"], 1)
            self.assertTrue(metadata["review_only_score_computed"])
            self.assertFalse(metadata["epk_score_computed"])

    def test_build_epk_unified_prototype_broad_stress_audit_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype = root / "prototype.json"
            stress = root / "stress.json"
            scout = root / "scout.json"
            review = root / "review.json"
            out = root / "broad_stress.json"
            prototype.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_unified_review_only_scoring_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "prototype_passes_current_controls": True,
                            "positive_like_full_score_count": 1,
                            "current_control_false_non_abstention_count": 0,
                            "imported_external_hard_negative_non_abstention_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            stress.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_heteromeric_peptide_broader_stress_audit",
                            "combined_reviewed_pdb_count": 10,
                            "unreviewed_exact_query_pdb_count": 0,
                            "exact_source_query_exhausted": True,
                            "positive_non_peptide_substrate_chain_hit_count": 0,
                            "nonaccepted_peptide_identity_false_hit_count": 0,
                            "sibling_peptide_identity_false_hit_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            scout.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_heteromeric_positive_coverage_candidate_scout",
                            "reviewed_candidate_count": 2,
                            "fetch_failure_count": 0,
                            "heteromeric_candidate_structure_count": 1,
                            "heteromeric_candidate_pdb_ids": ["9L3M"],
                            "positive_coverage_status": (
                                "source_validation_pending_for_broadened_heteromeric_candidates_review_only"
                            ),
                        }
                    }
                ),
                encoding="utf-8",
            )
            review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_heteromeric_candidate_source_validation_review"
                        },
                        "rows": [
                            {
                                "pdb_id": "9L3M",
                                "source_validation_status": (
                                    "blocked_source_context_insufficient_review_only"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-unified-prototype-broad-stress-audit",
                    "--epk-unified-review-only-scoring-prototype",
                    str(prototype),
                    "--epk-heteromeric-peptide-broader-stress-audit",
                    str(stress),
                    "--epk-heteromeric-source-expansion-candidate-scout",
                    str(scout),
                    "--epk-heteromeric-source-expansion-source-validation-review",
                    str(review),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"], "epk_unified_prototype_broad_stress_audit"
            )
            self.assertEqual(
                metadata["broad_stress_status"],
                "bounded_stress_has_source_validation_counterexamples_review_only",
            )
            self.assertEqual(metadata["outside_query_reviewed_candidate_count"], 2)
            self.assertEqual(metadata["outside_query_heteromeric_candidate_hit_count"], 1)
            self.assertEqual(
                metadata["source_validation_blocked_or_rejected_pdb_ids"], ["9L3M"]
            )
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])

    def test_build_epk_unified_prototype_next_broad_stress_preregistration_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            stress = root / "stress.json"
            out = root / "prereg.json"
            stress.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_unified_prototype_broad_stress_audit",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "source_validation_blocked_or_rejected_pdb_ids": [
                                "9L3M"
                            ],
                            "source_validated_positive_like_pdb_ids": ["1O6K"],
                            "outside_query_heteromeric_candidate_pdb_ids": [
                                "1O6K",
                                "9L3M",
                            ],
                        },
                        "rows": [
                            {
                                "row_type": "outside_query_source_validation_row",
                                "pdb_id": "9L3M",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-unified-prototype-next-broad-stress-preregistration",
                    "--epk-unified-prototype-broad-stress-audit",
                    str(stress),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            preregistration = json.loads(out.read_text(encoding="utf-8"))
            metadata = preregistration["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_unified_prototype_next_broad_stress_preregistration",
            )
            self.assertEqual(
                metadata["preregistration_status"],
                "active_review_only_next_broad_stress_tranche_preregistered",
            )
            self.assertEqual(metadata["known_counterexample_pdb_ids"], ["9L3M"])
            self.assertEqual(metadata["source_validated_positive_like_pdb_ids"], ["1O6K"])
            self.assertEqual(metadata["lane_count"], 3)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])

    def test_build_epk_acceptor_identity_review_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            gamma = root / "gamma.json"
            graph = root / "graph.json"
            out = root / "acceptor_identity.json"
            gamma.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_geometry_measurement_sample",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "measured_row_count": 1,
                            "gamma_phosphate_geometry_measured": True,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "pdb_id": "2PHK",
                                "measurement_status": (
                                    "gamma_to_hydroxyl_distance_measured_review_only"
                                ),
                                "distance_rows": [
                                    {
                                        "gamma_ligand_code": "ATP",
                                        "gamma_atom_name": "PG",
                                        "hydroxyl_residue_code": "SER",
                                        "hydroxyl_atom_name": "OG",
                                        "hydroxyl_chain_name": "B",
                                        "hydroxyl_resid": "5",
                                        "distance_angstrom": 3.6,
                                    }
                                ],
                            },
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "pdb_id": "1L8T",
                                "measurement_status": (
                                    "product_or_missing_gamma_nucleotide_skipped"
                                ),
                                "distance_rows": [],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "v1_graph"},
                        "nodes": [
                            {
                                "id": "m_csa:35:mechanism:1",
                                "type": "mechanism_text",
                                "text": (
                                    "Asp149 deprotonates the protein substrate "
                                    "hydroxyl group for attack on the "
                                    "gamma-phosphate of ATP."
                                ),
                            },
                            {
                                "id": "m_csa:35:residue:1",
                                "type": "catalytic_residue",
                                "structure_positions": [
                                    {"chain_name": "A", "resid": 136}
                                ],
                            },
                            {
                                "id": "m_csa:640:mechanism:1",
                                "type": "mechanism_text",
                                "text": (
                                    "Nucleophilic attack on the gamma phosphate "
                                    "of ATP by the 3' or 5' OH group of the "
                                    "substrate."
                                ),
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-acceptor-identity-review",
                    "--epk-gamma-geometry-measurement-sample",
                    str(gamma),
                    "--graph",
                    str(graph),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(metadata["method"], "epk_acceptor_identity_review")
            self.assertEqual(
                metadata["measured_acceptor_identity_source_supported_count"],
                1,
            )
            self.assertTrue(metadata["measured_acceptor_identity_review_complete"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            rows = {row["entry_id"]: row for row in review["rows"]}
            self.assertEqual(
                rows["m_csa:35"]["acceptor_identity_review_status"],
                "measured_acceptor_identity_source_supported_review_only",
            )
            self.assertTrue(
                rows["m_csa:35"]["nearest_measured_hydroxyl"][
                    "on_non_catalytic_chain"
                ]
            )
            self.assertEqual(
                rows["m_csa:640"]["acceptor_identity_review_status"],
                "source_acceptor_supported_gamma_geometry_missing",
            )
            self.assertFalse(rows["m_csa:35"]["epk_score_computed"])

    def test_build_epk_atp_state_evidence_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            identity = root / "identity.json"
            graph = root / "graph.json"
            geometry = root / "geometry.json"
            cif_dir = root / "cif"
            cif_dir.mkdir()
            out = root / "atp_state.json"
            identity.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_acceptor_identity_review",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "pdb_id": "1BBB",
                                "acceptor_identity_review_status": (
                                    "source_acceptor_supported_gamma_geometry_missing"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "v1_graph"},
                        "nodes": [
                            {
                                "id": "m_csa:640",
                                "type": "m_csa_entry",
                                "reference_uniprot_id": "PTEST",
                            },
                            {
                                "id": "m_csa:640:residue:1",
                                "type": "catalytic_residue",
                                "sequence_positions": [
                                    {
                                        "uniprot_id": "PTEST",
                                        "resid": 44,
                                        "code": "Lys",
                                    }
                                ],
                            }
                        ],
                        "edges": [
                            {
                                "source": "m_csa:640",
                                "target": "uniprot:PTEST",
                                "predicate": "has_reference_protein",
                            },
                            {
                                "source": "uniprot:PTEST",
                                "target": "pdb:1AAA",
                                "predicate": "has_structure",
                            },
                            {
                                "source": "uniprot:PTEST",
                                "target": "pdb:1BBB",
                                "predicate": "has_structure",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "active_site_geometry_features"},
                        "entries": [
                            {
                                "entry_id": "m_csa:640",
                                "pdb_id": "1BBB",
                                "ligand_context": {
                                    "structure_ligand_codes": ["ADP", "KAN"]
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (cif_dir / "1AAA.cif").write_text(
                "\n".join(
                    [
                        "data_1AAA",
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
                        "HETATM 1 P PG ATP A 1 0.0 0.0 0.0 PG ATP A 1",
                        "HETATM 2 C C1 KAN B 1 1.0 0.0 0.0 C1 KAN B 1",
                        "HETATM 3 O O1 KAN B 1 2.0 0.0 0.0 O1 KAN B 1",
                        "ATOM 4 N NZ LYS A 44 3.0 0.0 0.0 NZ LYS A 44",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            (cif_dir / "1BBB.cif").write_text(
                "\n".join(
                    [
                        "data_1BBB",
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
                        "HETATM 1 P PB ADP A 1 0.0 0.0 0.0 PB ADP A 1",
                        "HETATM 2 C C1 KAN B 1 1.0 0.0 0.0 C1 KAN B 1",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-atp-state-evidence-plan",
                    "--epk-acceptor-identity-review",
                    str(identity),
                    "--graph",
                    str(graph),
                    "--geometry",
                    str(geometry),
                    "--entry-ids",
                    "m_csa:640",
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            plan = json.loads(out.read_text(encoding="utf-8"))
            metadata = plan["metadata"]
            self.assertEqual(metadata["method"], "epk_atp_state_evidence_plan")
            self.assertEqual(metadata["candidate_atp_state_acceptor_row_count"], 1)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            row = plan["rows"][0]
            self.assertEqual(
                row["atp_state_evidence_status"],
                "candidate_atp_state_acceptor_structure_found_review_only",
            )
            self.assertEqual(row["gamma_capable_acceptor_candidate_structure_count"], 1)
            self.assertEqual(
                row["alternate_gamma_acceptor_geometry_measured_structure_count"],
                1,
            )
            self.assertEqual(
                metadata["gamma_capable_residue_mapped_candidate_structure_count"],
                1,
            )
            self.assertEqual(
                metadata["alternate_gamma_acceptor_geometry_measured_count"],
                1,
            )
            self.assertFalse(row["epk_score_computed"])

    def test_build_epk_gamma_threshold_control_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            gamma = root / "gamma.json"
            identity = root / "identity.json"
            atp_state = root / "atp_state.json"
            threshold = root / "threshold.json"
            out = root / "threshold_control.json"
            gamma.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_geometry_measurement_sample",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "pdb_id": "2PHK",
                                "measurement_status": (
                                    "gamma_to_hydroxyl_distance_measured_review_only"
                                ),
                                "distance_rows": [
                                    {
                                        "gamma_ligand_code": "ATP",
                                        "gamma_atom_name": "PG",
                                        "hydroxyl_residue_code": "SER",
                                        "hydroxyl_atom_name": "OG",
                                        "hydroxyl_chain_name": "B",
                                        "hydroxyl_resid": "5",
                                        "distance_angstrom": 3.6,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            identity.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "epk_acceptor_identity_review"},
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "acceptor_identity_review_status": (
                                    "measured_acceptor_identity_source_supported_review_only"
                                ),
                                "acceptor_identity_source_supported": True,
                            },
                            {
                                "entry_id": "m_csa:640",
                                "acceptor_identity_review_status": (
                                    "source_acceptor_supported_gamma_geometry_missing"
                                ),
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            atp_state.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "epk_atp_state_evidence_plan"},
                        "rows": [
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "candidate_structures": [
                                    {
                                        "pdb_id": "3TM0",
                                        "current_selected_structure": False,
                                        "nearest_gamma_to_acceptor_like_oxygen_distance_angstrom": 3.5,
                                        "nearest_gamma_acceptor_atom_pair": {
                                            "gamma_ligand_code": "ANP",
                                            "gamma_atom_name": "PG",
                                            "acceptor_ligand_code": "B31",
                                            "acceptor_atom_name": "O14",
                                            "acceptor_chain_name": "A",
                                            "acceptor_resid": "305",
                                        },
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            threshold.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_acceptor_axis_threshold_design",
                            "candidate_thresholds_angstrom": [3.0, 4.0, 6.0],
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-gamma-threshold-control-plan",
                    "--epk-gamma-geometry-measurement-sample",
                    str(gamma),
                    "--epk-acceptor-identity-review",
                    str(identity),
                    "--epk-atp-state-evidence-plan",
                    str(atp_state),
                    "--epk-acceptor-axis-threshold-design",
                    str(threshold),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            plan = json.loads(out.read_text(encoding="utf-8"))
            metadata = plan["metadata"]
            self.assertEqual(metadata["method"], "epk_gamma_threshold_control_plan")
            self.assertEqual(metadata["row_count"], 2)
            self.assertEqual(
                metadata["lowest_review_geometry_covering_candidate_angstrom"],
                4.0,
            )
            self.assertTrue(metadata["threshold_control_plan_ready"])
            self.assertIsNone(metadata["selected_threshold_angstrom"])
            self.assertFalse(metadata["threshold_calibrated"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertEqual(metadata["control_requirement_count"], 4)
            rows = {row["entry_id"]: row for row in plan["rows"]}
            self.assertEqual(
                rows["m_csa:640"]["geometry_scope"],
                "alternate_graph_linked_structure",
            )
            self.assertFalse(rows["m_csa:640"]["epk_score_computed"])

    def test_build_epk_m_csa640_alternate_gamma_geometry_review_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            atp_state = root / "atp_state.json"
            threshold = root / "threshold.json"
            out = root / "m_csa640_review.json"
            atp_state.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_atp_state_evidence_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "candidate_structures": [
                                    {
                                        "pdb_id": "3TM0",
                                        "has_gamma_capable_nucleotide": True,
                                        "has_acceptor_like_ligand": True,
                                        "all_catalytic_residues_mapped": True,
                                        "mapped_catalytic_residue_count": 4,
                                        "expected_catalytic_residue_count": 4,
                                        "nearest_gamma_to_acceptor_like_oxygen_distance_angstrom": 3.5,
                                        "nearest_gamma_acceptor_atom_pair": {
                                            "gamma_ligand_code": "ANP",
                                            "gamma_atom_name": "PG",
                                            "acceptor_ligand_code": "B31",
                                            "acceptor_atom_name": "O14",
                                            "acceptor_chain_name": "A",
                                            "acceptor_resid": "305",
                                        },
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            threshold.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_threshold_control_plan"
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:640",
                                "pdb_id": "3TM0",
                                "source_support_status": (
                                    "source_supported_alternate_analog_context_review_only"
                                ),
                                "acceptor_ligand_or_residue_code": "B31",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-m-csa640-alternate-gamma-geometry-review",
                    "--epk-atp-state-evidence-plan",
                    str(atp_state),
                    "--epk-gamma-threshold-control-plan",
                    str(threshold),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_m_csa640_alternate_gamma_geometry_review",
            )
            self.assertEqual(
                metadata["alternate_gamma_geometry_supports_positive_axis_count"],
                1,
            )
            self.assertFalse(metadata["epk_score_computed"])
            row = review["rows"][0]
            self.assertEqual(row["pdb_id"], "3TM0")
            self.assertEqual(row["acceptor_ligand_code"], "B31")
            self.assertTrue(
                row["alternate_gamma_geometry_supports_positive_axis_review_only"]
            )
            self.assertFalse(row["production_scoring_admissible"])

    def test_build_epk_negative_control_gamma_distance_distribution_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            threshold = root / "threshold_control.json"
            family = root / "family_expansion.json"
            geometry = root / "geometry.json"
            cif_dir = root / "cif"
            cif_dir.mkdir()
            out = root / "negative_controls.json"
            threshold.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_threshold_control_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "candidate_thresholds_angstrom": [4.0, 6.0, 8.0],
                            "lowest_review_geometry_covering_candidate_angstrom": 6.0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            family.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "atp_phosphoryl_transfer_family_expansion"
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "family_id": "epk",
                            },
                            {
                                "entry_id": "m_csa:615",
                                "entry_name": "deoxyguanosine kinase",
                                "family_id": "dnk",
                                "family_name": "Deoxynucleoside kinases",
                                "decision_action": "reject_label",
                            },
                            {
                                "entry_id": "m_csa:643",
                                "entry_name": "acetate kinase",
                                "family_id": "askha",
                                "family_name": "ASKHA sugar and acetate kinases",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {"max_entries": 1000},
                        "entries": [
                            {
                                "entry_id": "m_csa:615",
                                "pdb_id": "2OCP",
                                "status": "ok",
                                "ligand_context": {
                                    "ligand_codes": ["DTP"],
                                    "structure_ligand_codes": ["DTP"],
                                },
                                "pocket_context": {
                                    "nearby_residue_sites": [
                                        {
                                            "code": "SER",
                                            "chain_name": "A",
                                            "resid": "52",
                                        }
                                    ]
                                },
                            },
                            {
                                "entry_id": "m_csa:643",
                                "pdb_id": "1G99",
                                "status": "ok",
                                "ligand_context": {
                                    "structure_ligand_codes": ["ADP"]
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (cif_dir / "pdb_2OCP.cif").write_text(
                "\n".join(
                    [
                        "data_2OCP",
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
                        "HETATM 1 P PG DTP A 1 0.0 0.0 0.0 PG DTP A 1",
                        "ATOM 2 O OG SER A 52 3.0 4.0 0.0 OG SER A 52",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-negative-control-gamma-distance-distribution",
                    "--epk-gamma-threshold-control-plan",
                    str(threshold),
                    "--atp-phosphoryl-transfer-family-expansion",
                    str(family),
                    "--geometry",
                    str(geometry),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            distribution = json.loads(out.read_text(encoding="utf-8"))
            metadata = distribution["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_negative_control_gamma_distance_distribution",
            )
            self.assertEqual(metadata["source_control_row_count"], 2)
            self.assertEqual(metadata["measured_control_count"], 1)
            self.assertFalse(metadata["negative_control_distance_distribution_ready"])
            self.assertEqual(
                metadata["lowest_covering_candidate_negative_control_hit_count"],
                1,
            )
            rows = {row["entry_id"]: row for row in distribution["rows"]}
            self.assertNotIn("m_csa:35", rows)
            self.assertEqual(
                rows["m_csa:615"]["measurement_status"],
                "selected_structure_gamma_to_hydroxyl_distance_measured_review_only",
            )
            self.assertEqual(
                rows["m_csa:615"]["nearest_gamma_to_hydroxyl_distance_angstrom"],
                5.0,
            )
            self.assertEqual(
                rows["m_csa:643"]["measurement_status"],
                "selected_structure_product_or_no_gamma_nucleotide_skipped",
            )
            self.assertFalse(rows["m_csa:615"]["epk_score_computed"])

    def test_build_epk_sibling_negative_control_alternate_structure_plan_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            distribution = root / "negative_controls.json"
            family = root / "family_expansion.json"
            graph = root / "graph.json"
            cif_dir = root / "cif"
            cif_dir.mkdir()
            out = root / "alternate_controls.json"
            distribution.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_negative_control_gamma_distance_distribution"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "control_row_count": 2,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:592",
                                "entry_name": "glucokinase",
                                "family_id": "askha",
                                "family_name": "ASKHA sugar and acetate kinases",
                                "pdb_id": "1AAA",
                                "measurement_status": (
                                    "selected_structure_product_or_no_gamma_nucleotide_skipped"
                                ),
                            },
                            {
                                "entry_id": "m_csa:615",
                                "entry_name": "deoxyguanosine kinase",
                                "family_id": "dnk",
                                "measurement_status": (
                                    "selected_structure_gamma_to_hydroxyl_distance_measured_review_only"
                                ),
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            family.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "atp_phosphoryl_transfer_family_expansion"
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:592",
                                "entry_name": "glucokinase",
                                "family_id": "askha",
                            },
                            {
                                "entry_id": "m_csa:615",
                                "entry_name": "deoxyguanosine kinase",
                                "family_id": "dnk",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "v1_graph"},
                        "nodes": [
                            {
                                "id": "m_csa:592",
                                "type": "m_csa_entry",
                                "reference_uniprot_id": "PTEST",
                            },
                            {
                                "id": "m_csa:592:residue:1",
                                "type": "catalytic_residue",
                                "sequence_positions": [
                                    {
                                        "uniprot_id": "PTEST",
                                        "resid": 44,
                                        "code": "Lys",
                                    }
                                ],
                            },
                        ],
                        "edges": [
                            {
                                "source": "m_csa:592",
                                "target": "uniprot:PTEST",
                                "predicate": "has_reference_protein",
                            },
                            {
                                "source": "uniprot:PTEST",
                                "target": "pdb:1AAA",
                                "predicate": "has_structure",
                            },
                            {
                                "source": "uniprot:PTEST",
                                "target": "pdb:1AAB",
                                "predicate": "has_structure",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (cif_dir / "pdb_1AAB.cif").write_text(
                "\n".join(
                    [
                        "data_1AAB",
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
                        "HETATM 1 P PG ATP A 1 0.0 0.0 0.0 PG ATP A 1",
                        "HETATM 2 MG MG MG A 2 1.0 0.0 0.0 MG MG A 2",
                        "ATOM 3 N NZ LYS A 44 2.0 0.0 0.0 NZ LYS A 44",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-sibling-negative-control-alternate-structure-plan",
                    "--epk-negative-control-gamma-distance-distribution",
                    str(distribution),
                    "--atp-phosphoryl-transfer-family-expansion",
                    str(family),
                    "--graph",
                    str(graph),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            plan = json.loads(out.read_text(encoding="utf-8"))
            metadata = plan["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_sibling_negative_control_alternate_structure_plan",
            )
            self.assertEqual(metadata["source_unmeasured_control_row_count"], 1)
            self.assertEqual(metadata["ready_for_future_distance_measurement_count"], 1)
            self.assertEqual(metadata["alternate_gamma_metal_mapped_structure_count"], 1)
            self.assertFalse(metadata["negative_control_distance_distribution_ready"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            rows = {row["entry_id"]: row for row in plan["rows"]}
            self.assertEqual(set(rows), {"m_csa:592"})
            self.assertEqual(
                rows["m_csa:592"]["alternate_control_evidence_status"],
                "alternate_gamma_metal_mapped_candidate_found_review_only",
            )
            self.assertFalse(rows["m_csa:592"]["epk_score_computed"])
            self.assertFalse(rows["m_csa:592"]["countable_label_candidate"])

    def test_build_epk_sibling_negative_control_alternate_gamma_distance_sample_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            plan = root / "alternate_controls.json"
            cif_dir = root / "cif"
            cif_dir.mkdir()
            out = root / "alternate_distances.json"
            plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_negative_control_alternate_structure_plan"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "ready_for_future_distance_measurement_count": 1,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:592",
                                "entry_name": "glucokinase",
                                "family_id": "askha",
                                "family_name": "ASKHA sugar and acetate kinases",
                                "source_selected_measurement_status": (
                                    "selected_structure_product_or_no_gamma_nucleotide_skipped"
                                ),
                                "candidate_structures": [
                                    {
                                        "pdb_id": "1AAB",
                                        "target_ligand_codes": ["ANP", "MG"],
                                        "has_gamma_capable_nucleotide": True,
                                        "has_metal_ligand": True,
                                        "all_catalytic_residues_mapped": True,
                                        "mapped_catalytic_residue_count": 1,
                                        "expected_catalytic_residue_count": 1,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (cif_dir / "pdb_1AAB.cif").write_text(
                "\n".join(
                    [
                        "data_1AAB",
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
                        "HETATM 1 P PG ANP A 1 0.0 0.0 0.0 PG ANP A 1",
                        "HETATM 2 MG MG MG A 2 1.0 0.0 0.0 MG MG A 2",
                        "ATOM 3 O OG SER A 52 3.0 4.0 0.0 OG SER A 52",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-sibling-negative-control-alternate-gamma-distance-sample",
                    "--epk-sibling-negative-control-alternate-structure-plan",
                    str(plan),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            sample = json.loads(out.read_text(encoding="utf-8"))
            metadata = sample["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_sibling_negative_control_alternate_gamma_distance_sample",
            )
            self.assertEqual(metadata["candidate_structure_count"], 1)
            self.assertEqual(metadata["measured_candidate_structure_count"], 1)
            self.assertFalse(metadata["negative_control_distance_distribution_ready"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            row = sample["rows"][0]
            self.assertEqual(
                row["measurement_status"],
                "alternate_gamma_to_hydroxyl_distance_measured_review_only",
            )
            self.assertEqual(
                row["nearest_gamma_to_hydroxyl_distance_angstrom"],
                5.0,
            )
            self.assertEqual(row["candidate_threshold_hits_angstrom"], [6.0, 8.0])
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_negative_control_calibration_sufficiency_decision_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            distribution = root / "selected_distribution.json"
            alternate = root / "alternate_sample.json"
            out = root / "sufficiency.json"
            distribution.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_negative_control_gamma_distance_distribution"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "candidate_thresholds_angstrom": [4.0, 6.0, 8.0],
                            "lowest_review_geometry_covering_candidate_angstrom": 6.0,
                            "control_family_ids": ["askha", "dnk"],
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:615",
                                "entry_name": "deoxyguanosine kinase",
                                "family_id": "dnk",
                                "pdb_id": "1ABC",
                                "measurement_status": (
                                    "selected_structure_gamma_to_hydroxyl_distance_measured_review_only"
                                ),
                                "nearest_gamma_to_hydroxyl_distance_angstrom": 3.2,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_negative_control_alternate_gamma_distance_sample"
                            ),
                            "candidate_thresholds_angstrom": [4.0, 6.0, 8.0],
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:592",
                                "entry_name": "glucokinase",
                                "family_id": "askha",
                                "pdb_id": "3FGU",
                                "measurement_status": (
                                    "alternate_gamma_to_hydroxyl_distance_measured_review_only"
                                ),
                                "nearest_gamma_to_hydroxyl_distance_angstrom": 4.2,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-negative-control-calibration-sufficiency-decision",
                    "--epk-negative-control-gamma-distance-distribution",
                    str(distribution),
                    "--epk-sibling-negative-control-alternate-gamma-distance-sample",
                    str(alternate),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            decision = json.loads(out.read_text(encoding="utf-8"))
            metadata = decision["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_negative_control_calibration_sufficiency_decision",
            )
            self.assertEqual(metadata["combined_measured_control_count"], 2)
            self.assertEqual(metadata["combined_measured_family_count"], 2)
            self.assertEqual(
                metadata["calibration_sufficiency_status"],
                "blocked_review_only",
            )
            self.assertEqual(
                metadata["threshold_calibration_decision"],
                "do_not_select_threshold",
            )
            self.assertFalse(metadata["threshold_calibrated"])
            self.assertFalse(metadata["epk_score_computed"])
            collisions = {
                row["threshold_angstrom"]: row
                for row in metadata["threshold_collision_rows"]
            }
            self.assertEqual(collisions[6.0]["combined_negative_control_hit_count"], 2)
            self.assertEqual(len(decision["rows"]), 2)

    def test_build_epk_missing_sibling_control_source_request_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sufficiency = root / "sufficiency.json"
            distribution = root / "distribution.json"
            alternate_plan = root / "alternate_plan.json"
            out = root / "source_request.json"
            sufficiency.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_negative_control_calibration_sufficiency_decision"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "combined_measured_family_ids": ["askha", "dnk"],
                            "missing_sibling_family_ids": ["atp_grasp", "pfkb"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            distribution.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_negative_control_gamma_distance_distribution"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:310",
                                "entry_name": "D-alanine ligase",
                                "family_id": "atp_grasp",
                                "family_name": "ATP-grasp ligases",
                                "pdb_id": "1E4E",
                                "measurement_status": (
                                    "selected_structure_product_or_no_gamma_nucleotide_skipped"
                                ),
                            },
                            {
                                "entry_id": "m_csa:663",
                                "entry_name": "ribokinase",
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "pdb_id": "1RK2",
                                "measurement_status": (
                                    "selected_structure_product_or_no_gamma_nucleotide_skipped"
                                ),
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate_plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_negative_control_alternate_structure_plan"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:310",
                                "entry_name": "D-alanine ligase",
                                "family_id": "atp_grasp",
                                "family_name": "ATP-grasp ligases",
                                "selected_pdb_id": "1E4E",
                                "alternate_control_evidence_status": (
                                    "no_alternate_pdb_structure_screened"
                                ),
                                "graph_linked_alternate_pdb_count": 0,
                                "screened_alternate_pdb_count": 0,
                                "candidate_structures": [],
                            },
                            {
                                "entry_id": "m_csa:663",
                                "entry_name": "ribokinase",
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "selected_pdb_id": "1RK2",
                                "alternate_control_evidence_status": (
                                    "alternate_gamma_structure_found_metal_or_mapping_gap"
                                ),
                                "graph_linked_alternate_pdb_count": 1,
                                "screened_alternate_pdb_count": 1,
                                "alternate_gamma_structure_count": 1,
                                "alternate_gamma_metal_mapped_structure_count": 0,
                                "candidate_structures": [
                                    {
                                        "pdb_id": "1RKA",
                                        "target_ligand_codes": ["ANP"],
                                        "has_gamma_capable_nucleotide": True,
                                        "has_metal_ligand": False,
                                        "mapped_catalytic_residue_count": 1,
                                        "expected_catalytic_residue_count": 2,
                                        "all_catalytic_residues_mapped": False,
                                    }
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-missing-sibling-control-source-request",
                    "--epk-negative-control-calibration-sufficiency-decision",
                    str(sufficiency),
                    "--epk-negative-control-gamma-distance-distribution",
                    str(distribution),
                    "--epk-sibling-negative-control-alternate-structure-plan",
                    str(alternate_plan),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            request = json.loads(out.read_text(encoding="utf-8"))
            metadata = request["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_missing_sibling_control_source_request",
            )
            self.assertEqual(metadata["missing_sibling_family_count"], 2)
            self.assertEqual(metadata["row_count"], 2)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            rows = {row["entry_id"]: row for row in request["rows"]}
            self.assertEqual(
                rows["m_csa:310"]["source_request_type"],
                "source_graph_linked_or_external_pdb_structure",
            )
            self.assertEqual(
                rows["m_csa:663"]["source_request_type"],
                "repair_gamma_structure_metal_or_mapping_gap",
            )
            self.assertEqual(
                rows["m_csa:663"]["candidate_structure_summaries"][0][
                    "structure_gap_status"
                ],
                "gamma_capable_metal_or_mapping_gap",
            )

    def test_build_epk_sibling_control_repair_review_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_request = root / "source_request.json"
            alternate_plan = root / "alternate_plan.json"
            out = root / "repair_review.json"
            (root / "1GQT.cif").write_text(
                "\n".join(
                    [
                        "data_1GQT",
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
                        "HETATM ACP ACP PG PG A A 1 1 0.0 0.0 0.0",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            source_request.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_missing_sibling_control_source_request",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:663",
                                "entry_name": "ribokinase",
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "source_request_type": (
                                    "repair_gamma_structure_metal_or_mapping_gap"
                                ),
                                "selected_pdb_id": "1RK2",
                                "reference_uniprot_id": "P0A9J6",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate_plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_negative_control_alternate_structure_plan"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:663",
                                "entry_name": "ribokinase",
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "selected_pdb_id": "1RK2",
                                "reference_uniprot_id": "P0A9J6",
                                "candidate_structures": [
                                    {
                                        "pdb_id": "1GQT",
                                        "target_ligand_codes": ["ACP"],
                                        "has_gamma_capable_nucleotide": True,
                                        "has_product_or_partial_nucleotide": False,
                                        "has_metal_ligand": False,
                                        "mapped_catalytic_residue_count": 4,
                                        "expected_catalytic_residue_count": 4,
                                        "all_catalytic_residues_mapped": True,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-sibling-control-repair-review",
                    "--epk-missing-sibling-control-source-request",
                    str(source_request),
                    "--epk-sibling-negative-control-alternate-structure-plan",
                    str(alternate_plan),
                    "--family-id",
                    "pfkb",
                    "--cif-dir",
                    str(root),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(metadata["method"], "epk_sibling_control_repair_review")
            self.assertEqual(metadata["reviewed_family_id"], "pfkb")
            self.assertEqual(metadata["family_repair_review_status"], "blocked_review_only")
            self.assertEqual(metadata["mapped_gamma_structure_count"], 1)
            self.assertEqual(metadata["metal_supported_gamma_structure_count"], 0)
            self.assertEqual(metadata["measurement_ready_repaired_structure_count"], 0)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = review["rows"][0]
            self.assertEqual(
                row["repair_review_status"],
                "mapping_verified_metal_context_unresolved",
            )
            self.assertEqual(
                row["candidate_structure_reviews"][0]["repair_assessment_status"],
                "mapping_verified_metal_context_unresolved",
            )
            self.assertEqual(
                row["candidate_structure_reviews"][0]["observed_metal_ligand_codes"],
                [],
            )

    def test_build_epk_missing_sibling_control_post_repair_source_decision_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_request = root / "source_request.json"
            repair_review = root / "repair_review.json"
            out = root / "post_repair_decision.json"
            source_request.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_missing_sibling_control_source_request",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "missing_sibling_family_ids": ["pfkb"],
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:663",
                                "entry_name": "ribokinase",
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "source_request_type": (
                                    "repair_gamma_structure_metal_or_mapping_gap"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            repair_review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_sibling_control_repair_review",
                            "reviewed_family_id": "pfkb",
                            "family_repair_review_status": "blocked_review_only",
                            "measurement_ready_repaired_structure_count": 0,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:663",
                                "family_id": "pfkb",
                                "repair_review_status": (
                                    "mapping_verified_metal_context_unresolved"
                                ),
                                "candidate_structure_review_count": 1,
                                "measurement_ready_structure_count": 0,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-missing-sibling-control-post-repair-source-decision",
                    "--epk-missing-sibling-control-source-request",
                    str(source_request),
                    "--epk-sibling-control-repair-review",
                    str(repair_review),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            decision = json.loads(out.read_text(encoding="utf-8"))
            metadata = decision["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_missing_sibling_control_post_repair_source_decision",
            )
            self.assertEqual(metadata["reviewed_sibling_family_ids"], ["pfkb"])
            self.assertEqual(
                metadata["post_repair_source_decision_counts"],
                {"external_or_homolog_source_needed": 1},
            )
            self.assertEqual(metadata["source_escalation_required_entry_count"], 1)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = decision["rows"][0]
            self.assertEqual(
                row["post_repair_source_decision"],
                "external_or_homolog_source_needed",
            )
            self.assertIn("metal-supported", row["next_source_evidence_needed"])

    def test_build_epk_sibling_control_homolog_source_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            post_repair = root / "post_repair.json"
            out = root / "homolog_source_plan.json"
            (root / "9PFY.cif").write_text(
                "\n".join(
                    [
                        "data_9PFY",
                        "_struct.title 'Crystal structure of nucleoside-diphosphate kinase with ATP'",
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
                        "HETATM ATP ATP PG PG A A 1 1 0.0 0.0 0.0",
                        "HETATM MG MG MG MG A A 2 2 1.0 0.0 0.0",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            post_repair.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_missing_sibling_control_post_repair_source_decision"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:637",
                                "family_id": "ndk",
                                "post_repair_source_decision": (
                                    "external_or_homolog_source_needed"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-sibling-control-homolog-source-plan",
                    "--epk-missing-sibling-control-post-repair-source-decision",
                    str(post_repair),
                    "--family-id",
                    "ndk",
                    "--candidate-pdb-ids",
                    "9PFY",
                    "--candidate-source-query",
                    "RCSB title phrase NDK plus ATP and MG",
                    "--cif-dir",
                    str(root),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            plan = json.loads(out.read_text(encoding="utf-8"))
            metadata = plan["metadata"]
            self.assertEqual(
                metadata["method"], "epk_sibling_control_homolog_source_plan"
            )
            self.assertEqual(metadata["reviewed_sibling_family_id"], "ndk")
            self.assertEqual(metadata["source_entry_ids"], ["m_csa:637"])
            self.assertEqual(metadata["candidate_pdb_count"], 1)
            self.assertEqual(metadata["metal_supported_gamma_candidate_count"], 1)
            self.assertEqual(metadata["measurement_ready_homolog_structure_count"], 0)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = plan["rows"][0]
            self.assertEqual(
                row["source_candidate_status"],
                "candidate_gamma_metal_source_review_only",
            )
            self.assertEqual(row["catalytic_mapping_status"], "not_mapped_review_pending")
            self.assertFalse(row["measurement_ready_for_negative_control"])

    def test_build_epk_sibling_control_homolog_mapping_review_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_plan = root / "source_plan.json"
            out = root / "homolog_mapping_review.json"
            (root / "9PFY.cif").write_text(
                "\n".join(
                    [
                        "data_9PFY",
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
                        "HETATM ATP ATP PG PG A A 201 201 0.0 0.0 0.0",
                        "HETATM MG MG MG MG A A 202 202 1.0 0.0 0.0",
                        "ATOM HIS HIS ND1 ND1 A A 139 139 3.0 0.0 0.0",
                        "ATOM LYS LYS NZ NZ A A 34 34 3.5 0.2 0.0",
                        "ATOM ARG ARG NH1 NH1 A A 126 126 3.7 0.0 0.0",
                        "ATOM ASN ASN OD1 OD1 A A 136 136 4.0 0.1 0.0",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            source_plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_sibling_control_homolog_source_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "reviewed_sibling_family_id": "ndk",
                            "candidate_pdb_count": 1,
                        },
                        "rows": [
                            {
                                "pdb_id": "9PFY",
                                "family_id": "ndk",
                                "family_name": "Nucleoside diphosphate kinases",
                                "source_entry_ids": ["m_csa:637"],
                                "source_candidate_status": (
                                    "candidate_gamma_metal_source_review_only"
                                ),
                                "has_gamma_capable_nucleotide": True,
                                "has_metal_ligand": True,
                                "gamma_capable_nucleotide_codes": ["ATP"],
                                "metal_ligand_codes": ["MG"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-sibling-control-homolog-mapping-review",
                    "--epk-sibling-control-homolog-source-plan",
                    str(source_plan),
                    "--family-id",
                    "ndk",
                    "--cif-dir",
                    str(root),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"], "epk_sibling_control_homolog_mapping_review"
            )
            self.assertEqual(metadata["reviewed_sibling_family_id"], "ndk")
            self.assertEqual(metadata["mapping_reviewed_candidate_count"], 1)
            self.assertEqual(metadata["catalytic_histidine_mapped_candidate_count"], 1)
            self.assertEqual(metadata["nucleotide_site_mapped_candidate_count"], 1)
            self.assertEqual(metadata["measurement_ready_homolog_structure_count"], 1)
            self.assertFalse(metadata["calibration_distance_measured"])
            self.assertFalse(metadata["epk_score_computed"])
            row = review["rows"][0]
            self.assertEqual(
                row["homolog_mapping_status"],
                "homolog_mapping_ready_for_distance_measurement_review_only",
            )
            self.assertTrue(row["measurement_ready_for_negative_control"])
            self.assertFalse(row["negative_control_distance_distribution_ready"])
            self.assertEqual(row["chain_mappings"][0]["chain_id"], "A")

    def test_build_epk_family_specific_mapping_template_review_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            geometry_features = root / "geometry_features.json"
            mapping_review = root / "homolog_mapping_review.json"
            out = root / "template_review.json"
            geometry_features.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "geometry_fixture"},
                        "entries": [
                            {
                                "entry_id": "m_csa:663",
                                "entry_name": "ribokinase",
                                "pdb_id": "1RK2",
                                "residues": [
                                    {
                                        "code": "Asp",
                                        "chain_name": "A",
                                        "resid": 255,
                                        "roles": ["proton acceptor"],
                                        "residue_node_id": "m_csa:663:residue:4",
                                    },
                                    {
                                        "code": "Gly",
                                        "chain_name": "A",
                                        "resid": 254,
                                        "roles": ["electrostatic stabiliser"],
                                        "residue_node_id": "m_csa:663:residue:3",
                                    },
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            mapping_review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_sibling_control_homolog_mapping_review",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "reviewed_sibling_family_id": "pfkb",
                            "mapping_reviewed_candidate_count": 1,
                            "homolog_mapping_status_counts": {
                                "homolog_catalytic_histidine_mapping_unresolved": 1
                            },
                            "catalytic_histidine_mapped_candidate_count": 0,
                            "nucleotide_site_mapped_candidate_count": 1,
                            "measurement_ready_homolog_structure_count": 0,
                        },
                        "rows": [{"source_entry_ids": ["m_csa:663"]}],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-family-specific-mapping-template-review",
                    "--geometry-features",
                    str(geometry_features),
                    "--epk-sibling-control-homolog-mapping-review",
                    str(mapping_review),
                    "--family-id",
                    "pfkb",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"], "epk_family_specific_mapping_template_review"
            )
            self.assertEqual(metadata["reviewed_sibling_family_id"], "pfkb")
            self.assertEqual(metadata["seeded_template_entry_count"], 1)
            self.assertEqual(metadata["template_residue_count"], 2)
            self.assertEqual(metadata["source_mapping_review_histidine_mapped_count"], 0)
            self.assertEqual(metadata["source_mapping_review_nucleotide_site_mapped_count"], 1)
            self.assertFalse(metadata["family_specific_mapping_ready"])
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = review["rows"][0]
            self.assertEqual(row["entry_id"], "m_csa:663")
            self.assertFalse(row["template_ready_for_automated_mapping"])
            self.assertFalse(row["template_can_be_used_for_distance_measurement"])
            self.assertEqual(
                row["template_residues"][0]["template_role"],
                "acid_base_or_acceptor_seed",
            )

    def test_build_epk_family_specific_homolog_mapping_and_distance_commands(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_plan = root / "source_plan.json"
            template_review = root / "template_review.json"
            mapping_out = root / "family_mapping_review.json"
            distance_out = root / "family_distance_sample.json"
            (root / "PFB1.cif").write_text(
                "\n".join(
                    [
                        "data_PFB1",
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
                        "HETATM ATP ATP PG PG A A 300 300 0.0 0.0 0.0",
                        "HETATM MG MG MG MG A A 301 301 3.0 0.0 0.0",
                        "ATOM ASP ASP OD1 OD1 A A 126 126 5.0 0.0 0.0",
                        "ATOM GLY GLY CA CA A A 122 122 6.0 0.0 0.0",
                        "ATOM LYS LYS NZ NZ A A 121 121 5.6 0.0 0.0",
                        "ATOM THR THR OG1 OG1 A A 191 191 6.1 0.0 0.0",
                        "ATOM ALA ALA CA CA A A 124 124 7.0 0.0 0.0",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            source_plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_sibling_control_homolog_source_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "reviewed_sibling_family_id": "pfkb",
                            "candidate_pdb_count": 1,
                        },
                        "rows": [
                            {
                                "pdb_id": "PFB1",
                                "family_id": "pfkb",
                                "family_name": "PfkB family kinases",
                                "source_entry_ids": ["m_csa:663"],
                                "source_candidate_status": (
                                    "candidate_gamma_metal_source_review_only"
                                ),
                                "has_gamma_capable_nucleotide": True,
                                "has_metal_ligand": True,
                                "gamma_capable_nucleotide_codes": ["ATP"],
                                "metal_ligand_codes": ["MG"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            template_review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_family_specific_mapping_template_review",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "reviewed_sibling_family_id": "pfkb",
                            "template_review_status": (
                                "template_seeded_mapping_algorithm_pending_review_only"
                            ),
                            "seeded_template_entry_count": 1,
                            "template_residue_count": 4,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:663",
                                "family_id": "pfkb",
                                "template_residues": [
                                    {
                                        "residue_code": "Asp",
                                        "template_role": "acid_base_or_acceptor_seed",
                                    },
                                    {
                                        "residue_code": "Gly",
                                        "template_role": (
                                            "phosphate_or_transition_state_stabilizer_seed"
                                        ),
                                    },
                                    {
                                        "residue_code": "Lys",
                                        "template_role": (
                                            "phosphate_or_transition_state_stabilizer_seed"
                                        ),
                                    },
                                    {
                                        "residue_code": "Ala",
                                        "template_role": (
                                            "phosphate_or_transition_state_stabilizer_seed"
                                        ),
                                    },
                                    {
                                        "residue_code": "Thr",
                                        "template_role": "metal_ligand_seed",
                                    },
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-family-specific-homolog-mapping-review",
                    "--epk-sibling-control-homolog-source-plan",
                    str(source_plan),
                    "--epk-family-specific-mapping-template-review",
                    str(template_review),
                    "--family-id",
                    "pfkb",
                    "--cif-dir",
                    str(root),
                    "--out",
                    str(mapping_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            mapping_review = json.loads(mapping_out.read_text(encoding="utf-8"))
            metadata = mapping_review["metadata"]
            self.assertEqual(
                metadata["method"], "epk_family_specific_homolog_mapping_review"
            )
            self.assertEqual(metadata["reviewed_sibling_family_id"], "pfkb")
            self.assertEqual(metadata["measurement_ready_homolog_structure_count"], 1)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = mapping_review["rows"][0]
            self.assertEqual(
                row["family_specific_homolog_mapping_status"],
                "family_specific_homolog_mapping_ready_for_distance_measurement_review_only",
            )
            self.assertTrue(row["measurement_ready_for_negative_control"])
            self.assertFalse(
                row["chain_mappings"][0]["exact_residue_position_transfer_used"]
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-family-specific-homolog-gamma-distance-sample",
                    "--epk-family-specific-homolog-mapping-review",
                    str(mapping_out),
                    "--candidate-thresholds",
                    "4,6,8",
                    "--cif-dir",
                    str(root),
                    "--out",
                    str(distance_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            sample = json.loads(distance_out.read_text(encoding="utf-8"))
            sample_meta = sample["metadata"]
            self.assertEqual(
                sample_meta["method"],
                "epk_family_specific_homolog_gamma_distance_sample",
            )
            self.assertEqual(sample_meta["measured_homolog_structure_count"], 1)
            self.assertFalse(sample_meta["negative_control_distance_distribution_ready"])
            self.assertFalse(sample_meta["epk_score_computed"])
            sample_row = sample["rows"][0]
            self.assertEqual(
                sample_row["measurement_status"],
                "family_specific_gamma_to_acid_base_distance_measured_review_only",
            )
            self.assertEqual(
                sample_row["nearest_gamma_to_family_acid_base_distance_angstrom"],
                5.0,
            )

    def test_build_epk_family_specific_mapping_template_validation_review_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            template = root / "template.json"
            mapping = root / "mapping.json"
            distance = root / "distance.json"
            blocked_distance = root / "blocked_distance.json"
            out = root / "validation.json"
            blocked_out = root / "blocked_validation.json"
            template.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_family_specific_mapping_template_review",
                            "reviewed_sibling_family_id": "pfkb",
                            "reviewed_sibling_family_name": "PfkB family kinases",
                            "template_review_status": (
                                "template_seeded_mapping_algorithm_pending_review_only"
                            ),
                            "family_specific_mapping_ready": False,
                            "seeded_template_entry_count": 1,
                            "template_residue_count": 4,
                        }
                    }
                ),
                encoding="utf-8",
            )
            mapping.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_family_specific_homolog_mapping_review"
                            ),
                            "reviewed_sibling_family_id": "pfkb",
                            "reviewed_sibling_family_name": "PfkB family kinases",
                            "measurement_ready_homolog_structure_count": 1,
                        }
                    }
                ),
                encoding="utf-8",
            )
            distance.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_family_specific_homolog_gamma_distance_sample"
                            ),
                            "reviewed_sibling_family_id": "pfkb",
                            "reviewed_sibling_family_name": "PfkB family kinases",
                            "measured_homolog_structure_count": 1,
                        }
                    }
                ),
                encoding="utf-8",
            )
            blocked_distance.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_family_specific_homolog_gamma_distance_sample"
                            ),
                            "reviewed_sibling_family_id": "pfkb",
                            "reviewed_sibling_family_name": "PfkB family kinases",
                            "measured_homolog_structure_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-family-specific-mapping-template-validation-review",
                    "--epk-family-specific-mapping-template-review",
                    str(template),
                    "--epk-family-specific-homolog-mapping-review",
                    str(mapping),
                    "--epk-family-specific-homolog-gamma-distance-sample",
                    str(distance),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_family_specific_mapping_template_validation_review",
            )
            self.assertTrue(metadata["template_validation_ready"])
            self.assertEqual(metadata["validated_template_family_ids"], ["pfkb"])
            self.assertEqual(metadata["validated_template_family_count"], 1)
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            self.assertEqual(metadata["countable_label_candidate_count"], 0)
            row = review["rows"][0]
            self.assertTrue(row["validated_by_downstream_mapping"])
            self.assertFalse(row["countable_label_candidate"])

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-family-specific-mapping-template-validation-review",
                    "--epk-family-specific-mapping-template-review",
                    str(template),
                    "--epk-family-specific-homolog-mapping-review",
                    str(mapping),
                    "--epk-family-specific-homolog-gamma-distance-sample",
                    str(blocked_distance),
                    "--out",
                    str(blocked_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            blocked = json.loads(blocked_out.read_text(encoding="utf-8"))
            blocked_metadata = blocked["metadata"]
            self.assertFalse(blocked_metadata["template_validation_ready"])
            self.assertEqual(blocked_metadata["validated_template_family_ids"], [])
            self.assertEqual(
                blocked["rows"][0]["validation_status"],
                "template_validation_blocked_review_only",
            )

    def test_build_epk_sibling_control_homolog_gamma_distance_sample_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            mapping_review = root / "homolog_mapping_review.json"
            out = root / "homolog_distance_sample.json"
            (root / "9PFY.cif").write_text(
                "\n".join(
                    [
                        "data_9PFY",
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
                        "HETATM ATP ATP PG PG A A 201 201 0.0 0.0 0.0",
                        "HETATM MG MG MG MG A A 202 202 1.0 0.0 0.0",
                        "ATOM HIS HIS ND1 ND1 A A 139 139 3.0 0.0 0.0",
                        "ATOM HIS HIS NE2 NE2 A A 139 139 3.4 0.0 0.0",
                        "ATOM SER SER OG OG A A 45 45 6.5 0.0 0.0",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            mapping_review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_sibling_control_homolog_mapping_review",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "reviewed_sibling_family_id": "ndk",
                            "ready_for_future_distance_measurement_count": 1,
                        },
                        "rows": [
                            {
                                "pdb_id": "9PFY",
                                "family_id": "ndk",
                                "family_name": "Nucleoside diphosphate kinases",
                                "source_entry_ids": ["m_csa:637"],
                                "measurement_ready_for_negative_control": True,
                                "gamma_capable_nucleotide_codes": ["ATP"],
                                "metal_ligand_codes": ["MG"],
                                "mapped_chain_count": 1,
                                "chain_mappings": [
                                    {
                                        "chain_id": "A",
                                        "gamma_ligand_code": "ATP",
                                        "gamma_atom_name": "PG",
                                        "gamma_ligand_auth_seq_id": "201",
                                        "gamma_ligand_label_seq_id": "201",
                                        "mapping_status": (
                                            "mapped_catalytic_histidine_and_nucleotide_site_review_only"
                                        ),
                                        "catalytic_histidine_residues": [
                                            {
                                                "auth_asym_id": "A",
                                                "label_asym_id": "A",
                                                "auth_seq_id": "139",
                                                "label_seq_id": "139",
                                                "residue_code": "HIS",
                                            }
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-sibling-control-homolog-gamma-distance-sample",
                    "--epk-sibling-control-homolog-mapping-review",
                    str(mapping_review),
                    "--candidate-thresholds",
                    "4,6,8",
                    "--cif-dir",
                    str(root),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            sample = json.loads(out.read_text(encoding="utf-8"))
            metadata = sample["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_sibling_control_homolog_gamma_distance_sample",
            )
            self.assertEqual(metadata["reviewed_sibling_family_id"], "ndk")
            self.assertEqual(metadata["measured_homolog_structure_count"], 1)
            self.assertEqual(
                metadata["homolog_control_axis"],
                "mapped_phosphohistidine_site_not_hydroxyl_acceptor",
            )
            self.assertFalse(metadata["threshold_calibrated"])
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = sample["rows"][0]
            self.assertEqual(
                row["measurement_status"],
                "homolog_gamma_to_mapped_histidine_distance_measured_review_only",
            )
            self.assertEqual(
                row["nearest_gamma_to_mapped_histidine_distance_angstrom"], 3.0
            )
            self.assertEqual(row["candidate_threshold_hits_angstrom"], [4.0, 6.0, 8.0])
            self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_sibling_control_homolog_terminal_review_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            mapping_review = root / "homolog_mapping_review.json"
            distance_sample = root / "homolog_distance_sample.json"
            out = root / "homolog_terminal_review.json"
            mapping_review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_sibling_control_homolog_mapping_review",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "reviewed_sibling_family_id": "ndk",
                            "reviewed_sibling_family_name": (
                                "Nucleoside diphosphate kinases"
                            ),
                        },
                        "rows": [
                            {
                                "pdb_id": "9PFY",
                                "family_id": "ndk",
                                "homolog_mapping_status": (
                                    "homolog_mapping_ready_for_distance_measurement_review_only"
                                ),
                                "measurement_ready_for_negative_control": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            distance_sample.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_control_homolog_gamma_distance_sample"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "reviewed_sibling_family_id": "ndk",
                            "reviewed_sibling_family_name": (
                                "Nucleoside diphosphate kinases"
                            ),
                            "threshold_selection_status": (
                                "blocked_homolog_histidine_axis_requires_counterevidence_rule"
                            ),
                            "observed_homolog_histidine_distance_min_angstrom": 3.0,
                            "observed_homolog_histidine_distance_max_angstrom": 3.0,
                        },
                        "rows": [
                            {
                                "pdb_id": "9PFY",
                                "family_id": "ndk",
                                "measurement_status": (
                                    "homolog_gamma_to_mapped_histidine_distance_measured_review_only"
                                ),
                                "gamma_to_mapped_histidine_distance_measured": True,
                                "nearest_gamma_to_mapped_histidine_distance_angstrom": 3.0,
                                "nearest_gamma_to_same_chain_hydroxyl_distance_angstrom": 6.5,
                                "control_use_status": (
                                    "homolog_histidine_axis_counterevidence_review_only_not_calibration"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-sibling-control-homolog-terminal-review",
                    "--epk-sibling-control-homolog-mapping-review",
                    str(mapping_review),
                    "--epk-sibling-control-homolog-gamma-distance-sample",
                    str(distance_sample),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"], "epk_sibling_control_homolog_terminal_review"
            )
            self.assertEqual(metadata["reviewed_sibling_family_id"], "ndk")
            self.assertEqual(
                metadata["terminal_review_status"],
                "terminal_review_only_all_homologs_measured_histidine_axis_blocks_threshold",
            )
            self.assertEqual(metadata["measured_homolog_pdb_ids"], ["9PFY"])
            self.assertEqual(metadata["countable_label_candidate_count"], 0)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])

    def test_build_epk_review_only_scoring_prototype_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            axis = root / "axis.json"
            gamma = root / "gamma.json"
            identity = root / "identity.json"
            homolog = root / "homolog.json"
            external = root / "external.json"
            out = root / "prototype.json"
            axis.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_text_free_local_axis_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "pdb_id": "2PHK",
                                "prototype_vector": {
                                    "local_adenine_nucleotide_ligand": 1,
                                    "local_metal_ligand": 1,
                                    "catalytic_acid_base_residue": 1,
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            gamma.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_geometry_measurement_sample"
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "nearest_gamma_to_hydroxyl_distance_angstrom": 3.6,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            identity.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "epk_acceptor_identity_review"},
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "acceptor_identity_source_supported": True,
                                "acceptor_identity_review_status": (
                                    "measured_acceptor_identity_source_supported_review_only"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            homolog.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_control_homolog_gamma_distance_sample"
                            )
                        },
                        "rows": [
                            {
                                "pdb_id": "9PFY",
                                "family_id": "ndk",
                                "family_name": "Nucleoside diphosphate kinases",
                                "measurement_status": (
                                    "homolog_gamma_to_mapped_histidine_distance_measured_review_only"
                                ),
                                "nearest_gamma_to_mapped_histidine_distance_angstrom": 3.0,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            external.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "uniprot:P78549",
                                "accession": "P78549",
                                "active_site_feature_count": 2,
                                "out_of_scope_inverse_gate": {
                                    "inverse_gate_status": "passed",
                                    "max_current_fingerprint_score": 0.115,
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-review-only-scoring-prototype",
                    "--epk-text-free-local-axis-prototype",
                    str(axis),
                    "--epk-gamma-geometry-measurement-sample",
                    str(gamma),
                    "--epk-acceptor-identity-review",
                    str(identity),
                    "--epk-sibling-control-homolog-gamma-distance-sample",
                    str(homolog),
                    "--external-hard-negative-inverse-gate-scores",
                    str(external),
                    "--imported-external-entry-ids",
                    "uniprot:P78549",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            prototype = json.loads(out.read_text(encoding="utf-8"))
            metadata = prototype["metadata"]
            self.assertEqual(metadata["method"], "epk_review_only_scoring_prototype")
            self.assertEqual(metadata["prototype_gate_status"], "fail_closed_review_only")
            self.assertEqual(metadata["current_positive_full_axis_count"], 1)
            self.assertEqual(metadata["sibling_homolog_counteraxis_row_count"], 1)
            self.assertEqual(metadata["imported_external_hard_negative_row_count"], 1)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            decisions = {row["prototype_decision"] for row in prototype["rows"]}
            self.assertIn(
                "blocked_by_phosphohistidine_counteraxis_review_only", decisions
            )
            self.assertIn(
                "external_hard_negative_abstain_missing_epk_axes_review_only",
                decisions,
            )

    def test_build_epk_counteraxis_sufficiency_decision_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype = root / "prototype.json"
            precount = root / "precount.json"
            out = root / "counteraxis.json"
            prototype.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_review_only_scoring_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "candidate_threshold_angstrom": 6.0,
                            "prototype_gate_status": "fail_closed_review_only",
                        },
                        "rows": [
                            {
                                "row_type": (
                                    "sibling_family_specific_negative_control"
                                ),
                                "pdb_id": "1ABC",
                                "family_id": "pfkb",
                                "nearest_gamma_to_family_acid_base_distance_angstrom": (
                                    4.2
                                ),
                                "review_only_prototype_score": 0.0,
                            },
                            {
                                "row_type": "sibling_homolog_negative_control",
                                "pdb_id": "9PFY",
                                "family_id": "ndk",
                                "review_only_prototype_score": 0.0,
                            },
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P78549",
                                "review_only_prototype_score": 0.0,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            precount.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_precount_gate_status",
                            "precount_gate_status": "blocked_review_only",
                            "failing_gate_ids": [
                                "acceptor_threshold_calibrated",
                                "external_hard_negative_scored_reaudit",
                            ],
                            "chain_ligand_acceptor_feature_passes_current_review_controls": True,
                            "chain_ligand_acceptor_feature_admissible_for_production_scoring": False,
                            "chain_ligand_acceptor_negative_control_false_hit_count": 0,
                            "chain_ligand_external_feature_non_abstention_count": 0,
                            "heteromeric_peptide_acceptor_identity_status": (
                                "passes_current_controls_peptide_like_acceptor_identity_review_only"
                            ),
                            "heteromeric_peptide_acceptor_identity_positive_hit_count": 3,
                            "heteromeric_peptide_acceptor_identity_source_free_ready_count": 3,
                            "heteromeric_peptide_acceptor_identity_nonaccepted_false_hit_count": 0,
                            "heteromeric_peptide_acceptor_identity_sibling_false_hit_count": 0,
                            "heteromeric_peptide_acceptor_identity_axis_narrow": True,
                            "heteromeric_peptide_external_feature_probe_passed": True,
                            "heteromeric_peptide_external_feature_non_abstention_count": 0,
                            "heteromeric_source_expansion_peptide_role_axis_passed": True,
                            "heteromeric_source_expansion_peptide_role_axis_status": (
                                "passes_source_expansion_controls_peptide_role_axis_review_only"
                            ),
                            "heteromeric_source_expansion_peptide_role_hit_count": 2,
                            "heteromeric_source_expansion_peptide_role_hit_pdb_ids": [
                                "1O6K",
                                "1O6L",
                            ],
                            "heteromeric_source_expansion_peptide_role_nonpositive_false_hit_count": 0,
                            "heteromeric_source_expansion_peptide_role_general_substrate_ready_count": 0,
                            "negative_control_family_template_validated_family_ids": [
                                "pfkb"
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-counteraxis-sufficiency-decision",
                    "--epk-review-only-scoring-prototype",
                    str(prototype),
                    "--epk-precount-gate-status",
                    str(precount),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            decision = json.loads(out.read_text(encoding="utf-8"))
            metadata = decision["metadata"]
            self.assertEqual(metadata["method"], "epk_counteraxis_sufficiency_decision")
            self.assertEqual(metadata["threshold_selection_decision"], "do_not_select_threshold")
            self.assertEqual(metadata["family_specific_counteraxis_threshold_hit_count"], 1)
            self.assertEqual(metadata["phosphohistidine_counteraxis_row_count"], 1)
            self.assertTrue(
                metadata[
                    "chain_ligand_acceptor_feature_passes_current_review_controls"
                ]
            )
            self.assertEqual(
                metadata["family_specific_template_validated_family_ids"], ["pfkb"]
            )
            self.assertTrue(
                metadata["counteraxis_sufficient_to_block_distance_only_threshold"]
            )
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            self.assertFalse(metadata["fingerprint_registry_edited"])
            self.assertFalse(metadata["curated_label_registry_edited"])
            self.assertEqual(metadata["countable_label_candidate_count"], 0)
            axes = {row["decision_axis"]: row for row in decision["decision_rows"]}
            self.assertEqual(
                axes["family_specific_sibling_counteraxis"]["decision"],
                "blocks_distance_only_threshold_selection",
            )
            self.assertEqual(
                axes["chain_ligand_acceptor_disambiguation_feature"]["decision"],
                "passes_current_controls_but_not_production_admissible",
            )
            self.assertEqual(
                axes["heteromeric_peptide_acceptor_identity_feature"]["decision"],
                "passes_current_controls_and_external_feature_probe_but_narrow_not_production_admissible",
            )
            self.assertTrue(
                metadata[
                    "heteromeric_peptide_acceptor_identity_passes_current_review_controls"
                ]
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
                axes["heteromeric_source_expansion_peptide_role_axis"]["decision"],
                "passes_source_expansion_controls_but_peptide_axis_narrow_not_production_admissible",
            )

    def test_build_epk_substrate_acceptor_counteraxis_prototype_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype = root / "prototype.json"
            counteraxis = root / "counteraxis.json"
            out = root / "substrate_acceptor.json"
            prototype.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_review_only_scoring_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "text_free_inputs_only": True,
                                "prototype_decision": (
                                    "candidate_positive_signal_review_only_not_calibrated"
                                ),
                                "review_only_prototype_score": 1.0,
                                "prototype_axis_values": {
                                    "local_adenine_nucleotide_ligand": 1,
                                    "local_metal_ligand": 1,
                                    "catalytic_acid_base_residue": 1,
                                    "gamma_to_acceptor_distance_within_candidate_cutoff": 1,
                                    "source_supported_hydroxyl_acceptor_identity": 1,
                                },
                            },
                            {
                                "row_type": "sibling_homolog_negative_control",
                                "family_id": "ndk",
                                "pdb_id": "9PFY",
                                "text_free_inputs_only": True,
                                "prototype_decision": (
                                    "blocked_by_phosphohistidine_counteraxis_review_only"
                                ),
                                "prototype_axis_values": {
                                    "gamma_to_mapped_histidine_counteraxis": 1,
                                    "source_supported_hydroxyl_acceptor_identity": 0,
                                },
                            },
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P78549",
                                "text_free_inputs_only": True,
                                "prototype_axis_values": {
                                    "local_adenine_nucleotide_ligand": 0,
                                    "local_metal_ligand": 0,
                                    "catalytic_acid_base_residue": 0,
                                    "gamma_to_acceptor_distance_within_candidate_cutoff": 0,
                                    "source_supported_hydroxyl_acceptor_identity": 0,
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            counteraxis.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_counteraxis_sufficiency_decision"
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-substrate-acceptor-counteraxis-prototype",
                    "--epk-review-only-scoring-prototype",
                    str(prototype),
                    "--epk-counteraxis-sufficiency-decision",
                    str(counteraxis),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            surface = json.loads(out.read_text(encoding="utf-8"))
            metadata = surface["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_substrate_acceptor_counteraxis_prototype",
            )
            self.assertEqual(metadata["positive_like_acceptor_axis_row_count"], 1)
            self.assertEqual(metadata["blocked_counteraxis_row_count"], 1)
            self.assertEqual(metadata["external_hard_negative_abstention_row_count"], 1)
            self.assertTrue(metadata["decision_surface_changed"])
            self.assertFalse(metadata["epk_score_computed"])
            decisions = {
                row["counteraxis_rule_decision"] for row in surface["rows"]
            }
            self.assertIn("positive_like_acceptor_axis_review_only", decisions)
            self.assertIn(
                "blocked_by_non_hydroxyl_phosphohistidine_counteraxis",
                decisions,
            )
            self.assertIn(
                "external_hard_negative_abstain_missing_epk_acceptor_axes",
                decisions,
            )

    def test_build_epk_external_hard_negative_counteraxis_review_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            substrate = root / "substrate.json"
            out = root / "external_review.json"
            substrate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_substrate_acceptor_counteraxis_prototype"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P78549",
                                "text_free_inputs_only": True,
                                "counteraxis_rule_decision": (
                                    "external_hard_negative_abstain_missing_epk_acceptor_axes"
                                ),
                                "source_axis_values": {
                                    "local_adenine_nucleotide_ligand": 0
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-external-hard-negative-counteraxis-review",
                    "--epk-substrate-acceptor-counteraxis-prototype",
                    str(substrate),
                    "--imported-external-entry-ids",
                    "uniprot:P78549",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_external_hard_negative_counteraxis_review",
            )
            self.assertEqual(
                metadata["review_only_external_hard_negative_abstention_count"],
                1,
            )
            self.assertEqual(
                metadata["review_only_external_hard_negative_non_abstention_count"],
                0,
            )
            self.assertFalse(metadata["clean_heldout_performance_claim_permitted"])
            self.assertFalse(metadata["epk_score_computed"])
            self.assertEqual(
                review["rows"][0]["review_status"],
                "review_only_external_hard_negative_abstention",
            )

    def test_build_epk_text_free_acceptor_feature_gap_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype = root / "prototype.json"
            homolog = root / "homolog.json"
            family = root / "family.json"
            out = root / "acceptor_gap.json"
            prototype.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_review_only_scoring_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "nearest_gamma_to_hydroxyl_distance_angstrom": 5.0,
                                "acceptor_context_type": (
                                    "source_supported_hydroxyl_residue"
                                ),
                                "gamma_geometry_scope": "current_selected_structure",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            homolog.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_control_homolog_gamma_distance_sample"
                            )
                        },
                        "rows": [
                            {
                                "measurement_status": (
                                    "homolog_gamma_to_mapped_histidine_distance_measured_review_only"
                                ),
                                "family_id": "ndk",
                                "family_name": "Nucleoside diphosphate kinases",
                                "pdb_id": "9PFY",
                                "nearest_gamma_to_same_chain_hydroxyl_distance_angstrom": 4.8,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            family.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_family_specific_homolog_gamma_distance_sample"
                            )
                        },
                        "rows": [
                            {
                                "measurement_status": (
                                    "family_specific_gamma_to_acid_base_distance_measured_review_only"
                                ),
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "pdb_id": "1ESQ",
                                "nearest_gamma_to_same_chain_hydroxyl_distance_angstrom": 7.1,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-text-free-acceptor-feature-gap-audit",
                    "--epk-review-only-scoring-prototype",
                    str(prototype),
                    "--epk-sibling-control-homolog-gamma-distance-sample",
                    str(homolog),
                    "--epk-family-specific-homolog-gamma-distance-sample",
                    str(family),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_text_free_acceptor_feature_gap_audit",
            )
            self.assertEqual(metadata["current_positive_feature_hit_count"], 1)
            self.assertEqual(metadata["negative_control_row_count"], 2)
            self.assertEqual(metadata["negative_control_false_hit_count"], 1)
            self.assertEqual(metadata["candidate_feature_status"], "blocked_review_only")
            self.assertFalse(metadata["feature_admissible_for_scoring"])
            self.assertFalse(metadata["epk_score_computed"])
            decisions = {row["feature_audit_decision"] for row in audit["rows"]}
            self.assertIn(
                "control_false_hit_blocks_text_free_feature", decisions
            )
            self.assertIn("control_nonhit_review_only", decisions)

    def test_build_epk_chain_ligand_acceptor_disambiguation_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype = root / "prototype.json"
            identity = root / "identity.json"
            alternate = root / "alternate.json"
            homolog = root / "homolog.json"
            family = root / "family.json"
            out = root / "chain_ligand.json"
            prototype.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_review_only_scoring_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "nearest_gamma_to_hydroxyl_distance_angstrom": 5.0,
                                "acceptor_context_type": (
                                    "source_supported_hydroxyl_residue"
                                ),
                            },
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:640",
                                "pdb_id": "3TM0",
                                "acceptor_context_type": (
                                    "acceptor_like_ligand_analog"
                                ),
                            },
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P78549",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            identity.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "epk_acceptor_identity_review"},
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "nearest_measured_hydroxyl": {
                                    "distance_angstrom": 5.0,
                                    "on_non_catalytic_chain": True,
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_m_csa640_alternate_gamma_geometry_review"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:640",
                                "pdb_id": "3TM0",
                                "gamma_to_acceptor_distance_angstrom": 3.5,
                                "acceptor_like_ligand_present": True,
                                "within_candidate_threshold": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            homolog.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_control_homolog_gamma_distance_sample"
                            )
                        },
                        "rows": [
                            {
                                "measurement_status": (
                                    "homolog_gamma_to_mapped_histidine_distance_measured_review_only"
                                ),
                                "family_id": "ndk",
                                "family_name": "Nucleoside diphosphate kinases",
                                "pdb_id": "9PFY",
                                "nearest_gamma_to_same_chain_hydroxyl_distance_angstrom": 4.8,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            family.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_family_specific_homolog_gamma_distance_sample"
                            )
                        },
                        "rows": [
                            {
                                "measurement_status": (
                                    "family_specific_gamma_to_acid_base_distance_measured_review_only"
                                ),
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "pdb_id": "1TZ6",
                                "nearest_gamma_to_same_chain_hydroxyl_distance_angstrom": 7.1,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-chain-ligand-acceptor-disambiguation-audit",
                    "--epk-review-only-scoring-prototype",
                    str(prototype),
                    "--epk-acceptor-identity-review",
                    str(identity),
                    "--epk-m-csa640-alternate-gamma-geometry-review",
                    str(alternate),
                    "--epk-sibling-control-homolog-gamma-distance-sample",
                    str(homolog),
                    "--epk-family-specific-homolog-gamma-distance-sample",
                    str(family),
                    "--imported-external-entry-ids",
                    "uniprot:P78549",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_chain_ligand_acceptor_disambiguation_audit",
            )
            self.assertEqual(metadata["current_positive_feature_hit_count"], 2)
            self.assertEqual(metadata["negative_control_row_count"], 2)
            self.assertEqual(metadata["negative_control_false_hit_count"], 0)
            self.assertEqual(
                metadata["negative_control_same_chain_block_count"], 1
            )
            self.assertEqual(
                metadata["external_hard_negative_abstention_row_count"], 1
            )
            self.assertTrue(metadata["feature_passes_current_review_controls"])
            self.assertFalse(metadata["feature_admissible_for_production_scoring"])
            self.assertFalse(metadata["epk_score_computed"])
            decisions = {row["feature_audit_decision"] for row in audit["rows"]}
            self.assertIn(
                "positive_chain_ligand_acceptor_context_hit_review_only",
                decisions,
            )
            self.assertIn("control_blocked_same_chain_hydroxyl_context", decisions)
            self.assertIn(
                "external_hard_negative_abstain_missing_chain_ligand_axes",
                decisions,
            )

    def test_build_epk_chain_ligand_external_hard_negative_feature_screen_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            audit_path = root / "chain_ligand.json"
            out = root / "external_screen.json"
            audit_path.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_chain_ligand_acceptor_disambiguation_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "candidate_feature_id": (
                                "gamma_acceptor_non_catalytic_chain_or_ligand_analog_v0"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P78549",
                                "text_free_inputs_only": True,
                                "candidate_feature_hit": False,
                                "feature_audit_decision": (
                                    "external_hard_negative_abstain_missing_chain_ligand_axes"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-chain-ligand-external-hard-negative-feature-screen",
                    "--epk-chain-ligand-acceptor-disambiguation-audit",
                    str(audit_path),
                    "--imported-external-entry-ids",
                    "uniprot:P78549",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            screen = json.loads(out.read_text(encoding="utf-8"))
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
            self.assertEqual(screen["rows"][0]["review_only_feature_score"], 0.0)

    def test_build_epk_protein_substrate_acceptor_candidate_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            chain_ligand = root / "chain_ligand.json"
            out = root / "protein_substrate.json"
            chain_ligand.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_chain_ligand_acceptor_disambiguation_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "candidate_feature_id": (
                                "gamma_acceptor_non_catalytic_chain_or_ligand_analog_v0"
                            ),
                            "candidate_threshold_angstrom": 6.0,
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "candidate_feature_hit": True,
                                "non_catalytic_chain_acceptor": True,
                                "ligand_analog_acceptor": False,
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:640",
                                "pdb_id": "3TM0",
                                "candidate_feature_hit": True,
                                "non_catalytic_chain_acceptor": False,
                                "ligand_analog_acceptor": True,
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": "sibling_family_specific_negative_control",
                                "family_id": "pfkb",
                                "pdb_id": "1TZ6",
                                "candidate_feature_hit": False,
                                "non_catalytic_chain_acceptor": False,
                                "ligand_analog_acceptor": False,
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P78549",
                                "candidate_feature_hit": False,
                                "text_free_inputs_only": True,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-protein-substrate-acceptor-candidate-audit",
                    "--epk-chain-ligand-acceptor-disambiguation-audit",
                    str(chain_ligand),
                    "--imported-external-entry-ids",
                    "uniprot:P78549",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_protein_substrate_acceptor_candidate_audit",
            )
            self.assertEqual(metadata["current_positive_feature_hit_count"], 1)
            self.assertEqual(metadata["current_positive_feature_miss_count"], 1)
            self.assertEqual(metadata["ligand_analog_only_positive_miss_count"], 1)
            self.assertEqual(metadata["negative_control_false_hit_count"], 0)
            self.assertEqual(
                metadata["external_hard_negative_feature_abstention_count"],
                1,
            )
            self.assertEqual(
                metadata["candidate_feature_status"],
                "blocked_review_only_positive_coverage_gap",
            )
            self.assertFalse(metadata["feature_admissible_for_production_scoring"])
            self.assertFalse(metadata["epk_score_computed"])
            decisions = {row["feature_audit_decision"] for row in audit["rows"]}
            self.assertIn(
                "positive_protein_substrate_acceptor_hit_review_only",
                decisions,
            )
            self.assertIn(
                "positive_ligand_analog_only_miss_blocks_production_candidate",
                decisions,
            )

    def test_build_epk_ligand_analog_policy_blocker_decision_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            protein = root / "protein.json"
            chain_ligand = root / "chain_ligand.json"
            alternate = root / "alternate.json"
            out = root / "ligand_policy.json"
            protein.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_protein_substrate_acceptor_candidate_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:640",
                                "pdb_id": "3TM0",
                                "candidate_feature_hit": False,
                                "ligand_analog_acceptor": True,
                                "feature_audit_decision": (
                                    "positive_ligand_analog_only_miss_blocks_production_candidate"
                                ),
                                "text_free_inputs_only": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            chain_ligand.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_chain_ligand_acceptor_disambiguation_audit"
                            )
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:640",
                                "candidate_feature_hit": True,
                                "ligand_analog_acceptor": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_m_csa640_alternate_gamma_geometry_review"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:640",
                                "pdb_id": "3TM0",
                                "acceptor_ligand_code": "B31",
                                "acceptor_like_ligand_present": True,
                                "gamma_to_acceptor_distance_angstrom": 3.558,
                                "alternate_gamma_geometry_review_status": (
                                    "alternate_gamma_to_acceptor_analog_distance_reviewed_review_only"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-ligand-analog-policy-blocker-decision",
                    "--epk-protein-substrate-acceptor-candidate-audit",
                    str(protein),
                    "--epk-chain-ligand-acceptor-disambiguation-audit",
                    str(chain_ligand),
                    "--epk-m-csa640-alternate-gamma-geometry-review",
                    str(alternate),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            decision = json.loads(out.read_text(encoding="utf-8"))
            metadata = decision["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_ligand_analog_policy_blocker_decision",
            )
            self.assertEqual(metadata["ligand_analog_dependency_count"], 1)
            self.assertEqual(
                metadata["ligand_analog_policy_decision"],
                "do_not_use_ligand_analog_as_production_acceptor_evidence",
            )
            self.assertFalse(metadata["feature_admissible_for_production_scoring"])
            self.assertFalse(metadata["epk_score_computed"])
            row = decision["rows"][0]
            self.assertEqual(row["entry_id"], "m_csa:640")
            self.assertEqual(row["acceptor_ligand_code"], "B31")
            self.assertFalse(
                row["ligand_analog_evidence_admissible_for_production_scoring"]
            )

    def test_build_epk_analog_product_state_policy_activation_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prereg = root / "prereg.json"
            ligand_policy = root / "ligand_policy.json"
            protein = root / "protein.json"
            chain_ligand = root / "chain_ligand.json"
            external = root / "external.json"
            terminal = root / "terminal.json"
            precount = root / "precount.json"
            out = root / "activation.json"
            prereg.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_analog_product_state_policy_preregistration"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "policy_status": (
                                "draft_preregistered_review_only_not_activated"
                            ),
                            "policy_activation_allowed": False,
                            "production_scoring_admissible": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            ligand_policy.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_ligand_analog_policy_blocker_decision"
                            ),
                            "ligand_analog_dependency_count": 1,
                            "ligand_analog_dependency_entry_ids": ["m_csa:640"],
                            "ligand_analog_production_admissible_count": 0,
                            "ligand_analog_policy_decision": (
                                "do_not_use_ligand_analog_as_production_acceptor_evidence"
                            ),
                        }
                    }
                ),
                encoding="utf-8",
            )
            protein.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_protein_substrate_acceptor_candidate_audit"
                            ),
                            "current_positive_row_count": 3,
                            "current_positive_feature_hit_count": 2,
                            "current_positive_feature_miss_count": 1,
                            "ligand_analog_only_positive_miss_entry_ids": [
                                "m_csa:640"
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )
            chain_ligand.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_chain_ligand_acceptor_disambiguation_audit"
                            ),
                            "candidate_feature_id": (
                                "gamma_acceptor_non_catalytic_chain_or_ligand_analog_v0"
                            ),
                            "feature_passes_current_review_controls": True,
                            "negative_control_false_hit_count": 0,
                            "negative_control_row_count": 25,
                        }
                    }
                ),
                encoding="utf-8",
            )
            external.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_chain_ligand_external_hard_negative_feature_screen"
                            ),
                            "review_only_feature_screen_passed": True,
                            "review_only_external_hard_negative_feature_non_abstention_count": 0,
                            "clean_heldout_performance_claim_permitted": False,
                            "external_hard_negative_reaudit_scored": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            terminal.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_protein_substrate_source_repair_terminal_decision"
                            ),
                            "current_source_candidates_exhausted": True,
                            "measurement_ready_candidate_count": 0,
                            "terminal_decision": (
                                "current_source_candidates_exhausted_review_only"
                            ),
                            "recommended_next_experiment": (
                                "pre_register_ligand_analog_or_product_state_policy_or_source_new_epk_positive"
                            ),
                        }
                    }
                ),
                encoding="utf-8",
            )
            precount.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_precount_gate_status",
                            "ready_to_run_epk_scorer": False,
                            "epk_score_computed": False,
                            "external_hard_negative_reaudit_scored": False,
                            "threshold_calibrated": False,
                            "fingerprint_registry_edited": False,
                            "curated_label_registry_edited": False,
                            "ready_to_expand_positive_fingerprint_universe": False,
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-analog-product-state-policy-activation-audit",
                    "--epk-analog-product-state-policy-preregistration",
                    str(prereg),
                    "--epk-ligand-analog-policy-blocker-decision",
                    str(ligand_policy),
                    "--epk-protein-substrate-acceptor-candidate-audit",
                    str(protein),
                    "--epk-chain-ligand-acceptor-disambiguation-audit",
                    str(chain_ligand),
                    "--epk-chain-ligand-external-hard-negative-feature-screen",
                    str(external),
                    "--epk-protein-substrate-source-repair-terminal-decision",
                    str(terminal),
                    "--epk-precount-gate-status",
                    str(precount),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_analog_product_state_policy_activation_audit",
            )
            self.assertEqual(
                metadata["policy_activation_status"], "blocked_review_only"
            )
            self.assertFalse(metadata["policy_activation_allowed"])
            self.assertEqual(metadata["failed_activation_requirement_count"], 7)
            self.assertEqual(metadata["diagnostic_control_pass_count"], 2)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
            criteria = {row["criterion_id"]: row for row in audit["rows"]}
            self.assertFalse(criteria["ligand_analog_dependency_resolved"]["passed"])
            self.assertTrue(
                criteria[
                    "sibling_controls_remain_blocked_under_candidate_feature"
                ]["passed"]
            )

    def test_build_epk_analog_product_state_policy_control_reaudit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prereg = root / "prereg.json"
            chain_ligand = root / "chain_ligand.json"
            external = root / "external.json"
            terminal = root / "terminal.json"
            out = root / "control_reaudit.json"
            prereg.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_analog_product_state_policy_preregistration"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        }
                    }
                ),
                encoding="utf-8",
            )
            chain_ligand.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_chain_ligand_acceptor_disambiguation_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "candidate_feature_hit": True,
                                "non_catalytic_chain_acceptor": True,
                                "ligand_analog_acceptor": False,
                                "nearest_gamma_to_candidate_acceptor_distance_angstrom": 3.61,
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:640",
                                "pdb_id": "3TM0",
                                "candidate_feature_hit": True,
                                "non_catalytic_chain_acceptor": False,
                                "ligand_analog_acceptor": True,
                                "nearest_gamma_to_candidate_acceptor_distance_angstrom": 3.558,
                                "gamma_geometry_scope": (
                                    "alternate_graph_linked_structure"
                                ),
                                "text_free_inputs_only": True,
                            },
                            {
                                "row_type": "sibling_family_specific_negative_control",
                                "family_id": "pfkb",
                                "pdb_id": "1TZ6",
                                "candidate_feature_hit": False,
                                "non_catalytic_chain_acceptor": False,
                                "ligand_analog_acceptor": False,
                                "text_free_inputs_only": True,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            external.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_chain_ligand_external_hard_negative_feature_screen"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "uniprot:P78549",
                                "candidate_feature_hit": False,
                                "review_only_feature_non_abstention": False,
                                "review_only_feature_score": 0.0,
                                "text_free_inputs_only": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            terminal.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_protein_substrate_source_repair_terminal_decision"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:760",
                                "decision": "terminal_split_state_blocked_review_only",
                                "measurement_ready_candidate_count": 0,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-analog-product-state-policy-control-reaudit",
                    "--epk-analog-product-state-policy-preregistration",
                    str(prereg),
                    "--epk-chain-ligand-acceptor-disambiguation-audit",
                    str(chain_ligand),
                    "--epk-chain-ligand-external-hard-negative-feature-screen",
                    str(external),
                    "--epk-protein-substrate-source-repair-terminal-decision",
                    str(terminal),
                    "--imported-external-entry-ids",
                    "uniprot:P78549",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_analog_product_state_policy_control_reaudit",
            )
            self.assertEqual(metadata["current_positive_policy_hit_count"], 2)
            self.assertEqual(
                metadata["ligand_analog_positive_policy_hit_count"], 1
            )
            self.assertEqual(metadata["sibling_control_policy_false_hit_count"], 0)
            self.assertTrue(metadata["sibling_family_control_reaudit_passed"])
            self.assertTrue(
                metadata["external_hard_negative_feature_screen_passed"]
            )
            self.assertFalse(metadata["policy_activation_allowed"])
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
            decisions = {row.get("policy_reaudit_decision") for row in audit["rows"]}
            self.assertIn("policy_positive_ligand_analog_hit_review_only", decisions)
            self.assertIn(
                "policy_source_repair_blocked_by_exclusion_or_missing_geometry",
                decisions,
            )

    def test_build_epk_review_only_external_hard_negative_score_probe_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype = root / "prototype.json"
            policy = root / "policy.json"
            out = root / "score_probe.json"
            prototype.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_review_only_scoring_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P06744",
                                "review_only_prototype_score": 0.0,
                                "prototype_decision": (
                                    "external_hard_negative_abstain_missing_epk_axes_review_only"
                                ),
                                "prototype_axis_values": {
                                    "local_adenine_nucleotide_ligand": 0,
                                    "local_metal_ligand": 0,
                                },
                                "text_free_inputs_only": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            policy.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_analog_product_state_policy_control_reaudit"
                            ),
                            "policy_activation_allowed": False,
                        },
                        "rows": [
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P06744",
                                "policy_feature_hit": False,
                                "policy_reaudit_decision": (
                                    "policy_external_hard_negative_feature_abstention"
                                ),
                                "text_free_inputs_only": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-review-only-external-hard-negative-score-probe",
                    "--epk-review-only-scoring-prototype",
                    str(prototype),
                    "--epk-analog-product-state-policy-control-reaudit",
                    str(policy),
                    "--imported-external-entry-ids",
                    "uniprot:P06744",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            probe = json.loads(out.read_text(encoding="utf-8"))
            metadata = probe["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_review_only_external_hard_negative_score_probe",
            )
            self.assertTrue(metadata["review_only_score_probe_complete"])
            self.assertTrue(metadata["review_only_score_probe_passed"])
            self.assertEqual(
                metadata["review_only_score_probe_non_abstention_count"], 0
            )
            self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["fingerprint_registry_edited"])
            self.assertFalse(metadata["curated_label_registry_edited"])
            row = probe["rows"][0]
            self.assertEqual(row["entry_id"], "uniprot:P06744")
            self.assertEqual(row["review_only_probe_score"], 0.0)
            self.assertFalse(row["review_only_score_probe_non_abstention"])

    def test_build_epk_heteromeric_followon_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            cif_dir = root / "cif"
            cif_dir.mkdir()
            base = root / "base.json"
            scout = root / "scout.json"
            validation = root / "validation.json"
            distances = root / "distances.json"
            sibling = root / "sibling.json"
            rerun_out = root / "rerun.json"
            gap_out = root / "gap.json"
            probe_out = root / "probe.json"
            counteraxis_out = root / "counteraxis.json"
            broader_out = root / "broader.json"
            asymmetry_out = root / "asymmetry.json"
            identity_out = root / "identity.json"
            identity_rule_out = root / "identity_rule.json"

            base.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_ligand_specific_5hvk_prototype_control_rerun"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "control_rerun_status": (
                                "passes_review_only_controls_but_scorer_blocked"
                            ),
                            "current_positive_prototype_row_count": 1,
                            "positive_like_review_row_count": 2,
                            "source_valid_5hvk_candidate_row_count": 1,
                            "sibling_control_row_count": 1,
                            "imported_external_hard_negative_row_count": 1,
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "pdb_id": "2PHK",
                                "prototype_decision": (
                                    "candidate_positive_signal_review_only_not_calibrated"
                                ),
                                "rerun_surface_role": "carried_current_positive",
                            },
                            {
                                "row_type": (
                                    "ligand_specific_5hvk_source_valid_positive_candidate"
                                ),
                                "pdb_id": "5HVK",
                                "prototype_decision": (
                                    "source_valid_5hvk_positive_signal_review_only_not_calibrated"
                                ),
                                "rerun_surface_role": "source_valid_5hvk",
                            },
                            {
                                "row_type": "sibling_family_specific_negative_control",
                                "pdb_id": "1ESQ",
                                "prototype_decision": (
                                    "blocked_by_family_specific_sibling_counteraxis_review_only"
                                ),
                                "candidate_feature_hit": False,
                                "rerun_surface_role": "carried_sibling_control",
                            },
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P06744",
                                "prototype_decision": (
                                    "external_hard_negative_abstain_missing_epk_axes_review_only"
                                ),
                                "rerun_surface_role": (
                                    "carried_imported_external_hard_negative"
                                ),
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            scout.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_positive_coverage_candidate_scout"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "pdb_id": "6Z3R",
                                "heteromeric_candidate_hits": [
                                    {"nearest_gamma_distance_angstrom": 4.2}
                                ],
                            },
                            {
                                "pdb_id": "7M0T",
                                "heteromeric_candidate_hits": [
                                    {"nearest_gamma_distance_angstrom": 4.5}
                                ],
                            },
                            {
                                "pdb_id": "8ZN6",
                                "heteromeric_candidate_hits": [
                                    {"nearest_gamma_distance_angstrom": 4.8}
                                ],
                            },
                            {"pdb_id": "9NOH", "heteromeric_candidate_hits": []},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            validation.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_candidate_source_validation_review"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "pdb_id": "6Z3R",
                                "source_pair_id": "smg1_upf1",
                                "source_validated_positive_like": True,
                                "source_validation_status": (
                                    "accepted_source_valid_heteromeric_kinase_substrate_review_only"
                                ),
                                "entity_descriptions": ["MAGNESIUM ION"],
                                "candidate_hits": [
                                    {
                                        "candidate_chain_name": "E",
                                        "candidate_residue_code": "SER",
                                        "gamma_associated_polymer_chain_name": "A",
                                        "nearest_gamma_distance_angstrom": 4.2,
                                    }
                                ],
                                "nearest_heteromeric_candidate_distance_angstrom": 4.2,
                            },
                            {
                                "pdb_id": "7M0T",
                                "source_pair_id": "braf_mek",
                                "source_validated_positive_like": False,
                                "source_validation_status": (
                                    "blocked_ambiguous_kinase_kinase_role_direction_review_only"
                                ),
                                "candidate_hits": [
                                    {
                                        "candidate_chain_name": "B",
                                        "gamma_associated_polymer_chain_name": "A",
                                        "nearest_gamma_distance_angstrom": 4.5,
                                    }
                                ],
                                "nearest_heteromeric_candidate_distance_angstrom": 4.5,
                            },
                            {
                                "pdb_id": "8ZN6",
                                "source_pair_id": "kaic_design",
                                "source_validated_positive_like": False,
                                "source_validation_status": (
                                    "rejected_non_epk_substrate_cocomplex_or_designed_clock_protein_review_only"
                                ),
                                "candidate_hits": [
                                    {
                                        "candidate_chain_name": "C",
                                        "gamma_associated_polymer_chain_name": "A",
                                        "nearest_gamma_distance_angstrom": 4.8,
                                    }
                                ],
                                "nearest_heteromeric_candidate_distance_angstrom": 4.8,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            distances.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_source_valid_candidate_gamma_distance_sample"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "all_source_valid_candidates_measured": True,
                        },
                        "rows": [
                            {
                                "pdb_id": "6Z3R",
                                "source_pair_id": "smg1_upf1",
                                "measurement_ready_for_review_controls": True,
                                "nearest_gamma_acceptor_distance_angstrom": 4.2,
                                "distance_candidates": [
                                    {"gamma_ligand_code": "ANP"}
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            sibling.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_control_homolog_gamma_distance_sample"
                            ),
                            "reviewed_sibling_family_id": "ndk",
                            "reviewed_sibling_family_name": (
                                "Nucleoside diphosphate kinases"
                            ),
                        },
                        "rows": [
                            {
                                "pdb_id": "1WKL",
                                "family_id": "ndk",
                                "gamma_to_mapped_histidine_distance_measured": True,
                                "gamma_capable_nucleotide_codes": ["ATP"],
                                "same_chain_hydroxyl_candidate_threshold_hits_angstrom": [
                                    6.0
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            for pdb_id, acceptor_chain, acceptor_context in [
                ("6Z3R", "E", []),
                ("7M0T", "B", ["ANP", "MG"]),
                ("8ZN6", "C", ["ANP", "MG"]),
            ]:
                lines = [
                    f"data_{pdb_id}",
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
                    "HETATM 1 P PG ANP A 701 0 0 0 PG ANP A 701",
                ]
                for idx, code in enumerate(acceptor_context, start=2):
                    lines.append(
                        "HETATM "
                        f"{idx} X X {code} {acceptor_chain} 900 0 0 0 "
                        f"X {code} {acceptor_chain} 900"
                    )
                lines.append("#")
                (cif_dir / f"{pdb_id.lower()}.cif").write_text(
                    "\n".join(lines),
                    encoding="utf-8",
                )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-heteromeric-source-valid-control-rerun",
                    "--epk-ligand-specific-5hvk-prototype-control-rerun",
                    str(base),
                    "--epk-heteromeric-candidate-source-validation-review",
                    str(validation),
                    "--epk-heteromeric-source-valid-candidate-gamma-distance-sample",
                    str(distances),
                    "--out",
                    str(rerun_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            rerun = json.loads(rerun_out.read_text(encoding="utf-8"))
            self.assertEqual(
                rerun["metadata"]["control_rerun_status"],
                "passes_review_only_controls_but_scorer_blocked",
            )
            self.assertEqual(
                rerun["metadata"]["heteromeric_source_valid_pdb_ids"], ["6Z3R"]
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-heteromeric-text-free-axis-gap-audit",
                    "--epk-heteromeric-source-valid-control-rerun",
                    str(rerun_out),
                    "--out",
                    str(gap_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            gap = json.loads(gap_out.read_text(encoding="utf-8"))
            self.assertEqual(
                gap["metadata"]["gap_audit_status"],
                "blocked_review_only_source_free_role_acceptor_axes_missing",
            )
            self.assertEqual(
                gap["metadata"]["production_admissible_positive_like_count"], 0
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-heteromeric-source-free-role-rule-probe",
                    "--epk-heteromeric-candidate-source-validation-review",
                    str(validation),
                    "--out",
                    str(probe_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            probe = json.loads(probe_out.read_text(encoding="utf-8"))
            self.assertEqual(
                probe["metadata"]["source_free_rule_status"],
                "blocked_review_only_source_free_rule_false_hit_risk",
            )
            self.assertEqual(
                probe["metadata"]["nonaccepted_rule_hit_pdb_ids"],
                ["7M0T", "8ZN6"],
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-heteromeric-acceptor-chain-counteraxis-audit",
                    "--epk-heteromeric-candidate-source-validation-review",
                    str(validation),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(counteraxis_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            counteraxis = json.loads(counteraxis_out.read_text(encoding="utf-8"))
            self.assertEqual(
                counteraxis["metadata"]["counteraxis_status"],
                "passes_current_review_controls_not_scoring_admissible",
            )
            self.assertEqual(
                counteraxis["metadata"]["blocked_nonaccepted_rule_hit_pdb_ids"],
                ["7M0T", "8ZN6"],
            )
            self.assertEqual(
                counteraxis["metadata"]["residual_nonaccepted_rule_hit_count"], 0
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-heteromeric-broader-counteraxis-control-audit",
                    "--epk-heteromeric-positive-coverage-candidate-scout",
                    str(scout),
                    "--epk-heteromeric-candidate-source-validation-review",
                    str(validation),
                    "--epk-heteromeric-acceptor-chain-counteraxis-audit",
                    str(counteraxis_out),
                    "--epk-sibling-control-artifact",
                    str(sibling),
                    "--out",
                    str(broader_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            broader = json.loads(broader_out.read_text(encoding="utf-8"))
            self.assertEqual(
                broader["metadata"]["broader_counteraxis_status"],
                "passes_broader_review_controls_not_scoring_admissible",
            )
            self.assertEqual(
                broader["metadata"]["broader_heteromeric_reviewed_structure_count"],
                4,
            )
            self.assertEqual(
                broader["metadata"]["sibling_counteraxis_blocked_hit_count"], 1
            )
            self.assertEqual(
                broader["metadata"]["sibling_residual_false_hit_count"], 0
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-heteromeric-ligand-asymmetry-role-audit",
                    "--epk-heteromeric-broader-counteraxis-control-audit",
                    str(broader_out),
                    "--out",
                    str(asymmetry_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            asymmetry = json.loads(asymmetry_out.read_text(encoding="utf-8"))
            self.assertEqual(
                asymmetry["metadata"]["role_axis_status"],
                "passes_current_ligand_asymmetry_role_controls_not_scoring_admissible",
            )
            self.assertEqual(
                asymmetry["metadata"]["retained_source_valid_role_hit_count"],
                1,
            )
            self.assertEqual(asymmetry["metadata"]["nonaccepted_role_hit_count"], 0)

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-heteromeric-acceptor-identity-gap-audit",
                    "--epk-heteromeric-ligand-asymmetry-role-audit",
                    str(asymmetry_out),
                    "--epk-heteromeric-candidate-source-validation-review",
                    str(validation),
                    "--out",
                    str(identity_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            identity = json.loads(identity_out.read_text(encoding="utf-8"))
            self.assertEqual(
                identity["metadata"]["acceptor_identity_gap_status"],
                "blocked_review_only_source_free_acceptor_identity_missing",
            )
            self.assertEqual(identity["metadata"]["retained_role_hit_count"], 1)
            self.assertEqual(
                identity["metadata"]["source_free_acceptor_identity_ready_count"],
                0,
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-heteromeric-acceptor-identity-rule-probe",
                    "--epk-heteromeric-acceptor-identity-gap-audit",
                    str(identity_out),
                    "--epk-heteromeric-broader-counteraxis-control-audit",
                    str(broader_out),
                    "--out",
                    str(identity_rule_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            identity_rule = json.loads(identity_rule_out.read_text(encoding="utf-8"))
            self.assertEqual(
                identity_rule["metadata"]["identity_rule_status"],
                "passes_current_controls_but_generic_identity_axis_weak_review_only",
            )
            self.assertEqual(
                identity_rule["metadata"]["positive_identity_rule_hit_count"], 1
            )
            self.assertEqual(
                identity_rule["metadata"][
                    "nonaccepted_blocked_before_identity_rule_count"
                ],
                2,
            )
            self.assertEqual(
                identity_rule["metadata"][
                    "sibling_same_chain_blocked_before_identity_rule_count"
                ],
                1,
            )
            self.assertTrue(identity_rule["metadata"]["generic_identity_axis_weak"])
            self.assertEqual(
                identity_rule["metadata"]["source_free_acceptor_identity_ready_count"],
                0,
            )

    def test_build_epk_ligand_specific_5hvk_source_validity_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            cif_dir = root / "cif"
            cif_dir.mkdir()
            priority = root / "priority.json"
            kinase = root / "kinase.json"
            acceptor = root / "acceptor.json"
            out = root / "source_validity.json"
            (cif_dir / "5hvk.cif").write_text(
                """data_5HVK
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
""",
                encoding="utf-8",
            )
            priority.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_ligand_specific_5hvk_review_priority",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {"pdb_id": "5HVK", "accession": "P53667"},
                            {"pdb_id": "5HVK", "accession": "P23528"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            kinase.write_text(
                json.dumps(
                    {
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
                    }
                ),
                encoding="utf-8",
            )
            acceptor.write_text(
                json.dumps(
                    {
                        "record": {
                            "modified_residue_features": [
                                {
                                    "begin": 3,
                                    "description": "Phosphoserine; by NRK",
                                    "evidence": [{"evidence_code": "ECO:0000269"}],
                                }
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-ligand-specific-5hvk-source-validity-review",
                    "--epk-ligand-specific-5hvk-review-priority",
                    str(priority),
                    "--kinase-uniprot-entry",
                    str(kinase),
                    "--acceptor-uniprot-entry",
                    str(acceptor),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_ligand_specific_5hvk_source_validity_review",
            )
            self.assertEqual(
                metadata["source_validity_status"],
                "accepted_source_valid_kinase_substrate_cocomplex_review_only",
            )
            self.assertEqual(metadata["measurement_ready_candidate_count"], 1)
            self.assertEqual(
                metadata["nearest_source_phosphoacceptor_distance_angstrom"],
                3.0,
            )
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["curated_label_registry_edited"])
            self.assertFalse(metadata["fingerprint_registry_edited"])

    def test_build_epk_ligand_specific_5hvk_control_rerun_queue_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "source.json"
            prototype = root / "prototype.json"
            probe = root / "probe.json"
            out = root / "queue.json"
            source.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_ligand_specific_5hvk_source_validity_review"
                            ),
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
                    }
                ),
                encoding="utf-8",
            )
            prototype.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_review_only_scoring_prototype"
                        },
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
                    }
                ),
                encoding="utf-8",
            )
            probe.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_review_only_external_hard_negative_score_probe"
                            ),
                            "review_only_score_probe_non_abstention_count": 0,
                            "not_a_real_scored_reaudit": True,
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-ligand-specific-5hvk-control-rerun-queue",
                    "--epk-ligand-specific-5hvk-source-validity-review",
                    str(source),
                    "--epk-review-only-scoring-prototype",
                    str(prototype),
                    "--epk-review-only-external-hard-negative-score-probe",
                    str(probe),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            queue = json.loads(out.read_text(encoding="utf-8"))
            metadata = queue["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_ligand_specific_5hvk_control_rerun_queue",
            )
            self.assertEqual(
                metadata["control_rerun_queue_status"],
                "ready_for_review_only_control_rerun",
            )
            self.assertEqual(metadata["sibling_control_row_count"], 1)
            self.assertEqual(metadata["imported_external_hard_negative_row_count"], 1)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertTrue(metadata["not_a_real_scored_reaudit"])

    def test_build_epk_protein_substrate_positive_source_triage_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            queue = root / "queue.json"
            geometry = root / "geometry.json"
            retrieval = root / "retrieval.json"
            readiness = root / "readiness.json"
            protein = root / "protein.json"
            out = root / "source_triage.json"
            queue.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "active_learning_review_queue"},
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "known ePK",
                                "rank": 1,
                                "atp_phosphoryl_transfer_family_id": "epk",
                            },
                            {
                                "entry_id": "m_csa:760",
                                "entry_name": "new protein kinase",
                                "rank": 2,
                                "review_score": 6.8,
                                "atp_phosphoryl_transfer_family_id": "epk",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "mechanism_text_snippets": [
                                    "Serine substrate attacks ATP gamma phosphate."
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {"artifact": "active_site_geometry_features"},
                        "entries": [
                            {
                                "entry_id": "m_csa:760",
                                "entry_name": "new protein kinase",
                                "status": "ok",
                                "pdb_id": "1L0O",
                                "resolved_residue_count": 3,
                                "ligand_context": {
                                    "ligand_codes": ["ADP", "MG"],
                                    "structure_ligand_codes": ["ADP", "MG"],
                                    "cofactor_families": ["metal_ion"],
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            retrieval.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "geometry_aware_seed_fingerprint_retrieval"
                        },
                        "results": [
                            {
                                "entry_id": "m_csa:760",
                                "top_fingerprints": [
                                    {
                                        "fingerprint_id": (
                                            "metal_dependent_hydrolase"
                                        ),
                                        "score": 0.39,
                                        "counterevidence_reasons": [
                                            "nucleotide_transfer_ligand_context"
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            readiness.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_positive_fingerprint_readiness_packet"
                        },
                        "rows": [{"entry_id": "m_csa:35"}],
                    }
                ),
                encoding="utf-8",
            )
            protein.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_protein_substrate_acceptor_candidate_audit"
                            )
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:35",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-protein-substrate-positive-source-triage",
                    "--active-learning-queue",
                    str(queue),
                    "--geometry",
                    str(geometry),
                    "--retrieval",
                    str(retrieval),
                    "--epk-positive-fingerprint-readiness-packet",
                    str(readiness),
                    "--epk-protein-substrate-acceptor-candidate-audit",
                    str(protein),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            triage = json.loads(out.read_text(encoding="utf-8"))
            metadata = triage["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_protein_substrate_positive_source_triage",
            )
            self.assertEqual(metadata["candidate_row_count"], 1)
            self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
            self.assertEqual(metadata["product_state_repair_candidate_count"], 1)
            self.assertEqual(metadata["recommended_next_entry_id"], "m_csa:760")
            self.assertFalse(metadata["epk_score_computed"])
            row = triage["rows"][0]
            self.assertEqual(row["entry_id"], "m_csa:760")
            self.assertEqual(
                row["triage_decision"],
                "product_state_atp_repair_candidate_review_only",
            )
            self.assertTrue(row["has_product_state_nucleotide"])
            self.assertTrue(row["has_local_metal"])
            self.assertFalse(row["measurement_ready"])

    def test_build_epk_m_csa760_atp_state_repair_scan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            triage = root / "source_triage.json"
            remediation = root / "remediation.json"
            cif_dir = root / "cifs"
            cif_dir.mkdir()
            out = root / "repair_scan.json"

            def write_cif(path: Path, rows: list[str]) -> None:
                path.write_text(
                    "\n".join(
                        [
                            f"data_{path.stem}",
                            "loop_",
                            "_atom_site.group_PDB",
                            "_atom_site.auth_comp_id",
                            "_atom_site.label_comp_id",
                            "_atom_site.auth_asym_id",
                            "_atom_site.label_asym_id",
                            "_atom_site.auth_seq_id",
                            "_atom_site.label_seq_id",
                            "_atom_site.auth_atom_id",
                            "_atom_site.label_atom_id",
                            "_atom_site.Cartn_x",
                            "_atom_site.Cartn_y",
                            "_atom_site.Cartn_z",
                            *rows,
                            "#",
                        ]
                    ),
                    encoding="utf-8",
                )

            residue_rows = [
                "ATOM ASN ASN A A 50 50 CA CA 0.0 0.0 0.0",
                "ATOM GLU GLU A A 46 46 CA CA 1.0 0.0 0.0",
                "ATOM ARG ARG A A 105 105 CA CA 0.0 1.0 0.0",
            ]
            write_cif(
                cif_dir / "pdb_1L0O.cif",
                [
                    *residue_rows,
                    "HETATM ADP ADP A A 200 200 PB PB 1.0 1.0 0.0",
                    "HETATM MG MG A A 300 300 MG MG 2.0 1.0 0.0",
                ],
            )
            write_cif(
                cif_dir / "pdb_1TID.cif",
                [
                    *residue_rows,
                    "HETATM ATP ATP A A 200 200 PG PG 1.0 1.0 0.0",
                    "HETATM MG MG A A 300 300 MG MG 2.0 1.0 0.0",
                ],
            )
            write_cif(
                cif_dir / "pdb_1TH8.cif",
                [
                    *residue_rows,
                    "ATOM SER SER B B 58 58 OG OG 2.0 2.0 0.0",
                    "HETATM ADP ADP A A 200 200 PB PB 1.0 1.0 0.0",
                    "HETATM MG MG A A 300 300 MG MG 2.0 1.0 0.0",
                ],
            )
            triage.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_protein_substrate_positive_source_triage"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:760",
                                "entry_name": "non-specific kinase",
                                "pdb_id": "1L0O",
                                "mechanism_text_snippets": [
                                    "SpoIIAA Ser 58 attacks the gamma-phosphate of ATP."
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            remediation.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_remediation_plan"},
                        "rows": [
                            {
                                "entry_id": "m_csa:760",
                                "entry_name": "non-specific kinase",
                                "selected_pdb_id": "1L0O",
                                "candidate_pdb_structure_ids": [
                                    "1L0O",
                                    "1TID",
                                    "1TH8",
                                ],
                                "candidate_pdb_residue_positions": {
                                    "1L0O": [
                                        {
                                            "chain_name": "A",
                                            "code": "ASN",
                                            "resid": 50,
                                            "residue_node_id": (
                                                "m_csa:760:residue:1"
                                            ),
                                        },
                                        {
                                            "chain_name": "A",
                                            "code": "GLU",
                                            "resid": 46,
                                            "residue_node_id": (
                                                "m_csa:760:residue:2"
                                            ),
                                        },
                                        {
                                            "chain_name": "A",
                                            "code": "ARG",
                                            "resid": 105,
                                            "residue_node_id": (
                                                "m_csa:760:residue:3"
                                            ),
                                        },
                                    ]
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-m-csa760-atp-state-repair-scan",
                    "--epk-protein-substrate-positive-source-triage",
                    str(triage),
                    "--review-debt-remediation",
                    str(remediation),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            scan = json.loads(out.read_text(encoding="utf-8"))
            metadata = scan["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_m_csa760_atp_state_repair_scan",
            )
            self.assertEqual(metadata["candidate_pdb_count"], 3)
            self.assertEqual(metadata["atp_metal_state_candidate_count"], 1)
            self.assertEqual(
                metadata["protein_substrate_acceptor_context_candidate_count"],
                1,
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
            self.assertFalse(metadata["epk_score_computed"])
            rows = {row["pdb_id"]: row for row in scan["rows"]}
            self.assertEqual(
                rows["1TID"]["repair_scan_decision"],
                "atp_metal_state_without_protein_substrate_acceptor_review_only",
            )
            self.assertEqual(
                rows["1TH8"]["repair_scan_decision"],
                "substrate_acceptor_product_state_no_gamma_review_only",
            )
            for row in rows.values():
                self.assertTrue(row["review_only"])
                self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_m_csa757_active_state_repair_scan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            triage = root / "source_triage.json"
            remediation = root / "remediation.json"
            cif_dir = root / "cifs"
            cif_dir.mkdir()
            out = root / "repair_scan.json"

            def write_cif(path: Path, rows: list[str]) -> None:
                path.write_text(
                    "\n".join(
                        [
                            f"data_{path.stem}",
                            "loop_",
                            "_atom_site.group_PDB",
                            "_atom_site.auth_comp_id",
                            "_atom_site.label_comp_id",
                            "_atom_site.auth_asym_id",
                            "_atom_site.label_asym_id",
                            "_atom_site.auth_seq_id",
                            "_atom_site.label_seq_id",
                            "_atom_site.auth_atom_id",
                            "_atom_site.label_atom_id",
                            "_atom_site.Cartn_x",
                            "_atom_site.Cartn_y",
                            "_atom_site.Cartn_z",
                            *rows,
                            "#",
                        ]
                    ),
                    encoding="utf-8",
                )

            selected_rows = [
                "ATOM ASN ASN E E 171 171 CA CA 0.0 0.0 0.0",
                "ATOM ASP ASP E E 184 184 CA CA 1.0 0.0 0.0",
                "ATOM ASP ASP E E 166 166 CA CA 0.0 1.0 0.0",
                "ATOM LYS LYS E E 168 168 CA CA 1.0 1.0 0.0",
                "ATOM THR THR E E 201 201 CA CA 2.0 1.0 0.0",
            ]
            write_cif(
                cif_dir / "pdb_1STC.cif",
                [
                    *selected_rows,
                    "HETATM STU STU E E 300 300 C1 C1 2.0 2.0 0.0",
                    "HETATM TPO TPO E E 197 197 OG1 OG1 9.0 9.0 0.0",
                ],
            )
            homomer_rows = []
            for chain, offset in [("A", 0.0), ("B", 8.0)]:
                homomer_rows.extend(
                    [
                        f"ATOM ASN ASN {chain} {chain} 171 171 CA CA {offset + 0.0} 0.0 0.0",
                        f"ATOM ASP ASP {chain} {chain} 184 184 CA CA {offset + 1.0} 0.0 0.0",
                        f"ATOM ASP ASP {chain} {chain} 166 166 CA CA {offset + 0.0} 1.0 0.0",
                        f"ATOM LYS LYS {chain} {chain} 168 168 CA CA {offset + 1.0} 1.0 0.0",
                        f"ATOM THR THR {chain} {chain} 201 201 CA CA {offset + 2.0} 1.0 0.0",
                    ]
                )
            write_cif(
                cif_dir / "pdb_1CDK.cif",
                [
                    *homomer_rows,
                    "HETATM ANP ANP A A 400 400 PG PG 1.0 1.0 0.0",
                    "HETATM MN MN A A 401 401 MN MN 2.0 1.0 0.0",
                    "HETATM TPO TPO A A 197 197 OG1 OG1 8.0 8.0 0.0",
                ],
            )
            write_cif(
                cif_dir / "pdb_1Q24.cif",
                [
                    "ATOM ASN ASN A A 171 171 CA CA 0.0 0.0 0.0",
                    "ATOM ASP ASP A A 184 184 CA CA 1.0 0.0 0.0",
                    "ATOM ASP ASP A A 166 166 CA CA 0.0 1.0 0.0",
                    "ATOM LYS LYS A A 168 168 CA CA 1.0 1.0 0.0",
                    "ATOM THR THR A A 201 201 CA CA 2.0 1.0 0.0",
                    "HETATM ATP ATP A A 400 400 PG PG 1.0 1.0 0.0",
                    "HETATM MG MG A A 401 401 MG MG 2.0 1.0 0.0",
                    "HETATM TPO TPO A A 197 197 OG1 OG1 8.0 8.0 0.0",
                ],
            )
            triage.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_protein_substrate_positive_source_triage"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:757",
                                "entry_name": "cAMP-dependent protein kinase",
                                "pdb_id": "1STC",
                                "mechanism_text_snippets": [
                                    "Asp 166 activates the phosphoacceptor serine."
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            remediation.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_remediation_plan"},
                        "rows": [
                            {
                                "entry_id": "m_csa:757",
                                "entry_name": "cAMP-dependent protein kinase",
                                "selected_pdb_id": "1STC",
                                "candidate_pdb_structure_ids": [
                                    "1STC",
                                    "1CDK",
                                    "1Q24",
                                ],
                                "candidate_pdb_residue_positions": {
                                    "1STC": [
                                        {
                                            "chain_name": "E",
                                            "code": "ASN",
                                            "resid": 171,
                                        },
                                        {
                                            "chain_name": "E",
                                            "code": "ASP",
                                            "resid": 184,
                                        },
                                        {
                                            "chain_name": "E",
                                            "code": "ASP",
                                            "resid": 166,
                                        },
                                        {
                                            "chain_name": "E",
                                            "code": "LYS",
                                            "resid": 168,
                                        },
                                        {
                                            "chain_name": "E",
                                            "code": "THR",
                                            "resid": 201,
                                        },
                                    ]
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-m-csa757-active-state-repair-scan",
                    "--epk-protein-substrate-positive-source-triage",
                    str(triage),
                    "--review-debt-remediation",
                    str(remediation),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            scan = json.loads(out.read_text(encoding="utf-8"))
            metadata = scan["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_m_csa757_active_state_repair_scan",
            )
            self.assertEqual(metadata["candidate_pdb_count"], 3)
            self.assertEqual(metadata["scanned_candidate_pdb_count"], 3)
            self.assertEqual(metadata["active_state_atp_metal_candidate_count"], 2)
            self.assertEqual(
                metadata["active_state_atp_metal_candidate_pdb_ids"],
                ["1CDK", "1Q24"],
            )
            self.assertEqual(
                metadata["conservative_active_state_atp_metal_candidate_pdb_ids"],
                ["1Q24"],
            )
            self.assertEqual(
                metadata[
                    "homomeric_mapping_ambiguous_active_state_candidate_pdb_ids"
                ],
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

    def test_build_epk_m_csa756_5li1_residue_evidence_audit_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scan = root / "scan.json"
            remediation = root / "remediation.json"
            cif_dir = root / "cifs"
            cif_dir.mkdir()
            out = root / "5li1_audit.json"
            (cif_dir / "pdb_5LI1.cif").write_text(
                "\n".join(
                    [
                        "data_5LI1",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.auth_comp_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.auth_seq_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.auth_atom_id",
                        "_atom_site.label_atom_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "ATOM LYS LYS A A 380 380 CA CA 0.0 0.0 0.0",
                        "ATOM ASP ASP A A 382 382 CA CA 1.0 0.0 0.0",
                        "ATOM ASN ASN A A 383 383 CA CA 0.0 1.0 0.0",
                        "HETATM ANP ANP A A 900 900 PA PA 1.0 1.0 0.0",
                        "HETATM ANP ANP A A 900 900 PB PB 2.0 1.0 0.0",
                        "HETATM MG MG A A 901 901 MG MG 2.0 1.0 0.0",
                        "HETATM SEP SEP A A 484 484 OG OG 9.0 9.0 0.0",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            scan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_m_csa756_active_state_repair_scan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        }
                    }
                ),
                encoding="utf-8",
            )
            remediation.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_remediation_plan"},
                        "rows": [
                            {
                                "entry_id": "m_csa:756",
                                "entry_name": "protein kinase",
                                "selected_pdb_id": "1ATP",
                                "candidate_pdb_residue_position_counts": {
                                    "1ATP": 3,
                                    "5LI1": 0,
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-m-csa756-5li1-residue-evidence-audit",
                    "--epk-m-csa756-active-state-repair-scan",
                    str(scan),
                    "--review-debt-remediation",
                    str(remediation),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_m_csa756_5li1_residue_evidence_audit",
            )
            self.assertEqual(metadata["pdb_id"], "5LI1")
            self.assertTrue(metadata["active_site_residue_evidence_found"])
            self.assertFalse(metadata["terminal_gamma_atom_detected"])
            self.assertEqual(
                metadata["noncanonical_terminal_atom_names_detected"], ["PB"]
            )
            self.assertFalse(
                metadata["noncanonical_terminal_atom_policy_admissible"]
            )
            self.assertEqual(metadata["measurement_ready_candidate_count"], 0)
            self.assertEqual(
                metadata["repair_status"],
                "blocked_review_only_residue_evidence_lacks_terminal_gamma_atom_no_mapped_acceptor",
            )
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
            self.assertFalse(metadata["fingerprint_registry_edited"])
            self.assertFalse(metadata["curated_label_registry_edited"])

    def test_build_learned_retrieval_manifest_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            geometry = root / "geometry.json"
            retrieval = root / "retrieval.json"
            labels = root / "labels.json"
            out = root / "manifest.json"
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {"artifact": "active_site_geometry_features"},
                        "entries": [
                            {
                                "entry_id": "m_csa:1",
                                "entry_name": "labeled hydrolase",
                                "status": "ok",
                                "pdb_id": "1ABC",
                                "resolved_residue_count": 3,
                                "residues": [
                                    {"code": "Ser"},
                                    {"code": "His"},
                                    {"code": "Asp"},
                                ],
                                "pairwise_distances_angstrom": [{}, {}, {}],
                                "ligand_context": {"cofactor_families": ["metal"]},
                                "pocket_context": {
                                    "descriptors": {"polar_fraction": 0.2}
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            retrieval.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "geometry_aware_seed_fingerprint_retrieval"
                        },
                        "results": [
                            {
                                "entry_id": "m_csa:1",
                                "status": "ok",
                                "top_fingerprints": [
                                    {
                                        "fingerprint_id": "ser_his_acid_hydrolase",
                                        "score": 0.7,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "m_csa:1",
                            "fingerprint_id": "ser_his_acid_hydrolase",
                            "label_type": "seed_fingerprint",
                            "confidence": "high",
                            "rationale": "Curated test label with enough rationale.",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "evidence_score": 0.85,
                            "evidence": {"sources": ["test"]},
                        }
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-learned-retrieval-manifest",
                    "--geometry",
                    str(geometry),
                    "--retrieval",
                    str(retrieval),
                    "--labels",
                    str(labels),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            manifest = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(manifest["metadata"]["eligible_entry_count"], 1)
            self.assertTrue(manifest["rows"][0]["countable_training_label"])

    def test_audit_sequence_similarity_failure_sets_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            clusters = root / "clusters.json"
            labels = root / "labels.json"
            queue = root / "queue.json"
            out = root / "sequence_failures.json"
            clusters.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "cluster_source": "reference_uniprot_exact_set",
                            "cluster_count": 1,
                        },
                        "clusters": [
                            {
                                "sequence_cluster_id": "uniprot:P12345",
                                "entry_ids": ["m_csa:1", "m_csa:2"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "m_csa:1",
                            "fingerprint_id": "ser_his_acid_hydrolase",
                            "label_type": "seed_fingerprint",
                            "confidence": "high",
                            "rationale": "Curated test label with enough rationale.",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "evidence_score": 0.85,
                            "evidence": {"sources": ["test"]},
                        },
                        {
                            "entry_id": "m_csa:2",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "confidence": "medium",
                            "rationale": "Curated test label with enough rationale.",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "evidence_score": 0.65,
                            "evidence": {"sources": ["test"]},
                        },
                    ]
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:2",
                                "recommended_action": "expert_label_decision_needed",
                                "top1_ontology_family": "hydrolysis",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-sequence-similarity-failure-sets",
                    "--sequence-clusters",
                    str(clusters),
                    "--labels",
                    str(labels),
                    "--active-learning-queue",
                    str(queue),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(audit["metadata"]["duplicate_cluster_count"], 1)
            self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_check_label_preview_promotion_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            acceptance = root / "acceptance.json"
            summary = root / "summary.json"
            preview_debt = root / "preview_debt.json"
            current_debt = root / "current_debt.json"
            out = root / "readiness.json"
            acceptance.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "accepted_for_counting": True,
                            "accepted_new_label_count": 18,
                            "countable_label_count": 636,
                            "pending_review_count": 44,
                            "hard_negative_count": 0,
                            "near_miss_count": 0,
                            "out_of_scope_false_non_abstentions": 0,
                            "actionable_in_scope_failure_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            summary.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "blocker_count": 0,
                            "latest_countable_label_count": 636,
                            "total_accepted_new_label_count": 18,
                            "all_active_queues_retain_unlabeled_candidates": True,
                        }
                    }
                ),
                encoding="utf-8",
            )
            preview_debt.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_summary",
                            "review_debt_count": 61,
                            "needs_more_evidence_count": 44,
                            "new_review_debt_count": 1,
                            "new_review_debt_entry_ids": ["m_csa:650"],
                            "recommended_next_action_counts_by_debt_status": {
                                "new": {"verify_local_cofactor_or_active_site_mapping": 1}
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            current_debt.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_summary",
                            "review_debt_count": 53,
                            "needs_more_evidence_count": 37,
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "check-label-preview-promotion",
                    "--preview-acceptance",
                    str(acceptance),
                    "--preview-summary",
                    str(summary),
                    "--preview-review-debt",
                    str(preview_debt),
                    "--current-review-debt",
                    str(current_debt),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            readiness = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(readiness["metadata"]["promotion_recommendation"], "review_before_promoting")
            self.assertEqual(readiness["metadata"]["preview_new_review_debt_count"], 1)
            self.assertEqual(readiness["metadata"]["preview_new_review_debt_entry_ids"], ["m_csa:650"])
            self.assertEqual(
                readiness["metadata"]["preview_new_review_debt_next_action_counts"],
                {"verify_local_cofactor_or_active_site_mapping": 1},
            )

    def test_audit_label_scaling_quality_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            acceptance = root / "acceptance.json"
            readiness = root / "readiness.json"
            debt = root / "debt.json"
            gaps = root / "gaps.json"
            queue = root / "queue.json"
            guardrails = root / "guardrails.json"
            hard = root / "hard.json"
            decision = root / "decision.json"
            mapping = root / "mapping.json"
            sequence_clusters = root / "sequence_clusters.json"
            alternate_scan = root / "alternate_scan.json"
            remap_local_audit = root / "remap_local_audit.json"
            reaction_mismatch_audit = root / "reaction_mismatch_audit.json"
            expert_label_export = root / "expert_label_export.json"
            expert_label_repair = root / "expert_label_repair.json"
            expert_label_repair_guardrail = root / "expert_label_repair_guardrail.json"
            expert_label_local_gap = root / "expert_label_local_gap.json"
            expert_label_local_export = root / "expert_label_local_export.json"
            out = root / "audit.json"
            acceptance.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "label_batch_acceptance_check",
                            "out_of_scope_false_non_abstentions": 0,
                            "actionable_in_scope_failure_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            readiness.write_text(
                json.dumps({"metadata": {"promotion_recommendation": "review_before_promoting"}}),
                encoding="utf-8",
            )
            debt.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_summary",
                            "new_review_debt_entry_ids": ["m_csa:651", "m_csa:652"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            gaps.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_evidence_gap_analysis"},
                        "rows": [
                            {
                                "entry_id": "m_csa:651",
                                "entry_name": "accepted debt",
                                "decision_action": "accept_label",
                                "coverage_status": "expected_absent_from_structure",
                                "gap_reasons": ["top1_below_abstention_threshold"],
                                "counterevidence_reasons": ["absent_heme_context"],
                                "target_fingerprint_id": "heme_peroxidase_oxidase",
                                "top1_fingerprint_id": "heme_peroxidase_oxidase",
                                "mechanism_text_snippets": ["Hydrolysis text without heme evidence."],
                            },
                            {
                                "entry_id": "m_csa:652",
                                "entry_name": "decision-only PLP review",
                                "decision_action": "mark_needs_more_evidence",
                                "coverage_status": "all_expected_local",
                                "gap_reasons": ["review_marked_needs_more_evidence"],
                                "counterevidence_reasons": [],
                                "target_fingerprint_id": "plp_dependent_enzyme",
                                "top1_fingerprint_id": "plp_dependent_enzyme",
                                "mechanism_text_snippets": [
                                    "PLP support is local, but external review is still required."
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps(
                    {
                        "metadata": {"all_unlabeled_rows_retained": True},
                        "rows": [
                            {
                                "entry_id": "m_csa:650",
                                "recommended_action": "expert_label_decision_needed",
                                "top1_ontology_family": "hydrolysis",
                            },
                            {
                                "entry_id": "m_csa:651",
                                "top1_ontology_family": "heme_redox",
                            },
                            {
                                "entry_id": "m_csa:652",
                                "top1_ontology_family": "plp_chemistry",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            guardrails.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "family_propagation_guardrail_audit",
                            "blocker_counts": {},
                        },
                        "rows": [],
                    }
                ),
                encoding="utf-8",
            )
            hard.write_text(
                json.dumps({"metadata": {"hard_negative_count": 0, "near_miss_count": 0}}),
                encoding="utf-8",
            )
            decision.write_text(
                json.dumps(
                    {
                        "review_items": [
                            {"entry_id": "m_csa:651", "decision": {"action": "accept_label"}}
                        ]
                    }
                ),
                encoding="utf-8",
            )
            mapping.write_text(
                json.dumps({"metadata": {"issue_count": 0}, "rows": []}),
                encoding="utf-8",
            )
            sequence_clusters.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:651",
                                "sequence_cluster_id": "cluster-cli",
                            },
                            {
                                "entry_id": "m_csa:652",
                                "sequence_cluster_id": "cluster-cli-2",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            alternate_scan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_alternate_structure_scan",
                            "expected_family_hit_entry_ids": ["m_csa:651"],
                            "structure_wide_hit_without_local_support_entry_ids": [
                                "m_csa:651"
                            ],
                            "fetch_failure_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            remap_local_audit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_remap_local_lead_audit",
                            "countable_label_candidate_count": 0,
                            "strict_remap_guardrail_entry_ids": ["m_csa:651"],
                            "expert_family_boundary_review_entry_ids": [],
                            "local_structure_selection_rule_candidate_entry_ids": [
                                "m_csa:651"
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )
            reaction_mismatch_audit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "reaction_substrate_mismatch_audit",
                            "mismatch_count": 1,
                            "mismatch_entry_ids": ["m_csa:651"],
                            "mismatch_reason_counts": {
                                "kinase_name_with_hydrolase_top1": 1
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            expert_label_export.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_review_export",
                            "exported_count": 1,
                            "exported_entry_ids": ["m_csa:650"],
                            "countable_label_candidate_count": 0,
                            "decision_counts": {"no_decision": 1},
                            "export_ready": True,
                        },
                        "review_items": [{"entry_id": "m_csa:650"}],
                    }
                ),
                encoding="utf-8",
            )
            expert_label_repair.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_repair_candidate_summary",
                            "candidate_count": 1,
                            "candidate_entry_ids": ["m_csa:650"],
                            "countable_label_candidate_count": 0,
                        },
                        "rows": [{"entry_id": "m_csa:650"}],
                    }
                ),
                encoding="utf-8",
            )
            expert_label_repair_guardrail.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_repair_guardrail_audit",
                            "guardrail_ready": True,
                            "all_priority_lanes_non_countable": True,
                            "priority_repair_row_count": 1,
                            "countable_label_candidate_count": 0,
                        },
                        "rows": [{"entry_id": "m_csa:650"}],
                    }
                ),
                encoding="utf-8",
            )
            expert_label_local_gap.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_local_evidence_gap_audit",
                            "audit_ready": True,
                            "priority_rows_accounted_for": True,
                            "priority_repair_row_count": 1,
                            "audited_entry_count": 1,
                            "missing_priority_entry_ids": [],
                            "countable_label_candidate_count": 0,
                            "local_evidence_gap_class_counts": {
                                "selected_structure_residue_support_shortfall": 1
                            },
                        },
                        "rows": [{"entry_id": "m_csa:650"}],
                    }
                ),
                encoding="utf-8",
            )
            expert_label_local_export.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_local_evidence_review_export",
                            "export_ready": True,
                            "all_source_rows_exported": True,
                            "exported_count": 1,
                            "countable_label_candidate_count": 0,
                            "decision_counts": {"no_decision": 1},
                        },
                        "review_items": [{"entry_id": "m_csa:650"}],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-label-scaling-quality",
                    "--batch-id",
                    "test_preview",
                    "--acceptance",
                    str(acceptance),
                    "--readiness",
                    str(readiness),
                    "--review-debt",
                    str(debt),
                    "--review-evidence-gaps",
                    str(gaps),
                    "--active-learning-queue",
                    str(queue),
                    "--family-propagation-guardrails",
                    str(guardrails),
                    "--hard-negatives",
                    str(hard),
                    "--decision-batch",
                    str(decision),
                    "--structure-mapping",
                    str(mapping),
                    "--sequence-clusters",
                    str(sequence_clusters),
                    "--alternate-structure-scan",
                    str(alternate_scan),
                    "--remap-local-lead-audit",
                    str(remap_local_audit),
                    "--reaction-substrate-mismatch-audit",
                    str(reaction_mismatch_audit),
                    "--expert-label-decision-review-export",
                    str(expert_label_export),
                    "--expert-label-decision-repair-candidates",
                    str(expert_label_repair),
                    "--expert-label-decision-repair-guardrail-audit",
                    str(expert_label_repair_guardrail),
                    "--expert-label-decision-local-evidence-gap-audit",
                    str(expert_label_local_gap),
                    "--expert-label-decision-local-evidence-review-export",
                    str(expert_label_local_export),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(audit["metadata"]["batch_id"], "test_preview")
            self.assertEqual(
                audit["metadata"]["artifact_lineage"]["method"],
                "label_scaling_quality_cli_lineage_validation",
            )
            self.assertEqual(audit["metadata"]["accepted_new_debt_entry_ids"], ["m_csa:651"])
            self.assertEqual(audit["metadata"]["unclassified_new_review_debt_entry_ids"], [])
            self.assertEqual(
                audit["metadata"]["issue_class_counts"]["expert_review_decision_needed"],
                1,
            )
            self.assertIn("accepted_new_labels_without_review_debt", audit["blockers"])
            self.assertEqual(
                audit["metadata"]["near_duplicate_audit_status"],
                "not_observed_in_sequence_cluster_artifact",
            )
            self.assertTrue(audit["metadata"]["alternate_structure_scan_present"])
            self.assertTrue(audit["metadata"]["remap_local_lead_audit_present"])
            self.assertTrue(
                audit["metadata"]["reaction_substrate_mismatch_audit_present"]
            )
            self.assertTrue(
                audit["gates"][
                    "expert_label_decision_repair_candidates_cover_review_only_lanes"
                ]
            )
            self.assertTrue(
                audit["gates"]["expert_label_decision_local_evidence_gaps_audited"]
            )
            self.assertTrue(
                audit["gates"][
                    "expert_label_decision_local_evidence_review_export_ready"
                ]
            )
            self.assertEqual(
                audit["metadata"][
                    "expert_label_decision_repair_candidates_missing_entry_ids"
                ],
                [],
            )
            self.assertTrue(
                audit["metadata"][
                    "expert_label_decision_local_evidence_gap_audit_present"
                ]
            )
            self.assertTrue(
                audit["metadata"][
                    "expert_label_decision_local_evidence_review_export_present"
                ]
            )
            self.assertIn("alternate_structure_hits_lack_local_support", audit["review_warnings"])
            self.assertIn("remap_local_leads_require_strict_guardrail", audit["review_warnings"])
            self.assertIn("reaction_substrate_mismatch_audit_hits", audit["review_warnings"])

    def test_audit_label_scaling_quality_rejects_mixed_slice_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            required_paths = {
                "acceptance": root / "v3_label_batch_acceptance_check_650.json",
                "readiness": root / "v3_label_preview_promotion_readiness_675.json",
                "review_debt": root / "v3_review_debt_summary_650_preview.json",
                "review_evidence_gaps": root / "v3_review_evidence_gaps_650_preview.json",
                "active_learning_queue": root / "v3_active_learning_review_queue_650.json",
                "family_propagation_guardrails": root / "v3_family_propagation_guardrails_650.json",
                "hard_negatives": root / "v3_hard_negative_controls_650.json",
            }
            for path in required_paths.values():
                path.write_text(json.dumps({"metadata": {}}), encoding="utf-8")
            out = root / "audit.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-label-scaling-quality",
                    "--acceptance",
                    str(required_paths["acceptance"]),
                    "--readiness",
                    str(required_paths["readiness"]),
                    "--review-debt",
                    str(required_paths["review_debt"]),
                    "--review-evidence-gaps",
                    str(required_paths["review_evidence_gaps"]),
                    "--active-learning-queue",
                    str(required_paths["active_learning_queue"]),
                    "--family-propagation-guardrails",
                    str(required_paths["family_propagation_guardrails"]),
                    "--hard-negatives",
                    str(required_paths["hard_negatives"]),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "mismatched label-scaling quality artifact lineage",
                result.stderr,
            )
            self.assertFalse(out.exists())

    def test_check_label_batch_acceptance_rejects_mixed_slice_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            evaluation = root / "v3_geometry_label_eval_650.json"
            hard_negatives = root / "v3_hard_negative_controls_650.json"
            in_scope_failures = root / "v3_in_scope_failure_analysis_675.json"
            label_factory_gate = root / "v3_label_factory_gate_check_650.json"
            for path in (
                evaluation,
                hard_negatives,
                in_scope_failures,
                label_factory_gate,
            ):
                path.write_text(json.dumps({"metadata": {}}), encoding="utf-8")
            out = root / "acceptance.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "check-label-batch-acceptance",
                    "--review-state-labels",
                    str(root / "v3_imported_labels_batch_650.json"),
                    "--countable-labels",
                    str(root / "v3_countable_labels_batch_650.json"),
                    "--evaluation",
                    str(evaluation),
                    "--hard-negatives",
                    str(hard_negatives),
                    "--in-scope-failures",
                    str(in_scope_failures),
                    "--label-factory-gate",
                    str(label_factory_gate),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "mismatched label-batch acceptance artifact lineage",
                result.stderr,
            )
            self.assertFalse(out.exists())

    def test_external_blocker_matrix_rejects_mixed_slice_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = {
                "candidate_manifest": (
                    root / "v3_external_source_candidate_manifest_1025.json"
                ),
                "external_import_readiness_audit": (
                    root
                    / "v3_external_source_import_readiness_audit_1025.json"
                ),
                "active_site_sourcing_export": (
                    root
                    / "v3_external_source_active_site_sourcing_export_1025.json"
                ),
                "sequence_search_export": (
                    root / "v3_external_source_sequence_search_export_1025.json"
                ),
                "representation_backend_plan": (
                    root
                    / "v3_external_source_representation_backend_plan_1000.json"
                ),
                "active_site_sourcing_resolution": (
                    root
                    / "v3_external_source_active_site_sourcing_resolution_1025.json"
                ),
                "representation_backend_sample": (
                    root
                    / "v3_external_source_representation_backend_sample_1025.json"
                ),
            }
            for name, path in paths.items():
                slice_id = 1000 if name == "representation_backend_plan" else 1025
                path.write_text(
                    json.dumps(
                        {
                            "metadata": {
                                "method": name,
                                "source_slice_id": slice_id,
                            },
                            "rows": [],
                        }
                    ),
                    encoding="utf-8",
                )
            out = root / "matrix.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-transfer-blocker-matrix",
                    "--candidate-manifest",
                    str(paths["candidate_manifest"]),
                    "--external-import-readiness-audit",
                    str(paths["external_import_readiness_audit"]),
                    "--active-site-sourcing-export",
                    str(paths["active_site_sourcing_export"]),
                    "--sequence-search-export",
                    str(paths["sequence_search_export"]),
                    "--representation-backend-plan",
                    str(paths["representation_backend_plan"]),
                    "--active-site-sourcing-resolution",
                    str(paths["active_site_sourcing_resolution"]),
                    "--representation-backend-sample",
                    str(paths["representation_backend_sample"]),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "mismatched external transfer artifact lineage",
                result.stderr,
            )
            self.assertFalse(out.exists())

    def test_external_import_readiness_rejects_mixed_slice_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = {
                "candidate_manifest": (
                    root / "v3_external_source_candidate_manifest_1025.json"
                ),
                "active_site_evidence_sample": (
                    root / "v3_external_source_active_site_evidence_sample_1025.json"
                ),
                "heuristic_control_scores": (
                    root / "v3_external_source_heuristic_control_scores_1025.json"
                ),
                "representation_control_comparison": (
                    root
                    / "v3_external_source_representation_control_comparison_1000.json"
                ),
                "active_site_gap_source_requests": (
                    root
                    / "v3_external_source_active_site_gap_source_requests_1025.json"
                ),
                "sequence_neighborhood_sample": (
                    root / "v3_external_source_sequence_neighborhood_sample_1025.json"
                ),
                "sequence_alignment_verification": (
                    root
                    / "v3_external_source_sequence_alignment_verification_1025.json"
                ),
            }
            for name, path in paths.items():
                slice_id = 1000 if name == "representation_control_comparison" else 1025
                path.write_text(
                    json.dumps(
                        {
                            "metadata": {
                                "method": name,
                                "source_slice_id": slice_id,
                            },
                            "rows": [],
                        }
                    ),
                    encoding="utf-8",
                )
            out = root / "import_readiness.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-external-source-import-readiness",
                    "--candidate-manifest",
                    str(paths["candidate_manifest"]),
                    "--active-site-evidence-sample",
                    str(paths["active_site_evidence_sample"]),
                    "--heuristic-control-scores",
                    str(paths["heuristic_control_scores"]),
                    "--representation-control-comparison",
                    str(paths["representation_control_comparison"]),
                    "--active-site-gap-source-requests",
                    str(paths["active_site_gap_source_requests"]),
                    "--sequence-neighborhood-sample",
                    str(paths["sequence_neighborhood_sample"]),
                    "--sequence-alignment-verification",
                    str(paths["sequence_alignment_verification"]),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "mismatched external transfer artifact lineage",
                result.stderr,
            )
            self.assertFalse(out.exists())

    def test_build_external_pilot_packet_rejects_mixed_slice_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = {
                "pilot_candidate_priority": (
                    root / "v3_external_source_pilot_candidate_priority_1025.json"
                ),
                "active_site_sourcing_export": (
                    root / "v3_external_source_active_site_sourcing_export_1000.json"
                ),
                "sequence_search_export": (
                    root / "v3_external_source_sequence_search_export_1025.json"
                ),
            }
            for name, path in paths.items():
                slice_id = 1000 if name == "active_site_sourcing_export" else 1025
                path.write_text(
                    json.dumps(
                        {
                            "metadata": {
                                "method": name,
                                "source_slice_id": slice_id,
                            },
                            "rows": [],
                        }
                    ),
                    encoding="utf-8",
                )
            out = root / "packet.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-pilot-evidence-packet",
                    "--pilot-candidate-priority",
                    str(paths["pilot_candidate_priority"]),
                    "--active-site-sourcing-export",
                    str(paths["active_site_sourcing_export"]),
                    "--sequence-search-export",
                    str(paths["sequence_search_export"]),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "mismatched external transfer artifact lineage",
                result.stderr,
            )
            self.assertFalse(out.exists())

    def test_build_external_pilot_dossiers_rejects_mixed_slice_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = {
                "pilot_evidence_packet": (
                    root / "v3_external_source_pilot_evidence_packet_1025.json"
                ),
                "active_site_evidence_sample": (
                    root / "v3_external_source_active_site_evidence_sample_1000.json"
                ),
                "active_site_sourcing_resolution": (
                    root
                    / "v3_external_source_active_site_sourcing_resolution_1025.json"
                ),
                "reaction_evidence_sample": (
                    root / "v3_external_source_reaction_evidence_sample_1025.json"
                ),
                "sequence_alignment_verification": (
                    root
                    / "v3_external_source_sequence_alignment_verification_1025.json"
                ),
                "representation_backend_sample": (
                    root
                    / "v3_external_source_pilot_representation_backend_sample_1025.json"
                ),
                "heuristic_control_scores": (
                    root / "v3_external_source_heuristic_control_scores_1025.json"
                ),
                "structure_mapping_sample": (
                    root / "v3_external_source_structure_mapping_sample_1025.json"
                ),
                "transfer_blocker_matrix": (
                    root / "v3_external_source_transfer_blocker_matrix_1025.json"
                ),
                "external_import_readiness_audit": (
                    root
                    / "v3_external_source_import_readiness_audit_1025.json"
                ),
            }
            for name, path in paths.items():
                slice_id = 1000 if name == "active_site_evidence_sample" else 1025
                path.write_text(
                    json.dumps(
                        {
                            "metadata": {
                                "method": name,
                                "source_slice_id": slice_id,
                            },
                            "rows": [],
                        }
                    ),
                    encoding="utf-8",
                )
            out = root / "dossiers.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-pilot-evidence-dossiers",
                    "--pilot-evidence-packet",
                    str(paths["pilot_evidence_packet"]),
                    "--active-site-evidence-sample",
                    str(paths["active_site_evidence_sample"]),
                    "--active-site-sourcing-resolution",
                    str(paths["active_site_sourcing_resolution"]),
                    "--reaction-evidence-sample",
                    str(paths["reaction_evidence_sample"]),
                    "--sequence-alignment-verification",
                    str(paths["sequence_alignment_verification"]),
                    "--representation-backend-sample",
                    str(paths["representation_backend_sample"]),
                    "--heuristic-control-scores",
                    str(paths["heuristic_control_scores"]),
                    "--structure-mapping-sample",
                    str(paths["structure_mapping_sample"]),
                    "--transfer-blocker-matrix",
                    str(paths["transfer_blocker_matrix"]),
                    "--external-import-readiness-audit",
                    str(paths["external_import_readiness_audit"]),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "mismatched external transfer artifact lineage",
                result.stderr,
            )
            self.assertFalse(out.exists())

    def test_build_external_pilot_active_site_decisions_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = {
                "pilot_evidence_dossiers": (
                    root / "v3_external_source_pilot_evidence_dossiers_1025.json"
                ),
                "pilot_evidence_packet": (
                    root / "v3_external_source_pilot_evidence_packet_1025.json"
                ),
                "active_site_sourcing_resolution": (
                    root
                    / "v3_external_source_active_site_sourcing_resolution_1025.json"
                ),
                "reaction_evidence_sample": (
                    root / "v3_external_source_reaction_evidence_sample_1025.json"
                ),
                "backend_sequence_search": (
                    root / "v3_external_source_backend_sequence_search_1025.json"
                ),
                "pilot_representation_backend_sample": (
                    root
                    / "v3_external_source_pilot_representation_backend_sample_1025.json"
                ),
                "transfer_blocker_matrix": (
                    root / "v3_external_source_transfer_blocker_matrix_1025.json"
                ),
            }
            payloads = {
                "pilot_evidence_dossiers": {
                    "metadata": {
                        "method": "external_source_pilot_evidence_dossier",
                        "source_slice_id": 1025,
                    },
                    "rows": [
                        {
                            "rank": 1,
                            "accession": "P12345",
                            "entry_id": "uniprot:P12345",
                            "lane_id": "external_source:lyase",
                            "active_site_evidence": {
                                "explicit_active_site_feature_count": 1,
                                "binding_site_feature_count": 0,
                            },
                            "reaction_evidence": {
                                "reaction_record_count": 1,
                                "specific_reaction_record_count": 1,
                                "rhea_ids": ["RHEA:1"],
                            },
                            "sequence_evidence": {
                                "backend_search_complete": True,
                                "backend_search_status": "no_near_duplicate_signal",
                            },
                            "representation_control": {
                                "backend_status": (
                                    "learned_representation_sample_complete"
                                ),
                                "comparison_status": (
                                    "pilot_sequence_embedding_control"
                                ),
                            },
                            "remaining_blockers": [
                                "external_review_decision_artifact_not_built"
                            ],
                        }
                    ],
                },
                "pilot_evidence_packet": {
                    "metadata": {
                        "method": "external_source_pilot_evidence_packet",
                        "source_slice_id": 1025,
                    },
                    "rows": [
                        {
                            "accession": "P12345",
                            "pilot_selection_status": "selected_for_review_pilot",
                        }
                    ],
                },
                "active_site_sourcing_resolution": {
                    "metadata": {
                        "method": "external_source_active_site_sourcing_resolution",
                        "source_slice_id": 1025,
                    },
                    "rows": [],
                },
                "reaction_evidence_sample": {
                    "metadata": {
                        "method": "external_source_reaction_evidence_sample",
                        "source_slice_id": 1025,
                    },
                    "rows": [],
                },
                "backend_sequence_search": {
                    "metadata": {
                        "method": "external_source_backend_sequence_search",
                        "source_slice_id": 1025,
                    },
                    "rows": [
                        {
                            "accession": "P12345",
                            "backend_name": "mmseqs2_easy_search",
                            "backend_search_complete": True,
                            "search_status": "no_near_duplicate_signal",
                        }
                    ],
                },
                "pilot_representation_backend_sample": {
                    "metadata": {
                        "method": "external_source_representation_backend_sample",
                        "source_slice_id": 1025,
                    },
                    "rows": [
                        {
                            "accession": "P12345",
                            "backend_status": (
                                "learned_representation_sample_complete"
                            ),
                            "comparison_status": (
                                "pilot_sequence_embedding_control"
                            ),
                        }
                    ],
                },
                "transfer_blocker_matrix": {
                    "metadata": {
                        "method": "external_source_transfer_blocker_matrix",
                        "source_slice_id": 1025,
                    },
                    "rows": [{"accession": "P12345", "blockers": []}],
                },
            }
            for name, path in paths.items():
                path.write_text(json.dumps(payloads[name]), encoding="utf-8")
            out = root / "decisions.json"

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-pilot-active-site-evidence-decisions",
                    "--pilot-evidence-dossiers",
                    str(paths["pilot_evidence_dossiers"]),
                    "--pilot-evidence-packet",
                    str(paths["pilot_evidence_packet"]),
                    "--active-site-sourcing-resolution",
                    str(paths["active_site_sourcing_resolution"]),
                    "--reaction-evidence-sample",
                    str(paths["reaction_evidence_sample"]),
                    "--backend-sequence-search",
                    str(paths["backend_sequence_search"]),
                    "--pilot-representation-backend-sample",
                    str(paths["pilot_representation_backend_sample"]),
                    "--transfer-blocker-matrix",
                    str(paths["transfer_blocker_matrix"]),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["metadata"]["method"],
                "external_source_pilot_active_site_evidence_decisions",
            )
            self.assertEqual(
                payload["metadata"]["artifact_lineage"]["blocker_removed"],
                "external_pilot_active_site_source_status_ambiguity",
            )
            self.assertEqual(payload["metadata"]["candidate_count"], 1)
            self.assertEqual(payload["metadata"]["countable_label_candidate_count"], 0)
            self.assertFalse(payload["metadata"]["ready_for_label_import"])
            self.assertEqual(
                payload["rows"][0]["active_site_evidence_decision_status"],
                "explicit_active_site_source_present",
            )

    def test_next_candidate_factory_import_gate_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            terminal = root / "v3_external_hard_negative_next_candidate_terminal_review_decisions_1025.json"
            label_gate = root / "v3_label_factory_gate_check_1025_preview.json"
            transfer_gate = root / "v3_external_source_transfer_gate_check_1025.json"
            labels = root / "curated_mechanism_labels.json"
            out = root / "v3_external_hard_negative_next_candidate_factory_import_gate_1025.json"
            terminal.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "external_hard_negative_next_candidate_terminal_"
                                "review_decisions"
                            )
                        },
                        "rows": [
                            {
                                "accession": "PLOW",
                                "entry_id": "uniprot:PLOW",
                                "lane_id": "external_source:lyase",
                                "target_label_type": "out_of_scope",
                                "target_fingerprint_id": None,
                                "ontology_version_at_decision": (
                                    "label_factory_v1_8fp"
                                ),
                                "terminal_review_decision_status": (
                                    "accepted_out_of_scope_pending_factory_gate"
                                ),
                                "source_evidence_status": (
                                    "explicit_active_site_and_catalytic_activity_"
                                    "source_present"
                                ),
                                "bounded_duplicate_evidence_status": (
                                    "bounded_duplicate_controls_clear_uniref_pending"
                                ),
                                "uniref_current_reference_screen_status": (
                                    "uniref_current_reference_screen_no_current_"
                                    "reference_overlap"
                                ),
                                "remaining_import_blockers": [
                                    "full_label_factory_gate_not_run"
                                ],
                                "out_of_scope_inverse_gate": {
                                    "target_fingerprint_id": None,
                                    "inverse_gate_status": "passed",
                                    "all_current_fingerprint_scores_below_threshold": True,
                                    "observed_current_fingerprint_count": 8,
                                    "expected_current_fingerprint_count": 8,
                                    "max_current_fingerprint_score": 0.2,
                                },
                                "max_current_fingerprint_score": 0.2,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            label_gate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "label_factory_gate_check",
                            "gate_count": 21,
                            "passed_gate_count": 21,
                        },
                        "blockers": [],
                    }
                ),
                encoding="utf-8",
            )
            transfer_gate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_transfer_gate_check",
                            "gate_count": 68,
                            "passed_gate_count": 68,
                        },
                        "blockers": [],
                    }
                ),
                encoding="utf-8",
            )
            labels.write_text("[]", encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-hard-negative-next-candidate-factory-import-gate",
                    "--terminal-review-decisions",
                    str(terminal),
                    "--label-factory-gate-check",
                    str(label_gate),
                    "--external-transfer-gate",
                    str(transfer_gate),
                    "--labels",
                    str(labels),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["metadata"]["method"],
                "external_hard_negative_next_candidate_factory_import_gate",
            )
            self.assertEqual(payload["metadata"]["selected_import_accessions"], ["PLOW"])
            self.assertEqual(payload["metadata"]["import_ready_candidate_count"], 1)
            self.assertEqual(
                payload["review_items"][0]["decision"]["action"], "accept_label"
            )

    def test_external_transfer_gate_help_exposes_pilot_active_site_input(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "catalytic_earth.cli",
                "check-external-source-transfer-gates",
                "--help",
            ],
            cwd=ROOT,
            env={"PYTHONPATH": str(ROOT / "src")},
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("--pilot-active-site-evidence-decisions", result.stdout)

    def test_automation_lock_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_dir = Path(tmpdir) / "run.lock"
            env = {"PYTHONPATH": str(ROOT / "src")}
            acquire = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "acquire",
                    "--started-at",
                    "2026-05-10T00:00:00Z",
                    "--skip-worktree-check",
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            acquired = json.loads(acquire.stdout)
            self.assertTrue(acquired["acquired"])
            self.assertEqual(acquired["status"], "acquired")
            self.assertTrue((lock_dir / "pid").exists())
            blocked = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "acquire",
                    "--started-at",
                    "2026-05-10T00:01:00Z",
                    "--skip-worktree-check",
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(blocked.returncode, 3)
            self.assertEqual(json.loads(blocked.stdout)["status"], "active_lock_present")
            status = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "status",
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(json.loads(status.stdout)["status"], "active_lock_present")
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "release",
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse(lock_dir.exists())

    def test_automation_lock_release_can_require_clean_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True, text=True)
            lock_dir = Path(tmpdir) / "run.lock"
            env = {"PYTHONPATH": str(ROOT / "src")}
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "--repo-root",
                    str(repo),
                    "acquire",
                    "--started-at",
                    "2026-05-10T00:00:00Z",
                    "--skip-worktree-check",
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")
            blocked = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "--repo-root",
                    str(repo),
                    "release",
                    "--require-clean",
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(blocked.returncode, 4)
            self.assertIn("worktree_dirty", json.loads(blocked.stdout)["blockers"])
            self.assertTrue(lock_dir.exists())
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "--repo-root",
                    str(repo),
                    "release",
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse(lock_dir.exists())

    def test_artifact_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger = Path(tmpdir) / "source_ledger.json"
            demo = Path(tmpdir) / "mechanism_demo.json"
            score_margins = Path(tmpdir) / "score_margins.json"
            hard_negatives = Path(tmpdir) / "hard_negatives.json"
            in_scope_failures = Path(tmpdir) / "in_scope_failures.json"
            cofactor_coverage = Path(tmpdir) / "cofactor_coverage.json"
            cofactor_policy = Path(tmpdir) / "cofactor_policy.json"
            seed_family_performance = Path(tmpdir) / "seed_family_performance.json"
            label_candidates = Path(tmpdir) / "label_candidates.json"
            label_factory = Path(tmpdir) / "label_factory.json"
            applied_factory = Path(tmpdir) / "applied_factory.json"
            active_queue = Path(tmpdir) / "active_queue.json"
            adversarial_negatives = Path(tmpdir) / "adversarial_negatives.json"
            review_export = Path(tmpdir) / "review_export.json"
            decision_batch = Path(tmpdir) / "decision_batch.json"
            imported_labels = Path(tmpdir) / "imported_labels.json"
            countable_labels = Path(tmpdir) / "countable_labels.json"
            gate_check = Path(tmpdir) / "gate_check.json"
            review_resolution = Path(tmpdir) / "review_resolution.json"
            review_gaps = Path(tmpdir) / "review_gaps.json"
            family_guardrails = Path(tmpdir) / "family_guardrails.json"
            migrated_labels = Path(tmpdir) / "migrated_labels.json"
            mapping_issues = Path(tmpdir) / "mapping_issues.json"
            calibration = Path(tmpdir) / "calibration.json"
            slice_summary = Path(tmpdir) / "slice_summary.json"
            subprocess.run(
                [sys.executable, "-m", "catalytic_earth.cli", "build-ledger", "--out", str(ledger)],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [sys.executable, "-m", "catalytic_earth.cli", "fingerprint-demo", "--out", str(demo)],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-geometry-score-margins",
                    "--out",
                    str(score_margins),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-seed-family-performance",
                    "--out",
                    str(seed_family_performance),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-cofactor-policy",
                    "--out",
                    str(cofactor_policy),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-cofactor-coverage",
                    "--out",
                    str(cofactor_coverage),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-hard-negative-controls",
                    "--out",
                    str(hard_negatives),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-in-scope-failures",
                    "--out",
                    str(in_scope_failures),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-label-expansion-candidates",
                    "--out",
                    str(label_candidates),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "migrate-label-registry",
                    "--out",
                    str(migrated_labels),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-label-factory-audit",
                    "--out",
                    str(label_factory),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "apply-label-factory-actions",
                    "--label-factory-audit",
                    str(label_factory),
                    "--out",
                    str(applied_factory),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-active-learning-queue",
                    "--label-factory-audit",
                    str(label_factory),
                    "--out",
                    str(active_queue),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "export-label-review",
                    "--queue",
                    str(active_queue),
                    "--out",
                    str(review_export),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-review-decision-batch",
                    "--review",
                    str(review_export),
                    "--batch-id",
                    "test_batch",
                    "--out",
                    str(decision_batch),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-review-evidence-gaps",
                    "--review",
                    str(decision_batch),
                    "--out",
                    str(review_gaps),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-adversarial-negatives",
                    "--out",
                    str(adversarial_negatives),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-family-propagation-guardrails",
                    "--out",
                    str(family_guardrails),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "check-label-factory-gates",
                    "--label-factory-audit",
                    str(label_factory),
                    "--applied-label-factory",
                    str(applied_factory),
                    "--active-learning-queue",
                    str(active_queue),
                    "--adversarial-negatives",
                    str(adversarial_negatives),
                    "--expert-review-export",
                    str(review_export),
                    "--family-propagation-guardrails",
                    str(family_guardrails),
                    "--out",
                    str(gate_check),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "import-label-review",
                    "--review",
                    str(decision_batch),
                    "--out",
                    str(imported_labels),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "import-countable-label-review",
                    "--review",
                    str(decision_batch),
                    "--out",
                    str(countable_labels),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "check-label-review-resolution",
                    "--baseline-label-count",
                    "499",
                    "--review",
                    str(decision_batch),
                    "--review-state-labels",
                    str(imported_labels),
                    "--countable-labels",
                    str(countable_labels),
                    "--label-expansion-candidates",
                    str(label_candidates),
                    "--label-factory-gate",
                    str(gate_check),
                    "--out",
                    str(review_resolution),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-structure-mapping-issues",
                    "--out",
                    str(mapping_issues),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "summarize-geometry-slices",
                    "--artifact-dir",
                    "artifacts",
                    "--out",
                    str(slice_summary),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "calibrate-abstention",
                    "--out",
                    str(calibration),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(ledger.exists())
            self.assertTrue(demo.exists())
            self.assertIn("score_separation_gap", json.loads(score_margins.read_text())["metadata"])
            self.assertIn("hard_negative_count", json.loads(hard_negatives.read_text())["metadata"])
            self.assertIn(
                "target_fingerprint_counts",
                json.loads(in_scope_failures.read_text())["metadata"],
            )
            self.assertIn(
                "coverage_status_counts",
                json.loads(cofactor_coverage.read_text())["metadata"],
            )
            self.assertIn(
                "recommendation",
                json.loads(cofactor_policy.read_text())["metadata"],
            )
            self.assertIn(
                "in_scope_family_count",
                json.loads(seed_family_performance.read_text())["metadata"],
            )
            self.assertIn(
                "ready_for_label_review_count",
                json.loads(label_candidates.read_text())["metadata"],
            )
            self.assertIn("tier", json.loads(migrated_labels.read_text())[0])
            self.assertIn("promote_to_silver_count", json.loads(label_factory.read_text())["metadata"])
            self.assertIn("output_summary", json.loads(applied_factory.read_text())["metadata"])
            self.assertIn("ranking_terms", json.loads(active_queue.read_text())["metadata"])
            self.assertIn("axis_counts", json.loads(adversarial_negatives.read_text())["metadata"])
            self.assertIn("decision_schema", json.loads(review_export.read_text())["metadata"])
            self.assertIn("decision_counts", json.loads(decision_batch.read_text())["metadata"])
            self.assertIn("automation_ready_for_next_label_batch", json.loads(gate_check.read_text())["metadata"])
            self.assertIn("resolved_for_scaling", json.loads(review_resolution.read_text())["metadata"])
            self.assertIn("gap_reason_counts", json.loads(review_gaps.read_text())["metadata"])
            self.assertIn("source_guardrails", json.loads(family_guardrails.read_text())["metadata"])
            self.assertGreaterEqual(len(json.loads(imported_labels.read_text())), 475)
            self.assertLessEqual(len(json.loads(countable_labels.read_text())), len(json.loads(imported_labels.read_text())))
            self.assertIn("status_counts", json.loads(mapping_issues.read_text())["metadata"])
            self.assertEqual(json.loads(slice_summary.read_text())["metadata"]["largest_slice"], "1000")
            self.assertGreater(json.loads(calibration.read_text())["metadata"]["threshold_count"], 21)

    def test_build_epk_ligand_specific_active_query_extension_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scout = root / "scout.json"
            review = root / "review.json"
            out = root / "extension.json"
            scout.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_positive_coverage_candidate_scout"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "source_query": "test active query rows100-119",
                        },
                        "rows": [
                            {
                                "pdb_id": "5HVK",
                                "candidate_status": (
                                    "heteromeric_candidate_source_validation_pending_review_only"
                                ),
                                "heteromeric_candidate_hit_count": 1,
                                "heteromeric_candidate_hits": [
                                    {
                                        "candidate_chain_name": "D",
                                        "gamma_associated_polymer_chain_name": "C",
                                        "nearest_gamma_distance_angstrom": 4.2,
                                    }
                                ],
                            },
                            {
                                "pdb_id": "9UUR",
                                "candidate_status": (
                                    "heteromeric_candidate_source_validation_pending_review_only"
                                ),
                                "heteromeric_candidate_hit_count": 1,
                                "heteromeric_candidate_hits": [
                                    {
                                        "candidate_chain_name": "B",
                                        "gamma_associated_polymer_chain_name": "A",
                                        "nearest_gamma_distance_angstrom": 4.1,
                                    }
                                ],
                            },
                            {
                                "pdb_id": "9UW4",
                                "candidate_status": (
                                    "heteromeric_candidate_source_validation_pending_review_only"
                                ),
                                "heteromeric_candidate_hit_count": 1,
                                "heteromeric_candidate_hits": [
                                    {
                                        "candidate_chain_name": "A",
                                        "gamma_associated_polymer_chain_name": "A",
                                        "nearest_gamma_distance_angstrom": 4.2,
                                    }
                                ],
                            },
                            {
                                "pdb_id": "1ABC",
                                "candidate_status": (
                                    "no_heteromeric_candidate_hit_review_only"
                                ),
                                "heteromeric_candidate_hit_count": 0,
                                "heteromeric_candidate_hits": [],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_candidate_source_validation_review"
                            )
                        },
                        "rows": [
                            {
                                "pdb_id": "9UUR",
                                "source_validation_status": (
                                    "blocked_source_context_insufficient_review_only"
                                ),
                                "source_validated_positive_like": False,
                                "structure_title": (
                                    "The complex of human pMEK1 and uERK1 (ANP)"
                                ),
                                "entity_descriptions": [
                                    "Dual specificity mitogen-activated protein kinase kinase 1",
                                    "Mitogen-activated protein kinase 3",
                                ],
                                "chain_accessions": {
                                    "A": ["Q02750"],
                                    "B": ["P27361"],
                                },
                            },
                            {
                                "pdb_id": "9UW4",
                                "source_validation_status": (
                                    "blocked_source_context_insufficient_review_only"
                                ),
                                "source_validated_positive_like": False,
                                "structure_title": (
                                    "The complex of human pMEK1 and uERK1 (ANP)"
                                ),
                                "chain_accessions": {
                                    "A": ["Q02750"],
                                    "B": ["P27361"],
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-ligand-specific-active-query-extension-audit",
                    "--epk-ligand-specific-active-query-candidate-scout",
                    str(scout),
                    "--epk-ligand-specific-active-query-source-validation-review",
                    str(review),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["active_query_extension_status"],
                "blocked_review_only_mek_erk_role_direction_and_acceptor_state_unresolved",
            )
            self.assertEqual(metadata["reviewed_structure_count"], 4)
            self.assertEqual(metadata["known_positive_repeat_hit_pdb_ids"], ["5HVK"])
            self.assertEqual(metadata["new_topology_hit_pdb_ids"], ["9UUR", "9UW4"])
            self.assertEqual(
                metadata["mek_erk_role_direction_blocker_pdb_ids"],
                ["9UUR", "9UW4"],
            )
            self.assertEqual(
                metadata["same_author_chain_topology_artifact_risk_pdb_ids"],
                ["9UW4"],
            )
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_mek_erk_phosphosite_source_review_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            cif_dir = root / "cifs"
            cif_dir.mkdir()
            review = root / "review.json"
            records = root / "records.json"
            out = root / "mek_erk_review.json"
            review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_candidate_source_validation_review"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "pdb_id": "9TST",
                                "source_pair_id": "mek1_erk1",
                                "source_validation_status": (
                                    "blocked_mek_erk_role_direction_or_phosphosite_state_unresolved_review_only"
                                ),
                                "structure_title": "MEK1/ERK1 test complex",
                                "chain_accessions": {
                                    "A": ["Q02750"],
                                    "B": ["P27361"],
                                },
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
                ),
                encoding="utf-8",
            )
            (cif_dir / "9TST.cif").write_text(
                """
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
""",
                encoding="utf-8",
            )
            records.write_text(
                json.dumps(
                    {
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
                                    "description": (
                                        "Phosphotyrosine; by MAP2K1 and MAP2K2"
                                    ),
                                    "evidence": [],
                                }
                            ],
                        },
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-mek-erk-phosphosite-source-review",
                    "--epk-mek-erk-source-validation-review",
                    str(review),
                    "--uniprot-records-by-accession",
                    str(records),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            metadata = payload["metadata"]
            self.assertEqual(
                metadata["method"], "epk_mek_erk_phosphosite_source_review"
            )
            self.assertEqual(metadata["source_authoritative_measurement_ready_count"], 1)
            self.assertEqual(
                metadata["source_authoritative_measurement_ready_pdb_ids"], ["9TST"]
            )
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertEqual(payload["rows"][0]["candidate_uniprot_position"], 204)

    def test_build_epk_mek_erk_role_control_rerun_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_review = root / "source_review.json"
            protein_role = root / "protein_role.json"
            midlength = root / "midlength.json"
            out = root / "role_rerun.json"
            source_review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_mek_erk_phosphosite_source_review",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": (
                                    "mek_erk_phosphosite_source_review_candidate"
                                ),
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
                ),
                encoding="utf-8",
            )
            protein_role.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_source_free_protein_substrate_role_discriminator_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "protein_role_control_false_hit_count": 0,
                            "protein_role_external_hard_negative_non_abstention_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            midlength.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_midlength_protein_role_counteraxis_audit",
                            "residual_protein_role_false_hit_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-mek-erk-role-control-rerun",
                    "--epk-mek-erk-phosphosite-source-review",
                    str(source_review),
                    "--epk-source-free-protein-substrate-role-discriminator-audit",
                    str(protein_role),
                    "--epk-midlength-protein-role-counteraxis-audit",
                    str(midlength),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            metadata = payload["metadata"]
            self.assertEqual(metadata["method"], "epk_mek_erk_role_control_rerun")
            self.assertEqual(metadata["source_reviewed_broad_protein_role_hit_count"], 1)
            self.assertEqual(
                metadata["role_control_rerun_status"],
                "passes_review_only_with_source_reviewed_broad_rows_but_scoring_closed",
            )
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_mek_erk_broad_role_stress_audit_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            rerun = root / "role_rerun.json"
            terminal = root / "terminal.json"
            out = root / "broad_role_stress.json"
            rerun.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_mek_erk_role_control_rerun",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "source_reviewed_broad_protein_role_hit_pdb_ids": [
                                "9POS"
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )
            terminal.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_ligand_specific_active_query_extension_audit"
                            ),
                            "known_positive_repeat_hit_pdb_ids": ["1POS"],
                        },
                        "rows": [
                            {
                                "pdb_id": "9POS",
                                "topology_hit": True,
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
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-mek-erk-broad-role-stress-audit",
                    "--epk-mek-erk-role-control-rerun",
                    str(rerun),
                    "--epk-multi-query-active-site-terminal-audit",
                    str(terminal),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            metadata = payload["metadata"]
            self.assertEqual(metadata["method"], "epk_mek_erk_broad_role_stress_audit")
            self.assertEqual(
                metadata["broad_role_stress_status"],
                "fails_closed_naive_broad_role_rule_false_hits_terminal_surface",
            )
            self.assertEqual(
                metadata["nonpositive_naive_broad_role_false_hit_pdb_ids"],
                ["7BAD"],
            )
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_mek_erk_context_counteraxis_stress_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            broad = root / "broad_role_stress.json"
            out = root / "context_counteraxis.json"
            broad.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_mek_erk_broad_role_stress_audit",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
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
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-mek-erk-context-counteraxis-stress-audit",
                    "--epk-mek-erk-broad-role-stress-audit",
                    str(broad),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            metadata = payload["metadata"]
            self.assertEqual(
                metadata["method"], "epk_mek_erk_context_counteraxis_stress_audit"
            )
            self.assertEqual(
                metadata["context_counteraxis_status"],
                "passes_review_context_counteraxis_but_not_source_free",
            )
            self.assertEqual(
                metadata["prior_counterexample_context_blocked_pdb_ids"],
                ["7OLD"],
            )
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_mek_erk_residual_false_hit_source_adjudication_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            context = root / "context_counteraxis.json"
            review = root / "source_review.json"
            out = root / "residual_adjudication.json"
            context.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_mek_erk_context_counteraxis_stress_audit",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "residual_new_topology_false_hit_pdb_ids": ["8TRN"],
                        },
                        "rows": [
                            {
                                "pdb_id": "8TRN",
                                "context_counteraxis_decision": (
                                    "residual_new_topology_false_hit_review_only"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_heteromeric_candidate_source_validation_review"
                            )
                        },
                        "rows": [
                            {
                                "pdb_id": "8TRN",
                                "source_validation_status": (
                                    "blocked_source_context_insufficient_review_only"
                                ),
                                "source_validation_evidence": [
                                    "no_explicit_kinase_substrate_source_context_detected"
                                ],
                                "entity_descriptions": [
                                    "Energy-coupling factor transporter",
                                    "MAGNESIUM ION",
                                ],
                                "keywords": ["MEMBRANE PROTEIN"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-mek-erk-residual-false-hit-source-adjudication",
                    "--epk-mek-erk-context-counteraxis-stress-audit",
                    str(context),
                    "--epk-ligand-specific-active-query-source-validation-review",
                    str(review),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            metadata = payload["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_mek_erk_residual_false_hit_source_adjudication",
            )
            self.assertEqual(
                metadata["terminally_blocked_residual_false_hit_pdb_ids"],
                ["8TRN"],
            )
            self.assertEqual(metadata["unresolved_residual_false_hit_count"], 0)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_mek_erk_source_free_topology_ambiguity_counteraxis_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_review = root / "phosphosite_source_review.json"
            context = root / "context_counteraxis.json"
            candidate_artifact = root / "candidate_context.json"
            out = root / "topology_counteraxis.json"
            source_review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_mek_erk_phosphosite_source_review",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "source_authoritative_measurement_ready_pdb_ids": [
                                "9POS"
                            ],
                        },
                        "rows": [
                            {
                                "pdb_id": "9POS",
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
                ),
                encoding="utf-8",
            )
            context.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_mek_erk_context_counteraxis_stress_audit",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "residual_new_topology_false_hit_pdb_ids": ["7TRN"],
                        },
                        "rows": [],
                    }
                ),
                encoding="utf-8",
            )
            candidate_artifact.write_text(
                json.dumps(
                    {
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
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-mek-erk-source-free-topology-ambiguity-counteraxis",
                    "--epk-mek-erk-phosphosite-source-review",
                    str(source_review),
                    "--epk-mek-erk-context-counteraxis-stress-audit",
                    str(context),
                    "--candidate-context-artifact",
                    str(candidate_artifact),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            metadata = payload["metadata"]
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
            self.assertEqual(
                metadata["residual_false_hit_blocked_pdb_ids"], ["7TRN"]
            )
            self.assertTrue(metadata["source_free_predictive_feature_materialized"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_mek_erk_source_free_topology_broader_stress_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            broad = root / "broad_role.json"
            candidate_artifact = root / "candidate_context.json"
            out = root / "broader_stress.json"
            broad.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_mek_erk_broad_role_stress_audit",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "pdb_id": "9POS",
                                "naive_broad_protein_role_rule_hit": True,
                                "source_reviewed_mek_erk_positive": True,
                                "broad_role_stress_decision": (
                                    "source_reviewed_mek_erk_positive_retained_review_only"
                                ),
                                "candidate_chain_name": "B",
                                "gamma_associated_polymer_chain_name": "A",
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
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            candidate_artifact.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "candidate_context_fixture"},
                        "rows": [
                            {
                                "pdb_id": "7TRN",
                                "candidate_hits": [
                                    {
                                        "candidate_chain_name": "C",
                                        "gamma_associated_polymer_chain_name": "C",
                                        "nearest_gamma_distance_angstrom": 4.8,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-mek-erk-source-free-topology-broader-stress-audit",
                    "--epk-mek-erk-broad-role-stress-audit",
                    str(broad),
                    "--candidate-context-artifact",
                    str(candidate_artifact),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            metadata = payload["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_mek_erk_source_free_topology_broader_stress_audit",
            )
            self.assertEqual(
                metadata["broader_stress_status"],
                "passes_broader_topology_ambiguity_controls_review_only",
            )
            self.assertEqual(metadata["false_hit_blocked_pdb_ids"], ["7TRN"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_mek_erk_substrate_mode_counteraxis_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            stress = root / "topology_broader_stress.json"
            out = root / "substrate_mode_counteraxis.json"
            stress.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_mek_erk_source_free_topology_broader_stress_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
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
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-mek-erk-substrate-mode-counteraxis-audit",
                    "--epk-mek-erk-source-free-topology-broader-stress-audit",
                    str(stress),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            metadata = payload["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_mek_erk_substrate_mode_counteraxis_audit",
            )
            self.assertEqual(
                metadata["substrate_mode_counteraxis_status"],
                "passes_current_broad_stress_substrate_mode_controls_review_only",
            )
            self.assertEqual(metadata["positive_control_retained_count"], 2)
            self.assertEqual(metadata["false_hit_blocked_by_topology_pdb_ids"], ["7TOPO"])
            self.assertEqual(
                metadata["false_hit_blocked_by_substrate_mode_pdb_ids"], ["8BAD"]
            )
            self.assertEqual(metadata["residual_false_hit_count"], 0)
            self.assertTrue(metadata["source_free_predictive_feature_materialized"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_mek_erk_substrate_mode_fresh_stress_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            substrate = root / "substrate_mode_counteraxis.json"
            scout = root / "targeted_candidate_scout.json"
            validation = root / "targeted_source_validation.json"
            out = root / "fresh_stress.json"
            substrate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_mek_erk_substrate_mode_counteraxis_audit",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "candidate_threshold_angstrom": 6.0,
                            "max_n_terminal_acceptor_auth_seq_id": 25,
                        },
                        "rows": [
                            {
                                "pdb_id": "9REP",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            scout.write_text(
                json.dumps(
                    {
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
                ),
                encoding="utf-8",
            )
            validation.write_text(
                json.dumps(
                    {
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
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-mek-erk-substrate-mode-fresh-stress-audit",
                    "--epk-mek-erk-substrate-mode-counteraxis-audit",
                    str(substrate),
                    "--epk-mek-erk-targeted-candidate-scout",
                    str(scout),
                    "--epk-mek-erk-targeted-source-validation-review",
                    str(validation),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            metadata = payload["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_mek_erk_substrate_mode_fresh_stress_audit",
            )
            self.assertEqual(
                metadata["substrate_mode_fresh_stress_status"],
                (
                    "passes_fresh_nonrepeat_controls_with_topology_confounding_review_only"
                ),
            )
            self.assertEqual(metadata["fresh_nonrepeat_candidate_pdb_ids"], ["7NEW"])
            self.assertEqual(
                metadata["fresh_nonrepeat_rejected_by_substrate_mode_pdb_ids"],
                ["7NEW"],
            )
            self.assertEqual(metadata["fresh_nonrepeat_rule_hit_count"], 0)
            self.assertEqual(
                metadata["repeat_current_surface_rule_hit_pdb_ids"], ["9REP"]
            )
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_mek_erk_substrate_mode_existing_scout_gap_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            substrate = root / "substrate_mode_counteraxis.json"
            fresh = root / "fresh_stress.json"
            scout = root / "candidate_scout.json"
            out = root / "existing_gap.json"
            substrate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_mek_erk_substrate_mode_counteraxis_audit",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [{"pdb_id": "9OLD"}],
                    }
                ),
                encoding="utf-8",
            )
            fresh.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_mek_erk_substrate_mode_fresh_stress_audit"
                            )
                        },
                        "rows": [{"pdb_id": "7SEEN"}],
                    }
                ),
                encoding="utf-8",
            )
            scout.write_text(
                json.dumps(
                    {
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
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-mek-erk-substrate-mode-existing-scout-gap-audit",
                    "--epk-mek-erk-substrate-mode-counteraxis-audit",
                    str(substrate),
                    "--epk-mek-erk-substrate-mode-fresh-stress-audit",
                    str(fresh),
                    "--candidate-context-artifact",
                    str(scout),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            metadata = json.loads(out.read_text(encoding="utf-8"))["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_mek_erk_substrate_mode_existing_scout_gap_audit",
            )
            self.assertEqual(
                metadata["existing_scout_gap_status"],
                (
                    "blocked_existing_scouts_only_topology_confounded_candidates_review_only"
                ),
            )
            self.assertEqual(metadata["topology_confounded_candidate_pdb_ids"], ["7NEW"])
            self.assertEqual(metadata["non_topology_confounded_candidate_count"], 0)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_substrate_mode_next_tranche_source_review_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            substrate = root / "substrate_mode_counteraxis.json"
            scout = root / "next_scout.json"
            validation = root / "next_validation.json"
            uniprot_records = root / "uniprot_records.json"
            cif_dir = root / "cifs"
            cif_dir.mkdir()
            out = root / "next_source_review.json"
            substrate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_mek_erk_substrate_mode_counteraxis_audit",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "candidate_threshold_angstrom": 6.0,
                            "max_n_terminal_acceptor_auth_seq_id": 25,
                        }
                    }
                ),
                encoding="utf-8",
            )
            scout.write_text(
                json.dumps(
                    {
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
                ),
                encoding="utf-8",
            )
            validation.write_text(
                json.dumps(
                    {
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
                ),
                encoding="utf-8",
            )
            uniprot_records.write_text(
                json.dumps(
                    {
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
                ),
                encoding="utf-8",
            )
            (cif_dir / "4EKK.cif").write_text(
                """
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
""",
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-substrate-mode-next-tranche-source-review",
                    "--epk-mek-erk-substrate-mode-counteraxis-audit",
                    str(substrate),
                    "--epk-next-tranche-candidate-scout",
                    str(scout),
                    "--epk-next-tranche-source-validation-review",
                    str(validation),
                    "--uniprot-records-by-accession",
                    str(uniprot_records),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            metadata = json.loads(out.read_text(encoding="utf-8"))["metadata"]
            self.assertEqual(
                metadata["method"], "epk_substrate_mode_next_tranche_source_review"
            )
            self.assertEqual(metadata["source_mapped_measurement_ready_pdb_ids"], ["4EKK"])
            self.assertEqual(metadata["source_mapped_measurement_ready_count"], 1)
            self.assertTrue(metadata["source_context_used_as_review_evidence_only"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])

    def test_build_epk_substrate_mode_tranche_recovery_decision_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            ready_review = root / "ready_review.json"
            unresolved_review = root / "unresolved_review.json"
            out = root / "recovery_decision.json"
            ready_review.write_text(
                json.dumps(
                    {
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
                                "next_tranche_source_review_status": (
                                    "source_mapped_non_topology_substrate_mode_measurement_ready_review_only"
                                ),
                                "measurement_ready_for_review_controls": True,
                                "nearest_gamma_to_candidate_acceptor_distance_angstrom": 3.228,
                                "remaining_blockers": [
                                    "source_review_evidence_not_source_free_predictive_feature"
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            unresolved_review.write_text(
                json.dumps(
                    {
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
                                "next_tranche_source_review_status": (
                                    "non_topology_confounded_source_mapping_unresolved_review_only"
                                ),
                                "measurement_ready_for_review_controls": False,
                                "nearest_gamma_to_candidate_acceptor_distance_angstrom": 3.566,
                                "remaining_blockers": [
                                    "source_phosphosite_or_role_direction_not_mapped_to_candidate"
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-substrate-mode-tranche-recovery-decision",
                    "--epk-substrate-mode-next-tranche-source-review",
                    str(ready_review),
                    "--epk-substrate-mode-next-tranche-source-review",
                    str(unresolved_review),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            metadata = json.loads(out.read_text(encoding="utf-8"))["metadata"]
            self.assertEqual(
                metadata["method"], "epk_substrate_mode_tranche_recovery_decision"
            )
            self.assertEqual(metadata["measurement_ready_pdb_ids"], ["4EKK"])
            self.assertEqual(metadata["source_mapping_unresolved_pdb_ids"], ["1O6K"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])


if __name__ == "__main__":
    unittest.main()
