from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.targeted_expansion_acquisition_conversion import (
    build_targeted_expansion_acquisition_conversion_screens,
    render_acquisition_conversion_report,
    write_targeted_expansion_acquisition_conversion_screens,
)


ROOT = Path(__file__).resolve().parents[1]


def _source_records(*names: str) -> dict[str, dict[str, object]]:
    return {
        name: {
            "path": f"artifacts/{name}.json",
            "sha256": f"{index + 1:064x}",
            "bytes": 10,
        }
        for index, name in enumerate(names)
    }


def _batch_row(
    accession: str,
    *,
    active_site_status: str = "explicit_active_site_and_catalytic_activity_source_present",
    family_axis: str = "near_orphan_or_unrepresented_mechanism_tail",
    required_screens: list[str] | None = None,
    source_blockers: list[str] | None = None,
) -> dict[str, object]:
    return {
        "candidate_id": f"uniprot:{accession}",
        "accession_or_source_id": accession,
        "display_name": f"{accession} candidate",
        "family_axis": family_axis,
        "admission_state": "acquisition_needed",
        "active_site_or_locator_evidence": {
            "active_site_evidence_status": active_site_status,
            "active_site_feature_count": 1
            if active_site_status.startswith("explicit_active_site")
            else None,
            "binding_site_feature_count": 0,
        },
        "predicted_coordinate_or_provenance_availability": {
            "coordinate_provenance_available": True,
            "pdb_ids": ["1ABC"],
            "alphafold_ids": [accession],
        },
        "geometry_or_reconstruction_status": {
            "reconstruction_status": "sourced_pending_sequence_structure_distance_screens"
        },
        "mechanical_unblock_requirements": {
            "next_required_screens": required_screens or [],
            "source_evidence_blockers": source_blockers or [],
        },
        "source_hashes": {"external_hard_negative_next_sourcing": "a" * 64},
        "row_context_sha256": accession.lower().ljust(64, "0")[:64],
    }


