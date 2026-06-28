from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.predicted_geometry_atlas_engine_preregistration import (
    build_predicted_geometry_atlas_engine_preregistration,
    write_predicted_geometry_atlas_engine_preregistration,
)


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _minimal_surface(root: Path) -> dict[str, Path]:
    current702 = root / "current702.json"
    current702.write_text("[]\n", encoding="utf-8")
    cofactor = _write_json(
        root / "cofactor.json",
        {"artifact_id": "cofactor", "status": "complete", "schema_version": "x"},
    )
    recovery = _write_json(
        root / "recovery.json",
        {
            "artifact_id": "recovery",
            "status": "complete",
            "readouts_by_split": {
                "calibration": {
                    "experimental_correct": 34,
                    "apo_correct": 17,
                    "fused_correct": 30,
                    "apo_lost_primary_rows": 17,
                    "fused_recovered_rows": 12,
                    "recovery_fraction_of_apo_loss": 0.7059,
                    "fused_regressed_rows": 0,
                }
            },
        },
    )
    precision = _write_json(
        root / "precision.json",
        {
            "artifact_id": "precision",
            "status": "complete",
            "dial_comparison": {
                "surface": "calibration_out_of_sample",
                "fused_frozen": {
                    "inscope_correct": 30,
                    "inscope_total": 35,
                    "oos_false_positives": 9,
                    "oos_total": 26,
                },
                "suppression_dial": {
                    "inscope_correct": 23,
                    "inscope_total": 35,
                    "oos_false_positives": 8,
                    "oos_total": 26,
                },
                "threshold_dial_matching_suppression_precision": {
                    "threshold": 0.44,
                    "inscope_correct": 30,
                    "oos_false_positives": 8,
                },
                "threshold_dial_dominates_suppression_dial": True,
            },
        },
    )
    fold_channel = _write_json(
        root / "fold_channel.json",
        {
            "artifact_id": "fold",
            "status": "computed_all_heldout_foldseek_scores",
        },
    )
    contract_audit = _write_json(
        root / "contract_audit.json",
        {"artifact_id": "audit", "status": "fold_channel_contract_passed_current702"},
    )
    provenance = _write_json(
        root / "provenance.json",
        {"artifact_id": "provenance", "status": "fold_channel_coordinate_provenance_passed"},
    )
    threshold_contract = _write_json(
        root / "threshold.json",
        {
            "artifact_id": "threshold",
            "status": "computed_oos_calibrated_threshold_contract",
            "primary_channel_readout": {
                "selected_at_90pct_calibration_in_scope_retention": {
                    "threshold": 0.44155
                }
            },
        },
    )
    closure = _write_json(
        root / "closure.json",
        {
            "artifact_id": "closure",
            "status": "fold_augmented_post_rerun_deployment_closure_status_blocked",
            "fixed_threshold": 0.44155,
            "remaining_blockers": [
                {"entry_id": "m_csa:204", "blocker": "fold_only_policy_caveat"}
            ],
            "decision": {"deployment_closed_now": False},
        },
    )
    confounded = _write_json(
        root / "confounded.json",
        {
            "artifact_id": "confounded",
            "status": "post_rerun_confounded_fold_channel_research_ready_p10746_caveat",
            "operating_point": {
                "channel": "combined_mean_geometry_fold",
                "fixed_threshold": 0.44155,
                "calibration_oos_abstain_recall": 0.4,
                "calibration_oos_abstained": 30,
                "calibration_oos_total": 75,
                "heldout_confounded_oos_abstain_recall": 0.8333,
                "heldout_confounded_oos_abstained": 5,
                "heldout_confounded_oos_total": 6,
            },
        },
    )
    split = _write_json(root / "split.json", {"artifact_id": "split", "status": "complete"})
    coord = root / "coords"
    for subdir in ("atlas_in_distribution", "confounded_proxy_train_cal_tranche_queries"):
        (coord / subdir).mkdir(parents=True)
        (coord / subdir / "afdb_P0_v6.cif").write_text("data\n", encoding="utf-8")
    return {
        "current702_path": current702,
        "cofactor_channel_path": cofactor,
        "recovery_path": recovery,
        "cofactor_precision_path": precision,
        "fold_channel_path": fold_channel,
        "fold_contract_audit_path": contract_audit,
        "fold_coordinate_provenance_path": provenance,
        "fold_threshold_contract_path": threshold_contract,
        "fold_post_rerun_closure_path": closure,
        "fold_confounded_closure_path": confounded,
        "split_manifest_path": split,
        "coordinate_root": coord,
    }


