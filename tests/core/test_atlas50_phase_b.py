from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas50_phase_b import (
    PHASE_B_RELATIVE,
    build_phase_b_outputs,
    canonical_json_bytes,
    validate_freeze_candidate,
    validate_phase_b_package,
    validate_review_queue,
    validate_review_submission,
    validate_source_plan,
)


ROOT = Path(__file__).resolve().parents[2]
PHASE_A = ROOT / "data/atlas/atlas50/phase_a"
PHASE_B = ROOT / PHASE_B_RELATIVE


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class Atlas50PhaseBTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = _load(PHASE_B / "review_spec.json")
        cls.crosswalk = _load(PHASE_A / "crosswalk_draft.json")
        cls.matrix = _load(PHASE_A / "candidate_matrix.json")
        cls.proposal = _load(PHASE_A / "proposed_panel.json")
        cls.crosswalk_queue = _load(PHASE_B / "crosswalk_review_queue.json")
        cls.panel_queue = _load(PHASE_B / "panel_review_queue.json")
        cls.attempts = _load(PHASE_B / "review_attempts.json")
        cls.freeze_candidate = _load(PHASE_B / "freeze_candidate.json")
        cls.source_plan = _load(PHASE_B / "source_reacquisition_plan.json")

    def test_repository_package_is_byte_current_and_explicitly_unfrozen(self) -> None:
        summary = validate_phase_b_package(ROOT)

        self.assertEqual(summary["crosswalk_packets"], 57)
        self.assertEqual(summary["crosswalk_reviewed"], 0)
        self.assertEqual(summary["panel_packets"], 40)
        self.assertEqual(summary["panel_reviewed"], 0)
        self.assertEqual(summary["review_attempts"], 0)
        self.assertFalse(summary["selection_frozen"])
        self.assertEqual(summary["proposed_total"], 47)
        self.assertEqual(summary["planned_source_cases"], 37)
        self.assertEqual(summary["source_records_acquired"], 0)
        self.assertEqual(summary["compiled_follow_on_mechanisms"], 0)
        self.assertEqual(summary["gpu_hours"], 0)

    def test_all_review_packets_remain_unreviewed_and_source_bound(self) -> None:
        validate_review_queue(
            self.crosswalk_queue, self.crosswalk["rows"], "crosswalk"
        )
        validate_review_queue(self.panel_queue, self.matrix["rows"], "panel")

        self.assertEqual(len(self.crosswalk_queue["packets"]), 57)
        self.assertEqual(len(self.panel_queue["packets"]), 40)
        for packet in self.crosswalk_queue["packets"]:
            self.assertEqual(packet["review_state"]["status"], "unreviewed")
            self.assertEqual(len(packet["machine_draft"]["source_links"]), 13)
        for packet in self.panel_queue["packets"]:
            self.assertEqual(packet["review_state"]["status"], "unreviewed")
            self.assertFalse(
                packet["review_requirements"]["mechanism_compilation_permitted"]
            )

    def test_review_attempt_ledger_claims_no_contact_or_reviewer(self) -> None:
        self.assertEqual(self.attempts["status"], "no_review_or_outreach_attempted")
        self.assertEqual(self.attempts["attempts"], [])
        self.assertEqual(self.attempts["attempt_count"], 0)
        self.assertEqual(self.attempts["submission_count"], 0)
        self.assertEqual(self.attempts["identified_reviewer_count"], 0)
        self.assertEqual(self.attempts["external_messages_sent"], 0)
        self.assertFalse(self.attempts["review_claimed"])
        self.assertFalse(self.attempts["independent_annotation_claimed"])

    def test_freeze_candidate_is_exact_fail_closed_proposal_not_selection(self) -> None:
        validate_freeze_candidate(self.freeze_candidate, self.proposal)

        self.assertFalse(self.freeze_candidate["selection_frozen"])
        self.assertFalse(self.freeze_candidate["freeze_gate"]["ready"])
        self.assertEqual(
            self.freeze_candidate["freeze_gate"]["blocked_condition_count"], 6
        )
        self.assertEqual(
            self.freeze_candidate["candidate_panel"]["total_case_count"], 47
        )
        self.assertEqual(
            self.freeze_candidate["candidate_panel"]["shortfall_from_50"], 3
        )
        self.assertEqual(len(self.freeze_candidate["blocker_dispositions"]), 3)

    def test_source_plan_is_complete_but_not_authorized_or_executed(self) -> None:
        validate_source_plan(self.source_plan, self.matrix)

        self.assertEqual(self.source_plan["planned_case_count"], 37)
        self.assertEqual(self.source_plan["shared_lane_count"], 10)
        self.assertFalse(self.source_plan["may_execute"])
        self.assertFalse(self.source_plan["selection_frozen"])
        self.assertIsNone(
            self.source_plan["budget"]["post_freeze_external_requests_max"]
        )
        self.assertEqual(set(self.source_plan["actual_usage"].values()), {0})

    def test_phase_a_bytes_and_inherited_proofs_remain_current(self) -> None:
        proof = _load(PHASE_B / "inheritance_proof.json")

        self.assertTrue(proof["phase_a_unchanged"])
        self.assertTrue(proof["atlas3_atlas10_and_protected_registries_unchanged"])
        self.assertEqual(proof["phase_a_file_count"], 10)
        self.assertEqual(proof["phase_a_validation"]["crosswalk_rows"], 57)
        self.assertEqual(proof["phase_a_validation"]["proposed_total"], 47)

    def test_builder_is_deterministic_against_checked_outputs(self) -> None:
        expected = build_phase_b_outputs(ROOT)

        for filename, value in expected.items():
            self.assertEqual(
                (PHASE_B / filename).read_bytes(), canonical_json_bytes(value)
            )

    def test_attributable_crosswalk_submission_contract_accepts_complete_review(self) -> None:
        packet = self.crosswalk_queue["packets"][0]
        submission = self._valid_crosswalk_submission(packet)

        validate_review_submission(submission, packet, self.spec)

    def test_review_submission_cannot_claim_independent_annotation(self) -> None:
        packet = self.crosswalk_queue["packets"][0]
        submission = self._valid_panel_submission(self.panel_queue["packets"][0])
        submission["independent_annotation_claimed"] = True

        with self.assertRaisesRegex(ValueError, "independent annotation"):
            validate_review_submission(
                submission, self.panel_queue["packets"][0], self.spec
            )

        self.assertEqual(packet["review_state"]["status"], "unreviewed")

    def test_review_queue_cannot_be_upgraded_or_gain_compiled_fields(self) -> None:
        changed = copy.deepcopy(self.crosswalk_queue)
        changed["packets"][0]["review_state"]["status"] = "reviewed"
        with self.assertRaisesRegex(ValueError, "review status was upgraded"):
            validate_review_queue(changed, self.crosswalk["rows"], "crosswalk")

        changed = copy.deepcopy(self.panel_queue)
        changed["packets"][0]["machine_draft"]["mechanism_steps"] = [
            {"invented": True}
        ]
        with self.assertRaisesRegex(ValueError, "prohibited compiled fields"):
            validate_review_queue(changed, self.matrix["rows"], "panel")

    def test_selection_and_source_gates_cannot_be_lifted_by_edit(self) -> None:
        changed_freeze = copy.deepcopy(self.freeze_candidate)
        changed_freeze["selection_frozen"] = True
        with self.assertRaisesRegex(ValueError, "frozen without review"):
            validate_freeze_candidate(changed_freeze, self.proposal)

        changed_plan = copy.deepcopy(self.source_plan)
        changed_plan["may_execute"] = True
        with self.assertRaisesRegex(ValueError, "authorized before freeze"):
            validate_source_plan(changed_plan, self.matrix)

    def test_panel_review_revision_requires_evidence(self) -> None:
        packet = self.panel_queue["packets"][0]
        submission = self._valid_panel_submission(packet)
        submission["decision"]["outcome"] = "revise_with_evidence"

        with self.assertRaisesRegex(ValueError, "require evidence"):
            validate_review_submission(submission, packet, self.spec)

    def test_crosswalk_submission_rejects_contradictory_revision(self) -> None:
        packet = self.crosswalk_queue["packets"][0]
        submission = self._valid_crosswalk_submission(packet)
        submission["decision"]["field_decisions"][
            "classification"
        ] = "revise_classification"

        with self.assertRaisesRegex(ValueError, "conflicts with outcome"):
            validate_review_submission(submission, packet, self.spec)

    def test_crosswalk_source_confirmation_must_match_packet_gap_state(self) -> None:
        packet = self.crosswalk_queue["packets"][0]
        links = packet["machine_draft"]["source_links"]
        gap_key = next(key for key, link in links.items() if link["gap_reason"])
        mapped_key = next(key for key, link in links.items() if not link["gap_reason"])

        submission = self._valid_crosswalk_submission(packet)
        submission["decision"]["field_decisions"]["source_links"][
            gap_key
        ] = "confirm_candidate_mapping"
        with self.assertRaisesRegex(ValueError, "explicit source gap"):
            validate_review_submission(submission, packet, self.spec)

        submission = self._valid_crosswalk_submission(packet)
        submission["decision"]["field_decisions"]["source_links"][
            mapped_key
        ] = "confirm_explicit_gap"
        with self.assertRaisesRegex(ValueError, "none is recorded"):
            validate_review_submission(submission, packet, self.spec)

    def test_panel_acceptance_must_match_machine_draft_disposition(self) -> None:
        packet = next(
            item
            for item in self.panel_queue["packets"]
            if item["machine_draft"]["proposed_disposition"] == "exclude_blocked"
        )
        submission = self._valid_panel_submission(packet)
        submission["decision"]["outcome"] = "accept_proposed_include"

        with self.assertRaisesRegex(ValueError, "conflicts with machine-draft"):
            validate_review_submission(submission, packet, self.spec)

    def test_review_submission_enforces_identity_and_timestamp_types(self) -> None:
        packet = self.crosswalk_queue["packets"][0]
        changes = (
            (
                lambda submission: submission.update({"unexpected": True}),
                "declared schema",
            ),
            (
                lambda submission: submission["reviewer"].update(
                    {"project_author": "false"}
                ),
                "must be boolean",
            ),
            (
                lambda submission: submission["reviewer"].update(
                    {"reviewed_on": "not-a-date"}
                ),
                "must be ISO 8601",
            ),
            (
                lambda submission: submission.update({"submitted_at": "not-a-date"}),
                "must be RFC 3339",
            ),
            (
                lambda submission: submission.update(
                    {"submitted_at": "2026-07-14T00:00:00+00:99"}
                ),
                "must be RFC 3339",
            ),
        )
        for change, expected_error in changes:
            with self.subTest(expected_error=expected_error):
                submission = self._valid_crosswalk_submission(packet)
                change(submission)
                with self.assertRaisesRegex(ValueError, expected_error):
                    validate_review_submission(submission, packet, self.spec)

    def test_revision_evidence_reference_cannot_be_empty_placeholder(self) -> None:
        packet = self.panel_queue["packets"][0]
        submission = self._valid_panel_submission(packet)
        submission["decision"]["outcome"] = "revise_with_evidence"
        submission["evidence_references"] = [{}]

        with self.assertRaisesRegex(ValueError, "require evidence"):
            validate_review_submission(submission, packet, self.spec)

    def test_review_submission_cannot_introduce_compiled_chemistry(self) -> None:
        packet = self.panel_queue["packets"][0]
        submission = self._valid_panel_submission(packet)
        submission["decision"]["mechanism_steps"] = [{"invented": True}]

        with self.assertRaisesRegex(ValueError, "prohibited compiled fields"):
            validate_review_submission(submission, packet, self.spec)

    def _valid_crosswalk_submission(self, packet: dict) -> dict:
        source_decisions = {
            key: (
                "confirm_explicit_gap"
                if link["gap_reason"]
                else "confirm_candidate_mapping"
            )
            for key, link in packet["machine_draft"]["source_links"].items()
        }
        return {
            "schema_version": "catalytic-earth.atlas50-review-submission.v1",
            "submission_id": "review.example.crosswalk.fp-001",
            "packet_id": packet["packet_id"],
            "packet_type": "crosswalk",
            "packet_sha256": hashlib.sha256(canonical_json_bytes(packet)).hexdigest(),
            "reviewer": {
                "reviewer_id": "reviewer.example",
                "reviewer_display_name": "Example Reviewer",
                "expertise_context": "Contract-only synthetic test fixture",
                "reviewed_on": "2026-07-14",
                "project_author": False,
            },
            "attestation": self.spec["reviewer_evidence_contract"][
                "required_attestation"
            ],
            "decision": {
                "outcome": "accept_machine_draft",
                "rationale": "Synthetic complete submission used only to test the contract.",
                "uncertainty": [],
                "field_decisions": {
                    "classification": "accept_machine_draft",
                    "source_links": source_decisions,
                },
            },
            "evidence_references": [],
            "conflicts": [],
            "submitted_at": "2026-07-14T00:00:00Z",
            "independent_annotation_claimed": False,
        }

    def _valid_panel_submission(self, packet: dict) -> dict:
        outcome = (
            "accept_proposed_include"
            if packet["machine_draft"]["proposed_disposition"] == "propose_include"
            else "accept_fail_closed_exclusion"
        )
        return {
            "schema_version": "catalytic-earth.atlas50-review-submission.v1",
            "submission_id": "review.example.panel.m0001",
            "packet_id": packet["packet_id"],
            "packet_type": "panel",
            "packet_sha256": hashlib.sha256(canonical_json_bytes(packet)).hexdigest(),
            "reviewer": {
                "reviewer_id": "reviewer.example",
                "reviewer_display_name": "Example Reviewer",
                "expertise_context": "Contract-only synthetic test fixture",
                "reviewed_on": "2026-07-14",
                "project_author": False,
            },
            "attestation": self.spec["reviewer_evidence_contract"][
                "required_attestation"
            ],
            "decision": {
                "outcome": outcome,
                "rationale": "Synthetic complete submission used only to test the contract.",
                "uncertainty": [],
                "field_decisions": {
                    dimension: "accept_machine_draft_gate"
                    for dimension in self.spec["panel_review_contract"][
                        "review_dimensions"
                    ]
                },
            },
            "evidence_references": [],
            "conflicts": [],
            "submitted_at": "2026-07-14T00:00:00Z",
            "independent_annotation_claimed": False,
        }


if __name__ == "__main__":
    unittest.main()
