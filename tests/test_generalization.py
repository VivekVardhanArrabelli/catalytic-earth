import json
import shutil
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.generalization import (
    aggregate_foldseek_tm_score_query_chunks,
    audit_foldseek_tm_score_split_repair,
    audit_foldseek_tm_score_target_failure,
    build_sequence_distance_holdout_split_repair_candidate,
    build_sequence_distance_holdout_split_redesign_candidate,
    build_foldseek_coordinate_readiness,
    build_foldseek_tm_score_all_materializable_signal,
    build_foldseek_tm_score_cluster_first_split,
    build_foldseek_tm_score_query_chunk_signal,
    build_foldseek_tm_score_signal,
    build_sequence_distance_holdout_eval,
    project_foldseek_tm_score_split_repair,
)
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
        self.assertTrue(
            artifact["metadata"]["backend"].startswith("deterministic_local_proxy_")
        )
        self.assertEqual(artifact["metadata"]["cluster_threshold"], 0.3)
        self.assertFalse(artifact["metadata"]["target_identity_achieved"])
        self.assertIn(
            "deterministic proxy partition is retained because real sequence identity was not computed",
            artifact["metadata"]["limitations"],
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
        self.assertEqual(
            artifact["metadata"]["backend"], "mmseqs2_cluster_sequence_identity"
        )
        self.assertEqual(
            artifact["metadata"]["backend_resolved_path"], shutil.which("mmseqs")
        )
        self.assertEqual(artifact["metadata"]["cluster_threshold"], 0.3)
        self.assertEqual(artifact["metadata"]["target_max_train_test_identity"], 0.3)
        self.assertTrue(artifact["metadata"]["target_identity_achieved"])
        self.assertEqual(
            artifact["metadata"]["limitations"],
            artifact["metadata"]["sequence_identity_limitations"],
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
        self.assertEqual(
            artifact["metadata"]["backend"], "mmseqs2_cluster_sequence_identity"
        )
        self.assertEqual(artifact["metadata"]["cluster_threshold"], 0.3)
        self.assertTrue(artifact["metadata"]["target_identity_achieved"])
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


class FoldseekCoordinateReadinessTests(unittest.TestCase):
    def test_explicit_foldseek_binary_path_is_recorded_when_not_on_path(self) -> None:
        labels = [
            MechanismLabel("m_csa:1", "fp_a", "seed_fingerprint", "medium", "a"),
        ]
        retrieval = {"results": [_result("m_csa:1", "fp_a", 0.8, pdb_id="1ABC")]}
        with tempfile.TemporaryDirectory() as tmpdir:
            foldseek = Path(tmpdir) / "foldseek"
            foldseek.write_text(
                "#!/bin/sh\nprintf '10.test-explicit\\n'\n",
                encoding="utf-8",
            )
            foldseek.chmod(0o755)
            artifact = build_foldseek_coordinate_readiness(
                retrieval=retrieval,
                labels=labels,
                slice_id="test",
                foldseek_binary=str(foldseek),
                coordinate_dir=str(Path(tmpdir) / "coords"),
                max_coordinate_files=0,
            )

        self.assertEqual(artifact["metadata"]["foldseek_binary_requested"], str(foldseek))
        self.assertEqual(artifact["metadata"]["foldseek_binary_resolved"], str(foldseek))
        self.assertTrue(artifact["metadata"]["foldseek_binary_available"])
        self.assertEqual(artifact["metadata"]["foldseek_version"], "10.test-explicit")
        self.assertIn(str(foldseek), artifact["metadata"]["foldseek_version_command"])
        self.assertFalse(artifact["metadata"]["tm_score_split_computed"])

    def test_coordinate_staging_is_bounded_and_deterministic(self) -> None:
        labels = [
            MechanismLabel("m_csa:1", "fp_a", "seed_fingerprint", "medium", "a"),
            MechanismLabel("m_csa:2", "fp_a", "seed_fingerprint", "medium", "a"),
            MechanismLabel("m_csa:3", "fp_b", "seed_fingerprint", "medium", "b"),
        ]
        retrieval = {
            "results": [
                _result("m_csa:1", "fp_a", 0.8, pdb_id="1AAA"),
                _result("m_csa:2", "fp_a", 0.8, pdb_id="2BBB"),
                _result("m_csa:3", "fp_b", 0.8, pdb_id="3CCC"),
            ]
        }
        fetched: list[str] = []

        def fake_fetch(pdb_id: str) -> str:
            fetched.append(pdb_id)
            return f"data_{pdb_id}\n#\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = build_foldseek_coordinate_readiness(
                retrieval=retrieval,
                labels=labels,
                slice_id="test",
                coordinate_dir=str(Path(tmpdir) / "coords"),
                max_coordinate_files=2,
                fetch_pdb_cif_fn=fake_fetch,
            )

        self.assertEqual(fetched, ["1AAA", "2BBB"])
        self.assertEqual(artifact["metadata"]["coordinate_fetch_cap"], 2)
        self.assertEqual(artifact["metadata"]["materialized_coordinate_count"], 2)
        self.assertEqual(artifact["metadata"]["not_materialized_structure_count"], 1)
        rows_by_id = {row["entry_id"]: row for row in artifact["rows"]}
        self.assertEqual(
            rows_by_id["m_csa:1"]["coordinate_materialization_status"],
            "materialized",
        )
        self.assertEqual(
            rows_by_id["m_csa:2"]["coordinate_materialization_status"],
            "materialized",
        )
        self.assertEqual(
            rows_by_id["m_csa:3"]["coordinate_materialization_status"],
            "not_materialized_fetch_cap_reached",
        )

    def test_readiness_artifact_emits_no_countable_or_import_ready_rows(self) -> None:
        labels = [
            MechanismLabel("m_csa:1", "fp_a", "seed_fingerprint", "medium", "a"),
            MechanismLabel("m_csa:2", None, "out_of_scope", "medium", "out"),
        ]
        retrieval = {
            "results": [
                _result("m_csa:1", "fp_a", 0.8, pdb_id="1AAA"),
                _result("m_csa:2", "fp_a", 0.1, pdb_id="2BBB"),
            ]
        }

        artifact = build_foldseek_coordinate_readiness(
            retrieval=retrieval,
            labels=labels,
            slice_id="test",
            foldseek_binary="/missing/foldseek",
            max_coordinate_files=0,
        )

        self.assertEqual(artifact["metadata"]["review_status"], "review_only_non_countable")
        self.assertEqual(artifact["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(artifact["metadata"]["import_ready_candidate_count"], 0)
        self.assertFalse(artifact["metadata"]["ready_for_label_import"])
        self.assertFalse(artifact["metadata"]["tm_score_split_computed"])
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in artifact["rows"])
        )
        self.assertTrue(all(not row["import_ready"] for row in artifact["rows"]))

    def test_readiness_records_supported_coordinate_blocker_removed(self) -> None:
        labels = [
            MechanismLabel("m_csa:1", "fp_a", "seed_fingerprint", "medium", "a"),
            MechanismLabel("m_csa:2", "fp_a", "seed_fingerprint", "medium", "a"),
            MechanismLabel("m_csa:3", "fp_b", "seed_fingerprint", "medium", "b"),
        ]
        retrieval = {
            "results": [
                _result("m_csa:1", "fp_a", 0.8, pdb_id="1AAA"),
                _result("m_csa:2", "fp_a", 0.8, pdb_id="2BBB"),
                {
                    "entry_id": "m_csa:3",
                    "entry_name": "m_csa:3",
                    "status": "ok",
                    "top_fingerprints": [{"fingerprint_id": "fp_b", "score": 0.8}],
                },
            ]
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = build_foldseek_coordinate_readiness(
                retrieval=retrieval,
                labels=labels,
                slice_id="test",
                foldseek_binary="/bin/echo",
                coordinate_dir=str(Path(tmpdir) / "coords"),
                max_coordinate_files=2,
                fetch_pdb_cif_fn=lambda pdb_id: f"data_{pdb_id}\n#\n",
            )

        metadata = artifact["metadata"]
        self.assertEqual(metadata["materialized_coordinate_count"], 2)
        self.assertEqual(metadata["staged_coordinate_count"], 2)
        self.assertEqual(metadata["missing_or_unsupported_structure_count"], 1)
        self.assertEqual(metadata["tm_score_coordinate_exclusion_count"], 1)
        self.assertIn("all currently materializable", metadata["blocker_removed"])
        self.assertIn(
            "evaluated rows without supported selected structures are explicitly "
            "excluded from Foldseek coordinate materialization",
            metadata["blockers_remaining"],
        )
        excluded = metadata["tm_score_coordinate_exclusions"][0]
        self.assertEqual(
            excluded["tm_score_coordinate_exclusion_reason"],
            "missing_selected_coordinate_structure",
        )
        self.assertIn(
            "full Foldseek/TM-score split builder has not been run",
            metadata["blockers_remaining"],
        )
        self.assertNotIn(
            "supported selected structures remain unstaged",
            metadata["blockers_remaining"],
        )
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertEqual(metadata["train_test_pair_count"], 0)
        self.assertIsNone(metadata["max_observed_train_test_tm_score"])
        self.assertFalse(metadata["max_observed_train_test_tm_score_computable"])
        self.assertEqual(metadata["raw_name_mapping_unmapped_count"], 0)
        self.assertIn(
            "coordinate staging is deterministic; all currently materializable supported selected structures are staged",
            metadata["limitations"],
        )
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])

    def test_current_1000_foldseek_readiness_artifact_is_pinned(self) -> None:
        artifact = _load_artifact("artifacts/v3_foldseek_coordinate_readiness_1000.json")
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_coordinate_readiness")
        self.assertEqual(metadata["evaluated_count"], 678)
        self.assertEqual(metadata["coordinate_materialization_possible_count"], 676)
        self.assertEqual(metadata["materialized_coordinate_count"], 25)
        self.assertEqual(metadata["fetch_failure_count"], 0)
        self.assertEqual(metadata["missing_or_unsupported_structure_count"], 2)
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertEqual(metadata["review_status"], "review_only_non_countable")
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        if metadata.get("foldseek_version") is not None:
            self.assertEqual(metadata["foldseek_version"], "10.941cd33")
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in artifact["rows"])
        )
        self.assertTrue(all(not row["import_ready"] for row in artifact["rows"]))


