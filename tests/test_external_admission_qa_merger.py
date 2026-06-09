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
        "source_provenance": {"query_timestamp_utc": "2026-06-08T00:00:00Z"},
        "exact_next_action": "continue gate",
        "blocker_basis": {
            "duplicate_or_current_registry_conflict": False,
        },
    }


def _validation_row(accession: str, *, terminal_state: str) -> dict[str, object]:
    return {
        "stable_candidate_key": f"external_source_ingestion:uniprot:{accession}",
        "candidate_id": f"uniprot:{accession}",
        "accession": accession,
        "target_family_lane": "redox oxygen/sulfur",
        "lane_id": "redox_oxygen_sulfur",
        "terminal_state": terminal_state,
        "source_hashes": {
            "uniprot_search_row_sha256": "a" * 64,
            "uniprot_entry_record_sha256": "b" * 64,
            "rhea_records_sha256": "c" * 64,
        },
        "source_provenance": {"query_timestamp_utc": "2026-06-08T00:00:00Z"},
        "exact_next_action": "materialize locator",
        "duplicate_status": {
            "recomputed_current_registry_duplicate_status": {
                "duplicate_or_current_registry_conflict": False,
            }
        },
    }


class ExternalAdmissionQaMergerTests(unittest.TestCase):
    def test_merges_validation_upgrades_and_builds_repair_queue(self) -> None:
        validation = {
            "counts": {"validated_rows": 1},
            "rows": [
                _validation_row(
                    "PVALID",
                    terminal_state="admission_ready_pending_locator_materialization",
                )
            ],
        }
        bulk = {
            "candidate_count": 3,
            "rows": [
                _bulk_row(
                    "PVALID",
                    terminal_state="provisional_external_countable_preflight_candidate",
                ),
                _bulk_row("PREPAIR", terminal_state="coordinate_repair_candidate"),
                _bulk_row("PBULK", terminal_state="locator_ready_candidate"),
            ],
        }
        bulk_preview = {
            "candidate_count": 1,
            "rows": [
                {
                    "candidate_id": "uniprot:PVALID",
                }
            ],
        }
        scaleout = {
            "canonical_records": [
                {
                    "canonical_key": "canon1",
                    "canonical_terminal_state": "review_only_evidence",
                    "source_members": [{"accession": "PBULK"}],
                }
            ]
        }

        merged = build_external_admission_merged_surface(
            validation_payload=validation,
            bulk_scout_payload=bulk,
            bulk_preview_payload=bulk_preview,
            scaleout_merged_payload=scaleout,
            created_utc="2026-06-08T00:00:00Z",
        )

        self.assertTrue(merged["validation_checks"]["passed"])
        self.assertEqual(merged["counts"]["merged_rows"], 3)
        self.assertEqual(merged["counts"]["validation_upgrade_rows"], 1)
        self.assertEqual(merged["counts"]["bulk_only_rows"], 2)
        self.assertEqual(merged["terminal_state_counts"]["admission_ready_pending_locator_materialization"], 1)

        rows = {row["candidate_id"]: row for row in merged["rows"]}
        self.assertEqual(
            rows["uniprot:PVALID"]["merge_status"],
            "validated_upgrade_from_bulk_provisional",
        )
        self.assertEqual(
            rows["uniprot:PREPAIR"]["repair_bucket"],
            "coordinate_repair",
        )
        self.assertTrue(
            rows["uniprot:PBULK"]["scaleout_overlap"]["overlaps_current_main_scaleout_surface"]
        )

        import_ready = build_external_admission_import_ready_preview(merged)
        repair_queue = build_external_admission_repair_queue(merged)
        self.assertEqual(import_ready["candidate_count"], 0)
        self.assertEqual(repair_queue["candidate_count"], 2)


if __name__ == "__main__":
    unittest.main()
