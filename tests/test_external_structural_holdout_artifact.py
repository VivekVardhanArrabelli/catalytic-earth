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

    def test_external_structural_cluster_index_records_nearest_neighbor_cache(self) -> None:
        artifact = _load_json(
            ROOT / "artifacts" / "v3_external_structural_cluster_index_1025.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "external_structural_cluster_index")
        self.assertEqual(metadata["candidate_count"], 10)
        self.assertEqual(metadata["coordinate_materialized_count"], 10)
        self.assertEqual(metadata["fetch_failure_count"], 0)
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertTrue(metadata["nearest_neighbor_cache_complete"])
        self.assertEqual(metadata["nearest_neighbor_cache_candidate_count"], 10)
        self.assertEqual(metadata["nearest_neighbor_cache_candidate_coverage"], 1.0)
        self.assertTrue(metadata["structure_cluster_before_split_assignment"])
        self.assertFalse(metadata["tm_score_split_claim_permitted"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertGreaterEqual(metadata["high_tm_pair_count"], 1)
        self.assertLess(metadata["tm_cluster_count"], metadata["candidate_count"])

        cluster_by_accession = {
            accession: cluster["cluster_id"]
            for cluster in artifact["clusters"]
            for accession in cluster["accessions"]
        }
        self.assertEqual(
            cluster_by_accession["O95050"],
            cluster_by_accession["P51580"],
        )
        self.assertTrue(
            all(not row["ready_for_label_import"] for row in artifact["rows"])
        )

    def test_current_guidance_does_not_resume_mcsa_strict_tm_repair(self) -> None:
        handoff = (ROOT / "work" / "handoff.md").read_text(encoding="utf-8")
        current_handoff = handoff.split("## Current Handoff", 1)[1].split(
            "## Start-of-Run Confidence Call", 1
        )[0]
        self.assertIn("Do not open M-CSA round33", current_handoff)
        self.assertIn("external structural pilot", current_handoff)

        forbidden_active_guidance = [
            "Next start: retry or adjudicate staged index 145",
            "continue single-query verification",
            "continue from staged index",
            "active readiness artifact is",
            "resume M-CSA strict-TM round repair",
        ]
        guidance_texts = {
            ROOT / "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            ROOT / "docs" / "external_source_transfer.md": (
                ROOT / "docs" / "external_source_transfer.md"
            ).read_text(encoding="utf-8"),
            ROOT / "work" / "foldseek_readiness_notes.md": (
                ROOT / "work" / "foldseek_readiness_notes.md"
            ).read_text(encoding="utf-8"),
            ROOT / "work" / "handoff.md": current_handoff,
            ROOT / "work" / "scope.md": (ROOT / "work" / "scope.md").read_text(
                encoding="utf-8"
            ),
        }
        for path, text in guidance_texts.items():
            for phrase in forbidden_active_guidance:
                self.assertNotIn(phrase, text, f"{phrase!r} remains in {path}")


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
