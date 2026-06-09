from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.external_materialization_admission_batch import (
    build_external_materialization_admission_batch,
)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class ExternalMaterializationAdmissionBatchTests(unittest.TestCase):
    def test_materializes_coordinate_and_locator_and_emits_import_ready_preview(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_cwd = Path.cwd()
            os.chdir(root)
            try:
                ready_preview = root / "artifacts" / "ready.json"
                provisional_preview = root / "artifacts" / "provisional.json"
                pilot = root / "artifacts" / "pilot.json"
                bulk = root / "artifacts" / "bulk.json"
                current_manifest = root / "artifacts" / "current_manifest.json"
                label_registry = root / "data" / "registries" / "curated_mechanism_labels.json"
                locator_dir = root / "artifacts" / "locators"
                coordinate_dir = root / "artifacts" / "coords"

                full_ready_row = {
                    "candidate_id": "uniprot:PTEST1",
                    "accession": "PTEST1",
                    "stable_candidate_key": "external::ptest1",
                    "target_family_lane": "phosphoryl transfer",
                    "lane_id": "phosphoryl_transfer",
                    "reviewed_status": "reviewed",
                    "source_hashes": {
                        "uniprot_search_row_sha256": "a" * 64,
                        "uniprot_entry_record_sha256": "b" * 64,
                        "rhea_records_sha256": "c" * 64,
                    },
                    "source_provenance": {
                        "uniprot_entry_url": "https://rest.uniprot.org/uniprotkb/PTEST1",
                        "uniprot_search_url": "https://rest.uniprot.org/uniprotkb/search",
                        "query_timestamp_utc": "2026-06-08T00:00:00Z",
                    },
                    "coordinate_source_status": "afdb_predicted_coordinate_provenance_available",
                    "coordinate_mapping_basis": "direct_uniprot_to_afdb_sequence_positions",
                    "afdb_or_pdb_identifier": "AF-PTEST1-F1",
                    "alphafold_ids": ["PTEST1"],
                    "pdb_ids": [],
                    "residue_locators": [
                        {
                            "exact": True,
                            "position": 1,
                            "feature_code": "ACT_SITE",
                            "feature_type": "Active site",
                        },
                        {
                            "exact": True,
                            "position": 2,
                            "feature_code": "BINDING",
                            "feature_type": "Binding site",
                            "ligand_name": "ATP",
                        },
                    ],
                    "rhea_ec_provenance": {
                        "ec_numbers": ["2.7.1.1"],
                        "specific_ec_count": 1,
                        "rhea_record_count": 1,
                        "rhea_records": [{"rhea_id": "RHEA:1"}],
                    },
                    "duplicate_current_registry_conflict": {
                        "duplicate_or_current_registry_conflict": False,
                        "current_registry_conflict_status": "no_exact_current702_accession_or_sequence_sha_overlap",
                        "exact_sequence_sha256": "d" * 64,
                    },
                }
                full_blocked_row = {
                    **full_ready_row,
                    "candidate_id": "uniprot:PTEST2",
                    "accession": "PTEST2",
                    "stable_candidate_key": "external::ptest2",
                    "target_family_lane": "PLP children",
                    "lane_id": "plp_children",
                    "afdb_or_pdb_identifier": "AF-PTEST2-F1",
                    "alphafold_ids": ["PTEST2"],
                    "source_hashes": {
                        "uniprot_search_row_sha256": "e" * 64,
                        "uniprot_entry_record_sha256": "f" * 64,
                        "rhea_records_sha256": "1" * 64,
                    },
                    "residue_locators": [
                        {
                            "exact": True,
                            "position": 1,
                            "feature_code": "ACT_SITE",
                            "feature_type": "Active site",
                        }
                    ],
                }
                _write_json(
                    ready_preview,
                    {
                        "rows": [
                            {
                                "candidate_id": "uniprot:PTEST1",
                                "target_family_lane": "phosphoryl transfer",
                                "terminal_state": "admission_ready_pending_coordinate_materialization",
                            }
                        ]
                    },
                )
                _write_json(
                    provisional_preview,
                    {
                        "rows": [
                            {
                                "candidate_id": "uniprot:PTEST2",
                                "target_family_lane": "PLP children",
                                "terminal_state": "provisional_external_countable_preflight_candidate",
                            }
                        ]
                    },
                )
                _write_json(pilot, {"rows": [full_ready_row]})
                _write_json(bulk, {"rows": [full_blocked_row]})
                _write_json(current_manifest, {"rows": []})
                _write_json(label_registry, [])

                def fake_fetcher(source: str, structure_id: str) -> str:
                    self.assertEqual(source, "alphafold")
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
                            "ATOM 1 C CA . SER A 1 1 ? 0.0 0.0 0.0 1.00 1.00 ? 1 SER A CA 1",
                            "ATOM 2 C CA . THR A 1 2 ? 1.0 0.0 0.0 1.00 1.00 ? 2 THR A CA 1",
                            "#",
                        ]
                    )

                artifact, preview = build_external_materialization_admission_batch(
                    ready_preview_path=ready_preview,
                    provisional_preview_path=provisional_preview,
                    pilot_path=pilot,
                    bulk_path=bulk,
                    current_manifest_path=current_manifest,
                    label_registry_path=label_registry,
                    coordinate_dir=coordinate_dir,
                    locator_dir=locator_dir,
                    created_utc="2026-06-09T00:00:00Z",
                    fetcher=fake_fetcher,
                )
                coordinate_exists = Path(preview["rows"][0]["coordinate_path"]).exists()
                locator_exists = Path(preview["rows"][0]["locator_sidecar_path"]).exists()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(artifact["counts"]["input_rows"], 2)
        self.assertEqual(artifact["counts"]["import_ready_preview"], 1)
        self.assertEqual(artifact["counts"]["repairable_locator_blockers"], 1)
        self.assertEqual(preview["candidate_count"], 1)
        ready_row = preview["rows"][0]
        self.assertEqual(ready_row["candidate_id"], "uniprot:PTEST1")
        self.assertTrue(coordinate_exists)
        self.assertTrue(locator_exists)


if __name__ == "__main__":
    unittest.main()
