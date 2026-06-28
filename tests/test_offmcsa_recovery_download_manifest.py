from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.offmcsa_recovery_download_manifest import (
    build_offmcsa_recovery_download_manifest,
    select_trusted_positives,
    write_offmcsa_recovery_download_manifest,
)


def _bronze() -> list[dict]:
    return [
        # trusted, atlas family, non-mcsa -> selected
        {"entry_id": "uniprot:Q1", "fingerprint_id": "fpA", "confidence": "high", "label_type": "seed_fingerprint"},
        # medium confidence -> excluded
        {"entry_id": "uniprot:Q2", "fingerprint_id": "fpA", "confidence": "medium", "label_type": "seed_fingerprint"},
        # out_of_scope -> excluded
        {"entry_id": "uniprot:Q3", "fingerprint_id": "fpA", "confidence": "high", "label_type": "out_of_scope"},
        # family not in atlas -> excluded
        {"entry_id": "uniprot:Q4", "fingerprint_id": "fpZ", "confidence": "high", "label_type": "seed_fingerprint"},
        # M-CSA accession -> excluded
        {"entry_id": "uniprot:M1", "fingerprint_id": "fpB", "confidence": "high", "label_type": "seed_fingerprint"},
        # already structured -> excluded
        {"entry_id": "uniprot:S1", "fingerprint_id": "fpB", "confidence": "high", "label_type": "seed_fingerprint"},
        # second good one
        {"entry_id": "uniprot:Q5", "fingerprint_id": "fpB", "confidence": "high", "label_type": "seed_fingerprint"},
    ]


class OffMcsaRecoveryDownloadManifestTests(unittest.TestCase):
    def test_selection_filters_apply(self) -> None:
        selected = select_trusted_positives(
            bronze_rows=_bronze(),
            families={"fpA", "fpB"},
            mcsa={"M1"},
            structured={"S1"},
        )
        accs = [r["accession"] for r in selected]
        self.assertEqual(accs, ["Q1", "Q5"])
        self.assertTrue(
            selected[0]["alphafold_cif_url"].endswith("AF-Q1-F1-model_v4.cif")
        )

    def test_manifest_summary_and_guardrails(self) -> None:
        selected = select_trusted_positives(
            bronze_rows=_bronze(), families={"fpA", "fpB"}, mcsa={"M1"}, structured={"S1"}
        )
        manifest = build_offmcsa_recovery_download_manifest(
            selected=selected, families={"fpA", "fpB"}
        )
        self.assertEqual(manifest["status"], "download_manifest_ready_awaiting_authorization")
        self.assertEqual(manifest["summary"]["selected_structures_to_download"], 2)
        self.assertEqual(manifest["summary"]["families_covered"], 2)
        self.assertFalse(manifest["guardrails"]["downloads_performed"])
        self.assertTrue(manifest["guardrails"]["fetch_requires_explicit_authorization"])
        self.assertTrue(
            manifest["guardrails"][
                "fold_recovery_is_non_circular_admission_used_sequence_cofactor_not_structure"
            ]
        )

    def test_accession_list_hash_is_content_sensitive(self) -> None:
        a = build_offmcsa_recovery_download_manifest(
            selected=select_trusted_positives(
                bronze_rows=_bronze(), families={"fpA", "fpB"}, mcsa={"M1"}, structured={"S1"}
            ),
            families={"fpA", "fpB"},
        )
        b = build_offmcsa_recovery_download_manifest(
            selected=select_trusted_positives(
                bronze_rows=_bronze(), families={"fpA"}, mcsa={"M1"}, structured={"S1"}
            ),
            families={"fpA"},
        )
        self.assertNotEqual(
            a["summary"]["accession_list_sha256"],
            b["summary"]["accession_list_sha256"],
        )

    def test_writer_emits_json_and_report_and_no_fetch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shard_dir = root / "shards"
            shard_dir.mkdir()
            (shard_dir / "part-0.json").write_text(json.dumps(_bronze()), encoding="utf-8")
            atlas = root / "atlas.json"
            atlas.write_text(
                json.dumps(
                    {
                        "artifact_id": "atlas",
                        "rows": {
                            "train_in_scope_targets": [
                                {"accession": "T1", "true_fingerprint_id": "fpA"},
                                {"accession": "T2", "true_fingerprint_id": "fpB"},
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            labels = root / "labels.json"
            labels.write_text(
                json.dumps({"artifact_id": "labels", "rows": [{"sequence_id": "M1"}]}),
                encoding="utf-8",
            )
            coords = root / "x_coordinates"
            coords.mkdir()
            (coords / "afdb_S1_v6.cif").write_text("data\n", encoding="utf-8")
            out = root / "manifest.json"
            report = root / "manifest.md"
            manifest = write_offmcsa_recovery_download_manifest(
                bronze_shard_glob=str(shard_dir / "*.json"),
                atlas_manifest_path=atlas,
                label_manifest_path=labels,
                coordinate_glob=str(root / "*coordinates*"),
                out_path=out,
                report_path=report,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            # Q1, Q5 selected; M1 excluded (mcsa), S1 excluded (structured)
            self.assertEqual(manifest["summary"]["selected_structures_to_download"], 2)
            self.assertIn("Fetch Procedure", report.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
