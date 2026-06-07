from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.cli import build_parser
from catalytic_earth.family_label_admission import (
    ADMISSION_STATES,
    build_family_label_admission_pipeline,
)


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    return path


class FamilyLabelAdmissionTests(unittest.TestCase):
    def _fixture_paths(
        self,
        root: Path,
        *,
        row_ids: list[str],
        row_gate_status: list[dict] | None = None,
        row_blockers: list[dict] | None = None,
        expert_stubs: list[dict] | None = None,
        accepted_rows: list[dict] | None = None,
        gate_input_rows: list[dict] | None = None,
        research_extra: dict | None = None,
    ) -> dict[str, Path]:
        panel = "test_family_axis"
        packet = _write_json(
            root / "panel_packet.json",
            {
                "panel": {"candidate_family": panel},
                "row_evidence": [
                    {
                        "entry_id": entry_id,
                        "selected_organic_cofactor_max": 0.5,
                        "predicted_geometry_status": "score_available",
                        "predicted_atlas_geometry_variant_scores": {"v": 0.5},
                        "electron_flow": "available_review_only",
                    }
                    for entry_id in row_ids
                ],
            },
        )
        research_rows = []
        for entry_id in row_ids:
            row = {
                "entry_id": entry_id,
                "panel_id": panel,
                "research_gate_status": "non_abstained_at_research_threshold",
                "primary_threshold": 0.44155,
                "primary_threshold_margin": 0.1,
                "channel_scores": {"fold_nearest_atlas_tm_score": 0.7},
            }
            if research_extra:
                row.update(research_extra)
            research_rows.append(row)
        paths = {
            "targets": _write_json(
                root / "targets.json",
                {
                    "status": "proposal_only_no_imports",
                    "candidate_families": [
                        {
                            "candidate_family": panel,
                            "candidate_rows": row_ids,
                            "candidate_sources": ["source review"],
                            "priority_bins": ["dark_bin"],
                            "expected_eval_bin_impact": "review signal",
                            "required_human_validation": "expert decision",
                        }
                    ],
                },
            ),
            "research": _write_json(
                root / "research.json",
                {
                    "panel_summaries": [{"panel_id": panel, "artifact": str(packet)}],
                    "row_scores": research_rows,
                },
            ),
            "countability": _write_json(
                root / "countability.json",
                {"row_gate_status": row_gate_status or []},
            ),
            "blockers": _write_json(
                root / "blockers.json", {"row_blockers": row_blockers or []}
            ),
            "expert": _write_json(
                root / "expert.json",
                {"expert_import_decision_stubs": expert_stubs or []},
            ),
            "preview": _write_json(
                root / "preview.json",
                {"accepted_import_preview_rows": accepted_rows or []},
            ),
            "readiness": _write_json(
                root / "readiness.json",
                {"label_factory_gate_input_rows": gate_input_rows or []},
            ),
        }
        return paths

    def _build(self, paths: dict[str, Path]) -> dict:
        return build_family_label_admission_pipeline(
            family_expansion_targets_path=paths["targets"],
            family_panel_research_readout_path=paths["research"],
            countability_gate_preflight_path=paths["countability"],
            import_preview_blocker_gate_path=paths["blockers"],
            expert_import_decision_packet_path=paths["expert"],
            accepted_import_preview_path=paths["preview"],
            label_factory_gate_readiness_path=paths["readiness"],
            created_utc="2026-06-07T00:00:00Z",
        )

    def test_row_state_classifier_emits_exactly_one_allowed_state_per_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            panel = "test_family_axis"
            rows = ["countable", "review", "oos", "locator", "coordinate", "family", "reject"]
            paths = self._fixture_paths(
                root,
                row_ids=rows,
                row_gate_status=[
                    {
                        "entry_id": "countable",
                        "panel_id": panel,
                        "countable_label_candidate": True,
                    },
                    {
                        "entry_id": "review",
                        "panel_id": panel,
                        "source_check_completion_status": "completed_review_only_no_label_change",
                    },
                    {
                        "entry_id": "locator",
                        "panel_id": panel,
                        "gate_blockers": [
                            "source_free_locator_human_or_policy_decision_required"
                        ],
                    },
                    {
                        "entry_id": "coordinate",
                        "panel_id": panel,
                        "gate_blockers": ["primary_channel_score_missing"],
                    },
                    {"entry_id": "family", "panel_id": panel},
                    {"entry_id": "reject", "panel_id": panel},
                ],
                row_blockers=[
                    {
                        "entry_id": "review",
                        "panel_id": panel,
                        "primary_blocker_class": "completed_source_check_review_only_no_promotion",
                    },
                    {
                        "entry_id": "oos",
                        "panel_id": panel,
                        "primary_blocker_class": "accepted_oos_hard_negative",
                    },
                    {
                        "entry_id": "locator",
                        "panel_id": panel,
                        "primary_blocker_class": "source_free_locator_or_primary_channel_missing",
                        "locator_decision_class": "nonlabel_locator_strategy_or_alternate_source_required",
                    },
                    {
                        "entry_id": "coordinate",
                        "panel_id": panel,
                        "primary_blocker_class": "source_free_locator_or_primary_channel_missing",
                        "locator_decision_class": "alternate_coordinate_fetch_approval_required",
                    },
                    {
                        "entry_id": "family",
                        "panel_id": panel,
                        "primary_blocker_class": "expert_family_admission_decision_required",
                    },
                ],
                expert_stubs=[
                    {
                        "entry_id": "reject",
                        "panel_id": panel,
                        "decision": "reject_family_panel_import_candidate",
                        "decision_context_sha256": "a" * 64,
                    }
                ],
                gate_input_rows=[{"entry_id": "countable", "panel_id": panel}],
            )

            audit = self._build(paths)

        states = {row["entry_id"]: row["state"] for row in audit["row_admission_table"]}
        self.assertEqual(
            states,
            {
                "countable": "countable_candidate",
                "review": "review_only_evidence",
                "oos": "oos_hard_negative",
                "locator": "blocked_locator",
                "coordinate": "blocked_coordinate",
                "family": "blocked_family_decision",
                "reject": "reject_preserve_signal",
            },
        )
        self.assertEqual(len(states), len(audit["row_admission_table"]))
        self.assertTrue(set(states.values()).issubset(set(ADMISSION_STATES)))

    def test_source_hashes_and_expert_provenance_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = self._fixture_paths(
                root,
                row_ids=["row1"],
                row_blockers=[
                    {
                        "entry_id": "row1",
                        "panel_id": "test_family_axis",
                        "primary_blocker_class": "expert_family_admission_decision_required",
                    }
                ],
                expert_stubs=[
                    {
                        "entry_id": "row1",
                        "panel_id": "test_family_axis",
                        "decision_context_sha256": "b" * 64,
                        "allowed_decisions": ["explicit_accept_family_panel_import_candidate"],
                    }
                ],
            )

            audit = self._build(paths)

        row = audit["row_admission_table"][0]
        self.assertEqual(
            row["evidence_preserved"]["human_expert_decision_provenance"][
                "decision_context_sha256"
            ],
            "b" * 64,
        )
        self.assertEqual(len(row["source_hashes"]["family_onboarding_manifest"]), 64)
        self.assertIn(
            "panel_packet::panel_packet",
            audit["machinery_applied"]["source_artifacts"],
        )

    def test_guardrails_exclude_source_fields_from_state_classification(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            blockers = [
                {
                    "entry_id": "row1",
                    "panel_id": "test_family_axis",
                    "primary_blocker_class": "expert_family_admission_decision_required",
                }
            ]
            paths_a = self._fixture_paths(
                root / "a",
                row_ids=["row1"],
                row_blockers=blockers,
                research_extra={"accession": "A0A", "mechanism_text": "do not use"},
            )
            paths_b = self._fixture_paths(
                root / "b",
                row_ids=["row1"],
                row_blockers=blockers,
                research_extra={
                    "accession": "DIFFERENT",
                    "mechanism_text": "changed text",
                    "coordinate_path": "/tmp/changed.cif",
                    "source_id": "changed",
                },
            )

            audit_a = self._build(paths_a)
            audit_b = self._build(paths_b)

        self.assertEqual(
            audit_a["row_admission_table"][0]["state"],
            audit_b["row_admission_table"][0]["state"],
        )
        self.assertFalse(
            audit_a["guardrails"]["source_text_or_label_fields_used_as_predictive_features"]
        )
        self.assertTrue(
            audit_a["guardrails"]["classification_uses_only_gate_and_review_outputs"]
        )

    def test_missing_required_input_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = self._fixture_paths(root, row_ids=["row1"])
            paths["research"] = root / "missing.json"

            with self.assertRaises(FileNotFoundError):
                self._build(paths)

    def test_missing_row_machinery_preserves_signal_without_countability(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = self._fixture_paths(root, row_ids=["row1"])

            audit = self._build(paths)

        row = audit["row_admission_table"][0]
        self.assertEqual(row["state"], "reject_preserve_signal")
        self.assertIn("missing_or_unrecognized_admission_inputs", row["state_blockers"])
        self.assertEqual(audit["counts"]["countable_candidate_rows"], 0)

    def test_cli_parser_registers_family_label_admission_command(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["build-family-label-admission-pipeline"])
        self.assertEqual(args.func.__name__, "cmd_build_family_label_admission_pipeline")


if __name__ == "__main__":
    unittest.main()
