from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.pymol_review import (
    build_mcsa_pymol_expert_review_queue,
    build_mcsa_pymol_remaining_blocker_report,
    launch_mcsa_pymol_review,
    materialize_mcsa_pymol_structure_tranche,
    select_mcsa_pymol_materialization_tranche,
    validate_mcsa_pymol_decision_batch,
    write_mcsa_pymol_scripts,
)


class PyMOLReviewTests(unittest.TestCase):
    def test_queue_builds_ready_and_blocked_rows_without_guessing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            structure_dir = Path(tmp)
            (structure_dir / "pdb_1ABC.cif").write_text(
                _structure_cif(), encoding="utf-8"
            )
            queue = build_mcsa_pymol_expert_review_queue(
                expert_review_export=_review_export(),
                review_debt_summary=_review_debt(),
                review_evidence_gaps=_evidence_gaps(),
                geometry_features=_geometry_features(),
                structure_dirs=[structure_dir],
                source_paths={"expert_review_export": "review.json"},
            )

        self.assertEqual(queue["metadata"]["total_review_rows_scanned"], 2)
        self.assertEqual(queue["metadata"]["pymol_ready_count"], 1)
        ready, blocked = queue["rows"]
        self.assertTrue(ready["pymol_ready"])
        self.assertTrue(ready["focus_atom_selection_verified"])
        self.assertFalse(ready["countable_import_ready"])
        self.assertEqual(ready["focus_atom_pair"]["left"]["atom_name"], "CA")
        self.assertEqual(ready["exact_measured_distance_angstrom"], 7.2)
        self.assertFalse(blocked["pymol_ready"])
        self.assertIn("missing_structure_path", blocked["missing_fields"])
        self.assertIn("missing_exact_ca_atom_pair", blocked["missing_fields"])

    def test_pml_generation_writes_focused_scene_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            structure_dir = root / "structures"
            structure_dir.mkdir()
            (structure_dir / "pdb_1ABC.cif").write_text(
                _structure_cif(), encoding="utf-8"
            )
            queue = build_mcsa_pymol_expert_review_queue(
                expert_review_export=_review_export(max_items=1),
                review_debt_summary=_review_debt(),
                review_evidence_gaps=_evidence_gaps(),
                geometry_features=_geometry_features(),
                structure_dirs=[structure_dir],
            )
            manifest = write_mcsa_pymol_scripts(queue, out_dir=root / "pml")
            script = Path(manifest["rows"][0]["pml_script_path"]).read_text(
                encoding="utf-8"
            )

        self.assertIn('load "', script)
        self.assertIn("select m_csa_1_left", script)
        self.assertIn("distance m_csa_1_distance", script)
        self.assertIn('label m_csa_1_distance, "7.200 A"', script)
        self.assertIn("zoom m_csa_1_left or m_csa_1_right, 8", script)

    def test_dry_run_launcher_writes_parseable_non_countable_batch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            structure_dir = root / "structures"
            structure_dir.mkdir()
            (structure_dir / "pdb_1ABC.cif").write_text(
                _structure_cif(), encoding="utf-8"
            )
            queue = build_mcsa_pymol_expert_review_queue(
                expert_review_export=_review_export(max_items=1),
                review_debt_summary=_review_debt(),
                review_evidence_gaps=_evidence_gaps(),
                geometry_features=_geometry_features(),
                structure_dirs=[structure_dir],
            )
            write_mcsa_pymol_scripts(queue, out_dir=root / "pml")
            out = root / "manual_batch.json"
            batch = launch_mcsa_pymol_review(
                queue=queue,
                out_path=out,
                reviewer="tester",
                dry_run=True,
                no_launch=True,
                max_rows=1,
            )
            validation = validate_mcsa_pymol_decision_batch(batch)
            persisted = json.loads(out.read_text(encoding="utf-8"))

        self.assertEqual(batch["metadata"]["review_item_count"], 1)
        self.assertEqual(batch["review_items"][0]["decision"], "skipped")
        self.assertFalse(batch["review_items"][0]["countable_import_ready"])
        self.assertEqual(validation["metadata"]["countable_import_ready_count"], 0)
        self.assertEqual(persisted["metadata"]["decision_counts"], {"skipped": 1})

    def test_launcher_fails_closed_when_pymol_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            structure_dir = root / "structures"
            structure_dir.mkdir()
            (structure_dir / "pdb_1ABC.cif").write_text(
                _structure_cif(), encoding="utf-8"
            )
            queue = build_mcsa_pymol_expert_review_queue(
                expert_review_export=_review_export(max_items=1),
                review_debt_summary=_review_debt(),
                review_evidence_gaps=_evidence_gaps(),
                geometry_features=_geometry_features(),
                structure_dirs=[structure_dir],
            )

            with self.assertRaisesRegex(RuntimeError, "PyMOL executable not found"):
                launch_mcsa_pymol_review(
                    queue=queue,
                    out_path=root / "manual_batch.json",
                    reviewer="tester",
                    pymol_bin="definitely-not-pymol",
                )

    def test_queue_fails_closed_when_structure_atom_selection_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            structure_dir = Path(tmp)
            (structure_dir / "pdb_1ABC.cif").write_text("data_1ABC\n", encoding="utf-8")
            queue = build_mcsa_pymol_expert_review_queue(
                expert_review_export=_review_export(max_items=1),
                review_debt_summary=_review_debt(),
                review_evidence_gaps=_evidence_gaps(),
                geometry_features=_geometry_features(),
                structure_dirs=[structure_dir],
            )

        row = queue["rows"][0]
        self.assertFalse(row["pymol_ready"])
        self.assertFalse(row["focus_atom_selection_verified"])
        self.assertIn("missing_left_structure_atom", row["missing_fields"])
        self.assertIn("missing_right_structure_atom", row["missing_fields"])

    def test_remaining_blocker_report_selects_only_structure_path_gaps(self) -> None:
        queue = build_mcsa_pymol_expert_review_queue(
            expert_review_export=_review_export(),
            review_debt_summary=_review_debt(),
            review_evidence_gaps=_evidence_gaps(),
            geometry_features=_geometry_features(),
            structure_dirs=[],
        )
        report = build_mcsa_pymol_remaining_blocker_report(
            queue=queue,
            source_queue_path="queue.json",
            max_next_tranche_rows=1,
            tranche_id="unit",
        )
        selection = select_mcsa_pymol_materialization_tranche(
            blocker_report=report,
            max_rows=1,
            tranche_id="unit",
            source_blocker_report_path="blockers.json",
        )

        self.assertEqual(report["metadata"]["next_tranche_candidate_count"], 1)
        self.assertEqual(
            report["next_structure_materialization_candidates"][0]["entry_id"],
            "m_csa:1",
        )
        self.assertEqual(
            report["exact_atom_pair_mapping_blockers_sample"][0]["entry_id"],
            "m_csa:2",
        )
        self.assertEqual(selection["metadata"]["selected_row_count"], 1)
        self.assertFalse(selection["metadata"]["ready_for_label_import"])
        self.assertEqual(selection["rows"][0]["structure_id"], "1ABC")

    def test_structure_tranche_materialization_is_review_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "coords"
            materialization = materialize_mcsa_pymol_structure_tranche(
                selection={
                    "rows": [
                        {
                            "entry_id": "m_csa:1",
                            "entry_name": "alpha testase",
                            "structure_id": "1ABC",
                            "rank": 1,
                            "missing_fields": ["missing_structure_path"],
                        }
                    ]
                },
                coordinate_output_dir=out_dir,
                source_selection_artifact="selection.json",
                tranche_id="unit",
                fetcher=lambda _url: b"data_1ABC   \n#   \n",
            )

            row = materialization["rows"][0]
            structure_path = Path(row["local_structure_path"])
            materialized_bytes = structure_path.read_bytes()
        self.assertEqual(materialization["metadata"]["materialized_count"], 1)
        self.assertEqual(materialization["metadata"]["failed_count"], 0)
        self.assertFalse(materialization["metadata"]["ready_for_label_import"])
        self.assertFalse(materialization["metadata"]["removal_allowed"])
        self.assertEqual(
            materialization["metadata"]["coordinate_normalization"],
            "utf8_line_trailing_whitespace_stripped_lf",
        )
        self.assertEqual(row["materialization_status"], "materialized")
        self.assertTrue(row["coordinate_normalized"])
        self.assertEqual(materialized_bytes, b"data_1ABC\n#\n")
        self.assertEqual(len(row["sha256"]), 64)
        self.assertEqual(row["first_line"], "data_1ABC")


