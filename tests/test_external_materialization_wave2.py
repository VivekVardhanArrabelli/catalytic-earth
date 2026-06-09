from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.external_materialization_wave2 import (
    build_external_materialization_wave2,
    write_external_materialization_wave2,
)


def _row(
    accession: str,
    terminal_state: str,
    *,
    exact_locators: int = 2,
) -> dict[str, object]:
    locators = [
        {
            "position": index + 10,
            "end": index + 10,
            "exact": True,
            "feature_code": "ACT_SITE",
            "feature_type": "Active site",
            "evidence_codes": ["ECO:0000269"],
        }
        for index in range(exact_locators)
    ]
    return {
        "candidate_id": f"uniprot:{accession}",
        "stable_candidate_key": f"external_source_ingestion:uniprot:{accession}",
        "accession": accession,
        "target_family_lane": "redox oxygen/sulfur",
        "terminal_state": terminal_state,
        "afdb_or_pdb_identifier": f"AF-{accession}-F1",
        "alphafold_ids": [accession],
        "pdb_ids": [],
        "coordinate_source_status": "afdb_predicted_coordinate_provenance_available",
        "coordinate_mapping_basis": "UniProt residue positions map directly",
        "residue_locators": locators,
        "source_hashes": {
            "uniprot_search_row_sha256": "a" * 64,
            "uniprot_entry_record_sha256": "b" * 64,
            "rhea_records_sha256": "c" * 64,
        },
        "duplicate_status_summary": {
            "blocked_by_duplicate_or_current_registry_conflict": (
                terminal_state == "blocked_duplicate_or_current_registry_conflict"
            ),
            "current702_status": (
                "exact_current702_accession_overlap"
                if terminal_state == "blocked_duplicate_or_current_registry_conflict"
                else "no_exact_current702_accession_or_sequence_sha_overlap"
            ),
            "external_pilot_status": "no_exact_external_pilot_accession_or_sequence_sha_overlap",
        },
    }


