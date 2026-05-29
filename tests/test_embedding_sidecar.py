from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.embedding_sidecar import build_sequence_embedding_sidecar


class EmbeddingSidecarTests(unittest.TestCase):
    def test_sidecar_retains_raw_vectors_without_label_fields(self) -> None:
        manifest = {
            "metadata": {"method": "test_sequence_manifest"},
            "rows": [
                {
                    "entry_id": "m_csa:1",
                    "entry_name": "not retained",
                    "label_type": "seed_fingerprint",
                    "target_fingerprint_id": "not retained",
                    "split_assignment": "heldout",
                    "sequence_records": [
                        {
                            "accession_or_structure_id": "P11111",
                            "sequence_sha256": "sha",
                        }
                    ],
                }
            ],
        }
        fasta = ">sp|P11111|TEST\nACDEFGHIK\n"

        sidecar = build_sequence_embedding_sidecar(
            sequence_manifest=manifest,
            fasta_text=fasta,
            embedding_backend="deterministic_sequence_kmer_control",
        )

        self.assertEqual(sidecar["summary"]["status"], "complete")
        self.assertTrue(sidecar["summary"]["raw_embedding_vectors_retained"])
        self.assertFalse(sidecar["summary"]["label_fields_retained"])
        record = sidecar["records"][0]
        self.assertEqual(record["entry_id"], "m_csa:1")
        self.assertIn("raw_embedding", record)
        self.assertNotIn("label_type", record)
        self.assertNotIn("target_fingerprint_id", record)
        self.assertNotIn("entry_name", record)


if __name__ == "__main__":
    unittest.main()
