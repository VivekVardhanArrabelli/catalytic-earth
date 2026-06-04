from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from catalytic_earth.predicted_geometry_recovery import (
    _default_context_fusion,
    _default_unsupported_suppression,
    _per_entry_transitions,
    _readouts_by_split,
    staged_cif_fetcher,
)


def _router_row(entry_id, *, correct, abstained=False, called="fp", true="fp"):
    return {
        "entry_id": entry_id,
        "true_fingerprint_id": true,
        "called_fingerprint_id": None if abstained else called,
        "top1_fingerprint_id": called,
        "top1_score": 0.5,
        "abstained": abstained,
        "exact_label_match": bool(correct),
    }


class StagedCifFetcherTests(unittest.TestCase):
    def test_reads_present_cif_and_raises_on_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            staged = Path(tmp)
            (staged / "afdb_P12345_v6.cif").write_text("data_X\n", encoding="utf-8")
            fetch = staged_cif_fetcher(staged)
            text, meta = fetch("P12345")
            self.assertEqual(text, "data_X\n")
            self.assertEqual(meta["backend"], "staged_local_alphafold")
            self.assertEqual(meta["accession"], "P12345")
            with self.assertRaises(RuntimeError):
                fetch("Q99999")


class RecoveryReadoutTests(unittest.TestCase):
    def test_transitions_and_readouts(self) -> None:
        # A: apo lost then recovered; B: never lost; C: apo lost not recovered;
        # D (train): apo correct but fusion regresses it.
        exp = [
            _router_row("m_csa:1", correct=True),
            _router_row("m_csa:2", correct=True),
            _router_row("m_csa:3", correct=True),
            _router_row("m_csa:4", correct=True),
        ]
        apo = [
            _router_row("m_csa:1", correct=False, abstained=True),
            _router_row("m_csa:2", correct=True),
            _router_row("m_csa:3", correct=False, abstained=True),
            _router_row("m_csa:4", correct=True),
        ]
        fused = [
            _router_row("m_csa:1", correct=True),
            _router_row("m_csa:2", correct=True),
            _router_row("m_csa:3", correct=False, abstained=True),
            _router_row("m_csa:4", correct=False),
        ]
        suppressed = fused  # not exercised in this assertion set
        split_by_entry = {
            "m_csa:1": "calibration",
            "m_csa:2": "calibration",
            "m_csa:3": "calibration",
            "m_csa:4": "train",
        }
        per_entry = _per_entry_transitions(
            exp_rows=exp,
            apo_rows=apo,
            fused_rows=fused,
            suppressed_rows=suppressed,
            split_by_entry=split_by_entry,
        )
        by_id = {row["entry_id"]: row for row in per_entry}
        self.assertTrue(by_id["m_csa:1"]["apo_lost_primary"])
        self.assertTrue(by_id["m_csa:1"]["fused_recovered"])
        self.assertFalse(by_id["m_csa:2"]["apo_lost_primary"])
        self.assertTrue(by_id["m_csa:3"]["apo_lost_primary"])
        self.assertFalse(by_id["m_csa:3"]["fused_recovered"])
        self.assertTrue(by_id["m_csa:4"]["fused_regressed"])

        readouts = _readouts_by_split(per_entry)
        cal = readouts["calibration"]
        self.assertEqual(cal["row_count"], 3)
        self.assertEqual(cal["experimental_correct"], 3)
        self.assertEqual(cal["apo_correct"], 1)
        self.assertEqual(cal["fused_correct"], 2)
        self.assertEqual(cal["apo_lost_primary_rows"], 2)
        self.assertEqual(cal["fused_recovered_rows"], 1)
        self.assertEqual(cal["fused_regressed_rows"], 0)
        self.assertTrue(cal["is_out_of_sample_for_cofactor_channel"])
        self.assertEqual(cal["recovery_fraction_of_apo_loss"], 0.5)

        train = readouts["train"]
        self.assertFalse(train["is_out_of_sample_for_cofactor_channel"])
        self.assertEqual(train["fused_regressed_rows"], 1)


class ContextAdapterTests(unittest.TestCase):
    def test_default_cofactor_adapters_are_the_pluggable_seam(self) -> None:
        predicted_geometry = {
            "entries": [{"entry_id": "m_csa:1", "status": "ok", "ligand_context": {}}],
            "metadata": {},
        }
        channel = {
            "channel_predictions": [
                {
                    "entry_id": "m_csa:1",
                    "predicted_cofactor_families": ["metal_ion"],
                    "prediction_sources": {},
                    "scores": {},
                }
            ]
        }
        fused = _default_context_fusion(predicted_geometry, channel)
        injected = fused["entries"][0]["ligand_context"]["cofactor_families"]
        self.assertIn("metal_ion", injected)

        # The suppression adapter abstains a metal-requiring call when the channel
        # supports no cofactor family for that row.
        rows = [
            {
                "entry_id": "m_csa:9",
                "called_fingerprint_id": "metal_dependent_hydrolase",
                "true_fingerprint_id": "metal_dependent_hydrolase",
                "abstained": False,
            }
        ]
        empty_channel = {
            "channel_predictions": [
                {"entry_id": "m_csa:9", "predicted_cofactor_families": []}
            ]
        }
        suppressed = _default_unsupported_suppression(rows, empty_channel)
        self.assertTrue(suppressed[0]["abstained"])


if __name__ == "__main__":
    unittest.main()