class ExternalMaterializationWave2Tests(unittest.TestCase):
    def test_builds_low_disk_sidecar_continuation_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            merged_path = root / "merged.json"
            import_ready_path = root / "import_ready.json"
            merged = {
                "artifact_id": "merged",
                "source_artifacts": {
                    "external_bulk_ingestion_scaleout": {
                        "spec": "origin/test:bulk.json",
                        "sha256": "d" * 64,
                    }
                },
                "rows": [
                    _row("PREADY", "import_ready_preview"),
                    _row("PLOC", "provisional_external_countable_preflight_candidate"),
                    _row("PDUP", "blocked_duplicate_or_current_registry_conflict"),
                    _row("PNOLOC", "coordinate_ready_pending_locator", exact_locators=0),
                ],
            }
            import_ready = {
                "artifact_id": "import_ready",
                "rows": [
                    {
                        "candidate_id": "uniprot:PREADY",
                        "accession": "PREADY",
                        "coordinate_path": "artifacts/external/pready.cif",
                        "locator_sidecar_path": "artifacts/locators/pready.json",
                        "ready_for_controlled_import_review": True,
                        "ready_for_production_label_import": False,
                    }
                ],
            }
            merged_path.write_text(json.dumps(merged), encoding="utf-8")
            import_ready_path.write_text(json.dumps(import_ready), encoding="utf-8")

            artifact, preview, repair, sidecars = build_external_materialization_wave2(
                merged_surface_path=merged_path,
                import_ready_source_path=import_ready_path,
                locator_dir=root / "locators",
                created_utc="2026-06-09T00:00:00Z",
                disk_free_gib_at_start=7.1,
            )

            self.assertTrue(artifact["validation_checks"]["passed"])
            self.assertEqual(artifact["counts"]["input_rows"], 4)
            self.assertEqual(artifact["counts"]["import_ready_preview_count"], 1)
            self.assertEqual(artifact["counts"]["repair_queue_count"], 3)
            self.assertEqual(artifact["counts"]["locator_sidecars_materialized_new"], 1)
            self.assertEqual(preview["candidate_count"], 1)
            self.assertEqual(repair["candidate_count"], 3)
            self.assertEqual(len(sidecars), 1)
            self.assertEqual(
                sidecars[0][1]["source_free_active_site_locator_status"],
                "materialized_pending_coordinate_local_residue_identity",
            )

    def test_writer_emits_artifacts_and_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            merged_path = root / "merged.json"
            import_ready_path = root / "import_ready.json"
            merged_path.write_text(
                json.dumps(
                    {
                        "artifact_id": "merged",
                        "source_artifacts": {},
                        "rows": [
                            _row(
                                "PLOC",
                                "provisional_external_countable_preflight_candidate",
                            )
                        ],
                    }
                ),
                encoding="utf-8",
            )
            import_ready_path.write_text(
                json.dumps({"artifact_id": "import_ready", "rows": []}),
                encoding="utf-8",
            )
            out_path = root / "wave2.json"
            preview_path = root / "preview.json"
            repair_path = root / "repair.json"
            report_path = root / "report.md"
            locator_dir = root / "locators"

            artifact = write_external_materialization_wave2(
                merged_surface_path=merged_path,
                import_ready_source_path=import_ready_path,
                out_path=out_path,
                import_ready_preview_path=preview_path,
                repair_queue_path=repair_path,
                report_path=report_path,
                locator_dir=locator_dir,
                created_utc="2026-06-09T00:00:00Z",
            )

            self.assertEqual(artifact["counts"]["locator_sidecars_materialized_new"], 1)
            self.assertTrue(out_path.exists())
            self.assertTrue(preview_path.exists())
            self.assertTrue(repair_path.exists())
            self.assertTrue(report_path.exists())
            self.assertEqual(len(list(locator_dir.glob("*.json"))), 1)

    def test_additional_shard_preview_stays_coordinate_continuation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            merged_path = root / "merged.json"
            import_ready_path = root / "import_ready.json"
            shard_path = root / "shard.json"
            shard_preview_path = root / "shard_preview.json"
            merged_path.write_text(
                json.dumps(
                    {
                        "artifact_id": "merged",
                        "source_artifacts": {},
                        "rows": [_row("PREADY", "import_ready_preview")],
                    }
                ),
                encoding="utf-8",
            )
            import_ready_path.write_text(
                json.dumps(
                    {
                        "artifact_id": "import_ready",
                        "rows": [
                            {
                                "candidate_id": "uniprot:PREADY",
                                "accession": "PREADY",
                                "coordinate_path": "artifacts/external/pready.cif",
                                "locator_sidecar_path": "artifacts/locators/pready.json",
                                "ready_for_controlled_import_review": True,
                                "ready_for_production_label_import": False,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            shard_path.write_text(
                json.dumps(
                    {
                        "artifact_id": "redox_shard",
                        "rows": [_row("PSHARD", "import_ready_preview")],
                    }
                ),
                encoding="utf-8",
            )
            shard_preview_path.write_text(
                json.dumps(
                    {
                        "artifact_id": "redox_shard_preview",
                        "rows": [_row("PSHARD", "import_ready_preview")],
                    }
                ),
                encoding="utf-8",
            )

            artifact, preview, repair, sidecars = build_external_materialization_wave2(
                merged_surface_path=merged_path,
                import_ready_source_path=import_ready_path,
                additional_surface_paths=[shard_path],
                additional_import_ready_source_paths=[shard_preview_path],
                locator_dir=root / "locators",
                created_utc="2026-06-09T00:00:00Z",
            )

            self.assertTrue(artifact["validation_checks"]["passed"])
            self.assertEqual(artifact["counts"]["input_rows"], 2)
            self.assertEqual(artifact["counts"]["import_ready_preview_count"], 1)
            self.assertEqual(preview["candidate_count"], 1)
            self.assertEqual(repair["candidate_count"], 1)
            self.assertEqual(len(sidecars), 1)
            self.assertEqual(
                repair["rows"][0]["wave2_terminal_state"],
                (
                    "shard_import_ready_preview_locator_sidecar_"
                    "materialized_coordinate_pending"
                ),
            )

    def test_bounded_coordinate_materialization_promotes_ready_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            merged_path = root / "merged.json"
            import_ready_path = root / "import_ready.json"
            merged_path.write_text(
                json.dumps(
                    {
                        "artifact_id": "merged",
                        "source_artifacts": {},
                        "rows": [_row("PMAT", "locator_ready_candidate")],
                    }
                ),
                encoding="utf-8",
            )
            import_ready_path.write_text(
                json.dumps({"artifact_id": "import_ready", "rows": []}),
                encoding="utf-8",
            )

            def fake_fetcher(source: str, structure_id: str) -> str:
                self.assertEqual(source, "alphafold")
                self.assertEqual(structure_id, "PMAT")
                return "\n".join(
                    [
                        "data_TEST",
                        "#",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.id",
                        "_atom_site.type_symbol",
                        "_atom_site.label_atom_id",
                        "_atom_site.label_alt_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.label_entity_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.pdbx_PDB_ins_code",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "_atom_site.occupancy",
                        "_atom_site.B_iso_or_equiv",
                        "_atom_site.pdbx_formal_charge",
                        "_atom_site.auth_seq_id",
                        "_atom_site.auth_comp_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.auth_atom_id",
                        "_atom_site.pdbx_PDB_model_num",
                        "ATOM 1 C CA . SER A 1 10 ? 0.0 0.0 0.0 1.00 1.00 ? 10 SER A CA 1",
                        "ATOM 2 C CA . THR A 1 11 ? 1.0 0.0 0.0 1.00 1.00 ? 11 THR A CA 1",
                        "#",
                    ]
                )

            artifact, preview, repair, sidecars = build_external_materialization_wave2(
                merged_surface_path=merged_path,
                import_ready_source_path=import_ready_path,
                locator_dir=root / "locators",
                coordinate_dir=root / "coords",
                created_utc="2026-06-09T00:00:00Z",
                disk_free_gib_at_start=20.0,
                max_coordinate_downloads=1,
                coordinate_fetcher=fake_fetcher,
                disk_free_gib_provider=lambda _path: 20.0,
            )

            self.assertTrue(artifact["validation_checks"]["passed"])
            self.assertEqual(artifact["counts"]["coordinate_downloads_performed"], 1)
            self.assertEqual(
                artifact["counts"]["coordinate_ready_promoted_preview_count"], 1
            )
            self.assertEqual(preview["candidate_count"], 1)
            self.assertEqual(repair["candidate_count"], 0)
            self.assertEqual(len(sidecars), 1)
            self.assertEqual(
                preview["rows"][0]["wave2_materialization_state"],
                "coordinate_and_locator_identity_materialized",
            )


if __name__ == "__main__":
    unittest.main()