def _review_export(max_items: int | None = None) -> dict:
    review_items = [
        {
            "entry_id": "m_csa:1",
            "entry_name": "alpha testase",
            "rank": 1,
            "decision": {"fingerprint_id": "metal_dependent_hydrolase"},
            "queue_context": {
                "top1_fingerprint_id": "metal_dependent_hydrolase",
                "counterevidence_reasons": ["top1_below_abstention_threshold"],
            },
        },
        {
            "entry_id": "m_csa:2",
            "entry_name": "blocked testase",
            "rank": 2,
            "decision": {"fingerprint_id": "ser_his_acid_hydrolase"},
            "queue_context": {"top1_fingerprint_id": "ser_his_acid_hydrolase"},
        },
    ]
    return {
        "metadata": {"method": "expert_label_decision_review_export"},
        "review_items": review_items[:max_items],
    }


def _review_debt() -> dict:
    return {
        "metadata": {"method": "review_debt_summary"},
        "rows": [
            {
                "entry_id": "m_csa:1",
                "target_fingerprint_id": "metal_dependent_hydrolase",
                "gap_reasons": ["review_marked_needs_more_evidence"],
            }
        ],
    }


def _evidence_gaps() -> dict:
    return {
        "metadata": {"method": "review_evidence_gap_analysis"},
        "rows": [
            {
                "entry_id": "m_csa:1",
                "target_fingerprint_id": "metal_dependent_hydrolase",
                "gap_reasons": ["top1_below_abstention_threshold"],
            }
        ],
    }


