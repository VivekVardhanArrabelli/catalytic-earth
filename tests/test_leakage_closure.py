from __future__ import annotations

import json
import unittest
from pathlib import Path

from catalytic_earth.labels import load_labels
from catalytic_earth.transfer_scope import (
    EXTERNAL_HARD_NEGATIVE_ABSTAIN_THRESHOLD,
    EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_VERSION,
    EXTERNAL_HARD_NEGATIVE_THRESHOLD_POLICY_VERSION,
    build_external_hard_negative_next_candidate_factory_import_gate,
)


ROOT = Path(__file__).resolve().parents[1]
PILOT_REPAIR_CANDIDATES = {
    "O14756",
    "Q6NSJ0",
    "P34949",
    "Q9BXD5",
    "C9JRZ8",
    "P06746",
    "P55263",
    "O60568",
    "O95050",
    "P51580",
}
EXTERNAL_HARD_NEGATIVES = {
    "uniprot:P06744",
    "uniprot:P78549",
    "uniprot:Q3LXA3",
}
FORBIDDEN_PREDICTIVE_CONTEXT = (
    "protein_name",
    "ec_label",
    "uniprot_prose",
    "source_annotation",
    "curated_mechanism_text",
)


class LeakageClosureTests(unittest.TestCase):
    def test_pilot_repair_lanes_are_not_clean_performance_evidence(self) -> None:
        artifact = _load_json(
            ROOT / "artifacts" / "v3_external_pilot_repair_leakage_closure_1025.json"
        )

        self.assertEqual(set(artifact["candidates"]), PILOT_REPAIR_CANDIDATES)
        self.assertEqual(
            artifact["metadata"]["clean_performance_evidence_candidate_count"], 0
        )
        self.assertEqual(
            artifact["decision"]["classification"],
            "development_review_evidence_not_clean_performance_evidence",
        )
        self.assertTrue(
            artifact["metadata"][
                "rules_frozen_before_future_candidate_selection_required"
            ]
        )

    def test_next_tranche_pre_registration_is_frozen_before_selection(self) -> None:
        artifact = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_hard_negative_next_tranche_preregistration_1025.json"
        )
        metadata = artifact["metadata"]
        fingerprints = _load_json(
            ROOT / "data" / "registries" / "mechanism_fingerprints.json"
        )
        expected_fingerprints = sorted(row["id"] for row in fingerprints)

        self.assertEqual(
            metadata["version"],
            EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_VERSION,
        )
        self.assertEqual(
            metadata["registration_status"], "frozen_before_candidate_selection"
        )
        self.assertFalse(metadata["candidate_selection_started"])
        self.assertEqual(
            sorted(metadata["fingerprint_universe"]), expected_fingerprints
        )
        self.assertEqual(
            metadata["ontology_version_at_decision"], "label_factory_v1_8fp"
        )
        self.assertEqual(
            metadata["threshold_policy_version"],
            EXTERNAL_HARD_NEGATIVE_THRESHOLD_POLICY_VERSION,
        )
        self.assertEqual(
            metadata["abstain_threshold"], EXTERNAL_HARD_NEGATIVE_ABSTAIN_THRESHOLD
        )
        self.assertEqual(
            metadata["inverse_gate_rule"], "all_current_fingerprints_below_floor"
        )
        self.assertIn("excluded_context", artifact["frozen_rules"])

    def test_factory_import_gate_blocks_next_tranche_without_preregistration(self) -> None:
        gate = build_external_hard_negative_next_candidate_factory_import_gate(
            terminal_review_decisions=_terminal_review_decisions(),
            label_factory_gate_check=_passed_label_factory_gate(),
            external_transfer_gate=_passed_external_transfer_gate(),
            existing_label_entry_ids=[],
            max_imports=1,
            require_pre_registration=True,
        )

        self.assertFalse(gate["metadata"]["ready_for_label_import"])
        self.assertEqual(gate["metadata"]["selected_import_accessions"], [])
        self.assertIn(
            "external_hard_negative_pre_registration_missing",
            gate["rows"][0]["remaining_import_blockers"],
        )

    def test_factory_import_gate_accepts_frozen_preregistration(self) -> None:
        prereg = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_hard_negative_next_tranche_preregistration_1025.json"
        )
        gate = build_external_hard_negative_next_candidate_factory_import_gate(
            terminal_review_decisions=_terminal_review_decisions(),
            label_factory_gate_check=_passed_label_factory_gate(),
            external_transfer_gate=_passed_external_transfer_gate(),
            existing_label_entry_ids=[],
            max_imports=1,
            pre_registration=prereg,
            pre_registration_artifact_path=(
                "artifacts/v3_external_hard_negative_next_tranche_preregistration_1025.json"
            ),
            require_pre_registration=True,
        )

        self.assertTrue(gate["metadata"]["ready_for_label_import"])
        self.assertEqual(gate["metadata"]["selected_import_accessions"], ["PTEST"])
        self.assertEqual(
            gate["metadata"]["pre_registration_reference"]["version"],
            EXTERNAL_HARD_NEGATIVE_NEXT_TRANCHE_PREREGISTRATION_VERSION,
        )
        self.assertEqual(gate["rows"][0]["remaining_import_blockers"], [])
        separation = gate["rows"][0]["evidence_separation"]
        self.assertIn("predictive_evidence", separation)
        self.assertIn("import_gate_evidence", separation)
        self.assertIn("review_only_context", separation)
        self.assertIn("excluded_context", separation)

    def test_threshold_policy_pins_external_import_floor(self) -> None:
        policy = _load_json(
            ROOT / "artifacts" / "v3_external_hard_negative_threshold_policy_1025.json"
        )
        self.assertEqual(
            policy["metadata"]["version"],
            EXTERNAL_HARD_NEGATIVE_THRESHOLD_POLICY_VERSION,
        )
        self.assertEqual(
            policy["metadata"]["abstain_threshold"],
            EXTERNAL_HARD_NEGATIVE_ABSTAIN_THRESHOLD,
        )
        self.assertFalse(policy["metadata"]["candidate_or_tranche_tuning_permitted"])

        for path in (
            "artifacts/v3_external_hard_negative_next_candidate_factory_import_gate_1025.json",
            "artifacts/v3_external_hard_negative_q3lxa3_single_import_cycle_gate_1025.json",
            "artifacts/v3_external_hard_negative_broader_structural_factory_import_gate_1025.json",
        ):
            artifact = _load_json(ROOT / path)
            for row in artifact["rows"]:
                if row.get("ready_for_label_import"):
                    inverse_gate = row["out_of_scope_inverse_gate"]
                    self.assertEqual(
                        inverse_gate["abstain_threshold"],
                        EXTERNAL_HARD_NEGATIVE_ABSTAIN_THRESHOLD,
                    )
                    self.assertEqual(
                        inverse_gate["ontology_version_at_decision"],
                        "label_factory_v1_8fp",
                    )

    def test_external_label_evidence_separates_review_context(self) -> None:
        labels = {label.entry_id: label for label in load_labels()}
        self.assertEqual(
            set(entry for entry in labels if entry.startswith("uniprot:")),
            EXTERNAL_HARD_NEGATIVES,
        )

        for entry_id in EXTERNAL_HARD_NEGATIVES:
            evidence = labels[entry_id].evidence
            for key in (
                "predictive_evidence",
                "import_gate_evidence",
                "review_only_context",
                "excluded_context",
            ):
                self.assertIsInstance(evidence[key], list)
                self.assertTrue(evidence[key])
            predictive_blob = json.dumps(evidence["predictive_evidence"]).lower()
            for term in FORBIDDEN_PREDICTIVE_CONTEXT:
                self.assertNotIn(term, predictive_blob)

    def test_ontology_reaudit_policy_lists_external_hard_negatives(self) -> None:
        artifact = _load_json(
            ROOT
            / "artifacts"
            / "v3_external_hard_negative_ontology_reaudit_policy_1025.json"
        )
        self.assertTrue(
            artifact["metadata"]["re_audit_required_on_positive_fingerprint_expansion"]
        )
        self.assertEqual(
            {row["entry_id"] for row in artifact["external_labels_requiring_reaudit"]},
            EXTERNAL_HARD_NEGATIVES,
        )
        for trigger in ("epk", "sdr", "akr", "glycoside_hydrolase", "isomerase", "lyase"):
            self.assertIn(trigger, artifact["expansion_triggers"])

    def test_mcsa_strict_structural_ood_claim_stays_disabled(self) -> None:
        adjudication = _load_json(
            ROOT / "artifacts" / "v3_mcsa_tm_holdout_feasibility_adjudication_1000.json"
        )
        self.assertFalse(
            adjudication["metadata"]["full_tm_score_holdout_claim_permitted"]
        )
        for path in (
            ROOT / "README.md",
            ROOT / "docs" / "external_source_transfer.md",
            ROOT / "work" / "handoff.md",
            ROOT / "work" / "scope.md",
        ):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("full_tm_score_holdout_claim_permitted=true", text)
            self.assertNotIn("resume M-CSA strict-TM round repair", text)


