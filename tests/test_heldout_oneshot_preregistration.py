from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.heldout_oneshot_preregistration import (
    build_frozen_heldout_set,
    build_heldout_oneshot_preregistration,
    write_heldout_oneshot_preregistration,
)


def _split() -> dict:
    return {"split_records": [{"entry_id": "m_csa:1"}, {"entry_id": "m_csa:2"}]}


def _labels() -> dict:
    return {
        "artifact_id": "labels",
        "rows": [
            {"entry_id": "m_csa:1", "sequence_id": "P1", "true_fingerprint_id": "fpA"},
            {"entry_id": "m_csa:2", "sequence_id": "P2", "true_fingerprint_id": "fpB"},
            # held-out in-scope (with structure P3)
            {"entry_id": "m_csa:3", "sequence_id": "P3", "true_fingerprint_id": "fpA"},
            # held-out OOS (with structure P4)
            {"entry_id": "m_csa:4", "sequence_id": "P4", "true_fingerprint_id": None},
            # held-out but NO structure -> excluded
            {"entry_id": "m_csa:5", "sequence_id": "P5", "true_fingerprint_id": "fpC"},
        ],
    }


class HeldoutOneshotPreregistrationTests(unittest.TestCase):
    def test_frozen_set_excludes_train_cal_and_unstructured(self) -> None:
        frozen = build_frozen_heldout_set(
            split_manifest=_split(),
            label_manifest=_labels(),
            heldout_structure_accessions={"P3", "P4"},
        )
        ids = [m["entry_id"] for m in frozen["members"]]
        self.assertEqual(ids, ["m_csa:3", "m_csa:4"])  # m_csa:5 dropped (no structure)
        self.assertEqual(frozen["counts"], {"total": 2, "inscope": 1, "oos": 1})

    def test_frozen_set_hash_is_deterministic_and_content_sensitive(self) -> None:
        a = build_frozen_heldout_set(
            split_manifest=_split(),
            label_manifest=_labels(),
            heldout_structure_accessions={"P3", "P4"},
        )
        b = build_frozen_heldout_set(
            split_manifest=_split(),
            label_manifest=_labels(),
            heldout_structure_accessions={"P3", "P4"},
        )
        self.assertEqual(a["sha256"], b["sha256"])
        # dropping a member changes the hash (cannot be silently trimmed)
        c = build_frozen_heldout_set(
            split_manifest=_split(),
            label_manifest=_labels(),
            heldout_structure_accessions={"P3"},
        )
        self.assertNotEqual(a["sha256"], c["sha256"])

    def test_preregistration_locks_rule_bar_and_is_not_run(self) -> None:
        frozen = build_frozen_heldout_set(
            split_manifest=_split(),
            label_manifest=_labels(),
            heldout_structure_accessions={"P3", "P4"},
        )
        prereg = build_heldout_oneshot_preregistration(
            frozen_heldout_set=frozen,
            heldout_coordinate_dirs=("dir_a", "dir_b"),
            split_manifest_summary={"path": "s"},
            label_manifest_summary={"path": "l"},
        )
        self.assertEqual(prereg["status"], "preregistered_not_yet_run")
        self.assertFalse(prereg["guardrails"]["heldout_rows_scored"])
        self.assertFalse(prereg["guardrails"]["success_bar_derived_from_heldout"])
        self.assertTrue(prereg["guardrails"]["success_bar_derived_from_calibration_only"])
        self.assertEqual(prereg["frozen_rule"]["cofactor_threshold"], 0.44)
        self.assertIn("0.70", prereg["success_bar"]["primary_pass_criteria"])
        self.assertIn("0.40", prereg["success_bar"]["primary_pass_criteria"])
        self.assertEqual(
            prereg["frozen_heldout_set"]["sha256"], frozen["sha256"]
        )

    def test_writer_emits_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            split = root / "split.json"
            labels = root / "labels.json"
            coords = root / "queries_all_heldout"
            coords.mkdir()
            (coords / "afdb_P3_v6.cif").write_text("data\n", encoding="utf-8")
            (coords / "afdb_P4_v6.cif").write_text("data\n", encoding="utf-8")
            split.write_text(json.dumps(_split()), encoding="utf-8")
            labels.write_text(json.dumps(_labels()), encoding="utf-8")
            out = root / "prereg.json"
            report = root / "prereg.md"
            prereg = write_heldout_oneshot_preregistration(
                split_manifest_path=split,
                label_manifest_path=labels,
                heldout_coordinate_dirs=(str(coords),),
                out_path=out,
                report_path=report,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(prereg["frozen_heldout_set"]["counts"]["total"], 2)
            self.assertIn("One-Shot Guardrail", report.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