class TargetedExpansionAcquisitionConversionTests(unittest.TestCase):
    def test_routes_acquisition_rows_to_terminal_states(self) -> None:
        batch = {
            "candidate_rows": [
                _batch_row("QEXACT", required_screens=["current_reference_backend_sequence_search"]),
                _batch_row("PSTRUCT"),
                _batch_row("PREADY"),
                _batch_row("PLOC", active_site_status="not_sampled_metadata_blocked"),
                _batch_row(
                    "PFAM",
                    source_blockers=[
                        "mechanism_lane_not_covered_by_existing_counterevidence_rules"
                    ],
                ),
            ]
        }
        screen_payloads = {
            "sequence_cluster_proxy_1025": {
                "rows": [
                    {
                        "entry_id": "m_csa:1",
                        "reference_uniprot_ids": ["QEXACT"],
                        "sequence_cluster_id": "uniprot:QEXACT",
                    }
                ]
            },
            "external_hard_negative_new_current_countable_structural_screen": {
                "rows": [
                    {
                        "entry_id": "uniprot:PSTRUCT",
                        "accession": "PSTRUCT",
                        "current_countable_structural_screen_status": (
                            "current_countable_structural_duplicate_signal"
                        ),
                        "current_countable_high_tm_hit_count": 2,
                        "nearest_current_countable_hit": {
                            "example_current_entry_id": "m_csa:20",
                            "max_pair_tm_score": 0.91,
                        },
                    }
                ]
            },
            "external_hard_negative_next_factory_import_gate": {
                "rows": [
                    {
                        "entry_id": "uniprot:PREADY",
                        "accession": "PREADY",
                        "countable_label_candidate": True,
                        "import_ready_candidate": True,
                        "ready_for_label_import": True,
                        "factory_gate_status": "passed",
                    }
                ]
            },
        }
        source_records = _source_records(*screen_payloads)

        artifact = build_targeted_expansion_acquisition_conversion_screens(
            batch_payload=batch,
            batch_source_record={
                "path": "artifacts/batch.json",
                "sha256": "b" * 64,
                "bytes": 100,
            },
            screen_payloads=screen_payloads,
            screen_source_records=source_records,
            created_utc="2026-06-08T00:00:00Z",
        )

        self.assertTrue(artifact["validation_checks"]["passed"])
        self.assertTrue(
            artifact["validation_checks"]["all_rows_have_required_screen_axes"]
        )
        self.assertTrue(
            artifact["validation_checks"]["all_rows_have_conversion_context_hashes"]
        )
        self.assertIn(
            "locator_coordinate_readiness",
            artifact["routing_policy"]["required_screen_axes"],
        )
        rows = {row["accession"]: row for row in artifact["rows"]}
        self.assertEqual(
            rows["QEXACT"]["terminal_state"],
            "reject/OOS_preserve_signal",
        )
        self.assertEqual(
            rows["QEXACT"]["terminal_route_basis"],
            "current_reference_sequence_duplicate_or_holdout",
        )
        self.assertEqual(
            rows["PSTRUCT"]["terminal_route_basis"],
            "current_countable_structural_duplicate",
        )
        self.assertEqual(
            rows["PREADY"]["terminal_state"],
            "countable_candidate_preflight_only",
        )
        self.assertEqual(rows["PLOC"]["terminal_state"], "blocked_locator")
        self.assertEqual(rows["PFAM"]["terminal_state"], "blocked_family_decision")
        self.assertNotIn("acquisition_needed", rows["PREADY"]["terminal_state"])
        self.assertTrue(
            all(row["terminal_state"] != "acquisition_needed" for row in rows.values())
        )
        self.assertFalse(rows["PREADY"]["guardrails"]["import_or_promotion_performed"])
        report = render_acquisition_conversion_report(artifact)
        self.assertIn("Countable Preflight Only", report)
        self.assertIn("Locator Blocker Queue", report)
        self.assertIn("Family Decision Blocker Queue", report)
        self.assertIn(
            "source_free_locator_ready_explicit_active_site_source\\|"
            "coordinate_provenance_ready_materialization_pending",
            report,
        )
        self.assertIn("`uniprot:PREADY`", report)

    def test_write_materializes_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            batch_path = root / "batch.json"
            screen_path = root / "screen.json"
            out_path = root / "out.json"
            report_path = root / "report.md"
            batch_path.write_text(
                json.dumps({"candidate_rows": [_batch_row("QEXACT")]}),
                encoding="utf-8",
            )
            screen_path.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "reference_uniprot_ids": ["QEXACT"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            artifact = write_targeted_expansion_acquisition_conversion_screens(
                batch_path=batch_path,
                out_path=out_path,
                report_path=report_path,
                screen_paths={"sequence_cluster_proxy_1025": screen_path},
                created_utc="2026-06-08T00:00:01Z",
            )

            self.assertEqual(artifact["candidate_count"], 1)
            self.assertTrue(out_path.exists())
            self.assertIn(
                "Targeted Expansion Acquisition Conversion Screens",
                report_path.read_text(encoding="utf-8"),
            )

    def test_current702_conversion_artifact_regression(self) -> None:
        artifact_path = (
            ROOT
            / "artifacts"
            / "v3_targeted_expansion_acquisition_conversion_screens_current702_20260608.json"
        )
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))

        self.assertTrue(artifact["validation_checks"]["passed"])
        self.assertTrue(
            artifact["validation_checks"]["all_rows_have_required_screen_axes"]
        )
        self.assertTrue(
            artifact["validation_checks"]["all_rows_have_input_source_hashes"]
        )
        self.assertEqual(artifact["candidate_count"], 86)
        self.assertEqual(artifact["priority_screen_ready_count"], 16)
        self.assertEqual(
            artifact["terminal_state_counts"],
            {
                "blocked_coordinate": 0,
                "blocked_family_decision": 50,
                "blocked_locator": 7,
                "countable_candidate_preflight_only": 1,
                "reject/OOS_preserve_signal": 27,
                "review_only_evidence": 1,
            },
        )
        rows = {row["candidate_id"]: row for row in artifact["rows"]}
        self.assertEqual(
            rows["uniprot:P78549"]["terminal_state"],
            "countable_candidate_preflight_only",
        )
        self.assertFalse(
            rows["uniprot:P78549"]["guardrails"]["import_or_promotion_performed"]
        )
        self.assertEqual(
            rows["uniprot:P22830"]["screens"][
                "current_reference_sequence_duplicate_screen"
            ]["matched_current_entry_ids"],
            ["m_csa:578"],
        )
        self.assertEqual(
            rows["uniprot:O60568"]["terminal_state"],
            "blocked_locator",
        )