def _terminal_review_decisions() -> dict:
    return {
        "metadata": {
            "method": "external_hard_negative_next_candidate_terminal_review_decisions"
        },
        "rows": [
            {
                "accession": "PTEST",
                "entry_id": "uniprot:PTEST",
                "lane_id": "test_lane",
                "target_label_type": "out_of_scope",
                "target_fingerprint_id": None,
                "ontology_version_at_decision": "label_factory_v1_8fp",
                "terminal_review_decision_status": (
                    "accepted_out_of_scope_pending_factory_gate"
                ),
                "source_evidence_status": (
                    "explicit_active_site_and_catalytic_activity_source_present"
                ),
                "bounded_duplicate_evidence_status": (
                    "bounded_duplicate_controls_clear_uniref_pending"
                ),
                "uniref_current_reference_screen_status": (
                    "uniref_current_reference_screen_no_current_reference_overlap"
                ),
                "out_of_scope_inverse_gate": {
                    "inverse_gate_status": "passed",
                    "target_label_type": "out_of_scope",
                    "target_fingerprint_id": None,
                    "ontology_version_at_decision": "label_factory_v1_8fp",
                    "threshold_policy_version": (
                        EXTERNAL_HARD_NEGATIVE_THRESHOLD_POLICY_VERSION
                    ),
                    "abstain_threshold": EXTERNAL_HARD_NEGATIVE_ABSTAIN_THRESHOLD,
                    "expected_current_fingerprint_count": 8,
                    "observed_current_fingerprint_count": 8,
                    "all_current_fingerprint_scores_below_threshold": True,
                    "max_current_fingerprint_score": 0.2,
                    "current_fingerprint_scores": {
                        "cobalamin_radical_rearrangement": 0.1,
                        "flavin_dehydrogenase_reductase": 0.1,
                        "flavin_monooxygenase": 0.1,
                        "heme_peroxidase_oxidase": 0.1,
                        "metal_dependent_hydrolase": 0.2,
                        "plp_dependent_enzyme": 0.1,
                        "radical_sam_enzyme": 0.1,
                        "ser_his_acid_hydrolase": 0.1,
                    },
                },
                "top1_fingerprint_id": "metal_dependent_hydrolase",
                "top1_score": 0.2,
                "max_current_fingerprint_score": 0.2,
                "remaining_import_blockers": ["full_label_factory_gate_not_run"],
            }
        ],
    }


def _passed_label_factory_gate() -> dict:
    return {
        "metadata": {
            "method": "label_factory_gate_check",
            "gate_count": 1,
            "passed_gate_count": 1,
        },
        "blockers": [],
    }


def _passed_external_transfer_gate() -> dict:
    return {
        "metadata": {
            "method": "external_source_transfer_gate_check",
            "guardrail_clean": True,
        },
        "blockers": [],
    }


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    unittest.main()
