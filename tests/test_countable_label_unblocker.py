from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from catalytic_earth.countable_label_unblocker import (
    build_countable_label_unblocker_matrix,
    render_countable_label_unblocker_report,
    write_countable_label_unblocker_matrix,
)


class CountableLabelUnblockerTests(unittest.TestCase):
    def test_current702_matrix_reconciles_and_has_no_import_preview(self) -> None:
        matrix = build_countable_label_unblocker_matrix(
            created_utc="2026-06-08T00:00:00Z"
        )

        self.assertTrue(matrix["validation_checks"]["passed"])
        self.assertEqual(matrix["counts"]["target_canonical_records"], 523)
        self.assertEqual(
            matrix["counts"]["input_terminal_state_counts"],
            {
                "blocked_coordinate": 24,
                "blocked_family_decision": 134,
                "blocked_locator": 85,
                "review_only_evidence": 280,
            },
        )
        self.assertEqual(matrix["counts"]["import_preview_candidate_rows"], 0)
        self.assertEqual(matrix["counts"]["rows_with_ready_for_label_import_true"], 0)
        self.assertEqual(
            matrix["counts"]["rows_with_countable_label_candidate_true"], 0
        )
        self.assertTrue(
            matrix["validation_checks"][
                "all_rows_have_terminal_state_evidence_blockers_hashes_next_action"
            ]
        )

    def test_known_rows_route_to_concrete_blockers(self) -> None:
        matrix = build_countable_label_unblocker_matrix(
            created_utc="2026-06-08T00:00:00Z"
        )
        rows = {row["canonical_key"]: row for row in matrix["rows"]}

        self.assertEqual(
            rows["uniprot:p12995"]["unblock_classification"],
            "hard_blocked_with_next_action",
        )
        self.assertIn(
            "current_registry_overlap_blocks_import_preview",
            rows["uniprot:p12995"]["blocker_basis"],
        )
        self.assertEqual(
            rows["uniprot:o50131"]["unblock_classification"],
            "reject/OOS_preserve_signal",
        )
        self.assertTrue(
            any(
                blocker.startswith("positive_duplicate_screen:")
                for blocker in rows["uniprot:o50131"]["blocker_basis"]
            )
        )
        self.assertEqual(
            rows["m_csa:1005"]["unblock_classification"],
            "locator_repair_candidate",
        )
        self.assertEqual(
            rows["m_csa:567"]["unblock_classification"],
            "locator_repair_candidate",
        )
        self.assertTrue(rows["m_csa:567"]["evidence_basis"]["local_coordinate_matches"])
        self.assertEqual(
            rows["secondary_probe::cobalamin_radical_rearrangement"][
                "unblock_classification"
            ],
            "coordinate_repair_candidate",
        )

    def test_write_outputs_matrix_report_and_no_empty_preview(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            out = root / "matrix.json"
            report = root / "matrix.md"
            preview = root / "preview.json"

            matrix = write_countable_label_unblocker_matrix(
                out_path=out,
                report_path=report,
                import_preview_path=preview,
                created_utc="2026-06-08T00:00:00Z",
            )

            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertFalse(preview.exists())
            self.assertEqual(matrix["counts"]["import_preview_candidate_rows"], 0)
            rendered = render_countable_label_unblocker_report(matrix)
            self.assertIn("Import-preview candidates: `0`", rendered)
            self.assertIn("Validation passed: `True`", rendered)

