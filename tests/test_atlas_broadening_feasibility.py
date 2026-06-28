from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.atlas_broadening_feasibility import (
    build_atlas_broadening_feasibility,
    curated_label_family_count,
    current_atlas_families,
    label_manifest_fine_fingerprint_rows,
    write_atlas_broadening_feasibility,
)


def _atlas_manifest() -> dict:
    return {
        "rows": {
            "train_in_scope_targets": [
                {"accession": "P1", "true_fingerprint_id": "fpA"},
                {"accession": "P2", "true_fingerprint_id": "fpB"},
                {"accession": "P3", "true_fingerprint_id": "fpA"},
            ]
        }
    }


class AtlasBroadeningFeasibilityTests(unittest.TestCase):
    def test_helpers(self) -> None:
        ca = current_atlas_families(_atlas_manifest())
        self.assertEqual(ca["family_count"], 2)
        self.assertEqual(ca["structures"], 3)
        self.assertEqual(
            label_manifest_fine_fingerprint_rows(
                {"rows": [{"true_fingerprint_id": "x"}, {"true_fingerprint_id": None}]}
            ),
            1,
        )
        self.assertEqual(
            curated_label_family_count(
                [{"fingerprint_id": "a"}, {"fingerprint_id": "a"}, {"fingerprint_id": None}]
            ),
            1,
        )

    def test_blocked_when_no_fine_multifamily_source(self) -> None:
        audit = build_atlas_broadening_feasibility(
            current_atlas=current_atlas_families(_atlas_manifest()),
            label_manifest_fine_rows=0,
            curated_families=8,
        )
        self.assertEqual(
            audit["status"],
            "blocked_atlas_broadening_no_fine_multifamily_mcsa_label_source",
        )
        self.assertEqual(audit["blocker"]["families_unreachable_for_now"], 57 - 2)

    def test_runnable_when_fine_rows_present(self) -> None:
        audit = build_atlas_broadening_feasibility(
            current_atlas=current_atlas_families(_atlas_manifest()),
            label_manifest_fine_rows=120,
            curated_families=8,
        )
        self.assertEqual(
            audit["status"],
            "atlas_broadening_runnable_fine_multifamily_source_present",
        )

    def test_writer_emits_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            atlas = root / "atlas.json"
            labels = root / "labels.json"
            curated = root / "curated.json"
            atlas.write_text(json.dumps(_atlas_manifest()), encoding="utf-8")
            labels.write_text(json.dumps({"rows": [{"entry_id": "m_csa:1"}]}), encoding="utf-8")
            curated.write_text(
                json.dumps([{"fingerprint_id": "a"}, {"fingerprint_id": "b"}]),
                encoding="utf-8",
            )
            out = root / "audit.json"
            report = root / "audit.md"
            audit = write_atlas_broadening_feasibility(
                atlas_manifest_path=atlas,
                label_manifest_path=labels,
                curated_labels_path=curated,
                out_path=out,
                report_path=report,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(
                audit["status"],
                "blocked_atlas_broadening_no_fine_multifamily_mcsa_label_source",
            )
            self.assertIn("Unblock Plan", report.read_text(encoding="utf-8"))
            self.assertIn("source_artifacts", audit)


if __name__ == "__main__":
    unittest.main()
