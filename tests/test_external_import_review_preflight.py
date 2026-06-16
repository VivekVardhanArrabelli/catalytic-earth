from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.external_import_review_preflight import (
    build_external_batch_import_approval_packet,
    build_external_import_review_preflight,
    build_external_import_review_ready_preview,
    build_external_import_review_repair_queue,
    build_targeted_expansion_defense_ledger,
    render_targeted_expansion_defense_ledger_report,
)


def _hashes(seed: str) -> dict[str, str]:
    alphabet = "0123456789abcdef"
    index = alphabet.index(seed)
    return {
        "full_row_sha256": alphabet[index] * 64,
        "queue_row_sha256": alphabet[(index + 1) % len(alphabet)] * 64,
        "uniprot_entry_record_sha256": alphabet[(index + 2) % len(alphabet)] * 64,
        "uniprot_search_row_sha256": alphabet[(index + 3) % len(alphabet)] * 64,
    }


def _preview_row(
    candidate: str,
    *,
    lane: str,
    coordinate_path: str,
    locator_path: str,
    seed: str,
    external_duplicate: bool = False,
) -> dict[str, object]:
    return {
        "candidate_id": f"uniprot:{candidate}",
        "accession": candidate,
        "stable_candidate_key": f"external_source_ingestion:uniprot:{candidate}",
        "target_family_lane": lane,
        "merge_status": "materialized_from_provisional_queue",
        "terminal_state": "import_ready_preview",
        "coordinate_path": coordinate_path,
        "locator_sidecar_path": locator_path,
        "duplicate_status": {
            "current_registry_conflict_status": (
                "no_exact_current702_accession_or_sequence_sha_overlap"
            ),
            "duplicate_or_current_registry_conflict": False,
            "exact_accession_matched_current_entry_ids": [],
            "exact_sequence_matched_current_entry_ids": [],
            "exact_sequence_sha256": seed * 64,
        },
        "non_overlap_checks": {
            "exact_current702_non_overlap": True,
            "external_duplicate_overlap_present": external_duplicate,
        },
        "source_hashes": _hashes(seed),
        "source_provenance": {
            "query_timestamp_utc": "2026-06-09T00:00:00Z",
            "source_hash_basis": "canonical_normalized_source_records",
        },
    }


def _locator(candidate: str, coordinate_path: str, coordinate_hash: str | None) -> dict[str, object]:
    provenance: dict[str, object] = {
        "coordinate_path": coordinate_path,
    }
    if coordinate_hash is not None:
        provenance["coordinate_sha256"] = coordinate_hash
    return {
        "artifact_id": f"locator_{candidate}",
        "candidate_id": f"uniprot:{candidate}",
        "schema_version": "v3.external_source_free_active_site_locator_review_only",
        "source_free_active_site_locator_status": "ready",
        "coordinate_provenance": provenance,
        "guardrails": {
            "label_import_performed": False,
            "production_registry_edited": False,
            "review_only": True,
        },
        "residue_locators": [
            {
                "sequence_position": 10,
                "residue_code": "SER",
                "locator_confidence": 1.0,
            }
        ],
    }


