from __future__ import annotations

import unittest

from catalytic_earth.cofactor_channel_probe import build_sequence_cofactor_channel_probe


class CofactorChannelProbeTests(unittest.TestCase):
    def test_builds_presence_label_balance_and_kmer_probe(self) -> None:
        label_manifest = {
            "rows": [
                {
                    "entry_id": "m_csa:1",
                    "split_assignment": "in_distribution",
                    "fingerprint_id": None,
                    "sequence_id": "P1",
                },
                {
                    "entry_id": "m_csa:2",
                    "split_assignment": "in_distribution",
                    "fingerprint_id": None,
                    "sequence_id": "P2",
                },
                {
                    "entry_id": "m_csa:3",
                    "split_assignment": "heldout",
                    "fingerprint_id": None,
                    "sequence_id": "P3",
                },
                {
                    "entry_id": "m_csa:4",
                    "split_assignment": "heldout",
                    "fingerprint_id": None,
                    "sequence_id": "P4",
                },
            ]
        }
        geometry_features = {
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
        kmer_records = [
            {"entry_id": "m_csa:1", "raw_embedding": {"aa:H": 1.0}},
            {"entry_id": "m_csa:2", "raw_embedding": {"aa:A": 1.0}},
            {"entry_id": "m_csa:3", "raw_embedding": {"aa:H": 0.9}},
            {"entry_id": "m_csa:4", "raw_embedding": {"aa:A": 0.9}},
        ]

        audit = build_sequence_cofactor_channel_probe(
            label_manifest=label_manifest,
            geometry_features=geometry_features,
            kmer_sidecar_records=kmer_records,
            kmer_sidecar_summary={"status": "complete", "emitted_row_count": 4},
            min_train_positive=1,
            min_heldout_positive=1,
        )

        self.assertEqual(audit["status"], "complete")
        self.assertEqual(
            audit["label_balance"]["runnable_presence_classes"], ["metal_ion"]
        )
        self.assertEqual(
            audit["answer"]["core_presence_support_train_heldout"]["metal_ion"],
            {"train": 1, "heldout": 1},
        )
        probe = audit["sequence_probe"]["kmer_logistic_presence_probe"]
        self.assertEqual(probe["status"], "complete")
        self.assertIn("metal_ion", probe["class_results"])


if __name__ == "__main__":
    unittest.main()
