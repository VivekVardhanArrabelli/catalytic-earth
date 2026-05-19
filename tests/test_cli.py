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

    def test_label_factory_gate_cli_lineage_rejects_payload_slice_mismatch(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            required = {
                "label_factory_audit": str(root / "v3_label_factory_audit_1000.json"),
                "applied_label_factory": str(
                    root / "v3_label_factory_applied_labels_1000.json"
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
            loaded_artifacts = {
                field_name: {
                    "metadata": {
                        "method": field_name,
                        "slice_id": 1000,
                    }
                }
                for field_name in required
            }
            loaded_artifacts["active_learning_queue"]["metadata"]["slice_id"] = 975

            with self.assertRaisesRegex(
                ValueError,
                "payload slice id 975 conflicts with path slice id 1000",
            ):
                _validate_label_factory_gate_cli_lineage(
                    labels_path=str(root / "curated_mechanism_labels.json"),
                    required_artifacts=required,
                    optional_artifacts={},
                    loaded_artifacts=loaded_artifacts,
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

    def test_external_pilot_success_criteria_cli_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            priority = root / "priority.json"
            review = root / "review.json"
            decisions = root / "decisions.json"
            readiness = root / "readiness.json"
            gate = root / "gate.json"
            out = root / "success.json"
            priority.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_pilot_candidate_priority"
                        },
                        "rows": [
                            {
                                "accession": "P12345",
                                "lane_id": "external_source:lane_a",
                                "pilot_selection_status": "selected_for_review_pilot",
                                "countable_label_candidate": False,
                                "ready_for_label_import": False,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_pilot_review_decision_export"
                        },
                        "review_items": [
                            {
                                "accession": "P12345",
                                "decision": {
                                    "decision_status": "no_decision",
                                    "ready_for_label_import": False,
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            decisions.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "external_source_pilot_active_site_evidence_decisions"
                            )
                        },
                        "rows": [
                            {
                                "accession": "P12345",
                                "rank": 1,
                                "active_site_evidence_source_category": (
                                    "explicit_active_site_source_present"
                                ),
                                "broader_duplicate_screening_status": (
                                    "broader_duplicate_screening_required"
                                ),
                                "representation_control_status": (
                                    "pilot_representation_control_review_only"
                                ),
                                "countable_label_candidate": False,
                                "ready_for_label_import": False,
                                "import_readiness_blockers": [
                                    "broader_duplicate_screening_required",
                                    "external_review_decision_artifact_not_built",
                                    "full_label_factory_gate_not_run",
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            readiness.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_import_readiness_audit"
                        },
                        "rows": [],
                    }
                ),
                encoding="utf-8",
            )
            gate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_transfer_gate_check",
                            "gate_count": 68,
                            "passed_gate_count": 68,
                            "ready_for_label_import": False,
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
                    "build-external-source-pilot-success-criteria",
                    "--pilot-candidate-priority",
                    str(priority),
                    "--pilot-review-decision-export",
                    str(review),
                    "--pilot-active-site-evidence-decisions",
                    str(decisions),
                    "--external-import-readiness-audit",
                    str(readiness),
                    "--external-transfer-gate",
                    str(gate),
                    "--max-rows",
                    "1",
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
            self.assertEqual(
                payload["metadata"]["method"],
                "external_source_pilot_success_criteria",
            )
            self.assertEqual(payload["metadata"]["pilot_status"], "needs_more_work")
            self.assertEqual(payload["metadata"]["terminal_decision_count"], 0)
            self.assertEqual(payload["metadata"]["import_ready_row_count"], 0)

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

    def test_build_epk_positive_fingerprint_readiness_packet_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            atp_expansion = root / "atp_expansion.json"
            decision_batch = root / "mismatch_decisions.json"
            reaudit_policy = root / "reaudit_policy.json"
            out = root / "epk_readiness.json"
            epk_rows = [
                (
                    "m_csa:35",
                    "phosphorylase kinase",
                    "Asp149 deprotonates the protein substrate hydroxyl group before attack on the gamma-phosphate of ATP.",
                ),
                (
                    "m_csa:246",
                    "receptor protein-tyrosine kinase",
                    "A tyrosine hydroxyl attacks the gamma phosphate of ATP with Mg2+ phosphate positioning.",
                ),
                (
                    "m_csa:640",
                    "kanamycin kinase",
                    "A substrate hydroxyl attacks ATP gamma phosphate during aminoglycoside phosphorylation.",
                ),
            ]
            atp_expansion.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "atp_phosphoryl_transfer_family_expansion"
                        },
                        "rows": [
                            {
                                "entry_id": entry_id,
                                "entry_name": entry_name,
                                "family_id": "epk",
                                "support_level": (
                                    "expert_review_supported_family_boundary"
                                ),
                                "decision_action": "reject_label",
                                "decision_label_type": "out_of_scope",
                                "decision_review_status": "expert_reviewed",
                                "reaction_substrate_resolution": (
                                    "confirm_current_label_or_out_of_scope"
                                ),
                                "reviewer": "test_reviewer",
                                "top1_fingerprint_id": "metal_dependent_hydrolase",
                                "top1_ontology_family": "hydrolysis",
                                "mismatch_reasons": [
                                    "kinase_name_with_hydrolase_top1"
                                ],
                                "propagation_blockers": [
                                    "reaction_substrate_mismatch"
                                ],
                                "countable_label_candidate": False,
                            }
                            for entry_id, entry_name, _snippet in epk_rows
                        ],
                    }
                ),
                encoding="utf-8",
            )
            decision_batch.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "provisional_label_review_decision_batch"
                        },
                        "review_items": [
                            {
                                "entry_id": entry_id,
                                "entry_name": entry_name,
                                "mismatch_context": {
                                    "entry_id": entry_id,
                                    "entry_name": entry_name,
                                    "top1_fingerprint_id": (
                                        "metal_dependent_hydrolase"
                                    ),
                                    "top1_ontology_family": "hydrolysis",
                                    "mechanism_text_snippets": [snippet],
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
                                    "future_fingerprint_family_hint": "ePK",
                                    "rationale": (
                                        f"{entry_name} is ePK-like ATP "
                                        "gamma-phosphoryl transfer to a "
                                        "hydroxyl acceptor."
                                    ),
                                },
                            }
                            for entry_id, entry_name, snippet in epk_rows
                        ],
                    }
                ),
                encoding="utf-8",
            )
            reaudit_policy.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "external_hard_negative_ontology_reaudit_policy"
                            )
                        },
                        "expansion_triggers": [
                            "epk",
                            "any_positive_fingerprint_universe_expansion",
                        ],
                        "external_labels_requiring_reaudit": [
                            {"entry_id": "uniprot:P06744"}
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
                    "build-epk-positive-fingerprint-readiness-packet",
                    "--atp-phosphoryl-transfer-family-expansion",
                    str(atp_expansion),
                    "--reaction-substrate-mismatch-decision-batch",
                    str(decision_batch),
                    "--external-hard-negative-ontology-reaudit-policy",
                    str(reaudit_policy),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            packet = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(
                packet["metadata"]["evidence_ready_for_draft_fingerprint_spec"]
            )
            self.assertFalse(
                packet["metadata"]["ready_to_expand_positive_fingerprint_universe"]
            )
            self.assertEqual(packet["metadata"]["current_positive_fingerprint_count"], 8)
            self.assertEqual(packet["metadata"]["epk_boundary_row_count"], 3)
            self.assertEqual(packet["metadata"]["countable_label_candidate_count"], 0)
            self.assertIn(
                "external_hard_negative_reaudit_required_before_positive_expansion_counts",
                packet["metadata"]["expansion_blockers"],
            )

    def test_build_epk_external_hard_negative_reaudit_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            epk_readiness = root / "epk_readiness.json"
            reaudit_policy = root / "reaudit_policy.json"
            labels = root / "labels.json"
            out = root / "reaudit_plan.json"
            epk_readiness.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_positive_fingerprint_readiness_packet",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "readiness_status": (
                                "draft_fingerprint_spec_ready_not_countable"
                            ),
                            "evidence_ready_for_draft_fingerprint_spec": True,
                            "ready_to_expand_positive_fingerprint_universe": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            reaudit_policy.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "external_hard_negative_ontology_reaudit_policy"
                            )
                        },
                        "expansion_triggers": ["epk"],
                        "external_labels_requiring_reaudit": [
                            {"entry_id": "uniprot:P06744"}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            labels.write_text(
                json.dumps(
                    [
                        {
                            "entry_id": "uniprot:P06744",
                            "fingerprint_id": None,
                            "label_type": "out_of_scope",
                            "tier": "bronze",
                            "review_status": "automation_curated",
                            "ontology_version_at_decision": "label_factory_v1_8fp",
                            "confidence": "medium",
                            "evidence_score": 0.65,
                            "rationale": (
                                "External hard-negative label retained for "
                                "the current ontology version only."
                            ),
                            "evidence": {
                                "predictive_evidence": ["scored local surface"],
                                "import_gate_evidence": ["factory gate passed"],
                                "review_only_context": ["source context"],
                                "excluded_context": ["annotation prose"],
                            },
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
                    "build-epk-external-hard-negative-reaudit-plan",
                    "--epk-positive-fingerprint-readiness-packet",
                    str(epk_readiness),
                    "--external-hard-negative-ontology-reaudit-policy",
                    str(reaudit_policy),
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
            plan = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(plan["metadata"]["reaudit_plan_ready"])
            self.assertFalse(plan["metadata"]["ready_to_run_scored_reaudit"])
            self.assertFalse(
                plan["metadata"]["ready_to_expand_positive_fingerprint_universe"]
            )
            self.assertEqual(plan["metadata"]["external_label_reaudit_row_count"], 1)
            self.assertEqual(plan["metadata"]["countable_label_candidate_count"], 0)

    def test_build_epk_draft_fingerprint_spec_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            epk_readiness = root / "epk_readiness.json"
            reaudit_plan = root / "reaudit_plan.json"
            out = root / "epk_draft_spec.json"
            epk_readiness.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_positive_fingerprint_readiness_packet",
                            "target_parent_family_id": "atp_phosphoryl_transfer",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "readiness_status": (
                                "draft_fingerprint_spec_ready_not_countable"
                            ),
                            "evidence_ready_for_draft_fingerprint_spec": True,
                            "ready_to_expand_positive_fingerprint_universe": False,
                            "current_positive_fingerprint_ids": [
                                "ser_his_acid_hydrolase",
                                "metal_dependent_hydrolase",
                                "plp_dependent_enzyme",
                                "radical_sam_enzyme",
                                "cobalamin_radical_rearrangement",
                                "flavin_monooxygenase",
                                "flavin_dehydrogenase_reductase",
                                "heme_peroxidase_oxidase",
                            ],
                        },
                        "target_fingerprint_draft": {
                            "id": "epk_atp_gamma_phosphoryl_transfer",
                            "name": "ePK/ePK-like ATP gamma-phosphoryl transfer",
                            "family_id": "epk",
                            "parent_family_id": "atp_phosphoryl_transfer",
                            "cofactors": ["ATP", "Mg2+"],
                        },
                        "rows": [
                            {
                                "entry_id": entry_id,
                                "entry_name": name,
                                "family_id": "epk",
                                "source_family_support_level": (
                                    "expert_review_supported_family_boundary"
                                ),
                                "expert_supported_family_boundary": True,
                                "active_site_base_evidence_status": (
                                    "review_text_support"
                                ),
                                "cofactor_evidence_status": (
                                    "review_text_mg_atp_context"
                                ),
                                "reaction_center_evidence_status": (
                                    "review_text_atp_gamma_phosphoryl_transfer"
                                ),
                                "acceptor_scope_evidence_status": (
                                    "review_text_hydroxyl_acceptor"
                                ),
                                "current_top1_fingerprint_id": (
                                    "metal_dependent_hydrolase"
                                ),
                                "current_top1_score": 0.3,
                                "readiness_blockers": [
                                    "positive_fingerprint_registry_not_expanded"
                                ],
                                "review_only": True,
                                "countable_label_candidate": False,
                            }
                            for entry_id, name in [
                                ("m_csa:35", "phosphorylase kinase"),
                                ("m_csa:246", "receptor protein-tyrosine kinase"),
                                ("m_csa:282", "MAP kinase kinase"),
                            ]
                        ],
                    }
                ),
                encoding="utf-8",
            )
            reaudit_plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_external_hard_negative_reaudit_plan",
                            "reaudit_plan_ready": True,
                            "ready_to_run_scored_reaudit": False,
                            "scored_reaudit_blockers": [
                                "epk_positive_scoring_rule_not_implemented"
                            ],
                        },
                        "rows": [
                            {
                                "entry_id": entry_id,
                                "reaudit_status": "planned_not_scored",
                                "current_label_contract_valid": True,
                                "evidence_separation_valid": True,
                                "review_only": True,
                                "countable_label_candidate": False,
                            }
                            for entry_id in [
                                "uniprot:P06744",
                                "uniprot:P78549",
                                "uniprot:Q3LXA3",
                            ]
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
                    "build-epk-draft-fingerprint-spec",
                    "--epk-positive-fingerprint-readiness-packet",
                    str(epk_readiness),
                    "--epk-external-hard-negative-reaudit-plan",
                    str(reaudit_plan),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            spec = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(
                spec["metadata"]["draft_spec_ready_for_scorer_prototype"]
            )
            self.assertFalse(
                spec["metadata"]["ready_to_expand_positive_fingerprint_universe"]
            )
            self.assertFalse(spec["metadata"]["fingerprint_registry_edited"])
            self.assertEqual(spec["metadata"]["countable_label_candidate_count"], 0)
            self.assertEqual(spec["metadata"]["current_positive_fingerprint_count"], 8)
            self.assertEqual(spec["metadata"]["external_reaudit_row_count"], 3)
            self.assertEqual(
                spec["external_hard_negative_reaudit_summary"]["reaudit_status"],
                "planned_not_scored",
            )
            self.assertIn(
                "M-CSA mechanism text",
                spec["draft_fingerprint_spec"]["predictive_evidence_exclusions"],
            )

    def test_build_epk_local_evidence_audit_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            draft_spec = root / "epk_draft_spec.json"
            geometry = root / "geometry.json"
            out = root / "epk_local_audit.json"
            draft_spec.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_draft_fingerprint_spec",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "draft_spec_ready_for_scorer_prototype": True,
                        },
                        "boundary_rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                            },
                            {
                                "entry_id": "m_csa:662",
                                "entry_name": "phosphatidylinositol kinase",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "geometry_feature_extraction",
                            "slice_size": 1000,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "status": "ok",
                                "pdb_id": "2PHK",
                                "resolved_residue_count": 3,
                                "ligand_context": {
                                    "ligand_codes": ["ATP", "MG"],
                                    "structure_ligand_codes": ["ATP", "MG"],
                                },
                                "residues": [
                                    {
                                        "code": "Asp",
                                        "resid": 149,
                                        "chain_name": "A",
                                        "roles": ["proton acceptor"],
                                    }
                                ],
                            },
                            {
                                "entry_id": "m_csa:662",
                                "status": "ok",
                                "pdb_id": "1BO1",
                                "resolved_residue_count": 2,
                                "ligand_context": {
                                    "ligand_codes": [],
                                    "structure_ligand_codes": [],
                                },
                                "residues": [
                                    {
                                        "code": "Asp",
                                        "resid": 278,
                                        "chain_name": "A",
                                        "roles": ["proton shuttle"],
                                    }
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
                    "build-epk-local-evidence-audit",
                    "--epk-draft-fingerprint-spec",
                    str(draft_spec),
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
            audit = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(audit["metadata"]["method"], "epk_local_evidence_audit")
            self.assertEqual(audit["metadata"]["boundary_row_count"], 2)
            self.assertEqual(
                audit["metadata"]["ready_for_text_free_axis_prototype_count"], 1
            )
            self.assertFalse(audit["metadata"]["ready_to_run_epk_scorer"])
            rows = {row["entry_id"]: row for row in audit["rows"]}
            self.assertEqual(
                rows["m_csa:35"]["scorer_input_readiness"],
                "ready_for_text_free_axis_prototype",
            )
            self.assertEqual(
                rows["m_csa:662"]["scorer_input_readiness"],
                "needs_ligand_source_or_alternate_structure",
            )

    def test_build_epk_text_free_local_axis_prototype_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            audit = root / "epk_local_audit.json"
            out = root / "epk_axis_prototype.json"
            audit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_local_evidence_audit",
                            "audit_status": "local_evidence_profile_ready_not_scored",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "boundary_row_count": 2,
                            "ready_for_text_free_axis_prototype_count": 1,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "pdb_id": "2PHK",
                                "geometry_status": "ok",
                                "scorer_input_readiness": (
                                    "ready_for_text_free_axis_prototype"
                                ),
                                "local_nucleotide_ligand_codes": ["ATP"],
                                "local_metal_ligand_codes": ["MG"],
                                "acid_base_residues": [
                                    {
                                        "code": "Asp",
                                        "resid": 136,
                                        "chain_name": "A",
                                        "roles": ["proton acceptor"],
                                    }
                                ],
                                "audit_blockers": [
                                    "acceptor_axis_still_source_traced_not_geometry_scored",
                                    "no_epk_score_computed",
                                ],
                            },
                            {
                                "entry_id": "m_csa:662",
                                "entry_name": "phosphatidylinositol kinase",
                                "scorer_input_readiness": (
                                    "needs_ligand_source_or_alternate_structure"
                                ),
                                "local_feature_status": "local_ligand_axis_missing",
                                "audit_blockers": [
                                    "local_atp_or_adenine_nucleotide_ligand_missing",
                                    "local_mg_or_metal_ligand_missing",
                                    "no_epk_score_computed",
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
                    "build-epk-text-free-local-axis-prototype",
                    "--epk-local-evidence-audit",
                    str(audit),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            prototype = json.loads(out.read_text(encoding="utf-8"))
            metadata = prototype["metadata"]
            self.assertEqual(metadata["method"], "epk_text_free_local_axis_prototype")
            self.assertEqual(metadata["prototype_ready_row_count"], 1)
            self.assertEqual(metadata["excluded_row_count"], 1)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            self.assertEqual(metadata["countable_label_candidate_count"], 0)
            self.assertEqual(prototype["rows"][0]["axis_presence_count"], 3)
            self.assertFalse(prototype["rows"][0]["epk_score_computed"])
            self.assertIn(
                "external_hard_negative_inverse_axis",
                metadata["blocked_axis_ids"],
            )
            self.assertEqual(
                prototype["excluded_rows"][0]["entry_id"],
                "m_csa:662",
            )

    def test_build_epk_acceptor_geometry_axis_gap_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype_path = root / "epk_axis_prototype.json"
            geometry = root / "geometry.json"
            out = root / "epk_acceptor_plan.json"
            prototype_path.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_text_free_local_axis_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "prototype_ready_row_count": 1,
                            "excluded_row_count": 1,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "pdb_id": "2PHK",
                                "geometry_status": "ok",
                                "axis_presence_count": 3,
                            }
                        ],
                        "excluded_rows": [
                            {
                                "entry_id": "m_csa:662",
                                "entry_name": "phosphatidylinositol kinase",
                                "source_scorer_input_readiness": (
                                    "needs_ligand_source_or_alternate_structure"
                                ),
                                "exclusion_reasons": ["local_ligand_axis_missing"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "active_site_geometry_features",
                            "slice_size": 1000,
                        },
                        "entries": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "status": "ok",
                                "pdb_id": "2PHK",
                                "ligand_context": {
                                    "structure_ligands": [
                                        {
                                            "code": "PTR",
                                            "min_distance_to_active_site": 7.5,
                                            "atom_count": 20,
                                            "instance_count": 1,
                                        }
                                    ]
                                },
                                "pocket_context": {
                                    "distance_cutoff_angstrom": 8.0,
                                    "nearby_residue_sites": [
                                        {
                                            "code": "THR",
                                            "resid": "166",
                                            "chain_name": "A",
                                            "min_distance_to_active_site": 3.2,
                                            "atom_count": 7,
                                        },
                                        {
                                            "code": "ASP",
                                            "resid": "154",
                                            "chain_name": "A",
                                            "min_distance_to_active_site": 4.0,
                                            "atom_count": 8,
                                        },
                                    ],
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
                    "build-epk-acceptor-geometry-axis-gap-plan",
                    "--epk-text-free-local-axis-prototype",
                    str(prototype_path),
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
            metadata = plan["metadata"]
            self.assertEqual(metadata["method"], "epk_acceptor_geometry_axis_gap_plan")
            self.assertEqual(metadata["prototype_ready_row_count"], 1)
            self.assertEqual(metadata["excluded_row_count"], 1)
            self.assertEqual(metadata["rows_with_candidate_acceptor_context_count"], 1)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = plan["rows"][0]
            self.assertEqual(
                row["acceptor_axis_status"],
                "hydroxyl_residue_and_acceptor_ligand_context_present_not_scored",
            )
            self.assertEqual(row["hydroxyl_residue_candidate_count"], 1)
            self.assertEqual(row["acceptor_like_structure_ligand_count"], 1)
            self.assertFalse(row["epk_score_computed"])
            self.assertIn("acceptor_axis_not_thresholded", row["remaining_blockers"])

    def test_build_epk_nonready_ligand_repair_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            audit = root / "epk_local_audit.json"
            geometry = root / "geometry.json"
            out = root / "epk_nonready_repair.json"
            audit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_local_evidence_audit",
                            "audit_status": "local_evidence_profile_ready_not_scored",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "boundary_row_count": 2,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "scorer_input_readiness": (
                                    "ready_for_text_free_axis_prototype"
                                ),
                            },
                            {
                                "entry_id": "m_csa:282",
                                "entry_name": "MAP kinase kinase",
                                "pdb_id": "1S9I",
                                "geometry_status": "ok",
                                "scorer_input_readiness": (
                                    "needs_ligand_distance_or_structure_repair"
                                ),
                                "local_feature_status": (
                                    "structure_ligand_signal_not_local_axis"
                                ),
                                "local_ligand_codes": [],
                                "structure_ligand_codes": ["ATP", "MG"],
                                "audit_blockers": [
                                    "local_atp_or_adenine_nucleotide_ligand_missing",
                                    "local_mg_or_metal_ligand_missing",
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "active_site_geometry_features"},
                        "entries": [
                            {
                                "entry_id": "m_csa:282",
                                "status": "ok",
                                "pdb_id": "1S9I",
                                "ligand_context": {
                                    "structure_ligands": [
                                        {
                                            "code": "ATP",
                                            "min_distance_to_active_site": 14.7,
                                            "atom_count": 62,
                                            "instance_count": 2,
                                        },
                                        {
                                            "code": "MG",
                                            "min_distance_to_active_site": 16.1,
                                            "atom_count": 2,
                                            "instance_count": 2,
                                        },
                                    ]
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
                    "build-epk-nonready-ligand-repair-plan",
                    "--epk-local-evidence-audit",
                    str(audit),
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
            metadata = plan["metadata"]
            self.assertEqual(metadata["method"], "epk_nonready_ligand_repair_plan")
            self.assertEqual(metadata["nonready_row_count"], 1)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = plan["rows"][0]
            self.assertEqual(row["entry_id"], "m_csa:282")
            self.assertEqual(row["repair_lane"], "structure_ligand_signal_not_local_axis")
            self.assertEqual(row["structure_nucleotide_ligand_leads"][0]["code"], "ATP")
            self.assertEqual(row["structure_metal_ligand_leads"][0]["code"], "MG")
            self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_nonready_ligand_alternate_structure_plan_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            repair = root / "repair.json"
            graph = root / "graph.json"
            cif_dir = root / "cif"
            cif_dir.mkdir()
            out = root / "alternate_plan.json"
            repair.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_nonready_ligand_repair_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:282",
                                "entry_name": "MAP kinase kinase",
                                "pdb_id": "1AAA",
                                "repair_lane": "structure_ligand_signal_not_local_axis",
                                "source_scorer_input_readiness": (
                                    "needs_ligand_distance_or_structure_repair"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "v1_graph"},
                        "nodes": [
                            {
                                "id": "m_csa:282",
                                "type": "m_csa_entry",
                                "reference_uniprot_id": "PTEST",
                            },
                            {
                                "id": "m_csa:282:residue:1",
                                "type": "catalytic_residue",
                                "sequence_positions": [
                                    {
                                        "uniprot_id": "PTEST",
                                        "resid": 44,
                                        "code": "Lys",
                                    }
                                ],
                            },
                        ],
                        "edges": [
                            {
                                "source": "m_csa:282",
                                "target": "uniprot:PTEST",
                                "predicate": "has_reference_protein",
                            },
                            {
                                "source": "uniprot:PTEST",
                                "target": "pdb:1AAA",
                                "predicate": "has_structure",
                            },
                            {
                                "source": "uniprot:PTEST",
                                "target": "pdb:1AAB",
                                "predicate": "has_structure",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            for pdb_id in ("1AAA", "1AAB"):
                (cif_dir / f"pdb_{pdb_id}.cif").write_text(
                    "\n".join(
                        [
                            f"data_{pdb_id}",
                            "loop_",
                            "_atom_site.group_PDB",
                            "_atom_site.id",
                            "_atom_site.type_symbol",
                            "_atom_site.label_atom_id",
                            "_atom_site.label_comp_id",
                            "_atom_site.label_asym_id",
                            "_atom_site.label_seq_id",
                            "_atom_site.Cartn_x",
                            "_atom_site.Cartn_y",
                            "_atom_site.Cartn_z",
                            "_atom_site.auth_atom_id",
                            "_atom_site.auth_comp_id",
                            "_atom_site.auth_asym_id",
                            "_atom_site.auth_seq_id",
                            "HETATM 1 P PG ATP A 1 0.0 0.0 0.0 PG ATP A 1",
                            "HETATM 2 MG MG MG A 2 1.0 0.0 0.0 MG MG A 2",
                            "ATOM 3 N NZ LYS A 44 2.0 0.0 0.0 NZ LYS A 44",
                            "#",
                        ]
                    ),
                    encoding="utf-8",
                )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-nonready-ligand-alternate-structure-plan",
                    "--epk-nonready-ligand-repair-plan",
                    str(repair),
                    "--graph",
                    str(graph),
                    "--cif-dir",
                    str(cif_dir),
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
            metadata = plan["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_nonready_ligand_alternate_structure_plan",
            )
            self.assertEqual(metadata["row_count"], 1)
            self.assertEqual(metadata["alternate_gamma_structure_count"], 1)
            self.assertEqual(
                metadata["alternate_gamma_metal_mapped_structure_count"],
                1,
            )
            self.assertFalse(metadata["ready_to_rerun_local_evidence_audit"])
            row = plan["rows"][0]
            self.assertEqual(
                row["repair_evidence_status"],
                "alternate_gamma_metal_structure_found_review_only",
            )
            self.assertEqual(row["alternate_gamma_metal_mapped_structure_count"], 1)
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_nonready_ligand_exclusion_decision_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            repair = root / "repair.json"
            alternate = root / "alternate.json"
            out = root / "exclusion.json"
            repair.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_nonready_ligand_repair_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:282",
                                "entry_name": "MAP kinase kinase",
                                "pdb_id": "1AAA",
                                "repair_lane": "structure_ligand_signal_not_local_axis",
                                "source_scorer_input_readiness": (
                                    "needs_ligand_distance_or_structure_repair"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_nonready_ligand_alternate_structure_plan"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:282",
                                "entry_name": "MAP kinase kinase",
                                "current_selected_pdb_id": "1AAA",
                                "repair_evidence_status": (
                                    "alternate_gamma_structure_found_metal_or_mapping_gap"
                                ),
                                "candidate_structures": [
                                    {
                                        "pdb_id": "1AAA",
                                        "current_selected_structure": True,
                                        "has_gamma_capable_nucleotide": True,
                                        "has_metal_ligand": True,
                                        "all_catalytic_residues_mapped": True,
                                    },
                                    {
                                        "pdb_id": "1AAB",
                                        "current_selected_structure": False,
                                        "has_gamma_capable_nucleotide": True,
                                        "has_metal_ligand": False,
                                        "all_catalytic_residues_mapped": False,
                                    },
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
                    "build-epk-nonready-ligand-exclusion-decision",
                    "--epk-nonready-ligand-repair-plan",
                    str(repair),
                    "--epk-nonready-ligand-alternate-structure-plan",
                    str(alternate),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            decision = json.loads(out.read_text(encoding="utf-8"))
            metadata = decision["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_nonready_ligand_exclusion_decision",
            )
            self.assertEqual(metadata["excluded_nonready_row_count"], 1)
            self.assertEqual(metadata["excluded_nonready_entry_ids"], ["m_csa:282"])
            self.assertTrue(metadata["nonready_rows_repaired_or_excluded"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = decision["rows"][0]
            self.assertEqual(
                row["exclusion_decision"],
                "exclude_from_current_epk_threshold_calibration",
            )
            self.assertTrue(row["excluded_from_current_epk_threshold_calibration"])
            self.assertEqual(row["alternate_gamma_structure_count"], 1)
            self.assertEqual(row["alternate_gamma_metal_mapped_structure_count"], 0)
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_acceptor_axis_threshold_design_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            acceptor_plan = root / "epk_acceptor_plan.json"
            out = root / "epk_threshold_design.json"
            acceptor_plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_acceptor_geometry_axis_gap_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "prototype_ready_row_count": 2,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "nearest_hydroxyl_residue_distance_angstrom": 2.5,
                                "nearest_acceptor_ligand_distance_angstrom": None,
                                "acceptor_axis_status": (
                                    "hydroxyl_residue_context_present_not_scored"
                                ),
                            },
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "nearest_hydroxyl_residue_distance_angstrom": 5.2,
                                "nearest_acceptor_ligand_distance_angstrom": 6.3,
                                "acceptor_axis_status": (
                                    "hydroxyl_residue_and_acceptor_ligand_context_present_not_scored"
                                ),
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
                    "build-epk-acceptor-axis-threshold-design",
                    "--epk-acceptor-geometry-axis-gap-plan",
                    str(acceptor_plan),
                    "--candidate-thresholds",
                    "4,6,8",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            design = json.loads(out.read_text(encoding="utf-8"))
            metadata = design["metadata"]
            self.assertEqual(metadata["method"], "epk_acceptor_axis_threshold_design")
            self.assertEqual(metadata["candidate_thresholds_angstrom"], [4.0, 6.0, 8.0])
            self.assertEqual(
                metadata[
                    "smallest_candidate_hydroxyl_cutoff_covering_current_prototype_rows"
                ],
                6.0,
            )
            self.assertIsNone(metadata["selected_threshold_angstrom"])
            self.assertFalse(metadata["threshold_calibrated"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            threshold_rows = {
                row["candidate_threshold_angstrom"]: row
                for row in design["threshold_rows"]
            }
            self.assertEqual(threshold_rows[4.0]["hydroxyl_residue_hit_count"], 1)
            self.assertEqual(threshold_rows[6.0]["hydroxyl_residue_hit_count"], 2)
            self.assertEqual(threshold_rows[8.0]["acceptor_ligand_hit_count"], 1)

    def test_build_epk_gamma_geometry_feasibility_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype_path = root / "epk_axis_prototype.json"
            acceptor_plan = root / "epk_acceptor_plan.json"
            out = root / "epk_gamma_feasibility.json"
            prototype_path.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_text_free_local_axis_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "text_free_axis_inputs": {
                                    "local_adenine_nucleotide_ligand": {
                                        "evidence_codes": ["ATP"]
                                    }
                                },
                            },
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "text_free_axis_inputs": {
                                    "local_adenine_nucleotide_ligand": {
                                        "evidence_codes": ["ADP"]
                                    }
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            acceptor_plan.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "epk_acceptor_geometry_axis_gap_plan"},
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "acceptor_axis_status": (
                                    "hydroxyl_residue_context_present_not_scored"
                                ),
                                "nearest_hydroxyl_residue_distance_angstrom": 2.5,
                            },
                            {
                                "entry_id": "m_csa:640",
                                "acceptor_axis_status": (
                                    "hydroxyl_residue_and_acceptor_ligand_context_present_not_scored"
                                ),
                                "nearest_hydroxyl_residue_distance_angstrom": 5.2,
                                "nearest_acceptor_ligand_distance_angstrom": 6.3,
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
                    "build-epk-gamma-geometry-feasibility-plan",
                    "--epk-text-free-local-axis-prototype",
                    str(prototype_path),
                    "--epk-acceptor-geometry-axis-gap-plan",
                    str(acceptor_plan),
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
            metadata = plan["metadata"]
            self.assertEqual(metadata["method"], "epk_gamma_geometry_feasibility_plan")
            self.assertFalse(metadata["gamma_phosphate_geometry_measured"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            rows = {row["entry_id"]: row for row in plan["rows"]}
            self.assertEqual(
                rows["m_csa:35"]["gamma_geometry_feasibility_status"],
                "gamma_capable_nucleotide_and_acceptor_context_present_not_measured",
            )
            self.assertEqual(
                rows["m_csa:640"]["gamma_geometry_feasibility_status"],
                "product_state_nucleotide_acceptor_context_present_needs_gamma_source",
            )
            self.assertFalse(rows["m_csa:35"]["epk_score_computed"])

    def test_build_epk_gamma_geometry_measurement_sample_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            feasibility = root / "epk_gamma_feasibility.json"
            geometry = root / "geometry.json"
            cif_dir = root / "cif"
            cif_dir.mkdir()
            out = root / "epk_gamma_measurement.json"
            feasibility.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_geometry_feasibility_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "gamma_capable_nucleotide_codes": ["ATP"],
                            },
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "gamma_capable_nucleotide_codes": [],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "active_site_geometry_features"},
                        "entries": [
                            {
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "pocket_context": {
                                    "nearby_residue_sites": [
                                        {
                                            "code": "THR",
                                            "chain_name": "A",
                                            "resid": "166",
                                        }
                                    ]
                                },
                            },
                            {"entry_id": "m_csa:640", "pdb_id": "1L8T"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (cif_dir / "2PHK.cif").write_text(
                "\n".join(
                    [
                        "data_2PHK",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.id",
                        "_atom_site.type_symbol",
                        "_atom_site.label_atom_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "_atom_site.auth_atom_id",
                        "_atom_site.auth_comp_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.auth_seq_id",
                        "HETATM 1 P PG ATP A 1 0.0 0.0 0.0 PG ATP A 1",
                        "ATOM 2 O OG1 THR A 166 3.0 4.0 0.0 OG1 THR A 166",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-gamma-geometry-measurement-sample",
                    "--epk-gamma-geometry-feasibility-plan",
                    str(feasibility),
                    "--geometry",
                    str(geometry),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            sample = json.loads(out.read_text(encoding="utf-8"))
            metadata = sample["metadata"]
            self.assertEqual(metadata["method"], "epk_gamma_geometry_measurement_sample")
            self.assertEqual(metadata["measured_row_count"], 1)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            rows = {row["entry_id"]: row for row in sample["rows"]}
            self.assertEqual(
                rows["m_csa:35"]["measurement_status"],
                "gamma_to_hydroxyl_distance_measured_review_only",
            )
            self.assertEqual(
                rows["m_csa:35"]["nearest_gamma_to_hydroxyl_distance_angstrom"],
                5.0,
            )
            self.assertEqual(
                rows["m_csa:640"]["measurement_status"],
                "product_or_missing_gamma_nucleotide_skipped",
            )
            self.assertFalse(rows["m_csa:35"]["epk_score_computed"])

    def test_build_epk_precount_gate_status_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            axis = root / "axis.json"
            threshold = root / "threshold.json"
            gamma = root / "gamma.json"
            repair = root / "repair.json"
            negative = root / "negative_controls.json"
            reaudit = root / "reaudit.json"
            template = root / "template.json"
            template_validation = root / "template_validation.json"
            chain_ligand = root / "chain_ligand.json"
            chain_external = root / "chain_external.json"
            out = root / "gate_status.json"
            axis.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_text_free_local_axis_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "prototype_ready_row_count": 3,
                        }
                    }
                ),
                encoding="utf-8",
            )
            threshold.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_acceptor_axis_threshold_design",
                            "selected_threshold_angstrom": None,
                            "threshold_calibrated": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            gamma.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_geometry_measurement_sample",
                            "measured_row_count": 2,
                            "measurement_status_counts": {
                                "gamma_to_hydroxyl_distance_measured_review_only": 2,
                                "product_or_missing_gamma_nucleotide_skipped": 1,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            repair.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_nonready_ligand_repair_plan",
                            "nonready_row_count": 2,
                            "repair_lane_counts": {
                                "selected_structure_ligand_axis_missing": 1
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            negative.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_negative_control_gamma_distance_distribution"
                            ),
                            "negative_control_distance_distribution_started": True,
                            "negative_control_distance_distribution_ready": False,
                            "measured_control_count": 1,
                            "lowest_covering_candidate_negative_control_hit_count": 1,
                            "threshold_selection_status": (
                                "blocked_negative_controls_overlap_or_insufficient_distribution"
                            ),
                        }
                    }
                ),
                encoding="utf-8",
            )
            reaudit.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_external_hard_negative_reaudit_plan",
                            "ready_to_run_scored_reaudit": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            template.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_family_specific_mapping_template_review",
                            "reviewed_sibling_family_id": "pfkb",
                            "seeded_template_entry_count": 1,
                            "template_residue_count": 2,
                            "template_review_status": (
                                "template_seeded_mapping_algorithm_pending_review_only"
                            ),
                            "family_specific_mapping_ready": False,
                            "measurement_ready_homolog_structure_count": 0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            template_validation.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_family_specific_mapping_template_validation_review"
                            ),
                            "template_validation_ready": True,
                            "all_template_families_validated_review_only": True,
                            "validated_template_family_ids": ["pfkb"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            chain_ligand.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_chain_ligand_acceptor_disambiguation_audit"
                            ),
                            "candidate_feature_id": (
                                "gamma_acceptor_non_catalytic_chain_or_ligand_analog_v0"
                            ),
                            "candidate_feature_status": (
                                "passes_current_review_controls_review_only"
                            ),
                            "current_positive_feature_hit_count": 3,
                            "negative_control_same_chain_block_count": 11,
                            "negative_control_false_hit_count": 0,
                            "external_hard_negative_abstention_row_count": 3,
                            "feature_passes_current_review_controls": True,
                            "feature_admissible_for_production_scoring": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            chain_external.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_chain_ligand_external_hard_negative_feature_screen"
                            ),
                            "candidate_feature_id": (
                                "gamma_acceptor_non_catalytic_chain_or_ligand_analog_v0"
                            ),
                            "review_only_feature_screen_complete": True,
                            "review_only_feature_screen_passed": True,
                            "review_only_external_hard_negative_feature_abstention_count": 3,
                            "review_only_external_hard_negative_feature_non_abstention_count": 0,
                            "clean_heldout_performance_claim_permitted": False,
                            "external_hard_negative_reaudit_scored": False,
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
                    "build-epk-precount-gate-status",
                    "--epk-text-free-local-axis-prototype",
                    str(axis),
                    "--epk-acceptor-axis-threshold-design",
                    str(threshold),
                    "--epk-gamma-geometry-measurement-sample",
                    str(gamma),
                    "--epk-nonready-ligand-repair-plan",
                    str(repair),
                    "--epk-negative-control-gamma-distance-distribution",
                    str(negative),
                    "--epk-family-specific-mapping-template-review",
                    str(template),
                    "--epk-family-specific-mapping-template-validation-review",
                    str(template_validation),
                    "--epk-chain-ligand-acceptor-disambiguation-audit",
                    str(chain_ligand),
                    "--epk-chain-ligand-external-hard-negative-feature-screen",
                    str(chain_external),
                    "--epk-external-hard-negative-reaudit-plan",
                    str(reaudit),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            status = json.loads(out.read_text(encoding="utf-8"))
            metadata = status["metadata"]
            self.assertEqual(metadata["method"], "epk_precount_gate_status")
            self.assertEqual(metadata["precount_gate_status"], "blocked_review_only")
            self.assertIn("acceptor_threshold_calibrated", metadata["failing_gate_ids"])
            self.assertIn(
                "gamma_geometry_measured_for_all_prototype_rows",
                metadata["failing_gate_ids"],
            )
            self.assertNotIn(
                "family_specific_homolog_mapping_template",
                metadata["failing_gate_ids"],
            )
            self.assertEqual(
                metadata["source_epk_family_specific_mapping_template_review_method"],
                "epk_family_specific_mapping_template_review",
            )
            self.assertEqual(
                metadata[
                    "source_epk_family_specific_mapping_template_validation_review_method"
                ],
                "epk_family_specific_mapping_template_validation_review",
            )
            self.assertEqual(metadata["negative_control_family_template_family_id"], "pfkb")
            self.assertEqual(
                metadata["negative_control_family_template_validated_family_ids"],
                ["pfkb"],
            )
            self.assertTrue(metadata["negative_control_family_template_validation_ready"])
            self.assertEqual(
                metadata[
                    "source_epk_chain_ligand_acceptor_disambiguation_audit_method"
                ],
                "epk_chain_ligand_acceptor_disambiguation_audit",
            )
            self.assertTrue(
                metadata[
                    "chain_ligand_acceptor_feature_passes_current_review_controls"
                ]
            )
            self.assertTrue(metadata["chain_ligand_external_feature_screen_passed"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            checks = {check["gate_id"]: check for check in status["gate_checks"]}
            self.assertTrue(checks["local_axis_prototype"]["passed"])
            self.assertFalse(checks["external_hard_negative_scored_reaudit"]["passed"])
            self.assertFalse(
                checks["gamma_negative_control_distance_distribution"]["passed"]
            )
            self.assertTrue(checks["family_specific_homolog_mapping_template"]["passed"])
            self.assertTrue(
                checks["chain_ligand_acceptor_disambiguation_audit"]["passed"]
            )
            self.assertTrue(
                checks[
                    "chain_ligand_external_hard_negative_feature_screen"
                ]["passed"]
            )

    def test_build_epk_acceptor_identity_review_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            gamma = root / "gamma.json"
            graph = root / "graph.json"
            out = root / "acceptor_identity.json"
            gamma.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_geometry_measurement_sample",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "measured_row_count": 1,
                            "gamma_phosphate_geometry_measured": True,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "pdb_id": "2PHK",
                                "measurement_status": (
                                    "gamma_to_hydroxyl_distance_measured_review_only"
                                ),
                                "distance_rows": [
                                    {
                                        "gamma_ligand_code": "ATP",
                                        "gamma_atom_name": "PG",
                                        "hydroxyl_residue_code": "SER",
                                        "hydroxyl_atom_name": "OG",
                                        "hydroxyl_chain_name": "B",
                                        "hydroxyl_resid": "5",
                                        "distance_angstrom": 3.6,
                                    }
                                ],
                            },
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "pdb_id": "1L8T",
                                "measurement_status": (
                                    "product_or_missing_gamma_nucleotide_skipped"
                                ),
                                "distance_rows": [],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "v1_graph"},
                        "nodes": [
                            {
                                "id": "m_csa:35:mechanism:1",
                                "type": "mechanism_text",
                                "text": (
                                    "Asp149 deprotonates the protein substrate "
                                    "hydroxyl group for attack on the "
                                    "gamma-phosphate of ATP."
                                ),
                            },
                            {
                                "id": "m_csa:35:residue:1",
                                "type": "catalytic_residue",
                                "structure_positions": [
                                    {"chain_name": "A", "resid": 136}
                                ],
                            },
                            {
                                "id": "m_csa:640:mechanism:1",
                                "type": "mechanism_text",
                                "text": (
                                    "Nucleophilic attack on the gamma phosphate "
                                    "of ATP by the 3' or 5' OH group of the "
                                    "substrate."
                                ),
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
                    "build-epk-acceptor-identity-review",
                    "--epk-gamma-geometry-measurement-sample",
                    str(gamma),
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
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(metadata["method"], "epk_acceptor_identity_review")
            self.assertEqual(
                metadata["measured_acceptor_identity_source_supported_count"],
                1,
            )
            self.assertTrue(metadata["measured_acceptor_identity_review_complete"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            rows = {row["entry_id"]: row for row in review["rows"]}
            self.assertEqual(
                rows["m_csa:35"]["acceptor_identity_review_status"],
                "measured_acceptor_identity_source_supported_review_only",
            )
            self.assertTrue(
                rows["m_csa:35"]["nearest_measured_hydroxyl"][
                    "on_non_catalytic_chain"
                ]
            )
            self.assertEqual(
                rows["m_csa:640"]["acceptor_identity_review_status"],
                "source_acceptor_supported_gamma_geometry_missing",
            )
            self.assertFalse(rows["m_csa:35"]["epk_score_computed"])

    def test_build_epk_atp_state_evidence_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            identity = root / "identity.json"
            graph = root / "graph.json"
            geometry = root / "geometry.json"
            cif_dir = root / "cif"
            cif_dir.mkdir()
            out = root / "atp_state.json"
            identity.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_acceptor_identity_review",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "pdb_id": "1BBB",
                                "acceptor_identity_review_status": (
                                    "source_acceptor_supported_gamma_geometry_missing"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "v1_graph"},
                        "nodes": [
                            {
                                "id": "m_csa:640",
                                "type": "m_csa_entry",
                                "reference_uniprot_id": "PTEST",
                            },
                            {
                                "id": "m_csa:640:residue:1",
                                "type": "catalytic_residue",
                                "sequence_positions": [
                                    {
                                        "uniprot_id": "PTEST",
                                        "resid": 44,
                                        "code": "Lys",
                                    }
                                ],
                            }
                        ],
                        "edges": [
                            {
                                "source": "m_csa:640",
                                "target": "uniprot:PTEST",
                                "predicate": "has_reference_protein",
                            },
                            {
                                "source": "uniprot:PTEST",
                                "target": "pdb:1AAA",
                                "predicate": "has_structure",
                            },
                            {
                                "source": "uniprot:PTEST",
                                "target": "pdb:1BBB",
                                "predicate": "has_structure",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "active_site_geometry_features"},
                        "entries": [
                            {
                                "entry_id": "m_csa:640",
                                "pdb_id": "1BBB",
                                "ligand_context": {
                                    "structure_ligand_codes": ["ADP", "KAN"]
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (cif_dir / "1AAA.cif").write_text(
                "\n".join(
                    [
                        "data_1AAA",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.id",
                        "_atom_site.type_symbol",
                        "_atom_site.label_atom_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "_atom_site.auth_atom_id",
                        "_atom_site.auth_comp_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.auth_seq_id",
                        "HETATM 1 P PG ATP A 1 0.0 0.0 0.0 PG ATP A 1",
                        "HETATM 2 C C1 KAN B 1 1.0 0.0 0.0 C1 KAN B 1",
                        "HETATM 3 O O1 KAN B 1 2.0 0.0 0.0 O1 KAN B 1",
                        "ATOM 4 N NZ LYS A 44 3.0 0.0 0.0 NZ LYS A 44",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            (cif_dir / "1BBB.cif").write_text(
                "\n".join(
                    [
                        "data_1BBB",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.id",
                        "_atom_site.type_symbol",
                        "_atom_site.label_atom_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "_atom_site.auth_atom_id",
                        "_atom_site.auth_comp_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.auth_seq_id",
                        "HETATM 1 P PB ADP A 1 0.0 0.0 0.0 PB ADP A 1",
                        "HETATM 2 C C1 KAN B 1 1.0 0.0 0.0 C1 KAN B 1",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-atp-state-evidence-plan",
                    "--epk-acceptor-identity-review",
                    str(identity),
                    "--graph",
                    str(graph),
                    "--geometry",
                    str(geometry),
                    "--entry-ids",
                    "m_csa:640",
                    "--cif-dir",
                    str(cif_dir),
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
            metadata = plan["metadata"]
            self.assertEqual(metadata["method"], "epk_atp_state_evidence_plan")
            self.assertEqual(metadata["candidate_atp_state_acceptor_row_count"], 1)
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            row = plan["rows"][0]
            self.assertEqual(
                row["atp_state_evidence_status"],
                "candidate_atp_state_acceptor_structure_found_review_only",
            )
            self.assertEqual(row["gamma_capable_acceptor_candidate_structure_count"], 1)
            self.assertEqual(
                row["alternate_gamma_acceptor_geometry_measured_structure_count"],
                1,
            )
            self.assertEqual(
                metadata["gamma_capable_residue_mapped_candidate_structure_count"],
                1,
            )
            self.assertEqual(
                metadata["alternate_gamma_acceptor_geometry_measured_count"],
                1,
            )
            self.assertFalse(row["epk_score_computed"])

    def test_build_epk_gamma_threshold_control_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            gamma = root / "gamma.json"
            identity = root / "identity.json"
            atp_state = root / "atp_state.json"
            threshold = root / "threshold.json"
            out = root / "threshold_control.json"
            gamma.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_geometry_measurement_sample",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "pdb_id": "2PHK",
                                "measurement_status": (
                                    "gamma_to_hydroxyl_distance_measured_review_only"
                                ),
                                "distance_rows": [
                                    {
                                        "gamma_ligand_code": "ATP",
                                        "gamma_atom_name": "PG",
                                        "hydroxyl_residue_code": "SER",
                                        "hydroxyl_atom_name": "OG",
                                        "hydroxyl_chain_name": "B",
                                        "hydroxyl_resid": "5",
                                        "distance_angstrom": 3.6,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            identity.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "epk_acceptor_identity_review"},
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "acceptor_identity_review_status": (
                                    "measured_acceptor_identity_source_supported_review_only"
                                ),
                                "acceptor_identity_source_supported": True,
                            },
                            {
                                "entry_id": "m_csa:640",
                                "acceptor_identity_review_status": (
                                    "source_acceptor_supported_gamma_geometry_missing"
                                ),
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            atp_state.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "epk_atp_state_evidence_plan"},
                        "rows": [
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "candidate_structures": [
                                    {
                                        "pdb_id": "3TM0",
                                        "current_selected_structure": False,
                                        "nearest_gamma_to_acceptor_like_oxygen_distance_angstrom": 3.5,
                                        "nearest_gamma_acceptor_atom_pair": {
                                            "gamma_ligand_code": "ANP",
                                            "gamma_atom_name": "PG",
                                            "acceptor_ligand_code": "B31",
                                            "acceptor_atom_name": "O14",
                                            "acceptor_chain_name": "A",
                                            "acceptor_resid": "305",
                                        },
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            threshold.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_acceptor_axis_threshold_design",
                            "candidate_thresholds_angstrom": [3.0, 4.0, 6.0],
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
                    "build-epk-gamma-threshold-control-plan",
                    "--epk-gamma-geometry-measurement-sample",
                    str(gamma),
                    "--epk-acceptor-identity-review",
                    str(identity),
                    "--epk-atp-state-evidence-plan",
                    str(atp_state),
                    "--epk-acceptor-axis-threshold-design",
                    str(threshold),
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
            metadata = plan["metadata"]
            self.assertEqual(metadata["method"], "epk_gamma_threshold_control_plan")
            self.assertEqual(metadata["row_count"], 2)
            self.assertEqual(
                metadata["lowest_review_geometry_covering_candidate_angstrom"],
                4.0,
            )
            self.assertTrue(metadata["threshold_control_plan_ready"])
            self.assertIsNone(metadata["selected_threshold_angstrom"])
            self.assertFalse(metadata["threshold_calibrated"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            self.assertEqual(metadata["control_requirement_count"], 4)
            rows = {row["entry_id"]: row for row in plan["rows"]}
            self.assertEqual(
                rows["m_csa:640"]["geometry_scope"],
                "alternate_graph_linked_structure",
            )
            self.assertFalse(rows["m_csa:640"]["epk_score_computed"])

    def test_build_epk_m_csa640_alternate_gamma_geometry_review_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            atp_state = root / "atp_state.json"
            threshold = root / "threshold.json"
            out = root / "m_csa640_review.json"
            atp_state.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_atp_state_evidence_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:640",
                                "entry_name": "kanamycin kinase",
                                "candidate_structures": [
                                    {
                                        "pdb_id": "3TM0",
                                        "has_gamma_capable_nucleotide": True,
                                        "has_acceptor_like_ligand": True,
                                        "all_catalytic_residues_mapped": True,
                                        "mapped_catalytic_residue_count": 4,
                                        "expected_catalytic_residue_count": 4,
                                        "nearest_gamma_to_acceptor_like_oxygen_distance_angstrom": 3.5,
                                        "nearest_gamma_acceptor_atom_pair": {
                                            "gamma_ligand_code": "ANP",
                                            "gamma_atom_name": "PG",
                                            "acceptor_ligand_code": "B31",
                                            "acceptor_atom_name": "O14",
                                            "acceptor_chain_name": "A",
                                            "acceptor_resid": "305",
                                        },
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            threshold.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_threshold_control_plan"
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:640",
                                "pdb_id": "3TM0",
                                "source_support_status": (
                                    "source_supported_alternate_analog_context_review_only"
                                ),
                                "acceptor_ligand_or_residue_code": "B31",
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
                    "build-epk-m-csa640-alternate-gamma-geometry-review",
                    "--epk-atp-state-evidence-plan",
                    str(atp_state),
                    "--epk-gamma-threshold-control-plan",
                    str(threshold),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_m_csa640_alternate_gamma_geometry_review",
            )
            self.assertEqual(
                metadata["alternate_gamma_geometry_supports_positive_axis_count"],
                1,
            )
            self.assertFalse(metadata["epk_score_computed"])
            row = review["rows"][0]
            self.assertEqual(row["pdb_id"], "3TM0")
            self.assertEqual(row["acceptor_ligand_code"], "B31")
            self.assertTrue(
                row["alternate_gamma_geometry_supports_positive_axis_review_only"]
            )
            self.assertFalse(row["production_scoring_admissible"])

    def test_build_epk_negative_control_gamma_distance_distribution_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            threshold = root / "threshold_control.json"
            family = root / "family_expansion.json"
            geometry = root / "geometry.json"
            cif_dir = root / "cif"
            cif_dir.mkdir()
            out = root / "negative_controls.json"
            threshold.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_threshold_control_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "candidate_thresholds_angstrom": [4.0, 6.0, 8.0],
                            "lowest_review_geometry_covering_candidate_angstrom": 6.0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            family.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "atp_phosphoryl_transfer_family_expansion"
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "family_id": "epk",
                            },
                            {
                                "entry_id": "m_csa:615",
                                "entry_name": "deoxyguanosine kinase",
                                "family_id": "dnk",
                                "family_name": "Deoxynucleoside kinases",
                                "decision_action": "reject_label",
                            },
                            {
                                "entry_id": "m_csa:643",
                                "entry_name": "acetate kinase",
                                "family_id": "askha",
                                "family_name": "ASKHA sugar and acetate kinases",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            geometry.write_text(
                json.dumps(
                    {
                        "metadata": {"max_entries": 1000},
                        "entries": [
                            {
                                "entry_id": "m_csa:615",
                                "pdb_id": "2OCP",
                                "status": "ok",
                                "ligand_context": {
                                    "ligand_codes": ["DTP"],
                                    "structure_ligand_codes": ["DTP"],
                                },
                                "pocket_context": {
                                    "nearby_residue_sites": [
                                        {
                                            "code": "SER",
                                            "chain_name": "A",
                                            "resid": "52",
                                        }
                                    ]
                                },
                            },
                            {
                                "entry_id": "m_csa:643",
                                "pdb_id": "1G99",
                                "status": "ok",
                                "ligand_context": {
                                    "structure_ligand_codes": ["ADP"]
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (cif_dir / "pdb_2OCP.cif").write_text(
                "\n".join(
                    [
                        "data_2OCP",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.id",
                        "_atom_site.type_symbol",
                        "_atom_site.label_atom_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "_atom_site.auth_atom_id",
                        "_atom_site.auth_comp_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.auth_seq_id",
                        "HETATM 1 P PG DTP A 1 0.0 0.0 0.0 PG DTP A 1",
                        "ATOM 2 O OG SER A 52 3.0 4.0 0.0 OG SER A 52",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-negative-control-gamma-distance-distribution",
                    "--epk-gamma-threshold-control-plan",
                    str(threshold),
                    "--atp-phosphoryl-transfer-family-expansion",
                    str(family),
                    "--geometry",
                    str(geometry),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            distribution = json.loads(out.read_text(encoding="utf-8"))
            metadata = distribution["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_negative_control_gamma_distance_distribution",
            )
            self.assertEqual(metadata["source_control_row_count"], 2)
            self.assertEqual(metadata["measured_control_count"], 1)
            self.assertFalse(metadata["negative_control_distance_distribution_ready"])
            self.assertEqual(
                metadata["lowest_covering_candidate_negative_control_hit_count"],
                1,
            )
            rows = {row["entry_id"]: row for row in distribution["rows"]}
            self.assertNotIn("m_csa:35", rows)
            self.assertEqual(
                rows["m_csa:615"]["measurement_status"],
                "selected_structure_gamma_to_hydroxyl_distance_measured_review_only",
            )
            self.assertEqual(
                rows["m_csa:615"]["nearest_gamma_to_hydroxyl_distance_angstrom"],
                5.0,
            )
            self.assertEqual(
                rows["m_csa:643"]["measurement_status"],
                "selected_structure_product_or_no_gamma_nucleotide_skipped",
            )
            self.assertFalse(rows["m_csa:615"]["epk_score_computed"])

    def test_build_epk_sibling_negative_control_alternate_structure_plan_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            distribution = root / "negative_controls.json"
            family = root / "family_expansion.json"
            graph = root / "graph.json"
            cif_dir = root / "cif"
            cif_dir.mkdir()
            out = root / "alternate_controls.json"
            distribution.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_negative_control_gamma_distance_distribution"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "control_row_count": 2,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:592",
                                "entry_name": "glucokinase",
                                "family_id": "askha",
                                "family_name": "ASKHA sugar and acetate kinases",
                                "pdb_id": "1AAA",
                                "measurement_status": (
                                    "selected_structure_product_or_no_gamma_nucleotide_skipped"
                                ),
                            },
                            {
                                "entry_id": "m_csa:615",
                                "entry_name": "deoxyguanosine kinase",
                                "family_id": "dnk",
                                "measurement_status": (
                                    "selected_structure_gamma_to_hydroxyl_distance_measured_review_only"
                                ),
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            family.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "atp_phosphoryl_transfer_family_expansion"
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:592",
                                "entry_name": "glucokinase",
                                "family_id": "askha",
                            },
                            {
                                "entry_id": "m_csa:615",
                                "entry_name": "deoxyguanosine kinase",
                                "family_id": "dnk",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            graph.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "v1_graph"},
                        "nodes": [
                            {
                                "id": "m_csa:592",
                                "type": "m_csa_entry",
                                "reference_uniprot_id": "PTEST",
                            },
                            {
                                "id": "m_csa:592:residue:1",
                                "type": "catalytic_residue",
                                "sequence_positions": [
                                    {
                                        "uniprot_id": "PTEST",
                                        "resid": 44,
                                        "code": "Lys",
                                    }
                                ],
                            },
                        ],
                        "edges": [
                            {
                                "source": "m_csa:592",
                                "target": "uniprot:PTEST",
                                "predicate": "has_reference_protein",
                            },
                            {
                                "source": "uniprot:PTEST",
                                "target": "pdb:1AAA",
                                "predicate": "has_structure",
                            },
                            {
                                "source": "uniprot:PTEST",
                                "target": "pdb:1AAB",
                                "predicate": "has_structure",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (cif_dir / "pdb_1AAB.cif").write_text(
                "\n".join(
                    [
                        "data_1AAB",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.id",
                        "_atom_site.type_symbol",
                        "_atom_site.label_atom_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "_atom_site.auth_atom_id",
                        "_atom_site.auth_comp_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.auth_seq_id",
                        "HETATM 1 P PG ATP A 1 0.0 0.0 0.0 PG ATP A 1",
                        "HETATM 2 MG MG MG A 2 1.0 0.0 0.0 MG MG A 2",
                        "ATOM 3 N NZ LYS A 44 2.0 0.0 0.0 NZ LYS A 44",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-sibling-negative-control-alternate-structure-plan",
                    "--epk-negative-control-gamma-distance-distribution",
                    str(distribution),
                    "--atp-phosphoryl-transfer-family-expansion",
                    str(family),
                    "--graph",
                    str(graph),
                    "--cif-dir",
                    str(cif_dir),
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
            metadata = plan["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_sibling_negative_control_alternate_structure_plan",
            )
            self.assertEqual(metadata["source_unmeasured_control_row_count"], 1)
            self.assertEqual(metadata["ready_for_future_distance_measurement_count"], 1)
            self.assertEqual(metadata["alternate_gamma_metal_mapped_structure_count"], 1)
            self.assertFalse(metadata["negative_control_distance_distribution_ready"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            rows = {row["entry_id"]: row for row in plan["rows"]}
            self.assertEqual(set(rows), {"m_csa:592"})
            self.assertEqual(
                rows["m_csa:592"]["alternate_control_evidence_status"],
                "alternate_gamma_metal_mapped_candidate_found_review_only",
            )
            self.assertFalse(rows["m_csa:592"]["epk_score_computed"])
            self.assertFalse(rows["m_csa:592"]["countable_label_candidate"])

    def test_build_epk_sibling_negative_control_alternate_gamma_distance_sample_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            plan = root / "alternate_controls.json"
            cif_dir = root / "cif"
            cif_dir.mkdir()
            out = root / "alternate_distances.json"
            plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_negative_control_alternate_structure_plan"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "ready_for_future_distance_measurement_count": 1,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:592",
                                "entry_name": "glucokinase",
                                "family_id": "askha",
                                "family_name": "ASKHA sugar and acetate kinases",
                                "source_selected_measurement_status": (
                                    "selected_structure_product_or_no_gamma_nucleotide_skipped"
                                ),
                                "candidate_structures": [
                                    {
                                        "pdb_id": "1AAB",
                                        "target_ligand_codes": ["ANP", "MG"],
                                        "has_gamma_capable_nucleotide": True,
                                        "has_metal_ligand": True,
                                        "all_catalytic_residues_mapped": True,
                                        "mapped_catalytic_residue_count": 1,
                                        "expected_catalytic_residue_count": 1,
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (cif_dir / "pdb_1AAB.cif").write_text(
                "\n".join(
                    [
                        "data_1AAB",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.id",
                        "_atom_site.type_symbol",
                        "_atom_site.label_atom_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "_atom_site.auth_atom_id",
                        "_atom_site.auth_comp_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.auth_seq_id",
                        "HETATM 1 P PG ANP A 1 0.0 0.0 0.0 PG ANP A 1",
                        "HETATM 2 MG MG MG A 2 1.0 0.0 0.0 MG MG A 2",
                        "ATOM 3 O OG SER A 52 3.0 4.0 0.0 OG SER A 52",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-sibling-negative-control-alternate-gamma-distance-sample",
                    "--epk-sibling-negative-control-alternate-structure-plan",
                    str(plan),
                    "--cif-dir",
                    str(cif_dir),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            sample = json.loads(out.read_text(encoding="utf-8"))
            metadata = sample["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_sibling_negative_control_alternate_gamma_distance_sample",
            )
            self.assertEqual(metadata["candidate_structure_count"], 1)
            self.assertEqual(metadata["measured_candidate_structure_count"], 1)
            self.assertFalse(metadata["negative_control_distance_distribution_ready"])
            self.assertFalse(metadata["ready_to_run_epk_scorer"])
            row = sample["rows"][0]
            self.assertEqual(
                row["measurement_status"],
                "alternate_gamma_to_hydroxyl_distance_measured_review_only",
            )
            self.assertEqual(
                row["nearest_gamma_to_hydroxyl_distance_angstrom"],
                5.0,
            )
            self.assertEqual(row["candidate_threshold_hits_angstrom"], [6.0, 8.0])
            self.assertFalse(row["epk_score_computed"])
            self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_negative_control_calibration_sufficiency_decision_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            distribution = root / "selected_distribution.json"
            alternate = root / "alternate_sample.json"
            out = root / "sufficiency.json"
            distribution.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_negative_control_gamma_distance_distribution"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "candidate_thresholds_angstrom": [4.0, 6.0, 8.0],
                            "lowest_review_geometry_covering_candidate_angstrom": 6.0,
                            "control_family_ids": ["askha", "dnk"],
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:615",
                                "entry_name": "deoxyguanosine kinase",
                                "family_id": "dnk",
                                "pdb_id": "1ABC",
                                "measurement_status": (
                                    "selected_structure_gamma_to_hydroxyl_distance_measured_review_only"
                                ),
                                "nearest_gamma_to_hydroxyl_distance_angstrom": 3.2,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_negative_control_alternate_gamma_distance_sample"
                            ),
                            "candidate_thresholds_angstrom": [4.0, 6.0, 8.0],
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:592",
                                "entry_name": "glucokinase",
                                "family_id": "askha",
                                "pdb_id": "3FGU",
                                "measurement_status": (
                                    "alternate_gamma_to_hydroxyl_distance_measured_review_only"
                                ),
                                "nearest_gamma_to_hydroxyl_distance_angstrom": 4.2,
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
                    "build-epk-negative-control-calibration-sufficiency-decision",
                    "--epk-negative-control-gamma-distance-distribution",
                    str(distribution),
                    "--epk-sibling-negative-control-alternate-gamma-distance-sample",
                    str(alternate),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            decision = json.loads(out.read_text(encoding="utf-8"))
            metadata = decision["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_negative_control_calibration_sufficiency_decision",
            )
            self.assertEqual(metadata["combined_measured_control_count"], 2)
            self.assertEqual(metadata["combined_measured_family_count"], 2)
            self.assertEqual(
                metadata["calibration_sufficiency_status"],
                "blocked_review_only",
            )
            self.assertEqual(
                metadata["threshold_calibration_decision"],
                "do_not_select_threshold",
            )
            self.assertFalse(metadata["threshold_calibrated"])
            self.assertFalse(metadata["epk_score_computed"])
            collisions = {
                row["threshold_angstrom"]: row
                for row in metadata["threshold_collision_rows"]
            }
            self.assertEqual(collisions[6.0]["combined_negative_control_hit_count"], 2)
            self.assertEqual(len(decision["rows"]), 2)

    def test_build_epk_missing_sibling_control_source_request_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            sufficiency = root / "sufficiency.json"
            distribution = root / "distribution.json"
            alternate_plan = root / "alternate_plan.json"
            out = root / "source_request.json"
            sufficiency.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_negative_control_calibration_sufficiency_decision"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "combined_measured_family_ids": ["askha", "dnk"],
                            "missing_sibling_family_ids": ["atp_grasp", "pfkb"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            distribution.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_negative_control_gamma_distance_distribution"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:310",
                                "entry_name": "D-alanine ligase",
                                "family_id": "atp_grasp",
                                "family_name": "ATP-grasp ligases",
                                "pdb_id": "1E4E",
                                "measurement_status": (
                                    "selected_structure_product_or_no_gamma_nucleotide_skipped"
                                ),
                            },
                            {
                                "entry_id": "m_csa:663",
                                "entry_name": "ribokinase",
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "pdb_id": "1RK2",
                                "measurement_status": (
                                    "selected_structure_product_or_no_gamma_nucleotide_skipped"
                                ),
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate_plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_negative_control_alternate_structure_plan"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:310",
                                "entry_name": "D-alanine ligase",
                                "family_id": "atp_grasp",
                                "family_name": "ATP-grasp ligases",
                                "selected_pdb_id": "1E4E",
                                "alternate_control_evidence_status": (
                                    "no_alternate_pdb_structure_screened"
                                ),
                                "graph_linked_alternate_pdb_count": 0,
                                "screened_alternate_pdb_count": 0,
                                "candidate_structures": [],
                            },
                            {
                                "entry_id": "m_csa:663",
                                "entry_name": "ribokinase",
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "selected_pdb_id": "1RK2",
                                "alternate_control_evidence_status": (
                                    "alternate_gamma_structure_found_metal_or_mapping_gap"
                                ),
                                "graph_linked_alternate_pdb_count": 1,
                                "screened_alternate_pdb_count": 1,
                                "alternate_gamma_structure_count": 1,
                                "alternate_gamma_metal_mapped_structure_count": 0,
                                "candidate_structures": [
                                    {
                                        "pdb_id": "1RKA",
                                        "target_ligand_codes": ["ANP"],
                                        "has_gamma_capable_nucleotide": True,
                                        "has_metal_ligand": False,
                                        "mapped_catalytic_residue_count": 1,
                                        "expected_catalytic_residue_count": 2,
                                        "all_catalytic_residues_mapped": False,
                                    }
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
                    "build-epk-missing-sibling-control-source-request",
                    "--epk-negative-control-calibration-sufficiency-decision",
                    str(sufficiency),
                    "--epk-negative-control-gamma-distance-distribution",
                    str(distribution),
                    "--epk-sibling-negative-control-alternate-structure-plan",
                    str(alternate_plan),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            request = json.loads(out.read_text(encoding="utf-8"))
            metadata = request["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_missing_sibling_control_source_request",
            )
            self.assertEqual(metadata["missing_sibling_family_count"], 2)
            self.assertEqual(metadata["row_count"], 2)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            rows = {row["entry_id"]: row for row in request["rows"]}
            self.assertEqual(
                rows["m_csa:310"]["source_request_type"],
                "source_graph_linked_or_external_pdb_structure",
            )
            self.assertEqual(
                rows["m_csa:663"]["source_request_type"],
                "repair_gamma_structure_metal_or_mapping_gap",
            )
            self.assertEqual(
                rows["m_csa:663"]["candidate_structure_summaries"][0][
                    "structure_gap_status"
                ],
                "gamma_capable_metal_or_mapping_gap",
            )

    def test_build_epk_sibling_control_repair_review_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_request = root / "source_request.json"
            alternate_plan = root / "alternate_plan.json"
            out = root / "repair_review.json"
            (root / "1GQT.cif").write_text(
                "\n".join(
                    [
                        "data_1GQT",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.auth_comp_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.auth_atom_id",
                        "_atom_site.label_atom_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.auth_seq_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "HETATM ACP ACP PG PG A A 1 1 0.0 0.0 0.0",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            source_request.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_missing_sibling_control_source_request",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:663",
                                "entry_name": "ribokinase",
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "source_request_type": (
                                    "repair_gamma_structure_metal_or_mapping_gap"
                                ),
                                "selected_pdb_id": "1RK2",
                                "reference_uniprot_id": "P0A9J6",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate_plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_negative_control_alternate_structure_plan"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:663",
                                "entry_name": "ribokinase",
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "selected_pdb_id": "1RK2",
                                "reference_uniprot_id": "P0A9J6",
                                "candidate_structures": [
                                    {
                                        "pdb_id": "1GQT",
                                        "target_ligand_codes": ["ACP"],
                                        "has_gamma_capable_nucleotide": True,
                                        "has_product_or_partial_nucleotide": False,
                                        "has_metal_ligand": False,
                                        "mapped_catalytic_residue_count": 4,
                                        "expected_catalytic_residue_count": 4,
                                        "all_catalytic_residues_mapped": True,
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
                    "build-epk-sibling-control-repair-review",
                    "--epk-missing-sibling-control-source-request",
                    str(source_request),
                    "--epk-sibling-negative-control-alternate-structure-plan",
                    str(alternate_plan),
                    "--family-id",
                    "pfkb",
                    "--cif-dir",
                    str(root),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(metadata["method"], "epk_sibling_control_repair_review")
            self.assertEqual(metadata["reviewed_family_id"], "pfkb")
            self.assertEqual(metadata["family_repair_review_status"], "blocked_review_only")
            self.assertEqual(metadata["mapped_gamma_structure_count"], 1)
            self.assertEqual(metadata["metal_supported_gamma_structure_count"], 0)
            self.assertEqual(metadata["measurement_ready_repaired_structure_count"], 0)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = review["rows"][0]
            self.assertEqual(
                row["repair_review_status"],
                "mapping_verified_metal_context_unresolved",
            )
            self.assertEqual(
                row["candidate_structure_reviews"][0]["repair_assessment_status"],
                "mapping_verified_metal_context_unresolved",
            )
            self.assertEqual(
                row["candidate_structure_reviews"][0]["observed_metal_ligand_codes"],
                [],
            )

    def test_build_epk_missing_sibling_control_post_repair_source_decision_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_request = root / "source_request.json"
            repair_review = root / "repair_review.json"
            out = root / "post_repair_decision.json"
            source_request.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_missing_sibling_control_source_request",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "missing_sibling_family_ids": ["pfkb"],
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:663",
                                "entry_name": "ribokinase",
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "source_request_type": (
                                    "repair_gamma_structure_metal_or_mapping_gap"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            repair_review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_sibling_control_repair_review",
                            "reviewed_family_id": "pfkb",
                            "family_repair_review_status": "blocked_review_only",
                            "measurement_ready_repaired_structure_count": 0,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:663",
                                "family_id": "pfkb",
                                "repair_review_status": (
                                    "mapping_verified_metal_context_unresolved"
                                ),
                                "candidate_structure_review_count": 1,
                                "measurement_ready_structure_count": 0,
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
                    "build-epk-missing-sibling-control-post-repair-source-decision",
                    "--epk-missing-sibling-control-source-request",
                    str(source_request),
                    "--epk-sibling-control-repair-review",
                    str(repair_review),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            decision = json.loads(out.read_text(encoding="utf-8"))
            metadata = decision["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_missing_sibling_control_post_repair_source_decision",
            )
            self.assertEqual(metadata["reviewed_sibling_family_ids"], ["pfkb"])
            self.assertEqual(
                metadata["post_repair_source_decision_counts"],
                {"external_or_homolog_source_needed": 1},
            )
            self.assertEqual(metadata["source_escalation_required_entry_count"], 1)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = decision["rows"][0]
            self.assertEqual(
                row["post_repair_source_decision"],
                "external_or_homolog_source_needed",
            )
            self.assertIn("metal-supported", row["next_source_evidence_needed"])

    def test_build_epk_sibling_control_homolog_source_plan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            post_repair = root / "post_repair.json"
            out = root / "homolog_source_plan.json"
            (root / "9PFY.cif").write_text(
                "\n".join(
                    [
                        "data_9PFY",
                        "_struct.title 'Crystal structure of nucleoside-diphosphate kinase with ATP'",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.auth_comp_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.auth_atom_id",
                        "_atom_site.label_atom_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.auth_seq_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "HETATM ATP ATP PG PG A A 1 1 0.0 0.0 0.0",
                        "HETATM MG MG MG MG A A 2 2 1.0 0.0 0.0",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            post_repair.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_missing_sibling_control_post_repair_source_decision"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:637",
                                "family_id": "ndk",
                                "post_repair_source_decision": (
                                    "external_or_homolog_source_needed"
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
                    "build-epk-sibling-control-homolog-source-plan",
                    "--epk-missing-sibling-control-post-repair-source-decision",
                    str(post_repair),
                    "--family-id",
                    "ndk",
                    "--candidate-pdb-ids",
                    "9PFY",
                    "--candidate-source-query",
                    "RCSB title phrase NDK plus ATP and MG",
                    "--cif-dir",
                    str(root),
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
            metadata = plan["metadata"]
            self.assertEqual(
                metadata["method"], "epk_sibling_control_homolog_source_plan"
            )
            self.assertEqual(metadata["reviewed_sibling_family_id"], "ndk")
            self.assertEqual(metadata["source_entry_ids"], ["m_csa:637"])
            self.assertEqual(metadata["candidate_pdb_count"], 1)
            self.assertEqual(metadata["metal_supported_gamma_candidate_count"], 1)
            self.assertEqual(metadata["measurement_ready_homolog_structure_count"], 0)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = plan["rows"][0]
            self.assertEqual(
                row["source_candidate_status"],
                "candidate_gamma_metal_source_review_only",
            )
            self.assertEqual(row["catalytic_mapping_status"], "not_mapped_review_pending")
            self.assertFalse(row["measurement_ready_for_negative_control"])

    def test_build_epk_sibling_control_homolog_mapping_review_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_plan = root / "source_plan.json"
            out = root / "homolog_mapping_review.json"
            (root / "9PFY.cif").write_text(
                "\n".join(
                    [
                        "data_9PFY",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.auth_comp_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.auth_atom_id",
                        "_atom_site.label_atom_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.auth_seq_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "HETATM ATP ATP PG PG A A 201 201 0.0 0.0 0.0",
                        "HETATM MG MG MG MG A A 202 202 1.0 0.0 0.0",
                        "ATOM HIS HIS ND1 ND1 A A 139 139 3.0 0.0 0.0",
                        "ATOM LYS LYS NZ NZ A A 34 34 3.5 0.2 0.0",
                        "ATOM ARG ARG NH1 NH1 A A 126 126 3.7 0.0 0.0",
                        "ATOM ASN ASN OD1 OD1 A A 136 136 4.0 0.1 0.0",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            source_plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_sibling_control_homolog_source_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "reviewed_sibling_family_id": "ndk",
                            "candidate_pdb_count": 1,
                        },
                        "rows": [
                            {
                                "pdb_id": "9PFY",
                                "family_id": "ndk",
                                "family_name": "Nucleoside diphosphate kinases",
                                "source_entry_ids": ["m_csa:637"],
                                "source_candidate_status": (
                                    "candidate_gamma_metal_source_review_only"
                                ),
                                "has_gamma_capable_nucleotide": True,
                                "has_metal_ligand": True,
                                "gamma_capable_nucleotide_codes": ["ATP"],
                                "metal_ligand_codes": ["MG"],
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
                    "build-epk-sibling-control-homolog-mapping-review",
                    "--epk-sibling-control-homolog-source-plan",
                    str(source_plan),
                    "--family-id",
                    "ndk",
                    "--cif-dir",
                    str(root),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"], "epk_sibling_control_homolog_mapping_review"
            )
            self.assertEqual(metadata["reviewed_sibling_family_id"], "ndk")
            self.assertEqual(metadata["mapping_reviewed_candidate_count"], 1)
            self.assertEqual(metadata["catalytic_histidine_mapped_candidate_count"], 1)
            self.assertEqual(metadata["nucleotide_site_mapped_candidate_count"], 1)
            self.assertEqual(metadata["measurement_ready_homolog_structure_count"], 1)
            self.assertFalse(metadata["calibration_distance_measured"])
            self.assertFalse(metadata["epk_score_computed"])
            row = review["rows"][0]
            self.assertEqual(
                row["homolog_mapping_status"],
                "homolog_mapping_ready_for_distance_measurement_review_only",
            )
            self.assertTrue(row["measurement_ready_for_negative_control"])
            self.assertFalse(row["negative_control_distance_distribution_ready"])
            self.assertEqual(row["chain_mappings"][0]["chain_id"], "A")

    def test_build_epk_family_specific_mapping_template_review_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            geometry_features = root / "geometry_features.json"
            mapping_review = root / "homolog_mapping_review.json"
            out = root / "template_review.json"
            geometry_features.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "geometry_fixture"},
                        "entries": [
                            {
                                "entry_id": "m_csa:663",
                                "entry_name": "ribokinase",
                                "pdb_id": "1RK2",
                                "residues": [
                                    {
                                        "code": "Asp",
                                        "chain_name": "A",
                                        "resid": 255,
                                        "roles": ["proton acceptor"],
                                        "residue_node_id": "m_csa:663:residue:4",
                                    },
                                    {
                                        "code": "Gly",
                                        "chain_name": "A",
                                        "resid": 254,
                                        "roles": ["electrostatic stabiliser"],
                                        "residue_node_id": "m_csa:663:residue:3",
                                    },
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            mapping_review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_sibling_control_homolog_mapping_review",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "reviewed_sibling_family_id": "pfkb",
                            "mapping_reviewed_candidate_count": 1,
                            "homolog_mapping_status_counts": {
                                "homolog_catalytic_histidine_mapping_unresolved": 1
                            },
                            "catalytic_histidine_mapped_candidate_count": 0,
                            "nucleotide_site_mapped_candidate_count": 1,
                            "measurement_ready_homolog_structure_count": 0,
                        },
                        "rows": [{"source_entry_ids": ["m_csa:663"]}],
                    }
                ),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-family-specific-mapping-template-review",
                    "--geometry-features",
                    str(geometry_features),
                    "--epk-sibling-control-homolog-mapping-review",
                    str(mapping_review),
                    "--family-id",
                    "pfkb",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"], "epk_family_specific_mapping_template_review"
            )
            self.assertEqual(metadata["reviewed_sibling_family_id"], "pfkb")
            self.assertEqual(metadata["seeded_template_entry_count"], 1)
            self.assertEqual(metadata["template_residue_count"], 2)
            self.assertEqual(metadata["source_mapping_review_histidine_mapped_count"], 0)
            self.assertEqual(metadata["source_mapping_review_nucleotide_site_mapped_count"], 1)
            self.assertFalse(metadata["family_specific_mapping_ready"])
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = review["rows"][0]
            self.assertEqual(row["entry_id"], "m_csa:663")
            self.assertFalse(row["template_ready_for_automated_mapping"])
            self.assertFalse(row["template_can_be_used_for_distance_measurement"])
            self.assertEqual(
                row["template_residues"][0]["template_role"],
                "acid_base_or_acceptor_seed",
            )

    def test_build_epk_family_specific_homolog_mapping_and_distance_commands(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_plan = root / "source_plan.json"
            template_review = root / "template_review.json"
            mapping_out = root / "family_mapping_review.json"
            distance_out = root / "family_distance_sample.json"
            (root / "PFB1.cif").write_text(
                "\n".join(
                    [
                        "data_PFB1",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.auth_comp_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.auth_atom_id",
                        "_atom_site.label_atom_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.auth_seq_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "HETATM ATP ATP PG PG A A 300 300 0.0 0.0 0.0",
                        "HETATM MG MG MG MG A A 301 301 3.0 0.0 0.0",
                        "ATOM ASP ASP OD1 OD1 A A 126 126 5.0 0.0 0.0",
                        "ATOM GLY GLY CA CA A A 122 122 6.0 0.0 0.0",
                        "ATOM LYS LYS NZ NZ A A 121 121 5.6 0.0 0.0",
                        "ATOM THR THR OG1 OG1 A A 191 191 6.1 0.0 0.0",
                        "ATOM ALA ALA CA CA A A 124 124 7.0 0.0 0.0",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            source_plan.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_sibling_control_homolog_source_plan",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "reviewed_sibling_family_id": "pfkb",
                            "candidate_pdb_count": 1,
                        },
                        "rows": [
                            {
                                "pdb_id": "PFB1",
                                "family_id": "pfkb",
                                "family_name": "PfkB family kinases",
                                "source_entry_ids": ["m_csa:663"],
                                "source_candidate_status": (
                                    "candidate_gamma_metal_source_review_only"
                                ),
                                "has_gamma_capable_nucleotide": True,
                                "has_metal_ligand": True,
                                "gamma_capable_nucleotide_codes": ["ATP"],
                                "metal_ligand_codes": ["MG"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            template_review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_family_specific_mapping_template_review",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "reviewed_sibling_family_id": "pfkb",
                            "template_review_status": (
                                "template_seeded_mapping_algorithm_pending_review_only"
                            ),
                            "seeded_template_entry_count": 1,
                            "template_residue_count": 4,
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:663",
                                "family_id": "pfkb",
                                "template_residues": [
                                    {
                                        "residue_code": "Asp",
                                        "template_role": "acid_base_or_acceptor_seed",
                                    },
                                    {
                                        "residue_code": "Gly",
                                        "template_role": (
                                            "phosphate_or_transition_state_stabilizer_seed"
                                        ),
                                    },
                                    {
                                        "residue_code": "Lys",
                                        "template_role": (
                                            "phosphate_or_transition_state_stabilizer_seed"
                                        ),
                                    },
                                    {
                                        "residue_code": "Ala",
                                        "template_role": (
                                            "phosphate_or_transition_state_stabilizer_seed"
                                        ),
                                    },
                                    {
                                        "residue_code": "Thr",
                                        "template_role": "metal_ligand_seed",
                                    },
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
                    "build-epk-family-specific-homolog-mapping-review",
                    "--epk-sibling-control-homolog-source-plan",
                    str(source_plan),
                    "--epk-family-specific-mapping-template-review",
                    str(template_review),
                    "--family-id",
                    "pfkb",
                    "--cif-dir",
                    str(root),
                    "--out",
                    str(mapping_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            mapping_review = json.loads(mapping_out.read_text(encoding="utf-8"))
            metadata = mapping_review["metadata"]
            self.assertEqual(
                metadata["method"], "epk_family_specific_homolog_mapping_review"
            )
            self.assertEqual(metadata["reviewed_sibling_family_id"], "pfkb")
            self.assertEqual(metadata["measurement_ready_homolog_structure_count"], 1)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = mapping_review["rows"][0]
            self.assertEqual(
                row["family_specific_homolog_mapping_status"],
                "family_specific_homolog_mapping_ready_for_distance_measurement_review_only",
            )
            self.assertTrue(row["measurement_ready_for_negative_control"])
            self.assertFalse(
                row["chain_mappings"][0]["exact_residue_position_transfer_used"]
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-family-specific-homolog-gamma-distance-sample",
                    "--epk-family-specific-homolog-mapping-review",
                    str(mapping_out),
                    "--candidate-thresholds",
                    "4,6,8",
                    "--cif-dir",
                    str(root),
                    "--out",
                    str(distance_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            sample = json.loads(distance_out.read_text(encoding="utf-8"))
            sample_meta = sample["metadata"]
            self.assertEqual(
                sample_meta["method"],
                "epk_family_specific_homolog_gamma_distance_sample",
            )
            self.assertEqual(sample_meta["measured_homolog_structure_count"], 1)
            self.assertFalse(sample_meta["negative_control_distance_distribution_ready"])
            self.assertFalse(sample_meta["epk_score_computed"])
            sample_row = sample["rows"][0]
            self.assertEqual(
                sample_row["measurement_status"],
                "family_specific_gamma_to_acid_base_distance_measured_review_only",
            )
            self.assertEqual(
                sample_row["nearest_gamma_to_family_acid_base_distance_angstrom"],
                5.0,
            )

    def test_build_epk_family_specific_mapping_template_validation_review_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            template = root / "template.json"
            mapping = root / "mapping.json"
            distance = root / "distance.json"
            blocked_distance = root / "blocked_distance.json"
            out = root / "validation.json"
            blocked_out = root / "blocked_validation.json"
            template.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_family_specific_mapping_template_review",
                            "reviewed_sibling_family_id": "pfkb",
                            "reviewed_sibling_family_name": "PfkB family kinases",
                            "template_review_status": (
                                "template_seeded_mapping_algorithm_pending_review_only"
                            ),
                            "family_specific_mapping_ready": False,
                            "seeded_template_entry_count": 1,
                            "template_residue_count": 4,
                        }
                    }
                ),
                encoding="utf-8",
            )
            mapping.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_family_specific_homolog_mapping_review"
                            ),
                            "reviewed_sibling_family_id": "pfkb",
                            "reviewed_sibling_family_name": "PfkB family kinases",
                            "measurement_ready_homolog_structure_count": 1,
                        }
                    }
                ),
                encoding="utf-8",
            )
            distance.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_family_specific_homolog_gamma_distance_sample"
                            ),
                            "reviewed_sibling_family_id": "pfkb",
                            "reviewed_sibling_family_name": "PfkB family kinases",
                            "measured_homolog_structure_count": 1,
                        }
                    }
                ),
                encoding="utf-8",
            )
            blocked_distance.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_family_specific_homolog_gamma_distance_sample"
                            ),
                            "reviewed_sibling_family_id": "pfkb",
                            "reviewed_sibling_family_name": "PfkB family kinases",
                            "measured_homolog_structure_count": 0,
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
                    "build-epk-family-specific-mapping-template-validation-review",
                    "--epk-family-specific-mapping-template-review",
                    str(template),
                    "--epk-family-specific-homolog-mapping-review",
                    str(mapping),
                    "--epk-family-specific-homolog-gamma-distance-sample",
                    str(distance),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_family_specific_mapping_template_validation_review",
            )
            self.assertTrue(metadata["template_validation_ready"])
            self.assertEqual(metadata["validated_template_family_ids"], ["pfkb"])
            self.assertEqual(metadata["validated_template_family_count"], 1)
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            self.assertEqual(metadata["countable_label_candidate_count"], 0)
            row = review["rows"][0]
            self.assertTrue(row["validated_by_downstream_mapping"])
            self.assertFalse(row["countable_label_candidate"])

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-epk-family-specific-mapping-template-validation-review",
                    "--epk-family-specific-mapping-template-review",
                    str(template),
                    "--epk-family-specific-homolog-mapping-review",
                    str(mapping),
                    "--epk-family-specific-homolog-gamma-distance-sample",
                    str(blocked_distance),
                    "--out",
                    str(blocked_out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            blocked = json.loads(blocked_out.read_text(encoding="utf-8"))
            blocked_metadata = blocked["metadata"]
            self.assertFalse(blocked_metadata["template_validation_ready"])
            self.assertEqual(blocked_metadata["validated_template_family_ids"], [])
            self.assertEqual(
                blocked["rows"][0]["validation_status"],
                "template_validation_blocked_review_only",
            )

    def test_build_epk_sibling_control_homolog_gamma_distance_sample_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            mapping_review = root / "homolog_mapping_review.json"
            out = root / "homolog_distance_sample.json"
            (root / "9PFY.cif").write_text(
                "\n".join(
                    [
                        "data_9PFY",
                        "loop_",
                        "_atom_site.group_PDB",
                        "_atom_site.auth_comp_id",
                        "_atom_site.label_comp_id",
                        "_atom_site.auth_atom_id",
                        "_atom_site.label_atom_id",
                        "_atom_site.auth_asym_id",
                        "_atom_site.label_asym_id",
                        "_atom_site.auth_seq_id",
                        "_atom_site.label_seq_id",
                        "_atom_site.Cartn_x",
                        "_atom_site.Cartn_y",
                        "_atom_site.Cartn_z",
                        "HETATM ATP ATP PG PG A A 201 201 0.0 0.0 0.0",
                        "HETATM MG MG MG MG A A 202 202 1.0 0.0 0.0",
                        "ATOM HIS HIS ND1 ND1 A A 139 139 3.0 0.0 0.0",
                        "ATOM HIS HIS NE2 NE2 A A 139 139 3.4 0.0 0.0",
                        "ATOM SER SER OG OG A A 45 45 6.5 0.0 0.0",
                        "#",
                    ]
                ),
                encoding="utf-8",
            )
            mapping_review.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_sibling_control_homolog_mapping_review",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "reviewed_sibling_family_id": "ndk",
                            "ready_for_future_distance_measurement_count": 1,
                        },
                        "rows": [
                            {
                                "pdb_id": "9PFY",
                                "family_id": "ndk",
                                "family_name": "Nucleoside diphosphate kinases",
                                "source_entry_ids": ["m_csa:637"],
                                "measurement_ready_for_negative_control": True,
                                "gamma_capable_nucleotide_codes": ["ATP"],
                                "metal_ligand_codes": ["MG"],
                                "mapped_chain_count": 1,
                                "chain_mappings": [
                                    {
                                        "chain_id": "A",
                                        "gamma_ligand_code": "ATP",
                                        "gamma_atom_name": "PG",
                                        "gamma_ligand_auth_seq_id": "201",
                                        "gamma_ligand_label_seq_id": "201",
                                        "mapping_status": (
                                            "mapped_catalytic_histidine_and_nucleotide_site_review_only"
                                        ),
                                        "catalytic_histidine_residues": [
                                            {
                                                "auth_asym_id": "A",
                                                "label_asym_id": "A",
                                                "auth_seq_id": "139",
                                                "label_seq_id": "139",
                                                "residue_code": "HIS",
                                            }
                                        ],
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
                    "build-epk-sibling-control-homolog-gamma-distance-sample",
                    "--epk-sibling-control-homolog-mapping-review",
                    str(mapping_review),
                    "--candidate-thresholds",
                    "4,6,8",
                    "--cif-dir",
                    str(root),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            sample = json.loads(out.read_text(encoding="utf-8"))
            metadata = sample["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_sibling_control_homolog_gamma_distance_sample",
            )
            self.assertEqual(metadata["reviewed_sibling_family_id"], "ndk")
            self.assertEqual(metadata["measured_homolog_structure_count"], 1)
            self.assertEqual(
                metadata["homolog_control_axis"],
                "mapped_phosphohistidine_site_not_hydroxyl_acceptor",
            )
            self.assertFalse(metadata["threshold_calibrated"])
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            row = sample["rows"][0]
            self.assertEqual(
                row["measurement_status"],
                "homolog_gamma_to_mapped_histidine_distance_measured_review_only",
            )
            self.assertEqual(
                row["nearest_gamma_to_mapped_histidine_distance_angstrom"], 3.0
            )
            self.assertEqual(row["candidate_threshold_hits_angstrom"], [4.0, 6.0, 8.0])
            self.assertFalse(row["countable_label_candidate"])

    def test_build_epk_review_only_scoring_prototype_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            axis = root / "axis.json"
            gamma = root / "gamma.json"
            identity = root / "identity.json"
            homolog = root / "homolog.json"
            external = root / "external.json"
            out = root / "prototype.json"
            axis.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_text_free_local_axis_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "entry_name": "phosphorylase kinase",
                                "pdb_id": "2PHK",
                                "prototype_vector": {
                                    "local_adenine_nucleotide_ligand": 1,
                                    "local_metal_ligand": 1,
                                    "catalytic_acid_base_residue": 1,
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            gamma.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_gamma_geometry_measurement_sample"
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "nearest_gamma_to_hydroxyl_distance_angstrom": 3.6,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            identity.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "epk_acceptor_identity_review"},
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "acceptor_identity_source_supported": True,
                                "acceptor_identity_review_status": (
                                    "measured_acceptor_identity_source_supported_review_only"
                                ),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            homolog.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_control_homolog_gamma_distance_sample"
                            )
                        },
                        "rows": [
                            {
                                "pdb_id": "9PFY",
                                "family_id": "ndk",
                                "family_name": "Nucleoside diphosphate kinases",
                                "measurement_status": (
                                    "homolog_gamma_to_mapped_histidine_distance_measured_review_only"
                                ),
                                "nearest_gamma_to_mapped_histidine_distance_angstrom": 3.0,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            external.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "uniprot:P78549",
                                "accession": "P78549",
                                "active_site_feature_count": 2,
                                "out_of_scope_inverse_gate": {
                                    "inverse_gate_status": "passed",
                                    "max_current_fingerprint_score": 0.115,
                                },
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
                    "build-epk-review-only-scoring-prototype",
                    "--epk-text-free-local-axis-prototype",
                    str(axis),
                    "--epk-gamma-geometry-measurement-sample",
                    str(gamma),
                    "--epk-acceptor-identity-review",
                    str(identity),
                    "--epk-sibling-control-homolog-gamma-distance-sample",
                    str(homolog),
                    "--external-hard-negative-inverse-gate-scores",
                    str(external),
                    "--imported-external-entry-ids",
                    "uniprot:P78549",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            prototype = json.loads(out.read_text(encoding="utf-8"))
            metadata = prototype["metadata"]
            self.assertEqual(metadata["method"], "epk_review_only_scoring_prototype")
            self.assertEqual(metadata["prototype_gate_status"], "fail_closed_review_only")
            self.assertEqual(metadata["current_positive_full_axis_count"], 1)
            self.assertEqual(metadata["sibling_homolog_counteraxis_row_count"], 1)
            self.assertEqual(metadata["imported_external_hard_negative_row_count"], 1)
            self.assertFalse(metadata["epk_score_computed"])
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            decisions = {row["prototype_decision"] for row in prototype["rows"]}
            self.assertIn(
                "blocked_by_phosphohistidine_counteraxis_review_only", decisions
            )
            self.assertIn(
                "external_hard_negative_abstain_missing_epk_axes_review_only",
                decisions,
            )

    def test_build_epk_counteraxis_sufficiency_decision_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype = root / "prototype.json"
            precount = root / "precount.json"
            out = root / "counteraxis.json"
            prototype.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_review_only_scoring_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "candidate_threshold_angstrom": 6.0,
                            "prototype_gate_status": "fail_closed_review_only",
                        },
                        "rows": [
                            {
                                "row_type": (
                                    "sibling_family_specific_negative_control"
                                ),
                                "pdb_id": "1ABC",
                                "family_id": "pfkb",
                                "nearest_gamma_to_family_acid_base_distance_angstrom": (
                                    4.2
                                ),
                                "review_only_prototype_score": 0.0,
                            },
                            {
                                "row_type": "sibling_homolog_negative_control",
                                "pdb_id": "9PFY",
                                "family_id": "ndk",
                                "review_only_prototype_score": 0.0,
                            },
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P78549",
                                "review_only_prototype_score": 0.0,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            precount.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_precount_gate_status",
                            "precount_gate_status": "blocked_review_only",
                            "failing_gate_ids": [
                                "acceptor_threshold_calibrated",
                                "external_hard_negative_scored_reaudit",
                            ],
                            "chain_ligand_acceptor_feature_passes_current_review_controls": True,
                            "chain_ligand_acceptor_feature_admissible_for_production_scoring": False,
                            "chain_ligand_acceptor_negative_control_false_hit_count": 0,
                            "chain_ligand_external_feature_non_abstention_count": 0,
                            "negative_control_family_template_validated_family_ids": [
                                "pfkb"
                            ],
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
                    "build-epk-counteraxis-sufficiency-decision",
                    "--epk-review-only-scoring-prototype",
                    str(prototype),
                    "--epk-precount-gate-status",
                    str(precount),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            decision = json.loads(out.read_text(encoding="utf-8"))
            metadata = decision["metadata"]
            self.assertEqual(metadata["method"], "epk_counteraxis_sufficiency_decision")
            self.assertEqual(metadata["threshold_selection_decision"], "do_not_select_threshold")
            self.assertEqual(metadata["family_specific_counteraxis_threshold_hit_count"], 1)
            self.assertEqual(metadata["phosphohistidine_counteraxis_row_count"], 1)
            self.assertTrue(
                metadata[
                    "chain_ligand_acceptor_feature_passes_current_review_controls"
                ]
            )
            self.assertEqual(
                metadata["family_specific_template_validated_family_ids"], ["pfkb"]
            )
            self.assertTrue(
                metadata["counteraxis_sufficient_to_block_distance_only_threshold"]
            )
            self.assertFalse(metadata["ready_to_expand_positive_fingerprint_universe"])
            self.assertFalse(metadata["fingerprint_registry_edited"])
            self.assertFalse(metadata["curated_label_registry_edited"])
            self.assertEqual(metadata["countable_label_candidate_count"], 0)
            axes = {row["decision_axis"]: row for row in decision["decision_rows"]}
            self.assertEqual(
                axes["family_specific_sibling_counteraxis"]["decision"],
                "blocks_distance_only_threshold_selection",
            )
            self.assertEqual(
                axes["chain_ligand_acceptor_disambiguation_feature"]["decision"],
                "passes_current_controls_but_not_production_admissible",
            )

    def test_build_epk_substrate_acceptor_counteraxis_prototype_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype = root / "prototype.json"
            counteraxis = root / "counteraxis.json"
            out = root / "substrate_acceptor.json"
            prototype.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_review_only_scoring_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "text_free_inputs_only": True,
                                "prototype_decision": (
                                    "candidate_positive_signal_review_only_not_calibrated"
                                ),
                                "review_only_prototype_score": 1.0,
                                "prototype_axis_values": {
                                    "local_adenine_nucleotide_ligand": 1,
                                    "local_metal_ligand": 1,
                                    "catalytic_acid_base_residue": 1,
                                    "gamma_to_acceptor_distance_within_candidate_cutoff": 1,
                                    "source_supported_hydroxyl_acceptor_identity": 1,
                                },
                            },
                            {
                                "row_type": "sibling_homolog_negative_control",
                                "family_id": "ndk",
                                "pdb_id": "9PFY",
                                "text_free_inputs_only": True,
                                "prototype_decision": (
                                    "blocked_by_phosphohistidine_counteraxis_review_only"
                                ),
                                "prototype_axis_values": {
                                    "gamma_to_mapped_histidine_counteraxis": 1,
                                    "source_supported_hydroxyl_acceptor_identity": 0,
                                },
                            },
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P78549",
                                "text_free_inputs_only": True,
                                "prototype_axis_values": {
                                    "local_adenine_nucleotide_ligand": 0,
                                    "local_metal_ligand": 0,
                                    "catalytic_acid_base_residue": 0,
                                    "gamma_to_acceptor_distance_within_candidate_cutoff": 0,
                                    "source_supported_hydroxyl_acceptor_identity": 0,
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            counteraxis.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_counteraxis_sufficiency_decision"
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
                    "build-epk-substrate-acceptor-counteraxis-prototype",
                    "--epk-review-only-scoring-prototype",
                    str(prototype),
                    "--epk-counteraxis-sufficiency-decision",
                    str(counteraxis),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            surface = json.loads(out.read_text(encoding="utf-8"))
            metadata = surface["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_substrate_acceptor_counteraxis_prototype",
            )
            self.assertEqual(metadata["positive_like_acceptor_axis_row_count"], 1)
            self.assertEqual(metadata["blocked_counteraxis_row_count"], 1)
            self.assertEqual(metadata["external_hard_negative_abstention_row_count"], 1)
            self.assertTrue(metadata["decision_surface_changed"])
            self.assertFalse(metadata["epk_score_computed"])
            decisions = {
                row["counteraxis_rule_decision"] for row in surface["rows"]
            }
            self.assertIn("positive_like_acceptor_axis_review_only", decisions)
            self.assertIn(
                "blocked_by_non_hydroxyl_phosphohistidine_counteraxis",
                decisions,
            )
            self.assertIn(
                "external_hard_negative_abstain_missing_epk_acceptor_axes",
                decisions,
            )

    def test_build_epk_external_hard_negative_counteraxis_review_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            substrate = root / "substrate.json"
            out = root / "external_review.json"
            substrate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_substrate_acceptor_counteraxis_prototype"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P78549",
                                "text_free_inputs_only": True,
                                "counteraxis_rule_decision": (
                                    "external_hard_negative_abstain_missing_epk_acceptor_axes"
                                ),
                                "source_axis_values": {
                                    "local_adenine_nucleotide_ligand": 0
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
                    "build-epk-external-hard-negative-counteraxis-review",
                    "--epk-substrate-acceptor-counteraxis-prototype",
                    str(substrate),
                    "--imported-external-entry-ids",
                    "uniprot:P78549",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            review = json.loads(out.read_text(encoding="utf-8"))
            metadata = review["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_external_hard_negative_counteraxis_review",
            )
            self.assertEqual(
                metadata["review_only_external_hard_negative_abstention_count"],
                1,
            )
            self.assertEqual(
                metadata["review_only_external_hard_negative_non_abstention_count"],
                0,
            )
            self.assertFalse(metadata["clean_heldout_performance_claim_permitted"])
            self.assertFalse(metadata["epk_score_computed"])
            self.assertEqual(
                review["rows"][0]["review_status"],
                "review_only_external_hard_negative_abstention",
            )

    def test_build_epk_text_free_acceptor_feature_gap_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype = root / "prototype.json"
            homolog = root / "homolog.json"
            family = root / "family.json"
            out = root / "acceptor_gap.json"
            prototype.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_review_only_scoring_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "nearest_gamma_to_hydroxyl_distance_angstrom": 5.0,
                                "acceptor_context_type": (
                                    "source_supported_hydroxyl_residue"
                                ),
                                "gamma_geometry_scope": "current_selected_structure",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            homolog.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_control_homolog_gamma_distance_sample"
                            )
                        },
                        "rows": [
                            {
                                "measurement_status": (
                                    "homolog_gamma_to_mapped_histidine_distance_measured_review_only"
                                ),
                                "family_id": "ndk",
                                "family_name": "Nucleoside diphosphate kinases",
                                "pdb_id": "9PFY",
                                "nearest_gamma_to_same_chain_hydroxyl_distance_angstrom": 4.8,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            family.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_family_specific_homolog_gamma_distance_sample"
                            )
                        },
                        "rows": [
                            {
                                "measurement_status": (
                                    "family_specific_gamma_to_acid_base_distance_measured_review_only"
                                ),
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "pdb_id": "1ESQ",
                                "nearest_gamma_to_same_chain_hydroxyl_distance_angstrom": 7.1,
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
                    "build-epk-text-free-acceptor-feature-gap-audit",
                    "--epk-review-only-scoring-prototype",
                    str(prototype),
                    "--epk-sibling-control-homolog-gamma-distance-sample",
                    str(homolog),
                    "--epk-family-specific-homolog-gamma-distance-sample",
                    str(family),
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
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_text_free_acceptor_feature_gap_audit",
            )
            self.assertEqual(metadata["current_positive_feature_hit_count"], 1)
            self.assertEqual(metadata["negative_control_row_count"], 2)
            self.assertEqual(metadata["negative_control_false_hit_count"], 1)
            self.assertEqual(metadata["candidate_feature_status"], "blocked_review_only")
            self.assertFalse(metadata["feature_admissible_for_scoring"])
            self.assertFalse(metadata["epk_score_computed"])
            decisions = {row["feature_audit_decision"] for row in audit["rows"]}
            self.assertIn(
                "control_false_hit_blocks_text_free_feature", decisions
            )
            self.assertIn("control_nonhit_review_only", decisions)

    def test_build_epk_chain_ligand_acceptor_disambiguation_audit_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prototype = root / "prototype.json"
            identity = root / "identity.json"
            alternate = root / "alternate.json"
            homolog = root / "homolog.json"
            family = root / "family.json"
            out = root / "chain_ligand.json"
            prototype.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "epk_review_only_scoring_prototype",
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:35",
                                "pdb_id": "2PHK",
                                "nearest_gamma_to_hydroxyl_distance_angstrom": 5.0,
                                "acceptor_context_type": (
                                    "source_supported_hydroxyl_residue"
                                ),
                            },
                            {
                                "row_type": "current_epk_positive_prototype",
                                "entry_id": "m_csa:640",
                                "pdb_id": "3TM0",
                                "acceptor_context_type": (
                                    "acceptor_like_ligand_analog"
                                ),
                            },
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P78549",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            identity.write_text(
                json.dumps(
                    {
                        "metadata": {"method": "epk_acceptor_identity_review"},
                        "rows": [
                            {
                                "entry_id": "m_csa:35",
                                "nearest_measured_hydroxyl": {
                                    "distance_angstrom": 5.0,
                                    "on_non_catalytic_chain": True,
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            alternate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_m_csa640_alternate_gamma_geometry_review"
                            )
                        },
                        "rows": [
                            {
                                "entry_id": "m_csa:640",
                                "pdb_id": "3TM0",
                                "gamma_to_acceptor_distance_angstrom": 3.5,
                                "acceptor_like_ligand_present": True,
                                "within_candidate_threshold": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            homolog.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_sibling_control_homolog_gamma_distance_sample"
                            )
                        },
                        "rows": [
                            {
                                "measurement_status": (
                                    "homolog_gamma_to_mapped_histidine_distance_measured_review_only"
                                ),
                                "family_id": "ndk",
                                "family_name": "Nucleoside diphosphate kinases",
                                "pdb_id": "9PFY",
                                "nearest_gamma_to_same_chain_hydroxyl_distance_angstrom": 4.8,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            family.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_family_specific_homolog_gamma_distance_sample"
                            )
                        },
                        "rows": [
                            {
                                "measurement_status": (
                                    "family_specific_gamma_to_acid_base_distance_measured_review_only"
                                ),
                                "family_id": "pfkb",
                                "family_name": "PfkB/ribokinase-family kinases",
                                "pdb_id": "1TZ6",
                                "nearest_gamma_to_same_chain_hydroxyl_distance_angstrom": 7.1,
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
                    "build-epk-chain-ligand-acceptor-disambiguation-audit",
                    "--epk-review-only-scoring-prototype",
                    str(prototype),
                    "--epk-acceptor-identity-review",
                    str(identity),
                    "--epk-m-csa640-alternate-gamma-geometry-review",
                    str(alternate),
                    "--epk-sibling-control-homolog-gamma-distance-sample",
                    str(homolog),
                    "--epk-family-specific-homolog-gamma-distance-sample",
                    str(family),
                    "--imported-external-entry-ids",
                    "uniprot:P78549",
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
            metadata = audit["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_chain_ligand_acceptor_disambiguation_audit",
            )
            self.assertEqual(metadata["current_positive_feature_hit_count"], 2)
            self.assertEqual(metadata["negative_control_row_count"], 2)
            self.assertEqual(metadata["negative_control_false_hit_count"], 0)
            self.assertEqual(
                metadata["negative_control_same_chain_block_count"], 1
            )
            self.assertEqual(
                metadata["external_hard_negative_abstention_row_count"], 1
            )
            self.assertTrue(metadata["feature_passes_current_review_controls"])
            self.assertFalse(metadata["feature_admissible_for_production_scoring"])
            self.assertFalse(metadata["epk_score_computed"])
            decisions = {row["feature_audit_decision"] for row in audit["rows"]}
            self.assertIn(
                "positive_chain_ligand_acceptor_context_hit_review_only",
                decisions,
            )
            self.assertIn("control_blocked_same_chain_hydroxyl_context", decisions)
            self.assertIn(
                "external_hard_negative_abstain_missing_chain_ligand_axes",
                decisions,
            )

    def test_build_epk_chain_ligand_external_hard_negative_feature_screen_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            audit_path = root / "chain_ligand.json"
            out = root / "external_screen.json"
            audit_path.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "epk_chain_ligand_acceptor_disambiguation_audit"
                            ),
                            "target_fingerprint_id": (
                                "epk_atp_gamma_phosphoryl_transfer"
                            ),
                            "candidate_feature_id": (
                                "gamma_acceptor_non_catalytic_chain_or_ligand_analog_v0"
                            ),
                        },
                        "rows": [
                            {
                                "row_type": "imported_external_hard_negative",
                                "entry_id": "uniprot:P78549",
                                "text_free_inputs_only": True,
                                "candidate_feature_hit": False,
                                "feature_audit_decision": (
                                    "external_hard_negative_abstain_missing_chain_ligand_axes"
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
                    "build-epk-chain-ligand-external-hard-negative-feature-screen",
                    "--epk-chain-ligand-acceptor-disambiguation-audit",
                    str(audit_path),
                    "--imported-external-entry-ids",
                    "uniprot:P78549",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            screen = json.loads(out.read_text(encoding="utf-8"))
            metadata = screen["metadata"]
            self.assertEqual(
                metadata["method"],
                "epk_chain_ligand_external_hard_negative_feature_screen",
            )
            self.assertTrue(metadata["review_only_feature_screen_complete"])
            self.assertTrue(metadata["review_only_feature_screen_passed"])
            self.assertEqual(
                metadata[
                    "review_only_external_hard_negative_feature_non_abstention_count"
                ],
                0,
            )
            self.assertFalse(metadata["external_hard_negative_reaudit_scored"])
            self.assertFalse(metadata["clean_heldout_performance_claim_permitted"])
            self.assertEqual(screen["rows"][0]["review_only_feature_score"], 0.0)

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
            self.assertEqual(
                audit["metadata"]["artifact_lineage"]["method"],
                "label_scaling_quality_cli_lineage_validation",
            )
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

    def test_audit_label_scaling_quality_rejects_mixed_slice_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            required_paths = {
                "acceptance": root / "v3_label_batch_acceptance_check_650.json",
                "readiness": root / "v3_label_preview_promotion_readiness_675.json",
                "review_debt": root / "v3_review_debt_summary_650_preview.json",
                "review_evidence_gaps": root / "v3_review_evidence_gaps_650_preview.json",
                "active_learning_queue": root / "v3_active_learning_review_queue_650.json",
                "family_propagation_guardrails": root / "v3_family_propagation_guardrails_650.json",
                "hard_negatives": root / "v3_hard_negative_controls_650.json",
            }
            for path in required_paths.values():
                path.write_text(json.dumps({"metadata": {}}), encoding="utf-8")
            out = root / "audit.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-label-scaling-quality",
                    "--acceptance",
                    str(required_paths["acceptance"]),
                    "--readiness",
                    str(required_paths["readiness"]),
                    "--review-debt",
                    str(required_paths["review_debt"]),
                    "--review-evidence-gaps",
                    str(required_paths["review_evidence_gaps"]),
                    "--active-learning-queue",
                    str(required_paths["active_learning_queue"]),
                    "--family-propagation-guardrails",
                    str(required_paths["family_propagation_guardrails"]),
                    "--hard-negatives",
                    str(required_paths["hard_negatives"]),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "mismatched label-scaling quality artifact lineage",
                result.stderr,
            )
            self.assertFalse(out.exists())

    def test_check_label_batch_acceptance_rejects_mixed_slice_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            evaluation = root / "v3_geometry_label_eval_650.json"
            hard_negatives = root / "v3_hard_negative_controls_650.json"
            in_scope_failures = root / "v3_in_scope_failure_analysis_675.json"
            label_factory_gate = root / "v3_label_factory_gate_check_650.json"
            for path in (
                evaluation,
                hard_negatives,
                in_scope_failures,
                label_factory_gate,
            ):
                path.write_text(json.dumps({"metadata": {}}), encoding="utf-8")
            out = root / "acceptance.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "check-label-batch-acceptance",
                    "--review-state-labels",
                    str(root / "v3_imported_labels_batch_650.json"),
                    "--countable-labels",
                    str(root / "v3_countable_labels_batch_650.json"),
                    "--evaluation",
                    str(evaluation),
                    "--hard-negatives",
                    str(hard_negatives),
                    "--in-scope-failures",
                    str(in_scope_failures),
                    "--label-factory-gate",
                    str(label_factory_gate),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "mismatched label-batch acceptance artifact lineage",
                result.stderr,
            )
            self.assertFalse(out.exists())

    def test_external_blocker_matrix_rejects_mixed_slice_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = {
                "candidate_manifest": (
                    root / "v3_external_source_candidate_manifest_1025.json"
                ),
                "external_import_readiness_audit": (
                    root
                    / "v3_external_source_import_readiness_audit_1025.json"
                ),
                "active_site_sourcing_export": (
                    root
                    / "v3_external_source_active_site_sourcing_export_1025.json"
                ),
                "sequence_search_export": (
                    root / "v3_external_source_sequence_search_export_1025.json"
                ),
                "representation_backend_plan": (
                    root
                    / "v3_external_source_representation_backend_plan_1000.json"
                ),
                "active_site_sourcing_resolution": (
                    root
                    / "v3_external_source_active_site_sourcing_resolution_1025.json"
                ),
                "representation_backend_sample": (
                    root
                    / "v3_external_source_representation_backend_sample_1025.json"
                ),
            }
            for name, path in paths.items():
                slice_id = 1000 if name == "representation_backend_plan" else 1025
                path.write_text(
                    json.dumps(
                        {
                            "metadata": {
                                "method": name,
                                "source_slice_id": slice_id,
                            },
                            "rows": [],
                        }
                    ),
                    encoding="utf-8",
                )
            out = root / "matrix.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-transfer-blocker-matrix",
                    "--candidate-manifest",
                    str(paths["candidate_manifest"]),
                    "--external-import-readiness-audit",
                    str(paths["external_import_readiness_audit"]),
                    "--active-site-sourcing-export",
                    str(paths["active_site_sourcing_export"]),
                    "--sequence-search-export",
                    str(paths["sequence_search_export"]),
                    "--representation-backend-plan",
                    str(paths["representation_backend_plan"]),
                    "--active-site-sourcing-resolution",
                    str(paths["active_site_sourcing_resolution"]),
                    "--representation-backend-sample",
                    str(paths["representation_backend_sample"]),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "mismatched external transfer artifact lineage",
                result.stderr,
            )
            self.assertFalse(out.exists())

    def test_external_import_readiness_rejects_mixed_slice_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = {
                "candidate_manifest": (
                    root / "v3_external_source_candidate_manifest_1025.json"
                ),
                "active_site_evidence_sample": (
                    root / "v3_external_source_active_site_evidence_sample_1025.json"
                ),
                "heuristic_control_scores": (
                    root / "v3_external_source_heuristic_control_scores_1025.json"
                ),
                "representation_control_comparison": (
                    root
                    / "v3_external_source_representation_control_comparison_1000.json"
                ),
                "active_site_gap_source_requests": (
                    root
                    / "v3_external_source_active_site_gap_source_requests_1025.json"
                ),
                "sequence_neighborhood_sample": (
                    root / "v3_external_source_sequence_neighborhood_sample_1025.json"
                ),
                "sequence_alignment_verification": (
                    root
                    / "v3_external_source_sequence_alignment_verification_1025.json"
                ),
            }
            for name, path in paths.items():
                slice_id = 1000 if name == "representation_control_comparison" else 1025
                path.write_text(
                    json.dumps(
                        {
                            "metadata": {
                                "method": name,
                                "source_slice_id": slice_id,
                            },
                            "rows": [],
                        }
                    ),
                    encoding="utf-8",
                )
            out = root / "import_readiness.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-external-source-import-readiness",
                    "--candidate-manifest",
                    str(paths["candidate_manifest"]),
                    "--active-site-evidence-sample",
                    str(paths["active_site_evidence_sample"]),
                    "--heuristic-control-scores",
                    str(paths["heuristic_control_scores"]),
                    "--representation-control-comparison",
                    str(paths["representation_control_comparison"]),
                    "--active-site-gap-source-requests",
                    str(paths["active_site_gap_source_requests"]),
                    "--sequence-neighborhood-sample",
                    str(paths["sequence_neighborhood_sample"]),
                    "--sequence-alignment-verification",
                    str(paths["sequence_alignment_verification"]),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "mismatched external transfer artifact lineage",
                result.stderr,
            )
            self.assertFalse(out.exists())

    def test_build_external_pilot_packet_rejects_mixed_slice_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = {
                "pilot_candidate_priority": (
                    root / "v3_external_source_pilot_candidate_priority_1025.json"
                ),
                "active_site_sourcing_export": (
                    root / "v3_external_source_active_site_sourcing_export_1000.json"
                ),
                "sequence_search_export": (
                    root / "v3_external_source_sequence_search_export_1025.json"
                ),
            }
            for name, path in paths.items():
                slice_id = 1000 if name == "active_site_sourcing_export" else 1025
                path.write_text(
                    json.dumps(
                        {
                            "metadata": {
                                "method": name,
                                "source_slice_id": slice_id,
                            },
                            "rows": [],
                        }
                    ),
                    encoding="utf-8",
                )
            out = root / "packet.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-pilot-evidence-packet",
                    "--pilot-candidate-priority",
                    str(paths["pilot_candidate_priority"]),
                    "--active-site-sourcing-export",
                    str(paths["active_site_sourcing_export"]),
                    "--sequence-search-export",
                    str(paths["sequence_search_export"]),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "mismatched external transfer artifact lineage",
                result.stderr,
            )
            self.assertFalse(out.exists())

    def test_build_external_pilot_dossiers_rejects_mixed_slice_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = {
                "pilot_evidence_packet": (
                    root / "v3_external_source_pilot_evidence_packet_1025.json"
                ),
                "active_site_evidence_sample": (
                    root / "v3_external_source_active_site_evidence_sample_1000.json"
                ),
                "active_site_sourcing_resolution": (
                    root
                    / "v3_external_source_active_site_sourcing_resolution_1025.json"
                ),
                "reaction_evidence_sample": (
                    root / "v3_external_source_reaction_evidence_sample_1025.json"
                ),
                "sequence_alignment_verification": (
                    root
                    / "v3_external_source_sequence_alignment_verification_1025.json"
                ),
                "representation_backend_sample": (
                    root
                    / "v3_external_source_pilot_representation_backend_sample_1025.json"
                ),
                "heuristic_control_scores": (
                    root / "v3_external_source_heuristic_control_scores_1025.json"
                ),
                "structure_mapping_sample": (
                    root / "v3_external_source_structure_mapping_sample_1025.json"
                ),
                "transfer_blocker_matrix": (
                    root / "v3_external_source_transfer_blocker_matrix_1025.json"
                ),
                "external_import_readiness_audit": (
                    root
                    / "v3_external_source_import_readiness_audit_1025.json"
                ),
            }
            for name, path in paths.items():
                slice_id = 1000 if name == "active_site_evidence_sample" else 1025
                path.write_text(
                    json.dumps(
                        {
                            "metadata": {
                                "method": name,
                                "source_slice_id": slice_id,
                            },
                            "rows": [],
                        }
                    ),
                    encoding="utf-8",
                )
            out = root / "dossiers.json"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-pilot-evidence-dossiers",
                    "--pilot-evidence-packet",
                    str(paths["pilot_evidence_packet"]),
                    "--active-site-evidence-sample",
                    str(paths["active_site_evidence_sample"]),
                    "--active-site-sourcing-resolution",
                    str(paths["active_site_sourcing_resolution"]),
                    "--reaction-evidence-sample",
                    str(paths["reaction_evidence_sample"]),
                    "--sequence-alignment-verification",
                    str(paths["sequence_alignment_verification"]),
                    "--representation-backend-sample",
                    str(paths["representation_backend_sample"]),
                    "--heuristic-control-scores",
                    str(paths["heuristic_control_scores"]),
                    "--structure-mapping-sample",
                    str(paths["structure_mapping_sample"]),
                    "--transfer-blocker-matrix",
                    str(paths["transfer_blocker_matrix"]),
                    "--external-import-readiness-audit",
                    str(paths["external_import_readiness_audit"]),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "mismatched external transfer artifact lineage",
                result.stderr,
            )
            self.assertFalse(out.exists())

    def test_build_external_pilot_active_site_decisions_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            paths = {
                "pilot_evidence_dossiers": (
                    root / "v3_external_source_pilot_evidence_dossiers_1025.json"
                ),
                "pilot_evidence_packet": (
                    root / "v3_external_source_pilot_evidence_packet_1025.json"
                ),
                "active_site_sourcing_resolution": (
                    root
                    / "v3_external_source_active_site_sourcing_resolution_1025.json"
                ),
                "reaction_evidence_sample": (
                    root / "v3_external_source_reaction_evidence_sample_1025.json"
                ),
                "backend_sequence_search": (
                    root / "v3_external_source_backend_sequence_search_1025.json"
                ),
                "pilot_representation_backend_sample": (
                    root
                    / "v3_external_source_pilot_representation_backend_sample_1025.json"
                ),
                "transfer_blocker_matrix": (
                    root / "v3_external_source_transfer_blocker_matrix_1025.json"
                ),
            }
            payloads = {
                "pilot_evidence_dossiers": {
                    "metadata": {
                        "method": "external_source_pilot_evidence_dossier",
                        "source_slice_id": 1025,
                    },
                    "rows": [
                        {
                            "rank": 1,
                            "accession": "P12345",
                            "entry_id": "uniprot:P12345",
                            "lane_id": "external_source:lyase",
                            "active_site_evidence": {
                                "explicit_active_site_feature_count": 1,
                                "binding_site_feature_count": 0,
                            },
                            "reaction_evidence": {
                                "reaction_record_count": 1,
                                "specific_reaction_record_count": 1,
                                "rhea_ids": ["RHEA:1"],
                            },
                            "sequence_evidence": {
                                "backend_search_complete": True,
                                "backend_search_status": "no_near_duplicate_signal",
                            },
                            "representation_control": {
                                "backend_status": (
                                    "learned_representation_sample_complete"
                                ),
                                "comparison_status": (
                                    "pilot_sequence_embedding_control"
                                ),
                            },
                            "remaining_blockers": [
                                "external_review_decision_artifact_not_built"
                            ],
                        }
                    ],
                },
                "pilot_evidence_packet": {
                    "metadata": {
                        "method": "external_source_pilot_evidence_packet",
                        "source_slice_id": 1025,
                    },
                    "rows": [
                        {
                            "accession": "P12345",
                            "pilot_selection_status": "selected_for_review_pilot",
                        }
                    ],
                },
                "active_site_sourcing_resolution": {
                    "metadata": {
                        "method": "external_source_active_site_sourcing_resolution",
                        "source_slice_id": 1025,
                    },
                    "rows": [],
                },
                "reaction_evidence_sample": {
                    "metadata": {
                        "method": "external_source_reaction_evidence_sample",
                        "source_slice_id": 1025,
                    },
                    "rows": [],
                },
                "backend_sequence_search": {
                    "metadata": {
                        "method": "external_source_backend_sequence_search",
                        "source_slice_id": 1025,
                    },
                    "rows": [
                        {
                            "accession": "P12345",
                            "backend_name": "mmseqs2_easy_search",
                            "backend_search_complete": True,
                            "search_status": "no_near_duplicate_signal",
                        }
                    ],
                },
                "pilot_representation_backend_sample": {
                    "metadata": {
                        "method": "external_source_representation_backend_sample",
                        "source_slice_id": 1025,
                    },
                    "rows": [
                        {
                            "accession": "P12345",
                            "backend_status": (
                                "learned_representation_sample_complete"
                            ),
                            "comparison_status": (
                                "pilot_sequence_embedding_control"
                            ),
                        }
                    ],
                },
                "transfer_blocker_matrix": {
                    "metadata": {
                        "method": "external_source_transfer_blocker_matrix",
                        "source_slice_id": 1025,
                    },
                    "rows": [{"accession": "P12345", "blockers": []}],
                },
            }
            for name, path in paths.items():
                path.write_text(json.dumps(payloads[name]), encoding="utf-8")
            out = root / "decisions.json"

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-pilot-active-site-evidence-decisions",
                    "--pilot-evidence-dossiers",
                    str(paths["pilot_evidence_dossiers"]),
                    "--pilot-evidence-packet",
                    str(paths["pilot_evidence_packet"]),
                    "--active-site-sourcing-resolution",
                    str(paths["active_site_sourcing_resolution"]),
                    "--reaction-evidence-sample",
                    str(paths["reaction_evidence_sample"]),
                    "--backend-sequence-search",
                    str(paths["backend_sequence_search"]),
                    "--pilot-representation-backend-sample",
                    str(paths["pilot_representation_backend_sample"]),
                    "--transfer-blocker-matrix",
                    str(paths["transfer_blocker_matrix"]),
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
            self.assertEqual(
                payload["metadata"]["method"],
                "external_source_pilot_active_site_evidence_decisions",
            )
            self.assertEqual(
                payload["metadata"]["artifact_lineage"]["blocker_removed"],
                "external_pilot_active_site_source_status_ambiguity",
            )
            self.assertEqual(payload["metadata"]["candidate_count"], 1)
            self.assertEqual(payload["metadata"]["countable_label_candidate_count"], 0)
            self.assertFalse(payload["metadata"]["ready_for_label_import"])
            self.assertEqual(
                payload["rows"][0]["active_site_evidence_decision_status"],
                "explicit_active_site_source_present",
            )

    def test_next_candidate_factory_import_gate_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            terminal = root / "v3_external_hard_negative_next_candidate_terminal_review_decisions_1025.json"
            label_gate = root / "v3_label_factory_gate_check_1025_preview.json"
            transfer_gate = root / "v3_external_source_transfer_gate_check_1025.json"
            labels = root / "curated_mechanism_labels.json"
            out = root / "v3_external_hard_negative_next_candidate_factory_import_gate_1025.json"
            terminal.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": (
                                "external_hard_negative_next_candidate_terminal_"
                                "review_decisions"
                            )
                        },
                        "rows": [
                            {
                                "accession": "PLOW",
                                "entry_id": "uniprot:PLOW",
                                "lane_id": "external_source:lyase",
                                "target_label_type": "out_of_scope",
                                "target_fingerprint_id": None,
                                "ontology_version_at_decision": (
                                    "label_factory_v1_8fp"
                                ),
                                "terminal_review_decision_status": (
                                    "accepted_out_of_scope_pending_factory_gate"
                                ),
                                "source_evidence_status": (
                                    "explicit_active_site_and_catalytic_activity_"
                                    "source_present"
                                ),
                                "bounded_duplicate_evidence_status": (
                                    "bounded_duplicate_controls_clear_uniref_pending"
                                ),
                                "uniref_current_reference_screen_status": (
                                    "uniref_current_reference_screen_no_current_"
                                    "reference_overlap"
                                ),
                                "remaining_import_blockers": [
                                    "full_label_factory_gate_not_run"
                                ],
                                "out_of_scope_inverse_gate": {
                                    "target_fingerprint_id": None,
                                    "inverse_gate_status": "passed",
                                    "all_current_fingerprint_scores_below_threshold": True,
                                    "observed_current_fingerprint_count": 8,
                                    "expected_current_fingerprint_count": 8,
                                    "max_current_fingerprint_score": 0.2,
                                },
                                "max_current_fingerprint_score": 0.2,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            label_gate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "label_factory_gate_check",
                            "gate_count": 21,
                            "passed_gate_count": 21,
                        },
                        "blockers": [],
                    }
                ),
                encoding="utf-8",
            )
            transfer_gate.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "method": "external_source_transfer_gate_check",
                            "gate_count": 68,
                            "passed_gate_count": 68,
                        },
                        "blockers": [],
                    }
                ),
                encoding="utf-8",
            )
            labels.write_text("[]", encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-hard-negative-next-candidate-factory-import-gate",
                    "--terminal-review-decisions",
                    str(terminal),
                    "--label-factory-gate-check",
                    str(label_gate),
                    "--external-transfer-gate",
                    str(transfer_gate),
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
            self.assertEqual(
                payload["metadata"]["method"],
                "external_hard_negative_next_candidate_factory_import_gate",
            )
            self.assertEqual(payload["metadata"]["selected_import_accessions"], ["PLOW"])
            self.assertEqual(payload["metadata"]["import_ready_candidate_count"], 1)
            self.assertEqual(
                payload["review_items"][0]["decision"]["action"], "accept_label"
            )

    def test_external_transfer_gate_help_exposes_pilot_active_site_input(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "catalytic_earth.cli",
                "check-external-source-transfer-gates",
                "--help",
            ],
            cwd=ROOT,
            env={"PYTHONPATH": str(ROOT / "src")},
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("--pilot-active-site-evidence-decisions", result.stdout)

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