class ExternalImportReviewPreflightTests(unittest.TestCase):
    def test_classifies_import_review_terminal_states(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            coords = root / "coords"
            locators = root / "locators"
            coords.mkdir()
            locators.mkdir()

            ready_coord = coords / "ready.cif"
            dup_coord = coords / "dup.cif"
            structural_coord = coords / "pdb_1ABC.cif"
            near_coord = coords / "near.cif"
            for path in (ready_coord, dup_coord, structural_coord, near_coord):
                path.write_text("data_test\n", encoding="utf-8")

            rows = [
                _preview_row(
                    "PREADY",
                    lane="metal hydrolase",
                    coordinate_path=str(ready_coord),
                    locator_path=str(locators / "ready.json"),
                    seed="a",
                ),
                _preview_row(
                    "PDUP",
                    lane="redox oxygen/sulfur",
                    coordinate_path=str(dup_coord),
                    locator_path=str(locators / "dup.json"),
                    seed="e",
                    external_duplicate=True,
                ),
                _preview_row(
                    "PCOORD",
                    lane="phosphoryl transfer",
                    coordinate_path=str(coords / "missing.cif"),
                    locator_path=str(locators / "coord.json"),
                    seed="9",
                ),
                _preview_row(
                    "PSTRUCT",
                    lane="PLP children",
                    coordinate_path=str(structural_coord),
                    locator_path=str(locators / "struct.json"),
                    seed="b",
                ),
                _preview_row(
                    "PNEAR",
                    lane="near-orphan/no-reliable-structure",
                    coordinate_path=str(near_coord),
                    locator_path=str(locators / "near.json"),
                    seed="c",
                ),
            ]
            for candidate, coord, hash_value in [
                ("PREADY", ready_coord, "1" * 64),
                ("PDUP", dup_coord, "2" * 64),
                ("PCOORD", coords / "missing.cif", None),
                ("PSTRUCT", structural_coord, "3" * 64),
                ("PNEAR", near_coord, "4" * 64),
            ]:
                (locators / f"{candidate[1:].lower()}.json").write_text(
                    json.dumps(_locator(candidate, str(coord), hash_value)),
                    encoding="utf-8",
                )

            preview = {"candidate_count": len(rows), "rows": rows}
            merged = {
                "rows": [
                    {
                        **row,
                        "external_duplicate_conflict": (
                            row["candidate_id"] == "uniprot:PDUP"
                        ),
                        "afdb_or_pdb_identifier": (
                            "1ABC"
                            if row["candidate_id"] == "uniprot:PSTRUCT"
                            else None
                        ),
                    }
                    for row in rows
                ]
            }
            materialization = {
                "rows": [
                    {
                        "candidate_id": row["candidate_id"],
                        "row_sha256": row["source_hashes"]["full_row_sha256"],
                    }
                    for row in rows
                ]
            }
            current_manifest = {
                "rows": [
                    {
                        "entry_id": "m_csa:1",
                        "selected_structure_id": "1ABC",
                        "coordinate_path": "artifacts/current/pdb_1ABC.cif",
                    }
                ],
                "structures": [],
            }
            preview_path = root / "preview.json"
            merged_path = root / "merged.json"
            materialization_path = root / "materialization.json"
            current_path = root / "current.json"
            preview_path.write_text(json.dumps(preview), encoding="utf-8")
            merged_path.write_text(json.dumps(merged), encoding="utf-8")
            materialization_path.write_text(json.dumps(materialization), encoding="utf-8")
            current_path.write_text(json.dumps(current_manifest), encoding="utf-8")

            artifact = build_external_import_review_preflight(
                preview_source=preview_path,
                merged_surface_source=merged_path,
                materialization_source=materialization_path,
                repair_surface_source=None,
                current702_coordinate_manifest_path=current_path,
                tree_refs=(),
                expected_preview_count=5,
                expected_repair_count=0,
                expected_review_surface_count=5,
                created_utc="2026-06-09T00:00:00Z",
            )

            states = {row["candidate_id"]: row["terminal_state"] for row in artifact["rows"]}
            self.assertEqual(
                states["uniprot:PREADY"], "controlled_import_review_ready"
            )
            self.assertEqual(
                states["uniprot:PDUP"], "duplicate_external_conflict"
            )
            self.assertEqual(
                states["uniprot:PCOORD"], "repairable_coordinate_blocker"
            )
            self.assertEqual(
                states["uniprot:PSTRUCT"], "needs_structural_duplicate_screen"
            )
            self.assertEqual(
                states["uniprot:PNEAR"], "needs_family_policy_review"
            )
            self.assertTrue(artifact["validation_checks"]["passed"])
            self.assertEqual(artifact["counts"]["controlled_import_review_ready"], 1)

            ready_preview = build_external_import_review_ready_preview(artifact)
            repair_queue = build_external_import_review_repair_queue(artifact)
            self.assertEqual(ready_preview["candidate_count"], 1)
            self.assertEqual(repair_queue["candidate_count"], 4)

            packet = build_external_batch_import_approval_packet(
                artifact,
                ready_preview,
                repair_queue,
                artifact_date="20260610",
                current_main_commit="test-head",
            )
            self.assertEqual(
                packet["artifact_id"],
                "v3_external_batch_import_approval_packet_current702_20260610",
            )
            self.assertEqual(
                packet["batch_approval"][
                    "rows_that_can_become_countable_after_one_batch_approval"
                ],
                1,
            )
            self.assertEqual(packet["batch_approval"]["blocked_rows_remaining"], 4)
            self.assertEqual(
                packet["blocked_mechanical_gate_counts"][
                    "current702_structural_duplicate_screen"
                ],
                1,
            )
            self.assertTrue(packet["validation_checks"]["passed"])

            ledger = build_targeted_expansion_defense_ledger(
                artifact,
                packet,
                previous_ledger={
                    "expansion_thesis": [
                        "Prior non-random family rationale.",
                        "The import-review preflight classifies 275 rows as controlled import-review ready.",
                        "The selected families remain targeted because they map to prior failure modes.",
                    ],
                    "count_table": {
                        "current_label_surface": {"countable_labels": 702}
                    },
                    "family_lane_rationale": [
                        {
                            "family_or_lane": "metal hydrolase",
                            "included_because": "Known metal/fold confounding lane.",
                            "failure_mode_or_atlas_need": "Needs duplicate gates.",
                            "supporting_artifacts": [],
                        }
                    ],
                },
                artifact_date="20260610",
                current_main_commit="test-head",
            )
            self.assertEqual(
                ledger["artifact_id"],
                "v3_targeted_expansion_defense_ledger_current702_20260610",
            )
            self.assertEqual(
                ledger["count_table"]["batch_approval_packet"][
                    "rows_can_become_countable_after_one_batch_approval"
                ],
                1,
            )
            self.assertEqual(
                ledger["count_table"]["post_batch_projection"][
                    "if_one_batch_approval_accepts_ready_rows"
                ],
                703,
            )
            dynamic_ledger_text = "\n".join(
                ledger["expansion_thesis"]
                + ledger["review_narrative"]["honest_claims_for_review"]
            )
            self.assertIn(
                "contains 5 unique candidate rows: 5 preview rows and 0 repair-surface rows",
                dynamic_ledger_text,
            )
            self.assertIn(
                "surface of 5 unique external candidates",
                dynamic_ledger_text,
            )
            self.assertNotIn("12,495", dynamic_ledger_text)
            self.assertNotIn("11,895", dynamic_ledger_text)
            self.assertNotIn("275 rows", dynamic_ledger_text)
            report = render_targeted_expansion_defense_ledger_report(ledger)
            self.assertIn(
                "| Wave 2 review surface | 5 | 5 preview rows plus 0 repair-surface rows. |",
                report,
            )
            self.assertNotIn("11,895", report)
            self.assertTrue(ledger["validation_checks"]["passed"])

    def test_classifies_wave2_repair_surface_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            preview_path = root / "preview.json"
            repair_path = root / "repair.json"
            materialization_path = root / "materialization.json"
            current_path = root / "current.json"

            preview_path.write_text(json.dumps({"rows": []}), encoding="utf-8")
            repair_rows = [
                {
                    "candidate_id": "uniprot:PCUR",
                    "accession": "PCUR",
                    "target_family_lane": "metal hydrolase",
                    "wave2_terminal_state": "blocked_duplicate_or_current_registry_conflict",
                    "repair_bucket": "duplicate_conflict_no_import",
                    "duplicate_status": {
                        "current702_status": "exact_current702_accession_overlap",
                    },
                    "source_hashes": _hashes("a"),
                    "source_occurrences": [
                        {
                            "source_key": "source-a",
                            "source_path": "artifacts/source-a.json",
                            "terminal_state": "blocked_duplicate_or_current_registry_conflict",
                        }
                    ],
                },
                {
                    "candidate_id": "uniprot:PCOORD",
                    "accession": "PCOORD",
                    "target_family_lane": "redox oxygen/sulfur",
                    "wave2_terminal_state": (
                        "shard_import_ready_preview_locator_sidecar_reused_coordinate_pending"
                    ),
                    "repair_bucket": "coordinate_materialization_continuation_due_disk_floor",
                    "duplicate_status": {
                        "current702_status": (
                            "no_exact_current702_accession_or_sequence_sha_overlap"
                        ),
                        "prior_external_status": (
                            "no_exact_prior_external_artifact_or_branch_overlap"
                        ),
                    },
                    "source_hashes": _hashes("b"),
                    "source_occurrences": [
                        {
                            "source_key": "source-b",
                            "source_path": "artifacts/source-b.json",
                            "terminal_state": "import_ready_preview",
                        }
                    ],
                },
            ]
            repair_path.write_text(json.dumps({"rows": repair_rows}), encoding="utf-8")
            materialization_path.write_text(
                json.dumps({"rows": repair_rows}), encoding="utf-8"
            )
            current_path.write_text(json.dumps({"rows": [], "structures": []}), encoding="utf-8")

            artifact = build_external_import_review_preflight(
                preview_source=preview_path,
                merged_surface_source=None,
                materialization_source=materialization_path,
                repair_surface_source=repair_path,
                current702_coordinate_manifest_path=current_path,
                tree_refs=(),
                expected_preview_count=0,
                expected_repair_count=2,
                expected_review_surface_count=2,
                created_utc="2026-06-09T00:00:00Z",
            )

            states = {row["candidate_id"]: row["terminal_state"] for row in artifact["rows"]}
            self.assertEqual(states["uniprot:PCUR"], "duplicate_current702_conflict")
            self.assertEqual(states["uniprot:PCOORD"], "repairable_coordinate_blocker")
            self.assertTrue(artifact["validation_checks"]["passed"])
            self.assertEqual(artifact["counts"]["review_surface_rows"], 2)


if __name__ == "__main__":
    unittest.main()
