from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.external_source_admission_validation import (
    build_external_source_admission_validation,
    build_external_source_admission_ready_preview,
)


def _source_hashes(seed: str) -> dict[str, str]:
    return {
        "uniprot_search_row_sha256": seed * 64,
        "uniprot_entry_record_sha256": chr(ord(seed) + 1) * 64,
        "rhea_records_sha256": chr(ord(seed) + 2) * 64,
    }


def _pilot_row(accession: str, *, pdb_id: str, seed: str) -> dict[str, object]:
    source_hashes = _source_hashes(seed)
    return {
        "stable_candidate_key": f"external_source_ingestion:uniprot:{accession}",
        "candidate_id": f"uniprot:{accession}",
        "accession": accession,
        "target_family_lane": "redox oxygen/sulfur",
        "lane_id": "redox_oxygen_sulfur",
        "source_query": "reviewed test query",
        "terminal_state": "external_countable_preflight_candidate",
        "reviewed_status": "reviewed",
        "residue_locators": [
            {
                "position": 10,
                "end": 10,
                "exact": True,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "evidence_codes": ["ECO:0000269"],
            }
        ],
        "source_evidence_feature_count": 1,
        "source_evidence_codes": ["ECO:0000269"],
        "coordinate_source": "PDB",
        "coordinate_source_status": "experimental_pdb_coordinate_provenance_available",
        "afdb_or_pdb_identifier": pdb_id,
        "pdb_ids": [pdb_id],
        "alphafold_ids": [accession],
        "coordinate_mapping_basis": "UniProt residue positions map directly",
        "rhea_ec_provenance": {
            "ec_numbers": ["1.14.14.18"],
            "specific_ec_count": 1,
            "rhea_record_count": 1,
            "rhea_records": [{"rhea_id": "RHEA:21764"}],
            "rhea_status": "rhea_provenance_available",
        },
        "duplicate_current_registry_conflict_status": (
            "no_exact_current702_accession_or_sequence_sha_overlap"
        ),
        "duplicate_current_registry_conflict": {
            "duplicate_or_current_registry_conflict": False,
            "current_registry_conflict_status": (
                "no_exact_current702_accession_or_sequence_sha_overlap"
            ),
            "exact_accession_matched_current_entry_ids": [],
            "exact_sequence_sha256": seed * 64,
            "exact_sequence_matched_current_entry_ids": [],
            "structural_duplicate_screen_status": "not_run_test",
        },
        "source_hashes": source_hashes,
        "source_provenance": {
            "query_timestamp_utc": "2026-06-08T00:00:00Z",
            "uniprot_search_url": "https://rest.uniprot.org/uniprotkb/search?query=x",
            "uniprot_entry_url": f"https://rest.uniprot.org/uniprotkb/{accession}.json",
        },
    }


class ExternalSourceAdmissionValidationTests(unittest.TestCase):
    def test_classifies_coordinate_and_locator_materialization_queues(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            artifacts_dir = root / "artifacts"
            artifacts_dir.mkdir()
            (artifacts_dir / "coords").mkdir()
            (artifacts_dir / "coords" / "pdb_1ABC.cif").write_text(
                "data_1ABC\n", encoding="utf-8"
            )
            manifest_path = root / "manifest.json"
            label_registry_path = root / "labels.json"
            manifest_path.write_text(json.dumps({"rows": []}), encoding="utf-8")
            label_registry_path.write_text("[]", encoding="utf-8")

            row_with_coordinate = _pilot_row("PNEW1", pdb_id="1ABC", seed="a")
            row_without_coordinate = _pilot_row("PNEW2", pdb_id="2ABC", seed="d")
            pilot = {
                "artifact_id": "pilot",
                "candidate_count": 2,
                "lane_summaries": [
                    {"target_family_lane": "redox oxygen/sulfur"}
                ],
                "source_artifacts": {
                    "current_manifest": {"path": str(manifest_path)},
                    "label_registry": {"path": str(label_registry_path)},
                },
                "rows": [row_with_coordinate, row_without_coordinate],
            }
            preview = {
                "artifact_id": "preview",
                "candidate_count": 2,
                "rows": [
                    {
                        "candidate_id": row_with_coordinate["candidate_id"],
                        "terminal_state": "external_countable_preflight_candidate",
                        "import_preview_candidate": True,
                        "source_hashes": row_with_coordinate["source_hashes"],
                    },
                    {
                        "candidate_id": row_without_coordinate["candidate_id"],
                        "terminal_state": "external_countable_preflight_candidate",
                        "import_preview_candidate": True,
                        "source_hashes": row_without_coordinate["source_hashes"],
                    },
                ],
            }
            pilot_path = root / "pilot.json"
            preview_path = root / "preview.json"
            pilot_path.write_text(json.dumps(pilot), encoding="utf-8")
            preview_path.write_text(json.dumps(preview), encoding="utf-8")

            artifact = build_external_source_admission_validation(
                pilot_path=pilot_path,
                import_preview_path=preview_path,
                expected_preview_count=2,
                artifacts_dir=artifacts_dir,
                locator_sidecar_dirs=(root / "missing_locators",),
                created_utc="2026-06-08T00:00:00Z",
            )

            self.assertTrue(artifact["validation_checks"]["passed"])
            rows = {row["candidate_id"]: row for row in artifact["rows"]}
            self.assertEqual(
                rows["uniprot:PNEW1"]["terminal_state"],
                "admission_ready_pending_locator_materialization",
            )
            self.assertEqual(
                rows["uniprot:PNEW2"]["terminal_state"],
                "admission_ready_pending_coordinate_materialization",
            )
            self.assertEqual(artifact["counts"]["admission_ready_rows"], 2)
            self.assertEqual(
                artifact["counts"]["direct_external_label_candidate_rows"], 0
            )

            ready_preview = build_external_source_admission_ready_preview(
                artifact, created_utc="2026-06-08T00:00:00Z"
            )
            self.assertEqual(ready_preview["candidate_count"], 2)
            self.assertFalse(ready_preview["rows"][0]["ready_for_production_label_import"])


if __name__ == "__main__":
    unittest.main()
