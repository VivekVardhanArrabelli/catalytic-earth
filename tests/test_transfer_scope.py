from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from catalytic_earth.transfer_scope import (
    audit_external_source_active_site_evidence_sample,
    audit_external_source_active_site_sourcing_export,
    audit_external_source_active_site_sourcing_queue,
    audit_external_source_active_site_sourcing_resolution,
    audit_external_source_binding_context_mapping_sample,
    audit_external_source_binding_context_repair_plan,
    audit_external_source_broad_ec_disambiguation,
    audit_external_source_candidate_manifest,
    audit_external_source_candidate_sample,
    audit_external_source_heuristic_control_queue,
    audit_external_source_heuristic_control_scores,
    audit_external_source_failure_modes,
    audit_external_source_import_readiness,
    audit_external_source_lane_balance,
    audit_external_source_reaction_evidence_sample,
    audit_external_source_representation_control_comparison,
    audit_external_source_representation_control_manifest,
    audit_external_source_representation_backend_plan,
    audit_external_source_representation_backend_sample,
    audit_external_source_sequence_alignment_verification,
    audit_external_source_sequence_reference_screen,
    audit_external_source_sequence_search_export,
    audit_external_source_sequence_holdouts,
    audit_external_source_sequence_neighborhood_sample,
    audit_external_source_structure_mapping_plan,
    audit_external_source_structure_mapping_sample,
    audit_external_source_control_repair_plan,
    audit_external_source_transfer_blocker_matrix,
    build_external_ood_calibration_plan,
    build_external_source_active_site_gap_source_requests,
    build_external_source_active_site_sourcing_export,
    build_external_source_active_site_sourcing_queue,
    build_external_source_active_site_sourcing_resolution,
    build_external_source_binding_context_mapping_sample,
    build_external_source_binding_context_repair_plan,
    build_external_source_active_site_evidence_queue,
    build_external_source_active_site_evidence_sample,
    build_external_source_candidate_manifest,
    build_external_source_candidate_sample,
    build_external_source_control_repair_plan,
    build_external_source_evidence_plan,
    build_external_source_evidence_request_export,
    build_external_source_heuristic_control_queue,
    build_external_source_heuristic_control_scores,
    build_external_source_pilot_candidate_priority,
    build_external_source_pilot_evidence_packet,
    build_external_source_pilot_evidence_dossiers,
    build_external_source_pilot_review_decision_export,
    build_external_source_structure_mapping_plan,
    build_external_source_structure_mapping_sample,
    build_external_source_query_manifest,
    build_external_source_reaction_evidence_sample,
    build_external_source_representation_control_comparison,
    build_external_source_representation_control_manifest,
    build_external_source_representation_backend_plan,
    build_external_source_representation_backend_sample,
    build_external_source_sequence_alignment_verification,
    build_external_source_sequence_search_export,
    build_external_source_sequence_neighborhood_plan,
    build_external_source_sequence_neighborhood_sample,
    build_external_source_transfer_manifest,
    build_external_source_transfer_blocker_matrix,
    check_external_source_transfer_gates,
    ExternalSourceTransferGateInputs,
    validate_external_transfer_artifact_path_lineage,
)


ROOT = Path(__file__).resolve().parents[1]


def _base_external_transfer_gate_inputs() -> dict:
    return {
        "transfer_manifest": {
            "metadata": {
                "ready_for_label_import": False,
                "countable_label_candidate_count": 0,
            }
        },
        "query_manifest": {
            "metadata": {
                "ready_for_label_import": False,
                "countable_label_candidate_count": 0,
            }
        },
        "ood_calibration_plan": {
            "metadata": {
                "ready_for_label_import": False,
                "requires_heuristic_control": True,
            }
        },
        "candidate_sample_audit": {
            "metadata": {
                "guardrail_clean": True,
                "countable_label_candidate_count": 0,
            }
        },
        "candidate_manifest": {
            "metadata": {
                "ready_for_label_import": False,
                "countable_label_candidate_count": 0,
                "candidate_count": 1,
                "heuristic_control_required": True,
            },
            "rows": [{"accession": "P12345"}],
        },
        "candidate_manifest_audit": {
            "metadata": {
                "guardrail_clean": True,
                "countable_label_candidate_count": 0,
            }
        },
        "lane_balance_audit": {
            "metadata": {
                "guardrail_clean": True,
                "countable_label_candidate_count": 0,
                "lane_count": 1,
                "dominant_lane_fraction": 1.0,
            }
        },
        "evidence_plan": {
            "metadata": {
                "ready_for_label_import": False,
                "ready_for_evidence_collection": True,
                "countable_label_candidate_count": 0,
                "candidate_count": 1,
                "exact_reference_overlap_holdout_count": 0,
            },
            "rows": [{"accession": "P12345"}],
        },
        "evidence_request_export": {
            "metadata": {
                "external_source_review_only": True,
                "countable_label_candidate_count": 0,
            },
            "review_items": [{"accession": "P12345"}],
        },
        "review_only_import_safety_audit": {
            "metadata": {
                "countable_import_safe": True,
                "total_new_countable_label_count": 0,
            }
        },
    }


