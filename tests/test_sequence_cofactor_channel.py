from __future__ import annotations

import unittest

from catalytic_earth.sequence_cofactor_channel import (
    _sequence_supported_suppression_rows,
    build_sequence_cofactor_channel,
)


class SequenceCofactorChannelTests(unittest.TestCase):
    def test_builds_clean_label_set_and_dense_head_predictions(self) -> None:
        label_manifest = {
            "rows": [
                {"entry_id": "m_csa:1", "split_assignment": "in_distribution"},
                {"entry_id": "m_csa:2", "split_assignment": "in_distribution"},
                {"entry_id": "m_csa:3", "split_assignment": "heldout"},
                {"entry_id": "m_csa:4", "split_assignment": "heldout"},
            ]
        }
        geometry = {
            "entries": [
                {
                    "entry_id": "m_csa:1",
                    "status": "ok",
                    "ligand_context": {"cofactor_families": ["metal_ion"]},
                },
                {
                    "entry_id": "m_csa:2",
                    "status": "ok",
                    "ligand_context": {"cofactor_families": []},
                },
                {
                    "entry_id": "m_csa:3",
                    "status": "ok",
                    "ligand_context": {"cofactor_families": ["metal_ion"]},
                },
                {
                    "entry_id": "m_csa:4",
                    "status": "ok",
                    "ligand_context": {"cofactor_families": []},
                },
            ]
        }
        sidecar = [
            {"entry_id": "m_csa:1", "raw_embedding": [1.0, 0.0]},
            {"entry_id": "m_csa:2", "raw_embedding": [0.0, 1.0]},
            {"entry_id": "m_csa:3", "raw_embedding": [0.9, 0.1]},
            {"entry_id": "m_csa:4", "raw_embedding": [0.1, 0.9]},
        ]

        audit = build_sequence_cofactor_channel(
            label_manifest=label_manifest,
            geometry_features=geometry,
            sequence_manifest={"rows": []},
            fasta_text="",
            embedding_sidecars={"toy": sidecar},
            embedding_sidecar_summaries={},
        )

        self.assertEqual(audit["label_set"]["row_count"], 4)
        self.assertEqual(
            audit["label_set"]["class_presence_counts_by_split"]["heldout"]["metal_ion"],
            1,
        )
        self.assertEqual(
            audit["trained_sequence_heads"]["toy"]["class_results"]["metal_ion"][
                "status"
            ],
            "complete",
        )
        self.assertEqual(len(audit["channel_predictions"]), 4)

    def test_sequence_supported_suppression_abstains_unsupported_cofactor_call(self) -> None:
        rows = [
            {
                "entry_id": "m_csa:1",
                "called_fingerprint_id": "metal_dependent_hydrolase",
                "true_fingerprint_id": None,
                "abstained": False,
                "exact_label_match": False,
            },
            {
                "entry_id": "m_csa:2",
                "called_fingerprint_id": "heme_peroxidase_oxidase",
                "true_fingerprint_id": "heme_peroxidase_oxidase",
                "abstained": False,
                "exact_label_match": True,
            },
        ]
        channel = {
            "channel_predictions": [
                {"entry_id": "m_csa:1", "predicted_cofactor_families": []},
                {"entry_id": "m_csa:2", "predicted_cofactor_families": ["heme"]},
            ]
        }

        suppressed = _sequence_supported_suppression_rows(
            rows=rows,
            cofactor_channel=channel,
        )

        self.assertTrue(suppressed[0]["abstained"])
        self.assertIsNone(suppressed[0]["called_fingerprint_id"])
        self.assertFalse(suppressed[1]["abstained"])
        self.assertEqual(suppressed[1]["called_fingerprint_id"], "heme_peroxidase_oxidase")


if __name__ == "__main__":
    unittest.main()
