from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.option_b_heldout_preregistration import (
    build_option_b_heldout_preregistration,
    select_untouched_heldout_positives,
    write_option_b_heldout_preregistration,
)


def _bronze():
    return [
        # untouched metal positive -> selected
        {"entry_id": "uniprot:Q1", "fingerprint_id": "metal_dependent_hydrolase",
         "confidence": "high", "label_type": "seed_fingerprint"},
        # untouched non-metal positive -> selected
        {"entry_id": "uniprot:Q2", "fingerprint_id": "flavin_dehydrogenase_reductase",
         "confidence": "high", "label_type": "seed_fingerprint"},
        # used in development -> excluded
        {"entry_id": "uniprot:U1", "fingerprint_id": "flavin_dehydrogenase_reductase",
         "confidence": "high", "label_type": "seed_fingerprint"},
        # M-CSA accession -> excluded
        {"entry_id": "uniprot:M1", "fingerprint_id": "metal_dependent_hydrolase",
         "confidence": "high", "label_type": "seed_fingerprint"},
        # medium confidence -> excluded
        {"entry_id": "uniprot:Q3", "fingerprint_id": "metal_dependent_hydrolase",
         "confidence": "medium", "label_type": "seed_fingerprint"},
        # not an atlas family -> excluded
        {"entry_id": "uniprot:Q4", "fingerprint_id": "fpZ",
         "confidence": "high", "label_type": "seed_fingerprint"},
    ]


_FAMILIES = {"metal_dependent_hydrolase", "flavin_dehydrogenase_reductase"}


class OptionBHeldoutPreregistrationTests(unittest.TestCase):
    def test_selection_excludes_used_mcsa_and_low_confidence(self) -> None:
        members = select_untouched_heldout_positives(
            bronze_rows=_bronze(), families=_FAMILIES, mcsa={"M1"}, used_accessions={"U1"}
        )
        accs = [m["accession"] for m in members]
        self.assertEqual(accs, ["Q1", "Q2"])

    def test_metal_vs_nonmetal_classification(self) -> None:
        members = select_untouched_heldout_positives(
            bronze_rows=_bronze(), families=_FAMILIES, mcsa={"M1"}, used_accessions={"U1"}
        )
        by = {m["accession"]: m["metal_family"] for m in members}
        self.assertTrue(by["Q1"])   # metal_dependent_hydrolase
        self.assertFalse(by["Q2"])  # flavin -> non-metal

    def test_prereg_freezes_set_bar_and_is_not_run(self) -> None:
        members = select_untouched_heldout_positives(
            bronze_rows=_bronze(), families=_FAMILIES, mcsa={"M1"}, used_accessions={"U1"}
        )
        prereg = build_option_b_heldout_preregistration(members=members)
        self.assertEqual(
            prereg["status"], "preregistered_not_yet_run_pending_router_fix"
        )
        self.assertFalse(prereg["guardrails"]["heldout_rows_scored"])
        self.assertTrue(prereg["guardrails"]["labels_are_bronze_not_gold"])
        self.assertEqual(prereg["pass_bar"]["min_recovery_rate"], 0.70)
        self.assertEqual(
            prereg["pass_bar"]["max_nonmetal_into_metal_misroute_rate"], 0.20
        )
        self.assertEqual(prereg["frozen_heldout_set"]["counts"]["total"], 2)
        self.assertEqual(prereg["frozen_heldout_set"]["counts"]["non_metal_family"], 1)

    def test_hash_is_deterministic_and_content_sensitive(self) -> None:
        a = build_option_b_heldout_preregistration(
            members=select_untouched_heldout_positives(
                bronze_rows=_bronze(), families=_FAMILIES, mcsa={"M1"}, used_accessions={"U1"}
            )
        )
        b = build_option_b_heldout_preregistration(
            members=select_untouched_heldout_positives(
                bronze_rows=_bronze(), families=_FAMILIES, mcsa={"M1"}, used_accessions={"U1"}
            )
        )
        c = build_option_b_heldout_preregistration(
            members=select_untouched_heldout_positives(
                bronze_rows=_bronze(), families=_FAMILIES, mcsa={"M1"},
                used_accessions={"U1", "Q1"},
            )
        )
        self.assertEqual(a["frozen_heldout_set"]["sha256"], b["frozen_heldout_set"]["sha256"])
        self.assertNotEqual(a["frozen_heldout_set"]["sha256"], c["frozen_heldout_set"]["sha256"])

    def test_writer_emits_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shard_dir = root / "shards"
            shard_dir.mkdir()
            (shard_dir / "p.json").write_text(json.dumps(_bronze()), encoding="utf-8")
            atlas = root / "atlas.json"
            atlas.write_text(
                json.dumps({"rows": {"train_in_scope_targets": [
                    {"true_fingerprint_id": "metal_dependent_hydrolase"},
                    {"true_fingerprint_id": "flavin_dehydrogenase_reductase"},
                ]}}), encoding="utf-8")
            labels = root / "labels.json"
            labels.write_text(json.dumps({"rows": [{"sequence_id": "M1"}]}), encoding="utf-8")
            usedmap = root / "map.json"
            usedmap.write_text(json.dumps({"rows": [{"accession": "U1"}]}), encoding="utf-8")
            useddl = root / "dl.json"
            useddl.write_text(json.dumps({"downloads": []}), encoding="utf-8")
            out = root / "prereg.json"
            report = root / "prereg.md"
            prereg = write_option_b_heldout_preregistration(
                bronze_shard_glob=str(shard_dir / "*.json"),
                atlas_manifest_path=atlas,
                label_manifest_path=labels,
                recovery_positive_map_path=usedmap,
                recovery_download_manifest_path=useddl,
                out_path=out,
                report_path=report,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(prereg["frozen_heldout_set"]["counts"]["total"], 2)
            self.assertIn("One-Shot Guardrail", report.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