class ExternalSourceTransferManifestTests(unittest.TestCase):
    def test_manifest_keeps_transfer_scope_non_countable(self) -> None:
        manifest = build_external_source_transfer_manifest(
            source_scale_audit={
                "metadata": {
                    "source_limit_reached": True,
                    "recommendation": "stop_m_csa_only_tranche_growth_and_scope_external_source_transfer",
                    "observed_source_entries": 1003,
                    "target_source_entries": 1025,
                    "public_target_countable_labels": 10000,
                }
            },
            learned_retrieval_manifest={"metadata": {"eligible_row_count": 617}},
            sequence_similarity_failure_sets={
                "metadata": {"duplicate_cluster_count": 6}
            },
            ontology_gap_audit={"metadata": {"row_count": 226}, "rows": []},
            active_learning_queue={
                "rows": [
                    {
                        "entry_id": "m_csa:1003",
                        "top1_ontology_family": "heme_redox",
                        "issue_classes": ["cofactor_family_ambiguity"],
                    }
                ]
            },
            labels=[
                {
                    "entry_id": "m_csa:1",
                    "label_type": "seed_fingerprint",
                    "review_status": "automation_curated",
                }
            ],
        )

        metadata = manifest["metadata"]
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            metadata["manifest_recommendation"],
            "prototype_external_source_transfer_before_next_count_growth",
        )
        self.assertIn("m_csa_source_limit_reached", manifest["blockers"])
        self.assertIn("heuristic geometry retrieval", manifest["required_guardrails"][0])

    def test_build_external_source_transfer_manifest_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_scale = root / "source_scale.json"
            learned = root / "learned.json"
            sequence = root / "sequence.json"
            ontology = root / "ontology.json"
            queue = root / "queue.json"
            labels = root / "labels.json"
            out = root / "transfer.json"
            source_scale.write_text(
                json.dumps({"metadata": {"source_limit_reached": True}}),
                encoding="utf-8",
            )
            learned.write_text(json.dumps({"metadata": {}}), encoding="utf-8")
            sequence.write_text(json.dumps({"metadata": {}}), encoding="utf-8")
            ontology.write_text(json.dumps({"metadata": {}, "rows": []}), encoding="utf-8")
            queue.write_text(json.dumps({"rows": []}), encoding="utf-8")
            labels.write_text(json.dumps([]), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-transfer-manifest",
                    "--source-scale-audit",
                    str(source_scale),
                    "--learned-retrieval-manifest",
                    str(learned),
                    "--sequence-similarity-failure-sets",
                    str(sequence),
                    "--ontology-gap-audit",
                    str(ontology),
                    "--active-learning-queue",
                    str(queue),
                    "--labels",
                    str(labels),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["metadata"]["countable_label_candidate_count"], 0)

    def test_external_transfer_planning_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            transfer = root / "transfer.json"
            ontology = root / "ontology.json"
            sequence = root / "sequence.json"
            labels = root / "labels.json"
            queries = root / "queries.json"
            ood = root / "ood.json"
            sample = root / "sample.json"
            sample_audit = root / "sample_audit.json"
            transfer.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "manifest_recommendation": (
                                "prototype_external_source_transfer_before_next_count_growth"
                            ),
                            "m_csa_source_limit_reached": True,
                        }
                    }
                ),
                encoding="utf-8",
            )
            ontology.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "scope_signals": ["transferase_phosphoryl"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            sequence.write_text(
                json.dumps({"metadata": {"duplicate_cluster_count": 1}}),
                encoding="utf-8",
            )
            labels.write_text(json.dumps([]), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-query-manifest",
                    "--transfer-manifest",
                    str(transfer),
                    "--ontology-gap-audit",
                    str(ontology),
                    "--out",
                    str(queries),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-ood-calibration-plan",
                    "--query-manifest",
                    str(queries),
                    "--sequence-similarity-failure-sets",
                    str(sequence),
                    "--labels",
                    str(labels),
                    "--out",
                    str(ood),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            sample.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "accession": "P12345",
                                "reviewed": "reviewed",
                                "ec_numbers": ["2.7.1.1"],
                                "alphafold_ids": ["AF-P12345-F1"],
                                "countable_label_candidate": False,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-external-source-candidate-sample",
                    "--candidate-sample",
                    str(sample),
                    "--out",
                    str(sample_audit),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual(
                json.loads(queries.read_text(encoding="utf-8"))["metadata"][
                    "lane_count"
                ],
                1,
            )
            self.assertFalse(
                json.loads(ood.read_text(encoding="utf-8"))["metadata"][
                    "ready_for_label_import"
                ]
            )
            self.assertTrue(
                json.loads(sample_audit.read_text(encoding="utf-8"))["metadata"][
                    "guardrail_clean"
                ]
            )

    def test_query_manifest_uses_ontology_scope_signals(self) -> None:
        manifest = build_external_source_query_manifest(
            transfer_manifest={
                "metadata": {
                    "manifest_recommendation": (
                        "prototype_external_source_transfer_before_next_count_growth"
                    ),
                    "m_csa_source_limit_reached": True,
                }
            },
            ontology_gap_audit={
                "rows": [
                    {
                        "entry_id": "m_csa:603",
                        "scope_signals": ["transferase_phosphoryl"],
                    },
                    {
                        "entry_id": "m_csa:35",
                        "scope_signals": ["transferase_phosphoryl", "lyase"],
                    },
                ]
            },
            max_lanes=2,
        )

        self.assertEqual(manifest["metadata"]["lane_count"], 2)
        self.assertFalse(manifest["metadata"]["ready_for_label_import"])
        self.assertEqual(manifest["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            manifest["rows"][0]["lane_id"], "external_source:transferase_phosphoryl"
        )
        self.assertIn("kinase", manifest["rows"][0]["source_query_draft"])

    def test_ood_calibration_plan_keeps_external_lanes_review_only(self) -> None:
        plan = build_external_ood_calibration_plan(
            query_manifest={
                "rows": [
                    {
                        "lane_id": "external_source:lyase",
                        "scope_signal": "lyase",
                        "source_query_draft": "(reviewed:true) AND (ec:4.*)",
                    }
                ]
            },
            sequence_similarity_failure_sets={
                "metadata": {"duplicate_cluster_count": 2}
            },
            labels=[
                {
                    "entry_id": "m_csa:1",
                    "label_type": "out_of_scope",
                    "review_status": "automation_curated",
                }
            ],
        )

        self.assertFalse(plan["metadata"]["ready_for_label_import"])
        self.assertEqual(plan["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(plan["metadata"]["lane_count"], 1)
        self.assertEqual(plan["metadata"]["sequence_duplicate_cluster_count"], 2)
        self.assertIn(
            "exact_sequence_cluster_exclusion",
            plan["rows"][0]["calibration_controls"],
        )

    def test_candidate_sample_deduplicates_and_stays_non_countable(self) -> None:
        def fake_fetcher(query: str, size: int) -> dict:
            self.assertEqual(size, 2)
            return {
                "records": [
                    {
                        "accession": "P12345",
                        "entry_name": "KINASE_HUMAN",
                        "protein_name": "Example kinase",
                        "organism": "Homo sapiens",
                        "length": 300,
                        "reviewed": "reviewed",
                        "ec_numbers": ["2.7.1.1"],
                        "pdb_ids": ["1ABC"],
                        "alphafold_ids": ["AF-P12345-F1"],
                    },
                    {
                        "accession": "P12345",
                        "entry_name": "KINASE_HUMAN",
                        "protein_name": "Duplicate kinase",
                    },
                ]
            }

        sample = build_external_source_candidate_sample(
            query_manifest={
                "rows": [
                    {
                        "lane_id": "external_source:transferase_phosphoryl",
                        "scope_signal": "transferase_phosphoryl",
                        "source_query_draft": "reviewed:true",
                    }
                ]
            },
            max_records_per_lane=2,
            fetcher=fake_fetcher,
        )

        self.assertFalse(sample["metadata"]["ready_for_label_import"])
        self.assertEqual(sample["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(sample["metadata"]["candidate_count"], 1)
        self.assertEqual(sample["rows"][0]["accession"], "P12345")
        self.assertFalse(sample["rows"][0]["countable_label_candidate"])

    def test_candidate_sample_audit_blocks_countable_external_rows(self) -> None:
        audit = audit_external_source_candidate_sample(
            {
                "rows": [
                    {
                        "accession": "P12345",
                        "reviewed": "reviewed",
                        "ec_numbers": ["2.7.1.1"],
                        "alphafold_ids": ["AF-P12345-F1"],
                        "countable_label_candidate": True,
                        "ready_for_label_import": True,
                    }
                ]
            }
        )

        self.assertFalse(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 1)
        self.assertEqual(audit["metadata"]["import_ready_row_count"], 1)
        self.assertEqual(audit["metadata"]["reviewed_count"], 1)
        self.assertIn("external_rows_marked_countable", audit["blockers"])
        self.assertIn("external_rows_marked_ready_for_import", audit["blockers"])

    def test_candidate_manifest_adds_sequence_and_ood_controls(self) -> None:
        manifest = build_external_source_candidate_manifest(
            candidate_sample={
                "metadata": {"method": "external_source_candidate_sample"},
                "rows": [
                    {
                        "accession": "P12345",
                        "lane_id": "external_source:transferase_phosphoryl",
                        "scope_signal": "transferase_phosphoryl",
                        "protein_name": "Example kinase",
                        "reviewed": "reviewed",
                        "ec_numbers": ["2.7.1.1"],
                        "pdb_ids": ["1ABC"],
                        "alphafold_ids": ["P12345"],
                    }
                ],
            },
            ood_calibration_plan={
                "rows": [
                    {
                        "lane_id": "external_source:transferase_phosphoryl",
                        "calibration_controls": [
                            "exact_sequence_cluster_exclusion",
                            "heuristic_retrieval_control_comparison",
                        ],
                        "promotion_rule": "review-only until gated",
                    }
                ]
            },
            sequence_clusters={
                "metadata": {"cluster_source": "reference_uniprot_exact_set"},
                "rows": [
                    {
                        "entry_id": "m_csa:1",
                        "reference_uniprot_ids": ["P12345"],
                        "sequence_cluster_id": "uniprot:P12345",
                    }
                ],
            },
            sequence_similarity_failure_sets={
                "rows": [{"sequence_cluster_id": "uniprot:P12345"}]
            },
            transfer_manifest={
                "metadata": {
                    "manifest_recommendation": (
                        "prototype_external_source_transfer_before_next_count_growth"
                    )
                }
            },
        )

        self.assertFalse(manifest["metadata"]["ready_for_label_import"])
        self.assertEqual(manifest["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(manifest["metadata"]["exact_reference_overlap_count"], 1)
        self.assertEqual(manifest["metadata"]["sequence_failure_set_overlap_count"], 1)
        self.assertEqual(manifest["metadata"]["missing_ood_lane_count"], 0)
        row = manifest["rows"][0]
        self.assertFalse(row["countable_label_candidate"])
        self.assertFalse(row["ready_for_label_import"])
        self.assertIn(
            "exact_sequence_cluster_overlap_existing_m_csa", row["blockers"]
        )
        self.assertTrue(
            row["external_source_controls"]["heuristic_baseline_control_required"]
        )
        self.assertEqual(
            row["external_source_controls"]["sequence_similarity_control"][
                "matched_m_csa_entry_ids"
            ],
            ["m_csa:1"],
        )

    def test_candidate_manifest_audit_blocks_import_ready_rows(self) -> None:
        audit = audit_external_source_candidate_manifest(
            {
                "rows": [
                    {
                        "accession": "P12345",
                        "countable_label_candidate": False,
                        "ready_for_label_import": True,
                        "external_source_controls": {
                            "heuristic_baseline_control_required": True,
                            "ood_calibration_controls": [
                                "heuristic_retrieval_control_comparison"
                            ],
                            "sequence_similarity_control": {
                                "exact_reference_overlap": False
                            },
                        },
                    }
                ]
            }
        )

        self.assertFalse(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["import_ready_row_count"], 1)
        self.assertIn(
            "external_manifest_rows_marked_ready_for_import", audit["blockers"]
        )

    def test_sequence_holdout_audit_keeps_external_overlap_rows_non_countable(
        self,
    ) -> None:
        audit = audit_external_source_sequence_holdouts(
            candidate_manifest={
                "metadata": {
                    "method": "external_source_candidate_manifest",
                    "candidate_count": 2,
                },
                "rows": [
                    {
                        "accession": "P12345",
                        "countable_label_candidate": False,
                        "external_source_controls": {
                            "sequence_similarity_control": {
                                "exact_reference_overlap": True,
                                "matched_m_csa_entry_ids": ["m_csa:1"],
                                "sequence_cluster_ids": ["uniprot:P12345"],
                                "sequence_failure_set_overlap": False,
                            }
                        },
                        "lane_id": "external_source:lyase",
                        "ready_for_label_import": False,
                    },
                    {
                        "accession": "Q99999",
                        "countable_label_candidate": False,
                        "external_source_controls": {
                            "sequence_similarity_control": {
                                "exact_reference_overlap": False,
                                "sequence_failure_set_overlap": False,
                            }
                        },
                        "lane_id": "external_source:isomerase",
                        "ready_for_label_import": False,
                    },
                ],
            }
        )

        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertFalse(audit["metadata"]["ready_for_label_import"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            audit["metadata"]["exact_reference_overlap_holdout_count"], 1
        )
        self.assertEqual(
            audit["metadata"]["near_duplicate_search_candidate_count"], 1
        )
        self.assertEqual(
            audit["rows"][0]["holdout_status"], "exact_reference_overlap_holdout"
        )

    def test_external_source_evidence_plan_stays_review_only(self) -> None:
        plan = build_external_source_evidence_plan(
            candidate_manifest={
                "rows": [
                    {
                        "accession": "P12345",
                        "blockers": [
                            "external_mechanism_evidence_not_attached"
                        ],
                        "countable_label_candidate": False,
                        "ec_numbers": ["2.7.1.1"],
                        "alphafold_ids": ["P12345"],
                        "external_source_controls": {
                            "sequence_similarity_control": {
                                "exact_reference_overlap": True,
                                "matched_m_csa_entry_ids": ["m_csa:1"],
                            }
                        },
                        "lane_id": "external_source:transferase_phosphoryl",
                        "pdb_ids": ["1ABC"],
                        "protein_name": "Example kinase",
                        "ready_for_label_import": False,
                        "scope_signal": "transferase_phosphoryl",
                        "structure_reference_status": (
                            "pdb_or_alphafold_reference_present"
                        ),
                    }
                ]
            },
            candidate_manifest_audit={"metadata": {"guardrail_clean": True}},
        )

        self.assertFalse(plan["metadata"]["ready_for_label_import"])
        self.assertTrue(plan["metadata"]["ready_for_evidence_collection"])
        self.assertEqual(plan["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            plan["metadata"]["exact_reference_overlap_holdout_count"], 1
        )
        self.assertEqual(
            plan["rows"][0]["sequence_similarity_bucket"],
            "exact_reference_overlap_holdout",
        )
        self.assertEqual(
            plan["rows"][0]["next_action"],
            "route_exact_reference_overlap_to_holdout_control",
        )
        self.assertIn(
            "active_site_residue_positions", plan["rows"][0]["required_evidence"]
        )
        self.assertEqual(plan["rows"][0]["pdb_ids"], ["1ABC"])
        self.assertEqual(plan["rows"][0]["alphafold_ids"], ["P12345"])

    def test_external_source_evidence_plan_routes_broad_ec_context(self) -> None:
        plan = build_external_source_evidence_plan(
            candidate_manifest={
                "rows": [
                    {
                        "accession": "P12345",
                        "blockers": [
                            "external_mechanism_evidence_not_attached"
                        ],
                        "countable_label_candidate": False,
                        "ec_numbers": ["1.11.1.-"],
                        "alphafold_ids": ["P12345"],
                        "external_source_controls": {
                            "sequence_similarity_control": {
                                "exact_reference_overlap": False,
                                "matched_m_csa_entry_ids": [],
                            }
                        },
                        "lane_id": "external_source:oxidoreductase_long_tail",
                        "pdb_ids": ["1ABC"],
                        "protein_name": "Example oxidoreductase",
                        "ready_for_label_import": False,
                        "scope_signal": "oxidoreductase_long_tail",
                        "structure_reference_status": (
                            "pdb_or_alphafold_reference_present"
                        ),
                    }
                ]
            },
            candidate_manifest_audit={"metadata": {"guardrail_clean": True}},
        )

        self.assertFalse(plan["metadata"]["ready_for_label_import"])
        self.assertEqual(
            plan["metadata"]["broad_or_incomplete_ec_candidate_count"], 1
        )
        self.assertEqual(
            plan["metadata"]["broad_or_incomplete_ec_only_candidate_count"], 1
        )
        self.assertEqual(
            plan["metadata"]["broad_or_incomplete_ec_numbers"], ["1.11.1.-"]
        )
        self.assertEqual(
            plan["rows"][0]["next_action"],
            "resolve_broad_or_incomplete_ec_before_active_site_mapping",
        )
        self.assertEqual(
            plan["rows"][0]["ec_specificity_bucket"],
            "broad_or_incomplete_ec_only",
        )
        self.assertIn(
            "specific_reaction_disambiguation_for_broad_ec",
            plan["rows"][0]["required_evidence"],
        )

    def test_active_site_evidence_queue_separates_ready_and_deferred_rows(self) -> None:
        queue = build_external_source_active_site_evidence_queue(
            evidence_plan={
                "metadata": {"method": "external_source_evidence_plan"},
                "rows": [
                    {
                        "accession": "P22222",
                        "alphafold_ids": ["P22222"],
                        "broad_or_incomplete_ec_numbers": [],
                        "countable_label_candidate": False,
                        "ec_specificity_bucket": "specific_ec_only",
                        "lane_id": "external_source:lyase",
                        "next_action": "collect_active_site_and_mechanism_evidence",
                        "pdb_ids": ["2ABC", "3ABC"],
                        "ready_for_label_import": False,
                        "required_evidence": ["active_site_residue_positions"],
                        "scope_signal": "lyase",
                        "sequence_similarity_bucket": "requires_near_duplicate_search",
                        "specific_ec_numbers": ["4.1.1.1"],
                    },
                    {
                        "accession": "P11111",
                        "alphafold_ids": ["P11111"],
                        "broad_or_incomplete_ec_numbers": ["1.11.1.-"],
                        "countable_label_candidate": False,
                        "ec_specificity_bucket": "broad_or_incomplete_ec_only",
                        "lane_id": "external_source:oxidoreductase_long_tail",
                        "next_action": (
                            "resolve_broad_or_incomplete_ec_before_active_site_mapping"
                        ),
                        "pdb_ids": ["1ABC"],
                        "ready_for_label_import": False,
                        "required_evidence": [
                            "specific_reaction_disambiguation_for_broad_ec"
                        ],
                        "scope_signal": "oxidoreductase_long_tail",
                        "sequence_similarity_bucket": "requires_near_duplicate_search",
                        "specific_ec_numbers": [],
                    },
                ],
            },
            max_rows=5,
        )

        self.assertFalse(queue["metadata"]["ready_for_label_import"])
        self.assertEqual(queue["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(queue["metadata"]["ready_candidate_count"], 1)
        self.assertEqual(queue["metadata"]["deferred_candidate_count"], 1)
        self.assertEqual(
            queue["metadata"]["queue_status_counts"][
                "ready_for_active_site_evidence"
            ],
            1,
        )
        self.assertEqual(queue["rows"][0]["accession"], "P22222")
        self.assertEqual(
            queue["deferred_rows"][0]["queue_status"],
            "defer_broad_ec_disambiguation",
        )

    def test_active_site_evidence_sample_collects_review_only_uniprot_features(
        self,
    ) -> None:
        def fake_fetcher(accession: str) -> dict:
            self.assertEqual(accession, "P22222")
            return {
                "record": {
                    "entry_name": "LYASE_EXAMPLE",
                    "entry_type": "Swiss-Prot",
                    "active_site_features": [
                        {
                            "begin": 42,
                            "description": "Proton acceptor",
                            "end": 42,
                            "evidence": [
                                {
                                    "evidence_code": "ECO:0000269",
                                    "source": "PubMed",
                                    "id": "123",
                                }
                            ],
                            "feature_type": "Active site",
                        }
                    ],
                    "binding_site_features": [
                        {
                            "begin": 101,
                            "description": "",
                            "end": 101,
                            "feature_type": "Binding site",
                            "ligand_name": "magnesium",
                        }
                    ],
                    "catalytic_activity_comments": [
                        {"reaction": "substrate = product", "ec_number": "4.1.1.1"}
                    ],
                    "cofactor_comments": [{"cofactors": [{"name": "Mg(2+)"}]}],
                }
            }

        sample = build_external_source_active_site_evidence_sample(
            active_site_evidence_queue={
                "metadata": {"method": "external_source_active_site_evidence_queue"},
                "rows": [
                    {
                        "accession": "P22222",
                        "broad_or_incomplete_ec_numbers": [],
                        "countable_label_candidate": False,
                        "lane_id": "external_source:lyase",
                        "pdb_ids": ["2ABC"],
                        "protein_name": "Example lyase",
                        "queue_status": "ready_for_active_site_evidence",
                        "rank": 1,
                        "ready_for_label_import": False,
                        "scope_signal": "lyase",
                        "specific_ec_numbers": ["4.1.1.1"],
                    },
                    {
                        "accession": "P11111",
                        "queue_status": "defer_broad_ec_disambiguation",
                    },
                ],
            },
            max_candidates=5,
            fetcher=fake_fetcher,
        )

        self.assertFalse(sample["metadata"]["ready_for_label_import"])
        self.assertEqual(sample["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(sample["metadata"]["candidate_count"], 1)
        self.assertEqual(
            sample["metadata"]["candidate_with_active_site_feature_count"], 1
        )
        self.assertEqual(sample["metadata"]["active_site_feature_count"], 1)
        self.assertEqual(sample["metadata"]["binding_site_feature_count"], 1)
        self.assertEqual(sample["metadata"]["catalytic_activity_count"], 1)
        self.assertEqual(sample["metadata"]["skipped_queue_row_count"], 1)
        self.assertEqual(
            sample["candidate_summaries"][0]["evidence_status"],
            "active_site_and_catalytic_activity_context_found",
        )
        self.assertFalse(sample["candidate_summaries"][0]["countable_label_candidate"])
        self.assertEqual(sample["rows"][0]["feature_type"], "Active site")
        self.assertFalse(sample["rows"][0]["ready_for_label_import"])

    def test_active_site_evidence_sample_deferred_gap_stays_non_countable(
        self,
    ) -> None:
        sample = build_external_source_active_site_evidence_sample(
            active_site_evidence_queue={
                "metadata": {"method": "external_source_active_site_evidence_queue"},
                "rows": [
                    {
                        "accession": "P33333",
                        "broad_or_incomplete_ec_numbers": [],
                        "countable_label_candidate": False,
                        "lane_id": "external_source:isomerase",
                        "pdb_ids": ["3ABC"],
                        "protein_name": "Example isomerase",
                        "queue_status": "ready_for_active_site_evidence",
                        "rank": 1,
                        "ready_for_label_import": False,
                        "scope_signal": "isomerase",
                        "specific_ec_numbers": ["5.3.1.1"],
                    }
                ],
            },
            max_candidates=1,
            fetcher=lambda accession: {
                "record": {
                    "entry_name": "ISOM_EXAMPLE",
                    "active_site_features": [],
                    "binding_site_features": [],
                    "catalytic_activity_comments": [],
                    "cofactor_comments": [],
                }
            },
        )
        audit = audit_external_source_active_site_evidence_sample(sample)

        self.assertEqual(
            sample["candidate_summaries"][0]["evidence_status"],
            "active_site_feature_missing",
        )
        self.assertIn(
            "uniprot_active_site_feature_missing",
            sample["candidate_summaries"][0]["blockers"],
        )
        self.assertEqual(sample["metadata"]["countable_label_candidate_count"], 0)
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["active_site_feature_gap_count"], 1)
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_active_site_evidence_audit_blocks_import_ready_rows(self) -> None:
        audit = audit_external_source_active_site_evidence_sample(
            {
                "candidate_summaries": [
                    {
                        "accession": "P33333",
                        "countable_label_candidate": True,
                        "ready_for_label_import": True,
                        "active_site_feature_count": 1,
                    }
                ],
                "rows": [
                    {
                        "accession": "P33333",
                        "countable_label_candidate": False,
                        "ready_for_label_import": False,
                        "evidence_status": "uniprot_feature_context_only",
                    }
                ],
            }
        )

        self.assertFalse(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 1)
        self.assertEqual(audit["metadata"]["import_ready_item_count"], 1)
        self.assertIn(
            "active_site_evidence_rows_marked_countable", audit["blockers"]
        )

    def test_heuristic_control_queue_splits_ready_and_deferred_candidates(
        self,
    ) -> None:
        queue = build_external_source_heuristic_control_queue(
            active_site_evidence_sample={
                "metadata": {"method": "external_source_active_site_evidence_sample"},
                "candidate_summaries": [
                    {
                        "accession": "P22222",
                        "active_site_feature_count": 2,
                        "binding_site_feature_count": 1,
                        "broad_or_incomplete_ec_numbers": [],
                        "catalytic_activity_count": 1,
                        "countable_label_candidate": False,
                        "lane_id": "external_source:lyase",
                        "pdb_ids_sample": ["2ABC"],
                        "protein_name": "Example lyase",
                        "queue_rank": 1,
                        "ready_for_label_import": False,
                        "scope_signal": "lyase",
                        "specific_ec_numbers": ["4.1.1.1"],
                    },
                    {
                        "accession": "P33333",
                        "active_site_feature_count": 0,
                        "binding_site_feature_count": 3,
                        "broad_or_incomplete_ec_numbers": [],
                        "catalytic_activity_count": 1,
                        "countable_label_candidate": False,
                        "lane_id": "external_source:glycan_chemistry",
                        "pdb_ids_sample": ["3ABC"],
                        "protein_name": "Binding-only example",
                        "queue_rank": 2,
                        "ready_for_label_import": False,
                        "scope_signal": "glycan_chemistry",
                        "specific_ec_numbers": ["3.2.2.21"],
                    },
                ],
            }
        )
        audit = audit_external_source_heuristic_control_queue(queue)

        self.assertFalse(queue["metadata"]["ready_for_label_import"])
        self.assertTrue(queue["metadata"]["ready_for_heuristic_control_execution"])
        self.assertEqual(queue["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(queue["metadata"]["ready_candidate_count"], 1)
        self.assertEqual(queue["metadata"]["deferred_candidate_count"], 1)
        self.assertEqual(
            queue["rows"][0]["queue_status"],
            "ready_for_heuristic_control_prototype",
        )
        self.assertEqual(
            queue["deferred_rows"][0]["queue_status"],
            "defer_active_site_feature_gap",
        )
        self.assertIn(
            "uniprot_active_site_feature_missing",
            queue["deferred_rows"][0]["blockers"],
        )
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_structure_mapping_plan_uses_active_site_positions_and_stays_review_only(
        self,
    ) -> None:
        plan = build_external_source_structure_mapping_plan(
            active_site_evidence_sample={
                "rows": [
                    {
                        "accession": "P22222",
                        "begin": 42,
                        "description": "Proton acceptor",
                        "end": 42,
                        "evidence": [{"evidence_code": "ECO:0000269"}],
                        "feature_type": "Active site",
                    }
                ]
            },
            heuristic_control_queue={
                "metadata": {"method": "external_source_heuristic_control_queue"},
                "rows": [
                    {
                        "accession": "P22222",
                        "alphafold_ids_sample": ["AF-P22222-F1"],
                        "countable_label_candidate": False,
                        "heuristic_control_rank": 1,
                        "lane_id": "external_source:lyase",
                        "pdb_ids_sample": ["2ABC"],
                        "protein_name": "Example lyase",
                        "queue_status": "ready_for_heuristic_control_prototype",
                        "ready_for_label_import": False,
                        "scope_signal": "lyase",
                        "specific_ec_numbers": ["4.1.1.1"],
                    }
                ],
                "deferred_rows": [
                    {
                        "accession": "P33333",
                        "countable_label_candidate": False,
                        "queue_status": "defer_active_site_feature_gap",
                        "ready_for_label_import": False,
                    }
                ],
            },
        )
        audit = audit_external_source_structure_mapping_plan(plan)

        self.assertFalse(plan["metadata"]["ready_for_label_import"])
        self.assertTrue(plan["metadata"]["ready_for_structure_mapping"])
        self.assertEqual(plan["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(plan["metadata"]["ready_mapping_candidate_count"], 1)
        self.assertEqual(plan["metadata"]["deferred_mapping_candidate_count"], 1)
        self.assertEqual(plan["rows"][0]["active_site_position_count"], 1)
        self.assertEqual(
            plan["rows"][0]["mapping_status"], "ready_for_structure_mapping"
        )
        self.assertEqual(
            plan["deferred_rows"][0]["mapping_status"],
            "defer_before_structure_mapping",
        )
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_structure_mapping_sample_resolves_review_only_geometry(self) -> None:
        cif_text = """data_test
loop_
_atom_site.group_PDB
_atom_site.label_atom_id
_atom_site.auth_atom_id
_atom_site.label_comp_id
_atom_site.auth_comp_id
_atom_site.label_asym_id
_atom_site.auth_asym_id
_atom_site.label_seq_id
_atom_site.auth_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM CA CA GLY GLY A A 42 42 0.0 0.0 0.0
ATOM N N GLY GLY A A 42 42 1.0 0.0 0.0
ATOM CA CA SER SER A A 45 45 4.0 0.0 0.0
ATOM N N SER SER A A 45 45 5.0 0.0 0.0
HETATM C1 C1 ATP ATP A A 900 900 2.0 0.0 0.0
#
"""

        sample = build_external_source_structure_mapping_sample(
            structure_mapping_plan={
                "metadata": {"method": "external_source_structure_mapping_plan"},
                "rows": [
                    {
                        "accession": "P22222",
                        "active_site_positions": [
                            {"begin": 42, "description": "base", "end": 42},
                            {"begin": 45, "description": "acid", "end": 45},
                        ],
                        "alphafold_ids_sample": ["P22222"],
                        "countable_label_candidate": False,
                        "pdb_ids_sample": [],
                        "ready_for_label_import": False,
                    }
                ],
            },
            max_candidates=1,
            cif_fetcher=lambda source, structure_id: cif_text,
        )
        audit = audit_external_source_structure_mapping_sample(sample)

        self.assertFalse(sample["metadata"]["ready_for_label_import"])
        self.assertTrue(sample["metadata"]["ready_for_heuristic_control_scoring"])
        self.assertEqual(sample["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(sample["metadata"]["mapped_candidate_count"], 1)
        self.assertEqual(sample["entries"][0]["status"], "ok")
        self.assertEqual(sample["entries"][0]["resolved_residue_count"], 2)
        self.assertEqual(
            sample["entries"][0]["structure_source"],
            "alphafold",
        )
        self.assertEqual(sample["entries"][0]["structure_id"], "P22222")
        self.assertTrue(sample["entries"][0]["pairwise_distances_angstrom"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_heuristic_control_scores_stay_review_only(self) -> None:
        scores = build_external_source_heuristic_control_scores(
            structure_mapping_sample={
                "metadata": {"method": "external_source_structure_mapping_sample"},
                "entries": [
                    {
                        "entry_id": "uniprot:P22222",
                        "entry_name": None,
                        "scope_signal": "isomerase",
                        "status": "ok",
                        "resolved_residue_count": 2,
                        "residues": [
                            {
                                "code": "SER",
                                "roles": ["uniprot_active_site_feature"],
                                "ca": {"x": 0.0, "y": 0.0, "z": 0.0},
                            },
                            {
                                "code": "HIS",
                                "roles": ["uniprot_active_site_feature"],
                                "ca": {"x": 4.0, "y": 0.0, "z": 0.0},
                            },
                        ],
                        "pairwise_distances_angstrom": [
                            {
                                "left": "a",
                                "right": "b",
                                "distance": 4.0,
                                "coordinate_type": "ca_or_centroid",
                            }
                        ],
                        "ligand_context": {},
                        "pocket_context": {},
                    }
                ],
            },
            top_k=3,
        )
        audit = audit_external_source_heuristic_control_scores(scores)

        self.assertFalse(scores["metadata"]["ready_for_label_import"])
        self.assertEqual(scores["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(scores["metadata"]["candidate_count"], 1)
        self.assertEqual(len(scores["results"][0]["top_fingerprints"]), 3)
        self.assertFalse(scores["results"][0]["countable_label_candidate"])
        self.assertFalse(scores["results"][0]["ready_for_label_import"])
        self.assertTrue(scores["results"][0]["scope_top1_mismatch"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertGreaterEqual(audit["metadata"]["control_finding_count"], 1)
        self.assertIn(
            "heuristic_control_scope_top1_mismatch", audit["control_findings"]
        )

    def test_external_failure_mode_audit_collects_review_only_findings(self) -> None:
        audit = audit_external_source_failure_modes(
            active_site_evidence_sample_audit={
                "metadata": {"active_site_feature_gap_count": 2}
            },
            heuristic_control_queue={
                "metadata": {
                    "queue_status_counts": {
                        "defer_broad_ec_disambiguation": 1,
                        "ready_for_heuristic_control_prototype": 3,
                    }
                }
            },
            heuristic_control_scores_audit={
                "metadata": {"candidate_count": 4},
                "control_findings": ["heuristic_control_top1_fingerprint_collapse"],
            },
            structure_mapping_sample_audit={
                "metadata": {"unresolved_candidate_count": 0}
            },
        )

        self.assertFalse(audit["metadata"]["ready_for_label_import"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["failure_mode_count"], 3)
        self.assertEqual(
            [row["failure_mode"] for row in audit["rows"]],
            [
                "external_active_site_feature_gap",
                "external_broad_ec_disambiguation_needed",
                "heuristic_control_top1_fingerprint_collapse",
            ],
        )

    def test_external_failure_mode_audit_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            active_site_audit = root / "active_site_audit.json"
            heuristic_queue = root / "heuristic_queue.json"
            heuristic_scores_audit = root / "heuristic_scores_audit.json"
            structure_mapping_audit = root / "structure_mapping_audit.json"
            out = root / "failure_modes.json"
            active_site_audit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "active_site_feature_gap_count": 1,
                            "countable_label_candidate_count": 0,
                            "guardrail_clean": True,
                        }
                    }
                ),
                encoding="utf-8",
            )
            heuristic_queue.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "queue_status_counts": {
                                "defer_broad_ec_disambiguation": 1
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            heuristic_scores_audit.write_text(
                json.dumps(
                    {
                        "metadata": {"candidate_count": 2},
                        "control_findings": [
                            "heuristic_control_scope_top1_mismatch"
                        ],
                    }
                ),
                encoding="utf-8",
            )
            structure_mapping_audit.write_text(
                json.dumps({"metadata": {"unresolved_candidate_count": 0}}),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-external-source-failure-modes",
                    "--active-site-evidence-sample-audit",
                    str(active_site_audit),
                    "--heuristic-control-queue",
                    str(heuristic_queue),
                    "--heuristic-control-scores-audit",
                    str(heuristic_scores_audit),
                    "--structure-mapping-sample-audit",
                    str(structure_mapping_audit),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["metadata"]["failure_mode_count"], 3)
            self.assertFalse(payload["metadata"]["ready_for_label_import"])
            self.assertEqual(payload["metadata"]["countable_label_candidate_count"], 0)

    def test_external_control_repair_plan_covers_review_only_failures(self) -> None:
        plan = build_external_source_control_repair_plan(
            active_site_evidence_sample={
                "metadata": {"method": "external_source_active_site_evidence_sample"},
                "candidate_summaries": [
                    {
                        "accession": "P11111",
                        "active_site_feature_count": 0,
                        "binding_site_feature_count": 3,
                        "broad_or_incomplete_ec_numbers": [],
                        "catalytic_activity_count": 1,
                        "lane_id": "external_source:glycan_chemistry",
                        "protein_name": "Binding-only glycan candidate",
                        "ready_for_label_import": False,
                        "scope_signal": "glycan_chemistry",
                        "specific_ec_numbers": ["3.2.2.21"],
                    },
                    {
                        "accession": "P22222",
                        "active_site_feature_count": 2,
                        "binding_site_feature_count": 1,
                        "broad_or_incomplete_ec_numbers": ["1.1.1.-"],
                        "catalytic_activity_count": 1,
                        "lane_id": "external_source:oxidoreductase_long_tail",
                        "protein_name": "Broad EC candidate",
                        "ready_for_label_import": False,
                        "scope_signal": "oxidoreductase_long_tail",
                        "specific_ec_numbers": [],
                    },
                ],
            },
            heuristic_control_scores={
                "metadata": {"method": "external_source_heuristic_control_scores"},
                "results": [
                    {
                        "entry_id": "uniprot:P33333",
                        "external_lane_id": "external_source:isomerase",
                        "external_scope_signal": "isomerase",
                        "protein_name": "Isomerase control",
                        "ready_for_label_import": False,
                        "scope_top1_mismatch": True,
                        "specific_ec_numbers": ["5.3.1.1"],
                        "top_fingerprints": [
                            {"fingerprint_id": "metal_dependent_hydrolase"}
                        ],
                    }
                ],
            },
            heuristic_control_scores_audit={
                "control_findings": [
                    "heuristic_control_top1_fingerprint_collapse",
                    "heuristic_control_metal_hydrolase_collapse",
                    "heuristic_control_scope_top1_mismatch",
                ]
            },
            external_failure_mode_audit={
                "metadata": {"method": "external_source_failure_mode_audit"},
                "rows": [
                    {"failure_mode": "external_active_site_feature_gap"},
                    {"failure_mode": "external_broad_ec_disambiguation_needed"},
                    {"failure_mode": "heuristic_control_top1_fingerprint_collapse"},
                    {"failure_mode": "heuristic_control_metal_hydrolase_collapse"},
                    {"failure_mode": "heuristic_control_scope_top1_mismatch"},
                ],
            },
        )
        audit = audit_external_source_control_repair_plan(
            control_repair_plan=plan,
            external_failure_mode_audit={
                "metadata": {
                    "active_site_feature_gap_count": 1,
                    "broad_ec_disambiguation_count": 1,
                    "failure_mode_count": 5,
                    "heuristic_control_finding_count": 3,
                }
            },
        )

        self.assertFalse(plan["metadata"]["ready_for_label_import"])
        self.assertEqual(plan["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(plan["metadata"]["active_site_gap_repair_count"], 1)
        self.assertEqual(plan["metadata"]["broad_ec_disambiguation_repair_count"], 1)
        self.assertEqual(plan["metadata"]["heuristic_control_repair_count"], 1)
        self.assertTrue(
            plan["metadata"]["repair_plan_complete_for_observed_failures"]
        )
        self.assertEqual(plan["metadata"]["uncovered_failure_modes"], [])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_external_control_repair_plan_counts_emitted_rows(self) -> None:
        plan = build_external_source_control_repair_plan(
            active_site_evidence_sample={
                "metadata": {"method": "external_source_active_site_evidence_sample"},
                "candidate_summaries": [
                    {
                        "accession": "P11111",
                        "active_site_feature_count": 0,
                        "broad_or_incomplete_ec_numbers": [],
                        "lane_id": "external_source:glycan_chemistry",
                        "ready_for_label_import": False,
                    },
                    {
                        "accession": "P22222",
                        "active_site_feature_count": 0,
                        "broad_or_incomplete_ec_numbers": [],
                        "lane_id": "external_source:isomerase",
                        "ready_for_label_import": False,
                    },
                ],
            },
            heuristic_control_scores={
                "metadata": {"method": "external_source_heuristic_control_scores"},
                "results": [],
            },
            heuristic_control_scores_audit={"control_findings": []},
            external_failure_mode_audit={
                "metadata": {"method": "external_source_failure_mode_audit"},
                "rows": [{"failure_mode": "external_active_site_feature_gap"}],
            },
            max_rows=1,
        )

        self.assertEqual(plan["metadata"]["repair_row_count"], 1)
        self.assertEqual(
            plan["metadata"]["row_type_counts"], {"active_site_feature_gap": 1}
        )
        self.assertEqual(
            sum(plan["metadata"]["repair_lane_counts"].values()), 1
        )
        self.assertEqual(len(plan["rows"]), 1)

    def test_external_control_repair_plan_cli_and_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            active_site_sample = root / "active_site_sample.json"
            heuristic_scores = root / "heuristic_scores.json"
            heuristic_scores_audit = root / "heuristic_scores_audit.json"
            failure_modes = root / "failure_modes.json"
            repair_plan = root / "repair_plan.json"
            repair_audit = root / "repair_audit.json"
            active_site_sample.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_active_site_evidence_sample"
                        },
                        "candidate_summaries": [
                            {
                                "accession": "P11111",
                                "active_site_feature_count": 0,
                                "binding_site_feature_count": 1,
                                "catalytic_activity_count": 1,
                                "countable_label_candidate": False,
                                "lane_id": "external_source:glycan_chemistry",
                                "ready_for_label_import": False,
                                "scope_signal": "glycan_chemistry",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            heuristic_scores.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "ready_for_label_import": False,
                            "countable_label_candidate_count": 0,
                        },
                        "results": [
                            {
                                "entry_id": "uniprot:P22222",
                                "countable_label_candidate": False,
                                "external_scope_signal": "isomerase",
                                "ready_for_label_import": False,
                                "scope_top1_mismatch": True,
                                "top_fingerprints": [
                                    {"fingerprint_id": "metal_dependent_hydrolase"}
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            heuristic_scores_audit.write_text(
                json.dumps(
                    {
                        "metadata": {"candidate_count": 1},
                        "control_findings": [
                            "heuristic_control_scope_top1_mismatch"
                        ],
                    }
                ),
                encoding="utf-8",
            )
            failure_modes.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "active_site_feature_gap_count": 1,
                            "failure_mode_count": 2,
                            "heuristic_control_finding_count": 1,
                        },
                        "rows": [
                            {"failure_mode": "external_active_site_feature_gap"},
                            {"failure_mode": "heuristic_control_scope_top1_mismatch"},
                        ],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-control-repair-plan",
                    "--active-site-evidence-sample",
                    str(active_site_sample),
                    "--heuristic-control-scores",
                    str(heuristic_scores),
                    "--heuristic-control-scores-audit",
                    str(heuristic_scores_audit),
                    "--external-failure-mode-audit",
                    str(failure_modes),
                    "--out",
                    str(repair_plan),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-external-source-control-repair-plan",
                    "--control-repair-plan",
                    str(repair_plan),
                    "--external-failure-mode-audit",
                    str(failure_modes),
                    "--out",
                    str(repair_audit),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            repair_payload = json.loads(repair_plan.read_text(encoding="utf-8"))
            audit_payload = json.loads(repair_audit.read_text(encoding="utf-8"))
            self.assertTrue(
                repair_payload["metadata"][
                    "repair_plan_complete_for_observed_failures"
                ]
            )
            self.assertTrue(audit_payload["metadata"]["guardrail_clean"])

            gates = check_external_source_transfer_gates(
                transfer_manifest={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                    }
                },
                query_manifest={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                    }
                },
                ood_calibration_plan={
                    "metadata": {
                        "ready_for_label_import": False,
                        "requires_heuristic_control": True,
                    }
                },
                candidate_sample_audit={
                    "metadata": {
                        "method": "external_source_sequence_reference_screen_audit",
                        "guardrail_clean": True,
                        "countable_label_candidate_count": 0,
                    }
                },
                candidate_manifest={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "heuristic_control_required": True,
                    }
                },
                candidate_manifest_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "countable_label_candidate_count": 0,
                    }
                },
                lane_balance_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "countable_label_candidate_count": 0,
                        "lane_count": 2,
                        "dominant_lane_fraction": 0.5,
                    }
                },
                evidence_plan={
                    "metadata": {
                        "ready_for_label_import": False,
                        "ready_for_evidence_collection": True,
                        "countable_label_candidate_count": 0,
                    }
                },
                evidence_request_export={
                    "metadata": {
                        "external_source_review_only": True,
                        "countable_label_candidate_count": 0,
                    }
                },
                review_only_import_safety_audit={
                    "metadata": {
                        "countable_import_safe": True,
                        "total_new_countable_label_count": 0,
                    }
                },
                external_control_repair_plan=repair_payload,
                external_control_repair_plan_audit=audit_payload,
                reaction_evidence_sample={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "reaction_record_count": 1,
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "evidence_status": "reaction_context_only",
                            "ready_for_label_import": False,
                        }
                    ],
                },
                reaction_evidence_sample_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "broad_ec_context_row_count": 0,
                    }
                },
                representation_control_manifest={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "eligible_control_count": 1,
                        "scope_top1_mismatch_count": 1,
                        "embedding_status": "not_computed_interface_only",
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "ready_for_label_import": False,
                        }
                    ],
                },
                representation_control_manifest_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                    }
                },
                representation_control_comparison={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "scope_top1_mismatch_count": 1,
                        "metal_hydrolase_collapse_flag_count": 1,
                        "embedding_status": "feature_proxy_no_embedding",
                    },
                    "rows": [
                        {
                            "comparison_status": (
                                "proxy_flags_metal_hydrolase_collapse"
                            ),
                            "countable_label_candidate": False,
                            "feature_proxy_tokens": ["scope:isomerase"],
                            "ready_for_label_import": False,
                        }
                    ],
                },
                representation_control_comparison_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                    }
                },
                representation_backend_plan={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "embedding_status": "backend_plan_only_not_computed",
                        "sequence_search_blocked_count": 0,
                        "heuristic_contrast_required_count": 1,
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "ready_for_label_import": False,
                            "recommended_backends": [
                                "active_site_contrastive_baseline"
                            ],
                            "required_inputs": [{"input_type": "candidate_sequence"}],
                            "review_status": "representation_backend_plan_review_only",
                        }
                    ],
                },
                representation_backend_plan_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "embedding_status": "backend_plan_only_not_computed",
                    }
                },
                representation_backend_sample={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "embedding_backend": "deterministic_sequence_kmer_control",
                        "embedding_status": "computed_review_only",
                        "representation_near_duplicate_alert_count": 1,
                    },
                    "rows": [
                        {
                            "backend_status": (
                                "representation_near_duplicate_holdout"
                            ),
                            "countable_label_candidate": False,
                            "ready_for_label_import": False,
                            "review_status": (
                                "representation_backend_sample_review_only"
                            ),
                        }
                    ],
                },
                representation_backend_sample_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "embedding_status": "computed_review_only",
                    }
                },
                broad_ec_disambiguation_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "specific_context_available_count": 1,
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "disambiguation_status": (
                                "specific_reaction_context_available_for_review"
                            ),
                            "ready_for_label_import": False,
                        }
                    ],
                },
                active_site_gap_source_requests={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "mapped_binding_context_request_count": 1,
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "ready_for_label_import": False,
                            "request_status": (
                                "binding_context_mapped_ready_for_active_site_sourcing"
                            ),
                        }
                    ],
                },
                sequence_neighborhood_plan={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "near_duplicate_search_request_count": 1,
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "plan_status": (
                                "near_duplicate_search_required_before_import"
                            ),
                            "ready_for_label_import": False,
                        }
                    ],
                },
                sequence_neighborhood_sample={
                    "metadata": {
                        "ready_for_label_import": False,
                        "complete_near_duplicate_search_required": True,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "reference_sequence_count": 1,
                        "high_similarity_candidate_count": 1,
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "ready_for_label_import": False,
                            "screen_status": "near_duplicate_candidate_holdout",
                        }
                    ],
                },
                sequence_neighborhood_sample_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "complete_near_duplicate_search_required": True,
                        "countable_label_candidate_count": 0,
                    }
                },
                sequence_alignment_verification={
                    "metadata": {
                        "ready_for_label_import": False,
                        "complete_near_duplicate_search_required": True,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "verified_pair_count": 1,
                        "alignment_alert_candidate_count": 1,
                        "alignment_deferred_pair_count": 0,
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "ready_for_label_import": False,
                            "verification_status": (
                                "alignment_near_duplicate_candidate_holdout"
                            ),
                        }
                    ],
                },
                sequence_alignment_verification_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "complete_near_duplicate_search_required": True,
                        "countable_label_candidate_count": 0,
                    }
                },
                sequence_reference_screen_audit={
                    "metadata": {
                        "method": "external_source_sequence_reference_screen_audit",
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "complete_near_duplicate_search_required": True,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "screened_reference_sequence_count": 1,
                        "current_reference_screen_complete": True,
                        "missing_reference_sequence_count": 0,
                        "incomplete_candidate_count": 0,
                        "blocker_removed": (
                            "external_pilot_current_reference_near_duplicate_screen"
                        ),
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "current_reference_screen_status": (
                                "current_reference_top_hits_aligned_no_alert"
                            ),
                            "ready_for_label_import": False,
                            "review_status": (
                                "sequence_reference_screen_audit_review_only"
                            ),
                        }
                    ],
                },
                sequence_search_export={
                    "metadata": {
                        "ready_for_label_import": False,
                        "complete_near_duplicate_search_required": True,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "near_duplicate_search_request_count": 1,
                        "current_reference_screen_complete_candidate_count": 1,
                        "source_sequence_reference_screen_audit_method": (
                            "external_source_sequence_reference_screen_audit"
                        ),
                        "blocker_removed": (
                            "external_pilot_current_reference_near_duplicate_screen"
                        ),
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "current_reference_screen": {
                                "status": (
                                    "current_reference_top_hits_aligned_no_alert"
                                )
                            },
                            "decision": {"decision_status": "no_decision"},
                            "ready_for_label_import": False,
                            "review_status": "sequence_search_export_review_only",
                            "search_task": (
                                "run_complete_uniref_or_all_vs_all_near_duplicate_search"
                            ),
                            "source_targets": [
                                {"source_id": "P11111", "source_type": "UniRef"}
                            ],
                        }
                    ],
                },
                sequence_search_export_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "complete_near_duplicate_search_required": True,
                        "countable_label_candidate_count": 0,
                        "completed_decision_count": 0,
                    }
                },
                external_import_readiness_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "label_import_ready_count": 0,
                        "candidate_count": 1,
                        "active_site_gap_count": 1,
                        "representation_control_issue_count": 1,
                    }
                },
                active_site_sourcing_queue={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "ready_sourcing_candidate_count": 1,
                        "text_source_candidate_count": 0,
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "queue_status": "ready_for_curated_active_site_sourcing",
                            "ready_for_label_import": False,
                        }
                    ],
                },
                active_site_sourcing_queue_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                    }
                },
                active_site_sourcing_export={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "source_target_count": 2,
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "decision": {"decision_status": "no_decision"},
                            "ready_for_label_import": False,
                            "review_status": (
                                "active_site_sourcing_export_review_only"
                            ),
                            "source_targets": [
                                {"source_id": "P11111", "source_type": "UniProtKB"}
                            ],
                            "source_task": (
                                "curate_active_site_positions_from_mapped_binding_context"
                            ),
                        }
                    ],
                },
                active_site_sourcing_export_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "completed_decision_count": 0,
                    }
                },
                active_site_sourcing_resolution={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "explicit_active_site_source_count": 0,
                    },
                    "rows": [
                        {
                            "active_site_source_status": (
                                "binding_and_reaction_context_only_no_active_site_positions"
                            ),
                            "countable_label_candidate": False,
                            "ready_for_label_import": False,
                            "review_status": (
                                "active_site_sourcing_resolution_review_only"
                            ),
                        }
                    ],
                },
                active_site_sourcing_resolution_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                    }
                },
                transfer_blocker_matrix={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "active_site_sourcing_export_candidate_count": 1,
                        "active_site_sourcing_resolution_candidate_count": 1,
                        "sequence_search_export_candidate_count": 1,
                        "representation_backend_plan_candidate_count": 1,
                        "representation_backend_sample_candidate_count": 1,
                    },
                    "rows": [
                        {
                            "active_site_sourcing": {
                                "decision_status": "no_decision",
                                "resolution_status": (
                                    "binding_and_reaction_context_only_no_active_site_positions"
                                ),
                            },
                            "blockers": ["full_label_factory_gate_not_run"],
                            "countable_label_candidate": False,
                            "ready_for_label_import": False,
                            "representation_backend": {
                                "sample_backend_status": (
                                    "representation_near_duplicate_holdout"
                                )
                            },
                            "review_status": (
                                "external_transfer_blocker_matrix_review_only"
                            ),
                            "sequence_search": {
                                "decision_status": "no_decision",
                                "search_task": (
                                    "run_complete_uniref_or_all_vs_all_"
                                    "near_duplicate_search"
                                ),
                            },
                        }
                    ],
                },
                transfer_blocker_matrix_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "completed_active_site_decision_count": 0,
                        "completed_sequence_decision_count": 0,
                    }
                },
                binding_context_repair_plan={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "ready_binding_context_candidate_count": 1,
                        "deferred_binding_context_candidate_count": 1,
                        "binding_position_count": 2,
                    },
                    "rows": [
                        {
                            "countable_label_candidate": False,
                            "ready_for_label_import": False,
                        }
                    ],
                },
                binding_context_repair_plan_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                    }
                },
                binding_context_mapping_sample={
                    "metadata": {
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "mapped_candidate_count": 1,
                    },
                    "entries": [
                        {
                            "countable_label_candidate": False,
                            "ready_for_label_import": False,
                        }
                    ],
                },
                binding_context_mapping_sample_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                    }
                },
                sequence_holdout_audit={
                    "metadata": {
                        "guardrail_clean": True,
                        "ready_for_label_import": False,
                        "countable_label_candidate_count": 0,
                        "candidate_count": 1,
                        "exact_reference_overlap_holdout_count": 1,
                        "near_duplicate_search_candidate_count": 0,
                    }
                },
            )

            self.assertTrue(
                gates["gates"]["external_control_repair_plan_review_only"]
            )
            self.assertTrue(
                gates["gates"][
                    "external_control_repair_plan_audit_guardrail_clean"
                ]
            )
            self.assertEqual(
                gates["metadata"]["external_control_repair_row_count"], 2
            )
            self.assertTrue(gates["gates"]["reaction_evidence_sample_review_only"])
            self.assertTrue(
                gates["gates"]["reaction_evidence_sample_audit_guardrail_clean"]
            )
            self.assertEqual(gates["metadata"]["reaction_evidence_record_count"], 1)
            self.assertTrue(
                gates["gates"]["representation_control_manifest_review_only"]
            )
            self.assertTrue(
                gates["gates"][
                    "representation_control_manifest_audit_guardrail_clean"
                ]
            )
            self.assertEqual(
                gates["metadata"]["representation_control_eligible_count"], 1
            )
            self.assertTrue(
                gates["gates"]["representation_control_comparison_review_only"]
            )
            self.assertTrue(
                gates["gates"][
                    "representation_control_comparison_audit_guardrail_clean"
                ]
            )
            self.assertEqual(
                gates["metadata"][
                    "representation_control_comparison_metal_collapse_count"
                ],
                1,
            )
            self.assertTrue(
                gates["gates"]["representation_backend_plan_review_only"]
            )
            self.assertTrue(
                gates["gates"][
                    "representation_backend_plan_audit_guardrail_clean"
                ]
            )
            self.assertEqual(
                gates["metadata"]["representation_backend_plan_candidate_count"], 1
            )
            self.assertEqual(
                gates["metadata"][
                    "representation_backend_plan_contrast_required_count"
                ],
                1,
            )
            self.assertTrue(
                gates["gates"]["broad_ec_disambiguation_audit_review_only"]
            )
            self.assertEqual(
                gates["metadata"]["broad_ec_specific_context_available_count"], 1
            )
            self.assertTrue(
                gates["gates"]["active_site_gap_source_requests_review_only"]
            )
            self.assertEqual(
                gates["metadata"]["active_site_gap_source_request_count"], 1
            )
            self.assertTrue(gates["gates"]["sequence_neighborhood_plan_review_only"])
            self.assertEqual(
                gates["metadata"][
                    "sequence_neighborhood_near_duplicate_search_request_count"
                ],
                1,
            )
            self.assertTrue(
                gates["gates"]["sequence_neighborhood_sample_review_only"]
            )
            self.assertTrue(
                gates["gates"][
                    "sequence_neighborhood_sample_audit_guardrail_clean"
                ]
            )
            self.assertEqual(
                gates["metadata"]["sequence_neighborhood_high_similarity_candidate_count"],
                1,
            )
            self.assertTrue(
                gates["gates"]["sequence_alignment_verification_review_only"]
            )
            self.assertTrue(
                gates["gates"][
                    "sequence_alignment_verification_audit_guardrail_clean"
                ]
            )
            self.assertEqual(
                gates["metadata"]["sequence_alignment_verified_pair_count"], 1
            )
            self.assertEqual(
                gates["metadata"]["sequence_alignment_alert_candidate_count"], 1
            )
            self.assertTrue(
                gates["gates"]["sequence_reference_screen_audit_guardrail_clean"]
            )
            self.assertEqual(
                gates["metadata"]["sequence_reference_screen_candidate_count"], 1
            )
            self.assertEqual(
                gates["metadata"][
                    "sequence_reference_screened_reference_sequence_count"
                ],
                1,
            )
            self.assertEqual(
                gates["metadata"][
                    "sequence_reference_screen_blocker_removed"
                ],
                "external_pilot_current_reference_near_duplicate_screen",
            )
            self.assertTrue(gates["gates"]["sequence_search_export_review_only"])
            self.assertTrue(
                gates["gates"]["sequence_search_export_audit_guardrail_clean"]
            )
            self.assertEqual(
                gates["metadata"][
                    "sequence_search_export_near_duplicate_request_count"
                ],
                1,
            )
            self.assertTrue(
                gates["gates"][
                    "external_import_readiness_audit_blocks_label_import"
                ]
            )
            self.assertEqual(
                gates["metadata"]["external_import_readiness_candidate_count"], 1
            )
            self.assertTrue(
                gates["gates"]["active_site_sourcing_queue_review_only"]
            )
            self.assertTrue(
                gates["gates"][
                    "active_site_sourcing_queue_audit_guardrail_clean"
                ]
            )
            self.assertEqual(
                gates["metadata"]["active_site_sourcing_queue_candidate_count"], 1
            )
            self.assertEqual(
                gates["metadata"]["active_site_sourcing_ready_candidate_count"], 1
            )
            self.assertTrue(
                gates["gates"]["active_site_sourcing_export_review_only"]
            )
            self.assertTrue(
                gates["gates"][
                    "active_site_sourcing_export_audit_guardrail_clean"
                ]
            )
            self.assertEqual(
                gates["metadata"]["active_site_sourcing_export_candidate_count"], 1
            )
            self.assertEqual(
                gates["metadata"][
                    "active_site_sourcing_export_completed_decision_count"
                ],
                0,
            )
            self.assertTrue(
                gates["gates"]["external_transfer_blocker_matrix_review_only"]
            )
            self.assertTrue(
                gates["gates"][
                    "external_transfer_blocker_matrix_audit_guardrail_clean"
                ]
            )
            self.assertEqual(
                gates["metadata"]["external_transfer_blocker_matrix_candidate_count"],
                1,
            )
            self.assertEqual(
                gates["metadata"][
                    "external_transfer_blocker_matrix_completed_decision_count"
                ],
                0,
            )
            self.assertTrue(gates["gates"]["binding_context_repair_plan_review_only"])
            self.assertTrue(
                gates["gates"][
                    "binding_context_repair_plan_audit_guardrail_clean"
                ]
            )
            self.assertEqual(gates["metadata"]["binding_context_position_count"], 2)
            self.assertTrue(
                gates["gates"]["binding_context_mapping_sample_review_only"]
            )
            self.assertTrue(
                gates["gates"][
                    "binding_context_mapping_sample_audit_guardrail_clean"
                ]
            )
            self.assertEqual(
                gates["metadata"]["binding_context_mapping_mapped_candidate_count"], 1
            )
            self.assertTrue(
                gates["gates"]["external_sequence_holdout_audit_guardrail_clean"]
            )
            self.assertEqual(
                gates["metadata"]["sequence_holdout_exact_overlap_count"], 1
            )

    def test_external_binding_context_repair_plan_separates_mappable_gaps(
        self,
    ) -> None:
        plan = build_external_source_binding_context_repair_plan(
            active_site_evidence_sample={
                "metadata": {"method": "external_source_active_site_evidence_sample"},
                "rows": [
                    {
                        "accession": "P11111",
                        "begin": 99,
                        "description": "substrate",
                        "end": 99,
                        "feature_type": "Binding site",
                        "ligand_name": "ATP",
                    }
                ],
            },
            control_repair_plan={
                "metadata": {"method": "external_source_control_repair_plan"},
                "rows": [
                    {
                        "accession": "P11111",
                        "lane_id": "external_source:transferase_phosphoryl",
                        "protein_name": "Binding gap",
                        "repair_lane": (
                            "map_binding_site_context_then_source_catalytic_positions"
                        ),
                        "repair_type": "active_site_feature_gap",
                        "scope_signal": "transferase_phosphoryl",
                    },
                    {
                        "accession": "P22222",
                        "lane_id": "external_source:transferase_methyl",
                        "protein_name": "No binding gap",
                        "repair_lane": (
                            "source_catalytic_positions_from_curated_literature"
                        ),
                        "repair_type": "active_site_feature_gap",
                        "scope_signal": "transferase_methyl",
                    },
                ],
            },
        )
        audit = audit_external_source_binding_context_repair_plan(plan)

        self.assertFalse(plan["metadata"]["ready_for_label_import"])
        self.assertEqual(plan["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(plan["metadata"]["candidate_count"], 2)
        self.assertEqual(plan["metadata"]["ready_binding_context_candidate_count"], 1)
        self.assertEqual(
            plan["metadata"]["deferred_binding_context_candidate_count"], 1
        )
        self.assertEqual(plan["metadata"]["binding_position_count"], 1)
        self.assertEqual(
            plan["rows"][0]["repair_status"],
            "ready_for_binding_context_mapping",
        )
        self.assertEqual(
            plan["rows"][1]["repair_status"], "defer_binding_context_missing"
        )
        self.assertTrue(audit["metadata"]["guardrail_clean"])

    def test_external_binding_context_mapping_sample_maps_review_only_positions(
        self,
    ) -> None:
        cif_text = """data_test
loop_
_atom_site.group_PDB
_atom_site.label_atom_id
_atom_site.auth_atom_id
_atom_site.label_comp_id
_atom_site.auth_comp_id
_atom_site.label_asym_id
_atom_site.auth_asym_id
_atom_site.label_seq_id
_atom_site.auth_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM CA CA GLY GLY A A 99 99 0.0 0.0 0.0
ATOM N N GLY GLY A A 99 99 1.0 0.0 0.0
HETATM C1 C1 ATP ATP A A 900 900 2.0 0.0 0.0
#
"""
        sample = build_external_source_binding_context_mapping_sample(
            binding_context_repair_plan={
                "metadata": {
                    "method": "external_source_binding_context_repair_plan"
                },
                "rows": [
                    {
                        "accession": "P11111",
                        "alphafold_ids_sample": ["P11111"],
                        "binding_positions": [
                            {
                                "begin": 99,
                                "end": 99,
                                "ligand_name": "ATP",
                            }
                        ],
                        "countable_label_candidate": False,
                        "ready_for_label_import": False,
                        "repair_status": "ready_for_binding_context_mapping",
                    }
                ],
            },
            max_candidates=1,
            cif_fetcher=lambda source, structure_id: cif_text,
        )
        audit = audit_external_source_binding_context_mapping_sample(sample)

        self.assertFalse(sample["metadata"]["ready_for_label_import"])
        self.assertEqual(sample["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(sample["metadata"]["mapped_candidate_count"], 1)
        self.assertEqual(sample["entries"][0]["status"], "ok")
        self.assertEqual(sample["entries"][0]["resolved_binding_position_count"], 1)
        self.assertFalse(sample["entries"][0]["countable_label_candidate"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_external_representation_control_manifest_stays_review_only(self) -> None:
        manifest = build_external_source_representation_control_manifest(
            structure_mapping_sample={
                "metadata": {"method": "external_source_structure_mapping_sample"},
                "entries": [
                    {
                        "accession": "P33333",
                        "entry_id": "uniprot:P33333",
                        "ligand_context": {"cofactor_families": ["metal"]},
                        "pairwise_distances_angstrom": [{"distance": 4.0}],
                        "pocket_context": {
                            "descriptors": {"polar_fraction": 0.5}
                        },
                        "protein_name": "Isomerase control",
                        "ready_for_label_import": False,
                        "resolved_residue_count": 2,
                        "residues": [{"code": "SER"}, {"code": "HIS"}],
                        "scope_signal": "isomerase",
                        "specific_ec_numbers": ["5.3.1.1"],
                        "status": "ok",
                        "structure_id": "P33333",
                        "structure_source": "alphafold",
                    }
                ],
            },
            heuristic_control_scores={
                "metadata": {"method": "external_source_heuristic_control_scores"},
                "results": [
                    {
                        "entry_id": "uniprot:P33333",
                        "scope_top1_mismatch": True,
                        "top_fingerprints": [
                            {
                                "fingerprint_id": "metal_dependent_hydrolase",
                                "score": 0.4,
                            }
                        ],
                    }
                ],
            },
            control_repair_plan={
                "metadata": {"method": "external_source_control_repair_plan"},
                "rows": [
                    {
                        "entry_id": "uniprot:P33333",
                        "repair_lane": (
                            "add_scope_specific_negative_control_and_representation_features"
                        ),
                        "repair_type": "heuristic_control_failure",
                    }
                ],
            },
        )
        audit = audit_external_source_representation_control_manifest(manifest)

        self.assertFalse(manifest["metadata"]["ready_for_label_import"])
        self.assertEqual(manifest["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(manifest["metadata"]["eligible_control_count"], 1)
        self.assertEqual(manifest["metadata"]["scope_top1_mismatch_count"], 1)
        self.assertFalse(manifest["rows"][0]["countable_label_candidate"])
        self.assertFalse(manifest["rows"][0]["ready_for_label_import"])
        self.assertEqual(
            manifest["rows"][0]["heuristic_baseline_control"]["repair_lane"],
            "add_scope_specific_negative_control_and_representation_features",
        )
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_external_representation_control_manifest_counts_emitted_rows(self) -> None:
        manifest = build_external_source_representation_control_manifest(
            structure_mapping_sample={
                "metadata": {"method": "external_source_structure_mapping_sample"},
                "entries": [
                    {
                        "accession": "P11111",
                        "entry_id": "uniprot:P11111",
                        "ligand_context": {},
                        "pocket_context": {"descriptors": {}},
                        "ready_for_label_import": False,
                        "resolved_residue_count": 1,
                        "residues": [{"code": "ASP"}],
                        "status": "ok",
                    },
                    {
                        "accession": "P22222",
                        "entry_id": "uniprot:P22222",
                        "ligand_context": {},
                        "pocket_context": {"descriptors": {}},
                        "ready_for_label_import": False,
                        "resolved_residue_count": 1,
                        "residues": [{"code": "HIS"}],
                        "status": "ok",
                    },
                ],
            },
            heuristic_control_scores={
                "metadata": {"method": "external_source_heuristic_control_scores"},
                "results": [
                    {
                        "entry_id": "uniprot:P11111",
                        "top_fingerprints": [
                            {"fingerprint_id": "metal_dependent_hydrolase"}
                        ],
                    },
                    {
                        "entry_id": "uniprot:P22222",
                        "top_fingerprints": [
                            {"fingerprint_id": "heme_peroxidase_oxidase"}
                        ],
                    },
                ],
            },
            control_repair_plan={
                "metadata": {"method": "external_source_control_repair_plan"},
                "rows": [],
            },
            max_rows=1,
        )

        self.assertEqual(manifest["metadata"]["candidate_count"], 1)
        self.assertEqual(
            manifest["metadata"]["top1_fingerprint_counts"],
            {"metal_dependent_hydrolase": 1},
        )
        self.assertEqual(len(manifest["rows"]), 1)

    def test_external_representation_control_comparison_flags_collapse(self) -> None:
        comparison = build_external_source_representation_control_comparison(
            representation_control_manifest={
                "metadata": {
                    "method": "external_source_representation_control_manifest"
                },
                "rows": [
                    {
                        "accession": "P11111",
                        "entry_id": "uniprot:P11111",
                        "feature_summary": {
                            "local_cofactor_families": [],
                            "pocket_descriptor_names": ["polar_fraction"],
                            "residue_codes": ["HIS", "GLU"],
                            "resolved_residue_count": 2,
                        },
                        "heuristic_baseline_control": {
                            "top1_fingerprint_id": "metal_dependent_hydrolase",
                            "top1_score": 0.5,
                        },
                        "lane_id": "external_source:isomerase",
                        "scope_signal": "isomerase",
                    },
                    {
                        "accession": "P22222",
                        "entry_id": "uniprot:P22222",
                        "feature_summary": {
                            "local_cofactor_families": [],
                            "pocket_descriptor_names": ["negative_fraction"],
                            "residue_codes": ["ASP", "ASP"],
                            "resolved_residue_count": 2,
                        },
                        "heuristic_baseline_control": {
                            "top1_fingerprint_id": "metal_dependent_hydrolase",
                            "top1_score": 0.7,
                        },
                        "lane_id": "external_source:glycan_chemistry",
                        "scope_signal": "glycan_chemistry",
                    },
                ],
            },
            heuristic_control_scores={
                "metadata": {"method": "external_source_heuristic_control_scores"},
                "results": [
                    {
                        "entry_id": "uniprot:P11111",
                        "top_fingerprints": [
                            {
                                "fingerprint_id": "metal_dependent_hydrolase",
                                "score": 0.5,
                            }
                        ],
                    },
                    {
                        "entry_id": "uniprot:P22222",
                        "top_fingerprints": [
                            {
                                "fingerprint_id": "metal_dependent_hydrolase",
                                "score": 0.7,
                            }
                        ],
                    },
                ],
            },
            reaction_evidence_sample={
                "metadata": {"method": "external_source_reaction_evidence_sample"},
                "rows": [
                    {
                        "entry_id": "uniprot:P11111",
                        "ec_number": "5.3.1.1",
                        "ec_specificity": "specific",
                        "rhea_id": "RHEA:11111",
                    },
                    {
                        "entry_id": "uniprot:P22222",
                        "ec_number": "3.2.1.22",
                        "ec_specificity": "specific",
                        "rhea_id": "RHEA:22222",
                    },
                ],
            },
        )
        audit = audit_external_source_representation_control_comparison(comparison)

        self.assertFalse(comparison["metadata"]["ready_for_label_import"])
        self.assertEqual(comparison["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            comparison["metadata"]["metal_hydrolase_collapse_flag_count"], 1
        )
        self.assertEqual(comparison["metadata"]["boundary_case_count"], 1)
        self.assertEqual(
            comparison["rows"][0]["comparison_status"],
            "proxy_flags_metal_hydrolase_collapse",
        )
        self.assertEqual(
            comparison["rows"][1]["comparison_status"],
            "proxy_boundary_case_requires_glycan_hydrolase_split",
        )
        self.assertIn(
            "reaction:specific", comparison["rows"][0]["feature_proxy_tokens"]
        )
        self.assertFalse(comparison["rows"][0]["countable_label_candidate"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_external_representation_backend_plan_keeps_embeddings_absent(self) -> None:
        plan = build_external_source_representation_backend_plan(
            representation_control_manifest={
                "metadata": {
                    "method": "external_source_representation_control_manifest"
                },
                "rows": [
                    {
                        "accession": "P11111",
                        "eligible_for_representation_control": True,
                        "entry_id": "uniprot:P11111",
                        "feature_summary": {
                            "resolved_residue_count": 2,
                            "structure_id": "AF-P11111-F1",
                            "structure_source": "alphafold",
                        },
                        "heuristic_baseline_control": {
                            "scope_top1_mismatch": True,
                            "top1_fingerprint_id": "metal_dependent_hydrolase",
                        },
                        "scope_signal": "transferase_phosphoryl",
                    },
                    {
                        "accession": "P22222",
                        "eligible_for_representation_control": True,
                        "entry_id": "uniprot:P22222",
                        "feature_summary": {"resolved_residue_count": 2},
                        "heuristic_baseline_control": {
                            "scope_top1_mismatch": False,
                            "top1_fingerprint_id": "heme_peroxidase_oxidase",
                        },
                        "scope_signal": "oxidoreductase_long_tail",
                    },
                ],
            },
            representation_control_comparison={
                "metadata": {
                    "method": "external_source_representation_control_comparison"
                },
                "rows": [
                    {
                        "comparison_status": "proxy_flags_metal_hydrolase_collapse",
                        "entry_id": "uniprot:P11111",
                    },
                    {
                        "comparison_status": "proxy_consistent_with_heuristic_scope",
                        "entry_id": "uniprot:P22222",
                    },
                ],
            },
            sequence_search_export={
                "metadata": {"method": "external_source_sequence_search_export"},
                "rows": [
                    {
                        "accession": "P11111",
                        "search_task": (
                            "run_complete_uniref_or_all_vs_all_near_duplicate_search"
                        ),
                    },
                    {
                        "accession": "P22222",
                        "search_task": "keep_sequence_holdout_control",
                    },
                ],
            },
        )
        audit = audit_external_source_representation_backend_plan(plan)

        self.assertFalse(plan["metadata"]["ready_for_label_import"])
        self.assertEqual(plan["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            plan["metadata"]["embedding_status"], "backend_plan_only_not_computed"
        )
        self.assertEqual(plan["metadata"]["candidate_count"], 2)
        self.assertEqual(
            plan["rows"][0]["backend_readiness_status"],
            "ready_for_backend_selection_not_embedding",
        )
        self.assertEqual(
            plan["rows"][1]["backend_readiness_status"],
            "blocked_by_sequence_holdout_control",
        )
        self.assertIn(
            "active_site_contrastive_baseline",
            plan["rows"][0]["recommended_backends"],
        )
        self.assertEqual(
            plan["rows"][0]["review_status"],
            "representation_backend_plan_review_only",
        )
        self.assertFalse(plan["rows"][0]["countable_label_candidate"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["missing_review_only_status_row_count"], 0)

    def test_external_representation_backend_sample_is_review_only(self) -> None:
        plan = {
            "metadata": {"method": "external_source_representation_backend_plan"},
            "rows": [
                {
                    "accession": "P11111",
                    "backend_readiness_status": (
                        "ready_for_backend_selection_not_embedding"
                    ),
                    "comparison_status": "proxy_flags_metal_hydrolase_collapse",
                    "countable_label_candidate": False,
                    "entry_id": "uniprot:P11111",
                    "heuristic_baseline_control": {
                        "scope_top1_mismatch": True,
                        "top1_fingerprint_id": "metal_dependent_hydrolase",
                    },
                    "lane_id": "external_source:isomerase",
                    "ready_for_label_import": False,
                    "scope_signal": "isomerase",
                    "sequence_search_task": (
                        "run_complete_uniref_or_all_vs_all_near_duplicate_search"
                    ),
                }
            ],
        }
        sequence_sample = {
            "metadata": {"method": "external_source_sequence_neighborhood_sample"},
            "rows": [
                {
                    "accession": "P11111",
                    "top_matches": [
                        {
                            "matched_m_csa_entry_ids": ["m_csa:1"],
                            "near_duplicate_score": 0.2,
                            "reference_accession": "P22222",
                        }
                    ],
                }
            ],
        }

        def fake_fetcher(accessions: list[str]) -> dict[str, object]:
            self.assertEqual(sorted(accessions), ["P11111", "P22222"])
            return {
                "metadata": {"source": "fake_sequence_records"},
                "records": [
                    {"accession": "P11111", "sequence": "ACDEFGHIKLMNPQRSTVWY"},
                    {"accession": "P22222", "sequence": "ACDEYGHIKLMNPQRSTVWY"},
                ],
            }

        sample = build_external_source_representation_backend_sample(
            representation_backend_plan=plan,
            sequence_neighborhood_sample=sequence_sample,
            fetcher=fake_fetcher,
        )
        audit = audit_external_source_representation_backend_sample(sample)

        self.assertFalse(sample["metadata"]["ready_for_label_import"])
        self.assertEqual(sample["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(sample["metadata"]["candidate_count"], 1)
        self.assertEqual(sample["metadata"]["embedding_status"], "computed_review_only")
        self.assertEqual(
            sample["metadata"]["predictive_feature_sources"],
            ["sequence_embedding_cosine", "sequence_length_coverage"],
        )
        self.assertEqual(
            sample["rows"][0]["review_status"],
            "representation_backend_sample_review_only",
        )
        self.assertEqual(
            sample["rows"][0]["embedding_backend"],
            "deterministic_sequence_kmer_control",
        )
        self.assertGreater(sample["rows"][0]["top_embedding_cosine"], 0.5)
        self.assertEqual(
            sample["rows"][0]["predictive_feature_sources"],
            ["sequence_embedding_cosine", "sequence_length_coverage"],
        )
        self.assertEqual(
            sample["rows"][0]["leakage_flags"],
            [
                "heuristic_fingerprint_id_review_context_only",
                "matched_m_csa_reference_ids_holdout_context_only",
                "source_scope_signal_review_context_only",
            ],
        )
        self.assertFalse(sample["rows"][0]["countable_label_candidate"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["missing_predictive_sources_row_count"], 0)

        broken_sample = json.loads(json.dumps(sample))
        broken_sample["rows"][0].pop("predictive_feature_sources")
        broken_audit = audit_external_source_representation_backend_sample(broken_sample)
        self.assertIn(
            "representation_backend_sample_rows_missing_predictive_sources",
            broken_audit["blockers"],
        )

        leakage_sample = json.loads(json.dumps(sample))
        leakage_sample["metadata"]["predictive_feature_sources"] = [
            "sequence_embedding_cosine",
            "ec_number_text_label",
        ]
        leakage_sample["rows"][0]["predictive_feature_sources"] = [
            "sequence_embedding_cosine",
            "mechanism_text_label",
        ]
        leakage_audit = audit_external_source_representation_backend_sample(
            leakage_sample
        )
        self.assertIn(
            "representation_backend_sample_leakage_prone_predictive_sources",
            leakage_audit["blockers"],
        )
        self.assertEqual(
            leakage_audit["metadata"]["leakage_prone_predictive_sources"],
            ["ec_number_text_label", "mechanism_text_label"],
        )

    def test_external_representation_backend_sample_accepts_learned_backend(self) -> None:
        plan = {
            "metadata": {"method": "external_source_representation_backend_plan"},
            "rows": [
                {
                    "accession": "P11111",
                    "backend_readiness_status": (
                        "ready_for_backend_selection_not_embedding"
                    ),
                    "comparison_status": "feature_proxy_boundary_case",
                    "countable_label_candidate": False,
                    "entry_id": "uniprot:P11111",
                    "heuristic_baseline_control": {
                        "scope_top1_mismatch": True,
                        "top1_fingerprint_id": "metal_dependent_hydrolase",
                    },
                    "lane_id": "external_source:isomerase",
                    "ready_for_label_import": False,
                    "scope_signal": "isomerase",
                    "sequence_search_task": (
                        "run_complete_uniref_or_all_vs_all_near_duplicate_search"
                    ),
                }
            ],
        }
        sequence_sample = {
            "metadata": {"method": "external_source_sequence_neighborhood_sample"},
            "rows": [
                {
                    "accession": "P11111",
                    "top_matches": [
                        {
                            "matched_m_csa_entry_ids": ["m_csa:1"],
                            "near_duplicate_score": 0.2,
                            "reference_accession": "P22222",
                        }
                    ],
                }
            ],
        }

        def fake_fetcher(accessions: list[str]) -> dict[str, object]:
            self.assertEqual(sorted(accessions), ["P11111", "P22222"])
            return {
                "metadata": {"source": "fake_sequence_records"},
                "records": [
                    {"accession": "P11111", "sequence": "ACDEFGHIKLMNPQRSTVWY"},
                    {"accession": "P22222", "sequence": "YYYYYGHIKLMNPQRSTVWY"},
                ],
            }

        fake_embedding_payload = {
            "metadata": {
                "embedding_backend": "esm2_t6_8m_ur50d",
                "embedding_backend_available": True,
                "embedding_failure_count": 0,
                "embedding_vector_dimension": 2,
                "model_name": "fake-esm2",
            },
            "embeddings_by_accession": {
                "P11111": [1.0, 0.0],
                "P22222": [0.0, 1.0],
            },
            "embedding_failures": [],
            "warnings": ["fake learned backend"],
            "warnings_by_accession": {},
        }

        with patch(
            "catalytic_earth.transfer_scope._compute_esm2_t6_embeddings",
            return_value=fake_embedding_payload,
        ):
            sample = build_external_source_representation_backend_sample(
                representation_backend_plan=plan,
                sequence_neighborhood_sample=sequence_sample,
                embedding_backend="esm2_t6_8m_ur50d",
                fetcher=fake_fetcher,
            )
        audit = audit_external_source_representation_backend_sample(sample)

        self.assertEqual(sample["metadata"]["embedding_backend"], "esm2_t6_8m_ur50d")
        self.assertTrue(sample["metadata"]["embedding_backend_available"])
        self.assertEqual(sample["metadata"]["embedding_vector_dimension"], 2)
        self.assertEqual(
            sample["rows"][0]["backend_status"],
            "learned_representation_sample_complete",
        )
        self.assertEqual(sample["metadata"]["learned_representation_complete_count"], 1)
        self.assertEqual(
            sample["metadata"]["predictive_feature_sources"],
            ["sequence_embedding_cosine", "sequence_length_coverage"],
        )
        self.assertEqual(
            sample["metadata"]["learned_vs_heuristic_disagreement_count"], 1
        )
        self.assertFalse(sample["rows"][0]["countable_label_candidate"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])

    def test_external_broad_ec_disambiguation_stays_review_only(self) -> None:
        audit = audit_external_source_broad_ec_disambiguation(
            control_repair_plan={
                "metadata": {"method": "external_source_control_repair_plan"},
                "rows": [
                    {
                        "accession": "P11111",
                        "broad_or_incomplete_ec_numbers": ["2.7.1.-"],
                        "countable_label_candidate": False,
                        "repair_type": "broad_ec_disambiguation",
                        "scope_signal": "transferase_phosphoryl",
                        "specific_ec_numbers": ["2.7.1.20"],
                    },
                    {
                        "accession": "P22222",
                        "broad_or_incomplete_ec_numbers": ["1.1.1.-"],
                        "countable_label_candidate": False,
                        "repair_type": "broad_ec_disambiguation",
                        "scope_signal": "oxidoreductase_long_tail",
                    },
                ],
            },
            reaction_evidence_sample={
                "metadata": {"method": "external_source_reaction_evidence_sample"},
                "rows": [
                    {
                        "entry_id": "uniprot:P11111",
                        "ec_number": "2.7.1.20",
                        "ec_specificity": "specific",
                        "rhea_id": "RHEA:11111",
                    },
                    {
                        "entry_id": "uniprot:P22222",
                        "ec_number": "1.1.1.-",
                        "ec_specificity": "broad_or_incomplete",
                        "rhea_id": "RHEA:22222",
                    },
                ],
            },
        )

        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertFalse(audit["metadata"]["ready_for_label_import"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(audit["metadata"]["candidate_count"], 2)
        self.assertEqual(audit["metadata"]["specific_context_available_count"], 1)
        self.assertEqual(
            audit["rows"][0]["disambiguation_status"],
            "specific_reaction_context_available_for_review",
        )
        self.assertEqual(
            audit["rows"][1]["disambiguation_status"],
            "specific_reaction_context_missing",
        )
        self.assertFalse(audit["rows"][0]["countable_label_candidate"])

    def test_external_active_site_gap_source_requests_are_non_countable(self) -> None:
        requests = build_external_source_active_site_gap_source_requests(
            control_repair_plan={
                "metadata": {"method": "external_source_control_repair_plan"},
                "rows": [
                    {
                        "accession": "P11111",
                        "alphafold_ids_sample": ["P11111"],
                        "binding_site_feature_count": 2,
                        "catalytic_activity_count": 1,
                        "countable_label_candidate": False,
                        "pdb_ids_sample": ["1ABC"],
                        "repair_type": "active_site_feature_gap",
                        "scope_signal": "transferase_phosphoryl",
                    },
                    {
                        "accession": "P22222",
                        "binding_site_feature_count": 0,
                        "catalytic_activity_count": 1,
                        "countable_label_candidate": False,
                        "repair_type": "active_site_feature_gap",
                        "scope_signal": "glycan_chemistry",
                    },
                ],
            },
            binding_context_repair_plan={
                "metadata": {"method": "external_source_binding_context_repair_plan"},
                "rows": [
                    {
                        "accession": "P11111",
                        "binding_position_count": 2,
                        "binding_positions": [
                            {
                                "evidence": [
                                    {
                                        "id": "1ABC",
                                        "source": "PDB",
                                    }
                                ],
                                "ligand_name": "ATP",
                            }
                        ],
                    }
                ],
            },
            binding_context_mapping_sample={
                "metadata": {
                    "method": "external_source_binding_context_mapping_sample"
                },
                "entries": [
                    {
                        "accession": "P11111",
                        "resolved_binding_position_count": 2,
                    }
                ],
            },
        )

        self.assertFalse(requests["metadata"]["ready_for_label_import"])
        self.assertEqual(requests["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(requests["metadata"]["candidate_count"], 2)
        self.assertEqual(
            requests["metadata"]["mapped_binding_context_request_count"], 1
        )
        self.assertEqual(
            requests["rows"][0]["request_status"],
            "binding_context_mapped_ready_for_active_site_sourcing",
        )
        self.assertEqual(
            requests["rows"][1]["request_status"],
            "reaction_text_only_needs_curated_residue_source",
        )
        self.assertFalse(requests["rows"][0]["countable_label_candidate"])

    def test_external_active_site_sourcing_queue_prioritizes_gap_rows(self) -> None:
        queue = build_external_source_active_site_sourcing_queue(
            active_site_gap_source_requests={
                "metadata": {
                    "method": "external_source_active_site_gap_source_requests"
                },
                "rows": [
                    {
                        "accession": "P11111",
                        "binding_evidence_reference_count": 2,
                        "mapped_binding_position_count": 4,
                        "request_status": (
                            "binding_context_mapped_ready_for_active_site_sourcing"
                        ),
                    },
                    {
                        "accession": "P22222",
                        "request_status": (
                            "reaction_text_only_needs_curated_residue_source"
                        ),
                    },
                ],
            },
            external_import_readiness_audit={
                "metadata": {
                    "method": "external_source_import_readiness_audit",
                    "active_site_gap_count": 2,
                },
                "rows": [
                    {
                        "accession": "P11111",
                        "readiness_status": "blocked_by_active_site_sourcing",
                    },
                    {
                        "accession": "P22222",
                        "readiness_status": "blocked_by_active_site_sourcing",
                    },
                ],
            },
        )
        audit = audit_external_source_active_site_sourcing_queue(
            active_site_sourcing_queue=queue,
            external_import_readiness_audit={
                "metadata": {"active_site_gap_count": 2},
                "rows": [],
            },
        )

        self.assertFalse(queue["metadata"]["ready_for_label_import"])
        self.assertEqual(queue["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(queue["metadata"]["candidate_count"], 2)
        self.assertEqual(queue["metadata"]["ready_sourcing_candidate_count"], 1)
        self.assertEqual(queue["metadata"]["text_source_candidate_count"], 1)
        self.assertEqual(
            queue["rows"][0]["queue_status"],
            "ready_for_curated_active_site_sourcing",
        )
        self.assertFalse(queue["rows"][0]["countable_label_candidate"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])

        truncated = build_external_source_active_site_sourcing_queue(
            active_site_gap_source_requests={
                "rows": [
                    {
                        "accession": "P11111",
                        "mapped_binding_position_count": 4,
                        "request_status": (
                            "binding_context_mapped_ready_for_active_site_sourcing"
                        ),
                    },
                    {
                        "accession": "P22222",
                        "request_status": (
                            "reaction_text_only_needs_curated_residue_source"
                        ),
                    },
                ]
            },
            external_import_readiness_audit={
                "metadata": {"active_site_gap_count": 2},
                "rows": [],
            },
            max_rows=1,
        )
        self.assertEqual(truncated["metadata"]["candidate_count"], 1)
        self.assertEqual(
            truncated["metadata"]["queue_status_counts"],
            {"ready_for_curated_active_site_sourcing": 1},
        )

    def test_external_active_site_sourcing_export_is_review_only(self) -> None:
        queue = {
            "metadata": {
                "method": "external_source_active_site_sourcing_queue",
                "candidate_count": 2,
            },
            "rows": [
                {
                    "accession": "P11111",
                    "entry_id": "uniprot:P11111",
                    "lane_id": "external_source:transferase_phosphoryl",
                    "mapped_binding_position_count": 2,
                    "priority_score": 12.0,
                    "protein_name": "Example kinase",
                    "queue_status": "ready_for_curated_active_site_sourcing",
                    "scope_signal": "transferase_phosphoryl",
                    "sequence_alignment_status": "alignment_no_near_duplicate_signal",
                    "specific_ec_numbers": ["2.7.1.1"],
                },
                {
                    "accession": "P22222",
                    "entry_id": "uniprot:P22222",
                    "lane_id": "external_source:glycan_chemistry",
                    "mapped_binding_position_count": 0,
                    "priority_score": 5.0,
                    "protein_name": "Example glycosylase",
                    "queue_status": "needs_primary_active_site_source",
                    "scope_signal": "glycan_chemistry",
                    "sequence_alignment_status": "alignment_no_near_duplicate_signal",
                    "specific_ec_numbers": ["3.2.2.21"],
                },
            ],
        }
        export = build_external_source_active_site_sourcing_export(
            active_site_sourcing_queue=queue,
            active_site_gap_source_requests={
                "metadata": {
                    "method": "external_source_active_site_gap_source_requests"
                },
                "rows": [
                    {
                        "accession": "P11111",
                        "alphafold_ids_sample": ["P11111"],
                        "binding_evidence_references": [
                            {
                                "id": "12345",
                                "ligand_name": "ATP",
                                "source": "PubMed",
                            }
                        ],
                        "mapped_binding_position_count": 2,
                        "pdb_ids_sample": ["1ABC"],
                        "request_status": (
                            "binding_context_mapped_ready_for_active_site_sourcing"
                        ),
                    },
                    {
                        "accession": "P22222",
                        "alphafold_ids_sample": ["P22222"],
                        "request_status": (
                            "reaction_text_only_needs_curated_residue_source"
                        ),
                    },
                ],
            },
            active_site_evidence_sample={
                "metadata": {"method": "external_source_active_site_evidence_sample"},
                "candidate_summaries": [
                    {"accession": "P11111", "pdb_ids_sample": ["1ABC"]},
                    {"accession": "P22222", "pdb_ids_sample": []},
                ],
                "rows": [
                    {
                        "accession": "P11111",
                        "begin": 10,
                        "end": 10,
                        "evidence": [
                            {
                                "evidence_code": "ECO:0000269",
                                "id": "12345",
                                "source": "PubMed",
                            }
                        ],
                        "feature_type": "Binding site",
                        "ligand_name": "ATP",
                    }
                ],
            },
            reaction_evidence_sample={
                "metadata": {"method": "external_source_reaction_evidence_sample"},
                "rows": [
                    {
                        "entry_id": "uniprot:P11111",
                        "ec_number": "2.7.1.1",
                        "ec_specificity": "specific",
                        "rhea_id": "RHEA:12345",
                    }
                ],
            },
        )
        audit = audit_external_source_active_site_sourcing_export(
            active_site_sourcing_export=export,
            active_site_sourcing_queue=queue,
        )

        self.assertFalse(export["metadata"]["ready_for_label_import"])
        self.assertEqual(export["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(export["metadata"]["candidate_count"], 2)
        self.assertEqual(export["metadata"]["decision_status_counts"], {"no_decision": 2})
        self.assertEqual(
            export["rows"][0]["source_task"],
            "curate_active_site_positions_from_mapped_binding_context",
        )
        self.assertEqual(
            export["rows"][1]["source_task"],
            "find_primary_active_site_or_residue_role_source",
        )
        self.assertFalse(export["rows"][0]["countable_label_candidate"])
        self.assertEqual(
            export["rows"][0]["decision"]["decision_status"], "no_decision"
        )
        self.assertEqual(
            export["rows"][0]["review_status"],
            "active_site_sourcing_export_review_only",
        )
        self.assertTrue(export["rows"][0]["source_targets"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["missing_review_only_status_row_count"], 0)

    def test_external_active_site_sourcing_resolution_is_review_only(self) -> None:
        export = {
            "metadata": {
                "method": "external_source_active_site_sourcing_export",
                "candidate_count": 2,
            },
            "rows": [
                {
                    "accession": "P11111",
                    "active_site_gap_request_status": (
                        "binding_context_mapped_ready_for_active_site_sourcing"
                    ),
                    "countable_label_candidate": False,
                    "entry_id": "uniprot:P11111",
                    "lane_id": "external_source:transferase_phosphoryl",
                    "protein_name": "Example kinase",
                    "queue_status": "ready_for_curated_active_site_sourcing",
                    "ready_for_label_import": False,
                    "scope_signal": "transferase_phosphoryl",
                    "source_task": "curate_active_site_positions_from_mapped_binding_context",
                },
                {
                    "accession": "P22222",
                    "active_site_gap_request_status": (
                        "reaction_text_only_needs_curated_residue_source"
                    ),
                    "countable_label_candidate": False,
                    "entry_id": "uniprot:P22222",
                    "lane_id": "external_source:glycan_chemistry",
                    "protein_name": "Example glycosylase",
                    "queue_status": "needs_primary_active_site_source",
                    "ready_for_label_import": False,
                    "scope_signal": "glycan_chemistry",
                    "source_task": "find_primary_active_site_or_residue_role_source",
                },
            ],
        }

        def fake_fetcher(accession: str) -> dict[str, object]:
            records = {
                "P11111": {
                    "record": {
                        "accession": "P11111",
                        "active_site_features": [
                            {
                                "begin": 42,
                                "end": 42,
                                "description": "Proton acceptor",
                                "evidence": [
                                    {
                                        "evidence_code": "ECO:0000269",
                                        "id": "12345",
                                        "source": "PubMed",
                                    }
                                ],
                                "feature_type": "Active site",
                            }
                        ],
                        "binding_site_features": [],
                        "catalytic_activity_comments": [{"reaction": "ATP + glucose"}],
                        "entry_name": "EXAMPLE_HUMAN",
                        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
                    }
                },
                "P22222": {
                    "record": {
                        "accession": "P22222",
                        "active_site_features": [],
                        "binding_site_features": [
                            {
                                "begin": 10,
                                "end": 10,
                                "evidence": [
                                    {
                                        "evidence_code": "ECO:0007744",
                                        "id": "1ABC",
                                        "source": "PDB",
                                    }
                                ],
                                "feature_type": "Binding site",
                            }
                        ],
                        "catalytic_activity_comments": [],
                    }
                },
            }
            return records[accession]

        resolution = build_external_source_active_site_sourcing_resolution(
            active_site_sourcing_export=export,
            fetcher=fake_fetcher,
        )
        audit = audit_external_source_active_site_sourcing_resolution(
            active_site_sourcing_resolution=resolution,
            active_site_sourcing_export=export,
        )

        self.assertFalse(resolution["metadata"]["ready_for_label_import"])
        self.assertEqual(resolution["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(resolution["metadata"]["candidate_count"], 2)
        self.assertEqual(resolution["metadata"]["explicit_active_site_source_count"], 1)
        self.assertEqual(
            resolution["rows"][0]["active_site_source_status"],
            "explicit_uniprot_active_site_positions_found",
        )
        self.assertEqual(
            resolution["rows"][1]["active_site_source_status"],
            "binding_context_only_no_active_site_positions",
        )
        self.assertEqual(
            resolution["rows"][0]["review_status"],
            "active_site_sourcing_resolution_review_only",
        )
        self.assertFalse(resolution["rows"][0]["countable_label_candidate"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])

    def test_external_sequence_neighborhood_plan_is_review_only(self) -> None:
        plan = build_external_source_sequence_neighborhood_plan(
            candidate_manifest={
                "metadata": {
                    "candidate_count": 2,
                    "method": "external_source_candidate_manifest",
                },
                "rows": [
                    {
                        "accession": "P11111",
                        "lane_id": "external_source:lyase",
                        "protein_name": "Lyase candidate",
                    },
                    {
                        "accession": "P22222",
                        "lane_id": "external_source:isomerase",
                        "protein_name": "Isomerase candidate",
                    },
                ],
            },
            sequence_holdout_audit={
                "metadata": {"method": "external_source_sequence_holdout_audit"},
                "rows": [
                    {
                        "accession": "P11111",
                        "holdout_status": "exact_reference_overlap_holdout",
                        "matched_m_csa_entry_ids": ["m_csa:1"],
                    },
                    {
                        "accession": "P22222",
                        "holdout_status": "requires_near_duplicate_search",
                    },
                ],
            },
        )

        self.assertFalse(plan["metadata"]["ready_for_label_import"])
        self.assertEqual(plan["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(plan["metadata"]["candidate_count"], 2)
        self.assertEqual(plan["metadata"]["exact_reference_overlap_holdout_count"], 1)
        self.assertEqual(plan["metadata"]["near_duplicate_search_request_count"], 1)
        self.assertEqual(
            plan["rows"][1]["plan_status"],
            "near_duplicate_search_required_before_import",
        )
        self.assertFalse(plan["rows"][0]["countable_label_candidate"])

    def test_external_sequence_search_export_stays_no_decision(self) -> None:
        export = build_external_source_sequence_search_export(
            sequence_neighborhood_plan={
                "metadata": {
                    "candidate_count": 2,
                    "method": "external_source_sequence_neighborhood_plan",
                },
                "rows": [
                    {
                        "accession": "P11111",
                        "entry_id": "uniprot:P11111",
                        "plan_status": (
                            "near_duplicate_search_required_before_import"
                        ),
                    },
                    {
                        "accession": "P22222",
                        "entry_id": "uniprot:P22222",
                        "plan_status": "exact_reference_overlap_keep_as_holdout",
                    },
                ],
            },
            sequence_neighborhood_sample={
                "metadata": {
                    "method": "external_source_sequence_neighborhood_sample"
                },
                "rows": [
                    {
                        "accession": "P11111",
                        "screen_status": "no_high_similarity_hit_in_bounded_screen",
                        "top_matches": [
                            {
                                "matched_m_csa_entry_ids": ["m_csa:1"],
                                "near_duplicate_score": 0.4,
                                "reference_accession": "Q11111",
                            }
                        ],
                    },
                    {
                        "accession": "P22222",
                        "screen_status": "preexisting_sequence_holdout_retained",
                    },
                ],
            },
            sequence_alignment_verification={
                "metadata": {
                    "method": "external_source_sequence_alignment_verification"
                },
                "rows": [
                    {
                        "accession": "P11111",
                        "verification_status": "alignment_no_near_duplicate_signal",
                    },
                    {
                        "accession": "P22222",
                        "verification_status": (
                            "alignment_near_duplicate_candidate_holdout"
                        ),
                    },
                ],
            },
        )
        audit = audit_external_source_sequence_search_export(
            sequence_search_export=export,
            sequence_neighborhood_plan={
                "metadata": {"candidate_count": 2},
                "rows": [{"accession": "P11111"}, {"accession": "P22222"}],
            },
        )

        self.assertFalse(export["metadata"]["ready_for_label_import"])
        self.assertTrue(export["metadata"]["complete_near_duplicate_search_required"])
        self.assertEqual(export["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(export["metadata"]["candidate_count"], 2)
        self.assertEqual(export["metadata"]["decision_status_counts"], {"no_decision": 2})
        self.assertEqual(
            export["metadata"]["search_task_counts"],
            {
                "keep_sequence_holdout_control": 1,
                "run_complete_uniref_or_all_vs_all_near_duplicate_search": 1,
            },
        )
        self.assertEqual(
            export["rows"][0]["search_task"],
            "run_complete_uniref_or_all_vs_all_near_duplicate_search",
        )
        self.assertEqual(
            export["rows"][0]["review_status"],
            "sequence_search_export_review_only",
        )
        self.assertFalse(export["rows"][0]["countable_label_candidate"])
        self.assertTrue(export["rows"][0]["source_targets"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["missing_review_only_status_row_count"], 0)

    def test_external_transfer_blocker_matrix_integrates_review_packets(self) -> None:
        matrix = build_external_source_transfer_blocker_matrix(
            candidate_manifest={
                "metadata": {
                    "candidate_count": 2,
                    "method": "external_source_candidate_manifest",
                },
                "rows": [
                    {
                        "accession": "P11111",
                        "lane_id": "external_source:transferase_phosphoryl",
                        "protein_name": "Example kinase",
                        "scope_signal": "transferase_phosphoryl",
                    },
                    {
                        "accession": "P22222",
                        "lane_id": "external_source:glycan_chemistry",
                        "protein_name": "Example glycosylase",
                        "scope_signal": "glycan_chemistry",
                    },
                ],
            },
            external_import_readiness_audit={
                "metadata": {"method": "external_source_import_readiness_audit"},
                "rows": [
                    {
                        "accession": "P11111",
                        "blockers": [
                            "external_active_site_feature_gap",
                            "complete_near_duplicate_search_required",
                        ],
                        "next_action": "source_explicit_active_site_residue_positions",
                        "readiness_status": "blocked_by_active_site_sourcing",
                    },
                    {
                        "accession": "P22222",
                        "blockers": [
                            "complete_near_duplicate_search_required",
                            "representation_control_not_compared",
                        ],
                        "next_action": "complete_near_duplicate_sequence_search",
                        "readiness_status": "blocked_by_sequence_search",
                    },
                ],
            },
            active_site_sourcing_export={
                "metadata": {"method": "external_source_active_site_sourcing_export"},
                "rows": [
                    {
                        "accession": "P11111",
                        "blockers": [
                            "explicit_active_site_residue_sources_not_collected"
                        ],
                        "decision": {"decision_status": "no_decision"},
                        "queue_status": "ready_for_curated_active_site_sourcing",
                        "source_task": (
                            "curate_active_site_positions_from_mapped_binding_context"
                        ),
                        "source_targets": [{"source_type": "UniProtKB"}],
                    }
                ],
            },
            sequence_search_export={
                "metadata": {"method": "external_source_sequence_search_export"},
                "rows": [
                    {
                        "accession": "P11111",
                        "blockers": [
                            "complete_near_duplicate_reference_search_not_completed"
                        ],
                        "decision": {"decision_status": "no_decision"},
                        "search_task": (
                            "run_complete_uniref_or_all_vs_all_near_duplicate_search"
                        ),
                        "source_targets": [{"source_type": "UniRef"}],
                    },
                    {
                        "accession": "P22222",
                        "blockers": ["sequence_holdout_control_not_resolved"],
                        "decision": {"decision_status": "no_decision"},
                        "search_task": "keep_sequence_holdout_control",
                        "source_targets": [{"source_type": "UniProtKB"}],
                    },
                ],
            },
            representation_backend_plan={
                "metadata": {"method": "external_source_representation_backend_plan"},
                "rows": [
                    {
                        "accession": "P22222",
                        "backend_readiness_status": (
                            "ready_for_backend_selection_not_embedding"
                        ),
                        "blockers": ["representation_backend_not_selected"],
                        "embedding_status": "backend_plan_only_not_computed",
                        "recommended_backends": ["sequence_language_model_embedding"],
                        "required_inputs": [{"input_type": "candidate_sequence"}],
                        "sequence_search_task": "keep_sequence_holdout_control",
                    }
                ],
            },
            active_site_sourcing_resolution={
                "metadata": {
                    "method": "external_source_active_site_sourcing_resolution"
                },
                "rows": [
                    {
                        "accession": "P11111",
                        "active_site_source_status": (
                            "binding_and_reaction_context_only_no_active_site_positions"
                        ),
                        "blockers": [
                            "explicit_active_site_residue_sources_absent"
                        ],
                        "review_status": (
                            "active_site_sourcing_resolution_review_only"
                        ),
                        "sourced_active_site_positions": [],
                    }
                ],
            },
            representation_backend_sample={
                "metadata": {
                    "method": "external_source_representation_backend_sample"
                },
                "rows": [
                    {
                        "accession": "P22222",
                        "backend_status": "representation_near_duplicate_holdout",
                        "blockers": [
                            "representation_near_duplicate_control_holdout"
                        ],
                        "embedding_status": "computed_review_only",
                        "nearest_reference": {"reference_accession": "P99999"},
                        "top_embedding_cosine": 0.98,
                    }
                ],
            },
        )
        audit = audit_external_source_transfer_blocker_matrix(
            transfer_blocker_matrix=matrix,
            candidate_manifest={
                "metadata": {
                    "candidate_count": 2,
                    "method": "external_source_candidate_manifest",
                },
                "rows": [{"accession": "P11111"}, {"accession": "P22222"}],
            },
        )

        self.assertFalse(matrix["metadata"]["ready_for_label_import"])
        self.assertEqual(matrix["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(matrix["metadata"]["candidate_count"], 2)
        self.assertEqual(
            matrix["metadata"]["active_site_sourcing_export_candidate_count"], 1
        )
        self.assertEqual(matrix["metadata"]["sequence_search_export_candidate_count"], 2)
        self.assertEqual(
            matrix["metadata"]["representation_backend_plan_candidate_count"], 1
        )
        self.assertEqual(
            matrix["metadata"][
                "active_site_sourcing_resolution_candidate_count"
            ],
            1,
        )
        self.assertEqual(
            matrix["metadata"]["representation_backend_sample_candidate_count"], 1
        )
        self.assertEqual(
            matrix["metadata"]["dominant_prioritized_action_fraction"], 0.5
        )
        self.assertEqual(matrix["metadata"]["dominant_lane_fraction"], 0.5)
        self.assertEqual(
            matrix["rows"][0]["prioritized_action"],
            "curate_primary_literature_or_pdb_active_site_sources",
        )
        self.assertEqual(
            matrix["rows"][1]["prioritized_action"],
            "keep_sequence_holdout_out_of_import_batch",
        )
        self.assertFalse(matrix["rows"][0]["countable_label_candidate"])
        self.assertEqual(
            matrix["rows"][0]["sequence_search"]["decision_status"], "no_decision"
        )
        self.assertEqual(
            matrix["rows"][0]["active_site_sourcing"]["resolution_status"],
            "binding_and_reaction_context_only_no_active_site_positions",
        )
        self.assertIn(
            "explicit_active_site_residue_sources_absent",
            matrix["rows"][0]["blockers"],
        )
        self.assertTrue(
            matrix["rows"][1]["representation_backend"][
                "sample_near_duplicate_alert"
            ]
        )
        self.assertIn(
            "representation_near_duplicate_control_holdout",
            matrix["rows"][1]["blockers"],
        )
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["manifest_accession_count"], 2)
        self.assertEqual(audit["metadata"]["completed_sequence_decision_count"], 0)
        self.assertEqual(
            audit["metadata"]["dominant_prioritized_action_fraction"], 0.5
        )
        mismatch_audit = audit_external_source_transfer_blocker_matrix(
            transfer_blocker_matrix=matrix,
            candidate_manifest={
                "metadata": {
                    "candidate_count": 2,
                    "method": "external_source_candidate_manifest",
                },
                "rows": [{"accession": "P11111"}, {"accession": "P33333"}],
            },
        )
        self.assertIn(
            "external_transfer_blocker_matrix_candidate_lineage_mismatch",
            mismatch_audit["blockers"],
        )

    def test_external_review_packet_audits_reject_non_review_status(self) -> None:
        representation_audit = audit_external_source_representation_backend_plan(
            {
                "metadata": {"embedding_status": "backend_plan_only_not_computed"},
                "rows": [
                    {
                        "countable_label_candidate": False,
                        "ready_for_label_import": False,
                        "recommended_backends": ["active_site_contrastive_baseline"],
                        "required_inputs": [{"input_type": "candidate_sequence"}],
                        "review_status": "promote",
                    }
                ],
            }
        )
        sequence_audit = audit_external_source_sequence_search_export(
            sequence_search_export={
                "rows": [
                    {
                        "countable_label_candidate": False,
                        "decision": {"decision_status": "no_decision"},
                        "ready_for_label_import": False,
                        "review_status": "promote",
                        "search_task": (
                            "run_complete_uniref_or_all_vs_all_near_duplicate_search"
                        ),
                        "source_targets": [{"source_type": "UniRef"}],
                    }
                ]
            },
            sequence_neighborhood_plan={"metadata": {"candidate_count": 1}},
        )
        active_site_audit = audit_external_source_active_site_sourcing_export(
            active_site_sourcing_export={
                "rows": [
                    {
                        "countable_label_candidate": False,
                        "decision": {"decision_status": "no_decision"},
                        "ready_for_label_import": False,
                        "review_status": "promote",
                        "source_targets": [{"source_type": "UniProtKB"}],
                        "source_task": (
                            "curate_active_site_positions_from_mapped_binding_context"
                        ),
                    }
                ]
            },
            active_site_sourcing_queue={"metadata": {"candidate_count": 1}},
        )

        self.assertFalse(representation_audit["metadata"]["guardrail_clean"])
        self.assertIn(
            "representation_backend_plan_rows_not_review_only",
            representation_audit["blockers"],
        )
        self.assertFalse(sequence_audit["metadata"]["guardrail_clean"])
        self.assertIn(
            "sequence_search_export_rows_not_review_only",
            sequence_audit["blockers"],
        )
        self.assertFalse(active_site_audit["metadata"]["guardrail_clean"])
        self.assertIn(
            "active_site_sourcing_export_rows_not_review_only",
            active_site_audit["blockers"],
        )

    def test_external_transfer_blocker_matrix_flags_action_collapse(self) -> None:
        audit = audit_external_source_transfer_blocker_matrix(
            transfer_blocker_matrix={
                "metadata": {
                    "candidate_count": 5,
                    "dominant_lane_fraction": 0.9,
                    "dominant_prioritized_action_fraction": 0.9,
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                },
                "rows": [
                    {
                        "blockers": ["complete_near_duplicate_search_required"],
                        "countable_label_candidate": False,
                        "prioritized_action": "complete_near_duplicate_sequence_search",
                        "ready_for_label_import": False,
                        "review_status": (
                            "external_transfer_blocker_matrix_review_only"
                        ),
                        "sequence_search": {
                            "decision_status": "no_decision",
                            "search_task": (
                                "run_complete_uniref_or_all_vs_all_"
                                "near_duplicate_search"
                            ),
                        },
                    }
                    for _ in range(5)
                ],
            },
            candidate_manifest={"metadata": {"candidate_count": 5}},
        )

        self.assertFalse(audit["metadata"]["guardrail_clean"])
        self.assertIn(
            "external_transfer_blocker_matrix_action_queue_collapsed",
            audit["blockers"],
        )
        self.assertIn(
            "external_transfer_blocker_matrix_lane_queue_collapsed",
            audit["blockers"],
        )

    def test_external_source_pilot_candidate_priority_defers_holdouts(self) -> None:
        priority = build_external_source_pilot_candidate_priority(
            {
                "metadata": {"method": "external_source_transfer_blocker_matrix"},
                "rows": [
                    {
                        "accession": "PGOOD1",
                        "active_site_sourcing": {
                            "queue_status": "ready_for_curated_active_site_sourcing",
                            "source_task": (
                                "curate_active_site_positions_from_mapped_binding_context"
                            ),
                        },
                        "blockers": ["complete_near_duplicate_search_required"],
                        "lane_id": "external_source:lane_a",
                        "mechanism_text": "tempting text must stay review context",
                        "prioritized_action": "complete_near_duplicate_sequence_search",
                        "representation_backend": {
                            "sample_backend_status": (
                                "learned_representation_sample_complete"
                            ),
                            "sample_near_duplicate_alert": False,
                        },
                        "sequence_search": {
                            "alignment_status": "alignment_no_near_duplicate_signal"
                        },
                        "source_label": "do_not_use_label_as_evidence",
                    },
                    {
                        "accession": "PHOLD",
                        "blockers": [
                            "complete_near_duplicate_search_required",
                            "exact_sequence_holdout",
                        ],
                        "lane_id": "external_source:lane_b",
                        "representation_backend": {
                            "sample_backend_status": (
                                "learned_representation_sample_complete"
                            ),
                            "sample_near_duplicate_alert": False,
                        },
                        "sequence_search": {
                            "alignment_status": "alignment_no_near_duplicate_signal"
                        },
                    },
                    {
                        "accession": "PNEAR",
                        "blockers": [
                            "complete_near_duplicate_search_required",
                            "representation_near_duplicate_control_holdout",
                        ],
                        "lane_id": "external_source:lane_c",
                        "representation_backend": {
                            "sample_near_duplicate_alert": True
                        },
                    },
                    {
                        "accession": "PGOOD2",
                        "active_site_sourcing": {
                            "queue_status": "ready_for_curated_active_site_sourcing"
                        },
                        "blockers": ["complete_near_duplicate_search_required"],
                        "lane_id": "external_source:lane_b",
                        "prioritized_action": "complete_near_duplicate_sequence_search",
                        "representation_backend": {
                            "sample_backend_status": (
                                "learned_representation_sample_complete"
                            ),
                            "sample_near_duplicate_alert": False,
                        },
                        "sequence_search": {
                            "alignment_status": "alignment_no_near_duplicate_signal"
                        },
                    },
                ],
            },
            max_candidates=2,
            max_per_lane=1,
        )

        self.assertEqual(priority["metadata"]["candidate_count"], 4)
        self.assertEqual(priority["metadata"]["selected_candidate_count"], 2)
        self.assertEqual(priority["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(priority["metadata"]["ready_for_label_import"])
        self.assertEqual(
            priority["metadata"]["blocker_removed"],
            "external_pilot_candidate_ranking",
        )
        self.assertFalse(
            priority["metadata"]["leakage_policy"][
                "text_or_label_fields_used_for_priority"
            ]
        )
        self.assertEqual(priority["metadata"]["selected_accessions"], ["PGOOD1", "PGOOD2"])
        self.assertEqual(
            priority["rows"][0]["leakage_provenance"][
                "present_text_or_label_context_fields"
            ],
            ["mechanism_text", "source_label"],
        )
        self.assertFalse(
            priority["rows"][0]["leakage_provenance"][
                "text_or_label_fields_used_for_priority"
            ]
        )
        self.assertEqual(
            priority["metadata"]["holdout_or_near_duplicate_deferred_count"],
            2,
        )
        self.assertTrue(
            all(not row["countable_label_candidate"] for row in priority["rows"])
        )
        self.assertTrue(all(not row["ready_for_label_import"] for row in priority["rows"]))
        self.assertNotIn(
            "exact_sequence_holdout",
            {blocker for row in priority["rows"] for blocker in row["blockers"]},
        )
        self.assertEqual(
            {
                row["accession"]: row["pilot_selection_status"]
                for row in priority["deferred_rows"]
            },
            {
                "PHOLD": "deferred_by_holdout_or_near_duplicate",
                "PNEAR": "deferred_by_holdout_or_near_duplicate",
            },
        )

    def test_external_source_pilot_review_decision_export_is_no_decision(self) -> None:
        priority = {
            "metadata": {"method": "external_source_pilot_candidate_priority"},
            "rows": [
                {
                    "accession": "PGOOD1",
                    "active_site_sourcing": {"queue_status": "ready"},
                    "blockers": ["complete_near_duplicate_search_required"],
                    "countable_label_candidate": False,
                    "entry_id": "uniprot:PGOOD1",
                    "lane_id": "external_source:lane_a",
                    "pilot_priority_score": 92.0,
                    "pilot_selection_status": "selected_for_review_pilot",
                    "ready_for_label_import": False,
                    "representation_backend": {
                        "sample_backend_status": (
                            "learned_representation_sample_complete"
                        )
                    },
                    "sequence_search": {
                        "alignment_status": "alignment_no_near_duplicate_signal"
                    },
                },
                {
                    "accession": "PDEFER",
                    "blockers": ["exact_sequence_holdout"],
                    "pilot_selection_status": "deferred_by_holdout_or_near_duplicate",
                },
            ],
        }

        export = build_external_source_pilot_review_decision_export(
            pilot_candidate_priority=priority
        )

        self.assertEqual(
            export["metadata"]["method"],
            "external_source_pilot_review_decision_export",
        )
        self.assertEqual(
            export["metadata"]["blocker_removed"],
            "external_pilot_review_decision_export_scaffold",
        )
        self.assertEqual(export["metadata"]["candidate_count"], 1)
        self.assertEqual(export["metadata"]["completed_decision_count"], 0)
        self.assertFalse(export["metadata"]["ready_for_label_import"])
        self.assertEqual(export["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            export["metadata"]["decision_status_counts"], {"no_decision": 1}
        )
        item = export["review_items"][0]
        self.assertEqual(item["accession"], "PGOOD1")
        self.assertEqual(item["decision"]["decision_status"], "no_decision")
        self.assertFalse(item["decision"]["ready_for_label_import"])
        self.assertFalse(item["countable_label_candidate"])
        self.assertIn(
            "complete_near_duplicate_sequence_search",
            item["review_requirements"],
        )

    def test_external_source_pilot_evidence_packet_consolidates_source_targets(
        self,
    ) -> None:
        priority = {
            "metadata": {"method": "external_source_pilot_candidate_priority"},
            "rows": [
                {
                    "accession": "PGOOD1",
                    "active_site_sourcing": {
                        "source_task": (
                            "curate_active_site_positions_from_mapped_binding_context"
                        )
                    },
                    "blockers": ["complete_near_duplicate_search_required"],
                    "entry_id": "uniprot:PGOOD1",
                    "lane_id": "external_source:lane_a",
                    "pilot_priority_score": 92.0,
                    "pilot_selection_status": "selected_for_review_pilot",
                    "representation_backend": {
                        "sample_backend_status": (
                            "learned_representation_sample_complete"
                        )
                    },
                },
                {
                    "accession": "PDEFER",
                    "pilot_selection_status": "deferred_by_holdout_or_near_duplicate",
                },
            ],
        }
        active_site_export = {
            "metadata": {"method": "external_source_active_site_sourcing_export"},
            "rows": [
                {
                    "accession": "PGOOD1",
                    "review_status": "active_site_sourcing_export_review_only",
                    "source_task": "curate_active_site_positions_from_mapped_binding_context",
                    "source_targets": [
                        {
                            "source_type": "PDB",
                            "source_id": "1ABC",
                            "url": "https://www.rcsb.org/structure/1ABC",
                        }
                    ],
                }
            ],
        }
        sequence_export = {
            "metadata": {"method": "external_source_sequence_search_export"},
            "rows": [
                {
                    "accession": "PGOOD1",
                    "review_status": "sequence_search_export_review_only",
                    "source_targets": [
                        {
                            "source_type": "UniRef",
                            "source_id": "PGOOD1",
                            "url": "https://www.uniprot.org/uniref?query=PGOOD1",
                        }
                    ],
                }
            ],
        }

        packet = build_external_source_pilot_evidence_packet(
            pilot_candidate_priority=priority,
            active_site_sourcing_export=active_site_export,
            sequence_search_export=sequence_export,
        )

        self.assertEqual(
            packet["metadata"]["method"],
            "external_source_pilot_evidence_packet",
        )
        self.assertEqual(
            packet["metadata"]["blocker_removed"],
            "external_pilot_source_packet_consolidation",
        )
        self.assertTrue(packet["metadata"]["guardrail_clean"])
        self.assertEqual(packet["metadata"]["candidate_count"], 1)
        self.assertEqual(packet["metadata"]["source_target_count"], 2)
        self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(packet["metadata"]["ready_for_label_import"])
        row = packet["rows"][0]
        self.assertEqual(row["accession"], "PGOOD1")
        self.assertEqual(
            {target["evidence_track"] for target in row["source_targets"]},
            {"active_site", "sequence_search"},
        )
        self.assertFalse(row["countable_label_candidate"])
        self.assertFalse(row["ready_for_label_import"])

    def test_external_transfer_blocker_matrix_audit_rejects_missing_integrated_rows(
        self,
    ) -> None:
        audit = audit_external_source_transfer_blocker_matrix(
            transfer_blocker_matrix={
                "metadata": {
                    "active_site_sourcing_resolution_candidate_count": 1,
                    "candidate_count": 1,
                    "dominant_lane_fraction": 0.0,
                    "dominant_prioritized_action_fraction": 0.0,
                    "representation_backend_sample_candidate_count": 1,
                },
                "rows": [
                    {
                        "active_site_sourcing": {"decision_status": "no_decision"},
                        "blockers": ["external_review_decision_artifact_not_built"],
                        "countable_label_candidate": False,
                        "prioritized_action": "complete_external_review",
                        "ready_for_label_import": False,
                        "representation_backend": {},
                        "review_status": "external_transfer_blocker_matrix_review_only",
                        "sequence_search": {
                            "decision_status": "no_decision",
                            "search_task": "run_complete_uniref_or_all_vs_all_near_duplicate_search",
                        },
                    }
                ],
            },
            candidate_manifest={"metadata": {"candidate_count": 1}},
        )

        self.assertFalse(audit["metadata"]["guardrail_clean"])
        self.assertIn(
            "external_transfer_blocker_matrix_active_site_resolution_mismatch",
            audit["blockers"],
        )
        self.assertIn(
            "external_transfer_blocker_matrix_representation_sample_mismatch",
            audit["blockers"],
        )

    def test_external_sequence_neighborhood_sample_screens_reference_sequences(
        self,
    ) -> None:
        sample = build_external_source_sequence_neighborhood_sample(
            sequence_neighborhood_plan={
                "metadata": {"method": "external_source_sequence_neighborhood_plan"},
                "rows": [
                    {
                        "accession": "P22222",
                        "holdout_status": "requires_near_duplicate_search",
                        "lane_id": "external_source:isomerase",
                        "plan_status": (
                            "near_duplicate_search_required_before_import"
                        ),
                        "ready_for_label_import": False,
                    }
                ],
            },
            sequence_clusters={
                "metadata": {"method": "sequence_cluster_proxy_from_reference_uniprot"},
                "rows": [
                    {
                        "entry_id": "m_csa:1",
                        "reference_uniprot_ids": ["P11111"],
                    }
                ],
            },
            labels=[
                {
                    "entry_id": "m_csa:1",
                    "label_type": "seed_fingerprint",
                    "review_status": "automation_curated",
                }
            ],
            fetcher=lambda accessions: {
                "metadata": {"source": "unit_test_fetcher"},
                "records": [
                    {
                        "accession": "P11111",
                        "sequence": "M" + "A" * 80 + "GGGG",
                    },
                    {
                        "accession": "P22222",
                        "sequence": "M" + "A" * 80 + "GGGA",
                    },
                ],
            },
        )
        audit = audit_external_source_sequence_neighborhood_sample(sample)

        self.assertFalse(sample["metadata"]["ready_for_label_import"])
        self.assertTrue(sample["metadata"]["complete_near_duplicate_search_required"])
        self.assertEqual(sample["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(sample["metadata"]["candidate_count"], 1)
        self.assertEqual(sample["metadata"]["reference_sequence_count"], 1)
        self.assertEqual(sample["metadata"]["high_similarity_candidate_count"], 1)
        self.assertEqual(
            sample["rows"][0]["screen_status"], "near_duplicate_candidate_holdout"
        )
        self.assertTrue(sample["rows"][0]["top_matches"][0]["near_duplicate_alert"])
        self.assertFalse(sample["rows"][0]["countable_label_candidate"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_external_sequence_neighborhood_sample_resolves_inactive_references(
        self,
    ) -> None:
        sample = build_external_source_sequence_neighborhood_sample(
            sequence_neighborhood_plan={
                "rows": [
                    {
                        "accession": "P22222",
                        "plan_status": (
                            "near_duplicate_search_required_before_import"
                        ),
                    }
                ],
            },
            sequence_clusters={
                "rows": [
                    {
                        "entry_id": "m_csa:1",
                        "reference_uniprot_ids": ["P03176"],
                    }
                ],
            },
            labels=[
                {
                    "entry_id": "m_csa:1",
                    "label_type": "seed_fingerprint",
                    "review_status": "automation_curated",
                }
            ],
            fetcher=lambda accessions: {
                "metadata": {
                    "source": "unit_test_fetcher",
                    "inactive_accession_replacements": {
                        "P03176": ["P0DTH5", "Q9QNF7"],
                    },
                },
                "records": [
                    {"accession": "P22222", "sequence": "M" + "A" * 40},
                    {"accession": "P0DTH5", "sequence": "M" + "C" * 40},
                    {"accession": "Q9QNF7", "sequence": "M" + "D" * 40},
                ],
            },
        )

        self.assertEqual(sample["metadata"]["reference_sequence_count"], 1)
        self.assertEqual(sample["metadata"]["reference_sequence_record_count"], 2)
        self.assertEqual(sample["metadata"]["missing_reference_sequence_count"], 0)
        self.assertEqual(
            sample["metadata"]["inactive_reference_accession_resolutions"],
            {"P03176": ["P0DTH5", "Q9QNF7"]},
        )
        references = {
            match["reference_accession"]: match
            for match in sample["rows"][0]["top_matches"]
        }
        self.assertEqual(set(references), {"P0DTH5", "Q9QNF7"})
        self.assertEqual(
            references["P0DTH5"]["requested_reference_accession"], "P03176"
        )
        self.assertEqual(
            references["P0DTH5"]["reference_accession_resolution"],
            "inactive_accession_replacement",
        )
        self.assertEqual(
            references["P0DTH5"]["matched_m_csa_entry_ids"], ["m_csa:1"]
        )

    def test_external_sequence_neighborhood_sample_audit_blocks_import_rows(
        self,
    ) -> None:
        audit = audit_external_source_sequence_neighborhood_sample(
            {
                "metadata": {
                    "candidate_count": 1,
                    "top_hit_row_count": 0,
                    "high_similarity_candidate_count": 0,
                },
                "rows": [
                    {
                        "accession": "P22222",
                        "countable_label_candidate": True,
                        "ready_for_label_import": True,
                        "screen_status": "near_duplicate_candidate_holdout",
                    }
                ],
            }
        )

        self.assertFalse(audit["metadata"]["guardrail_clean"])
        self.assertIn(
            "sequence_neighborhood_rows_marked_countable", audit["blockers"]
        )
        self.assertIn(
            "sequence_neighborhood_rows_marked_ready_for_import", audit["blockers"]
        )

    def test_external_sequence_alignment_verification_is_review_only(self) -> None:
        verification = build_external_source_sequence_alignment_verification(
            sequence_neighborhood_sample={
                "metadata": {
                    "method": "external_source_sequence_neighborhood_sample"
                },
                "top_hit_rows": [
                    {
                        "accession": "P22222",
                        "reference_accession": "P11111",
                        "matched_m_csa_entry_ids": ["m_csa:1"],
                        "near_duplicate_alert": False,
                        "near_duplicate_score": 0.72,
                    }
                ],
            },
            fetcher=lambda accessions: {
                "metadata": {"source": "unit_test_fetcher"},
                "records": [
                    {
                        "accession": "P11111",
                        "sequence": "M" + "A" * 40 + "GGGG",
                    },
                    {
                        "accession": "P22222",
                        "sequence": "M" + "A" * 40 + "GGGA",
                    },
                ],
            },
        )
        audit = audit_external_source_sequence_alignment_verification(verification)

        self.assertFalse(verification["metadata"]["ready_for_label_import"])
        self.assertTrue(
            verification["metadata"]["complete_near_duplicate_search_required"]
        )
        self.assertEqual(verification["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(verification["metadata"]["verified_pair_count"], 1)
        self.assertEqual(verification["metadata"]["alignment_alert_candidate_count"], 1)
        self.assertEqual(
            verification["rows"][0]["verification_status"],
            "alignment_near_duplicate_candidate_holdout",
        )
        self.assertFalse(verification["rows"][0]["countable_label_candidate"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

        deferred = build_external_source_sequence_alignment_verification(
            sequence_neighborhood_sample={
                "top_hit_rows": [
                    {
                        "accession": "P22222",
                        "reference_accession": "P11111",
                    }
                ],
            },
            max_alignment_cells=10,
            fetcher=lambda accessions: {
                "metadata": {"source": "unit_test_fetcher"},
                "records": [
                    {"accession": "P11111", "sequence": "M" + "A" * 40},
                    {"accession": "P22222", "sequence": "M" + "A" * 40},
                ],
            },
        )
        self.assertEqual(
            deferred["rows"][0]["verification_status"],
            "alignment_deferred_pair_too_large",
        )
        self.assertEqual(deferred["metadata"]["alignment_deferred_pair_count"], 1)

    def test_external_sequence_alignment_audit_blocks_import_rows(self) -> None:
        audit = audit_external_source_sequence_alignment_verification(
            {
                "metadata": {
                    "complete_near_duplicate_search_required": True,
                    "candidate_count": 1,
                    "verified_pair_count": 1,
                },
                "rows": [
                    {
                        "accession": "P22222",
                        "countable_label_candidate": True,
                        "ready_for_label_import": True,
                        "verification_status": (
                            "alignment_near_duplicate_candidate_holdout"
                        ),
                    }
                ],
            }
        )

        self.assertFalse(audit["metadata"]["guardrail_clean"])
        self.assertIn("sequence_alignment_rows_marked_countable", audit["blockers"])
        self.assertIn(
            "sequence_alignment_rows_marked_ready_for_import", audit["blockers"]
        )

    def test_external_sequence_reference_screen_audit_clears_current_reference_blocker(
        self,
    ) -> None:
        sequence_neighborhood_sample = {
            "metadata": {
                "candidate_count": 1,
                "fetch_failure_count": 0,
                "missing_external_sequence_count": 0,
                "reference_sequence_count": 2,
            },
            "rows": [
                {
                    "accession": "P22222",
                    "entry_id": "uniprot:P22222",
                    "screen_status": "no_high_similarity_hit_in_bounded_screen",
                    "top_matches": [
                        {
                            "reference_accession": "P11111",
                            "matched_m_csa_entry_ids": ["m_csa:1"],
                        },
                        {
                            "reference_accession": "Q11111",
                            "matched_m_csa_entry_ids": ["m_csa:2"],
                        },
                    ],
                }
            ],
        }
        sequence_alignment_verification = {
            "metadata": {"method": "external_source_sequence_alignment_verification"},
            "rows": [
                {
                    "accession": "P22222",
                    "reference_accession": "P11111",
                    "alignment_identity": 0.2,
                    "verification_status": "alignment_no_near_duplicate_signal",
                },
                {
                    "accession": "P22222",
                    "reference_accession": "Q11111",
                    "alignment_identity": 0.18,
                    "verification_status": "alignment_no_near_duplicate_signal",
                },
            ],
        }
        sequence_clusters = {
            "rows": [
                {
                    "entry_id": "m_csa:1",
                    "reference_uniprot_ids": ["P11111"],
                },
                {
                    "entry_id": "m_csa:2",
                    "reference_uniprot_ids": ["Q11111"],
                },
            ]
        }
        labels = [
            {
                "entry_id": "m_csa:1",
                "label_type": "seed_fingerprint",
                "review_status": "automation_curated",
            },
            {
                "entry_id": "m_csa:2",
                "label_type": "out_of_scope",
                "review_status": "automation_curated",
            },
        ]

        audit = audit_external_source_sequence_reference_screen(
            sequence_neighborhood_sample=sequence_neighborhood_sample,
            sequence_alignment_verification=sequence_alignment_verification,
            sequence_clusters=sequence_clusters,
            labels=labels,
        )
        export = build_external_source_sequence_search_export(
            sequence_neighborhood_plan={
                "metadata": {"candidate_count": 1},
                "rows": [
                    {
                        "accession": "P22222",
                        "entry_id": "uniprot:P22222",
                        "plan_status": "near_duplicate_search_required_before_import",
                    }
                ],
            },
            sequence_neighborhood_sample=sequence_neighborhood_sample,
            sequence_alignment_verification=sequence_alignment_verification,
            sequence_reference_screen_audit=audit,
        )

        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertTrue(audit["metadata"]["current_reference_screen_complete"])
        self.assertEqual(
            audit["metadata"]["blocker_removed"],
            "external_pilot_current_reference_near_duplicate_screen",
        )
        self.assertEqual(
            audit["rows"][0]["current_reference_screen_status"],
            "current_reference_top_hits_aligned_no_alert",
        )
        self.assertEqual(
            export["metadata"]["blocker_removed"],
            "external_pilot_current_reference_near_duplicate_screen",
        )
        self.assertNotIn(
            "complete_near_duplicate_reference_search_not_completed",
            export["rows"][0]["blockers"],
        )
        self.assertIn(
            "complete_uniref_or_all_vs_all_near_duplicate_search_required",
            export["rows"][0]["blockers"],
        )

        incomplete = audit_external_source_sequence_reference_screen(
            sequence_neighborhood_sample={
                **sequence_neighborhood_sample,
                "metadata": {
                    **sequence_neighborhood_sample["metadata"],
                    "reference_sequence_count": 1,
                },
            },
            sequence_alignment_verification=sequence_alignment_verification,
            sequence_clusters=sequence_clusters,
            labels=labels,
        )
        self.assertFalse(incomplete["metadata"]["guardrail_clean"])
        self.assertIn(
            "current_reference_sequence_screen_incomplete",
            incomplete["blockers"],
        )

    def test_external_import_readiness_audit_prioritizes_remaining_blockers(
        self,
    ) -> None:
        audit = audit_external_source_import_readiness(
            candidate_manifest={
                "metadata": {"method": "external_source_candidate_manifest"},
                "rows": [
                    {
                        "accession": "P11111",
                        "lane_id": "external_source:isomerase",
                        "protein_name": "Example isomerase",
                        "scope_signal": "isomerase",
                    },
                    {
                        "accession": "P22222",
                        "lane_id": "external_source:glycan_chemistry",
                        "protein_name": "Example glycan enzyme",
                        "scope_signal": "glycan_chemistry",
                    },
                ],
            },
            active_site_evidence_sample={
                "candidate_summaries": [
                    {
                        "accession": "P11111",
                        "active_site_feature_count": 2,
                    },
                    {
                        "accession": "P22222",
                        "active_site_feature_count": 0,
                    },
                ]
            },
            heuristic_control_scores={
                "results": [
                    {
                        "entry_id": "uniprot:P11111",
                        "scope_top1_mismatch": True,
                        "top_fingerprints": [
                            {"fingerprint_id": "metal_dependent_hydrolase"}
                        ],
                    }
                ]
            },
            representation_control_comparison={
                "rows": [
                    {
                        "entry_id": "uniprot:P11111",
                        "comparison_status": (
                            "proxy_flags_metal_hydrolase_collapse"
                        ),
                    }
                ]
            },
            active_site_gap_source_requests={
                "rows": [
                    {
                        "accession": "P22222",
                        "request_status": (
                            "binding_context_mapped_ready_for_active_site_sourcing"
                        ),
                    }
                ]
            },
            sequence_neighborhood_sample={
                "rows": [
                    {
                        "accession": "P11111",
                        "screen_status": "no_high_similarity_hit_in_bounded_screen",
                    },
                    {
                        "accession": "P22222",
                        "screen_status": "preexisting_sequence_holdout_retained",
                    },
                ]
            },
            sequence_alignment_verification={
                "rows": [
                    {
                        "accession": "P22222",
                        "verification_status": (
                            "alignment_near_duplicate_candidate_holdout"
                        ),
                    }
                ]
            },
        )

        self.assertFalse(audit["metadata"]["ready_for_label_import"])
        self.assertTrue(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(audit["metadata"]["candidate_count"], 2)
        self.assertEqual(audit["metadata"]["active_site_gap_count"], 1)
        self.assertEqual(audit["metadata"]["heuristic_scope_mismatch_count"], 1)
        self.assertEqual(audit["metadata"]["representation_control_issue_count"], 2)
        self.assertEqual(audit["metadata"]["sequence_alignment_alert_count"], 1)
        self.assertEqual(
            audit["rows"][0]["readiness_status"], "blocked_by_heuristic_control"
        )
        self.assertEqual(
            audit["rows"][1]["readiness_status"], "blocked_by_sequence_holdout"
        )
        self.assertEqual(
            audit["rows"][1]["sequence_alignment_status"],
            "alignment_near_duplicate_candidate_holdout",
        )
        self.assertFalse(audit["rows"][0]["countable_label_candidate"])

    def test_external_import_readiness_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            candidate_manifest = root / "candidate_manifest.json"
            active_site_sample = root / "active_site_sample.json"
            heuristic_scores = root / "heuristic_scores.json"
            representation = root / "representation.json"
            active_site_gap_sources = root / "active_site_gap_sources.json"
            sequence_sample = root / "sequence_sample.json"
            out = root / "import_readiness.json"
            candidate_manifest.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "external_source_candidate_manifest"},
                        "rows": [
                            {
                                "accession": "P11111",
                                "lane_id": "external_source:lyase",
                                "scope_signal": "lyase",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            active_site_sample.write_text(
                json.dumps(
                    {
                        "candidate_summaries": [
                            {"accession": "P11111", "active_site_feature_count": 1}
                        ]
                    }
                ),
                encoding="utf-8",
            )
            heuristic_scores.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "entry_id": "uniprot:P11111",
                                "scope_top1_mismatch": False,
                                "top_fingerprints": [
                                    {"fingerprint_id": "flavin_dehydrogenase_reductase"}
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            representation.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "uniprot:P11111",
                                "comparison_status": (
                                    "proxy_consistent_with_heuristic_scope"
                                ),
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            active_site_gap_sources.write_text(json.dumps({"rows": []}), encoding="utf-8")
            sequence_sample.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "accession": "P11111",
                                "screen_status": (
                                    "no_high_similarity_hit_in_bounded_screen"
                                ),
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-external-source-import-readiness",
                    "--candidate-manifest",
                    str(candidate_manifest),
                    "--active-site-evidence-sample",
                    str(active_site_sample),
                    "--heuristic-control-scores",
                    str(heuristic_scores),
                    "--representation-control-comparison",
                    str(representation),
                    "--active-site-gap-source-requests",
                    str(active_site_gap_sources),
                    "--sequence-neighborhood-sample",
                    str(sequence_sample),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(payload["metadata"]["guardrail_clean"])
            self.assertFalse(payload["metadata"]["ready_for_label_import"])
            self.assertEqual(payload["metadata"]["candidate_count"], 1)
            self.assertEqual(
                payload["rows"][0]["next_action"],
                "complete_near_duplicate_sequence_search",
            )

    def test_external_source_evidence_request_export_is_no_decision(self) -> None:
        export = build_external_source_evidence_request_export(
            evidence_plan={
                "metadata": {
                    "method": "external_source_evidence_plan",
                    "exact_reference_overlap_holdout_count": 1,
                },
                "rows": [
                    {
                        "accession": "P12345",
                        "countable_label_candidate": False,
                        "lane_id": "external_source:lyase",
                        "next_action": "collect_active_site_and_mechanism_evidence",
                        "required_evidence": ["active_site_residue_positions"],
                    }
                ],
            },
            max_rows=10,
        )

        self.assertTrue(export["metadata"]["external_source_review_only"])
        self.assertFalse(export["metadata"]["ready_for_label_import"])
        self.assertEqual(export["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(export["metadata"]["decision_counts"], {"no_decision": 1})
        self.assertEqual(export["review_items"][0]["entry_id"], "uniprot:P12345")
        self.assertEqual(
            export["review_items"][0]["decision"]["external_source_resolution"],
            "needs_more_evidence",
        )

    def test_external_transfer_artifact_lineage_rejects_mismatched_slices(
        self,
    ) -> None:
        lineage = validate_external_transfer_artifact_path_lineage(
            {
                "candidate_manifest": (
                    "artifacts/v3_external_source_candidate_manifest_1025.json"
                ),
                "evidence_plan": (
                    "artifacts/v3_external_source_evidence_plan_1000.json"
                ),
                "pilot_evidence_packet": (
                    "artifacts/v3_external_source_pilot_evidence_packet_1025.json"
                ),
            },
            {
                "candidate_manifest": {
                    "metadata": {
                        "method": "external_source_candidate_manifest",
                        "source_slice_id": 1025,
                    }
                },
                "evidence_plan": {
                    "metadata": {
                        "method": "external_source_evidence_plan",
                        "source_slice_id": 1000,
                    }
                },
                "pilot_evidence_packet": {
                    "metadata": {
                        "method": "external_source_pilot_evidence_packet",
                        "source_slice_id": 1025,
                    }
                },
            },
        )

        self.assertFalse(lineage["guardrail_clean"])
        self.assertIn(
            "external_transfer_artifact_path_slice_mismatch",
            lineage["blockers"],
        )
        self.assertEqual(lineage["path_slice_ids"]["evidence_plan"], 1000)
        with self.assertRaisesRegex(
            ValueError,
            "mismatched external transfer artifact lineage",
        ):
            validate_external_transfer_artifact_path_lineage(
                {
                    "candidate_manifest": (
                        "artifacts/v3_external_source_candidate_manifest_1025.json"
                    ),
                    "evidence_plan": (
                        "artifacts/v3_external_source_evidence_plan_1000.json"
                    ),
                },
                fail_fast=True,
            )

    def test_external_transfer_gate_accepts_typed_input_contract(self) -> None:
        gate_inputs = ExternalSourceTransferGateInputs(
            **_base_external_transfer_gate_inputs()
        )

        gates = check_external_source_transfer_gates(gate_inputs)

        self.assertEqual(
            gates["metadata"]["gate_input_contract"],
            "ExternalSourceTransferGateInputs.v1",
        )
        self.assertTrue(
            gates["metadata"]["artifact_lineage"]["guardrail_clean"]
        )
        self.assertIn(
            "evidence_plan",
            gates["metadata"]["artifact_lineage"]["checked_artifacts"],
        )
        with self.assertRaisesRegex(
            ValueError,
            "ExternalSourceTransferGateInputs.v1 or keyword artifacts",
        ):
            check_external_source_transfer_gates(
                gate_inputs,
                **_base_external_transfer_gate_inputs(),
            )
        missing_required = _base_external_transfer_gate_inputs()
        del missing_required["evidence_plan"]
        with self.assertRaisesRegex(
            ValueError,
            "missing external transfer gate inputs: evidence_plan",
        ):
            check_external_source_transfer_gates(**missing_required)
        wrong_required_type = _base_external_transfer_gate_inputs()
        wrong_required_type["candidate_manifest"] = []
        with self.assertRaisesRegex(
            ValueError,
            "required inputs must be JSON objects: candidate_manifest",
        ):
            check_external_source_transfer_gates(**wrong_required_type)
        with self.assertRaisesRegex(
            ValueError,
            "optional inputs must be JSON objects when present: pilot_evidence_packet",
        ):
            check_external_source_transfer_gates(
                **_base_external_transfer_gate_inputs(),
                pilot_evidence_packet=[],
            )

    def test_external_transfer_gate_rejects_incomplete_reference_screen(
        self,
    ) -> None:
        gates = check_external_source_transfer_gates(
            **_base_external_transfer_gate_inputs(),
            sequence_neighborhood_sample={
                "metadata": {
                    "ready_for_label_import": False,
                    "complete_near_duplicate_search_required": True,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "reference_sequence_count": 2,
                },
                "rows": [
                    {
                        "accession": "P12345",
                        "countable_label_candidate": False,
                        "ready_for_label_import": False,
                        "screen_status": "current_reference_top_hits_available",
                    }
                ],
            },
            sequence_reference_screen_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "ready_for_label_import": False,
                    "complete_near_duplicate_search_required": True,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "screened_reference_sequence_count": 1,
                    "current_reference_screen_complete": False,
                    "missing_reference_sequence_count": 1,
                    "incomplete_candidate_count": 1,
                    "blocker_removed": (
                        "external_pilot_current_reference_near_duplicate_screen"
                    ),
                },
                "rows": [
                    {
                        "accession": "P12345",
                        "countable_label_candidate": False,
                        "current_reference_screen_status": (
                            "current_reference_screen_incomplete"
                        ),
                        "ready_for_label_import": False,
                        "review_status": "sequence_reference_screen_audit_review_only",
                    }
                ],
            },
        )

        self.assertFalse(
            gates["gates"]["sequence_reference_screen_audit_guardrail_clean"]
        )
        self.assertEqual(
            gates["blockers"],
            ["sequence_reference_screen_audit_guardrail_clean"],
        )
        self.assertEqual(
            gates["metadata"]["sequence_reference_screen_incomplete_candidate_count"],
            1,
        )

    def test_external_transfer_gate_rejects_stale_reference_screen_export(
        self,
    ) -> None:
        gates = check_external_source_transfer_gates(
            **_base_external_transfer_gate_inputs(),
            sequence_neighborhood_sample={
                "metadata": {
                    "ready_for_label_import": False,
                    "complete_near_duplicate_search_required": True,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "reference_sequence_count": 1,
                },
                "rows": [
                    {
                        "accession": "P12345",
                        "countable_label_candidate": False,
                        "ready_for_label_import": False,
                        "screen_status": "current_reference_top_hits_available",
                    }
                ],
            },
            sequence_reference_screen_audit={
                "metadata": {
                    "method": "external_source_sequence_reference_screen_audit",
                    "guardrail_clean": True,
                    "ready_for_label_import": False,
                    "complete_near_duplicate_search_required": True,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "screened_reference_sequence_count": 1,
                    "current_reference_screen_complete": True,
                    "missing_reference_sequence_count": 0,
                    "incomplete_candidate_count": 0,
                    "blocker_removed": (
                        "external_pilot_current_reference_near_duplicate_screen"
                    ),
                },
                "rows": [
                    {
                        "accession": "P12345",
                        "countable_label_candidate": False,
                        "current_reference_screen_status": (
                            "current_reference_top_hits_aligned_no_alert"
                        ),
                        "ready_for_label_import": False,
                        "review_status": "sequence_reference_screen_audit_review_only",
                    }
                ],
            },
            sequence_search_export={
                "metadata": {
                    "ready_for_label_import": False,
                    "complete_near_duplicate_search_required": True,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "current_reference_screen_complete_candidate_count": 0,
                    "source_sequence_reference_screen_audit_method": (
                        "external_source_sequence_reference_screen_audit"
                    ),
                    "blocker_removed": (
                        "external_pilot_current_reference_near_duplicate_screen"
                    ),
                },
                "rows": [
                    {
                        "accession": "P12345",
                        "countable_label_candidate": False,
                        "current_reference_screen": {
                            "status": "current_reference_top_hits_aligned_no_alert"
                        },
                        "decision": {"decision_status": "no_decision"},
                        "ready_for_label_import": False,
                        "review_status": "sequence_search_export_review_only",
                        "search_task": (
                            "run_complete_uniref_or_all_vs_all_near_duplicate_search"
                        ),
                        "source_targets": [
                            {"source_id": "P11111", "source_type": "UniRef"}
                        ],
                    }
                ],
            },
        )

        self.assertTrue(
            gates["gates"]["sequence_reference_screen_audit_guardrail_clean"]
        )
        self.assertFalse(gates["gates"]["sequence_search_export_review_only"])
        self.assertEqual(gates["blockers"], ["sequence_search_export_review_only"])

    def test_external_pilot_evidence_dossiers_are_review_only(self) -> None:
        dossiers = build_external_source_pilot_evidence_dossiers(
            pilot_evidence_packet={
                "metadata": {"method": "external_source_pilot_evidence_packet"},
                "rows": [
                    {
                        "rank": 1,
                        "accession": "P12345",
                        "entry_id": "uniprot:P12345",
                        "protein_name": "Pilot enzyme",
                        "lane_id": "external_source:lyase",
                        "pilot_priority_score": 88.0,
                        "blockers": ["complete_near_duplicate_search_required"],
                        "sequence_search": {
                            "search_task": "run_complete_uniref_search",
                            "decision_status": "no_decision",
                        },
                    }
                ],
            },
            active_site_evidence_sample={
                "rows": [
                    {
                        "accession": "P12345",
                        "feature_type": "Active site",
                        "begin": 42,
                        "end": 42,
                        "description": "Nucleophile",
                        "evidence": [{"source": "PubMed", "id": "1"}],
                    }
                ]
            },
            active_site_sourcing_resolution={
                "rows": [
                    {
                        "accession": "P12345",
                        "active_site_source_status": (
                            "explicit_uniprot_active_site_positions_found"
                        ),
                        "sourced_active_site_positions": [42],
                        "source_task": "curate_active_site_positions",
                        "blockers": ["external_review_decision_artifact_not_built"],
                    }
                ]
            },
            reaction_evidence_sample={
                "rows": [
                    {
                        "accession": "P12345",
                        "ec_number": "4.2.1.1",
                        "ec_specificity": "specific",
                        "rhea_id": "RHEA:1",
                        "equation": "A = B",
                    }
                ]
            },
            sequence_alignment_verification={
                "rows": [
                    {
                        "accession": "P12345",
                        "reference_accession": "Q99999",
                        "alignment_identity": 0.2,
                        "length_coverage": 0.9,
                        "verification_status": "alignment_no_near_duplicate_signal",
                    }
                ]
            },
            representation_backend_sample={
                "rows": [
                    {
                        "accession": "P12345",
                        "backend_status": "learned_representation_sample_complete",
                        "embedding_status": "computed_review_only",
                        "top_embedding_cosine": 0.7,
                        "nearest_reference": {"entry_id": "m_csa:1"},
                    }
                ]
            },
            heuristic_control_scores={
                "results": [
                    {
                        "entry_id": "uniprot:P12345",
                        "scope_top1_mismatch": False,
                        "top_fingerprints": [
                            {"fingerprint_id": "flavin_dehydrogenase_reductase", "score": 0.5}
                        ],
                    }
                ]
            },
            structure_mapping_sample={
                "entries": [
                    {
                        "accession": "P12345",
                        "status": "mapped",
                        "structure_id": "AF-P12345-F1",
                        "resolved_residue_count": 2,
                    }
                ]
            },
            transfer_blocker_matrix={
                "metadata": {"method": "external_source_transfer_blocker_matrix"},
                "rows": [
                    {
                        "accession": "P12345",
                        "prioritized_action": "complete_near_duplicate_sequence_search",
                        "readiness_status": "blocked_by_sequence_search",
                        "blockers": ["full_label_factory_gate_not_run"],
                    }
                ],
            },
            external_import_readiness_audit={
                "rows": [
                    {
                        "accession": "P12345",
                        "readiness_status": "blocked_by_sequence_search",
                        "blockers": ["external_review_decision_artifact_not_built"],
                    }
                ]
            },
        )

        self.assertFalse(dossiers["metadata"]["ready_for_label_import"])
        self.assertEqual(dossiers["metadata"]["candidate_count"], 1)
        self.assertEqual(
            dossiers["metadata"]["blocker_removed"],
            "external_pilot_per_candidate_evidence_dossier_assembly",
        )
        self.assertEqual(
            dossiers["metadata"]["review_policy"]["semantics"],
            "review_only_non_countable",
        )
        row = dossiers["rows"][0]
        self.assertFalse(row["countable_label_candidate"])
        self.assertEqual(
            row["review_status"], "external_pilot_evidence_dossier_review_only"
        )
        self.assertEqual(
            row["active_site_evidence"]["explicit_active_site_feature_count"], 1
        )
        self.assertEqual(row["reaction_evidence"]["reaction_record_count"], 1)
        self.assertEqual(row["sequence_evidence"]["alignment_checked_pair_count"], 1)
        self.assertIn("full_label_factory_gate_not_run", row["remaining_blockers"])

    def test_external_pilot_evidence_dossiers_add_local_evidence_blockers(
        self,
    ) -> None:
        dossiers = build_external_source_pilot_evidence_dossiers(
            pilot_evidence_packet={
                "metadata": {"method": "external_source_pilot_evidence_packet"},
                "rows": [
                    {
                        "rank": 1,
                        "accession": "P12345",
                        "entry_id": "uniprot:P12345",
                        "lane_id": "external_source:lyase",
                        "sequence_search": {"decision_status": "no_decision"},
                    }
                ],
            },
            active_site_evidence_sample={"rows": []},
            active_site_sourcing_resolution={"rows": [{"accession": "P12345"}]},
            reaction_evidence_sample={
                "rows": [
                    {
                        "accession": "P12345",
                        "ec_number": "4.2.-.-",
                        "ec_specificity": "broad_or_incomplete",
                    }
                ]
            },
            sequence_alignment_verification={
                "rows": [
                    {
                        "accession": "P12345",
                        "verification_status": "alignment_near_duplicate_candidate_holdout",
                    }
                ]
            },
            representation_backend_sample={
                "rows": [
                    {
                        "accession": "P12345",
                        "backend_status": "learned_representation_sample_complete",
                    }
                ]
            },
            heuristic_control_scores={"results": []},
            structure_mapping_sample={"entries": []},
            transfer_blocker_matrix={"rows": [{"accession": "P12345"}]},
            external_import_readiness_audit={"rows": [{"accession": "P12345"}]},
        )

        blockers = dossiers["rows"][0]["remaining_blockers"]
        self.assertIn("pilot_explicit_active_site_evidence_missing", blockers)
        self.assertIn("pilot_specific_reaction_context_missing", blockers)
        self.assertIn("pilot_sequence_near_duplicate_alert_present", blockers)
        self.assertEqual(
            dossiers["metadata"]["local_evidence_blocker_counts"],
            {
                "pilot_explicit_active_site_evidence_missing": 1,
                "pilot_sequence_near_duplicate_alert_present": 1,
                "pilot_specific_reaction_context_missing": 1,
            },
        )

    def test_external_transfer_gate_requires_pilot_packets_to_stay_review_only(
        self,
    ) -> None:
        pilot_candidate_priority = {
            "metadata": {
                "method": "external_source_pilot_candidate_priority",
                "ready_for_label_import": False,
                "countable_label_candidate_count": 0,
                "candidate_count": 1,
                "selected_candidate_count": 1,
                "max_candidates": 10,
                "max_per_lane": 1,
                "leakage_policy": {
                    "text_or_label_fields_used_for_priority": False,
                },
            },
            "rows": [
                {
                    "accession": "P12345",
                    "entry_id": "uniprot:P12345",
                    "lane_id": "external_source:lyase",
                    "pilot_selection_status": "selected_for_review_pilot",
                    "eligible_for_review_pilot": True,
                    "pilot_priority_blockers": [],
                    "countable_label_candidate": False,
                    "ready_for_label_import": False,
                    "review_status": "external_pilot_candidate_priority_review_only",
                    "leakage_provenance": {
                        "text_or_label_fields_used_for_priority": False,
                    },
                }
            ],
        }
        pilot_review_decision_export = {
            "metadata": {
                "method": "external_source_pilot_review_decision_export",
                "ready_for_label_import": False,
                "review_only": True,
                "countable_label_candidate_count": 0,
                "candidate_count": 1,
                "completed_decision_count": 0,
                "decision_status_counts": {"no_decision": 1},
            },
            "review_items": [
                {
                    "accession": "P12345",
                    "entry_id": "uniprot:P12345",
                    "countable_label_candidate": False,
                    "ready_for_label_import": False,
                    "review_requirements": [
                        "curated_active_site_residue_evidence",
                        "specific_reaction_or_mechanism_evidence",
                        "complete_near_duplicate_sequence_search",
                        "leakage_safe_representation_control",
                        "review_decision",
                        "full_label_factory_gate",
                    ],
                    "decision": {
                        "decision_status": "no_decision",
                        "ready_for_label_import": False,
                    },
                }
            ],
        }
        pilot_evidence_packet = {
            "metadata": {
                "method": "external_source_pilot_evidence_packet",
                "ready_for_label_import": False,
                "review_only": True,
                "guardrail_clean": True,
                "countable_label_candidate_count": 0,
                "candidate_count": 1,
                "sequence_search_packet_count": 1,
                "source_target_count": 1,
                "missing_sequence_export_accessions": [],
                "missing_required_active_site_export_accessions": [],
            },
            "rows": [
                {
                    "accession": "P12345",
                    "entry_id": "uniprot:P12345",
                    "countable_label_candidate": False,
                    "ready_for_label_import": False,
                    "review_status": "external_pilot_evidence_packet_review_only",
                    "review_requirements": [
                        "curated_active_site_residue_evidence",
                        "specific_reaction_or_mechanism_evidence",
                        "complete_near_duplicate_sequence_search",
                        "leakage_safe_representation_control",
                        "review_decision",
                        "full_label_factory_gate",
                    ],
                    "source_targets": [{"source": "UniProtKB", "id": "P12345"}],
                    "sequence_search": {
                        "decision": {"decision_status": "no_decision"},
                    },
                }
            ],
        }
        pilot_evidence_dossiers = {
            "metadata": {
                "method": "external_source_pilot_evidence_dossier",
                "ready_for_label_import": False,
                "review_only": True,
                "countable_label_candidate_count": 0,
                "candidate_count": 1,
                "candidate_with_remaining_blocker_count": 1,
            },
            "rows": [
                {
                    "accession": "P12345",
                    "entry_id": "uniprot:P12345",
                    "countable_label_candidate": False,
                    "ready_for_label_import": False,
                    "review_status": "external_pilot_evidence_dossier_review_only",
                    "evidence_dossier_status": "blocked_before_import",
                    "active_site_evidence": {"explicit_active_site_feature_count": 1},
                    "reaction_evidence": {"reaction_record_count": 1},
                    "sequence_evidence": {"alignment_checked_pair_count": 1},
                    "representation_control": {
                        "backend_status": "learned_representation_sample_complete",
                    },
                }
            ],
        }

        gates = check_external_source_transfer_gates(
            **_base_external_transfer_gate_inputs(),
            pilot_candidate_priority=pilot_candidate_priority,
            pilot_review_decision_export=pilot_review_decision_export,
            pilot_evidence_packet=pilot_evidence_packet,
            pilot_evidence_dossiers=pilot_evidence_dossiers,
        )

        self.assertEqual(gates["blockers"], [])
        self.assertTrue(
            gates["gates"]["external_pilot_candidate_priority_review_only"]
        )
        self.assertTrue(
            gates["gates"]["external_pilot_review_decision_export_no_decision"]
        )
        self.assertTrue(gates["gates"]["external_pilot_evidence_packet_review_only"])
        self.assertTrue(
            gates["gates"]["external_pilot_evidence_dossiers_review_only"]
        )
        self.assertEqual(gates["metadata"]["external_pilot_selected_candidate_count"], 1)
        self.assertEqual(
            gates["metadata"]["external_pilot_review_completed_decision_count"],
            0,
        )

        blocked_gates = check_external_source_transfer_gates(
            **_base_external_transfer_gate_inputs(),
            pilot_candidate_priority=pilot_candidate_priority,
            pilot_review_decision_export={
                "metadata": {
                    **pilot_review_decision_export["metadata"],
                    "completed_decision_count": 1,
                    "decision_status_counts": {"accept": 1},
                },
                "review_items": [
                    {
                        "accession": "P12345",
                        "entry_id": "uniprot:P12345",
                        "countable_label_candidate": False,
                        "ready_for_label_import": True,
                        "decision": {
                            "decision_status": "accept",
                            "ready_for_label_import": True,
                        },
                    }
                ],
            },
            pilot_evidence_packet=pilot_evidence_packet,
            pilot_evidence_dossiers=pilot_evidence_dossiers,
        )

        self.assertFalse(
            blocked_gates["gates"][
                "external_pilot_review_decision_export_no_decision"
            ]
        )
        self.assertIn(
            "external_pilot_review_decision_export_no_decision",
            blocked_gates["blockers"],
        )

        missing_requirement_gates = check_external_source_transfer_gates(
            **_base_external_transfer_gate_inputs(),
            pilot_candidate_priority=pilot_candidate_priority,
            pilot_review_decision_export={
                "metadata": pilot_review_decision_export["metadata"],
                "review_items": [
                    {
                        **pilot_review_decision_export["review_items"][0],
                        "review_requirements": [
                            "curated_active_site_residue_evidence",
                            "specific_reaction_or_mechanism_evidence",
                        ],
                    }
                ],
            },
            pilot_evidence_packet=pilot_evidence_packet,
            pilot_evidence_dossiers=pilot_evidence_dossiers,
        )

        self.assertFalse(
            missing_requirement_gates["gates"][
                "external_pilot_review_decision_export_no_decision"
            ]
        )
        self.assertIn(
            "external_pilot_review_decision_export_no_decision",
            missing_requirement_gates["blockers"],
        )

        ineligible_priority = {
            "metadata": pilot_candidate_priority["metadata"],
            "rows": [
                {
                    **pilot_candidate_priority["rows"][0],
                    "eligible_for_review_pilot": False,
                    "pilot_priority_blockers": ["exact_sequence_holdout"],
                }
            ],
        }
        ineligible_gates = check_external_source_transfer_gates(
            **_base_external_transfer_gate_inputs(),
            pilot_candidate_priority=ineligible_priority,
            pilot_review_decision_export=pilot_review_decision_export,
            pilot_evidence_packet=pilot_evidence_packet,
            pilot_evidence_dossiers=pilot_evidence_dossiers,
        )

        self.assertFalse(
            ineligible_gates["gates"]["external_pilot_candidate_priority_review_only"]
        )
        self.assertIn(
            "external_pilot_candidate_priority_review_only",
            ineligible_gates["blockers"],
        )

    def test_external_transfer_gate_requires_review_only_artifacts(self) -> None:
        gates = check_external_source_transfer_gates(
            transfer_manifest={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                }
            },
            query_manifest={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                }
            },
            ood_calibration_plan={
                "metadata": {
                    "ready_for_label_import": False,
                    "requires_heuristic_control": True,
                }
            },
            candidate_sample_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "countable_label_candidate_count": 0,
                }
            },
            candidate_manifest={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "heuristic_control_required": True,
                }
            },
            candidate_manifest_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "countable_label_candidate_count": 0,
                }
            },
            lane_balance_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "countable_label_candidate_count": 0,
                    "lane_count": 2,
                    "dominant_lane_fraction": 0.5,
                }
            },
            evidence_plan={
                "metadata": {
                    "ready_for_label_import": False,
                    "ready_for_evidence_collection": True,
                    "countable_label_candidate_count": 0,
                    "exact_reference_overlap_holdout_count": 1,
                }
            },
            evidence_request_export={
                "metadata": {
                    "external_source_review_only": True,
                    "countable_label_candidate_count": 0,
                }
            },
            review_only_import_safety_audit={
                "metadata": {
                    "countable_import_safe": True,
                    "total_new_countable_label_count": 0,
                }
            },
            active_site_evidence_queue={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "ready_candidate_count": 1,
                    "deferred_candidate_count": 0,
                },
                "rows": [
                    {
                        "countable_label_candidate": False,
                        "ready_for_label_import": False,
                    }
                ],
            },
            active_site_evidence_sample={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "candidate_with_active_site_feature_count": 1,
                },
                "candidate_summaries": [
                    {
                        "countable_label_candidate": False,
                        "ready_for_label_import": False,
                    }
                ],
                "rows": [
                    {
                        "countable_label_candidate": False,
                        "ready_for_label_import": False,
                    }
                ],
            },
            active_site_evidence_sample_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                    "active_site_feature_gap_count": 0,
                }
            },
            heuristic_control_queue={
                "metadata": {
                    "ready_for_label_import": False,
                    "ready_for_heuristic_control_execution": True,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "ready_candidate_count": 1,
                    "deferred_candidate_count": 0,
                },
                "rows": [
                    {
                        "countable_label_candidate": False,
                        "ready_for_label_import": False,
                    }
                ],
                "deferred_rows": [],
            },
            heuristic_control_queue_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                }
            },
            structure_mapping_plan={
                "metadata": {
                    "ready_for_label_import": False,
                    "ready_for_structure_mapping": True,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "ready_mapping_candidate_count": 1,
                    "deferred_mapping_candidate_count": 0,
                },
                "rows": [
                    {
                        "countable_label_candidate": False,
                        "ready_for_label_import": False,
                    }
                ],
                "deferred_rows": [],
            },
            structure_mapping_plan_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                }
            },
            structure_mapping_sample={
                "metadata": {
                    "ready_for_label_import": False,
                    "ready_for_heuristic_control_scoring": True,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "mapped_candidate_count": 1,
                },
                "entries": [
                    {
                        "countable_label_candidate": False,
                        "ready_for_label_import": False,
                    }
                ],
            },
            structure_mapping_sample_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                }
            },
            heuristic_control_scores={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                },
                "results": [
                    {
                        "countable_label_candidate": False,
                        "ready_for_label_import": False,
                    }
                ],
            },
            heuristic_control_scores_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                }
            },
            external_failure_mode_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                    "failure_mode_count": 2,
                }
            },
        )

        self.assertEqual(gates["blockers"], [])
        self.assertFalse(gates["metadata"]["ready_for_label_import"])
        self.assertTrue(gates["gates"]["active_site_evidence_sample_review_only"])
        self.assertTrue(
            gates["gates"]["active_site_evidence_sample_audit_guardrail_clean"]
        )
        self.assertEqual(
            gates["metadata"]["active_site_evidence_sampled_candidate_count"], 1
        )
        self.assertTrue(gates["gates"]["heuristic_control_queue_review_only"])
        self.assertTrue(
            gates["gates"]["heuristic_control_queue_audit_guardrail_clean"]
        )
        self.assertEqual(
            gates["metadata"]["heuristic_control_ready_candidate_count"], 1
        )
        self.assertTrue(gates["gates"]["structure_mapping_plan_review_only"])
        self.assertTrue(
            gates["gates"]["structure_mapping_plan_audit_guardrail_clean"]
        )
        self.assertEqual(
            gates["metadata"]["structure_mapping_ready_candidate_count"], 1
        )
        self.assertTrue(gates["gates"]["structure_mapping_sample_review_only"])
        self.assertTrue(
            gates["gates"]["structure_mapping_sample_audit_guardrail_clean"]
        )
        self.assertEqual(
            gates["metadata"]["structure_mapping_sample_mapped_candidate_count"], 1
        )
        self.assertTrue(gates["gates"]["heuristic_control_scores_review_only"])
        self.assertTrue(
            gates["gates"]["heuristic_control_scores_audit_guardrail_clean"]
        )
        self.assertEqual(
            gates["metadata"]["heuristic_control_scored_candidate_count"], 1
        )
        self.assertTrue(gates["gates"]["external_failure_mode_audit_review_only"])
        self.assertEqual(gates["metadata"]["external_failure_mode_count"], 2)
        self.assertTrue(gates["metadata"]["ready_for_external_evidence_collection"])
        self.assertEqual(gates["metadata"]["passed_gate_count"], 23)
        self.assertTrue(
            gates["gates"]["external_lane_balance_audit_guardrail_clean"]
        )
        self.assertTrue(gates["gates"]["external_review_only_import_safety_clean"])

    def test_external_transfer_gate_rejects_candidate_lineage_mismatch(self) -> None:
        gates = check_external_source_transfer_gates(
            transfer_manifest={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                }
            },
            query_manifest={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                }
            },
            ood_calibration_plan={
                "metadata": {
                    "ready_for_label_import": False,
                    "requires_heuristic_control": True,
                }
            },
            candidate_sample_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "countable_label_candidate_count": 0,
                }
            },
            candidate_manifest={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "heuristic_control_required": True,
                },
                "rows": [{"accession": "P12345"}],
            },
            candidate_manifest_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "countable_label_candidate_count": 0,
                }
            },
            lane_balance_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "countable_label_candidate_count": 0,
                    "lane_count": 1,
                    "dominant_lane_fraction": 1.0,
                }
            },
            evidence_plan={
                "metadata": {
                    "ready_for_label_import": False,
                    "ready_for_evidence_collection": True,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "exact_reference_overlap_holdout_count": 0,
                },
                "rows": [{"accession": "Q99999"}],
            },
            evidence_request_export={
                "metadata": {
                    "external_source_review_only": True,
                    "countable_label_candidate_count": 0,
                }
            },
            review_only_import_safety_audit={
                "metadata": {
                    "countable_import_safe": True,
                    "total_new_countable_label_count": 0,
                }
            },
            pilot_review_decision_export={
                "metadata": {"candidate_count": 1},
                "review_items": [{"accession": "Q99999"}],
            },
            pilot_evidence_packet={
                "metadata": {"candidate_count": 1},
                "rows": [{"accession": "Q88888"}],
            },
            sequence_holdout_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                },
                "rows": [{"accession": "Q77777"}],
            },
        )

        self.assertFalse(
            gates["gates"]["external_transfer_candidate_lineage_consistent"]
        )
        self.assertIn("external_transfer_candidate_lineage_consistent", gates["blockers"])
        lineage = gates["metadata"]["artifact_lineage"]
        self.assertEqual(
            lineage["unexpected_accessions"]["evidence_plan"], ["Q99999"]
        )
        self.assertEqual(
            lineage["unexpected_accessions"]["pilot_review_decision_export"],
            ["Q99999"],
        )
        self.assertEqual(
            lineage["unexpected_accessions"]["pilot_evidence_packet"],
            ["Q88888"],
        )
        self.assertEqual(
            lineage["unexpected_accessions"]["sequence_holdout_audit"],
            ["Q77777"],
        )
        self.assertEqual(lineage["missing_accessions"]["evidence_plan"], ["P12345"])

    def test_external_transfer_gate_blocks_countable_active_site_queue(self) -> None:
        gates = check_external_source_transfer_gates(
            transfer_manifest={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                }
            },
            query_manifest={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                }
            },
            ood_calibration_plan={
                "metadata": {
                    "ready_for_label_import": False,
                    "requires_heuristic_control": True,
                }
            },
            candidate_sample_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "countable_label_candidate_count": 0,
                }
            },
            candidate_manifest={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                    "candidate_count": 1,
                    "heuristic_control_required": True,
                }
            },
            candidate_manifest_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "countable_label_candidate_count": 0,
                }
            },
            lane_balance_audit={
                "metadata": {
                    "guardrail_clean": True,
                    "countable_label_candidate_count": 0,
                    "lane_count": 2,
                    "dominant_lane_fraction": 0.5,
                }
            },
            evidence_plan={
                "metadata": {
                    "ready_for_label_import": False,
                    "ready_for_evidence_collection": True,
                    "countable_label_candidate_count": 0,
                    "exact_reference_overlap_holdout_count": 0,
                }
            },
            evidence_request_export={
                "metadata": {
                    "external_source_review_only": True,
                    "countable_label_candidate_count": 0,
                }
            },
            review_only_import_safety_audit={
                "metadata": {
                    "countable_import_safe": True,
                    "total_new_countable_label_count": 0,
                }
            },
            active_site_evidence_queue={
                "metadata": {
                    "ready_for_label_import": False,
                    "countable_label_candidate_count": 0,
                    "ready_candidate_count": 1,
                    "deferred_candidate_count": 0,
                },
                "rows": [
                    {
                        "accession": "P12345",
                        "countable_label_candidate": True,
                        "ready_for_label_import": False,
                    }
                ],
                "deferred_rows": [],
            },
        )

        self.assertIn("active_site_evidence_queue_review_only", gates["blockers"])
        self.assertFalse(gates["gates"]["active_site_evidence_queue_review_only"])

    def test_reaction_evidence_sample_fetches_context_without_labels(self) -> None:
        def fake_fetcher(ec_number: str, limit: int) -> dict:
            self.assertEqual(ec_number, "4.1.1.1")
            self.assertEqual(limit, 2)
            return {
                "records": [
                    {
                        "rhea_id": "RHEA:12345",
                        "equation": "A = B + CO2",
                        "mapped_enzyme_count": 4,
                    }
                ]
            }

        sample = build_external_source_reaction_evidence_sample(
            evidence_request_export={
                "review_items": [
                    {
                        "entry_id": "uniprot:P12345",
                        "external_source_context": {
                            "accession": "P12345",
                            "ec_numbers": ["4.1.1.1"],
                            "lane_id": "external_source:lyase",
                            "scope_signal": "lyase",
                        },
                    }
                ]
            },
            max_candidates=1,
            max_reactions_per_ec=2,
            fetcher=fake_fetcher,
        )

        self.assertFalse(sample["metadata"]["ready_for_label_import"])
        self.assertEqual(sample["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(sample["metadata"]["reaction_record_count"], 1)
        self.assertEqual(sample["metadata"]["broad_or_incomplete_ec_count"], 0)
        self.assertFalse(sample["rows"][0]["countable_label_candidate"])
        self.assertEqual(sample["rows"][0]["ec_specificity"], "specific")
        self.assertEqual(sample["rows"][0]["evidence_status"], "reaction_context_only")

    def test_reaction_evidence_audit_blocks_countable_context(self) -> None:
        audit = audit_external_source_reaction_evidence_sample(
            {
                "metadata": {"fetch_failure_count": 0},
                "rows": [
                    {
                        "accession": "P12345",
                        "countable_label_candidate": True,
                        "ec_number": "1.1.1.-",
                        "ec_specificity": "broad_or_incomplete",
                        "evidence_status": "reaction_context_only",
                        "ready_for_label_import": False,
                    }
                ],
            }
        )

        self.assertFalse(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 1)
        self.assertEqual(audit["metadata"]["broad_ec_context_row_count"], 1)
        self.assertIn("reaction_context_rows_marked_countable", audit["blockers"])

    def test_lane_balance_audit_blocks_single_lane_collapse(self) -> None:
        audit = audit_external_source_lane_balance(
            candidate_manifest={
                "rows": [
                    {
                        "accession": "P1",
                        "lane_id": "external_source:lyase",
                        "scope_signal": "lyase",
                        "countable_label_candidate": False,
                    },
                    {
                        "accession": "P2",
                        "lane_id": "external_source:lyase",
                        "scope_signal": "lyase",
                        "countable_label_candidate": False,
                    },
                ]
            },
            min_lanes=2,
            max_dominant_lane_fraction=0.6,
        )

        self.assertFalse(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["lane_count"], 1)
        self.assertIn("external_candidate_lane_count_below_floor", audit["blockers"])
        self.assertIn("external_candidate_lane_collapse", audit["blockers"])

    def test_candidate_manifest_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sample = root / "sample.json"
            queries = root / "queries.json"
            ood = root / "ood.json"
            clusters = root / "clusters.json"
            sequence_failures = root / "sequence_failures.json"
            transfer = root / "transfer.json"
            sample_audit = root / "sample_audit.json"
            manifest = root / "manifest.json"
            audit = root / "audit.json"
            lane_balance = root / "lane_balance.json"
            evidence_plan = root / "evidence_plan.json"
            evidence_export = root / "evidence_export.json"
            active_site_queue = root / "active_site_queue.json"
            transfer_gate = root / "transfer_gate.json"
            import_safety = root / "import_safety.json"
            reaction_sample = root / "reaction_sample.json"
            reaction_sample_audit = root / "reaction_sample_audit.json"
            sample.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "accession": "P12345",
                                "lane_id": "external_source:lyase",
                                "reviewed": "reviewed",
                                "ec_numbers": ["4.1.1.1"],
                                "alphafold_ids": ["P12345"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            ood.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "ready_for_label_import": False,
                            "requires_heuristic_control": True,
                        },
                        "rows": [
                            {
                                "lane_id": "external_source:lyase",
                                "calibration_controls": [
                                    "heuristic_retrieval_control_comparison"
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            queries.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "ready_for_label_import": False,
                            "countable_label_candidate_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            sample_audit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "guardrail_clean": True,
                            "countable_label_candidate_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            clusters.write_text(
                json.dumps({"metadata": {}, "rows": []}), encoding="utf-8"
            )
            sequence_failures.write_text(
                json.dumps({"metadata": {}, "rows": []}), encoding="utf-8"
            )
            transfer.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "ready_for_label_import": False,
                            "countable_label_candidate_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-candidate-manifest",
                    "--candidate-sample",
                    str(sample),
                    "--ood-calibration-plan",
                    str(ood),
                    "--sequence-clusters",
                    str(clusters),
                    "--sequence-similarity-failure-sets",
                    str(sequence_failures),
                    "--transfer-manifest",
                    str(transfer),
                    "--out",
                    str(manifest),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-external-source-lane-balance",
                    "--candidate-manifest",
                    str(manifest),
                    "--min-lanes",
                    "1",
                    "--max-dominant-lane-fraction",
                    "1",
                    "--out",
                    str(lane_balance),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-external-source-candidate-manifest",
                    "--candidate-manifest",
                    str(manifest),
                    "--out",
                    str(audit),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-evidence-plan",
                    "--candidate-manifest",
                    str(manifest),
                    "--candidate-manifest-audit",
                    str(audit),
                    "--out",
                    str(evidence_plan),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-active-site-evidence-queue",
                    "--evidence-plan",
                    str(evidence_plan),
                    "--out",
                    str(active_site_queue),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-evidence-request-export",
                    "--evidence-plan",
                    str(evidence_plan),
                    "--out",
                    str(evidence_export),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            import_safety.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "countable_import_safe": True,
                            "total_new_countable_label_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "check-external-source-transfer-gates",
                    "--transfer-manifest",
                    str(transfer),
                    "--query-manifest",
                    str(queries),
                    "--ood-calibration-plan",
                    str(ood),
                    "--candidate-sample-audit",
                    str(sample_audit),
                    "--candidate-manifest",
                    str(manifest),
                    "--candidate-manifest-audit",
                    str(audit),
                    "--lane-balance-audit",
                    str(lane_balance),
                    "--evidence-plan",
                    str(evidence_plan),
                    "--evidence-request-export",
                    str(evidence_export),
                    "--review-only-import-safety-audit",
                    str(import_safety),
                    "--active-site-evidence-queue",
                    str(active_site_queue),
                    "--out",
                    str(transfer_gate),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-reaction-evidence-sample",
                    "--evidence-request-export",
                    str(evidence_export),
                    "--max-candidates",
                    "0",
                    "--out",
                    str(reaction_sample),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-external-source-reaction-evidence-sample",
                    "--reaction-evidence-sample",
                    str(reaction_sample),
                    "--out",
                    str(reaction_sample_audit),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(manifest.read_text(encoding="utf-8"))
            audit_payload = json.loads(audit.read_text(encoding="utf-8"))
            lane_balance_payload = json.loads(lane_balance.read_text(encoding="utf-8"))
            evidence_payload = json.loads(evidence_plan.read_text(encoding="utf-8"))
            active_site_queue_payload = json.loads(
                active_site_queue.read_text(encoding="utf-8")
            )
            evidence_export_payload = json.loads(
                evidence_export.read_text(encoding="utf-8")
            )
            gate_payload = json.loads(transfer_gate.read_text(encoding="utf-8"))
            reaction_sample_payload = json.loads(
                reaction_sample.read_text(encoding="utf-8")
            )
            reaction_sample_audit_payload = json.loads(
                reaction_sample_audit.read_text(encoding="utf-8")
            )
            self.assertEqual(payload["metadata"]["candidate_count"], 1)
            self.assertEqual(payload["metadata"]["countable_label_candidate_count"], 0)
            self.assertTrue(audit_payload["metadata"]["guardrail_clean"])
            self.assertTrue(lane_balance_payload["metadata"]["guardrail_clean"])
            self.assertEqual(
                evidence_payload["metadata"]["active_site_evidence_required_count"],
                1,
            )
            self.assertEqual(
                active_site_queue_payload["metadata"]["ready_candidate_count"], 1
            )
            self.assertFalse(
                active_site_queue_payload["metadata"]["ready_for_label_import"]
            )
            self.assertTrue(
                evidence_export_payload["metadata"]["external_source_review_only"]
            )
            self.assertEqual(gate_payload["blockers"], [])
            self.assertEqual(
                gate_payload["metadata"]["gate_input_contract"],
                "ExternalSourceTransferGateInputs.v1",
            )
            self.assertTrue(
                gate_payload["gates"]["active_site_evidence_queue_review_only"]
            )
            self.assertEqual(reaction_sample_payload["metadata"]["candidate_count"], 0)
            self.assertFalse(
                reaction_sample_audit_payload["metadata"]["guardrail_clean"]
            )

    def test_external_repair_cli_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            representation_manifest = root / "representation_manifest.json"
            heuristic_scores = root / "heuristic_scores.json"
            reaction_sample = root / "reaction_sample.json"
            representation_comparison = root / "representation_comparison.json"
            representation_comparison_audit = (
                root / "representation_comparison_audit.json"
            )
            representation_backend_plan = root / "representation_backend_plan.json"
            representation_backend_plan_audit = (
                root / "representation_backend_plan_audit.json"
            )
            control_repair = root / "control_repair.json"
            binding_repair = root / "binding_repair.json"
            binding_mapping = root / "binding_mapping.json"
            active_site_requests = root / "active_site_requests.json"
            active_site_evidence = root / "active_site_evidence.json"
            import_readiness = root / "import_readiness.json"
            active_site_sourcing = root / "active_site_sourcing.json"
            active_site_sourcing_audit = root / "active_site_sourcing_audit.json"
            active_site_sourcing_export = root / "active_site_sourcing_export.json"
            active_site_sourcing_export_audit = (
                root / "active_site_sourcing_export_audit.json"
            )
            broad_ec_audit = root / "broad_ec_audit.json"
            candidate_manifest = root / "candidate_manifest.json"
            sequence_holdout = root / "sequence_holdout.json"
            sequence_plan = root / "sequence_plan.json"
            sequence_sample = root / "sequence_sample.json"
            sequence_alignment = root / "sequence_alignment.json"
            sequence_alignment_audit = root / "sequence_alignment_audit.json"
            sequence_search_export = root / "sequence_search_export.json"
            sequence_search_export_audit = root / "sequence_search_export_audit.json"
            transfer_blocker_matrix = root / "transfer_blocker_matrix.json"
            transfer_blocker_matrix_audit = root / "transfer_blocker_matrix_audit.json"

            representation_manifest.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "external_source_representation_control_manifest"
                            )
                        },
                        "rows": [
                            {
                                "accession": "P11111",
                                "entry_id": "uniprot:P11111",
                                "feature_summary": {
                                    "pocket_descriptor_names": ["polar_fraction"],
                                    "residue_codes": ["HIS", "GLU"],
                                    "resolved_residue_count": 2,
                                },
                                "heuristic_baseline_control": {
                                    "top1_fingerprint_id": (
                                        "metal_dependent_hydrolase"
                                    ),
                                    "top1_score": 0.5,
                                },
                                "lane_id": "external_source:isomerase",
                                "scope_signal": "isomerase",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            heuristic_scores.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_heuristic_control_scores"
                        },
                        "results": [
                            {
                                "entry_id": "uniprot:P11111",
                                "top_fingerprints": [
                                    {
                                        "fingerprint_id": (
                                            "metal_dependent_hydrolase"
                                        ),
                                        "score": 0.5,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            reaction_sample.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_reaction_evidence_sample"
                        },
                        "rows": [
                            {
                                "entry_id": "uniprot:P11111",
                                "ec_number": "5.3.1.1",
                                "ec_specificity": "specific",
                                "rhea_id": "RHEA:11111",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            control_repair.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "external_source_control_repair_plan"},
                        "rows": [
                            {
                                "accession": "P11111",
                                "binding_site_feature_count": 1,
                                "countable_label_candidate": False,
                                "repair_type": "active_site_feature_gap",
                            },
                            {
                                "accession": "P22222",
                                "broad_or_incomplete_ec_numbers": ["2.7.1.-"],
                                "countable_label_candidate": False,
                                "repair_type": "broad_ec_disambiguation",
                                "specific_ec_numbers": ["2.7.1.20"],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            binding_repair.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_binding_context_repair_plan"
                        },
                        "rows": [
                            {
                                "accession": "P11111",
                                "binding_position_count": 1,
                                "binding_positions": [
                                    {
                                        "evidence": [{"id": "1ABC", "source": "PDB"}],
                                        "ligand_name": "ATP",
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            binding_mapping.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "external_source_binding_context_mapping_sample"
                            )
                        },
                        "entries": [
                            {
                                "accession": "P11111",
                                "resolved_binding_position_count": 1,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            active_site_evidence.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_active_site_evidence_sample"
                        },
                        "candidate_summaries": [
                            {
                                "accession": "P11111",
                                "pdb_ids_sample": ["1ABC"],
                            }
                        ],
                        "rows": [
                            {
                                "accession": "P11111",
                                "begin": 99,
                                "end": 99,
                                "feature_type": "Binding site",
                                "ligand_name": "ATP",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            candidate_manifest.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "candidate_count": 1,
                            "method": "external_source_candidate_manifest",
                        },
                        "rows": [{"accession": "P11111"}],
                    }
                ),
                encoding="utf-8",
            )
            sequence_holdout.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_sequence_holdout_audit"
                        },
                        "rows": [
                            {
                                "accession": "P11111",
                                "holdout_status": "requires_near_duplicate_search",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            sequence_alignment.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "complete_near_duplicate_search_required": True,
                            "candidate_count": 1,
                            "verified_pair_count": 1,
                        },
                        "rows": [
                            {
                                "accession": "P11111",
                                "countable_label_candidate": False,
                                "ready_for_label_import": False,
                                "verification_status": (
                                    "alignment_no_near_duplicate_signal"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            sequence_sample.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_sequence_neighborhood_sample"
                        },
                        "rows": [
                            {
                                "accession": "P11111",
                                "screen_status": (
                                    "no_high_similarity_hit_in_bounded_screen"
                                ),
                                "top_matches": [
                                    {"reference_accession": "Q11111"}
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            import_readiness.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_import_readiness_audit",
                            "active_site_gap_count": 1,
                        },
                        "rows": [
                            {
                                "accession": "P11111",
                                "readiness_status": (
                                    "blocked_by_active_site_sourcing"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            base_cmd = [sys.executable, "-m", "catalytic_earth.cli"]
            env = {"PYTHONPATH": str(ROOT / "src")}
            subprocess.run(
                base_cmd
                + [
                    "build-external-source-representation-control-comparison",
                    "--representation-control-manifest",
                    str(representation_manifest),
                    "--heuristic-control-scores",
                    str(heuristic_scores),
                    "--reaction-evidence-sample",
                    str(reaction_sample),
                    "--out",
                    str(representation_comparison),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "audit-external-source-representation-control-comparison",
                    "--representation-control-comparison",
                    str(representation_comparison),
                    "--out",
                    str(representation_comparison_audit),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "build-external-source-active-site-gap-source-requests",
                    "--control-repair-plan",
                    str(control_repair),
                    "--binding-context-repair-plan",
                    str(binding_repair),
                    "--binding-context-mapping-sample",
                    str(binding_mapping),
                    "--out",
                    str(active_site_requests),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "audit-external-source-broad-ec-disambiguation",
                    "--control-repair-plan",
                    str(control_repair),
                    "--reaction-evidence-sample",
                    str(reaction_sample),
                    "--out",
                    str(broad_ec_audit),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "build-external-source-sequence-neighborhood-plan",
                    "--candidate-manifest",
                    str(candidate_manifest),
                    "--sequence-holdout-audit",
                    str(sequence_holdout),
                    "--out",
                    str(sequence_plan),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "audit-external-source-sequence-alignment-verification",
                    "--sequence-alignment-verification",
                    str(sequence_alignment),
                    "--out",
                    str(sequence_alignment_audit),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "build-external-source-sequence-search-export",
                    "--sequence-neighborhood-plan",
                    str(sequence_plan),
                    "--sequence-neighborhood-sample",
                    str(sequence_sample),
                    "--sequence-alignment-verification",
                    str(sequence_alignment),
                    "--out",
                    str(sequence_search_export),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "audit-external-source-sequence-search-export",
                    "--sequence-search-export",
                    str(sequence_search_export),
                    "--sequence-neighborhood-plan",
                    str(sequence_plan),
                    "--out",
                    str(sequence_search_export_audit),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "build-external-source-representation-backend-plan",
                    "--representation-control-manifest",
                    str(representation_manifest),
                    "--representation-control-comparison",
                    str(representation_comparison),
                    "--sequence-search-export",
                    str(sequence_search_export),
                    "--out",
                    str(representation_backend_plan),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "audit-external-source-representation-backend-plan",
                    "--representation-backend-plan",
                    str(representation_backend_plan),
                    "--out",
                    str(representation_backend_plan_audit),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "build-external-source-active-site-sourcing-queue",
                    "--active-site-gap-source-requests",
                    str(active_site_requests),
                    "--external-import-readiness-audit",
                    str(import_readiness),
                    "--sequence-alignment-verification",
                    str(sequence_alignment),
                    "--out",
                    str(active_site_sourcing),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "audit-external-source-active-site-sourcing-queue",
                    "--active-site-sourcing-queue",
                    str(active_site_sourcing),
                    "--external-import-readiness-audit",
                    str(import_readiness),
                    "--out",
                    str(active_site_sourcing_audit),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "build-external-source-active-site-sourcing-export",
                    "--active-site-sourcing-queue",
                    str(active_site_sourcing),
                    "--active-site-gap-source-requests",
                    str(active_site_requests),
                    "--active-site-evidence-sample",
                    str(active_site_evidence),
                    "--reaction-evidence-sample",
                    str(reaction_sample),
                    "--out",
                    str(active_site_sourcing_export),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "audit-external-source-active-site-sourcing-export",
                    "--active-site-sourcing-export",
                    str(active_site_sourcing_export),
                    "--active-site-sourcing-queue",
                    str(active_site_sourcing),
                    "--out",
                    str(active_site_sourcing_export_audit),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "build-external-source-transfer-blocker-matrix",
                    "--candidate-manifest",
                    str(candidate_manifest),
                    "--external-import-readiness-audit",
                    str(import_readiness),
                    "--active-site-sourcing-export",
                    str(active_site_sourcing_export),
                    "--sequence-search-export",
                    str(sequence_search_export),
                    "--representation-backend-plan",
                    str(representation_backend_plan),
                    "--out",
                    str(transfer_blocker_matrix),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                base_cmd
                + [
                    "audit-external-source-transfer-blocker-matrix",
                    "--transfer-blocker-matrix",
                    str(transfer_blocker_matrix),
                    "--candidate-manifest",
                    str(candidate_manifest),
                    "--out",
                    str(transfer_blocker_matrix_audit),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )

            comparison_payload = json.loads(
                representation_comparison.read_text(encoding="utf-8")
            )
            comparison_audit_payload = json.loads(
                representation_comparison_audit.read_text(encoding="utf-8")
            )
            representation_backend_payload = json.loads(
                representation_backend_plan.read_text(encoding="utf-8")
            )
            representation_backend_audit_payload = json.loads(
                representation_backend_plan_audit.read_text(encoding="utf-8")
            )
            active_site_payload = json.loads(
                active_site_requests.read_text(encoding="utf-8")
            )
            broad_ec_payload = json.loads(broad_ec_audit.read_text(encoding="utf-8"))
            sequence_payload = json.loads(sequence_plan.read_text(encoding="utf-8"))
            sequence_alignment_payload = json.loads(
                sequence_alignment_audit.read_text(encoding="utf-8")
            )
            sequence_search_export_payload = json.loads(
                sequence_search_export.read_text(encoding="utf-8")
            )
            sequence_search_export_audit_payload = json.loads(
                sequence_search_export_audit.read_text(encoding="utf-8")
            )
            active_site_sourcing_payload = json.loads(
                active_site_sourcing.read_text(encoding="utf-8")
            )
            active_site_sourcing_audit_payload = json.loads(
                active_site_sourcing_audit.read_text(encoding="utf-8")
            )
            active_site_sourcing_export_payload = json.loads(
                active_site_sourcing_export.read_text(encoding="utf-8")
            )
            active_site_sourcing_export_audit_payload = json.loads(
                active_site_sourcing_export_audit.read_text(encoding="utf-8")
            )
            transfer_blocker_matrix_payload = json.loads(
                transfer_blocker_matrix.read_text(encoding="utf-8")
            )
            transfer_blocker_matrix_audit_payload = json.loads(
                transfer_blocker_matrix_audit.read_text(encoding="utf-8")
            )

            self.assertEqual(comparison_payload["metadata"]["candidate_count"], 1)
            self.assertTrue(comparison_audit_payload["metadata"]["guardrail_clean"])
            self.assertEqual(
                representation_backend_payload["metadata"]["candidate_count"], 1
            )
            self.assertTrue(
                representation_backend_audit_payload["metadata"]["guardrail_clean"]
            )
            self.assertEqual(active_site_payload["metadata"]["candidate_count"], 1)
            self.assertEqual(broad_ec_payload["metadata"]["candidate_count"], 1)
            self.assertEqual(sequence_payload["metadata"]["candidate_count"], 1)
            self.assertEqual(
                sequence_payload["metadata"]["near_duplicate_search_request_count"],
                1,
            )
            self.assertTrue(
                sequence_alignment_payload["metadata"]["guardrail_clean"]
            )
            self.assertEqual(
                sequence_search_export_payload["metadata"]["candidate_count"], 1
            )
            self.assertTrue(
                sequence_search_export_audit_payload["metadata"]["guardrail_clean"]
            )
            self.assertEqual(
                active_site_sourcing_payload["metadata"]["candidate_count"], 1
            )
            self.assertTrue(
                active_site_sourcing_audit_payload["metadata"]["guardrail_clean"]
            )
            self.assertEqual(
                active_site_sourcing_export_payload["metadata"]["candidate_count"], 1
            )
            self.assertTrue(
                active_site_sourcing_export_audit_payload["metadata"][
                    "guardrail_clean"
                ]
            )
            self.assertEqual(
                transfer_blocker_matrix_payload["metadata"]["candidate_count"], 1
            )
            self.assertEqual(
                transfer_blocker_matrix_payload["metadata"][
                    "sequence_search_export_candidate_count"
                ],
                1,
            )
            self.assertTrue(
                transfer_blocker_matrix_audit_payload["metadata"]["guardrail_clean"]
            )
