from __future__ import annotations

from copy import deepcopy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.labels import (
    MechanismLabel,
    analyze_cofactor_abstention_policy,
    analyze_cofactor_coverage,
    analyze_geometry_score_margins,
    analyze_in_scope_failures,
    analyze_review_debt_remediation,
    analyze_review_evidence_gaps,
    analyze_seed_family_performance,
    analyze_out_of_scope_failures,
    analyze_structure_mapping_issues,
    audit_accepted_review_debt_deferrals,
    audit_expert_label_decision_local_evidence_gaps,
    audit_expert_label_decision_repair_guardrails,
    audit_label_scaling_quality,
    audit_mechanism_ontology_gaps,
    audit_reaction_substrate_mismatches,
    audit_sequence_similarity_failure_sets,
    audit_review_debt_remap_local_leads,
    audit_structure_selection_holo_preference,
    build_active_learning_review_queue,
    build_adversarial_negative_controls,
    build_atp_phosphoryl_transfer_family_expansion,
    build_expert_label_decision_local_evidence_review_export,
    build_expert_label_decision_review_export,
    build_expert_review_export,
    build_family_propagation_guardrails,
    build_hard_negative_controls,
    build_label_expansion_candidates,
    build_label_factory_audit,
    build_provisional_review_decision_batch,
    build_reaction_substrate_mismatch_review_export,
    check_label_batch_acceptance,
    check_label_factory_gates,
    check_label_preview_promotion_readiness,
    check_label_review_resolution,
    classify_out_of_scope_failure,
    compare_threshold_policies,
    countable_benchmark_labels,
    evaluate_geometry_retrieval,
    apply_label_factory_actions,
    group_hard_negative_controls,
    import_countable_review_decisions,
    import_expert_review_decisions,
    label_summary,
    load_labels,
    migrate_label_record,
    scan_review_debt_alternate_structures,
    summarize_expert_label_decision_repair_candidates,
    summarize_expert_label_decision_local_evidence_repair_plan,
    select_threshold,
    summarize_label_factory_batches,
    summarize_review_debt,
    summarize_review_debt_remap_leads,
    summarize_review_debt_structure_selection_candidates,
    sweep_abstention_thresholds,
)