class AtlasEnginePreregistrationTests(unittest.TestCase):
    def test_preregisters_cached_surface_when_foldseek_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = _minimal_surface(Path(tmp))
            audit = build_predicted_geometry_atlas_engine_preregistration(
                **paths,
                module_status={
                    "numpy": True,
                    "torch": True,
                    "sklearn": True,
                    "pandas": True,
                    "esm": False,
                    "Bio": False,
                    "biotite": False,
                },
                executable_status={
                    "mmseqs": {"available": True, "path": "/bin/mmseqs", "version": "x"},
                    "foldseek": {"available": False, "path": None, "version": None},
                    "diamond": {"available": True, "path": "/bin/diamond", "version": "x"},
                },
            )
        self.assertEqual(
            audit["status"],
            "preregistered_cached_surface_ready_new_foldseek_backend_blocked",
        )
        self.assertFalse(audit["guardrails"]["heldout_rows_scored_now"])
        self.assertFalse(audit["guardrails"]["new_fingerprint_family_growth"])
        self.assertTrue(
            audit["runtime_capability"]["existing_scored_fold_tm_surfaces_reusable"]
        )
        self.assertFalse(audit["runtime_capability"]["full_new_fold_tm_scoring_runnable"])
        self.assertTrue(
            audit["decision"]["can_run_cached_surface_atlas_engine_readout_now"]
        )
        thresholds = audit["preregistered_experiment"]["thresholds_and_selection_rule"]
        self.assertEqual(thresholds["cofactor_fused_router_threshold"], 0.44)
        self.assertEqual(thresholds["fold_tm_combined_mean_geometry_fold_threshold"], 0.44155)
        self.assertIn(
            "foldseek_missing_for_new_fold_tm_scoring",
            audit["runtime_capability"]["blockers"],
        )

    def test_current_router_drift_blocks_cached_surface_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = _minimal_surface(root)
            drift_path = _write_json(
                root / "current57.json",
                {
                    "artifact_id": "current57",
                    "status": "current57_registry_rerun_complete_precision_regression_diagnostic",
                    "rerun_context": {
                        "previous_calibration_fused_frozen": {
                            "inscope_correct": 30,
                            "oos_false_positives": 9,
                        },
                        "current57_calibration_fused_frozen": {
                            "inscope_correct": 13,
                            "oos_false_positives": 26,
                        },
                        "interpretation": "drift",
                    },
                },
            )
            contract_path = _write_json(
                root / "current57_contract.json",
                {
                    "artifact_id": "contract",
                    "status": "blocked_current57_cofactor_precision_contract_not_deployable",
                    "selection_rule": {
                        "decision": "fail_closed_keep_atlas_engine_blocked_on_current57_cofactor_surface"
                    },
                    "calibration_summary": {
                        "exact_fused_current57_at_frozen_threshold": {
                            "inscope_correct": 13,
                            "oos_false_positives": 26,
                        },
                        "legacy_v1_compatible_fused_current57_at_frozen_threshold": {
                            "inscope_correct": 26,
                            "oos_false_positives": 26,
                        },
                        "best_point_under_trusted_oos_fp": {
                            "threshold": 0.733,
                            "inscope_correct": 20,
                            "oos_false_positives": 8,
                        },
                        "taxonomy_version_recovered_count": 13,
                        "remaining_recovery_gap_vs_trusted": 4,
                    },
                },
            )
            alignment_path = _write_json(
                root / "alignment.json",
                {
                    "artifact_id": "alignment",
                    "status": (
                        "blocked_cached_fold_surface_not_row_aligned_with_"
                        "current57_cofactor_surface"
                    ),
                    "alignment_gate": {
                        "passed": False,
                        "decision": (
                            "fail_closed_cached_fold_rows_do_not_cover_current57_"
                            "cofactor_surface"
                        ),
                    },
                    "calibration_overlap": {
                        "inscope": {
                            "current57_rows": 35,
                            "overlap_rows": 4,
                            "overlap_fraction": 0.1143,
                        },
                        "oos": {
                            "current57_rows": 26,
                            "overlap_rows": 0,
                            "overlap_fraction": 0.0,
                        },
                    },
                    "overlap_only_fixed_gate_probe": {"interpretable": False},
                },
            )
            audit = build_predicted_geometry_atlas_engine_preregistration(
                **paths,
                current_router_cofactor_rerun_path=drift_path,
                current57_cofactor_precision_contract_path=contract_path,
                current57_cofactor_fold_alignment_audit_path=alignment_path,
                module_status={
                    "numpy": True,
                    "torch": True,
                    "sklearn": True,
                    "pandas": True,
                    "esm": False,
                    "Bio": False,
                    "biotite": False,
                },
                executable_status={
                    "mmseqs": {"available": True},
                    "foldseek": {"available": False},
                    "diamond": {"available": True},
                },
            )
        drift = audit["preexisting_train_cal_context"]["current_router_cofactor_rerun"]
        contract = audit["preexisting_train_cal_context"][
            "current57_cofactor_precision_contract"
        ]
        alignment = audit["preexisting_train_cal_context"][
            "current57_cofactor_fold_alignment"
        ]
        self.assertTrue(drift["current_router_drift_detected"])
        self.assertTrue(contract["blocks_atlas_engine_fusion"])
        self.assertTrue(alignment["blocks_cached_atlas_engine_fusion"])
        self.assertIn("precision_contract", audit["status"])
        self.assertIn("fold_alignment", audit["status"])
        self.assertFalse(
            audit["decision"]["can_run_cached_surface_atlas_engine_readout_now"]
        )
        self.assertIn(
            "not row-aligned",
            audit["decision"]["next_action"],
        )

    def test_missing_source_artifact_blocks_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = _minimal_surface(Path(tmp))
            paths["cofactor_precision_path"].unlink()
            audit = build_predicted_geometry_atlas_engine_preregistration(
                **paths,
                module_status={"numpy": True, "sklearn": True, "torch": True},
                executable_status={
                    "mmseqs": {"available": True},
                    "foldseek": {"available": True},
                    "diamond": {"available": True},
                },
            )
        self.assertEqual(audit["status"], "blocked_missing_preregistration_source_artifacts")
        self.assertFalse(
            audit["decision"]["can_run_cached_surface_atlas_engine_readout_now"]
        )

    def test_writer_emits_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = _minimal_surface(root)
            out = root / "out.json"
            report = root / "report.md"
            audit = write_predicted_geometry_atlas_engine_preregistration(
                **paths,
                out_path=out,
                report_path=report,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(json.loads(out.read_text())["artifact_id"], audit["artifact_id"])
            self.assertIn("No heldout rows", report.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
