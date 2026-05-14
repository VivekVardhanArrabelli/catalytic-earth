import json
import shutil
import tempfile
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
        self.assertFalse(artifact["metadata"]["real_sequence_identity_computed"])
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

    @unittest.skipUnless(shutil.which("mmseqs"), "MMseqs2 is required for real clustering")
    def test_mmseqs_holdout_clusters_whole_sequence_units(self) -> None:
        labels = [
            MechanismLabel("m_csa:1", "fp_a", "seed_fingerprint", "medium", "a"),
            MechanismLabel("m_csa:2", "fp_a", "seed_fingerprint", "medium", "a"),
            MechanismLabel("m_csa:3", "fp_b", "seed_fingerprint", "medium", "b"),
            MechanismLabel("m_csa:4", None, "out_of_scope", "medium", "out"),
        ]
        retrieval = {
            "results": [
                _result("m_csa:1", "fp_a", 0.9),
                _result("m_csa:2", "fp_a", 0.9),
                _result("m_csa:3", "fp_b", 0.9),
                _result("m_csa:4", "fp_a", 0.1),
            ]
        }
        sequence_clusters = {
            "rows": [
                {
                    "entry_id": f"m_csa:{index}",
                    "sequence_cluster_id": f"uniprot:P{index}",
                    "reference_uniprot_ids": [f"P{index}"],
                }
                for index in range(1, 5)
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            fasta = Path(tmpdir) / "seqs.fasta"
            seq_a = (
                "MKIGIFDSGVGGLTVLKAIRNRYRKVDIVYLGDTARVPYGIRSKDTIIRYSLECAGFLKD"
                "KGVDIIVVACNTASAYALERLKKEINVPVFGVIEPGVKEALKKSRNKKIGVIGTPATVKS"
            )
            seq_b = (
                "MVDKRESYTKEDLLASGRGELFGAKGPQLPAPNMLMMDRVVKMTETGGNFDKGYVEAELD"
                "INPDLWFFGCHFIGDPVMPGCLGLDAMWQLVGFYLGWLGGEGKGRALGVGEVKFTGQVLP"
            )
            seq_c = (
                "SAFDQAARSRGHSNRRTALRPRRQQEATEVRPEQKMPTLLRVYIDGPHGMGKTTTTQLLV"
                "ALGSRDDIVYVPEPMTYWRVLGASETIANIYTTQHRLDQGEISAGDAAVVMTSAQITMG"
            )
            fasta.write_text(
                "\n".join(
                    [
                        ">m_csa:1",
                        seq_a,
                        ">m_csa:2",
                        seq_a,
                        ">m_csa:3",
                        seq_b,
                        ">m_csa:4",
                        seq_c,
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            artifact = build_sequence_distance_holdout_eval(
                retrieval=retrieval,
                labels=labels,
                sequence_clusters=sequence_clusters,
                slice_id="mmseqs-test",
                abstain_threshold=0.5,
                holdout_fraction=0.25,
                min_holdout_rows=1,
                sequence_fasta=str(fasta),
                sequence_identity_backend="mmseqs",
                compute_max_train_test_identity=False,
            )

        rows_by_id = {row["entry_id"]: row for row in artifact["rows"]}
        self.assertTrue(artifact["metadata"]["real_sequence_identity_computed"])
        self.assertEqual(artifact["metadata"]["sequence_entry_coverage_count"], 4)
        self.assertEqual(artifact["metadata"]["sequence_missing_entry_count"], 0)
        self.assertEqual(
            rows_by_id["m_csa:1"]["real_sequence_identity_cluster_id"],
            rows_by_id["m_csa:2"]["real_sequence_identity_cluster_id"],
        )
        self.assertEqual(
            rows_by_id["m_csa:1"]["partition"],
            rows_by_id["m_csa:2"]["partition"],
        )

    def test_current_1000_holdout_artifact_is_pinned(self) -> None:
        artifact = _load_artifact("artifacts/v3_sequence_distance_holdout_eval_1000.json")
        self.assertEqual(
            artifact["metadata"]["clustering_backend"],
            "mmseqs2_cluster_sequence_identity",
        )
        self.assertTrue(artifact["metadata"]["real_sequence_identity_computed"])
        self.assertEqual(artifact["metadata"]["sequence_count"], 738)
        self.assertEqual(artifact["metadata"]["sequence_entry_coverage_count"], 678)
        self.assertEqual(artifact["metadata"]["sequence_missing_entry_count"], 0)
        self.assertEqual(
            artifact["metadata"]["real_sequence_identity_record_cluster_count"], 692
        )
        self.assertEqual(
            artifact["metadata"]["real_sequence_identity_entry_cluster_count"], 635
        )
        self.assertEqual(artifact["metadata"]["heldout_count"], 136)
        self.assertEqual(len(artifact["metadata"]["heldout_cluster_ids"]), 136)
        self.assertEqual(len(artifact["metadata"]["heldout_entry_ids"]), 136)
        self.assertEqual(
            artifact["metadata"]["max_observed_train_test_identity"], 0.284
        )
        self.assertTrue(artifact["metadata"]["sequence_identity_target_achieved"])
        self.assertEqual(
            artifact["metrics"]["heldout"]["out_of_scope_false_non_abstentions"],
            0,
        )
        self.assertEqual(
            artifact["metrics"]["heldout"]["top1_accuracy_in_scope_evaluable"],
            1.0,
        )
        self.assertEqual(
            artifact["metrics"]["heldout"][
                "top3_retained_accuracy_in_scope_evaluable"
            ],
            1.0,
        )
        self.assertEqual(
            artifact["metrics"]["heldout"]["retention_rate_in_scope_evaluable"], 1.0
        )
        self.assertEqual(
            artifact["metrics"]["in_distribution"]["retention_rate_in_scope_evaluable"],
            0.9821,
        )
        self.assertEqual(
            artifact["per_fingerprint_breakdowns"]["heldout"][
                "in_scope_by_target_fingerprint"
            ]["metal_dependent_hydrolase"]["evaluated_count"],
            13,
        )
        self.assertEqual(
            artifact["per_fingerprint_breakdowns"]["in_distribution"][
                "in_scope_by_target_fingerprint"
            ]["flavin_dehydrogenase_reductase"][
                "top1_accuracy_in_scope_evaluable"
            ],
            0.9744,
        )

    def test_current_1025_holdout_artifact_is_pinned(self) -> None:
        artifact = _load_artifact("artifacts/v3_sequence_distance_holdout_eval_1025.json")
        self.assertEqual(artifact["metadata"]["evaluated_count"], 678)
        self.assertTrue(artifact["metadata"]["real_sequence_identity_computed"])
        self.assertEqual(
            artifact["metadata"]["clustering_backend"],
            "mmseqs2_cluster_sequence_identity",
        )
        self.assertEqual(artifact["metadata"]["heldout_count"], 136)
        self.assertEqual(artifact["metadata"]["sequence_count"], 738)
        self.assertEqual(
            artifact["metadata"]["max_observed_train_test_identity"], 0.284
        )
        self.assertEqual(
            artifact["metrics"]["heldout"]["out_of_scope_false_non_abstentions_evaluable"],
            0,
        )
        self.assertEqual(
            artifact["metadata"]["proxy_pass_counts"]["heldout_low_similarity_proxy_pass"],
            135,
        )
        self.assertEqual(
            artifact["metrics"]["heldout"]["top3_retained_accuracy_in_scope_evaluable"],
            1.0,
        )
        self.assertEqual(
            artifact["metrics"]["in_distribution"]["abstention_rate_in_scope_evaluable"],
            0.0179,
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
