from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.targeted_expansion_factory import (
    ADMISSION_STATES,
    build_targeted_expansion_factory_batch,
    write_targeted_expansion_factory_batch,
)


ROOT = Path(__file__).resolve().parents[1]


def _write(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    return path


class TargetedExpansionFactoryTests(unittest.TestCase):
    def test_current702_factory_artifact_counts_and_guardrails(self) -> None:
        path = (
            ROOT
            / "artifacts"
            / "v3_targeted_expansion_factory_batch_current702_20260608.json"
        )
        batch = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(batch["counts"]["candidate_rows_evaluated"], 703)
        self.assertEqual(batch["counts"]["source_namespace_counts"]["m_csa"], 324)
        self.assertEqual(
            batch["counts"]["source_namespace_counts"]["uniprot_swissprot"], 379
        )
        self.assertEqual(batch["counts"]["countable_candidate_rows"], 0)
        self.assertEqual(batch["counts"]["ready_for_label_import_rows"], 0)
        self.assertTrue(batch["state_assignment_audit"]["passed"])
        self.assertTrue(batch["factory_guardrail_audit"]["passed"])
        self.assertFalse(
            batch["guardrails"][
                "mechanism_text_ec_rhea_names_or_source_ids_used_as_predictive_features"
            ]
        )
        excluded = set(batch["target_policy"]["prior_architecture_default_rows_excluded"])
        self.assertFalse(
            excluded & {row["candidate_id"] for row in batch["candidate_rows"]}
        )
        first_tranche = batch["action_tranches"][0]
        self.assertEqual(first_tranche["admission_state"], "review_only_evidence")
        self.assertEqual(first_tranche["candidate_count"], 12)
        self.assertIn("duplicate", first_tranche["allowed_next_action"])
        first_input = batch["first_action_screen_input"]
        self.assertEqual(first_input["status"], "ready")
        self.assertEqual(first_input["candidate_count"], 12)
        self.assertEqual(len(first_input["rows"]), 12)
        self.assertIn(
            "current_countable_foldseek_structural_screen",
            first_input["rows"][0]["next_required_screens"],
        )
        candidate_payload = json.dumps(batch["candidate_rows"], sort_keys=True)
        self.assertNotIn("mechanism_text_snippets", candidate_payload)
        for row in batch["candidate_rows"]:
            self.assertNotIn("ec_numbers", row)
            self.assertNotIn("rhea_ids", row)
            self.assertNotIn("ec_numbers", row.get("review_context", {}))
            self.assertNotIn("rhea_ids", row.get("review_context", {}))

    def test_batch_routes_rows_without_countable_or_import_flags(self) -> None:
        label_expansion = {
            "rows": [
                {
                    "cofactor_evidence_level": "ligand_supported",
                    "cofactor_families": ["metal_ion"],
                    "entry_id": "m_csa:1000",
                    "entry_name": "geometry ready row",
                    "has_pairwise_geometry": True,
                    "has_pocket_context": True,
                    "mechanism_text_count": 1,
                    "mechanism_text_snippets": ["must not be copied"],
                    "mechanistic_coherence_score": 1.0,
                    "pdb_id": "1ABC",
                    "readiness_blockers": [],
                    "readiness_checks": {
                        "has_pairwise_geometry": True,
                        "has_pocket_context": True,
                        "resolved_at_least_three_residues": True,
                        "status_ok": True,
                        "top1_score_at_least_0_4": True,
                    },
                    "readiness_score": 5,
                    "resolved_residue_count": 4,
                    "status": "ok",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_score": 0.61,
                },
                {
                    "cofactor_evidence_level": "absent",
                    "cofactor_families": [],
                    "entry_id": "m_csa:1001",
                    "entry_name": "locator gap row",
                    "has_pairwise_geometry": False,
                    "has_pocket_context": False,
                    "mechanism_text_count": 1,
                    "pdb_id": "1DEF",
                    "readiness_blockers": ["resolved_at_least_three_residues"],
                    "readiness_checks": {},
                    "readiness_score": 2,
                    "resolved_residue_count": 1,
                    "status": "insufficient_resolved_residues",
                    "top1_fingerprint_id": "ser_his_acid_hydrolase",
                    "top1_score": 0.31,
                },
            ]
        }
        external_freeze = {
            "rows": [
                {
                    "accession": "P11111",
                    "active_site_evidence_status": (
                        "explicit_active_site_and_catalytic_activity_source_present"
                    ),
                    "active_site_feature_count": 2,
                    "alphafold_ids": ["P11111"],
                    "binding_site_feature_count": 4,
                    "catalytic_activity_count": 2,
                    "cofactor_comment_count": 1,
                    "covered_counterevidence_lane": True,
                    "entry_id": "uniprot:P11111",
                    "lane_id": "external_source:oxidoreductase_long_tail",
                    "new_to_current_external_pool": True,
                    "next_required_screens": [
                        "current_reference_backend_sequence_search"
                    ],
                    "pdb_ids": ["2ABC"],
                    "protein_name": "review context only",
                    "ready_for_label_import": False,
                    "source_evidence_blockers": [],
                    "sourcing_status": (
                        "sourced_pending_sequence_structure_distance_screens"
                    ),
                },
                {
                    "accession": "P22222",
                    "active_site_evidence_status": "binding_or_reaction_context_only",
                    "alphafold_ids": ["P22222"],
                    "covered_counterevidence_lane": True,
                    "entry_id": "uniprot:P22222",
                    "lane_id": "external_source:glycan_chemistry",
                    "new_to_current_external_pool": True,
                    "pdb_ids": [],
                    "source_evidence_blockers": ["uniprot_active_site_feature_missing"],
                    "sourcing_status": "blocked_active_site_source_missing",
                },
                {
                    "accession": "P33333",
                    "active_site_evidence_status": "not_sampled_metadata_blocked",
                    "alphafold_ids": ["P33333"],
                    "covered_counterevidence_lane": False,
                    "entry_id": "uniprot:P33333",
                    "lane_id": "external_source:transferase_methyl",
                    "new_to_current_external_pool": True,
                    "pdb_ids": [],
                    "source_evidence_blockers": [
                        "mechanism_lane_not_covered_by_existing_counterevidence_rules"
                    ],
                    "sourcing_status": "blocked_uncovered_mechanism_lane",
                },
                {
                    "accession": "P44444",
                    "active_site_evidence_status": "not_sampled_metadata_blocked",
                    "alphafold_ids": ["P44444"],
                    "covered_counterevidence_lane": True,
                    "entry_id": "uniprot:P44444",
                    "lane_id": "external_source:isomerase",
                    "new_to_current_external_pool": False,
                    "pdb_ids": [],
                    "source_evidence_blockers": [
                        "accession_already_in_current_external_pool"
                    ],
                    "sourcing_status": "excluded_current_external_pool",
                },
            ]
        }
        sequence_proxy = {
            "rows": [
                {
                    "entry_id": "m_csa:1000",
                    "reference_uniprot_ids": ["Q00001"],
                    "sequence_cluster_id": "uniprot:Q00001",
                },
                {
                    "entry_id": "m_csa:1001",
                    "reference_uniprot_ids": ["Q00002"],
                    "sequence_cluster_id": "uniprot:Q00002",
                }
            ]
        }

        batch = build_targeted_expansion_factory_batch(
            label_expansion_candidates=label_expansion,
            external_candidate_freeze=external_freeze,
            sequence_cluster_proxy=sequence_proxy,
            min_target_candidates=1,
            max_target_candidates=10,
        )

        self.assertTrue(batch["state_assignment_audit"]["passed"])
        self.assertTrue(batch["factory_guardrail_audit"]["passed"])
        self.assertEqual(batch["counts"]["candidate_rows_evaluated"], 6)
        self.assertEqual(batch["counts"]["countable_candidate_rows"], 0)
        self.assertEqual(batch["counts"]["ready_for_label_import_rows"], 0)
        states = batch["counts"]["admission_state_counts"]
        self.assertEqual(states["review_only_evidence"], 2)
        self.assertEqual(states["blocked_locator"], 1)
        self.assertEqual(states["acquisition_needed"], 1)
        self.assertEqual(states["blocked_family_decision"], 1)
        self.assertEqual(states["reject_preserve_signal"], 1)
        self.assertEqual(batch["action_tranches"][0]["candidate_count"], 1)
        self.assertIn("duplicate", batch["action_tranches"][0]["allowed_next_action"])
        self.assertEqual(batch["first_action_screen_input"]["candidate_count"], 1)
        self.assertEqual(
            batch["first_action_screen_input"]["rows"][0]["accession"],
            "P11111",
        )
        self.assertTrue(
            all(
                row["admission_state"] in ADMISSION_STATES
                for row in batch["candidate_rows"]
            )
        )
        self.assertTrue(
            all(
                not row["countable_label_candidate"]
                and not row["ready_for_label_import"]
                for row in batch["candidate_rows"]
            )
        )
        payload_text = json.dumps(batch["candidate_rows"], sort_keys=True)
        self.assertNotIn("mechanism_text_snippets", payload_text)
        self.assertNotIn("must not be copied", payload_text)
        self.assertFalse(
            batch["guardrails"][
                "mechanism_text_ec_rhea_names_or_source_ids_used_as_predictive_features"
            ]
        )

    def test_write_batch_materializes_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            label_path = _write(
                root / "labels.json",
                {
                    "rows": [
                        {
                            "cofactor_evidence_level": "absent",
                            "cofactor_families": [],
                            "entry_id": "m_csa:2000",
                            "entry_name": "coordinate gap",
                            "has_pairwise_geometry": False,
                            "has_pocket_context": False,
                            "mechanism_text_count": 0,
                            "pdb_id": None,
                            "readiness_blockers": [],
                            "readiness_checks": {},
                            "readiness_score": 0,
                            "resolved_residue_count": 0,
                            "status": "no_structure_positions",
                            "top1_fingerprint_id": None,
                            "top1_score": None,
                        }
                    ]
                },
            )
            external_path = _write(root / "external.json", {"rows": []})
            sequence_path = _write(
                root / "sequence.json",
                {
                    "rows": [
                        {
                            "entry_id": "m_csa:2000",
                            "reference_uniprot_ids": ["Q00003"],
                            "sequence_cluster_id": "uniprot:Q00003",
                        }
                    ]
                },
            )
            out_path = root / "out.json"
            report_path = root / "report.md"

            batch = write_targeted_expansion_factory_batch(
                label_expansion_candidates_path=label_path,
                external_candidate_freeze_path=external_path,
                sequence_cluster_proxy_path=sequence_path,
                out_path=out_path,
                report_path=report_path,
                created_utc="2026-06-08T04:06:45Z",
                min_target_candidates=1,
                max_target_candidates=10,
            )

            self.assertEqual(batch["status"], "targeted_expansion_factory_batch_ready")
            self.assertTrue(batch["factory_guardrail_audit"]["passed"])
            self.assertTrue(out_path.exists())
            self.assertTrue(report_path.exists())
            parsed = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(parsed["created_utc"], "2026-06-08T04:06:45Z")
            report_text = report_path.read_text()
            self.assertIn("Targeted Expansion Factory Batch", report_text)
            self.assertIn("Target volume:", report_text)
            self.assertIn("Coordinate Status", report_text)
            self.assertIn("Proposed Tiers", report_text)
            self.assertIn("Source Hashes", report_text)
            self.assertIn("First Action Preview", report_text)


if __name__ == "__main__":
    unittest.main()