class FoldseekTmScoreSignalTests(unittest.TestCase):
    def test_tm_score_signal_is_partial_non_countable_and_parses_pair_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            coord_dir = Path(tmpdir) / "coords"
            coord_dir.mkdir()
            first = coord_dir / "pdb_1AAA.cif"
            second = coord_dir / "pdb_2BBB.cif"
            first.write_text("data_1AAA\n#\n", encoding="utf-8")
            second.write_text("data_2BBB\n#\n", encoding="utf-8")
            commands: list[list[str]] = []

            def fake_runner(command: list[str], cwd: Path) -> None:
                commands.append(command)
                Path(command[4]).write_text(
                    "\n".join(
                        [
                            "pdb_1AAA\tpdb_2BBB\t0.510\t0.490\t0.550",
                            "pdb_2BBB\tpdb_1AAA\t0.420\t0.620\t0.530",
                            "",
                        ]
                    ),
                    encoding="utf-8",
                )

            readiness = _tm_signal_readiness(
                first_coordinate_path=str(first),
                second_coordinate_path=str(second),
            )
            artifact = build_foldseek_tm_score_signal(
                readiness=readiness,
                slice_id="test",
                foldseek_binary="/bin/echo",
                runner=fake_runner,
            )

        metadata = artifact["metadata"]
        self.assertEqual(metadata["review_status"], "review_only_non_countable")
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertTrue(metadata["partial_tm_score_signal_computed"])
        self.assertFalse(metadata["full_evaluated_coordinate_coverage"])
        self.assertEqual(
            metadata["tm_score_signal_coverage_status"],
            "partial_staged_coordinate_signal",
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertIn(
            "evaluated selected-coordinate coverage is partial",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertEqual(metadata["staged_coordinate_count"], 2)
        self.assertEqual(metadata["remaining_to_full_signal_structure_count"], 1)
        self.assertEqual(metadata["pair_count"], 2)
        self.assertEqual(metadata["train_test_pair_count"], 2)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.62)
        self.assertEqual(metadata["threshold_target"], "<0.7")
        self.assertIn("--exhaustive-search", commands[0])
        self.assertIn("query,target,qtmscore,ttmscore,alntmscore", commands[0])
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in artifact["rows"])
        )
        self.assertTrue(all(not row["import_ready"] for row in artifact["rows"]))
        first_row = artifact["rows"][0]
        self.assertEqual(first_row["query_structure_key"], "pdb:1AAA")
        self.assertEqual(first_row["target_structure_key"], "pdb:2BBB")
        self.assertEqual(first_row["qtmscore"], 0.51)
        self.assertEqual(first_row["ttmscore"], 0.49)
        self.assertEqual(first_row["alntmscore"], 0.55)
        self.assertEqual(first_row["max_pair_tm_score"], 0.55)
        self.assertTrue(first_row["train_test_pair"])

    def test_tm_score_signal_records_unmapped_raw_names_without_guessing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            coord_dir = Path(tmpdir) / "coords"
            coord_dir.mkdir()
            first = coord_dir / "pdb_1AAA.cif"
            second = coord_dir / "pdb_2BBB.cif"
            first.write_text("data_1AAA\n#\n", encoding="utf-8")
            second.write_text("data_2BBB\n#\n", encoding="utf-8")

            def fake_runner(command: list[str], cwd: Path) -> None:
                Path(command[4]).write_text(
                    "foldseekInternal42\tpdb_2BBB\t0.1\t0.2\t0.3\n",
                    encoding="utf-8",
                )

            artifact = build_foldseek_tm_score_signal(
                readiness=_tm_signal_readiness(
                    first_coordinate_path=str(first),
                    second_coordinate_path=str(second),
                ),
                slice_id="test",
                foldseek_binary="/bin/echo",
                runner=fake_runner,
            )

        self.assertEqual(artifact["metadata"]["raw_name_mapping_unmapped_count"], 1)
        self.assertEqual(
            artifact["metadata"]["raw_name_mapping_unmapped_names"],
            ["foldseekInternal42"],
        )
        self.assertEqual(artifact["rows"][0]["query_structure_key"], None)
        self.assertEqual(
            artifact["rows"][0]["query_name_mapping_status"],
            "unmapped_raw_name",
        )
        self.assertEqual(artifact["rows"][0]["target_structure_key"], "pdb:2BBB")

    def test_tm_score_signal_maps_pdb_chain_suffixes_from_staged_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            coord_dir = Path(tmpdir) / "coords"
            coord_dir.mkdir()
            first = coord_dir / "renamed_first.cif"
            second = coord_dir / "renamed_second.cif"
            first.write_text("data_1AAA\n#\n", encoding="utf-8")
            second.write_text("data_2BBB\n#\n", encoding="utf-8")

            def fake_runner(command: list[str], cwd: Path) -> None:
                Path(command[4]).write_text(
                    "pdb_1AAA_A\tpdb_2BBB_B\t0.1\t0.2\t0.3\n",
                    encoding="utf-8",
                )

            artifact = build_foldseek_tm_score_signal(
                readiness=_tm_signal_readiness(
                    first_coordinate_path=str(first),
                    second_coordinate_path=str(second),
                ),
                slice_id="test",
                foldseek_binary="/bin/echo",
                runner=fake_runner,
            )

        self.assertEqual(artifact["metadata"]["raw_name_mapping_unmapped_count"], 0)
        self.assertEqual(artifact["rows"][0]["query_structure_key"], "pdb:1AAA")
        self.assertEqual(artifact["rows"][0]["target_structure_key"], "pdb:2BBB")
        self.assertEqual(
            artifact["rows"][0]["query_name_mapping_status"],
            "mapped_chain_suffix_alias",
        )
        self.assertEqual(
            artifact["rows"][0]["target_name_mapping_status"],
            "mapped_chain_suffix_alias",
        )

    def test_tm_score_signal_records_cap_coverage_and_target_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            coord_dir = Path(tmpdir) / "coords"
            coord_dir.mkdir()
            first = coord_dir / "pdb_1AAA.cif"
            second = coord_dir / "pdb_2BBB.cif"
            third = coord_dir / "pdb_3CCC.cif"
            for path in (first, second, third):
                path.write_text(f"data_{path.stem}\n#\n", encoding="utf-8")
            commands: list[list[str]] = []

            def fake_runner(command: list[str], cwd: Path) -> None:
                commands.append(command)
                Path(command[4]).write_text(
                    "\n".join(
                        [
                            "pdb_1AAA\tpdb_2BBB\t0.210\t0.220\t0.230",
                            "pdb_2BBB\tpdb_1AAA\t0.310\t0.320\t0.330",
                            "",
                        ]
                    ),
                    encoding="utf-8",
                )

            readiness = _tm_signal_readiness(
                first_coordinate_path=str(first),
                second_coordinate_path=str(second),
            )
            readiness["metadata"]["coordinate_materialization_possible_count"] = 3
            readiness["metadata"]["coordinate_fetch_cap"] = 3
            readiness["metadata"]["materialized_coordinate_count"] = 3
            readiness["metadata"]["not_materialized_structure_count"] = 0
            readiness["structures"][2]["coordinate_path"] = str(third)
            readiness["structures"][2]["fetch_status"] = "already_materialized"
            artifact = build_foldseek_tm_score_signal(
                readiness=readiness,
                slice_id="test",
                foldseek_binary="/bin/echo",
                max_staged_coordinates=2,
                runner=fake_runner,
            )

        metadata = artifact["metadata"]
        self.assertEqual(metadata["tm_signal_coordinate_cap_requested"], 2)
        self.assertTrue(metadata["tm_signal_coordinate_cap_applied"])
        self.assertEqual(metadata["available_staged_coordinate_count"], 3)
        self.assertEqual(metadata["staged_coordinate_count"], 2)
        self.assertEqual(metadata["remaining_to_full_signal_structure_count"], 1)
        self.assertEqual(metadata["remaining_uncomputed_staged_coordinate_count"], 1)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertIn(
            "available staged coordinates were excluded by the signal cap",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertEqual(metadata["computed_subset_structure_coverage"], 0.6667)
        self.assertEqual(metadata["computed_subset_materialized_coverage"], 0.6667)
        self.assertEqual(metadata["computed_subset_evaluated_entry_coverage"], 0.6667)
        self.assertEqual(Path(commands[0][2]).name, "selected_coordinates")
        self.assertEqual(Path(commands[0][3]).name, "selected_coordinates")
        self.assertEqual(metadata["heldout_in_distribution_pair_count"], 2)
        self.assertEqual(metadata["heldout_pair_count"], 0)
        self.assertEqual(metadata["in_distribution_pair_count"], 0)
        self.assertTrue(metadata["tm_score_target_achieved_for_computed_subset"])
        self.assertIn("staged25-only proof blocker", metadata["blocker_removed"])
        self.assertIn(
            "computed TM-score signal was capped below the available staged coordinate count",
            metadata["limitations"],
        )
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])

    def test_tm_score_signal_summary_only_streams_counts_and_reports_top_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            coord_dir = Path(tmpdir) / "coords"
            coord_dir.mkdir()
            first = coord_dir / "pdb_1AAA.cif"
            second = coord_dir / "pdb_2BBB.cif"
            for path in (first, second):
                path.write_text(f"data_{path.stem}\n#\n", encoding="utf-8")
            commands: list[list[str]] = []

            def fake_runner(command: list[str], cwd: Path) -> None:
                commands.append(command)
                Path(command[4]).write_text(
                    "\n".join(
                        [
                            "pdb_1AAA\tpdb_2BBB\t0.210\t0.220\t0.230",
                            "pdb_2BBB\tpdb_1AAA\t0.710\t0.720\t0.750",
                            "pdb_1AAA\tpdb_1AAA\t0.990\t0.990\t0.990",
                            "",
                        ]
                    ),
                    encoding="utf-8",
                )

            readiness = _tm_signal_readiness(
                first_coordinate_path=str(first),
                second_coordinate_path=str(second),
            )
            readiness["metadata"]["selected_structure_count"] = 2
            readiness["metadata"]["materialized_coordinate_count"] = 2
            readiness["metadata"]["not_materialized_structure_count"] = 0
            readiness["structures"] = readiness["structures"][:2]
            artifact = build_foldseek_tm_score_signal(
                readiness=readiness,
                slice_id="test",
                foldseek_binary="/bin/echo",
                keep_all_rows=False,
                max_reported_rows=1,
                threads=3,
                runner=fake_runner,
            )

        metadata = artifact["metadata"]
        self.assertEqual(metadata["pair_count"], 3)
        self.assertEqual(metadata["mapped_pair_count"], 3)
        self.assertEqual(metadata["train_test_pair_count"], 2)
        self.assertEqual(metadata["target_violating_train_test_pair_row_count"], 1)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.75)
        self.assertEqual(
            metadata["pair_rows_retained_policy"],
            "summary_top_train_test_and_target_violations",
        )
        self.assertEqual(metadata["reported_pair_row_count"], 1)
        self.assertEqual(metadata["omitted_pair_row_count"], 2)
        self.assertEqual(metadata["foldseek_threads"], 3)
        self.assertIn("--threads", commands[0])
        self.assertIn("3", commands[0])
        self.assertEqual(len(artifact["rows"]), 1)
        self.assertEqual(artifact["rows"][0]["max_pair_tm_score"], 0.75)

    def test_tm_score_signal_distinguishes_full_materializable_from_full_evaluated(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            coord_dir = Path(tmpdir) / "coords"
            coord_dir.mkdir()
            first = coord_dir / "pdb_1AAA.cif"
            second = coord_dir / "pdb_2BBB.cif"
            for path in (first, second):
                path.write_text(f"data_{path.stem}\n#\n", encoding="utf-8")

            def fake_runner(command: list[str], cwd: Path) -> None:
                Path(command[4]).write_text(
                    "pdb_1AAA\tpdb_2BBB\t0.310\t0.320\t0.330\n",
                    encoding="utf-8",
                )

            readiness = _tm_signal_readiness(
                first_coordinate_path=str(first),
                second_coordinate_path=str(second),
            )
            readiness["metadata"]["selected_structure_count"] = 2
            readiness["metadata"]["materialized_coordinate_count"] = 2
            readiness["metadata"]["not_materialized_structure_count"] = 0
            readiness["metadata"]["missing_or_unsupported_structure_count"] = 1
            readiness["structures"] = readiness["structures"][:2]
            artifact = build_foldseek_tm_score_signal(
                readiness=readiness,
                slice_id="test",
                foldseek_binary="/bin/echo",
                runner=fake_runner,
            )

        metadata = artifact["metadata"]
        self.assertTrue(metadata["all_materializable_coordinate_signal_computed"])
        self.assertTrue(metadata["all_materializable_coordinate_coverage"])
        self.assertFalse(metadata["full_evaluated_coordinate_coverage"])
        self.assertEqual(
            metadata["tm_score_signal_coverage_status"],
            "full_materializable_coordinate_signal_with_exclusions",
        )
        self.assertFalse(metadata["tm_signal_coordinate_cap_applied"])
        self.assertEqual(metadata["remaining_uncomputed_staged_coordinate_count"], 0)
        self.assertIn(
            "one or more evaluated rows lacks a supported selected structure",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertIn(
            "all currently materializable selected coordinates were searched, but excluded rows without selected structures still block a full evaluated-coordinate claim",
            metadata["limitations"],
        )

    def test_tm_score_signal_records_prior_baseline_and_blocks_false_full_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            coord_dir = Path(tmpdir) / "coords"
            coord_dir.mkdir()
            first = coord_dir / "pdb_1AAA.cif"
            second = coord_dir / "pdb_2BBB.cif"
            for path in (first, second):
                path.write_text(f"data_{path.stem}\n#\n", encoding="utf-8")

            def fake_runner(command: list[str], cwd: Path) -> None:
                Path(command[4]).write_text(
                    "\n".join(
                        [
                            "pdb_1AAA\tpdb_2BBB\t0.710\t0.720\t0.750",
                            "pdb_2BBB\tpdb_1AAA\t0.730\t0.740\t0.760",
                            "",
                        ]
                    ),
                    encoding="utf-8",
                )

            artifact = build_foldseek_tm_score_signal(
                readiness=_tm_signal_readiness(
                    first_coordinate_path=str(first),
                    second_coordinate_path=str(second),
                ),
                slice_id="test",
                foldseek_binary="/bin/echo",
                prior_staged_coordinate_count=1,
                runner=fake_runner,
            )

        metadata = artifact["metadata"]
        self.assertEqual(metadata["prior_staged_coordinate_count"], 1)
        self.assertTrue(metadata["staged_coordinate_count_exceeds_prior"])
        self.assertIn(
            "previous expanded1 partial-signal ceiling",
            metadata["blocker_removed"],
        )
        self.assertFalse(metadata["tm_score_target_achieved_for_computed_subset"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertEqual(
            metadata["tm_score_signal_coverage_status"],
            "partial_staged_coordinate_signal",
        )
        self.assertIn(
            "computed train/test TM-score target <0.7 is not achieved",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertIn(
            "computed train/test TM-score target <0.7 is not achieved",
            metadata["blockers_remaining"],
        )
        self.assertIn(
            "selected structures remain outside the computed signal",
            metadata["full_tm_score_holdout_claim_blockers"],
        )

    def test_all_materializable_signal_writes_compact_split_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            coord_dir = Path(tmpdir) / "coords"
            coord_dir.mkdir()
            first = coord_dir / "pdb_1AAA.cif"
            second = coord_dir / "pdb_2BBB.cif"
            for path in (first, second):
                path.write_text(f"data_{path.stem}\n#\n", encoding="utf-8")
            commands: list[list[str]] = []

            def fake_runner(command: list[str], cwd: Path) -> None:
                commands.append(command)
                Path(command[4]).write_text(
                    "\n".join(
                        [
                            "pdb_1AAA\tpdb_2BBB\t0.610\t0.620\t0.630",
                            "pdb_2BBB\tpdb_1AAA\t0.710\t0.720\t0.760",
                            "pdb_1AAA\tpdb_1AAA\t0.990\t0.990\t0.990",
                            "",
                        ]
                    ),
                    encoding="utf-8",
                )

            readiness = _tm_signal_readiness(
                first_coordinate_path=str(first),
                second_coordinate_path=str(second),
            )
            readiness["metadata"]["evaluated_count"] = 2
            readiness["metadata"]["selected_structure_count"] = 2
            readiness["metadata"]["materialized_coordinate_count"] = 2
            readiness["metadata"]["coordinate_materialization_possible_count"] = 2
            readiness["metadata"]["not_materialized_structure_count"] = 0
            readiness["structures"] = readiness["structures"][:2]
            readiness["rows"] = readiness["rows"][:2]

            artifact = build_foldseek_tm_score_all_materializable_signal(
                readiness=readiness,
                readiness_path="readiness.json",
                slice_id="test",
                foldseek_binary="/bin/echo",
                threads=2,
                runner=fake_runner,
            )

        metadata = artifact["metadata"]
        self.assertEqual(metadata["method"], "foldseek_tm_score_all_materializable_signal")
        self.assertEqual(metadata["review_status"], "review_only_non_countable")
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertTrue(metadata["tm_score_split_computed"])
        self.assertTrue(metadata["all_materializable_tm_score_split_computed"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertTrue(metadata["all_materializable_coordinate_coverage"])
        self.assertTrue(metadata["full_evaluated_coordinate_coverage"])
        self.assertEqual(
            metadata["tm_score_signal_coverage_status"],
            "all_materializable_coordinate_signal",
        )
        self.assertEqual(metadata["staged_coordinate_count"], 2)
        self.assertEqual(metadata["pair_count"], 3)
        self.assertEqual(metadata["mapped_pair_count"], 3)
        self.assertEqual(metadata["train_test_pair_count"], 2)
        self.assertEqual(metadata["heldout_in_distribution_pair_count"], 2)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.76)
        self.assertFalse(metadata["tm_score_target_achieved"])
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 1)
        self.assertEqual(metadata["violating_unique_structure_pair_count"], 1)
        self.assertEqual(metadata["raw_name_mapping_unmapped_count"], 0)
        self.assertEqual(metadata["foldseek_threads"], 2)
        self.assertIn("--threads", commands[0])
        self.assertEqual(commands[0][commands[0].index("--threads") + 1], "2")
        self.assertIn("compact summary artifact", " ".join(metadata["limitations"]))
        self.assertEqual(len(artifact["top_train_test_pairs"]), 2)
        self.assertEqual(len(artifact["blocking_pairs"]), 1)
        self.assertEqual(
            artifact["blocking_pairs"][0]["query_structure_key"], "pdb:2BBB"
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])

    def test_current_1000_all_materializable_signal_timeout_artifact_is_pinned(
        self,
    ) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "foldseek_tm_score_all_materializable_signal"
        )
        self.assertEqual(metadata["foldseek_run_status"], "foldseek_run_timeout")
        self.assertEqual(metadata["foldseek_max_runtime_seconds"], 1500)
        self.assertEqual(metadata["foldseek_threads"], 4)
        self.assertEqual(metadata["staged_coordinate_count"], 672)
        self.assertEqual(metadata["available_staged_coordinate_count"], 672)
        self.assertEqual(metadata["materialized_coordinate_count"], 672)
        self.assertEqual(metadata["remaining_uncomputed_staged_coordinate_count"], 672)
        self.assertTrue(metadata["all_materializable_coordinate_coverage"])
        self.assertFalse(metadata["full_evaluated_coordinate_coverage"])
        self.assertEqual(metadata["missing_or_unsupported_structure_count"], 2)
        self.assertEqual(metadata["pair_count"], 0)
        self.assertEqual(metadata["mapped_pair_count"], 0)
        self.assertEqual(metadata["train_test_pair_count"], 0)
        self.assertIsNone(metadata["max_observed_train_test_tm_score"])
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(len(artifact["top_train_test_pairs"]), 0)
        self.assertEqual(len(artifact["blocking_pairs"]), 0)

    def test_query_chunk_signal_bounds_all_materializable_foldseek_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            coord_dir = Path(tmpdir) / "coords"
            coord_dir.mkdir()
            first = coord_dir / "pdb_1AAA.cif"
            second = coord_dir / "pdb_2BBB.cif"
            third = coord_dir / "pdb_3CCC.cif"
            for path in (first, second, third):
                path.write_text(f"data_{path.stem}\n#\n", encoding="utf-8")
            commands: list[list[str]] = []

            def fake_runner(command: list[str], cwd: Path) -> None:
                commands.append(command)
                query_dir = Path(command[2])
                self.assertEqual(
                    sorted(path.name for path in query_dir.glob("*.cif")),
                    ["pdb_1AAA.cif"],
                )
                self.assertEqual(Path(command[3]).resolve(), coord_dir.resolve())
                Path(command[4]).write_text(
                    "\n".join(
                        [
                            "pdb_1AAA\tpdb_2BBB\t0.610\t0.620\t0.630",
                            "pdb_1AAA\tpdb_3CCC\t0.510\t0.520\t0.530",
                            "pdb_1AAA\tpdb_1AAA\t0.990\t0.990\t0.990",
                            "",
                        ]
                    ),
                    encoding="utf-8",
                )

            readiness = _tm_signal_readiness(
                first_coordinate_path=str(first),
                second_coordinate_path=str(second),
            )
            readiness["metadata"]["evaluated_count"] = 3
            readiness["metadata"]["selected_structure_count"] = 3
            readiness["metadata"]["materialized_coordinate_count"] = 3
            readiness["metadata"]["coordinate_materialization_possible_count"] = 3
            readiness["metadata"]["not_materialized_structure_count"] = 0
            readiness["structures"][2]["coordinate_path"] = str(third)
            readiness["structures"][2]["fetch_status"] = "already_materialized"

            artifact = build_foldseek_tm_score_query_chunk_signal(
                readiness=readiness,
                readiness_path="readiness.json",
                slice_id="test",
                foldseek_binary="/bin/echo",
                chunk_index=0,
                chunk_size=1,
                threads=2,
                runner=fake_runner,
            )

        metadata = artifact["metadata"]
        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
        self.assertEqual(metadata["review_status"], "review_only_non_countable")
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["all_materializable_tm_score_split_computed"])
        self.assertTrue(metadata["all_materializable_query_chunk_signal_computed"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertTrue(metadata["all_materializable_coordinate_coverage"])
        self.assertTrue(metadata["full_evaluated_coordinate_coverage"])
        self.assertEqual(metadata["query_chunk_index"], 0)
        self.assertEqual(metadata["query_chunk_size"], 1)
        self.assertEqual(metadata["query_chunk_count"], 3)
        self.assertEqual(metadata["query_staged_coordinate_count"], 1)
        self.assertEqual(metadata["target_staged_coordinate_count"], 3)
        self.assertEqual(metadata["pair_count"], 3)
        self.assertEqual(metadata["mapped_pair_count"], 3)
        self.assertEqual(metadata["train_test_pair_count"], 2)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.63)
        self.assertTrue(metadata["tm_score_target_achieved_for_query_chunk"])
        self.assertEqual(metadata["remaining_uncomputed_staged_coordinate_count"], 2)
        self.assertEqual(metadata["remaining_query_chunk_count_after_this_chunk"], 2)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertIn(
            "all query chunks must complete and aggregate before a full all-materializable signal exists",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertEqual(len(artifact["query_staged_structures"]), 1)
        self.assertIn("--threads", commands[0])
        self.assertEqual(commands[0][commands[0].index("--threads") + 1], "2")

    def test_current_foldseek_query_chunk_signal_is_pinned(self) -> None:
        expectations = [
            (
                "artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_000_of_056.json",
                0,
                16475,
                6291,
                0.8957,
                11,
                6,
                ["m_csa:12"],
                ["m_csa:405"],
            ),
            (
                "artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_001_of_056.json",
                1,
                11776,
                2851,
                0.8684,
                59,
                7,
                ["m_csa:20"],
                ["m_csa:739"],
            ),
        ]
        for (
            path,
            chunk_index,
            pair_count,
            train_test_pair_count,
            max_tm_score,
            violating_rows,
            violating_unique_pairs,
            first_query_entries,
            first_target_entries,
        ) in expectations:
            artifact = _load_artifact(path)
            metadata = artifact["metadata"]

            self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
            self.assertEqual(metadata["foldseek_run_status"], "completed")
            self.assertEqual(metadata["query_chunk_index"], chunk_index)
            self.assertEqual(metadata["query_chunk_size"], 12)
            self.assertEqual(metadata["query_chunk_count"], 56)
            self.assertEqual(metadata["query_staged_coordinate_count"], 12)
            self.assertEqual(metadata["target_staged_coordinate_count"], 672)
            self.assertEqual(metadata["pair_count"], pair_count)
            self.assertEqual(metadata["mapped_pair_count"], pair_count)
            self.assertEqual(metadata["train_test_pair_count"], train_test_pair_count)
            self.assertEqual(metadata["max_observed_train_test_tm_score"], max_tm_score)
            self.assertFalse(metadata["tm_score_target_achieved_for_query_chunk"])
            self.assertEqual(
                metadata["violating_train_test_pair_row_count"], violating_rows
            )
            self.assertEqual(
                metadata["violating_unique_structure_pair_count"],
                violating_unique_pairs,
            )
            self.assertEqual(
                metadata["violating_unique_entry_pair_count"],
                violating_unique_pairs,
            )
            self.assertFalse(metadata["tm_score_split_computed"])
            self.assertFalse(metadata["full_tm_score_split_computed"])
            self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
            self.assertEqual(metadata["countable_label_count"], 0)
            self.assertEqual(metadata["import_ready_row_count"], 0)
            self.assertIn(
                "all query chunks must complete and aggregate before a full all-materializable signal exists",
                metadata["full_tm_score_holdout_claim_blockers"],
            )
            self.assertIn(
                "computed query-chunk train/test TM-score target <0.7 is not achieved",
                metadata["full_tm_score_holdout_claim_blockers"],
            )
            self.assertEqual(len(artifact["query_staged_structures"]), 12)
            self.assertGreaterEqual(len(artifact["blocking_pairs"]), 5)
            self.assertEqual(
                artifact["blocking_pairs"][0]["query_entry_ids"],
                first_query_entries,
            )
            self.assertEqual(
                artifact["blocking_pairs"][0]["target_entry_ids"],
                first_target_entries,
            )

    def test_current_foldseek_query_chunk_timeout_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
        self.assertEqual(metadata["foldseek_run_status"], "foldseek_run_timeout")
        self.assertEqual(metadata["query_chunk_index"], 2)
        self.assertEqual(metadata["query_chunk_size"], 12)
        self.assertEqual(metadata["query_chunk_count"], 56)
        self.assertEqual(metadata["query_staged_coordinate_count"], 12)
        self.assertEqual(metadata["target_staged_coordinate_count"], 672)
        self.assertEqual(metadata["pair_count"], 0)
        self.assertEqual(metadata["train_test_pair_count"], 0)
        self.assertIsNone(metadata["max_observed_train_test_tm_score"])
        self.assertFalse(metadata["all_materializable_query_chunk_signal_computed"])
        self.assertFalse(metadata["real_tm_score_computed"])
        self.assertFalse(metadata["max_observed_train_test_tm_score_computable"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["remaining_query_chunk_count_after_this_chunk"], 56)
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertIn(
            "Foldseek query chunk did not complete with pair rows",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertIn(
            "exceeded 900 seconds",
            metadata["foldseek_run_error"],
        )

    def test_current_foldseek_query_chunk_retry_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_retry_1800_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertEqual(metadata["query_chunk_index"], 2)
        self.assertEqual(metadata["query_chunk_size"], 12)
        self.assertEqual(metadata["query_chunk_count"], 56)
        self.assertEqual(metadata["query_staged_coordinate_count"], 12)
        self.assertEqual(metadata["target_staged_coordinate_count"], 672)
        self.assertEqual(metadata["pair_count"], 12639)
        self.assertEqual(metadata["mapped_pair_count"], 12639)
        self.assertEqual(metadata["train_test_pair_count"], 3216)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.8427)
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 6)
        self.assertEqual(metadata["violating_unique_structure_pair_count"], 2)
        self.assertEqual(metadata["foldseek_max_runtime_seconds"], 1800)
        self.assertFalse(metadata["tm_score_target_achieved_for_query_chunk"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(artifact["blocking_pairs"][0]["query_entry_ids"], ["m_csa:32"])
        self.assertEqual(artifact["blocking_pairs"][0]["target_entry_ids"], ["m_csa:359"])

    def test_query_chunk_aggregate_keeps_partial_claims_review_only(self) -> None:
        chunk_0 = {
            "metadata": {
                "method": "foldseek_tm_score_query_chunk_signal",
                "query_chunk_index": 0,
                "query_chunk_count": 2,
                "query_chunk_size": 1,
                "foldseek_run_status": "completed",
                "all_materializable_query_chunk_signal_computed": True,
                "full_evaluated_coordinate_coverage": False,
                "all_materializable_coordinate_coverage": True,
                "target_staged_coordinate_count": 2,
                "selected_structure_count": 3,
                "evaluated_count": 3,
                "materialized_coordinate_count": 2,
                "missing_or_unsupported_structure_count": 1,
                "tm_score_coordinate_exclusions": [{"entry_id": "m_csa:9"}],
                "pair_count": 4,
                "mapped_pair_count": 4,
                "train_test_pair_count": 2,
                "heldout_in_distribution_pair_count": 2,
                "heldout_pair_count": 1,
                "in_distribution_pair_count": 1,
                "other_partition_pair_count": 0,
                "unique_unordered_nonself_pair_count": 3,
                "max_observed_train_test_tm_score": 0.8,
                "violating_train_test_pair_row_count": 1,
                "violating_unique_structure_pair_count": 1,
                "raw_name_mapping_unmapped_count": 0,
                "foldseek_version": "10.test",
                "foldseek_command": "foldseek easy-search q all out tmp",
            },
            "query_staged_structures": [{"structure_key": "pdb:1AAA"}],
            "top_train_test_pairs": [
                {
                    "query_structure_key": "pdb:1AAA",
                    "target_structure_key": "pdb:2BBB",
                    "query_entry_ids": ["m_csa:1"],
                    "target_entry_ids": ["m_csa:2"],
                    "max_pair_tm_score": 0.8,
                }
            ],
            "blocking_pairs": [
                {
                    "query_structure_key": "pdb:1AAA",
                    "target_structure_key": "pdb:2BBB",
                    "query_entry_ids": ["m_csa:1"],
                    "target_entry_ids": ["m_csa:2"],
                    "max_pair_tm_score": 0.8,
                    "violates_target": True,
                }
            ],
        }
        chunk_1 = {
            "metadata": {
                "method": "foldseek_tm_score_query_chunk_signal",
                "query_chunk_index": 1,
                "query_chunk_count": 2,
                "query_chunk_size": 1,
                "foldseek_run_status": "completed",
                "all_materializable_query_chunk_signal_computed": True,
                "full_evaluated_coordinate_coverage": False,
                "all_materializable_coordinate_coverage": True,
                "target_staged_coordinate_count": 2,
                "selected_structure_count": 3,
                "evaluated_count": 3,
                "materialized_coordinate_count": 2,
                "missing_or_unsupported_structure_count": 1,
                "tm_score_coordinate_exclusions": [{"entry_id": "m_csa:9"}],
                "pair_count": 3,
                "mapped_pair_count": 3,
                "train_test_pair_count": 1,
                "heldout_in_distribution_pair_count": 1,
                "heldout_pair_count": 1,
                "in_distribution_pair_count": 1,
                "other_partition_pair_count": 0,
                "unique_unordered_nonself_pair_count": 2,
                "max_observed_train_test_tm_score": 0.65,
                "violating_train_test_pair_row_count": 0,
                "violating_unique_structure_pair_count": 0,
                "raw_name_mapping_unmapped_count": 0,
                "foldseek_version": "10.test",
                "foldseek_command": "foldseek easy-search q2 all out tmp",
            },
            "query_staged_structures": [{"structure_key": "pdb:2BBB"}],
            "top_train_test_pairs": [],
            "blocking_pairs": [],
        }

        artifact = aggregate_foldseek_tm_score_query_chunks(
            chunks=[chunk_0, chunk_1],
            chunk_paths=["chunk0.json", "chunk1.json"],
            slice_id="test",
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_aggregate")
        self.assertEqual(metadata["completed_query_chunk_count"], 2)
        self.assertTrue(metadata["all_query_chunks_completed"])
        self.assertEqual(metadata["completed_query_coordinate_count"], 2)
        self.assertEqual(metadata["pair_count"], 7)
        self.assertEqual(metadata["train_test_pair_count"], 3)
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 1)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.8)
        self.assertFalse(metadata["tm_score_target_achieved"])
        self.assertFalse(
            metadata["tm_score_target_achieved_for_completed_query_chunks"]
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(metadata["tm_score_coordinate_exclusion_count"], 1)
        self.assertEqual(len(artifact["blocking_pairs"]), 1)
        self.assertEqual(artifact["blocking_pairs"][0]["source_chunk_index"], 0)
        self.assertIn(
            "completed query-chunk train/test TM-score target <0.7 is not achieved",
            metadata["full_tm_score_holdout_claim_blockers"],
        )

    def test_current_foldseek_query_chunk_aggregate_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_aggregate")
        self.assertEqual(metadata["completed_query_chunk_count"], 2)
        self.assertEqual(metadata["query_chunk_count"], 56)
        self.assertFalse(metadata["all_query_chunks_completed"])
        self.assertEqual(len(artifact["chunks"]), 3)
        self.assertFalse(artifact["chunks"][2]["completed"])
        self.assertEqual(artifact["chunks"][2]["foldseek_run_status"], "foldseek_run_timeout")
        self.assertEqual(metadata["missing_query_chunk_count"], 54)
        self.assertEqual(metadata["missing_query_chunk_indices"][0], 2)
        self.assertEqual(metadata["missing_query_chunk_indices"][-1], 55)
        self.assertEqual(metadata["attempted_query_coordinate_count"], 36)
        self.assertEqual(metadata["completed_query_coordinate_count"], 24)
        self.assertEqual(metadata["target_staged_coordinate_count"], 672)
        self.assertEqual(metadata["completed_query_coordinate_coverage"], 0.0357)
        self.assertEqual(metadata["pair_count"], 28251)
        self.assertEqual(metadata["mapped_pair_count"], 28251)
        self.assertEqual(metadata["train_test_pair_count"], 9142)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.8957)
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 70)
        self.assertEqual(metadata["violating_unique_structure_pair_count_reported"], 13)
        self.assertFalse(
            metadata["tm_score_target_achieved_for_completed_query_chunks"]
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertIn(
            "one or more Foldseek query chunks remain uncomputed",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertIn(
            "completed query-chunk train/test TM-score target <0.7 is not achieved",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertEqual(artifact["blocking_pairs"][0]["query_entry_ids"], ["m_csa:12"])
        self.assertEqual(artifact["blocking_pairs"][0]["target_entry_ids"], ["m_csa:405"])

    def test_current_foldseek_query_chunk_retry_aggregate_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_retry_1800_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_aggregate")
        self.assertEqual(metadata["completed_query_chunk_count"], 3)
        self.assertEqual(metadata["query_chunk_count"], 56)
        self.assertFalse(metadata["all_query_chunks_completed"])
        self.assertEqual(len(artifact["chunks"]), 3)
        self.assertTrue(artifact["chunks"][2]["completed"])
        self.assertEqual(artifact["chunks"][2]["foldseek_run_status"], "completed")
        self.assertEqual(metadata["missing_query_chunk_count"], 53)
        self.assertEqual(metadata["missing_query_chunk_indices"][0], 3)
        self.assertEqual(metadata["missing_query_chunk_indices"][-1], 55)
        self.assertEqual(metadata["completed_query_coordinate_count"], 36)
        self.assertEqual(metadata["remaining_uncomputed_query_coordinate_count"], 636)
        self.assertEqual(metadata["pair_count"], 40890)
        self.assertEqual(metadata["mapped_pair_count"], 40890)
        self.assertEqual(metadata["train_test_pair_count"], 12358)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.8957)
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 76)
        self.assertEqual(metadata["violating_unique_structure_pair_count_reported"], 15)
        self.assertFalse(
            metadata["tm_score_target_achieved_for_completed_query_chunks"]
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(artifact["blocking_pairs"][0]["query_entry_ids"], ["m_csa:12"])
        self.assertEqual(artifact["blocking_pairs"][0]["target_entry_ids"], ["m_csa:405"])

    def test_current_query_chunk_split_repair_plan_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_query_chunk_split_repair_plan_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_split_repair_plan")
        self.assertEqual(
            metadata["source_target_failure_method"],
            "foldseek_tm_score_query_chunk_aggregate",
        )
        self.assertEqual(metadata["observed_blocking_pair_count"], 15)
        self.assertEqual(metadata["repair_candidate_pair_count"], 9)
        self.assertEqual(metadata["manual_review_pair_count"], 6)
        self.assertFalse(metadata["all_observed_blocking_pairs_have_repair_candidate"])
        self.assertEqual(
            metadata["projected_observed_blocking_pair_count_after_repair"], 6
        )
        self.assertEqual(
            metadata["heldout_in_scope_blocking_entry_ids"],
            ["m_csa:20", "m_csa:497", "m_csa:895"],
        )
        self.assertEqual(
            metadata["proposed_moved_heldout_entry_ids"],
            [
                "m_csa:12",
                "m_csa:30",
                "m_csa:32",
                "m_csa:230",
                "m_csa:267",
                "m_csa:346",
                "m_csa:375",
                "m_csa:388",
                "m_csa:614",
            ],
        )
        self.assertEqual(metadata["heldout_count_before_repair"], 135)
        self.assertEqual(metadata["projected_heldout_count_after_repair"], 126)
        self.assertEqual(metadata["heldout_in_scope_count_before_repair"], 44)
        self.assertEqual(metadata["projected_heldout_in_scope_count_after_repair"], 44)
        self.assertEqual(
            metadata["source_signal_remaining_uncomputed_staged_coordinate_count"], 636
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertIn(
            "one or more observed blocking pairs lacks a conservative repair candidate",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        manual_rows = [row for row in artifact["rows"] if not row["repair_candidate"]]
        self.assertEqual(len(manual_rows), 6)
        self.assertEqual(
            manual_rows[0]["repair_status"],
            "requires_manual_review_would_move_heldout_in_scope_rows",
        )

    def test_tm_score_split_redesign_candidate_preserves_in_scope_holdouts(self) -> None:
        sequence_holdout = {
            "metadata": {
                "method": "sequence_distance_holdout_split_repair_candidate",
                "slice_id": "test",
                "sequence_identity_target_preserved_by_cluster_partition": True,
            },
            "rows": [
                {
                    "entry_id": "m_csa:1",
                    "partition": "heldout",
                    "label_type": "seed_fingerprint",
                    "top1_correct": True,
                    "top3_correct": True,
                    "abstained": False,
                    "real_sequence_identity_cluster_id": "mmseqs30:m_csa:1",
                },
                {
                    "entry_id": "m_csa:2",
                    "partition": "in_distribution",
                    "label_type": "seed_fingerprint",
                    "top1_correct": True,
                    "top3_correct": True,
                    "abstained": False,
                    "real_sequence_identity_cluster_id": "mmseqs30:m_csa:2",
                },
                {
                    "entry_id": "m_csa:3",
                    "partition": "heldout",
                    "label_type": "out_of_scope",
                    "abstained": True,
                    "real_sequence_identity_cluster_id": "mmseqs30:m_csa:3",
                },
                {
                    "entry_id": "m_csa:4",
                    "partition": "in_distribution",
                    "label_type": "out_of_scope",
                    "abstained": True,
                    "real_sequence_identity_cluster_id": "mmseqs30:m_csa:4",
                },
            ],
        }
        split_repair_plan = {
            "metadata": {
                "method": "foldseek_tm_score_split_repair_plan",
                "slice_id": "test",
                "manual_review_pair_count": 1,
                "heldout_in_scope_blocking_entry_ids": ["m_csa:1"],
                "heldout_in_scope_blocking_entry_count": 1,
            },
            "rows": [
                {
                    "blocking_pair_index": 1,
                    "blocking_pair_id": "m_csa:1|m_csa:2",
                    "entry_ids": ["m_csa:1", "m_csa:2"],
                    "query_entry_ids": ["m_csa:1"],
                    "target_entry_ids": ["m_csa:2"],
                    "heldout_in_scope_entry_ids": ["m_csa:1"],
                    "heldout_out_of_scope_entry_ids": [],
                    "in_distribution_entry_ids": ["m_csa:2"],
                    "repair_candidate": False,
                    "repair_status": "requires_manual_review_would_move_heldout_in_scope_rows",
                    "max_pair_tm_score": 0.82,
                    "violates_target": True,
                },
                {
                    "blocking_pair_index": 2,
                    "blocking_pair_id": "m_csa:3|m_csa:4",
                    "entry_ids": ["m_csa:3", "m_csa:4"],
                    "query_entry_ids": ["m_csa:3"],
                    "target_entry_ids": ["m_csa:4"],
                    "heldout_in_scope_entry_ids": [],
                    "heldout_out_of_scope_entry_ids": ["m_csa:3"],
                    "in_distribution_entry_ids": ["m_csa:4"],
                    "proposed_entries_to_move_to_in_distribution": ["m_csa:3"],
                    "repair_candidate": True,
                    "repair_status": "repair_candidate_move_heldout_out_of_scope_entries_to_in_distribution",
                    "max_pair_tm_score": 0.74,
                    "violates_target": True,
                },
            ],
        }

        artifact = build_sequence_distance_holdout_split_redesign_candidate(
            sequence_holdout=sequence_holdout,
            split_repair_plan=split_repair_plan,
            sequence_holdout_path="artifacts/test_sequence_holdout.json",
            split_repair_plan_path="artifacts/test_split_repair_plan.json",
            threshold=0.7,
        )
        metadata = artifact["metadata"]
        rows_by_entry = {row["entry_id"]: row for row in artifact["rows"]}

        self.assertEqual(
            metadata["method"], "sequence_distance_holdout_split_redesign_candidate"
        )
        self.assertEqual(metadata["observed_query_chunk_blocking_pair_count"], 2)
        self.assertEqual(
            metadata["projected_observed_blocking_pair_count_after_redesign"], 0
        )
        self.assertTrue(metadata["observed_query_chunk_blockers_resolved_by_redesign"])
        self.assertEqual(metadata["proposed_moved_to_in_distribution_entry_ids"], ["m_csa:3"])
        self.assertEqual(metadata["proposed_moved_to_heldout_entry_ids"], ["m_csa:2"])
        self.assertEqual(metadata["source_heldout_in_scope_count"], 1)
        self.assertEqual(metadata["redesigned_heldout_in_scope_count"], 2)
        self.assertEqual(
            metadata["redesigned_heldout_out_of_scope_false_non_abstention_count"], 0
        )
        self.assertEqual(metadata["sequence_identity_cluster_split_count"], 0)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(rows_by_entry["m_csa:1"]["partition"], "heldout")
        self.assertEqual(rows_by_entry["m_csa:2"]["partition"], "heldout")
        self.assertEqual(rows_by_entry["m_csa:3"]["partition"], "in_distribution")
        self.assertTrue(rows_by_entry["m_csa:2"]["split_redesign_applied_to_candidate"])

    def test_cluster_first_split_assigns_whole_high_tm_components(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        coord_dir = Path(tmp.name) / "coords"
        coord_dir.mkdir()
        paths = {}
        for pdb_id in ("1AAA", "2BBB", "3CCC", "4DDD"):
            path = coord_dir / f"pdb_{pdb_id}.cif"
            path.write_text(f"data_{pdb_id}\n#\n", encoding="utf-8")
            paths[pdb_id] = str(path)

        readiness = {
            "metadata": {
                "method": "foldseek_coordinate_readiness",
                "slice_id": "test",
                "selected_structure_count": 4,
                "materialized_coordinate_count": 4,
                "coordinate_directory": str(coord_dir),
                "foldseek_version": "10.test",
            },
            "structures": [
                {
                    "structure_key": f"pdb:{pdb_id}",
                    "source": "pdb",
                    "structure_id": pdb_id,
                    "entry_ids": [entry_id],
                    "coordinate_path": paths[pdb_id],
                    "fetch_status": "already_materialized",
                }
                for pdb_id, entry_id in (
                    ("1AAA", "m_csa:1"),
                    ("2BBB", "m_csa:2"),
                    ("3CCC", "m_csa:3"),
                    ("4DDD", "m_csa:4"),
                )
            ],
        }
        sequence_holdout = {
            "metadata": {
                "method": "sequence_fold_distance_holdout_evaluation",
                "slice_id": "test",
                "target_identity_achieved": True,
            },
            "rows": [
                {
                    "entry_id": "m_csa:1",
                    "partition": "heldout",
                    "label_type": "seed_fingerprint",
                    "top1_correct": True,
                    "top3_correct": True,
                    "abstained": False,
                    "real_sequence_identity_cluster_id": "mmseqs30:m_csa:1",
                },
                {
                    "entry_id": "m_csa:2",
                    "partition": "in_distribution",
                    "label_type": "seed_fingerprint",
                    "top1_correct": True,
                    "top3_correct": True,
                    "abstained": False,
                    "real_sequence_identity_cluster_id": "mmseqs30:m_csa:2",
                },
                {
                    "entry_id": "m_csa:3",
                    "partition": "heldout",
                    "label_type": "out_of_scope",
                    "abstained": True,
                    "real_sequence_identity_cluster_id": "mmseqs30:m_csa:3",
                },
                {
                    "entry_id": "m_csa:4",
                    "partition": "in_distribution",
                    "label_type": "out_of_scope",
                    "abstained": True,
                    "real_sequence_identity_cluster_id": "mmseqs30:m_csa:4",
                },
            ],
        }
        evidence = {
            "metadata": {"method": "foldseek_tm_score_query_chunk_aggregate"},
            "blocking_pairs": [
                {
                    "query_structure_key": "pdb:1AAA",
                    "target_structure_key": "pdb:2BBB",
                    "query_entry_ids": ["m_csa:1"],
                    "target_entry_ids": ["m_csa:2"],
                    "query_partitions": ["heldout"],
                    "target_partitions": ["in_distribution"],
                    "max_pair_tm_score": 0.82,
                },
                {
                    "query_structure_key": "pdb:3CCC",
                    "target_structure_key": "pdb:4DDD",
                    "query_entry_ids": ["m_csa:3"],
                    "target_entry_ids": ["m_csa:4"],
                    "query_partitions": ["heldout"],
                    "target_partitions": ["in_distribution"],
                    "max_pair_tm_score": 0.78,
                },
            ],
            "top_train_test_pairs": [
                {
                    "query_structure_key": "pdb:2BBB",
                    "target_structure_key": "pdb:4DDD",
                    "query_entry_ids": ["m_csa:2"],
                    "target_entry_ids": ["m_csa:4"],
                    "max_pair_tm_score": 0.65,
                }
            ],
        }

        artifact = build_foldseek_tm_score_cluster_first_split(
            readiness=readiness,
            sequence_holdout=sequence_holdout,
            evidence_artifacts=[evidence],
            readiness_path="readiness.json",
            sequence_holdout_path="holdout.json",
            evidence_paths=["evidence.json"],
        )
        metadata = artifact["metadata"]
        rows_by_entry = {row["entry_id"]: row for row in artifact["rows"]}

        self.assertEqual(
            metadata["method"], "foldseek_tm_score_cluster_first_split_candidate"
        )
        self.assertEqual(metadata["structure_index_member_count"], 4)
        self.assertEqual(metadata["high_tm_partition_constraint_count"], 2)
        self.assertEqual(
            metadata["projected_violating_constraint_count_after_cluster_assignment"],
            0,
        )
        self.assertTrue(
            metadata["observed_high_tm_constraints_resolved_by_cluster_assignment"]
        )
        self.assertEqual(metadata["proposed_moved_to_heldout_entry_ids"], ["m_csa:2"])
        self.assertEqual(
            metadata["proposed_moved_to_in_distribution_entry_ids"], ["m_csa:3"]
        )
        self.assertEqual(metadata["sequence_identity_cluster_split_count"], 0)
        self.assertEqual(metadata["cluster_count"], 2)
        self.assertEqual(metadata["constrained_cluster_count"], 2)
        self.assertEqual(metadata["max_observed_intra_cluster_tm_score"], 0.82)
        self.assertEqual(
            metadata["max_observed_inter_cluster_tm_score_from_supplied_cache"], 0.65
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(rows_by_entry["m_csa:1"]["partition"], "heldout")
        self.assertEqual(rows_by_entry["m_csa:2"]["partition"], "heldout")
        self.assertEqual(rows_by_entry["m_csa:3"]["partition"], "in_distribution")
        self.assertEqual(rows_by_entry["m_csa:4"]["partition"], "in_distribution")
        self.assertEqual(
            len(
                [
                    constraint
                    for constraint in artifact["partition_constraints"]
                    if constraint["projected_violates_target_after_cluster_assignment"]
                ]
            ),
            0,
        )

    def test_current_foldseek_cluster_first_split_candidate_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_cluster_first_split_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "foldseek_tm_score_cluster_first_split_candidate"
        )
        self.assertEqual(metadata["structure_index_member_count"], 672)
        self.assertEqual(metadata["pair_constraint_cache_count"], 33)
        self.assertEqual(metadata["high_tm_partition_constraint_count"], 24)
        self.assertEqual(metadata["cluster_count"], 650)
        self.assertEqual(metadata["constrained_cluster_count"], 12)
        self.assertEqual(metadata["singleton_cluster_count"], 638)
        self.assertEqual(metadata["max_cluster_structure_count"], 6)
        self.assertEqual(
            metadata["projected_violating_constraint_count_after_cluster_assignment"],
            0,
        )
        self.assertTrue(
            metadata["observed_high_tm_constraints_resolved_by_cluster_assignment"]
        )
        self.assertEqual(
            metadata["proposed_moved_to_heldout_entry_ids"],
            [
                "m_csa:6",
                "m_csa:15",
                "m_csa:16",
                "m_csa:108",
                "m_csa:123",
                "m_csa:157",
                "m_csa:258",
                "m_csa:277",
                "m_csa:294",
                "m_csa:320",
                "m_csa:378",
                "m_csa:739",
            ],
        )
        self.assertEqual(
            metadata["proposed_moved_to_in_distribution_entry_ids"],
            [
                "m_csa:12",
                "m_csa:30",
                "m_csa:32",
                "m_csa:34",
                "m_csa:230",
                "m_csa:267",
                "m_csa:346",
                "m_csa:375",
                "m_csa:388",
                "m_csa:614",
            ],
        )
        self.assertEqual(metadata["cluster_first_heldout_count"], 138)
        self.assertEqual(metadata["cluster_first_heldout_in_scope_count"], 56)
        self.assertEqual(
            metadata["cluster_first_heldout_out_of_scope_false_non_abstention_count"],
            0,
        )
        self.assertEqual(metadata["sequence_identity_cluster_split_count"], 0)
        self.assertEqual(metadata["max_observed_intra_cluster_tm_score"], 0.926)
        self.assertEqual(
            metadata["max_observed_inter_cluster_tm_score_from_supplied_cache"],
            0.695,
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(len(artifact["partition_constraints"]), 24)
        self.assertFalse(
            any(
                constraint["projected_violates_target_after_cluster_assignment"]
                for constraint in artifact["partition_constraints"]
            )
        )

    def test_current_foldseek_cluster_first_round3_candidate_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_cluster_first_split_round3_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "foldseek_tm_score_cluster_first_split_candidate"
        )
        self.assertEqual(metadata["structure_index_member_count"], 672)
        self.assertEqual(metadata["pair_constraint_cache_count"], 56)
        self.assertEqual(metadata["high_tm_partition_constraint_count"], 34)
        self.assertEqual(metadata["cluster_count"], 640)
        self.assertEqual(metadata["constrained_cluster_count"], 14)
        self.assertEqual(metadata["max_cluster_structure_count"], 10)
        self.assertEqual(
            metadata["projected_violating_constraint_count_after_cluster_assignment"],
            0,
        )
        self.assertTrue(
            metadata["observed_high_tm_constraints_resolved_by_cluster_assignment"]
        )
        self.assertEqual(metadata["proposed_moved_to_heldout_entry_count"], 12)
        self.assertEqual(
            metadata["proposed_moved_to_in_distribution_entry_ids"],
            [
                "m_csa:12",
                "m_csa:30",
                "m_csa:32",
                "m_csa:34",
                "m_csa:45",
                "m_csa:118",
                "m_csa:230",
                "m_csa:267",
                "m_csa:346",
                "m_csa:375",
                "m_csa:388",
                "m_csa:614",
            ],
        )
        self.assertEqual(metadata["cluster_first_heldout_count"], 136)
        self.assertEqual(metadata["cluster_first_heldout_in_scope_count"], 56)
        self.assertEqual(
            metadata["cluster_first_heldout_out_of_scope_false_non_abstention_count"],
            0,
        )
        self.assertEqual(metadata["sequence_identity_cluster_split_count"], 0)
        self.assertEqual(metadata["max_observed_intra_cluster_tm_score"], 0.926)
        self.assertEqual(
            metadata["max_observed_inter_cluster_tm_score_from_supplied_cache"],
            0.6993,
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_cluster_first_round4_candidate_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_cluster_first_split_round4_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "foldseek_tm_score_cluster_first_split_candidate"
        )
        self.assertEqual(metadata["structure_index_member_count"], 672)
        self.assertEqual(metadata["pair_constraint_cache_count"], 64)
        self.assertEqual(metadata["high_tm_partition_constraint_count"], 35)
        self.assertEqual(metadata["cluster_count"], 639)
        self.assertEqual(metadata["constrained_cluster_count"], 14)
        self.assertEqual(metadata["max_cluster_structure_count"], 11)
        self.assertEqual(
            metadata["projected_violating_constraint_count_after_cluster_assignment"],
            0,
        )
        self.assertTrue(
            metadata["observed_high_tm_constraints_resolved_by_cluster_assignment"]
        )
        self.assertEqual(metadata["proposed_moved_to_heldout_entry_count"], 12)
        self.assertEqual(metadata["proposed_moved_to_in_distribution_entry_count"], 13)
        self.assertIn(
            "m_csa:397", metadata["proposed_moved_to_in_distribution_entry_ids"]
        )
        self.assertEqual(metadata["cluster_first_heldout_count"], 135)
        self.assertEqual(metadata["cluster_first_heldout_in_scope_count"], 56)
        self.assertEqual(
            metadata["cluster_first_heldout_out_of_scope_false_non_abstention_count"],
            0,
        )
        self.assertEqual(metadata["sequence_identity_cluster_split_count"], 0)
        self.assertEqual(metadata["max_observed_intra_cluster_tm_score"], 0.926)
        self.assertEqual(
            metadata["max_observed_inter_cluster_tm_score_from_supplied_cache"],
            0.6993,
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(len(artifact["partition_constraints"]), 35)

    def test_current_foldseek_cluster_first_round2_subchunk_aggregate_is_pinned(
        self,
    ) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round2_query_subchunk_aggregate_006_007_of_112.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_aggregate")
        self.assertEqual(metadata["query_chunk_count"], 112)
        self.assertEqual(metadata["completed_query_chunk_count"], 2)
        self.assertEqual(metadata["completed_query_coordinate_count"], 12)
        self.assertEqual(metadata["remaining_uncomputed_query_coordinate_count"], 660)
        self.assertEqual(metadata["pair_count"], 23301)
        self.assertEqual(metadata["mapped_pair_count"], 23301)
        self.assertEqual(metadata["train_test_pair_count"], 7807)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.8651)
        self.assertFalse(
            metadata["tm_score_target_achieved_for_completed_query_chunks"]
        )
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 16)
        self.assertEqual(metadata["violating_unique_structure_pair_count_reported"], 9)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_cluster_first_round3_subchunk_aggregate_is_pinned(
        self,
    ) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round3_query_subchunk_aggregate_006_007_of_112.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_aggregate")
        self.assertEqual(metadata["query_chunk_count"], 112)
        self.assertEqual(metadata["completed_query_chunk_count"], 2)
        self.assertEqual(metadata["completed_query_coordinate_count"], 12)
        self.assertEqual(metadata["remaining_uncomputed_query_coordinate_count"], 660)
        self.assertEqual(metadata["pair_count"], 23301)
        self.assertEqual(metadata["mapped_pair_count"], 23301)
        self.assertEqual(metadata["train_test_pair_count"], 7332)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.8043)
        self.assertFalse(
            metadata["tm_score_target_achieved_for_completed_query_chunks"]
        )
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 1)
        self.assertEqual(metadata["violating_unique_structure_pair_count_reported"], 1)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_cluster_first_round4_subchunk_007_is_pinned(
        self,
    ) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round4_query_subchunk_007_of_112.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertEqual(metadata["query_chunk_count"], 112)
        self.assertEqual(metadata["query_chunk_index"], 7)
        self.assertEqual(metadata["query_chunk_size"], 6)
        self.assertEqual(metadata["query_staged_coordinate_count"], 6)
        self.assertEqual(metadata["pair_count"], 9094)
        self.assertEqual(metadata["mapped_pair_count"], 9094)
        self.assertEqual(metadata["train_test_pair_count"], 4975)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.6598)
        self.assertTrue(metadata["tm_score_target_achieved"])
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 0)
        self.assertEqual(artifact["blocking_pairs"], [])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_cluster_first_round3_readiness_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round3.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_coordinate_readiness")
        self.assertEqual(metadata["sequence_holdout_row_count"], 678)
        self.assertEqual(metadata["materialized_coordinate_count"], 672)
        self.assertEqual(metadata["tm_score_coordinate_exclusion_count"], 2)
        self.assertEqual(
            [row["entry_id"] for row in metadata["tm_score_coordinate_exclusions"]],
            ["m_csa:372", "m_csa:501"],
        )
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_cluster_first_round4_readiness_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round4.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_coordinate_readiness")
        self.assertEqual(metadata["sequence_holdout_row_count"], 678)
        self.assertEqual(metadata["materialized_coordinate_count"], 672)
        self.assertEqual(metadata["tm_score_coordinate_exclusion_count"], 2)
        self.assertEqual(
            [row["entry_id"] for row in metadata["tm_score_coordinate_exclusions"]],
            ["m_csa:372", "m_csa:501"],
        )
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_cluster_first_round6_subchunk_010_timeout_is_pinned(
        self,
    ) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round6_query_subchunk_010_of_112.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
        self.assertEqual(metadata["foldseek_run_status"], "foldseek_run_timeout")
        self.assertEqual(metadata["query_chunk_count"], 112)
        self.assertEqual(metadata["query_chunk_index"], 10)
        self.assertEqual(metadata["query_chunk_size"], 6)
        self.assertEqual(
            metadata["query_staged_entry_ids"],
            ["m_csa:61", "m_csa:62", "m_csa:63", "m_csa:64", "m_csa:65", "m_csa:66"],
        )
        self.assertEqual(metadata["pair_count"], 0)
        self.assertEqual(metadata["mapped_pair_count"], 0)
        self.assertEqual(metadata["train_test_pair_count"], 0)
        self.assertFalse(metadata["tm_score_target_achieved_for_query_chunk"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])

    def test_current_foldseek_cluster_first_round6_microchunk_020_failure_is_pinned(
        self,
    ) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round6_query_microchunk_020_of_224.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertEqual(metadata["query_chunk_count"], 224)
        self.assertEqual(metadata["query_chunk_index"], 20)
        self.assertEqual(metadata["query_chunk_size"], 3)
        self.assertEqual(
            metadata["query_staged_entry_ids"], ["m_csa:61", "m_csa:62", "m_csa:63"]
        )
        self.assertEqual(metadata["pair_count"], 7488)
        self.assertEqual(metadata["mapped_pair_count"], 7488)
        self.assertEqual(metadata["train_test_pair_count"], 1319)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.7116)
        self.assertFalse(metadata["tm_score_target_achieved_for_query_chunk"])
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 2)
        self.assertEqual(metadata["violating_unique_structure_pair_count"], 1)
        self.assertEqual(len(artifact["blocking_pairs"]), 1)
        self.assertEqual(artifact["blocking_pairs"][0]["query_entry_ids"], ["m_csa:63"])
        self.assertEqual(artifact["blocking_pairs"][0]["target_entry_ids"], ["m_csa:188"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])

    def test_current_foldseek_cluster_first_round7_candidate_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_cluster_first_split_round7_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "foldseek_tm_score_cluster_first_split_candidate"
        )
        self.assertEqual(metadata["high_tm_partition_constraint_count"], 38)
        self.assertEqual(metadata["constrained_cluster_count"], 17)
        self.assertEqual(metadata["cluster_first_heldout_count"], 132)
        self.assertEqual(metadata["cluster_first_heldout_in_scope_count"], 56)
        self.assertEqual(metadata["cluster_first_heldout_out_of_scope_count"], 76)
        self.assertEqual(
            metadata["cluster_first_heldout_out_of_scope_false_non_abstention_count"],
            0,
        )
        self.assertEqual(metadata["sequence_identity_cluster_split_count"], 0)
        self.assertEqual(
            metadata["projected_violating_constraint_count_after_cluster_assignment"],
            0,
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_cluster_first_round7_microchunk_020_timeout_is_pinned(
        self,
    ) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_microchunk_020_of_224.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
        self.assertEqual(metadata["foldseek_run_status"], "foldseek_run_timeout")
        self.assertEqual(metadata["query_chunk_count"], 224)
        self.assertEqual(metadata["query_chunk_index"], 20)
        self.assertEqual(metadata["query_chunk_size"], 3)
        self.assertEqual(
            metadata["query_staged_entry_ids"], ["m_csa:61", "m_csa:62", "m_csa:63"]
        )
        self.assertEqual(metadata["pair_count"], 0)
        self.assertEqual(metadata["mapped_pair_count"], 0)
        self.assertEqual(metadata["train_test_pair_count"], 0)
        self.assertFalse(metadata["tm_score_target_achieved_for_query_chunk"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])

    def test_current_sequence_holdout_split_redesign_candidate_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_sequence_distance_holdout_split_redesign_candidate_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "sequence_distance_holdout_split_redesign_candidate"
        )
        self.assertEqual(metadata["observed_query_chunk_blocking_pair_count"], 15)
        self.assertEqual(
            metadata["projected_observed_blocking_pair_count_after_redesign"], 0
        )
        self.assertTrue(metadata["observed_query_chunk_blockers_resolved_by_redesign"])
        self.assertEqual(metadata["proposed_moved_to_in_distribution_entry_count"], 9)
        self.assertEqual(metadata["proposed_moved_to_heldout_entry_count"], 6)
        self.assertEqual(metadata["redesigned_heldout_count"], 132)
        self.assertEqual(metadata["redesigned_heldout_in_scope_count"], 50)
        self.assertEqual(
            metadata["redesigned_heldout_out_of_scope_false_non_abstention_count"], 0
        )
        self.assertEqual(metadata["sequence_identity_cluster_split_count"], 0)
        self.assertEqual(
            metadata["proposed_moved_to_heldout_entry_ids"],
            ["m_csa:6", "m_csa:15", "m_csa:16", "m_csa:123", "m_csa:294", "m_csa:739"],
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_split_redesign_readiness_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_coordinate_readiness_1000_split_redesign_candidate.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_coordinate_readiness")
        self.assertEqual(
            metadata["sequence_holdout_row_count"],
            678,
        )
        self.assertEqual(metadata["materialized_coordinate_count"], 672)
        self.assertEqual(metadata["tm_score_coordinate_exclusion_count"], 2)
        self.assertEqual(
            [row["entry_id"] for row in metadata["tm_score_coordinate_exclusions"]],
            ["m_csa:372", "m_csa:501"],
        )
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_split_redesign_chunk_zero_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_query_chunk_000_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertEqual(metadata["query_chunk_index"], 0)
        self.assertEqual(metadata["query_staged_coordinate_count"], 12)
        self.assertEqual(metadata["pair_count"], 16475)
        self.assertEqual(metadata["train_test_pair_count"], 6909)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.926)
        self.assertFalse(metadata["tm_score_target_achieved_for_query_chunk"])
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 15)
        self.assertEqual(metadata["violating_unique_structure_pair_count"], 4)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(artifact["blocking_pairs"][0]["query_entry_ids"], ["m_csa:6"])
        self.assertEqual(artifact["blocking_pairs"][0]["target_entry_ids"], ["m_csa:277"])

    def test_current_foldseek_split_redesign_repair_plan_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_split_redesign_candidate_query_chunk_repair_plan_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_split_repair_plan")
        self.assertEqual(metadata["observed_blocking_pair_count"], 4)
        self.assertEqual(metadata["repair_candidate_pair_count"], 0)
        self.assertEqual(metadata["manual_review_pair_count"], 4)
        self.assertEqual(
            metadata["projected_observed_blocking_pair_count_after_repair"], 4
        )
        self.assertEqual(metadata["heldout_in_scope_blocking_entry_ids"], ["m_csa:6"])
        self.assertFalse(metadata["all_observed_blocking_pairs_have_repair_candidate"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(
            [row["target_entry_ids"][0] for row in artifact["rows"]],
            ["m_csa:277", "m_csa:378", "m_csa:320", "m_csa:108"],
        )

    def test_current_sequence_holdout_split_redesign_round2_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_sequence_distance_holdout_split_redesign_candidate_round2_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "sequence_distance_holdout_split_redesign_candidate"
        )
        self.assertEqual(metadata["observed_query_chunk_blocking_pair_count"], 4)
        self.assertEqual(
            metadata["projected_observed_blocking_pair_count_after_redesign"], 0
        )
        self.assertTrue(metadata["observed_query_chunk_blockers_resolved_by_redesign"])
        self.assertEqual(metadata["proposed_moved_to_heldout_entry_count"], 4)
        self.assertEqual(
            metadata["proposed_moved_to_heldout_entry_ids"],
            ["m_csa:108", "m_csa:277", "m_csa:320", "m_csa:378"],
        )
        self.assertEqual(metadata["redesigned_heldout_count"], 136)
        self.assertEqual(metadata["redesigned_heldout_in_scope_count"], 54)
        self.assertEqual(
            metadata["redesigned_heldout_out_of_scope_false_non_abstention_count"], 0
        )
        self.assertEqual(metadata["sequence_identity_cluster_split_count"], 0)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_split_redesign_round2_chunk_zero_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_000_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertEqual(metadata["query_chunk_index"], 0)
        self.assertEqual(metadata["query_staged_coordinate_count"], 12)
        self.assertEqual(metadata["pair_count"], 16475)
        self.assertEqual(metadata["train_test_pair_count"], 6939)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.695)
        self.assertTrue(metadata["tm_score_target_achieved_for_query_chunk"])
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 0)
        self.assertEqual(metadata["violating_unique_structure_pair_count"], 0)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(artifact["blocking_pairs"], [])

    def test_current_foldseek_split_redesign_round2_aggregate_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_aggregate_000_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_aggregate")
        self.assertEqual(metadata["completed_query_chunk_count"], 1)
        self.assertEqual(metadata["completed_query_coordinate_count"], 12)
        self.assertEqual(metadata["remaining_uncomputed_query_coordinate_count"], 660)
        self.assertEqual(metadata["pair_count"], 16475)
        self.assertEqual(metadata["train_test_pair_count"], 6939)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.695)
        self.assertTrue(metadata["tm_score_target_achieved_for_completed_query_chunks"])
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 0)
        self.assertEqual(metadata["violating_unique_structure_pair_count_reported"], 0)
        self.assertFalse(metadata["all_query_chunks_completed"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_split_redesign_round2_chunk_one_failure_is_pinned(
        self,
    ) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_001_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertEqual(metadata["query_chunk_index"], 1)
        self.assertEqual(metadata["query_staged_coordinate_count"], 12)
        self.assertEqual(metadata["pair_count"], 11776)
        self.assertEqual(metadata["train_test_pair_count"], 4154)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.8182)
        self.assertFalse(metadata["tm_score_target_achieved_for_query_chunk"])
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 12)
        self.assertEqual(metadata["violating_unique_structure_pair_count"], 4)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_split_redesign_round2_repair_plan_is_pinned(
        self,
    ) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_split_redesign_candidate_round2_query_chunk_repair_plan_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_split_repair_plan")
        self.assertEqual(metadata["observed_blocking_pair_count"], 4)
        self.assertEqual(metadata["repair_candidate_pair_count"], 0)
        self.assertEqual(metadata["manual_review_pair_count"], 4)
        self.assertEqual(
            metadata["heldout_in_scope_blocking_entry_ids"],
            ["m_csa:15", "m_csa:16"],
        )
        self.assertTrue(metadata["current_sequence_holdout_split_tm_score_target_blocked"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_sequence_holdout_split_redesign_round3_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_sequence_distance_holdout_split_redesign_candidate_round3_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "sequence_distance_holdout_split_redesign_candidate"
        )
        self.assertEqual(metadata["observed_query_chunk_blocking_pair_count"], 4)
        self.assertEqual(
            metadata["projected_observed_blocking_pair_count_after_redesign"], 0
        )
        self.assertTrue(metadata["observed_query_chunk_blockers_resolved_by_redesign"])
        self.assertEqual(
            metadata["proposed_moved_to_heldout_entry_ids"],
            ["m_csa:157", "m_csa:258"],
        )
        self.assertEqual(metadata["redesigned_heldout_count"], 138)
        self.assertEqual(metadata["redesigned_heldout_in_scope_count"], 56)
        self.assertEqual(metadata["sequence_identity_cluster_split_count"], 0)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_split_redesign_round3_aggregate_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_001_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_aggregate")
        self.assertEqual(metadata["completed_query_chunk_count"], 2)
        self.assertEqual(metadata["completed_query_coordinate_count"], 24)
        self.assertEqual(metadata["remaining_uncomputed_query_coordinate_count"], 648)
        self.assertEqual(metadata["pair_count"], 28251)
        self.assertEqual(metadata["train_test_pair_count"], 11087)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.695)
        self.assertTrue(metadata["tm_score_target_achieved_for_completed_query_chunks"])
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 0)
        self.assertEqual(metadata["violating_unique_structure_pair_count_reported"], 0)
        self.assertFalse(metadata["all_query_chunks_completed"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)

    def test_current_foldseek_split_redesign_round3_chunk_two_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_002_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertEqual(metadata["query_chunk_index"], 2)
        self.assertEqual(metadata["query_staged_coordinate_count"], 12)
        self.assertEqual(metadata["target_staged_coordinate_count"], 672)
        self.assertEqual(metadata["pair_count"], 12639)
        self.assertEqual(metadata["mapped_pair_count"], 12639)
        self.assertEqual(metadata["train_test_pair_count"], 2385)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.584)
        self.assertTrue(metadata["tm_score_target_achieved_for_query_chunk"])
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 0)
        self.assertEqual(metadata["violating_unique_structure_pair_count"], 0)
        self.assertEqual(metadata["remaining_query_chunk_count_after_this_chunk"], 53)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(artifact["blocking_pairs"], [])

    def test_current_foldseek_split_redesign_round3_aggregate_000_002_is_pinned(
        self,
    ) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_002_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_aggregate")
        self.assertEqual(metadata["completed_query_chunk_count"], 3)
        self.assertEqual(metadata["completed_query_coordinate_count"], 36)
        self.assertEqual(metadata["remaining_uncomputed_query_coordinate_count"], 636)
        self.assertEqual(metadata["missing_query_chunk_count"], 53)
        self.assertEqual(metadata["missing_query_chunk_indices"][0], 3)
        self.assertEqual(metadata["missing_query_chunk_indices"][-1], 55)
        self.assertEqual(metadata["pair_count"], 40890)
        self.assertEqual(metadata["mapped_pair_count"], 40890)
        self.assertEqual(metadata["train_test_pair_count"], 13472)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.695)
        self.assertTrue(metadata["tm_score_target_achieved_for_completed_query_chunks"])
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 0)
        self.assertEqual(metadata["violating_unique_structure_pair_count_reported"], 0)
        self.assertFalse(metadata["all_query_chunks_completed"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(artifact["blocking_pairs"], [])

    def test_current_foldseek_split_redesign_round3_chunk_three_timeout_is_pinned(
        self,
    ) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_003_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_signal")
        self.assertEqual(metadata["foldseek_run_status"], "foldseek_run_timeout")
        self.assertEqual(metadata["query_chunk_index"], 3)
        self.assertEqual(metadata["query_staged_coordinate_count"], 12)
        self.assertEqual(metadata["target_staged_coordinate_count"], 672)
        self.assertEqual(metadata["pair_count"], 0)
        self.assertEqual(metadata["mapped_pair_count"], 0)
        self.assertEqual(metadata["train_test_pair_count"], 0)
        self.assertIsNone(metadata["max_observed_train_test_tm_score"])
        self.assertFalse(metadata["all_materializable_query_chunk_signal_computed"])
        self.assertFalse(metadata["real_tm_score_computed"])
        self.assertFalse(metadata["max_observed_train_test_tm_score_computable"])
        self.assertEqual(metadata["remaining_query_chunk_count_after_this_chunk"], 56)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertIn("exceeded 900 seconds", metadata["foldseek_run_error"])
        self.assertIn(
            "Foldseek query chunk did not complete with pair rows",
            metadata["full_tm_score_holdout_claim_blockers"],
        )

    def test_current_foldseek_split_redesign_round3_aggregate_000_003_is_pinned(
        self,
    ) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_003_of_056.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_query_chunk_aggregate")
        self.assertEqual(len(artifact["chunks"]), 4)
        self.assertTrue(artifact["chunks"][2]["completed"])
        self.assertFalse(artifact["chunks"][3]["completed"])
        self.assertEqual(artifact["chunks"][3]["foldseek_run_status"], "foldseek_run_timeout")
        self.assertEqual(metadata["completed_query_chunk_count"], 3)
        self.assertEqual(metadata["attempted_query_coordinate_count"], 48)
        self.assertEqual(metadata["completed_query_coordinate_count"], 36)
        self.assertEqual(metadata["remaining_uncomputed_query_coordinate_count"], 636)
        self.assertEqual(metadata["missing_query_chunk_count"], 53)
        self.assertEqual(metadata["missing_query_chunk_indices"][0], 3)
        self.assertEqual(metadata["missing_query_chunk_indices"][-1], 55)
        self.assertEqual(metadata["pair_count"], 40890)
        self.assertEqual(metadata["mapped_pair_count"], 40890)
        self.assertEqual(metadata["train_test_pair_count"], 13472)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.695)
        self.assertTrue(metadata["tm_score_target_achieved_for_completed_query_chunks"])
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 0)
        self.assertEqual(metadata["violating_unique_structure_pair_count_reported"], 0)
        self.assertFalse(metadata["all_query_chunks_completed"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(artifact["blocking_pairs"], [])

    def test_tm_score_target_failure_audit_names_blocking_pairs(self) -> None:
        signal = {
            "metadata": {
                "method": "foldseek_tm_score_signal",
                "slice_id": "test",
                "foldseek_version": "10.test",
                "foldseek_command": "foldseek easy-search coords coords out tmp",
                "foldseek_run_status": "completed",
                "staged_coordinate_count": 2,
                "available_staged_coordinate_count": 3,
                "remaining_uncomputed_staged_coordinate_count": 1,
                "tm_score_signal_coverage_status": "partial_staged_coordinate_signal",
                "tm_signal_coordinate_cap_applied": True,
                "full_tm_score_split_computed": False,
                "full_tm_score_holdout_claim_permitted": False,
                "full_tm_score_holdout_claim_blockers": [
                    "available staged coordinates were excluded by the signal cap"
                ],
            },
            "rows": [
                {
                    "query_structure_key": "pdb:1AAA",
                    "target_structure_key": "pdb:2BBB",
                    "query_structure_id": "1AAA",
                    "target_structure_id": "2BBB",
                    "query_entry_ids": ["m_csa:1"],
                    "target_entry_ids": ["m_csa:2"],
                    "query_partitions": ["heldout"],
                    "target_partitions": ["in_distribution"],
                    "raw_query_name": "pdb_1AAA_A",
                    "raw_target_name": "pdb_2BBB_A",
                    "qtmscore": 0.71,
                    "ttmscore": 0.72,
                    "alntmscore": 0.75,
                    "max_pair_tm_score": 0.75,
                    "train_test_pair": True,
                    "self_pair": False,
                    "line_number": 1,
                },
                {
                    "query_structure_key": "pdb:2BBB",
                    "target_structure_key": "pdb:1AAA",
                    "query_entry_ids": ["m_csa:2"],
                    "target_entry_ids": ["m_csa:1"],
                    "query_partitions": ["in_distribution"],
                    "target_partitions": ["heldout"],
                    "raw_query_name": "pdb_2BBB_A",
                    "raw_target_name": "pdb_1AAA_A",
                    "max_pair_tm_score": 0.73,
                    "train_test_pair": True,
                    "self_pair": False,
                    "line_number": 2,
                },
                {
                    "query_structure_key": "pdb:1AAA",
                    "target_structure_key": "pdb:3CCC",
                    "query_entry_ids": ["m_csa:1"],
                    "target_entry_ids": ["m_csa:3"],
                    "query_partitions": ["heldout"],
                    "target_partitions": ["in_distribution"],
                    "max_pair_tm_score": 0.61,
                    "train_test_pair": True,
                    "self_pair": False,
                    "line_number": 3,
                },
            ],
        }

        artifact = audit_foldseek_tm_score_target_failure(
            signal=signal,
            signal_path="artifacts/test_signal.json",
            threshold=0.7,
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_target_failure_audit")
        self.assertEqual(metadata["review_status"], "review_only_non_countable")
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertTrue(
            metadata["current_sequence_holdout_split_tm_score_target_blocked"]
        )
        self.assertTrue(metadata["split_repair_required_for_target"])
        self.assertFalse(metadata["tm_score_target_achieved_for_computed_subset"])
        self.assertEqual(metadata["train_test_pair_count"], 3)
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 2)
        self.assertEqual(metadata["violating_unique_structure_pair_count"], 1)
        self.assertEqual(metadata["violating_unique_entry_pair_count"], 1)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.75)
        self.assertIn(
            "computed train/test TM-score target <0.7 is already violated in the computed subset",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertEqual(len(artifact["blocking_pairs"]), 1)
        pair = artifact["blocking_pairs"][0]
        self.assertEqual(pair["query_structure_key"], "pdb:1AAA")
        self.assertEqual(pair["target_structure_key"], "pdb:2BBB")
        self.assertEqual(pair["query_entry_ids"], ["m_csa:1"])
        self.assertEqual(pair["target_entry_ids"], ["m_csa:2"])
        self.assertEqual(pair["max_pair_tm_score"], 0.75)
        self.assertTrue(pair["violates_target"])
        self.assertFalse(pair["countable_label_candidate"])
        self.assertFalse(pair["import_ready"])

    def test_tm_score_split_repair_plan_preserves_heldout_in_scope_rows(self) -> None:
        target_failure = {
            "metadata": {
                "method": "foldseek_tm_score_target_failure_audit",
                "slice_id": "test",
                "current_sequence_holdout_split_tm_score_target_blocked": True,
                "source_signal_coverage_status": "partial_staged_coordinate_signal",
                "source_signal_full_tm_score_split_computed": False,
                "source_signal_remaining_uncomputed_staged_coordinate_count": 1,
                "full_tm_score_holdout_claim_blockers": [
                    "computed train/test TM-score target <0.7 is already violated in the computed subset"
                ],
            },
            "blocking_pairs": [
                {
                    "query_structure_key": "pdb:1AAA",
                    "target_structure_key": "pdb:2BBB",
                    "query_entry_ids": ["m_csa:1"],
                    "target_entry_ids": ["m_csa:2"],
                    "max_pair_tm_score": 0.75,
                    "violates_target": True,
                }
            ],
        }
        sequence_holdout = {
            "metadata": {
                "method": "sequence_fold_distance_holdout_evaluation",
                "slice_id": "test",
                "heldout_count": 2,
                "in_distribution_count": 1,
            },
            "rows": [
                {
                    "entry_id": "m_csa:1",
                    "partition": "in_distribution",
                    "label_type": "out_of_scope",
                    "label_group": "out_of_scope",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "selected_structure_proxy_id": "pdb:1AAA",
                },
                {
                    "entry_id": "m_csa:2",
                    "partition": "heldout",
                    "label_type": "out_of_scope",
                    "label_group": "out_of_scope",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "selected_structure_proxy_id": "pdb:2BBB",
                },
                {
                    "entry_id": "m_csa:3",
                    "partition": "heldout",
                    "label_type": "seed_fingerprint",
                    "label_group": "flavin_dehydrogenase_reductase",
                    "top1_fingerprint_id": "flavin_dehydrogenase_reductase",
                    "selected_structure_proxy_id": "pdb:3CCC",
                },
            ],
        }

        artifact = audit_foldseek_tm_score_split_repair(
            target_failure=target_failure,
            sequence_holdout=sequence_holdout,
            target_failure_path="artifacts/test_target_failure.json",
            sequence_holdout_path="artifacts/test_sequence_holdout.json",
            threshold=0.7,
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_split_repair_plan")
        self.assertEqual(metadata["review_status"], "review_only_non_countable")
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertTrue(metadata["current_sequence_holdout_split_tm_score_target_blocked"])
        self.assertTrue(metadata["split_repair_required_for_target"])
        self.assertTrue(metadata["all_observed_blocking_pairs_have_repair_candidate"])
        self.assertEqual(metadata["repair_candidate_pair_count"], 1)
        self.assertEqual(metadata["manual_review_pair_count"], 0)
        self.assertEqual(metadata["proposed_moved_heldout_entry_ids"], ["m_csa:2"])
        self.assertEqual(metadata["proposed_moved_heldout_in_scope_entry_count"], 0)
        self.assertEqual(metadata["heldout_in_scope_count_before_repair"], 1)
        self.assertEqual(metadata["projected_heldout_in_scope_count_after_repair"], 1)
        self.assertEqual(metadata["projected_observed_blocking_pair_count_after_repair"], 0)
        self.assertTrue(metadata["sequence_holdout_metrics_need_regeneration_after_repair"])
        self.assertEqual(len(artifact["rows"]), 1)
        row = artifact["rows"][0]
        self.assertTrue(row["repair_candidate"])
        self.assertEqual(
            row["repair_status"],
            "repair_candidate_move_heldout_out_of_scope_entries_to_in_distribution",
        )
        self.assertEqual(row["heldout_out_of_scope_entry_ids"], ["m_csa:2"])
        self.assertEqual(row["heldout_in_scope_entry_ids"], [])
        self.assertFalse(row["countable_label_candidate"])
        self.assertFalse(row["import_ready"])

    def test_tm_score_split_repair_projection_reclassifies_existing_signal(self) -> None:
        signal = {
            "metadata": {
                "method": "foldseek_tm_score_signal",
                "slice_id": "test",
                "staged_coordinate_count": 3,
                "remaining_uncomputed_staged_coordinate_count": 0,
                "tm_score_signal_coverage_status": "partial_staged_coordinate_signal",
                "full_tm_score_split_computed": False,
                "full_tm_score_holdout_claim_blockers": [
                    "computed train/test TM-score target <0.7 is not achieved"
                ],
            },
            "rows": [
                {
                    "query_structure_key": "pdb:1AAA",
                    "target_structure_key": "pdb:2BBB",
                    "query_entry_ids": ["m_csa:1"],
                    "target_entry_ids": ["m_csa:2"],
                    "query_partitions": ["in_distribution"],
                    "target_partitions": ["heldout"],
                    "max_pair_tm_score": 0.75,
                    "train_test_pair": True,
                    "self_pair": False,
                    "line_number": 1,
                },
                {
                    "query_structure_key": "pdb:1AAA",
                    "target_structure_key": "pdb:3CCC",
                    "query_entry_ids": ["m_csa:1"],
                    "target_entry_ids": ["m_csa:3"],
                    "query_partitions": ["in_distribution"],
                    "target_partitions": ["heldout"],
                    "max_pair_tm_score": 0.62,
                    "train_test_pair": True,
                    "self_pair": False,
                    "line_number": 2,
                },
            ],
        }
        repair_plan = {
            "metadata": {
                "method": "foldseek_tm_score_split_repair_plan",
                "slice_id": "test",
                "proposed_moved_heldout_entry_ids": ["m_csa:2"],
            }
        }

        artifact = project_foldseek_tm_score_split_repair(
            signal=signal,
            repair_plan=repair_plan,
            signal_path="artifacts/test_signal.json",
            repair_plan_path="artifacts/test_repair_plan.json",
            threshold=0.7,
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "foldseek_tm_score_split_repair_projection"
        )
        self.assertEqual(metadata["source_train_test_pair_count"], 2)
        self.assertEqual(metadata["source_violating_train_test_pair_row_count"], 1)
        self.assertEqual(metadata["source_max_observed_train_test_tm_score"], 0.75)
        self.assertEqual(metadata["projected_train_test_pair_count"], 1)
        self.assertEqual(metadata["projected_violating_train_test_pair_row_count"], 0)
        self.assertEqual(metadata["projected_max_observed_train_test_tm_score"], 0.62)
        self.assertTrue(
            metadata["projected_tm_score_target_achieved_for_computed_subset"]
        )
        self.assertTrue(metadata["computed_subset_target_blocker_removed_by_projection"])
        self.assertFalse(metadata["repair_applied_to_sequence_holdout"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(len(artifact["projected_blocking_pairs"]), 0)
        self.assertEqual(len(artifact["projected_top_train_test_pairs"]), 1)
        top_pair = artifact["projected_top_train_test_pairs"][0]
        self.assertEqual(top_pair["target_entry_ids"], ["m_csa:3"])
        self.assertFalse(top_pair["violates_target_after_projection"])
        self.assertFalse(top_pair["countable_label_candidate"])
        self.assertFalse(top_pair["import_ready"])

    def test_sequence_holdout_split_repair_candidate_recomputes_partition_metrics(
        self,
    ) -> None:
        sequence_holdout = {
            "metadata": {
                "method": "sequence_fold_distance_holdout_evaluation",
                "slice_id": "test",
                "sequence_identity_target_achieved": True,
            },
            "rows": [
                {
                    "entry_id": "m_csa:1",
                    "partition": "in_distribution",
                    "label_type": "out_of_scope",
                    "abstained": True,
                    "real_sequence_identity_cluster_id": "cluster:1",
                },
                {
                    "entry_id": "m_csa:2",
                    "partition": "heldout",
                    "label_type": "out_of_scope",
                    "abstained": True,
                    "real_sequence_identity_cluster_id": "cluster:2",
                },
                {
                    "entry_id": "m_csa:3",
                    "partition": "heldout",
                    "label_type": "seed_fingerprint",
                    "abstained": False,
                    "top1_correct": True,
                    "top3_correct": True,
                    "real_sequence_identity_cluster_id": "cluster:3",
                },
            ],
        }
        repair_plan = {
            "metadata": {
                "method": "foldseek_tm_score_split_repair_plan",
                "slice_id": "test",
                "proposed_moved_heldout_entry_ids": ["m_csa:2"],
            }
        }
        projection = {
            "metadata": {
                "method": "foldseek_tm_score_split_repair_projection",
                "projected_tm_score_target_achieved_for_computed_subset": True,
                "projected_max_observed_train_test_tm_score": 0.62,
                "projected_violating_train_test_pair_row_count": 0,
            }
        }

        artifact = build_sequence_distance_holdout_split_repair_candidate(
            sequence_holdout=sequence_holdout,
            repair_plan=repair_plan,
            projection=projection,
            sequence_holdout_path="artifacts/test_sequence_holdout.json",
            repair_plan_path="artifacts/test_repair_plan.json",
            projection_path="artifacts/test_projection.json",
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "sequence_distance_holdout_split_repair_candidate"
        )
        self.assertEqual(metadata["source_heldout_count"], 2)
        self.assertEqual(metadata["repaired_heldout_count"], 1)
        self.assertEqual(metadata["source_heldout_in_scope_count"], 1)
        self.assertEqual(metadata["repaired_heldout_in_scope_count"], 1)
        self.assertEqual(
            metadata["repaired_heldout_out_of_scope_false_non_abstention_count"], 0
        )
        self.assertTrue(metadata["repair_candidate_applied"])
        self.assertEqual(metadata["applied_moved_heldout_entry_ids"], ["m_csa:2"])
        self.assertEqual(
            metadata["remaining_heldout_sequence_identity_cluster_overlap_count"], 0
        )
        self.assertTrue(
            metadata["sequence_identity_target_preserved_by_cluster_partition"]
        )
        self.assertFalse(metadata["real_sequence_identity_recomputed"])
        self.assertFalse(metadata["canonical_holdout_replaced"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        moved = [row for row in artifact["rows"] if row["entry_id"] == "m_csa:2"][0]
        self.assertEqual(moved["source_partition"], "heldout")
        self.assertEqual(moved["partition"], "in_distribution")
        self.assertTrue(moved["split_repair_applied_to_candidate"])

    def test_current_1000_foldseek_tm_score_signal_artifact_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_staged25.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_signal")
        self.assertEqual(metadata["staged_coordinate_count"], 25)
        self.assertEqual(metadata["pair_count"], 1840)
        self.assertEqual(metadata["mapped_pair_count"], 1840)
        self.assertEqual(metadata["train_test_pair_count"], 532)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.6426)
        self.assertTrue(metadata["partial_tm_score_signal_computed"])
        self.assertTrue(metadata["partial_real_tm_score_signal_computed"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["review_status"], "review_only_non_countable")
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["raw_name_mapping_unmapped_count"], 0)
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in artifact["rows"])
        )
        self.assertTrue(all(not row["import_ready"] for row in artifact["rows"]))

    def test_expanded_1000_foldseek_coordinate_readiness_artifact_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_coordinate_readiness_1000_expanded100.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_coordinate_readiness")
        self.assertEqual(metadata["coordinate_fetch_cap"], 100)
        self.assertEqual(metadata["materialized_coordinate_count"], 100)
        self.assertEqual(metadata["coordinate_materialization_possible_count"], 676)
        self.assertEqual(metadata["missing_or_unsupported_structure_count"], 2)
        self.assertEqual(metadata["fetch_failure_count"], 0)
        self.assertEqual(metadata["not_materialized_structure_count"], 572)
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["foldseek_version"], "10.941cd33")

    def test_all_materializable_1000_foldseek_readiness_artifact_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_coordinate_readiness")
        self.assertEqual(metadata["coordinate_fetch_cap"], 676)
        self.assertFalse(metadata["coordinate_fetch_cap_applied"])
        self.assertEqual(metadata["selected_structure_count"], 672)
        self.assertEqual(metadata["coordinate_materialization_possible_count"], 676)
        self.assertEqual(metadata["materialized_coordinate_count"], 672)
        self.assertEqual(metadata["staged_coordinate_count"], 672)
        self.assertEqual(metadata["missing_or_unsupported_structure_count"], 2)
        self.assertEqual(metadata["tm_score_coordinate_exclusion_count"], 2)
        self.assertEqual(metadata["fetch_failure_count"], 0)
        self.assertEqual(metadata["not_materialized_structure_count"], 0)
        self.assertIn("all currently materializable", metadata["blocker_removed"])
        self.assertIn(
            "evaluated rows without supported selected structures are explicitly "
            "excluded from Foldseek coordinate materialization",
            metadata["blockers_remaining"],
        )
        self.assertEqual(
            {
                row["entry_id"]: row["tm_score_coordinate_exclusion_reason"]
                for row in metadata["tm_score_coordinate_exclusions"]
            },
            {
                "m_csa:372": "missing_selected_coordinate_structure",
                "m_csa:501": "missing_selected_coordinate_structure",
            },
        )
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertIsNone(metadata["max_observed_train_test_tm_score"])
        self.assertFalse(metadata["max_observed_train_test_tm_score_computable"])
        self.assertEqual(metadata["train_test_pair_count"], 0)
        self.assertEqual(metadata["raw_name_mapping_unmapped_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertEqual(metadata["foldseek_version"], "10.941cd33")
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in artifact["rows"])
        )
        self.assertTrue(all(not row["import_ready"] for row in artifact["rows"]))

    def test_expanded_40_foldseek_tm_score_completed_partial_artifact_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_expanded40.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_signal")
        self.assertEqual(metadata["available_staged_coordinate_count"], 100)
        self.assertEqual(metadata["staged_coordinate_count"], 40)
        self.assertEqual(metadata["tm_signal_coordinate_cap_requested"], 40)
        self.assertTrue(metadata["tm_signal_coordinate_cap_applied"])
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertEqual(metadata["foldseek_version"], "10.941cd33")
        self.assertEqual(metadata["pair_count"], 5699)
        self.assertEqual(metadata["mapped_pair_count"], 5699)
        self.assertEqual(metadata["heldout_pair_count"], 183)
        self.assertEqual(metadata["heldout_in_distribution_pair_count"], 1633)
        self.assertEqual(metadata["train_test_pair_count"], 1633)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.7515)
        self.assertTrue(metadata["max_observed_train_test_tm_score_computable"])
        self.assertEqual(metadata["threshold_target"], "<0.7")
        self.assertFalse(metadata["tm_score_target_achieved_for_computed_subset"])
        self.assertGreater(metadata["max_observed_train_test_tm_score"], 0.7)
        self.assertTrue(metadata["partial_tm_score_signal_computed"])
        self.assertTrue(metadata["partial_real_tm_score_signal_computed"])
        self.assertIn("selected_coordinates", metadata["foldseek_command"])
        self.assertEqual(metadata["raw_name_mapping_unmapped_count"], 0)
        self.assertEqual(metadata["raw_name_mapping_unmapped_names"], [])
        self.assertIn("previous expanded25 partial-signal ceiling", metadata["blocker_removed"])
        self.assertEqual(metadata["prior_staged_coordinate_count"], 25)
        self.assertTrue(metadata["staged_coordinate_count_exceeds_prior"])
        self.assertEqual(
            metadata["tm_score_signal_coverage_status"],
            "partial_staged_coordinate_signal",
        )
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertIn(
            "computed train/test TM-score target <0.7 is not achieved",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertIn(
            "evaluated selected-coordinate coverage is partial",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertEqual(metadata["remaining_to_full_signal_structure_count"], 632)
        self.assertEqual(metadata["remaining_uncomputed_staged_coordinate_count"], 60)
        self.assertIsNone(metadata["blocker_not_removed"])
        self.assertIn(
            "partial staged-coordinate Foldseek signal only; it is not a full accepted-registry TM-score holdout",
            metadata["limitations"],
        )
        self.assertIn(
            "full evaluated-coordinate coverage is absent; full TM-score split remains blocked",
            metadata["limitations"],
        )
        self.assertIn(
            "review-only artifact; it creates no countable labels and no import-ready rows",
            metadata["limitations"],
        )
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["review_status"], "review_only_non_countable")
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in artifact["rows"])
        )
        self.assertTrue(all(not row["import_ready"] for row in artifact["rows"]))

    def test_expanded_60_foldseek_tm_score_completed_partial_artifact_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_expanded60.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_signal")
        self.assertEqual(metadata["available_staged_coordinate_count"], 672)
        self.assertEqual(metadata["staged_coordinate_count"], 60)
        self.assertEqual(metadata["tm_signal_coordinate_cap_requested"], 60)
        self.assertTrue(metadata["tm_signal_coordinate_cap_applied"])
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertEqual(metadata["foldseek_version"], "10.941cd33")
        self.assertEqual(metadata["pair_count"], 12329)
        self.assertEqual(metadata["mapped_pair_count"], 12329)
        self.assertEqual(metadata["heldout_pair_count"], 457)
        self.assertEqual(metadata["heldout_in_distribution_pair_count"], 3716)
        self.assertEqual(metadata["train_test_pair_count"], 3716)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.7515)
        self.assertFalse(metadata["tm_score_target_achieved_for_computed_subset"])
        self.assertGreater(metadata["max_observed_train_test_tm_score"], 0.7)
        self.assertTrue(metadata["partial_tm_score_signal_computed"])
        self.assertTrue(metadata["partial_real_tm_score_signal_computed"])
        self.assertEqual(metadata["raw_name_mapping_unmapped_count"], 0)
        self.assertIn("previous expanded40 partial-signal ceiling", metadata["blocker_removed"])
        self.assertEqual(metadata["prior_staged_coordinate_count"], 40)
        self.assertTrue(metadata["staged_coordinate_count_exceeds_prior"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertEqual(metadata["remaining_to_full_signal_structure_count"], 612)
        self.assertEqual(metadata["remaining_uncomputed_staged_coordinate_count"], 612)
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["review_status"], "review_only_non_countable")
        self.assertIn(
            "computed train/test TM-score target <0.7 is not achieved",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertIn(
            "available staged coordinates were excluded by the signal cap",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in artifact["rows"])
        )
        self.assertTrue(all(not row["import_ready"] for row in artifact["rows"]))

    def test_expanded_80_foldseek_tm_score_completed_partial_artifact_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_expanded80.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_signal")
        self.assertEqual(metadata["available_staged_coordinate_count"], 672)
        self.assertEqual(metadata["staged_coordinate_count"], 80)
        self.assertEqual(metadata["tm_signal_coordinate_cap_requested"], 80)
        self.assertTrue(metadata["tm_signal_coordinate_cap_applied"])
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertEqual(metadata["foldseek_version"], "10.941cd33")
        self.assertEqual(metadata["pair_count"], 18591)
        self.assertEqual(metadata["mapped_pair_count"], 18591)
        self.assertEqual(metadata["heldout_pair_count"], 827)
        self.assertEqual(metadata["heldout_in_distribution_pair_count"], 5666)
        self.assertEqual(metadata["train_test_pair_count"], 5666)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.7515)
        self.assertFalse(metadata["tm_score_target_achieved_for_computed_subset"])
        self.assertGreater(metadata["max_observed_train_test_tm_score"], 0.7)
        self.assertTrue(metadata["partial_tm_score_signal_computed"])
        self.assertTrue(metadata["partial_real_tm_score_signal_computed"])
        self.assertEqual(metadata["raw_name_mapping_unmapped_count"], 0)
        self.assertIn(
            "previous expanded60 partial-signal ceiling",
            metadata["blocker_removed"],
        )
        self.assertEqual(metadata["prior_staged_coordinate_count"], 60)
        self.assertTrue(metadata["staged_coordinate_count_exceeds_prior"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertEqual(metadata["remaining_to_full_signal_structure_count"], 592)
        self.assertEqual(metadata["remaining_uncomputed_staged_coordinate_count"], 592)
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["review_status"], "review_only_non_countable")
        self.assertIn(
            "computed train/test TM-score target <0.7 is not achieved",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertIn(
            "available staged coordinates were excluded by the signal cap",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in artifact["rows"])
        )
        self.assertTrue(all(not row["import_ready"] for row in artifact["rows"]))

    def test_expanded_100_foldseek_tm_score_completed_partial_artifact_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_expanded100.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_signal")
        self.assertEqual(metadata["available_staged_coordinate_count"], 672)
        self.assertEqual(metadata["staged_coordinate_count"], 100)
        self.assertEqual(metadata["tm_signal_coordinate_cap_requested"], 100)
        self.assertTrue(metadata["tm_signal_coordinate_cap_applied"])
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertEqual(metadata["foldseek_version"], "10.941cd33")
        self.assertEqual(metadata["pair_count"], 27542)
        self.assertEqual(metadata["mapped_pair_count"], 27542)
        self.assertEqual(metadata["heldout_pair_count"], 838)
        self.assertEqual(metadata["heldout_in_distribution_pair_count"], 7317)
        self.assertEqual(metadata["train_test_pair_count"], 7317)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.7515)
        self.assertFalse(metadata["tm_score_target_achieved_for_computed_subset"])
        self.assertGreater(metadata["max_observed_train_test_tm_score"], 0.7)
        self.assertTrue(metadata["partial_tm_score_signal_computed"])
        self.assertTrue(metadata["partial_real_tm_score_signal_computed"])
        self.assertEqual(metadata["raw_name_mapping_unmapped_count"], 0)
        self.assertIn(
            "previous expanded80 partial-signal ceiling",
            metadata["blocker_removed"],
        )
        self.assertEqual(metadata["prior_staged_coordinate_count"], 80)
        self.assertTrue(metadata["staged_coordinate_count_exceeds_prior"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertEqual(metadata["remaining_to_full_signal_structure_count"], 572)
        self.assertEqual(metadata["remaining_uncomputed_staged_coordinate_count"], 572)
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["review_status"], "review_only_non_countable")
        self.assertIn(
            "computed train/test TM-score target <0.7 is not achieved",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertIn(
            "available staged coordinates were excluded by the signal cap",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in artifact["rows"])
        )
        self.assertTrue(all(not row["import_ready"] for row in artifact["rows"]))

    def test_current_foldseek_target_failure_audit_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_target_failure_audit_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "foldseek_tm_score_target_failure_audit"
        )
        self.assertEqual(metadata["source_signal_staged_coordinate_count"], 100)
        self.assertEqual(
            metadata["source_signal_remaining_uncomputed_staged_coordinate_count"],
            572,
        )
        self.assertEqual(metadata["source_signal_foldseek_version"], "10.941cd33")
        self.assertEqual(metadata["train_test_pair_count"], 7317)
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 48)
        self.assertEqual(metadata["violating_unique_structure_pair_count"], 1)
        self.assertEqual(metadata["violating_unique_entry_pair_count"], 1)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.7515)
        self.assertTrue(
            metadata["current_sequence_holdout_split_tm_score_target_blocked"]
        )
        self.assertTrue(metadata["split_repair_required_for_target"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertIn(
            "computed train/test TM-score target <0.7 is already violated in the computed subset",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertEqual(len(artifact["blocking_pairs"]), 1)
        pair = artifact["blocking_pairs"][0]
        self.assertEqual(pair["query_entry_ids"], ["m_csa:33"])
        self.assertEqual(pair["target_entry_ids"], ["m_csa:34"])
        self.assertEqual(pair["query_structure_key"], "pdb:1JC5")
        self.assertEqual(pair["target_structure_key"], "pdb:1MPY")
        self.assertEqual(pair["max_pair_tm_score"], 0.7515)
        self.assertTrue(pair["violates_target"])
        self.assertFalse(pair["countable_label_candidate"])
        self.assertFalse(pair["import_ready"])

    def test_current_foldseek_split_repair_plan_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_split_repair_plan_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_split_repair_plan")
        self.assertEqual(metadata["observed_blocking_pair_count"], 1)
        self.assertEqual(metadata["repair_candidate_pair_count"], 1)
        self.assertEqual(metadata["manual_review_pair_count"], 0)
        self.assertTrue(metadata["all_observed_blocking_pairs_have_repair_candidate"])
        self.assertEqual(
            metadata["projected_observed_blocking_pair_count_after_repair"], 0
        )
        self.assertEqual(metadata["proposed_moved_heldout_entry_ids"], ["m_csa:34"])
        self.assertEqual(metadata["proposed_moved_heldout_in_scope_entry_count"], 0)
        self.assertEqual(metadata["heldout_count_before_repair"], 136)
        self.assertEqual(metadata["projected_heldout_count_after_repair"], 135)
        self.assertEqual(metadata["heldout_in_scope_count_before_repair"], 44)
        self.assertEqual(metadata["projected_heldout_in_scope_count_after_repair"], 44)
        self.assertTrue(metadata["sequence_holdout_metrics_need_regeneration_after_repair"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(len(artifact["rows"]), 1)
        row = artifact["rows"][0]
        self.assertEqual(row["blocking_pair_id"], "m_csa:33|m_csa:34")
        self.assertEqual(row["query_structure_key"], "pdb:1JC5")
        self.assertEqual(row["target_structure_key"], "pdb:1MPY")
        self.assertEqual(row["heldout_out_of_scope_entry_ids"], ["m_csa:34"])
        self.assertEqual(row["heldout_in_scope_entry_ids"], [])
        self.assertTrue(row["repair_candidate"])
        self.assertFalse(row["countable_label_candidate"])
        self.assertFalse(row["import_ready"])

    def test_current_foldseek_split_repair_projection_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_split_repair_projection_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "foldseek_tm_score_split_repair_projection"
        )
        self.assertEqual(metadata["source_train_test_pair_count"], 7317)
        self.assertEqual(metadata["source_violating_train_test_pair_row_count"], 48)
        self.assertEqual(metadata["source_max_observed_train_test_tm_score"], 0.7515)
        self.assertEqual(metadata["projected_train_test_pair_count"], 6930)
        self.assertEqual(metadata["projected_violating_train_test_pair_row_count"], 0)
        self.assertEqual(metadata["projected_max_observed_train_test_tm_score"], 0.6993)
        self.assertTrue(
            metadata["projected_tm_score_target_achieved_for_computed_subset"]
        )
        self.assertTrue(metadata["computed_subset_target_blocker_removed_by_projection"])
        self.assertEqual(metadata["proposed_moved_heldout_entry_ids"], ["m_csa:34"])
        self.assertFalse(metadata["repair_applied_to_sequence_holdout"])
        self.assertFalse(metadata["sequence_holdout_metrics_regenerated"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(len(artifact["projected_blocking_pairs"]), 0)
        self.assertEqual(len(artifact["projected_top_train_test_pairs"]), 20)
        top_pair = artifact["projected_top_train_test_pairs"][0]
        self.assertEqual(top_pair["query_entry_ids"], ["m_csa:45"])
        self.assertEqual(top_pair["target_entry_ids"], ["m_csa:54"])
        self.assertEqual(top_pair["max_pair_tm_score"], 0.6993)
        self.assertFalse(top_pair["violates_target_after_projection"])
        self.assertFalse(top_pair["countable_label_candidate"])
        self.assertFalse(top_pair["import_ready"])

    def test_current_sequence_holdout_split_repair_candidate_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_sequence_distance_holdout_split_repair_candidate_1000.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "sequence_distance_holdout_split_repair_candidate"
        )
        self.assertTrue(metadata["repair_candidate_applied"])
        self.assertEqual(metadata["applied_moved_heldout_entry_ids"], ["m_csa:34"])
        self.assertEqual(metadata["source_heldout_count"], 136)
        self.assertEqual(metadata["repaired_heldout_count"], 135)
        self.assertEqual(metadata["source_in_distribution_count"], 542)
        self.assertEqual(metadata["repaired_in_distribution_count"], 543)
        self.assertEqual(metadata["source_heldout_in_scope_count"], 44)
        self.assertEqual(metadata["repaired_heldout_in_scope_count"], 44)
        self.assertEqual(metadata["source_heldout_out_of_scope_count"], 92)
        self.assertEqual(metadata["repaired_heldout_out_of_scope_count"], 91)
        self.assertEqual(
            metadata["repaired_heldout_out_of_scope_false_non_abstention_count"], 0
        )
        self.assertEqual(metadata["remaining_heldout_sequence_identity_cluster_overlap_count"], 0)
        self.assertTrue(
            metadata["sequence_identity_target_preserved_by_cluster_partition"]
        )
        self.assertFalse(metadata["real_sequence_identity_recomputed"])
        self.assertEqual(metadata["foldseek_projection_max_train_test_tm_score"], 0.6993)
        self.assertEqual(
            metadata["foldseek_projection_violating_train_test_pair_row_count"], 0
        )
        self.assertFalse(metadata["canonical_holdout_replaced"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        moved_rows = [
            row
            for row in artifact["rows"]
            if row.get("split_repair_applied_to_candidate")
        ]
        self.assertEqual(len(moved_rows), 1)
        self.assertEqual(moved_rows[0]["entry_id"], "m_csa:34")
        self.assertEqual(moved_rows[0]["source_partition"], "heldout")
        self.assertEqual(moved_rows[0]["partition"], "in_distribution")

    def test_current_foldseek_split_repair_candidate_readiness_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_coordinate_readiness")
        self.assertEqual(metadata["sequence_holdout_row_count"], 678)
        self.assertEqual(metadata["coordinate_fetch_cap"], 676)
        self.assertFalse(metadata["coordinate_fetch_cap_applied"])
        self.assertEqual(metadata["selected_structure_count"], 672)
        self.assertEqual(metadata["materialized_coordinate_count"], 672)
        self.assertEqual(metadata["missing_or_unsupported_structure_count"], 2)
        self.assertEqual(metadata["fetch_failure_count"], 0)
        self.assertEqual(metadata["not_materialized_structure_count"], 0)
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        rows_by_entry = {row["entry_id"]: row for row in artifact["rows"]}
        self.assertEqual(
            rows_by_entry["m_csa:34"]["sequence_holdout_partition"],
            "in_distribution",
        )
        self.assertEqual(
            rows_by_entry["m_csa:34"]["coordinate_materialization_status"],
            "already_materialized",
        )

    def test_current_repaired_foldseek_signal_expanded100_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_expanded100.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(metadata["method"], "foldseek_tm_score_signal")
        self.assertEqual(
            metadata["readiness_artifact"],
            "artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json",
        )
        self.assertEqual(metadata["available_staged_coordinate_count"], 672)
        self.assertEqual(metadata["staged_coordinate_count"], 100)
        self.assertEqual(metadata["tm_signal_coordinate_cap_requested"], 100)
        self.assertTrue(metadata["tm_signal_coordinate_cap_applied"])
        self.assertEqual(metadata["foldseek_run_status"], "completed")
        self.assertEqual(metadata["foldseek_version"], "10.941cd33")
        self.assertEqual(metadata["pair_count"], 27542)
        self.assertEqual(metadata["mapped_pair_count"], 27542)
        self.assertEqual(metadata["heldout_pair_count"], 646)
        self.assertEqual(metadata["heldout_in_distribution_pair_count"], 6930)
        self.assertEqual(metadata["train_test_pair_count"], 6930)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.6993)
        self.assertTrue(metadata["tm_score_target_achieved_for_computed_subset"])
        self.assertLess(metadata["max_observed_train_test_tm_score"], 0.7)
        self.assertEqual(metadata["raw_name_mapping_unmapped_count"], 0)
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertEqual(metadata["remaining_uncomputed_staged_coordinate_count"], 572)
        self.assertNotIn(
            "computed train/test TM-score target <0.7 is not achieved",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertIn(
            "available staged coordinates were excluded by the signal cap",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in artifact["rows"])
        )
        self.assertTrue(all(not row["import_ready"] for row in artifact["rows"]))

    def test_current_repaired_foldseek_target_audit_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_target_failure_audit_1000_split_repair_candidate_expanded100.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "foldseek_tm_score_target_failure_audit"
        )
        self.assertEqual(metadata["source_signal_staged_coordinate_count"], 100)
        self.assertEqual(
            metadata["source_signal_artifact"],
            "artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_expanded100.json",
        )
        self.assertEqual(metadata["train_test_pair_count"], 6930)
        self.assertEqual(metadata["violating_train_test_pair_row_count"], 0)
        self.assertEqual(metadata["violating_unique_structure_pair_count"], 0)
        self.assertEqual(metadata["violating_unique_entry_pair_count"], 0)
        self.assertEqual(metadata["max_observed_train_test_tm_score"], 0.6993)
        self.assertTrue(metadata["tm_score_target_achieved_for_computed_subset"])
        self.assertFalse(
            metadata["current_sequence_holdout_split_tm_score_target_blocked"]
        )
        self.assertFalse(metadata["split_repair_required_for_target"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(artifact["blocking_pairs"], [])

    def test_current_all_materializable_foldseek_attempt_is_pinned(self) -> None:
        artifact = _load_artifact(
            "artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json"
        )
        metadata = artifact["metadata"]

        self.assertEqual(
            metadata["method"], "foldseek_tm_score_all_materializable_signal"
        )
        self.assertEqual(metadata["foldseek_run_status"], "foldseek_run_timeout")
        self.assertEqual(metadata["foldseek_version"], "10.941cd33")
        self.assertEqual(metadata["foldseek_threads"], 4)
        self.assertEqual(metadata["foldseek_max_runtime_seconds"], 1500)
        self.assertEqual(metadata["available_staged_coordinate_count"], 672)
        self.assertEqual(metadata["staged_coordinate_count"], 672)
        self.assertTrue(metadata["all_materializable_coordinate_coverage"])
        self.assertFalse(metadata["full_evaluated_coordinate_coverage"])
        self.assertEqual(metadata["missing_or_unsupported_structure_count"], 2)
        self.assertEqual(
            [item["entry_id"] for item in metadata["tm_score_coordinate_exclusions"]],
            ["m_csa:372", "m_csa:501"],
        )
        self.assertEqual(metadata["pair_count"], 0)
        self.assertEqual(metadata["train_test_pair_count"], 0)
        self.assertFalse(metadata["tm_score_split_computed"])
        self.assertFalse(metadata["all_materializable_tm_score_split_computed"])
        self.assertFalse(metadata["full_tm_score_split_computed"])
        self.assertFalse(metadata["full_tm_score_holdout_claim_permitted"])
        self.assertEqual(metadata["countable_label_count"], 0)
        self.assertEqual(metadata["import_ready_row_count"], 0)
        self.assertIn(
            "Foldseek all-materializable signal did not complete with pair rows",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertIn(
            "one or more evaluated rows lacks a supported selected structure",
            metadata["full_tm_score_holdout_claim_blockers"],
        )
        self.assertEqual(artifact["top_train_test_pairs"], [])
        self.assertEqual(artifact["blocking_pairs"], [])


def _result(
    entry_id: str,
    top1: str,
    score: float,
    *,
    second: str | None = None,
    pdb_id: str | None = None,
) -> dict[str, object]:
    top_fingerprints = [{"fingerprint_id": top1, "score": score}]
    if second:
        top_fingerprints.append({"fingerprint_id": second, "score": max(score - 0.1, 0.0)})
    return {
        "entry_id": entry_id,
        "entry_name": entry_id,
        "pdb_id": pdb_id or entry_id.replace("m_csa:", "") + "XYZ",
        "resolved_residue_count": 3,
        "residue_codes": ["SER", "HIS", "ASP"],
        "status": "ok",
        "top_fingerprints": top_fingerprints,
    }


def _tm_signal_readiness(
    *,
    first_coordinate_path: str,
    second_coordinate_path: str,
) -> dict[str, object]:
    return {
        "metadata": {
            "method": "foldseek_coordinate_readiness",
            "slice_id": "test",
            "evaluated_count": 3,
            "selected_structure_count": 3,
            "missing_or_unsupported_structure_count": 0,
            "fetch_failure_count": 0,
            "tm_score_split_computed": False,
            "ready_for_label_import": False,
            "countable_label_candidate_count": 0,
        },
        "structures": [
            {
                "structure_key": "pdb:1AAA",
                "source": "pdb",
                "structure_id": "1AAA",
                "entry_ids": ["m_csa:1"],
                "coordinate_path": first_coordinate_path,
                "fetch_status": "already_materialized",
            },
            {
                "structure_key": "pdb:2BBB",
                "source": "pdb",
                "structure_id": "2BBB",
                "entry_ids": ["m_csa:2"],
                "coordinate_path": second_coordinate_path,
                "fetch_status": "already_materialized",
            },
            {
                "structure_key": "pdb:3CCC",
                "source": "pdb",
                "structure_id": "3CCC",
                "entry_ids": ["m_csa:3"],
                "coordinate_path": None,
                "fetch_status": "not_requested_fetch_cap_reached",
            },
        ],
        "rows": [
            {
                "entry_id": "m_csa:1",
                "selected_structure_key": "pdb:1AAA",
                "sequence_holdout_partition": "heldout",
                "countable_label_candidate": False,
                "import_ready": False,
            },
            {
                "entry_id": "m_csa:2",
                "selected_structure_key": "pdb:2BBB",
                "sequence_holdout_partition": "in_distribution",
                "countable_label_candidate": False,
                "import_ready": False,
            },
            {
                "entry_id": "m_csa:3",
                "selected_structure_key": "pdb:3CCC",
                "sequence_holdout_partition": "in_distribution",
                "countable_label_candidate": False,
                "import_ready": False,
            },
        ],
    }


def _load_artifact(path: str) -> dict[str, object]:
    with (ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
