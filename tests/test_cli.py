from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.cli import _validate_label_factory_gate_cli_lineage

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_label_factory_gate_cli_lineage_rejects_mismatched_slices(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            required = {
                "label_factory_audit": str(root / "v3_label_factory_audit_1000.json"),
                "applied_label_factory": str(
                    root / "v3_label_factory_applied_labels_1025.json"
                ),
                "active_learning_queue": str(
                    root / "v3_active_learning_review_queue_1000.json"
                ),
                "adversarial_negatives": str(
                    root / "v3_adversarial_negative_controls_1000.json"
                ),
                "expert_review_export": str(
                    root / "v3_expert_review_export_1000_post_batch.json"
                ),
                "family_propagation_guardrails": str(
                    root / "v3_family_propagation_guardrails_1000.json"
                ),
            }
            optional = {
                "atp_phosphoryl_transfer_family_expansion": str(
                    root / "v3_atp_phosphoryl_transfer_family_expansion_700.json"
                )
            }

            with self.assertRaisesRegex(
                ValueError,
                "mismatched label-factory gate artifact lineage",
            ):
                _validate_label_factory_gate_cli_lineage(
                    labels_path=str(root / "curated_mechanism_labels.json"),
                    required_artifacts=required,
                    optional_artifacts=optional,
                )

    def test_validate_command(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "catalytic_earth.cli", "validate"],
            cwd=ROOT,
            env={"PYTHONPATH": str(ROOT / "src")},
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Validated", result.stdout)

    def test_build_sequence_cluster_proxy_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            graph = root / "graph.json"
            out = root / "clusters.json"
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"builder": "test"},
                        "nodes": [
                            {"id": "m_csa:1", "type": "m_csa_entry", "name": "first"},
                            {"id": "m_csa:2", "type": "m_csa_entry", "name": "second"},
                        ],
                        "edges": [
                            {
                                "source": "m_csa:1",
                                "target": "uniprot:P12345",
                                "predicate": "has_reference_protein",
                            },
                            {
                                "source": "m_csa:2",
                                "target": "uniprot:P12345",
                                "predicate": "has_reference_protein",
                            },
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
                    "build-sequence-cluster-proxy",
                    "--graph",
                    str(graph),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            clusters = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(clusters["metadata"]["duplicate_cluster_count"], 1)
            self.assertEqual(clusters["duplicate_clusters"][0]["entry_count"], 2)

    def test_external_pilot_priority_cli_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            matrix = root / "matrix.json"
            priority = root / "priority.json"
            review_export = root / "review_export.json"
            matrix.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_transfer_blocker_matrix"
                        },
                        "rows": [
                            {
                                "accession": "PGOOD",
                                "blockers": [
                                    "complete_near_duplicate_search_required"
                                ],
                                "lane_id": "external_source:lane_a",
                                "representation_backend": {
                                    "sample_backend_status": (
                                        "learned_representation_sample_complete"
                                    ),
                                    "sample_near_duplicate_alert": False,
                                },
                                "sequence_search": {
                                    "alignment_status": (
                                        "alignment_no_near_duplicate_signal"
                                    )
                                },
                            },
                            {
                                "accession": "PHOLD",
                                "blockers": ["exact_sequence_holdout"],
                                "lane_id": "external_source:lane_b",
                            },
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
                    "build-external-source-pilot-candidate-priority",
                    "--transfer-blocker-matrix",
                    str(matrix),
                    "--out",
                    str(priority),
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
                    "build-external-source-pilot-review-decision-export",
                    "--pilot-candidate-priority",
                    str(priority),
                    "--out",
                    str(review_export),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            priority_payload = json.loads(priority.read_text(encoding="utf-8"))
            review_payload = json.loads(review_export.read_text(encoding="utf-8"))
            self.assertEqual(
                priority_payload["metadata"]["selected_accessions"], ["PGOOD"]
            )
            self.assertFalse(
                priority_payload["metadata"]["leakage_policy"][
                    "text_or_label_fields_used_for_priority"
                ]
            )
            self.assertEqual(review_payload["metadata"]["candidate_count"], 1)
            self.assertEqual(
                review_payload["metadata"]["decision_status_counts"],
                {"no_decision": 1},
            )

    def test_build_geometry_features_reuse_existing_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            graph = root / "graph.json"
            reuse = root / "reuse.json"
            out = root / "geometry.json"
            reused_row = {
                "entry_id": "m_csa:1",
                "status": "ok",
                "pairwise_distances_angstrom": [{"distance": 1.0}],
                "ligand_context": {
                    "proximal_ligands": [],
                    "cofactor_families": [],
                    "structure_ligands": [],
                    "structure_cofactor_families": [],
                },
                "pocket_context": {"nearby_residue_count": 0},
            }
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"builder": "test"},
                        "nodes": [
                            {
                                "id": "m_csa:1:residue:1",
                                "type": "catalytic_residue",
                                "roles": ["acid"],
                                "structure_positions": [
                                    {
                                        "pdb_id": "1ABC",
                                        "chain_name": "A",
                                        "code": "ASP",
                                        "resid": 7,
                                    }
                                ],
                            }
                        ],
                        "edges": [],
                    }
                ),
                encoding="utf-8",
            )
            reuse.write_text(json.dumps({"entries": [reused_row]}), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-geometry-features",
                    "--graph",
                    str(graph),
                    "--max-entries",
                    "1",
                    "--reuse-existing",
                    str(reuse),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            geometry = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(geometry["metadata"]["reused_entry_count"], 1)
            self.assertEqual(geometry["entries"], [reused_row])

    def test_filter_countable_labels_requires_explicit_lossy_filter(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            labels = Path(tmpdir) / "labels.json"
            out = Path(tmpdir) / "countable.json"
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "m_csa:1",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "confidence": "medium",
                            "evidence_score": 0.65,
                            "evidence": {"sources": ["test"]},
                            "rationale": "This countable baseline label is long enough.",
                        },
                        {
                            "entry_id": "m_csa:2",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "tier": "bronze",
                            "review_status": "needs_expert_review",
                            "confidence": "medium",
                            "evidence_score": 0.55,
                            "evidence": {"sources": ["test"]},
                            "rationale": "This pending review label is long enough.",
                        },
                    ]
                ),
                encoding="utf-8",
            )
            blocked = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "filter-countable-labels",
                    "--labels",
                    str(labels),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                capture_output=True,
                text=True,
            )
            self.assertEqual(blocked.returncode, 2)
            self.assertIn("Refusing to filter", blocked.stdout)
            self.assertFalse(out.exists())
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "filter-countable-labels",
                    "--labels",
                    str(labels),
                    "--out",
                    str(out),
                    "--allow-pending-review",
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(len(json.loads(out.read_text(encoding="utf-8"))), 1)

    def test_summarize_label_factory_batches_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            acceptance = root / "v3_label_batch_acceptance_check_650.json"
            gate = root / "v3_label_factory_gate_check_650.json"
            queue = root / "v3_active_learning_review_queue_650.json"
            scaling_audit = root / "v3_label_scaling_quality_audit_650.json"
            out = root / "summary.json"
            acceptance.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "accepted_for_counting": True,
                            "baseline_label_count": 599,
                            "countable_label_count": 618,
                            "accepted_new_label_count": 19,
                            "pending_review_count": 37,
                            "hard_negative_count": 0,
                            "near_miss_count": 0,
                            "out_of_scope_false_non_abstentions": 0,
                            "actionable_in_scope_failure_count": 0,
                            "factory_gate_ready": True,
                        },
                        "blockers": [],
                    }
                ),
                encoding="utf-8",
            )
            gate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "automation_ready_for_next_label_batch": True,
                            "gate_count": 10,
                            "passed_gate_count": 10,
                        }
                    }
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "total_unlabeled_candidate_count": 32,
                            "unlabeled_omitted_by_max_rows": 0,
                            "all_unlabeled_rows_retained": True,
                        }
                    }
                ),
                encoding="utf-8",
            )
            scaling_audit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "audit_recommendation": "promotion_quality_audit_clean",
                            "accepted_new_debt_count": 0,
                            "unclassified_new_review_debt_entry_ids": [],
                            "omitted_underrepresented_queue_entry_ids": [],
                            "issue_class_counts": {},
                        },
                        "blockers": [],
                        "review_warnings": [
                            "sequence_cluster_artifact_missing_for_near_duplicate_audit"
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
                    "summarize-label-factory-batches",
                    "--acceptance",
                    str(acceptance),
                    "--gate",
                    str(gate),
                    "--active-learning-queue",
                    str(queue),
                    "--scaling-quality-audit",
                    str(scaling_audit),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(summary["metadata"]["latest_batch"], "650")
            self.assertTrue(summary["metadata"]["all_active_queues_retain_unlabeled_candidates"])
            self.assertTrue(summary["metadata"]["latest_scaling_quality_audit_present"])
            self.assertEqual(
                summary["metadata"]["latest_scaling_quality_review_warnings"],
                ["sequence_cluster_artifact_missing_for_near_duplicate_audit"],
            )
            self.assertTrue(summary["rows"][0]["scaling_quality_ready"])

    def test_resolve_local_evidence_repair_lanes_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            plan = root / "plan.json"
            gap = root / "gap.json"
            local_export = root / "local_export.json"
            mismatch_export = root / "mismatch_export.json"
            mismatch_batch = root / "mismatch_batch.json"
            out = root / "resolution.json"
            plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_local_evidence_repair_plan",
                            "planned_entry_count": 2,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "entry_name": "kinase lane",
                                "repair_lane": "expert_reaction_substrate_review",
                                "recommended_next_action": (
                                    "route_to_reaction_substrate_expert_review"
                                ),
                                "local_evidence_gap_classes": [
                                    "reaction_substrate_mismatch_review_required"
                                ],
                                "non_countable_blockers": [
                                    "reaction_substrate_mismatch_review_required"
                                ],
                            },
                            {
                                "entry_id": "m_csa:2",
                                "entry_name": "mapping lane",
                                "repair_lane": (
                                    "source_explicit_alternate_structure_residue_positions"
                                ),
                                "recommended_next_action": (
                                    "source_explicit_alternate_structure_residue_positions"
                                ),
                                "local_evidence_gap_classes": [
                                    "alternate_structures_lack_explicit_residue_positions"
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            gap.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "expert_label_decision_local_evidence_gap_audit"
                            )
                        },
                        "rows": [],
                    }
                ),
                encoding="utf-8",
            )
            local_export.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "expert_label_decision_local_evidence_review_export"
                            )
                        },
                        "review_items": [
                            {
                                "entry_id": "m_csa:1",
                                "decision": {
                                    "action": "no_decision",
                                    "local_evidence_resolution": "needs_more_evidence",
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            mismatch_export.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "reaction_substrate_mismatch_review_export",
                            "exported_entry_ids": ["m_csa:1"],
                        },
                        "review_items": [{"entry_id": "m_csa:1"}],
                    }
                ),
                encoding="utf-8",
            )
            mismatch_batch.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "provisional_label_review_decision_batch"
                        },
                        "review_items": [
                            {
                                "entry_id": "m_csa:1",
                                "decision": {
                                    "action": "accept_label",
                                    "label_type": "out_of_scope",
                                    "review_status": "expert_reviewed",
                                    "reviewer": "tester",
                                    "reaction_substrate_resolution": (
                                        "confirm_current_label_or_out_of_scope"
                                    ),
                                    "rationale": "Reviewed as a kinase boundary lane.",
                                },
                            }
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
                    "resolve-expert-label-decision-local-evidence-repair-lanes",
                    "--expert-label-decision-local-evidence-repair-plan",
                    str(plan),
                    "--expert-label-decision-local-evidence-gap-audit",
                    str(gap),
                    "--expert-label-decision-local-evidence-review-export",
                    str(local_export),
                    "--reaction-substrate-mismatch-review-export",
                    str(mismatch_export),
                    "--reaction-substrate-mismatch-decision-batch",
                    str(mismatch_batch),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            resolution = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(resolution["metadata"]["resolution_ready"])
            self.assertEqual(resolution["metadata"]["resolved_entry_ids"], ["m_csa:1"])
            self.assertEqual(
                resolution["metadata"]["remaining_open_entry_ids"], ["m_csa:2"]
            )
            self.assertEqual(
                resolution["metadata"]["countable_label_candidate_count"], 0
            )

    def test_build_explicit_alternate_residue_position_requests_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            plan = root / "plan.json"
            remediation = root / "remediation.json"
            graph = root / "graph.json"
            out = root / "requests.json"
            plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_local_evidence_repair_plan"
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:7",
                                "entry_name": "alternate residue lane",
                                "repair_lane": (
                                    "source_explicit_alternate_structure_residue_positions"
                                ),
                                "recommended_next_action": (
                                    "source_explicit_alternate_structure_residue_positions"
                                ),
                                "selected_pdb_id": "1AAA",
                                "selected_pdb_residue_position_count": 1,
                                "alternate_pdb_count": 2,
                                "alternate_pdb_with_residue_positions_count": 0,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            remediation.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_remediation"},
                        "rows": [
                            {
                                "entry_id": "m_csa:7",
                                "candidate_pdb_structure_ids": [
                                    "1AAA",
                                    "2BBB",
                                    "3CCC",
                                ],
                                "alternate_pdb_ids": ["2BBB", "3CCC"],
                                "expected_cofactor_families": ["metal_ion"],
                                "gap_reasons": ["review_marked_needs_more_evidence"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "nodes": [
                            {
                                "id": "m_csa:7",
                                "type": "m_csa_entry",
                                "reference_uniprot_id": "P00007",
                            }
                        ],
                        "edges": [
                            {
                                "source": "m_csa:7",
                                "target": "ec:1.2.3.4",
                                "predicate": "has_ec",
                            }
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
                    "build-explicit-alternate-residue-position-requests",
                    "--expert-label-decision-local-evidence-repair-plan",
                    str(plan),
                    "--review-debt-remediation",
                    str(remediation),
                    "--graph",
                    str(graph),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            requests = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(requests["metadata"]["sourcing_request_ready"])
            self.assertEqual(requests["metadata"]["request_entry_ids"], ["m_csa:7"])
            self.assertEqual(
                requests["metadata"]["candidate_alternate_structure_count"], 2
            )
            self.assertEqual(requests["rows"][0]["reference_uniprot_id"], "P00007")
            self.assertEqual(requests["rows"][0]["ec_ids"], ["ec:1.2.3.4"])
            self.assertFalse(requests["rows"][0]["countable_label_candidate"])

    def test_summarize_review_debt_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            gaps = root / "v3_review_evidence_gaps_650.json"
            queue = root / "v3_active_learning_review_queue_650.json"
            baseline = root / "baseline_review_debt.json"
            out = root / "review_debt.json"
            gaps.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_evidence_gap_analysis"},
                        "rows": [
                            {
                                "entry_id": "m_csa:650",
                                "entry_name": "phospholipase A1",
                                "decision_action": "mark_needs_more_evidence",
                                "coverage_status": "expected_structure_only",
                                "gap_reasons": ["counterevidence_present"],
                                "target_fingerprint_id": "ser_his_acid_hydrolase",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps({"rows": [{"entry_id": "m_csa:650", "rank": 1, "review_score": 8.0}]}),
                encoding="utf-8",
            )
            baseline.write_text(json.dumps({"rows": []}), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "summarize-review-debt",
                    "--review-evidence-gaps",
                    str(gaps),
                    "--active-learning-queue",
                    str(queue),
                    "--baseline-review-debt",
                    str(baseline),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(summary["metadata"]["review_debt_count"], 1)
            self.assertEqual(summary["metadata"]["new_review_debt_count"], 1)
            self.assertEqual(summary["metadata"]["new_review_debt_entry_ids"], ["m_csa:650"])
            self.assertEqual(
                summary["metadata"]["recommended_next_action_counts_by_debt_status"]["new"],
                {"verify_local_cofactor_or_active_site_mapping": 1},
            )
            self.assertEqual(summary["rows"][0]["entry_id"], "m_csa:650")

    def test_analyze_review_debt_remediation_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            debt = root / "review_debt.json"
            gaps = root / "review_gaps.json"
            graph = root / "graph.json"
            geometry = root / "geometry.json"
            out = root / "remediation.json"
            debt.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_summary",
                            "review_debt_entry_ids": ["m_csa:651"],
                            "new_review_debt_entry_ids": ["m_csa:651"],
                            "carried_review_debt_entry_ids": [],
                        },
                        "rows": [],
                    }
                ),
                encoding="utf-8",
            )
            gaps.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_evidence_gap_analysis"},
                        "rows": [
                            {
                                "entry_id": "m_csa:651",
                                "entry_name": "flavin gap",
                                "decision_action": "mark_needs_more_evidence",
                                "coverage_status": "expected_absent_from_structure",
                                "gap_reasons": ["expected_cofactor_absent_from_structure"],
                                "expected_cofactor_families": ["flavin"],
                                "local_cofactor_families": [],
                                "structure_cofactor_families": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "nodes": [
                            {
                                "id": "pdb:1AAA",
                                "type": "structure",
                                "structure_source": "pdb",
                                "structure_id": "1AAA",
                            },
                            {
                                "id": "pdb:2BBB",
                                "type": "structure",
                                "structure_source": "pdb",
                                "structure_id": "2BBB",
                            },
                        ],
                        "edges": [
                            {
                                "source": "m_csa:651",
                                "target": "uniprot:P651",
                                "predicate": "has_reference_protein",
                            },
                            {
                                "source": "uniprot:P651",
                                "target": "pdb:1AAA",
                                "predicate": "has_structure",
                            },
                            {
                                "source": "uniprot:P651",
                                "target": "pdb:2BBB",
                                "predicate": "has_structure",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps({"entries": [{"entry_id": "m_csa:651", "pdb_id": "1AAA", "status": "ok"}]}),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "analyze-review-debt-remediation",
                    "--review-debt",
                    str(debt),
                    "--review-evidence-gaps",
                    str(gaps),
                    "--graph",
                    str(graph),
                    "--geometry",
                    str(geometry),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            plan = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(plan["metadata"]["requested_entry_count"], 1)
            self.assertEqual(plan["rows"][0]["entry_id"], "m_csa:651")
            self.assertEqual(plan["rows"][0]["alternate_pdb_ids"], ["2BBB"])

    def test_summarize_review_debt_remap_leads_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scan = root / "scan.json"
            remediation = root / "remediation.json"
            out = root / "remap_leads.json"
            scan.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_alternate_structure_scan"},
                        "rows": [
                            {
                                "entry_id": "m_csa:653",
                                "entry_name": "alternate local flavin gap",
                                "remediation_bucket": "alternate_pdb_ligand_scan",
                                "expected_cofactor_families": ["flavin"],
                                "structure_hits": [
                                    {
                                        "pdb_id": "2BBB",
                                        "ligand_codes": ["FAD"],
                                        "expected_family_hits": ["flavin"],
                                        "local_ligand_codes": ["FAD"],
                                        "local_cofactor_families": ["flavin"],
                                        "local_expected_family_hits": ["flavin"],
                                        "is_selected_structure": False,
                                        "residue_position_source": "selected_position_remap",
                                        "residue_position_remap_basis": "same_chain_residue_id",
                                        "usable_residue_position_count": 1,
                                        "remapped_residue_position_count": 1,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            remediation.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:653",
                                "debt_status": "carried",
                                "coverage_status": "expected_absent_from_structure",
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
                    "summarize-review-debt-remap-leads",
                    "--alternate-structure-scan",
                    str(scan),
                    "--remediation",
                    str(remediation),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(summary["metadata"]["lead_count"], 1)
            self.assertEqual(
                summary["metadata"]["local_expected_family_hit_from_remap_entry_ids"],
                ["m_csa:653"],
            )
            self.assertFalse(summary["rows"][0]["countable_label_candidate"])

    def test_audit_review_debt_remap_local_leads_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            remap_leads = root / "remap_leads.json"
            remediation = root / "remediation.json"
            out = root / "audit.json"
            remap_leads.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_remap_lead_summary"},
                        "rows": [
                            {
                                "entry_id": "m_csa:653",
                                "entry_name": "alternate local metal gap",
                                "lead_type": "local_expected_family_hit_from_remap",
                                "gap_reasons": [
                                    "counterevidence_present",
                                    "expected_cofactor_absent_from_structure",
                                ],
                                "expected_cofactor_families": ["metal_ion"],
                                "local_expected_family_hit_pdb_ids": ["2BBB"],
                                "local_expected_family_hit_from_remap_pdb_ids": [
                                    "2BBB"
                                ],
                                "local_expected_ligand_codes": ["ZN"],
                                "remap_basis_counts": {"same_chain_residue_id": 1},
                                "remapped_residue_position_structure_count": 1,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            remediation.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:653",
                                "selected_pdb_id": "1AAA",
                                "coverage_status": "expected_absent_from_structure",
                                "selected_active_site_has_expected_family": False,
                                "selected_structure_has_expected_family": False,
                                "alternate_pdb_with_residue_positions_count": 0,
                                "candidate_pdb_with_residue_positions_count": 1,
                                "counterevidence_reasons": [
                                    "role_inferred_metal_low_pocket_support"
                                ],
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
                    "audit-review-debt-remap-local-leads",
                    "--remap-leads",
                    str(remap_leads),
                    "--remediation",
                    str(remediation),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(audit["metadata"]["audited_entry_count"], 1)
            self.assertEqual(
                audit["metadata"]["expert_family_boundary_review_entry_ids"],
                ["m_csa:653"],
            )
            self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
            self.assertTrue(audit["rows"][0]["strict_remap_guardrail_required"])

    def test_summarize_review_debt_structure_selection_candidates_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            remap_local_audit = root / "remap_local_audit.json"
            alternate_scan = root / "alternate_scan.json"
            out = root / "structure_selection.json"
            remap_local_audit.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_remap_local_lead_audit"},
                        "rows": [
                            {
                                "entry_id": "m_csa:654",
                                "entry_name": "clean remap lead",
                                "audit_decision": "local_structure_selection_rule_candidate",
                                "selected_pdb_id": "3AAA",
                                "selected_structure_gap_reasons": [
                                    "selected_structure_missing_expected_cofactor_family"
                                ],
                                "selected_active_site_has_expected_family": False,
                                "selected_structure_has_expected_family": False,
                                "expected_cofactor_families": ["metal_ion"],
                                "local_expected_ligand_codes": ["MG"],
                                "local_expected_family_hit_from_remap_pdb_ids": [
                                    "3CCC"
                                ],
                                "strict_remap_guardrail_required": True,
                                "alternate_pdb_with_explicit_residue_positions_count": 0,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate_scan.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_debt_alternate_structure_scan"},
                        "rows": [
                            {
                                "entry_id": "m_csa:654",
                                "entry_name": "clean remap lead",
                                "structure_hits": [
                                    {
                                        "pdb_id": "3CCC",
                                        "residue_position_source": "selected_position_remap",
                                        "residue_position_remap_basis": "same_chain_residue_id",
                                        "usable_residue_position_count": 2,
                                        "remapped_residue_position_count": 2,
                                        "expected_family_hits": ["metal_ion"],
                                        "local_expected_family_hits": ["metal_ion"],
                                        "local_ligand_codes": ["BGC", "MG"],
                                        "ligand_codes": ["ANP", "BGC", "MG"],
                                    }
                                ],
                            }
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
                    "summarize-review-debt-structure-selection-candidates",
                    "--remap-local-lead-audit",
                    str(remap_local_audit),
                    "--alternate-structure-scan",
                    str(alternate_scan),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(summary["metadata"]["candidate_entry_ids"], ["m_csa:654"])
            self.assertEqual(summary["metadata"]["countable_label_candidate_count"], 0)
            self.assertEqual(summary["rows"][0]["candidate_local_expected_ligand_codes"], ["MG"])

    def test_audit_reaction_substrate_mismatches_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            queue = root / "queue.json"
            out = root / "reaction_mismatch.json"
            queue.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:655",
                                "entry_name": "glucokinase-like lead",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "mechanism_text_snippets": [
                                    "Glucose attacks the gamma phosphorous of ATP."
                                ],
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
                    "audit-reaction-substrate-mismatches",
                    "--active-learning-queue",
                    str(queue),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(audit["metadata"]["mismatch_entry_ids"], ["m_csa:655"])
            self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_build_reaction_substrate_mismatch_review_export_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            labels = root / "labels.json"
            reaction_audit = root / "reaction_mismatch.json"
            family_guardrails = root / "family_guardrails.json"
            out = root / "reaction_mismatch_review_export.json"
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "m_csa:655",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "confidence": "medium",
                            "rationale": "kinase boundary control kept outside the seed set",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "evidence_score": 0.65,
                            "evidence": {"sources": ["test"]},
                        }
                    ]
                ),
                encoding="utf-8",
            )
            reaction_audit.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "reaction_substrate_mismatch_audit"},
                        "rows": [
                            {
                                "entry_id": "m_csa:655",
                                "entry_name": "glucokinase-like lead",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "mismatch_reasons": ["kinase_name_with_hydrolase_top1"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            family_guardrails.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "family_propagation_guardrail_audit"},
                        "rows": [
                            {
                                "entry_id": "m_csa:655",
                                "entry_name": "glucokinase-like lead",
                                "label_state": "labeled",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "reaction_substrate_mismatch_reasons": [
                                    "kinase_name_with_hydrolase_top1"
                                ],
                            },
                            {
                                "entry_id": "m_csa:656",
                                "entry_name": "pending ribokinase",
                                "label_state": "unlabeled",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "reaction_substrate_mismatch_reasons": [
                                    "kinase_name_with_hydrolase_top1"
                                ],
                            },
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
                    "build-reaction-substrate-mismatch-review-export",
                    "--reaction-substrate-mismatch-audit",
                    str(reaction_audit),
                    "--family-propagation-guardrails",
                    str(family_guardrails),
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
            export = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(export["metadata"]["exported_count"], 2)
            self.assertTrue(export["metadata"]["all_family_guardrail_mismatches_exported"])
            self.assertEqual(
                export["metadata"]["recommended_path"],
                "expert_reaction_substrate_review_before_ontology_split",
            )

    def test_build_expert_label_decision_review_export_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            labels = root / "labels.json"
            queue = root / "queue.json"
            debt = root / "review_debt.json"
            mismatch_export = root / "mismatch_export.json"
            remediation = root / "remediation.json"
            structure_mapping = root / "structure_mapping.json"
            alternate_scan = root / "alternate_scan.json"
            out = root / "expert_label_decision_export.json"
            repair_out = root / "expert_label_decision_repair.json"
            guardrail_out = root / "expert_label_decision_repair_guardrail.json"
            local_gap_out = root / "expert_label_decision_local_gap.json"
            local_gap_export_out = root / "expert_label_decision_local_gap_export.json"
            local_gap_plan_out = root / "expert_label_decision_local_gap_plan.json"
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "m_csa:1",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "confidence": "medium",
                            "rationale": "Existing boundary control kept outside seed labels.",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "evidence_score": 0.65,
                            "evidence": {"sources": ["test"]},
                        }
                    ]
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "active_learning_label_review_queue"},
                        "rows": [
                            {
                                "rank": 1,
                                "entry_id": "m_csa:650",
                                "entry_name": "phospholipase A1",
                                "label_state": "unlabeled",
                                "recommended_action": "expert_label_decision_needed",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "top1_ontology_family": "hydrolysis",
                                "top1_score": 0.61,
                                "top2_fingerprint_id": "ser_his_acid_hydrolase",
                                "top2_score": 0.45,
                                "abstain_threshold": 0.4115,
                                "cofactor_evidence_level": "ligand_supported",
                                "readiness_blockers": [
                                    "fewer_than_three_resolved_residues"
                                ],
                                "counterevidence_reasons": [],
                                "reaction_substrate_mismatch_reasons": [],
                                "mechanism_text_snippets": [
                                    "Ser-His hydrolase text with no explicit metal catalysis."
                                ],
                            },
                            {
                                "rank": 2,
                                "entry_id": "m_csa:655",
                                "entry_name": "glucokinase",
                                "label_state": "unlabeled",
                                "recommended_action": "expert_label_decision_needed",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "top1_ontology_family": "hydrolysis",
                                "top1_score": 0.5,
                                "abstain_threshold": 0.4115,
                                "cofactor_evidence_level": "ligand_supported",
                                "readiness_blockers": [],
                                "counterevidence_reasons": [
                                    "nucleotide_transfer_ligand_context"
                                ],
                                "reaction_substrate_mismatch_reasons": [
                                    "kinase_name_with_hydrolase_top1"
                                ],
                                "mechanism_text_snippets": [
                                    "ATP phosphoryl transfer to glucose."
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            debt.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_summary",
                            "carried_review_debt_entry_ids": ["m_csa:650"],
                            "new_review_debt_entry_ids": ["m_csa:655"],
                        },
                        "rows": [{"entry_id": "m_csa:650"}],
                    }
                ),
                encoding="utf-8",
            )
            mismatch_export.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "reaction_substrate_mismatch_review_export",
                            "exported_count": 1,
                            "exported_entry_ids": ["m_csa:655"],
                        },
                        "review_items": [{"entry_id": "m_csa:655"}],
                    }
                ),
                encoding="utf-8",
            )
            remediation.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:650",
                                "remediation_bucket": "active_site_mapping_repair",
                                "selected_pdb_id": "1ABC",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            structure_mapping.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:650",
                                "status": "insufficient_resolved_residues",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            alternate_scan.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:650",
                                "scan_outcome": "no_expected_cofactor_in_scanned_structures",
                                "scanned_structure_count": 3,
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
                    "build-expert-label-decision-review-export",
                    "--active-learning-queue",
                    str(queue),
                    "--labels",
                    str(labels),
                    "--review-debt",
                    str(debt),
                    "--reaction-substrate-mismatch-review-export",
                    str(mismatch_export),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            export = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(export["metadata"]["exported_count"], 2)
            self.assertEqual(export["metadata"]["decision_counts"], {"no_decision": 2})
            self.assertEqual(export["metadata"]["countable_label_candidate_count"], 0)
            self.assertEqual(
                export["metadata"][
                    "missing_reaction_substrate_mismatch_export_entry_ids"
                ],
                [],
            )
            self.assertEqual(
                export["metadata"]["quality_risk_flag_counts"][
                    "external_expert_decision_required"
                ],
                2,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "summarize-expert-label-decision-repair-candidates",
                    "--expert-label-decision-review-export",
                    str(out),
                    "--review-debt-remediation",
                    str(remediation),
                    "--structure-mapping",
                    str(structure_mapping),
                    "--alternate-structure-scan",
                    str(alternate_scan),
                    "--max-rows",
                    "0",
                    "--out",
                    str(repair_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            repair = json.loads(repair_out.read_text(encoding="utf-8"))
            self.assertEqual(repair["metadata"]["candidate_count"], 2)
            self.assertEqual(repair["metadata"]["countable_label_candidate_count"], 0)
            self.assertEqual(
                repair["metadata"]["repair_bucket_counts"][
                    "reaction_substrate_review_already_exported"
                ],
                1,
            )
            self.assertEqual(repair["metadata"]["remediation_context_linked_count"], 1)
            self.assertEqual(
                repair["metadata"]["structure_mapping_context_linked_count"], 1
            )
            self.assertEqual(
                repair["metadata"]["alternate_structure_scan_context_linked_count"], 1
            )
            rows = {row["entry_id"]: row for row in repair["rows"]}
            self.assertEqual(
                rows["m_csa:650"]["alternate_structure_scan_context"][
                    "scanned_structure_count"
                ],
                3,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-expert-label-decision-repair-guardrails",
                    "--expert-label-decision-repair-candidates",
                    str(repair_out),
                    "--out",
                    str(guardrail_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            guardrail = json.loads(guardrail_out.read_text(encoding="utf-8"))
            self.assertTrue(guardrail["metadata"]["guardrail_ready"])
            self.assertEqual(guardrail["metadata"]["priority_repair_row_count"], 1)
            self.assertEqual(
                guardrail["metadata"]["countable_label_candidate_count"], 0
            )
            self.assertIn(
                "active_site_mapping_or_structure_gap_unresolved",
                guardrail["rows"][0]["non_countable_blockers"],
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-expert-label-decision-local-evidence-gaps",
                    "--expert-label-decision-repair-guardrail-audit",
                    str(guardrail_out),
                    "--expert-label-decision-repair-candidates",
                    str(repair_out),
                    "--out",
                    str(local_gap_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            local_gap = json.loads(local_gap_out.read_text(encoding="utf-8"))
            self.assertTrue(local_gap["metadata"]["audit_ready"])
            self.assertEqual(local_gap["metadata"]["audited_entry_count"], 1)
            self.assertEqual(
                local_gap["metadata"]["countable_label_candidate_count"], 0
            )
            self.assertIn(
                "scanned_structures_without_local_expected_family_hit",
                local_gap["rows"][0]["local_evidence_gap_classes"],
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-expert-label-decision-local-evidence-review-export",
                    "--expert-label-decision-local-evidence-gap-audit",
                    str(local_gap_out),
                    "--labels",
                    str(labels),
                    "--out",
                    str(local_gap_export_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            local_gap_export = json.loads(
                local_gap_export_out.read_text(encoding="utf-8")
            )
            self.assertTrue(local_gap_export["metadata"]["export_ready"])
            self.assertEqual(local_gap_export["metadata"]["decision_counts"], {"no_decision": 1})
            self.assertEqual(
                local_gap_export["metadata"]["countable_label_candidate_count"], 0
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "summarize-expert-label-decision-local-evidence-repair-plan",
                    "--expert-label-decision-local-evidence-gap-audit",
                    str(local_gap_out),
                    "--expert-label-decision-local-evidence-review-export",
                    str(local_gap_export_out),
                    "--out",
                    str(local_gap_plan_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            local_gap_plan = json.loads(
                local_gap_plan_out.read_text(encoding="utf-8")
            )
            self.assertTrue(local_gap_plan["metadata"]["repair_plan_ready"])
            self.assertEqual(local_gap_plan["metadata"]["planned_entry_count"], 1)

    def test_import_countable_review_rejects_automation_mismatch_accepts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            labels = root / "labels.json"
            review = root / "mismatch_review.json"
            out = root / "countable_labels.json"
            labels.write_text("[]", encoding="utf-8")
            review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "reaction_substrate_mismatch_review_export"
                        },
                        "review_items": [
                            {
                                "entry_id": "m_csa:656",
                                "entry_name": "pending ribokinase",
                                "decision": {
                                    "action": "accept_label",
                                    "label_type": "seed_fingerprint",
                                    "fingerprint_id": "metal_dependent_hydrolase",
                                    "tier": "bronze",
                                    "confidence": "medium",
                                    "reviewer": "automation_label_factory",
                                    "rationale": (
                                        "Automation must not count mismatch "
                                        "review rows without expert resolution."
                                    ),
                                    "evidence_score": 0.65,
                                    "review_status": "automation_curated",
                                    "reaction_substrate_resolution": "needs_more_evidence",
                                },
                            }
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
                    "import-countable-label-review",
                    "--review",
                    str(review),
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

            self.assertEqual(json.loads(out.read_text(encoding="utf-8")), [])

    def test_audit_review_only_import_safety_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            labels = root / "labels.json"
            review = root / "review_only_batch.json"
            out = root / "import_safety.json"
            labels.write_text("[]", encoding="utf-8")
            review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "provisional_label_review_decision_batch",
                            "source_method": "reaction_substrate_mismatch_review_export",
                            "reaction_substrate_mismatch_review_only": True,
                            "decision_counts": {"accept_label": 1},
                        },
                        "review_items": [
                            {
                                "entry_id": "m_csa:656",
                                "entry_name": "pending ribokinase",
                                "decision": {
                                    "action": "accept_label",
                                    "label_type": "out_of_scope",
                                    "fingerprint_id": None,
                                    "tier": "bronze",
                                    "confidence": "high",
                                    "reviewer": "test_reviewer",
                                    "rationale": "Reviewed but still review-only.",
                                    "evidence_score": None,
                                    "review_status": "expert_reviewed",
                                    "reaction_substrate_resolution": (
                                        "confirm_current_label_or_out_of_scope"
                                    ),
                                },
                            }
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
                    "audit-review-only-import-safety",
                    "--review",
                    str(review),
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
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(audit["metadata"]["countable_import_safe"])
            self.assertEqual(audit["metadata"]["total_new_countable_label_count"], 0)
            self.assertTrue(
                audit["rows"][0]["review_only_flags"][
                    "reaction_substrate_mismatch_review_only"
                ]
            )

    def test_audit_accepted_review_debt_deferrals_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            review_debt = root / "review_debt.json"
            acceptance = root / "acceptance.json"
            remap = root / "remap.json"
            import_safety = root / "import_safety.json"
            out = root / "deferrals.json"
            review_debt.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_summary",
                            "review_debt_entry_ids": ["m_csa:712"],
                            "new_review_debt_entry_ids": ["m_csa:712"],
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:712",
                                "entry_name": "strict remap local lead",
                                "debt_status": "new",
                                "recommended_next_action": (
                                    "expert_family_boundary_review"
                                ),
                                "decision_action": "mark_needs_more_evidence",
                                "gap_reasons": ["review_marked_needs_more_evidence"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            acceptance.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "label_batch_acceptance_check",
                            "accepted_new_label_entry_ids": ["m_csa:705"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            remap.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_remap_local_lead_audit",
                            "strict_remap_guardrail_entry_ids": ["m_csa:712"],
                            "expert_family_boundary_review_entry_ids": ["m_csa:712"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            import_safety.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_only_import_safety_audit",
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
                    "audit-accepted-review-debt-deferrals",
                    "--review-debt",
                    str(review_debt),
                    "--acceptance",
                    str(acceptance),
                    "--remap-local-lead-audit",
                    str(remap),
                    "--review-only-import-safety-audit",
                    str(import_safety),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(audit["metadata"]["deferral_ready"])
            self.assertEqual(audit["metadata"]["deferred_entry_count"], 1)
            self.assertEqual(
                audit["rows"][0]["deferral_status"],
                "deferred_strict_remap_family_boundary_review",
            )

    def test_audit_mechanism_ontology_gaps_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            queue = root / "queue.json"
            repair = root / "repair.json"
            local_gap = root / "local_gap.json"
            out = root / "ontology_gap.json"
            queue.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "rank": 1,
                                "entry_id": "m_csa:655",
                                "entry_name": "glucokinase",
                                "recommended_action": "expert_label_decision_needed",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "top1_ontology_family": "hydrolysis",
                                "reaction_substrate_mismatch_reasons": [
                                    "kinase_name_with_hydrolase_top1"
                                ],
                                "mechanism_text_snippets": [
                                    "ATP phosphoryl transfer to glucose."
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            repair.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:655",
                                "quality_risk_flags": [
                                    "text_leakage_or_nonlocal_evidence_risk"
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            local_gap.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_local_evidence_gap_audit"
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:655",
                                "local_evidence_gap_classes": [
                                    "reaction_substrate_mismatch_review_required"
                                ],
                                "recommended_next_action": (
                                    "route_to_reaction_substrate_expert_review"
                                ),
                            }
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
                    "audit-mechanism-ontology-gaps",
                    "--active-learning-queue",
                    str(queue),
                    "--expert-label-decision-repair-candidates",
                    str(repair),
                    "--expert-label-decision-local-evidence-gap-audit",
                    str(local_gap),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(audit["metadata"]["candidate_scope_signal_count"], 1)
            self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
            self.assertEqual(
                audit["metadata"]["local_evidence_gap_context_entry_count"], 1
            )
            self.assertIn("transferase_phosphoryl", audit["rows"][0]["scope_signals"])
            self.assertIn(
                "local_evidence_gap_unresolved",
                audit["rows"][0]["ontology_update_blockers"],
            )

    def test_build_atp_phosphoryl_transfer_family_expansion_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            decision_batch = root / "mismatch_decisions.json"
            out = root / "atp_families.json"
            hints = [
                ("m_csa:35", "phosphorylase kinase", "ePK"),
                ("m_csa:592", "glucokinase", "ASKHA"),
                ("m_csa:498", "glutathione synthase", "ATP-grasp"),
                ("m_csa:603", "pyruvate dehydrogenase kinase", "GHKL"),
                ("m_csa:588", "thymidine kinase", "dNK"),
                ("m_csa:637", "nucleoside-diphosphate kinase", "NDK"),
                ("m_csa:365", "Phosphofructokinase I", "PfkA"),
                ("m_csa:663", "ribokinase", "PfkB"),
                ("m_csa:654", "CDP-ME kinase", "GHMP"),
            ]
            decision_batch.write_text(
                json.dumps(
                    {
                        "review_items": [
                            {
                                "entry_id": entry_id,
                                "entry_name": name,
                                "mismatch_context": {
                                    "entry_id": entry_id,
                                    "entry_name": name,
                                    "top1_fingerprint_id": (
                                        "metal_dependent_hydrolase"
                                    ),
                                    "top1_ontology_family": "hydrolysis",
                                    "mismatch_reasons": [
                                        "kinase_name_with_hydrolase_top1"
                                    ],
                                },
                                "decision": {
                                    "action": "reject_label",
                                    "label_type": "out_of_scope",
                                    "review_status": "expert_reviewed",
                                    "reviewer": "test_reviewer",
                                    "reaction_substrate_resolution": (
                                        "confirm_current_label_or_out_of_scope"
                                    ),
                                    "future_fingerprint_family_hint": hint,
                                },
                            }
                            for entry_id, name, hint in hints
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
                    "build-atp-phosphoryl-transfer-family-expansion",
                    "--reaction-substrate-mismatch-decision-batch",
                    str(decision_batch),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            expansion = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(expansion["metadata"]["boundary_guardrail_ready"])
            self.assertEqual(expansion["metadata"]["countable_label_candidate_count"], 0)
            self.assertEqual(
                expansion["metadata"]["mapped_required_family_ids"],
                [
                    "askha",
                    "atp_grasp",
                    "dnk",
                    "epk",
                    "ghkl",
                    "ghmp",
                    "ndk",
                    "pfka",
                    "pfkb",
                ],
            )

    def test_build_learned_retrieval_manifest_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            geometry = root / "geometry.json"
            retrieval = root / "retrieval.json"
            labels = root / "labels.json"
            out = root / "manifest.json"
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {"artifact": "active_site_geometry_features"},
                        "entries": [
                            {
                                "entry_id": "m_csa:1",
                                "entry_name": "labeled hydrolase",
                                "status": "ok",
                                "pdb_id": "1ABC",
                                "resolved_residue_count": 3,
                                "residues": [
                                    {"code": "Ser"},
                                    {"code": "His"},
                                    {"code": "Asp"},
                                ],
                                "pairwise_distances_angstrom": [{}, {}, {}],
                                "ligand_context": {"cofactor_families": ["metal"]},
                                "pocket_context": {
                                    "descriptors": {"polar_fraction": 0.2}
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            retrieval.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "geometry_aware_seed_fingerprint_retrieval"
                        },
                        "results": [
                            {
                                "entry_id": "m_csa:1",
                                "status": "ok",
                                "top_fingerprints": [
                                    {
                                        "fingerprint_id": "ser_his_acid_hydrolase",
                                        "score": 0.7,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "m_csa:1",
                            "fingerprint_id": "ser_his_acid_hydrolase",
                            "label_type": "seed_fingerprint",
                            "confidence": "high",
                            "rationale": "Curated test label with enough rationale.",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "evidence_score": 0.85,
                            "evidence": {"sources": ["test"]},
                        }
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-learned-retrieval-manifest",
                    "--geometry",
                    str(geometry),
                    "--retrieval",
                    str(retrieval),
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
            manifest = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(manifest["metadata"]["eligible_entry_count"], 1)
            self.assertTrue(manifest["rows"][0]["countable_training_label"])

    def test_audit_sequence_similarity_failure_sets_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            clusters = root / "clusters.json"
            labels = root / "labels.json"
            queue = root / "queue.json"
            out = root / "sequence_failures.json"
            clusters.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "cluster_source": "reference_uniprot_exact_set",
                            "cluster_count": 1,
                        },
                        "clusters": [
                            {
                                "sequence_cluster_id": "uniprot:P12345",
                                "entry_ids": ["m_csa:1", "m_csa:2"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "m_csa:1",
                            "fingerprint_id": "ser_his_acid_hydrolase",
                            "label_type": "seed_fingerprint",
                            "confidence": "high",
                            "rationale": "Curated test label with enough rationale.",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "evidence_score": 0.85,
                            "evidence": {"sources": ["test"]},
                        },
                        {
                            "entry_id": "m_csa:2",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "confidence": "medium",
                            "rationale": "Curated test label with enough rationale.",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "evidence_score": 0.65,
                            "evidence": {"sources": ["test"]},
                        },
                    ]
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:2",
                                "recommended_action": "expert_label_decision_needed",
                                "top1_ontology_family": "hydrolysis",
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
                    "audit-sequence-similarity-failure-sets",
                    "--sequence-clusters",
                    str(clusters),
                    "--labels",
                    str(labels),
                    "--active-learning-queue",
                    str(queue),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(audit["metadata"]["duplicate_cluster_count"], 1)
            self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)

    def test_check_label_preview_promotion_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            acceptance = root / "acceptance.json"
            summary = root / "summary.json"
            preview_debt = root / "preview_debt.json"
            current_debt = root / "current_debt.json"
            out = root / "readiness.json"
            acceptance.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "accepted_for_counting": True,
                            "accepted_new_label_count": 18,
                            "countable_label_count": 636,
                            "pending_review_count": 44,
                            "hard_negative_count": 0,
                            "near_miss_count": 0,
                            "out_of_scope_false_non_abstentions": 0,
                            "actionable_in_scope_failure_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            summary.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "blocker_count": 0,
                            "latest_countable_label_count": 636,
                            "total_accepted_new_label_count": 18,
                            "all_active_queues_retain_unlabeled_candidates": True,
                        }
                    }
                ),
                encoding="utf-8",
            )
            preview_debt.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_summary",
                            "review_debt_count": 61,
                            "needs_more_evidence_count": 44,
                            "new_review_debt_count": 1,
                            "new_review_debt_entry_ids": ["m_csa:650"],
                            "recommended_next_action_counts_by_debt_status": {
                                "new": {"verify_local_cofactor_or_active_site_mapping": 1}
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            current_debt.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_summary",
                            "review_debt_count": 53,
                            "needs_more_evidence_count": 37,
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
                    "check-label-preview-promotion",
                    "--preview-acceptance",
                    str(acceptance),
                    "--preview-summary",
                    str(summary),
                    "--preview-review-debt",
                    str(preview_debt),
                    "--current-review-debt",
                    str(current_debt),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            readiness = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(readiness["metadata"]["promotion_recommendation"], "review_before_promoting")
            self.assertEqual(readiness["metadata"]["preview_new_review_debt_count"], 1)
            self.assertEqual(readiness["metadata"]["preview_new_review_debt_entry_ids"], ["m_csa:650"])
            self.assertEqual(
                readiness["metadata"]["preview_new_review_debt_next_action_counts"],
                {"verify_local_cofactor_or_active_site_mapping": 1},
            )

    def test_audit_label_scaling_quality_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            acceptance = root / "acceptance.json"
            readiness = root / "readiness.json"
            debt = root / "debt.json"
            gaps = root / "gaps.json"
            queue = root / "queue.json"
            guardrails = root / "guardrails.json"
            hard = root / "hard.json"
            decision = root / "decision.json"
            mapping = root / "mapping.json"
            sequence_clusters = root / "sequence_clusters.json"
            alternate_scan = root / "alternate_scan.json"
            remap_local_audit = root / "remap_local_audit.json"
            reaction_mismatch_audit = root / "reaction_mismatch_audit.json"
            expert_label_export = root / "expert_label_export.json"
            expert_label_repair = root / "expert_label_repair.json"
            expert_label_repair_guardrail = root / "expert_label_repair_guardrail.json"
            expert_label_local_gap = root / "expert_label_local_gap.json"
            expert_label_local_export = root / "expert_label_local_export.json"
            out = root / "audit.json"
            acceptance.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "label_batch_acceptance_check",
                            "out_of_scope_false_non_abstentions": 0,
                            "actionable_in_scope_failure_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            readiness.write_text(
                json.dumps({"metadata": {"promotion_recommendation": "review_before_promoting"}}),
                encoding="utf-8",
            )
            debt.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_summary",
                            "new_review_debt_entry_ids": ["m_csa:651", "m_csa:652"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            gaps.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "review_evidence_gap_analysis"},
                        "rows": [
                            {
                                "entry_id": "m_csa:651",
                                "entry_name": "accepted debt",
                                "decision_action": "accept_label",
                                "coverage_status": "expected_absent_from_structure",
                                "gap_reasons": ["top1_below_abstention_threshold"],
                                "counterevidence_reasons": ["absent_heme_context"],
                                "target_fingerprint_id": "heme_peroxidase_oxidase",
                                "top1_fingerprint_id": "heme_peroxidase_oxidase",
                                "mechanism_text_snippets": ["Hydrolysis text without heme evidence."],
                            },
                            {
                                "entry_id": "m_csa:652",
                                "entry_name": "decision-only PLP review",
                                "decision_action": "mark_needs_more_evidence",
                                "coverage_status": "all_expected_local",
                                "gap_reasons": ["review_marked_needs_more_evidence"],
                                "counterevidence_reasons": [],
                                "target_fingerprint_id": "plp_dependent_enzyme",
                                "top1_fingerprint_id": "plp_dependent_enzyme",
                                "mechanism_text_snippets": [
                                    "PLP support is local, but external review is still required."
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            queue.write_text(
                json.dumps(
                    {
                        "metadata": {"all_unlabeled_rows_retained": True},
                        "rows": [
                            {
                                "entry_id": "m_csa:650",
                                "recommended_action": "expert_label_decision_needed",
                                "top1_ontology_family": "hydrolysis",
                            },
                            {
                                "entry_id": "m_csa:651",
                                "top1_ontology_family": "heme_redox",
                            },
                            {
                                "entry_id": "m_csa:652",
                                "top1_ontology_family": "plp_chemistry",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            guardrails.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "family_propagation_guardrail_audit",
                            "blocker_counts": {},
                        },
                        "rows": [],
                    }
                ),
                encoding="utf-8",
            )
            hard.write_text(
                json.dumps({"metadata": {"hard_negative_count": 0, "near_miss_count": 0}}),
                encoding="utf-8",
            )
            decision.write_text(
                json.dumps(
                    {
                        "review_items": [
                            {"entry_id": "m_csa:651", "decision": {"action": "accept_label"}}
                        ]
                    }
                ),
                encoding="utf-8",
            )
            mapping.write_text(
                json.dumps({"metadata": {"issue_count": 0}, "rows": []}),
                encoding="utf-8",
            )
            sequence_clusters.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:651",
                                "sequence_cluster_id": "cluster-cli",
                            },
                            {
                                "entry_id": "m_csa:652",
                                "sequence_cluster_id": "cluster-cli-2",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            alternate_scan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_alternate_structure_scan",
                            "expected_family_hit_entry_ids": ["m_csa:651"],
                            "structure_wide_hit_without_local_support_entry_ids": [
                                "m_csa:651"
                            ],
                            "fetch_failure_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            remap_local_audit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "review_debt_remap_local_lead_audit",
                            "countable_label_candidate_count": 0,
                            "strict_remap_guardrail_entry_ids": ["m_csa:651"],
                            "expert_family_boundary_review_entry_ids": [],
                            "local_structure_selection_rule_candidate_entry_ids": [
                                "m_csa:651"
                            ],
                        }
                    }
                ),
                encoding="utf-8",
            )
            reaction_mismatch_audit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "reaction_substrate_mismatch_audit",
                            "mismatch_count": 1,
                            "mismatch_entry_ids": ["m_csa:651"],
                            "mismatch_reason_counts": {
                                "kinase_name_with_hydrolase_top1": 1
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            expert_label_export.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_review_export",
                            "exported_count": 1,
                            "exported_entry_ids": ["m_csa:650"],
                            "countable_label_candidate_count": 0,
                            "decision_counts": {"no_decision": 1},
                            "export_ready": True,
                        },
                        "review_items": [{"entry_id": "m_csa:650"}],
                    }
                ),
                encoding="utf-8",
            )
            expert_label_repair.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_repair_candidate_summary",
                            "candidate_count": 1,
                            "candidate_entry_ids": ["m_csa:650"],
                            "countable_label_candidate_count": 0,
                        },
                        "rows": [{"entry_id": "m_csa:650"}],
                    }
                ),
                encoding="utf-8",
            )
            expert_label_repair_guardrail.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_repair_guardrail_audit",
                            "guardrail_ready": True,
                            "all_priority_lanes_non_countable": True,
                            "priority_repair_row_count": 1,
                            "countable_label_candidate_count": 0,
                        },
                        "rows": [{"entry_id": "m_csa:650"}],
                    }
                ),
                encoding="utf-8",
            )
            expert_label_local_gap.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_local_evidence_gap_audit",
                            "audit_ready": True,
                            "priority_rows_accounted_for": True,
                            "priority_repair_row_count": 1,
                            "audited_entry_count": 1,
                            "missing_priority_entry_ids": [],
                            "countable_label_candidate_count": 0,
                            "local_evidence_gap_class_counts": {
                                "selected_structure_residue_support_shortfall": 1
                            },
                        },
                        "rows": [{"entry_id": "m_csa:650"}],
                    }
                ),
                encoding="utf-8",
            )
            expert_label_local_export.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "expert_label_decision_local_evidence_review_export",
                            "export_ready": True,
                            "all_source_rows_exported": True,
                            "exported_count": 1,
                            "countable_label_candidate_count": 0,
                            "decision_counts": {"no_decision": 1},
                        },
                        "review_items": [{"entry_id": "m_csa:650"}],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-label-scaling-quality",
                    "--batch-id",
                    "test_preview",
                    "--acceptance",
                    str(acceptance),
                    "--readiness",
                    str(readiness),
                    "--review-debt",
                    str(debt),
                    "--review-evidence-gaps",
                    str(gaps),
                    "--active-learning-queue",
                    str(queue),
                    "--family-propagation-guardrails",
                    str(guardrails),
                    "--hard-negatives",
                    str(hard),
                    "--decision-batch",
                    str(decision),
                    "--structure-mapping",
                    str(mapping),
                    "--sequence-clusters",
                    str(sequence_clusters),
                    "--alternate-structure-scan",
                    str(alternate_scan),
                    "--remap-local-lead-audit",
                    str(remap_local_audit),
                    "--reaction-substrate-mismatch-audit",
                    str(reaction_mismatch_audit),
                    "--expert-label-decision-review-export",
                    str(expert_label_export),
                    "--expert-label-decision-repair-candidates",
                    str(expert_label_repair),
                    "--expert-label-decision-repair-guardrail-audit",
                    str(expert_label_repair_guardrail),
                    "--expert-label-decision-local-evidence-gap-audit",
                    str(expert_label_local_gap),
                    "--expert-label-decision-local-evidence-review-export",
                    str(expert_label_local_export),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(audit["metadata"]["batch_id"], "test_preview")
            self.assertEqual(audit["metadata"]["accepted_new_debt_entry_ids"], ["m_csa:651"])
            self.assertEqual(audit["metadata"]["unclassified_new_review_debt_entry_ids"], [])
            self.assertEqual(
                audit["metadata"]["issue_class_counts"]["expert_review_decision_needed"],
                1,
            )
            self.assertIn("accepted_new_labels_without_review_debt", audit["blockers"])
            self.assertEqual(
                audit["metadata"]["near_duplicate_audit_status"],
                "not_observed_in_sequence_cluster_artifact",
            )
            self.assertTrue(audit["metadata"]["alternate_structure_scan_present"])
            self.assertTrue(audit["metadata"]["remap_local_lead_audit_present"])
            self.assertTrue(
                audit["metadata"]["reaction_substrate_mismatch_audit_present"]
            )
            self.assertTrue(
                audit["gates"][
                    "expert_label_decision_repair_candidates_cover_review_only_lanes"
                ]
            )
            self.assertTrue(
                audit["gates"]["expert_label_decision_local_evidence_gaps_audited"]
            )
            self.assertTrue(
                audit["gates"][
                    "expert_label_decision_local_evidence_review_export_ready"
                ]
            )
            self.assertEqual(
                audit["metadata"][
                    "expert_label_decision_repair_candidates_missing_entry_ids"
                ],
                [],
            )
            self.assertTrue(
                audit["metadata"][
                    "expert_label_decision_local_evidence_gap_audit_present"
                ]
            )
            self.assertTrue(
                audit["metadata"][
                    "expert_label_decision_local_evidence_review_export_present"
                ]
            )
            self.assertIn("alternate_structure_hits_lack_local_support", audit["review_warnings"])
            self.assertIn("remap_local_leads_require_strict_guardrail", audit["review_warnings"])
            self.assertIn("reaction_substrate_mismatch_audit_hits", audit["review_warnings"])

    def test_automation_lock_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_dir = Path(tmpdir) / "run.lock"
            env = {"PYTHONPATH": str(ROOT / "src")}
            acquire = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "acquire",
                    "--started-at",
                    "2026-05-10T00:00:00Z",
                    "--skip-worktree-check",
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            acquired = json.loads(acquire.stdout)
            self.assertTrue(acquired["acquired"])
            self.assertEqual(acquired["status"], "acquired")
            self.assertTrue((lock_dir / "pid").exists())
            blocked = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "acquire",
                    "--started-at",
                    "2026-05-10T00:01:00Z",
                    "--skip-worktree-check",
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(blocked.returncode, 3)
            self.assertEqual(json.loads(blocked.stdout)["status"], "active_lock_present")
            status = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "status",
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(json.loads(status.stdout)["status"], "active_lock_present")
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "release",
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse(lock_dir.exists())

    def test_automation_lock_release_can_require_clean_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True, text=True)
            lock_dir = Path(tmpdir) / "run.lock"
            env = {"PYTHONPATH": str(ROOT / "src")}
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "--repo-root",
                    str(repo),
                    "acquire",
                    "--started-at",
                    "2026-05-10T00:00:00Z",
                    "--skip-worktree-check",
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")
            blocked = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "--repo-root",
                    str(repo),
                    "release",
                    "--require-clean",
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(blocked.returncode, 4)
            self.assertIn("worktree_dirty", json.loads(blocked.stdout)["blockers"])
            self.assertTrue(lock_dir.exists())
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "automation-lock",
                    "--lock-dir",
                    str(lock_dir),
                    "--repo-root",
                    str(repo),
                    "release",
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse(lock_dir.exists())

    def test_artifact_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger = Path(tmpdir) / "source_ledger.json"
            demo = Path(tmpdir) / "mechanism_demo.json"
            score_margins = Path(tmpdir) / "score_margins.json"
            hard_negatives = Path(tmpdir) / "hard_negatives.json"
            in_scope_failures = Path(tmpdir) / "in_scope_failures.json"
            cofactor_coverage = Path(tmpdir) / "cofactor_coverage.json"
            cofactor_policy = Path(tmpdir) / "cofactor_policy.json"
            seed_family_performance = Path(tmpdir) / "seed_family_performance.json"
            label_candidates = Path(tmpdir) / "label_candidates.json"
            label_factory = Path(tmpdir) / "label_factory.json"
            applied_factory = Path(tmpdir) / "applied_factory.json"
            active_queue = Path(tmpdir) / "active_queue.json"
            adversarial_negatives = Path(tmpdir) / "adversarial_negatives.json"
            review_export = Path(tmpdir) / "review_export.json"
            decision_batch = Path(tmpdir) / "decision_batch.json"
            imported_labels = Path(tmpdir) / "imported_labels.json"
            countable_labels = Path(tmpdir) / "countable_labels.json"
            gate_check = Path(tmpdir) / "gate_check.json"
            review_resolution = Path(tmpdir) / "review_resolution.json"
            review_gaps = Path(tmpdir) / "review_gaps.json"
            family_guardrails = Path(tmpdir) / "family_guardrails.json"
            migrated_labels = Path(tmpdir) / "migrated_labels.json"
            mapping_issues = Path(tmpdir) / "mapping_issues.json"
            calibration = Path(tmpdir) / "calibration.json"
            slice_summary = Path(tmpdir) / "slice_summary.json"
            subprocess.run(
                [sys.executable, "-m", "catalytic_earth.cli", "build-ledger", "--out", str(ledger)],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [sys.executable, "-m", "catalytic_earth.cli", "fingerprint-demo", "--out", str(demo)],
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
                    "analyze-geometry-score-margins",
                    "--out",
                    str(score_margins),
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
                    "analyze-seed-family-performance",
                    "--out",
                    str(seed_family_performance),
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
                    "analyze-cofactor-policy",
                    "--out",
                    str(cofactor_policy),
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
                    "analyze-cofactor-coverage",
                    "--out",
                    str(cofactor_coverage),
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
                    "build-hard-negative-controls",
                    "--out",
                    str(hard_negatives),
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
                    "analyze-in-scope-failures",
                    "--out",
                    str(in_scope_failures),
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
                    "build-label-expansion-candidates",
                    "--out",
                    str(label_candidates),
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
                    "migrate-label-registry",
                    "--out",
                    str(migrated_labels),
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
                    "build-label-factory-audit",
                    "--out",
                    str(label_factory),
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
                    "apply-label-factory-actions",
                    "--label-factory-audit",
                    str(label_factory),
                    "--out",
                    str(applied_factory),
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
                    "build-active-learning-queue",
                    "--label-factory-audit",
                    str(label_factory),
                    "--out",
                    str(active_queue),
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
                    "export-label-review",
                    "--queue",
                    str(active_queue),
                    "--out",
                    str(review_export),
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
                    "build-review-decision-batch",
                    "--review",
                    str(review_export),
                    "--batch-id",
                    "test_batch",
                    "--out",
                    str(decision_batch),
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
                    "analyze-review-evidence-gaps",
                    "--review",
                    str(decision_batch),
                    "--out",
                    str(review_gaps),
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
                    "build-adversarial-negatives",
                    "--out",
                    str(adversarial_negatives),
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
                    "build-family-propagation-guardrails",
                    "--out",
                    str(family_guardrails),
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
                    "check-label-factory-gates",
                    "--label-factory-audit",
                    str(label_factory),
                    "--applied-label-factory",
                    str(applied_factory),
                    "--active-learning-queue",
                    str(active_queue),
                    "--adversarial-negatives",
                    str(adversarial_negatives),
                    "--expert-review-export",
                    str(review_export),
                    "--family-propagation-guardrails",
                    str(family_guardrails),
                    "--out",
                    str(gate_check),
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
                    "import-label-review",
                    "--review",
                    str(decision_batch),
                    "--out",
                    str(imported_labels),
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
                    "import-countable-label-review",
                    "--review",
                    str(decision_batch),
                    "--out",
                    str(countable_labels),
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
                    "check-label-review-resolution",
                    "--baseline-label-count",
                    "499",
                    "--review",
                    str(decision_batch),
                    "--review-state-labels",
                    str(imported_labels),
                    "--countable-labels",
                    str(countable_labels),
                    "--label-expansion-candidates",
                    str(label_candidates),
                    "--label-factory-gate",
                    str(gate_check),
                    "--out",
                    str(review_resolution),
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
                    "analyze-structure-mapping-issues",
                    "--out",
                    str(mapping_issues),
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
                    "summarize-geometry-slices",
                    "--artifact-dir",
                    "artifacts",
                    "--out",
                    str(slice_summary),
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
                    "calibrate-abstention",
                    "--out",
                    str(calibration),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(ledger.exists())
            self.assertTrue(demo.exists())
            self.assertIn("score_separation_gap", json.loads(score_margins.read_text())["metadata"])
            self.assertIn("hard_negative_count", json.loads(hard_negatives.read_text())["metadata"])
            self.assertIn(
                "target_fingerprint_counts",
                json.loads(in_scope_failures.read_text())["metadata"],
            )
            self.assertIn(
                "coverage_status_counts",
                json.loads(cofactor_coverage.read_text())["metadata"],
            )
            self.assertIn(
                "recommendation",
                json.loads(cofactor_policy.read_text())["metadata"],
            )
            self.assertIn(
                "in_scope_family_count",
                json.loads(seed_family_performance.read_text())["metadata"],
            )
            self.assertIn(
                "ready_for_label_review_count",
                json.loads(label_candidates.read_text())["metadata"],
            )
            self.assertIn("tier", json.loads(migrated_labels.read_text())[0])
            self.assertIn("promote_to_silver_count", json.loads(label_factory.read_text())["metadata"])
            self.assertIn("output_summary", json.loads(applied_factory.read_text())["metadata"])
            self.assertIn("ranking_terms", json.loads(active_queue.read_text())["metadata"])
            self.assertIn("axis_counts", json.loads(adversarial_negatives.read_text())["metadata"])
            self.assertIn("decision_schema", json.loads(review_export.read_text())["metadata"])
            self.assertIn("decision_counts", json.loads(decision_batch.read_text())["metadata"])
            self.assertIn("automation_ready_for_next_label_batch", json.loads(gate_check.read_text())["metadata"])
            self.assertIn("resolved_for_scaling", json.loads(review_resolution.read_text())["metadata"])
            self.assertIn("gap_reason_counts", json.loads(review_gaps.read_text())["metadata"])
            self.assertIn("source_guardrails", json.loads(family_guardrails.read_text())["metadata"])
            self.assertGreaterEqual(len(json.loads(imported_labels.read_text())), 475)
            self.assertLessEqual(len(json.loads(countable_labels.read_text())), len(json.loads(imported_labels.read_text())))
            self.assertIn("status_counts", json.loads(mapping_issues.read_text())["metadata"])
            self.assertEqual(json.loads(slice_summary.read_text())["metadata"]["largest_slice"], "1000")
            self.assertGreater(json.loads(calibration.read_text())["metadata"]["threshold_count"], 21)


if __name__ == "__main__":
    unittest.main()
