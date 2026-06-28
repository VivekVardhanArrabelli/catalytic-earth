from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.offmcsa_recovery_feasibility import (
    build_offmcsa_recovery_feasibility,
    mcsa_accessions,
    scan_structured_surfaces,
    write_offmcsa_recovery_feasibility,
)


def _surface(name: str, non_mcsa: list[str], extra: int = 0) -> dict:
    return {
        "surface": name,
        "structures": len(non_mcsa) + extra,
        "distinct_accessions": len(non_mcsa) + extra,
        "non_mcsa_accessions": len(non_mcsa),
        "non_mcsa_accession_ids": sorted(non_mcsa),
    }


class OffMcsaRecoveryFeasibilityTests(unittest.TestCase):
    def test_blocked_when_no_labeled_nonmcsa_positive_with_structure(self) -> None:
        audit = build_offmcsa_recovery_feasibility(
            structured_surfaces=[_surface("ext", ["Q11111", "Q22222"], extra=200)],
            labeled_nonmcsa_positive_accessions=set(),
        )
        self.assertEqual(
            audit["status"],
            "blocked_offmcsa_recovery_no_local_labeled_nonmcsa_positive_structures",
        )
        self.assertEqual(
            audit["inventory"]["distinct_non_mcsa_structured_accessions"], 2
        )
        self.assertEqual(
            audit["inventory"]["usable_labeled_nonmcsa_positives_with_structure"], 0
        )

    def test_runnable_when_labeled_positive_has_structure(self) -> None:
        audit = build_offmcsa_recovery_feasibility(
            structured_surfaces=[_surface("ext", ["Q11111", "Q22222"])],
            labeled_nonmcsa_positive_accessions={"Q22222"},
        )
        self.assertEqual(
            audit["status"],
            "offmcsa_recovery_test_runnable_local_positive_surface_present",
        )
        self.assertEqual(audit["inventory"]["usable_accession_ids"], ["Q22222"])

    def test_mcsa_accessions_and_surface_scan_classify_non_mcsa(self) -> None:
        manifest = {
            "rows": [
                {"sequence_id": "P00001", "real_sequence_accessions": ["P00001"]},
                {"sequence_id": "P00002", "real_sequence_accessions": ["P00002", "P00003"]},
            ]
        }
        mcsa = mcsa_accessions(manifest)
        self.assertEqual(mcsa, {"P00001", "P00002", "P00003"})
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "coords"
            d.mkdir()
            # one M-CSA structure, one non-M-CSA
            (d / "afdb_P00001_v6.cif").write_text("data\n", encoding="utf-8")
            (d / "AF-Q99999-F1-model_v6.cif").write_text("data\n", encoding="utf-8")
            surfaces = scan_structured_surfaces([str(d)], mcsa)
        self.assertEqual(len(surfaces), 1)
        self.assertEqual(surfaces[0]["distinct_accessions"], 2)
        self.assertEqual(surfaces[0]["non_mcsa_accession_ids"], ["Q99999"])

    def test_writer_emits_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "labels.json"
            coords = root / "alpha_coordinates"
            coords.mkdir()
            (coords / "afdb_P00001_v6.cif").write_text("data\n", encoding="utf-8")
            (coords / "AF-Q99999-F1-model_v6.cif").write_text("data\n", encoding="utf-8")
            manifest.write_text(
                json.dumps(
                    {
                        "artifact_id": "labels",
                        "rows": [
                            {"sequence_id": "P00001", "real_sequence_accessions": ["P00001"]}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            out = root / "audit.json"
            report = root / "audit.md"
            audit = write_offmcsa_recovery_feasibility(
                label_manifest_path=manifest,
                coordinate_glob=str(root / "*coordinates*"),
                external_abstention_readout_path=None,
                out_path=out,
                report_path=report,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(
                json.loads(out.read_text())["artifact_id"], audit["artifact_id"]
            )
            self.assertEqual(
                audit["inventory"]["distinct_non_mcsa_structured_accessions"], 1
            )
            self.assertIn("Unblock Plan", report.read_text(encoding="utf-8"))
            self.assertIn("source_artifacts", audit)


if __name__ == "__main__":
    unittest.main()
