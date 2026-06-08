from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.scaleout_radical_sam_cobalamin_shard import (
    TERMINAL_STATES,
    build_scaleout_radical_sam_cobalamin_shard,
    write_scaleout_radical_sam_cobalamin_shard,
)


class ScaleoutRadicalSamCobalaminShardTests(unittest.TestCase):
    def _write_json(self, root: Path, name: str, payload: object) -> Path:
        path = root / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def _write_text(self, root: Path, name: str, payload: str) -> Path:
        path = root / name
        path.write_text(payload, encoding="utf-8")
        return path

    def test_build_merges_sidecars_fasta_and_coupled_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            factory = self._write_json(
                root,
                "factory.json",
                {
                    "candidate_rows": [
                        {
                            "candidate_id": "m_csa:946",
                            "display_name": "cycloisomerase radical-SAM boundary",
                            "family_axis": "radical_cobalamin_sam_like_probes",
                            "admission_state": "blocked_coordinate",
                            "proposed_label_tier": "evidence_blocked_coordinate_repair",
                            "allowed_next_action": "materialize or approve a valid coordinate source before scoring",
                            "active_site_or_locator_evidence": {
                                "resolved_residue_count": 0,
                                "readiness_blockers": ["fewer_than_three_resolved_residues"],
                            },
                            "predicted_coordinate_or_provenance_availability": {
                                "coordinate_provenance_available": False,
                                "selected_structure": None,
                            },
                            "cofactor_or_metal_evidence": {
                                "cofactor_families": ["sam"],
                            },
                            "fold_tm_or_near_neighbor_signal": {
                                "top1_fingerprint_id": "radical_sam_enzyme"
                            },
                            "mechanical_unblock_requirements": {
                                "allowed_next_action": "materialize or approve a valid coordinate source before scoring",
                                "readiness_blockers": ["fewer_than_three_resolved_residues"],
                            },
                        }
                    ]
                },
            )
            radical_sidecar = self._write_json(
                root,
                "radical_sidecar.json",
                {
                    "rows": [
                        {
                            "entry_id": "m_csa:358",
                            "sidecar_status": "proximal_radical_sam_context_available",
                            "fingerprint_id": "plp_dependent_enzyme",
                            "label_type": "seed_fingerprint",
                            "benchmark_role": "primary_supervised_metric::plp_dependent_enzyme",
                            "nearest_active_site_distance_angstrom": 3.8,
                            "supporting_ligand_codes": ["SAM"],
                            "proximal_radical_sam_ligands": [{"code": "SAM"}],
                            "structure_radical_sam_ligands": [{"code": "SAM"}],
                            "sam_fe_s_copresence_status": "proximal_sam_and_fe_s_context",
                            "predictive_use_allowed": False,
                            "ready_for_label_import": False,
                        }
                    ]
                },
            )
            cobalamin_sidecar = self._write_json(
                root,
                "cobalamin_sidecar.json",
                {
                    "rows": [
                        {
                            "entry_id": "m_csa:62",
                            "sidecar_status": "proximal_cobalamin_context_available",
                            "fingerprint_id": "cobalamin_radical_rearrangement",
                            "label_type": "seed_fingerprint",
                            "benchmark_role": "secondary_ood_probe::cobalamin_radical_rearrangement",
                            "nearest_active_site_distance_angstrom": 3.6,
                            "supporting_ligand_codes": ["B12"],
                            "proximal_cobalamin_ligands": [{"code": "B12"}],
                            "structure_cobalamin_ligands": [{"code": "B12"}],
                            "adenosyl_or_methyl_context_flag": True,
                            "radical_rearrangement_source_flag": True,
                            "predictive_use_allowed": False,
                            "ready_for_label_import": False,
                        }
                    ]
                },
            )
            freeze = self._write_json(
                root,
                "freeze.json",
                {
                    "rows": [
                        {
                            "row_id": "uniprot:Q1",
                            "accession": "Q1",
                            "entry_name": "RAD_Q1",
                            "protein_name": "Radical SAM enzyme",
                            "score_status": "not_scored_at_freeze",
                            "radical_sam_source_context_present": True,
                            "fe_s_or_sam_source_context_present": True,
                            "pdb_ids_sample": ["1AAA"],
                            "pdb_count": 1,
                        }
                    ]
                },
            )
            fasta = self._write_text(
                root,
                "radical.fasta",
                ">uniprot:Q1|RAD_Q1\nMAAACAAACAACQ\n",
            )
            coupled = self._write_json(
                root,
                "coupled.json",
                {
                    "row": {
                        "entry_id": "m_csa:737",
                        "entry_name": "beta-lysine 5,6-aminomutase",
                        "selected_pdb": "1XRS",
                        "current_target_fingerprint": "cobalamin_radical_rearrangement",
                        "schema_issue": "requires PLP plus adenosylcobalamin",
                        "exact_blocker": "No production coupled-cofactor family",
                        "future_reopen_condition": "explicit future schema/fingerprint task",
                        "import_gate_eligible": False,
                        "terminal_current_production_universe_no_go": True,
                        "not_counted_as": ["plain_cobalamin_radical_rearrangement"],
                        "observed_cofactor_context": {
                            "hetatms_in_structure": ["B12", "PLP"],
                            "b12_ligands": [{"resn": "B12"}],
                            "cofactors_required": ["adenosylcobalamin", "PLP"],
                        },
                    }
                },
            )

            artifact = build_scaleout_radical_sam_cobalamin_shard(
                source_paths={
                    "targeted_expansion_factory_batch": factory,
                    "radical_sam_locus_sidecar": radical_sidecar,
                    "cobalamin_locus_sidecar": cobalamin_sidecar,
                    "radical_sam_minicampaign_freeze": freeze,
                    "coupled_plp_cobalamin_schema_decision": coupled,
                },
                fasta_paths={"radical_sam_minicampaign_sequence_fasta": fasta},
                created_utc="2026-06-08T00:00:00Z",
            )

        by_id = {row["candidate_id"]: row for row in artifact["rows"]}
        self.assertEqual(by_id["m_csa:946"]["terminal_state"], "blocked_coordinate")
        self.assertEqual(
            by_id["m_csa:62"]["proposed_subfamily_lane"],
            "cobalamin_radical_rearrangement",
        )
        self.assertEqual(by_id["m_csa:737"]["terminal_state"], "blocked_family_decision")
        self.assertTrue(
            by_id["m_csa:737"]["sf4_fe_s_sam_cobalamin_plp_evidence"][
                "evidence_flags"
            ]["plp_evidence_present"]
        )
        self.assertGreater(
            by_id["uniprot:Q1"]["active_site_or_locator_evidence"][
                "cx3cx2c_motif_count"
            ],
            0,
        )
        self.assertTrue(artifact["validation_checks"]["required_row_fields_present"])
        self.assertEqual(
            set(artifact["terminal_state_counts"]) - set(TERMINAL_STATES),
            set(),
        )

    def test_write_outputs_json_report_and_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sidecar = self._write_json(
                root,
                "iron.json",
                {
                    "rows": [
                        {
                            "entry_id": "m_csa:127",
                            "sidecar_status": "proximal_iron_sulfur_context_available",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "benchmark_role": "oos_tier::unknown_oos",
                            "nearest_active_site_distance_angstrom": 3.4,
                            "supporting_ligand_codes": ["SF4"],
                            "proximal_iron_sulfur_ligands": [{"code": "SF4"}],
                            "structure_iron_sulfur_ligands": [{"code": "SF4"}],
                            "sam_fe_s_copresence_status": "iron_sulfur_without_copresent_partner",
                            "predictive_use_allowed": False,
                            "ready_for_label_import": False,
                        }
                    ]
                },
            )
            out = root / "out.json"
            report = root / "report.md"
            handoff = root / "handoff.md"

            artifact = write_scaleout_radical_sam_cobalamin_shard(
                out_path=out,
                report_path=report,
                handoff_path=handoff,
                source_paths={"iron_sulfur_locus_sidecar": sidecar},
                fasta_paths={},
                created_utc="2026-06-08T00:00:00Z",
                started_at_utc="2026-06-08T00:00:00Z",
                started_at_local="2026-06-07T19:00:00-0500",
                elapsed_minutes=1.25,
            )

            persisted = json.loads(out.read_text(encoding="utf-8"))
            self.assertIn("Radical SAM Cobalamin Scale-Out Shard", report.read_text())
            self.assertIn("STARTED_AT_UTC", handoff.read_text())

        self.assertEqual(persisted["artifact_id"], artifact["artifact_id"])


if __name__ == "__main__":
    unittest.main()
