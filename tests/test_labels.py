from __future__ import annotations

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
    analyze_seed_family_performance,
    analyze_out_of_scope_failures,
    analyze_structure_mapping_issues,
    build_active_learning_review_queue,
    build_adversarial_negative_controls,
    build_expert_review_export,
    build_family_propagation_guardrails,
    build_hard_negative_controls,
    build_label_expansion_candidates,
    build_label_factory_audit,
    build_provisional_review_decision_batch,
    check_label_batch_acceptance,
    check_label_factory_gates,
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
    select_threshold,
    sweep_abstention_thresholds,
)


class LabelTests(unittest.TestCase):
    def test_load_labels(self) -> None:
        labels = load_labels()
        self.assertEqual(len(labels), 499)
        summary = label_summary(labels)
        self.assertGreater(summary["by_type"]["seed_fingerprint"], 0)
        self.assertGreater(summary["by_type"]["out_of_scope"], 0)
        self.assertEqual(summary["by_tier"]["bronze"], 499)
        self.assertEqual(summary["by_review_status"]["automation_curated"], 499)
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
        geometry = {"entries": [{"entry_id": "m_csa:8", "entry_name": "unlabeled proxy"}]}
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
            ]
        }
        guardrails = build_family_propagation_guardrails(geometry, retrieval, labels)
        decisions = {row["entry_id"]: row["propagation_decision"] for row in guardrails["rows"]}
        self.assertEqual(decisions["m_csa:1"], "block_family_propagation")
        self.assertEqual(decisions["m_csa:8"], "bronze_review_only")
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
