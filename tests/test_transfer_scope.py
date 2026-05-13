from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.transfer_scope import (
    audit_external_source_candidate_manifest,
    audit_external_source_candidate_sample,
    audit_external_source_lane_balance,
    audit_external_source_reaction_evidence_sample,
    build_external_ood_calibration_plan,
    build_external_source_active_site_evidence_queue,
    build_external_source_candidate_manifest,
    build_external_source_candidate_sample,
    build_external_source_evidence_plan,
    build_external_source_evidence_request_export,
    build_external_source_query_manifest,
    build_external_source_reaction_evidence_sample,
    build_external_source_transfer_manifest,
    check_external_source_transfer_gates,
)


ROOT = Path(__file__).resolve().parents[1]


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
        )

        self.assertEqual(gates["blockers"], [])
        self.assertFalse(gates["metadata"]["ready_for_label_import"])
        self.assertTrue(gates["metadata"]["ready_for_external_evidence_collection"])
        self.assertEqual(gates["metadata"]["passed_gate_count"], 10)
        self.assertTrue(
            gates["gates"]["external_lane_balance_audit_guardrail_clean"]
        )
        self.assertTrue(gates["gates"]["external_review_only_import_safety_clean"])

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
            self.assertTrue(
                gate_payload["gates"]["active_site_evidence_queue_review_only"]
            )
            self.assertEqual(reaction_sample_payload["metadata"]["candidate_count"], 0)
            self.assertFalse(
                reaction_sample_audit_payload["metadata"]["guardrail_clean"]
            )