def _geometry_features() -> dict:
    return {
        "metadata": {"artifact": "active_site_geometry_features"},
        "entries": [
            {
                "entry_id": "m_csa:1",
                "entry_name": "alpha testase",
                "status": "ok",
                "pdb_id": "1ABC",
                "residues": [
                    {
                        "residue_node_id": "m_csa:1:residue:1",
                        "chain_name": "A",
                        "code": "Asp",
                        "resid": 10,
                        "ca": {"x": 0.0, "y": 0.0, "z": 0.0},
                        "roles": ["acid/base"],
                    },
                    {
                        "residue_node_id": "m_csa:1:residue:2",
                        "chain_name": "A",
                        "code": "His",
                        "resid": 20,
                        "ca": {"x": 7.2, "y": 0.0, "z": 0.0},
                        "roles": ["proton shuttle"],
                    },
                ],
                "pairwise_distances_angstrom": [
                    {
                        "left": "m_csa:1:residue:1",
                        "right": "m_csa:1:residue:2",
                        "distance": 7.2,
                        "coordinate_type": "ca_or_centroid",
                    }
                ],
            },
            {
                "entry_id": "m_csa:2",
                "entry_name": "blocked testase",
                "status": "ok",
                "pdb_id": "2ABC",
                "residues": [],
                "pairwise_distances_angstrom": [],
            },
        ],
    }


def _structure_cif() -> str:
    return "\n".join(
        [
            "data_1ABC",
            "loop_",
            "_atom_site.group_PDB",
            "_atom_site.id",
            "_atom_site.type_symbol",
            "_atom_site.label_atom_id",
            "_atom_site.label_comp_id",
            "_atom_site.label_asym_id",
            "_atom_site.label_seq_id",
            "_atom_site.auth_atom_id",
            "_atom_site.auth_comp_id",
            "_atom_site.auth_asym_id",
            "_atom_site.auth_seq_id",
            "ATOM 1 C CA ASP A 10 CA ASP A 10",
            "ATOM 2 C CA HIS A 20 CA HIS A 20",
            "#",
            "",
        ]
    )


if __name__ == "__main__":
    unittest.main()
