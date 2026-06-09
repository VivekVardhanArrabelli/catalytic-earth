from __future__ import annotations

import unittest

from catalytic_earth.external_admission_qa_merger import (
    build_external_admission_import_ready_preview,
    build_external_admission_merged_surface,
    build_external_admission_repair_queue,
)


def _bulk_row(accession: str, *, terminal_state: str) -> dict[str, object]:
    return {
        "stable_candidate_key": f"external_source_ingestion:uniprot:{accession}",
        "candidate_id": f"uniprot:{accession}",
        "accession": accession,
        "target_family_lane": "redox oxygen/sulfur",
        "lane_id": "redox_oxygen_sulfur",
        "terminal_state": terminal_state,
        "duplicate_status_summary": {
            "blocked_by_duplicate_or_current_registry_conflict": False,
            "current702_status": "no_exact_current702_accession_or_sequence_sha_overlap",
            "external_pilot_status": "no_exact_external_pilot_accession_or_sequence_sha_overlap",
        },
        "source_hashes": {
            "uniprot_search_row_sha256": "a" * 64,
            "uniprot_entry_record_sha256": "b" * 64,
            "rhea_records_sha256": "c" * 64,
        },
        "source_provenance": {"query_timestamp_utc": "2026-06-09T00:00:00Z"},
        "exact_next_action": "continue gate",
    }


def _materialized_row(
    accession: str,
    *,
    terminal_state: str,
    queue_name: str,
) -> dict[str, object]:
    return {
        "stable_candidate_key": f"external_source_ingestion:uniprot:{accession}",
        "candidate_id": f"uniprot:{accession}",
        "accession": accession,
        "target_family_lane": "redox oxygen/sulfur",
        "terminal_state": terminal_state,
        "queue_name": queue_name,
        "source_hashes": {
            "uniprot_search_row_sha256": "a" * 64,
            "uniprot_entry_record_sha256": "b" * 64,
            "rhea_records_sha256": "c" * 64,
        },
        "source_provenance": {"query_timestamp_utc": "2026-06-09T00:00:00Z"},
        "duplicate_status": {
            "current_registry_conflict_status": "no_exact_current702_accession_or_sequence_sha_overlap",
            "duplicate_or_current_registry_conflict": False,
        },
        "next_action": "preview only",
        "input_preview_terminal_state": (
            "admission_ready_pending_locator_materialization"
            if queue_name == "validated_ready_preview"
            else "provisional_external_countable_preflight_candidate"
        ),
    }


class ExternalAdmissionQaMergerTests(unittest.TestCase):
    def test_merges_materialized_rows_over_bulk_scaleout_surface(self) -> None:
        materialization = {
            "counts": {"input_rows": 2},
            "rows": [
                _materialized_row(
                    "PVALID",
                    terminal_state="import_ready_preview",
                    queue_name="validated_ready_preview",
                ),
                _materialized_row(
                    "PREPAIR",
                    terminal_state="repairable_locator_blocker",
                    queue_name="provisional_bulk_preview",
                ),
            ],
        }
        materialization_preview = {
            "candidate_count": 1,
            "rows": [{"candidate_id": "uniprot:PVALID"}],
        }
        bulk = {
            "candidate_count": 3,
            "rows": [
                _bulk_row(
                    "PVALID",
                    terminal_state="blocked_duplicate_or_current_registry_conflict",
                ),
                _bulk_row(
                    "PREPAIR",
                    terminal_state="provisional_external_countable_preflight_candidate",
                ),
                _bulk_row("PBULK", terminal_state="locator_ready_candidate"),
            ],
        }
        bulk_preview = {
            "candidate_count": 1,
            "rows": [{"candidate_id": "uniprot:PREPAIR"}],
        }
        previous_merged = {
            "rows": [
                {"candidate_id": "uniprot:PVALID"},
                {"candidate_id": "uniprot:PREPAIR"},
            ]
        }

        merged = build_external_admission_merged_surface(
            materialization_payload=materialization,
            materialization_preview_payload=materialization_preview,
            bulk_scaleout_payload=bulk,
            bulk_preview_payload=bulk_preview,
            previous_merged_surface_payload=previous_merged,
            created_utc="2026-06-09T02:25:12Z",
        )

        self.assertTrue(merged["validation_checks"]["passed"])
        self.assertEqual(merged["counts"]["merged_rows"], 3)
        self.assertEqual(merged["counts"]["import_ready_rows"], 1)
        self.assertEqual(merged["counts"]["repair_queue_rows"], 1)
        self.assertEqual(merged["counts"]["rows_newly_added_by_scaleout"], 1)
        self.assertEqual(merged["counts"]["materialized_from_validated_queue_rows"], 1)
        self.assertEqual(
            merged["counts"]["materialized_from_provisional_queue_rows"], 1
        )

        rows = {row["candidate_id"]: row for row in merged["rows"]}
        self.assertEqual(
            rows["uniprot:PVALID"]["merge_status"],
            "materialized_from_validated_queue",
        )
        self.assertTrue(rows["uniprot:PVALID"]["ready_for_import_preview"])
        self.assertEqual(
            rows["uniprot:PREPAIR"]["repair_bucket"],
            "locator_repair",
        )
        self.assertEqual(
            rows["uniprot:PBULK"]["merge_status"],
            "scaleout_bulk_only_candidate",
        )

        import_ready = build_external_admission_import_ready_preview(merged)
        repair_queue = build_external_admission_repair_queue(merged)
        self.assertEqual(import_ready["candidate_count"], 1)
        self.assertEqual(repair_queue["candidate_count"], 1)
        self.assertTrue(import_ready["rows"][0]["non_overlap_checks"]["exact_current702_non_overlap"])


if __name__ == "__main__":
    unittest.main()
