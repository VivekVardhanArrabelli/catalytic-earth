from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
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
                            "new_review_debt_entry_ids": ["m_csa:651"],
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
                        "rows": [{"entry_id": "m_csa:651", "top1_ontology_family": "heme_redox"}],
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
            self.assertIn("accepted_new_labels_without_review_debt", audit["blockers"])
            self.assertEqual(
                audit["metadata"]["near_duplicate_audit_status"],
                "not_observed_in_sequence_cluster_artifact",
            )

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
            self.assertEqual(json.loads(slice_summary.read_text())["metadata"]["largest_slice"], "650")
            self.assertGreater(json.loads(calibration.read_text())["metadata"]["threshold_count"], 21)


if __name__ == "__main__":
    unittest.main()
