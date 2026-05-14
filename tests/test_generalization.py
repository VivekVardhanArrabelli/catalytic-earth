import json
import shutil
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.generalization import (
    build_foldseek_coordinate_readiness,
    build_foldseek_tm_score_signal,
    build_sequence_distance_holdout_eval,
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
        self.assertEqual(metadata["import_ready_candidate_count"], 0)
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
            "selected structures remain outside the computed signal",
            metadata["full_tm_score_holdout_claim_blockers"],
        )

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
