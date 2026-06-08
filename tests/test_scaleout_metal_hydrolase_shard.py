from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.scaleout_metal_hydrolase_shard import (
    TERMINAL_STATES,
    build_scaleout_metal_hydrolase_shard,
    write_scaleout_metal_hydrolase_shard,
)


class ScaleoutMetalHydrolaseShardTests(unittest.TestCase):
    def _write_json(self, root: Path, name: str, payload: object) -> Path:
        path = root / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_build_merges_factory_and_tail_panel_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            factory = self._write_json(
                root,
                "factory.json",
                {
                    "candidate_rows": [
                        {
                            "candidate_id": "m_csa:200",
                            "display_name": "NAD+ synthase",
                            "family_axis": "metal_hydrolase_subclasses",
                            "admission_state": "blocked_locator",
                            "proposed_label_tier": "evidence_blocked_locator_repair",
                            "allowed_next_action": "repair source-free residue mapping",
                            "active_site_or_locator_evidence": {
                                "readiness_blockers": [
                                    "fewer_than_three_resolved_residues"
                                ],
                                "resolved_residue_count": 2,
                            },
                            "predicted_coordinate_or_provenance_availability": {
                                "coordinate_path": "coords/1KQP.cif",
                                "coordinate_status": "already_materialized",
                                "selected_structure": "pdb:1KQP",
                            },
                            "cofactor_or_metal_evidence": {
                                "cofactor_evidence_level": "ligand_supported",
                                "cofactor_families": ["metal_ion"],
                            },
                            "fold_tm_or_near_neighbor_signal": {
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "top1_score": 0.51,
                            },
                            "mechanical_unblock_requirements": {
                                "allowed_next_action": "repair source-free residue mapping",
                                "readiness_blockers": [
                                    "fewer_than_three_resolved_residues"
                                ],
                            },
                        }
                    ]
                },
            )
            tail = self._write_json(
                root,
                "tail.json",
                {
                    "candidate_rows": [
                        {
                            "accession": "m_csa:200",
                            "candidate_role": "positive_anchor",
                            "lane": "binuclear_metallohydrolase_amidohydrolase",
                            "name": "NAD+ synthase",
                            "geometry_class": "tight_active_site_geometry",
                            "evidence_summary": "curated anchor",
                            "observed_ligand_codes": ["MG"],
                            "metal_ligand_state": "metal-supported hydrolase",
                            "ligand_or_substrate_state": "amide hydrolysis",
                            "readiness_tier": "gold",
                            "ready_for_label_import": False,
                        }
                    ]
                },
            )

            artifact = build_scaleout_metal_hydrolase_shard(
                source_paths={
                    "targeted_expansion_factory_batch": factory,
                    "external_metal_hydrolase_tail_panel": tail,
                },
                created_utc="2026-06-08T00:00:00Z",
            )

        self.assertEqual(artifact["candidate_count"], 1)
        row = artifact["rows"][0]
        self.assertEqual(row["candidate_id"], "m_csa:200")
        self.assertEqual(row["terminal_state"], "blocked_locator")
        self.assertEqual(
            row["proposed_subfamily_lane"],
            "binuclear_metallohydrolase_amidohydrolase",
        )
        self.assertEqual(
            set(row["source_hashes"]),
            {"targeted_expansion_factory_batch", "external_metal_hydrolase_tail_panel"},
        )
        self.assertTrue(row["duplicate_screens"]["source_specific"])
        self.assertTrue(artifact["validation_checks"]["required_row_fields_present"])
        self.assertTrue(artifact["validation_checks"]["terminal_states_allowed"])

    def test_metal_phosphatase_precedence_and_required_states(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            freeze = self._write_json(
                root,
                "freeze.json",
                {
                    "rows": [
                        {
                            "row_id": "uniprot:Q1",
                            "accession": "Q1",
                            "protein_name": "Metal phosphatase candidate",
                            "score_status": "not_scored_at_freeze",
                            "pdb_ids_sample": ["1AAA"],
                            "active_site_count": 2,
                            "metal_binding_site_count": 3,
                        }
                    ]
                },
            )
            specificity = self._write_json(
                root,
                "specificity.json",
                {
                    "rows": [
                        {
                            "row_id": "uniprot:Q1",
                            "accession": "Q1",
                            "terminal_decision": "mechanism_match_review_ready",
                            "countable_label_candidate": False,
                            "ready_for_label_import": False,
                            "exact_missing_evidence_to_resolve": [
                                "preregister source-free phosphate pocket extractor"
                            ],
                            "remaining_import_blockers": [
                                "full_label_factory_gate_not_run"
                            ],
                            "current_geometry_retrieval_score_summary": {
                                "geometry_score_status": "source_free_coordinate_geometry_scored",
                                "text_or_label_fields_used_for_score": False,
                            },
                        },
                        {
                            "row_id": "uniprot:Q2",
                            "accession": "Q2",
                            "terminal_decision": "terminal_rejection_duplicate_or_leakage",
                            "duplicate_leakage_screen": {
                                "current_countable_high_tm_hit_count": 1
                            },
                        },
                    ]
                },
            )
            controls = self._write_json(
                root,
                "controls.json",
                {
                    "row_evidence": [
                        {
                            "entry_id": "mh_065",
                            "evidence_role": "cofactor-confounded OOS control",
                            "predicted_geometry_status": "missing",
                            "predicted_structure_fold_channel": {
                                "nearest_atlas_entry_id": "m_csa:15"
                            },
                        }
                    ]
                },
            )

            artifact = build_scaleout_metal_hydrolase_shard(
                source_paths={
                    "metal_phosphatase_minicampaign_freeze": freeze,
                    "external_metal_phosphatase_review_ready_specificity_blocker": specificity,
                    "no_reliable_structure_metal_hydrolase_controls": controls,
                },
                created_utc="2026-06-08T00:00:00Z",
            )

        by_id = {row["candidate_id"]: row for row in artifact["rows"]}
        self.assertEqual(by_id["uniprot:Q1"]["terminal_state"], "blocked_family_decision")
        self.assertIn("extractor", by_id["uniprot:Q1"]["machine_actionable_next_step"])
        self.assertEqual(by_id["uniprot:Q2"]["terminal_state"], "reject/OOS_preserve_signal")
        self.assertIn("duplicate", by_id["uniprot:Q2"]["machine_actionable_next_step"])
        self.assertEqual(by_id["mh_065"]["terminal_state"], "reject/OOS_preserve_signal")
        self.assertEqual(
            set(artifact["terminal_state_counts"]) - set(TERMINAL_STATES),
            set(),
        )
        self.assertTrue(artifact["guardrails"]["oos_reject_signal_preserved"])

    def test_write_outputs_json_report_and_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tail = self._write_json(
                root,
                "tail.json",
                {
                    "candidate_rows": [
                        {
                            "accession": "m_csa:44",
                            "candidate_role": "positive_anchor",
                            "lane": "phosphatase_phosphoesterase",
                            "name": "alkaline phosphatase",
                            "observed_ligand_codes": ["ZN", "MG"],
                            "ready_for_label_import": False,
                        }
                    ]
                },
            )
            out = root / "out.json"
            report = root / "report.md"
            handoff = root / "handoff.md"

            artifact = write_scaleout_metal_hydrolase_shard(
                out_path=out,
                report_path=report,
                handoff_path=handoff,
                source_paths={"external_metal_hydrolase_tail_panel": tail},
                created_utc="2026-06-08T00:00:00Z",
                started_at_utc="2026-06-08T00:00:00Z",
                started_at_local="2026-06-07T19:00:00-0500",
                elapsed_minutes=1.25,
            )

            persisted = json.loads(out.read_text(encoding="utf-8"))
            self.assertIn("Metal Hydrolase Scale-Out Shard", report.read_text())
            self.assertIn("STARTED_AT_UTC", handoff.read_text())

        self.assertEqual(persisted["artifact_id"], artifact["artifact_id"])


if __name__ == "__main__":
    unittest.main()
