import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ExternalStructuralHoldoutArtifactTests(unittest.TestCase):
    def test_external_structural_tm_holdout_path_requires_pre_split_clustering(self) -> None:
        artifact = _load_json(
            ROOT / "artifacts" / "v3_external_structural_tm_holdout_path_1025.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "external_structural_tm_holdout_path")
        self.assertEqual(metadata["candidate_count"], 10)
        self.assertEqual(metadata["structure_reference_candidate_count"], 10)
        self.assertTrue(metadata["structure_cluster_before_split_assignment"])
        self.assertTrue(metadata["nearest_neighbor_cache_required"])
        self.assertTrue(metadata["foldseek_or_tmalign_backend_required"])
        self.assertFalse(metadata["tm_score_split_claim_permitted"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertTrue(
            all(row["alphafold_ids"] for row in artifact["rows"])
        )
        self.assertEqual(
            sum(1 for row in artifact["rows"] if row["pdb_reference_count"] > 0),
            7,
        )


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