class LabelTests(unittest.TestCase):
    def test_load_labels(self) -> None:
        labels = load_labels()
        self.assertEqual(len(labels), 679)
        summary = label_summary(labels)
        self.assertGreater(summary["by_type"]["seed_fingerprint"], 0)
        self.assertGreater(summary["by_type"]["out_of_scope"], 0)
        self.assertEqual(summary["by_tier"]["bronze"], 679)
        self.assertEqual(summary["by_review_status"]["automation_curated"], 679)
        self.assertGreater(summary["mean_evidence_score"], 0)

    def test_invalid_label(self) -> None:
        with self.assertRaises(ValueError):
            MechanismLabel.from_dict(
                {
                    "entry_id": "m_csa:1",
                    "fingerprint_id": None,
                    "label_type": "seed_fingerprint",
                    "confidence": "high",
                    "rationale": "This rationale is long enough to pass length.",
                }
            )

    def test_migrate_legacy_label_record(self) -> None:
        migrated = migrate_label_record(
            {
                "entry_id": "m_csa:1",
                "fingerprint_id": None,
                "label_type": "out_of_scope",
                "confidence": "medium",
                "rationale": "Legacy label rationale long enough for migration.",
            }
        )
        self.assertEqual(migrated["tier"], "bronze")
        self.assertEqual(migrated["review_status"], "automation_curated")
        self.assertEqual(migrated["evidence_score"], 0.65)
        self.assertEqual(migrated["evidence"]["sources"], ["curator_rationale"])

    def test_ser_his_counterevidence_blocks_provisional_counting(self) -> None:
        review = {
            "metadata": {"method": "expert_review_export"},
            "review_items": [
                {
                    "entry_id": "m_csa:771",
                    "entry_name": "2-hydroxymuconate-semialdehyde hydrolase",
                    "current_label": None,
                    "queue_context": {
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "not_required",
                        "counterevidence_reasons": [
                            "ser_his_seed_missing_triad_coherence"
                        ],
                        "mechanism_text_snippets": [
                            "The active site contains a Ser, Asp, His catalytic triad."
                        ],
                        "readiness_blockers": [],
                        "top1_fingerprint_id": "ser_his_acid_hydrolase",
                        "top1_score": 0.4385,
                    },
                }
            ],
        }

        batch = build_provisional_review_decision_batch(review)
        decision = batch["review_items"][0]["decision"]

        self.assertEqual(decision["action"], "mark_needs_more_evidence")
        self.assertEqual(decision["fingerprint_id"], "ser_his_acid_hydrolase")
        self.assertIn("counterevidence remains", decision["rationale"])

    def test_evaluate_geometry_retrieval(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="example rationale long enough",
            ),
            MechanismLabel(
                entry_id="m_csa:2",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="example rationale long enough",
            ),
        ]
        retrieval = {
            "results": [
                {
                    "entry_id": "m_csa:1",
                    "top_fingerprints": [
                        {"fingerprint_id": "metal_dependent_hydrolase", "score": 0.8}
                    ],
                },
                {
                    "entry_id": "m_csa:2",
                    "entry_name": "out-of-scope example",
                    "mechanism_text_count": 1,
                    "mechanism_text_snippets": ["Out-of-scope mechanism sentence."],
                    "top_fingerprints": [
                        {"fingerprint_id": "ser_his_acid_hydrolase", "score": 0.2}
                    ],
                },
            ]
        }
        evaluation = evaluate_geometry_retrieval(retrieval, labels, abstain_threshold=0.7)
        self.assertEqual(evaluation["metadata"]["top1_accuracy_in_scope"], 1.0)
        self.assertEqual(evaluation["metadata"]["top3_retained_accuracy_in_scope"], 1.0)
        self.assertEqual(evaluation["metadata"]["in_scope_retention_rate"], 1.0)
        self.assertEqual(evaluation["metadata"]["out_of_scope_abstention_rate"], 1.0)
        self.assertEqual(evaluation["metadata"]["out_of_scope_false_non_abstentions"], 0)
        out_scope_row = next(row for row in evaluation["rows"] if row["entry_id"] == "m_csa:2")
        self.assertEqual(out_scope_row["context"]["entry_name"], "out-of-scope example")
        self.assertEqual(out_scope_row["context"]["mechanism_text_count"], 1)

        sweep = sweep_abstention_thresholds(retrieval, labels, thresholds=[0.0, 0.7, 1.0])
        self.assertEqual(sweep["metadata"]["threshold_count"], 3)
        self.assertIn("selected", sweep)
        self.assertIn("legacy_selected", sweep)
        self.assertIn("retained_top3_reference", sweep)
        self.assertEqual(sweep["metadata"]["selected_threshold"], 0.7)
        self.assertEqual(sweep["metadata"]["retained_top3_reference_threshold"], 0.7)
        self.assertEqual(sweep["metadata"]["selection_comparison"]["same_threshold"], True)
        self.assertTrue(
            sweep["metadata"]["selection_comparison"]["zero_false_preserves_retained_top3"]
        )

        auto_sweep = sweep_abstention_thresholds(retrieval, labels)
        self.assertGreater(auto_sweep["metadata"]["threshold_count"], 21)
        self.assertEqual(auto_sweep["metadata"]["selected_threshold"], 0.2001)
        self.assertEqual(
            auto_sweep["metadata"]["selection_comparison"][
                "selected_top3_retained_accuracy_in_scope_evaluable"
            ],
            1.0,
        )

        margins = analyze_geometry_score_margins(retrieval, labels)
        self.assertEqual(margins["metadata"]["min_in_scope_top1_score"], 0.8)
        self.assertEqual(margins["metadata"]["min_correct_in_scope_top1_score"], 0.8)
        self.assertEqual(margins["metadata"]["correct_in_scope_evaluable_count"], 1)
        self.assertEqual(margins["metadata"]["max_out_of_scope_top1_score"], 0.2)
        self.assertEqual(margins["metadata"]["correct_positive_score_separation_gap"], 0.6)
        self.assertEqual(margins["metadata"]["near_margin"], 0.02)
        self.assertEqual(margins["metadata"]["score_margin_boundary_count"], 2)
        self.assertTrue(
            margins["metadata"][
                "strict_threshold_exists_to_retain_all_in_scope_and_abstain_all_out_of_scope"
            ]
        )
        self.assertTrue(
            margins["metadata"][
                "strict_threshold_exists_to_retain_all_correct_top1_in_scope_and_abstain_all_out_of_scope"
            ]
        )
        self.assertEqual(margins["metadata"]["out_of_scope_entries_at_or_above_min_in_scope"], 0)
        self.assertEqual(
            margins["metadata"]["out_of_scope_entries_at_or_above_min_correct_in_scope"],
            0,
        )
        self.assertEqual(margins["conflicting_out_of_scope_against_correct_floor_rows"], [])
        self.assertEqual(margins["limiting_in_scope_rows"][0]["entry_id"], "m_csa:1")
        self.assertEqual(margins["limiting_correct_in_scope_rows"][0]["entry_id"], "m_csa:1")
        self.assertEqual(margins["limiting_out_of_scope_rows"][0]["entry_id"], "m_csa:2")
        self.assertEqual(
            margins["limiting_out_of_scope_rows"][0]["context"]["entry_name"],
            "out-of-scope example",
        )

        controls = build_hard_negative_controls(retrieval, labels)
        self.assertEqual(controls["metadata"]["hard_negative_count"], 0)
        self.assertEqual(controls["metadata"]["near_miss_count"], 0)
        self.assertEqual(controls["metadata"]["closest_below_floor_entry_id"], "m_csa:2")
        self.assertEqual(controls["metadata"]["minimum_below_floor_score_gap"], 0.6)
        self.assertEqual(controls["closest_below_floor_rows"][0]["entry_id"], "m_csa:2")
        self.assertEqual(
            controls["closest_below_floor_rows"][0]["negative_control_type"],
            "below_in_scope_floor",
        )
        self.assertEqual(controls["groups"], [])
        controls = build_hard_negative_controls(retrieval, labels, score_floor=0.1)
        self.assertEqual(controls["metadata"]["hard_negative_count"], 1)
        self.assertEqual(controls["rows"][0]["negative_control_type"], "score_overlap_with_in_scope_positive")
        self.assertIn("context", controls["rows"][0])
        self.assertEqual(controls["groups"][0]["top1_fingerprint_id"], "ser_his_acid_hydrolase")
        self.assertEqual(controls["groups"][0]["cofactor_evidence_level"], "unknown")
        self.assertEqual(controls["groups"][0]["count"], 1)

        near_miss = build_hard_negative_controls(retrieval, labels, score_floor=0.205)
        self.assertEqual(near_miss["metadata"]["hard_negative_count"], 0)
        self.assertEqual(near_miss["metadata"]["near_miss_count"], 1)
        self.assertEqual(
            near_miss["metadata"]["near_miss_top1_fingerprint_counts"],
            {"ser_his_acid_hydrolase": 1},
        )
        self.assertEqual(
            near_miss["metadata"]["near_miss_cofactor_evidence_counts"],
            {"unknown": 1},
        )
        self.assertEqual(near_miss["metadata"]["closest_near_miss_entry_id"], "m_csa:2")
        self.assertEqual(near_miss["metadata"]["closest_below_floor_entry_id"], "m_csa:2")
        self.assertEqual(
            near_miss["metadata"]["minimum_near_miss_score_gap_to_floor"],
            0.005,
        )
        self.assertEqual(near_miss["metadata"]["minimum_below_floor_score_gap"], 0.005)
        self.assertEqual(
            near_miss["near_miss_rows"][0]["negative_control_type"],
            "near_miss_below_in_scope_floor",
        )
        self.assertEqual(near_miss["near_miss_groups"][0]["count"], 1)

        expansion = build_label_expansion_candidates(
            {
                "entries": [
                    {
                        "entry_id": "m_csa:1",
                        "status": "ok",
                        "resolved_residue_count": 3,
                    },
                    {
                        "entry_id": "m_csa:3",
                        "entry_name": "candidate enzyme",
                        "mechanism_text_count": 1,
                        "mechanism_text_snippets": [
                            "Candidate mechanism text for curator review."
                        ],
                        "pdb_id": "1XYZ",
                        "status": "ok",
                        "resolved_residue_count": 3,
                        "pairwise_distances_angstrom": [{"distance": 5.0}],
                        "pocket_context": {"nearby_residue_count": 2},
                    },
                ]
            },
            {
                "results": [
                    {
                        "entry_id": "m_csa:3",
                        "top_fingerprints": [
                            {
                                "fingerprint_id": "metal_dependent_hydrolase",
                                "score": 0.6,
                                "cofactor_evidence_level": "ligand_supported",
                            }
                        ],
                    }
                ]
            },
            labels,
        )
        self.assertEqual(expansion["metadata"]["candidate_count"], 1)
        self.assertEqual(expansion["metadata"]["ready_for_label_review_count"], 1)
        self.assertEqual(expansion["metadata"]["candidate_group_count"], 1)
        self.assertEqual(expansion["rows"][0]["entry_id"], "m_csa:3")
        self.assertEqual(expansion["rows"][0]["entry_name"], "candidate enzyme")
        self.assertEqual(expansion["rows"][0]["mechanism_text_count"], 1)
        self.assertEqual(
            expansion["rows"][0]["mechanism_text_snippets"],
            ["Candidate mechanism text for curator review."],
        )
        self.assertEqual(expansion["rows"][0]["readiness_blockers"], [])
        self.assertEqual(expansion["groups"][0]["ready_entry_ids"], ["m_csa:3"])
        self.assertEqual(expansion["groups"][0]["ready_entries"][0]["entry_id"], "m_csa:3")
        self.assertEqual(
            expansion["groups"][0]["ready_entries"][0]["entry_name"],
            "candidate enzyme",
        )

        mapping_issues = analyze_structure_mapping_issues(
            {
                "entries": [
                    {"entry_id": "m_csa:1", "status": "ok"},
                    {
                        "entry_id": "m_csa:2",
                        "entry_name": "partial mapping enzyme",
                        "pdb_id": "2XYZ",
                        "status": "partial",
                        "mechanism_text_count": 1,
                        "mechanism_text_snippets": ["Mechanism context for mapping triage."],
                        "resolved_residue_count": 1,
                        "missing_positions": 2,
                        "missing_position_details": [
                            {
                                "expected_code": "MG",
                                "observed_codes_at_position": ["HOH"],
                                "resid": 401,
                            }
                        ],
                    },
                    {
                        "entry_id": "m_csa:4",
                        "pdb_id": "4XYZ",
                        "status": "no_resolved_residues",
                        "resolved_residue_count": 0,
                        "missing_positions": 3,
                    },
                ]
            },
            labels,
        )
        self.assertEqual(mapping_issues["metadata"]["issue_count"], 2)
        self.assertEqual(mapping_issues["metadata"]["labeled_issue_count"], 1)
        self.assertEqual(mapping_issues["metadata"]["status_counts"]["partial"], 1)
        self.assertEqual(mapping_issues["metadata"]["label_type_counts"]["out_of_scope"], 1)
        self.assertEqual(mapping_issues["metadata"]["label_type_counts"]["unlabeled"], 1)
        self.assertEqual(mapping_issues["metadata"]["missing_expected_code_counts"]["MG"], 1)
        self.assertEqual(
            mapping_issues["metadata"]["observed_code_at_missing_position_counts"]["HOH"],
            1,
        )
        self.assertEqual(mapping_issues["rows"][0]["entry_id"], "m_csa:2")
        self.assertEqual(mapping_issues["rows"][0]["entry_name"], "partial mapping enzyme")
        self.assertEqual(mapping_issues["rows"][0]["mechanism_text_count"], 1)
        self.assertEqual(
            mapping_issues["rows"][0]["mechanism_text_snippets"],
            ["Mechanism context for mapping triage."],
        )

    def test_analyze_seed_family_performance(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="example rationale long enough for metal family",
            ),
            MechanismLabel(
                entry_id="m_csa:2",
                fingerprint_id="flavin_dehydrogenase_reductase",
                label_type="seed_fingerprint",
                confidence="medium",
                rationale="example rationale long enough for flavin family",
            ),
            MechanismLabel(
                entry_id="m_csa:3",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="example rationale long enough for out of scope",
            ),
        ]
        retrieval = {
            "results": [
                {
                    "entry_id": "m_csa:1",
                    "status": "ok",
                    "resolved_residue_count": 3,
                    "ligand_context": {"cofactor_families": ["metal_ion"]},
                    "top_fingerprints": [
                        {"fingerprint_id": "metal_dependent_hydrolase", "score": 0.8}
                    ],
                },
                {
                    "entry_id": "m_csa:2",
                    "status": "ok",
                    "resolved_residue_count": 3,
                    "ligand_context": {},
                    "top_fingerprints": [
                        {"fingerprint_id": "flavin_dehydrogenase_reductase", "score": 0.4}
                    ],
                },
                {
                    "entry_id": "m_csa:3",
                    "status": "ok",
                    "resolved_residue_count": 3,
                    "top_fingerprints": [
                        {
                            "fingerprint_id": "metal_dependent_hydrolase",
                            "score": 0.55,
                            "cofactor_evidence_level": "role_inferred",
                        }
                    ],
                },
            ]
        }
        analysis = analyze_seed_family_performance(retrieval, labels, abstain_threshold=0.5)
        self.assertEqual(analysis["metadata"]["in_scope_family_count"], 2)
        self.assertEqual(analysis["metadata"]["out_of_scope_retained_family_count"], 1)
        metal_row = next(
            row
            for row in analysis["in_scope_families"]
            if row["fingerprint_id"] == "metal_dependent_hydrolase"
        )
        self.assertEqual(metal_row["top3_retained_accuracy_evaluable"], 1.0)
        flavin_row = next(
            row
            for row in analysis["in_scope_families"]
            if row["fingerprint_id"] == "flavin_dehydrogenase_reductase"
        )
        self.assertEqual(flavin_row["abstained_entry_ids"], ["m_csa:2"])
        out_scope_row = analysis["out_of_scope_top1_families"][0]
        self.assertEqual(out_scope_row["false_non_abstention_entry_ids"], ["m_csa:3"])

    def test_label_factory_promotes_abstains_and_demotes(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="example rationale long enough for promotion",
                evidence_score=0.85,
            ),
            MechanismLabel(
                entry_id="m_csa:2",
                fingerprint_id="flavin_dehydrogenase_reductase",
                label_type="seed_fingerprint",
                confidence="medium",
                rationale="example rationale long enough for abstention",
            ),
            MechanismLabel(
                entry_id="m_csa:3",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="example rationale long enough for out of scope",
                tier="silver",
            ),
        ]
        retrieval = {
            "results": [
                {
                    "entry_id": "m_csa:1",
                    "status": "ok",
                    "resolved_residue_count": 3,
                    "ligand_context": {"cofactor_families": ["metal_ion"]},
                    "top_fingerprints": [
                        {
                            "fingerprint_id": "metal_dependent_hydrolase",
                            "score": 0.82,
                            "cofactor_evidence_level": "ligand_supported",
                        }
                    ],
                },
                {
                    "entry_id": "m_csa:2",
                    "status": "ok",
                    "resolved_residue_count": 3,
                    "ligand_context": {},
                    "top_fingerprints": [
                        {
                            "fingerprint_id": "ser_his_acid_hydrolase",
                            "score": 0.3,
                            "cofactor_evidence_level": "not_required",
                        },
                        {
                            "fingerprint_id": "flavin_dehydrogenase_reductase",
                            "score": 0.2,
                            "cofactor_evidence_level": "absent",
                        },
                    ],
                },
                {
                    "entry_id": "m_csa:3",
                    "status": "ok",
                    "resolved_residue_count": 3,
                    "top_fingerprints": [
                        {
                            "fingerprint_id": "metal_dependent_hydrolase",
                            "score": 0.78,
                            "cofactor_evidence_level": "role_inferred",
                        }
                    ],
                },
            ]
        }
        audit = build_label_factory_audit(retrieval, labels, abstain_threshold=0.5)
        actions = {row["entry_id"]: row["recommended_action"] for row in audit["rows"]}
        tiers = {row["entry_id"]: row["proposed_tier"] for row in audit["rows"]}
        self.assertEqual(actions["m_csa:1"], "promote_to_silver")
        self.assertEqual(tiers["m_csa:1"], "silver")
        self.assertEqual(actions["m_csa:2"], "abstain_pending_evidence")
        self.assertEqual(actions["m_csa:3"], "demote_to_bronze")
        self.assertEqual(audit["metadata"]["promote_to_silver_count"], 1)
        self.assertEqual(audit["metadata"]["demote_to_bronze_count"], 1)
        applied = apply_label_factory_actions(labels, audit)
        applied_by_entry = {row["entry_id"]: row for row in applied["labels"]}
        self.assertEqual(applied_by_entry["m_csa:1"]["tier"], "silver")
        self.assertEqual(
            applied_by_entry["m_csa:2"]["review_status"],
            "needs_expert_review",
        )
        self.assertEqual(applied_by_entry["m_csa:3"]["tier"], "bronze")
        self.assertIn(
            "label_factory_audit",
            applied_by_entry["m_csa:1"]["evidence"]["sources"],
        )

    def test_active_learning_queue_and_expert_round_trip(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="example rationale long enough for existing label",
                evidence={"sources": ["curator_rationale"], "notes": ["preserve me"]},
            )
        ]
        geometry = {
            "entries": [
                {
                    "entry_id": "m_csa:1",
                    "entry_name": "existing enzyme",
                    "status": "ok",
                    "resolved_residue_count": 3,
                    "mechanism_text_snippets": ["Existing mechanism text."],
                },
                {
                    "entry_id": "m_csa:4",
                    "entry_name": "new candidate enzyme",
                    "status": "ok",
                    "resolved_residue_count": 4,
                    "mechanism_text_count": 1,
                    "mechanism_text_snippets": ["Candidate mechanism text."],
                },
            ]
        }
        retrieval = {
            "results": [
                {
                    "entry_id": "m_csa:1",
                    "entry_name": "existing enzyme",
                    "status": "ok",
                    "resolved_residue_count": 3,
                    "mechanism_text_count": 1,
                    "mechanism_text_snippets": ["Existing mechanism text."],
                    "top_fingerprints": [
                        {"fingerprint_id": "ser_his_acid_hydrolase", "score": 0.49},
                        {"fingerprint_id": "metal_dependent_hydrolase", "score": 0.48},
                    ],
                },
                {
                    "entry_id": "m_csa:4",
                    "entry_name": "new candidate enzyme",
                    "status": "ok",
                    "resolved_residue_count": 4,
                    "mechanism_text_count": 1,
                    "mechanism_text_snippets": ["Candidate mechanism text."],
                    "top_fingerprints": [
                        {
                            "fingerprint_id": "plp_dependent_enzyme",
                            "score": 0.51,
                            "cofactor_evidence_level": "ligand_supported",
                        },
                        {"fingerprint_id": "cobalamin_radical_rearrangement", "score": 0.49},
                    ],
                },
            ]
        }
        audit = build_label_factory_audit(retrieval, labels, abstain_threshold=0.5)
        queue = build_active_learning_review_queue(
            geometry,
            retrieval,
            labels,
            label_factory_audit=audit,
            abstain_threshold=0.5,
            max_rows=10,
        )
        self.assertGreaterEqual(queue["metadata"]["queued_count"], 2)
        self.assertEqual(queue["rows"][0]["rank"], 1)
        self.assertIn("uncertainty", queue["rows"][0]["review_scores"])
        self.assertIn(
            "reaction_substrate_mismatch_value",
            queue["metadata"]["ranking_terms"],
        )
        self.assertIn("reaction_substrate_mismatch_count", queue["metadata"])
        self.assertTrue(queue["metadata"]["all_unlabeled_rows_retained"])

        export = build_expert_review_export(queue, labels, max_rows=1)
        export["review_items"][0]["decision"] = {
            "action": "accept_label",
            "label_type": "seed_fingerprint",
            "fingerprint_id": "plp_dependent_enzyme",
            "tier": "gold",
            "confidence": "high",
            "reviewer": "expert-a",
            "rationale": "Expert review confirms a PLP-family mechanism for this candidate.",
            "evidence_score": 0.98,
        }
        imported = import_expert_review_decisions(labels, export)
        imported_by_entry = {label.entry_id: label for label in imported}
        reviewed = imported_by_entry[export["review_items"][0]["entry_id"]]
        self.assertEqual(reviewed.review_status, "expert_reviewed")
        self.assertEqual(reviewed.tier, "gold")
        self.assertIn("expert_review_import", reviewed.evidence["sources"])
        self.assertEqual(reviewed.evidence["expert_reviews"][0]["reviewer"], "expert-a")
        if reviewed.entry_id == "m_csa:1":
            self.assertEqual(reviewed.evidence["notes"], ["preserve me"])

        export["review_items"][0]["decision"] = {
            **export["review_items"][0]["decision"],
            "fingerprint_id": "unknown_fingerprint",
        }
        with self.assertRaises(ValueError):
            import_expert_review_decisions(labels, export)

        gates = check_label_factory_gates(
            labels,
            audit,
            None,
            queue,
            {
                "metadata": {
                    "control_count": 1,
                    "axis_counts": {"ontology_family_boundary": 1},
                }
            },
            export,
            {"metadata": {"reported_count": 1, "source_guardrails": [{"source": "local_proxy"}]}},
        )
        self.assertTrue(gates["gates"]["label_schema_explicit"])
        self.assertTrue(gates["gates"]["active_queue_ranked"])
        self.assertTrue(gates["gates"]["active_queue_retains_unlabeled_candidates"])

        truncated_queue = {
            **queue,
            "metadata": {
                **queue["metadata"],
                "all_unlabeled_rows_retained": False,
                "unlabeled_omitted_by_max_rows": 1,
            },
        }
        truncated_gates = check_label_factory_gates(
            labels,
            audit,
            None,
            truncated_queue,
            {
                "metadata": {
                    "control_count": 1,
                    "axis_counts": {"ontology_family_boundary": 1},
                }
            },
            export,
            {"metadata": {"reported_count": 1, "source_guardrails": [{"source": "local_proxy"}]}},
        )
        self.assertFalse(truncated_gates["gates"]["active_queue_retains_unlabeled_candidates"])
        self.assertIn("active_queue_retains_unlabeled_candidates", truncated_gates["blockers"])

    def test_expert_review_export_includes_underrepresented_queue_families(self) -> None:
        labels = [
            MechanismLabel(
                entry_id=f"m_csa:{index}",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="Existing label for diversity export testing.",
            )
            for index in range(1, 9)
        ]
        queue = {
            "metadata": {
                "queued_count": 8,
                "all_unlabeled_rows_retained": True,
                "ranking_terms": [
                    "uncertainty",
                    "impact",
                    "novelty",
                    "hard_negative_value",
                    "evidence_conflict",
                    "family_boundary_value",
                    "reaction_substrate_mismatch_value",
                ],
            },
            "rows": [
                {
                    "entry_id": f"m_csa:{index}",
                    "entry_name": f"hydrolase {index}",
                    "rank": index,
                    "top1_ontology_family": "hydrolysis",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                }
                for index in range(1, 7)
            ]
            + [
                {
                    "entry_id": "m_csa:7",
                    "entry_name": "flavin boundary",
                    "rank": 7,
                    "top1_ontology_family": "flavin_redox",
                    "top1_fingerprint_id": "flavin_dehydrogenase_reductase",
                },
                {
                    "entry_id": "m_csa:8",
                    "entry_name": "heme boundary",
                    "rank": 8,
                    "top1_ontology_family": "heme_redox",
                    "top1_fingerprint_id": "heme_peroxidase_oxidase",
                },
            ]
        }

        export = build_expert_review_export(queue, labels, max_rows=3)

        self.assertEqual(export["metadata"]["dominant_top1_ontology_family"], "hydrolysis")
        self.assertEqual(export["metadata"]["diversity_added_count"], 2)
        self.assertEqual(
            [item["entry_id"] for item in export["review_items"]],
            ["m_csa:1", "m_csa:2", "m_csa:3", "m_csa:7", "m_csa:8"],
        )
        self.assertEqual(
            export["metadata"]["export_top1_ontology_family_counts"],
            {"flavin_redox": 1, "heme_redox": 1, "hydrolysis": 3},
        )
        gates = check_label_factory_gates(
            labels,
            {
                "metadata": {
                    "promote_to_silver_count": 1,
                    "abstention_or_review_count": 1,
                }
            },
            {
                "metadata": {
                    "output_label_count": len(labels),
                    "output_summary": {"by_tier": {"silver": 1}},
                }
            },
            queue,
            {
                "metadata": {
                    "control_count": 1,
                    "axis_counts": {"ontology_family_boundary": 1},
                }
            },
            export,
            {"metadata": {"reported_count": 1, "source_guardrails": [{"source": "local_proxy"}]}},
        )
        self.assertTrue(gates["gates"]["expert_review_export_diversity_ready"])
        self.assertEqual(gates["metadata"]["omitted_underrepresented_queue_entry_ids"], [])

    def test_label_factory_batch_summary_tracks_review_debt_and_queue_retention(self) -> None:
        acceptance_625 = {
            "metadata": {
                "accepted_for_counting": True,
                "baseline_label_count": 579,
                "countable_label_count": 599,
                "accepted_new_label_count": 20,
                "pending_review_count": 31,
                "hard_negative_count": 0,
                "near_miss_count": 0,
                "out_of_scope_false_non_abstentions": 0,
                "actionable_in_scope_failure_count": 0,
                "factory_gate_ready": True,
            },
            "blockers": [],
        }
        acceptance_650 = {
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
        gate_650 = {
            "metadata": {
                "automation_ready_for_next_label_batch": True,
                "gate_count": 10,
                "passed_gate_count": 10,
            }
        }
        retained_queue = {
            "metadata": {
                "total_unlabeled_candidate_count": 32,
                "unlabeled_omitted_by_max_rows": 0,
                "all_unlabeled_rows_retained": True,
            }
        }
        truncated_queue = {
            "metadata": {
                "total_unlabeled_candidate_count": 32,
                "unlabeled_omitted_by_max_rows": 2,
                "all_unlabeled_rows_retained": False,
            }
        }
        scaling_audit_650 = {
            "metadata": {
                "audit_recommendation": "promotion_quality_audit_clean",
                "accepted_new_debt_count": 0,
                "unclassified_new_review_debt_entry_ids": [],
                "omitted_underrepresented_queue_entry_ids": [],
                "issue_class_counts": {},
            },
            "blockers": [],
            "review_warnings": ["sequence_cluster_artifact_missing_for_near_duplicate_audit"],
        }

        summary = summarize_label_factory_batches(
            [
                ("artifacts/v3_label_batch_acceptance_check_625.json", acceptance_625),
                ("artifacts/v3_label_batch_acceptance_check_650.json", acceptance_650),
            ],
            gate_checks=[("artifacts/v3_label_factory_gate_check_650.json", gate_650)],
            active_learning_queues=[
                ("artifacts/v3_active_learning_review_queue_650.json", retained_queue)
            ],
            scaling_quality_audits=[
                ("artifacts/v3_label_scaling_quality_audit_650.json", scaling_audit_650)
            ],
        )

        self.assertEqual(summary["metadata"]["latest_batch"], "650")
        self.assertEqual(summary["metadata"]["latest_countable_label_count"], 618)
        self.assertEqual(summary["metadata"]["latest_pending_review_count"], 37)
        self.assertEqual(summary["metadata"]["total_accepted_new_label_count"], 39)
        self.assertTrue(summary["metadata"]["all_zero_hard_negatives"])
        self.assertTrue(summary["metadata"]["all_active_queues_retain_unlabeled_candidates"])
        self.assertEqual(summary["metadata"]["scaling_quality_audit_count"], 1)
        self.assertTrue(summary["metadata"]["latest_scaling_quality_audit_present"])
        self.assertTrue(summary["metadata"]["all_supplied_scaling_quality_audits_ready"])
        self.assertEqual(
            summary["metadata"]["latest_scaling_quality_review_warnings"],
            ["sequence_cluster_artifact_missing_for_near_duplicate_audit"],
        )
        self.assertTrue(summary["rows"][-1]["scaling_quality_ready"])

        blocked = summarize_label_factory_batches(
            [("artifacts/v3_label_batch_acceptance_check_650.json", acceptance_650)],
            active_learning_queues=[
                ("artifacts/v3_active_learning_review_queue_650.json", truncated_queue)
            ],
        )
        self.assertFalse(blocked["metadata"]["all_active_queues_retain_unlabeled_candidates"])
        self.assertEqual(
            blocked["blockers"][0]["blockers"],
            ["unlabeled_rows_omitted_from_active_queue"],
        )

        blocked_audit = summarize_label_factory_batches(
            [("artifacts/v3_label_batch_acceptance_check_650.json", acceptance_650)],
            scaling_quality_audits=[
                (
                    "artifacts/v3_label_scaling_quality_audit_650.json",
                    {
                        "metadata": {
                            "audit_recommendation": "do_not_promote_until_quality_repair",
                            "accepted_new_debt_count": 1,
                            "unclassified_new_review_debt_entry_ids": [],
                            "omitted_underrepresented_queue_entry_ids": [],
                            "issue_class_counts": {"text_leakage_risk": 1},
                        },
                        "blockers": ["accepted_new_labels_have_unresolved_review_debt"],
                    },
                )
            ],
        )
        self.assertFalse(blocked_audit["rows"][0]["scaling_quality_ready"])
        self.assertIn("scaling_quality_audit_not_ready", blocked_audit["blockers"][0]["blockers"])

    def test_label_batch_acceptance_blocks_new_countable_review_gap(self) -> None:
        baseline = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="Baseline label is already countable.",
            )
        ]
        new_label = MechanismLabel(
            entry_id="m_csa:2",
            fingerprint_id="metal_dependent_hydrolase",
            label_type="seed_fingerprint",
            confidence="medium",
            rationale="New label should be blocked by review-gap evidence.",
        )
        check = check_label_batch_acceptance(
            baseline_labels=baseline,
            review_state_labels=baseline + [new_label],
            countable_labels=baseline + [new_label],
            evaluation={"metadata": {"out_of_scope_false_non_abstentions": 0}},
            hard_negatives={"metadata": {"hard_negative_count": 0, "near_miss_count": 0}},
            in_scope_failures={"metadata": {"actionable_failure_count": 0}},
            label_factory_gate={"metadata": {"automation_ready_for_next_label_batch": True}},
            review_evidence_gaps={
                "rows": [
                    {
                        "entry_id": "m_csa:2",
                        "decision_action": "mark_needs_more_evidence",
                        "gap_reasons": ["expected_cofactor_absent_from_structure"],
                    }
                ]
            },
        )

        self.assertFalse(check["metadata"]["accepted_for_counting"])
        self.assertEqual(check["metadata"]["accepted_new_label_entry_ids"], ["m_csa:2"])
        self.assertEqual(check["metadata"]["accepted_review_gap_entry_ids"], ["m_csa:2"])
        self.assertIn("accepted_labels_have_no_review_evidence_gaps", check["blockers"])

    def test_label_batch_acceptance_blocks_reaction_substrate_mismatch(self) -> None:
        baseline = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="Baseline label is already countable.",
            )
        ]
        new_label = MechanismLabel(
            entry_id="m_csa:2",
            fingerprint_id="metal_dependent_hydrolase",
            label_type="seed_fingerprint",
            confidence="medium",
            rationale="New label should be blocked by reaction mismatch evidence.",
        )
        check = check_label_batch_acceptance(
            baseline_labels=baseline,
            review_state_labels=baseline + [new_label],
            countable_labels=baseline + [new_label],
            evaluation={"metadata": {"out_of_scope_false_non_abstentions": 0}},
            hard_negatives={"metadata": {"hard_negative_count": 0, "near_miss_count": 0}},
            in_scope_failures={"metadata": {"actionable_failure_count": 0}},
            label_factory_gate={"metadata": {"automation_ready_for_next_label_batch": True}},
            review_evidence_gaps={
                "rows": [
                    {
                        "entry_id": "m_csa:2",
                        "entry_name": "glucokinase-like accepted label",
                        "decision_action": "accept_label",
                        "top1_fingerprint_id": "metal_dependent_hydrolase",
                        "mechanism_text_snippets": [
                            "Glucose attacks the gamma phosphorous of ATP."
                        ],
                    }
                ]
            },
        )

        self.assertFalse(check["metadata"]["accepted_for_counting"])
        self.assertEqual(
            check["metadata"]["accepted_reaction_substrate_mismatch_entry_ids"],
            ["m_csa:2"],
        )
        self.assertIn(
            "accepted_labels_have_no_reaction_substrate_mismatches",
            check["blockers"],
        )

    def test_review_debt_summary_prioritizes_cofactor_and_boundary_gaps(self) -> None:
        gaps = {
            "metadata": {"method": "review_evidence_gap_analysis"},
            "rows": [
                {
                    "entry_id": "m_csa:650",
                    "entry_name": "phospholipase A1",
                    "decision_action": "mark_needs_more_evidence",
                    "coverage_status": "expected_structure_only",
                    "gap_reasons": [
                        "review_marked_needs_more_evidence",
                        "counterevidence_present",
                        "target_not_top1",
                    ],
                    "counterevidence_reasons": ["metal_boundary_without_text"],
                    "target_fingerprint_id": "ser_his_acid_hydrolase",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_score": 0.61,
                    "target_score": 0.58,
                },
                {
                    "entry_id": "m_csa:494",
                    "entry_name": "cobalamin candidate",
                    "decision_action": "mark_needs_more_evidence",
                    "coverage_status": "expected_absent_from_structure",
                    "gap_reasons": [
                        "review_marked_needs_more_evidence",
                        "expected_cofactor_absent_from_structure",
                    ],
                    "counterevidence_reasons": [],
                    "target_fingerprint_id": "cobalamin_radical_rearrangement",
                    "top1_fingerprint_id": "cobalamin_radical_rearrangement",
                    "top1_score": 0.3,
                    "target_score": 0.3,
                },
            ],
        }
        queue = {
            "rows": [
                {"entry_id": "m_csa:650", "rank": 1, "review_score": 8.0},
                {"entry_id": "m_csa:494", "rank": 40, "review_score": 5.0},
            ]
        }

        summary = summarize_review_debt(gaps, active_learning_queue=queue, max_rows=2)

        self.assertEqual(summary["metadata"]["review_debt_count"], 2)
        self.assertEqual(summary["metadata"]["review_debt_entry_ids"], ["m_csa:494", "m_csa:650"])
        self.assertEqual(summary["metadata"]["active_queue_rows_linked"], 2)
        self.assertEqual(summary["rows"][0]["entry_id"], "m_csa:650")
        self.assertEqual(
            summary["rows"][0]["recommended_next_action"],
            "verify_local_cofactor_or_active_site_mapping",
        )
        self.assertIn("counterevidence_present", summary["metadata"]["gap_reason_counts"])

        with_baseline = summarize_review_debt(
            gaps,
            active_learning_queue=queue,
            baseline_review_debt={"rows": [{"entry_id": "m_csa:494"}]},
            max_rows=2,
        )
        self.assertEqual(with_baseline["metadata"]["debt_status_counts"]["carried"], 1)
        self.assertEqual(with_baseline["metadata"]["debt_status_counts"]["new"], 1)
        self.assertEqual(with_baseline["metadata"]["carried_review_debt_entry_ids"], ["m_csa:494"])
        self.assertEqual(with_baseline["metadata"]["new_review_debt_entry_ids"], ["m_csa:650"])
        self.assertEqual(
            with_baseline["metadata"]["recommended_next_action_counts_by_debt_status"]["carried"],
            {"inspect_alternate_structure_or_cofactor_source": 1},
        )
        self.assertEqual(
            with_baseline["metadata"]["recommended_next_action_counts_by_debt_status"]["new"],
            {"verify_local_cofactor_or_active_site_mapping": 1},
        )
        self.assertEqual(with_baseline["rows"][0]["debt_status"], "new")

    def test_review_debt_remediation_keeps_all_new_rows_inspectable(self) -> None:
        review_debt = {
            "metadata": {
                "method": "review_debt_summary",
                "review_debt_entry_ids": ["m_csa:650", "m_csa:651"],
                "new_review_debt_entry_ids": ["m_csa:650", "m_csa:651"],
                "carried_review_debt_entry_ids": [],
            },
            "rows": [
                {
                    "entry_id": "m_csa:650",
                    "priority_score": 7.0,
                    "recommended_next_action": "verify_local_cofactor_or_active_site_mapping",
                    "debt_status": "new",
                }
            ],
        }
        gaps = {
            "metadata": {"method": "review_evidence_gap_analysis"},
            "rows": [
                {
                    "entry_id": "m_csa:650",
                    "entry_name": "phospholipase A1",
                    "decision_action": "mark_needs_more_evidence",
                    "coverage_status": "expected_structure_only",
                    "gap_reasons": ["expected_cofactor_not_local"],
                    "expected_cofactor_families": ["metal_ion"],
                    "local_cofactor_families": [],
                    "structure_cofactor_families": ["metal_ion"],
                    "target_fingerprint_id": "ser_his_acid_hydrolase",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                },
                {
                    "entry_id": "m_csa:651",
                    "entry_name": "flavin gap",
                    "decision_action": "mark_needs_more_evidence",
                    "coverage_status": "expected_absent_from_structure",
                    "gap_reasons": ["expected_cofactor_absent_from_structure"],
                    "expected_cofactor_families": ["flavin"],
                    "local_cofactor_families": [],
                    "structure_cofactor_families": [],
                    "target_fingerprint_id": "flavin_dehydrogenase_reductase",
                    "top1_fingerprint_id": "flavin_dehydrogenase_reductase",
                },
            ],
        }
        graph = {
            "nodes": [
                {"id": "pdb:1AAA", "type": "structure", "structure_source": "pdb", "structure_id": "1AAA"},
                {"id": "pdb:2BBB", "type": "structure", "structure_source": "pdb", "structure_id": "2BBB"},
                {"id": "pdb:3CCC", "type": "structure", "structure_source": "pdb", "structure_id": "3CCC"},
                {"id": "pdb:4DDD", "type": "structure", "structure_source": "pdb", "structure_id": "4DDD"},
                {"id": "alphafold:P651", "type": "structure", "structure_source": "alphafold_db", "structure_id": "P651"},
                {
                    "id": "m_csa:651:residue:1",
                    "type": "catalytic_residue",
                    "structure_positions": [{"pdb_id": "3CCC"}, {"pdb_id": "4DDD"}],
                },
                {
                    "id": "m_csa:651:residue:2",
                    "type": "catalytic_residue",
                    "structure_positions": [{"pdb_id": "3CCC"}],
                },
            ],
            "edges": [
                {"source": "m_csa:650", "target": "uniprot:P650", "predicate": "has_reference_protein"},
                {"source": "uniprot:P650", "target": "pdb:1AAA", "predicate": "has_structure"},
                {"source": "uniprot:P650", "target": "pdb:2BBB", "predicate": "has_structure"},
                {"source": "m_csa:651", "target": "uniprot:P651", "predicate": "has_reference_protein"},
                {"source": "uniprot:P651", "target": "pdb:3CCC", "predicate": "has_structure"},
                {"source": "uniprot:P651", "target": "pdb:4DDD", "predicate": "has_structure"},
                {"source": "uniprot:P651", "target": "alphafold:P651", "predicate": "has_structure"},
            ],
        }
        geometry = {
            "entries": [
                {"entry_id": "m_csa:650", "pdb_id": "1AAA", "status": "ok"},
                {"entry_id": "m_csa:651", "pdb_id": "3CCC", "status": "ok"},
            ]
        }

        plan = analyze_review_debt_remediation(
            review_debt,
            gaps,
            graph=graph,
            geometry=geometry,
            debt_status="new",
        )

        self.assertEqual(plan["metadata"]["method"], "review_debt_remediation_plan")
        self.assertEqual(plan["metadata"]["requested_entry_count"], 2)
        self.assertEqual(plan["metadata"]["emitted_row_count"], 2)
        self.assertTrue(plan["metadata"]["all_requested_entries_have_gap_detail"])
        rows_by_entry = {row["entry_id"]: row for row in plan["rows"]}
        self.assertEqual(
            rows_by_entry["m_csa:650"]["remediation_bucket"],
            "local_mapping_or_structure_selection_review",
        )
        self.assertEqual(
            rows_by_entry["m_csa:651"]["remediation_bucket"],
            "alternate_pdb_ligand_scan",
        )
        self.assertEqual(rows_by_entry["m_csa:651"]["alternate_pdb_ids"], ["4DDD"])
        self.assertEqual(rows_by_entry["m_csa:651"]["alphafold_structure_ids"], ["P651"])
        self.assertEqual(rows_by_entry["m_csa:651"]["selected_pdb_residue_position_count"], 2)
        self.assertEqual(
            rows_by_entry["m_csa:651"]["alternate_pdb_residue_position_counts"],
            {"4DDD": 1},
        )
        self.assertEqual(
            plan["metadata"]["remediation_bucket_counts"]["alternate_pdb_ligand_scan"],
            1,
        )
        self.assertEqual(plan["metadata"]["alternate_pdb_position_gap_entry_ids"], ["m_csa:650"])

    def test_review_debt_alternate_structure_scan_records_expected_family_hits(self) -> None:
        remediation = {
            "metadata": {"method": "review_debt_remediation_plan"},
            "rows": [
                {
                    "entry_id": "m_csa:651",
                    "entry_name": "flavin gap",
                    "remediation_bucket": "alternate_pdb_ligand_scan",
                    "expected_cofactor_families": ["flavin"],
                    "selected_pdb_id": "1AAA",
                    "alternate_pdb_ids": ["2BBB", "3CCC"],
                    "candidate_pdb_structure_ids": ["1AAA", "2BBB", "3CCC"],
                }
            ],
        }

        scan = scan_review_debt_alternate_structures(
            remediation,
            max_entries=1,
            max_structures_per_entry=2,
            inventory_by_pdb={
                "1AAA": {"ligand_codes": ["SO4"], "cofactor_families": []},
                "2BBB": {"ligand_codes": ["FAD"], "cofactor_families": ["flavin"]},
            },
        )

        self.assertEqual(scan["metadata"]["method"], "review_debt_alternate_structure_scan")
        self.assertEqual(scan["metadata"]["scanned_entry_count"], 1)
        self.assertEqual(scan["metadata"]["scanned_structure_count"], 2)
        self.assertEqual(scan["metadata"]["expected_family_hit_entry_ids"], ["m_csa:651"])
        self.assertEqual(scan["metadata"]["local_expected_family_hit_entry_ids"], [])
        self.assertEqual(
            scan["metadata"]["structure_wide_hit_without_local_support_entry_ids"],
            ["m_csa:651"],
        )
        row = scan["rows"][0]
        self.assertEqual(row["scanned_pdb_ids"], ["1AAA", "2BBB"])
        self.assertEqual(row["unscanned_pdb_ids"], ["3CCC"])
        self.assertTrue(row["alternate_structure_expected_family_observed"])
        self.assertEqual(
            row["scan_outcome"],
            "alternate_structure_has_expected_cofactor_candidate",
        )

    def test_review_debt_alternate_structure_scan_records_local_hits(self) -> None:
        cif_text = """data_test
#
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.auth_atom_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_seq_id
ATOM 1 N N ASP A 7 0.0 0.0 0.0 N ASP A 7
ATOM 2 C CA ASP A 7 1.0 0.0 0.0 CA ASP A 7
HETATM 3 N N1 FAD A 900 1.5 0.0 0.0 N1 FAD A 900
#
"""
        remediation = {
            "metadata": {"method": "review_debt_remediation_plan"},
            "rows": [
                {
                    "entry_id": "m_csa:652",
                    "entry_name": "local flavin gap",
                    "remediation_bucket": "local_mapping_or_structure_selection_review",
                    "expected_cofactor_families": ["flavin"],
                    "selected_pdb_id": "2BBB",
                    "alternate_pdb_ids": [],
                    "candidate_pdb_structure_ids": ["2BBB"],
                    "candidate_pdb_residue_position_counts": {"2BBB": 1},
                    "candidate_pdb_residue_positions": {
                        "2BBB": [
                            {
                                "chain_name": "A",
                                "resid": 7,
                                "code": "ASP",
                                "residue_node_id": "m_csa:652:residue:1",
                            }
                        ]
                    },
                }
            ],
        }

        scan = scan_review_debt_alternate_structures(
            remediation,
            max_entries=1,
            max_structures_per_entry=1,
            cif_fetcher=lambda _pdb_id: cif_text,
            inventory_by_pdb={
                "2BBB": {"ligand_codes": ["FAD"], "cofactor_families": ["flavin"]},
            },
        )

        self.assertEqual(scan["metadata"]["expected_family_hit_entry_ids"], ["m_csa:652"])
        self.assertEqual(scan["metadata"]["local_expected_family_hit_entry_ids"], ["m_csa:652"])
        self.assertEqual(
            scan["metadata"]["structure_wide_hit_without_local_support_entry_ids"],
            [],
        )
        hit = scan["rows"][0]["structure_hits"][0]
        self.assertEqual(hit["local_expected_family_hits"], ["flavin"])
        self.assertEqual(hit["local_resolved_residue_count"], 1)
        self.assertEqual(hit["residue_position_source"], "mcsa_explicit")

    def test_review_debt_alternate_structure_scan_remaps_selected_positions(self) -> None:
        selected_cif = """data_selected
#
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.auth_atom_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_seq_id
ATOM 1 N N ASP A 7 0.0 0.0 0.0 N ASP A 7
ATOM 2 C CA ASP A 7 1.0 0.0 0.0 CA ASP A 7
#
"""
        alternate_cif = """data_alternate
#
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.auth_atom_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_seq_id
ATOM 1 N N ASP B 7 0.0 0.0 0.0 N ASP B 7
ATOM 2 C CA ASP B 7 1.0 0.0 0.0 CA ASP B 7
HETATM 3 N N1 FAD B 900 1.5 0.0 0.0 N1 FAD B 900
#
"""
        remediation = {
            "metadata": {"method": "review_debt_remediation_plan"},
            "rows": [
                {
                    "entry_id": "m_csa:653",
                    "entry_name": "alternate local flavin gap",
                    "remediation_bucket": "alternate_pdb_ligand_scan",
                    "expected_cofactor_families": ["flavin"],
                    "selected_pdb_id": "1AAA",
                    "alternate_pdb_ids": ["2BBB"],
                    "candidate_pdb_structure_ids": ["1AAA", "2BBB"],
                    "candidate_pdb_residue_position_counts": {"1AAA": 1, "2BBB": 0},
                    "candidate_pdb_residue_positions": {
                        "1AAA": [
                            {
                                "chain_name": "A",
                                "resid": 7,
                                "code": "ASP",
                                "residue_node_id": "m_csa:653:residue:1",
                            }
                        ]
                    },
                }
            ],
        }

        scan = scan_review_debt_alternate_structures(
            remediation,
            max_entries=1,
            max_structures_per_entry=2,
            cif_fetcher=lambda pdb_id: selected_cif if pdb_id == "1AAA" else alternate_cif,
        )

        self.assertEqual(scan["metadata"]["expected_family_hit_entry_ids"], ["m_csa:653"])
        self.assertEqual(scan["metadata"]["local_expected_family_hit_entry_ids"], ["m_csa:653"])
        self.assertEqual(
            scan["metadata"]["alternate_pdb_remapped_residue_position_entry_ids"],
            ["m_csa:653"],
        )
        self.assertEqual(
            scan["metadata"]["local_expected_family_hit_from_remap_entry_ids"],
            ["m_csa:653"],
        )
        self.assertEqual(
            scan["metadata"]["residue_position_remap_basis_counts"],
            {"same_residue_id_chain_remap": 1},
        )
        self.assertEqual(scan["metadata"]["unscanned_structure_count"], 0)
        self.assertTrue(scan["metadata"]["all_candidate_structures_scanned"])
        self.assertEqual(
            scan["metadata"]["alternate_pdb_without_usable_residue_position_entry_ids"],
            [],
        )
        self.assertEqual(
            scan["metadata"]["structure_wide_hit_without_local_support_entry_ids"],
            [],
        )
        row = scan["rows"][0]
        self.assertEqual(row["scanned_pdb_residue_position_counts"], {"1AAA": 1, "2BBB": 0})
        self.assertEqual(
            row["scanned_pdb_remapped_residue_position_counts"],
            {"1AAA": 0, "2BBB": 1},
        )
        self.assertTrue(row["local_active_site_expected_family_observed_from_remap"])
        alternate_hit = row["structure_hits"][1]
        self.assertEqual(alternate_hit["pdb_id"], "2BBB")
        self.assertEqual(alternate_hit["residue_position_source"], "selected_position_remap")
        self.assertEqual(
            alternate_hit["residue_position_remap_basis"],
            "same_residue_id_chain_remap",
        )
        self.assertEqual(alternate_hit["local_expected_family_hits"], ["flavin"])

    def test_review_debt_remap_lead_summary_keeps_hits_review_only(self) -> None:
        scan = {
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
                            "residue_position_remap_basis": "same_residue_id_chain_remap",
                            "usable_residue_position_count": 1,
                            "remapped_residue_position_count": 1,
                        }
                    ],
                },
                {
                    "entry_id": "m_csa:654",
                    "entry_name": "structure-only metal gap",
                    "remediation_bucket": "alternate_pdb_ligand_scan",
                    "expected_cofactor_families": ["metal_ion"],
                    "structure_hits": [
                        {
                            "pdb_id": "3CCC",
                            "ligand_codes": ["ZN"],
                            "expected_family_hits": ["metal_ion"],
                            "local_ligand_codes": [],
                            "local_cofactor_families": [],
                            "local_expected_family_hits": [],
                            "is_selected_structure": False,
                            "residue_position_source": "none",
                            "usable_residue_position_count": 0,
                            "remapped_residue_position_count": 0,
                        }
                    ],
                },
            ],
        }
        remediation = {
            "rows": [
                {
                    "entry_id": "m_csa:653",
                    "debt_status": "carried",
                    "coverage_status": "expected_absent_from_structure",
                    "gap_reasons": ["expected_cofactor_absent_from_structure"],
                }
            ]
        }

        summary = summarize_review_debt_remap_leads(
            scan,
            remediation_plan=remediation,
        )

        self.assertEqual(summary["metadata"]["method"], "review_debt_remap_lead_summary")
        self.assertEqual(summary["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            summary["metadata"]["local_expected_family_hit_from_remap_entry_ids"],
            ["m_csa:653"],
        )
        self.assertEqual(
            summary["metadata"]["lead_type_counts"],
            {
                "local_expected_family_hit_from_remap": 1,
                "structure_wide_hit_without_local_support": 1,
            },
        )
        self.assertFalse(summary["rows"][0]["countable_label_candidate"])
        self.assertEqual(
            summary["rows"][0]["recommended_next_action"],
            "verify_remapped_local_evidence_before_review_import",
        )
        self.assertEqual(summary["rows"][0]["local_expected_ligand_codes"], ["FAD"])
        self.assertEqual(summary["rows"][0]["structure_expected_ligand_codes"], ["FAD"])

    def test_review_debt_remap_local_lead_audit_classifies_review_lanes(self) -> None:
        remap_leads = {
            "metadata": {"method": "review_debt_remap_lead_summary"},
            "rows": [
                {
                    "entry_id": "m_csa:653",
                    "entry_name": "counterevidence remap lead",
                    "lead_type": "local_expected_family_hit_from_remap",
                    "gap_reasons": [
                        "counterevidence_present",
                        "expected_cofactor_absent_from_structure",
                    ],
                    "expected_cofactor_families": ["metal_ion"],
                    "local_expected_family_hit_pdb_ids": ["2BBB"],
                    "local_expected_family_hit_from_remap_pdb_ids": ["2BBB"],
                    "local_expected_ligand_codes": ["ZN"],
                    "remap_basis_counts": {"same_chain_residue_id": 1},
                    "remapped_residue_position_structure_count": 1,
                },
                {
                    "entry_id": "m_csa:654",
                    "entry_name": "clean remap lead",
                    "lead_type": "local_expected_family_hit_from_remap",
                    "gap_reasons": ["expected_cofactor_absent_from_structure"],
                    "expected_cofactor_families": ["metal_ion"],
                    "local_expected_family_hit_pdb_ids": ["3CCC"],
                    "local_expected_family_hit_from_remap_pdb_ids": ["3CCC"],
                    "local_expected_ligand_codes": ["MG"],
                    "remap_basis_counts": {"same_chain_residue_id": 1},
                    "remapped_residue_position_structure_count": 1,
                },
                {
                    "entry_id": "m_csa:655",
                    "entry_name": "glucokinase-like remap lead",
                    "lead_type": "local_expected_family_hit_from_remap",
                    "gap_reasons": ["expected_cofactor_absent_from_structure"],
                    "expected_cofactor_families": ["metal_ion"],
                    "local_expected_family_hit_pdb_ids": ["4DDD"],
                    "local_expected_family_hit_from_remap_pdb_ids": ["4DDD"],
                    "local_expected_ligand_codes": ["MG"],
                    "remap_basis_counts": {"same_chain_residue_id": 1},
                    "remapped_residue_position_structure_count": 1,
                },
            ],
        }
        remediation = {
            "rows": [
                {
                    "entry_id": "m_csa:653",
                    "selected_pdb_id": "1AAA",
                    "coverage_status": "expected_absent_from_structure",
                    "selected_active_site_has_expected_family": False,
                    "selected_structure_has_expected_family": False,
                    "alternate_pdb_with_residue_positions_count": 0,
                    "candidate_pdb_with_residue_positions_count": 1,
                    "counterevidence_reasons": ["role_inferred_metal_low_pocket_support"],
                    "target_fingerprint_id": "metal_dependent_hydrolase",
                    "target_score": 0.42,
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_score": 0.42,
                },
                {
                    "entry_id": "m_csa:654",
                    "selected_pdb_id": "3AAA",
                    "coverage_status": "expected_absent_from_structure",
                    "selected_active_site_has_expected_family": False,
                    "selected_structure_has_expected_family": False,
                    "alternate_pdb_with_residue_positions_count": 0,
                    "candidate_pdb_with_residue_positions_count": 1,
                    "counterevidence_reasons": [],
                    "target_fingerprint_id": "metal_dependent_hydrolase",
                    "target_score": 0.58,
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_score": 0.58,
                },
                {
                    "entry_id": "m_csa:655",
                    "selected_pdb_id": "4AAA",
                    "coverage_status": "expected_absent_from_structure",
                    "selected_active_site_has_expected_family": False,
                    "selected_structure_has_expected_family": False,
                    "alternate_pdb_with_residue_positions_count": 0,
                    "candidate_pdb_with_residue_positions_count": 1,
                    "counterevidence_reasons": [],
                    "target_fingerprint_id": "metal_dependent_hydrolase",
                    "target_score": 0.6,
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_score": 0.6,
                },
            ]
        }
        review_gaps = {
            "rows": [
                {
                    "entry_id": "m_csa:655",
                    "entry_name": "glucokinase-like remap lead",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "mechanism_text_snippets": [
                        "Glucose attacks the gamma phosphorous of ATP during kinase chemistry."
                    ],
                }
            ]
        }

        audit = audit_review_debt_remap_local_leads(
            remap_leads,
            remediation_plan=remediation,
            review_evidence_gaps=review_gaps,
        )

        self.assertEqual(
            audit["metadata"]["method"], "review_debt_remap_local_lead_audit"
        )
        self.assertEqual(audit["metadata"]["audited_entry_count"], 3)
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            audit["metadata"]["decision_counts"],
            {
                "expert_family_boundary_review_required": 1,
                "expert_reaction_substrate_review_required": 1,
                "local_structure_selection_rule_candidate": 1,
            },
        )
        self.assertEqual(
            audit["metadata"]["expert_family_boundary_review_entry_ids"],
            ["m_csa:653"],
        )
        self.assertEqual(
            audit["metadata"]["local_structure_selection_rule_candidate_entry_ids"],
            ["m_csa:654"],
        )
        self.assertEqual(
            audit["metadata"]["expert_reaction_substrate_review_entry_ids"],
            ["m_csa:655"],
        )
        self.assertEqual(
            audit["metadata"]["strict_remap_guardrail_entry_ids"],
            ["m_csa:653", "m_csa:654", "m_csa:655"],
        )
        self.assertTrue(audit["rows"][0]["strict_remap_guardrail_required"])
        self.assertIn(
            "local_evidence_from_conservative_remap_only",
            audit["rows"][0]["counting_blockers"],
        )
        self.assertEqual(
            audit["rows"][1]["recommended_resolution"],
            "local_structure_selection_review",
        )
        self.assertEqual(audit["rows"][2]["recommended_resolution"], "expert_review")
        self.assertIn(
            "atp_phosphoryl_transfer_text_with_hydrolase_top1",
            audit["rows"][2]["reaction_substrate_mismatch_reasons"],
        )

    def test_holo_preference_recommends_swap_when_apo_selected_with_holo_alternate(
        self,
    ) -> None:
        scan = {
            "metadata": {"method": "review_debt_alternate_structure_scan_bounded"},
            "rows": [
                {
                    "entry_id": "m_csa:577",
                    "entry_name": "inositol-phosphate phosphatase",
                    "expected_cofactor_families": ["metal_ion"],
                    "selected_pdb_id": "1IMA",
                    "selected_active_site_has_expected_family": False,
                    "selected_structure_has_expected_family": False,
                    "structure_hits": [
                        {
                            "pdb_id": "1IMA",
                            "is_selected_structure": True,
                            "local_expected_family_hits": [],
                            "local_ligand_codes": ["GD", "IPD"],
                            "local_resolved_residue_count": 6,
                            "usable_residue_position_count": 6,
                            "residue_position_source": "mcsa_explicit",
                        },
                        {
                            "pdb_id": "1AWB",
                            "is_selected_structure": False,
                            "local_expected_family_hits": ["metal_ion"],
                            "local_ligand_codes": ["CA", "IPD"],
                            "local_resolved_residue_count": 6,
                            "usable_residue_position_count": 6,
                            "residue_position_source": "selected_position_remap",
                        },
                        {
                            "pdb_id": "4AS4",
                            "is_selected_structure": False,
                            "local_expected_family_hits": ["metal_ion"],
                            "local_ligand_codes": ["MG"],
                            "local_resolved_residue_count": 5,
                            "usable_residue_position_count": 5,
                            "residue_position_source": "selected_position_remap",
                        },
                    ],
                }
            ],
        }
        audit = audit_structure_selection_holo_preference(scan)
        meta = audit["metadata"]
        self.assertEqual(meta["method"], "structure_selection_holo_preference_audit")
        self.assertEqual(meta["swap_recommended_count"], 1)
        self.assertEqual(meta["swap_recommended_entry_ids"], ["m_csa:577"])
        self.assertEqual(meta["already_holo_entry_count"], 0)
        self.assertEqual(meta["no_holo_alternate_entry_count"], 0)
        row = audit["rows"][0]
        self.assertEqual(row["recommendation"], "swap_selected_structure")
        # 1AWB beats 4AS4 on local_resolved_residue_count tiebreak (6 > 5)
        self.assertEqual(row["recommended_pdb_id"], "1AWB")
        self.assertEqual(
            row["recommended_pdb_local_expected_family_hits"], ["metal_ion"]
        )
        self.assertEqual(row["alternative_holo_candidate_count"], 2)
        self.assertEqual(
            row["alternative_holo_candidate_pdb_ids"], ["1AWB", "4AS4"]
        )

    def test_holo_preference_no_swap_when_already_holo(self) -> None:
        scan = {
            "metadata": {"method": "review_debt_alternate_structure_scan_bounded"},
            "rows": [
                {
                    "entry_id": "m_csa:600",
                    "entry_name": "test enzyme",
                    "expected_cofactor_families": ["metal_ion"],
                    "selected_pdb_id": "2BBB",
                    "selected_active_site_has_expected_family": True,
                    "selected_structure_has_expected_family": True,
                    "structure_hits": [
                        {
                            "pdb_id": "2BBB",
                            "is_selected_structure": True,
                            "local_expected_family_hits": ["metal_ion"],
                            "local_ligand_codes": ["ZN"],
                            "local_resolved_residue_count": 4,
                            "usable_residue_position_count": 4,
                            "residue_position_source": "mcsa_explicit",
                        },
                    ],
                }
            ],
        }
        audit = audit_structure_selection_holo_preference(scan)
        self.assertEqual(audit["metadata"]["swap_recommended_count"], 0)
        self.assertEqual(audit["metadata"]["already_holo_entry_count"], 1)
        self.assertEqual(audit["rows"][0]["recommendation"], "no_swap_already_holo")
        self.assertIsNone(audit["rows"][0]["recommended_pdb_id"])

    def test_holo_preference_no_swap_when_no_holo_alternate(self) -> None:
        scan = {
            "metadata": {"method": "review_debt_alternate_structure_scan_bounded"},
            "rows": [
                {
                    "entry_id": "m_csa:610",
                    "entry_name": "all-apo enzyme",
                    "expected_cofactor_families": ["metal_ion"],
                    "selected_pdb_id": "3CCC",
                    "selected_active_site_has_expected_family": False,
                    "selected_structure_has_expected_family": False,
                    "structure_hits": [
                        {
                            "pdb_id": "3CCC",
                            "is_selected_structure": True,
                            "local_expected_family_hits": [],
                            "local_ligand_codes": [],
                            "local_resolved_residue_count": 4,
                            "usable_residue_position_count": 4,
                            "residue_position_source": "mcsa_explicit",
                        },
                        {
                            "pdb_id": "3DDD",
                            "is_selected_structure": False,
                            "local_expected_family_hits": [],
                            "local_ligand_codes": [],
                            "local_resolved_residue_count": 4,
                            "usable_residue_position_count": 4,
                            "residue_position_source": "selected_position_remap",
                        },
                    ],
                }
            ],
        }
        audit = audit_structure_selection_holo_preference(scan)
        self.assertEqual(audit["metadata"]["swap_recommended_count"], 0)
        self.assertEqual(audit["metadata"]["no_holo_alternate_entry_count"], 1)
        self.assertEqual(
            audit["rows"][0]["recommendation"], "no_swap_no_holo_alternate"
        )

    def test_holo_preference_no_swap_when_expected_families_missing(self) -> None:
        scan = {
            "metadata": {"method": "review_debt_alternate_structure_scan_bounded"},
            "rows": [
                {
                    "entry_id": "m_csa:620",
                    "entry_name": "no-cofactor enzyme",
                    "expected_cofactor_families": [],
                    "selected_pdb_id": "4EEE",
                    "selected_active_site_has_expected_family": False,
                    "selected_structure_has_expected_family": False,
                    "structure_hits": [],
                }
            ],
        }
        audit = audit_structure_selection_holo_preference(scan)
        self.assertEqual(
            audit["metadata"]["no_expected_cofactor_families_entry_count"], 1
        )
        self.assertEqual(
            audit["rows"][0]["recommendation"],
            "no_swap_missing_expected_families",
        )

    def test_holo_preference_prefers_mcsa_explicit_over_remap_when_flag_true(
        self,
    ) -> None:
        scan = {
            "metadata": {"method": "review_debt_alternate_structure_scan_bounded"},
            "rows": [
                {
                    "entry_id": "m_csa:630",
                    "entry_name": "tied candidates enzyme",
                    "expected_cofactor_families": ["metal_ion"],
                    "selected_pdb_id": "5FFF",
                    "selected_active_site_has_expected_family": False,
                    "selected_structure_has_expected_family": False,
                    "structure_hits": [
                        {
                            "pdb_id": "5FFF",
                            "is_selected_structure": True,
                            "local_expected_family_hits": [],
                            "local_resolved_residue_count": 4,
                            "usable_residue_position_count": 4,
                            "residue_position_source": "mcsa_explicit",
                        },
                        {
                            "pdb_id": "5GGG",
                            "is_selected_structure": False,
                            "local_expected_family_hits": ["metal_ion"],
                            "local_resolved_residue_count": 4,
                            "usable_residue_position_count": 4,
                            "residue_position_source": "selected_position_remap",
                        },
                        {
                            "pdb_id": "5HHH",
                            "is_selected_structure": False,
                            "local_expected_family_hits": ["metal_ion"],
                            "local_resolved_residue_count": 4,
                            "usable_residue_position_count": 4,
                            "residue_position_source": "mcsa_explicit",
                        },
                    ],
                }
            ],
        }
        # default flag True → 5HHH (mcsa_explicit) wins despite alphabetic tie
        audit_default = audit_structure_selection_holo_preference(scan)
        self.assertEqual(
            audit_default["rows"][0]["recommended_pdb_id"], "5HHH"
        )
        # flag False → alphabetic tiebreak → 5GGG wins
        audit_flat = audit_structure_selection_holo_preference(
            scan, prefer_mcsa_explicit_over_remap=False
        )
        self.assertEqual(audit_flat["rows"][0]["recommended_pdb_id"], "5GGG")

    def test_holo_preference_min_residue_positions_filter(self) -> None:
        scan = {
            "metadata": {"method": "review_debt_alternate_structure_scan_bounded"},
            "rows": [
                {
                    "entry_id": "m_csa:640",
                    "entry_name": "tiny-mapping enzyme",
                    "expected_cofactor_families": ["metal_ion"],
                    "selected_pdb_id": "6III",
                    "selected_active_site_has_expected_family": False,
                    "selected_structure_has_expected_family": False,
                    "structure_hits": [
                        {
                            "pdb_id": "6III",
                            "is_selected_structure": True,
                            "local_expected_family_hits": [],
                            "local_resolved_residue_count": 6,
                            "usable_residue_position_count": 6,
                            "residue_position_source": "mcsa_explicit",
                        },
                        {
                            "pdb_id": "6JJJ",
                            "is_selected_structure": False,
                            "local_expected_family_hits": ["metal_ion"],
                            "local_resolved_residue_count": 1,
                            "usable_residue_position_count": 1,
                            "residue_position_source": "selected_position_remap",
                        },
                    ],
                }
            ],
        }
        # Threshold 1 → swap recommended
        audit_loose = audit_structure_selection_holo_preference(
            scan, min_usable_residue_positions=1
        )
        self.assertEqual(audit_loose["metadata"]["swap_recommended_count"], 1)
        # Threshold 4 → no swap (alternate has only 1 usable position)
        audit_strict = audit_structure_selection_holo_preference(
            scan, min_usable_residue_positions=4
        )
        self.assertEqual(audit_strict["metadata"]["swap_recommended_count"], 0)
        self.assertEqual(
            audit_strict["metadata"]["no_holo_alternate_entry_count"], 1
        )

    def test_holo_preference_handles_empty_scan(self) -> None:
        audit = audit_structure_selection_holo_preference({"rows": []})
        self.assertEqual(audit["metadata"]["audited_entry_count"], 0)
        self.assertEqual(audit["metadata"]["swap_recommended_count"], 0)
        self.assertEqual(audit["rows"], [])

    def test_review_debt_structure_selection_candidates_remain_review_only(self) -> None:
        remap_local_audit = {
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
                    "local_expected_family_hit_from_remap_pdb_ids": ["3CCC"],
                    "strict_remap_guardrail_required": True,
                    "alternate_pdb_with_explicit_residue_positions_count": 0,
                }
            ],
        }
        alternate_scan = {
            "metadata": {"method": "review_debt_alternate_structure_scan"},
            "rows": [
                {
                    "entry_id": "m_csa:654",
                    "entry_name": "clean remap lead",
                    "selected_pdb_id": "3AAA",
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

        summary = summarize_review_debt_structure_selection_candidates(
            remap_local_audit,
            alternate_scan,
        )

        self.assertEqual(
            summary["metadata"]["method"],
            "review_debt_structure_selection_candidate_summary",
        )
        self.assertEqual(summary["metadata"]["candidate_entry_ids"], ["m_csa:654"])
        self.assertEqual(summary["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(summary["rows"][0]["countable_label_candidate"])
        self.assertEqual(summary["rows"][0]["candidate_pdb_ids"], ["3CCC"])
        self.assertEqual(summary["rows"][0]["candidate_local_expected_ligand_codes"], ["MG"])
        self.assertTrue(summary["rows"][0]["strict_remap_guardrail_required"])

    def test_reaction_substrate_mismatch_audit_flags_kinase_hydrolase_text(self) -> None:
        audit = audit_reaction_substrate_mismatches(
            active_learning_queue={
                "rows": [
                    {
                        "entry_id": "m_csa:655",
                        "entry_name": "glucokinase-like lead",
                        "top1_fingerprint_id": "metal_dependent_hydrolase",
                        "top1_score": 0.6,
                        "rank": 5,
                        "mechanism_text_snippets": [
                            "Glucose attacks the gamma phosphorous of ATP."
                        ],
                    },
                    {
                        "entry_id": "m_csa:656",
                        "entry_name": "metal hydrolase control",
                        "top1_fingerprint_id": "metal_dependent_hydrolase",
                        "mechanism_text_snippets": [
                            "Water attacks the substrate in a hydrolysis reaction."
                        ],
                    },
                ]
            }
        )

        self.assertEqual(audit["metadata"]["method"], "reaction_substrate_mismatch_audit")
        self.assertEqual(audit["metadata"]["mismatch_entry_ids"], ["m_csa:655"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(audit["rows"][0]["countable_label_candidate"])
        self.assertIn(
            "kinase_name_with_hydrolase_top1",
            audit["rows"][0]["mismatch_reasons"],
        )
        self.assertIn(
            "atp_phosphoryl_transfer_text_with_hydrolase_top1",
            audit["rows"][0]["mismatch_reasons"],
        )

    def test_reaction_substrate_mismatch_review_export_keeps_lanes_together(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:655",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="kinase boundary control kept outside the seed set",
            )
        ]
        reaction_audit = {
            "metadata": {"method": "reaction_substrate_mismatch_audit"},
            "rows": [
                {
                    "entry_id": "m_csa:655",
                    "entry_name": "glucokinase-like labeled control",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "mismatch_reasons": ["kinase_name_with_hydrolase_top1"],
                    "mechanism_text_snippets": ["Glucose attacks ATP."],
                }
            ],
        }
        family_guardrails = {
            "metadata": {"method": "family_propagation_guardrail_audit"},
            "rows": [
                {
                    "entry_id": "m_csa:655",
                    "entry_name": "glucokinase-like labeled control",
                    "label_state": "labeled",
                    "current_label_type": "out_of_scope",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_ontology_family": "hydrolysis",
                    "propagation_decision": "block_family_propagation",
                    "propagation_blockers": ["reaction_substrate_mismatch"],
                    "reaction_substrate_mismatch_reasons": [
                        "kinase_name_with_hydrolase_top1"
                    ],
                },
                {
                    "entry_id": "m_csa:656",
                    "entry_name": "pending ribokinase",
                    "label_state": "unlabeled",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_ontology_family": "hydrolysis",
                    "propagation_decision": "block_propagation_pending_review",
                    "propagation_blockers": [
                        "unlabeled_candidate_requires_direct_review",
                        "reaction_substrate_mismatch",
                    ],
                    "reaction_substrate_mismatch_reasons": [
                        "kinase_name_with_hydrolase_top1",
                        "atp_phosphoryl_transfer_text_with_hydrolase_top1",
                    ],
                },
            ],
        }

        export = build_reaction_substrate_mismatch_review_export(
            reaction_substrate_mismatch_audit=reaction_audit,
            family_propagation_guardrails=family_guardrails,
            labels=labels,
        )

        self.assertEqual(
            export["metadata"]["method"],
            "reaction_substrate_mismatch_review_export",
        )
        self.assertEqual(export["metadata"]["exported_count"], 2)
        self.assertTrue(export["metadata"]["all_reaction_audit_mismatches_exported"])
        self.assertTrue(export["metadata"]["all_family_guardrail_mismatches_exported"])
        self.assertEqual(
            export["metadata"]["label_state_counts"],
            {"labeled": 1, "unlabeled": 1},
        )
        self.assertEqual(
            export["metadata"]["current_label_type_counts"],
            {"out_of_scope": 1, "unlabeled": 1},
        )
        self.assertEqual(export["metadata"]["labeled_seed_mismatch_count"], 0)
        self.assertEqual(
            export["metadata"]["recommended_path"],
            "expert_reaction_substrate_review_before_ontology_split",
        )
        self.assertEqual(export["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            [item["entry_id"] for item in export["review_items"]],
            ["m_csa:655", "m_csa:656"],
        )
        self.assertIsNotNone(export["review_items"][0]["current_label"])
        self.assertEqual(
            export["review_items"][1]["mismatch_context"]["resolution_lane"],
            "unlabeled_pending_review",
        )
        self.assertFalse(
            any(
                item["mismatch_context"]["countable_label_candidate"]
                for item in export["review_items"]
            )
        )
        batch = build_provisional_review_decision_batch(export)
        self.assertTrue(batch["metadata"]["reaction_substrate_mismatch_review_only"])
        self.assertEqual(batch["metadata"]["decision_counts"], {"no_decision": 2})
        self.assertTrue(
            all(
                item["decision"]["action"] == "no_decision"
                for item in batch["review_items"]
            )
        )
        unsafe_countable = deepcopy(export)
        unsafe_countable["review_items"][1]["decision"] = {
            "action": "accept_label",
            "label_type": "seed_fingerprint",
            "fingerprint_id": "metal_dependent_hydrolase",
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": "automation_label_factory",
            "rationale": "Automation must not count mismatch review rows without expert resolution.",
            "evidence_score": 0.65,
            "review_status": "automation_curated",
            "reaction_substrate_resolution": "needs_more_evidence",
        }
        imported = import_countable_review_decisions(labels, unsafe_countable)
        self.assertNotIn("m_csa:656", {label.entry_id for label in imported})
        reviewed_batch = deepcopy(batch)
        reviewed_batch["review_items"][1]["decision"] = {
            "action": "accept_label",
            "label_type": "out_of_scope",
            "fingerprint_id": None,
            "tier": "bronze",
            "confidence": "high",
            "reviewer": "test_reviewer",
            "rationale": "Expert reviewed as out of scope, but this batch is still review-only.",
            "evidence_score": None,
            "review_status": "expert_reviewed",
            "reaction_substrate_resolution": "confirm_current_label_or_out_of_scope",
        }
        imported = import_countable_review_decisions(labels, reviewed_batch)
        self.assertNotIn("m_csa:656", {label.entry_id for label in imported})

    def test_external_source_review_exports_cannot_import_countable_labels(
        self,
    ) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="high",
                rationale="baseline out-of-scope control",
            )
        ]
        export = {
            "metadata": {
                "method": "external_source_evidence_request_export",
                "external_source_review_only": True,
            },
            "review_items": [
                {
                    "entry_id": "uniprot:P12345",
                    "current_label": None,
                    "external_source_context": {
                        "accession": "P12345",
                        "countable_label_candidate": False,
                    },
                    "decision": {
                        "action": "accept_label",
                        "label_type": "seed_fingerprint",
                        "fingerprint_id": "metal_dependent_hydrolase",
                        "tier": "bronze",
                        "confidence": "medium",
                        "reviewer": "automation_label_factory",
                        "rationale": (
                            "Automation must not count external-source review rows."
                        ),
                        "evidence_score": 0.7,
                        "review_status": "automation_curated",
                    },
                }
            ],
        }

        batch = build_provisional_review_decision_batch(export)
        self.assertTrue(batch["metadata"]["external_source_review_only"])
        self.assertEqual(batch["metadata"]["decision_counts"], {"no_decision": 1})
        imported = import_countable_review_decisions(labels, export)
        self.assertEqual([label.entry_id for label in imported], ["m_csa:1"])

    def test_factory_gate_requires_mismatch_review_export_when_guardrails_find_lanes(
        self,
    ) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:655",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="kinase boundary control kept outside the seed set",
            )
        ]
        queue = {
            "metadata": {
                "queued_count": 1,
                "all_unlabeled_rows_retained": True,
                "ranking_terms": [
                    "uncertainty",
                    "impact",
                    "novelty",
                    "hard_negative_value",
                    "evidence_conflict",
                    "family_boundary_value",
                    "reaction_substrate_mismatch_value",
                ],
            },
            "rows": [
                {
                    "entry_id": "m_csa:655",
                    "top1_ontology_family": "hydrolysis",
                }
            ],
        }
        family_guardrails = {
            "metadata": {
                "method": "family_propagation_guardrail_audit",
                "reported_count": 2,
                "source_guardrails": [{"source": "local_proxy"}],
            },
            "rows": [
                {
                    "entry_id": "m_csa:655",
                    "entry_name": "glucokinase-like labeled control",
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
        gate_without_export = check_label_factory_gates(
            labels,
            {"metadata": {"promote_to_silver_count": 1, "abstention_or_review_count": 1}},
            {
                "metadata": {
                    "output_label_count": len(labels),
                    "output_summary": {"by_tier": {"silver": 1}},
                }
            },
            queue,
            {"metadata": {"control_count": 1, "axis_counts": {"ontology_family_boundary": 1}}},
            {"metadata": {"exported_count": 1}, "review_items": [{"entry_id": "m_csa:655"}]},
            family_propagation_guardrails=family_guardrails,
        )
        self.assertFalse(
            gate_without_export["gates"][
                "reaction_substrate_mismatch_review_export_ready"
            ]
        )
        self.assertIn(
            "reaction_substrate_mismatch_review_export_ready",
            gate_without_export["blockers"],
        )
        self.assertEqual(
            gate_without_export["metadata"][
                "family_guardrail_reaction_substrate_mismatch_count"
            ],
            2,
        )

        mismatch_export = build_reaction_substrate_mismatch_review_export(
            reaction_substrate_mismatch_audit={
                "metadata": {"method": "reaction_substrate_mismatch_audit"},
                "rows": [],
            },
            family_propagation_guardrails=family_guardrails,
            labels=labels,
        )
        gate_with_export = check_label_factory_gates(
            labels,
            {"metadata": {"promote_to_silver_count": 1, "abstention_or_review_count": 1}},
            {
                "metadata": {
                    "output_label_count": len(labels),
                    "output_summary": {"by_tier": {"silver": 1}},
                }
            },
            queue,
            {"metadata": {"control_count": 1, "axis_counts": {"ontology_family_boundary": 1}}},
            {"metadata": {"exported_count": 1}, "review_items": [{"entry_id": "m_csa:655"}]},
            family_propagation_guardrails=family_guardrails,
            reaction_substrate_mismatch_review_export=mismatch_export,
        )
        self.assertTrue(
            gate_with_export["gates"][
                "reaction_substrate_mismatch_review_export_ready"
            ]
        )
        self.assertEqual(
            gate_with_export["metadata"][
                "reaction_substrate_mismatch_review_export_missing_entry_ids"
            ],
            [],
        )
        self.assertEqual(
            gate_with_export["metadata"][
                "reaction_substrate_mismatch_review_export_labeled_seed_mismatch_count"
            ],
            0,
        )

    def test_expert_label_decision_review_export_keeps_rows_review_only(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="Existing reviewed boundary control.",
            )
        ]
        queue = {
            "metadata": {
                "method": "active_learning_review_queue",
                "queued_count": 3,
                "all_unlabeled_rows_retained": True,
                "ranking_terms": [
                    "uncertainty",
                    "impact",
                    "novelty",
                    "hard_negative_value",
                    "evidence_conflict",
                    "family_boundary_value",
                    "reaction_substrate_mismatch_value",
                ],
            },
            "rows": [
                {
                    "rank": 1,
                    "entry_id": "m_csa:1",
                    "entry_name": "labeled boundary",
                    "label_state": "labeled",
                    "current_label_type": "out_of_scope",
                    "recommended_action": "hold_bronze_boundary_review",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_ontology_family": "hydrolysis",
                },
                {
                    "rank": 2,
                    "entry_id": "m_csa:650",
                    "entry_name": "phospholipase A1",
                    "label_state": "unlabeled",
                    "recommended_action": "expert_label_decision_needed",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_ontology_family": "hydrolysis",
                    "top1_score": 0.6085,
                    "cofactor_evidence_level": "ligand_supported",
                    "reaction_substrate_mismatch_reasons": [],
                },
                {
                    "rank": 3,
                    "entry_id": "m_csa:655",
                    "entry_name": "glucokinase",
                    "label_state": "unlabeled",
                    "recommended_action": "expert_label_decision_needed",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_ontology_family": "hydrolysis",
                    "top1_score": 0.512,
                    "cofactor_evidence_level": "ligand_supported",
                    "reaction_substrate_mismatch_reasons": [
                        "kinase_name_with_hydrolase_top1"
                    ],
                },
            ],
        }
        review_debt = {
            "metadata": {
                "method": "review_debt_summary",
                "carried_review_debt_entry_ids": ["m_csa:650"],
                "new_review_debt_entry_ids": ["m_csa:655"],
            },
            "rows": [
                {
                    "entry_id": "m_csa:650",
                    "recommended_next_action": "expert_review_decision_needed",
                }
            ],
        }
        mismatch_export = {
            "metadata": {
                "method": "reaction_substrate_mismatch_review_export",
                "exported_count": 1,
                "exported_entry_ids": ["m_csa:655"],
            },
            "review_items": [{"entry_id": "m_csa:655"}],
        }

        export = build_expert_label_decision_review_export(
            active_learning_queue=queue,
            labels=labels,
            review_debt=review_debt,
            reaction_substrate_mismatch_review_export=mismatch_export,
        )

        self.assertEqual(export["metadata"]["exported_count"], 2)
        self.assertEqual(export["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(export["metadata"]["decision_counts"], {"no_decision": 2})
        self.assertEqual(
            export["metadata"]["quality_risk_flag_counts"][
                "external_expert_decision_required"
            ],
            2,
        )
        self.assertEqual(
            export["metadata"]["quality_risk_flag_counts"][
                "reaction_substrate_mismatch"
            ],
            1,
        )
        self.assertEqual(
            export["metadata"]["missing_reaction_substrate_mismatch_export_entry_ids"],
            [],
        )
        contexts = {
            item["entry_id"]: item["expert_label_decision_context"]
            for item in export["review_items"]
        }
        self.assertEqual(
            contexts["m_csa:650"]["resolution_lane"],
            "external_expert_label_decision",
        )
        self.assertEqual(
            contexts["m_csa:655"]["resolution_lane"],
            "already_routed_reaction_substrate_mismatch_export",
        )
        self.assertIn(
            "reaction_substrate_mismatch",
            contexts["m_csa:655"]["quality_risk_flags"],
        )
        self.assertFalse(contexts["m_csa:650"]["countable_label_candidate"])

        batch = build_provisional_review_decision_batch(export)
        self.assertTrue(batch["metadata"]["expert_label_decision_review_only"])
        self.assertEqual(batch["metadata"]["decision_counts"], {"no_decision": 2})
        countable = import_countable_review_decisions(labels, batch)
        self.assertEqual([label.entry_id for label in countable], ["m_csa:1"])
        unsafe_countable = deepcopy(export)
        unsafe_countable["review_items"][0]["decision"] = {
            "action": "accept_label",
            "label_type": "seed_fingerprint",
            "fingerprint_id": "metal_dependent_hydrolase",
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": "automation_label_factory",
            "rationale": "Automation must not count expert-label decision exports.",
            "evidence_score": 0.65,
            "review_status": "automation_curated",
        }
        self.assertEqual(
            [label.entry_id for label in import_countable_review_decisions(labels, unsafe_countable)],
            ["m_csa:1"],
        )
        repair = summarize_expert_label_decision_repair_candidates(
            export,
            review_debt_remediation={
                "rows": [
                    {
                        "entry_id": "m_csa:650",
                        "remediation_bucket": "active_site_mapping_repair",
                        "selected_pdb_id": "1ABC",
                        "alternate_pdb_count": 2,
                    }
                ]
            },
            structure_mapping={
                "rows": [{"entry_id": "m_csa:650", "status": "ok"}]
            },
            alternate_structure_scan={
                "rows": [
                    {
                        "entry_id": "m_csa:650",
                        "scan_outcome": "alternate_structure_has_expected_cofactor_candidate",
                        "scanned_structure_count": 4,
                    }
                ]
            },
            max_rows=0,
        )
        self.assertEqual(repair["metadata"]["candidate_count"], 2)
        self.assertEqual(repair["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            repair["metadata"]["repair_bucket_counts"],
            {
                "reaction_substrate_review_already_exported": 1,
                "external_expert_label_decision": 1,
            },
        )
        repair_rows = {row["entry_id"]: row for row in repair["rows"]}
        self.assertEqual(
            repair_rows["m_csa:655"]["repair_bucket"],
            "reaction_substrate_review_already_exported",
        )
        self.assertEqual(
            repair_rows["m_csa:650"]["repair_bucket"],
            "external_expert_label_decision",
        )
        self.assertEqual(
            repair_rows["m_csa:650"]["review_debt_remediation_context"][
                "selected_pdb_id"
            ],
            "1ABC",
        )
        self.assertEqual(repair["metadata"]["remediation_context_linked_count"], 1)
        self.assertEqual(repair["metadata"]["structure_mapping_context_linked_count"], 1)
        self.assertEqual(
            repair["metadata"]["alternate_structure_scan_context_linked_count"], 1
        )
        self.assertEqual(
            repair["metadata"]["candidate_entry_ids"],
            ["m_csa:650", "m_csa:655"],
        )
        self.assertEqual(
            repair_rows["m_csa:650"]["alternate_structure_scan_context"][
                "scanned_structure_count"
            ],
            4,
        )
        self.assertFalse(repair_rows["m_csa:650"]["countable_label_candidate"])

        gate_without_export = check_label_factory_gates(
            labels,
            {"metadata": {"promote_to_silver_count": 1, "abstention_or_review_count": 1}},
            {
                "metadata": {
                    "output_label_count": len(labels),
                    "output_summary": {"by_tier": {"silver": 1}},
                }
            },
            queue,
            {"metadata": {"control_count": 1, "axis_counts": {"ontology_family_boundary": 1}}},
            {"metadata": {"exported_count": 1}, "review_items": [{"entry_id": "m_csa:650"}]},
            family_propagation_guardrails={
                "metadata": {
                    "reported_count": 1,
                    "source_guardrails": [{"source": "local_proxy"}],
                },
                "rows": [],
            },
        )
        self.assertFalse(
            gate_without_export["gates"]["expert_label_decision_review_export_ready"]
        )
        self.assertFalse(
            gate_without_export["gates"][
                "expert_label_decision_repair_candidates_ready"
            ]
        )
        self.assertFalse(
            gate_without_export["gates"][
                "expert_label_decision_repair_guardrails_ready"
            ]
        )
        repair_guardrail = audit_expert_label_decision_repair_guardrails(repair)

        gate_with_export = check_label_factory_gates(
            labels,
            {"metadata": {"promote_to_silver_count": 1, "abstention_or_review_count": 1}},
            {
                "metadata": {
                    "output_label_count": len(labels),
                    "output_summary": {"by_tier": {"silver": 1}},
                }
            },
            queue,
            {"metadata": {"control_count": 1, "axis_counts": {"ontology_family_boundary": 1}}},
            {"metadata": {"exported_count": 1}, "review_items": [{"entry_id": "m_csa:650"}]},
            family_propagation_guardrails={
                "metadata": {
                    "reported_count": 1,
                    "source_guardrails": [{"source": "local_proxy"}],
                },
                "rows": [],
            },
            expert_label_decision_review_export=export,
            expert_label_decision_repair_candidates=repair,
            expert_label_decision_repair_guardrail_audit=repair_guardrail,
        )
        self.assertTrue(
            gate_with_export["gates"]["expert_label_decision_review_export_ready"]
        )
        self.assertTrue(
            gate_with_export["gates"][
                "expert_label_decision_repair_candidates_ready"
            ]
        )
        self.assertTrue(
            gate_with_export["gates"][
                "expert_label_decision_repair_guardrails_ready"
            ]
        )
        self.assertEqual(
            gate_with_export["metadata"][
                "expert_label_decision_review_export_missing_entry_ids"
            ],
            [],
        )
        self.assertEqual(
            gate_with_export["metadata"][
                "expert_label_decision_repair_candidates_missing_entry_ids"
            ],
            [],
        )
        self.assertTrue(
            gate_with_export["metadata"][
                "expert_label_decision_repair_candidate_entry_id_count_matches"
            ]
        )

    def test_expert_label_decision_repair_guardrail_keeps_priority_lanes_review_only(
        self,
    ) -> None:
        repair = {
            "metadata": {
                "method": "expert_label_decision_repair_candidate_summary",
                "candidate_count": 3,
                "all_candidates_retained": True,
            },
            "rows": [
                {
                    "entry_id": "m_csa:577",
                    "entry_name": "inositol-phosphate phosphatase",
                    "repair_bucket": "text_leakage_or_nonlocal_evidence_guardrail",
                    "quality_risk_flags": [
                        "text_leakage_or_nonlocal_evidence_risk",
                        "cofactor_family_ambiguity",
                        "counterevidence_boundary",
                    ],
                    "counterevidence_reasons": ["role_inferred_metal_low_pocket_support"],
                    "readiness_blockers": [],
                    "reaction_substrate_mismatch_reasons": [],
                    "review_debt_remediation_context": {
                        "selected_pdb_id": "1IMA",
                        "selected_pdb_residue_position_count": 6,
                        "alternate_pdb_with_residue_positions_count": 0,
                    },
                    "alternate_structure_scan_context": {
                        "local_active_site_expected_family_observed": True,
                        "local_expected_family_hit_count": 2,
                        "structure_wide_expected_family_hit_count": 4,
                    },
                    "countable_label_candidate": False,
                },
                {
                    "entry_id": "m_csa:692",
                    "entry_name": "mapping gap",
                    "repair_bucket": "active_site_mapping_or_structure_gap_repair",
                    "quality_risk_flags": [
                        "active_site_mapping_or_structure_gap",
                        "cofactor_family_ambiguity",
                    ],
                    "readiness_blockers": ["fewer_than_three_resolved_residues"],
                    "counterevidence_reasons": [],
                    "reaction_substrate_mismatch_reasons": [],
                    "review_debt_remediation_context": {
                        "selected_pdb_id": "1DL5",
                        "selected_pdb_residue_position_count": 1,
                        "alternate_pdb_with_residue_positions_count": 0,
                    },
                    "alternate_structure_scan_context": None,
                    "countable_label_candidate": False,
                },
                {
                    "entry_id": "m_csa:700",
                    "entry_name": "external decision only",
                    "repair_bucket": "external_expert_label_decision",
                    "quality_risk_flags": ["external_expert_decision_required"],
                    "countable_label_candidate": False,
                },
            ],
        }
        remap_audit = {
            "metadata": {
                "method": "review_debt_remap_local_lead_audit",
                "strict_remap_guardrail_entry_ids": ["m_csa:577"],
                "expert_family_boundary_review_entry_ids": ["m_csa:577"],
                "expert_reaction_substrate_review_entry_ids": [],
            }
        }

        audit = audit_expert_label_decision_repair_guardrails(
            repair,
            remap_local_lead_audit=remap_audit,
        )

        self.assertTrue(audit["metadata"]["guardrail_ready"])
        self.assertEqual(audit["metadata"]["priority_repair_row_count"], 2)
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            audit["metadata"]["local_expected_family_evidence_review_only_entry_ids"],
            ["m_csa:577"],
        )
        self.assertEqual(
            audit["metadata"]["missing_local_mechanistic_evidence_entry_ids"],
            ["m_csa:692"],
        )
        rows = {row["entry_id"]: row for row in audit["rows"]}
        self.assertEqual(
            rows["m_csa:577"]["local_mechanistic_evidence_status"],
            "local_expected_family_evidence_from_conservative_remap_review_only",
        )
        self.assertIn(
            "strict_conservative_remap_guardrail",
            rows["m_csa:577"]["non_countable_blockers"],
        )
        self.assertIn(
            "active_site_mapping_or_structure_gap_unresolved",
            rows["m_csa:692"]["non_countable_blockers"],
        )

    def test_expert_label_decision_local_evidence_gap_audit_classifies_repair_lanes(
        self,
    ) -> None:
        guardrail = {
            "metadata": {
                "method": "expert_label_decision_repair_guardrail_audit",
                "priority_repair_entry_ids": ["m_csa:577", "m_csa:692"],
                "missing_local_mechanistic_evidence_entry_ids": ["m_csa:692"],
                "local_expected_family_evidence_review_only_entry_ids": ["m_csa:577"],
            },
            "rows": [
                {
                    "entry_id": "m_csa:577",
                    "entry_name": "remap lead",
                    "repair_bucket": "text_leakage_or_nonlocal_evidence_guardrail",
                    "quality_risk_flags": [
                        "text_leakage_or_nonlocal_evidence_risk"
                    ],
                    "local_mechanistic_evidence_status": (
                        "local_expected_family_evidence_from_conservative_remap_review_only"
                    ),
                    "selected_pdb_id": "1IMA",
                    "selected_pdb_residue_position_count": 6,
                    "alternate_pdb_with_residue_positions_count": 0,
                    "local_expected_family_hit_count": 2,
                    "structure_wide_expected_family_hit_count": 4,
                    "strict_remap_guardrail": True,
                    "non_countable_blockers": [
                        "strict_conservative_remap_guardrail",
                        "external_expert_decision_required",
                    ],
                    "counterevidence_reasons": ["role_inferred_metal_low_pocket_support"],
                    "reaction_substrate_mismatch_reasons": [],
                    "countable_label_candidate": False,
                },
                {
                    "entry_id": "m_csa:692",
                    "entry_name": "mapping gap",
                    "repair_bucket": "active_site_mapping_or_structure_gap_repair",
                    "quality_risk_flags": [
                        "active_site_mapping_or_structure_gap",
                        "cofactor_family_ambiguity",
                    ],
                    "local_mechanistic_evidence_status": (
                        "no_local_expected_family_evidence"
                    ),
                    "selected_pdb_id": "1DL5",
                    "selected_pdb_residue_position_count": 1,
                    "alternate_pdb_with_residue_positions_count": 0,
                    "local_expected_family_hit_count": 0,
                    "structure_wide_expected_family_hit_count": 0,
                    "strict_remap_guardrail": False,
                    "non_countable_blockers": [
                        "active_site_mapping_or_structure_gap_unresolved",
                        "external_expert_decision_required",
                    ],
                    "counterevidence_reasons": [],
                    "reaction_substrate_mismatch_reasons": [],
                    "countable_label_candidate": False,
                },
            ],
        }
        repair = {
            "metadata": {"method": "expert_label_decision_repair_candidate_summary"},
            "rows": [
                {
                    "entry_id": "m_csa:577",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_ontology_family": "hydrolysis",
                    "top1_score": 0.61,
                    "cofactor_evidence_level": "ligand_supported",
                    "review_debt_remediation_context": {
                        "candidate_pdb_structure_count": 3,
                        "alternate_pdb_count": 2,
                    },
                    "alternate_structure_scan_context": {
                        "scan_outcome": "alternate_structure_has_expected_cofactor_candidate",
                        "scanned_structure_count": 3,
                        "local_expected_family_hit_count": 2,
                        "structure_wide_expected_family_hit_count": 4,
                    },
                },
                {
                    "entry_id": "m_csa:692",
                    "top1_fingerprint_id": "flavin_dehydrogenase_reductase",
                    "top1_ontology_family": "flavin_redox",
                    "top1_score": 0.37,
                    "cofactor_evidence_level": "absent",
                    "review_debt_remediation_context": {
                        "candidate_pdb_structure_count": 1,
                        "alternate_pdb_count": 0,
                    },
                    "alternate_structure_scan_context": {
                        "scan_outcome": "no_expected_cofactor_in_scanned_structures",
                        "scanned_structure_count": 1,
                        "local_expected_family_hit_count": 0,
                        "structure_wide_expected_family_hit_count": 0,
                    },
                },
            ],
        }

        audit = audit_expert_label_decision_local_evidence_gaps(
            guardrail,
            expert_label_decision_repair_candidates=repair,
        )

        self.assertEqual(
            audit["metadata"]["method"],
            "expert_label_decision_local_evidence_gap_audit",
        )
        self.assertTrue(audit["metadata"]["audit_ready"])
        self.assertTrue(audit["metadata"]["priority_rows_accounted_for"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(audit["metadata"]["repair_ready_for_count_growth"])
        self.assertEqual(
            audit["metadata"][
                "selected_structure_residue_support_shortfall_entry_ids"
            ],
            ["m_csa:692"],
        )
        self.assertEqual(
            audit["metadata"]["single_structure_no_alternate_context_entry_ids"],
            ["m_csa:692"],
        )
        rows = {row["entry_id"]: row for row in audit["rows"]}
        self.assertIn(
            "strict_conservative_remap_guardrail",
            rows["m_csa:577"]["local_evidence_gap_classes"],
        )
        self.assertIn(
            "scanned_structures_without_local_expected_family_hit",
            rows["m_csa:692"]["local_evidence_gap_classes"],
        )
        self.assertEqual(
            rows["m_csa:692"]["recommended_next_action"],
            "source_external_cofactor_or_structure_evidence",
        )

    def test_label_factory_gate_requires_local_evidence_gap_audit_for_priority_repairs(
        self,
    ) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="Countable seed label used to exercise factory gates.",
            )
        ]
        queue = {
            "metadata": {
                "queued_count": 1,
                "all_unlabeled_rows_retained": True,
                "ranking_terms": [
                    "uncertainty",
                    "impact",
                    "novelty",
                    "hard_negative_value",
                    "evidence_conflict",
                    "family_boundary_value",
                    "reaction_substrate_mismatch_value",
                ],
            },
            "rows": [
                {
                    "entry_id": "m_csa:650",
                    "recommended_action": "expert_label_decision_needed",
                    "top1_ontology_family": "hydrolysis",
                }
            ],
        }
        expert_export = {
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
        repair = {
            "metadata": {
                "method": "expert_label_decision_repair_candidate_summary",
                "candidate_count": 1,
                "candidate_entry_ids": ["m_csa:650"],
                "countable_label_candidate_count": 0,
            },
            "rows": [{"entry_id": "m_csa:650"}],
        }
        repair_guardrail = {
            "metadata": {
                "method": "expert_label_decision_repair_guardrail_audit",
                "guardrail_ready": True,
                "all_priority_lanes_non_countable": True,
                "priority_repair_row_count": 1,
                "countable_label_candidate_count": 0,
            },
            "rows": [{"entry_id": "m_csa:650"}],
        }
        common_args = dict(
            labels=labels,
            label_factory_audit={
                "metadata": {"promote_to_silver_count": 1, "abstention_or_review_count": 1}
            },
            applied_label_factory={
                "metadata": {
                    "output_label_count": len(labels),
                    "output_summary": {"by_tier": {"silver": 1}},
                }
            },
            active_learning_queue=queue,
            adversarial_negatives={
                "metadata": {
                    "control_count": 1,
                    "axis_counts": {"ontology_family_boundary": 1},
                }
            },
            expert_review_export={
                "metadata": {"exported_count": 1},
                "review_items": [{"entry_id": "m_csa:650"}],
            },
            family_propagation_guardrails={
                "metadata": {
                    "reported_count": 1,
                    "source_guardrails": [{"source": "local_proxy"}],
                },
                "rows": [],
            },
            expert_label_decision_review_export=expert_export,
            expert_label_decision_repair_candidates=repair,
            expert_label_decision_repair_guardrail_audit=repair_guardrail,
        )

        without_gap_audit = check_label_factory_gates(**common_args)
        self.assertFalse(
            without_gap_audit["gates"][
                "expert_label_decision_local_evidence_gaps_audited"
            ]
        )
        self.assertIn(
            "expert_label_decision_local_evidence_gaps_audited",
            without_gap_audit["blockers"],
        )

        with_gap_audit = check_label_factory_gates(
            **common_args,
            expert_label_decision_local_evidence_gap_audit={
                "metadata": {
                    "method": "expert_label_decision_local_evidence_gap_audit",
                    "audit_ready": True,
                    "priority_rows_accounted_for": True,
                    "audited_entry_count": 1,
                    "missing_priority_entry_ids": [],
                    "countable_label_candidate_count": 0,
                },
                "rows": [{"entry_id": "m_csa:650"}],
            },
        )
        self.assertTrue(
            with_gap_audit["gates"][
                "expert_label_decision_local_evidence_gaps_audited"
            ]
        )
        self.assertFalse(
            with_gap_audit["gates"][
                "expert_label_decision_local_evidence_review_export_ready"
            ]
        )

        with_gap_export = check_label_factory_gates(
            **common_args,
            expert_label_decision_local_evidence_gap_audit={
                "metadata": {
                    "method": "expert_label_decision_local_evidence_gap_audit",
                    "audit_ready": True,
                    "priority_rows_accounted_for": True,
                    "audited_entry_count": 1,
                    "missing_priority_entry_ids": [],
                    "countable_label_candidate_count": 0,
                },
                "rows": [{"entry_id": "m_csa:650"}],
            },
            expert_label_decision_local_evidence_review_export={
                "metadata": {
                    "method": "expert_label_decision_local_evidence_review_export",
                    "export_ready": True,
                    "all_source_rows_exported": True,
                    "exported_count": 1,
                    "countable_label_candidate_count": 0,
                    "decision_counts": {"no_decision": 1},
                },
                "review_items": [{"entry_id": "m_csa:650"}],
            },
        )
        self.assertTrue(
            with_gap_export["gates"][
                "expert_label_decision_local_evidence_review_export_ready"
            ]
        )
        self.assertTrue(
            with_gap_export["metadata"]["automation_ready_for_next_label_batch"]
        )

    def test_local_evidence_gap_review_export_stays_no_decision(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:654",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="high",
                rationale="Existing out-of-scope control.",
            )
        ]
        local_gap_audit = {
            "metadata": {
                "method": "expert_label_decision_local_evidence_gap_audit",
                "audit_ready": True,
                "audited_entry_count": 2,
            },
            "rows": [
                {
                    "entry_id": "m_csa:654",
                    "entry_name": "single structure kinase",
                    "local_evidence_gap_classes": [
                        "single_structure_no_alternate_context",
                        "reaction_substrate_mismatch_review_required",
                    ],
                    "recommended_next_action": (
                        "route_to_reaction_substrate_expert_review"
                    ),
                    "countable_label_candidate": False,
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                },
                {
                    "entry_id": "m_csa:659",
                    "entry_name": "single structure heme gap",
                    "local_evidence_gap_classes": [
                        "single_structure_no_alternate_context",
                        "counterevidence_boundary_unresolved",
                    ],
                    "recommended_next_action": "route_to_family_boundary_expert_review",
                    "countable_label_candidate": False,
                    "top1_fingerprint_id": "heme_peroxidase",
                },
            ],
        }

        export = build_expert_label_decision_local_evidence_review_export(
            local_gap_audit,
            labels,
        )
        self.assertEqual(
            export["metadata"]["method"],
            "expert_label_decision_local_evidence_review_export",
        )
        self.assertTrue(export["metadata"]["export_ready"])
        self.assertEqual(export["metadata"]["exported_count"], 2)
        self.assertEqual(export["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(export["metadata"]["decision_counts"], {"no_decision": 2})
        self.assertIn(
            "reaction or substrate",
            export["review_items"][0]["review_question"],
        )

        batch = build_provisional_review_decision_batch(export)
        self.assertTrue(batch["metadata"]["local_evidence_gap_review_only"])
        self.assertEqual(batch["metadata"]["decision_counts"], {"no_decision": 2})
        self.assertEqual(
            {
                item["decision"]["local_evidence_resolution"]
                for item in batch["review_items"]
            },
            {"needs_more_evidence"},
        )
        unsafe_countable = deepcopy(export)
        unsafe_countable["review_items"][1]["decision"] = {
            "action": "accept_label",
            "label_type": "seed_fingerprint",
            "fingerprint_id": "heme_peroxidase",
            "tier": "bronze",
            "confidence": "medium",
            "reviewer": "automation_label_factory",
            "rationale": "Automation must not count local-evidence review rows.",
            "evidence_score": 0.65,
            "review_status": "automation_curated",
            "local_evidence_resolution": "confirms_local_mechanistic_evidence",
        }
        countable = import_countable_review_decisions(labels, unsafe_countable)
        self.assertEqual([label.entry_id for label in countable], ["m_csa:654"])

        plan = summarize_expert_label_decision_local_evidence_repair_plan(
            local_gap_audit,
            local_evidence_review_export=export,
        )
        self.assertTrue(plan["metadata"]["repair_plan_ready"])
        self.assertEqual(plan["metadata"]["planned_entry_count"], 2)
        self.assertEqual(
            plan["metadata"]["repair_lane_counts"][
                "expert_reaction_substrate_review"
            ],
            1,
        )
        self.assertTrue(plan["metadata"]["all_planned_rows_review_exported"])
        self.assertEqual(
            [row["repair_lane"] for row in plan["rows"]],
            ["expert_reaction_substrate_review", "expert_family_boundary_review"],
        )

    def test_accepted_review_debt_deferral_audit_keeps_rows_non_countable(self) -> None:
        review_debt = {
            "metadata": {
                "method": "review_debt_summary",
                "review_debt_entry_ids": ["m_csa:712", "m_csa:718"],
                "new_review_debt_count": 2,
                "new_review_debt_entry_ids": ["m_csa:712", "m_csa:718"],
            },
            "rows": [
                {
                    "entry_id": "m_csa:712",
                    "entry_name": "strict remap local lead",
                    "debt_status": "new",
                    "decision_action": "mark_needs_more_evidence",
                    "recommended_next_action": "expert_family_boundary_review",
                    "gap_reasons": ["review_marked_needs_more_evidence"],
                    "target_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                },
                {
                    "entry_id": "m_csa:718",
                    "entry_name": "structure wide only lead",
                    "debt_status": "new",
                    "decision_action": "mark_needs_more_evidence",
                    "recommended_next_action": (
                        "inspect_alternate_structure_or_cofactor_source"
                    ),
                    "gap_reasons": ["expected_cofactor_not_local"],
                    "target_fingerprint_id": "heme_peroxidase_oxidase",
                    "top1_fingerprint_id": "heme_peroxidase_oxidase",
                },
            ],
        }
        acceptance = {
            "metadata": {
                "method": "label_batch_acceptance_check",
                "accepted_new_label_entry_ids": ["m_csa:705"],
            }
        }
        audit = audit_accepted_review_debt_deferrals(
            review_debt,
            acceptance,
            scaling_quality_audit={
                "metadata": {
                    "method": "label_scaling_quality_audit",
                    "unclassified_new_review_debt_entry_ids": [],
                    "alternate_structure_scan_structure_wide_hit_without_local_support_entry_ids": [
                        "m_csa:718"
                    ],
                    "alternate_structure_scan_local_expected_family_hit_from_remap_entry_ids": [
                        "m_csa:712"
                    ],
                }
            },
            local_evidence_gap_audit={
                "metadata": {
                    "method": "expert_label_decision_local_evidence_gap_audit",
                    "audited_entry_ids": ["m_csa:712"],
                },
                "rows": [{"entry_id": "m_csa:712"}],
            },
            local_evidence_review_export={
                "metadata": {
                    "method": "expert_label_decision_local_evidence_review_export",
                    "exported_entry_ids": ["m_csa:712"],
                },
                "review_items": [{"entry_id": "m_csa:712"}],
            },
            remap_local_lead_audit={
                "metadata": {
                    "method": "review_debt_remap_local_lead_audit",
                    "strict_remap_guardrail_entry_ids": ["m_csa:712"],
                    "expert_family_boundary_review_entry_ids": ["m_csa:712"],
                }
            },
            review_only_import_safety_audit={
                "metadata": {
                    "method": "review_only_import_safety_audit",
                    "countable_import_safe": True,
                    "total_new_countable_label_count": 0,
                }
            },
        )
        self.assertTrue(audit["metadata"]["deferral_ready"])
        self.assertEqual(audit["metadata"]["accepted_review_debt_overlap_count"], 0)
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            audit["metadata"]["strict_remap_guardrail_entry_ids"], ["m_csa:712"]
        )
        statuses = {row["entry_id"]: row["deferral_status"] for row in audit["rows"]}
        self.assertEqual(
            statuses["m_csa:712"],
            "deferred_strict_remap_family_boundary_review",
        )
        self.assertEqual(
            statuses["m_csa:718"],
            "deferred_structure_wide_only_evidence",
        )

    def test_mechanism_ontology_gap_audit_is_review_only(self) -> None:
        queue = {
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
                    "mechanism_text_snippets": ["ATP phosphoryl transfer."],
                },
                {
                    "rank": 2,
                    "entry_id": "m_csa:777",
                    "entry_name": "alanine racemase",
                    "recommended_action": "needs_review",
                    "top1_fingerprint_id": "plp_dependent_transaminase",
                    "top1_ontology_family": "plp_chemistry",
                    "mechanism_text_snippets": [],
                },
                {
                    "rank": 3,
                    "entry_id": "m_csa:1",
                    "entry_name": "plain hydrolase",
                    "recommended_action": "hold",
                },
            ]
        }
        repair = {
            "rows": [
                {
                    "entry_id": "m_csa:655",
                    "quality_risk_flags": [
                        "cofactor_family_ambiguity",
                        "text_leakage_or_nonlocal_evidence_risk",
                    ],
                }
            ]
        }

        audit = audit_mechanism_ontology_gaps(
            queue,
            expert_label_decision_repair_candidates=repair,
            expert_label_decision_local_evidence_gap_audit={
                "metadata": {
                    "method": "expert_label_decision_local_evidence_gap_audit"
                },
                "rows": [
                    {
                        "entry_id": "m_csa:655",
                        "local_evidence_gap_classes": [
                            "reaction_substrate_mismatch_review_required",
                            "selected_structure_residue_support_shortfall",
                        ],
                        "recommended_next_action": (
                            "route_to_reaction_substrate_expert_review"
                        ),
                    },
                    {
                        "entry_id": "m_csa:777",
                        "local_evidence_gap_classes": [
                            "local_evidence_review_only_not_countable"
                        ],
                        "recommended_next_action": (
                            "keep_local_evidence_review_only_until_expert_resolution"
                        ),
                    }
                ],
            },
            max_rows=0,
        )

        self.assertFalse(audit["metadata"]["ontology_update_ready"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(audit["metadata"]["candidate_scope_signal_count"], 2)
        self.assertEqual(
            audit["metadata"]["scope_signal_counts"]["transferase_phosphoryl"],
            1,
        )
        rows = {row["entry_id"]: row for row in audit["rows"]}
        self.assertIn("isomerase", rows["m_csa:777"]["scope_signals"])
        self.assertIn(
            "reaction_substrate_mismatch_review_required",
            rows["m_csa:655"]["ontology_update_blockers"],
        )
        self.assertIn(
            "local_evidence_gap_unresolved",
            rows["m_csa:655"]["ontology_update_blockers"],
        )
        self.assertEqual(
            audit["metadata"]["local_evidence_gap_context_entry_count"], 2
        )
        self.assertEqual(
            audit["metadata"]["local_evidence_gap_class_counts"][
                "selected_structure_residue_support_shortfall"
            ],
            1,
        )
        self.assertFalse(rows["m_csa:655"]["countable_label_candidate"])

        capped = audit_mechanism_ontology_gaps(
            queue,
            expert_label_decision_repair_candidates=repair,
            expert_label_decision_local_evidence_gap_audit={
                "metadata": {
                    "method": "expert_label_decision_local_evidence_gap_audit"
                },
                "rows": [
                    {
                        "entry_id": "m_csa:777",
                        "local_evidence_gap_classes": [
                            "local_evidence_review_only_not_countable"
                        ],
                    }
                ],
            },
            max_rows=1,
        )
        self.assertEqual(capped["metadata"]["priority_local_evidence_gap_added_count"], 1)
        self.assertEqual(capped["metadata"]["emitted_row_count"], 2)
        self.assertIn("m_csa:777", [row["entry_id"] for row in capped["rows"]])

    def test_atp_phosphoryl_transfer_family_expansion_maps_expert_hints_review_only(
        self,
    ) -> None:
        target_rows = [
            ("m_csa:35", "phosphorylase kinase", "ePK"),
            ("m_csa:592", "glucokinase", "ASKHA"),
            ("m_csa:498", "glutathione synthase", "ATP-grasp"),
            ("m_csa:603", "pyruvate dehydrogenase kinase", "GHKL"),
            ("m_csa:588", "thymidine kinase", "dNK"),
            ("m_csa:637", "nucleoside-diphosphate kinase", "NDK"),
            ("m_csa:365", "Phosphofructokinase I", "PfkA"),
            ("m_csa:663", "ribokinase", "PfkB"),
            ("m_csa:654", "CDP-ME kinase", "GHMP"),
            ("m_csa:151", "pteridine diphosphokinase", "HPPK"),
        ]
        decision_batch = {
            "review_items": [
                {
                    "entry_id": entry_id,
                    "entry_name": name,
                    "mismatch_context": {
                        "entry_id": entry_id,
                        "entry_name": name,
                        "top1_fingerprint_id": "metal_dependent_hydrolase",
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
                for entry_id, name, hint in target_rows
            ]
        }

        expansion = build_atp_phosphoryl_transfer_family_expansion(
            reaction_substrate_mismatch_decision_batch=decision_batch,
            reaction_substrate_mismatch_review_export={"review_items": []},
            family_propagation_guardrails={"rows": []},
            active_learning_queue={"metadata": {}, "rows": []},
            adversarial_negatives={"metadata": {}, "rows": []},
        )

        self.assertTrue(expansion["metadata"]["boundary_guardrail_ready"])
        self.assertEqual(
            expansion["metadata"]["mapped_required_family_ids"],
            ["askha", "atp_grasp", "dnk", "epk", "ghkl", "ghmp", "ndk", "pfka", "pfkb"],
        )
        self.assertEqual(expansion["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(expansion["metadata"]["non_target_expert_hint_count"], 1)
        rows = {row["entry_id"]: row for row in expansion["rows"]}
        self.assertEqual(rows["m_csa:35"]["family_id"], "epk")
        self.assertIn(
            "review_only_reaction_substrate_mismatch_lane",
            rows["m_csa:35"]["non_countable_blockers"],
        )
        self.assertFalse(rows["m_csa:35"]["countable_label_candidate"])

    def test_atp_family_expansion_keeps_unsupported_mapping_non_countable(self) -> None:
        expansion = build_atp_phosphoryl_transfer_family_expansion(
            reaction_substrate_mismatch_decision_batch={
                "review_items": [
                    {
                        "entry_id": "m_csa:588",
                        "entry_name": "thymidine kinase",
                        "mismatch_context": {
                            "top1_fingerprint_id": "metal_dependent_hydrolase",
                            "mismatch_reasons": ["kinase_name_with_hydrolase_top1"],
                        },
                        "decision": {
                            "action": "no_decision",
                            "label_type": "out_of_scope",
                            "review_status": "needs_expert_review",
                            "reaction_substrate_resolution": "needs_more_evidence",
                            "future_fingerprint_family_hint": "dNK",
                        },
                    }
                ]
            }
        )

        self.assertFalse(expansion["metadata"]["boundary_guardrail_ready"])
        self.assertEqual(expansion["metadata"]["unsupported_mapping_count"], 1)
        self.assertEqual(expansion["metadata"]["countable_label_candidate_count"], 0)
        self.assertFalse(expansion["rows"][0]["countable_label_candidate"])
        self.assertIn(
            "family_mapping_not_expert_supported",
            expansion["rows"][0]["non_countable_blockers"],
        )

    def test_sequence_similarity_failure_sets_track_mixed_clusters(self) -> None:
        clusters = {
            "metadata": {
                "method": "sequence_cluster_proxy_from_reference_uniprot",
                "cluster_count": 1,
                "cluster_source": "reference_uniprot_exact_set",
            },
            "clusters": [
                {
                    "sequence_cluster_id": "uniprot:P12345",
                    "cluster_source": "reference_uniprot_exact_set",
                    "entry_ids": ["m_csa:1", "m_csa:2"],
                }
            ],
        }
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="ser_his_acid_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="test",
            ),
            MechanismLabel(
                entry_id="m_csa:2",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="test",
            ),
        ]
        queue = {
            "rows": [
                {
                    "entry_id": "m_csa:2",
                    "recommended_action": "expert_label_decision_needed",
                    "top1_ontology_family": "hydrolysis",
                }
            ]
        }

        audit = audit_sequence_similarity_failure_sets(
            clusters,
            labels,
            active_learning_queue=queue,
        )

        self.assertEqual(audit["metadata"]["duplicate_cluster_count"], 1)
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 0)
        self.assertIn(
            "mixed_label_types_within_sequence_cluster",
            audit["rows"][0]["risk_flags"],
        )
        self.assertIn(
            "active_queue_cluster_member",
            audit["rows"][0]["risk_flags"],
        )

    def test_preview_promotion_readiness_warns_on_new_review_debt(self) -> None:
        acceptance = {
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
        preview_summary = {
            "metadata": {
                "blocker_count": 0,
                "latest_countable_label_count": 636,
                "total_accepted_new_label_count": 18,
                "all_active_queues_retain_unlabeled_candidates": True,
            }
        }
        current_debt = {
            "metadata": {
                "method": "review_debt_summary",
                "review_debt_count": 53,
                "needs_more_evidence_count": 37,
            }
        }
        preview_debt = {
            "metadata": {
                "method": "review_debt_summary",
                "review_debt_count": 61,
                "needs_more_evidence_count": 44,
                "new_review_debt_count": 1,
                "carried_review_debt_count": 1,
                "new_review_debt_entry_ids": ["m_csa:650"],
                "carried_review_debt_entry_ids": ["m_csa:494"],
                "recommended_next_action_counts_by_debt_status": {
                    "new": {"verify_local_cofactor_or_active_site_mapping": 1},
                    "carried": {"inspect_alternate_structure_or_cofactor_source": 1},
                },
            }
        }

        readiness = check_label_preview_promotion_readiness(
            acceptance,
            preview_summary,
            preview_debt,
            current_review_debt=current_debt,
        )

        self.assertTrue(readiness["metadata"]["mechanically_ready"])
        self.assertEqual(readiness["metadata"]["review_debt_delta"], 8)
        self.assertEqual(readiness["metadata"]["preview_new_review_debt_count"], 1)
        self.assertEqual(readiness["metadata"]["preview_new_review_debt_entry_ids"], ["m_csa:650"])
        self.assertEqual(
            readiness["metadata"]["preview_new_review_debt_next_action_counts"],
            {"verify_local_cofactor_or_active_site_mapping": 1},
        )
        self.assertEqual(readiness["metadata"]["promotion_recommendation"], "review_before_promoting")
        self.assertIn("review_debt_count_increased", readiness["review_warnings"])

        clean_preview = check_label_preview_promotion_readiness(
            {
                "metadata": {
                    **acceptance["metadata"],
                    "pending_review_count": 0,
                }
            },
            preview_summary,
            {"metadata": {"method": "review_debt_summary", "review_debt_count": 0}},
            current_review_debt={"metadata": {"review_debt_count": 0}},
        )
        self.assertTrue(clean_preview["gates"]["preview_debt_summary_present"])
        self.assertEqual(clean_preview["metadata"]["promotion_recommendation"], "promote_if_policy_allows")

        mismatched = check_label_preview_promotion_readiness(
            acceptance,
            {"metadata": {"blocker_count": 0, "latest_countable_label_count": 999}},
            preview_debt,
            current_review_debt=current_debt,
        )
        self.assertFalse(mismatched["gates"]["preview_summary_matches_acceptance"])
        self.assertFalse(mismatched["gates"]["preview_summary_retains_unlabeled_candidates"])
        self.assertIn("preview_summary_matches_acceptance", mismatched["blockers"])
        self.assertIn("preview_summary_retains_unlabeled_candidates", mismatched["blockers"])
        self.assertEqual(mismatched["metadata"]["promotion_recommendation"], "do_not_promote")

    def test_label_scaling_quality_audit_blocks_accepted_debt(self) -> None:
        acceptance = {
            "metadata": {
                "method": "label_batch_acceptance_check",
                "out_of_scope_false_non_abstentions": 0,
                "actionable_in_scope_failure_count": 0,
            }
        }
        readiness = {"metadata": {"promotion_recommendation": "review_before_promoting"}}
        review_debt = {
            "metadata": {
                "method": "review_debt_summary",
                "new_review_debt_entry_ids": ["m_csa:650", "m_csa:651"],
            }
        }
        review_gaps = {
            "metadata": {"method": "review_evidence_gap_analysis"},
            "rows": [
                {
                    "entry_id": "m_csa:650",
                    "entry_name": "phospholipase A1",
                    "decision_action": "mark_needs_more_evidence",
                    "decision_review_status": "needs_expert_review",
                    "coverage_status": "expected_structure_only",
                    "gap_reasons": ["target_not_top1", "counterevidence_present"],
                    "counterevidence_reasons": ["metal_supported_site_for_ser_his_seed"],
                    "target_fingerprint_id": "ser_his_acid_hydrolase",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_score": 0.61,
                    "mechanism_text_snippets": ["Ser-His hydrolase text with metal support."],
                },
                {
                    "entry_id": "m_csa:651",
                    "entry_name": "redox-like accepted control",
                    "decision_action": "accept_label",
                    "decision_review_status": "automation_curated",
                    "coverage_status": "expected_absent_from_structure",
                    "gap_reasons": [
                        "top1_below_abstention_threshold",
                        "expected_cofactor_absent_from_structure",
                    ],
                    "counterevidence_reasons": ["absent_flavin_context"],
                    "target_fingerprint_id": "flavin_dehydrogenase_reductase",
                    "top1_fingerprint_id": "flavin_dehydrogenase_reductase",
                    "top1_score": 0.25,
                    "mechanism_text_snippets": [
                        "Hydrolysis of a glycosidic bond is described without flavin evidence."
                    ],
                },
            ],
        }
        queue = {
            "metadata": {"all_unlabeled_rows_retained": True},
            "rows": [
                {
                    "entry_id": "m_csa:650",
                    "top1_ontology_family": "hydrolysis",
                    "recommended_action": "expert_label_decision_needed",
                },
                {"entry_id": "m_csa:651", "top1_ontology_family": "flavin_redox"},
            ],
        }
        guardrails = {
            "metadata": {
                "method": "family_propagation_guardrail_audit",
                "blocker_counts": {"close_cross_family_top1_top2": 1},
                "local_proxy_rule": "local proxies cannot promote above bronze",
            },
            "rows": [
                {
                    "entry_id": "m_csa:650",
                    "propagation_blockers": ["target_family_top1_family_mismatch"],
                }
            ],
        }
        hard_negatives = {"metadata": {"hard_negative_count": 0, "near_miss_count": 0}}
        decision_batch = {
            "review_items": [
                {"entry_id": "m_csa:650", "decision": {"action": "mark_needs_more_evidence"}},
                {"entry_id": "m_csa:651", "decision": {"action": "accept_label"}},
            ]
        }
        structure_mapping = {
            "metadata": {"issue_count": 1, "status_counts": {"structure_fetch_failed": 1}},
            "rows": [{"entry_id": "m_csa:651", "status": "structure_fetch_failed"}],
        }
        sequence_clusters = {
            "clusters": [
                {
                    "id": "cluster-a",
                    "entry_ids": ["m_csa:650", "m_csa:651"],
                }
            ]
        }
        alternate_scan = {
            "metadata": {
                "method": "review_debt_alternate_structure_scan",
                "expected_family_hit_entry_ids": ["m_csa:651"],
                "remapped_residue_position_entry_ids": ["m_csa:650"],
                "alternate_pdb_remapped_residue_position_entry_ids": ["m_csa:650"],
                "local_expected_family_hit_from_remap_entry_ids": [],
                "remapped_residue_position_structure_count": 2,
                "alternate_pdb_remapped_residue_position_structure_count": 2,
                "structure_wide_hit_without_local_support_entry_ids": ["m_csa:651"],
                "fetch_failure_count": 0,
            }
        }
        remap_local_audit = {
            "metadata": {
                "method": "review_debt_remap_local_lead_audit",
                "countable_label_candidate_count": 0,
                "strict_remap_guardrail_entry_ids": ["m_csa:650"],
                "expert_family_boundary_review_entry_ids": ["m_csa:650"],
                "local_structure_selection_rule_candidate_entry_ids": [],
                "decision_rule": "test rule",
            }
        }
        reaction_mismatch_audit = {
            "metadata": {
                "method": "reaction_substrate_mismatch_audit",
                "mismatch_count": 1,
                "mismatch_entry_ids": ["m_csa:650"],
                "mismatch_reason_counts": {"kinase_name_with_hydrolase_top1": 1},
            }
        }
        expert_label_decision_export = {
            "metadata": {
                "method": "expert_label_decision_review_export",
                "exported_count": 1,
                "exported_entry_ids": ["m_csa:650"],
                "countable_label_candidate_count": 0,
                "decision_counts": {"no_decision": 1},
                "export_ready": True,
                "quality_risk_flag_counts": {
                    "external_expert_decision_required": 1,
                    "ser_his_metal_boundary": 1,
                },
                "review_only_rule": "test review-only rule",
            },
            "review_items": [{"entry_id": "m_csa:650"}],
        }
        expert_label_decision_repair = {
            "metadata": {
                "method": "expert_label_decision_repair_candidate_summary",
                "candidate_count": 1,
                "candidate_entry_ids": ["m_csa:650"],
                "countable_label_candidate_count": 0,
                "repair_bucket_counts": {"ser_his_metal_boundary_review": 1},
            },
            "rows": [{"entry_id": "m_csa:650"}],
        }
        expert_label_decision_repair_guardrail = {
            "metadata": {
                "method": "expert_label_decision_repair_guardrail_audit",
                "guardrail_ready": True,
                "all_priority_lanes_non_countable": True,
                "priority_repair_row_count": 1,
                "local_expected_family_evidence_review_only_count": 0,
                "countable_label_candidate_count": 0,
            },
            "rows": [{"entry_id": "m_csa:650", "countable_label_candidate": False}],
        }
        expert_label_decision_local_gap = {
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
            "rows": [{"entry_id": "m_csa:650", "countable_label_candidate": False}],
        }
        expert_label_decision_local_export = {
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

        audit = audit_label_scaling_quality(
            acceptance,
            readiness,
            review_debt,
            review_gaps,
            queue,
            guardrails,
            hard_negatives,
            decision_batch=decision_batch,
            structure_mapping=structure_mapping,
            sequence_clusters=sequence_clusters,
            alternate_structure_scan=alternate_scan,
            remap_local_lead_audit=remap_local_audit,
            reaction_substrate_mismatch_audit=reaction_mismatch_audit,
            expert_label_decision_review_export=expert_label_decision_export,
            expert_label_decision_repair_candidates=expert_label_decision_repair,
            expert_label_decision_repair_guardrail_audit=(
                expert_label_decision_repair_guardrail
            ),
            expert_label_decision_local_evidence_gap_audit=(
                expert_label_decision_local_gap
            ),
            expert_label_decision_local_evidence_review_export=(
                expert_label_decision_local_export
            ),
            batch_id="test_preview",
        )

        self.assertEqual(audit["metadata"]["audit_recommendation"], "do_not_promote_until_quality_repair")
        self.assertEqual(audit["metadata"]["accepted_new_debt_entry_ids"], ["m_csa:651"])
        self.assertEqual(audit["metadata"]["accepted_clean_label_entry_ids"], [])
        self.assertIn("accepted_new_labels_without_review_debt", audit["blockers"])
        self.assertIn("cofactor_family_ambiguity", audit["metadata"]["issue_class_counts"])
        self.assertEqual(audit["metadata"]["near_duplicate_audit_status"], "observed")
        self.assertTrue(audit["metadata"]["alternate_structure_scan_present"])
        self.assertEqual(
            audit["metadata"]["alternate_structure_scan_expected_family_hit_entry_ids"],
            ["m_csa:651"],
        )
        self.assertEqual(
            audit["metadata"][
                "alternate_structure_scan_local_expected_family_hit_entry_ids"
            ],
            [],
        )
        self.assertEqual(
            audit["metadata"][
                "alternate_structure_scan_alternate_pdb_remapped_residue_position_entry_ids"
            ],
            ["m_csa:650"],
        )
        self.assertEqual(
            audit["metadata"][
                "alternate_structure_scan_alternate_pdb_remapped_residue_position_structure_count"
            ],
            2,
        )
        self.assertEqual(
            audit["metadata"][
                "alternate_structure_scan_structure_wide_hit_without_local_support_entry_ids"
            ],
            ["m_csa:651"],
        )
        self.assertIn("candidate_entries_share_sequence_clusters", audit["review_warnings"])
        self.assertIn("alternate_structure_hits_lack_local_support", audit["review_warnings"])
        self.assertIn("remap_local_leads_require_strict_guardrail", audit["review_warnings"])
        self.assertIn("reaction_substrate_mismatch_audit_hits", audit["review_warnings"])
        self.assertIn(
            "expert_label_decision_rows_require_external_review",
            audit["review_warnings"],
        )
        self.assertTrue(audit["gates"]["remap_local_leads_remain_review_only"])
        self.assertTrue(
            audit["gates"][
                "expert_label_decision_review_export_retains_review_only_lanes"
            ]
        )
        self.assertTrue(
            audit["gates"][
                "expert_label_decision_repair_candidates_cover_review_only_lanes"
            ]
        )
        self.assertTrue(
            audit["gates"][
                "expert_label_decision_repair_guardrail_keeps_priority_lanes_non_countable"
            ]
        )
        self.assertTrue(
            audit["gates"]["expert_label_decision_local_evidence_gaps_audited"]
        )
        self.assertEqual(
            audit["metadata"][
                "expert_label_decision_repair_candidates_missing_entry_ids"
            ],
            [],
        )
        self.assertEqual(
            audit["metadata"]["remap_local_lead_audit_strict_guardrail_entry_ids"],
            ["m_csa:650"],
        )
        self.assertTrue(
            audit["metadata"][
                "expert_label_decision_local_evidence_gap_audit_present"
            ]
        )
        self.assertTrue(
            audit["gates"][
                "expert_label_decision_local_evidence_review_export_ready"
            ]
        )
        self.assertTrue(
            audit["metadata"][
                "expert_label_decision_local_evidence_review_export_present"
            ]
        )
        failure_modes = {row["id"]: row for row in audit["failure_modes"]}
        self.assertEqual(failure_modes["sibling_mechanism_confusion"]["issue_count"], 1)
        self.assertEqual(
            failure_modes[
                "conservative_remap_local_evidence_without_explicit_alt_positions"
            ]["entry_ids"],
            ["m_csa:650"],
        )
        self.assertEqual(
            failure_modes["reaction_direction_or_substrate_class_mismatch"][
                "entry_ids"
            ],
            ["m_csa:650", "m_csa:651"],
        )
        self.assertEqual(
            failure_modes["text_leakage_without_mechanistic_evidence"]["entry_ids"],
            ["m_csa:650", "m_csa:651"],
        )
        self.assertEqual(failure_modes["sequence_family_leakage"]["status"], "guardrail_active")
        self.assertEqual(
            failure_modes["overcounted_paralogs_or_near_duplicates"]["entry_ids"],
            ["m_csa:650", "m_csa:651"],
        )
        self.assertEqual(
            failure_modes["expert_label_decision_review_only_debt"]["entry_ids"],
            ["m_csa:650"],
        )
        self.assertEqual(
            failure_modes["expert_label_decision_review_only_debt"]["evidence"][
                "quality_risk_flag_counts"
            ]["ser_his_metal_boundary"],
            1,
        )
        self.assertEqual(
            failure_modes["expert_label_decision_review_only_debt"]["evidence"][
                "repair_bucket_counts"
            ]["ser_his_metal_boundary_review"],
            1,
        )
        self.assertTrue(
            failure_modes["expert_label_decision_review_only_debt"]["evidence"][
                "repair_guardrail_audit_present"
            ]
        )
        self.assertTrue(
            failure_modes["expert_label_decision_review_only_debt"]["evidence"][
                "local_evidence_gap_audit_present"
            ]
        )

    def test_scaling_audit_classifies_counterevidence_deferrals(self) -> None:
        audit = audit_label_scaling_quality(
            {
                "metadata": {
                    "method": "label_batch_acceptance_check",
                    "out_of_scope_false_non_abstentions": 0,
                    "actionable_in_scope_failure_count": 0,
                }
            },
            {"metadata": {"promotion_recommendation": "review_before_promoting"}},
            {
                "metadata": {
                    "method": "review_debt_summary",
                    "new_review_debt_entry_ids": ["m_csa:771"],
                }
            },
            {
                "metadata": {"method": "review_evidence_gap_analysis"},
                "rows": [
                    {
                        "entry_id": "m_csa:771",
                        "entry_name": "2-hydroxymuconate-semialdehyde hydrolase",
                        "decision_action": "mark_needs_more_evidence",
                        "decision_review_status": "needs_expert_review",
                        "coverage_status": "not_required",
                        "gap_reasons": [
                            "counterevidence_present",
                            "review_marked_needs_more_evidence",
                        ],
                        "counterevidence_reasons": [
                            "ser_his_seed_missing_triad_coherence"
                        ],
                        "target_fingerprint_id": "ser_his_acid_hydrolase",
                        "top1_fingerprint_id": "ser_his_acid_hydrolase",
                        "top1_score": 0.4385,
                        "mechanism_text_snippets": [
                            "Ser-His-Asp catalytic triad text with weak role coherence."
                        ],
                    }
                ],
            },
            {"metadata": {"all_unlabeled_rows_retained": True}, "rows": []},
            {"metadata": {"method": "family_propagation_guardrail_audit"}, "rows": []},
            {"metadata": {"hard_negative_count": 0, "near_miss_count": 0}},
        )

        self.assertIn("text_leakage_risk", audit["rows"][0]["issue_classes"])
        self.assertEqual(audit["metadata"]["unclassified_new_review_debt_entry_ids"], [])

    def test_provisional_review_batch_imports_without_expert_claim(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="Existing boundary-control label for review testing.",
            )
        ]
        review = {
            "metadata": {"method": "expert_review_export"},
            "review_items": [
                {
                    "entry_id": "m_csa:1",
                    "entry_name": "existing boundary enzyme",
                    "current_label": labels[0].to_dict(),
                    "queue_context": {
                        "entry_id": "m_csa:1",
                        "entry_name": "existing boundary enzyme",
                        "current_label_type": "out_of_scope",
                        "top1_fingerprint_id": "heme_peroxidase_oxidase",
                        "top1_score": 0.405,
                        "abstain_threshold": 0.4115,
                        "counterevidence_reasons": ["absent_heme_context"],
                    },
                    "decision": {"action": "no_decision"},
                },
                {
                    "entry_id": "m_csa:10",
                    "entry_name": "new PLP enzyme",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:10",
                        "entry_name": "new PLP enzyme",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "plp_dependent_enzyme",
                        "top1_score": 0.62,
                        "abstain_threshold": 0.5,
                        "cofactor_evidence_level": "ligand_supported",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "PLP dependent chemistry supports a seed-fingerprint assignment."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                },
                {
                    "entry_id": "m_csa:11",
                    "entry_name": "new cobalamin enzyme",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:11",
                        "entry_name": "new cobalamin enzyme",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "ser_his_acid_hydrolase",
                        "top1_score": 0.38,
                        "abstain_threshold": 0.5,
                        "cofactor_evidence_level": "not_required",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "A cobalamin radical mechanism begins with Co-C5 bond cleavage."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                },
                {
                    "entry_id": "m_csa:12",
                    "entry_name": "structure-wide cobalamin enzyme",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:12",
                        "entry_name": "structure-wide cobalamin enzyme",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "cobalamin_radical_rearrangement",
                        "top1_score": 0.62,
                        "abstain_threshold": 0.5,
                        "cofactor_evidence_level": "structure_only",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "A cobalamin radical rearrangement uses adenosylcobalamin."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                },
            ],
        }
        batch = build_provisional_review_decision_batch(
            review,
            batch_id="test_batch",
            reviewer="automation_label_factory_test",
            max_boundary_controls=1,
        )
        self.assertEqual(batch["metadata"]["decision_counts"]["accept_label"], 1)
        self.assertEqual(batch["metadata"]["decision_counts"]["mark_needs_more_evidence"], 3)

        imported = import_expert_review_decisions(labels, batch)
        imported_by_entry = {label.entry_id: label for label in imported}
        self.assertEqual(imported_by_entry["m_csa:1"].review_status, "needs_expert_review")
        self.assertEqual(imported_by_entry["m_csa:10"].review_status, "automation_curated")
        self.assertEqual(imported_by_entry["m_csa:10"].tier, "bronze")
        self.assertIn(
            "label_factory_review_import",
            imported_by_entry["m_csa:10"].evidence["sources"],
        )
        self.assertNotIn(
            "expert_review_import",
            imported_by_entry["m_csa:10"].evidence["sources"],
        )
        self.assertEqual(imported_by_entry["m_csa:11"].review_status, "needs_expert_review")
        self.assertEqual(
            imported_by_entry["m_csa:11"].fingerprint_id,
            "cobalamin_radical_rearrangement",
        )
        self.assertEqual(imported_by_entry["m_csa:12"].review_status, "needs_expert_review")
        countable = countable_benchmark_labels(imported)
        self.assertEqual({label.entry_id for label in countable}, {"m_csa:10"})
        countable_import = import_countable_review_decisions(labels, batch)
        self.assertEqual(
            {label.entry_id for label in countable_import},
            {"m_csa:1", "m_csa:10"},
        )
        self.assertEqual(
            {label.entry_id: label.review_status for label in countable_import},
            {"m_csa:1": "automation_curated", "m_csa:10": "automation_curated"},
        )
        acceptance = check_label_batch_acceptance(
            baseline_labels=labels,
            review_state_labels=imported,
            countable_labels=countable_import,
            evaluation={"metadata": {"out_of_scope_false_non_abstentions": 0}},
            hard_negatives={"metadata": {"hard_negative_count": 0, "near_miss_count": 0}},
            in_scope_failures={"metadata": {"actionable_failure_count": 0}},
            label_factory_gate={"metadata": {"automation_ready_for_next_label_batch": True}},
        )
        self.assertTrue(acceptance["metadata"]["accepted_for_counting"])
        self.assertEqual(acceptance["metadata"]["accepted_new_label_count"], 1)

    def test_targeted_review_deferral_resolves_candidate_without_counting(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="Existing out-of-scope baseline label for resolution testing.",
            )
        ]
        review = {
            "metadata": {"method": "expert_review_export"},
            "review_items": [
                {
                    "entry_id": "m_csa:2",
                    "entry_name": "cobalamin gap enzyme",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:2",
                        "entry_name": "cobalamin gap enzyme",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "ser_his_acid_hydrolase",
                        "top1_score": 0.38,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "not_required",
                        "counterevidence_reasons": ["ser_his_seed_missing_triad_coherence"],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "A cobalamin radical mechanism begins with Co-C5 bond cleavage."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                },
                {
                    "entry_id": "m_csa:3",
                    "entry_name": "lower-priority boundary",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:3",
                        "entry_name": "lower-priority boundary",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "plp_dependent_enzyme",
                        "top1_score": 0.52,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "ligand_supported",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": ["PLP chemistry is supported locally."],
                    },
                    "decision": {"action": "no_decision"},
                },
            ],
        }
        batch = build_provisional_review_decision_batch(
            review,
            batch_id="targeted_deferral",
            reviewer="automation_label_factory_test",
            entry_ids={"m_csa:2"},
        )
        self.assertEqual(len(batch["review_items"]), 1)
        self.assertEqual(batch["metadata"]["selected_entry_ids"], ["m_csa:2"])
        self.assertEqual(batch["metadata"]["decision_counts"], {"mark_needs_more_evidence": 1})
        self.assertEqual(
            batch["metadata"]["decision_entry_ids"]["mark_needs_more_evidence"],
            ["m_csa:2"],
        )

        review_state = import_expert_review_decisions(labels, batch)
        countable = import_countable_review_decisions(labels, batch)
        check = check_label_review_resolution(
            baseline_labels=labels,
            review_state_labels=review_state,
            countable_labels=countable,
            review_artifact=batch,
            label_expansion_candidates={"rows": [{"entry_id": "m_csa:2"}]},
            label_factory_gate={
                "metadata": {"automation_ready_for_next_label_batch": True}
            },
        )
        self.assertTrue(check["metadata"]["resolved_for_scaling"])
        self.assertEqual(check["metadata"]["accepted_new_label_count"], 0)
        self.assertEqual(check["metadata"]["needs_more_evidence_entry_ids"], ["m_csa:2"])
        self.assertEqual(check["metadata"]["remaining_unresolved_candidate_count"], 0)
        self.assertEqual({label.entry_id for label in countable}, {"m_csa:1"})

        retrieval = {
            "results": [
                {
                    "entry_id": "m_csa:2",
                    "entry_name": "cobalamin gap enzyme",
                    "ligand_context": {
                        "cofactor_families": [],
                        "ligand_codes": ["PGO"],
                        "structure_cofactor_families": ["cobalamin"],
                        "structure_ligand_codes": ["PGO", "B12"],
                        "structure_ligands": [
                            {
                                "code": "B12",
                                "instance_count": 1,
                                "min_distance_to_active_site": 8.349,
                            }
                        ],
                    },
                    "mechanism_text_snippets": [
                        "A cobalamin radical mechanism begins with Co-C5 bond cleavage."
                    ],
                    "top_fingerprints": [
                        {
                            "fingerprint_id": "ser_his_acid_hydrolase",
                            "score": 0.38,
                            "counterevidence_reasons": [
                                "ser_his_seed_missing_triad_coherence"
                            ],
                        },
                        {
                            "fingerprint_id": "cobalamin_radical_rearrangement",
                            "score": 0.37,
                        },
                    ],
                }
            ]
        }
        gaps = analyze_review_evidence_gaps(retrieval, batch)
        self.assertEqual(gaps["metadata"]["gap_count"], 1)
        self.assertEqual(gaps["rows"][0]["coverage_status"], "expected_structure_only")
        self.assertEqual(gaps["rows"][0]["nearest_expected_ligand_distance_angstrom"], 8.349)
        self.assertIn("expected_cofactor_not_local", gaps["rows"][0]["gap_reasons"])

    def test_provisional_review_defers_ser_his_metal_boundary(self) -> None:
        review = {
            "metadata": {"method": "expert_review_export"},
            "review_items": [
                {
                    "entry_id": "m_csa:650",
                    "entry_name": "phospholipase A1",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:650",
                        "entry_name": "phospholipase A1",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "metal_dependent_hydrolase",
                        "top1_score": 0.6085,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "ligand_supported",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "The mechanism is analogous to serine hydrolases. His acts as a base to deprotonate Ser for nucleophilic attack."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                }
            ],
        }
        batch = build_provisional_review_decision_batch(review)
        decision = batch["review_items"][0]["decision"]

        self.assertEqual(decision["action"], "mark_needs_more_evidence")
        self.assertEqual(decision["fingerprint_id"], "ser_his_acid_hydrolase")
        self.assertIn("top retrieval favored metal_dependent_hydrolase", decision["rationale"])

    def test_provisional_batch_defers_ser_his_hydrolase_text_with_counterevidence(self) -> None:
        review = {
            "metadata": {"method": "expert_review_export"},
            "review_items": [
                {
                    "entry_id": "m_csa:519",
                    "entry_name": "triacylglycerol lipase",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:519",
                        "entry_name": "triacylglycerol lipase",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "ser_his_acid_hydrolase",
                        "top1_score": 0.6199,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "not_required",
                        "counterevidence_reasons": [
                            "metal_supported_site_for_ser_his_seed"
                        ],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "This alpha-beta hydrolase uses a classical Ser-His-Asp triad mechanism."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                }
            ],
        }
        batch = build_provisional_review_decision_batch(review)
        decision = batch["review_items"][0]["decision"]
        self.assertEqual(decision["action"], "mark_needs_more_evidence")
        self.assertEqual(decision["label_type"], "seed_fingerprint")
        self.assertEqual(decision["fingerprint_id"], "ser_his_acid_hydrolase")
        self.assertIn("counterevidence remains", decision["rationale"])

    def test_provisional_batch_does_not_count_metal_transferase_as_hydrolase(self) -> None:
        review = {
            "metadata": {"method": "expert_review_export"},
            "review_items": [
                {
                    "entry_id": "m_csa:568",
                    "entry_name": "lipopolysaccharide 3-alpha-galactosyltransferase",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:568",
                        "entry_name": "lipopolysaccharide 3-alpha-galactosyltransferase",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "metal_dependent_hydrolase",
                        "top1_score": 0.5672,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "ligand_supported",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "The glycosyltransferase reaction proceeds through UDP-galactose transfer."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                },
                {
                    "entry_id": "m_csa:577",
                    "entry_name": "inositol-phosphate phosphatase",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:577",
                        "entry_name": "inositol-phosphate phosphatase",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "metal_dependent_hydrolase",
                        "top1_score": 0.4288,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "role_inferred",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "Two Mg(II) ions activate water to cleave the phosphate-inositolate bond."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                },
            ],
        }
        batch = build_provisional_review_decision_batch(review)
        decisions = {
            item["entry_id"]: item["decision"] for item in batch["review_items"]
        }
        self.assertEqual(decisions["m_csa:568"]["action"], "mark_needs_more_evidence")
        self.assertEqual(decisions["m_csa:568"]["label_type"], "out_of_scope")
        self.assertIsNone(decisions["m_csa:568"]["fingerprint_id"])
        self.assertIn("high-scoring metal-hydrolase boundary", decisions["m_csa:568"]["rationale"])
        self.assertEqual(decisions["m_csa:577"]["action"], "mark_needs_more_evidence")
        self.assertEqual(
            decisions["m_csa:577"]["fingerprint_id"],
            "metal_dependent_hydrolase",
        )

    def test_provisional_batch_defers_role_inferred_metal_hydrolase(self) -> None:
        review = {
            "metadata": {"method": "expert_review_export"},
            "review_items": [
                {
                    "entry_id": "m_csa:836",
                    "entry_name": "exodeoxyribonuclease (lambda-induced)",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:836",
                        "entry_name": "exodeoxyribonuclease (lambda-induced)",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "metal_dependent_hydrolase",
                        "top1_score": 0.58,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "role_inferred",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "A three-metal dissociative hydrolysis mechanism activates water to cleave phosphate."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                }
            ],
        }
        batch = build_provisional_review_decision_batch(review)
        decision = batch["review_items"][0]["decision"]

        self.assertEqual(decision["action"], "mark_needs_more_evidence")
        self.assertEqual(decision["fingerprint_id"], "metal_dependent_hydrolase")
        self.assertIn("rather than local ligand support", decision["rationale"])

    def test_provisional_batch_defers_seed_label_with_structural_blockers(self) -> None:
        review = {
            "metadata": {"method": "expert_review_export"},
            "review_items": [
                {
                    "entry_id": "m_csa:567",
                    "entry_name": "glucose oxidase",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:567",
                        "entry_name": "glucose oxidase",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "flavin_dehydrogenase_reductase",
                        "top1_score": 0.685,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "ligand_supported",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [
                            "geometry_status_not_ok",
                            "fewer_than_three_resolved_residues",
                        ],
                        "mechanism_text_snippets": [
                            "Glucose oxidase uses FAD for redox chemistry."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                }
            ],
        }
        batch = build_provisional_review_decision_batch(review)
        decision = batch["review_items"][0]["decision"]
        self.assertEqual(decision["action"], "mark_needs_more_evidence")
        self.assertEqual(decision["fingerprint_id"], "flavin_dehydrogenase_reductase")
        self.assertIn("not sufficiently resolved", decision["rationale"])

    def test_provisional_batch_defers_non_abstaining_boundary_negative(self) -> None:
        review = {
            "metadata": {"method": "expert_review_export"},
            "review_items": [
                {
                    "entry_id": "m_csa:553",
                    "entry_name": "N-acetylneuraminate lyase",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:553",
                        "entry_name": "N-acetylneuraminate lyase",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "heme_peroxidase_oxidase",
                        "top1_score": 0.4135,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "absent",
                        "counterevidence_reasons": ["absent_heme_context"],
                        "readiness_blockers": ["fewer_than_three_resolved_residues"],
                        "mechanism_text_snippets": [
                            "A lyase mechanism proceeds through a lysine Schiff-base intermediate."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                }
            ],
        }
        batch = build_provisional_review_decision_batch(review)
        decision = batch["review_items"][0]["decision"]
        self.assertEqual(decision["action"], "mark_needs_more_evidence")
        self.assertEqual(decision["label_type"], "out_of_scope")
        self.assertIn("non-abstaining boundary candidate", decision["rationale"])

    def test_provisional_batch_defers_below_floor_evidence_limited_negative(self) -> None:
        review = {
            "metadata": {"method": "expert_review_export"},
            "review_items": [
                {
                    "entry_id": "m_csa:653",
                    "entry_name": "diphosphate phosphotransferase",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:653",
                        "entry_name": "diphosphate phosphotransferase",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "metal_dependent_hydrolase",
                        "top1_score": 0.3642,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "absent",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "A phosphate transfer mechanism is stabilized by Mg2+."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                },
                {
                    "entry_id": "m_csa:666",
                    "entry_name": "clean out-of-scope control",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:666",
                        "entry_name": "clean out-of-scope control",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "ser_his_acid_hydrolase",
                        "top1_score": 0.2,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "not_required",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "No current seed fingerprint has enough retrieval support."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                },
            ],
        }
        batch = build_provisional_review_decision_batch(review)
        decisions = {
            item["entry_id"]: item["decision"] for item in batch["review_items"]
        }

        self.assertEqual(decisions["m_csa:653"]["action"], "mark_needs_more_evidence")
        self.assertEqual(decisions["m_csa:653"]["label_type"], "out_of_scope")
        self.assertIn("not a clean countable out-of-scope negative", decisions["m_csa:653"]["rationale"])
        self.assertEqual(decisions["m_csa:666"]["action"], "accept_label")
        self.assertEqual(decisions["m_csa:666"]["label_type"], "out_of_scope")

    def test_provisional_batch_defers_low_score_local_heme_boundary_negative(self) -> None:
        review = {
            "metadata": {"method": "expert_review_export"},
            "review_items": [
                {
                    "entry_id": "m_csa:986",
                    "entry_name": "Thiosulfate dehydrogenase",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:986",
                        "entry_name": "Thiosulfate dehydrogenase",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "heme_peroxidase_oxidase",
                        "top1_score": 0.3935,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "ligand_supported",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "Cys123 bound to heme acts as an electron relay during redox turnover."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                }
            ],
        }
        batch = build_provisional_review_decision_batch(review)
        decision = batch["review_items"][0]["decision"]

        self.assertEqual(decision["action"], "mark_needs_more_evidence")
        self.assertEqual(decision["label_type"], "out_of_scope")
        self.assertIsNone(decision["fingerprint_id"])
        self.assertIn("local ligand_supported evidence", decision["rationale"])
        self.assertIn("clean out-of-scope negative", decision["rationale"])

    def test_provisional_batch_defers_ser_his_boundary_without_triad_text(self) -> None:
        review = {
            "metadata": {"method": "expert_review_export"},
            "review_items": [
                {
                    "entry_id": "m_csa:602",
                    "entry_name": "6-deoxyerythronolide-B synthase",
                    "current_label": None,
                    "queue_context": {
                        "entry_id": "m_csa:602",
                        "entry_name": "6-deoxyerythronolide-B synthase",
                        "label_state": "unlabeled",
                        "top1_fingerprint_id": "ser_his_acid_hydrolase",
                        "top1_score": 0.9052,
                        "abstain_threshold": 0.4115,
                        "cofactor_evidence_level": "not_required",
                        "counterevidence_reasons": [],
                        "readiness_blockers": [],
                        "mechanism_text_snippets": [
                            "The catalytic triad consists of Asp, His, and Ser, but the synthase elongates an acyl carrier protein-bound polyketide chain."
                        ],
                    },
                    "decision": {"action": "no_decision"},
                }
            ],
        }
        batch = build_provisional_review_decision_batch(review)
        decision = batch["review_items"][0]["decision"]
        self.assertEqual(decision["action"], "mark_needs_more_evidence")
        self.assertEqual(decision["label_type"], "out_of_scope")
        self.assertIn("Ser-His hydrolase boundary", decision["rationale"])

    def test_adversarial_negative_controls_use_more_than_threshold(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:9",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="example rationale long enough for adversarial negative",
            )
        ]
        retrieval = {
            "results": [
                {
                    "entry_id": "m_csa:9",
                    "entry_name": "near-boundary control",
                    "top_fingerprints": [
                        {
                            "fingerprint_id": "metal_dependent_hydrolase",
                            "score": 0.49,
                            "cofactor_evidence_level": "ligand_supported",
                            "mechanistic_coherence_score": 0.9,
                            "counterevidence_reasons": ["nonhydrolytic_metal_transfer"],
                        },
                        {
                            "fingerprint_id": "flavin_dehydrogenase_reductase",
                            "score": 0.47,
                        },
                    ],
                }
            ]
        }
        controls = build_adversarial_negative_controls(
            retrieval,
            labels,
            abstain_threshold=0.5,
        )
        self.assertEqual(controls["metadata"]["control_count"], 1)
        axes = set(controls["rows"][0]["control_axes"])
        self.assertIn("threshold_boundary", axes)
        self.assertIn("ontology_family_boundary", axes)
        self.assertIn("cofactor_mimic", axes)

    def test_family_propagation_guardrails_block_cross_family_proxy_labels(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="medium",
                rationale="example rationale long enough for propagation audit",
            )
        ]
        geometry = {
            "entries": [
                {"entry_id": "m_csa:8", "entry_name": "unlabeled proxy"},
                {"entry_id": "m_csa:9", "entry_name": "adenylate kinase proxy"},
            ]
        }
        retrieval = {
            "results": [
                {
                    "entry_id": "m_csa:1",
                    "entry_name": "labeled mismatch",
                    "top_fingerprints": [
                        {"fingerprint_id": "flavin_dehydrogenase_reductase", "score": 0.5},
                        {"fingerprint_id": "metal_dependent_hydrolase", "score": 0.49},
                    ],
                },
                {
                    "entry_id": "m_csa:8",
                    "entry_name": "unlabeled proxy",
                    "mechanism_text_count": 1,
                    "mechanism_text_snippets": ["Proxy mechanism text."],
                    "top_fingerprints": [
                        {"fingerprint_id": "plp_dependent_enzyme", "score": 0.6}
                    ],
                },
                {
                    "entry_id": "m_csa:9",
                    "entry_name": "adenylate kinase proxy",
                    "mechanism_text_count": 1,
                    "mechanism_text_snippets": [
                        "ATP gamma phosphate is transferred to the acceptor substrate."
                    ],
                    "top_fingerprints": [
                        {"fingerprint_id": "metal_dependent_hydrolase", "score": 0.62}
                    ],
                },
            ]
        }
        guardrails = build_family_propagation_guardrails(geometry, retrieval, labels)
        rows = {row["entry_id"]: row for row in guardrails["rows"]}
        decisions = {entry_id: row["propagation_decision"] for entry_id, row in rows.items()}
        self.assertEqual(decisions["m_csa:1"], "block_family_propagation")
        self.assertEqual(decisions["m_csa:8"], "bronze_review_only")
        self.assertEqual(decisions["m_csa:9"], "block_propagation_pending_review")
        self.assertIn("reaction_substrate_mismatch", rows["m_csa:9"]["propagation_blockers"])
        self.assertIn(
            "kinase_name_with_hydrolase_top1",
            rows["m_csa:9"]["reaction_substrate_mismatch_reasons"],
        )
        self.assertEqual(guardrails["metadata"]["reaction_substrate_mismatch_count"], 1)
        self.assertEqual(
            guardrails["metadata"]["reaction_substrate_mismatch_label_state_counts"],
            {"unlabeled": 1},
        )
        self.assertIn("source_guardrails", guardrails["metadata"])

    def test_group_hard_negative_controls(self) -> None:
        groups = group_hard_negative_controls(
            [
                {
                    "entry_id": "m_csa:2",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_score": 0.6,
                    "cofactor_evidence_level": "role_inferred",
                    "hard_negative_reason": "metal_role_overlap_without_confirmed_hydrolysis",
                    "component_scores": {
                        "counterevidence_reasons": [
                            "role_inferred_metal_missing_water_activation_role"
                        ]
                    },
                },
                {
                    "entry_id": "m_csa:3",
                    "top1_fingerprint_id": "metal_dependent_hydrolase",
                    "top1_score": 0.5,
                    "cofactor_evidence_level": "role_inferred",
                    "hard_negative_reason": "metal_role_overlap_without_confirmed_hydrolysis",
                    "component_scores": {
                        "counterevidence_reasons": [
                            "role_inferred_metal_missing_water_activation_role",
                            "role_inferred_metal_low_pocket_support",
                        ]
                    },
                },
                {
                    "entry_id": "m_csa:4",
                    "top1_fingerprint_id": "heme_peroxidase_oxidase",
                    "top1_score": 0.55,
                    "cofactor_evidence_level": "absent",
                    "hard_negative_reason": "high_score_out_of_scope_overlap",
                },
            ]
        )

        self.assertEqual(groups[0]["top1_fingerprint_id"], "metal_dependent_hydrolase")
        self.assertEqual(groups[0]["cofactor_evidence_level"], "role_inferred")
        self.assertEqual(groups[0]["count"], 2)
        self.assertEqual(groups[0]["min_top1_score"], 0.5)
        self.assertEqual(groups[0]["mean_top1_score"], 0.55)
        self.assertEqual(groups[0]["max_top1_score"], 0.6)
        self.assertIsNone(groups[0]["min_score_gap_to_floor"])
        self.assertEqual(
            groups[0]["counterevidence_reason_counts"],
            {
                "role_inferred_metal_low_pocket_support": 1,
                "role_inferred_metal_missing_water_activation_role": 2,
            },
        )
        self.assertEqual(groups[0]["entry_ids"], ["m_csa:2", "m_csa:3"])

    def test_threshold_policy_prefers_zero_false_non_abstentions(self) -> None:
        rows = [
            {
                "abstain_threshold": 0.35,
                "top3_accuracy_in_scope": 1.0,
                "out_of_scope_abstention_rate": 0.5,
                "out_of_scope_false_non_abstentions": 2,
                "in_scope_retention_rate": 1.0,
                "top3_retained_accuracy_in_scope": 1.0,
            },
            {
                "abstain_threshold": 0.55,
                "top3_accuracy_in_scope": 1.0,
                "out_of_scope_abstention_rate": 0.75,
                "out_of_scope_false_non_abstentions": 1,
                "in_scope_retention_rate": 1.0,
                "top3_retained_accuracy_in_scope": 1.0,
            },
            {
                "abstain_threshold": 0.75,
                "top3_accuracy_in_scope": 1.0,
                "out_of_scope_abstention_rate": 1.0,
                "out_of_scope_false_non_abstentions": 0,
                "in_scope_retention_rate": 0.0,
                "top3_retained_accuracy_in_scope": 0.0,
            },
            {
                "abstain_threshold": 0.8,
                "top3_accuracy_in_scope": 1.0,
                "out_of_scope_abstention_rate": 1.0,
                "out_of_scope_false_non_abstentions": 0,
                "in_scope_retention_rate": 0.0,
                "top3_retained_accuracy_in_scope": 0.0,
            },
        ]
        selected = select_threshold(rows)
        self.assertIsNotNone(selected)
        self.assertEqual(selected["abstain_threshold"], 0.75)

        comparison = compare_threshold_policies(selected, rows[0], rows[1])
        self.assertFalse(comparison["same_threshold"])
        self.assertFalse(comparison["zero_false_preserves_retained_top3"])
        self.assertFalse(comparison["zero_false_preserves_in_scope_retention"])
        self.assertEqual(comparison["selected_out_of_scope_false_non_abstentions"], 0)
        self.assertEqual(comparison["legacy_out_of_scope_false_non_abstentions"], 2)
        self.assertEqual(comparison["retained_top3_reference_threshold"], 0.55)

    def test_analyze_out_of_scope_failures(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="example rationale long enough for in-scope",
            ),
            MechanismLabel(
                entry_id="m_csa:2",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="example rationale long enough for out-of-scope",
            ),
        ]
        retrieval = {
            "results": [
                {
                    "entry_id": "m_csa:1",
                    "top_fingerprints": [
                        {"fingerprint_id": "metal_dependent_hydrolase", "score": 0.8}
                    ],
                },
                {
                    "entry_id": "m_csa:2",
                    "top_fingerprints": [
                        {
                            "fingerprint_id": "flavin_monooxygenase",
                            "score": 0.84,
                            "residue_match_fraction": 0.1,
                            "role_match_fraction": 0.2,
                            "cofactor_context_score": 0.85,
                            "substrate_pocket_score": 0.2,
                            "compactness_score": 0.5,
                        }
                    ],
                },
            ]
        }
        analysis = analyze_out_of_scope_failures(retrieval, labels, abstain_threshold=0.75)
        self.assertEqual(analysis["metadata"]["false_non_abstentions"], 1)
        self.assertEqual(analysis["rows"][0]["evidence_pattern"], "cofactor_dominant")
        self.assertEqual(analysis["metadata"]["max_false_non_abstention_score"], 0.84)
        self.assertEqual(
            analysis["metadata"]["recommended_threshold_for_zero_current_false_non_abstentions"],
            0.85,
        )

    def test_analyze_in_scope_failures(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="example rationale long enough for correct hit",
            ),
            MechanismLabel(
                entry_id="m_csa:2",
                fingerprint_id="flavin_dehydrogenase_reductase",
                label_type="seed_fingerprint",
                confidence="medium",
                rationale="example rationale long enough for missed hit",
            ),
        ]
        retrieval = {
            "results": [
                {
                    "entry_id": "m_csa:1",
                    "top_fingerprints": [
                        {"fingerprint_id": "metal_dependent_hydrolase", "score": 0.8}
                    ],
                },
                {
                    "entry_id": "m_csa:2",
                    "entry_name": "missed flavin enzyme",
                    "mechanism_text_count": 1,
                    "mechanism_text_snippets": [
                        "The flavin accepts a hydride before product release."
                    ],
                    "ligand_context": {
                        "structure_ligand_codes": ["FAD"],
                        "structure_cofactor_families": ["flavin"],
                    },
                    "top_fingerprints": [
                        {
                            "fingerprint_id": "heme_peroxidase_oxidase",
                            "score": 0.4,
                            "residue_match_fraction": 1.0,
                            "cofactor_evidence_level": "absent",
                            "counterevidence_penalty": 0.75,
                            "counterevidence_reasons": ["absent_heme_context"],
                        },
                        {
                            "fingerprint_id": "flavin_dehydrogenase_reductase",
                            "score": 0.3,
                            "cofactor_context_score": 0.0,
                            "cofactor_evidence_level": "absent",
                        },
                    ],
                },
            ]
        }
        analysis = analyze_in_scope_failures(retrieval, labels, abstain_threshold=0.5)
        self.assertEqual(analysis["metadata"]["evaluated_in_scope_count"], 2)
        self.assertEqual(analysis["metadata"]["failure_count"], 1)
        self.assertEqual(analysis["metadata"]["actionable_failure_count"], 0)
        self.assertEqual(analysis["metadata"]["evidence_limited_abstention_count"], 1)
        self.assertEqual(analysis["metadata"]["top1_mismatch_count"], 1)
        self.assertEqual(analysis["metadata"]["abstained_positive_count"], 1)
        self.assertEqual(
            analysis["metadata"]["target_fingerprint_counts"],
            {"flavin_dehydrogenase_reductase": 1},
        )
        self.assertEqual(
            analysis["metadata"]["failure_cause_counts"],
            {"target_cofactor_not_proximal": 1},
        )
        self.assertEqual(
            analysis["metadata"]["top1_fingerprint_counts"],
            {"heme_peroxidase_oxidase": 1},
        )
        self.assertEqual(analysis["metadata"]["target_cofactor_evidence_counts"], {"absent": 1})
        self.assertEqual(analysis["rows"][0]["target_rank"], 2)
        self.assertEqual(analysis["rows"][0]["score_gap_top1_minus_target"], 0.1)
        self.assertEqual(analysis["rows"][0]["failure_cause"], "target_cofactor_not_proximal")
        self.assertEqual(analysis["rows"][0]["top1_cofactor_evidence_level"], "absent")
        self.assertEqual(analysis["rows"][0]["target_cofactor_evidence_level"], "absent")
        self.assertEqual(
            analysis["rows"][0]["target_cofactor_coverage_status"],
            "expected_structure_only",
        )
        self.assertEqual(analysis["rows"][0]["target_expected_cofactor_families"], ["flavin"])
        self.assertEqual(analysis["rows"][0]["context"]["entry_name"], "missed flavin enzyme")
        self.assertEqual(analysis["rows"][0]["context"]["mechanism_text_count"], 1)
        self.assertIn(
            "hydride",
            analysis["rows"][0]["context"]["mechanism_text_snippets"][0],
        )
        self.assertEqual(analysis["rows"][0]["context"]["structure_ligand_codes"], ["FAD"])
        self.assertEqual(
            analysis["rows"][0]["context"]["structure_cofactor_families"], ["flavin"]
        )
        self.assertIn("top1_component_scores", analysis["rows"][0])
        self.assertEqual(
            analysis["rows"][0]["top1_component_scores"]["counterevidence_reasons"],
            ["absent_heme_context"],
        )

    def test_analyze_cofactor_coverage(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="high",
                rationale="example rationale long enough for metal coverage",
            ),
            MechanismLabel(
                entry_id="m_csa:2",
                fingerprint_id="flavin_dehydrogenase_reductase",
                label_type="seed_fingerprint",
                confidence="medium",
                rationale="example rationale long enough for flavin coverage",
            ),
            MechanismLabel(
                entry_id="m_csa:3",
                fingerprint_id="ser_his_acid_hydrolase",
                label_type="seed_fingerprint",
                confidence="medium",
                rationale="example rationale long enough for no cofactor",
            ),
            MechanismLabel(
                entry_id="m_csa:4",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="medium",
                rationale="example rationale long enough for missing metal coverage",
            ),
        ]
        retrieval = {
            "results": [
                {
                    "entry_id": "m_csa:1",
                    "ligand_context": {
                        "cofactor_families": ["metal_ion"],
                        "structure_cofactor_families": ["metal_ion"],
                        "ligand_codes": ["ZN"],
                        "structure_ligand_codes": ["ZN"],
                        "structure_ligands": [
                            {
                                "code": "ZN",
                                "instance_count": 1,
                                "min_distance_to_active_site": 2.5,
                            }
                        ],
                    },
                    "top_fingerprints": [
                        {"fingerprint_id": "metal_dependent_hydrolase", "score": 0.8}
                    ],
                },
                {
                    "entry_id": "m_csa:2",
                    "entry_name": "flavin structure-only enzyme",
                    "mechanism_text_count": 1,
                    "mechanism_text_snippets": ["Flavin context is present but distal."],
                    "ligand_context": {
                        "cofactor_families": [],
                        "structure_cofactor_families": ["flavin"],
                        "ligand_codes": [],
                        "structure_ligand_codes": ["FAD"],
                        "structure_ligands": [
                            {
                                "code": "FAD",
                                "instance_count": 1,
                                "min_distance_to_active_site": 14.5,
                            }
                        ],
                    },
                    "top_fingerprints": [
                        {"fingerprint_id": "flavin_dehydrogenase_reductase", "score": 0.4}
                    ],
                },
                {
                    "entry_id": "m_csa:3",
                    "ligand_context": {},
                    "top_fingerprints": [
                        {"fingerprint_id": "ser_his_acid_hydrolase", "score": 0.6}
                    ],
                },
                {
                    "entry_id": "m_csa:4",
                    "ligand_context": {},
                    "top_fingerprints": [
                        {"fingerprint_id": "metal_dependent_hydrolase", "score": 0.9}
                    ],
                },
            ]
        }
        analysis = analyze_cofactor_coverage(retrieval, labels, abstain_threshold=0.5)
        self.assertEqual(analysis["metadata"]["evaluated_in_scope_count"], 4)
        self.assertEqual(
            analysis["metadata"]["coverage_status_counts"],
            {
                "all_expected_local": 1,
                "expected_absent_from_structure": 1,
                "expected_structure_only": 1,
                "not_required": 1,
            },
        )
        self.assertEqual(analysis["metadata"]["expected_absent_retained_count"], 1)
        self.assertEqual(analysis["metadata"]["expected_absent_entry_ids"], ["m_csa:4"])
        self.assertEqual(
            analysis["metadata"]["expected_absent_retained_entry_ids"],
            ["m_csa:4"],
        )
        self.assertEqual(analysis["metadata"]["expected_absent_abstained_entry_ids"], [])
        self.assertEqual(analysis["metadata"]["structure_only_retained_count"], 0)
        self.assertEqual(analysis["metadata"]["structure_only_retained_entry_ids"], [])
        self.assertEqual(
            analysis["metadata"]["structure_only_abstained_entry_ids"],
            ["m_csa:2"],
        )
        self.assertEqual(analysis["metadata"]["structure_only_entry_ids"], ["m_csa:2"])
        self.assertEqual(analysis["metadata"]["evidence_limited_retained_count"], 1)
        self.assertEqual(
            analysis["metadata"]["evidence_limited_retained_entry_ids"],
            ["m_csa:4"],
        )
        self.assertEqual(analysis["metadata"]["evidence_limited_abstained_count"], 1)
        self.assertEqual(
            analysis["metadata"]["evidence_limited_abstained_entry_ids"],
            ["m_csa:2"],
        )
        flavin_row = next(row for row in analysis["rows"] if row["entry_id"] == "m_csa:2")
        self.assertEqual(flavin_row["expected_cofactor_families"], ["flavin"])
        self.assertEqual(flavin_row["coverage_status"], "expected_structure_only")
        self.assertEqual(flavin_row["nearest_expected_ligand_distance_angstrom"], 14.5)
        self.assertEqual(flavin_row["matching_structure_ligands"][0]["code"], "FAD")
        self.assertEqual(flavin_row["context"]["entry_name"], "flavin structure-only enzyme")
        self.assertIn("distal", flavin_row["context"]["mechanism_text_snippets"][0])
        self.assertTrue(flavin_row["abstained"])

    def test_analyze_cofactor_abstention_policy(self) -> None:
        labels = [
            MechanismLabel(
                entry_id="m_csa:1",
                fingerprint_id="metal_dependent_hydrolase",
                label_type="seed_fingerprint",
                confidence="medium",
                rationale="example rationale long enough for retained absent cofactor",
            ),
            MechanismLabel(
                entry_id="m_csa:2",
                fingerprint_id="flavin_dehydrogenase_reductase",
                label_type="seed_fingerprint",
                confidence="medium",
                rationale="example rationale long enough for structure-only cofactor",
            ),
            MechanismLabel(
                entry_id="m_csa:3",
                fingerprint_id=None,
                label_type="out_of_scope",
                confidence="medium",
                rationale="example rationale long enough for out-of-scope row",
            ),
        ]
        retrieval = {
            "results": [
                {
                    "entry_id": "m_csa:1",
                    "status": "ok",
                    "resolved_residue_count": 3,
                    "ligand_context": {},
                    "top_fingerprints": [
                        {"fingerprint_id": "metal_dependent_hydrolase", "score": 0.56}
                    ],
                },
                {
                    "entry_id": "m_csa:2",
                    "status": "ok",
                    "resolved_residue_count": 3,
                    "ligand_context": {
                        "structure_cofactor_families": ["flavin"],
                        "structure_ligand_codes": ["FAD"],
                    },
                    "top_fingerprints": [
                        {
                            "fingerprint_id": "flavin_dehydrogenase_reductase",
                            "score": 0.53,
                        }
                    ],
                },
                {
                    "entry_id": "m_csa:3",
                    "status": "ok",
                    "resolved_residue_count": 3,
                    "top_fingerprints": [
                        {"fingerprint_id": "ser_his_acid_hydrolase", "score": 0.2}
                    ],
                },
            ]
        }

        analysis = analyze_cofactor_abstention_policy(
            retrieval,
            labels,
            abstain_threshold=0.5,
            absent_penalties=[0.0, 0.1],
            structure_only_penalties=[0.0, 0.04],
        )

        self.assertEqual(analysis["metadata"]["recommendation"], "audit_only_or_separate_stratum")
        self.assertEqual(
            analysis["metadata"]["audit_evidence_limited_retained_positive_entry_ids"],
            ["m_csa:1", "m_csa:2"],
        )
        self.assertEqual(
            analysis["metadata"]["lossless_decision_changing_policy_count"],
            0,
        )
        self.assertEqual(analysis["metadata"]["minimum_evidence_limited_retained_margin"], 0.03)
        self.assertEqual(
            [row["entry_id"] for row in analysis["sensitivity_rows"]],
            ["m_csa:1", "m_csa:2"],
        )
        self.assertEqual(
            analysis["sensitivity_rows"][1]["affected_penalty"],
            "structure_only_penalty",
        )
        absent_policy = next(
            row
            for row in analysis["policies"]
            if row["absent_penalty"] == 0.1 and row["structure_only_penalty"] == 0.0
        )
        self.assertEqual(absent_policy["lost_retained_positive_entry_ids"], ["m_csa:1"])
        structure_only_policy = next(
            row
            for row in analysis["policies"]
            if row["absent_penalty"] == 0.0 and row["structure_only_penalty"] == 0.04
        )
        self.assertEqual(structure_only_policy["lost_retained_positive_entry_ids"], ["m_csa:2"])
        limiting = [
            row
            for row in analysis["limiting_rows"]
            if row["entry_id"] == "m_csa:2" and row["structure_only_penalty"] == 0.04
        ][0]
        self.assertEqual(limiting["target_cofactor_coverage_status"], "expected_structure_only")
        self.assertTrue(limiting["lost_retained_positive"])

    def test_classify_out_of_scope_failure_near_threshold(self) -> None:
        category = classify_out_of_scope_failure(
            {"score": 0.76, "residue_match_fraction": 0.9, "role_match_fraction": 0.9},
            abstain_threshold=0.75,
        )
        self.assertEqual(category, "near_threshold")


if __name__ == "__main__":
    unittest.main()
