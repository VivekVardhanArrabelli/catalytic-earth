import json
import unittest
from pathlib import Path

from catalytic_earth.generalization import build_sequence_distance_holdout_eval
from catalytic_earth.labels import MechanismLabel


ROOT = Path(__file__).resolve().parents[1]


class SequenceDistanceHoldoutTests(unittest.TestCase):
    def test_proxy_holdout_reports_partition_metrics(self) -> None:
        labels = [
            MechanismLabel("m_csa:1", "fp_a", "seed_fingerprint", "medium", "a"),
            MechanismLabel("m_csa:2", "fp_a", "seed_fingerprint", "medium", "a"),
            MechanismLabel("m_csa:3", "fp_b", "seed_fingerprint", "medium", "b"),
            MechanismLabel("m_csa:4", None, "out_of_scope", "medium", "out"),
            MechanismLabel("m_csa:5", None, "out_of_scope", "medium", "out"),
            MechanismLabel("m_csa:6", None, "out_of_scope", "medium", "out"),
        ]
        retrieval = {
            "results": [
                _result("m_csa:1", "fp_a", 0.8),
                _result("m_csa:2", "fp_b", 0.7, second="fp_a"),
                _result("m_csa:3", "fp_b", 0.2),
                _result("m_csa:4", "fp_a", 0.1),
                _result("m_csa:5", "fp_a", 0.9),
                _result("m_csa:6", "fp_b", 0.1),
            ]
        }
        sequence_clusters = {
            "metadata": {
                "method": "sequence_cluster_proxy_from_reference_uniprot",
                "cluster_source": "reference_uniprot_exact_set",
            },
            "rows": [
                {
                    "entry_id": f"m_csa:{index}",
                    "sequence_cluster_id": f"uniprot:P{index}",
                    "reference_uniprot_ids": [f"P{index}"],
                }
                for index in range(1, 7)
            ],
            "clusters": [
                {
                    "sequence_cluster_id": f"uniprot:P{index}",
                    "entry_count": 1,
                    "entry_ids": [f"m_csa:{index}"],
                }
                for index in range(1, 7)
            ],
        }
        geometry = {
            "metadata": {"method": "geometry_features"},
            "entries": [
                {"entry_id": f"m_csa:{index}", "pdb_id": f"{index}ABC"}
                for index in range(1, 7)
            ],
        }

        artifact = build_sequence_distance_holdout_eval(
            retrieval=retrieval,
            labels=labels,
            sequence_clusters=sequence_clusters,
            geometry=geometry,
            slice_id="test",
            abstain_threshold=0.5,
            holdout_fraction=0.5,
            min_holdout_rows=2,
        )

        self.assertEqual(
            artifact["metadata"]["method"], "sequence_fold_distance_holdout_evaluation"
        )
        self.assertEqual(artifact["metadata"]["heldout_count"], 3)
        self.assertIn("heldout", artifact["metrics"])
        self.assertIn(
            "in_scope_by_target_fingerprint",
            artifact["per_fingerprint_breakdowns"]["heldout"],
        )
        self.assertTrue(
            all(row["distance_proxy_note"].startswith("proxy_only") for row in artifact["rows"])
        )
        self.assertEqual(
            artifact["metadata"]["proxy_pass_counts"]["heldout_low_similarity_proxy_pass"],
            3,
        )

    def test_current_1000_holdout_artifact_is_pinned(self) -> None:
        artifact = _load_artifact("artifacts/v3_sequence_distance_holdout_eval_1000.json")
        self.assertEqual(
            artifact["metadata"]["clustering_backend"],
            "deterministic_local_proxy_no_foldseek_mmseqs2_blast_or_diamond",
        )
        self.assertEqual(artifact["metadata"]["heldout_count"], 136)
        self.assertEqual(
            artifact["metrics"]["heldout"]["out_of_scope_false_non_abstentions"],
            0,
        )
        self.assertEqual(
            artifact["metrics"]["heldout"]["top1_accuracy_in_scope_evaluable"],
            0.9767,
        )
        self.assertEqual(
            artifact["metrics"]["heldout"][
                "top3_accuracy_among_retained_in_scope_evaluable"
            ],
            1.0,
        )

    def test_current_1025_holdout_artifact_is_pinned(self) -> None:
        artifact = _load_artifact("artifacts/v3_sequence_distance_holdout_eval_1025.json")
        self.assertEqual(artifact["metadata"]["evaluated_count"], 678)
        self.assertEqual(artifact["metadata"]["heldout_count"], 136)
        self.assertEqual(
            artifact["metrics"]["heldout"]["out_of_scope_false_non_abstentions_evaluable"],
            0,
        )
        self.assertEqual(
            artifact["metadata"]["proxy_pass_counts"]["heldout_low_similarity_proxy_pass"],
            135,
        )


def _result(
    entry_id: str,
    top1: str,
    score: float,
    *,
    second: str | None = None,
) -> dict[str, object]:
    top_fingerprints = [{"fingerprint_id": top1, "score": score}]
    if second:
        top_fingerprints.append({"fingerprint_id": second, "score": max(score - 0.1, 0.0)})
    return {
        "entry_id": entry_id,
        "entry_name": entry_id,
        "pdb_id": entry_id.replace("m_csa:", "") + "XYZ",
        "resolved_residue_count": 3,
        "residue_codes": ["SER", "HIS", "ASP"],
        "status": "ok",
        "top_fingerprints": top_fingerprints,
    }


def _load_artifact(path: str) -> dict[str, object]:
    with (ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
